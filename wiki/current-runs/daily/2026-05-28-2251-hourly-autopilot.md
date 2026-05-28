# 2026-05-28-2251-hourly-autopilot scheduled paper autopilot

## 요약

- Paper mode: `ALPACA_PAPER_TRADE=true`. 정규장 clock은 `2026-05-28T09:51:16.272050313-04:00` 기준 open=true.
- Scheduler stale cleanup: `pass`. 이전 BAC validation buy `hourly-20260528-2231-bac-buy-01`는 미체결이지만 약 13.33분으로 stale 대상이 아니었다.
- Alpaca core gate: PASS. account/positions/open orders/recent activities/assets/quotes/snapshots/trades는 scheduler MCP preflight를 출처로 사용했다.
- Research MCP gate: SEC EDGAR, FRED, Firecrawl, Yahoo Finance PASS; Alpha Vantage는 `empty_response` gap. 4개 usable/pass로 submit 기준 3개를 충족했다.
- 계획 주문: CVX, NEE, NKE 각 1주 day limit buy. 모두 stock, whole-share, regular-session, extended_hours=false.

## 후보 및 주문 계획

| Symbol | Action | Qty | Limit | Spread % | 근거 |
| --- | --- | ---: | ---: | ---: | --- |
| CVX | buy | 1 | 184.35 | 0.0434 | 에너지/원자재 클러스터의 유동성 높은 분산 후보. 당일 SPY 대비 상대 강도가 양호하고 스프레드가 0.05% 미만이다. 기존 BAC open buy와 심볼/클러스터가 달라 중복 주문이 아니며, 1주 검증 규모는 포트폴리오와 테마 한도 안에 있다. |
| NEE | buy | 1 | 88.00 | 0.0227 | 유틸리티 방어 클러스터 보강 후보. 당일 양의 상대 모멘텀과 매우 좁은 스프레드를 확인했고, 기존 성장/반도체 집중을 낮추는 분산 효과가 있다. SEC/FRED/Firecrawl/Yahoo 확인 4개가 사용 가능하다. |
| NKE | buy | 1 | 46.03 | 0.0435 | 소비재 경기민감 클러스터의 소액 검증 후보. 가격은 5달러 이상, 스프레드 0.05% 미만, 기존 보유 1주에 대한 추가 1주도 티커 한도에 크게 못 미친다. 에너지/유틸리티 후보와 상관 클러스터가 달라 추가 슬롯 요건에 부합한다. |

## 게이트

- Universe strict: 62개 metadata universe, SPY/QQQ 포함, pre-MCP shortlist 10개, final candidates 3개.
- MCP strict: Alpaca core PASS + research usable/pass 4개. Alpha Vantage gap은 `empty_response`로 기록하고 점수에는 미사용.
- Risk validator: 생성 직후 실행 예정. 실패하면 제출하지 않는다.
- Open-order lifecycle: BAC open buy는 fresh order라 same-symbol/financials cluster 추가만 차단하고, 이번 후보 세 클러스터와는 중복되지 않는다.

## 지표 설명

- `spread_pct`: Alpaca latest quote의 bid/ask 중간값 대비 스프레드. 0.50% 이하여야 제출 가능하다.
- `quote_age_minutes`: 주문 계획 생성 시점 기준 quote 경과 시간. 정책상 20분 이하여야 한다.
- `research confirmations`: SEC EDGAR, Alpha Vantage, FRED, Firecrawl, Yahoo Finance 중 usable/pass로 확인된 provider 수. Buy 제출은 3개 이상이 필요하다.
- `risk_open_order_lifecycle`: stale unfilled autopilot order가 취소 또는 조정되지 않아 새 주문을 막는 상태. 이번 run에서는 발생하지 않았다.

## 제출 및 사후 점검

| Symbol | Client order id | Status | Filled qty | Fill price | 비고 |
| --- | --- | --- | ---: | ---: | --- |
| CVX | `hourly-20260528-2251-cvx-buy-01` | filled | 1 | 184.03 | Alpaca order-by-client-id와 FILL activity에서 확인 |
| NEE | `hourly-20260528-2251-nee-buy-01` | new/open | 0 |  | open orders reconciliation에서 확인 |
| NKE | `hourly-20260528-2251-nke-buy-01` | filled | 1 | 46.03 | FILL activity에서 확인 |

- 남은 open order: BAC prior open buy 1주 limit 50.89, NEE 1주 limit 88.00.
- Fresh account/positions post-submit refresh는 runtime safety monitor에서 `cancelled`; `gap_category=cancelled`로 manifest와 post-trade JSON에 기록했다.
- 체결된 CVX/NKE는 `회고 대기`로 표시한다. NEE는 미체결 open lifecycle follow-up 대상이다.
