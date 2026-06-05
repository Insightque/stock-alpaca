# 2026-06-06-0431-hourly-autopilot scheduled paper autopilot

## 요약

정규장 scheduled hourly autopilot을 실행했다. `.env`의 `ALPACA_PAPER_TRADE=true`를 확인했고, scheduler-owned `0431` stale cleanup/core/research preflight를 우선 사용했다. stale cleanup은 open order 0건으로 종료됐고, core preflight hard gate도 `pass`였다. runtime Alpaca MCP에서는 `get_clock`, `get_account_info`, `get_orders(status=all, symbols=NEE,NKE,TSLA,SO,AVGO, after=2026-06-05T04:00:00Z)`를 추가로 확인했다.

이번 run은 sell/trim을 먼저 평가했지만 `AVGO`는 same-day duplicate sell, `SO`는 decision-grade metric gap, `TSLA`는 held-quantity and metric gap 때문에 실제 trim/exit로 승격되지 못했다. buy fallback에서는 `NEE`가 0231 cycle same-day canceled buy 이력 때문에 stale-cancel reentry/duplicate discipline에 막혔고, `NKE`는 runtime `get_asset(NKE)` 1회 확인이 tool layer에서 `cancelled`로 끝나 asset hard gate를 닫지 못했다. `SPY`와 `QQQ`는 validation floor per-order cap을 넘었다. 따라서 이번 cycle은 hard-gate 수준의 exact blocker를 남긴 채 `orders: []`로 종료한다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env`의 `ALPACA_PAPER_TRADE=true` 확인 |
| Market clock | PASS | runtime `get_clock` `2026-06-05T15:35:49.031187181-04:00`, regular market open |
| Stale order lifecycle | PASS | `0431` stale cleanup artifact 기준 open order 0건 |
| Alpaca core MCP | PASS | scheduler-owned core preflight hard gate pass, positions 33건, recent fills 20건 |
| Research MCP | PASS tiered | SEC EDGAR/FRED/Firecrawl/Yahoo positive; Alpha `empty_response` gap only |
| Universe strict | PASS | metadata universe 62개, SPY/QQQ 포함 |
| Quote/spread | PASS for screened symbols | `AVGO/SO/TSLA/NEE/NKE/SPY/QQQ` preflight quote 모두 freshness 범위 내 |
| Risk plan | PASS | `check-risk-policy.py --json` PASS |
| Final submit path | BLOCK | sell 3종은 sell gate 미통과, buy fallback은 duplicate/asset-check/per-order-cap blocker |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| AVGO | watch_same_day_sell | 0.0334% | 0331 cycle sell 4주가 same-day all-orders에 이미 존재해 같은 side trim 재진입 불가 |
| SO | watch_metric_gap | 0.0323% | weak-to-neutral review 누적은 있으나 trim replacement margin이 비어 있음 |
| TSLA | watch_held_qty_gap | 0.0256% | speculative loss-control 재점검 대상이지만 1주 보유라 whole-share trim 규칙을 만들기 어렵고 metric도 비어 있음 |
| NEE | blocked_reentry | 0.0117% | 0231 cycle `hourly-20260606-0231-buy-nee`가 same-day `canceled` 처리돼 stale-cancel reentry 회피 유지 |
| NKE | blocked_asset_check | 0.0233% | same-day symbol/side order는 없지만 runtime `get_asset(NKE)` 1회 확인이 `cancelled`로 끝나 asset/tradable hard gate를 닫지 못함 |
| SPY | blocked_validation_floor_cap | 0.0041% | 1주 ask `737.82 USD`가 validation floor `0.5%` per-order cap을 초과 |
| QQQ | blocked_validation_floor_cap | 0.0099% | 1주 ask `707.86 USD`가 validation floor `0.5%` per-order cap을 초과 |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| AVGO | watch | same_day_duplicate_symbol_side | 0331 cycle trim 4주 filled가 same-day all-orders에 남아 있어 0431 cycle 추가 trim 불가 |
| SO | watch | decision_grade_metric_gap | review 약세와 FRED macro pass는 확인됐지만 trim justification용 expected-excess/replacement margin 공백 |
| TSLA | watch | held_quantity_and_metric_gap | 1주 보유라 minimum remaining qty를 만족하면서 trim할 수 없고 decision-grade metric도 비어 있음 |

## 주문/체결

- Planned orders: 0
- Submitted orders: 0
- `place_stock_order` 호출: 없음
- Pre-submit gate summary: 주문 후보가 최종 hard gate를 통과하지 못해 작성/호출 대상이 없었다.
- Post-trade reconciliation: submit attempt는 없었지만 `0431` core preflight 기준 open orders 0건, positions 33건, recent fills 20건을 post-trade artifact에 기록했다. 특히 `INTC` 0411 exit sell은 `2026-06-05T19:24:41.14102Z`에 `99.93 USD` fill로 닫힌 것이 recent activities에서 확인됐다.

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | 62 symbols, SPY/QQQ 포함, final candidates 5개 |
| `check-mcp-coverage.py --strict --json` | PASS | Alpaca core pass, positive research 4개, Alpha `empty_response` gap only |
| `check-risk-policy.py --json` | PASS | 주문 0건, 현재 포지션 포함 |

## 산출물

- Report: `wiki/current-runs/daily/2026-06-06-0431-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-06-0431-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-06-0431-hourly-autopilot.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-06-0431-hourly-autopilot-post-trade.json`

## 지표 설명

- `sell_candidate_diagnostics`: 보유 포지션 중 trim/exit 재점검이 필요한 상위 후보와 metric gap 사유를 남기는 audit trail이다.
- `same-day duplicate discipline`: 같은 정규장 세션에서 이미 submit/fill/cancel 이력이 있는 동일 symbol/side를 반복 학습 주문으로 재사용하지 않는 규칙이다.
- `validation floor per-order cap`: `confidence_tiers.validation_floor.max_notional_pct=0.005`에 따라 1주 notional이 계좌 가치의 0.5%를 넘는 benchmark fallback 매수는 막는다.
- `asset-check cancelled`: scheduler preflight에 없는 candidate asset row를 runtime Alpaca MCP로 1회 보강하려 했지만 `cancelled`로 끝나 asset/tradable hard gate를 닫지 못한 상태다.
