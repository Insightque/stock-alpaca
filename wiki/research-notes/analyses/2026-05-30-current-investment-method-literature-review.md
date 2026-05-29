# 2026-05-30 최신 투자 방법 문헌 기반 정책 점검

## 결론

현 하네스의 방향은 최신 문헌과 대체로 맞다. 특히 LLM을 직접 매수/매도 엔진으로 쓰지 않고, 출처 확인, 가격/상대강도, 리스크 게이트, paper validation, 회고 기반 정책학습으로 분리한 점은 안전하다.

다만 최신 문헌 기준으로 보면 다음 개선이 필요하다.

- 정보 활용: 뉴스/공시/재무제표/매크로/애널리스트 정보를 narrative가 아니라 as-of timestamp가 있는 구조화 feature row로 저장해야 한다.
- 분석 방법: 단일 expected return 점수보다 forecast uncertainty, confidence interval, cost-adjusted excess return, portfolio utility를 같이 산출해야 한다.
- 정책: LLM/RAG는 정보추출과 해석 보조로 제한하고, prompt-only forecast는 주문 근거로 쓰지 않는 규칙을 명시해야 한다.
- 포트폴리오: 신규 후보 점수보다 기존 보유분의 active risk contribution, replacement rank, transaction cost, uncertainty-adjusted return을 먼저 계산해야 한다.
- 회고: policy-learning pipeline은 YAML에 들어갔지만 builder가 아직 없으므로 review row dataset, due index, scorecard 구현이 최우선이다.

## 검토 문헌과 시사점

| 문헌/자료 | 핵심 시사점 | 현 하네스 평가 | 개선 필요 |
| --- | --- | --- | --- |
| Lopez-Lira & Tang, `Can ChatGPT Forecast Stock Price Movements?` | LLM headline sentiment가 뉴스 반응과 후속 drift를 일부 예측하지만, LLM 보급이 늘수록 전략 수익은 감소한다. | 뉴스-가격 lead/lag와 source gate는 이미 있음. | 뉴스 sentiment를 단독 alpha가 아니라 event type, pre-news drift, novelty, market feedback과 결합한다. |
| Kim/Muhn/Nikolaev, `Financial Statement Analysis with LLMs` | GPT-4는 표준화 재무제표만으로도 earnings direction 판단에 유용한 narrative insight를 만들 수 있다. | valuation/filing feature는 정책상 존재하지만 자동 구조화는 약함. | SEC/XBRL 기반 재무 feature extractor를 만들고 LLM은 ratio 해석/이상치 설명에만 쓴다. |
| XBRL International / SEC machine-readable disclosure 자료 | PDF보다 Inline XBRL/xBRL-JSON 같은 구조화 데이터가 투자급 분석에 더 적합하다. | SEC EDGAR 사용 정책은 좋지만 filings를 정량 feature로 축적하지 못함. | revenue growth, margin, accruals, cash conversion, debt, dilution, buyback, guidance 관련 XBRL facts를 as-of feature로 저장한다. |
| FinBen, NeurIPS 2024 | 금융 LLM은 정보추출/텍스트분석에 강하지만 forecasting, reasoning, decision-making은 더 어렵다. | LLM이 주문을 직접 내리지 않는 구조는 타당함. | `llm_use_policy`: extraction/summarization/contradiction check는 허용, submit 근거 forecast는 금지 또는 shadow-only로 분리한다. |
| Knowledge-enhanced LLM sentiment / DK-CoT 연구 | 금융 도메인 지식과 RAG를 결합하면 sentiment 분석 안정성이 개선된다. | llm-wiki와 MCP raw source는 RAG의 재료가 있음. | ticker별 retrieved context, event taxonomy, source timestamp, confidence를 가진 `source_signal_rows`를 만든다. |
| Time-Series Foundation Models in Finance / StockLLM류 | TSFM/RAG forecasting은 유망하지만 financial benchmark, risk-aware evaluation, leakage 통제가 핵심이다. | 가격 기반 backtest와 baseline 비교 원칙은 좋음. | TSFM/Transformer는 주문 신호가 아니라 shadow forecast feature로 도입하고 price-only/simple model 대비 lift를 검증한다. |
| ML stock return prediction: Transformer vs simple NN / regression-based approaches | 복잡한 모델이 항상 이기는 것은 아니며, 단순 모델도 out-of-sample에서 경쟁력이 있다. | 현재 heuristic+backtest 중심이라 단순하고 설명 가능함. | regularized regression/GBM/simple NN를 기준선으로 두고 Transformer/LLM feature의 incremental lift만 채택한다. |
| ML prediction uncertainty in asset pricing | expected return point estimate만 쓰면 불확실성을 무시한다. CI와 shrinkage가 out-of-sample 개선에 중요하다. | `confidence_score`는 있지만 forecast interval은 약함. | 모든 후보에 `expected_excess_ci_low/high`, `forecast_uncertainty`, `shrinkage_reason`을 추가한다. |
| Robust predict-and-optimize / robust online portfolio selection | return prediction과 portfolio decision을 분리하면 극단 weight와 비용 문제가 생긴다. 거래비용과 불확실성을 함께 최적화해야 한다. | v1.10의 portfolio construction policy는 방향만 있음. | sizing은 score가 아니라 uncertainty-adjusted return, active risk, turnover cost, fill probability를 통과해야 한다. |
| LLM look-ahead bias 연구 | LLM historical forecast는 사전학습 기억 때문에 미래정보 오염 가능성이 있다. | wiki historical simulation은 leakage control이 있으나 LLM pretraining leakage까지는 명시적으로 막지 못함. | historical sim에서 LLM forecast는 `llm_memory_leakage_risk`로 태그하고, alpha 검증은 구조화 as-of 데이터와 deterministic model 중심으로 수행한다. |

