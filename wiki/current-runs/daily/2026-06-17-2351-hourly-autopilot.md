# 2026-06-17-2351-hourly-autopilot scheduled paper autopilot

## 요약

`2351` scheduled hourly-autopilot은 scheduler-owned stale cleanup/core/research preflight를 source-of-record로 사용했다. preflight clock `2026-06-17T10:51:10.734240278-04:00`, account `ACTIVE`, positions `33`, open orders `0`, fresh quote rows는 decision time 기준 20분 이내라 Alpaca core hard gate를 PASS 처리했다. Research tiered gate도 `SEC EDGAR/FRED/Yahoo Finance` pass로 strict submit threshold `3` confirmations를 유지했고, `Alpha Vantage`는 `empty_response`, `Firecrawl`은 credits 부족 `unknown` gap only로 유지했다.

live Alpaca continuity에서는 `2331`의 `NKE` buy 1주가 `2026-06-17T14:47:16.442937Z`에 `45.30 USD`로 filled 전환됐고 open orders는 `0`건임을 먼저 재확인했다. sell-first 재평가에서는 `SO`가 trim decision-grade metric gap, `RGTI`와 `PFE`가 같은 미국 거래일 after-hours trim fill에 따른 duplicate symbol/side gate로 executable trim이 없었다. buy fallback에서는 `BAC/WMT/FCX/NKE`가 same-day duplicate buy로 탈락했고, `SPY/QQQ`는 validation floor per-order cap을 초과했으며 `PLTR`는 spread fail이었다. `NEE`는 FRED-confirmed utilities/rate-sensitive diversifier로 recent `2026-06-17` portfolio review가 `중립 양호`, live quote `86.50/86.52`, spread `0.0231%`, duplicate/open-order conflict 없음 조건을 충족해 floor-size learning buy 1주 후보로 승격했다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env` 기준 `ALPACA_PAPER_TRADE=true` |
| Market clock | PASS | live `get_clock` `2026-06-17T10:53:49.227409233-04:00`, regular market open |
| Stale order lifecycle | PASS | `2351` stale cleanup artifact 기준 stale candidates 0, remaining open orders 0 |
| Alpaca core MCP | PASS | scheduler core preflight hard gate `pass`, live continuity 기준 open orders `0`, watchlists `0`, account `ACTIVE` |
| Research MCP | PASS tiered | SEC EDGAR/FRED/Yahoo positive 3개, Alpha empty-response gap, Firecrawl credit gap |
| Universe strict | PASS | broad metadata universe `62`개, SPY/QQQ 포함 |
| Review backlog throttle | PASS for buy | `pending_1d_count=0`, `blocked_add_symbols=['NOK']` |
| Quote/spread | PASS for NEE | live NEE quote `86.50/86.52`, spread `0.0231%`, freshness pass |
| Risk plan | PASS | `check-risk-policy.py --json` 기준 NEE 1주 buy risk gate 통과 |
| Final submit path | PASS | same-day duplicate/open-order check for `NEE` pass, whole-share day-limit stock, order submitted and filled |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| SO | blocked_sell_metric_gap | 0.0320% | quote/spread는 통과했지만 trim decision-grade expected-excess/replacement margin 공백 지속 |
| RGTI | blocked_same_day_duplicate_sell | 0.0958% | speculative trim trigger와 spread는 pass지만 same US-date after-hours sell fill이 있어 duplicate sell gate 유지 |
| PFE | blocked_same_day_duplicate_sell | 0.0382% | repeated weak-review trim rationale와 quote/spread는 pass지만 same US-date after-hours sell fill이 있어 regular-session 추가 sell 차단 |
| BAC | blocked_same_day_duplicate_buy | 0.0173% | `2231` buy 1주가 same US-date에 이미 filled돼 regular-session duplicate buy 재진입 불가 |
| WMT | blocked_same_day_duplicate_buy | 0.0334% | `2251` buy 1주가 same-day filled라 duplicate buy gate 적용 |
| FCX | blocked_same_day_duplicate_buy | n/a | `2311` buy 1주가 `14:40:58Z`에 filled돼 same-day energy sleeve 추가 buy는 보류 |
| NKE | blocked_same_day_duplicate_buy | 0.0221% | `2331` buy 1주가 `14:47:16Z`에 filled돼 duplicate buy gate 적용 |
| NEE | selected_buy | 0.0231% | FRED-confirmed utilities diversifier, recent 중립 양호 review, duplicate/open-order conflict 없음 |
| AMZN | backup | 0.0208% | quote/spread는 양호하지만 mega-cap 추가노출과 recent weak-review history로 NEE보다 후순위 |
| GOOGL | backup | 0.0192% | quote/spread는 양호하지만 mega-cap existing exposure와 review history로 NEE보다 후순위 |
| SPY | blocked_validation_floor_cap | 0.0067% | 1주 ask `750.10 USD`가 validation floor per-order cap을 초과 |
| QQQ | blocked_validation_floor_cap | 0.0137% | 1주 ask `732.57 USD`가 validation floor per-order cap을 초과 |
| NOK | blocked_validation_lifecycle_add_block | n/a | review-due add-block 유지 |
| PLTR | blocked_spread | 3.0671% | live quote spread가 policy cap `0.50%`를 크게 초과 |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| SO | watch | `sell_metric_gap` | trim expected-excess/replacement margin metric 공백 지속 |
| RGTI | watch | `duplicate_symbol_side_same_day` | spread는 정상이나 same-day after-hours trim fill 때문에 regular-session 추가 sell 차단 |
| PFE | watch | `duplicate_symbol_side_same_day` | same US-date after-hours trim fill 1건 뒤라 regular-session 추가 sell 비허용 |

## 주문/체결

- Planned order: `NEE` buy `1` @ `86.52 USD` day limit
- `place_stock_order`: `NEE` buy 1주, `client_order_id=hourly-20260617-2351-buy-nee`, `order_id=4d8da69a-fd1d-4911-a410-d9df759a6217`
- Immediate reconciliation: `get_order_by_client_id` 기준 `2026-06-17T14:59:48.76418374Z`에 `filled_avg_price=86.38 USD`, `filled_qty=1`, `status=filled`
- Open orders after submit: 없음
- Same US-date fills after submit: `NEE` buy 1주 `86.38 USD`, `NKE` buy 1주 `45.30 USD`, `FCX` buy 1주 `71.40 USD`, `WMT` buy 1주 `119.83 USD`, `BAC` buy 1주 `57.57 USD`, prior after-hours `PFE` sell 1주 `26.03 USD`, `RGTI` sell 1주 `20.96 USD`
- Post-trade position check: `NEE qty=7`, `avg_entry_price=86.337143`, `current_price=86.39`, account cash `30,011.30 USD`, portfolio value `101,196.67 USD`, buying power `303,729.65 USD`

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | 62 symbols, SPY/QQQ 포함, shortlist 10개 |
| `check-mcp-coverage.py --strict --json` | PASS | Alpaca core pass, positive research 3개, Alpha/Firecrawl non-core gaps |
| `check-risk-policy.py --json` | PASS | NEE 1주 buy notional `86.52 USD`; staged deployment warning only |

## 산출물

- Report: `wiki/current-runs/daily/2026-06-17-2351-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-17-2351-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-17-2351-hourly-autopilot.json`
- Runtime gate evaluation: `wiki/evidence-store/sources/2026-06-17-2351-hourly-autopilot-runtime-gate-evaluation.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-17-2351-hourly-autopilot-post-trade.json`

## 지표 설명

- `blocked_same_day_duplicate_buy`: 같은 미국 거래일에 이미 filled된 동일 symbol buy가 있으면 regular-session 추가 buy를 만들지 않는다.
- `validation floor per-order cap`: floor-size learning buy도 `portfolio_value * 0.5%` 상한을 넘을 수 없다. 이번 cycle cap은 약 `506.70 USD`라 `SPY/QQQ` 1주가 초과했다.
- `tiered MCP gate`: core `alpaca` pass와 research positive confirmation `3개` 이상이면 Alpha/Firecrawl 비핵심 gap이 있어도 submit을 막지 않는다.
