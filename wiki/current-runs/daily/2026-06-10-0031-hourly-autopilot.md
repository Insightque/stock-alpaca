# 2026-06-10-0031-hourly-autopilot scheduled paper autopilot

## 요약

정규장 scheduled hourly autopilot을 실행했다. `ALPACA_PAPER_TRADE=true`를 확인했고, scheduler-owned `0031` stale cleanup/core/research preflight를 우선 사용했다. stale cleanup JSON 기준 stale candidate는 없었고 fresh open order `SO` buy 1주와 `WMT` buy 1주만 남아 있었다. runtime Alpaca MCP `get_clock/get_account_info/get_orders/get_account_activities/get_all_positions/get_stock_latest_quote/get_asset` 재확인에서도 regular market open, account `ACTIVE`, open orders 2건, same-day fill `BAC` buy 1건과 `RGTI` sell 22건만 유지됐다.

sell/trim 재평가에서는 `AVGO`가 live quote `380.32/398.95` 기준 spread `4.7804%`로 정책 상한 `0.50%`를 크게 넘겨 trim hard gate fail, `RGTI`는 same-day sell fill 때문에 duplicate symbol/side conflict, `SO`는 same-day open buy와 trim decision-grade metric gap으로 risk-reducing sell submit에 승격되지 못했다. buy fallback에서는 `WMT`가 fresh open-order duplicate, `BAC`가 same-day buy fill duplicate, `SPY/QQQ`가 validation floor per-order cap 초과, `NOK`가 validation_lifecycle add-block, `NEE`가 utilities cluster open-order conflict로 막혔다. 그 다음 clean candidate였던 `PFE` 1주 buy는 quote/research/cap 기준으로는 통과했지만, risk validator가 `WMT` open buy age `32.7`분을 잡아 `risk_open_order_lifecycle`로 실패했기 때문에 제출하지 않았다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env`의 `ALPACA_PAPER_TRADE=true` 확인 |
| Market clock | PASS | runtime `get_clock` `2026-06-09T11:33:59.847821433-04:00`, regular market open |
| Stale order cleanup | PASS then runtime stale | scheduler cleanup 시점에는 stale candidate 0건이었지만 `WMT` open buy가 validator 시점에 30분 초과 |
| Alpaca core MCP | PASS | scheduler-owned core preflight hard gate pass + runtime `get_clock/get_account_info/get_orders/get_account_activities/get_all_positions/get_stock_latest_quote/get_asset` 재확인 |
| Research MCP | PASS tiered | SEC EDGAR/FRED/Firecrawl/Yahoo positive, Alpha Vantage one-call throttle `provider_error` gap only |
| Universe strict | PASS | metadata universe 62개, SPY/QQQ 포함 |
| Quote/spread | PASS for blocked candidate | `PFE` live quote `25.62/25.63`, spread `0.0390%`, freshness pass |
| Risk plan | FAIL | `check-risk-policy.py --json`가 `WMT: open order age 32.7 minutes exceeds lifecycle limit 30.0` 반환 |
| Final submit path | FAIL | first blocking gate=`risk_open_order_lifecycle`; 신규 Alpaca submit 없음 |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| AVGO | watch | 4.7804% | ai_semiconductor warning band와 de-risk watch는 유지되지만 live spread가 정책 상한 초과 |
| RGTI | watch | 0.0509% | speculative loss-control trim trigger는 유지되나 same-day earlier sell fill 때문에 duplicate sell gate |
| SO | watch | 0.0324% | fresh same symbol/side open buy와 trim metric gap이 동시에 남아 있음 |
| WMT | block | 0.0334% | fresh open buy가 validator 시점에 lifecycle 30분 한도를 초과 |
| BAC | watch | 0.0186% | same-day buy fill이 이미 있어 duplicate buy gate |
| SPY | watch | 0.0041% | 1주 ask `731.28 USD`가 validation floor per-order cap 초과 |
| QQQ | watch | 0.0783% | 1주 ask `702.21 USD`가 validation floor per-order cap 초과 |
| NOK | watch | 0.0729% | `review-due-index` add-block 유지 |
| NEE | watch | 0.0238% | utilities cluster에 fresh `SO` open buy가 있어 same-cluster new buy gate |
| PFE | watch | 0.0390% | healthcare diversifier fallback 자체는 passable이었지만 `risk_open_order_lifecycle`가 최종 blocker |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| AVGO | watch | spread_out_of_policy | live spread `4.7804%`가 policy cap `0.50%` 초과 |
| RGTI | watch | duplicate_symbol_side_same_day | earlier `RGTI` sell fill `22주` 때문에 이번 cycle 추가 same-day sell 차단 |
| SO | watch | decision_grade_metric_gap | trim justification용 decision-grade expected-excess/replacement margin 공백 지속 |

## 주문 제출과 reconciliation

- Planned order before risk validation: `PFE` buy `1` @ `25.63 USD` day limit
- Pre-submit gate summary: paper mode `true`, market open, universe strict `PASS`, MCP strict `PASS`, risk `FAIL(risk_open_order_lifecycle)`, `PFE` quote freshness/spread `PASS`, same-day duplicate/open-order conflict 없음, 그러나 `WMT` stale open order가 lifecycle gate를 block
- Orders: 없음. `place_stock_order`와 `cancel_order_by_id`는 호출하지 않았다.
- Immediate reconciliation: `get_orders(status=open)` 기준 `SO`/`WMT` open buy 2건이 그대로 남아 있다. `get_account_activities(activity_types=FILL, after=2026-06-09T00:00:00Z)` 기준 same-day fill은 `BAC` buy 1건과 `RGTI` sell 22건뿐이며, 이번 cycle 신규 fill은 없다. `get_all_positions`는 `32` positions 유지다.

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | actionable strict gate 통과 |
| `check-mcp-coverage.py --strict --json` | PASS | Alpha throttle gap 포함 tiered strict gate 통과 |
| `check-risk-policy.py --json` | FAIL | `WMT` open order age `32.7`분이 lifecycle limit `30.0` 초과 |

## 산출물

- Report: `wiki/current-runs/daily/2026-06-10-0031-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-10-0031-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-10-0031-hourly-autopilot.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-10-0031-hourly-autopilot-post-trade.json`
- Source refs: `wiki/evidence-store/sources/2026-06-10-0031-hourly-autopilot-stale-order-cleanup.json`, `wiki/evidence-store/sources/2026-06-10-0031-hourly-autopilot-alpaca-core-preflight.json`, `wiki/evidence-store/sources/2026-06-10-0031-hourly-autopilot-research-mcp-preflight.json`, `wiki/evidence-store/sources/2026-06-10-0031-hourly-autopilot-runtime-gate-evaluation.json`, `wiki/evidence-store/sources/2026-06-10-0031-hourly-autopilot-deterministic-submit.json`

## 지표 설명

- `risk_open_order_lifecycle`: stale cleanup 이후에도 autopilot open order가 lifecycle 한도를 넘겨 남아 있을 때 신규 주문을 막는 hard gate다.
- `sell_candidate_diagnostics`: 보유 포지션 중 trim/exit 재점검이 필요한 상위 미실행 후보와 blocked gate를 남기는 audit trail이다.
- `decision_grade_metric_gap`: trim은 열려 있어도 expected-excess/replacement margin 같은 결정급 지표가 비면 risk-reducing sell로 승격하지 않는다는 뜻이다.
- `validation_lifecycle add-block`: 기존 validation buy의 due review가 남아 있어 해당 symbol의 추가 매수를 막는 규칙이다. 이번 cycle에서는 `NOK`에만 적용됐다.
- `provider_error`: 이번 run의 Alpha Vantage는 scheduler-owned one-call-per-hour throttle 때문에 provider_error gap으로만 기록됐고, 나머지 4개 research confirmations가 유지돼 strict MCP gate는 통과했다.
