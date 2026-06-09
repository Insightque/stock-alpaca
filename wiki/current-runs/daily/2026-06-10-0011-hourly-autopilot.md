# 2026-06-10-0011-hourly-autopilot scheduled paper autopilot

## 요약

정규장 scheduled hourly autopilot을 실행했다. `ALPACA_PAPER_TRADE=true`를 확인했고, scheduler-owned `0011` stale cleanup/core/research preflight를 우선 사용했다. stale cleanup JSON 기준 fresh open order `WMT` buy 1주가 남아 있었지만 stale candidate는 아니었고, runtime Alpaca MCP `get_orders(status=open)` 재확인에서도 `WMT`는 `status=new` open order로 유지됐다. 이 open order는 same symbol/side duplicate만 막고 different-cluster fallback buy를 전면 차단하지 않으므로 sell-first 재평가를 이어갔다.

sell/trim 재평가에서는 `AVGO`가 live quote `386.00/388.42` 기준 spread `0.6251%`로 정책 상한 `0.50%`를 넘겨 trim hard gate fail, `RGTI`는 same-day sell fill 때문에 duplicate symbol/side conflict, `SO`는 trim decision-grade metric gap으로 risk-reducing sell submit에 승격되지 못했다. buy fallback에서는 `WMT`가 fresh open-order duplicate, `BAC`가 same-day buy fill duplicate, `SPY/QQQ`가 validation floor per-order cap 초과, `NOK`가 validation_lifecycle add-block으로 막혔다. 따라서 `SO` 1주 regular-session day limit buy를 floor-size existing holding fallback으로 제출했다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env`의 `ALPACA_PAPER_TRADE=true` 확인 |
| Market clock | PASS | runtime `get_clock` `2026-06-09T11:13:43.961686036-04:00`, regular market open |
| Stale order cleanup | PASS | stale candidate 0건, fresh `WMT` open buy만 남음 |
| Alpaca core MCP | PASS | scheduler-owned core preflight hard gate pass + runtime `get_clock/get_account_info/get_orders/get_account_activities/get_stock_latest_quote/get_stock_snapshot/get_all_positions/get_asset` 재확인 |
| Research MCP | PASS tiered | SEC EDGAR/FRED/Firecrawl/Yahoo positive, Alpha Vantage one-call throttle `provider_error` gap only |
| Universe strict | PASS | metadata universe 62개, SPY/QQQ 포함 |
| Quote/spread | PASS for submitted order | `SO` pre-submit live quote `91.90/92.03`, spread `0.1414%`, freshness pass |
| Risk plan | PASS | `SO` 1주 buy notional `92.03 USD`, cash/exposure/ticker/theme/factor/cluster caps 통과 |
| Final submit path | PASS | eligible sell 없음, exact buy-side blockers 기록 후 `SO` 1주 fallback buy가 learning_trade_directive와 hard gate를 모두 충족 |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| AVGO | watch | 0.6251% | ai_semiconductor warning band와 de-risk watch는 유지되지만 live spread가 정책 상한 초과 |
| RGTI | watch | 0.0487% | speculative loss-control trim trigger는 유지되나 same-day earlier sell fill 때문에 duplicate sell gate |
| SO | submit | 0.1414% | trim metric gap은 남지만 buy-side floor-size existing holding fallback hard gate 통과 |
| WMT | watch | 0.0335% | fresh open buy order가 남아 same symbol/side duplicate gate |
| BAC | watch | 0.0185% | same-day buy fill이 이미 있어 duplicate buy gate |
| SPY | watch | 0.0027% | 1주 ask `737.70 USD`가 validation floor per-order cap 초과 |
| QQQ | watch | 0.0084% | 1주 ask `711.43 USD`가 validation floor per-order cap 초과 |
| NOK | watch | 0.0715% | `review-due-index` add-block 유지 |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| AVGO | watch | spread_out_of_policy | live spread `0.6251%`가 policy cap `0.50%` 초과 |
| RGTI | watch | duplicate_symbol_side_same_day | earlier `RGTI` sell fill `22주` 때문에 이번 cycle 추가 same-day sell 차단 |
| SO | watch | decision_grade_metric_gap | trim justification용 decision-grade expected-excess/replacement margin 공백 지속 |

## 주문 제출과 reconciliation

- Planned order: `SO` buy `1` @ `92.03 USD` day limit
- Pre-submit gate summary: paper mode `true`, market open, universe strict `PASS`, MCP strict `PASS`, risk `PASS`, `SO` pre-submit quote freshness/spread `PASS`, same-day duplicate/open-order conflict 없음
- `place_stock_order`: `SO` buy 1주 `@ 92.03 USD`, `client_order_id=hourly-20260610-0011-buy-so`, `order_id=8775f764-2758-4958-9fa1-21a92e69fb91`
- Immediate reconciliation: `get_orders(status=open)` 기준 `SO` 주문은 `status=new`, `filled_qty=0` open order다. 기존 `WMT` buy 1주 open order도 그대로라 current open orders는 2건이다. `get_account_activities(activity_types=FILL, after=2026-06-09T15:15:00Z)`는 0건이었고 `get_all_positions`도 `32` positions 유지라 즉시 체결은 없었다.
- Post-submit quote note: reconciliation 직후 `SO` latest quote는 `92.27/96.81`로 widened spread 상태였지만, submit hard gate 평가는 order 직전 `91.90/92.03` quote로 완료했다.

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | actionable strict gate 통과 |
| `check-mcp-coverage.py --strict --json` | PASS | Alpha throttle gap 포함 tiered strict gate 통과 |
| `check-risk-policy.py --json` | PASS | staged-deployment warning only |

## 산출물

- Report: `wiki/current-runs/daily/2026-06-10-0011-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-10-0011-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-10-0011-hourly-autopilot.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-10-0011-hourly-autopilot-post-trade.json`
- Source refs: `wiki/evidence-store/sources/2026-06-10-0011-hourly-autopilot-stale-order-cleanup.json`, `wiki/evidence-store/sources/2026-06-10-0011-hourly-autopilot-alpaca-core-preflight.json`, `wiki/evidence-store/sources/2026-06-10-0011-hourly-autopilot-research-mcp-preflight.json`, `wiki/evidence-store/sources/2026-06-10-0011-hourly-autopilot-runtime-gate-evaluation.json`, `wiki/evidence-store/sources/2026-06-10-0011-hourly-autopilot-deterministic-submit.json`

## 지표 설명

- `sell_candidate_diagnostics`: 보유 포지션 중 trim/exit 재점검이 필요한 상위 미실행 후보와 blocked gate를 남기는 audit trail이다.
- `decision_grade_metric_gap`: trim은 열려 있어도 expected-excess/replacement margin 같은 결정급 지표가 비면 risk-reducing sell로 승격하지 않는다는 뜻이다.
- `validation_lifecycle add-block`: 기존 validation buy의 due review가 남아 있어 해당 symbol의 추가 매수를 막는 규칙이다. 이번 cycle에서는 `NOK`에만 적용됐다.
- `learning_trade_directive`: hard gate가 모두 통과하고 executable sell이 없을 때 benchmark/diversifier/existing holding의 floor-size buy를 강제하는 validation policy다.
- `provider_error`: 이번 run의 Alpha Vantage는 scheduler-owned one-call-per-hour throttle 때문에 provider_error gap으로만 기록됐고, 나머지 4개 research confirmations가 유지돼 strict MCP gate는 통과했다.
