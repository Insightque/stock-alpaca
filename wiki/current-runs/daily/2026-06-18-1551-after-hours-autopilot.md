# 2026-06-18-1551-after-hours-autopilot

## 요약

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Session: `after_hours`
- Policy profile: `after_hours_policy`
- Artifact tag: `after-hours`
- Review bucket: `after_hours_validation`
- Paper mode: `ALPACA_PAPER_TRADE=true` 확인
- 결과: scheduler-owned `1551` Alpaca core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. direct Alpaca continuity `get_clock/get_account_info/get_all_positions/get_orders(status=open|all)/get_account_activities(activity_types=[FILL])/get_order_by_client_id(PFE,RGTI)/get_watchlists` 기준 regular market closed, same-session prior trim `ah-20260618-1111-sell-pfe-01`, `ah-20260618-1131-sell-rgti-01`가 모두 filled이며 open orders `0`, watchlists `0`임을 재확인했다. separate after-hours submitted orders가 이미 `2/2`라 이번 cycle 신규 submit은 없었다.

## 사용한 스케줄러 프리플라이트

- Alpaca core: `wiki/evidence-store/sources/2026-06-18-1551-after-hours-autopilot-alpaca-core-preflight.json`
- Research MCP: `wiki/evidence-store/sources/2026-06-18-1551-after-hours-autopilot-research-mcp-preflight.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-06-18-1551-after-hours-autopilot-after-hours-gate-evaluation.json`
- Runtime spot check: `wiki/evidence-store/sources/2026-06-18-1551-after-hours-autopilot-runtime-alpaca-spot-check.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-18-1551-after-hours-autopilot-post-trade.json`
- Alpaca core preflight의 `first_blocking_gate=market_closed`는 장외 워크플로우에서 expected nonblocking으로 처리했고, 같은 preflight의 passing account/positions/orders/account-activities/watchlists/asset/quote/spread rows를 submit-boundary source-of-record로 유지했다.

## Alpaca MCP 확인

- Regular market: closed (`scheduler-owned get_clock.timestamp=2026-06-18T02:51:09.600817114-04:00`), after-hours workflow 계속 진행
- Account: source-of-record preflight 기준 account `ACTIVE`, cash `28,050.17 USD`, portfolio value `101,007.92 USD`, buying power `300,780.27 USD`, positions `34`, open orders `0`
- Direct continuity: `get_clock.timestamp=2026-06-18T02:53:16.282042938-04:00`, `get_account_info` 기준 account `ACTIVE`, cash `28,050.17 USD`, portfolio value `101,008.14 USD`, buying power `300,780.89 USD`
- Positions / orders / watchlists: direct `get_all_positions` 기준 positions `34`, direct `get_orders(status=open)` 기준 open orders `0`, direct `get_watchlists` 기준 watchlists `0`
- Same-session after-hours ledger: direct `get_orders(status=all, after=2026-06-17T20:00:00-04:00)`, `get_account_activities(activity_types=[FILL], after=2026-06-17T20:00:00-04:00)`, `get_order_by_client_id` readback 기준 same-session after-hours submitted orders는 `PFE`, `RGTI` 총 `2건`, fills도 `2건`이다.
- Quote / spread evidence: 이번 cycle은 separate after-hours session budget이 이미 `2/2`여서 새 submit path를 열지 않았고, 추가 live quote refresh 없이 scheduler-owned `1551` preflight의 passing quote/spread rows를 audit source로만 유지했다.

## Gate 결과

| Gate | Status |
| --- | --- |
| alpaca_paper_mode | pass |
| regular_market_open | pass_regular_market_closed |
| extended_hours_session | pass |
| alpaca_core_account_clock_position_order_quote_spread | pass_scheduler_preflight_rows_reused_and_direct_order_reconciliation_confirmed |
| after_hours_policy_profile | pass |
| separate_after_hours_order_budget | FAIL `2/2` |
| universe_strict | PASS |
| mcp_tiered_strict | PASS |
| risk_policy | PASS (warning `orders is empty`) |
| fresh_quote | not_rechecked_budget_exhausted_before_new_submit_path |
| spread_within_after_hours_policy | not_rechecked_budget_exhausted_before_new_submit_path |
| whole_share_day_limit_extended_hours_order | pass_no_new_order_built |
| immediate_reconcile_and_cancel_or_lifecycle_record | PASS_prior_client_order_ids_reconciled_without_retry |

## Submit And Reconcile

- 이번 cycle에서는 `place_stock_order`를 호출하지 않았다. separate after-hours submitted order count가 이미 `2/2`였기 때문이다.
- immediate pre-submit gate summary는 submit path가 budget gate에서 닫혀 별도 작성/호출 대상이 없었다.
- alternate `client_order_id` retry나 `cancel_order_by_id` 호출도 없었다. 두 after-hours `client_order_id` 모두 체결 상태로 reconciliation이 끝났고 다른 `client_order_id`를 새로 만들지 않았다.
- `get_order_by_client_id(ah-20260618-1111-sell-pfe-01)` 기준 `PFE` trim은 `filled_avg_price=25.97 USD`, `filled_at=2026-06-18T02:58:29.784751618Z`로 체결 완료다.
- `get_order_by_client_id(ah-20260618-1131-sell-rgti-01)` 기준 `RGTI` trim은 `filled_avg_price=20.75 USD`, `filled_at=2026-06-18T03:31:57.099382354Z`로 체결 완료다.

## Validators

- `PATH=/usr/local/bin:$PATH python3 scripts/check-universe-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-18-1551-after-hours-autopilot.json` PASS
- `PATH=/usr/local/bin:$PATH python3 scripts/check-mcp-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-18-1551-after-hours-autopilot.json` PASS
- `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-06-18-1551-after-hours-autopilot.json` PASS (warning `orders is empty`)

## Artifacts

- Report: `wiki/current-runs/daily/2026-06-18-1551-after-hours-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-18-1551-after-hours-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-18-1551-after-hours-autopilot.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-06-18-1551-after-hours-autopilot-after-hours-gate-evaluation.json`
- Runtime spot check: `wiki/evidence-store/sources/2026-06-18-1551-after-hours-autopilot-runtime-alpaca-spot-check.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-18-1551-after-hours-autopilot-post-trade.json`
