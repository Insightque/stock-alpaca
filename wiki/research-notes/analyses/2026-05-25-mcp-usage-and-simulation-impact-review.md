---
id: 2026-05-25-mcp-usage-and-simulation-impact-review
created_at: 2026-05-25T14:20:00+09:00
source_type: mcp-usage-impact-review
paper: true
orders_submitted: 0
---

# MCP 사용 여부와 시뮬레이션 영향 검토

## 결론

MCP 연결 자체는 개선됐다. `alpha-vantage`, `sec-edgar`, `yahoo-finance`, 로컬 `fred`, 로컬 `firecrawl`은 재확인 기준 정상 응답을 받았다. `fred`와 `firecrawl`은 외부 npm 즉석 실행 대신 각각 로컬 `scripts/fred-mcp-server.py`, `scripts/firecrawl-mcp-server.py`로 공식 API 데이터를 받을 수 있게 됐다.

2026-05-25 17:36 KST 재확인에서 Alpaca는 현재 세션에 이미 로드된 MCP 도구에서는 401이지만, `scripts/fetch-alpaca-bars-mcp.py`가 새로 띄운 로컬 Alpaca MCP 래퍼로는 SPY/QQQ 일봉을 정상 수집했다. 따라서 Alpaca는 키 자체보다 현재 Codex/IDE MCP 세션 재시작 문제가 더 유력하다.

Firecrawl은 현재 세션에 이미 로드된 MCP 도구에서는 여전히 `Invalid token`이지만, 공식 API 직접 호출과 새 로컬 Firecrawl MCP wrapper는 정상 동작했다. 기존 `npx firecrawl-mcp` 방식은 API 키를 외부 npm 패키지 프로세스에 넘기는 구조라 보안 검토에서 차단됐고, 이를 레포 내부 로컬 MCP 서버로 교체했다.

다만 과거 실행 이력을 보면 MCP가 항상 분석에 반영된 것은 아니다. 특히 `2026-05-25` 현재 추천은 quick no-submit run이라 Alpaca/Yahoo Finance 중심이었고, SEC/Alpha/FRED/Firecrawl은 데이터 공백으로 남았다. 가격 기반 정책 백테스트는 대부분 의도적으로 Alpaca bars만 사용했다.

따라서 개선 방향은 두 단계다.

- 현재 추천/daily run: 보강 MCP를 실제 점수와 리스크 판단에 사용해야 한다.
- 대규모 시뮬레이션: MCP 연결만으로 결과가 바뀌지 않는다. SEC/earnings/macro/IR feature를 시점별로 캐시하고 leakage control을 적용한 뒤 시뮬레이터에 feature로 결합해야 한다.

## Workflow 기준과 실제 사용

| 구분 | 정책상 기대 | 실제 이력 | 판단 |
| --- | --- | --- | --- |
| daily/current recommendation | Alpaca, SEC EDGAR, Alpha Vantage, FRED, Firecrawl, Yahoo Finance | 2026-05-24는 Alpaca/SEC/Alpha/Yahoo 사용, FRED 공백. 2026-05-25는 Alpaca/Yahoo만 사용 | quick run에서는 누락이 있었고 submit 후보 전 보강 필수 |
| historical decision simulation | 기준시점 이전 Alpaca, SEC, Alpha, FRED, Firecrawl, Yahoo | 2026-05-15 decision report는 Alpaca/SEC만 사용 | strict as-of 재현을 우선해 일부러 제한했지만, 이제 FRED/Alpha/Firecrawl as-of 보강 가능 |
| MCP comparison / policy reaudit | 기존 결과에 MCP 보강을 붙여 결론 차이 확인 | 2026-05-08 비교와 2026-05-24 재감사는 Alpha/SEC/Firecrawl/Yahoo를 썼지만 FRED는 실패 | FRED gap은 이번 로컬 MCP 적용으로 해소 가능 |
| one-year daily policy simulation | Alpaca 일봉 기반 수치 검증 | Alpaca만 사용 | 의도된 가격 기반 검증. MCP 연결만으로 숫자가 자동 변경되지는 않음 |

