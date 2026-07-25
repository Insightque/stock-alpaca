# 2026-07-25-1511-after-hours-autopilot

## 요약

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Session: `after_hours`
- Policy profile: `after_hours_policy`
- Artifact tag: `after-hours`
- Review bucket: `after_hours_validation`
- Market date evaluated: `Friday, July 24, 2026 EDT`
- Scheduler file label used: `2026-07-25-1511` (`Asia/Seoul` next-day file label; actual market date anchor for this run is `Friday, July 24, 2026 EDT`)
- Paper mode: `ALPACA_PAPER_TRADE=true` 확인
- 결과: scheduler-owned future-labeled KST artifact path `2026-07-25-1511` core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. 같은 `2026-07-25-1511` preflight는 passing account/positions/open-orders/asset/quote/spread rows와 `orders_submitted=0`을 제공했다. Post-preflight Alpaca MCP continuity readback에서도 account `ACTIVE`, positions `31`, watchlists `0`, open orders `0`, same-session after-hours orders/fills `0/0`을 재확인했다. 다만 이번 scheduled run은 user requirement에 따라 `2026-07-25-1511` source-of-record quote/spread rows를 submit boundary로 유지했고, 모든 executable 후보가 stale, one-sided, spread fail, 또는 per-order cap fail로 남아 신규 `place_stock_order` 없이 reconcile-only run으로 종료했다.

## 사용한 스케줄러 프리플라이트

- Alpaca core: `wiki/evidence-store/sources/2026-07-25-1511-after-hours-autopilot-alpaca-core-preflight.json`
- Research MCP: `wiki/evidence-store/sources/2026-07-25-1511-after-hours-autopilot-research-mcp-preflight.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-07-25-1511-after-hours-autopilot-after-hours-gate-evaluation.json`
- Alpaca core preflight의 `first_blocking_gate=market_closed`는 after-hours 워크플로우에서 expected nonblocking으로 처리했다.

## Alpaca MCP 확인

- Source-of-record account / positions / open orders / asset / quote / spread rows는 scheduler-owned future-labeled KST artifact path `2026-07-25-1511` Alpaca core preflight를 사용했다.
- Post-preflight continuity는 Alpaca MCP `get_account_info`, `get_all_positions`, `get_watchlists`, `get_orders(status=open)`, `get_orders(status=all, after=2026-07-24T20:00:00Z)`, `get_account_activities(activity_types=[FILL], after=2026-07-24T20:00:00Z)`로 닫았다. continuity 기준 account `ACTIVE`, positions `31`, watchlists `0`, open orders `0`, same-session after-hours orders/fills `0/0`, `AVGO position 없음`, `SO qty=6`, `QQQ qty=3`, `SPY qty=2`, `WMT qty=10`, `NOK qty=398`, `NOK qty_available=398`였다.
- live account snapshot은 `cash=29036.78 USD`, `portfolio_value=96284.31 USD`, `buying_power=294299.16 USD`였다. submit boundary는 여전히 `2026-07-25-1511` source-of-record quote/spread row에 고정했다.

## 후보 평가

- `NOK` sell/trim: source-of-record quote `9.05/9.10`, quote age 약 `556.97분`, spread 약 `0.5495%`로 stale + spread hard gate fail이다.
- `SO` sell/trim: source-of-record quote `89.30/0.00`, quote age 약 `611.43분`, ask 누락이라 one-sided + stale hard gate fail이다.
- `QQQ`: source-of-record spread 자체는 `0.0132%`로 좁았지만 quote age가 약 `599.41분`으로 stale이고 1주 ask 기준 `after_hours_policy.max_notional_pct_per_order=0.005` cap도 넘는다.
- `WMT`와 `SMH`는 source-of-record quote가 one-sided이고 각각 약 `611.44분`, `611.40분` stale이다.
- `MCD/NEE/CVX/GS/SPY`는 source-of-record 기준 stale + spread 또는 cap fail이라 executable after-hours path를 만들지 못했다.
- live continuity를 refresh submit 근거로 승격하지 않았기 때문에 first blocking gate는 계속 `fresh_quote`였다.

## Submit And Reconcile

- Submitted order this cycle: 없음
- Pre-submit gate summary: 신규 `place_stock_order` 호출이 없어서 작성하지 않았다. submit branch 진입 전 `fresh_quote` 게이트가 fail했다.
- Reconciled same-session client_order_id: 없음. `2026-07-25-1511` source-of-record preflight `orders_submitted=0`, post-preflight `get_orders(status=open)=[]`, `get_orders(status=all, after=2026-07-24T20:00:00Z)=[]`, `get_account_activities(activity_types=[FILL], after=2026-07-24T20:00:00Z)=[]` 기준 이번 after-hours 세션에 새 주문 경로는 열리지 않았다.
- Retry discipline: alternate `client_order_id`는 사용하지 않았다.

## Artifacts

- Report: `wiki/current-runs/daily/2026-07-25-1511-after-hours-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-07-25-1511-after-hours-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-07-25-1511-after-hours-autopilot.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-07-25-1511-after-hours-autopilot-after-hours-gate-evaluation.json`
- Post-trade check: `wiki/trade-ledger/positions/2026-07-25-1511-after-hours-autopilot-post-trade.json`
- Prompt: `wiki/evidence-store/sources/2026-07-25-1511-after-hours-autopilot-prompt.txt`

## Validators

- `python3 scripts/check-universe-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-07-25-1511-after-hours-autopilot.json`
- `python3 scripts/check-mcp-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-07-25-1511-after-hours-autopilot.json`
- `PYTHONPATH=/private/tmp/yamlshim python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-07-25-1511-after-hours-autopilot.json`
