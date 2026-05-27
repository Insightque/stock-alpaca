결론

현재 저장소는 paper-only Alpaca MCP 기반의 주식/ETF 정책 실험 하네스로 설계되어 있고, 학습 루프도 “후보군 구성 → 시장/뉴스/공시/제약 수집 → paper-only 추천/주문 dry-run → 1D/5D/20D 성과 리뷰 → 충분한 증거가 쌓일 때만 정책 업데이트” 구조로 잡혀 있습니다. 또한 live/options/crypto/short/fractional 거래 금지, Alpaca REST 직접 호출 금지, 리스크 게이트 통과 전 주문 금지 같은 안전 원칙이 명확합니다.  ￼

제 판단은 명확합니다. 지금은 단타 자동주문을 확장할 때가 아니라, 장기/스윙형 정책을 더 엄격하게 검증하고 주문 정책으로 전환하는 단계입니다. 최근 백테스트에서는 장기 후보군의 dual benchmark, drawdown/volatility guard가 의미 있는 개선을 보였지만, intraday 쪽은 IEX 30분봉, spread/fill/slippage 부재, stop/take 체결 가정 때문에 자동주문으로 승격하기에는 아직 부족합니다.  ￼

⸻

P0. 즉시 업데이트해야 할 정책 항목

1. Intraday 자동주문은 계속 금지하고, 관찰 전용으로 분리

현재 정책 문서도 intraday 자동주문을 금지하고 있으며, 최근 6개월 3시간봉/30분봉 기반 리뷰에서도 intraday는 paper-only 관찰 대상으로 유지해야 한다고 정리되어 있습니다. 특히 데이터 갭으로 IEX가 SIP가 아니고, bid/ask spread, limit-fill probability, queue priority, slippage가 반영되어 있지 않습니다.  ￼

업데이트 방향:

* intraday 전략 상태를 auto_eligible=false, dry_run_only=true로 명시합니다.
* intraday 결과는 “수익률 후보”가 아니라 체결 품질 데이터 수집용으로 사용합니다.
* 자동주문 승격 조건을 별도로 둡니다:
    * 1분봉 또는 quote-level 검증 완료
    * spread_pct 계산 가능
    * limit fill 확률 추정 가능
    * stop/take가 같은 봉 안에서 발생할 때 체결 순서 검증 가능
    * 최소 3개 독립 기간에서 비용 차감 후 양수 성과
* harness/workflows/intraday-paper-dry-run.md에는 주문 생성이 아니라 signal_log, skip_reason, spread/fill_observation 기록을 의무화합니다.

정책 문구 예시

intraday_policy:
  status: observation_only
  auto_orders_allowed: false
  required_before_promotion:
    - quote_level_validation
    - spread_pct_available
    - limit_fill_probability_model
    - minute_level_stop_take_ordering
    - cost_adjusted_walk_forward_positive

⸻

2. 장기 정책은 “후보 승격”하되, 바로 완전자동화하지 않기

최근 정책 개선 백테스트에서 long-term 후보들은 intraday보다 훨씬 유망합니다. 예를 들어 lt-dual-benchmark-confirm-v1은 completed 233건, 평균 20D 수익률 +10.86%, 평균 SPY 초과수익 +9.48%, validation SPY excess +16.44%를 기록했고, lt-drawdown-volatility-guard-v1은 validation SPY excess +17.10%를 기록했습니다. 다만 review hardening 비교에서는 일부 결과가 기간/정렬 방식에 따라 달라지고, NOK/AMD/INTC 등 특정 종목 기여도가 집중되는 경고도 있습니다.  ￼

업데이트 방향:

* long-term quality + theme cap + dual benchmark + drawdown/volatility guard를 v1 후보 정책으로 승격합니다.
* staged entry는 독립 알파가 아니라 사이징/진입 방식 조절용으로 사용합니다.
* overheat guard는 수익률 극대화보다 chase 방지/리스크 축소 용도로 적용합니다.
* 자동주문 전에는 공시, 실적, 밸류에이션, 이벤트 타임스탬프 확인을 필수화합니다.

추천 v1 구조

