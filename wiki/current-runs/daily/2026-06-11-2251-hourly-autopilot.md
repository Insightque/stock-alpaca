# 2026-06-11-2251-hourly-autopilot

## 요약

`2251` scheduled hourly-autopilot은 scheduler-owned stale cleanup/core/research preflight를 source-of-record로 사용했고, live Alpaca MCP로 submit 직전 clock/account/open orders/positions/same-day fills/quotes를 짧게 재확인했다. stale cleanup과 live open-order check 모두 0건이라 lifecycle blocker는 없었다.

sell-first 재평가에서는 `AVGO`가 ai_semiconductor warning band와 post-earnings staged de-risking rationale를 유지한 채 live IEX quote `379.93/380.06`에서 spread `0.0342%`로 정상화돼 trim executable 상태가 됐다. 반면 `RGTI`는 same-day duplicate sell discipline, `SO`는 decision-grade metric gap이 남았다. `review_backlog_pending_1d_count=14`는 YAML stop threshold `12`를 넘겨 신규 validation buy를 막지만 risk-reducing sell/trim에는 비적용이므로, 이번 cycle은 `AVGO` 1주 trim을 실행했고 immediate reconciliation 기준 `filled_avg_price=380.43 USD`로 즉시 체결됐다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env` paper mode와 scheduler artifact 기준 `ALPACA_PAPER_TRADE=true` |
| Market clock | PASS | live Alpaca clock `2026-06-11T09:53:39.707140969-04:00`, regular market open |
| Stale order lifecycle | PASS | scheduler cleanup과 live `get_orders(status=open)` 모두 open orders `0`건 |
| Alpaca core MCP | PASS | scheduler core preflight hard gate pass + live clock/account/orders/positions/quotes 재확인 |
| Research MCP | PASS tiered | SEC EDGAR/FRED/Firecrawl/Yahoo positive, Alpha `provider_error` throttle gap only |
| Universe strict | PASS | metadata universe `62`개, SPY/QQQ 포함 |
| Review backlog throttle | BUY BLOCK | `pending_1d_count=14`가 stop threshold `12` 초과, sell/trim에는 비적용 |
| Quote/spread | PASS for AVGO | AVGO live quote `379.93/380.06`, spread `0.0342%`, quote age 약 `0.01`분 |
| Risk plan | PASS | `check-risk-policy.py --json` PASS |
| Final submit path | PASS | whole-share/day-limit/stock, duplicate/open-order conflict 없음, source refs 확보 |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| AVGO | selected_trim | 0.0342% | ai_semiconductor warning-band / post-earnings de-risking rationale active, whole-share floor trim executable |
| RGTI | blocked_duplicate_same_day | 0.0991% | speculative loss-control trim trigger는 active지만 same-day sell fills 2건이 duplicate discipline을 유지 |
| SO | blocked_metric_gap | 0.0528% | spread 정상화 후에도 trim decision-grade metric gap 지속 |
| MSFT | blocked_spread_and_review_backlog | 1.0203% | spread cap 초과, 신규 buy는 backlog throttle에도 막힘 |
| SPY | blocked_floor_cap_and_review_backlog | 0.0055% | 1주 ask `731.33 USD`가 validation floor per-order cap 초과, 신규 buy stop |
| QQQ | blocked_floor_cap_and_review_backlog | 0.0666% | 1주 ask `705.49 USD`가 validation floor per-order cap 초과, 신규 buy stop |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| AVGO | trim | executable | target-band de-risking과 post-earnings weakness가 유지되고 spread가 정상화돼 1주 trim 실행 |
| RGTI | watch | duplicate_symbol_side_same_day | speculative de-risking rationale는 유효하지만 same-day fill 2건이 추가 trim을 막음 |
| SO | watch | sell_metric_gap | quote/spread는 통과했지만 decision-grade replacement metric gap 지속 |

## 주문/체결

### 제출 전 게이트 요약

paper mode `true`; market clock `2026-06-11T09:53:39.707140969-04:00`; order plan path `wiki/trade-ledger/orders/2026-06-11-2251-hourly-autopilot.json`; universe strict `PASS`; MCP strict `PASS`; risk validator `PASS`; AVGO quote freshness 약 `0.01`분; spread `0.0342%`; order shape `sell 1 share / limit 379.93 / day / stock / regular session`; duplicate/open-order check `PASS`; source refs는 `2251` stale cleanup/core/research preflight, runtime gate snapshot, policy/review/ticker artifacts다.

| Symbol | Side | Qty | Limit | Order id | Result |
| --- | --- | ---: | ---: | --- | --- |
| AVGO | sell | 1 | 379.93 | `a4414ccd-c32c-48bb-97ec-189dc42f6cb8` | `filled_avg_price=380.43 USD` |

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | 62 symbols, SPY/QQQ 포함, pre_mcp_shortlist 6개 |
| `check-mcp-coverage.py --strict --json` | PASS | Alpaca core pass, positive research 4개, Alpha throttle gap only |
| `check-risk-policy.py --json` | PASS | AVGO trim order-plan risk gate 통과 |

## 제출 후 정산

- `get_order_by_id` 기준 `AVGO` 주문은 `filled`다.
- `get_orders(status=open)` 기준 open orders는 `0`건이다.
- `get_all_positions` 기준 positions는 `33`개 유지이며 `AVGO`는 `6주 -> 5주`, `avg_entry_price=419.151667`, `qty_available=5`로 감소했다.
- `get_account_info` snapshot은 portfolio value `98,618.81 USD`, cash `31,285.06 USD`, buying power `298,242.76 USD`다.
- `get_account_activities(activity_types=FILL, after=2026-06-11T00:00:00Z)`는 이번 `AVGO` fill 1건과 earlier same-day `RGTI` trim fills 2건을 반환했다.

## 산출물

- Report: `wiki/current-runs/daily/2026-06-11-2251-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-11-2251-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-11-2251-hourly-autopilot.json`
- Runtime gate evaluation: `wiki/evidence-store/sources/2026-06-11-2251-hourly-autopilot-runtime-gate-evaluation.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-11-2251-hourly-autopilot-post-trade.json`

## 지표 설명

- `review_backlog_pending_1d_count`: validation buy 1D review backlog count다. 이번 cycle에서는 `14`라 신규 buy가 stop되지만 sell/trim 진단은 독립적으로 유지된다.
- `sell_candidate_diagnostics`: 실행하지 않은 trim 후보도 why-not evidence를 남겨 후속 analyst review와 policy learning에 사용한다.
- `target_band_de_risking`: target/warning band를 넘긴 동일 theme/cluster 노출이 약화 신호와 함께 나타날 때 staged trim을 허용하는 규칙이다.
- `provider_error`: 이번 run의 Alpha Vantage는 scheduler one-call-per-hour throttle 때문에 provider call을 건너뛰었고, 나머지 4개 research confirmations가 유지돼 strict MCP gate는 통과했다.
