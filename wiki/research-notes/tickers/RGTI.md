---
id: RGTI
updated_at: 2026-05-24T23:42:18Z
symbol: RGTI
asset_type: stock
---

# RGTI

## 2026-06-19 04:17 KST hourly-autopilot trim

`0411` scheduled hourly-autopilot은 scheduler-owned stale cleanup/core/research preflight를 source-of-record로 사용했고 `Alpha Vantage` throttle, `Firecrawl` credits gap에도 `SEC EDGAR/FRED/Yahoo Finance` 3-provider pass로 strict MCP submit gate를 유지했다. buy side는 `review_backlog_pending_1d_count=17`로 계속 닫혀 있어 sell-first directive를 유지했고, `RGTI`는 live quote `20.73/20.74`, spread 약 `0.0482%`, open orders `0`, held qty `2`, active/tradable US stock 조건에서 residual speculative sleeve staged de-risking floor trim `1주`를 통과했다. `client_order_id=hourly-20260619-0411-sell-rgti` regular-session day limit sell은 same client id readback 기준 `2026-06-18T19:16:44.852563131Z`에 `filled_avg_price=20.8 USD`로 즉시 체결됐고 보유수량은 `2주 -> 1주`로 감소했다. 해석은 `strict gate pass + residual speculative sleeve staged de-risking 지속`이다.

출처: [[2026-06-19-0411-hourly-autopilot]], `wiki/trade-ledger/positions/2026-06-19-0411-hourly-autopilot-post-trade.json`

## 2026-06-19 03:38 KST hourly-autopilot trim

`0331` scheduled hourly-autopilot은 scheduler-owned stale cleanup/core/research preflight를 source-of-record로 사용했고 `Alpha Vantage` throttle, `Firecrawl` credits gap에도 `SEC EDGAR/FRED/Yahoo Finance` 3-provider pass로 strict MCP submit gate를 유지했다. buy side는 `review_backlog_pending_1d_count=17`로 계속 닫혀 있어 sell-first directive를 유지했고, `RGTI`는 source-of-record quote `20.68/20.69`, spread 약 `0.0484%`, open orders `0`, held qty `4`, active/tradable US stock 조건에서 residual speculative sleeve staged de-risking floor trim `1주`를 통과했다. `client_order_id=hourly-20260619-0331-sell-rgti` regular-session day limit sell은 same client id readback 기준 `2026-06-18T18:37:39.173808824Z`에 `filled_avg_price=20.7 USD`로 즉시 체결됐고 보유수량은 `4주 -> 3주`로 감소했다. 해석은 `strict gate pass + residual speculative sleeve staged de-risking 지속`이다.

출처: [[2026-06-19-0331-hourly-autopilot]], `wiki/trade-ledger/positions/2026-06-19-0331-hourly-autopilot-post-trade.json`

## 2026-06-19 03:17 KST hourly-autopilot trim submit

`0311` scheduled hourly-autopilot은 scheduler-owned stale cleanup/core/research preflight를 source-of-record로 사용했고 별도 live continuity 없이도 regular market open, account `ACTIVE`, open orders `0`, watchlists `0`, `RGTI` asset active/tradable, fresh quote `20.61/20.62`, spread 약 `0.0485%`를 재확인했다. research strict gate는 `SEC EDGAR`, `FRED`, `Yahoo Finance` 3-provider pass를 유지했고 buy side는 `review_backlog_pending_1d_count=17`로 계속 닫혀 있어 sell-first directive를 유지했다. `RGTI`는 speculative loss-control trim trigger와 residual speculative sleeve staged de-risking rationale 조건에서 floor trim `1주` 경로를 통과했고 `client_order_id=hourly-20260619-0311-sell-rgti`로 regular-session day limit sell을 제출했다. immediate reconciliation 기준 주문은 아직 `status=new`, `filled_qty=0` open order이며 보유수량은 `5주`, `qty_available=4`로 1주만 예약 상태다. 해석은 `strict gate pass, staged de-risking submit 지속, next cycle fill/open-order lifecycle 추적 필요`다.

출처: [[2026-06-19-0311-hourly-autopilot]], `wiki/trade-ledger/positions/2026-06-19-0311-hourly-autopilot-post-trade.json`

