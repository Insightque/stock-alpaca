#!/usr/bin/env bash
set -euo pipefail

export HOME="${HOME:-/Users/insightque}"
export LANG="${LANG:-en_US.UTF-8}"
export LC_ALL="${LC_ALL:-en_US.UTF-8}"
export PATH="/opt/homebrew/bin:/usr/local/bin:/Library/Frameworks/Python.framework/Versions/3.11/bin:${PATH}"
export CODEX_HOME="${CODEX_AFTER_HOURS_CODEX_HOME:-${CODEX_SCHEDULED_CODEX_HOME:-${HOME}/.codex}}"
export HTTPS_PROXY="${HTTPS_PROXY:-${https_proxy:-}}"
export HTTP_PROXY="${HTTP_PROXY:-${http_proxy:-}}"
export NO_PROXY="${NO_PROXY:-${no_proxy:-127.0.0.1,localhost}}"
if [ -z "${SSL_CERT_FILE:-}" ]; then
  SSL_CERT_CANDIDATE="$(python3 -c 'import certifi; print(certifi.where())' 2>/dev/null || true)"
  if [ -n "${SSL_CERT_CANDIDATE}" ]; then
    export SSL_CERT_FILE="${SSL_CERT_CANDIDATE}"
  fi
fi
if [ -n "${SSL_CERT_FILE:-}" ]; then
  export REQUESTS_CA_BUNDLE="${REQUESTS_CA_BUNDLE:-${SSL_CERT_FILE}}"
fi

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RUN_LABEL="after-hours-autopilot"
LOCK_DIR="${ROOT_DIR}/.locks/${RUN_LABEL}.lock"
LOG_DIR="${ROOT_DIR}/logs"
PROMPT_TMP=""
RUN_ID="$(date '+%Y-%m-%d-%H%M')-${RUN_LABEL}"
ALPACA_PREFLIGHT_PATH="${ROOT_DIR}/wiki/evidence-store/sources/${RUN_ID}-alpaca-core-preflight.json"
RESEARCH_PREFLIGHT_PATH="${ROOT_DIR}/wiki/evidence-store/sources/${RUN_ID}-research-mcp-preflight.json"
NOTIFY_SCRIPT="${ROOT_DIR}/scripts/send-openclaw-autopilot-update.py"
TERMINAL_NOTIFY_SENT=0
RESEARCH_CACHE_TTL_ARGS=()
if [ -n "${CODEX_AFTER_HOURS_RESEARCH_CACHE_TTL_SECONDS:-}" ]; then
  RESEARCH_CACHE_TTL_ARGS=(--cache-ttl-seconds "${CODEX_AFTER_HOURS_RESEARCH_CACHE_TTL_SECONDS}")
fi

mkdir -p "${ROOT_DIR}/.locks" "${LOG_DIR}"

now_iso() {
  date '+%Y-%m-%dT%H:%M:%S%z'
}

notify_autopilot() {
  local notify_status="$1"
  local notify_reason="${2:-}"
  TERMINAL_NOTIFY_SENT=1
  if [ "${CODEX_AFTER_HOURS_AUTOPILOT_NOTIFY:-1}" != "1" ]; then
    return 0
  fi
  if [ ! -x "${NOTIFY_SCRIPT}" ]; then
    return 0
  fi
  PATH="/usr/local/bin:${PATH}" python3 "${NOTIFY_SCRIPT}" \
    --run-id "${RUN_ID}" \
    --session "after_hours" \
    --status "${notify_status}" \
    --reason "${notify_reason}" || true
}

if ! mkdir "${LOCK_DIR}" 2>/dev/null; then
  echo "$(now_iso) ${RUN_LABEL} already running; exiting."
  notify_autopilot "skipped" "${RUN_LABEL} already running"
  exit 0
fi

