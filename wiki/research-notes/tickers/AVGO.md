---
id: AVGO
updated_at: 2026-06-12T05:18:39Z
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
- 2026-06-08 09:20 KST: scheduled after-hours-autopilot에서 post-earnings risk watch와 validation add failure를 근거로 추가 1주 trim이 `391.27 USD`에 체결됐다.
- 2026-06-10 02:00 KST: scheduled hourly-autopilot에서 regular-session trim 2주가 `375.47 USD`에 체결됐다.
- 2026-06-10 23:01 KST: scheduled hourly-autopilot에서 ai_semiconductor warning band와 post-earnings de-risking rationale를 근거로 추가 2주 trim이 `373.25 USD`에 체결됐다.
- 2026-06-11 23:00 KST: scheduled hourly-autopilot에서 review backlog가 신규 buy를 막는 동안 sell-first 경로를 유지했고, live IEX quote `379.93/380.06`과 spread 정상화를 근거로 추가 1주 trim이 `380.43 USD`에 체결됐다.
- 2026-06-12 14:18 KST: scheduled after-hours-autopilot에서 runtime overnight quote `386.79/387.61`, spread `0.2119%`, held qty `5`, staged de-risking rationale를 근거로 추가 1주 trim sell을 `client_order_id=ah-20260612-1411-sell-avgo-01`로 제출했다. exposed runtime surface에는 post-submit `get_order_by_client_id` readback이 없었지만 immediate Alpaca MCP `get_all_positions`에서 보유수량이 `5주 -> 4주`로 감소해 filled reconciliation으로 기록했다.
- 2026-06-15 23:02 KST: scheduled `2251` hourly-autopilot에서 direct Alpaca quote `394.90/395.07`, spread `0.0430%`, held qty `3`, ai_semiconductor warning band, post-earnings staged de-risking rationale를 근거로 `client_order_id=hourly-20260615-2251-sell-avgo` 1주 trim sell을 제출했다. immediate reconciliation 기준 주문은 `status=new` open 상태이고 `qty_available=2`로 1주가 예약됐으며 fill은 아직 없다.
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

### 2026-06-07 analyst review cycle

`2026-06-06` 미국 정규장 close 기준 새로 닫힌 horizon은 없었다. 다만 current Alpaca snapshot상 `AVGO`는 close/current `385.73 USD`, 평균단가 `414.940833 USD`로 미실현 `-7.04%` 수준이고, 전일 close `418.955 USD` 대비 하루 `-7.93%`다. 이미 `2026-06-06 03:37 KST` trim으로 size를 줄인 만큼 이번 run에서는 추가 trim/exit 규칙을 만들지 않고 `post-earnings risk watch`를 유지한다.

출처: [[2026-06-07-portfolio-review]], [[2026-06-07-0623-analyst-review-cycle-sources]]

### 2026-06-08 analyst review cycle

`2026-06-07 17:22 ET` closed-market scan 기준 새로 닫힌 review horizon은 없다. Alpha Vantage `EARNINGS`는 latest quarter `reportedDate=2026-06-03`, `reportedEPS=2.44`, `estimatedEPS=2.39`, `surprisePercentage=2.0921`를 재확인했지만, price는 여전히 `385.73 USD`로 평균단가 대비 `-7.04%`다. 따라서 이번 run에서도 `validation add 실패 + core thesis 완전 폐기 아님` 해석과 `post-earnings risk watch`를 유지한다.

출처: [[2026-06-08-portfolio-review]], [[2026-06-08-0622-analyst-review-cycle-sources]]

### 2026-06-08 after-hours-autopilot trim

`0911` scheduled after-hours-autopilot은 scheduler-owned core/research preflight와 runtime Alpaca MCP 장외 quote를 재확인한 뒤, `AVGO` 1주 trim을 `391.26 USD` limit, `extended_hours=true`, `client_order_id=ah-20260608-0911-sell-avgo`로 제출했다. same client id reconciliation 기준 주문은 `2026-06-08T00:20:05.775901Z`에 `391.27 USD`로 체결됐고 보유수량은 `12주 -> 11주`로 감소했다. 해석은 `validation add 실패 + core thesis 완전 폐기 아님`을 유지한 채 post-earnings risk watch에 맞춘 floor-size 추가 de-risking이다.

출처: [[2026-06-08-0911-after-hours-autopilot]], `wiki/trade-ledger/positions/2026-06-08-0911-after-hours-autopilot-post-trade.json`

