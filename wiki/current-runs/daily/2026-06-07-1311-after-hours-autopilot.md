# 2026-06-07-1311-after-hours-autopilot

## 요약

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Session: `after_hours`
- Policy profile: `after_hours_policy`
- Artifact tag: `after-hours`
- Review bucket: `after_hours_validation`
- Paper mode: `ALPACA_PAPER_TRADE=true` 확인
- 결과: scheduler-owned `1311` core/research preflight를 우선 사용했고 Alpaca core `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. separate after-hours order budget은 `0/2`로 남아 있었지만, runtime Alpaca MCP와 동일한 stale/bid-only IEX quote stack 때문에 주문 없이 종료했다.

## 사용한 스케줄러 프리플라이트

- Alpaca core: `wiki/evidence-store/sources/2026-06-07-1311-after-hours-autopilot-alpaca-core-preflight.json`
- Research MCP: `wiki/evidence-store/sources/2026-06-07-1311-after-hours-autopilot-research-mcp-preflight.json`
- Alpaca core preflight의 `first_blocking_gate=market_closed`는 장외 워크플로우에서 예상되는 상태였고, passing clock/account/positions/open-order/asset/quote rows는 그대로 사용했다. 이번 cycle에서는 runtime Alpaca MCP `get_clock`, `get_account_info`, `get_all_positions`, `get_orders(status=open)`, `get_orders(status=all, after=2026-06-05T20:00:00Z)`, `get_watchlists`, `get_account_activities(activity_types=FILL, after=2026-06-05T20:00:00Z)`, `get_stock_latest_quote(feed=iex)`, `get_stock_latest_quote(feed=overnight)`를 read-only로 재호출해 동일 상태를 교차 확인했다.

## Alpaca MCP 확인

- Regular market: closed (`2026-06-07T00:12:56.578721211-04:00` runtime `get_clock`, source-of-record cutoff `2026-06-07T00:11:07.296296326-04:00` scheduler preflight clock)
- Account: runtime `get_account_info`와 scheduler-owned `1311` preflight 모두 account `ACTIVE`, portfolio value `98,156.33 USD`, cash `29,947.79 USD`, buying power `294,276.14 USD`, long market value `68,208.54 USD`.
- Positions: runtime `get_all_positions`와 scheduler-owned `1311` preflight 모두 current positions `33`건.
- Open orders: runtime `get_orders(status=open)`와 scheduler-owned `1311` preflight open-order row 모두 `0`건.
- Watchlists: runtime `get_watchlists`와 scheduler-owned `1311` preflight watchlist row 모두 `0`건.
- Recent order history: runtime `get_orders(status=all, after=2026-06-05T20:00:00Z)`에는 canceled regular-session `hourly-20260606-0451-buy-nke` 1건만 있었고 `extended_hours=false`라 after-hours session budget에 포함하지 않았다.
- Fill reconciliation: runtime `get_account_activities(activity_types=FILL, after=2026-06-05T20:00:00Z)`는 빈 결과였고, 이번 cycle은 submit attempt가 없어 새로운 after-hours fill이나 `client_order_id` reconcile 대상이 없었다.
- After-hours session order count: scheduler-owned `1311` preflight의 `orders_submitted=0`과 이번 cycle의 no-submit result를 근거로 `risk_inputs.after_hours_new_orders_submitted_today=0`을 유지했다.

## Universe/MCP 게이트

- Universe strict gate: PASS. broad metadata universe `62`개를 유지했고 required benchmarks `SPY`, `QQQ`를 포함했다. pre-MCP shortlist는 `QQQ, GOOGL, SMH, SPY, WMT, XOM, BAC, TSLA`였다.
- MCP strict gate: PASS. research preflight 기준 `sec-edgar`, `fred`, `firecrawl`, `yahoo-finance`는 pass였고 `alpha-vantage`는 `NEWS_SENTIMENT` empty_response으로 `gap(empty_response)`였지만 policy상 submit-blocking gap은 아니었다.

## Quote/Spread 및 주문 결정

- `QQQ`는 runtime IEX quote spread가 `0.0157%`로 가장 양호했지만 quote age가 약 `1884.82`분으로 5분 fresh-quote cap을 넘겼다.
- `SMH`, `SPY`, `WMT`, `GOOGL`, `XOM`, `BAC`, `TSLA`는 runtime IEX quote age가 약 `1932.89-1932.94`분 stale였고 spread도 after-hours cap `0.25%`를 크게 초과했다.
- `AVGO`, `PFE`는 runtime IEX quote가 bid-only였다. `AVGO` sell/trim은 active sell side 정책에 따라 다시 평가했지만 executable two-sided quote가 없어 제출 후보로 승격되지 않았다.
- `QQQ`, `AVGO`, `PFE`의 runtime `overnight` feed도 각각 약 `2652.94`, `2652.94`, `2652.94`분 stale여서 fallback extended-hours quote stack을 보강하지 못했다.
- 정책상 hard gates가 모두 통과하면 최소 1건의 floor-size order를 만들어야 하지만, 이번 cycle은 fresh quote / spread hard gate가 명시적으로 실패해 order plan을 비워 둔 no-submit 케이스로 기록했다.
- `place_stock_order`와 `cancel_order_by_id`는 호출하지 않았다.

## Validator 및 산출물

- Order plan: `wiki/trade-ledger/orders/2026-06-07-1311-after-hours-autopilot.json`
- Run manifest: `wiki/evidence-store/run-manifests/2026-06-07-1311-after-hours-autopilot.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-06-07-1311-after-hours-autopilot-after-hours-gate-evaluation.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-07-1311-after-hours-autopilot-post-trade.json`
- Validators: `check-universe-coverage --strict --json`, `check-mcp-coverage --strict --json`, `check-risk-policy.py --json`
