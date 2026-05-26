# 2026-05-27-0331-hourly-autopilot hourly autopilot

## 요약

2026-05-27 03:31 KST scheduled paper autopilot은 주문을 제출하지 않았다. Scheduler-owned Alpaca core preflight는 market open, account, positions, open orders, recent activities, quotes를 모두 `pass`로 제공했고 quote도 decision time 기준 20분 이내였다. 하지만 nested Codex shell에서 `ALPACA_PAPER_TRADE=true`가 확인되지 않아 workflow의 첫 hard gate인 paper mode가 실패했다.

- 첫 blocking gate: `paper_mode_env_missing`
- 제출 주문: 없음
- `place_stock_order` 호출: 없음
- 기존 open order: AAPL buy 1주 `new`, client_order_id `hourly-20260527-0251-aapl-buy-1`
- 리서치 MCP usable/pass: FRED, Yahoo Finance 2개. Submit buy 기준 3개 미달.
- Risk gate: FAIL, 기존 AAPL open order age 34.8분이 lifecycle limit 30분 초과.

## 계좌/시장 상태

| 항목 | 값 |
| --- | ---: |
| Market clock | 2026-05-26T14:31:10.242063192-04:00 open=True |
| Portfolio value | 101621.09 USD |
| Cash | 42657.04 USD |
| Buying power | 137380.24 USD |
| Positions | 12 |
| Open orders | 1 |

## 추천 Shortlist

| 순위 | Symbol | 판단 | 근거 | 주문 여부 |
| ---: | --- | --- | --- | --- |
| 1 | AMZN | 재점검 후보 | quote/spread pass, Yahoo news usable, SEC/Alpha filing/news 보강 실패 | 미제출: paper mode gate 실패 |
| 2 | INTC | 재점검 후보 | quote/spread pass, local CIK 확인, research MCP usable/pass 부족 | 미제출: paper mode gate 실패 |
| 3 | SMH | 재점검 후보 | ETF 분산 후보, quote/spread pass, SEC CIK lookup은 ETF 공백 | 미제출: paper mode gate 실패 |

## Quote/Spread Gate

| Symbol | Bid | Ask | Spread % | Quote time | 상태 |
| --- | ---: | ---: | ---: | --- | --- |
| AMZN | 263.26 | 263.29 | 0.0114 | 2026-05-26T18:31:31.02721451Z | pass |
| INTC | 122.39 | 122.42 | 0.0245 | 2026-05-26T18:31:32.126892757Z | pass |
| SMH | 600.18 | 600.47 | 0.0483 | 2026-05-26T18:31:32.580431757Z | pass |
| AAPL | 309.6 | 310.2 | 0.1936 | 2026-05-26T18:31:32.324221533Z | pass |
| MU | 906.81 | 912.5 | 0.6255 | 2026-05-26T18:31:32.617881386Z | fail |
| NVDA | 213.74 | 213.77 | 0.014 | 2026-05-26T18:31:32.658801539Z | pass |
| FCX | 64.17 | 64.19 | 0.0312 | 2026-05-26T18:31:31.246506057Z | pass |
| NOK | 16.42 | 16.43 | 0.0609 | 2026-05-26T18:31:32.506175072Z | pass |
| LLY | 1073 | 1081.96 | 0.8316 | 2026-05-26T18:31:32.400101831Z | fail |
| AMD | 498.51 | 500 | 0.2984 | 2026-05-26T18:31:30.823815325Z | pass |


## MCP Coverage

| MCP | 결과 | gap_category | 판단 반영 |
| --- | --- | --- | --- |
| Alpaca | pass | not_applicable | yes |
| SEC EDGAR | failed | cancelled | no |
| Alpha Vantage | failed | cancelled | no |
| FRED | pass | not_applicable | yes |
| Firecrawl | failed | wrapper_error | no |
| Yahoo Finance | usable | not_applicable | yes |

## 주문 계획

이번 run의 order plan은 submit mode 형식으로 생성했지만 `orders: []`이다. 모든 buy/sell 후보는 `paper_mode_env_missing` 때문에 skip했다. 기존 AAPL open buy order가 있어 duplicate/open-order check도 신규 AAPL buy를 막는다.

## 검증 상태

검증 명령 실행 결과: universe strict `PASS`, MCP strict `FAIL`, risk check `FAIL`. MCP strict는 research usable/pass가 FRED와 Yahoo Finance 2개뿐이라 submit 기준 3개에 미달했다. Risk check는 기존 AAPL open order age 34.8분이 lifecycle limit 30분을 초과해 실패했다. 신규 주문은 없고 `orders: []`이다.

## 지표 설명

- `spread %`: `(ask - bid) / midpoint * 100`. 0.5% 이내만 주문 후보로 본다.
- `MCP usable/pass`: 해당 provider 결과가 점수나 리스크 판단에 사용할 수 있는 상태다.
- `first_blocking_gate`: 주문 제출을 가장 먼저 막은 hard gate다. 이번 run은 paper mode 환경변수 미확인이다.
- `orders: []`: 주문 후보를 만들 수 없거나 hard gate가 실패해 제출할 주문이 없음을 뜻한다.

## 산출물

- Source note: `wiki/evidence-store/sources/2026-05-27-0331-hourly-autopilot-sources.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-05-27-0331-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-05-27-0331-hourly-autopilot.json`
