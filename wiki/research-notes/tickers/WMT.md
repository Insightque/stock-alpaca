---
symbol: WMT
asset_type: stock
---

# WMT

## 2026-06-10 02:19 KST hourly-autopilot

`WMT` 1주 regular-session day limit buy가 `118.84 USD` limit으로 제출됐고, Alpaca MCP 기준 `client_order_id=hourly-20260610-0211-buy-wmt`, `order_id=40066752-96cc-4225-aa77-0e6ba6c7ccb3`가 생성된 뒤 same client id reconciliation에서 `2026-06-09T17:19:41.414935036Z`에 `118.70 USD`로 즉시 체결됐다. 근거는 scheduler-owned `0211` stale cleanup/core/research preflight와 strict universe/MCP/risk gate 통과, `AVGO/RGTI` sell duplicate 및 `SO` trim metric gap 이후에도 learning_trade_directive가 최소 1건 validation order를 요구한다는 점, 그리고 `WMT`가 same-day duplicate/open-order conflict 없이 최근 1D review `중립 양호`, Yahoo recommendation breadth 우호, preflight quote `118.79/118.84` spread `0.0421%`를 보여 defensive diversifier fallback으로 가장 executable했다는 점이다.

출처: [[2026-06-10-0211-hourly-autopilot]], `wiki/trade-ledger/positions/2026-06-10-0211-hourly-autopilot-post-trade.json`

## 2026-06-05 23:11 KST hourly-autopilot

`WMT` 1주 regular-session day limit buy가 `120.50 USD` limit으로 제출됐고, Alpaca MCP 기준 첫 submit 시도는 runtime safety cancellation으로 반환됐지만 동일 `client_order_id=hourly-20260605-2311-buy-wmt` 기준 404/0건 reconciliation 후 1회만 재시도해 `2026-06-05T14:17:18.858272769Z`에 `119.78 USD`로 즉시 체결됐다. 근거는 scheduler-owned `2311` core/research preflight와 strict universe/MCP/risk gate 통과, same-day duplicate/open-order conflict 없음, scheduler quote `120.45/120.50` 기준 spread `0.0415%`, 그리고 2026-06-05 portfolio review에서 defensive cohort 전반은 약했지만 `WMT` 개별 5D 평가는 `중립 양호`로 회복했다는 점이다. 이 체결은 새 validation lifecycle 표본으로 기록하며 1D/5D/20D review를 추적한다.

출처: [[2026-06-05-2311-hourly-autopilot]], `wiki/trade-ledger/positions/2026-06-05-2311-hourly-autopilot-post-trade.json`

## 2026-06-05 01:11 KST hourly-autopilot

`WMT` 1주 regular-session day limit buy가 `118.40 USD` limit으로 제출됐고, Alpaca MCP 기준 `2026-06-04T16:20:17.746749451Z`에 `118.36 USD`로 즉시 체결됐다. 근거는 scheduler core/research preflight와 strict universe/MCP/risk gate 통과, same-day duplicate가 없는 기존 defensive holding, 그리고 runtime IEX quote `118.37/118.40` 기준 spread `0.0253%`가 policy 한도 이내였다는 점이다. 이 체결은 새 validation lifecycle 표본으로 기록하며 1D/5D/20D review를 추적한다.

출처: [[2026-06-05-0111-hourly-autopilot]], `wiki/trade-ledger/positions/2026-06-05-0111-hourly-autopilot-post-trade.json`

## 회고 기록

### 2026-05-29 analyst review cycle

2026-05-27 validation buy 1주는 2026-05-28 close 기준 +0.49%로 거의 SPY와 유사하고 QQQ를 하회했다. Defensive consumer 후보로 중립 평가하며 5D/20D 회고를 기다린다.

출처: [[2026-05-29-portfolio-review]], [[2026-05-29-0625-analyst-review-cycle-sources]]

### 2026-05-30 analyst review cycle

2026-05-28 validation buy 1주는 118.63 USD 진입 대비 2026-05-29 close/current 115.79 USD로 -2.39%, SPY 대비 -2.59%p였다. 소비 방어/quality 라벨은 AI-led risk-on 장세에서 1D 방어력을 주지 못했다. 5D에서도 반복되면 defensive 후보의 price confirmation 강화 가설로 남긴다.

출처: [[2026-05-30-portfolio-review]], [[2026-05-30-0625-analyst-review-cycle-sources]]

### 2026-05-31 analyst review cycle

2026-05-29 validation add 1주는 115.00 USD 체결 후 주말 현재 115.75 USD reference로 +0.65%지만, 다음 미국 정규장 close 전이라 1D 판단은 보류한다. Defensive retail thesis와 Yahoo의 buy-the-dip/healthcare-logistics 확장 맥락은 2026-06-01 close 이후 재점검한다.

출처: [[2026-05-31-portfolio-review]], [[2026-05-31-0624-analyst-review-cycle-sources]]
### 2026-06-02 analyst review cycle

2026-05-29 validation add 1주는 115.00 USD 진입 대비 2026-06-01 close 114.57 USD로 -0.37%였다. target raise headline은 있었지만 SPY/QQQ 대비 약해 defensive/quality retail validation은 `중립 약함`으로 본다. 5D/20D 대기.

