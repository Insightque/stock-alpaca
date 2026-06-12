# 2026-06-13-0111-hourly-autopilot

## 요약

`0111` scheduled hourly-autopilot은 scheduler-owned stale cleanup/core/research preflight를 source-of-record로 사용했다. 이번 cycle의 preflight clock `2026-06-12T12:11:11.337825881-04:00`, account `ACTIVE`, positions `33`, open orders `0`, fresh IEX quote rows가 모두 20분 이내라 Alpaca core hard gate를 PASS 처리했다. Research tiered gate도 `SEC EDGAR/FRED/Firecrawl/Yahoo Finance` pass로 strict submit threshold `3` confirmations를 충분히 충족했고, `Alpha Vantage`는 one-call-per-hour throttle 때문에 `provider_error` failed row만 남겼다.

sell-first 재평가에서는 `AVGO`가 fresh IEX quote `379.28/383.90` spread `1.2107%`로 다시 policy cap `0.50%`를 넘겨 trim hard gate fail로 돌아왔고 same-day sell discipline도 계속 남았다. `RGTI`는 spread `0.0945%` pass에도 same-day sell fill 12주가 남아 duplicate sell discipline에 막혔고, `SO`는 spread `0.4136%` pass에도 trim decision-grade metric gap이 지속됐다. buy fallback에서는 `FCX/WMT/NEE`가 모두 quote/spread/duplicate 기준으로는 executable이었지만, risk validator가 `review_backlog_pending_1d_count=14`를 읽어 stop threshold `12` 초과로 신규 buy 슬롯을 `0`으로 계산했다. `SPY/QQQ`는 per-order cap 약 `501.52 USD` 초과, `NOK`는 validation lifecycle add-block이 유지돼 결과적으로 이번 cycle은 hard gates 대부분이 PASS했음에도 `review_backlog_throttle` 때문에 submit-mode no-op로 종료한다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env` 기준 `ALPACA_PAPER_TRADE=true` |
| Market clock | PASS | scheduler-owned Alpaca clock `2026-06-12T12:11:11.337825881-04:00`, regular market open |
| Stale order lifecycle | PASS | stale cleanup status `pass`; initial/remaining open orders 모두 `0` |
| Alpaca core MCP | PASS | scheduler core preflight hard gate `pass`, quote rows fresh |
| Research MCP | PASS tiered | SEC EDGAR/FRED/Firecrawl/Yahoo positive, Alpha는 one-call-per-hour throttle `provider_error` failed row only |
| Universe strict | PASS | broad metadata universe `62`개, SPY/QQQ 포함 |
| Review backlog throttle | BUY BLOCK ONLY | `pending_1d=14`, `pending_5d=13`, `pending_20d=1`; stop threshold `12` 초과 |
| Quote/spread | MIXED | `RGTI/SO/FCX/WMT/NEE/SPY/QQQ/NOK` pass, `AVGO` spread `1.2107%` fail |
| Risk plan | PASS with no-submit warning | `check-risk-policy.py --json`는 `orders=[]` no-submit plan을 통과 |
| Final submit path | NO SUBMIT | sell-first는 spread fail/duplicate/metric gap, buy path는 review_backlog_throttle가 차단 |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| FCX | blocked_review_backlog_only | 0.0586% | quote/spread는 executable이지만 review_backlog_pending_1d_count=14가 stop threshold 12를 초과 |
| AVGO | blocked_spread_fail | 1.2107% | same-day sell discipline도 남아 있지만 spread hard gate가 먼저 닫힘 |
| RGTI | blocked_same_day_duplicate_sell | 0.0945% | spread는 pass지만 same-day sell discipline 유지 |
| SO | blocked_metric_gap | 0.4136% | spread는 pass지만 trim decision-grade metric gap 지속 |
| WMT | blocked_review_backlog_only | 0.0334% | executable이지만 review_backlog_pending_1d_count=14가 stop threshold 12를 초과 |
| NEE | blocked_review_backlog_only | 0.0117% | executable이지만 review_backlog_pending_1d_count=14가 stop threshold 12를 초과 |
| SPY | blocked_floor_cap_and_review_backlog | 0.0095% | 1주 ask `739.75 USD`가 validation floor cap 약 `501.52 USD` 초과 |
| QQQ | blocked_floor_cap_and_review_backlog | 0.0362% | 1주 ask `718.39 USD`가 validation floor cap 약 `501.52 USD` 초과 |
| NOK | blocked_validation_lifecycle_add_block | 0.0674% | `blocked_add_symbols` 유지 |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| AVGO | watch | `spread_within_policy` | same-day sell discipline도 남아 있지만 spread `1.2107%`가 먼저 trim submit을 막음 |
| RGTI | watch | `duplicate_symbol_side_same_day` | spread `0.0945%`는 pass지만 same-day trim fill 12주가 남아 추가 sell 차단 |
| SO | watch | `decision_grade_metric_gap` | spread `0.4136%`는 pass지만 trim decision-grade metric gap 지속 |

## 주문/체결

- Planned orders: 0
- Submitted orders: 0
- `place_stock_order` 호출: 없음
- Same-day fills seen in source-of-record: `RGTI` sell 12주 `filled_avg_price=21.010833 USD`, `AVGO` sell 1주 `387.06 USD`, `PFE` sell 1주 `26.13 USD`

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | broad universe 62개, shortlist 9개 |
| `check-mcp-coverage.py --strict --json` | PASS | Alpaca core pass, positive research 4개, Alpha provider_error throttle only |
| `check-risk-policy.py --json` | PASS | `review_backlog_throttle`를 반영한 `orders=[]` no-submit plan |

## 산출물

- Report: `wiki/current-runs/daily/2026-06-13-0111-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-13-0111-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-13-0111-hourly-autopilot.json`
- Runtime gate evaluation: `wiki/evidence-store/sources/2026-06-13-0111-hourly-autopilot-runtime-gate-evaluation.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-13-0111-hourly-autopilot-post-trade.json`

## 지표 설명

- `review_backlog_pending_*`: 이번 cycle의 source-of-record는 `pending_1d=14`, `pending_5d=13`, `pending_20d=1`이며, buy throttle stop threshold `12`를 넘어 신규 validation buy가 차단됐다.
- `validation floor per-order cap`: `portfolio_value * 0.5%` 상한이다. 이번 cycle의 cap은 약 `501.52 USD`라 `SPY/QQQ` 1주가 초과했다.
- `same-day duplicate sell discipline`: 같은 미국 거래일에 이미 fill된 동일 symbol/side sell을 반복 제출하지 않는 규율이다. 이번 cycle에서는 `RGTI`에 직접 적용됐고 `AVGO`는 spread fail 뒤에도 동일 규율이 남아 있다.
- `sell_candidate_diagnostics`: 실행하지 않은 trim 후보도 why-not evidence를 남겨 후속 analyst review와 policy learning에 사용한다.
- `provider gap`: 이번 run의 Alpha Vantage는 one-call-per-hour throttle 때문에 `provider_error` failed row만 남았고, 나머지 4개 research confirmations가 strict MCP gate를 통과시켰다.
