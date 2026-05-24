---
id: 2026-05-24-six-month-3h-independent-policy-review
created_at: 2026-05-24T13:04:26+09:00
source_type: six-month-3h-policy-simulation
paper: true
orders_submitted: 0
---

# 최근 6개월 3시간 단위 독립 시뮬레이션과 정책 검토

## 목적

사용자 요청에 따라 2025-11-24부터 2026-05-22까지 최근 6개월 미국 정규 거래일을 대상으로, Alpaca MCP에서 30분봉을 읽어 정규장 3시간 구간으로 집계했다. 주문 제출, 취소, 교체, 포지션 변경은 하지 않았다.

watchlist는 비어 있어 현재 paper 보유 종목과 기존 정책 후보, 벤치마크를 합쳐 16개 심볼을 사용했다. 기준 universe는 `AMD, AVGO, ETN, IONQ, LRCX, NOK, NVDA, PLTR, QBTS, QQQ, RGTI, SMH, SPY, TSLA, TSM, UNH`이다.

## 데이터 범위

- 거래일: 124일
- 3시간 구간 레코드: 5920개
- 정규장 집계 일봉 레코드: 1984개
- 원천: [[2026-05-24-six-month-3h-simulation-sources]]
- 계산 데이터: `wiki/evidence-store/sources/2026-05-24-six-month-3h-simulation-data.json`
- 학습/검증 분리 기준: `2026-02-25`까지를 앞구간, 이후를 뒤구간으로 보았다. 규칙은 새로 튜닝하지 않고 고정식으로 적용했다.

## 단타형 3시간 정책 결과

| 정책 | active days | trade count | hit rate | stop | take | P/L | average per trade | 검증 hit | 검증 P/L |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 3h-momentum-top3 | 55 | 127 | 48.0% | 37 | 17 | $+981.43 | $+7.73 | 52.4% | $+1,640.29 |
| 3h-momentum-top2 | 55 | 99 | 45.5% | 31 | 14 | $+517.95 | $+5.23 | 48.0% | $+971.65 |
| 3h-vwap-reclaim-top2 | 25 | 35 | 48.6% | 17 | 12 | $+734.04 | $+20.97 | 38.9% | $+228.80 |
| 3h-afternoon-continuation-top2 | 48 | 90 | 61.1% | 22 | 22 | $+1,530.61 | $+17.01 | 66.0% | $+971.74 |

해석:

- 가장 좋은 총손익 정책은 `3h-afternoon-continuation-top2`였고, 전체 가상 P/L은 $+1,530.61, 거래당 평균은 $+17.01였다.
- 단타 정책들은 모두 IEX 30분봉 기반이라 실제 체결 가능성, spread, slippage를 반영하지 못한다.
- 검증 구간에서 손익이 약하거나 stop 비중이 높은 정책은 자동 주문 후보로 올리지 않는다.

## 일별 장타형 정책 결과

| 정책 | as-of days | 20D 완료 | 20D 절대 hit | SPY 초과 hit | 평균 20D | 평균 SPY 초과 | 평균 불리 이동 | 검증 SPY 초과 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| daily-3h-quality-top5 | 84 | 320 | 192/320 | 214/320 | +9.73% | +7.70% | -8.37% | +11.21% |
| daily-3h-theme-capped-top5 | 84 | 320 | 195/320 | 214/320 | +9.86% | +7.82% | -8.34% | +11.10% |
| daily-3h-momentum-top3 | 83 | 174 | 100/174 | 110/174 | +12.17% | +10.62% | -9.47% | +17.52% |

해석:

- 전체 기준 평균 SPY 초과수익이 가장 높은 장타형 정책은 `daily-3h-momentum-top3`였다.
- `daily-3h-theme-capped-top5`는 같은 테마를 2개까지만 허용하는 variant다. 총수익이 조금 낮아져도 포트폴리오 집중 리스크를 낮추는지 확인하기 위해 별도로 유지한다.
- `daily-3h-momentum-top3`는 성과가 강할 수 있지만 종목/테마 집중과 불리 이동을 함께 보아야 한다.

## 정책 검토

