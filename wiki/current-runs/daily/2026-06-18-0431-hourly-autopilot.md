# 2026-06-18-0431-hourly-autopilot scheduled paper autopilot

## 요약

`0431` scheduled hourly-autopilot은 scheduler-owned stale cleanup/core/research preflight를 source-of-record로 사용했다. preflight hard gate는 `pass`였고 regular market은 `2026-06-17T15:31:11.646488605-04:00` 기준 열려 있었다. stale cleanup artifact는 stale candidate `0`, remaining open order `0`이라 `risk_open_order_lifecycle` block이 없었다. live Alpaca submit-boundary continuity 기준 account `ACTIVE`, cash `28,003.45 USD`, portfolio value `100,332.59 USD`, buying power `299,013.24 USD`, positions `34`를 재확인했다.

research tiered gate도 `SEC EDGAR/FRED/Yahoo Finance` pass로 strict submit threshold `3` confirmations를 유지했고, `Alpha Vantage`는 one-call-per-hour throttle `provider_error`, `Firecrawl`은 credit 부족 `unknown` gap only로 남겼다. sell-first 재평가에서는 `SO`가 `0211` same-day buy fill 때문에 `require_no_same_day_buy_for_trim`과 trim metric gap에 같이 막혔고, `RGTI`와 `PFE`는 same US-date after-hours trim fill 때문에 duplicate symbol/side gate가 유지돼 executable trim이 없었다. buy fallback에서는 current-cycle research-preflight scope의 `WMT/BAC/NKE/NEE/SLB/XOM/GOOGL`가 same-day filled buy duplicate, `SPY/QQQ`가 validation floor cap 약 `501.66 USD` 초과, `PLTR`가 낮은 current thesis/source confidence에 막혔다. 남은 current-cycle research-confirmed candidate `CVX`는 live submit-boundary IEX quote `170.43/184.00` 기준 spread `7.6624%`가 policy hard cap `0.50%`를 크게 초과해 최종 submit gate에서 탈락했다. 결과적으로 이번 cycle은 hard platform/MCP/universe/risk gate는 PASS했지만 duplicate/source-confidence/floor-cap/spread gate 때문에 minimum learning order 1건을 만들지 못한 submit-mode policy exception no-op다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env` 기준 `ALPACA_PAPER_TRADE=true` |
| Market clock | PASS | live Alpaca `get_clock` `2026-06-17T15:34:35.037645625-04:00`, regular market open |
| Stale order lifecycle | PASS | `0431` stale cleanup artifact 기준 stale candidates `0`, remaining open orders `0` |
| Alpaca core MCP | PASS | scheduler core preflight hard gate `pass`, live continuity 기준 positions `34`, account `ACTIVE` |
| Research MCP | PASS tiered | SEC EDGAR/FRED/Yahoo positive 3개, Alpha throttle `provider_error`, Firecrawl credit gap |
| Universe strict | PASS | broad metadata universe `62`개, SPY/QQQ 포함 |
| Review backlog throttle | PASS for buy count | `pending_1d_count=0`, `blocked_add_symbols=['NOK']` |
| Quote freshness | PASS | live `CVX` quote timestamp `2026-06-17T19:34:35.976945323Z`, age 약 `0.73`분 |
| Spread | FAIL for submit candidate | live `CVX` spread `7.6624%` > policy cap `0.50%` |
| Risk plan | PASS | `check-risk-policy.py --json` 기준 current positions `34`, open orders `0`, `orders=[]` 허용 |
| Final submit path | NO SUBMIT | `CVX` live spread hard gate fail, 나머지 후보는 duplicate/floor-cap/source-confidence/research-scope gate로 탈락 |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| SO | blocked_same_day_buy_for_trim | 0.1082% | `0211` same-day buy fill과 trim metric gap이 겹쳐 regular-session trim 승격 불가 |
| RGTI | blocked_same_day_duplicate_sell | 0.0483% | speculative trim trigger와 spread는 pass지만 same US-date after-hours trim fill 때문에 추가 sell 차단 |
| PFE | blocked_same_day_duplicate_sell | 0.0386% | repeated weak-review trim rationale와 quote/spread는 pass하지만 same US-date after-hours trim fill 때문에 추가 sell 차단 |
| WMT | blocked_same_day_duplicate_buy | 0.0170% | `2026-06-17T14:07:50Z` fill 이후 same US-date duplicate buy 규율 유지 |
| BAC | blocked_same_day_duplicate_buy | 0.0178% | `2026-06-17T13:39:20Z` fill 이후 same US-date duplicate buy 규율 유지 |
| NKE | blocked_same_day_duplicate_buy | 0.0451% | `2026-06-17T14:47:16Z` fill 이후 same US-date duplicate buy 규율 유지 |
| NEE | blocked_same_day_duplicate_buy | 0.0234% | `2026-06-17T14:59:48Z` fill 이후 same US-date duplicate buy 규율 유지 |
| SLB | blocked_same_day_duplicate_buy | 0.0198% | `2026-06-17T17:39:03Z` fill 이후 same US-date duplicate buy 규율 유지 |
| XOM | blocked_same_day_duplicate_buy | 0.0214% | `2026-06-17T16:17:56Z` fill 이후 same US-date duplicate buy 규율 유지 |
| GOOGL | blocked_same_day_duplicate_buy | 0.0386% | `2026-06-17T16:40:11Z` fill 이후 same US-date duplicate buy 규율 유지 |
| SPY | blocked_validation_floor_cap | 0.0067% | 1주 ask `741.90 USD`가 validation floor per-order cap 약 `501.66 USD`를 초과 |
| QQQ | blocked_validation_floor_cap | 0.0400% | 1주 ask `726.20 USD`가 validation floor per-order cap 약 `501.66 USD`를 초과 |
| PLTR | blocked_low_source_confidence | 0.0228% | current ticker note가 `이번 주문 제외`, `신뢰도: 낮음`을 유지해 floor-size add hard gate 미충족 |
| CVX | blocked_live_spread | 7.6624% | current-cycle research-preflight scope 포함, same-day duplicate/open-order 없음, review backlog 비차단이지만 live submit-boundary quote `170.43/184.00`가 spread hard cap 초과 |
| V | blocked_missing_current_cycle_research_confirmation | n/a | live quote는 별도 조회하지 않았고 current-cycle scheduler research preflight symbol scope 밖이라 nested research omission cycle에서 submit-grade confirmation 불가 |

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
- Post-trade reconciliation: live `get_account_info/get_all_positions/get_clock/get_stock_latest_quote(symbols=CVX, feed=iex)`와 scheduler-owned stale/core/research preflight를 결합해 account `ACTIVE`, cash `28,003.45 USD`, portfolio value `100,332.59 USD`, buying power `299,013.24 USD`, positions `34`, stale cleanup remaining open orders `0`, same US-date fill ledger `17건`을 재확인했다.

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | 62 symbols, broad-universe fallback 포함 |
| `check-mcp-coverage.py --strict --json` | PASS | Alpaca core pass, positive research 3개 |
| `check-risk-policy.py --json` | PASS | current positions `34`, open orders `0`, `orders=[]` no-submit plan |

## 산출물

- Report: `wiki/current-runs/daily/2026-06-18-0431-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-18-0431-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-18-0431-hourly-autopilot.json`
- Runtime gate evaluation: `wiki/evidence-store/sources/2026-06-18-0431-hourly-autopilot-runtime-gate-evaluation.json`

## 지표 설명

- `same_day_duplicate_buy`: 같은 미국 거래일에 이미 filled된 동일 symbol buy는 regular-session에서 다시 만들지 않는다.
- `same_day_buy_for_trim`: 같은 미국 거래일에 같은 symbol buy가 체결되면 trim/exit 재평가는 다음 cycle로 넘긴다.
- `validation floor per-order cap`: floor-size learning buy도 `portfolio_value * 0.5%` 상한을 넘을 수 없다. 이번 cycle cap은 약 `501.66 USD`다.
- `preflight symbol scope`: current-cycle scheduler research preflight가 포함한 symbol 집합 밖 후보는 등록된 research MCP surface가 없는 cycle에서는 submit-grade symbol confirmation으로 승격하지 않는다.
- `sell_candidate_diagnostics`: 실행하지 않은 trim 후보도 why-not evidence를 남겨 analyst review와 policy learning에 사용한다.