long_term_quality_momentum_v1:
  status: active_dry_run_candidate
  core_filters:
    - ret20_exceeds_spy20
    - ret20_exceeds_qqq20
    - drawdown_60d_above_threshold
    - volatility_20d_below_threshold
    - theme_cap_pass
    - overheat_guard_pass
  sizing:
    default_entry: staged
    high_vol_initial_size_cap_pct: 5
    normal_initial_size_cap_pct: 7
  auto_submit:
    allowed: false
    promotion_required: true

⸻

3. 주문 스키마와 리스크 정책의 metadata 불일치 수정

현재 risk-policy.yaml은 require_exposure_metadata: true를 사용하고 theme/factor/speculative exposure cap을 적용합니다. 그런데 order-plan.schema.json에서는 theme, factor, volatility_bucket, speculative_flag가 optional 필드입니다. 이 상태에서는 스키마는 통과했지만 리스크 정책의 의도와 맞지 않는 order plan이 생성될 수 있습니다.  ￼

업데이트 방향:

* require_exposure_metadata: true일 때는 order schema에서도 아래 필드를 required로 바꿉니다.
    * theme
    * factor
    * volatility_bucket
    * speculative_flag
    * liquidity_bucket
    * source_confidence
* expanded universe 종목이 늘어난 만큼 symbol_metadata를 하드코딩 목록이 아니라 별도 중앙 파일로 분리합니다.
* risk-policy.yaml의 symbol_metadata와 simulation의 THEMES 하드코딩을 하나의 harness/symbol-metadata.yaml에서 읽도록 통합합니다.

수정 대상

harness/order-plan.schema.json
harness/risk-policy.yaml
scripts/check-risk-policy.py
scripts/simulate-policy-improvement-candidates.py
scripts/simulate-long-term-policy.py

⸻

4. 리스크 정책 버전 v1.1로 올리고, cap 기준을 문서와 코드에서 통일

현재 리스크 정책은 max invested 80%, min cash 20%, max ticker 20%, max theme 35%, max factor 50%, speculative 12%, max 10 orders/run, day limit, quote age 20분, limit guardrail 0.5% 구조입니다.  ￼

업데이트해야 할 점은 정책 문서, 백테스트 문서, risk yaml의 cap 수치가 동일한 기준으로 관리되어야 한다는 것입니다. 일부 리뷰 문서에서는 theme cap을 40% 또는 “2 ticker” 관점으로 해석하는 내용이 있고, 실제 risk yaml은 35%입니다. 이런 차이는 운영 단계에서 정책 해석 오류를 만듭니다.  ￼

권장:

version: medium-risk-v1.1
portfolio_limits:
  max_invested_ratio: 0.80
  min_cash_ratio: 0.20
  max_ticker_ratio: 0.15   # 기존 0.20에서 축소 검토
exposure_limits:
  max_theme_ratio: 0.35
  max_factor_ratio: 0.50
  max_speculative_ratio: 0.12
  max_correlated_cluster_ratio: 0.45
  require_exposure_metadata: true
liquidity_limits:
  min_price: 5.00
  min_avg_daily_dollar_volume: 50000000
  max_spread_pct: 0.50
  reject_if_spread_missing: true
daily_limits:
  max_new_orders_per_day: 20
  max_policy_turnover_ratio: 0.20
  max_daily_realized_loss_ratio: 0.02
  max_stop_triggered_orders_per_day: 3

⸻

P1. 시뮬레이션/백테스트 엔진 개선

5. 전략 파라미터를 코드 하드코딩에서 config 기반으로 분리

현재 simulation 스크립트에는 universe, benchmark, theme, split date, filter threshold, stop/take rule 등이 코드에 박혀 있습니다. 예를 들어 policy improvement simulation은 BENCHMARKS, THEMES, speculative themes, intraday/long-term 후보 로직을 스크립트 내부에서 정의합니다. long-term simulation도 특정 universe와 train/validation 날짜가 코드에 하드코딩되어 있습니다.  ￼

업데이트 방향:

harness/strategies/
  long-term-quality-momentum-v1.yaml
  intraday-afternoon-followthrough-v1.yaml
harness/strategy-config.schema.json

전략 config에 반드시 포함할 항목:

strategy_id: long-term-quality-momentum-v1
universe_id: expanded-us-liquid-v1
benchmarks: [SPY, QQQ]
bar_source: alpaca_iex
bar_interval: 30m_to_3h
asof_alignment: date_key
train_validation:
  method: walk_forward
  train_months: 3
  validation_months: 1
