# 2026-05-30 회고 기반 정책 업데이트 가속 제안

## 결론

현재 구조는 안전하다. 거래 회고는 주문을 내지 않고, 1D/5D/20D horizon을 분리하며, 단일 사례로 정책을 바꾸지 않는 원칙도 있다. 문제는 회고 결과가 대부분 Markdown 문장과 표로 남아 있어, 반복 패턴을 빠르게 집계하고 정책 변경 후보로 승격하는 경로가 느리다는 점이다.

정책 업데이트를 빠르게 하려면 기준을 낮추는 것이 아니라, 회고를 기계가 집계 가능한 행 데이터로 바꾸고, 자동 scorecard와 정책 제안 큐를 추가해야 한다.

## 현재 구조의 병목

1. 회고가 portfolio-level Markdown 중심이다.
   - `wiki/trade-ledger/reviews/`에는 유용한 판단이 있지만, 거래 1건 또는 skipped candidate 1건이 독립 row로 쌓이지 않는다.
   - 결과적으로 `evidence_count`, `hit_rate`, `avg_excess_return`를 매번 사람이 다시 읽고 계산해야 한다.

2. 정책 신호와 거래 결과의 연결이 약하다.
   - `wiki/policy-book/recommendation-policy.md`에는 `policy_signal_id` 테이블이 있지만 실제 live paper trade review row와 자동 연결되지 않는다.
   - 예: `review_backlog_throttle`, `defensive-diversification-price-confirmation`, `software/AI follow-through` 같은 새 가설은 prose로 남고 집계 대상이 되기 어렵다.

3. skipped recommendation과 blocked candidate가 충분히 정량화되지 않는다.
   - 정책 개선에는 체결된 주문뿐 아니라 `막았는데 좋았는지`, `놓쳤는데 아쉬웠는지`가 중요하다.
   - 현재 skipped section은 있지만 counterfactual return, rank, skip_reason_code, later return이 표준 필드가 아니다.

4. due review는 동작하지만 backlog 압력은 정책 입력으로 충분히 쓰이지 않는다.
   - validation lifecycle은 due review가 있으면 해당 symbol add를 막는다.
   - 하지만 "미회고 체결이 너무 많으면 전체 신규 validation buy를 줄인다"는 portfolio-level throttle은 아직 구조화되지 않았다.

5. sell/trim 진단이 아직 정량 feature로 약하다.
   - `sell_candidate_diagnostics`는 큰 개선이지만 `expected_excess_return_20d_pct`, `relative_to_spy_20d_pct`가 0 또는 정성 설명 중심이면 빠른 정책 학습에는 한계가 있다.

6. 데이터 공백이 정책 업데이트를 막는 방식이 투박하다.
   - Alpaca portfolio history cancellation 때문에 MFE/MAE가 비는 경우가 반복된다.
   - 모든 정책 업데이트를 막기보다, fallback metric과 data_quality_score를 분리해야 한다.

## 제안 아키텍처

### 1. Review Row Dataset 추가

새 산출물:

```text
wiki/evidence-store/review-datasets/YYYY-MM-DD-review-rows.jsonl
```

각 row는 실제 체결, 미체결 주문, skipped high-ranked candidate, sell/trim diagnostic을 하나씩 담는다.

필수 필드:

- `review_row_id`
- `decision_id`
- `run_id`
- `symbol`
- `side`
- `session`
- `review_bucket`
- `row_type`: `filled_trade`, `not_filled_order`, `skipped_candidate`, `sell_diagnostic`
- `strategy_id`
- `entry_style`
- `candidate_rank`
- `skip_reason_code`
- `policy_signal_ids`
- `confidence_score`
- `source_confidence`
- `mcp_confirmations`
- `mcp_gap_categories`
- `quote_age_minutes`
- `spread_pct`
- `fill_price`
- `current_or_exit_price`
- `return_1d_pct`, `return_5d_pct`, `return_20d_pct`
- `excess_spy_1d_pct`, `excess_qqq_1d_pct`
- `mfe_pct`, `mae_pct`
- `decision_quality_label`: `good_process`, `bad_process`, `inconclusive`
- `outcome_label`: `win`, `loss`, `mixed`, `pending`
- `data_quality_score`
- `source_refs`

효과:

- 회고 문서와 별개로 집계 가능한 원장 생성.
- 정책 신호별 evidence_count와 hit rate를 자동 계산 가능.

### 2. Review Due Index 추가

새 산출물:

```text
wiki/trade-ledger/reviews/review-due-index.json
```

역할:

- 모든 validation fill의 1D/5D/20D due 상태를 한 파일에서 관리.
- `pending_1d_count`, `pending_5d_count`, `pending_20d_count`, `blocked_add_symbols`, `oldest_due_at`를 계산.
- hourly autopilot의 validation lifecycle이 Markdown index 대신 이 파일을 우선 참조.

추가 정책 후보:

- `pending_1d_count >= 8`이면 신규 validation buy slots를 1개로 축소.
- `pending_1d_count >= 12`이면 신규 validation buy를 전면 중단하고 review만 우선.
- risk-reducing sell/trim은 이 throttle에서 제외.

### 3. Policy Signal Registry 추가

