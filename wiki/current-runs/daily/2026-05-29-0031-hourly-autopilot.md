# 2026-05-29 00:31 KST 정규장 hourly autopilot

## 실행 요약

- 실행 ID: `2026-05-29-0031-hourly-autopilot`
- 모드: `submit`, paper only
- 시장 시계: Alpaca preflight 기준 open, `2026-05-28T11:31:17.193870329-04:00` ET, next close `2026-05-28T16:00:00-04:00`
- stale order cleanup: `wiki/evidence-store/sources/2026-05-29-0031-hourly-autopilot-stale-order-cleanup.json`에서 AAPL stale 주문 cancel attempt `pass`; 이후 등록 Alpaca MCP open-order 재조정 결과 open order 없음.
- Alpaca core: scheduler preflight hard gate `pass`; account/positions/orders/activity/assets/quotes/snapshots/trades 사용.
- Research MCP: SEC EDGAR, FRED, Firecrawl, Yahoo Finance pass; Alpha Vantage는 `empty_response` gap. 최소 3개 research confirmation 충족.

## 후보와 주문 계획

| 티커 | 방향 | 수량 | limit | spread | quote age | confidence | 근거 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| NVDA | buy | 1 | 212.87 | 0.0141% | 6.58분 | 0.68 | AI semiconductor 핵심 종목 1주 검증. 20분 cadence 기준 quote/spread가 신선하고, 직전 같은 날 buy 체결 종목과 동일 symbol이 아니며 COP/TSLA와 다른 cluster라 분산 검증 가치가 있다. |
| COP | buy | 1 | 114.98 | 0.0261% | 6.63분 | 0.63 | Energy commodity 대형주 1주 검증. 현재 shortlist 내에서 AI/mega-cap tech와 상관 cluster가 다르고, 스프레드가 정책 한도 안이라 정규장 validation 관찰 대상으로 적합하다. |
| TSLA | buy | 1 | 441.45 | 0.0249% | 6.57분 | 0.58 | EV/AI event 고베타 종목 1주 소액 검증. source_confidence는 medium이지만 정책상 허용되고 SEC/FRED/Firecrawl/Yahoo 확인 수가 threshold를 넘었으며, speculative cap 내에서 1주만 관찰한다. |

## Gate 상태

- Paper mode: `ALPACA_PAPER_TRADE=true`
- Universe gate: broad metadata universe 62개, SPY/QQQ 포함, final candidates 3개.
- MCP gate: Alpaca core pass + research 4/5 pass, Alpha Vantage `empty_response` gap 기록.
- Quote/spread: 세 후보 모두 20분 이내, 0.50% 이하.
- Open-order lifecycle: cleanup artifact의 즉시 remaining list는 stale AAPL을 남겼지만, 등록 Alpaca MCP 재조정에서 open order 0건으로 확인.
- Risk validator: PASS, buy notional 769.30달러, post-cash 37,606.13달러.

## 제출/체결 결과

| 티커 | client_order_id | 상태 | 체결 수량 | 평균 체결가 | 비고 |
| --- | --- | --- | ---: | ---: | --- |
| NVDA | hourly-20260529-0031-nvda-buy-01 | filled | 1 | 212.55 | Alpaca MCP client-order reconciliation PASS |
| COP | hourly-20260529-0031-cop-buy-01 | filled | 1 | 114.95 | Alpaca MCP client-order reconciliation PASS |
| TSLA | hourly-20260529-0031-tsla-buy-01 | new/open | 0 |  | 정규장 day limit open order로 남음 |

Post-trade reconciliation: account PASS, positions PASS, fills PASS, open orders PASS. 현재 open order는 TSLA 1주 buy limit 441.45뿐이다. NVDA/COP는 `회고 대기`로 표시한다.

## 지표 설명

- `spread`: ask와 bid의 차이를 중간가격으로 나눈 값이다. 정책 한도는 0.50%다.
- `quote age`: 주문 판단 시각과 Alpaca latest quote timestamp의 차이다. submit 한도는 20분이다.
- `confidence`: 추천 정책의 후보 품질, 리서치 확인, 분산 효과, 리스크를 합친 0~1 점수다.
- `expected adverse move`: 20거래일 안에 감수할 수 있는 불리한 변동 가정이다.
