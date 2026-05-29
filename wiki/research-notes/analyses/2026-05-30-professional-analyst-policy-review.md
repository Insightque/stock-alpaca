# 2026-05-30 전문 애널리스트 관점 정책 리뷰

## 결론

현재 정책은 공격적인 수익 극대화 전략이라기보다, controlled paper validation 전략으로는 잘 설계돼 있다. 장타 quality/momentum 계열은 충분한 백테스트 표본과 SPY/QQQ 상대강도, drawdown/volatility, theme/factor cap을 결합했고, 단타/시간봉 신호는 자동주문이 아니라 관찰 전용으로 묶어 과최적화 위험을 줄였다.

전문 애널리스트 관점의 핵심 평가는 다음과 같다.

- 투자 가설: 양호. 장타 quality/momentum 정책은 현재 가장 투자 가능한 축이다.
- 리스크 통제: 양호. paper-only, whole-share limit, universe/MCP/risk gate, cash reserve, exposure cap은 탄탄하다.
- 매도 정책: 개선 필요. sell/trim 진단은 시작됐지만 아직 정량 decision feature가 약하다.
- 포트폴리오 구성: 개선 필요. 후보 선별은 강하지만 target allocation과 active risk budget은 아직 얕다.
- 정책학습 구조: 개선 필요. 회고가 Markdown 중심이라 live paper evidence가 빠르게 집계되지 않는다.

즉, 현재 정책은 "무리하게 매수/매도를 반복하지 않는 안전한 검증 하네스"로는 적합하다. 다만 "전문 운용자가 자본을 배분하는 전략"으로 보려면 매도/리밸런싱, 포트폴리오 기여도, live review dataset이 더 필요하다.

## 점수표

| 영역 | 평가 | 판단 |
| --- | --- | --- |
| 장타 투자 가설 | A- | 20D 상대강도, drawdown, volatility, theme cap 근거가 비교적 탄탄하다. |
| 단타/시간봉 통제 | A | 자동주문 금지와 관찰 전용 분리가 적절하다. |
| 리스크 게이트 | A- | cash, ticker, theme, factor, cluster, quote/spread gate가 명확하다. |
| 매수 집행 | B+ | validation 목적에는 적합하지만 1주 buy가 분산 과다를 만들 수 있다. |
| 매도/축소 규칙 | C+ | sell diagnostics는 생겼지만 기대초과수익/상대성과 값이 아직 0 또는 정성 중심이다. |
| 포트폴리오 구성 | B- | exposure cap은 있으나 expected return, beta, active risk, contribution 기준이 약하다. |
| 정책학습 루프 | B | 보수적이고 안전하지만 집계 자동화가 부족하다. |
| 문서 일관성 | B- | YAML v1.9와 Markdown 일부 설명 사이에 stale 표현이 있다. |

## 잘 설계된 부분

1. Alpha와 execution을 분리했다.
   - 점수 높은 종목을 바로 주문하지 않고, confidence, source confidence, universe, quote, spread, risk, open orders, staged entry를 통과해야 한다.

2. 장타 정책의 근거가 단일 backtest에 머물지 않는다.
   - `long_term_quality_momentum_v1`은 282개 evidence, 3개 validation period, 평균 20D SPY 초과수익 +7.91%p를 근거로 paper validation에 올라와 있다.

3. 단타는 보수적으로 막아뒀다.
   - intraday 계열은 성과가 있어도 quote-level fill model, spread history, minute-level stop/take ordering이 없으면 자동주문 금지다. 이건 실전 관점에서 맞다.

4. Risk-reducing sell/trim을 buy budget과 분리했다.
   - 2026-05-29 v1.9 이후 daily buy cap이나 entry window가 매도 판단을 막지 않게 된 점은 큰 개선이다.

5. After-hours 정책이 별도 bucket이다.
   - 정규장 validation과 장외 validation의 budget, artifact, review bucket을 분리해 혼선을 줄였다.

## 핵심 개선항목

### 1. 매도/축소 정책을 정량화해야 한다

