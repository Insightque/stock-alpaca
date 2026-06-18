# 2026-06-19-0131-hourly-autopilot scheduled paper autopilot

## 요약

`0131` scheduled hourly-autopilot은 scheduler-owned stale cleanup/core/research preflight를 source-of-record로 사용했다. stale cleanup은 `remaining open orders 0`, Alpaca core는 hard gate `pass`, same-day fill ledger에는 직전 `0111` cycle의 `RGTI` 3주 trim이 `2026-06-18T16:21:48.495146Z`에 `20.43 USD`로 체결된 기록이 남아 있어 포지션이 `RGTI qty=9`, `qty_available=9`로 줄어든 상태를 확인했다.

다만 이번 cycle research preflight는 `SEC EDGAR`와 `FRED`만 usable/pass로 남고 `Yahoo Finance`는 `timeout`, `Alpha Vantage`는 throttle-based `provider_error`, `Firecrawl`은 credits failure `unknown` gap으로 남아 `check-mcp-coverage.py --strict`가 다시 FAIL했다. sell-first 평가에서는 residual `RGTI` 2주 trim이 core/quote/spread/open-order/risk 관점에서 가장 executable했지만, workflow의 strict MCP submit gate를 통과하지 못해 submit을 열지 않았다. buy side는 `review_backlog_pending_1d_count=17`이 YAML stop threshold `12`를 넘겨 신규 validation buy가 별도로 닫혀 있었다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env` 기준 `ALPACA_PAPER_TRADE=true` |
| Market clock | PASS | scheduler preflight `get_clock` `2026-06-18T12:31:06.894636067-04:00`, regular market open |
| Stale order lifecycle | PASS | `0131` stale cleanup artifact 기준 stale candidates `0`, remaining open orders `0` |
| Alpaca core MCP | PASS | scheduler core preflight hard gate `pass`, account `ACTIVE`, positions `33`, open orders `0`, watchlists `0` |
| Research MCP strict | FAIL | usable/pass research provider가 `SEC EDGAR`, `FRED` 2개뿐이라 strict submit threshold `3` 미달 |
| Universe strict | PASS | broad metadata universe `62`개, SPY/QQQ 포함 |
| Review backlog throttle | FAIL for buys only | `pending_1d_count=17` > `stop_new_buys_at_pending_1d=12` |
| Quote freshness | PASS | scheduler quote timestamp가 decision time 기준 20분 cap 이내 |
| Spread | MIXED PASS | `RGTI 0.0491%`, `AAPL 0.0202%`, `BAC 0.0178%`, `WMT 0.0085%`, `NVDA 0.0095%`, `QQQ 0.0041%`, `SPY 0.0027%`는 pass, `SO 0.7224%`는 fail |
| Risk plan | PASS | `check-risk-policy.py --json` 기준 current positions `33`, `orders=[]` 허용 |
| Final submit path | NO SUBMIT | first blocking gate `mcp_research_confirmations` |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| RGTI | blocked_mcp_tiered_strict | 0.0491% | speculative trim trigger, duplicate/open-order clean, residual 2주 trim path까지 열렸지만 strict research confirmation `2/3`로 submit gate 실패 |
| SO | blocked_sell_metric_gap | 0.7224% | repeated weak-review trim narrative는 유지되지만 decision-grade expected-excess/replacement margin 공백, spread도 hard cap 초과 |
| AAPL | blocked_review_backlog_throttle | 0.0202% | preflight-covered mega-cap fallback이나 pending review backlog가 신규 buy slot을 닫음 |
| BAC | blocked_review_backlog_throttle | 0.0178% | financials diversifier fallback이나 buy-side backlog throttle 우선 차단 |
| WMT | blocked_review_backlog_throttle | 0.0085% | defensive fallback이나 buy-side backlog throttle 우선 차단 |
| NVDA | blocked_review_backlog_and_same_theme_warning | 0.0095% | ai_semiconductor warning band와 pending review backlog 동시 유지 |
| QQQ | blocked_validation_floor_cap | 0.0041% | 1주 ask `738.96 USD`가 validation floor per-order cap 약 `507.98 USD` 초과 |
| SPY | blocked_validation_floor_cap | 0.0027% | 1주 ask `746.42 USD`가 validation floor per-order cap 약 `507.98 USD` 초과 |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| RGTI | watch | `mcp_tiered_strict` | core-only trim 관점에서는 가장 executable했지만 이번 cycle strict MCP validator가 submit boundary를 막음 |
| SO | watch | `sell_metric_gap` | quote/spread fail과 별개로 decision-grade trim metric 공백이 남아 있음 |
| AAPL | hold | `sell_trigger_none` | active trim trigger 없음 |

## 주문/체결

- Planned orders: 0
- Submitted orders: 0
- `place_stock_order` 호출: 없음
- submit 직전까지 열렸던 최상위 order 후보: `RGTI sell 2 @ 20.38 USD`
- no-submit 사유: `check-mcp-coverage.py --strict` FAIL, first blocking gate `mcp_research_confirmations`
- Post-trade reconciliation: scheduler core preflight `get_account_activities(activity_types=[FILL])` 기준 same-day fill ledger에는 `RGTI` sell 3주 `20.43 USD` fill이 포함된다. source-of-record account는 cash `28,424.81 USD`, portfolio value `101,595.45 USD`, buying power `303,308.26 USD`, positions `33`, open orders `0`, watchlists `0`였다.

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | 62 symbols, shortlist 10개 |
| `check-mcp-coverage.py --strict --json` | FAIL | positive research `fred`, `sec-edgar`만 usable |
| `check-risk-policy.py --json` | PASS | current positions `33`, `orders=[]` warning only |

## 산출물

- Report: `wiki/current-runs/daily/2026-06-19-0131-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-19-0131-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-19-0131-hourly-autopilot.json`
- Runtime gate evaluation: `wiki/evidence-store/sources/2026-06-19-0131-hourly-autopilot-runtime-gate-evaluation.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-19-0131-hourly-autopilot-post-trade.json`

## 지표 설명

- `blocked_mcp_tiered_strict`: core/quote/spread/risk 관점에서 실행 가능해도 current-cycle research confirmation이 strict submit threshold에 못 미쳐 최종 제출을 막은 상태다.
- `review_backlog_throttle`: `paper_validation_execution.validation_order_sizing.review_backlog_throttle`가 신규 buy만 줄이거나 중단하는 YAML gate다. risk-reducing sell 진단은 별도로 계속 기록한다.
- `sell_candidate_diagnostics`: 실행하지 않은 trim 후보도 metric 값 또는 explicit gap reason을 남겨 다음 analyst review와 policy learning에 연결한다.
