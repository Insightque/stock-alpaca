#!/usr/bin/env python3
"""Capture scheduler-owned research MCP preflight data.

This script talks to local research MCP wrappers over stdio. It is intended for
scheduled Codex runs where nested non-interactive sessions can produce false
tool-catalog or approval cancellations. It never submits orders and never
prints API keys.
"""

from __future__ import annotations

import argparse
import asyncio
import contextlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT_DIR = Path(__file__).resolve().parents[1]
DEFAULT_FRED_SERIES = ["DGS10", "DGS2", "FEDFUNDS", "CPIAUCSL", "UNRATE", "NFCI"]
DEFAULT_MAX_SYMBOLS = 12
DEFAULT_MCP_TIMEOUT_SECONDS = 75
MCP_TIMEOUT_SECONDS = DEFAULT_MCP_TIMEOUT_SECONDS
STDERR_CAPTURE_LIMIT = 4000
STDIO_READ_LIMIT = 8 * 1024 * 1024
POSITIVE_OUTCOMES = {"pass", "usable", "ok"}
SYSTEMIC_GAP_CATEGORIES = {"timeout", "cancelled", "dns", "auth", "wrapper_error"}


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_env(root: Path = ROOT_DIR) -> dict[str, str]:
    env = os.environ.copy()
    env_file = root / ".env"
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            if not stripped or stripped.startswith("#") or "=" not in stripped:
                continue
            if stripped.startswith("export "):
                stripped = stripped[len("export ") :].strip()
            key, value = stripped.split("=", 1)
            env.setdefault(key.strip(), value.strip().strip('"').strip("'"))
    return env


def classify_error(exc: BaseException) -> str:
    text = str(exc).lower()
    if "cancelled" in text or "canceled" in text or "user cancelled" in text:
        return "cancelled"
    if "could not resolve host" in text or "nodename nor servname" in text:
        return "dns"
    if "api_key" in text or "unauthorized" in text or "forbidden" in text:
        return "auth"
    if "timed out" in text or "timeout" in text:
        return "timeout"
    if "iserror" in text or "api request failed" in text:
        return "provider_error"
    return "unknown"


def encode_message(payload: dict[str, Any], *, protocol: str) -> bytes:
    body = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    if protocol == "jsonl":
        return body + b"\n"
    return f"Content-Length: {len(body)}\r\n\r\n".encode("ascii") + body


async def write_message(writer: asyncio.StreamWriter, payload: dict[str, Any], *, protocol: str) -> None:
    writer.write(encode_message(payload, protocol=protocol))
    await writer.drain()


async def read_message(reader: asyncio.StreamReader, *, protocol: str) -> dict[str, Any]:
    if protocol == "jsonl":
        line = await reader.readline()
        if not line:
            raise RuntimeError("MCP server closed stdout before responding.")
        payload = json.loads(line.decode("utf-8"))
        if not isinstance(payload, dict):
            raise RuntimeError("MCP response body was not a JSON object.")
        return payload

    headers: dict[str, str] = {}
    while True:
        line = await reader.readline()
        if not line:
            raise RuntimeError("MCP server closed stdout before responding.")
        if line in (b"\r\n", b"\n"):
            break
        key, _, value = line.decode("ascii", errors="replace").partition(":")
        headers[key.lower()] = value.strip()
    length_raw = headers.get("content-length")
    if not length_raw:
        raise RuntimeError("MCP response missing Content-Length header.")
    body = await reader.readexactly(int(length_raw))
    payload = json.loads(body.decode("utf-8"))
    if not isinstance(payload, dict):
        raise RuntimeError("MCP response body was not a JSON object.")
    return payload


async def drain_stderr(reader: asyncio.StreamReader | None, chunks: list[bytes]) -> None:
    if reader is None:
        return
    while True:
        chunk = await reader.read(1024)
        if not chunk:
            return
        current = sum(len(item) for item in chunks)
        if current < STDERR_CAPTURE_LIMIT:
            chunks.append(chunk[: STDERR_CAPTURE_LIMIT - current])