cost_model:
  slippage_bps: 10
  spread_bps: 5
  reject_unfilled_limit_orders: true
filters:
  min_ret20_vs_spy: 0
  min_ret20_vs_qqq: 0
  max_vol20: 7.0
  min_drawdown60: -30
  max_ret20_overheat: 45
  max_ret5_overheat: 25

이렇게 해야 동일한 전략을 반복 실행해도 결과가 재현되고, 나중에 정책 변경의 원인을 추적할 수 있습니다.

⸻

6. 고정 split이 아니라 walk-forward 검증으로 전환

현재 백테스트는 특정 split date를 기준으로 train/validation을 나누는 방식이 많습니다. 최근 리뷰에서는 asof_date key 기반 정렬 개선이 적용되었지만, 여전히 하나의 split 결과가 과대평가될 수 있습니다.  ￼

권장 검증 방식:

* 3개월 train → 1개월 validation
* 6개월 train → 1개월 validation
* 월별 rolling window
* bull/bear/sideways regime별 성능 분리
* SPY/QQQ/sector benchmark 대비 초과수익 계산
* 동일 종목 반복 추천에 따른 concentration-adjusted 성과 계산

추가 지표:

avg_excess_return
median_excess_return
hit_rate_with_ci
bootstrap_95_ci
max_drawdown
avg_adverse_move
turnover
symbol_concentration
theme_concentration
cost_adjusted_return

정책 승격 기준은 단일 평균 수익률이 아니라 독립 기간에서 반복되는 초과수익 + 낮은 adverse move + 낮은 concentration이어야 합니다.

⸻

7. 체결/슬리피지 모델을 추가하지 않으면 intraday 결과를 신뢰하면 안 됨

현재 intraday 리뷰는 stop/take 결과를 계산하지만, 문서상 bid/ask spread, queue priority, limit-fill probability, slippage, fee, 30분봉 내부 체결 순서가 반영되지 않았습니다. 이 때문에 intraday 성과가 좋아 보여도 실거래성은 낮습니다.  ￼

추가할 모듈:

scripts/estimate-fill-slippage.py
scripts/simulate-limit-order-fills.py
scripts/validate-intraday-minute-bars.py

필수 로직:

* limit order가 실제로 체결됐을 확률 추정
* spread_pct가 큰 종목 제외
* 같은 30분봉 안에서 stop과 take가 모두 발생한 경우 보수적 순서 적용
* partial fill 처리
* gap risk 반영
* 주문 후 1분/5분/15분 adverse move 기록
* intraday는 체결 실패를 “손실 회피”가 아니라 “기회비용/미체결”로 별도 집계

⸻

8. 데이터 품질 manifest를 run마다 저장

현재 run manifest schema는 run_id, mode, paper, git_commit, prompt SHA, risk policy version, recommendation policy SHA, MCP 서버, 실패 목록, data_cutoff_time, source_refs, risk_check_result 등을 요구합니다. 이는 좋은 출발점입니다.  ￼

추가해야 할 manifest 필드:

data_manifest:
  source_feed: alpaca_iex
  adjusted_prices: true
  timezone: America/New_York
  trading_calendar: nyse
  symbols_requested: 62
  symbols_loaded: 61
  missing_symbol_dates: 14
  stale_quotes: 3
  corporate_actions_checked: true
  survivorship_bias_controlled: false
  dataset_hash: sha256:...
  raw_input_file: wiki/raw/sources/...

특히 expanded universe를 사용할수록 누락 데이터, delisting, symbol status, survivorship bias가 성능을 왜곡할 수 있습니다.

⸻

P1. 추천 정책 자체의 개선

9. 추천 정책을 Markdown만이 아니라 machine-readable policy로 관리

현재 wiki/policies/recommendation-policy.md에는 중요한 정책 변화가 잘 기록되어 있습니다. 예를 들어 overheat guard, theme cap, SPY/QQQ dual benchmark, drawdown/volatility guard, staged entry, intraday 자동주문 금지 등이 change log와 hypothesis 형태로 관리됩니다.  ￼

하지만 운영 정책으로 쓰려면 Markdown만으로는 부족합니다. 아래 파일을 추가하는 것을 권장합니다.

harness/recommendation-policy.schema.json
harness/recommendation-policy.yaml

예시:

