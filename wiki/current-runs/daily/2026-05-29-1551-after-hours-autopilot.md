# 2026-05-29 15:51 KST after-hours autopilot

## 실행 요약

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Run ID: `2026-05-29-1551-after-hours-autopilot`
- Session: `after_hours`
- Policy profile: `after_hours_policy`
- Artifact tag: `after-hours`
- Review bucket: `after_hours_validation`
- Mode: `submit`
- 결과: 신규 주문 없음

## 핵심 게이트

- Paper mode: PASS. `ALPACA_PAPER_TRADE=true`.
- Regular market not open: PASS. Alpaca MCP clock는 `2026-05-29T02:52:36.919662785-04:00` 기준 `is_open=false`.
- Alpaca core: PASS. Scheduler-owned Alpaca core preflight에서 account/positions/open orders/assets/quotes/spreads가 usable이었다. `first_blocking_gate=market_closed`는 after-hours workflow에서 예상된 비차단 상태로 처리했다.
- Runtime Alpaca MCP spot checks: account ACTIVE, open US equity orders `[]`, same-session after-hours fill은 ADBE 1건, live asset checks는 QQQ/LIN active/tradable, overnight quote feed checked for `QQQ,NOK,SMH,SPY,NVDA,ADBE,LIN,XOM`. Runtime positions spot check는 safety wrapper cancelled였으므로 scheduler preflight의 passing positions row를 사용했다.
- Universe strict: PASS. Broad metadata universe 62 symbols screened, `SPY`와 `QQQ` 포함.
- MCP strict: PASS. Alpaca core와 research MCP minimum은 충족했다. Alpha Vantage는 daily rate-limit circuit breaker로 provider gap이지만 SEC EDGAR/FRED/Firecrawl/Yahoo confirmations가 3개 이상이다.
- Separate after-hours budget: PASS. `risk_inputs.after_hours_new_orders_submitted_today=1`, policy cap `max_new_orders_per_session=2`.
- Risk gate: PASS for empty order plan after validator run.

## 후보 판단

| Symbol | Quote | Spread % | 판단 | 사유 |
| --- | ---: | ---: | --- | --- |
| NOK | fresh | 0.0648 | skip | quote/spread는 통과했지만 thesis가 overheat guard와 이전 add 약세 때문에 신규 추격을 막는다. |
| NVDA | fresh | 0.1439 | skip | quote/spread는 통과했지만 기존 AI semiconductor concentration을 after-hours validation에서 추가하지 않는다. |
| XOM | fresh | 0.1093 | skip | quote/spread는 통과했지만 약한 interim validation review 이후 fresh additional-buy thesis가 없다. |
| ADBE | fresh | 0.0493 | skip | 같은 after-hours session에서 ADBE validation fill이 이미 있어 duplicate-session을 차단한다. |
| QQQ | fresh | 0.0014 | skip | quote/spread는 통과했지만 1주 notional이 after-hours per-order validation cap을 초과한다. |
| SPY | fresh | 0.0331 | skip | quote/spread는 통과했지만 1주 notional이 after-hours per-order validation cap을 초과한다. |
| SMH | fresh | 0.1606 | skip | quote/spread는 통과했지만 1주 notional이 after-hours per-order validation cap을 초과한다. |
| LIN | stale | 1.5299 | skip | quote freshness와 spread cap을 모두 통과하지 못했다. |

## 주문 및 reconcile

- `place_stock_order` 호출 없음.
- 신규 `client_order_id` 없음.
- 제출 시도가 없었으므로 reconcile은 `not_applicable_no_submit`.
- 모든 order plan tag는 `market.session=after_hours`로 유지했고, order array가 비어 있어 `extended_hours=true` 주문 생성 대상은 없었다.

## 산출물

- Manifest: `wiki/evidence-store/run-manifests/2026-05-29-1551-after-hours-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-05-29-1551-after-hours-autopilot.json`
- Alpaca core preflight: `wiki/evidence-store/sources/2026-05-29-1551-after-hours-autopilot-alpaca-core-preflight.json`
- Research MCP preflight: `wiki/evidence-store/sources/2026-05-29-1551-after-hours-autopilot-research-mcp-preflight.json`

## 검증

- `python3 scripts/check-universe-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-05-29-1551-after-hours-autopilot.json`: PASS
- `python3 scripts/check-mcp-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-05-29-1551-after-hours-autopilot.json`: PASS
- `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-05-29-1551-after-hours-autopilot.json`: PASS with empty-orders warning
