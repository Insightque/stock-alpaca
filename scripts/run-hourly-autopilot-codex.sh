#!/usr/bin/env bash
set -euo pipefail

export PATH="/opt/homebrew/bin:/usr/local/bin:/Library/Frameworks/Python.framework/Versions/3.11/bin:${PATH}"
export CODEX_HOME="${CODEX_AUTOPILOT_CODEX_HOME:-${CODEX_SCHEDULED_CODEX_HOME:-${HOME}/.codex}}"

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LOCK_DIR="${ROOT_DIR}/.locks/hourly-autopilot.lock"
LOG_DIR="${ROOT_DIR}/logs"
PROMPT_FILE="${ROOT_DIR}/harness/workflows/hourly-autopilot.md"
PROMPT_TMP=""
RUN_ID="$(date '+%Y-%m-%d-%H%M')-hourly-autopilot"
STALE_ORDER_CLEANUP_PATH="${ROOT_DIR}/wiki/evidence-store/sources/${RUN_ID}-stale-order-cleanup.json"
ALPACA_PREFLIGHT_PATH="${ROOT_DIR}/wiki/evidence-store/sources/${RUN_ID}-alpaca-core-preflight.json"
RESEARCH_PREFLIGHT_PATH="${ROOT_DIR}/wiki/evidence-store/sources/${RUN_ID}-research-mcp-preflight.json"

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
set -a
# shellcheck disable=SC1091
source .env
set +a

set +e
MARKET_CLOCK_STATUS="$(PATH="/usr/local/bin:${PATH}" python3 "${ROOT_DIR}/scripts/check-alpaca-market-open-mcp.py" 2>&1)"
MARKET_CLOCK_EXIT=$?
set -e
if [ "${MARKET_CLOCK_EXIT}" -eq 75 ]; then
  echo "$(now_iso) Alpaca market is closed; scheduled autopilot exits before research/Codex run. ${MARKET_CLOCK_STATUS}"
  exit 0
fi
if [ "${MARKET_CLOCK_EXIT}" -ne 0 ]; then
  echo "$(now_iso) Unable to confirm Alpaca market is open through MCP; scheduled autopilot exits closed. ${MARKET_CLOCK_STATUS}"
  exit 0
fi
echo "$(now_iso) Alpaca market open confirmed. ${MARKET_CLOCK_STATUS}"

PROMPT_TMP="$(mktemp "${LOG_DIR}/hourly-autopilot-prompt.XXXXXX")"
if ! PATH="/usr/local/bin:${PATH}" python3 "${ROOT_DIR}/scripts/cancel-stale-autopilot-orders.py" \
  --run-id "${RUN_ID}" \
  --output-json "${STALE_ORDER_CLEANUP_PATH}"; then
  echo "$(now_iso) stale autopilot order cleanup failed; nested workflow will classify lifecycle gap."
fi

if ! PATH="/usr/local/bin:${PATH}" python3 "${ROOT_DIR}/scripts/fetch-alpaca-core-preflight.py" \
  --run-id "${RUN_ID}" \
  --output-json "${ALPACA_PREFLIGHT_PATH}"; then
  echo "$(now_iso) Alpaca core MCP preflight failed; nested workflow will classify the core gap."
fi

if ! PATH="/usr/local/bin:${PATH}" python3 "${ROOT_DIR}/scripts/fetch-research-mcp-preflight.py" \
  --run-id "${RUN_ID}" \
  --output-json "${RESEARCH_PREFLIGHT_PATH}" \
  --alpaca-preflight-json "${ALPACA_PREFLIGHT_PATH}" \
  --max-symbols "${CODEX_AUTOPILOT_RESEARCH_SYMBOL_LIMIT:-12}"; then
  echo "$(now_iso) research MCP preflight failed; nested workflow will classify provider gaps."
fi

cat >"${PROMPT_TMP}" <<'PROMPT'
You are running the stock-alpaca scheduled paper autopilot.

Execute `harness/workflows/hourly-autopilot.md` exactly. The user explicitly authorized scheduled current-market recommendations and automatic Alpaca paper buy/sell operation on 2026-05-26, and requested a 20-minute cadence on 2026-05-27, but only within the workflow's safety rules.

