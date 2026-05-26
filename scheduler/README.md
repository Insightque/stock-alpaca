# Optional Scheduler

Manual Codex execution is the primary workflow. The scheduler is optional and disabled by default.

The example launchd plist runs `scripts/run-daily-codex.sh`, which asks Codex to execute `harness/workflows/daily.md`. It does not bypass the harness safety rules: orders still must go through Alpaca MCP and pass the risk gate.

To install on macOS, adjust the time in `com.insightque.stock-alpaca.daily.plist.example`, copy it to `~/Library/LaunchAgents/com.insightque.stock-alpaca.daily.plist`, then load it with `launchctl`.

The sample time is local machine time. Adjust it for US market hours and daylight saving time.

## Hourly paper autopilot

`com.insightque.stock-alpaca.hourly-autopilot.plist.example` runs `scripts/run-hourly-autopilot-codex.sh` every 20 minutes during the KST windows that can overlap US regular market hours. The wrapper first checks Alpaca MCP `get_clock`; if the US equity market is closed, it exits before research preflight, nested Codex, wiki mutation, or order planning. The script asks Codex to execute `harness/workflows/hourly-autopilot.md`; the legacy name remains `hourly-autopilot` for artifact compatibility.

The wrapper runs Codex in non-interactive mode with scheduled-run MCP overrides: required Alpaca, SEC EDGAR, Alpha Vantage, FRED, Firecrawl, Yahoo Finance tools and the paper-order submission tool use `approval_mode="approve"` only for this scheduled process. The nested run ignores the global Codex config and loads only those MCP servers; scheduler-owned stale-order cleanup cancels only stale unfilled autopilot paper orders when the risk policy allows it, scheduler-owned Alpaca core preflight captures read-only account, position, open-order, asset, and quote evidence before launch, and scheduler-owned FRED preflight captures macro context before launch so local research wrappers cannot stall nested shutdown. The global Codex config can remain conservative for manual sessions.

This is allowed to submit Alpaca paper orders only when every gate passes:

- `ALPACA_PAPER_TRADE=true`
- market open
- fresh quote/spread
- broad universe coverage strict gate
- all-MCP coverage strict gate
- risk policy gate
- whole-share day limit stock/ETF order shape

If `harness/risk-policy.yaml` has `order_lifecycle.cancel_stale_unfilled_orders=true`, the wrapper may call Alpaca MCP `cancel_order_by_id` before nested Codex starts, but only for stale unfilled day limit US-equity orders whose `client_order_id` starts with `hourly-`. It never cancels non-autopilot orders, partially filled orders, options, crypto, shorts, or live orders.

If the Alpaca clock is closed, the scheduled wakeup exits with no workflow artifacts. If the clock is open but any later gate fails, the scheduled run must submit nothing and still write a report, manifest, order plan, and log entry.
After a successful scheduled run, the wrapper regenerates `ui/agent-dashboard.html`, then `scripts/git-autopush-artifacts.sh hourly-autopilot` commits and pushes the scheduled-run artifact paths such as `wiki/`, `wiki/log.md`, generated dashboard files, and recommendation policy files. It leaves unrelated local files unstaged.

The nested Codex execution defaults to a 15-minute timeout (`CODEX_AUTOPILOT_TIMEOUT_SECONDS=900`) so a single run cannot occupy the 20-minute cadence indefinitely. The lock is released by the wrapper cleanup path on timeout.

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
