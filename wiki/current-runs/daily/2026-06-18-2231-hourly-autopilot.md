# 2026-06-18-2231-hourly-autopilot scheduled paper autopilot

## 요약

`2231` scheduled hourly-autopilot은 scheduler-owned stale cleanup/core/research preflight를 source-of-record로 사용했고, live Alpaca submit-boundary continuity로 regular market open, account `ACTIVE`, open orders `0`, same US-date fills `0`, watchlists `0`를 재확인했다. stale cleanup은 pass, Alpaca core도 pass, universe strict와 risk validator도 pass였다.

다만 이번 cycle research preflight는 `SEC EDGAR`와 `FRED`만 usable/pass로 남고 `Yahoo Finance`는 `timeout`, `Alpha Vantage`는 `empty_response`, `Firecrawl`은 credits failure로 남아 `check-mcp-coverage.py --strict`가 FAIL했다. sell-first 평가에서는 `RGTI` 6주 trim이 core/quote/spread/open-order/risk 관점에서 가장 executable했지만, workflow의 strict MCP submit gate를 통과하지 못해 submit을 열지 않았다. buy side는 `review_backlog_pending_1d_count=17`이 YAML stop threshold `12`를 넘겨 신규 validation buy가 별도로 닫혀 있었다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env` 기준 `ALPACA_PAPER_TRADE=true` |
| Market clock | PASS | live Alpaca `get_clock` `2026-06-18T09:34:09.231654264-04:00`, regular market open |
| Stale order lifecycle | PASS | `2231` stale cleanup artifact 기준 stale candidates `0`, remaining open orders `0` |
| Alpaca core MCP | PASS | scheduler core preflight hard gate `pass`, live continuity 기준 account `ACTIVE`, open orders `0`, fills today `0` |
| Research MCP strict | FAIL | usable/pass research provider가 `SEC EDGAR`, `FRED` 2개뿐이라 strict submit threshold `3` 미달 |
| Universe strict | PASS | broad metadata universe `62`개, SPY/QQQ 포함 |
| Review backlog throttle | FAIL for buys only | `pending_1d_count=17` > `stop_new_buys_at_pending_1d=12`, `NOK` add-block 유지 |
| Quote freshness | PASS | live `RGTI/SO/PFE/AAPL/BAC/WMT/NVDA` quote age 모두 약 `0.1`분 이내 |
| Spread | MIXED | `RGTI 0.0978%`, `SO 0.1727%` PASS, `PFE 10.3470%` FAIL |
| Risk plan | PASS | `check-risk-policy.py --json` 기준 current positions `34`, `orders=[]` 허용 |
| Final submit path | NO SUBMIT | first blocking gate `mcp_research_confirmations` |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| RGTI | blocked_mcp_tiered_strict | 0.0978% | speculative trim trigger, duplicate/open-order clean, 6주 trim path까지 열렸지만 strict research confirmation `2/3`로 submit gate 실패 |
| SO | blocked_sell_metric_gap | 0.1727% | repeated weak-review trim narrative는 유지되지만 decision-grade expected-excess/replacement margin 수치 공백 |
| PFE | blocked_live_spread | 10.3470% | repeated weak-review trim rationale는 유지되지만 live spread가 hard cap `0.50%` 크게 초과 |
| AAPL | blocked_review_backlog_throttle | 0.0268% | preflight-covered mega-cap fallback이나 pending review backlog가 신규 buy slot을 닫음 |
| BAC | blocked_review_backlog_throttle | 0.0699% | financials diversifier fallback이나 buy-side backlog throttle 우선 차단 |
| WMT | blocked_review_backlog_throttle | 0.0425% | defensive fallback이나 buy-side backlog throttle 우선 차단 |
| NVDA | blocked_review_backlog_and_same_theme_warning | 0.0338% | ai_semiconductor warning band와 pending review backlog 동시 유지 |
| QQQ | blocked_validation_floor_cap | 0.0856% | 1주 ask `736.62 USD`가 validation floor per-order cap 약 `507.40 USD` 초과 |
| SPY | blocked_validation_floor_cap | 0.0054% | 1주 ask `746.67 USD`가 validation floor per-order cap 약 `507.40 USD` 초과 |
| PLTR | blocked_low_source_confidence | 0.0854% | current thesis/source confidence가 relaxed floor-size buy 허용 범위 밖 |
| NOK | blocked_validation_lifecycle_add_block | 0.0723% | `review-due-index`가 `blocked_add_symbols=['NOK']` 유지 |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| RGTI | watch | `mcp_tiered_strict` | core-only trim 관점에서는 가장 executable했지만 이번 cycle strict MCP validator가 submit boundary를 막음 |
| SO | watch | `sell_metric_gap` | quote/spread는 pass지만 decision-grade trim metric 공백이 남아 있음 |
| PFE | watch | `spread_within_policy` | negative expected excess는 유지되지만 live spread `10.3470%`로 hard cap fail |

## 주문/체결

- Planned orders: 0
- Submitted orders: 0
- `place_stock_order` 호출: 없음
- submit 직전까지 열렸던 최상위 order 후보: `RGTI sell 6 @ 20.44 USD`
- no-submit 사유: `check-mcp-coverage.py --strict` FAIL, first blocking gate `mcp_research_confirmations`

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | 62 symbols, shortlist 10개 |
| `check-mcp-coverage.py --strict --json` | FAIL | positive research `fred`, `sec-edgar`만 usable |
| `check-risk-policy.py --json` | PASS | current positions `34`, `orders=[]` warning only |

## 산출물

- Report: `wiki/current-runs/daily/2026-06-18-2231-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-18-2231-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-18-2231-hourly-autopilot.json`
- Runtime gate evaluation: `wiki/evidence-store/sources/2026-06-18-2231-hourly-autopilot-runtime-gate-evaluation.json`

## 지표 설명

- `blocked_mcp_tiered_strict`: core/quote/spread/risk 관점에서 실행 가능해도 current-cycle research confirmation이 strict submit threshold에 못 미쳐 최종 제출을 막은 상태다.
- `review_backlog_throttle`: `paper_validation_execution.validation_order_sizing.review_backlog_throttle`가 신규 buy만 줄이거나 중단하는 YAML gate다. risk-reducing sell 진단은 별도로 계속 기록한다.
- `sell_candidate_diagnostics`: 실행하지 않은 trim 후보도 metric 값 또는 explicit gap reason을 남겨 다음 analyst review와 policy learning에 연결한다.
