# 2026-07-24-1911-after-hours-autopilot

## 요약

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Session: `after_hours`
- Policy profile: `after_hours_policy`
- Artifact tag: `after-hours`
- Review bucket: `after_hours_validation`
- Market date evaluated: `Thursday, July 23, 2026 EDT`
- Scheduler file label used: `2026-07-24-1911-` (`Asia/Seoul` next-day file label; actual market date anchor for this run is `Thursday, July 23, 2026 EDT`)
- Paper mode: `ALPACA_PAPER_TRADE=true` 확인
- 결과: scheduler-owned future-labeled KST artifact path `2026-07-24-1911-` core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. 같은 `2026-07-24-1911-` preflight는 passing account/positions/open-orders/asset/quote/spread rows와 `orders_submitted=0`을 제공했다. live Alpaca continuity는 current session의 Alpaca MCP `get_account_info`, `get_all_positions`, `get_watchlists`, `get_orders(status=open)`, `get_orders(status=all, after=2026-07-23T20:00:00Z)`, `get_stock_latest_quote(feed=overnight, symbols=SO,WMT,MCD,QQQ,SPY,SMH,NOK,NEE,CVX,GS)`로 닫았고 account `ACTIVE`, positions `31`, watchlists `0`, open orders `0`, same-session after-hours orders/fills `0/0`을 재확인했다. `get_account_activities(activity_types=[FILL], after=2026-07-23T20:00:00Z)` continuity 호출은 두 번 user-cancelled로 끝나서 fill count는 source-of-record preflight와 live empty order book parity에 고정했다. 다만 이번 scheduled run은 user requirement에 따라 `2026-07-24-1911-` source-of-record quote/spread rows를 submit boundary로 유지했고, 모든 executable 후보가 stale, one-sided, spread fail, 또는 per-order cap fail로 남아 신규 `place_stock_order` 없이 reconcile-only run으로 종료했다.

## 사용한 스케줄러 프리플라이트

- Alpaca core: `wiki/evidence-store/sources/2026-07-24-1911-after-hours-autopilot-alpaca-core-preflight.json`
- Research MCP: `wiki/evidence-store/sources/2026-07-24-1911-after-hours-autopilot-research-mcp-preflight.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-07-24-1911-after-hours-autopilot-after-hours-gate-evaluation.json`
- Alpaca core preflight의 `first_blocking_gate=market_closed`는 after-hours 워크플로우에서 expected nonblocking으로 처리했다.

## Alpaca MCP 확인

- Source-of-record account / positions / open orders / asset / quote / spread rows는 scheduler-owned future-labeled KST artifact path `2026-07-24-1911-` Alpaca core preflight를 사용했다.
- Live continuity 기준 account `ACTIVE`, positions `31`, watchlists `0`, open orders `0`, same-session after-hours orders/fills `0/0`, `AVGO position 없음`, `SO qty=6`, `QQQ qty=3`, `SPY qty=2`, `WMT qty=10`, `NOK qty=399`, `NOK qty_available=399`였다.
- source-of-record submit boundary는 scheduler-owned preflight quote/spread row에 고정했고, live continuity account snapshot은 `status=ACTIVE`, `cash=29027.11 USD`, `portfolio_value=97453.77 USD`, `buying_power=296955.61 USD`였다.

## 후보 평가

- `NOK` sell/trim: source-of-record quote `9.73/9.82`, quote age 약 `771.51분`, spread 약 `0.9207%`로 stale + spread hard gate fail이다.
- `SO` sell/trim: source-of-record quote `91.44/100.57`, quote age 약 `831.50분`, spread 약 `9.5099%`로 stale + spread hard gate fail이다.
- `QQQ`: source-of-record spread 자체는 `0.0144%`로 좁았지만 quote age가 약 `775.84분`으로 stale이고 1주 ask `694.87 USD`가 `after_hours_policy.max_notional_pct_per_order=0.005` cap `487.28 USD`를 넘는다.
- `WMT`와 `MCD`는 source-of-record quote가 one-sided이고 각각 약 `831.46분`, `831.45분` stale이다.
- `SPY/SMH/NEE/CVX/GS`는 source-of-record 기준 stale + spread 또는 cap fail, `NOK` buy fallback은 stale/spread fail에 더해 `blocked_add_symbol_review_queue`가 남아 executable after-hours path를 만들지 못했다.
- live overnight quote를 continuity 참고로만 사용했고 submit 근거로 승격하지 않았기 때문에 first blocking gate는 계속 `fresh_quote`였다.

## Submit And Reconcile

- Submitted order this cycle: 없음
- Pre-submit gate summary: 신규 `place_stock_order` 호출이 없어서 작성하지 않았다. submit branch 진입 전 `fresh_quote` 게이트가 fail했다.
- Reconciled same-session client_order_id: 없음. `2026-07-24-1911-` source-of-record preflight `orders_submitted=0`, live `get_orders(status=open)=[]`, `get_orders(status=all, after=2026-07-23T20:00:00Z)=[]` 기준 이번 after-hours 세션에 새 주문 경로는 열리지 않았다. `get_account_activities(activity_types=[FILL], after=2026-07-23T20:00:00Z)` continuity 호출은 user-cancelled였지만 source-of-record preflight recent-activities row와 live empty order books가 same-session fill `0`과 모순되지 않았다.
- Retry discipline: alternate `client_order_id`는 사용하지 않았다.

## Artifacts

- Report: `wiki/current-runs/daily/2026-07-24-1911-after-hours-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-07-24-1911-after-hours-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-07-24-1911-after-hours-autopilot.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-07-24-1911-after-hours-autopilot-after-hours-gate-evaluation.json`
- Post-trade check: `wiki/trade-ledger/positions/2026-07-24-1911-after-hours-autopilot-post-trade.json`
- Prompt: `wiki/evidence-store/sources/2026-07-24-1911-after-hours-autopilot-prompt.txt`

## Validators

- `python3 scripts/check-universe-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-07-24-1911-after-hours-autopilot.json`
- `python3 scripts/check-mcp-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-07-24-1911-after-hours-autopilot.json`
- `PYTHONPATH=/private/tmp/yamlshim python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-07-24-1911-after-hours-autopilot.json`

- Validator result: universe strict PASS, MCP strict PASS, risk policy PASS with warning `orders is empty`.
