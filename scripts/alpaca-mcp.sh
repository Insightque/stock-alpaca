#!/usr/bin/env bash
set -euo pipefail

export PATH="/opt/homebrew/bin:/usr/local/bin:/Library/Frameworks/Python.framework/Versions/3.11/bin:${PATH}"

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENV_FILE="${ROOT_DIR}/.env"

if [[ -f "${ENV_FILE}" ]]; then
  set -a
  # shellcheck disable=SC1090
  source "${ENV_FILE}"
  set +a
fi

if [[ -z "${ALPACA_API_KEY:-}" || -z "${ALPACA_SECRET_KEY:-}" ]]; then
  echo "Missing ALPACA_API_KEY or ALPACA_SECRET_KEY. Fill ${ENV_FILE} with your Alpaca paper trading keys." >&2
  exit 1
fi

if [[ "${ALPACA_PAPER_TRADE:-}" != "true" ]]; then
  echo "ALPACA_PAPER_TRADE must be true for this paper-trading harness." >&2
  exit 64
fi

exec uvx alpaca-mcp-server "$@"
