# 2026-06-11-1311-after-hours-autopilot

## 요약

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Session: `after_hours`
- Policy profile: `after_hours_policy`
- Artifact tag: `after-hours`
- Review bucket: `after_hours_validation`
- Paper mode: `ALPACA_PAPER_TRADE=true` 확인
- 결과: scheduler-owned `1311` core/research preflight를 source-of-record로 사용했고 Alpaca core preflight의 `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. runtime Alpaca MCP cross-check 결과 regular market은 계속 closed, account는 `ACTIVE`, open orders는 `0`, same-session after-hours fills는 `2`건으로 유지됐고 separate session budget `2/2`가 이미 소진돼 no-submit으로 종료했다.

## 사용한 스케줄러 프리플라이트

- Alpaca core: `wiki/evidence-store/sources/2026-06-11-1311-after-hours-autopilot-alpaca-core-preflight.json`
- Research MCP: `wiki/evidence-store/sources/2026-06-11-1311-after-hours-autopilot-research-mcp-preflight.json`
- Alpaca core preflight는 `first_blocking_gate=market_closed`만 regular-session blocker로 남겼다. after-hours run에서는 이를 nonblocking으로 처리했고 scheduler-owned passing account/positions/orders rows를 유지한 채 runtime Alpaca MCP `get_clock`, `get_account_info`, `get_all_positions`, `get_orders`, `get_account_activities`, `get_watchlists`, `get_order_by_client_id`로 same-session budget evidence를 다시 확인했다.

## Alpaca MCP 확인

- Regular market: scheduler preflight 기준 closed (`timestamp=2026-06-11T00:11:08.962884423-04:00`); runtime Alpaca MCP `get_clock`도 `timestamp=2026-06-11T00:12:30.326191554-04:00`로 여전히 closed였다.
- Account/positions: runtime `get_account_info/get_all_positions` cross-check에서는 account `ACTIVE`, portfolio value `97549.58 USD`, cash `30904.65 USD`, buying power `295197.64 USD`, positions `33`건이 유지됐다. `RGTI`는 `49주`, `qty_available=49`, `avg_entry_price=25.569583 USD`로 확인됐다.
- Open orders / same-session orders / watchlists: runtime `get_orders(status=open)`는 `0`건, `get_orders(status=all, after=2026-06-10T20:00:00Z)`와 `get_account_activities(activity_types=FILL, after=2026-06-10T20:00:00Z)`는 `ah-20260611-1011-sell-rgti`, `ah-20260611-0951-sell-rgti` 두 건의 `filled` record만 남겼고 `get_watchlists`도 `0`건이었다.

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
- Separate after-hours session budget은 `after_hours_new_orders_submitted_today=2`로 `after_hours_policy.max_new_orders_per_session=2`에 도달해 submit path 진입 전에 차단됐다. regular validation count는 재사용하지 않았고, `risk_inputs.after_hours_new_orders_submitted_today`만 별도 세션 예산 근거로 사용했다.
- Reconciliation은 기존 same-session client order id `ah-20260611-0951-sell-rgti`, `ah-20260611-1011-sell-rgti`가 이미 filled 상태임을 확인하는 용도로만 수행했다.

## Validators

- `PATH=/usr/local/bin:$PATH python3 scripts/check-universe-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-11-1311-after-hours-autopilot.json`
  - 결과: PASS
- `PATH=/usr/local/bin:$PATH python3 scripts/check-mcp-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-11-1311-after-hours-autopilot.json`
  - 결과: PASS
- `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-06-11-1311-after-hours-autopilot.json`
  - 결과: PASS

## Artifacts

- Manifest: `wiki/evidence-store/run-manifests/2026-06-11-1311-after-hours-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-11-1311-after-hours-autopilot.json`
- Gate evaluation source: `wiki/evidence-store/sources/2026-06-11-1311-after-hours-autopilot-after-hours-gate-evaluation.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-11-1311-after-hours-autopilot-post-trade.json`

## 지표 설명

- `same-session after-hours fills`: 같은 after-hours 세션 안에서 이미 제출되어 체결된 주문 수다. 이번 cycle에서는 `RGTI` trim 2건이 이미 filled라 separate session budget이 `2/2`로 닫혀 있었다.
- `separate_after_hours_order_budget`: regular-session validation 주문 수와 분리된 장외 전용 주문 예산이다. `risk_inputs.after_hours_new_orders_submitted_today`만 근거로 계산한다.
- `market_closed expected nonblocking`: Alpaca core preflight의 regular-session blocker가 after-hours workflow에서는 정상 상태일 수 있음을 뜻한다. 이 경우 account/positions/orders/quote rows가 pass면 계속 사용한다.
