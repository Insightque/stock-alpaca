# 2026-06-15-1511-after-hours-autopilot

## 요약

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Session: `after_hours`
- Policy profile: `after_hours_policy`
- Artifact tag: `after-hours`
- Review bucket: `after_hours_validation`
- Paper mode: `ALPACA_PAPER_TRADE=true` 확인
- 결과: scheduler-owned `1511` core/research preflight를 source-of-record로 유지했다. Alpaca core `first_blocking_gate=market_closed`는 after-hours에서 expected nonblocking으로 처리했고, 같은 preflight의 passing account/positions/open-orders/recent-activities/watchlist/asset/quote/snapshot rows를 사용했다. same-session after-hours fills `2`건이 이미 separate session budget `2/2`를 채운 상태여서 이번 cycle은 no-submit으로 종료했다.

## 사용한 스케줄러 프리플라이트

- Alpaca core: `wiki/evidence-store/sources/2026-06-15-1511-after-hours-autopilot-alpaca-core-preflight.json`
- Research MCP: `wiki/evidence-store/sources/2026-06-15-1511-after-hours-autopilot-research-mcp-preflight.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-06-15-1511-after-hours-autopilot-after-hours-gate-evaluation.json`
- Runtime Alpaca summary: `wiki/evidence-store/sources/2026-06-15-1511-after-hours-autopilot-runtime-alpaca-spot-check.json`
- Alpaca core preflight의 `first_blocking_gate=market_closed`는 after-hours 워크플로우에서 expected nonblocking으로 처리했다. 이번 `1511` preflight는 passing account/positions/open-orders/recent-activities/watchlist/asset/quote/snapshot rows를 보존했으므로, 추가 Alpaca runtime read call 없이 같은 preflight를 source-of-record로 유지했다.

## Alpaca MCP 확인

- Regular market: closed (scheduler-owned `get_clock.timestamp=2026-06-15T02:11:08.314735911-04:00`)
- Account: scheduler-owned `get_account_info` 기준 account `ACTIVE`, portfolio value `102142.97 USD`, cash `31946.39 USD`, buying power `306979.23 USD`였다.
- Positions / open orders: scheduler-owned `get_all_positions`, `get_orders(status=open)`, `get_watchlists` 기준 positions `33`건, open orders `0`건, watchlists `0`건이었다.
- Same-session after-hours fills: scheduler-owned `get_account_activities(activity_types=FILL)` recent rows 기준 `AVGO` sell `1주` `391.92 USD`, `MSFT` buy `1주` `395.87 USD` 두 건이 유지됐다.
- Same-session after-hours order budget: `after_hours_new_orders_submitted_today=2/2`. regular-session validation count는 재사용하지 않았다.

## Gate 결과

| Gate | Status |
| --- | --- |
| alpaca_paper_mode | pass |
| regular_market_open | pass_regular_market_closed |
| extended_hours_session | pass |
| alpaca_core_account_clock_position_order_quote_spread | pass_scheduler_preflight_rows |
| after_hours_policy_profile | pass |
| separate_after_hours_order_budget | block_after_hours_session_budget_exhausted |
| universe_strict | PASS |
| mcp_tiered_strict | PASS |
| risk_policy | PASS |
| fresh_quote | not_actionable_budget_exhausted_before_submit_path |
| spread_within_after_hours_policy | not_actionable_budget_exhausted_before_submit_path |
| whole_share_day_limit_extended_hours_order | not_applicable_no_order |
| immediate_reconcile_and_cancel_or_lifecycle_record | not_applicable_no_submit |

## Submit And Reconcile

- `place_stock_order`는 호출하지 않았다. 신규 `client_order_id`, retry, alternate client id도 없었다.
- Separate after-hours session budget은 `after_hours_new_orders_submitted_today=2`로 `after_hours_policy.max_new_orders_per_session=2`에 도달한 상태를 유지해 1511 submit path 진입 전에 차단됐다.
- 이번 cycle의 reconciliation은 scheduler-owned `get_account_activities`와 `get_orders(status=open)` preflight rows 기준으로 same-session fills `2`건과 open orders `0`건을 재확인하는 수준에서 종료했다.

## Validators

- `PATH=/usr/local/bin:$PATH python3 scripts/check-universe-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-15-1511-after-hours-autopilot.json`
  - 결과: PASS
- `PATH=/usr/local/bin:$PATH python3 scripts/check-mcp-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-15-1511-after-hours-autopilot.json`
  - 결과: PASS
- `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-06-15-1511-after-hours-autopilot.json`
  - 결과: PASS
  - 경고: `orders is empty`

## Artifacts

- Report: `wiki/current-runs/daily/2026-06-15-1511-after-hours-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-15-1511-after-hours-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-15-1511-after-hours-autopilot.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-06-15-1511-after-hours-autopilot-after-hours-gate-evaluation.json`
- Runtime Alpaca summary: `wiki/evidence-store/sources/2026-06-15-1511-after-hours-autopilot-runtime-alpaca-spot-check.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-15-1511-after-hours-autopilot-post-trade.json`
