# 2026-06-06-0351-hourly-autopilot scheduled paper autopilot

## 요약

정규장 scheduled hourly autopilot을 실행했다. `.env`의 `ALPACA_PAPER_TRADE=true` 요구를 확인했고, scheduler-owned `0351` stale cleanup/core/research preflight를 우선 사용했다. stale cleanup은 open order 0건으로 종료됐고, core preflight hard gate도 `pass`였다. runtime Alpaca MCP는 `get_clock`, `place_stock_order`, `get_order_by_client_id`, `get_all_positions`, `get_account_info`가 성공했고, post-submit `get_orders(status=open, symbols=JPM)`만 tool layer에서 cancelled 되었다.

이번 run은 workflow 지시대로 sell/trim을 먼저 평가했다. `AVGO`는 직전 `0331` cycle에서 이미 same-day trim 4주가 filled 되어 이번 cycle에서는 duplicate symbol/side discipline에 걸렸고, `SO`와 `TSLA`는 각각 decision-grade metric gap과 held-quantity gate 때문에 risk-reducing sell로 승격되지 못했다. buy fallback에서는 same-day duplicate 때문에 `BAC/WMT/FCX/PLTR/AAPL/V/NVDA/SLB/COP/AMZN/PFE/SO` 재진입이 막혔고, `SPY/QQQ`는 1주 ask가 validation per-order cap을 초과했다. `JPM`은 0351 research shortlist 포함, four-provider positive research confirmation, active/tradable, quote `311.98/312.04`, spread `0.0192%`, review backlog throttle pass, invested ratio 약 `69.3%` 조건으로 financials diversifier floor-size validation buy 1주를 제출했고 `311.81 USD`에 즉시 체결됐다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env`의 `ALPACA_PAPER_TRADE=true` 확인 |
| Market clock pre-submit | PASS | runtime `get_clock` `2026-06-05T14:54:03.885757711-04:00`, market open |
| Stale order lifecycle | PASS | scheduler cleanup artifact 기준 open order 0건 |
| Alpaca core MCP | PASS | scheduler-owned core preflight hard gate pass, runtime clock/submit/reconciliation 교차 확인 |
| Research MCP | PASS tiered | SEC EDGAR/FRED/Firecrawl/Yahoo positive; Alpha Vantage `provider_error` throttle gap |
| Universe strict | PASS | metadata universe 62개, SPY/QQQ 포함 |
| Quote/spread | PASS for planned order | scheduler quote `JPM` `2026-06-05T18:51:29.312221244Z`, spread `0.0192%` |
| Risk plan | PASS | `check-risk-policy.py --json` PASS |
| Final submit path | PASS | `hourly-20260606-0351-buy-jpm` filled |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| JPM | submit_buy | 0.0192% | same-day duplicate/open-order conflict 없음, financials diversifier, four-provider research confirmation, validation floor notional 적합 |
| AVGO | watch_same_day_sell | 0.0232% | 직전 0331 cycle에서 이미 4주 trim이 filled 되어 이번 cycle 동일 side 재진입은 duplicate discipline에 막힘 |
| SPY | watch_notional_cap | 0.0054% | benchmark fallback은 유효했지만 1주 ask가 validation per-order cap을 초과 |
| QQQ | watch_notional_cap | 0.0071% | benchmark fallback은 유효했지만 1주 ask가 validation per-order cap을 초과 |
| SO | watch_review_weak | n/a | trim decision-grade metric이 부족 |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| AVGO | watch | same_day_duplicate_symbol_side | 0331 cycle에서 이미 same-day trim 4주가 체결돼 0351 cycle에서는 추가 trim을 내지 않음 |
| SO | watch | decision_grade_metric_gap | weak-to-neutral review 누적은 있지만 trim을 정당화할 replacement margin과 decision-grade metric이 부족 |
| TSLA | watch | held_quantity_and_metric_gap | drawdown은 크지만 1주 보유라 trim minimum-remaining gate를 충족하기 어렵고 metric도 비어 있음 |

## 주문 제출과 reconciliation

- Planned order: `JPM` buy 1 @ `312.04` day limit
- Planned client order id: `hourly-20260606-0351-buy-jpm`
- Pre-submit gate summary: paper mode `true`, market clock `2026-06-05T14:54:03.885757711-04:00`, order plan path `wiki/trade-ledger/orders/2026-06-06-0351-hourly-autopilot.json`, universe strict `PASS`, MCP strict `PASS`, risk `PASS`, JPM quote freshness `2.6`분 및 spread `PASS`, order shape `buy 1 share / limit / day / stock`, duplicate/open-order check `PASS`, source refs는 `0351` stale cleanup/core/research preflight와 review/thesis artifacts
- Submit result: `place_stock_order`가 `hourly-20260606-0351-buy-jpm`를 Alpaca order id `dc6e7545-bf7d-47a1-a257-fc5c82866680`로 생성했고, `get_order_by_client_id` 기준 `2026-06-05T19:02:33.577640965Z`에 `311.81 USD`로 filled 됐다.
- Reconciliation: direct `get_orders(status=open, symbols=JPM)`는 cancelled 되었지만 `get_order_by_client_id`가 `status=filled`, `filled_qty=1`, `filled_avg_price=311.81`을 반환했고, post-trade `get_all_positions`는 `JPM` 신규 보유 `1주 @ 311.81`와 position count `34`를 확인했다. post-trade `get_account_info`는 portfolio value `98,378.18 USD`, cash `29,847.88 USD`, buying power `244,983.06 USD`, long market value `68,530.30 USD`를 기록했다.

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | 62 symbols, SPY/QQQ 포함, final candidates 3개 |
| `check-mcp-coverage.py --strict --json` | PASS | Alpaca core pass, positive research 4개, Alpha `provider_error` throttle gap only |
| `check-risk-policy.py --json` | PASS | JPM 1주 regular-session validation buy 계획 통과 |

## 산출물

- Report: `wiki/current-runs/daily/2026-06-06-0351-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-06-0351-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-06-0351-hourly-autopilot.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-06-0351-hourly-autopilot-post-trade.json`

## 지표 설명

- `sell_candidate_diagnostics`: 보유 포지션 중 trim/exit 재점검이 필요한 상위 후보와 metric gap 사유를 남기는 audit trail이다.
- `provider_error throttle gap`: Alpha Vantage가 1시간 one-call throttle 정책에 걸려 이번 cycle에서는 추가 호출을 시도하지 않았다는 뜻이다.
- `same-day duplicate discipline`: 같은 정규장 세션에서 이미 submit 또는 fill된 동일 symbol/side buy 또는 sell을 반복 학습 주문으로 재사용하지 않는 규칙이다.
- `validation per-order cap`: `paper_validation_execution.validation_order_sizing.max_validation_notional_pct_per_order`에 따라 과도한 1주 benchmark fallback 매수는 막는다.
