# 2026-06-10-2311-hourly-autopilot

## 요약

`2311` scheduled hourly-autopilot은 scheduler-owned stale cleanup/core/research preflight를 source-of-record로 사용했고, live Alpaca MCP로 submit 직전 clock/account/open orders/positions/same-day fills/quotes를 짧게 재확인했다. stale cleanup과 live open-order check 모두 0건이라 lifecycle blocker는 없었고, review backlog는 `pending_1d_count=9`라 신규 buy 슬롯만 `1`개로 축소됐지만 risk-reducing sell/trim은 독립적으로 유지됐다.

sell-first 재평가에서는 `RGTI`가 speculative loss-control trim trigger, 큰 미실현 손실, 정상 spread, duplicate/open-order conflict 없음 조건을 모두 만족해 이번 cycle의 우선 trim 후보로 승격됐다. `AVGO`는 2251 cycle same-day filled trim이 이미 있어 duplicate sell discipline에 막혔고, `SO`는 quote/spread 정상화 후에도 decision-grade metric gap이 남았다. 따라서 buy fallback으로 가지 않고 `RGTI` 17주 trim @ `20.38 USD`를 direct Alpaca MCP로 제출했고, immediate reconciliation 기준 `filled_avg_price=20.38 USD`로 즉시 전량 체결됐다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env` paper mode와 scheduler artifact 기준 `ALPACA_PAPER_TRADE=true` |
| Market clock | PASS | live Alpaca clock `2026-06-10T10:13:52.694604269-04:00`, regular market open |
| Stale order lifecycle | PASS | scheduler cleanup과 live `get_orders(status=open)` 모두 open orders `0`건 |
| Alpaca core MCP | PASS | scheduler core preflight hard gate pass + live clock/account/orders/positions/quotes 재확인 |
| Research MCP | PASS tiered | SEC EDGAR/FRED/Firecrawl/Yahoo positive, Alpha `provider_error` throttle gap only |
| Universe strict | PASS | metadata universe `62`개, SPY/QQQ 포함 |
| Review backlog throttle | REDUCED PASS | `pending_1d_count=9`로 buy 슬롯 `1`개로 축소, sell/trim은 비차단 |
| Quote/spread | PASS for RGTI | RGTI live quote `20.38/20.39`, spread `0.0491%`, quote age 약 `0.01`분 |
| Risk plan | PASS | `check-risk-policy.py --json` PASS |
| Final submit path | PASS | whole-share/day-limit/stock, duplicate/open-order conflict 없음, source refs 확보 |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| RGTI | selected_trim | 0.0491% | speculative loss-control trim gate pass, 25% trim executable |
| AVGO | blocked_duplicate_same_day | 0.2960% | 2251 cycle same-day filled trim으로 duplicate sell discipline 적용 |
| SO | blocked_metric_gap | 0.1180% | spread 정상화 후에도 trim decision-grade metric gap 지속 |
| BAC | watch_fallback | 0.0364% | eligible buy fallback이지만 eligible RGTI trim이 우선 |
| PFE | watch_fallback | 0.0390% | eligible buy fallback이지만 eligible RGTI trim이 우선 |
| WMT | blocked_duplicate_same_day | 0.0336% | same-day buy fill `hourly-20260610-2231-buy-wmt` 이미 존재 |
| SPY | blocked_floor_cap | 0.0258% | 1주 ask `737.27 USD`가 validation floor per-order cap 초과 |
| QQQ | blocked_floor_cap | 0.0960% | 1주 ask `708.44 USD`가 validation floor per-order cap 초과 |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| RGTI | trim | executable | speculative loss-control, 큰 미실현 손실, 정상 spread, held qty 68주에서 25% trim 17주 실행 |
| AVGO | watch | duplicate_symbol_side_same_day | same-day filled trim이 이미 있어 추가 trim 비허용 |
| SO | watch | sell_metric_gap | quote/spread는 정상이나 replacement/expected-excess metric gap 지속 |

## 주문/체결

### 제출 전 게이트 요약

paper mode `true`; market clock `2026-06-10T10:13:52.694604269-04:00`; order plan path `wiki/trade-ledger/orders/2026-06-10-2311-hourly-autopilot.json`; universe strict `PASS`; MCP strict `PASS`; risk validator `PASS`; RGTI quote freshness 약 `0.01`분; spread `0.0491%`; order shape `sell 17 shares / limit 20.38 / day / stock / regular session`; duplicate/open-order check `PASS`; source refs는 `2311` stale cleanup/core/research preflight, runtime gate snapshot, policy/review/ticker artifacts다.

| Symbol | Side | Qty | Limit | Order id | Result |
| --- | --- | ---: | ---: | --- | --- |
| RGTI | sell | 17 | 20.38 | `b9253931-4e50-45ec-a30b-972a4a76903e` | `filled_avg_price=20.38 USD` |

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | 62 symbols, SPY/QQQ 포함, pre_mcp_shortlist 10개 |
| `check-mcp-coverage.py --strict --json` | PASS | Alpaca core pass, positive research 4개, Alpha throttle gap only |
| `check-risk-policy.py --json` | PASS | RGTI trim order-plan risk gate 통과 |

## 제출 후 정산

- `get_order_by_id`와 `get_orders(status=all, symbols=RGTI)` 기준 `RGTI` 주문은 `filled`다.
- `get_orders(status=open)` 기준 open orders는 `0`건이다.
- `get_all_positions` 기준 positions는 `33`개 유지이며 `RGTI`는 `68주 -> 51주`, `avg_entry_price=25.569583`, `qty_available=51`로 감소했다.
- `get_account_info` snapshot은 portfolio value `99,029.72 USD`, cash `32,343.10 USD`, buying power `300,589.78 USD`다.
- `get_account_activities(activity_types=FILL, after=2026-06-10)`는 `RGTI` partial fill 1건 + final fill 1건, earlier same-day `AVGO` sell 2 fills, `WMT` buy 1 fill, `AAPL` buy 2 fills를 반환했다.

## 산출물

- Report: `wiki/current-runs/daily/2026-06-10-2311-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-10-2311-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-10-2311-hourly-autopilot.json`
- Runtime gate evaluation: `wiki/evidence-store/sources/2026-06-10-2311-hourly-autopilot-runtime-gate-evaluation.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-10-2311-hourly-autopilot-post-trade.json`
- Submit trace: `wiki/evidence-store/sources/2026-06-10-2311-hourly-autopilot-deterministic-submit.json`

## 지표 설명

- `sell_candidate_diagnostics`: 보유 포지션 중 trim/exit 재점검이 필요한 상위 후보와 blocked gate를 남기는 audit trail이다.
- `review_backlog_pending_1d_count`: validation buy 1D review backlog count다. 이번 cycle에서는 `9`라 신규 buy 슬롯이 `1`개로 축소되지만 sell/trim 진단은 독립적으로 유지된다.
- `speculative_loss_control`: speculative sleeve에서 큰 미실현 손실과 약한 후속 품질이 함께 나타날 때 staged trim을 허용하는 규칙이다.
- `duplicate_symbol_side_same_day`: 같은 정규장 날짜에 동일 symbol/side filled order가 이미 있으면 추가 submit을 막는 규칙이다.
- `provider_error`: 이번 run의 Alpha Vantage는 scheduler one-call-per-hour throttle 때문에 provider call을 건너뛰었고, 나머지 4개 research confirmations가 유지돼 strict MCP gate는 통과했다.