## 정보 활용 측면 개선안

### 1. Source Signal Row Dataset

현재 raw source는 보존되지만, 정책학습이 재사용할 수 있는 행 단위 feature가 부족하다. 다음 JSONL 구조를 추천한다.

```json
{
  "asof_at": "2026-05-29T14:30:00-04:00",
  "symbol": "NVDA",
  "source_type": "sec|earnings|news|macro|analyst|price",
  "source_ref": "wiki/evidence-store/sources/...",
  "event_type": "earnings|filing|product|macro|analyst|policy|unknown",
  "target": "revenue|margin|guidance|capex|demand|risk",
  "direction": "positive|negative|neutral|mixed",
  "novelty": "new|repeat|stale",
  "market_reaction": "news_led|price_led|same_day|sell_the_news|unknown",
  "confidence": 0.0,
  "available_to_agent": true
}
```

정책 효과:

- LLM/RAG 출력을 검증 가능한 데이터셋으로 바꿀 수 있다.
- 뉴스가 가격보다 늦은지, 실적 surprise가 이미 반영됐는지, analyst-only 신호인지 구분 가능하다.
- skipped candidate와 filled trade 회고를 같은 feature schema로 비교할 수 있다.

### 2. SEC/XBRL Fundamental Feature Pipeline

현재 정책은 valuation/filing features를 요구하지만 실제 자동 feature 축적은 약하다. XBRL 기반으로 다음 feature를 계산해 `source_signal_rows` 또는 별도 `fundamental_features.jsonl`에 넣는 것이 좋다.

- growth: revenue, gross profit, operating income, EPS, free cash flow YoY/QoQ.
- quality: gross margin, operating margin, FCF margin, accruals, ROA/ROE.
- balance sheet: net debt, current ratio, interest burden, dilution/share count.
- capital allocation: buyback, issuance, capex, R&D intensity.
- filing risk: going concern, litigation, customer concentration, material weakness, late filing.
- timestamp: filing date가 아니라 SEC acceptance time.

