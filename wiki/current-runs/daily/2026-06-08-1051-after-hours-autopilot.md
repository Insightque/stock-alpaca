# 2026-06-08-1051-after-hours-autopilot

## 요약

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Session: `after_hours`
- Policy profile: `after_hours_policy`
- Artifact tag: `after-hours`
- Review bucket: `after_hours_validation`
- Paper mode: `ALPACA_PAPER_TRADE=true` 확인
- 결과: scheduler-owned `1051` core/research preflight를 우선 사용했고 Alpaca core `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. 이번 cycle은 same-session after-hours order budget이 이미 `2/2`라 submit 없이 종료했다.

## 사용한 스케줄러 프리플라이트

- Alpaca core: `wiki/evidence-store/sources/2026-06-08-1051-after-hours-autopilot-alpaca-core-preflight.json`
- Research MCP: `wiki/evidence-store/sources/2026-06-08-1051-after-hours-autopilot-research-mcp-preflight.json`
- Alpaca core preflight의 `first_blocking_gate=market_closed`는 장외 워크플로우에서 예상되는 상태였고, passing account/positions/open-order/activity/asset/quote rows는 그대로 사용했다. runtime Alpaca MCP `get_clock`, `get_account_info`, `get_all_positions`, `get_orders(status=open)`, `get_orders(status=all, after=2026-06-08T00:00:00Z)`, `get_watchlists`, `get_stock_latest_quote(feed=overnight)`, `get_asset(AVGO,GOOGL,PFE,QQQ,SPY,WMT,BAC,XOM,SMH,TSLA)`는 same-session budget과 현재 executable quote stack을 교차 확인하는 용도로만 사용했다.

## Alpaca MCP 확인

- Regular market: closed (scheduler-owned `2026-06-07T21:51:06.964068577-04:00`, runtime `get_clock` `2026-06-07T21:54:04.816931046-04:00`)
- Account/positions: runtime `get_account_info` 기준 account `ACTIVE`, portfolio value `98,555.41 USD`, cash `30,731.86 USD`, buying power `296,444.32 USD`, positions `33`건이었다.
- Open orders: scheduler-owned preflight와 runtime `get_orders(status=open)` 모두 `0`건이었다.
- Same-session after-hours orders: runtime `get_orders(status=all, after=2026-06-08T00:00:00Z)` 기준 `ah-20260608-0911-sell-avgo`, `ah-20260608-0931-sell-avgo` 두 건만 `filled`였다. 따라서 `risk_inputs.after_hours_new_orders_submitted_today=2`이고 session cap `2/2`가 닫혔다.

## Universe/MCP 게이트

- Universe strict gate: PASS. broad metadata universe `62`개를 유지했고 required benchmarks `SPY`, `QQQ`를 포함했다. pre-MCP shortlist는 `QQQ, GOOGL, SMH, SPY, WMT, XOM, BAC, TSLA`였다.
- MCP strict gate: PASS. research preflight 기준 `sec-edgar`, `fred`, `firecrawl`, `yahoo-finance`는 pass였고 `alpha-vantage`는 `NEWS_SENTIMENT` `empty_response`였지만 submit-blocking gap으로 승격되지는 않았다.

## Quote/Spread 및 주문 결정

- `AVGO` sell/trim은 runtime overnight quote `387.17/388.31`, spread `0.293995%`로 이번 cycle에는 after-hours spread cap `0.25%`를 넘겨 sell path가 닫혔다.
- `GOOGL`, `PFE`, `WMT`, `BAC`, `TSLA`는 runtime overnight quote/spread/notional cap을 통과해 fallback buy executable stack을 형성했다.
- `QQQ`, `SPY`, `SMH`는 1주 ask가 after-hours per-order notional cap `0.5%`를 초과했고, `SMH`와 `XOM`은 spread도 after-hours cap `0.25%`를 넘겼다.
- 이번 cycle의 first blocking gate는 `separate_after_hours_order_budget`였다. hard requirement상 다른 이유로 빈 주문계획을 반환한 것이 아니라, same-session after-hours 제출 수가 이미 `2/2`에 도달해 새로운 `place_stock_order` 호출이 금지된 상태였다.
- `place_stock_order`와 `cancel_order_by_id`는 호출하지 않았다.

## Validator 및 산출물

- Order plan: `wiki/trade-ledger/orders/2026-06-08-1051-after-hours-autopilot.json`
- Run manifest: `wiki/evidence-store/run-manifests/2026-06-08-1051-after-hours-autopilot.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-06-08-1051-after-hours-autopilot-after-hours-gate-evaluation.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-08-1051-after-hours-autopilot-post-trade.json`
- Deterministic submit artifact: `wiki/evidence-store/sources/2026-06-08-1051-after-hours-autopilot-deterministic-submit.json`
- Validators: `check-universe-coverage --strict --json`, `check-mcp-coverage --strict --json`, `check-risk-policy.py --json`
- Universe strict: PASS (`PATH=/usr/local/bin:$PATH python3 scripts/check-universe-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-08-1051-after-hours-autopilot.json`)
- MCP strict: PASS (`PATH=/usr/local/bin:$PATH python3 scripts/check-mcp-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-08-1051-after-hours-autopilot.json`)
- Risk policy: PASS with expected `orders is empty` warning (`PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-06-08-1051-after-hours-autopilot.json`)
- Schema note: 현재 order-plan schema의 `risk_inputs.cash_deployment_blocker` enum에는 `separate_after_hours_order_budget_reached`가 없어 validator 호환을 위해 order plan에는 `daily_buy_cap_exhausted`를 기록했고, 실제 first blocking gate는 report/manifest에서 `separate_after_hours_order_budget`로 유지했다.
