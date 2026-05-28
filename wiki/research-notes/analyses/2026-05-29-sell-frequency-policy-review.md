---
id: 2026-05-29-sell-frequency-policy-review
reviewed_at: 2026-05-29T06:12:00+09:00
review_type: policy-implementation-review
paper: true
---

# 매도 발생 빈도 정책 검토

## 요약 판단

현재 정책은 의도보다 매도가 너무 안 일어나기 쉬운 상태였다. 실제 주문 계획 장부를 구조적으로 확인한 결과 `wiki/trade-ledger/orders/*.json` 108개 order entry 중 buy 108개, sell 0개였고, hourly autopilot order entry도 buy 40개, sell 0개였다. 일부는 아직 1D/5D/20D 회고 전인 validation buy라 정상일 수 있지만, sell/trim order-plan이 0건인 것은 정책 및 validator가 매수 쪽으로 기울어 있음을 보여준다.

이번 검토에서 확인한 핵심 결함은 두 가지다.

- 이미 고친 문제: 일일 신규 주문 cap이 side를 구분하지 않아 validation buy budget 소진 후 sell/trim도 막힐 수 있었다. 근거와 1차 수정은 [[2026-05-29-buy-sell-cap-review]]에 기록했다.
- 추가 확인 문제: `scripts/check-risk-policy.py`가 `confidence_score`, `source_confidence`, `policy_status=auto_eligible_paper` 같은 신규 buy 품질 게이트를 sell에도 적용했다. 이러면 thesis가 낮은 신뢰도나 rejected 상태라서 팔아야 하는 경우에도 sell order-plan이 실패할 수 있었다.

## 근거

로컬 장부와 정책만 확인했다. 실제 주문 제출, Alpaca 계좌 변경, 라이브 endpoint 호출은 없었다.

| 확인 항목 | 결과 | 해석 |
| --- | ---: | --- |
| 전체 order-plan JSON 파일 | 108 | 현재 장부 표본 |
| order entry가 있는 파일 | 41 | 나머지는 empty plan |
| 전체 order entry | 108 | 전부 buy |
| 전체 sell entry | 0 | sell/trim 계획 자체가 생성되지 않음 |
| hourly autopilot order entry | 40 | 자동운영 표본 |
| hourly autopilot sell entry | 0 | 자동 sell/trim 실험 데이터가 없음 |

## 정책상 매도가 적은 이유

### 1. Sell trigger가 너무 늦다

현재 active trim trigger는 명확한 risk trim에 집중한다. 예: overweight, theme/factor/cluster warning, 과열 후 5D 반락, stale thesis, speculative loss. 이 방향은 안전하지만, validation buy를 많이 쌓는 운용에서는 "나쁜 포지션을 빨리 줄이는" 관찰 기회가 적어진다.

### 2. Buy 후보 품질 조건이 sell에도 적용됐다

기존 validator는 side와 무관하게 다음 조건을 적용했다.

- `policy_status`가 `observation_only`, `comparison_only`, `rejected`면 order-plan entry 차단.
- submit mode는 `policy_status=auto_eligible_paper`만 허용.
- `confidence_score < 0.50` 차단.
- `source_confidence=low` 차단.

신규 buy에는 맞는 조건이다. 하지만 sell/trim에서는 반대로 낮은 confidence, low source quality, rejected thesis가 청산 사유가 될 수 있다. 따라서 이 조건이 sell에 걸리면 "좋지 않아서 팔아야 할 포지션"일수록 매도 계획이 막히는 역전이 생긴다.

### 3. 보고서가 sell trigger 부재와 gate 실패를 충분히 분리하지 않았다

최근 no-submit run들은 `risk_daily_new_orders_budget`을 첫 차단 gate로 많이 기록했다. 이 표현은 buy 후보 차단에는 맞지만, sell 후보가 없었는지, 있었는데 다른 gate로 막혔는지까지 분리해주지 않는다. 앞으로는 "매도 trigger 없음"과 "매도 trigger는 있으나 비-budget gate 실패"를 분리해야 한다.

## 이번 개정

- `scripts/check-risk-policy.py`에서 buy-only 품질 게이트를 `side == "buy"`에만 적용하도록 변경했다.
- sell order는 `entry_style=trim` 또는 `entry_style=exit`를 요구하도록 했다.
- `policy_status=rejected`, `source_confidence=low`, 낮은 `confidence_score`인 sell exit가 held qty와 quote/spread/risk gate를 통과하면 validator에서 막히지 않도록 테스트를 추가했다.
- `harness/risk-policy.md`와 `harness/workflows/hourly-autopilot.md`에 buy-quality gate와 sell/trim gate를 분리한다고 명시했다.

## 아직 보류한 부분

- Turnover, daily realized loss, stop-trigger count는 아직 side와 무관하게 전체 plan을 막을 수 있다. 위험 축소 sell까지 막아야 하는지, buy만 막아야 하는지는 실제 손실일 표본으로 별도 검증해야 한다.
- 자동 sell trigger 자체를 더 민감하게 만드는 것은 아직 보류한다. 현재는 validator가 sell을 부당하게 막던 문제를 먼저 제거했다.
- 실제 sell/trim order-plan이 생기면 1D/5D/20D 회고에서 trigger 품질을 별도로 평가해야 한다.

## 제안

다음 정규장 hourly autopilot부터는 보고서에 sell diagnostics를 필수로 남긴다.

- 보유 종목별 trim trigger 상태.
- sell 후보가 없으면 `sell_trigger_none`.
- sell 후보가 있었지만 skip이면 `sell_skip_gate`.
- sell order-plan이 생성되면 `entry_style=trim|exit`, 보유 수량, trim 사유, 남기는 수량, 재진입 조건.

## 지표 설명

- `sell entry`: 주문 계획 JSON에서 `side=sell`인 주문 항목이다.
- `trim`: 보유 포지션 일부를 줄이는 매도다.
- `exit`: 보유 포지션을 전부 청산하는 매도다.
- `buy-quality gate`: 신규 매수 후보가 충분히 좋은지 보는 신뢰도, 정책 상태, 근거 품질 조건이다.
- `risk-reducing sell`: 수익 극대화가 아니라 포트폴리오 위험을 낮추기 위한 매도다.
