# 2026-06-15-2251-hourly-autopilot

## 요약

`2251` scheduled hourly-autopilot은 scheduler-owned stale cleanup/core/research preflight를 source-of-record로 재사용했고, direct Alpaca spot check로 `clock/account/positions/quotes/recent fills`를 한 번 더 맞췄다. `RGTI`는 `2026-06-15T13:41:43Z` same-session sell fill 9주가 이미 있어 duplicate sell discipline에 막혔고, `AVGO`는 direct quote `394.90/395.07`, spread `0.0430%`, held qty `3`, open orders `0`, ai_semiconductor target-band warning, post-earnings staged de-risking rationale를 모두 만족해 이번 cycle의 우선 risk-reducing trim으로 승격됐다.

`place_stock_order`는 `2026-06-15T14:02:23Z`에 `AVGO` sell `1주`를 `client_order_id=hourly-20260615-2251-sell-avgo`로 제출했고, immediate reconciliation 시점 상태는 `new` open order다. `get_all_positions` 기준 `AVGO qty=3`는 유지됐지만 `qty_available=2`로 1주가 예약됐고, `get_account_activities(activity_types=FILL, after=2026-06-15T14:02:00Z)`에는 아직 새 fill row가 없었다. 이번 run은 `submitted/open` 상태로 마감하며 다음 cycle에서 fill 또는 stale lifecycle을 다시 확인해야 한다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env` 기준 `ALPACA_PAPER_TRADE=true` |
| Market clock | PASS | direct Alpaca clock `2026-06-15T09:55:13.006882407-04:00`, regular market open |
| Stale order lifecycle | PASS | scheduler stale cleanup status `pass`; initial/remaining open orders 0건 |
| Alpaca core MCP | PASS | scheduler core preflight hard gate `pass`, required rows complete, quotes fresh |
| Research MCP | PASS tiered | `sec-edgar/fred/firecrawl/yahoo-finance` positive, `alpha-vantage` one-call throttle `provider_error` gap only |
| Universe strict | PASS | broad metadata universe 62개, `SPY/QQQ` 포함 |
| Review backlog throttle | PASS for sells / PASS for buys | `pending_1d=1`, `pending_5d=16`, `pending_20d=1`; buy stop threshold 12 미만 |
| Quote/spread | PASS for AVGO | submit boundary quote age 약 `0.0`분, spread `0.0430%` |
| Risk plan | PASS | `check-risk-policy.py --json` PASS |
| Final submit path | PASS | eligible sell-first trim `AVGO 1주 @ 394.90 USD` submitted |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| AVGO | submit_trim | 0.0430% | post-earnings staged de-risking, ai_semiconductor target-band warning, same-session duplicate 없음 |
| RGTI | blocked_duplicate_sell | 2.7875% | speculative trim trigger는 유지되지만 `2231` same-session sell fill 9주가 duplicate discipline 유지 |
| BAC | executable_if_no_sell | 0.0356% | financials diversifier fallback buy로는 유효하지만 eligible sell-first trim이 먼저 열림 |
| SO | watch_only | 0.0536% | quote/spread는 pass지만 반복 weak review와 trim metric gap이 남음 |
| SPY | blocked_floor_cap | 0.0027% | 1주 ask `753.84 USD`가 validation floor per-order cap 초과 |
| NOK | blocked_validation_lifecycle_add_block | n/a | `review-due-index` add-block 유지 |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| AVGO | submit_trim | pass | de-risking rationale 유지, spread 정상화, open-order/duplicate conflict 없음 |
| RGTI | watch | `duplicate_symbol_side_same_day` | same-session filled trim 9주 때문에 추가 sell 차단 |
| BAC | hold_watch | `sell_trigger_none` | buy fallback은 가능하지만 active sell/trim trigger 없음 |

## 주문/체결

| Symbol | Side | Qty | Limit | Status | Filled Avg | Order ID |
| --- | --- | ---: | ---: | --- | ---: | --- |
| AVGO | sell | 1 | 394.90 | new | n/a | `f41578c0-cb41-4620-ad3d-7a6e6a87946a` |

- `place_stock_order` actual submit: `2026-06-15T14:02:23.793160947Z`
- `get_order_by_client_id` immediate reconciliation: `status=new`, `filled_qty=0`
- `get_all_positions` immediate reconciliation: `AVGO qty=3`, `qty_available=2`, `current_price=390.54`
- `get_account_activities(activity_types=FILL, after=2026-06-15T14:02:00Z)` immediate reconciliation: 새 fill row 없음

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | broad universe 62개, shortlist 10개 |
| `check-mcp-coverage.py --strict --json` | PASS | Alpaca core pass, positive research 4개, Alpha throttle gap only |
| `check-risk-policy.py --json` | PASS | sell-first trim order plan 통과 |

## 산출물

- Report: `wiki/current-runs/daily/2026-06-15-2251-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-15-2251-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-15-2251-hourly-autopilot.json`
- Runtime gate evaluation: `wiki/evidence-store/sources/2026-06-15-2251-hourly-autopilot-runtime-gate-evaluation.json`
- Deterministic submit note: `wiki/evidence-store/sources/2026-06-15-2251-hourly-autopilot-deterministic-submit.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-15-2251-hourly-autopilot-post-trade.json`

## 지표 설명

- `same-session duplicate sell discipline`: 같은 미국 정규 세션 안에서 이미 fill된 동일 symbol/side sell을 반복 제출하지 않는 규율이다. 이번 cycle에서는 `RGTI`에 적용됐다.
- `target-band de-risking`: `ai_semiconductor` theme/factor/cluster 경고 band와 음수 expected excess가 함께 남을 때, hard gate가 열리면 보유 수량을 소폭 줄여 policy-learning 표본을 만든다.
- `qty_available`: Alpaca가 open order에 묶어 둔 즉시 매도 가능 수량이다. 이번 run의 `AVGO qty=3`, `qty_available=2`는 주문 1주가 아직 open임을 뜻한다.
- `provider gap`: 이번 run의 `alpha-vantage`는 one-call-per-hour throttle 때문에 `gap_category=provider_error`로만 기록됐고, 나머지 4개 research confirmations가 strict MCP gate를 통과시켰다.
