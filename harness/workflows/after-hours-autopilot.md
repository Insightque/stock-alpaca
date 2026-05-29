# Workflow: After-Hours Paper Autopilot

Use this only when the user explicitly asks for after-hours Alpaca paper automation or when the scheduled wrapper is launched with the explicit after-hours probe flag.

## Goal

Run a separate after-hours paper validation loop without mixing its policy, order budget, artifacts, or reviews with regular-session `hourly-autopilot`.

The machine-readable source of truth is `harness/recommendation-policy.yaml` under `after_hours_policy`. Do not copy numeric limits from that YAML into this workflow.

## Separation Rules

- Session tag must be `after_hours`.
- Order plans must set `market.session=after_hours`.
- Every after-hours order must set `extended_hours=true`.
- Every after-hours order must set `session=after_hours`.
- Every after-hours order must set `review_bucket` from `after_hours_policy.review_bucket`.
- Client order ids must use `after_hours_policy.order_id_prefix`.
- Artifacts should include `after_hours_policy.artifact_tag` in the run id or filename.
- After-hours order counts must use `risk_inputs.after_hours_new_orders_submitted_today`; do not reuse the regular validation count as the after-hours session budget.
- Reviews must be recorded in the after-hours review bucket and must not be merged into regular-session validation conclusions unless a later policy review explicitly compares the buckets.
- Do not import regular-session sell/trim or force-exit behavior into this workflow unless `after_hours_policy.allowed_sides` explicitly permits that side. If a regular-session risk-trim concern is noticed here, record it as a diagnostic for the next regular-session review rather than silently submitting outside the allowed side set.

## Gates

After-hours orders may be submitted only when all of these pass:

- `ALPACA_PAPER_TRADE=true`.
- Alpaca MCP account, clock, positions, orders, asset, quote, and spread evidence.
- `after_hours_policy.hard_gates`.
- Universe strict gate.
- MCP strict gate.
- Risk gate through `scripts/check-risk-policy.py`.
- Whole-share day limit stock or ETF order shape.
- `extended_hours=true`.

The regular-session `market.is_open=true` gate does not apply to this workflow. Instead, `scripts/check-risk-policy.py` validates `market.session=after_hours` and applies the after-hours policy profile from `harness/recommendation-policy.yaml`.

## Procedure

1. Confirm paper mode from `.env`.
2. Read `harness/risk-policy.yaml` and `harness/recommendation-policy.yaml`.
3. Capture Alpaca MCP clock/account/position/open-order/asset/quote evidence.
4. Build a run manifest with `session=after_hours`, MCP coverage, universe coverage, source refs, and the after-hours policy profile id.
5. Create an order plan under `wiki/trade-ledger/orders/` with `market.session=after_hours`.
6. Validate universe coverage, MCP coverage, and risk policy before any submit.
7. Submit only through Alpaca MCP `place_stock_order`.
8. Reconcile by `client_order_id` immediately.
9. Cancel or lifecycle-record unfilled validation orders according to `after_hours_policy`.
10. Append `wiki/log.md` with the after-hours session tag, artifact paths, submit/reconcile/cancel status, and review bucket.

## Stop Conditions

- Paper mode is not true.
- The explicit after-hours workflow or probe flag is absent.
- The order plan lacks after-hours session tags.
- Any after-hours order lacks `extended_hours=true`.
- The separate after-hours order budget is missing or exceeded.
- The review bucket is missing or points to the regular validation bucket.
- Alpaca core MCP, universe, MCP coverage, quote, spread, or risk gate fails.
- Reconciliation by `client_order_id` fails after submit.
