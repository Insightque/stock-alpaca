# 2026-06-18-0031-hourly-autopilot scheduled paper autopilot

## 요약

`0031` scheduled hourly-autopilot은 scheduler-owned stale cleanup/core/research preflight를 source-of-record로 사용했다. preflight clock `2026-06-17T11:31:07.672671195-04:00`, account/positions/open-orders/quotes rows가 모두 pass였고 decision time 기준 20분 이내라 Alpaca core hard gate를 PASS 처리했다. Research tiered gate도 `SEC EDGAR/FRED/Yahoo Finance` pass로 strict submit threshold `3` confirmations를 유지했고, `Alpha Vantage`는 hourly throttle `provider_error`, `Firecrawl`은 credits 부족 `unknown` gap only로 유지했다.

live Alpaca continuity에서는 `0011`의 `AMZN` buy 1주가 `2026-06-17T15:23:00.571840Z`에 `240.44 USD`로 filled 전환됐고 open orders는 `0`건임을 먼저 재확인했다. sell-first 재평가에서는 `SO`가 trim decision-grade metric gap, `RGTI`와 `PFE`가 같은 미국 거래일 after-hours trim fill에 따른 duplicate symbol/side gate로 executable trim이 없었다. buy fallback에서는 `AMZN`을 포함한 same-day filled buy 후보들이 duplicate buy로 탈락했고, `SPY/QQQ`는 validation floor per-order cap을 초과했다. `[[MSFT]]`는 existing mega-cap quality holding이지만 hard gate를 깨지 않고 live quote `384.65/385.42`, spread `0.2000%`, duplicate/open-order conflict 없음, preflight research coverage 유지 조건을 충족해 floor-size learning buy 1주 후보로 승격했다. direct Alpaca MCP submit 이후 same `client_order_id=hourly-20260618-0031-buy-msft` reconciliation 기준 `filled_avg_price=385.40 USD`로 즉시 체결됐다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env` 기준 `ALPACA_PAPER_TRADE=true` |
| Market clock | PASS | live `get_clock` `2026-06-17T11:32:37.864341719-04:00`, regular market open |
| Stale order lifecycle | PASS | `0031` stale cleanup artifact 기준 stale candidates 0, remaining open orders 0 |
| Alpaca core MCP | PASS | scheduler core preflight hard gate `pass`, live continuity 기준 open orders `0`, watchlists `0`, account `ACTIVE` |
| Research MCP | PASS tiered | SEC EDGAR/FRED/Yahoo positive 3개, Alpha throttle gap, Firecrawl credit gap |
| Universe strict | PASS | broad metadata universe `62`개, SPY/QQQ 포함 |
| Review backlog throttle | PASS for buy | `pending_1d_count=0`, `blocked_add_symbols=['NOK']` |
| Quote/spread | PASS for MSFT | live MSFT quote `384.65/385.42`, spread `0.2000%`, freshness pass |
| Risk plan | PASS | `check-risk-policy.py --json` 기준 MSFT 1주 buy risk gate 통과 |
| Final submit path | PASS | same-day duplicate/open-order check for `MSFT` pass, whole-share day-limit stock, order submitted |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| SO | blocked_sell_metric_gap | 0.0321% | quote/spread는 통과했지만 trim decision-grade expected-excess/replacement margin 공백 지속 |
| RGTI | blocked_same_day_duplicate_sell | 0.0478% | speculative trim trigger와 spread는 pass지만 same US-date after-hours sell fill이 있어 duplicate sell gate 유지 |
| PFE | blocked_same_day_duplicate_sell | 0.0382% | repeated weak-review trim rationale와 quote/spread는 pass지만 same US-date after-hours sell fill이 있어 regular-session 추가 sell 차단 |
| AMZN | blocked_same_day_duplicate_buy | 0.0208% | `0011` buy 1주가 same US-date에 이미 filled돼 regular-session duplicate buy 재진입 불가 |
| MSFT | selected_buy | 0.2000% | research preflight coverage 유지, duplicate/open-order conflict 없음, current invested ratio가 acceleration threshold 아래 |
| SPY | blocked_validation_floor_cap | 0.0053% | 1주 ask `750.28 USD`가 validation floor per-order cap 약 `506.47 USD`를 초과 |
| QQQ | blocked_validation_floor_cap | 0.0478% | 1주 ask `732.96 USD`가 validation floor per-order cap 약 `506.47 USD`를 초과 |
| AVGO | blocked_same_theme_warning | 0.1156% | ai_semiconductor warning band와 pending review가 남아 current mega-cap fallback보다 후순위 |
| PLTR | blocked_lower_source_confidence_speculative | 0.0296% | medium source confidence speculative growth profile이라 MSFT보다 후순위 |
| NOK | blocked_validation_lifecycle_add_block | n/a | review-due add-block 유지 |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| SO | watch | `sell_metric_gap` | trim expected-excess/replacement margin metric 공백 지속 |
| RGTI | watch | `duplicate_symbol_side_same_day` | spread는 정상이나 same-day after-hours trim fill 때문에 regular-session 추가 sell 차단 |
| PFE | watch | `duplicate_symbol_side_same_day` | same US-date after-hours trim fill 1건 뒤라 regular-session 추가 sell 비허용 |

## 주문/체결

### 제출 전 게이트 요약

paper mode `true`; market clock `2026-06-17T11:32:37.864341719-04:00`; order plan path `wiki/trade-ledger/orders/2026-06-18-0031-hourly-autopilot.json`; universe strict `PASS`; MCP strict `PASS`; risk validator `PASS`; MSFT quote freshness 약 `0.0`분; spread `0.2000%`; order shape `buy 1 share / limit 385.42 / day / stock / regular`; duplicate/open-order check `PASS`; source refs는 `0031` stale cleanup/core/research preflight, runtime gate evaluation, `review-due-index`, `2026-06-17-portfolio-review`, `[[MSFT]]`다.

| Symbol | Side | Qty | Limit | Status | Filled Avg | Order ID |
| --- | --- | ---: | ---: | --- | ---: | --- |
| MSFT | buy | 1 | 385.42 | filled | 385.40 | `ea46746b-7625-43c6-93b1-75627ea0a0cc` |

## Reconciliation

immediate reconciliation 기준 `get_order_by_client_id`와 `get_orders(status=all, after=2026-06-16T20:00:00-04:00)` 모두 `MSFT` 주문을 `status=filled`, `filled_qty=1`, `filled_avg_price=385.40 USD`로 반환했다. direct `get_orders(status=open)` 기준 open orders는 `0`건이며, `get_account_info/get_all_positions` 기준 account `ACTIVE`, cash `29,385.46 USD`, portfolio value `101,355.71 USD`, positions `33`건, `MSFT qty=4 -> 5`, `avg_entry_price=401.028`로 반영됐다.

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | 62 symbols, SPY/QQQ 포함 |
| `check-mcp-coverage.py --strict --json` | PASS | Alpaca core pass, positive research 3개 |
| `check-risk-policy.py --json` | PASS | staged deployment warning only |

## 산출물

- Report: `wiki/current-runs/daily/2026-06-18-0031-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-18-0031-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-18-0031-hourly-autopilot.json`
- Runtime gate evaluation: `wiki/evidence-store/sources/2026-06-18-0031-hourly-autopilot-runtime-gate-evaluation.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-18-0031-hourly-autopilot-post-trade.json`

## 지표 설명

- `blocked_same_day_duplicate_buy`: 같은 미국 거래일에 이미 filled된 동일 symbol buy가 있으면 regular-session 추가 buy를 만들지 않는다.
- `validation floor per-order cap`: floor-size learning buy도 `portfolio_value * 0.5%` 상한을 넘을 수 없다. 이번 cycle cap은 약 `506.47 USD`다.
- `tiered MCP gate`: core `alpaca` pass와 research positive confirmation `3개` 이상이면 Alpha/Firecrawl 비핵심 gap이 있어도 submit을 막지 않는다.

## 사후 정합성

- Immediate post-trade account: cash `29,385.46 USD`, portfolio value `101,355.71 USD`, buying power `303,339.54 USD`
- Open orders: 없음
- Position continuity: `MSFT qty=5`, `avg_entry_price=401.028`, `current_price=385.38`
