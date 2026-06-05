# 2026-06-06-0411-hourly-autopilot scheduled paper autopilot

## 요약

정규장 scheduled hourly autopilot을 실행했다. `.env`의 `ALPACA_PAPER_TRADE=true` 요구를 확인했고, scheduler-owned `0411` stale cleanup/core/research preflight를 우선 사용했다. stale cleanup은 open order 0건으로 종료됐고, core preflight hard gate도 `pass`였다. runtime Alpaca MCP는 `get_clock`, `get_account_info`, `get_orders(status=open)`, `get_orders(status=all, after=2026-06-05T04:00:00Z)`, `get_asset(INTC)`, `place_stock_order`, `get_order_by_client_id`, `get_order_by_id`가 부분적으로 성공했다. `get_all_positions`와 일부 post-submit `get_orders`/quote refresh는 tool layer에서 cancelled 되었지만, scheduler-owned core preflight와 direct order lookup이 있어 reconciliation 근거는 유지했다.

이번 run은 workflow 지시대로 sell/trim을 먼저 평가했다. `AVGO`는 직전 `0331` cycle에서 이미 4주 trim이 filled 되어 same-day duplicate sell discipline에 걸렸고, `SO`는 decision-grade metric gap 때문에 risk-reducing trim으로 승격되지 못했다. buy fallback에서는 `SPY/QQQ`가 여전히 1주 ask 기준 validation per-order cap을 초과했고, `AAPL/BAC/NVDA/AMZN/SO/NKE/NEE/WMT/COP/JPM`은 same-day duplicate 또는 기존 실행 이력 때문에 신규 buy 우선순위에서 제외됐다. 반면 `INTC`는 same-day duplicate/open-order conflict가 없고, 2026-06-05 portfolio review가 2026-05-28 validation fill cohort를 5D 기준 `약함`으로 정리했으며, Yahoo research preflight도 Broadcom 실적 이후 semiconductor sector sell-off headline을 남겼다. 이에 따라 `INTC` 1주 보유를 risk-reducing lifecycle exit으로 day limit sell 제출했고, immediate reconciliation 기준 `status=new` open order로 기록했다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env`의 `ALPACA_PAPER_TRADE=true` 확인 |
| Market clock pre-submit | PASS | runtime `get_clock` `2026-06-05T15:15:21.347258226-04:00`, market open |
| Stale order lifecycle | PASS | scheduler cleanup artifact 기준 open order 0건 |
| Alpaca core MCP | PASS | scheduler-owned core preflight hard gate pass, runtime clock/account/orders/order lookup 교차 확인 |
| Research MCP | PASS tiered | SEC EDGAR/FRED/Firecrawl/Yahoo positive; Alpha Vantage `provider_error` throttle gap |
| Universe strict | PASS | metadata universe 62개, SPY/QQQ 포함 |
| Quote/spread | PASS for planned order | scheduler quote `INTC` `99.93/99.96`, spread `0.0300%`, quote age `3.8`분 |
| Risk plan | PASS | `check-risk-policy.py --json` PASS |
| Final submit path | PASS | `hourly-20260606-0411-sell-intc` created; immediate reconciliation `status=new` |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| INTC | submit_sell_exit | 0.0300% | 2026-05-28 validation fill 5D review `약함`, SPY 대비 underperformance, same-day duplicate 없음, 1주 full exit 가능 |
| AVGO | watch_same_day_sell | 0.0594% | 직전 0331 cycle에서 이미 4주 trim이 filled 되어 이번 cycle 동일 side 재진입은 duplicate discipline에 막힘 |
| SPY | watch_notional_cap | 0.0027% | benchmark fallback은 유효했지만 1주 ask가 validation per-order cap을 초과 |
| QQQ | watch_notional_cap | 0.0085% | benchmark fallback은 유효했지만 1주 ask가 validation per-order cap을 초과 |
| SO | watch_review_weak | 0.0215% | trim decision-grade metric과 replacement margin이 부족 |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| INTC | sell_submit | active | 5D validation review `약함`, SPY 대비 약 -4.10%p underperformance, same-day duplicate 없음, full-exit 1주 가능 |
| AVGO | watch | same_day_duplicate_symbol_side | 0331 cycle에서 이미 same-day trim 4주가 체결돼 0411 cycle에서는 추가 trim을 내지 않음 |
| SO | watch | decision_grade_metric_gap | weak-to-neutral review 누적은 있지만 trim을 정당화할 replacement margin과 decision-grade metric이 부족 |

## 주문 제출과 reconciliation

- Planned order: `INTC` sell 1 @ `99.93` day limit
- Planned client order id: `hourly-20260606-0411-sell-intc`
- Pre-submit gate summary: paper mode `true`, market clock `2026-06-05T15:15:21.347258226-04:00`, order plan path `wiki/trade-ledger/orders/2026-06-06-0411-hourly-autopilot.json`, universe strict `PASS`, MCP strict `PASS`, risk `PASS`, INTC quote freshness `3.8`분 및 spread `PASS`, order shape `sell 1 share / limit / day / stock`, duplicate/open-order check `PASS`, source refs는 `0411` stale cleanup/core/research preflight와 review/thesis artifacts
- Submit result: `place_stock_order`가 `hourly-20260606-0411-sell-intc`를 Alpaca order id `3cb070b3-08ed-461d-854d-8fa63cf9d441`로 생성했다.
- Reconciliation: `get_order_by_client_id`와 `get_order_by_id`가 모두 동일 주문을 `status=new`, `filled_qty=0`, `limit_price=99.93`로 재확인했다. symbol-filtered `get_orders` refresh는 tool layer에서 cancelled 되었지만, direct order lookup 기준 현재 open/new order 1건으로 기록한다. post-submit `get_account_info`는 portfolio value `97,970.99 USD`, cash `29,847.88 USD`, buying power `244,265.17 USD`, long market value `68,123.11 USD`를 기록했다. `get_all_positions` refresh는 cancelled 되어 positions는 latest confirmed scheduler preflight 기준 `34` positions, `INTC`는 아직 `1주 @ 116.79`로 유지 기록한다.

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | 62 symbols, SPY/QQQ 포함, final candidates 3개 |
| `check-mcp-coverage.py --strict --json` | PASS | Alpaca core pass, positive research 4개, Alpha `provider_error` throttle gap only |
| `check-risk-policy.py --json` | PASS | INTC 1주 regular-session validation exit 계획 통과 |

## 산출물

- Report: `wiki/current-runs/daily/2026-06-06-0411-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-06-0411-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-06-0411-hourly-autopilot.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-06-0411-hourly-autopilot-post-trade.json`

## 지표 설명

- `sell_candidate_diagnostics`: 보유 포지션 중 trim/exit 재점검이 필요한 상위 후보와 metric gap 사유를 남기는 audit trail이다.
- `provider_error throttle gap`: Alpha Vantage가 1시간 one-call throttle 정책에 걸려 이번 cycle에서는 추가 호출을 시도하지 않았다는 뜻이다.
- `same-day duplicate discipline`: 같은 정규장 세션에서 이미 submit 또는 fill된 동일 symbol/side buy 또는 sell을 반복 학습 주문으로 재사용하지 않는 규칙이다.
- `validation per-order cap`: `paper_validation_execution.validation_order_sizing.max_validation_notional_pct_per_order`에 따라 과도한 1주 benchmark fallback 매수는 막는다.
