# 2026-06-02 08:11 KST After-Hours Paper Autopilot

## 요약

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Session: `after_hours`
- Policy profile: `after_hours_policy`
- Artifact tag: `after-hours`
- Review bucket: `after_hours_validation`
- Paper mode: `ALPACA_PAPER_TRADE=true`
- 결과: 신규 주문 없음

## 게이트

- Alpaca core: scheduler-owned preflight `wiki/evidence-store/sources/2026-06-02-0811-after-hours-autopilot-alpaca-core-preflight.json` 사용. `first_blocking_gate=market_closed`는 after-hours에서 예상된 비차단 상태로 처리했고, account/positions/orders/asset/quote/spread 행은 통과 근거로 사용했다.
- Alpaca MCP runtime: account ACTIVE와 positions 32개를 확인했고, watchlist는 0개였다. `get_order_by_client_id`로 `ah-20260601-0911-nvda-buy-01` canceled/filled_qty 0, `ah-20260601-0931-avgo-buy-01` filled/filled_qty 1을 확인했다. 둘 다 `extended_hours=true`다.
- Research MCP: `wiki/evidence-store/sources/2026-06-02-0811-after-hours-autopilot-research-mcp-preflight.json` 사용. SEC EDGAR, Firecrawl, Yahoo Finance pass; Alpha Vantage는 empty_response gap, FRED는 provider_error gap. 최소 research confirmation 3개를 충족했다.
- Universe strict: broad metadata universe 62개와 SPY/QQQ 포함 조건 통과.
- Risk policy: empty order plan으로 검증 대상 생성. `market.session=after_hours`, `risk_inputs.after_hours_new_orders_submitted_today=2`를 사용했고 정규 validation order count는 재사용하지 않았다.
- Submit gate summary: 별도 장외 session budget 2건이 이미 소진되어 `place_stock_order` 호출 전 차단했다.

## 주문 및 조정

- `place_stock_order` 호출 없음.
- 새 `client_order_id` 없음.
- 대체 client order id retry 없음.
- after-hours sell은 `after_hours_policy.allowed_sides=[buy]` 밖이므로 TSLA/SO/NEE 약세 포지션은 다음 regular-session risk diagnostic queue로만 남겼다.

## 산출물

- Manifest: `wiki/evidence-store/run-manifests/2026-06-02-0811-after-hours-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-02-0811-after-hours-autopilot.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-06-02-0811-after-hours-autopilot-after-hours-gate-evaluation.json`
- Scheduler Alpaca preflight: `wiki/evidence-store/sources/2026-06-02-0811-after-hours-autopilot-alpaca-core-preflight.json`
- Scheduler research preflight: `wiki/evidence-store/sources/2026-06-02-0811-after-hours-autopilot-research-mcp-preflight.json`

## 검증

- Universe strict: PASS
- MCP strict: PASS
- Risk policy: PASS, expected warning `orders is empty`
