#!/usr/bin/env bash
set -euo pipefail

export PATH="/opt/homebrew/bin:/usr/local/bin:/Library/Frameworks/Python.framework/Versions/3.11/bin:${PATH}"
export CODEX_HOME="${CODEX_AUTOPILOT_CODEX_HOME:-${CODEX_SCHEDULED_CODEX_HOME:-${HOME}/.codex}}"

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LOCK_DIR="${ROOT_DIR}/.locks/hourly-autopilot.lock"
LOG_DIR="${ROOT_DIR}/logs"
PROMPT_FILE="${ROOT_DIR}/harness/workflows/hourly-autopilot.md"
PROMPT_TMP=""

mkdir -p "${ROOT_DIR}/.locks" "${LOG_DIR}"

now_iso() {
  date '+%Y-%m-%dT%H:%M:%S%z'
}

if ! mkdir "${LOCK_DIR}" 2>/dev/null; then
  echo "$(now_iso) hourly autopilot already running; exiting."
  exit 0
fi

cleanup() {
  if [ -n "${PROMPT_TMP}" ]; then
    rm -f "${PROMPT_TMP}" 2>/dev/null || true
  fi
  rmdir "${LOCK_DIR}" 2>/dev/null || true
}
trap cleanup EXIT

cd "${ROOT_DIR}"

if ! grep -q '^ALPACA_PAPER_TRADE=true$' .env; then
  echo "$(now_iso) ALPACA_PAPER_TRADE=true is required; exiting."
  exit 64
fi

PROMPT_TMP="$(mktemp "${LOG_DIR}/hourly-autopilot-prompt.XXXXXX")"
cat >"${PROMPT_TMP}" <<'PROMPT'
You are running the stock-alpaca hourly paper autopilot.

Execute `harness/workflows/hourly-autopilot.md` exactly. The user explicitly authorized hourly current-market recommendations and automatic Alpaca paper buy/sell operation on 2026-05-26, but only within the workflow's safety rules.

Hard requirements:
- Paper trading only; abort if `ALPACA_PAPER_TRADE=true` is not present.
- Use Alpaca MCP for all account, market, position, and order operations.
- Do not call Alpaca trading REST endpoints directly.
- Submit paper orders only if the market is open and universe, MCP, quote, spread, and risk gates all pass.
- If any gate fails, submit nothing and still write the report, manifest, order plan, and log entry.
- Classify every MCP gap as one of: timeout, cancelled, dns, auth, empty_response, provider_error, wrapper_error, unknown.
- For Alpaca core, make short independent attempts for clock, account, orders, positions, and quotes. Record which exact core check was the first blocking gate.
- For SEC EDGAR, use the local `harness/sec-ticker-cik-map.json` mapping as a ticker-to-CIK fallback before marking a ticker lookup gap.
- Record detailed buy/sell rationale for every proposed or submitted order so analyst reviews can improve policy later.
- After any submit attempt, run post-trade reconciliation.
- Do not touch unrelated dirty files.

Start now.
PROMPT

python3 - "${ROOT_DIR}" "${PROMPT_TMP}" <<'PY'
from __future__ import annotations

import os
import subprocess
import sys


root_dir = sys.argv[1]
prompt_path = sys.argv[2]
timeout_seconds = int(os.environ.get("CODEX_AUTOPILOT_TIMEOUT_SECONDS", "2400"))
prompt = open(prompt_path, "r", encoding="utf-8").read()
scheduled_mcp_config = [
    'sandbox_permissions=["network-full-access"]',
    'mcp_servers.alpaca.tools.get_asset.approval_mode="auto"',
    'mcp_servers.alpaca.tools.get_news.approval_mode="auto"',
    'mcp_servers.alpaca.tools.get_market_movers.approval_mode="auto"',
    'mcp_servers.alpaca.tools.get_all_positions.approval_mode="auto"',
    'mcp_servers.alpaca.tools.place_stock_order.approval_mode="auto"',
]
codex_command = [
    "codex",
    "--search",
    "-a",
    "never",
    "exec",
    "--ephemeral",
    "-C",
    root_dir,
]
for item in scheduled_mcp_config:
    codex_command.extend(["-c", item])
codex_command.append("-")

try:
    completed = subprocess.run(
        codex_command,
        input=prompt,
        text=True,
        timeout=timeout_seconds,
        check=False,
    )
except subprocess.TimeoutExpired:
    print(
        f"hourly autopilot timed out after {timeout_seconds}s; lock will be released.",
        file=sys.stderr,
    )
    raise SystemExit(124)

raise SystemExit(completed.returncode)
PY

"${ROOT_DIR}/scripts/git-autopush-artifacts.sh" "hourly-autopilot"
