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
import copy
import hashlib
import json
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


ROOT_DIR = Path(__file__).resolve().parents[1]
DEFAULT_FRED_SERIES = ["DGS10", "DGS2", "FEDFUNDS", "CPIAUCSL", "UNRATE", "NFCI"]
DEFAULT_MAX_SYMBOLS = 12
DEFAULT_MCP_TIMEOUT_SECONDS = 75
DEFAULT_CACHE_DIR = ROOT_DIR / ".cache" / "research-mcp-preflight"
DEFAULT_CIRCUIT_BREAKER_SECONDS = 600
ALPHA_VANTAGE_MIN_CALL_INTERVAL_SECONDS = 3600
PROVIDER_CACHE_TTL_SECONDS = {
    "sec-edgar": 3600,
    "alpha-vantage": ALPHA_VANTAGE_MIN_CALL_INTERVAL_SECONDS,
    "fred": 21600,
    "firecrawl": 3600,
    "yahoo-finance": 1800,
}
MCP_TIMEOUT_SECONDS = DEFAULT_MCP_TIMEOUT_SECONDS
STDERR_CAPTURE_LIMIT = 4000
STDIO_READ_LIMIT = 8 * 1024 * 1024
POSITIVE_OUTCOMES = {"pass", "usable", "ok"}
SYSTEMIC_GAP_CATEGORIES = {"timeout", "cancelled", "dns", "auth", "wrapper_error"}


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def parse_utc(value: Any) -> datetime | None:
    if not value:
        return None
    try:
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


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


def normalize_gap_category(value: Any, outcome: str) -> str:
    category = str(value or "").strip().lower()
    if category:
        return category
    if str(outcome).lower() in {"gap", "failed", "unavailable", "not_applicable"}:
        return "unknown"
    return ""


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


async def call_sequence_with_retries(
    *,
    command: Path,
    env: dict[str, str],
    calls: list[tuple[str, dict[str, Any]]],
    retries: int,
    protocol: str = "headers",
) -> dict[str, Any]:
    last_error: BaseException | None = None
    for attempt in range(retries + 1):
        try:
            payloads = await call_stdio_tool_sequence(command=command, env=env, calls=calls, protocol=protocol)
            return {"outcome": "pass", "payloads": payloads, "retry_count": attempt}
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
        "gap_category": normalize_gap_category(gap_category, outcome),
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


def alpha_provider_issue(payload: dict[str, Any]) -> str:
    for key in ("Information", "Note", "Error Message"):
        value = payload.get(key)
        if not isinstance(value, str):
            continue
        text = value.lower()
        if "rate limit" in text:
            return "rate_limit"
        if "invalid api call" in text or "error" in text:
            return "provider_error"
    return ""


def safe_alpha_payload(candidate_payload: dict[str, Any], item_count: int) -> dict[str, Any]:
    issue = alpha_provider_issue(candidate_payload)
    if issue:
        return {"item_count": item_count, "provider_issue": issue}
    return {"item_count": item_count, "candidate_payload": candidate_payload}


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


def provider_cache_key(server: str, symbols: list[str], *, cache_scope: str = "") -> str:
    payload = {"version": 2, "server": server, "symbols": sorted(symbols)}
    if cache_scope:
        payload["cache_scope"] = cache_scope
    body = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(body.encode("utf-8")).hexdigest()


def provider_cache_path(cache_dir: Path, server: str, cache_key: str) -> Path:
    return cache_dir / "providers" / server / f"{cache_key}.json"


def provider_cache_ttl(server: str, override_seconds: int | None) -> int:
    if override_seconds is not None:
        return max(0, override_seconds)
    return PROVIDER_CACHE_TTL_SECONDS.get(server, 0)


