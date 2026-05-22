# Order Plan Template

Create concrete order plans as JSON files in `wiki/portfolio/order-plans/` and validate them with `scripts/check-risk-policy.py` before using Alpaca MCP to submit paper orders.

```json
{
  "run_id": "YYYY-MM-DD-daily",
  "mode": "dry_run",
  "paper": true,
  "market": {
    "is_open": false,
    "checked_at": "YYYY-MM-DDTHH:MM:SSZ"
  },
  "account": {
    "portfolio_value": 100000.0,
    "cash": 100000.0,
    "buying_power": 200000.0
  },
  "positions": [],
  "orders": []
}
```

