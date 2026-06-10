# 2026-06-11-0211-hourly-autopilot

## 요약

`0211` scheduled hourly-autopilot은 scheduler-owned stale cleanup/core/research preflight를 source-of-record로 사용했고, live Alpaca MCP로 submit 직전 clock/account/open orders/positions/same-day fills/watchlists/quotes/asset를 다시 확인했다. stale cleanup과 live open-order check 모두 0건이라 lifecycle blocker는 없었고, `AMZN` 0131 open order는 이번 cycle 전 `2026-06-10T16:41:37.562873Z` fill로 정리됐다.

sell-first 재평가에서는 `AVGO`가 post-earnings de-risking rationale는 유지하지만 live spread가 policy cap을 넘었고, `RGTI`는 spread는 정상이나 same-day sell duplicate가 남았으며, `SO`는 quote/spread 정상화 이후에도 trim decision-grade metric gap이 남았다. buy fallback에서는 `FCX/AMZN/SLB/COP/JNJ/XOM/PFE/BAC/WMT/AAPL`이 same-day buy duplicate, `SPY/QQQ`가 validation floor per-order cap, `CVX/MCD`가 spread fail, `HOOD`가 wiki thesis evidence 부족으로 밀렸다. 남은 thesis-covered fallback 중 `NEE`는 FRED macro confirmation을 유지한 utilities/rate-sensitive diversifier로서 live quote `85.27/85.29`, spread `0.0235%`, active tradable NYSE stock, duplicate/open-order conflict 부재를 모두 충족해 1주 floor-size validation buy 후보로 승격됐고, direct Alpaca MCP submit 결과 `85.22 USD`로 즉시 체결됐다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | scheduler artifact와 runtime policy 기준 `ALPACA_PAPER_TRADE=true` |
| Market clock | PASS | live Alpaca clock `2026-06-10T13:13:27.721752232-04:00`, regular market open |
| Stale order lifecycle | PASS | scheduler cleanup과 live `get_orders(status=open)` 모두 open orders `0`건 |
| Alpaca core MCP | PASS | scheduler core preflight hard gate pass + live clock/account/orders/positions/quotes 재확인 |
| Research MCP | PASS tiered | SEC EDGAR/FRED/Firecrawl/Yahoo positive, Alpha empty-response gap only |
| Universe strict | PASS | metadata universe `62`개, SPY/QQQ 포함 |
| Review backlog throttle | REDUCED PASS | `pending_1d_count=9`라 신규 buy 슬롯은 `1`개, sell/trim은 비차단 |
| Quote/spread | PASS for NEE | NEE quote `85.27/85.29`, spread `0.0235%`, quote age `0.01`분 |
| Risk plan | PASS | `check-risk-policy.py --json` PASS, staged deployment warning only |
| Final submit path | PASS | whole-share/day-limit/stock, duplicate/open-order conflict 없음, source refs 확보 |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| AVGO | blocked_spread_and_duplicate | 1.5265% | trim rationale는 유지되지만 spread hard gate fail과 same-day sell duplicate가 겹친다 |
| RGTI | blocked_duplicate_same_day | 0.0501% | speculative loss-control trigger는 유지되지만 same-day sell duplicate가 남는다 |
| SO | blocked_metric_gap | 0.0318% | quote/spread는 통과했지만 trim decision-grade expected-excess/replacement margin 공백 지속 |
| NEE | selected_buy | 0.0235% | FRED-confirmed utilities diversifier, same-day duplicate/open-order conflict 없음 |
| GOOGL | lower_rank_backup | 0.0420% | mega-cap quality review 약세가 누적돼 NEE보다 replacement rank가 낮다 |
| NKE | lower_rank_backup | 0.0227% | consumer turnaround review 약세가 남아 NEE보다 우선순위가 낮다 |
| CVX | blocked_spread | 7.9111% | live quote wide spread로 hard gate fail |
| SPY | blocked_floor_cap | 0.0041% | 1주 ask가 validation floor per-order cap 초과 |
| QQQ | blocked_floor_cap | 0.0072% | 1주 ask가 validation floor per-order cap 초과 |
| MCD | blocked_spread | 1.2540% | live spread가 policy cap을 크게 초과 |
| HOOD | blocked_thesis_evidence_missing | 0.0339% | quote/spread는 양호하지만 reusable ticker thesis evidence가 wiki에 얕다 |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| AVGO | watch | spread_within_policy | spread fail과 same-day sell duplicate가 함께 남아 추가 trim 불가 |
| RGTI | watch | duplicate_symbol_side_same_day | speculative trim trigger는 active지만 same-day filled trim이 이미 있다 |
| SO | watch | sell_metric_gap | quote/spread는 통과했지만 trim decision-grade metric gap이 남는다 |

