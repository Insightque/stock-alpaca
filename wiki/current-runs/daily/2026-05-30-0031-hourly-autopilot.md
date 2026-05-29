# 2026-05-30 00:31 KST hourly paper autopilot

## 요약

- Workflow: `harness/workflows/hourly-autopilot.md` regular-session scheduled paper autopilot.
- Paper mode: `ALPACA_PAPER_TRADE=true` 확인.
- Scheduler stale cleanup: PASS, 남은 open hourly order 없음.
- Alpaca core: scheduler-owned preflight hard gate PASS, market open.
- Research MCP: SEC EDGAR/FRED/Firecrawl/Yahoo Finance usable/pass, Alpha Vantage는 `provider_error` rate-limit/circuit-breaker 공백이다. 최소 3개 research confirmation은 충족했다.
- 주문 계획: MRK 1주 day limit paper validation buy. AAPL/COP/NOK 추가매수는 validation lifecycle due review 누락 때문에 차단했다.
- Sell/trim: AMD/PLTR/RGTI를 먼저 진단했지만 thesis-break, risk-limit, stale-thesis underperformance, overheat reversal, speculative loss-control 조건이 주문 가능 수준으로 충족되지 않았다.

## Gate 결과

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env`의 paper flag true 확인, 값은 기록하지 않음 |
| Market clock | PASS | Alpaca preflight timestamp 2026-05-29T11:31:08.581835446-04:00 |
| Stale/open order lifecycle | PASS | cleanup PASS, open orders `[]` |
| Alpaca core | PASS | account/clock/positions/orders/activities/assets/quotes/snapshots/trades preflight PASS |
| Universe strict | PASS | 62개 broad universe, SPY/QQQ 포함, final candidate MRK |
| Research MCP tiered | PASS | 4 usable/pass providers, Alpha Vantage provider_error gap |
| Quote freshness/spread | PASS | MRK quote age 2.343분, spread 0.0423% |
| Risk validator | PASS | `scripts/check-risk-policy.py --json` PASS |
| Submit | DONE | MRK Alpaca MCP day-limit paper buy 제출, reconciliation 기준 open `new` |

## Sell/Trim 진단

| Symbol | 판단 | 이유 |
| --- | --- | --- |
| AMD | watch | AI semiconductor target-band watch지만 deterioriation/overheat reversal/thesis-break 조건이 확인되지 않았고 trim gate가 부족하다. |
| PLTR | watch | 작은 speculative-growth 보유. overheat watch이나 5D reversal 조건이 확인되지 않았다. |
| RGTI | watch | speculative exposure와 손실-control 조건이 hard trim까지 도달하지 않았다. |

## 주문 후보

| Symbol | 계획 | 근거 |
| --- | --- | --- |
| MRK | 1주 buy 계획 | healthcare_pharma/defensive_healthcare 신규 validation 표본. 기존 AI semiconductor/mega-cap 집중을 늘리지 않고, SEC/FRED/Firecrawl/Yahoo preflight가 usable/pass다. |
| AAPL/COP/NOK | 추가매수 차단 | 1D validation lifecycle review가 due이지만 hold/add/trim/close 결정 기록이 아직 없다. |
| BAC/NKE/PFE/V/NEE/WMT/GOOGL | 관찰 | 최근 validation 표본이 이미 누적되어 이번 run에서는 반복 add보다 MRK 신규 healthcare 표본을 우선했다. |

## 지표 설명

- `quote_age_minutes`: Alpaca quote timestamp와 의사결정 시각 사이의 분 단위 차이. submit 상한은 `harness/risk-policy.yaml` 기준 20분이다.
- `spread_pct`: `(ask - bid) / mid` 백분율. 상한은 `harness/risk-policy.yaml` 기준 0.50%다.
- `mcp_coverage`: Alpaca core와 SEC EDGAR/Alpha Vantage/FRED/Firecrawl/Yahoo Finance 확인 상태다. Research provider 하나가 실패해도 core와 최소 3개 research confirmation이 통과하면 nonblocking으로 둔다.
- `sell_candidate_diagnostics`: 매 run sell/trim 후보를 먼저 평가해 주문이 없더라도 top diagnostics를 남기는 v1.9 정책 필드다.
- `validation_lifecycle`: validation buy의 1D/5D/20D due review가 있으면 해당 symbol 추가매수를 막는 정책 필드다.

## 제출 및 사후 확인

- Submitted: MRK 1주 day limit buy, client_order_id `hourly-20260530-0031-buy-mrk`, order id `fa63eb83-042a-4982-8dd5-e0491cc18276`.
- Status after reconciliation: `new`, filled_qty 0, open order에 남아 있다.
- Reconciliation: client-id order lookup PASS, open orders PASS(MRK open), positions lookup PASS on registered Alpaca MCP retry, fills lookup PASS(no MRK fill). Account refresh는 tool safety monitor에서 cancelled되어 scheduler Alpaca core preflight account를 snapshot source로 유지했다.
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-05-30-0031-hourly-autopilot-post-trade.json`.

## 산출물

- Manifest: `wiki/evidence-store/run-manifests/2026-05-30-0031-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-05-30-0031-hourly-autopilot.json`
- Report: `wiki/current-runs/daily/2026-05-30-0031-hourly-autopilot.md`