## 최근 run manifest 감사

| run | 사용 MCP | 누락/공백 |
| --- | --- | --- |
| `2026-05-24-1227-current-recommendations` | Alpaca, SEC EDGAR, Alpha Vantage, Yahoo Finance | Alpha broad news 0건, FRED callable tool 미노출 |
| `2026-05-24-3h-six-month-policy-review` | Alpaca | 가격/거래량 기반 정책 검증이라 보강 MCP 미사용 |
| `2026-05-24-expanded-six-month-3h-policy-review` | Alpaca | 가격/거래량 기반 정책 검증이라 보강 MCP 미사용 |
| `2026-05-25-0842-current-recommendations` | Alpaca, Yahoo Finance | SEC, Alpha, FRED, Firecrawl 미조회 |
| `2026-05-25-one-year-daily-policy-simulation` | Alpaca | 일봉 가격 기반 정책 검증. SEC/earnings/macro/valuation feature 미결합 |

## 새 MCP 확인 결과

### 2026-05-25 17:58 KST 현재 세션 재점검

현재 Codex 세션 기준으로 다시 확인했다. 키 값은 출력하지 않았고, `ALPACA_PAPER_TRADE=true`만 확인했다. 실제 주문, 취소, 교체, 포지션 청산 도구는 호출하지 않았다.

| MCP | 현재 상태 | 확인 내용 | 남은 공백 |
| --- | --- | --- | --- |
| Alpaca | 정상 | `get_calendar`, `get_account_info`, `get_all_positions`, `get_watchlists`, `get_stock_bars`, `get_news` read-only 호출 성공. SPY/QQQ 2026-05-20~2026-05-22 IEX adjusted 일봉 각각 3개 확인 | 로컬 `scripts/fetch-alpaca-bars-mcp.py` 새 실행은 sandbox의 uv cache 접근 제한으로 실패했고, escalated rerun은 credential network 사용 때문에 거부됨 |
| Alpha Vantage | 정상 | `TOOL_LIST`, `PING`, AMD `EARNINGS_CALENDAR` 성공. AMD 다음 예상 실적일 2026-08-04, estimate 1.61 확인 | 없음 |
| SEC EDGAR | 정상 | AMD `get_company_info`, `get_recent_filings` 성공. 최근 30일 filing 3건 확인 | 없음 |
| Yahoo Finance | 정상 | AMD `get_stock_info`, `get_recommendations` 성공 | 없음 |
| FRED | 부분 확인 | 로컬 `scripts/mcp-fred.sh`가 `initialize`/`tools/list`에 응답했고 4개 도구를 노출 | 공식 FRED API health check는 sandbox DNS 제한으로 실패했고, escalated rerun이 거부되어 이번 세션에서는 외부 API 호출까지 확인하지 못함 |
| Firecrawl | 정상 | 로컬 `scripts/mcp-firecrawl.sh`가 `initialize`/`tools/list`에 응답했고, `--health-check` 공식 API 호출도 성공 | 없음 |

시뮬레이션 스모크는 기존 Alpaca MCP 캡처 파일 `wiki/evidence-store/sources/2026-05-25-one-year-daily-bars.json`으로 재실행했다. 결과는 `daily_independent_runs=191`, `recommendations=953`, `completed=853`, 비용 차감 hit rate `58.73388%`, 평균 SPY 초과수익 `+3.749958%p`, 정책 상태 `active_dry_run_candidate`, `orders_submitted=0`으로 재현됐다.

이번 재점검의 핵심 결론은 “MCP 연결은 대부분 정상이나, 모든 시뮬레이션이 모든 MCP를 쓰는 구조는 아니다”이다. 가격 기반 1년/6개월 시뮬레이션은 설계상 Alpaca bars 중심이고, SEC/Alpha/FRED/Firecrawl/Yahoo 결과는 아직 event-level feature cache로 결합되어 있지 않다. 또한 `scripts/simulate-intraday-policy-candidates.py`와 `scripts/simulate-short-long-policy-review.py`에는 Alpaca market data REST를 직접 `curl`로 읽는 경로가 남아 있어 MCP-only 원칙에 맞게 이전해야 한다.

