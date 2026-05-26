---
id: portfolio-current
updated_at: 2026-05-26T19:53:30Z
paper: true
---

# 현재 포트폴리오

## 계좌

- Source: [[2026-05-27-0451-hourly-autopilot-sources]]
- Alpaca account/clock/orders/fills/positions source: MCP `get_clock`, `get_account_info`, `get_orders`, `get_account_activities`, `get_all_positions`.
- 이번 run에서는 신규 주문을 제출하지 않았다. Scheduler-owned Alpaca core preflight 기준 AMZN 1주 day limit paper buy는 order id `642f83f9-cce5-4555-b4eb-9bee644d8545`, client_order_id `hourly-20260527-0411-amzn-buy-1`, status `new`, filled_qty 0이다. AMZN open order age가 약 34.4분으로 risk lifecycle 30분 한도를 넘어 신규 주문은 차단했다.

| 지표 | 값 |
| --- | ---: |
| 포트폴리오 가치 | 101738.22 USD |
| 현금 | 42347.59 USD |
| Buying power | 137240.29 USD |
| Long market value | 59390.63 USD |
| Short market value | 0 USD |
| 투자 노출 | preflight 기준 약 58.38% |

## 포지션

| 티커 | 수량 | 평균 단가 | 현재가 | 시장 가치 | 포트폴리오 비중 | 미실현 손익 | 수익률 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| AAPL | 1 | 309.45 | 308.57 | 308.57 | 0.30% | -0.88 | -0.28% |
| AMD | 14 | 462.73 | 502.833 | 7039.662 | 6.92% | 561.442 | 8.67% |
| AVGO | 15 | 410.73 | 424.36 | 6365.40 | 6.26% | 204.45 | 3.32% |
| ETN | 15 | 387.90 | 404.06 | 6060.90 | 5.96% | 242.40 | 4.17% |
| FCX | 1 | 63.94 | 64.345 | 64.345 | 0.06% | 0.405 | 0.63% |
| IONQ | 45 | 63.48 | 63.50 | 2857.50 | 2.81% | 0.90 | 0.03% |
| LLY | 1 | 1079.38 | 1069.90 | 1069.90 | 1.05% | -9.48 | -0.88% |
| LRCX | 20 | 307.91 | 322.76 | 6455.20 | 6.35% | 297.00 | 4.82% |
| NOK | 401 | 15.043641 | 16.415 | 6582.415 | 6.47% | 549.915959 | 9.12% |
| NVDA | 36 | 215.275556 | 214.07 | 7706.52 | 7.57% | -43.40 | -0.56% |
| RGTI | 120 | 25.569583 | 25.055 | 3006.60 | 2.96% | -61.75 | -2.01% |
| TSM | 15 | 405.20 | 412.95 | 6194.25 | 6.09% | 116.25 | 1.91% |
| UNH | 15 | 386.56 | 378.425 | 5676.375 | 5.58% | -122.025 | -2.10% |

## 미체결 주문

| 티커 | 방향 | 수량 | 지정가 | 상태 | 제출 시각 |
| --- | --- | ---: | ---: | --- | --- |
| AMZN | buy | 1 | 263.10 | new, filled_qty 0 | 2026-05-26T19:19:07.508236707Z |

## 2026-05-26 체결 요약

| 티커 | 방향 | 체결 수량 | 평균 체결가 | 주문 상태 | 체결 시각 |
| --- | --- | ---: | ---: | --- | --- |
| FCX | buy | 1 | 63.94 | filled | 2026-05-26T16:41:44.795047598Z |
| LLY | buy | 1 | 1079.38 | filled | 2026-05-26T16:02:35.719698Z |
| NOK | buy | 1 | 16.50 | filled | 2026-05-26T17:21:49.961677153Z |
| NVDA | buy | 1 | 213.72 | filled | 2026-05-26T17:34:00.662457Z |
| AAPL | buy | 1 | 309.45 | filled | 2026-05-26T18:43:10.778359Z |

## 2026-05-22 체결 요약

| 티커 | 방향 | 체결 수량 | 평균 체결가 | 주문 상태 | 체결 시각 |
| --- | --- | ---: | ---: | --- | --- |
| AMD | buy | 14 | 462.73 | filled | 2026-05-22T14:24:31.832897Z |
| AVGO | buy | 15 | 410.73 | filled | 2026-05-22T14:24:36.546406Z |
| LRCX | buy | 20 | 307.91 | filled | 2026-05-22T14:24:43.090189Z |
| TSM | buy | 15 | 405.20 | filled | 2026-05-22T14:24:51.480151Z |
| NOK | buy | 400 | 15.04 | filled | 2026-05-22T14:24:53.609589Z |
| UNH | buy | 15 | 386.56 | filled | 2026-05-22T14:24:57.827179Z |
| ETN | buy | 15 | 387.90 | filled | 2026-05-22T14:24:59.966652Z |
| RGTI | buy | 120 | 25.569584 | filled | 2026-05-22T14:26:14.451446Z |
| IONQ | buy | 45 | 63.48 | filled | 2026-05-22T14:25:06.490660Z |
| NVDA | buy | 35 | 215.32 | filled | 2026-05-22T19:14:02.277181Z |

## 메모

- `ALPACA_PAPER_TRADE=true`를 `.env`에서 확인했다.
- 2026-05-27 04:51 KST hourly autopilot은 Alpaca core/universe/MCP/quote/spread는 통과했지만 AMZN open order age가 30분 한도를 넘어 risk gate FAIL로 신규 주문을 제출하지 않았다. AMZN은 계속 open `new`, filled_qty 0이다.
- 2026-05-27 04:11 KST hourly autopilot은 SEC/FRED/Yahoo 3개 research confirmation과 Alpaca core/risk/universe/quote/spread gate를 통과해 AMZN 1주 paper validation buy를 제출했다. 현재 status는 open `new`, filled_qty 0이다.
- 2026-05-27 02:51 KST hourly autopilot은 SEC/FRED/Yahoo 3개 research confirmation과 Alpaca core/risk/universe/quote/spread gate를 통과해 AAPL 1주 paper validation buy를 제출했고 체결됐다.
- 2026-05-27 02:26 KST hourly autopilot은 SEC/FRED/Yahoo 3개 research confirmation과 Alpaca core/risk/universe/quote/spread gate를 통과해 NVDA 1주 paper validation buy를 제출했고 체결됐다.
- 2026-05-27 02:11 KST hourly autopilot은 SEC/Alpha/FRED 3개 research confirmation과 Alpaca core/risk/universe/quote/spread gate를 통과해 NOK 1주 paper validation buy를 제출했고 체결됐다.
- 2026-05-27 01:31 KST hourly autopilot은 SEC/Yahoo/FRED 3개 research confirmation과 Alpaca core/risk/universe/quote/spread gate를 통과해 FCX 1주 paper validation buy를 제출했고 체결됐다.
- 2026-05-27 00:52 KST hourly autopilot은 SEC/Yahoo/FRED 3개 research confirmation과 Alpaca core/risk/universe/quote/spread gate를 통과해 LLY 1주 paper validation buy를 제출했고 체결됐다.
- FCX 신규 fill은 1D/5D/20D `회고 대기`다.
- LLY 신규 fill은 1D/5D/20D `회고 대기`다.
- NOK 신규 fill은 1D/5D/20D `회고 대기`다.
- NVDA 신규 fill은 1D/5D/20D `회고 대기`다.
- AAPL 신규 fill은 1D/5D/20D `회고 대기`다.
- AMZN open order는 아직 fill이 없어 회고 대기가 아니다.
- 2026-05-22 체결분도 계속 `회고 대기`다.
