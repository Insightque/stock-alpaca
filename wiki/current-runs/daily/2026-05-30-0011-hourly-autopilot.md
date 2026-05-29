# 2026-05-30-0011-hourly-autopilot scheduled paper autopilot

## 요약

- 실행 모드: regular-session hourly autopilot, `mode=submit`, paper only.
- Paper gate: `ALPACA_PAPER_TRADE=true` 확인.
- 시장 clock: registered Alpaca MCP spot check 기준 `is_open=true`, timestamp `2026-05-29T11:14:17.876346122-04:00`.
- Alpaca core: scheduler-owned preflight hard gate `pass`; nested registered Alpaca MCP spot checks(account/positions/open orders/GOOGL-WMT-NEE quotes)도 사용했다.
- Research MCP: SEC EDGAR/FRED/Firecrawl/Yahoo Finance usable/pass, Alpha Vantage는 `provider_error` circuit breaker 공백이다. 최소 3개 research confirmation은 충족했다.
- 주문 계획: GOOGL, WMT, NEE 각 1주 day limit paper validation buy. AAPL/COP/NOK 추가매수는 validation lifecycle due review 누락 때문에 차단했다.

## 게이트 상태

| Gate | 상태 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | 환경값 `ALPACA_PAPER_TRADE=true` |
| Market open | PASS | registered Alpaca MCP `get_clock`, `wiki/evidence-store/sources/2026-05-30-0011-hourly-autopilot-runtime-alpaca-spot-check.json` |
| Alpaca core MCP | PASS | scheduler preflight + spot checks |
| Stale/open-order lifecycle | PASS | `wiki/evidence-store/sources/2026-05-30-0011-hourly-autopilot-stale-order-cleanup.json` 및 spot `get_orders` 결과 open orders 없음 |
| Universe strict | PASS | broad universe 62개, SPY/QQQ 포함, shortlist 10개, final candidates 3개 |
| Research MCP tiered | PASS | 4 usable/pass providers, Alpha Vantage provider_error gap |
| Quote freshness/spread | PASS | GOOGL/WMT/NEE quotes < 1분, spread 0.016%/0.444%/0.035% |
| Risk validator | PASS | buy notional $584.82, post-cash $34800.03 |
| Submit | DONE | GOOGL/WMT/NEE Alpaca MCP day-limit paper buy 제출 및 체결 확인 |

## sell/trim 진단

보유 포지션을 신규 매수보다 먼저 점검했다. 이번 run에서는 open-order lifecycle이 깨끗하지만, AMD/PLTR/RGTI 모두 YAML 활성 trim 조건을 충족하지 못해 주문이 아니라 watch 진단으로 남겼다.

| Symbol | Held qty | Weight % | Trigger | 판단 |
| --- | ---: | ---: | --- | --- |
| AMD | 14 | 7.065 | sell_skip_gate | AI semiconductor target-band watch, deterioration trigger 부족 및 AMD spread gate 부적합 |
| PLTR | 1 | 0.153 | sell_trigger_none | 과열 watch, reversal trigger 미확인 |
| RGTI | 120 | 2.965 | sell_trigger_none | 투기 포지션 약세 watch, speculative-loss trigger 미충족 |

## 후보 및 주문 판단

| Symbol | 판단 |
| --- | --- |
| GOOGL | 1주 buy 계획. mega_cap_tech/growth_quality이지만 기존 보유는 1주뿐이고 ticker cap 여유가 크며, AI semiconductor 집중을 직접 늘리지 않는다. |
| WMT | 1주 buy 계획. consumer_defensive/defensive_quality로 고베타 포지션을 완충한다. spread는 정책 상한 아래지만 넓어 1주 validation으로 제한한다. |
| NEE | 1주 buy 계획. utilities/defensive_yield 분산 목적이고 due review blocker가 없다. |
| AAPL/COP/NOK | 추가매수 차단. 1D validation lifecycle review가 due로 보이지만 아직 hold/add/trim/close 결정 기록이 없다. |
| BAC/NKE/PFE/SLB | 관찰. 이미 같은 ET 세션 validation 표본이 늘었고 이번 run은 distinct mega-cap/defensive/utilities cluster를 우선했다. |

## validation lifecycle

`risk_trim_policy.validation_lifecycle`를 적용했다. NKE/PFE/SO/WMT/NEE/AMZN/BAC/XOM/V는 `wiki/index.md` 기준 1D 회고가 기록되어 있고, same-day fill인 PFE/NKE/SO/SLB/AMZN/QQQ/V는 아직 1D/5D/20D review due가 아니다. AAPL/COP/NOK는 due review 누락으로 추가매수만 차단했다.

## MCP 공백

- `alpha-vantage`: `provider_error`. Daily API rate limit circuit breaker가 열려 NEWS_SENTIMENT data를 사용할 수 없었다. 비차단 공백이며 retry_count=0, source_ref `wiki/evidence-store/sources/2026-05-30-0011-hourly-autopilot-research-mcp-preflight.json`.
- 나머지 research MCP: SEC EDGAR, FRED, Firecrawl, Yahoo Finance는 scheduler research preflight에서 usable/pass로 반영했다.

## 주문 계획

- Order plan: `wiki/trade-ledger/orders/2026-05-30-0011-hourly-autopilot.json`
- Planned orders: 3
- Submitted orders: 3
- Filled orders: GOOGL 1주 at $383.13, WMT 1주 at $115.00, NEE 1주 at $86.46
- Open orders after reconciliation: 0
- First blocking gate: 없음.

## 검증 결과

- Universe validator: PASS.
- MCP validator: PASS.
- Risk validator: PASS.

## 지표 설명

- `spread_pct`: `(ask - bid) / midpoint * 100`으로 계산한 호가 스프레드다. 정책 상한은 0.50%다.
- `quote_age_minutes`: order plan 작성 시점과 quote timestamp의 차이다. submit 상한은 20분이다.
- `mcp_coverage.used_in_score`: 해당 MCP evidence가 점수, confidence, risk, allocation 판단에 반영됐는지를 뜻한다.
- `sell_trigger_none`: risk trim policy의 활성 매도/축소 사유가 현재 evidence로 확인되지 않았다는 뜻이다.
- `validation_lifecycle`: filled validation buy가 1D/5D/20D 회고 시점에 도달했을 때 hold/add/trim/close 판단을 요구하는 정책이다.

## 산출물

- Manifest: `wiki/evidence-store/run-manifests/2026-05-30-0011-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-05-30-0011-hourly-autopilot.json`
- Report: `wiki/current-runs/daily/2026-05-30-0011-hourly-autopilot.md`

## 제출 및 사후 확인

| Symbol | Client order id | Status | Fill |
| --- | --- | --- | --- |
| GOOGL | `hourly-20260530-0011-buy-googl` | filled | 1주 at $383.13 |
| WMT | `hourly-20260530-0011-buy-wmt` | filled | 1주 at $115.00 |
| NEE | `hourly-20260530-0011-buy-nee` | filled | 1주 at $86.46 |

WMT initial `place_stock_order` call은 tool safety monitor에서 cancelled 되었고, 같은 client_order_id 조회가 404 및 open order 없음으로 reconciliation된 뒤 같은 client_order_id 1회 retry만 수행했다. 사후 reconciliation에서 client-id 주문 조회, open orders, positions, account, fill activities가 모두 확인됐다. Open US-equity orders는 `[]`이다. Post-trade snapshot: `wiki/trade-ledger/positions/2026-05-30-0011-hourly-autopilot-post-trade.json`.
