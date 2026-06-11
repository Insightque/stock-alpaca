# 2026-06-11-2011-after-hours-autopilot

## 요약

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Session: `after_hours`
- Policy profile: `after_hours_policy`
- Artifact tag: `after-hours`
- Review bucket: `after_hours_validation`
- Paper mode: `ALPACA_PAPER_TRADE=true` 확인
- 결과: scheduler-owned `2011` core/research preflight를 source-of-record로 사용했고 Alpaca core preflight의 `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. scheduler preflight와 runtime Alpaca MCP cross-check 모두 same-session after-hours fills `2`건, open orders `0`건, positions `33`건, watchlists `0`건을 유지했고 separate session budget `2/2`가 이미 소진돼 no-submit으로 종료했다.

## 사용한 스케줄러 프리플라이트

- Alpaca core: `wiki/evidence-store/sources/2026-06-11-2011-after-hours-autopilot-alpaca-core-preflight.json`
- Research MCP: `wiki/evidence-store/sources/2026-06-11-2011-after-hours-autopilot-research-mcp-preflight.json`
- Alpaca core preflight는 `first_blocking_gate=market_closed`를 regular-session blocker로 남겼다. after-hours run에서는 이를 nonblocking으로 처리했고 scheduler-owned passing account/positions/open-orders/recent-fills/watchlists rows를 그대로 사용했다.

## Alpaca MCP 확인

- Regular market: runtime `get_clock` 기준 closed (`timestamp=2026-06-11T07:12:52.426000739-04:00`), `next_open=2026-06-11T09:30:00-04:00`.
- Account/positions: scheduler preflight `get_account_info/get_all_positions`를 source-of-record로 유지했고 runtime `get_account_info/get_all_positions` cross-check 기준 account `ACTIVE`, portfolio value `98023.96 USD`, cash `30904.63 USD`, buying power `296379.57 USD`, positions `33`건이었다. `RGTI`는 `49주`, `qty_available=49`, `avg_entry_price=25.569583 USD`로 unchanged였다.
- Open orders / same-session fills / watchlists: runtime `get_orders(status=open)`는 `0`건, `get_account_activities(activity_types=FILL, after=2026-06-10T20:00:00Z)`는 이번 장외 세션의 `RGTI` sell fill `2건`(`19.50 USD`, `19.78 USD`)만 반환했고 `get_watchlists`도 `0`건이었다.
- Runtime read-only cross-check: local Alpaca MCP `get_order_by_client_id(ah-20260611-0951-sell-rgti)`, `get_order_by_client_id(ah-20260611-1011-sell-rgti)`, `get_stock_latest_quote(feed=overnight)`, `get_stock_snapshot(feed=overnight)`로 same-session lifecycle과 overnight quote availability를 재확인했다. 두 client id는 모두 `filled`, sampled `ORCL` overnight quote timestamp는 `2026-06-11T08:00:00.37547251Z`였다.

## Gate 결과

| Gate | Status |
| --- | --- |
| alpaca_paper_mode | pass |
| regular_market_open | pass_regular_market_closed |
| extended_hours_session | pass |
| alpaca_core_account_clock_position_order_quote_spread | pass_scheduler_preflight_plus_runtime_cross_check |
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
- Separate after-hours session budget은 `after_hours_new_orders_submitted_today=2`로 `after_hours_policy.max_new_orders_per_session=2`에 도달해 submit path 진입 전에 차단됐다. regular validation count는 재사용하지 않았고, `risk_inputs.after_hours_new_orders_submitted_today`만 별도 세션 예산 근거로 사용했다.
- Reconciliation은 scheduler-owned `2011` preflight recent-fill/open-order evidence와 runtime `get_order_by_client_id` 결과를 함께 기준으로 유지했다.

## Validators

- `PATH=/usr/local/bin:$PATH python3 scripts/check-universe-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-11-2011-after-hours-autopilot.json`
- 결과: PASS
- `PATH=/usr/local/bin:$PATH python3 scripts/check-mcp-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-11-2011-after-hours-autopilot.json`
- 결과: PASS
- `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-06-11-2011-after-hours-autopilot.json`
- 결과: PASS

## Artifacts

- Manifest: `wiki/evidence-store/run-manifests/2026-06-11-2011-after-hours-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-11-2011-after-hours-autopilot.json`
- Gate evaluation source: `wiki/evidence-store/sources/2026-06-11-2011-after-hours-autopilot-after-hours-gate-evaluation.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-11-2011-after-hours-autopilot-post-trade.json`
