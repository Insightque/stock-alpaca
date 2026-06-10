# 2026-06-11-0151-hourly-autopilot

## 요약

`0151` scheduled hourly-autopilot은 scheduler-owned stale cleanup/core/research preflight를 source-of-record로 사용했고, live Alpaca MCP로 submit 직전 clock/account/open orders/positions/same-day fills/watchlists/quotes/asset를 다시 확인했다. stale cleanup과 live open-order check 모두 0건이라 lifecycle blocker는 없었고, `AMZN` 0131 open order는 이번 cycle 전 already filled로 정리됐다.

sell-first 재평가에서는 `AVGO`가 post-earnings de-risking rationale는 유지하지만 live spread가 policy cap을 넘었고, `RGTI`는 spread는 정상이나 same-day sell duplicate가 남았으며, `SO`는 quote/spread 정상화 이후에도 trim decision-grade metric gap이 남았다. buy fallback에서는 `SPY/QQQ`가 validation floor per-order cap, `AAPL/BAC/WMT/SLB/AMZN`이 same-day buy duplicate, `NVDA`가 반도체 cluster 집중, `GOOGL/NKE/NEE`가 weak-to-neutral review 열세로 밀려 `FCX` 1주 materials/mining floor-size add가 가장 보수적으로 hard gate를 모두 통과하는 후보가 됐다. direct Alpaca MCP submit 결과 `FCX` 1주는 `62.21 USD`로 즉시 체결됐다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | scheduler artifact와 runtime policy 기준 `ALPACA_PAPER_TRADE=true` |
| Market clock | PASS | live Alpaca clock `2026-06-10T12:59:27.277345873-04:00`, regular market open |
| Stale order lifecycle | PASS | scheduler cleanup과 live `get_orders(status=open)` 모두 open orders `0`건 |
| Alpaca core MCP | PASS | scheduler core preflight hard gate pass + live clock/account/orders/positions/quotes 재확인 |
| Research MCP | PASS tiered | SEC EDGAR/FRED/Firecrawl/Yahoo positive, Alpha throttle `provider_error` gap only |
| Universe strict | PASS | metadata universe `62`개, SPY/QQQ 포함 |
| Review backlog throttle | REDUCED PASS | `pending_1d_count=9`라 신규 buy 슬롯은 `1`개, sell/trim은 비차단 |
| Quote/spread | PASS for FCX | FCX quote `62.19/62.22`, spread `0.0482%`, quote age `0.09`분 |
| Risk plan | PASS | `check-risk-policy.py --json` PASS, staged deployment warning only |
| Final submit path | PASS | whole-share/day-limit/stock, duplicate/open-order conflict 없음, source refs 확보 |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| AVGO | blocked_spread_and_duplicate | 1.5258% | trim rationale는 유지되지만 spread hard gate fail과 same-day sell duplicate가 겹친다 |
| RGTI | blocked_duplicate_same_day | 0.1002% | speculative loss-control trigger는 유지되지만 same-day sell duplicate가 남는다 |
| SO | blocked_metric_gap | 0.3069% | quote/spread는 정상이나 trim decision-grade expected-excess/replacement margin 공백 지속 |
| FCX | selected_buy | 0.0482% | preflight coverage 유지, same-day duplicate/open-order conflict 없음, materials/mining diversifier |
| CVX | backup_buy | 0.0209% | spread는 양호하지만 energy sleeve 중복과 최근 review 열세로 FCX보다 낮다 |
| GOOGL | lower_rank_backup | 0.1839% | mega-cap quality review 약세가 누적돼 FCX보다 replacement rank가 낮다 |
| NEE | lower_rank_backup | 0.0352% | utilities/rate-sensitive review 약세가 누적돼 FCX보다 우선순위가 낮다 |
| SPY | blocked_floor_cap | 0.0123% | 1주 ask가 validation floor per-order cap 초과 |
| QQQ | blocked_floor_cap | 0.0472% | 1주 ask가 validation floor per-order cap 초과 |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| AVGO | watch | spread_within_policy | spread fail과 same-day sell duplicate가 함께 남아 추가 trim 불가 |
| RGTI | watch | duplicate_symbol_side_same_day | speculative trim trigger는 active지만 same-day filled trim이 이미 있다 |
| SO | watch | sell_metric_gap | quote/spread는 통과했지만 trim decision-grade metric gap이 남는다 |

