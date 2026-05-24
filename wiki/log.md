# Trading Wiki Log

Append new entries below. Do not rewrite earlier entries except to fix broken Markdown formatting.

## [2026-05-22 21:45 Asia/Seoul] setup | Harness initialized

- Added initial llm-wiki structure for Alpaca paper-trading research and execution.
- Default policy: paper only, US stocks/ETFs only, day limit orders, medium risk.

## [2026-05-22 22:39 Asia/Seoul] daily | Current no-submit analysis

- Interpreted `현재 기준 분석해줘` as a daily current-market analysis in no-submit mode.
- Confirmed `ALPACA_PAPER_TRADE=true`; Alpaca market clock was open.
- Account snapshot: portfolio value 100000 USD, cash 100000 USD, no positions, no open US equity orders, no watchlists.
- Built fallback universe from market proxies plus Alpaca most-active/mover symbols: SPY, QQQ, SMH, SOXS, RGTI, FUTU, TIGR, LFS, QTEX, BIYA.
- Updated daily report, ticker pages, raw source notes, portfolio snapshot, and empty dry-run order plan.
- Submitted orders: none.
- Skipped orders: all, because the run was no-submit and no watchlist/target allocation exists yet.
- Report: `wiki/reports/daily/2026-05-22.md`.

## [2026-05-22 22:45 Asia/Seoul] wiki | Daily report Korean format

- Updated `wiki/reports/daily/2026-05-22.md` so the daily report body is written in Korean.
- User preference recorded for future daily reports: write daily reports in Korean.

## [2026-05-22 22:47 Asia/Seoul] wiki | 기록 언어 정책 한글화

- `wiki/tickers/`의 기존 종목 분석 페이지 10개를 한글 본문으로 변경했다.
- `wiki/index.md`의 설명 문구도 한글로 정리했다.
- 앞으로 위키, 리포트, 종목 분석, 포트폴리오 노트, raw source 요약, 로그는 기본적으로 한글로 작성하도록 `AGENTS.md`에 규칙을 추가했다.

## [2026-05-22 22:50 Asia/Seoul] harness | 거래 회고 및 추천 정책 개선 루프 추가

- `거래 회고해줘` 명령을 `harness/workflows/trade-review.md`로 라우팅하도록 추가했다.
- 체결 거래를 당시 thesis, 주문 계획, 시장 맥락, raw source, 실제 결과와 비교하는 회고 워크플로우를 추가했다.
- `wiki/reviews/trades/`와 `wiki/policies/recommendation-policy.md`를 신설했다.
- post-trade, daily, research, rebalance 워크플로우가 거래 회고와 추천 정책을 확인하도록 연결했다.
- 목적: 거래된 종목의 판단 품질을 회고하고, 반복적으로 확인된 교훈을 향후 추천 정책에 반영한다.

## [2026-05-22 23:10 Asia/Seoul] analysis | ETF 제외 주식 중심 거래 제안

- 사용자 요청에 따라 ETF를 제외하고 주식 중심 후보를 분석했다.
- Paper mode, 시장 개장, 계좌 현금 100000 USD, 포지션 없음, 미체결 주문 없음을 확인했다.
- 검토 후보: NVDA, RGTI, IONQ, QBTS, AMD, MU, INTC, TSLA, RKLB, NOK, NIO, GOVX.
- 최종 dry-run 거래 제안: NVDA 46주, AMD 21주, NOK 650주, RGTI 190주, IONQ 75주.
- 총 예상 매수 금액은 39183.30 USD로 포트폴리오 약 39.2%다.
- 실제 주문은 제출하지 않았다.
- 분석: `wiki/analyses/2026-05-22-stock-only-trade-proposal.md`.
- 주문 계획: `wiki/portfolio/order-plans/2026-05-22-stock-only-proposal.json`.

## [2026-05-22 23:16 Asia/Seoul] analysis | 추가 요청 종목 반영 매수 계획 업데이트

- 사용자 요청 종목 Lam Research, TSMC, UnitedHealth, Eaton, Broadcom, Palantir, Tesla를 각각 LRCX, TSM, UNH, ETN, AVGO, PLTR, TSLA로 해석해 검토했다.
- 7개 모두 Alpaca 기준 active/tradable 주식으로 확인했다.
- 업데이트된 dry-run 매수 계획은 NVDA, AMD, AVGO, LRCX, TSM, NOK, UNH, ETN, RGTI, IONQ 총 10개 주문이다.
- PLTR, TSLA, QBTS는 분석했지만 이번 주문 계획에서는 제외했다.
- 총 예상 매수 금액은 56254.75 USD, 예상 투자 노출은 약 56.3%다.
- 실제 주문은 제출하지 않았다.
- 업데이트 파일: `wiki/portfolio/order-plans/2026-05-22-stock-only-proposal.json`, `wiki/analyses/2026-05-22-stock-only-trade-proposal.md`.

## [2026-05-22 23:26 Asia/Seoul] execution | 주식 중심 paper 매수 실행

- 사용자 요청 `매수해줘`를 명시적 주문 실행 요청으로 해석했다.
- `.env`에서 `ALPACA_PAPER_TRADE=true`를 확인했고 Alpaca clock 기준 장중임을 확인했다.
- 주문 전 모든 후보가 Alpaca asset 기준 active/tradable US equity임을 확인했다.
- `scripts/check-risk-policy.py` 검증 결과 PASS: buy notional 56098.45 USD, 주문 후 예상 cash 43901.55 USD.
- Alpaca MCP `place_stock_order`로 day limit whole-share buy 주문 10건을 제출했다.
- 체결: AMD, AVGO, LRCX, TSM, NOK, UNH, ETN, RGTI, IONQ.
- 미체결: NVDA 35주, limit 215.32, status new.
- 사후 계좌: portfolio value 100041.52 USD, cash 51566.78 USD, buying power 138036.10 USD, long market value 48474.74 USD.
- 원천 기록: `wiki/raw/sources/2026-05-22-paper-order-submission.md`.

