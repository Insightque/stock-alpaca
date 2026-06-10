# 2026-06-11-0131-hourly-autopilot

## 요약

`0131` scheduled hourly-autopilot은 scheduler-owned stale cleanup/core/research preflight를 source-of-record로 사용했고, live Alpaca MCP로 submit 직전 clock/account/open orders/positions/same-day fills/watchlists/quotes/assets를 짧게 재확인했다. stale cleanup과 live open-order check 모두 0건이라 lifecycle blocker는 없었고, review backlog는 `pending_1d_count=9`라 신규 buy 슬롯만 `1`개로 축소됐지만 risk-reducing sell/trim 평가는 독립적으로 유지됐다.

sell-first 재평가에서는 `AVGO`와 `RGTI`가 모두 same-day filled trim duplicate에 막혔고 `SO`는 trim decision-grade metric gap이 지속됐다. buy fallback으로 이동한 뒤 `SPY/QQQ`는 validation floor per-order cap, `COP/JNJ/XOM/PFE/BAC/WMT/SLB`는 same-day buy duplicate가 남았고 `CVX`는 spread는 정상화됐지만 같은 energy sleeve의 same-day buy 누적 때문에 다른 cluster fallback 우선순위로 밀렸다. 따라서 `AMZN` 1주 validation buy @ `239.33 USD`를 direct Alpaca MCP submit 대상으로 선택했다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env`와 scheduler artifact 기준 `ALPACA_PAPER_TRADE=true` |
| Market clock | PASS | live Alpaca clock `2026-06-10T12:37:07.385153891-04:00`, regular market open |
| Stale order lifecycle | PASS | scheduler cleanup과 live `get_orders(status=open)` 모두 open orders `0`건 |
| Alpaca core MCP | PASS | scheduler core preflight hard gate pass + live clock/account/orders/positions/quotes 재확인 |
| Research MCP | PASS tiered | SEC EDGAR/FRED/Firecrawl/Yahoo positive, Alpha throttle `provider_error` gap only |
| Universe strict | PASS | metadata universe `62`개, SPY/QQQ 포함 |
| Review backlog throttle | REDUCED PASS | `pending_1d_count=9`로 buy 슬롯 `1`개로 축소, sell/trim은 비차단 |
| Quote/spread | PASS for AMZN | AMZN quote `239.00/239.33`, spread `0.1379%`, quote age `0.72`분 |
| Risk plan | PASS | `check-risk-policy.py --json` PASS (target cash 경고만 유지) |
| Final submit path | PASS | whole-share/day-limit/stock, duplicate/open-order conflict 없음, source refs 확보 |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| AVGO | blocked_duplicate_same_day | 1.1921% | same-day filled trim이 있어 추가 sell 비허용 |
| RGTI | blocked_duplicate_same_day | 0.0503% | same-day filled trim이 있어 추가 sell 비허용 |
| SO | blocked_metric_gap | 0.0213% | quote/spread는 정상이나 trim decision-grade expected-excess/replacement margin 공백 지속 |
| AMZN | selected_buy | 0.1379% | research preflight 포함, mega-cap AI/cloud fallback, same-day duplicate/open-order conflict 없음 |
| CVX | backup_buy | 0.2240% | spread는 정상화됐지만 same-day energy sleeve buy 누적으로 different-cluster fallback보다 우선순위가 낮다 |
| GOOGL | lower_rank_backup | 0.0223% | quote/spread는 양호하지만 최근 validation review 약세가 계속돼 AMZN보다 replacement rank가 낮다 |
| NKE | lower_rank_backup | 0.0226% | consumer turnaround review 약세가 남아 AMZN보다 portfolio contribution이 낮다 |
| SPY | blocked_floor_cap | 0.0055% | 1주 ask가 validation floor per-order cap 초과 |
| QQQ | blocked_floor_cap | 0.0100% | 1주 ask가 validation floor per-order cap 초과 |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| AVGO | watch | duplicate_symbol_side_same_day | ai_semiconductor warning band trim trigger는 active지만 same-day filled trim이 이미 있다 |
| RGTI | watch | duplicate_symbol_side_same_day | speculative loss-control trim trigger는 active지만 same-day filled trim이 이미 있다 |
| SO | watch | sell_metric_gap | quote/spread는 통과했지만 trim decision-grade metric gap이 남는다 |

## 주문/체결

### 제출 전 게이트 요약

paper mode `true`; market clock `2026-06-10T12:37:07.385153891-04:00`; order plan path `wiki/trade-ledger/orders/2026-06-11-0131-hourly-autopilot.json`; universe strict `PASS`; MCP strict `PASS`; risk validator `PASS`; AMZN quote freshness `0.72`분; spread `0.1379%`; order shape `buy 1 share / limit 239.33 / day / stock / regular session`; duplicate/open-order check `PASS`; source refs는 `0131` stale cleanup/core/research preflight, runtime gate snapshot, policy/review/AMZN artifacts다.

| Symbol | Side | Qty | Limit | Order id | Result |
| --- | --- | ---: | ---: | --- | --- |
| AMZN | buy | 1 | 239.33 | `d23787d5-be1a-4b35-a08e-b43670b24265` | `status=new`, `filled_qty=0` |

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | 62 symbols, SPY/QQQ 포함, pre_mcp_shortlist 10개 |
| `check-mcp-coverage.py --strict --json` | PASS | Alpaca core pass, positive research 4개, Alpha throttle gap only |
| `check-risk-policy.py --json` | PASS | target cash 경고만 남기고 AMZN floor-size validation buy risk gate 통과 |

## 제출 후 정산

- `place_stock_order`는 정상 반환됐고 `order_id=d23787d5-be1a-4b35-a08e-b43670b24265`, `client_order_id=hourly-20260611-0131-buy-amzn`로 기록됐다.
- `get_order_by_id`/`get_order_by_client_id` 재확인 기준 주문은 아직 `status=new`, `filled_qty=0` open order다.
- `get_orders(status=all, symbols=AMZN, after=2026-06-10T00:00:00Z)` 기준 same-day `AMZN` buy order는 1건이며 아직 미체결이다.
- `get_orders(status=open)` 기준 open orders는 `1`건이고 해당 주문만 남아 있다.
- `get_all_positions` 기준 positions는 `33`개 유지이며 `AMZN`은 아직 `5주`, `avg_entry_price=262.386`, `qty_available=5`로 unchanged다.
- `get_account_info` snapshot은 portfolio value `97,956.19 USD`, cash `31,694.49 USD`, buying power `296,797.56 USD`다.
- `get_account_activities(activity_types=FILL, after=2026-06-10)`에는 새 `AMZN` fill이 아직 없고 earlier same-day `SLB/COP/JNJ/XOM/PFE/BAC/WMT` buy fills, `RGTI/AVGO` sell fills, `AAPL` after-hours fills만 남아 있다.
- 이 주문은 open-order lifecycle 대상으로 다음 cycle stale cleanup/reconcile에서 다시 점검한다.

## 산출물

- Report: `wiki/current-runs/daily/2026-06-11-0131-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-11-0131-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-11-0131-hourly-autopilot.json`
- Runtime gate evaluation: `wiki/evidence-store/sources/2026-06-11-0131-hourly-autopilot-runtime-gate-evaluation.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-11-0131-hourly-autopilot-post-trade.json`
- Submit trace: `wiki/evidence-store/sources/2026-06-11-0131-hourly-autopilot-deterministic-submit.json`

## 지표 설명

- `expected_excess_return_20d_pct`: 후보의 향후 20거래일 기대 초과수익 추정치다. 이번 AMZN floor-size validation buy는 hard gate 통과 이후 fallback different-cluster 역할만 반영해 `0.61`로 낮게 둔다.
- `review_backlog_pending_1d_count`: 아직 1D review를 기다리는 validation buy 수다. `9`건이라 신규 buy 슬롯이 `1`개로 축소됐다.
- `spread_pct`: `(ask-bid)/ask*100` 기준 호가 스프레드다. regular-session hard gate는 `0.50%` 이하다.
- `sell_candidate_diagnostics`: 실행하지 않은 trim 후보도 why-not evidence를 남겨 후속 analyst review와 policy learning에 사용한다.
