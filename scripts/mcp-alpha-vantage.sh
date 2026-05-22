#!/usr/bin/env bash
set -euo pipefail

if [ -f .env ]; then
  set -a
  # shellcheck disable=SC1091
  . ./.env
  set +a
fi

if [ -z "${ALPHA_VANTAGE_API_KEY:-}" ]; then
  echo "ALPHA_VANTAGE_API_KEY is required for Alpha Vantage MCP." >&2
  exit 64
fi

exec uvx --from marketdata-mcp-server marketdata-mcp "$ALPHA_VANTAGE_API_KEY"