## 2026-06-19 02:37 KST hourly-autopilot trim submit

`0231` scheduled hourly-autopilot은 scheduler-owned stale cleanup/core/research preflight를 source-of-record로 사용했고, live Alpaca submit-boundary recheck 기준 regular market open, account `ACTIVE`, open orders `0`, watchlists `0`, `RGTI` asset active/tradable, fresh quote `20.68/20.70`, spread 약 `0.0967%`를 재확인했다. research strict gate는 `SEC EDGAR`, `FRED`, `Yahoo Finance` 3-provider pass를 유지했고 buy side는 `review_backlog_pending_1d_count=17`로 계속 닫혀 있어 sell-first directive를 유지했다. `RGTI`는 speculative loss-control trim trigger와 residual speculative sleeve staged de-risking rationale 조건에서 floor trim `1주` 경로를 통과했고 `client_order_id=hourly-20260619-0231-sell-rgti`로 regular-session day limit sell을 제출했다. immediate reconciliation 기준 주문은 아직 `status=new`, `filled_qty=0` open order이며 보유수량은 `6주`, `qty_available=5`로 1주만 예약 상태다. 해석은 `strict gate pass, staged de-risking submit 완료, next cycle fill/open-order lifecycle 추적 필요`다.

출처: [[2026-06-19-0231-hourly-autopilot]], `wiki/trade-ledger/positions/2026-06-19-0231-hourly-autopilot-post-trade.json`

## 2026-06-19 01:55 KST hourly-autopilot trim submit

`0151` scheduled hourly-autopilot은 scheduler-owned stale cleanup/core/research preflight를 source-of-record로 사용했고, live Alpaca submit-boundary recheck 기준 regular market open, account `ACTIVE`, open orders `0`, watchlists `0`, `RGTI` asset active/tradable, fresh quote `20.50/20.51`, spread 약 `0.0488%`를 재확인했다. research strict gate는 `SEC EDGAR`, `FRED`, `Yahoo Finance` 3-provider pass로 다시 열렸고 buy side는 `review_backlog_pending_1d_count=17`로 계속 닫혀 있어 sell-first directive를 유지했다. `RGTI`는 speculative loss-control trim trigger와 residual speculative sleeve staged de-risking rationale 조건에서 25% trim `2주` 경로를 통과했고 `client_order_id=hourly-20260619-0151-sell-rgti`로 regular-session day limit sell을 제출했다. follow-up reconciliation 기준 주문은 `2026-06-18T16:57:27.477402Z`에 `filled_avg_price=20.50 USD`로 전량 체결됐고 보유수량은 `9주 -> 7주`로 감소했다. 해석은 `strict MCP gate recovered, staged de-risking 지속`이다.

출처: [[2026-06-19-0151-hourly-autopilot]], `wiki/trade-ledger/positions/2026-06-19-0151-hourly-autopilot-post-trade.json`

## 2026-06-19 01:20 KST hourly-autopilot trim submit

`0111` scheduled hourly-autopilot은 scheduler-owned stale cleanup/core/research preflight를 source-of-record로 사용했고, live Alpaca `get_order_by_client_id(hourly-20260619-0031-sell-rgti)` readback 기준 직전 stale open sell 3주는 `2026-06-18T16:11:08Z`에 `status=canceled`로 정리됐다. strict universe/MCP/risk gate는 모두 PASS했고 buy side는 `review_backlog_pending_1d_count=17`로 계속 닫혀 있어 sell-first directive를 유지했다. `RGTI`는 fresh regular-session quote `20.43/20.45`, spread 약 `0.0978%`, held qty `12`, open orders `0` before submit, speculative loss-control trim trigger 조건에서 25% trim `3주` 경로를 다시 통과했고 `client_order_id=hourly-20260619-0111-sell-rgti`로 regular-session day limit sell을 제출했다. immediate reconciliation 기준 주문은 아직 `status=new`, `filled_qty=0` open order이며 보유수량은 `12주`, `qty_available=9`로 3주만 예약 상태다. 해석은 `residual speculative sleeve staged de-risking 지속, next cycle fill/open-order lifecycle 추적 필요`다.