## [2026-05-23 00:17 Asia/Seoul] session | Happy Codex 작업 세션 시작

- 새 Happy Codex 작업 세션에서 저장소 상태를 짧게 확인했다.
- 현재 브랜치: `main`.
- `git status --short` 기준 미추적 항목: `.openclaw/`, `HEARTBEAT.md`, `IDENTITY.md`, `SOUL.md`, `TOOLS.md`, `USER.md`.
- 이번 확인에서는 Alpaca MCP 호출, 시장 데이터 조회, 주문 제출, 리스크 검증을 수행하지 않았다.

## [2026-05-23 00:20 Asia/Seoul] post-trade | 오늘 주식 체결현황 조회

- 사용자 요청 `오늘 주식 체결현황 조회`를 post-trade 조회로 해석했다. 새 주문은 제출하지 않았다.
- `.env`에서 `ALPACA_PAPER_TRADE=true`를 확인했다.
- Alpaca clock: `2026-05-22T11:20:24.233474202-04:00` 기준 장중.
- 계좌: portfolio value 100567.57 USD, cash 51566.78 USD, buying power 138444.15 USD, long market value 49000.79 USD.
- 주문 상태: 체결 9건, 미체결 1건, 취소/실패 0건.
- 체결: AMD, AVGO, LRCX, TSM, NOK, UNH, ETN, RGTI, IONQ.
- 미체결: NVDA 35주 buy limit 215.32, status `new`.
- 현재 포지션은 체결된 9개 종목과 일치한다. 거래 회고는 아직 `회고 대기`다.
- 업데이트: `wiki/portfolio/current.md`, `wiki/reports/daily/2026-05-22.md`, `wiki/raw/sources/2026-05-23-alpaca-fill-status.md`, `wiki/index.md`.

## [2026-05-23 00:26 Asia/Seoul] research | 다음 미국 거래일 유망종목 분석

- 사용자 요청 `내일 유망종목`을 한국 시간 2026-05-23 토요일 기준으로 해석했다.
- 한국 기준 내일 2026-05-24는 일요일이고, 미국 2026-05-25는 Memorial Day 휴장으로 확인했다.
- 실제 다음 미국 정규 거래일은 2026-05-26 화요일이다.
- 현재 셸 환경에서 `ALPACA_PAPER_TRADE`가 비어 있어 주문 워크플로우는 중단 조건이며, Alpaca MCP 도구도 이번 세션에 노출되지 않았다.
- 주문, 매수, 매도, 주문 계획 생성은 수행하지 않았다.
- 기존 포트폴리오 노출과 2026-05-22 가격/뉴스 원천을 바탕으로 research-only 후보 요약을 작성했다.
- 원천 기록: `wiki/raw/sources/2026-05-23-next-session-research.md`.

## [2026-05-23 00:57 Asia/Seoul] harness | 과거 시점 추천 시뮬레이션과 정책학습 워크플로우 추가

- 과거 특정 시점 기준으로 당시 정보만 사용해 종목과 매수/매도 수량을 추천하는 워크플로우를 추가했다.
- 추천 이후 1D/5D/20D 실제 가격으로 추천 품질을 회고하는 워크플로우를 추가했다.
- 미래 정보 누출 방지를 위해 추천 문서와 회고 문서를 분리하도록 규칙화했다.
- 새 저장소: `wiki/simulations/`, `wiki/reviews/decisions/`.
- 새 템플릿: `harness/templates/historical-decision.md`, `harness/templates/historical-decision-review.md`.
- 주문 제출은 금지하고, 과거 추천 주문 계획은 항상 dry-run으로만 생성하도록 했다.

## [2026-05-23 00:57 Asia/Seoul] docs | 과거 기준 시뮬레이션 회고 사용법 가이드 보강

- `harness/agent-tasking-guide.md`에 과거 기준 추천 시뮬레이션 사용 절차를 추가했다.
- 기준일/정확한 시각/종목군 지정 예시를 문서화했다.
- 추천 문서, raw source, dry-run 주문 계획, 회고 문서의 저장 위치를 정리했다.
- 1D/5D/20D 회고와 정책학습 지표 반영 방식을 설명했다.
- 미래 정보 누출 금지와 실제 주문 미제출 원칙을 사용법 섹션에 명시했다.

## [2026-05-23 06:18 Asia/Seoul] simulation | 30일 전~15일 전 과거 추천 시뮬레이션 및 회고 배치

- 사용자 요청에 따라 2026-04-23부터 2026-05-08까지 16개 calendar date를 1일 단위로 처리했다.
- 주말 기준일 2026-04-25, 2026-04-26, 2026-05-02, 2026-05-03은 직전 미국 정규 거래일 종가 기준으로 보정했다.
- 해당 기간에는 저장소 위키가 존재하지 않아 strict historical universe가 비어 있었고, 현재 위키의 보유/주문 후보를 fallback universe로 사용했다.
- Alpaca MCP `get_stock_bars` daily IEX 데이터를 사용했고, 응답 절단으로 PLTR은 배치 계산에서 제외했다.
- 날짜별 dry-run 주문 계획 16개를 생성했고 `scripts/check-risk-policy.py` 검증을 모두 통과했다.
- 추천 배치: `wiki/simulations/2026-04-23-to-2026-05-08-historical-decision-batch.md`.
- 회고 배치: `wiki/reviews/decisions/2026-04-23-to-2026-05-08-historical-review-batch.md`.
- 원천 기록: `wiki/raw/sources/2026-05-23-historical-batch-2026-04-23-to-2026-05-08-alpaca.md`.
- 5D 기준 hit rate는 26/48 = 54.2%로 기록했다. 20D는 2026-04-27 이후 기준일 대부분이 아직 대기다.

## [2026-05-23 07:12 Asia/Seoul] simulation | 보강 데이터 기반 과거 추천 v2 재시뮬레이션 및 회고

