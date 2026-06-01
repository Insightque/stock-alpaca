# 2026-06-01-0931-after-hours-autopilot

## 요약

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Session: `after_hours`
- Policy profile: `after_hours_policy`
- Artifact tag: `after-hours`
- Review bucket: `after_hours_validation`
- Paper mode: `ALPACA_PAPER_TRADE=true` 확인
- 결과: 09:11 NVDA 장외 validation open order는 lifecycle 한도 초과로 취소 및 client_order_id reconcile 완료. 이후 AVGO 1주 after-hours day limit paper buy를 Alpaca MCP로 제출했고 같은 client_order_id 기준 filled 확인.

## 사용한 스케줄러 프리플라이트

- Alpaca core: `wiki/evidence-store/sources/2026-06-01-0931-after-hours-autopilot-alpaca-core-preflight.json`
- Research MCP: `wiki/evidence-store/sources/2026-06-01-0931-after-hours-autopilot-research-mcp-preflight.json`
- Alpaca core `first_blocking_gate=market_closed`는 장외 워크플로우에서 예상되는 상태로, 단독 차단 사유로 보지 않았다. 같은 preflight의 account, positions, open_orders, asset, quote, snapshot, latest_trade pass row를 사용했다.

## Alpaca MCP 확인

- Regular market: closed (`2026-05-31T20:37:46.172814867-04:00`)
- Account/positions/open orders: runtime Alpaca MCP pass
- Prior lifecycle: `ah-20260601-0911-nvda-buy-01` canceled, filled_qty 0, reconciled by client_order_id.
- Post-submit: open US-equity orders `[]`; AVGO position qty 16; account ACTIVE.

## Submitted Order

- AVGO 1주 buy limit 461.59, `time_in_force=day`, `extended_hours=true`, `session=after_hours`, `review_bucket=after_hours_validation`, client_order_id `ah-20260601-0931-avgo-buy-01`.
- Reconciliation: status `filled`, filled_qty 1, filled_avg_price 461.26.
- No retry was attempted and no alternate client order id was used.
- `risk_inputs.after_hours_new_orders_submitted_today=1`; regular validation order count는 장외 예산으로 재사용하지 않았다.

## Quote/Spread

- Runtime overnight AVGO quote: `2026-06-01T00:37:31.654998342Z`, age 0.242 minutes, bid 461.33, ask 461.59, spread 0.056%
- After-hours max quote age: 5.0 minutes
- After-hours max spread: 0.25%

## Artifacts

- Manifest: `wiki/evidence-store/run-manifests/2026-06-01-0931-after-hours-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-01-0931-after-hours-autopilot.json`
- Gate evaluation source: `wiki/evidence-store/sources/2026-06-01-0931-after-hours-autopilot-after-hours-gate-evaluation.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-01-0931-after-hours-autopilot-post-trade.json`

## Gate 결과

| Gate | Status |
| --- | --- |
| alpaca_paper_mode | pass |
| regular_market_open | pass_regular_market_closed |
| extended_hours_session | pass |
| alpaca_core_account_clock_position_order_quote_spread | pass_with_market_closed_expected_nonblocking |
| after_hours_policy_profile | pass |
| separate_after_hours_order_budget | pass |
| stale_prior_order_lifecycle | pass_cancelled_prior_nvda_by_client_order_id |
| universe_strict | pass |
| mcp_tiered_strict | pass |
| risk_policy | pass |
| fresh_quote | pass |
| spread_within_after_hours_policy | pass |
| whole_share_day_limit_extended_hours_order | pass |
| immediate_reconcile_and_cancel_or_lifecycle_record | pass_reconciled_filled_by_client_order_id |

## Validators

- Universe strict: PASS (`PATH=/usr/local/bin:$PATH python3 scripts/check-universe-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-01-0931-after-hours-autopilot.json`)
- MCP strict: PASS (`PATH=/usr/local/bin:$PATH python3 scripts/check-mcp-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-01-0931-after-hours-autopilot.json`)
- Risk policy: PASS (`PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-06-01-0931-after-hours-autopilot.json`)

## Submit/Reconcile

- Pre-submit gate summary was written immediately before the Alpaca MCP submit call.
- Submitted through Alpaca MCP only.
- Reconciled by the same `client_order_id`: status `filled`, filled_qty `1`, filled_avg_price `461.26`.
- No retry was attempted and no alternate client order id was used.
