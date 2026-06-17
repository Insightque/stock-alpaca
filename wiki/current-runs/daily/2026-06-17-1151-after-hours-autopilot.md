# 2026-06-17-1151-after-hours-autopilot

## 요약

- Workflow: `harness/workflows/after-hours-autopilot.md`
- Session: `after_hours`
- Policy profile: `after_hours_policy`
- Artifact tag: `after-hours`
- Review bucket: `after_hours_validation`
- Paper mode: `ALPACA_PAPER_TRADE=true` 확인
- 결과: scheduler-owned `1151` core/research preflight를 source-of-record로 사용했고 Alpaca core regular-session `market_closed` 상태는 after-hours expected nonblocking으로 처리했다. 같은 preflight의 passing account/positions/open-orders/asset/quote/spread rows를 submit-boundary evidence로 유지했고, separate after-hours order budget은 `0/2`로 열려 있었지만 모든 shortlist quote가 `5분` freshness cap을 크게 초과해 주문 없이 종료했다.

## 사용한 스케줄러 프리플라이트

- Alpaca core: `wiki/evidence-store/sources/2026-06-17-1151-after-hours-autopilot-alpaca-core-preflight.json`
- Research MCP: `wiki/evidence-store/sources/2026-06-17-1151-after-hours-autopilot-research-mcp-preflight.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-06-17-1151-after-hours-autopilot-after-hours-gate-evaluation.json`
- Runtime continuity note: `wiki/evidence-store/sources/2026-06-17-1151-after-hours-autopilot-runtime-alpaca-spot-check.json`
- Alpaca core preflight의 regular-session `market_closed` 상태는 장외 워크플로우에서 예상되는 nonblocking 상태였다. 사용자가 같은 preflight의 passing account/positions/orders/asset/quote/spread rows를 submit-boundary evidence로 유지하라고 요구했으므로, 이번 cycle의 live Alpaca MCP continuity는 `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-16T20:00:00-04:00)/get_account_activities(activity_types=[FILL], after=2026-06-16T20:00:00-04:00)/get_watchlists/get_stock_latest_quote(feed=iex, symbols=QQQ,AVGO)` 확인에만 제한했다.

## Alpaca MCP 확인

- Regular market: scheduler preflight `get_clock`=`2026-06-16T22:51:09.025357853-04:00` 기준 regular market closed였고, live `get_clock`=`2026-06-16T22:53:35.11766221-04:00`도 같은 closed 상태였다.
- Account: scheduler preflight `get_account_info` source-of-record 기준 account `ACTIVE`, cash `30,344.81 USD`, portfolio value `101,013.82 USD`, buying power `303,392.77 USD`였다. live `get_account_info` 기준 portfolio value `101,013.68 USD`, buying power `303,392.38 USD`로 drift는 경미했고 submit-boundary 재개 없이 별도 continuity로만 기록했다.
- Positions/Open orders/Watchlists: scheduler preflight `get_all_positions/get_orders(status=open)/get_watchlists` source-of-record 기준 positions `33`건, open orders `0`건, watchlists `0`건이었다. live continuity `get_all_positions/get_orders(status=open)/get_watchlists` 기준도 positions `33`건, open orders `0`건, watchlists `0`건으로 유지됐다.
- Same-session after-hours orders/fills: live `get_orders(status=all, after=2026-06-16T20:00:00-04:00)`와 `get_account_activities(activity_types=[FILL], after=2026-06-16T20:00:00-04:00)` 기준 same-session after-hours orders `0`건, fills `0`건이었다. scheduler preflight `get_account_activities(activity_types=[FILL])`는 same-day regular-session fill history만 보여 줬고 `20:00 ET` 이후 after-hours fill은 `0`건이었다. separate after-hours session budget은 `0/2`였다.

## 후보 평가

- `QQQ`: IEX quote `729.73/729.83`, spread 약 `0.0137%`, age 약 `359.85분`으로 freshest source-of-record였지만 1주 ask가 after-hours per-order cap 약 `505.24 USD`를 넘고 freshness gate도 실패했다.
- `IONQ`: IEX quote `56.51/56.56`, spread 약 `0.0884%`, age 약 `380.43분`으로 size/spread는 허용 범위였지만 freshness gate를 크게 초과했다.
- `QBTS`: IEX quote `24.11/24.26`, spread 약 `0.6202%`, age 약 `389.25분`으로 stale quote와 spread gate를 동시에 실패했다.
- `JPM`: IEX quote `329.45/330.99`, spread 약 `0.4664%`, age 약 `407.59분`으로 stale quote와 spread gate를 동시에 실패했다.
- `PFE`: IEX quote `26.01/26.13`, spread 약 `0.4603%`, age 약 `410.41분`으로 stale quote와 spread gate를 동시에 실패했다.
- `MSFT`: IEX quote `392.89/424.01`, spread 약 `7.6190%`, age 약 `359.61분`으로 freshest large-cap fallback이었지만 freshness와 spread gate를 함께 실패했다.
- Sell/trim side도 `AVGO/SO/RGTI`가 stale quote와 wide spread로, `PFE`가 stale quote와 spread fail로 모두 실행 후보에 오르지 못했다.

## Gate 결과

- `ALPACA_PAPER_TRADE=true`: PASS
- Regular market open check: PASS (`market_closed`는 after-hours expected nonblocking)
- Alpaca core account/clock/positions/orders/asset/quote/spread: PASS (scheduler-owned submit-boundary evidence 유지)
- `after_hours_policy` profile/session/review bucket/order budget separation: PASS
- Universe strict gate: PASS (`62` symbols screened, `SPY/QQQ` benchmarks 포함)
- MCP strict gate: PASS (`sec-edgar`, `fred`, `yahoo-finance` pass; `alpha-vantage` provider_error, `firecrawl` credits 부족 gap 기록)
- Risk gate: PASS (`PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json ...`, warning=`orders is empty`)
- Fresh quote gate: FAIL
- Spread gate: FAIL
- Submit/reconcile path: 미진입

## 주문 및 리스크 검증

- 주문 계획: `wiki/trade-ledger/orders/2026-06-17-1151-after-hours-autopilot.json`
- 제출된 주문: 없음
- `session=after_hours`, `review_bucket=after_hours_validation`, `risk_inputs.after_hours_new_orders_submitted_today=0`로 기록했다.
- 같은 session budget을 regular validation count와 섞지 않았다.

## 산출물

- Run manifest: `wiki/evidence-store/run-manifests/2026-06-17-1151-after-hours-autopilot.json`
- Gate evaluation: `wiki/evidence-store/sources/2026-06-17-1151-after-hours-autopilot-after-hours-gate-evaluation.json`
- Runtime spot-check: `wiki/evidence-store/sources/2026-06-17-1151-after-hours-autopilot-runtime-alpaca-spot-check.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-17-1151-after-hours-autopilot.json`
- Post-trade note: `wiki/trade-ledger/positions/2026-06-17-1151-after-hours-autopilot-post-trade.json`

## Validators

- `PATH=/usr/local/bin:$PATH python3 scripts/check-universe-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-17-1151-after-hours-autopilot.json`: PASS
- `PATH=/usr/local/bin:$PATH python3 scripts/check-mcp-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-06-17-1151-after-hours-autopilot.json`: PASS
- `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-06-17-1151-after-hours-autopilot.json`: PASS (`orders is empty` warning only)