- 이전 배치 회고를 바탕으로 추가 수집해야 할 데이터와 소스를 정리했다.
- 추가 데이터는 Alpaca MCP `get_news`, `get_stock_bars`, SPY/QQQ/SMH 벤치마크, 후보군 누락 점검, 향후 IR/SEC/실적 캘린더와 quote spread로 구분했다.
- 지난 배치에서 빠졌던 PLTR daily bar를 Alpaca MCP로 보강했지만, 해당 기간 상대성과가 약해 v2 추천에는 승격하지 않았다.
- v2는 뉴스 촉매, 거래량/가격 돌파, 섹터 대비 상대강도, 변동성 패널티를 반영한 진단용 재시뮬레이션으로 기록했다.
- v2 5D hit rate는 47/48 = 97.9%, 평균 SPY 대비 초과수익은 +9.63%p로 계산했다.
- 단, v2는 v1 회고 후 설계한 규칙이라 과최적화 위험이 크며, 독립 기간 검증 전 정책 승격은 금지한다고 기록했다.
- 원천 기록: `wiki/raw/sources/2026-05-23-historical-batch-v2-supplemental-sources.md`.
- 추천 배치: `wiki/simulations/2026-04-23-to-2026-05-08-historical-decision-batch-v2.md`.
- 회고 배치: `wiki/reviews/decisions/2026-04-23-to-2026-05-08-historical-review-batch-v2.md`.

## [2026-05-23 07:48 Asia/Seoul] validation | v2 규칙 별도 검증셋 평가

- 사용자 지적대로 v2 재시뮬레이션은 학습셋과 검증셋이 같아 과적합 가능성이 크다고 판단했다.
- v2 규칙을 설계에 사용하지 않은 2026-05-11~2026-05-15 구간에 적용해 out-of-sample 검증을 수행했다.
- Alpaca MCP `get_stock_bars`로 2026-05-04~2026-05-23 가격/거래량을 조회했고, `get_news`로 2026-05-09~2026-05-16 뉴스 촉매를 확인했다.
- 검증 추천 15개 중 9개가 5D 기준 SPY를 초과해 hit rate는 60.0%였다.
- 평균 5D SPY 대비 초과수익은 +0.73%p로, v2 학습셋의 +9.63%p보다 크게 낮았다.
- 결론: 뉴스 촉매+상대강도 보강 데이터는 후보 발굴에는 유용하지만, 매수 결정 신호로 승격하기에는 부족하다.
- 정책에는 과열/차익실현/매크로 악화 필터 필요성을 추가했다.
- 원천 기록: `wiki/raw/sources/2026-05-23-historical-validation-2026-05-11-to-2026-05-15-sources.md`.
- 검증 추천: `wiki/simulations/2026-05-11-to-2026-05-15-historical-validation-decision.md`.
- 검증 회고: `wiki/reviews/decisions/2026-05-11-to-2026-05-15-historical-validation-review.md`.

## [2026-05-23 08:20 Asia/Seoul] harness | 뉴스/이벤트 보강 MCP 연결

- 주식 분석의 뉴스/이벤트 보강을 위해 Codex MCP 서버를 추가 등록했다.
- 등록 서버: `sec-edgar`, `yahoo-finance`, `alpha-vantage`, `fred`, `firecrawl`.
- `sec-edgar`와 `yahoo-finance`는 별도 키 없이 실행 가능한 보강 MCP로 설정했다.
- `alpha-vantage`, `fred`, `firecrawl`은 각각 `ALPHA_VANTAGE_API_KEY`, `FRED_API_KEY`, `FIRECRAWL_API_KEY`가 `.env`에 있을 때 실행되도록 래퍼를 만들었다.
- 새 래퍼: `scripts/mcp-sec-edgar.sh`, `scripts/mcp-yahoo-finance.sh`, `scripts/mcp-alpha-vantage.sh`, `scripts/mcp-fred.sh`, `scripts/mcp-firecrawl.sh`.
- `harness/mcp-source-map.md`를 추가하고, daily/research/historical workflow와 agent guide가 이 MCP들을 활용하도록 문서화했다.
- API 키 값은 출력하거나 커밋하지 않았다.

## [2026-05-23 08:45 Asia/Seoul] validation | MCP 보강 데이터 기반 검증과 정책 수립

- 사용자가 `.env`에 보강 MCP 키를 추가한 뒤, 키 값은 출력하지 않고 존재 여부만 확인했다.
- Alpha Vantage MCP가 정상 초기화되는 것을 확인했고, `EARNINGS`, `NEWS_SENTIMENT`, `TREASURY_YIELD` 도구 스키마를 확인했다.
- Alpha Vantage `EARNINGS`로 AMD 2026-05-05 실적 beat를 확인했다: EPS 1.37, 추정 1.29, surprise +6.20%, post-market.
- Alpha Vantage `NEWS_SENTIMENT`는 2026-05-09~2026-05-16 AMD/NVDA/IONQ/NOK/TSLA 조회에서 0건을 반환해 데이터 공백으로 기록했다.
- Alpha Vantage `TREASURY_YIELD`는 무료 키 rate limit 안내가 반환되어 이번 검증에서는 미사용으로 기록했다.
- SEC EDGAR MCP는 `SEC_EDGAR_USER_AGENT`가 없어 실행 불가였고, FRED MCP는 유효한 JSON-RPC 응답을 반환하지 않아 데이터 공백으로 기록했다.
- MCP 보강 정책을 2026-05-11~2026-05-15 검증셋에 적용한 결과 5D hit rate는 12/15 = 80.0%, 평균 SPY 대비 초과수익은 +3.35%p였다.
- 기존 검증셋 9/15 = 60.0%, +0.73%p보다 개선됐지만 표본이 작아 `검증 중` 정책으로만 반영했다.
- 정책 후보: `earnings-beat-overextension-filter`, `mcp-confirmation-gap-penalty`, `post-catalyst-reentry`.
- 원천 기록: `wiki/raw/sources/2026-05-23-mcp-enhanced-validation-sources.md`.
- 검증 추천: `wiki/simulations/2026-05-11-to-2026-05-15-mcp-enhanced-validation-decision.md`.
- 검증 회고: `wiki/reviews/decisions/2026-05-11-to-2026-05-15-mcp-enhanced-validation-review.md`.