def parse_tool_payload(result: dict[str, Any]) -> dict[str, Any]:
    if result.get("isError"):
        text = "MCP tool returned isError=true"
        for item in result.get("content") or []:
            if isinstance(item, dict) and item.get("text"):
                text = str(item["text"])
                break
        raise RuntimeError(text)

    text_fallbacks: list[str] = []
    for item in result.get("content") or []:
        if not isinstance(item, dict) or not item.get("text"):
            continue
        text = str(item["text"])
        if text.lower().startswith("error:"):
            raise RuntimeError(text)
        try:
            payload = json.loads(text)
        except json.JSONDecodeError:
            text_fallbacks.append(text[:500])
            continue
        if isinstance(payload, dict):
            return payload
        if isinstance(payload, list):
            return {"items": payload}
    if text_fallbacks:
        return {"text": text_fallbacks[0]}
    raise RuntimeError(f"Could not parse MCP tool response as JSON: {result}")


async def create_stdio_process(command: Path, env: dict[str, str]) -> asyncio.subprocess.Process:
    proc_args = [str(command)]
    if command.suffix == ".sh" and not os.access(command, os.X_OK):
        proc_args = ["/bin/bash", str(command)]
    return await asyncio.create_subprocess_exec(
        *proc_args,
        cwd=str(ROOT_DIR),
        env=env,
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        limit=STDIO_READ_LIMIT,
    )


async def call_stdio_tool(
    *,
    command: Path,
    env: dict[str, str],
    tool_name: str,
    arguments: dict[str, Any],
    protocol: str = "headers",
) -> dict[str, Any]:
    return (
        await call_stdio_tool_sequence(
            command=command,
            env=env,
            calls=[(tool_name, arguments)],
            protocol=protocol,
        )
    )[0]


async def call_stdio_tool_sequence(
    *,
    command: Path,
    env: dict[str, str],
    calls: list[tuple[str, dict[str, Any]]],
    protocol: str = "headers",
) -> list[dict[str, Any]]:
    proc = await create_stdio_process(command, env)
    if proc.stdin is None or proc.stdout is None:
        raise RuntimeError("MCP subprocess did not expose stdio pipes.")

    stderr_chunks: list[bytes] = []
    stderr_task = asyncio.create_task(drain_stderr(proc.stderr, stderr_chunks))

    async def exchange() -> list[dict[str, Any]]:
        await write_message(
            proc.stdin,
            {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {},
                    "clientInfo": {"name": "stock-alpaca-scheduler-preflight", "version": "0.2.0"},
                },
            },
            protocol=protocol,
        )
        initialized = await read_message(proc.stdout, protocol=protocol)
        if "error" in initialized:
            raise RuntimeError(f"MCP initialize failed: {initialized['error']}")
        await write_message(
            proc.stdin,
            {"jsonrpc": "2.0", "method": "notifications/initialized", "params": {}},
            protocol=protocol,
        )

        payloads: list[dict[str, Any]] = []
        for index, (tool_name, arguments) in enumerate(calls, start=2):
            await write_message(
                proc.stdin,
                {
                    "jsonrpc": "2.0",
                    "id": index,
                    "method": "tools/call",
                    "params": {"name": tool_name, "arguments": arguments},
                },
                protocol=protocol,
            )
            response = await read_message(proc.stdout, protocol=protocol)
            if "error" in response:
                raise RuntimeError(f"MCP tools/call failed: {response['error']}")
            payloads.append(parse_tool_payload(response.get("result") or {}))
        return payloads

    try:
        return await asyncio.wait_for(exchange(), timeout=MCP_TIMEOUT_SECONDS)
    except asyncio.TimeoutError as exc:
        raise TimeoutError(f"MCP stdio call sequence timed out after {MCP_TIMEOUT_SECONDS}s") from exc
    finally:
        if proc.stdin and not proc.stdin.is_closing():
            proc.stdin.close()
            with contextlib.suppress(Exception):
                await proc.stdin.wait_closed()
        if proc.returncode is None:
            proc.terminate()
            with contextlib.suppress(asyncio.TimeoutError):
                await asyncio.wait_for(proc.wait(), timeout=5)
        if proc.returncode is None:
            proc.kill()
            await proc.wait()
        stderr_task.cancel()
        with contextlib.suppress(asyncio.CancelledError):
            await stderr_task


