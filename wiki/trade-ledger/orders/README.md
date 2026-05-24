# Order Plans

Order plans are JSON files generated before any paper order submission.

Validate each plan with:

```bash
python3 scripts/check-risk-policy.py wiki/trade-ledger/orders/YOUR-PLAN.json
python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/YOUR-PLAN.json
```

New plans use `harness/order-plan.schema.json` and must include provenance fields such as `schema_version`, `risk_policy_version`, `recommendation_policy_sha`, `created_at`, root `source_refs`, and per-order `quote_captured_at`, `asset_checked_at`, and `source_refs`.

Only submit orders through Alpaca MCP after validation passes.
