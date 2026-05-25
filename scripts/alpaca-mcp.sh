#!/usr/bin/env bash
set -euo pipefail

export PATH="/opt/homebrew/bin:/usr/local/bin:/Library/Frameworks/Python.framework/Versions/3.11/bin:${PATH}"

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENV_FILE="${ROOT_DIR}/.env"

export XDG_CACHE_HOME="${XDG_CACHE_HOME:-${ROOT_DIR}/.cache}"
export XDG_DATA_HOME="${XDG_DATA_HOME:-${ROOT_DIR}/.cache/xdg-data}"
export UV_CACHE_DIR="${UV_CACHE_DIR:-${XDG_CACHE_HOME}/uv}"
export UV_TOOL_DIR="${UV_TOOL_DIR:-${ROOT_DIR}/.cache/uv/tools}"
export UV_LINK_MODE="${UV_LINK_MODE:-copy}"
export UV_PYTHON_DOWNLOADS="${UV_PYTHON_DOWNLOADS:-never}"
mkdir -p "${UV_CACHE_DIR}" "${UV_TOOL_DIR}" "${XDG_DATA_HOME}"

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

if command -v alpaca-mcp-server >/dev/null 2>&1; then
  exec alpaca-mcp-server "$@"
fi

exec uvx alpaca-mcp-server "$@"