def alpha_min_call_interval_seconds() -> int:
    try:
        value = int(
            os.environ.get(
                "CODEX_AUTOPILOT_ALPHA_MIN_CALL_INTERVAL_SECONDS",
                str(ALPHA_VANTAGE_MIN_CALL_INTERVAL_SECONDS),
            )
        )
    except (TypeError, ValueError):
        value = ALPHA_VANTAGE_MIN_CALL_INTERVAL_SECONDS
    return max(0, value)


def alpha_vantage_cache_scope(env: dict[str, str]) -> str:
    api_key = str(env.get("ALPHA_VANTAGE_API_KEY") or "").strip()
    if not api_key:
        return "key-missing"
    return "key-" + hashlib.sha256(api_key.encode("utf-8")).hexdigest()[:12]


def load_cached_provider(cache_dir: Path, server: str, cache_key: str, *, ttl_seconds: int) -> dict[str, Any] | None:
    if ttl_seconds <= 0:
        return None
    path = provider_cache_path(cache_dir, server, cache_key)
    if not path.exists():
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    row = payload.get("provider")
    stored_at = parse_utc(payload.get("stored_at"))
    if not isinstance(row, dict) or stored_at is None:
        return None
    if datetime.now(timezone.utc) - stored_at > timedelta(seconds=ttl_seconds):
        return None
    cached = copy.deepcopy(row)
    cached["cache_hit"] = True
    cached["cache_stored_at"] = stored_at.isoformat(timespec="seconds")
    cached["cache_reused_at"] = now_utc()
    cached["cache_ttl_seconds"] = ttl_seconds
    return cached


def provider_row_cacheable(server: str, row: dict[str, Any]) -> bool:
    if str(row.get("outcome", "")).lower() in POSITIVE_OUTCOMES:
        return True
    return server == "alpha-vantage"


def save_cached_provider(cache_dir: Path, server: str, cache_key: str, row: dict[str, Any], *, ttl_seconds: int) -> None:
    if ttl_seconds <= 0 or not provider_row_cacheable(server, row):
        return
    path = provider_cache_path(cache_dir, server, cache_key)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "stored_at": now_utc(),
        "ttl_seconds": ttl_seconds,
        "provider": row,
    }
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def provider_attempt_path(cache_dir: Path, server: str, *, cache_scope: str = "") -> Path:
    if cache_scope:
        return cache_dir / "providers" / server / f"last-attempt-{cache_scope}.json"
    return cache_dir / "providers" / server / "last-attempt.json"


def save_provider_attempt(cache_dir: Path, server: str, symbols: list[str], *, cache_scope: str = "") -> None:
    path = provider_attempt_path(cache_dir, server, cache_scope=cache_scope)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {"stored_at": now_utc(), "symbols": symbols}
    if cache_scope:
        payload["cache_scope"] = cache_scope
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def recent_alpha_attempt_row(
    cache_dir: Path,
    symbols: list[str],
    *,
    min_interval_seconds: int,
    cache_scope: str = "",
) -> dict[str, Any] | None:
    if min_interval_seconds <= 0:
        return None
    path = provider_attempt_path(cache_dir, "alpha-vantage", cache_scope=cache_scope)
    if not path.exists():
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    stored_at = parse_utc(payload.get("stored_at"))
    if stored_at is None:
        return None
    elapsed = (datetime.now(timezone.utc) - stored_at).total_seconds()
    if elapsed >= min_interval_seconds:
        return None
    previous_symbols = [str(symbol).upper() for symbol in payload.get("symbols", []) if str(symbol).strip()]
    remaining = max(1, int(min_interval_seconds - elapsed))
    return provider_row(
        server="alpha-vantage",
        queried=True,
        outcome="failed",
        checked_at=now_utc(),
        gap_category="provider_error",
        gap_reason=(
            "Skipped Alpha Vantage API call to enforce one-call-per-hour throttle; "
            f"previous attempt at {stored_at.isoformat(timespec='seconds')}, retry after ~{remaining}s."
        )[:240],
        retry_count=0,
        payload={
            "throttled": True,
            "last_attempt_at": stored_at.isoformat(timespec="seconds"),
            "min_interval_seconds": min_interval_seconds,
            "requested_symbols": symbols,
            "previous_symbols": previous_symbols,
            "cache_scope": cache_scope,
        },
    )


