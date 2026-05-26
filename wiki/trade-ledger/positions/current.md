---
id: portfolio-current
updated_at: 2026-05-26T19:20:00Z
paper: true
---

# 현재 포트폴리오

## 계좌

- Source: [[2026-05-27-0411-hourly-autopilot-sources]]
- Alpaca account/clock/orders/fills/positions source: MCP `get_clock`, `get_account_info`, `get_orders`, `get_account_activities`, `get_all_positions`.
- 이번 run에서 AMZN 1주 day limit paper buy를 제출했다. Order id `642f83f9-cce5-4555-b4eb-9bee644d8545`, client_order_id `hourly-20260527-0411-amzn-buy-1`이며 `get_orders(status=open)` 기준 status는 `new`, filled_qty 0이다. `get_account_activities(FILL, after=2026-05-26T19:10:00Z)`는 신규 fill 0건이다. Post-submit symbol-filtered order query, `get_order_by_id`, positions/account refresh는 wrapper/user cancellation이었다.

| 지표 | 값 |
| --- | ---: |
| 포트폴리오 가치 | post-submit account 조회 cancelled, 직전 preflight 101684.58 USD |
| 현금 | post-submit account 조회 cancelled, 직전 preflight 42347.59 USD |
| Buying power | post-submit account 조회 cancelled, 직전 preflight 137455.77 USD |
| Long market value | post-submit positions 조회 cancelled, 직전 preflight 59336.99 USD |
| Short market value | 0 USD |
| 투자 노출 | 직전 preflight 기준 약 58.35% |

## 포지션

| 티커 | 수량 | 평균 단가 | 현재가 | 시장 가치 | 포트폴리오 비중 | 미실현 손익 | 수익률 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| AAPL | 1 | 309.45 | 308.945 | 308.945 | 0.30% | -0.505 | -0.16% |
| AMD | 14 | 462.73 | 506.42 | 7089.88 | 6.97% | 611.66 | 9.44% |
| AVGO | 15 | 410.73 | 423.41 | 6351.15 | 6.25% | 190.20 | 3.09% |
| ETN | 15 | 387.90 | 404.055 | 6060.825 | 5.96% | 242.325 | 4.17% |
| FCX | 1 | 63.94 | 64.075 | 64.075 | 0.06% | 0.135 | 0.21% |
| IONQ | 45 | 63.48 | 62.86 | 2828.70 | 2.78% | -27.90 | -0.98% |
| LLY | 1 | 1079.38 | 1072.77 | 1072.77 | 1.05% | -6.61 | -0.61% |
| LRCX | 20 | 307.91 | 322.4567 | 6449.134 | 6.34% | 290.934 | 4.72% |
| NOK | 401 | 15.043641 | 16.41 | 6580.41 | 6.47% | 547.909959 | 9.08% |
| NVDA | 36 | 215.275556 | 213.285 | 7678.26 | 7.55% | -71.660016 | -0.93% |
| RGTI | 120 | 25.569583 | 24.715 | 2965.80 | 2.92% | -102.54996 | -3.34% |
| TSM | 15 | 405.20 | 413.16 | 6197.40 | 6.09% | 119.40 | 1.96% |
| UNH | 15 | 386.56 | 379.705 | 5695.575 | 5.60% | -102.825 | -1.77% |

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
