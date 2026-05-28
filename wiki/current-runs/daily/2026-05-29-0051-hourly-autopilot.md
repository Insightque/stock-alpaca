# 2026-05-29 00:51 KST 정규장 hourly autopilot

## 실행 요약

- 실행 ID: `2026-05-29-0051-hourly-autopilot`
- 모드: `submit`, paper only
- 시장 시계: Alpaca scheduler preflight 기준 open, `2026-05-28T11:51:17.944282587-04:00` ET, next close `2026-05-28T16:00:00-04:00`
- stale order cleanup: `wiki/evidence-store/sources/2026-05-29-0051-hourly-autopilot-stale-order-cleanup.json` status `pass`, remaining open orders 없음. 직전 TSLA open은 cleanup/reconciliation 이후 포지션에 반영되어 신규 open-order lifecycle은 통과로 처리했다.
- Alpaca core: scheduler preflight hard gate `pass`; 등록 Alpaca MCP로 positions/open orders/quotes/snapshots를 재확인했다. account refresh와 FILL activity refresh는 runtime cancelled로 기록하되 scheduler preflight와 직전 post-trade snapshot을 보조 근거로 사용했다.
- Research MCP: SEC EDGAR, FRED, Firecrawl, Yahoo Finance pass; Alpha Vantage는 `empty_response` gap. 최소 3개 research confirmation 충족.

## 후보와 주문 계획

| 티커 | 방향 | 수량 | limit | spread | quote age | confidence | 근거 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| AMZN | buy | 1 | 270.55 | 0.0518% | 0.4분 | 0.62 | Mega-cap tech 보유 종목 1주 추가 검증. 오늘 정규장 동일 symbol/side 신규 주문이 없고 quote/spread가 신선하지만, cluster 노출을 고려해 1주로 제한한다. |
| INTC | buy | 1 | 120.81 | 0.0331% | 0.4분 | 0.60 | AI semiconductor complex의 고변동 대형주 1주 검증. 기존 반도체 노출이 커서 크기를 늘리지 않고, 정규장 동일 symbol/side 주문 부재와 MCP threshold 통과에 한정한다. |

## Gate 상태

- Paper mode: `ALPACA_PAPER_TRADE=true`
- Universe gate: broad metadata universe 62개, SPY/QQQ 포함, final candidates 3개(AMZN/INTC/WMT). WMT는 daily cap 때문에 재점검 후보로만 남기고 AMZN/INTC 2건만 계획한다.
- MCP gate: Alpaca core pass + research 4/5 pass, Alpha Vantage `empty_response` gap 기록.
- Quote/spread: 두 후보 모두 20분 이내, 0.50% 이하.
- Open-order lifecycle: scheduler stale cleanup pass 및 등록 Alpaca MCP open order 0건.
- Daily order cap: 이번 실행 전 18건, 계획 2건으로 policy cap 20건에 정확히 맞춘다. WMT는 final candidate로 기록하지만 cap 때문에 제출하지 않는다.
- Risk validator: PASS. 계획 buy notional 391.36달러, post-cash 37,215.17달러, post-invested 65,186.76달러.

## 제출/체결 결과

| 티커 | client_order_id | 상태 | 체결 수량 | 평균 체결가 | 비고 |
| --- | --- | --- | ---: | ---: | --- |
| AMZN | hourly-20260529-0051-amzn-buy-01 | filled | 1 | 270.55 | 첫 submit은 runtime cancelled, same client id 404 확인 후 same-id retry가 체결됨 |
| INTC | hourly-20260529-0051-intc-buy-01 | not submitted | 0 |  | 첫 submit cancelled, same client id 404 확인, same-id retry도 cancelled라 추가 재시도 중단 |

Post-trade reconciliation: AMZN client-order-id PASS, INTC client-order-id 404/not found, open US equity orders 0건, positions refresh PASS. account refresh와 FILL activity refresh는 runtime `cancelled` gap으로 기록했다. AMZN은 `회고 대기`로 표시한다.

## 지표 설명

- `spread`: ask와 bid의 차이를 중간가격으로 나눈 값이다. 정책 한도는 0.50%다.
- `quote age`: 주문 판단 시각과 Alpaca latest quote timestamp의 차이다. submit 한도는 20분이다.
- `confidence`: 추천 정책의 후보 품질, 리서치 확인, 분산 효과, 리스크를 합친 0~1 점수다.
- `expected adverse move`: 20거래일 안에 감수할 수 있는 불리한 변동 가정이다.
