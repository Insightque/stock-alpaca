# Workflow: Hourly Paper Autopilot

Use this when the user explicitly asks for scheduled stock recommendations and Alpaca paper buy/sell operation. The legacy workflow name remains `hourly-autopilot`, but the scheduled cadence is defined in `harness/recommendation-policy.yaml`.

## Goal

Run the current-market recommendation loop on the cadence defined in `harness/recommendation-policy.yaml`. If and only if every safety, universe, core MCP, quote, spread, and risk gate passes while the US equity market is open, submit Alpaca paper day limit stock/ETF orders through Alpaca MCP. Record detailed decision evidence for later analyst-style reviews and policy improvement.

This workflow is regular-session only. After-hours automation must use `harness/workflows/after-hours-autopilot.md` and the `after_hours_policy` profile in `harness/recommendation-policy.yaml`; do not mix after-hours order budgets, artifact tags, or review buckets into this workflow.

## Authorization

- This workflow is authorized for Alpaca paper trading automation by the user request on 2026-05-26.
- Paper trading only. Abort if `ALPACA_PAPER_TRADE` is missing or not exactly `true`.
- Never place live, crypto, options, short, margin-expansion, market, fractional, or custom REST orders.
- Never bypass `scripts/check-risk-policy.py`, `scripts/check-universe-coverage.py --strict`, or `scripts/check-mcp-coverage.py --strict`.
- MCP gating is tiered for paper automation:
  - Core MCP gate: Alpaca account, clock, positions, open orders, recent activities, tradability, fresh quote, and spread must pass.
  - Research MCP gate: use the research MCP list and confirmation threshold from `harness/recommendation-policy.yaml`.
  - A failed non-core research provider no longer blocks paper action by itself when core and minimum research confirmations pass.
- Paper validation execution is intentionally less passive than production trading, but it must not bypass hard gates:
  - During regular market hours, prefer active paper validation orders when all hard gates pass.
  - Default exploratory validation size and confidence/notional sizing tiers come from `harness/recommendation-policy.yaml`; subject all quantities to whole-share rounding and `harness/risk-policy.yaml` caps.
  - Use `paper_validation_execution.validation_order_sizing.max_new_buy_orders_per_run` for normal per-run buy slots and the validation notional caps in `harness/recommendation-policy.yaml`; do not hardcode those values in this workflow.
  - Treat the invested-ratio path in `paper_validation_execution.validation_order_sizing.target_exposure_path` as a staged policy target, not a one-shot order target: below the acceleration threshold, allow normal acceleration; between selective and max target thresholds, require stronger candidate quality and diversification benefit; above the rebalance threshold, prefer trim/rebalance and only add high-conviction candidates.
  - Use additional buy slots only for different correlated clusters, or for a clearly higher-confidence candidate that still passes ticker, theme, factor, speculative, cash, turnover, duplicate-order, and spread gates.
  - Fresh open orders block new buys for the same symbol/side and normally for the same correlated cluster, but they do not automatically block different-cluster candidates when the open-order lifecycle gate passes.
  - Medium source confidence handling follows `harness/recommendation-policy.yaml`; candidates still need positive expected excess return, no thesis-break, and tiered MCP validation.
  - Evaluate risk-reducing sell/trim candidates before new buys on every run. The buy entry window and validation-buy budget gate new buy exposure only; they must not suppress sell/trim diagnostics or order-plan entries that pass the sell gates.
  - If no order is submitted, record the first blocking gate, the next relaxation candidate, and the top recheck candidates. Do not submit a forced order.

## Required Cadence

- Scheduled runner cadence and launch minutes come from `harness/recommendation-policy.yaml`.
- The shell wrapper must confirm Alpaca MCP `get_clock.is_open=true` before research preflight or nested Codex execution. If the market is closed, exit with no report/manifest/order plan for that skipped wakeup.
- The market-open validation run comes from `harness/recommendation-policy.yaml`.
- Recommendation cadence follows the scheduled runner cadence.
- Submit cadence: only during regular US equity market hours, after fresh quote validation.
- After-hours submit cadence belongs to `harness/workflows/after-hours-autopilot.md`.
- Post-trade reconciliation: every run after any submit attempt, and on any run with open orders or same-day fills.
- Analyst review cadence:
  - New fills: mark `회고 대기` immediately.
  - Interim review: after 1 full trading day or if thesis break/catalyst/risk event occurs.
  - Follow-up review: after 5 full trading days.
  - Full policy review: after 20 full trading days or when a position is closed.
  - Portfolio-level review: weekly after Friday close, or next available session.

