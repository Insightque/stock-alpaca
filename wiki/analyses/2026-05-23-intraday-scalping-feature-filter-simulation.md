---
id: 2026-05-23-intraday-scalping-feature-filter-simulation
created_at: 2026-05-23T18:50:00+09:00
source_type: intraday-scalping-feature-filter-backtest
paper: true
---

# 단타 성과 개선용 추가 정보와 필터 검증

## 목적

단타 성과를 올리기 위해 필요한 추가 정보와 분석법을 정리하고, 기존 `intraday-rs-breakout-v0`에 적용해 같은 28개 표본에서 재시뮬레이션했다.

실제 주문은 제출하지 않았다.

## 추가 정보 후보

단타는 단순 가격 돌파만으로는 gap-and-fade에 취약했다. 그래서 다음 정보를 추가로 검토했다.

| 정보 | 필요한 이유 |
| --- | --- |
| QQQ VWAP | 시장 전체가 당일 평균 매수가보다 위에 있어야 long 추격이 덜 위험하다 |
| SMH VWAP | 반도체/AI 후보는 섹터 ETF가 같이 버텨야 개별주 돌파 신뢰도가 높다 |
| 종목 VWAP | 후보가 장중 평균가 위에 있어야 눌림 매도 압력이 덜하다 |
| 반도체 breadth | SMH, NVDA, AMD, AVGO, TSM, LRCX 중 다수가 상승해야 섹터 동반 흐름으로 본다 |
| opening range breakout | 개장 초반 고점 돌파 유지 여부를 확인한다 |
| gap filter | 전일 대비 과도한 gap-up 후 fade되는 날을 줄인다 |
| 실시간 bid/ask spread | 실제 paper 주문에서 fill 가능성과 slippage를 확인한다. 과거 bar만으로는 부족하다 |
| 뉴스/이벤트 시각 | 뉴스가 장중 전에 나온 것인지, 가격이 먼저 움직인 것인지 분리한다 |

## 검증 variants

모든 variants는 11:00 ET 이후 진입, +2% take, -1% stop, 15:59 ET EOD 청산을 기본으로 했다. entry price는 11:00 ET 이후 첫 1분봉 open 기준으로 보정했다.

| variant | 설명 | active days | 거래 수 | hit rate | stop | take | 가상 P/L | 평균/거래 |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| baseline_11_top3 | 기존 v0, top3 | 14 | 34 | 55.9% | 12 | 11 | +$1,425.06 | +$41.91 |
| vwap_stock_only_top3 | 종목 VWAP 위 | 14 | 34 | 55.9% | 12 | 11 | +$1,425.06 | +$41.91 |
| vwap_q_smh_stock_top3 | QQQ+SMH+종목 VWAP 위 | 13 | 33 | 57.6% | 11 | 11 | +$1,524.37 | +$46.19 |
| opening_range_breakout_top3 | opening range high 돌파 | 14 | 34 | 52.9% | 13 | 10 | +$1,132.23 | +$33.30 |
| semi_breadth4_top3 | 반도체 breadth 4개 이상 | 10 | 28 | 57.1% | 10 | 11 | +$1,447.94 | +$51.71 |
| semi_breadth4_vwap_top3 | breadth 4개 이상 + QQQ/SMH/종목 VWAP | 9 | 27 | 59.3% | 9 | 11 | +$1,547.25 | +$57.31 |
| no_big_gap_vwap_top3 | 과도한 gap 제외 + VWAP | 13 | 28 | 57.1% | 9 | 8 | +$1,135.72 | +$40.56 |
| best_candidate_filter_top2 | breadth 4개 이상 + VWAP + top2 | 9 | 18 | 66.7% | 6 | 9 | +$1,395.55 | +$77.53 |
| best_candidate_filter_top2_take15 | 같은 필터, take +1.5% | 9 | 18 | 66.7% | 6 | 10 | +$1,006.21 | +$55.90 |

## 결과 해석

가장 좋은 총손익은 `semi_breadth4_vwap_top3`였다.

- baseline 대비 거래 수는 34건에서 27건으로 줄었다.
- hit rate는 55.9%에서 59.3%로 올랐다.
- stop은 12건에서 9건으로 줄었다.
- 평균 거래 손익은 +$41.91에서 +$57.31로 개선됐다.
- 총손익은 +$1,425.06에서 +$1,547.25로 개선됐다.

가장 좋은 거래 품질은 `best_candidate_filter_top2`였다.

- hit rate 66.7%.
- 평균 거래 손익 +$77.53.
- stop 6건, take 9건.
- 다만 거래 수가 18건으로 줄어 총손익은 +$1,395.55로 baseline보다 낮았다.

나쁜 필터:

- 종목 VWAP 단독은 baseline과 거의 같아 추가 정보 가치가 없었다.
- opening range breakout 단독은 오히려 stop을 늘리고 총손익을 낮췄다.
- 과도한 gap 제외는 일부 손실을 줄였지만 수익 거래도 줄여 총손익이 낮았다.
- take +1.5%는 take 수를 늘렸지만 총손익을 낮췄다. +2% 손익비가 더 낫다.

## 개선된 정책 후보

정책 이름: `intraday-rs-breadth-vwap-v1`

조건:

1. 기존 v0 조건을 먼저 만족한다.
   - QQQ 초기 hour bar risk-on.
   - 후보 초기 수익률 +0.90% 이상.
   - QQQ 대비 상대강도 +0.40%p 이상.
   - 11:00 ET 이후 실행 가능.
2. 11:00 ET 진입 시점에 QQQ가 당일 VWAP 위에 있어야 한다.
3. SMH가 당일 VWAP 위에 있어야 한다.
4. 후보 종목이 당일 VWAP 위에 있어야 한다.
5. 반도체 breadth가 4개 이상이어야 한다.
   - 대상: SMH, NVDA, AMD, AVGO, TSM, LRCX.
   - 11:00 ET 진입가가 당일 open보다 높은 종목 수 기준.
6. 자동 주문은 금지하고, paper-only manual candidate로 기록한다.

운영 선택:

- 수익 극대화형: top3, +2% take, -1% stop.
- 안정성 우선형: top2, +2% take, -1% stop.

## 추가로 필요한 정보

과거 bar 검증을 넘어 실제 성과를 올리려면 아래 정보가 더 필요하다.

- 11:00 ET 실제 bid/ask spread와 mid-price.
- 후보별 예상 slippage와 limit fill 가능성.
- 체결 후 1분/5분 adverse move.
- 당일 뉴스가 장전/장중 어느 시점에 나왔는지.
- QQQ/SMH 동시 하락 전환 알림.
- 같은 섹터 후보 간 상관 노출. top3가 전부 반도체면 동시 stop 위험이 커진다.

## 결론

성과 개선에 가장 유효한 추가 정보는 `시장 VWAP + 섹터 VWAP + 섹터 breadth`였다. 기존 v0는 유지하되, `intraday-rs-breadth-vwap-v1`을 새 paper-only 후보로 추가한다.

다음 단계는 다음 미국 정규장부터 5~10일 동안 11:00 ET에 v0와 v1 신호를 동시에 기록하고, 실제 bid/ask와 fill 가능성을 비교하는 것이다.

## 연결 원천

- [[2026-05-23-intraday-scalping-feature-filter-sources]]
- [[2026-05-23-intraday-scalping-minute-validation]]
- [[recommendation-policy]]
