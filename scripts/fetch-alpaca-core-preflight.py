#!/usr/bin/env python3
"""Capture scheduler-owned Alpaca core MCP evidence for autopilot runs.

This helper talks to the local Alpaca MCP server over stdio. It is read-only:
it never submits, replaces, cancels, or closes orders, and it never calls
Alpaca REST directly.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


ROOT_DIR = Path(__file__).resolve().parents[1]
EXIT_MCP_UNAVAILABLE = 70
MCP_TIMEOUT_SECONDS = 35
SENSITIVE_KEY_PARTS = ("api", "authorization", "key", "password", "secret", "token")


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def read_env(root: Path = ROOT_DIR) -> dict[str, str]:
    env = os.environ.copy()
    env_file = root / ".env"
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            if not stripped or stripped.startswith("#") or "=" not in stripped:
                continue
            key, value = stripped.split("=", 1)
            env.setdefault(key.strip(), value.strip().strip('"').strip("'"))
    return env


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Capture Alpaca core MCP preflight evidence.")
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--metadata-yaml", type=Path, default=ROOT_DIR / "harness" / "symbol-metadata.yaml")
    parser.add_argument("--symbols", default="", help="Comma-separated extra symbols to preflight.")
    parser.add_argument("--batch-size", type=int, default=25)
    parser.add_argument("--timeout", type=int, default=MCP_TIMEOUT_SECONDS)
    parser.add_argument("--retries", type=int, default=2)
    return parser.parse_args()


def classify_error(exc: BaseException) -> str:
    text = str(exc).lower()
    if "cancelled" in text or "canceled" in text or "user cancelled" in text:
        return "cancelled"
    if "could not resolve host" in text or "nodename nor servname" in text or "name resolution" in text:
        return "dns"
    if "unauthorized" in text or "forbidden" in text or "api_key" in text or "secret" in text:
        return "auth"
    if "timed out" in text or "timeout" in text:
        return "timeout"
    if "iserror" in text or "api request failed" in text or "request error" in text:
        return "provider_error"
    return "unknown"


def redact_sensitive(value: Any) -> Any:
    if isinstance(value, dict):
        redacted: dict[str, Any] = {}
        for key, item in value.items():
            lowered = str(key).lower()
            if lowered == "account_number" or any(part in lowered for part in SENSITIVE_KEY_PARTS):
                redacted[str(key)] = "[redacted]"
            else:
                redacted[str(key)] = redact_sensitive(item)
        return redacted
    if isinstance(value, list):
        return [redact_sensitive(item) for item in value]
    return value


def parse_tool_payload(result: Any) -> dict[str, Any] | list[Any]:
    if bool(getattr(result, "isError", False)):
        for item in getattr(result, "content", []):
            text = getattr(item, "text", None)
            if text:
                raise RuntimeError(str(text)[:500])
        raise RuntimeError("MCP tool returned isError=true")

    text_errors: list[str] = []
    for item in getattr(result, "content", []):
        text = getattr(item, "text", None)
        if not text:
            continue
        try:
            payload = json.loads(text)
        except json.JSONDecodeError:
            text_errors.append(str(text)[:500])
            continue
        if isinstance(payload, (dict, list)):
            if isinstance(payload, dict) and payload.get("error"):
                raise RuntimeError(str(payload["error"])[:500])
            return payload
    if text_errors:
        raise RuntimeError(text_errors[0])
    dumped = result.model_dump() if hasattr(result, "model_dump") else {"result": str(result)}
    raise RuntimeError(f"Could not parse MCP tool response as JSON: {dumped}")


def summarize_arguments(arguments: dict[str, Any]) -> dict[str, Any]:
    summary: dict[str, Any] = {}
    if "symbols" in arguments:
        symbols = [item.strip() for item in str(arguments["symbols"]).split(",") if item.strip()]
        summary["symbols_count"] = len(symbols)
        summary["symbols_preview"] = symbols[:8]
    if "symbol_or_asset_id" in arguments:
        summary["symbol_or_asset_id"] = arguments["symbol_or_asset_id"]
    for key in ("status", "limit", "feed", "page_size", "activity_types"):
        if key in arguments:
            summary[key] = arguments[key]
    return summary


async def call_tool_with_retries(
    session: ClientSession,
    name: str,
    arguments: dict[str, Any] | None = None,
    *,
    retries: int,
    timeout: int,
) -> dict[str, Any]:
    args = arguments or {}
    last_error: BaseException | None = None
    checked_at = now_utc()
    for attempt in range(retries + 1):
        checked_at = now_utc()
        try:
            result = await asyncio.wait_for(session.call_tool(name, args), timeout=timeout)
            payload = parse_tool_payload(result)
            return {
                "tool": name,
                "arguments": summarize_arguments(args),
                "outcome": "pass",
                "checked_at": checked_at,
                "gap_category": "not_applicable",
                "gap_reason": "",
                "retry_count": attempt,
                "payload": redact_sensitive(payload),
            }
        except Exception as exc:  # noqa: BLE001 - preflight must classify and continue.
            last_error = exc
            if attempt < retries:
                await asyncio.sleep(1 + attempt)

    assert last_error is not None
    return {
        "tool": name,
        "arguments": summarize_arguments(args),
        "outcome": "failed",
        "checked_at": checked_at,
        "gap_category": classify_error(last_error),
        "gap_reason": str(last_error)[:500],
        "retry_count": retries,
    }


def load_metadata_symbols(path: Path) -> set[str]:
    if not path.exists():
        return set()
    try:
        import yaml

        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        symbols = (data or {}).get("symbols", {})
        if isinstance(symbols, dict):
            return {str(symbol).upper() for symbol in symbols if str(symbol).strip()}
    except Exception:
        pass

    symbols: set[str] = set()
    in_symbols = False
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("symbols:"):
            in_symbols = True
            continue
        if in_symbols and line and not line.startswith(" "):
            break
        match = re.match(r"^  ([A-Z][A-Z0-9.\-]+):\s*$", line)
        if in_symbols and match:
            symbols.add(match.group(1).upper())
    return symbols


def extract_symbols(value: Any) -> set[str]:
    symbols: set[str] = set()
    if isinstance(value, dict):
        for key, item in value.items():
            lowered = str(key).lower()
            if lowered == "symbol" and isinstance(item, str):
                symbols.add(item.upper())
            elif lowered == "symbols":
                if isinstance(item, str):
                    symbols.update(part.strip().upper() for part in item.split(",") if part.strip())
                elif isinstance(item, list):
                    symbols.update(str(part).upper() for part in item if str(part).strip())
            symbols.update(extract_symbols(item))
    elif isinstance(value, list):
        for item in value:
            symbols.update(extract_symbols(item))
    return symbols


def normalize_clock(row: dict[str, Any]) -> dict[str, Any]:
    payload = row.get("payload")
    if not isinstance(payload, dict):
        return {"is_open": False}
    clock = payload.get("clock") if isinstance(payload.get("clock"), dict) else payload
    is_open = clock.get("is_open")
    if is_open is None:
        is_open = clock.get("isOpen")
    return {
        "is_open": bool(is_open),
        "timestamp": clock.get("timestamp") or clock.get("time"),
        "next_open": clock.get("next_open") or clock.get("nextOpen"),
        "next_close": clock.get("next_close") or clock.get("nextClose"),
    }


def chunked(items: list[str], size: int) -> list[list[str]]:
    size = max(1, size)
    return [items[index : index + size] for index in range(0, len(items), size)]


async def capture_asset_checks(
    session: ClientSession,
    symbols: list[str],
    *,
    retries: int,
    timeout: int,
) -> dict[str, Any]:
    results: dict[str, Any] = {}
    failures: list[dict[str, Any]] = []
    for symbol in symbols:
        row = await call_tool_with_retries(
            session,
            "get_asset",
            {"symbol_or_asset_id": symbol},
            retries=retries,
            timeout=timeout,
        )
        if row["outcome"] == "pass":
            results[symbol] = row["payload"]
        else:
            failures.append({key: row[key] for key in ("tool", "arguments", "gap_category", "gap_reason", "retry_count")})
    return {
        "tool": "get_asset",
        "outcome": "pass" if len(results) == len(symbols) and not failures else "failed",
        "checked_at": now_utc(),
        "symbols_requested": len(symbols),
        "symbols_passed": len(results),
        "symbols_failed": len(failures),
        "failures": failures[:20],
        "payload_by_symbol": results,
    }


async def capture_symbol_batch_tool(
    session: ClientSession,
    tool_name: str,
    symbols: list[str],
    *,
    batch_size: int,
    retries: int,
    timeout: int,
) -> dict[str, Any]:
    batches: list[dict[str, Any]] = []
    failures: list[dict[str, Any]] = []
    symbols_passed = 0
    for batch in chunked(symbols, batch_size):
        row = await call_tool_with_retries(
            session,
            tool_name,
            {"symbols": ",".join(batch), "feed": "iex"},
            retries=retries,
            timeout=timeout,
        )
        if row["outcome"] == "pass":
            symbols_passed += len(batch)
            batches.append(
                {
                    "symbols": batch,
                    "checked_at": row["checked_at"],
                    "payload": row["payload"],
                }
            )
        else:
            failures.append({key: row[key] for key in ("tool", "arguments", "gap_category", "gap_reason", "retry_count")})
    return {
        "tool": tool_name,
        "outcome": "pass" if symbols_passed == len(symbols) and not failures else "failed",
        "checked_at": now_utc(),
        "feed": "iex",
        "symbols_requested": len(symbols),
        "symbols_passed": symbols_passed,
        "symbols_failed": len(symbols) - symbols_passed,
        "batches": batches,
        "failures": failures,
    }


def coverage_hint(
    *,
    source_ref: str,
    created_at: str,
    hard_gate: dict[str, Any],
) -> dict[str, Any]:
    status = hard_gate["status"]
    return {
        "server": "alpaca",
        "required": True,
        "queried": True,
        "used_in_score": status == "pass",
        "outcome": "pass" if status == "pass" else "failed",
        "checked_at": created_at,
        "source_refs": [source_ref],
        "gap_reason": "" if status == "pass" else hard_gate.get("gap_reason", "Alpaca core preflight failed."),
        "gap_category": "not_applicable" if status == "pass" else hard_gate.get("gap_category", "unknown"),
        "retry_count": int(hard_gate.get("max_retry_count", 0) or 0),
        "first_blocking_gate": hard_gate.get("first_blocking_gate", ""),
    }


def build_hard_gate(tool_results: dict[str, Any], *, retries: int) -> dict[str, Any]:
    checks = {
        "clock": tool_results.get("get_clock", {}).get("outcome") == "pass",
        "market_open": normalize_clock(tool_results.get("get_clock", {})).get("is_open") is True,
        "account": tool_results.get("get_account_info", {}).get("outcome") == "pass",
        "positions": tool_results.get("get_all_positions", {}).get("outcome") == "pass",
        "open_orders": tool_results.get("get_orders_open", {}).get("outcome") == "pass",
        "recent_activities": tool_results.get("get_account_activities", {}).get("outcome") == "pass",
        "quotes": tool_results.get("get_stock_latest_quote", {}).get("outcome") == "pass",
    }
    order = [
        ("alpaca_clock", "clock"),
        ("market_closed", "market_open"),
        ("alpaca_account", "account"),
        ("alpaca_positions", "positions"),
        ("alpaca_open_orders", "open_orders"),
        ("alpaca_recent_activities", "recent_activities"),
        ("alpaca_quotes", "quotes"),
    ]
    first_blocking_gate = ""
    for gate, key in order:
        if not checks[key]:
            first_blocking_gate = gate
            break
    status = "pass" if not first_blocking_gate else "failed"
    gap_category = "not_applicable"
    gap_reason = ""
    if first_blocking_gate:
        result_key = {
            "alpaca_clock": "get_clock",
            "market_closed": "get_clock",
            "alpaca_account": "get_account_info",
            "alpaca_positions": "get_all_positions",
            "alpaca_open_orders": "get_orders_open",
            "alpaca_recent_activities": "get_account_activities",
            "alpaca_quotes": "get_stock_latest_quote",
        }[first_blocking_gate]
        row = tool_results.get(result_key, {})
        gap_category = row.get("gap_category", "provider_error" if first_blocking_gate == "market_closed" else "unknown")
        gap_reason = row.get("gap_reason") or f"{first_blocking_gate} did not pass."
    return {
        "status": status,
        "checks": checks,
        "first_blocking_gate": first_blocking_gate,
        "gap_category": gap_category,
        "gap_reason": gap_reason,
        "max_retry_count": retries,
    }


async def main_async(args: argparse.Namespace) -> int:
    env = read_env()
    if env.get("ALPACA_PAPER_TRADE") != "true":
        print("ALPACA_PAPER_TRADE=true is required.", file=sys.stderr)
        return 64

    symbols = load_metadata_symbols(args.metadata_yaml)
    symbols.update({"SPY", "QQQ"})
    symbols.update(symbol.strip().upper() for symbol in args.symbols.split(",") if symbol.strip())

    server = StdioServerParameters(
        command=str(ROOT_DIR / "scripts" / "alpaca-mcp.sh"),
        args=[],
        env=env,
        cwd=str(ROOT_DIR),
    )

    tool_results: dict[str, Any] = {}
    try:
        with open(os.devnull, "w", encoding="utf-8") as errlog:
            async with stdio_client(server, errlog=errlog) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    tool_results["get_clock"] = await call_tool_with_retries(
                        session, "get_clock", retries=args.retries, timeout=args.timeout
                    )
                    tool_results["get_account_info"] = await call_tool_with_retries(
                        session, "get_account_info", retries=args.retries, timeout=args.timeout
                    )
                    tool_results["get_all_positions"] = await call_tool_with_retries(
                        session, "get_all_positions", retries=args.retries, timeout=args.timeout
                    )
                    tool_results["get_orders_open"] = await call_tool_with_retries(
                        session,
                        "get_orders",
                        {"status": "open", "limit": 100, "direction": "desc"},
                        retries=args.retries,
                        timeout=args.timeout,
                    )
                    tool_results["get_account_activities"] = await call_tool_with_retries(
                        session,
                        "get_account_activities",
                        {"activity_types": ["FILL"], "page_size": 20, "direction": "desc"},
                        retries=args.retries,
                        timeout=args.timeout,
                    )
                    tool_results["get_watchlists"] = await call_tool_with_retries(
                        session, "get_watchlists", retries=args.retries, timeout=args.timeout
                    )

                    symbols.update(extract_symbols(tool_results["get_all_positions"].get("payload")))
                    symbols.update(extract_symbols(tool_results["get_watchlists"].get("payload")))
                    ordered_symbols = sorted(symbol for symbol in symbols if symbol)

                    tool_results["get_asset"] = await capture_asset_checks(
                        session, ordered_symbols, retries=args.retries, timeout=args.timeout
                    )
                    tool_results["get_stock_latest_quote"] = await capture_symbol_batch_tool(
                        session,
                        "get_stock_latest_quote",
                        ordered_symbols,
                        batch_size=args.batch_size,
                        retries=args.retries,
                        timeout=args.timeout,
                    )
                    tool_results["get_stock_snapshot"] = await capture_symbol_batch_tool(
                        session,
                        "get_stock_snapshot",
                        ordered_symbols,
                        batch_size=args.batch_size,
                        retries=args.retries,
                        timeout=args.timeout,
                    )
                    tool_results["get_stock_latest_trade"] = await capture_symbol_batch_tool(
                        session,
                        "get_stock_latest_trade",
                        ordered_symbols,
                        batch_size=args.batch_size,
                        retries=args.retries,
                        timeout=args.timeout,
                    )
    except Exception as exc:  # noqa: BLE001 - scheduler guard should classify failure.
        created_at = now_utc()
        hard_gate = {
            "status": "failed",
            "checks": {},
            "first_blocking_gate": "alpaca_mcp_startup",
            "gap_category": classify_error(exc),
            "gap_reason": str(exc)[:500],
            "max_retry_count": 0,
        }
        source_ref = str(args.output_json.relative_to(ROOT_DIR)) if args.output_json.is_relative_to(ROOT_DIR) else str(args.output_json)
        output = {
            "run_id": args.run_id,
            "created_at": created_at,
            "paper": True,
            "source": "scheduler local Alpaca MCP stdio core preflight",
            "read_only": True,
            "orders_submitted": 0,
            "hard_gate_summary": hard_gate,
            "mcp_coverage_hint": coverage_hint(source_ref=source_ref, created_at=created_at, hard_gate=hard_gate),
            "tool_results": tool_results,
        }
        args.output_json.parent.mkdir(parents=True, exist_ok=True)
        args.output_json.write_text(json.dumps(output, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(json.dumps({"run_id": args.run_id, "status": "failed", "first_blocking_gate": "alpaca_mcp_startup"}, ensure_ascii=False))
        return EXIT_MCP_UNAVAILABLE

    created_at = now_utc()
    source_ref = str(args.output_json.relative_to(ROOT_DIR)) if args.output_json.is_relative_to(ROOT_DIR) else str(args.output_json)
    hard_gate = build_hard_gate(tool_results, retries=args.retries)
    output = {
        "run_id": args.run_id,
        "created_at": created_at,
        "paper": True,
        "source": "scheduler local Alpaca MCP stdio core preflight",
        "read_only": True,
        "orders_submitted": 0,
        "universe_symbols": sorted(symbols),
        "hard_gate_summary": hard_gate,
        "clock": normalize_clock(tool_results.get("get_clock", {})),
        "mcp_coverage_hint": coverage_hint(source_ref=source_ref, created_at=created_at, hard_gate=hard_gate),
        "tool_results": tool_results,
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(output, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(
        json.dumps(
            {
                "run_id": args.run_id,
                "status": hard_gate["status"],
                "market_open": output["clock"].get("is_open"),
                "symbols": len(symbols),
                "first_blocking_gate": hard_gate.get("first_blocking_gate", ""),
            },
            ensure_ascii=False,
        )
    )
    return 0 if hard_gate["status"] == "pass" else EXIT_MCP_UNAVAILABLE


def main() -> None:
    raise SystemExit(asyncio.run(main_async(parse_args())))


if __name__ == "__main__":
    main()