## [2026-05-23 09:30 Asia/Seoul] validation | 최근 7일 과거 추천 시뮬레이션 및 1D 회고

- 사용자 요청에 따라 2026-05-16~2026-05-22 최근 7일 범위의 과거 추천 시뮬레이션을 수행했다.
- 미국 거래일 기준 2026-05-18~2026-05-21 추천은 다음 거래일 종가가 있어 1D 회고를 완료했고, 2026-05-22 추천은 회고 대기로 남겼다.
- Alpaca MCP `get_stock_bars`로 2026-05-01~2026-05-22 일봉을 확인했고, `get_news`로 2026-05-16~2026-05-22 후보 종목 뉴스를 확인했다.
- 2026-05-21 양자컴퓨팅 정부 지원 뉴스, NVDA 실적/AI 수요 뉴스, AMD advanced packaging 뉴스, NOK AI Networking Innovation Lab 뉴스를 촉매로 기록했다.
- 검증 가능한 12개 추천의 1D hit rate는 12/12 = 100.0%, 평균 SPY 대비 초과수익은 +5.63%p였다.
- 단, 성과가 2026-05-21 이벤트에 집중되어 있어 정책 승격이 아니라 `1d-event-catalyst-confirmation` 검증 중 가설로만 반영했다.
- 2026-05-22 dry-run 주문 계획은 `scripts/check-risk-policy.py` 검증을 통과했다.
- 원천 기록: `wiki/raw/sources/2026-05-23-recent-7d-historical-validation-sources.md`.
- 검증 추천: `wiki/simulations/2026-05-18-to-2026-05-22-recent-7d-historical-decision.md`.
- 검증 회고: `wiki/reviews/decisions/2026-05-18-to-2026-05-22-recent-7d-historical-review.md`.

## [2026-05-23 10:15 Asia/Seoul] report | 투자·시뮬레이션 종합 인사이트 보고서 작성

- 실제 2026-05-22 paper 매수 이력, 현재 포트폴리오, 과거 시점 추천 시뮬레이션, 독립 검증, MCP 보강 검증, 최근 7일 검증을 한 보고서로 정리했다.
- 핵심 결론은 촉매+상대강도 신호는 후보 발굴에 유용하지만 과열, 데이터 공백, 이벤트 반납 위험을 감점해야 한다는 것이다.
- v2의 97.9% 성과는 과최적화 위험으로 해석하고, MCP 보강 80.0%와 최근 7일 1D 100.0% 결과는 모두 `검증 중` 가설로만 정리했다.
- 보고서: `wiki/reports/2026-05-23-investment-simulation-insight-report.md`.

## [2026-05-23 10:55 Asia/Seoul] analysis | 뉴스와 주가 반응 선후관계 이벤트 스터디

- 사용자 요청에 따라 뉴스보다 실제 주가 변화가 빠른지 느린지 파악하기 위한 이벤트 스터디를 수행했다.
- Alpaca MCP `get_stock_bars`로 2026-04-20~2026-05-22 일봉을 확인했고, `get_news`로 2026-05-01~2026-05-22 후보 종목 뉴스를 확인했다.
- AMD 실적 beat, RGTI/QBTS/IONQ 양자컴퓨팅 정부 지원 뉴스, NOK AI Networking Innovation Lab, NVDA 실적/AI 수요 뉴스, UNH 목표가 상향 등을 대표 이벤트로 분류했다.
- 결론: 실적 surprise는 뉴스 후 1D 반응이 빠르고, 정책/테마 뉴스는 당일 동행과 다음날 follow-through가 나타날 수 있으며, NVDA 같은 대형 인기주는 좋은 뉴스보다 기대 선반영/차익실현이 먼저 작동할 수 있다.
- 분석 문서: `wiki/analyses/2026-05-23-news-price-lead-lag-simulation.md`.

## [2026-05-23 11:05 Asia/Seoul] policy | 뉴스-가격 선후관계 정책 반영

- 뉴스-가격 선후관계 분석에서 나온 정책 제안과 하네스 반영 후보를 실제 추천 정책과 워크플로우에 연결했다.
- `wiki/policies/recommendation-policy.md`에 `news-price-lead-lag`, `sell-the-news-risk`, `theme-news-follow-through`, `earnings-fast-reaction` 신호를 추가했다.
- Daily workflow의 Trend Agent가 뉴스 전 3D/5D 수익률, 뉴스 당일 반응, 후속 반응 가능성을 반영하도록 수정했다.
- Research workflow가 종목 페이지에 lead/lag 라벨과 뉴스 전후 가격 반응을 기록하도록 수정했다.
- Historical decision workflow는 기준 시점 이후 가격을 추천 문서에 넣지 않고 회고 문서에서만 post-news 성과를 계산하도록 명시했다.

## [2026-05-23 16:20 Asia/Seoul] analysis | 3월/4월 시간별 단타 정책 시뮬레이션

- 사용자 요청에 따라 2026년 3월 특정일 3개를 선정해 시간별 단타 정책을 검토하고, 2026년 4월 특정일로 검증했다.
- 3월 학습일은 QQQ open-to-close 절대수익률 상위 3일인 2026-03-09, 2026-03-31, 2026-03-30으로 선정했다.
- 4월 검증일은 2026년 4월 QQQ open-to-close 절대수익률 상위일인 2026-04-02로 선정했다.
- Alpaca Market Data API IEX feed의 `1Day`, `1Hour` bars와 Alpaca News API의 해당일 뉴스 맥락을 원천으로 기록했다.
- 검토 정책 `intraday-rs-breakout-v0`는 QQQ 초기 risk-on, 종목 상대강도, 돌파 유지, +2% take, -1% stop, 당일 청산 구조다.
- 3월 학습 표본 결과는 3개 거래, +$591.81였고, 2026-03-31과 2026-03-30은 정책상 무거래였다.
- 4월 검증일 2026-04-02 결과는 3개 거래, +$83.84였다. LRCX stop, AMD take, TSM EOD 소폭 손실로 기록했다.
- 정책에는 자동 주문 원칙이 아닌 `검증 중` 단타 후보로 반영했다.
- 원천 기록: `wiki/raw/sources/2026-05-23-march-april-intraday-scalping-sources.md`.
- 분석 문서: `wiki/analyses/2026-05-23-march-april-intraday-scalping-simulation.md`.

