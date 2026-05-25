#!/usr/bin/env python3
"""Fetch historical 1Hour stock bars through the local Alpaca MCP server.

The output preserves timestamps for intraday backtests. This helper only calls
read-only Alpaca MCP tools and never submits, replaces, cancels, or closes
orders.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


ROOT_DIR = Path(__file__).resolve().parents[1]
ET = ZoneInfo("America/New_York")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fetch Alpaca historical hourly bars through MCP.")
    parser.add_argument("--symbols", required=True, help="Comma-separated symbols.")
    parser.add_argument("--start", required=True, help="RFC3339 start time.")
    parser.add_argument("--end", required=True, help="RFC3339 end time.")
    parser.add_argument("--timeframe", default="1Hour")
    parser.add_argument("--feed", default="iex")
    parser.add_argument("--adjustment", default="all")
    parser.add_argument("--batch-size", type=int, default=5)
    parser.add_argument("--chunk-days", type=int, default=14, help="Date chunk size used to avoid MCP pagination.")
    parser.add_argument("--progress", action="store_true", help="Print agent-style progress lines.")
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


def progress(enabled: bool, agent: str, message: str) -> None:
    if enabled:
        print(f"[{agent}] {message}", flush=True)


def parse_rfc3339(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)


def format_rfc3339(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def iter_time_chunks(start: str, end: str, chunk_days: int) -> list[tuple[str, str]]:
    start_dt = parse_rfc3339(start)
    end_dt = parse_rfc3339(end)
    if chunk_days <= 0:
        return [(format_rfc3339(start_dt), format_rfc3339(end_dt))]
    chunks = []
    current = start_dt
    while current <= end_dt:
        chunk_end = min(current + timedelta(days=chunk_days) - timedelta(seconds=1), end_dt)
        chunks.append((format_rfc3339(current), format_rfc3339(chunk_end)))
        current = chunk_end + timedelta(seconds=1)
    return chunks


async def fetch_batch(
    session: ClientSession,
    symbols: list[str],
    args: argparse.Namespace,
    *,
    start: str,
    end: str,
) -> dict[str, list[dict[str, Any]]]:
    payload = {
        "symbols": ",".join(symbols),
        "timeframe": args.timeframe,
        "start": start,
        "end": end,
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
    return {symbol.upper(): rows for symbol, rows in bars.items() if isinstance(rows, list)}


def normalize_row(row: dict[str, Any]) -> dict[str, Any]:
    timestamp = str(row["t"])
    parsed = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    et = parsed.astimezone(ET)
    return {
        "timestamp": timestamp,
        "date_et": et.date().isoformat(),
        "time_et": et.strftime("%H:%M:%S"),
        "open": row.get("o"),
        "high": row.get("h"),
        "low": row.get("l"),
        "close": row.get("c"),
        "volume": row.get("v"),
        "vwap": row.get("vw"),
        "trade_count": row.get("n"),
    }


async def main_async(args: argparse.Namespace) -> None:
    env = read_env()
    if env.get("ALPACA_PAPER_TRADE") != "true":
        raise SystemExit("ALPACA_PAPER_TRADE must be true before fetching Alpaca MCP data.")
    symbols = [symbol.strip().upper() for symbol in args.symbols.split(",") if symbol.strip()]
    if not symbols:
        raise SystemExit("--symbols did not contain any symbols")

    progress(args.progress, "Coordinator Agent", "paper 모드 확인 완료; hourly MCP 캡처를 시작합니다.")
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
            chunks = iter_time_chunks(args.start, args.end, args.chunk_days)
            for chunk_index, (chunk_start, chunk_end) in enumerate(chunks, start=1):
                for offset in range(0, len(symbols), args.batch_size):
                    batch = symbols[offset : offset + args.batch_size]
                    progress(
                        args.progress,
                        "Market Data Agent",
                        f"chunk {chunk_index}/{len(chunks)} {chunk_start[:10]}~{chunk_end[:10]}, "
                        f"{offset + 1}-{min(offset + args.batch_size, len(symbols))}/{len(symbols)} 심볼 조회 중: {','.join(batch)}",
                    )
                    batch_bars = await fetch_batch(session, batch, args, start=chunk_start, end=chunk_end)
                    for symbol, rows in batch_bars.items():
                        all_bars.setdefault(symbol, []).extend(rows)

    hourly_bars = {}
    for symbol, rows in sorted(all_bars.items()):
        deduped = {str(row["t"]): row for row in rows if row.get("t")}
        hourly_bars[symbol] = [normalize_row(row) for _, row in sorted(deduped.items())]
    bar_counts = {symbol: len(rows) for symbol, rows in hourly_bars.items()}
    symbols_loaded = len(hourly_bars)
    missing_symbols = sorted(set(symbols) - set(hourly_bars))
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
        "extracted": {
            "hourly_bars": hourly_bars,
        },
        "data_manifest": {
            "source_feed": f"alpaca_{args.feed}",
            "bar_interval": args.timeframe,
            "adjusted_prices": args.adjustment != "raw",
            "timezone": "America/New_York",
            "trading_calendar": "nyse",
            "symbols_requested": len(symbols),
            "symbols_loaded": symbols_loaded,
            "bars_loaded": sum(bar_counts.values()),
            "bar_counts": bar_counts,
            "missing_symbols": missing_symbols,
            "stale_quotes": 0,
            "corporate_actions_checked": args.adjustment != "raw",
            "survivorship_bias_controlled": False,
        },
        "data_gaps": [
            "Historical hourly bars do not include bid/ask spread, queue priority, or limit-fill probability.",
            "IEX feed can differ from consolidated SIP prices and volume.",
            "Survivorship-bias control is partial unless the universe was captured as-of each historical day.",
        ],
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(output, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    progress(
        args.progress,
        "Market Data Agent",
        f"캡처 완료: {symbols_loaded}/{len(symbols)} 심볼, {sum(bar_counts.values())}개 hourly bars 저장.",
    )


def main() -> None:
    asyncio.run(main_async(parse_args()))


if __name__ == "__main__":
    main()
