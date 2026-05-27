---
id: 2026-05-27-2246-hourly-autopilot
created_at: 2026-05-27T13:49:30Z
workflow: hourly-autopilot
paper: true
orders_submitted: 3
---

# 2026-05-27 22:46 KST Hourly Paper Autopilot

## 결론

이번 20분 paper autopilot run은 scheduler-owned Alpaca core preflight, stale-order cleanup, universe, quote freshness, spread, tiered MCP, 그리고 risk gate를 모두 통과해 `NKE`, `PFE`, `SO` 각 1주 validation buy를 Alpaca MCP로 제출했다. 세 주문은 모두 filled로 체결됐고, post-trade reconciliation 기준 미체결 주문은 0건이다.

PFE의 첫 `place_stock_order` 호출은 wrapper safety cancellation으로 Alpaca 주문 객체를 반환하지 않았다. 같은 client order id `hourly-20260527-2246-pfe-buy-1`로 `get_order_by_client_id`를 조회해 404/not found를 확인했고, `get_orders(status=open)`에서도 관련 open order가 없음을 확인한 뒤 같은 client order id로 1회 재시도해 체결했다.

## 시장/계좌 상태

| 항목 | 값 |
| --- | --- |
| Market clock | open, `2026-05-27T09:46:40.303390074-04:00` |
| Next close | `2026-05-27T16:00:00-04:00` |
| Portfolio value | 100985.47 USD |
| Cash | 42347.59 USD |
| Buying power | 137078.27 USD |
| Long market value | 58637.88 USD |
| 포지션 수 | 13 |
| 미체결 주문 | 0 |

## 추천 Shortlist

| 순위 | 티커 | 판단 | 근거 | 상태 |
| ---: | --- | --- | --- | --- |
| 1 | NKE | validation buy | +2.90% intraday, spread 0.0216%, consumer discretionary 분산 | filled |
| 2 | PFE | validation buy | +2.44% intraday, spread 0.0378%, defensive healthcare 분산 | filled |
| 3 | SO | validation buy | +0.32% intraday, spread 0.0635%, utility defensive 분산 | filled |
| 4 | AMZN | recheck | research 확인은 강하지만 새 분산 우선순위에서 후순위 | skip |
| 5 | PLTR | recheck | Yahoo/news 확인은 있으나 speculative flag와 당일 약세 | skip |

## MCP Coverage

| MCP | 결과 | 사용 | gap_category | 비고 |
| --- | --- | --- | --- | --- |
| Alpaca | pass | yes | not_applicable | scheduler core preflight hard gate pass |
| SEC EDGAR | pass | yes | not_applicable | scheduler lightweight filings/company evidence, local CIK fallback policy 적용 |
| Alpha Vantage | gap | no | empty_response | `NEWS_SENTIMENT` candidate feed 0건 |
| FRED | pass | yes | not_applicable | scheduler macro snapshot pass |
| Firecrawl | pass | yes | not_applicable | scheduler scrape evidence pass |
| Yahoo Finance | pass | yes | not_applicable | recommendations/news evidence pass |

## 주문/스킵

| 티커 | 방향 | 수량 | 지정가 | 결과 | 이유 |
| --- | --- | ---: | ---: | --- | --- |
| NKE | buy | 1 | 46.25 | filled @ 46.15 | Alpaca MCP order `47826e52-14ed-437d-b8db-c55a0e255bf9` |
| PFE | buy | 1 | 26.46 | filled @ 26.34 | 첫 submit wrapper-cancelled 후 same client id reconciliation/retry, order `230a1212-7660-40ed-a12d-b2ad73c1b59e` |
| SO | buy | 1 | 94.52 | filled @ 94.28 | Alpaca MCP order `958582ba-cdaa-4be0-942e-27da20cc6daa` |

## 검증 결과

| 검증 | 결과 |
| --- | --- |
| Universe strict | PASS |
| MCP strict | PASS |
| Risk check | PASS: buy notional 167.23 USD, post-cash 42180.36 USD, post-invested 58799.48 USD |

## Post-Trade Reconciliation

| 항목 | 결과 |
| --- | --- |
| NKE | filled 1주 @ 46.15, client_order_id `hourly-20260527-2246-nke-buy-1` |
| PFE | filled 1주 @ 26.34, client_order_id `hourly-20260527-2246-pfe-buy-1` |
| SO | filled 1주 @ 94.28, client_order_id `hourly-20260527-2246-so-buy-1` |
| Open orders | 0 |
| Portfolio value | 101385.20 USD |
| Cash | 42180.82 USD |
| Long market value | 59204.38 USD |
| Review due | NKE/PFE/SO 모두 `회고 대기`: 1D/5D/20D |

- Post-trade source: `wiki/evidence-store/sources/2026-05-27-2246-hourly-autopilot-post-trade.json`

## 산출물

- Source note: `wiki/evidence-store/sources/2026-05-27-2246-hourly-autopilot-sources.md`
- Run manifest: `wiki/evidence-store/run-manifests/2026-05-27-2246-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-05-27-2246-hourly-autopilot.json`
- Post-trade source: `wiki/evidence-store/sources/2026-05-27-2246-hourly-autopilot-post-trade.json`

## 지표 설명

- `quote age`: Alpaca quote timestamp와 의사결정 시각 사이의 차이다. Submit-mode에서는 20분 이내여야 한다.
- `spread`: `(ask - bid) / midpoint`로 계산한 호가 비용이다. 0.5% 이내여야 신규 validation buy 후보가 될 수 있다.
- `research MCP confirmations`: SEC EDGAR, Alpha Vantage, FRED, Firecrawl, Yahoo Finance 중 usable/pass provider 수다. Buy 후보는 최소 3개가 필요하다.
- `open order lifecycle`: 기존 미체결 주문이 너무 오래 방치되어 중복/오염된 리스크 판단을 만들지 않도록 막는 gate다. 현재 한도는 30분이다.
