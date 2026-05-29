# 2026-05-29-2011-after-hours-autopilot

## 요약

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Session: `after_hours`
- Policy profile: `after_hours_policy`
- Artifact tag: `after-hours`
- Review bucket: `after_hours_validation`
- Paper mode: `ALPACA_PAPER_TRADE=true` 확인
- 주문 제출: 없음

## 게이트 결과

| Gate | Status | 근거 |
|---|---:|---|
| Paper mode | PASS | 환경 변수 `ALPACA_PAPER_TRADE=true` |
| Regular market not open | PASS | Alpaca MCP clock `is_open=false`, `timestamp=2026-05-29T07:12:48.526339982-04:00` |
| Alpaca core | PASS | scheduler preflight의 `market_closed`는 장외 expected/nonblocking, runtime MCP account/positions/open orders/assets/quotes 확인 |
| Universe strict | PASS | broad metadata universe 62개, SPY/QQQ 포함, shortlist 8개 |
| MCP strict | PASS | Alpaca core + research MCP 4개 usable/pass, Alpha Vantage provider_error gap은 정책상 core+min research pass 시 주문 단독 차단 아님 |
| Separate after-hours budget | PASS | `risk_inputs.after_hours_new_orders_submitted_today=1`, session cap 2 |
| Quote freshness | FAIL | overnight quote `quote_captured_at=2026-05-29T08:00:00Z`, live clock 기준 약 192.8분 stale, after-hours cap 5분 초과 |
| Spread | MIXED | NVDA/QQQ만 after-hours spread cap 통과, 나머지 후보는 초과 |
| Risk policy | PASS | empty order plan 기준 `scripts/check-risk-policy.py --json` 통과, warning: orders empty |

## 후보 판단

| Symbol | Quote age min | Spread % | Decision | Reason |
|---|---:|---:|---|---|
| NOK | 192.8 | 6.4052 | skip | quote freshness and spread failed; thesis blocks new chase/add after prior weak add and overheat guard. |
| NVDA | 192.8 | 0.0743 | skip | quote freshness failed; AI semiconductor concentration remains too high for an after-hours validation add. |
| XOM | 192.8 | 4.3300 | skip | quote freshness and spread failed; no fresh additional-buy thesis for adding energy exposure after-hours. |
| ADBE | 192.8 | 9.9339 | skip | quote freshness and spread failed; same after-hours session already has an ADBE validation fill, so duplicate-session rule blocks add. |
| LIN | 192.8 | 1.4081 | skip | quote freshness and spread failed; LIN ticker thesis page is missing. |
| QQQ | 192.8 | 0.2025 | skip | quote freshness failed; 1-share notional exceeds after-hours per-order validation cap. |
| SPY | 192.8 | 0.4981 | skip | quote freshness and spread failed; 1-share notional exceeds after-hours per-order validation cap. |
| SMH | 192.8 | 4.1277 | skip | quote freshness and spread failed; 1-share notional exceeds after-hours per-order validation cap. |

## 제출 및 사후 확인

Quote freshness gate가 실패했으므로 `place_stock_order` 호출 전 pre-submit 단계까지 가지 않았다. 새 `client_order_id`는 생성하지 않았고, reconcile 대상도 없다.

## 산출물

- Manifest: `wiki/evidence-store/run-manifests/2026-05-29-2011-after-hours-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-05-29-2011-after-hours-autopilot.json`
- Runtime Alpaca source: `wiki/evidence-store/sources/2026-05-29-2011-after-hours-autopilot-runtime-alpaca-spot-check.json`
- Scheduler Alpaca preflight: `wiki/evidence-store/sources/2026-05-29-2011-after-hours-autopilot-alpaca-core-preflight.json`
- Scheduler research preflight: `wiki/evidence-store/sources/2026-05-29-2011-after-hours-autopilot-research-mcp-preflight.json`
