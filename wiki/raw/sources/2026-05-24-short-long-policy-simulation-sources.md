---
id: 2026-05-24-short-long-policy-simulation-sources
created_at: 2026-05-24T10:30:00+09:00
source_type: alpaca-market-data-simulation
paper: true
---

# 2026-05-24 단타/장타 정책 재시뮬레이션 원천

## 목적

사용자 요청에 따라 2026년 2월과 3월 날짜를 선정해 현재 단타/장타 정책을 paper-only로 시뮬레이션하고, 2026년 4월과 5월 날짜로 검증/회고하기 위한 원천 기록이다.

실제 주문, 취소, 포지션 변경은 없었다.

## 사용 원천

- Alpaca MCP `get_stock_bars`: 2026-02-01~2026-03-31 및 2026-04-01~2026-05-22 QQQ/SMH `1Day` IEX bars를 조회해 날짜 선정용 시장/섹터 regime을 확인했다.
- read-only Alpaca Market Data API IEX `1Min` bars: 단타 11:00 ET 진입, VWAP, sector breadth, stop/take/EOD 계산에 사용했다.
- 기존 raw source `[[2026-05-23-long-term-feb-mar-apr-may-sources]]`: 장타 `quality_top5` 계산 결과와 1Day bars 기반 결과를 재사용했다.
- 계산 스크립트: `scripts/simulate-short-long-policy-review.py`.
- 결과 JSON: `wiki/raw/sources/2026-05-24-short-long-policy-simulation-data.json`.
- 로컬 1분봉 cache: `.openclaw/short-long-policy-intraday-bars-cache.json`.

## 단타 날짜 선정

2월/3월 학습 날짜는 QQQ/SMH 일봉 기준으로 risk-on, risk-off, 반도체 동반 강세, 반등/되돌림이 섞이도록 선정했다.

- 학습: 2026-02-03, 2026-02-12, 2026-02-20, 2026-03-03, 2026-03-09, 2026-03-19, 2026-03-26, 2026-03-31.
- 검증: 2026-04-01, 2026-04-09, 2026-04-14, 2026-04-17, 2026-04-29, 2026-05-04, 2026-05-08, 2026-05-13, 2026-05-21, 2026-05-22.

## 단타 정책

- `intraday-rs-breakout-v0-top3/top2`: 10:00~10:59 ET QQQ risk-on, 종목 상대강도, 개장 초반 고점 근접/돌파, 11:00 ET 진입, +2% take, -1% stop.
- `intraday-rs-breadth-vwap-v1-top3/top2`: v0 조건에 QQQ VWAP, SMH VWAP, 종목 VWAP, 반도체 breadth 4개 이상을 추가.
- 종목당 가상 거래 금액은 $10,000으로 계산했다.

## 장타 정책

- `long-term-quality-momentum-v0`: 기존 `quality_top5` 결과를 사용했다.
- 기준일 종가까지의 20D/40D/60D 수익률, SPY/QQQ 상대강도, 60D drawdown, 20D 변동성, 거래량 변화를 기준으로 top5 분산 후보를 만든다.
- 가상 성과는 종목당 $10,000 투자 기준 20D 보유 수익률로 계산했다.

## 데이터 공백과 한계

- 단타 bars는 IEX feed 기준이라 전체 SIP 기준 VWAP, 고가/저가, 거래량과 다를 수 있다.
- 단타 결과에는 실제 bid/ask spread, limit fill 가능성, queue position, slippage가 없다.
- 5월 장타 기준일 일부는 아직 20거래일 결과가 완성되지 않았다.
- 장타 점수는 가격/거래량 기반이며 실적, 밸류에이션, SEC filing, macro, analyst revision은 아직 반영하지 않았다.
- Alpaca MCP 결과 전체를 파일로 직접 저장하는 도구가 없어, 날짜 선정 확인은 MCP로 수행하고 대량 1분봉 계산은 read-only Alpaca Market Data capture/cache로 수행했다.
