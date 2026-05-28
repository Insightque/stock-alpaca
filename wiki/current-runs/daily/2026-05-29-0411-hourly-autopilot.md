# 2026-05-29-0411-hourly-autopilot scheduled paper autopilot

## 요약

- 실행 모드: regular-session hourly autopilot, `mode=submit`, paper only.
- Paper gate: `ALPACA_PAPER_TRADE=true` 확인.
- 시장 clock: Alpaca MCP preflight 기준 `is_open=true`, timestamp `2026-05-28T15:11:14.912334142-04:00`.
- Alpaca core: scheduler-owned Alpaca MCP preflight hard gate `pass` 사용. account, positions, open orders, recent fills, watchlists, asset checks, latest quotes/snapshots/trades가 모두 read-only MCP evidence로 존재한다.
- Stale order cleanup: `wiki/evidence-store/sources/2026-05-29-0411-hourly-autopilot-stale-order-cleanup.json` status `pass`, remaining open order 0건.
- 주문 결정: 신규 주문 없음. 첫 차단 gate는 `risk_daily_new_orders_budget`이며 regular ET session 신규 주문 카운트가 20/20에 도달했다.

## 게이트 상태

| Gate | 상태 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | 환경값 `ALPACA_PAPER_TRADE=true` |
| Market open | PASS | `wiki/evidence-store/sources/2026-05-29-0411-hourly-autopilot-alpaca-core-preflight.json` |
| Alpaca core MCP | PASS | `wiki/evidence-store/sources/2026-05-29-0411-hourly-autopilot-alpaca-core-preflight.json` hard_gate_summary |
| Open-order lifecycle | PASS | `wiki/evidence-store/sources/2026-05-29-0411-hourly-autopilot-stale-order-cleanup.json`, open orders 0건 |
| Universe strict | PASS | broad universe 62개, SPY/QQQ 포함 |
| Research MCP tiered | PASS | SEC EDGAR/FRED/Firecrawl/Yahoo usable, Alpha Vantage empty_response gap |
| Quote freshness/spread | PASS | shortlist quote rows captured at `2026-05-28T19:11:35Z`-`2026-05-28T19:11:36Z` |
| Risk validator | PASS | `check-risk-policy.py --json`, empty orders warning only |
| Submit | BLOCKED | `risk_daily_new_orders_budget` 20/20 |

## 후보 및 주문 판단

Research preflight shortlist는 SPY, QQQ, WMT, NEE, GOOGL, PLTR, FCX, AAPL, SLB, NVDA, NKE, MSFT 이다. 상위 재점검 후보는 SPY, QQQ, WMT, NEE, GOOGL로 유지하지만, 신규 매수는 같은 ET 세션 daily order cap 때문에 계획하지 않았다. 보유 포지션 trim 후보는 open-order lifecycle과 quote gate는 통과했지만, 현재 preflight에는 thesis-break, risk-limit, stale-thesis underperformance, speculative cap 초과 같은 활성 trim 사유가 확인되지 않아 매도 계획도 만들지 않았다.

| Symbol | Bid | Ask | Spread % | 판단 |
| --- | ---: | ---: | ---: | --- |
| SPY | 754.41 | 754.44 | 0.0040 | daily cap 해소 후 재점검 |
| QQQ | 735.72 | 735.76 | 0.0054 | daily cap 해소 후 재점검 |
| WMT | 118.59 | 118.60 | 0.0084 | daily cap 해소 후 재점검 |
| NEE | 87.57 | 87.58 | 0.0114 | daily cap 해소 후 재점검 |
| GOOGL | 390.63 | 390.68 | 0.0128 | daily cap 해소 후 재점검 |
| PLTR | 142.37 | 142.39 | 0.0140 | daily cap 해소 후 재점검 |
| FCX | 65.39 | 65.40 | 0.0153 | daily cap 해소 후 재점검 |
| AAPL | 310.43 | 310.48 | 0.0161 | daily cap 해소 후 재점검 |
| SLB | 55.34 | 55.35 | 0.0181 | daily cap 해소 후 재점검 |
| NVDA | 214.51 | 214.55 | 0.0186 | daily cap 해소 후 재점검 |

## MCP 공백

- `alpha-vantage`: `empty_response`. NEWS_SENTIMENT가 shortlist 후보에 대해 candidate news item 0건을 반환했다. 비차단 공백이며 retry_count=0, source_ref `wiki/evidence-store/sources/2026-05-29-0411-hourly-autopilot-research-mcp-preflight.json`.
- 나머지 research MCP: SEC EDGAR, FRED, Firecrawl, Yahoo Finance는 scheduler research preflight에서 usable/pass로 반영했다.

## 주문 계획

- Order plan: `wiki/trade-ledger/orders/2026-05-29-0411-hourly-autopilot.json`
- Planned orders: 0
- Submitted orders: 0
- Post-trade reconciliation: submit attempt가 없으므로 별도 주문 reconciliation은 수행하지 않았고, scheduler Alpaca core preflight의 open orders 0건 및 recent fills를 현재 상태 근거로 사용했다.

## 검증 결과

- Universe validator: `PATH=/usr/local/bin:$PATH python3 scripts/check-universe-coverage.py --strict --json ...` PASS.
- MCP validator: `PATH=/usr/local/bin:$PATH python3 scripts/check-mcp-coverage.py --strict --json ...` PASS.
- Risk validator: `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json ...` PASS, warning `orders is empty`.

## 지표 설명

- `risk_daily_new_orders_budget`: `harness/risk-policy.yaml`의 `daily_limits.max_new_orders_per_day` 대비 같은 ET 정규장 세션 신규 주문 수를 비교하는 hard gate다.
- `spread_pct`: `(ask - bid) / midpoint * 100`으로 계산한 호가 스프레드다. 정책 상한은 0.50%다.
- `mcp_coverage.used_in_score`: 해당 MCP evidence가 점수, confidence, risk, allocation 판단에 반영됐는지를 뜻한다.
- `first_blocking_gate`: 모든 후보 중 실제 주문 제출을 처음으로 막은 hard gate다.

## 산출물

- Manifest: `wiki/evidence-store/run-manifests/2026-05-29-0411-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-05-29-0411-hourly-autopilot.json`
- Report: `wiki/current-runs/daily/2026-05-29-0411-hourly-autopilot.md`
