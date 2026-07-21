# 2026-07-22-0831-after-hours-autopilot

## 요약

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Session: `after_hours`
- Policy profile: `after_hours_policy`
- Artifact tag: `after-hours`
- Review bucket: `after_hours_validation`
- Market date: `2026-07-21 EDT`
- Scheduler artifact date: `2026-07-22 KST`
- Paper mode: `ALPACA_PAPER_TRADE=true` 확인
- 결과: scheduler-owned `0831` core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. 이어서 live Alpaca MCP continuity로 regular market closed, account `ACTIVE`, positions `32`, open orders `0`, same-session after-hours submitted orders `0`, fills `0`를 다시 확인했다. 그러나 freshest executable IEX quote가 `NOK` `2026-07-21T20:59:59Z`로 약 `155.29`분 stale였고 `QQQ/SPY`는 spread pass에도 1주 notional cap을 넘었으며 나머지 executable set은 stale quote 또는 spread 또는 quote completeness gate를 통과하지 못해 `place_stock_order`는 호출하지 않았다.

## 사용한 스케줄러 프리플라이트

- Alpaca core: `wiki/evidence-store/sources/2026-07-22-0831-after-hours-autopilot-alpaca-core-preflight.json`
- Research MCP: `wiki/evidence-store/sources/2026-07-22-0831-after-hours-autopilot-research-mcp-preflight.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-07-22-0831-after-hours-autopilot-after-hours-gate-evaluation.json`
- Alpaca core preflight의 `first_blocking_gate=market_closed`는 after-hours 워크플로우에서 expected nonblocking으로 처리했다. 이번 cycle의 run id는 KST scheduler 파일명 `2026-07-22-0831-*`를 유지하지만, 실제 미국 장 판단과 continuity는 `2026-07-21 EDT` clock 기준으로 기록했다.

## Alpaca MCP 확인

- Regular market: closed. live `get_clock` 기준 `timestamp=2026-07-21T19:35:16.394453116-04:00`였다.
- Account: live `get_account_info` 기준 account `ACTIVE`, portfolio value `98602.01 USD`, cash `28610.95 USD`, buying power `297980.88 USD`였다.
- Positions / orders: live `get_all_positions` 기준 positions `32`건이었다. `get_orders(status=open)` 기준 open orders `0`건, `get_orders(status=all, after=2026-07-21T20:00:00Z)` 기준 same-session after-hours submitted orders `0`건이었다. `get_account_activities(activity_types=[FILL], after=2026-07-21T20:00:00Z)` 기준 same-session fills도 `0`건이었다.
- Quote boundary: live `get_stock_latest_quote(feed=iex)` 기준 freshest executable shortlist quote는 `NOK`였지만 약 `155.29`분 stale였다. `QQQ`는 약 `163.62`분 stale, `SPY`는 약 `214.93`분 stale였다. `feed=overnight` cross-check는 전 종목에서 `2026-07-21T08:00:00Z` 부근 older quote만 제공해 freshness gate를 다시 열지 못했다.

## 후보 평가

- `AVGO`: allowed sell side trim/exit를 우선 검토했지만 latestQuote `362.15/402.10`이 약 `215.24`분 stale였고 spread가 약 `10.45%`였다. held qty가 `1`주뿐이라 floor-size trim 후 잔여 최소수량 discipline도 만족하지 못했다.
- `SO`: latestQuote `89.08/99.75`가 약 `215.27`분 stale였고 spread가 약 `11.30%`였다. latest review backlog context상 `sell_metric_gap`도 남아 있어 decision-grade trim으로 승격되지 않았다.
- `QQQ`: benchmark fallback으로 검토했지만 latestQuote `708.17/708.24`가 약 `163.62`분 stale였다. spread 자체는 약 `0.01%`로 양호했지만 1주 ask `708.24 USD`가 after-hours per-order notional cap `493.01 USD`를 넘었다.
- `SPY`: benchmark fallback secondary 후보였지만 latestQuote `748.21/748.32`가 약 `214.93`분 stale였고 1주 ask `748.32 USD`도 same per-order cap을 넘었다.
- `NOK`: latestQuote `10.78/10.92`가 약 `155.29`분 stale였고 spread도 약 `1.29%`로 cap 초과였다. `review-due-index`의 `blocked_add_symbols=['NOK']`도 add path를 계속 막고 있었다.
- `WMT/SMH/MCD/NEE/GS/CVX`: 모두 stale quote였고 `WMT`는 ask `0`으로 quote completeness fail, 나머지는 spread가 after-hours cap을 초과했다. `SMH`와 `GS`는 per-order cap까지 동시에 초과했다.

## MCP 커버리지

- `alpaca`: PASS. scheduler-owned core preflight의 `market_closed`는 expected nonblocking으로 처리했고, same source-of-record account/positions/orders/asset rows와 live continuity로 after-hours submit boundary를 닫았다.
- `sec-edgar`: PASS. scheduler-owned research preflight reused.
- `alpha-vantage`: GAP. `NEWS_SENTIMENT`가 shortlisted symbols에 대해 candidate news item `0`건을 반환했다.
- `fred`: PASS. scheduler-owned research preflight reused.
- `firecrawl`: PASS. scheduler-owned research preflight reused.
- `yahoo-finance`: PASS. scheduler-owned research preflight reused.
- Strict MCP gate는 `sec-edgar/fred/firecrawl/yahoo-finance` 4개 research confirmation을 유지했으므로 PASS였다.

## Gate 결과

| Gate | Status |
| --- | --- |
| alpaca_paper_mode | pass |
| regular_market_open | pass_regular_market_closed |
| extended_hours_session | pass |
| alpaca_core_account_clock_position_order_quote_spread | pass_source_of_record_plus_live_continuity |
| after_hours_policy_profile | pass |
| separate_after_hours_order_budget | pass_zero_of_two_submitted |
| universe_strict | PASS |
| mcp_tiered_strict | PASS |
| risk_policy | PASS with expected `orders is empty` warning |
| fresh_quote | FAIL at submit boundary for all executable candidates |
| spread_within_after_hours_policy | FAIL for every executable candidate except `QQQ/SPY` spread-only pass; both still failed freshness and per-order cap |
| whole_share_day_limit_extended_hours_order | fail_no_eligible_order_survived_hard_gates |
| immediate_reconcile_and_cancel_or_lifecycle_record | pass_no_submit |

## Submit And Reconcile

- `place_stock_order`는 호출하지 않았다. 신규 `client_order_id`, retry, alternate client order id도 없었다.
- Separate after-hours session budget은 `0/2`로 열려 있었지만 sell side는 `AVGO/SO`가 fresh quote·spread·minimum remaining qty·sell metric gate에 막혔고, buy side shortlist는 모두 freshness 또는 spread 또는 quote completeness 또는 per-order cap 또는 validation lifecycle blocker를 통과하지 못했다.
- 이번 cycle의 reconciliation은 live continuity 기준 `submit_attempted=false`, `reconciled=true`, `open orders=0`, `same-session after-hours fills=0`로 닫았다.

## 산출물

- Manifest: `wiki/evidence-store/run-manifests/2026-07-22-0831-after-hours-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-07-22-0831-after-hours-autopilot.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-07-22-0831-after-hours-autopilot-after-hours-gate-evaluation.json`
- Post-trade check: `wiki/trade-ledger/positions/2026-07-22-0831-after-hours-autopilot-post-trade.json`
- Report: `wiki/current-runs/daily/2026-07-22-0831-after-hours-autopilot.md`
