# Optional Daily Scheduler

Manual Codex execution is the primary workflow. The scheduler is optional and disabled by default.

The example launchd plist runs `scripts/run-daily-codex.sh`, which asks Codex to execute `harness/workflows/daily.md`. It does not bypass the harness safety rules: orders still must go through Alpaca MCP and pass the risk gate.

To install on macOS, adjust the time in `com.insightque.stock-alpaca.daily.plist.example`, copy it to `~/Library/LaunchAgents/com.insightque.stock-alpaca.daily.plist`, then load it with `launchctl`.

The sample time is local machine time. Adjust it for US market hours and daylight saving time.

