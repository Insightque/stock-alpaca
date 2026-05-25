#!/usr/bin/env python3
"""Fetch historical bars through the local Alpaca MCP server.

This script talks to ``scripts/alpaca-mcp.sh`` over the MCP stdio protocol. It
does not call Alpaca REST endpoints directly and never submits, replaces,
cancels, or closes orders.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


ROOT_DIR = Path(__file__).resolve().parents[1]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fetch Alpaca historical bars through MCP.")
    parser.add_argument("--symbols", required=True, help="Comma-separated symbols.")
    parser.add_argument("--start", required=True, help="RFC3339 start time.")
    parser.add_argument("--end", required=True, help="RFC3339 end time.")
    parser.add_argument("--timeframe", default="1Day")
    parser.add_argument("--feed", default="iex")
    parser.add_argument("--adjustment", default="all")
    parser.add_argument("--batch-size", type=int, default=12)
    parser.add_argument("--output-json", type=Path, required=True)
    return parser.parse_args()


def read_env() -> dict[str, str]:
    env = os.environ.copy()
    env_file = ROOT_DIR / ".env"
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            if not stripped or stripped.startswith("#") or "=" not in stripped:
                continue
            key, value = stripped.split("=", 1)
            env.setdefault(key.strip(), value.strip().strip('"').strip("'"))
    return env


def parse_tool_payload(result: Any) -> dict[str, Any]:
    for item in getattr(result, "content", []):
        text = getattr(item, "text", None)
        if not text:
            continue
        try:
            payload = json.loads(text)
        except json.JSONDecodeError:
            continue
        if isinstance(payload, dict):
            return payload
    dumped = result.model_dump() if hasattr(result, "model_dump") else {"result": str(result)}
    raise RuntimeError(f"Could not parse MCP tool response as JSON: {dumped}")


async def fetch_batch(session: ClientSession, symbols: list[str], args: argparse.Namespace) -> dict[str, list[dict[str, Any]]]:
    payload = {
        "symbols": ",".join(symbols),
        "timeframe": args.timeframe,
        "start": args.start,
        "end": args.end,
        "feed": args.feed,
        "adjustment": args.adjustment,
        "limit": 10000,
        "sort": "asc",
    }
    result = await session.call_tool("get_stock_bars", payload)
    parsed = parse_tool_payload(result)
    if parsed.get("error"):
        raise RuntimeError(f"MCP get_stock_bars returned error: {parsed['error']}")
    if parsed.get("next_page_token"):
        raise RuntimeError(
            "MCP get_stock_bars returned next_page_token; reduce --batch-size or date range to avoid pagination loss"
        )
    bars = parsed.get("bars", {})
    if not isinstance(bars, dict):
        raise RuntimeError("MCP get_stock_bars payload did not contain a bars object")
    return {symbol: rows for symbol, rows in bars.items() if isinstance(rows, list)}


async def main_async(args: argparse.Namespace) -> None:
    env = read_env()
    if env.get("ALPACA_PAPER_TRADE") != "true":
        raise SystemExit("ALPACA_PAPER_TRADE must be true before fetching Alpaca MCP data.")
    symbols = [symbol.strip().upper() for symbol in args.symbols.split(",") if symbol.strip()]
    if not symbols:
        raise SystemExit("--symbols did not contain any symbols")

    server = StdioServerParameters(
        command=str(ROOT_DIR / "scripts" / "alpaca-mcp.sh"),
        args=[],
        env=env,
        cwd=str(ROOT_DIR),
    )
    all_bars: dict[str, list[dict[str, Any]]] = {}
    async with stdio_client(server, errlog=sys.stderr) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            for offset in range(0, len(symbols), args.batch_size):
                batch = symbols[offset : offset + args.batch_size]
                all_bars.update(await fetch_batch(session, batch, args))

    extracted = {
        "daily_bars": {
            symbol: [
                {
                    "date": str(row["t"])[:10],
                    "open": row.get("o"),
                    "high": row.get("h"),
                    "low": row.get("l"),
                    "close": row.get("c"),
                    "volume": row.get("v"),
                    "vwap": row.get("vw"),
                    "trade_count": row.get("n"),
                }
                for row in rows
            ]
            for symbol, rows in sorted(all_bars.items())
        }
    }
    symbols_loaded = len(extracted["daily_bars"])
    missing_symbols = sorted(set(symbols) - set(extracted["daily_bars"]))
    output = {
        "created_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "paper": True,
        "orders_submitted": 0,
        "source": "Alpaca MCP get_stock_bars",
        "request": {
            "symbols": symbols,
            "start": args.start,
            "end": args.end,
            "timeframe": args.timeframe,
            "feed": args.feed,
            "adjustment": args.adjustment,
        },
        "extracted": extracted,
        "data_manifest": {
            "source_feed": f"alpaca_{args.feed}",
            "bar_interval": args.timeframe,
            "adjusted_prices": args.adjustment != "raw",
            "timezone": "America/New_York",
            "trading_calendar": "nyse",
            "symbols_requested": len(symbols),
            "symbols_loaded": symbols_loaded,
            "missing_symbol_dates": 0,
            "stale_quotes": 0,
            "corporate_actions_checked": args.adjustment != "raw",
            "survivorship_bias_controlled": False,
            "missing_symbols": missing_symbols,
        },
        "data_gaps": [
            "Historical daily bars do not include quote-level spread or fill probability.",
            "Survivorship-bias control is partial unless the universe was captured as-of each historical day.",
        ],
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(output, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> None:
    asyncio.run(main_async(parse_args()))


if __name__ == "__main__":
    main()
