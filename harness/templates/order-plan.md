# 주문 계획 템플릿

구체적인 주문 계획은 `wiki/portfolio/order-plans/` 아래 JSON 파일로 작성한다. Alpaca MCP로 paper 주문을 제출하기 전 반드시 `scripts/check-risk-policy.py`로 검증한다.

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

과거 시점 추천 시뮬레이션에서 생성하는 주문 계획도 같은 형식을 사용하되, 반드시 `mode: "dry_run"`으로 둔다. 각 주문에는 선택적으로 `decision_id`, `historical_asof`, `review_horizons`, `rationale`을 넣어 이후 `wiki/reviews/decisions/` 회고와 연결한다.
