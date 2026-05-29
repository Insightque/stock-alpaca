# 2026-05-30-0111-hourly-autopilot

## 요약

정규장 scheduled paper autopilot을 실행했다. `ALPACA_PAPER_TRADE=true`를 확인했고, scheduler-owned Alpaca core preflight는 clock/account/positions/open orders/recent activities/quotes hard gate를 통과했다. Research preflight도 SEC EDGAR, FRED, Firecrawl, Yahoo Finance 4개 확인을 제공했고 Alpha Vantage는 rate-limit `provider_error` gap으로 남았지만 최소 3개 research confirmation 기준은 충족했다.

이번 run에서는 신규 paper 주문을 제출하지 않았다. 00:31 KST MRK validation buy는 scheduler stale cleanup에서 cancel 시도 후 `pending_cancel`로 남아 있었지만, decision time의 registered Alpaca MCP `get_orders` reconciliation에서는 open US-equity order가 0건이었다. 따라서 전역 open-order lifecycle block은 해소됐지만, MRK 같은 symbol/side를 강제로 재주문하지 않았고 나머지 후보도 same-session validation exposure, thesis evidence, validation lifecycle, target-band 조건 때문에 주문 후보가 되지 않았다.

## 게이트

| 항목 | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | 환경값 존재 확인, 값은 기록하지 않음 |
| Market clock | PASS from scheduler preflight | Alpaca clock 2026-05-29T12:11:11.356154616-04:00 open |
| Alpaca core MCP | PASS with spot-check caveat | `wiki/evidence-store/sources/2026-05-30-0111-hourly-autopilot-alpaca-core-preflight.json`; nested `get_clock` spot check는 `gap_category=cancelled`로 별도 기록, preflight hard gate와 positions/account/orders reconciliation 사용 |
| Stale order cleanup | PASS after reconciliation | `wiki/evidence-store/sources/2026-05-30-0111-hourly-autopilot-stale-order-cleanup.json`; MRK pending_cancel 후 registered `get_orders` open 0건 |
| Research MCP | PASS | SEC EDGAR/FRED/Firecrawl/Yahoo pass, Alpha Vantage provider_error nonblocking |
| Universe strict | PASS | 62 symbols + SPY/QQQ |
| Risk validator | PASS | empty order plan, `orders is empty` warning only |
| Submit | SKIP | eligible order 없음 |

## 후보 판단

| Symbol | 판단 | 이유 |
| --- | --- | --- |
| MRK | skip | 00:31 KST 같은 ET session validation buy가 이미 제출됐고 cleanup 이후 강제 재주문하지 않음 |
| SPY/QQQ | skip | 같은 ET regular session에서 이미 validation buy 노출 존재 |
| MCD | skip | preflight research evidence는 있으나 유지 중인 ticker thesis page가 없어 thesis gate 미충족 |
| NVDA/SMH | skip | AI semiconductor theme/factor/cluster target-band warning에서 같은 노출 추가 제한 |
| AAPL/COP/NOK | skip | due validation lifecycle review 미작성으로 add 차단 |

## Sell/Trim 진단

| Symbol | 판단 | 이유 |
| --- | --- | --- |
| AMD | watch | AI semiconductor warning band 진단 대상이나 deterioration/overheat reversal/stale-thesis trigger 없음 |
| PLTR | watch | 수익 상태지만 overheat reversal 조건 미확인 |
| RGTI | watch | intraday 약세가 있으나 speculative loss-control threshold 미충족 |

## 산출물

- Manifest: `wiki/evidence-store/run-manifests/2026-05-30-0111-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-05-30-0111-hourly-autopilot.json`
- Position/open-order snapshot: `wiki/trade-ledger/positions/2026-05-30-0111-hourly-autopilot-post-trade.json`
- Scheduler cleanup: `wiki/evidence-store/sources/2026-05-30-0111-hourly-autopilot-stale-order-cleanup.json`
- Alpaca core preflight: `wiki/evidence-store/sources/2026-05-30-0111-hourly-autopilot-alpaca-core-preflight.json`
- Research preflight: `wiki/evidence-store/sources/2026-05-30-0111-hourly-autopilot-research-mcp-preflight.json`

## 지표 설명

- `mcp_coverage`: Alpaca core와 research MCP의 사용 가능 여부 및 점수 반영 여부다.
- `sell_candidate_diagnostics`: 주문이 없어도 보유 종목의 trim/exit 후보를 매번 남기는 진단 필드다.
- `validation_lifecycle`: validation buy 이후 1D/5D/20D review가 필요한지와 추가매수 차단 여부를 기록한다.
- `open_order_lifecycle`: stale unfilled hourly order가 남아 있는지, cleanup 이후 reconciliation이 주문 가능성을 막는지 판단한다.
