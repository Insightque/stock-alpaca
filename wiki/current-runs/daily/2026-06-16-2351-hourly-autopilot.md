# 2026-06-16-2351-hourly-autopilot scheduled paper autopilot

## 요약

`2351` scheduled hourly-autopilot은 scheduler-owned stale cleanup/core/research preflight를 source-of-record로 사용했다. preflight clock `2026-06-16T10:51:09.678756276-04:00`, account `ACTIVE`, positions `33`, fresh IEX quote rows는 모두 20분 이내라 Alpaca core hard gate를 PASS 처리했다. Research tiered gate도 `SEC EDGAR/FRED/Yahoo Finance` pass로 strict submit threshold `3` confirmations를 충족했고, `Alpha Vantage`는 `empty_response`, `Firecrawl`은 credits 부족 `unknown` gap only로 유지했다.

이번 cycle의 차이는 live submit-boundary quote refresh다. 직전 `2331`에서는 `SO` quote가 `88.70/99.36`으로 비정상 spread `11.3368%`를 보여 trim path가 닫혔지만, `2026-06-16T14:53:38.471988345Z` live Alpaca quote는 `94.77/94.79`로 spread `0.0211%`에 정상화됐다. same-day duplicate 규칙으로 `RGTI`와 `PFE` sell은 재제출 불가이고 buy fallback은 `review_backlog_pending_1d_count=18`, `SPY/QQQ` floor cap, `NOK` add-block 때문에 닫혀 있어, sell-first learning directive 기준 `SO` 1주 trim이 이번 cycle의 최소 검증 주문으로 승격됐다. `place_stock_order` 결과 주문은 `client_order_id=hourly-20260616-2351-sell-so`, `order_id=19434dfc-6383-440e-a649-4479dbc15669`로 접수됐고 same client id reconciliation 기준 `2026-06-16T14:58:02.526808Z` `filled_avg_price=94.77 USD`로 즉시 체결됐다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env` 기준 `ALPACA_PAPER_TRADE=true` |
| Market clock | PASS | live `get_clock` `2026-06-16T10:53:36.842841877-04:00`, regular market open |
| Stale order lifecycle | PASS | `2351` stale cleanup artifact 기준 stale candidates/open orders 모두 0 |
| Alpaca core MCP | PASS | scheduler core preflight hard gate `pass` + live boundary recheck |
| Research MCP | PASS tiered | SEC EDGAR/FRED/Yahoo positive 3개, Alpha empty-response gap, Firecrawl credit gap |
| Universe strict | PASS | broad metadata universe `62`개, SPY/QQQ 포함 |
| Review backlog throttle | BUY BLOCK ONLY | `pending_1d_count=18`가 stop threshold `12` 초과, sell/trim에는 비적용 |
| Quote/spread | PASS/MIXED | `SO` live spread `0.0211%` pass, `RGTI/PFE` quote pass but duplicate block, `SPY/QQQ` buy-side cap block |
| Risk plan | PASS | `check-risk-policy.py --json` 기준 current positions 포함 SO trim 1주 plan 적합 |
| Final submit path | PASS | `SO` 1주 trim이 hard gate와 learning directive를 충족했고 즉시 fill로 종료 |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| SO | submitted_sell_filled | 0.0211% | repeated weak-review trim rationale, same-day duplicate 없음, live quote 정상화 후 1주 trim 즉시 체결 |
| RGTI | blocked_same_day_duplicate_sell | 0.0479% 수준 | same-day earlier sell order `hourly-20260616-2251-sell-rgti`가 이미 존재/canceled |
| PFE | blocked_same_day_duplicate_sell | 0.0769% 수준 | `2026-06-16T14:18:55.368488Z` same-day sell fill 1건 존재 |
| SPY | blocked_floor_cap_and_review_backlog | 0.0040% 수준 | benchmark fallback이지만 1주 ask가 validation floor cap 초과, buy backlog stop 유지 |
| QQQ | blocked_floor_cap_and_review_backlog | 0.0596% 수준 | benchmark fallback이지만 1주 ask가 validation floor cap 초과, buy backlog stop 유지 |
| NOK | blocked_validation_lifecycle_add_block | 0.0711% 수준 | due review add-block과 review backlog stop 동시 유지 |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| SO | filled | pass | live quote `94.77/94.79`, spread `0.0211%`, open orders 0, same-day SO sell 0 후 `94.77 USD` 체결 |
| RGTI | watch | `duplicate_symbol_side_same_day` | spread/held qty는 정상이나 same-day earlier sell history가 재제출을 막음 |
| PFE | watch | `duplicate_symbol_side_same_day` | same-day trim fill 1건 뒤라 추가 same-side trim 비허용 |

## 주문/체결

- Planned orders: 1 (`SO` sell 1주 at `94.77 USD`)
- Submitted orders: 1
- Filled orders: `SO` sell 1주 `filled_avg_price=94.77 USD` at `2026-06-16T14:58:02.526808Z`
- `place_stock_order` 호출: 1회, alternate client id/retry 없음
- Post-trade reconciliation: live Alpaca 기준 open orders `0`, same-session fills `2(PFE, SO)`, `SO qty 6 -> 5`, cash `30,344.81 USD`, portfolio value `101,432.05 USD`

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | 62 symbols, SPY/QQQ 포함, final candidates 6개 |
| `check-mcp-coverage.py --strict --json` | PASS | Alpaca core pass, positive research 3개, Alpha/Firecrawl non-core gaps |
| `check-risk-policy.py --json` | PASS | current positions 포함 SO trim 1주 submit plan 적합 |

## 산출물

- Report: `wiki/current-runs/daily/2026-06-16-2351-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-16-2351-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-16-2351-hourly-autopilot.json`
- Runtime gate evaluation: `wiki/evidence-store/sources/2026-06-16-2351-hourly-autopilot-runtime-gate-evaluation.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-16-2351-hourly-autopilot-post-trade.json`

## 지표 설명

- `duplicate symbol/side discipline`: 같은 미국 거래일에 이미 제출된 동일 symbol/side 주문을 반복 제출하지 않는 submit safety 규칙이다.
- `validation floor per-order cap`: floor-size learning buy도 `portfolio_value * 0.5%` 상한을 넘을 수 없다. 이번 cycle cap은 약 `507.70 USD`라 `SPY/QQQ` 1주가 초과한다.
- `review_backlog_pending_1d_count`: validation buy 1D review backlog count다. 이번 cycle에서는 `18`이라 YAML stop threshold `12`를 넘어 신규 buy가 차단됐다.
- `sell_candidate_diagnostics`: 실행하지 않은 trim 후보도 why-not evidence를 남겨 후속 analyst review와 policy learning에 사용한다.