## [2026-05-23 17:25 Asia/Seoul] analysis | 다른 일정으로 시간별 단타 정책 재검증

- 사용자 요청에 따라 앞선 표본과 다른 일정으로 `intraday-rs-breakout-v0`를 다시 검증했다.
- 3월 학습일은 기존 2026-03-09, 2026-03-31, 2026-03-30을 제외한 QQQ open-to-close 절대수익률 상위 3일인 2026-03-26, 2026-03-02, 2026-03-20으로 선정했다.
- 4월 검증일은 기존 2026-04-02를 제외한 4월 QQQ open-to-close 절대수익률 상위일인 2026-04-14로 선정했다.
- 2026-03-26과 2026-03-20은 neutral/risk-off로 무거래, 2026-03-02는 PLTR/NVDA/TSLA 3개 거래로 +$33.50이었다.
- 2026-04-14 검증은 TSLA/NVDA 2개 거래로 +$185.00이었다.
- 두 차례 표본 합산 결과는 8거래일, 11거래, 가상 P/L +$894.15, trade hit rate 72.7%로 기록했다.
- 단, 이번 재검증에서는 take profit 도달 거래가 없어 EOD 수익과 무거래 필터 기여가 컸다. 정책은 계속 `검증 중`으로 유지했다.
- 원천 기록: `wiki/raw/sources/2026-05-23-march-april-intraday-scalping-alt-sources.md`.
- 분석 문서: `wiki/analyses/2026-05-23-march-april-intraday-scalping-alt-simulation.md`.

## [2026-05-23 17:55 Asia/Seoul] analysis | 2월~5월 임의 일자 시간별 단타 5회 반복 검증

- 사용자 요청에 따라 2026년 2월부터 2026년 5월 22일까지 임의 일자를 선정해 `intraday-rs-breakout-v0`를 5번 더 반복 검증했다.
- 무작위 시드는 `20260523`으로 고정했고, 앞선 두 차례 시뮬레이션에 사용한 날짜는 제외했다.
- 각 반복은 3개 학습일과 1개 검증일로 구성했다.
- 5회 반복 합계는 20거래일, 23거래, 이익 거래 11개, hit rate 47.8%, 가상 P/L +$515.86이었다.
- 검증일만 분리하면 5거래일, 7거래, 이익 거래 5개, hit rate 71.4%, 가상 P/L +$551.68이었다.
- 기존 1차/2차와 합산하면 28거래일, 34거래, hit rate 55.9%, 가상 P/L +$1,410.01이었다.
- 총손익은 플러스지만 2026-04-01, 2026-02-20, 2026-04-29에서 개장 초반 돌파 후 동시 stop 위험이 확인되어 자동 주문 부적합으로 정책을 강등했다.
- 원천 기록: `wiki/raw/sources/2026-05-23-random-intraday-scalping-5x-sources.md`.
- 분석 문서: `wiki/analyses/2026-05-23-random-intraday-scalping-5x-simulation.md`.

## [2026-05-23 18:25 Asia/Seoul] analysis | 단타 정책 1시간봉 timestamp 보정 및 분봉 검증

- 사용자 요청의 다음 단계로 `intraday-rs-breakout-v0`의 1시간봉 timestamp 해석을 보정하고 1분봉으로 stop/take 순서를 검증했다.
- Alpaca `1Hour` bar timestamp는 시작 시각이므로, `10:00` hour bar close 기반 신호는 11:00 ET 이후에만 실행 가능하다고 정정했다.
- 기존 28개 표본일에 대해 `1Min` bars로 진입 이후 stop/take/EOD 순서를 재계산했다.
- v0 보정 버전은 28거래일, active 14일, 34거래, hit rate 55.9%, stop 12, take 11, 가상 P/L +$1,410.00이었다.
- 12:00 confirmation variants는 모두 v0보다 총손익이 낮았다: top3 +$556.63, top2 +$488.35, top1 -$175.96, top2/take 1.5% +$444.87.
- 결론: v0는 플러스 기대값 후보로 남지만, 자동 주문에는 부적합하며 주문 없는 실시간 paper dry-run으로 11:00 ET 신호를 기록하는 단계가 필요하다.
- 원천 기록: `wiki/raw/sources/2026-05-23-intraday-scalping-minute-validation-sources.md`.
- 분석 문서: `wiki/analyses/2026-05-23-intraday-scalping-minute-validation.md`.

## [2026-05-23 18:55 Asia/Seoul] analysis | 단타 성과 개선용 추가 필터 검증

- 사용자 요청에 따라 단타 성과를 올리기 위한 추가 정보와 분석법을 파악하고 같은 28개 표본에 적용했다.
- 추가 검토 정보는 QQQ VWAP, SMH VWAP, 종목 VWAP, 반도체 breadth, opening range breakout, gap filter, 실시간 bid/ask 필요성이다.
- baseline 11:00 top3는 34거래, hit rate 55.9%, stop 12, take 11, 가상 P/L +$1,425.06으로 계산했다. 진입가는 11:00 이후 첫 1분봉 open 기준이라 이전 minute validation의 hour close 기준 +$1,410.00과 소폭 다르다.
- QQQ+SMH+종목 VWAP 필터는 33거래, hit rate 57.6%, P/L +$1,524.37로 개선됐다.
- 반도체 breadth 4개 이상 + QQQ/SMH/종목 VWAP 필터는 27거래, hit rate 59.3%, stop 9, take 11, P/L +$1,547.25로 총손익과 평균 거래 손익이 가장 좋았다.
- 같은 필터에서 top2만 쓰면 18거래, hit rate 66.7%, P/L +$1,395.55로 총손익은 낮지만 거래 품질은 가장 좋았다.
- opening range breakout 단독, gap filter, take +1.5%는 개선 효과가 약하거나 손익을 낮췄다.
- 새 후보 정책 `intraday-rs-breadth-vwap-v1`을 paper-only manual candidate로 추가했다.
- 원천 기록: `wiki/raw/sources/2026-05-23-intraday-scalping-feature-filter-sources.md`.
- 분석 문서: `wiki/analyses/2026-05-23-intraday-scalping-feature-filter-simulation.md`.

