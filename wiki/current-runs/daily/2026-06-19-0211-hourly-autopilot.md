# 2026-06-19-0211-hourly-autopilot scheduled paper autopilot

## 요약

`0211` scheduled hourly-autopilot은 scheduler-owned stale cleanup/core/research preflight를 source-of-record로 사용했고, `Alpha Vantage`는 one-call-per-hour throttle 기반 `provider_error`, `Firecrawl`은 credits failure `unknown` gap으로 남았지만 `SEC EDGAR`, `FRED`, `Yahoo Finance`가 `3/3` usable/pass confirmation을 유지해 strict MCP submit gate가 열려 있었다.

이번 cycle의 핵심 변화는 preflight freshness 범위 안에서 sell-first continuation이 실제 체결까지 이어졌다는 점이다. preflight 기준 regular market open, account `ACTIVE`, open orders `0`, watchlists `0`, `RGTI` asset active/tradable, quote `20.61/20.62` spread `0.0485%`를 재확인했고 buy side는 `review_backlog_pending_1d_count=17`로 YAML stop threshold `12`를 넘어 계속 닫혀 있으므로 sell-first directive에 따라 `RGTI` 1주 trim을 이번 cycle 최소 learning order로 제출했다. follow-up reconciliation 기준 신규 주문 `client_order_id=hourly-20260619-0211-sell-rgti`는 `2026-06-18T17:19:16.190511737Z`에 `filled_avg_price=20.72 USD`로 전량 체결됐고 `RGTI qty=6`, `qty_available=6`로 감소했다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env` 기준 `ALPACA_PAPER_TRADE=true` |
| Market clock | PASS | scheduler core preflight `2026-06-18T13:11:11.22474378-04:00`, regular market open |
| Stale order lifecycle | PASS | `0211` stale cleanup artifact 기준 stale candidates `0`, remaining open orders `0` |
| Alpaca core MCP | PASS | scheduler core preflight hard gate `pass`, account `ACTIVE`, positions `33`, open orders `0` |
| Research MCP strict | PASS | usable/pass research provider `sec-edgar`, `fred`, `yahoo-finance` = `3/3` |
| Universe strict | PASS | broad metadata universe `62`개, SPY/QQQ 포함 |
| Review backlog throttle | FAIL for buys only | `pending_1d_count=17` > `stop_new_buys_at_pending_1d=12` |
| Quote freshness | PASS | preflight quote timestamp `2026-06-18T17:11:27Z` 부근, plan market clock 기준 age `0.0m` |
| Spread | MIXED PASS | `RGTI 0.0485%`, `SO 0.0107%`, `BAC 0.0177%`, `WMT 0.0170%`, `NVDA 0.1189%`, `QQQ 0.0270%`, `SPY 0.0054%`, `AAPL 0.3367%` 모두 hard cap 0.50% 이내 |
| Risk plan | PASS | `RGTI sell 1 @ 20.61 USD` trim plan 작성 및 validator PASS |
| Final submit path | PASS | sell-first `RGTI trim` candidate가 strict gates를 모두 통과했고 buy-only throttle과 분리된다 |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| RGTI | executable_sell_trim | 0.0485% | speculative loss-control trim trigger, negative expected excess, open-order/duplicate blocker 없음 |
| SO | blocked_sell_metric_gap | 0.0107% | quote/spread는 pass지만 trim decision-grade expected-excess/replacement margin 공백 |
| AAPL | blocked_review_backlog_throttle | 0.3367% | buy-only backlog throttle로 신규 add 차단 |
| BAC | blocked_review_backlog_throttle | 0.0177% | buy-only backlog throttle로 신규 add 차단 |
| WMT | blocked_review_backlog_throttle | 0.0170% | buy-only backlog throttle로 신규 add 차단 |
| NVDA | blocked_review_backlog_and_same_theme_warning | 0.1189% | buy-only backlog throttle와 ai_semiconductor warning context가 겹침 |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| RGTI | trim | pass | residual speculative sleeve staged de-risking과 preflight freshness가 동시에 확인돼 이번 cycle sell-first learning order |
| SO | watch | `sell_metric_gap` | quote/spread는 pass지만 decision-grade trim metric 공백이 남음 |
| AAPL | hold | `sell_trigger_none` | active trim trigger 없음 |

## 주문/체결

- Planned orders: 1
- Submitted orders: 1
- Filled orders: `RGTI sell 1 @ limit 20.61 USD`가 follow-up reconciliation 기준 `2026-06-18T17:19:16.190511737Z`에 `filled_avg_price=20.72 USD`로 전량 체결됐다.
- Post-trade reconciliation: `get_order_by_id` 기준 `status=filled`, `filled_qty=1`, `get_orders(status=open)` 기준 open orders `0`, `get_all_positions` 기준 positions `33`, `RGTI qty=6`, `qty_available=6`, `get_account_info` 기준 cash `28,486.53 USD`, portfolio value `101,704.09 USD`, buying power `303,894.75 USD`, `get_watchlists` 기준 watchlists `0`

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict` | PASS | `62` symbols, shortlist `10`, final candidates `6` |
| `check-mcp-coverage.py --strict` | PASS | positive research `sec-edgar`, `fred`, `yahoo-finance` |
| `check-risk-policy.py --json` | PASS | `RGTI sell 1 @ 20.61 USD` trim plan |

## 산출물

- Report: `wiki/current-runs/daily/2026-06-19-0211-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-19-0211-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-19-0211-hourly-autopilot.json`
- Runtime gate evaluation: `wiki/evidence-store/sources/2026-06-19-0211-hourly-autopilot-runtime-gate-evaluation.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-19-0211-hourly-autopilot-post-trade.json`

## 지표 설명

- `executable_sell_trim`: buy-only throttle과 무관하게 sell-first risk-reducing trim이 strict gate를 모두 통과한 상태다.
- `review_backlog_throttle`: `paper_validation_execution.validation_order_sizing.review_backlog_throttle`는 신규 buy만 줄이거나 중단한다. sell/trim/exit 진단은 별도로 계속 평가한다.
- `sell_candidate_diagnostics`: 실행하지 않은 trim 후보도 metric 값 또는 explicit gap reason을 남겨 다음 analyst review와 policy learning에 연결한다.
