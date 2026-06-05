---
id: AVGO
updated_at: 2026-06-05T18:43:00Z
symbol: AVGO
asset_type: stock
---

# AVGO

## 현재 Thesis

AVGO는 Broadcom으로, AI chip bottleneck과 AMAT partnership 뉴스가 있는 AI 반도체 인프라 후보다. 최신 체결가 414.84는 전일 종가 414.32와 거의 비슷해 당일 추세는 강하지 않지만, 뉴스 촉매와 AI 공급망 내 위치가 좋아 업데이트된 계획에 포함한다.

## 추세

- 일간: 보합.
- 주간: 변동성 있는 횡보.
- 월간: AI 반도체 테마 안에서 상대적으로 안정적.

## 촉매

- AI chip bottleneck 대응.
- AMAT partnership 뉴스.
- AI 인프라 수요.

## 리스크

- 당일 모멘텀은 NVDA/AMD보다 약하다.
- IEX 호가 스프레드가 넓게 보였으므로 실제 주문 전 fresh quote가 중요하다.

## 포트폴리오 맥락

- 현재 노출: 0%.
- 제안 역할: AI 반도체 인프라 후보.
- 제안 주문: 15주, 지정가 414.85, 예상 6222.75 USD.
- 현재 조치: 주문 제출 없음.

## 점수

- 점수: 77/100
- 신뢰도: 중간

## 출처

- [[2026-05-22-expanded-stock-review-alpaca]]

## 거래 기록

- 2026-05-22: paper 매수 15주가 평균 410.73 USD에 체결됐다.
- 2026-06-01: after-hours validation buy 1주가 평균 461.26 USD에 체결됐다.
- 2026-06-06 03:37 KST: scheduled hourly-autopilot에서 risk-reducing trim 4주가 `389.25 USD`에 체결됐다.
- 주문/체결 출처: [[2026-05-22-paper-order-submission]]

## 회고 기록

- 2026-05-27: [[2026-05-27-portfolio-review]]에서 2026-05-22 stock-only 매수 1D interim review를 작성했다. AVGO는 410.73 USD 진입 대비 Alpaca 현재가 422.50 USD, 미실현 +2.87%였다. AI 인프라 thesis는 유효하지만 AMD/LRCX보다 1D follow-through는 약했다.
### 2026-06-02 analyst review cycle

2026-05-22 stock-only cohort는 410.73 USD 진입 대비 2026-06-01 close 460.09 USD로 +12.02%였다. AI semiconductor/infrastructure thesis는 5D에서 강했다. 별도로 2026-06-01 after-hours validation 1주는 461.26 USD 진입 대비 첫 regular close 460.09 USD로 -0.25%라 판단 보류이며, earnings-preview narrative는 1D/5D 확인 전 add 근거로 쓰지 않는다.

출처: [[2026-06-02-portfolio-review]], [[2026-06-02-0624-analyst-review-cycle-sources]]
### 2026-06-04 analyst review cycle

2026-06-01 after-hours validation 1주는 461.26 USD 진입 대비 2026-06-03 close 478.62 USD로 +3.76%였다. SPY 대비 +4.33%p, QQQ 대비 +3.55%p라 first-close validation 자체는 `양호`다. 다만 Yahoo Finance 기준 post-market price가 425.30 USD까지 밀려 earnings event risk가 남았으므로, 즉시 add 규칙으로 승격하지 않고 5D/20D를 더 본다.

출처: [[2026-06-04-portfolio-review]], [[2026-06-04-0624-analyst-review-cycle-sources]]

### 2026-06-05 analyst review cycle

2026-06-04 미국 정규장에서는 earnings-event 재평가로 close 417.99 USD, 당일 -12.78%가 나왔다. 기존 stock-only 15주는 평균 413.888125 USD라 계좌 손익은 아직 소폭 플러스지만, `2026-06-01` after-hours validation 1주 5D horizon은 `2026-06-05` 미국 정규장 close 이후에야 닫을 수 있다. 오늘 run에서는 AI 인프라 thesis 유지와 event-risk 확대를 동시에 기록하고, add/trim 정책 승격은 보류한다.

출처: [[2026-06-05-portfolio-review]], [[2026-06-05-0627-analyst-review-cycle-sources]]

### 2026-06-06 hourly-autopilot trim

`0331` scheduled hourly-autopilot은 stale cleanup artifact의 `CVX/NEE` open-order 모순을 runtime Alpaca reconciliation으로 해소한 뒤, buy 쪽 same-day duplicate/per-order-cap 제약과 별개로 `AVGO`를 sell/trim 우선 평가했다. ai_semiconductor_complex warning band 노출, earnings-event drawdown, runtime quote `389.00/389.72`, spread `0.1847%`, active/tradable, held qty `16`이라는 조건에서 25% trim `4주` regular-session day limit sell을 제출했고, 첫 submit cancellation 뒤 동일 `client_order_id=hourly-20260606-0331-sell-avgo`로 1회만 재시도해 `389.25 USD`에 체결됐다. 체결 후 보유수량은 `16주 -> 12주`로 감소했다.

출처: [[2026-06-06-0331-hourly-autopilot]], `wiki/trade-ledger/positions/2026-06-06-0331-hourly-autopilot-post-trade.json`

### 2026-06-06 analyst review cycle

`2026-06-01` after-hours validation 1주는 평균 `461.26 USD` 진입 대비 `2026-06-05` 미국 정규장 close `385.73 USD`로 `-16.37%` 5D 결과를 남겼다. earnings 이후 AI guidance disappointment와 semiconductor-wide de-risking이 겹쳐 validation add 자체는 `약함`으로 닫는다. 다만 `2026-06-06 03:37 KST` trim 4주가 `389.25 USD`에 체결돼 size reduction 대응은 합리적이었다. 현재 해석은 `validation add 실패 + core thesis 완전 폐기 아님`이다.

출처: [[2026-06-06-portfolio-review]], [[2026-06-06-0626-analyst-review-cycle-sources]]
