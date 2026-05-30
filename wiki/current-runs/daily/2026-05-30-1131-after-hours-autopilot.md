# 2026-05-30-1131-after-hours-autopilot

## 요약

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Session: `after_hours`
- Policy profile: `after_hours_policy`
- Artifact tag: `after-hours`
- Review bucket: `after_hours_validation`
- 결론: 주문 없음. `fresh_quote` gate가 첫 제출 차단 사유다.

## 게이트

- Paper mode: PASS (`ALPACA_PAPER_TRADE=true` 존재 확인, 값은 기록하지 않음)
- Regular market not open: PASS. Alpaca MCP clock은 `2026-05-29T22:32:57.868871735-04:00` 기준 `is_open=false`다.
- Alpaca core: PASS for after-hours interpretation. Scheduler preflight의 `first_blocking_gate=market_closed`는 장외 workflow에서 예상된 비차단 상태로 처리했다. Scheduler account/positions/open orders/assets/quotes rows를 사용했고, runtime Alpaca MCP는 clock/account/open orders/overnight QQQ quote를 확인했다. Runtime positions/asset read는 tool safety layer가 차단해 scheduler-owned passing row를 사용했다.
- Universe strict: PASS.
- MCP strict: PASS. Alpha Vantage는 `empty_response` gap이지만 SEC EDGAR/FRED/Firecrawl/Yahoo Finance가 pass라 최소 research confirmation을 충족했다.
- Separate after-hours order budget: PASS. `risk_inputs.after_hours_new_orders_submitted_today=0`; regular validation order count를 재사용하지 않았다.
- Review backlog throttle fields: included (`pending_1d=10`, `pending_5d=32`, `pending_20d=32`). 빈 주문 계획이므로 신규 buy slot 축소는 제출로 이어지지 않았다.
- Quote freshness: FAIL. Runtime QQQ overnight quote는 `2026-05-29T08:00:00.386377592Z`이고, 다른 scheduler quote evidence도 after-hours 5분 한도를 초과했다.
- Spread: MIXED. 일부 후보는 after-hours spread 한도 이내지만 나머지는 한도 밖이거나 측정 불가다.
- Risk validator: PASS. 빈 주문 계획이므로 `orders is empty` warning만 발생했다.

## 후보 판단

| Symbol | Quote fresh | Spread pass | Decision | Reason |
| --- | --- | --- | --- | --- |
| QQQ | false | true | skip | available quote evidence exceeded after-hours 5-minute freshness cap; 1-share notional exceeds after-hours per-order validation cap. |
| NOK | false | false | skip | available quote evidence exceeded after-hours 5-minute freshness cap; spread failed or was not measurable; prior large NOK exposure blocks another after-hours add. |
| AVGO | false | false | skip | available quote evidence exceeded after-hours 5-minute freshness cap; spread failed or was not measurable; AI semiconductor concentration blocks after-hours add. |
| NVDA | false | false | skip | available quote evidence exceeded after-hours 5-minute freshness cap; spread failed or was not measurable; AI semiconductor concentration blocks after-hours add. |
| COST | false | false | skip | available quote evidence exceeded after-hours 5-minute freshness cap; spread failed or was not measurable; 1-share notional exceeds after-hours per-order validation cap. |
| FCX | false | false | skip | available quote evidence exceeded after-hours 5-minute freshness cap; spread failed or was not measurable; existing FCX validation exposure blocks duplicate add. |
| UNH | false | false | skip | available quote evidence exceeded after-hours 5-minute freshness cap; spread failed or was not measurable. |
| SBUX | false | false | skip | available quote evidence exceeded after-hours 5-minute freshness cap; spread failed or was not measurable; maintained ticker thesis evidence is not current enough for after-hours submit. |

## 주문 및 조정

`place_stock_order`는 호출하지 않았다. 따라서 `client_order_id` 조정은 해당 없음이다. 제출 가능 주문이 없었기 때문에 사전 제출 게이트 요약은 주문 직전 단계까지 도달하지 않았다.

## 산출물

- Manifest: `wiki/evidence-store/run-manifests/2026-05-30-1131-after-hours-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-05-30-1131-after-hours-autopilot.json`
- Runtime Alpaca spot check: `wiki/evidence-store/sources/2026-05-30-1131-after-hours-autopilot-runtime-alpaca-spot-check.json`
- Scheduler Alpaca preflight: `wiki/evidence-store/sources/2026-05-30-1131-after-hours-autopilot-alpaca-core-preflight.json`
- Scheduler research preflight: `wiki/evidence-store/sources/2026-05-30-1131-after-hours-autopilot-research-mcp-preflight.json`
