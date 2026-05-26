#!/usr/bin/env python3
"""Capture scheduler-owned research MCP preflight data.

This script talks to the local research MCP wrappers over stdio. It is intended
for scheduled Codex runs where some local MCP servers are configured but not
exposed as first-class Codex tools inside the nested non-interactive session.
It never submits orders and never prints API keys.
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
MCP_TIMEOUT_SECONDS = 45
STDERR_CAPTURE_LIMIT = 4000


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


def classify_error(exc: BaseException) -> str:
    text = str(exc).lower()
    if "could not resolve host" in text or "nodename nor servname" in text:
        return "dns"
    if "api_key" in text or "unauthorized" in text or "forbidden" in text:
        return "auth"
    if "timed out" in text or "timeout" in text:
        return "timeout"
    if "iserror" in text or "api request failed" in text:
        return "provider_error"
    return "unknown"


def encode_message(payload: dict[str, Any]) -> bytes:
    body = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    return f"Content-Length: {len(body)}\r\n\r\n".encode("ascii") + body


async def write_message(writer: asyncio.StreamWriter, payload: dict[str, Any]) -> None:
    writer.write(encode_message(payload))
    await writer.drain()


async def read_message(reader: asyncio.StreamReader) -> dict[str, Any]:
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
    for item in result.get("content") or []:
        if not isinstance(item, dict) or not item.get("text"):
            continue
        try:
            payload = json.loads(item["text"])
        except json.JSONDecodeError:
            continue
        if isinstance(payload, dict):
            return payload
    raise RuntimeError(f"Could not parse MCP tool response as JSON: {result}")


async def call_stdio_tool(
    *,
    command: Path,
    env: dict[str, str],
    tool_name: str,
    arguments: dict[str, Any],
) -> dict[str, Any]:
    proc_args = [str(command)]
    if command.suffix == ".sh" and not os.access(command, os.X_OK):
        proc_args = ["/bin/bash", str(command)]
    proc = await asyncio.create_subprocess_exec(
        *proc_args,
        cwd=str(ROOT_DIR),
        env=env,
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    if proc.stdin is None or proc.stdout is None:
        raise RuntimeError("MCP subprocess did not expose stdio pipes.")

    stderr_chunks: list[bytes] = []
    stderr_task = asyncio.create_task(drain_stderr(proc.stderr, stderr_chunks))

    async def exchange() -> dict[str, Any]:
        await write_message(
            proc.stdin,
            {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {},
                    "clientInfo": {"name": "stock-alpaca-scheduler-preflight", "version": "0.1.0"},
                },
            },
        )
        initialized = await read_message(proc.stdout)
        if "error" in initialized:
            raise RuntimeError(f"MCP initialize failed: {initialized['error']}")
        await write_message(proc.stdin, {"jsonrpc": "2.0", "method": "notifications/initialized", "params": {}})
        await write_message(
            proc.stdin,
            {
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/call",
                "params": {"name": tool_name, "arguments": arguments},
            },
        )
        response = await read_message(proc.stdout)
        if "error" in response:
            raise RuntimeError(f"MCP tools/call failed: {response['error']}")
        return parse_tool_payload(response.get("result") or {})

    try:
        return await asyncio.wait_for(exchange(), timeout=MCP_TIMEOUT_SECONDS)
    except asyncio.TimeoutError as exc:
        raise TimeoutError(f"MCP stdio call timed out after {MCP_TIMEOUT_SECONDS}s") from exc
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


async def capture_fred(env: dict[str, str]) -> dict[str, Any]:
    checked_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    if not env.get("FRED_API_KEY"):
        return {
            "server": "fred",
            "queried": False,
            "outcome": "unavailable",
            "checked_at": checked_at,
            "gap_category": "auth",
            "gap_reason": "FRED_API_KEY is not present in the scheduler environment.",
            "retry_count": 0,
        }
    try:
        payload = await call_stdio_tool(
            command=ROOT_DIR / "scripts" / "mcp-fred.sh",
            env=env,
            tool_name="get_macro_snapshot",
            arguments={"series_ids": DEFAULT_FRED_SERIES},
        )
    except Exception as exc:
        return {
            "server": "fred",
            "queried": True,
            "outcome": "failed",
            "checked_at": checked_at,
            "gap_category": classify_error(exc),
            "gap_reason": str(exc)[:240],
            "retry_count": 0,
        }
    return {
        "server": "fred",
        "queried": True,
        "outcome": "pass",
        "checked_at": checked_at,
        "gap_category": "not_applicable",
        "gap_reason": "",
        "retry_count": 0,
        "tool": "get_macro_snapshot",
        "payload": payload,
    }


async def main_async() -> int:
    parser = argparse.ArgumentParser(description="Capture scheduler-owned research MCP preflight data.")
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--output-json", type=Path, required=True)
    args = parser.parse_args()

    env = read_env()
    captured_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    fred = await capture_fred(env)
    output = {
        "run_id": args.run_id,
        "created_at": captured_at,
        "paper": env.get("ALPACA_PAPER_TRADE") == "true",
        "source": "scheduler local MCP stdio preflight",
        "providers": [fred],
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(output, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({k: output[k] for k in ("run_id", "created_at", "paper")}, ensure_ascii=False))
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
