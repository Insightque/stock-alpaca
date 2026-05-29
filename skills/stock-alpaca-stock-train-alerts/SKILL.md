---
name: stock-alpaca-stock-train-alerts
description: Maintain and diagnose stock-alpaca [STOCK-TRAIN] messenger notifications. Use for OpenClaw/Telegram output, duplicate start/result messages, Alerts causes, portfolio summary fields, buy/sell rationale formatting, or send-openclaw-autopilot-update.py work.
---

# Stock Alpaca Stock Train Alerts

Use this skill for messenger notifications and alert diagnosis.

## Boundary

This skill owns notification rendering and alert explanation. It does not control scheduler cadence, order submission, or provider retry policy; hand off those questions to the runtime, safety, or MCP gate skills.

## Message Contract

- Start every message with `[STOCK-TRAIN]`.
- Send only one notification per scheduled wakeup: final `skipped`, `failed`, or `completed`.
- Keep the message concise and within 20 lines.
- Include execution time, portfolio status, top holdings/exposure when available, buy count/reasons, sell count/reasons, summary, alerts, and next action.
- If there are no buys or sells, include the reason.
- If data collection failed, include the failure in `Alerts`.

## Data Sources

Prefer the latest run artifacts in this order:

1. Run manifest under `wiki/evidence-store/run-manifests/`.
2. Order plan under `wiki/trade-ledger/orders/`.
3. Alpaca core preflight source artifact.
4. Research MCP preflight source artifact.
5. Workflow report.

Use Alpaca core preflight account payload as a fallback for day P/L fields when the order plan lacks `last_equity`.

## Alert Diagnosis

- Distinguish true data absence from a parser fallback bug.
- Report provider gaps by provider and category.
- Avoid showing raw provider payloads or secrets.
- Keep old manifest gaps distinct from future-run behavior after a code fix.

## Verification

Run:

```bash
PATH=/usr/local/bin:$PATH python3 -m unittest tests.test_autopilot_notification_schema tests.test_mcp_runtime_wrappers
```
