# 2026-05-30-0351-hourly-autopilot scheduled paper autopilot

## 요약

- 세션: regular paper submit workflow, Alpaca clock `2026-05-29T14:51:11.825723747-04:00` 기준 시장 open.
- Paper mode: `ALPACA_PAPER_TRADE=true` 확인.
- Scheduler stale cleanup: `pass`, remaining open orders `0`.
- Alpaca core preflight: hard gate `pass`; account/clock/positions/open orders/recent fills/quotes를 scheduler-owned MCP evidence로 사용했다.
- Research MCP: SEC EDGAR, FRED, Firecrawl, Yahoo Finance pass; Alpha Vantage는 `provider_error` gap으로 분류했다. 최소 research confirmation 3개를 넘어서 MCP strict gate는 통과 대상이다.
- Validators: universe/MCP/risk validation은 아래 검증 결과를 따른다. 주문 계획은 empty-order이며 현재 32개 position을 포함한다.
- 결론: 주문 없음. 매도/트림 후보를 먼저 평가했지만 정상 sell gate를 통과한 활성 트리거가 없었고, 신규 매수 후보는 same-session validation exposure, validation lifecycle, thesis/portfolio-fit/target-band 제약으로 제외했다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| paper mode | PASS | env 확인, 값은 secret 없이 boolean만 확인 |
| market clock | PASS | `2026-05-29T14:51:11.825723747-04:00`, regular session open |
| stale order cleanup | PASS | `wiki/evidence-store/sources/2026-05-30-0351-hourly-autopilot-stale-order-cleanup.json` |
| Alpaca core | PASS | `wiki/evidence-store/sources/2026-05-30-0351-hourly-autopilot-alpaca-core-preflight.json` |
| research MCP | PASS | 4 usable/pass, Alpha Vantage `provider_error` gap |
| universe | PASS | broad 62-symbol universe, SPY/QQQ 포함 |
| risk | PASS | empty-order plan, positions 32개 포함; expected warning `orders is empty` |

## 매도/트림 진단

| Symbol | 보유수량 | 진단 | 결정 |
| --- | ---: | --- | --- |
| AMD | 14 | AI semiconductor target-band warning area이나 active trim trigger 미확인, AMD quote spread도 sell gate 초과 | watch |
| PLTR | 1 | 수익 상태지만 overheat reversal trigger 없음 | watch |
| RGTI | 120 | speculative loss-control threshold 이내, close trigger 없음 | watch |

## 매수 후보

| Symbol | 상태 | 제외 사유 |
| --- | --- | --- |
| SBUX | watch | spread는 통과하지만 maintained thesis evidence와 portfolio-fit 우위가 신규 검증주문 기준에 미달 |
| CAT | watch | spread는 통과하지만 신규 노출 우선순위와 source thesis evidence가 부족 |
| SPY | watch | same-session validation exposure |
| QQQ | watch | same-session validation exposure |
| SLB | watch | 최근 same-session validation exposure와 포트폴리오 우선순위 제약 |
| AAPL/COP/NOK | add blocked | due validation lifecycle review pending |
| NVDA/SMH | add blocked | AI semiconductor target-band controls |

## 주문 계획

주문 계획: `wiki/trade-ledger/orders/2026-05-30-0351-hourly-autopilot.json`

`orders`는 빈 배열이다. 현재 account invested exposure가 존재하므로 Alpaca preflight의 32개 current positions를 order plan에 포함했다.

## 지표 설명

- `mcp_coverage`: Alpaca core 및 SEC/Alpha/FRED/Firecrawl/Yahoo research evidence의 사용 가능 여부다. Core는 필수이고 research는 최소 3개 usable/pass가 필요하다.
- `sell_candidate_diagnostics`: 실제 주문이 없더라도 매도/트림 후보를 매수보다 먼저 평가했다는 audit trail이다.
- `validation_lifecycle`: filled validation buy가 review due 상태이면 해당 symbol의 추가 매수를 막는다.
- `spread_pct`: `(ask-bid)/mid*100`이며 risk policy 한도는 0.50%다.
- `risk_open_order_lifecycle`: stale/open autopilot 주문이 정리되지 않으면 신규 주문을 막는 gate다.