policy_id: recommendation-policy-v1.1
updated_at: 2026-05-24T18:55:00+09:00
strategies:
  long_term_quality_momentum_v1:
    status: active_dry_run_candidate
    evidence_count: 282
    validation_periods: 3
    avg_spy_excess_20d: 7.91
    avg_adverse_20d: -7.75
    promotion_status: not_auto_yet
    required_next_evidence:
      - cost_adjusted_walk_forward
      - event_source_confirmation
      - concentration_adjusted_score
  intraday_afternoon_followthrough_v1:
    status: observation_only
    auto_orders_allowed: false
    blocker:
      - no_quote_level_fill_model
      - no_spread_pct
      - no_minute_level_stop_take_ordering

이렇게 하면 Codex/agent가 정책 상태를 파싱할 수 있고, “실험 후보”와 “실제 주문 후보”를 혼동하지 않습니다.

⸻

10. 알파 점수와 주문 결정을 분리

현재 정책은 좋은 후보를 찾는 scoring과 실제 order sizing/risk gate가 점점 결합되고 있습니다. 앞으로는 두 계층을 분리해야 합니다.

계층 1: Alpha Signal

* ret20, ret40, ret60
* SPY/QQQ excess
* sector/ETF relative strength
* drawdown/volatility
* overheat
* event confirmation
* earnings/filing/news quality
* valuation risk

계층 2: Execution & Portfolio Decision

* 현재 보유 비중
* theme/factor/speculative cap
* liquidity/spread
* expected adverse move
* cash reserve
* staged entry 여부
* open orders
* 기존 포지션과 correlation

즉, score가 높다 = 크게 산다가 아니라, score가 높고, 리스크/체결/소스 조건이 모두 통과하면 제한된 크기로 진입한다가 되어야 합니다.

⸻

11. source confidence를 추천 정책의 핵심 feature로 추가

현재 정책 문서는 공시/뉴스/SEC acceptance time, broad query 0개 결과, source gap 등을 중요하게 다룹니다.  ￼

추천 정책에는 아래 점수를 추가해야 합니다.

source_confidence:
  sec_filing_confirmed: true
  earnings_confirmed: true
  news_count: 4
  source_diversity: 3
  provider_gap: false
  event_timestamp_known: true
  confidence_score: 0.82

정책 규칙:

* confidence_score < 0.5이면 신규 매수 금지
* provider_gap=true이면 order 생성 금지
* 실적/공시 이벤트는 published_at이 아니라 market-relevant timestamp 기준으로 as-of 처리
* 뉴스 기반 급등 종목은 “이미 오른 뒤 진입” penalty 적용

⸻

12. expanded universe는 theme cap 없이는 위험

expanded universe 리뷰에서는 universe를 62개로 늘렸을 때 intraday top3/VWAP 계열이 악화되고, daily theme-capped 쪽은 상대적으로 안정적이었습니다. 문서에서도 universe 확장은 theme cap, overheat guard, SPY/QQQ relative strength와 함께만 허용해야 한다고 정리되어 있습니다.  ￼

업데이트 방향:

universe_policy:
  allow_expanded_universe: true
  require:
    - theme_cap
    - factor_cap
    - liquidity_filter
    - active_tradable_check
    - min_price_filter
    - max_spread_filter
    - dual_benchmark_relative_strength
  reject:
    - low_source_spike
    - low_float_extreme_volatility
    - stale_quote
    - missing_theme_metadata

⸻

P2. 주문/운영 안정성 개선

13. check-risk-policy.py에 유동성, turnover, correlation 검사를 추가

현재 risk checker는 스키마 검증, policy version, quote freshness, guardrail, asset type, side, order type, cash reserve, invested ratio, ticker/theme/factor/speculative exposure 등을 검증합니다.  ￼

추가할 검사:

liquidity_check:
  - min_avg_daily_dollar_volume
  - max_spread_pct
  - quote_bid_ask_present
turnover_check:
  - max_daily_turnover_ratio
  - max_weekly_turnover_ratio
correlation_check:
  - max_cluster_exposure
  - semiconductor_ai_cluster_cap
  - quantum_speculative_cluster_cap
order_lifecycle_check:
  - duplicate_client_order_id
  - duplicate_decision_id
  - open_order_conflict
  - stale_unfilled_order
  - partial_fill_reconciliation_required

