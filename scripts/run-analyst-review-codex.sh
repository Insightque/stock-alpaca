#!/usr/bin/env bash
set -euo pipefail

export PATH="/opt/homebrew/bin:/usr/local/bin:/Library/Frameworks/Python.framework/Versions/3.11/bin:${PATH}"
export CODEX_HOME="${CODEX_ANALYST_REVIEW_CODEX_HOME:-${CODEX_SCHEDULED_CODEX_HOME:-${HOME}/.codex}}"

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LOCK_DIR="${ROOT_DIR}/.locks/analyst-review.lock"
LOG_DIR="${ROOT_DIR}/logs"

mkdir -p "${ROOT_DIR}/.locks" "${LOG_DIR}"

now_iso() {
  date '+%Y-%m-%dT%H:%M:%S%z'
}

if ! mkdir "${LOCK_DIR}" 2>/dev/null; then
  echo "$(now_iso) analyst review already running; exiting."
  exit 0
fi

cleanup() {
  rmdir "${LOCK_DIR}" 2>/dev/null || true
}
trap cleanup EXIT

cd "${ROOT_DIR}"

if ! grep -q '^ALPACA_PAPER_TRADE=true$' .env; then
  echo "$(now_iso) ALPACA_PAPER_TRADE=true is required; exiting."
  exit 64
fi

PROMPT_TMP="$(mktemp "${LOG_DIR}/analyst-review-prompt.XXXXXX")"
cleanup_prompt() {
  rm -f "${PROMPT_TMP}" 2>/dev/null || true
}
trap 'cleanup_prompt; cleanup' EXIT

cat >"${PROMPT_TMP}" <<'PROMPT'
You are running the stock-alpaca scheduled analyst review cycle.

Execute `harness/workflows/analyst-review-cycle.md` exactly.

Hard requirements:
- This workflow never submits, replaces, cancels, or closes orders.
- Use Alpaca MCP for account, order, activity, position, and market-data reconciliation.
- Review paper trades, open positions, skipped recommendations, and due 1D/5D/20D review horizons.
- Use registered Codex MCP tools for Alpaca, SEC EDGAR, Alpha Vantage, and Yahoo Finance. Do not run local Alpaca/FRED/Firecrawl network helper scripts or curl from the nested shell for current-market data.
- For Firecrawl and FRED, use registered MCP tools only if exposed in the Codex tool catalog. If they are not exposed, classify the provider as `gap_category=wrapper_error` rather than probing with shell/curl.
- For Alpha Vantage, first use `TOOL_LIST`, then `TOOL_GET("PING")`, then `TOOL_CALL("PING", {})` as a health check. For candidate data, call `TOOL_GET` immediately before the matching `TOOL_CALL`. If any non-PING `TOOL_CALL` is cancelled once, stop Alpha retries and classify `alpha-vantage` as `gap_category=cancelled`; do not try a second Alpha function in the same run.
- When running Python validators, use `PATH=/usr/local/bin:$PATH python3 ...` if the default `python3` is missing PyYAML.
- Use `LC_ALL=C` for checksum commands that otherwise fail on unavailable `C.UTF-8` locales.
- In zsh snippets, avoid using `status` as a variable name because it is read-only.
- Write detailed analyst-style review artifacts and log entries.
- Update recommendation policy only when the evidence threshold in the workflow is met.
- Do not touch unrelated dirty files.

Start now.
PROMPT

python3 - "${ROOT_DIR}" "${PROMPT_TMP}" <<'PY'
from __future__ import annotations

import os
import json
import subprocess
import sys


root_dir = sys.argv[1]
prompt_path = sys.argv[2]
timeout_seconds = int(os.environ.get("CODEX_ANALYST_REVIEW_TIMEOUT_SECONDS", "2400"))
prompt = open(prompt_path, "r", encoding="utf-8").read()
# In non-interactive `-a never` scheduled runs, MCP tools that would prompt
# for approval are reported as "user cancelled".  Analyst review is read-only,
# so pre-approve only the reconciliation/research tools it needs.
scheduled_mcp_config = [
    'sandbox_permissions=["network-full-access"]',
    f'mcp_servers.alpaca.command={json.dumps(os.path.join(root_dir, "scripts", "alpaca-mcp.sh"))}',
    f'mcp_servers.sec-edgar.command={json.dumps(os.path.join(root_dir, "scripts", "mcp-sec-edgar.sh"))}',
    f'mcp_servers.alpha-vantage.command={json.dumps(os.path.join(root_dir, "scripts", "mcp-alpha-vantage.sh"))}',
    f'mcp_servers.yahoo-finance.command={json.dumps(os.path.join(root_dir, "scripts", "mcp-yahoo-finance.sh"))}',
    'mcp_servers.alpaca.tools.get_clock.approval_mode="approve"',
    'mcp_servers.alpaca.tools.get_account_info.approval_mode="approve"',
    'mcp_servers.alpaca.tools.get_orders.approval_mode="approve"',
    'mcp_servers.alpaca.tools.get_all_positions.approval_mode="approve"',
    'mcp_servers.alpaca.tools.get_account_activities.approval_mode="approve"',
    'mcp_servers.alpaca.tools.get_watchlists.approval_mode="approve"',
    'mcp_servers.alpaca.tools.get_asset.approval_mode="approve"',
    'mcp_servers.alpaca.tools.get_stock_bars.approval_mode="approve"',
    'mcp_servers.alpaca.tools.get_stock_quotes.approval_mode="approve"',
    'mcp_servers.alpaca.tools.get_stock_latest_quote.approval_mode="approve"',
    'mcp_servers.alpaca.tools.get_stock_snapshot.approval_mode="approve"',
    'mcp_servers.alpaca.tools.get_news.approval_mode="approve"',
    'mcp_servers.alpaca.tools.get_market_movers.approval_mode="approve"',
    'mcp_servers.alpaca.tools.get_most_active_stocks.approval_mode="approve"',
    'mcp_servers.sec-edgar.tools.get_company_info.approval_mode="approve"',
    'mcp_servers.sec-edgar.tools.get_recent_filings.approval_mode="approve"',
    'mcp_servers.alpha-vantage.tools.TOOL_LIST.approval_mode="approve"',
    'mcp_servers.alpha-vantage.tools.TOOL_GET.approval_mode="approve"',
    'mcp_servers.alpha-vantage.tools.TOOL_CALL.approval_mode="approve"',
    'mcp_servers.yahoo-finance.tools.get_stock_info.approval_mode="approve"',
    'mcp_servers.yahoo-finance.tools.get_yahoo_finance_news.approval_mode="approve"',
    'mcp_servers.yahoo-finance.tools.get_recommendations.approval_mode="approve"',
]
codex_command = [
    "codex",
    "--search",
    "-a",
    "never",
    "exec",
    "--ignore-user-config",
    "--sandbox",
    "workspace-write",
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
        f"analyst review timed out after {timeout_seconds}s; lock will be released.",
        file=sys.stderr,
    )
    raise SystemExit(124)

raise SystemExit(completed.returncode)
PY

PATH="/usr/local/bin:${PATH}" python3 "${ROOT_DIR}/scripts/build-agent-dashboard.py"
"${ROOT_DIR}/scripts/git-autopush-artifacts.sh" "analyst-review"
