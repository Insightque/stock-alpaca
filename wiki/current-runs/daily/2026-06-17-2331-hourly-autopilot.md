# 2026-06-17-2331-hourly-autopilot scheduled paper autopilot

## 요약

`2331` scheduled hourly-autopilot은 scheduler-owned stale cleanup/core/research preflight를 source-of-record로 사용했다. preflight clock `2026-06-17T10:31:11.518683923-04:00`, account `ACTIVE`, positions `33`, open orders `1`(fresh `FCX` buy), fresh quote rows는 decision time 기준 20분 이내라 Alpaca core hard gate를 PASS 처리했다. Research tiered gate도 `SEC EDGAR/FRED/Yahoo Finance` pass로 strict submit threshold `3` confirmations를 유지했고, `Alpha Vantage`는 one-call-per-hour throttle `provider_error`, `Firecrawl`은 credits 부족 `unknown` gap only로 유지했다.

live Alpaca continuity에서는 `2311`의 `FCX` buy 1주가 여전히 `status=new` open order로 남아 있음을 먼저 재확인했다. sell-first 재평가에서는 `SO`가 trim decision-grade metric gap, `RGTI`와 `PFE`가 같은 미국 거래일 after-hours trim fill에 따른 duplicate symbol/side gate로 executable trim이 없었다. buy fallback에서는 `FCX`가 same symbol/side open-order gate, `COP`가 same correlated-cluster open-order gate, `BAC/WMT`가 same-day filled buy duplicate로 탈락했고, `NKE`가 different-cluster consumer turnaround floor-size learning order로 가장 executable한 후보가 됐다.

