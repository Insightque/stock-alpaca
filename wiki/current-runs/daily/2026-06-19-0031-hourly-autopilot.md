# 2026-06-19-0031-hourly-autopilot scheduled paper autopilot

## 요약

`0031` scheduled hourly-autopilot은 scheduler-owned stale cleanup/core/research preflight를 source-of-record로 사용했고, stale lifecycle PASS, Alpaca core PASS, universe strict PASS, research strict PASS 경로를 유지했다. `Alpha Vantage`는 one-call-per-hour throttle로 `provider_error`, `Firecrawl`은 credits failure로 남았지만 `SEC EDGAR`, `FRED`, `Yahoo Finance`가 `3/3` usable/pass confirmation을 제공해 strict MCP submit gate는 열려 있었다.

buy side는 `review_backlog_pending_1d_count=17`이 YAML stop threshold `12`를 넘어 신규 validation buy가 계속 막혔다. sell-first 재평가에서는 `RGTI`가 scheduler preflight quote `20.61/20.62`, spread `0.0485%`, open orders `0`, active tradable NASDAQ stock, speculative loss-control trim trigger를 동시에 만족해 이번 cycle의 최소 learning order로 승격됐다. `SO`는 quote/spread는 pass지만 decision-grade trim metric 공백이 남았고, broad buy fallback 후보 `AAPL/BAC/WMT/NVDA/QQQ/SPY`는 모두 buy-only backlog throttle에 묶였다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env` 기준 `ALPACA_PAPER_TRADE=true` |
| Market clock | PASS | live `get_clock` `2026-06-18T11:31:09.79513893-04:00`, regular market open |
| Stale order lifecycle | PASS | `0031` stale cleanup artifact 기준 stale candidates `0`, remaining open orders `0` |
| Alpaca core MCP | PASS | scheduler core preflight hard gate `pass`, live continuity account `ACTIVE`, open orders `0` before submit |
| Research MCP strict | PASS | usable/pass research provider `sec-edgar`, `fred`, `yahoo-finance` = `3/3` |
| Universe strict | PASS | broad metadata universe `62`개, SPY/QQQ 포함 |
| Review backlog throttle | FAIL for buys only | `pending_1d_count=17` > `stop_new_buys_at_pending_1d=12` |
| Quote freshness | PASS | scheduler quote timestamp `2026-06-18T15:31:29.674846063Z`, decision time 기준 약 `4.0`분 |
| Spread | MIXED | `RGTI 0.0485%`, `SO 0.0213%` PASS, buy fallback은 backlog throttle로 미진입 |
| Risk plan | PASS | `RGTI sell 3 @ 20.61 USD` trim plan 작성 |
| Final submit path | PASS | sell-first `RGTI trim` candidate가 strict gates를 모두 통과했고 buy-only throttle과 분리된다 |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| RGTI | executable_sell_trim | 0.0485% | speculative loss-control trim trigger, negative expected excess, open-order clean |
| SO | blocked_sell_metric_gap | 0.0213% | quote/spread는 pass지만 trim decision-grade expected-excess/replacement margin 공백 |
| AAPL | blocked_review_backlog_throttle | 0.0101% | buy-only backlog throttle로 신규 add 차단 |
| BAC | blocked_review_backlog_throttle | 0.0177% | buy-only backlog throttle로 신규 add 차단 |
| WMT | blocked_review_backlog_throttle | 0.0256% | buy-only backlog throttle로 신규 add 차단 |
| NVDA | blocked_review_backlog_and_same_theme_warning | 0.0287% | buy-only backlog throttle와 ai_semiconductor warning context가 겹침 |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| RGTI | trim | pass | residual speculative sleeve staged de-risking과 strict research recovery가 동시에 확인돼 이번 cycle sell-first learning order |
| SO | watch | `sell_metric_gap` | quote/spread는 pass지만 decision-grade trim metric 공백이 남음 |
| AAPL | hold | `sell_trigger_none` | active trim trigger 없음 |

## 주문/체결

- Planned orders: 1
- Submitted orders: 1
- Filled orders: 없음. `RGTI sell 3 @ limit 20.61 USD`는 immediate reconciliation 기준 아직 `status=new` open order다.
- Post-trade reconciliation: `get_order_by_client_id` 기준 `status=new`, `filled_qty=0`, `get_orders(status=open)` 기준 open orders `1`, `get_all_positions` 기준 positions `33`, `RGTI qty=12`, `qty_available=9`, `get_account_info` 기준 cash `28,363.52 USD`, portfolio value `101,364.57 USD`, buying power `302,650.16 USD`, `get_watchlists` 기준 watchlists `0`

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | `62` symbols, shortlist `10`, final candidates `6` |
| `check-mcp-coverage.py --strict --json` | PASS | positive research `sec-edgar`, `fred`, `yahoo-finance` |
| `check-risk-policy.py --json` | PASS | `RGTI sell 3 @ 20.61 USD` trim plan |

## 산출물

- Report: `wiki/current-runs/daily/2026-06-19-0031-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-19-0031-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-19-0031-hourly-autopilot.json`
- Runtime gate evaluation: `wiki/evidence-store/sources/2026-06-19-0031-hourly-autopilot-runtime-gate-evaluation.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-19-0031-hourly-autopilot-post-trade.json`

## 지표 설명

- `executable_sell_trim`: buy-only throttle과 무관하게 sell-first risk-reducing trim이 strict gate를 모두 통과한 상태다.
- `review_backlog_throttle`: `paper_validation_execution.validation_order_sizing.review_backlog_throttle`는 신규 buy만 줄이거나 중단한다. sell/trim/exit 진단은 별도로 계속 평가한다.
- `sell_candidate_diagnostics`: 실행하지 않은 trim 후보도 metric 값 또는 explicit gap reason을 남겨 다음 analyst review와 policy learning에 연결한다.