def circuit_state_path(cache_dir: Path) -> Path:
    return cache_dir / "circuit-breaker.json"


def load_circuit_state(cache_dir: Path) -> dict[str, Any]:
    path = circuit_state_path(cache_dir)
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return payload if isinstance(payload, dict) else {}


def save_circuit_state(cache_dir: Path, state: dict[str, Any]) -> None:
    path = circuit_state_path(cache_dir)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def circuit_state_key(server: str, cache_scope: str = "") -> str:
    if server == "alpha-vantage" and cache_scope:
        return f"{server}:{cache_scope}"
    return server


def circuit_open_row(server: str, state: dict[str, Any], *, cache_scope: str = "") -> dict[str, Any] | None:
    row = state.get(circuit_state_key(server, cache_scope))
    if not isinstance(row, dict):
        return None
    opened_until = parse_utc(row.get("opened_until"))
    if opened_until is None or opened_until <= datetime.now(timezone.utc):
        return None
    gap_category = str(row.get("gap_category") or "unknown")
    gap_reason = str(row.get("gap_reason") or "provider circuit breaker is open")
    return provider_row(
        server=server,
        queried=True,
        outcome="failed",
        checked_at=now_utc(),
        gap_category=gap_category,
        gap_reason=(
            f"Circuit breaker open until {opened_until.isoformat(timespec='seconds')} after recent "
            f"{gap_category} failure: {gap_reason}"
        )[:240],
        retry_count=0,
        payload={"circuit_breaker_open": True, "opened_until": opened_until.isoformat(timespec="seconds")},
    )


def update_circuit_state(
    cache_dir: Path,
    state: dict[str, Any],
    server: str,
    row: dict[str, Any],
    *,
    circuit_seconds: int,
    cache_scope: str = "",
) -> None:
    state_key = circuit_state_key(server, cache_scope)
    outcome = str(row.get("outcome", "")).lower()
    if outcome in POSITIVE_OUTCOMES:
        stale_keys = [state_key]
        if server == "alpha-vantage":
            stale_keys.append(server)
        changed = False
        for key in stale_keys:
            if key in state:
                state.pop(key, None)
                changed = True
        if changed:
            save_circuit_state(cache_dir, state)
        return
    gap_category = str(row.get("gap_category") or "")
    if circuit_seconds <= 0 or gap_category not in SYSTEMIC_GAP_CATEGORIES:
        payload = row.get("payload")
        provider_issue = payload.get("provider_issue") if isinstance(payload, dict) else ""
        if not (server == "alpha-vantage" and gap_category == "provider_error" and provider_issue == "rate_limit"):
            return
        circuit_seconds = max(
            circuit_seconds,
            int(
                os.environ.get(
                    "CODEX_AUTOPILOT_ALPHA_RATE_LIMIT_CIRCUIT_SECONDS",
                    str(ALPHA_VANTAGE_MIN_CALL_INTERVAL_SECONDS),
                )
            ),
        )
    opened_until = datetime.now(timezone.utc) + timedelta(seconds=circuit_seconds)
    state[state_key] = {
        "opened_at": now_utc(),
        "opened_until": opened_until.isoformat(timespec="seconds"),
        "gap_category": gap_category,
        "gap_reason": str(row.get("gap_reason") or "")[:240],
        "cache_scope": cache_scope,
    }
    save_circuit_state(cache_dir, state)


