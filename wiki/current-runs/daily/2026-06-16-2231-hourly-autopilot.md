# 2026-06-16-2231-hourly-autopilot scheduled paper autopilot

## 요약

정규장 scheduled hourly autopilot을 실행했다. `.env`의 `ALPACA_PAPER_TRADE=true` 요구는 유지됐고, scheduler-owned `2231` stale cleanup/core/research preflight를 source-of-record로 사용했다. stale cleanup은 open order `0`건, core preflight는 `market_open/account/positions/open_orders/recent_activities/quotes` hard gate를 모두 PASS로 기록했다. direct Alpaca submit-boundary check도 `2026-06-16 09:42 ET` regular market open, account `ACTIVE`, current-session open orders `0`, fills `0`를 재확인했다.

이번 cycle은 sell-first 경로가 실제 체결로 이어졌다. `[[AVGO]]`는 ai_semiconductor target-band de-risking rationale, post-earnings staged de-risking, 음수 expected excess, fresh quote `387.00/388.50`, spread `0.3868%`, current-session duplicate/open-order `0`를 모두 충족해 1주 trim 후보로 승격됐다. `[[RGTI]]`는 speculative loss-control trim trigger가 남아 있었지만 direct quote `22.34/22.50` spread `0.7137%`로 hard cap `0.50%`를 넘겨 탈락했고, `[[PFE]]`는 quote `25.91/25.92`로 trim 가능했지만 현재 위험 축소 우선순위는 `AVGO`보다 낮았다. direct Alpaca MCP `place_stock_order`는 `2026-06-16T13:43:56Z`에 `client_order_id=hourly-20260616-2231-sell-avgo`를 제출했고, immediate reconciliation 기준 `2026-06-16T13:43:57.208757279Z` `filled_avg_price=387.76 USD`로 즉시 체결됐다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env`의 `ALPACA_PAPER_TRADE=true` 확인 |
| Market clock pre-submit | PASS | direct `get_clock` timestamp `2026-06-16T09:42:13.129128423-04:00`, market open |
| Stale order lifecycle | PASS | scheduler cleanup `status=pass`, remaining open orders `0` |
| Alpaca core MCP | PASS | scheduler-owned core preflight hard gate pass + direct boundary recheck |
| Research MCP | PASS tiered | SEC EDGAR/FRED/Yahoo positive; Alpha `empty_response`, Firecrawl credit 부족 `unknown` non-core gap |
| Universe strict | PASS | metadata universe 62개, SPY/QQQ 포함 |
| Quote/spread | PASS for planned order | direct `AVGO` quote `387.00/388.50`, spread `0.3868%`, freshness 약 `0.0`분 |
| Risk plan | PASS | `check-risk-policy.py --json` PASS |
| Final submit path | PASS | eligible sell-first trim `AVGO 1주 @ 387.00 USD` executed |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| AVGO | submitted_filled | 0.3868% | ai_semiconductor target-band de-risking, negative expected excess, same-session duplicate/open-order 0 |
| RGTI | blocked_spread_fail | 0.7137% | speculative loss-control trim trigger는 유지되지만 direct spread가 policy cap 초과 |
| PFE | executable_lower_priority_trim | 0.0386% | repeated weak-review trim 후보이나 이번 cycle의 위험 축소 우선순위는 AVGO가 상위 |
| SO | blocked_spread_and_metric_gap | 5.9691% | live spread 급확대와 trim decision-grade metric gap이 함께 남음 |
| NOK | blocked_validation_lifecycle_add_block | 0.0692% | `review-due-index` add-block과 `pending_1d_count=18` 유지 |
| SPY | blocked_review_backlog_buy | 0.0040% | benchmark fallback이지만 buy path는 review backlog throttle에 막힘 |
| QQQ | blocked_review_backlog_buy | 0.0431% | benchmark fallback이지만 buy path는 review backlog throttle에 막힘 |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| AVGO | trim | pass | target-band de-risking rationale, 음수 expected excess, quote/spread/open-order/risk gate 모두 통과 |
| RGTI | watch | `spread_within_policy` | speculative loss-control trim trigger는 active지만 direct spread `0.7137%`로 hard cap 초과 |
| PFE | watch | `ranked_below_selected_trim` | repeated weak-review trim 후보지만 current weight와 theme de-risking urgency는 AVGO가 더 큼 |

## 주문 제출과 reconciliation

제출 전 게이트 요약은 아래와 같다.

paper mode `true`; market clock `2026-06-16T09:42:13.129128423-04:00`; order plan path `wiki/trade-ledger/orders/2026-06-16-2231-hourly-autopilot.json`; universe strict `PASS`; MCP strict `PASS`; risk validator `PASS`; AVGO quote freshness 약 `0.0`분; spread `0.3868%`; order shape `sell 1 share / limit 387.00 / day / stock / regular`; duplicate/open-order check `PASS`; source refs는 `2231` stale cleanup/core/research preflight, `review-due-index`, `2026-06-16-portfolio-review`, `[[AVGO]]`, `[[RGTI]]`, `[[PFE]]`, `[[SO]]`, `[[NOK]]`다.

| Symbol | Side | Qty | Limit | Status | Filled Avg | Order ID |
| --- | --- | ---: | ---: | --- | ---: | --- |
| AVGO | sell | 1 | 387.00 | filled | 387.76 | `498ab49e-c195-4fce-a049-a4e9020e39f9` |

immediate reconciliation 기준 `get_order_by_client_id`는 `AVGO` 주문을 `status=filled`, `filled_qty=1`, `filled_avg_price=387.76 USD`로 반환했다. `get_all_positions` 기준 `AVGO`는 `2주 @ 435.995`에서 `1주 @ 435.995`로 갱신됐고 `get_account_info` 기준 cash는 `29,836.34 USD -> 30,224.10 USD`, portfolio value는 `102,171.80 USD -> 102,163.28 USD`로 갱신됐다. `get_orders(status=open)`는 `0`건, `get_account_activities(activity_types=[FILL], after=2026-06-16T13:30:00Z)`는 `AVGO` fill 1건을 반환했다.

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | broad universe 62개, shortlist 7개 |
| `check-mcp-coverage.py --strict --json` | PASS | Alpaca core pass, positive research 3개, Alpha/Firecrawl non-core gap |
| `check-risk-policy.py --json` | PASS | AVGO floor-size trim order plan 통과 |

## 산출물

- Report: `wiki/current-runs/daily/2026-06-16-2231-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-16-2231-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-16-2231-hourly-autopilot.json`
- Runtime gate evaluation: `wiki/evidence-store/sources/2026-06-16-2231-hourly-autopilot-runtime-gate-evaluation.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-16-2231-hourly-autopilot-post-trade.json`

## 지표 설명

- `pass_tiered`: core MCP와 최소 research confirmation이 확보돼 일부 non-core provider gap이 있어도 submit 가능하다는 뜻이다.
- `target-band de-risking`: theme/factor/cluster warning band와 성과 저하가 겹칠 때 staged trim을 허용하는 정책 경로다.
- `review_backlog_throttle`: 신규 validation buy에만 적용되는 backlog 제동 규칙이다. 이번 cycle에서는 sell-first trim이 먼저 열렸고 buy path는 여전히 `pending_1d_count=18`에 막혔다.
- `spread_within_policy`: direct submit-boundary quote의 bid/ask spread가 `harness/risk-policy.yaml` 상한 이내여야 한다는 뜻이다.
