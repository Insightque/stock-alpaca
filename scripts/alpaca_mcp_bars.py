#!/usr/bin/env python3
"""Small helpers for read-only Alpaca stock bar calls through MCP."""

from __future__ import annotations

import asyncio
import json
import os
import sys
from pathlib import Path
from typing import Any, Sequence

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


ROOT_DIR = Path(__file__).resolve().parents[1]


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


async def fetch_stock_bars_mcp_async(
    *,
    root: Path = ROOT_DIR,
    symbols: Sequence[str],
    start: str,
    end: str,
    timeframe: str,
    feed: str = "iex",
    adjustment: str = "raw",
    limit: int = 10000,
    sort: str = "asc",
) -> dict[str, list[dict[str, Any]]]:
    env = read_env(root)
    if env.get("ALPACA_PAPER_TRADE") != "true":
        raise SystemExit("ALPACA_PAPER_TRADE must be true before fetching Alpaca MCP data.")
    clean_symbols = [symbol.strip().upper() for symbol in symbols if symbol.strip()]
    if not clean_symbols:
        return {}

    params = StdioServerParameters(
        command=str(root / "scripts" / "alpaca-mcp.sh"),
        args=[],
        env=env,
        cwd=str(root),
    )
    async with stdio_client(params, errlog=sys.stderr) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.call_tool(
                "get_stock_bars",
                {
                    "symbols": ",".join(clean_symbols),
                    "timeframe": timeframe,
                    "start": start,
                    "end": end,
                    "feed": feed,
                    "adjustment": adjustment,
                    "limit": limit,
                    "sort": sort,
                },
            )
    payload = parse_tool_payload(result)
    if payload.get("next_page_token"):
        raise RuntimeError(
            "Alpaca MCP get_stock_bars returned next_page_token; reduce the symbol set or date range"
        )
    bars = payload.get("bars", {})
    if not isinstance(bars, dict):
        raise RuntimeError("Alpaca MCP get_stock_bars payload did not contain a bars object")
    return {
        symbol.upper(): rows
        for symbol, rows in bars.items()
        if isinstance(rows, list)
    }


def fetch_stock_bars_mcp(**kwargs: Any) -> dict[str, list[dict[str, Any]]]:
    return asyncio.run(fetch_stock_bars_mcp_async(**kwargs))
