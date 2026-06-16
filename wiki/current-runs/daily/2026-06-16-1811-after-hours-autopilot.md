# 2026-06-16-1811-after-hours-autopilot

## 요약

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Session: `after_hours`
- Policy profile: `after_hours_policy`
- Artifact tag: `after-hours`
- Review bucket: `after_hours_validation`
- Paper mode: `ALPACA_PAPER_TRADE=true` 확인
- 결과: scheduler-owned `1811` core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. direct Alpaca MCP continuity는 `overnight` feed에서 `QQQ/RGTI/NOK/TSLA/SMH/SLB/AVGO/GE/SPY/MSFT/PFE` quote stack을 2026-06-16 18:13 KST에 재확인했다. 그러나 최신 overnight quote가 모두 약 `73.44`분 stale로 남아 `fresh_quote` hard gate가 닫혀 있었고, sell-first 후보는 `AVGO/RGTI/PFE` duplicate sell discipline과 spread fail이 겹쳤으며, buy fallback은 `review_backlog_pending_1d_count=18`, `blocked_add_symbols=['NOK']`, `QQQ/SPY/SMH` after-hours per-order cap, `MSFT` same-day duplicate buy, `TSLA` watch-only thesis, `GE/SLB/NOK` spread cap 때문에 executable after-hours order가 남지 않았다.

## 사용한 스케줄러 프리플라이트

- Alpaca core: `wiki/evidence-store/sources/2026-06-16-1811-after-hours-autopilot-alpaca-core-preflight.json`
- Research MCP: `wiki/evidence-store/sources/2026-06-16-1811-after-hours-autopilot-research-mcp-preflight.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-06-16-1811-after-hours-autopilot-after-hours-gate-evaluation.json`
- Alpaca core preflight의 `first_blocking_gate=market_closed`는 after-hours 워크플로우에서 expected nonblocking으로 처리했다. 이번 `1811` preflight는 passing account/positions/open-order/quote rows를 유지했고, direct continuity는 refreshed overnight quote stack과 same-session order absence만 재확인했다.

## Alpaca MCP 확인

- Regular market: closed. direct `get_clock` 기준 `timestamp=2026-06-16T05:13:26.59866916-04:00`.
- Account: direct `get_account_info` 기준 account `ACTIVE`, portfolio value `102694.22 USD`, cash `29836.34 USD`, buying power `306564.71 USD`였다.
- Positions / watchlists / orders: direct `get_all_positions` 기준 positions `33`건, direct `get_watchlists` 기준 watchlists `0`건, direct `get_orders(status=open)` 기준 open orders `0`건이었다.
- Same-session after-hours orders/fills: direct `get_orders(status=all, after=2026-06-15T20:00:00Z)` 기준 same-session after-hours submitted orders `0`건, direct `get_account_activities(activity_types=[FILL], after=2026-06-15T20:00:00Z)` 기준 same-session after-hours fills `0`건이었다. 따라서 `risk_inputs.after_hours_new_orders_submitted_today=0`, session cap `0/2`를 유지했다.
- Quote boundary: direct `get_stock_latest_quote(feed=overnight)` / `get_stock_snapshot(feed=overnight)` 기준 `QQQ 719.66/799.94`, `RGTI 21.02/23.11`, `NOK 14.92/15.49`, `TSLA 405.19/419.07`, `SMH 644.69/645.98`, `SLB 44.99/56.96`, `AVGO 385.18/397.28`, `GE 316.70/349.71`, `SPY 753.72/754.96`, `MSFT 399.97/400.09`, `PFE 26.04/26.82`를 재확인했다. 다만 quote timestamp가 모두 `2026-06-16T08:00:00Z` 근처에 머물러 decision 시점 기준 약 `73.44`분 stale였고, spread cap `0.25%`는 `MSFT/SMH/SPY`만 PASS, 나머지는 FAIL이었다.

## 후보 평가

