# 2026-06-18-0351-hourly-autopilot scheduled paper autopilot

## 요약

`0351` scheduled hourly-autopilot은 scheduler-owned stale cleanup/core/research preflight를 source-of-record로 사용했다. preflight hard gate는 `pass`였고 regular market은 `2026-06-17T14:51:09.719839643-04:00` 기준 열려 있었다. stale cleanup artifact는 stale candidate `0`, remaining open order `0`이라 `risk_open_order_lifecycle` block이 없었다. research tiered gate도 `SEC EDGAR/FRED/Yahoo Finance` 3개 positive confirmation으로 strict submit threshold를 유지했고, `Alpha Vantage`는 `empty_response`, `Firecrawl`은 credit 부족 `unknown` gap only로 남겼다.

sell-first 재평가에서는 `SO`가 `0211` same-day buy fill 때문에 `require_no_same_day_buy_for_trim`과 trim metric gap에 같이 막혔고, `RGTI`와 `PFE`는 same US-date after-hours trim fill 때문에 duplicate symbol/side gate가 유지돼 executable trim이 없었다. buy fallback에서는 `AMZN/BAC/WMT/NKE/NEE/SO/COP/GOOGL/AAPL/XOM/MSFT/FCX/SLB/MRK`가 same-day filled buy duplicate, `SPY/QQQ`가 validation floor cap, `PLTR`가 낮은 current thesis/source confidence에 막혔다. 반면 `NVDA`는 current-cycle research preflight symbol scope 안에 있고 live IEX quote `206.75/206.78`, spread `0.0145%`, active tradable US equity, existing AI core holding, backlog throttle 비차단, duplicate/open-order 없음 조건을 모두 충족해 이번 cycle의 floor-size learning buy로 승격됐다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env` 기준 `ALPACA_PAPER_TRADE=true` 확인 |
| Market clock | PASS | scheduler core preflight `2026-06-17T14:51:09.719839643-04:00`, regular market open |
| Stale order lifecycle | PASS | `0351` stale cleanup artifact 기준 stale candidates `0`, remaining open orders `0` |
| Alpaca core MCP | PASS | scheduler core preflight hard gate `pass`, quotes/snapshots/assets 포함 |
| Research MCP | PASS tiered | SEC EDGAR/FRED/Yahoo positive 3개, Alpha `empty_response`, Firecrawl credit gap |
| Universe strict | PASS | broad metadata universe `62`개, SPY/QQQ 포함 |
| Review backlog throttle | PASS for buy count | `pending_1d_count=0`, `blocked_add_symbols=['NOK']` |
| Quote/spread | PASS for NVDA | `NVDA` live IEX quote `206.75/206.78`, spread `0.0145%`, freshness 20분 이내 |
| Risk plan | PASS | `check-risk-policy.py --json` PASS, staged deployment warning only |
| Final submit path | DONE | Alpaca MCP `place_stock_order`로 `NVDA` 1주 day limit buy 제출 후 즉시 체결 |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| SO | blocked_same_day_buy_for_trim | 0.0323% | `0211` same-day buy fill 뒤 trim 금지와 trim metric gap이 겹친다. |
| RGTI | blocked_same_day_duplicate_sell | 0.0941% | speculative trim trigger와 spread는 pass지만 same US-date after-hours trim fill 때문에 추가 sell 차단 |
| PFE | blocked_same_day_duplicate_sell | 0.0384% | repeated weak-review trim rationale와 quote/spread는 pass지만 same US-date after-hours trim fill 때문에 추가 sell 차단 |
| SPY | blocked_validation_floor_cap | 0.0094% | 1주 ask `748.54 USD`가 validation floor per-order cap 약 `507.34 USD`를 초과 |
| QQQ | blocked_validation_floor_cap | 0.0477% | 1주 ask `733.45 USD`가 validation floor per-order cap 약 `507.34 USD`를 초과 |
| PLTR | blocked_low_source_confidence | 0.0298% | spread는 pass지만 current ticker note의 낮은 thesis/source confidence가 유지된다 |
| NVDA | selected_buy | 0.0145% | current-cycle research-preflight scope 포함, same-day duplicate/open-order 없음, existing AI core holding floor-size add 경로 pass |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| SO | watch | `same_day_buy_for_trim` | 0211 same-day buy fill이 있어 이번 cycle regular-session trim을 열지 않는다. trim metric gap도 남아 있다. |
| RGTI | watch | `duplicate_symbol_side_same_day` | spread는 정상이나 same-day after-hours trim fill 때문에 regular-session 추가 sell 차단 |
| PFE | watch | `duplicate_symbol_side_same_day` | same US-date after-hours trim fill 뒤라 regular-session 추가 sell 비허용 |

## 주문/체결

- Planned orders: `NVDA` buy 1주 `206.78 USD` day limit, `client_order_id=hourly-20260618-0351-buy-nvda`
- Submitted orders: `NVDA` buy 1주 `206.78 USD` day limit, `order_id=cf1c84cc-cf32-4cf5-b080-01283baaa42a`
- Post-trade reconciliation: same `client_order_id` lookup 기준 주문은 `2026-06-17T19:01:04.818092222Z`에 `filled_avg_price=206.23 USD`로 즉시 체결됐다. `get_orders(status=open)` 기준 open US-equity order는 `0`건이고, `get_account_info` 기준 account `ACTIVE`, cash `28,003.45 USD`, portfolio value `101,151.93 USD`, buying power `300,997.97 USD`, `get_all_positions` 기준 positions `33`, `NVDA qty=39`, `avg_entry_price=214.805897`, `current_price=206.2`, watchlists `0`를 재확인했다.

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | 62 symbols, broad universe screen 유지 |
| `check-mcp-coverage.py --strict --json` | PASS | Alpaca core pass, positive research 3개 |
| `check-risk-policy.py --json` | PASS | staged deployment warning only |

## 산출물

- Report: `wiki/current-runs/daily/2026-06-18-0351-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-18-0351-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-18-0351-hourly-autopilot.json`
- Runtime gate evaluation: `wiki/evidence-store/sources/2026-06-18-0351-hourly-autopilot-runtime-gate-evaluation.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-18-0351-hourly-autopilot-post-trade.json`

## 지표 설명

- `same_day_duplicate_buy`: 같은 미국 거래일에 이미 filled된 동일 symbol buy는 regular-session에서 다시 만들지 않는다.
- `same_day_buy_for_trim`: 같은 미국 거래일에 같은 symbol buy가 체결되면 trim/exit 재평가는 다음 cycle로 넘긴다.
- `validation floor per-order cap`: floor-size learning buy도 `portfolio_value * 0.5%` 상한을 넘을 수 없다.
- `preflight symbol scope`: current-cycle scheduler research preflight가 포함한 symbol 집합 안 후보를 우선 submit-grade symbol confirmation으로 사용한다.
- `sell_candidate_diagnostics`: 실행하지 않은 trim 후보도 why-not evidence를 남겨 analyst review와 policy learning에 사용한다.
