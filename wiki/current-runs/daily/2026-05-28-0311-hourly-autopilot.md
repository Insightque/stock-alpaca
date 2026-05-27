---
id: 2026-05-28-0311-hourly-autopilot
created_at: 2026-05-27T18:13:50Z
workflow: hourly-autopilot
paper: true
---

# 2026-05-28 03:11 KST Hourly Autopilot

## 실행 요약

- Paper mode: 환경에서 `ALPACA_PAPER_TRADE=true` 확인.
- Market clock: scheduler cleanup/preflight 기준 `2026-05-27T14:11:11.515780299-04:00`, 정규장 open, next close `2026-05-27T16:00:00-04:00`.
- Stale order cleanup: `wiki/evidence-store/sources/2026-05-28-0311-hourly-autopilot-stale-order-cleanup.json` 기준 pass. Stale 후보, cancel attempt, remaining open autopilot order 모두 0건이다.
- Alpaca core MCP: scheduler preflight의 clock/account/positions/open orders/recent fills/assets/quotes/snapshots/trades pass. First Alpaca blocking gate는 없음.
- Research MCP: SEC EDGAR, FRED, Firecrawl, Yahoo Finance pass; Alpha Vantage는 `empty_response` gap. Buy actionability에 필요한 usable/pass 3개 이상은 충족했다.
- Universe: `harness/symbol-metadata.yaml`, 현재 포지션, Alpaca preflight universe, SPY/QQQ 포함 62개 loaded.
- 주문 판단: 이번 2026-05-27 ET 세션에서 scheduled validation buy order가 이미 10건 생성되어 daily validation order budget을 소진했다. 따라서 새 주문은 제출하지 않았다.

## 추천 Shortlist

| 순위 | 티커 | 판단 | 일중 변화 | spread | 핵심 제한 |
| ---: | --- | --- | ---: | ---: | --- |
| 1 | AMZN | skip_duplicate | 1.4127% | 0.0185% | same ET-session scheduled validation buy/fill already exists and daily validation order budget is exhausted |
| 2 | BAC | skip_duplicate | -2.1600% | 0.0195% | same ET-session scheduled validation buy/fill already exists and daily validation order budget is exhausted |
| 3 | V | skip_duplicate | 0.8152% | 0.0213% | same ET-session scheduled validation buy/fill already exists and daily validation order budget is exhausted |
| 4 | SO | skip_duplicate | 0.4063% | 0.0213% | same ET-session scheduled validation buy/fill already exists and daily validation order budget is exhausted |
| 5 | FCX | recheck_only | -1.2107% | 0.0158% | fresh quote/research candidate, but daily validation order budget blocks new validation buy |
| 6 | COP | recheck_only | 0.4123% | 0.0173% | fresh quote/research candidate, but daily validation order budget blocks new validation buy |
| 7 | SLB | recheck_only | -0.1235% | 0.0177% | fresh quote/research candidate, but daily validation order budget blocks new validation buy |
| 8 | SPY | recheck_only | -0.1365% | 0.0040% | fresh quote/research candidate, but daily validation order budget blocks new validation buy |
| 9 | QQQ | recheck_only | -0.6412% | 0.0069% | fresh quote/research candidate, but daily validation order budget blocks new validation buy |
| 10 | PLTR | recheck_only | -0.2364% | 0.0301% | fresh quote/research candidate, but daily validation order budget blocks new validation buy |
| 11 | NEE | skip_duplicate | 0.3563% | 0.0344% | same ET-session scheduled validation buy/fill already exists and daily validation order budget is exhausted |
| 12 | QBTS | recheck_only | 0.5882% | 0.0366% | fresh quote/research candidate, but daily validation order budget blocks new validation buy |

## 주문 계획

이번 run의 order-plan은 submit-mode context이지만 `orders: []`이다.

| 티커 | 방향 | 수량 | 지정가 | 상태 | 차단 사유 |
| --- | --- | ---: | ---: | --- | --- |
| AMZN/BAC/V/SO/NEE | buy | 0 | - | skipped | same-session validation buy/fill, `risk_daily_new_orders_budget` |
| FCX/COP/SLB/SPY/QQQ/PLTR/QBTS | buy | 0 | - | recheck only | daily validation order budget 소진 |

