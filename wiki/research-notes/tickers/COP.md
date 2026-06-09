---
symbol: COP
asset_type: stock
---

# COP

## 2026-06-10 03:01 KST hourly-autopilot

`COP` 1주 regular-session day limit buy가 `116.14 USD` limit으로 제출됐고, Alpaca MCP 기준 `client_order_id=hourly-20260610-0251-buy-cop`, `order_id=34da84fa-1653-4852-a955-6a1e0efd3fa8`가 생성된 뒤 same client id reconciliation에서 `2026-06-09T18:00:39.436794108Z`에 `116.05 USD`로 즉시 체결됐다. 근거는 scheduler-owned `0251` stale cleanup/core/research preflight와 strict universe/MCP/risk gate 통과, `AVGO/RGTI` sell duplicate 및 `SO` trim metric gap 이후에도 learning_trade_directive가 최소 1건 validation order를 요구한다는 점, 그리고 `COP`가 2026-06-09 analyst review 기준 `2026-06-05 ET` fill 1D `+1.28%`, `SPY` 대비 `+1.04%p`, live IEX quote `116.09/116.14` spread `0.0431%`, same-day duplicate/open-order conflict 부재를 보여 energy/value diversifier fallback으로 가장 executable했다는 점이다.

출처: [[2026-06-10-0251-hourly-autopilot]], `wiki/trade-ledger/positions/2026-06-10-0251-hourly-autopilot-post-trade.json`

## 2026-06-06 01:37 KST hourly-autopilot

`COP` 1주 regular-session day limit buy가 `117.51 USD` limit으로 제출됐다. direct `get_order_by_client_id` 경로는 tool safety monitor가 막혔지만, post-submit Alpaca MCP `get_all_positions` 기준 `COP` 보유수량이 `2주 -> 3주`, 평균단가가 `117.06 -> 117.18`로 갱신돼 이번 1주 validation add가 약 `117.42 USD`에 체결된 것으로 추정 기록했다. 근거는 scheduler-owned stale cleanup/core/research preflight, strict universe/MCP/risk gate 통과, runtime IEX quote `117.49/117.51` 기준 spread `0.0170%`, 그리고 2026-06-05 portfolio review의 5D follow-through 양호다.

## 회고 기록

### 2026-05-30 analyst review cycle

2026-05-28 validation buy 1주는 114.95 USD 진입 대비 2026-05-29 close/current 114.36 USD로 -0.51%, SPY 대비 -0.71%p였다. 손실은 작지만 energy/value hedge 후보로서 1D 우위는 확인되지 않았다. 판단은 `중립 약함`이며 5D/20D 대기.

출처: [[2026-05-30-portfolio-review]], [[2026-05-30-0625-analyst-review-cycle-sources]]

### 2026-06-09 analyst review cycle

`2026-06-05 ET` fill 1D는 `117.42 USD -> 118.92 USD`로 `+1.28%`였다. `SPY` 대비 `+1.04%p`, `QQQ` 대비 `-0.24%p`라 broad risk-on을 거의 따라가면서 energy/value hedge 역할도 유지했다. 판단은 `양호`이며 5D에서도 energy sleeve가 계속 버티는지 확인한다.

출처: [[2026-06-09-portfolio-review]], [[2026-06-09-0623-analyst-review-cycle-sources]]
