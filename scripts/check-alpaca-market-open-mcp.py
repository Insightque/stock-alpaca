#!/usr/bin/env python3
"""Check Alpaca market clock through the local Alpaca MCP server.

This is a scheduler guard. It does not call Alpaca REST directly and never
submits, replaces, cancels, or closes orders.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
from pathlib import Path
from typing import Any

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


ROOT_DIR = Path(__file__).resolve().parents[1]
EXIT_MARKET_CLOSED = 75
EXIT_MCP_UNAVAILABLE = 70


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check Alpaca market clock through MCP.")
    parser.add_argument("--quiet", action="store_true", help="Print only failures.")
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


def normalize_clock(payload: dict[str, Any]) -> dict[str, Any]:
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


async def get_clock(env: dict[str, str]) -> dict[str, Any]:
    server = StdioServerParameters(
        command=str(ROOT_DIR / "scripts" / "alpaca-mcp.sh"),
        args=[],
        env=env,
        cwd=str(ROOT_DIR),
    )
    with open(os.devnull, "w", encoding="utf-8") as errlog:
        async with stdio_client(server, errlog=errlog) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                return normalize_clock(parse_tool_payload(await session.call_tool("get_clock", {})))


async def main_async(args: argparse.Namespace) -> int:
    env = read_env()
    if env.get("ALPACA_PAPER_TRADE") != "true":
        print("ALPACA_PAPER_TRADE=true is required.", file=sys.stderr)
        return 64

    try:
        clock = await get_clock(env)
    except Exception as exc:  # noqa: BLE001 - scheduler guard should fail closed.
        print(f"Could not confirm Alpaca market clock through MCP: {exc}", file=sys.stderr)
        return EXIT_MCP_UNAVAILABLE

    if not args.quiet or not clock["is_open"]:
        print(json.dumps(clock, ensure_ascii=False, sort_keys=True))
    return 0 if clock["is_open"] else EXIT_MARKET_CLOSED


def main() -> None:
    raise SystemExit(asyncio.run(main_async(parse_args())))


if __name__ == "__main__":
    main()
