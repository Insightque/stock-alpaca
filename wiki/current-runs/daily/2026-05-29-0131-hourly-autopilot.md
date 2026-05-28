---
id: 2026-05-29-0131-hourly-autopilot
created_at: 2026-05-28T16:33:00Z
workflow: hourly-autopilot
paper: true
---

# 2026-05-29 01:31 KST 정규장 hourly autopilot

## 실행 요약

- 실행 ID: `2026-05-29-0131-hourly-autopilot`
- 모드: `submit`, paper only
- 시장 시계: scheduler Alpaca core preflight 기준 `2026-05-28T12:31:17.475666018-04:00` ET open, next close `2026-05-28T16:00:00-04:00`
- stale order cleanup: `wiki/evidence-store/sources/2026-05-29-0131-hourly-autopilot-stale-order-cleanup.json` status `pass`, remaining open orders 없음.
- Alpaca core: scheduler preflight hard gate `pass`; clock/account/positions/open orders/recent activities/assets/quotes/snapshots/latest trades가 모두 passing row로 기록됐다. First Alpaca blocking gate는 없음.
- Research MCP: SEC EDGAR, FRED, Firecrawl, Yahoo Finance pass; Alpha Vantage는 `empty_response` gap. 최소 3개 research confirmation 충족.
- 주문 판단: 같은 ET 세션 정규장 신규 주문 수가 이미 `20/20`에 도달해 새 주문을 제출하지 않았다. 이번 run의 첫 차단 gate는 `risk_daily_new_orders_budget`이다.

## 추천 Shortlist

| 순위 | 티커 | 판단 | 핵심 근거 | 제한 |
| ---: | --- | --- | --- | --- |
| 1 | NVDA | recheck_only | AI 반도체 core 보유와 research preflight 확인은 유지됨 | daily new order cap 20/20 |
| 2 | QQQ | recheck_only | 성장주 벤치마크, fresh quote/research 확인 | daily new order cap 20/20 |
| 3 | AAPL | recheck_only | mega-cap quality 후보, fresh quote와 asset gate pass | daily new order cap 20/20 |
| 4 | NEE | recheck_only | defensive utility/energy transition 분산 후보 | daily new order cap 20/20 |
| 5 | WMT | recheck_only | defensive consumer 후보, Yahoo/Firecrawl 확인 | daily new order cap 20/20 |
| 6 | SLB | recheck_only | energy services 후보, 기존 소액 보유 | daily new order cap 20/20 |
| 7 | BAC | recheck_only | financials 분산 후보, same-session fill 이후 추가 매수 보류 | daily new order cap 20/20 |
| 8 | XOM | recheck_only | 직전 run에서 1주 체결, energy hedge 유지 | same-session fill 및 daily cap |

## 주문 계획

이번 run의 order-plan은 submit-mode context이지만 `orders: []`이다.

| 티커 | 방향 | 수량 | 지정가 | 상태 | 차단 사유 |
| --- | --- | ---: | ---: | --- | --- |
| NVDA/QQQ/AAPL/NEE/WMT/SLB/BAC/XOM | buy | 0 | - | skipped | `risk_daily_new_orders_budget`, same ET-session cap 20/20 |

## MCP Coverage Matrix

| MCP | queried | used_in_score | outcome | gap_category | source_refs |
| --- | --- | --- | --- | --- | --- |
| alpaca | true | true | pass | not_applicable | `wiki/evidence-store/sources/2026-05-29-0131-hourly-autopilot-alpaca-core-preflight.json` |
| sec-edgar | true | true | pass | not_applicable | `wiki/evidence-store/sources/2026-05-29-0131-hourly-autopilot-research-mcp-preflight.json` |
| alpha-vantage | true | false | gap | empty_response | `wiki/evidence-store/sources/2026-05-29-0131-hourly-autopilot-research-mcp-preflight.json` |
| fred | true | true | pass | not_applicable | `wiki/evidence-store/sources/2026-05-29-0131-hourly-autopilot-research-mcp-preflight.json` |
| firecrawl | true | true | pass | not_applicable | `wiki/evidence-store/sources/2026-05-29-0131-hourly-autopilot-research-mcp-preflight.json` |
| yahoo-finance | true | true | pass | not_applicable | `wiki/evidence-store/sources/2026-05-29-0131-hourly-autopilot-research-mcp-preflight.json` |

## Gate 상태

- Paper mode: `ALPACA_PAPER_TRADE=true`
- Market clock: PASS, 정규장 open.
- Universe gate: broad metadata universe 62개, SPY/QQQ 포함, strict PASS.
- MCP gate: Alpaca core pass + research 4/5 pass, Alpha Vantage `empty_response` gap 기록, strict PASS.
- Quote freshness: Alpaca quote rows are from `2026-05-28T16:31:38Z`~`2026-05-28T16:31:41Z`, submit freshness 한도 20분 이내.
- Spread: shortlist spread rows are present; 주문 후보는 daily cap에서 먼저 차단되어 추가 limit price를 만들지 않았다.
- Open-order lifecycle: scheduler stale cleanup pass, Alpaca open orders empty.
- Daily order cap: 이번 run 전 same ET-session 신규 주문 수 20건으로 계산되어 새 validation order 불가.
- Risk validator: PASS. Empty order plan 경고(`orders is empty`)만 있으며, 주문이 없으므로 submit 전 `place_stock_order` pre-submit summary는 발생하지 않는다.

## 제출 및 사후 점검

| 티커 | client_order_id | 결과 | 체결 | 비고 |
| --- | --- | --- | --- | --- |
| - | - | submitted 없음 | - | daily new order cap 20/20로 submit 생략 |

Post-trade reconciliation은 새 submit attempt가 없어서 주문 제출 후 재조회는 수행하지 않았다. 다만 이번 run은 same-day fills가 있어 scheduler Alpaca core preflight의 read-only account/positions/open orders/recent activities rows를 reconciliation source로 사용했다. Open order는 0건이며, 직전 XOM fill을 포함한 same-session fill activity가 preflight에 기록되어 있다.

Review due markers: 이번 run 신규 체결 없음. 기존 validation fills는 1D/5D/20D 회고 대기 상태를 유지한다.

## 지표 설명

- `quote_age_minutes`: 주문 판단 시점과 Alpaca quote timestamp 사이의 시간이다. Submit mode에서는 20분 이내여야 한다.
- `spread_pct`: ask와 bid 차이를 중간값으로 나눈 비율이다. 낮을수록 지정가 체결 비용과 미체결 위험이 작다.
- `confidence_score`: trend, MCP 원천, 리스크, 포트폴리오 fit을 합친 내부 점수다.
- `expected_excess_return_20d_pct`: SPY 대비 20거래일 기대 초과수익 추정치다. 이번 run은 주문이 없어 주문 필드에 기록하지 않았다.
- `review_horizons`: paper validation 주문을 1D/5D/20D 뒤에 회고해 정책 개선 자료로 쓰는 기간이다.
