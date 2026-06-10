# 2026-06-10-1311-after-hours-autopilot

## 요약

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Session: `after_hours`
- Policy profile: `after_hours_policy`
- Artifact tag: `after-hours`
- Review bucket: `after_hours_validation`
- Paper mode: `ALPACA_PAPER_TRADE=true` 확인
- 결과: scheduler-owned `1311` core/research preflight를 source-of-record로 사용했고 Alpaca core preflight의 `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. runtime Alpaca MCP cross-check 결과 regular market은 계속 closed, account는 `ACTIVE`, positions는 `33`, open orders는 `0`, same-session after-hours orders/fills는 각각 `2`, watchlists는 `0`이었고 earlier same-session client ids `ah-20260610-1011-aapl-buy-01`, `ah-20260610-1031-aapl-buy-01`도 여전히 `filled`였다. separate session budget `2/2`가 이미 소진돼 no-submit으로 종료했다.

## 사용한 스케줄러 프리플라이트

- Alpaca core: `wiki/evidence-store/sources/2026-06-10-1311-after-hours-autopilot-alpaca-core-preflight.json`
- Research MCP: `wiki/evidence-store/sources/2026-06-10-1311-after-hours-autopilot-research-mcp-preflight.json`
- Alpaca core preflight는 `first_blocking_gate=market_closed`만 regular-session blocker로 남겼다. after-hours run에서는 이를 nonblocking으로 처리했고 scheduler-owned open-order/fill/asset/quote rows를 유지했다.

## Alpaca MCP 확인

- Regular market: closed (`get_clock.timestamp=2026-06-10T00:12:27.339802843-04:00`)
- Account/positions: runtime `get_account_info`, `get_all_positions` 기준 account `ACTIVE`, portfolio value `98,369.78 USD`, cash `31,368.65 USD`, buying power `297,780.85 USD`, positions `33`건이었다.
- Open orders / same-session orders / fills: runtime `get_orders(status=open)` 기준 open order count `0`, runtime `get_orders(status=all, after=2026-06-09T20:00:00Z)` 기준 same-session after-hours orders `2`, runtime `get_account_activities(activity_types=FILL, after=2026-06-09T20:00:00Z)` 기준 same-session after-hours fill `2`건이었다.
- Watchlists: runtime `get_watchlists`는 `0`건이었다.
- Reconciled client ids: `ah-20260610-1011-aapl-buy-01`, `ah-20260610-1031-aapl-buy-01` 모두 `filled`로 유지됐다.

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
- Separate after-hours session budget은 `after_hours_new_orders_submitted_today=2`로 `after_hours_policy.max_new_orders_per_session=2`에 도달해 submit path 진입 전에 차단됐다.
- Reconciliation은 기존 same-session client order id `ah-20260610-1011-aapl-buy-01`, `ah-20260610-1031-aapl-buy-01`가 이미 filled 상태임을 확인하는 용도로만 수행했다.

## Validators

- `PATH=/usr/local/bin:$PATH python3 scripts/check-universe-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-10-1311-after-hours-autopilot.json`
  - 결과: PASS
- `PATH=/usr/local/bin:$PATH python3 scripts/check-mcp-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-10-1311-after-hours-autopilot.json`
  - 결과: PASS
- `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-06-10-1311-after-hours-autopilot.json`
  - 결과: PASS
  - 경고: `orders is empty`

## Artifacts

- Manifest: `wiki/evidence-store/run-manifests/2026-06-10-1311-after-hours-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-10-1311-after-hours-autopilot.json`
- Gate evaluation source: `wiki/evidence-store/sources/2026-06-10-1311-after-hours-autopilot-after-hours-gate-evaluation.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-10-1311-after-hours-autopilot-post-trade.json`
