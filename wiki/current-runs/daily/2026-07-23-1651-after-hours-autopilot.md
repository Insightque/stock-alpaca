# 2026-07-23-1651-after-hours-autopilot

## 요약

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Session: `after_hours`
- Policy profile: `after_hours_policy`
- Artifact tag: `after-hours`
- Review bucket: `after_hours_validation`
- Market date evaluated: `Wednesday, July 22, 2026 EDT`
- Scheduler file label used: `2026-07-23-1651` (`Asia/Seoul` next-day label; actual market date anchor for this run is `Wednesday, July 22, 2026 EDT`)
- Paper mode: `ALPACA_PAPER_TRADE=true` 확인
- 결과: scheduler-owned `1651` core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. 같은 preflight의 passing clock/account/order/position/quote/spread rows와 recent fill rows를 사용한 결과 regular market closed, account `ACTIVE`, positions `31`, open orders `0`, watchlists `0`, same-session after-hours submitted/fills `2/2`를 재확인했다. 이번 cycle의 first blocking gate는 `separate_after_hours_order_budget`였고 신규 `place_stock_order` 없이 reconcile-only로 종료했다.

## 사용한 스케줄러 프리플라이트

- Alpaca core: `wiki/evidence-store/sources/2026-07-23-1651-after-hours-autopilot-alpaca-core-preflight.json`
- Research MCP: `wiki/evidence-store/sources/2026-07-23-1651-after-hours-autopilot-research-mcp-preflight.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-07-23-1651-after-hours-autopilot-after-hours-gate-evaluation.json`
- Prompt source: `wiki/evidence-store/sources/2026-07-23-1651-after-hours-autopilot-prompt.txt`
- Alpaca core preflight의 `first_blocking_gate=market_closed`는 after-hours 워크플로우에서 expected nonblocking으로 처리했다.
- submit eligibility는 `1651` core preflight의 passing clock/account/positions/open-orders/recent-activity/asset/quote rows에 고정했다. live Alpaca continuity는 reconcile-only 진단으로만 사용했다.

## Alpaca MCP 확인

- Source-of-record 기준 account `ACTIVE`, cash `29027.15 USD`, portfolio value `98152.54 USD`, buying power `29027.15 USD`, positions `31`, open orders `0`, watchlists `0`였다.
- direct Alpaca continuity spot check(`get_clock`, `get_account_info`, `get_all_positions`, `get_orders(status=open|closed)`, `get_stock_snapshot(feed=overnight)`)도 `2026-07-23T03:53:05.44693557-04:00` regular market closed, open orders `0`, same-session filled `ah-` client order ids `2건`을 재확인했다. live portfolio value는 `98148.67 USD`였다.
- same-session after-hours fill은 `NOK` sell `2건`이다. `ah-20260722-0931-sell-nok-01`은 `filled_avg_price=10.95 USD`, `filled_at=2026-07-23T01:16:18.20135Z`, `ah-20260722-1211-sell-nok-01`은 `filled_avg_price=10.78 USD`, `filled_at=2026-07-23T03:18:44.891868Z`다. same-session after-hours submitted/fills는 `2/2`로 유지됐다.
- Post-run focus는 `AVGO position 없음`, `SO qty=6`, `QQQ qty=3`, `SPY qty=2`, `WMT qty=10`, `NOK qty=399`, `NOK qty_available=399`이다.

## 후보 평가

- `NOK` sell/trim: source-of-record preflight IEX quote `10.60/10.85`, quote age `651.09분`, spread `2.3310%`다. after-hours quote/spread gate fail이며 separate after-hours session budget도 이미 `0/2 remaining`이다. live overnight continuity `10.56/10.58`는 진단상 executable이지만 submit boundary 밖이라 승격하지 않았다.
- `SO` sell/trim: preflight IEX quote `88.45/99.75`, quote age `711.04분`, spread `12.0085%`로 stale + spread cap fail이다. live overnight continuity `90.68/98.43`도 spread `8.1939%`로 cap을 크게 넘는다.
- `WMT`: preflight IEX quote `104.20/115.28`, quote age `711.08분`, spread `10.0966%`로 stale + spread cap fail이다. live overnight continuity `109.16/109.39`는 executable buy fallback처럼 보였지만 separate after-hours session budget이 이미 차단 게이트라 diagnostic-only로 유지했다.
- `MCD`: preflight IEX quote `251.75/0.00`, quote age `711.03분`, one-sided quote라 submit 불가다. live overnight continuity `262.88/264.19`는 spread `0.4960%`로 after-hours cap `0.25%`를 넘는다.
- `QQQ`: preflight IEX quote `706.51/706.68`, quote age `710.08분`, spread `0.0241%`이지만 stale이며 1주 ask 기준 after-hours per-order cap `0.5%`도 초과한다. live overnight continuity `700.32/700.43`도 per-order cap 초과는 유지한다.
- `SPY`: preflight IEX quote `748.37/748.99`, quote age `679.96분`, spread `0.0828%`이지만 stale이며 1주 ask 기준 per-order cap도 초과한다. live overnight continuity `743.16/743.91`도 per-order cap 초과는 유지한다.
- `SMH`: preflight IEX quote `571.72/607.38`, quote age `711.08분`, spread `6.0487%`와 per-order cap을 함께 fail한다. live overnight continuity `580.44/582.47`는 spread `0.3492%`로 여전히 after-hours cap을 넘고 per-order cap도 초과한다.
- `NEE`, `CVX`, `GS`: 모두 preflight 기준 stale이며 spread cap fail이다. `GS`는 per-order cap도 함께 fail이다. live continuity에서도 `NEE 89.39/89.95`, `CVX 194.45/195.66`, `GS 1081.66/1105.23`로 spread 또는 per-order cap fail이 남았다.

## Submit And Reconcile

- Pre-submit gate summary는 생성되지 않았다. submit branch 진입 전에 `separate_after_hours_order_budget` 게이트가 fail했기 때문이다.
- Submitted order this cycle: 없음
- Immediate reconciliation: source-of-record recent activity와 live continuity 모두 same-session `ah-` fill stack `2건`과 open orders `0`를 재확인했다.
- Retry discipline: alternate `client_order_id`는 사용하지 않았다.

## Artifacts

- Prompt source: `wiki/evidence-store/sources/2026-07-23-1651-after-hours-autopilot-prompt.txt`
- Report: `wiki/current-runs/daily/2026-07-23-1651-after-hours-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-07-23-1651-after-hours-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-07-23-1651-after-hours-autopilot.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-07-23-1651-after-hours-autopilot-after-hours-gate-evaluation.json`
- Post-trade check: `wiki/trade-ledger/positions/2026-07-23-1651-after-hours-autopilot-post-trade.json`

## Validators

- `PATH=/usr/local/bin:$PATH python3 scripts/check-universe-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-07-23-1651-after-hours-autopilot.json` PASS
- `PATH=/usr/local/bin:$PATH python3 scripts/check-mcp-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-07-23-1651-after-hours-autopilot.json` PASS
- `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-07-23-1651-after-hours-autopilot.json` PASS with warning `orders is empty`
