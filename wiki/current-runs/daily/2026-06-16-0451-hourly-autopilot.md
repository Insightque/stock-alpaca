# 2026-06-16-0451-hourly-autopilot scheduled paper autopilot

## 요약

정규장 scheduled hourly autopilot을 실행했다. `.env`의 `ALPACA_PAPER_TRADE=true` 요구는 유지됐고, scheduler-owned `0451` stale cleanup/core/research preflight를 source-of-record로 사용했다. stale cleanup은 open order `0`건, core preflight는 `market_open/account/positions/open_orders/recent_activities/quotes` hard gate를 모두 PASS로 기록했다. research preflight는 `sec-edgar`, `fred`, `yahoo-finance` positive confirmation을 유지했고 `alpha-vantage`는 `empty_response`, `firecrawl`은 credit 부족 `unknown` non-core gap으로 남았다.

이번 cycle은 sell-first 경로가 실제 체결로 이어졌다. `[[AVGO]]`와 `[[RGTI]]`는 각각 same-day duplicate sell discipline에 막혔고, buy fallback 쪽은 `AAPL/AMZN/BAC/COP/FCX/GOOGL/JPM/MSFT/NEE/NKE/SLB/SO/V/WMT/XOM` same-day duplicate buy, `SPY/QQQ` validation floor per-order cap, `INTC` ai_semiconductor cluster warning으로 비집행 상태였다. 반면 `[[PFE]]`는 반복 약세 review와 `2026-06-12` trim precedent가 이미 문서화돼 있고, direct Alpaca quote `26.01/26.02`, spread `0.0384%`, active tradable NYSE stock, same-day duplicate/open-order `0`를 충족해 floor-size risk-reducing trim 1주 후보로 승격했고, `client_order_id=hourly-20260616-0451-sell-pfe`는 `2026-06-15T19:59:48.06371096Z`에 `filled_avg_price=26.01 USD`로 즉시 체결됐다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env`의 `ALPACA_PAPER_TRADE=true` 확인 |
| Market clock pre-submit | PASS | direct `get_clock` timestamp `2026-06-15T15:58:55.814462809-04:00`, market open |
| Stale order lifecycle | PASS | scheduler cleanup pass, stale autopilot order 0건 |
| Alpaca core MCP | PASS | scheduler-owned core preflight hard gate pass + direct boundary recheck |
| Research MCP | PASS tiered | SEC EDGAR/FRED/Yahoo positive; Alpha `empty_response`, Firecrawl `unknown` non-core gap |
| Universe strict | PASS | metadata universe 62개, SPY/QQQ 포함 |
| Quote/spread | PASS for planned order | direct `PFE` quote `26.01/26.02`, spread `0.0384%`, freshness 약 `0.0`분 |
| Risk plan | PASS | `check-risk-policy.py --json` PASS |
| Final submit path | PASS | `place_stock_order` accepted, `get_order_by_client_id` 기준 `2026-06-15T19:59:48.06371096Z` `26.01 USD` filled |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| PFE | submitted_filled | 0.0384% | repeated weak validation reviews, prior trim precedent, same-day duplicate/open-order 0, direct quote pass |
| AVGO | watch_same_day_duplicate_sell | 0.0178% | `11:18 ET` same-day filled sell 이후 duplicate sell discipline 유지 |
| RGTI | watch_same_day_duplicate_sell | n/a | `09:41 ET` same-day filled sell 9주 이후 duplicate sell discipline 유지 |
| INTC | watch_cluster_warning | 0.0156% | ai_semiconductor_complex warning band와 prior weak thesis note로 buy fallback 후순위 |
| SPY | watch_notional_cap | 0.0027% | 1주 ask `753.82 USD`가 validation floor per-order cap 약 `513.27 USD` 초과 |
| QQQ | watch_notional_cap | 0.0027% | 1주 ask `742.93 USD`가 validation floor per-order cap 약 `513.27 USD` 초과 |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| PFE | trim_candidate | pass | repeated weak review 누적과 prior trim precedent, fresh quote/spread, same-day sell 0, open orders 0 |
| AVGO | watch | `duplicate_symbol_side_same_day` | same-session trim fill 이후 duplicate sell discipline 유지 |
| RGTI | watch | `duplicate_symbol_side_same_day` | same-session trim fill 9주가 있어 추가 trim 차단 |

## 주문 제출과 reconciliation

제출 전 게이트 요약은 아래와 같다.

paper mode `true`; market clock `2026-06-15T15:58:55.814462809-04:00`; order plan path `wiki/trade-ledger/orders/2026-06-16-0451-hourly-autopilot.json`; universe strict `PASS`; MCP strict `PASS`; risk validator `PASS`; PFE quote freshness 약 `0.0`분; spread `0.0384%`; order shape `sell 1 share / limit 26.01 / day / stock / regular`; duplicate/open-order check `PASS`; source refs는 `0451` stale cleanup/core/research preflight, `review-due-index`, `2026-06-15-portfolio-review`, `[[PFE]]`, `[[AVGO]]`, `[[RGTI]]`다.

| Symbol | Side | Qty | Limit | Status | Filled Avg | Order ID |
| --- | --- | ---: | ---: | --- | ---: | --- |
| PFE | sell | 1 | 26.01 | filled | 26.01 | `ee39d403-962f-45c1-856d-8289286d5ba8` |

immediate reconciliation 기준 `get_order_by_client_id`는 `PFE` 주문을 `status=filled`, `filled_qty=1`, `filled_avg_price=26.01 USD`로 반환했다. `get_all_positions` 기준 `PFE`는 `5주 @ 25.972`에서 `4주 @ 25.972`로 갱신됐고 `get_account_info` 기준 cash는 `29,810.35 USD -> 29,836.36 USD`, portfolio value는 `102,653.95 USD -> 102,596.60 USD`로 갱신됐다.

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | broad universe 62개, shortlist 7개 |
| `check-mcp-coverage.py --strict --json` | PASS | Alpaca core pass, positive research 3개, Alpha/Firecrawl non-core gap |
| `check-risk-policy.py --json` | PASS | PFE floor-size trim order plan 통과 |

## 산출물

- Report: `wiki/current-runs/daily/2026-06-16-0451-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-16-0451-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-16-0451-hourly-autopilot.json`
- Runtime gate evaluation: `wiki/evidence-store/sources/2026-06-16-0451-hourly-autopilot-runtime-gate-evaluation.json`
- Submit trace: `wiki/evidence-store/sources/2026-06-16-0451-hourly-autopilot-deterministic-submit.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-16-0451-hourly-autopilot-post-trade.json`

## 지표 설명

- `pass_tiered`: core MCP와 최소 research confirmation이 확보돼 일부 non-core provider gap이 있어도 submit 가능하다는 뜻이다.
- `duplicate_symbol_side_same_day`: 같은 세션에 이미 체결된 동일 symbol/side order가 있어 추가 학습 주문을 막는 규칙이다.
- `validation floor per-order cap`: `portfolio_value * 0.5%` 상한이다. 이번 cycle의 cap은 약 `513.27 USD`다.
