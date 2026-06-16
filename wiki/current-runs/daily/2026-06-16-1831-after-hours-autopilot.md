# 2026-06-16-1831-after-hours-autopilot

## 요약

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Session: `after_hours`
- Policy profile: `after_hours_policy`
- Artifact tag: `after-hours`
- Review bucket: `after_hours_validation`
- Paper mode: `ALPACA_PAPER_TRADE=true` 확인
- 결과: scheduler-owned `1831` core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. 다만 같은 preflight의 after-hours quote rows가 `QQQ/RGTI/NOK/TSLA/SMH/SLB/AVGO/GE/SPY/MSFT/PFE` 전반에서 약 `760.95-811.47`분 stale였고, sell-first 후보는 duplicate sell discipline과 spread cap에 막혔으며, buy fallback은 review backlog throttle, `blocked_add_symbols=['NOK']`, per-order cap, watch-only thesis, quote completeness failure 때문에 executable after-hours order가 남지 않았다.

## 사용한 스케줄러 프리플라이트

- Alpaca core: `wiki/evidence-store/sources/2026-06-16-1831-after-hours-autopilot-alpaca-core-preflight.json`
- Research MCP: `wiki/evidence-store/sources/2026-06-16-1831-after-hours-autopilot-research-mcp-preflight.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-06-16-1831-after-hours-autopilot-after-hours-gate-evaluation.json`
- Alpaca core preflight의 `first_blocking_gate=market_closed`는 after-hours 워크플로우에서 expected nonblocking으로 처리했다. 이번 `1831` cycle은 direct live Alpaca MCP read tool이 노출되지 않아 scheduler-owned passing account/positions/open-order/activity/watchlist/quote rows 자체를 source-of-record로 유지했다.

## Alpaca MCP 확인

- Regular market: closed. scheduler-owned `get_clock` 기준 `timestamp=2026-06-16T05:31:08.692360829-04:00`.
- Account: scheduler-owned `get_account_info` 기준 account `ACTIVE`, portfolio value `102630.59 USD`, cash `29836.34 USD`, buying power `306352.79 USD`였다.
- Positions / watchlists / orders: scheduler-owned `get_all_positions` 기준 positions `33`건, `get_watchlists` 기준 watchlists `0`건, `get_orders_open` 기준 open orders `0`건이었다.
- Same-session after-hours orders/fills: scheduler-owned preflight 범위에서 same-session after-hours submitted orders `0`건, `risk_inputs.after_hours_new_orders_submitted_today=0`, separate session cap `0/2`로 유지했다. `get_account_activities`에 보인 항목은 `2026-06-15` regular-session fills였다.
- Quote boundary: scheduler-owned `get_stock_latest_quote(feed=overnight)` rows 기준 `QQQ 742.78/743.24`, `RGTI 22.73/22.81`, `NOK 14.78/14.84`, `TSLA 391.40/410.95`, `SMH 629.42/662.96`, `SLB 53.00/56.73`, `AVGO 375.72/408.22`, `GE 330.01/359.63`, `SPY 753.31/0.00`, `MSFT 376.73/424.01`, `PFE 24.89/27.58`를 사용했다. 그러나 timestamp는 모두 `2026-06-15T20:00:00Z` 부근에 머물러 decision 시점 기준 약 `760.95-811.47`분 stale였고, `QQQ`만 spread cap `0.25%` 이내, `RGTI/NOK`조차 cap 초과, `SPY`는 ask `0.0`으로 quote completeness가 실패했다.

## 후보 평가