새 파일:

```text
wiki/policy-book/policy-signals.yaml
```

역할:

- 각 가설을 `policy_signal_id`로 관리.
- `status`: `hypothesis`, `watch`, `proposal_ready`, `applied`, `rejected`.
- `evidence_count`, `independent_days`, `hit_rate`, `avg_excess_return`, `avg_mae`, `data_quality_min`, `source_refs`.

예시 신호:

- `review-backlog-throttle`
- `defensive-diversification-price-confirmation`
- `existing-position-add-penalty`
- `software-ai-follow-through`
- `sell-diagnostic-expected-excess-required`

효과:

- `recommendation-policy.md`는 사람이 읽는 요약으로 유지하고, 집계 가능한 상태는 YAML에서 관리.

### 4. Review Scorecard Builder 추가

새 스크립트:

```text
scripts/build-review-scorecard.py
```

입력:

- order plans
- run manifests
- position snapshots
- Alpaca FILL activities raw note
- review row dataset
- current prices 또는 historical bars

출력:

```text
wiki/evidence-store/sources/YYYY-MM-DD-review-scorecard.json
wiki/research-notes/analyses/YYYY-MM-DD-review-scorecard.md
```

계산:

- horizon별 win/loss/pending
- SPY/QQQ/sector excess
- signal별 hit rate
- signal별 avg excess return
- skipped candidate opportunity cost
- not-filled order opportunity cost
- sell diagnostic later outcome
- data gap ratio

### 5. Policy Proposal Generator 추가

새 스크립트:

```text
scripts/propose-policy-updates.py
```

역할:

- `policy-signals.yaml`과 scorecard를 읽고 proposal template을 자동 작성.
- 단, `harness/recommendation-policy.yaml`은 자동 수정하지 않는다.

출력:

```text
wiki/policy-book/proposals/YYYY-MM-DD-POLICY-SIGNAL.md
```

승격 lane:

- 운영/기록 품질 규칙: 명확한 1건이면 proposal 가능.
- risk throttle/sizing 규칙: 독립 3거래일 또는 material loss 1건이면 proposal 가능.
- buy alpha 규칙: 최소 10~15개 completed 1D/5D row, 2개 이상 독립 날짜 필요.
- sell/trim 규칙: 실제 sell 부족 시 counterfactual sell diagnostic 10개 이상 필요.
- auto-eligible 변경: 기존처럼 더 긴 표본과 strict validator 유지.

## 빠르게 적용할 우선순위

1. `review-due-index.json`과 `review_backlog_throttle`부터 추가한다.
   - 최근 한 밤에 10건의 validation fill이 쌓인 문제가 바로 여기에 해당한다.
   - 과최적화 위험이 낮고 운영 안정성 효과가 크다.

2. `review-rows.jsonl`을 만든다.
   - 처음에는 filled trade와 not-filled order만 row로 쌓아도 충분하다.
   - 이후 skipped candidate와 sell diagnostic까지 확장한다.

3. `build-review-scorecard.py`를 만든다.
   - 정책 업데이트 속도를 실제로 높이는 핵심은 scorecard다.

4. `policy-signals.yaml`을 만든다.
   - Markdown 정책 문서와 YAML 정책 source 사이에 가설 상태판을 둔다.

5. `propose-policy-updates.py`는 마지막에 붙인다.
   - 자동 정책 변경이 아니라 자동 제안까지만 한다.

## 추천 즉시 도입 정책 후보

아직 YAML을 바로 바꾸지는 않는다. 다만 다음 proposal 후보로 올릴 만하다.

### review-backlog-throttle

- 문제: 1D 회고가 쌓이기 전에 신규 validation fill이 과도하게 쌓일 수 있다.
- 제안: pending 1D review가 일정 수 이상이면 신규 buy slots를 축소한다.
- 예외: risk-reducing sell/trim은 계속 평가한다.
- 근거: 2026-05-29 밤~2026-05-30 새벽 10건 체결 cohort.
- 상태: proposal 후보.

### skipped-candidate-counterfactual

- 문제: 체결된 것만 보면 정책 누락을 늦게 발견한다.
- 제안: top skipped/not-filled 후보도 1D/5D/20D later return을 기록한다.
- 근거: HOOD, MRK, AAPL/COP/NOK 같은 missed/blocked candidate가 prose로만 남음.
- 상태: proposal 후보.

### sell-diagnostic-feature-completeness

- 문제: sell/trim diagnostic은 기록되지만 expected/relative metric이 0이면 학습력이 약하다.
- 제안: `expected_excess_return_20d_pct`와 `relative_to_spy_20d_pct`를 계산하거나, 계산 불가 시 `metric_gap_reason`을 필수화한다.
- 상태: proposal 후보.

## 최종 판단

정책을 빠르게 업데이트하려면 "회고를 더 자주 쓴다"보다 "회고를 더 구조화한다"가 맞다. 현재 회고 워크플로우는 안전하지만, 정책 업데이트로 이어지는 자동 집계층이 없다. `review-due-index`, `review-rows`, `scorecard`, `policy-signals`, `proposal generator` 순서로 붙이면 과최적화 위험을 키우지 않고도 정책 반영 속도를 높일 수 있다.
