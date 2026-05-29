# Recommendation Policy v1.10 Analyst Improvements

## Summary

전문 애널리스트 관점 리뷰에서 확인한 P0/P1 개선사항을 `harness/recommendation-policy.yaml` v1.10에 반영한다. 이 변경은 새 alpha 전략 승격이 아니라 paper validation 운용의 리스크 통제, 매도 진단 품질, 회고 기반 정책학습 속도를 개선하는 운영 정책 변경이다.

## Changed Rules

- Review backlog throttle을 추가해 회고 대기열이 커질수록 신규 validation buy를 줄이거나 중단한다. Risk-reducing sell/trim은 이 throttle에서 제외한다.
- Sell/trim diagnostics에 metric policy를 추가해 expected excess, SPY 상대성과, replacement margin 또는 metric gap reason을 남기도록 한다.
- MCP gate에 signal-specific critical source rule을 추가해 실적, macro/rate, filing risk, analyst-only thesis를 provider 개수만으로 통과시키지 않는다.
- Portfolio construction policy를 추가해 신규 buy를 기존 보유 종목의 contribution/replacement rank와 비교한다.
- After-hours risk diagnostic queue를 추가해 장외에서 sell order를 만들지 않더라도 정규장 재평가 대기열을 남긴다.
- Policy-learning pipeline 항목을 추가해 review due index, review row dataset, review scorecard, policy signal registry를 공식 산출물 후보로 둔다.

## Evidence

- train period: 해당 없음. 운영 리스크 통제 변경이다.
- validation period: 2026-05-29 밤~2026-05-30 새벽 paper validation fills와 2026-05-30 analyst review.
- completed recommendations: 해당 없음. 2026-05-29 밤 validation fills는 아직 1D/5D/20D 완료 전이다.
- avg excess return: 해당 없음. 본 변경은 수익률 승격이 아니라 backlog/diagnostic control이다.
- median excess return: 해당 없음.
- adverse move: 2026-05-30 overnight review에서 임시 mark-to-market은 작았지만 1D 판단 전이라 정책 alpha 근거로 쓰지 않는다.
- concentration: 1주 단위라도 한 밤에 validation buy가 여러 건 누적되어 review backlog risk가 확인됐다.
- cost-adjusted result: 해당 없음.

## Failure Cases

- Sell diagnostics가 AMD/PLTR/RGTI를 포착했지만 expected/relative metric이 0 또는 정성 중심으로 남아 decision-grade trim 판단으로 승격되지 못했다.
- Portfolio-level review backlog가 커질 때 신규 validation buy를 자동으로 줄이는 machine-readable throttle이 없었다.
- Provider gate는 최소 confirmation 개수는 관리했지만 thesis 유형별 critical source 누락을 구분하는 정책이 부족했다.

## Data Gaps

- 2026-05-29 밤 신규 fills는 아직 1D/5D/20D 회고가 완료되지 않았다.
- Alpaca portfolio history cancellation으로 일부 MFE/MAE가 불완전하다.
- review row dataset과 review due index는 아직 산출물 구조만 정책에 반영됐고 builder는 후속 작업이다.

## Risk Impact

Risk impact는 보수적이다. 신규 buy는 review backlog에 따라 더 엄격해지고, sell/trim은 buy budget과 무관하게 유지된다. After-hours는 allowed side set을 바꾸지 않고 diagnostic queue만 추가하므로 장외 주문 위험을 늘리지 않는다.

## Promotion Decision

- auto_eligible_paper: `long_term_quality_momentum_v1`의 paper validation 상태는 유지한다.
- applied risk-control: review backlog throttle, sell diagnostic metric policy, critical source rules, portfolio construction policy, after-hours diagnostic queue.
- needs follow-up implementation: review row dataset builder, review due index generator, review scorecard builder, policy signal registry updater.