## 주문/체결

### 제출 전 게이트 요약

paper mode `true`; market clock `2026-06-10T12:59:27.277345873-04:00`; order plan path `wiki/trade-ledger/orders/2026-06-11-0151-hourly-autopilot.json`; universe strict `PASS`; MCP strict `PASS`; risk validator `PASS`; FCX quote freshness `0.09`분; spread `0.0482%`; order shape `buy 1 share / limit 62.22 / day / stock / regular session`; duplicate/open-order check `PASS`; source refs는 `0151` stale cleanup/core/research preflight, runtime gate snapshot, policy/review/FCX artifacts다.

| Symbol | Side | Qty | Limit | Order id | Result |
| --- | --- | ---: | ---: | --- | --- |
| FCX | buy | 1 | 62.22 | `dc2dd11d-89ef-4664-a300-65a801ee30e7` | `filled_avg_price=62.21 USD` |

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | 62 symbols, SPY/QQQ 포함, pre_mcp_shortlist 10개 |
| `check-mcp-coverage.py --strict --json` | PASS | Alpaca core pass, positive research 4개, Alpha throttle `provider_error` only |
| `check-risk-policy.py --json` | PASS | staged deployment warning only |

## 제출 후 정산

- `place_stock_order`는 정상 반환됐고 `client_order_id=hourly-20260611-0151-buy-fcx`, `order_id=dc2dd11d-89ef-4664-a300-65a801ee30e7`로 기록됐다.
- `get_order_by_id`와 `get_order_by_client_id` 모두 주문이 `filled`, `filled_qty=1`, `filled_avg_price=62.21 USD`임을 재확인했다.
- `get_orders(status=all, symbols=FCX, after=2026-06-10T16:50:00Z)` 기준 same-day FCX buy order는 이번 1건뿐이다.
- `get_orders(status=open)` 기준 open orders는 `0`건이다.
- `get_all_positions` 기준 positions는 `33`개 유지이며 `FCX`는 `4주 -> 5주`, `avg_entry_price=64.912`, `qty_available=5`로 증가했다.
- `get_account_info` snapshot은 portfolio value `97,708.23 USD`, cash `31,392.95 USD`, buying power `296,075.87 USD`다.
- `get_account_activities(activity_types=FILL, after=2026-06-10T16:55:00Z)`는 새 `FCX` fill 1건만 반환했다.

## 산출물

- Report: `wiki/current-runs/daily/2026-06-11-0151-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-11-0151-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-11-0151-hourly-autopilot.json`
- Runtime gate evaluation: `wiki/evidence-store/sources/2026-06-11-0151-hourly-autopilot-runtime-gate-evaluation.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-11-0151-hourly-autopilot-post-trade.json`
- Submit trace: `wiki/evidence-store/sources/2026-06-11-0151-hourly-autopilot-deterministic-submit.json`

## 지표 설명

- `sell_candidate_diagnostics`: 실행하지 않은 trim 후보도 why-not evidence를 남겨 후속 analyst review와 policy learning에 사용한다.
- `review_backlog_pending_1d_count`: validation buy 1D review backlog count다. 이번 cycle에서는 `9`라 신규 buy 슬롯이 `1`개로 축소된다.
- `spread_pct`: `(ask-bid)/ask*100` 기준 호가 스프레드다. regular-session hard gate는 `0.50%` 이하다.
- `validation_floor_per_order_cap`: `confidence_tiers.validation_floor.max_notional_pct=0.005`에 따라 계좌 가치의 0.5%를 넘는 1주 fallback 매수는 막는다.