출처: [[2026-06-19-0111-hourly-autopilot]], `wiki/trade-ledger/positions/2026-06-19-0111-hourly-autopilot-post-trade.json`

## 2026-06-19 00:19 KST hourly-autopilot trim submit

`0011` scheduled hourly-autopilot은 scheduler-owned stale cleanup/core/research preflight를 source-of-record로 사용했고, strict universe/MCP/risk gate가 모두 PASS한 상태에서 buy side는 `review_backlog_pending_1d_count=17`로 계속 닫혀 있었다. `RGTI`는 live regular-session quote `20.68/20.69`, spread 약 `0.0483%`, held qty `15`, open orders `0`, speculative loss-control trim trigger 조건에서 25% trim `3주` 경로를 통과했고 `client_order_id=hourly-20260619-0011-sell-rgti`로 regular-session day limit sell을 제출했다. immediate reconciliation 기준 주문은 아직 `status=new`, `filled_qty=0` open order이며 보유수량은 `15주`, `qty_available=12`로 3주만 예약 상태다. 해석은 `residual speculative sleeve staged de-risking 지속, next cycle fill/open-order lifecycle 추적 필요`다.

출처: [[2026-06-19-0011-hourly-autopilot]], `wiki/trade-ledger/positions/2026-06-19-0011-hourly-autopilot-post-trade.json`

## 2026-06-19 00:00 KST hourly-autopilot trim

`2351` scheduled hourly-autopilot은 scheduler-owned stale cleanup/core/research preflight를 source-of-record로 사용했고, strict universe/MCP/risk gate가 모두 PASS한 상태에서 buy side는 `review_backlog_pending_1d_count=17`로 계속 닫혀 있었다. `RGTI`는 source-of-record regular-session quote `20.49/20.51`, spread 약 `0.0976%`, held qty `20`, open orders `0`, speculative loss-control trim trigger 조건에서 25% trim `5주` 경로를 통과했고 `client_order_id=hourly-20260618-2351-sell-rgti`로 regular-session day limit sell을 제출했다. same client id reconciliation 기준 주문은 `2026-06-18T15:00:14.548344756Z`에 `filled_avg_price=20.812 USD`로 즉시 체결됐고 보유수량은 `20주 -> 15주`로 감소했다. 해석은 `residual speculative sleeve staged de-risking 지속`이다.

출처: [[2026-06-18-2351-hourly-autopilot]], `wiki/trade-ledger/positions/2026-06-18-2351-hourly-autopilot-post-trade.json`

## 2026-06-18 23:20 KST hourly-autopilot trim

`2311` scheduled hourly-autopilot은 scheduler-owned stale cleanup/core/research preflight를 source-of-record로 사용했고, strict universe/MCP/risk gate가 모두 PASS한 상태에서 buy side는 `review_backlog_pending_1d_count=17`로 계속 닫혀 있었다. `RGTI`는 direct Alpaca regular-session quote `20.19/20.21`, spread 약 `0.0991%`, held qty `26`, current US-date duplicate sell `0`, open orders `0`, speculative loss-control trim trigger 조건에서 25% trim `6주` 경로를 통과했고 `client_order_id=hourly-20260618-2311-sell-rgti`로 regular-session day limit sell을 제출했다. same client id reconciliation 기준 주문은 `2026-06-18T14:20:10.945043985Z`에 `filled_avg_price=20.331667 USD`로 즉시 체결됐고 보유수량은 `26주 -> 20주`로 감소했다. 해석은 `residual speculative sleeve staged de-risking 지속`이다.

출처: [[2026-06-18-2311-hourly-autopilot]], `wiki/trade-ledger/positions/2026-06-18-2311-hourly-autopilot-post-trade.json`

## 2026-06-18 12:15 KST after-hours-autopilot reconciliation

`2026-06-18 12:11 KST` after-hours cycle은 scheduler-owned `1211` core/research preflight를 source-of-record로 유지했고 Alpaca core `first_blocking_gate=market_closed`는 장외 워크플로우에서 expected nonblocking으로 처리했다. live Alpaca continuity `get_order_by_client_id(ah-20260618-1131-sell-rgti-01)` 기준 earlier trim 1주는 여전히 `status=new`, `filled_qty=0` open order다. live overnight quote `20.73/20.75`와 spread는 executable 범위였지만 same-session after-hours submitted orders가 이미 `2/2`였고 risk validator는 이 open order age `30.3분 > 30.0분` lifecycle limit으로 FAIL이었다. `get_all_positions` 기준 보유수량은 `27주`, `qty_available=26`이며 해석은 `staged de-risking open order stale lifecycle 추적 필요`다.

