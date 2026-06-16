# 2026-06-16-2031-after-hours-autopilot

## 요약

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Session: `after_hours`
- Policy profile: `after_hours_policy`
- Artifact tag: `after-hours`
- Review bucket: `after_hours_validation`
- Paper mode: `ALPACA_PAPER_TRADE=true` 확인
- 결과: scheduler-owned `2031` core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. live continuity로 `get_clock/get_account_info/get_all_positions/get_watchlists/get_orders(status=open)/get_orders(status=all, after=2026-06-15T20:00:00Z)/get_stock_snapshot(feed=overnight)`를 다시 열었지만, candidate `latestQuote` timestamp가 모두 `2026-06-16T08:00:00Z` 부근에 머물러 약 `212.83`분 stale였다. sell-first 후보는 same-day duplicate sell discipline과 spread cap에 막혔고, buy fallback은 review backlog throttle, `blocked_add_symbols=['NOK']`, per-order cap, watch-only thesis, spread cap 때문에 executable after-hours order가 남지 않았다.

## 사용한 스케줄러 프리플라이트

- Alpaca core: `wiki/evidence-store/sources/2026-06-16-2031-after-hours-autopilot-alpaca-core-preflight.json`
- Research MCP: `wiki/evidence-store/sources/2026-06-16-2031-after-hours-autopilot-research-mcp-preflight.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-06-16-2031-after-hours-autopilot-after-hours-gate-evaluation.json`
- Alpaca core preflight의 `first_blocking_gate=market_closed`는 after-hours 워크플로우에서 expected nonblocking으로 처리했다. 이번 `2031` cycle은 scheduler-owned passing rows로 recent activity baseline을 유지했고, live continuity로 clock/account/positions/watchlists/open orders/order history/overnight snapshot boundary를 다시 확인했다.

## Alpaca MCP 확인

- Regular market: closed. live `get_clock` 기준 `timestamp=2026-06-16T07:32:49.952167827-04:00`.
- Account: live `get_account_info` 기준 account `ACTIVE`, portfolio value `102719.44 USD`, cash `29836.34 USD`, buying power `306691.62 USD`였다.
- Positions / orders: live `get_all_positions` 기준 positions `33`건, live `get_watchlists` 기준 watchlists `0`건이었다. live `get_orders(status=open)`와 `get_orders(status=all, after=2026-06-15T20:00:00Z)` 기준 open orders `0`건, same-session after-hours submitted orders `0`건이었다.
- Quote boundary: live `get_stock_snapshot(feed=overnight)` 기준 `QQQ 719.66/799.94`, `RGTI 21.02/23.11`, `NOK 14.92/15.49`, `TSLA 405.19/419.07`, `SMH 644.69/645.98`, `SLB 44.99/56.96`, `AVGO 385.18/397.28`, `GE 316.70/349.71`, `SPY 753.72/754.96`, `MSFT 399.97/400.09`, `PFE 26.04/26.82`를 사용했다. 그러나 latestQuote timestamp는 전부 `2026-06-16T08:00:00Z` 부근이라 decision 시점 기준 약 `212.83`분 stale였다.

## 후보 평가

- `AVGO`: live overnight latestQuote `385.18/397.28`, spread 약 `3.0928%`, stale quote, `2026-06-15 11:18 ET` fill에 따른 same-day duplicate sell discipline이 동시에 남았다.
- `RGTI`: live overnight latestQuote `21.02/23.11`, spread 약 `9.4720%`, stale quote, `2026-06-15 09:41 ET` regular-session trim fills에 따른 duplicate sell discipline이 겹쳤다.
- `PFE`: repeated weak-review trim rationale은 유지됐지만 latestQuote `26.04/26.82`, spread 약 `2.9512%`, stale quote, same-day duplicate sell discipline 때문에 submit path가 열리지 않았다.
- `MSFT`: latestQuote `399.97/400.09`로 spread는 약 `0.0300%`까지 정상화됐지만 stale quote, same-day duplicate buy, `review_backlog_pending_1d_count=18`이 여전히 남았다.
- `NOK`: latestQuote `14.92/15.49`, stale quote, spread 약 `3.7488%`, `review-due-index`의 `blocked_add_symbols=['NOK']`, review backlog throttle이 동시에 남았다.
- `QQQ`: benchmark fallback quote는 있었지만 stale quote였고 spread도 약 `10.5659%`로 widened됐다. 1주 ask `799.94 USD`는 after-hours per-order cap 약 `513.60 USD`를 넘었다.
- `SPY`: live overnight ask liquidity는 있었고 spread는 약 `0.1644%`였지만 stale quote였고 1주 ask `754.96 USD`가 per-order cap을 넘었다.
- `SMH`: stale quote였고 1주 ask `645.98 USD`가 per-order cap을 넘었다. spread는 약 `0.1999%`로 cap 안쪽이어도 notional gate가 닫혔다.
- `TSLA`: stale quote, spread 약 `3.3679%`, watch-only thesis 때문에 actionable fallback으로 승격되지 않았다.
- `SLB/GE`: stale quote에 더해 spread가 각각 약 `23.4821%`, `9.9068%`로 계속 fail이었다.

## MCP 커버리지

- `alpaca`: PASS. scheduler-owned `2031` core preflight를 source-of-record로 사용했고 live continuity로 clock/account/positions/watchlists/open-order/order-history/overnight snapshot boundary를 재확인했다.
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
| fresh_quote | FAIL: live overnight latestQuote rows were about `212.83` minutes old |
| spread_within_after_hours_policy | fail for `AVGO/GE/NOK/PFE/QQQ/RGTI/SLB/TSLA`; `MSFT/SPY/SMH` only spread-pass but still stale, and `QQQ/SPY/SMH` also failed notional caps |
| whole_share_day_limit_extended_hours_order | fail_no_eligible_order_survived_fresh_quote_duplicate_sells_buy_backlog_add_block_watch_only_notional_or_spread_caps |
| immediate_reconcile_and_cancel_or_lifecycle_record | pass_no_submit |

## Submit And Reconcile

- `place_stock_order`는 호출하지 않았다. 신규 `client_order_id`, retry, alternate client id도 없었다.
- Separate after-hours session budget은 `0/2`로 열려 있었지만 fresh-quote hard gate가 닫혀 있었고, sell path는 same-day duplicate discipline과 spread cap에, buy path는 review backlog throttle, add-block, per-order cap, watch-only thesis, spread cap에 막혀 executable order가 남지 않았다.
- 이번 cycle의 reconciliation은 live continuity 기준 positions `33`건, watchlists `0`건, account `ACTIVE`, open orders `0`건, same-session after-hours orders `0`건을 재확인하는 수준에서 종료했다.

## Validators

- `PATH=/usr/local/bin:$PATH python3 scripts/check-universe-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-16-2031-after-hours-autopilot.json`
- `PATH=/usr/local/bin:$PATH python3 scripts/check-mcp-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-16-2031-after-hours-autopilot.json`
- `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-06-16-2031-after-hours-autopilot.json`

## Artifacts

- Report: `wiki/current-runs/daily/2026-06-16-2031-after-hours-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-16-2031-after-hours-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-16-2031-after-hours-autopilot.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-06-16-2031-after-hours-autopilot-after-hours-gate-evaluation.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-16-2031-after-hours-autopilot-post-trade.json`
