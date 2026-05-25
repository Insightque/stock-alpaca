#!/usr/bin/env python3
"""Small local MCP server for FRED macro data.

This avoids fetching and executing an npm package at runtime. The server reads
`FRED_API_KEY` from the environment and calls the official FRED API through
curl with the key passed via stdin config, so the key does not appear in the
process list or normal command output.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from typing import Any, BinaryIO


SERVER_NAME = "stock-alpaca-fred"
SERVER_VERSION = "0.1.0"
PROTOCOL_VERSION = "2024-11-05"
FRED_BASE_URL = "https://api.stlouisfed.org/fred"
DEFAULT_SNAPSHOT_SERIES = ["DGS10", "DGS2", "FEDFUNDS", "CPIAUCSL", "UNRATE", "NFCI"]


class McpError(Exception):
    def __init__(self, message: str, code: int = -32000):
        super().__init__(message)
        self.code = code


def require_api_key() -> str:
    api_key = os.environ.get("FRED_API_KEY", "").strip()
    if not api_key:
        raise McpError("FRED_API_KEY is required for FRED MCP.")
    return api_key


def clamp_int(value: Any, default: int, minimum: int, maximum: int) -> int:
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        parsed = default
    return max(minimum, min(maximum, parsed))


def clean_string(value: Any, *, max_len: int = 120) -> str:
    text = str(value or "").strip()
    text = re.sub(r"[\r\n\t]+", " ", text)
    return text[:max_len]


def clean_series_id(value: Any) -> str:
    series_id = clean_string(value, max_len=40).upper()
    if not re.fullmatch(r"[A-Z0-9_.:-]+", series_id):
        raise McpError(f"Invalid FRED series_id: {series_id!r}", code=-32602)
    return series_id


def clean_date(value: Any) -> str | None:
    if value in (None, ""):
        return None
    text = clean_string(value, max_len=10)
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", text):
        raise McpError(f"Invalid date: {text!r}. Use YYYY-MM-DD.", code=-32602)
    return text


def curl_quote(value: Any) -> str:
    text = str(value)
    text = text.replace("\\", "\\\\").replace('"', '\\"')
    return text.replace("\r", " ").replace("\n", " ")


def fred_get(endpoint: str, params: dict[str, Any]) -> dict[str, Any]:
    api_key = require_api_key()
    config_lines = [
        f'url = "{FRED_BASE_URL}/{curl_quote(endpoint)}"',
        "get",
        "silent",
        "show-error",
        "fail",
        "connect-timeout = 10",
        "max-time = 25",
        'user-agent = "stock-alpaca-fred-mcp/0.1"',
    ]
    full_params = {"api_key": api_key, "file_type": "json", **params}
    for key, value in full_params.items():
        if value in (None, ""):
            continue
        config_lines.append(f'data-urlencode = "{curl_quote(key)}={curl_quote(value)}"')
    config = "\n".join(config_lines) + "\n"
    result = subprocess.run(["curl", "--config", "-"], input=config, text=True, capture_output=True)
    if result.returncode != 0:
        message = result.stderr.strip() or f"curl exited with {result.returncode}"
        raise McpError(f"FRED API request failed: {message[:240]}")
    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise McpError(f"FRED API returned invalid JSON: {exc}") from exc
    if "error_message" in payload:
        raise McpError(f"FRED API error: {payload['error_message']}")
    return payload


def get_series_observations(arguments: dict[str, Any]) -> dict[str, Any]:
    params: dict[str, Any] = {
        "series_id": clean_series_id(arguments.get("series_id")),
        "sort_order": clean_string(arguments.get("sort_order") or "desc", max_len=4).lower(),
        "limit": clamp_int(arguments.get("limit"), 10, 1, 1000),
    }
    if params["sort_order"] not in {"asc", "desc"}:
        raise McpError("sort_order must be 'asc' or 'desc'.", code=-32602)
    for name in ("observation_start", "observation_end", "realtime_start", "realtime_end"):
        value = clean_date(arguments.get(name))
        if value:
            params[name] = value
    for name in ("frequency", "aggregation_method", "units"):
        value = clean_string(arguments.get(name), max_len=20)
        if value:
            params[name] = value
    payload = fred_get("series/observations", params)
    return {
        "series_id": params["series_id"],
        "count": len(payload.get("observations", [])),
        "observations": payload.get("observations", []),
    }


def get_series_info(arguments: dict[str, Any]) -> dict[str, Any]:
    series_id = clean_series_id(arguments.get("series_id"))
    payload = fred_get("series", {"series_id": series_id})
    return {"series_id": series_id, "seriess": payload.get("seriess", [])}


def search_series(arguments: dict[str, Any]) -> dict[str, Any]:
    search_text = clean_string(arguments.get("search_text"), max_len=160)
    if not search_text:
        raise McpError("search_text is required.", code=-32602)
    order_by = clean_string(arguments.get("order_by") or "search_rank", max_len=40)
    sort_order = clean_string(arguments.get("sort_order") or "desc", max_len=4).lower()
    if sort_order not in {"asc", "desc"}:
        raise McpError("sort_order must be 'asc' or 'desc'.", code=-32602)
    payload = fred_get(
        "series/search",
        {
            "search_text": search_text,
            "limit": clamp_int(arguments.get("limit"), 10, 1, 100),
            "order_by": order_by,
            "sort_order": sort_order,
        },
    )
    return {
        "search_text": search_text,
        "count": len(payload.get("seriess", [])),
        "seriess": payload.get("seriess", []),
    }


def get_macro_snapshot(arguments: dict[str, Any]) -> dict[str, Any]:
    raw_series = arguments.get("series_ids") or DEFAULT_SNAPSHOT_SERIES
    if not isinstance(raw_series, list):
        raise McpError("series_ids must be an array of FRED series IDs.", code=-32602)
    series_ids = [clean_series_id(item) for item in raw_series[:12]]
    observation_end = clean_date(arguments.get("observation_end"))
    snapshot: list[dict[str, Any]] = []
    for series_id in series_ids:
        params: dict[str, Any] = {"series_id": series_id, "sort_order": "desc", "limit": 1}
        if observation_end:
            params["observation_end"] = observation_end
        payload = fred_get("series/observations", params)
        observations = payload.get("observations", [])
        snapshot.append({"series_id": series_id, "latest": observations[0] if observations else None})
    return {"observation_end": observation_end, "series": snapshot}


TOOLS: dict[str, dict[str, Any]] = {
    "get_series_observations": {
        "description": "Fetch FRED time-series observations for a series ID.",
        "handler": get_series_observations,
        "inputSchema": {
            "type": "object",
            "properties": {
                "series_id": {"type": "string", "description": "FRED series ID, e.g. DGS10, CPIAUCSL, UNRATE."},
                "observation_start": {"type": "string", "description": "Optional YYYY-MM-DD start date."},
                "observation_end": {"type": "string", "description": "Optional YYYY-MM-DD end date."},
                "limit": {"type": "integer", "minimum": 1, "maximum": 1000, "default": 10},
                "sort_order": {"type": "string", "enum": ["asc", "desc"], "default": "desc"},
                "frequency": {"type": "string", "description": "Optional frequency such as d, w, m, q, a."},
                "units": {"type": "string", "description": "Optional FRED units transform, e.g. lin, pc1, pca."},
            },
            "required": ["series_id"],
        },
    },
    "get_series_info": {
        "description": "Fetch metadata for a FRED series ID.",
        "handler": get_series_info,
        "inputSchema": {
            "type": "object",
            "properties": {
                "series_id": {"type": "string", "description": "FRED series ID, e.g. DGS10, CPIAUCSL, UNRATE."}
            },
            "required": ["series_id"],
        },
    },
    "search_series": {
        "description": "Search FRED series by text.",
        "handler": search_series,
        "inputSchema": {
            "type": "object",
            "properties": {
                "search_text": {"type": "string", "description": "Search query, e.g. financial conditions index."},
                "limit": {"type": "integer", "minimum": 1, "maximum": 100, "default": 10},
                "order_by": {"type": "string", "default": "search_rank"},
                "sort_order": {"type": "string", "enum": ["asc", "desc"], "default": "desc"},
            },
            "required": ["search_text"],
        },
    },
    "get_macro_snapshot": {
        "description": "Fetch the latest values for core macro series such as DGS10, DGS2, FEDFUNDS, CPIAUCSL, UNRATE, and NFCI.",
        "handler": get_macro_snapshot,
        "inputSchema": {
            "type": "object",
            "properties": {
                "series_ids": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Optional list of FRED series IDs.",
                },
                "observation_end": {"type": "string", "description": "Optional YYYY-MM-DD as-of date."},
            },
        },
    },
}


def tool_descriptions() -> list[dict[str, Any]]:
    return [
        {
            "name": name,
            "description": spec["description"],
            "inputSchema": spec["inputSchema"],
        }
        for name, spec in TOOLS.items()
    ]


def read_message(stream: BinaryIO) -> dict[str, Any] | None:
    headers: dict[str, str] = {}
    while True:
        line = stream.readline()
        if not line:
            return None
        if line in (b"\r\n", b"\n"):
            break
        key, _, value = line.decode("ascii", errors="replace").partition(":")
        headers[key.lower()] = value.strip()
    length_raw = headers.get("content-length")
    if not length_raw:
        raise McpError("Missing Content-Length header.", code=-32700)
    body = stream.read(int(length_raw))
    if not body:
        return None
    return json.loads(body.decode("utf-8"))


def write_message(stream: BinaryIO, payload: dict[str, Any]) -> None:
    body = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    stream.write(f"Content-Length: {len(body)}\r\n\r\n".encode("ascii") + body)
    stream.flush()


def jsonrpc_error(message_id: Any, code: int, message: str) -> dict[str, Any]:
    return {"jsonrpc": "2.0", "id": message_id, "error": {"code": code, "message": message}}


def jsonrpc_result(message_id: Any, result: dict[str, Any]) -> dict[str, Any]:
    return {"jsonrpc": "2.0", "id": message_id, "result": result}


def handle_request(request: dict[str, Any]) -> dict[str, Any] | None:
    method = request.get("method")
    message_id = request.get("id")
    if method == "initialize":
        return jsonrpc_result(
            message_id,
            {
                "protocolVersion": PROTOCOL_VERSION,
                "capabilities": {"tools": {}},
                "serverInfo": {"name": SERVER_NAME, "version": SERVER_VERSION},
            },
        )
    if method == "ping":
        return jsonrpc_result(message_id, {})
    if method == "tools/list":
        return jsonrpc_result(message_id, {"tools": tool_descriptions()})
    if method == "tools/call":
        params = request.get("params") or {}
        tool_name = params.get("name")
        arguments = params.get("arguments") or {}
        if tool_name not in TOOLS:
            return jsonrpc_error(message_id, -32601, f"Unknown tool: {tool_name}")
        try:
            data = TOOLS[tool_name]["handler"](arguments)
            text = json.dumps(data, ensure_ascii=False, indent=2)
            return jsonrpc_result(message_id, {"content": [{"type": "text", "text": text}], "isError": False})
        except McpError as exc:
            return jsonrpc_result(
                message_id,
                {"content": [{"type": "text", "text": str(exc)}], "isError": True},
            )
    if method and method.startswith("notifications/"):
        return None
    return jsonrpc_error(message_id, -32601, f"Unknown method: {method}")


def serve() -> None:
    require_api_key()
    while True:
        try:
            request = read_message(sys.stdin.buffer)
        except Exception as exc:
            write_message(sys.stdout.buffer, jsonrpc_error(None, -32700, str(exc)))
            continue
        if request is None:
            return
        response = handle_request(request)
        if response is not None:
            write_message(sys.stdout.buffer, response)


def health_check() -> int:
    require_api_key()
    payload = fred_get("series/observations", {"series_id": "DGS10", "sort_order": "desc", "limit": 1})
    observations = payload.get("observations", [])
    if not observations:
        print("fred_api: no_observations")
        return 2
    latest = observations[0]
    print("fred_api: ok")
    print("series: DGS10")
    print(f"latest_date: {latest.get('date', '-')}")
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(description="Local FRED MCP server.")
    parser.add_argument("--health-check", action="store_true", help="Call the official FRED API once and exit.")
    args = parser.parse_args()
    try:
        raise SystemExit(health_check() if args.health_check else serve())
    except McpError as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(64)


if __name__ == "__main__":
    main()
