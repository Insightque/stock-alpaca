# 2026-06-18-1151-after-hours-autopilot

## 요약

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Session: `after_hours`
- Policy profile: `after_hours_policy`
- Artifact tag: `after-hours`
- Review bucket: `after_hours_validation`
- Paper mode: `ALPACA_PAPER_TRADE=true` 확인
- 결과: scheduler-owned `1151` Alpaca core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. live Alpaca continuity로 `clock/account/positions/orders/fills/watchlists/overnight quote`를 재확인한 결과 same-session after-hours submitted orders가 `2/2`로 이미 닫혀 있어 신규 submit 없이 lifecycle record로 종료했다.

## 사용한 스케줄러 프리플라이트

- Alpaca core: `wiki/evidence-store/sources/2026-06-18-1151-after-hours-autopilot-alpaca-core-preflight.json`
- Research MCP: `wiki/evidence-store/sources/2026-06-18-1151-after-hours-autopilot-research-mcp-preflight.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-06-18-1151-after-hours-autopilot-after-hours-gate-evaluation.json`
- Runtime spot check: `wiki/evidence-store/sources/2026-06-18-1151-after-hours-autopilot-runtime-alpaca-spot-check.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-18-1151-after-hours-autopilot-post-trade.json`

## Alpaca MCP 확인

- Regular market: closed (`live clock.timestamp=2026-06-17T22:52:57.638058802-04:00`), after-hours workflow 계속 진행
- Account: direct `get_account_info` 기준 account `ACTIVE`, cash `28003.45 USD`, portfolio value `101156.14 USD`, buying power `301094.19 USD`
- Positions / watchlists: direct `get_all_positions` 기준 positions `34`, `PFE qty=2 -> qty_available=1`, `RGTI qty=27 -> qty_available=26`; direct `get_watchlists` 기준 `0`
- Orders / fills: direct `get_orders(status=open)`와 `get_orders(status=all, after=2026-06-17T20:00:00-04:00)` 기준 open after-hours sell 2건(`PFE`, `RGTI`)이 그대로 남아 있고 direct `get_account_activities(activity_types=[FILL], after=2026-06-17T20:00:00-04:00)` 기준 same-session after-hours fill은 `0`건이었다.

## 후보 평가

- `PFE` / `RGTI` sell lifecycle: 두 주문 모두 fresh overnight quote path는 유지됐지만 이미 제출된 same-session after-hours sell 주문이므로 이번 cycle에서는 신규 trim 재시도를 만들지 않았다.
- `AVGO` sell/trim 보류: direct overnight quote `402.75/403.18`, spread 약 `0.1067%`로 executable 수준이지만 잔여 `1주`라 `keep_minimum_remaining_qty` 해석을 유지했다.
- `QQQ` buy fallback 차단: direct overnight quote `732.00/732.73`, spread는 양호했지만 1주 ask notional이 after-hours per-order cap을 넘는다. 다만 이번 cycle의 first blocker는 이 조건이 아니라 separate session budget `2/2`다.

## Gate 결과

| Gate | Status |
| --- | --- |
| alpaca_paper_mode | pass |
| regular_market_open | pass_regular_market_closed |
| extended_hours_session | pass |
| alpaca_core_account_clock_position_order_quote_spread | pass_scheduler_preflight_rows_reused_plus_live_clock_account_position_order_quote_continuity |
| after_hours_policy_profile | pass |
| separate_after_hours_order_budget | block_two_of_two_same_session_orders_already_submitted |
| universe_strict | PASS |
| mcp_tiered_strict | PASS |
| risk_policy | FAIL_stale_open_order_age_exceeds_lifecycle_limit |
| fresh_quote | pass_rechecked_but_budget_blocked_before_new_submit |
| spread_within_after_hours_policy | pass_rechecked_but_budget_blocked_before_new_submit |
| whole_share_day_limit_extended_hours_order | pass_no_new_orders_built |
| immediate_reconcile_and_cancel_or_lifecycle_record | pass_existing_open_orders_reconciled_by_client_order_id |

## Submit And Reconcile

- 이번 cycle에서는 `place_stock_order`를 호출하지 않았다. separate after-hours session budget이 already `2/2`였고, 별도로 risk validator도 `PFE` stale open order age `34.6분 > 30분` lifecycle limit 때문에 FAIL이었다. 다른 `client_order_id`로 retry하지 않았다.
- Existing reconciliation: `get_orders(status=open)` 기준 `ah-20260618-1111-sell-pfe-01`, `ah-20260618-1131-sell-rgti-01` 두 주문 모두 `status=new`, `filled_qty=0` open order다.
- Lifecycle note: policy `cancel_unfilled_after_minutes=5`는 이번 cycle에서 별도 `cancel_order_by_id` 실행으로 소비하지 않고 open-order lifecycle record로 남겼다. 후속 scheduler cycle에서 같은 `client_order_id` 기준으로만 추적한다.

## Validators

- `PATH=/usr/local/bin:$PATH python3 scripts/check-universe-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-18-1151-after-hours-autopilot.json`: PASS
- `PATH=/usr/local/bin:$PATH python3 scripts/check-mcp-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-18-1151-after-hours-autopilot.json`: PASS
- `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-06-18-1151-after-hours-autopilot.json`: FAIL (`PFE` stale open order age `34.6분 > 30분`, warning `orders is empty`)

## Artifacts

- Report: `wiki/current-runs/daily/2026-06-18-1151-after-hours-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-18-1151-after-hours-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-18-1151-after-hours-autopilot.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-06-18-1151-after-hours-autopilot-after-hours-gate-evaluation.json`
- Runtime spot check: `wiki/evidence-store/sources/2026-06-18-1151-after-hours-autopilot-runtime-alpaca-spot-check.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-18-1151-after-hours-autopilot-post-trade.json`
