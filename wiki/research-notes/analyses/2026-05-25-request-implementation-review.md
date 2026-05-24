---
id: 2026-05-25-request-implementation-review
created_at: 2026-05-25T02:25:00+09:00
source_type: implementation-review
paper: true
orders_submitted: 0
---

# Request.md 반영 검토

## 반영 완료

- P0 intraday 자동주문 금지: `harness/recommendation-policy.yaml`, `harness/workflows/intraday-paper-dry-run.md`에 `observation_only`, `auto_orders_allowed=false`, `signal_log`, `skip_reason`, `spread_fill_observation`을 반영했다.
- P0 장기 정책 dry-run 후보 승격: `long-term-quality-momentum-v1`을 `active_dry_run_candidate`로 정의하고 dual benchmark, drawdown/volatility, theme/factor cap, overheat, source confidence, liquidity 필터를 config화했다.
- P0 주문 스키마/리스크 metadata 정합성: `harness/order-plan.schema.json` v1.2에서 exposure/liquidity/source/order metadata를 required로 바꾸고, `scripts/check-risk-policy.py`가 missing metadata를 error로 처리한다.
- P0 리스크 정책 v1.1: `harness/risk-policy.yaml`을 `medium-risk-v1.1`로 올리고 max ticker 15%, theme 35%, factor 50%, speculative 12%, cluster 45%, liquidity, daily turnover/loss, order lifecycle 한도를 추가했다.
- P1 strategy config: `harness/strategy-config.schema.json`, `harness/strategies/long-term-quality-momentum-v1.yaml`, `harness/strategies/intraday-afternoon-followthrough-v1.yaml`을 추가했다.
- P1 walk-forward/cost/concentration: `scripts/policy_simulation_lib.py`, `scripts/simulate-one-year-daily-policy.py`, `scripts/simulate-policy-improvement-candidates.py`에 비용 차감, bootstrap CI, 집중도, walk-forward 요약을 추가했다.
- P1 fill/slippage guard: `scripts/policy_simulation_lib.py`에 보수적 stop/take ordering helper를 추가하고, intraday는 quote/fill 검증 전 주문 생성 금지를 유지했다.
- P1 data manifest: `harness/run-manifest.schema.json`과 `harness/templates/run-manifest.json`에 `data_manifest` 필드를 추가했다.
- P1 machine-readable recommendation policy: `harness/recommendation-policy.schema.json`과 `harness/recommendation-policy.yaml`을 추가했다.
- P1 alpha/execution 분리와 source confidence: 추천 정책 YAML/Markdown과 order-plan schema에 알파 feature, execution/portfolio layer, `confidence_score`, `source_confidence` gate를 반영했다.
- P2 risk checker 확장: liquidity, turnover, daily loss, correlated cluster, duplicate client/decision id, stale open order, partial fill recompute hook을 추가했다.
- P2 tests/CI: alignment, walk-forward, strategy schema, required metadata, liquidity, duplicate id, cost model, stop/take ordering 테스트를 추가했고 전체 unittest가 통과했다.
- P2 policy proposal template: `wiki/policy-book/proposals/TEMPLATE-policy-change.md`를 추가했다.
- 1년 일별 독립 시뮬레이션 workflow: `harness/workflows/one-year-daily-simulation.md`와 실행 스크립트를 추가하고 실제 2025-05-23~2026-05-22 시뮬레이션을 수행했다.

## 시뮬레이션 결과 검토

- 원천: Alpaca MCP `get_stock_bars`, 62개 심볼, 251거래일, adjusted IEX 일봉.
- 일별 독립 run: 191개 기준일.
- 완료 추천: 853개.
- 비용 차감 후 SPY 초과 hit rate: 58.73%.
- 비용 차감 후 평균 SPY 초과수익: +3.75%.
- bootstrap 95% CI: +2.84% ~ +4.76%.
- 평균 20D 불리 이동: -6.46%.
- 최대 단일 심볼 추천 비중: 9.96%, 최대 단일 테마 추천 비중: 17.58%.
- 2026-03 validation window는 평균 -5.48%로 실패 구간이 남아 있어 자동 주문 승격은 보류한다.

