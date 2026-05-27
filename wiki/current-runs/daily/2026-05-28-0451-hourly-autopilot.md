# 2026-05-28-0451-hourly-autopilot scheduled paper autopilot

## 요약

- 시장 시계: Alpaca MCP preflight 기준 `2026-05-27T15:51:11.90038039-04:00` open=true, next_close `2026-05-27T16:00:00-04:00`.
- 계좌: portfolio value `$101,573.77`, cash `$41,175.98`, invested ratio `59.46%`, cash ratio `40.54%`.
- Scheduler stale-order cleanup: stale candidates 0, cancel attempts 0. 남은 stale autopilot order 보고는 없으며 core preflight open orders는 빈 목록이다.
- MCP coverage: Alpaca core PASS. SEC EDGAR, FRED, Firecrawl, Yahoo Finance PASS. Alpha Vantage는 candidate news 0건으로 `empty_response` gap이며 점수에는 미사용.
- Universe/risk/MCP gate는 empty order plan 기준 통과 가능하지만, ET 2026-05-27 scheduled validation new order count가 10건으로 이미 소진되어 `risk_daily_new_orders_budget`에서 신규 주문을 차단했다.
- 제출 주문: 없음. `place_stock_order` 호출 없음.

## 추천 Shortlist

| Rank | Symbol | 결정 | Spread % | Intraday % | 근거 |
| ---: | --- | --- | ---: | ---: | --- |
| 1 | AMZN | skip_duplicate | 0.011062 | 1.937 | same ET-session scheduled validation buy/fill already exists and daily validation order budget is exhausted |
| 2 | NEE | skip_duplicate | 0.011408 | 0.701 | same ET-session scheduled validation buy/fill already exists and daily validation order budget is exhausted |
| 3 | WMT | skip_duplicate | 0.016861 | 0.249 | same ET-session scheduled validation buy/fill already exists and daily validation order budget is exhausted |
| 4 | BAC | skip_duplicate | 0.019545 | -2.284 | same ET-session scheduled validation buy/fill already exists and daily validation order budget is exhausted |
| 5 | SO | skip_duplicate | 0.288200 | 0.246 | same ET-session scheduled validation buy/fill already exists and daily validation order budget is exhausted |
| 6 | NKE | skip_duplicate | 0.021760 | -0.152 | same ET-session scheduled validation buy/fill already exists and daily validation order budget is exhausted |
| 7 | SPY | recheck_only | 0.011993 | -0.058 | fresh quote/research candidate, but daily validation order budget blocks new validation buy |
| 8 | QQQ | recheck_only | 0.004112 | -0.463 | fresh quote/research candidate, but daily validation order budget blocks new validation buy |
| 9 | COP | recheck_only | 0.026022 | 0.048 | fresh quote/research candidate, but daily validation order budget blocks new validation buy |
| 10 | SLB | recheck_only | 0.017729 | -0.521 | fresh quote/research candidate, but daily validation order budget blocks new validation buy |
| 11 | PLTR | recheck_only | 0.015052 | -0.311 | fresh quote/research candidate, but daily validation order budget blocks new validation buy |
| 12 | HOOD | spread_blocked_recheck_only | 3.073648 | 3.179 | spread exceeds 0.50% policy limit, and daily validation order budget also blocks new validation buy |

## 주문 판단

- AMZN, NEE, WMT, BAC, SO, NKE는 모두 quote/spread와 research confirmation 자체는 주문 검토권에 들어오지만, 같은 ET 세션 validation buy/fill 이력과 일일 validation order budget 소진 때문에 추가 매수하지 않는다.
- SPY, QQQ, COP, SLB, PLTR은 다음 recheck 후보로 남긴다. HOOD는 현재 spread가 0.50% 한도를 초과해 spread gate에서도 차단된다.
- 매도/trim: active trim trigger에 해당하는 thesis-break, overweight, stale-thesis underperformance, speculative loss-control 조건을 이번 preflight evidence만으로 확인하지 못했고, 신규 매수 후보보다 순위가 낮다는 이유만으로 매도하지 않는다.

## 검증

- Universe validator: PASS (`--strict`).
- MCP coverage validator: PASS (`--strict`).
- Risk policy validator: PASS (`--json`), empty order plan warning만 존재.

## 지표 설명

- `Spread %`: Alpaca latest quote의 ask-bid를 중간가격으로 나눈 값이다. submit 후보는 0.50% 이하만 허용한다.
- `Intraday %`: 당일 daily bar open 대비 최신 daily/minute 가격 변화율이다. 단독 매수 신호가 아니라 후보 정렬과 리스크 확인에만 사용한다.
- `MCP coverage`: Alpaca core와 SEC EDGAR, Alpha Vantage, FRED, Firecrawl, Yahoo Finance provider evidence의 사용 가능 여부다. Buy 후보는 Alpaca core pass와 research provider 3개 이상 pass/usable이 필요하다.
- `risk_daily_new_orders_budget`: 같은 ET 거래일에 scheduled validation 신규 주문 수가 내부 budget에 도달해 추가 주문을 막는 gate다.
