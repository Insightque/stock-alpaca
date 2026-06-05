# 2026-06-05-1951-after-hours-autopilot

## 요약

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Session: `after_hours`
- Policy profile: `after_hours_policy`
- Artifact tag: `after-hours`
- Review bucket: `after_hours_validation`
- Paper mode: `ALPACA_PAPER_TRADE=true` 확인
- 결과: scheduler-owned `1951` core/research preflight를 우선 사용했고 Alpaca core `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. runtime Alpaca MCP 기준 실제 장외 submit count는 여전히 `ah-20260605-1231-buy-wmt` 취소 + `ah-20260605-1251-buy-wmt` 체결로 `2/2`였고, 이번 cycle에서도 runtime overnight quote가 모두 `173.35`분 stale 상태라 submit 없이 종료했다.

## 사용한 스케줄러 프리플라이트

- Alpaca core: `wiki/evidence-store/sources/2026-06-05-1951-after-hours-autopilot-alpaca-core-preflight.json`
- Research MCP: `wiki/evidence-store/sources/2026-06-05-1951-after-hours-autopilot-research-mcp-preflight.json`
- Alpaca core preflight의 `first_blocking_gate=market_closed`는 장외 워크플로우에서 예상되는 상태였고, passing clock/account/positions/open-order/asset/quote rows는 그대로 사용했다. runtime Alpaca MCP는 `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-04T20:00:00Z)/get_order_by_client_id/get_stock_latest_quote(feed=overnight)/get_stock_snapshot(feed=overnight)`로 after-hours order lifecycle과 overnight quote/spread를 재확인했다.

## Alpaca MCP 확인

- Regular market: closed (`2026-06-05T06:53:21.254642876-04:00`)
- Account/positions: runtime Alpaca MCP 기준 account `ACTIVE`, portfolio value `102,344.62 USD`, cash `30,369.55 USD`, buying power `252,564.34 USD`, positions `33`건. runtime reconciliation highlight는 `WMT` `5주`, `AVGO` `16주`, `PFE` `3주`.
- Open orders: 이번 cycle에서 신규 open order 확인 없음.
- After-hours session order count: runtime Alpaca MCP `get_orders(status=all, after=2026-06-04T20:00:00Z)` + `get_order_by_client_id` 교차 확인 기준 실제 장외 submit은 `ah-20260605-1231-buy-wmt` 취소 1건과 `ah-20260605-1251-buy-wmt` 체결 1건으로 이미 `2/2`였다.

## 후보 평가

- `AVGO` sell/trim: sell side 허용 정책에 따라 다시 평가했지만 runtime overnight quote `409.39/420.40`, quote age `173.35`분, spread `2.6189%`로 장외 fresh-quote/spread gate를 동시에 위반했다. 또한 `2026-06-05-portfolio-review`의 catalyst-risk alert 상태와 `review-due-index` due-review discipline, decision-grade trim metric gap 때문에 executable sell trigger로 승격하지 못했다.
- `PFE`: runtime overnight quote `25.77/26.32`, quote age `173.35`분, spread `2.0897%`로 after-hours fresh-quote/spread cap을 동시에 위반했다.
- `WMT`: runtime overnight quote `112.78/129.09`, quote age `173.35`분, spread `12.6346%`로 after-hours fresh-quote/spread cap을 동시에 위반했다.
- `QQQ`/`SPY`: stale overnight quote였고 spread도 각각 `4.7399%`, `0.4728%`로 cap을 넘겼다. 동시에 1주 ask가 장외 per-order cap `511.72 USD`를 초과했다.

## Artifacts

- Manifest: `wiki/evidence-store/run-manifests/2026-06-05-1951-after-hours-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-05-1951-after-hours-autopilot.json`
- Gate evaluation source: `wiki/evidence-store/sources/2026-06-05-1951-after-hours-autopilot-after-hours-gate-evaluation.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-05-1951-after-hours-autopilot-post-trade.json`

## Gate 결과

| Gate | Status |
| --- | --- |
| alpaca_paper_mode | pass |
| regular_market_open | pass_regular_market_closed |
| extended_hours_session | pass |
| alpaca_core_account_clock_position_order_quote_spread | pass_market_closed_nonblocking_after_hours |
| after_hours_policy_profile | pass |
| separate_after_hours_order_budget | fail_budget_already_2_of_2_submitted |
| universe_strict | pass |
| mcp_tiered_strict | pass |
| risk_policy | pass_no_submit_budget_block |
| fresh_quote | fail_runtime_quotes_stale_over_5_minutes_for_avgo_pfe_wmt_qqq_spy |
| spread_within_after_hours_policy | fail_runtime_spread_cap_exceeded_for_avgo_pfe_wmt_qqq_spy |
| whole_share_day_limit_extended_hours_order | pass_candidate_shape_confirmed_but_not_executed |
| immediate_reconcile_and_cancel_or_lifecycle_record | pass_no_submit_reconciled_by_account_orders_positions |

## 주문 계획

- `market.session=after_hours`, `after_hours_new_orders_submitted_today=2`를 기록한 submit-mode order plan을 생성했다.
- separate after-hours session budget이 이미 소진되어 `orders=[]`로 유지했다.

## 검증

- `PATH=/usr/local/bin:$PATH python3 scripts/check-universe-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-05-1951-after-hours-autopilot.json`: PASS
- `PATH=/usr/local/bin:$PATH python3 scripts/check-mcp-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-05-1951-after-hours-autopilot.json`: PASS
- `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-06-05-1951-after-hours-autopilot.json`: PASS (`orders is empty` warning only)

## Submit And Reconcile

- `place_stock_order`, `cancel_order_by_id`는 이번 cycle에서 호출하지 않았다. separate after-hours session budget gate가 hard-gate 순서상 먼저 막았고, runtime quote freshness/spread gate도 동시에 실패했다. 신규 client order id는 만들지 않았다.
- runtime Alpaca MCP `get_orders(status=open)/get_orders(status=all, after=2026-06-04T20:00:00Z)/get_order_by_client_id/get_stock_latest_quote(feed=overnight)/get_stock_snapshot(feed=overnight)` 교차 확인 기준 신규 fill 없음, 포지션 수량 변화 없음.