특히 AI/semiconductor/quantum 테마는 종목이 달라도 같은 factor shock에 함께 노출될 수 있으므로 theme만으로 부족하고 correlated_cluster가 필요합니다.

⸻

14. order plan에 기대수익/기대손실/사이징 근거를 강제

현재 order schema는 주문 필수 필드와 source_refs, rationale 등을 요구하고, optional로 review_horizons, historical_asof 등을 둡니다.  ￼

추가할 필드:

{
  "expected_excess_return_20d_pct": 8.0,
  "expected_adverse_move_20d_pct": -7.5,
  "confidence_score": 0.78,
  "sizing_basis": "dual_benchmark_pass + drawdown_vol_guard + theme_cap_room",
  "entry_style": "staged",
  "max_additional_entry_count": 2,
  "liquidity": {
    "spread_pct": 0.12,
    "avg_daily_dollar_volume": 250000000,
    "quote_source": "alpaca"
  }
}

이렇게 해야 주문 계획이 단순 rationale이 아니라 검증 가능한 투자 가설 + 리스크 허용치가 됩니다.

⸻

15. open order/partial fill/취소 정책 추가

현재 리스크 정책은 같은 run에서 매도대금에 의존한 매수를 막는 등 기본 안전장치가 있습니다.  ￼

실제 paper 운영 안정성을 위해 추가할 내용:

order_lifecycle:
  max_open_order_age_minutes: 30
  cancel_stale_unfilled_orders: true
  reject_duplicate_symbol_side_same_day: true
  require_post_trade_reconciliation: true
  partial_fill_policy:
    allow: true
    require_recompute_risk_after_fill: true
  retry_policy:
    max_submit_retries: 1
    retry_only_if_idempotent_client_order_id: true

⸻

P2. 테스트/CI 업데이트

16. 정책 회귀 방지용 golden backtest 추가

현재 scripts와 workflows는 많지만, 정책 업데이트가 성과 계산 방식을 깨뜨리는지 자동으로 확인하는 fixture 기반 테스트가 필요합니다. scripts 디렉터리에는 risk check, leakage check, 여러 simulation/review 스크립트가 존재합니다.  ￼

추가 테스트:

tests/test_backtest_alignment.py
tests/test_walk_forward_split.py
tests/test_strategy_config_schema.py
tests/test_risk_policy_liquidity.py
tests/test_order_plan_required_metadata.py
tests/test_duplicate_order_id.py
tests/test_cost_model.py
tests/test_intraday_stop_take_ordering.py

특히 asof_date 정렬은 이미 개선 포인트로 언급되었으므로, 다시 row-index alignment로 회귀하지 않도록 golden fixture를 만들어야 합니다.  ￼

⸻

17. 정책 변경 제안서 템플릿 추가

정책은 “좋아 보이는 백테스트”만으로 바꾸면 안 됩니다. 모든 정책 변경은 아래 템플릿을 통과해야 합니다.

wiki/policies/proposals/YYYY-MM-DD-policy-change.md

템플릿:

# Policy Change Proposal
## Summary
## Changed Rules
## Evidence
- train period:
- validation period:
- completed recommendations:
- avg excess return:
- median excess return:
- adverse move:
- concentration:
- cost-adjusted result:
## Failure Cases
## Data Gaps
## Risk Impact
## Promotion Decision
- rejected
- observation_only
- active_dry_run_candidate
- auto_eligible_paper

이 구조가 있어야 “결과가 좋았다 → 바로 정책 반영”이 아니라 “증거 → 한계 → 리스크 → 제한적 승격” 흐름이 됩니다.

⸻

파일별 구체 업데이트 제안

wiki/policies/recommendation-policy.md

추가할 내용:

* intraday는 observation_only
* long-term은 active_dry_run_candidate
* dual benchmark, drawdown/vol guard는 v1 핵심 필터
* staged entry는 독립 알파가 아니라 execution modifier
* expanded universe는 theme cap + liquidity + source confidence 없이는 금지
* 정책 승격 기준 명문화

⸻

harness/recommendation-policy.yaml 신규 생성

Markdown 정책을 agent가 읽을 수 있는 machine-readable 정책으로 변환합니다.

핵심 필드:

policy_version:
strategy_status:
promotion_criteria:
active_filters:
retired_filters:
evidence_metrics:
blockers:

