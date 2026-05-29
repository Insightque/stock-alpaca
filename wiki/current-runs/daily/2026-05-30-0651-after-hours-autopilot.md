# 2026-05-30 06:51 KST after-hours autopilot

## 실행 요약

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Run ID: `2026-05-30-0651-after-hours-autopilot`
- Session: `after_hours`
- Policy profile: `after_hours_policy`
- Artifact tag: `after-hours`
- Review bucket: `after_hours_validation`
- Mode: `submit`
- 결과: 신규 주문 없음

## 핵심 게이트

- Paper mode: PASS. `ALPACA_PAPER_TRADE=true`.
- Regular market not open: PASS. Alpaca MCP clock는 `2026-05-29T17:53:04.898679039-04:00` 기준 `is_open=false`.
- Alpaca core: PASS. Scheduler-owned Alpaca core preflight의 `first_blocking_gate=market_closed`는 after-hours workflow에서 예상된 비차단 상태로 처리했다. Runtime Alpaca MCP spot check도 account readable, positions readable, open US equity orders `[]`, overnight quote evidence를 확인했다.
- Universe strict: PASS. Broad metadata universe 62 symbols screened, `SPY`와 `QQQ` 포함.
- MCP strict: PASS. Alpaca core와 research MCP minimum은 충족했다. Alpha Vantage는 `empty_response` gap이지만 SEC EDGAR/FRED/Firecrawl/Yahoo confirmations가 3개 이상이다.
- Separate after-hours budget: PASS. `risk_inputs.after_hours_new_orders_submitted_today=0`; regular validation order count는 사용하지 않았다.
- Quote freshness: FAIL. Overnight quote timestamps are around `2026-05-29T08:00:00Z`, about 833.08 minutes old at the live clock check, exceeding the 5 minute after-hours submit cap.
- Quote source gap: BOATS feed returned subscription-not-permitted, so it was recorded as a data gap and not used as a submit source.
- Risk gate: PASS. Empty order plan risk validator returned only `orders is empty` warning.

## 후보 판단

| Symbol | Quote age min | Spread % | 판단 | 사유 |
| --- | ---: | ---: | --- | --- |
| QQQ | 833.08 | 0.2025 | skip | quote freshness failed; 1-share notional exceeds after-hours per-order validation cap. |
| NOK | 833.07 | 6.4052 | skip | quote freshness and spread failed; prior large NOK exposure plus weak recent add/lifecycle review blocks another after-hours add. |
| AVGO | 833.07 | 3.2871 | skip | quote freshness and spread failed; AI semiconductor concentration is already near policy pressure, so no after-hours add. |
| NVDA | 833.07 | 0.0743 | skip | quote freshness failed; AI semiconductor concentration remains too high for an after-hours validation add. |
| COST | 833.07 | 24.4918 | skip | quote freshness and spread failed; 1-share notional exceeds after-hours per-order validation cap. |
| FCX | 833.07 | 7.1581 | skip | quote freshness and spread failed; existing FCX validation exposure means no duplicate after-hours add. |
| UNH | 833.07 | 1.3343 | skip | quote freshness and spread failed; existing healthcare exposure and stale quote block submit. |
| SBUX | 833.08 | 13.3915 | skip | quote freshness and spread failed; maintained ticker thesis evidence is not current enough for after-hours validation submit. |

## 주문 및 reconcile

- `place_stock_order` 호출 없음.
- 신규 `client_order_id` 없음.
- 제출 시도가 없었으므로 reconcile은 `not_applicable_no_submit`.
- Order plan은 `market.session=after_hours`로 유지했고, order array가 비어 있어 `extended_hours=true` 주문 생성 대상은 없었다.

## 산출물

- Manifest: `wiki/evidence-store/run-manifests/2026-05-30-0651-after-hours-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-05-30-0651-after-hours-autopilot.json`
- Runtime Alpaca MCP spot check source: `wiki/evidence-store/sources/2026-05-30-0651-after-hours-autopilot-runtime-alpaca-spot-check.json`
- Alpaca core preflight: `wiki/evidence-store/sources/2026-05-30-0651-after-hours-autopilot-alpaca-core-preflight.json`
- Research MCP preflight: `wiki/evidence-store/sources/2026-05-30-0651-after-hours-autopilot-research-mcp-preflight.json`

## 검증

- `python3 scripts/check-universe-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-05-30-0651-after-hours-autopilot.json`: PASS
- `python3 scripts/check-mcp-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-05-30-0651-after-hours-autopilot.json`: PASS
- `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-05-30-0651-after-hours-autopilot.json`: PASS with `orders is empty` warning