원천 기록: [[2026-05-25-mcp-connection-simulation-audit-sources]]

### 2026-05-25 18:16 KST 조치 완료

이전 감사에서 남았던 구현 공백 중 직접 조치 가능한 부분을 반영했다.

| 공백 | 조치 | 상태 |
| --- | --- | --- |
| `simulate-intraday-policy-candidates.py`의 Alpaca market data REST 직접 `curl` | 공용 `scripts/alpaca_mcp_bars.py`를 추가하고 `get_stock_bars` MCP 호출로 이전 | 완료 |
| `simulate-short-long-policy-review.py`의 Alpaca market data REST 직접 `curl` | 같은 Alpaca MCP helper로 이전 | 완료 |
| 1년 장기 시뮬레이션의 research MCP feature 미결합 | `--event-features-json` 입력, point-in-time join, `score_adjustment`, `source_confidence_delta`, `exclude`, `mcp_gaps`, `source_refs` 반영 | 완료 |
| 6개월 3시간 정책 리뷰의 research MCP feature 미결합 | `--event-features-json` 입력, 단타/장타 row feature 결합, daily score와 intraday ranking에 event adjustment 반영 | 완료 |
| workflow 문서의 feature cache 기준 부재 | `harness/templates/event-feature-cache.json`와 one-year workflow 단계 추가 | 완료 |

검증 결과 `python3 -m unittest discover -s tests`는 45개 통과했다. 샘플 event feature cache로 1년 시뮬레이션을 재실행했을 때 `mcp_event_servers_used=alpha-vantage,firecrawl,fred,sec-edgar,yahoo-finance`, `event_feature_cache_used=true`, `orders_submitted=0`을 확인했다.

주의: 이것은 “feature cache를 결합할 수 있는 경로”를 닫은 것이며, 전체 1년/6개월 표본에 대해 모든 종목/날짜의 research MCP cache가 이미 채워졌다는 뜻은 아니다. 실제 정책학습 성능을 다시 평가하려면 as-of cache coverage를 충분히 만든 뒤 재시뮬레이션해야 한다.

원천 기록: [[2026-05-25-mcp-simulation-integration-fix-sources]]

### 2026-05-25 17:36 KST 재확인

| MCP | 상태 | 확인 내용 | 조치 |
| --- | --- | --- | --- |
| Alpaca | 부분 정상 | 현재 로드된 MCP 도구는 계좌/시세 모두 401. 새 Alpaca MCP helper는 SPY/QQQ IEX 일봉 3개씩 정상 수집 | 현재 Codex/IDE MCP 세션 재시작 필요 |
| Alpha Vantage | 정상 | AMD `EARNINGS_CALENDAR` 응답 확인 | 현재 추천/시뮬레이션 보강에 사용 가능 |
| SEC EDGAR | 정상 | AMD 2026-05-06 10-Q income statement 응답 확인 | filing 기반 재무 확인에 사용 가능 |
| Yahoo Finance | 정상 | AMD stock info 응답 확인 | 보조 analyst/news/financial context에 사용 가능 |
| FRED | 정상 | `DGS10` latest date 2026-05-21 health check 통과 | 매크로 regime 입력에 사용 가능 |
| Firecrawl | 부분 정상 | 현재 로드된 MCP 도구는 `Invalid token`. 공식 API는 정상, 새 로컬 Firecrawl MCP wrapper도 `firecrawl_scrape` 정상 | 현재 Codex/IDE MCP 세션 재시작 필요 |

시뮬레이션 스모크 테스트는 두 단계로 확인했다.