## 결론

Request.md의 방향은 반영됐다. 다만 이번 1년 시뮬레이션은 일봉/단순 비용 모델이므로 quote-level fill, spread history, SEC/earnings/valuation feature가 완성되기 전까지 정책 상태는 `active_dry_run_candidate`로 유지한다. Intraday는 계속 `observation_only`다.

## 2차 누락 점검

- 스키마 파싱: `harness/order-plan.schema.json`, `harness/run-manifest.schema.json`, `harness/recommendation-policy.schema.json`, `harness/strategy-config.schema.json` 모두 JSON 파싱 통과.
- YAML 파싱: risk policy, symbol metadata, recommendation policy, strategy configs 모두 파싱 통과.
- manifest 검증: `wiki/evidence-store/run-manifests/2026-05-25-one-year-daily-policy-simulation.json`이 `harness/run-manifest.schema.json` 검증 통과.
- risk gate 예제: `python3 scripts/check-risk-policy.py harness/examples/order-plan.example.json` PASS.
- 테스트: `python3 -m unittest discover -s tests` 32개 통과.
- wrapper 검증: `scripts/simulate-long-term-policy.py`가 캡처된 Alpaca MCP 일봉 파일을 입력으로 정상 실행됨.
- lint 공백: `ruff` 실행 파일과 `python3 -m ruff` 모듈이 로컬에 없어 실행하지 못했다.

## 3차 항목별 대조 검토

