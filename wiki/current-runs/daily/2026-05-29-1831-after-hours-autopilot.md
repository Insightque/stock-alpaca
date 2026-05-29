# 2026-05-29 18:31 KST after-hours autopilot

## 실행 요약

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Run ID: `2026-05-29-1831-after-hours-autopilot`
- Session: `after_hours`
- Policy profile: `after_hours_policy`
- Artifact tag: `after-hours`
- Review bucket: `after_hours_validation`
- Mode: `submit`
- 결과: 신규 주문 없음

## 핵심 게이트

- Paper mode: PASS. `ALPACA_PAPER_TRADE=true`.
- Regular market not open: PASS. Alpaca MCP clock는 `2026-05-29T05:32:19.733953309-04:00` 기준 `is_open=false`.
- Alpaca core: PASS. Scheduler-owned Alpaca core preflight에서 `first_blocking_gate=market_closed`가 있었지만 after-hours workflow에서는 예상된 비차단 상태로 처리했다. Account, positions, open orders, assets, quotes, spreads, recent activities rows는 usable이었다.
- Runtime Alpaca MCP spot checks: account ACTIVE, positions 32 symbols, `QQQ,NOK,SMH,SPY,NVDA,ADBE,LIN,XOM` overnight quote/snapshot feed checked. Runtime open-order query는 safety wrapper가 cancelled 처리해서 scheduler preflight의 passing open-order row `[]`를 사용했다.
- Universe strict: PASS. Broad metadata universe 62 symbols screened, `SPY`와 `QQQ` 포함.
- MCP strict: PASS. Alpaca core와 research MCP minimum은 충족했다. Alpha Vantage는 provider_error circuit breaker gap이지만 SEC EDGAR/FRED/Firecrawl/Yahoo confirmations가 3개 이상이다.
- Separate after-hours budget: PASS. `risk_inputs.after_hours_new_orders_submitted_today=1`, policy cap `max_new_orders_per_session=2`. Regular validation order count는 사용하지 않았다.
- Quote freshness: FAIL. Overnight quote timestamps are around `2026-05-29T08:00:00Z`, about 92.32 minutes old at the live clock check, exceeding the 5 minute after-hours submit cap.
- Risk gate: PASS after validation. Empty order plan risk validator returned only `orders is empty` warning.

## 후보 판단

| Symbol | Quote age min | Spread % | 판단 | 사유 |
| --- | ---: | ---: | --- | --- |
| NOK | 92.32 | 6.4052 | skip | quote freshness and spread failed; thesis also blocks new chase/add after prior weak add and overheat guard. |
| NVDA | 92.32 | 0.0743 | skip | quote freshness failed; AI semiconductor concentration remains too high for an after-hours validation add. |
| XOM | 92.32 | 4.3300 | skip | quote freshness and spread failed; no fresh additional-buy thesis for adding energy exposure after-hours. |
| ADBE | 92.32 | 9.9339 | skip | quote freshness and spread failed; same after-hours session already has an ADBE validation fill, so duplicate-session rule blocks add. |
| LIN | 92.32 | 1.4081 | skip | quote freshness and spread failed; LIN ticker thesis page is missing. |
| QQQ | 92.32 | 0.2025 | skip | quote freshness failed; 1-share notional exceeds after-hours per-order validation cap. |
| SPY | 92.32 | 0.4981 | skip | quote freshness and spread failed; 1-share notional exceeds after-hours per-order validation cap. |
| SMH | 92.32 | 4.1277 | skip | quote freshness and spread failed; 1-share notional exceeds after-hours per-order validation cap. |

## 주문 및 reconcile

- `place_stock_order` 호출 없음.
- 신규 `client_order_id` 없음.
- 제출 시도가 없었으므로 reconcile은 `not_applicable_no_submit`.
- 모든 order plan tag는 `market.session=after_hours`로 유지했고, order array가 비어 있어 `extended_hours=true` 주문 생성 대상은 없었다.

## 산출물

- Manifest: `wiki/evidence-store/run-manifests/2026-05-29-1831-after-hours-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-05-29-1831-after-hours-autopilot.json`
- Runtime Alpaca MCP spot check source: `wiki/evidence-store/sources/2026-05-29-1831-after-hours-autopilot-runtime-alpaca-spot-check.json`
- Alpaca core preflight: `wiki/evidence-store/sources/2026-05-29-1831-after-hours-autopilot-alpaca-core-preflight.json`
- Research MCP preflight: `wiki/evidence-store/sources/2026-05-29-1831-after-hours-autopilot-research-mcp-preflight.json`

## 검증

- `python3 scripts/check-universe-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-05-29-1831-after-hours-autopilot.json`: PASS
- `python3 scripts/check-mcp-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-05-29-1831-after-hours-autopilot.json`: PASS
- `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-05-29-1831-after-hours-autopilot.json`: PASS with `orders is empty` warning
