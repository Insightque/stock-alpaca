# Workflow: Hourly Paper Autopilot

Use this when the user explicitly asks for scheduled stock recommendations and Alpaca paper buy/sell operation. The legacy workflow name remains `hourly-autopilot`, but the scheduled cadence is every 20 minutes.

## Goal

Run a 20-minute current-market recommendation loop. If and only if every safety, universe, core MCP, quote, spread, and risk gate passes while the US equity market is open, submit Alpaca paper day limit stock/ETF orders through Alpaca MCP. Record detailed decision evidence for later analyst-style reviews and policy improvement.

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
  - During regular market hours, prefer active paper validation orders when all hard gates pass.
  - Default validation size is 1 share, with at most 3 new buy orders per run, 2% of portfolio value per validation order, and 6% of portfolio value per day.
  - Use additional buy slots only for different correlated clusters, or for a clearly higher-confidence candidate that still passes ticker, theme, factor, speculative, cash, turnover, duplicate-order, and spread gates.
  - Medium source confidence is allowed only when confidence score is at least 0.50, expected excess return is positive, no thesis-break is present, and tiered MCP validation passes.
  - If no order is submitted, record the first blocking gate, the next relaxation candidate, and the top recheck candidates. Do not submit a forced order.

## Required Cadence

- Scheduled runner: fixed 20-minute calendar schedule at minutes 11, 31, and 51.
- The shell wrapper must confirm Alpaca MCP `get_clock.is_open=true` before research preflight or nested Codex execution. If the market is closed, exit with no report/manifest/order plan for that skipped wakeup.
- The 22:31 KST run is also the market-open validation run for US regular sessions.
- Recommendation cadence: every scheduled 20-minute run.
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
- `harness/sec-ticker-cik-map.json`
- Recent `wiki/log.md`, daily reports, order plans, positions, ticker notes, and reviews.

## Procedure

1. Acquire the automation lock if the shell wrapper has not already done so. If another run is active, exit without side effects.
2. Confirm `.env` has `ALPACA_PAPER_TRADE=true`.
3. In the shell wrapper, call Alpaca MCP `get_clock` through `scripts/check-alpaca-market-open-mcp.py`. If the market is closed or cannot be confirmed open, exit before research MCP preflight, nested Codex, order planning, or wiki mutation.
4. Use Alpaca MCP to check market clock, account, cash, positions, open orders, recent activities, current quotes, snapshots, and relevant news.
5. Build a broad universe from `harness/symbol-metadata.yaml`, current holdings, Alpaca watchlists, and benchmarks `SPY` and `QQQ`.
6. Run the expanded-universe first-pass screen. Record `universe_coverage` in the run manifest.
7. For the pre-MCP shortlist and any proposed order symbol, query all decision MCPs:
   - Core: Alpaca
   - Research: SEC EDGAR, Alpha Vantage, FRED, Firecrawl, Yahoo Finance
   - For Alpaca core, call and record clock, account, positions, open orders, recent activities, and per-candidate quotes/spreads as separate checks. If the core gate fails, record the first failed check in `first_blocking_gate`.
   - For SEC EDGAR, resolve ticker to CIK with `harness/sec-ticker-cik-map.json` before marking a ticker lookup failure. If a ticker is absent from the cache, record `gap_category=empty_response` for lookup gaps rather than conflating it with provider failure.
   - If a required MCP fails due to timeout, cancellation, DNS, or transient network error, retry up to 2 times with a short backoff before marking it failed.
   - For DNS/network failures, run a read-only connectivity probe when practical and record whether the provider endpoint itself was reachable.
   - Classify failed/gap coverage rows with `gap_category`: `timeout`, `cancelled`, `dns`, `auth`, `empty_response`, `provider_error`, `wrapper_error`, `not_applicable`, or `unknown`.
   - Never mark a failed provider as usable because of a retry. Retries only prevent false negatives from transient failures.
   - Record `mcp_gate_policy` in the run manifest with `core_servers=["alpaca"]`, the five research servers, `min_research_confirmations=3`, and `all_research_must_be_attempted=true`.
   - If fewer than 3 research MCPs are usable/pass, set `recommendation_actionability=actionable_if_provider_recovered` for otherwise strong candidates and submit nothing.
8. Create a detailed current recommendation report under `wiki/current-runs/daily/` or a scheduled-run subreport if multiple runs happen on the same date.
9. Create a concrete order-plan JSON under `wiki/trade-ledger/orders/`.
   - Include detailed per-order `rationale`.
   - Include source refs, quote timestamp, asset check timestamp, liquidity/spread, confidence score, strategy id/version, policy status, expected excess return, expected adverse move, entry style, sizing basis, and review horizons.
   - If all hard gates pass during regular market hours, prefer validation buys for the highest-ranked actionable candidates that pass position/theme/factor/speculative caps.
   - Use up to `paper_validation_execution.validation_order_sizing.max_new_buy_orders_per_run` buy slots. The second and third slots should normally be different correlated clusters and must satisfy the cash-ratio floors in `harness/recommendation-policy.yaml`.
   - If the highest-ranked candidate is already held, add only when the ticker cap and cluster caps still pass.
   - Buy orders require core MCP pass, at least 3 usable/pass research MCPs, universe pass, fresh quote, spread, and risk pass.
   - Sell/trim orders require core MCP pass, fresh quote, spread, open-order check, and risk pass. Full research MCP pass is not required for risk trim.
   - Valid sell/trim rationales: thesis-break, risk-limit, stale-thesis, position-sizing, portfolio-fit, speculative cap exceeded, correlated cluster cap exceeded, theme/factor cap exceeded, or overheat profit protection.
   - Evaluate active trim triggers every run using `risk_trim_policy.active_trim_triggers`: position overweight, theme/factor/cluster cap warning, overheat reversal, stale thesis underperformance, and speculative loss control should produce a trim candidate when quote/spread/open-order/risk gates pass.
   - Do not sell solely because a new buy candidate ranks higher.
10. Validate:

```bash
python3 scripts/check-universe-coverage.py --strict wiki/evidence-store/run-manifests/YOUR-RUN.json
python3 scripts/check-mcp-coverage.py --strict wiki/evidence-store/run-manifests/YOUR-RUN.json
python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/YOUR-RUN.json
```

11. Submit paper orders only when all of the following are true:
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
12. Submit only through Alpaca MCP order tools. Do not call Alpaca trading REST endpoints directly.
13. Run post-trade reconciliation immediately after any submit attempt.
14. Append `wiki/log.md` with:
    - run id
    - market clock
    - recommendation shortlist
    - submitted/skipped orders
    - validation status
    - manifest path
    - order-plan path
    - report path
    - review due markers
15. Let the scheduled shell wrapper commit and push generated artifacts after the workflow exits successfully. Do not run ad hoc git commands inside this workflow unless explicitly requested.

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
