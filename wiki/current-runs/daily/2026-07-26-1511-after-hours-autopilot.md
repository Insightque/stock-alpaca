# 2026-07-26-1511-after-hours-autopilot

## 요약

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Session: `after_hours`
- Policy profile: `after_hours_policy`
- Artifact tag: `after-hours`
- Review bucket: `after_hours_validation`
- Actual runtime date: `Sunday, July 26, 2026`
- Alpaca continuity date: `Sunday, July 26, 2026`
- Market date evaluated: `Friday, July 24, 2026 EDT`
- Scheduler file label used: `2026-07-26-1511-` (`Asia/Seoul` scheduler-owned artifact path)
- Paper mode: `ALPACA_PAPER_TRADE=true` 확인
- 결과: scheduler-owned `2026-07-26-1511-` core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. live Alpaca continuity에서는 `get_account_info().status=ACTIVE`, `get_all_positions() count=31`, `get_watchlists()=[]`, `get_stock_latest_quote(SO,WMT,MCD,QQQ,SPY,SMH,NOK,NEE,CVX,GS, feed=iex)`가 scheduler-owned submit-boundary quote와 동일한 stale/one-sided 상태를 유지했고 `get_order_by_client_id(ah-20260723-2151-sell-nok-01)=filled`를 재확인했다. same-session fills는 scheduler-owned recent-activities preflight row 기준 `0`으로 유지했고 direct `get_account_activities_by_type(FILL, after=2026-07-24T20:00:00Z)` 재시도 2회는 모두 `user cancelled MCP tool call`로 돌아와 source-of-record를 유지했다. submit boundary quote/spread는 user requirement에 따라 scheduler-owned `2026-07-26-1511-` row에 고정했고 executable 후보 전부가 stale, one-sided, spread fail, 또는 per-order cap fail이라 신규 `place_stock_order` 없이 reconcile-only run으로 종료했다.

## 사용한 스케줄러 프리플라이트

- Alpaca core: `wiki/evidence-store/sources/2026-07-26-1511-after-hours-autopilot-alpaca-core-preflight.json`
- Research MCP: `wiki/evidence-store/sources/2026-07-26-1511-after-hours-autopilot-research-mcp-preflight.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-07-26-1511-after-hours-autopilot-after-hours-gate-evaluation.json`
- Alpaca core preflight의 `first_blocking_gate=market_closed`는 after-hours 워크플로우에서 expected nonblocking으로 처리했다.

## Alpaca MCP 확인

- Source-of-record account / positions / open orders / asset / quote / spread rows는 scheduler-owned `2026-07-26-1511-` Alpaca core preflight를 사용했다.
- Current-turn continuity는 Alpaca MCP `get_account_info`, `get_all_positions`, `get_watchlists`, `get_stock_latest_quote(symbols=SO,WMT,MCD,QQQ,SPY,SMH,NOK,NEE,CVX,GS, feed=iex)`, `get_order_by_client_id(ah-20260723-2151-sell-nok-01)`로 닫았고 `get_account_activities_by_type(FILL, after=2026-07-24T20:00:00Z)`는 두 번 모두 `user cancelled MCP tool call`이라 same-session fill count는 scheduler-owned preflight row를 유지했다.
- continuity 기준 account `ACTIVE`, positions `31`, watchlists `0`, scheduler-owned source-of-record open orders `0`, same-session after-hours orders `0`, same-session after-hours fills `0`, prior after-hours `ah-20260723-2151-sell-nok-01`는 `filled_avg_price=9.67 USD` `filled` 상태로 유지됐다.
- submit boundary quote/spread는 live continuity로 승격하지 않았고 scheduler-owned `2026-07-26-1511-` row를 그대로 유지했다.

## 후보 평가

- `SO` sell/trim: source-of-record quote `89.30/0.00`, quote age 약 `2054.05`분, ask 누락이라 one-sided + stale hard gate fail이다.
- `WMT`와 `SMH`는 source-of-record quote가 one-sided이고 각각 약 `2054.06`분, `2054.02`분 stale이다.
- `NOK` sell/trim: source-of-record quote `9.05/9.10`, quote age 약 `1999.59`분, spread 약 `0.5525%`로 stale + spread hard gate fail이다.
- `QQQ`는 source-of-record spread 자체는 `0.0132%`로 좁았지만 quote age가 약 `2042.03`분으로 stale이고 1주 ask 기준 `after_hours_policy.max_notional_pct_per_order=0.005` cap도 넘는다.
- `MCD/SPY/NEE/CVX/GS`도 source-of-record 기준 stale + spread 또는 cap fail이라 executable after-hours path를 만들지 못했다. first blocking gate는 계속 `fresh_quote`였다.

## Submit And Reconcile

- Submitted order this cycle: 없음
- Pre-submit gate summary: 신규 `place_stock_order` 호출이 없어서 작성하지 않았다. submit branch 진입 전 `fresh_quote` 게이트가 fail했다.
- Reconciled same-session client_order_id: 없음. `2026-07-26-1511-` source-of-record preflight `orders_submitted=0`과 direct Alpaca MCP continuity 기준 이번 after-hours 세션에 새 주문 경로는 열리지 않았다.
- Retry discipline: alternate `client_order_id`는 사용하지 않았다.

## Artifacts

- Report: `wiki/current-runs/daily/2026-07-26-1511-after-hours-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-07-26-1511-after-hours-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-07-26-1511-after-hours-autopilot.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-07-26-1511-after-hours-autopilot-after-hours-gate-evaluation.json`
- Post-trade check: `wiki/trade-ledger/positions/2026-07-26-1511-after-hours-autopilot-post-trade.json`
- Prompt: `wiki/evidence-store/sources/2026-07-26-1511-after-hours-autopilot-prompt.txt`
- Deterministic submit summary: `wiki/evidence-store/sources/2026-07-26-1511-after-hours-autopilot-deterministic-submit.json`

## Validators

- `python3 scripts/check-universe-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-07-26-1511-after-hours-autopilot.json`
- `python3 scripts/check-mcp-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-07-26-1511-after-hours-autopilot.json`
- `PYTHONPATH=/private/tmp/yamlshim /usr/local/bin/python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-07-26-1511-after-hours-autopilot.json`