### 2026-06-08 after-hours-autopilot trim 2

`0931` scheduled after-hours-autopilot은 scheduler-owned core preflight가 regular-market-closed clock row만 남긴 sparse artifact였기 때문에, runtime Alpaca MCP로 account/positions/orders/asset/overnight quote를 다시 채웠다. 그 결과 `AVGO`는 `392.73/392.78` 장외 quote, spread `0.012731%`, quote age `0.06`분, held qty `11` 조건에서 다시 floor-size trim 경로를 통과했고 `client_order_id=ah-20260608-0931-sell-avgo`로 1주 sell을 제출했다. same client id reconciliation 기준 주문은 `2026-06-08T00:37:53.182189Z`에 `392.80 USD`로 체결됐고 보유수량은 `11주 -> 10주`로 감소했다. 해석은 여전히 `validation add 실패 + core thesis 완전 폐기 아님`이며, buy backlog throttle 아래에서 post-earnings risk watch를 반영한 추가 de-risking이다.

출처: [[2026-06-08-0931-after-hours-autopilot]], `wiki/trade-ledger/positions/2026-06-08-0931-after-hours-autopilot-post-trade.json`

### 2026-06-09 analyst review cycle

`2026-06-08 ET` after-hours trim 2건은 `391.27 USD`, `392.80 USD`에 체결됐고 same-day close는 `396.72 USD`였다. exit 이후 `+1.39%`, `+1.00%` rebound가 있어 exact timing은 조금 이르렀지만, 평균단가 `414.940833 USD` 대비 포지션은 여전히 `-4.39%`라 post-earnings staged de-risking 자체는 타당했다. 판단은 `중립 양호`이며 core thesis를 전면 폐기하지는 않는다.

출처: [[2026-06-09-portfolio-review]], [[2026-06-09-0623-analyst-review-cycle-sources]]

### 2026-06-10 analyst review cycle

`2026-06-08 ET` after-hours trim 2건의 다음 regular close는 `392.765 USD`였다. `391.27 USD` trim 대비 `+0.38%`, `392.80 USD` trim 대비 `-0.01%`로 exact timing edge는 제한적이었지만 staged de-risking 해석은 유지된다. 새로 `2026-06-09 ET` regular-session trim 2주가 `375.47 USD`에 체결돼 보유수량은 `8주`로 줄었고, 이 regular-session trim의 1D horizon은 `2026-06-10 ET` close 이후 별도로 본다.

출처: [[2026-06-10-portfolio-review]], [[2026-06-10-0622-analyst-review-cycle-sources]]


### 2026-06-10 23:01 KST hourly-autopilot trim

`2251` scheduled hourly-autopilot은 scheduler-owned stale cleanup/core/research preflight와 live Alpaca MCP submit-boundary check를 함께 사용했다. `AVGO`는 live IEX quote `373.21/374.78`, spread `0.4191%`, held qty `8`, ai_semiconductor warning band, post-earnings de-risking rationale 조건에서 25% trim 경로를 통과했고 `client_order_id=hourly-20260610-2251-sell-avgo`로 2주 sell을 제출했다. same order id reconciliation 기준 주문은 `2026-06-10T14:01:38.378996Z`에 `373.25 USD`로 전량 체결됐고 보유수량은 `8주 -> 6주`로 감소했다. 해석은 `core thesis 전면 폐기 아님 + staged de-risking 지속`이다.

출처: [[2026-06-10-2251-hourly-autopilot]], `wiki/trade-ledger/positions/2026-06-10-2251-hourly-autopilot-post-trade.json`

### 2026-06-11 analyst review cycle

`2026-06-09 ET` regular-session trim 2주는 `375.47 USD` 체결 대비 `2026-06-10 ET` close `371.88 USD`로 `-0.96%`였다. sell 이후 close가 더 낮아 same-day trim 자체는 hindsight 기준으로도 방어적이었다. Alpha Vantage earnings beat와 SEC `2026-06-09` 10-Q/`2026-06-03` 8-K는 확인됐지만, current Alpaca snapshot 기준 포지션은 아직 `6주`, 평균단가 `417.04625 USD`, 미실현 `-10.80%`라 staged de-risking 해석을 유지한다.

출처: [[2026-06-11-portfolio-review]], [[2026-06-11-0622-analyst-review-cycle-sources]]

### 2026-06-11 23:00 KST hourly-autopilot trim

