# 2026-06-01 15:31 KST 장외 paper autopilot

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Session: `after_hours`
- Policy profile: `after_hours_policy`
- Artifact tag: `after-hours`
- Review bucket: `after_hours_validation`
- Mode: `submit`
- Paper mode: `ALPACA_PAPER_TRADE=true` 확인

## 결론

신규 주문 없음. 장외 전용 session budget이 이미 소진되어 `risk_inputs.after_hours_new_orders_submitted_today=2`가 `after_hours_policy.max_new_orders_per_session=2`에 도달했다. 정규장 validation 주문 수는 재사용하지 않았다.

`place_stock_order` 호출은 없었고, 신규 `client_order_id`, 재시도, alternate client id도 없었다. 제출 시도가 없었기 때문에 신규 주문 reconciliation은 해당 없음이다. 기존 장외 session 주문은 `ah-20260601-0911-nvda-buy-01` canceled/filled_qty 0, `ah-20260601-0931-avgo-buy-01` filled/filled_qty 1로 확인했다.

## Gate 상태

| Gate | Status | Note |
| --- | --- | --- |
| paper mode | PASS | `.env`에서 `ALPACA_PAPER_TRADE=true` 확인 |
| regular market open | PASS | Alpaca clock `is_open=false`; 장외 workflow에서는 정규장 open이면 중단 |
| Alpaca core | PASS | scheduler preflight의 `first_blocking_gate=market_closed`는 장외 run에서 예상된 nonblocking 상태 |
| after-hours policy profile | PASS | `after_hours_policy`, `session=after_hours`, `artifact_tag=after-hours`, `review_bucket=after_hours_validation` |
| universe strict | PASS | 62개 metadata universe, SPY/QQQ 포함 |
| MCP strict | PASS | SEC EDGAR, Firecrawl, Yahoo Finance 3개 positive confirmation; Alpha Vantage empty response, FRED provider_error는 기록 |
| quote/spread | PASS for evidence | runtime Alpaca overnight quote spot-check로 QQQ/NOK/AVGO/NVDA/COST/FCX/UNH/SBUX fresh quote 확인 |
| risk policy | PASS | empty-order plan으로 PASS, warning `orders is empty` |
| separate after-hours order budget | BLOCK | `after_hours_new_orders_submitted_today=2`, session limit 2 도달 |

## Alpaca MCP 확인

- Account: `ACTIVE`, portfolio value 약 102313.19 USD, cash 34339.00 USD.
- Positions: runtime Alpaca MCP `get_all_positions` 기준 32개 US-equity position.
- Open orders: runtime Alpaca MCP `get_orders(status=open, asset_class=us_equity)` 기준 0건.
- Session order history: Alpaca MCP `get_orders(status=all, after=2026-05-31T20:00:00Z)` 기준 장외 client id 2건.
- Asset spot-check: QQQ active/tradable/US equity/overnight tradable.
- Quote spot-check: QQQ, NOK, AVGO, NVDA, COST, FCX, UNH, SBUX overnight quote 확인.

## 산출물

- Manifest: `wiki/evidence-store/run-manifests/2026-06-01-1531-after-hours-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-01-1531-after-hours-autopilot.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-06-01-1531-after-hours-autopilot-after-hours-gate-evaluation.json`
- Scheduler Alpaca preflight: `wiki/evidence-store/sources/2026-06-01-1531-after-hours-autopilot-alpaca-core-preflight.json`
- Scheduler research preflight: `wiki/evidence-store/sources/2026-06-01-1531-after-hours-autopilot-research-mcp-preflight.json`

## 검증

- `PATH=/usr/local/bin:$PATH python3 scripts/check-universe-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-01-1531-after-hours-autopilot.json` PASS
- `PATH=/usr/local/bin:$PATH python3 scripts/check-mcp-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-01-1531-after-hours-autopilot.json` PASS
- `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-06-01-1531-after-hours-autopilot.json` PASS, warning `orders is empty`
