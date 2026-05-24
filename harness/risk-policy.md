# Medium Risk Policy

This policy is intentionally simple and conservative enough for automated paper trading while still allowing meaningful allocation experiments.

`harness/risk-policy.yaml` is the machine-readable source of truth. This Markdown page explains the same policy for humans; if a numeric limit changes, update the YAML first and then this page.

Current policy version: `medium-risk-v1.1`.

## Portfolio Limits

- Keep at least 20% of portfolio value in cash after new buy orders.
- Keep total invested exposure at or below 80% of portfolio value after new orders.
- Keep target exposure per ticker at or below 15% of portfolio value.
- Keep post-order theme exposure at or below 35% of portfolio value.
- Keep post-order factor exposure at or below 50% of portfolio value.
- Keep post-order speculative exposure at or below 12% of portfolio value.
- Keep post-order correlated-cluster exposure at or below 45% of portfolio value unless a stricter cluster-specific cap applies.
- Submit at most 10 new orders per run.
- Keep policy turnover at or below 20% of portfolio value per day and 40% per week.
- Stop new submit-mode orders if daily realized loss exceeds 2% of portfolio value or more than 3 stop-triggered orders occurred that day.

## Asset And Order Limits

- Allowed: active tradable US stocks and ETFs.
- Disallowed: live trading, options, crypto, shorts, margin-specific strategies, bracket orders, trailing stops, and fractional shares.
- Allowed order type: day limit orders only.
- Limit prices must be within 0.5% of the recorded reference price.
- Submit-mode quote data must be no older than 20 minutes.
- Order reference prices must be at least $5.
- Average daily dollar volume must be at least $50,000,000.
- Spread must be present and no wider than 0.50%.
- Buy orders must fit within current cash without relying on sell proceeds from the same run.
- Submit-mode orders must include `client_order_id`, and duplicate same-run orders with the same ticker, side, quantity, and limit are rejected.
- Each symbol must have exposure metadata from the order plan and `harness/symbol-metadata.yaml`: `theme`, `factor`, `volatility_bucket`, `speculative_flag`, `liquidity_bucket`, `source_confidence`, and `correlated_cluster`.
- Observation-only, comparison-only, and rejected strategies cannot create order-plan entries. Submit-mode orders require `policy_status=auto_eligible_paper`.

## Order Lifecycle Limits

- Open orders older than 30 minutes block a new conflicting order until reconciled.
- Duplicate `client_order_id` and `decision_id` values are rejected.
- Duplicate symbol+side orders on the same day are rejected when an open order already exists.
- Partial fills require risk recomputation before additional orders.
- Retry is allowed at most once and only with an idempotent `client_order_id`.

## Order Plan Metadata

New order plans must conform to `harness/order-plan.schema.json` and include provenance fields:

- `schema_version`
- `risk_policy_version`
- `recommendation_policy_sha`
- `created_at`
- root-level `source_refs`
- `risk_inputs` for turnover, weekly turnover, stop-trigger count, and partial-fill recomputation.
- per-order strategy status, expected excess return, expected adverse move, confidence score, sizing basis, liquidity object, `client_order_id`, `decision_id`, `quote_captured_at`, `asset_checked_at`, and `source_refs`.

Validate plans with human output or JSON output:

```bash
python3 scripts/check-risk-policy.py wiki/trade-ledger/orders/YOUR-PLAN.json
python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/YOUR-PLAN.json
```

## Failure Policy

If a proposed order plan violates any rule, do not submit orders. Update the relevant report with:

- The skipped ticker/order.
- The failing rule.
- The data source used for the decision.
- The next question or data gap to resolve.
