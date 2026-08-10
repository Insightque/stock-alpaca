---
symbol: GOOGL
asset_type: stock
---

# GOOGL

## 2026-06-05 hourly-autopilot

`GOOGL` 1주 regular-session day limit buy가 `372.48 USD` limit으로 제출됐고, Alpaca MCP 기준 `2026-06-04T17:21:28.345440863Z`에 `372.43 USD`로 즉시 체결됐다. 근거는 scheduler core/research preflight와 strict universe/MCP/risk gate 통과, same-day duplicate가 없는 기존 mega-cap quality holding, 그리고 runtime IEX quote `372.43/372.48` 기준 spread `0.0134%`가 policy 한도 이내였다는 점이다. 이 체결은 새 validation lifecycle 표본으로 기록하며 1D/5D/20D review를 추적한다.

## 회고 기록

### 2026-05-30 analyst review cycle

2026-05-28 validation buy 1주는 389.00 USD 진입 대비 2026-05-29 close/current 380.80 USD로 -2.11%, SPY 대비 -2.30%p였다. Mega-cap quality/AI 분산 목적은 유지되지만 이 1D 표본은 QQQ와 software follow-through를 따라가지 못했다. 판단은 `약함`이며 5D/20D 대기.

출처: [[2026-05-30-portfolio-review]], [[2026-05-30-0625-analyst-review-cycle-sources]]

### 2026-05-31 analyst review cycle

2026-05-29 validation add 1주는 383.13 USD 체결 후 주말 현재 380.34 USD reference로 -0.73%지만, 다음 미국 정규장 close 전이라 1D 판단은 보류한다. AI/hyperscaler thesis는 2026-06-01 close 이후 SPY/QQQ 대비로 재회고한다.

출처: [[2026-05-31-portfolio-review]], [[2026-05-31-0624-analyst-review-cycle-sources]]
### 2026-06-02 analyst review cycle

2026-05-29 validation add 1주는 383.13 USD 진입 대비 2026-06-01 close 376.26 USD로 -1.79%였다. AI tape가 강했지만 직접 AI infrastructure 수혜주보다 약했고, mega-cap quality label만으로는 1D edge가 부족했다. 판단은 `약함`, 5D/20D 대기.

출처: [[2026-06-02-portfolio-review]], [[2026-06-02-0624-analyst-review-cycle-sources]]
### 2026-06-04 analyst review cycle

2026-05-29 validation add 1주는 383.13 USD 진입 대비 2026-06-03 close 359.37 USD로 -6.20%였다. Alphabet capital raise/AI spend narrative가 있었지만 direct AI infrastructure leader 대비 상대성과가 크게 약했다. 판단은 `약함`, mega-cap quality 라벨만으로는 재매수 근거가 부족하다.

출처: [[2026-06-04-portfolio-review]], [[2026-06-04-0624-analyst-review-cycle-sources]]

### 2026-06-16 hourly-autopilot

2026-06-16 03:58 KST hourly autopilot에서 `GOOGL` 1주 regular-session day limit add를 `371.26 USD` limit으로 제출했고, same `client_order_id=hourly-20260616-0351-buy-googl` reconciliation 기준 `2026-06-15T18:58:47.524255326Z`에 `371.22 USD`로 즉시 체결됐다. 근거는 scheduler-owned `0351` stale cleanup/core/research preflight 기준 hard gate pass, same-day duplicate/open-order conflict 부재, preflight quote `371.21/371.26` spread `0.0135%`, SEC/FRED/Yahoo 3-provider positive confirmation, 그리고 `AAPL/AMZN` weak-review history와 `SPY/QQQ` per-order cap 초과 이후 남은 가장 보수적인 executable mega-cap quality floor-size add였다는 점이다. immediate reconciliation 기준 보유 수량은 `3주 -> 4주`, `avg_entry_price=378.945`로 갱신됐다.

출처: [[2026-06-16-0351-hourly-autopilot]], `wiki/trade-ledger/orders/2026-06-16-0351-hourly-autopilot.json`, `wiki/trade-ledger/positions/2026-06-16-0351-hourly-autopilot-post-trade.json`