`2251` scheduled hourly-autopilot은 scheduler-owned stale cleanup/core/research preflight와 live Alpaca MCP submit-boundary check를 함께 사용했다. `review_backlog_pending_1d_count=14`로 신규 validation buy는 stop됐지만 sell-first path는 유지됐고, `AVGO`는 live IEX quote `379.93/380.06`, spread `0.0342%`, held qty `6`, ai_semiconductor warning band, post-earnings staged de-risking rationale 조건에서 whole-share floor 1주 trim 경로를 통과했다. `client_order_id=hourly-20260611-2251-sell-avgo` 주문은 `2026-06-11T14:00:59.058708Z`에 `380.43 USD`로 즉시 체결됐고 보유수량은 `6주 -> 5주`로 감소했다. 해석은 여전히 `core thesis 전면 폐기 아님 + staged de-risking 지속`이다.

출처: [[2026-06-11-2251-hourly-autopilot]], `wiki/trade-ledger/positions/2026-06-11-2251-hourly-autopilot-post-trade.json`

### 2026-06-12 analyst review cycle

`2026-06-10 ET` regular-session trim 2주는 `373.25 USD` 체결 대비 `2026-06-11 ET` close/current `384.25 USD`로 `+2.95%` rebound가 나왔다. 이번 1D만 보면 exact timing edge는 전일 trim보다 약했지만, current Alpaca snapshot 기준 포지션은 여전히 `5주`, 평균단가 `419.151667 USD`, 미실현 약 `-8.33%`라 staged de-risking 해석을 뒤집지는 않는다. 다음 cycle에서는 `2026-06-11 ET` trim 1주의 1D horizon을 따로 본다.

출처: [[2026-06-12-portfolio-review]], [[2026-06-12-0632-analyst-review-cycle-sources]]

### 2026-06-12 after-hours-autopilot trim

`1411` scheduled after-hours-autopilot은 scheduler-owned `1411` core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 expected nonblocking으로 처리했다. `review_backlog_pending_1d_count=14`로 신규 buy는 계속 막혔지만 sell-first path는 유지됐고, `AVGO`는 runtime overnight quote `386.79/387.61`, spread `0.2119%`, quote age 약 `0.51`분, held qty `5` 조건에서 whole-share floor 1주 trim 경로를 통과했다. `client_order_id=ah-20260612-1411-sell-avgo-01` 주문은 Alpaca MCP `place_stock_order`에서 `order_id=ecdd85cb-0b94-410c-b9f8-5e29f4a8ee2b`, `status=pending_new`로 생성됐고, exposed runtime surface에는 post-submit `get_order_by_client_id` readback이 없었지만 immediate `get_all_positions` 기준 보유수량이 `5주 -> 4주`로 감소해 filled reconciliation으로 기록했다. 해석은 여전히 `validation add 실패 + core thesis 완전 폐기 아님 + staged de-risking 지속`이다.

출처: [[2026-06-12-1411-after-hours-autopilot]], `wiki/trade-ledger/positions/2026-06-12-1411-after-hours-autopilot-post-trade.json`

### 2026-06-13 analyst review cycle

`2026-06-11 ET` after-hours trim 1주는 `387.06 USD` 체결 대비 `2026-06-12 ET` close/current `381.95 USD`로 `-1.32%`였다. trim 뒤 다음 정규장 close가 더 낮아져 staged de-risking 판단은 다시 타당했다. Alpha Vantage `EARNINGS` 기준 latest quarter는 `reportedDate=2026-06-03`, `reportedEPS=2.44`, `estimatedEPS=2.39`, `surprisePercentage=2.0921`로 beat였지만, current Alpaca snapshot 기준 포지션은 `4주`, 평균단가 `420.836 USD`, 미실현 약 `-9.28%`라 recovery confirmation은 여전히 부족하다.

출처: [[2026-06-13-portfolio-review]], [[2026-06-13-0622-analyst-review-cycle-sources]]

### 2026-06-14 analyst review cycle

live Alpaca clock이 `2026-06-13 17:22 ET` 토요일 closed 상태라 새 regular-session closeout은 추가되지 않았다. current Alpaca snapshot 기준 `AVGO`는 `4주`, 평균단가 `423.3625 USD`, current `382.07 USD`, 미실현 약 `-9.75%`이고, staged de-risking 뒤에도 recovery confirmation이 부족해 `post-earnings staged de-risking 지속` 해석을 유지한다.

출처: [[2026-06-14-portfolio-review]], [[2026-06-14-0623-analyst-review-cycle-sources]]

