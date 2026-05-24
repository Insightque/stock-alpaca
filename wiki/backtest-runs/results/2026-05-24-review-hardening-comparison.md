---
id: 2026-05-24-review-hardening-comparison
created_at: 2026-05-24T18:55:00+09:00
source_type: review-hardening-comparison-backtest
paper: true
orders_submitted: 0
---

# 리뷰 개선사항 반영 후 시뮬레이션 비교

## 목적

외부 리뷰에서 지적된 개선점 중 바로 반영한 항목이 이전 시뮬레이션 대비 어떤 차이를 만드는지 확인했다.

- 기준 데이터: `wiki/evidence-store/sources/2026-05-24-expanded-six-month-3h-simulation-data.json`
- 개선 후 계산 데이터: `wiki/evidence-store/sources/2026-05-24-review-hardening-expanded-policy-data.json`
- 기간: 2025-11-24~2026-05-22
- universe: 확장 62개 심볼 + SPY/QQQ/SMH
- split: `2026-02-25`까지 train, 이후 validation
- 실제 주문, 취소, 포지션 변경 없음.

이번 비교에서 본 개선점은 세 가지다.

1. 백테스트 날짜 정렬을 row index가 아니라 `asof_date` key로 수행한다.
2. 장타 후보에 overheat guard, dual benchmark confirmation, drawdown/volatility guard, staged entry 조건을 적용한다.
3. 주문화 단계에서는 theme/factor/speculative exposure cap을 통과해야 한다. 이 항목은 백테스트 손익을 직접 바꾸는 것이 아니라, 실제 order-plan 승격 시 집중 리스크를 차단하는 안전장치다.

## 장타 비교

기준선은 직전 확장 universe 리포트의 `daily-3h-theme-capped-top5`다. 개선 후 후보는 같은 확장 universe 데이터에 정책 개선 후보 4개를 재적용한 결과다.

| 구분 | 완료 추천 | SPY 초과 hit | 평균 20D | 평균 SPY 초과 | 평균 불리 이동 | 검증 SPY 초과 | 해석 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 이전 `daily-3h-theme-capped-top5` | 320 | 186/320 | +9.68% | +7.65% | -9.07% | +11.84% | 기존 확장 universe 기준선 |
| 개선 `lt-overheat-guard-theme-cap-v1` | 304 | 178/304 | +7.65% | +5.89% | -7.76% | +9.26% | 수익률은 낮아졌지만 평균 불리 이동이 +1.31%p 개선 |
| 개선 `lt-dual-benchmark-confirm-v1` | 292 | 169/292 | +9.73% | +8.03% | -7.86% | +13.15% | 평균 SPY 초과 +0.38%p, 검증 SPY 초과 +1.31%p 개선 |
| 개선 `lt-drawdown-volatility-guard-v1` | 282 | 160/282 | +9.42% | +7.91% | -7.75% | +13.25% | 평균 SPY 초과 +0.26%p, 불리 이동 +1.32%p, 검증 +1.41%p 개선 |
| 개선 `lt-anti-chase-staged-entry-v1` | 269 | 140/269 | +3.69% | +2.27% | -7.78% | +3.08% | 추격 제한용. 수익률 개선 정책은 아니고 진입 보수화 장치 |

## 장타에서 좋아진 점

- `dual benchmark`와 `drawdown/volatility guard`는 이전 기준선보다 검증 구간 SPY 초과수익이 좋아졌다. 각각 +13.15%p, +13.25%p로 이전 +11.84%p보다 높다.
- 평균 불리 이동은 이전 -9.07%에서 개선 후보들이 -7.75%~-7.86% 범위로 줄었다. 즉, 20D 보유 중 평균 최대 하락폭이 약 1.2~1.3%p 완화됐다.
- 완료 추천 수는 320개에서 282~304개로 줄었다. 잡음 후보를 일부 걷어낸 대가로 표본 수가 감소한 것이다.
- 날짜 key 정렬 재실행에서 `skipped_missing_symbol_dates=0`이었다. 이번 데이터셋에서는 실제 row misalignment가 결과를 바꾸지는 않았지만, 향후 ADR/provider gap이 생길 때 오매칭을 막는 방어 로직이 들어갔다.

## 장타에서 나빠졌거나 유지해야 할 주의점

