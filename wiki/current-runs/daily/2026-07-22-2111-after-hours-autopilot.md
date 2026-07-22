# 2026-07-22-2111-after-hours-autopilot

## 요약

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Session: `after_hours`
- Policy profile: `after_hours_policy`
- Artifact tag: `after-hours`
- Review bucket: `after_hours_validation`
- Market date: `2026-07-22 EDT`
- Scheduler artifact date: `2026-07-22 KST`
- Paper mode: `ALPACA_PAPER_TRADE=true` 확인
- 결과: scheduler-owned `2111` core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. 이번 cycle의 `2111` preflight는 `NOK` `10.33/10.34`, `SPY` `745.57/745.69`, `SMH` `566.89/575.94` fresh rows를 제공했다. buy fallback은 `SPY` per-order notional cap, `SMH` spread cap, `review_backlog_pending_1d_count=17` buy throttle 때문에 다시 막혔고, sell-first 경로에서 `NOK` 1주 trim이 strict universe/MCP/risk/quote/spread gate를 모두 통과해 `client_order_id=ah-20260722-2111-sell-nok-01`로 제출됐다. immediate reconciliation 기준 주문은 `status=new` open order이며 fill은 아직 없다.

## 사용한 스케줄러 프리플라이트

- Alpaca core: `wiki/evidence-store/sources/2026-07-22-2111-after-hours-autopilot-alpaca-core-preflight.json`
- Research MCP: `wiki/evidence-store/sources/2026-07-22-2111-after-hours-autopilot-research-mcp-preflight.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-07-22-2111-after-hours-autopilot-after-hours-gate-evaluation.json`
- Alpaca core preflight의 `first_blocking_gate=market_closed`는 after-hours 워크플로우에서 expected nonblocking으로 처리했다.

## Alpaca MCP 확인

- Regular market: closed. live `get_clock` 기준 `timestamp=2026-07-22T08:13:02.873762892-04:00`였다.
- Account: live `get_account_info` 기준 account `ACTIVE`, portfolio value `97492.39 USD`, cash `28995.09 USD`, buying power `296169.22 USD`였다.
- Positions / orders: submit 전 open orders `0`건이었고 submit 후 `get_orders(status=open)` 기준 `NOK` open order `1`건이 남았다. `get_orders(status=all, after=2026-07-21T20:00:00Z)` 기준 same-session after-hours submitted orders는 `2`건, fills는 `1`건이다. 이전 `AVGO` sell `client_order_id=ah-20260722-0911-sell-avgo-01`은 계속 `filled` 상태다.
- Position continuity: live `get_all_positions` 기준 positions `31`건이었다. `NOK qty=402`, `qty_available=401`로 방금 제출한 1주 sell이 예약됐고 `AVGO position 없음`도 유지됐다. watchlists는 `0`건이었다.

## 후보 평가

- `NOK` sell/trim: source-of-record quote `10.33/10.34`, spread `0.0968%`, quote age 약 `1.7`분, open orders `0`, same-day `NOK` sell `0`, after-hours session budget `1/2` 상태로 executable trim 조건을 통과했다. `[[NOK]]`와 `2026-06-19` portfolio review는 `existing-position-breakout-add-penalty` 유지와 기준단가 하회 상태를 기록하고 있어 sell-first policy-learning trim으로 승격했다.
- `SPY` buy fallback: quote freshness와 spread는 pass였지만 1주 ask `745.69 USD`가 `after_hours_policy.max_notional_pct_per_order=0.005` cap을 넘었다.
- `SMH` buy fallback: quote age는 pass였지만 spread `1.5838%`가 after-hours cap `0.25%`를 넘었다.
- `WMT`, `SO`, `MCD`, `QQQ`, `NEE`, `CVX`, `GS`: one-sided quote 또는 stale quote 또는 spread hard gate fail로 executable path가 열리지 않았다.

## Gate 결과

| Gate | Status |
| --- | --- |
| alpaca_paper_mode | pass |
| regular_market_open | pass_regular_market_closed |
| extended_hours_session | pass |
| alpaca_core_account_clock_position_order_quote_spread | pass_scheduler_preflight_plus_live_reconciliation |
| after_hours_policy_profile | pass |
| separate_after_hours_order_budget | pass_second_of_two_slots_submitted |
| universe_strict | PASS |
| mcp_tiered_strict | PASS |
| risk_policy | PASS |
| fresh_quote | PASS_nok_1.7_minutes |
| spread_within_after_hours_policy | PASS_nok_0.0968pct |
| whole_share_day_limit_extended_hours_order | PASS_nok_sell_shape |
| immediate_reconcile_and_cancel_or_lifecycle_record | PASS_client_order_id_reconciled_open_new_lifecycle_recorded |

## Validators

- `PATH=/usr/local/bin:$PATH python3 scripts/check-universe-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-07-22-2111-after-hours-autopilot.json`
- `PATH=/usr/local/bin:$PATH python3 scripts/check-mcp-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-07-22-2111-after-hours-autopilot.json`
- `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-07-22-2111-after-hours-autopilot.json`

## Submit And Reconcile

- Submitted order: `NOK` sell `1` share, `limit_price=10.33`, `time_in_force=day`, `extended_hours=true`, `session=after_hours`, `review_bucket=after_hours_validation`, `client_order_id=ah-20260722-2111-sell-nok-01`
- Alpaca MCP `place_stock_order` returned `order_id=78270797-caec-4673-a861-69f4db403bc0`, initial `status=pending_new`.
- Immediate `get_order_by_client_id`와 `get_orders(status=open|all)` readback은 same `client_order_id`를 `status=new`, `filled_qty=0`로 재확인했다.
- `get_all_positions` cross-check에서는 `NOK qty=402`, `qty_available=401`가 보여 1주가 open sell order로 예약된 상태임을 확인했다. alternate `client_order_id`는 사용하지 않았다.
- policy `cancel_unfilled_after_minutes=5`는 후속 scheduler lifecycle에서 처리하도록 남기고, 이번 cycle은 no-retry open order lifecycle record로 종료한다.

## Artifacts

- Report: `wiki/current-runs/daily/2026-07-22-2111-after-hours-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-07-22-2111-after-hours-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-07-22-2111-after-hours-autopilot.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-07-22-2111-after-hours-autopilot-after-hours-gate-evaluation.json`
- Post-trade check: `wiki/trade-ledger/positions/2026-07-22-2111-after-hours-autopilot-post-trade.json`
