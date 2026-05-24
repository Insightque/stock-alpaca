---
id: 2026-05-23-intraday-policy-candidates-simulation
created_at: 2026-05-23T19:20:00+09:00
source_type: intraday-policy-candidate-backtest
paper: true
---

# 미검토 단타 정책 후보 시뮬레이션

## 목적

기존 단타 후보는 주로 개장 초반 risk-on, 상대강도, VWAP, 반도체 breadth를 결합한 모멘텀 추격형이었다. 이번에는 아직 충분히 고려하지 않은 정책 계열을 조사하고, 과거 특정일 학습 표본과 다른 날짜 검증 표본에 적용했다.

실제 주문은 제출하지 않았다.

## 조사 후 선택한 후보

| 후보 | 핵심 아이디어 | 기존 v0/v1과 다른 점 |
| --- | --- | --- |
| `pullback-vwap-reclaim-morning` | 장초반 눌린 종목이 11:00 ET에 VWAP 위로 회복하면 long 진입 | 돌파 추격이 아니라 눌림 후 회복을 산다 |
| `midday-vwap-reversal` | 오전에 크게 밀린 종목이 13:00 ET에 VWAP 위로 회복하면 long 진입 | 장중 후반 반전장을 별도 모듈로 본다 |
| `volume-confirmed-momentum` | 10시대 상승이 거래량 증가와 같이 나올 때만 추격 | 가격만 보지 않고 거래량 확인을 추가한다 |

## 표본

학습 표본:

- 2026-03-03
- 2026-03-09
- 2026-03-10
- 2026-03-19
- 2026-03-25

검증 표본:

- 2026-04-01
- 2026-04-09
- 2026-04-10
- 2026-04-14
- 2026-04-17

후보군은 `NVDA`, `AMD`, `AVGO`, `TSM`, `LRCX`, `PLTR`, `TSLA`이고, 시장/섹터 확인용으로 `QQQ`, `SMH`를 사용했다.

## 학습 표본 결과

| policy | active days | 거래 수 | hit rate | stop | take | 가상 P/L | 평균/거래 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `pullback-vwap-reclaim-morning` | 4 | 6 | 66.7% | 2 | 3 | +$308.80 | +$51.47 |
| `midday-vwap-reversal` | 3 | 4 | 50.0% | 2 | 1 | -$2.93 | -$0.73 |
| `volume-confirmed-momentum` | 1 | 1 | 0.0% | 1 | 0 | -$80.00 | -$80.00 |

학습 표본에서 가장 나은 후보는 `pullback-vwap-reclaim-morning`이었다.

- 2026-03-09 TSLA/TSM은 모두 +1.5% take에 도달했다.
- 2026-03-19 PLTR은 take, NVDA는 EOD 소폭 수익이었다.
- 2026-03-10 TSM과 2026-03-25 LRCX는 회복 후 다시 밀려 stop이었다.

`midday-vwap-reversal`은 거의 손익분기였고, `volume-confirmed-momentum`은 표본이 너무 적고 첫 거래가 stop이었다.

## 검증 표본 결과

| policy | active days | 거래 수 | hit rate | stop | take | 가상 P/L | 평균/거래 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `pullback-vwap-reclaim-morning` | 5 | 10 | 60.0% | 3 | 2 | +$222.57 | +$22.26 |
| `midday-vwap-reversal` | 1 | 1 | 100.0% | 0 | 0 | +$72.28 | +$72.28 |
| `volume-confirmed-momentum` | 2 | 2 | 0.0% | 2 | 0 | -$160.00 | -$80.00 |

검증 표본에서도 `pullback-vwap-reclaim-morning`은 플러스였다.

- 2026-04-01은 TSLA/PLTR 모두 stop으로 실패했다.
- 2026-04-09는 AMD EOD 수익, TSLA take로 회복했다.
- 2026-04-10은 PLTR stop, LRCX EOD 손실이었다.
- 2026-04-14는 LRCX EOD 수익, AMD take였다.
- 2026-04-17은 LRCX/AMD 모두 EOD 수익이었다.

`midday-vwap-reversal`은 2026-04-14 LRCX 한 건만 발생해 성과는 좋지만 표본이 너무 작다. `volume-confirmed-momentum`은 2026-04-10 PLTR, 2026-04-17 TSLA 모두 stop으로 실패했다.

## 59거래일 보조 스캔

2026-03-02부터 2026-05-22까지 59개 정규 거래일을 같은 규칙으로 스캔했다. 이 스캔은 정책 선택을 위한 보조 안정성 확인이며, 위 학습/검증 표본보다 넓다.

| policy | active days | 거래 수 | hit rate | stop | take | 가상 P/L | 평균/거래 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `pullback-vwap-reclaim-morning` | 24 | 38 | 55.3% | 15 | 11 | +$822.98 | +$21.66 |
| `midday-vwap-reversal` | 16 | 23 | 52.2% | 7 | 5 | +$404.14 | +$17.57 |
| `volume-confirmed-momentum` | 6 | 6 | 0.0% | 5 | 0 | -$425.87 | -$70.98 |

