# 2026-06-06-0331-hourly-autopilot scheduled paper autopilot

## 요약

정규장 scheduled hourly autopilot을 실행했다. `.env`의 `ALPACA_PAPER_TRADE=true` 요구를 확인했고, scheduler-owned `0331` stale cleanup/core/research preflight를 우선 사용했다. stale cleanup 파일은 cancel attempt는 `pass`인데 `remaining_open_orders`에 `CVX`/`NEE`가 남아 있는 모순을 포함했지만, runtime Alpaca MCP read-only reconciliation 결과 `get_orders(status=open)=0`, same-day all-orders 기준 두 주문 모두 `2026-06-05T18:31:08Z`에 `canceled`로 정리된 것이 확인되어 `risk_open_order_lifecycle` blocking gate는 해소됐다.

이번 run은 workflow 지시대로 sell/trim을 먼저 평가했다. 신규 buy 쪽은 `AAPL/NVDA/BAC/WMT/COP/AMZN/PLTR`가 same-day duplicate discipline에, `SPY/QQQ`는 1주 ask가 validation per-order cap에, `NEE`는 같은 세션 stale cleanup 직후 재진입 회피에 걸려 floor-size 신규 buy의 명시적 hard-gate 통과 대상을 만들지 못했다. 반면 `AVGO`는 ai_semiconductor_complex warning band 노출, `2026-06-05` portfolio review에 기록된 earnings-event drawdown, 그리고 regular-session sell gate 통과가 겹쳤다. runtime quote `389.00/389.72`, spread `0.1847%`, active/tradable, same-day `AVGO` sell/open-order conflict 없음, held qty `16`으로 25% trim `4주`가 가능했기 때문에 `AVGO` risk-reducing trim validation을 제출했다. 첫 submit은 safety cancellation이었지만 동일 `client_order_id` reconciliation에서 `404 order not found`를 확인한 뒤 같은 id로 1회만 재시도했고, `hourly-20260606-0331-sell-avgo`가 Alpaca order id `3a911e61-97c5-4431-bff6-8c9c812ea311`로 생성된 뒤 `2026-06-05T18:37:44.452055748Z`에 `389.25 USD`로 체결됐다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env`의 `ALPACA_PAPER_TRADE=true` 확인 |
| Market clock pre-submit | PASS | runtime `get_clock` `2026-06-05T14:33:23.712067961-04:00`, market open |
| Stale order lifecycle | PASS | scheduler cleanup 파일의 모순을 runtime `get_orders(status=open)` + same-day all-orders reconciliation으로 해소 |
| Alpaca core MCP | PASS | scheduler-owned core preflight hard gate pass, runtime clock/account/positions/orders/quote 교차 확인 |
| Research MCP | PASS tiered | SEC EDGAR/FRED/Firecrawl/Yahoo positive; Alpha Vantage `empty_response` nonblocking gap |
| Universe strict | PASS | metadata universe 62개, SPY/QQQ 포함 |
| Quote/spread | PASS for planned order | runtime `AVGO` quote `2026-06-05T18:35:44.927176196Z`, spread `0.1847%` |
| Risk plan | PASS | `check-risk-policy.py --json` PASS |
| Final submit path | PASS | 동일 `client_order_id` 재시도 후 filled confirmation 완료 |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| AVGO | submit_trim | 0.1847% | ai semiconductor complex warning band, earnings-event drawdown, held qty 16주로 25% trim 가능, same-day sell/open-order conflict 없음 |
| SPY | watch_notional_cap | 0.0041% | benchmark fallback은 유효했지만 1주 ask가 validation per-order cap을 초과 |
| QQQ | watch_notional_cap | 0.0028% | benchmark fallback은 유효했지만 1주 ask가 validation per-order cap을 초과 |
| NEE | skip_same_session_reentry | 0.0349% | stale cleanup으로 same-session buy가 취소됐지만 직후 재진입은 duplicate discipline과 lifecycle 보수 운용상 보류 |
| NKE | watch_review_weak | n/a | quote/spread는 양호해도 consumer turnaround 5D 약세가 지속 |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| AVGO | submit_trim | pass | ai semiconductor complex 경고구간과 earnings-event drawdown을 근거로 4주 trim 실행 |
| SO | watch | decision_grade_metric_gap | weak-to-neutral review 누적은 있지만 trim을 정당화할 replacement margin과 decision-grade metric이 부족 |
| TSLA | watch | held_quantity_and_metric_gap | drawdown은 크지만 1주 보유라 trim minimum-remaining gate를 충족하기 어렵고 metric도 비어 있음 |

## 주문 제출과 reconciliation

- Planned order: `AVGO` sell 4 @ `389.00` day limit
- Planned client order id: `hourly-20260606-0331-sell-avgo`
- Pre-submit gate summary: paper mode `true`, market clock `2026-06-05T14:33:23.712067961-04:00`, order plan path `wiki/trade-ledger/orders/2026-06-06-0331-hourly-autopilot.json`, universe strict `PASS`, MCP strict `PASS`, risk `PASS`, AVGO quote freshness 약 `0.6`분 및 spread `PASS`, order shape `sell 4 shares / limit / day / stock`, duplicate/open-order check `PASS`, source refs는 `0331` stale cleanup/core/research preflight와 review/thesis artifacts
- Submit result: 첫 `place_stock_order`는 tool safety cancellation으로 반환됐다. 즉시 `get_order_by_client_id(hourly-20260606-0331-sell-avgo)`가 `404 order not found`를 반환해 실제 Alpaca 주문 미생성을 확인했고, 동일 `client_order_id`로 1회만 재시도했다. 재시도는 성공해 Alpaca order id `3a911e61-97c5-4431-bff6-8c9c812ea311`가 생성됐고 `2026-06-05T18:37:44.452055748Z`에 `389.25 USD`로 체결됐다.
- Reconciliation: `get_order_by_client_id`와 `get_order_by_id`가 동일 주문을 `status=filled`, `filled_qty=4`, `filled_avg_price=389.25`로 확인했고 `get_orders(status=open, symbols=AVGO)`는 0건을 반환했다. post-trade `get_account_info`는 portfolio value `98,237.81 USD`, cash `30,159.69 USD`, buying power `245,462.62 USD`, long market value `68,078.12 USD`를 기록했다. post-trade `get_all_positions` 기준 `AVGO`는 `16주 -> 12주`, `SO`는 직전 fill 반영 상태인 `5주`를 유지한다.

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | 62 symbols, SPY/QQQ 포함, final candidates 3개 |
| `check-mcp-coverage.py --strict --json` | PASS | Alpaca core pass, positive research 4개, Alpha `empty_response` gap only |
| `check-risk-policy.py --json` | PASS | AVGO 4주 regular-session trim 계획 통과 |

## 산출물

- Report: `wiki/current-runs/daily/2026-06-06-0331-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-06-0331-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-06-0331-hourly-autopilot.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-06-0331-hourly-autopilot-post-trade.json`

## 지표 설명

- `sell_candidate_diagnostics`: 보유 포지션 중 trim/exit 재점검이 필요한 상위 후보와 metric gap 사유를 남기는 audit trail이다.
- `pass_after_runtime_reconciliation`: scheduler stale cleanup artifact의 write timing 때문에 남은 것처럼 보인 open order를 runtime Alpaca MCP read-only reconciliation로 실제 상태에 맞게 정정했다는 뜻이다.
- `same-day duplicate discipline`: 같은 정규장 세션에서 이미 submit 또는 fill된 동일 symbol/side buy를 반복 학습 주문으로 재사용하지 않는 규칙이다.
- `validation per-order cap`: `paper_validation_execution.validation_order_sizing.max_validation_notional_pct_per_order`에 따라 계좌 가치 대비 과도한 1주 benchmark fallback 매수는 막는다.
