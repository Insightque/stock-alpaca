# 2026-06-15-2331-hourly-autopilot

## 요약

`2331` scheduled hourly-autopilot은 scheduler-owned stale cleanup/core/research preflight를 source-of-record로 사용했고, registered Alpaca MCP submit-boundary check로 regular market open, `AVGO` open sell 1건, `BAC` same-session filled buy 1건, fresh `WMT` quote를 재확인했다. sell-first 재평가에서는 `AVGO`가 same-symbol open-order gate에 막혔고, `RGTI`는 `2026-06-15T13:41:43Z` same-session filled sell 때문에 duplicate discipline이 유지됐으며, `SO`는 decision-grade trim metric gap이 남았다. 따라서 learning-trade-directive는 buy fallback으로 이동했고, `WMT`가 consumer-defensive existing holding, 4-provider positive research confirmation, fresh quote `120.17/120.20`, spread `0.0250%`, same-day duplicate 부재, different-cluster open-order policy 허용 조건을 모두 충족해 1주 validation buy로 승격됐다.

제출 전 strict gate는 모두 PASS 상태다. `SPY/QQQ`는 1주 ask가 validation floor per-order cap을 넘고, `BAC`는 `14:19:50Z` same-session filled buy 때문에 duplicate gate에 막히며, `NOK`는 `review-due-index` add-block이 유지된다. 따라서 이번 cycle의 floor-size learning order는 `WMT` 1주 buy다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | scheduler artifact와 workflow contract 기준 `ALPACA_PAPER_TRADE=true` |
| Market clock | PASS | direct Alpaca clock `2026-06-15T10:35:33.84384781-04:00`, regular market open |
| Stale order lifecycle | PASS | scheduler stale cleanup은 fresh `AVGO` sell 1건만 관측, stale candidate `0`건 |
| Alpaca core MCP | PASS | scheduler core preflight hard gate `pass` + direct clock/account/orders/positions/quote 재확인 |
| Research MCP | PASS tiered | `sec-edgar/fred/firecrawl/yahoo-finance` positive, `alpha-vantage` throttle `provider_error` gap only |
| Universe strict | PASS | broad metadata universe `62`개, `SPY/QQQ` 포함 |
| Review backlog throttle | PASS for buys | `pending_1d=1`, `pending_5d=16`, `pending_20d=1`; buy stop threshold `12` 미만 |
| Quote/spread | PASS for WMT | direct quote `120.17/120.20`, spread `0.0250%`, quote age 약 `0.01`분 |
| Risk plan | PASS | `check-risk-policy.py --json` PASS |
| Final submit path | PASS | direct Alpaca MCP `place_stock_order`로 `WMT 1주 @ 120.20 USD` submitted |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| AVGO | blocked_open_order_gate | 0.1586% | 2251 cycle same-symbol sell 1주가 아직 `status=new` open order |
| RGTI | blocked_duplicate_sell | 0.0433% | `2231` same-session filled trim 9주 때문에 duplicate sell discipline 유지 |
| WMT | selected_validation_buy | 0.0250% | consumer-defensive existing holding, 4-provider positive confirmation, duplicate/open-order conflict 없음 |
| BAC | blocked_same_day_duplicate_buy | 0.0356% | `2026-06-15T14:19:50Z` same-session filled buy 1주가 있어 추가 buy 차단 |
| SPY | blocked_floor_cap | 0.0040% | 1주 ask `753.40 USD`가 validation floor per-order cap 초과 |
| QQQ | blocked_floor_cap | 0.0081% | 1주 ask `740.54 USD`가 validation floor per-order cap 초과 |
| NOK | blocked_validation_lifecycle_add_block | 0.0699% | `blocked_add_symbols` 유지 |
| NEE | watch_lower_rank | 0.0349% | executable하지만 이번 cycle consumer-defensive fallback으로는 `WMT`보다 우선순위가 낮음 |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| AVGO | watch | `same_symbol_side_open_order_exists` | de-risking rationale는 유지되지만 existing open sell 1주가 먼저 해소돼야 함 |
| RGTI | watch | `duplicate_symbol_side_same_day` | same-session filled trim 9주 때문에 추가 sell 차단 |
| SO | watch | `sell_metric_gap` | spread는 pass지만 trim decision-grade expected-excess/replacement margin 공백 지속 |

## 주문/체결

### 제출 전 게이트 요약

paper mode `true`; market clock `2026-06-15T10:35:33.84384781-04:00`; order plan path `wiki/trade-ledger/orders/2026-06-15-2331-hourly-autopilot.json`; universe strict `PASS`; MCP strict `PASS`; risk validator `PASS`; WMT quote freshness 약 `0.01`분; spread `0.0250%`; order shape `buy 1 share / limit 120.20 / day / stock / regular session`; duplicate/open-order check `PASS`; source refs는 `2331` stale cleanup/core/research preflight, runtime gate snapshot, policy/review/ticker artifacts다.

| Symbol | Side | Qty | Limit | Status | Filled Avg | Order ID |
| --- | --- | ---: | ---: | --- | ---: | --- |
| WMT | buy | 1 | 120.20 | new | n/a | `ee4c1e0c-46cc-43cb-8ec8-59b25b2b99ba` |

- `place_stock_order` actual submit: `2026-06-15T14:40:08.28247584Z`
- `get_order_by_client_id` immediate reconciliation: `status=new`, `filled_qty=0`
- `get_orders(status=open)` immediate reconciliation: `WMT` buy `1건` + earlier `AVGO` sell `1건` = 총 `2건`
- `get_all_positions` immediate reconciliation: `WMT qty=8`, `qty_available=8`, `AVGO qty=3`, `qty_available=2`
- same-session filled order readback: `BAC` buy `1주` 외 새 fill row 없음

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | broad universe 62개, shortlist 8개 |
| `check-mcp-coverage.py --strict --json` | PASS | Alpaca core pass, positive research 4개, Alpha throttle gap only |
| `check-risk-policy.py --json` | PASS | WMT floor-size buy order plan 통과 |

## 산출물

- Report: `wiki/current-runs/daily/2026-06-15-2331-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-15-2331-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-15-2331-hourly-autopilot.json`
- Runtime gate evaluation: `wiki/evidence-store/sources/2026-06-15-2331-hourly-autopilot-runtime-gate-evaluation.json`
- Submit trace: `wiki/evidence-store/sources/2026-06-15-2331-hourly-autopilot-deterministic-submit.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-15-2331-hourly-autopilot-post-trade.json`

## 지표 설명

- `same_symbol_side_open_order_exists`: stale은 아니어도 동일 symbol/side open order가 남아 있을 때 추가 동일 방향 주문을 막는 open-order policy다. 이번 cycle에서는 `AVGO` trim 추가를 막았다.
- `duplicate_symbol_side_same_day`: 같은 세션에 이미 체결된 동일 symbol/side order가 있으면 추가 학습 주문을 막는 규칙이다. 이번 cycle에서는 `RGTI` sell과 `BAC` buy 재진입을 막는다.
- `validation floor per-order cap`: floor-size learning buy라도 계좌 가치의 `0.5%`를 넘는 1주 notional은 제출할 수 없다는 뜻이다. 이번 cycle에서 `SPY/QQQ`가 여기에 막혔다.