## [2026-05-23 18:56 Asia/Seoul] workflow | 단타 실시간 paper dry-run 운영안 추가

- 다음 미국 정규장부터 사용할 `harness/workflows/intraday-paper-dry-run.md`를 추가했다.
- 운영안은 `intraday-rs-breakout-v0`와 `intraday-rs-breadth-vwap-v1`를 11:00 ET 이후 병렬 기록하며, 주문 제출/취소/수정/포지션 변경을 금지한다.
- 11:00 ET 신호 기록 포맷, v0/v1 비교 항목, bid/ask spread와 fill 가능성 기록 항목을 정의했다.
- 캡처된 1분봉 JSON만 읽는 `scripts/evaluate-intraday-dry-run.py` 초안을 추가했다. 이 스크립트는 Alpaca API를 호출하지 않고 `orders_submitted=0` 관찰 결과만 생성한다.
- `wiki/policies/recommendation-policy.md`, `wiki/index.md`, `harness/README.md`에 dry-run 운영 연결을 반영했다.

## [2026-05-23 18:57 Asia/Seoul] docs | 분석 문서 지표 설명 규칙 추가

- 사용자 의도를 반영해 분석 결과 문서에는 별도 답변이 아니라 문서 하단에 `지표 설명` 섹션을 함께 작성하도록 규칙을 추가했다.
- `harness/workflows/daily.md`, `harness/workflows/research.md`, `harness/workflows/intraday-paper-dry-run.md`, `wiki/policies/recommendation-policy.md`를 갱신했다.
- 실제 주문, 취소, 포지션 변경은 없었다.

## [2026-05-23 19:25 Asia/Seoul] analysis | 미검토 단타 정책 후보 학습/검증

- 사용자 요청에 따라 기존 v0/v1에서 덜 다룬 VWAP 평균회귀, 장중 반전, 거래량 확인 모멘텀 후보를 조사하고 시뮬레이션했다.
- 외부 조사로 ORB, VWAP 평균회귀, intraday momentum/reversal, 거래비용 관련 자료를 확인했다.
- 학습 표본은 2026-03-03, 2026-03-09, 2026-03-10, 2026-03-19, 2026-03-25다.
- 검증 표본은 2026-04-01, 2026-04-09, 2026-04-10, 2026-04-14, 2026-04-17이다.
- `pullback-vwap-reclaim-morning`은 학습 6거래 hit 66.7%, +$308.80, 검증 10거래 hit 60.0%, +$222.57로 플러스였다.
- 2026-03-02~2026-05-22 59거래일 보조 스캔에서도 `pullback-vwap-reclaim-morning`은 38거래, hit 55.3%, +$822.98이었다.
- `midday-vwap-reversal`은 플러스 가능성은 있으나 표본과 안정성이 부족해 보류했다.
- `volume-confirmed-momentum`은 59거래일 스캔에서 6거래 모두 실패해 폐기 후보로 기록했다.
- 새 보조 후보 `intraday-pullback-vwap-reclaim-v0`를 `paper-only secondary candidate`로 정책에 반영했다. 자동 주문은 금지한다.
- 원천 기록: `wiki/raw/sources/2026-05-23-intraday-policy-candidates-sources.md`.
- 계산 데이터: `wiki/raw/sources/2026-05-23-intraday-policy-candidates-simulation-data.json`.
- 분석 문서: `wiki/analyses/2026-05-23-intraday-policy-candidates-simulation.md`.
- 실제 주문, 취소, 포지션 변경은 없었다.

## [2026-05-23 20:20 Asia/Seoul] analysis | 장타 정책 2~3월 학습 및 4~5월 검증

- 사용자 요청에 따라 장타 투자 목적의 종목 선별 정책을 2026년 2~3월 13개 기준일로 학습하고, 2026년 4~5월 10개 기준일로 검증했다.
- Alpaca Market Data API IEX `1Day` bars를 read-only로 조회했고 실제 주문/취소/포지션 변경은 없었다.
- 테스트 variants는 `balanced_top3`, `quality_top5`, `momentum_top3`다.
- 학습 결과 `quality_top5`는 65개 추천, 20D 절대 hit 37/65, SPY hit 42/65, 평균 20D +7.18%, 평균 SPY 대비 +6.77%p, 평균 불리 이동 -8.25%였다.
- 검증 결과 `quality_top5`는 50개 추천 중 20D 완료 30개, 20D 절대 hit 27/30, SPY hit 24/30, 평균 20D +25.62%, 평균 SPY 대비 +18.64%p였다.
- `balanced_top3`와 `momentum_top3`는 검증 수익률이 더 높았지만 집중도와 학습 구간 불리 이동을 고려해 장타 기본 후보는 `quality_top5`로 판단했다.
- 새 후보 정책 `long-term-quality-momentum-v0`를 `paper-only long-term candidate`로 정책에 반영했다.
- 5월 기준일 일부는 20D 결과가 아직 없으므로 5D/10D 보조값으로만 기록했다.
- 원천 기록: `wiki/raw/sources/2026-05-23-long-term-feb-mar-apr-may-sources.md`.
- 계산 데이터: `wiki/raw/sources/2026-05-23-long-term-feb-mar-apr-may-simulation-data.json`.
- 분석 문서: `wiki/analyses/2026-05-23-long-term-feb-mar-apr-may-simulation.md`.

