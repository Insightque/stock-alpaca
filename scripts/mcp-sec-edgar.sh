#!/usr/bin/env bash
set -euo pipefail

if [ -f .env ]; then
  set -a
  # shellcheck disable=SC1091
  . ./.env
  set +a
fi

if [ -z "${SEC_EDGAR_USER_AGENT:-}" ]; then
  echo "SEC_EDGAR_USER_AGENT is required for SEC EDGAR MCP." >&2
  exit 64
fi

exec uvx sec-edgar-mcp
