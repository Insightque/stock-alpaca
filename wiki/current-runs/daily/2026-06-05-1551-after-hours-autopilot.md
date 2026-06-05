# 2026-06-05-1551-after-hours-autopilot

## 요약

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Session: `after_hours`
- Policy profile: `after_hours_policy`
- Artifact tag: `after-hours`
- Review bucket: `after_hours_validation`
- Paper mode: `ALPACA_PAPER_TRADE=true` 확인
- 결과: scheduler-owned `1551` core/research preflight를 우선 사용했고, Alpaca core `first_blocking_gate=market_closed`는 장외 워크플로우에서 expected nonblocking으로 처리했다. runtime Alpaca MCP 기준 strict universe/MCP/risk gate는 유지됐지만, separate after-hours session budget이 이미 `2/2`라 신규 submit 없이 종료했다.

## 사용한 스케줄러 프리플라이트

- Alpaca core: `wiki/evidence-store/sources/2026-06-05-1551-after-hours-autopilot-alpaca-core-preflight.json`
- Research MCP: `wiki/evidence-store/sources/2026-06-05-1551-after-hours-autopilot-research-mcp-preflight.json`
- Alpaca core `first_blocking_gate=market_closed`는 장외 워크플로우에서 예상되는 상태로, 단독 차단 사유로 보지 않았다. 같은 preflight의 account, positions, open_orders, asset, latest_quote, snapshot, latest_trade pass row를 사용했다.

## Alpaca MCP 확인

- Regular market: closed (`2026-06-05T02:52:59.103818242-04:00`)
- Account/positions: runtime Alpaca MCP `get_account_info/get_all_positions` 기준 account `ACTIVE`, portfolio value `101,998.30 USD`, positions `33`건, `WMT` 보유 수량 `5주`, `AVGO` `16주`, `PFE` `3주` 유지.
- Open orders: runtime Alpaca MCP `get_orders(status=open)` 기준 0건.
- After-hours session order count: runtime Alpaca MCP `get_orders(status=all, after=2026-06-04T20:00:00Z)` 기준 실제 장외 submit은 `ah-20260605-1231-buy-wmt` 취소 1건과 `ah-20260605-1251-buy-wmt` 체결 1건으로 이미 `2/2`였다.

## 후보 평가

- `AVGO` sell/trim: sell side 허용 정책에 따라 다시 평가했지만 runtime overnight quote `409.59/410.28`, spread `0.1683%`에도 `2026-06-05-portfolio-review`의 catalyst-risk alert 상태와 `review-due-index` due-review discipline, decision-grade trim metric gap 때문에 executable sell trigger로 승격하지 못했다.
- `PFE`: scheduler-owned `1551` preflight에서는 passing quote/spread row를 유지했지만 runtime overnight quote `25.68/25.79`, spread `0.4274%`, quote age 약 `1.18분`으로 after-hours spread cap `0.25%`를 초과했다. 별도로 separate after-hours budget도 이미 `2/2`라 submit 불가였다.
- `WMT`: runtime overnight quote `117.53/118.15`, quote age 약 `1.12분`이었지만 spread `0.5263%`로 after-hours spread cap `0.25%`를 초과했다.
- `QQQ`/`SPY`: fresh overnight quote와 tight spread는 유지됐지만 1주 ask가 장외 per-order cap `509.99 USD`를 초과했다.

## Artifacts

- Manifest: `wiki/evidence-store/run-manifests/2026-06-05-1551-after-hours-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-05-1551-after-hours-autopilot.json`
- Gate evaluation source: `wiki/evidence-store/sources/2026-06-05-1551-after-hours-autopilot-after-hours-gate-evaluation.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-05-1551-after-hours-autopilot-post-trade.json`

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
| fresh_quote | pass_runtime_quotes_fresh_for_pfe_avgo_qqq_spy_wmt |
| spread_within_after_hours_policy | pass_avgo_qqq_spy_within_cap_pfe_wmt_over_cap_budget_still_blocking |
| whole_share_day_limit_extended_hours_order | pass_candidate_shape_confirmed_but_not_executed |
| immediate_reconcile_and_cancel_or_lifecycle_record | pass_no_submit_reconciled_by_account_orders_positions |

## 주문 계획

- `market.session=after_hours`, `after_hours_new_orders_submitted_today=2`를 기록한 submit-mode order plan을 생성했다.
- separate after-hours session budget이 이미 소진되어 `orders=[]`로 유지했다.

## 검증

- `PATH=/usr/local/bin:$PATH python3 scripts/check-universe-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-05-1551-after-hours-autopilot.json`: PASS
- `PATH=/usr/local/bin:$PATH python3 scripts/check-mcp-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-05-1551-after-hours-autopilot.json`: PASS
- `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-06-05-1551-after-hours-autopilot.json`: PASS (`orders is empty` warning only)

## Submit And Reconcile

- `place_stock_order`, `cancel_order_by_id`, `get_order_by_client_id`는 이번 cycle에서 호출하지 않았다.
- scheduler-owned core preflight + runtime Alpaca MCP `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-04T20:00:00Z)/get_stock_latest_quote(feed=overnight)/get_stock_snapshot(feed=overnight)` 교차 확인 기준 open order 0건, 신규 fill 없음, 포지션 수량 변화 없음.
