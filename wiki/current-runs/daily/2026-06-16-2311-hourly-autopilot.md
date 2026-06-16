# 2026-06-16-2311-hourly-autopilot scheduled paper autopilot

## 요약

정규장 scheduled hourly autopilot을 실행했다. `.env`의 `ALPACA_PAPER_TRADE=true`는 유지됐고, scheduler-owned `2311` stale cleanup/core/research preflight를 source-of-record로 사용했다. stale cleanup은 `status=pass`, core preflight는 `market_open/account/positions/open_orders/recent_activities/quotes` hard gate를 모두 PASS로 기록했다. direct Alpaca submit-boundary check도 `2026-06-16T10:14:19.689714377-04:00` 기준 regular market open, account `ACTIVE`, existing open order `1(RGTI trim)`, current-session same-day fill `0`를 재확인했다.

이번 cycle에서 sell-first 경로의 유일한 executable 후보는 `[[PFE]]`였다. `[[RGTI]]`는 live quote 자체는 정상화됐지만 직전 cycle의 `client_order_id=hourly-20260616-2251-sell-rgti` open sell 7주가 아직 `status=new`로 남아 있어 same-symbol duplicate/open-order lifecycle 재제출 대상이 아니었다. `[[SO]]`는 live quote `88.70/94.62`로 spread `6.4603%`가 policy cap `0.50%`를 크게 넘어 hard gate에서 탈락했다. buy fallback은 `review_backlog_pending_1d_count=18`과 `NOK` add-block 때문에 정책상 닫혀 있었다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env`의 `ALPACA_PAPER_TRADE=true` 확인 |
| Market clock pre-submit | PASS | direct `get_clock` timestamp `2026-06-16T10:14:19.689714377-04:00`, market open |
| Stale order lifecycle | PASS | scheduler cleanup `status=pass`; stale blocking order 없음 |
| Alpaca core MCP | PASS | scheduler-owned core preflight hard gate pass + direct boundary recheck |
| Research MCP | PASS tiered | SEC EDGAR/FRED/Yahoo positive; Alpha throttle `provider_error`, Firecrawl credits 부족 `unknown` non-core gap |
| Universe strict | PASS | metadata universe 62개, SPY/QQQ 포함 |
| Quote/spread | PASS for planned order | direct `PFE` quote `25.90/25.91`, spread `0.0386%`, freshness 약 `0.0`분 |
| Risk plan | PASS | `check-risk-policy.py --json` PASS |
| Final submit path | PASS | executable sell-first trim `PFE 1주 @ 25.90 USD` |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| PFE | submitted_filled | 0.0386% | repeated weak-review trim precedent, defensive-healthcare thesis 약화, same-day duplicate 없음 |
| RGTI | blocked_open_order_duplicate | 0.0925% | 기존 `hourly-20260616-2251-sell-rgti` open sell 7주가 아직 살아 있어 재제출 비대상 |
| SO | blocked_spread_fail | 6.4603% | live quote `88.70/94.62`가 policy spread cap 초과 |
| AVGO | blocked_min_remaining_qty | 0.9103% | prior trims 뒤 `keep_minimum_remaining_qty=1` 경로 유지 |
| NOK | blocked_validation_lifecycle_add_block | 0.1387% | `review-due-index` add-block과 backlog buy throttle 유지 |
| SPY | blocked_review_backlog_buy | 0.0146% | benchmark fallback이지만 buy path는 `pending_1d_count=18`에 막힘 |
| QQQ | blocked_review_backlog_buy | 0.0377% | benchmark fallback이지만 buy path는 `pending_1d_count=18`에 막힘 |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| PFE | trim | pass | weak review 누적, `25.90/25.91` fresh quote, spread pass, same-day sell 0 |
| RGTI | watch | `open_order_check` | speculative trim trigger는 유지되지만 same-symbol open sell 1건이 재제출을 막음 |
| SO | watch | `spread_within_policy` | weak-to-neutral review는 남지만 live spread fail이 우선 hard blocker |

## 주문 제출과 reconciliation

제출 전 게이트 요약은 아래와 같다.

paper mode `true`; market clock `2026-06-16T10:14:19.689714377-04:00`; order plan path `wiki/trade-ledger/orders/2026-06-16-2311-hourly-autopilot.json`; universe strict `PASS`; MCP strict `PASS`; risk validator `PASS`; `PFE` quote freshness 약 `0.0`분; spread `0.0386%`; order shape `sell 1 share / limit 25.90 / day / stock / regular`; duplicate/open-order check `PFE same-day sell 0, existing open order는 RGTI에만 국한`; source refs는 `2311` stale cleanup/core/research preflight, runtime gate note, `review-due-index`, `[[PFE]]`, `[[RGTI]]`, `[[SO]]`, `[[NOK]]`다.

| Symbol | Side | Qty | Limit | Status | Filled Avg | Order ID |
| --- | --- | ---: | ---: | --- | ---: | --- |
| PFE | sell | 1 | 25.90 | filled | 25.94 | `4eedfe47-fa78-4f51-a71b-f14c7731f516` |

reconciliation 기준 `get_orders(status=all, after=2026-06-16T14:18:00Z)`는 `PFE` 주문을 `filled`로 반환했고, `get_account_activities(activity_types=[FILL], after=2026-06-16T14:18:00Z)`도 `2026-06-16T14:18:55.368488Z` `25.94 USD` fill 1건을 확인했다. `get_all_positions` 기준 `PFE`는 `4주 -> 3주`, `avg_entry_price=25.925`, `qty_available=3`으로 감소했다. `get_orders(status=open)`는 기존 `RGTI` sell 7주 open order 1건만 유지했고, `get_account_info` 기준 cash는 `30,250.04 USD`, portfolio value는 `101,888.16 USD`였다.

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | broad universe 62개, shortlist 7개 |
| `check-mcp-coverage.py --strict --json` | PASS | Alpaca core pass, positive research 3개, Alpha/Firecrawl non-core gap |
| `check-risk-policy.py --json` | PASS | `PFE` 1주 trim order plan 통과 |

## 산출물

- Report: `wiki/current-runs/daily/2026-06-16-2311-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-16-2311-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-16-2311-hourly-autopilot.json`
- Runtime gate evaluation: `wiki/evidence-store/sources/2026-06-16-2311-hourly-autopilot-runtime-gate-evaluation.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-16-2311-hourly-autopilot-post-trade.json`

## 지표 설명

- `pass tiered`: core MCP와 최소 research confirmation이 확보돼 일부 non-core provider gap이 있어도 submit 가능하다는 뜻이다.
- `open_order_check`: stale blocker는 아니지만 동일 symbol/side open order가 남아 있으면 추가 재제출을 막는 lifecycle 검사다.
- `review_backlog_throttle`: 신규 validation buy에만 적용되는 backlog 제동 규칙이다. 이번 cycle에서는 sell-first trim이 먼저 열렸고 buy path는 여전히 `pending_1d_count=18`에 막혔다.
- `spread_within_policy`: direct submit-boundary quote의 bid/ask spread가 `harness/risk-policy.yaml` 상한 이내여야 한다는 뜻이다.