## 주문/체결

### 제출 전 게이트 요약

paper mode `true`; market clock `2026-06-10T13:13:27.721752232-04:00`; order plan path `wiki/trade-ledger/orders/2026-06-11-0211-hourly-autopilot.json`; universe strict `PASS`; MCP strict `PASS`; risk validator `PASS`; NEE quote freshness `0.01`분; spread `0.0235%`; order shape `buy 1 share / limit 85.29 / day / stock / regular session`; duplicate/open-order check `PASS`; source refs는 `0211` stale cleanup/core/research preflight, runtime gate snapshot, policy/review/NEE artifacts다.

| Symbol | Side | Qty | Limit | Order id | Result |
| --- | --- | ---: | ---: | --- | --- |
| NEE | buy | 1 | 85.29 | `7fd2a9cf-bde9-454e-83f0-64a8a722409d` | `filled_avg_price=85.22 USD` |

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | 62 symbols, SPY/QQQ 포함, pre_mcp_shortlist 10개 |
| `check-mcp-coverage.py --strict --json` | PASS | Alpaca core pass, positive research 4개, Alpha empty-response gap only |
| `check-risk-policy.py --json` | PASS | staged deployment warning only |

## 제출 후 정산

- `place_stock_order`는 정상 반환됐고 `client_order_id=hourly-20260611-0211-buy-nee`, `order_id=7fd2a9cf-bde9-454e-83f0-64a8a722409d`로 기록됐다.
- `get_order_by_id`와 `get_order_by_client_id` 모두 주문이 `filled`, `filled_qty=1`, `filled_avg_price=85.22 USD`임을 재확인했다.
- `get_orders(status=all, symbols=NEE, after=2026-06-10T17:15:00Z)` 기준 same-day NEE buy order는 이번 1건뿐이다.
- `get_orders(status=open)` 기준 open orders는 `0`건이다.
- `get_all_positions` 기준 positions는 `33`개 유지이며 `NEE`는 `4주 -> 5주`, `avg_entry_price=86.44`, `qty_available=5`로 증가했다.
- `get_account_info` snapshot은 portfolio value `97,402.72 USD`, cash `31,307.73 USD`, buying power `295,236.48 USD`다.
- `get_account_activities(activity_types=FILL, after=2026-06-10T17:15:00Z)`는 새 `NEE` fill 1건만 반환했다.

## 산출물

- Report: `wiki/current-runs/daily/2026-06-11-0211-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-11-0211-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-11-0211-hourly-autopilot.json`
- Runtime gate evaluation: `wiki/evidence-store/sources/2026-06-11-0211-hourly-autopilot-runtime-gate-evaluation.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-11-0211-hourly-autopilot-post-trade.json`
- Submit trace: `wiki/evidence-store/sources/2026-06-11-0211-hourly-autopilot-deterministic-submit.json`

## 지표 설명

- `sell_candidate_diagnostics`: 실행하지 않은 trim 후보도 why-not evidence를 남겨 후속 analyst review와 policy learning에 사용한다.
- `review_backlog_pending_1d_count`: validation buy 1D review backlog count다. 이번 cycle에서는 `9`라 신규 buy 슬롯이 `1`개로 축소된다.
- `spread_pct`: `(ask-bid)/ask*100` 기준 호가 스프레드다. regular-session hard gate는 `0.50%` 이하다.
- `validation_floor_per_order_cap`: `confidence_tiers.validation_floor.max_notional_pct=0.005`에 따라 계좌 가치의 0.5%를 넘는 1주 fallback 매수는 막는다.