출처: [[2026-06-18-1211-after-hours-autopilot]], `wiki/trade-ledger/positions/2026-06-18-1211-after-hours-autopilot-post-trade.json`

## 현재 Thesis

RGTI는 핵심 포트폴리오 보유 종목이라기보다 고모멘텀 이벤트 중심 양자컴퓨팅 종목이다. Alpaca 스냅샷 기준 최신 체결가는 24.80 근처였고, 전일 종가는 22.04였다. 현재 뉴스는 연방 양자컴퓨팅 지원과 CHIPS Act 관련 내용에 연결되어 있다. 셋업은 흥미롭지만, 새 paper 계좌에서 자동 매수하기에는 변동성이 너무 높다.

2026-05-22 14:10 UTC 업데이트: 최신 체결가는 25.76으로 상승했고, stock-only 거래 제안에서는 소액 매수 후보로만 포함했다. 촉매는 강하지만 이벤트성 변동성이 커서 포트폴리오 비중은 약 5%로 제한한다.

## 추세

- 일간: 강한 긍정.
- 주간: 긍정적이나 변동성 높음.
- 월간: 3-4월 약세 이후 급격히 회복.

## 촉매

- 연방 양자컴퓨팅 지원 관련 헤드라인.
- 양자컴퓨팅 섹터 동반 강세.

## 리스크

- 뉴스 기반 갭 리스크.
- 높은 변동성과 밸류에이션 불확실성.
- 촉매 이후 후속 매수세가 약해질 수 있다.

## 포트폴리오 맥락

- 현재 노출: 0%.
- 제안 역할: 투기적 소액 양자컴퓨팅 후보.
- 제안 주문: 190주, 지정가 25.77, 예상 4896.30 USD.
- 현재 조치: 주문 제출 없음.

## 점수

- 점수: 68/100
- 신뢰도: 낮음

## 출처

- [[2026-05-22-alpaca-market-data]]
- [[2026-05-22-alpaca-news]]
- [[2026-05-22-stock-only-alpaca-snapshot]]

## 거래 기록

- 2026-05-22: paper 매수 120주가 평균 25.569584 USD에 체결됐다.
- 2026-06-08: scheduled hourly-autopilot에서 regular-session trim 30주가 `21.48 USD`에 체결됐다.
- 2026-06-09: scheduled hourly-autopilot에서 regular-session trim 22주가 `22.298182 USD`에 체결됐다.
- 2026-06-10 23:15 KST: scheduled hourly-autopilot에서 speculative loss-control trim 17주가 `20.38 USD`에 체결됐다.
- 2026-06-11 09:59 KST: scheduled after-hours-autopilot에서 residual speculative sleeve de-risking 근거로 1주 trim sell이 `19.50 USD`에 체결됐다.
- 2026-06-11 10:20 KST: scheduled after-hours-autopilot `1011` cycle의 추가 trim 1주가 `19.78 USD`에 체결됐고 `1031` reconciliation에서 fill이 확인됐다.
- 2026-06-15 22:41 KST: scheduled `2231` hourly-autopilot을 scheduler-owned regular-session preflight로 실행했고, `RGTI` 9주 trim sell이 `client_order_id=hourly-20260615-2231-sell-rgti`, `filled_avg_price=23.366667 USD`로 즉시 체결돼 보유수량이 `37주 -> 28주`로 감소했다.
- 2026-06-17 13:39 KST: scheduled after-hours-autopilot에서 residual speculative sleeve staged de-risking 근거로 추가 1주 trim sell이 `client_order_id=ah-20260617-1331-sell-rgti-01`, `filled_avg_price=20.96 USD`로 즉시 체결돼 보유수량이 `28주 -> 27주`로 감소했다.
- 2026-06-18 11:40 KST: scheduled after-hours-autopilot에서 fresh overnight quote `20.74/20.76`, spread 약 `0.0964%`, same-session `RGTI` duplicate `0`을 근거로 추가 1주 trim sell `client_order_id=ah-20260618-1131-sell-rgti-01`을 제출했다. immediate reconciliation 기준 주문은 `status=new`, `filled_qty=0` open order이며 `qty_available=26`으로 1주만 예약 상태다.
- 주문/체결 출처: [[2026-05-22-paper-order-submission]]

