---
id: 2026-05-23-random-intraday-scalping-5x-sources
created_at: 2026-05-23T17:45:00+09:00
source_type: alpaca-market-data-rest
paper: true
---

# 2026년 2월~5월 무작위 시간별 단타 5회 반복 원천

## 목적

사용자 요청에 따라 2026년 2월부터 5월까지 임의 일자를 선정해 `intraday-rs-breakout-v0` 단타 정책을 5개 묶음으로 반복 검증하기 위한 원천 기록이다.

## 데이터 원천

- 가격: Alpaca Market Data API, IEX feed, `1Day` 및 `1Hour` bars.
- 뉴스: Alpaca News API, Benzinga source.
- 조회 시각: 2026-05-23 KST.
- 가격 조회 범위: 2026-02-01~2026-05-23.
- 후보군: QQQ, SPY, SMH, NVDA, AMD, TSLA, PLTR, AVGO, TSM, LRCX.
- 무작위 시드: `20260523`.

주의: 이번 실행은 market data와 news 조회만 수행했다. 실제 주문 제출은 없었고, API 키 값은 출력하지 않았다.

## 날짜 선정

앞선 두 차례 시뮬레이션에 사용한 날짜는 제외했다: 2026-03-09, 2026-03-31, 2026-03-30, 2026-04-02, 2026-03-26, 2026-03-02, 2026-03-20, 2026-04-14.

각 묶음은 무작위로 4개 거래일을 뽑아 앞의 3개를 학습 표본, 마지막 1개를 검증 표본으로 지정했다.

| 묶음 | 학습일 1 | 학습일 2 | 학습일 3 | 검증일 |
| --- | --- | --- | --- | --- |
| 1 | 2026-04-01 | 2026-04-27 | 2026-02-04 | 2026-03-13 |
| 2 | 2026-05-05 | 2026-02-12 | 2026-05-12 | 2026-03-05 |
| 3 | 2026-05-22 | 2026-02-20 | 2026-04-29 | 2026-02-09 |
| 4 | 2026-04-21 | 2026-05-13 | 2026-02-03 | 2026-02-06 |
| 5 | 2026-03-23 | 2026-04-22 | 2026-03-06 | 2026-04-08 |

## 해당일 주요 뉴스 맥락

뉴스는 진입 조건으로 쓰지 않고, 당일 가격 움직임의 배경 확인용으로만 사용했다.

| 날짜 | 주요 뉴스 맥락 |
| --- | --- |
| 2026-04-01 | Iran 외교/지정학, NATO 관련 매크로 뉴스 |
| 2026-04-27 | AVGO 장기 수익률 기사, Intel vs Nvidia 비교 기사 |
| 2026-02-04 | TSLA 소송/장기 수익률 기사 |
| 2026-03-13 | 자동차주 선호, Iran/Trump 지정학 뉴스 |
| 2026-05-05 | Trump/Iran Strait of Hormuz 관련 매크로 뉴스, 원유 재고 |
| 2026-02-12 | Taiwan-US trade pact, NVDA data center bond 관련 기사 |
| 2026-05-12 | TSLA/SpaceX, AMD 13F holding 관련 기사 |
| 2026-03-05 | NVDA orbital datacenter hiring, Together AI valuation 기사 |
| 2026-05-22 | 시장 사상 최고/정치 승인율, Fed chair 관련 뉴스 |
| 2026-02-20 | PLTR/AVGO 장기 수익률 기사 |
| 2026-04-29 | TSM 장기 수익률, Germany troop review 관련 뉴스 |
| 2026-02-09 | TSLA humanoid robot, Gordie Howe bridge 관련 매크로 뉴스 |
| 2026-04-21 | SOXX/SMH record inflows, 원유 재고 뉴스 |
| 2026-05-13 | TSM/PLTR 장기 수익률 기사 |
| 2026-02-03 | UK/US base deal, Fed Miran 관련 뉴스 |
| 2026-02-06 | Amazon/Google capex와 market low point 의견 기사, India-US trade news |
| 2026-03-23 | AMD 장기 수익률, Trump approval/Iran action 뉴스 |
| 2026-04-22 | TSLA capex/Intel/Musk, Trump approval/market high 뉴스 |
| 2026-03-06 | Kalshi/Polymarket valuation, China/FBI surveillance network 뉴스 |
| 2026-04-08 | Venezuela sanctions, NATO/Iran war support 관련 뉴스 |

## 데이터 공백과 한계

- `1Hour` bar는 IEX feed 기준이다. 전체 SIP 체결량과 다를 수 있다.
- 1시간봉으로 stop/take 체결 순서를 완전히 검증할 수 없다. 같은 bar 안에서 stop과 take가 모두 가능한 경우에는 분봉 검증이 필요하다.
- 2026-05-22까지의 데이터만 사용했다.
- 이번 5회 반복에서는 정책 파라미터를 조정하지 않고 고정 적용했다.
