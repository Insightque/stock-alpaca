#!/usr/bin/env python3
"""Small local MCP server for Firecrawl.

This avoids fetching and executing an npm package at runtime. The server reads
`FIRECRAWL_API_KEY` from the environment and calls the official Firecrawl API
through curl with the key passed via stdin config, so the key does not appear
in the process list or normal command output.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from typing import Any, BinaryIO


SERVER_NAME = "stock-alpaca-firecrawl"
SERVER_VERSION = "0.1.0"
PROTOCOL_VERSION = "2024-11-05"
FIRECRAWL_BASE_URL = "https://api.firecrawl.dev/v2"


class McpError(Exception):
    def __init__(self, message: str, code: int = -32000):
        super().__init__(message)
        self.code = code


def require_api_key() -> str:
    api_key = os.environ.get("FIRECRAWL_API_KEY", "").strip()
    if not api_key:
        raise McpError("FIRECRAWL_API_KEY is required for Firecrawl MCP.")
    return api_key


def clean_url(value: Any) -> str:
    url = str(value or "").strip()
    if not re.fullmatch(r"https?://[^\s]+", url):
        raise McpError(f"Invalid URL: {url!r}", code=-32602)
    return url


def clean_string(value: Any, *, max_len: int = 240) -> str:
    text = str(value or "").strip()
    text = re.sub(r"[\r\n\t]+", " ", text)
    return text[:max_len]


def clamp_int(value: Any, default: int, minimum: int, maximum: int) -> int:
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        parsed = default
    return max(minimum, min(maximum, parsed))


def clean_bool(value: Any, default: bool = False) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "on"}
    return bool(value)


def clean_formats(value: Any, default: list[str]) -> list[str]:
    allowed = {
        "markdown",
        "html",
        "rawHtml",
        "links",
        "summary",
        "json",
        "query",
        "screenshot",
        "changeTracking",
        "branding",
    }
    if value is None:
        return default
    if not isinstance(value, list):
        raise McpError("formats must be an array.", code=-32602)
    formats = [clean_string(item, max_len=40) for item in value if clean_string(item, max_len=40) in allowed]
    return formats or default


def curl_quote(value: Any) -> str:
    text = str(value)
    text = text.replace("\\", "\\\\").replace('"', '\\"')
    return text.replace("\r", " ").replace("\n", " ")


def firecrawl_post(endpoint: str, body: dict[str, Any]) -> dict[str, Any]:
    api_key = require_api_key()
    json_body = json.dumps(body, ensure_ascii=False, separators=(",", ":"))
    config_lines = [
        f'url = "{FIRECRAWL_BASE_URL}/{curl_quote(endpoint)}"',
        'request = "POST"',
        f'header = "Authorization: Bearer {curl_quote(api_key)}"',
        'header = "Content-Type: application/json"',
        f'data = "{curl_quote(json_body)}"',
        "silent",
        "show-error",
        "connect-timeout = 10",
        "max-time = 60",
        'user-agent = "stock-alpaca-firecrawl-mcp/0.1"',
    ]
    config = "\n".join(config_lines) + "\n"
    result = subprocess.run(["curl", "--config", "-"], input=config, text=True, capture_output=True)
    if result.returncode != 0:
        message = result.stderr.strip() or f"curl exited with {result.returncode}"
        raise McpError(f"Firecrawl API request failed: {message[:240]}")
    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise McpError(f"Firecrawl API returned invalid JSON: {exc}") from exc
    if payload.get("success") is False:
        raise McpError(f"Firecrawl API error: {payload.get('error') or payload}")
    return payload


def optional_array(arguments: dict[str, Any], name: str) -> list[Any] | None:
    value = arguments.get(name)
    if value is None:
        return None
    if not isinstance(value, list):
        raise McpError(f"{name} must be an array.", code=-32602)
    return value


def firecrawl_scrape(arguments: dict[str, Any]) -> dict[str, Any]:
    body: dict[str, Any] = {
        "url": clean_url(arguments.get("url")),
        "formats": clean_formats(arguments.get("formats"), ["markdown"]),
        "onlyMainContent": clean_bool(arguments.get("onlyMainContent"), True),
    }
    if arguments.get("maxAge") is not None:
        body["maxAge"] = clamp_int(arguments.get("maxAge"), 3600000, 0, 31_536_000_000)
    if arguments.get("waitFor") is not None:
        body["waitFor"] = clamp_int(arguments.get("waitFor"), 0, 0, 30000)
    if arguments.get("zeroDataRetention") is not None:
        body["zeroDataRetention"] = clean_bool(arguments.get("zeroDataRetention"), False)
    for name in ("includeTags", "excludeTags", "parsers"):
        value = optional_array(arguments, name)
        if value is not None:
            body[name] = value
    for name in ("jsonOptions", "queryOptions", "pdfOptions"):
        value = arguments.get(name)
        if isinstance(value, dict):
            body[name] = value
    payload = firecrawl_post("scrape", body)
    return payload


def firecrawl_map(arguments: dict[str, Any]) -> dict[str, Any]:
    body: dict[str, Any] = {"url": clean_url(arguments.get("url"))}
    if arguments.get("search"):
        body["search"] = clean_string(arguments.get("search"), max_len=200)
    if arguments.get("limit") is not None:
        body["limit"] = clamp_int(arguments.get("limit"), 20, 1, 500)
    for name in ("includeSubdomains", "ignoreQueryParameters"):
        if arguments.get(name) is not None:
            body[name] = clean_bool(arguments.get(name), False)
    sitemap = clean_string(arguments.get("sitemap"), max_len=20)
    if sitemap:
        body["sitemap"] = sitemap
    return firecrawl_post("map", body)


TOOLS: dict[str, dict[str, Any]] = {
    "firecrawl_scrape": {
        "description": "Scrape a single URL through the official Firecrawl API.",
        "handler": firecrawl_scrape,
        "inputSchema": {
            "type": "object",
            "properties": {
                "url": {"type": "string", "description": "URL to scrape."},
                "formats": {"type": "array", "items": {"type": "string"}, "default": ["markdown"]},
                "onlyMainContent": {"type": "boolean", "default": True},
                "maxAge": {"type": "integer", "description": "Cache max age in milliseconds."},
                "waitFor": {"type": "integer", "description": "Optional render wait in milliseconds."},
                "zeroDataRetention": {"type": "boolean", "default": False},
                "includeTags": {"type": "array", "items": {"type": "string"}},
                "excludeTags": {"type": "array", "items": {"type": "string"}},
                "jsonOptions": {"type": "object"},
                "queryOptions": {"type": "object"},
            },
            "required": ["url"],
        },
    },
    "firecrawl_map": {
        "description": "Map a site through the official Firecrawl API.",
        "handler": firecrawl_map,
        "inputSchema": {
            "type": "object",
            "properties": {
                "url": {"type": "string", "description": "Site URL to map."},
                "search": {"type": "string", "description": "Optional search filter."},
                "limit": {"type": "integer", "minimum": 1, "maximum": 500},
                "includeSubdomains": {"type": "boolean"},
                "ignoreQueryParameters": {"type": "boolean"},
                "sitemap": {"type": "string"},
            },
            "required": ["url"],
        },
    },
}


def tool_descriptions() -> list[dict[str, Any]]:
    return [
        {"name": name, "description": spec["description"], "inputSchema": spec["inputSchema"]}
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
    payload = firecrawl_scrape({"url": "https://example.com", "formats": ["markdown"], "onlyMainContent": True})
    markdown = ((payload.get("data") or {}).get("markdown") or "") if isinstance(payload, dict) else ""
    print("firecrawl_api: ok" if payload.get("success") else "firecrawl_api: not_ok")
    print(f"markdown_chars: {len(markdown)}")
    return 0 if payload.get("success") else 2


def main() -> None:
    parser = argparse.ArgumentParser(description="Local Firecrawl MCP server.")
    parser.add_argument("--health-check", action="store_true", help="Call the official Firecrawl API once and exit.")
    args = parser.parse_args()
    try:
        raise SystemExit(health_check() if args.health_check else serve())
    except McpError as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(64)


if __name__ == "__main__":
    main()
