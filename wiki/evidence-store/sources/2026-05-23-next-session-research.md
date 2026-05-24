---
id: 2026-05-23-next-session-research
captured_at: 2026-05-23T00:26:00+09:00
type: web-and-price-context
immutable: true
---

# 2026-05-23 다음 미국 거래일 유망종목 조사 원천 메모

## 범위

- 사용자 요청: 한국 시간 2026-05-23 토요일 기준 `내일 유망종목`.
- 해석: 한국 기준 내일 2026-05-24 일요일은 미국 정규장이 없고, 2026-05-25 월요일은 Memorial Day 휴장이다. 다음 미국 정규 거래일은 2026-05-26 화요일이다.
- 주문/매수/매도 실행: 없음. `ALPACA_PAPER_TRADE`는 현재 셸 환경에서 비어 있어 주문 워크플로우는 중단 조건이다.

## 휴장일 확인

- NYSE Holidays & Trading Hours: 2026년 Memorial Day는 Monday, May 25로 표시되어 있다. NYSE 정규장은 9:30 a.m. to 4:00 p.m. ET.
  - URL: https://www.nyse.com/trade/hours-calendars
- Nasdaq Trader calendar/alert: Nasdaq U.S. equities and options markets will be closed on Monday, May 25, 2026, in observance of Memorial Day.
  - URL: https://www.nasdaqtrader.com/trader.aspx?id=Calendar
  - URL: https://www.nasdaqtrader.com/TraderNews.aspx?id=ETA2026-27

## 2026-05-22 가격 캡처

Stooq CSV quote endpoint 캡처. 시간은 제공 원문 기준 `2026-05-22 17:11:45~17:11:50`.

Source URL:
https://stooq.com/q/l/?s=nvda.us+amd.us+avgo.us+lrcx.us+tsm.us+nok.us+etn.us+unh.us+ionq.us+rgti.us+pltr.us+tsla.us+qqq.us+smh.us+spy.us&f=sd2t2ohlcv&h&e=csv

| Symbol | Date | Time | Open | High | Low | Close | Volume |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| NVDA.US | 2026-05-22 | 17:11:50 | 220.904 | 221.01 | 215.16 | 217.11 | 45456191 |
| AMD.US | 2026-05-22 | 17:11:50 | 469.84 | 481.41 | 461.71 | 472.965 | 10089819 |
| AVGO.US | 2026-05-22 | 17:11:48 | 417.49 | 419.99 | 410.21 | 413.74 | 3646097 |
| LRCX.US | 2026-05-22 | 17:11:50 | 305.725 | 309.98 | 303.18 | 307.98 | 1128253 |
| TSM.US | 2026-05-22 | 17:11:50 | 409.48 | 410.67 | 404.73 | 407.3506 | 1709642 |
| NOK.US | 2026-05-22 | 17:11:50 | 14.71 | 15.4 | 14.575 | 15.355 | 55581195 |
| ETN.US | 2026-05-22 | 17:11:45 | 385.35 | 389.81 | 380.56 | 388.1 | 332966 |
| UNH.US | 2026-05-22 | 17:11:49 | 381.92 | 389.5 | 381.01 | 388.29 | 914290 |
| IONQ.US | 2026-05-22 | 17:11:50 | 58 | 64.86 | 58 | 63.92 | 17531300 |
| RGTI.US | 2026-05-22 | 17:11:50 | 22.96 | 26.495 | 22.66 | 26.0801 | 61082884 |
| PLTR.US | 2026-05-22 | 17:11:50 | 137.425 | 139.02 | 134.3 | 136.2317 | 9239743 |
| TSLA.US | 2026-05-22 | 17:11:50 | 422.665 | 430.83 | 420.51 | 430.14 | 15331029 |
| QQQ.US | 2026-05-22 | 17:11:50 | 718.07 | 721.33 | 715.95 | 720.54 | 8295259 |
| SMH.US | 2026-05-22 | 17:11:50 | 574.27 | 581.22 | 572.86 | 580.5 | 1697122 |
| SPY.US | 2026-05-22 | 17:11:50 | 746.24 | 748.16 | 744.48 | 746.8 | 6757230 |

## 뉴스/이벤트 원천

- NVIDIA Q1 FY27 results: 2026-05-20 보도. Q1 FY27 revenue는 81.615B USD, 전분기 대비 20%, 전년 대비 85%. Q2 FY27 revenue outlook는 91.0B USD ±2%, China Data Center compute revenue는 가정하지 않음.
  - URL: https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Announces-Financial-Results-for-First-Quarter-Fiscal-2027/default.aspx
- IonQ Q1 2026 results: 2026-05-06 보도. Q1 revenue 64.7M USD, 전년 대비 755%, FY revenue guidance 260M~270M USD, RPO 470M USD.
  - URL: https://www.sec.gov/Archives/edgar/data/1824920/000119312526208923/ionq-ex99_1.htm
- Rigetti Q1 2026 results: 2026-05-11 보도. Q1 revenue 4.4M USD, operating loss 26.0M USD, cash/investments 569.0M USD, 108-qubit Cepheus-1-108Q general availability.
  - URL: https://investors.rigetti.com/node/11041/pdf
- Nokia Q1 2026 slides: Q1 net sales 4.5B EUR, gross margin 45.5%, FCF 0.6B EUR, 10 customers publicly committed to work with Nokia on AI-RAN.
  - URL: https://www.nokia.com/system/files/2026-04/nokia_slides_2026_q1_fi.pdf
- Reuters/Investing.com semiconductor context: AI 반도체 랠리의 시장 주도와 과열/조정 리스크를 함께 지적.
  - URL: https://www.investing.com/news/stock-market-news/analysissizzling-semiconductor-trade-at-risk-of-cooling--and-stalling-us-stocks-rally-4683659
