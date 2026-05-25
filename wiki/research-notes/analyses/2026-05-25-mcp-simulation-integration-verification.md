---
id: 2026-05-25-mcp-simulation-integration-verification
created_at: 2026-05-25T18:28:00+09:00
paper: true
orders_submitted: 0
---

# MCP 시뮬레이션 반영 검증

## 결론

이번 검증에서 큰 이슈는 발견하지 못했다. 1년 장기 시뮬레이션은 기존 결과와 baseline 재실행이 완전히 일치했고, research MCP event feature cache를 무영향 값으로 전체 결합해도 성과와 추천 구성이 바뀌지 않았다. 동시에 감도 테스트에서는 추천 구성이 실제로 바뀌어 `score_adjustment`가 ranking에 반영되는 것도 확인했다.

다만 6개월 3시간 스크립트의 live smoke run은 sandbox가 `uv` cache 접근을 막아 끝까지 실행하지 못했다. 이 부분은 코드 결합 문제가 아니라 실행 환경 제약이다. 안전한 대안으로 기존 6개월 캡처 결과 1,425개 row에 최신 event join 로직을 적용했고, 단타/장타 모두 100% event feature 매칭을 확인했다.

## 1년 장기 시뮬레이션 검증

| 항목 | 기존 결과 | baseline 재실행 | 무영향 MCP cache | 감도 테스트 cache |
| --- | ---: | ---: | ---: | ---: |
| 추천 수 | 953 | 953 | 953 | 953 |
| 완료 수 | 853 | 853 | 853 | 853 |
| hit rate | 58.73388% | 58.73388% | 58.73388% | 57.913247% |
| 평균 SPY 초과수익 | +3.749958%p | +3.749958%p | +3.749958%p | +3.453211%p |
| event feature 매칭 | - | 0 / 953 | 953 / 953 | 953 / 953 |
| 사용 MCP server | - | 없음 | SEC/Alpha/FRED/Firecrawl/Yahoo | SEC/Alpha/FRED/Firecrawl/Yahoo |

무영향 cache에서는 baseline 대비 추천 key 차이가 0개였다. 따라서 event feature 결합 경로가 추가됐다는 이유만으로 기존 성과가 흔들리지는 않는다.

감도 테스트 cache에서는 `MU`에 2026-01-02 이후 큰 감점을 넣었다. 결과적으로 baseline 대비 추천 key 214개가 바뀌었고, `MU` 추천 수는 85개에서 57개로 줄었다. 이는 인위 테스트이므로 투자 성과 결론으로 해석하면 안 되지만, event feature가 실제 ranking과 추천 선택에 반영됨을 보여준다.

## 과거 장기/단기 대비 차이

과거 1년 장기 결과와 비교하면 성과 숫자는 그대로다. 달라진 점은 결과 자체가 아니라 결과의 provenance다. 이제 결과 JSON/Markdown에 `event_feature_cache_used`, `event_feature_matches`, `event_feature_coverage_pct`, `mcp_event_servers_used`가 남아 “이 시뮬레이션이 가격만 본 것인지, SEC/Alpha/FRED/Firecrawl/Yahoo event cache까지 본 것인지”를 구분할 수 있다.

과거 6개월 3시간 결과와 비교하면 기존 성과 기준선은 다음과 같다.

| 단타 정책 | trades | hit rate | P/L per 10k trade | validation hit | validation P/L |
| --- | ---: | ---: | ---: | ---: | ---: |
| `3h-momentum-top3` | 127 | 48.031496% | +981.432960 | 52.380952% | +1,640.290756 |
| `3h-momentum-top2` | 99 | 45.454545% | +517.945749 | 48.000000% | +971.654366 |
| `3h-vwap-reclaim-top2` | 35 | 48.571429% | +734.039580 | 38.888889% | +228.796339 |
| `3h-afternoon-continuation-top2` | 90 | 61.111111% | +1,530.609297 | 65.957447% | +971.738291 |

| 장타 정책 | recommendations | completed20 | hit20_abs | hit20_spy | avg SPY excess20 | validation avg SPY excess20 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `daily-3h-quality-top5` | 420 | 320 | 192 | 214 | +7.700837%p | +11.213664%p |
| `daily-3h-theme-capped-top5` | 420 | 320 | 195 | 214 | +7.823488%p | +11.095388%p |
| `daily-3h-momentum-top3` | 234 | 174 | 100 | 110 | +10.616914%p | +17.524234%p |

