# 2026-06-01-1011-after-hours-autopilot

## 요약

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Session: `after_hours`
- Policy profile: `after_hours_policy`
- Artifact tag: `after-hours`
- Review bucket: `after_hours_validation`
- Paper mode: `ALPACA_PAPER_TRADE=true` 확인
- 결과: Alpaca regular market closed, Alpaca core/research/universe gate와 live quote/spread evidence는 주문 가능 조건을 충족했지만 장외 전용 session budget이 이미 2건으로 소진되어 신규 주문을 제출하지 않았다.

## 사용한 스케줄러 프리플라이트

- Alpaca core: `wiki/evidence-store/sources/2026-06-01-1011-after-hours-autopilot-alpaca-core-preflight.json`
- Research MCP: `wiki/evidence-store/sources/2026-06-01-1011-after-hours-autopilot-research-mcp-preflight.json`
- Alpaca core `first_blocking_gate=market_closed`는 장외 워크플로우에서 예상되는 상태로, 단독 차단 사유로 보지 않았다. 같은 preflight의 account, positions, open_orders, asset, quote, snapshot row를 사용했다.

## Alpaca MCP 확인

- Regular market: closed (`2026-05-31T21:11:08.992090709-04:00`)
- Account/positions: runtime Alpaca MCP pass
- Open US-equity orders: scheduler preflight `[]`; runtime spot-check는 cancelled라 preflight pass row를 유지했다.
- Same after-hours session orders: `ah-20260601-0911-nvda-buy-01` canceled, `ah-20260601-0931-avgo-buy-01` filled.

## 주문 판단

- `risk_inputs.after_hours_new_orders_submitted_today=2`; regular validation order count는 장외 예산으로 재사용하지 않았다.
- `after_hours_policy.max_new_orders_per_session=2`에 도달해 신규 order candidate를 만들지 않았다.
- 따라서 `place_stock_order` 호출, `client_order_id` 생성, submit retry, reconcile은 모두 해당 없음.

## Quote/Spread

- Runtime overnight QQQ/NVDA/AVGO quote는 fresh였고 spread도 after-hours 한도 안에 있었다.
- Submit gate는 quote/spread가 아니라 별도 장외 session budget에서 차단되었다.

## Artifacts

- Manifest: `wiki/evidence-store/run-manifests/2026-06-01-1011-after-hours-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-01-1011-after-hours-autopilot.json`
- Gate evaluation source: `wiki/evidence-store/sources/2026-06-01-1011-after-hours-autopilot-after-hours-gate-evaluation.json`

## Gate 결과

| Gate | Status |
| --- | --- |
| alpaca_paper_mode | pass |
| regular_market_open | pass_regular_market_closed |
| extended_hours_session | pass |
| alpaca_core_account_clock_position_order_quote_spread | pass_with_market_closed_expected_nonblocking |
| after_hours_policy_profile | pass |
| separate_after_hours_order_budget | block_after_hours_session_budget_exhausted |
| universe_strict | pass |
| mcp_tiered_strict | pass |
| risk_policy | pass_empty_order_plan |
| fresh_quote | pass |
| spread_within_after_hours_policy | pass |
| whole_share_day_limit_extended_hours_order | not_applicable_no_order |
| immediate_reconcile_and_cancel_or_lifecycle_record | not_applicable_no_submit |

## Validators

- Universe strict: PASS (`PATH=/usr/local/bin:$PATH python3 scripts/check-universe-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-01-1011-after-hours-autopilot.json`)
- MCP strict: PASS (`PATH=/usr/local/bin:$PATH python3 scripts/check-mcp-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-01-1011-after-hours-autopilot.json`)
- Risk policy: PASS (`PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-06-01-1011-after-hours-autopilot.json`; warning: `orders is empty`)
