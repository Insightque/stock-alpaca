# 2026-06-06-0451-hourly-autopilot scheduled paper autopilot

## 요약

정규장 scheduled hourly autopilot을 실행했다. `.env`의 `ALPACA_PAPER_TRADE=true`를 확인했고, scheduler-owned `0451` stale cleanup/core/research preflight를 우선 사용했다. preflight 기준 stale open order는 0건, Alpaca core hard gate는 `pass`였다. sell/trim-first 평가에서는 `AVGO`가 same-day duplicate sell, `SO`가 decision-grade metric gap, `TSLA`가 held-quantity/metric gap 때문에 risk-reducing sell로 승격되지 못했다.

buy fallback에서는 `NKE`가 existing consumer diversifier holding이면서 same-day duplicate/open-order 0건, asset active/tradable, preflight quote `43.19/43.20` spread `0.0231%`, tiered MCP strict pass, risk validator pass 조건을 충족해 floor-size learning candidate로 승격됐다. 그러나 실제 `place_stock_order`는 `2026-06-05T20:00:07.873287392Z`, 즉 `16:00:07 ET`에 기록되어 regular close 이후로 넘어갔다. runtime `get_clock`가 `2026-06-05T16:00:39.341819415-04:00`, `is_open=false`를 반환한 뒤 해당 order를 즉시 취소했고, 최종 standing order와 fill은 남기지 않았다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env`의 `ALPACA_PAPER_TRADE=true` 확인 |
| Market clock pre-submit | PASS | scheduler-owned core preflight `2026-06-05T15:51:13.261248906-04:00`, regular market open |
| Market clock post-submit reconciliation | FAIL | runtime `get_clock` `2026-06-05T16:00:39.341819415-04:00`, `is_open=false` |
| Stale order lifecycle | PASS | `0451` stale cleanup artifact 기준 open order 0건 |
| Alpaca core MCP | PASS | scheduler-owned core preflight hard gate pass, runtime `get_order_by_client_id/get_order_by_id`로 order 상태 확인 |
| Research MCP | PASS tiered | SEC EDGAR/FRED/Firecrawl/Yahoo positive; Alpha one-call throttle `provider_error` gap only |
| Universe strict | PASS | metadata universe 62개, SPY/QQQ 포함 |
| Quote/spread | PASS for planned order | `NKE` preflight quote `43.19/43.20`, spread `0.0231%` |
| Risk plan | PASS | `check-risk-policy.py --json` PASS |
| Final execution state | CANCELED | actual submit timestamp가 close 이후로 밀려 workflow safety 복구 차원에서 즉시 cancel |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| NKE | canceled_after_close | 0.0231% | pre-submit hard gate는 모두 통과했지만 actual submit이 `16:00:07 ET`에 기록돼 즉시 취소 |
| AVGO | watch_same_day_sell | 0.1847% | 0331 cycle trim 4주가 same-day all-orders에 존재해 같은 side trim 재진입 불가 |
| SO | watch_metric_gap | 0.0215% | weak-to-neutral review 누적은 있으나 trim replacement margin이 비어 있음 |
| TSLA | watch_held_qty_gap | 0.0254% | speculative loss-control 재점검 대상이지만 1주 보유라 whole-share trim 규칙을 만들기 어렵고 metric도 비어 있음 |
| IONQ | blocked_spread | 2.5623% | existing holding fallback이지만 quote `55.82/57.25` spread가 policy 상한 `0.50%`를 초과 |
| HOOD | watch_new_speculative | 0.0122% | active/tradable과 quote는 pass지만 existing holding/diversifier fallback보다 우선순위가 낮고 신규 speculative broker add로 분류 |
| SPY | blocked_validation_floor_cap | 0.0041% | 1주 ask가 validation floor per-order cap을 초과 |
| QQQ | blocked_validation_floor_cap | 0.0099% | 1주 ask가 validation floor per-order cap을 초과 |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| AVGO | watch | same_day_duplicate_symbol_side | 0331 cycle trim 4주 filled가 same ET session에 남아 있어 0451 cycle 추가 trim 불가 |
| SO | watch | decision_grade_metric_gap | review 약세와 FRED macro pass는 확인됐지만 trim justification용 expected-excess/replacement margin 공백 |
| TSLA | watch | held_quantity_and_metric_gap | 1주 보유라 minimum remaining qty를 만족하면서 trim할 수 없고 decision-grade metric도 비어 있음 |

## 주문 제출과 reconciliation

- Planned order: `NKE` buy 1 @ `43.20` day limit
- Alpaca order id: `40b6fc5b-30e7-48bc-8035-a47bd7efb084`
- Client order id: `hourly-20260606-0451-buy-nke`
- Pre-submit gate summary: paper mode `true`, market open, universe strict `PASS`, MCP strict `PASS`, risk `PASS`, NKE quote freshness/spread `PASS`, same-day duplicate/open-order conflict 없음
- `place_stock_order`: Alpaca accepted the order with `status=accepted`, but `submitted_at=2026-06-05T20:00:07.873287392Z` (`16:00:07 ET`) so regular close 이후에 도착했다
- Reconciliation: runtime `get_clock`는 `2026-06-05T16:00:39.341819415-04:00`, `is_open=false`를 반환했다. `cancel_order_by_id`를 즉시 호출했고 `get_order_by_client_id/get_order_by_id`는 동일 주문을 `status=canceled`, `filled_qty=0`, `canceled_at=2026-06-05T20:00:50.537163308Z`로 확인했다. symbol-scoped `get_orders(status=all, symbols=NKE, after=2026-06-05T04:00:00Z)`도 canceled 1건만 반환해 fill이 없음을 재확인했다.

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | 62 symbols, SPY/QQQ 포함, final candidates 4개 |
| `check-mcp-coverage.py --strict --json` | PASS | Alpaca core pass, positive research 4개, Alpha `provider_error` gap only |
| `check-risk-policy.py --json` | PASS | NKE 1주 regular-session day limit buy 계획 통과 |

## 산출물

- Report: `wiki/current-runs/daily/2026-06-06-0451-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-06-0451-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-06-0451-hourly-autopilot.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-06-0451-hourly-autopilot-post-trade.json`

## 지표 설명

- `sell_candidate_diagnostics`: 보유 포지션 중 trim/exit 재점검이 필요한 상위 후보와 metric gap 사유를 남기는 audit trail이다.
- `provider_error`: 이번 cycle의 Alpha Vantage는 one-call-per-hour throttle 때문에 재호출하지 않고 nonblocking gap으로 남겼다.
- `validation floor per-order cap`: `confidence_tiers.validation_floor.max_notional_pct=0.005`에 따라 1주 notional이 계좌 가치의 0.5%를 넘는 benchmark fallback 매수는 막는다.
- `market close race`: pre-submit hard gate는 열려 있었지만 submit RPC가 regular close 이후에 도착한 경우다. 이번 run은 workflow 안전규칙을 복구하기 위해 즉시 cancel로 정리했다.