이번 변경 후 같은 captured rows에 무영향 cache를 적용하면 단타 trade row 351개, 장타 recommendation row 1,074개가 모두 100% 매칭된다. 즉 과거 단기/장기 시뮬레이션과의 결과적 차이는 “기존 성과가 즉시 좋아졌다/나빠졌다”가 아니라, 앞으로 실제 event cache가 채워질 때 non-price evidence가 순위와 제외 조건에 반영될 수 있게 된 점이다.

기존 `2026-05-24-short-long-policy-feb-mar-apr-may-review`와 비교하면 단타 validation 약세와 장타 validation 강세라는 판단은 유지된다.

- 단타 validation: v0/v1 정책은 각각 `-724.07`, `-624.07`, `-300.00`, `-200.00` P/L로 약했다.
- 장타 validation: `avg20=+25.6244%`, `avg_excess_spy20=+18.6411%p`, `hit20_spy=24/30`으로 강했다.

이번 조치는 이 결론을 뒤집지 않는다. 다만 앞으로 실적/SEC/매크로/IR/애널리스트/뉴스 event cache가 들어오면, 단타의 과열·뉴스 리스크 회피나 장타의 품질/촉매 보강을 score level에서 검증할 수 있게 됐다.

## 이슈 점검

- 직접 Alpaca market data REST 흔적: 테스트 assertion 외 없음.
- leakage control: event feature는 `available_at`/`asof_date`가 as-of 날짜 이하인 record만 사용한다.
- 주문 안전: 모든 검증 실행에서 `orders_submitted=0`.
- 테스트: `python3 -m unittest discover -s tests` 45개 통과.
- 남은 제약: 6개월 live smoke는 현재 sandbox에서 `uv` cache 접근이 막혀 실행하지 못했다. 기존 캡처 데이터 기반 coverage 감사로 대체했다.

## 2026-05-25 18:34 KST 추가 조치

`uv` cache 접근 문제는 wrapper 코드로 조치했다. `scripts/alpaca-mcp.sh`, `scripts/mcp-alpha-vantage.sh`, `scripts/mcp-sec-edgar.sh`, `scripts/mcp-yahoo-finance.sh`가 이제 `UV_CACHE_DIR`, `UV_TOOL_DIR`, `XDG_CACHE_HOME`, `XDG_DATA_HOME`을 레포 내부 `.cache/` 아래로 잡는다. 로컬 설치된 MCP 실행 파일이 있으면 `uvx` 없이 우선 사용한다.

재시도 결과 홈 디렉터리 cache/tool 권한 에러는 사라졌다. 다만 현재 레포-local cache가 비어 있어 `uvx`가 `alpaca-mcp-server`를 PyPI에서 받아오려 했고, sandbox DNS 제한으로 실패했다. unsandboxed 네트워크 실행은 정책상 승인되지 않았다. 따라서 남은 제약은 코드 경로가 아니라 최초 dependency fetch 권한이다.

추가 검증:

- `bash -n scripts/alpaca-mcp.sh scripts/mcp-alpha-vantage.sh scripts/mcp-sec-edgar.sh scripts/mcp-yahoo-finance.sh scripts/mcp-fred.sh scripts/mcp-firecrawl.sh`: PASS.
- `python3 -m unittest tests.test_mcp_runtime_wrappers`: 3개 통과.
- `python3 -m unittest discover -s tests`: 48개 통과.

원천: [[2026-05-25-mcp-uv-runtime-fix-sources]]

## 원천

- [[2026-05-25-mcp-simulation-integration-verification-sources]]
- [[2026-05-25-mcp-uv-runtime-fix-sources]]
- `wiki/evidence-store/run-manifests/2026-05-25-1828-mcp-simulation-integration-verification.json`
- `wiki/evidence-store/run-manifests/2026-05-25-1834-mcp-uv-runtime-fix.json`
- `wiki/evidence-store/sources/2026-05-25-mcp-verification-neutral-event-feature-cache.json`
- `wiki/evidence-store/sources/2026-05-25-mcp-verification-sensitivity-event-feature-cache.json`
