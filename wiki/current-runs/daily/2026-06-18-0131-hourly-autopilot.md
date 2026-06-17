# 2026-06-18-0131-hourly-autopilot scheduled paper autopilot

## 요약

`0131` scheduled hourly-autopilot은 scheduler-owned stale cleanup/core/research preflight를 source-of-record로 사용했다. preflight clock `2026-06-17T12:31:09.378600342-04:00`, account/positions/open-orders/quotes rows가 모두 pass였고 decision time 기준 20분 이내라 Alpaca core hard gate를 PASS 처리했다. Research tiered gate도 `SEC EDGAR/FRED/Yahoo Finance` pass로 strict submit threshold `3` confirmations를 유지했고, `Alpha Vantage`는 `provider_error`, `Firecrawl`은 `unknown` gap only로 남겼다.

live Alpaca continuity에서는 직전 `0111`의 `AAPL` buy 1주가 `2026-06-17T16:23:03Z`에 `298.42 USD`로 filled 전환됐고 현재 open orders는 `0`건이었다. sell-first 재평가에서는 `SO`가 trim decision-grade metric gap, `RGTI`와 `PFE`가 같은 미국 거래일 after-hours trim fill에 따른 duplicate symbol/side gate로 executable trim이 없었다. buy fallback에서는 `AAPL/XOM/AMZN/MSFT/NEE/NKE/FCX/WMT/BAC`이 same-day filled buy duplicate, `SPY/QQQ`가 floor cap 초과, `PLTR`이 low source confidence, `NVDA`가 ai_semiconductor warning band에 막혔다. `[[GOOGL]]`은 same-day duplicate/open-order conflict가 없는 existing mega-cap quality holding으로 live quote `365.30/365.88`, spread `0.1585%`, latest `2026-06-16` add evidence, high source confidence를 유지해 이번 cycle floor-size learning buy 후보로 승격했고, `365.88 USD` day limit 1주가 `filled_avg_price=365.24 USD`로 즉시 체결됐다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env` 기준 `ALPACA_PAPER_TRADE=true` |
| Market clock | PASS | live `get_clock` `2026-06-17T12:34:24.958287422-04:00`, regular market open |
| Stale order lifecycle | PASS | `0131` stale cleanup artifact 기준 stale candidates 0, remaining open orders 0 |
| Alpaca core MCP | PASS | scheduler core preflight hard gate `pass`, live continuity 기준 open orders `0`, account `ACTIVE`, watchlists `0` |
| Research MCP | PASS tiered | SEC EDGAR/FRED/Yahoo positive 3개, Alpha provider_error gap, Firecrawl unknown gap |
| Universe strict | PASS | broad metadata universe `62`개, SPY/QQQ 포함 |
| Review backlog throttle | PASS for buy | `pending_1d_count=0`, `blocked_add_symbols=['NOK']` |
| Quote/spread | PASS for GOOGL | live quote `365.30/365.88`, spread `0.1585%`, freshness pass |
| Risk plan | PASS | `check-risk-policy.py --json` 기준 GOOGL 1주 buy risk gate 통과 |
| Final submit path | PASS | same-day duplicate/open-order check pass, whole-share day-limit stock, order filled |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| SO | blocked_sell_metric_gap | 0.0215% | quote/spread는 통과했지만 trim decision-grade expected-excess/replacement margin 공백 지속 |
| RGTI | blocked_same_day_duplicate_sell | 0.0471% | speculative trim trigger와 spread는 pass지만 same US-date after-hours trim fill 때문에 regular-session 추가 sell 차단 |
| PFE | blocked_same_day_duplicate_sell | 0.0382% | repeated weak-review trim rationale와 quote/spread는 pass지만 same US-date after-hours trim fill 때문에 regular-session 추가 sell 차단 |
| AAPL | blocked_same_day_duplicate_buy | 0.1072% | `0111` buy 1주가 same US-date에 이미 filled |
| XOM | blocked_same_day_duplicate_buy | n/a | `0051` buy 1주가 same US-date에 이미 filled |
| NVDA | blocked_same_theme_warning | 0.0145% | ai_semiconductor warning band 때문에 different-cluster fallback보다 후순위 |
| SPY | blocked_validation_floor_cap | 0.0027% | 1주 ask `750.38 USD`가 validation floor per-order cap 약 `506.80 USD`를 초과 |
| QQQ | blocked_validation_floor_cap | 0.0218% | 1주 ask `733.42 USD`가 validation floor per-order cap 약 `506.80 USD`를 초과 |
| PLTR | blocked_low_source_confidence | 0.0296% | existing thesis note의 source confidence가 낮아 relaxed floor-size buy 허용 범위를 벗어남 |
| GOOGL | selected_buy | 0.1585% | existing mega-cap quality holding, same-day duplicate/open-order conflict 없음, high source confidence |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| SO | watch | `sell_metric_gap` | trim expected-excess/replacement margin metric 공백 지속 |
| RGTI | watch | `duplicate_symbol_side_same_day` | spread는 정상이나 same-day after-hours trim fill 때문에 regular-session 추가 sell 차단 |
| PFE | watch | `duplicate_symbol_side_same_day` | same US-date after-hours trim fill 뒤라 regular-session 추가 sell 비허용 |

## 주문/체결

### 제출 전 게이트 요약

paper mode `true`; market clock `2026-06-17T12:34:24.958287422-04:00`; order plan path `wiki/trade-ledger/orders/2026-06-18-0131-hourly-autopilot.json`; universe strict `PASS`; MCP strict `PASS`; risk validator `PASS`; GOOGL quote freshness `~0.02m`; spread `0.1585%`; order shape `buy 1 share / limit 365.88 / day / stock / regular`; duplicate/open-order check `PASS`; source refs는 `0131` stale cleanup/core/research preflight, runtime gate evaluation, `review-due-index`, `2026-06-17-portfolio-review`, `[[GOOGL]]`다.

| Symbol | Side | Qty | Limit | Status | Filled Avg | Order ID |
| --- | --- | ---: | ---: | --- | ---: | --- |
| GOOGL | buy | 1 | 365.88 | filled | 365.24 | `d3348fdf-59ff-4f89-9e42-be97d6ff2fa4` |

## Reconciliation

same `client_order_id` readback 기준 `GOOGL` 주문은 `2026-06-17T16:40:11.20362247Z`에 `filled_avg_price=365.24 USD`로 즉시 체결됐다. live `get_orders(status=open)` 기준 open orders는 `0`건이다. same-day `get_orders(status=all, after=2026-06-16T20:00:00-04:00)` readback에서는 이번 `GOOGL` fill에 더해 `AAPL/XOM/MSFT/AMZN/NEE/NKE/FCX/WMT/BAC` buy 9건과 prior after-hours `PFE/RGTI` sell 두 건이 유지됐다. direct `get_account_info/get_all_positions` 기준 account `ACTIVE`, cash `28,580.26 USD`, portfolio value `101,359.05 USD`, buying power `302,371.39 USD`, positions `33`건, `GOOGL qty=5`, `avg_entry_price=376.204`, `current_price=365.05`, `AAPL qty=7`, `XOM qty=7`로 반영됐다.

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | 62 symbols, SPY/QQQ 포함 |
| `check-mcp-coverage.py --strict --json` | PASS | Alpaca core pass, positive research 3개 |
| `check-risk-policy.py --json` | PASS | staged deployment warning only |

## 산출물

- Report: `wiki/current-runs/daily/2026-06-18-0131-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-18-0131-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-18-0131-hourly-autopilot.json`
- Runtime gate evaluation: `wiki/evidence-store/sources/2026-06-18-0131-hourly-autopilot-runtime-gate-evaluation.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-18-0131-hourly-autopilot-post-trade.json`

## 지표 설명

- `blocked_same_day_duplicate_buy`: 같은 미국 거래일에 이미 filled된 동일 symbol buy는 재진입하지 않는다.
- `validation floor per-order cap`: floor-size learning buy도 `portfolio_value * 0.5%` 상한을 넘을 수 없다. 이번 cycle cap은 약 `506.80 USD`다.
- `tiered MCP gate`: core `alpaca` pass와 research positive confirmation `3개` 이상이면 Alpha/Firecrawl 비핵심 gap이 있어도 submit을 막지 않는다.
- `same_theme_warning`: ai_semiconductor warning band를 넘긴 same-theme add는 다른 executable fallback이 있을 때 후순위로 둔다.
