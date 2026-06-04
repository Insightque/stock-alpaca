# 2026-06-05-0451-hourly-autopilot scheduled paper autopilot

## 요약

정규장 scheduled hourly autopilot을 실행했다. `.env`의 `ALPACA_PAPER_TRADE=true` 요구를 확인했고, scheduler-owned `0451` stale cleanup/core/research preflight를 우선 사용했다. pre-submit 시점 runtime Alpaca clock `2026-06-04T15:58:12.864955496-04:00` 기준 미국 정규장은 열려 있었고, research preflight는 `sec-edgar`, `fred`, `firecrawl`, `yahoo-finance` 4개 provider가 usable/pass였으며 `alpha-vantage`는 one-call-per-hour throttle 때문에 nonblocking `provider_error` gap으로 남았다.

이번 run은 sell/trim 후보를 먼저 평가했지만 `AVGO`, `SO`, `TSLA`는 여전히 decision-grade metric 또는 held-quantity gate에 막혔다. 같은 ET regular session same-day duplicate 규칙 때문에 `BAC`, `SPY`, `QQQ` 및 오늘 이미 매수된 cohort는 submit 후보에서 제외했고, `PLTR`은 same-symbol open buy 때문에 제외했다. 남는 clean candidate `JNJ`로 1주 validation buy 계획과 strict universe/MCP/risk validator는 모두 통과했다. 다만 실제 `place_stock_order`가 `2026-06-04T20:02:59Z` 즉 `16:02:59 ET`에 기록되어 regular close 이후로 넘어갔고, runtime clock `2026-06-04T16:03:56.934008822-04:00`에서 `is_open=false`를 확인해 해당 order를 즉시 취소했다. 최종적으로 standing order와 fill은 남기지 않았다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env`의 `ALPACA_PAPER_TRADE=true` 확인 |
| Market clock pre-submit | PASS | runtime `get_clock` `2026-06-04T15:58:12.864955496-04:00`, regular market open |
| Market clock post-submit reconciliation | FAIL | runtime `get_clock` `2026-06-04T16:03:56.934008822-04:00`, `is_open=false` |
| Stale order lifecycle | PASS | scheduler cleanup pass, close 이후 open orders 0건 |
| Alpaca core MCP | PASS | scheduler-owned core preflight hard gate pass, runtime `get_clock/get_account_info/get_orders(status=open)/get_asset(JNJ)/get_stock_latest_quote(JNJ)` 보조 확인 |
| Research MCP | PASS tiered | SEC EDGAR/FRED/Firecrawl/Yahoo positive; Alpha Vantage는 `provider_error` nonblocking gap |
| Universe strict | PASS | metadata universe 62개, SPY/QQQ 포함 |
| Quote/spread | PASS for planned order | JNJ runtime quote `2026-06-04T19:56:29.922222282Z`, spread `0.4065%` |
| Risk plan | PASS | JNJ 1주 buy notional `229.25`, cash/ticker/theme/factor/cluster caps 통과 |
| Final execution state | CANCELED | actual submit이 close 이후로 밀려 workflow safety 복구 차원에서 즉시 cancel |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| JNJ | canceled_after_close | 0.4065% | defensive healthcare diversifier로 pre-submit hard gate는 모두 통과했지만 actual submit timestamp가 close 이후로 밀려 즉시 취소했다. |
| PLTR | blocked | 0.0283% | 04:31 cycle buy open order가 pre-submit 시점에 남아 있어 same-symbol buy를 추가할 수 없었다. |
| BAC | blocked | 0.0185% | 같은 ET regular session 15:21 filled buy가 있어 reject_duplicate_symbol_side_same_day 정책에 막혔다. |
| SPY | blocked | 0.0026% | 같은 ET regular session filled buy가 있어 risk policy duplicate-symbol-side 규칙에 막혔다. |
| QQQ | blocked | 0.0040% | 같은 ET regular session buy 이력이 있어 duplicate-symbol-side 규칙에 막혔다. |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| AVGO | watch | decision_grade_metric_gap | AI semiconductor_complex 경고구간과 급락 반전으로 trim 재점검 대상이지만 decision-grade expected-excess와 replacement margin이 비어 있다. |
| SO | watch | decision_grade_metric_gap | defensive/utilities validation review 약세와 rate-sensitive 부담은 있지만 per-symbol decision-grade expected-excess 공백이 남아 있다. |
| TSLA | watch | held_quantity_and_metric_gap | 약한 validation review와 speculative growth 성격은 재점검 대상이지만 1주 보유라 whole-share trim 규칙을 만족시키기 어렵고 metric도 비어 있다. |

## 주문 제출과 reconciliation

- Planned order: `JNJ` buy 1 @ `229.25` day limit
- Alpaca order id: `915838ec-e52b-41c2-9682-fdb7b94dba52`
- Client order id: `hourly-20260605-0451-buy-jnj`
- Pre-submit gate summary: paper mode `true`, market open, universe strict `PASS`, MCP strict `PASS`, risk `PASS`, JNJ quote freshness/spread `PASS`, same-day duplicate/open-order conflict 없음
- `place_stock_order`: Alpaca accepted the order with `status=accepted`, but submit timestamp was `2026-06-04T20:02:59Z` (`16:02:59 ET`) after regular close
- Reconciliation: runtime `get_clock` returned `is_open=false` at `2026-06-04T16:03:56.934008822-04:00`; `cancel_order_by_id` was issued immediately; `get_order_by_id` confirmed `status=canceled`, `canceled_at=2026-06-04T20:04:09.116873884Z`; `get_orders(status=open)` returned `0` open orders. JNJ fill/position 증가는 확인되지 않았다.

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | 62 symbols, SPY/QQQ 포함, final candidates 5개 |
| `check-mcp-coverage.py --strict --json` | PASS | Alpaca core pass, positive research 4개, Alpha `provider_error` gap only |
| `check-risk-policy.py --json` | PASS | JNJ 1주 regular-session day limit buy 계획 통과 |

## 산출물

- Report: `wiki/current-runs/daily/2026-06-05-0451-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-05-0451-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-05-0451-hourly-autopilot.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-05-0451-hourly-autopilot-post-trade.json`

## 지표 설명

- `sell_candidate_diagnostics`: 보유 포지션 중 trim/exit 재점검이 필요한 상위 후보와 metric gap 사유를 남기는 audit trail이다.
- `provider_error`: 이번 cycle의 Alpha Vantage는 one-call-per-hour throttle 때문에 재호출하지 않고 nonblocking gap으로 남겼다.
- `reject_duplicate_symbol_side_same_day`: 같은 ET regular session에서 이미 제출/체결된 동일 symbol/side buy를 새 submit-mode plan에 다시 넣지 않는 risk policy다.
- `market close race`: pre-submit gate는 열려 있었지만 실제 submit RPC가 close 이후에 도착한 경우다. 이 run에서는 safety rule을 복구하기 위해 즉시 cancel로 정리했다.
