# 2026-05-28 21:51 KST after-hours autopilot

## 요약

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Session: `after_hours`
- Artifact tag: `after-hours`
- Review bucket: `after_hours_validation`
- Mode: `submit`, paper only
- Result: 주문 없음

`ALPACA_PAPER_TRADE=true`를 확인했다. Scheduler-owned Alpaca core preflight 기준 Alpaca 정규장은 `2026-05-28T08:51:13.205464921-04:00`에 닫혀 있었고, after-hours workflow의 "정규장 open이면 제출 금지" 조건과 충돌하지 않았다.

## 사용한 소스

- Scheduler Alpaca core preflight: `wiki/evidence-store/sources/2026-05-28-2151-after-hours-autopilot-alpaca-core-preflight.json`
- Scheduler research MCP preflight: `wiki/evidence-store/sources/2026-05-28-2151-after-hours-autopilot-research-mcp-preflight.json`
- Fresh Alpaca MCP spot checks: `get_all_positions`, `get_orders(status=open)`, `get_stock_latest_quote`, `get_stock_snapshot`, `get_order_by_client_id`

Alpaca core preflight의 `first_blocking_gate=market_closed`는 after-hours 실행에서 예상되는 정규장 closed 신호로 비차단 처리했다. Fresh `get_clock`와 `get_account_info` 호출은 런타임에서 취소되어 같은 preflight의 passing clock/account rows를 사용했다.

## Gate 결과

- Paper mode: PASS
- Regular market not open: PASS
- Alpaca core: PASS, 정규장 `market_closed`는 after-hours에서 비차단 처리
- Account: PASS, `ACTIVE`, portfolio value `101208.9`, buying power `135973.45`
- Open US equity orders: PASS, fresh Alpaca MCP `[]`
- Universe strict: PASS, 62개 metadata universe와 `SPY`, `QQQ` 포함
- MCP strict: PASS, SEC EDGAR/FRED/Firecrawl/Yahoo Finance pass, Alpha Vantage는 `empty_response` gap
- Quote/spread: mixed, 일부 후보는 fresh quote가 오래되었거나 spread가 넓고, `SPY`/`QQQ`는 whole-share notional cap 초과
- Separate after-hours order budget: FAIL
- Risk policy: PASS for empty no-submit plan

첫 차단 gate는 `separate_after_hours_order_budget`이다. Alpaca MCP `get_order_by_client_id`로 같은 after-hours session의 체결 주문 `ah-20260528-1311-intc-buy-01`, `ah-20260528-1351-nok-buy-01`을 확인했다. 따라서 `risk_inputs.after_hours_new_orders_submitted_today=2`, `after_hours_policy.max_new_orders_per_session=2` 상태라 신규 주문을 제출하지 않았다.

## 후보와 판단

| Symbol | 판단 | 이유 |
| --- | --- | --- |
| SPY | skip | 1주 주문 notional이 after-hours validation cap을 초과 |
| QQQ | skip | 1주 주문 notional이 after-hours validation cap을 초과 |
| NOK | skip | 동일 after-hours session에 이미 validation fill 존재, session budget 소진 |

## 제출 및 조정

`place_stock_order` 호출 없음. 제출 시도도 없었으므로 새 `client_order_id` 기준 reconciliation 대상은 없다. After-hours order plan은 `market.session=after_hours`, 빈 `orders`, `risk_inputs.after_hours_new_orders_submitted_today=2`로 기록했다.

## 검증

- Order plan: `wiki/trade-ledger/orders/2026-05-28-2151-after-hours-autopilot.json`
- Run manifest: `wiki/evidence-store/run-manifests/2026-05-28-2151-after-hours-autopilot.json`
- Risk validator: `scripts/check-risk-policy.py --json` PASS, warning `orders is empty`
- Universe coverage validator: `scripts/check-universe-coverage.py --strict --json` PASS
- MCP coverage validator: `scripts/check-mcp-coverage.py --strict --json` PASS
