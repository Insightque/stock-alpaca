# 2026-06-17-2131-after-hours-autopilot

## 요약

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Session: `after_hours`
- Policy profile: `after_hours_policy`
- Artifact tag: `after-hours`
- Review bucket: `after_hours_validation`
- Paper mode: `ALPACA_PAPER_TRADE=true` 확인
- 결과: scheduler-owned `2131` core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. direct Alpaca MCP readback으로 positions `33`, watchlists `0`, same-session fills `RGTI`/`PFE`, overnight quote parity를 다시 확인했지만 separate after-hours session budget이 계속 `2/2`로 닫혀 있어 이번 cycle도 신규 submit 없이 no-submit으로 종료했다.

## 사용한 스케줄러 프리플라이트

- Alpaca core: `wiki/evidence-store/sources/2026-06-17-2131-after-hours-autopilot-alpaca-core-preflight.json`
- Research MCP: `wiki/evidence-store/sources/2026-06-17-2131-after-hours-autopilot-research-mcp-preflight.json`
- Runtime continuity fallback: `wiki/evidence-store/sources/2026-06-17-2131-after-hours-autopilot-runtime-alpaca-spot-check.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-06-17-2131-after-hours-autopilot-after-hours-gate-evaluation.json`
- Alpaca core preflight의 `first_blocking_gate=market_closed`는 after-hours 워크플로우에서 expected nonblocking으로 처리했다. submit-boundary source-of-record는 같은 preflight의 passing clock/account/positions/orders/activity/asset/quote rows였고, direct Alpaca MCP readback은 current clock/positions/watchlists/same client_order_id fill/overnight quote continuity만 재확인했다.

## Alpaca MCP 확인

- Regular market: closed (scheduler-owned `get_clock.timestamp=2026-06-17T08:31:09.435412808-04:00`)
- Account: source-of-record 기준 account `ACTIVE`, portfolio value `101,355.28 USD`, cash `30,391.78 USD`, buying power `304,101.53 USD`
- Positions / open orders: source-of-record `get_all_positions`, `get_orders_open`, `get_watchlists` 기준 positions `33`건, open orders `0`건, watchlists `0`건이었다.
- Reconciled same-session fills:
  - `ah-20260617-1331-sell-rgti-01` -> `RGTI` sell `1주`, `filled_avg_price=20.96 USD`
  - `ah-20260617-1351-sell-pfe-01` -> `PFE` sell `1주`, `filled_avg_price=26.03 USD`
- Same-session after-hours order budget: exact same `client_order_id` readback 기준 submitted/fill `2`건으로 `after_hours_new_orders_submitted_today=2/2`였다.
- Direct runtime continuity: live `get_clock/get_all_positions/get_watchlists/get_order_by_client_id/get_stock_latest_quote(feed=overnight)/get_stock_snapshot(feed=overnight)` 기준 regular market closed, positions `33`, watchlists `0`, `PFE qty=2`, `RGTI qty=27`, overnight `RGTI/PFE/QQQ` quote parity를 재확인했다.
- Review backlog reference: `review-due-index` 기준 `pending_1d_count=0`, `pending_5d_count=37`, `pending_20d_count=1`, `blocked_add_symbols=['NOK']`였고 이번 cycle의 직접 차단 게이트는 backlog가 아니라 separate after-hours session budget이었다.

## Gate 결과

| Gate | Status |
| --- | --- |
| alpaca_paper_mode | pass |
| regular_market_open | pass_regular_market_closed |
| extended_hours_session | pass |
| alpaca_core_account_clock_position_order_quote_spread | pass_scheduler_preflight_rows_plus_direct_mcp_readback |
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
- Separate after-hours session budget은 `after_hours_new_orders_submitted_today=2`로 `after_hours_policy.max_new_orders_per_session=2`에 도달한 상태를 유지해 `2131` submit path 진입 전에 차단됐다.
- 이번 cycle의 reconciliation은 scheduler-owned same-session fill ledger와 direct Alpaca MCP readback 유지에 집중했다. `PFE qty=2`, `RGTI qty=27`, open orders `0`, watchlists `0` 상태를 그대로 보존했다.

## Validators

- `PATH=/usr/local/bin:$PATH python3 scripts/check-universe-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-17-2131-after-hours-autopilot.json`
- `PATH=/usr/local/bin:$PATH python3 scripts/check-mcp-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-17-2131-after-hours-autopilot.json`
- `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-06-17-2131-after-hours-autopilot.json`

## Artifacts

- Report: `wiki/current-runs/daily/2026-06-17-2131-after-hours-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-17-2131-after-hours-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-17-2131-after-hours-autopilot.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-06-17-2131-after-hours-autopilot-after-hours-gate-evaluation.json`
- Runtime continuity fallback: `wiki/evidence-store/sources/2026-06-17-2131-after-hours-autopilot-runtime-alpaca-spot-check.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-17-2131-after-hours-autopilot-post-trade.json`