현재 가장 큰 약점이다. sell/trim diagnostics는 매 run 기록되지만, 최근 manifest에서 `expected_excess_return_20d_pct`와 `relative_to_spy_20d_pct`가 0으로 남는다. 이러면 매도 판단은 "trigger 없음"이라는 결론에 머물고, 포지션 간 기회비용을 제대로 반영하지 못한다.

권장 개선:

- 보유 종목의 20D expected excess return을 계산해 sell diagnostic 필수값으로 만든다.
- 보유 종목이 SPY/QQQ 대비 20D 기대초과수익 0% 미만이고, 대체 후보가 +3%p 이상 margin을 가지면 `rotation_trim_watch`로 올린다.
- 1D/5D validation review에서 SPY 대비 -2%p 이하인 신규 validation buy는 추가매수 금지와 trim watch를 자동 부여한다.
- spread/fresh quote가 실패하면 매도 자체는 막더라도 `blocked_sell_candidate`로 남겨 다음 run에서 재평가한다.

### 2. Validation buy backlog throttle이 필요하다

한 밤에 10건의 validation buy가 쌓였고, 아직 1D/5D/20D review 전이다. 개별 주문은 1주라 작지만, 회고 대기열이 커지면 정책학습 노이즈가 늘어난다.

권장 개선:

- `pending_1d_count >= 8`: 신규 validation buy slot을 1개로 축소.
- `pending_1d_count >= 12`: 신규 validation buy 중단, review 우선.
- risk-reducing sell/trim은 이 throttle에서 제외.

### 3. Markdown/YAML 정책 상태 표현을 맞춰야 한다

`harness/recommendation-policy.yaml`은 `long_term_quality_momentum_v1`을 `auto_eligible_paper`, `auto_orders_allowed: true`로 둔다. 반면 `wiki/policy-book/recommendation-policy.md`의 일부 설명은 장타 후보를 아직 자동주문 금지/active dry-run candidate처럼 표현한다.

운영 기준은 YAML이 맞지만, 사람이 읽는 정책서의 stale 표현은 사고를 부를 수 있다. Markdown은 "live/production 자동주문 금지, paper validation 자동주문 허용"으로 정리하는 편이 낫다.

### 4. 포트폴리오 구성 모델이 아직 약하다

현재 정책은 좋은 후보를 고르고 위험한 노출을 막는 데 강하다. 하지만 전문 운용 관점에서는 다음 질문도 답해야 한다.

- 각 포지션이 포트폴리오 active return에 얼마나 기여하는가?
- top holdings와 theme/factor exposure가 벤치마크 대비 과도한가?
- 새 후보가 기존 보유 종목보다 기대수익/리스크 조정 후 우월한가?
- cash 20%, invested 80% 목표에서 어느 구간은 매수보다 리밸런싱이 우선인가?

권장 개선:

- target allocation table을 별도로 둔다.
- position별 `expected_excess_return`, `expected_adverse_move`, `portfolio_contribution`, `replacement_rank`를 계산한다.
- 75% invested 이후에는 신규 buy보다 rotation/trim/rebalance 후보를 우선한다.

### 5. Provider gate를 source-critical 방식으로 보강해야 한다

현재 research MCP는 최소 3개 usable/pass면 일부 provider gap을 허용한다. 운영 안정성에는 좋지만, 모든 provider가 같은 중요도를 갖지는 않는다.

예를 들어 실적 기반 후보라면 Alpha/SEC/IR 확인이 중요하고, macro-sensitive 후보라면 FRED가 중요하다. 단순히 3개 provider pass가 아니라 signal별 critical source rule이 필요하다.

권장 개선:

- earnings signal: SEC 또는 Alpha 또는 company IR 중 1개 이상 필수.
- macro/rate-sensitive signal: FRED 또는 명시적 macro source 필수.
- filing-risk signal: SEC acceptance time 필수.
- analyst-only signal: 자동매수 가산점이 아니라 thesis confirmation으로만 사용.

