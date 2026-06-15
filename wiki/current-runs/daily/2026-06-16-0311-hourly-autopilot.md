# 2026-06-16-0311-hourly-autopilot scheduled paper autopilot

## 요약

정규장 scheduled hourly autopilot을 실행했다. `.env`의 `ALPACA_PAPER_TRADE=true` 요구는 유지됐고, scheduler-owned `0311` stale cleanup/core/research preflight를 source-of-record로 사용했다. stale cleanup은 open order `0`건, core preflight는 `market_open/account/positions/open_orders/recent_activities/quotes` hard gate를 모두 PASS로 기록했다. direct Alpaca submit-boundary check도 `2026-06-15 14:13:32 ET` regular market open, account `ACTIVE`, open orders `0`, same-day `SO` buy duplicate `0`를 재확인했다.

이번 cycle은 sell-first 경로를 다시 평가했지만 `AVGO`와 `RGTI`는 same-day duplicate sell discipline에, `SO`는 trim decision-grade metric gap에 막혀 executable risk-reducing sell로는 승격되지 못했다. buy fallback에서는 `FCX/XOM/SLB/JPM/NEE/BAC/WMT/NKE/COP/V`가 same-day duplicate buy 규율, `SPY/QQQ`가 validation floor per-order cap 약 `514.02 USD`, `NVDA`가 ai_semiconductor cluster warning, `AAPL/GOOGL`이 반복 약세 review와 mega-cap overlap으로 후순위였다. `[[SO]]`는 current research preflight shortlist 안에서 `SEC EDGAR/FRED/Yahoo Finance` 3-provider positive confirmation을 유지하고, `2026-06-13` portfolio review 기준 `2026-06-10 ET` fill 1D가 `중립 양호`였으며, direct quote `94.34/94.37`, spread `0.0318%`, active tradable NYSE stock, existing utilities diversifier, same-day duplicate/open-order conflict 없음 조건을 충족해 이번 cycle floor-size learning buy 1주 후보로 승격했다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env` paper-only context 유지 |
| Market clock | PASS | direct Alpaca clock `2026-06-15T14:13:32.039115934-04:00`, regular market open |
| Stale order cleanup | PASS | scheduler cleanup `status=pass`, remaining open order `0` |
| Alpaca core MCP | PASS | scheduler-owned core preflight hard gate `pass`, direct continuity도 account/open order/positions 정상 |
| Research MCP | PASS tiered | SEC EDGAR/FRED/Yahoo positive, Alpha `provider_error` throttle gap, Firecrawl `unknown` credit gap only |
| Universe strict | PASS | metadata universe `62`개, `SPY/QQQ` 포함 |
| Quote/spread | PASS | `SO` direct quote `94.34/94.37`, spread `0.0318%`, freshness 약 `0.0`분 |
| Risk plan | PASS | `check-risk-policy.py --json` PASS |
| Final submit path | READY | same-day duplicate/open-order `0`, whole-share day-limit stock, validation floor size |

## 후보와 판단

| Symbol | 판단 | 이유 |
| --- | --- | --- |
| SO | selected_validation_buy | utilities diversifier fallback, current research-preflight symbol, SEC/FRED/Yahoo 3-provider positive confirmation, same-day duplicate/open-order 0 |
| CVX | watch | energy diversifier지만 existing energy cluster 대비 portfolio contribution/replacement rank가 `SO`보다 낮음 |
| AAPL | watch | repeated weak-review history와 mega-cap quality averaging-down 관찰 가설 유지 |
| GOOGL | watch | mixed weak-review history와 mega-cap overlap으로 `SO`보다 후순위 |
| SPY | watch | 1주 ask `755.12 USD`가 validation floor per-order cap 약 `514.02 USD` 초과 |
| QQQ | watch | 1주 ask `743.58 USD`가 validation floor per-order cap 약 `514.02 USD` 초과 |
| NVDA | watch | ai_semiconductor_complex warning-band add block |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| AVGO | watch | `duplicate_symbol_side_same_day` | ai_semiconductor warning band와 음수 expected excess는 남지만 same-day trim fill 이후 추가 sell 차단 |
| RGTI | watch | `duplicate_symbol_side_same_day` | speculative loss-control trim trigger는 남지만 same-day filled trim 때문에 추가 sell 차단 |
| SO | watch | `sell_metric_gap` | spread는 pass지만 trim decision-grade expected-excess/replacement margin 공백 지속 |

## 주문/체결

### 제출 전 게이트 요약

paper mode `true`; market clock `2026-06-15T14:13:32.039115934-04:00`; order plan path `wiki/trade-ledger/orders/2026-06-16-0311-hourly-autopilot.json`; universe strict `PASS`; MCP strict `PASS`; risk validator `PASS`; SO quote freshness 약 `0.0`분; spread `0.0318%`; order shape `buy 1 share / limit 94.37 / day / stock / regular`; duplicate/open-order check `PASS`; source refs는 `0311` stale cleanup/core/research preflight, runtime gate evaluation, `review-due-index`, `2026-06-15-portfolio-review`, `[[SO]]`다.

| Symbol | Side | Qty | Limit | Status | Filled Avg | Order ID |
| --- | --- | ---: | ---: | --- | ---: | --- |
| SO | buy | 1 | 94.37 | new | - | `39a326aa-6544-4ef1-9a05-319e3460bbab` |

## Reconciliation

immediate reconciliation 기준 `get_order_by_client_id`와 `get_orders(status=open)` 모두 `SO` 주문을 `status=new`, `filled_qty=0` open order로 반환했다. direct `get_account_info/get_all_positions` 기준 account `ACTIVE`, cash `31,216.95 USD`, portfolio value `102,826.47 USD`, positions `33`건이며 `SO qty=5`, `qty_available=5`, `avg_entry_price=92.696 USD`로 아직 신규 fill은 반영되지 않았다. 따라서 이번 cycle은 submit 성공, fill 미확정 open-order lifecycle 추적 상태로 종료한다.

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | broad universe 62개, shortlist 9개 |
| `check-mcp-coverage.py --strict --json` | PASS | Alpaca core pass, positive research 3개, Alpha/Firecrawl non-core gap |
| `check-risk-policy.py --json` | PASS | staged deployment warning only, hard gate 위반 없음 |

## 산출물

- Report: `wiki/current-runs/daily/2026-06-16-0311-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-16-0311-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-16-0311-hourly-autopilot.json`
- Runtime gate evaluation: `wiki/evidence-store/sources/2026-06-16-0311-hourly-autopilot-runtime-gate-evaluation.json`
- Submit trace: `wiki/evidence-store/sources/2026-06-16-0311-hourly-autopilot-deterministic-submit.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-16-0311-hourly-autopilot-post-trade.json`

## 지표 설명

- `pass_tiered`: core MCP와 최소 research confirmation이 확보돼 일부 non-core provider gap이 있어도 submit 가능하다는 뜻이다.
- `duplicate_symbol_side_same_day`: 같은 세션에 이미 체결된 동일 symbol/side order가 있어 추가 학습 주문을 막는 규칙이다.
- `sell_metric_gap`: trim 판단에 필요한 expected-excess 또는 replacement margin이 비어 있어 집행형 trim으로 승격하지 못한 상태다.
- `validation floor per-order cap`: `portfolio_value * 0.5%` 상한이다. 이번 cycle의 cap은 약 `514.02 USD`라 `SPY/QQQ` 1주가 초과했다.

- `place_stock_order` actual submit: `2026-06-15T18:18:29.236351179Z`
- `get_order_by_client_id` immediate reconciliation: `status=new`, `filled_qty=0`, `filled_avg_price` 없음
- `get_orders(status=open)` immediate reconciliation: `1`건 (`SO`)
- `get_all_positions` immediate reconciliation: `SO qty=5`, `avg_entry_price=92.696`, positions 총 `33`건
- `get_account_info` immediate reconciliation: cash `31,216.95 USD`, portfolio value `102,826.47 USD`
