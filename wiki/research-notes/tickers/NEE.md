---
symbol: NEE
asset_type: stock
---

# NEE

## 회고 기록

### 2026-05-29 analyst review cycle

2026-05-27 validation buy 1주는 2026-05-28 close 기준 -0.09%였다. 장중 MFE는 있었지만 종가 기준 벤치마크 우위가 없어 중립으로 두고 5D/20D를 확인한다.

출처: [[2026-05-29-portfolio-review]], [[2026-05-29-0625-analyst-review-cycle-sources]]

### 2026-05-30 analyst review cycle

2026-05-28 validation buy 1주는 87.83 USD 진입 대비 2026-05-29 close/current 87.28 USD로 -0.63%, SPY 대비 -0.82%p였다. Utility/defensive 분산 후보로는 1D 우위가 없었고 5D/20D 확인이 필요하다.

출처: [[2026-05-30-portfolio-review]], [[2026-05-30-0625-analyst-review-cycle-sources]]

### 2026-05-31 analyst review cycle

2026-05-29 validation add 1주는 86.46 USD 체결 후 주말 현재 87.01 USD reference로 +0.64%지만, 다음 미국 정규장 close 전이라 1D 판단은 보류한다. Utilities/defensive-yield thesis는 2026-06-01 close 이후 재회고한다.

출처: [[2026-05-31-portfolio-review]], [[2026-05-31-0624-analyst-review-cycle-sources]]
### 2026-06-02 analyst review cycle

2026-05-29 validation add 1주는 86.46 USD 진입 대비 2026-06-01 close 83.65 USD로 -3.25%였다. rate-sensitive utility/renewable defensive thesis는 1D에서 크게 약했고 FRED macro gap도 남아 있다. 판단은 `약함`, 5D/20D 대기.

출처: [[2026-06-02-portfolio-review]], [[2026-06-02-0624-analyst-review-cycle-sources]]
### 2026-06-04 analyst review cycle

2026-05-29 validation add 1주는 86.46 USD 진입 대비 2026-06-03 close 84.615 USD로 -2.13%였다. 1D 대비 손실은 줄었지만 rate-sensitive utility/renewable defensive thesis는 5D에서도 benchmark를 하회했다. 판단은 `약함`, 20D review 전 add 보류가 맞다.

출처: [[2026-06-04-portfolio-review]], [[2026-06-04-0624-analyst-review-cycle-sources]]

## 2026-06-06 02:44 KST hourly autopilot

`NEE` 1주 regular-session day limit buy가 `85.47 USD` limit으로 제출됐다. 첫 `place_stock_order`는 safety cancellation으로 반환됐지만, 동일 `client_order_id=hourly-20260606-0231-buy-nee` 기준 `get_order_by_client_id` 404와 symbol-scoped `get_orders(status=all)` 0건을 확인한 뒤 1회만 재시도해 Alpaca order id `202d7a0d-c061-4385-a693-b91f403a2b4f`를 생성했다. immediate reconciliation 기준 `get_order_by_client_id`, `get_order_by_id`, `get_orders(status=all, symbols=NEE, after=2026-06-05T17:40:00Z)`는 동일 주문을 `status=new`, `filled_qty=0` open order로 확인했다. 근거는 scheduler-owned `0231` core/research preflight와 strict universe/MCP/risk gate 통과, FRED macro confirmation 유지, same-day duplicate/open-order conflict 없음, Yahoo recommendations breadth usable, utilities diversifier floor-size validation 목적이었다.

출처: [[2026-06-06-0231-hourly-autopilot]], `wiki/trade-ledger/positions/2026-06-06-0231-hourly-autopilot-post-trade.json`


## 2026-06-11 02:18 KST hourly-autopilot

`NEE` 1주 regular-session day limit buy가 `85.29 USD` limit으로 제출됐고, Alpaca MCP 기준 `client_order_id=hourly-20260611-0211-buy-nee`, `order_id=7fd2a9cf-bde9-454e-83f0-64a8a722409d`가 생성된 뒤 same client id reconciliation에서 `2026-06-10T17:18:05.301779Z`에 `85.22 USD`로 즉시 체결됐다. 근거는 scheduler-owned `0211` stale cleanup/core/research preflight와 live Alpaca MCP submit-boundary check 기준 paper mode/market open/universe strict/MCP strict/risk strict 모두 통과했고, sell-first 재평가 뒤 same-day duplicate가 없는 utilities/rate-sensitive diversifier 중 `NEE`가 FRED macro confirmation을 유지한 가장 보수적인 floor-size learning buy였다는 점이다.

출처: [[2026-06-11-0211-hourly-autopilot]], `wiki/trade-ledger/positions/2026-06-11-0211-hourly-autopilot-post-trade.json`

### 2026-06-14 analyst review cycle

토요일 Alpaca clock 기준 새 미국 정규장 close가 없어 skipped recommendation 재점검만 수행했다. current snapshot 기준 `NEE`는 `5주`, 평균단가 `86.44 USD`, current `85.99 USD`, 미실현 약 `-0.52%`로 급한 missed upside는 아니며, `2026-06-13` cycle의 backlog throttle 해석을 뒤집을 새 근거는 없다.

출처: [[2026-06-14-portfolio-review]], [[2026-06-14-0623-analyst-review-cycle-sources]]

### 2026-06-15 analyst review cycle

일요일 closed clock 기준 새 미국 정규장 close는 없고, skipped recommendation 재점검만 carry-forward했다. current snapshot 기준 `NEE`는 `5주`, 평균단가 `86.44 USD`, current `85.99 USD`, 미실현 약 `-0.52%`이며 Alpaca IEX daily bar는 전일 대비 `+1.30%`였다. defensive tape는 안정적이지만 backlog throttle 우선순위를 뒤집을 정도의 missed-upside는 아니어서 기존 해석을 유지한다.

출처: [[2026-06-15-portfolio-review]], [[2026-06-15-0624-analyst-review-cycle-sources]]
