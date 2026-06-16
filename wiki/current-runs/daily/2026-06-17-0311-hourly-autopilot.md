# 2026-06-17-0311-hourly-autopilot scheduled paper autopilot

## 요약

`0311` scheduled hourly-autopilot은 scheduler-owned stale cleanup/core/research preflight를 source-of-record로 사용했다. preflight clock `2026-06-16T14:11:09.914769307-04:00`, account `ACTIVE`, positions `33`, open orders `0`, fresh IEX quote rows는 decision time `2026-06-17 03:14 KST` 기준 모두 20분 이내라 Alpaca core hard gate를 PASS 처리했다. Research tiered gate도 `SEC EDGAR/FRED/Yahoo Finance` pass로 strict submit threshold `3` confirmations를 충족했고, `Alpha Vantage`는 one-call-per-hour throttle 때문에 `provider_error` gap, `Firecrawl`은 credits 부족 `unknown` gap only로 유지했다.

이번 cycle은 추가 Alpaca read-only 재호출 없이 `0311` preflight를 그대로 submit boundary로 재사용했다. stale cleanup artifact 기준 stale candidates/open orders는 모두 `0`이다. sell-first 후보인 `SO`와 `PFE`는 same-day sell fill이 이미 있어 duplicate symbol/side discipline에 막혔고, `RGTI`는 earlier same-day sell submission이 `2026-06-16T14:31:08.972628Z`에 `canceled`로 정리됐더라도 동일 미국 거래일 duplicate-side blocker로 계속 남아 있다. buy fallback은 `review_backlog_pending_1d_count=18`가 stop threshold `12`를 넘는 상태에서 `NEE/WMT/NKE/SLB`가 모두 review backlog throttle에 막혔고, `SPY/QQQ`는 validation floor per-order cap 약 `505.94 USD`까지 추가로 초과했으며, `NOK`는 lifecycle add-block이 계속 열려 있어 submit path를 만들지 못했다. 결과적으로 이번 cycle도 hard platform/MCP/universe/risk gate는 PASS했지만 exact duplicate/backlog/floor-cap/add-block gate 때문에 minimum learning order 1건을 만들지 못한 submit-mode no-op다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env` 기준 `ALPACA_PAPER_TRADE=true` |
| Market clock | PASS | scheduler core preflight `get_clock` `2026-06-16T14:11:09.914769307-04:00`, regular market open |
| Stale order lifecycle | PASS | `0311` stale cleanup artifact 기준 stale candidates/open orders 모두 0 |
| Alpaca core MCP | PASS | scheduler core preflight hard gate `pass`, quote rows fresh |
| Research MCP | PASS tiered | SEC EDGAR/FRED/Yahoo positive 3개, Alpha one-call throttle `provider_error`, Firecrawl credit gap |
| Universe strict | PASS | broad metadata universe `62`개, SPY/QQQ 포함 |
| Review backlog throttle | BUY BLOCK ONLY | `pending_1d_count=18`가 stop threshold `12` 초과, sell/trim에는 비적용 |
| Quote/spread | PASS/MIXED | `SO/RGTI/PFE/NEE/WMT/NKE/SLB/SPY/QQQ/NOK`는 spread cap 이내 |
| Risk plan | PASS | `check-risk-policy.py --json` 기준 current positions/no open orders 포함, `orders=[]` 허용 |
| Final submit path | NO SUBMIT | `SO/PFE` same-day sell fill, `RGTI` same-day canceled sell history, `NEE/WMT/NKE/SLB` backlog stop, `SPY/QQQ` floor cap+review backlog, `NOK` validation lifecycle add-block으로 minimum learning order를 만들지 못함 |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| SO | blocked_same_day_duplicate_sell | 0.0318% | repeated weak-review trim rationale와 preflight quote `94.38/94.41` spread pass는 유지됐지만 `2026-06-16T14:58:02.526808Z` same-day sell fill 1건이 이미 있어 추가 same-side trim 비허용 |
| RGTI | blocked_same_day_duplicate_sell | 0.0942% | speculative trim trigger와 preflight quote `21.23/21.25` spread pass는 유지되지만 same-day earlier sell order `hourly-20260616-2251-sell-rgti`의 canceled history가 동일 미국 거래일 duplicate gate로 남음 |
| PFE | blocked_same_day_duplicate_sell | 0.0385% | `2026-06-16T14:18:55.368488Z` same-day trim fill 1건이 이미 있어 추가 same-side sell 비허용 |
| NEE | blocked_review_backlog_throttle_buy | 0.0116% | utility diversifier 1주 buy는 quote/spread와 per-order cap은 통과하지만 `review_backlog_pending_1d_count=18`가 submit buy hard gate를 닫음 |
| WMT | blocked_review_backlog_throttle_buy | 0.0166% | consumer defensive fallback 1주 buy는 executable price range지만 buy backlog stop 때문에 제출 불가 |
| NKE | blocked_review_backlog_throttle_buy | 0.0221% | existing consumer add 후보이나 backlog stop이 submit buy를 차단 |
| SLB | blocked_review_backlog_throttle_buy | 0.0188% | energy-services diversifier 1주 buy는 quote/spread와 floor cap은 통과하지만 buy backlog stop 때문에 제출 불가 |
| SPY | blocked_floor_cap_and_review_backlog | 0.0027% | benchmark fallback이지만 1주 ask `752.01 USD`가 validation floor cap 약 `505.94 USD`를 초과하고 buy backlog stop도 유지 |
| QQQ | blocked_floor_cap_and_review_backlog | 0.0054% | benchmark fallback이지만 1주 ask `734.24 USD`가 validation floor cap 약 `505.94 USD`를 초과하고 buy backlog stop도 유지 |
| NOK | blocked_validation_lifecycle_add_block | 0.0720% | due review add-block과 `pending_1d_count=18` buy throttle이 동시에 유지 |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| SO | watch | `duplicate_symbol_side_same_day` | trim rationale와 quote/spread는 정상이지만 same-day `SO` sell fill 이후 재제출 금지 |
| RGTI | watch | `duplicate_symbol_side_same_day` | quote/spread와 held qty는 정상이지만 same-day canceled sell history가 재제출을 막음 |
| PFE | watch | `duplicate_symbol_side_same_day` | same-day trim fill 1건 뒤라 추가 same-side trim 비허용 |

## 주문/체결

- Planned orders: 0
- Submitted orders: 0
- `place_stock_order` 호출: 없음
- Same-day fill history seen in `0311` preflight: `SO` sell 1주 `filled_avg_price=94.77 USD`, `PFE` sell 1주 `25.94 USD`, `AVGO` sell 1주 `387.76 USD`
- Same-day duplicate history reused from prior runtime evidence: `RGTI` sell 7주 `client_order_id=hourly-20260616-2251-sell-rgti`는 `0011` cycle recheck 기준 `2026-06-16T14:31:08.972628Z` `canceled`
- Post-trade reconciliation: 이번 cycle 신규 submit attempt는 없었다. scheduler preflight 기준 open orders `0`, positions `33`, `SO qty=5`, `RGTI qty_available=28`, cash `30,344.81 USD`, portfolio value `101,188.48 USD`를 재확인했다.

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | 62 symbols, SPY/QQQ 포함, final candidates 10개 |
| `check-mcp-coverage.py --strict --json` | PASS | Alpaca core pass, positive research 3개, Alpha/Firecrawl non-core gaps |
| `check-risk-policy.py --json` | PASS | current positions/no open orders 포함, `orders=[]` no-submit plan |

## 산출물

- Report: `wiki/current-runs/daily/2026-06-17-0311-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-17-0311-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-17-0311-hourly-autopilot.json`
- Runtime gate evaluation: `wiki/evidence-store/sources/2026-06-17-0311-hourly-autopilot-runtime-gate-evaluation.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-17-0311-hourly-autopilot-post-trade.json`

## 지표 설명

- `duplicate symbol/side discipline`: 같은 미국 거래일에 이미 제출된 동일 symbol/side 주문을 반복 제출하지 않는 submit safety 규칙이다. 이번 cycle에서는 filled `SO`/`PFE` sell과 prior-cycle canceled `RGTI` sell이 모두 재제출 차단 근거로 남았다.
- `validation floor per-order cap`: floor-size learning buy도 `portfolio_value * 0.5%` 상한을 넘을 수 없다. 이번 cycle의 cap은 약 `505.94 USD`라 `SPY/QQQ` 1주가 초과했다.
- `review_backlog_pending_1d_count`: validation buy 1D review backlog count다. 이번 cycle에서는 `18`이라 YAML stop threshold `12`를 넘어 신규 buy가 차단됐다.
- `sell_candidate_diagnostics`: 실행하지 않은 trim 후보도 why-not evidence를 남겨 후속 analyst review와 policy learning에 사용한다.