post-trade reconciliation에서는 새 `NKE` buy 1주가 immediate `status=new` open order로 남았고, 동시에 직전 cycle의 `FCX` buy 1주가 `2026-06-17T14:40:58.679036Z`에 `71.40 USD`로 filled 전환된 점을 확인했다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env` 기준 `ALPACA_PAPER_TRADE=true` |
| Market clock | PASS | live `get_clock` `2026-06-17T10:33:32.244239361-04:00`, regular market open |
| Stale order lifecycle | PASS | `2331` stale cleanup artifact 기준 stale candidates 0, open order `FCX` 1건은 fresh/non-stale |
| Alpaca core MCP | PASS | scheduler core preflight hard gate `pass`, live continuity 기준 open orders `1`, watchlists `0`, account `ACTIVE` |
| Research MCP | PASS tiered | SEC EDGAR/FRED/Yahoo positive 3개, Alpha throttle gap, Firecrawl credit gap |
| Universe strict | PASS | broad metadata universe `62`개, SPY/QQQ 포함 |
| Review backlog throttle | PASS for buy | `pending_1d_count=0`, `blocked_add_symbols=['NOK']` |
| Quote/spread | PASS for NKE | scheduler NKE quote `45.29/45.30`, spread `0.0221%`, freshness pass |
| Risk plan | PASS | `check-risk-policy.py --json` 기준 NKE 1주 buy risk gate 통과 |
| Final submit path | PASS | same-day duplicate/open-order check for `NKE` pass, whole-share day-limit stock, order submitted |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| SO | blocked_sell_metric_gap | 0.0427% | quote/spread는 통과했지만 trim decision-grade expected-excess/replacement margin 공백 지속 |
| RGTI | blocked_same_day_duplicate_sell | 0.0962% | speculative trim trigger와 spread는 pass지만 same US-date after-hours sell fill이 있어 duplicate sell gate 유지 |
| PFE | blocked_same_day_duplicate_sell | 0.0383% | repeated weak-review trim rationale와 quote/spread는 pass지만 같은 미국 거래일 after-hours sell fill이 있어 regular-session 추가 sell 차단 |
| FCX | blocked_same_symbol_side_open_order | 0.0557% | decision 시점에는 `2311` FCX buy open order가 fresh `status=new`라 same symbol/side 신규 buy 금지 |
| COP | blocked_same_cluster_open_order | 5.2442% | `FCX` open buy와 같은 `energy_commodity` cluster이며 spread도 policy cap 초과 |
| BAC | blocked_same_day_duplicate_buy | 0.0173% | `2231` buy 1주가 same US-date에 이미 filled돼 regular-session duplicate buy 재진입 불가 |
| WMT | blocked_same_day_duplicate_buy | 0.0334% | `2251` buy 1주가 `10:07 ET`에 filled돼 same-day duplicate buy gate 적용 |
| NKE | selected_buy | 0.0221% | recent 1D 양호, consumer turnaround different-cluster fallback, 3-provider positive confirmation, duplicate/open-order conflict 없음 |
| QQQ | blocked_validation_floor_cap | 0.0341% | 1주 ask `734.06 USD`가 validation floor per-order cap을 초과 |
| NOK | blocked_validation_lifecycle_add_block | n/a | review-due add-block 유지 |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| SO | watch | `sell_metric_gap` | trim expected-excess/replacement margin metric 공백 지속 |
| RGTI | watch | `duplicate_symbol_side_same_day` | spread는 정상이나 same-day after-hours trim fill 때문에 regular-session 추가 sell 차단 |
| PFE | watch | `duplicate_symbol_side_same_day` | same US-date after-hours trim fill 1건 뒤라 regular-session 추가 sell 비허용 |

## 주문/체결

- Planned order: `NKE` buy `1` @ `45.30 USD` day limit
- `place_stock_order`: `NKE` buy 1주, `client_order_id=hourly-20260617-2331-buy-nke`, `order_id=3f5cd1a0-cd69-48a6-8380-f9042cffd668`
- Immediate reconciliation: `get_order_by_client_id` 기준 상태는 `new`, `filled_qty=0`, `filled_avg_price=null`이다.
- Open orders after submit: `NKE` buy 1건 `status=new`
- Same US-date fills seen after submit: `FCX` buy 1주 `71.40 USD`, `WMT` buy 1주 `119.83 USD`, `BAC` buy 1주 `57.57 USD`, prior after-hours `PFE` sell 1주 `26.03 USD`, `RGTI` sell 1주 `20.96 USD`
- Post-trade position check: `NKE qty=6`, `avg_entry_price=45.228333`, `FCX qty=7`, `avg_entry_price=66.492857`, account cash `30,142.98 USD`, portfolio value `101,124.05 USD`, buying power `303,779.72 USD`

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | 62 symbols, SPY/QQQ 포함, shortlist 10개 |
| `check-mcp-coverage.py --strict --json` | PASS | Alpaca core pass, positive research 3개, Alpha/Firecrawl non-core gaps |
| `check-risk-policy.py --json` | PASS | NKE 1주 buy notional `45.30 USD`; staged deployment warning only |

## 산출물

- Report: `wiki/current-runs/daily/2026-06-17-2331-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-17-2331-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-17-2331-hourly-autopilot.json`
- Runtime gate evaluation: `wiki/evidence-store/sources/2026-06-17-2331-hourly-autopilot-runtime-gate-evaluation.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-17-2331-hourly-autopilot-post-trade.json`

## 지표 설명

- `blocked_same_symbol_side_open_order`: fresh open buy가 있으면 같은 symbol/side 신규 buy는 만들지 않는다.
- `blocked_same_cluster_open_order`: fresh open buy가 있을 때 같은 correlated cluster 신규 buy는 차단하고, 다른 cluster만 허용한다.
- `validation floor per-order cap`: floor-size learning buy도 `portfolio_value * 0.5%` 상한을 넘을 수 없다. 이번 cycle cap은 약 `506.63 USD`라 `QQQ` 1주가 초과했다.
- `tiered MCP gate`: core `alpaca` pass와 research positive confirmation `3개` 이상이면 Alpha/Firecrawl 비핵심 gap이 있어도 submit을 막지 않는다.
