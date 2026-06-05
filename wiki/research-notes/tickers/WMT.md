---
symbol: WMT
asset_type: stock
---

# WMT

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
