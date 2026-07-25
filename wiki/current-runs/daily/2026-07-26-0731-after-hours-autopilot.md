# 2026-07-26-0731-after-hours-autopilot

## 요약

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Session: `after_hours`
- Policy profile: `after_hours_policy`
- Artifact tag: `after-hours`
- Review bucket: `after_hours_validation`
- Actual runtime date: `Saturday, July 25, 2026`
- Market date evaluated: `Friday, July 24, 2026 EDT`
- Scheduler file label used: `2026-07-26-0731-` (`Asia/Seoul` future-labeled artifact path; actual current runtime date for this run was `Saturday, July 25, 2026`)
- Paper mode: `ALPACA_PAPER_TRADE=true` 확인
- 결과: scheduler-owned `2026-07-26-0731-` core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. 현재 시점 live Alpaca continuity도 `2026-07-25T22:33:55Z` 기준 regular market closed, account `ACTIVE`, positions `31`, watchlists `0`, same-session after-hours orders `0`, same-session fills `0`, prior after-hours `client_order_id=ah-20260723-2151-sell-nok-01` `filled`를 재확인했다. 다만 user requirement에 따라 submit boundary quote/spread는 scheduler-owned `2026-07-26-0731-` source-of-record row에 고정했고, executable 후보 전부가 stale, one-sided, spread fail, 또는 per-order cap fail이라 신규 `place_stock_order` 없이 reconcile-only run으로 종료했다.

## 사용한 스케줄러 프리플라이트

- Alpaca core: `wiki/evidence-store/sources/2026-07-26-0731-after-hours-autopilot-alpaca-core-preflight.json`
- Research MCP: `wiki/evidence-store/sources/2026-07-26-0731-after-hours-autopilot-research-mcp-preflight.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-07-26-0731-after-hours-autopilot-after-hours-gate-evaluation.json`
- Alpaca core preflight의 `first_blocking_gate=market_closed`는 after-hours 워크플로우에서 expected nonblocking으로 처리했다.

## Alpaca MCP 확인

- Source-of-record account / positions / open orders / asset / quote / spread rows는 scheduler-owned future-labeled artifact path `2026-07-26-0731-` Alpaca core preflight를 사용했다.
- Current-turn continuity는 Alpaca MCP `get_clock`, `get_account_info`, `get_all_positions`, `get_watchlists`, `get_orders(status=open)`, `get_orders(status=all, after=2026-07-24T20:00:00Z)`, `get_account_activities(activity_types=[FILL], after=2026-07-24T20:00:00Z)`, `get_order_by_client_id(ah-20260723-2151-sell-nok-01)`로 닫았다.
- continuity 기준 `get_clock().is_open=false` at `2026-07-25T18:33:55.989541337-04:00`, account `ACTIVE`, positions `31`, watchlists `0`, same-session after-hours orders `0`, same-session after-hours fills `0`, prior after-hours `ah-20260723-2151-sell-nok-01`는 `filled_avg_price=9.67 USD` `filled` 상태로 유지됐다.
- live account / positions continuity는 drift 확인 용도로만 사용했고, submit boundary quote/spread는 scheduler-owned `2026-07-26-0731-` row를 그대로 유지했다.

## 후보 평가

- `NOK` sell/trim: source-of-record quote `9.05/9.10`, quote age 약 `1539.44분`, spread 약 `0.551%`로 stale + spread hard gate fail이다.
- `SO` sell/trim: source-of-record quote `89.30/0.00`, quote age 약 `1593.90분`, ask 누락이라 one-sided + stale hard gate fail이다.
- `QQQ`: source-of-record spread 자체는 `0.0132%`로 좁았지만 quote age가 약 `1581.88분`으로 stale이고 1주 ask 기준 `after_hours_policy.max_notional_pct_per_order=0.005` cap도 넘는다.
- `WMT`와 `SMH`는 source-of-record quote가 one-sided이고 각각 약 `1593.91분`, `1593.87분` stale이다.
- `MCD/NEE/CVX/GS/SPY`는 source-of-record 기준 stale + spread 또는 cap fail이라 executable after-hours path를 만들지 못했다. current-turn Alpaca continuity는 refresh submit 근거로 승격하지 않았고, first blocking gate는 계속 `fresh_quote`였다.

## Submit And Reconcile

- Submitted order this cycle: 없음
- Pre-submit gate summary: 신규 `place_stock_order` 호출이 없어서 작성하지 않았다. submit branch 진입 전 `fresh_quote` 게이트가 fail했다.
- Reconciled same-session client_order_id: 없음. `2026-07-26-0731-` source-of-record preflight `orders_submitted=0`과 current-turn continuity 기준 이번 after-hours 세션에 새 주문 경로는 열리지 않았다.
- Retry discipline: alternate `client_order_id`는 사용하지 않았다.

## Artifacts

- Report: `wiki/current-runs/daily/2026-07-26-0731-after-hours-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-07-26-0731-after-hours-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-07-26-0731-after-hours-autopilot.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-07-26-0731-after-hours-autopilot-after-hours-gate-evaluation.json`
- Post-trade check: `wiki/trade-ledger/positions/2026-07-26-0731-after-hours-autopilot-post-trade.json`
- Prompt: `wiki/evidence-store/sources/2026-07-26-0731-after-hours-autopilot-prompt.txt`
- Deterministic submit summary: `wiki/evidence-store/sources/2026-07-26-0731-after-hours-autopilot-deterministic-submit.json`

## Validators

- `python3 scripts/check-universe-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-07-26-0731-after-hours-autopilot.json`
- `python3 scripts/check-mcp-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-07-26-0731-after-hours-autopilot.json`
- `python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-07-26-0731-after-hours-autopilot.json`
- 실제 실행: `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-07-26-0731-after-hours-autopilot.json`
- 결과: universe strict PASS, MCP strict PASS, risk policy PASS with warning `orders is empty`
