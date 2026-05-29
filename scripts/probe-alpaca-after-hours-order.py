#!/usr/bin/env python3
"""Probe Alpaca paper extended-hours order submission through MCP.

This runtime probe is intentionally separate from the scheduled autopilot. It
places one tiny, far-from-market paper buy limit order with extended_hours=true,
reconciles it by client_order_id, and cancels it immediately unless --no-cancel
is supplied. It never uses Alpaca REST directly.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
from datetime import datetime, timezone
from decimal import Decimal, ROUND_DOWN
from pathlib import Path
from typing import Any

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


ROOT_DIR = Path(__file__).resolve().parents[1]
EXIT_PROBE_FAILED = 70
DEFAULT_SYMBOL = "SPY"
DEFAULT_FEED = "iex"
DEFAULT_QTY = "1"
MCP_TIMEOUT_SECONDS = 35


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
    parser = argparse.ArgumentParser(description="Probe Alpaca paper extended-hours order submission.")
    parser.add_argument("--symbol", default=DEFAULT_SYMBOL)
    parser.add_argument("--qty", default=DEFAULT_QTY)
    parser.add_argument("--feed", default=DEFAULT_FEED)
    parser.add_argument("--run-id", default="")
    parser.add_argument("--output-json", type=Path)
    parser.add_argument("--timeout", type=int, default=MCP_TIMEOUT_SECONDS)
    parser.add_argument(
        "--limit-discount",
        type=Decimal,
        default=Decimal("0.70"),
        help="Buy limit as a fraction of the reference bid/mid price.",
    )
    parser.add_argument("--limit-price", type=Decimal, help="Explicit buy limit price.")
    parser.add_argument("--execute", action="store_true", help="Actually submit the paper probe order.")
    parser.add_argument("--no-cancel", action="store_true", help="Leave the probe order open after submit.")
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


def parse_tool_payload(result: Any, *, allow_text: bool = False) -> dict[str, Any] | list[Any]:
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
        if allow_text:
            return {"text": text_errors[0]}
        raise RuntimeError(text_errors[0])
    if allow_text:
        return {}
    raise RuntimeError("Could not parse MCP tool response as JSON")


async def call_tool(
    session: ClientSession,
    name: str,
    arguments: dict[str, Any] | None = None,
    *,
    timeout: int,
    allow_text: bool = False,
) -> dict[str, Any]:
    checked_at = now_utc()
    try:
        result = await asyncio.wait_for(session.call_tool(name, arguments or {}), timeout=timeout)
        payload = parse_tool_payload(result, allow_text=allow_text)
    except Exception as exc:  # noqa: BLE001 - probe should classify and report.
        return {
            "tool": name,
            "outcome": "failed",
            "checked_at": checked_at,
            "gap_category": classify_error(exc),
            "gap_reason": str(exc)[:500],
        }
    return {
        "tool": name,
        "outcome": "pass",
        "checked_at": checked_at,
        "gap_category": "not_applicable",
        "gap_reason": "",
        "payload": payload,
    }


def normalize_clock(payload: Any) -> dict[str, Any]:
    data = payload if isinstance(payload, dict) else {}
    clock = data.get("clock") if isinstance(data.get("clock"), dict) else data
    is_open = clock.get("is_open")
    if is_open is None:
        is_open = clock.get("isOpen")
    return {
        "is_open": bool(is_open),
        "timestamp": clock.get("timestamp") or clock.get("time"),
        "next_open": clock.get("next_open") or clock.get("nextOpen"),
        "next_close": clock.get("next_close") or clock.get("nextClose"),
    }


def unwrap_single_symbol_payload(payload: Any, symbol: str) -> dict[str, Any]:
    if isinstance(payload, dict):
        for key in ("quotes", "quote", "result", "data"):
            value = payload.get(key)
            if isinstance(value, dict):
                if symbol in value and isinstance(value[symbol], dict):
                    return value[symbol]
                return value
        if symbol in payload and isinstance(payload[symbol], dict):
            return payload[symbol]
        return payload
    return {}


def decimal_from_quote(quote: dict[str, Any], keys: tuple[str, ...]) -> Decimal | None:
    for key in keys:
        value = quote.get(key)
        if value in (None, ""):
            continue
        try:
            number = Decimal(str(value))
        except Exception:
            continue
        if number > 0:
            return number
    return None


def quantize_price(value: Decimal) -> Decimal:
    minimum = Decimal("0.01")
    price = max(value, minimum)
    return price.quantize(Decimal("0.01"), rounding=ROUND_DOWN)


def compute_limit_price(quote: dict[str, Any], discount: Decimal) -> Decimal:
    bid = decimal_from_quote(quote, ("bp", "bid_price", "bidPrice", "bid"))
    ask = decimal_from_quote(quote, ("ap", "ask_price", "askPrice", "ask"))
    if bid and ask and ask >= bid:
        reference = (bid + ask) / Decimal("2")
    else:
        reference = bid or ask
    if not reference:
        raise RuntimeError("latest quote did not include a usable bid or ask price")
    return quantize_price(reference * discount)


def extract_order_id(payload: Any) -> str:
    if not isinstance(payload, dict):
        return ""
    for key in ("id", "order_id"):
        value = payload.get(key)
        if value:
            return str(value)
    result = payload.get("result")
    if isinstance(result, dict):
        return extract_order_id(result)
    order = payload.get("order")
    if isinstance(order, dict):
        return extract_order_id(order)
    return ""


async def main_async(args: argparse.Namespace) -> int:
    env = read_env()
    run_id = args.run_id or f"{datetime.now(timezone.utc).strftime('%Y-%m-%d-%H%M')}-after-hours-probe"
    symbol = args.symbol.upper()
    client_order_id = f"probe-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}-{symbol.lower()}-eh"
    output_path = args.output_json or (
        ROOT_DIR / "wiki" / "evidence-store" / "sources" / f"{run_id}-alpaca-after-hours-order-probe.json"
    )
    output: dict[str, Any] = {
        "run_id": run_id,
        "created_at": now_utc(),
        "paper": True,
        "alpaca_mcp_only": True,
        "execute": bool(args.execute),
        "symbol": symbol,
        "qty": str(args.qty),
        "client_order_id": client_order_id,
        "order_request": {},
        "clock": {},
        "asset": {},
        "quote": {},
        "submit": {},
        "reconcile": {},
        "cancel": {},
        "status": "dry_run" if not args.execute else "failed",
        "gap_category": "not_applicable",
        "gap_reason": "",
    }

    if env.get("ALPACA_PAPER_TRADE") != "true":
        output["status"] = "failed"
        output["gap_category"] = "paper_mode_env_missing"
        output["gap_reason"] = "ALPACA_PAPER_TRADE=true is required"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(output, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(json.dumps({"status": output["status"], "gap_reason": output["gap_reason"]}, ensure_ascii=False))
        return 64

    server = StdioServerParameters(
        command=str(ROOT_DIR / "scripts" / "alpaca-mcp.sh"),
        args=[],
        env=env,
        cwd=str(ROOT_DIR),
    )

    try:
        with open(os.devnull, "w", encoding="utf-8") as errlog:
            async with stdio_client(server, errlog=errlog) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    clock_row = await call_tool(session, "get_clock", timeout=args.timeout)
                    if clock_row["outcome"] != "pass":
                        raise RuntimeError(clock_row.get("gap_reason") or "get_clock failed")
                    output["clock"] = normalize_clock(clock_row.get("payload"))

                    asset_row = await call_tool(
                        session,
                        "get_asset",
                        {"symbol_or_asset_id": symbol},
                        timeout=args.timeout,
                    )
                    output["asset"] = asset_row
                    if asset_row["outcome"] != "pass":
                        raise RuntimeError(asset_row.get("gap_reason") or "get_asset failed")

                    quote_row = await call_tool(
                        session,
                        "get_stock_latest_quote",
                        {"symbols": symbol, "feed": args.feed},
                        timeout=args.timeout,
                    )
                    output["quote"] = quote_row
                    if quote_row["outcome"] != "pass":
                        raise RuntimeError(quote_row.get("gap_reason") or "get_stock_latest_quote failed")

                    quote = unwrap_single_symbol_payload(quote_row.get("payload"), symbol)
                    limit_price = args.limit_price or compute_limit_price(quote, args.limit_discount)
                    order_request = {
                        "symbol": symbol,
                        "side": "buy",
                        "qty": str(args.qty),
                        "type": "limit",
                        "time_in_force": "day",
                        "limit_price": str(limit_price),
                        "extended_hours": True,
                        "client_order_id": client_order_id,
                    }
                    output["order_request"] = order_request

                    if args.execute:
                        submit_row = await call_tool(
                            session,
                            "place_stock_order",
                            order_request,
                            timeout=args.timeout,
                        )
                        output["submit"] = submit_row
                        if submit_row["outcome"] != "pass":
                            raise RuntimeError(submit_row.get("gap_reason") or "place_stock_order failed")

                        reconcile_row = await call_tool(
                            session,
                            "get_order_by_client_id",
                            {"client_order_id": client_order_id},
                            timeout=args.timeout,
                        )
                        output["reconcile"] = reconcile_row
                        if reconcile_row["outcome"] != "pass":
                            raise RuntimeError(reconcile_row.get("gap_reason") or "get_order_by_client_id failed")

                        order_id = extract_order_id(reconcile_row.get("payload")) or extract_order_id(
                            submit_row.get("payload")
                        )
                        if not args.no_cancel and order_id:
                            output["cancel"] = await call_tool(
                                session,
                                "cancel_order_by_id",
                                {"order_id": order_id},
                                timeout=args.timeout,
                                allow_text=True,
                            )
                        elif not args.no_cancel:
                            output["cancel"] = {
                                "tool": "cancel_order_by_id",
                                "outcome": "failed",
                                "gap_category": "empty_response",
                                "gap_reason": "could not extract order id for cancellation",
                            }

                        if not args.no_cancel and output["cancel"].get("outcome") != "pass":
                            raise RuntimeError(output["cancel"].get("gap_reason") or "cancel_order_by_id failed")
                        output["status"] = "pass"
                    else:
                        output["status"] = "dry_run"
    except Exception as exc:  # noqa: BLE001 - runtime probe report must explain failures.
        output["status"] = "failed"
        output["gap_category"] = classify_error(exc)
        output["gap_reason"] = str(exc)[:500]

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(output, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "run_id": run_id,
                "status": output["status"],
                "symbol": symbol,
                "client_order_id": client_order_id,
                "market_is_open": output.get("clock", {}).get("is_open"),
                "limit_price": output.get("order_request", {}).get("limit_price"),
                "output_json": str(output_path),
                "gap_category": output.get("gap_category"),
                "gap_reason": output.get("gap_reason"),
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0 if output["status"] in {"pass", "dry_run"} else EXIT_PROBE_FAILED


def main() -> None:
    raise SystemExit(asyncio.run(main_async(parse_args())))


if __name__ == "__main__":
    main()
