---
symbol: BAC
asset_type: stock
---

# BAC

`BAC` 1주 regular-session day limit buy가 `53.92 USD` limit으로 제출됐고, Alpaca MCP 기준 `2026-06-05T13:39:42.716508022Z`에 `53.83 USD`로 체결됐다. 근거는 scheduler-owned `2231` core/research preflight와 strict universe/MCP/risk gate 통과, live BAC quote `53.90/53.92` 기준 spread `0.0371%`, same-day duplicate/open-order conflict 없음, 그리고 2026-06-05 portfolio review에서 financials diversification 5D 결과가 strongest cohort로 확인됐다는 점이다. 이 체결은 새 validation lifecycle 표본으로 기록하며 1D/5D/20D review를 추적한다.

## 2026-05-28 22:31 KST hourly autopilot

2026-05-28 22:31 KST hourly autopilot에서 BAC 1주 regular-session day limit buy를 제출했으나 post-trade reconciliation 기준 status `new`, filled_qty 0으로 open order다. financials cluster 분산 후보이며 open-order lifecycle gate에서 다음 run이 추적해야 한다.

출처: [[2026-05-28-2231-hourly-autopilot]], `wiki/trade-ledger/orders/2026-05-28-2231-hourly-autopilot.json`, `wiki/trade-ledger/positions/2026-05-28-2231-hourly-autopilot-post-trade.json`

## 회고 기록

### 2026-05-29 analyst review cycle

2026-05-27 validation buy 1주는 2026-05-28 close 기준 -2.38%로 SPY/QQQ 대비 부진했다. SEC EDGAR에서 2026-05-28 다수 424B2 filing이 확인됐지만 단기 매수 촉매로 보기는 약해 financials 분산 thesis는 5D/20D 확인 전 보류한다.

출처: [[2026-05-29-portfolio-review]], [[2026-05-29-0625-analyst-review-cycle-sources]]

### 2026-05-30 analyst review cycle

2026-05-28 validation buy 1주는 51.14 USD 진입 대비 2026-05-29 close/current 51.55 USD로 +0.80%, SPY 대비 +0.60%p였다. 2026-05-27 fill 1D 부진과 달리 이번 financials 분산 표본은 양호했다. 단일 1D 반전이라 정책 변경은 없다.

출처: [[2026-05-30-portfolio-review]], [[2026-05-30-0625-analyst-review-cycle-sources]]

### 2026-06-05 analyst review cycle

5D 기준으로는 financials 분산 thesis가 회복됐다. `2026-05-27` validation buy 1주는 52.06 USD 대비 54.11 USD로 +3.94%, `2026-05-28` validation buy 1주는 51.14 USD 대비 54.11 USD로 +5.81%였다. 두 표본 모두 `XLF`, SPY, QQQ를 앞질렀고 1D 약세만으로 failure로 단정하지 말아야 한다는 사례가 됐다.

출처: [[2026-06-05-portfolio-review]], [[2026-06-05-0627-analyst-review-cycle-sources]]
