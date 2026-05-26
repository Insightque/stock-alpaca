#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

export XDG_CACHE_HOME="${XDG_CACHE_HOME:-${ROOT_DIR}/.cache}"
export XDG_DATA_HOME="${XDG_DATA_HOME:-${ROOT_DIR}/.cache/xdg-data}"
export UV_CACHE_DIR="${UV_CACHE_DIR:-${XDG_CACHE_HOME}/uv}"
export UV_TOOL_DIR="${UV_TOOL_DIR:-${ROOT_DIR}/.cache/uv/tools}"
export UV_LINK_MODE="${UV_LINK_MODE:-copy}"
export UV_PYTHON_DOWNLOADS="${UV_PYTHON_DOWNLOADS:-never}"
mkdir -p "${UV_CACHE_DIR}" "${UV_TOOL_DIR}" "${XDG_DATA_HOME}"

if [ -f "$ROOT_DIR/.env" ]; then
  set -a
  # shellcheck disable=SC1091
  . "$ROOT_DIR/.env"
  set +a
fi

if [ -z "${ALPHA_VANTAGE_API_KEY:-}" ]; then
  echo "ALPHA_VANTAGE_API_KEY is required for Alpha Vantage MCP." >&2
  exit 64
fi

export ALPHA_VANTAGE_API_KEY

if command -v marketdata-mcp >/dev/null 2>&1; then
  exec marketdata-mcp
fi

exec uvx --from marketdata-mcp-server marketdata-mcp
