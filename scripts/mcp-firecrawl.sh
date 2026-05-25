#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENV_FILE="${ROOT_DIR}/.env"

if [[ -f "${ENV_FILE}" ]]; then
  set -a
  # shellcheck disable=SC1090
  source "${ENV_FILE}"
  set +a
fi

if [[ -z "${FIRECRAWL_API_KEY:-}" ]]; then
  echo "FIRECRAWL_API_KEY is required for Firecrawl MCP." >&2
  exit 64
fi

exec python3 "${ROOT_DIR}/scripts/firecrawl-mcp-server.py" "$@"
