---
id: 2026-05-25-one-year-hourly-trend-event-cache-sources
created_at: 2026-05-25T21:46:54+09:00
source_type: alpaca-mcp-trend-event-feature-cache
paper: true
orders_submitted: 0
---

# 과거 1년 1시간봉 시뮬레이션용 일별 동향 feature cache 원천

## 조회 원천

- Alpaca MCP: `get_news`
- Alpaca MCP hourly bars: previous-close market/sector trend 계산에 사용
- hourly bars JSON: `wiki/evidence-store/sources/2026-05-25-one-year-hourly-bars.json`
- raw news JSON: `wiki/evidence-store/sources/2026-05-25-one-year-hourly-alpaca-news.json`
- event cache JSON: `wiki/evidence-store/sources/2026-05-25-one-year-hourly-trend-event-feature-cache.json`
- source note: `wiki/evidence-store/sources/2026-05-25-one-year-hourly-trend-event-cache-sources.md`

## 캡처 결과

- Alpaca news articles captured: 38131
- event feature rows: 13570
- failed news pages: 0

## 데이터 공백

- 이번 cache는 광범위한 일별 동향 1차 보강이다.
- SEC filing, Alpha Vantage earnings, FRED macro, Firecrawl IR, Yahoo Finance analyst/news는 전 종목/전일자 풀 coverage로 결합하지 않았다.
- 뉴스 감성 점수는 headline/summary 키워드 기반의 보조 feature다.
- 모든 row의 `available_at`은 해당 미국 거래일 장 시작 시각으로 두고, 뉴스는 `available_at` 이전 3일 window만 집계했다.

## 실패 기록

- 없음
