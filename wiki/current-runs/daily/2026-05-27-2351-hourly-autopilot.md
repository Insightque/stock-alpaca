---
id: 2026-05-27-2351-hourly-autopilot
created_at: 2026-05-27T14:59:22Z
workflow: hourly-autopilot
paper: true
---

# 2026-05-27 23:51 KST Hourly Autopilot

## 실행 요약

- Paper mode: 환경에서 `ALPACA_PAPER_TRADE=true` 확인.
- Market clock: scheduler Alpaca preflight 기준 `2026-05-27T10:51:12.523545285-04:00`, 정규장 open, next close `2026-05-27T16:00:00-04:00`.
- Stale order cleanup: GOOGL stale autopilot order cancel attempt pass. Cleanup JSON에는 같은 주문이 `remaining_open_orders`에 남아 보였지만, 등록 Alpaca MCP `get_order_by_id` 직접 대조에서 `canceled`로 확인했다.
- Alpaca core MCP: scheduler preflight의 clock/account/positions/open orders/recent fills/assets/quotes/snapshots/trades pass. 보조 `get_orders(status=open)` 재시도는 `cancelled`로 기록하고 점수에는 쓰지 않았다.
- Research MCP: SEC EDGAR, FRED, Firecrawl, Yahoo Finance pass; Alpha Vantage는 `empty_response` gap. Buy actionability에 필요한 usable/pass 3개 이상은 충족.
- Universe: `harness/symbol-metadata.yaml`, 현재 포지션, Alpaca preflight universe, SPY/QQQ 포함 62개 loaded.

## 추천 Shortlist

| 순위 | 티커 | 판단 | 핵심 이유 | 제한 |
| ---: | --- | --- | --- | --- |
| 1 | V | 1주 validation buy | payments/growth_quality 분산, 0.0303% spread, 보유/동일일 buy 없음 | 당일 validation 주문 수를 보수적으로 1개 슬롯만 남김 |
| 2 | MS | recheck | financials 후보이나 BAC를 같은 세션에 이미 1주 매수 | 같은 cluster 추가 확대 보류 |
| 3 | QQQ | recheck | broad growth index 후보 | 1주 notional이 커서 최종 daily slot에는 V 우선 |
| - | GOOGL | skip canceled stale | 23:11 stale open buy는 cleanup 이후 canceled 확인 | 새 client id로 재시도하지 않음 |
| - | NKE/PFE/SO/WMT/NEE/AMZN/BAC/XOM | skip duplicate | 같은 ET 거래일 validation buy 체결 | same-day duplicate symbol/side 회피 |

## 주문 계획

| 티커 | 방향 | 수량 | 지정가 | 기준 quote | Spread | 주문 근거 |
| --- | --- | ---: | ---: | --- | ---: | --- |
| V | buy | 1 | 330.01 | `2026-05-27T14:51:34.409818476Z` | 0.0303% | payments/growth_quality 분산 validation, fresh quote, active/tradable asset |

## MCP Coverage Matrix

| MCP | queried | used_in_score | outcome | gap_category | source_refs |
| --- | --- | --- | --- | --- | --- |
| alpaca | true | true | pass | not_applicable | `wiki/evidence-store/sources/2026-05-27-2351-hourly-autopilot-alpaca-core-preflight.json` |
| sec-edgar | true | true | pass | not_applicable | `wiki/evidence-store/sources/2026-05-27-2351-hourly-autopilot-research-mcp-preflight.json` |
| alpha-vantage | true | false | gap | empty_response | `wiki/evidence-store/sources/2026-05-27-2351-hourly-autopilot-research-mcp-preflight.json` |
| fred | true | true | pass | not_applicable | `wiki/evidence-store/sources/2026-05-27-2351-hourly-autopilot-research-mcp-preflight.json` |
| firecrawl | true | true | pass | not_applicable | `wiki/evidence-store/sources/2026-05-27-2351-hourly-autopilot-research-mcp-preflight.json` |
| yahoo-finance | true | true | pass | not_applicable | `wiki/evidence-store/sources/2026-05-27-2351-hourly-autopilot-research-mcp-preflight.json` |
| alpaca supplemental get_orders | true | false | failed | cancelled | `wiki/evidence-store/sources/2026-05-27-2351-hourly-autopilot-alpaca-core-preflight.json` |

## 제출 전 Gate 상태

- Universe strict: PASS.
- MCP strict: PASS under tiered policy: Alpaca core pass, research usable/pass 4개.
- Risk policy: PASS. `buy_notional=330.01`, `post_cash=41175.98`, `post_invested=59904.13`.
- Quote freshness: 7.8분, 20분 정책 이내.
- Spread: 0.0303%, 0.50% 한도 이내.
- Order shape: whole-share long-only stock day limit order.
- Duplicate/open-order check: GOOGL stale order는 canceled 확인; `V`는 보유/동일일 buy/open buy 없음.

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
| V | `hourly-20260527-2351-v-buy-1` | submitted, `new` | 0/1 | day limit 330.01, client-order reconciliation pass |

Post-trade account snapshot: portfolio value 100727.49 USD, cash 41505.99 USD, buying power 135615.79 USD, long market value 59221.50 USD.

Open order after reconciliation: V buy 1 `new`, client_order_id `hourly-20260527-2351-v-buy-1`, submitted `2026-05-27T15:00:22.244592675Z`.

Post-trade source: `wiki/evidence-store/sources/2026-05-27-2351-hourly-autopilot-post-trade.json`.

Review due marker: V는 아직 미체결이라 fill 발생 후 `회고 대기`로 전환한다.
