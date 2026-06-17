---
symbol: NKE
asset_type: stock
---

# NKE

## 2026-06-17 23:41 KST hourly-autopilot

`NKE` 1주 regular-session day limit buy가 `45.30 USD` limit으로 제출됐다. scheduler-owned `2331` stale cleanup/core/research preflight와 live Alpaca submit-boundary check 기준 paper mode, market open, strict universe/MCP/risk gate, review backlog throttle, same-day duplicate/open-order conflict, fresh `FCX` open buy의 different-cluster 예외가 모두 통과했다. immediate reconciliation 기준 `client_order_id=hourly-20260617-2331-buy-nke`, `order_id=3f5cd1a0-cd69-48a6-8380-f9042cffd668`는 `status=new`, `filled_qty=0` open order이며 같은 readback에서 `FCX` prior open buy fill 전환도 함께 확인됐다.

출처: [[2026-06-17-2331-hourly-autopilot]], `wiki/trade-ledger/positions/2026-06-17-2331-hourly-autopilot-post-trade.json`

## 회고 기록

### 2026-05-29 analyst review cycle

2026-05-27 validation buy 1주는 2026-05-28 close 기준 +2.62%로 SPY/QQQ를 모두 상회했다. 1D 판단은 `양호`지만 Yahoo consensus가 hold-heavy라 5D/20D 확인 전 policy 승격 근거로 쓰지 않는다.

출처: [[2026-05-29-portfolio-review]], [[2026-05-29-0625-analyst-review-cycle-sources]]

### 2026-05-30 analyst review cycle

2026-05-28 validation buy 1주는 46.03 USD 진입 대비 2026-05-29 close/current 46.28 USD로 +0.54%, SPY 대비 +0.35%p였다. 2026-05-27 fill에 이어 1D 기준은 양호하지만 절대 초과폭은 작아 5D/20D 확인 전 policy 승격 근거로 쓰지 않는다.

출처: [[2026-05-30-portfolio-review]], [[2026-05-30-0625-analyst-review-cycle-sources]]

### 2026-05-31 analyst review cycle

2026-05-29 validation add 1주는 46.59 USD 체결 후 주말 현재 46.23 USD reference로 -0.77%지만, 다음 미국 정규장 close 전이라 1D 판단은 보류한다. Rebound thesis는 2026-06-01 close 이후 확인한다.

출처: [[2026-05-31-portfolio-review]], [[2026-05-31-0624-analyst-review-cycle-sources]]
### 2026-06-02 analyst review cycle

2026-05-29 validation add 1주는 46.59 USD 진입 대비 2026-06-01 close 45.92 USD로 -1.44%였다. 소비재/turnaround validation thesis는 1D에서 SPY/QQQ를 모두 밑돌아 `약함`으로 분류한다. 5D/20D 회고 대기.

출처: [[2026-06-02-portfolio-review]], [[2026-06-02-0624-analyst-review-cycle-sources]]
### 2026-06-04 analyst review cycle

2026-05-29 validation add 1주는 46.59 USD 진입 대비 2026-06-03 close 43.81 USD로 -5.97%였다. SPY/QQQ 대비 모두 크게 약해 consumer turnaround validation은 5D에서도 실패 쪽으로 기울었다. 판단은 `약함`, 20D 전 정책 승격 근거는 없다.

출처: [[2026-06-04-portfolio-review]], [[2026-06-04-0624-analyst-review-cycle-sources]]

## 2026-06-05 03:31 KST hourly autopilot

2026-06-05 03:31 KST hourly autopilot에서 `NKE` 1주 regular-session day limit buy를 제출했고, reconciliation 시점 상태는 `new` open order다. 근거는 scheduler research preflight shortlist 포함, runtime spread 0.0231%, same-day duplicate/open-order conflict 없음, consumer diversifier floor-size validation 목적이었다.


## 2026-06-11 02:38 KST hourly autopilot

2026-06-11 02:38 KST hourly autopilot에서 `NKE` 1주 regular-session day limit buy를 `43.99 USD`로 제출했고, immediate reconciliation 시점 상태는 `new` open order다. 근거는 scheduler research preflight shortlist 포함, live spread 0.0227%, same-day duplicate/open-order conflict 부재, consumer diversifier floor-size validation 목적이었다.

## 2026-06-16 02:18 KST hourly autopilot

`NKE` 1주 regular-session day limit buy가 `45.39 USD` limit으로 제출됐고, Alpaca MCP 기준 `client_order_id=hourly-20260616-0211-buy-nke`, `order_id=145242e1-6811-4542-af84-6df70f8b9727`가 `2026-06-15T17:18:03.494379872Z`에 `45.36 USD`로 즉시 체결됐다. 근거는 scheduler-owned `0211` stale cleanup/core/research preflight와 direct Alpaca submit-boundary check 기준 paper mode/market open/universe strict/MCP strict/risk strict가 모두 PASS했고, sell-first 재평가에서 `AVGO/RGTI` same-day sell duplicate와 `SO` trim metric gap 이후에도 learning_trade_directive가 최소 1건 validation order를 요구했다는 점, 그리고 `NKE`가 current research-preflight shortlist 유지, live quote `45.38/45.39` spread `0.0220%`, same-day duplicate/open-order conflict 부재, `2026-06-12` analyst review 기준 `+3.74%`, `SPY 대비 +2.02%p`의 최근 양호 표본을 제공했다는 점이다. 이 체결 후 runtime `get_all_positions` 기준 `NKE` 보유수량은 `5주 -> 6주`, 평균단가는 `45.228333 USD`로 갱신됐다.

출처: [[2026-06-16-0211-hourly-autopilot]], `wiki/trade-ledger/positions/2026-06-16-0211-hourly-autopilot-post-trade.json`

### 2026-06-12 analyst review cycle

`2026-06-10 ET` add 1주는 direct fill ledger 기준 `43.98 USD`에 체결됐고 `2026-06-11 ET` close/current `45.625 USD`로 `+3.74%`였다. `SPY` 대비 `+2.02%p`, `QQQ` 대비 `+0.47%p`라 consumer rebound 표본으로는 양호하다. 다만 기존 `2026-05-29` validation add 1D/5D가 약했던 이력이 있어 active rule 승격 전에는 더 많은 반복 표본이 필요하다.

출처: [[2026-06-12-portfolio-review]], [[2026-06-12-0632-analyst-review-cycle-sources]]
