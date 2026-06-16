# 2026-06-17-0011-hourly-autopilot scheduled paper autopilot

## 요약

`0011` scheduled hourly-autopilot은 scheduler-owned stale cleanup/core/research preflight를 source-of-record로 사용했다. preflight clock `2026-06-16T11:11:11.293655652-04:00`, account `ACTIVE`, positions `33`, fresh IEX quote rows는 모두 20분 이내라 Alpaca core hard gate를 PASS 처리했다. Research tiered gate도 `SEC EDGAR/FRED/Yahoo Finance` pass로 strict submit threshold `3` confirmations를 충족했고, `Alpha Vantage`는 `provider_error`, `Firecrawl`은 credits 부족 `unknown` gap only로 유지했다.

이번 cycle의 live boundary recheck는 `2026-06-16T11:13:39.032668607-04:00` clock, account `ACTIVE`, open orders `0`, same-day order history `4건(AVGO fill, RGTI cancel, PFE fill, SO fill)`을 확인했다. `SO`는 직전 `2351` fill 이후에도 quote `94.67/94.70` spread `0.0317%`로 정상 trim path를 유지했지만, 이제는 `2026-06-16T14:58:02.526808Z` same-day sell fill이 생겨 duplicate symbol/side discipline이 추가 trim을 막는다. `RGTI`와 `PFE`도 같은 미국 거래일 sell history 때문에 동일 duplicate gate가 유지된다. buy fallback은 `review_backlog_pending_1d_count=18`가 stop threshold `12`를 넘는 상태에서 `SPY/QQQ`가 validation floor per-order cap 약 `507.53 USD`를 초과하고, `NOK`는 lifecycle add-block이 계속 열려 있어 submit path를 만들지 못했다. 결과적으로 이번 cycle은 hard platform/MCP/universe/risk gate는 PASS했지만 exact duplicate/backlog/floor-cap gate 때문에 minimum learning order 1건을 만들지 못한 submit-mode no-op다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env` 기준 `ALPACA_PAPER_TRADE=true` |
| Market clock | PASS | live `get_clock` `2026-06-16T11:13:39.032668607-04:00`, regular market open |
| Stale order lifecycle | PASS | `0011` stale cleanup artifact 기준 stale candidates/open orders 모두 0 |
| Alpaca core MCP | PASS | scheduler core preflight hard gate `pass` + live boundary recheck |
| Research MCP | PASS tiered | SEC EDGAR/FRED/Yahoo positive 3개, Alpha `provider_error`, Firecrawl credit gap |
| Universe strict | PASS | broad metadata universe `62`개, SPY/QQQ 포함 |
| Review backlog throttle | BUY BLOCK ONLY | `pending_1d_count=18`가 stop threshold `12` 초과, sell/trim에는 비적용 |
| Quote/spread | PASS/MIXED | `SO/RGTI/PFE/SPY/QQQ/NOK` 모두 spread cap 이내 |
| Risk plan | PASS | `check-risk-policy.py --json` 기준 current positions/no open orders 포함, `orders=[]` 허용 |
| Final submit path | NO SUBMIT | `SO/RGTI/PFE` same-day duplicate symbol/side, `SPY/QQQ` floor cap+review backlog, `NOK` validation lifecycle add-block으로 minimum learning order를 만들지 못함 |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| SO | blocked_same_day_duplicate_sell | 0.0317% | repeated weak-review trim rationale와 spread pass는 유지됐지만 `2026-06-16T14:58:02.526808Z` same-day sell fill 1건이 이미 있어 추가 same-side trim 비허용 |
| RGTI | blocked_same_day_duplicate_sell | 0.0469% | speculative trim trigger와 spread pass는 유지되지만 same-day earlier `sell` order `hourly-20260616-2251-sell-rgti`가 이미 존재 |
| PFE | blocked_same_day_duplicate_sell | 0.0385% | `2026-06-16T14:18:55.368488Z` same-day trim fill 1건이 이미 있어 추가 same-side sell 비허용 |
| SPY | blocked_floor_cap_and_review_backlog | 0.0040% | benchmark fallback이지만 1주 ask `753.51 USD`가 validation floor cap 약 `507.53 USD`를 초과하고 buy backlog stop도 유지 |
| QQQ | blocked_floor_cap_and_review_backlog | 0.0420% | benchmark fallback이지만 1주 ask `738.09 USD`가 validation floor cap 약 `507.53 USD`를 초과하고 buy backlog stop도 유지 |
| NOK | blocked_validation_lifecycle_add_block | 0.0713% | due review add-block과 `pending_1d_count=18` buy throttle이 동시에 유지 |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| SO | watch | `duplicate_symbol_side_same_day` | trim rationale와 quote/spread는 정상이지만 same-day `SO` sell fill 이후 재제출 금지 |
| RGTI | watch | `duplicate_symbol_side_same_day` | quote/spread와 held qty는 정상이나 same-day earlier sell order 이력이 재제출을 막음 |
| PFE | watch | `duplicate_symbol_side_same_day` | same-day trim fill 1건 뒤라 추가 same-side trim 비허용 |

## 주문/체결

- Planned orders: 0
- Submitted orders: 0
- `place_stock_order` 호출: 없음
- Same-day order history seen live: `AVGO` sell 1주 `filled_avg_price=387.76 USD`, `PFE` sell 1주 `25.94 USD`, `SO` sell 1주 `94.77 USD`, `RGTI` sell 7주 `status=canceled` at `2026-06-16T14:31:08.972628Z`
- Post-trade reconciliation: 이번 cycle 신규 submit attempt는 없었다. live Alpaca recheck 기준 open orders `0`, positions `33`, `SO qty=5`, `RGTI qty_available=28`, cash `30,344.81 USD`, portfolio value `101,506.73 USD`를 재확인했다.

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | 62 symbols, SPY/QQQ 포함, final candidates 6개 |
| `check-mcp-coverage.py --strict --json` | PASS | Alpaca core pass, positive research 3개, Alpha/Firecrawl non-core gaps |
| `check-risk-policy.py --json` | PASS | current positions/no open orders 포함, `orders=[]` no-submit plan |

## 산출물

- Report: `wiki/current-runs/daily/2026-06-17-0011-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-17-0011-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-17-0011-hourly-autopilot.json`
- Runtime gate evaluation: `wiki/evidence-store/sources/2026-06-17-0011-hourly-autopilot-runtime-gate-evaluation.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-17-0011-hourly-autopilot-post-trade.json`

## 지표 설명

- `duplicate symbol/side discipline`: 같은 미국 거래일에 이미 제출된 동일 symbol/side 주문을 반복 제출하지 않는 submit safety 규칙이다. 이번 cycle에서는 filled `SO`/`PFE` sell과 canceled `RGTI` sell 모두 재제출 차단 근거로 남았다.
- `validation floor per-order cap`: floor-size learning buy도 `portfolio_value * 0.5%` 상한을 넘을 수 없다. 이번 cycle의 cap은 약 `507.53 USD`라 `SPY/QQQ` 1주가 초과했다.
- `review_backlog_pending_1d_count`: validation buy 1D review backlog count다. 이번 cycle에서는 `18`이라 YAML stop threshold `12`를 넘어 신규 buy가 차단됐다.
- `sell_candidate_diagnostics`: 실행하지 않은 trim 후보도 why-not evidence를 남겨 후속 analyst review와 policy learning에 사용한다.
