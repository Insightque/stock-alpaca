# portfolio-current

_Last updated: 2026-06-05 01:20 KST_

## 계좌 요약

- Alpaca paper account status: ACTIVE
- Portfolio value: $103,075.90
- Cash: $32,210.68
- Buying power: $257,459.91
- Long market value: $70,865.22

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-05-0111-hourly-autopilot]]
- Open/new: 없음. reconciliation 기준 `WMT` same-cycle order는 즉시 `filled`로 전환됐고 open order는 0건이다.
- Filled: `WMT` buy 1 @ `118.40` limit, `status=filled`, `filled_avg_price=118.36`, `client_order_id=hourly-20260605-0111-buy-wmt`. same-day earlier fills `XOM`, `AAPL`, `SLB`, `SPY`, `QQQ`도 order history에 남아 있다.
- Position count observed by Alpaca MCP: 32
- Recent FILL scope: 이번 reconciliation 시점 기준 `WMT` 보유수량은 3주에서 4주로 늘었고 open order는 0건이다.
- Orders submitted/replaced/cancelled/closed by this workflow: 1 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-05-0111-hourly-autopilot-post-trade.json`

## 계좌 요약 주석

- 위 계좌 요약 수치는 submit 이후 runtime `get_account_info` MCP call 기준이다.
- direct position refresh MCP call은 `cancelled`로 돌아와, 체결과 수량 증가는 `get_order_by_client_id`, `get_orders`, `get_account_activities(FILL)`, preflight position snapshot으로 대조했다.
