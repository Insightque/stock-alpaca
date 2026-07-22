# 2026-07-22-2151-after-hours-autopilot

## 요약

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Session: `after_hours`
- Policy profile: `after_hours_policy`
- Artifact tag: `after-hours`
- Review bucket: `after_hours_validation`
- Market date: `2026-07-22 EDT`
- Scheduler artifact date: `2026-07-22 KST`
- Paper mode: `ALPACA_PAPER_TRADE=true` 확인
- 결과: scheduler-owned `2151` core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. `2151` preflight는 `NOK 10.29/10.31` two-sided row를 유지해 sell-first path 자체는 열려 있었지만, live continuity 기준 same-session after-hours submitted orders/fills가 이미 `2/2`로 닫혀 separate session budget이 먼저 소진됐다. 따라서 이번 cycle은 신규 `place_stock_order` 없이 기존 `AVGO`/`NOK` client order id만 재정산하는 reconcile-only run으로 종료했다.

## 사용한 스케줄러 프리플라이트

- Alpaca core: `wiki/evidence-store/sources/2026-07-22-2151-after-hours-autopilot-alpaca-core-preflight.json`
- Research MCP: `wiki/evidence-store/sources/2026-07-22-2151-after-hours-autopilot-research-mcp-preflight.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-07-22-2151-after-hours-autopilot-after-hours-gate-evaluation.json`
- Alpaca core preflight의 `first_blocking_gate=market_closed`는 after-hours 워크플로우에서 expected nonblocking으로 처리했다.

## Alpaca MCP 확인

- Source-of-record account / positions / open orders / asset / quote / spread rows는 scheduler-owned `2151` Alpaca core preflight를 사용했다.
- Live continuity는 Alpaca MCP `get_clock/get_account_info/get_all_positions/get_orders(status=open|all)/get_watchlists/get_order_by_client_id(client_order_id=ah-20260722-0911-sell-avgo-01)/get_order_by_client_id(client_order_id=ah-20260722-2111-sell-nok-01)`로 닫았다. regular market은 `2026-07-22T08:53:31.221834743-04:00`에도 계속 closed였고, account `ACTIVE`, positions `31`, open orders `0`, watchlists `0`였다.
- Same-session reconciliation 기준 `AVGO` sell은 `status=filled`, `filled_qty=1`, `filled_avg_price=384.14 USD`, `filled_at=2026-07-22T01:48:58.933756Z`였고 `NOK` sell은 `status=filled`, `filled_qty=1`, `filled_avg_price=10.33 USD`, `filled_at=2026-07-22T12:30:02.329191394Z`였다.
- `NOK qty=401`, `SO qty=6`, `QQQ qty=3`, `SPY qty=2`, `WMT qty=10`, `AVGO position 없음`을 재확인했다.

## 후보 평가

- `NOK` sell/trim: source-of-record quote `10.29/10.31`, spread `0.1940%`, quote age 약 `3.77`분으로 executable sell-first path 자체는 열려 있었다. 다만 same-session after-hours budget이 이미 `2/2`로 소진돼 `separate_after_hours_order_budget`에서 차단됐다.
- `SPY` buy fallback: source-of-record quote `745.89/746.04`, spread `0.0201%`였지만 submit boundary 기준 quote age 약 `16.08`분으로 stale이고 1주 ask도 `after_hours_policy.max_notional_pct_per_order=0.005` cap을 넘었다.
- `SMH`: quote age 약 `46.58`분, spread `1.5713%`로 stale + spread fail이다.
- `SO` / `WMT`: stale 또는 one-sided quote로 hard gate fail이다.
- 이번 cycle의 first blocking gate는 `separate_after_hours_order_budget`였다.

## Gate 결과

| Gate | Status |
| --- | --- |
| alpaca_paper_mode | pass |
| regular_market_open | pass_regular_market_closed |
| extended_hours_session | pass |
| alpaca_core_account_clock_position_order_quote_spread | pass_scheduler_preflight_plus_live_reconciliation |
| after_hours_policy_profile | pass |
| separate_after_hours_order_budget | FAIL `2/2` |
| universe_strict | PASS |
| mcp_tiered_strict | PASS |
| risk_policy | PASS |
| fresh_quote | PASS_nok_3.77_minutes |
| spread_within_after_hours_policy | PASS_nok_0.1940pct |
| whole_share_day_limit_extended_hours_order | PASS_sell_shape_if_budget_opened |
| immediate_reconcile_and_cancel_or_lifecycle_record | PASS_existing_client_order_ids_reconciled |

## Submit And Reconcile

- Submitted order this cycle: 없음
- Pre-submit gate summary: 신규 `place_stock_order` 호출이 없어서 작성하지 않았다. submit branch 진입 전 `separate_after_hours_order_budget`이 fail했다.
- Reconciled prior after-hours orders:
  - `AVGO` sell `1` share, `limit_price=384.13`, `time_in_force=day`, `extended_hours=true`, `session=after_hours`, `review_bucket=after_hours_validation`, `client_order_id=ah-20260722-0911-sell-avgo-01`
  - `NOK` sell `1` share, `limit_price=10.33`, `time_in_force=day`, `extended_hours=true`, `session=after_hours`, `review_bucket=after_hours_validation`, `client_order_id=ah-20260722-2111-sell-nok-01`
- Retry discipline: alternate `client_order_id`는 사용하지 않았고 기존 주문 두 건의 fill 상태만 continuity로 재확인했다.

## Artifacts

- Report: `wiki/current-runs/daily/2026-07-22-2151-after-hours-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-07-22-2151-after-hours-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-07-22-2151-after-hours-autopilot.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-07-22-2151-after-hours-autopilot-after-hours-gate-evaluation.json`
- Post-trade check: `wiki/trade-ledger/positions/2026-07-22-2151-after-hours-autopilot-post-trade.json`

## Validators

- `PATH=/usr/local/bin:$PATH python3 scripts/check-universe-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-07-22-2151-after-hours-autopilot.json`
- `PATH=/usr/local/bin:$PATH python3 scripts/check-mcp-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-07-22-2151-after-hours-autopilot.json`
- `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-07-22-2151-after-hours-autopilot.json`
