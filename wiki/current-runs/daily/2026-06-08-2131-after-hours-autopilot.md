# 2026-06-08-2131-after-hours-autopilot

## 요약

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Session: `after_hours`
- Policy profile: `after_hours_policy`
- Artifact tag: `after-hours`
- Review bucket: `after_hours_validation`
- Paper mode: `ALPACA_PAPER_TRADE=true` 확인
- 결과: scheduler-owned `2131` core/research preflight를 우선 사용했고 Alpaca core `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. 이번 cycle은 same-session after-hours order budget이 이미 `2/2`라 submit 없이 종료했다.

## 사용한 스케줄러 프리플라이트

- Alpaca core: `wiki/evidence-store/sources/2026-06-08-2131-after-hours-autopilot-alpaca-core-preflight.json`
- Research MCP: `wiki/evidence-store/sources/2026-06-08-2131-after-hours-autopilot-research-mcp-preflight.json`
- Alpaca core preflight의 `first_blocking_gate=market_closed`는 장외 워크플로우에서 예상되는 상태였고, passing account/positions/open-order/asset/quote/spread rows는 그대로 사용했다. same-session fill 근거는 scheduler-owned `get_account_activities` row를 source of record로 유지했고, Alpaca MCP `get_order_by_client_id`로 `ah-20260608-0911-sell-avgo`, `ah-20260608-0931-sell-avgo`를 재확인했다.

## Alpaca MCP 확인

- Regular market: closed (scheduler-owned `get_clock` `2026-06-08T08:31:05.282249171-04:00`)
- Account/positions: scheduler-owned `2131` preflight 기준 account `ACTIVE`, portfolio value `99,841.23 USD`, cash `30,731.86 USD`, buying power `299,297.80 USD`, positions `33`건이었다.
- Open orders: scheduler-owned `get_orders_open` 기준 `0`건이었다.
- Same-session after-hours orders: scheduler-owned recent-activities row와 Alpaca MCP `get_order_by_client_id` 기준 `ah-20260608-0911-sell-avgo`, `ah-20260608-0931-sell-avgo` 두 건만 `filled`였다. 따라서 `risk_inputs.after_hours_new_orders_submitted_today=2`이고 session cap `2/2`가 닫혔다.
- Watchlists: Alpaca MCP `get_watchlists` 기준 `0`건이었다.

## Universe/MCP 게이트

- Universe strict gate: PASS. broad metadata universe `62`개를 유지했고 required benchmarks `SPY`, `QQQ`를 포함했다. pre-MCP shortlist는 `SPY, QQQ, NOK, GOOGL, SMH, WMT, XOM, BAC`였다.
- MCP strict gate: PASS. research preflight 기준 `sec-edgar`, `fred`, `firecrawl`, `yahoo-finance`는 pass였고 `alpha-vantage`는 `NEWS_SENTIMENT` `empty_response`였지만 submit-blocking gap으로 승격되지는 않았다.

## Quote/Spread 및 주문 결정

- 이 cycle은 hard requirement에 따라 scheduler-owned `2131` Alpaca core preflight의 passing account/positions/orders/asset/quote/spread rows를 그대로 사용했다. 추가적인 after-hours-required row 누락이나 실패는 확인되지 않았다.
- `AVGO`는 이번 cycle에서도 preferred sell/trim candidate로 유지됐고, `GOOGL/NOK/WMT/BAC/XOM`는 unchanged shortlist 기준 fallback buy stack으로 유지됐다. 다만 실제 `place_stock_order` 분기 전 first blocking gate가 이미 `separate_after_hours_order_budget`로 닫혀 있었다.
- `QQQ`, `SPY`, `SMH`는 scheduler-owned `2131` preflight ask 기준 current after-hours per-order notional cap `499.21 USD`를 초과했다.
- 이번 cycle의 first blocking gate는 `separate_after_hours_order_budget`였다. hard requirement상 다른 이유로 빈 주문계획을 반환한 것이 아니라, same-session after-hours 제출 수가 이미 `2/2`에 도달해 새로운 `place_stock_order` 호출이 금지된 상태였다.
- `place_stock_order`와 `cancel_order_by_id`는 호출하지 않았다.

## Validator 및 산출물

- Order plan: `wiki/trade-ledger/orders/2026-06-08-2131-after-hours-autopilot.json`
- Run manifest: `wiki/evidence-store/run-manifests/2026-06-08-2131-after-hours-autopilot.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-06-08-2131-after-hours-autopilot-after-hours-gate-evaluation.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-08-2131-after-hours-autopilot-post-trade.json`
- Deterministic submit artifact: `wiki/evidence-store/sources/2026-06-08-2131-after-hours-autopilot-deterministic-submit.json`

- Validators: `PATH=/usr/local/bin:$PATH python3 scripts/check-universe-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-08-2131-after-hours-autopilot.json` PASS, `PATH=/usr/local/bin:$PATH python3 scripts/check-mcp-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-08-2131-after-hours-autopilot.json` PASS, `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-06-08-2131-after-hours-autopilot.json` PASS with expected `orders is empty` warning
- Schema note: validator 호환을 위해 order plan `risk_inputs.cash_deployment_blocker`에는 `daily_buy_cap_exhausted`를 기록했고, 실제 first blocking gate는 report/manifest에서 `separate_after_hours_order_budget`로 유지했다.