출처: [[2026-06-02-portfolio-review]], [[2026-06-02-0624-analyst-review-cycle-sources]]
### 2026-06-04 analyst review cycle

2026-05-29 validation add 1주는 115.00 USD 진입 대비 2026-06-03 close 116.93 USD로 +1.68%였다. SPY 대비 +1.96%p, QQQ 대비 +0.87%p로 5D는 `중립 양호`까지 회복했다. 다만 defensive retail의 구조적 edge가 확인된 수준은 아니라 20D 확인이 필요하다.

출처: [[2026-06-04-portfolio-review]], [[2026-06-04-0624-analyst-review-cycle-sources]]

### 2026-06-09 analyst review cycle

`2026-06-05 ET` fill 1D는 `119.78 USD -> 119.83 USD`로 `+0.04%`였다. 절대수익은 거의 없지만 `SPY` 대비 `-0.20%p`, `QQQ` 대비 `-1.47%p`로 defensive retail 특유의 downside control은 유지됐다. 판단은 `중립 양호`이며 stronger alpha는 5D에서 다시 확인한다.

출처: [[2026-06-09-portfolio-review]], [[2026-06-09-0623-analyst-review-cycle-sources]]

### 2026-06-11 analyst review cycle

`2026-06-09 ET` buy 1주는 `118.70 USD` 진입 대비 `2026-06-10 ET` close `120.56 USD`로 `+1.57%`였다. `SPY` 대비 `+3.13%p`, `QQQ` 대비 `+3.57%p`로 defensive retail validation은 이번 1D에서 분명히 양호했다. 다만 `2026-06-10 ET` regular-session 추가 fill `118.49 USD`가 새로 생겨 다음 1D horizon을 별도로 추적한다.

출처: [[2026-06-11-portfolio-review]], [[2026-06-11-0622-analyst-review-cycle-sources]]

### 2026-06-17 analyst review cycle

`2026-06-15 ET` add 1주는 `120.20 USD -> 121.07 USD`로 `+0.72%`였다. `SPY`와 `QQQ`가 하락한 날에 defensive retail이 방어적으로 작동해 1D closeout은 `양호`다. 다만 skipped recommendation 관점에서는 급한 missed-upside 사례로 보긴 어려워, defensive backlog throttle 해석을 바꿀 정도의 새 정책 신호로는 쓰지 않는다.

출처: [[2026-06-17-portfolio-review]], [[2026-06-17-0623-analyst-review-cycle-sources]]

## 2026-06-17 22:59 KST hourly-autopilot

`WMT` 1주 regular-session day limit buy가 `119.83 USD` limit으로 제출됐다. scheduler-owned `2251` stale cleanup/core/research preflight와 live Alpaca submit-boundary check 기준 paper mode, market open, strict universe/MCP/risk gate, review backlog throttle, same-day duplicate/open-order conflict, quote freshness가 모두 통과했고, `BAC`는 같은 미국 거래일 2231 fill로 duplicate buy gate가 생겼으며 `PFE/RGTI/SO` sell-first 경로도 각각 duplicate/spread/metric gate에 막혀 있었다. immediate reconciliation 기준 `client_order_id=hourly-20260617-2251-buy-wmt`, `order_id=381c1f40-067a-4c71-99e6-c57ab92dd6e6`는 `status=new`, `filled_qty=0` open order이며 `get_all_positions` 기준 보유수량은 아직 `9주`, `qty_available=9`로 unchanged다. 해석은 `defensive retail floor-size validation add submit 완료, next cycle fill/open-order lifecycle 추적 필요`다.

출처: [[2026-06-17-2251-hourly-autopilot]], `wiki/trade-ledger/positions/2026-06-17-2251-hourly-autopilot-post-trade.json`

### 2026-06-18 analyst review cycle

`2026-06-10 ET` add 1주는 `118.49 USD -> 118.185 USD`로 `-0.26%`였다. 절대수익은 미세한 음수지만 `SPY -1.27%`, `QQQ -1.01%` 대비 방어는 유지돼 defensive retail validation 해석은 `중립 양호`로 닫는다.

출처: [[2026-06-18-portfolio-review]], [[2026-06-18-0621-analyst-review-cycle-sources]]

### 2026-08-16 analyst review cycle

`Sunday, August 16, 2026 ET` carry-forward review에서는 skipped recommendation 관점에서 `WMT`를 다시 확인했다. `Friday, July 24, 2026 ET` close `109.46 USD` 대비 `Friday, August 14, 2026 ET` close `115.27 USD`로 약 `+5.31%`였지만, 이 정도 후행 성과만으로 당시 source-of-record quote discipline을 policy miss로 뒤집을 수준은 아니다. 다음 주 earnings-volatility headline도 hindsight add 정당화보다 변동성 경계에 가깝다. 따라서 이번 cycle의 판단은 `gate-correct skip 유지`다.

출처: [[2026-08-16-portfolio-review]], [[2026-08-16-analyst-review-cycle-sources]]
