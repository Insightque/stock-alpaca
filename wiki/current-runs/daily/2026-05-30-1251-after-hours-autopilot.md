# 2026-05-30-1251-after-hours-autopilot

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Run ID: `2026-05-30-1251-after-hours-autopilot`
- Session: `after_hours`
- Policy profile: `after_hours_policy`
- Artifact tag: `after-hours`
- Review bucket: `after_hours_validation`
- Paper mode: `ALPACA_PAPER_TRADE=true` 확인

## 게이트 요약

- Regular market: Alpaca scheduler preflight 기준 `is_open=false`. `first_blocking_gate=market_closed`는 after-hours workflow에서 예상 상태이므로 단독 차단 사유로 처리하지 않았다.
- Alpaca core: scheduler-owned preflight의 account/positions/open orders/assets/quotes rows를 사용했다. Runtime Alpaca MCP는 open US-equity orders `[]`와 QQQ active/tradable/overnight_tradable을 확인했으며, 일부 read-only spot check는 tool safety layer에서 취소되어 scheduler row를 유지했다.
- Universe gate: broad metadata universe 62개와 `SPY`/`QQQ` benchmark 포함. strict validator 결과는 아래 검증 섹션에 기록했다.
- MCP gate: Alpaca core + research preflight 사용. Alpha Vantage는 후보 뉴스 0건 gap이지만 SEC EDGAR/FRED/Firecrawl/Yahoo Finance confirmation 기준을 충족한다.
- Risk gate: `market.session=after_hours`, `orders=[]`, `risk_inputs.after_hours_new_orders_submitted_today=0`로 별도 after-hours budget을 사용했다.
- Submit gate: 사용 가능한 after-hours quote evidence가 `after_hours_policy.max_quote_age_minutes_submit=5.0`분을 초과해 stale quote로 차단했다.

## 주문/체결

- `place_stock_order` 호출 없음.
- `client_order_id` 없음.
- 제출 시도가 없어 `client_order_id` reconciliation은 해당 없음.
- 모든 planned order는 없음: `orders=[]`.

## 산출물

- Manifest: `wiki/evidence-store/run-manifests/2026-05-30-1251-after-hours-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-05-30-1251-after-hours-autopilot.json`
- Runtime Alpaca spot check: `wiki/evidence-store/sources/2026-05-30-1251-after-hours-autopilot-runtime-alpaca-spot-check.json`
- Scheduler Alpaca preflight: `wiki/evidence-store/sources/2026-05-30-1251-after-hours-autopilot-alpaca-core-preflight.json`
- Scheduler research preflight: `wiki/evidence-store/sources/2026-05-30-1251-after-hours-autopilot-research-mcp-preflight.json`

## 검증

- `python3 scripts/check-universe-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-05-30-1251-after-hours-autopilot.json`: PASS
- `python3 scripts/check-mcp-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-05-30-1251-after-hours-autopilot.json`: PASS
- `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-05-30-1251-after-hours-autopilot.json`: PASS with `orders is empty` warning
