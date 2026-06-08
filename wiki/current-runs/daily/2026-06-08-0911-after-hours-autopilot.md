# 2026-06-08-0911-after-hours-autopilot

## 요약

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Session: `after_hours`
- Policy profile: `after_hours_policy`
- Artifact tag: `after-hours`
- Review bucket: `after_hours_validation`
- Paper mode: `ALPACA_PAPER_TRADE=true` 확인
- 결과: scheduler-owned `0911` core/research preflight를 우선 사용했고 Alpaca core `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. strict universe/MCP/risk gate와 separate after-hours budget `0/2`를 통과한 뒤, buy backlog throttle을 피할 수 있는 허용 sell side에서 `AVGO` 1주 trim을 선택했다. runtime `overnight` quote `391.26/391.31`, spread `0.012775%`, quote age `1.86`분 기준으로 장외 quote/spread cap을 통과했고, Alpaca MCP `place_stock_order`는 `AVGO` 1주 sell을 생성한 뒤 same client id reconciliation에서 `391.27 USD` 체결로 닫혔다.

## 사용한 스케줄러 프리플라이트

- Alpaca core: `wiki/evidence-store/sources/2026-06-08-0911-after-hours-autopilot-alpaca-core-preflight.json`
- Research MCP: `wiki/evidence-store/sources/2026-06-08-0911-after-hours-autopilot-research-mcp-preflight.json`
- Alpaca core preflight의 `first_blocking_gate=market_closed`는 장외 워크플로우에서 예상되는 상태였고, passing account/positions/open-order rows는 그대로 사용했다. runtime Alpaca MCP는 execution boundary에서 `get_clock`, `get_account_info`, `get_all_positions`, `get_orders`, `get_account_activities`, `get_stock_latest_quote(feed=iex)`, `get_stock_latest_quote(feed=overnight)` 보조 확인을 수행했다.

## Alpaca MCP 확인

- Regular market: closed (`2026-06-07T20:11:09.334287213-04:00` scheduler-owned `get_clock`, runtime `get_clock`도 `2026-06-07T20:12:40.255160665-04:00` 기준 closed)
- Account/positions: scheduler-owned core preflight와 post-trade runtime `get_account_info`, `get_all_positions` 교차 확인 기준 account `ACTIVE`, pre-submit portfolio value `98,223.98 USD`, cash `29,947.79 USD`, buying power `294,440.86 USD`, positions `33`건이었다. 체결 후 account는 cash `30,339.06 USD`, buying power `295,718.63 USD`, portfolio value `98,601.15 USD`로 갱신됐고 `AVGO` 보유수량은 `12주 -> 11주`로 줄었다.
- Open orders / activities: pre-submit runtime `get_orders(status=open)`는 `0`건이었고 after-hours submitted count는 `0/2`였다. submit 후 `get_orders(status=all, symbols=AVGO, after=2026-06-08T00:00:00Z)`와 `get_account_activities(activity_types=FILL, after=2026-06-08T00:00:00Z)`가 동일 `client_order_id=ah-20260608-0911-sell-avgo`, `order_id=59e6a81b-1c03-449a-ba62-8a141eef7b4b`, `filled_avg_price=391.27`, `filled_at=2026-06-08T00:20:05.775901Z`를 확인했다. post-trade open AVGO order는 `0`건이다.

## 후보 평가

- `AVGO` sell/trim: sell side 허용 정책에 따라 우선 재평가했다. `2026-06-06` portfolio review는 `2026-06-01` after-hours validation add 5D 결과를 `약함`으로 닫았고, `2026-06-07` portfolio review도 `post-earnings risk watch`를 유지했다. runtime `overnight` quote `391.26/391.31`, spread `0.012775%`, quote age `1.86`분, `AVGO` asset active/tradable/overnight_tradable, trim 후 보유 `11주` 유지 조건을 모두 만족해 floor-size 1주 trim으로 승격했다.
- `QQQ`, `SPY`: overnight quote quality는 양호했지만 1주 ask가 after-hours per-order `0.5%` cap을 초과했다.
- `PFE`, `WMT`, `BAC`: fresh overnight quote를 받았지만 spread가 after-hours cap `0.25%`를 넘었다.
- `GOOGL`, `XOM`: buy fallback 후보로는 유효했지만 review backlog throttle이 새 after-hours buy를 차단했고, 이번 cycle은 allowed sell side `AVGO` trim이 우선이었다.

## Artifacts

- Manifest: `wiki/evidence-store/run-manifests/2026-06-08-0911-after-hours-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-08-0911-after-hours-autopilot.json`
- Gate evaluation source: `wiki/evidence-store/sources/2026-06-08-0911-after-hours-autopilot-after-hours-gate-evaluation.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-08-0911-after-hours-autopilot-post-trade.json`
- Deterministic submit artifact: `wiki/evidence-store/sources/2026-06-08-0911-after-hours-autopilot-deterministic-submit.json`

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
| risk_policy | pass_sell_trim_candidate_ready |
| fresh_quote | pass |
| spread_within_after_hours_policy | pass |
| whole_share_day_limit_extended_hours_order | pass_avgo_sell_order_shape |
| immediate_reconcile_and_cancel_or_lifecycle_record | pass_reconciled_filled |

## Validators

- `PATH=/usr/local/bin:$PATH python3 scripts/check-universe-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-08-0911-after-hours-autopilot.json`
  - 결과: PASS
- `PATH=/usr/local/bin:$PATH python3 scripts/check-mcp-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-08-0911-after-hours-autopilot.json`
  - 결과: PASS
- `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-06-08-0911-after-hours-autopilot.json`
  - 결과: PASS

## Submit And Reconcile

- Pre-submit gate summary: `session=after_hours`, paper mode true, regular market closed, strict universe/MCP/risk PASS, separate after-hours budget `0/2`, selected order `AVGO sell 1 @ 391.26 day limit extended_hours=true`, runtime overnight quote `391.26/391.31`.
- `place_stock_order`는 `client_order_id=ah-20260608-0911-sell-avgo`로 호출했다. 다른 client id로 재시도하지 않았다.
- Same client id reconciliation 기준 주문은 `filled`로 닫혔고 `filled_avg_price=391.27 USD`, `filled_qty=1`이었다.
- Post-trade `get_orders(status=open, symbols=AVGO)`는 빈 결과였고, `get_all_positions` 기준 AVGO 보유수량은 `11주`로 감소했다.
