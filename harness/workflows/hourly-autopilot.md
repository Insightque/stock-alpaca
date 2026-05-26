# Workflow: Hourly Paper Autopilot

Use this only when the user explicitly asks for automatic hourly stock recommendations and Alpaca paper buy/sell operation.

## Goal

Run an hourly current-market recommendation loop. If and only if every safety, universe, core MCP, quote, spread, and risk gate passes while the US equity market is open, submit Alpaca paper day limit stock/ETF orders through Alpaca MCP. Record detailed decision evidence for later analyst-style reviews and policy improvement.

## Authorization

- This workflow is authorized for Alpaca paper trading automation by the user request on 2026-05-26.
- Paper trading only. Abort if `ALPACA_PAPER_TRADE` is missing or not exactly `true`.
- Never place live, crypto, options, short, margin-expansion, market, fractional, or custom REST orders.
- Never bypass `scripts/check-risk-policy.py`, `scripts/check-universe-coverage.py --strict`, or `scripts/check-mcp-coverage.py --strict`.
- MCP gating is tiered for paper automation:
  - Core MCP gate: Alpaca account, clock, positions, open orders, recent activities, tradability, fresh quote, and spread must pass.
  - Research MCP gate: SEC EDGAR, Alpha Vantage, FRED, Firecrawl, and Yahoo Finance must all be attempted; at least 3 must be usable/pass for actionable buy candidates.
  - A failed non-core research provider no longer blocks paper action by itself when core and minimum research confirmations pass.
- Paper validation execution is intentionally less passive than production trading, but it must not bypass hard gates:
  - During the market-open validation window, prefer one tiny paper validation order when all hard gates pass.
  - Default validation size is 1 share, with at most 2 new buy orders per run, 2% of portfolio value per validation order, and 4% of portfolio value per day.
  - Medium source confidence is allowed only when confidence score is at least 0.50, expected excess return is positive, no thesis-break is present, and tiered MCP validation passes.
  - If no order is submitted, record the first blocking gate, the next relaxation candidate, and the top recheck candidates. Do not submit a forced order.

## Required Cadence

- Scheduled runner: fixed hourly calendar schedule at minute 31.
- The 22:31 KST run is also the market-open validation run for US regular sessions.
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
6. For the pre-MCP shortlist and any proposed order symbol, query all decision MCPs:
   - Core: Alpaca
   - Research: SEC EDGAR, Alpha Vantage, FRED, Firecrawl, Yahoo Finance
   - If a required MCP fails due to timeout, cancellation, DNS, or transient network error, retry up to 2 times with a short backoff before marking it failed.
   - For DNS/network failures, run a read-only connectivity probe when practical and record whether the provider endpoint itself was reachable.
   - Never mark a failed provider as usable because of a retry. Retries only prevent false negatives from transient failures.
   - Record `mcp_gate_policy` in the run manifest with `core_servers=["alpaca"]`, the five research servers, `min_research_confirmations=3`, and `all_research_must_be_attempted=true`.
   - If fewer than 3 research MCPs are usable/pass, set `recommendation_actionability=actionable_if_provider_recovered` for otherwise strong candidates and submit nothing.
7. Create a detailed current recommendation report under `wiki/current-runs/daily/` or an hourly subreport if multiple runs happen on the same date.
8. Create a concrete order-plan JSON under `wiki/trade-ledger/orders/`.
   - Include detailed per-order `rationale`.
   - Include source refs, quote timestamp, asset check timestamp, liquidity/spread, confidence score, strategy id/version, policy status, expected excess return, expected adverse move, entry style, sizing basis, and review horizons.
   - If this run is inside the market-open validation window and all hard gates pass, prefer a 1-share validation buy for the highest-ranked actionable candidate that passes position/theme/factor/speculative caps. If the highest-ranked candidate is already held, add only when the ticker cap and cluster caps still pass.
   - Buy orders require core MCP pass, at least 3 usable/pass research MCPs, universe pass, fresh quote, spread, and risk pass.
   - Sell/trim orders require core MCP pass, fresh quote, spread, open-order check, and risk pass. Full research MCP pass is not required for risk trim.
   - Valid sell/trim rationales: thesis-break, risk-limit, stale-thesis, position-sizing, portfolio-fit, speculative cap exceeded, correlated cluster cap exceeded, theme/factor cap exceeded, or overheat profit protection.
   - Do not sell solely because a new buy candidate ranks higher.
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
    - MCP strict gate passes under the tiered policy: Alpaca core pass and at least 3 usable/pass research MCPs for buys; Alpaca core pass for risk trim sells.
    - Risk gate passes.
    - Quote age is within policy.
    - Spread is present and within policy.
    - Order plan mode is `submit`.
    - Order shape is whole-share day limit stock/ETF.
    - No same-day duplicate symbol/side conflict.
    - For validation buys, the order respects the `paper_validation_execution.validation_order_sizing` limits in `harness/recommendation-policy.yaml`.
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
14. Let the scheduled shell wrapper commit and push generated artifacts after the workflow exits successfully. Do not run ad hoc git commands inside this workflow unless explicitly requested.

## Stop Conditions

- Paper mode is not true.
- Market closed for submit action.
- Alpaca core MCP is unavailable or returns unusable data for an actionable order candidate.
- Fewer than 3 research MCPs are usable/pass for a buy candidate after retries.
- Universe strict gate fails.
- MCP strict gate fails.
- Risk gate fails.
- Quote or spread validation fails.
- Any order would violate long-only, whole-share, day-limit, stock/ETF-only constraints.
- The only way to create an order is to pass the hard gates; paper validation must increase observation frequency, not override missing Alpaca core, stale quote, spread, universe, MCP, or risk evidence.
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