⸻

harness/risk-policy.yaml

업데이트:

* version: medium-risk-v1.1
* liquidity_limits 추가
* daily_limits 추가
* correlated_cluster_limits 추가
* symbol_metadata를 별도 파일로 분리
* max_ticker_ratio를 20%에서 15%로 낮추는 방안 검토
* max_theme_ratio 35% 기준을 문서와 통일

⸻

harness/order-plan.schema.json

업데이트:

* exposure metadata required
* liquidity object required
* expected return/adverse/confidence required
* entry_style required
* decision_id/client_order_id idempotency 강화
* strategy_id, strategy_version required
* policy_status required

⸻

scripts/check-risk-policy.py

업데이트:

* spread/liquidity 검사
* turnover 검사
* daily loss 검사
* correlation cluster 검사
* duplicate order 검사
* partial fill 이후 recompute hook
* missing metadata는 warning이 아니라 error

⸻

scripts/simulate-policy-improvement-candidates.py

업데이트:

* hardcoded strategy 제거
* YAML strategy config 입력
* cost model 적용
* bootstrap confidence interval 출력
* concentration-adjusted score 출력
* walk-forward 지원
* intraday fill/slippage model 없으면 자동으로 observation_only

⸻

scripts/simulate-long-term-policy.py

업데이트:

* universe config 입력
* dynamic symbol metadata
* rolling validation
* benchmark 선택 가능
* event/source confidence feature 결합
* valuation/earnings/filing feature 결합
* 결과를 policy_scorecard.json으로 저장

⸻

wiki/backtests/와 wiki/simulations/

업데이트:

* backtest와 simulation의 목적을 더 엄격히 분리
* 모든 결과에 cost_adjusted 여부 표시
* 모든 결과에 data_feed, bar_interval, fill_model, slippage_model 표시
* “자동주문 승격 가능/불가능” 결론을 명시

⸻

권장 정책 승격 기준

Long-term 전략 승격 기준

auto_eligible_paper로 올리려면 아래를 모두 만족시키는 것이 좋습니다.

promotion_criteria_long_term:
  min_completed_recommendations: 250
  min_independent_validation_windows: 3
  min_avg_spy_excess_20d_after_cost: 3.0
  min_bootstrap_ci_lower_bound: 0.0
  max_avg_adverse_move_20d: -8.0
  max_single_symbol_contribution_pct: 25
  max_single_theme_exposure_pct: 35
  source_confidence_required: true
  liquidity_filter_required: true
  risk_gate_required: true

Intraday 전략 승격 기준

promotion_criteria_intraday:
  required_status_before_auto: quote_level_validated
  min_trades_after_cost: 300
  min_independent_validation_windows: 4
  require_spread_pct: true
  require_limit_fill_probability: true
  require_minute_level_stop_take_ordering: true
  max_stop_rate: 25
  min_profit_factor_after_cost: 1.25
  auto_orders_allowed: false_until_all_pass

⸻

최종 우선순위

우선순위	업데이트	이유
P0	intraday 자동주문 금지 유지	체결/스프레드/슬리피지 검증 부재
P0	long-term v1 후보 정책 정리	최근 검증에서 가장 유망
P0	order schema와 risk metadata required 통일	리스크 게이트 누락 방지
P0	strategy config 분리	재현성/정책 변경 추적
P1	walk-forward + cost-adjusted backtest	과최적화 방지
P1	liquidity/spread/fill model 추가	실거래성 검증
P1	source confidence feature 추가	뉴스/공시 기반 오판 방지
P1	symbol metadata 중앙화	expanded universe 안정화
P2	golden tests/CI 추가	정책 회귀 방지
P2	policy proposal template 추가	증거 기반 정책 업데이트

⸻

한 줄 판단

이 저장소의 다음 업데이트는 “더 많은 주문”이 아니라 “장기 후보 정책의 machine-readable 승격, 리스크/체결/소스 검증 강화, intraday 자동화 보류”가 핵심입니다. 지금 가장 안전하고 성능 가능성이 높은 방향은 long-term quality + dual benchmark + drawdown/volatility guard + theme cap + source confidence + staged entry를 paper dry-run 후보 정책으로 고정하고, intraday는 체결 데이터가 충분해질 때까지 관찰 전용으로 유지하는 것입니다.
