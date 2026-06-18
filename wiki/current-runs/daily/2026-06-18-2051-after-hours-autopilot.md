# 2026-06-18-2051-after-hours-autopilot

## 요약

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Session: `after_hours`
- Policy profile: `after_hours_policy`
- Artifact tag: `after-hours`
- Review bucket: `after_hours_validation`
- Paper mode: `ALPACA_PAPER_TRADE=true` 확인
- 결과: scheduler-owned `2051` Alpaca core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. 같은 preflight의 passing account/positions/open-orders/account-activities/watchlists/asset/quote/spread rows로 submit-boundary evidence를 유지했고, live Alpaca MCP `get_clock/get_account_info/get_all_positions/get_orders(status=open|all)/get_watchlists/get_order_by_client_id` continuity에서도 same-session after-hours submitted orders가 이미 `2/2`로 재확인돼 이번 cycle 신규 submit은 없었다.

## 사용한 스케줄러 프리플라이트

- Alpaca core: `wiki/evidence-store/sources/2026-06-18-2051-after-hours-autopilot-alpaca-core-preflight.json`
- Research MCP: `wiki/evidence-store/sources/2026-06-18-2051-after-hours-autopilot-research-mcp-preflight.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-06-18-2051-after-hours-autopilot-after-hours-gate-evaluation.json`
- Runtime spot check: `wiki/evidence-store/sources/2026-06-18-2051-after-hours-autopilot-runtime-alpaca-spot-check.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-18-2051-after-hours-autopilot-post-trade.json`
- Alpaca core preflight의 `first_blocking_gate=market_closed`는 장외 워크플로우에서 expected nonblocking으로 처리했고, 같은 preflight의 passing account/positions/open-orders/account-activities/watchlists/asset/quote/spread rows를 submit-boundary source-of-record로 유지했다.

## Alpaca MCP 확인

- Regular market: closed (`scheduler-owned get_clock.timestamp=2026-06-18T07:51:05.732036963-04:00`, live `get_clock.timestamp=2026-06-18T07:52:50.32620922-04:00`), after-hours workflow 계속 진행
- Account: source-of-record preflight 기준 account `ACTIVE`, cash `28,050.15 USD`, portfolio value `101,229.88 USD`, buying power `301,367.96 USD`, positions `34`, open orders `0`
- Live continuity: `get_account_info` 기준 account `ACTIVE`, cash `28,050.15 USD`, portfolio value `101,274.86 USD`, buying power `301,482.64 USD`, `get_all_positions` 기준 positions `34`, `get_orders(status=open)` 기준 open orders `0`, `get_watchlists` 기준 watchlists `0`
- Same-session after-hours ledger: live `get_orders(status=all, after=2026-06-17T20:00:00-04:00)`와 exact `client_order_id` reconciliation 기준 `PFE`, `RGTI` prior fills 두 건은 각각 filled 상태로 유지됐고 same-session submitted order budget은 `2/2`로 닫혀 있다.
- Quote / spread evidence: 이번 cycle은 separate after-hours session budget이 먼저 닫혀 새 submit path를 열지 않았고, scheduler-owned `2051` preflight의 passing asset/quote/spread rows를 audit source로 유지했다.

## Gate 결과

| Gate | Status |
| --- | --- |
| alpaca_paper_mode | pass |
| regular_market_open | pass_regular_market_closed |
| extended_hours_session | pass |
| alpaca_core_account_clock_position_order_quote_spread | pass_scheduler_preflight_rows_reused |
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
- alternate `client_order_id` retry나 `cancel_order_by_id` 호출도 없었다. 두 after-hours `client_order_id` 모두 체결 상태로 reconciliation reference만 유지했고 다른 `client_order_id`를 새로 만들지 않았다.
- `ah-20260618-1111-sell-pfe-01`은 `filled_avg_price=25.97 USD` 체결 완료 reference로 유지했다.
- `ah-20260618-1131-sell-rgti-01`은 `filled_avg_price=20.75 USD` 체결 완료 reference로 유지했다.

## Validators

- `PATH=/usr/local/bin:$PATH python3 scripts/check-universe-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-18-2051-after-hours-autopilot.json` PASS
- `PATH=/usr/local/bin:$PATH python3 scripts/check-mcp-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-18-2051-after-hours-autopilot.json` PASS
- `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-06-18-2051-after-hours-autopilot.json` PASS (warning `orders is empty`)

## Artifacts

- Report: `wiki/current-runs/daily/2026-06-18-2051-after-hours-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-18-2051-after-hours-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-18-2051-after-hours-autopilot.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-06-18-2051-after-hours-autopilot-after-hours-gate-evaluation.json`
- Runtime spot check: `wiki/evidence-store/sources/2026-06-18-2051-after-hours-autopilot-runtime-alpaca-spot-check.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-18-2051-after-hours-autopilot-post-trade.json`
