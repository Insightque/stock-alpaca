# 2026-05-31-2031-after-hours-autopilot

## 요약

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Session: `after_hours`
- Policy profile: `after_hours_policy`
- Artifact tag: `after-hours`
- Review bucket: `after_hours_validation`
- Paper mode: `ALPACA_PAPER_TRADE=true` 확인
- 결과: 주문 없음. `fresh_quote` gate 실패로 `place_stock_order` 호출 전 차단.

## 사용한 스케줄러 프리플라이트

- Alpaca core: `wiki/evidence-store/sources/2026-05-31-2031-after-hours-autopilot-alpaca-core-preflight.json`
- Research MCP: `wiki/evidence-store/sources/2026-05-31-2031-after-hours-autopilot-research-mcp-preflight.json`
- Alpaca core `first_blocking_gate=market_closed`는 장외 워크플로우에서 예상되는 상태로, 단독 차단 사유로 보지 않았다. 같은 preflight의 account, positions, open_orders, asset, quote, snapshot, latest_trade pass row를 사용했다.

## Alpaca MCP 확인

- Regular market: closed (`2026-05-31T07:31:07.917854697-04:00`)
- Account/open US-equity orders: scheduler Alpaca MCP pass row 사용; account identifiers는 기록하지 않음
- Positions: runtime Alpaca MCP pass, 32개 포지션 확인
- QQQ asset: scheduler Alpaca MCP pass(active/tradable/us_equity/overnight_tradable). Runtime asset read는 safety monitor가 차단해 scheduler-owned row를 유지
- Runtime overnight quote/snapshot: pass, but stale versus after-hours freshness cap

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
| risk_policy | pass_empty_order_plan_warning_only |
| fresh_quote | fail |
| spread_within_after_hours_policy | pass |
| whole_share_day_limit_extended_hours_order | not_applicable_no_orders |
| immediate_reconcile_and_cancel_or_lifecycle_record | not_applicable_no_submit_attempt |

## Quote/Spread

- Scheduler QQQ quote: `2026-05-29T20:58:00.000802558Z`, age 2317.45 minutes, bid 737.95, ask 738.04, spread 0.0122%
- Runtime overnight QQQ quote: `2026-05-29T08:00:00.386377592Z`, age 3095.44 minutes, bid 735.21, ask 736.7, spread 0.2025%
- Scheduler QQQ latest trade: `2026-05-29T20:40:59.963546484Z`, age 2334.45 minutes
- Runtime overnight latest trade: `2026-05-29T07:59:14.99126611Z`, age 3096.2 minutes
- After-hours max quote age: 5.0 minutes
- After-hours max spread: 0.25%

Fresh quote가 정책 한도를 초과했으므로 주문 후보를 생성하지 않았고, pre-submit gate summary 및 `place_stock_order` 호출은 발생하지 않았다.

## 주문/리컨실리에이션

- `risk_inputs.after_hours_new_orders_submitted_today=0`
- Regular validation order count는 장외 예산으로 재사용하지 않았다.
- Submitted orders: 0
- Client order ids: none
- Reconciliation: no submit attempt

## Artifacts

- Manifest: `wiki/evidence-store/run-manifests/2026-05-31-2031-after-hours-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-05-31-2031-after-hours-autopilot.json`
- Gate evaluation source: `wiki/evidence-store/sources/2026-05-31-2031-after-hours-autopilot-after-hours-gate-evaluation.json`

## Validators

- Universe strict: PASS (`PATH=/usr/local/bin:$PATH python3 scripts/check-universe-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-05-31-2031-after-hours-autopilot.json`)
- MCP strict: PASS (`PATH=/usr/local/bin:$PATH python3 scripts/check-mcp-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-05-31-2031-after-hours-autopilot.json`)
- Risk policy: PASS with expected `orders is empty` warning (`PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-05-31-2031-after-hours-autopilot.json`)
