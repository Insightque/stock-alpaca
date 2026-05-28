# 2026-05-28 14:31 KST After-Hours Autopilot

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Session: `after_hours`
- Artifact tag: `after-hours`
- Review bucket: `after_hours_validation`
- Paper mode: `ALPACA_PAPER_TRADE=true`

## 요약

이번 장외 scheduled paper autopilot은 주문을 제출하지 않았다. Alpaca MCP clock은 `2026-05-28T01:32:44.745431459-04:00` 기준 정규장이 닫혀 있음을 확인했다. 장외 workflow에서는 `market_closed`가 예상 상태라 단독 차단 사유가 아니지만, 별도 장외 주문 예산이 이미 소진되어 신규 검증 주문이 허용되지 않았다.

## 사용한 원천

- Alpaca core preflight: `wiki/evidence-store/sources/2026-05-28-1431-after-hours-autopilot-alpaca-core-preflight.json`
- Research MCP preflight: `wiki/evidence-store/sources/2026-05-28-1431-after-hours-autopilot-research-mcp-preflight.json`
- Fresh Alpaca MCP calls: `get_clock`, `get_account_info`, `get_all_positions`, `get_orders`, `get_stock_latest_quote`
- Order plan: `wiki/trade-ledger/orders/2026-05-28-1431-after-hours-autopilot.json`
- Manifest: `wiki/evidence-store/run-manifests/2026-05-28-1431-after-hours-autopilot.json`

## 게이트 결과

- Paper mode: PASS
- Alpaca regular market closed: PASS for after-hours workflow
- Alpaca core MCP: PASS. Scheduler preflight의 `first_blocking_gate=market_closed`는 장외 workflow에서 expected non-blocking으로 처리했다.
- Open orders: PASS. Fresh Alpaca MCP `get_orders(status=open, asset_class=us_equity)` 결과 미체결 US equity 주문 0건.
- Universe strict: PASS. Metadata universe 62개와 SPY/QQQ benchmark 포함.
- MCP strict: PASS. SEC EDGAR/FRED/Firecrawl/Yahoo Finance pass, Alpha Vantage는 `empty_response` gap이나 최소 research confirmation 기준은 충족.
- Separate after-hours order budget: FAIL. `risk_inputs.after_hours_new_orders_submitted_today=2`, `after_hours_policy.max_new_orders_per_session=2`.
- Risk policy validation: FAIL. `python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-05-28-1431-after-hours-autopilot.json` 실행 결과 현재 Python 환경에 PyYAML이 없어 validator가 정책 파일을 로드하지 못했다.

## 주문 판단

신규 주문 없음. `place_stock_order` 호출 없음. 제출 시도가 없었으므로 `client_order_id` reconciliation도 필요하지 않았다.

Shortlist 판단:

- QQQ: whole-share notional이 장외 per-order validation cap보다 커서 제외.
- NOK: 이번 장외 session에서 이미 `ah-20260528-1351-nok-buy-01` 1주 체결, 예산 소진으로 제외.
- INTC: 이번 장외 session에서 이미 `ah-20260528-1311-intc-buy-01` 1주 체결, 예산 소진으로 제외.

## 후속

INTC와 NOK 장외 validation fill은 계속 `after_hours_validation` bucket에서 next_regular_open, 1D, 5D, 20D 회고 대상으로 유지한다. 이번 run은 신규 체결이 없으므로 추가 회고 대상은 생성하지 않았다.
