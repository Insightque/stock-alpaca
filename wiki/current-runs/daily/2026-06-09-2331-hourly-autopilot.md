# 2026-06-09-2331-hourly-autopilot scheduled paper autopilot

## 요약

정규장 scheduled hourly autopilot을 실행했다. `ALPACA_PAPER_TRADE=true`를 확인했고, scheduler-owned `2331` stale cleanup/core/research preflight를 우선 사용했다. stale cleanup JSON은 직전 `AVGO` trim order를 stale candidate로 남겼지만, 더 늦은 scheduler core preflight와 registered Alpaca MCP `get_orders(status=open)` 재확인 기준 현재 open orders는 `0`건이고 `hourly-20260609-2251-sell-avgo`는 `2026-06-09T14:31:11Z`에 `canceled`로 정리됐다.

이번 cycle은 sell/trim을 먼저 다시 평가했다. `AVGO`는 lifecycle block은 해소됐지만 live quote `390.00/394.00` 기준 spread `1.0152%`로 정책 상한 `0.50%`를 넘겨 trim hard gate를 통과하지 못했다. `RGTI`는 speculative loss-control trim trigger를 유지했지만 2026-06-09 ET same-day sell fill 22주가 이미 있어 duplicate symbol/side conflict가 남았다. `SO`는 spread는 정상이나 decision-grade replacement margin 공백이 지속됐다. 따라서 eligible risk-reducing sell/trim이 없었고, learning_trade_directive에 따라 duplicate-free financials diversifier인 `BAC` 1주 regular-session day limit buy를 floor-size validation fallback으로 제출한다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env`의 `ALPACA_PAPER_TRADE=true` 확인 |
| Market clock | PASS | runtime `get_clock` `2026-06-09T10:35:38.546700706-04:00`, regular market open |
| Stale order cleanup | PASS after reconciliation | stale cleanup JSON은 `AVGO` stale candidate 1건을 남겼지만 later core preflight와 runtime `get_orders(status=open)`는 open orders 0건, runtime `get_orders(status=all, symbols=AVGO)`는 `canceled_at=2026-06-09T14:31:11.020892Z` 확인 |
| Alpaca core MCP | PASS | scheduler-owned core preflight hard gate pass + runtime clock/account/orders/positions/snapshot 재확인 |
| Research MCP | PASS tiered | SEC EDGAR/FRED/Firecrawl/Yahoo positive, Alpha Vantage one-call throttle `provider_error` gap only |
| Universe strict | PASS | metadata universe 62개, SPY/QQQ 포함 |
| Quote/spread | PASS for submitted order | `BAC` live quote `54.32/54.33`, spread `0.0184%`, freshness pass |
| Risk plan | PASS | `BAC` 1주 buy notional `54.33 USD`, cash/exposure/ticker/theme/factor/cluster caps 통과 |
| Final submit path | PASS | sell-first 진단 후 eligible sell 없음, `BAC` 1주 validation buy가 learning_trade_directive fallback과 hard gate를 모두 충족 |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| AVGO | watch | 1.0152% | 2251 cycle trim order는 이미 취소됐지만 live spread가 정책 상한을 넘겨 trim hard gate fail |
| RGTI | watch | 0.0474% | speculative loss-control trigger는 유지되지만 same-day earlier sell fill 때문에 duplicate symbol/side conflict |
| SO | watch | 0.1851% | spread는 정상이나 trim justification용 decision-grade expected-excess/replacement margin 공백 지속 |
| BAC | submit | 0.0184% | duplicate-free financials diversifier fallback buy, existing low-weight holding, min research confirmation 유지, review backlog throttle 비차단 |
| SPY | watch | 0.0040% | benchmark fallback 1주 ask가 validation floor per-order cap 초과 |
| QQQ | watch | 0.0084% | benchmark fallback 1주 ask가 validation floor per-order cap 초과 |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| AVGO | watch | spread_out_of_policy | lifecycle block 해소 후에도 live spread가 0.50% 상한 초과 |
| RGTI | watch | duplicate_symbol_side_same_day | earlier `RGTI` sell fill 22주가 이미 있어 이번 cycle 추가 same-day sell 제출 차단 |
| SO | watch | decision_grade_metric_gap | live spread는 정상이나 trim justification용 replacement margin 공백 지속 |

## 주문 제출과 reconciliation

- Planned order: `BAC` buy 1 @ `54.33` day limit
- Pre-submit gate summary: paper mode `true`, market open, universe strict `PASS`, MCP strict `PASS`, risk `PASS`, `BAC` quote freshness/spread `PASS`, same-day duplicate/open-order conflict 없음
- `place_stock_order`: pending
- Reconciliation: submit 이후 `get_orders(status=all, symbols=BAC)`, `get_all_positions`, `get_account_info`로 즉시 재확인할 예정이다.

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | pending | manifest/order-plan 작성 후 실행 |
| `check-mcp-coverage.py --strict --json` | pending | manifest/order-plan 작성 후 실행 |
| `check-risk-policy.py --json` | pending | manifest/order-plan 작성 후 실행 |

## 산출물

- Report: `wiki/current-runs/daily/2026-06-09-2331-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-09-2331-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-09-2331-hourly-autopilot.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-09-2331-hourly-autopilot-post-trade.json`
- Source refs: `wiki/evidence-store/sources/2026-06-09-2331-hourly-autopilot-stale-order-cleanup.json`, `wiki/evidence-store/sources/2026-06-09-2331-hourly-autopilot-alpaca-core-preflight.json`, `wiki/evidence-store/sources/2026-06-09-2331-hourly-autopilot-research-mcp-preflight.json`, `wiki/evidence-store/sources/2026-06-09-2331-hourly-autopilot-runtime-gate-evaluation.json`

## 지표 설명

- `sell_candidate_diagnostics`: 보유 포지션 중 trim/exit 재점검이 필요한 상위 미실행 후보와 blocked gate를 남기는 audit trail이다.
- `spread_out_of_policy`: trim signal이 있어도 live spread가 `harness/risk-policy.yaml` 상한을 넘으면 submit을 막는 hard gate다.
- `learning_trade_directive`: hard gate가 모두 통과하고 executable sell이 없을 때 benchmark/diversifier/existing holding의 floor-size buy를 강제하는 validation policy다.
- `provider_error`: 이번 run의 Alpha Vantage는 scheduler-owned one-call-per-hour throttle 때문에 provider_error gap으로만 기록됐고, 나머지 4개 research confirmations가 유지돼 strict MCP gate는 통과했다.