## Current User Portfolio Directive

For the 2026-05-27 US regular session, apply this user-requested overlay after all normal gates and before final order selection:

- The user asked to run today's autopilot more aggressively, but with better diversification.
- Current intended exposure target follows the staged target path in `harness/recommendation-policy.yaml` and the maximum invested ratio in `harness/risk-policy.yaml`.
- Candidate ranking, buy/hold/trim decisions, and diversification tradeoffs should be determined by the workflow's own policy, current portfolio state, and current MCP/market evidence rather than by hard-coded preferred ticker pairs or manual exclusions.
- This overlay may only influence the maximum allowed aggressiveness among candidates that already pass market, universe, MCP, quote, spread, duplicate-order, cash, and risk gates. It must not override hard gates, concentration limits, or paper validation sizing limits.

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
4. In the shell wrapper, run `scripts/cancel-stale-autopilot-orders.py`.
   - This helper is Alpaca MCP only and paper-mode only.
   - It may cancel only stale, unfilled, day limit US-equity orders whose `client_order_id` starts with `hourly-`, and only when `harness/risk-policy.yaml` has `order_lifecycle.cancel_stale_unfilled_orders=true`.
   - It must never cancel non-autopilot orders, partially filled orders, options, crypto, shorts, or live orders.
   - If stale autopilot orders remain because cancellation or reconciliation failed, block new submissions with `first_blocking_gate=risk_open_order_lifecycle`.
5. In the shell wrapper, capture scheduler-owned Alpaca core read-only evidence through `scripts/fetch-alpaca-core-preflight.py`.
   - This helper talks to the Alpaca MCP stdio server only. It never submits, replaces, cancels, closes, or REST-calls orders.
   - If the preflight JSON exists and its `hard_gate_summary.status` is `pass`, use its `mcp_coverage_hint` and passing tool rows as Alpaca MCP evidence for clock, account, positions, open orders, recent fills, watchlists, tradability checks, latest quotes, snapshots, and latest trades.
   - The preflight exists to prevent non-interactive scheduled runs from turning read-only Alpaca core calls into false `cancelled` gaps. If a row is missing, stale, or failed, retry only that missing read-only Alpaca MCP tool through the registered Codex MCP tool, then classify any remaining gap.
   - Do not submit on a quote row that would be older than the freshness limit in `harness/risk-policy.yaml`; refresh through Alpaca MCP or skip the order.
6. In the shell wrapper, capture scheduler-owned research evidence through `scripts/fetch-research-mcp-preflight.py`.
   - Pass the Alpaca core preflight JSON path and `CODEX_AUTOPILOT_RESEARCH_SYMBOL_LIMIT` so the helper can choose liquid shortlist symbols from fresh Alpaca quotes before nested Codex starts.
   - This helper attempts SEC EDGAR, Alpha Vantage, FRED, Firecrawl, and Yahoo Finance through their local MCP stdio wrappers, writes one provider row per research MCP, and emits `mcp_coverage_hint` rows for direct manifest use.
   - Provider checks run concurrently across providers. SEC EDGAR and Yahoo Finance must reuse one MCP stdio session per provider for the shortlisted symbols instead of starting a new MCP process per symbol/tool call.
   - Positive provider rows may be reused from the short-lived `.cache/research-mcp-preflight` cache. Treat `cache_hit=true` rows as scheduler-owned MCP evidence and keep their original `source_ref`/provider classification.
   - If a provider recently failed with a systemic `timeout`, `cancelled`, `dns`, `auth`, or `wrapper_error`, the preflight may emit a `circuit_breaker_open` row for the configured cool-down period. Preserve that row as a provider gap instead of spending the cycle retrying a known-bad provider.
   - Treat this preflight as the authoritative scheduled evidence for the symbols listed in its `symbols` field. Count rows with `outcome=pass|usable|ok` and `used_in_score=true` toward the 3-provider buy gate.
   - If a provider row is `gap`, `failed`, or `unavailable`, preserve its `gap_category`, `gap_reason`, and `retry_count` in the manifest. Do not call shell/curl/local network helpers from nested Codex to "make up" a failed provider.
   - SEC EDGAR preflight must use `harness/sec-ticker-cik-map.json` first and lightweight `get_company_info`/`get_recent_filings` before any heavier SEC tool. Missing ETF/non-company CIKs are `empty_response` lookup gaps, not provider outages.
   - When all five research provider rows are present in the preflight, the shell wrapper may omit research MCP registrations from nested Codex to avoid a second cold start. Nested Codex must not treat that intentional omission as a provider failure.
   - If the research preflight file is missing or malformed, use registered Codex MCP tools once for the missing providers, classify any remaining failures, and submit nothing unless the strict MCP gate passes.
