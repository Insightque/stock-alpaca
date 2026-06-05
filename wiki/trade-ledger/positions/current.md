# portfolio-current

_Last updated: 2026-06-05 12:59 KST_

## 계좌 요약

- Alpaca paper account status: ACTIVE
- Portfolio value: $102,168.84
- Cash: $30,369.56
- Buying power: $252,204.76
- Long market value: $71,799.28

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-05-1251-after-hours-autopilot]]
- Open/new: 없음
- Filled: `WMT` buy 1 @ `118.38` avg fill, `client_order_id=ah-20260605-1251-buy-wmt`, `order_id=6bc7b899-df65-463e-bee9-b671d20c2126`, `status=filled`
- Cancelled: stale prior `WMT` buy 1 @ `118.28` limit, `client_order_id=ah-20260605-1231-buy-wmt`, `order_id=1fd44ccc-f889-4d18-ad35-6326e16e557e`, `status=canceled`
- Position count observed by Alpaca MCP: 33 positions. `WMT` 보유 수량은 5주로 증가했고 신규 open order는 없다.
- Recent reconciliation scope: scheduler-owned `1251` Alpaca core/research preflight와 runtime `cancel_order_by_id/place_stock_order/get_order_by_client_id/get_orders(status=open)/get_orders(after=2026-06-04T20:00:00Z)/get_account_info/get_all_positions` 확인 기준 장외 stale order cancel 후 replacement buy 1주가 즉시 체결됐다.
- Orders submitted/replaced/cancelled/closed by this workflow: 1 / 0 / 1 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-05-1251-after-hours-autopilot-post-trade.json`

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

- 위 계좌 요약 수치는 `1251` scheduler core preflight와 runtime Alpaca MCP reconciliation 기준이다.
- after-hours session budget은 이번 체결로 `2/2`가 됐고, 같은 세션의 stale prior WMT order는 먼저 취소 후 재실행됐다.
- close 이후 reconciliation 기준 open order는 0건이며 신규 fill은 `WMT` 1주다.