## [2026-05-24 09:45 Asia/Seoul] workflow | Request.md 하네스 검증 레이어 반영

- `Request.md`의 개선 제안 중 리스크 정책 단일 소스화, schema 검증, 구조화된 risk-check 결과, 테스트/CI, MCP 설정 정합성, run manifest, leakage checker를 우선 반영했다.
- `harness/risk-policy.yaml`을 추가하고 `scripts/check-risk-policy.py`가 YAML 정책과 `harness/order-plan.schema.json`을 함께 검증하도록 수정했다.
- 신규 order plan은 `schema_version`, `risk_policy_version`, `recommendation_policy_sha`, `created_at`, root/per-order `source_refs`, `quote_captured_at`, `asset_checked_at`을 포함하도록 템플릿과 워크플로우를 갱신했다.
- `scripts/check-risk-policy.py --json` 출력, non-finite number 거부, bool qty 거부, submit stale quote error/dry-run stale quote warning, same-run sell proceeds 의존 금지를 추가했다.
- `scripts/check-leakage.py`, `harness/run-manifest.schema.json`, `harness/templates/run-manifest.json`, `wiki/runs/README.md`, 단위 테스트, CI, pre-commit 설정을 추가했다.
- `.vscode/mcp.json`과 `.env.example`을 보강 MCP 기준에 맞춰 갱신했고, `scripts/alpaca-mcp.sh`는 `ALPACA_PAPER_TRADE=true`가 아니면 중단하도록 강화했다.
- 검증: `python3 -m unittest discover -s tests` 17개 테스트 통과, `python3 scripts/check-risk-policy.py --json harness/examples/order-plan.example.json`, `python3 -m py_compile ...`, `git diff --check` 통과. 로컬 `ruff` 모듈은 미설치라 실행하지 못했고 CI에서 설치 후 실행하도록 구성했다.
- 실제 주문, 취소, 포지션 변경은 없었다.

## [2026-05-24 10:32 Asia/Seoul] analysis | 단타/장타 현재 정책 2~3월 시뮬레이션 및 4~5월 검증

- 사용자 요청에 따라 현재 단타 정책 `intraday-rs-breakout-v0`, `intraday-rs-breadth-vwap-v1`과 장타 정책 `long-term-quality-momentum-v0`를 재점검했다.
- Alpaca MCP `get_stock_bars`로 2026년 2~3월 QQQ/SMH 일봉 regime을 확인했고, 단타 계산은 read-only Alpaca IEX 1분봉으로 수행했다.
- 단타 학습 날짜는 2026-02-03, 02-12, 02-20, 03-03, 03-09, 03-19, 03-26, 03-31이다. 4~5월 검증 날짜는 2026-04-01, 04-09, 04-14, 04-17, 04-29, 05-04, 05-08, 05-13, 05-21, 05-22다.
- 단타 2~3월 학습은 v1 top3 기준 8일 중 active 2일, 6거래, hit 50.0%, 가상 P/L +$300.00이었다.
- 단타 4~5월 검증은 v1 top3 기준 active 1일, 3거래 모두 stop, 가상 P/L -$300.00이었다. v0 top3도 9거래 중 7 stop, -$724.07로 자동 주문 부적합을 강화했다.
- 장타 `quality_top5`는 2~3월 65개 추천 평균 20D +7.18%, SPY 초과 +6.77%p였고, 4~5월 검증 완료 30개 추천 평균 20D +25.62%, SPY 초과 +18.64%p였다.
- 정책 결론: 단타 v1은 관찰 전용으로 낮추고 11:05~11:15 후속 유지, bid/ask spread, fill 가능성, 뉴스 timestamp를 추가한다. 장타 `quality_top5`는 유지하되 실적/filing/valuation/theme exposure 보강 전 자동 주문으로 승격하지 않는다.
- 원천 기록: `wiki/raw/sources/2026-05-24-short-long-policy-simulation-sources.md`.
- 계산 데이터: `wiki/raw/sources/2026-05-24-short-long-policy-simulation-data.json`.
- 분석 문서: `wiki/analyses/2026-05-24-short-long-policy-feb-mar-apr-may-review.md`.
- 실제 주문, 취소, 포지션 변경은 없었다.

## [2026-05-24 11:11 Asia/Seoul] analysis | 2026-05-08 과거 추천 표본 MCP 보강 비교

- 사용자 요청에 따라 이전 시뮬레이션 중 [[2026-04-23-to-2026-05-08-historical-decision-batch-v2]]의 `2026-05-08` 추천 표본을 선택했다.
- 원래 추천은 `NVDA, IONQ, UNH`였고, 비교 후보로 `AMD, TSLA`를 함께 확인했다.
- Alpaca MCP 가격/뉴스, SEC EDGAR MCP filings, Alpha Vantage MCP earnings/news sentiment, Firecrawl MCP 공식 IR 검색, Yahoo Finance MCP 보조 정보를 수집했다.
- MCP 보강 후에도 추천 세트는 바뀌지 않았지만, NVDA/IONQ/UNH 추천 근거와 AMD/TSLA 제외 근거가 더 명확해졌다.
- 특히 AMD는 2026-05-05 실적 beat와 bullish news에도 2026-05-01→05-08 +26.22% 급등 후 2026-05-08→05-15 -6.83%로 되돌림이 확인되어 `post-earnings-overheat-gate` 후보 규칙을 기록했다.
- FRED MCP는 도구 목록을 반환하지 않아 매크로 보강 공백으로 기록했다.
- 원천 기록: `wiki/raw/sources/2026-05-24-mcp-comparison-2026-05-08-sources.md`.
- 분석 문서: `wiki/analyses/2026-05-24-mcp-comparison-2026-05-08-historical-simulation.md`.
- 실제 주문, 취소, 포지션 변경은 없었다.

