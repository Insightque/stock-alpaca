---
symbol: MSFT
asset_type: stock
---

# MSFT

## 2026-06-05 hourly-autopilot

`MSFT` 1주 regular-session day limit buy가 `426.80 USD` limit으로 제출됐고, Alpaca MCP 기준 `2026-06-04T17:39:48.565193428Z`에 `426.78 USD`로 즉시 체결됐다. 근거는 scheduler core/research preflight와 strict universe/MCP/risk gate 통과, same-day duplicate가 없는 신규 mega-cap quality diversifier 후보, 그리고 runtime IEX quote `426.67/426.80` 기준 spread `0.0305%`가 policy 한도 이내였다는 점이다. Yahoo Finance recommendation snapshot은 `strongBuy 13`, `buy 40`, `hold 3`였고, news 요약에는 Microsoft in-house AI model 출시 맥락이 포함됐다. 이 체결은 새 validation lifecycle 표본으로 기록하며 1D/5D/20D review를 추적한다.

출처: [[2026-06-05-0231-hourly-autopilot]], `wiki/trade-ledger/positions/2026-06-05-0231-hourly-autopilot-post-trade.json`, `wiki/evidence-store/sources/2026-06-05-0231-hourly-autopilot-research-mcp-preflight.json`, `wiki/evidence-store/sources/2026-06-05-0231-hourly-autopilot-alpaca-core-preflight.json`, [[2026-06-04-portfolio-review]]

## 2026-06-11 04:39 KST hourly autopilot

2026-06-11 04:39 KST hourly autopilot에서 `MSFT` 1주 regular-session day limit add를 `398.38 USD` limit으로 제출했고, `2026-06-11 04:47 KST`(`2026-06-10T19:47:34.876997Z`)에 `398.38 USD`로 체결됐다. 근거는 scheduler-owned `0431` stale cleanup/core/research preflight 기준 hard gate pass, same-day duplicate/open-order conflict 부재, quote `398.32/398.38` spread `0.0151%`, active tradable NASDAQ stock, 그리고 `2026-06-06` portfolio review의 1D `중립` 이후 아직 `2026-06-11 ET` close 전이라 validation_lifecycle add-block이 없다는 점이다. `0451` close-boundary reconciliation 기준 보유 수량은 `1주 -> 2주`, `avg_entry_price=412.58`, open orders는 `0`건으로 정리됐다.

출처: [[2026-06-11-0431-hourly-autopilot]], [[2026-06-11-0451-hourly-autopilot]], `wiki/trade-ledger/orders/2026-06-11-0431-hourly-autopilot.json`, `wiki/trade-ledger/positions/2026-06-11-0431-hourly-autopilot-post-trade.json`, `wiki/trade-ledger/positions/2026-06-11-0451-hourly-autopilot-post-trade.json`


## 2026-06-16 03:39 KST hourly autopilot

2026-06-16 03:39 KST hourly autopilot에서 `MSFT` 1주 regular-session day limit add를 `399.55 USD` limit으로 제출했고, same client id reconciliation 기준 `2026-06-15T18:39:13.952806277Z`에 `398.71 USD`로 즉시 체결됐다. 근거는 scheduler-owned `0331` stale cleanup/core/research preflight 기준 hard gate pass, 직전 `0311` cycle `SO` buy fill 반영 후 open orders `0`, direct quote `398.63/399.55` spread `0.2303%`, same-day duplicate/open-order conflict 부재, 그리고 `AAPL/AMZN` weak-review history와 `SPY/QQQ` per-order cap 초과 이후 남은 가장 보수적인 executable mega-cap quality floor-size add였다는 점이다. immediate reconciliation 기준 보유 수량은 `3주 -> 4주`, `avg_entry_price=404.935`로 갱신됐다.

출처: [[2026-06-16-0331-hourly-autopilot]], `wiki/trade-ledger/orders/2026-06-16-0331-hourly-autopilot.json`, `wiki/trade-ledger/positions/2026-06-16-0331-hourly-autopilot-post-trade.json`, `wiki/evidence-store/sources/2026-06-16-0331-hourly-autopilot-research-mcp-preflight.json`, `wiki/evidence-store/sources/2026-06-16-0331-hourly-autopilot-alpaca-core-preflight.json`
