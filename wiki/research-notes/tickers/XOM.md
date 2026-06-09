---
symbol: XOM
asset_type: stock
---

# XOM

## 2026-06-05 00:51 KST hourly-autopilot

`XOM` 1주 regular-session day limit buy가 `153.41 USD` limit으로 제출됐고, Alpaca MCP 기준 `2026-06-04T16:02:05.40965797Z`에 `153.26 USD`로 즉시 체결됐다. 근거는 scheduler core/research preflight와 strict universe/MCP/risk gate 통과, same-day duplicate가 없는 기존 energy hedge/diversifier holding, 그리고 scheduler IEX quote `153.37/153.41` 기준 spread `0.0261%`가 policy 한도 이내였다는 점이다. 이 체결은 새 validation lifecycle 표본으로 기록하며 1D/5D/20D review를 추적한다.

출처: [[2026-06-05-0051-hourly-autopilot]], `wiki/trade-ledger/positions/2026-06-05-0051-hourly-autopilot-post-trade.json`

## 2026-06-10 04:39 KST hourly-autopilot

`XOM` 1주 regular-session day limit buy가 `148.40 USD` limit으로 제출됐고, direct Alpaca MCP reconciliation 기준 `2026-06-09T19:38:54.928294142Z`에 `148.35 USD`로 즉시 체결됐다. 근거는 scheduler-owned `0431` stale cleanup/core/research preflight 재사용, same-day duplicate/open-order conflict 부재, `XOM` live quote `148.36/148.40` spread `0.0270%`, active tradable NYSE stock 확인, 그리고 `2026-06-09` portfolio review에서 energy/value sleeve의 `COP/SLB` follow-through가 양호했다고 기록된 점이다. 이번 체결도 validation lifecycle 표본으로 1D/5D/20D review를 추가 추적한다.

출처: [[2026-06-10-0431-hourly-autopilot]], `wiki/trade-ledger/positions/2026-06-10-0431-hourly-autopilot-post-trade.json`

## 회고 기록

### 2026-05-29 analyst review cycle

2026-05-27 validation buy 1주는 2026-05-28 close 기준 -0.05%였다. 장중 MFE는 있었지만 종가 기준 우위는 없고, Iran ceasefire/nuclear-talk headline은 energy hedge thesis의 단기 변동 요인으로 기록한다.

출처: [[2026-05-29-portfolio-review]], [[2026-05-29-0625-analyst-review-cycle-sources]]

### 2026-05-30 analyst review cycle

2026-05-28 validation buy 1주는 148.37 USD 진입 대비 2026-05-29 close/current 145.38 USD로 -2.02%, SPY 대비 -2.21%p였다. 에너지/인플레이션 헤지 thesis는 1D에서 약했고, Iran/Hormuz headline에 따른 risk premium 변화가 주요 불확실성으로 남았다.

출처: [[2026-05-30-portfolio-review]], [[2026-05-30-0625-analyst-review-cycle-sources]]
