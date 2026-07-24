# 2026-07-25-0651-after-hours-autopilot

## 요약

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Session: `after_hours`
- Policy profile: `after_hours_policy`
- Artifact tag: `after-hours`
- Review bucket: `after_hours_validation`
- Market date evaluated: `Friday, July 24, 2026 EDT`
- Scheduler file label used: `2026-07-25-0651-` (`Asia/Seoul` next-day future label; actual market date anchor for this run is `Friday, July 24, 2026 EDT`)
- Paper mode: `ALPACA_PAPER_TRADE=true` 확인
- 결과: scheduler-owned future-labeled KST artifact path `2026-07-25-0651-` core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. 같은 `2026-07-25-0651-` preflight는 passing account/positions/open-orders/asset/quote/spread rows와 `orders_submitted=0`을 제공했다. 이번 cycle에서는 same source-of-record quote rows 중 submit gate를 끝까지 통과한 후보가 없었고, 가장 근접한 `NOK`도 `bid/ask 9.05/9.10`, quote age `56.66분`, spread `0.5510%`로 freshness/spread hard gate를 넘지 못해 신규 `place_stock_order` 없이 no-submit으로 종료했다.

## 사용한 스케줄러 프리플라이트

- Alpaca core: `wiki/evidence-store/sources/2026-07-25-0651-after-hours-autopilot-alpaca-core-preflight.json`
- Research MCP: `wiki/evidence-store/sources/2026-07-25-0651-after-hours-autopilot-research-mcp-preflight.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-07-25-0651-after-hours-autopilot-after-hours-gate-evaluation.json`
- Alpaca core preflight의 `first_blocking_gate=market_closed`는 after-hours 워크플로우에서 expected nonblocking으로 처리했다.

## Alpaca MCP 확인

- Source-of-record account / positions / open orders / asset / quote / spread rows는 scheduler-owned future-labeled KST artifact path `2026-07-25-0651-` Alpaca core preflight를 사용했다.
- Source-of-record preflight 기준 account `ACTIVE`, positions `31`, open orders `0`, same-session after-hours orders/fills `0/0`, `AVGO position 없음`, `SO qty=6`, `QQQ qty=3`, `SPY qty=2`, `WMT qty=10`, `NOK qty=398`, `NOK qty_available=398`였다.
- no-submit 결정 후 live Alpaca MCP continuity에서 `get_order_by_client_id(client_order_id=ah-20260723-2151-sell-nok-01)`은 `filled`였고, `get_account_activities(activity_types=[FILL], after=2026-07-24T20:00:00Z)=[]`라 current after-hours session drift가 없음을 재확인했다.
- source-of-record account snapshot은 `status=ACTIVE`, `cash=29036.78 USD`, `portfolio_value=96294.09 USD`, `buying_power=294337.68 USD`였다. submit boundary는 여전히 scheduler-owned preflight quote/spread row다.

## 후보 평가

- `NOK` sell/trim: source-of-record quote `9.05/9.10`, age `56.66분`, spread `0.5510%`로 after-hours freshness/spread hard gate fail이다.
- `SO` sell/trim: source-of-record quote가 one-sided이고 age `111.12분`이라 executable sell gate fail이다.
- `QQQ`: source-of-record quote spread는 양호하지만 age `99.10분`으로 stale이고 1주 ask가 `after_hours_policy.max_notional_pct_per_order=0.005` cap를 넘는다.
- `WMT`는 one-sided + stale, `MCD`는 age `69.11분` + spread `2.2471%`, `SPY/NEE/CVX/GS`는 stale + spread fail, `SMH`는 one-sided + stale였다.
- source-of-record submit boundary를 유지했기 때문에 first blocking gate는 `fresh_quote`였다.

## Submit And Reconcile

- Submitted order this cycle: 없음
- Pre-submit gate summary: 신규 `place_stock_order` 호출이 없어서 작성하지 않았다. submit branch 진입 전 `fresh_quote` 게이트가 fail했다.
- Reconciled same-session client_order_id: 없음. `2026-07-25-0651-` source-of-record preflight `orders_submitted=0`과 live Alpaca MCP continuity 모두 이번 `Friday, July 24, 2026 EDT` after-hours 세션에 새 주문/체결이 없음을 유지했다.
- Retry discipline: alternate `client_order_id`는 사용하지 않았다.

## Artifacts

- Report: `wiki/current-runs/daily/2026-07-25-0651-after-hours-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-07-25-0651-after-hours-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-07-25-0651-after-hours-autopilot.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-07-25-0651-after-hours-autopilot-after-hours-gate-evaluation.json`
- Post-trade check: `wiki/trade-ledger/positions/2026-07-25-0651-after-hours-autopilot-post-trade.json`
- Prompt: `wiki/evidence-store/sources/2026-07-25-0651-after-hours-autopilot-prompt.txt`

## Validators

- `python3 scripts/check-universe-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-07-25-0651-after-hours-autopilot.json` -> PASS
- `python3 scripts/check-mcp-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-07-25-0651-after-hours-autopilot.json` -> PASS
- `PYTHONPATH=/private/tmp/yamlshim python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-07-25-0651-after-hours-autopilot.json` -> PASS

- Validator result: universe strict PASS, MCP strict PASS, risk policy PASS with warning `orders is empty`.