### 6. After-hours는 buy-only 편향을 계속 감시해야 한다

장외 정책은 `allowed_sides: buy`이고 quote freshness/spread를 강하게 요구한다. 유동성 리스크 때문에 보수적인 설계는 맞다. 다만 정규장에서는 sell/trim을 평가하고 장외에서는 buy 후보만 평가하는 구조가 장기적으로 buy-only drift를 만들 수 있다.

권장 개선:

- 장외 sell을 바로 허용할 필요는 없다.
- 대신 장외 run에서도 보유 포지션 risk diagnostic은 남기고, 정규장 open 이후 첫 run에서 sell/trim 재평가 queue로 넘긴다.
- 장외 신규 buy는 pending review backlog와 after-hours quote quality가 모두 양호할 때만 허용한다.

### 7. Live paper review dataset이 필요하다

정책학습 지표 표에는 좋은 구조가 있지만, live paper review가 자동으로 연결되지 않는다. 현재는 사람이 Markdown을 읽고 evidence_count, hit_rate, avg excess return을 갱신해야 한다.

권장 개선:

- `review-rows.jsonl`: filled trade, not-filled order, skipped candidate, sell diagnostic을 row로 저장.
- `review-due-index.json`: 1D/5D/20D due와 blocked add symbols를 관리.
- `policy-signals.yaml`: 가설/검증중/제안/적용/폐기 상태를 기계적으로 추적.
- scorecard builder로 SPY/QQQ excess, MFE/MAE, skipped opportunity cost를 자동 산출.

## 매도가 안 나오는 현상에 대한 판단

현재까지는 "팔 것이 전혀 없어서 안 판다"와 "정책이 아직 매도 정량화를 충분히 못 했다"가 섞여 있다.

- budget이나 buy entry window가 매도를 막는 구조적 문제는 2026-05-29 v1.9에서 상당 부분 해소됐다.
- 하지만 sell trigger가 thesis break, hard cap breach, reversal, stale thesis underperformance 중심이라, 상대매력 하락이나 opportunity cost trim은 아직 약하게 작동한다.
- 최근 run에서 AMD/PLTR/RGTI가 diagnostic에 올랐지만, expected excess와 relative metrics가 0으로 남아 실제 trim 후보로 승격되지 못했다.

따라서 지금 필요한 것은 강제 매도가 아니라 sell diagnostics를 decision-grade metric으로 끌어올리는 것이다.

## 우선순위

| 우선순위 | 개선 | 이유 |
| --- | --- | --- |
| P0 | Markdown/YAML 정책 상태 표현 정리 | 운영자가 paper validation 허용 범위를 오해하지 않게 해야 한다. |
| P0 | sell diagnostic expected excess/relative metric 계산 | 매도 판단이 정성 결론에 머무는 문제를 줄인다. |
| P1 | review backlog throttle | validation buy 누적과 회고 지연을 제어한다. |
| P1 | review row dataset/scorecard | 정책학습을 사람이 읽는 문서에서 기계 집계로 전환한다. |
| P2 | portfolio target allocation/active risk model | 후보 선별에서 전문 운용형 자본배분으로 발전시킨다. |
| P2 | signal별 critical source rule | provider 3개 pass만으로 중요한 결측을 놓치지 않게 한다. |
| P3 | macro/regime overlay | 금리/변동성/sector regime에 따라 cap과 entry aggressiveness를 조정한다. |

## 권장 결론

오늘 기준으로 주문 정책을 더 공격적으로 바꾸면 안 된다. 현재 v1.9는 paper validation 정책으로는 충분히 합리적이다. 다만 다음 정책 개선은 "더 많이 사게 하기"가 아니라 "언제 더 사지 말아야 하는지, 언제 일부 줄여야 하는지, 어떤 회고가 정책 변경 후보인지"를 정량화하는 방향이어야 한다.

가장 먼저 할 작업은 sell diagnostic 정량화와 review backlog throttle이다. 이 두 가지가 들어가면 현재의 buy-only drift 우려를 실질적으로 줄일 수 있다.
