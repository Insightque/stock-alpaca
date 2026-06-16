# 2026-06-16-2251-hourly-autopilot scheduled paper autopilot

## 요약

정규장 scheduled hourly autopilot을 실행했다. `.env`의 `ALPACA_PAPER_TRADE=true` 요구는 유지됐고, scheduler-owned `2251` stale cleanup/core/research preflight를 source-of-record로 사용했다. stale cleanup은 open order `0`건, core preflight는 `market_open/account/positions/open_orders/recent_activities/quotes` hard gate를 모두 PASS로 기록했다. direct Alpaca submit-boundary check도 `2026-06-16 09:54 ET` regular market open, account `ACTIVE`, current-session open orders `0`, fills `1(AVGO sell)`을 재확인했다.

이번 cycle은 sell-first 경로가 다시 실제 체결로 이어졌다. `[[RGTI]]`는 speculative loss-control trim trigger, residual speculative sleeve staged de-risking rationale, fresh quote `22.07/22.09`, spread `0.0906%`, current-session duplicate/open-order `0`를 모두 충족해 25% trim `7주` 후보로 승격됐다. `[[PFE]]`와 `[[SO]]`도 trim 가능했지만 risk-reduction priority는 `RGTI`보다 낮았다. buy fallback은 `review_backlog_pending_1d_count=18`과 `NOK` add-block 때문에 정책상 닫혀 있었다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env`의 `ALPACA_PAPER_TRADE=true` 확인 |
| Market clock pre-submit | PASS | direct `get_clock` timestamp `2026-06-16T09:54:13.485803056-04:00`, market open |
| Stale order lifecycle | PASS | scheduler cleanup `status=pass`, remaining open orders `0` |
| Alpaca core MCP | PASS | scheduler-owned core preflight hard gate pass + direct boundary recheck |
| Research MCP | PASS tiered | SEC EDGAR/FRED/Yahoo positive; Alpha throttle `provider_error`, Firecrawl credits 부족 `unknown` non-core gap |
| Universe strict | PASS | metadata universe 62개, SPY/QQQ 포함 |
| Quote/spread | PASS for planned order | direct `RGTI` quote `22.07/22.09`, spread `0.0906%`, freshness 약 `0.0`분 |
| Risk plan | PASS | `check-risk-policy.py --json` PASS |
| Final submit path | PASS | eligible sell-first trim `RGTI 7주 @ 22.07 USD` |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| RGTI | submitted | 0.0906% | speculative loss-control trim trigger, residual speculative sleeve de-risking, same-session duplicate/open-order 0 |
| PFE | executable_lower_priority_trim | 0.0388% | repeated weak-review trim 후보이나 이번 cycle의 위험 축소 우선순위는 RGTI가 상위 |
| SO | executable_lower_priority_trim | 0.0640% | weak-to-neutral validation review 누적은 남지만 speculative sleeve reduction보다 우선순위 낮음 |
| AVGO | blocked_same_day_duplicate_or_min_remaining_qty | 0.5361% | same-session sell fill 1건과 keep-minimum-remaining gate로 추가 trim 비활성 |
| NOK | blocked_validation_lifecycle_add_block | 0.0683% | `review-due-index` add-block과 `pending_1d_count=18` 유지 |
| SPY | blocked_review_backlog_buy | 0.0093% | benchmark fallback이지만 buy path는 review backlog throttle에 막힘 |
| QQQ | blocked_review_backlog_buy | 0.0081% | benchmark fallback이지만 buy path는 review backlog throttle에 막힘 |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| RGTI | trim | pass | speculative loss-control, residual speculative sleeve de-risking, quote/spread/open-order/risk gate 모두 통과 |
| PFE | watch | `ranked_below_selected_trim` | repeated weak-review trim 후보지만 current weight와 speculative-risk reduction urgency는 RGTI가 더 큼 |
| SO | watch | `ranked_below_selected_trim` | quote/spread는 pass지만 weak review 누적만으로는 이번 cycle 우선순위가 낮음 |

## 주문 제출과 reconciliation

제출 전 게이트 요약은 아래와 같다.

paper mode `true`; market clock `2026-06-16T09:54:13.485803056-04:00`; order plan path `wiki/trade-ledger/orders/2026-06-16-2251-hourly-autopilot.json`; universe strict `PASS`; MCP strict `PASS`; risk validator `PASS`; `RGTI` quote freshness 약 `0.0`분; spread `0.0906%`; order shape `sell 7 shares / limit 22.07 / day / stock / regular`; duplicate/open-order check `PASS`; source refs는 `2251` stale cleanup/core/research preflight, `review-due-index`, `2026-06-16-portfolio-review`, `[[RGTI]]`, `[[PFE]]`, `[[SO]]`, `[[NOK]]`다.

| Symbol | Side | Qty | Limit | Status | Filled Avg | Order ID |
| --- | --- | ---: | ---: | --- | ---: | --- |
| RGTI | sell | 7 | 22.07 | new | - | `84d82c1a-3b82-40dc-9794-78071359f629` |

immediate reconciliation 기준 `get_order_by_client_id`는 `RGTI` 주문을 `status=new`, `filled_qty=0`으로 반환했다. `get_orders(status=open)`는 `RGTI` open order 1건을 반환했고, `get_account_activities(activity_types=[FILL], after=2026-06-16T14:00:00Z)`는 신규 fill이 없음을 확인했다. `get_all_positions` 기준 `RGTI`는 `28주` 유지, `qty_available=21`만 예약 상태이며 `get_account_info` 기준 cash는 `30,224.10 USD` 그대로, portfolio value는 `102,087.01 USD`로 반영됐다.

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | broad universe 62개, shortlist 7개 |
| `check-mcp-coverage.py --strict --json` | PASS | Alpaca core pass, positive research 3개, Alpha/Firecrawl non-core gap |
| `check-risk-policy.py --json` | PASS | RGTI 7주 trim order plan 통과 |

## 산출물

- Report: `wiki/current-runs/daily/2026-06-16-2251-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-16-2251-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-16-2251-hourly-autopilot.json`
- Runtime gate evaluation: `wiki/evidence-store/sources/2026-06-16-2251-hourly-autopilot-runtime-gate-evaluation.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-16-2251-hourly-autopilot-post-trade.json`

## 지표 설명

- `pass_tiered`: core MCP와 최소 research confirmation이 확보돼 일부 non-core provider gap이 있어도 submit 가능하다는 뜻이다.
- `speculative loss-control`: speculative sleeve에서 미실현 손실과 변동성 리스크가 누적될 때 staged trim을 허용하는 정책 경로다.
- `review_backlog_throttle`: 신규 validation buy에만 적용되는 backlog 제동 규칙이다. 이번 cycle에서는 sell-first trim이 먼저 열렸고 buy path는 여전히 `pending_1d_count=18`에 막혔다.
- `spread_within_policy`: direct submit-boundary quote의 bid/ask spread가 `harness/risk-policy.yaml` 상한 이내여야 한다는 뜻이다.
