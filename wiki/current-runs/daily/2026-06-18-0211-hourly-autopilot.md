# 2026-06-18-0211-hourly-autopilot scheduled paper autopilot

## 요약

`0211` scheduled hourly-autopilot은 scheduler-owned stale cleanup/core/research preflight를 source-of-record로 사용했다. preflight hard gate는 `pass`였고 live Alpaca continuity 기준 regular market open, account `ACTIVE`, open orders `0`, watchlists `0`, 직전 `0151`의 `COP` buy 1주가 `2026-06-17T16:59:32.674078658Z`에 `110.83 USD`로 filled 전환된 점을 재확인했다. Research tiered gate도 `SEC EDGAR/FRED/Yahoo Finance` pass로 strict submit threshold `3` confirmations를 유지했고, `Alpha Vantage`는 one-call throttle `provider_error`, `Firecrawl`은 credit 부족 `unknown` gap only로 남겼다.

sell-first 재평가에서는 `SO`가 repeated weak-review defensive sleeve trim 후보이지만 trim decision-grade expected-excess/replacement margin 공백으로 sell 승격이 막혔고, `RGTI`와 `PFE`는 same US-date after-hours trim fill 때문에 duplicate symbol/side gate가 유지돼 executable trim이 없었다. buy fallback에서는 `GOOGL/AAPL/AMZN/BAC/WMT/NEE/FCX/COP`가 same-day filled buy duplicate, `SPY/QQQ`가 floor cap 초과, `PLTR`가 low source confidence speculative profile로 탈락했다. 남은 preflight-covered existing holding 중 `[[SO]]`는 live quote `93.36/93.38`, spread `0.0214%`, active tradable NYSE stock, utilities/rate-sensitive diversifier 역할, review backlog throttle 비차단, 3-provider positive research confirmation을 유지해 floor-size learning buy 후보로 승격됐고, `93.38 USD` day limit 1주가 `filled_avg_price=93.24 USD`로 즉시 체결됐다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env` 기준 `ALPACA_PAPER_TRADE=true` |
| Market clock | PASS | live `get_clock` `2026-06-17T13:14:05.509651875-04:00`, regular market open |
| Stale order lifecycle | PASS | `0211` stale cleanup artifact 기준 stale candidates `0`, remaining open orders `0` |
| Alpaca core MCP | PASS | scheduler core preflight hard gate `pass`, live continuity 기준 `COP` fill 재확인, open orders `0`, account `ACTIVE`, watchlists `0` |
| Research MCP | PASS tiered | SEC EDGAR/FRED/Yahoo positive 3개, Alpha provider_error gap, Firecrawl unknown gap |
| Universe strict | PASS | broad metadata universe `62`개, SPY/QQQ 포함 |
| Review backlog throttle | PASS for buy | `pending_1d_count=0`, `blocked_add_symbols=['NOK']` |
| Quote/spread | PASS for SO | live quote `93.36/93.38`, spread `0.0214%`, freshness pass |
| Risk plan | PASS | `check-risk-policy.py --json` 기준 SO 1주 buy risk gate 통과 |
| Final submit path | PASS | same-day duplicate/open-order check pass, whole-share day-limit stock, order filled |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| SO | blocked_sell_metric_gap / selected_buy | 0.0214% | trim 경로는 decision-grade metric gap으로 막혔지만 buy 경로는 hard gate를 모두 통과한 existing utilities fallback |
| RGTI | blocked_same_day_duplicate_sell | 0.0472% | speculative trim trigger와 spread는 pass지만 same US-date after-hours trim fill 때문에 추가 sell 차단 |
| PFE | blocked_same_day_duplicate_sell | 0.0382% | repeated weak-review trim rationale와 quote/spread는 pass지만 same US-date after-hours trim fill 때문에 추가 sell 차단 |
| GOOGL | blocked_same_day_duplicate_buy | n/a | `0131` buy 1주가 same US-date에 이미 filled |
| AAPL | blocked_same_day_duplicate_buy | n/a | `0111` buy 1주가 same US-date에 이미 filled |
| AMZN | blocked_same_day_duplicate_buy | n/a | `0011` buy 1주가 same US-date에 이미 filled |
| BAC | blocked_same_day_duplicate_buy | n/a | `2231` buy 1주가 same US-date에 이미 filled |
| WMT | blocked_same_day_duplicate_buy | n/a | `2251` buy 1주가 same US-date에 이미 filled |
| NEE | blocked_same_day_duplicate_buy | n/a | `2351` buy 1주가 same US-date에 이미 filled |
| FCX | blocked_same_day_duplicate_buy | n/a | `2311` buy 1주가 same US-date에 이미 filled |
| COP | blocked_same_day_duplicate_buy | n/a | `0151` buy 1주가 same US-date에 이미 filled |
| SPY | blocked_validation_floor_cap | 0.0040% | 1주 ask `749.34 USD`가 validation floor per-order cap 약 `506.45 USD`를 초과 |
| QQQ | blocked_validation_floor_cap | 0.0287% | 1주 ask `731.96 USD`가 validation floor per-order cap 약 `506.45 USD`를 초과 |
| PLTR | blocked_low_source_confidence | 0.0296% | existing thesis note의 source confidence가 낮아 relaxed floor-size buy 허용 범위를 벗어남 |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| SO | watch | `sell_metric_gap` | trim expected-excess/replacement margin metric 공백 지속 |
| RGTI | watch | `duplicate_symbol_side_same_day` | spread는 정상이나 same-day after-hours trim fill 때문에 regular-session 추가 sell 차단 |
| PFE | watch | `duplicate_symbol_side_same_day` | same US-date after-hours trim fill 뒤라 regular-session 추가 sell 비허용 |

## 주문/체결

### 제출 전 게이트 요약

paper mode `true`; market clock `2026-06-17T13:14:05.509651875-04:00`; order plan path `wiki/trade-ledger/orders/2026-06-18-0211-hourly-autopilot.json`; universe strict `PASS`; MCP strict `PASS`; risk validator `PASS`; SO quote freshness `~0m`; spread `0.0214%`; order shape `buy 1 share / limit 93.38 / day / stock / regular`; duplicate/open-order check `PASS`; source refs는 `0211` stale cleanup/core/research preflight, runtime gate evaluation, `review-due-index`, `2026-06-17-portfolio-review`, `[[SO]]`, `[[RGTI]]`, `[[PFE]]`, `[[PLTR]]`다.

| Symbol | Side | Qty | Limit | Status | Filled Avg | Order ID |
| --- | --- | ---: | ---: | --- | ---: | --- |
| SO | buy | 1 | 93.38 | filled | 93.24 | `9ba83a07-21e4-4d69-8496-8a34075b9d92` |

## Reconciliation

same `client_order_id` readback 기준 `SO` 주문은 `2026-06-17T17:19:02.097011303Z`에 `filled_avg_price=93.24 USD`로 즉시 체결됐다. live `get_orders(status=open)` 기준 open orders는 `0`건이다. same-day `get_orders(status=all, after=2026-06-16T20:00:00-04:00)` readback에서는 이번 `SO` fill에 더해 `COP/GOOGL/AAPL/XOM/MSFT/AMZN/NEE/NKE/FCX/WMT/BAC` buy 11건과 prior after-hours `PFE/RGTI` sell 두 건이 유지됐다. direct `get_account_info/get_all_positions` 기준 account `ACTIVE`, cash `28,376.19 USD`, portfolio value `101,309.29 USD`, buying power `301,908.39 USD`, positions `33`건, `SO qty=6`, `avg_entry_price=92.801667`, `current_price=93.23`, `COP qty=7`, `PLTR qty=3`로 반영됐다.

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | 62 symbols, pre-shortlist 10, SPY/QQQ 포함 |
| `check-mcp-coverage.py --strict --json` | PASS | Alpaca core pass, positive research 3개 |
| `check-risk-policy.py --json` | PASS | staged deployment warning only |

## 산출물

- Report: `wiki/current-runs/daily/2026-06-18-0211-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-18-0211-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-18-0211-hourly-autopilot.json`
- Runtime gate evaluation: `wiki/evidence-store/sources/2026-06-18-0211-hourly-autopilot-runtime-gate-evaluation.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-18-0211-hourly-autopilot-post-trade.json`

## 지표 설명

- `blocked_same_day_duplicate_buy`: 같은 미국 거래일에 이미 filled된 동일 symbol buy는 regular-session에서 다시 만들지 않는다.
- `validation floor per-order cap`: floor-size learning buy도 `portfolio_value * 0.5%` 상한을 넘을 수 없다. 이번 cycle cap은 약 `506.45 USD`다.
- `tiered MCP gate`: core `alpaca` pass와 research positive confirmation `3개` 이상이면 Alpha/Firecrawl 비핵심 gap이 있어도 submit을 막지 않는다.
- `sell_metric_gap`: trim rationale 자체는 있으나 policy가 요구하는 decision-grade expected-excess/replacement margin 수치가 비어 있어 sell 승격을 막는 상태다.
