# 2026-06-16-2331-hourly-autopilot scheduled paper autopilot

## 요약

`2331` scheduled hourly-autopilot은 scheduler-owned stale cleanup/core/research preflight를 source-of-record로 사용했다. preflight clock `2026-06-16T10:31:11.132561765-04:00`, account `ACTIVE`, positions `33`, fresh IEX quote rows는 모두 20분 이내라 Alpaca core hard gate를 PASS 처리했다. Research tiered gate도 `SEC EDGAR/FRED/Yahoo Finance` pass로 strict submit threshold `3` confirmations를 충족했고, `Alpha Vantage`는 one-call-per-hour throttle `provider_error`, `Firecrawl`은 credits 부족 `unknown` gap only로 유지했다.

stale cleanup artifact는 직렬화 시점에 `RGTI` stale sell 7주를 remaining open으로 남겼지만, live Alpaca `get_orders(status=open)` 재조정은 open orders `0`을 반환했고 `get_orders(status=all, after=2026-06-16T13:31:00Z)`는 같은 `hourly-20260616-2251-sell-rgti`가 `2026-06-16T14:31:08.972628Z`에 `canceled`로 전환된 것을 보여줬다. 따라서 global `risk_open_order_lifecycle` 차단은 해소로 기록한다. 다만 final submit path는 별개로 닫혔다. `RGTI`는 same-day earlier sell order 이력 때문에 duplicate symbol/side discipline이 재제출을 막았고, `PFE`는 `2026-06-16T14:18:55.368488Z` same-day sell fill 1건, `SO`는 spread `11.3368%` fail, buy fallback은 `review_backlog_pending_1d_count=18`와 validation floor per-order cap/add-block 때문에 모두 비실행 상태였다. 결과적으로 이번 cycle은 hard platform/MCP/universe/risk gate는 PASS했지만 exact duplicate/spread/backlog gate 때문에 minimum learning order 1건을 만들지 못한 submit-mode no-op다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env` 기준 `ALPACA_PAPER_TRADE=true` |
| Market clock | PASS | live `get_clock` `2026-06-16T10:33:05.200440095-04:00`, regular market open |
| Stale order lifecycle | PASS after live reconcile | stale cleanup artifact의 residual `RGTI` open row는 live Alpaca `get_orders(status=open)=[]`, same order `canceled_at=2026-06-16T14:31:08.972628Z`로 해소 |
| Alpaca core MCP | PASS | scheduler core preflight hard gate `pass` + live boundary recheck |
| Research MCP | PASS tiered | SEC EDGAR/FRED/Yahoo positive 3개, Alpha throttle `provider_error`, Firecrawl credit gap |
| Universe strict | PASS | broad metadata universe `62`개, SPY/QQQ 포함 |
| Review backlog throttle | BUY BLOCK ONLY | `pending_1d_count=18`가 stop threshold `12` 초과, sell/trim에는 비적용 |
| Quote/spread | PASS/MIXED | `RGTI/PFE/NOK/SPY/QQQ`는 spread cap 이내, `SO`는 `11.3368%`로 fail |
| Risk plan | PASS | `check-risk-policy.py --json` 기준 current positions/no open orders 포함, `orders=[]` 허용 |
| Final submit path | NO SUBMIT | `RGTI/PFE` same-day duplicate symbol/side, `SO` spread fail, `SPY/QQQ/NOK` buy-side hard/submit gates로 minimum learning order를 만들지 못함 |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| RGTI | blocked_same_day_duplicate_sell | 0.0479% | speculative trim trigger와 open-order lifecycle 해소는 확인됐지만 same-day earlier `sell` order `hourly-20260616-2251-sell-rgti`가 이미 존재해 duplicate symbol/side discipline이 재제출을 막음 |
| PFE | blocked_same_day_duplicate_sell | 0.0769% | `2026-06-16T14:18:55.368488Z` same-day trim fill 1건이 이미 있어 추가 same-side sell 비허용 |
| SO | blocked_spread_fail | 11.3368% | scheduler-owned `2331` quote `88.70/99.36`이 policy spread cap `0.50%`를 크게 초과 |
| SPY | blocked_floor_cap_and_review_backlog | 0.0040% | benchmark fallback이지만 1주 ask `752.54 USD`가 validation floor cap 약 `506.89 USD`를 초과하고 buy backlog stop도 유지 |
| QQQ | blocked_floor_cap_and_review_backlog | 0.0596% | benchmark fallback이지만 1주 ask `738.01 USD`가 validation floor cap 약 `506.89 USD`를 초과하고 buy backlog stop도 유지 |
| NOK | blocked_validation_lifecycle_add_block | 0.0711% | due review add-block과 `pending_1d_count=18` buy throttle이 동시에 유지 |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| RGTI | watch | `duplicate_symbol_side_same_day` | quote/spread와 held qty는 정상이나 same-day earlier sell order 이력이 재제출을 막음 |
| PFE | watch | `duplicate_symbol_side_same_day` | same-day trim fill 1건 뒤라 추가 same-side trim 비허용 |
| SO | watch | `spread_within_policy` | trim rationale는 남지만 submit-boundary spread fail이 첫 hard blocker |

## 주문/체결

- Planned orders: 0
- Submitted orders: 0
- `place_stock_order` 호출: 없음
- Same-day order history seen live: `AVGO` sell 1주 `filled_avg_price=387.76 USD`, `PFE` sell 1주 `25.94 USD`, `RGTI` sell 7주 `status=canceled` at `2026-06-16T14:31:08.972628Z`
- Post-trade reconciliation: 이번 cycle 신규 submit attempt는 없었다. live Alpaca recheck 기준 open orders `0`, positions `33`, `RGTI qty_available=28`, cash `30,250.04 USD`, portfolio value `101,378.20 USD`를 재확인했다.

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | 62 symbols, SPY/QQQ 포함, final candidates 6개 |
| `check-mcp-coverage.py --strict --json` | PASS | Alpaca core pass, positive research 3개, Alpha/Firecrawl non-core gaps |
| `check-risk-policy.py --json` | PASS | current positions/no open orders 포함, `orders=[]` no-submit plan |

## 산출물

- Report: `wiki/current-runs/daily/2026-06-16-2331-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-16-2331-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-16-2331-hourly-autopilot.json`
- Runtime gate evaluation: `wiki/evidence-store/sources/2026-06-16-2331-hourly-autopilot-runtime-gate-evaluation.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-16-2331-hourly-autopilot-post-trade.json`

## 지표 설명

- `duplicate symbol/side discipline`: 같은 미국 거래일에 이미 제출된 동일 symbol/side 주문을 반복 제출하지 않는 submit safety 규칙이다. 이번 cycle에서는 filled `PFE` sell과 canceled `RGTI` sell 모두 재제출 차단 근거로 남았다.
- `validation floor per-order cap`: floor-size learning buy도 `portfolio_value * 0.5%` 상한을 넘을 수 없다. 이번 cycle의 cap은 약 `506.89 USD`라 `SPY/QQQ` 1주가 초과했다.
- `review_backlog_pending_1d_count`: validation buy 1D review backlog count다. 이번 cycle에서는 `18`이라 YAML stop threshold `12`를 넘어 신규 buy가 차단됐다.
- `sell_candidate_diagnostics`: 실행하지 않은 trim 후보도 why-not evidence를 남겨 후속 analyst review와 policy learning에 사용한다.
