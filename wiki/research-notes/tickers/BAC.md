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

### 2026-06-09 analyst review cycle

`2026-06-05 ET` fill 1D는 `53.83 USD -> 53.59 USD`로 `-0.45%`였다. `SPY` 대비 `-0.69%p`, `QQQ` 대비 `-1.96%p`지만 financials benchmark `XLF -0.59%`보다는 약간 나았다. 첫날 큰 alpha는 없었어도 financials diversifier 표본으로는 `중립 양호`다.

출처: [[2026-06-09-portfolio-review]], [[2026-06-09-0623-analyst-review-cycle-sources]]

## 2026-06-10 23:39 KST hourly-autopilot

`BAC` 1주 regular-session day limit buy가 `54.85 USD` limit으로 제출됐고, Alpaca MCP 기준 `client_order_id=hourly-20260610-2331-buy-bac`, `order_id=544dec18-dc40-499f-9085-e5ad37b50fef`가 생성된 뒤 same order id reconciliation에서 `2026-06-10T14:39:03.058660726Z`에 `54.77 USD`로 즉시 체결됐다. 근거는 scheduler-owned `2331` stale cleanup/core/research preflight와 strict universe/MCP/risk gate 통과, sell-first 평가에서 `RGTI/AVGO` same-day sell duplicate와 `SO` trim metric gap으로 executable trim이 남지 않았다는 점, `WMT` same-day buy duplicate와 `SPY/QQQ` per-order cap 초과 이후에도 learning_trade_directive가 최소 1건 validation order를 요구한다는 점, 그리고 `BAC`가 기존 financials diversifier holding으로서 Yahoo recommendation breadth 우호, SEC/FRED/Firecrawl/Yahoo positive confirmation 유지, live quote `54.84/54.85` spread `0.0182%`, same-day duplicate/open-order conflict 부재를 보여 가장 executable했다는 점이다. 이 체결은 새 validation lifecycle 표본으로 기록하며 `1D/5D/20D` review를 추적한다.

출처: [[2026-06-10-2331-hourly-autopilot]], `wiki/trade-ledger/positions/2026-06-10-2331-hourly-autopilot-post-trade.json`

### 2026-06-11 analyst review cycle

`2026-06-09 ET` buy 1주는 `54.07 USD` 진입 대비 `2026-06-10 ET` close `54.54 USD`로 `+0.87%`였다. `SPY` 대비 `+2.43%p`, `QQQ` 대비 `+2.87%p`라 financials diversifier validation은 down tape에서 오히려 양호했다. 단일 1D 표본이라 정책 승격은 없지만, `2026-06-10 ET` 추가 fill `54.77 USD`는 다음 1D horizon 대기로 넘긴다.

출처: [[2026-06-11-portfolio-review]], [[2026-06-11-0622-analyst-review-cycle-sources]]

### 2026-06-12 analyst review cycle

`2026-06-10 ET` add 1주는 `54.77 USD` 진입 대비 `2026-06-11 ET` close/current `55.20 USD`로 `+0.79%`였다. broad rebound 장세에서는 `SPY/QQQ`를 이기지 못했지만, `2026-06-05 ET` fill 5D `+2.55%`와 합치면 financials diversifier 표본은 여전히 가장 안정적인 축에 속한다. 공격적 승격 근거는 아니어도 hold-quality는 유지된다.

출처: [[2026-06-12-portfolio-review]], [[2026-06-12-0632-analyst-review-cycle-sources]]

### 2026-06-13 analyst review cycle

`2026-06-05 ET` fill 5D는 `53.83 USD -> 55.99 USD`로 `+4.01%`였다. `SPY` 대비 `+3.44%p`, `QQQ` 대비 `+1.75%p`라 이번 cycle에서도 financials diversifier 표본은 가장 안정적인 축을 유지했다. 단일 섹터 승격보다 `hold-quality` 강화 근거로 쓰는 편이 적절하다.

출처: [[2026-06-13-portfolio-review]], [[2026-06-13-0622-analyst-review-cycle-sources]]


## 2026-06-15 23:20 KST hourly-autopilot

`BAC` 1주 regular-session day limit buy가 `56.28 USD` limit으로 제출됐고, Alpaca MCP 기준 `client_order_id=hourly-20260615-2311-buy-bac`, `order_id=dda6e628-c48f-48b5-891e-2bc6169bba6c`가 생성됐다. immediate reconciliation 시점 상태는 `new` open order이며 fill은 아직 없다. 근거는 scheduler-owned `2311` stale cleanup/core/research preflight와 strict universe/MCP/risk gate 통과, `AVGO` fresh open sell 1주와 `RGTI` same-session filled sell 9주 때문에 sell-first 경로가 explicit gate에 막혔다는 점, 그리고 `BAC`가 same-day duplicate/open-order conflict 없는 financials diversifier floor-size fallback으로 가장 executable했다는 점이다. 다음 cycle은 이 주문의 fill 또는 stale lifecycle을 추적한다.

출처: [[2026-06-15-2311-hourly-autopilot]], `wiki/trade-ledger/positions/2026-06-15-2311-hourly-autopilot-post-trade.json`
