# 2026-06-16-0011-hourly-autopilot scheduled paper autopilot

## 요약

정규장 scheduled hourly autopilot을 실행했다. `.env`에서 `ALPACA_PAPER_TRADE=true`를 확인했고, scheduler-owned `0011` stale cleanup/core/research preflight를 source-of-record로 사용했다. stale cleanup은 open order `0`건, core preflight는 `market_open/account/positions/open_orders/recent_activities/quotes` hard gate를 모두 PASS로 기록했다. account snapshot은 portfolio value `102,407.68 USD`, cash `31,980.21 USD`, positions `33`건이었다.

이번 cycle은 sell-first 경로가 실제 집행으로 이어졌다. `RGTI`는 `2026-06-15T13:41:43Z` same-session filled sell 9주 때문에 duplicate sell gate에 막혔고, `SO`는 trim metric gap이 남았다. 반면 `AVGO`는 ai_semiconductor target-band de-risking rationale, negative expected excess, fresh quote `391.74/392.19`, spread `0.1148%`, open orders `0`, stale cleanup pass를 모두 충족해 1주 validation trim으로 승격됐다. direct Alpaca MCP `place_stock_order`는 `2026-06-15T15:18:03Z`에 `client_order_id=hourly-20260616-0011-sell-avgo`를 제출했고, immediate reconciliation 기준 `2026-06-15T15:18:03.982786708Z` `filled_avg_price=392.14 USD`로 즉시 체결됐다. post-trade readback 기준 open orders `0`, cash `32,372.35 USD`, `AVGO qty=3 -> 2`다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env`의 `ALPACA_PAPER_TRADE=true` 확인 |
| Market clock | PASS | scheduler core preflight `2026-06-15T11:11:11.109331665-04:00`, regular market open |
| Stale order cleanup | PASS | scheduler cleanup `status=pass`, stale candidate `0`, remaining open order `0` |
| Alpaca core MCP | PASS | scheduler-owned core preflight hard gate `pass`, positions `33`, open orders row `0` |
| Research MCP | PASS tiered | SEC EDGAR/FRED/Firecrawl/Yahoo positive, Alpha Vantage `provider_error` gap only |
| Universe strict | PASS | metadata universe `62`개, `SPY/QQQ` 포함 |
| Quote/spread | PASS | `AVGO` quote `391.74/392.19`, spread `0.1148%`, freshness `0.0`분 |
| Risk plan | PASS | `check-risk-policy.py --json` PASS |
| Final submit path | PASS | `place_stock_order` executed and immediate fill confirmed |

## 후보와 판단

| Symbol | 판단 | 이유 |
| --- | --- | --- |
| AVGO | selected_validation_trim | ai_semiconductor de-risking rationale, negative expected excess, open orders `0`, spread pass |
| RGTI | watch | `2026-06-15T13:41:43Z` same-session filled sell 9주로 duplicate sell gate |
| SO | watch | trim decision-grade expected-excess/replacement margin 공백 지속 |
| WMT | watch | sell-first eligible trim이 열려 buy fallback까지 갈 필요가 없었음 |
| BAC | watch | same-session filled buy 이력과 lower-rank fallback 상태 |
| SPY | watch | fallback benchmark지만 executable sell-first trim이 먼저 열림 |
| QQQ | watch | fallback benchmark지만 executable sell-first trim이 먼저 열림 |
| NOK | watch | `validation_lifecycle` add-block 유지 |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| AVGO | trim | pass | target-band de-risking rationale와 negative expected excess가 유지되고 quote/spread/open-order/risk gate가 모두 열림 |
| RGTI | watch | `duplicate_symbol_side_same_day` | same-session filled trim 9주가 있어 추가 sell 차단 |
| SO | watch | `sell_metric_gap` | trim 판단용 decision-grade metric 공백 지속 |

## 주문/체결

### 제출 전 게이트 요약

paper mode `true`; market clock `2026-06-15T11:11:11.109331665-04:00`; order plan path `wiki/trade-ledger/orders/2026-06-16-0011-hourly-autopilot.json`; universe strict `PASS`; MCP strict `PASS`; risk validator `PASS`; AVGO quote freshness `0.0`분; spread `0.1148%`; order shape `sell 1 share / limit 391.74 / day / stock / regular`; duplicate/open-order check `PASS`; source refs는 `0011` stale cleanup/core/research preflight, policy/review/ticker artifacts다.

| Symbol | Side | Qty | Limit | Status | Filled Avg | Order ID |
| --- | --- | ---: | ---: | --- | ---: | --- |
| AVGO | sell | 1 | 391.74 | filled | 392.14 | `a57c7e1a-5f57-4acc-a32b-15788f2fc335` |

- `place_stock_order` actual submit: `2026-06-15T15:18:03.437536674Z`
- `get_order_by_client_id` immediate reconciliation: `status=filled`, `filled_qty=1`, `filled_avg_price=392.14 USD`
- `get_orders(status=open)` immediate reconciliation: `0`건
- `get_all_positions` immediate reconciliation: `AVGO qty=2`, `qty_available=2`, positions 총 `33`건
- `get_account_info` immediate reconciliation: cash `32,372.35 USD`, portfolio value `102,324.39 USD`

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | broad universe 62개, shortlist 10개 |
| `check-mcp-coverage.py --strict --json` | PASS | Alpaca core pass, positive research 4개, Alpha provider-error gap only |
| `check-risk-policy.py --json` | PASS | AVGO floor-size trim order plan 통과 |

## 산출물

- Report: `wiki/current-runs/daily/2026-06-16-0011-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-16-0011-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-16-0011-hourly-autopilot.json`
- Runtime gate evaluation: `wiki/evidence-store/sources/2026-06-16-0011-hourly-autopilot-runtime-gate-evaluation.json`
- Submit trace: `wiki/evidence-store/sources/2026-06-16-0011-hourly-autopilot-deterministic-submit.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-16-0011-hourly-autopilot-post-trade.json`

## 지표 설명

- `pass_tiered`: core MCP와 최소 research confirmation이 확보돼 일부 non-core provider gap이 있어도 submit 가능하다는 뜻이다.
- `duplicate_symbol_side_same_day`: 같은 세션에 이미 체결된 동일 symbol/side order가 있어 추가 학습 주문을 막는 규칙이다.
- `sell_metric_gap`: trim 판단에 필요한 expected-excess 또는 replacement margin이 비어 있어 집행형 trim으로 승격하지 못한 상태다.
- `target-band de-risking`: theme/factor/cluster warning band와 성과 저하가 겹칠 때 staged trim을 허용하는 정책 경로다.
