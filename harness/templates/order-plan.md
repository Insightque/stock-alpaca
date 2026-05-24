# 주문 계획 템플릿

구체적인 주문 계획은 `wiki/portfolio/order-plans/` 아래 JSON 파일로 작성한다. Alpaca MCP로 paper 주문을 제출하기 전 반드시 `scripts/check-risk-policy.py`로 검증한다.

```json
{
  "run_id": "YYYY-MM-DD-daily",
  "schema_version": "1.1",
  "risk_policy_version": "medium-risk-v1",
  "recommendation_policy_sha": "sha256:...",
  "created_at": "YYYY-MM-DDTHH:MM:SSZ",
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
  "orders": [
    {
      "symbol": "SPY",
      "asset_type": "etf",
      "asset_status": "active",
      "asset_tradable": true,
      "side": "buy",
      "order_type": "limit",
      "time_in_force": "day",
      "qty": 1,
      "limit_price": 500.0,
      "reference_price": 500.0,
      "quote_age_minutes": 0,
      "quote_captured_at": "YYYY-MM-DDTHH:MM:SSZ",
      "asset_checked_at": "YYYY-MM-DDTHH:MM:SSZ",
      "source_refs": ["wiki/raw/sources/YYYY-MM-DD-alpaca-market-data.md"],
      "rationale": "주문 근거를 한국어로 기록한다."
    }
  ],
  "source_refs": [
    "wiki/raw/sources/YYYY-MM-DD-alpaca-account-clock.md",
    "wiki/raw/sources/YYYY-MM-DD-alpaca-market-data.md"
  ],
  "manifest_path": "wiki/runs/YYYY-MM-DD-HHMM-run-id.json"
}
```

과거 시점 추천 시뮬레이션에서 생성하는 주문 계획도 같은 형식을 사용하되, 반드시 `mode: "dry_run"`으로 둔다. 각 주문에는 `decision_id`, `historical_asof`, `review_horizons`, `rationale`, `quote_captured_at`, `asset_checked_at`, `source_refs`를 넣어 이후 `wiki/reviews/decisions/` 회고와 leakage 점검에 연결한다.
