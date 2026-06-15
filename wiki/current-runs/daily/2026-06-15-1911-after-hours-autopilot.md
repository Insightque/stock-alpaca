# 2026-06-15-1911-after-hours-autopilot

## 요약

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Session: `after_hours`
- Policy profile: `after_hours_policy`
- Artifact tag: `after-hours`
- Review bucket: `after_hours_validation`
- Paper mode: `ALPACA_PAPER_TRADE=true` 확인
- 결과: scheduler-owned `1911` core/research preflight를 source-of-record로 유지했다. Alpaca core `first_blocking_gate=market_closed`는 after-hours에서 expected nonblocking으로 처리했고, direct Alpaca MCP `get_all_positions`, `get_orders(status=open)`, `get_watchlists`, `get_orders(status=all, after=2026-06-14T20:00:00Z)`, `get_order_by_client_id` continuity readback까지 합쳐 regular market closed, account `ACTIVE`, positions `33`, open orders `0`, watchlists `0`, same-session after-hours fills `2`를 재확인했다. separate session budget `2/2`가 유지돼 이번 cycle은 no-submit으로 종료했다.

## 사용한 스케줄러 프리플라이트

- Alpaca core: `wiki/evidence-store/sources/2026-06-15-1911-after-hours-autopilot-alpaca-core-preflight.json`
- Research MCP: `wiki/evidence-store/sources/2026-06-15-1911-after-hours-autopilot-research-mcp-preflight.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-06-15-1911-after-hours-autopilot-after-hours-gate-evaluation.json`
- Runtime Alpaca summary: `wiki/evidence-store/sources/2026-06-15-1911-after-hours-autopilot-runtime-alpaca-spot-check.json`
- Alpaca core preflight의 `first_blocking_gate=market_closed`는 after-hours 워크플로우에서 expected nonblocking으로 처리했다. 이번 `1911` preflight는 passing account/positions/open-orders/recent-activities/watchlist/quote/snapshot/trade rows를 유지했고, direct Alpaca MCP continuity는 same-session fill/client-order 상태 재확인에만 사용했다.

## Alpaca MCP 확인

- Regular market: closed (direct `get_clock.timestamp=2026-06-15T06:12:42.510425896-04:00`)
- Account: direct `get_account_info` 기준 account `ACTIVE`, portfolio value `102023.94 USD`, cash `31946.39 USD`, buying power `306983.63 USD`였다.
- Positions / open orders: direct `get_all_positions`, `get_orders(status=open)`, `get_watchlists` 기준 positions `33`건, open orders `0`건, watchlists `0`건이었다.
- Direct continuity: direct `get_orders(status=all, after=2026-06-14T20:00:00Z)`와 `get_order_by_client_id` readback 기준 same-session fills는 `MSFT` buy `1주` `395.87 USD`, `AVGO` sell `1주` `391.92 USD` 두 건뿐이었고 둘 다 `extended_hours=true`, `status=filled`를 유지했다.
- Same-session after-hours order budget: `after_hours_new_orders_submitted_today=2/2`. regular-session validation count는 재사용하지 않았다.

## Gate 결과

| Gate | Status |
| --- | --- |
| alpaca_paper_mode | pass |
| regular_market_open | pass_regular_market_closed |
| extended_hours_session | pass |
| alpaca_core_account_clock_position_order_quote_spread | pass_scheduler_preflight_plus_direct_continuity |
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
- Separate after-hours session budget은 `after_hours_new_orders_submitted_today=2`로 `after_hours_policy.max_new_orders_per_session=2`에 도달한 상태를 유지해 `1911` submit path 진입 전에 차단됐다.
- 이번 cycle의 reconciliation은 scheduler-owned preflight rows와 direct Alpaca MCP `get_all_positions`, `get_orders(status=open)`, `get_watchlists`, `get_orders(status=all, after=2026-06-14T20:00:00Z)`, `get_order_by_client_id` readback 기준 same-session fills `2`건, positions `33`건, open orders `0`건, watchlists `0`건을 재확인하는 수준에서 종료했다.

## Validators

- `PATH=/usr/local/bin:$PATH python3 scripts/check-universe-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-15-1911-after-hours-autopilot.json`
  - 결과: PASS
- `PATH=/usr/local/bin:$PATH python3 scripts/check-mcp-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-15-1911-after-hours-autopilot.json`
  - 결과: PASS
- `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-06-15-1911-after-hours-autopilot.json`
  - 결과: PASS
  - 경고: `orders is empty`

## Artifacts

- Report: `wiki/current-runs/daily/2026-06-15-1911-after-hours-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-15-1911-after-hours-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-15-1911-after-hours-autopilot.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-06-15-1911-after-hours-autopilot-after-hours-gate-evaluation.json`
- Runtime Alpaca summary: `wiki/evidence-store/sources/2026-06-15-1911-after-hours-autopilot-runtime-alpaca-spot-check.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-15-1911-after-hours-autopilot-post-trade.json`
