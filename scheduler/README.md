# Optional Scheduler

Manual Codex execution is the primary workflow. The scheduler is optional and disabled by default.

The example launchd plist runs `scripts/run-daily-codex.sh`, which asks Codex to execute `harness/workflows/daily.md`. It does not bypass the harness safety rules: orders still must go through Alpaca MCP and pass the risk gate.

To install on macOS, adjust the time in `com.insightque.stock-alpaca.daily.plist.example`, copy it to `~/Library/LaunchAgents/com.insightque.stock-alpaca.daily.plist`, then load it with `launchctl`.

The sample time is local machine time. Adjust it for US market hours and daylight saving time.

## Hourly paper autopilot

`com.insightque.stock-alpaca.hourly-autopilot.plist.example` runs `scripts/run-hourly-autopilot-codex.sh` every hour. The script asks Codex to execute `harness/workflows/hourly-autopilot.md`.

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

## Market-open paper validation pulse

`com.insightque.stock-alpaca.market-open-autopilot.plist.example` runs `scripts/run-market-open-autopilot-codex.sh` once near the US regular open. This supplements the hourly interval job so a run that happens shortly before 22:30 KST does not defer the first market-open decision until the next hourly interval.

The pulse uses the same hard gates as the hourly autopilot. It may prefer a tiny validation order only when all hard gates pass:

- Alpaca paper mode
- market open
- Alpaca core account, clock, position, open-order, quote, and spread checks
- broad universe coverage strict gate
- tiered MCP strict gate
- risk policy gate
- whole-share day limit stock/ETF order shape

Install:

```bash
mkdir -p ~/Library/LaunchAgents
cp scheduler/com.insightque.stock-alpaca.market-open-autopilot.plist.example \
  ~/Library/LaunchAgents/com.insightque.stock-alpaca.market-open-autopilot.plist
launchctl bootstrap "gui/$(id -u)" \
  ~/Library/LaunchAgents/com.insightque.stock-alpaca.market-open-autopilot.plist
launchctl enable "gui/$(id -u)/com.insightque.stock-alpaca.market-open-autopilot"
```