async def cached_or_capture_provider(
    *,
    server: str,
    symbols: list[str],
    cache_dir: Path,
    cache_ttl_override: int | None,
    no_cache: bool,
    circuit_state: dict[str, Any],
    circuit_seconds: int,
    capture,
    cache_scope: str = "",
) -> dict[str, Any]:
    cache_key = provider_cache_key(server, symbols, cache_scope=cache_scope)
    ttl_seconds = provider_cache_ttl(server, cache_ttl_override)
    if not no_cache:
        cached = load_cached_provider(cache_dir, server, cache_key, ttl_seconds=ttl_seconds)
        if cached is not None:
            return cached
    open_row = circuit_open_row(server, circuit_state, cache_scope=cache_scope)
    if open_row is not None:
        return open_row
    if server == "alpha-vantage":
        throttled = recent_alpha_attempt_row(
            cache_dir,
            symbols,
            min_interval_seconds=alpha_min_call_interval_seconds(),
            cache_scope=cache_scope,
        )
        if throttled is not None:
            return throttled
    row = await capture()
    if not no_cache:
        save_cached_provider(cache_dir, server, cache_key, row, ttl_seconds=ttl_seconds)
    if server == "alpha-vantage":
        save_provider_attempt(cache_dir, server, symbols, cache_scope=cache_scope)
    update_circuit_state(cache_dir, circuit_state, server, row, circuit_seconds=circuit_seconds, cache_scope=cache_scope)
    return row


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
    active: list[tuple[str, str]] = []
    for symbol in symbols:
        cik = ciks.get(symbol)
        if not cik:
            per_symbol[symbol] = {
                "outcome": "gap",
                "gap_category": "empty_response",
                "gap_reason": "symbol missing from local SEC ticker-CIK cache; likely ETF/non-company lookup gap",
            }
            continue
        active.append((symbol, cik))

    if not active:
        return provider_row(
            server="sec-edgar",
            queried=True,
            outcome="gap",
            checked_at=checked_at,
            gap_category="empty_response",
            gap_reason="No candidate symbol had a local SEC CIK mapping for lightweight filing checks.",
            retry_count=0,
            tool="get_company_info|get_recent_filings",
            per_symbol=per_symbol,
        )

    calls: list[tuple[str, dict[str, Any]]] = []
    for _, cik in active:
        calls.append(("get_company_info", {"identifier": cik}))
        calls.append(("get_recent_filings", {"identifier": cik, "days": 30, "limit": 5}))

    result = await call_sequence_with_retries(
        command=command,
        env=env,
        calls=calls,
        retries=1,
        protocol="jsonl",
    )
    if result["outcome"] != "pass":
        gap_category, gap_reason = gap_from_failed_call(result)
        failed_row = {
            "outcome": "failed",
            "gap_category": gap_category,
            "gap_reason": gap_reason,
            "retry_count": int(result.get("retry_count", 0)),
        }
        for symbol, cik in active:
            per_symbol[symbol] = {
                "cik": cik,
                "outcome": "failed",
                "company_info": failed_row,
                "recent_filings": skipped_after(failed_row, "get_recent_filings"),
            }
        return provider_row(
            server="sec-edgar",
            queried=True,
            outcome="failed",
            checked_at=checked_at,
            gap_category=gap_category,
            gap_reason=gap_reason,
            retry_count=int(result.get("retry_count", 0)),
            tool="get_company_info|get_recent_filings",
            per_symbol=per_symbol,
        )

    payloads = result.get("payloads") or []
    for index, (symbol, cik) in enumerate(active):
        company_payload = payloads[index * 2] if index * 2 < len(payloads) else {}
        filings_payload = payloads[index * 2 + 1] if index * 2 + 1 < len(payloads) else {}
        per_symbol[symbol] = {
            "cik": cik,
            "outcome": "pass",
            "company_info": {
                "outcome": "pass",
                "payload": company_payload,
                "retry_count": int(result.get("retry_count", 0)),
            },
            "recent_filings": {
                "outcome": "pass",
                "payload": filings_payload,
                "retry_count": int(result.get("retry_count", 0)),
            },
        }

    return provider_row(
        server="sec-edgar",
        queried=True,
        outcome="pass",
        checked_at=checked_at,
        gap_category="not_applicable",
        gap_reason="",
        retry_count=int(result.get("retry_count", 0)),
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
    calls: list[tuple[str, dict[str, Any]]] = []
    for symbol in symbols:
        calls.append(
            (
                "get_recommendations",
                {"ticker": symbol, "recommendation_type": "recommendations", "months_back": 12},
            )
        )
        calls.append(("get_yahoo_finance_news", {"ticker": symbol}))

    result = await call_sequence_with_retries(
        command=command,
        env=env,
        calls=calls,
        retries=1,
        protocol="jsonl",
    )
    if result["outcome"] != "pass":
        gap_category, gap_reason = gap_from_failed_call(result)
        failed_row = {
            "outcome": "failed",
            "gap_category": gap_category,
            "gap_reason": gap_reason,
            "retry_count": int(result.get("retry_count", 0)),
        }
        for symbol in symbols:
            per_symbol[symbol] = {
                "outcome": "failed",
                "recommendations": failed_row,
                "news": skipped_after(failed_row, "get_yahoo_finance_news"),
            }
        return provider_row(
            server="yahoo-finance",
            queried=True,
            outcome="failed",
            checked_at=checked_at,
            gap_category=gap_category,
            gap_reason=gap_reason,
            retry_count=int(result.get("retry_count", 0)),
            tool="get_recommendations|get_yahoo_finance_news",
            per_symbol=per_symbol,
        )

    payloads = result.get("payloads") or []
    pass_count = 0
    for index, symbol in enumerate(symbols):
        recommendations_payload = payloads[index * 2] if index * 2 < len(payloads) else {}
        news_payload = payloads[index * 2 + 1] if index * 2 + 1 < len(payloads) else {}
        pass_count += 1
        per_symbol[symbol] = {
            "outcome": "pass",
            "recommendations": {
                "outcome": "pass",
                "payload": recommendations_payload,
                "retry_count": int(result.get("retry_count", 0)),
            },
            "news": {
                "outcome": "pass",
                "payload": news_payload,
                "retry_count": int(result.get("retry_count", 0)),
            },
        }

    return provider_row(
        server="yahoo-finance",
        queried=True,
        outcome="pass" if pass_count else "gap",
        checked_at=checked_at,
        gap_category="not_applicable" if pass_count else "empty_response",
        gap_reason="" if pass_count else "No Yahoo Finance candidate call returned usable data.",
        retry_count=int(result.get("retry_count", 0)),
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
    if not isinstance(candidate_payload, dict):
        candidate_payload = {}
    item_count = alpha_news_item_count(candidate_payload)
    provider_issue = alpha_provider_issue(candidate_payload)
    if provider_issue == "rate_limit":
        return provider_row(
            server="alpha-vantage",
            queried=True,
            outcome="failed",
            checked_at=checked_at,
            gap_category="provider_error",
            gap_reason="Alpha Vantage daily API rate limit reached; NEWS_SENTIMENT data unavailable.",
            retry_count=0,
            tool="TOOL_LIST|TOOL_GET|TOOL_CALL(NEWS_SENTIMENT)",
            payload=safe_alpha_payload(candidate_payload, item_count),
        )
    if provider_issue:
        return provider_row(
            server="alpha-vantage",
            queried=True,
            outcome="failed",
            checked_at=checked_at,
            gap_category="provider_error",
            gap_reason="Alpha Vantage provider returned an error message for NEWS_SENTIMENT.",
            retry_count=0,
            tool="TOOL_LIST|TOOL_GET|TOOL_CALL(NEWS_SENTIMENT)",
            payload=safe_alpha_payload(candidate_payload, item_count),
        )
    return provider_row(
        server="alpha-vantage",
        queried=True,
        outcome="pass" if item_count else "gap",
        checked_at=checked_at,
        gap_category="not_applicable" if item_count else "empty_response",
        gap_reason="" if item_count else "NEWS_SENTIMENT returned no candidate news items for the shortlisted symbols.",
        retry_count=0,
        tool="TOOL_LIST|TOOL_GET|TOOL_CALL(NEWS_SENTIMENT)",
        payload=safe_alpha_payload(candidate_payload, item_count),
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
                "gap_category": normalize_gap_category(provider.get("gap_category"), outcome or "failed"),
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
    parser.add_argument(
        "--cache-dir",
        type=Path,
        default=Path(os.environ.get("CODEX_AUTOPILOT_RESEARCH_CACHE_DIR", str(DEFAULT_CACHE_DIR))),
        help="Directory for short-lived provider preflight cache and circuit-breaker state.",
    )
    parser.add_argument(
        "--cache-ttl-seconds",
        type=int,
        help="Override per-provider positive-result cache TTL. Use 0 to disable positive-result cache writes.",
    )
    parser.add_argument("--no-cache", action="store_true", help="Disable provider preflight cache reads/writes.")
    parser.add_argument(
        "--circuit-breaker-seconds",
        type=int,
        default=int(
            os.environ.get("CODEX_AUTOPILOT_RESEARCH_CIRCUIT_SECONDS", DEFAULT_CIRCUIT_BREAKER_SECONDS)
        ),
        help="Seconds to skip a provider after systemic timeout/cancelled/dns/auth/wrapper failures.",
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
    cache_dir = args.cache_dir
    circuit_state = load_circuit_state(cache_dir)

    sec_edgar, alpha_vantage, fred, firecrawl, yahoo_finance = await asyncio.gather(
        cached_or_capture_provider(
            server="sec-edgar",
            symbols=symbols,
            cache_dir=cache_dir,
            cache_ttl_override=args.cache_ttl_seconds,
            no_cache=args.no_cache,
            circuit_state=circuit_state,
            circuit_seconds=max(0, int(args.circuit_breaker_seconds)),
            capture=lambda: capture_sec_edgar(env, symbols, ciks),
        ),
        cached_or_capture_provider(
            server="alpha-vantage",
            symbols=symbols,
            cache_dir=cache_dir,
            cache_ttl_override=args.cache_ttl_seconds,
            no_cache=args.no_cache,
            circuit_state=circuit_state,
            circuit_seconds=max(0, int(args.circuit_breaker_seconds)),
            capture=lambda: capture_alpha_vantage(env, symbols),
            cache_scope=alpha_vantage_cache_scope(env),
        ),
        cached_or_capture_provider(
            server="fred",
            symbols=[],
            cache_dir=cache_dir,
            cache_ttl_override=args.cache_ttl_seconds,
            no_cache=args.no_cache,
            circuit_state=circuit_state,
            circuit_seconds=max(0, int(args.circuit_breaker_seconds)),
            capture=lambda: capture_fred(env),
        ),
        cached_or_capture_provider(
            server="firecrawl",
            symbols=symbols,
            cache_dir=cache_dir,
            cache_ttl_override=args.cache_ttl_seconds,
            no_cache=args.no_cache,
            circuit_state=circuit_state,
            circuit_seconds=max(0, int(args.circuit_breaker_seconds)),
            capture=lambda: capture_firecrawl(env, symbols, ciks),
        ),
        cached_or_capture_provider(
            server="yahoo-finance",
            symbols=symbols,
            cache_dir=cache_dir,
            cache_ttl_override=args.cache_ttl_seconds,
            no_cache=args.no_cache,
            circuit_state=circuit_state,
            circuit_seconds=max(0, int(args.circuit_breaker_seconds)),
            capture=lambda: capture_yahoo_finance(env, symbols),
        ),
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
        "cache_dir": str(cache_dir),
        "cache_enabled": not args.no_cache,
        "circuit_breaker_seconds": max(0, int(args.circuit_breaker_seconds)),
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