- 로컬 Alpaca MCP helper로 `SPY,QQQ` 2026-05-20~2026-05-22 IEX adjusted 일봉을 수집했다. 두 종목 모두 3개 bar가 로드됐다.
- 기존 1년 입력 `wiki/evidence-store/sources/2026-05-25-one-year-daily-bars.json`으로 재실행한 결과 `daily_independent_runs=191`, `recommendations=953`, `completed=853`, 비용 차감 hit rate `58.73388%`, 평균 SPY 초과수익 `+3.749958%p`, 정책 상태 `active_dry_run_candidate`가 재현됐다.

### FRED

로컬 FRED MCP로 `get_macro_snapshot`을 호출해 기준일 macro를 확인했다.

| 기준일 | DGS10 | DGS2 | FEDFUNDS | CPIAUCSL | UNRATE | NFCI |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 2026-05-15 | 4.59 | 4.09 | 3.64 | 332.407 | 4.3 | -0.52300 |
| 2026-05-22 | 4.57 | 4.08 | 3.64 | 332.407 | 4.3 | -0.52300 |

해석: 금리는 높은 편이고 10Y-2Y spread는 약 +0.49~+0.50%p다. 반면 NFCI는 음수라 금융여건은 평균보다 완화적인 쪽이다. 따라서 macro는 “무조건 위험 회피”가 아니라 “높은 금리 부담은 있으나 금융여건은 아직 risk-on을 막지 않는 상태”로 보는 편이 맞다.

### Alpha Vantage

- AMD `EARNINGS`: 2026-05-05 post-market, EPS 1.37 vs estimate 1.29, surprise +6.2016%.
- AMD `EARNINGS_CALENDAR`: 다음 예상 실적일 2026-08-04, fiscal quarter 2026-06-30, estimate 1.61.
- UNH `EARNINGS_CALENDAR`: 다음 예상 실적일 2026-07-28, fiscal quarter 2026-06-30, estimate 4.85.
- LRCX `EARNINGS_CALENDAR`: 3개월 horizon 응답에서 예정 행 없음.

해석: AMD는 실적 beat 자체가 긍정 근거라기보다, 이미 반응한 가격을 추격하지 않도록 `post-earnings-overheat` 감점에 쓰는 것이 맞다. UNH/AMD의 다음 실적일은 가까운 며칠 내 이벤트가 아니므로 2026-05-25 추천을 즉시 막지는 않는다.

### Firecrawl

Firecrawl은 이전 감사에서 공식 IR/뉴스룸 URL 확인에 사용됐다. 2026-05-25 17:36 KST 재확인 기준 현재 세션에 이미 로드된 MCP는 `Invalid token`이지만, 공식 API 직접 호출과 새 로컬 `scripts/firecrawl-mcp-server.py` wrapper의 MCP `tools/list` 및 `firecrawl_scrape`는 정상 동작했다. 따라서 다음 Codex/IDE MCP 세션 재시작 후에는 Firecrawl 보강을 사용할 수 있는 상태다.

## 표본별 변경 영향

