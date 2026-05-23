---
id: 2026-05-23-intraday-scalping-feature-filter-sources
created_at: 2026-05-23T18:45:00+09:00
source_type: alpaca-market-data-rest
paper: true
---

# 단타 성과 개선용 추가 필터 원천

## 목적

단타 성과를 올리기 위해 어떤 추가 정보와 분석법이 필요한지 확인하고, 이를 `intraday-rs-breakout-v0`에 적용해 재시뮬레이션하기 위한 원천 기록이다.

## 데이터 원천

- 가격: Alpaca Market Data API, IEX feed.
- 사용 bars:
  - `1Day`: 전일 종가와 gap 계산.
  - `1Hour`: 기존 신호 계산.
  - `1Min`: VWAP, opening range, sector breadth, stop/take/EOD 순서 계산.
- 조회 범위: 2026-01-20~2026-05-23.
- 검증 표본: 기존 단타 검증에서 사용한 28개 거래일.
- 후보군: QQQ, SMH, NVDA, AMD, TSLA, PLTR, AVGO, TSM, LRCX.

## 추가로 검토한 정보

| 정보 | 목적 | 계산 방식 |
| --- | --- | --- |
| 종목 VWAP | 장중 평균 매수가보다 위에서 유지되는지 확인 | 09:30~11:00 ET 1분봉 volume-weighted average |
| QQQ VWAP | 시장 전체가 당일 평균 위에 있는지 확인 | QQQ 09:30~11:00 ET VWAP 대비 11:00 진입가 |
| SMH VWAP | 반도체/AI 섹터가 당일 평균 위에 있는지 확인 | SMH 09:30~11:00 ET VWAP 대비 11:00 진입가 |
| 반도체 breadth | 개별 종목만 튄 것인지 섹터 동반 상승인지 확인 | SMH, NVDA, AMD, AVGO, TSM, LRCX 중 11:00 진입가가 당일 open보다 높은 종목 수 |
| opening range breakout | 개장 초반 고점을 재돌파하는지 확인 | 09:30~10:00 ET high 대비 11:00 진입가 |
| gap filter | 과도한 gap-up 후 fade 위험 회피 | 당일 open / 전일 close - 1 |

## 데이터 공백과 한계

- IEX feed 기준이라 전체 SIP 기준 VWAP과 다를 수 있다.
- 실제 bid/ask spread, limit fill 실패, slippage는 아직 반영하지 않았다.
- 뉴스 sentiment와 옵션 flow는 이번 feature filter에는 넣지 않았다.
- 이번 결과는 과거 28개 표본에 대한 재검증이며, 다음 정규장에서 실시간 paper dry-run이 필요하다.
