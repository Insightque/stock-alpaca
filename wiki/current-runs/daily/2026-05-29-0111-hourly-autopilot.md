# 2026-05-29 01:11 KST 정규장 hourly autopilot

## 실행 요약

- 실행 ID: `2026-05-29-0111-hourly-autopilot`
- 모드: `submit`, paper only
- 시장 시계: scheduler Alpaca core preflight `pass`, 등록 Alpaca MCP fresh clock `2026-05-28T12:15:00.685556747-04:00` ET open, next close `2026-05-28T16:00:00-04:00`
- stale order cleanup: `wiki/evidence-store/sources/2026-05-29-0111-hourly-autopilot-stale-order-cleanup.json` status `pass`, stale candidates 없음, remaining open orders 없음.
- Alpaca core: scheduler preflight hard gate `pass`; 등록 Alpaca MCP로 clock, open orders, XOM quote, XOM asset을 재확인했다.
- Research MCP: SEC EDGAR, FRED, Firecrawl, Yahoo Finance pass; Alpha Vantage는 `empty_response` gap. 최소 3개 research confirmation 충족.

## 후보와 주문 계획

| 티커 | 방향 | 수량 | limit | spread | quote age | confidence | 근거 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| XOM | buy | 1 | 148.37 | 0.0742% | 0.0분 | 0.58 | 에너지/가치 인플레이션 헤지 성격의 1주 검증 매수. 기존 XOM 보유는 작고, fresh quote와 open-order lifecycle이 통과했으며 research threshold를 충족했다. 당일 주문 수가 많아 남은 한 슬롯만 사용했다. |

## Gate 상태

- Paper mode: `ALPACA_PAPER_TRADE=true`
- Universe gate: broad metadata universe 62개, SPY/QQQ 포함, final candidates 3개(XOM/NEE/INTC).
- MCP gate: Alpaca core pass + research 4/5 pass, Alpha Vantage `empty_response` gap 기록.
- Quote/spread: XOM quote `2026-05-28T16:15:13.733333989Z`, 20분 이내, 0.50% 이하.
- Open-order lifecycle: scheduler stale cleanup pass 및 등록 Alpaca MCP open US equity order 0건.
- Daily order cap: 이번 실행 전 19건으로 계산, XOM 1건만 계획해 policy cap 20건에 맞췄다.
- Risk validator: PASS. 계획 buy notional 148.37달러, post-cash 37,187.61달러, post-invested 65,266.84달러.

## 제출/체결 결과

| 티커 | client_order_id | 상태 | 체결 수량 | 평균 체결가 | 비고 |
| --- | --- | --- | ---: | ---: | --- |
| XOM | hourly-20260529-0111-xom-buy-01 | filled | 1 | 148.37 | Alpaca MCP `place_stock_order` 1회 제출 후 client-order-id reconciliation에서 체결 확인 |

Post-trade reconciliation: XOM client-order-id PASS, open US equity orders 0건, positions refresh PASS(XOM qty=2, avg_entry_price=147.72), FILL activity PASS. account refresh는 runtime `cancelled` gap으로 기록하고 scheduler account preflight를 fallback으로 남겼다. XOM은 `회고 대기`로 표시한다.

## 지표 설명

- `spread`: ask와 bid의 차이를 중간가격으로 나눈 값이다. 정책 한도는 0.50%다.
- `quote age`: 주문 판단 시각과 Alpaca latest quote timestamp의 차이다. submit 한도는 20분이다.
- `confidence`: 추천 정책의 후보 품질, 리서치 확인, 분산 효과, 리스크를 합친 0~1 점수다.
- `expected adverse move`: 20거래일 안에 감수할 수 있는 불리한 변동 가정이다.
