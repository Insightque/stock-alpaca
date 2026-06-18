# 2026-06-18-2331-hourly-autopilot scheduled paper autopilot

## 요약

`2331` scheduled hourly-autopilot은 scheduler-owned stale cleanup/core/research preflight를 source-of-record로 재사용했고 stale lifecycle PASS, Alpaca core PASS, universe strict PASS, risk validator PASS를 유지했다. source-of-record account는 `ACTIVE`, cash `28,197.42 USD`, portfolio value `101,318.12 USD`, buying power `302,148.67 USD`, positions `33`, open orders `0`였다.

다만 이번 cycle research preflight는 `SEC EDGAR`, `FRED`만 usable/pass로 남고 `Yahoo Finance`는 `BAC` recommendations timeout, `Alpha Vantage`는 one-call-per-hour throttle `provider_error`, `Firecrawl`은 credits failure로 남아 `check-mcp-coverage.py --strict`가 FAIL했다. sell-first 평가에서는 `RGTI` trim path가 여전히 가장 직접적인 risk-reducing 후보였지만 strict MCP submit gate가 닫혀 있었고, same US-date regular-session `RGTI` sell fill도 이미 존재해 no-submit으로 종료했다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env` 기준 `ALPACA_PAPER_TRADE=true` |
| Market clock | PASS | scheduler core preflight `2026-06-18T10:31:11.104848198-04:00`, regular market open |
| Stale order lifecycle | PASS | `2331` stale cleanup artifact 기준 stale candidates `0`, remaining open orders `0` |
| Alpaca core MCP | PASS | scheduler core preflight hard gate `pass`, account `ACTIVE`, positions `33`, open orders `0` |
| Research MCP strict | FAIL | usable/pass research provider가 `SEC EDGAR`, `FRED` 2개뿐이라 strict submit threshold `3` 미달 |
| Universe strict | PASS | broad metadata universe `62`개, SPY/QQQ 포함 |
| Review backlog throttle | FAIL for buys only | `pending_1d_count=17` > `stop_new_buys_at_pending_1d=12` |
| Quote freshness | PASS | source-of-record quote timestamp `2026-06-18T14:31:28Z` 부근, decision time 기준 약 `6`분 이내 |
| Spread | PASS for top candidates | `RGTI 0.0498%`, `SO 0.0321%`, `AAPL 0.1433%`, `BAC 0.0176%`, `WMT 0.0255%` |
| Risk plan | PASS | `check-risk-policy.py --json` 기준 current positions `33`, `orders=[]` 허용 |
| Final submit path | NO SUBMIT | first blocking gate `mcp_research_confirmations` |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| RGTI | blocked_mcp_tiered_strict | 0.0498% | speculative trim trigger와 음수 expected excess는 유지됐지만 strict research confirmation이 `2/3`라 submit gate 실패 |
| SO | blocked_sell_metric_gap | 0.0321% | quote/spread는 pass지만 trim decision-grade expected-excess/replacement margin 공백 |
| AAPL | blocked_review_backlog_throttle | 0.1433% | mega-cap fallback add 후보지만 buy-side backlog throttle 우선 차단 |
| BAC | blocked_review_backlog_throttle | 0.0176% | financials diversifier fallback이나 buy-side backlog throttle 우선 차단 |
| WMT | blocked_review_backlog_throttle | 0.0255% | defensive fallback이나 pending review backlog가 신규 buy를 차단 |
| NVDA | blocked_review_backlog_and_same_theme_warning | 0.0191% | ai_semiconductor warning band와 pending review backlog 동시 유지 |
| QQQ | blocked_validation_floor_cap | 0.0394% | 1주 ask `735.65 USD`가 validation floor per-order cap 약 `506.59 USD` 초과 |
| SPY | blocked_validation_floor_cap | 0.0054% | 1주 ask `745.21 USD`가 validation floor per-order cap 약 `506.59 USD` 초과 |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| RGTI | watch | `mcp_tiered_strict` | core-only trim path는 유지되지만 current-cycle strict MCP validator가 submit boundary를 막음 |
| SO | watch | `sell_metric_gap` | quote/spread는 pass지만 decision-grade trim metric 공백이 남아 있음 |
| AAPL | hold | `sell_trigger_none` | active trim trigger 없음 |

## 주문/체결

- Planned orders: 0
- Submitted orders: 0
- `place_stock_order` 호출: 없음
- submit 직전까지 최상위 risk-reducing 후보: `RGTI sell 5 @ 20.07 USD` trim path
- no-submit 사유: `check-mcp-coverage.py --strict` FAIL, first blocking gate `mcp_research_confirmations`

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | `62` symbols, shortlist `10`, final candidates `6` |
| `check-mcp-coverage.py --strict --json` | FAIL | positive research `fred`, `sec-edgar`만 usable |
| `check-risk-policy.py --json` | PASS | current positions `33`, `orders=[]` warning only |

## 산출물

- Report: `wiki/current-runs/daily/2026-06-18-2331-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-18-2331-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-18-2331-hourly-autopilot.json`
- Runtime gate evaluation: `wiki/evidence-store/sources/2026-06-18-2331-hourly-autopilot-runtime-gate-evaluation.json`

## 지표 설명

- `blocked_mcp_tiered_strict`: core/quote/spread/risk 관점에서 trim path가 보여도 current-cycle research confirmation이 strict submit threshold에 못 미쳐 최종 제출을 막은 상태다.
- `review_backlog_throttle`: `paper_validation_execution.validation_order_sizing.review_backlog_throttle`는 신규 buy만 줄이거나 중단한다. risk-reducing sell 진단은 별도로 계속 기록한다.
- `sell_candidate_diagnostics`: 실행하지 않은 trim 후보도 metric 값 또는 explicit gap reason을 남겨 다음 analyst review와 policy learning에 연결한다.
