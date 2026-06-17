# 2026-06-17-2311-hourly-autopilot scheduled paper autopilot

## 요약

`2311` scheduled hourly-autopilot은 scheduler-owned stale cleanup/core/research preflight를 source-of-record로 사용했다. preflight clock `2026-06-17T10:11:08.054383916-04:00`, account `ACTIVE`, positions `33`, open orders `0`, fresh quote rows는 decision time 기준 20분 이내라 Alpaca core hard gate를 PASS 처리했다. Research tiered gate도 `SEC EDGAR/FRED/Yahoo Finance` pass로 strict submit threshold `3` confirmations를 유지했고, `Alpha Vantage`는 one-call-per-hour throttle에 따른 `provider_error` gap, `Firecrawl`은 credits 부족 `unknown` gap only로 유지했다.

live Alpaca continuity에서는 직전 `2251`의 `WMT` buy 1주가 `2026-06-17T14:07:50.521793Z`에 `119.83 USD`로 이미 filled 됐음을 재확인했다. sell-first 재평가에서는 `SO`가 trim decision-grade metric gap, `RGTI`와 `PFE`가 같은 미국 거래일 after-hours trim fill에 따른 duplicate symbol/side gate로 executable trim이 없었다. buy fallback에서는 `BAC`와 `WMT`가 same-day filled buy duplicate로 탈락했고, `FCX`가 materials/copper diversifier floor-size learning order로 가장 executable한 후보가 됐다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env` 기준 `ALPACA_PAPER_TRADE=true` |
| Market clock | PASS | live `get_clock` `2026-06-17T10:19:14.368668829-04:00`, regular market open |
| Stale order lifecycle | PASS | `2311` stale cleanup artifact 기준 stale candidates/open orders 모두 0 |
| Alpaca core MCP | PASS | scheduler core preflight hard gate `pass`, live continuity 기준 open orders `0` and WMT fill continuity |
| Research MCP | PASS tiered | SEC EDGAR/FRED/Yahoo positive 3개, Alpha throttle gap, Firecrawl credit gap |
| Universe strict | PASS | broad metadata universe `62`개, SPY/QQQ 포함 |
| Review backlog throttle | PASS for buy | `pending_1d_count=0`, `blocked_add_symbols=['NOK']` |
| Quote/spread | PASS for FCX | live FCX quote `71.36/71.40`, spread `0.0561%`, freshness pass |
| Risk plan | PASS | `check-risk-policy.py --json` 기준 FCX 1주 buy risk gate 통과 |
| Final submit path | PASS | same-day duplicate/open-order 0, whole-share day-limit stock, order submitted |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| SO | blocked_sell_metric_gap | 0.0533% | quote/spread는 통과했지만 trim decision-grade expected-excess/replacement margin 공백 지속 |
| RGTI | blocked_same_day_duplicate_sell | 0.0485% | speculative trim trigger와 spread는 pass지만 same US-date after-hours sell fill이 있어 duplicate sell gate 유지 |
| PFE | blocked_same_day_duplicate_sell | 0.0383% | repeated weak-review trim rationale와 quote/spread는 pass지만 같은 미국 거래일 after-hours sell fill이 있어 regular-session 추가 sell 차단 |
| BAC | blocked_same_day_duplicate_buy | 0.0173% | `2231` buy 1주가 same US-date에 이미 filled돼 regular-session duplicate buy로 재진입 불가 |
| WMT | blocked_same_day_duplicate_buy | 0.0250% | `2251` buy 1주가 `10:07 ET`에 filled돼 same-day duplicate buy gate 적용 |
| FCX | selected_buy | 0.0561% | latest 1D closeout 양호, materials/copper diversifier, 3-provider positive confirmation, duplicate/open-order conflict 없음 |
| COP | lower_rank_backup | 0.0814% | energy/value diversifier로 usable하지만 latest review strength가 FCX보다 약함 |
| NKE | lower_rank_backup | 0.0222% | consumer turnaround candidate지만 current tape/portfolio contribution이 FCX보다 열세 |
| QQQ | blocked_validation_floor_cap | 0.0082% | 1주 ask `733.16 USD`가 validation floor per-order cap을 초과 |
| NOK | blocked_validation_lifecycle_add_block | 0.0721% | review-due add-block 유지 |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| SO | watch | `sell_metric_gap` | trim expected-excess/replacement margin metric 공백 지속 |
| RGTI | watch | `duplicate_symbol_side_same_day` | spread는 정상화됐지만 same-day after-hours trim fill 때문에 regular-session 추가 sell 차단 |
| PFE | watch | `duplicate_symbol_side_same_day` | same US-date after-hours trim fill 1건 뒤라 regular-session 추가 sell 비허용 |

## 주문/체결

- Planned order: `FCX` buy `1` @ `71.40 USD` day limit
- `place_stock_order`: `FCX` buy 1주, `client_order_id=hourly-20260617-2311-buy-fcx`, `order_id=1ffe1486-ed10-4b4c-9ec9-690600d04970`
- Immediate reconciliation: `get_order_by_client_id` 기준 상태는 `new`, `filled_qty=0`, `filled_avg_price=null`이다.
- Open orders after submit: `FCX` buy 1건 `status=new`
- Same US-date fills seen before submit: `WMT` buy 1주 `119.83 USD`, `BAC` buy 1주 `57.57 USD`, prior after-hours `PFE` sell 1주 `26.03 USD`, `RGTI` sell 1주 `20.96 USD`
- Post-trade position check: pre-submit 기준 `FCX qty=6`, `avg_entry_price=65.675`, account cash `30,214.38 USD`, portfolio value `101,221.44 USD`, buying power `304,059.59 USD`

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | 62 symbols, SPY/QQQ 포함 |
| `check-mcp-coverage.py --strict --json` | PASS | Alpaca core pass, positive research 3개, Alpha/Firecrawl non-core gaps |
| `check-risk-policy.py --json` | PASS | FCX 1주 buy notional `71.40 USD`; staged deployment warning only |

## 산출물

- Report: `wiki/current-runs/daily/2026-06-17-2311-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-17-2311-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-17-2311-hourly-autopilot.json`
- Runtime gate evaluation: `wiki/evidence-store/sources/2026-06-17-2311-hourly-autopilot-runtime-gate-evaluation.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-17-2311-hourly-autopilot-post-trade.json`

## 지표 설명

- `duplicate_symbol_side_same_day`: 동일 미국 거래일에 이미 체결된 같은 symbol/side 주문이 있으면 learning order라도 재진입하지 않는다.
- `validation floor per-order cap`: floor-size learning buy도 `portfolio_value * 0.5%` 상한을 넘을 수 없다. 이번 cycle cap은 약 `506.11 USD`라 `QQQ` 1주가 초과했다.
- `tiered MCP gate`: core `alpaca` pass와 research positive confirmation `3개` 이상이면 Alpha/Firecrawl 비핵심 gap이 있어도 submit을 막지 않는다.