LLM은 숫자 원천이 아니라 ratio 해석, 사업부 설명, risk contradiction check에만 쓰는 편이 안전하다.

### 3. LLM/RAG 사용 정책 명확화

문헌상 금융 LLM은 정보추출과 텍스트 분석에는 강하지만 복합 forecasting/decision에는 취약하다. 따라서 정책상 다음 구분이 필요하다.

| LLM 사용 | 허용 수준 |
| --- | --- |
| raw source 요약 | 허용 |
| source contradiction / stale claim 탐지 | 허용 |
| event taxonomy / sentiment / stance 추출 | 허용, 단 structured source row와 confidence 필요 |
| 재무제표 ratio narrative | 허용, 숫자는 XBRL/structured source에서 계산 |
| 종목별 expected return 직접 예측 | shadow-only |
| 주문 수량/매수/매도 직접 결정 | 금지 |
| historical sim에서 모델 기억 기반 판단 | 금지 또는 leakage-risk 태그 |

## 분석 방법 개선안

### 1. Forecast Uncertainty First

현재 `confidence_score`와 expected excess가 있지만, 불확실성 범위가 약하다. 다음 필드를 order plan 후보와 sell diagnostic에 추가하는 편이 좋다.

- `expected_excess_return_20d_pct`
- `expected_excess_ci_low_20d_pct`
- `expected_excess_ci_high_20d_pct`
- `expected_adverse_move_20d_pct`
- `forecast_uncertainty_score`
- `uncertainty_shrinkage_applied`
- `cost_adjusted_expected_excess_pct`

정책 판단:

- 신규 buy: CI lower bound가 0보다 낮으면 validation size 이하만 허용.
- add/scale-up: cost-adjusted CI lower bound가 0 이상이고 source-critical gate 통과 시에만 허용.
- trim/watch: 보유종목 CI lower가 음수이고 대체 후보 CI lower가 충분히 높으면 rotation trim watch.

### 2. Baseline Model Registry

최신 문헌은 복잡한 모델이 항상 우월하지 않음을 반복적으로 보여준다. 현 하네스는 다음 순서로 모델을 관리하는 것이 좋다.

1. price-only heuristic baseline.
2. regularized regression / simple tree / GBM baseline.
3. LLM-extracted event features added.
4. TSFM/Transformer shadow forecast.
5. portfolio utility-aware predict-and-optimize candidate.

승격 조건은 기존 원칙대로 price-only 대비 cost-adjusted incremental lift, walk-forward, CI, regime attribution이 있어야 한다.

### 3. Portfolio Utility Layer 구현

v1.10에 portfolio construction policy는 들어갔지만, 실제 산출물은 아직 부족하다. 다음 계산이 필요하다.

- position별 active risk contribution.
- theme/factor/cluster별 marginal exposure.
- candidate 추가 후 portfolio expected excess 변화.
- candidate 추가 후 adverse move / drawdown 변화.
- sell/trim 후보의 replacement margin.
- turnover cost와 expected fill probability.

결론적으로 신규 매수는 "좋은 종목인가"가 아니라 "현재 포트폴리오에 추가했을 때 효용이 증가하는가"로 판단해야 한다.

## 정책 개선 후보

### P0

- `source_signal_rows.jsonl` builder 구현.
- `review_due_index.json` / `review_rows.jsonl` / scorecard builder 구현.
- LLM 사용 정책을 YAML에 추가: extraction allowed, direct forecast shadow-only, direct order decision forbidden.
- Historical simulation에 `llm_memory_leakage_risk` 필드 추가.
- XBRL/fundamental feature extraction을 high-conviction sizing의 blocker로 연결.

### P1

