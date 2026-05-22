#!/usr/bin/env bash
set -euo pipefail

if [ -f .env ]; then
  set -a
  # shellcheck disable=SC1091
  . ./.env
  set +a
fi

if [ -z "${FRED_API_KEY:-}" ]; then
  echo "FRED_API_KEY is required for FRED MCP." >&2
  exit 64
fi

exec npx -y fred-mcp-server
