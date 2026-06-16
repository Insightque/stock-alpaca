# 2026-06-16-1931-after-hours-autopilot

## 요약

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Session: `after_hours`
- Policy profile: `after_hours_policy`
- Artifact tag: `after-hours`
- Review bucket: `after_hours_validation`
- Paper mode: `ALPACA_PAPER_TRADE=true` 확인
- 결과: scheduler-owned `1931` core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. 이번 turn은 별도 live continuity를 열지 않고 same preflight rows를 그대로 사용했으며, candidate latestQuote timestamp가 약 `823.38-873.90`분 stale로 남아 fresh-quote hard gate가 닫혔다. sell-first 후보는 same-day duplicate sell discipline과 spread cap에 막혔고, buy fallback은 review backlog throttle, `blocked_add_symbols=['NOK']`, per-order cap, quote completeness, watch-only thesis 때문에 executable after-hours order가 남지 않았다.

## 사용한 스케줄러 프리플라이트

- Alpaca core: `wiki/evidence-store/sources/2026-06-16-1931-after-hours-autopilot-alpaca-core-preflight.json`
- Research MCP: `wiki/evidence-store/sources/2026-06-16-1931-after-hours-autopilot-research-mcp-preflight.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-06-16-1931-after-hours-autopilot-after-hours-gate-evaluation.json`
- Alpaca core preflight의 `first_blocking_gate=market_closed`는 after-hours 워크플로우에서 expected nonblocking으로 처리했다. 이번 `1931` cycle은 scheduler-owned passing rows만으로 account, positions, open orders, recent activities, asset, quote/spread, shortlist, research coverage를 유지했다.

## Alpaca MCP 확인

- Regular market: closed. scheduler-owned `get_clock` 기준 `timestamp=2026-06-16T06:31:09.911936136-04:00`.
- Account: scheduler-owned `get_account_info` 기준 account `ACTIVE`, portfolio value `102580.93 USD`, cash `29836.34 USD`, buying power `306303.78 USD`였다.
- Positions / orders: scheduler-owned `get_all_positions` 기준 positions `33`건, `get_orders(status=open)` 기준 open orders `0`건이었다.
- Same-session after-hours orders: scheduler-owned recent order/activity baseline 기준 same-session after-hours submitted orders `0`건, fills `0`건이었다. watchlists도 `0`건으로 유지됐다.
- Quote boundary: scheduler-owned `get_stock_snapshot` rows 기준 `QQQ 742.78/743.24`, `RGTI 22.73/22.81`, `NOK 14.78/14.84`, `TSLA 391.40/410.95`, `SMH 629.42/662.96`, `SLB 53.00/56.73`, `AVGO 375.72/408.22`, `GE 330.01/359.63`, `SPY 753.31/0.00`, `MSFT 376.73/424.01`, `PFE 24.89/27.58`를 사용했다. 그러나 freshest `QQQ`도 decision 시점 기준 약 `823.38`분 stale였고 나머지는 `861.22-873.90`분 stale였다.

## 후보 평가

- `AVGO`: scheduler-owned latestQuote `375.72/408.22`, spread 약 `8.2915%`, stale quote, 그리고 `2026-06-15 11:18 ET` fill에 따른 same-day duplicate sell discipline이 동시에 남았다.
- `RGTI`: scheduler-owned latestQuote `22.73/22.81`, spread 약 `0.3513%`, stale quote, `2026-06-15 09:41 ET` regular-session trim fills에 따른 duplicate sell discipline이 겹쳤다.
- `PFE`: repeated weak-review trim rationale은 유지됐지만 latestQuote `24.89/27.58`, spread 약 `10.2535%`, stale quote, same-day duplicate sell discipline 때문에 submit path가 열리지 않았다.
- `MSFT`: latestQuote `376.73/424.01`, spread 약 `11.8091%`로 policy cap을 크게 넘었고, stale quote, same-day duplicate buy, `review_backlog_pending_1d_count=18`이 함께 남았다.
- `NOK`: latestQuote `14.78/14.84`, stale quote, spread 약 `0.4051%`, `review-due-index`의 `blocked_add_symbols=['NOK']`, review backlog throttle이 동시에 남았다.
- `QQQ`: benchmark fallback quote는 있었지만 stale quote였고 1주 ask `743.24 USD`가 after-hours per-order cap 약 `512.90 USD`를 넘었다.
- `SPY`: stale quote였고 ask liquidity가 `0`이라 quote completeness가 닫혔다. latest trade `754.50 USD`도 per-order cap을 넘었다.
- `SMH`: stale quote와 spread 약 `5.1904%`, 1주 ask `662.96 USD` per-order cap 초과가 동시에 남았다.
- `TSLA`: stale quote, spread 약 `4.8732%`, watch-only thesis 때문에 actionable fallback으로 승격되지 않았다.
- `SLB/GE`: stale quote에 더해 spread가 각각 약 `6.7985%`, `8.5900%`로 계속 fail이었다.