## MCP Coverage Matrix

| MCP | queried | used_in_score | outcome | gap_category | source_refs |
| --- | --- | --- | --- | --- | --- |
| alpaca | true | true | pass | not_applicable | `wiki/evidence-store/sources/2026-05-28-0311-hourly-autopilot-alpaca-core-preflight.json` |
| sec-edgar | true | true | pass | not_applicable | `wiki/evidence-store/sources/2026-05-28-0311-hourly-autopilot-research-mcp-preflight.json` |
| alpha-vantage | true | false | gap | empty_response | `wiki/evidence-store/sources/2026-05-28-0311-hourly-autopilot-research-mcp-preflight.json` |
| fred | true | true | pass | not_applicable | `wiki/evidence-store/sources/2026-05-28-0311-hourly-autopilot-research-mcp-preflight.json` |
| firecrawl | true | true | pass | not_applicable | `wiki/evidence-store/sources/2026-05-28-0311-hourly-autopilot-research-mcp-preflight.json` |
| yahoo-finance | true | true | pass | not_applicable | `wiki/evidence-store/sources/2026-05-28-0311-hourly-autopilot-research-mcp-preflight.json` |

## 제출 전 Gate 상태

- Paper mode: PASS.
- Market clock: PASS, `2026-05-27T14:11:11.515780299-04:00` open.
- Universe strict: PASS.
- MCP strict: PASS under tiered policy. Alpaca core pass, research usable/pass 4개.
- Quote freshness: shortlist quote rows are within 20 minutes at scheduler decision time; shortlist quote timestamps cluster around `2026-05-27T18:11:25Z ~ 2026-05-27T18:11:31Z`.
- Spread: selected shortlist spreads are present and below the 0.50% policy.
- Risk validator: PASS for empty order plan.
- Duplicate/open-order check: cleanup and Alpaca preflight both show no open autopilot orders; same-day duplicate and daily validation-order budget still block new buys.
- First blocking gate: `risk_daily_new_orders_budget`.

## 지표 설명

- `quote_age_minutes`: 주문 판단 시점과 Alpaca quote timestamp 사이의 시간이다. Submit mode에서는 20분 이내여야 한다.
- `spread_pct`: ask와 bid 차이를 중간값으로 나눈 비율이다. 낮을수록 지정가 체결 비용과 미체결 위험이 작다.
- `confidence_score`: trend, MCP 원천, 리스크, 포트폴리오 fit을 합친 내부 점수다. 0.50 이상이면 medium source confidence validation 후보가 될 수 있다.
- `expected_excess_return_20d_pct`: SPY 대비 20거래일 기대 초과수익 추정치다. 이번 run은 주문이 없어 산출 주문 필드에 기록하지 않았다.
- `expected_adverse_move_20d_pct`: 20거래일 안에 불리하게 움직일 수 있는 손실폭 추정치다.
- `review_horizons`: paper validation 주문을 1D/5D/20D 뒤에 회고해 정책 개선 자료로 쓰는 기간이다.

## 제출 및 사후 점검

| 티커 | client_order_id | 결과 | 체결 | 비고 |
| --- | --- | --- | --- | --- |
| - | - | submitted 없음 | - | daily validation order budget 소진으로 submit 생략 |

Post-trade reconciliation은 새 submit attempt가 없어서 주문 제출 후 재조회는 수행하지 않았다. 다만 이번 run은 same-day fills가 있어 scheduler Alpaca core preflight의 read-only account/positions/open orders/recent fills rows를 reconciliation source로 사용했다. Open order는 0건이며, 같은 ET 세션 fill은 V, XOM, BAC, AMZN, NEE, WMT, SO, PFE, NKE로 확인된다.

Review due markers: 이번 run 신규 체결 없음. 기존 validation fills는 1D/5D/20D 회고 대기 상태를 유지한다.
