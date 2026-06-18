# 2026-06-19-0451-hourly-autopilot scheduled paper autopilot

## 요약

`0451` scheduled hourly-autopilot은 scheduler-owned stale cleanup/core/research preflight를 source-of-record로 사용했다. 이번 cycle의 preflight clock은 `2026-06-18T15:51:11.04838424-04:00`이며 account `ACTIVE`, positions `32`, open orders `0`, watchlists `0`, 그리고 broad universe `62`개에 대한 fresh IEX quote rows가 모두 20분 이내라 Alpaca core hard gate를 PASS 처리했다. research tiered gate도 `SEC EDGAR`, `FRED`, `Yahoo Finance`가 `3/3` usable/pass confirmation을 유지해 strict submit threshold를 충족했고, `Alpha Vantage`는 `NEWS_SENTIMENT` `empty_response`, `Firecrawl`은 credits failure `unknown` gap으로만 남았다.

sell-first 재평가에서는 `SO`가 source-of-record quote `93.08/93.10`, spread `0.0215%`로 policy cap `0.50%` 이내를 유지했지만 repeated weak-review trim narrative를 orderable sell로 승격할 decision-grade expected-excess/replacement margin 수치가 이번 cycle에도 비어 있어 `sell_metric_gap`에 막혔다. `AVGO`는 quote `411.72/412.77`, spread `0.2547%` pass와 ai_semiconductor de-risking 맥락이 남아 있어도 held qty가 `1주`뿐이라 trim 후 `keep_minimum_remaining_qty=1`을 만족할 수 없어 `minimum_remaining_qty`에서 막혔다. buy fallback에서는 `AAPL/BAC/WMT/NVDA/QQQ/SPY`가 모두 quote/spread/core 관점에서는 executable이지만 `review_backlog_pending_1d_count=17`가 YAML stop threshold `12`를 넘어 신규 validation buy path를 닫고 있다. 결과적으로 이번 cycle은 hard gates pass 상태의 submit-mode no-op이며, broad labels가 아니라 `sell_metric_gap -> minimum_remaining_qty -> review_backlog_throttle` 순서의 exact blockers를 기록한다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env` 기준 `ALPACA_PAPER_TRADE=true` |
| Market clock | PASS | scheduler-owned Alpaca clock `2026-06-18T15:51:11.04838424-04:00`, regular market open |
| Stale order lifecycle | PASS | stale cleanup status `pass`; initial/remaining open orders 모두 `0` |
| Alpaca core MCP | PASS | scheduler core preflight hard gate `pass`, quote rows fresh |
| Research MCP strict | PASS | positive research provider `sec-edgar`, `fred`, `yahoo-finance` = `3/3` |
| Universe strict | PASS | broad metadata universe `62`개, SPY/QQQ 포함 |
| Review backlog throttle | BUY BLOCK ONLY | `pending_1d=17`, `pending_5d=23`, `pending_20d=15`; stop threshold `12` 초과 |
| Quote/spread | PASS for shortlisted symbols | `SO/AVGO/AAPL/BAC/WMT/NVDA/QQQ/SPY` 모두 spread cap 이내 |
| Risk plan | PASS with expected no-submit warning | `check-risk-policy.py --json`는 `orders=[]` no-submit plan을 통과 |
| Final submit path | NO SUBMIT | `SO=sell_metric_gap`, `AVGO=minimum_remaining_qty`, buy fallback=`review_backlog_throttle` |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| SO | blocked_sell_metric_gap | 0.0215% | trim narrative는 유지되지만 decision-grade expected-excess/replacement margin 공백 |
| AVGO | blocked_minimum_remaining_qty | 0.2547% | 잔여 1주만 남아 non-exit trim 후 minimum remaining qty 1주 유지 불가 |
| AAPL | blocked_review_backlog_throttle | 0.0168% | 신규 add는 buy-only backlog throttle로 차단 |
| BAC | blocked_review_backlog_throttle | 0.0178% | 신규 add는 buy-only backlog throttle로 차단 |
| WMT | blocked_review_backlog_throttle | 0.1881% | quote/spread는 pass지만 신규 add는 buy-only backlog throttle로 차단 |
| NVDA | blocked_review_backlog_and_same_theme_warning | 0.0237% | buy-only backlog throttle와 same-theme warning context 중첩 |
| QQQ | blocked_floor_cap_and_review_backlog | 0.0216% | 1주 ask `740.99 USD`가 validation floor cap 약 `508.76 USD`를 초과 |
| SPY | blocked_floor_cap_and_review_backlog | 0.0027% | 1주 ask `747.79 USD`가 validation floor cap 약 `508.76 USD`를 초과 |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| SO | watch | `sell_metric_gap` | repeated weak-review trim narrative는 유지되지만 decision-grade metric 공백 |
| AVGO | watch | `minimum_remaining_qty` | ai_semiconductor de-risking 맥락은 남아도 잔여 1주라 trim 실행 불가 |
| AAPL | hold | `sell_trigger_none` | active trim trigger 없음 |

## 주문/체결

- Planned orders: 0
- Submitted orders: 0
- `place_stock_order` 호출: 없음
- Source-of-record same-day fills: `RGTI` sell fill stack은 계속 보이지만 `0451` cycle 신규 submit은 없다.
- Post-trade continuity snapshot: account `ACTIVE`, cash `28,610.97 USD`, portfolio value `101,751.72 USD`, buying power `303,935.44 USD`, open orders `0`, positions `32`, `RGTI position 없음`, `SO qty=6`, `AVGO qty=1`

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | broad universe `62` symbols |
| `check-mcp-coverage.py --strict --json` | PASS | positive research `sec-edgar`, `fred`, `yahoo-finance`; Alpha empty-response gap only |
| `check-risk-policy.py --json` | PASS | `orders=[]` no-submit plan |

## 산출물

- Report: `wiki/current-runs/daily/2026-06-19-0451-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-19-0451-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-19-0451-hourly-autopilot.json`
- Runtime gate evaluation: `wiki/evidence-store/sources/2026-06-19-0451-hourly-autopilot-runtime-gate-evaluation.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-19-0451-hourly-autopilot-post-trade.json`

## 지표 설명

- `sell_metric_gap`: broad trim narrative만으로는 submit할 수 없고, `risk_trim_policy.sell_candidate_diagnostics.metric_policy`가 요구하는 decision-grade expected-excess/replacement margin 또는 explicit metric 근거가 필요하다.
- `minimum_remaining_qty`: `risk_trim_policy.active_trim_triggers.keep_minimum_remaining_qty=1` 때문에 held qty `1` 종목은 별도 exit trigger 없이 trim 경로로는 더 줄일 수 없다.
- `review_backlog_throttle`: `paper_validation_execution.validation_order_sizing.review_backlog_throttle`는 신규 buy만 줄이거나 중단한다. 이번 cycle에서는 `pending_1d=17`로 stop threshold `12`를 넘겨 buy fallback 전체를 닫았다.
- `tiered MCP strict`: `alpha-vantage`와 `firecrawl`는 gap이 남았지만 non-core tiered policy상 `sec-edgar/fred/yahoo-finance` 3-provider positive confirmation으로 submit gate 자체는 유지됐다.
