# 2026-05-30 일별 정책 업데이트 건강도 점검

## 결론

현재 정책은 일별 진행을 무시하고 있지는 않다. 2026-05-22 이후 trade review, historical simulation, source-of-truth 정리, 2026-05-29 sell/trim hardening까지 정책 개선이 단계적으로 반영됐다. 특히 2026-05-29 v1.9에서는 매도 진단을 매수 gate와 분리하고, validation lifecycle과 target band를 추가해 "매수만 누적되는" 문제를 줄이는 방향으로 발전했다.

다만 "일별 진행을 정책으로 빠르게 업데이트하는 구조"로는 아직 부족하다. 현재는 Markdown 회고와 사람이 읽는 정책 표 중심이라, 매일 쌓이는 실제 paper fill, skipped candidate, sell diagnostic이 자동으로 evidence_count, hit rate, excess return으로 합산되지 않는다.

종합 판단: 방향은 양호하고 과최적화 위험은 잘 막고 있다. 하지만 빠른 정책 학습 루프로는 B+ 수준이며, 다음 개선은 정책 기준을 더 자주 바꾸는 것이 아니라 회고 데이터를 구조화하는 것이다.

## 확인한 근거

- `wiki/policy-book/recommendation-policy.md`와 `harness/recommendation-policy.yaml`은 2026-05-29 23:09 KST v1.9로 맞춰져 있다.
- 정책 변경 이력은 2026-05-22 trade review 체계화, 2026-05-23~25 historical simulation/overfit control/source-of-truth 정리, 2026-05-29 sell/trim/lifecycle hardening으로 이어진다.
- 2026-05-30 analyst review는 2026-05-28 validation fills의 1D 결과를 평가했지만, 단일 1D cohort와 portfolio history gap 때문에 정책 반영을 보류했다. 이는 보수적이고 맞는 판단이다.
- 2026-05-30 overnight trade review도 10건의 신규 validation buy를 확인했지만, 아직 1D/5D/20D horizon 전이라 정책 변경을 보류했다. 이 역시 hindsight overfit을 피한 정상 판단이다.
- 이후 자동운영 로그는 sell/trim diagnostics를 먼저 평가하고, lifecycle review 미작성 종목의 추가매수를 막고 있다. 이는 2026-05-29 정책 변경이 runtime 행동으로 반영되고 있음을 보여준다.

## 잘 되고 있는 점

1. 정책 변경이 회고와 시뮬레이션 근거를 요구한다.
2. YAML을 machine-readable source of truth로 두고, Markdown은 설명/감사 로그로 유지한다.
3. 단일 거래나 단일 1D 결과만으로 정책을 바꾸지 않는다.
4. buy gate와 sell/trim gate를 분리해 risk-reducing action이 buy budget에 막히지 않게 했다.
5. due lifecycle review가 추가매수 차단에 실제로 쓰이고 있다.

## 부족한 점

1. live paper trade review가 구조화된 row dataset으로 쌓이지 않는다.
2. policy_signal_id별 evidence_count, hit_rate, avg_excess_return이 자동 갱신되지 않는다.
3. skipped candidate와 not-filled order의 opportunity cost가 표준 필드로 남지 않는다.
4. review backlog가 늘어날 때 신규 validation buy를 줄이는 portfolio-level throttle이 아직 정책에 구현되지 않았다.
5. sell diagnostic의 `expected_excess_return_20d_pct`, `relative_to_spy_20d_pct`가 정량 feature로 충분히 강하지 않다.
6. MFE/MAE가 비는 경우 policy update 전체를 보류하기 쉬워, fallback metric과 data_quality_score가 필요하다.

## 일별 업데이트 건강도

| 항목 | 평가 | 판단 |
| --- | --- | --- |
| 회고 기록성 | A- | run, review, log, index가 잘 남는다. |
| 정책 안전성 | A | 단일 사례 overfit을 잘 피한다. |
| 정책 반영성 | B+ | 2026-05-29 변경은 runtime에 반영됐다. |
| 일별 학습 속도 | C+ | 사람이 읽고 판단해야 하는 구간이 많다. |
| 기계 집계성 | C | review row/scorecard가 아직 없다. |

## 권장 운영 판단

오늘 기준으로 `recommendation-policy.yaml`을 추가 변경할 필요는 없다. 2026-05-29 밤 체결 10건은 2026-06-01 미국 정규장 close 이후 1D review가 완료될 때까지 정책 변경 근거로 쓰면 안 된다.

다음 개선은 아래 순서가 적절하다.

1. `wiki/trade-ledger/reviews/review-due-index.json` 생성.
2. `wiki/evidence-store/review-datasets/YYYY-MM-DD-review-rows.jsonl` 생성.
3. `scripts/build-review-scorecard.py` 추가.
4. `wiki/policy-book/policy-signals.yaml` 추가.
5. `review_backlog_throttle`은 1D review backlog가 실제로 8건 이상 누적되는지 확인한 뒤 proposal 상태로 승격.

## 다음 점검 조건

- 2026-06-01 정규장 close 이후 2026-05-29 밤 validation fills의 1D review를 작성한다.
- 해당 review에서 PFE/NKE/SO/SLB/AMZN/QQQ/V/GOOGL/NEE/WMT의 SPY/QQQ excess return을 계산한다.
- 1D review가 8건 이상 밀린 상태에서 신규 validation buy가 계속 발생하면 `review_backlog_throttle`을 policy proposal로 승격한다.
- sell/trim diagnostics에서 20D expected excess return이 계속 0 또는 정성 값이면 metric completeness 개선을 우선 작업한다.
