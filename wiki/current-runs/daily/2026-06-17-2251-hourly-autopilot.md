# 2026-06-17-2251-hourly-autopilot scheduled paper autopilot

## 요약

`2251` scheduled hourly-autopilot은 scheduler-owned stale cleanup/core/research preflight를 source-of-record로 사용했다. preflight clock `2026-06-17T09:51:11.299013765-04:00`, account `ACTIVE`, positions `33`, open orders `0`, fresh quote rows는 decision time 기준 20분 이내라 Alpaca core hard gate를 PASS 처리했다. Research tiered gate도 `SEC EDGAR/FRED/Yahoo Finance` pass로 strict submit threshold `3` confirmations를 유지했고, `Alpha Vantage`는 one-call-per-hour throttle에 따른 `provider_error` gap, `Firecrawl`은 credits 부족 `unknown` gap only로 유지했다.

live Alpaca continuity에서는 직전 `2231`의 `BAC` buy 1주가 `2026-06-17T13:39:20.834459Z`에 `57.57 USD`로 이미 filled 됐음을 재확인했다. sell-first 재평가에서는 `SO`가 trim decision-grade metric gap, `RGTI`가 live spread `2.8713%` fail, `PFE`가 same US-date after-hours trim fill로 duplicate symbol/side lifecycle gate에 막혀 executable trim이 없었다. buy fallback에서는 `BAC`가 same-day filled buy duplicate로 탈락했고, `FCX/SLB/MSFT`보다 latest review와 diversification benefit이 더 나은 `WMT`가 floor-size learning order로 승격됐다. `WMT` 1주 buy를 `119.83 USD` day limit로 제출했고 immediate reconciliation 기준 `order_id=381c1f40-067a-4c71-99e6-c57ab92dd6e6`는 `status=new`, `filled_qty=0` open order다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env` 기준 `ALPACA_PAPER_TRADE=true` |
| Market clock | PASS | live `get_clock` `2026-06-17T09:53:21.077840947-04:00`, regular market open |
| Stale order lifecycle | PASS | `2251` stale cleanup artifact 기준 stale candidates/open orders 모두 0 |
| Alpaca core MCP | PASS | scheduler core preflight hard gate `pass`, live continuity 기준 open orders `0` before submit |
| Research MCP | PASS tiered | SEC EDGAR/FRED/Yahoo positive 3개, Alpha throttle gap, Firecrawl credit gap |
| Universe strict | PASS | broad metadata universe `62`개, SPY/QQQ 포함 |
| Review backlog throttle | PASS for buy | `pending_1d_count=0`, `blocked_add_symbols=['NOK']` |
| Quote/spread | PASS for WMT | live WMT quote `119.56/119.83`, spread `0.2258%`, freshness pass |
| Risk plan | PASS | `check-risk-policy.py --json` 기준 WMT 1주 buy risk gate 통과 |
| Final submit path | PASS | WMT는 same-day duplicate/open-order conflict 없음, floor-size learning directive 충족 |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| SO | blocked_sell_metric_gap | 0.0534% | quote/spread는 통과했지만 trim decision-grade expected-excess/replacement margin 공백 지속 |
| RGTI | blocked_spread_fail_sell | 2.8713% | speculative trim trigger는 유지되지만 current spread가 policy cap 초과 |
| PFE | blocked_same_day_duplicate_sell | 0.0383% | trim rationale와 quote/spread는 pass지만 같은 미국 거래일 after-hours sell fill이 있어 duplicate sell gate에 막힘 |
| BAC | blocked_same_day_duplicate_buy | 0.0346% | 직전 `2231` buy 1주가 same US-date에 이미 filled돼 regular-session duplicate buy로 재진입 불가 |
| WMT | submitted_buy | 0.2258% | latest 1D closeout 양호, defensive retail diversifier, 3-provider positive confirmation, duplicate/open-order conflict 없음 |
| FCX | lower_rank_backup | 0.0567% | materials hindsight 강세는 유지되지만 commodity sleeve chase 완화 필요 |
| SLB | lower_rank_backup | 0.0585% | same energy sleeve 내에서 latest review가 WMT보다 약함 |
| MSFT | lower_rank_backup | 0.4253% | mega-cap quality candidate지만 diversification benefit이 WMT보다 약함 |
| SPY | blocked_validation_floor_cap | 0.0040% | 1주 ask `751.05 USD`가 validation floor per-order cap을 초과 |
| NOK | blocked_validation_lifecycle_add_block | 0.0719% | review-due add-block 유지 |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| SO | watch | `sell_metric_gap` | trim expected-excess/replacement margin metric 공백 지속 |
| RGTI | watch | `spread_within_policy` | current spread `2.8713%`가 cap `0.50%` 초과 |
| PFE | watch | `duplicate_symbol_side_same_day` | same US-date after-hours trim fill이 있어 regular-session 추가 sell 차단 |

## 주문/체결

- Planned order: `WMT` buy `1` @ `119.83 USD` day limit
- `place_stock_order`: `WMT` buy 1주, `client_order_id=hourly-20260617-2251-buy-wmt`, `order_id=381c1f40-067a-4c71-99e6-c57ab92dd6e6`
- Immediate reconciliation: `get_order_by_client_id` 기준 상태는 `new`, `filled_qty=0`, `filled_avg_price=null`이다.
- Open orders after submit: `WMT` buy 1건 `status=new`
- Same US-date fills seen during reconciliation: `BAC` buy 1주 `57.57 USD`, `PFE` sell 1주 `26.03 USD`, `RGTI` sell 1주 `20.96 USD`
- Post-trade position check: `WMT qty=9`, `avg_entry_price=118.427778`, account cash `30,334.21 USD`, portfolio value `100,996.63 USD`, buying power `303,454.07 USD`

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | 62 symbols, SPY/QQQ 포함, pre-MCP shortlist 10개 |
| `check-mcp-coverage.py --strict --json` | PASS | Alpaca core pass, positive research 3개, Alpha/Firecrawl non-core gaps |
| `check-risk-policy.py --json` | PASS | WMT 1주 buy notional `119.83 USD`; staged deployment warning only |

## 산출물

- Report: `wiki/current-runs/daily/2026-06-17-2251-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-17-2251-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-17-2251-hourly-autopilot.json`
- Runtime gate evaluation: `wiki/evidence-store/sources/2026-06-17-2251-hourly-autopilot-runtime-gate-evaluation.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-17-2251-hourly-autopilot-post-trade.json`

## 지표 설명

- `duplicate_symbol_side_same_day`: 동일 미국 거래일에 이미 체결된 같은 symbol/side 주문이 있으면 learning order라도 재진입하지 않는다.
- `validation floor per-order cap`: floor-size learning buy도 `portfolio_value * 0.5%` 상한을 넘을 수 없다. 이번 cycle cap은 약 `506.53 USD`라 `SPY` 1주가 초과했다.
- `tiered MCP gate`: core `alpaca` pass와 research positive confirmation `3개` 이상이면 Alpha/Firecrawl 비핵심 gap이 있어도 submit을 막지 않는다.
