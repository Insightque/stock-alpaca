# 2026-05-30 07:11 after-hours-autopilot

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Run ID: `2026-05-30-0711-after-hours-autopilot`
- Session: `after_hours`
- Policy profile: `after_hours_policy`
- Artifact tag: `after-hours`
- Review bucket: `after_hours_validation`
- Paper mode: `ALPACA_PAPER_TRADE=true`

## 결과

주문 없음. Alpaca regular market은 닫혀 있어 after-hours workflow 조건에는 맞았지만, submit 직전 필수 조건인 fresh quote gate가 실패했다. 따라서 `place_stock_order`를 호출하지 않았고, `client_order_id`도 생성하지 않았다.

## 사용한 증거

- Scheduler Alpaca core preflight: `wiki/evidence-store/sources/2026-05-30-0711-after-hours-autopilot-alpaca-core-preflight.json`
- Scheduler research MCP preflight: `wiki/evidence-store/sources/2026-05-30-0711-after-hours-autopilot-research-mcp-preflight.json`
- Runtime Alpaca MCP spot check: `wiki/evidence-store/sources/2026-05-30-0711-after-hours-autopilot-runtime-alpaca-spot-check.json`
- Order plan: `wiki/trade-ledger/orders/2026-05-30-0711-after-hours-autopilot.json`
- Run manifest: `wiki/evidence-store/run-manifests/2026-05-30-0711-after-hours-autopilot.json`

## Gate 요약

- Paper mode: PASS
- Regular market not open: PASS
- Alpaca core evidence: PASS. `first_blocking_gate=market_closed`는 after-hours run에서 expected/nonblocking으로 처리했다.
- Universe strict: PASS
- MCP strict: PASS
- Separate after-hours budget: PASS, `risk_inputs.after_hours_new_orders_submitted_today=0`
- Risk policy: PASS, empty order plan warning only
- Fresh quote: FAIL
- Spread: MIXED
- First blocking gate: `fresh_quote`

## 후보 판단

Scheduler research shortlist는 `QQQ`, `NOK`, `AVGO`, `NVDA`, `COST`, `FCX`, `UNH`, `SBUX`였다. Runtime Alpaca MCP overnight quote 확인 기준으로 모든 후보의 quote timestamp가 `2026-05-29T08:00:00Z` 부근이어서, `after_hours_policy.max_quote_age_minutes_submit=5.0`를 크게 초과했다.

- `QQQ`: spread는 통과했지만 quote freshness 실패 및 1주 notional cap 초과.
- `NOK`: quote freshness와 spread 실패, 기존 NOK exposure와 최근 lifecycle 약세.
- `AVGO`: quote freshness와 spread 실패, AI semiconductor concentration 압력.
- `NVDA`: spread는 통과했지만 quote freshness 실패 및 AI semiconductor concentration 압력.
- `COST`: quote freshness와 spread 실패, 1주 notional cap 초과.
- `FCX`: quote freshness와 spread 실패, 기존 validation exposure.
- `UNH`: quote freshness와 spread 실패, 기존 healthcare exposure.
- `SBUX`: quote freshness와 spread 실패, maintained thesis evidence 부족.

## 검증

- `PATH=/usr/local/bin:$PATH python3 scripts/check-universe-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-05-30-0711-after-hours-autopilot.json`: PASS
- `PATH=/usr/local/bin:$PATH python3 scripts/check-mcp-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-05-30-0711-after-hours-autopilot.json`: PASS
- `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-05-30-0711-after-hours-autopilot.json`: PASS with `orders is empty`

## 제출/조정

- `place_stock_order`: 호출 안 함
- `client_order_id`: 없음
- Reconcile by `client_order_id`: submit attempt가 없어 해당 없음
- Post-trade snapshot: 신규 주문이 없어 별도 post-trade position artifact는 만들지 않음
