---
id: portfolio-current
updated_at: 2026-05-27T14:39:53Z
paper: true
---

# Portfolio Current

2026-05-27 23:39 KST hourly autopilot post-trade reconciliation 기준.

## Account

| 항목 | 값 |
| --- | ---: |
| Portfolio value | 100,853.90 USD |
| Cash | 41,505.99 USD |
| Buying power | 135,667.60 USD |
| Long market value | 59,347.91 USD |
| Short market value | 0.00 USD |

## 이번 run 체결

| 티커 | 방향 | 수량 | 평균 체결가 | client_order_id |
| --- | --- | ---: | ---: | --- |
| AMZN | buy | 1 | 270.05 | `hourly-20260527-2331-amzn-buy-1` |
| BAC | buy | 1 | 52.06 | `hourly-20260527-2331-bac-buy-1` |
| XOM | buy | 1 | 147.07 | `hourly-20260527-2331-xom-buy-1` |

## 미체결 주문

| 티커 | 방향 | 수량 | 지정가 | 상태 | client_order_id |
| --- | --- | ---: | ---: | --- | --- |
| GOOGL | buy | 1 | 390.57 | new | `hourly-20260527-2311-googl-buy-1` |

## 보유 포지션 요약

Post-trade Alpaca MCP `get_all_positions`에서 AMZN, BAC, XOM 신규 long 포지션이 확인됐다. 세 종목 모두 1주 validation size이며 1D/5D/20D 회고 대상이다.

Source: `wiki/evidence-store/sources/2026-05-27-2331-hourly-autopilot-post-trade.json`.
