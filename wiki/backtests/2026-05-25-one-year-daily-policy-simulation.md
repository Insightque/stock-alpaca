---
id: 2026-05-25-one-year-daily-independent-policy-simulation
created_at: 2026-05-25T02:24:31+09:00
source_type: one-year-daily-independent-policy-simulation
paper: true
orders_submitted: 0
---

# 과거 1년 일별 독립 정책 시뮬레이션

## 결론

- 전략: `long-term-quality-momentum-v1`
- 정책 상태: `active_dry_run_candidate`
- 일별 독립 run 수: 191
- 완료 추천: 853 / 전체 추천 953
- 비용 차감 후 SPY 초과 hit rate: 58.73%
- 비용 차감 후 평균 SPY 초과수익: +3.75%
- bootstrap 95% CI: +2.84% ~ +4.76%
- 평균 20D 불리 이동: -6.46%

이 시뮬레이션은 각 기준일을 독립 run으로 취급했다. 과거 하루의 추천은 다음 날 추천 상태를 이어받지 않으며, 보유/현금/체결 상태도 누적하지 않는다.

## Walk-Forward 검증

| train | validation | 완료 추천 | 평균 비용차감 SPY 초과 | hit rate |
| --- | --- | ---: | ---: | ---: |
| 2025-05-23~2025-07-31 | 2025-08-01~2025-08-29 | 40 | +9.74% | 70.00% |
| 2025-06-02~2025-08-29 | 2025-09-02~2025-09-30 | 105 | +8.88% | 72.38% |
| 2025-07-01~2025-09-30 | 2025-10-01~2025-10-31 | 115 | +2.89% | 63.48% |
| 2025-08-01~2025-10-31 | 2025-11-03~2025-11-28 | 95 | -0.28% | 52.63% |
| 2025-09-02~2025-11-28 | 2025-12-01~2025-12-31 | 110 | +4.32% | 54.55% |
| 2025-10-01~2025-12-31 | 2026-01-02~2026-01-30 | 100 | +7.20% | 85.00% |
| 2025-11-03~2026-01-30 | 2026-02-02~2026-02-27 | 95 | +1.62% | 55.79% |
| 2025-12-01~2026-02-27 | 2026-03-02~2026-03-31 | 108 | -5.48% | 28.70% |
| 2026-01-02~2026-03-31 | 2026-04-01~2026-04-30 | 85 | +9.57% | 52.94% |
| 2026-02-02~2026-04-30 | 2026-05-01~2026-05-22 | 0 | n/a | n/a |

## 집중도와 데이터 품질

- 최대 단일 심볼 추천 비중: 9.96%
- 최대 단일 테마 추천 비중: 17.58%
- 원천 데이터 hash: `sha256:dd4652f26a5fee046692bf29e5b28f0dd91bedf738d0ff0dac36d252196db5ce`
- 원천 파일: `wiki/raw/sources/2026-05-25-one-year-daily-bars.json`
- source feed: `alpaca_iex`, bar interval: `1Day`
- fill model: 없음. 일봉 정책 검증이며 실제 limit fill probability는 아직 별도 검증 필요.
- slippage model: strategy config의 spread/slippage bps를 단순 비용으로 차감.

## 정책 반영 검토

- intraday 전략은 이 결과와 무관하게 `observation_only`이며 자동주문 대상이 아니다.
- 장기 전략은 비용 차감 walk-forward와 집중도 지표를 추가로 기록했지만, quote-level spread/fill 및 공시/실적/밸류에이션 feature가 아직 완전하지 않아 `active_dry_run_candidate` 상태를 유지한다.
- 정책 업데이트는 `harness/recommendation-policy.yaml`의 승격 기준을 기준으로 별도 proposal을 통과해야 한다.