- `AVGO`: overnight quote `385.18/397.28`, spread 약 `3.0928%`와 stale quote가 동시에 fail이며 `2026-06-15 11:18 ET` regular-session trim fill 이후 `duplicate_symbol_side_same_day`도 유지됐다.
- `RGTI`: overnight quote `21.02/23.11`, spread 약 `9.4720%`, stale quote, `2026-06-15 09:41 ET` filled sell에 따른 duplicate sell discipline이 모두 겹쳤다.
- `PFE`: repeated weak-review trim precedent는 유지됐지만 overnight quote `26.04/26.82`, spread 약 `2.9512%`, stale quote, `2026-06-15 15:59 ET` regular-session trim fill에 따른 duplicate sell discipline 때문에 추가 sell path가 열리지 않았다.
- `MSFT`: overnight quote `399.97/400.09`, spread 약 `0.0300%`, 1주 ask `400.09 USD`로 execution quality 자체는 충분했지만 quote가 stale했고 `review_backlog_pending_1d_count=18`, `2026-06-15 14:39 ET` regular-session buy가 신규 buy path를 계속 차단했다.
- `NOK`: overnight quote `14.92/15.49`, 1주 notional은 cap 이내였지만 `review-due-index`의 `blocked_add_symbols=['NOK']`, review backlog throttle, stale quote, spread 약 `3.7488%` fail이 동시에 남았다.
- `QQQ/SPY`: benchmark fallback quote는 확보됐지만 stale quote가 선차단으로 남았고, 1주 ask `799.94/754.96 USD`가 after-hours per-order cap 약 `513.47 USD`를 넘어 buy path가 열리지 않았다.
- `SMH`: stale quote가 남았고 1주 ask `645.98 USD`가 per-order cap을 넘었다. spread 약 `0.1999%`는 cap 이내였지만 notional gate와 backlog throttle이 막았다.
- `TSLA`: stale quote, spread 약 `3.3679%`, watch-only thesis, review backlog throttle이 함께 남아 actionable fallback으로 승격되지 않았다.
- `SLB/GE`: stale quote에 더해 `SLB` spread 약 `23.4821%`, `GE` spread 약 `9.9068%`가 계속 fail이었다.

## MCP 커버리지

- `alpaca`: PASS. scheduler-owned `1811` core preflight passing rows와 direct continuity check를 함께 사용했다.
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
| alpaca_core_account_clock_position_order_quote_spread | pass_scheduler_preflight_plus_runtime_overnight_continuity |
| after_hours_policy_profile | pass |
| separate_after_hours_order_budget | pass_zero_of_two_submitted |
| universe_strict | PASS |
| mcp_tiered_strict | PASS |
| risk_policy | PASS with expected `orders is empty` warning |
| fresh_quote | FAIL: latest runtime overnight quotes were about `73.44` minutes old |
| spread_within_after_hours_policy | pass for `MSFT/SMH/SPY`, fail for `AVGO/GE/NOK/PFE/QQQ/RGTI/SLB/TSLA` |
| whole_share_day_limit_extended_hours_order | fail_no_eligible_order_survived_fresh_quote_duplicate_sells_buy_backlog_add_block_watch_only_or_notional_or_quote_spread_caps |
| immediate_reconcile_and_cancel_or_lifecycle_record | pass_no_submit |

## Submit And Reconcile

- `place_stock_order`는 호출하지 않았다. 신규 `client_order_id`, retry, alternate client id도 없었다.
- Separate after-hours session budget은 `0/2`로 열려 있었지만 fresh-quote hard gate가 닫혀 있었고, stale quote를 통과시켜도 실행 가능한 sell은 duplicate discipline 또는 spread cap에 막히고 buy는 review backlog throttle, add-block, after-hours per-order cap, watch-only thesis 때문에 submit path가 열리지 않았다.
- 이번 cycle의 reconciliation은 scheduler-owned preflight rows와 direct Alpaca MCP continuity check 기준 same-session after-hours orders `0`건, fills `0`건, positions `33`건, watchlists `0`건, open orders `0`건을 재확인하는 수준에서 종료했다.

## Validators

- `PATH=/usr/local/bin:$PATH python3 scripts/check-universe-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-16-1811-after-hours-autopilot.json`
- `PATH=/usr/local/bin:$PATH python3 scripts/check-mcp-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-16-1811-after-hours-autopilot.json`
- `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-06-16-1811-after-hours-autopilot.json`

## Artifacts

- Report: `wiki/current-runs/daily/2026-06-16-1811-after-hours-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-16-1811-after-hours-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-16-1811-after-hours-autopilot.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-06-16-1811-after-hours-autopilot-after-hours-gate-evaluation.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-16-1811-after-hours-autopilot-post-trade.json`