| 표본 | 기존 결론 | MCP 추가 연결 후 변화 | 결론 변경 |
| --- | --- | --- | --- |
| 2026-05-25 현재 추천 | LRCX, UNH, AMD 우선. 시장 휴장/fresh quote 부재로 주문 없음 | FRED는 높은 금리와 완화적 금융여건을 함께 보여줘 macro 중립~약한 주의. Alpha는 AMD 실적 beat 후 과열 감점을 강화하고, UNH/AMD 다음 실적이 임박하지 않음을 확인. Firecrawl/SEC 원문 확인은 submit 전 source confidence 강화 대상 | 순위 자체는 유지. AMD는 staged-only 근거가 더 강해짐 |
| 2026-05-15 decision process report | NOK, UNH, GOOGL staged buy. AMD/MU는 과열로 small staged/watch | FRED 2026-05-15는 시장 레짐 risk-on 판단을 뒤집지 않음. Alpha AMD 2026-05-05 beat는 AMD 과열 제한을 더 강하게 뒷받침. Firecrawl은 공식 IR 확인으로 근거 품질 개선 가능 | 큰 결론 유지. AMD full-size 금지 근거 강화 |
| 2026-05-08 MCP 비교 표본 | NVDA, IONQ, UNH 유지. AMD/TSLA 제외 판단 강화 | 이미 Alpha/SEC/Firecrawl/Yahoo를 쓴 표본이다. 새 FRED는 macro gap을 채우지만 추천 세트 변화보다는 당시 risk-on/금리 부담 설명을 보강 | 추천 세트 유지 |
| 1년 일봉 정책 시뮬레이션 | `active_dry_run_candidate`, 비용 차감 hit rate 58.73%, 평균 SPY 초과 +3.75% | MCP 연결만으로 수치가 자동 변경되지 않음. event-level earnings/SEC/macro/IR feature를 일별 as-of cache로 만들고 시뮬레이터에 넣어야 결과가 바뀜 | 현재 결과 유지. 다음 버전에서 feature 결합 필요 |

## 적절성 평가

현재 기준으로는 “MCP가 연결되어 있느냐”보다 “run 타입별로 의무 호출 여부가 명확하냐”가 더 중요하다.

- 현재 추천에서 `주문 후보` 또는 `submit 가능성`이 있으면 SEC, Alpha, FRED, Firecrawl, Yahoo Finance 보강을 필수로 해야 한다.
- quick no-submit은 일부 MCP 생략이 가능하지만, 그 경우 추천 리포트와 manifest에 `not queried`를 데이터 공백으로 명확히 남겨야 한다.
- 가격 기반 backtest는 MCP 미사용이 허용된다. 대신 문서에 “가격 기반 검증이며 event/fundamental/macro feature 미결합”을 계속 명시해야 한다.
- 과거 시점 decision simulation은 현재 MCP 결과를 그대로 쓰면 미래정보 누출 위험이 있다. SEC acceptance time, Alpha reportedDate, FRED observation/realtime date, Firecrawl URL publication date를 기준시점 이전으로 제한해야 한다.

## 다음 개선 과제

1. daily/historical report에 `MCP coverage matrix`를 필수 섹션으로 추가한다.
2. run manifest에 `mcp_coverage` 필드를 추가해 `queried`, `used_in_score`, `gap_reason`, `source_ref`를 기록한다.
3. Alpha broad query가 0건이면 추천 상위 5개는 per-ticker fallback을 자동 수행한다.
4. FRED macro snapshot을 daily run 기본 입력으로 넣고, 최소한 `DGS10`, `DGS2`, `FEDFUNDS`, `CPIAUCSL`, `UNRATE`, `NFCI`를 raw source에 저장한다.
5. Firecrawl은 submit 후보의 공식 IR/press release 원문 확인에 사용한다. 검색/추출 실패는 source confidence 감점으로 연결한다.
6. 대규모 backtest는 기존 성과표를 다시 쓰기 전에 as-of event feature cache를 먼저 만들어야 한다.

## 출처

- `harness/workflows/daily.md`
- `harness/workflows/historical-decision-sim.md`
- `harness/workflows/one-year-daily-simulation.md`
- `harness/mcp-source-map.md`
- `wiki/evidence-store/run-manifests/2026-05-24-1227-current-recommendations.json`
- `wiki/evidence-store/run-manifests/2026-05-25-0842-current-recommendations.json`
- `wiki/evidence-store/run-manifests/2026-05-25-one-year-daily-policy-simulation.json`
- `wiki/current-runs/daily/2026-05-25.md`
- `wiki/backtest-runs/results/2026-05-24-may-15-decision-process-report.md`
- `wiki/research-notes/analyses/2026-05-24-mcp-comparison-2026-05-08-historical-simulation.md`
- FRED 로컬 MCP `get_macro_snapshot`
- Alpha Vantage MCP `EARNINGS`, `EARNINGS_CALENDAR`
