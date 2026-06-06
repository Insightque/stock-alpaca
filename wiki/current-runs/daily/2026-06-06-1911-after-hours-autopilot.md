# 2026-06-06-1911-after-hours-autopilot

## 요약

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Session: `after_hours`
- Policy profile: `after_hours_policy`
- Artifact tag: `after-hours`
- Review bucket: `after_hours_validation`
- Paper mode: `ALPACA_PAPER_TRADE=true` 확인
- 결과: scheduler-owned `1911` core/research preflight를 우선 사용했고 Alpaca core `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. separate after-hours order budget은 `0/2`로 남아 있었지만, runtime Alpaca MCP clock/order/quote cross-check 기준 executable two-sided fresh quote stack을 만들지 못해 주문 없이 종료했다.

## 사용한 스케줄러 프리플라이트

- Alpaca core: `wiki/evidence-store/sources/2026-06-06-1911-after-hours-autopilot-alpaca-core-preflight.json`
- Research MCP: `wiki/evidence-store/sources/2026-06-06-1911-after-hours-autopilot-research-mcp-preflight.json`
- Alpaca core preflight의 `first_blocking_gate=market_closed`는 장외 워크플로우에서 예상되는 상태였고, passing account/positions/open-order/asset/watchlist/quote rows는 그대로 사용했다. 이번 cycle의 runtime Alpaca MCP 보조 확인은 `get_clock`, `get_orders(status=open)`, `get_orders(status=all, after=2026-06-05T20:00:00Z)`, `get_watchlists`, `get_stock_latest_quote(feed=iex)`, `get_stock_latest_quote(feed=overnight)`로 제한했다. market session, account, positions, recent fill source of record는 scheduler-owned `1911` preflight의 `get_clock`, `get_account_info`, `get_all_positions`, `get_account_activities(activity_types=FILL)` rows를 유지했다.

## Alpaca MCP 확인

- Regular market: closed (`2026-06-06T06:13:13.733235282-04:00`)
- Account: scheduler-owned `1911` preflight `get_account_info` 기준 account `ACTIVE`, portfolio value `98,156.33 USD`, cash `29,947.79 USD`, buying power `294,276.14 USD`, long market value `68,208.54 USD`였다.
- Positions: scheduler-owned `1911` preflight `get_all_positions` 기준 current positions `33`건이었다.
- Open orders: runtime `get_orders(status=open)` 기준 open order `0`건이었다.
- Watchlists: runtime `get_watchlists` 기준 `0`건이었다.
- Recent order history: runtime `get_orders(status=all, after=2026-06-05T20:00:00Z)` 기준 canceled regular-session `hourly-20260606-0451-buy-nke` 1건만 확인됐고 after-hours client order id는 없었다.
- After-hours session order count: scheduler-owned `1911` preflight의 `orders_submitted=0`과 이번 cycle의 no-submit result를 근거로 `risk_inputs.after_hours_new_orders_submitted_today=0`을 유지했다.
- Fill reconciliation: scheduler-owned `1911` preflight `get_account_activities(activity_types=FILL)` row를 source of record로 유지했고, 이번 cycle은 submit attempt가 없어 새로운 after-hours fill이나 `client_order_id` reconcile 대상이 없었다.

## Universe/MCP 게이트

- Universe strict gate: PASS. broad metadata universe `62`개를 유지했고 required benchmarks `SPY`, `QQQ`를 포함했다. pre-MCP shortlist는 `QQQ, GOOGL, SMH, SPY, WMT, XOM, BAC, TSLA`였다.
- MCP strict gate: PASS. research preflight 기준 `sec-edgar`, `fred`, `firecrawl`, `yahoo-finance`는 pass였고 `alpha-vantage`는 `NEWS_SENTIMENT` 빈 응답으로 `gap(empty_response)`였지만 policy상 submit-blocking gap은 아니었다.

## Quote/Spread 및 주문 결정

- `QQQ`는 runtime IEX quote spread가 `0.0157%`로 가장 양호했지만 quote age가 약 `805.10`분으로 5분 fresh-quote cap을 넘겼다.
- `SMH`, `SPY`, `WMT`, `GOOGL`, `XOM`, `BAC`, `TSLA`는 runtime IEX quote age가 약 `853.18-853.23`분 stale였고 spread도 after-hours cap `0.25%`를 크게 초과했다.
- `AVGO`, `PFE`는 runtime IEX quote가 bid-only였고 overnight quote는 `QQQ/AVGO/PFE` 모두 약 `1573.22`분 stale였다.
- 정책상 hard gates가 모두 통과하면 최소 1건의 floor-size order를 만들어야 하지만, 이번 cycle은 fresh quote / spread hard gate가 명시적으로 실패해 order plan을 비워 둔 no-submit 케이스로 기록했다.
- `place_stock_order`와 `cancel_order_by_id`는 호출하지 않았다.

## Validator 및 산출물

- Order plan: `wiki/trade-ledger/orders/2026-06-06-1911-after-hours-autopilot.json`
- Run manifest: `wiki/evidence-store/run-manifests/2026-06-06-1911-after-hours-autopilot.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-06-06-1911-after-hours-autopilot-after-hours-gate-evaluation.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-06-1911-after-hours-autopilot-post-trade.json`
- Validators: `check-universe-coverage --strict --json` PASS, `check-mcp-coverage --strict --json` PASS, `check-risk-policy --json` PASS (`orders is empty` warning only).
