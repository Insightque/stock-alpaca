---
id: portfolio-current
updated_at: 2026-05-26T16:43:00Z
paper: true
---

# 현재 포트폴리오

## 계좌

- Source: [[2026-05-27-0131-hourly-autopilot-sources]]
- Alpaca account/clock/orders/fills/positions source: MCP `get_clock`, `get_account_info`, `get_orders`, `get_account_activities`, `get_all_positions`.
- 이번 run에서 FCX 1주 day limit paper buy가 체결됐다. `get_account_activities` reconciliation은 MCP safety wrapper에서 cancelled 되었지만, order endpoint와 position endpoint가 fill을 확인했다.

| 지표 | 값 |
| --- | ---: |
| 포트폴리오 가치 | 101535.19 USD |
| 현금 | 42887.26 USD |
| Buying power | 137824.45 USD |
| Long market value | 58647.93 USD |
| Short market value | 0 USD |
| 투자 노출 | 약 57.76% |

## 포지션

| 티커 | 수량 | 평균 단가 | 현재가 | 시장 가치 | 포트폴리오 비중 | 미실현 손익 | 수익률 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| AMD | 14 | 462.73 | 494.71 | 6925.94 | 6.82% | 447.72 | 6.91% |
| AVGO | 15 | 410.73 | 421.88 | 6328.20 | 6.23% | 167.25 | 2.71% |
| ETN | 15 | 387.90 | 406.92 | 6103.80 | 6.01% | 285.30 | 4.90% |
| FCX | 1 | 63.94 | 63.935 | 63.935 | 0.06% | -0.005 | -0.01% |
| IONQ | 45 | 63.48 | 63.89 | 2875.05 | 2.83% | 18.45 | 0.65% |
| LLY | 1 | 1079.38 | 1079.92 | 1079.92 | 1.06% | 0.54 | 0.05% |
| LRCX | 20 | 307.91 | 317.19 | 6343.80 | 6.25% | 185.60 | 3.01% |
| NOK | 400 | 15.04 | 16.475 | 6590.00 | 6.49% | 574.00 | 9.54% |
| NVDA | 35 | 215.32 | 213.0601 | 7457.1035 | 7.34% | -79.0965 | -1.05% |
| RGTI | 120 | 25.569583 | 25.315 | 3037.80 | 2.99% | -30.54996 | -1.00% |
| TSM | 15 | 405.20 | 410.69 | 6160.35 | 6.07% | 82.35 | 1.35% |
| UNH | 15 | 386.56 | 377.4579 | 5661.8685 | 5.58% | -136.5315 | -2.35% |

## 미체결 주문

| 티커 | 방향 | 수량 | 지정가 | 상태 | 제출 시각 |
| --- | --- | ---: | ---: | --- | --- |
| 없음 | - | 0 | - | FCX 주문 filled 후 open orders 없음 | 2026-05-26T16:43Z 확인 |

## 2026-05-26 체결 요약

| 티커 | 방향 | 체결 수량 | 평균 체결가 | 주문 상태 | 체결 시각 |
| --- | --- | ---: | ---: | --- | --- |
| FCX | buy | 1 | 63.94 | filled | 2026-05-26T16:41:44.795047598Z |
| LLY | buy | 1 | 1079.38 | filled | 2026-05-26T16:02:35.719698Z |

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
- 2026-05-27 01:31 KST hourly autopilot은 SEC/Yahoo/FRED 3개 research confirmation과 Alpaca core/risk/universe/quote/spread gate를 통과해 FCX 1주 paper validation buy를 제출했고 체결됐다.
- 2026-05-27 00:52 KST hourly autopilot은 SEC/Yahoo/FRED 3개 research confirmation과 Alpaca core/risk/universe/quote/spread gate를 통과해 LLY 1주 paper validation buy를 제출했고 체결됐다.
- FCX 신규 fill은 1D/5D/20D `회고 대기`다.
- LLY 신규 fill은 1D/5D/20D `회고 대기`다.
- 2026-05-22 체결분도 계속 `회고 대기`다.
