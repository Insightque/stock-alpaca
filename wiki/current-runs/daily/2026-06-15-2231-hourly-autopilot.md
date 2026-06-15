# 2026-06-15-2231-hourly-autopilot

## 요약

`2231` scheduled hourly-autopilot은 scheduler-owned stale cleanup/core/research preflight를 source-of-record로 사용했다. preflight clock `2026-06-15T09:31:09.669268737-04:00`, account `ACTIVE`, positions `33`, open orders `0`, fresh quote rows가 모두 20분 이내라 Alpaca core hard gate를 PASS 처리했다. Research tiered gate도 `SEC EDGAR/FRED/Firecrawl/Yahoo Finance` pass로 strict submit threshold `3` confirmations를 충분히 충족했고, `Alpha Vantage`는 `NEWS_SENTIMENT` empty-response row를 `gap_category=empty_response`로 기록했다.

sell-first 재평가에서는 `RGTI`가 speculative loss-control trim trigger와 미실현 손실 `-11.40%`, fresh quote `22.55/22.58`, spread `0.1329%`, open orders `0`, validation lifecycle due-block 없음 조건을 모두 만족해 이번 cycle의 우선 실행 후보가 됐다. `AVGO`는 de-risking rationale가 남아 있지만 fresh quote `394.38/396.50` 기준 spread `0.5361%`로 policy cap `0.50%`를 넘겨 hard gate에서 탈락했다. 실제 submit은 `2026-06-15T13:41:41Z`에 수행됐고 `RGTI` sell `9주` order는 `2026-06-15T13:41:43Z`에 `filled_avg_price=23.366667 USD`로 즉시 체결됐다. post-trade reconciliation 기준 open orders는 `0`, `RGTI` 보유수량은 `37주 -> 28주`, cash는 `32156.69 USD`로 증가했다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env` 기준 `ALPACA_PAPER_TRADE=true` |
| Market clock | PASS | scheduler-owned Alpaca clock `2026-06-15T09:31:09.669268737-04:00`, regular market open |
| Stale order lifecycle | PASS | stale cleanup status `pass`; initial/remaining open orders 모두 `0` |
| Alpaca core MCP | PASS | scheduler core preflight hard gate `pass`, required rows complete, quotes fresh |
| Research MCP | PASS tiered | SEC EDGAR/FRED/Firecrawl/Yahoo positive, Alpha는 empty-response gap only |
| Universe strict | PASS | broad metadata universe `62`개, SPY/QQQ 포함 |
| Review backlog throttle | PASS for sells / PASS for buys | `pending_1d=1`, `pending_5d=16`, `pending_20d=1`; buy stop threshold `12` 이하 |
| Quote/spread | PASS for RGTI | submit boundary quote age 약 `10.28`분, spread `0.1329%` |
| Risk plan | PASS | `check-risk-policy.py --json` PASS |
| Final submit path | PASS | eligible sell-first trim `RGTI 9주 @ 22.55 USD` executed |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| RGTI | submit_trim | 0.1329% | speculative loss-control trim trigger, duplicate/open-order conflict 없음, held qty `37 -> 9` trim executable |
| AVGO | blocked_spread_gate | 0.5361% | de-risking rationale는 유지되지만 policy cap `0.50%` 초과 |
| BAC | executable_if_no_sell | 0.0707% | financials diversifier fallback buy로는 유효하지만 eligible sell-first trim이 먼저 열림 |
| NEE | watch_only | 0.1287% | executable quote는 있으나 weak lifecycle cohort라 fallback 우선순위가 낮음 |
| SPY | blocked_floor_cap | 0.0080% | 1주 ask `752.50 USD`가 validation floor cap 약 `511.02 USD` 초과 |
| NOK | blocked_validation_lifecycle_add_block | 0.0672% | `review-due-index` add-block 유지 |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| RGTI | submit_trim | pass | speculative loss-control trigger active, spread pass, same-day duplicate 없음 |
| AVGO | watch | spread_within_policy | de-risking rationale는 남지만 fresh spread `0.5361%`가 hard cap 초과 |
| BAC | hold_watch | sell_trigger_none | buy fallback은 가능하지만 active sell/trim trigger 없음 |

## 주문/체결

| Symbol | Side | Qty | Limit | Status | Filled Avg | Order ID |
| --- | --- | ---: | ---: | --- | ---: | --- |
| RGTI | sell | 9 | 22.55 | filled | 23.366667 | `ae15441f-844b-47ab-8970-a37242d13421` |

- `place_stock_order` actual submit: `2026-06-15T13:41:41.654523Z`
- `filled_at`: `2026-06-15T13:41:43.341983Z`
- Open orders after reconciliation: `0`

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | broad universe 62개, shortlist 10개 |
| `check-mcp-coverage.py --strict --json` | PASS | Alpaca core pass, positive research 4개, Alpha empty-response gap only |
| `check-risk-policy.py --json` | PASS | sell-first trim order plan 통과 |

## 산출물

- Report: `wiki/current-runs/daily/2026-06-15-2231-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-15-2231-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-15-2231-hourly-autopilot.json`
- Runtime gate evaluation: `wiki/evidence-store/sources/2026-06-15-2231-hourly-autopilot-runtime-gate-evaluation.json`
- Deterministic submit note: `wiki/evidence-store/sources/2026-06-15-2231-hourly-autopilot-deterministic-submit.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-15-2231-hourly-autopilot-post-trade.json`

## 지표 설명

- `speculative loss-control trim`: `risk_trim_policy.active_trim_triggers.speculative_loss_pct=-8` 기준으로 큰 미실현 손실이 남은 speculative sleeve를 단계적으로 줄이는 경로다.
- `validation floor per-order cap`: `portfolio_value * 0.5%` 상한이다. 이번 cycle cap은 약 `511.02 USD`라 `SPY/QQQ` 1주가 초과한다.
- `sell_candidate_diagnostics`: 실행하지 않은 trim/hold 후보도 why-not evidence를 남겨 후속 analyst review와 policy learning에 사용한다.
- `provider gap`: 이번 run의 Alpha Vantage는 shortlisted symbols에서 candidate news를 반환하지 않아 `gap_category=empty_response`로 남았다. 나머지 4개 research confirmations가 strict MCP gate를 통과시켰다.
