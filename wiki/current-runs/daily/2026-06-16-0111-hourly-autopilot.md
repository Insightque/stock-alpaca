# 2026-06-16-0111-hourly-autopilot scheduled paper autopilot

## 요약

정규장 scheduled hourly autopilot을 실행했다. `.env`의 `ALPACA_PAPER_TRADE=true` 요구는 scheduler workflow 컨텍스트와 preflight 증거로 유지됐고, scheduler-owned `0111` stale cleanup/core/research preflight를 source-of-record로 사용했다. stale cleanup은 open order `0`건, core preflight는 `market_open/account/positions/open_orders/recent_activities/quotes` hard gate를 모두 PASS로 기록했다. direct Alpaca submit-boundary check도 `2026-06-15 12:15:52 ET` regular market open, account `ACTIVE`, open orders `0`, same-day `FCX` orders `0`를 재확인했다.

이번 cycle은 sell-first 경로를 다시 평가했지만 `AVGO`와 `RGTI`는 same-day duplicate sell discipline에, `SO`는 trim decision-grade metric gap에 막혔다. buy fallback에서는 `NEE/BAC/WMT/JPM`이 same-day duplicate buy 규율, `SPY/QQQ`가 validation floor per-order cap, `AMZN/NKE`가 mixed weak-review history, `XOM/SLB/PLTR`가 상대 순위에서 `FCX`보다 후순위였다. `FCX`는 existing materials/copper diversifier holding으로 2026-06-13 analyst review 5D가 `SPY` 대비 `+4.42%p`로 가장 강했고, research preflight에서 `SEC EDGAR/FRED/Yahoo Finance` 3-provider positive confirmation을 유지하며, direct quote `69.48/69.49`, spread `0.0144%`, active tradable NYSE stock, same-day duplicate/open-order conflict 없음 조건을 충족해 floor-size learning buy 1주 후보로 승격됐다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | scheduler workflow authorization 및 preflight evidence 기준 paper-only context 유지 |
| Market clock | PASS | direct Alpaca clock `2026-06-15T12:15:52.699072615-04:00`, regular market open |
| Stale order cleanup | PASS | scheduler cleanup `status=pass`, stale candidate `0`, remaining open order `0` |
| Alpaca core MCP | PASS | scheduler-owned core preflight hard gate `pass`, positions `33`, open orders row `0` |
| Research MCP | PASS tiered | SEC EDGAR/FRED/Yahoo positive, Alpha `empty_response`, Firecrawl `unknown` credit gap only |
| Universe strict | PASS | metadata universe `62`개, `SPY/QQQ` 포함 |
| Quote/spread | PASS | `FCX` direct quote `69.48/69.49`, spread `0.0144%`, freshness 약 `0.02`분 |
| Risk plan | PASS | `check-risk-policy.py --json` PASS |
| Final submit path | READY | same-day duplicate/open-order `0`, whole-share day-limit stock, validation floor size |

## 후보와 판단

| Symbol | 판단 | 이유 |
| --- | --- | --- |
| FCX | selected_validation_buy | materials/copper diversifier, 2026-06-13 5D review 강함, 3-provider positive confirmation, same-day duplicate/open-order 0 |
| AVGO | watch | same-day duplicate sell gate로 trim 차단 |
| RGTI | watch | same-day duplicate sell gate로 trim 차단 |
| SO | watch | trim decision-grade expected-excess/replacement margin 공백 지속 |
| NEE | watch | `2026-06-15T15:37:52Z` same-day filled buy 1주 때문에 duplicate buy gate |
| BAC | watch | `2026-06-15T14:19:50Z` same-day filled buy 1주 때문에 duplicate buy gate |
| WMT | watch | `2026-06-15T14:41:05Z` same-day filled buy 1주 때문에 duplicate buy gate |
| JPM | watch | `2026-06-15T16:00:28Z` same-day filled buy 1주 때문에 duplicate buy gate |
| XOM | watch | energy headline sensitivity와 relative ranking에서 FCX보다 후순위 |
| SLB | watch | same cluster energy-services holding이지만 당일 상대 약세로 FCX보다 후순위 |
| AMZN | watch | mixed weak-review history로 FCX보다 후순위 |
| NKE | watch | mixed review history와 consumer rebound 불확실성으로 FCX보다 후순위 |
| PLTR | watch | speculative_growth sleeve 변동성과 valuation noise로 FCX보다 후순위 |
| SPY | watch | 1주 ask `756.33 USD`가 validation floor per-order cap 약 `513.39 USD` 초과 |
| QQQ | watch | 1주 ask `744.33 USD`가 validation floor per-order cap 약 `513.39 USD` 초과 |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| AVGO | watch | `duplicate_symbol_side_same_day` | de-risking trigger는 남지만 same-day trim fill 때문에 추가 sell 차단 |
| RGTI | watch | `duplicate_symbol_side_same_day` | speculative loss-control trim trigger는 남지만 same-day filled trim 때문에 추가 sell 차단 |
| SO | watch | `sell_metric_gap` | spread는 pass지만 trim decision-grade metric gap 지속 |

