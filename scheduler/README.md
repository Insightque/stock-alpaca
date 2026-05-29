# Optional Scheduler

Manual Codex execution is the primary workflow. The scheduler is optional and disabled by default.

The example launchd plist runs `scripts/run-daily-codex.sh`, which asks Codex to execute `harness/workflows/daily.md`. It does not bypass the harness safety rules: orders still must go through Alpaca MCP and pass the risk gate.

To install on macOS, adjust the time in `com.insightque.stock-alpaca.daily.plist.example`, copy it to `~/Library/LaunchAgents/com.insightque.stock-alpaca.daily.plist`, then load it with `launchctl`.

The sample time is local machine time. Adjust it for US market hours and daylight saving time.

## Hourly paper autopilot

`com.insightque.stock-alpaca.hourly-autopilot.plist.example` runs `scripts/run-hourly-autopilot-codex.sh` on the cadence and KST windows defined in `harness/recommendation-policy.yaml`. The wrapper first checks Alpaca MCP `get_clock`; if the US equity market is closed, it exits before research preflight, nested Codex, wiki mutation, or order planning. The script asks Codex to execute `harness/workflows/hourly-autopilot.md`; the legacy name remains `hourly-autopilot` for artifact compatibility.

The wrapper runs Codex in non-interactive mode with scheduled-run MCP overrides: required Alpaca, SEC EDGAR, Alpha Vantage, FRED, Firecrawl, Yahoo Finance tools and the paper-order submission tool use `approval_mode="approve"` only for this scheduled process. The nested run ignores the global Codex config and loads only those MCP servers; scheduler-owned stale-order cleanup cancels only stale unfilled autopilot paper orders when the risk policy allows it, scheduler-owned Alpaca core preflight captures read-only account, position, open-order, asset, and quote evidence before launch, scheduler-owned Alpha Vantage preflight is throttled to one actual API call per hour, and scheduler-owned FRED preflight captures macro context before launch so local research wrappers cannot stall nested shutdown. The global Codex config can remain conservative for manual sessions.

This is allowed to submit Alpaca paper orders only when every gate passes:

- `ALPACA_PAPER_TRADE=true`
- market open
- fresh quote/spread
- broad universe coverage strict gate
- all-MCP coverage strict gate
- risk policy gate
- whole-share day limit stock/ETF order shape

If `harness/risk-policy.yaml` has `order_lifecycle.cancel_stale_unfilled_orders=true`, the wrapper may call Alpaca MCP `cancel_order_by_id` before nested Codex starts, but only for stale unfilled day limit US-equity orders whose `client_order_id` starts with `hourly-`. It never cancels non-autopilot orders, partially filled orders, options, crypto, shorts, or live orders.

The regular-session wrapper sends one OpenClaw messenger update per scheduled wakeup: skip, failure, or completion only. It does not send a separate start notification. Set `OPENCLAW_AUTOPILOT_NOTIFY_TARGET` in the installed LaunchAgent to the Telegram chat id; leave it unset to skip notifications without failing the run. Messages start with `[STOCK-TRAIN]` and keep the portfolio, top exposure, buy/sell decisions, alerts, and next action within a short messenger summary.

If the Alpaca clock is closed, the scheduled wakeup exits before workflow artifacts and sends a skip update when notifications are configured. If the clock is open but any later gate fails, the scheduled run must submit nothing and still write a report, manifest, order plan, and log entry.
After a successful scheduled run, the wrapper regenerates `ui/agent-dashboard.html`, then `scripts/git-autopush-artifacts.sh hourly-autopilot` commits and pushes the scheduled-run artifact paths such as `wiki/`, `wiki/log.md`, generated dashboard files, and recommendation policy files. It leaves unrelated local files unstaged.

The nested Codex execution defaults to a 15-minute timeout (`CODEX_AUTOPILOT_TIMEOUT_SECONDS=900`) so a single run cannot occupy the 20-minute cadence indefinitely. The lock is released by the wrapper cleanup path on timeout.

## Runtime order probes

Use `scripts/probe-alpaca-after-hours-order.py` for explicit paper runtime checks outside the scheduled trading loop. The probe uses Alpaca MCP only, requires `ALPACA_PAPER_TRADE=true`, prepares an extended-hours day limit paper buy with an idempotent `client_order_id`, reconciles it by client id, cancels it immediately, and writes JSON evidence under `wiki/evidence-store/sources/`.

Run without `--execute` for read-only clock/asset/quote validation. Add `--execute` only when the goal is to verify actual paper submit/reconcile/cancel behavior.

To verify this through the hourly autopilot wrapper rather than calling the probe directly, run `CODEX_AUTOPILOT_AFTER_HOURS_ORDER_PROBE=1 scripts/run-hourly-autopilot-codex.sh`. This explicit flag makes a closed-market scheduled wakeup run only the after-hours paper probe, then exit before research or normal order planning.

For policy-bearing after-hours automation, use `harness/workflows/after-hours-autopilot.md`. Its source of truth is `after_hours_policy` in `harness/recommendation-policy.yaml`, and its artifacts, order budget, and review bucket must stay separate from regular-session autopilot.

`com.insightque.stock-alpaca.after-hours-autopilot.plist.example` runs `scripts/run-after-hours-autopilot-codex.sh` on the cadence and KST windows defined in `harness/recommendation-policy.yaml` under `after_hours_policy.cadence`. The wrapper uses a separate run label and lock, and exits before the after-hours probe when Alpaca reports the regular market is open.

The after-hours wrapper also sends one OpenClaw messenger update per scheduled wakeup: skip, failure, or completion only. It does not send a separate start notification. Set `OPENCLAW_AUTOPILOT_NOTIFY_TARGET` in the installed LaunchAgent to the Telegram chat id; leave it unset to skip notifications without failing the run. Messages use the same `[STOCK-TRAIN]` portfolio/order/alert summary as regular-session automation.

Install:

```bash
mkdir -p ~/Library/LaunchAgents
cp scheduler/com.insightque.stock-alpaca.hourly-autopilot.plist.example \
  ~/Library/LaunchAgents/com.insightque.stock-alpaca.hourly-autopilot.plist
launchctl bootstrap "gui/$(id -u)" \
  ~/Library/LaunchAgents/com.insightque.stock-alpaca.hourly-autopilot.plist
launchctl enable "gui/$(id -u)/com.insightque.stock-alpaca.hourly-autopilot"
```

## Analyst review cycle

`com.insightque.stock-alpaca.analyst-review.plist.example` runs `scripts/run-analyst-review-codex.sh` once per day after the US market close in Korea time. The workflow performs post-trade reconciliation, checks 1D/5D/20D review horizons, writes analyst-style reviews, and updates policy only when evidence accumulates.

This workflow never submits, replaces, cancels, or closes orders.
The wrapper uses the same non-interactive read-only MCP approval overrides as the hourly runner, but it does not pre-approve any order submission tool.
After a successful analyst review run, the wrapper regenerates `ui/agent-dashboard.html`, then `scripts/git-autopush-artifacts.sh analyst-review` commits and pushes generated review/policy/dashboard artifacts. It does not stage unrelated local workspace edits.

Install:

```bash
mkdir -p ~/Library/LaunchAgents
cp scheduler/com.insightque.stock-alpaca.analyst-review.plist.example \
  ~/Library/LaunchAgents/com.insightque.stock-alpaca.analyst-review.plist
launchctl bootstrap "gui/$(id -u)" \
  ~/Library/LaunchAgents/com.insightque.stock-alpaca.analyst-review.plist
launchctl enable "gui/$(id -u)/com.insightque.stock-alpaca.analyst-review"
```