보조 스캔에서도 결론은 같다.

- `pullback-vwap-reclaim-morning`은 플러스지만 v1보다 약하다.
- `midday-vwap-reversal`은 플러스지만 신호 수와 안정성이 부족하다.
- `volume-confirmed-momentum`은 폐기 후보가 맞다.

## 정책 판단

`pullback-vwap-reclaim-morning`은 새 paper-only 후보로 남길 가치가 있다. 다만 기존 `intraday-rs-breadth-vwap-v1`보다 성과가 낮다.

비교:

- v1 top3 기존 검증: 27거래, hit 59.3%, P/L +$1,547.25, 평균/거래 +$57.31.
- 새 pullback 후보 59거래일 스캔: 38거래, hit 55.3%, P/L +$822.98, 평균/거래 +$21.66.

따라서 새 정책은 v1을 대체하는 후보가 아니라, v1 신호가 없을 때 관찰할 보조 후보로 두는 것이 맞다.

## 제안 정책

정책 이름: `intraday-pullback-vwap-reclaim-v0`

조건:

1. 09:30~10:59 ET에 종목이 당일 open 대비 최소 -1.0% 이상 눌린다.
2. 11:00 ET 이론 진입가가 오전 저점 대비 최소 +0.8% 회복한다.
3. 11:00 ET 이론 진입가가 종목 VWAP 위에 있다.
4. QQQ와 SMH가 11:00 ET 기준 VWAP 위에 있다.
5. 11:00 ET 이론 진입가가 당일 open 대비 +1.0%를 넘지 않는다. 너무 많이 회복한 뒤 추격하지 않기 위한 제한이다.
6. 후보는 회복률 기준 상위 2개까지만 추적한다.
7. +1.5% take, -0.8% stop, EOD 청산을 사용한다.
8. 자동 주문은 금지한다. 실시간 paper dry-run에서 v1과 병렬 관찰만 한다.

폐기 후보:

- `volume-confirmed-momentum`은 가격 상승과 거래량 증가가 같이 나와도 검증 표본과 59거래일 스캔 모두 좋지 않았다. 현재 후보에서 제외한다.

보류 후보:

- `midday-vwap-reversal`은 가능성은 있지만 신호 수가 부족하다. 장중 후반 정책으로 승격하려면 별도 표본이 더 필요하다.

## 지표 설명

- `active days`: 정책 조건이 맞아 최소 1개 이상 신호가 나온 날짜 수다. 낮으면 정책이 보수적이거나 표본이 부족하다는 뜻이다.
- `거래 수`: 가상 진입과 청산이 발생한 총 횟수다. 이번 계산은 종목당 $10,000 진입을 가정했다.
- `hit rate`: 수익으로 끝난 거래 비율이다. 높을수록 좋지만, 손절 폭과 익절 폭이 다르면 P/L과 같이 봐야 한다.
- `stop`: -0.8% 손절에 닿은 거래 수다. 많으면 회복 신호가 거짓 반등이었을 가능성이 크다.
- `take`: 목표 수익률에 닿은 거래 수다. `pullback-vwap-reclaim-morning`과 `volume-confirmed-momentum`은 +1.5%, `midday-vwap-reversal`은 +1.2%를 사용했다.
- `가상 P/L`: 종목당 $10,000씩 진입했다고 가정한 총 가상 손익이다.
- `평균/거래`: 가상 P/L을 거래 수로 나눈 값이다. 거래 한 번의 기대 품질을 보는 데 유용하다.
- `VWAP`: 거래량 가중 평균 가격이다. 가격이 VWAP 위로 회복했다는 것은 당일 평균 매수 단가보다 위로 올라왔다는 뜻이다.
- `QQQ VWAP`: 시장 전체가 당일 평균가 위에 있는지 확인하는 필터다.
- `SMH VWAP`: 반도체/AI 섹터가 당일 평균가 위에 있는지 확인하는 필터다.
- `early_drawdown_pct`: 당일 open 이후 진입 전까지 종목이 얼마나 밀렸는지다. 음수가 클수록 눌림이 깊다.
- `recovery_from_low_pct`: 오전 또는 정오 전 저점에서 진입 시점까지 얼마나 회복했는지다. 평균회귀 신호의 핵심이다.
- `volume_ratio`: 10:30~10:59 ET 평균 1분 거래량을 09:30~09:59 ET 평균 1분 거래량과 비교한 값이다. 1보다 크면 최근 거래량이 더 많다는 뜻이다.
- `EOD 청산`: take나 stop에 닿지 않으면 장 마감 근처 가격으로 이론 청산하는 방식이다.

## 연결 원천

- [[2026-05-23-intraday-policy-candidates-sources]]
- [[recommendation-policy]]
