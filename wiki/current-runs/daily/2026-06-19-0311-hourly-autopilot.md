# 2026-06-19-0311-hourly-autopilot scheduled paper autopilot

## 요약

`0311` scheduled hourly-autopilot은 scheduler-owned stale cleanup/core/research preflight를 source-of-record로 사용했다. `Alpha Vantage`는 one-call-per-hour throttle 기반 `provider_error`, `Firecrawl`은 credits failure `unknown` gap으로 남았지만 `SEC EDGAR`, `FRED`, `Yahoo Finance`가 `3/3` usable/pass confirmation을 유지해 strict MCP submit gate는 열려 있다. stale cleanup은 `remaining open orders 0`, Alpaca core는 hard gate `pass`, regular market clock은 `2026-06-18T14:11:11.172857652-04:00` 기준 open이며 `RGTI qty=5`, `qty_available=5`로 residual speculative sleeve만 남아 있다.

buy side는 `review_backlog_pending_1d_count=17`로 YAML stop threshold `12`를 넘어 계속 닫혀 있으므로 sell-first directive에 따라 `RGTI` 1주 trim을 이번 cycle 최소 learning order로 제출했다. immediate reconciliation 기준 신규 주문 `client_order_id=hourly-20260619-0311-sell-rgti`는 `status=new`, `filled_qty=0` open order이며 `RGTI qty=5`, `qty_available=4`로 1주만 예약 상태다. 해석은 `strict gate pass + residual speculative sleeve staged de-risking submit 완료, next cycle fill/open-order lifecycle 추적 필요`다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env` 기준 `ALPACA_PAPER_TRADE=true` |
| Market clock | PASS | scheduler preflight `get_clock` `2026-06-18T14:11:11.172857652-04:00`, regular market open |
| Stale order lifecycle | PASS | `0311` stale cleanup artifact 기준 stale candidates `0`, remaining open orders `0` |
| Alpaca core MCP | PASS | scheduler core preflight hard gate `pass`, account `ACTIVE`, positions `33`, open orders `0`, watchlists `0` |
| Research MCP strict | PASS | usable/pass research provider `sec-edgar`, `fred`, `yahoo-finance` = `3/3` |
| Universe strict | PASS | broad metadata universe `62`개, SPY/QQQ 포함 |
| Review backlog throttle | FAIL for buys only | `pending_1d_count=17` > `stop_new_buys_at_pending_1d=12` |
| Quote freshness | PASS | scheduler quote timestamp `2026-06-18T18:11:27.112699852Z` |
| Spread | PASS | `RGTI 0.0485%`는 hard cap `0.50%` 이내 |
| Risk plan | PASS | `RGTI sell 1 @ 20.61 USD` trim plan validator PASS |
| Final submit path | PASS | sell-first `RGTI trim` candidate가 strict gates를 모두 통과했고 buy-only throttle과 분리된다 |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| RGTI | executable_sell_trim | 0.0485% | speculative loss-control trim trigger, negative expected excess, open-order blocker 없음 |
| SO | blocked_sell_metric_gap | 0.0215% | trim decision-grade expected-excess/replacement margin 공백 |
| AAPL | blocked_review_backlog_throttle | 0.0135% | 신규 add는 buy-only backlog throttle로 차단 |
| BAC | blocked_review_backlog_throttle | 0.0178% | 신규 add는 buy-only backlog throttle로 차단 |
| WMT | blocked_review_backlog_throttle | 0.0171% | 신규 add는 buy-only backlog throttle로 차단 |
| NVDA | blocked_review_backlog_and_same_theme_warning | 0.0095% | 신규 add는 buy-only backlog throttle와 same-theme warning context 중첩 |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| RGTI | trim | pass | residual speculative sleeve staged de-risking과 fresh preflight quote가 동시에 확인돼 이번 cycle sell-first learning order |
| SO | watch | `sell_metric_gap` | quote/spread는 pass지만 decision-grade trim metric 공백이 남음 |
| AAPL | hold | `sell_trigger_none` | active trim trigger 없음 |

## 주문/체결

- Planned orders: 1
- Submitted orders: 1
- Immediate reconciliation: `RGTI sell 1 @ limit 20.61 USD`는 same `client_order_id` readback 기준 `status=new`, `filled_qty=0`, `filled_avg_price=null` open order다.
- Post-trade reconciliation: `get_orders(status=open)` 기준 open orders `1`, `get_all_positions` 기준 positions `33`, `RGTI qty=5`, `qty_available=4`, `get_account_info` 기준 cash `28,507.21 USD`, portfolio value `101,479.98 USD`, buying power `303,365.22 USD`, `get_watchlists` 기준 watchlists `0`

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict` | PASS | `62` symbols, shortlist `10`, final candidates `6` |
| `check-mcp-coverage.py --strict` | PASS | positive research `sec-edgar`, `fred`, `yahoo-finance` |
| `check-risk-policy.py --json` | PASS | `RGTI sell 1 @ 20.61 USD` trim plan |

## 산출물

- Report: `wiki/current-runs/daily/2026-06-19-0311-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-19-0311-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-19-0311-hourly-autopilot.json`
- Runtime gate evaluation: `wiki/evidence-store/sources/2026-06-19-0311-hourly-autopilot-runtime-gate-evaluation.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-19-0311-hourly-autopilot-post-trade.json`

## 지표 설명

- `executable_sell_trim`: buy-only throttle과 무관하게 sell-first risk-reducing trim이 strict gate를 모두 통과한 상태다.
- `review_backlog_throttle`: `paper_validation_execution.validation_order_sizing.review_backlog_throttle`는 신규 buy만 줄이거나 중단한다. sell/trim/exit 진단은 별도로 계속 평가한다.
- `sell_candidate_diagnostics`: 실행하지 않은 trim 후보도 metric 값 또는 explicit gap reason을 남겨 다음 analyst review와 policy learning에 연결한다.
