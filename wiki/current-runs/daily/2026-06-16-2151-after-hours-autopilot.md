# 2026-06-16-2151-after-hours-autopilot

## 요약

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Session: `after_hours`
- Policy profile: `after_hours_policy`
- Artifact tag: `after-hours`
- Review bucket: `after_hours_validation`
- Paper mode: `ALPACA_PAPER_TRADE=true` 확인
- 결과: scheduler-owned `2151` core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. live continuity로 `get_clock/get_account_info/get_all_positions/get_watchlists/get_orders(status=open)/get_orders(status=all, after=2026-06-15T20:00:00Z)/get_account_activities(activity_types=[FILL], after=2026-06-15T20:00:00Z)/get_stock_latest_quote(feed=iex)/get_stock_snapshot(feed=iex)`를 다시 열었다. `GOOGL/NOK`는 fresh IEX quote까지 확보했지만 `GOOGL`은 spread cap과 same-session duplicate/review backlog, `NOK`는 `blocked_add_symbols=['NOK']`와 review backlog throttle에 막혔고, 나머지 shortlist는 freshness·spread·notional cap을 통과하지 못해 executable after-hours order가 남지 않았다.

## 사용한 스케줄러 프리플라이트

- Alpaca core: `wiki/evidence-store/sources/2026-06-16-2151-after-hours-autopilot-alpaca-core-preflight.json`
- Research MCP: `wiki/evidence-store/sources/2026-06-16-2151-after-hours-autopilot-research-mcp-preflight.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-06-16-2151-after-hours-autopilot-after-hours-gate-evaluation.json`
- Alpaca core preflight의 `first_blocking_gate=market_closed`는 after-hours 워크플로우에서 expected nonblocking으로 처리했다. 이번 `2151` cycle은 scheduler-owned passing rows로 account/positions/open-order/recent-activity/asset/quote baseline을 유지했고, live continuity로 clock/account/positions/watchlists/open orders/order history/fills/IEX quote/snapshot boundary를 다시 확인했다.

## Alpaca MCP 확인

- Regular market: closed. live `get_clock` 기준 `timestamp=2026-06-16T08:52:53.694057015-04:00`였다.
- Account: live `get_account_info` 기준 account `ACTIVE`, portfolio value `102314.19 USD`, cash `29836.34 USD`, buying power `305702.92 USD`였다.
- Positions / orders: live `get_all_positions` 기준 positions `33`건, live `get_watchlists` 기준 watchlists `0`건이었다. live `get_orders(status=open)`와 `get_orders(status=all, after=2026-06-15T20:00:00Z)` 기준 open orders `0`건, same-session after-hours submitted orders `0`건이었다. live `get_account_activities(activity_types=[FILL], after=2026-06-15T20:00:00Z)` 기준 same-session after-hours fills도 `0`건이었다.
- Quote boundary: live `get_stock_latest_quote(feed=iex)`와 `get_stock_snapshot(feed=iex)` 기준 `GOOGL 367.54/370.15`, `NOK 14.72/14.73`, `QQQ 742.77/743.21`, `SPY 754.23/754.40`, `RGTI 22.73/22.81`, `SMH 629.42/662.96`, `TSLA 391.40/410.95`, `SLB 53.00/56.73`를 사용했다. `GOOGL/NOK`만 각각 약 `2.19`분, `2.52`분으로 fresh cap 안쪽이었고, 나머지는 `16.60`분 이상 stale였다.

## 후보 평가

