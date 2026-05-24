# Workflow: Rebalance Paper Portfolio

Use this when the user says `리밸런싱 계획 짜줘`, `paper 주문까지 실행해줘`, or asks to rebalance the paper portfolio.

## Goal

Use current positions, account state, ticker theses, and fresh market data to create a risk-checked rebalance plan.

Default simple-command modes:

- `리밸런싱 계획 짜줘` means no-submit mode.
- `paper 주문까지 실행해줘` means submit mode.
- In no-submit mode, create and validate the order plan, but do not submit orders.
- In submit mode, submit automatic Alpaca paper orders only if the risk gate passes and the market is open.

## Required Outputs

- Updated `wiki/portfolio/current.md`
- Rebalance order plan JSON in `wiki/portfolio/order-plans/YYYY-MM-DD-rebalance.json`
- A rebalance note in `wiki/analyses/`
- Updated ticker pages for affected symbols
- Updated `wiki/index.md`
- Appended `wiki/log.md` entry

## Procedure

1. Read `AGENTS.md`, `harness/risk-policy.yaml`, `harness/risk-policy.md`, `wiki/policies/recommendation-policy.md`, `wiki/index.md`, and current ticker pages.
2. Use Alpaca MCP to get account, clock, open orders, positions, and portfolio history if available.
3. Refresh market snapshots and quotes for held tickers and candidate watchlist tickers.
4. Re-score held and candidate tickers with the daily scoring model and the current recommendation policy lessons.
5. Propose target allocations:
   - Cash reserve at least 20%.
   - Invested exposure at most 80%.
   - Ticker exposure at most 20%.
   - Sells must not create short positions.
6. Create `wiki/portfolio/order-plans/YYYY-MM-DD-rebalance.json` with schema/provenance fields and per-order `quote_captured_at`, `asset_checked_at`, and `source_refs`.
7. Run `python3 scripts/check-risk-policy.py --json wiki/portfolio/order-plans/YYYY-MM-DD-rebalance.json`.
8. If the run is no-submit mode, submit nothing and record the plan as proposed.
9. If the run is submit mode, validation passes, market is open, and quotes are fresh, submit paper day limit orders through Alpaca MCP only.
10. Verify orders and update `wiki/portfolio/current.md`.
11. Create/update a run manifest in `wiki/runs/`, then update index and log.

## Stop Conditions

Stop before order submission if risk validation fails, market is closed, quote data is stale, paper mode is not true, or MCP is unavailable.
