# 2026-05-28 21:31 KST after-hours autopilot

## 요약

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Session: `after_hours`
- Artifact tag: `after-hours`
- Review bucket: `after_hours_validation`
- Mode: `submit`, paper only
- Result: 주문 없음

`ALPACA_PAPER_TRADE=true`를 확인했다. Alpaca MCP clock은 `2026-05-28T08:33:05.88208016-04:00` 기준 정규장이 닫혀 있음을 확인했고, 정규장 open 상태가 아니므로 after-hours workflow 조건과 충돌하지 않았다.

## 사용한 소스

- Scheduler Alpaca core preflight: `wiki/evidence-store/sources/2026-05-28-2131-after-hours-autopilot-alpaca-core-preflight.json`
- Scheduler research MCP preflight: `wiki/evidence-store/sources/2026-05-28-2131-after-hours-autopilot-research-mcp-preflight.json`
- Fresh Alpaca MCP spot checks: `get_clock`, `get_account_info`, `get_all_positions`, `get_orders(status=open)`, `get_orders(status=closed, after=2026-05-28T00:00:00Z)`

Alpaca core preflight의 `first_blocking_gate=market_closed`는 after-hours 실행에서 예상되는 정규장 closed 신호로 처리했다. 같은 preflight의 account, positions, open orders, asset, quote, spread rows를 after-hours-required rows로 사용했다.

## Gate 결과

- Paper mode: PASS
- Regular market not open: PASS
- Alpaca core: PASS, 정규장 `market_closed`는 after-hours에서 비차단 처리
- Account: PASS, `ACTIVE`, portfolio value `101023.45`, buying power `135820.16`
- Open US equity orders: PASS, fresh Alpaca MCP `[]`
- Universe strict: PASS, 62개 metadata universe와 `SPY`, `QQQ` 포함
- MCP strict: PASS, SEC EDGAR/FRED/Firecrawl/Yahoo Finance pass, Alpha Vantage는 `empty_response` gap
- Quote/spread: mixed, `NOK` quote/spread는 after-hours 한도 내, `QQQ`는 whole-share notional cap 초과, `INTC`는 preflight quote가 stale/wide
- Separate after-hours order budget: FAIL
- Risk policy: PASS for empty no-submit plan

첫 차단 gate는 `separate_after_hours_order_budget`이다. Alpaca MCP closed-order reconciliation에서 같은 after-hours session의 체결 주문 `ah-20260528-1311-intc-buy-01`, `ah-20260528-1351-nok-buy-01`을 확인했다. 따라서 `risk_inputs.after_hours_new_orders_submitted_today=2`, `after_hours_policy.max_new_orders_per_session=2` 상태라 신규 주문을 제출하지 않았다.

## 후보와 판단

| Symbol | 판단 | 이유 |
| --- | --- | --- |
| QQQ | skip | 1주 주문 notional이 after-hours validation cap을 초과 |
| NOK | skip | 동일 after-hours session에 이미 validation fill 존재, session budget 소진 |
| INTC | skip | 동일 after-hours session에 이미 validation fill 존재, quote/spread evidence도 제출 기준 미흡, session budget 소진 |

## 제출 및 조정

`place_stock_order` 호출 없음. 제출 시도도 없었으므로 `client_order_id` 기준 재시도 또는 reconciliation 대상은 없다. After-hours order plan은 `market.session=after_hours`, 빈 `orders`, `risk_inputs.after_hours_new_orders_submitted_today=2`로 기록했다.

## 검증

- Order plan: `wiki/trade-ledger/orders/2026-05-28-2131-after-hours-autopilot.json`
- Run manifest: `wiki/evidence-store/run-manifests/2026-05-28-2131-after-hours-autopilot.json`
- Risk validator: `scripts/check-risk-policy.py --json`
- Universe coverage validator: `scripts/check-universe-coverage.py --strict --json`
- MCP coverage validator: `scripts/check-mcp-coverage.py --strict --json`
