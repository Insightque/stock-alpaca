# Optional Scheduler

Manual Codex execution is the primary workflow. The scheduler is optional and disabled by default.

The example launchd plist runs `scripts/run-daily-codex.sh`, which asks Codex to execute `harness/workflows/daily.md`. It does not bypass the harness safety rules: orders still must go through Alpaca MCP and pass the risk gate.

To install on macOS, adjust the time in `com.insightque.stock-alpaca.daily.plist.example`, copy it to `~/Library/LaunchAgents/com.insightque.stock-alpaca.daily.plist`, then load it with `launchctl`.

The sample time is local machine time. Adjust it for US market hours and daylight saving time.

## Hourly paper autopilot

`com.insightque.stock-alpaca.hourly-autopilot.plist.example` runs `scripts/run-hourly-autopilot-codex.sh` at minute 31 of every hour. The script asks Codex to execute `harness/workflows/hourly-autopilot.md`.

The wrapper runs Codex in non-interactive mode with scheduled-run MCP overrides: read-only Alpaca tools and the paper-order submission tool use `approval_mode="auto"` only for this scheduled process, and network access is enabled for research MCPs such as FRED and Firecrawl. The global Codex config can remain conservative for manual sessions.

This is allowed to submit Alpaca paper orders only when every gate passes:

- `ALPACA_PAPER_TRADE=true`
- market open
- fresh quote/spread
- broad universe coverage strict gate
- all-MCP coverage strict gate
- risk policy gate
- whole-share day limit stock/ETF order shape

If any gate fails, the hourly run must submit nothing and still write a report, manifest, order plan, and log entry.
After a successful hourly run, `scripts/git-autopush-artifacts.sh hourly-autopilot` commits and pushes only the scheduled-run artifact paths such as `wiki/`, `wiki/log.md`, and recommendation policy files. It leaves unrelated local files unstaged.

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
The wrapper uses the same non-interactive read-only MCP approval overrides as the hourly runner, but it does not auto-approve any order submission tool.
After a successful analyst review run, `scripts/git-autopush-artifacts.sh analyst-review` commits and pushes only generated review/policy artifacts. It does not stage unrelated local workspace edits.

Install:

```bash
mkdir -p ~/Library/LaunchAgents
cp scheduler/com.insightque.stock-alpaca.analyst-review.plist.example \
  ~/Library/LaunchAgents/com.insightque.stock-alpaca.analyst-review.plist
launchctl bootstrap "gui/$(id -u)" \
  ~/Library/LaunchAgents/com.insightque.stock-alpaca.analyst-review.plist
launchctl enable "gui/$(id -u)/com.insightque.stock-alpaca.analyst-review"
```
