#!/usr/bin/env bash
set -euo pipefail

export PATH="/opt/homebrew/bin:/usr/local/bin:/Library/Frameworks/Python.framework/Versions/3.11/bin:${PATH}"

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LOCK_DIR="${ROOT_DIR}/.locks/analyst-review.lock"
LOG_DIR="${ROOT_DIR}/logs"

mkdir -p "${ROOT_DIR}/.locks" "${LOG_DIR}"

if ! mkdir "${LOCK_DIR}" 2>/dev/null; then
  echo "$(date -Is) analyst review already running; exiting."
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

cat <<'PROMPT' | codex --search -a never exec -C "${ROOT_DIR}" -
You are running the stock-alpaca scheduled analyst review cycle.

Execute `harness/workflows/analyst-review-cycle.md` exactly.

Hard requirements:
- This workflow never submits, replaces, cancels, or closes orders.
- Use Alpaca MCP for account, order, activity, position, and market-data reconciliation.
- Review paper trades, open positions, skipped recommendations, and due 1D/5D/20D review horizons.
- Write detailed analyst-style review artifacts and log entries.
- Update recommendation policy only when the evidence threshold in the workflow is met.
- Do not touch unrelated dirty files.

Start now.
PROMPT

"${ROOT_DIR}/scripts/git-autopush-artifacts.sh" "analyst-review"
