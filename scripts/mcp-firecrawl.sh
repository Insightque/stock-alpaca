#!/usr/bin/env bash
set -euo pipefail

if [ -f .env ]; then
  set -a
  # shellcheck disable=SC1091
  . ./.env
  set +a
fi

if [ -z "${FIRECRAWL_API_KEY:-}" ]; then
  echo "FIRECRAWL_API_KEY is required for Firecrawl MCP." >&2
  exit 64
fi

exec npx -y firecrawl-mcp
