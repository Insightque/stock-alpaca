# 2026-05-28 15:51 KST after-hours autopilot

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Session: `after_hours`
- Artifact tag: `after-hours`
- Review bucket: `after_hours_validation`
- Mode: submit-capable workflow, no submit due to gate failure

## Gate Summary

- Paper mode: PASS (`ALPACA_PAPER_TRADE=true`)
- Alpaca regular market clock: PASS for after-hours workflow. Regular market was closed at `2026-05-28T02:52:32.026145834-04:00`; scheduler preflight `first_blocking_gate=market_closed` was treated as expected non-blocking.
- Alpaca core evidence: PASS. Scheduler preflight and fresh MCP checks covered account, positions, open orders, recent fills, quote, and spread evidence.
- Universe strict gate: PASS. Broad metadata universe coverage was 62 symbols with `SPY` and `QQQ`; shortlist used scheduler Alpaca/research preflight symbols.
- MCP strict gate: PASS. SEC EDGAR, FRED, Firecrawl, and Yahoo Finance passed; Alpha Vantage returned an `empty_response` gap and did not block because minimum confirmations were met.
- Quote/spread gate: PASS for observed after-hours candidates in the scheduler-owned Alpaca core preflight.
- Separate after-hours budget: FAIL. `risk_inputs.after_hours_new_orders_submitted_today=2`, matching `after_hours_policy.max_new_orders_per_session=2`.
- Risk gate: PASS for the empty no-submit plan with `orders is empty` warning.

## Decision

No paper order was submitted. No `place_stock_order` call was made, so no reconcile or cancel step was required.

Skipped candidates:

- `QQQ`: whole-share notional exceeds after-hours per-order validation cap.
- `NOK`: same after-hours session already has a NOK validation fill and after-hours session budget is exhausted.
- `INTC`: same after-hours session already has an INTC validation fill and after-hours session budget is exhausted.

## Artifacts

- Order plan: `wiki/trade-ledger/orders/2026-05-28-1551-after-hours-autopilot.json`
- Run manifest: `wiki/evidence-store/run-manifests/2026-05-28-1551-after-hours-autopilot.json`
- Alpaca preflight: `wiki/evidence-store/sources/2026-05-28-1551-after-hours-autopilot-alpaca-core-preflight.json`
- Research preflight: `wiki/evidence-store/sources/2026-05-28-1551-after-hours-autopilot-research-mcp-preflight.json`

## Validation

- `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-05-28-1551-after-hours-autopilot.json`: PASS, warning `orders is empty`
- `PATH=/usr/local/bin:$PATH python3 scripts/check-universe-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-05-28-1551-after-hours-autopilot.json`: PASS
- `PATH=/usr/local/bin:$PATH python3 scripts/check-mcp-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-05-28-1551-after-hours-autopilot.json`: PASS
