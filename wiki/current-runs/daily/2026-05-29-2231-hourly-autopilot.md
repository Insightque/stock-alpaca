# 2026-05-29-2231-hourly-autopilot scheduled paper autopilot

## 요약

- 실행 모드: regular-session hourly autopilot, `mode=submit`, paper only.
- Paper gate: `ALPACA_PAPER_TRADE=true` 확인.
- 시장 clock: Alpaca MCP preflight 기준 `is_open=true`, timestamp `2026-05-29T09:31:08.374186646-04:00`.
- Alpaca core: scheduler-owned Alpaca MCP preflight hard gate `pass` 사용. account, positions, open orders, recent fills, watchlists, asset checks, latest quotes/snapshots/trades가 read-only MCP evidence로 존재한다.
- Stale order cleanup: `wiki/evidence-store/sources/2026-05-29-2231-hourly-autopilot-stale-order-cleanup.json` status `pass`, stale candidate 0건, remaining open order 0건.
- 주문 결정: sell/trim은 `sell_trigger_none`; 신규 validation buy 후보는 SPY, AMZN, NKE, PFE, BAC 각 1주다. 최종 제출은 universe/MCP/risk validator PASS 이후에만 진행한다.

## 게이트 상태

| Gate | 상태 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | 환경값 `ALPACA_PAPER_TRADE=true` |
| Market open | PASS | `wiki/evidence-store/sources/2026-05-29-2231-hourly-autopilot-alpaca-core-preflight.json` |
| Alpaca core MCP | PASS | `wiki/evidence-store/sources/2026-05-29-2231-hourly-autopilot-alpaca-core-preflight.json` hard_gate_summary |
| Open-order lifecycle | PASS | `wiki/evidence-store/sources/2026-05-29-2231-hourly-autopilot-stale-order-cleanup.json`, stale/open order 0건 |
| Universe strict | PASS | broad universe 62개, SPY/QQQ 포함 |
| Research MCP tiered | PASS | SEC EDGAR/FRED/Firecrawl/Yahoo usable, Alpha Vantage provider_error gap |
| Quote freshness/spread | PASS | 후보 quote rows captured around `2026-05-29T13:31:27Z` |
| Risk validator | PASS | `check-risk-policy.py --json`, buy notional $1,152.53 |
| Submit | READY | pre-submit gate summary 이후 Alpaca MCP `place_stock_order`만 사용 |

## sell/trim 진단

보유 포지션을 먼저 점검했다. AMD/NVDA/AVGO/TSM/LRCX 중심 AI semiconductor cluster는 정책 상한 아래이고, IONQ/RGTI speculative 노출도 상한 아래다. RGTI의 당일 약세는 관찰 대상이지만 누적 손익이 loss-control 조건에 닿지 않았고, stale-thesis underperformance 또는 thesis-break를 확인할 scheduler evidence가 없다. 따라서 이번 run의 sell/trim 엔트리는 없다.

## 후보 및 주문 판단

| Symbol | Bid | Ask | Spread % | 판단 |
| --- | ---: | ---: | ---: | --- |
| SPY | 755.78 | 755.90 | 0.0159 | 1주 validation buy 계획; broad_market/broad_index 분산 |
| AMZN | 272.61 | 272.82 | 0.0770 | 1주 validation buy 계획; mega_cap_tech/growth_quality 분산 |
| NKE | 46.90 | 46.93 | 0.0639 | 1주 validation buy 계획; consumer_cyclical/consumer_rate_sensitive 분산 |
| PFE | 26.14 | 26.16 | 0.0765 | 1주 validation buy 계획; healthcare_pharma/defensive_healthcare 분산 |
| BAC | 50.68 | 50.72 | 0.0789 | 1주 validation buy 계획; financials/bank_rate_sensitive 분산 |

## MCP 공백

- `alpha-vantage`: `provider_error`. Alpha Vantage daily API rate limit 때문에 NEWS_SENTIMENT data를 사용할 수 없었다. 비차단 공백이며 retry_count=0, source_ref `wiki/evidence-store/sources/2026-05-29-2231-hourly-autopilot-research-mcp-preflight.json`.
- 나머지 research MCP: SEC EDGAR, FRED, Firecrawl, Yahoo Finance는 scheduler research preflight에서 usable/pass로 반영했다.

## 주문 계획

- Order plan: `wiki/trade-ledger/orders/2026-05-29-2231-hourly-autopilot.json`
- Planned orders: 5
- Submitted orders: 4건 accepted/open-or-filled, 1건 not submitted. SPY/AMZN/BAC는 `new`, PFE는 1주 filled, NKE는 cancelled retry 후 client id 404로 not submitted.
- Review horizons: 1D, 5D, 20D

## 제출 및 사후 reconciliation

| Symbol | Client order id | 상태 | 세부 |
| --- | --- | --- | --- |
| SPY | `hourly-20260529-2231-buy-spy` | new | Alpaca order `9bd742a2-2b33-4833-b810-8c8284d1d10c`, 1주 limit $755.90 |
| AMZN | `hourly-20260529-2231-buy-amzn` | new | Alpaca order `7a871e73-4dc1-4f99-8cd5-fe8ff3be3208`, 1주 limit $272.82 |
| NKE | `hourly-20260529-2231-buy-nke` | not submitted | 최초 submit cancelled, client-id reconciliation 404, 동일 client-id retry도 tool monitor cancelled; 다른 client id로 재시도하지 않음 |
| PFE | `hourly-20260529-2231-buy-pfe` | filled | Alpaca order `8c450a91-d5b5-4d2c-919e-d36523d64ce4`, 1주 filled at $26.09 |
| BAC | `hourly-20260529-2231-buy-bac` | new | Alpaca order `71d29236-810c-4a3e-af0d-f79e7521534e`, 1주 limit $50.72 |

Post-trade reconciliation은 `get_order_by_client_id`, `get_orders`, `get_all_positions`, `get_account_info`로 수행했다. `get_account_activities`는 tool monitor에서 cancelled 되었지만, PFE fill은 order reconciliation과 positions에서 확인됐다. Snapshot: `wiki/trade-ledger/positions/2026-05-29-2231-hourly-autopilot-post-trade.json`.

## 검증 결과

- Universe validator: `PATH=/usr/local/bin:$PATH python3 scripts/check-universe-coverage.py --strict --json ...` PASS.
- MCP validator: `PATH=/usr/local/bin:$PATH python3 scripts/check-mcp-coverage.py --strict --json ...` PASS.
- Risk validator: `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json ...` PASS. Buy notional $1,152.53, post-cash $35,792.72, post-invested $66,420.64.

## 지표 설명

- `spread_pct`: `(ask - bid) / midpoint * 100`으로 계산한 호가 스프레드다. 정책 상한은 0.50%다.
- `quote_age_minutes`: market clock check 시점과 quote timestamp의 차이다. submit 상한은 20분이다.
- `mcp_coverage.used_in_score`: 해당 MCP evidence가 점수, confidence, risk, allocation 판단에 반영됐는지를 뜻한다.
- `sell_trigger_none`: risk trim policy의 활성 매도/축소 사유가 현재 evidence로 확인되지 않았다는 뜻이다.

## 산출물

- Manifest: `wiki/evidence-store/run-manifests/2026-05-29-2231-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-05-29-2231-hourly-autopilot.json`
- Report: `wiki/current-runs/daily/2026-05-29-2231-hourly-autopilot.md`