## 2026-06-18 01:40 KST hourly-autopilot

`GOOGL` 1주 regular-session day limit buy가 `365.88 USD` limit으로 제출됐고, same `client_order_id=hourly-20260618-0131-buy-googl` reconciliation 기준 `2026-06-17T16:40:11.20362247Z`에 `365.24 USD`로 즉시 체결됐다. 근거는 scheduler-owned `0131` stale cleanup/core/research preflight 기준 hard gate pass, live continuity 기준 `AAPL` fill 이후 open orders `0` 재확인, `SO/RGTI/PFE` sell-first 경로가 각각 metric gap과 same-day duplicate sell gate로 막혔다는 점, 그리고 `GOOGL`이 same-day duplicate/open-order conflict가 없는 existing mega-cap quality holding으로 live quote `365.30/365.88` spread `0.1585%`, high source confidence, `2026-06-16` add evidence를 유지해 different-cluster fallback으로 가장 executable했다는 점이다. immediate reconciliation 기준 보유 수량은 `4주 -> 5주`, `avg_entry_price=376.204`로 갱신됐다.

출처: [[2026-06-18-0131-hourly-autopilot]], `wiki/trade-ledger/orders/2026-06-18-0131-hourly-autopilot.json`, `wiki/trade-ledger/positions/2026-06-18-0131-hourly-autopilot-post-trade.json`

### 2026-07-22 analyst review cycle

`2026-06-17 ET` add 1주는 `365.24 USD -> 342.06 USD`로 `-6.35%`다. 최근 Yahoo recommendation summary에는 `2026-07-21` Wells Fargo `Overweight / PT 438`, `2026-07-22` Citizens `Market Outperform / PT 515 유지`가 보이지만, 실제 tape는 아직 add 표본을 정당화하지 못한다. 현재 해석은 `mega-cap quality 유지`이되 `즉시 추가 매수 근거 부족`이다.

출처: [[2026-07-22-portfolio-review]], [[2026-07-22-analyst-review-cycle-sources]]

### 2026-07-24 analyst review cycle

`Friday, July 24, 2026 ET` close/current 기준 `GOOGL`은 `319.66 USD`로 평균단가 `376.204 USD` 대비 미실현 손실이 약 `-15.03%`다. quality/scale thesis 자체는 남지만 recent add cohort의 손실이 지속되고, 이번 run의 Yahoo recommendation summary query도 timeout이라 street support refresh를 검증하지 못했다. 따라서 현재 해석은 계속 `mega-cap quality 유지`이되 `immediate add 보류`다.

출처: [[2026-07-24-portfolio-review]], [[2026-07-24-analyst-review-cycle-sources]]

### 2026-07-25 analyst review cycle

`Saturday, July 25, 2026` review에서는 Yahoo recommendation summary `0m`가 `strongBuy=14`, `buy=44`, `hold=6`으로 여전히 강한 street support를 보인다는 점을 다시 확인했다. 그럼에도 Alpaca current `319.74 USD`는 평균단가 `376.204 USD` 대비 미실현 손실 약 `-15.01%` 구간이라 recent add cohort를 정당화하지 못한다. quality/scale thesis는 유지하되 immediate add는 계속 보류한다.

출처: [[2026-07-25-portfolio-review]], [[2026-07-25-analyst-review-cycle-sources]]

### 2026-08-10 analyst review cycle

`Monday, August 10, 2026 ET` close/current 기준 `GOOGL`은 `357.545/357.03 USD`로 7월 저점 대비 뚜렷이 회복했고 평균단가 `376.204 USD` 대비 손실도 약 `-4.96%`까지 줄었다. Alpaca news에서는 `2026-08-05` AI leadership exit headline으로 흔들린 뒤 `Gemini 3.5 Pro` 일정과 AI spending 관련 재평가가 이어졌다. quality/scale thesis 자체는 유지되지만, 이번 run에서는 외부 research MCP surface가 노출되지 않아 street confirmation을 새로 cross-check하지 못했다. 따라서 `회복 확인`으로는 보되 immediate add는 계속 보류한다.

출처: [[2026-08-10-portfolio-review]], [[2026-08-10-analyst-review-cycle-sources]]
