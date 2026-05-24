---
id: 2026-05-24-policy-improvement-candidates
created_at: 2026-05-24T18:25:12+09:00
source_type: policy-improvement-backtest
paper: true
orders_submitted: 0
---

# 정책 개선 후보 5개 시뮬레이션

## 목적

현재 저장된 최근 6개월 3시간/일봉 데이터로 정책 개선 후보 5개를 고정식으로 검증했다. 이 작업은 read-only 백테스트이며 실제 주문, 취소, 포지션 변경은 없다.

- 원천 계산 데이터: `wiki/evidence-store/sources/2026-05-24-six-month-3h-simulation-data.json`
- 학습/검증 분리 기준: `2026-02-25`까지 train, 이후 validation
- 후보 5개: 장타 정책 개선 4개, 단타 관찰 정책 개선 1개

## 장타 정책 개선 후보

| 개선 후보 | 완료 추천 | SPY 초과 hit | 평균 20D | 평균 SPY 초과 | 평균 불리 이동 | 검증 SPY 초과 | 판단 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `lt-overheat-guard-theme-cap-v1` | 257 | 174/257 | +10.32% | +8.89% | -7.16% | +14.54% | 채택 후보. 기존 theme cap에 과열 제한을 추가해 성과를 크게 훼손하지 않았다. |
| `lt-dual-benchmark-confirm-v1` | 233 | 155/233 | +10.86% | +9.48% | -7.11% | +16.44% | 보조 채택. 시장/나스닥 동시 초과 조건은 후보 수를 줄이지만 검증 성과가 양호했다. |
| `lt-drawdown-volatility-guard-v1` | 220 | 143/220 | +10.54% | +9.44% | -7.12% | +17.10% | 부분 채택. 방어적 필터로 불리 이동을 줄이는 목적에는 유효하지만 성과도 낮아진다. |
| `lt-anti-chase-staged-entry-v1` | 188 | 117/188 | +7.42% | +6.65% | -7.26% | +11.38% | 채택 후보. 추격 구간을 줄이면서 평균 초과수익이 유지됐다. |

## 단타 정책 개선 후보

| 개선 후보 | 거래 수 | active days | hit rate | stop | take | P/L | 검증 P/L | 판단 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `intraday-afternoon-followthrough-filter-v1` | 78 | 46 | +58.97% | 3 | 13 | $+1386.98 | $+1053.78 | 기존 단타보다 손익 안정성은 나아졌지만 여전히 IEX 30분봉/체결 공백 때문에 자동 주문 금지. |

## 정책 업데이트

1. 장타 기본 후보는 `quality + theme cap`을 유지하되 `20D <= 45%`, `5D <= 25%` 과열 제한을 추가한다.
2. 신규 매수 우선순위에는 `ret20 > SPY20`와 `ret20 > QQQ20`를 보조 확인 조건으로 둔다.
3. 방어형 계좌 상태나 시장 변동성 확대 시 `20D volatility <= 5.5%`, `40D drawdown >= -22%` 필터를 적용한다.
4. 과열 종목은 한 번에 비중을 채우지 않고 `5D -7%~+12%`, `20D 2%~35%` 구간에서 staged entry 후보로만 둔다.
5. 단타는 `afternoon follow-through` 필터를 paper-only 관찰 후보로 추가하되, fresh quote/spread/fill 확인 전 자동 주문에 넣지 않는다.

## 데이터 공백

- Alpaca MCP stock bars were requested from the IEX feed, not consolidated SIP; high/low/VWAP can differ from full-market data.
- 3-hour windows are aggregated from 30Min bars, so stop/take ordering inside a 30Min bar is conservatively treated as stop-first when both levels appear.
- The simulation does not include bid/ask spread, queue priority, limit-fill probability, fees, or slippage.
- Policy review is price/volume based; SEC filings, earnings surprise, valuation, analyst, and macro context are treated as follow-up checks rather than included features.
- Watchlists were empty at run time, so the universe combines current paper holdings, existing policy candidates, and SPY/QQQ/SMH benchmarks.
- This improvement simulation reuses previously captured IEX 30Min/daily bars and does not fetch fresh quotes.
- Fundamental, valuation, filing, analyst, and macro features are policy requirements but not numerically simulated here.
- Daily policy simulation now aligns symbols by as-of date keys instead of shared row index position.

## 지표 설명

- `완료 추천`: 추천일 이후 20거래일 성과를 계산할 수 있는 표본 수다.
- `SPY 초과 hit`: 후보의 20D 수익률이 같은 기간 SPY 수익률보다 높았던 비율이다.
- `평균 20D`: 추천일 종가에서 20거래일 뒤 종가까지의 평균 수익률이다.
- `평균 SPY 초과`: 후보 20D 수익률에서 SPY 20D 수익률을 뺀 평균값이다.
- `평균 불리 이동`: 추천 후 20거래일 동안 가장 불리했던 저점 기준 손실률 평균이다.
- `검증 SPY 초과`: 2026-02-25 이후 검증 구간에서의 평균 SPY 초과수익이다.
- `P/L`: 종목당 10,000달러 가상 진입 기준 손익 합계다.
