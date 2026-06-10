---
symbol: AMZN
asset_type: stock
---

# AMZN

## 2026-06-11 01:41 KST hourly autopilot

`AMZN` 1주 regular-session day limit buy가 `239.33 USD` limit으로 제출됐고, Alpaca MCP 기준 `client_order_id=hourly-20260611-0131-buy-amzn`, `order_id=d23787d5-be1a-4b35-a08e-b43670b24265`가 생성됐다. same client/order id reconciliation 시점 상태는 `new` open order이며 `filled_qty=0`이다. 근거는 scheduler-owned `0131` stale cleanup/core/research preflight와 live Alpaca MCP submit-boundary check 기준 paper mode/market open/universe strict/MCP strict/risk strict 모두 통과했고, sell-first 재평가에서 `AVGO/RGTI` same-day sell duplicate와 `SO` trim metric gap 이후에도 learning_trade_directive가 최소 1건 validation order를 요구한다는 점, 그리고 `AMZN`이 same-day duplicate/open-order conflict 없이 live quote `239.00/239.33` spread `0.1379%`, research preflight coverage 유지, mega-cap AI/cloud different-cluster fallback 역할을 제공했다는 점이다.

출처: [[2026-06-11-0131-hourly-autopilot]], `wiki/trade-ledger/positions/2026-06-11-0131-hourly-autopilot-post-trade.json`

## 2026-06-10 03:38 KST hourly autopilot

`AMZN` 1주 regular-session day limit buy가 `245.48 USD` limit으로 제출됐고, Alpaca MCP 기준 `client_order_id=hourly-20260610-0331-buy-amzn`, `order_id=7a783061-253f-4c53-8c0e-377e194c469e`가 생성된 뒤 same client id reconciliation에서 `2026-06-09T18:38:03.133912338Z`에 `245.40 USD`로 즉시 체결됐다. 근거는 scheduler-owned `0331` stale cleanup/core/research preflight와 strict universe/MCP/risk gate 통과, fresh `NVDA` open buy가 같은 AI cluster 추가만 차단하고 다른 cluster buy는 막지 않았다는 점, `AVGO/RGTI` sell duplicate 및 `SO` trim metric gap 이후에도 learning_trade_directive가 최소 1건 validation order를 요구한다는 점, 그리고 `AMZN`이 preflight research coverage를 유지하면서 same-day duplicate/open-order conflict 없이 live quote `245.43/245.48` spread `0.0204%`를 보여 different-cluster mega-cap AI/cloud fallback으로 가장 executable했다는 점이다.

출처: [[2026-06-10-0331-hourly-autopilot]], `wiki/trade-ledger/positions/2026-06-10-0331-hourly-autopilot-post-trade.json`

## 2026-06-06 01:51 KST hourly autopilot

`AMZN` 1주 regular-session day limit buy가 `253.17 USD` limit으로 제출됐고, Alpaca MCP 기준 `2026-06-05T17:01:54.545263432Z`에 `253.17 USD`로 체결됐다. 근거는 scheduler core/research preflight와 strict universe/MCP/risk gate 통과, same-day duplicate가 없는 기존 mega-cap AI/cloud holding, 그리고 preflight IEX quote `253.12/253.17` 기준 spread `0.0197%`가 policy 한도 이내였다는 점이다. 최근 5D review 약세는 남아 있지만 hard gates가 모두 통과한 상태에서 learning_trade_directive floor-size observation을 우선해 새 validation lifecycle 표본으로 기록한다.

## 회고 기록

### 2026-05-29 analyst review cycle

2026-05-27 validation buy 1주는 2026-05-28 close 기준 +1.45%로 SPY/QQQ를 상회했다. Alpaca/Yahoo news의 AWS, AI data infrastructure 맥락과 가격 follow-through가 맞았으나 1D 표본이므로 정책 변경은 보류한다.

출처: [[2026-05-29-portfolio-review]], [[2026-05-29-0625-analyst-review-cycle-sources]]

### 2026-05-30 analyst review cycle

2026-05-28 validation buy 1주는 270.55 USD 진입 대비 2026-05-29 close/current 270.62 USD로 +0.03%, SPY 대비 -0.17%p였다. Mega-cap AI/cloud thesis는 유지하지만 이번 add의 1D 결과는 중립이다.

출처: [[2026-05-30-portfolio-review]], [[2026-05-30-0625-analyst-review-cycle-sources]]

### 2026-05-31 analyst review cycle

2026-05-29 validation add 1주는 272.76 USD 체결 후 주말 현재 270.64 USD reference로 -0.78%지만, 다음 미국 정규장 close 전이라 1D 판단은 보류한다. AI/cloud thesis는 유지하되 2026-06-01 close 이후 SPY/QQQ 대비로 재회고한다.

출처: [[2026-05-31-portfolio-review]], [[2026-05-31-0624-analyst-review-cycle-sources]]
### 2026-06-02 analyst review cycle

2026-05-29 validation add 1주는 272.76 USD 진입 대비 2026-06-01 close 261.20 USD로 -4.24%였다. SPY +0.28%, QQQ +0.59% 대비 모두 약해 mega-cap quality/AI infrastructure label만으로는 1D edge가 부족했다. 판단은 `약함`이며 5D/20D 대기.

출처: [[2026-06-02-portfolio-review]], [[2026-06-02-0624-analyst-review-cycle-sources]]
### 2026-06-04 analyst review cycle

2026-05-29 validation add 1주는 272.76 USD 진입 대비 2026-06-03 close 249.99 USD로 -8.35%였다. SPY 대비 -8.06%p, QQQ 대비 -9.16%p라서 mega-cap quality/AI adjacency thesis는 5D에서도 약했다. 판단은 `약함`이며 20D 전까지 add 근거로 쓰지 않는다.

출처: [[2026-06-04-portfolio-review]], [[2026-06-04-0624-analyst-review-cycle-sources]]

### 2026-06-09 analyst review cycle

`2026-06-05 ET` fill 1D는 `253.17 USD -> 245.21 USD`로 `-3.14%`였다. `SPY` 대비 `-3.39%p`, `QQQ` 대비 `-4.66%p`라 mega-cap quality/AI cloud thesis의 immediate follow-through는 약했다. 판단은 `약함`이며 기존 quality label만으로 add cadence를 빠르게 가져가면 안 된다는 표본으로 남긴다.

출처: [[2026-06-09-portfolio-review]], [[2026-06-09-0623-analyst-review-cycle-sources]]
