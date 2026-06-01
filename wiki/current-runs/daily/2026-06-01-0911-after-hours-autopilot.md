# 2026-06-01-0911-after-hours-autopilot

## 요약

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Session: `after_hours`
- Policy profile: `after_hours_policy`
- Artifact tag: `after-hours`
- Review bucket: `after_hours_validation`
- Paper mode: `ALPACA_PAPER_TRADE=true` 확인
- 현재 상태: NVDA 1주 after-hours validation buy 계획 생성, validators 실행 대기.

## 사용한 스케줄러 프리플라이트

- Alpaca core: `wiki/evidence-store/sources/2026-06-01-0911-after-hours-autopilot-alpaca-core-preflight.json`
- Research MCP: `wiki/evidence-store/sources/2026-06-01-0911-after-hours-autopilot-research-mcp-preflight.json`
- Alpaca core `first_blocking_gate=market_closed`는 장외 워크플로우에서 예상되는 상태로, 단독 차단 사유로 보지 않았다. 같은 preflight의 account, positions, open_orders, asset, quote, snapshot, latest_trade pass row를 사용했다.

## Alpaca MCP 확인

- Regular market: closed (`2026-05-31T20:15:26.301467535-04:00`)
- Account: runtime Alpaca MCP pass, identifiers는 기록하지 않음
- Positions: runtime call은 cancelled; scheduler-owned passing positions row 사용
- Open US-equity orders: runtime Alpaca MCP pass, `[]`
- QQQ asset: runtime Alpaca MCP pass(active/tradable/us_equity/overnight_tradable)
- NVDA overnight quote/snapshot: fresh quote pass

## Planned Order

- NVDA 1주 buy limit 214.11, `time_in_force=day`, `extended_hours=true`, `session=after_hours`, `review_bucket=after_hours_validation`, client_order_id `ah-20260601-0911-nvda-buy-01`.
- `risk_inputs.after_hours_new_orders_submitted_today=0`; regular validation order count는 장외 예산으로 재사용하지 않았다.
- QQQ는 fresh/liquid했지만 1주 notional이 장외 per-order 0.5% 한도를 초과해 제외했다.

## Quote/Spread

- Runtime overnight NVDA quote: `2026-06-01T00:15:01.241563643Z`, age 0.418 minutes, bid 214.02, ask 214.11, spread 0.042%
- After-hours max quote age: 5.0 minutes
- After-hours max spread: 0.25%

## Artifacts

- Manifest: `wiki/evidence-store/run-manifests/2026-06-01-0911-after-hours-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-01-0911-after-hours-autopilot.json`
- Gate evaluation source: `wiki/evidence-store/sources/2026-06-01-0911-after-hours-autopilot-after-hours-gate-evaluation.json`

## Gate 결과

| Gate | Status |
| --- | --- |
| alpaca_paper_mode | pass |
| regular_market_open | pass_regular_market_closed |
| extended_hours_session | pass |
| alpaca_core_account_clock_position_order_quote_spread | pass_with_market_closed_expected_nonblocking |
| after_hours_policy_profile | pass |
| separate_after_hours_order_budget | pass |
| universe_strict | pass |
| mcp_tiered_strict | pass |
| risk_policy | pass |
| fresh_quote | pass |
| spread_within_after_hours_policy | pass |
| whole_share_day_limit_extended_hours_order | pass |
| immediate_reconcile_and_cancel_or_lifecycle_record | pending_submit |

## Validators

- Universe strict: PASS (`PATH=/usr/local/bin:$PATH python3 scripts/check-universe-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-01-0911-after-hours-autopilot.json`)
- MCP strict: PASS (`PATH=/usr/local/bin:$PATH python3 scripts/check-mcp-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-01-0911-after-hours-autopilot.json`)
- Risk policy: PASS (`PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-06-01-0911-after-hours-autopilot.json`)

## Submit/Reconcile

- Pre-submit gate summary was written immediately before the Alpaca MCP submit call.
- Submitted through Alpaca MCP only: NVDA 1주 buy limit 214.11, `time_in_force=day`, `extended_hours=true`, `session=after_hours`, `review_bucket=after_hours_validation`, client_order_id `ah-20260601-0911-nvda-buy-01`.
- Reconciled by the same `client_order_id`: status `new`, filled_qty `0`, filled_avg_price `null`.
- No retry was attempted and no alternate client order id was used.
- Lifecycle: order is recorded as open/new; immediate cancel is not applied before the after-hours policy unfilled-age threshold.