- `AVGO`: scheduler-owned quote `375.72/408.22`, spread 약 `8.2915%`, stale quote, 그리고 same-day duplicate sell discipline이 동시에 남았다.
- `RGTI`: scheduler-owned quote `22.73/22.81`, spread 약 `0.3513%`, stale quote, `2026-06-15` regular-session trim fills에 따른 duplicate sell discipline이 겹쳤다.
- `PFE`: repeated weak-review trim rationale은 유지됐지만 quote `24.89/27.58`, spread 약 `10.2535%`, stale quote, same-day duplicate sell discipline 때문에 submit path가 열리지 않았다.
- `MSFT`: quote `376.73/424.01`, spread 약 `11.8091%`, stale quote, same-day duplicate buy, `review_backlog_pending_1d_count=18`이 함께 남았다.
- `NOK`: quote `14.78/14.84`, stale quote, spread 약 `0.4051%`, `review-due-index`의 `blocked_add_symbols=['NOK']`, review backlog throttle이 동시에 남았다.
- `QQQ`: benchmark fallback quote는 있었지만 stale quote였고 1주 ask `743.24 USD`가 after-hours per-order cap 약 `513.15 USD`를 넘었다.
- `SPY`: stale quote에 더해 ask `0.0`으로 quote completeness가 실패했고, benchmark fallback 1주 notional도 cap을 넘었다.
- `SMH`: stale quote, spread 약 `5.1904%`, 1주 ask `662.96 USD`로 per-order cap 초과였다.
- `TSLA`: stale quote, spread 약 `4.8732%`, watch-only thesis 때문에 actionable fallback으로 승격되지 않았다.
- `SLB/GE`: stale quote에 더해 spread가 각각 약 `6.7985%`, `8.5900%`로 계속 fail이었다.

## MCP 커버리지

- `alpaca`: PASS. scheduler-owned `1831` core preflight passing rows를 사용했다.
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
| alpaca_core_account_clock_position_order_quote_spread | pass_scheduler_preflight_rows_reused |
| after_hours_policy_profile | pass |
| separate_after_hours_order_budget | pass_zero_of_two_submitted |
| universe_strict | PASS |
| mcp_tiered_strict | PASS |
| risk_policy | PASS with expected `orders is empty` warning |
| fresh_quote | FAIL: scheduler-owned quotes were about `760.95-811.47` minutes old |
| spread_within_after_hours_policy | pass only for `QQQ`; fail for `AVGO/GE/MSFT/NOK/PFE/RGTI/SLB/SMH/TSLA` and `SPY` quote completeness |
| whole_share_day_limit_extended_hours_order | fail_no_eligible_order_survived_fresh_quote_duplicate_sells_buy_backlog_add_block_quote_completeness_or_notional_or_spread_caps |
| immediate_reconcile_and_cancel_or_lifecycle_record | pass_no_submit |

## Submit And Reconcile

- `place_stock_order`는 호출하지 않았다. 신규 `client_order_id`, retry, alternate client id도 없었다.
- Separate after-hours session budget은 `0/2`로 열려 있었지만 fresh-quote hard gate가 닫혀 있었고, 같은 preflight rows 기준으로도 실행 가능한 sell은 duplicate discipline 또는 spread cap에 막히고 buy는 review backlog throttle, add-block, per-order cap, watch-only thesis, quote completeness 때문에 submit path가 열리지 않았다.
- 이번 cycle의 reconciliation은 scheduler-owned `1831` preflight rows 기준 same-session after-hours orders `0`건, positions `33`건, watchlists `0`건, open orders `0`건을 재확인하는 수준에서 종료했다.

## Validators

- `PATH=/usr/local/bin:$PATH python3 scripts/check-universe-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-16-1831-after-hours-autopilot.json`
- `PATH=/usr/local/bin:$PATH python3 scripts/check-mcp-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-16-1831-after-hours-autopilot.json`
- `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-06-16-1831-after-hours-autopilot.json`

## Artifacts

- Report: `wiki/current-runs/daily/2026-06-16-1831-after-hours-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-16-1831-after-hours-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-16-1831-after-hours-autopilot.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-06-16-1831-after-hours-autopilot-after-hours-gate-evaluation.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-16-1831-after-hours-autopilot-post-trade.json`
