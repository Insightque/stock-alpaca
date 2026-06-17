# 2026-06-18-0011-hourly-autopilot scheduled paper autopilot

## 요약

`0011` scheduled hourly-autopilot은 scheduler-owned stale cleanup/core/research preflight를 source-of-record로 사용했다. preflight clock `2026-06-17T11:11:09.53945663-04:00`, account/positions/open-orders/quotes rows가 모두 pass였고 decision time 기준 20분 이내라 Alpaca core hard gate를 PASS 처리했다. Research tiered gate도 `SEC EDGAR/FRED/Yahoo Finance` pass로 strict submit threshold `3` confirmations를 유지했고, `Alpha Vantage`는 hourly throttle `provider_error`, `Firecrawl`은 credits 부족 `unknown` gap only로 유지했다.

live Alpaca continuity에서는 `2351`의 `NEE` buy 1주가 `2026-06-17T14:59:48.764184Z`에 `86.38 USD`로 filled 전환됐고 open orders는 `0`건임을 먼저 재확인했다. sell-first 재평가에서는 `SO`가 trim decision-grade metric gap, `RGTI`와 `PFE`가 같은 미국 거래일 after-hours trim fill에 따른 duplicate symbol/side gate로 executable trim이 없었다. buy fallback에서는 `BAC/WMT/FCX/NKE/NEE`가 same-day duplicate buy로 탈락했고, `SPY/QQQ`는 validation floor per-order cap을 초과했으며 `GOOGL`은 ask outlier로 spread fail이었다. `AMZN`은 existing mega-cap holding이지만 hard gate를 깨지 않고 live quote `240.40/240.45`, spread `0.0208%`, duplicate/open-order conflict 없음, preflight research coverage 유지 조건을 충족해 floor-size learning buy 1주 후보로 승격했다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env` 기준 `ALPACA_PAPER_TRADE=true` |
| Market clock | PASS | live `get_clock` `2026-06-17T11:13:29.862278789-04:00`, regular market open |
| Stale order lifecycle | PASS | `0011` stale cleanup artifact 기준 stale candidates 0, remaining open orders 0 |
| Alpaca core MCP | PASS | scheduler core preflight hard gate `pass`, live continuity 기준 open orders `0`, watchlists `0`, account `ACTIVE` |
| Research MCP | PASS tiered | SEC EDGAR/FRED/Yahoo positive 3개, Alpha throttle gap, Firecrawl credit gap |
| Universe strict | PASS | broad metadata universe `62`개, SPY/QQQ 포함 |
| Review backlog throttle | PASS for buy | `pending_1d_count=0`, `blocked_add_symbols=['NOK']` |
| Quote/spread | PASS for AMZN | live AMZN quote `240.40/240.45`, spread `0.0208%`, freshness pass |
| Risk plan | PASS | `check-risk-policy.py --json` 기준 AMZN 1주 buy risk gate 통과 |
| Final submit path | PASS | same-day duplicate/open-order check for `AMZN` pass, whole-share day-limit stock, order submitted |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| SO | blocked_sell_metric_gap | 0.0321% | quote/spread는 통과했지만 trim decision-grade expected-excess/replacement margin 공백 지속 |
| RGTI | blocked_same_day_duplicate_sell | 0.0965% | speculative trim trigger와 spread는 pass지만 same US-date after-hours sell fill이 있어 duplicate sell gate 유지 |
| PFE | blocked_same_day_duplicate_sell | 0.0382% | repeated weak-review trim rationale와 quote/spread는 pass지만 same US-date after-hours sell fill이 있어 regular-session 추가 sell 차단 |
| BAC | blocked_same_day_duplicate_buy | 0.0174% | `2231` buy 1주가 same US-date에 이미 filled돼 regular-session duplicate buy 재진입 불가 |
| WMT | blocked_same_day_duplicate_buy | 0.0168% | `2251` buy 1주가 same-day filled라 duplicate buy gate 적용 |
| FCX | blocked_same_day_duplicate_buy | 0.0279% | `2311` buy 1주가 same-day filled돼 materials sleeve add를 더 늘리지 않는다 |
| NKE | blocked_same_day_duplicate_buy | 0.0221% | `2331` buy 1주가 same-day filled돼 duplicate buy gate 적용 |
| NEE | blocked_same_day_duplicate_buy | 0.0116% | `2351` buy 1주가 same-day filled돼 utilities sleeve duplicate buy gate 적용 |
| AMZN | selected_buy | 0.0208% | research preflight coverage 유지, duplicate/open-order conflict 없음, current invested ratio가 acceleration threshold 아래 |
| GOOGL | blocked_spread | 1.4309% | live ask outlier로 spread cap `0.50%` 초과 |
| SPY | blocked_validation_floor_cap | 0.0027% | 1주 ask `749.27 USD`가 validation floor per-order cap 약 `506.15 USD`를 초과 |
| QQQ | blocked_validation_floor_cap | 0.0492% | 1주 ask `732.06 USD`가 validation floor per-order cap 약 `506.15 USD`를 초과 |
| NOK | blocked_validation_lifecycle_add_block | n/a | review-due add-block 유지 |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| SO | watch | `sell_metric_gap` | trim expected-excess/replacement margin metric 공백 지속 |
| RGTI | watch | `duplicate_symbol_side_same_day` | spread는 정상이나 same-day after-hours trim fill 때문에 regular-session 추가 sell 차단 |
| PFE | watch | `duplicate_symbol_side_same_day` | same US-date after-hours trim fill 1건 뒤라 regular-session 추가 sell 비허용 |

## 주문/체결

- Planned order: `AMZN` buy `1` @ `240.45 USD` day limit
- `place_stock_order`: `AMZN` buy 1주, `client_order_id=hourly-20260618-0011-buy-amzn`, `order_id=fcc7c8b1-d8e5-4598-970d-b865a63bba35`
- Immediate reconciliation: `get_order_by_client_id` 기준 `status=new`, `filled_qty=0`, `filled_avg_price=null`
- Open orders after submit: `AMZN` buy open order 1건만 남아 있다
- Same US-date fills before submit: `NEE` buy 1주 `86.38 USD`, `NKE` buy 1주 `45.30 USD`, `FCX` buy 1주 `71.40 USD`, `WMT` buy 1주 `119.83 USD`, `BAC` buy 1주 `57.57 USD`, prior after-hours `PFE` sell 1주 `26.03 USD`, `RGTI` sell 1주 `20.96 USD`

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | 62 symbols, SPY/QQQ 포함 |
| `check-mcp-coverage.py --strict --json` | PASS | Alpaca core pass, positive research 3개 |
| `check-risk-policy.py --json` | PASS | staged deployment warning only |

## 산출물

- Report: `wiki/current-runs/daily/2026-06-18-0011-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-18-0011-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-18-0011-hourly-autopilot.json`
- Runtime gate evaluation: `wiki/evidence-store/sources/2026-06-18-0011-hourly-autopilot-runtime-gate-evaluation.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-18-0011-hourly-autopilot-post-trade.json`

## 지표 설명

- `blocked_same_day_duplicate_buy`: 같은 미국 거래일에 이미 filled된 동일 symbol buy가 있으면 regular-session 추가 buy를 만들지 않는다.
- `validation floor per-order cap`: floor-size learning buy도 `portfolio_value * 0.5%` 상한을 넘을 수 없다. 이번 cycle cap은 약 `506.15 USD`라 `SPY/QQQ` 1주가 초과했다.
- `tiered MCP gate`: core `alpaca` pass와 research positive confirmation `3개` 이상이면 Alpha/Firecrawl 비핵심 gap이 있어도 submit을 막지 않는다.

## 사후 정합성

- Immediate post-trade account: cash `30,011.30 USD`, portfolio value `101,278.97 USD`, buying power `303,689.81 USD`
- Open orders: `AMZN` buy 1주 `240.45 USD` day limit만 `status=new`
- Position continuity: `AMZN qty=7`, `avg_entry_price=256.778571`, `current_price=240.475`
