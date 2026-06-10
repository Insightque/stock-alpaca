---
symbol: MSFT
asset_type: stock
---

# MSFT

## 2026-06-05 hourly-autopilot

`MSFT` 1주 regular-session day limit buy가 `426.80 USD` limit으로 제출됐고, Alpaca MCP 기준 `2026-06-04T17:39:48.565193428Z`에 `426.78 USD`로 즉시 체결됐다. 근거는 scheduler core/research preflight와 strict universe/MCP/risk gate 통과, same-day duplicate가 없는 신규 mega-cap quality diversifier 후보, 그리고 runtime IEX quote `426.67/426.80` 기준 spread `0.0305%`가 policy 한도 이내였다는 점이다. Yahoo Finance recommendation snapshot은 `strongBuy 13`, `buy 40`, `hold 3`였고, news 요약에는 Microsoft in-house AI model 출시 맥락이 포함됐다. 이 체결은 새 validation lifecycle 표본으로 기록하며 1D/5D/20D review를 추적한다.

출처: [[2026-06-05-0231-hourly-autopilot]], `wiki/trade-ledger/positions/2026-06-05-0231-hourly-autopilot-post-trade.json`, `wiki/evidence-store/sources/2026-06-05-0231-hourly-autopilot-research-mcp-preflight.json`, `wiki/evidence-store/sources/2026-06-05-0231-hourly-autopilot-alpaca-core-preflight.json`, [[2026-06-04-portfolio-review]]

## 2026-06-11 04:39 KST hourly autopilot

2026-06-11 04:39 KST hourly autopilot에서 `MSFT` 1주 regular-session day limit add를 `398.38 USD` limit으로 제출했다. 근거는 scheduler-owned `0431` stale cleanup/core/research preflight 기준 hard gate pass, same-day duplicate/open-order conflict 부재, quote `398.32/398.38` spread `0.0151%`, active tradable NASDAQ stock, 그리고 `2026-06-06` portfolio review의 1D `중립` 이후 아직 `2026-06-11 ET` close 전이라 validation_lifecycle add-block이 없다는 점이다. immediate reconciliation 시점 주문 상태는 `new`, `filled_qty=0` open order다.

출처: [[2026-06-11-0431-hourly-autopilot]], `wiki/trade-ledger/orders/2026-06-11-0431-hourly-autopilot.json`, `wiki/trade-ledger/positions/2026-06-11-0431-hourly-autopilot-post-trade.json`
