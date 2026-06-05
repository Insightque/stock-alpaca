# portfolio-current

_Last updated: 2026-06-05 13:34 KST_

## 계좌 요약

- Alpaca paper account status: ACTIVE
- Portfolio value: $102,213.74
- Cash: $30,369.56
- Buying power: $252,278.48
- Long market value: $71,844.18

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-05-1331-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: 33 positions. `WMT` 5주, `AVGO` 16주, 신규 open order 없음.
- Recent reconciliation scope: scheduler-owned `1331` Alpaca core/research preflight와 runtime `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-04T20:00:00Z)/get_stock_latest_quote(feed=overnight)` 확인 기준 장외 separate session budget `2/2` 소진으로 submit 없이 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-05-1331-after-hours-autopilot-post-trade.json`

## 직전 after-hours-autopilot reconciliation

- Run: [[2026-06-05-1311-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: 33 positions. `WMT` 5주, `AVGO` 16주, 신규 open order 없음.
- Recent reconciliation scope: scheduler-owned `1311` Alpaca core/research preflight와 runtime `get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-04T20:00:00Z)/get_stock_latest_quote/get_stock_snapshot` 확인 기준 장외 separate session budget `2/2` 소진으로 submit 없이 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-05-1311-after-hours-autopilot-post-trade.json`

## 직전 hourly-autopilot reconciliation

- Run: [[2026-06-05-0451-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: `JNJ` buy 1 @ `229.25` limit, `client_order_id=hourly-20260605-0451-buy-jnj`, `order_id=915838ec-e52b-41c2-9682-fdb7b94dba52`, `status=canceled`
- Position count observed by Alpaca MCP: 33 positions. `JNJ` 신규 보유는 생기지 않았다.
- Recent reconciliation scope: `get_clock`, `place_stock_order`, `cancel_order_by_id`, `get_order_by_id`, `get_orders(status=open)` 기준 regular close 이후 생성된 JNJ queued order를 즉시 취소했고 open order 0건을 확인했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 1 / 0 / 1 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-05-0451-hourly-autopilot-post-trade.json`

## 계좌 요약 주석

- 위 계좌 요약 수치는 `1331` runtime Alpaca MCP reconciliation 기준이다.
- after-hours session budget은 `1231` cancel + `1251` fill submit lifecycle로 이미 `2/2`라 `1331` cycle에서도 추가 주문을 만들지 않았다.
- close 이후 reconciliation 기준 open order는 0건이며 `1331` 신규 fill은 없다.
