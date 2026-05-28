# 2026-05-28 19:11 KST after-hours autopilot

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Session: `after_hours`
- Artifact tag: `after-hours`
- Review bucket: `after_hours_validation`
- Policy profile: `after_hours_policy`
- Paper mode: `ALPACA_PAPER_TRADE=true`

## 결과

주문 제출 없음. Scheduler-owned Alpaca core preflight 기준 regular market clock은 `2026-05-28T06:11:15.433854061-04:00`에 `is_open=false`였고, after-hours workflow에서는 `first_blocking_gate=market_closed`를 예상된 비차단 상태로 처리했다.

차단 사유는 별도 장외 주문 예산이다. `risk_inputs.after_hours_new_orders_submitted_today=2`이고 `after_hours_policy.max_new_orders_per_session=2`이므로 신규 장외 validation 주문은 제출하지 않았다.

## Gate

- Alpaca paper mode: PASS
- Regular market closed: PASS
- Alpaca core MCP: PASS for after-hours-required rows; scheduler preflight의 `market_closed`는 expected non-blocking
- Fresh Alpaca MCP spot checks: account ACTIVE, positions fetched, open US equity orders empty, prior `ah-20260528-1311-intc-buy-01` and `ah-20260528-1351-nok-buy-01` reconciled as filled
- Universe strict: PASS
- MCP strict: PASS; SEC EDGAR, FRED, Firecrawl, Yahoo Finance pass, Alpha Vantage는 `empty_response` gap
- Quote/spread: PASS from scheduler-owned Alpaca core preflight; fresh IEX quote spot-check was stale and not used for submit eligibility
- Separate after-hours budget: FAIL, 2/2
- Risk policy: PASS for empty no-submit plan, warning `orders is empty`
- Universe coverage validator: PASS, 62 symbols screened with SPY/QQQ benchmarks
- MCP coverage validator: PASS, four positive research confirmations

## Artifacts

- Order plan: `wiki/trade-ledger/orders/2026-05-28-1911-after-hours-autopilot.json`
- Manifest: `wiki/evidence-store/run-manifests/2026-05-28-1911-after-hours-autopilot.json`
- Alpaca core preflight: `wiki/evidence-store/sources/2026-05-28-1911-after-hours-autopilot-alpaca-core-preflight.json`
- Research MCP preflight: `wiki/evidence-store/sources/2026-05-28-1911-after-hours-autopilot-research-mcp-preflight.json`

## Submit/Reconcile

No `place_stock_order` call was made. No submit attempt means no new `client_order_id` reconciliation was required.
