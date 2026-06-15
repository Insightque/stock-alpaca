# 2026-06-16-0331-hourly-autopilot scheduled paper autopilot

## 요약

정규장 scheduled hourly autopilot을 실행했다. `.env`의 `ALPACA_PAPER_TRADE=true` 요구는 유지됐고, scheduler-owned `0331` stale cleanup/core/research preflight를 source-of-record로 사용했다. stale cleanup은 open order `0`건, core preflight는 `market_open/account/positions/open_orders/recent_activities/quotes` hard gate를 모두 PASS로 기록했다. direct Alpaca continuity check에서는 `2026-06-15 14:33:41 ET` regular market open, account `ACTIVE`, open orders `0`, 그리고 직전 `0311` cycle의 `SO` buy 1주가 `2026-06-15T18:30:03Z`에 `filled`로 전환됐음을 재확인했다.

이번 cycle은 sell-first 경로를 다시 평가했지만 `AVGO`와 `RGTI`는 same-day duplicate sell discipline에, `SO`는 trim decision-grade metric gap에 막혀 executable risk-reducing sell로는 승격되지 못했다. buy fallback에서는 `WMT/BAC/NEE/JPM/FCX/SLB/XOM/NKE/COP/V/SO`가 same-day duplicate buy 규율, `SPY/QQQ`가 validation floor per-order cap 약 `513.97 USD`, `NVDA`가 ai_semiconductor cluster warning, `AAPL/AMZN`이 반복 약세 review, `MCD`가 thesis evidence 부족으로 후순위였다. `[[MSFT]]`는 current research preflight shortlist 안에서 `SEC EDGAR/FRED/Yahoo Finance` 3-provider positive confirmation을 유지하고, direct quote `398.63/399.55`, spread `0.2303%`, active tradable NASDAQ stock, same-day duplicate/open-order conflict 없음, 기존 mega-cap quality holding이라는 조건을 모두 충족해 이번 cycle floor-size learning buy 1주 후보로 승격했다. direct Alpaca MCP submit 이후 same `client_order_id=hourly-20260616-0331-buy-msft` reconciliation 기준 `filled_avg_price=398.71 USD`로 즉시 체결됐다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env` paper-only context 유지 |
| Market clock | PASS | direct Alpaca clock `2026-06-15T14:33:41.842387607-04:00`, regular market open |
| Stale order cleanup | PASS | scheduler cleanup `status=pass`, remaining open order `0` |
| Alpaca core MCP | PASS | scheduler-owned core preflight hard gate `pass`, direct continuity도 account/open order/positions 정상 |
| Research MCP | PASS tiered | SEC EDGAR/FRED/Yahoo positive, Alpha `empty_response` gap, Firecrawl credit gap only |
| Universe strict | PASS | metadata universe `62`개, `SPY/QQQ` 포함 |
| Quote/spread | PASS | `MSFT` direct quote `398.63/399.55`, spread `0.2303%`, freshness 약 `0.0`분 |
| Risk plan | PASS | `check-risk-policy.py --json` PASS |
| Final submit path | READY | same-day duplicate/open-order `0`, whole-share day-limit stock, validation floor size |

## 후보와 판단

| Symbol | 판단 | 이유 |
| --- | --- | --- |
| MSFT | selected_validation_buy | existing mega-cap quality fallback, current research-preflight symbol, SEC/FRED/Yahoo 3-provider positive confirmation, same-day duplicate/open-order 0 |
| SO | watch | `0311` buy 1주가 `14:30 ET`에 filled로 전환돼 same-day duplicate buy 상태 |
| AAPL | watch | repeated weak-review history와 quality averaging-down 관찰 가설 유지 |
| AMZN | watch | repeated weak-review history와 cloud add cadence 약세 누적 |
| MCD | watch | reusable ticker thesis evidence 부족 |
| SPY | watch | 1주 ask `754.82 USD`가 validation floor per-order cap 약 `513.97 USD` 초과 |
| QQQ | watch | 1주 ask `743.27 USD`가 validation floor per-order cap 약 `513.97 USD` 초과 |
| NVDA | watch | ai_semiconductor_complex warning-band add block |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| AVGO | watch | `duplicate_symbol_side_same_day` | ai_semiconductor warning band와 음수 expected excess는 남지만 same-day trim fill 때문에 추가 sell 차단 |
| RGTI | watch | `duplicate_symbol_side_same_day` | speculative loss-control trim trigger는 남지만 same-day filled trim 때문에 추가 sell 차단 |
| SO | watch | `sell_metric_gap` | same-day filled buy가 생겼지만 그보다 먼저 trim decision-grade metric gap이 지속 |

## 주문/체결

### 제출 전 게이트 요약

paper mode `true`; market clock `2026-06-15T14:33:41.842387607-04:00`; order plan path `wiki/trade-ledger/orders/2026-06-16-0331-hourly-autopilot.json`; universe strict `PASS`; MCP strict `PASS`; risk validator `PASS`; MSFT quote freshness 약 `0.0`분; spread `0.2303%`; order shape `buy 1 share / limit 399.55 / day / stock / regular`; duplicate/open-order check `PASS`; source refs는 `0331` stale cleanup/core/research preflight, runtime gate evaluation, `review-due-index`, `2026-06-15-portfolio-review`, `[[MSFT]]`다.

| Symbol | Side | Qty | Limit | Status | Filled Avg | Order ID |
| --- | --- | ---: | ---: | --- | ---: | --- |
| MSFT | buy | 1 | 399.55 | filled | 398.71 | `6917414a-a128-4119-9e1a-2a133484c335` |

## Reconciliation

immediate reconciliation 기준 `get_order_by_client_id`와 `get_orders(status=all, symbols=MSFT, after=2026-06-15T18:35:00Z)` 모두 `MSFT` 주문을 `status=filled`, `filled_qty=1`, `filled_avg_price=398.71 USD`로 반환했다. direct `get_orders(status=open)` 기준 open orders는 `0`건이며, `get_account_info/get_all_positions` 기준 account `ACTIVE`, cash `30723.87 USD`, portfolio value `102794.12 USD`, positions `33`건, `MSFT qty=3 -> 4`, `avg_entry_price=404.935 USD`로 반영됐다.

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | broad universe 62개, shortlist 10개 |
| `check-mcp-coverage.py --strict --json` | PASS | Alpaca core pass, positive research 3개, Alpha/Firecrawl non-core gap |
| `check-risk-policy.py --json` | PASS | staged deployment warning only, hard gate 위반 없음 |

## 산출물

- Report: `wiki/current-runs/daily/2026-06-16-0331-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-16-0331-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-16-0331-hourly-autopilot.json`
- Runtime gate evaluation: `wiki/evidence-store/sources/2026-06-16-0331-hourly-autopilot-runtime-gate-evaluation.json`
- Submit trace: `wiki/evidence-store/sources/2026-06-16-0331-hourly-autopilot-deterministic-submit.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-16-0331-hourly-autopilot-post-trade.json`

## 지표 설명

- `pass_tiered`: core MCP와 최소 research confirmation이 확보돼 일부 non-core provider gap이 있어도 submit 가능하다는 뜻이다.
- `duplicate_symbol_side_same_day`: 같은 세션에 이미 체결된 동일 symbol/side order가 있어 추가 학습 주문을 막는 규칙이다.
- `sell_metric_gap`: trim 판단에 필요한 expected-excess 또는 replacement margin이 비어 있어 집행형 trim으로 승격하지 못한 상태다.
- `validation floor per-order cap`: `portfolio_value * 0.5%` 상한이다. 이번 cycle의 cap은 약 `513.97 USD`다.

- `place_stock_order` actual submit: `2026-06-15T18:39:13.500811516Z`
- `get_order_by_client_id` immediate reconciliation: `status=filled`, `filled_qty=1`, `filled_avg_price=398.71 USD`
- `get_orders(status=open)` immediate reconciliation: `0`건
- `get_all_positions` immediate reconciliation: `MSFT qty=4`, `avg_entry_price=404.935`, positions 총 `33`건
- `get_account_info` immediate reconciliation: cash `30723.87 USD`, portfolio value `102794.12 USD`
