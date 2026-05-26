# Workflow: Hourly Paper Autopilot

Use this only when the user explicitly asks for automatic hourly stock recommendations and Alpaca paper buy/sell operation.

## Goal

Run an hourly current-market recommendation loop. If and only if every safety, universe, MCP, quote, and risk gate passes while the US equity market is open, submit Alpaca paper day limit stock/ETF orders through Alpaca MCP. Record detailed decision evidence for later analyst-style reviews and policy improvement.

## Authorization

- This workflow is authorized for Alpaca paper trading automation by the user request on 2026-05-26.
- Paper trading only. Abort if `ALPACA_PAPER_TRADE` is missing or not exactly `true`.
- Never place live, crypto, options, short, margin-expansion, market, fractional, or custom REST orders.
- Never bypass `scripts/check-risk-policy.py`, `scripts/check-universe-coverage.py --strict`, or `scripts/check-mcp-coverage.py --strict`.

## Required Cadence

- Scheduled runner: hourly.
- Recommendation cadence: every hourly run.
- Submit cadence: only during regular US equity market hours, after fresh quote validation.
- Post-trade reconciliation: every run after any submit attempt, and on any run with open orders or same-day fills.
- Analyst review cadence:
  - New fills: mark `회고 대기` immediately.
  - Interim review: after 1 full trading day or if thesis break/catalyst/risk event occurs.
  - Follow-up review: after 5 full trading days.
  - Full policy review: after 20 full trading days or when a position is closed.
  - Portfolio-level review: weekly after Friday close, or next available session.

## Required Inputs

- `AGENTS.md`
- `harness/workflows/daily.md`
- `harness/workflows/post-trade.md`
- `harness/workflows/trade-review.md`
- `harness/mcp-source-map.md`
- `harness/risk-policy.yaml`
- `harness/recommendation-policy.yaml`
- `harness/symbol-metadata.yaml`
- Recent `wiki/log.md`, daily reports, order plans, positions, ticker notes, and reviews.

## Procedure

1. Acquire the automation lock if the shell wrapper has not already done so. If another run is active, exit without side effects.
2. Confirm `.env` has `ALPACA_PAPER_TRADE=true`.
3. Use Alpaca MCP to check market clock, account, cash, positions, open orders, recent activities, current quotes, snapshots, and relevant news.
4. Build a broad universe from `harness/symbol-metadata.yaml`, current holdings, Alpaca watchlists, and benchmarks `SPY` and `QQQ`.
5. Run the expanded-universe first-pass screen. Record `universe_coverage` in the run manifest.
6. For the pre-MCP shortlist and any proposed order symbol, query all required decision MCPs:
   - Alpaca
   - SEC EDGAR
   - Alpha Vantage
   - FRED
   - Firecrawl
   - Yahoo Finance
7. Create a detailed current recommendation report under `wiki/current-runs/daily/` or an hourly subreport if multiple runs happen on the same date.
8. Create a concrete order-plan JSON under `wiki/trade-ledger/orders/`.
   - Include detailed per-order `rationale`.
   - Include source refs, quote timestamp, asset check timestamp, liquidity/spread, confidence score, strategy id/version, policy status, expected excess return, expected adverse move, entry style, sizing basis, and review horizons.
   - Sell/trim orders require a thesis-break, risk-limit, stale-thesis, position-sizing, or portfolio-fit rationale. Do not sell solely because a new buy candidate ranks higher.
9. Validate:

```bash
python3 scripts/check-universe-coverage.py --strict wiki/evidence-store/run-manifests/YOUR-RUN.json
python3 scripts/check-mcp-coverage.py --strict wiki/evidence-store/run-manifests/YOUR-RUN.json
python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/YOUR-RUN.json
```

10. Submit paper orders only when all of the following are true:
    - Market is open.
    - `ALPACA_PAPER_TRADE=true`.
    - Universe strict gate passes.
    - MCP strict gate passes.
    - Risk gate passes.
    - Quote age is within policy.
    - Spread is present and within policy.
    - Order plan mode is `submit`.
    - Order shape is whole-share day limit stock/ETF.
    - No same-day duplicate symbol/side conflict.
11. Submit only through Alpaca MCP order tools. Do not call Alpaca trading REST endpoints directly.
12. Run post-trade reconciliation immediately after any submit attempt.
13. Append `wiki/log.md` with:
    - run id
    - market clock
    - recommendation shortlist
    - submitted/skipped orders
    - validation status
    - manifest path
    - order-plan path
    - report path
    - review due markers

## Stop Conditions

- Paper mode is not true.
- Market closed for submit action.
- Any required MCP is unavailable or returns unusable data for an actionable order candidate.
- Universe strict gate fails.
- MCP strict gate fails.
- Risk gate fails.
- Quote or spread validation fails.
- Any order would violate long-only, whole-share, day-limit, stock/ETF-only constraints.
- Codex cannot write a complete report, manifest, and order plan.

## Output Contract

Every run must produce or update:

- A report with Korean explanation and `## 지표 설명`.
- A run manifest with `universe_coverage` and `mcp_coverage`.
- An order plan, even if `orders: []`.
- A log entry.

If orders are submitted, also produce or update:

- `wiki/trade-ledger/positions/current.md`
- submitted/skipped order tables in the report
- trade-review due markers
