# 2026-06-11-0931-after-hours-autopilot

## 요약

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Session: `after_hours`
- Policy profile: `after_hours_policy`
- Artifact tag: `after-hours`
- Review bucket: `after_hours_validation`
- Paper mode: `ALPACA_PAPER_TRADE=true` 확인
- 결과: scheduler-owned `0931` core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. runtime overnight quote 기준 `ORCL`이 다시 executable buy fallback까지 올라왔지만, `check-risk-policy.py --json`가 `review_backlog_pending_1d_count=14` 기준 신규 after-hours buy 슬롯을 `0`으로 계산해 no-submit으로 종료했다.

## 사용한 스케줄러 프리플라이트

- Alpaca core: `wiki/evidence-store/sources/2026-06-11-0931-after-hours-autopilot-alpaca-core-preflight.json`
- Research MCP: `wiki/evidence-store/sources/2026-06-11-0931-after-hours-autopilot-research-mcp-preflight.json`
- Alpaca core preflight의 `first_blocking_gate=market_closed`는 장외 워크플로우에서 예상되는 상태였고, passing clock/account/positions/open-order/recent-activity/quote rows는 그대로 사용했다. runtime Alpaca MCP는 `get_clock`, `get_account_info`, `get_all_positions`, `get_orders(status=open)`, `get_orders(status=all, after=2026-06-10T20:00:00Z)`, `get_account_activities(activity_types=FILL, after=2026-06-10T20:00:00Z)`, `get_watchlists`, `get_stock_latest_quote(feed=overnight)` 교차 확인만 수행했다.

## Alpaca MCP 확인

- Regular market: runtime `get_clock` 기준 closed (`2026-06-10T20:33:18.343955897-04:00`)
- Account/positions: runtime `get_account_info` 기준 account `ACTIVE`, portfolio value `96773.80 USD`, cash `30865.37 USD`, buying power `293203.44 USD`, positions `33`건이다.
- Open orders: runtime `get_orders(status=open)` 기준 `0`건이다.
- Watchlists: runtime `get_watchlists` 기준 `0`건이다.
- Same-session after-hours orders: runtime `get_orders(status=all, after=2026-06-10T20:00:00Z)`와 `get_account_activities(activity_types=FILL, after=2026-06-10T20:00:00Z)` 기준 신규 after-hours order/fill은 `0`건이었다. 따라서 `risk_inputs.after_hours_new_orders_submitted_today=0`, session cap은 `0/2`다.

## 후보 평가

- `AVGO` sell/trim: sell side 허용 정책에 따라 먼저 재평가했지만 runtime overnight quote `370.14/371.07`의 spread가 약 `0.2506%`로 after-hours cap `0.25%`를 아주 근소하게 넘었다.
- `RGTI` sell/trim: runtime overnight quote `19.34/19.41`는 fresh였지만 spread 약 `0.3606%`로 cap 초과였다.
- `SO` sell/trim: runtime overnight quote `79.93/95.05`는 비대칭이 심했고 decision 시점 기준 freshness cap `5분`도 넘겨 executable two-sided trim order를 만들지 못했다.
- `ORCL`: runtime overnight quote `181.28/181.51`, spread 약 `0.1267%`, 1주 notional `181.51 USD`, asset active/tradable/overnight_tradable, research preflight의 `SEC EDGAR/FRED/Firecrawl/Yahoo` confirmation 조합까지 모두 유지돼 이번 cycle의 최상위 executable buy fallback이 됐다.
- `IONQ`: runtime overnight quote `56.27/56.36`는 fresh이고 spread 약 `0.1597%`로 양호했지만 speculative quantum sleeve라 `ORCL`보다 우선순위가 낮았다.
- `NOK`: runtime overnight quote `13.14/13.17`는 fresh이고 spread 약 `0.2278%`로 cap 이내였지만 review-due add-block이 유지됐다.
- `SPY/QQQ`: runtime overnight quote도 fresh였지만 1주 ask가 각각 `725.57 USD`, `693.14 USD`로 after-hours per-order cap 약 `483.87 USD`를 넘었다.
- Review backlog: `review-due-index` 기준 `pending_1d_count=14`, `pending_5d_count=13`, `pending_20d_count=1`이었다. 이번 cycle의 직접 blocker는 quote가 아니라 risk validator의 backlog throttle이다.

## Artifacts

- Manifest: `wiki/evidence-store/run-manifests/2026-06-11-0931-after-hours-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-11-0931-after-hours-autopilot.json`
- Gate evaluation source: `wiki/evidence-store/sources/2026-06-11-0931-after-hours-autopilot-after-hours-gate-evaluation.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-11-0931-after-hours-autopilot-post-trade.json`

## Gate 결과

| Gate | Status |
| --- | --- |
| alpaca_paper_mode | pass |
| regular_market_open | pass_regular_market_closed |
| extended_hours_session | pass |
| alpaca_core_account_clock_position_order_quote_spread | pass_market_closed_nonblocking_after_hours |
| after_hours_policy_profile | pass |
| separate_after_hours_order_budget | pass_zero_of_two_submitted |
| universe_strict | pass |
| mcp_tiered_strict | pass |
| risk_policy | fail_review_backlog_throttle_zero_new_buy_slots |
| fresh_quote | pass_runtime_overnight_quotes_fresh_for_orcl_ionq_nok_and_benchmark_cross_check |
| spread_within_after_hours_policy | pass_orcl_ionq_nok_runtime_spreads_within_cap_sell_candidates_still_fail |
| whole_share_day_limit_extended_hours_order | pass_orcl_order_shape_but_removed_before_submit |
| immediate_reconcile_and_cancel_or_lifecycle_record | pass_no_submit |

## 주문 계획

- `market.session=after_hours`, `risk_inputs.after_hours_new_orders_submitted_today=0`, `session=after_hours`, `review_bucket=after_hours_validation`를 기록한 submit-mode order plan을 생성했다.
- runtime 기준 `ORCL` 1주 buy limit `181.51 USD`가 가장 executable했지만 `check-risk-policy.py --json`가 `pending_1d_count=14`에서 신규 buy 슬롯을 `0`으로 계산해 최종 plan은 `orders=[]`로 확정했다.

## 검증

- `PATH=/usr/local/bin:$PATH python3 scripts/check-universe-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-11-0931-after-hours-autopilot.json`
- `PATH=/usr/local/bin:$PATH python3 scripts/check-mcp-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-11-0931-after-hours-autopilot.json`
- `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-06-11-0931-after-hours-autopilot.json`

## Submit And Reconcile

- `place_stock_order`, `cancel_order_by_id`는 이번 cycle에서 호출하지 않았다.
- runtime Alpaca MCP cross-check 기준 신규 after-hours order 없음, standing extended-hours order 없음, 포지션 수량 변화 없음.