## [2026-05-24 11:25 Asia/Seoul] analysis | 남은 시뮬레이션 이력 MCP 보강 재감사

- 사용자 요청에 따라 2026-05-08 표본 외 남은 과거 추천, 최근 7일, 단타, 장타 정책 시뮬레이션 이력을 MCP 보강 정보로 재검토했다.
- Alpaca MCP 일봉/뉴스, Alpha Vantage earnings/news sentiment, SEC EDGAR filings, Firecrawl 공식 IR/뉴스룸 검색을 사용했다.
- 2026-05-11~05-15 MCP 보강 검증은 SEC/IR 확인으로 신뢰도가 올라갔고, `earnings-beat-overextension-filter`와 `mcp-confirmation-gap-penalty` 결론을 유지했다.
- 2026-05-18~05-22 최근 7일 성과는 RGTI/QBTS/NOK 이벤트가 SEC/IR로 확인됐지만, 성과 집중과 고변동 테마 리스크 때문에 정책 승격 보류 결론을 유지했다.
- 단타 정책은 MCP 보강이 과거 분봉 손익을 바꾸지 않으며, 뉴스 timestamp, filing acceptance time, bid/ask spread, fill 가능성 없이 자동 주문으로 올리지 않는 결론을 강화했다.
- 장타 `long-term-quality-momentum-v0`는 유지하되, 실적/filing 확인, theme exposure cap, staged entry 보강 전 자동 주문 승격은 보류했다.
- Alpha broad `NEWS_SENTIMENT` 0건과 Firecrawl domain-restricted 0건은 정보 부재가 아니라 provider/query gap일 수 있어 fallback 원칙을 정책에 추가했다.
- FRED MCP tools/list는 응답 지연으로 중단했고 macro MCP operational gap으로 기록했다.
- 원천 기록: `wiki/raw/sources/2026-05-24-mcp-policy-history-reaudit-sources.md`.
- 분석 문서: `wiki/analyses/2026-05-24-mcp-policy-history-reaudit.md`.
- 정책 문서: `wiki/policies/recommendation-policy.md`.
- 실제 주문, 취소, 포지션 변경은 없었다.

## [2026-05-24 12:27 Asia/Seoul] daily | 현재 기준 no-submit 종목 추천

- 사용자 요청 `현재 기준으로 주식 종목 추천해줘`를 daily no-submit 추천 run으로 해석했다. 주문/매수/실행 키워드가 없어 실제 주문은 제출하지 않았다.
- `.env`에서 `ALPACA_PAPER_TRADE=true`를 확인했고, Alpaca MCP로 계좌, 시장 시계, 포지션, 미체결 주문, calendar, 가격 bars/snapshot/news, asset tradability를 확인했다.
- Alpaca clock 기준 시장은 닫혀 있었고 다음 정규장 개장은 2026-05-26 09:30 ET였다.
- 최종 추천 순위는 UNH, LRCX, AMD, NVDA, TSM이다. NOK/IONQ/RGTI/QBTS는 강한 모멘텀에도 단기 과열과 valuation/short-interest 리스크로 신규 추격을 보류했다.
- `wiki/portfolio/order-plans/2026-05-24-current-recommendations.json` dry-run 후보를 생성했고 risk check는 PASS였다. Buy notional 16193.14 USD, post-order cash 27837.44 USD, post-order invested 72581.23 USD다.
- 모든 후보 quote가 장 마감 후 stale 상태라 dry-run 경고를 기록했다. Submit-mode 주문 가능 상태가 아니며 실제 주문, 취소, 포지션 변경은 없었다.
- 원천 기록: `wiki/raw/sources/2026-05-24-current-recommendation-sources.md`.
- 리포트: `wiki/reports/daily/2026-05-24.md`.
- run manifest: `wiki/runs/2026-05-24-1227-current-recommendations.json`.

## [2026-05-24 13:04 Asia/Seoul] analysis | 최근 6개월 3시간 단위 독립 정책 시뮬레이션

- 사용자 요청에 따라 2025-11-24~2026-05-22 최근 6개월 124거래일을 일별 3시간 구간으로 추출하고 독립 시뮬레이션했다.
- `.env`에서 `ALPACA_PAPER_TRADE=true`를 확인했고, Alpaca MCP `get_clock`, `get_watchlists`, `get_all_positions`, `get_calendar`, `get_asset`, `get_stock_bars` read-only 도구만 사용했다.
- watchlist가 비어 있어 현재 paper 보유 종목과 기존 정책 후보, SPY/QQQ/SMH 벤치마크를 합친 16개 심볼을 universe로 사용했다.
- 긴 기간 `get_stock_bars` 요청은 `next_page_token`이 생겼지만 page token 인자가 MCP 스키마에 없어, 14일 청크로 재조회해 누락 없이 5,920개 3시간 window와 1,984개 정규장 일봉을 생성했다.
- 단타형 3시간 정책은 `3h-afternoon-continuation-top2`가 90거래, hit rate 61.1%, 가상 P/L +$1,530.61로 가장 좋았지만, IEX 30분봉·spread·fill 공백 때문에 자동 주문 후보로 승격하지 않았다.
- 장타형 `daily-3h-theme-capped-top5`는 320개 완료 추천에서 214/320 SPY 초과 hit, 평균 20D SPY 초과 +7.82%p였다. theme cap은 장타 후보 보강 근거로 추가했지만 실적/filing/valuation 확인 전 자동 주문으로 승격하지 않는다.
- 원천 기록: `wiki/raw/sources/2026-05-24-six-month-3h-simulation-sources.md`.
- 계산 데이터: `wiki/raw/sources/2026-05-24-six-month-3h-simulation-data.json`.
- 분석 문서: `wiki/analyses/2026-05-24-six-month-3h-independent-policy-review.md`.
- run manifest: `wiki/runs/2026-05-24-3h-six-month-policy-review.json`.
- 정책 문서: `wiki/policies/recommendation-policy.md`.
- 실제 주문, 취소, 포지션 변경은 없었다.
