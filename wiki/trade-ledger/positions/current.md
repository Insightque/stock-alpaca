# portfolio-current

- 기준: `2026-05-28T14:22:00Z` 23:11 hourly autopilot post-trade reconciliation.
- 계좌: status ACTIVE, portfolio value `$101,471.45`, cash `$39,924.27`, buying power `$135,028.44`, long market value `$61,547.18`.
- 신규 체결: PFE 1주 @ 26.16.
- 신규 미체결/open order: WMT buy 1주 limit 118.63.
- 기존 미체결/open order: NEE buy 1주 limit 88.00. BAC stale order는 scheduler cleanup 이후 등록 Alpaca MCP open-order reconciliation에서 더 이상 open이 아닌 것으로 확인.

| Symbol | Qty | 상태 | 비고 |
| --- | ---: | --- | --- |
| PFE | 2 | long | 23:11 run에서 1주 추가 체결, avg entry 26.25 |
| WMT | 1 | long + open buy 1 | 보유 1주, 23:11 run WMT buy 1주 open/new |
| NEE | 1 | long + open buy 1 | 22:51 run NEE buy 1주 open/new |
| 주요 기타 | n/a | long | 전체 포지션은 post-trade JSON `wiki/trade-ledger/positions/2026-05-28-2311-hourly-autopilot-post-trade.json`와 Alpaca MCP positions refresh 기준 |