### 2026-06-15 analyst review cycle

live Alpaca clock이 `2026-06-14 17:21 ET` 일요일 closed 상태라 새 regular-session closeout은 여전히 없다. current Alpaca snapshot 기준 `AVGO`는 `4주`, 평균단가 `423.3625 USD`, current `382.07 USD`, 미실현 약 `-9.75%`이며 Alpaca IEX daily bar는 전일 대비 `-0.79%`였다. 이번 cycle SEC EDGAR recent filings에서 `2026-06-11` 8-K와 `2026-06-09` 10-Q가 바로 확인됐지만, price recovery confirmation이 부족해 `post-earnings staged de-risking 지속` 해석을 유지한다.

출처: [[2026-06-15-portfolio-review]], [[2026-06-15-0624-analyst-review-cycle-sources]]

### 2026-06-16 analyst review cycle

`2026-06-14 ET` after-hours trim 1주는 `391.92 USD` 체결 대비 `2026-06-15 ET` close `393.97 USD`로 `+0.52%` 반등해 trim timing은 약했다. 그래도 current snapshot 기준 잔여 포지션은 `2주`, 평균단가 `423.3625 USD`, 미실현 약 `-6.94%`라 staged de-risking 자체를 뒤집을 정도의 회복 confirmation은 아직 부족하다. 이번 cycle에서는 `2026-06-15 ET` regular-session trim 1주도 새 `1D` 대기열로 등록한다.

출처: [[2026-06-16-portfolio-review]], [[2026-06-16-0621-analyst-review-cycle-sources]], [[2026-06-16-0011-hourly-autopilot]]

### 2026-06-16 22:31 KST hourly-autopilot trim

`2231` scheduled hourly-autopilot은 scheduler-owned `2231` stale cleanup/core/research preflight를 source-of-record로 사용했고, direct Alpaca submit-boundary check에서 `AVGO`가 quote `387.00/388.50`, spread `0.3868%`, held qty `2`, ai_semiconductor target-band de-risking rationale, negative expected excess, open orders `0`, current-session same-day duplicate `0` 조건을 만족해 1주 trim 경로를 통과했다. `client_order_id=hourly-20260616-2231-sell-avgo` 주문은 `2026-06-16T13:43:57.208757279Z`에 `387.76 USD`로 즉시 체결됐고 보유수량은 `2주 -> 1주`로 감소했다. 해석은 `core thesis 전면 폐기 아님 + staged de-risking 지속`이다.

출처: [[2026-06-16-2231-hourly-autopilot]], `wiki/trade-ledger/positions/2026-06-16-2231-hourly-autopilot-post-trade.json`

### 2026-06-15 23:02 KST hourly-autopilot trim submit

`2251` scheduled hourly-autopilot은 scheduler-owned stale cleanup/core/research preflight를 source-of-record로 사용했고, direct Alpaca spot check로 `clock/account/positions/quotes/recent fills`를 다시 맞췄다. `AVGO`는 direct quote `394.90/395.07`, spread `0.0430%`, held qty `3`, ai_semiconductor target-band warning, post-earnings staged de-risking rationale 조건에서 1주 trim 경로를 통과했고 `client_order_id=hourly-20260615-2251-sell-avgo`로 regular-session day limit sell을 제출했다. immediate reconciliation 기준 same order는 `status=new`, `filled_qty=0`이며 `get_all_positions`는 `qty=3`, `qty_available=2`를 반환해 1주가 예약 상태임을 보여줬다. 해석은 `staged de-risking submit 완료, next cycle fill/open-order lifecycle 추적 필요`다.

출처: [[2026-06-15-2251-hourly-autopilot]], `wiki/trade-ledger/positions/2026-06-15-2251-hourly-autopilot-post-trade.json`

### 2026-06-17 analyst review cycle

`2026-06-15 ET` regular-session trim 1주는 `392.14 USD -> 376.53 USD`로 sell 이후 `-3.98%` 더 밀렸다. hindsight 기준 trim timing은 양호했고 `post-earnings staged de-risking` 해석도 유지된다. 다만 current Alpaca snapshot 기준 잔여 `1주` 포지션 자체는 여전히 약하므로, 이번 closeout은 `양호`로 닫되 core thesis 복귀 신호로 과대해석하지 않는다.

출처: [[2026-06-17-portfolio-review]], [[2026-06-17-0623-analyst-review-cycle-sources]]