## MCP 커버리지

- `alpaca`: PASS. scheduler-owned `1931` core preflight를 source-of-record로 사용했다.
- `sec-edgar`: PASS. scheduler-owned research preflight reused.
- `alpha-vantage`: GAP. `NEWS_SENTIMENT`가 shortlisted symbols에 대해 빈 결과를 반환했다.
- `fred`: PASS. scheduler-owned research preflight reused.
- `firecrawl`: FAILED. credit 부족 provider error가 유지됐다.
- `yahoo-finance`: PASS. scheduler-owned research preflight reused.
- Strict MCP gate는 `sec-edgar/fred/yahoo-finance` 3개 research confirmation을 유지했으므로 PASS였다.

## Gate 결과

| Gate | Status |
| --- | --- |
| alpaca_paper_mode | pass |
| regular_market_open | pass_regular_market_closed |
| extended_hours_session | pass |
| alpaca_core_account_clock_position_order_quote_spread | pass_scheduler_preflight |
| after_hours_policy_profile | pass |
| separate_after_hours_order_budget | pass_zero_of_two_submitted |
| universe_strict | PASS |
| mcp_tiered_strict | PASS |
| risk_policy | PASS with expected `orders is empty` warning |
| fresh_quote | FAIL: scheduler-owned latestQuote rows were about `823.38-873.90` minutes old |
| spread_within_after_hours_policy | fail for `AVGO/GE/MSFT/NOK/PFE/SLB/SMH/TSLA`; `QQQ/RGTI` only spread-pass but still stale, and `SPY` ask was missing |
| whole_share_day_limit_extended_hours_order | fail_no_eligible_order_survived_fresh_quote_duplicate_sells_buy_backlog_add_block_watch_only_notional_quote_completeness_or_spread_caps |
| immediate_reconcile_and_cancel_or_lifecycle_record | pass_no_submit |

## Submit And Reconcile

- `place_stock_order`는 호출하지 않았다. 신규 `client_order_id`, retry, alternate client id도 없었다.
- Separate after-hours session budget은 `0/2`로 열려 있었지만 fresh-quote hard gate가 닫혀 있었고, sell path는 same-day duplicate discipline과 spread cap에, buy path는 review backlog throttle, add-block, per-order cap, quote completeness, watch-only thesis에 막혀 executable order가 남지 않았다.
- 이번 cycle의 reconciliation은 scheduler-owned `1931` preflight 기준 same-session after-hours orders `0`건, positions `33`건, open orders `0`건을 재확인하는 수준에서 종료했다.

## Validators

- `PATH=/usr/local/bin:$PATH python3 scripts/check-universe-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-16-1931-after-hours-autopilot.json`
- `PATH=/usr/local/bin:$PATH python3 scripts/check-mcp-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-16-1931-after-hours-autopilot.json`
- `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-06-16-1931-after-hours-autopilot.json`

## Artifacts

- Report: `wiki/current-runs/daily/2026-06-16-1931-after-hours-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-16-1931-after-hours-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-16-1931-after-hours-autopilot.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-06-16-1931-after-hours-autopilot-after-hours-gate-evaluation.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-16-1931-after-hours-autopilot-post-trade.json`
