# portfolio-current

_Last updated: 2026-06-05 10:13 KST_

## 계좌 요약

- Alpaca paper account status: ACTIVE
- Portfolio value: $101,948.09
- Cash: $30,487.94
- Buying power: $252,152.78
- Long market value: $71,460.15

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-05-1011-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: 33 positions. 장외 세션에서 신규 fill, 신규 open order, 포지션 수량 변화는 없었다.
- Recent reconciliation scope: scheduler-owned `1011` Alpaca core preflight와 runtime `get_watchlists`, `get_stock_latest_quote`, `get_stock_snapshot` 기준 regular market closed와 장외 `ah-` 신규 주문 0건을 재확인했다. `QQQ`는 여전히 1주 ask가 per-order cap을 넘었고 quote freshness도 265분 이상 stale로 돌아가 `place_stock_order` 호출은 생략했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-05-1011-after-hours-autopilot-post-trade.json`

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

- 위 계좌 요약 수치는 `1011` scheduler core preflight account snapshot과 runtime `get_watchlists/get_stock_latest_quote/get_stock_snapshot` 보조 확인 기준이다.
- `JNJ` order는 pre-submit gate 시점에는 market open이었지만 실제 Alpaca submit timestamp가 `16:02:59 ET`로 close 이후가 되어, workflow safety 복구 차원에서 즉시 취소했다.
- close 이후 reconciliation 기준 open order는 0건이며 신규 fill은 없다.
