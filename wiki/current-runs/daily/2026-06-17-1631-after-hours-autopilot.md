# 2026-06-17-1631-after-hours-autopilot

## 요약

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Session: `after_hours`
- Policy profile: `after_hours_policy`
- Artifact tag: `after-hours`
- Review bucket: `after_hours_validation`
- Paper mode: `ALPACA_PAPER_TRADE=true` 확인
- 결과: scheduler-owned `1631` core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. exact same `client_order_id` reconciliation과 live continuity 기준 same-session fill `RGTI`, `PFE` 두 건이 모두 유지되고 separate after-hours session budget이 계속 `2/2`로 닫혀 있어 이번 cycle은 신규 submit 없이 no-submit으로 종료했다.

## 사용한 스케줄러 프리플라이트

- Alpaca core: `wiki/evidence-store/sources/2026-06-17-1631-after-hours-autopilot-alpaca-core-preflight.json`
- Research MCP: `wiki/evidence-store/sources/2026-06-17-1631-after-hours-autopilot-research-mcp-preflight.json`
- Runtime continuity: `wiki/evidence-store/sources/2026-06-17-1631-after-hours-autopilot-runtime-alpaca-spot-check.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-06-17-1631-after-hours-autopilot-after-hours-gate-evaluation.json`
- Alpaca core preflight의 `first_blocking_gate=market_closed`는 after-hours 워크플로우에서 expected nonblocking으로 처리했다. submit-boundary source-of-record는 같은 preflight의 passing account/positions/orders/activity/quote rows였고, live continuity는 same `client_order_id` 두 건의 fill 상태와 current account/order/fill/watchlist/overnight quote 재확인으로만 제한했다.

## Alpaca MCP 확인

- Regular market: closed (scheduler-owned `get_clock.timestamp=2026-06-17T03:31:07.604019333-04:00`)
- Account:
  - source-of-record 기준 account `ACTIVE`, portfolio value `101,325.26 USD`, cash `30,391.80 USD`, buying power `304,332.44 USD`
  - live continuity 기준 portfolio value `101,347.84 USD`, cash `30,391.80 USD`, buying power `304,350.64 USD`
- Positions / open orders: source-of-record `get_all_positions`, `get_orders_open`, `get_watchlists` 기준 positions `33`건, open orders `0`건, watchlists `0`건이었다. live continuity 기준도 동일하게 유지됐다.
- Reconciled same-session fills:
  - `ah-20260617-1331-sell-rgti-01` -> `RGTI` sell `1주`, `filled_avg_price=20.96 USD`
  - `ah-20260617-1351-sell-pfe-01` -> `PFE` sell `1주`, `filled_avg_price=26.03 USD`
- Same-session after-hours order budget: `get_orders(status=all, after=2026-06-16T20:00:00-04:00)`, `get_account_activities(activity_types=[FILL], after=2026-06-16T20:00:00-04:00)`, exact same `client_order_id` readback 기준 submitted/fill `2`건으로 `after_hours_new_orders_submitted_today=2/2`였다.

## Gate 결과

| Gate | Status |
| --- | --- |
| alpaca_paper_mode | pass |
| regular_market_open | pass_regular_market_closed |
| extended_hours_session | pass |
| alpaca_core_account_clock_position_order_quote_spread | pass_scheduler_preflight_rows_plus_live_continuity |
| after_hours_policy_profile | pass |
| separate_after_hours_order_budget | block_after_hours_session_budget_exhausted |
| universe_strict | PASS |
| mcp_tiered_strict | PASS |
| risk_policy | PASS |
| fresh_quote | not_actionable_budget_exhausted_before_submit_path |
| spread_within_after_hours_policy | not_actionable_budget_exhausted_before_submit_path |
| whole_share_day_limit_extended_hours_order | not_applicable_no_order |
| immediate_reconcile_and_cancel_or_lifecycle_record | pass_same_client_id_fill_reconciliation_completed |

## Submit And Reconcile

- `place_stock_order`는 호출하지 않았다. 신규 `client_order_id`, retry, alternate client id도 없었다.
- Separate after-hours session budget은 `after_hours_new_orders_submitted_today=2`로 `after_hours_policy.max_new_orders_per_session=2`에 도달한 상태를 유지해 `1631` submit path 진입 전에 차단됐다.
- 이번 cycle의 reconciliation은 same `client_order_id` readback과 fills ledger, current positions/watchlists/account continuity 확인에 집중했다. `PFE qty=2`, `qty_available=2`, `RGTI qty=27`, open orders `0`가 유지됐다.

## Validators

- `PATH=/usr/local/bin:$PATH python3 scripts/check-universe-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-17-1631-after-hours-autopilot.json`
- `PATH=/usr/local/bin:$PATH python3 scripts/check-mcp-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-17-1631-after-hours-autopilot.json`
- `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-06-17-1631-after-hours-autopilot.json`

## Artifacts

- Report: `wiki/current-runs/daily/2026-06-17-1631-after-hours-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-17-1631-after-hours-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-17-1631-after-hours-autopilot.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-06-17-1631-after-hours-autopilot-after-hours-gate-evaluation.json`
- Runtime continuity: `wiki/evidence-store/sources/2026-06-17-1631-after-hours-autopilot-runtime-alpaca-spot-check.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-17-1631-after-hours-autopilot-post-trade.json`
