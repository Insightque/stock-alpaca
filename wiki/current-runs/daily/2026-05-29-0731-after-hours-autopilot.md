# 2026-05-29 07:31 KST after-hours autopilot

## 요약

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Session: `after_hours`
- Artifact tag: `after-hours`
- Review bucket: `after_hours_validation`
- Mode: `submit`, paper only
- Result: 주문 없음

`ALPACA_PAPER_TRADE=true`를 확인했다. Fresh Alpaca MCP clock 기준 정규장은 `2026-05-28T18:32:59.532715570-04:00`에 닫혀 있었고, after-hours workflow의 "정규장 open이면 제출 금지" 조건과 충돌하지 않았다.

## 사용한 소스

- Scheduler Alpaca core preflight: `wiki/evidence-store/sources/2026-05-29-0731-after-hours-autopilot-alpaca-core-preflight.json`
- Scheduler research MCP preflight: `wiki/evidence-store/sources/2026-05-29-0731-after-hours-autopilot-research-mcp-preflight.json`
- Fresh Alpaca MCP spot checks: `get_clock`, `get_account_info`, `get_all_positions`, `get_orders(status=open)`, `get_orders(status=all, after=2026-05-28T20:00:00Z)`, `get_stock_latest_quote(feed=overnight)`, `get_stock_snapshot(feed=overnight)`, `get_asset(QQQ/NOK/SMH)`

Alpaca core preflight의 `first_blocking_gate=market_closed`는 after-hours 실행에서 예상되는 정규장 closed 신호로 비차단 처리했다. 같은 preflight의 account, positions, open orders, asset, quote, spread rows와 fresh Alpaca MCP spot checks를 함께 사용했다.

## Gate 결과

- Paper mode: PASS
- Regular market not open: PASS
- Alpaca core: PASS, 정규장 `market_closed`는 after-hours에서 비차단 처리
- Account: PASS, fresh Alpaca MCP `ACTIVE`, portfolio value `102335.17`, buying power `133303.84`
- Open US equity orders: PASS, fresh Alpaca MCP `[]`
- Same after-hours session orders: PASS, fresh Alpaca MCP `[]` after `2026-05-28T20:00:00Z`
- Universe strict: PASS, 62개 metadata universe와 `SPY`, `QQQ` 포함
- MCP strict: PASS, SEC EDGAR/FRED/Firecrawl/Yahoo Finance pass, Alpha Vantage는 `empty_response` gap
- Separate after-hours order budget: PASS, `risk_inputs.after_hours_new_orders_submitted_today=0`
- Quote freshness: FAIL
- Spread within after-hours policy: MIXED, scheduler preflight 기준 QQQ만 spread 통과, NOK와 나머지 shortlist는 after-hours cap 초과
- Risk policy: PASS for empty no-submit plan

첫 차단 gate는 `fresh_quote`이다. Scheduler IEX preflight의 shortlist quote timestamp도 after-hours submit limit인 5분을 넘었고, fresh Alpaca MCP overnight quote는 `2026-05-28T08:00:00Z` 부근의 오래된 행만 반환했다.

## 후보와 판단

| Symbol | 판단 | 이유 |
| --- | --- | --- |
| QQQ | skip | quote freshness gate 실패. Scheduler IEX spread는 통과했지만 timestamp `2026-05-28T20:44:11.568144727Z`로 stale이고 fresh overnight quote도 stale |
| NOK | skip | quote freshness gate 실패, scheduler spread 약 `0.65%`로 after-hours cap 초과 |
| SPY | skip | quote freshness gate 실패, scheduler spread 약 `6.01%`, fresh overnight spread 약 `0.32%`, 1주 notional이 after-hours validation cap 초과 |
| SMH/NVDA/ADBE/LIN/XOM | skip | quote freshness/spread 또는 포트폴리오 fit 기준에서 최종 주문 후보 제외 |

## 제출 및 조정

`place_stock_order` 호출 없음. 제출 시도도 없었으므로 새 `client_order_id` 기준 reconciliation 대상은 없다. After-hours order plan은 `market.session=after_hours`, 빈 `orders`, `risk_inputs.after_hours_new_orders_submitted_today=0`로 기록했다.

## 검증

- Order plan: `wiki/trade-ledger/orders/2026-05-29-0731-after-hours-autopilot.json`
- Run manifest: `wiki/evidence-store/run-manifests/2026-05-29-0731-after-hours-autopilot.json`
- Risk validator: `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json ...` PASS, warning `orders is empty`
- Universe coverage validator: `python3 scripts/check-universe-coverage.py --strict --json ...` PASS
- MCP coverage validator: `python3 scripts/check-mcp-coverage.py --strict --json ...` PASS
