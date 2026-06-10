# 2026-06-11-0111-hourly-autopilot

## 요약

`0111` scheduled hourly-autopilot은 scheduler-owned stale cleanup/core/research preflight를 source-of-record로 사용했고, live Alpaca MCP로 submit 직전 clock/account/open orders/positions/same-day fills/watchlists/quotes/assets를 짧게 재확인했다. stale cleanup과 live open-order check 모두 0건이라 lifecycle blocker는 없었고, review backlog는 `pending_1d_count=9`라 신규 buy 슬롯만 `1`개로 축소됐지만 risk-reducing sell/trim 평가는 독립적으로 유지됐다.

sell-first 재평가에서는 `AVGO`와 `RGTI`가 모두 same-day filled trim duplicate에 막혔고 `SO`는 trim decision-grade metric gap이 지속됐다. buy fallback으로 이동한 뒤 `SPY/QQQ`는 validation floor per-order cap, `COP/JNJ/XOM/PFE/BAC/WMT`는 same-day buy duplicate, `CVX`는 live spread fail이 남아 `SLB` 1주 validation buy @ `56.55 USD`를 direct Alpaca MCP로 제출했다. immediate reconciliation 기준 이 주문은 `filled_avg_price=56.45 USD`로 즉시 전량 체결됐다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env`와 scheduler artifact 기준 `ALPACA_PAPER_TRADE=true` |
| Market clock | PASS | live Alpaca clock `2026-06-10T12:13:20.935556205-04:00`, regular market open |
| Stale order lifecycle | PASS | scheduler cleanup과 live `get_orders(status=open)` 모두 open orders `0`건 |
| Alpaca core MCP | PASS | scheduler core preflight hard gate pass + live clock/account/orders/positions/quotes 재확인 |
| Research MCP | PASS tiered | SEC EDGAR/FRED/Firecrawl/Yahoo positive, Alpha `empty_response` gap only |
| Universe strict | PASS | metadata universe `62`개, SPY/QQQ 포함 |
| Review backlog throttle | REDUCED PASS | `pending_1d_count=9`로 buy 슬롯 `1`개로 축소, sell/trim은 비차단 |
| Quote/spread | PASS for SLB | SLB quote `56.54/56.55`, spread `0.0177%`, quote age `0.03`분 |
| Risk plan | PASS | `check-risk-policy.py --json` PASS |
| Final submit path | PASS | whole-share/day-limit/stock, duplicate/open-order conflict 없음, source refs 확보 |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| AVGO | blocked_duplicate_same_day | 0.6800% | same-day filled trim `hourly-20260610-2251-sell-avgo`가 있어 추가 sell 비허용 |
| RGTI | blocked_duplicate_same_day | 0.1003% | same-day filled trim `hourly-20260610-2311-sell-rgti`가 있어 추가 sell 비허용 |
| SO | blocked_metric_gap | 0.0213% | quote/spread는 정상이나 trim decision-grade expected-excess/replacement margin 공백 지속 |
| SLB | selected_buy | 0.0177% | energy-services existing diversifier, positive recent review, research preflight 포함, same-day duplicate/open-order conflict 없음 |
| NEE | backup_buy | 0.0352% | utilities backup candidate지만 최근 review 약세가 이어져 SLB보다 replacement rank가 낮다 |
| PLTR | lower_rank_backup | 0.0455% | software/AI momentum 후보지만 SLB보다 분산 기여가 낮다 |
| CVX | blocked_spread | 6.7751% | live bid/ask 비대칭으로 spread hard gate 실패 |
| SPY | blocked_floor_cap | 0.0096% | 1주 ask가 validation floor per-order cap 초과 |
| QQQ | blocked_floor_cap | 0.0100% | 1주 ask가 validation floor per-order cap 초과 |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| AVGO | watch | duplicate_symbol_side_same_day | ai_semiconductor warning band trim trigger는 active지만 same-day filled trim이 이미 있다 |
| RGTI | watch | duplicate_symbol_side_same_day | speculative loss-control trim trigger는 active지만 same-day filled trim이 이미 있다 |
| SO | watch | sell_metric_gap | quote/spread는 통과했지만 trim decision-grade metric gap이 남는다 |

## 주문/체결

### 제출 전 게이트 요약

paper mode `true`; market clock `2026-06-10T12:13:20.935556205-04:00`; order plan path `wiki/trade-ledger/orders/2026-06-11-0111-hourly-autopilot.json`; universe strict `PASS`; MCP strict `PASS`; risk validator `PASS`; SLB quote freshness `0.03`분; spread `0.0177%`; order shape `buy 1 share / limit 56.55 / day / stock / regular session`; duplicate/open-order check `PASS`; source refs는 `0111` stale cleanup/core/research preflight, runtime gate snapshot, policy/review/SLB artifacts다.

| Symbol | Side | Qty | Limit | Order id | Result |
| --- | --- | ---: | ---: | --- | --- |
| SLB | buy | 1 | 56.55 | `14d20183-5063-4025-9114-5e82cbcf6386` | `filled_avg_price=56.45 USD` |

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | 62 symbols, SPY/QQQ 포함, pre_mcp_shortlist 10개 |
| `check-mcp-coverage.py --strict --json` | PASS | Alpaca core pass, positive research 4개, Alpha empty-response gap only |
| `check-risk-policy.py --json` | PASS | SLB floor-size validation buy risk gate 통과 |

## 제출 후 정산

- `get_order_by_id`와 `get_order_by_client_id` 기준 `SLB` 주문은 `filled`다.
- `get_orders(status=all, symbols=SLB, after=2026-06-10T04:00:00Z)` 기준 same-day `SLB` buy order는 1건이며 `filled_qty=1`, `filled_avg_price=56.45 USD`다.
- `get_orders(status=open)` 기준 open orders는 `0`건이다.
- `get_all_positions` 기준 positions는 `33`개 유지이며 `SLB`는 `5주 -> 6주`, `avg_entry_price=55.858333`, `qty_available=6`, `market_value=338.88 USD`로 증가했다.
- `get_account_info` snapshot은 portfolio value `97,671.40 USD`, cash `31,694.49 USD`, buying power `296,306.46 USD`다.
- `get_account_activities(activity_types=FILL, after=2026-06-10)`는 새 `SLB` fill 1건과 earlier same-day `COP/JNJ/XOM/PFE/BAC/WMT` buy fills, `RGTI/AVGO` sell fills, `AAPL` after-hours fills를 반환했다.
- 새 `SLB` validation buy는 `1D/5D/20D` review bucket에 추가 추적 대상으로 남긴다.

## 산출물

- Report: `wiki/current-runs/daily/2026-06-11-0111-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-11-0111-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-11-0111-hourly-autopilot.json`
- Runtime gate evaluation: `wiki/evidence-store/sources/2026-06-11-0111-hourly-autopilot-runtime-gate-evaluation.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-11-0111-hourly-autopilot-post-trade.json`
- Submit trace: `wiki/evidence-store/sources/2026-06-11-0111-hourly-autopilot-deterministic-submit.json`

## 지표 설명

- `expected_excess_return_20d_pct`: 후보의 향후 20거래일 기대 초과수익 추정치다. 이번 SLB floor-size validation buy는 최근 1D review와 existing sleeve replacement rank를 반영해 `1.22`를 기록했다.
- `review_backlog_pending_1d_count`: 아직 1D review를 기다리는 validation buy 수다. `9`건이라 신규 buy 슬롯이 `1`개로 축소됐다.
- `spread_pct`: `(ask-bid)/ask*100` 기준 호가 스프레드다. regular-session hard gate는 `0.50%` 이하다.
- `sell_candidate_diagnostics`: 실행하지 않은 trim 후보도 why-not evidence를 남겨 후속 analyst review와 policy learning에 사용한다.
