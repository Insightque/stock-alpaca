# 2026-05-29-2251-hourly-autopilot scheduled paper autopilot

## 요약

- 실행 모드: regular-session hourly autopilot, `mode=submit`, paper only.
- Paper gate: `ALPACA_PAPER_TRADE=true` 확인.
- 시장 clock: Alpaca MCP preflight 기준 `is_open=true`, timestamp `2026-05-29T09:51:11.640561516-04:00`.
- Alpaca core: scheduler-owned Alpaca MCP preflight hard gate `pass` 사용. account, positions, open orders, recent fills, watchlists, asset checks, latest quotes/snapshots/trades가 read-only MCP evidence로 존재한다.
- Stale order cleanup: `wiki/evidence-store/sources/2026-05-29-2251-hourly-autopilot-stale-order-cleanup.json` status `pass`, stale candidate 0건. Fresh open hourly buy orders는 SPY/AMZN/BAC 3건이며 stale이 아니므로 cleanup 대상이 아니다.
- 주문 결정: sell/trim은 `sell_trigger_none`; fresh open order duplicate/cluster gate 때문에 SPY/AMZN/BAC/QQQ/GOOGL/AAPL은 신규 매수에서 제외하고, 서로 다른 cluster의 NKE, SO, SLB 각 1주 validation buy만 계획했다.

## 게이트 상태

| Gate | 상태 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | 환경값 `ALPACA_PAPER_TRADE=true` |
| Market open | PASS | `wiki/evidence-store/sources/2026-05-29-2251-hourly-autopilot-alpaca-core-preflight.json` |
| Alpaca core MCP | PASS | `wiki/evidence-store/sources/2026-05-29-2251-hourly-autopilot-alpaca-core-preflight.json` hard_gate_summary |
| Open-order lifecycle | PASS | `wiki/evidence-store/sources/2026-05-29-2251-hourly-autopilot-stale-order-cleanup.json`, stale candidate 0건, fresh open order 3건 |
| Universe strict | PASS | broad universe 62개, SPY/QQQ 포함 |
| Research MCP tiered | PASS | SEC EDGAR/FRED/Firecrawl/Yahoo usable, Alpha Vantage provider_error gap |
| Quote freshness/spread | PASS | 후보 quote rows captured around `2026-05-29T13:51:28Z` |
| Risk validator | PASS | `check-risk-policy.py --json`, buy notional $193.52 |
| Submit | DONE | Alpaca MCP `place_stock_order`만 사용; NKE/SO/SLB filled |

## sell/trim 진단

보유 포지션을 먼저 점검했다. AI semiconductor theme/factor/cluster, quantum/speculative exposure, 단일 ticker 비중이 정책 상한과 warning trigger 아래에 있고, 현재 evidence로 thesis-break, stale-thesis underperformance, speculative loss-control, overheat reversal 조건이 확인되지 않는다. 따라서 이번 run의 sell/trim 엔트리는 없다.

## 후보 및 주문 판단

| Symbol | Bid | Ask | Spread % | 판단 |
| --- | ---: | ---: | ---: | --- |
| NKE | 46.86 | 46.88 | 0.0427 | 1주 validation buy 계획; consumer_discretionary 분산, fresh open-order conflict 없음 |
| SO | 91.64 | 91.69 | 0.0545 | 1주 validation buy 계획; utilities/defensive_yield 분산 |
| SLB | 54.92 | 54.95 | 0.0546 | 1주 validation buy 계획; energy_services 분산 |

## MCP 공백

- `alpha-vantage`: `provider_error`. Circuit breaker가 열려 NEWS_SENTIMENT data를 사용할 수 없었다. 비차단 공백이며 retry_count=0, source_ref `wiki/evidence-store/sources/2026-05-29-2251-hourly-autopilot-research-mcp-preflight.json`.
- 나머지 research MCP: SEC EDGAR, FRED, Firecrawl, Yahoo Finance는 scheduler research preflight에서 usable/pass로 반영했다.

## 주문 계획

- Order plan: `wiki/trade-ledger/orders/2026-05-29-2251-hourly-autopilot.json`
- Planned orders: 3
- Submitted/Filled orders: NKE, SO, SLB 각 1주 filled
- Existing fresh open orders: SPY/AMZN/BAC 3건. 신규 후보와 같은 symbol/side 또는 normally blocked same-cluster 후보는 제외했다.
- Review horizons: 1D, 5D, 20D

## 제출 및 사후 reconciliation

| Symbol | Client order id | 상태 | 세부 |
| --- | --- | --- | --- |
| NKE | `hourly-20260529-2251-buy-nke` | filled | 최초 submit은 safety monitor cancelled, 동일 client-id reconciliation 404 후 같은 client id retry accepted; 1주 filled at $46.59 |
| SO | `hourly-20260529-2251-buy-so` | filled | Alpaca order `cc988999-8d85-4db2-8ef3-f146101e3b1a`, 1주 filled at $91.55 |
| SLB | `hourly-20260529-2251-buy-slb` | filled | Alpaca order `ab2c37a3-7615-432f-8ba8-c32e05909582`, 1주 filled at $54.79 |

Post-trade reconciliation은 `get_order_by_client_id`, `get_orders`, `get_all_positions`, `get_account_info`, `get_account_activities`로 수행했다. Snapshot: `wiki/trade-ledger/positions/2026-05-29-2251-hourly-autopilot-post-trade.json`. 기존 22:31 SPY/AMZN/BAC buy order 3건은 계속 `new` open 상태다.

## 검증 결과

- Universe validator: `PATH=/usr/local/bin:$PATH python3 scripts/check-universe-coverage.py --strict --json ...` PASS.
- MCP validator: `PATH=/usr/local/bin:$PATH python3 scripts/check-mcp-coverage.py --strict --json ...` PASS.
- Risk validator: `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json ...` PASS. Buy notional $193.52, post-cash $36,725.64, post-invested $65,701.71.

## 지표 설명

- `spread_pct`: `(ask - bid) / midpoint * 100`으로 계산한 호가 스프레드다. 정책 상한은 0.50%다.
- `quote_age_minutes`: order plan 작성 시점과 quote timestamp의 차이다. submit 상한은 20분이다.
- `mcp_coverage.used_in_score`: 해당 MCP evidence가 점수, confidence, risk, allocation 판단에 반영됐는지를 뜻한다.
- `sell_trigger_none`: risk trim policy의 활성 매도/축소 사유가 현재 evidence로 확인되지 않았다는 뜻이다.

## 산출물

- Manifest: `wiki/evidence-store/run-manifests/2026-05-29-2251-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-05-29-2251-hourly-autopilot.json`
- Report: `wiki/current-runs/daily/2026-05-29-2251-hourly-autopilot.md`
