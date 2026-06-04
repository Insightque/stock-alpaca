# 2026-06-04 16:17 KST After-Hours Paper Autopilot

## 요약

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Session: `after_hours`
- Policy profile: `after_hours_policy`
- Artifact tag: `after-hours`
- Review bucket: `after_hours_validation`
- Paper mode: `ALPACA_PAPER_TRADE=true`
- 결과: 신규 주문 없음

## 게이트

- Alpaca core: scheduler-owned preflight `wiki/evidence-store/sources/2026-06-04-1611-after-hours-autopilot-alpaca-core-preflight.json` 사용. `first_blocking_gate=market_closed`는 after-hours에서 예상된 비차단 상태로 처리했고, account/positions/open_orders/asset/quote/spread 행을 통과 근거로 사용했다.
- Alpaca evidence: runtime Alpaca MCP 기준 `get_clock` regular market closed at `2026-06-04T03:13:31.497688143-04:00`, `get_account_info` ACTIVE, `get_all_positions` 32건, `get_orders status=all after 2026-06-03T20:00:00Z asset_class=us_equity` 0건, `get_watchlists` 0건, shortlist `get_stock_latest_quote` IEX spot-check를 확인했다.
- Research MCP: `wiki/evidence-store/sources/2026-06-04-1611-after-hours-autopilot-research-mcp-preflight.json` 사용. SEC EDGAR, FRED, Firecrawl, Yahoo Finance pass; Alpha Vantage는 `empty_response` gap이지만 최소 research confirmation 3개를 넘겨 strict MCP gate는 통과했다.
- Universe strict: broad metadata universe 62개와 SPY/QQQ 포함 조건을 유지했고, scheduler research shortlist `PFE, NOK, QQQ, SPY, META, XOM, INTC, AVGO`를 최종 후보로 사용했다.
- Risk policy: empty order plan으로 검증했다. `market.session=after_hours`, `risk_inputs.after_hours_new_orders_submitted_today=0`를 사용했고 정규 validation order count는 재사용하지 않았다.
- Submit gate summary: no submit candidate. paper mode PASS, regular market closed at `2026-06-04T03:11:07.928707769-04:00` in scheduler preflight and `2026-06-04T03:13:31.497688143-04:00` in runtime `get_clock`, order plan `wiki/trade-ledger/orders/2026-06-04-1611-after-hours-autopilot.json`, universe/MCP/risk validator PASS, scheduler quote freshness/spread rows PASS, order shape는 no-order로 N/A, duplicate/open-order check PASS(0 session orders), source refs는 scheduler Alpaca/research preflight와 after-hours gate evaluation이다.

## 후보 판단

- `PFE`: 2026-05-29 validation add 1D 회고 약함.
- `NOK`: 최신 review backlog에서 20D pending이 남아 after-hours add 차단.
- `QQQ`, `SPY`: 기존 benchmark 보유 유지.
- `META`: 현재 위키 ticker thesis page 부재.
- `XOM`: 2026-05-28 validation buy 1D 회고 약함.
- `INTC`: 2026-05-28 after-hours validation buy 1D 회고 약함.
- `AVGO`: 최신 review backlog에서 5D pending이 남아 동일 bucket add 차단.

## 주문 및 조정

- `place_stock_order` 호출 없음.
- 새 `client_order_id` 없음.
- 대체 client order id retry 없음.
- after-hours sell은 `after_hours_policy.allowed_sides=[buy]` 밖이므로 risk-trim 관찰은 다음 regular-session 진단 큐로만 넘긴다.

## 산출물

- Manifest: `wiki/evidence-store/run-manifests/2026-06-04-1611-after-hours-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-04-1611-after-hours-autopilot.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-06-04-1611-after-hours-autopilot-after-hours-gate-evaluation.json`
- Scheduler Alpaca preflight: `wiki/evidence-store/sources/2026-06-04-1611-after-hours-autopilot-alpaca-core-preflight.json`
- Scheduler research preflight: `wiki/evidence-store/sources/2026-06-04-1611-after-hours-autopilot-research-mcp-preflight.json`

## 검증

- Universe strict: PASS
- MCP strict: PASS
- Risk policy: PASS, expected warning `orders is empty`