- `RGTI`: sell-first trim 후보였지만 latestQuote `22.73/22.81`가 약 `1002.95`분 stale였고, `2026-06-15 09:41 ET` regular-session trim fills에 따른 same-session duplicate sell discipline이 남았다.
- `GOOGL`: existing actionable holding add fallback으로 승격 가능했지만 latestQuote `367.54/370.15` spread가 약 `0.7076%`로 after-hours cap `0.25%`를 넘었다. `2026-06-15 14:58 ET` same-session duplicate buy와 `pending_1d_count=18`도 동시에 남았다.
- `NOK`: latestQuote `14.72/14.73`는 fresh하고 spread도 약 `0.0679%`로 cap 안쪽이었지만 `review-due-index`의 `blocked_add_symbols=['NOK']`와 `pending_1d_count=18` 때문에 add path가 닫혔다.
- `QQQ/SPY`: benchmark fallback quote는 있었지만 각각 약 `16.60`분, `16.63`분 stale였고 1주 ask `743.21 / 754.40 USD`가 after-hours per-order cap `511.57 USD`를 넘었다.
- `SMH`: stale quote였고 spread 약 `5.1904%`, 1주 ask `662.96 USD` 모두 after-hours gates를 넘지 못했다.
- `TSLA`: stale quote, spread 약 `4.8732%`, watch-only thesis 때문에 actionable fallback으로 승격되지 않았다.
- `SLB`: stale quote, spread 약 `6.7985%`, `2026-06-15 12:41 ET` same-session duplicate buy discipline 때문에 submit path가 열리지 않았다.

## MCP 커버리지

- `alpaca`: PASS. scheduler-owned `2151` core preflight를 source-of-record로 사용했고 live continuity로 clock/account/positions/watchlists/open-order/order-history/fill/IEX quote/snapshot boundary를 재확인했다.
- `sec-edgar`: PASS. scheduler-owned research preflight reused.
- `alpha-vantage`: FAILED. one-call-per-hour throttle 때문에 이번 cycle은 provider call을 건너뛰었고 `gap_category=provider_error`로 기록됐다.
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
| alpaca_core_account_clock_position_order_quote_spread | pass_scheduler_preflight_and_live_continuity |
| after_hours_policy_profile | pass |
| separate_after_hours_order_budget | pass_zero_of_two_submitted |
| universe_strict | PASS |
| mcp_tiered_strict | PASS |
| risk_policy | PASS with expected `orders is empty` warning |
| fresh_quote | FAIL for `QQQ/SPY/RGTI/TSLA/SMH/SLB`; `GOOGL/NOK` only fresh |
| spread_within_after_hours_policy | FAIL for `GOOGL/SMH/SLB/TSLA`; `NOK` only spread-pass actionable buy but add-block/backlog remained |
| whole_share_day_limit_extended_hours_order | fail_no_eligible_order_survived_duplicate_backlog_add_block_spread_freshness_or_notional_caps |
| immediate_reconcile_and_cancel_or_lifecycle_record | pass_no_submit |

## Submit And Reconcile

- `place_stock_order`는 호출하지 않았다. 신규 `client_order_id`, retry, alternate client id도 없었다.
- Separate after-hours session budget은 `0/2`로 열려 있었지만 eligible sell 후보 `RGTI`는 same-session duplicate sell discipline과 stale quote에 막혔고, buy path는 `GOOGL` spread cap, `NOK` add-block/review backlog, `QQQ/SPY/SMH` notional/freshness, `TSLA/SLB` spread 또는 watch-only thesis 때문에 executable order가 남지 않았다.
- 이번 cycle의 reconciliation은 live continuity 기준 positions `33`건, watchlists `0`건, account `ACTIVE`, open orders `0`건, same-session after-hours orders `0`건, fills `0`건을 재확인하는 수준에서 종료했다.

## Validators

- `PATH=/usr/local/bin:$PATH python3 scripts/check-universe-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-16-2151-after-hours-autopilot.json`
- `PATH=/usr/local/bin:$PATH python3 scripts/check-mcp-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-16-2151-after-hours-autopilot.json`
- `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-06-16-2151-after-hours-autopilot.json`

## Artifacts

- Report: `wiki/current-runs/daily/2026-06-16-2151-after-hours-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-16-2151-after-hours-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-16-2151-after-hours-autopilot.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-06-16-2151-after-hours-autopilot-after-hours-gate-evaluation.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-16-2151-after-hours-autopilot-post-trade.json`