## 2026-05-25 현재 추천 메모

RGTI는 오늘 신규 매수 후보에서 제외했다. 2026-05-22 종가 26.41 기준 5D +48.04%, 20D +59.05%로 가격 모멘텀은 매우 강하지만 quantum 테마 급등과 valuation/short-interest concern이 동시에 확인됐다.

현재 paper 포지션은 소액 보유로 유지하되, speculative/quantum cluster cap과 overheat guard 때문에 추가 매수는 하지 않는다.

## 회고 기록

- 2026-05-27: [[2026-05-27-portfolio-review]]에서 2026-05-22 stock-only 매수 1D interim review를 작성했다. RGTI는 25.569584 USD 진입 대비 Alpaca 현재가 24.84 USD, 미실현 -2.85%로 양자컴퓨팅 이벤트 추격 리스크가 바로 나타났다. 낮은 비중 편입은 유지하되 5D/20D 회고가 필요하다.
### 2026-06-02 analyst review cycle

2026-05-22 stock-only cohort는 25.569584 USD 진입 대비 2026-06-01 close 25.63 USD로 +0.24%였다. 절대 수익은 flat에 가깝고 SPY/QQQ 대비 약해, quantum sleeve 안에서도 IONQ보다 낮은 품질로 본다. 판단은 `약함`, 20D 회고 대기.

출처: [[2026-06-02-portfolio-review]], [[2026-06-02-0624-analyst-review-cycle-sources]]

### 2026-06-09 analyst review cycle

`2026-06-08 ET` trim 30주는 `21.48 USD`에 체결됐고 same-day close는 `21.77 USD`였다. trimmed lot 기준 원진입 `25.569583 USD` 대비 `-15.99%` loss realization이지만, close-after-trim rebound는 `+1.35%`에 그쳐 speculative sleeve 축소 의사결정 자체를 뒤집지는 않는다. 판단은 `양호`이며 남은 90주는 20D review와 별도로 계속 monitor한다.

출처: [[2026-06-09-portfolio-review]], [[2026-06-09-0623-analyst-review-cycle-sources]]

### 2026-06-10 analyst review cycle

`2026-06-08 ET` trim 30주의 다음 regular close는 `19.69 USD`로 fill `21.48 USD`보다 `-8.33%` 낮았다. hindsight 기준으로도 de-risking timing이 더 나빠지기 전에 실행된 셈이다. 새로 `2026-06-09 ET` trim 22주가 `22.298182 USD`에 체결돼 잔여 수량은 `68주`가 됐고, current `19.75 USD` 기준 포지션 전체 미실현은 여전히 `-22.76%`라 추가 defensive monitor를 유지한다.

출처: [[2026-06-10-portfolio-review]], [[2026-06-10-0622-analyst-review-cycle-sources]]

### 2026-06-10 23:15 KST hourly-autopilot trim

`2311` scheduled hourly-autopilot은 scheduler-owned stale cleanup/core/research preflight와 live Alpaca MCP submit-boundary check를 함께 사용했다. `RGTI`는 live IEX quote `20.38/20.39`, spread `0.0491%`, held qty `68`, speculative loss-control trim trigger, 큰 미실현 손실, active/tradable NASDAQ stock 조건에서 25% trim 경로를 통과했고 `client_order_id=hourly-20260610-2311-sell-rgti`로 17주 sell을 제출했다. same order id reconciliation 기준 주문은 `2026-06-10T14:14:43.88079Z`에 `20.38 USD`로 전량 체결됐고 보유수량은 `68주 -> 51주`로 감소했다. 해석은 `speculative sleeve staged de-risking 지속`이다.

출처: [[2026-06-10-2311-hourly-autopilot]], `wiki/trade-ledger/positions/2026-06-10-2311-hourly-autopilot-post-trade.json`

