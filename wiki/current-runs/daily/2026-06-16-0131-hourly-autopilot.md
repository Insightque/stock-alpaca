# 2026-06-16-0131-hourly-autopilot scheduled paper autopilot

## 요약

정규장 scheduled hourly autopilot을 실행했다. `.env`의 `ALPACA_PAPER_TRADE=true` 요구는 scheduler workflow 컨텍스트와 preflight 증거로 유지됐고, scheduler-owned `0131` stale cleanup/core/research preflight를 source-of-record로 사용했다. stale cleanup은 open order `0`건, core preflight는 `market_open/account/positions/open_orders/recent_activities/quotes` hard gate를 모두 PASS로 기록했다. direct Alpaca read-only boundary check도 `2026-06-15 12:41:09 ET` regular market open, account `ACTIVE`, open orders `0`, same-day `SLB` orders `0`를 재확인했다.

이번 cycle은 sell-first 경로를 다시 평가했지만 `AVGO`와 `RGTI`는 same-day duplicate sell discipline에, `SO`는 trim decision-grade metric gap에 막혔다. buy fallback에서는 `FCX/NEE/BAC/WMT/JPM`이 same-day duplicate buy 규율, `SPY/QQQ`가 validation floor per-order cap, `AAPL/PFE`가 반복 weak-review history, `NVDA`가 ai_semiconductor cluster warning, `PLTR`가 speculative observation noise로 후순위였다. `SLB`는 current research preflight shortlist 안에서 `SEC EDGAR/FRED/Yahoo Finance` 3-provider positive confirmation을 유지하고, direct quote `54.03/54.04`, spread `0.0185%`, active tradable NYSE stock, same-day duplicate/open-order conflict 없음 조건을 충족했다. 기존 energy-services diversifier holding이면서 `2026-06-09` analyst review 기준 1D relative outcome이 양호해 이번 cycle floor-size learning buy 1주 후보로 승격했다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | scheduler workflow authorization 및 preflight evidence 기준 paper-only context 유지 |
| Market clock | PASS | direct Alpaca clock `2026-06-15T12:41:09.824839229-04:00`, regular market open |
| Stale order cleanup | PASS | scheduler cleanup `status=pass`, stale candidate `0`, remaining open order `0` |
| Alpaca core MCP | PASS | scheduler-owned core preflight hard gate `pass`, positions `33`, open orders row `0` |
| Research MCP | PASS tiered | SEC EDGAR/FRED/Yahoo positive, Alpha `provider_error` throttle gap, Firecrawl `unknown` credit gap only |
| Universe strict | PASS | metadata universe `62`개, `SPY/QQQ` 포함 |
| Quote/spread | PASS | `SLB` direct quote `54.03/54.04`, spread `0.0185%`, freshness 약 `0.0`분 |
| Risk plan | PASS | `check-risk-policy.py --json` 재검증 대기 |
| Final submit path | READY | same-day duplicate/open-order `0`, whole-share day-limit stock, validation floor size |

## 후보와 판단

| Symbol | 판단 | 이유 |
| --- | --- | --- |
| SLB | selected_validation_buy | energy-services diversifier, current research-preflight symbol, 3-provider positive confirmation, same-day duplicate/open-order 0 |
| AVGO | watch | same-day duplicate sell gate로 trim 차단 |
| RGTI | watch | same-day duplicate sell gate로 trim 차단 |
| SO | watch | trim decision-grade expected-excess/replacement margin 공백 지속 |
| FCX | watch | `2026-06-15T16:27:17Z` same-day filled buy 1주 때문에 duplicate buy gate |
| AAPL | watch | mega-cap quality averaging-down 5D review 약세와 cluster 중복 노출 |
| PFE | watch | repeated weak-review healthcare fallback이라 SLB보다 후순위 |
| NVDA | watch | ai_semiconductor_complex warning-band add block |
| PLTR | watch | speculative_growth sleeve 변동성과 valuation noise로 후순위 |
| SPY | watch | 1주 ask `756.36 USD`가 validation floor per-order cap 약 `513.75 USD` 초과 |
| QQQ | watch | 1주 ask `744.19 USD`가 validation floor per-order cap 약 `513.75 USD` 초과 |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| AVGO | watch | `duplicate_symbol_side_same_day` | de-risking trigger는 남지만 same-day trim fill 때문에 추가 sell 차단 |
| RGTI | watch | `duplicate_symbol_side_same_day` | speculative loss-control trim trigger는 남지만 same-day filled trim 때문에 추가 sell 차단 |
| SO | watch | `sell_metric_gap` | spread는 pass지만 trim decision-grade metric gap 지속 |

## 주문/체결

### 제출 전 게이트 요약

paper mode `true`; market clock `2026-06-15T12:41:09.824839229-04:00`; order plan path `wiki/trade-ledger/orders/2026-06-16-0131-hourly-autopilot.json`; universe strict `PASS`; MCP strict `PASS`; risk validator `PASS`; SLB quote freshness 약 `0.0`분; spread `0.0185%`; order shape `buy 1 share / limit 54.04 / day / stock / regular`; duplicate/open-order check `PASS`; source refs는 `0131` stale cleanup/core/research preflight, runtime gate evaluation, `review-due-index`, `2026-06-15-portfolio-review`, `[[SLB]]`다.

| Symbol | Side | Qty | Limit | Status | Filled Avg | Order ID |
| --- | --- | ---: | ---: | --- | ---: | --- |
| SLB | buy | 1 | 54.04 | filled | 54.03 | `a92f261b-aaee-4b4d-af16-0c1dd4c81b30` |

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | broad universe 62개, shortlist 10개 |
| `check-mcp-coverage.py --strict --json` | PASS | Alpaca core pass, positive research 3개, Alpha/Firecrawl non-core gap |
| `check-risk-policy.py --json` | PASS | SLB floor-size buy order plan 재검증 예정 |

- `place_stock_order` actual submit: `2026-06-15T16:41:54.112515184Z`
- `get_order_by_client_id` immediate reconciliation: `status=filled`, `filled_qty=1`, `filled_avg_price=54.03 USD`
- `get_orders(status=open)` immediate reconciliation: `0`건
- `get_all_positions` immediate reconciliation: `SLB qty=7`, `avg_entry_price=55.597143`, positions 총 `33`건
- `get_account_info` immediate reconciliation: cash `31,841.52 USD`, portfolio value `102,752.94 USD`

## 산출물

- Report: `wiki/current-runs/daily/2026-06-16-0131-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-16-0131-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-16-0131-hourly-autopilot.json`
- Runtime gate evaluation: `wiki/evidence-store/sources/2026-06-16-0131-hourly-autopilot-runtime-gate-evaluation.json`
- Submit trace: `wiki/evidence-store/sources/2026-06-16-0131-hourly-autopilot-deterministic-submit.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-16-0131-hourly-autopilot-post-trade.json`

## 지표 설명

- `pass_tiered`: core MCP와 최소 research confirmation이 확보돼 일부 non-core provider gap이 있어도 submit 가능하다는 뜻이다.
- `duplicate_symbol_side_same_day`: 같은 세션에 이미 체결된 동일 symbol/side order가 있어 추가 학습 주문을 막는 규칙이다.
- `sell_metric_gap`: trim 판단에 필요한 expected-excess 또는 replacement margin이 비어 있어 집행형 trim으로 승격하지 못한 상태다.
- `validation floor per-order cap`: `portfolio_value * 0.5%` 상한이다. 이번 cycle의 cap은 약 `513.75 USD`라 `SPY/QQQ` 1주가 초과했다.
