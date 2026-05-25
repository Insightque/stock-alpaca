---
id: 2026-05-25-mcp-simulation-integration-verification-sources
created_at: 2026-05-25T18:28:00+09:00
source_type: mcp-simulation-integration-verification-source
paper: true
orders_submitted: 0
---

# MCP 시뮬레이션 결합 검증 원천

## 목적

사용자 요청에 따라 MCP-only market data 경로와 research MCP event feature cache 결합이 실제 시뮬레이션 결과에 반영됐는지 검증했다. 주문, 취소, 포지션 변경은 없었다.

## 입력 자료

| 자료 | 경로 |
| --- | --- |
| 1년 일봉 입력 | `wiki/evidence-store/sources/2026-05-25-one-year-daily-bars.json` |
| 기존 1년 결과 | `wiki/evidence-store/sources/2026-05-25-one-year-daily-policy-simulation-data.json` |
| 기존 6개월 3시간 결과 | `wiki/evidence-store/sources/2026-05-24-six-month-3h-simulation-data.json` |
| 기존 단기/장기 결과 | `wiki/evidence-store/sources/2026-05-24-short-long-policy-simulation-data.json` |
| 무영향 event cache | `wiki/evidence-store/sources/2026-05-25-mcp-verification-neutral-event-feature-cache.json` |
| 감도 테스트 event cache | `wiki/evidence-store/sources/2026-05-25-mcp-verification-sensitivity-event-feature-cache.json` |

무영향 cache는 62개 심볼 전체에 `score_adjustment=0.0`, `source_confidence_delta=0.0`, `exclude=false`를 부여해 결합 coverage와 회귀를 확인하는 용도다. 감도 테스트 cache는 같은 neutral coverage에 더해 `MU`에 2026-01-02 이후 `score_adjustment=-100.0`을 부여한 인위 테스트 자료다. 감도 테스트는 실제 투자 결론이 아니라 ranking engine이 event feature를 반영하는지 확인하기 위한 자료다.

## 실행 결과

1년 장기 시뮬레이션 재실행:

| 실행 | event cache | 추천 | 완료 | hit rate | 평균 SPY 초과수익 | event 매칭 | MCP servers |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| 기존 결과 | 없음 | 953 | 853 | 58.73388% | +3.749958%p | - | - |
| baseline 재실행 | 없음 | 953 | 853 | 58.73388% | +3.749958%p | 0 / 953 | 없음 |
| 무영향 cache | 있음 | 953 | 853 | 58.73388% | +3.749958%p | 953 / 953 | `alpha-vantage`, `firecrawl`, `fred`, `sec-edgar`, `yahoo-finance` |
| 감도 테스트 cache | 있음 | 953 | 853 | 57.913247% | +3.453211%p | 953 / 953 | `alpha-vantage`, `firecrawl`, `fred`, `sec-edgar`, `yahoo-finance` |

추가 비교:

- 기존 1년 결과와 baseline 재실행은 `daily_independent_runs=191`, `recommendations=953`, `completed=853`, `hit_rate_after_cost_pct=58.73388`, `avg_excess_after_cost_pct=3.749958`, `median_excess_after_cost_pct=1.462286`, `avg_adverse_move_20d_pct=-6.462812`가 모두 일치했다.
- baseline과 무영향 cache 실행은 추천 key 차이가 0개였고, score 변경 row도 0개였다.
- 감도 테스트 cache는 baseline 대비 추천 key 214개가 바뀌었다. `MU` 추천 수는 85개에서 57개로 감소했다.
- 모든 실행에서 `orders_submitted=0`이었다.

기존 6개월 3시간 결과에 대한 event feature coverage 감사:

| 구분 | row 수 | event 매칭 | coverage | MCP servers |
| --- | ---: | ---: | ---: | --- |
| 단타 trade rows | 351 | 351 | 100.0% | `alpha-vantage`, `firecrawl`, `fred`, `sec-edgar`, `yahoo-finance` |
| 장타 recommendation rows | 1,074 | 1,074 | 100.0% | `alpha-vantage`, `firecrawl`, `fred`, `sec-edgar`, `yahoo-finance` |

6개월 실제 MCP smoke run은 다음 명령으로 제한 범위 실행을 시도했으나 sandbox가 `uv` cache 접근을 막아 실패했다.

```bash
python3 scripts/simulate-six-month-3h-policy-review.py \
  --start 2026-05-01 \
  --end 2026-05-08 \
  --symbols AMD,MU,NOK,SPY,QQQ,SMH \
  --event-features-json wiki/evidence-store/sources/2026-05-25-mcp-verification-neutral-event-feature-cache.json \
  --output-json /private/tmp/verify-six-month-smoke.json \
  --output-md /private/tmp/verify-six-month-smoke.md \
  --source-md /private/tmp/verify-six-month-smoke-source.md \
  --run-manifest /private/tmp/verify-six-month-smoke-manifest.json
```

실패 요약:

- `uv` cache 경로 `/Users/insightque/.cache/uv/sdists-v9/.git` 접근이 sandbox에서 거부됐다.
- unsandboxed 재시도는 정책상 승인되지 않았다.
- 대체 검증으로 기존 캡처된 6개월 결과 row에 최신 event feature 결합 함수를 적용해 100% 매칭을 확인했다.

## 검증 명령

- `python3 scripts/simulate-one-year-daily-policy.py ... --output-json /private/tmp/verify-one-year-baseline.json`
- `python3 scripts/simulate-one-year-daily-policy.py ... --event-features-json wiki/evidence-store/sources/2026-05-25-mcp-verification-neutral-event-feature-cache.json --output-json /private/tmp/verify-one-year-neutral.json`
- `python3 scripts/simulate-one-year-daily-policy.py ... --event-features-json wiki/evidence-store/sources/2026-05-25-mcp-verification-sensitivity-event-feature-cache.json --output-json /private/tmp/verify-one-year-sensitivity.json`
- `python3 -m unittest discover -s tests`: 45개 통과.
- `rg -n "APCA-API|data\\.alpaca\\.markets|Alpaca Market Data API|urllib\\.parse" scripts harness tests -g '*.py' -g '*.md'`: 테스트 파일의 금지 문자열 assertion 외 직접 REST 흔적 없음.

## 산출물 hash

| 파일 | sha256 |
| --- | --- |
| `wiki/evidence-store/sources/2026-05-25-mcp-verification-neutral-event-feature-cache.json` | `0fe9563b98eeffb1e176676acffa462bc7d291f27ef11484864aeda48b6f1596` |
| `wiki/evidence-store/sources/2026-05-25-mcp-verification-sensitivity-event-feature-cache.json` | `b835e403ab045cf3384fd4c35304285cb791a95cbf991e0737276522f35d4664` |
| `/private/tmp/verify-one-year-baseline.json` | `38f18d254c4f4337eb6181aa892d3f6acad55272e6ef97f32757aa12670e1288` |
| `/private/tmp/verify-one-year-neutral.json` | `21d4842e929464ae6291f7711eafd7ff4d67ebc9958879e4d8b89f4270dce189` |
| `/private/tmp/verify-one-year-sensitivity.json` | `69f91a152affea3c569c8353c1a844eaa9386694f88f4c2c51bab6c1d0e95e97` |