### 2026-06-11 09:59 KST after-hours-autopilot trim

`scheduler-owned 0951` 장외 preflight와 runtime Alpaca MCP submit-boundary check를 함께 사용했다. `RGTI`는 runtime overnight quote `19.47/19.48`, spread 약 `0.0513%`, held qty `51`, residual speculative sleeve de-risking rationale를 충족해 `client_order_id=ah-20260611-0951-sell-rgti` 1주 sell을 제출했고, same client id reconciliation 기준 `2026-06-11T00:59:35.159665043Z`에 `19.50 USD`로 즉시 체결됐다. 보유수량은 `51주 -> 50주`로 감소했고 해석은 `staged de-risking 지속`이다.

출처: [[2026-06-11-0951-after-hours-autopilot]], `wiki/trade-ledger/positions/2026-06-11-0951-after-hours-autopilot-post-trade.json`

### 2026-06-11 10:19 KST after-hours-autopilot trim submit

`scheduler-owned 1011` 장외 preflight와 runtime Alpaca MCP submit-boundary check를 함께 사용했다. `AVGO`는 submit 직전 spread가 cap을 다시 넘겨 탈락했고, `RGTI`는 runtime overnight quote `19.77/19.78`, spread 약 `0.0506%`, held qty `50`, residual speculative sleeve de-risking rationale를 충족해 `client_order_id=ah-20260611-1011-sell-rgti` 1주 sell을 제출했다. same client id immediate reconciliation 기준 주문은 아직 `status=new` open order이며 fill은 없고, 보유수량은 `50주`로 unchanged, `qty_available=49`만 예약 상태다. 해석은 `staged de-risking 지속, open order lifecycle 추적 필요`다.

출처: [[2026-06-11-1011-after-hours-autopilot]], `wiki/trade-ledger/positions/2026-06-11-1011-after-hours-autopilot-post-trade.json`

### 2026-06-11 10:36 KST after-hours-autopilot reconciliation

`scheduler-owned 1031` 장외 preflight와 runtime Alpaca MCP reconciliation check를 함께 사용했다. `get_order_by_client_id(ah-20260611-1011-sell-rgti)` 기준 앞서 open 상태였던 trim 1주는 `2026-06-11T01:20:06.981355496Z`에 `19.78 USD`로 체결 완료됐고, same-session prior fill `ah-20260611-0951-sell-rgti`와 합쳐 after-hours session budget이 `2/2`로 닫혔다. `get_all_positions` 기준 보유수량은 `50주 -> 49주`로 감소했고 해석은 `staged de-risking 지속, residual speculative sleeve monitor 유지`다.

출처: [[2026-06-11-1031-after-hours-autopilot]], `wiki/trade-ledger/positions/2026-06-11-1031-after-hours-autopilot-post-trade.json`

### 2026-06-18 11:40 KST after-hours-autopilot trim submit

`1131` scheduled after-hours-autopilot은 scheduler-owned core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. `PFE`는 같은 세션의 기존 open trim `ah-20260618-1111-sell-pfe-01` 때문에 same-symbol 추가 trim이 막혔고, `RGTI`는 direct overnight quote `20.74/20.76`, spread 약 `0.0964%`, held qty `27`, same-session duplicate `0`, open `RGTI` sell `0` 조건에서 residual speculative sleeve staged de-risking 경로를 다시 통과했다. `client_order_id=ah-20260618-1131-sell-rgti-01` 1주 after-hours day limit trim sell을 제출했고, same client id immediate reconciliation 기준 주문은 `status=new`, `filled_qty=0`, `filled_avg_price=null` open order다. `get_all_positions` 기준 보유수량은 아직 `27주`, `qty_available=26`이며, separate after-hours session budget은 `2/2` 사용 상태로 닫혔다. 해석은 `staged de-risking submit 완료, next cycle fill/open-order lifecycle 추적 필요`다.

출처: [[2026-06-18-1131-after-hours-autopilot]], `wiki/trade-ledger/positions/2026-06-18-1131-after-hours-autopilot-post-trade.json`

### 2026-06-11 analyst review cycle

