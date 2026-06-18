# 2026-06-18-2251-hourly-autopilot scheduled paper autopilot

## 요약

`2251` scheduled hourly-autopilot은 scheduler-owned stale cleanup/core/research preflight를 source-of-record로 사용했고, stale lifecycle PASS, Alpaca core PASS, universe strict PASS, risk validator PASS, research strict PASS를 모두 충족했다. `Yahoo Finance`가 이번 cycle에서는 pass로 회복돼 research usable/pass confirmation이 `SEC EDGAR`, `FRED`, `Yahoo Finance` 3개가 되었고 strict submit gate가 다시 열렸다.

buy side는 `review_backlog_pending_1d_count=17`이 YAML stop threshold `12`를 넘어 신규 validation buy가 막혔다. sell-first 재평가에서는 `PFE` 잔여 1주가 repeated weak-review precedent, fresh quote `25.24/25.25`, spread `0.0396%`, same US-date duplicate sell `0`, open orders `0` 조건을 모두 충족해 이번 cycle의 최소 learning order로 승격됐다. `place_stock_order` 제출 뒤 same `client_order_id=hourly-20260618-2251-sell-pfe` reconciliation 기준 주문은 `2026-06-18T14:01:07.126808291Z`에 `filled_avg_price=25.28 USD`로 즉시 체결됐고, live `get_all_positions`에서는 `PFE`가 빠져 positions count가 `34 -> 33`으로 줄었다. 반면 `SO`는 decision-grade trim metric gap이 남았고 `RGTI`는 live spread `20.6930%`로 hard cap을 크게 넘었다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env` 기준 `ALPACA_PAPER_TRADE=true` |
| Market clock | PASS | scheduler core preflight `2026-06-18T09:51:10.675848048-04:00`, regular market open |
| Stale order lifecycle | PASS | `2251` stale cleanup artifact 기준 stale candidates `0`, remaining open orders `0` |
| Alpaca core MCP | PASS | scheduler core preflight hard gate `pass`, account `ACTIVE`, positions `34`, open orders `0` |
| Research MCP strict | PASS | usable/pass research provider `sec-edgar`, `fred`, `yahoo-finance` = `3/3` |
| Universe strict | PASS | broad metadata universe `62`개, SPY/QQQ 포함 |
| Review backlog throttle | FAIL for buys only | `pending_1d_count=17` > `stop_new_buys_at_pending_1d=12` |
| Quote freshness | PASS | source-of-record quote timestamps `2026-06-18T13:51:27Z~13:51:29Z` |
| Spread | MIXED | `PFE 0.0396%`, `SO 0.0647%` PASS, `RGTI 20.6930%` FAIL |
| Risk plan | PASS | validator 기준 `PFE sell 1 @ 25.24 USD` plan 허용 |
| Final submit path | PASS | sell-first `PFE exit` candidate가 strict gates를 모두 통과했고 immediate fill까지 확인 |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| PFE | executable_sell_exit | 0.0396% | repeated weak-review defensive holding, residual 1-share exit, same US-date duplicate sell 없음 |
| SO | blocked_sell_metric_gap | 0.0647% | trim rationale는 있으나 decision-grade expected-excess/replacement margin 공백 |
| RGTI | blocked_live_spread | 20.6930% | residual speculative trim rationale는 있으나 live spread hard cap fail |
| AAPL | blocked_review_backlog_throttle | 0.0202% | buy-only backlog throttle로 신규 add 차단 |
| BAC | blocked_review_backlog_throttle | 0.0349% | buy-only backlog throttle로 신규 add 차단 |
| WMT | blocked_review_backlog_throttle | 0.0680% | buy-only backlog throttle로 신규 add 차단 |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| PFE | exit | pass | residual 1-share defensive weak-review holding으로 이번 cycle sell-first learning order |
| SO | watch | `sell_metric_gap` | fresh quote/spread는 pass지만 trim metric 공백이 남음 |
| RGTI | watch | `spread_within_policy` | expected-excess는 음수지만 live spread가 hard cap을 크게 초과 |

## 주문/체결

- Planned orders: 1
- Submitted orders: 1
- Filled orders: `PFE sell 1 @ limit 25.24 USD`, `filled_avg_price=25.28 USD`, `filled_at=2026-06-18T14:01:07.126808291Z`
- Post-trade reconciliation: `get_order_by_client_id` 기준 `status=filled`, `get_orders(status=open)` 기준 open orders `0`, `get_all_positions` 기준 positions `33`, `PFE position 없음`, `get_account_info` 기준 cash `28,075.43 USD`, portfolio value `101,342.08 USD`, buying power `302,231.46 USD`, watchlists `0`

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | `62` symbols, shortlist `10`, final candidates `6` |
| `check-mcp-coverage.py --strict --json` | PASS | positive research `sec-edgar`, `fred`, `yahoo-finance` |
| `check-risk-policy.py --json` | PASS | `PFE sell 1 @ 25.24 USD` exit plan 통과 |

## 산출물

- Report: `wiki/current-runs/daily/2026-06-18-2251-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-18-2251-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-18-2251-hourly-autopilot.json`
- Runtime gate evaluation: `wiki/evidence-store/sources/2026-06-18-2251-hourly-autopilot-runtime-gate-evaluation.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-18-2251-hourly-autopilot-post-trade.json`

## 지표 설명

- `executable_sell_exit`: buy-only throttle과 무관하게 sell-first risk-reducing order가 strict gate를 모두 통과한 상태다.
- `review_backlog_throttle`: `paper_validation_execution.validation_order_sizing.review_backlog_throttle`는 신규 buy만 줄이거나 중단한다. sell/trim/exit 진단은 별도로 계속 평가한다.
- `sell_candidate_diagnostics`: 실행하지 않은 trim 후보도 metric 값 또는 explicit gap reason을 남겨 다음 analyst review와 policy learning에 연결한다.
