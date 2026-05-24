# Medium Risk Policy

This policy is intentionally simple and conservative enough for automated paper trading while still allowing meaningful allocation experiments.

`harness/risk-policy.yaml` is the machine-readable source of truth. This Markdown page explains the same policy for humans; if a numeric limit changes, update the YAML first and then this page.

Current policy version: `medium-risk-v1`.

## Portfolio Limits

- Keep at least 20% of portfolio value in cash after new buy orders.
- Keep total invested exposure at or below 80% of portfolio value after new orders.
- Keep target exposure per ticker at or below 20% of portfolio value.
- Keep post-order theme exposure at or below 35% of portfolio value.
- Keep post-order factor exposure at or below 50% of portfolio value.
- Keep post-order speculative exposure at or below 12% of portfolio value.
- Submit at most 10 new orders per run.

## Asset And Order Limits

- Allowed: active tradable US stocks and ETFs.
- Disallowed: live trading, options, crypto, shorts, margin-specific strategies, bracket orders, trailing stops, and fractional shares.
- Allowed order type: day limit orders only.
- Limit prices must be within 0.5% of the recorded reference price.
- Submit-mode quote data must be no older than 20 minutes.
- Buy orders must fit within current cash without relying on sell proceeds from the same run.
- Submit-mode orders must include `client_order_id`, and duplicate same-run orders with the same ticker, side, quantity, and limit are rejected.
- Each symbol must have exposure metadata from the order plan or `harness/risk-policy.yaml`: `theme`, `factor`, `volatility_bucket`, and `speculative_flag`.

## Order Plan Metadata

New order plans must conform to `harness/order-plan.schema.json` and include provenance fields:

- `schema_version`
- `risk_policy_version`
- `recommendation_policy_sha`
- `created_at`
- root-level `source_refs`
- per-order `quote_captured_at`, `asset_checked_at`, and `source_refs`

Validate plans with human output or JSON output:

```bash
python3 scripts/check-risk-policy.py wiki/portfolio/order-plans/YOUR-PLAN.json
python3 scripts/check-risk-policy.py --json wiki/portfolio/order-plans/YOUR-PLAN.json
```

## Failure Policy

If a proposed order plan violates any rule, do not submit orders. Update the relevant report with:

- The skipped ticker/order.
- The failing rule.
- The data source used for the decision.
- The next question or data gap to resolve.
