# 2026-06-16-0351-hourly-autopilot scheduled paper autopilot

## 요약

정규장 scheduled hourly autopilot을 실행했다. `.env`의 `ALPACA_PAPER_TRADE=true` 요구는 유지됐고, scheduler-owned `0351` stale cleanup/core/research preflight를 source-of-record로 사용했다. stale cleanup은 open order `0`건, core preflight는 `market_open/account/positions/open_orders/recent_activities/quotes` hard gate를 모두 PASS로 기록했다. research preflight는 `sec-edgar`, `fred`, `yahoo-finance` positive confirmation을 유지했고 `alpha-vantage`는 one-call throttle `provider_error`, `firecrawl`은 credit 부족 `unknown` non-core gap으로 남았다.

이번 cycle은 sell-first 경로를 다시 평가했지만 `AVGO`와 `RGTI`는 same-day duplicate sell discipline에, `SO`는 trim decision-grade metric gap에 막혀 executable risk-reducing sell로는 승격되지 못했다. buy fallback에서는 `WMT/BAC/NEE/JPM/FCX/SLB/XOM/NKE/COP/V/SO/MSFT`가 same-day duplicate buy 규율, `SPY/QQQ`가 validation floor per-order cap 약 `513.96 USD`, `NVDA`가 ai_semiconductor cluster warning, `AAPL/AMZN`이 반복 약세 review, `PLTR`이 speculative valuation noise로 후순위였다. `[[GOOGL]]`은 current research preflight shortlist 안에서 `SEC EDGAR/FRED/Yahoo Finance` 3-provider positive confirmation을 유지하고, preflight quote `371.21/371.26`, spread `0.0135%`, active tradable NASDAQ stock, same-day duplicate/open-order conflict 없음, 기존 mega-cap quality holding이라는 조건을 모두 충족해 이번 cycle floor-size learning buy 1주 후보로 승격했다. direct Alpaca MCP submit 이후 same `client_order_id=hourly-20260616-0351-buy-googl` reconciliation 기준 `filled_avg_price=371.22 USD`로 즉시 체결됐다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env`의 `ALPACA_PAPER_TRADE=true` 확인 |
| Market clock pre-submit | PASS | scheduler core preflight `get_clock` timestamp `2026-06-15T14:51:10.966756542-04:00`, hard gate `pass` |
| Stale order lifecycle | PASS | scheduler cleanup pass, stale autopilot order 0건 |
| Alpaca core MCP | PASS | scheduler-owned core preflight hard gate pass |
| Research MCP | PASS tiered | SEC EDGAR/FRED/Yahoo positive; Alpha throttle `provider_error`, Firecrawl `unknown` non-core gap |
| Universe strict | PASS | metadata universe 62개, SPY/QQQ 포함 |
| Quote/spread | PASS for planned order | preflight `GOOGL` quote `371.21/371.26`, spread `0.0135%`, freshness 약 `0.0`분 |
| Risk plan | PASS | `check-risk-policy.py --json` PASS |
| Final submit path | PASS | `place_stock_order` accepted, `get_order_by_client_id` 기준 `2026-06-15T18:58:47.524255326Z` `371.22 USD` filled |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| GOOGL | submitted_filled | 0.0135% | current research-preflight symbol, SEC/FRED/Yahoo 3-provider confirmation, same-day duplicate/open-order 0, mega-cap quality fallback |
| AAPL | watch_review_weak | 0.0135% | repeated weak-review history와 quality averaging-down 관찰 가설 유지 |
| AMZN | watch_review_weak | 0.0081% | repeated weak-review history와 cloud add cadence 약세 누적 |
| PLTR | watch_speculative_noise | 0.0149% | speculative_growth sleeve 변동성과 valuation noise로 quality fallback보다 후순위 |
| SPY | watch_notional_cap | 0.0026% | 1주 ask `755.14 USD`가 validation floor per-order cap 약 `513.96 USD` 초과 |
| QQQ | watch_notional_cap | 0.0242% | 1주 ask `744.01 USD`가 validation floor per-order cap 약 `513.96 USD` 초과 |
| NVDA | watch_cluster_warning | 0.0141% | ai_semiconductor_complex warning band로 add block 유지 |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| AVGO | watch | `duplicate_symbol_side_same_day` | same-session trim fill 이후 duplicate sell discipline 유지 |
| RGTI | watch | `duplicate_symbol_side_same_day` | same-session trim fill 9주가 있어 추가 trim 차단 |
| SO | watch | `sell_metric_gap` | decision-grade expected-excess/replacement margin 공백 지속 |

## 주문 제출과 reconciliation

paper mode `true`; market clock `2026-06-15T14:51:10.966756542-04:00`; order plan path `wiki/trade-ledger/orders/2026-06-16-0351-hourly-autopilot.json`; universe strict `PASS`; MCP strict `PASS`; risk validator `PASS`; GOOGL quote freshness 약 `0.0`분; spread `0.0135%`; order shape `buy 1 share / limit 371.26 / day / stock / regular`; duplicate/open-order check `PASS`; source refs는 `0351` stale cleanup/core/research preflight, runtime gate evaluation, `review-due-index`, `2026-06-15-portfolio-review`, `[[GOOGL]]`다.

| Symbol | Side | Qty | Limit | Status | Filled Avg | Order ID |
| --- | --- | ---: | ---: | --- | ---: | --- |
| GOOGL | buy | 1 | 371.26 | filled | 371.22 | `80ed6d6a-d85d-4da9-973a-ecfec099420f` |

immediate reconciliation 기준 `get_order_by_client_id`는 `GOOGL` 주문을 `status=filled`, `filled_qty=1`, `filled_avg_price=371.22 USD`로 반환했다. `get_all_positions` 기준 `GOOGL`은 `3주 @ 381.52`에서 `4주 @ 378.945`로 갱신됐다. 이 runtime에는 post-submit `get_account_info`가 노출되지 않아 cash는 pre-submit 현금 `30,723.87 USD`에서 confirmed fill `371.22 USD`를 차감한 `30,352.65 USD` 추정치로 기록한다.

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | broad universe 62개, shortlist 10개 |
| `check-mcp-coverage.py --strict --json` | PASS | Alpaca core pass, positive research 3개, Alpha/Firecrawl non-core gap |
| `check-risk-policy.py --json` | PASS | staged deployment warning only, hard gate 위반 없음 |

## 산출물

- Report: `wiki/current-runs/daily/2026-06-16-0351-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-16-0351-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-16-0351-hourly-autopilot.json`
- Runtime gate evaluation: `wiki/evidence-store/sources/2026-06-16-0351-hourly-autopilot-runtime-gate-evaluation.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-16-0351-hourly-autopilot-post-trade.json`

## 지표 설명

- `pass_tiered`: core MCP와 최소 research confirmation이 확보돼 일부 non-core provider gap이 있어도 submit 가능하다는 뜻이다.
- `duplicate_symbol_side_same_day`: 같은 세션에 이미 체결된 동일 symbol/side order가 있어 추가 buy/trim을 막는 규칙이다.
- `sell_metric_gap`: trim 판단에 필요한 expected-excess 또는 replacement margin이 비어 있어 집행형 trim으로 승격하지 못한 상태다.
- `validation floor per-order cap`: `portfolio_value * 0.5%` 상한이다. 이번 cycle의 cap은 약 `513.96 USD`다.
