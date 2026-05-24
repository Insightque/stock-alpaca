---
id: 2026-05-23-intraday-policy-candidates-sources
created_at: 2026-05-23T19:15:00+09:00
source_type: alpaca-market-data-rest-and-web-research
paper: true
---

# 미검토 단타 정책 후보 시뮬레이션 원천

## 목적

기존 `intraday-rs-breakout-v0`와 `intraday-rs-breadth-vwap-v1`에서 충분히 다루지 않은 단타 정책 후보를 조사하고, 과거 특정일 학습 표본과 다른 날짜 검증 표본에 적용하기 위한 원천 기록이다.

## 조사한 정책 계열

| 계열 | 검토 이유 | 이번 테스트 반영 |
| --- | --- | --- |
| Opening Range Breakout / ORB | 개장 초반 범위 돌파가 intraday momentum 규칙으로 자주 검증된다 | 기존 v0/v1에 이미 일부 포함되어 새 후보에서는 제외 |
| VWAP 기준 평균회귀 | VWAP을 장중 fair value로 보고 과잉 이탈 후 회복을 진입 조건으로 본다 | `pullback-vwap-reclaim-morning`, `midday-vwap-reversal`로 테스트 |
| Intraday momentum/reversal | 장중 초반 수익률과 후속 구간 수익률 사이에 momentum 또는 reversal 가능성이 있다 | 오전 눌림 후 회복, 오후 VWAP 회복으로 분리 |
| 거래량 확인 모멘텀 | 가격 상승이 거래량 확대로 동반되는지 확인한다 | `volume-confirmed-momentum`으로 테스트 |

## 외부 조사 출처

- Opening Range Breakout 연구: https://ideas.repec.org/p/hhs/umnees/0845.html
- Intraday momentum/reversal 연구 개요: https://www.sciencedirect.com/science/article/pii/S1544612318307414
- Momentum/reversal intraday 전략과 거래비용 논의: https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0291119
- VWAP regime/mean-reversion 아이디어 참고: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6454659

## 가격 데이터 원천

- 가격: Alpaca Market Data API, IEX feed.
- 사용 bars: `1Min`.
- 조회 방식: `https://data.alpaca.markets/v2/stocks/bars` read-only 호출.
- 후보군: `QQQ`, `SMH`, `NVDA`, `AMD`, `AVGO`, `TSM`, `LRCX`, `PLTR`, `TSLA`.
- 학습 표본: 2026-03-03, 2026-03-09, 2026-03-10, 2026-03-19, 2026-03-25.
- 검증 표본: 2026-04-01, 2026-04-09, 2026-04-10, 2026-04-14, 2026-04-17.
- 보조 스캔: 2026-03-02부터 2026-05-22까지 59개 정규 거래일.

## 재현 산출물

- 계산 스크립트: `scripts/simulate-intraday-policy-candidates.py`.
- 계산 결과 JSON: `wiki/raw/sources/2026-05-23-intraday-policy-candidates-simulation-data.json`.
- 로컬 bar cache: `.openclaw/intraday-policy-candidates-bars-cache.json`.

## 테스트한 후보 정책

### `pullback-vwap-reclaim-morning`

- 09:30~10:59 ET에 종목이 당일 open 대비 최소 -1.0% 이상 눌린다.
- 11:00 ET 이론 진입가가 오전 저점 대비 최소 +0.8% 회복한다.
- 11:00 ET 이론 진입가가 종목 VWAP 위에 있다.
- QQQ와 SMH가 11:00 ET 기준 VWAP 위에 있다.
- 진입가는 당일 open 대비 +1.0%를 넘지 않아야 한다.
- 상위 2개만 추적한다.
- +1.5% take, -0.8% stop, EOD 청산.

### `midday-vwap-reversal`

- 09:30~12:59 ET에 종목이 당일 open 대비 최소 -2.0% 이상 눌린다.
- 13:00 ET 이론 진입가가 저점 대비 최소 +1.2% 회복한다.
- 13:00 ET 이론 진입가가 종목 VWAP 위에 있다.
- QQQ가 13:00 ET 기준 VWAP 위에 있다.
- 상위 2개만 추적한다.
- +1.2% take, -0.8% stop, EOD 청산.

### `volume-confirmed-momentum`

- 10:00~10:59 ET 종목 수익률이 +0.70% 이상이다.
- QQQ 대비 상대강도가 +0.40%p 이상이다.
- 10:30~10:59 ET 평균 1분 거래량이 09:30~09:59 ET 평균의 1.25배 이상이다.
- QQQ와 SMH가 11:00 ET 기준 VWAP 위에 있다.
- 상위 2개만 추적한다.
- +1.5% take, -0.8% stop, EOD 청산.

## 데이터 공백과 한계

- IEX feed 기준이라 전체 SIP 기준 VWAP, volume, high/low와 다를 수 있다.
- 1분봉 안에서 stop과 take가 동시에 가능한 경우는 보수적으로 stop first로 처리했다.
- 실제 bid/ask spread, limit fill 실패, slippage, 부분체결은 반영하지 않았다.
- 평균회귀 후보는 long-only로만 테스트했다. short, inverse ETF, options는 하네스 정책상 제외했다.
- 이번 결과는 과거 bar 기반 paper simulation이며 실제 주문 제출은 없었다.
