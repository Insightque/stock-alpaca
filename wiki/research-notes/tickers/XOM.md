---
symbol: XOM
asset_type: stock
---

# XOM

## 2026-06-16 02:04 KST hourly-autopilot

`XOM` 1주 regular-session day limit buy가 `141.77 USD` limit으로 제출됐고, direct Alpaca MCP reconciliation 기준 `client_order_id=hourly-20260616-0151-buy-xom`, `order_id=5fc57083-5f45-432c-ad12-41bcac2f18b6`가 `2026-06-15T17:04:15.309154993Z`에 `141.76 USD`로 체결됐다. 근거는 scheduler-owned `0151` stale cleanup/core/research preflight 재사용, same-day duplicate/open-order conflict 부재, `XOM` direct quote `141.73/141.77` spread `0.0282%`, active tradable NYSE stock 확인, 그리고 `2026-06-11` portfolio review에서 energy diversifier validation 1D가 양호했다고 기록된 점이다. 이번 체결도 validation lifecycle 표본으로 `1D/5D/20D` review를 추가 추적한다.

출처: [[2026-06-16-0151-hourly-autopilot]], `wiki/trade-ledger/positions/2026-06-16-0151-hourly-autopilot-post-trade.json`

## 2026-06-05 00:51 KST hourly-autopilot

`XOM` 1주 regular-session day limit buy가 `153.41 USD` limit으로 제출됐고, Alpaca MCP 기준 `2026-06-04T16:02:05.40965797Z`에 `153.26 USD`로 즉시 체결됐다. 근거는 scheduler core/research preflight와 strict universe/MCP/risk gate 통과, same-day duplicate가 없는 기존 energy hedge/diversifier holding, 그리고 scheduler IEX quote `153.37/153.41` 기준 spread `0.0261%`가 policy 한도 이내였다는 점이다. 이 체결은 새 validation lifecycle 표본으로 기록하며 1D/5D/20D review를 추적한다.

출처: [[2026-06-05-0051-hourly-autopilot]], `wiki/trade-ledger/positions/2026-06-05-0051-hourly-autopilot-post-trade.json`

## 2026-06-10 04:39 KST hourly-autopilot

`XOM` 1주 regular-session day limit buy가 `148.40 USD` limit으로 제출됐고, direct Alpaca MCP reconciliation 기준 `2026-06-09T19:38:54.928294142Z`에 `148.35 USD`로 즉시 체결됐다. 근거는 scheduler-owned `0431` stale cleanup/core/research preflight 재사용, same-day duplicate/open-order conflict 부재, `XOM` live quote `148.36/148.40` spread `0.0270%`, active tradable NYSE stock 확인, 그리고 `2026-06-09` portfolio review에서 energy/value sleeve의 `COP/SLB` follow-through가 양호했다고 기록된 점이다. 이번 체결도 validation lifecycle 표본으로 1D/5D/20D review를 추가 추적한다.

출처: [[2026-06-10-0431-hourly-autopilot]], `wiki/trade-ledger/positions/2026-06-10-0431-hourly-autopilot-post-trade.json`

## 2026-06-11 00:11 KST hourly-autopilot

`XOM` 1주 regular-session day limit buy가 `151.66 USD` limit으로 제출됐고, direct Alpaca MCP reconciliation 기준 `client_order_id=hourly-20260611-0011-buy-xom`, `order_id=1878c01b-3d57-400d-a66c-b9cbbce4d237`가 `2026-06-10T15:20:38.691740279Z`에 `151.41 USD`로 즉시 체결됐다. 근거는 scheduler-owned `0011` stale cleanup/core/research preflight 재사용, regular market open과 open orders `0`건 재확인, `AVGO/RGTI` same-day sell duplicate 및 `SO` trim metric gap 이후에도 learning_trade_directive가 최소 1건 validation order를 요구한다는 점, 그리고 `XOM`이 existing energy diversifier로서 same-day duplicate/open-order conflict 부재, active tradable NYSE stock, live quote `151.45/151.66` spread `0.1385%`, research confirmation 4/5 usable/pass를 유지했다는 점이다. 이번 체결도 validation lifecycle 표본으로 `1D/5D/20D` review를 추가 추적한다.

출처: [[2026-06-11-0011-hourly-autopilot]], `wiki/trade-ledger/positions/2026-06-11-0011-hourly-autopilot-post-trade.json`

## 회고 기록

### 2026-05-29 analyst review cycle

2026-05-27 validation buy 1주는 2026-05-28 close 기준 -0.05%였다. 장중 MFE는 있었지만 종가 기준 우위는 없고, Iran ceasefire/nuclear-talk headline은 energy hedge thesis의 단기 변동 요인으로 기록한다.

출처: [[2026-05-29-portfolio-review]], [[2026-05-29-0625-analyst-review-cycle-sources]]

### 2026-05-30 analyst review cycle

2026-05-28 validation buy 1주는 148.37 USD 진입 대비 2026-05-29 close/current 145.38 USD로 -2.02%, SPY 대비 -2.21%p였다. 에너지/인플레이션 헤지 thesis는 1D에서 약했고, Iran/Hormuz headline에 따른 risk premium 변화가 주요 불확실성으로 남았다.

출처: [[2026-05-30-portfolio-review]], [[2026-05-30-0625-analyst-review-cycle-sources]]

### 2026-06-11 analyst review cycle

`2026-06-09 ET` buy 1주는 `148.35 USD` 진입 대비 `2026-06-10 ET` close `150.68 USD`로 `+1.57%`였다. `SPY` 대비 `+3.13%p`, `QQQ` 대비 `+3.57%p`로 energy diversifier validation은 `WMT/COP`와 함께 이번 1D cohort에서 양호했다. 다만 `2026-06-10 ET` 추가 fill `151.41 USD`는 새 1D horizon으로 넘긴다.

출처: [[2026-06-11-portfolio-review]], [[2026-06-11-0622-analyst-review-cycle-sources]]

## 2026-06-18 00:58 KST hourly autopilot

`XOM` 1주 regular-session day limit buy가 `141.54 USD` limit으로 제출됐고, immediate Alpaca MCP reconciliation 기준 `client_order_id=hourly-20260618-0051-buy-xom`, `order_id=9e6b4b81-1307-41aa-b9ac-5c34f7d51793`는 현재 `status=new` open order다. 근거는 scheduler-owned `0051` stale cleanup/core/research preflight 기준 hard gate pass, live continuity 기준 regular market open과 open orders `0` 재확인, `SO` trim metric gap 및 `RGTI/PFE` same-day duplicate sell gate 이후에도 learning_trade_directive가 최소 1건 validation order를 요구한다는 점, 그리고 `XOM`이 preflight-covered energy diversifier existing holding으로 same-day duplicate/open-order conflict 부재, live quote `141.50/141.54` spread `0.0283%`, `2026-06-17` portfolio review의 `1D 중립 양호` 이력, current invested ratio `0.7101`을 모두 충족해 가장 executable한 floor-size fallback이었기 때문이다. 다음 cycle에서는 fill 여부와 open-order lifecycle을 우선 추적한다.

출처: [[2026-06-18-0051-hourly-autopilot]], `wiki/trade-ledger/orders/2026-06-18-0051-hourly-autopilot.json`, `wiki/trade-ledger/positions/2026-06-18-0051-hourly-autopilot-post-trade.json`
