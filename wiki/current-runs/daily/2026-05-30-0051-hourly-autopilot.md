# 2026-05-30-0051-hourly-autopilot

## 요약

정규장 scheduled paper autopilot을 실행했다. `ALPACA_PAPER_TRADE=true`를 확인했고, scheduler-owned Alpaca core preflight와 registered Alpaca MCP spot check 모두 정규장 open 상태를 확인했다. 이번 run에서는 신규 paper 주문을 제출하지 않았다.

가장 중요한 이유는 00:31 KST run의 MRK 1주 buy 주문이 아직 `new` 상태로 열려 있기 때문이다. 이 주문은 15:54 UTC 기준 약 17.0분 경과로 stale 기준 30분보다 짧아 취소 대상이 아니며, 동일 symbol/side 중복 주문만 차단한다. 나머지 shortlist는 same-session validation buy 중복, ticker thesis evidence 부족, validation lifecycle review 미작성, 또는 AI semiconductor target-band 제한 때문에 최종 주문 후보가 되지 않았다.

## 게이트

| 항목 | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | 환경값 존재 확인, 값은 기록하지 않음 |
| Market clock | PASS | Alpaca clock 2026-05-29T11:54:18-04:00 open |
| Alpaca core MCP | PASS | `wiki/evidence-store/sources/2026-05-30-0051-hourly-autopilot-alpaca-core-preflight.json` |
| Research MCP | PASS | SEC EDGAR/FRED/Firecrawl/Yahoo pass, Alpha Vantage provider_error nonblocking |
| Universe strict | PASS | 62 symbols + SPY/QQQ |
| Open-order lifecycle | PASS with duplicate block | MRK fresh open order, stale cleanup cancel 대상 아님 |
| Risk validator | PASS | empty order plan, `orders is empty` warning only |
| Submit | SKIP | eligible order 없음 |

## 후보 판단

| Symbol | 판단 | 이유 |
| --- | --- | --- |
| MRK | watch/open | 기존 hourly buy 1주가 `new`; duplicate symbol-side buy 금지 |
| SPY/QQQ | skip | 같은 ET regular session에서 이미 validation buy 제출 |
| MCD | skip | preflight research evidence는 있으나 유지 중인 ticker thesis page가 없어 thesis gate 미충족 |
| NVDA/SMH | skip | AI semiconductor theme/factor/cluster target-band warning에서 같은 노출 추가 제한 |
| AAPL/COP/NOK | skip | due validation lifecycle review 미작성으로 add 차단 |

## Sell/Trim 진단

| Symbol | 판단 | 이유 |
| --- | --- | --- |
| AMD | watch | AI semiconductor warning band 진단 대상이나 deterioration/overheat reversal/stale-thesis trigger 없음 |
| PLTR | watch | 수익 상태지만 overheat reversal 조건 미확인 |
| RGTI | watch | speculative loss-control threshold 미충족 |

## 산출물

- Manifest: `wiki/evidence-store/run-manifests/2026-05-30-0051-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-05-30-0051-hourly-autopilot.json`
- Position/open-order snapshot: `wiki/trade-ledger/positions/2026-05-30-0051-hourly-autopilot-post-trade.json`
- Scheduler cleanup: `wiki/evidence-store/sources/2026-05-30-0051-hourly-autopilot-stale-order-cleanup.json`
- Alpaca core preflight: `wiki/evidence-store/sources/2026-05-30-0051-hourly-autopilot-alpaca-core-preflight.json`
- Research preflight: `wiki/evidence-store/sources/2026-05-30-0051-hourly-autopilot-research-mcp-preflight.json`

## 지표 설명

- `mcp_coverage`: Alpaca core와 research MCP의 사용 가능 여부 및 점수 반영 여부다.
- `sell_candidate_diagnostics`: 주문이 없어도 보유 종목의 trim/exit 후보를 매번 남기는 진단 필드다.
- `validation_lifecycle`: validation buy 이후 1D/5D/20D review가 필요한지와 추가매수 차단 여부를 기록한다.
- `open_order_lifecycle`: stale unfilled hourly order가 남아 있는지, fresh open order가 중복 주문만 막는지 판단한다.
