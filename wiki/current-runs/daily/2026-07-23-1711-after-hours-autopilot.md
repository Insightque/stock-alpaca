# 2026-07-23-1711-after-hours-autopilot

## 요약

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Session: `after_hours`
- Policy profile: `after_hours_policy`
- Artifact tag: `after-hours`
- Review bucket: `after_hours_validation`
- Market date evaluated: `Wednesday, July 22, 2026 EDT`
- Scheduler file label used: `2026-07-23-1711` (`Asia/Seoul` next-day label; actual market date anchor for this run is `Wednesday, July 22, 2026 EDT`)
- Paper mode: `ALPACA_PAPER_TRADE=true` 확인
- 결과: scheduler-owned `1711` core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. 같은 preflight passing clock/account/order/position/quote/spread rows와 recent fill rows를 사용한 결과 regular market closed, account `ACTIVE`, positions `31`, open orders `0`, watchlists `0`, same-session after-hours submitted/fills `2/2`를 재확인했다. 이번 cycle의 first blocking gate는 `separate_after_hours_order_budget`였고 신규 `place_stock_order` 없이 reconcile-only로 종료했다.

## 사용한 스케줄러 프리플라이트

- Alpaca core: `wiki/evidence-store/sources/2026-07-23-1711-after-hours-autopilot-alpaca-core-preflight.json`
- Research MCP: `wiki/evidence-store/sources/2026-07-23-1711-after-hours-autopilot-research-mcp-preflight.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-07-23-1711-after-hours-autopilot-after-hours-gate-evaluation.json`
- Prompt source: `wiki/evidence-store/sources/2026-07-23-1711-after-hours-autopilot-prompt.txt`
- Alpaca core preflight의 `first_blocking_gate=market_closed`는 after-hours 워크플로우에서 expected nonblocking으로 처리했다.
- submit eligibility는 `1711` core preflight의 passing clock/account/positions/open-orders/recent-activity/asset/quote rows에 고정했다. live Alpaca continuity는 reconcile-only 진단으로만 사용했다.

## Alpaca MCP 확인

- Source-of-record 기준 account `ACTIVE`, cash `29027.15 USD`, portfolio value `98281.35 USD`, buying power `29027.15 USD`, positions `31`, open orders `0`, watchlists `0`였다.
- direct Alpaca continuity spot check(`get_clock`, `get_account_info`, `get_all_positions`, `get_orders(status=open|closed)`, `get_account_activities(activity_types=[FILL])`, `get_watchlists`, `get_stock_snapshot(feed=overnight)`)도 `2026-07-23T04:13:08.261719102-04:00` regular market closed, account `ACTIVE`, positions `31`, open orders `0`, watchlists `0`, same-session filled `ah-` client order ids `2건`을 재확인했다. live portfolio value는 `98313.48 USD`였다.
- same-session after-hours fill은 `NOK` sell `2건`이다. `ah-20260722-0931-sell-nok-01`은 `filled_avg_price=10.95 USD`, `filled_at=2026-07-23T01:16:18.20135Z`, `ah-20260722-1211-sell-nok-01`은 `filled_avg_price=10.78 USD`, `filled_at=2026-07-23T03:18:44.891868Z`다. same-session after-hours submitted/fills는 `2/2`로 유지됐다.
- Post-run focus는 `AVGO position 없음`, `SO qty=6`, `QQQ qty=3`, `SPY qty=2`, `WMT qty=10`, `NOK qty=399`, `NOK qty_available=399`이다.

## 후보 평가

- `NOK` sell/trim: live overnight quote `10.53/10.64`, quote age 약 `13.13분`, spread `1.0392%`다. after-hours spread gate fail이며 separate after-hours session budget도 이미 `0/2 remaining`이다.
- `SO` sell/trim: live overnight quote `93.29/96.54`, quote age 약 `13.13분`, spread `3.4244%`로 spread cap fail이다.
- `WMT`: live overnight quote `108.06/122.05`, spread `12.1597%`로 spread gate fail이다.
- `MCD`: live overnight quote `251.87/265.36`, spread `5.2154%`로 spread gate fail이다.
- `QQQ`: live overnight quote `700.70/706.24`, spread `0.7876%`이며 1주 ask 기준 after-hours per-order cap `0.5%`도 초과한다.
- `SPY`: live overnight quote `743.92/749.69`, spread `0.7727%`이며 1주 ask 기준 per-order cap도 초과한다.
- `SMH`: live overnight quote `579.88/590.99`, spread `1.8979%`와 per-order cap을 함께 fail한다.
- `NEE`, `CVX`, `GS`: 모두 live overnight 기준 spread cap fail이다. `GS`는 per-order cap도 함께 fail이다.

## Submit And Reconcile

- Pre-submit gate summary는 생성되지 않았다. submit branch 진입 전에 `separate_after_hours_order_budget` 게이트가 fail했기 때문이다.
- Submitted order this cycle: 없음
- Immediate reconciliation: source-of-record recent activity와 live continuity 모두 same-session `ah-` fill stack `2건`과 open orders `0`를 재확인했다.
- Retry discipline: alternate `client_order_id`는 사용하지 않았다.

## Artifacts

- Prompt source: `wiki/evidence-store/sources/2026-07-23-1711-after-hours-autopilot-prompt.txt`
- Report: `wiki/current-runs/daily/2026-07-23-1711-after-hours-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-07-23-1711-after-hours-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-07-23-1711-after-hours-autopilot.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-07-23-1711-after-hours-autopilot-after-hours-gate-evaluation.json`
- Post-trade check: `wiki/trade-ledger/positions/2026-07-23-1711-after-hours-autopilot-post-trade.json`

## Validators

- `PATH=/usr/local/bin:$PATH python3 scripts/check-universe-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-07-23-1711-after-hours-autopilot.json` PASS
- `PATH=/usr/local/bin:$PATH python3 scripts/check-mcp-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-07-23-1711-after-hours-autopilot.json` PASS
- `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-07-23-1711-after-hours-autopilot.json` PASS with warning `orders is empty`
