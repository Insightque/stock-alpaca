# 2026-06-10-1551-after-hours-autopilot

## 요약

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Session: `after_hours`
- Policy profile: `after_hours_policy`
- Artifact tag: `after-hours`
- Review bucket: `after_hours_validation`
- Paper mode: `ALPACA_PAPER_TRADE=true` 확인
- 결과: scheduler-owned `1551` core/research preflight를 source-of-record로 사용했고 Alpaca core preflight의 `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. runtime Alpaca MCP `get_clock/get_account_info/get_all_positions/get_watchlists/get_stock_latest_quote(feed=overnight)/get_stock_snapshot(feed=overnight)/get_order_by_client_id(ah-20260610-1011-aapl-buy-01)/get_order_by_client_id(ah-20260610-1031-aapl-buy-01)` cross-check에서도 regular market은 계속 closed였고, earlier same-session AAPL client ids 두 건이 모두 `filled` 상태로 유지되어 separate session budget `2/2`가 닫힌 상태가 재확인됐다. 따라서 no-submit으로 종료했다.

## 사용한 스케줄러 프리플라이트

- Alpaca core: `wiki/evidence-store/sources/2026-06-10-1551-after-hours-autopilot-alpaca-core-preflight.json`
- Research MCP: `wiki/evidence-store/sources/2026-06-10-1551-after-hours-autopilot-research-mcp-preflight.json`
- Alpaca core preflight는 `first_blocking_gate=market_closed`만 regular-session blocker로 남겼다. after-hours run에서는 이를 nonblocking으로 처리했고 scheduler-owned clock/account/position/open-order/fill/watchlist rows를 유지했다.

## Alpaca MCP 확인

- Regular market: scheduler preflight 기준 closed (`timestamp=2026-06-10T02:51:08.771162202-04:00`, `next_open=2026-06-10T09:30:00-04:00`); runtime Alpaca MCP `get_clock`도 `timestamp=2026-06-10T02:53:37.966252415-04:00`로 여전히 closed였다.
- Account/positions: scheduler preflight `get_account_info` 기준 account `ACTIVE`, portfolio value `98,388.21 USD`, cash `31,368.65 USD`, buying power `297,821.22 USD`, positions `33`건이었다. runtime `get_account_info/get_all_positions` cross-check에서도 account `ACTIVE`, portfolio value `98,370.53 USD`, positions `33`건이 유지됐다.
- Open orders / same-session fills / watchlists: scheduler preflight row 기준 open order count `0`, watchlists `0`건이었다. runtime `get_watchlists`도 `0`건이었고 same-session after-hours budget 증빙은 earlier client ids `ah-20260610-1011-aapl-buy-01`, `ah-20260610-1031-aapl-buy-01`의 `filled` 상태를 재확인해 유지했다.
- Runtime overnight quote/snapshot cross-check: shortlist `QQQ/SMH/SPY/JNJ/BA/AAPL/INTC/WMT` 8종에 대해 `get_stock_latest_quote(feed=overnight)`와 `get_stock_snapshot(feed=overnight)`가 모두 응답했다. 최신 quote timestamp 범위는 `2026-06-10T06:45:13Z`~`2026-06-10T06:52:40Z`였지만, 이번 cycle은 separate session budget blocker 때문에 submit path에 진입하지 않았다.

## Gate 결과

| Gate | Status |
| --- | --- |
| alpaca_paper_mode | pass |
| regular_market_open | pass_regular_market_closed |
| extended_hours_session | pass |
| alpaca_core_account_clock_position_order_quote_spread | pass_runtime_core_and_scheduler_preflight |
| after_hours_policy_profile | pass |
| separate_after_hours_order_budget | block_after_hours_session_budget_exhausted |
| universe_strict | pass |
| mcp_tiered_strict | pass |
| risk_policy | pass_empty_order_plan |
| fresh_quote | not_actionable_budget_exhausted_before_submit_path |
| spread_within_after_hours_policy | not_actionable_budget_exhausted_before_submit_path |
| whole_share_day_limit_extended_hours_order | not_applicable_no_order |
| immediate_reconcile_and_cancel_or_lifecycle_record | not_applicable_no_submit |

## Submit And Reconcile

- `place_stock_order`는 호출하지 않았다. 신규 `client_order_id`, retry, alternate client id도 없었다.
- Separate after-hours session budget은 `after_hours_new_orders_submitted_today=2`로 `after_hours_policy.max_new_orders_per_session=2`에 도달해 submit path 진입 전에 차단됐다. `risk_inputs.cash_deployment_blocker`는 schema 허용값 `no_candidate_passed_hard_gates`로 기록했고, 실제 hard gate reason은 manifest/report/log에 `separate_after_hours_order_budget`로 유지했다.
- Reconciliation은 기존 same-session client order id `ah-20260610-1011-aapl-buy-01`, `ah-20260610-1031-aapl-buy-01`가 이미 filled 상태임을 확인하는 용도로만 수행했다.

## Validators

- `PATH=/usr/local/bin:$PATH python3 scripts/check-universe-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-10-1551-after-hours-autopilot.json`
  - 결과: PASS
- `PATH=/usr/local/bin:$PATH python3 scripts/check-mcp-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-10-1551-after-hours-autopilot.json`
  - 결과: PASS
- `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-06-10-1551-after-hours-autopilot.json`
  - 결과: PASS
  - 경고: `orders is empty`

## Artifacts

- Manifest: `wiki/evidence-store/run-manifests/2026-06-10-1551-after-hours-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-10-1551-after-hours-autopilot.json`
- Gate evaluation source: `wiki/evidence-store/sources/2026-06-10-1551-after-hours-autopilot-after-hours-gate-evaluation.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-10-1551-after-hours-autopilot-post-trade.json`
