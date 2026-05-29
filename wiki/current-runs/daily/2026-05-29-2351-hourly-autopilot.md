# 2026-05-29-2351-hourly-autopilot scheduled paper autopilot

## 요약

- 실행 모드: regular-session hourly autopilot, `mode=submit`, paper only.
- Paper gate: `ALPACA_PAPER_TRADE=true` 확인.
- 시장 clock: registered Alpaca MCP spot check 기준 `is_open=true`, timestamp `2026-05-29T10:57:16.658478066-04:00`.
- Alpaca core: scheduler-owned preflight hard gate `pass`와 nested spot checks(account/positions/open orders/quotes) 모두 사용. open US-equity orders는 `[]`.
- Research MCP: SEC EDGAR/FRED/Firecrawl/Yahoo Finance usable/pass, Alpha Vantage는 `provider_error` circuit breaker 공백이다. 최소 3개 research confirmation은 충족했다.
- 주문 계획: QQQ, V 각 1주 day limit paper validation buy. AAPL/COP/NOK 추가매수는 validation lifecycle due review 누락 때문에 차단했다.

## 게이트 상태

| Gate | 상태 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | 환경값 `ALPACA_PAPER_TRADE=true` |
| Market open | PASS | registered Alpaca MCP `get_clock`, `wiki/evidence-store/sources/2026-05-29-2351-hourly-autopilot-runtime-alpaca-spot-check.json` |
| Alpaca core MCP | PASS | account/positions/open orders/quotes preflight + spot checks |
| Stale/open-order lifecycle | PASS | `wiki/evidence-store/sources/2026-05-29-2351-hourly-autopilot-stale-order-cleanup.json` 및 spot `get_orders` 결과 open orders 없음 |
| Universe strict | PASS | broad universe 62개, SPY/QQQ 포함, shortlist 10개, final candidates 3개 |
| Research MCP tiered | PASS | 4 usable/pass providers, Alpha Vantage provider_error gap |
| Quote freshness/spread | PASS | QQQ/V quotes < 1분, spread 0.033%/0.163% |
| Risk validator | PASS | buy notional $1,069.29, post-cash $35,384.18 |
| Submit | DONE | QQQ/V Alpaca MCP day-limit paper buy 제출 및 체결 확인 |

## sell/trim 진단

보유 포지션을 신규 매수보다 먼저 점검했다. 이번 run에서는 open-order lifecycle이 해소됐지만, AMD/PLTR/RGTI 모두 YAML 활성 trim 조건을 충족하지 못해 주문이 아니라 watch 진단으로 남겼다.

| Symbol | Held qty | Weight % | Trigger | 판단 |
| --- | ---: | ---: | --- | --- |
| AMD | 14 | 7.047 | sell_trigger_none | AI semiconductor target-band watch, deterioration trigger 부족 |
| PLTR | 1 | 0.153 | sell_trigger_none | 과열 watch, reversal trigger 미확인 |
| RGTI | 120 | 2.932 | sell_trigger_none | 투기 포지션 약세 watch, speculative-loss trigger 미충족 |

## 후보 및 주문 판단

| Symbol | 판단 |
| --- | --- |
| QQQ | 1주 buy 계획. broad_index cluster로 AI semiconductor 집중을 늘리지 않고, quote/spread/MCP/risk 사전 조건이 양호하다. |
| V | 1주 buy 계획. 2026-05-27 validation lifecycle 1D 회고가 기록된 payments/growth_quality 보유 종목이며 분산 효과가 있다. |
| AAPL | 추가매수 차단. 1D validation lifecycle review가 due로 보이지만 아직 hold/add/trim/close 결정 기록이 없다. |
| BAC | final watch 후보. 1D 회고 기록은 있으나 이번 run에서는 V가 같은 financials cluster의 더 나은 분산/quality 후보라 BAC 추가매수는 보류했다. |
| COP | 추가매수 차단. 1D validation lifecycle review가 due로 보이지만 아직 결정 기록이 없다. |
| NOK | 추가매수 차단. 1D validation lifecycle review가 due로 보이지만 아직 결정 기록이 없다. |

## validation lifecycle

`risk_trim_policy.validation_lifecycle`를 적용했다. NKE/PFE/SO/WMT/NEE/AMZN/BAC/XOM/V는 `wiki/index.md` 기준 1D 회고가 기록되어 있고, same-day fill인 PFE/NKE/SO/SLB/AMZN은 아직 1D/5D/20D review due가 아니다. AAPL/COP/NOK는 due review 누락으로 추가매수만 차단했다.

## MCP 공백

- `alpha-vantage`: `provider_error`. Daily API rate limit circuit breaker가 열려 NEWS_SENTIMENT data를 사용할 수 없었다. 비차단 공백이며 retry_count=0, source_ref `wiki/evidence-store/sources/2026-05-29-2351-hourly-autopilot-research-mcp-preflight.json`.
- 나머지 research MCP: SEC EDGAR, FRED, Firecrawl, Yahoo Finance는 scheduler research preflight에서 usable/pass로 반영했다.

## 주문 계획

- Order plan: `wiki/trade-ledger/orders/2026-05-29-2351-hourly-autopilot.json`
- Planned orders: 2
- Submitted orders: 2
- Filled orders: QQQ 1주 at $737.62, V 1주 at $331.00
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

- Manifest: `wiki/evidence-store/run-manifests/2026-05-29-2351-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-05-29-2351-hourly-autopilot.json`
- Report: `wiki/current-runs/daily/2026-05-29-2351-hourly-autopilot.md`

## 제출 및 사후 확인

| Symbol | Client order id | Status | Fill |
| --- | --- | --- | --- |
| QQQ | `hourly-20260529-2351-buy-qqq` | filled | 1주 at $737.62 |
| V | `hourly-20260529-2351-buy-v` | filled | 1주 at $331.00 |

사후 reconciliation에서 client-id 주문 조회, open orders, positions, account, fill activities가 모두 확인됐다. Open US-equity orders는 `[]`이다. Post-trade snapshot: `wiki/trade-ledger/positions/2026-05-29-2351-hourly-autopilot-post-trade.json`.
