---
id: 2026-05-27-0451-hourly-autopilot
created_at: 2026-05-26T19:53:30Z
workflow: hourly-autopilot
paper: true
orders_submitted: 0
---

# 2026-05-27 04:51 KST Hourly Paper Autopilot

## 결론

이번 20분 paper autopilot run은 주문을 제출하지 않았다. Alpaca core preflight, universe, quote freshness, spread, 그리고 research MCP 최소 3개 확인은 통과했지만, 기존 AMZN 미체결 buy order가 약 34.4분 동안 `new` 상태로 남아 있어 `risk_policy.order_lifecycle.max_open_order_age_minutes=30`을 초과했다. 첫 blocking gate는 `risk_open_order_lifecycle`이다.

`place_stock_order`는 호출하지 않았다.

## 시장/계좌 상태

| 항목 | 값 |
| --- | --- |
| Market clock | open, `2026-05-26T15:51:09.581579613-04:00` |
| Next close | `2026-05-26T16:00:00-04:00` |
| Portfolio value | 101738.22 USD |
| Cash | 42347.59 USD |
| Buying power | 137240.29 USD |
| Long market value | 59390.63 USD |
| 포지션 수 | 13 |
| 미체결 주문 | AMZN buy 1주, limit 263.10, status `new`, filled_qty 0 |

## 추천 Shortlist

| 순위 | 티커 | 판단 | 근거 | 상태 |
| ---: | --- | --- | --- | --- |
| 1 | INTC | validation buy 후보 | +2.88% intraday, quote age <20분, spread 0.0649%, SEC/FRED/Yahoo usable | risk gate 때문에 skip |
| 2 | SMH | recheck | spread 0.0133%, 반도체 breadth proxy로 유용 | 반도체 cluster 노출 부담 |
| 3 | AMAT | recheck | +5.29% intraday, spread 0.0462% | INTC보다 우선순위 낮고 risk gate blocked |

## MCP Coverage

| MCP | 결과 | 사용 | gap_category | 비고 |
| --- | --- | --- | --- | --- |
| Alpaca | pass | yes | not_applicable | scheduler core preflight hard gate pass |
| SEC EDGAR | pass | yes | not_applicable | local CIK `INTC -> 0000050863`, company info/recent filings pass |
| Alpha Vantage | failed | no | cancelled | PING pass 후 `TOOL_GET("NEWS_SENTIMENT")` cancelled |
| FRED | pass | yes | not_applicable | scheduler research preflight `get_macro_snapshot` pass |
| Firecrawl | failed | no | wrapper_error | Codex tool catalog에 registered Firecrawl tool 미노출 |
| Yahoo Finance | usable | yes | not_applicable | INTC news/recommendations usable |

## 주문/스킵

| 티커 | 방향 | 수량 | 지정가 | 결과 | 이유 |
| --- | --- | ---: | ---: | --- | --- |
| INTC | buy | 1 | 123.38 | skipped | AMZN open order lifecycle risk gate fail |

제출된 주문은 없다. 기존 AMZN open order는 preflight 기준 status `new`, filled_qty 0이며, 같은 날 LLY/FCX/NOK/NVDA/AAPL validation buy fill은 계속 회고 대기다.

## 검증 결과

| 검증 | 결과 |
| --- | --- |
| Universe strict | PASS |
| MCP strict | PASS |
| Risk check | FAIL: `AMZN: open order age 34.4 minutes exceeds lifecycle limit 30.0` |

## 산출물

- Source note: `wiki/evidence-store/sources/2026-05-27-0451-hourly-autopilot-sources.md`
- Run manifest: `wiki/evidence-store/run-manifests/2026-05-27-0451-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-05-27-0451-hourly-autopilot.json`

## 지표 설명

- `quote age`: Alpaca quote timestamp와 의사결정 시각 사이의 차이다. Submit-mode에서는 20분 이내여야 한다.
- `spread`: `(ask - bid) / midpoint`로 계산한 호가 비용이다. 0.5% 이내여야 신규 validation buy 후보가 될 수 있다.
- `research MCP confirmations`: SEC EDGAR, Alpha Vantage, FRED, Firecrawl, Yahoo Finance 중 usable/pass provider 수다. Buy 후보는 최소 3개가 필요하다.
- `open order lifecycle`: 기존 미체결 주문이 너무 오래 방치되어 중복/오염된 리스크 판단을 만들지 않도록 막는 gate다. 현재 한도는 30분이다.
