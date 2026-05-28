# 2026-05-28-2231-hourly-autopilot scheduled paper autopilot

## 요약

- 시장 시계: Alpaca MCP scheduler preflight 기준 `2026-05-28T09:31:17.465151556-04:00` open=true, next_close `2026-05-28T16:00:00-04:00`.
- 계좌: portfolio value `$101,596.22`, cash `$41,043.79`, invested ratio `59.60%`, cash ratio `40.40%`.
- Scheduler stale-order cleanup: status `pass`, stale candidates `0`, cancel attempts `0`, remaining open orders `0`. Stale autopilot order는 남아 있지 않다.
- MCP coverage: Alpaca core PASS. SEC EDGAR, FRED, Firecrawl, Yahoo Finance PASS. Alpha Vantage는 candidate news 0건으로 `empty_response` gap이며 점수에는 미사용했다.
- Universe gate: 62개 metadata universe와 SPY/QQQ benchmark 포함, strict coverage 대상 통과 예정.
- 주문 계획: PLTR, QQQ, BAC 각 1주 regular-session day limit buy. 제출 전 validator 3종을 통과해야 한다.

## 추천 Shortlist

| Rank | Symbol | 결정 | Spread % | Intraday % | 전일대비 % |
| ---: | --- | --- | ---: | ---: | ---: |
| 1 | PLTR | submit_candidate | 0.088659 | 1.540 | 2.061 |
| 2 | RGTI | recheck_only | 0.120265 | 0.302 | 1.259 |
| 3 | QQQ | submit_candidate | 0.082128 | 0.155 | 0.184 |
| 4 | META | recheck_only | 0.085917 | -0.158 | 0.532 |
| 5 | AAPL | recheck_only | 0.035436 | -0.060 | -0.164 |
| 6 | BAC | submit_candidate | 0.058968 | 0.020 | -0.391 |
| 7 | NEE | recheck_only | 0.079849 | -0.267 | -0.006 |
| 8 | WMT | recheck_only | 0.185326 | -0.252 | 0.110 |
| 9 | PFE | recheck_only | 0.115053 | -0.306 | -0.458 |
| 10 | NOK | recheck_only | 0.063877 | -0.698 | -0.191 |

## 주문 판단

- PLTR: 상대강도와 intraday follow-through가 가장 강하지만 speculative_growth 노출이므로 1주 검증 매수로 제한한다.
- QQQ: broad index 노출로 단일 테마 집중을 낮추는 분산 후보이며 spread와 quote freshness가 정책 안에 있다.
- BAC: financials cluster 분산 후보로, quote/spread와 source confidence가 양호하다.
- RGTI는 양호한 모멘텀이지만 quantum_speculative 기존 노출이 있어 이번 regular-session 신규 주문에서는 후순위 recheck로 남긴다.
- 매도/trim: thesis-break, overweight, stale-thesis underperformance, speculative loss-control 조건을 이번 preflight evidence만으로 확인하지 못했다. 신규 매수 후보보다 순위가 낮다는 이유만으로 매도하지 않는다.

## MCP Coverage Matrix

| MCP | queried | used_in_score | outcome | gap_category | source_refs |
| --- | --- | --- | --- | --- | --- |
| alpaca | true | true | pass | not_applicable | wiki/evidence-store/sources/2026-05-28-2231-hourly-autopilot-alpaca-core-preflight.json |
| sec-edgar | true | true | pass | not_applicable | wiki/evidence-store/sources/2026-05-28-2231-hourly-autopilot-research-mcp-preflight.json |
| alpha-vantage | true | false | gap | empty_response | wiki/evidence-store/sources/2026-05-28-2231-hourly-autopilot-research-mcp-preflight.json |
| fred | true | true | pass | not_applicable | wiki/evidence-store/sources/2026-05-28-2231-hourly-autopilot-research-mcp-preflight.json |
| firecrawl | true | true | pass | not_applicable | wiki/evidence-store/sources/2026-05-28-2231-hourly-autopilot-research-mcp-preflight.json |
| yahoo-finance | true | true | pass | not_applicable | wiki/evidence-store/sources/2026-05-28-2231-hourly-autopilot-research-mcp-preflight.json |


## 제출 전 상태

- Universe validator: PASS (`--strict`).
- MCP coverage validator: PASS (`--strict`).
- Risk policy validator: PASS (`--json`), planned buy notional `$917.17`.
- Submit: validators PASS 이후 Alpaca MCP `place_stock_order`만 사용한다.


## 제출 및 사후 점검

| Symbol | Client Order ID | Alpaca Order ID | 상태 | Fill Qty | Fill Price | 비고 |
| --- | --- | --- | --- | ---: | ---: | --- |
| PLTR | `hourly-20260528-2231-pltr-buy-01` | `9deb7a5f-74a6-422a-a8bd-053671ffd6f0` | filled | 1 | 134.94 | regular-session day limit buy 체결 |
| QQQ | `hourly-20260528-2231-qqq-buy-01` | `5ba5a3e8-e003-4e09-9d6e-0a726d8db818` | filled | 1 | 728.36 | 첫 submit call은 runtime `cancelled`; 같은 client_order_id 조회 404 후 같은 id로 1회 재시도, 체결 |
| BAC | `hourly-20260528-2231-bac-buy-01` | `23502ad0-37f0-4705-a110-8fc5b2059d4f` | open/new | 0 | - | day limit buy 미체결, open order로 추적 |

- Post-trade reconciliation: client-order-id별 조회 PASS, open orders 조회 PASS, recent fill activities 조회 PASS.
- Post-trade gap: fresh account refresh와 full positions refresh는 Alpaca MCP runtime safety monitor에서 `cancelled` 처리되어 `gap_category=cancelled`로 기록했다. 계좌/포지션 전체값은 scheduler core preflight snapshot을 기준으로 두 fill과 BAC open order delta를 별도 표시한다.
- Review due: PLTR, QQQ는 신규 체결로 `회고 대기`; BAC는 open order lifecycle 추적 대상이다.

## 지표 설명

- `Spread %`: Alpaca latest quote의 ask-bid를 중간가격으로 나눈 값이다. submit 후보는 0.50% 이하만 허용한다.
- `Intraday %`: 당일 daily bar open 대비 latest trade 가격 변화율이다. 단독 매수 신호가 아니라 후보 정렬과 리스크 확인에만 사용한다.
- `전일대비 %`: 전일 daily close 대비 latest trade 가격 변화율이다.
- `MCP coverage`: Alpaca core와 SEC EDGAR, Alpha Vantage, FRED, Firecrawl, Yahoo Finance evidence의 사용 가능 여부다. Buy 후보는 Alpaca core pass와 research provider 3개 이상 pass/usable이 필요하다.
- `quote_age_minutes`: 주문 계획의 기준 시각과 Alpaca latest quote timestamp 사이의 분 단위 차이다.