| 정책/원칙 | 이번 6개월 3시간 검증 후 판단 |
| --- | --- |
| `intraday-rs-breakout-v0` 계열 | 10시대 1시간 신호 대신 첫 3시간 구간으로 독립 재검증했다. 특정 구간에서는 플러스가 가능하지만 stop-first 보수 가정과 체결 공백 때문에 자동 주문 승격은 부적합하다. |
| `intraday-rs-breadth-vwap-v1` 계열 | 이번 3시간 집계에서는 QQQ/SMH breadth를 직접 재현하지 않고 시장 위험선호와 상대강도를 단순화했다. v1은 계속 paper-only 관찰 후보로 두고, 실시간 bid/ask와 11:05~11:15 유지 확인이 붙기 전 주문 금지 원칙을 유지한다. |
| `intraday-pullback-vwap-reclaim-v0` | 첫 3시간 하락 후 VWAP 회복형으로 독립 검증했다. 손익이 플러스라도 active day가 제한되고 개별 종목 stop 위험이 있어 보조 관찰 후보 상태를 유지한다. |
| `long-term-quality-momentum-v0` | 20D/40D 추세, SPY/QQQ 상대강도, drawdown, 변동성, 첫 3시간 양봉 빈도를 결합한 일별 variant가 장타 검토에 계속 유효했다. 다만 가격 기반 검증이므로 실적/filing/밸류에이션 확인 전 자동 주문 승격은 보류한다. |
| 테마 노출 상한 | 반도체/양자 등 성과가 한 테마에 몰릴 수 있어 theme cap variant를 정책 후보로 유지할 필요가 있다. 자동 주문 전에는 테마별 40% 상한 또는 종목 2개 제한을 order plan에 명시하는 쪽이 안전하다. |
| 실적 beat 후 과열 감점 | 3시간 가격 검증만으로 실적 품질은 알 수 없지만, 단기 급등 추격형 정책에서 손실이 반복될 수 있어 기존 과열 감점 원칙을 유지한다. |

## 다음 적용 기준

- 단타는 계속 `orders_submitted=0` paper dry-run으로만 운영한다.
- 자동 주문 후보는 장타형 `quality + theme cap + filing/earnings confirmation + staged entry` 조합을 별도 검증한 뒤에만 고려한다.
- 3시간 데이터는 정책 설계용 feature store로 유지하되, 주문 제출용 근거에는 fresh quote, asset check, risk gate, source confidence가 추가로 필요하다.

## 데이터 공백

- Alpaca MCP stock bars were requested from the IEX feed, not consolidated SIP; high/low/VWAP can differ from full-market data.
- 3-hour windows are aggregated from 30Min bars, so stop/take ordering inside a 30Min bar is conservatively treated as stop-first when both levels appear.
- The simulation does not include bid/ask spread, queue priority, limit-fill probability, fees, or slippage.
- Policy review is price/volume based; SEC filings, earnings surprise, valuation, analyst, and macro context are treated as follow-up checks rather than included features.
- Watchlists were empty at run time, so the universe combines current paper holdings, existing policy candidates, and SPY/QQQ/SMH benchmarks.

## 지표 설명

- `active days`: 해당 정책이 실제로 신호를 낸 거래일 수다. 표본 거래일 전체와 다르다.
- `trade count`: 이론상 진입한 거래 수다. 같은 날 여러 종목이 들어가면 여러 건으로 계산한다.
- `hit rate`: 수익 거래 비율이다. 단타는 `pl_pct > 0`, 장타는 forward return이 양수인지로 계산했다.
- `stop`: 이론적 stop 가격에 먼저 닿은 거래 수다. 30분봉 안에서 stop과 take가 모두 보이면 보수적으로 stop-first 처리했다.
- `take`: 이론적 take profit에 닿은 거래 수다.
- `P/L`: 종목당 10,000달러를 넣었다고 가정한 가상 손익 합계다.
- `average per trade`: 가상 손익을 trade count로 나눈 값이다.
- `QQQ VWAP`, `SMH VWAP`, `symbol VWAP`: 각각 시장, 반도체 섹터, 개별 종목의 거래량 가중 평균가다. 이번 3시간 배치에서는 개별 window VWAP만 직접 사용했고, 기존 v1의 QQQ/SMH VWAP는 정책 해석 항목으로 남겼다.
- `semiconductor breadth`: SMH, NVDA, AMD, AVGO, TSM, LRCX 중 상승 종목 수를 보는 지표다. 이번 배치에서는 별도 v1 재현 대신 theme cap과 QQQ 상대강도로 대체했다.
- `relative strength`: 같은 구간의 종목 수익률에서 QQQ 수익률을 뺀 값이다. 플러스면 시장보다 강했다는 뜻이다.
- `spread_pct`: bid/ask 차이를 mid-price로 나눈 비율이다. 이번 과거 배치는 quote를 포함하지 않아 계산하지 못했다.
- `fill_feasibility`: 실제 limit 주문이 체결될 가능성 판단이다. 이번 배치는 과거 bar 기반이라 `unknown`으로 남긴다.
