# 2026-06-18-0051-hourly-autopilot scheduled paper autopilot

## 요약

`0051` scheduled hourly-autopilot은 scheduler-owned stale cleanup/core/research preflight를 source-of-record로 사용했다. preflight clock `2026-06-17T11:51:11.141392322-04:00`, account/positions/open-orders/quotes rows가 모두 pass였고 decision time 기준 20분 이내라 Alpaca core hard gate를 PASS 처리했다. Research tiered gate도 `SEC EDGAR/FRED/Yahoo Finance` pass로 strict submit threshold `3` confirmations를 유지했고, `Alpha Vantage`는 hourly throttle `provider_error`, `Firecrawl`은 credits 부족 `unknown` gap only로 유지했다.

live Alpaca continuity에서는 `0031`의 `MSFT` buy 1주가 `2026-06-17T15:37:49.346911019Z`에 `385.40 USD`로 filled 전환됐고 open orders는 `0`건임을 먼저 재확인했다. sell-first 재평가에서는 `SO`가 trim decision-grade metric gap, `RGTI`와 `PFE`가 같은 미국 거래일 after-hours trim fill에 따른 duplicate symbol/side gate로 executable trim이 없었다. buy fallback에서는 `AMZN/MSFT/NEE/NKE/FCX/WMT/BAC`이 same-day filled buy duplicate로 탈락했고, `SPY/QQQ`는 validation floor per-order cap을 초과했다. `[[XOM]]`은 preflight-covered energy diversifier existing holding으로 live quote `141.50/141.54`, spread `0.0283%`, duplicate/open-order conflict 없음, current invested ratio `0.7101`로 acceleration threshold 아래, `2026-06-17` portfolio review의 `1D 중립 양호` 이력을 모두 충족해 floor-size learning buy 1주 후보로 승격했다. direct Alpaca MCP submit 이후 same `client_order_id=hourly-20260618-0051-buy-xom` reconciliation 기준 현재 상태는 `new` open order이며 next cycle lifecycle 추적이 필요하다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env` 기준 `ALPACA_PAPER_TRADE=true` |
| Market clock | PASS | live `get_clock` `2026-06-17T11:53:37.191737697-04:00`, regular market open |
| Stale order lifecycle | PASS | `0051` stale cleanup artifact 기준 stale candidates 0, remaining open orders 0 |
| Alpaca core MCP | PASS | scheduler core preflight hard gate `pass`, live continuity 기준 open orders `0 -> submit 후 1`, watchlists `0`, account `ACTIVE` |
| Research MCP | PASS tiered | SEC EDGAR/FRED/Yahoo positive 3개, Alpha throttle gap, Firecrawl credit gap |
| Universe strict | PASS | broad metadata universe `62`개, SPY/QQQ 포함 |
| Review backlog throttle | PASS for buy | `pending_1d_count=0`, `blocked_add_symbols=['NOK']` |
| Quote/spread | PASS for XOM | live XOM quote `141.50/141.54`, spread `0.0283%`, freshness pass |
| Risk plan | PASS | `check-risk-policy.py --json` 기준 XOM 1주 buy risk gate 통과 |
| Final submit path | PASS | same-day duplicate/open-order check for `XOM` pass, whole-share day-limit stock, order submitted |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| SO | blocked_sell_metric_gap | 0.0321% | quote/spread는 통과했지만 trim decision-grade expected-excess/replacement margin 공백 지속 |
| RGTI | blocked_same_day_duplicate_sell | 0.0475% | speculative trim trigger와 spread는 pass지만 same US-date after-hours sell fill이 있어 duplicate sell gate 유지 |
| PFE | blocked_same_day_duplicate_sell | 0.0381% | repeated weak-review trim rationale와 quote/spread는 pass지만 same US-date after-hours sell fill이 있어 regular-session 추가 sell 차단 |
| AMZN | blocked_same_day_duplicate_buy | 0.0458% | `0011` buy 1주가 same US-date에 이미 filled돼 regular-session duplicate buy 재진입 불가 |
| MSFT | blocked_same_day_duplicate_buy | 0.3262% | `0031` buy 1주가 same US-date에 이미 filled돼 바로 다음 cycle duplicate buy 차단 |
| XOM | selected_buy | 0.0283% | preflight-covered energy diversifier, 1D review `중립 양호`, duplicate/open-order conflict 없음 |
| AAPL | blocked_lower_priority_averaging_down | 0.0134% | latest 1D는 양호했지만 repeated mega-cap averaging-down note 때문에 XOM보다 후순위 |
| GOOGL | blocked_lower_priority_same_cluster_mega_cap | 0.0439% | latest 1D는 양호하지만 mega-cap cluster 내부라 XOM diversifier 이득이 더 큼 |
| NVDA | blocked_same_theme_warning | 0.0146% | ai_semiconductor warning band 때문에 floor-size slot 우선순위에서 밀림 |
| SPY | blocked_validation_floor_cap | 0.0053% | 1주 ask `750.45 USD`가 validation floor per-order cap 약 `506.87 USD`를 초과 |
| QQQ | blocked_validation_floor_cap | 0.0327% | 1주 ask `733.27 USD`가 validation floor per-order cap 약 `506.87 USD`를 초과 |
| PLTR | blocked_lower_source_confidence_speculative | 0.0372% | medium source confidence speculative growth profile이라 XOM보다 후순위 |
| NOK | blocked_validation_lifecycle_add_block | n/a | review-due add-block 유지 |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| SO | watch | `sell_metric_gap` | trim expected-excess/replacement margin metric 공백 지속 |
| RGTI | watch | `duplicate_symbol_side_same_day` | spread는 정상이나 same-day after-hours trim fill 때문에 regular-session 추가 sell 차단 |
| PFE | watch | `duplicate_symbol_side_same_day` | same US-date after-hours trim fill 1건 뒤라 regular-session 추가 sell 비허용 |

## 주문/체결

### 제출 전 게이트 요약

paper mode `true`; market clock `2026-06-17T11:53:37.191737697-04:00`; order plan path `wiki/trade-ledger/orders/2026-06-18-0051-hourly-autopilot.json`; universe strict `PASS`; MCP strict `PASS`; risk validator `PASS`; XOM quote freshness `<1m`; spread `0.0283%`; order shape `buy 1 share / limit 141.54 / day / stock / regular`; duplicate/open-order check `PASS`; source refs는 `0051` stale cleanup/core/research preflight, runtime gate evaluation, `review-due-index`, `2026-06-17-portfolio-review`, `[[XOM]]`다.

| Symbol | Side | Qty | Limit | Status | Filled Avg | Order ID |
| --- | --- | ---: | ---: | --- | ---: | --- |
| XOM | buy | 1 | 141.54 | new | n/a | `9e6b4b81-1307-41aa-b9ac-5c34f7d51793` |

## Reconciliation

immediate reconciliation 기준 `get_order_by_client_id`와 `get_orders(status=open)` 모두 `XOM` 주문을 `status=new`, `filled_qty=0`으로 반환했다. live `get_orders(status=open)` 기준 open orders는 `1`건이며 현재 open order는 `XOM` buy 한 건뿐이다. same US-date fill ledger에는 기존 `MSFT/AMZN/NEE/NKE/FCX/WMT/BAC` buy fills와 prior after-hours `PFE/RGTI` sell fills가 남아 있다. direct `get_account_info/get_all_positions` 기준 account `ACTIVE`, cash `29,385.46 USD`, portfolio value `101,434.09 USD`, positions `33`건, `XOM qty=6`, `avg_entry_price=148.37`, `current_price=141.6101`로 반영됐다.

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | 62 symbols, SPY/QQQ 포함 |
| `check-mcp-coverage.py --strict --json` | PASS | Alpaca core pass, positive research 3개 |
| `check-risk-policy.py --json` | PASS | staged deployment warning only |

## 산출물

- Report: `wiki/current-runs/daily/2026-06-18-0051-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-18-0051-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-18-0051-hourly-autopilot.json`
- Runtime gate evaluation: `wiki/evidence-store/sources/2026-06-18-0051-hourly-autopilot-runtime-gate-evaluation.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-18-0051-hourly-autopilot-post-trade.json`

## 지표 설명

- `blocked_same_day_duplicate_buy`: 같은 미국 거래일에 이미 filled된 동일 symbol buy가 있으면 regular-session 추가 buy를 만들지 않는다.
- `validation floor per-order cap`: floor-size learning buy도 `portfolio_value * 0.5%` 상한을 넘을 수 없다. 이번 cycle cap은 약 `506.87 USD`다.
- `tiered MCP gate`: core `alpaca` pass와 research positive confirmation `3개` 이상이면 Alpha/Firecrawl 비핵심 gap이 있어도 submit을 막지 않는다.

## 사후 정합성

- Immediate post-trade account: cash `29,385.46 USD`, portfolio value `101,434.09 USD`, buying power `303,349.92 USD`
- Open orders: `XOM` buy 1주 `141.54 USD` (`client_order_id=hourly-20260618-0051-buy-xom`) 1건
- Position continuity: `XOM qty=6`, `avg_entry_price=148.37`, `current_price=141.6101`
