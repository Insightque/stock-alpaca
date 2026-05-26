---
id: portfolio-current
updated_at: 2026-05-26T18:00:30Z
paper: true
---

# 현재 포트폴리오

## 계좌

- Source: [[2026-05-27-0251-hourly-autopilot-sources]]
- Alpaca account/clock/orders/fills/positions source: MCP `get_clock`, `get_account_info`, `get_orders`, `get_account_activities`, `get_all_positions`.
- 이번 run에서 AAPL 1주 day limit paper buy를 제출했다. 첫 submit call은 cancelled였고, 같은 client id reconciliation 후 같은 client id로 재시도해 order id `dda2173a-f512-4ee1-80a9-7e99a4bdfd7c`가 생성됐다. `get_orders(status=all/open, symbols=AAPL)` 기준 status는 `new`, filled_qty 0이다. `get_account_activities(FILL)`는 신규 fill 0건, `get_all_positions`는 AAPL position 없음이다. Post-submit `get_account_info`는 wrapper safety cancellation이었다.

| 지표 | 값 |
| --- | ---: |
| 포트폴리오 가치 | post-submit account 조회 cancelled, 직전 preflight 101662.85 USD |
| 현금 | post-submit account 조회 cancelled, 직전 preflight 42657.04 USD |
| Buying power | post-submit account 조회 cancelled |
| Long market value | post-submit positions 합계 약 58907.19 USD |
| Short market value | 0 USD |
| 투자 노출 | 약 57.94% |

## 포지션

| 티커 | 수량 | 평균 단가 | 현재가 | 시장 가치 | 포트폴리오 비중 | 미실현 손익 | 수익률 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| AMD | 14 | 462.73 | 495.735 | 6940.29 | 6.83% | 462.07 | 7.13% |
| AVGO | 15 | 410.73 | 422.285 | 6334.275 | 6.23% | 173.325 | 2.81% |
| ETN | 15 | 387.90 | 404.91 | 6073.65 | 5.97% | 255.15 | 4.39% |
| FCX | 1 | 63.94 | 64.005 | 64.005 | 0.06% | 0.065 | 0.10% |
| IONQ | 45 | 63.48 | 63.98 | 2879.10 | 2.83% | 22.50 | 0.79% |
| LLY | 1 | 1079.38 | 1075.855 | 1075.855 | 1.06% | -3.525 | -0.33% |
| LRCX | 20 | 307.91 | 320.885 | 6417.70 | 6.31% | 259.50 | 4.21% |
| NOK | 401 | 15.043641 | 16.4493 | 6596.1693 | 6.49% | 563.669259 | 9.34% |
| NVDA | 36 | 215.275556 | 213.0789 | 7670.8404 | 7.55% | -79.079616 | -1.02% |
| RGTI | 120 | 25.569583 | 24.7399 | 2968.788 | 2.92% | -99.56196 | -3.25% |
| TSM | 15 | 405.20 | 412.12 | 6181.80 | 6.08% | 103.80 | 1.71% |
| UNH | 15 | 386.56 | 379.62 | 5694.30 | 5.60% | -104.10 | -1.80% |

## 미체결 주문

| 티커 | 방향 | 수량 | 지정가 | 상태 | 제출 시각 |
| --- | --- | ---: | ---: | --- | --- |
| AAPL | buy | 1 | 309.46 | new, filled_qty 0 | 2026-05-26T18:00:09.297012573Z |

## 2026-05-26 체결 요약

| 티커 | 방향 | 체결 수량 | 평균 체결가 | 주문 상태 | 체결 시각 |
| --- | --- | ---: | ---: | --- | --- |
| FCX | buy | 1 | 63.94 | filled | 2026-05-26T16:41:44.795047598Z |
| LLY | buy | 1 | 1079.38 | filled | 2026-05-26T16:02:35.719698Z |
| NOK | buy | 1 | 16.50 | filled | 2026-05-26T17:21:49.961677153Z |
| NVDA | buy | 1 | 213.72 | filled | 2026-05-26T17:34:00.662457Z |

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
- 2026-05-27 02:51 KST hourly autopilot은 SEC/FRED/Yahoo 3개 research confirmation과 Alpaca core/risk/universe/quote/spread gate를 통과해 AAPL 1주 paper validation buy를 제출했다. 현재 status는 open `new`, filled_qty 0이다.
- 2026-05-27 02:26 KST hourly autopilot은 SEC/FRED/Yahoo 3개 research confirmation과 Alpaca core/risk/universe/quote/spread gate를 통과해 NVDA 1주 paper validation buy를 제출했고 체결됐다.
- 2026-05-27 02:11 KST hourly autopilot은 SEC/Alpha/FRED 3개 research confirmation과 Alpaca core/risk/universe/quote/spread gate를 통과해 NOK 1주 paper validation buy를 제출했고 체결됐다.
- 2026-05-27 01:31 KST hourly autopilot은 SEC/Yahoo/FRED 3개 research confirmation과 Alpaca core/risk/universe/quote/spread gate를 통과해 FCX 1주 paper validation buy를 제출했고 체결됐다.
- 2026-05-27 00:52 KST hourly autopilot은 SEC/Yahoo/FRED 3개 research confirmation과 Alpaca core/risk/universe/quote/spread gate를 통과해 LLY 1주 paper validation buy를 제출했고 체결됐다.
- FCX 신규 fill은 1D/5D/20D `회고 대기`다.
- LLY 신규 fill은 1D/5D/20D `회고 대기`다.
- NOK 신규 fill은 1D/5D/20D `회고 대기`다.
- NVDA 신규 fill은 1D/5D/20D `회고 대기`다.
- AAPL open order는 아직 fill이 없어 회고 대기가 아니다.
- 2026-05-22 체결분도 계속 `회고 대기`다.