- `overheat guard`는 리스크는 줄였지만 전체 평균 SPY 초과수익이 +7.65%에서 +5.89%로 낮아졌다. 과열 종목을 줄이면 일부 큰 수익도 같이 놓친다.
- `anti-chase staged entry`는 평균 SPY 초과가 +2.27%에 그쳐 독립 매수 정책으로 쓰기 어렵다. 다만 실전에서는 고점 추격을 막는 sizing/entry rule로 의미가 있다.
- 상위 기여가 여전히 `NOK`, `AMD`, `INTC`에 집중된다. 개선 정책만으로는 concentration bias가 완전히 사라지지 않는다. 이 때문에 주문화 단계에서 theme/factor/speculative exposure cap이 필요하다.

## 단타 비교

기준선은 직전 확장 universe 리포트에서 가장 나았던 `3h-afternoon-continuation-top2`다.

| 구분 | 거래 수 | hit rate | stop | take | 총 P/L | 평균 P/L/거래 | 검증 P/L | 해석 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 이전 `3h-afternoon-continuation-top2` | 104 | 61.54% | 14 | 26 | +$2,285.36 | +$21.97 | +$1,639.15 | 확장 universe 단타 기준선 중 최상 |
| 개선 `intraday-afternoon-followthrough-filter-v1` | 110 | 56.36% | 6 | 16 | +$1,711.34 | +$15.56 | +$1,456.67 | stop은 줄었지만 수익성과 hit rate는 낮아짐 |

## 단타에서 좋아진 점

- stop 횟수는 14건에서 6건으로 줄었다. 손실 방어 조건은 일부 작동했다.
- 검증 구간도 +$1,456.67로 플러스는 유지했다.

## 단타에서 나빠진 점

- hit rate는 61.54%에서 56.36%로 낮아졌다.
- 총 P/L은 +$2,285.36에서 +$1,711.34로 낮아졌다.
- 검증 P/L도 +$1,639.15에서 +$1,456.67로 소폭 낮아졌다.
- 결론적으로 단타는 개선 정책이 기존 최고 variant를 이기지 못했다. 따라서 단타 자동 주문 금지, paper-only 관찰 유지가 맞다.

## 주문화 risk gate 개선 효과

이번 손익 백테스트에는 실제 order-plan을 만들지 않았기 때문에 exposure cap이 P/L을 직접 바꾸지는 않는다. 대신 이전 리뷰에서 지적된 "개별 종목 한도는 지켜도 AI/반도체나 speculative theme에 몰릴 수 있다"는 문제를 주문 제출 전 차단한다.

- theme exposure cap: 포트폴리오의 35%
- factor exposure cap: 포트폴리오의 50%
- speculative exposure cap: 포트폴리오의 12%
- 적용 파일: `harness/risk-policy.yaml`, `scripts/check-risk-policy.py`
- 검증: theme exposure와 speculative exposure 초과 시 실패하는 테스트 추가

## 최종 판단

장타는 개선 가치가 있다. 특히 `lt-dual-benchmark-confirm-v1`과 `lt-drawdown-volatility-guard-v1`은 이전 확장 universe 기준선보다 검증 SPY 초과수익과 평균 불리 이동이 모두 나아졌다. 다음 추천 run에서는 이 둘을 우선 필터로 쓰고, `overheat guard`는 과열 추격 방지, `staged entry`는 포지션 크기 조절용으로 쓰는 것이 맞다.

단타는 개선으로 보기 어렵다. 손실 방어는 좋아졌지만 hit rate와 총 P/L이 기존 최고 variant보다 낮다. fresh quote, spread, fill 가능성, 1분봉 stop/take 순서 검증이 붙기 전까지 자동 주문 후보로 올리지 않는다.

## 지표 설명

- `완료 추천`: 추천일 이후 20거래일 성과를 계산할 수 있는 장타 표본 수다.
- `SPY 초과 hit`: 20D 수익률이 같은 기간 SPY 수익률보다 높았던 비율이다.
- `평균 20D`: 추천일 종가에서 20거래일 뒤 종가까지의 평균 수익률이다.
- `평균 SPY 초과`: 종목 20D 수익률에서 SPY 20D 수익률을 뺀 평균이다.
- `평균 불리 이동`: 추천 후 20거래일 동안 가장 불리했던 저점 기준 손실률 평균이다. 덜 음수일수록 좋다.
- `검증 SPY 초과`: `2026-02-25` 이후 검증 구간의 평균 SPY 초과수익이다.
- `총 P/L`: 단타에서 종목당 10,000달러 가상 진입 기준 손익 합계다.