Hard requirements:
- Paper trading only; abort if `ALPACA_PAPER_TRADE=true` is not present.
- Use Alpaca MCP for all account, market, position, and order operations.
- Do not call Alpaca trading REST endpoints directly.
- Submit paper orders only if the market is open and universe, MCP, quote, spread, and risk gates all pass.
- If any gate fails, submit nothing and still write the report, manifest, order plan, and log entry.
- Classify every MCP gap as one of: timeout, cancelled, dns, auth, empty_response, provider_error, wrapper_error, unknown.
- For Alpaca core, make short independent attempts for clock, account, orders, positions, and quotes. Record which exact core check was the first blocking gate.
- For SEC EDGAR, use the local `harness/sec-ticker-cik-map.json` mapping as a ticker-to-CIK fallback before marking a ticker lookup gap. In scheduled autopilot, prefer `get_company_info` and `get_recent_filings`; do not escalate to heavier SEC financials calls unless those tools are explicitly exposed and the lighter filing evidence is insufficient.
- Use registered Codex MCP tools for Alpaca, SEC EDGAR, Alpha Vantage, FRED, Firecrawl, and Yahoo Finance. Do not run ad hoc local network helper scripts or curl from the nested shell for current-market data.
- A scheduler-owned stale order cleanup report may exist at `STALE_ORDER_CLEANUP_PATH_PLACEHOLDER`. Read it before risk validation. If it cancelled stale unfilled autopilot orders, cite it. If stale autopilot orders remain because cleanup failed, block new orders with `risk_open_order_lifecycle`.
- A scheduler-owned Alpaca core preflight may exist at `ALPACA_PREFLIGHT_PATH_PLACEHOLDER`. If it exists, read it before making any Alpaca read-only calls. Treat `mcp_coverage_hint` plus passing tool rows in this file as Alpaca MCP evidence with that file as the source_ref. This preflight is read-only MCP stdio evidence for clock, account, positions, open orders, recent fills, watchlists, asset checks, latest quotes, snapshots, and latest trades; it exists to avoid non-interactive false `cancelled` gaps in nested Codex. If the preflight hard gate is `pass` and quote rows are less than 20 minutes old at decision time, set Alpaca core coverage to `outcome=pass` and `used_in_score=true`. If any required preflight row is missing, stale, or failed, call only the missing read-only Alpaca MCP tool once through the registered Codex MCP tool; if it is still cancelled, classify the exact row and submit nothing.
- A scheduler-owned research MCP preflight may exist at `RESEARCH_PREFLIGHT_PATH_PLACEHOLDER`. If it exists, read it before any research MCP calls. It is the authoritative scheduled evidence for SEC EDGAR, Alpha Vantage, FRED, Firecrawl, and Yahoo Finance for the symbols listed in its `symbols` field. Use its `mcp_coverage_hint` rows directly when present; otherwise use any provider row with `outcome=pass|usable|ok` as MCP evidence with that file as the source_ref. In particular, count passing SEC lightweight filings, Yahoo recommendations/news, and FRED macro rows as usable research confirmations. If a provider row has `outcome=gap|failed|unavailable`, classify that provider gap from the preflight; do not retry that provider through shell/curl from nested Codex.
- For Firecrawl, use the registered `firecrawl` MCP server only. If it is unexpectedly not exposed, classify it as `gap_category=wrapper_error`; do not call `scripts/mcp-firecrawl.sh` or `curl` from shell.
- For Alpha Vantage, first use `TOOL_LIST`, then `TOOL_GET("PING")`, then `TOOL_CALL("PING", {})` as a health check. For candidate data, call `TOOL_GET` immediately before the matching `TOOL_CALL`. If any non-PING `TOOL_CALL` is cancelled once, stop Alpha retries and classify `alpha-vantage` as `gap_category=cancelled`; do not try a second Alpha function in the same run.
- If `harness/risk-policy.yaml` has `order_lifecycle.cancel_stale_unfilled_orders=true`, stale unfilled autopilot orders whose `client_order_id` starts with `hourly-` may be cancelled only through Alpaca MCP `cancel_order_by_id`; never cancel non-autopilot, partially filled, live, option, crypto, or short-related orders. If cancellation is cancelled or cannot be reconciled, submit nothing.
- When running Python validators, use `PATH=/usr/local/bin:$PATH python3 ...` if the default `python3` is missing PyYAML.
- Use `LC_ALL=C` for checksum commands that otherwise fail on unavailable `C.UTF-8` locales.
- In zsh snippets, avoid using `status` as a variable name because it is read-only.
- Record detailed buy/sell rationale for every proposed or submitted order so analyst reviews can improve policy later.
- Immediately before any `place_stock_order` call, write a concise pre-submit gate summary in plain text: paper mode, market clock timestamp, order plan path, universe/MCP/risk validator status, quote freshness, spread, order shape, duplicate/open-order check, and source refs. If `place_stock_order` returns cancelled, reconcile orders and positions with the same `client_order_id` before retrying; never retry with a different client order id.
- After any submit attempt, run post-trade reconciliation.
- Do not touch unrelated dirty files.

