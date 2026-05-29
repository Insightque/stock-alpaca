# 2026-05-29 16:31 KST after-hours autopilot

## 실행 요약

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Run ID: `2026-05-29-1631-after-hours-autopilot`
- Session: `after_hours`
- Policy profile: `after_hours_policy`
- Artifact tag: `after-hours`
- Review bucket: `after_hours_validation`
- Mode: `submit`
- 결과: 신규 주문 없음

## 핵심 게이트

- Paper mode: PASS. `ALPACA_PAPER_TRADE=true`.
- Regular market not open: PASS. Alpaca MCP clock는 `2026-05-29T03:32:29.393189573-04:00` 기준 `is_open=false`.
- Alpaca core: PASS. Scheduler-owned Alpaca core preflight에서 account/positions/open orders/assets/quotes/spreads가 usable이었다. `first_blocking_gate=market_closed`는 after-hours workflow에서 예상된 비차단 상태로 처리했다.
- Runtime Alpaca MCP spot checks: account ACTIVE, positions 32 symbols, NOK/NVDA assets active/tradable, overnight quote feed checked for `QQQ,NOK,SMH,SPY,NVDA,ADBE,LIN,XOM`. Runtime open-order query는 safety wrapper가 cancel했으므로 scheduler preflight의 passing open-order row `[]`를 사용했다.
- Universe strict: PASS. Broad metadata universe 62 symbols screened, `SPY`와 `QQQ` 포함.
- MCP strict: PASS. Alpaca core와 research MCP minimum은 충족했다. Alpha Vantage는 daily rate-limit circuit breaker로 provider gap이지만 SEC EDGAR/FRED/Firecrawl/Yahoo confirmations가 3개 이상이다.
- Separate after-hours budget: PASS. `risk_inputs.after_hours_new_orders_submitted_today=1`, policy cap `max_new_orders_per_session=2`.
- Risk gate: PASS for empty order plan after validator run.

## 후보 판단

| Symbol | Quote | Spread % | 판단 | 사유 |
| --- | ---: | ---: | --- | --- |
| NOK | fresh | 0.1318 | skip | quote/spread는 통과했지만 thesis가 overheat guard와 이전 add 약세 때문에 신규 추격을 막는다. |
| NVDA | fresh | 0.0511 | skip | quote/spread는 통과했지만 기존 AI semiconductor concentration을 after-hours validation에서 추가하지 않는다. |
| XOM | stale | 0.1842 | skip | overnight quote가 after_hours_policy.max_quote_age_minutes_submit 5분을 초과했고 fresh additional-buy thesis도 없다. |
| ADBE | fresh | 0.3495 | skip | 같은 after-hours session에서 ADBE validation fill이 이미 있고 runtime spread도 after-hours 0.25% cap을 넘었다. |
| LIN | fresh | 0.2233 | skip | 이번 runtime quote/spread와 1주 notional은 통과했지만 LIN ticker thesis page가 없어 after-hours submit 전 thesis evidence gate를 통과하지 못했다. |
| QQQ | fresh | 0.1386 | skip | quote/spread는 통과했지만 1주 notional이 after-hours per-order validation cap을 초과한다. |
| SPY | fresh | 0.0066 | skip | quote/spread는 통과했지만 1주 notional이 after-hours per-order validation cap을 초과한다. |
| SMH | fresh | 0.2739 | skip | 1주 notional이 after-hours per-order validation cap을 초과하고 spread도 after-hours 0.25% cap을 넘었다. |

## 주문 및 reconcile

- `place_stock_order` 호출 없음.
- 신규 `client_order_id` 없음.
- 제출 시도가 없었으므로 reconcile은 `not_applicable_no_submit`.
- 모든 order plan tag는 `market.session=after_hours`로 유지했고, order array가 비어 있어 `extended_hours=true` 주문 생성 대상은 없었다.

## 산출물

- Manifest: `wiki/evidence-store/run-manifests/2026-05-29-1631-after-hours-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-05-29-1631-after-hours-autopilot.json`
- Runtime Alpaca MCP spot check source: `wiki/evidence-store/sources/2026-05-29-1631-after-hours-autopilot-runtime-alpaca-spot-check.json`
- Alpaca core preflight: `wiki/evidence-store/sources/2026-05-29-1631-after-hours-autopilot-alpaca-core-preflight.json`
- Research MCP preflight: `wiki/evidence-store/sources/2026-05-29-1631-after-hours-autopilot-research-mcp-preflight.json`

## 검증

- `python3 scripts/check-universe-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-05-29-1631-after-hours-autopilot.json`: PASS
- `python3 scripts/check-mcp-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-05-29-1631-after-hours-autopilot.json`: PASS
- `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-05-29-1631-after-hours-autopilot.json`: PASS
