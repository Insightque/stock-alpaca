# 주문 계획 템플릿

구체적인 주문 계획은 `wiki/portfolio/order-plans/` 아래 JSON 파일로 작성한다. Alpaca MCP로 paper 주문을 제출하기 전 반드시 `scripts/check-risk-policy.py`로 검증한다.

```json
{
  "run_id": "YYYY-MM-DD-daily",
  "schema_version": "1.2",
  "risk_policy_version": "medium-risk-v1.1",
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
  "risk_inputs": {
    "policy_turnover_ratio": 0.05,
    "weekly_turnover_ratio": 0.10,
    "stop_triggered_orders_today": 0,
    "risk_recomputed_after_partial_fill": true
  },
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
      "theme": "broad_market",
      "factor": "broad_index",
      "volatility_bucket": "low",
      "speculative_flag": false,
      "liquidity_bucket": "mega",
      "source_confidence": "high",
      "correlated_cluster": "broad_index",
      "strategy_id": "long-term-quality-momentum-v1",
      "strategy_version": "1.0",
      "policy_status": "active_dry_run_candidate",
      "expected_excess_return_20d_pct": 3.0,
      "expected_adverse_move_20d_pct": -4.0,
      "confidence_score": 0.75,
      "sizing_basis": "dual benchmark + drawdown/vol guard + theme cap room",
      "entry_style": "staged",
      "max_additional_entry_count": 2,
      "liquidity": {
        "bid": 499.95,
        "ask": 500.05,
        "spread_pct": 0.02,
        "avg_daily_dollar_volume": 20000000000,
        "quote_source": "alpaca",
        "measured_at": "YYYY-MM-DDTHH:MM:SSZ"
      },
      "client_order_id": "YYYYMMDD-SPY-buy-001",
      "decision_id": "YYYYMMDD-SPY-long-term-quality-momentum-v1",
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

과거 시점 추천 시뮬레이션에서 생성하는 주문 계획도 같은 형식을 사용하되, 반드시 `mode: "dry_run"`으로 둔다. 각 주문에는 `decision_id`, `client_order_id`, `strategy_id`, `policy_status`, 기대 초과수익, 기대 불리 이동, `confidence_score`, 유동성 정보, `historical_asof`, `review_horizons`, `rationale`, `quote_captured_at`, `asset_checked_at`, `source_refs`를 넣어 이후 `wiki/reviews/decisions/` 회고와 leakage 점검에 연결한다.
