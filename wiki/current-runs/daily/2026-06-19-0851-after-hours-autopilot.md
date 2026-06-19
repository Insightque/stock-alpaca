# 2026-06-19-0851-after-hours-autopilot

## 요약

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Session: `after_hours`
- Policy profile: `after_hours_policy`
- Artifact tag: `after-hours`
- Review bucket: `after_hours_validation`
- Paper mode: `ALPACA_PAPER_TRADE=true` 확인
- 결과: scheduler-owned `0851` core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. 같은 preflight의 passing account/positions/orders/asset/quote/spread rows를 유지한 상태에서 submit path를 평가했지만, executable shortlist 전체가 stale quote 또는 spread 또는 per-order cap 또는 validation lifecycle gate를 통과하지 못해 `place_stock_order`는 호출하지 않았다.

## 사용한 스케줄러 프리플라이트

- Alpaca core: `wiki/evidence-store/sources/2026-06-19-0851-after-hours-autopilot-alpaca-core-preflight.json`
- Research MCP: `wiki/evidence-store/sources/2026-06-19-0851-after-hours-autopilot-research-mcp-preflight.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-06-19-0851-after-hours-autopilot-after-hours-gate-evaluation.json`
- Alpaca core preflight의 `first_blocking_gate=market_closed`는 after-hours 워크플로우에서 expected nonblocking으로 처리했다. 이번 `0851` cycle은 same source-of-record 기준 regular market closed, account `ACTIVE`, positions `32`, watchlists `0`, open orders `0`, same-session after-hours submitted orders `0`, same-session fills `0`를 유지했다.

## Alpaca MCP 확인

- Regular market: closed. scheduler-owned `get_clock` 기준 `timestamp=2026-06-18T19:51:10.277663305-04:00`였다.
- Account: source-of-record `get_account_info` 기준 account `ACTIVE`, portfolio value `101642.92 USD`, cash `28610.97 USD`, buying power `303703.96 USD`였다.
- Positions / orders: source-of-record `get_all_positions` 기준 positions `32`건, `get_watchlists` 기준 watchlists `0`건이었다. `get_orders(status=open)` 기준 open orders `0`건, `get_account_activities(activity_types=[FILL])`에서 `2026-06-18T20:00:00Z` 이후 fill `0`건이었다.
- Quote boundary: scheduler-owned `get_stock_latest_quote(feed=iex)` 기준 freshest `AVGO`도 약 `175.62`분 stale였고 `QQQ`는 `189.83`분 stale였다.

## 후보 평가

- `AVGO`: allowed sell side trim/exit를 우선 검토했지만 latestQuote `411.01/495.48`가 약 `175.62`분 stale였고 spread가 약 `18.64%`로 after-hours cap `0.25%`를 크게 넘었다. 추가로 held qty가 `1`주뿐이라 floor-size trim 후 잔여 최소수량 discipline도 만족하지 못했다.
- `SO`: latestQuote `89.28/98.16`가 약 `231.47`분 stale였고 spread가 약 `9.47%`였다. latest regular-session source-of-record에서도 `sell_metric_gap`이 남아 decision-grade trim으로 승격되지 않았다.
- `QQQ`: benchmark fallback으로 검토했지만 latestQuote `740.34/740.47`가 약 `189.83`분 stale였다. spread 자체는 낮았지만 1주 ask `740.47 USD`가 after-hours per-order notional cap `508.21 USD`를 넘었다.
- `NOK`: latestQuote `13.51/13.57`가 약 `207.23`분 stale였고 spread도 약 `0.44%`로 cap 초과였다. `review-due-index`의 `blocked_add_symbols=['NOK']`, `pending_1d_count=17`도 add path를 계속 막고 있었다.
- `WMT/SMH/MCD/NEE/GS/CVX`: 모두 stale quote였고 spread가 after-hours cap을 초과했다. `GS`와 `SMH`는 per-order cap까지 동시에 초과했다.

## MCP 커버리지

- `alpaca`: PASS. scheduler-owned core preflight의 `market_closed`는 expected nonblocking으로 처리했고, 같은 source-of-record account/positions/orders/asset/quote/spread rows로 after-hours submit boundary를 닫았다.
- `sec-edgar`: PASS. scheduler-owned research preflight reused.
- `alpha-vantage`: GAP. `NEWS_SENTIMENT`가 shortlist에 대한 candidate news item `0`건을 반환했다.
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
| alpaca_core_account_clock_position_order_quote_spread | pass_source_of_record |
| after_hours_policy_profile | pass |
| separate_after_hours_order_budget | pass_zero_of_two_submitted |
| universe_strict | PASS |
| mcp_tiered_strict | PASS |
| risk_policy | PASS with expected `orders is empty` warning |
| fresh_quote | FAIL at submit boundary for all executable candidates |
| spread_within_after_hours_policy | FAIL for all executable candidates except `QQQ`, which still failed freshness and per-order cap |
| whole_share_day_limit_extended_hours_order | fail_no_eligible_order_survived_hard_gates |
| immediate_reconcile_and_cancel_or_lifecycle_record | pass_no_submit |

## Submit And Reconcile

- `place_stock_order`는 호출하지 않았다. 신규 `client_order_id`, retry, alternate client order id도 없었다.
- Separate after-hours session budget은 `0/2`로 열려 있었지만, sell side는 `AVGO/SO`가 fresh quote·spread·minimum remaining qty·sell metric gate에 막혔고, buy side shortlist는 모두 freshness 또는 spread 또는 per-order cap 또는 validation lifecycle blocker를 통과하지 못했다.
- 이번 cycle의 reconciliation은 source-of-record 기준 positions `32`건, account `ACTIVE`, open orders `0`건, same-session after-hours submitted orders `0`건, same-session fills `0`건을 재확인하는 수준에서 종료했다.

## Validators

- `PATH=/usr/local/bin:$PATH python3 scripts/check-universe-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-19-0851-after-hours-autopilot.json` PASS
- `PATH=/usr/local/bin:$PATH python3 scripts/check-mcp-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-19-0851-after-hours-autopilot.json` PASS
- `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-06-19-0851-after-hours-autopilot.json` PASS with expected `orders is empty` warning

## Artifacts

- Report: `wiki/current-runs/daily/2026-06-19-0851-after-hours-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-19-0851-after-hours-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-19-0851-after-hours-autopilot.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-06-19-0851-after-hours-autopilot-after-hours-gate-evaluation.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-19-0851-after-hours-autopilot-post-trade.json`
