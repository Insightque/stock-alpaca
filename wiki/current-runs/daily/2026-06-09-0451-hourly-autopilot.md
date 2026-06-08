# 2026-06-09-0451-hourly-autopilot scheduled paper autopilot

## 요약

정규장 scheduled hourly autopilot을 실행했다. `ALPACA_PAPER_TRADE=true`를 확인했고, scheduler-owned `0451` stale cleanup/core/research preflight를 우선 사용했다. stale cleanup은 open order 0건으로 종료됐고 core preflight hard gate도 `pass`였다. 이번 cycle은 required core row가 모두 fresh/pass라 추가 Alpaca read-only MCP 호출 없이 scheduler evidence만으로 clock/account/positions/open-orders/recent-fills/quotes 상태를 확정했다.

이번 run은 sell/trim을 먼저 평가했다. `RGTI`는 speculative sleeve trim trigger가 계속 active지만 2251 cycle same-day filled trim 때문에 duplicate sell gate에 막혔다. `AVGO`는 scheduler preflight quote가 `395.41/395.50`으로 spread `0.0228%`까지 정상 범위로 돌아왔어도, same-day after-hours sell 2건이 남아 duplicate discipline이 먼저 추가 trim을 막았다. `SO`는 scheduler preflight quote가 `91.25/91.27`로 spread `0.0219%`를 유지했지만 trim justification용 replacement quality margin이 비어 있어 decision-grade metric gate를 통과하지 못했다. buy fallback에서는 `review_backlog_pending_1d_count=13`이 YAML stop threshold `12`를 초과해 신규 buy slot이 먼저 차단됐고, 보조 후보 `SPY/QQQ`는 1주 ask가 validation floor per-order cap 약 `499.77 USD`를 넘었으며 `NOK`는 validation_lifecycle add-block이 유지됐다. 연구 MCP는 SEC EDGAR/FRED/Firecrawl/Yahoo pass를 유지했고, Alpha Vantage는 circuit breaker open `provider_error` gap만 기록됐다. 따라서 이번 cycle도 exact blocker를 남긴 채 `orders: []`로 종료한다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env`에서 `ALPACA_PAPER_TRADE=true` 확인 |
| Market clock | PASS | scheduler Alpaca clock `2026-06-08T15:51:11.896454741-04:00`, regular market open |
| Stale order lifecycle | PASS | `0451` stale cleanup artifact 기준 open order 0건 |
| Alpaca core MCP | PASS | scheduler-owned core preflight hard gate pass, quotes/account/positions/open-orders/recent-activities 모두 충족 |
| Research MCP | PASS tiered | SEC EDGAR/FRED/Firecrawl/Yahoo positive, Alpha circuit breaker `provider_error` gap은 nonblocking |
| Universe strict | PASS | metadata universe 62개, SPY/QQQ 포함 |
| Review backlog throttle | BUY BLOCK | `pending_1d_count=13`으로 YAML `stop_new_buys_at_pending_1d=12` 초과. sell/trim에는 비적용 |
| Quote/spread | PASS | `RGTI/AVGO/SO/SPY/QQQ/NOK` 모두 scheduler preflight fresh quote와 spread cap 통과 |
| Risk plan | PASS | `check-risk-policy.py --json` PASS |
| Final submit path | BLOCK | sell 3종은 duplicate/metric gate 미통과, buy fallback은 backlog/notional cap/lifecycle blocker |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| RGTI | watch_same_day_sell | 0.0456% | speculative loss trigger는 유지되지만 `hourly-20260608-2251-sell-rgti` filled가 same-day all-orders에 남아 추가 trim 불가 |
| AVGO | watch_same_day_sell | 0.0228% | warning-band trim rationale는 유지되지만 same-day after-hours sell 2건 때문에 duplicate discipline이 먼저 작동 |
| SO | blocked_metric_gap | 0.0219% | quote/spread는 정상 유지됐지만 trim justification용 replacement margin 공백이 남아 decision-grade metric gate 미통과 |
| SPY | blocked_review_backlog_and_floor_cap | 0.0041% | 신규 buy slot은 backlog throttle로 차단됐고 1주 ask `738.91 USD`도 validation floor per-order cap을 초과 |
| QQQ | blocked_review_backlog_and_floor_cap | 0.0112% | 신규 buy slot은 backlog throttle로 차단됐고 1주 ask `715.41 USD`도 validation floor per-order cap을 초과 |
| NOK | blocked_review_backlog_and_lifecycle | 0.0688% | backlog throttle가 먼저 걸리고 `review-due-index`의 add-block도 유지됨 |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| RGTI | watch | same_day_duplicate_symbol_side | 2251 cycle trim 30주 filled가 same-day all-orders에 남아 0451 cycle 추가 trim 불가 |
| AVGO | watch | same_day_duplicate_symbol_side | scheduler preflight spread는 `0.0228%`로 정상 범위지만 same-day after-hours sell 2건이 duplicate discipline을 유지 |
| SO | watch | decision_grade_metric_gap | scheduler preflight quote `91.25/91.27`은 spread gate를 통과했지만 trim replacement margin이 비어 있어 order 승격 불가 |

## 주문/체결

- Planned orders: 0
- Submitted orders: 0
- `place_stock_order` 호출: 없음
- Pre-submit gate summary: 주문 후보가 최종 hard gate를 통과하지 못해 작성/호출 대상이 없었다. paper mode `true`, market clock `2026-06-08T15:51:11.896454741-04:00`, order plan path `wiki/trade-ledger/orders/2026-06-09-0451-hourly-autopilot.json`, universe strict `PASS`, MCP strict `PASS`, risk `PASS`, quote freshness `PASS`, spread `PASS`, order shape는 whole-share/day-limit/stock 준비 상태였고 duplicate/open-order check는 `RGTI/AVGO` same-day duplicate로 막혔다. source refs는 `0451` stale cleanup/core/research preflight와 runtime gate snapshot, policy/review/ticker artifacts다.
- Post-trade reconciliation: submit attempt는 없었지만 scheduler preflight recent-activities 기준 same-day filled orders 4건(`AVGO` 장외 sell 2건, `TSLA` exit 1건, `RGTI` trim 1건)을 재확인했다. positions는 `32`, account snapshot은 portfolio value `99954.94 USD`, cash `31774.85 USD`, buying power `301654.30 USD`, long market value `68180.09 USD`다.

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | 62 symbols, SPY/QQQ 포함, final candidates 3개 |
| `check-mcp-coverage.py --strict --json` | PASS | Alpaca core pass, positive research 4개, Alpha circuit breaker `provider_error` gap only |
| `check-risk-policy.py --json` | PASS | 주문 0건, 현재 포지션 포함 |

## 산출물

- Report: `wiki/current-runs/daily/2026-06-09-0451-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-09-0451-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-09-0451-hourly-autopilot.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-09-0451-hourly-autopilot-post-trade.json`
- Source refs: `wiki/evidence-store/sources/2026-06-09-0451-hourly-autopilot-stale-order-cleanup.json`, `wiki/evidence-store/sources/2026-06-09-0451-hourly-autopilot-alpaca-core-preflight.json`, `wiki/evidence-store/sources/2026-06-09-0451-hourly-autopilot-research-mcp-preflight.json`, `wiki/evidence-store/sources/2026-06-09-0451-hourly-autopilot-runtime-gate-evaluation.json`

## 지표 설명

- `sell_candidate_diagnostics`: 보유 포지션 중 trim/exit 재점검이 필요한 상위 후보와 blocked gate를 남기는 audit trail이다.
- `review_backlog_pending_1d_count`: validation buy review backlog count다. 이번 run에서는 `13`으로 YAML stop threshold `12`를 넘어 신규 buy를 막았지만, risk-reducing sell에는 적용하지 않았다.
- `validation_floor_per_order_cap`: `confidence_tiers.validation_floor.max_notional_pct=0.005`에 따라 1주 notional이 계좌 가치의 0.5%를 넘는 benchmark fallback 매수는 막는다.
- `alpha-vantage` circuit breaker gap: scheduler research preflight가 직전 provider_error 이후 `2026-06-08T19:51:32+00:00`까지 circuit breaker open row를 남겼고, 나머지 4개 research provider pass로 strict MCP gate는 유지됐다.