`2026-06-09 ET` trim 22주는 `22.298182 USD` 체결 대비 `2026-06-10 ET` close `19.445 USD`로 `-12.80%`였다. `2026-06-10 ET` 추가 trim 17주도 이미 `20.38 USD`에 체결돼 staged de-risking이 이어졌고, current Alpaca snapshot 기준 잔여 `51주`의 평균단가 `25.569583 USD` 대비 미실현은 여전히 `-24.52%`다. speculative sleeve reduction은 계속 타당했고, 남은 포지션은 residual monitor로만 본다.

출처: [[2026-06-11-portfolio-review]], [[2026-06-11-0622-analyst-review-cycle-sources]]

### 2026-06-12 analyst review cycle

`2026-06-10 ET` regular-session trim 17주는 `20.38 USD` 체결 대비 `2026-06-11 ET` close/current `20.72 USD`로 `+1.67%` rebound가 있었다. 전일 trim만큼 깔끔한 hindsight 우위는 아니지만, after-hours `19.50/19.78` 추가 trim까지 포함하면 speculative sleeve staged de-risking 방향은 유지된다. current snapshot 기준 잔여 `49주`는 여전히 residual monitor 포지션이다.

출처: [[2026-06-12-portfolio-review]], [[2026-06-12-0632-analyst-review-cycle-sources]]

### 2026-06-13 analyst review cycle

`2026-06-12 ET` regular-session trim 12주는 `21.010833 USD`로 체결돼 보유수량이 `49주 -> 37주`로 감소했다. current Alpaca snapshot 기준 잔여 포지션은 평균단가 `25.569583 USD`, current `21.01 USD`, 미실현 약 `-17.83%`이며 residual speculative sleeve 해석은 유지된다. 이 trim의 첫 1D horizon은 주말을 건너 `2026-06-15` 미국 정규장 close에 닫힌다.

출처: [[2026-06-13-portfolio-review]], [[2026-06-13-0622-analyst-review-cycle-sources]]

### 2026-06-14 analyst review cycle

새 regular-session close가 아직 없어서 `2026-06-12 ET` trim 12주의 `1D` closeout은 여전히 대기 상태다. current Alpaca snapshot 기준 `RGTI`는 `37주`, 평균단가 `25.569583 USD`, current `20.98 USD`, 미실현 약 `-17.95%`이며 residual speculative sleeve 해석은 유지한다. 첫 `1D` 판단 시점은 그대로 `2026-06-15` 미국 정규장 close 이후다.

출처: [[2026-06-14-portfolio-review]], [[2026-06-14-0623-analyst-review-cycle-sources]]

### 2026-06-15 analyst review cycle

일요일 closed clock 기준 새 regular-session close가 없어서 `2026-06-12 ET` trim 12주의 `1D` closeout은 계속 대기 상태다. current Alpaca snapshot 기준 `RGTI`는 `37주`, 평균단가 `25.569583 USD`, current `20.98 USD`, 미실현 약 `-17.95%`이며, Alpaca IEX daily bar는 전일 대비 `+1.75%` 반등했지만 residual speculative sleeve 해석을 바꾸지는 않는다. 첫 `1D` 판단 시점은 그대로 `2026-06-15` 미국 정규장 close 이후다.

출처: [[2026-06-15-portfolio-review]], [[2026-06-15-0624-analyst-review-cycle-sources]]

### 2026-06-16 analyst review cycle

`2026-06-12 ET` trim 12주는 `21.010833 USD` 체결 대비 `2026-06-15 ET` close `22.72 USD`로 `+8.14%` 반등해 timing이 약했다. 다만 current 잔여 포지션은 `28주`, 평균단가 `25.569583 USD`, current `22.80 USD`로 아직 residual speculative sleeve 성격이 남아 있어 staged de-risking 해석 자체를 폐기하진 않는다. `2026-06-15 ET` regular-session trim 9주는 별도 새 `1D` 대기 표본으로 등록한다.

출처: [[2026-06-16-portfolio-review]], [[2026-06-16-0621-analyst-review-cycle-sources]], [[2026-06-15-2231-hourly-autopilot]]

### 2026-06-15 22:41 KST hourly-autopilot trim

