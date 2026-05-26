---
id: portfolio-current
updated_at: 2026-05-26T17:35:00Z
paper: true
---

# 현재 포트폴리오

## 계좌

- Source: [[2026-05-27-0226-hourly-autopilot-sources]]
- Alpaca account/clock/orders/fills/positions source: MCP `get_clock`, `get_account_info`, `get_orders`, `get_account_activities`, `get_all_positions`.
- 이번 run에서 NVDA 1주 day limit paper buy가 체결됐다. `get_orders(status=all, symbols=NVDA)`가 fill을 확인했고 `get_orders(status=open)`은 open order 0건을 반환했다. `get_order_by_client_id`, post-fill `get_all_positions`, post-fill `get_account_activities`는 wrapper cancelled였으므로 포지션 표는 직전 Alpaca preflight position snapshot에 확인된 NVDA fill 1주를 반영한 추정 post-trade 상태다.

| 지표 | 값 |
| --- | ---: |
| 포트폴리오 가치 | 약 101643.29 USD |
| 현금 | 약 42657.04 USD |
| Buying power | post-fill account 조회 cancelled |
| Long market value | 약 58986.30 USD |
| Short market value | 0 USD |
| 투자 노출 | 약 58.03% |

## 포지션

| 티커 | 수량 | 평균 단가 | 현재가 | 시장 가치 | 포트폴리오 비중 | 미실현 손익 | 수익률 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| AMD | 14 | 462.73 | 497.29 | 6962.06 | 6.85% | 483.84 | 7.47% |
| AVGO | 15 | 410.73 | 422.575 | 6338.625 | 6.24% | 177.675 | 2.88% |
| ETN | 15 | 387.90 | 405.0175 | 6075.2625 | 5.98% | 256.7625 | 4.41% |
| FCX | 1 | 63.94 | 64.035 | 64.035 | 0.06% | 0.095 | 0.15% |
| IONQ | 45 | 63.48 | 64.0037 | 2880.1665 | 2.83% | 23.5665 | 0.83% |
| LLY | 1 | 1079.38 | 1078.70 | 1078.70 | 1.06% | -0.68 | -0.06% |
| LRCX | 20 | 307.91 | 320.23 | 6404.60 | 6.30% | 246.40 | 4.00% |
| NOK | 401 | 15.043641 | 16.495 | 6614.495 | 6.51% | 581.994959 | 9.65% |
| NVDA | 36 | 215.275556 | 213.77 | 7695.72 | 7.57% | -54.20 | -0.70% |
| RGTI | 120 | 25.569583 | 25.195 | 3023.40 | 2.97% | -44.94996 | -1.46% |
| TSM | 15 | 405.20 | 412.11 | 6181.65 | 6.08% | 103.65 | 1.71% |
| UNH | 15 | 386.56 | 378.44 | 5676.60 | 5.58% | -121.80 | -2.10% |

## 미체결 주문

| 티커 | 방향 | 수량 | 지정가 | 상태 | 제출 시각 |
| --- | --- | ---: | ---: | --- | --- |
| 없음 | - | 0 | - | NVDA 주문 filled 후 `get_orders(status=open)` 0건 확인 | 2026-05-26T17:34Z 확인 |

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
- 2026-05-27 02:26 KST hourly autopilot은 SEC/FRED/Yahoo 3개 research confirmation과 Alpaca core/risk/universe/quote/spread gate를 통과해 NVDA 1주 paper validation buy를 제출했고 체결됐다.
- 2026-05-27 02:11 KST hourly autopilot은 SEC/Alpha/FRED 3개 research confirmation과 Alpaca core/risk/universe/quote/spread gate를 통과해 NOK 1주 paper validation buy를 제출했고 체결됐다.
- 2026-05-27 01:31 KST hourly autopilot은 SEC/Yahoo/FRED 3개 research confirmation과 Alpaca core/risk/universe/quote/spread gate를 통과해 FCX 1주 paper validation buy를 제출했고 체결됐다.
- 2026-05-27 00:52 KST hourly autopilot은 SEC/Yahoo/FRED 3개 research confirmation과 Alpaca core/risk/universe/quote/spread gate를 통과해 LLY 1주 paper validation buy를 제출했고 체결됐다.
- FCX 신규 fill은 1D/5D/20D `회고 대기`다.
- LLY 신규 fill은 1D/5D/20D `회고 대기`다.
- NOK 신규 fill은 1D/5D/20D `회고 대기`다.
- NVDA 신규 fill은 1D/5D/20D `회고 대기`다.
- 2026-05-22 체결분도 계속 `회고 대기`다.