Start now.
PROMPT

python3 - "${PROMPT_TMP}" "${STALE_ORDER_CLEANUP_PATH}" "${ALPACA_PREFLIGHT_PATH}" "${RESEARCH_PREFLIGHT_PATH}" <<'PY'
from pathlib import Path
import sys

prompt_path = Path(sys.argv[1])
stale_order_cleanup_path = sys.argv[2]
alpaca_preflight_path = sys.argv[3]
research_preflight_path = sys.argv[4]
text = prompt_path.read_text(encoding="utf-8")
prompt_path.write_text(
    text.replace("STALE_ORDER_CLEANUP_PATH_PLACEHOLDER", stale_order_cleanup_path)
    .replace("ALPACA_PREFLIGHT_PATH_PLACEHOLDER", alpaca_preflight_path)
    .replace("RESEARCH_PREFLIGHT_PATH_PLACEHOLDER", research_preflight_path),
    encoding="utf-8",
)
PY

python3 - "${ROOT_DIR}" "${PROMPT_TMP}" <<'PY'
from __future__ import annotations

import os
import json
import subprocess
import sys


root_dir = sys.argv[1]
prompt_path = sys.argv[2]
timeout_seconds = int(os.environ.get("CODEX_AUTOPILOT_TIMEOUT_SECONDS", "900"))
prompt = open(prompt_path, "r", encoding="utf-8").read()
# In non-interactive `-a never` scheduled runs, MCP tools that would prompt
# for approval are reported as "user cancelled".  Use the Codex MCP
# `approve` mode here to pre-approve only the tools this paper workflow needs;
# the workflow and risk gates still decide whether orders are allowed.
scheduled_mcp_config = [
    'sandbox_permissions=["network-full-access"]',
    f'mcp_servers.alpaca.command={json.dumps(os.path.join(root_dir, "scripts", "alpaca-mcp.sh"))}',
    f'mcp_servers.sec-edgar.command={json.dumps(os.path.join(root_dir, "scripts", "mcp-sec-edgar.sh"))}',
    f'mcp_servers.alpha-vantage.command={json.dumps(os.path.join(root_dir, "scripts", "mcp-alpha-vantage.sh"))}',
    f'mcp_servers.fred.command={json.dumps(os.path.join(root_dir, "scripts", "mcp-fred.sh"))}',
    f'mcp_servers.firecrawl.command={json.dumps(os.path.join(root_dir, "scripts", "mcp-firecrawl.sh"))}',
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
    'mcp_servers.alpaca.tools.get_order_by_id.approval_mode="approve"',
    'mcp_servers.alpaca.tools.get_order_by_client_id.approval_mode="approve"',
    'mcp_servers.alpaca.tools.cancel_order_by_id.approval_mode="approve"',
    'mcp_servers.sec-edgar.tools.get_company_info.approval_mode="approve"',
    'mcp_servers.sec-edgar.tools.get_recent_filings.approval_mode="approve"',
    'mcp_servers.alpha-vantage.tools.TOOL_LIST.approval_mode="approve"',
    'mcp_servers.alpha-vantage.tools.TOOL_GET.approval_mode="approve"',
    'mcp_servers.alpha-vantage.tools.TOOL_CALL.approval_mode="approve"',
    'mcp_servers.fred.tools.get_macro_snapshot.approval_mode="approve"',
    'mcp_servers.fred.tools.get_series_observations.approval_mode="approve"',
    'mcp_servers.fred.tools.get_series_info.approval_mode="approve"',
    'mcp_servers.fred.tools.search_series.approval_mode="approve"',
    'mcp_servers.firecrawl.tools.firecrawl_scrape.approval_mode="approve"',
    'mcp_servers.firecrawl.tools.firecrawl_map.approval_mode="approve"',
    'mcp_servers.yahoo-finance.tools.get_stock_info.approval_mode="approve"',
    'mcp_servers.yahoo-finance.tools.get_yahoo_finance_news.approval_mode="approve"',
    'mcp_servers.yahoo-finance.tools.get_recommendations.approval_mode="approve"',
    'mcp_servers.alpaca.tools.place_stock_order.approval_mode="approve"',
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
        f"hourly autopilot timed out after {timeout_seconds}s; lock will be released.",
        file=sys.stderr,
    )
    raise SystemExit(124)

raise SystemExit(completed.returncode)
PY

PATH="/usr/local/bin:${PATH}" python3 "${ROOT_DIR}/scripts/build-agent-dashboard.py"
"${ROOT_DIR}/scripts/git-autopush-artifacts.sh" "hourly-autopilot"
