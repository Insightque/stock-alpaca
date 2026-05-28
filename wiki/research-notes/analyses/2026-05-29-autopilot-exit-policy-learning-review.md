---
id: 2026-05-29-autopilot-exit-policy-learning-review
reviewed_at: 2026-05-29T06:23:00+09:00
review_type: policy-implementation-review
paper: true
orders_submitted: 0
---

# Autopilot 청산/매도 정책학습 관점 검토

## 요약 판단

다른 분기의 수정사항을 그대로 이식하지 않고, 현재 repo의 정책학습에 실제 왜곡을 만들 수 있는지만 분리했다.

적용한 수정은 두 가지다.

- 정규장 `hourly-autopilot`에서 보유 포지션의 sell/trim/exit 진단을 신규 buy 후보보다 먼저 평가하도록 명시했다. Buy entry window, validation buy slot, buy budget은 신규 매수 노출만 막고 risk-reducing sell/trim을 막지 않는다.
- 단타 dry-run의 청산 규칙을 스크립트 하드코딩이 아니라 strategy config의 `exit_rules`에서 읽도록 바꿨다. 현재 v0/v1은 기존 검증 근거와 맞추어 take/stop/fallback exit 구조를 유지한다.

보류한 수정은 두 가지다.

- Force-exit 창 확대는 현 repo의 정규장 risk-trim 정책에 아직 정의되어 있지 않다. 없는 force-exit 정책을 새로 만들면 매도 빈도와 성과 회고가 기존 정책과 비교 불가능해질 수 있어 채택하지 않았다.
- 80분 time-stop은 현 repo의 단타 검증 근거에 없다. 기존 위키 근거는 11:00 ET 진입 후 take/stop 또는 장마감 fallback 기준이다. 따라서 80분을 current rule로 박지 않고, 향후 별도 variant로 검증할 수 있게 설정 경로만 열었다.

## 확인 근거

| 점검 항목 | 확인 결과 | 정책학습 판단 |
| --- | --- | --- |
| Sell 판단이 buy window에 묶였는가 | 코드상 직접 조건문은 없지만 `opening_window`가 `paper_validation_execution` 아래에 있고 workflow/prompt가 sell 선평가를 강제하지 않았다 | 보고서가 buy 차단 gate만 남기고 sell trigger 관찰을 누락할 수 있어 명시화 필요 |
| Buy budget이 sell을 막는가 | 앞선 검토에서 daily cap과 buy-quality gate가 sell을 막을 수 있음을 확인하고 수정했다 | 이번에는 workflow/prompt에도 같은 원칙을 반영 |
| Force-exit window | 현재 YAML에 정규장/장외 force-exit policy가 없다. 장외 정책은 `allowed_sides=[buy]`다 | 근거 없이 새 매도 규칙을 만들지 않음 |
| 120분 time-stop 잔존 | `rg` 기준 120분 time-stop 설정은 없었다 | 다른 분기의 같은 오타는 여기에는 없음 |
| 80분 time-stop 필요성 | 현 단타 근거 문서는 EOD fallback 기준으로 검증했다 | 새 rule 채택이 아니라 별도 실험 후보로 남김 |
| 단타 exit rule 위치 | strategy YAML에는 exit rule이 없고 helper는 take/stop/EOD를 하드코딩했다 | 학습 재현성을 위해 machine-readable config로 이동 필요 |

## 개정 내용

- `harness/recommendation-policy.yaml`
  - `risk_trim_policy.evaluation_order=before_new_buys`
  - `risk_trim_policy.decouple_from_buy_entry_window=true`
  - `risk_trim_policy.decouple_from_buy_budget=true`
- `harness/workflows/hourly-autopilot.md`
  - every run에서 sell/trim/exit 진단을 먼저 수행하고, buy window/budget은 신규 buy에만 적용한다고 명시했다.
- `scripts/run-hourly-autopilot-codex.sh`
  - scheduled nested prompt에도 동일한 hard requirement를 추가했다.
- `harness/workflows/after-hours-autopilot.md`
  - 장외 workflow는 `after_hours_policy.allowed_sides`가 허용하지 않은 sell/trim/force-exit을 정규장에서 가져오지 않도록 명시했다.
- `harness/strategy-config.schema.json`
  - optional `exit_rules`를 추가했다.
- `harness/strategies/intraday-rs-breakout-v0.yaml`, `harness/strategies/intraday-rs-breadth-vwap-v1.yaml`
  - 기존 검증 기준과 맞는 take/stop/fallback exit rule을 명시했다.
- `scripts/evaluate-intraday-dry-run.py`
  - `--strategy-config`를 받으면 `exit_rules`를 읽어 take/stop/time-stop/fallback exit를 적용한다.
  - time-stop은 지원만 추가했고, 현재 v0/v1 기본 규칙으로는 켜지지 않는다.

## 보류 이유

정책학습에서 가장 위험한 것은 "운영 안정성 개선"처럼 보이는 새 규칙이 기존 성과 표본과 섞이는 것이다. Force-exit window와 80분 time-stop은 매도 빈도와 손익 분포를 크게 바꿀 수 있다. 따라서 이 둘은 현행 자동운영 규칙으로 채택하지 않고, 별도 backtest/dry-run variant가 기준선 대비 개선되는지 확인한 뒤 결정해야 한다.

## 다음 검증 제안

- 다음 regular-session autopilot report는 `sell_trigger_none`과 `sell_skip_gate`를 분리해 기록해야 한다.
- 80분 time-stop을 검토하려면 기존 EOD fallback 기준 v0/v1과 같은 표본에서 `time_stop_minutes` variant를 따로 돌려 hit rate, stop/take/time-stop 비중, 평균 P/L, adverse move를 비교한다.
- 장외 sell/trim은 after-hours bucket에서 별도 정책으로 검증하기 전까지 정규장 risk trim과 섞지 않는다.

## 지표 설명

- `buy entry window`: 신규 validation buy를 허용하는 시간 조건이다. 위험 축소 sell/trim 판단에는 적용하지 않는다.
- `risk-reducing sell/trim`: 보유 long 포지션의 위험을 줄이기 위한 매도다. 신규 short 신호가 아니다.
- `force-exit`: 특정 세션 종료 전 강제로 청산하는 규칙이다. 현 repo에서는 아직 채택된 current rule이 아니다.
- `time-stop`: 진입 후 정해진 시간이 지나면 take/stop에 닿지 않아도 이론 청산하는 규칙이다.
- `fallback exit`: take/stop/time-stop이 발생하지 않았을 때 사용하는 마지막 이론 청산 기준이다.