async def call_with_retries(
    *,
    command: Path,
    env: dict[str, str],
    tool_name: str,
    arguments: dict[str, Any],
    retries: int,
    protocol: str = "headers",
) -> dict[str, Any]:
    last_error: BaseException | None = None
    for attempt in range(retries + 1):
        try:
            payload = await call_stdio_tool(
                command=command,
                env=env,
                tool_name=tool_name,
                arguments=arguments,
                protocol=protocol,
            )
            return {"outcome": "pass", "payload": payload, "retry_count": attempt}
        except Exception as exc:  # noqa: BLE001 - preflight should classify and continue.
            last_error = exc
            if attempt < retries:
                await asyncio.sleep(1 + attempt)
    assert last_error is not None
    return {
        "outcome": "failed",
        "gap_category": classify_error(last_error),
        "gap_reason": str(last_error)[:240],
        "retry_count": retries,
    }


def parse_symbols(value: str) -> list[str]:
    seen: set[str] = set()
    symbols: list[str] = []
    for raw in value.split(","):
        symbol = raw.strip().upper()
        if not symbol or symbol in seen:
            continue
        seen.add(symbol)
        symbols.append(symbol)
    return symbols


def load_cik_map(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    rows = payload.get("symbols") if isinstance(payload, dict) else {}
    if not isinstance(rows, dict):
        return {}
    ciks: dict[str, str] = {}
    for symbol, row in rows.items():
        if not isinstance(row, dict):
            continue
        cik = str(row.get("cik") or "").strip()
        if cik:
            ciks[str(symbol).upper()] = cik
    return ciks


def quote_spread_pct(quote: dict[str, Any]) -> float | None:
    try:
        bid = float(quote.get("bp"))
        ask = float(quote.get("ap"))
    except (TypeError, ValueError):
        return None
    if bid <= 0 or ask <= 0 or ask < bid:
        return None
    midpoint = (bid + ask) / 2.0
    if midpoint <= 0:
        return None
    return (ask - bid) / midpoint * 100.0


def extract_symbols_from_alpaca_preflight(path: Path | None, *, max_symbols: int) -> list[str]:
    if not path or not path.exists():
        return []
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []
    if not isinstance(payload, dict):
        return []

    ranked: list[tuple[float, str]] = []
    quote_rows = payload.get("tool_results", {})
    if isinstance(quote_rows, dict):
        quote_rows = quote_rows.get("get_stock_latest_quote", {})
    batches = quote_rows.get("batches", []) if isinstance(quote_rows, dict) else []
    for batch in batches if isinstance(batches, list) else []:
        batch_payload = batch.get("payload") if isinstance(batch, dict) else {}
        quotes = batch_payload.get("quotes") if isinstance(batch_payload, dict) else {}
        if not isinstance(quotes, dict):
            continue
        for symbol, quote in quotes.items():
            if not isinstance(quote, dict):
                continue
            spread = quote_spread_pct(quote)
            if spread is not None:
                ranked.append((spread, str(symbol).upper()))

    if ranked:
        output: list[str] = []
        seen: set[str] = set()
        for _, symbol in sorted(ranked):
            if symbol in seen:
                continue
            seen.add(symbol)
            output.append(symbol)
            if len(output) >= max_symbols:
                return output

    universe = payload.get("universe_symbols")
    if isinstance(universe, list):
        return [str(symbol).upper() for symbol in universe[:max_symbols] if str(symbol).strip()]
    return []


def provider_row(
    *,
    server: str,
    queried: bool,
    outcome: str,
    checked_at: str,
    gap_category: str,
    gap_reason: str,
    retry_count: int,
    tool: str | None = None,
    payload: Any | None = None,
    per_symbol: dict[str, Any] | None = None,
) -> dict[str, Any]:
    row: dict[str, Any] = {
        "server": server,
        "queried": queried,
        "outcome": outcome,
        "checked_at": checked_at,
        "gap_category": gap_category,
        "gap_reason": gap_reason,
        "retry_count": retry_count,
    }
    if tool:
        row["tool"] = tool
    if payload is not None:
        row["payload"] = payload
    if per_symbol is not None:
        row["per_symbol"] = per_symbol
    return row


def alpha_news_item_count(payload: dict[str, Any]) -> int:
    for key in ("feed", "items", "data"):
        value = payload.get(key)
        if isinstance(value, list):
            return len(value)
    return 0


def gap_from_failed_call(row: dict[str, Any]) -> tuple[str, str]:
    return (
        str(row.get("gap_category") or "provider_error"),
        str(row.get("gap_reason") or "MCP provider call failed.")[:240],
    )


def skipped_after(row: dict[str, Any], tool_name: str) -> dict[str, Any]:
    gap_category, gap_reason = gap_from_failed_call(row)
    return {
        "outcome": "failed",
        "gap_category": gap_category,
        "gap_reason": f"Skipped {tool_name} after prior provider call failed: {gap_reason}"[:240],
        "retry_count": 0,
    }


async def capture_fred(env: dict[str, str]) -> dict[str, Any]:
    checked_at = now_utc()
    if not env.get("FRED_API_KEY"):
        return provider_row(
            server="fred",
            queried=True,
            outcome="unavailable",
            checked_at=checked_at,
            gap_category="auth",
            gap_reason="FRED_API_KEY is not present in the scheduler environment.",
            retry_count=0,
        )
    try:
        payload = await call_stdio_tool(
            command=ROOT_DIR / "scripts" / "mcp-fred.sh",
            env=env,
            tool_name="get_macro_snapshot",
            arguments={"series_ids": DEFAULT_FRED_SERIES},
        )
    except Exception as exc:
        return provider_row(
            server="fred",
            queried=True,
            outcome="failed",
            checked_at=checked_at,
            gap_category=classify_error(exc),
            gap_reason=str(exc)[:240],
            retry_count=0,
        )
    return provider_row(
        server="fred",
        queried=True,
        outcome="pass",
        checked_at=checked_at,
        gap_category="not_applicable",
        gap_reason="",
        retry_count=0,
        tool="get_macro_snapshot",
        payload=payload,
    )


async def capture_sec_edgar(env: dict[str, str], symbols: list[str], ciks: dict[str, str]) -> dict[str, Any]:
    checked_at = now_utc()
    if not env.get("SEC_EDGAR_USER_AGENT"):
        return provider_row(
            server="sec-edgar",
            queried=True,
            outcome="unavailable",
            checked_at=checked_at,
            gap_category="auth",
            gap_reason="SEC_EDGAR_USER_AGENT is not present in the scheduler environment.",
            retry_count=0,
        )
    if not symbols:
        return provider_row(
            server="sec-edgar",
            queried=True,
            outcome="gap",
            checked_at=checked_at,
            gap_category="empty_response",
            gap_reason="No candidate symbols were available for SEC EDGAR preflight.",
            retry_count=0,
        )

    command = ROOT_DIR / "scripts" / "mcp-sec-edgar.sh"
    per_symbol: dict[str, Any] = {}
    pass_count = 0
    max_retry = 0
    first_gap_category = ""
    first_gap_reason = ""
    for symbol in symbols:
        cik = ciks.get(symbol)
        if not cik:
            per_symbol[symbol] = {
                "outcome": "gap",
                "gap_category": "empty_response",
                "gap_reason": "symbol missing from local SEC ticker-CIK cache; likely ETF/non-company lookup gap",
            }
            continue
        company = await call_with_retries(
            command=command,
            env=env,
            tool_name="get_company_info",
            arguments={"identifier": cik},
            retries=1,
            protocol="jsonl",
        )
        if company["outcome"] != "pass":
            first_gap_category, first_gap_reason = first_gap_category or gap_from_failed_call(company)[0], (
                first_gap_reason or gap_from_failed_call(company)[1]
            )
            per_symbol[symbol] = {
                "cik": cik,
                "outcome": "failed",
                "company_info": company,
                "recent_filings": skipped_after(company, "get_recent_filings"),
            }
            max_retry = max(max_retry, int(company.get("retry_count", 0)))
            if company.get("gap_category") in SYSTEMIC_GAP_CATEGORIES:
                break
            continue
        filings = await call_with_retries(
            command=command,
            env=env,
            tool_name="get_recent_filings",
            arguments={"identifier": cik, "days": 30, "limit": 5},
            retries=1,
            protocol="jsonl",
        )
        max_retry = max(max_retry, int(company.get("retry_count", 0)), int(filings.get("retry_count", 0)))
        symbol_outcome = "pass" if company["outcome"] == "pass" and filings["outcome"] == "pass" else "failed"
        if filings["outcome"] != "pass":
            first_gap_category, first_gap_reason = first_gap_category or gap_from_failed_call(filings)[0], (
                first_gap_reason or gap_from_failed_call(filings)[1]
            )
        if symbol_outcome == "pass":
            pass_count += 1
        per_symbol[symbol] = {
            "cik": cik,
            "outcome": symbol_outcome,
            "company_info": company,
            "recent_filings": filings,
        }
        if symbol_outcome != "pass" and filings.get("gap_category") in SYSTEMIC_GAP_CATEGORIES:
            break

    return provider_row(
        server="sec-edgar",
        queried=True,
        outcome="pass" if pass_count else "failed",
        checked_at=checked_at,
        gap_category="not_applicable" if pass_count else first_gap_category or "provider_error",
        gap_reason="" if pass_count else first_gap_reason or "No candidate symbol returned both company info and recent filings.",
        retry_count=max_retry,
        tool="get_company_info|get_recent_filings",
        per_symbol=per_symbol,
    )


async def capture_yahoo_finance(env: dict[str, str], symbols: list[str]) -> dict[str, Any]:
    checked_at = now_utc()
    if not symbols:
        return provider_row(
            server="yahoo-finance",
            queried=True,
            outcome="gap",
            checked_at=checked_at,
            gap_category="empty_response",
            gap_reason="No candidate symbols were available for Yahoo Finance preflight.",
            retry_count=0,
        )

    command = ROOT_DIR / "scripts" / "mcp-yahoo-finance.sh"
    per_symbol: dict[str, Any] = {}
    pass_count = 0
    max_retry = 0
    first_gap_category = ""
    first_gap_reason = ""
    for symbol in symbols:
        recommendations = await call_with_retries(
            command=command,
            env=env,
            tool_name="get_recommendations",
            arguments={"ticker": symbol, "recommendation_type": "recommendations", "months_back": 12},
            retries=1,
            protocol="jsonl",
        )
        if recommendations["outcome"] != "pass":
            first_gap_category, first_gap_reason = first_gap_category or gap_from_failed_call(recommendations)[0], (
                first_gap_reason or gap_from_failed_call(recommendations)[1]
            )
            if recommendations.get("gap_category") in SYSTEMIC_GAP_CATEGORIES:
                per_symbol[symbol] = {
                    "outcome": "failed",
                    "recommendations": recommendations,
                    "news": skipped_after(recommendations, "get_yahoo_finance_news"),
                }
                max_retry = max(max_retry, int(recommendations.get("retry_count", 0)))
                break
        news = await call_with_retries(
            command=command,
            env=env,
            tool_name="get_yahoo_finance_news",
            arguments={"ticker": symbol},
            retries=1,
            protocol="jsonl",
        )
        max_retry = max(max_retry, int(recommendations.get("retry_count", 0)), int(news.get("retry_count", 0)))
        symbol_pass = recommendations["outcome"] == "pass" or news["outcome"] == "pass"
        if news["outcome"] != "pass":
            first_gap_category, first_gap_reason = first_gap_category or gap_from_failed_call(news)[0], (
                first_gap_reason or gap_from_failed_call(news)[1]
            )
        if symbol_pass:
            pass_count += 1
        per_symbol[symbol] = {
            "outcome": "pass" if symbol_pass else "failed",
            "recommendations": recommendations,
            "news": news,
        }
        if not symbol_pass and news.get("gap_category") in SYSTEMIC_GAP_CATEGORIES:
            break

    return provider_row(
        server="yahoo-finance",
        queried=True,
        outcome="pass" if pass_count else "failed",
        checked_at=checked_at,
        gap_category="not_applicable" if pass_count else first_gap_category or "provider_error",
        gap_reason="" if pass_count else first_gap_reason or "No Yahoo Finance candidate call returned usable data.",
        retry_count=max_retry,
        tool="get_recommendations|get_yahoo_finance_news",
        per_symbol=per_symbol,
    )


async def capture_alpha_vantage(env: dict[str, str], symbols: list[str]) -> dict[str, Any]:
    checked_at = now_utc()
    if not env.get("ALPHA_VANTAGE_API_KEY"):
        return provider_row(
            server="alpha-vantage",
            queried=True,
            outcome="unavailable",
            checked_at=checked_at,
            gap_category="auth",
            gap_reason="ALPHA_VANTAGE_API_KEY is not present in the scheduler environment.",
            retry_count=0,
        )
    if not symbols:
        return provider_row(
            server="alpha-vantage",
            queried=True,
            outcome="gap",
            checked_at=checked_at,
            gap_category="empty_response",
            gap_reason="No candidate symbols were available for Alpha Vantage preflight.",
            retry_count=0,
        )

    calls = [
        ("TOOL_LIST", {}),
        ("TOOL_GET", {"tool_name": "PING"}),
        ("TOOL_CALL", {"tool_name": "PING", "arguments": {}}),
        ("TOOL_GET", {"tool_name": "NEWS_SENTIMENT"}),
        (
            "TOOL_CALL",
            {
                "tool_name": "NEWS_SENTIMENT",
                "arguments": {
                    "tickers": ",".join(symbols),
                    "sort": "LATEST",
                    "limit": min(50, max(5, len(symbols) * 5)),
                },
            },
        ),
    ]
    try:
        payloads = await call_stdio_tool_sequence(
            command=ROOT_DIR / "scripts" / "mcp-alpha-vantage.sh",
            env=env,
            calls=calls,
            protocol="jsonl",
        )
    except Exception as exc:
        return provider_row(
            server="alpha-vantage",
            queried=True,
            outcome="failed",
            checked_at=checked_at,
            gap_category=classify_error(exc),
            gap_reason=str(exc)[:240],
            retry_count=0,
        )

    candidate_payload = payloads[-1] if payloads else {}
    item_count = alpha_news_item_count(candidate_payload)
    return provider_row(
        server="alpha-vantage",
        queried=True,
        outcome="pass" if item_count else "gap",
        checked_at=checked_at,
        gap_category="not_applicable" if item_count else "empty_response",
        gap_reason="" if item_count else "NEWS_SENTIMENT returned no candidate news items for the shortlisted symbols.",
        retry_count=0,
        tool="TOOL_LIST|TOOL_GET|TOOL_CALL(NEWS_SENTIMENT)",
        payload={"item_count": item_count, "candidate_payload": candidate_payload},
    )


async def capture_firecrawl(env: dict[str, str], symbols: list[str], ciks: dict[str, str]) -> dict[str, Any]:
    checked_at = now_utc()
    if not env.get("FIRECRAWL_API_KEY"):
        return provider_row(
            server="firecrawl",
            queried=True,
            outcome="unavailable",
            checked_at=checked_at,
            gap_category="auth",
            gap_reason="FIRECRAWL_API_KEY is not present in the scheduler environment.",
            retry_count=0,
        )

    first_cik_symbol = next((symbol for symbol in symbols if ciks.get(symbol)), "")
    if not first_cik_symbol:
        return provider_row(
            server="firecrawl",
            queried=True,
            outcome="gap",
            checked_at=checked_at,
            gap_category="empty_response",
            gap_reason="No candidate with a SEC CIK was available for Firecrawl source-page capture.",
            retry_count=0,
        )

    cik = ciks[first_cik_symbol]
    url = f"https://www.sec.gov/edgar/browse/?CIK={cik}"
    try:
        payload = await call_stdio_tool(
            command=ROOT_DIR / "scripts" / "mcp-firecrawl.sh",
            env=env,
            tool_name="firecrawl_scrape",
            arguments={"url": url, "formats": ["markdown"], "onlyMainContent": True},
        )
    except Exception as exc:
        return provider_row(
            server="firecrawl",
            queried=True,
            outcome="failed",
            checked_at=checked_at,
            gap_category=classify_error(exc),
            gap_reason=str(exc)[:240],
            retry_count=0,
        )

    return provider_row(
        server="firecrawl",
        queried=True,
        outcome="pass",
        checked_at=checked_at,
        gap_category="not_applicable",
        gap_reason="",
        retry_count=0,
        tool="firecrawl_scrape",
        payload={"symbol": first_cik_symbol, "url": url, "result": payload},
    )


def build_mcp_coverage_hint(providers: list[dict[str, Any]], source_ref: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for provider in providers:
        outcome = str(provider.get("outcome", "")).lower()
        positive = outcome in POSITIVE_OUTCOMES
        rows.append(
            {
                "server": str(provider.get("server", "")),
                "required": True,
                "queried": bool(provider.get("queried")),
                "used_in_score": positive,
                "outcome": outcome or "failed",
                "checked_at": provider.get("checked_at"),
                "source_refs": [source_ref],
                "gap_reason": provider.get("gap_reason", ""),
                "gap_category": provider.get("gap_category", "unknown"),
                "retry_count": int(provider.get("retry_count", 0) or 0),
            }
        )
    return rows


async def main_async() -> int:
    global MCP_TIMEOUT_SECONDS

    parser = argparse.ArgumentParser(description="Capture scheduler-owned research MCP preflight data.")
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--symbols", default="", help="Comma-separated candidate symbols for research MCP preflight.")
    parser.add_argument("--alpaca-preflight-json", type=Path)
    parser.add_argument("--max-symbols", type=int, default=DEFAULT_MAX_SYMBOLS)
    parser.add_argument(
        "--timeout",
        type=int,
        default=int(os.environ.get("CODEX_AUTOPILOT_RESEARCH_MCP_TIMEOUT_SECONDS", DEFAULT_MCP_TIMEOUT_SECONDS)),
        help="Per MCP stdio call sequence timeout in seconds.",
    )
    parser.add_argument("--sec-cik-map", type=Path, default=ROOT_DIR / "harness" / "sec-ticker-cik-map.json")
    args = parser.parse_args()

    MCP_TIMEOUT_SECONDS = max(5, int(args.timeout))
    env = read_env()
    captured_at = now_utc()
    max_symbols = max(1, int(args.max_symbols))
    explicit_symbols = parse_symbols(args.symbols)
    preflight_symbols = extract_symbols_from_alpaca_preflight(args.alpaca_preflight_json, max_symbols=max_symbols)
    symbols = (explicit_symbols or preflight_symbols)[:max_symbols]
    ciks = load_cik_map(args.sec_cik_map)

    sec_edgar, alpha_vantage, fred, firecrawl, yahoo_finance = await asyncio.gather(
        capture_sec_edgar(env, symbols, ciks),
        capture_alpha_vantage(env, symbols),
        capture_fred(env),
        capture_firecrawl(env, symbols, ciks),
        capture_yahoo_finance(env, symbols),
    )
    providers = [sec_edgar, alpha_vantage, fred, firecrawl, yahoo_finance]
    try:
        source_ref = str(args.output_json.relative_to(ROOT_DIR))
    except ValueError:
        source_ref = str(args.output_json)
    for provider in providers:
        provider["source_refs"] = [source_ref]

    output = {
        "run_id": args.run_id,
        "created_at": captured_at,
        "paper": env.get("ALPACA_PAPER_TRADE") == "true",
        "source": "scheduler local MCP stdio preflight",
        "symbols": symbols,
        "symbol_source": "explicit" if explicit_symbols else "alpaca_core_preflight" if preflight_symbols else "none",
        "providers": providers,
        "mcp_coverage_hint": build_mcp_coverage_hint(providers, source_ref),
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(output, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({key: output[key] for key in ("run_id", "created_at", "paper", "symbols")}, ensure_ascii=False))
    for provider in output["providers"]:
        print(
            f"{provider['server']}: {provider['outcome']}"
            + (f" ({provider.get('gap_category')})" if provider.get("gap_category") else "")
        )
    return 0


def main() -> None:
    raise SystemExit(asyncio.run(main_async()))


if __name__ == "__main__":
    main()
