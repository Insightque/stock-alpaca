---
id: 2026-05-27-2331-hourly-autopilot
created_at: 2026-05-27T14:35:00Z
workflow: hourly-autopilot
paper: true
---

# 2026-05-27 23:31 KST Hourly Autopilot

## 실행 요약

- Paper mode: 환경에서 `ALPACA_PAPER_TRADE=true` 확인.
- Market clock: scheduler Alpaca preflight 기준 `2026-05-27T10:31:12.444299543-04:00`, 정규장 open, next close `2026-05-27T16:00:00-04:00`.
- Stale order cleanup: pass. stale autopilot order 0건, fresh GOOGL open buy 1건은 risk `open_orders`에 반영.
- Alpaca core MCP: clock/account/positions/open orders/recent fills/assets/quotes/snapshots/trades pass.
- Research MCP: SEC EDGAR, FRED, Firecrawl, Yahoo Finance pass; Alpha Vantage는 `empty_response` gap. Buy actionability에 필요한 usable/pass 3개 이상은 충족.
- Universe: `harness/symbol-metadata.yaml`, 현재 포지션, Alpaca preflight universe, SPY/QQQ 포함 62개 loaded.

## 추천 Shortlist

| 순위 | 티커 | 판단 | 핵심 이유 | 제한 |
| ---: | --- | --- | --- | --- |
| 1 | AMZN | 1주 validation buy | mega_cap_tech quality growth 보강, 0.0111% spread | GOOGL open buy와 같은 클러스터라 1주로 제한 |
| 2 | BAC | 1주 validation buy | financials/bank_rate_sensitive 분산, 0.0192% spread | rate-sensitive 변동성은 validation size로 제한 |
| 3 | XOM | 1주 validation buy | energy/commodity_cyclical 분산, 0.0204% spread | FCX와 광의 commodity exposure가 있어 1주로 제한 |
| - | GOOGL | skip open order | 23:11 run의 buy 1주가 fresh open 상태 | duplicate/open-order gate 회피 |
| - | NKE/PFE/SO/WMT/NEE | skip duplicate | 같은 ET 거래일에 validation buy 체결 | same-day duplicate symbol/side 회피 |

## 주문 계획

| 티커 | 방향 | 수량 | 지정가 | 기준 quote | Spread | 주문 근거 |
| --- | --- | ---: | ---: | --- | ---: | --- |
| AMZN | buy | 1 | 270.20 | `2026-05-27T14:31:38.32286292Z` | 0.0111% | quality growth validation, tight spread, small notional |
| BAC | buy | 1 | 52.19 | `2026-05-27T14:31:38.216811192Z` | 0.0192% | financials diversification, low per-order notional |
| XOM | buy | 1 | 147.15 | `2026-05-27T14:31:39.712243151Z` | 0.0204% | energy diversification, tight spread |

## MCP Coverage Matrix

| MCP | queried | used_in_score | outcome | gap_category | source_refs |
| --- | --- | --- | --- | --- | --- |
| alpaca | true | true | pass | not_applicable | `wiki/evidence-store/sources/2026-05-27-2331-hourly-autopilot-alpaca-core-preflight.json` |
| sec-edgar | true | true | pass | not_applicable | `wiki/evidence-store/sources/2026-05-27-2331-hourly-autopilot-research-mcp-preflight.json` |
| alpha-vantage | true | false | gap | empty_response | `wiki/evidence-store/sources/2026-05-27-2331-hourly-autopilot-research-mcp-preflight.json` |
| fred | true | true | pass | not_applicable | `wiki/evidence-store/sources/2026-05-27-2331-hourly-autopilot-research-mcp-preflight.json` |
| firecrawl | true | true | pass | not_applicable | `wiki/evidence-store/sources/2026-05-27-2331-hourly-autopilot-research-mcp-preflight.json` |
| yahoo-finance | true | true | pass | not_applicable | `wiki/evidence-store/sources/2026-05-27-2331-hourly-autopilot-research-mcp-preflight.json` |

## 제출 전 Gate 상태

- Universe strict: PASS.
- MCP strict: PASS.
- Risk policy: PASS. `buy_notional=469.54`, `post_cash=41505.63`, `post_invested=59197.36`.
- Quote freshness: 약 3.3~3.4분, 20분 정책 이내.
- Spread: 0.0111%~0.0204%, 0.50% 한도 이내.
- Order shape: whole-share long-only stock day limit orders.
- Duplicate/open-order check: GOOGL fresh open buy 1건 존재하므로 GOOGL 추가 buy 제외. 같은 ET 거래일 buy 체결 종목은 제외.

## 지표 설명

- `quote_age_minutes`: 주문 판단 시점과 Alpaca quote timestamp 사이의 시간이다. Submit mode에서는 20분 이내여야 한다.
- `spread_pct`: ask와 bid 차이를 중간값으로 나눈 비율이다. 낮을수록 지정가 체결 비용과 미체결 위험이 작다.
- `confidence_score`: trend, MCP 원천, 리스크, 포트폴리오 fit을 합친 내부 점수다. 0.50 이상이면 medium source confidence validation 후보가 될 수 있다.
- `expected_excess_return_20d_pct`: SPY 대비 20거래일 기대 초과수익 추정치다. 실제 수익 보장이 아니라 후보 간 우선순위 입력값이다.
- `expected_adverse_move_20d_pct`: 20거래일 안에 불리하게 움직일 수 있는 손실폭 추정치다.
- `review_horizons`: paper validation 주문을 1D/5D/20D 뒤에 회고해 정책 개선 자료로 쓰는 기간이다.

## 제출 및 사후 점검

| 티커 | client_order_id | 결과 | 체결 | 비고 |
| --- | --- | --- | --- | --- |
| AMZN | `hourly-20260527-2331-amzn-buy-1` | submitted, `filled` | 1/1 @ 270.05 | day limit 270.20, client-order reconciliation pass |
| BAC | `hourly-20260527-2331-bac-buy-1` | submitted, `filled` | 1/1 @ 52.06 | day limit 52.19, client-order reconciliation pass |
| XOM | `hourly-20260527-2331-xom-buy-1` | submitted, `filled` | 1/1 @ 147.07 | day limit 147.15, client-order reconciliation pass |

Post-trade account snapshot: portfolio value 100853.90 USD, cash 41505.99 USD, buying power 135667.60 USD, long market value 59347.91 USD.

Open order after reconciliation: GOOGL buy 1 `new`, client_order_id `hourly-20260527-2311-googl-buy-1`, submitted `2026-05-27T14:17:31.432099441Z`. 다음 stale-order cleanup에서 lifecycle를 다시 확인해야 한다.

Post-trade source: `wiki/evidence-store/sources/2026-05-27-2331-hourly-autopilot-post-trade.json`.

Review due markers: AMZN/BAC/XOM `회고 대기` for 1D/5D/20D analyst review.