7. Use Alpaca MCP evidence to check market clock, account, cash, positions, open orders, recent activities, current quotes, snapshots, and relevant news.
8. Build a broad universe from `harness/symbol-metadata.yaml`, current holdings, Alpaca watchlists, and benchmarks `SPY` and `QQQ`.
9. Run the expanded-universe first-pass screen. Record `universe_coverage` in the run manifest.
10. For the pre-MCP shortlist and any proposed order symbol, query all decision MCPs:
   - Core: Alpaca
   - Research: SEC EDGAR, Alpha Vantage, FRED, Firecrawl, Yahoo Finance
   - For Alpaca core, call and record clock, account, positions, open orders, recent activities, and per-candidate quotes/spreads as separate checks. If the core gate fails, record the first failed check in `first_blocking_gate`.
   - Prefer the scheduler-owned research preflight rows over nested Codex provider calls when the file exists. Use direct research MCP calls only for provider rows that are missing from the preflight or for candidate symbols outside the preflight `symbols`.
   - For SEC EDGAR, resolve ticker to CIK with `harness/sec-ticker-cik-map.json` before marking a ticker lookup failure. If a ticker is absent from the cache, record `gap_category=empty_response` for lookup gaps rather than conflating it with provider failure. Scheduled autopilot should use lightweight company info and recent filing checks first; do not let a heavier financials call turn otherwise usable SEC evidence into a cancellation gap.
   - If a required MCP fails due to timeout, cancellation, DNS, or transient network error, retry up to 2 times with a short backoff before marking it failed.
   - For DNS/network failures, run a read-only connectivity probe when practical and record whether the provider endpoint itself was reachable.
   - Classify failed/gap coverage rows with `gap_category`: `timeout`, `cancelled`, `dns`, `auth`, `empty_response`, `provider_error`, `wrapper_error`, `not_applicable`, or `unknown`.
   - Never mark a failed provider as usable because of a retry. Retries only prevent false negatives from transient failures.
   - Record `mcp_gate_policy` in the run manifest with `core_servers=["alpaca"]`, the five research servers, `min_research_confirmations=3`, and `all_research_must_be_attempted=true`.
   - If fewer than 3 research MCPs are usable/pass, set `recommendation_actionability=actionable_if_provider_recovered` for otherwise strong candidates and submit nothing.
