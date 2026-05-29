---
name: stock-alpaca-risk-order-plan
description: Create, inspect, and validate stock-alpaca order-plan JSON files and risk gates. Use for buy/sell plans, rebalancing, trim/exit exceptions, order budgets, session throttles, after-hours validation sizing, or check-risk-policy failures.
---

# Stock Alpaca Risk Order Plan

Use this skill whenever an order plan or risk gate is involved.

## Boundary

This skill owns order-plan shape, risk validation, and buy/sell budget interpretation. Use `stock-alpaca-paper-trading-safety` for final permission to mutate Alpaca state and `stock-alpaca-mcp-research-gate` for provider coverage gates.

## Source Of Truth

- `harness/risk-policy.yaml` owns portfolio, cash, ticker, exposure, run-order, daily-order, quote, and order-shape limits.
- `harness/recommendation-policy.yaml` owns strategy promotion, validation sizing, after-hours policy, and risk-trim policy.
- `harness/order-plan.schema.json` owns required order-plan shape.
- Do not copy numeric policy values into the skill; read the YAML/schema at runtime.

## Build Or Inspect

1. Ensure plan metadata includes schema/risk policy/recommendation policy ids, timestamps, and `source_refs`.
2. Separate buy budget, sell/trim logic, regular-session budget, and after-hours budget.
3. Do not rely on same-run sell proceeds to fund buys.
4. Include skipped orders and reasons when a candidate fails.
5. Preserve whole-share day limit stock/ETF order shape.

## Validation

Run:

```bash
python3 scripts/check-risk-policy.py --json <order-plan>
```

For actionable current recommendation runs, also run:

```bash
python3 scripts/check-universe-coverage.py --strict <run-manifest>
python3 scripts/check-mcp-coverage.py --strict <run-manifest>
```

If validation fails, do not submit. Record the failed gate and correction path.

## Sell And Trim Review

For sell/trim changes, check that sell evaluation is not accidentally blocked by buy-only gates, entry windows, daily buy budgets, cash limits, or provider gaps that policy says should not block core risk trims.
