# 2026-05-30-0131-hourly-autopilot

## 요약

정규장 scheduled paper autopilot을 실행했다. `ALPACA_PAPER_TRADE=true`를 확인했고, scheduler-owned Alpaca core preflight는 clock/account/positions/open orders/recent activities/quotes hard gate를 통과했다. Research preflight는 SEC EDGAR, FRED, Firecrawl, Yahoo Finance 4개 확인을 제공했고 Alpha Vantage는 daily rate-limit `provider_error` gap으로 남았지만 최소 3개 research confirmation 기준은 충족했다.

이번 run에서는 신규 paper 주문을 제출하지 않았다. 01:31 KST stale cleanup과 Alpaca core preflight 모두 open order 0건을 기록해 `risk_open_order_lifecycle` 전역 block은 없었다. 다만 MRK는 같은 세션에서 이미 validation order가 제출된 뒤 cleanup된 후보라 강제 재주문하지 않았고, SPY/QQQ는 같은 세션 validation exposure, MCD는 ticker thesis evidence 부족, AAPL/COP/NOK는 due validation lifecycle review 미작성, NVDA/SMH는 AI semiconductor target-band 제한 때문에 주문 후보가 되지 않았다.

## 게이트

| 항목 | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | 환경값 존재 확인, 값은 기록하지 않음 |
| Market clock | PASS from scheduler preflight | Alpaca clock 2026-05-29T12:31:11.98430461-04:00 open |
| Alpaca core MCP | PASS | `wiki/evidence-store/sources/2026-05-30-0131-hourly-autopilot-alpaca-core-preflight.json`; clock/account/positions/open orders/recent activities/quotes pass |
| Stale order cleanup | PASS | `wiki/evidence-store/sources/2026-05-30-0131-hourly-autopilot-stale-order-cleanup.json`; stale candidates 0, remaining open orders 0 |
| Research MCP | PASS | SEC EDGAR/FRED/Firecrawl/Yahoo pass, Alpha Vantage provider_error nonblocking |
| Universe strict | PASS | 62 symbols + SPY/QQQ |
| Risk validator | PASS | empty order plan, `orders is empty` warning only |
| Submit | SKIP | eligible order 없음 |

## 후보 판단

| Symbol | 판단 | 이유 |
| --- | --- | --- |
| MRK | skip | 같은 ET session validation order가 cleanup된 뒤 같은 symbol/side 재주문을 강제하지 않음 |
| SPY/QQQ | skip | 같은 ET regular session에서 이미 validation buy 노출 존재 |
| MCD | skip | quote/spread는 관찰 가능하지만 유지 중인 ticker thesis page가 없어 thesis gate 미충족 |
| NVDA/SMH | skip | AI semiconductor theme/factor/cluster target-band warning에서 같은 노출 추가 제한 |
| AAPL/COP/NOK | skip | due validation lifecycle review 미작성으로 add 차단 |

## Sell/Trim 진단

| Symbol | 판단 | 이유 |
| --- | --- | --- |
| AMD | watch | AI semiconductor warning band 진단 대상이나 deterioration/overheat reversal/stale-thesis trigger 없음 |
| PLTR | watch | 수익 상태지만 overheat reversal 조건 미확인 |
| RGTI | watch | intraday 약세가 있으나 speculative loss-control threshold 미충족 |

## 산출물

- Manifest: `wiki/evidence-store/run-manifests/2026-05-30-0131-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-05-30-0131-hourly-autopilot.json`
- Position/open-order snapshot: `wiki/trade-ledger/positions/2026-05-30-0131-hourly-autopilot-post-trade.json`
- Scheduler cleanup: `wiki/evidence-store/sources/2026-05-30-0131-hourly-autopilot-stale-order-cleanup.json`
- Alpaca core preflight: `wiki/evidence-store/sources/2026-05-30-0131-hourly-autopilot-alpaca-core-preflight.json`
- Research preflight: `wiki/evidence-store/sources/2026-05-30-0131-hourly-autopilot-research-mcp-preflight.json`

## 지표 설명

- `mcp_coverage`: Alpaca core와 research MCP의 사용 가능 여부 및 점수 반영 여부다.
- `sell_candidate_diagnostics`: 주문이 없어도 보유 종목의 trim/exit 후보를 매번 남기는 진단 필드다.
- `validation_lifecycle`: validation buy 이후 1D/5D/20D review가 필요한지와 추가매수 차단 여부를 기록한다.
- `open_order_lifecycle`: stale unfilled hourly order가 남아 있는지, cleanup 이후 reconciliation이 주문 가능성을 막는지 판단한다.