`2231` scheduled hourly-autopilot은 scheduler-owned stale cleanup/core/research preflight를 source-of-record로 사용했고, actual submit은 `2026-06-15T13:41:41.654523Z`에 수행됐다. `RGTI`는 fresh Alpaca quote `22.55/22.58`, spread `0.1329%`, held qty `37`, speculative loss-control trim trigger, open orders `0`, validation lifecycle due-block 없음 조건에서 25% trim `9주` 경로를 통과했고 `client_order_id=hourly-20260615-2231-sell-rgti`로 regular-session day limit sell을 제출했다. immediate reconciliation 기준 same order는 `2026-06-15T13:41:43.341983Z`에 `filled_avg_price=23.366667 USD`로 전량 체결됐고 보유수량은 `37주 -> 28주`로 감소했다. 해석은 `residual speculative sleeve staged de-risking 지속`이다.

출처: [[2026-06-15-2231-hourly-autopilot]], `wiki/trade-ledger/positions/2026-06-15-2231-hourly-autopilot-post-trade.json`

### 2026-06-16 23:00 KST hourly-autopilot trim submit

`2251` scheduled hourly-autopilot은 scheduler-owned stale cleanup/core/research preflight를 source-of-record로 사용했고, actual submit은 `2026-06-16T14:00:27.219378296Z`에 수행됐다. `RGTI`는 fresh Alpaca quote `22.07/22.09`, spread 약 `0.0906%`, held qty `28`, speculative loss-control trim trigger, open orders `0`, validation lifecycle due-block 없음 조건에서 25% trim `7주` 경로를 통과했고 `client_order_id=hourly-20260616-2251-sell-rgti`로 regular-session day limit sell을 제출했다. immediate reconciliation 기준 same order는 아직 `status=new` open order이며 fill은 없고, 보유수량은 `28주`로 unchanged, `qty_available=21`만 예약 상태다. 해석은 `residual speculative sleeve staged de-risking 지속, open order lifecycle 추적 필요`다.

출처: [[2026-06-16-2251-hourly-autopilot]], `wiki/trade-ledger/positions/2026-06-16-2251-hourly-autopilot-post-trade.json`

### 2026-06-17 13:39 KST after-hours-autopilot trim

`1331` scheduled after-hours-autopilot은 scheduler-owned core/research preflight를 사용했고, sparse Alpaca core preflight는 direct Alpaca MCP continuity로 보강했다. `RGTI`는 fresh overnight quote `20.94/20.99`, spread 약 `0.2385%`, held qty `28`, same-session duplicate `0`, open orders `0`, residual speculative sleeve staged de-risking rationale 조건에서 whole-share floor 1주 trim 경로를 통과했고 `client_order_id=ah-20260617-1331-sell-rgti-01`로 after-hours day limit sell을 제출했다. same client id immediate reconciliation 기준 주문은 `2026-06-17T04:39:27.02715194Z`에 `filled_avg_price=20.96 USD`로 즉시 체결됐고 보유수량은 `28주 -> 27주`로 감소했다. 해석은 `residual speculative sleeve staged de-risking 지속`이다.

출처: [[2026-06-17-1331-after-hours-autopilot]], `wiki/trade-ledger/positions/2026-06-17-1331-after-hours-autopilot-post-trade.json`

### 2026-06-18 analyst review cycle

`2026-06-10 ET` trim 17주는 `20.38 USD -> 20.25 USD`로 sell 이후 `-0.64%` 더 밀렸다. magnitude는 작지만 trim 이후 약세가 이어져 speculative sleeve de-risking 해석은 `중립 양호`로 유지한다.

출처: [[2026-06-18-portfolio-review]], [[2026-06-18-0621-analyst-review-cycle-sources]]

## 2026-06-19 04:39 KST 업데이트

- `0431` regular-session hourly-autopilot에서 residual speculative sleeve 마지막 1주를 `entry_style=exit`로 정리했다. same `client_order_id=hourly-20260619-0431-sell-rgti` readback 기준 `filled_avg_price=20.87 USD`, `filled_at=2026-06-18T19:39:15.409145509Z`로 즉시 체결됐고 current portfolio에서는 `RGTI position 없음` 상태다. 이번 cycle에서도 buy-side는 `review_backlog_pending_1d_count=17`로 계속 막혀 있었고, strict gate가 모두 열린 sell-first 경로만 실행했다.
