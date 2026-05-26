#!/usr/bin/env bash
set -euo pipefail

export PATH="/opt/homebrew/bin:/usr/local/bin:/Library/Frameworks/Python.framework/Versions/3.11/bin:${PATH}"

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LOCK_DIR="${ROOT_DIR}/.locks/hourly-autopilot.lock"
LOG_DIR="${ROOT_DIR}/logs"
PROMPT_FILE="${ROOT_DIR}/harness/workflows/hourly-autopilot.md"

mkdir -p "${ROOT_DIR}/.locks" "${LOG_DIR}"

if ! mkdir "${LOCK_DIR}" 2>/dev/null; then
  echo "$(date -Is) hourly autopilot already running; exiting."
  exit 0
fi

cleanup() {
  rmdir "${LOCK_DIR}" 2>/dev/null || true
}
trap cleanup EXIT

cd "${ROOT_DIR}"

if ! grep -q '^ALPACA_PAPER_TRADE=true$' .env; then
  echo "$(date -Is) ALPACA_PAPER_TRADE=true is required; exiting."
  exit 64
fi

cat <<'PROMPT' | codex exec --search -a never -C "${ROOT_DIR}" -
You are running the stock-alpaca hourly paper autopilot.

Execute `harness/workflows/hourly-autopilot.md` exactly. The user explicitly authorized hourly current-market recommendations and automatic Alpaca paper buy/sell operation on 2026-05-26, but only within the workflow's safety rules.

Hard requirements:
- Paper trading only; abort if `ALPACA_PAPER_TRADE=true` is not present.
- Use Alpaca MCP for all account, market, position, and order operations.
- Do not call Alpaca trading REST endpoints directly.
- Submit paper orders only if the market is open and universe, MCP, quote, spread, and risk gates all pass.
- If any gate fails, submit nothing and still write the report, manifest, order plan, and log entry.
- Record detailed buy/sell rationale for every proposed or submitted order so analyst reviews can improve policy later.
- After any submit attempt, run post-trade reconciliation.
- Do not touch unrelated dirty files.

Start now.
PROMPT
