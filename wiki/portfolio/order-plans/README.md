# Order Plans

Order plans are JSON files generated before any paper order submission.

Validate each plan with:

```bash
python3 scripts/check-risk-policy.py wiki/portfolio/order-plans/YOUR-PLAN.json
```

Only submit orders through Alpaca MCP after validation passes.

