# 2026-06-18-0331-hourly-autopilot scheduled paper autopilot

## 요약

`0331` scheduled hourly-autopilot은 scheduler-owned stale cleanup/core/research preflight를 source-of-record로 사용했다. preflight hard gate는 `pass`였고 regular market은 `2026-06-17T14:31:10.542046132-04:00` 기준 열려 있었다. stale cleanup artifact는 stale candidate `0`, remaining open order `0`이라 `risk_open_order_lifecycle` block이 없었다. research tiered gate도 `SEC EDGAR/FRED/Yahoo Finance` 3개 positive confirmation으로 strict submit threshold를 유지했고, `Alpha Vantage`는 hourly throttle `provider_error`, `Firecrawl`은 credit 부족 `unknown` gap only로 남겼다.

sell-first 재평가에서는 `SO`가 `0211` same-day buy fill 때문에 `require_no_same_day_buy_for_trim`과 trim metric gap에 같이 막혔고, `RGTI`와 `PFE`는 same US-date after-hours trim fill 때문에 duplicate symbol/side gate가 유지돼 executable trim이 없었다. buy fallback에서는 `AMZN/BAC/WMT/NKE/NEE/SO/COP/GOOGL/AAPL/XOM/MSFT/FCX/SLB`가 same-day filled buy duplicate, `SPY/QQQ`가 validation floor cap 초과, `INTC/AVGO`가 ai_semiconductor warning band, `PLTR/TSLA`가 낮은 current thesis/source confidence에 막혔다. 반면 `MRK`는 current-cycle research preflight symbol scope 안에 있고 live IEX quote `115.16/115.21`, spread `0.0434%`, active tradable US equity, healthcare diversifier 역할, backlog throttle 비차단, duplicate/open-order 없음 조건을 모두 충족해 이번 cycle의 floor-size learning buy로 승격됐다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env` 기준 `ALPACA_PAPER_TRADE=true` 확인 |
| Market clock | PASS | scheduler core preflight `2026-06-17T14:31:10.542046132-04:00`, regular market open |
| Stale order lifecycle | PASS | `0331` stale cleanup artifact 기준 stale candidates `0`, remaining open orders `0` |
| Alpaca core MCP | PASS | scheduler core preflight hard gate `pass`, quotes/snapshots/assets 포함 |
| Research MCP | PASS tiered | SEC EDGAR/FRED/Yahoo positive 3개, Alpha throttle `provider_error`, Firecrawl credit gap |
| Universe strict | PASS | broad metadata universe `62`개, SPY/QQQ 포함 |
| Review backlog throttle | PASS for buy count | `pending_1d_count=0`, `blocked_add_symbols=['NOK']` |
| Quote/spread | PASS for MRK | `MRK` live IEX quote `115.16/115.21`, spread `0.0434%`, freshness 20분 이내 |
| Risk plan | PASS | `check-risk-policy.py --json` PASS, staged deployment warning only |
| Final submit path | DONE | Alpaca MCP `place_stock_order`로 `MRK` 1주 day limit buy 제출, immediate reconciliation 기준 open `new` |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| SO | blocked_same_day_buy_for_trim | 5.1078% | `0211` same-day buy fill 뒤 trim 금지와 trim metric gap이 겹친다. |
| RGTI | blocked_same_day_duplicate_sell | 0.0477% | speculative trim trigger와 spread는 pass지만 same US-date after-hours trim fill 때문에 추가 sell 차단 |
| PFE | blocked_same_day_duplicate_sell | 0.0384% | repeated weak-review trim rationale와 quote/spread는 pass지만 same US-date after-hours trim fill 때문에 추가 sell 차단 |
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
| SLB | blocked_same_day_duplicate_buy | 0.0197% | `0231` buy 1주가 same US-date에 이미 filled |
| SPY | blocked_validation_floor_cap | 0.0254% | 1주 ask `746.95 USD`가 validation floor per-order cap 약 `505.00 USD`를 초과 |
| QQQ | blocked_validation_floor_cap | 0.0384% | 1주 ask `729.69 USD`가 validation floor per-order cap 약 `505.00 USD`를 초과 |
| INTC | blocked_ai_semiconductor_warning_band | 0.0246% | ai_semiconductor theme/factor/cluster warning band 위라 relaxed floor-size buy 승격 중단 |
| AVGO | blocked_ai_semiconductor_warning_band | 0.0581% | same ai_semiconductor complex warning band와 post-earnings risk watch 지속 |
| PLTR | blocked_low_source_confidence | 0.5683% | spread도 cap 초과이며 current ticker note의 낮은 thesis/source confidence가 유지된다 |
| TSLA | blocked_low_source_confidence | 0.8829% | spread cap 초과 및 current thesis/source confidence 미충족 |
| MRK | selected_buy | 0.0434% | healthcare diversifier, current-cycle research-preflight scope 포함, duplicate/open-order 없음, spread/freshness/risk cap pass |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| SO | watch | `same_day_buy_for_trim` | 0211 same-day buy fill이 있어 이번 cycle regular-session trim을 열지 않는다. trim metric gap도 남아 있다. |
| RGTI | watch | `duplicate_symbol_side_same_day` | spread는 정상이나 same-day after-hours trim fill 때문에 regular-session 추가 sell 차단 |
| PFE | watch | `duplicate_symbol_side_same_day` | same US-date after-hours trim fill 뒤라 regular-session 추가 sell 비허용 |

## 주문/체결

- Planned orders: `MRK` buy 1주 `115.21 USD` day limit, `client_order_id=hourly-20260618-0331-buy-mrk`
- Submitted orders: `MRK` buy 1주 `115.21 USD` day limit, `order_id=1bea80db-11a3-4441-9589-24d4a36f5fc7`
- Post-trade reconciliation: same `client_order_id` lookup 기준 `status=new`, `filled_qty=0`, `filled_avg_price=null`이다. `get_orders(status=open)` 기준 open US-equity order는 `MRK` buy 1건뿐이고, `get_account_info` 기준 account `ACTIVE`, cash `28,324.87 USD`, portfolio value `101,362.51 USD`, buying power `301,666.74 USD`, `get_all_positions` 기준 positions `33`, watchlists `0`를 재확인했다. `get_open_position(MRK)` 단일 read-only 재조회는 `cancelled`로 끝났지만 order/open-orders/all-positions readback은 MRK가 아직 fill되지 않은 open order 상태임을 일관되게 보여준다.

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | 62 symbols, broad universe screen 유지 |
| `check-mcp-coverage.py --strict --json` | PASS | Alpaca core pass, positive research 3개 |
| `check-risk-policy.py --json` | PASS | staged deployment warning only |

## 산출물

- Report: `wiki/current-runs/daily/2026-06-18-0331-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-18-0331-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-18-0331-hourly-autopilot.json`
- Runtime gate evaluation: `wiki/evidence-store/sources/2026-06-18-0331-hourly-autopilot-runtime-gate-evaluation.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-18-0331-hourly-autopilot-post-trade.json`

## 지표 설명

- `same_day_duplicate_buy`: 같은 미국 거래일에 이미 filled된 동일 symbol buy는 regular-session에서 다시 만들지 않는다.
- `same_day_buy_for_trim`: 같은 미국 거래일에 같은 symbol buy가 체결되면 trim/exit 재평가는 다음 cycle로 넘긴다.
- `validation floor per-order cap`: floor-size learning buy도 `portfolio_value * 0.5%` 상한을 넘을 수 없다.
- `preflight symbol scope`: current-cycle scheduler research preflight가 포함한 symbol 집합 안 후보를 우선 submit-grade symbol confirmation으로 사용한다.
- `sell_candidate_diagnostics`: 실행하지 않은 trim 후보도 why-not evidence를 남겨 analyst review와 policy learning에 사용한다.
