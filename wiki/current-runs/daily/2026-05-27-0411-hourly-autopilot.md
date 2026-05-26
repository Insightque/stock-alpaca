# 2026-05-27-0411-hourly-autopilot hourly autopilot

## 요약

2026-05-27 04:11 KST scheduled paper autopilot은 AMZN 1주 paper validation buy를 제출했다. `.env`에서 `ALPACA_PAPER_TRADE=true`를 확인했고, scheduler-owned Alpaca core preflight는 market open, account, positions, open orders, recent activities, asset checks, quotes를 모두 `pass`로 제공했다.

- 첫 blocking gate: 없음
- 제출 주문: AMZN 1주 day limit buy, limit 263.10, status `new`
- 기존 open order: 0건
- 리서치 MCP usable/pass: SEC EDGAR, FRED, Yahoo Finance 3개
- Provider gap: Alpha Vantage `cancelled`, Firecrawl `wrapper_error`

## 계좌/시장 상태

| 항목 | 값 |
| --- | ---: |
| Market clock | 2026-05-26T15:11:05.905788802-04:00 open=True |
| Portfolio value | 101684.58 USD |
| Cash | 42347.59 USD |
| Buying power | 137455.77 USD |
| Positions | 13 |
| Open orders | 0 |

## 추천 Shortlist

| 순위 | Symbol | 판단 | 근거 | 주문 여부 |
| ---: | --- | --- | --- | --- |
| 1 | AMZN | 1주 validation buy | quote/spread pass, SEC/FRED/Yahoo pass, 보유 없음, semiconductor cluster 추가 회피 | 제출, status `new` |
| 2 | INTC | 재점검 후보 | quote/spread pass, local CIK 확인, turnaround risk와 AMZN 대비 낮은 확신 | 미제출 |
| 3 | AMAT | 재점검 후보 | 강한 semiconductor 장중 momentum, asset pass | 미제출: AI semiconductor cluster 부담 |

## Quote/Spread Gate

| Symbol | Bid | Ask | Spread % | Quote time | 상태 |
| --- | ---: | ---: | ---: | --- | --- |
| AMZN | 263.06 | 263.10 | 0.0152 | 2026-05-26T19:11:29.894160Z | pass |
| INTC | 122.46 | 122.58 | 0.0979 | 2026-05-26T19:11:29.842874Z | pass |
| AMAT | 454.30 | 454.58 | 0.0616 | 2026-05-26T19:11:25.907806Z | pass |
| SMH | 601.36 | 601.49 | 0.0216 | 2026-05-26T19:11:30.593469Z | pass |
| MU | 912.69 | 920.00 | 0.7977 | 2026-05-26T19:11:30.129809Z | fail |

## MCP Coverage

| MCP | 결과 | gap_category | 판단 반영 |
| --- | --- | --- | --- |
| Alpaca | pass | not_applicable | yes |
| SEC EDGAR | pass | not_applicable | yes |
| Alpha Vantage | failed | cancelled | no |
| FRED | pass | not_applicable | yes |
| Firecrawl | failed | wrapper_error | no |
| Yahoo Finance | usable | not_applicable | yes |

## 주문 계획

Order plan은 submit mode로 생성했고 `orders`에는 AMZN 1주 day limit buy 1건만 포함했다. AMZN은 같은 거래일 buy duplicate가 없고 open order도 없으며, 1주 notional은 cash reserve, invested ratio, ticker cap, theme/factor/cluster cap을 위반하지 않는다.

## 제출 및 사후 점검

제출 전 gate summary를 plain text로 기록한 뒤 Alpaca MCP `place_stock_order`만 사용했다. 제출 결과는 order id `642f83f9-cce5-4555-b4eb-9bee644d8545`, client_order_id `hourly-20260527-0411-amzn-buy-1`, status `pending_new`, filled_qty 0이었다. 이후 `get_orders(status=open)`에서 같은 order id/client id가 status `new`, filled_qty 0으로 확인됐다.

Post-trade FILL activity query after `2026-05-26T19:10:00Z`는 신규 fill 0건이었다. 따라서 AMZN은 open order이며 아직 fill review due가 아니다. Symbol-filtered order query, `get_order_by_id`, post-submit positions/account refresh는 wrapper/user cancellation이 있어 `gap_category=cancelled`로 기록했다.

## 검증 상태

검증 명령 실행 결과:

- Universe strict: PASS
- MCP strict: PASS
- Risk check: PASS. Buy notional 263.10 USD, post-order cash 42084.49 USD, post-order invested exposure 59606.024 USD.

## 지표 설명

- `spread %`: `(ask - bid) / midpoint * 100`. 0.5% 이내만 주문 후보로 본다.
- `MCP usable/pass`: 해당 provider 결과가 점수나 리스크 판단에 사용할 수 있는 상태다.
- `first_blocking_gate`: 주문 제출을 가장 먼저 막은 hard gate다. 이번 run은 검증 전 기준 blocking gate가 없다.
- `validation buy`: 수익 극대화보다 1D/5D/20D 회고용 근거 수집을 위한 1주 단위 paper 주문이다.

## 산출물

- Source note: `wiki/evidence-store/sources/2026-05-27-0411-hourly-autopilot-sources.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-05-27-0411-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-05-27-0411-hourly-autopilot.json`
