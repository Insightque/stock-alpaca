# 2026-06-18-0231-hourly-autopilot scheduled paper autopilot

## 요약

`0231` scheduled hourly-autopilot은 scheduler-owned stale cleanup/core/research preflight를 source-of-record로 사용했다. preflight hard gate는 `pass`였고 direct Alpaca continuity 기준 `2026-06-17T13:34:38.208782785-04:00` regular market open, account `ACTIVE`, open orders `0`, watchlists `0`, same US-date buy fill stack(`SO/COP/GOOGL/AAPL/XOM/MSFT/AMZN/NEE/NKE/FCX/WMT/BAC`)과 prior after-hours sell fill(`PFE/RGTI`)을 재확인했다. Research tiered gate도 `SEC EDGAR/FRED/Yahoo Finance` pass로 strict submit threshold `3` confirmations를 유지했고, `Alpha Vantage`는 `empty_response`, `Firecrawl`은 credit 부족 `unknown` gap only로 남겼다.

sell-first 재평가에서는 `SO`가 이번 미국 거래일 `0211` validation buy 체결 때문에 `require_no_same_day_buy_for_trim`에 막혔고 trim decision-grade metric gap도 그대로였다. `RGTI`와 `PFE`는 same US-date after-hours trim fill 때문에 duplicate symbol/side gate가 유지돼 executable trim이 없었다. buy fallback에서는 `AMZN/BAC/WMT/NKE/NEE/SO/COP/GOOGL/AAPL/XOM/MSFT/FCX`가 same-day filled buy duplicate, `SPY/QQQ`가 validation floor cap 초과, `INTC/AVGO`가 ai_semiconductor warning band, `PLTR/HOOD`가 source-confidence 또는 thesis-quality 제약으로 탈락했다. 남은 preflight-covered existing holding 중 `[[SLB]]`는 live quote `51.32/51.33`, spread `0.0195%`, active tradable NYSE stock, energy-services diversifier 역할, review backlog throttle 비차단, 3-provider positive research confirmation을 유지해 floor-size learning buy 후보로 승격됐고, `51.33 USD` day limit 1주가 `filled_avg_price=51.32 USD`로 즉시 체결됐다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env` 기준 `ALPACA_PAPER_TRADE=true` |
| Market clock | PASS | live `get_clock` `2026-06-17T13:34:38.208782785-04:00`, regular market open |
| Stale order lifecycle | PASS | `0231` stale cleanup artifact 기준 stale candidates `0`, remaining open orders `0` |
| Alpaca core MCP | PASS | scheduler core preflight hard gate `pass`, direct continuity 기준 open orders `0`, account `ACTIVE`, watchlists `0` |
| Research MCP | PASS tiered | SEC EDGAR/FRED/Yahoo positive 3개, Alpha `empty_response` gap, Firecrawl `unknown` gap |
| Universe strict | PASS | broad metadata universe `62`개, SPY/QQQ 포함 |
| Review backlog throttle | PASS for buy | `pending_1d_count=0`, `blocked_add_symbols=['NOK']` |
| Quote/spread | PASS for SLB | live quote `51.32/51.33`, spread `0.0195%`, freshness pass |
| Risk plan | PASS | `check-risk-policy.py --json` 기준 SLB 1주 buy risk gate 통과 |
| Final submit path | PASS | same-day duplicate/open-order check pass, whole-share day-limit stock, order filled |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| SO | blocked_same_day_buy_for_trim | 0.0215% | `0211` same-day buy fill과 trim metric gap이 겹쳐 regular-session trim 승격 불가 |
| RGTI | blocked_same_day_duplicate_sell | 0.0470% | speculative trim trigger와 spread는 pass지만 same US-date after-hours trim fill 때문에 추가 sell 차단 |
| PFE | blocked_same_day_duplicate_sell | 0.0383% | repeated weak-review trim rationale와 quote/spread는 pass지만 same US-date after-hours trim fill 때문에 추가 sell 차단 |
| AMZN | blocked_same_day_duplicate_buy | n/a | `0011` buy 1주가 same US-date에 이미 filled |
| BAC | blocked_same_day_duplicate_buy | n/a | `2231` buy 1주가 same US-date에 이미 filled |
| WMT | blocked_same_day_duplicate_buy | n/a | `2251` buy 1주가 same US-date에 이미 filled |
| NKE | blocked_same_day_duplicate_buy | n/a | `2331` buy 1주가 same US-date에 이미 filled |
| NEE | blocked_same_day_duplicate_buy | n/a | `2351` buy 1주가 same US-date에 이미 filled |
| SO | blocked_same_day_duplicate_buy | n/a | `0211` buy 1주가 same US-date에 이미 filled |
| COP | blocked_same_day_duplicate_buy | n/a | `0151` buy 1주가 same US-date에 이미 filled |
| GOOGL | blocked_same_day_duplicate_buy | n/a | `0131` buy 1주가 same US-date에 이미 filled |
| AAPL | blocked_same_day_duplicate_buy | n/a | `0111` buy 1주가 same US-date에 이미 filled |
| XOM | blocked_same_day_duplicate_buy | n/a | `0051` buy 1주가 same US-date에 이미 filled |
| MSFT | blocked_same_day_duplicate_buy | n/a | `0031` buy 1주가 same US-date에 이미 filled |
| FCX | blocked_same_day_duplicate_buy | n/a | `2311` buy 1주가 same US-date에 이미 filled |
| SPY | blocked_validation_floor_cap | 0.0040% | 1주 ask `749.21 USD`가 validation floor per-order cap 약 `506.55 USD`를 초과 |
| QQQ | blocked_validation_floor_cap | 0.0041% | 1주 ask `732.11 USD`가 validation floor per-order cap 약 `506.55 USD`를 초과 |
| INTC | blocked_ai_semiconductor_warning_band | 0.0164% | ai_semiconductor theme/factor/cluster warning band 위라 relaxed floor-size buy 승격 중단 |
| AVGO | blocked_ai_semiconductor_warning_band | n/a | same ai_semiconductor complex warning band와 post-earnings risk watch 지속 |
| PLTR | blocked_low_source_confidence | n/a | existing thesis note의 source confidence가 낮아 relaxed floor-size buy 허용 범위를 벗어남 |
| HOOD | blocked_medium_source_confidence_speculative | n/a | speculative high-beta sleeve에서 thesis evidence와 portfolio-fit 우선순위가 낮음 |
| SLB | selected_buy | 0.0195% | same-day duplicate/open-order conflict 없고 3-provider positive confirmation 유지한 existing energy-services fallback |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| SO | watch | `same_day_buy_for_trim` | 0211 same-day buy fill이 있어 이번 cycle regular-session trim을 열지 않는다. trim metric gap도 남아 있다. |
| RGTI | watch | `duplicate_symbol_side_same_day` | spread는 정상이나 same-day after-hours trim fill 때문에 regular-session 추가 sell 차단 |
| PFE | watch | `duplicate_symbol_side_same_day` | same US-date after-hours trim fill 뒤라 regular-session 추가 sell 비허용 |

## 주문/체결

### 제출 전 게이트 요약

paper mode `true`; market clock `2026-06-17T13:34:38.208782785-04:00`; order plan path `wiki/trade-ledger/orders/2026-06-18-0231-hourly-autopilot.json`; universe strict `PASS`; MCP strict `PASS`; risk validator `PASS`; SLB quote freshness `~0m`; spread `0.0195%`; order shape `buy 1 share / limit 51.33 / day / stock / regular`; duplicate/open-order check `PASS`; source refs는 `0231` stale cleanup/core/research preflight, runtime gate evaluation, `review-due-index`, `2026-06-17-portfolio-review`, `[[SLB]]`, `[[SO]]`, `[[RGTI]]`, `[[PFE]]`, `[[PLTR]]`다.

| Symbol | Side | Qty | Limit | Status | Filled Avg | Order ID |
| --- | --- | ---: | ---: | --- | ---: | --- |
| SLB | buy | 1 | 51.33 | filled | 51.32 | `2fde0559-07b0-4b3a-aa61-282927e1a64a` |

## Reconciliation

same `client_order_id` readback 기준 `SLB` 주문은 `2026-06-17T17:39:03.382610403Z`에 `filled_avg_price=51.32 USD`로 즉시 체결됐다. live `get_orders(status=open)` 기준 open orders는 `0`건이다. same-day `get_orders(status=all, after=2026-06-16T20:00:00-04:00)` readback에서는 이번 `SLB` fill에 더해 `SO/COP/GOOGL/AAPL/XOM/MSFT/AMZN/NEE/NKE/FCX/WMT/BAC` buy 12건과 prior after-hours `PFE/RGTI` sell 두 건이 유지됐다. direct `get_account_info/get_all_positions` 기준 account `ACTIVE`, cash `28,324.87 USD`, portfolio value `101,389.38 USD`, buying power `302,037.29 USD`, positions `33`건, `SLB qty=8`, `avg_entry_price=55.0625`, `current_price=51.315`, `SO qty=6`, `PLTR qty=3`로 반영됐다.

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | 62 symbols, pre-shortlist 10, SPY/QQQ 포함 |
| `check-mcp-coverage.py --strict --json` | PASS | Alpaca core pass, positive research 3개 |
| `check-risk-policy.py --json` | PASS | staged deployment warning only |

## 산출물

- Report: `wiki/current-runs/daily/2026-06-18-0231-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-18-0231-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-18-0231-hourly-autopilot.json`
- Runtime gate evaluation: `wiki/evidence-store/sources/2026-06-18-0231-hourly-autopilot-runtime-gate-evaluation.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-18-0231-hourly-autopilot-post-trade.json`

## 지표 설명

- `blocked_same_day_duplicate_buy`: 같은 미국 거래일에 이미 filled된 동일 symbol buy는 regular-session에서 다시 만들지 않는다.
- `blocked_same_day_buy_for_trim`: 같은 미국 거래일에 같은 symbol buy가 방금 체결되면 trim/exit 재평가는 다음 cycle로 넘긴다.
- `validation floor per-order cap`: floor-size learning buy도 `portfolio_value * 0.5%` 상한을 넘을 수 없다. 이번 cycle cap은 약 `506.55 USD`다.
- `tiered MCP gate`: core `alpaca` pass와 research positive confirmation `3개` 이상이면 Alpha/Firecrawl 비핵심 gap이 있어도 submit을 막지 않는다.
- `ai_semiconductor warning band`: theme/factor/cluster 경고 비중 위에서는 high-conviction이 아닌 새 buy를 제한한다.
