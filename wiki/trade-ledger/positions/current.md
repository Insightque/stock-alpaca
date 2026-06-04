# portfolio-current

_Last updated: 2026-06-05 01:59 KST_

## 계좌 요약

- Alpaca paper account status: ACTIVE
- Portfolio value: $103,239.37
- Cash: $32,141.17
- Buying power: $257,409.48
- Long market value: $71,098.20

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-05-0151-hourly-autopilot]]
- Open/new: `COP` buy 1 @ `119.17` limit, `status=new`, `client_order_id=hourly-20260605-0151-buy-cop`. same-day earlier fills `FCX`, `WMT`, `XOM`, `AAPL`, `SLB`, `SPY`, `QQQ`는 order history에 남아 있다.
- Filled: 이번 cycle 신규 fill 없음.
- Position count observed by Alpaca MCP: 32
- Recent reconciliation scope: `get_order_by_client_id`, `get_orders(symbol=COP)`, `get_orders(status=open)`, `get_all_positions`, `get_account_info` 기준 COP open order 1건과 unchanged position state를 확인했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 1 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-05-0151-hourly-autopilot-post-trade.json`

## 계좌 요약 주석

- 위 계좌 요약 수치는 submit 이후 runtime `get_account_info` MCP call 기준이다.
- COP는 아직 체결되지 않아 보유수량이 1주로 유지된다.
- `get_account_activities_by_type(FILL)` 1회는 tool-layer `cancelled`였지만, order/position/account state 대조는 모두 완료했다.
