---
id: 2026-05-24-six-month-3h-simulation-sources
created_at: 2026-05-24T13:04:26+09:00
source_type: alpaca-mcp-3h-bars
paper: true
orders_submitted: 0
---

# 최근 6개월 3시간 시뮬레이션 원천

## 조회 목적

2025-11-24부터 2026-05-22까지 일별 정규장 3시간 단위 종목 정보를 추출하고 독립 시뮬레이션을 수행하기 위해 Alpaca MCP read-only 도구를 사용했다.

## 사용 MCP와 도구

- `alpaca.get_clock`: 시장 시계 확인.
- `alpaca.get_watchlists`: watchlist universe 확인. 결과가 비어 있어 current holdings와 기존 정책 후보를 사용했다.
- `alpaca.get_all_positions`: 현재 paper 보유 종목 확인.
- `alpaca.get_calendar`: 거래일, 정규장 open/close 확인.
- `alpaca.get_asset`: 후보 심볼의 active/tradable 여부 확인.
- `alpaca.get_stock_bars`: IEX `30Min` bars 조회. 정규장 외 bar는 집계에서 제외했다.

## 기준 시점과 범위

- 조회 생성 시각: 2026-05-24T13:04:26+09:00
- 데이터 시작일: 2025-11-24
- 데이터 종료일: 2026-05-22
- 거래일 수: 124
- feed: `iex`
- timeframe: `30Min`
- universe: `AMD, AVGO, ETN, IONQ, LRCX, NOK, NVDA, PLTR, QBTS, QQQ, RGTI, SMH, SPY, TSLA, TSM, UNH`

## 추출 방식

정규장 30분봉만 사용해 아래처럼 3시간 window로 묶었다.

- window 0: 정규장 open부터 3시간.
- window 1: window 0 이후 3시간.
- window 2: 남은 정규장 구간. 보통 15:30-16:00 ET이며, 조기 폐장일에는 더 짧다.

각 window는 open, high, low, close, volume, volume-weighted average price를 저장했다.

## 데이터 공백

- Alpaca MCP stock bars were requested from the IEX feed, not consolidated SIP; high/low/VWAP can differ from full-market data.
- 3-hour windows are aggregated from 30Min bars, so stop/take ordering inside a 30Min bar is conservatively treated as stop-first when both levels appear.
- The simulation does not include bid/ask spread, queue priority, limit-fill probability, fees, or slippage.
- Policy review is price/volume based; SEC filings, earnings surprise, valuation, analyst, and macro context are treated as follow-up checks rather than included features.
- Watchlists were empty at run time, so the universe combines current paper holdings, existing policy candidates, and SPY/QQQ/SMH benchmarks.

## 산출물

- 계산 데이터: `wiki/raw/sources/2026-05-24-six-month-3h-simulation-data.json`
- 분석 문서: [[2026-05-24-six-month-3h-independent-policy-review]]
- run manifest: `wiki/runs/2026-05-24-3h-six-month-policy-review.json`
