#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

if [ -f "$ROOT_DIR/.env" ]; then
  set -a
  # shellcheck disable=SC1091
  . "$ROOT_DIR/.env"
  set +a
fi

if [ -z "${FRED_API_KEY:-}" ]; then
  echo "FRED_API_KEY is required for FRED MCP." >&2
  exit 64
fi

exec python3 "$SCRIPT_DIR/fred-mcp-server.py" "$@"
