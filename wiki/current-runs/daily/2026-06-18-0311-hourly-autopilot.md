# 2026-06-18-0311-hourly-autopilot scheduled paper autopilot

## 요약

`0311` scheduled hourly-autopilot은 scheduler-owned stale cleanup/core/research preflight를 source-of-record로 사용했다. preflight hard gate는 `pass`였고 live Alpaca continuity 기준 `2026-06-17T14:12:57.121580877-04:00` regular market open, account `ACTIVE`, open orders `0`, positions `33`, same US-date filled order stack `15건`과 latest filled order `hourly-20260618-0231-buy-slb`를 재확인했다. Research tiered gate도 `SEC EDGAR/FRED/Yahoo Finance` pass로 strict submit threshold `3` confirmations를 유지했고, `Alpha Vantage`는 one-call-per-hour throttle `provider_error`, `Firecrawl`은 credit 부족 `unknown` gap only로 남겼다.

sell-first 재평가에서는 `SO`가 `0211` same-day buy fill 때문에 `require_no_same_day_buy_for_trim`과 trim metric gap에 같이 막혔고, `RGTI`와 `PFE`는 same US-date after-hours trim fill 때문에 duplicate symbol/side gate가 계속 유지돼 executable trim이 없었다. buy fallback에서는 `AMZN/BAC/WMT/NKE/NEE/SO/COP/GOOGL/AAPL/XOM/MSFT/FCX/SLB`가 same-day filled buy duplicate, `SPY/QQQ`가 validation floor cap 약 `505.43 USD` 초과, `INTC/AVGO`가 ai_semiconductor warning band, `PLTR/TSLA`가 낮은 current thesis/source confidence에 막혔다. broad-universe fallback `JPM/V/JNJ`도 live IEX quote spread가 각각 약 `4.59% / 1.39% / 2.37%`로 policy cap `0.50%`를 크게 넘겼고, 동시에 current-cycle scheduler research preflight symbol scope 밖이라 nested research MCP omission 상태에서 submit-grade symbol confirmation도 만들지 못했다. 결과적으로 이번 cycle은 hard platform/MCP/universe/risk gate는 PASS했지만 exact duplicate/spread/source-confidence/symbol-scope gate 때문에 minimum learning order 1건을 만들지 못한 submit-mode policy exception no-op다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env` 기준 `ALPACA_PAPER_TRADE=true` |
| Market clock | PASS | live `get_clock` `2026-06-17T14:12:57.121580877-04:00`, regular market open |
| Stale order lifecycle | PASS | `0311` stale cleanup artifact 기준 stale candidates `0`, remaining open orders `0` |
| Alpaca core MCP | PASS | scheduler core preflight hard gate `pass`, direct continuity 기준 open orders `0`, account `ACTIVE`, watchlists `0` |
| Research MCP | PASS tiered | SEC EDGAR/FRED/Yahoo positive 3개, Alpha throttle `provider_error`, Firecrawl credit gap |
| Universe strict | PASS | broad metadata universe `62`개, SPY/QQQ 포함 |
| Review backlog throttle | PASS for buy count | `pending_1d_count=0`, `blocked_add_symbols=['NOK']` |
| Quote/spread | MIXED | preflight-covered shortlist는 quote freshness pass, broad-universe fallback `JPM/V/JNJ`는 spread hard cap fail |
| Risk plan | PASS | `check-risk-policy.py --json` 기준 current positions/no open orders 포함, `orders=[]` 허용 |
| Final submit path | NO SUBMIT | duplicate-side, floor-cap, ai-semiconductor warning, low source confidence, live spread fail, preflight symbol-scope gate 때문에 minimum learning order를 만들지 못함 |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| SO | blocked_same_day_buy_for_trim | 0.0215% | `0211` same-day buy fill과 trim metric gap이 겹쳐 regular-session trim 승격 불가 |
| RGTI | blocked_same_day_duplicate_sell | 0.0476% | speculative trim trigger와 spread는 pass지만 same US-date after-hours trim fill 때문에 추가 sell 차단 |
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
| SPY | blocked_validation_floor_cap | 0.0054% | 1주 ask `746.70 USD`가 validation floor per-order cap 약 `505.43 USD`를 초과 |
| QQQ | blocked_validation_floor_cap | 0.0302% | 1주 ask `729.09 USD`가 validation floor per-order cap 약 `505.43 USD`를 초과 |
| INTC | blocked_ai_semiconductor_warning_band | 0.0494% | ai_semiconductor theme/factor/cluster warning band 위라 relaxed floor-size buy 승격 중단 |
| AVGO | blocked_ai_semiconductor_warning_band | 0.2327% | same ai_semiconductor complex warning band와 post-earnings risk watch 지속 |
| PLTR | blocked_low_source_confidence | 0.0373% | current ticker note가 `이번 주문 제외`, `신뢰도: 낮음`을 유지해 floor-size add hard gate 미충족 |
| TSLA | blocked_low_source_confidence | 0.0248% | current ticker note가 이벤트성 optionality 위주 `이번 주문 제외`, `신뢰도: 낮음`을 유지 |
| JPM | blocked_live_spread_and_missing_current_cycle_research_confirmation | 4.5911% | spread hard cap fail, plus current-cycle scheduler research preflight symbol scope 밖 |
| V | blocked_live_spread_and_missing_current_cycle_research_confirmation | 1.3869% | spread hard cap fail, plus current-cycle scheduler research preflight symbol scope 밖 |
| JNJ | blocked_live_spread_and_missing_current_cycle_research_confirmation | 2.3698% | spread hard cap fail, plus current-cycle scheduler research preflight symbol scope 밖 |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| SO | watch | `same_day_buy_for_trim` | 0211 same-day buy fill이 있어 이번 cycle regular-session trim을 열지 않는다. trim metric gap도 남아 있다. |
| RGTI | watch | `duplicate_symbol_side_same_day` | spread는 정상이나 same-day after-hours trim fill 때문에 regular-session 추가 sell 차단 |
| PFE | watch | `duplicate_symbol_side_same_day` | same US-date after-hours trim fill 뒤라 regular-session 추가 sell 비허용 |

## 주문/체결

- Planned orders: 0
- Submitted orders: 0
- `place_stock_order` 호출: 없음
- Post-trade reconciliation: 이번 cycle 신규 submit attempt는 없었다. direct `get_orders(status=open)` 기준 open orders `0`, `get_account_info/get_all_positions` 기준 cash `28,324.87 USD`, portfolio value `101,086.26 USD`, buying power `301,267.35 USD`, positions `33`, `SLB qty=8`, `SO qty=6`, `RGTI qty=27`, `PFE qty=2`를 재확인했다.

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | 62 symbols, broad-universe fallback 포함 |
| `check-mcp-coverage.py --strict --json` | PASS | Alpaca core pass, positive research 3개 |
| `check-risk-policy.py --json` | PASS | current positions/no open orders 포함, `orders=[]` no-submit plan |

## 산출물

- Report: `wiki/current-runs/daily/2026-06-18-0311-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-18-0311-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-18-0311-hourly-autopilot.json`
- Runtime gate evaluation: `wiki/evidence-store/sources/2026-06-18-0311-hourly-autopilot-runtime-gate-evaluation.json`

## 지표 설명

- `same_day_duplicate_buy`: 같은 미국 거래일에 이미 filled된 동일 symbol buy는 regular-session에서 다시 만들지 않는다.
- `same_day_buy_for_trim`: 같은 미국 거래일에 같은 symbol buy가 체결되면 trim/exit 재평가는 다음 cycle로 넘긴다.
- `validation floor per-order cap`: floor-size learning buy도 `portfolio_value * 0.5%` 상한을 넘을 수 없다. 이번 cycle cap은 약 `505.43 USD`다.
- `preflight symbol scope`: current-cycle scheduler research preflight가 포함한 symbol 집합 밖 후보는 등록된 research MCP surface가 없는 cycle에서는 submit-grade symbol confirmation으로 승격하지 않는다.
- `sell_candidate_diagnostics`: 실행하지 않은 trim 후보도 why-not evidence를 남겨 analyst review와 policy learning에 사용한다.
