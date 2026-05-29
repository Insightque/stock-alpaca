# Medium Risk Policy

This policy is intentionally simple and conservative enough for automated paper trading while still allowing meaningful allocation experiments.

`harness/risk-policy.yaml` is the machine-readable source of truth. This Markdown page explains the same policy for humans; if a numeric limit changes, update the YAML first and then this page.

Current policy version: `medium-risk-v1.1`.

## Portfolio Limits

- Read numeric portfolio, exposure, run-order, daily-order, turnover, realized-loss, and stop-trigger limits from `harness/risk-policy.yaml`.
- Do not duplicate numeric policy caps in workflow instructions or run reports except as observed values copied from the active YAML during a specific run.

## Asset And Order Limits

- Allowed: active tradable US stocks and ETFs.
- Disallowed: live trading, options, crypto, shorts, margin-specific strategies, bracket orders, trailing stops, and fractional shares.
- Allowed order type: day limit orders only.
- Limit guardrail, quote freshness, minimum price, average daily dollar volume, spread, and liquidity-bucket limits come from `harness/risk-policy.yaml`.
- Buy orders must fit within current cash without relying on sell proceeds from the same run.
- The daily new-order cap applies only to the sides listed in `daily_limits.max_new_orders_per_day_applies_to_sides`. Under the current policy this is `buy`, so a consumed validation-buy budget must not block risk-reducing sell/trim orders.
- Buy-quality gates such as positive candidate status, minimum confidence, and source-confidence floor apply to new buys. Risk-reducing sells may use low confidence, rejected thesis status, or failed source quality as the reason to trim or exit, but they must use `entry_style=trim` or `entry_style=exit` and still pass held-quantity, quote, spread, open-order, and risk checks.
- Submit-mode orders must include `client_order_id`, and duplicate same-run orders with the same ticker, side, quantity, and limit are rejected.
- Each symbol must have exposure metadata from the order plan and `harness/symbol-metadata.yaml`: `theme`, `factor`, `volatility_bucket`, `speculative_flag`, `liquidity_bucket`, `source_confidence`, and `correlated_cluster`.
- Observation-only, comparison-only, and rejected strategies cannot create new buy order-plan entries. Submit-mode buy orders require `policy_status=auto_eligible_paper`.

## Order Lifecycle Limits

- Open-order age, duplicate handling, partial-fill, and retry limits come from `harness/risk-policy.yaml`.
- Duplicate `client_order_id` and `decision_id` values are rejected.
- Duplicate symbol+side orders on the same day are rejected when an open order already exists.
- Partial fills require risk recomputation before additional orders.
- Retry must use an idempotent `client_order_id`.

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
