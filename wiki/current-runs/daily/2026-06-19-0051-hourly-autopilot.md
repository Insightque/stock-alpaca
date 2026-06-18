# 2026-06-19-0051-hourly-autopilot scheduled paper autopilot

## 요약

`0051` scheduled hourly-autopilot은 scheduler-owned stale cleanup/core/research preflight를 source-of-record로 사용했고, live Alpaca continuity `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_order_by_client_id/get_watchlists/get_stock_latest_quote/get_asset`로 submit-boundary 상태를 재확인했다. Paper mode, regular market open, universe strict, tiered MCP strict, risk validator는 모두 PASS다. `Alpha Vantage`는 one-call-per-hour throttle 기반 `provider_error`, `Firecrawl`은 credits failure `unknown` gap only로 남았지만 `SEC EDGAR`, `FRED`, `Yahoo Finance`가 `3/3` usable/pass confirmation을 유지해 strict MCP submit gate는 계속 열려 있다.

이번 cycle의 first blocker는 시장 약세가 아니라 기존 open sell이다. `RGTI`는 live quote `20.52/20.54`, spread `0.0974%`, active tradable NASDAQ stock, held qty `12`, `qty_available=9`로 trim 조건 자체는 유지하지만 `hourly-20260619-0031-sell-rgti` 3주 sell이 아직 `status=new` open order로 남아 있어 same symbol/side `open_order_check`가 추가 trim을 막는다. `SO`는 quote/spread는 pass지만 decision-grade trim metric gap이 남아 있고, `AAPL/BAC/WMT/NVDA/QQQ/SPY` buy fallback은 `review_backlog_pending_1d_count=17`이 YAML stop threshold `12`를 초과해 계속 닫혀 있다. 따라서 이번 cycle은 새 주문 없이 open-order reconciliation 중심으로 종료한다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env` 기준 `ALPACA_PAPER_TRADE=true` |
| Market clock | PASS | live `get_clock` `2026-06-18T11:53:33.991800538-04:00`, regular market open |
| Stale order lifecycle | PASS with blocker note | scheduler cleanup 자체는 pass지만 remaining open orders에 `hourly-20260619-0031-sell-rgti` 1건이 남아 있다 |
| Alpaca core MCP | PASS | scheduler core preflight hard gate `pass`, live continuity account `ACTIVE`, positions `33`, open orders `1` |
| Research MCP strict | PASS | usable/pass research provider `sec-edgar`, `fred`, `yahoo-finance` = `3/3` |
| Universe strict | PASS | broad metadata universe `62`개, SPY/QQQ 포함 |
| Review backlog throttle | FAIL for buys only | `pending_1d_count=17` > `stop_new_buys_at_pending_1d=12` |
| Quote freshness | PASS | live quotes `2026-06-18T15:53:35Z~15:53:36Z`, decision time 기준 사실상 0분 |
| Spread | MIXED PASS | `RGTI 0.0974%`, `SO 0.0212%`, `AAPL 0.0101%`, `BAC 0.0177%`, `WMT 0.0170%`, `NVDA 0.0622%`, `QQQ 0.0257%`, `SPY 0.0094%` |
| Risk plan | PASS | `check-risk-policy.py --json` 기준 현재 포지션 포함, orders `0`, open order lifecycle 기록 포함 |
| Final submit path | BLOCK | sell-first `RGTI`가 same symbol/side `open_order_check`, `SO`가 `sell_metric_gap`, buy fallback은 `review_backlog_throttle` |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| RGTI | blocked_open_order_check | 0.0974% | speculative trim rationale는 유지되지만 기존 `0031` open sell 3주가 아직 살아 있다 |
| SO | blocked_sell_metric_gap | 0.0212% | quote/spread는 pass지만 trim decision-grade expected-excess/replacement margin 공백 |
| AAPL | blocked_review_backlog_throttle_buy_only | 0.0101% | sell trigger는 없고 buy fallback은 backlog throttle에 막힘 |
| BAC | blocked_review_backlog_throttle_buy_only | 0.0177% | financials diversifier fallback이지만 buy-only backlog throttle 우선 |
| WMT | blocked_review_backlog_throttle_buy_only | 0.0170% | defensive fallback이지만 buy slot이 0 |
| NVDA | blocked_review_backlog_and_same_theme_warning | 0.0622% | ai_semiconductor warning context와 buy backlog가 겹침 |
| QQQ | blocked_floor_cap_and_review_backlog | 0.0257% | 1주 ask가 validation floor per-order cap을 초과하고 buy backlog도 남음 |
| SPY | blocked_floor_cap_and_review_backlog | 0.0094% | 1주 ask가 validation floor per-order cap을 초과하고 buy backlog도 남음 |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| RGTI | watch | `open_order_check` | fresh open sell `hourly-20260619-0031-sell-rgti`가 남아 same symbol/side trim 재제출 불가 |
| SO | watch | `sell_metric_gap` | repeated weak-review defensive sleeve trim 후보지만 decision-grade metric 공백 유지 |
| AAPL | hold | `sell_trigger_none` | existing mega-cap quality holding이지만 active trim trigger 부재 |

## 주문/체결

- Planned orders: 0
- Submitted orders: 0
- `place_stock_order` 호출: 없음
- Pre-submit gate summary: 이번 cycle에는 최종 hard gate를 모두 통과한 신규 주문이 없었다. paper mode `PASS`, market clock `2026-06-18T11:53:33.991800538-04:00`, order plan `wiki/trade-ledger/orders/2026-06-19-0051-hourly-autopilot.json`, universe strict `PASS`, MCP strict `PASS`, risk validator `PASS`, quote freshness `PASS`, spread `PASS`, order shape는 whole-share/day-limit stock-or-ETF only로 유지됐다. 다만 duplicate/open-order check에서 `RGTI` 기존 open sell이 same symbol/side 추가 trim을 막았고, buy fallback은 review backlog throttle에 걸렸다. source refs는 scheduler-owned `0051` stale/core/research preflight와 runtime gate evaluation, review/ticker artifacts다.
- Post-trade reconciliation: live `get_order_by_client_id(hourly-20260619-0031-sell-rgti)` 기준 주문은 여전히 `status=new`, `filled_qty=0`, `filled_avg_price=null`이다. live `get_orders(status=open)` 기준 open orders `1`, live `get_all_positions` 기준 positions `33`, `RGTI qty=12`, `qty_available=9`, live `get_account_info` 기준 account `ACTIVE`, cash `28,363.52 USD`, portfolio value `101,526.24 USD`, buying power `303,023.93 USD`, live `get_watchlists` 기준 watchlists `0`였다.

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | `62` symbols, shortlist `10`, final candidates `6` |
| `check-mcp-coverage.py --strict --json` | PASS | positive research `sec-edgar`, `fred`, `yahoo-finance` |
| `check-risk-policy.py --json` | PASS | `orders is empty` warning only, open order lifecycle 기록 포함 |

## 산출물

- Report: `wiki/current-runs/daily/2026-06-19-0051-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-19-0051-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-19-0051-hourly-autopilot.json`
- Runtime gate evaluation: `wiki/evidence-store/sources/2026-06-19-0051-hourly-autopilot-runtime-gate-evaluation.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-19-0051-hourly-autopilot-post-trade.json`

## 지표 설명

- `open_order_check`: stale cleanup 대상은 아니어도 fresh same symbol/side open order가 남아 있으면 추가 주문을 막는다.
- `review_backlog_throttle`: `paper_validation_execution.validation_order_sizing.review_backlog_throttle`는 신규 buy만 줄이거나 중단한다. sell/trim 진단은 별도로 계속 평가한다.
- `sell_candidate_diagnostics`: 실행하지 않은 trim 후보도 metric 값 또는 explicit gap reason을 남겨 다음 analyst review와 policy learning에 연결한다.