## 주문/체결

### 제출 전 게이트 요약

paper mode `true`; market clock `2026-06-15T12:15:52.699072615-04:00`; order plan path `wiki/trade-ledger/orders/2026-06-16-0111-hourly-autopilot.json`; universe strict `PASS`; MCP strict `PASS`; risk validator `PASS`; FCX quote freshness 약 `0.02`분; spread `0.0144%`; order shape `buy 1 share / limit 69.49 / day / stock / regular`; duplicate/open-order check `PASS`; source refs는 `0111` stale cleanup/core/research preflight, runtime gate evaluation, `review-due-index`, `2026-06-15-portfolio-review`, `[[FCX]]`다.

| Symbol | Side | Qty | Limit | Status | Filled Avg | Order ID |
| --- | --- | ---: | ---: | --- | ---: | --- |
| FCX | buy | 1 | 69.49 | new | - | `25c585c7-5aba-4bdb-8d68-a12dde2a6258` |

- `place_stock_order` actual submit: `2026-06-15T16:21:07.887496306Z`
- `get_order_by_client_id` immediate reconciliation: `status=new`, `filled_qty=0`, `filled_avg_price` 없음
- `get_orders(status=open)` immediate reconciliation: `1`건 (`FCX` buy)
- `get_all_positions` immediate reconciliation: `FCX qty=5`, `avg_entry_price=64.912`, positions 총 `33`건
- `get_account_info` immediate reconciliation: cash `31,965.04 USD`, portfolio value `102,747.54 USD`

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | broad universe 62개, shortlist 10개 |
| `check-mcp-coverage.py --strict --json` | PASS | Alpaca core pass, positive research 3개, Alpha/Firecrawl non-core gap |
| `check-risk-policy.py --json` | PASS | FCX floor-size buy order plan 통과, post-order cash는 target max 위 경고만 유지 |

## 산출물

- Report: `wiki/current-runs/daily/2026-06-16-0111-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-16-0111-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-16-0111-hourly-autopilot.json`
- Runtime gate evaluation: `wiki/evidence-store/sources/2026-06-16-0111-hourly-autopilot-runtime-gate-evaluation.json`
- Submit trace: `wiki/evidence-store/sources/2026-06-16-0111-hourly-autopilot-deterministic-submit.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-16-0111-hourly-autopilot-post-trade.json`

## 지표 설명

- `pass_tiered`: core MCP와 최소 research confirmation이 확보돼 일부 non-core provider gap이 있어도 submit 가능하다는 뜻이다.
- `duplicate_symbol_side_same_day`: 같은 세션에 이미 체결된 동일 symbol/side order가 있어 추가 학습 주문을 막는 규칙이다.
- `sell_metric_gap`: trim 판단에 필요한 expected-excess 또는 replacement margin이 비어 있어 집행형 trim으로 승격하지 못한 상태다.
- `validation floor per-order cap`: `portfolio_value * 0.5%` 상한이다. 이번 cycle의 cap은 약 `513.39 USD`라 `SPY/QQQ` 1주가 초과했다.