11. Create a detailed current recommendation report under `wiki/current-runs/daily/` or a scheduled-run subreport if multiple runs happen on the same date.
12. Create a concrete order-plan JSON under `wiki/trade-ledger/orders/`.
   - Include current positions from Alpaca core evidence even when `orders` is empty or the run is blocked. Do not leave `positions` empty when the account snapshot shows invested exposure.
   - Include detailed per-order `rationale`.
   - Include source refs, quote timestamp, asset check timestamp, liquidity/spread, confidence score, strategy id/version, policy status, expected excess return, expected adverse move, entry style, sizing basis, and review horizons.
   - Include `risk_inputs.new_orders_submitted_today` before this run so the risk validator enforces `daily_limits.max_new_orders_per_day` for the sides listed in `daily_limits.max_new_orders_per_day_applies_to_sides`; do not impose any separate validation-order budget outside the active policy YAML.
   - First evaluate held positions for sell/trim/exit using `risk_trim_policy`. Record `sell_trigger_none` when no active trigger exists, or `sell_skip_gate` when a trigger exists but a non-budget gate blocks it.
   - Write `sell_candidate_diagnostics` into the order plan and manifest on every completed run. Use `risk_trim_policy.sell_candidate_diagnostics` for ranking and fields, and include the top unexecuted sell/trim candidates even when the final recommendation is hold/watch.
   - Treat the daily validation-buy cap as a buy-side throttle. It must not by itself suppress a risk-reducing sell/trim candidate that passes held-quantity, quote, spread, open-order, and risk checks.
   - If all hard gates pass during regular market hours, prefer validation buys for the highest-ranked actionable candidates that pass position/theme/factor/speculative caps.
   - Use up to `paper_validation_execution.validation_order_sizing.max_new_buy_orders_per_run` buy slots under normal conditions. Additional slots should normally be different correlated clusters and must satisfy the cash-ratio floors in `harness/recommendation-policy.yaml`.
   - Size validation buys from `paper_validation_execution.validation_order_sizing.confidence_tiers`. Use the largest whole-share quantity that fits the candidate tier's `max_notional_pct` and `max_qty`, then run the normal risk validator.
   - Apply `target_exposure_path`: below the acceleration threshold, a strong diversified run may use up to the normal per-run exposure budget; high-conviction runs may use the high-conviction budget. Between the selective threshold and the max policy target, submit only candidates that improve portfolio quality or diversify risk. Above the rebalance threshold, evaluate trim/rebalance before new buys.
   - Apply `risk_trim_policy.portfolio_target_bands`: target and warning bands are softer than hard caps but should restrict same-theme/factor/cluster buys when warning bands are crossed, and should create a trim diagnostic when deterioration is also present.
   - Apply `open_order_policy`: same symbol/side open orders block duplicates; same correlated-cluster open orders normally block additional buys in that cluster; fresh open orders in other clusters do not by themselves block a new candidate if the lifecycle and risk gates pass.
   - If the highest-ranked candidate is already held, add only when the ticker cap and cluster caps still pass.
   - Buy orders require core MCP pass, the research MCP confirmation threshold from `harness/recommendation-policy.yaml`, universe pass, fresh quote, spread, and risk pass.
   - Sell/trim orders require core MCP pass, fresh quote, spread, open-order check, and risk pass. Full research MCP pass is not required for risk trim.
   - Valid sell/trim rationales are the values in `risk_trim_policy.allowed_reasons`; include risk triggers, lifecycle review decisions, target-band de-risking, and relative opportunity-cost rotation only when their YAML conditions pass.
   - Do not apply new-buy confidence/source-confidence/policy-status gates to risk-reducing sells. A rejected or low-confidence thesis can be the reason for `entry_style=trim` or `entry_style=exit`; the risk validator still enforces held quantity and order-shape gates.
   - Evaluate active trim triggers every run using `risk_trim_policy.active_trim_triggers`: position overweight, theme/factor/cluster cap warning, overheat reversal, stale thesis underperformance, and speculative loss control should produce a trim candidate when quote/spread/open-order/risk gates pass.
   - Apply `risk_trim_policy.rotation_trim`: do not sell merely because a new candidate ranks higher, but if a held position falls below the YAML expected-return floor and a replacement passes the YAML quality margin plus all buy/sell gates, create a limited trim candidate rather than silently holding.
   - Apply `risk_trim_policy.validation_lifecycle`: every filled validation buy must receive due-horizon hold/add/trim/close review decisions. If a due review is missing, record it in diagnostics and block additional buys for that symbol until the review is written.
   - When buy slots or validation-buy notional budgets are exhausted, continue evaluating trim triggers separately and record whether there were zero sell triggers or whether a sell was skipped by a non-budget gate.
   - Do not sell solely because a new buy candidate ranks higher.
13. Validate:

```bash
python3 scripts/check-universe-coverage.py --strict wiki/evidence-store/run-manifests/YOUR-RUN.json
python3 scripts/check-mcp-coverage.py --strict wiki/evidence-store/run-manifests/YOUR-RUN.json
python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/YOUR-RUN.json
```

14. Submit paper orders only when all of the following are true:
    - Market is open.
    - `ALPACA_PAPER_TRADE=true`.
    - Universe strict gate passes.
    - MCP strict gate passes under the tiered policy in `harness/recommendation-policy.yaml`.
    - Risk gate passes.
    - Quote age is within policy.
    - Spread is present and within policy.
    - Order plan mode is `submit`.
    - Order shape is whole-share day limit stock/ETF.
    - No same-day duplicate symbol/side conflict.
    - For validation buys, the order respects the `paper_validation_execution.validation_order_sizing` limits in `harness/recommendation-policy.yaml`.
15. Submit only through Alpaca MCP order tools. Do not call Alpaca trading REST endpoints directly.
16. Run post-trade reconciliation immediately after any submit attempt.
17. Append `wiki/log.md` with:
    - run id
    - market clock
    - recommendation shortlist
    - submitted/skipped orders
    - validation status
    - manifest path
    - order-plan path
    - report path
    - review due markers
18. Let the scheduled shell wrapper commit and push generated artifacts after the workflow exits successfully. Do not run ad hoc git commands inside this workflow unless explicitly requested.

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