| Request.md 항목 | 상태 | 반영 위치 | 검토 메모 |
| --- | --- | --- | --- |
| 1. Intraday 자동주문 금지/관찰 전용 | 완료 | `harness/recommendation-policy.yaml`, `harness/strategies/intraday-afternoon-followthrough-v1.yaml`, `harness/workflows/intraday-paper-dry-run.md` | `observation_only`, `auto_orders_allowed=false`, `signal_log`, `skip_reason`, `spread_fill_observation`가 반영됐다. |
| 2. 장기 정책 후보 승격, 자동화 보류 | 완료 | `harness/recommendation-policy.yaml`, `harness/strategies/long-term-quality-momentum-v1.yaml` | `active_dry_run_candidate`로 승격했지만 `auto_orders_allowed=false`를 유지한다. |
| 3. 주문 스키마와 risk metadata 불일치 수정 | 완료 | `harness/order-plan.schema.json`, `harness/symbol-metadata.yaml`, `scripts/check-risk-policy.py` | order metadata, liquidity, source confidence가 required이며 missing metadata는 error다. |
| 4. risk policy v1.1 및 cap 통일 | 완료 | `harness/risk-policy.yaml`, `harness/risk-policy.md`, `README.md` | max ticker 15%, theme 35%, factor 50%, speculative 12%, cluster/liquidity/daily limits가 반영됐다. |
| 5. 전략 파라미터 config 분리 | 부분 반영 | `harness/strategy-config.schema.json`, `harness/strategies/*.yaml`, `scripts/simulate-one-year-daily-policy.py` | 장기 1년 시뮬레이션은 config 기반이다. 다만 `scripts/simulate-policy-improvement-candidates.py`의 후보 정책 selector 자체는 아직 함수/lambda로 남아 있어 완전한 strategy DSL은 아니다. |
| 6. walk-forward 검증 | 부분 반영 | `scripts/policy_simulation_lib.py`, `scripts/simulate-one-year-daily-policy.py`, `wiki/backtest-runs/results/2026-05-25-one-year-daily-policy-simulation.md` | 3개월 train → 1개월 validation rolling window, 비용차감, bootstrap CI, 집중도는 반영됐다. 6개월 train variant와 bull/bear/sideways regime 분리는 아직 별도 구현이 필요하다. |
| 7. 체결/슬리피지 모델 | 부분 반영 | `scripts/policy_simulation_lib.py`, `harness/workflows/intraday-paper-dry-run.md`, `harness/recommendation-policy.yaml` | 보수적 stop/take helper와 자동주문 차단은 반영됐다. 하지만 `estimate-fill-slippage.py`, `simulate-limit-order-fills.py`, `validate-intraday-minute-bars.py` 같은 전용 fill model 스크립트는 아직 없다. |
| 8. data quality manifest | 완료 | `harness/run-manifest.schema.json`, `harness/templates/run-manifest.json`, `wiki/evidence-store/run-manifests/2026-05-25-one-year-daily-policy-simulation.json` | `data_manifest`와 dataset hash/raw input file이 저장된다. |
| 9. machine-readable recommendation policy | 완료 | `harness/recommendation-policy.yaml`, `harness/recommendation-policy.schema.json` | 전략 상태, 승격 기준, blocker, evidence metric을 agent가 파싱 가능하다. |
| 10. alpha score와 주문 결정 분리 | 완료 | `harness/recommendation-policy.yaml`, `harness/order-plan.schema.json`, `scripts/check-risk-policy.py` | alpha layer와 execution/portfolio layer를 분리했고, 주문에는 risk/liquidity/source 조건이 필요하다. |
| 11. source confidence 핵심 feature | 부분 반영 | `harness/recommendation-policy.yaml`, `harness/order-plan.schema.json`, `scripts/check-risk-policy.py`, `harness/symbol-metadata.yaml` | `confidence_score < 0.5`와 `source_confidence=low` 차단은 구현됐다. 다만 SEC/earnings/news_count/source_diversity를 event-level로 계산해 결합하는 기능은 아직 없다. |
| 12. expanded universe theme cap | 완료 | `harness/recommendation-policy.yaml`, `harness/symbol-metadata.yaml`, `scripts/simulate-one-year-daily-policy.py` | 62개 universe metadata와 theme cap 선별이 적용됐다. |
| 13. risk checker 유동성/turnover/correlation | 완료 | `scripts/check-risk-policy.py`, `harness/risk-policy.yaml` | spread, ADV, turnover, daily loss, cluster cap, duplicate id, open order conflict, partial fill recompute를 확인한다. |
| 14. order plan 기대수익/손실/사이징 근거 강제 | 완료 | `harness/order-plan.schema.json`, `harness/templates/order-plan.md`, `harness/examples/order-plan.example.json` | expected excess/adverse, confidence, sizing_basis, entry_style, liquidity가 required다. |
| 15. open order/partial fill/취소 정책 | 완료 | `harness/risk-policy.yaml`, `harness/order-plan.schema.json`, `scripts/check-risk-policy.py` | stale open order, duplicate symbol-side, partial fill recompute, retry policy가 반영됐다. |
| 16. 회귀 방지 테스트 | 부분 반영 | `tests/` | alignment, walk-forward, schema, liquidity, required metadata, cost, stop/take ordering 테스트는 추가됐다. 단, Request.md에 명시된 `tests/test_duplicate_order_id.py`라는 별도 파일명은 없고 duplicate id 테스트는 `test_order_plan_required_metadata.py`에 포함되어 있다. |
| 17. 정책 변경 제안서 템플릿 | 완료 | `wiki/policy-book/proposals/TEMPLATE-policy-change.md` | evidence, data gap, risk impact, promotion decision 구조가 반영됐다. |

## 남은 개선 과제

1. `scripts/simulate-policy-improvement-candidates.py`의 후보 정책 정의를 완전히 YAML strategy config에서 읽도록 바꾸면 P1-5의 “hardcoded strategy 제거”가 완전해진다.
2. Intraday fill/slippage 전용 스크립트 3종을 추가해야 P1-7이 “부분 반영”에서 “완료”로 올라간다.
3. SEC/earnings/news/valuation feature를 event-level로 산출해 `source_confidence`에 결합해야 P1-11과 `scripts/simulate-long-term-policy.py`의 fundamental 결합 요구가 완성된다.
4. 6개월 train window, regime별 성능 분리, sector benchmark 초과수익을 추가하면 P1-6 walk-forward 요구가 더 충실해진다.
