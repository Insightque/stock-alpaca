---
id: 2026-05-29-buy-sell-cap-review
reviewed_at: 2026-05-29T05:58:00+09:00
review_type: policy-implementation-review
paper: true
---

# 매수/매도 상한 분리 검토

## 요약

이번 검토는 실제 주문을 제출하지 않고 로컬 정책, 주문 계획, 실행 보고서, 검증 스크립트만 확인했다. 결론은 명확하다. 기존 `scripts/check-risk-policy.py`는 `orders` 길이를 그대로 일일 신규 주문 수로 계산해, 같은 ET 세션의 validation buy budget이 `20/20`에 도달하면 보유 수량 이내의 sell/trim 주문도 `daily new orders` 초과로 실패할 수 있었다.

이는 자동운영이 "매수만 하고 매도는 안 되는" 방향으로 기울 수 있는 구현상 결함이다. 최근 주문 장부 검색에서도 실제 order-plan의 `side=sell` 항목은 없었고, 많은 hourly run은 `risk_daily_new_orders_budget` 때문에 empty order plan으로 끝났다. 따라서 buy budget과 risk-reducing sell/trim 판단은 분리되어야 한다.

## 확인한 증거

- `harness/risk-policy.yaml`: 기존 `daily_limits.max_new_orders_per_day=20`은 있었지만 side 적용 범위가 없었다.
- `scripts/check-risk-policy.py`: 기존 로직은 `planned_new_orders = len(orders)`로 모든 side를 세고 `new_orders_submitted_today + planned_new_orders`를 cap과 비교했다.
- `wiki/trade-ledger/orders/2026-05-29-0131-hourly-autopilot.json` 이후 여러 empty plan: `risk_inputs.new_orders_submitted_today=20`, `orders=[]`.
- `wiki/current-runs/daily/2026-05-29-0131-hourly-autopilot.md` 이후 여러 보고서: first blocking gate가 `risk_daily_new_orders_budget`로 반복 기록됐다.
- `rg '"side": "sell"' wiki/trade-ledger/orders` 결과: 실제 주문 계획 장부에서 sell 주문은 확인되지 않았다.

## 매도가 막힐 수 있던 경로

| 제한 | 기존 매도 차단 가능성 | 판단 |
| --- | --- | --- |
| 일일 신규 주문 수 cap | 가능 | `len(orders)`를 세어 buy/sell 구분 없이 cap에 포함했다. 20/20 이후 sell 1건도 실패 가능했다. |
| run당 주문 수 cap | 가능 | `orders` 배열 최대 20개는 모든 side에 적용된다. 대량 일괄 청산은 여전히 분할하거나 명시적 계획이 필요하다. |
| cash reserve / invested cap | 낮음 | sell은 현금을 늘리고 invested exposure를 낮추므로 일반적으로 차단하지 않는다. |
| ticker/theme/factor/cluster/speculative cap | 낮음 | sell은 노출을 줄이므로 일반적으로 차단하지 않는다. |
| turnover cap | 가능 | `risk_inputs.policy_turnover_ratio`, `weekly_turnover_ratio`가 이미 cap을 넘으면 side와 무관하게 실패한다. risk-limit trim은 별도 회고 대상으로 남긴다. |
| quote/spread/open-order/held-qty gate | 의도된 차단 | 보유 수량 초과 매도, stale quote, wide spread, 같은 symbol/side open order는 계속 차단해야 한다. |

## 개정 내용

- `harness/risk-policy.yaml`에 `daily_limits.max_new_orders_per_day_applies_to_sides: [buy]`를 추가했다.
- `scripts/check-risk-policy.py`가 해당 side 목록에 들어가는 주문만 일일 cap에 합산하도록 바꿨다.
- sell-only order plan은 `new_orders_submitted_today=20` 상태에서도 held qty, quote, spread, open-order, risk gate를 통과하면 daily buy cap 때문에 실패하지 않도록 회귀 테스트를 추가했다.
- `harness/workflows/hourly-autopilot.md`에 buy budget 소진 후에도 trim trigger를 별도로 평가하고, 매도 생략 사유를 `trigger 없음`과 `비-budget gate 실패`로 구분하라고 명시했다.
- [[recommendation-policy]]에 같은 원칙을 living policy로 반영했다.

## 회고

최근 hourly autopilot은 validation data를 빠르게 쌓기 위해 buy 후보를 적극적으로 만들었고, cap 소진 후에는 buy 후보를 empty plan으로 남겼다. 이 자체는 과매매 방지 관점에서 합리적이다. 문제는 검증기가 side 구분 없이 같은 cap을 적용해, cap이 "신규 매수 throttle"이 아니라 "모든 주문 throttle"처럼 작동할 수 있었다는 점이다.

자동 sell/trim은 short 신호가 아니라 보유 long 포지션의 위험 축소다. 따라서 신규 매수 예산이 소진됐다는 이유만으로 thesis-break, 과열 후 반락, speculative 손실, cluster cap 경고 같은 risk trim 후보를 보지 않는 것은 정책 목적과 맞지 않는다. 앞으로 보고서는 "매도 trigger가 없어서 매도 없음"과 "매도 trigger는 있었지만 quote/spread/open-order/risk gate 실패로 skip"을 분리해야 한다.

## 남은 점검

- 추가 확인: [[2026-05-29-sell-frequency-policy-review]]에서 buy-quality gate가 sell에도 적용되어 `source_confidence=low`, 낮은 `confidence_score`, `policy_status=rejected` 상태의 exit가 막힐 수 있음을 확인했고 validator를 추가 개정했다.
- turnover cap이 risk-reducing trim까지 막는 사례가 있는지 별도 표본으로 확인해야 한다.
- 실제 sell/trim order-plan 표본이 아직 없으므로, 다음 thesis-break 또는 risk-limit 상황에서 새 테스트와 post-trade 회고가 필요하다.
- after-hours 정책은 현재 `allowed_sides=[buy]`라 sell/trim 자동주문 대상이 아니다. 정규장 risk trim과 섞지 않는다.

## 지표 설명

- `daily new order cap`: 같은 ET 거래일에 자동 검증 주문이 너무 많이 생성되지 않도록 막는 수량 제한이다.
- `buy budget`: 신규 long exposure를 늘리는 validation buy용 예산이다. 위험 축소용 sell/trim과 분리한다.
- `risk-reducing sell/trim`: 보유 long 포지션 일부 또는 전부를 줄여 현금 비중을 높이거나 특정 종목/테마 위험을 낮추는 주문이다.
- `turnover`: 하루 또는 일주일 동안 포트폴리오가 얼마나 많이 바뀌었는지 보는 회전율이다. 과도한 매매를 막지만, 위험 축소 주문까지 막는지는 추가 검증이 필요하다.
