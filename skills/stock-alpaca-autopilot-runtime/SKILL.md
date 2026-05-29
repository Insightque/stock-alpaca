---
name: stock-alpaca-autopilot-runtime
description: Operate and debug stock-alpaca hourly, after-hours, and analyst-review scheduled runtimes. Use for LaunchAgent, 20-minute cadence, timeout, lock, executor, final notification timing, autopilot artifacts, scheduler logs, and runtime recovery work.
---

# Stock Alpaca Autopilot Runtime

Use this skill for scheduled automation and runtime recovery. Keep behavior aligned with `scheduler/README.md`.

## Boundary

This skill owns scheduler/wrapper lifecycle, locks, timeouts, artifacts, and final notification timing. Use `stock-alpaca-stock-train-alerts` for message content, `stock-alpaca-mcp-research-gate` for coverage decisions, and `stock-alpaca-risk-order-plan` for order-plan validation.

## Files To Read

1. `AGENTS.md`
2. `scheduler/README.md`
3. `harness/recommendation-policy.yaml`
4. The relevant workflow:
   - `harness/workflows/hourly-autopilot.md`
   - `harness/workflows/after-hours-autopilot.md`
   - `harness/workflows/analyst-review-cycle.md`
5. The relevant wrapper under `scripts/run-*-codex.sh`.

## Runtime Checks

For a scheduler issue, inspect in this order:

1. LaunchAgent state and latest wrapper logs.
2. Wrapper lock and timeout behavior.
3. Alpaca core preflight artifact.
4. Research MCP preflight artifact.
5. Latest run manifest and order plan.
6. Latest workflow report.
7. Notification artifact/result.
8. Dashboard/autopush result when applicable.

## Behavior Contracts

- Hourly autopilot exits before nested Codex when regular-market clock is closed.
- After-hours autopilot uses the separate `after_hours_policy` profile, artifact tag, order budget, and review bucket.
- Analyst review never mutates account/order/position state.
- Wrappers send one `[STOCK-TRAIN]` notification per scheduled wakeup: `skipped`, `failed`, or `completed`.
- Do not reintroduce separate start notifications.
- Preserve the 20-minute cadence and bounded timeout unless policy explicitly changes.

## Verification

After wrapper or final-notification timing changes, run at least:

```bash
PATH=/usr/local/bin:$PATH python3 -m unittest tests.test_mcp_runtime_wrappers tests.test_autopilot_notification_schema
```

For broader runtime-sensitive changes, add:

```bash
PATH=/usr/local/bin:$PATH python3 -m unittest tests.test_fetch_research_mcp_preflight tests.test_policy_source_of_truth
```