cleanup() {
  local exit_code=$?
  if [ "${exit_code}" -ne 0 ] && [ "${TERMINAL_NOTIFY_SENT}" -eq 0 ]; then
    notify_autopilot "failed" "after-hours runner exited unexpectedly with ${exit_code}"
  fi
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
if [ "${MARKET_CLOCK_EXIT}" -eq 0 ]; then
  echo "$(now_iso) Alpaca regular market is open; after-hours autopilot exits before workflow. ${MARKET_CLOCK_STATUS}"
  notify_autopilot "skipped" "Alpaca regular market is open"
  exit 0
fi
if [ "${MARKET_CLOCK_EXIT}" -ne 75 ]; then
  echo "$(now_iso) Unable to confirm after-hours clock state through MCP; after-hours autopilot exits closed. ${MARKET_CLOCK_STATUS}"
  notify_autopilot "skipped" "unable to confirm after-hours clock state through MCP"
  exit 0
fi
echo "$(now_iso) Alpaca regular market closed confirmed; starting after-hours autopilot. ${MARKET_CLOCK_STATUS}"

if ! PATH="/usr/local/bin:${PATH}" python3 "${ROOT_DIR}/scripts/fetch-alpaca-core-preflight.py" \
  --run-id "${RUN_ID}" \
  --output-json "${ALPACA_PREFLIGHT_PATH}"; then
  echo "$(now_iso) Alpaca core MCP preflight failed; nested workflow will classify the core gap."
fi

RESEARCH_PREFLIGHT_COMMAND=(
  PATH="/usr/local/bin:${PATH}"
  python3 "${ROOT_DIR}/scripts/fetch-research-mcp-preflight.py"
  --run-id "${RUN_ID}"
  --output-json "${RESEARCH_PREFLIGHT_PATH}"
  --alpaca-preflight-json "${ALPACA_PREFLIGHT_PATH}"
  --max-symbols "${CODEX_AFTER_HOURS_RESEARCH_SYMBOL_LIMIT:-8}"
  --timeout "${CODEX_AFTER_HOURS_RESEARCH_MCP_TIMEOUT_SECONDS:-75}"
  --cache-dir "${CODEX_AFTER_HOURS_RESEARCH_CACHE_DIR:-${ROOT_DIR}/.cache/after-hours-research-mcp-preflight}"
  --circuit-breaker-seconds "${CODEX_AFTER_HOURS_RESEARCH_CIRCUIT_SECONDS:-600}"
)
if [ "${#RESEARCH_CACHE_TTL_ARGS[@]}" -gt 0 ]; then
  RESEARCH_PREFLIGHT_COMMAND+=("${RESEARCH_CACHE_TTL_ARGS[@]}")
fi
if ! env "${RESEARCH_PREFLIGHT_COMMAND[@]}"; then
  echo "$(now_iso) after-hours research MCP preflight failed; nested workflow will classify provider gaps."
fi
if [ "${CODEX_AFTER_HOURS_AUTOPILOT_RUNTIME_SMOKE_TEST:-}" = "1" ]; then
  echo "$(now_iso) after-hours autopilot runtime smoke test reached research preflight."
  notify_autopilot "completed" "runtime smoke test reached research preflight"
  exit 0
fi

PROMPT_TMP="$(mktemp "${LOG_DIR}/after-hours-autopilot-prompt.XXXXXX")"
cat >"${PROMPT_TMP}" <<'PROMPT'
You are running the stock-alpaca scheduled after-hours paper autopilot.

Execute `harness/workflows/after-hours-autopilot.md` exactly.

Hard requirements:
- Paper trading only; abort if `ALPACA_PAPER_TRADE=true` is not present.
- Use the `after_hours_policy` profile in `harness/recommendation-policy.yaml`.
- Keep `session=after_hours`, artifact tag, order budget, and review bucket separate from regular-session `hourly-autopilot`.
- Use Alpaca MCP for all account, market, position, and order operations.
- Do not call Alpaca trading REST endpoints directly.
- Submit after-hours paper orders only when the after-hours workflow hard gates, universe gate, MCP gate, quote/spread gate, and risk gate all pass.
- Do not submit if Alpaca regular market is open.
- Every after-hours order must be a whole-share day limit stock/ETF order with `extended_hours=true`.
- Every order plan must set `market.session=after_hours`; every order must set `session=after_hours` and the after-hours review bucket from `harness/recommendation-policy.yaml`.
- Include `risk_inputs.after_hours_new_orders_submitted_today`; do not reuse the regular validation order count as the after-hours session budget.
- Validate with `scripts/check-risk-policy.py --json`.
- If any gate fails, submit nothing and still write the report, manifest, order plan, and log entry with `session=after_hours`.
- Use scheduler-owned Alpaca core preflight at `ALPACA_PREFLIGHT_PATH_PLACEHOLDER` and research preflight at `RESEARCH_PREFLIGHT_PATH_PLACEHOLDER` when present.
- For after-hours runs, an Alpaca core preflight first_blocking_gate of `market_closed` is expected and is not a blocking gate by itself. Use the same preflight's passing account, positions, orders, asset, quote, and spread rows; only block on missing or failed after-hours-required rows.
- Immediately before any `place_stock_order` call, write a concise pre-submit gate summary.
- After any submit attempt, reconcile by `client_order_id`; never retry with a different client order id.
- Do not touch unrelated dirty files.

Start now.
PROMPT

python3 - "${PROMPT_TMP}" "${ALPACA_PREFLIGHT_PATH}" "${RESEARCH_PREFLIGHT_PATH}" <<'PY'
from pathlib import Path
import sys

prompt_path = Path(sys.argv[1])
alpaca_preflight_path = sys.argv[2]
research_preflight_path = sys.argv[3]
text = prompt_path.read_text(encoding="utf-8")
prompt_path.write_text(
    text.replace("ALPACA_PREFLIGHT_PATH_PLACEHOLDER", alpaca_preflight_path)
    .replace("RESEARCH_PREFLIGHT_PATH_PLACEHOLDER", research_preflight_path),
    encoding="utf-8",
)
PY

set +e
python3 - "${ROOT_DIR}" "${PROMPT_TMP}" <<'PY'
from __future__ import annotations

import json
import os
import subprocess
import sys

root_dir = sys.argv[1]
prompt_path = sys.argv[2]
timeout_seconds = int(os.environ.get("CODEX_AFTER_HOURS_TIMEOUT_SECONDS", "900"))
prompt = open(prompt_path, "r", encoding="utf-8").read()

scheduled_mcp_config = [
    'sandbox_permissions=["network-full-access"]',
    f'mcp_servers.alpaca.command={json.dumps(os.path.join(root_dir, "scripts", "alpaca-mcp.sh"))}',
    'mcp_servers.alpaca.tools.get_clock.approval_mode="approve"',
    'mcp_servers.alpaca.tools.get_account_info.approval_mode="approve"',
    'mcp_servers.alpaca.tools.get_orders.approval_mode="approve"',
    'mcp_servers.alpaca.tools.get_all_positions.approval_mode="approve"',
    'mcp_servers.alpaca.tools.get_account_activities.approval_mode="approve"',
    'mcp_servers.alpaca.tools.get_watchlists.approval_mode="approve"',
    'mcp_servers.alpaca.tools.get_asset.approval_mode="approve"',
    'mcp_servers.alpaca.tools.get_stock_latest_quote.approval_mode="approve"',
    'mcp_servers.alpaca.tools.get_stock_snapshot.approval_mode="approve"',
    'mcp_servers.alpaca.tools.get_order_by_id.approval_mode="approve"',
    'mcp_servers.alpaca.tools.get_order_by_client_id.approval_mode="approve"',
    'mcp_servers.alpaca.tools.cancel_order_by_id.approval_mode="approve"',
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
        f"after-hours autopilot timed out after {timeout_seconds}s; lock will be released.",
        file=sys.stderr,
    )
    raise SystemExit(124)

raise SystemExit(completed.returncode)
PY
CODEX_EXIT=$?
set -e
if [ "${CODEX_EXIT}" -ne 0 ]; then
  notify_autopilot "failed" "nested after-hours Codex exited ${CODEX_EXIT}"
  exit "${CODEX_EXIT}"
fi

PATH="/usr/local/bin:${PATH}" python3 "${ROOT_DIR}/scripts/build-agent-dashboard.py"
"${ROOT_DIR}/scripts/git-autopush-artifacts.sh" "after-hours-autopilot"
notify_autopilot "completed" "after-hours workflow completed"
