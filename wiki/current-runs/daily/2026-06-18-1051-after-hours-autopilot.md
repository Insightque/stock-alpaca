# 2026-06-18-1051-after-hours-autopilot

## 요약

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Session: `after_hours`
- Policy profile: `after_hours_policy`
- Artifact tag: `after-hours`
- Review bucket: `after_hours_validation`
- Paper mode: `ALPACA_PAPER_TRADE=true` 확인
- 결과: scheduler-owned `1051` Alpaca core/research preflight를 source-of-record로 사용했다. Alpaca core `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했고, 같은 preflight의 account/positions/open-orders/account-activities/asset/quote/spread rows를 submit-boundary evidence로 재사용했다. separate after-hours session budget은 `0/2`로 열려 있었지만 freshest quote `MS`도 약 `331.44`분 stale였고 `QQQ`만 spread는 통과했지만 stale+per-order notional cap에, `MS/NVDA/SPY/TSLA/GOOGL/WMT/JPM/PFE/RGTI/AVGO/MSFT`는 stale+wide or missing spread에 막혀 no-submit으로 종료했다.

## 사용한 스케줄러 프리플라이트

- Alpaca core: `wiki/evidence-store/sources/2026-06-18-1051-after-hours-autopilot-alpaca-core-preflight.json`
- Research MCP: `wiki/evidence-store/sources/2026-06-18-1051-after-hours-autopilot-research-mcp-preflight.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-06-18-1051-after-hours-autopilot-after-hours-gate-evaluation.json`
- Alpaca core preflight의 `first_blocking_gate=market_closed`는 장외 워크플로우에서 expected nonblocking으로 처리했다. 이번 cycle은 scheduler-owned preflight에 already-passing account/positions/open-orders/account-activities/asset/quote/spread rows가 모두 존재해 same artifact를 submit-boundary source-of-record로 유지했다.

## Alpaca MCP 확인

- Regular market: closed (`get_clock.timestamp=2026-06-17T21:51:09.014454533-04:00`); callable Alpaca MCP surface에 direct `get_clock` tool이 노출되지 않아 이 gate는 scheduler-owned preflight clock을 source-of-record로 유지했다.
- Account: preflight `get_account_info` 기준 account `ACTIVE`, portfolio value `101109.31 USD`, cash `28003.45 USD`, buying power `301008.09 USD`; direct continuity `get_account_info`도 account `ACTIVE`, portfolio value `101105.47 USD`, cash `28003.45 USD`, buying power `300963.57 USD`로 parity 유지
- Positions / open orders / watchlists: preflight `get_all_positions` 기준 positions `34`건, `get_orders_open` 기준 open orders `0`건, `get_watchlists` 기준 watchlists `0`건; direct continuity도 positions `34`, open orders `0`, watchlists `0`
- Same-session after-hours orders / fills: scheduler preflight `orders_submitted=0`, current-session `ah-` submit 없음. direct `get_orders(status=all, after=2026-06-17T20:00:00-04:00)` 기준 same-session after-hours order `0`건, direct `get_account_activities(activity_types=[FILL], after=2026-06-17T20:00:00-04:00)` 기준 same-session after-hours fill도 `0`건이었다.
- Quote boundary: scheduler-owned IEX quote 기준 freshest candidate는 `MS` `2026-06-17T20:20:00.57860736Z`였고 scheduler-owned submit-boundary stack은 약 `331.44`분에서 `351.45`분 stale였다. direct continuity `get_stock_latest_quote(feed=iex)`도 같은 timestamp stack을 재확인해 freshness blocker가 해소되지 않았다.

## 후보 평가

- `PFE` sell/trim: quote `24.70/27.38`, spread `10.8502%`, age `351.42`분. repeated weak-review trim rationale는 유지됐지만 freshness/spread 동시 fail.
- `RGTI` sell/trim: quote `17.57/23.11`, spread `31.5310%`, age `351.43`분. residual speculative sleeve trim rationale는 유지됐지만 freshness/spread 동시 fail.
- `AVGO` sell/trim: quote `377.01/416.43`, spread `10.4560%`, age `351.44`분. sell side 허용 policy는 유지됐지만 executable sell gate는 닫혀 있었다.
- `QQQ` buy fallback: quote `722.87/723.00`, spread `0.0180%`로 양호했지만 age `351.38`분으로 stale이고 1주 ask `723.00 USD`가 after-hours per-order cap 약 `505.53 USD`를 넘었다.
- `MS` buy fallback: quote `220.00/231.46`, spread `5.2091%`, age `331.44`분. freshest shortlist quote였지만 spread/freshness가 모두 fail했다.
- Review backlog: `wiki/trade-ledger/reviews/review-due-index.json` 기준 `pending_1d_count=17`, `pending_5d_count=23`, `pending_20d_count=15`, `blocked_add_symbols=['NOK']`였다. 이번 cycle은 backlog throttle보다 fresh-quote hard gate가 직접 차단 요인이었다.

## Gate 결과

| Gate | Status |
| --- | --- |
| alpaca_paper_mode | pass |
| regular_market_open | pass_regular_market_closed |
| extended_hours_session | pass |
| alpaca_core_account_clock_position_order_quote_spread | pass_scheduler_preflight_rows_reused |
| after_hours_policy_profile | pass |
| separate_after_hours_order_budget | pass_zero_of_two_submitted |
| universe_strict | PASS |
| mcp_tiered_strict | PASS |
| risk_policy | PASS with expected `orders is empty` warning |
| fresh_quote | fail_scheduler_owned_submit_boundary_quotes_stale_331.44_to_351.45_minutes |
| spread_within_after_hours_policy | fail_no_candidate_met_fresh_and_spread_and_notional_together |
| whole_share_day_limit_extended_hours_order | pass_no_orders_built |
| immediate_reconcile_and_cancel_or_lifecycle_record | pass_no_submit |

## Submit And Reconcile

- `place_stock_order`는 호출하지 않았다. 신규 `client_order_id`, retry, alternate client id도 만들지 않았다.
- Separate after-hours session budget은 `0/2`로 열려 있었지만 fresh quote hard gate가 먼저 닫혀 submit path가 열리지 않았다.
- 이번 cycle의 reconciliation은 scheduler-owned preflight와 direct continuity 기준 open orders `0`, same-session after-hours submitted `0`, same-session after-hours fills `0`, positions `34` 확인으로 종료했다.

## Validators

- `PATH=/usr/local/bin:$PATH python3 scripts/check-universe-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-18-1051-after-hours-autopilot.json` PASS
- `PATH=/usr/local/bin:$PATH python3 scripts/check-mcp-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-18-1051-after-hours-autopilot.json` PASS
- `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-06-18-1051-after-hours-autopilot.json` PASS with expected `orders is empty` warning

## Artifacts

- Report: `wiki/current-runs/daily/2026-06-18-1051-after-hours-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-18-1051-after-hours-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-18-1051-after-hours-autopilot.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-06-18-1051-after-hours-autopilot-after-hours-gate-evaluation.json`
- Runtime spot check: `wiki/evidence-store/sources/2026-06-18-1051-after-hours-autopilot-runtime-alpaca-spot-check.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-18-1051-after-hours-autopilot-post-trade.json`
