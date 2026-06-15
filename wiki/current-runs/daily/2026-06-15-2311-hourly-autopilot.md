# 2026-06-15-2311-hourly-autopilot

## 요약

`2311` scheduled hourly-autopilot은 scheduler-owned stale cleanup/core/research preflight를 source-of-record로 사용했고, live Alpaca order-state readback으로 `2251`의 `AVGO` sell open order를 먼저 재확인했다. sell-first 재평가에서 `AVGO`는 fresh open sell `status=new` 때문에 same-symbol 추가 trim이 막혔고, `RGTI`는 `2026-06-15T13:41:43Z` same-session filled sell 9주가 duplicate discipline을 유지했다. 따라서 learning-trade-directive는 different-cluster fallback으로 이동했고, `BAC`가 financials diversifier 기존 보유주, research confirmation 4개 pass, fresh quote `56.27/56.28`, spread `0.0178%`, review backlog 비차단, same-day BAC duplicate 부재 조건을 충족해 1주 validation buy로 승격됐다.

`place_stock_order`는 `2026-06-15T14:19:38Z`에 `BAC` buy `1주`를 `client_order_id=hourly-20260615-2311-buy-bac`로 제출했다. immediate reconciliation 기준 same order는 `status=new`, `filled_qty=0`이고, open orders는 `BAC` buy 1건과 `AVGO` sell 1건으로 `2`건이다. `get_all_positions` 기준 `BAC qty=6`은 아직 유지돼 이번 cycle은 `submitted/open` 상태로 마감하며 다음 cycle이 fill 또는 stale lifecycle을 다시 확인해야 한다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env` 기준 `ALPACA_PAPER_TRADE=true` |
| Market clock | PASS | live Alpaca clock `2026-06-15T10:13:57.366828196-04:00`, regular market open |
| Stale order lifecycle | PASS | scheduler stale cleanup은 fresh `AVGO` sell 1건만 관측, stale candidate `0`건 |
| Alpaca core MCP | PASS | scheduler core preflight hard gate `pass`, required rows complete, quotes fresh |
| Research MCP | PASS tiered | `sec-edgar/fred/firecrawl/yahoo-finance` positive, `alpha-vantage` throttle `provider_error` gap only |
| Universe strict | PASS | broad metadata universe `62`개, `SPY/QQQ` 포함 |
| Review backlog throttle | PASS for buys | `pending_1d=1`, `pending_5d=16`, `pending_20d=1`; buy stop threshold `12` 미만 |
| Quote/spread | PASS for BAC | submit boundary quote age `2.52`분, spread `0.0178%` |
| Risk plan | PASS | `check-risk-policy.py --json` PASS |
| Final submit path | PASS | eligible sell이 explicit gate에 막힌 뒤 `BAC 1주 @ 56.28 USD` floor-size buy submitted |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| AVGO | blocked_open_order_gate | 0.2199% | 2251 cycle same-symbol sell 1주가 아직 `status=new` open order |
| RGTI | blocked_duplicate_sell | 0.0862% | `2231` same-session filled trim 9주가 duplicate discipline 유지 |
| BAC | submit_buy | 0.0178% | financials diversifier, fresh quote pass, different-cluster open-order policy 허용 |
| SO | watch_only | 0.0426% | quote/spread는 pass지만 반복 weak review와 trim metric gap 이력 때문에 fallback 우선순위 낮음 |
| SPY | blocked_floor_cap | 0.0053% | 1주 ask `753.23 USD`가 validation floor per-order cap 초과 |
| QQQ | blocked_floor_cap | 0.0081% | 1주 ask `740.46 USD`가 validation floor per-order cap 초과 |
| NOK | blocked_validation_lifecycle_add_block | 0.0689% | `review-due-index` add-block 유지 |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| AVGO | watch | `same_symbol_side_open_order_exists` | de-risking rationale는 유지되지만 fresh open sell 1주가 먼저 해소돼야 함 |
| RGTI | watch | `duplicate_symbol_side_same_day` | same-session filled trim 9주 때문에 추가 sell 차단 |
| BAC | hold_watch | `sell_trigger_none` | active sell trigger는 없고 이번 cycle에서는 buy fallback으로만 executable |

## 주문/체결

| Symbol | Side | Qty | Limit | Status | Filled Avg | Order ID |
| --- | --- | ---: | ---: | --- | ---: | --- |
| BAC | buy | 1 | 56.28 | new | n/a | `dda6e628-c48f-48b5-891e-2bc6169bba6c` |

- `place_stock_order` actual submit: `2026-06-15T14:19:38.883379405Z`
- `get_order_by_client_id` immediate reconciliation: `status=new`, `filled_qty=0`
- `get_orders(status=open)` immediate reconciliation: `BAC` buy `1건` + `AVGO` sell `1건` = 총 `2건`
- `get_all_positions` immediate reconciliation: `BAC qty=6`, `qty_available=6`, `AVGO qty=3`, `qty_available=2`
- same-session filled order readback: `RGTI` sell `9주` 외 새 fill row 없음

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | broad universe 62개, shortlist 7개 |
| `check-mcp-coverage.py --strict --json` | PASS | Alpaca core pass, positive research 4개, Alpha throttle gap only |
| `check-risk-policy.py --json` | PASS | BAC floor-size buy order plan 통과 |

## 산출물

- Report: `wiki/current-runs/daily/2026-06-15-2311-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-15-2311-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-15-2311-hourly-autopilot.json`
- Runtime gate evaluation: `wiki/evidence-store/sources/2026-06-15-2311-hourly-autopilot-runtime-gate-evaluation.json`
- Deterministic submit note: `wiki/evidence-store/sources/2026-06-15-2311-hourly-autopilot-deterministic-submit.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-15-2311-hourly-autopilot-post-trade.json`

## 지표 설명

- `same_symbol_side_open_order_exists`: stale은 아니어도 동일 symbol/side open order가 남아 있을 때 추가 동일 방향 주문을 막는 open-order policy다. 이번 cycle에서는 `AVGO` trim 추가를 막았다.
- `different-cluster fallback`: sell-first 경로가 explicit gate에 막힌 뒤, fresh open order와 상관없는 다른 correlated cluster의 floor-size validation buy를 허용하는 policy 경로다. 이번 cycle의 `BAC`가 여기에 해당한다.
- `validation floor per-order cap`: floor-size learning buy라도 policy의 per-order notional cap을 넘는 벤치마크 1주는 제출할 수 없다는 뜻이다. 이번 cycle에서 `SPY/QQQ`가 이 gate에 막혔다.
- `submitted/open`: 주문이 MCP submit은 통과했지만 immediate reconciliation 시점에는 아직 fill되지 않은 상태다. 다음 cycle은 fill 여부와 stale lifecycle을 함께 추적해야 한다.