- 후보별 forecast CI와 uncertainty shrinkage 추가.
- cost-adjusted expected excess와 turnover/fill probability를 order plan 필수 진단값으로 추가.
- sell diagnostic에 replacement margin의 CI 기준 추가.
- TSFM/Transformer forecast는 shadow-only로 저장하고 60~120 completed observations 전 주문에 쓰지 않는다.
- macro/regime overlay를 exposure throttle에 연결한다. 예: VIX, yield curve, credit spread, sector breadth.

### P2

- RAG 검색기를 local wiki/source store 위에 구성해 ticker별 최신 thesis packet을 자동 생성한다.
- analyst estimate revision, earnings call stance, guidance delta를 source-critical feature로 추가한다.
- model card와 feature drift report를 정기 생성한다.

## 현재 정책에 대한 판단

현재 방법은 "최신 문헌을 몰라서 뒤처진 구조"라기보다, 최신 문헌이 경고하는 실패를 꽤 잘 피하고 있다.

- 좋은 점: paper-only, strict gate, source confirmation, lead-lag, overheat guard, review throttle, sell diagnostic, portfolio construction 방향은 타당하다.
- 약한 점: feature가 문서와 manifest에 흩어져 있어 모델 학습 데이터로 바로 쓰기 어렵다.
- 가장 큰 리스크: LLM/RAG 결과가 narrative로만 남으면 좋은 설명은 쌓이지만 재현 가능한 alpha 검증으로 연결되지 않는다.
- 다음 개정 방향: 새 alpha를 추가하기보다 정보 행 구조화, forecast uncertainty, portfolio utility, LLM leakage control을 정책에 명시하고 구현한다.

## 참고 문헌 / 소스

- Lopez-Lira, Alejandro and Tang, Yuehua. `Can ChatGPT Forecast Stock Price Movements? Return Predictability and Large Language Models`. arXiv: https://arxiv.org/abs/2304.07619
- Kim, Alex G. and Muhn, Maximilian and Nikolaev, Valeri V. `Financial Statement Analysis with Large Language Models`. arXiv: https://arxiv.org/abs/2407.17866
- Chen, Weisi et al. `Leveraging large language model as news sentiment predictor in stock markets: a knowledge-enhanced strategy`. Springer Nature: https://link.springer.com/article/10.1007/s10791-025-09573-7
- Xie, Qianqian et al. `FinBen: A Holistic Financial Benchmark for Large Language Models`. NeurIPS 2024: https://proceedings.neurips.cc/paper_files/paper/2024/hash/adb1d9fa8be4576d28703b396b82ba1b-Abstract-Datasets_and_Benchmarks_Track.html
- Liu, Xiao-Yang. `Customized FinGPT Search Agents Using Foundation Models`. SSRN / ICAIF 2024: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4993491
- Lu, Juntong. `Time-Series Foundation Models in Finance`. SSRN: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5570099
- `Enhancing Financial Time-Series Forecasting with Retrieval-Augmented Large Language Models`. Hugging Face papers/arXiv: https://huggingface.co/papers/2502.05878
- `Machine learning for stock return prediction: Transformers or simple neural networks`. ScienceDirect: https://www.sciencedirect.com/science/article/pii/S1544612325020379
- Liao, Yuan et al. `The Uncertainty of Machine Learning Predictions in Asset Pricing`. arXiv: https://arxiv.org/abs/2503.00549
- `Robust portfolio selection with smart return prediction`. ScienceDirect: https://www.sciencedirect.com/science/article/pii/S0264999324000750
- `Adaptive robust online portfolio selection`. ScienceDirect: https://www.sciencedirect.com/science/article/pii/S0377221724006933
- U.S. SEC. `December 2024 Semi-Annual Report to Congress`: https://www.sec.gov/files/2024-fdta-machine-readable-data-report.pdf
- XBRL International. `How well do AI models like GPT-4 understand XBRL Data?`: https://www.xbrl.org/how-well-do-ai-models-like-gpt-4-understand-xbrl-data/
- Gao, Zhenyu et al. `A Test of Lookahead Bias in LLM Forecasts`. SSRN: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5985277
