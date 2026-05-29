# 2026-05-29-1911-after-hours-autopilot

## 실행 요약

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Session: `after_hours`
- Policy profile: `after_hours_policy`
- Artifact tag: `after-hours`
- Review bucket: `after_hours_validation`
- Paper mode: `ALPACA_PAPER_TRADE=true` 확인
- Submit result: 주문 없음

## 게이트 결과

- Alpaca regular market: 닫힘. Fresh MCP clock `2026-05-29T06:12:12.370378168-04:00` 기준 `is_open=false`; 정규장 개장 중이 아니므로 after-hours workflow 진행 가능.
- Alpaca core: PASS. Scheduler preflight의 `first_blocking_gate=market_closed`는 장외 workflow에서 예상된 비차단 상태이며, fresh Alpaca MCP로 account ACTIVE, open US equity orders `[]`, positions 32개, candidate asset active/tradable, overnight quote rows를 확인.
- Research MCP: PASS for submit minimum. SEC EDGAR, FRED, Firecrawl, Yahoo Finance rows are usable/pass; Alpha Vantage는 provider rate-limit circuit breaker gap으로 기록.
- Universe strict: PASS. Broad metadata universe 62 symbols, SPY/QQQ 포함, shortlist 8 symbols.
- Separate after-hours budget: PASS. `risk_inputs.after_hours_new_orders_submitted_today=1`; regular validation count는 재사용하지 않음.
- Quote freshness: FAIL. QQQ/NOK/SMH/SPY/NVDA/ADBE/LIN/XOM overnight quote timestamp가 대체로 `2026-05-29T08:00:00Z`이고 fresh clock 기준 약 132.2분 경과해 `after_hours_policy.max_quote_age_minutes_submit=5.0`을 초과.
- Spread gate: MIXED. NVDA와 QQQ는 spread cap 이내지만 quote freshness 실패. NOK/XOM/ADBE/LIN/SPY/SMH는 spread 또는 notional/thesis 제약도 동반.
- Risk gate: PASS. `scripts/check-risk-policy.py --json` 검증 결과 empty order plan 경고만 발생했고 오류는 없음.

## 후보 판단

| Symbol | Decision | 핵심 사유 |
| --- | --- | --- |
| NOK | skip | quote stale, spread 6.4052%, thesis/overheat guard |
| NVDA | skip | quote stale, AI semiconductor concentration |
| XOM | skip | quote stale, spread 4.33%, fresh add thesis 부족 |
| ADBE | skip | quote stale, spread 9.9339%, same-session duplicate after prior ADBE fill |
| LIN | skip | quote stale, spread 1.4081%, ticker thesis page missing |
| QQQ | skip | quote stale, 1-share notional exceeds after-hours cap |
| SPY | skip | quote stale, spread 0.4981%, 1-share notional exceeds after-hours cap |
| SMH | skip | quote stale, spread 4.1277%, 1-share notional exceeds after-hours cap |

## Submit/Reconcile

No `place_stock_order` call was made. No new `client_order_id` was created, so no post-submit reconciliation was required. Prior same-session ADBE after-hours fill remains counted only in the separate after-hours budget.

## Artifacts

- Manifest: `wiki/evidence-store/run-manifests/2026-05-29-1911-after-hours-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-05-29-1911-after-hours-autopilot.json`
- Runtime spot check: `wiki/evidence-store/sources/2026-05-29-1911-after-hours-autopilot-runtime-alpaca-spot-check.json`
- Alpaca preflight: `wiki/evidence-store/sources/2026-05-29-1911-after-hours-autopilot-alpaca-core-preflight.json`
- Research preflight: `wiki/evidence-store/sources/2026-05-29-1911-after-hours-autopilot-research-mcp-preflight.json`

## Validators

- `python3 scripts/check-universe-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-05-29-1911-after-hours-autopilot.json`: PASS
- `python3 scripts/check-mcp-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-05-29-1911-after-hours-autopilot.json`: PASS
- `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-05-29-1911-after-hours-autopilot.json`: PASS (`orders is empty` warning)
