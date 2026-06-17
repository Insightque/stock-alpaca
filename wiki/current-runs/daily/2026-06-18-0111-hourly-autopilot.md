# 2026-06-18-0111-hourly-autopilot scheduled paper autopilot

## 요약

`0111` scheduled hourly-autopilot은 scheduler-owned stale cleanup/core/research preflight를 source-of-record로 사용했다. preflight clock `2026-06-17T12:11:10.240512456-04:00`, account/positions/open-orders/quotes rows가 모두 pass였고 decision time 기준 20분 이내라 Alpaca core hard gate를 PASS 처리했다. Research tiered gate도 `SEC EDGAR/FRED/Yahoo Finance` pass로 strict submit threshold `3` confirmations를 유지했고, `Alpha Vantage`는 `empty_response`, `Firecrawl`은 `unknown` gap only로 남겼다.

live Alpaca continuity에서는 직전 `0051`의 `XOM` buy 1주가 submit 시점에는 `status=new` open order였고, 이 때문에 same symbol/cluster energy add는 차단했다. sell-first 재평가에서는 `SO`가 trim decision-grade metric gap, `RGTI`와 `PFE`가 같은 미국 거래일 after-hours trim fill에 따른 duplicate symbol/side gate로 executable trim이 없었다. buy fallback에서는 `SLB`가 same energy cluster open-order gate, `AMZN/MSFT/NEE/NKE/FCX/WMT/BAC`이 same-day filled buy duplicate, `SPY/QQQ`가 floor cap 초과로 탈락했다. `[[AAPL]]`은 preflight-covered mega-cap quality existing holding으로 scheduler quote `298.39/298.43`, spread `0.0134%`, different-cluster open-order 허용, latest `2026-06-17` review의 `1D 중립 양호` 이력을 모두 충족해 floor-size learning buy 1주 후보로 승격했다. submit 후 immediate reconciliation 기준 `AAPL`은 `status=new` open order이고, 같은 readback window에서 `0051`의 `XOM` buy 1주는 `filled_avg_price=141.54 USD`로 뒤늦게 체결 전환됐다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env` 기준 `ALPACA_PAPER_TRADE=true` |
| Market clock | PASS | live `get_clock` `2026-06-17T12:13:29.436265675-04:00`, regular market open |
| Stale order lifecycle | PASS | `0111` stale cleanup artifact 기준 stale candidates 0, remaining open order는 submit 전 fresh `XOM` 1건뿐 |
| Alpaca core MCP | PASS | scheduler core preflight hard gate `pass`, live continuity 기준 open orders `1 -> submit 후 1`, account `ACTIVE`, watchlists `0` |
| Research MCP | PASS tiered | SEC EDGAR/FRED/Yahoo positive 3개, Alpha empty-response gap, Firecrawl unknown gap |
| Universe strict | PASS | broad metadata universe `62`개, SPY/QQQ 포함 |
| Review backlog throttle | PASS for buy | `pending_1d_count=0`, `blocked_add_symbols=['NOK']` |
| Quote/spread | PASS for AAPL | scheduler quote `298.39/298.43`, spread `0.0134%`, freshness pass |
| Risk plan | PASS | `check-risk-policy.py --json` 기준 AAPL 1주 buy risk gate 통과 |
| Final submit path | PASS | same-day duplicate/open-order check for `AAPL` pass, whole-share day-limit stock, order submitted |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| SO | blocked_sell_metric_gap | 0.0322% | quote/spread는 통과했지만 trim decision-grade expected-excess/replacement margin 공백 지속 |
| RGTI | blocked_same_day_duplicate_sell | 0.0475% | speculative trim trigger와 spread는 pass지만 same US-date after-hours trim fill 때문에 regular-session 추가 sell 차단 |
| PFE | blocked_same_day_duplicate_sell | 0.0381% | repeated weak-review trim rationale와 quote/spread는 pass지만 same US-date after-hours trim fill 때문에 regular-session 추가 sell 차단 |
| XOM | blocked_same_symbol_open_order | 0.0212% | submit 시점에는 `0051` buy 1주가 아직 `new` open order라 same symbol/side duplicate gate 유지 |
| SLB | blocked_same_cluster_open_order | 0.0194% | energy-services diversifier 후보지만 fresh `XOM` open order 때문에 같은 `energy_commodity` cluster buy 차단 |
| AMZN | blocked_same_day_duplicate_buy | 0.0125% | `0011` buy 1주가 same US-date에 이미 filled |
| MSFT | blocked_same_day_duplicate_buy | n/a | `0031` buy 1주가 same US-date에 이미 filled |
| AAPL | selected_buy | 0.0134% | preflight-covered mega-cap quality existing holding, latest 1D `중립 양호`, different-cluster open-order 허용 |
| NVDA | blocked_same_theme_warning | 0.0145% | ai_semiconductor warning band 때문에 floor-size slot 우선순위에서 밀림 |
| SPY | blocked_validation_floor_cap | 0.0053% | 1주 ask `750.52 USD`가 validation floor per-order cap 약 `506.69 USD`를 초과 |
| QQQ | blocked_validation_floor_cap | 0.0055% | 1주 ask `733.27 USD`가 validation floor per-order cap 약 `506.69 USD`를 초과 |
| MRK | blocked_missing_wiki_thesis | 0.0259% | quote는 있으나 wiki thesis/trend/risk evidence 페이지 부재 |
| NOK | blocked_validation_lifecycle_add_block | n/a | review-due add-block 유지 |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| SO | watch | `sell_metric_gap` | trim expected-excess/replacement margin metric 공백 지속 |
| RGTI | watch | `duplicate_symbol_side_same_day` | spread는 정상이나 same-day after-hours trim fill 때문에 regular-session 추가 sell 차단 |
| PFE | watch | `duplicate_symbol_side_same_day` | same US-date after-hours trim fill 뒤라 regular-session 추가 sell 비허용 |

## 주문/체결

### 제출 전 게이트 요약

paper mode `true`; market clock `2026-06-17T12:13:29.436265675-04:00`; order plan path `wiki/trade-ledger/orders/2026-06-18-0111-hourly-autopilot.json`; universe strict `PASS`; MCP strict `PASS`; risk validator `PASS`; AAPL quote freshness `~2.05m`; spread `0.0134%`; order shape `buy 1 share / limit 298.43 / day / stock / regular`; duplicate/open-order check `PASS` with existing fresh open order limited to `XOM` only; source refs는 `0111` stale cleanup/core/research preflight, runtime gate evaluation, `review-due-index`, `2026-06-17-portfolio-review`, `[[AAPL]]`, `[[XOM]]`다.

| Symbol | Side | Qty | Limit | Status | Filled Avg | Order ID |
| --- | --- | ---: | ---: | --- | ---: | --- |
| AAPL | buy | 1 | 298.43 | new | n/a | `4c866a2d-25c2-4d1d-9304-f2b23a30f9d2` |

## Reconciliation

immediate reconciliation 기준 `get_order_by_client_id`와 `get_orders(status=open)` 모두 `AAPL` 주문을 `status=new`, `filled_qty=0`으로 반환했다. live `get_orders(status=open)` 기준 open orders는 `1`건이며 현재 open order는 `AAPL` buy 한 건뿐이다. same-day `get_orders(status=all, after=2026-06-16T20:00:00-04:00)` readback에서는 직전 `XOM` buy 1주가 `2026-06-17T16:17:56.544666Z`에 `141.54 USD`로 filled 전환된 것도 확인됐다. direct `get_account_info/get_all_positions` 기준 account `ACTIVE`, cash `29,243.92 USD`, portfolio value `101,357.51 USD`, positions `33`건, `AAPL qty=6`, `avg_entry_price=301.965`, `current_price=298.56`, `XOM qty=7`, `avg_entry_price=147.394286`로 반영됐다.

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | 62 symbols, SPY/QQQ 포함 |
| `check-mcp-coverage.py --strict --json` | PASS | Alpaca core pass, positive research 3개 |
| `check-risk-policy.py --json` | PASS | staged deployment warning only |

## 산출물

- Report: `wiki/current-runs/daily/2026-06-18-0111-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-18-0111-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-18-0111-hourly-autopilot.json`
- Runtime gate evaluation: `wiki/evidence-store/sources/2026-06-18-0111-hourly-autopilot-runtime-gate-evaluation.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-18-0111-hourly-autopilot-post-trade.json`

## 지표 설명

- `blocked_same_symbol_open_order`: 같은 symbol/side의 fresh open order가 있으면 해당 symbol 신규 buy를 추가하지 않는다.
- `blocked_same_cluster_open_order`: fresh open order가 있는 correlated cluster에는 추가 신규 buy를 만들지 않는다.
- `validation floor per-order cap`: floor-size learning buy도 `portfolio_value * 0.5%` 상한을 넘을 수 없다. 이번 cycle cap은 약 `506.69 USD`다.
- `tiered MCP gate`: core `alpaca` pass와 research positive confirmation `3개` 이상이면 Alpha/Firecrawl 비핵심 gap이 있어도 submit을 막지 않는다.

## 지표 설명

- `current invested ratio`: `(portfolio_value - cash) / portfolio_value`로 계산하며 submit 전 cycle은 `0.7100`이었다.
- `different-cluster open-order 허용`: `paper_validation_execution.validation_order_sizing.open_order_policy`에 따라 fresh open order가 있어도 다른 correlated cluster 신규 buy는 lifecycle gate pass 시 허용된다.
