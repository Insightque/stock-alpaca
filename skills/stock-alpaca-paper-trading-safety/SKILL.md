---
name: stock-alpaca-paper-trading-safety
description: Enforce stock-alpaca paper-trading safety gates. Use before any order, submit-mode workflow, rebalance execution, autopilot order path, stale-order cancellation, after-hours probe, or code change that could mutate Alpaca account/order/position state.
---

# Stock Alpaca Paper Trading Safety

Use this skill as the hard guardrail before any state-changing trading action.

## Boundary

This skill decides whether account/order/position mutation is allowed. Use `stock-alpaca-risk-order-plan` to build and inspect order-plan details, and use `stock-alpaca-autopilot-runtime` for scheduler lifecycle issues.

## Non-Negotiables

1. Read `AGENTS.md` and confirm `ALPACA_PAPER_TRADE=true` without printing secret values.
2. Abort trading if paper mode is missing or not true.
3. Never place live orders, options orders, crypto orders, short orders, or fractional-share orders.
4. Never call Alpaca trading REST endpoints directly from scripts.
5. Submit orders only through the Alpaca MCP paper-order tool after all gates pass.
6. Never rely on same-run sell proceeds to fund buy orders.
7. Do not bypass market, asset, quote freshness, spread, universe, MCP coverage, or risk gates.

## Required Gates

Before a paper order can be submitted:

1. Confirm Alpaca core data is available: account, clock/session, positions, open orders, asset, quote/spread.
2. Confirm the asset is an active tradable US stock or ETF.
3. Confirm thesis/trend/risk evidence exists in the wiki for the ticker.
4. Create or update an order-plan JSON under `wiki/trade-ledger/orders/`.
5. Run `python3 scripts/check-risk-policy.py --json <order-plan>`.
6. For actionable recommendation or submit-mode runs, run strict universe and MCP coverage validators.
7. Submit only whole-share day limit stock/ETF orders through Alpaca MCP.
8. Immediately reconcile orders/fills/positions and update the wiki.

## Cancellation And Probes

- Stale-order cleanup may cancel only scheduler-owned stale unfilled paper orders allowed by `harness/risk-policy.yaml`.
- After-hours probes require explicit probe intent and must reconcile/cancel only the probe order by idempotent client id.
- Analyst review workflows must never submit, replace, cancel, or close orders.

## Failure Rule

If any gate is uncertain, skip submission and record the reason in the run report, manifest, and `wiki/log.md`.
