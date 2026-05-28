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
- 분석 문서: `wiki/backtests/2026-05-23-news-price-lead-lag-simulation.md`.

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
- 분석 문서: `wiki/backtests/2026-05-23-march-april-intraday-scalping-simulation.md`.

## [2026-05-23 17:25 Asia/Seoul] analysis | 다른 일정으로 시간별 단타 정책 재검증

- 사용자 요청에 따라 앞선 표본과 다른 일정으로 `intraday-rs-breakout-v0`를 다시 검증했다.
- 3월 학습일은 기존 2026-03-09, 2026-03-31, 2026-03-30을 제외한 QQQ open-to-close 절대수익률 상위 3일인 2026-03-26, 2026-03-02, 2026-03-20으로 선정했다.
- 4월 검증일은 기존 2026-04-02를 제외한 4월 QQQ open-to-close 절대수익률 상위일인 2026-04-14로 선정했다.
- 2026-03-26과 2026-03-20은 neutral/risk-off로 무거래, 2026-03-02는 PLTR/NVDA/TSLA 3개 거래로 +$33.50이었다.
- 2026-04-14 검증은 TSLA/NVDA 2개 거래로 +$185.00이었다.
- 두 차례 표본 합산 결과는 8거래일, 11거래, 가상 P/L +$894.15, trade hit rate 72.7%로 기록했다.
- 단, 이번 재검증에서는 take profit 도달 거래가 없어 EOD 수익과 무거래 필터 기여가 컸다. 정책은 계속 `검증 중`으로 유지했다.
- 원천 기록: `wiki/raw/sources/2026-05-23-march-april-intraday-scalping-alt-sources.md`.
- 분석 문서: `wiki/backtests/2026-05-23-march-april-intraday-scalping-alt-simulation.md`.

## [2026-05-23 17:55 Asia/Seoul] analysis | 2월~5월 임의 일자 시간별 단타 5회 반복 검증

- 사용자 요청에 따라 2026년 2월부터 2026년 5월 22일까지 임의 일자를 선정해 `intraday-rs-breakout-v0`를 5번 더 반복 검증했다.
- 무작위 시드는 `20260523`으로 고정했고, 앞선 두 차례 시뮬레이션에 사용한 날짜는 제외했다.
- 각 반복은 3개 학습일과 1개 검증일로 구성했다.
- 5회 반복 합계는 20거래일, 23거래, 이익 거래 11개, hit rate 47.8%, 가상 P/L +$515.86이었다.
- 검증일만 분리하면 5거래일, 7거래, 이익 거래 5개, hit rate 71.4%, 가상 P/L +$551.68이었다.
- 기존 1차/2차와 합산하면 28거래일, 34거래, hit rate 55.9%, 가상 P/L +$1,410.01이었다.
- 총손익은 플러스지만 2026-04-01, 2026-02-20, 2026-04-29에서 개장 초반 돌파 후 동시 stop 위험이 확인되어 자동 주문 부적합으로 정책을 강등했다.
- 원천 기록: `wiki/raw/sources/2026-05-23-random-intraday-scalping-5x-sources.md`.
- 분석 문서: `wiki/backtests/2026-05-23-random-intraday-scalping-5x-simulation.md`.

## [2026-05-23 18:25 Asia/Seoul] analysis | 단타 정책 1시간봉 timestamp 보정 및 분봉 검증

- 사용자 요청의 다음 단계로 `intraday-rs-breakout-v0`의 1시간봉 timestamp 해석을 보정하고 1분봉으로 stop/take 순서를 검증했다.
- Alpaca `1Hour` bar timestamp는 시작 시각이므로, `10:00` hour bar close 기반 신호는 11:00 ET 이후에만 실행 가능하다고 정정했다.
- 기존 28개 표본일에 대해 `1Min` bars로 진입 이후 stop/take/EOD 순서를 재계산했다.
- v0 보정 버전은 28거래일, active 14일, 34거래, hit rate 55.9%, stop 12, take 11, 가상 P/L +$1,410.00이었다.
- 12:00 confirmation variants는 모두 v0보다 총손익이 낮았다: top3 +$556.63, top2 +$488.35, top1 -$175.96, top2/take 1.5% +$444.87.
- 결론: v0는 플러스 기대값 후보로 남지만, 자동 주문에는 부적합하며 주문 없는 실시간 paper dry-run으로 11:00 ET 신호를 기록하는 단계가 필요하다.
- 원천 기록: `wiki/raw/sources/2026-05-23-intraday-scalping-minute-validation-sources.md`.
- 분석 문서: `wiki/backtests/2026-05-23-intraday-scalping-minute-validation.md`.

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
- 분석 문서: `wiki/backtests/2026-05-23-intraday-scalping-feature-filter-simulation.md`.

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
- 분석 문서: `wiki/backtests/2026-05-23-intraday-policy-candidates-simulation.md`.
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
- 분석 문서: `wiki/backtests/2026-05-23-long-term-feb-mar-apr-may-simulation.md`.

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
- 분석 문서: `wiki/backtests/2026-05-24-short-long-policy-feb-mar-apr-may-review.md`.
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
- 분석 문서: `wiki/backtests/2026-05-24-six-month-3h-independent-policy-review.md`.
- run manifest: `wiki/runs/2026-05-24-3h-six-month-policy-review.json`.
- 정책 문서: `wiki/policies/recommendation-policy.md`.
- 실제 주문, 취소, 포지션 변경은 없었다.

## [2026-05-24 15:22 Asia/Seoul] wiki | 백테스트 폴더 분리

- 사용자 요청에 따라 정책 시뮬레이션/백테스트 결과 전용 `wiki/backtests/`를 만들었다.
- 기존 `wiki/analyses/`에 있던 단타 정책 실험, 장타 정책 검증, news lead/lag event study, 최근 6개월 3시간 정책 검토 문서를 `wiki/backtests/`로 이동했다.
- `wiki/simulations/`는 계속 과거 특정 시점 기준 추천 문서 전용으로 유지한다. 해당 문서는 미래 가격/성과 정보를 포함하지 않는다.
- `README.md`, `wiki/index.md`, `wiki/analyses/README.md`, `wiki/simulations/README.md`, `wiki/backtests/README.md`에 폴더별 역할을 반영했다.

## [2026-05-24 15:56 Asia/Seoul] backtest | 정책 개선 후보 5개 시뮬레이션

- 사용자 요청에 따라 현재 정책을 개선하기 위해 시도할 후보 5개를 뽑고, 기존 최근 6개월 3시간/일봉 계산 데이터를 재사용해 검증했다.
- 장타 후보는 `lt-overheat-guard-theme-cap-v1`, `lt-dual-benchmark-confirm-v1`, `lt-drawdown-volatility-guard-v1`, `lt-anti-chase-staged-entry-v1` 네 가지다.
- 단타 후보는 `intraday-afternoon-followthrough-filter-v1` 한 가지이며, 성과 개선에도 IEX 30분봉·spread·fill 공백 때문에 자동 주문 금지를 유지했다.
- 장타 `lt-overheat-guard-theme-cap-v1`은 257개 완료 추천 평균 20D +10.32%, SPY 초과 +8.89%p, 검증 구간 SPY 초과 +14.54%p였다.
- `lt-dual-benchmark-confirm-v1`은 233개 완료 추천 평균 SPY 초과 +9.48%p, 검증 구간 +16.44%p였다.
- `lt-drawdown-volatility-guard-v1`은 220개 완료 추천 평균 SPY 초과 +9.44%p, 평균 불리 이동 -7.12%였다.
- `lt-anti-chase-staged-entry-v1`은 188개 완료 추천 평균 SPY 초과 +6.65%p, 검증 구간 +11.38%p였다.
- 단타 `intraday-afternoon-followthrough-filter-v1`은 78거래, hit rate 58.97%, 가상 P/L +$1,386.98였다.
- 분석 문서: `wiki/backtests/2026-05-24-policy-improvement-candidates.md`.
- 계산 데이터: `wiki/raw/sources/2026-05-24-policy-improvement-candidates-data.json`.
- run manifest: `wiki/runs/2026-05-24-policy-improvement-candidates.json`.
- 정책 문서: `wiki/policies/recommendation-policy.md`.
- 실제 주문, 취소, 포지션 변경은 없었다.

## [2026-05-24 16:14 Asia/Seoul] backtest | 확장 universe 최근 6개월 3시간 시뮬레이션

- 사용자 요청에 따라 기존 관심 종목 외 빅테크, 소프트웨어, 반도체 장비, 금융, 헬스케어, 소비재, 산업재, 에너지, 소재, 유틸리티, 고변동 성장주를 포함한 62개 심볼로 universe를 확장했다.
- Alpaca MCP `get_clock`, `get_watchlists`, `get_all_positions`, `get_calendar`, `get_asset`, `get_stock_bars` read-only 도구만 사용했다.
- 기간은 2025-11-24~2026-05-22, 거래일 124일, 3시간 구간 레코드 22,940개, 정규장 일봉 7,688개다.
- 단타 `3h-afternoon-continuation-top2`는 104거래, hit rate 61.5%, 가상 P/L +$2,285.36로 확장 universe에서도 가장 견조했다.
- 반대로 `3h-momentum-top3`는 기존 관심 종목 universe의 +$981.43에서 확장 universe -$150.28로 악화됐고, `3h-vwap-reclaim-top2`도 +$734.04에서 -$580.17로 악화됐다.
- 장타 `daily-3h-theme-capped-top5`는 320개 완료 추천 평균 20D +9.68%, SPY 초과 +7.65%p, 검증 구간 SPY 초과 +11.84%p였다.
- 확장 universe 결론은 단순 종목 수 확대가 아니라 `theme cap + overheat guard + SPY/QQQ 상대강도 확인`을 붙여 장타 후보 발굴에 쓰는 쪽이다.
- 원천 기록: `wiki/raw/sources/2026-05-24-expanded-six-month-3h-simulation-sources.md`.
- 계산 데이터: `wiki/raw/sources/2026-05-24-expanded-six-month-3h-simulation-data.json`.
- 분석 문서: `wiki/backtests/2026-05-24-expanded-six-month-3h-policy-review.md`.
- run manifest: `wiki/runs/2026-05-24-expanded-six-month-3h-policy-review.json`.
- 정책 문서: `wiki/policies/recommendation-policy.md`.
- 실제 주문, 취소, 포지션 변경은 없었다.

## [2026-05-24 16:35 Asia/Seoul] report | 2026-05-15 매입/매도 정책 결정 과정 정리

- 사용자 요청에 따라 5월 특정일로 2026-05-15를 선정해 데이터 추출부터 매입/매도 정책 결정까지의 과정을 리포트로 정리했다.
- 기준 데이터는 확장 universe 62개 심볼의 `wiki/raw/sources/2026-05-24-expanded-six-month-3h-simulation-data.json`이다.
- 결정 근거에는 2026-05-15 종가까지의 일봉, 3시간 window, SPY/QQQ/SMH 시장 레짐, 20D/40D 추세, SPY/QQQ 상대강도, drawdown, 변동성, 첫 3시간 양봉률만 사용했다.
- 사후 5거래일 결과는 의사결정 근거와 분리해 검증 섹션에만 기록했다.
- 2026-05-15 기준 정상 staged buy 후보는 NOK, UNH, GOOGL이고, AMD와 MU는 과열/불리 이동 위험 때문에 소액 staged 또는 관찰 후보로 낮췄다.
- 보유 종목 판단에서는 AMD를 trim/no full add, RGTI를 reduce/avoid add, ETN을 weak add 제외, NOK/UNH/NVDA를 hold/add candidate로 분류했다.
- 리포트: `wiki/reports/2026-05-24-may-15-decision-process-report.md`.
- 실제 주문, 취소, 포지션 변경은 없었다.

## [2026-05-24 16:45 Asia/Seoul] report | 2026-05-15 의사결정 리포트 MCP 보강

- 사용자 요청에 따라 2026-05-15 의사결정 리포트에 뉴스와 종목 관련 MCP 보강 정보를 추가했다.
- 대상 심볼은 리포트 판단에 직접 연결된 `NOK`, `UNH`, `GOOGL`, `AMD`, `MU`, `NVDA`, `RGTI`, `ETN`이다.
- Alpaca MCP `get_asset`, `get_news`, `get_corporate_action_announcements`로 tradability, 뉴스, corporate action 여부를 확인했다.
- SEC EDGAR MCP `get_company_info`, `get_recent_filings`로 회사 식별 정보와 최근 filing을 확인했고, `2026-05-15T20:00:00Z` 이전 acceptance time만 판단 근거로 분류했다.
- MCP 보강 후에도 가격 기반 후보는 유지하되, NOK는 특허/법적 뉴스 리스크, UNH/GOOGL은 filing 및 기관/내부자 관련 맥락, AMD/MU는 반도체 과열 뉴스, RGTI/ETN은 보강 근거 부족 또는 filing 리스크 때문에 staged/감점으로 정리했다.
- 원천 요약: `wiki/raw/sources/2026-05-24-may-15-mcp-context-sources.md`.
- 원자료: `wiki/raw/sources/2026-05-24-may-15-mcp-context-data.json`.
- 수집 스크립트: `scripts/collect-may15-mcp-context.py`.
- 실제 주문, 취소, 포지션 변경은 없었다.

## [2026-05-24 18:40 Asia/Seoul] hardening | 외부 리뷰 개선사항 반영

- 사용자가 공유한 ChatGPT 리뷰의 개선사항 중 즉시 코드로 반영 가능한 항목을 우선 적용했다.
- `scripts/simulate-policy-improvement-candidates.py`의 장타 백테스트를 공통 row index 순회에서 `asof_date` key 기반 정렬로 바꿨다. 종목별 거래일 누락, ADR/provider gap, corporate action 전후 row count 차이에 의한 forward return 오매칭 위험을 줄인다.
- `harness/risk-policy.yaml`에 theme/factor/speculative exposure cap과 주요 심볼 metadata를 추가했다.
- `scripts/check-risk-policy.py`가 주문 후 theme, factor, speculative exposure를 계산해 각각 35%, 50%, 12% 한도를 강제하도록 했다.
- `harness/order-plan.schema.json`에 `theme`, `factor`, `volatility_bucket`, `speculative_flag` 선택 필드를 추가했다. plan에 없으면 risk policy의 `symbol_metadata`를 fallback으로 사용한다.
- `harness/templates/raw-source.md`에 machine-readable `구조화 시그널` 표를 추가해 뉴스/공시/밸류에이션/매크로/유동성 신호를 정책학습 feature로 남길 수 있게 했다.
- `tests/test_check_risk_policy.py`에 theme exposure와 speculative exposure 실패 케이스를 추가했다.
- 실제 주문, 취소, 포지션 변경은 없었다.

## [2026-05-24 18:55 Asia/Seoul] backtest | 리뷰 개선사항 반영 후 재시뮬레이션 비교

- 사용자 요청에 따라 외부 리뷰 개선사항을 바탕으로 확장 universe 62개 심볼 기준 재시뮬레이션을 수행하고 이전 시뮬레이션과 비교했다.
- 개선 후 계산 데이터는 `wiki/raw/sources/2026-05-24-review-hardening-expanded-policy-data.json`에 저장했다.
- 비교 리포트는 `wiki/backtests/2026-05-24-review-hardening-comparison.md`에 작성했다.
- 장타는 `lt-dual-benchmark-confirm-v1`과 `lt-drawdown-volatility-guard-v1`이 이전 `daily-3h-theme-capped-top5`보다 검증 SPY 초과수익과 평균 불리 이동 측면에서 개선됐다.
- 단타는 `intraday-afternoon-followthrough-filter-v1`이 stop 횟수는 줄였지만 hit rate와 총 P/L이 기존 최고 `3h-afternoon-continuation-top2`보다 낮아 자동 주문 금지 결론을 유지했다.
- 실제 주문, 취소, 포지션 변경은 없었다.

## [2026-05-25 02:25 Asia/Seoul] hardening | Request.md 정책/시뮬레이션 개선사항 반영

- 사용자 요청에 따라 `Request.md`의 P0/P1/P2 개선사항을 정책, 스키마, 스크립트, 테스트, workflow, wiki에 반영했다.
- `harness/risk-policy.yaml`을 `medium-risk-v1.1`로 올리고 ticker cap 15%, liquidity/spread, turnover/daily loss, correlated cluster, order lifecycle 한도를 추가했다.
- `harness/symbol-metadata.yaml`로 expanded universe 62개 심볼의 theme/factor/liquidity/source confidence/correlated cluster metadata를 중앙화했다.
- `harness/order-plan.schema.json` v1.2는 exposure metadata, liquidity object, expected return/adverse move, confidence, strategy id/version, policy status, client/decision id를 required로 강제한다.
- `scripts/check-risk-policy.py`는 missing metadata를 error로 처리하고 spread/ADV, source confidence, duplicate id, open order conflict, partial-fill recompute, cluster exposure를 검증한다.
- `harness/recommendation-policy.yaml`, `harness/recommendation-policy.schema.json`, `harness/strategy-config.schema.json`, `harness/strategies/*.yaml`을 추가해 장기 v1은 `active_dry_run_candidate`, intraday는 `observation_only`로 분리했다.
- `scripts/fetch-alpaca-bars-mcp.py`와 `scripts/simulate-one-year-daily-policy.py`를 추가해 Alpaca MCP bars 캡처와 과거 1년 일별 독립 시뮬레이션 workflow를 구성했다.
- Alpaca MCP로 2025-05-23~2026-05-22 62개 심볼 adjusted IEX 일봉 251거래일을 캡처했고, 장기 v1 시뮬레이션은 191개 독립 기준일, 완료 추천 853개, 비용차감 SPY 초과 hit rate 58.73%, 평균 초과 +3.75%, bootstrap 95% CI +2.84%~+4.76%, 평균 불리 이동 -6.46%를 기록했다.
- 2026-03 validation window가 평균 -5.48%로 실패했으며 quote-level fill/source/valuation feature가 아직 부족하므로 정책은 `auto_eligible_paper`가 아니라 `active_dry_run_candidate`로 유지한다. Intraday 자동주문 금지도 유지한다.
- 테스트: `python3 -m unittest discover -s tests` 통과, `scripts/check-risk-policy.py harness/examples/order-plan.example.json` 통과. `ruff`는 로컬에 설치되어 있지 않아 실행하지 못했다.
- 원천 기록: `wiki/raw/sources/2026-05-25-one-year-daily-simulation-sources.md`.
- 백테스트: `wiki/backtests/2026-05-25-one-year-daily-policy-simulation.md`.
- 검토 문서: `wiki/analyses/2026-05-25-request-implementation-review.md`.
- run manifest: `wiki/runs/2026-05-25-one-year-daily-policy-simulation.json`.
- 실제 주문, 취소, 포지션 변경은 없었다.

## [2026-05-25 07:21 Asia/Seoul] review | Request.md 항목별 반영 상태 재검토

- 사용자 요청에 따라 `Request.md`의 17개 요구사항과 파일별 세부 제안을 다시 대조했다.
- `wiki/analyses/2026-05-25-request-implementation-review.md`에 3차 항목별 대조 검토 표를 추가했다.
- 완료 항목은 intraday 관찰 전용, 장기 dry-run 후보, risk v1.1, order-plan metadata required, data manifest, machine-readable recommendation policy, expanded universe cap, risk checker 확장, order lifecycle, policy proposal template 등이다.
- 부분 반영으로 남은 항목은 strategy selector 완전 YAML화, intraday fill/slippage 전용 모델 스크립트, event-level SEC/earnings/news/valuation source confidence 결합, 6개월 train/regime별 walk-forward 확장이다.
- 테스트 재확인: `python3 -m unittest discover -s tests` 32개 통과, `python3 scripts/check-risk-policy.py harness/examples/order-plan.example.json` PASS.
- 실제 주문, 취소, 포지션 변경은 없었다.

## [2026-05-25 07:49 Asia/Seoul] wiki | backtests 하위 구조 통합

- 사용자 요청에 따라 `wiki/simulations/`와 `wiki/reviews/decisions/`를 별도 최상위 개념으로 두지 않고 `wiki/backtests/` 아래로 통합했다.
- 과거 기준 모의 의사결정 문서는 `wiki/backtests/decisions/`로 이동했다. 이 문서는 기준 시점 이후 가격, 뉴스, 결과를 포함하지 않는다.
- 과거 의사결정의 1D/5D/20D 사후 회고 문서는 `wiki/backtests/reviews/`로 이동했다. 이 문서는 미래 가격과 벤치마크 대비 결과를 기록할 수 있다.
- 여러 날짜를 묶은 정책 백테스트, event study, 단타/장타 검증 문서는 `wiki/backtests/summaries/`로 이동했다.
- 큰 원천/계산 데이터는 기존 llm-wiki 원칙에 따라 `wiki/raw/sources/`에 유지하고, `wiki/backtests/data/README.md`에는 데이터 위치 안내만 추가했다.
- `README.md`, `AGENTS.md`, `wiki/index.md`, `harness/workflows/*`, `harness/simple-commands.md`, `harness/agent-tasking-guide.md`, `scripts/check-leakage.py`, run manifest의 참조 경로를 새 구조에 맞췄다.
- `AGENTS.md`의 단일 티커 최대 비중 설명을 현행 `medium-risk-v1.1`과 같은 15%로 맞췄다.
- 검증: `python3 -m unittest discover -s tests` 33개 통과.
- 실제 주문, 취소, 포지션 변경은 없었다.

## [2026-05-25 08:00 Asia/Seoul] wiki | backtests 결과와 reports 역할 재정의

- 사용자 지적에 따라 `wiki/backtests/reviews/`와 `wiki/backtests/summaries/`를 다시 나누지 않고 `wiki/backtests/results/` 하나로 통합했다.
- `wiki/backtests/decisions/`는 미래 정보 없는 과거 기준 모의 의사결정만 저장하고, `wiki/backtests/results/`는 미래 결과를 쓰는 모든 백테스트 결과를 저장하도록 정의했다.
- 기존 개별 historical review 문서와 1년/6개월/단타/장타 정책 검증 문서를 모두 `wiki/backtests/results/`로 이동했다.
- `wiki/reports/`는 모든 사람이 읽는 문서가 아니라 현재 운영/사용자 요청 설명 보고서 저장소로 재정의했다.
- 기존 `wiki/reports/` 루트의 특별 보고서 2개는 `wiki/reports/special/`로 이동했고, 현재 시점 일일 workflow 결과는 `wiki/reports/daily/`에 유지했다.
- `README.md`, `AGENTS.md`, `wiki/index.md`, `harness/workflows/*`, `harness/simple-commands.md`, `harness/agent-tasking-guide.md`, run manifest, 추천 정책 source ref를 새 경로로 갱신했다.
- 검증: `python3 -m unittest discover -s tests` 33개 통과. append-only 로그와 raw source를 제외하고 예전 `wiki/backtests/reviews/`, `wiki/backtests/summaries/`, `wiki/reports/YYYY-...` 참조가 남지 않았음을 확인했다.
- 실제 주문, 취소, 포지션 변경은 없었다.

## [2026-05-25 08:04 Asia/Seoul] wiki | reports 저장 기준 축소

- 사용자 지적에 따라 `reports` 기준을 더 좁혀 `현재 계좌와 현재 시장을 대상으로 실행한 운영 리포트`만 저장하도록 재정의했다.
- `wiki/reports/special/` 개념은 제거했다. 사용자 요청 설명 문서라도 백테스트 결과를 다루면 `wiki/backtests/results/`, 재사용 가능한 정책/투자 인사이트면 `wiki/analyses/`에 둔다.
- `wiki/reports/special/2026-05-23-investment-simulation-insight-report.md`는 `wiki/analyses/2026-05-23-investment-simulation-insight-report.md`로 이동했다.
- `wiki/reports/special/2026-05-24-may-15-decision-process-report.md`는 2026-05-15 과거 결정과 5D 사후 검증을 포함하므로 `wiki/backtests/results/2026-05-24-may-15-decision-process-report.md`로 이동했다.
- `README.md`, `AGENTS.md`, `wiki/reports/README.md`, `wiki/analyses/README.md`, `wiki/index.md`에 새 기준을 반영했다.
- 검증: `python3 -m unittest discover -s tests` 33개 통과. append-only 로그와 raw source를 제외하고 `reports/special`, `wiki/reports/YYYY-...`, 예전 `wiki/backtests/reviews/`, `wiki/backtests/summaries/`, `wiki/simulations/`, `wiki/reviews/decisions/` 참조가 남지 않았음을 확인했다.
- 실제 주문, 취소, 포지션 변경은 없었다.

## [2026-05-25 08:26 Asia/Seoul] wiki | MECE wiki 용어 체계 적용

- 사용자 요청에 따라 wiki 최상위 폴더를 같은 레벨의 저장소 용어로 재구성했다.
- 최종 구조는 `current-runs/`, `backtest-runs/`, `trade-ledger/`, `research-notes/`, `policy-book/`, `evidence-store/`다.
- `wiki/current-runs/daily/`는 현재 계좌와 현재 시장 기준 workflow 결과만 저장한다.
- `wiki/backtest-runs/decisions/`는 미래 정보 없는 과거 기준 모의 의사결정, `wiki/backtest-runs/results/`는 미래 결과를 쓰는 백테스트 결과를 저장한다.
- `wiki/trade-ledger/orders/`, `wiki/trade-ledger/positions/`, `wiki/trade-ledger/reviews/`는 실제 paper 주문/포지션/거래 회고 장부로 분리했다.
- `wiki/research-notes/tickers/`, `wiki/research-notes/portfolio/`, `wiki/research-notes/analyses/`는 다음 판단에 재사용할 지식 저장소로 정리했다.
- `wiki/policy-book/`는 적용할 규칙, `wiki/evidence-store/sources/`와 `wiki/evidence-store/run-manifests/`는 원천 증거와 실행 provenance 저장소로 정리했다.
- `README.md`, `AGENTS.md`, `wiki/index.md`, workflow 문서, 템플릿, run manifest, order plan, 스크립트 경로를 새 구조로 갱신했다.
- 검증: `python3 -m unittest discover -s tests` 33개 통과, `python3 scripts/check-risk-policy.py harness/examples/order-plan.example.json` PASS.
- append-only 로그와 immutable source 본문을 제외한 실행 문서/스크립트/manifest에서 구 경로 참조가 남지 않았음을 확인했다.
- 실제 주문, 취소, 포지션 변경은 없었다.

## [2026-05-25 08:42 Asia/Seoul] daily | 현재 기준 종목 추천 no-submit

- 사용자 요청에 따라 오늘 기준 종목 추천을 no-submit으로 수행했다.
- Alpaca clock 기준 미국 동부 2026-05-24 19:37:59에 시장은 닫혀 있었고, 2026-05-25은 미국 휴장이라 다음 정규장은 2026-05-26 09:30 ET다.
- Alpaca account/positions/orders/watchlists를 확인했다. Portfolio value 100418.67 USD, cash 44030.58 USD, long market value 56388.09 USD, 미체결 주문 없음, watchlist 없음.
- Alpaca MCP로 22개 후보의 2026-02-01~2026-05-24 IEX adjusted daily bars를 캡처했고, Yahoo Finance MCP로 LRCX/UNH/AMD/NVDA 뉴스 맥락을 보강했다.
- 추천 우선순위는 LRCX, UNH, AMD다. NVDA는 보유/확인, NOK와 quantum basket은 급등 과열과 valuation/short-interest risk로 신규 추격을 보류했다.
- 시장 휴장과 stale/missing spread 때문에 신규 order entry는 만들지 않고 empty-order dry-run plan만 생성했다.
- risk check: `python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-05-25-current-recommendations.json` PASS.
- 리포트: `wiki/current-runs/daily/2026-05-25.md`.
- 원천: `wiki/evidence-store/sources/2026-05-25-current-recommendation-sources.md`, `wiki/evidence-store/sources/2026-05-25-current-recommendation-bars.json`.
- run manifest: `wiki/evidence-store/run-manifests/2026-05-25-0842-current-recommendations.json`.
- 실제 주문, 취소, 포지션 변경은 없었다.

## [2026-05-25 09:05 Asia/Seoul] ui | agent run 상태판 추가

- 사용자 요청에 따라 각 agent 역할의 진행 상태, 결과, 추천, 관련 문서를 한눈에 볼 수 있는 서버 없는 정적 UI를 추가했다.
- 생성 스크립트는 `scripts/build-agent-dashboard.py`이고, 결과 HTML은 `ui/agent-dashboard.html`이다.
- UI는 최신 run manifest, current-run report, order plan, wiki log를 읽어 self-contained HTML로 생성한다.
- 리포트, 주문계획, manifest, 원천 파일, 포지션 파일은 UI에서 클릭해 열 수 있다.
- 실제 주문, 취소, 포지션 변경은 없었다.

## [2026-05-25 09:21 Asia/Seoul] ui | backtest HTML viewer 적용

- 사용자 요청에 따라 agent run 상태판에서 초보자 용어 설명 영역을 제거했다.
- Backtests 카드는 원본 Markdown 파일을 직접 열지 않고 `ui/backtests/*.html`로 생성된 보기용 HTML 문서를 열도록 변경했다.
- `scripts/build-agent-dashboard.py`가 상태판 생성 시 최신 백테스트 결과 Markdown을 표, 제목, 목록이 보이는 정적 HTML 문서로 함께 렌더링한다.
- `README.md`, `ui/README.md`, `wiki/index.md`에 dashboard와 backtest viewer 기준을 반영했다.
- 실제 주문, 취소, 포지션 변경은 없었다.

## [2026-05-25 13:59 Asia/Seoul] mcp | FRED 로컬 MCP 서버 적용

- 사용자 요청에 따라 `fred` MCP wrapper가 외부 npm 패키지를 즉석 실행하지 않고 레포 내부 `scripts/fred-mcp-server.py`를 실행하도록 변경했다.
- 로컬 FRED MCP 서버는 `get_series_observations`, `get_series_info`, `search_series`, `get_macro_snapshot` 도구를 제공한다.
- FRED 공식 API health check와 MCP `tools/list`, `tools/call(get_series_observations, DGS10)` 호출이 성공했다.
- `harness/mcp-source-map.md`, `README.md`, `wiki/index.md`에 FRED 로컬 MCP 기준을 반영했다.
- 실제 주문, 취소, 포지션 변경은 없었다.

## [2026-05-25 14:20 Asia/Seoul] analysis | MCP 사용 여부와 시뮬레이션 영향 검토

- 사용자 요청에 따라 daily/current recommendation, historical decision, MCP comparison, one-year daily simulation 이력에서 MCP 사용 여부를 감사했다.
- `2026-05-25` 현재 추천은 Alpaca/Yahoo Finance 중심이었고 SEC/Alpha/FRED/Firecrawl은 quick run 데이터 공백으로 남았음을 확인했다.
- FRED 로컬 MCP로 2026-05-15와 2026-05-22 macro snapshot을 조회했고, Alpha Vantage로 AMD earnings 및 AMD/UNH/LRCX earnings calendar를 확인했다.
- 표본 영향 검토 결과 2026-05-25 추천 순위, 2026-05-15 decision, 2026-05-08 MCP 비교 표본의 큰 결론은 유지하되 AMD staged-only/과열 감점 근거가 강화됐다.
- 대규모 가격 기반 backtest는 MCP 연결만으로 결과가 바뀌지 않으며, as-of event feature cache와 시뮬레이터 결합이 필요하다고 정리했다.
- 분석 문서: `wiki/research-notes/analyses/2026-05-25-mcp-usage-and-simulation-impact-review.md`.
- 실제 주문, 취소, 포지션 변경은 없었다.

## [2026-05-25 17:26 Asia/Seoul] mcp | 키 교체 후 MCP 재확인 및 시뮬레이션 스모크 테스트

- 사용자 요청에 따라 키 교체 후 MCP 정상 동작 여부를 재확인했다. 키 값은 출력하거나 기록하지 않았다.
- `.env`의 필수 변수 존재와 `ALPACA_PAPER_TRADE=true`를 확인했다.
- Alpha Vantage, SEC EDGAR, Yahoo Finance, FRED 로컬 MCP는 정상 응답을 확인했다.
- 현재 세션에 로드된 Alpaca MCP 도구는 401이었지만, `scripts/fetch-alpaca-bars-mcp.py`로 새로 띄운 로컬 Alpaca MCP helper는 SPY/QQQ 일봉을 정상 수집했다. 현재 세션 MCP 재시작이 필요하다.
- Firecrawl은 현재 MCP와 공식 API 최소 호출 모두 `Unauthorized`로 실패했다. Firecrawl 키 또는 Firecrawl 프로젝트/API 설정 재확인이 필요하다.
- Alpaca MCP로 수집한 SPY/QQQ 2026-05-01~2026-05-22 일봉으로 시뮬레이션 helper 스모크 테스트를 통과했다.
- 기존 1년 입력 데이터로 재실행한 결과 `daily_independent_runs=191`, `recommendations=953`, `completed=853`, 정책 상태 `active_dry_run_candidate`가 재현됐다.
- 분석 문서와 인덱스에 최신 재확인 결과를 반영했다.
- 실제 주문, 취소, 포지션 변경은 없었다.

## [2026-05-25 17:36 Asia/Seoul] mcp | Firecrawl 로컬 MCP 전환 및 세션 재확인

- 현재 세션에 이미 로드된 Alpaca MCP는 계좌/시세 조회 모두 401이지만, 새로 띄운 Alpaca MCP helper는 같은 `.env`로 SPY/QQQ 일봉을 정상 수집했다. 현재 세션 MCP 재시작 이슈로 판단한다.
- 현재 세션에 이미 로드된 Firecrawl MCP는 `Invalid token`을 반환했지만, Firecrawl 공식 API는 `zeroDataRetention` 옵션 없이 정상 응답했다.
- 기존 `npx firecrawl-mcp` wrapper는 외부 npm 패키지에 API 키를 넘기는 구조라 새로 실행하지 않고, 레포 내부 `scripts/firecrawl-mcp-server.py` 로컬 MCP 서버로 교체했다.
- 새 Firecrawl 로컬 MCP wrapper의 health check, MCP `tools/list`, MCP `tools/call(firecrawl_scrape)`가 정상 동작했다.
- `harness/mcp-source-map.md`, `wiki/index.md`, MCP 영향 검토 문서에 로컬 Firecrawl MCP 기준과 세션 재시작 필요성을 반영했다.
- 실제 주문, 취소, 포지션 변경은 없었다.

## [2026-05-25 17:58 Asia/Seoul] mcp | 현재 세션 MCP 연결 및 시뮬레이션 사용 감사

- 사용자 요청에 따라 현재 세션에서 MCP 연결과 시뮬레이션의 MCP 사용 여부를 재점검했다. 키 값은 출력하거나 기록하지 않았다.
- `.env`의 필수 변수 존재와 `ALPACA_PAPER_TRADE=true`를 확인했다.
- 현재 Codex 세션 MCP 기준 Alpaca, Alpha Vantage, SEC EDGAR, Yahoo Finance는 read-only 호출이 정상 응답했다.
- Firecrawl은 로컬 wrapper `initialize`/`tools/list`와 공식 API health check가 정상 응답했다.
- FRED는 로컬 wrapper `initialize`/`tools/list`는 정상이나, 공식 API health check는 sandbox DNS 제한과 escalated credential network 거부로 이번 세션에서 확인하지 못했다.
- 기존 Alpaca MCP 1년 일봉 입력으로 장기 시뮬레이션을 재실행해 `daily_independent_runs=191`, `recommendations=953`, `completed=853`, 비용 차감 hit rate `58.73388%`, 평균 SPY 초과수익 `+3.749958%p`, `active_dry_run_candidate` 상태를 재현했다.
- 모든 시뮬레이션이 모든 MCP를 쓰는 구조는 아니며, 가격 기반 1년/6개월 시뮬레이션은 설계상 Alpaca bars 중심임을 확인했다. SEC/Alpha/FRED/Firecrawl/Yahoo는 아직 event-level feature cache로 결합되지 않았다.
- `scripts/simulate-intraday-policy-candidates.py`와 `scripts/simulate-short-long-policy-review.py`에 Alpaca market data REST 직접 `curl` 경로가 남아 있어 MCP-only 원칙에 맞게 이전해야 한다.
- 원천: `wiki/evidence-store/sources/2026-05-25-mcp-connection-simulation-audit-sources.md`.
- run manifest: `wiki/evidence-store/run-manifests/2026-05-25-1758-mcp-connection-simulation-audit.json`.
- 검증: `python3 -m unittest discover -s tests` 41개 통과.
- 실제 주문, 취소, 포지션 변경은 없었다.

## [2026-05-25 18:16 Asia/Seoul] mcp | 시뮬레이션 MCP-only 경로와 event feature 결합 조치

- 사용자 요청에 따라 이전 감사에서 남은 공백을 조치했다.
- `scripts/alpaca_mcp_bars.py`를 추가해 Alpaca `get_stock_bars` read-only MCP 호출을 공용 helper로 만들었다.
- `scripts/simulate-intraday-policy-candidates.py`와 `scripts/simulate-short-long-policy-review.py`의 Alpaca market data REST 직접 `curl` 경로를 제거하고 MCP helper로 이전했다.
- `scripts/simulate-one-year-daily-policy.py`, `scripts/simulate-long-term-policy.py`, `scripts/simulate-six-month-3h-policy-review.py`에 `--event-features-json` 입력을 추가했다.
- event feature cache는 `available_at`/`asof_date` 기준으로만 과거 시점에 결합하며, `score_adjustment`, `source_confidence_delta`, `exclude`, `mcp_gaps`, `source_refs`를 반영한다.
- `harness/templates/event-feature-cache.json` 템플릿과 `harness/workflows/one-year-daily-simulation.md`의 feature cache 단계를 추가했다.
- 샘플 feature cache smoke에서 `mcp_event_servers_used=alpha-vantage,firecrawl,fred,sec-edgar,yahoo-finance`, `event_feature_cache_used=true`, `orders_submitted=0`을 확인했다.
- 검증: `python3 -m py_compile ...` PASS, `python3 -m unittest discover -s tests` 45개 통과.
- 원천: `wiki/evidence-store/sources/2026-05-25-mcp-simulation-integration-fix-sources.md`.
- run manifest: `wiki/evidence-store/run-manifests/2026-05-25-1816-mcp-simulation-integration-fix.json`.
- 실제 주문, 취소, 포지션 변경은 없었다.

## [2026-05-25 18:28 Asia/Seoul] simulation | MCP event feature 반영 검증 및 과거 시뮬레이션 대비 분석

- 사용자 요청에 따라 MCP-only market data 이전과 research MCP event feature cache 결합이 실제 시뮬레이션에 반영됐는지 검증했다.
- 1년 장기 시뮬레이션 baseline 재실행은 기존 결과와 `recommendations=953`, `completed=853`, hit rate `58.73388%`, 평균 SPY 초과수익 `+3.749958%p`가 모두 일치했다.
- 62개 심볼 무영향 event cache를 결합한 실행은 `event_feature_matches=953/953`, `mcp_event_servers_used=alpha-vantage,firecrawl,fred,sec-edgar,yahoo-finance`였고 성과/추천 구성은 baseline과 동일했다.
- 감도 테스트 cache는 baseline 대비 추천 key 214개를 바꿔 event score adjustment가 ranking에 실제 반영됨을 확인했다.
- 기존 6개월 3시간 결과의 단타 trade row 351개와 장타 recommendation row 1,074개에 최신 event join 로직을 적용해 모두 100% 매칭됨을 확인했다.
- 6개월 live MCP smoke run은 sandbox의 `uv` cache 접근 제한으로 실패했고, unsandboxed 재시도는 정책상 승인되지 않아 기존 captured-row coverage 감사로 대체했다.
- 검증: `python3 -m unittest discover -s tests` 45개 통과. 직접 Alpaca market data REST 흔적은 테스트 assertion 외 없음.
- 분석 문서: `wiki/research-notes/analyses/2026-05-25-mcp-simulation-integration-verification.md`.
- 원천: `wiki/evidence-store/sources/2026-05-25-mcp-simulation-integration-verification-sources.md`.
- run manifest: `wiki/evidence-store/run-manifests/2026-05-25-1828-mcp-simulation-integration-verification.json`.
- 실제 주문, 취소, 포지션 변경은 없었다.

## [2026-05-25 18:34 Asia/Seoul] mcp | uvx 기반 MCP wrapper runtime 경로 조치

- 사용자 요청에 따라 6개월 live MCP smoke run 실패 원인을 설명하고 조치했다.
- 원인은 `uvx`가 기본 홈 경로 `~/.cache/uv`, `~/.local/share/uv/tools`에 cache/tool environment를 만들려다 sandbox 권한에 막힌 것이었다.
- `.gitignore`에 `.cache/`를 추가하고 Alpaca/SEC EDGAR/Alpha Vantage/Yahoo Finance wrapper가 `UV_CACHE_DIR`, `UV_TOOL_DIR`, `XDG_CACHE_HOME`, `XDG_DATA_HOME`을 레포 내부 `.cache/`로 사용하게 변경했다.
- 로컬 설치된 MCP 실행 파일이 있으면 `uvx` 없이 우선 실행하도록 fallback을 추가했다.
- 제한 범위 6개월 smoke 재시도에서 홈 cache/tool 권한 에러는 사라졌으나, 레포-local cache가 비어 있어 `alpaca-mcp-server` PyPI 조회가 필요했고 sandbox DNS 제한으로 실패했다. unsandboxed 재시도는 정책상 승인되지 않았다.
- 검증: wrapper `bash -n` PASS, `python3 -m unittest tests.test_mcp_runtime_wrappers` 3개 통과, `python3 -m unittest discover -s tests` 48개 통과.
- 원천: `wiki/evidence-store/sources/2026-05-25-mcp-uv-runtime-fix-sources.md`.
- run manifest: `wiki/evidence-store/run-manifests/2026-05-25-1834-mcp-uv-runtime-fix.json`.
- 실제 주문, 취소, 포지션 변경은 없었다.

## [2026-05-25 18:45 Asia/Seoul] ui | dashboard Alpaca paper 투자 현황 카드 추가

- 사용자 요청에 따라 `ui/agent-dashboard.html`에 현재 Alpaca paper 투자 현황을 간단히 볼 수 있는 `Alpaca Paper` 영역을 추가했다.
- `scripts/build-agent-dashboard.py`가 최신 run manifest와 별개로 `wiki/trade-ledger/positions/current.md`를 읽어 평가금액, 총 수익, 투자 노출, 현금, 미체결 주문 여부, 주요 보유 종목을 렌더링한다.
- 최신 run이 MCP 감사/시뮬레이션 검증처럼 order plan이 없는 경우에도 dashboard 상단 투자/현금 비율은 포트폴리오 스냅샷으로 fallback한다.
- `tests/test_agent_dashboard_portfolio.py`를 추가해 포트폴리오 스냅샷 파싱과 dashboard fallback 비율을 검증했다.
- `python3 scripts/build-agent-dashboard.py`로 정적 HTML을 재생성했다.
- 검증: `python3 -m py_compile scripts/build-agent-dashboard.py`, `python3 -m unittest tests.test_agent_dashboard_portfolio`, `python3 -m unittest discover -s tests` 50개 통과.
- 브라우저 자동화 확인은 현재 세션에 `playwright` 모듈이 없어 실행하지 못했다. 생성 HTML의 embedded data와 테스트로 Alpaca Paper 데이터 반영을 확인했다.
- 실제 주문, 취소, 포지션 변경은 없었다.

## [2026-05-25 21:48 Asia/Seoul] simulation | 1년 1시간봉 일별 buy/sell 동향보강 시뮬레이션

- 사용자 요청에 따라 지난 1년 2025-05-23~2026-05-22 기간을 1시간봉 단위로 캡처하고, 일별 virtual buy/sell 결정을 same-day/1D/5D/20D/60D로 평가했다.
- `ALPACA_PAPER_TRADE=true`를 확인했고, Alpaca MCP `get_stock_bars`로 62개 심볼 114,060개 1시간봉을 수집했다.
- 사용자가 지적한 당시 동향정보 필요성을 반영해 Alpaca MCP `get_news` 38,131건과 전일 시장/섹터 추세를 결합한 point-in-time event feature cache 13,570개 row를 생성했다. 뉴스는 각 거래일 장 시작 전 3일 window만 집계해 당일 장중 이후 뉴스 누수를 피했다.
- 가격-only 기준선은 추천 2,100개, 20D hit rate 54.263158%, 평균 방향성 SPY 초과수익 +0.849527%p였다.
- 동향보강 실행은 추천 2,100개 모두 event feature와 매칭됐고, 20D hit rate 53.210526%, 평균 방향성 SPY 초과수익 +0.567017%p였다.
- `virtual_sell`은 short가 아니라 기존 long 회피/매도 판단으로만 평가했다.
- 실행 중 Coordinator/Market Data/Web Research/Trend/Simulation/Wiki Curator Agent 진행 줄을 Codex 작업창에 출력했고, 일별 agent report는 결과 JSON에 저장했다.
- 신규 헬퍼: `scripts/fetch-alpaca-hourly-bars-mcp.py`, `scripts/build-one-year-hourly-trend-event-cache.py`, `scripts/simulate-one-year-hourly-buy-sell.py`.
- 결과 문서: `wiki/backtest-runs/results/2026-05-25-one-year-hourly-buy-sell-trend-enhanced-simulation.md`.
- 원천: `wiki/evidence-store/sources/2026-05-25-one-year-hourly-buy-sell-trend-enhanced-simulation-sources.md`, `wiki/evidence-store/sources/2026-05-25-one-year-hourly-trend-event-cache-sources.md`.
- run manifest: `wiki/evidence-store/run-manifests/2026-05-25-one-year-hourly-buy-sell-trend-enhanced-simulation.json`.
- 검증: `python3 -m py_compile scripts/fetch-alpaca-hourly-bars-mcp.py scripts/build-one-year-hourly-trend-event-cache.py scripts/simulate-one-year-hourly-buy-sell.py`, `python3 -m unittest tests.test_one_year_hourly_buy_sell`, `python3 -m unittest discover -s tests` 51개 통과.
- 실제 주문, 취소, 포지션 변경은 없었다. 모든 산출물은 `orders_submitted=0`이다.

## [2026-05-25 21:57 Asia/Seoul] policy | 1년 1시간봉 시뮬레이션 정책학습 반영

- 사용자 요청에 따라 주식 전문 애널리스트 관점에서 1년 1시간봉 가격-only/동향보강 buy/sell 시뮬레이션의 정책학습 레슨을 검토했다.
- 결론은 정책 승격 없음이다. 동향보강 cache는 전체 20D directional SPY 초과수익이 가격-only +0.849527%p보다 낮은 +0.567017%p였으므로 신규 feature로 채택하지 않았다.
- `virtual_buy`는 20D +3.277523%p, 60D +14.809358%p로 장기 후보 보조 확인 가설로 기록했다.
- `virtual_sell`은 20D directional SPY 초과수익 -2.143489%p로 장기 청산/회피 신호 채택을 금지하는 레슨으로 기록했다.
- `harness/recommendation-policy.yaml`을 v1.2로 갱신하고 `one_year_hourly_buy_sell_v1`을 `observation_only` 전략 상태로 추가했다.
- `wiki/policy-book/recommendation-policy.md`에 policy closeout 원칙, 시뮬레이션 정책 검토 프로토콜, 신규 정책학습 지표, 폐기/완화 규칙을 반영했다.
- `harness/workflows/one-year-daily-simulation.md`에 baseline comparison, action/horizon split, decision label, failure lesson 기록을 필수 closeout으로 추가했다.
- 실제 주문, 취소, 포지션 변경은 없었다. 정책 반영은 연구/백테스트 레슨 기록이며 자동 주문 허용 변경은 없다.

## [2026-05-25 22:06 Asia/Seoul] daily | 오늘 종목추천 재점검

- 사용자 요청 "오늘 종목추천"에 따라 simple command 변형을 `harness/workflows/daily.md` no-submit 모드로 처리했다.
- Alpaca MCP로 account, positions, open orders, clock, latest quote, news를 재확인했다. 미국 동부 `2026-05-25T09:06:06-04:00` 기준 정규장은 닫혀 있고 다음 개장은 `2026-05-26T09:30:00-04:00`이다.
- 포트폴리오 가치 100418.67 USD, 현금 44030.58 USD, long market value 56388.09 USD, 미체결 주문 0건을 확인했다.
- 추천 우선순위는 `LRCX`, `UNH`, `AMD`다. `LRCX/UNH`는 fresh quote 확인 후 staged 추가 후보, `AMD`는 과열/cluster 노출 때문에 소액 staged only로 정리했다.
- `TSLA`는 가격 필터는 통과했지만 이번 run에서 별도 이벤트/밸류에이션 원천을 캡처하지 않아 관찰 후보로만 두었다. `NOK/IONQ/RGTI/QBTS`는 급등 과열로 추격 금지다.
- Alpaca IEX latest quote는 2026-05-22 장마감 근처 stale quote였고 일부 후보는 ask=0 또는 wide spread라 주문 항목을 만들지 않았다.
- 원천: `wiki/evidence-store/sources/2026-05-25-today-stock-recommendation-sources.md`.
- dry-run 주문계획: `wiki/trade-ledger/orders/2026-05-25-2206-today-stock-recommendation.json`.
- run manifest: `wiki/evidence-store/run-manifests/2026-05-25-2206-today-stock-recommendation.json`.
- 검증: `python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-05-25-2206-today-stock-recommendation.json` PASS.
- 실제 주문, 취소, 포지션 변경은 없었다. `orders_submitted=0`.

## [2026-05-26 19:32 Asia/Seoul] policy-update | paper 자동운영 보수성 완화

- 사용자 요청에 따라 paper pilot 목적에 맞게 과도한 provider-all-pass 요구를 완화했다. 별도 paper pilot tier는 추가하지 않았다.
- MCP gate를 Alpaca core gate와 research confirmation gate로 분리했다. Alpaca account/clock/order/position/quote/spread는 계속 필수이고, SEC EDGAR/Alpha Vantage/FRED/Firecrawl/Yahoo Finance는 모두 시도하되 최소 3개 usable/pass면 research gate가 통과할 수 있다.
- provider 일부 장애로 막힌 강한 후보는 `actionable_if_provider_recovered`로 남겨 다음 hourly run에서 재검토하게 했다.
- sell/trim은 thesis-break 외에도 speculative cap, cluster cap, theme/factor cap, overheat profit protection 등 risk trim 사유를 허용한다. 단 Alpaca core, fresh quote/spread, open-order state, risk gate는 계속 필수다.
- 검증: `python3 -m unittest discover -s tests` 63개 통과.

## [2026-05-26 15:18 Asia/Seoul] policy | 추천 MCP coverage gate 강화

- 사용자 요청에 따라 빠른 판단보다 정확한 판단을 우선하도록 추천 정책 실행 기준을 강화했다.
- `scripts/check-mcp-coverage.py`를 추가해 recommendation run manifest의 MCP coverage를 검증하도록 했다.
- Actionable dry-run 또는 submit-mode 추천은 Alpaca, SEC EDGAR, Alpha Vantage, FRED, Firecrawl, Yahoo Finance가 모두 `queried=true`, `outcome=pass|usable|ok`, source ref 1개 이상이어야 통과한다.
- Submit mode에서는 모든 required MCP가 `used_in_score=true`여야 한다.
- `harness/templates/run-manifest.json`와 `harness/run-manifest.schema.json`에 `mcp_coverage`와 `recommendation_actionability` 필드를 추가했다.
- `harness/workflows/daily.md`, `harness/templates/daily-report.md`, `harness/mcp-source-map.md`, `AGENTS.md`, `README.md`에 all-MCP coverage gate와 `MCP Coverage Matrix` 기준을 반영했다.
- 최신 기존 추천 manifest `2026-05-25-2206-today-stock-recommendation.json`은 새 검증 기준에서 `mcp_coverage` 부재로 FAIL함을 확인했다. 앞으로 같은 빠른 Alpaca+Yahoo 추천은 actionable 추천으로 통과하지 못한다.
- 검증: `python3 -m py_compile scripts/check-mcp-coverage.py`, `python3 -m unittest tests.test_check_mcp_coverage`, `python3 -m unittest discover -s tests` 56개 통과.
- 실제 주문, 취소, 포지션 변경은 없었다.

## [2026-05-26 15:35 Asia/Seoul] daily | all-MCP 현재 종목 추천

- 사용자 요청에 따라 강화된 MCP coverage gate 기준으로 현재 종목 추천을 다시 수행했다.
- Alpaca, SEC EDGAR, Alpha Vantage, FRED, Firecrawl, Yahoo Finance를 모두 확인했다.
- Alpaca account는 ACTIVE, portfolio value 101389.32 USD, cash 44030.58 USD, long market value 57358.74 USD, 미체결 주문 없음.
- Alpaca clock은 미국 동부 2026-05-26 02:27 기준 closed이고 next open은 2026-05-26 09:30 ET다.
- 최신 정규장 일봉은 2026-05-22 종가이며, 최신 quote는 2026-05-22 장마감 부근 stale quote라 주문 후보는 만들지 않았다.
- 추천 우선순위는 `LRCX`, `UNH`, `AMD`다. `LRCX/UNH`는 개장 후 fresh quote 확인 시 staged 후보, `AMD`는 과열 감점 때문에 소액 staged only다.
- MCP coverage 검증: `python3 scripts/check-mcp-coverage.py --strict --json wiki/evidence-store/run-manifests/2026-05-26-1535-current-all-mcp-recommendation.json` PASS.
- Risk check: `python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-05-26-1535-current-all-mcp-recommendation.json` PASS with empty orders warning.
- 리포트: `wiki/current-runs/daily/2026-05-26.md`.
- 실제 주문, 취소, 포지션 변경은 없었다. `orders_submitted=0`.
## [2026-05-26 16:20 Asia/Seoul] daily | expanded-universe 종목 재추천

- 요청: 추천 정책을 한 단계 더 강화한 뒤 종목을 재추천.
- 변경: `harness/recommendation-policy.yaml`을 v1.3으로 올리고 broad universe screen, universe coverage manifest, universe gate를 추가. `scripts/check-universe-coverage.py`와 테스트 추가.
- 실행: `harness/symbol-metadata.yaml`의 62개 확장 universe를 Alpaca MCP daily bars로 1차 스크리닝하고 `LLY`, `LRCX`, `AAPL`, `SMH`, `ASML`을 pre-MCP shortlist로 선정.
- 결과: 최종 연구 추천은 `LRCX`, `LLY`, `ASML`. 다만 expanded shortlist Firecrawl IR scrape 실패로 strict MCP coverage는 실패하므로 `non_actionable_research`, 주문 없음.
- 산출물: `wiki/current-runs/daily/2026-05-26-expanded-universe.md`, `wiki/evidence-store/run-manifests/2026-05-26-1620-expanded-universe-recommendation.json`, `wiki/trade-ledger/orders/2026-05-26-1620-expanded-universe-recommendation.json`.

## [2026-05-26 18:53 Asia/Seoul] hourly-autopilot | paper 자동 운영 gate 점검

- 사용자 승인에 따라 `harness/workflows/hourly-autopilot.md`를 실행했다.
- `.env`에서 `ALPACA_PAPER_TRADE=true`를 확인했고, API key 값은 출력하거나 기록하지 않았다.
- Alpaca MCP `get_all_positions`, `get_market_movers`, broad universe `get_stock_bars`, shortlist `get_asset`, `get_news`는 usable했다.
- Alpaca MCP clock/account/orders/fills/watchlists/latest quote/snapshot/latest bar는 usable하지 않았고, repo-local Alpaca MCP도 DNS 실패를 반환했다.
- 62개 metadata universe와 `SPY`/`QQQ`를 스크리닝했다. pre-MCP shortlist는 `LLY`, `LRCX`, `ASML`, `AAPL`, `SMH`, final research candidates는 `LLY`, `LRCX`, `ASML`.
- SEC EDGAR, Alpha Vantage, FRED, Firecrawl, Yahoo Finance coverage가 실패해 MCP strict gate가 FAIL했다. quote freshness와 spread도 확인 불가라 자동 주문 gate가 실패했다.
- 검증: universe strict PASS, MCP strict FAIL, empty-order risk-check PASS.
- 리포트: `wiki/current-runs/daily/2026-05-26-1853-hourly-autopilot.md`.
- 원천: `wiki/evidence-store/sources/2026-05-26-1853-hourly-autopilot-sources.md`.
- run manifest: `wiki/evidence-store/run-manifests/2026-05-26-1853-hourly-autopilot.json`.
- order plan: `wiki/trade-ledger/orders/2026-05-26-1853-hourly-autopilot.json`.
- 실제 주문, 취소, 포지션 변경은 없었다. `orders_submitted=0`.

## [2026-05-26 20:11 Asia/Seoul] hourly-autopilot | paper 자동 운영 gate 점검

- 사용자 승인에 따라 `harness/workflows/hourly-autopilot.md`를 실행했다.
- `.env`에서 `ALPACA_PAPER_TRADE=true`를 확인했고, API key 값은 출력하거나 기록하지 않았다.
- Alpaca MCP `get_all_positions`, `get_market_movers`, broad universe `get_stock_bars`, shortlist `get_asset`, `get_news`는 일부 usable했다.
- Alpaca MCP clock/account/orders/fills/watchlists/latest quote/snapshot/latest bar는 usable하지 않았고, repo-local Alpaca MCP clock도 DNS 실패를 반환했다.
- 62개 metadata universe와 `SPY`/`QQQ`를 스크리닝했다. pre-MCP shortlist는 `LLY`, `LRCX`, `ASML`, `AAPL`, `SMH`, final research candidates는 `LLY`, `LRCX`, `ASML`.
- SEC EDGAR, Alpha Vantage, FRED, Firecrawl, Yahoo Finance coverage가 실패해 MCP strict gate가 FAIL했다. quote freshness와 spread도 확인 불가라 자동 주문 gate가 실패했다.
- 검증: universe strict PASS, MCP strict FAIL, empty-order risk-check PASS.
- 리포트: `wiki/current-runs/daily/2026-05-26-2011-hourly-autopilot.md`.
- 원천: `wiki/evidence-store/sources/2026-05-26-2011-hourly-autopilot-sources.md`.
- run manifest: `wiki/evidence-store/run-manifests/2026-05-26-2011-hourly-autopilot.json`.
- order plan: `wiki/trade-ledger/orders/2026-05-26-2011-hourly-autopilot.json`.
- 실제 주문, 취소, 포지션 변경은 없었다. `orders_submitted=0`.

## [2026-05-26 21:24 Asia/Seoul] hourly-autopilot | paper 자동 운영 gate 점검

- 사용자 승인에 따라 `harness/workflows/hourly-autopilot.md`를 실행했다.
- `.env`에서 `ALPACA_PAPER_TRADE=true`를 확인했고, API key 값은 출력하거나 기록하지 않았다.
- Alpaca MCP `get_all_positions`, broad universe `get_stock_bars`, shortlist `get_asset`, `get_market_movers`, `get_news`, `get_stock_quotes(SPY)`는 일부 usable했다.
- Alpaca MCP clock/account/orders/fills/watchlists/calendar/latest quote/snapshot/latest bar와 후보별 recent quote는 usable하지 않았거나 비어 있었다.
- 62개 metadata universe와 `SPY`/`QQQ`를 스크리닝했다. pre-MCP shortlist는 `LLY`, `LRCX`, `ASML`, `AAPL`, `SMH`, final research candidates는 `LLY`, `LRCX`, `ASML`.
- SEC EDGAR, Alpha Vantage, FRED, Firecrawl, Yahoo Finance coverage가 실패해 MCP strict gate가 FAIL했다. quote freshness와 spread도 확인 불가라 자동 주문 gate가 실패했다.
- 검증: universe strict PASS, MCP strict FAIL, empty-order risk-check PASS.
- 리포트: `wiki/current-runs/daily/2026-05-26-2124-hourly-autopilot.md`.
- 원천: `wiki/evidence-store/sources/2026-05-26-2124-hourly-autopilot-sources.md`.
- run manifest: `wiki/evidence-store/run-manifests/2026-05-26-2124-hourly-autopilot.json`.
- order plan: `wiki/trade-ledger/orders/2026-05-26-2124-hourly-autopilot.json`.
- 실제 주문, 취소, 포지션 변경은 없었다. `orders_submitted=0`.

## [2026-05-26 22:18 Asia/Seoul] policy-update | paper 검증 실행성 강화

- 사용자 우려에 따라 paper pilot이 지나치게 보수적으로 아무 주문도 만들지 못하는 문제를 줄이기 위해 `harness/recommendation-policy.yaml`을 `recommendation-policy-v1.5`로 갱신했다.
- `paper_validation_execution`을 추가해, 모든 hard gate가 통과하면 개장 직후 1주 단위의 작은 검증 주문을 선호하도록 했다.
- 단 Alpaca paper mode, 시장 개장, Alpaca core account/clock/position/order/quote/spread, universe strict, tiered MCP strict, risk policy, fresh quote, spread, whole-share day limit order gate는 계속 필수다.
- hard gate 실패 시에는 강제 주문하지 않고 첫 차단 gate, 다음 완화 후보, 상위 재점검 후보를 기록하도록 했다.
- hourly interval drift로 22:30 KST 개장 직후를 놓치지 않도록 `scripts/run-market-open-autopilot-codex.sh`와 `scheduler/com.insightque.stock-alpaca.market-open-autopilot.plist.example`을 추가했다.

## [2026-05-26 22:42 Asia/Seoul] scheduler-update | hourly 자동운영 단일화

- `hourly-autopilot`과 `market-open-autopilot`이 같은 목적의 paper 자동운영 판단을 수행하므로 별도 market-open 작업을 제거하고 hourly 작업 하나로 통합했다.
- `hourly-autopilot` launchd 예제를 `StartInterval=3600`에서 `StartCalendarInterval Minute=31`로 변경했다.
- 22:31 KST 실행을 US regular market-open validation run으로 사용하도록 `harness/recommendation-policy.yaml`을 `recommendation-policy-v1.6`으로 갱신했다.
- 설치된 launchd도 현재 실행 중인 hourly 작업이 끝난 뒤 같은 구조로 재등록할 예정이다.

## [2026-05-26 22:50 Asia/Seoul] reliability-update | MCP gap 분류와 실행 timeout 강화

- 자동운영 MCP 실패 원인을 `timeout`, `cancelled`, `dns`, `auth`, `empty_response`, `provider_error`, `wrapper_error`, `unknown` 등으로 분리 기록하도록 run manifest schema와 checker를 확장했다.
- Alpaca core 실패 시 `first_blocking_gate`를 남겨 clock/account/orders/positions/quotes 중 무엇이 주문을 막았는지 추적하도록 했다.
- `scripts/run-hourly-autopilot-codex.sh`에 Codex 실행 timeout 기본 2400초를 추가해 장시간 stuck 상태가 다음 스케줄을 막지 않도록 했다.
- SEC EDGAR ticker lookup 보강을 위해 SEC `company_tickers.json` 기반 로컬 캐시 `harness/sec-ticker-cik-map.json`을 추가했다. 현재 universe 62개 중 61개가 매핑되고 `SMH`만 SEC company ticker 캐시에서 제외됐다.
- 검증: `python3 -m unittest discover -s tests` 64개 통과, shell syntax 통과.
- 예외 수동 실행 중 OpenClaw `CODEX_HOME`을 상속하면 Codex CLI가 사용자 `~/.codex/auth.json`을 보지 못해 `401 Unauthorized`가 발생하는 것을 확인했다. 자동운영 wrapper에서 `CODEX_HOME=${HOME}/.codex`를 명시하도록 보완했다.

## [2026-05-26 23:01 Asia/Seoul] hourly-autopilot | paper 자동 운영 gate 점검

- 사용자 승인에 따라 `harness/workflows/hourly-autopilot.md`를 실행했다.
- `.env`에서 `ALPACA_PAPER_TRADE=true`를 확인했고, API key 값은 출력하거나 기록하지 않았다.
- Alpaca MCP `get_all_positions`, broad universe `get_stock_bars`, 후보 `get_asset`, `get_stock_quotes`, `get_market_movers`, `get_news`는 일부 usable했다.
- Alpaca MCP `get_clock`, `get_account_info`, `get_orders`, `get_account_activities`, `get_watchlists`, `get_stock_latest_quote`, `get_stock_snapshot`은 retry 후에도 cancelled였고 첫 차단 gate는 `alpaca_clock`이다.
- 62개 metadata universe와 `SPY`/`QQQ`를 스크리닝했다. pre-MCP shortlist는 `LLY`, `LRCX`, `ASML`, `SMH`, `AAPL`, final research candidates는 `LLY`, `LRCX`, `ASML`.
- 후보 quote는 fresh였지만 `LLY` 10.46%, `LRCX` 9.16%, `ASML` 0.66% spread로 buy spread gate가 실패했다.
- SEC EDGAR는 로컬 CIK cache를 사용한 뒤 direct MCP calls가 cancelled였다. `SMH`는 SEC ticker lookup empty_response로 provider failure와 구분했다.
- Alpha Vantage/Yahoo Finance는 cancelled, FRED/Firecrawl은 DNS failure로 gap 분류했다. research MCP usable count는 0이다.
- 검증: universe strict PASS, MCP strict FAIL, empty-order risk-check PASS.
- 리포트: `wiki/current-runs/daily/2026-05-26-2301-hourly-autopilot.md`.
- 원천: `wiki/evidence-store/sources/2026-05-26-2301-hourly-autopilot-sources.md`.
- run manifest: `wiki/evidence-store/run-manifests/2026-05-26-2301-hourly-autopilot.json`.
- order plan: `wiki/trade-ledger/orders/2026-05-26-2301-hourly-autopilot.json`.
- 실제 주문, 취소, 포지션 변경은 없었다. `orders_submitted=0`.

## [2026-05-26 23:22 Asia/Seoul] reliability-update | scheduled MCP 자동실행 보강

- `scripts/run-hourly-autopilot-codex.sh`에서 scheduled Codex 실행에 `--ephemeral`, MCP `approval_mode="auto"` override, research MCP용 `network-full-access` sandbox permission을 명시해 비대화형 실행 중 `user cancelled MCP tool call`과 FRED/Firecrawl DNS gap을 줄이도록 했다.
- hourly autopilot 전용 override에는 Alpaca read-only 도구와 paper `place_stock_order`만 포함했다. 주문은 계속 workflow hard gate와 risk policy를 통과해야 한다.
- `scripts/run-analyst-review-codex.sh`도 같은 scheduled read-only MCP override와 timeout 구조를 사용하도록 보강했다. analyst review는 주문 제출 도구를 auto-approve하지 않는다.
- hourly/analyst scheduled runner 모두 `CODEX_HOME` 기본값을 `${HOME}/.codex`로 고정하되 `CODEX_SCHEDULED_CODEX_HOME` 또는 각 workflow 전용 override로 바꿀 수 있게 했다.
- `scripts/mcp-alpha-vantage.sh`가 API key를 process argv로 넘기지 않고 `ALPHA_VANTAGE_API_KEY` 환경변수로만 전달하도록 수정했다.
- 검증: `bash -n` 통과, `python3 -m unittest discover -s tests` 66개 통과, Codex MCP config override parse 확인, Alpha Vantage wrapper argv smoke test 통과.

## [2026-05-26 23:35 Asia/Seoul] hourly-autopilot | paper 자동 운영 gate 점검

- 사용자 승인에 따라 `harness/workflows/hourly-autopilot.md`를 실행했다.
- `.env`에서 `ALPACA_PAPER_TRADE=true`를 확인했고, API key 값은 출력하거나 기록하지 않았다.
- Alpaca MCP `get_stock_bars` broad universe와 후보 `get_stock_quotes`는 일부 usable했다.
- Alpaca MCP `get_clock`, `get_account_info`, `get_orders`, `get_all_positions`, `get_account_activities`, `get_watchlists`, `get_stock_latest_quote`, `get_stock_snapshot`, `get_asset`, `get_news`, `get_market_movers`는 retry 후에도 cancelled였고 첫 차단 gate는 `alpaca_clock`이다.
- 62개 metadata universe와 `SPY`/`QQQ`를 스크리닝했다. pre-MCP shortlist는 `LLY`, `LRCX`, `ASML`, `SMH`, `AAPL`, final research candidates는 `LLY`, `LRCX`, `ASML`.
- 후보 quote는 fresh였고 `LLY`, `ASML`, `SMH`, `AAPL` spread는 통과했지만 `LRCX` spread는 9.16%로 실패했다. Alpaca core와 research MCP gate 실패 때문에 주문은 제출하지 않았다.
- SEC EDGAR는 로컬 CIK cache를 사용한 뒤 direct MCP calls가 cancelled였다. `SMH`는 SEC ticker lookup empty_response로 provider failure와 구분했다.
- Alpha Vantage/Yahoo Finance는 cancelled, FRED/Firecrawl은 DNS failure로 gap 분류했다. research MCP usable count는 0이다.
- 검증: universe strict PASS, MCP strict FAIL, empty-order risk-check PASS.
- 리포트: `wiki/current-runs/daily/2026-05-26-2331-hourly-autopilot.md`.
- 원천: `wiki/evidence-store/sources/2026-05-26-2331-hourly-autopilot-sources.md`.
- run manifest: `wiki/evidence-store/run-manifests/2026-05-26-2331-hourly-autopilot.json`.
- order plan: `wiki/trade-ledger/orders/2026-05-26-2331-hourly-autopilot.json`.
- 실제 주문, 취소, 포지션 변경은 없었다. `orders_submitted=0`.

## [2026-05-26 23:45 Asia/Seoul] reliability-update | nested Codex MCP 승인 모드 수정

- 23:31 one-off hourly autopilot에서 scheduled wrapper 자체, lock, artifact 생성, autopush는 동작했지만 nested Codex의 MCP tool 호출이 다수 `user cancelled MCP tool call`로 실패하는 것을 확인했다.
- 원인은 scheduled runner가 MCP override에 `approval_mode="auto"`를 사용한 점으로 판단했다. 현재 Codex MCP 설정에서 비대화형 `-a never` 실행 중 prompt 없이 진행해야 하는 도구는 `approval_mode="approve"`로 명시해야 한다.
- hourly runner에 Alpaca core/read/quote/news/mover/order 도구와 SEC EDGAR, Alpha Vantage, Yahoo Finance, FRED, Firecrawl research 도구의 scheduled-only `approval_mode="approve"` override를 추가했다.
- analyst review runner에도 주문 제출 도구를 제외한 read/research 도구의 scheduled-only `approval_mode="approve"` override를 추가했다.
- 검증: `python3 -m unittest discover -s tests` 66개 통과, nested Codex read-only smoke에서 Alpaca MCP `get_clock` 호출 성공.

## [2026-05-27 00:05 Asia/Seoul] hourly-autopilot | paper 자동 운영 gate 점검

- 사용자 승인에 따라 `harness/workflows/hourly-autopilot.md`를 실행했다.
- `.env`에서 `ALPACA_PAPER_TRADE=true`를 확인했고, API key 값은 출력하거나 기록하지 않았다.
- Alpaca MCP core `get_clock`, `get_account_info`, `get_orders`, `get_all_positions`, `get_account_activities`, `get_watchlists`, 후보 `get_stock_latest_quote`, `get_stock_snapshot`, `get_asset`, `get_news`는 usable했다.
- Alpaca market clock은 `2026-05-26T10:51:43-04:00` 기준 open이었고, open equity orders 0건, same-day fills 0건, current positions 10개를 확인했다.
- Alpaca core first blocking gate는 없고, 전체 첫 차단 gate는 `mcp_research_min_confirmations`이다.
- 62개 metadata universe와 `SPY`/`QQQ`를 스크리닝했다. pre-MCP shortlist는 `LRCX`, `SMH`, `ASML`, `AAPL`, `LLY`, final research candidates는 `AAPL`, `ASML`, `LLY`.
- 후보 quote는 fresh였다. `AAPL` 0.010%, `SMH` 0.060% spread는 통과했고 `LLY` 5.598%, `LRCX` 5.193%, `ASML` 0.562%는 spread gate 실패다.
- SEC EDGAR와 Yahoo Finance는 usable했지만 Alpha Vantage는 wrapper/schema data gap, FRED와 Firecrawl은 DNS gap으로 실패했다. research MCP usable count는 2라 최소 3에 미달했다.
- 검증: universe strict PASS, MCP strict FAIL, empty-order risk-check PASS.
- 리포트: `wiki/current-runs/daily/2026-05-26-2351-hourly-autopilot.md`.
- 원천: `wiki/evidence-store/sources/2026-05-26-2351-hourly-autopilot-sources.md`.
- run manifest: `wiki/evidence-store/run-manifests/2026-05-26-2351-hourly-autopilot.json`.
- order plan: `wiki/trade-ledger/orders/2026-05-26-2351-hourly-autopilot.json`.
- 실제 주문, 취소, 포지션 변경은 없었다. `orders_submitted=0`.

## [2026-05-27 00:24 Asia/Seoul] hourly-autopilot | paper 자동 운영 gate 점검

- run id: `2026-05-27-0012-hourly-autopilot`.
- 사용자 승인에 따라 `harness/workflows/hourly-autopilot.md`를 실행했다.
- `.env`에서 `ALPACA_PAPER_TRADE=true`를 확인했고, API key 값은 출력하거나 기록하지 않았다.
- Alpaca MCP core `get_clock`, `get_account_info`, `get_orders`, `get_all_positions`, `get_account_activities`, `get_watchlists`, 후보 `get_stock_latest_quote`, `get_stock_snapshot`, `get_asset`, `get_news`, `get_market_movers`, `get_most_active_stocks`는 usable했다.
- Market clock: `2026-05-26T11:14:12-04:00` 기준 open, next close `2026-05-26T16:00:00-04:00`.
- Account: portfolio value 101301.19 USD, cash 44030.58 USD, buying power 138895.81 USD, open US equity orders 0건, same-day fills 0건, current positions 10개.
- Universe: 62개 metadata universe와 `SPY`/`QQQ`를 스크리닝했다. Pre-MCP shortlist는 `ASML`, `LLY`, `AAPL`, `SMH`, `FCX`, final candidates는 `ASML`, `LLY`, `AAPL`.
- Candidate quote/spread: `ASML`, `LLY`, `AAPL`, `SMH`, `FCX`는 fresh quote와 spread gate를 통과했다. `AMD`, `KLAC`, `AMAT`, `LRCX`, `MU`는 spread fail로 skip했다.
- SEC EDGAR와 Yahoo Finance는 usable했다. Alpha Vantage는 `TOOL_LIST` -> `TOOL_GET` 후 `TOOL_CALL`이 cancelled, FRED/Firecrawl은 DNS failure로 gap 분류했다. Research MCP usable count는 2라 최소 3에 미달했다.
- First blocking gate: `mcp_research_min_confirmations`.
- 검증: universe strict PASS, MCP strict FAIL, empty-order risk-check PASS.
- submitted orders: 없음. skipped orders: `ASML`, `LLY`, `AAPL`, `SMH`, `FCX`, `AMD`, `KLAC`, `AMAT`, `LRCX`, `MU`, 보유 전 종목 sell.
- 리포트: `wiki/current-runs/daily/2026-05-27-0012-hourly-autopilot.md`.
- 원천: `wiki/evidence-store/sources/2026-05-27-0012-hourly-autopilot-sources.md`.
- run manifest: `wiki/evidence-store/run-manifests/2026-05-27-0012-hourly-autopilot.json`.
- order plan: `wiki/trade-ledger/orders/2026-05-27-0012-hourly-autopilot.json`.
- review due markers: 2026-05-22 체결분은 계속 `회고 대기`; 이번 run 신규 fill 없음.
- 실제 주문, 취소, 포지션 변경은 없었다. `orders_submitted=0`.

## [2026-05-27 00:43 Asia/Seoul] hourly-autopilot | paper 자동 운영 gate 점검

- run id: `2026-05-27-0032-hourly-autopilot`.
- 사용자 승인에 따라 `harness/workflows/hourly-autopilot.md`를 실행했다.
- `.env`에서 `ALPACA_PAPER_TRADE=true`를 확인했고, API key 값은 출력하거나 기록하지 않았다.
- Alpaca MCP core `get_clock`, `get_account_info`, `get_orders`, `get_all_positions`, `get_account_activities`, `get_watchlists`, 후보 `get_stock_latest_quote`, `get_stock_snapshot`, `get_stock_bars`, `get_asset`, `get_news`, `get_market_movers`, `get_most_active_stocks`는 usable했다.
- Market clock: `2026-05-26T11:33:01-04:00` 기준 open, next close `2026-05-26T16:00:00-04:00`.
- Account: portfolio value 101264.45 USD, cash 44030.58 USD, buying power 138855.03 USD, open US equity orders 0건, same-day fills 0건, current positions 10개.
- Universe: 62개 metadata universe와 `SPY`/`QQQ`를 스크리닝했다. Pre-MCP shortlist는 `MU`, `AMD`, `KLAC`, `SMH`, `INTC`, `AAPL`, `LLY`, `NOK`, `ASML`, `AMAT`, final candidates는 `LLY`, `AMD`, `MU`.
- Candidate quote/spread: `LLY`, `AMD`, `MU`, `SMH`, `INTC`, `AAPL`, `NOK`는 fresh quote와 spread gate를 통과했다. `KLAC`, `ASML`, `AMAT`, `LRCX`, `ETN`은 spread fail로 skip했다.
- SEC EDGAR와 Yahoo Finance는 usable했다. Alpha Vantage는 `TOOL_LIST` -> `TOOL_GET` 후 `TOOL_CALL`이 cancelled, FRED/Firecrawl은 DNS failure로 gap 분류했다. Research MCP usable count는 2라 최소 3에 미달했다.
- First blocking gate: `mcp_research_min_confirmations`.
- 검증: universe strict PASS, MCP strict FAIL, empty-order risk-check PASS.
- submitted orders: 없음. skipped orders: `LLY`, `AMD`, `MU`, `SMH`, `INTC`, `AAPL`, `KLAC`, `ASML`, `AMAT`, `LRCX`, 보유 전 종목 sell.
- 리포트: `wiki/current-runs/daily/2026-05-27-0032-hourly-autopilot.md`.
- 원천: `wiki/evidence-store/sources/2026-05-27-0032-hourly-autopilot-sources.md`.
- run manifest: `wiki/evidence-store/run-manifests/2026-05-27-0032-hourly-autopilot.json`.
- order plan: `wiki/trade-ledger/orders/2026-05-27-0032-hourly-autopilot.json`.
- review due markers: 2026-05-22 체결분은 계속 `회고 대기`; 이번 run 신규 fill 없음.
- 실제 주문, 취소, 포지션 변경은 없었다. `orders_submitted=0`.

## [2026-05-27 01:04 Asia/Seoul] hourly-autopilot | paper validation LLY 주문 체결

- run id: `2026-05-27-0052-hourly-autopilot`.
- 사용자 승인에 따라 `harness/workflows/hourly-autopilot.md`를 실행했다.
- `.env`에서 `ALPACA_PAPER_TRADE=true`를 확인했고, API key 값은 출력하거나 기록하지 않았다.
- Alpaca MCP core `get_clock`, `get_account_info`, `get_orders`, `get_all_positions`, `get_account_activities`, `get_watchlists`, 후보 `get_stock_latest_quote`, `get_stock_snapshot`, `get_asset`, `get_news`, `get_stock_bars`, `get_most_active_stocks`를 사용했다. Positions와 LLY asset은 각각 첫 시도 cancelled 후 retry pass였다.
- Market clock: `2026-05-26T12:00:39-04:00` 기준 open, next close `2026-05-26T16:00:00-04:00`.
- Account before order: portfolio value 101003.86 USD, cash 44030.58 USD, buying power 138599.44 USD, open US equity orders 0건, same-day fills 0건, current positions 10개.
- Universe: 62개 metadata universe와 `SPY`/`QQQ`를 스크리닝했다. Pre-MCP shortlist는 `MU`, `AMD`, `LLY`, `NOK`, `FCX`, `SMH`, `INTC`, `AAPL`, `LRCX`, `NVDA`, final candidates는 `LLY`, `FCX`, `NOK`.
- Candidate quote/spread: `LLY`, `FCX`, `NOK`, `SMH`, `AAPL`, `MU`, `NVDA`는 fresh quote와 spread gate를 통과했다. `AMD`, `LRCX`, `INTC`는 spread fail로 skip했다.
- SEC EDGAR는 local CIK cache로 `LLY -> 0000059478` 확인 후 company info/recent filings pass. Yahoo Finance는 LLY news/recommendations pass. FRED는 scheduler preflight `2026-05-27-0051-hourly-autopilot-research-mcp-preflight.json`의 `get_macro_snapshot` pass를 usable evidence로 사용했다.
- Alpha Vantage는 `TOOL_LIST` -> `TOOL_GET("PING")` 후 `TOOL_CALL("PING", {})`이 cancelled 되어 `gap_category=cancelled`로 기록했다. Firecrawl은 Codex tool catalog에 registered MCP tool이 노출되지 않아 `gap_category=wrapper_error`로 기록했고 shell/curl/local wrapper는 호출하지 않았다.
- First blocking gate: 없음. 검증: universe strict PASS, MCP strict PASS, risk-check PASS.
- 제출: LLY 1주 day limit buy, limit 1079.78, client_order_id `hourly-20260527-0052-lly-buy-1`. 첫 submit attempt는 MCP safety wrapper cancelled, 동일 idempotent client_order_id retry로 제출 성공.
- Post-trade: Alpaca order id `f2626164-9d01-4134-97ab-5e73748fc790`, status filled, filled_qty 1, filled_avg_price 1079.38, filled_at `2026-05-26T16:02:35.719698Z`. `get_all_positions`에서 LLY 1주 포지션 확인. `get_account_activities`는 즉시 조회에서 fill row 0건이었으나 order/position endpoint로 체결 확인.
- submitted orders: `LLY` 1주. skipped orders: `FCX`, `NOK`, `MU`, `AMD`, `LRCX`, `INTC`, 보유 전 종목 sell/trim.
- 리포트: `wiki/current-runs/daily/2026-05-27-0052-hourly-autopilot.md`.
- 원천: `wiki/evidence-store/sources/2026-05-27-0052-hourly-autopilot-sources.md`.
- run manifest: `wiki/evidence-store/run-manifests/2026-05-27-0052-hourly-autopilot.json`.
- order plan: `wiki/trade-ledger/orders/2026-05-27-0052-hourly-autopilot.json`.
- review due markers: 신규 LLY fill은 1D/5D/20D `회고 대기`; 2026-05-22 체결분도 계속 `회고 대기`.

## [2026-05-27 01:19 Asia/Seoul] ui | dashboard 자동 갱신 누락 수정

- 증상: hourly/analyst scheduled run은 wiki 산출물을 자동 commit/push했지만 `ui/agent-dashboard.html`은 재생성 및 autopush 대상에서 빠져 dashboard가 최신 run을 반영하지 못할 수 있었다.
- 수정: `scripts/run-hourly-autopilot-codex.sh`와 `scripts/run-analyst-review-codex.sh`가 성공 후 `scripts/build-agent-dashboard.py`를 실행하도록 변경했다.
- 수정: `scripts/git-autopush-artifacts.sh`의 trackable artifact 경로에 `ui/agent-dashboard.html`과 `ui/backtests`를 추가했다.
- 재생성: `python3 scripts/build-agent-dashboard.py`로 현재 dashboard를 `2026-05-27-0052-hourly-autopilot` 및 LLY 1주 포지션 반영 상태로 갱신했다.
- 검증: dashboard embedded JSON parse와 렌더 스크립트 fake-DOM 실행 pass, `bash -n` pass, `python3 -m unittest discover -s tests` 67개 pass.

## [2026-05-27 01:24 Asia/Seoul] ui | hourly dashboard 회색 fallback 수정

- 증상: 최신 hourly report가 `추천 Shortlist` 형식을 쓰지만 dashboard 파서는 예전 `추천 조치`, `Trend Agent` 섹션만 읽어 Today 추천과 일부 agent status가 회색/빈 값으로 표시됐다.
- 증상: `wiki/trade-ledger/positions/current.md`에 `총 수익`, `총 수익률` 행이 없어 Alpaca Paper 총수익 카드가 `-`로 표시됐다.
- 수정: `scripts/build-agent-dashboard.py`가 `추천 Shortlist`를 Today pick으로 normalize하고, manifest/order-plan 근거로 agent status를 완료 판정하며, 포지션별 미실현 손익을 합산해 총수익/총수익률을 계산하도록 변경했다.
- 재생성: `ui/agent-dashboard.html`은 Today `LLY`, `FCX`, `NOK`, 총수익 `+1239.44 USD`, 총수익률 `+2.17%`, waiting status 0개 상태로 갱신됐다.
- 검증: dashboard embedded JSON parse와 렌더 스크립트 fake-DOM 실행 pass, `bash -n` pass, `python3 -m unittest discover -s tests` 67개 pass.

## [2026-05-27 01:29 Asia/Seoul] ui | 추천 점수 표시 라벨 수정

- 증상: dashboard Today 카드가 `추천 Shortlist`의 순위 값을 실제 점수처럼 `점수 1 · shortlist`로 표시해 추천 점수처럼 오해될 수 있었다.
- 수정: `scripts/build-agent-dashboard.py`가 order-plan의 `confidence_score`가 있는 제출 후보는 `신뢰 62%`로 표시하고, shortlist-only 후보는 `순위 #2`, `순위 #3`처럼 표시하도록 분리했다.
- 수정: 주문 후보 chip은 `20D 기대 +3.0%`, `불리 -7.5%`처럼 order-plan의 기대/불리 이동 값을 사용한다.
- 재생성: `ui/agent-dashboard.html`에서 `점수 1` 표시는 사라지고 `LLY 신뢰 62%`, `FCX 순위 #2`, `NOK 순위 #3`로 표시된다.
- 검증: dashboard embedded JSON parse와 렌더 스크립트 fake-DOM 실행 pass, `bash -n` pass, `python3 -m unittest discover -s tests` 67개 pass.

## [2026-05-27 01:43 Asia/Seoul] hourly-autopilot | paper 자동 운영 gate 점검

- run id: `2026-05-27-0131-hourly-autopilot`.
- 사용자 승인에 따라 `harness/workflows/hourly-autopilot.md`를 실행했다.
- `.env`에서 `ALPACA_PAPER_TRADE=true`를 확인했고, API key 값은 출력하거나 기록하지 않았다.
- Alpaca MCP core `get_clock`, `get_account_info`, `get_orders`, `get_all_positions`, `get_account_activities`, `get_watchlists`, 후보 `get_stock_latest_quote`, `get_stock_snapshot`, `get_stock_bars`, `get_asset`, `get_news`, `get_market_movers`, `get_most_active_stocks`를 사용했다.
- Market clock: `2026-05-26T12:32:08-04:00` 기준 open, next close `2026-05-26T16:00:00-04:00`.
- Account: portfolio value 101605.13 USD, cash 42951.20 USD, buying power 137932.33 USD, open US equity orders 0건, same-day fills 1건 LLY buy 1주, current positions 11개.
- Universe: 62개 metadata universe와 `SPY`/`QQQ`를 스크리닝했다. Pre-MCP shortlist는 `MU`, `NOK`, `FCX`, `SMH`, `AMD`, `INTC`, `AAPL`, `AVGO`, `PLTR`, `NVDA`, final candidates는 `FCX`, `NOK`, `SMH`.
- Candidate quote/spread: `FCX`, `NOK`, `SMH`, `MU`, `AAPL`, `NVDA`, `AVGO`, `INTC`, `PLTR`는 fresh quote와 spread gate를 통과했다. `AMD`, `LLY`는 spread fail로 skip했다.
- SEC EDGAR는 local CIK cache로 `FCX -> 0000831259` 확인 후 company info/recent filings pass. Yahoo Finance는 FCX news pass. FRED는 scheduler preflight `2026-05-27-0131-hourly-autopilot-research-mcp-preflight.json`의 `get_macro_snapshot` pass를 usable evidence로 사용했다.
- Alpha Vantage는 `TOOL_LIST` -> `TOOL_GET("PING")` 후 `TOOL_CALL("PING", {})`이 cancelled 되어 `gap_category=cancelled`로 기록했다. Firecrawl은 Codex tool catalog에 registered MCP tool이 노출되지 않아 `gap_category=wrapper_error`로 기록했고 shell/curl/local wrapper는 호출하지 않았다.
- First blocking gate: 없음. 검증 및 제출 결과는 같은 run entry의 후속 업데이트로 기록한다.
- 리포트: `wiki/current-runs/daily/2026-05-27-0131-hourly-autopilot.md`.
- 원천: `wiki/evidence-store/sources/2026-05-27-0131-hourly-autopilot-sources.md`.
- run manifest: `wiki/evidence-store/run-manifests/2026-05-27-0131-hourly-autopilot.json`.
- order plan: `wiki/trade-ledger/orders/2026-05-27-0131-hourly-autopilot.json`.
- 검증: universe strict PASS, MCP strict PASS, risk-check PASS.
- 제출 전 fresh quote 재확인: FCX bid 63.95, ask 63.97, spread 0.031%, quote time `2026-05-26T16:40:36Z`. Open US equity orders 0건.
- 제출: FCX 1주 day limit buy, limit 63.97, client_order_id `hourly-20260527-0131-fcx-buy-1`.
- Post-trade: Alpaca order id `6c6a31ab-2a07-4da1-9e2e-c1dfb57ccee1`, status filled, filled_qty 1, filled_avg_price 63.94, filled_at `2026-05-26T16:41:44.795047598Z`. `get_all_positions`에서 FCX 1주 포지션 확인.
- Reconciliation gap: `get_order_by_client_id`, `get_order_by_id`, 일부 `get_orders`/`get_all_positions`, `get_account_activities` 호출은 cancelled 또는 safety cancellation이 있었고, 같은 주문 id 기준의 `get_orders` retry와 positions retry로 체결 확인했다.
- submitted orders: `FCX` 1주. skipped orders: `NOK`, `SMH`, `MU`, `AMD`, `LLY`, `AAPL`, `NVDA`, `AVGO`, `INTC`, `PLTR`, 보유 전 종목 sell/trim.
- review due markers: 신규 FCX fill은 1D/5D/20D `회고 대기`; LLY 및 2026-05-22 체결분도 계속 `회고 대기`.

## [2026-05-27 01:50 Asia/Seoul] policy | paper autopilot 적극 운용 및 20분 주기 전환

- 사용자 요청에 따라 `harness/recommendation-policy.yaml`을 `v1.7`로 올리고 `long_term_quality_momentum_v1`을 `auto_eligible_paper` / `auto_orders_allowed=true`로 승격했다. 이는 paper validation 전용이며 live/production 거래는 계속 금지한다.
- 매수 쪽은 hard gate 유지 조건에서 run당 최대 신규 buy 3개, validation notional 일일 6%, second/third slot cash floor, cluster 분산, confidence tier를 명시했다.
- 매도/trim 쪽은 `risk_trim_policy.active_trim_triggers`에 포지션 과대, 테마/팩터/cluster 경고, overheat reversal, stale thesis underperformance, speculative loss control 기준을 수치화했다.
- 스케줄은 launchd `StartCalendarInterval`을 미국 정규장과 겹칠 수 있는 KST 시간대의 20분 후보 슬롯으로 바꾸고, wrapper가 Alpaca MCP `get_clock.is_open=true`를 확인한 경우에만 research preflight/nested Codex/wiki/order planning을 시작하도록 변경했다. `22:31 KST` run은 계속 미국 정규장 market-open validation run이다.
- 장외 wakeup은 `scripts/check-alpaca-market-open-mcp.py`에서 fail-closed로 종료하며, 장외에는 report/manifest/order plan을 만들지 않는다.
- 문서/검증: `harness/workflows/hourly-autopilot.md`, `scheduler/README.md`, `README.md`, `wiki/index.md`, 관련 schema/test를 함께 갱신했다.

## [2026-05-27 02:06 Asia/Seoul] hourly-autopilot | paper 자동 운영 gate 점검

- run id: `2026-05-27-0159-hourly-autopilot`.
- 사용자 승인에 따라 `harness/workflows/hourly-autopilot.md`를 실행했다.
- `.env`에서 `ALPACA_PAPER_TRADE=true`를 확인했고, API key 값은 출력하거나 기록하지 않았다.
- Alpaca MCP `get_clock`은 `2026-05-26T13:00:24.142399574-04:00` 기준 open을 반환했다. `get_account_activities`, 후보 `get_stock_latest_quote`, `get_stock_bars`, `get_news`는 usable했다.
- Alpaca MCP `get_account_info`는 2회 cancelled, `get_all_positions`는 2회 cancelled, `get_orders(status=open)`는 2회 cancelled였다. `get_watchlists`, `get_stock_snapshot`, `get_stock_latest_trade`, `get_asset`도 cancelled였다. 첫 Alpaca core blocking gate는 `alpaca_account`다.
- Universe: 62개 metadata universe와 `SPY`/`QQQ`를 포함했다. Watchlist는 Alpaca cancellation 때문에 추가하지 못했다. Pre-MCP shortlist는 `NOK`, `SMH`, `FCX`, `NVDA`, `AAPL`, `INTC`, `MU`, `LLY`, `AVGO`, `PLTR`, final candidates는 `NOK`, `SMH`, `FCX`.
- Candidate quote/spread: `NOK`, `SMH`, `FCX`, `NVDA`, `AAPL`, `INTC`는 fresh quote와 spread gate를 통과했다. `MU`, `LLY`, `AVGO`, `PLTR`는 spread fail이다.
- SEC EDGAR는 local CIK cache로 `NOK -> 0000924613` 확인 후 company info/recent filings pass. Yahoo Finance는 NOK news/recommendations pass. FRED는 scheduler preflight `2026-05-27-0159-hourly-autopilot-research-mcp-preflight.json`의 `get_macro_snapshot` pass를 usable evidence로 사용했다.
- Alpha Vantage는 `TOOL_LIST` -> `TOOL_GET("PING")` -> `TOOL_CALL("PING", {})` pass 후 `TOOL_GET("NEWS_SENTIMENT")` 직후 첫 candidate `TOOL_CALL`이 cancelled되어 `gap_category=cancelled`로 기록하고 retry를 중단했다. Firecrawl은 Codex tool catalog에 registered MCP tool이 노출되지 않아 `gap_category=wrapper_error`로 기록했다.
- 검증: universe strict PASS, MCP strict FAIL, empty-order risk-check PASS.
- submitted orders: 없음. skipped orders: 모든 buy/sell 후보. 이유는 Alpaca account/order/position/asset core gate 미확정 및 MCP strict fail.
- 리포트: `wiki/current-runs/daily/2026-05-27-0159-hourly-autopilot.md`.
- 원천: `wiki/evidence-store/sources/2026-05-27-0159-hourly-autopilot-sources.md`.
- run manifest: `wiki/evidence-store/run-manifests/2026-05-27-0159-hourly-autopilot.json`.
- order plan: `wiki/trade-ledger/orders/2026-05-27-0159-hourly-autopilot.json`.
- review due markers: LLY/FCX 및 2026-05-22 체결분은 계속 `회고 대기`; 이번 run 신규 fill 없음.

## [2026-05-27 02:24 Asia/Seoul] hourly-autopilot | paper validation NOK 주문 체결

- run id: `2026-05-27-0211-hourly-autopilot`.
- 사용자 승인에 따라 `harness/workflows/hourly-autopilot.md`를 실행했다.
- `.env`에서 `ALPACA_PAPER_TRADE=true`를 확인했고, API key 값은 출력하거나 기록하지 않았다.
- Alpaca MCP core `get_clock`, `get_account_info`, `get_orders`, `get_all_positions`, `get_account_activities`, `get_watchlists`, 후보 `get_stock_latest_quote`, `get_asset`, `get_news`, `get_stock_bars`를 사용했다.
- Market clock: `2026-05-26T13:20:55.139534731-04:00` 기준 open, next close `2026-05-26T16:00:00-04:00`.
- Account before order: portfolio value 101680.85 USD, cash 42887.26 USD, buying power 137946.11 USD, open US equity orders 0건, same-day fills 2건 LLY/FCX buy, current positions 12개.
- Universe: 62개 metadata universe와 `SPY`/`QQQ`를 스크리닝했다. Pre-MCP shortlist는 `NOK`, `SMH`, `FCX`, `NVDA`, `AAPL`, `AMD`, `MU`, `INTC`, `LLY`, `PLTR`, final candidates는 `NOK`, `SMH`, `NVDA`.
- Candidate quote/spread: pre-submit NOK quote bid 16.50, ask 16.51, spread 0.0606%, quote time `2026-05-26T17:20:40.787261Z`.
- SEC EDGAR는 local CIK cache로 `NOK -> 0000924613` 확인 후 company info/recent filings pass. Alpha Vantage는 `TOOL_LIST` -> `TOOL_GET("PING")` -> `TOOL_CALL("PING", {})` -> `TOOL_GET("NEWS_SENTIMENT")` -> `TOOL_CALL("NEWS_SENTIMENT")` pass. FRED는 scheduler preflight `2026-05-27-0211-hourly-autopilot-research-mcp-preflight.json`의 `get_macro_snapshot` pass를 usable evidence로 사용했다.
- Firecrawl은 Codex tool catalog에 registered MCP tool이 노출되지 않아 `gap_category=wrapper_error`로 기록했고 shell/curl/local wrapper는 호출하지 않았다. Yahoo Finance registered MCP call은 wrapper cancelled로 `gap_category=cancelled` 기록했다.
- First blocking gate: 없음. 검증: universe strict PASS, MCP strict PASS, risk-check PASS.
- 제출 전 gate summary: paper mode, market clock, order plan, universe/MCP/risk validator, quote freshness/spread, order shape, duplicate/open-order check, source refs를 plain text로 기록했다.
- 제출: NOK 1주 day limit buy, limit 16.51, client_order_id `hourly-20260527-0211-nok-buy-1`.
- Post-trade: Alpaca order id `63e51a21-cbff-429c-82dc-9651d9756426`, status filled, filled_qty 1, filled_avg_price 16.50, filled_at `2026-05-26T17:21:49.961677153Z`. `get_all_positions`에서 NOK 401주 포지션 확인.
- Reconciliation gap: `get_order_by_client_id`와 post-fill `get_account_info`는 wrapper cancelled였고, `get_orders`, `get_account_activities`, `get_all_positions`로 체결/포지션을 확인했다.
- submitted orders: `NOK` 1주. skipped orders: `SMH`, `NVDA`, `AMD`, `MU`, `INTC`는 cluster/slot 우선순위, `FCX`/`LLY`는 같은 거래일 buy duplicate 회피.
- 리포트: `wiki/current-runs/daily/2026-05-27-0211-hourly-autopilot.md`.
- 원천: `wiki/evidence-store/sources/2026-05-27-0211-hourly-autopilot-sources.md`.
- run manifest: `wiki/evidence-store/run-manifests/2026-05-27-0211-hourly-autopilot.json`.
- order plan: `wiki/trade-ledger/orders/2026-05-27-0211-hourly-autopilot.json`.
- review due markers: 신규 NOK fill은 1D/5D/20D `회고 대기`; LLY/FCX 및 2026-05-22 체결분도 계속 `회고 대기`.

## [2026-05-27 02:35 Asia/Seoul] hourly-autopilot | paper validation NVDA 주문 체결

- run id: `2026-05-27-0226-hourly-autopilot`.
- 사용자 승인에 따라 `harness/workflows/hourly-autopilot.md`를 실행했다.
- `.env`에서 `ALPACA_PAPER_TRADE=true`를 확인했고, API key 값은 출력하거나 기록하지 않았다.
- Scheduler-owned Alpaca core preflight `wiki/evidence-store/sources/2026-05-27-0226-hourly-autopilot-alpaca-core-preflight.json`을 먼저 읽었다. Hard gate pass, market open, account/positions/open orders/fills/watchlists/asset/quotes/snapshots/latest trades 모두 pass로 기록되어 Alpaca core evidence로 사용했다.
- Market clock: `2026-05-26T13:26:42.969065887-04:00` 기준 open, next close `2026-05-26T16:00:00-04:00`.
- Account before order: portfolio value 101643.29 USD, cash 42870.76 USD, buying power 137899.56 USD, open US equity orders 0건, same-day fills 3건 LLY/FCX/NOK buy, current positions 12개.
- Universe: 62개 metadata universe와 `SPY`/`QQQ`를 스크리닝했다. Pre-MCP shortlist는 `NVDA`, `SMH`, `AAPL`, `INTC`, `MU`, `AMD`, `PLTR`, `FCX`, `NOK`, `LLY`, final candidates는 `NVDA`, `SMH`, `AAPL`.
- Candidate quote/spread: `NVDA` bid 213.48, ask 213.72, spread 0.1124%, quote time `2026-05-26T17:27:05.819127537Z`. `MU`는 spread 0.846%로 skip했고, `FCX`/`NOK`/`LLY`는 같은 거래일 buy duplicate 회피로 skip했다.
- SEC EDGAR는 local CIK cache로 `NVDA -> 0001045810` 확인 후 company info/recent filings pass. Yahoo Finance는 NVDA news/recommendations pass. FRED는 scheduler preflight `2026-05-27-0226-hourly-autopilot-research-mcp-preflight.json`의 `get_macro_snapshot` pass를 usable evidence로 사용했다.
- Alpha Vantage는 `TOOL_LIST` pass, `TOOL_GET("PING")` 첫 시도 cancelled 후 retry pass, `TOOL_CALL("PING", {})` cancelled로 health check가 막혀 `gap_category=cancelled`로 기록하고 후보 데이터 호출을 중단했다. Firecrawl은 Codex tool catalog에 registered MCP tool이 노출되지 않아 `gap_category=wrapper_error`로 기록했고 shell/curl/local wrapper는 호출하지 않았다.
- First blocking gate: 없음. 검증: universe strict PASS, MCP strict PASS, risk-check PASS.
- 제출 전 gate summary: paper mode, market clock, order plan, universe/MCP/risk validator, quote freshness/spread, order shape, duplicate/open-order check, source refs를 plain text로 기록했다.
- 제출: NVDA 1주 day limit buy, limit 213.72, client_order_id `hourly-20260527-0226-nvda-buy-1`.
- Post-trade: Alpaca order id `e4c49769-2341-404e-8ee9-15a20809bdfd`, status filled, filled_qty 1, filled_avg_price 213.72, filled_at `2026-05-26T17:34:00.662457Z`. `get_orders(status=open)`은 open orders 0건을 반환했다.
- Reconciliation gap: `get_order_by_client_id`, post-fill `get_all_positions`, post-fill `get_account_activities`는 wrapper cancelled였고, `get_orders(status=all, symbols=NVDA)`로 같은 client_order_id/order_id의 fill을 확인했다.
- submitted orders: `NVDA` 1주. skipped orders: `SMH`, `AAPL`, `INTC`는 recheck, `MU`는 spread fail, `FCX`/`NOK`/`LLY`는 same-day duplicate buy 회피.
- 리포트: `wiki/current-runs/daily/2026-05-27-0226-hourly-autopilot.md`.
- 원천: `wiki/evidence-store/sources/2026-05-27-0226-hourly-autopilot-sources.md`.
- run manifest: `wiki/evidence-store/run-manifests/2026-05-27-0226-hourly-autopilot.json`.
- order plan: `wiki/trade-ledger/orders/2026-05-27-0226-hourly-autopilot.json`.
- review due markers: 신규 NVDA fill은 1D/5D/20D `회고 대기`; LLY/FCX/NOK 및 2026-05-22 체결분도 계속 `회고 대기`.

## [2026-05-27 02:38 Asia/Seoul] automation-maintenance | Alpaca MCP core preflight 안정화

- `scripts/fetch-alpaca-core-preflight.py`를 추가해 scheduled autopilot이 nested Codex 진입 전에 Alpaca MCP read-only core evidence를 캡처하도록 했다.
- 대상 도구는 `get_clock`, `get_account_info`, `get_all_positions`, `get_orders(status=open)`, `get_account_activities(FILL)`, `get_watchlists`, `get_asset`, `get_stock_latest_quote`, `get_stock_snapshot`, `get_stock_latest_trade`다. 주문 제출/교체/취소/청산 및 Alpaca REST 직접 호출은 하지 않는다.
- `scripts/run-hourly-autopilot-codex.sh`는 preflight JSON을 nested prompt에 전달하고, hard gate pass 및 fresh quote rows를 Alpaca MCP evidence로 사용하도록 바꿨다. 누락/실패/stale row만 registered Codex MCP tool로 1회 재시도한다.
- nested Codex timeout 기본값을 900초로 줄여 20분 cadence를 오래 점유하지 않게 했다.
- 직접 검증: `manual-validate-2026-05-27` read-only Alpaca core preflight PASS, market open true, 62 symbols, first blocking gate 없음.
- 자동화 검증: `python3 -m unittest discover -s tests` 69개 PASS, `bash -n scripts/run-hourly-autopilot-codex.sh` PASS, `plutil -lint scheduler/com.insightque.stock-alpaca.hourly-autopilot.plist.example` PASS.
- launchd 확인: 실제 LaunchAgent는 22:31부터 05:51 KST까지 20분 단위 calendar interval로 로드되어 있고, 상태는 not running, last exit code 0이다.

## [2026-05-27 03:00 Asia/Seoul] hourly-autopilot | paper validation AAPL 주문 제출

- run id: `2026-05-27-0251-hourly-autopilot`.
- 사용자 승인에 따라 `harness/workflows/hourly-autopilot.md`를 실행했다.
- `.env`에서 `ALPACA_PAPER_TRADE=true`를 확인했고, API key 값은 출력하거나 기록하지 않았다.
- Scheduler-owned Alpaca core preflight `wiki/evidence-store/sources/2026-05-27-0251-hourly-autopilot-alpaca-core-preflight.json`을 먼저 읽었다. Hard gate pass, market open, account/positions/open orders/fills/watchlists/asset/quotes/snapshots/latest trades 모두 pass로 기록되어 Alpaca core evidence로 사용했다.
- Market clock: preflight `2026-05-26T13:51:08.757165289-04:00` open, submit 전 refresh `2026-05-26T13:58:37.983877701-04:00` open, next close `2026-05-26T16:00:00-04:00`.
- Account before order: portfolio value 101662.85 USD, cash 42657.04 USD, buying power 137687.35 USD, open US equity orders 0건, same-day fills 4건 LLY/FCX/NOK/NVDA buy, current positions 12개.
- Universe: 62개 metadata universe와 `SPY`/`QQQ`를 스크리닝했다. Pre-MCP shortlist는 `MU`, `NOK`, `AMD`, `KLAC`, `SMH`, `FCX`, `AAPL`, `INTC`, `AMZN`, `PLTR`, final candidates는 `AAPL`, `SMH`, `INTC`.
- Candidate quote/spread: submit 직전 AAPL quote bid 309.43, ask 309.46, spread 0.0097%, quote time `2026-05-26T17:56:03.094445033Z`.
- SEC EDGAR는 local CIK cache로 `AAPL -> 0000320193` 확인 후 company info/recent filings pass. Yahoo Finance는 AAPL news/recommendations pass. FRED는 scheduler preflight `2026-05-27-0251-hourly-autopilot-research-mcp-preflight.json`의 `get_macro_snapshot` pass를 usable evidence로 사용했다.
- Alpha Vantage는 `TOOL_LIST` -> `TOOL_GET("PING")` -> `TOOL_CALL("PING", {})` pass 후 `TOOL_GET("NEWS_SENTIMENT")`가 cancelled되어 candidate data call을 중단했고 `gap_category=cancelled`로 기록했다. Firecrawl은 Codex tool catalog에 registered MCP tool이 노출되지 않아 `gap_category=wrapper_error`로 기록했고 shell/curl/local wrapper는 호출하지 않았다.
- First blocking gate: 없음. 검증: universe strict PASS, MCP strict PASS, risk-check PASS.
- 제출 전 gate summary: paper mode, market clock, order plan, universe/MCP/risk validator, quote freshness/spread, order shape, duplicate/open-order check, source refs를 plain text로 기록했다.
- 제출: AAPL 1주 day limit buy, limit 309.46, client_order_id `hourly-20260527-0251-aapl-buy-1`. 첫 submit call은 cancelled였고, `get_orders(status=all, symbols=AAPL)` 및 `get_all_positions`에서 같은 client id/order/position이 없음을 확인한 뒤 같은 client id로 1회 재시도했다.
- Post-trade: Alpaca order id `dda2173a-f512-4ee1-80a9-7e99a4bdfd7c`, status `new`, filled_qty 0, submitted_at `2026-05-26T18:00:09.297012573Z`. `get_orders(status=open, symbols=AAPL)`에서 open order 확인, `get_account_activities(FILL, after=17:55Z)`는 신규 fill 0건, `get_all_positions`는 AAPL position 없음.
- Reconciliation gap: post-submit `get_account_info`는 MCP wrapper safety cancellation으로 `gap_category=cancelled` 기록했다.
- submitted orders: `AAPL` 1주 open order. skipped orders: `SMH`, `INTC`, `AMZN`은 recheck, `MU`는 spread fail, `FCX`/`NOK`/`NVDA`/`LLY`는 same-day duplicate buy 회피.
- 리포트: `wiki/current-runs/daily/2026-05-27-0251-hourly-autopilot.md`.
- 원천: `wiki/evidence-store/sources/2026-05-27-0251-hourly-autopilot-sources.md`.
- run manifest: `wiki/evidence-store/run-manifests/2026-05-27-0251-hourly-autopilot.json`.
- order plan: `wiki/trade-ledger/orders/2026-05-27-0251-hourly-autopilot.json`.
- post-trade snapshot: `wiki/trade-ledger/positions/current.md`.
- review due markers: AAPL은 open order라 아직 fill review due가 아님. LLY/FCX/NOK/NVDA 및 2026-05-22 체결분은 계속 `회고 대기`.

## [2026-05-27 03:14 Asia/Seoul] hourly-autopilot | research MCP gate 실패로 주문 없음

- run id: `2026-05-27-0311-hourly-autopilot`.
- 사용자 승인에 따라 `harness/workflows/hourly-autopilot.md`를 실행했다.
- `.env`에서 `ALPACA_PAPER_TRADE=true`를 확인했고, API key 값은 출력하거나 기록하지 않았다.
- Scheduler-owned Alpaca core preflight `wiki/evidence-store/sources/2026-05-27-0311-hourly-autopilot-alpaca-core-preflight.json`을 먼저 읽었다. Hard gate pass, market open, account/positions/open orders/fills/watchlists/asset/quotes/snapshots/latest trades 모두 pass로 기록되어 Alpaca core evidence로 사용했다.
- Market clock: `2026-05-26T14:11:10.836217373-04:00` 기준 open, next close `2026-05-26T16:00:00-04:00`.
- Account before decision: portfolio value 101639.85 USD, cash 42657.04 USD, buying power 137384.96 USD, current positions 12개, open order 1건 AAPL buy `new`.
- Universe: 62개 metadata universe와 `SPY`/`QQQ`를 스크리닝했다. Pre-MCP shortlist는 `AMZN`, `INTC`, `SMH`, `AAPL`, `MU`, `NVDA`, `FCX`, `NOK`, `LLY`, `AMD`, final candidates는 `AMZN`, `INTC`, `SMH`.
- Candidate quote/spread: AMZN spread 0.0152%, INTC 0.0408%, SMH 0.0467%, AAPL 0.0097%, MU 0.4796%; quote rows are from `2026-05-26T18:11:34Z` to `2026-05-26T18:11:35Z`.
- SEC EDGAR는 local CIK cache로 `AMZN -> 0001018724`, `INTC -> 0000050863` 확인 후 MCP `get_financials`가 cancelled되어 `gap_category=cancelled`로 기록했다. `SMH`는 ETF로 local CIK lookup 공백이다.
- Alpha Vantage는 `TOOL_LIST` -> `TOOL_GET("PING")` -> `TOOL_CALL("PING", {})` pass 후 `TOOL_GET("NEWS_SENTIMENT")` 직후 첫 candidate `TOOL_CALL("NEWS_SENTIMENT")`이 cancelled되어 `gap_category=cancelled`로 기록하고 retry를 중단했다.
- FRED는 scheduler preflight `2026-05-27-0311-hourly-autopilot-research-mcp-preflight.json`의 `get_macro_snapshot` pass를 usable evidence로 사용했다. Yahoo Finance AMZN recommendations는 usable했다. Firecrawl은 Codex tool catalog에 registered MCP tool이 노출되지 않아 `gap_category=wrapper_error`로 기록했고 shell/curl/local wrapper는 호출하지 않았다.
- First blocking gate: `research_mcp_minimum_confirmations`. 검증: universe strict PASS, MCP strict FAIL, empty-order risk-check PASS.
- submitted orders: 없음. `place_stock_order` 호출 없음. skipped orders: 모든 buy/sell 후보. 이유는 research MCP usable/pass 2개로 submit 기준 3개 미달 및 기존 AAPL open order.
- 리포트: `wiki/current-runs/daily/2026-05-27-0311-hourly-autopilot.md`.
- 원천: `wiki/evidence-store/sources/2026-05-27-0311-hourly-autopilot-sources.md`.
- run manifest: `wiki/evidence-store/run-manifests/2026-05-27-0311-hourly-autopilot.json`.
- order plan: `wiki/trade-ledger/orders/2026-05-27-0311-hourly-autopilot.json`.
- review due markers: 이번 run 신규 fill 없음. AAPL order는 open `new`라 아직 fill review due가 아니며, LLY/FCX/NOK/NVDA 및 2026-05-22 체결분은 계속 `회고 대기`.

## [2026-05-27 03:35 Asia/Seoul] hourly-autopilot | paper mode gate 실패로 주문 없음

- run id: `2026-05-27-0331-hourly-autopilot`.
- 사용자 승인에 따라 `harness/workflows/hourly-autopilot.md`를 실행했다.
- nested Codex shell에서 `ALPACA_PAPER_TRADE=true`가 확인되지 않아 첫 hard blocking gate를 `paper_mode_env_missing`으로 기록했고, `place_stock_order`는 호출하지 않았다.
- Scheduler-owned Alpaca core preflight `wiki/evidence-store/sources/2026-05-27-0331-hourly-autopilot-alpaca-core-preflight.json`를 먼저 읽었다. Hard gate pass, market open, account/positions/open orders/fills/watchlists/asset/quotes/snapshots/latest trades pass를 Alpaca MCP evidence로 사용했다.
- Market clock: `2026-05-26T14:31:10.242063192-04:00` 기준 open, next close `2026-05-26T16:00:00-04:00`.
- Account before decision: portfolio value 101621.09 USD, cash 42657.04 USD, buying power 137380.24 USD, current positions 12개, open order 1건 AAPL buy `new`.
- Universe: 62개 metadata universe와 `SPY`/`QQQ`를 스크리닝했다. Pre-MCP shortlist는 `AMZN`, `INTC`, `SMH`, `AAPL`, `MU`, `NVDA`, `FCX`, `NOK`, `LLY`, `AMD`, final candidates는 `AMZN`, `INTC`, `SMH`.
- Candidate quote/spread: AMZN 0.0114%, INTC 0.0245%, SMH 0.0483%, quote rows are from `2026-05-26T18:31:31Z` to `2026-05-26T18:31:32Z`.
- SEC EDGAR는 local CIK cache로 `AMZN -> 0001018724`, `INTC -> 0000050863` 확인 후 registered MCP call이 cancelled되어 `gap_category=cancelled`로 기록했다. `SMH`는 ETF로 local CIK lookup 공백이다.
- Alpha Vantage는 `TOOL_LIST` -> `TOOL_GET("PING")` -> `TOOL_CALL("PING", {})` pass 후 `TOOL_GET("NEWS_SENTIMENT")` 직후 첫 candidate `TOOL_CALL("NEWS_SENTIMENT")`이 cancelled되어 `gap_category=cancelled`로 기록하고 retry를 중단했다.
- FRED는 scheduler preflight `wiki/evidence-store/sources/2026-05-27-0331-hourly-autopilot-research-mcp-preflight.json`의 `get_macro_snapshot` pass를 usable evidence로 사용했다. Yahoo Finance AMZN news는 usable했다. Firecrawl은 Codex tool catalog에 registered MCP tool이 노출되지 않아 `gap_category=wrapper_error`로 기록했고 shell/curl/local wrapper는 호출하지 않았다.
- First blocking gate: `paper_mode_env_missing`. 검증 결과 universe strict PASS, MCP strict FAIL, risk-check FAIL(AAPL open order age 34.8분 > lifecycle limit 30분).
- submitted orders: 없음. `place_stock_order` 호출 없음. skipped orders: 모든 buy/sell 후보. 이유는 nested paper-mode env 미확인 및 MCP strict fail.
- 리포트: `wiki/current-runs/daily/2026-05-27-0331-hourly-autopilot.md`.
- 원천: `wiki/evidence-store/sources/2026-05-27-0331-hourly-autopilot-sources.md`.
- run manifest: `wiki/evidence-store/run-manifests/2026-05-27-0331-hourly-autopilot.json`.
- order plan: `wiki/trade-ledger/orders/2026-05-27-0331-hourly-autopilot.json`.
- review due markers: 이번 run 신규 fill 없음. AAPL order는 open `new`라 아직 fill review due가 아니며, LLY/FCX/NOK/NVDA 및 2026-05-22 체결분은 계속 `회고 대기`.

## [2026-05-27 04:20 Asia/Seoul] hourly-autopilot | paper validation AMZN 주문 제출

- run id: `2026-05-27-0411-hourly-autopilot`.
- 사용자 승인에 따라 `harness/workflows/hourly-autopilot.md`를 실행했다.
- `.env`에서 `ALPACA_PAPER_TRADE=true`를 확인했고, API key 값은 출력하거나 기록하지 않았다.
- Scheduler-owned Alpaca core preflight `wiki/evidence-store/sources/2026-05-27-0411-hourly-autopilot-alpaca-core-preflight.json`을 먼저 읽었다. Hard gate pass, market open, account/positions/open orders/fills/watchlists/asset/quotes/snapshots/latest trades 모두 pass로 기록되어 Alpaca core evidence로 사용했다.
- Market clock: `2026-05-26T15:11:05.905788802-04:00` 기준 open, next close `2026-05-26T16:00:00-04:00`.
- Account before decision: portfolio value 101684.58 USD, cash 42347.59 USD, buying power 137455.77 USD, current positions 13개, open orders 0건.
- Universe: 62개 metadata universe와 `SPY`/`QQQ`를 스크리닝했다. Pre-MCP shortlist는 `MU`, `AMD`, `KLAC`, `NOK`, `LRCX`, `AMAT`, `SMH`, `FCX`, `AMZN`, `INTC`, final candidates는 `AMZN`, `INTC`, `AMAT`.
- Candidate quote/spread: AMZN bid 263.06, ask 263.10, spread 0.0152%, quote time `2026-05-26T19:11:29.894160Z`.
- SEC EDGAR는 local CIK cache로 `AMZN -> 0001018724` 확인 후 company info/recent filings pass. Yahoo Finance는 AMZN news/recommendations usable. FRED는 scheduler preflight `2026-05-27-0411-hourly-autopilot-research-mcp-preflight.json`의 `get_macro_snapshot` pass를 usable evidence로 사용했다.
- Alpha Vantage는 `TOOL_LIST` -> `TOOL_GET("PING")` -> `TOOL_CALL("PING", {})` -> `TOOL_GET("NEWS_SENTIMENT")` 후 첫 non-PING `TOOL_CALL("NEWS_SENTIMENT")`이 wrapper cancelled되어 `gap_category=cancelled`로 기록하고 candidate data retry를 중단했다. Firecrawl은 Codex tool catalog에 registered MCP tool이 노출되지 않아 `gap_category=wrapper_error`로 기록했고 shell/curl/local wrapper는 호출하지 않았다.
- First blocking gate: 없음. 검증: universe strict PASS, MCP strict PASS, risk-check PASS.
- 제출 전 gate summary: paper mode, market clock, order plan, universe/MCP/risk validator, quote freshness/spread, order shape, duplicate/open-order check, source refs를 plain text로 기록했다.
- 제출: AMZN 1주 day limit buy, limit 263.10, client_order_id `hourly-20260527-0411-amzn-buy-1`.
- Post-trade: Alpaca order id `642f83f9-cce5-4555-b4eb-9bee644d8545`, status `new`, filled_qty 0, submitted_at `2026-05-26T19:19:07.508236707Z`. `get_orders(status=open)`에서 same client id/order id를 확인했고 `get_account_activities(FILL, after=2026-05-26T19:10:00Z)`는 신규 fill 0건이었다.
- Reconciliation gap: symbol-filtered `get_orders`, `get_order_by_id`, post-submit `get_all_positions`, post-submit `get_account_info`는 wrapper/user cancellation으로 `gap_category=cancelled` 기록했다.
- submitted orders: `AMZN` 1주 open order. skipped orders: `INTC`는 AMZN 대비 낮은 확신, `AMAT`/`SMH`/`MU`/`AMD`/`KLAC`/`LRCX`는 spread 또는 semiconductor cluster 부담, `NOK`/`FCX`는 same-day duplicate buy 회피.
- 리포트: `wiki/current-runs/daily/2026-05-27-0411-hourly-autopilot.md`.
- 원천: `wiki/evidence-store/sources/2026-05-27-0411-hourly-autopilot-sources.md`.
- run manifest: `wiki/evidence-store/run-manifests/2026-05-27-0411-hourly-autopilot.json`.
- order plan: `wiki/trade-ledger/orders/2026-05-27-0411-hourly-autopilot.json`.
- post-trade snapshot: `wiki/trade-ledger/positions/current.md`.
- review due markers: AMZN은 open order라 아직 fill review due가 아니다. AAPL/LLY/FCX/NOK/NVDA 및 2026-05-22 체결분은 계속 `회고 대기`.

## [2026-05-27 04:39 Asia/Seoul] hourly-autopilot | INTC submit cancelled, 실제 주문 없음

- run id: `2026-05-27-0431-hourly-autopilot`.
- 사용자 승인에 따라 `harness/workflows/hourly-autopilot.md`를 실행했다.
- `.env`에서 `ALPACA_PAPER_TRADE=true`를 확인했고, API key 값은 출력하거나 기록하지 않았다.
- Scheduler-owned Alpaca core preflight `wiki/evidence-store/sources/2026-05-27-0431-hourly-autopilot-alpaca-core-preflight.json`을 먼저 읽었다. Hard gate pass, market open, account/positions/open orders/fills/watchlists/asset/quotes/snapshots/latest trades 모두 pass로 기록되어 Alpaca core evidence로 사용했다.
- Market clock: `2026-05-26T15:31:09.123434238-04:00` 기준 open, next close `2026-05-26T16:00:00-04:00`.
- Account before decision: portfolio value 101631.14 USD, cash 42347.59 USD, buying power 137133.22 USD, current positions 13개, open order 1건 AMZN buy `new`.
- Universe: 62개 metadata universe와 `SPY`/`QQQ`를 스크리닝했다. Pre-MCP shortlist는 `MU`, `AMD`, `KLAC`, `LRCX`, `SMH`, `INTC`, `AMAT`, `AMZN`, `AAPL`, `NVDA`, final candidates는 `INTC`, `SMH`, `AMAT`.
- Candidate quote/spread: INTC bid 123.32, ask 123.35, spread 0.0243%, quote time `2026-05-26T19:31:32.567873288Z`.
- SEC EDGAR는 local CIK cache로 `INTC -> 0000050863` 확인 후 company info/recent filings pass. Yahoo Finance는 INTC news/recommendations usable. FRED는 scheduler preflight `2026-05-27-0431-hourly-autopilot-research-mcp-preflight.json`의 `get_macro_snapshot` pass를 usable evidence로 사용했다.
- Alpha Vantage는 `TOOL_LIST` -> `TOOL_GET("PING")` -> `TOOL_CALL("PING", {})` -> `TOOL_GET("NEWS_SENTIMENT")` 후 첫 non-PING `TOOL_CALL("NEWS_SENTIMENT")`이 wrapper cancelled되어 `gap_category=cancelled`로 기록하고 candidate data retry를 중단했다. Firecrawl은 Codex tool catalog에 registered MCP tool이 노출되지 않아 `gap_category=wrapper_error`로 기록했고 shell/curl/local wrapper는 호출하지 않았다.
- First blocking gate: 없음. 검증: universe strict PASS, MCP strict PASS, risk-check PASS.
- 제출 전 gate summary: paper mode, market clock, order plan, universe/MCP/risk validator, quote freshness/spread, order shape, duplicate/open-order check, source refs를 plain text로 기록했다.
- 제출 시도: INTC 1주 day limit buy, limit 123.35, client_order_id `hourly-20260527-0431-intc-buy-1`. 첫 submit call은 cancelled였고, `get_orders(status=all, symbols=INTC)`에서 주문 없음 확인 후 같은 client id로 1회 재시도했으나 retry도 cancelled였다. 다른 client id로 재시도하지 않았다.
- Post-attempt reconciliation: `get_orders(status=all, symbols=INTC)` empty, `get_account_activities(FILL, after=2026-05-26T19:30:00Z)` empty, `get_all_positions` pass 및 INTC position 없음. `get_order_by_client_id`는 wrapper/user cancellation으로 `gap_category=cancelled` 기록했다.
- submitted orders: 없음. skipped/failed orders: INTC submit cancelled, SMH는 semiconductor cluster 부담으로 recheck, AMAT은 spread fail, AMZN은 기존 open buy order로 중복 회피.
- 리포트: `wiki/current-runs/daily/2026-05-27-0431-hourly-autopilot.md`.
- 원천: `wiki/evidence-store/sources/2026-05-27-0431-hourly-autopilot-sources.md`.
- run manifest: `wiki/evidence-store/run-manifests/2026-05-27-0431-hourly-autopilot.json`.
- order plan: `wiki/trade-ledger/orders/2026-05-27-0431-hourly-autopilot.json`.
- review due markers: 이번 run 신규 fill 없음. AMZN open order는 아직 fill review due가 아니며, AAPL/LLY/FCX/NOK/NVDA 및 2026-05-22 체결분은 계속 `회고 대기`.

## [2026-05-27 04:54 Asia/Seoul] hourly-autopilot | AMZN open-order lifecycle risk gate 실패로 주문 없음

- run id: `2026-05-27-0451-hourly-autopilot`.
- 사용자 승인에 따라 `harness/workflows/hourly-autopilot.md`를 실행했다.
- `.env`에서 `ALPACA_PAPER_TRADE=true`를 확인했고, API key 값은 출력하거나 기록하지 않았다. Nested shell export는 비어 있었지만 repository paper-mode 설정이 true라 workflow file check는 통과로 기록했다.
- Scheduler-owned Alpaca core preflight `wiki/evidence-store/sources/2026-05-27-0451-hourly-autopilot-alpaca-core-preflight.json`을 먼저 읽었다. Hard gate pass, market open, account/positions/open orders/fills/watchlists/asset/quotes/snapshots/latest trades pass를 Alpaca core evidence로 사용했다.
- Market clock: `2026-05-26T15:51:09.581579613-04:00` 기준 open, next close `2026-05-26T16:00:00-04:00`.
- Account before decision: portfolio value 101738.22 USD, cash 42347.59 USD, buying power 137240.29 USD, current positions 13개, open order 1건 AMZN buy `new`.
- Universe: 62개 metadata universe와 `SPY`/`QQQ`를 스크리닝했다. Pre-MCP shortlist는 `MU`, `AMD`, `KLAC`, `NOK`, `LRCX`, `AMAT`, `SMH`, `FCX`, `GE`, `INTC`, final candidates는 `INTC`, `SMH`, `AMAT`.
- Candidate quote/spread: INTC bid 123.30, ask 123.38, spread 0.0649%, quote time `2026-05-26T19:51:32.634964759Z`; quote age는 decision time 기준 20분 이내였다.
- SEC EDGAR는 local CIK cache로 `INTC -> 0000050863` 확인 후 company info/recent filings pass. Yahoo Finance는 INTC news/recommendations usable. FRED는 scheduler preflight `2026-05-27-0451-hourly-autopilot-research-mcp-preflight.json`의 `get_macro_snapshot` pass를 usable evidence로 사용했다.
- Alpha Vantage는 `TOOL_LIST` -> `TOOL_GET("PING")` -> `TOOL_CALL("PING", {})` pass 후 candidate data용 `TOOL_GET("NEWS_SENTIMENT")`가 wrapper cancelled되어 `gap_category=cancelled`로 기록했고 추가 Alpha candidate function은 시도하지 않았다. Firecrawl은 Codex tool catalog에 registered MCP tool이 노출되지 않아 `gap_category=wrapper_error`로 기록했고 shell/curl/local wrapper는 호출하지 않았다.
- First blocking gate: `risk_open_order_lifecycle`. 검증: universe strict PASS, MCP strict PASS, risk-check FAIL(`AMZN: open order age 34.4 minutes exceeds lifecycle limit 30.0`).
- submitted orders: 없음. `place_stock_order` 호출 없음. skipped orders: INTC validation buy 후보는 기존 AMZN open order lifecycle risk gate 실패로 차단, SMH/AMAT은 recheck.
- Post-trade reconciliation: 신규 submit attempt는 없었고, Alpaca preflight 기준 AMZN open order `new` filled_qty 0, same-day fills LLY/FCX/NOK/NVDA/AAPL, positions 13개를 확인했다.
- 리포트: `wiki/current-runs/daily/2026-05-27-0451-hourly-autopilot.md`.
- 원천: `wiki/evidence-store/sources/2026-05-27-0451-hourly-autopilot-sources.md`.
- run manifest: `wiki/evidence-store/run-manifests/2026-05-27-0451-hourly-autopilot.json`.
- order plan: `wiki/trade-ledger/orders/2026-05-27-0451-hourly-autopilot.json`.
- portfolio snapshot: `wiki/trade-ledger/positions/current.md`.
- review due markers: 이번 run 신규 fill 없음. AMZN open order는 아직 fill review due가 아니며, AAPL/LLY/FCX/NOK/NVDA 및 2026-05-22 체결분은 계속 `회고 대기`.

## [2026-05-27 06:24 Asia/Seoul] analyst-review-cycle | 2026-05-22 stock-only 1D 회고

- `harness/workflows/analyst-review-cycle.md`를 review-only로 실행했다. 주문 제출/교체/취소/청산 도구는 호출하지 않았다.
- `.env`에서 `ALPACA_PAPER_TRADE=true`를 확인했고, API key 값은 출력하거나 기록하지 않았다.
- Alpaca MCP reconciliation: account, positions, open/all orders, FILL activities, snapshots, daily bars, news pass. `get_portfolio_history`는 최초 호출과 2회 retry 모두 cancelled라 `gap_category=cancelled`, `retry_count=2`로 기록했다.
- 현재 계좌: portfolio value 101779.63 USD, cash 42347.59 USD, buying power 137406.46 USD, long market value 59432.04 USD, open orders 0건. AMZN `hourly-20260527-0411-amzn-buy-1`는 `expired`, filled_qty 0으로 확인했다.
- Review candidates: 2026-05-22 stock-only 체결분 AMD, AVGO, LRCX, TSM, NOK, UNH, ETN, RGTI, IONQ, NVDA의 1D interim review가 due. 2026-05-26 LLY/FCX/NOK/NVDA/AAPL validation fills는 아직 1D review 대기. PLTR/QBTS/TSLA skipped recommendations도 1D 결과를 비교했다.
- Alpha Vantage는 `TOOL_LIST` -> `TOOL_GET("PING")` -> `TOOL_CALL("PING", {})` pass 후 `TOOL_GET("NEWS_SENTIMENT")` 직후 첫 non-PING `TOOL_CALL("NEWS_SENTIMENT")`이 cancelled되어 추가 Alpha retries를 중단하고 `gap_category=cancelled`로 기록했다.
- SEC EDGAR는 NVDA/UNH/RGTI/LLY recent filings pass, AMD filing call은 cancelled. Yahoo Finance는 AMD/NOK/UNH/RGTI recommendations와 NOK news pass, NVDA recommendations는 cancelled. FRED/Firecrawl은 Codex tool catalog에 exposed tools가 없어 shell/curl/local wrapper를 호출하지 않고 `gap_category=wrapper_error`로 기록했다.
- 1D 결과: AMD/NOK/LRCX/ETN/AVGO/TSM은 양호했고, RGTI/UNH/IONQ/NVDA는 event risk, healthcare headline risk, 양자 변동성, 대형 AI 기대 선반영 부담이 확인됐다. Skipped PLTR/QBTS 제외는 1D 기준 타당, TSLA 제외는 중립에 가까웠다.
- 산출물: [[2026-05-27-portfolio-review]], [[2026-05-27-0624-analyst-review-cycle-sources]], `wiki/evidence-store/run-manifests/2026-05-27-0624-analyst-review-cycle.json`, [[portfolio-current]].
- 정책 변경: 없음. 1D 단일 회고이고 5D/20D가 남아 있으며 portfolio history gap도 있어 evidence threshold를 충족하지 않았다.

## [2026-05-27 07:57 Asia/Seoul] automation-maintenance | scheduled MCP 재발 방지 강화

- 원인 분석 결과를 반영해 scheduled wrapper가 `.env`를 export한 뒤 nested Codex를 실행하도록 수정했다. 이는 nested shell에서 `ALPACA_PAPER_TRADE=true`가 비어 `paper_mode_env_missing`으로 오탐되는 문제를 막기 위한 조치다.
- `scripts/cancel-stale-autopilot-orders.py`를 추가했다. 이 helper는 Alpaca MCP만 사용하며, paper mode에서 `client_order_id`가 `hourly-`로 시작하는 stale/unfilled/day-limit/us-equity autopilot 주문만 취소 대상으로 삼는다. 비-autopilot 주문, 부분체결 주문, options, crypto, short/live 주문은 취소하지 않는다.
- hourly wrapper는 stale order cleanup을 먼저 실행하고, 이후 Alpaca core preflight를 다시 캡처한다. cleanup 실패 또는 stale 주문 잔존 시 workflow는 `risk_open_order_lifecycle`로 신규 주문을 막도록 문서화했다.
- scheduled Codex MCP override에 FRED와 Firecrawl 로컬 MCP를 정식 등록하고 approval mode를 명시했다. Analyst review wrapper에도 같은 read-only research MCP 등록을 적용했다.
- SEC EDGAR는 scheduled autopilot에서 local CIK fallback 후 lightweight `get_company_info`/`get_recent_filings`를 우선 사용하도록 명시해, 불필요한 heavy financials 호출 cancellation이 SEC usable evidence를 깨지 않게 했다.
- 검증: stale cleanup live dry-run `manual-stale-cleanup-dry-run-2026-05-27` PASS, stale candidates 0, cancel attempts 0, remaining open orders 0.
- 검증: `python3 -m unittest discover -s tests` 70개 PASS, wrapper `bash -n` PASS, 관련 Python helper `py_compile` PASS, launchd plist lint PASS.

## [2026-05-27 10:08 Asia/Seoul] analysis | 장마감 전 hourly autopilot gate 원인 설명

- 사용자 요청에 따라 `2026-05-27 02:06 KST` hourly autopilot gate 점검 로그부터 장마감까지 추천/주문 흐름을 재검토했다.
- 결론: 02:06 run 자체는 Alpaca account/order/position/asset core gate cancellation 때문에 주문이 없었지만, 이후 `NOK`, `NVDA`, `AAPL`은 1주 paper validation buy로 체결됐다.
- 장 후반에는 research MCP usable/pass 3개 미달, nested paper-mode env 미확인, AMZN open order lifecycle 30분 초과, INTC submit wrapper cancellation이 주문을 막았다.
- 매도/trim은 ticker cap, cash floor, invested cap, thesis-break, stale-thesis trigger가 없어 제출되지 않았다.
- 분석 문서: [[2026-05-27-autopilot-close-gate-analysis]].
- 이번 분석에서는 Alpaca 주문 제출/교체/취소/청산 도구를 호출하지 않았고, 실제 주문/포지션 변경도 없었다.

## [2026-05-27 10:20 Asia/Seoul] analysis | autopilot gate 세부 원인 Q&A 보강

- 사용자 추가 질문에 따라 Alpaca core cancellation, research MCP failure, AMZN 미체결, INTC submit cancellation, 매도 미발생 사유를 세부 원인별로 분리했다.
- Alpaca/INTC cancellation은 데이터 없음보다 scheduled nested Codex MCP 승인/래퍼 호출 이슈에 가깝고, `.env` export, scheduler-owned Alpaca preflight, MCP approval override로 예방 조치가 이미 들어간 상태임을 기록했다.
- `03:14 KST` research MCP 실패는 AMZN/INTC 데이터 부재가 아니라 SEC/Alpha 호출 cancellation, Firecrawl tool 노출 문제, Yahoo/FRED만 usable한 상황으로 분류했다.
- AMZN 미체결은 장마감 41분 전 제출이었지만 7분 전 ask 기준 limit order라 가격 이동/체결 우선순위 문제로 fill되지 않고 day order 만료된 것으로 해석했다.
- 매도 없음은 확인된 로직 오류가 아니라 보수적 trim 정책 결과이며, 회전매매형 매도는 별도 검증 후 정책 추가가 필요하다고 정리했다.
- 분석 문서 보강: [[2026-05-27-autopilot-close-gate-analysis]].
- 이번 보강에서는 Alpaca 주문 제출/교체/취소/청산 도구를 호출하지 않았고, 실제 주문/포지션 변경도 없었다.

## [2026-05-27 10:43 Asia/Seoul] automation-maintenance | research MCP preflight 근본 보강

- 사용자 요청에 따라 03:14 KST 이후 반복된 research MCP usable/pass 3개 미달 문제의 재발 방지 조치를 구현했다.
- `scripts/fetch-research-mcp-preflight.py`를 FRED 단일 preflight에서 SEC EDGAR, Alpha Vantage, FRED, Firecrawl, Yahoo Finance 5개 research MCP preflight로 확장했다.
- Scheduler wrapper `scripts/run-hourly-autopilot-codex.sh`는 Alpaca core preflight JSON과 `CODEX_AUTOPILOT_RESEARCH_SYMBOL_LIMIT`을 넘겨, nested Codex 시작 전 fresh quote/spread 기반 후보의 research evidence를 먼저 캡처한다.
- Nested workflow는 research preflight의 `mcp_coverage_hint`를 authoritative scheduled evidence로 사용하고, 실패 provider는 `gap_category`, `gap_reason`, `retry_count`를 그대로 manifest에 반영하도록 문서화했다.
- SEC EDGAR는 local CIK cache와 lightweight company/recent filing check를 우선 사용하고, Alpha Vantage는 PING 후 candidate `NEWS_SENTIMENT` 한 번으로 호출 문제와 데이터 공백을 분리하도록 테스트를 추가했다.
- 검증: `python3 -m py_compile scripts/fetch-research-mcp-preflight.py` PASS, `bash -n scripts/run-hourly-autopilot-codex.sh` PASS, `python3 -m unittest tests.test_fetch_research_mcp_preflight tests.test_mcp_runtime_wrappers` 14개 PASS, `python3 -m unittest discover -s tests` 77개 PASS.
- 이번 maintenance에서는 Alpaca 주문 제출/교체/취소/청산 도구를 호출하지 않았고, 실제 주문/포지션 변경도 없었다.

## [2026-05-27 10:49 Asia/Seoul] automation-test | 장외 hourly autopilot wrapper 테스트

- 사용자 요청에 따라 장외 상태에서 `scripts/run-hourly-autopilot-codex.sh`를 수동 실행했다.
- 기본 sandbox 실행에서는 Alpaca MCP clock 확인이 `TaskGroup` 예외로 실패했고, wrapper는 fail-closed로 `Unable to confirm Alpaca market is open through MCP`를 출력한 뒤 종료했다.
- 실제 스케줄 환경에 가깝게 샌드박스 밖에서 재실행하자 Alpaca MCP `get_clock`이 정상 응답했다. 결과는 `is_open=false`, timestamp `2026-05-26T21:48:57.362709291-04:00`, next open `2026-05-27T09:30:00-04:00`, next close `2026-05-27T16:00:00-04:00`.
- 장외 gate가 의도대로 동작해 research preflight, nested Codex, order plan, 주문 제출 단계로 진입하지 않았다.
- 이번 테스트에서는 Alpaca 주문 제출/교체/취소/청산 도구를 호출하지 않았고, 실제 주문/포지션 변경도 없었다.

## [2026-05-27 11:07 Asia/Seoul] automation-test | research MCP preflight 실제 상태 확인

- 변경된 scheduler-owned research MCP preflight 방식으로 `AMZN`, `INTC` 대상 실제 MCP 상태를 점검했다. 출력 파일은 `/private/tmp/research-mcp-preflight-check.json`로 두어 위키 raw source를 오염시키지 않았다.
- 최초 sandbox 실행은 MCP/network 제약으로 장시간 멈춰 정리했고, 실제 스케줄 환경에 가까운 샌드박스 밖 실행으로 확인했다.
- 최초 실제 결과: FRED pass, Firecrawl pass, SEC EDGAR failed, Alpha Vantage timeout, Yahoo Finance failed. 즉 현재 research confirmation은 2개라 buy actionable 기준 3개에는 미달했다.
- 실패 원인이 모두 timeout인데 SEC/Yahoo 최상위 row가 `provider_error`로 뭉개지는 문제가 보여 `scripts/fetch-research-mcp-preflight.py`를 보강했다. SEC/Yahoo는 systemic timeout/cancelled/dns/auth/wrapper gap이면 fail-fast하고 최상위 `gap_category`를 실제 원인으로 올리도록 수정했다.
- Scheduler wrapper는 research MCP timeout을 `CODEX_AUTOPILOT_RESEARCH_MCP_TIMEOUT_SECONDS`로 조정 가능하게 하고 기본 75초를 넘기도록 수정했다.
- 보강 후 `AMZN` 1종목 재점검 결과: FRED pass, Firecrawl pass, SEC EDGAR timeout, Alpha Vantage timeout, Yahoo Finance timeout. 새 분류는 timeout으로 정확히 기록됐다.
- 검증: `python3 -m py_compile scripts/fetch-research-mcp-preflight.py` PASS, `bash -n scripts/run-hourly-autopilot-codex.sh` PASS, `python3 -m unittest tests.test_fetch_research_mcp_preflight tests.test_mcp_runtime_wrappers` 16개 PASS, `python3 -m unittest discover -s tests` 79개 PASS.
- 이번 테스트에서는 Alpaca 주문 제출/교체/취소/청산 도구를 호출하지 않았고, 실제 주문/포지션 변경도 없었다.

## [2026-05-27 11:15 Asia/Seoul] automation-maintenance | research MCP timeout 원인 확정 및 수정

- 사용자 질문에 따라 SEC EDGAR, Alpha Vantage, Yahoo Finance timeout 원인이 provider 서버인지, shell wrapper인지, 우리 호출 방식인지 분리 진단했다.
- 진단 결과 SEC/Yahoo/Alpha 모두 provider tool call 전에 MCP `initialize` 단계에서 timeout됐다. stderr 확인 결과 해당 서버들은 JSON-lines stdio를 기대하는데, 우리 `fetch-research-mcp-preflight.py`가 FRED/Firecrawl 로컬 서버용 `Content-Length` framing으로 호출해 `Content-Length: ...`를 JSON으로 파싱하려다 실패하고 있었다.
- 결론: 이번 timeout의 1차 원인은 provider 데이터 부재나 서버 본연의 불안정성이 아니라 우리 scheduler preflight의 stdio protocol mismatch였다. Shell wrapper/uvx 자체도 startup overhead는 있지만, 이번 현상의 핵심 원인은 framing 불일치였다.
- 수정: SEC EDGAR, Alpha Vantage, Yahoo Finance는 JSON-lines protocol로 호출하고, FRED/Firecrawl 로컬 MCP는 기존 Content-Length protocol을 유지하도록 provider별 protocol을 분리했다.
- 추가 수정: Alpha Vantage 응답이 큰 한 줄 JSON으로 올 때 Python `readline` 기본 limit에 걸려 `Separator is not found, and chunk exceed the limit`가 발생해 stdio read limit을 8 MiB로 늘렸다.
- 실제 재검증: `/private/tmp/research-mcp-preflight-alpha-buffer-check.json` 기준 `AMZN` 1종목 preflight에서 SEC EDGAR, Alpha Vantage, FRED, Firecrawl, Yahoo Finance 5개 모두 pass.
- 검증: `python3 -m py_compile scripts/fetch-research-mcp-preflight.py` PASS, `python3 -m unittest tests.test_fetch_research_mcp_preflight tests.test_mcp_runtime_wrappers` 16개 PASS, `python3 -m unittest discover -s tests` 79개 PASS.
- 이번 maintenance에서는 Alpaca 주문 제출/교체/취소/청산 도구를 호출하지 않았고, 실제 주문/포지션 변경도 없었다.

## [2026-05-27 11:22 Asia/Seoul] automation-test | MCP 호출 경로 재점검

- 사용자 지적에 따라 "MCP 호출 때문에 남은 이슈가 없는지"를 다시 점검했다.
- 주문 상태를 바꿀 수 있는 stale cleanup/order submit/cancel 경로는 호출하지 않았고, read-only preflight만 실행했다.
- Alpaca core read-only preflight `/private/tmp/alpaca-core-mcp-check.json`: `get_clock`, `get_account_info`, `get_all_positions`, `get_orders(status=open)`, `get_account_activities(FILL)`, `get_watchlists`, 62개 symbol `get_asset`, `get_stock_latest_quote`, `get_stock_snapshot`, `get_stock_latest_trade` 모두 pass. Hard gate는 장외라 `market_closed`로만 failed.
- Research MCP preflight `/private/tmp/research-mcp-check.json`: `AMZN`, `INTC` 기준 SEC EDGAR, Alpha Vantage, FRED, Firecrawl, Yahoo Finance 5개 모두 pass, retry 0. `mcp_coverage_hint`도 5개 모두 `queried=true`, `used_in_score=true`, `outcome=pass`로 생성됐다.
- `scripts/check-mcp-coverage.py --strict` 임시 manifest는 Alpaca row가 장외 `market_closed`로 failed라 strict fail이 정상이다. MCP read-only 호출 자체의 failure는 확인되지 않았다.
- 검증: `python3 -m unittest discover -s tests` 79개 PASS.
- 이번 점검에서는 Alpaca 주문 제출/교체/취소/청산 도구를 호출하지 않았고, 실제 주문/포지션 변경도 없었다.

## [2026-05-27 11:55 Asia/Seoul] automation-maintenance | research MCP timeout 구조 개선

- 사용자 분석을 재점검했다. 한 사이클에서 preflight와 nested Codex가 research MCP를 각각 cold start할 수 있고, SEC/Yahoo가 심볼별로 MCP 프로세스를 반복 기동하던 구조, 사이클 간 cache 부재, provider circuit breaker 부재, launchd 환경 의존성은 실제 timeout 재발 위험으로 확인했다. Provider 5개 자체는 `asyncio.gather`로 병렬이었지만 provider 내부 호출이 병목이었다.
- `scripts/fetch-research-mcp-preflight.py`에서 SEC EDGAR와 Yahoo Finance를 provider당 단일 MCP stdio session으로 batch 호출하게 수정했다. 이제 12개 심볼이어도 SEC/Yahoo timeout 상한이 심볼 수만큼 곱해지지 않는다.
- Research provider positive row cache를 추가했다. 기본 TTL은 SEC/FRED/Firecrawl 60분, Yahoo 30분, Alpha Vantage 15분이며 `CODEX_AUTOPILOT_RESEARCH_CACHE_TTL_SECONDS`로 override 가능하다.
- Provider circuit breaker를 추가했다. `timeout`, `cancelled`, `dns`, `auth`, `wrapper_error` 같은 systemic failure가 나면 기본 600초 동안 해당 provider를 재시도하지 않고 `circuit_breaker_open` gap row로 기록한다.
- `scripts/run-hourly-autopilot-codex.sh`는 authoritative research preflight가 5개 provider row를 모두 포함하면 nested Codex에 research MCP를 의도적으로 등록하지 않아 두 번째 research MCP cold start를 피한다. 필요하면 `CODEX_AUTOPILOT_REGISTER_RESEARCH_MCP=always|never|auto`로 제어할 수 있다.
- Launchd 기본 환경 의존을 줄이기 위해 wrapper와 hourly plist example에 `HOME`, `LANG`, `LC_ALL`, `NO_PROXY`, scheduled Codex home, research cache/circuit env를 명시했고, wrapper는 `SSL_CERT_FILE`/`REQUESTS_CA_BUNDLE`을 certifi 경로로 보강한다.
- 실제 MCP 검증: `/private/tmp/research-cache-check-a.json` 첫 실행에서 `AMZN`, `INTC` 기준 SEC EDGAR, Alpha Vantage, FRED, Firecrawl, Yahoo Finance 5개 모두 pass, retry 0. `/private/tmp/research-cache-check-b.json` 두 번째 실행에서 5개 provider 모두 `cache_hit=true`.
- 검증: `python3 -m py_compile scripts/fetch-research-mcp-preflight.py` PASS, `bash -n scripts/run-hourly-autopilot-codex.sh` PASS, `python3 -m unittest tests.test_fetch_research_mcp_preflight tests.test_mcp_runtime_wrappers` 20개 PASS, `python3 -m unittest discover -s tests` 83개 PASS.
- 이번 maintenance에서는 Alpaca 주문 제출/교체/취소/청산 도구를 호출하지 않았고, 실제 주문/포지션 변경도 없었다.

## [2026-05-27 22:58 Asia/Seoul] hourly-autopilot | 2026-05-27-2246 scheduled paper autopilot

- Run id: `2026-05-27-2246-hourly-autopilot`. Market clock open at `2026-05-27T09:46:40.303390074-04:00`, next close `2026-05-27T16:00:00-04:00`.
- Scheduler stale-order cleanup passed: no initial/stale/remaining open autopilot orders.
- Recommendation shortlist: NKE, PFE, SO as validation buys; AMZN and PLTR retained as recheck candidates.
- Validation: universe strict PASS, MCP strict PASS, risk policy PASS. Alpaca core pass; SEC EDGAR/FRED/Firecrawl/Yahoo pass; Alpha Vantage gap `empty_response`.
- Submitted/skipped orders: NKE buy 1 filled @ 46.15, PFE buy 1 filled @ 26.34 after same-client-id retry following wrapper cancellation reconciliation, SO buy 1 filled @ 94.28. Open orders after reconciliation: 0.
- Manifest: `wiki/evidence-store/run-manifests/2026-05-27-2246-hourly-autopilot.json`. Order plan: `wiki/trade-ledger/orders/2026-05-27-2246-hourly-autopilot.json`. Report: `wiki/current-runs/daily/2026-05-27-2246-hourly-autopilot.md`.
- Review due markers: NKE/PFE/SO `회고 대기` for 1D/5D/20D analyst review.

## [2026-05-27 23:20 Asia/Seoul] hourly-autopilot | 2026-05-27-2311 scheduled paper autopilot

- Run id: `2026-05-27-2311-hourly-autopilot`. Market clock open at `2026-05-27T10:11:13.225633645-04:00`, next close `2026-05-27T16:00:00-04:00`.
- Scheduler stale-order cleanup passed: stale candidates 0, remaining open autopilot orders 0.
- Recommendation shortlist: GOOGL, WMT, NEE as validation buys; AAPL, BAC, QQQ, SPY, FCX, NOK, IONQ retained as recheck candidates. Same-day NKE/PFE/SO duplicate buys were skipped.
- Validation: universe strict PASS, MCP strict PASS, risk policy PASS. Alpaca core pass; SEC EDGAR/FRED/Firecrawl/Yahoo pass; Alpha Vantage gap `empty_response`. Optional registered quote refresh returned `cancelled`, but scheduler preflight quote rows were pass and less than 20 minutes old.
- Submitted/skipped orders: GOOGL buy 1 submitted open `new`; WMT buy 1 filled @ 118.31; NEE buy 1 submitted open `new`.
- Post-trade reconciliation: `get_order_by_client_id` pass for all three submitted client IDs, account/positions/FILL activity pass. `get_orders(status=open)` list reconciliation returned `cancelled`, so GOOGL/NEE open state is sourced to direct client-order checks.
- Manifest: `wiki/evidence-store/run-manifests/2026-05-27-2311-hourly-autopilot.json`. Order plan: `wiki/trade-ledger/orders/2026-05-27-2311-hourly-autopilot.json`. Report: `wiki/current-runs/daily/2026-05-27-2311-hourly-autopilot.md`.
- Review due markers: WMT `회고 대기` for 1D/5D/20D analyst review. GOOGL/NEE review markers pending fill; stale open-order lifecycle should be checked on the next scheduled run.

## [2026-05-27 23:40 Asia/Seoul] hourly-autopilot | 2026-05-27-2331-hourly-autopilot scheduled paper autopilot

- Run id: `2026-05-27-2331-hourly-autopilot`. Market clock open at `2026-05-27T10:31:09.601135165-04:00`, next close `2026-05-27T16:00:00-04:00`.
- Scheduler stale-order cleanup passed: stale candidates 0, cancel attempts 0, remaining fresh open autopilot order 1 for GOOGL.
- Recommendation shortlist: AMZN, BAC, XOM as validation buys; GOOGL skipped due fresh open buy order; same-day NKE/PFE/SO/WMT/NEE duplicate buys skipped.
- Validation: universe strict PASS, MCP strict PASS, risk policy PASS. Alpaca core pass; SEC EDGAR/FRED/Firecrawl/Yahoo pass; Alpha Vantage gap `empty_response`.
- Submitted/skipped orders: AMZN buy 1 filled @ 270.05, BAC buy 1 filled @ 52.06, XOM buy 1 filled @ 147.07. Open orders after reconciliation: GOOGL buy 1 `new` from 23:11 run.
- Manifest: `wiki/evidence-store/run-manifests/2026-05-27-2331-hourly-autopilot.json`. Order plan: `wiki/trade-ledger/orders/2026-05-27-2331-hourly-autopilot.json`. Report: `wiki/current-runs/daily/2026-05-27-2331-hourly-autopilot.md`.
- Review due markers: AMZN/BAC/XOM `회고 대기` for 1D/5D/20D analyst review.

## [2026-05-28 00:02 Asia/Seoul] hourly-autopilot | 2026-05-27-2351-hourly-autopilot scheduled paper autopilot

- Run id: `2026-05-27-2351-hourly-autopilot`. Market clock open at `2026-05-27T11:00:07.111449643-04:00`, next close `2026-05-27T16:00:00-04:00`.
- Scheduler stale-order cleanup canceled stale GOOGL order `hourly-20260527-2311-googl-buy-1`; direct order-id reconciliation confirmed `canceled`.
- Recommendation shortlist: V as final validation buy; MS and QQQ retained as recheck candidates. Same-day validation buys and the canceled GOOGL retry were skipped.
- Validation: universe strict PASS, MCP strict PASS, risk policy PASS. Alpaca core pass; SEC EDGAR/FRED/Firecrawl/Yahoo pass; Alpha Vantage gap `empty_response`; supplemental open-order retry gap `cancelled` recorded outside strict scoring.
- Submitted/skipped orders: V buy 1 submitted open `new`, client_order_id `hourly-20260527-2351-v-buy-1`; no fill at post-trade reconciliation.
- Manifest: `wiki/evidence-store/run-manifests/2026-05-27-2351-hourly-autopilot.json`. Order plan: `wiki/trade-ledger/orders/2026-05-27-2351-hourly-autopilot.json`. Report: `wiki/current-runs/daily/2026-05-27-2351-hourly-autopilot.md`.
- Review due markers: V fill pending; mark `회고 대기` after fill.

## [2026-05-28 00:13 Asia/Seoul] hourly-autopilot | 2026-05-28-0011-hourly-autopilot scheduled paper autopilot

- Run id: `2026-05-28-0011-hourly-autopilot`. Market clock open at `2026-05-27T11:11:12.097924695-04:00`, next close `2026-05-27T16:00:00-04:00`.
- Scheduler stale-order cleanup passed: stale candidates 0, cancel attempts 0, remaining fresh open autopilot order 1 for V.
- Recommendation shortlist: AMZN and PFE skipped as same-session duplicate buys; V skipped due fresh open buy order. SLB, INTC, PLTR, and QQQ remained research-preflight-covered recheck names but were not order candidates.
- Validation: universe strict PASS, MCP strict PASS, risk policy PASS for empty order plan. Alpaca core pass; SEC EDGAR/FRED/Firecrawl/Yahoo pass; Alpha Vantage gap `empty_response`.
- Submitted/skipped orders: no orders submitted. First blocking gate: `risk_daily_new_orders_budget` because 10 scheduled validation buy orders had already been created for the 2026-05-27 ET session.
- Manifest: `wiki/evidence-store/run-manifests/2026-05-28-0011-hourly-autopilot.json`. Order plan: `wiki/trade-ledger/orders/2026-05-28-0011-hourly-autopilot.json`. Report: `wiki/current-runs/daily/2026-05-28-0011-hourly-autopilot.md`.
- Review due markers: 신규 체결 없음. Existing filled validation buys remain queued for 1D/5D/20D analyst review.

## [2026-05-28 00:33 Asia/Seoul] hourly-autopilot | 2026-05-28-0031-hourly-autopilot scheduled paper autopilot

- Run id: `2026-05-28-0031-hourly-autopilot`. Market clock open at `2026-05-27T11:31:10.543392659-04:00`, next close `2026-05-27T16:00:00-04:00`.
- Scheduler stale-order cleanup passed: stale candidates 0, cancel attempts 0, remaining open autopilot orders 0. Prior V open buy was confirmed filled in scheduler Alpaca core preflight.
- Recommendation shortlist: AMZN, NKE, PFE skipped as same-session duplicate validation buys; HOOD, MSFT, QQQ retained as recheck names.
- Validation: universe strict PASS, MCP strict PASS, risk policy PASS for empty order plan. Alpaca core pass; SEC EDGAR/FRED/Firecrawl/Yahoo pass; Alpha Vantage gap `empty_response`.
- Submitted/skipped orders: no orders submitted. First blocking gate: `risk_daily_new_orders_budget` because 10 scheduled validation buy orders had already been created for the 2026-05-27 ET session.
- Manifest: `wiki/evidence-store/run-manifests/2026-05-28-0031-hourly-autopilot.json`. Order plan: `wiki/trade-ledger/orders/2026-05-28-0031-hourly-autopilot.json`. Report: `wiki/current-runs/daily/2026-05-28-0031-hourly-autopilot.md`.
- Review due markers: 신규 체결 없음. Existing filled validation buys remain queued for 1D/5D/20D analyst review.

## [2026-05-28 00:53 Asia/Seoul] hourly-autopilot | 2026-05-28-0051-hourly-autopilot scheduled paper autopilot

- Run id: `2026-05-28-0051-hourly-autopilot`. Market clock open at `2026-05-27T11:51:08.49930018-04:00`, next close `2026-05-27T16:00:00-04:00`.
- Scheduler stale-order cleanup passed: stale candidates 0, cancel attempts 0, remaining open autopilot orders 0.
- Recommendation shortlist: AMZN, NKE, WMT skipped as same-session duplicate validation buys; QQQ, NVDA, SLB, PLTR, NEE, FCX retained as recheck names.
- Validation: universe strict PASS, MCP strict PASS, risk policy PASS for empty order plan. Alpaca core pass; SEC EDGAR/FRED/Firecrawl/Yahoo pass; Alpha Vantage gap `empty_response`.
- Submitted/skipped orders: no orders submitted. First blocking gate: `risk_daily_new_orders_budget` because 10 scheduled validation buy orders had already been created for the 2026-05-27 ET session.
- Manifest: `wiki/evidence-store/run-manifests/2026-05-28-0051-hourly-autopilot.json`. Order plan: `wiki/trade-ledger/orders/2026-05-28-0051-hourly-autopilot.json`. Report: `wiki/current-runs/daily/2026-05-28-0051-hourly-autopilot.md`.
- Review due markers: 신규 체결 없음. Existing filled validation buys remain queued for 1D/5D/20D analyst review.

## [2026-05-28 01:13 Asia/Seoul] hourly-autopilot | 2026-05-28-0111-hourly-autopilot scheduled paper autopilot

- Run id: `2026-05-28-0111-hourly-autopilot`. Market clock open at `2026-05-27T12:11:07.963276302-04:00`, next close `2026-05-27T16:00:00-04:00`.
- Scheduler stale-order cleanup passed: stale candidates 0, cancel attempts 0, remaining open autopilot orders 0.
- Recommendation shortlist: AMZN, GOOGL, BAC skipped because same-session validation history and daily order budget block new buys; CVX, SBUX, QQQ, PLTR retained as recheck names.
- Validation: universe strict PASS, MCP strict PASS, risk policy PASS for empty order plan. Alpaca core pass; SEC EDGAR/FRED/Firecrawl/Yahoo pass; Alpha Vantage gap `empty_response`.
- Submitted/skipped orders: no orders submitted. First blocking gate: `risk_daily_new_orders_budget` because 10 scheduled validation buy orders had already been created for the 2026-05-27 ET session.
- Manifest: `wiki/evidence-store/run-manifests/2026-05-28-0111-hourly-autopilot.json`. Order plan: `wiki/trade-ledger/orders/2026-05-28-0111-hourly-autopilot.json`. Report: `wiki/current-runs/daily/2026-05-28-0111-hourly-autopilot.md`.
- Review due markers: 신규 체결 없음. Existing filled validation buys remain queued for 1D/5D/20D analyst review.

## [2026-05-28 01:33 Asia/Seoul] hourly-autopilot | 2026-05-28-0131-hourly-autopilot scheduled paper autopilot

- Run id: `2026-05-28-0131-hourly-autopilot`. Market clock open at `2026-05-27T12:31:12.962019871-04:00`, next close `2026-05-27T16:00:00-04:00`.
- Scheduler stale-order cleanup passed: stale candidates 0, cancel attempts 0, remaining open autopilot orders 0.
- Recommendation shortlist: AMZN, NKE, WMT, XOM, BAC skipped because same-session validation history and daily order budget block new buys; SLB, COP, INTC, QQQ retained as recheck names.
- Validation: universe strict PASS, MCP strict PASS, risk policy PASS for empty order plan. Alpaca core pass; SEC EDGAR/FRED/Firecrawl/Yahoo pass; Alpha Vantage gap `empty_response`.
- Submitted/skipped orders: no orders submitted. First blocking gate: `risk_daily_new_orders_budget` because 10 scheduled validation buy orders had already been created for the 2026-05-27 ET session.
- Manifest: `wiki/evidence-store/run-manifests/2026-05-28-0131-hourly-autopilot.json`. Order plan: `wiki/trade-ledger/orders/2026-05-28-0131-hourly-autopilot.json`. Report: `wiki/current-runs/daily/2026-05-28-0131-hourly-autopilot.md`.
- Review due markers: 신규 체결 없음. Existing filled validation buys remain queued for 1D/5D/20D analyst review.

## [2026-05-28 01:53 Asia/Seoul] hourly-autopilot | 2026-05-28-0151-hourly-autopilot scheduled paper autopilot

- Run id: `2026-05-28-0151-hourly-autopilot`. Market clock open at `2026-05-27T12:51:14.285369921-04:00`, next close `2026-05-27T16:00:00-04:00`.
- Scheduler stale-order cleanup passed: stale candidates 0, cancel attempts 0, remaining open autopilot orders 0.
- Recommendation shortlist: AMZN, NKE, WMT, XOM, BAC skipped because same-session validation history and daily order budget block new buys; SLB, FCX, COP, INTC, QQQ retained as recheck names.
- Validation: universe strict PASS, MCP strict PASS, risk policy PASS for empty order plan. Alpaca core pass; SEC EDGAR/FRED/Firecrawl/Yahoo pass; Alpha Vantage gap `empty_response`.
- Submitted/skipped orders: no orders submitted. First blocking gate: `risk_daily_new_orders_budget` because 10 scheduled validation buy orders had already been created for the 2026-05-27 ET session.
- Manifest: `wiki/evidence-store/run-manifests/2026-05-28-0151-hourly-autopilot.json`. Order plan: `wiki/trade-ledger/orders/2026-05-28-0151-hourly-autopilot.json`. Report: `wiki/current-runs/daily/2026-05-28-0151-hourly-autopilot.md`.
- Review due markers: 신규 체결 없음. Existing filled validation buys remain queued for 1D/5D/20D analyst review.

## [2026-05-28 02:13 Asia/Seoul] hourly-autopilot | 2026-05-28-0211-hourly-autopilot scheduled paper autopilot

- Run id: `2026-05-28-0211-hourly-autopilot`. Market clock open at `2026-05-27T13:11:09.269071583-04:00`, next close `2026-05-27T16:00:00-04:00`.
- Scheduler stale-order cleanup passed: stale candidates 0, cancel attempts 0, remaining open autopilot orders 0.
- Recommendation shortlist: AMZN, NKE, PFE, WMT, SO, NEE skipped because same-session validation history and daily order budget block new buys; SPY, COP, QQQ, QBTS retained as recheck names.
- Validation: universe strict PASS, MCP strict PASS, risk policy PASS for empty order plan. Alpaca core pass; SEC EDGAR/FRED/Firecrawl/Yahoo pass; Alpha Vantage gap `empty_response`.
- Submitted/skipped orders: no orders submitted. First blocking gate: `risk_daily_new_orders_budget` because 10 scheduled validation buy orders had already been created for the 2026-05-27 ET session.
- Manifest: `wiki/evidence-store/run-manifests/2026-05-28-0211-hourly-autopilot.json`. Order plan: `wiki/trade-ledger/orders/2026-05-28-0211-hourly-autopilot.json`. Report: `wiki/current-runs/daily/2026-05-28-0211-hourly-autopilot.md`.
- Review due markers: 신규 체결 없음. Existing filled validation buys remain queued for 1D/5D/20D analyst review.

## [2026-05-28 02:33 Asia/Seoul] hourly-autopilot | 2026-05-28-0231-hourly-autopilot scheduled paper autopilot

- Run id: `2026-05-28-0231-hourly-autopilot`. Market clock open at `2026-05-27T13:31:10.080501002-04:00`, next close `2026-05-27T16:00:00-04:00`.
- Scheduler stale-order cleanup passed: stale candidates 0, cancel attempts 0, remaining open autopilot orders 0.
- Recommendation shortlist: AMZN, NKE, PFE, WMT, SO, NEE skipped because same-session validation history and daily order budget block new buys; HOOD, SPY, COP, QQQ, QBTS, MSFT retained as recheck names.
- Validation: universe strict PASS, MCP strict PASS, risk policy PASS for empty order plan. Alpaca core pass; SEC EDGAR/FRED/Firecrawl/Yahoo pass; Alpha Vantage gap `empty_response`.
- Submitted/skipped orders: no orders submitted. First blocking gate: `risk_daily_new_orders_budget` because 10 scheduled validation buy orders had already been created for the 2026-05-27 ET session.
- Manifest: `wiki/evidence-store/run-manifests/2026-05-28-0231-hourly-autopilot.json`. Order plan: `wiki/trade-ledger/orders/2026-05-28-0231-hourly-autopilot.json`. Report: `wiki/current-runs/daily/2026-05-28-0231-hourly-autopilot.md`.
- Review due markers: 신규 체결 없음. Existing filled validation buys remain queued for 1D/5D/20D analyst review.

## [2026-05-28 02:53 Asia/Seoul] hourly-autopilot | 2026-05-28-0251-hourly-autopilot scheduled paper autopilot

- Run id: `2026-05-28-0251-hourly-autopilot`. Market clock open at `2026-05-27T13:51:06.924237391-04:00`, next close `2026-05-27T16:00:00-04:00`.
- Scheduler stale-order cleanup passed: stale candidates 0, cancel attempts 0, remaining open autopilot orders 0.
- Recommendation shortlist: NKE, AMZN, BAC skipped because same-session validation history and daily order budget block new buys; HOOD, GOOGL, MCD, SPY, QQQ, MS, COP, NVDA, SLB retained as recheck names.
- Validation: universe strict PASS, MCP strict PASS, risk policy PASS for empty order plan. Alpaca core pass; SEC EDGAR/FRED/Firecrawl/Yahoo pass; Alpha Vantage gap `empty_response`.
- Submitted/skipped orders: no orders submitted. First blocking gate: `risk_daily_new_orders_budget` because 10 scheduled validation buy orders had already been created for the 2026-05-27 ET session.
- Manifest: `wiki/evidence-store/run-manifests/2026-05-28-0251-hourly-autopilot.json`. Order plan: `wiki/trade-ledger/orders/2026-05-28-0251-hourly-autopilot.json`. Report: `wiki/current-runs/daily/2026-05-28-0251-hourly-autopilot.md`.
- Review due markers: 신규 체결 없음. Existing filled validation buys remain queued for 1D/5D/20D analyst review.

## [2026-05-28 03:13 Asia/Seoul] hourly-autopilot | 2026-05-28-0311-hourly-autopilot scheduled paper autopilot

- Run id: `2026-05-28-0311-hourly-autopilot`. Market clock open at `2026-05-27T14:11:11.515780299-04:00`, next close `2026-05-27T16:00:00-04:00`.
- Scheduler stale-order cleanup passed: stale candidates 0, cancel attempts 0, remaining open autopilot orders 0.
- Recommendation shortlist: AMZN, BAC, V, SO, NEE skipped because same-session validation history and daily order budget block new buys; FCX, COP, SLB, SPY, QQQ, PLTR, QBTS retained as recheck names.
- Validation: universe strict PASS, MCP strict PASS, risk policy PASS for empty order plan. Alpaca core pass; SEC EDGAR/FRED/Firecrawl/Yahoo pass; Alpha Vantage gap `empty_response`.
- Submitted/skipped orders: no orders submitted. First blocking gate: `risk_daily_new_orders_budget` because 10 scheduled validation buy orders had already been created for the 2026-05-27 ET session.
- Manifest: `wiki/evidence-store/run-manifests/2026-05-28-0311-hourly-autopilot.json`. Order plan: `wiki/trade-ledger/orders/2026-05-28-0311-hourly-autopilot.json`. Report: `wiki/current-runs/daily/2026-05-28-0311-hourly-autopilot.md`.
- Review due markers: 신규 체결 없음. Existing filled validation buys remain queued for 1D/5D/20D analyst review.

## [2026-05-28 03:33 Asia/Seoul] hourly-autopilot | 2026-05-28-0331-hourly-autopilot scheduled paper autopilot

- Run id: `2026-05-28-0331-hourly-autopilot`. Market clock open at `2026-05-27T14:31:09.933145584-04:00`, next close `2026-05-27T16:00:00-04:00`.
- Scheduler stale-order cleanup passed: stale candidates 0, cancel attempts 0, remaining open autopilot orders 0.
- Recommendation shortlist: AMZN, WMT, AAPL, BAC, SO, NVDA skipped because same-session validation history and daily order budget block new buys; HOOD, MSFT, SLB, SPY, QQQ, MRK retained as recheck names.
- Validation: universe strict PASS, MCP strict PASS, risk policy PASS for empty order plan. Alpaca core pass; SEC EDGAR/FRED/Firecrawl/Yahoo pass; Alpha Vantage gap `empty_response`.
- Submitted/skipped orders: no orders submitted. First blocking gate: `risk_daily_new_orders_budget` because 10 scheduled validation buy orders had already been created for the 2026-05-27 ET session.
- Manifest: `wiki/evidence-store/run-manifests/2026-05-28-0331-hourly-autopilot.json`. Order plan: `wiki/trade-ledger/orders/2026-05-28-0331-hourly-autopilot.json`. Report: `wiki/current-runs/daily/2026-05-28-0331-hourly-autopilot.md`.
- Review due markers: 신규 체결 없음. Existing filled validation buys remain queued for 1D/5D/20D analyst review.

## [2026-05-28 03:53 Asia/Seoul] hourly-autopilot | 2026-05-28-0351-hourly-autopilot scheduled paper autopilot

- Run id: `2026-05-28-0351-hourly-autopilot`. Market clock open at `2026-05-27T14:51:10.214791605-04:00`, next close `2026-05-27T16:00:00-04:00`.
- Scheduler stale-order cleanup passed: stale candidates 0, cancel attempts 0, remaining open autopilot orders 0.
- Recommendation shortlist: AMZN, NKE, NEE, BAC, SO skipped because same-session validation history and daily order budget block new buys; HD, INTC, PLTR, FCX, MSFT, SPY, QQQ retained as recheck names.
- Validation: universe strict PASS, MCP strict PASS, risk policy PASS for empty order plan. Alpaca core pass; SEC EDGAR/FRED/Firecrawl/Yahoo pass; Alpha Vantage gap `empty_response`.
- Submitted/skipped orders: no orders submitted. First blocking gate: `risk_daily_new_orders_budget` because 10 scheduled validation buy orders had already been created for the 2026-05-27 ET session.
- Manifest: `wiki/evidence-store/run-manifests/2026-05-28-0351-hourly-autopilot.json`. Order plan: `wiki/trade-ledger/orders/2026-05-28-0351-hourly-autopilot.json`. Report: `wiki/current-runs/daily/2026-05-28-0351-hourly-autopilot.md`.
- Review due markers: 신규 체결 없음. Existing filled validation buys remain queued for 1D/5D/20D analyst review.

## [2026-05-28 04:13 Asia/Seoul] hourly-autopilot | 2026-05-28-0411-hourly-autopilot scheduled paper autopilot

- Run id: `2026-05-28-0411-hourly-autopilot`. Market clock open at `2026-05-27T15:11:09.622434462-04:00`, next close `2026-05-27T16:00:00-04:00`.
- Scheduler stale-order cleanup passed: stale candidates 0, cancel attempts 0, remaining open autopilot orders 0.
- Recommendation shortlist: AMZN, V, BAC, SO skipped because same-session validation history and daily order budget block new buys; MSFT, NVDA, FCX, SLB, PLTR, INTC, SPY, QQQ retained as recheck names.
- Validation: universe strict PASS, MCP strict PASS, risk policy PASS for empty order plan. Alpaca core pass; SEC EDGAR/FRED/Firecrawl/Yahoo pass; Alpha Vantage gap `empty_response`.
- Submitted/skipped orders: no orders submitted. First blocking gate: `risk_daily_new_orders_budget` because 10 scheduled validation buy orders had already been created for the 2026-05-27 ET session.
- Manifest: `wiki/evidence-store/run-manifests/2026-05-28-0411-hourly-autopilot.json`. Order plan: `wiki/trade-ledger/orders/2026-05-28-0411-hourly-autopilot.json`. Report: `wiki/current-runs/daily/2026-05-28-0411-hourly-autopilot.md`.
- Review due markers: 신규 체결 없음. Existing filled validation buys remain queued for 1D/5D/20D analyst review.

## [2026-05-28 04:33 Asia/Seoul] hourly-autopilot | 2026-05-28-0431-hourly-autopilot scheduled paper autopilot

- Run id: `2026-05-28-0431-hourly-autopilot`. Market clock open at `2026-05-27T15:31:11.670858081-04:00`, next close `2026-05-27T16:00:00-04:00`.
- Scheduler stale-order cleanup passed: stale candidates 0, cancel attempts 0, remaining open autopilot orders 0.
- Recommendation shortlist: AMZN, WMT, BAC, SO, NKE skipped because same-session validation history and daily order budget block new buys; SPY, QQQ, FCX, COP, SLB, SBUX, HON retained as recheck names.
- Validation: universe strict PASS, MCP strict PASS, risk policy PASS for empty order plan. Alpaca core pass; SEC EDGAR/FRED/Firecrawl/Yahoo pass; Alpha Vantage gap `empty_response`.
- Submitted/skipped orders: no orders submitted. First blocking gate: `risk_daily_new_orders_budget` because 10 scheduled validation buy orders had already been created for the 2026-05-27 ET session.
- Manifest: `wiki/evidence-store/run-manifests/2026-05-28-0431-hourly-autopilot.json`. Order plan: `wiki/trade-ledger/orders/2026-05-28-0431-hourly-autopilot.json`. Report: `wiki/current-runs/daily/2026-05-28-0431-hourly-autopilot.md`.
- Review due markers: 신규 체결 없음. Existing filled validation buys remain queued for 1D/5D/20D analyst review.

## [2026-05-28 04:53 Asia/Seoul] hourly-autopilot | 2026-05-28-0451-hourly-autopilot scheduled paper autopilot

- Run id: `2026-05-28-0451-hourly-autopilot`. Market clock open at `2026-05-27T15:51:11.90038039-04:00`, next close `2026-05-27T16:00:00-04:00`.
- Scheduler stale-order cleanup passed: stale candidates 0, cancel attempts 0; core preflight open orders list was empty.
- Recommendation shortlist: AMZN, NEE, WMT, BAC, SO, NKE skipped because same-session validation history and daily order budget block new buys; SPY, QQQ, COP, SLB, PLTR retained as recheck names; HOOD also failed spread gate.
- Validation: universe strict PASS, MCP strict PASS, risk policy PASS for empty order plan. Alpaca core pass; SEC EDGAR/FRED/Firecrawl/Yahoo pass; Alpha Vantage gap `empty_response`.
- Submitted/skipped orders: no orders submitted. First blocking gate: `risk_daily_new_orders_budget` because 10 scheduled validation buy orders had already been created for the 2026-05-27 ET session.
- Manifest: `wiki/evidence-store/run-manifests/2026-05-28-0451-hourly-autopilot.json`. Order plan: `wiki/trade-ledger/orders/2026-05-28-0451-hourly-autopilot.json`. Report: `wiki/current-runs/daily/2026-05-28-0451-hourly-autopilot.md`.
- Review due markers: 신규 체결 없음. Existing filled validation buys remain queued for 1D/5D/20D analyst review.

## [2026-05-28 06:22 Asia/Seoul] analyst-review | scheduled analyst review cycle

- Workflow: `harness/workflows/analyst-review-cycle.md`. 주문 제출/교체/취소/청산 없음.
- Paper mode: `ALPACA_PAPER_TRADE=true`.
- Alpaca reconciliation: account/clock/positions/open orders/closed orders/fills/bars/snapshots/news pass. Portfolio value 101515.43 USD, cash 41175.98 USD, buying power 136375.98 USD, long market value 60339.45 USD, open orders 0. `get_portfolio_history`는 2회 cancelled로 `gap_category=cancelled`, `retry_count=1`.
- Due review: 2026-05-26 validation fills LLY/FCX/NOK/NVDA/AAPL 1D interim review 작성. LLY +0.45%, AAPL +0.48%는 SPY/QQQ 대비 양호했고 FCX -0.49%, NVDA -0.54%는 보류, NOK -4.97%는 breakout 직후 추가 진입 리스크가 확인됐다.
- 2026-05-27 validation fills NKE/PFE/SO/WMT/NEE/AMZN/BAC/XOM/V는 신규 체결로 1D/5D/20D 회고 대기. GOOGL canceled order와 AMZN expired order는 filled_qty 0이라 trade review 대상에서 제외.
- MCP coverage: SEC EDGAR LLY/NVDA recent filings pass, Yahoo Finance LLY/NVDA news pass. Alpha Vantage `TOOL_LIST` 및 `TOOL_GET("PING")` pass 후 `TOOL_CALL("PING", {})` cancelled. FRED/Firecrawl은 registered tool 미노출로 shell/curl probing 없이 `wrapper_error`.
- Artifacts: [[2026-05-28-portfolio-review]], [[2026-05-28-0622-analyst-review-cycle-sources]], `wiki/evidence-store/run-manifests/2026-05-28-0622-analyst-review-cycle.json`, [[portfolio-current]].
- Policy update: 없음. 1D 표본만으로 threshold 미달이며 5D/20D와 portfolio-history gap 해소가 필요하다.

## [2026-05-28 06:45 Asia/Seoul] policy | active instruction source-of-truth cleanup

- 문제: active 운영 문서와 workflow가 `harness/risk-policy.yaml`, `harness/recommendation-policy.yaml`의 숫자 정책을 복제해 10건/20건/validation slot 기준 혼선을 만들었다.
- 조치: `AGENTS.md`, `README.md`, `harness/risk-policy.md`, `harness/agent-tasking-guide.md`, `harness/mcp-source-map.md`, `harness/workflows/daily.md`, `harness/workflows/hourly-autopilot.md`, `harness/workflows/rebalance.md`, `harness/workflows/intraday-paper-dry-run.md`, `scheduler/README.md`에서 active numeric cap/threshold 복제를 제거하고 source YAML key 참조로 변경했다.
- Source of truth: risk/order/liquidity/lifecycle numeric caps는 `harness/risk-policy.yaml`, recommendation cadence/MCP gate/validation sizing은 `harness/recommendation-policy.yaml`, intraday signal thresholds는 `harness/strategies/intraday-rs-breakout-v0.yaml` 및 `harness/strategies/intraday-rs-breadth-vwap-v1.yaml`.
- Historical wiki run reports/log entries는 당시 실제 판단 기록이므로 임의 수정하지 않았다. 이후 해석 시 이 항목을 correction note로 사용한다.
- 검증: active instruction scan에서 hardcoded policy cap 잔재는 source YAML로만 남았다. `python3 -m unittest tests.test_strategy_config_schema tests.test_check_risk_policy` PASS. 전체 `python3 -m unittest discover -s tests`는 기존 dashboard fixture성 실패 1건(`test_dashboard_run_metrics_fall_back_to_portfolio_snapshot`, picks 0개)로 FAIL.
- 후속 하네스 보강: `scripts/check-policy-source-of-truth.py`와 `tests/test_policy_source_of_truth.py`를 추가해 active Markdown 지침에 정책 숫자 cap/threshold가 다시 들어오면 실패하도록 했다. `harness/workflows/wiki-lint.md`에도 이 check를 blocking source-of-truth drift 항목으로 추가했다.
- 추가 검증: `python3 scripts/check-policy-source-of-truth.py` PASS. `python3 -m unittest tests.test_policy_source_of_truth tests.test_strategy_config_schema tests.test_check_risk_policy` PASS. 전체 `python3 -m unittest discover -s tests`는 동일한 dashboard fixture성 실패 1건으로 FAIL.
- Review correction: [[2026-05-28-portfolio-review]] 안의 2026-05-27 후속 run 10건 daily validation budget 평가는 legacy 문서 중복 오염으로 정정했다. 해당 run들의 no-submit 판단은 active YAML 기준으로 별도 재평가 대상이다.

## [2026-05-28 07:00 Asia/Seoul] runtime-probe | Alpaca after-hours paper order probe

- 목적: 장외 시간에도 Alpaca paper `place_stock_order` runtime submit/reconcile/cancel 경로가 실제 동작하는지 확인.
- 하네스 보강: `scripts/probe-alpaca-after-hours-order.py`를 추가했다. 이 probe는 Alpaca MCP만 사용하며 `ALPACA_PAPER_TRADE=true`를 요구하고, `extended_hours=true` day limit paper buy 주문을 idempotent `client_order_id`로 제출한 뒤 `get_order_by_client_id`로 reconcile하고 즉시 `cancel_order_by_id`로 취소한다.
- Dry-run: `2026-05-28-0654-after-hours-probe-dry-run` PASS. Market clock `is_open=false`, quote/asset lookup pass, 실제 주문 제출 없음.
- Execute probe: `2026-05-28-0700-after-hours-probe` PASS. Market clock `is_open=false` at `2026-05-27T17:59:25.985046256-04:00`, SPY 1주 buy limit 525.27, `extended_hours=true`, client_order_id `probe-20260527-215924-spy-eh`. Submit/reconcile/cancel 모두 pass.
- Evidence: `wiki/evidence-store/sources/2026-05-28-0700-after-hours-probe-alpaca-after-hours-order-probe.json`.
- 검증: `python3 -m unittest tests.test_mcp_runtime_wrappers tests.test_policy_source_of_truth tests.test_strategy_config_schema tests.test_check_risk_policy` PASS.

## [2026-05-28 12:30 Asia/Seoul] hourly-autopilot | explicit after-hours paper order probe

- 실행 경로: `CODEX_AUTOPILOT_AFTER_HOURS_ORDER_PROBE=1 scripts/run-hourly-autopilot-codex.sh`.
- 하네스 보강: `run-hourly-autopilot-codex.sh`에 명시적 장외 probe flag를 추가했다. 기본 scheduled autopilot은 market closed 시 기존처럼 research/Codex/order planning 전 종료한다. 이 flag가 있을 때만 closed-market wakeup에서 `scripts/probe-alpaca-after-hours-order.py --execute`를 호출한다.
- Market clock: `is_open=false`, timestamp `2026-05-27T23:30:28.501422736-04:00`, next open `2026-05-28T09:30:00-04:00`.
- Probe order: SPY 1주 buy limit 525.27, `time_in_force=day`, `extended_hours=true`, client_order_id `probe-20260528-033027-spy-eh`.
- Runtime result: `place_stock_order` pass, `get_order_by_client_id` reconcile pass, `cancel_order_by_id` pass. Submit status was `pending_new` before cancellation.
- Evidence: `wiki/evidence-store/sources/2026-05-28-1230-hourly-autopilot-after-hours-order-probe.json`.
- 검증: `bash -n scripts/run-hourly-autopilot-codex.sh`, `python3 -m unittest tests.test_mcp_runtime_wrappers`, `python3 scripts/check-policy-source-of-truth.py` PASS.

## [2026-05-28 12:43 Asia/Seoul] policy | after-hours autopilot separation

- 정책 판단: 장외 paper 운영은 정규장 `hourly-autopilot`과 같은 Alpaca MCP/risk validator 하네스를 공유하되, 정책 profile, 주문 예산, artifact tag, review bucket은 분리한다.
- Source of truth: `harness/recommendation-policy.yaml`에 `after_hours_policy`를 추가했다. 장외 허용 여부, session name, artifact tag, review bucket, client id prefix, extended-hours requirement, separate budget requirement, sizing/spread/quote/lifecycle 기준은 이 YAML만 source of truth로 둔다.
- Schema/validator: `harness/recommendation-policy.schema.json`과 `harness/order-plan.schema.json`을 확장했고, `scripts/check-risk-policy.py`가 `market.session=after_hours`, per-order `session=after_hours`, `extended_hours=true`, 장외 전용 `review_bucket`, `risk_inputs.after_hours_new_orders_submitted_today`를 검증하도록 했다.
- Workflow: `harness/workflows/after-hours-autopilot.md`를 추가했다. `harness/workflows/hourly-autopilot.md`, `AGENTS.md`, `harness/simple-commands.md`, `scheduler/README.md`에는 장외가 정규장 validation과 섞이지 않도록 경계 문구를 추가했다.
- 검증: `python3 -m unittest tests.test_check_risk_policy tests.test_strategy_config_schema tests.test_mcp_runtime_wrappers tests.test_policy_source_of_truth` PASS. `python3 scripts/check-policy-source-of-truth.py` PASS.

## [2026-05-28 12:52 Asia/Seoul] runtime-test | regular vs after-hours autopilot separation

- 정규장 기본 wrapper 검증: `scripts/run-hourly-autopilot-codex.sh`를 장외 시간에 실행했다. Alpaca clock `is_open=false`, timestamp `2026-05-27T23:52:15.251271349-04:00`; wrapper는 `scheduled autopilot exits before research/Codex run`로 종료했다. 주문, 장외 probe, report, manifest, order plan 생성 없음.
- 장외 explicit wrapper 검증: `CODEX_AUTOPILOT_AFTER_HOURS_ORDER_PROBE=1 scripts/run-hourly-autopilot-codex.sh`를 단독 실행했다. Alpaca clock `is_open=false`, timestamp `2026-05-27T23:52:25.655921526-04:00`; `scripts/probe-alpaca-after-hours-order.py --execute` 경로만 실행했다.
- 장외 주문 결과: SPY 1주 buy limit 525.27, `time_in_force=day`, `extended_hours=true`, client_order_id `probe-20260528-035224-spy-eh`. `place_stock_order` pass, `get_order_by_client_id` pass, `cancel_order_by_id` pass. Submit 직후 status는 `pending_new`였고 즉시 취소했다.
- Evidence: `wiki/evidence-store/sources/2026-05-28-1252-hourly-autopilot-after-hours-order-probe.json`.
- 분리 확인: 정규장 기본 run은 closed-market에서 artifact 없이 종료했고, 장외 run은 explicit flag가 있을 때만 after-hours evidence artifact를 생성했다.
- 검증: `python3 -m unittest tests.test_check_risk_policy tests.test_strategy_config_schema tests.test_mcp_runtime_wrappers tests.test_policy_source_of_truth` PASS. `python3 scripts/check-policy-source-of-truth.py` PASS.

## [2026-05-28 13:04 Asia/Seoul] scheduler | after-hours autopilot cadence enabled

- 요청: 장외 autopilot도 정규장과 정책 혼선 없이 독립 파라미터로 20분마다 실행.
- 정책 보강: `harness/recommendation-policy.yaml`의 `after_hours_policy.cadence`에 장외 전용 cadence, launch minutes, KST hour window, overlap behavior, regular-market behavior를 추가했다. 정규장 `cadence_policy`와 별도 key로 유지한다.
- Runner 보강: `scripts/run-after-hours-autopilot-codex.sh`를 장외 전용 Codex workflow runner로 구현했다. 수동 runtime probe 반복이 아니라 `harness/workflows/after-hours-autopilot.md`를 실행하며, 별도 lock `.locks/after-hours-autopilot.lock`, run label `after-hours-autopilot`, after-hours research cache를 사용한다.
- 정규장 충돌 방지: 장외 runner는 Alpaca regular market이 open이면 workflow 시작 전 종료한다. 정규장 runner는 market closed에서 기존처럼 종료한다.
- Scheduler: `scheduler/com.insightque.stock-alpaca.after-hours-autopilot.plist.example`를 추가했고, `~/Library/LaunchAgents/com.insightque.stock-alpaca.after-hours-autopilot.plist`로 설치 후 `launchctl bootstrap/enable` 완료. `launchctl print gui/501/com.insightque.stock-alpaca.after-hours-autopilot`에서 LaunchAgent 등록, program path, stdout/stderr path, calendar triggers 확인.
- Smoke runtime: `CODEX_AFTER_HOURS_AUTOPILOT_RUNTIME_SMOKE_TEST=1 scripts/run-after-hours-autopilot-codex.sh` PASS. Alpaca regular market closed 상태에서 after-hours runner가 Alpaca/research preflight까지 도달했고, smoke flag에서 Codex submit workflow 전 정상 종료했다.
- 검증: `python3 -m unittest tests.test_mcp_runtime_wrappers tests.test_strategy_config_schema tests.test_check_risk_policy tests.test_policy_source_of_truth` PASS. `python3 scripts/check-policy-source-of-truth.py` PASS. `plutil -lint` for regular and after-hours plist PASS.

## [2026-05-28 13:20 Asia/Seoul] after-hours-autopilot | 2026-05-28-1311-after-hours-autopilot scheduled after-hours paper autopilot

- Workflow: `harness/workflows/after-hours-autopilot.md`. Paper mode `ALPACA_PAPER_TRADE=true`; session=`after_hours`; artifact tag=`after-hours`; review bucket=`after_hours_validation`.
- Scheduler preflight: `wiki/evidence-store/sources/2026-05-28-1311-after-hours-autopilot-alpaca-core-preflight.json` and `wiki/evidence-store/sources/2026-05-28-1311-after-hours-autopilot-research-mcp-preflight.json` used. Alpaca core `first_blocking_gate=market_closed` was treated as expected non-blocking for after-hours; account/positions/open orders/assets/quotes rows were usable.
- Gates: Alpaca regular market closed; universe strict PASS; MCP strict PASS with SEC EDGAR/FRED/Firecrawl/Yahoo pass and Alpha Vantage `empty_response` gap; risk policy PASS with `risk_inputs.after_hours_new_orders_submitted_today=0`; INTC overnight quote/spread gate PASS.
- Submitted order: INTC 1주 buy limit 116.80, `time_in_force=day`, `extended_hours=true`, `session=after_hours`, client_order_id `ah-20260528-1311-intc-buy-01`. Submitted through Alpaca MCP only.
- Reconciliation: `get_order_by_client_id` returned order id `843838bd-6083-481d-b013-5ec7b0bf47fd`, status filled, filled_qty 1, filled_avg_price 116.79. No retry with a different client order id.
- Artifacts: `wiki/evidence-store/run-manifests/2026-05-28-1311-after-hours-autopilot.json`, `wiki/trade-ledger/orders/2026-05-28-1311-after-hours-autopilot.json`, [[2026-05-28-1311-after-hours-autopilot]], `wiki/trade-ledger/positions/2026-05-28-1311-after-hours-autopilot-post-trade.json`.
- Review due markers: INTC after-hours validation fill enters the separate `after_hours_validation` review bucket for next_regular_open, 1D, 5D, and 20D review horizons.

## [2026-05-28 13:33 Asia/Seoul] scheduler | after-hours autopilot messenger updates

- 요청: 장외 autopilot도 메신저에 현황 및 거래내역 업데이트.
- 구현: `scripts/send-openclaw-autopilot-update.py`를 추가했다. run manifest, order plan, daily report를 읽어 start/skip/failure/completion 상태와 주문 수량, limit, `extended_hours`, client order id, reconcile/fill 결과를 OpenClaw `message send`로 요약 발송한다.
- Runner 연결: `scripts/run-after-hours-autopilot-codex.sh`가 start, skip, failure, completion 경로에서 notifier를 호출한다. 예기치 않은 non-zero exit도 cleanup trap에서 failure 알림을 보내도록 했다. `OPENCLAW_AUTOPILOT_NOTIFY_TARGET`이 없으면 run 실패 없이 알림만 skip한다.
- Scheduler: example LaunchAgent에 `OPENCLAW_AUTOPILOT_NOTIFY_CHANNEL=telegram`, `OPENCLAW_AUTOPILOT_NOTIFY_TARGET` placeholder를 추가했고, 설치된 `~/Library/LaunchAgents/com.insightque.stock-alpaca.after-hours-autopilot.plist`에는 현재 Telegram chat id를 반영 후 `launchctl bootstrap/enable`로 재로드했다.
- Runtime 검증: `CODEX_AFTER_HOURS_AUTOPILOT_RUNTIME_SMOKE_TEST=1 CODEX_AFTER_HOURS_AUTOPILOT_NOTIFY=0 scripts/run-after-hours-autopilot-codex.sh` PASS. Alpaca regular market closed 상태에서 preflight까지 도달 후 smoke flag로 정상 종료.
- 검증: `python3 -m unittest tests.test_mcp_runtime_wrappers tests.test_strategy_config_schema tests.test_check_risk_policy tests.test_policy_source_of_truth` PASS. `python3 scripts/check-policy-source-of-truth.py` PASS. after-hours plist example 및 설치본 `plutil -lint` PASS.

## [2026-05-28 13:59 Asia/Seoul] after-hours-autopilot | 2026-05-28-1351-after-hours-autopilot scheduled after-hours paper autopilot

- Workflow: `harness/workflows/after-hours-autopilot.md`. Paper mode `ALPACA_PAPER_TRADE=true`; session=`after_hours`; artifact tag=`after-hours`; review bucket=`after_hours_validation`.
- Scheduler preflight: `wiki/evidence-store/sources/2026-05-28-1351-after-hours-autopilot-alpaca-core-preflight.json` and `wiki/evidence-store/sources/2026-05-28-1351-after-hours-autopilot-research-mcp-preflight.json` used. Alpaca core `first_blocking_gate=market_closed` was treated as expected non-blocking for after-hours; account/positions/open orders/assets/quotes rows were usable.
- Gates: Alpaca regular market closed; universe strict PASS; MCP strict PASS with SEC EDGAR/FRED/Firecrawl/Yahoo pass and Alpha Vantage `empty_response` gap; risk policy PASS with `risk_inputs.after_hours_new_orders_submitted_today=1`; NOK fresh overnight quote/spread gate PASS.
- Submitted order: NOK 1주 buy limit 15.40, `time_in_force=day`, `extended_hours=true`, `session=after_hours`, client_order_id `ah-20260528-1351-nok-buy-01`. Submitted through Alpaca MCP only after the pre-submit gate summary.
- Reconciliation: `get_order_by_client_id` returned order id `98b8dbb6-7bcd-4e12-bcd8-d6ebb9853064`, status filled, filled_qty 1, filled_avg_price 15.40. No retry with a different client order id.
- Post-trade: Alpaca MCP account/positions/open orders check confirmed no open US equity orders and NOK position qty 402.
- Artifacts: `wiki/evidence-store/run-manifests/2026-05-28-1351-after-hours-autopilot.json`, `wiki/trade-ledger/orders/2026-05-28-1351-after-hours-autopilot.json`, [[2026-05-28-1351-after-hours-autopilot]], `wiki/trade-ledger/positions/2026-05-28-1351-after-hours-autopilot-post-trade.json`.
- Review due markers: NOK after-hours validation fill enters the separate `after_hours_validation` review bucket for next_regular_open, 1D, 5D, and 20D review horizons.

## [2026-05-28 14:13 Asia/Seoul] after-hours-autopilot | 2026-05-28-1411-after-hours-autopilot scheduled after-hours paper autopilot

- Workflow: `harness/workflows/after-hours-autopilot.md`. Paper mode `ALPACA_PAPER_TRADE=true`; session=`after_hours`; artifact tag=`after-hours`; review bucket=`after_hours_validation`.
- Scheduler preflight: `wiki/evidence-store/sources/2026-05-28-1411-after-hours-autopilot-alpaca-core-preflight.json` and `wiki/evidence-store/sources/2026-05-28-1411-after-hours-autopilot-research-mcp-preflight.json` used. Alpaca core `first_blocking_gate=market_closed` was treated as expected non-blocking for after-hours; account/positions/open orders/assets/quotes rows were usable.
- Fresh Alpaca MCP checks: regular market closed at `2026-05-28T01:13:25.825028326-04:00`; account ACTIVE; positions fetched; open US equity orders empty; same-day after-hours validation fills found for `ah-20260528-1311-intc-buy-01` and `ah-20260528-1351-nok-buy-01`.
- Gates: universe strict PASS; MCP strict PASS with SEC EDGAR/FRED/Firecrawl/Yahoo pass and Alpha Vantage `empty_response` gap. Separate after-hours order budget FAIL because `risk_inputs.after_hours_new_orders_submitted_today=2` and session cap is 2.
- Risk validation: `python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-05-28-1411-after-hours-autopilot.json` was executed and failed before policy evaluation because current system Python lacks PyYAML. This is treated as a failed risk gate.
- Submit/reconcile: no `place_stock_order` call, no submit attempt, no reconciliation required.
- Artifacts: `wiki/evidence-store/run-manifests/2026-05-28-1411-after-hours-autopilot.json`, `wiki/trade-ledger/orders/2026-05-28-1411-after-hours-autopilot.json`, [[2026-05-28-1411-after-hours-autopilot]].

## [2026-05-28 14:35 Asia/Seoul] after-hours-autopilot | 2026-05-28-1431-after-hours-autopilot scheduled after-hours paper autopilot

- Workflow: `harness/workflows/after-hours-autopilot.md`. Paper mode `ALPACA_PAPER_TRADE=true`; session=`after_hours`; artifact tag=`after-hours`; review bucket=`after_hours_validation`.
- Scheduler preflight: `wiki/evidence-store/sources/2026-05-28-1431-after-hours-autopilot-alpaca-core-preflight.json` and `wiki/evidence-store/sources/2026-05-28-1431-after-hours-autopilot-research-mcp-preflight.json` used. Alpaca core `first_blocking_gate=market_closed` was treated as expected non-blocking for after-hours.
- Fresh Alpaca MCP checks: regular market closed at `2026-05-28T01:32:44.745431459-04:00`; account ACTIVE; positions fetched; open US equity orders empty; same-day after-hours validation fills found for `ah-20260528-1311-intc-buy-01` and `ah-20260528-1351-nok-buy-01`.
- Gates: universe strict PASS; MCP strict PASS with SEC EDGAR/FRED/Firecrawl/Yahoo pass and Alpha Vantage `empty_response` gap. Separate after-hours order budget FAIL because `risk_inputs.after_hours_new_orders_submitted_today=2` and session cap is 2.
- Risk validation: `python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-05-28-1431-after-hours-autopilot.json` was executed and failed because current system Python lacks PyYAML. This is treated as a failed risk gate.
- Submit/reconcile: no `place_stock_order` call, no submit attempt, no reconciliation required.
- Artifacts: `wiki/evidence-store/run-manifests/2026-05-28-1431-after-hours-autopilot.json`, `wiki/trade-ledger/orders/2026-05-28-1431-after-hours-autopilot.json`, [[2026-05-28-1431-after-hours-autopilot]].

## [2026-05-28 14:54 Asia/Seoul] after-hours-autopilot | 2026-05-28-1451-after-hours-autopilot scheduled after-hours paper autopilot

- Workflow: `harness/workflows/after-hours-autopilot.md`. Paper mode `ALPACA_PAPER_TRADE=true`; session=`after_hours`; artifact tag=`after-hours`; review bucket=`after_hours_validation`.
- Scheduler preflight: `wiki/evidence-store/sources/2026-05-28-1451-after-hours-autopilot-alpaca-core-preflight.json` and `wiki/evidence-store/sources/2026-05-28-1451-after-hours-autopilot-research-mcp-preflight.json` used. Alpaca core `first_blocking_gate=market_closed` was treated as expected non-blocking for after-hours.
- Fresh Alpaca MCP checks: regular market closed at `2026-05-28T01:52:58.623272375-04:00`; account ACTIVE; positions fetched; open US equity orders empty; same-day after-hours validation fills found for `ah-20260528-1311-intc-buy-01` and `ah-20260528-1351-nok-buy-01`.
- Gates: universe strict PASS; MCP strict PASS with SEC EDGAR/FRED/Firecrawl/Yahoo pass and Alpha Vantage `empty_response` gap. Separate after-hours order budget FAIL because `risk_inputs.after_hours_new_orders_submitted_today=2` and session cap is 2.
- Risk validation: `python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-05-28-1451-after-hours-autopilot.json` PASS for the empty no-submit plan with `orders is empty` warning.
- Submit/reconcile: no `place_stock_order` call, no submit attempt, no reconciliation required.
- Artifacts: `wiki/evidence-store/run-manifests/2026-05-28-1451-after-hours-autopilot.json`, `wiki/trade-ledger/orders/2026-05-28-1451-after-hours-autopilot.json`, [[2026-05-28-1451-after-hours-autopilot]].

## [2026-05-28 15:14 Asia/Seoul] after-hours-autopilot | 2026-05-28-1511-after-hours-autopilot scheduled after-hours paper autopilot

- Workflow: `harness/workflows/after-hours-autopilot.md`. Paper mode `ALPACA_PAPER_TRADE=true`; session=`after_hours`; artifact tag=`after-hours`; review bucket=`after_hours_validation`.
- Scheduler preflight: `wiki/evidence-store/sources/2026-05-28-1511-after-hours-autopilot-alpaca-core-preflight.json` and `wiki/evidence-store/sources/2026-05-28-1511-after-hours-autopilot-research-mcp-preflight.json` used. Alpaca core `first_blocking_gate=market_closed` was treated as expected non-blocking for after-hours.
- Fresh Alpaca MCP checks: regular market closed at `2026-05-28T02:13:12.921549175-04:00`; account ACTIVE; positions fetched; open US equity orders empty. Direct fresh account-activities call was cancelled by the MCP runtime, so same-day after-hours fills were taken from the scheduler-owned Alpaca core preflight.
- Gates: universe strict PASS; MCP strict PASS with SEC EDGAR/FRED/Firecrawl/Yahoo pass and Alpha Vantage `empty_response` gap. Separate after-hours order budget FAIL because `risk_inputs.after_hours_new_orders_submitted_today=2` and session cap is 2.
- Risk validation: default `python3` lacked PyYAML, then `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-05-28-1511-after-hours-autopilot.json` PASS for the empty no-submit plan with `orders is empty` warning.
- Submit/reconcile: no `place_stock_order` call, no submit attempt, no reconciliation required.
- Artifacts: `wiki/evidence-store/run-manifests/2026-05-28-1511-after-hours-autopilot.json`, `wiki/trade-ledger/orders/2026-05-28-1511-after-hours-autopilot.json`, [[2026-05-28-1511-after-hours-autopilot]].

## [2026-05-28 15:34 Asia/Seoul] after-hours-autopilot | 2026-05-28-1531-after-hours-autopilot scheduled after-hours paper autopilot

- Workflow: `harness/workflows/after-hours-autopilot.md`. Paper mode `ALPACA_PAPER_TRADE=true`; session=`after_hours`; artifact tag=`after-hours`; review bucket=`after_hours_validation`.
- Scheduler preflight: `wiki/evidence-store/sources/2026-05-28-1531-after-hours-autopilot-alpaca-core-preflight.json` and `wiki/evidence-store/sources/2026-05-28-1531-after-hours-autopilot-research-mcp-preflight.json` used. Alpaca core `first_blocking_gate=market_closed` was treated as expected non-blocking for after-hours.
- Fresh Alpaca MCP checks: regular market closed at `2026-05-28T02:32:52.887013085-04:00`; account ACTIVE; positions fetched; open US equity orders empty; same-day after-hours validation fills found for `ah-20260528-1311-intc-buy-01` and `ah-20260528-1351-nok-buy-01`.
- Gates: universe strict PASS; MCP strict PASS with SEC EDGAR/FRED/Firecrawl/Yahoo pass and Alpha Vantage `empty_response` gap. Separate after-hours order budget FAIL because `risk_inputs.after_hours_new_orders_submitted_today=2` and session cap is 2.
- Risk validation: `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-05-28-1531-after-hours-autopilot.json` PASS for the empty no-submit plan with `orders is empty` warning. `python3 scripts/check-universe-coverage.py --strict --json ...` PASS. `python3 scripts/check-mcp-coverage.py --strict --json ...` PASS.
- Submit/reconcile: no `place_stock_order` call, no submit attempt, no reconciliation required.
- Artifacts: `wiki/evidence-store/run-manifests/2026-05-28-1531-after-hours-autopilot.json`, `wiki/trade-ledger/orders/2026-05-28-1531-after-hours-autopilot.json`, [[2026-05-28-1531-after-hours-autopilot]].

## [2026-05-28 15:53 Asia/Seoul] after-hours-autopilot | 2026-05-28-1551-after-hours-autopilot scheduled after-hours paper autopilot

- Workflow: `harness/workflows/after-hours-autopilot.md`. Paper mode `ALPACA_PAPER_TRADE=true`; session=`after_hours`; artifact tag=`after-hours`; review bucket=`after_hours_validation`.
- Scheduler preflight: `wiki/evidence-store/sources/2026-05-28-1551-after-hours-autopilot-alpaca-core-preflight.json` and `wiki/evidence-store/sources/2026-05-28-1551-after-hours-autopilot-research-mcp-preflight.json` used. Alpaca core `first_blocking_gate=market_closed` was treated as expected non-blocking for after-hours.
- Fresh Alpaca MCP checks: regular market closed at `2026-05-28T02:52:32.026145834-04:00`; account ACTIVE; positions fetched; open US equity orders empty; same-day after-hours validation fills found for `ah-20260528-1311-intc-buy-01` and `ah-20260528-1351-nok-buy-01`.
- Gates: universe strict PASS; MCP strict PASS with SEC EDGAR/FRED/Firecrawl/Yahoo pass and Alpha Vantage `empty_response` gap. Separate after-hours order budget FAIL because `risk_inputs.after_hours_new_orders_submitted_today=2` and session cap is 2.
- Risk validation: `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-05-28-1551-after-hours-autopilot.json` PASS for the empty no-submit plan with `orders is empty` warning. `python3 scripts/check-universe-coverage.py --strict --json ...` PASS. `python3 scripts/check-mcp-coverage.py --strict --json ...` PASS.
- Submit/reconcile: no `place_stock_order` call, no submit attempt, no reconciliation required.
- Artifacts: `wiki/evidence-store/run-manifests/2026-05-28-1551-after-hours-autopilot.json`, `wiki/trade-ledger/orders/2026-05-28-1551-after-hours-autopilot.json`, [[2026-05-28-1551-after-hours-autopilot]].

## [2026-05-28 16:14 Asia/Seoul] after-hours-autopilot | 2026-05-28-1611-after-hours-autopilot scheduled after-hours paper autopilot

- Workflow: `harness/workflows/after-hours-autopilot.md`. Paper mode `ALPACA_PAPER_TRADE=true`; session=`after_hours`; artifact tag=`after-hours`; review bucket=`after_hours_validation`.
- Scheduler preflight: `wiki/evidence-store/sources/2026-05-28-1611-after-hours-autopilot-alpaca-core-preflight.json` and `wiki/evidence-store/sources/2026-05-28-1611-after-hours-autopilot-research-mcp-preflight.json` used. Alpaca core `first_blocking_gate=market_closed` was treated as expected non-blocking for after-hours.
- Fresh Alpaca MCP checks: regular market closed at `2026-05-28T03:13:06.316432077-04:00`; account ACTIVE; positions fetched; open US equity orders empty; same-day after-hours validation fills found for `ah-20260528-1311-intc-buy-01` and `ah-20260528-1351-nok-buy-01`.
- Gates: universe strict PASS; MCP strict PASS with SEC EDGAR/FRED/Firecrawl/Yahoo pass and Alpha Vantage `empty_response` gap. Separate after-hours order budget FAIL because `risk_inputs.after_hours_new_orders_submitted_today=2` and session cap is 2.
- Risk validation: `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-05-28-1611-after-hours-autopilot.json` PASS for the empty no-submit plan with `orders is empty` warning. `python3 scripts/check-universe-coverage.py --strict --json ...` PASS. `python3 scripts/check-mcp-coverage.py --strict --json ...` PASS.
- Submit/reconcile: no `place_stock_order` call, no submit attempt, no reconciliation required.
- Artifacts: `wiki/evidence-store/run-manifests/2026-05-28-1611-after-hours-autopilot.json`, `wiki/trade-ledger/orders/2026-05-28-1611-after-hours-autopilot.json`, [[2026-05-28-1611-after-hours-autopilot]].

## [2026-05-28 16:34 Asia/Seoul] after-hours-autopilot | 2026-05-28-1631-after-hours-autopilot scheduled after-hours paper autopilot

- Workflow: `harness/workflows/after-hours-autopilot.md`. Paper mode `ALPACA_PAPER_TRADE=true`; session=`after_hours`; artifact tag=`after-hours`; review bucket=`after_hours_validation`.
- Scheduler preflight: `wiki/evidence-store/sources/2026-05-28-1631-after-hours-autopilot-alpaca-core-preflight.json` and `wiki/evidence-store/sources/2026-05-28-1631-after-hours-autopilot-research-mcp-preflight.json` used. Alpaca core `first_blocking_gate=market_closed` was treated as expected non-blocking for after-hours.
- Fresh Alpaca MCP checks: regular market closed at `2026-05-28T03:32:18.032350927-04:00`; account ACTIVE; positions fetched; open US equity orders empty; same-day after-hours validation fills found for `ah-20260528-1311-intc-buy-01` and `ah-20260528-1351-nok-buy-01`.
- Gates: universe strict PASS; MCP strict PASS with SEC EDGAR/FRED/Firecrawl/Yahoo pass and Alpha Vantage `empty_response` gap. Separate after-hours order budget FAIL because `risk_inputs.after_hours_new_orders_submitted_today=2` and session cap is 2.
- Risk validation: `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-05-28-1631-after-hours-autopilot.json` PASS for the empty no-submit plan with `orders is empty` warning. `python3 scripts/check-universe-coverage.py --strict --json ...` PASS. `python3 scripts/check-mcp-coverage.py --strict --json ...` PASS.
- Submit/reconcile: no `place_stock_order` call, no submit attempt, no reconciliation required.
- Artifacts: `wiki/evidence-store/run-manifests/2026-05-28-1631-after-hours-autopilot.json`, `wiki/trade-ledger/orders/2026-05-28-1631-after-hours-autopilot.json`, [[2026-05-28-1631-after-hours-autopilot]].

## [2026-05-28 16:54 Asia/Seoul] after-hours-autopilot | 2026-05-28-1651-after-hours-autopilot scheduled after-hours paper autopilot

- Workflow: `harness/workflows/after-hours-autopilot.md`. Paper mode `ALPACA_PAPER_TRADE=true`; session=`after_hours`; artifact tag=`after-hours`; review bucket=`after_hours_validation`.
- Scheduler preflight: `wiki/evidence-store/sources/2026-05-28-1651-after-hours-autopilot-alpaca-core-preflight.json` and `wiki/evidence-store/sources/2026-05-28-1651-after-hours-autopilot-research-mcp-preflight.json` used. Alpaca core `first_blocking_gate=market_closed` was treated as expected non-blocking for after-hours.
- Fresh Alpaca MCP checks: regular market closed at `2026-05-28T03:52:51.681399919-04:00`; account ACTIVE; positions fetched; open US equity orders empty; same-day after-hours validation fills found for `ah-20260528-1311-intc-buy-01` and `ah-20260528-1351-nok-buy-01`.
- Gates: universe strict PASS; MCP strict PASS with SEC EDGAR/FRED/Firecrawl/Yahoo pass and Alpha Vantage `empty_response` gap. Separate after-hours order budget FAIL because `risk_inputs.after_hours_new_orders_submitted_today=2` and session cap is 2.
- Risk validation: `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-05-28-1651-after-hours-autopilot.json` PASS for the empty no-submit plan with `orders is empty` warning. `python3 scripts/check-universe-coverage.py --strict --json ...` PASS. `python3 scripts/check-mcp-coverage.py --strict --json ...` PASS.
- Submit/reconcile: no `place_stock_order` call, no submit attempt, no reconciliation required.
- Artifacts: `wiki/evidence-store/run-manifests/2026-05-28-1651-after-hours-autopilot.json`, `wiki/trade-ledger/orders/2026-05-28-1651-after-hours-autopilot.json`, [[2026-05-28-1651-after-hours-autopilot]].

## [2026-05-28 17:13 Asia/Seoul] after-hours-autopilot | 2026-05-28-1711-after-hours-autopilot scheduled after-hours paper autopilot

- Workflow: `harness/workflows/after-hours-autopilot.md`. Paper mode `ALPACA_PAPER_TRADE=true`; session=`after_hours`; artifact tag=`after-hours`; review bucket=`after_hours_validation`.
- Scheduler preflight: `wiki/evidence-store/sources/2026-05-28-1711-after-hours-autopilot-alpaca-core-preflight.json` and `wiki/evidence-store/sources/2026-05-28-1711-after-hours-autopilot-research-mcp-preflight.json` used. Alpaca core `first_blocking_gate=market_closed` was treated as expected non-blocking for after-hours.
- Fresh Alpaca MCP checks: regular market closed at `2026-05-28T04:12:29.08983661-04:00`; account ACTIVE; positions fetched; open US equity orders empty; same-day after-hours validation fills found for `ah-20260528-1311-intc-buy-01` and `ah-20260528-1351-nok-buy-01`.
- Gates: universe strict PASS; MCP strict PASS with SEC EDGAR/FRED/Firecrawl/Yahoo pass and Alpha Vantage `empty_response` gap. Separate after-hours order budget FAIL because `risk_inputs.after_hours_new_orders_submitted_today=2` and session cap is 2.
- Risk validation: `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-05-28-1711-after-hours-autopilot.json` PASS for the empty no-submit plan with `orders is empty` warning. `PATH=/usr/local/bin:$PATH python3 scripts/check-universe-coverage.py --strict --json ...` PASS. `PATH=/usr/local/bin:$PATH python3 scripts/check-mcp-coverage.py --strict --json ...` PASS.
- Submit/reconcile: no `place_stock_order` call, no submit attempt, no reconciliation required.
- Artifacts: `wiki/evidence-store/run-manifests/2026-05-28-1711-after-hours-autopilot.json`, `wiki/trade-ledger/orders/2026-05-28-1711-after-hours-autopilot.json`, [[2026-05-28-1711-after-hours-autopilot]].

## [2026-05-28 17:34 Asia/Seoul] after-hours-autopilot | 2026-05-28-1731-after-hours-autopilot scheduled after-hours paper autopilot

- Workflow: `harness/workflows/after-hours-autopilot.md`. Paper mode `ALPACA_PAPER_TRADE=true`; session=`after_hours`; artifact tag=`after-hours`; review bucket=`after_hours_validation`.
- Scheduler preflight: `wiki/evidence-store/sources/2026-05-28-1731-after-hours-autopilot-alpaca-core-preflight.json` and `wiki/evidence-store/sources/2026-05-28-1731-after-hours-autopilot-research-mcp-preflight.json` used. Alpaca core `first_blocking_gate=market_closed` was treated as expected non-blocking for after-hours.
- Fresh Alpaca MCP checks: regular market closed at `2026-05-28T04:33:06.179331804-04:00`; account ACTIVE; open US equity orders empty. Fresh positions MCP call was blocked by the runtime safety monitor, so the scheduler-owned passing positions row was used per the after-hours instruction. Same-day after-hours validation fills found for `ah-20260528-1311-intc-buy-01` and `ah-20260528-1351-nok-buy-01`.
- Gates: universe strict PASS; MCP strict PASS with SEC EDGAR/FRED/Firecrawl/Yahoo pass and Alpha Vantage `empty_response` gap. Separate after-hours order budget FAIL because `risk_inputs.after_hours_new_orders_submitted_today=2` and session cap is 2.
- Risk validation: `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-05-28-1731-after-hours-autopilot.json` PASS for the empty no-submit plan with `orders is empty` warning. `PATH=/usr/local/bin:$PATH python3 scripts/check-universe-coverage.py --strict --json ...` PASS. `PATH=/usr/local/bin:$PATH python3 scripts/check-mcp-coverage.py --strict --json ...` PASS.
- Submit/reconcile: no `place_stock_order` call, no submit attempt, no reconciliation required.
- Artifacts: `wiki/evidence-store/run-manifests/2026-05-28-1731-after-hours-autopilot.json`, `wiki/trade-ledger/orders/2026-05-28-1731-after-hours-autopilot.json`, [[2026-05-28-1731-after-hours-autopilot]].

## [2026-05-28 17:54 Asia/Seoul] after-hours-autopilot | 2026-05-28-1751-after-hours-autopilot scheduled after-hours paper autopilot

- Workflow: `harness/workflows/after-hours-autopilot.md`. Paper mode `ALPACA_PAPER_TRADE=true`; session=`after_hours`; artifact tag=`after-hours`; review bucket=`after_hours_validation`.
- Scheduler preflight: `wiki/evidence-store/sources/2026-05-28-1751-after-hours-autopilot-alpaca-core-preflight.json` and `wiki/evidence-store/sources/2026-05-28-1751-after-hours-autopilot-research-mcp-preflight.json` used. Alpaca core `first_blocking_gate=market_closed` was treated as expected non-blocking for after-hours.
- Fresh Alpaca MCP checks: regular market closed at `2026-05-28T04:53:28.46560802-04:00`; account ACTIVE; positions fetched; open US equity orders empty; same-day after-hours validation fills reconciled by client order id for `ah-20260528-1311-intc-buy-01` and `ah-20260528-1351-nok-buy-01`.
- Gates: universe strict PASS; MCP strict PASS with SEC EDGAR/FRED/Firecrawl/Yahoo pass and Alpha Vantage `empty_response` gap. Separate after-hours order budget FAIL because `risk_inputs.after_hours_new_orders_submitted_today=2` and session cap is 2.
- Risk validation: `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-05-28-1751-after-hours-autopilot.json` PASS for the empty no-submit plan with `orders is empty` warning. `PATH=/usr/local/bin:$PATH python3 scripts/check-universe-coverage.py --strict --json ...` PASS. `PATH=/usr/local/bin:$PATH python3 scripts/check-mcp-coverage.py --strict --json ...` PASS.
- Submit/reconcile: no `place_stock_order` call, no submit attempt, no new reconciliation required.
- Artifacts: `wiki/evidence-store/run-manifests/2026-05-28-1751-after-hours-autopilot.json`, `wiki/trade-ledger/orders/2026-05-28-1751-after-hours-autopilot.json`, [[2026-05-28-1751-after-hours-autopilot]].

## [2026-05-28 18:14 Asia/Seoul] after-hours-autopilot | 2026-05-28-1811-after-hours-autopilot scheduled after-hours paper autopilot

- Workflow: `harness/workflows/after-hours-autopilot.md`. Paper mode `ALPACA_PAPER_TRADE=true`; session=`after_hours`; artifact tag=`after-hours`; review bucket=`after_hours_validation`.
- Scheduler preflight: `wiki/evidence-store/sources/2026-05-28-1811-after-hours-autopilot-alpaca-core-preflight.json` and `wiki/evidence-store/sources/2026-05-28-1811-after-hours-autopilot-research-mcp-preflight.json` used. Alpaca core `first_blocking_gate=market_closed` was treated as expected non-blocking for after-hours.
- Fresh Alpaca MCP checks: regular market closed at `2026-05-28T05:13:16.746679992-04:00`; account ACTIVE; positions fetched. Fresh open-order call was blocked by the runtime safety monitor, so the scheduler-owned passing open-order row was used. Same-day after-hours validation fills recorded for `ah-20260528-1311-intc-buy-01` and `ah-20260528-1351-nok-buy-01`.
- Gates: universe strict PASS; MCP strict PASS with SEC EDGAR/FRED/Firecrawl/Yahoo pass and Alpha Vantage `empty_response` gap. Separate after-hours order budget FAIL because `risk_inputs.after_hours_new_orders_submitted_today=2` and session cap is 2.
- Risk validation: `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-05-28-1811-after-hours-autopilot.json` PASS for the empty no-submit plan with `orders is empty` warning. `PATH=/usr/local/bin:$PATH python3 scripts/check-universe-coverage.py --strict --json ...` PASS. `PATH=/usr/local/bin:$PATH python3 scripts/check-mcp-coverage.py --strict --json ...` PASS.
- Submit/reconcile: no `place_stock_order` call, no submit attempt, no reconciliation required.
- Artifacts: `wiki/evidence-store/run-manifests/2026-05-28-1811-after-hours-autopilot.json`, `wiki/trade-ledger/orders/2026-05-28-1811-after-hours-autopilot.json`, [[2026-05-28-1811-after-hours-autopilot]].

## [2026-05-28 18:33 Asia/Seoul] after-hours-autopilot | 2026-05-28-1831-after-hours-autopilot scheduled after-hours paper autopilot

- Workflow: `harness/workflows/after-hours-autopilot.md`. Paper mode `ALPACA_PAPER_TRADE=true`; session=`after_hours`; artifact tag=`after-hours`; review bucket=`after_hours_validation`.
- Scheduler preflight: `wiki/evidence-store/sources/2026-05-28-1831-after-hours-autopilot-alpaca-core-preflight.json` and `wiki/evidence-store/sources/2026-05-28-1831-after-hours-autopilot-research-mcp-preflight.json` used. Alpaca core `first_blocking_gate=market_closed` was treated as expected non-blocking for after-hours because required account, positions, orders, activity, asset, quote, and spread rows passed.
- Fresh Alpaca MCP checks: regular market closed at `2026-05-28T05:32:32.28064454-04:00`; account ACTIVE; positions fetched; open US equity orders empty; same-day after-hours validation fills found for `ah-20260528-1311-intc-buy-01` and `ah-20260528-1351-nok-buy-01`.
- Gates: universe strict PASS; MCP strict PASS with SEC EDGAR/FRED/Firecrawl/Yahoo pass and Alpha Vantage `empty_response` gap. Separate after-hours order budget FAIL because `risk_inputs.after_hours_new_orders_submitted_today=2` and session cap is 2.
- Risk validation: `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-05-28-1831-after-hours-autopilot.json` PASS for the empty no-submit plan with `orders is empty` warning. `PATH=/usr/local/bin:$PATH python3 scripts/check-universe-coverage.py --strict --json ...` PASS. `PATH=/usr/local/bin:$PATH python3 scripts/check-mcp-coverage.py --strict --json ...` PASS.
- Submit/reconcile: no `place_stock_order` call, no submit attempt, no reconciliation required.
- Artifacts: `wiki/evidence-store/run-manifests/2026-05-28-1831-after-hours-autopilot.json`, `wiki/trade-ledger/orders/2026-05-28-1831-after-hours-autopilot.json`, [[2026-05-28-1831-after-hours-autopilot]].

## [2026-05-28 18:54 Asia/Seoul] after-hours-autopilot | 2026-05-28-1851-after-hours-autopilot scheduled after-hours paper autopilot

- Workflow: `harness/workflows/after-hours-autopilot.md`. Paper mode `ALPACA_PAPER_TRADE=true`; session=`after_hours`; artifact tag=`after-hours`; review bucket=`after_hours_validation`.
- Scheduler preflight: `wiki/evidence-store/sources/2026-05-28-1851-after-hours-autopilot-alpaca-core-preflight.json` and `wiki/evidence-store/sources/2026-05-28-1851-after-hours-autopilot-research-mcp-preflight.json` used. Alpaca core `first_blocking_gate=market_closed` was treated as expected non-blocking for after-hours because required account, positions, orders, activity, asset, quote, and spread rows passed.
- Fresh Alpaca MCP checks: account ACTIVE; positions fetched; open US equity orders empty; same-day after-hours validation fills reconciled by client order id for `ah-20260528-1311-intc-buy-01` and `ah-20260528-1351-nok-buy-01`. A fresh clock MCP spot-check was cancelled by the runtime, so the scheduler-owned passing clock row was used.
- Gates: universe strict PASS; MCP strict PASS with SEC EDGAR/FRED/Firecrawl/Yahoo pass and Alpha Vantage `empty_response` gap. Separate after-hours order budget FAIL because `risk_inputs.after_hours_new_orders_submitted_today=2` and session cap is 2.
- Risk validation: `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-05-28-1851-after-hours-autopilot.json` PASS for the empty no-submit plan with `orders is empty` warning. `PATH=/usr/local/bin:$PATH python3 scripts/check-universe-coverage.py --strict --json ...` PASS. `PATH=/usr/local/bin:$PATH python3 scripts/check-mcp-coverage.py --strict --json ...` PASS.
- Submit/reconcile: no `place_stock_order` call, no submit attempt, no new reconciliation required.
- Artifacts: `wiki/evidence-store/run-manifests/2026-05-28-1851-after-hours-autopilot.json`, `wiki/trade-ledger/orders/2026-05-28-1851-after-hours-autopilot.json`, [[2026-05-28-1851-after-hours-autopilot]].

## [2026-05-28 19:13 Asia/Seoul] after-hours-autopilot | 2026-05-28-1911-after-hours-autopilot scheduled after-hours paper autopilot

- Workflow: `harness/workflows/after-hours-autopilot.md`. Paper mode `ALPACA_PAPER_TRADE=true`; session=`after_hours`; artifact tag=`after-hours`; review bucket=`after_hours_validation`.
- Scheduler preflight: `wiki/evidence-store/sources/2026-05-28-1911-after-hours-autopilot-alpaca-core-preflight.json` and `wiki/evidence-store/sources/2026-05-28-1911-after-hours-autopilot-research-mcp-preflight.json` used. Alpaca core `first_blocking_gate=market_closed` was treated as expected non-blocking for after-hours because required account, positions, orders, asset, quote, and spread rows passed.
- Fresh Alpaca MCP checks: regular market closed at `2026-05-28T06:12:25.392962422-04:00`; account ACTIVE; positions fetched; open US equity orders empty; same-day after-hours validation fills reconciled by client order id for `ah-20260528-1311-intc-buy-01` and `ah-20260528-1351-nok-buy-01`.
- Gates: universe strict PASS; MCP strict PASS with SEC EDGAR/FRED/Firecrawl/Yahoo pass and Alpha Vantage `empty_response` gap. Separate after-hours order budget FAIL because `risk_inputs.after_hours_new_orders_submitted_today=2` and session cap is 2.
- Risk validation: `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-05-28-1911-after-hours-autopilot.json` PASS for the empty no-submit plan with `orders is empty` warning. `PATH=/usr/local/bin:$PATH python3 scripts/check-universe-coverage.py --strict --json ...` PASS. `PATH=/usr/local/bin:$PATH python3 scripts/check-mcp-coverage.py --strict --json ...` PASS.
- Submit/reconcile: no `place_stock_order` call, no submit attempt, no new reconciliation required.
- Artifacts: `wiki/evidence-store/run-manifests/2026-05-28-1911-after-hours-autopilot.json`, `wiki/trade-ledger/orders/2026-05-28-1911-after-hours-autopilot.json`, [[2026-05-28-1911-after-hours-autopilot]].

## [2026-05-28 19:34 Asia/Seoul] after-hours-autopilot | 2026-05-28-1931-after-hours-autopilot scheduled after-hours paper autopilot

- Workflow: `harness/workflows/after-hours-autopilot.md`. Paper mode `ALPACA_PAPER_TRADE=true`; session=`after_hours`; artifact tag=`after-hours`; review bucket=`after_hours_validation`.
- Scheduler preflight: `wiki/evidence-store/sources/2026-05-28-1931-after-hours-autopilot-alpaca-core-preflight.json` and `wiki/evidence-store/sources/2026-05-28-1931-after-hours-autopilot-research-mcp-preflight.json` used. Alpaca core `first_blocking_gate=market_closed` was treated as expected non-blocking for after-hours because required account, positions, orders, asset, quote, and spread rows passed.
- Fresh Alpaca MCP checks: regular market closed at `2026-05-28T06:32:58.389151151-04:00`; account ACTIVE; positions fetched; open US equity orders empty; same-day after-hours validation fills reconciled by client order id for `ah-20260528-1311-intc-buy-01` and `ah-20260528-1351-nok-buy-01`.
- Gates: universe strict PASS; MCP strict PASS with SEC EDGAR/FRED/Firecrawl/Yahoo pass and Alpha Vantage `empty_response` gap. Separate after-hours order budget FAIL because `risk_inputs.after_hours_new_orders_submitted_today=2` and session cap is 2.
- Risk validation: `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-05-28-1931-after-hours-autopilot.json` PASS for the empty no-submit plan with `orders is empty` warning. `PATH=/usr/local/bin:$PATH python3 scripts/check-universe-coverage.py --strict --json ...` PASS. `PATH=/usr/local/bin:$PATH python3 scripts/check-mcp-coverage.py --strict --json ...` PASS.
- Submit/reconcile: no `place_stock_order` call, no submit attempt, no new reconciliation required.
- Artifacts: `wiki/evidence-store/run-manifests/2026-05-28-1931-after-hours-autopilot.json`, `wiki/trade-ledger/orders/2026-05-28-1931-after-hours-autopilot.json`, [[2026-05-28-1931-after-hours-autopilot]].

## [2026-05-28 19:53 Asia/Seoul] after-hours-autopilot | 2026-05-28-1951-after-hours-autopilot scheduled after-hours paper autopilot

- Workflow: `harness/workflows/after-hours-autopilot.md`. Paper mode `ALPACA_PAPER_TRADE=true`; session=`after_hours`; artifact tag=`after-hours`; review bucket=`after_hours_validation`.
- Scheduler preflight: `wiki/evidence-store/sources/2026-05-28-1951-after-hours-autopilot-alpaca-core-preflight.json` and `wiki/evidence-store/sources/2026-05-28-1951-after-hours-autopilot-research-mcp-preflight.json` used. Alpaca core `first_blocking_gate=market_closed` was treated as expected non-blocking for after-hours because required account, positions, orders, asset, quote, and spread rows passed.
- Fresh Alpaca MCP checks: regular market closed at `2026-05-28T06:52:20.252922426-04:00`; account ACTIVE; positions fetched; open US equity orders empty; same-day after-hours validation fills reconciled by client order id for `ah-20260528-1311-intc-buy-01` and `ah-20260528-1351-nok-buy-01`.
- Gates: universe strict PASS; MCP strict PASS with SEC EDGAR/FRED/Firecrawl/Yahoo pass and Alpha Vantage `empty_response` gap. Separate after-hours order budget FAIL because `risk_inputs.after_hours_new_orders_submitted_today=2` and session cap is 2.
- Risk validation: `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-05-28-1951-after-hours-autopilot.json` PASS for the empty no-submit plan with `orders is empty` warning. `PATH=/usr/local/bin:$PATH python3 scripts/check-universe-coverage.py --strict --json ...` PASS. `PATH=/usr/local/bin:$PATH python3 scripts/check-mcp-coverage.py --strict --json ...` PASS.
- Submit/reconcile: no `place_stock_order` call, no submit attempt, no new reconciliation required.
- Artifacts: `wiki/evidence-store/run-manifests/2026-05-28-1951-after-hours-autopilot.json`, `wiki/trade-ledger/orders/2026-05-28-1951-after-hours-autopilot.json`, [[2026-05-28-1951-after-hours-autopilot]].

## [2026-05-28 20:13 Asia/Seoul] after-hours-autopilot | 2026-05-28-2011-after-hours-autopilot scheduled after-hours paper autopilot

- Workflow: `harness/workflows/after-hours-autopilot.md`. Paper mode `ALPACA_PAPER_TRADE=true`; session=`after_hours`; artifact tag=`after-hours`; review bucket=`after_hours_validation`.
- Scheduler preflight: `wiki/evidence-store/sources/2026-05-28-2011-after-hours-autopilot-alpaca-core-preflight.json` and `wiki/evidence-store/sources/2026-05-28-2011-after-hours-autopilot-research-mcp-preflight.json` used. Alpaca core `first_blocking_gate=market_closed` was treated as expected non-blocking for after-hours because required account, positions, orders, asset, quote, and spread rows passed.
- Fresh Alpaca MCP checks: regular market closed at `2026-05-28T07:12:44.45909527-04:00`; account ACTIVE; positions fetched; open US equity orders empty; same-day after-hours validation fills reconciled by client order id for `ah-20260528-1311-intc-buy-01` and `ah-20260528-1351-nok-buy-01`.
- Gates: universe strict PASS; MCP strict PASS with SEC EDGAR/FRED/Firecrawl/Yahoo pass and Alpha Vantage `empty_response` gap. Separate after-hours order budget FAIL because `risk_inputs.after_hours_new_orders_submitted_today=2` and session cap is 2.
- Risk validation: `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-05-28-2011-after-hours-autopilot.json` PASS for the empty no-submit plan with `orders is empty` warning. `PATH=/usr/local/bin:$PATH python3 scripts/check-universe-coverage.py --strict --json ...` PASS. `PATH=/usr/local/bin:$PATH python3 scripts/check-mcp-coverage.py --strict --json ...` PASS.
- Submit/reconcile: no `place_stock_order` call, no submit attempt, no new reconciliation required.
- Artifacts: `wiki/evidence-store/run-manifests/2026-05-28-2011-after-hours-autopilot.json`, `wiki/trade-ledger/orders/2026-05-28-2011-after-hours-autopilot.json`, [[2026-05-28-2011-after-hours-autopilot]].

## [2026-05-28 20:33 Asia/Seoul] after-hours-autopilot | 2026-05-28-2031-after-hours-autopilot scheduled after-hours paper autopilot

- Workflow: `harness/workflows/after-hours-autopilot.md`. Paper mode `ALPACA_PAPER_TRADE=true`; session=`after_hours`; artifact tag=`after-hours`; review bucket=`after_hours_validation`.
- Scheduler preflight: `wiki/evidence-store/sources/2026-05-28-2031-after-hours-autopilot-alpaca-core-preflight.json` and `wiki/evidence-store/sources/2026-05-28-2031-after-hours-autopilot-research-mcp-preflight.json` used. Alpaca core `first_blocking_gate=market_closed` was treated as expected non-blocking for after-hours because required account, positions, orders, activity, asset, quote, and spread rows passed.
- Fresh Alpaca MCP checks: regular market closed at `2026-05-28T07:32:52.611040483-04:00`; account ACTIVE; positions fetched; open US equity orders empty; same-day after-hours validation fills reconciled by client order id for `ah-20260528-1311-intc-buy-01` and `ah-20260528-1351-nok-buy-01`.
- Gates: universe strict PASS; MCP strict PASS with SEC EDGAR/FRED/Firecrawl/Yahoo pass and Alpha Vantage `empty_response` gap. Separate after-hours order budget FAIL because `risk_inputs.after_hours_new_orders_submitted_today=2` and session cap is 2.
- Risk validation: `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-05-28-2031-after-hours-autopilot.json` PASS for the empty no-submit plan with `orders is empty` warning. `PATH=/usr/local/bin:$PATH python3 scripts/check-universe-coverage.py --strict --json ...` PASS. `PATH=/usr/local/bin:$PATH python3 scripts/check-mcp-coverage.py --strict --json ...` PASS.
- Submit/reconcile: no `place_stock_order` call, no submit attempt, no new reconciliation required.
- Artifacts: `wiki/evidence-store/run-manifests/2026-05-28-2031-after-hours-autopilot.json`, `wiki/trade-ledger/orders/2026-05-28-2031-after-hours-autopilot.json`, [[2026-05-28-2031-after-hours-autopilot]].

## [2026-05-28 20:55 Asia/Seoul] after-hours-autopilot | 2026-05-28-2051-after-hours-autopilot scheduled after-hours paper autopilot

- Workflow: `harness/workflows/after-hours-autopilot.md`. Paper mode `ALPACA_PAPER_TRADE=true`; session=`after_hours`; artifact tag=`after-hours`; review bucket=`after_hours_validation`.
- Scheduler preflight: `wiki/evidence-store/sources/2026-05-28-2051-after-hours-autopilot-alpaca-core-preflight.json` and `wiki/evidence-store/sources/2026-05-28-2051-after-hours-autopilot-research-mcp-preflight.json` used. Alpaca core `first_blocking_gate=market_closed` was treated as expected non-blocking for after-hours because required account, positions, orders, asset, quote, and spread rows passed.
- Fresh Alpaca MCP checks: regular market closed at `2026-05-28T07:53:15.519092505-04:00`; positions fetched. Fresh account and open-order calls were cancelled/blocked by the runtime safety monitor, so the scheduler-owned passing account and open-order rows were used. Same-day after-hours validation fills remained `ah-20260528-1311-intc-buy-01` and `ah-20260528-1351-nok-buy-01`.
- Gates: universe strict PASS; MCP strict PASS with SEC EDGAR/FRED/Firecrawl/Yahoo pass and Alpha Vantage `empty_response` gap. Separate after-hours order budget FAIL because `risk_inputs.after_hours_new_orders_submitted_today=2` and session cap is 2.
- Risk validation: `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-05-28-2051-after-hours-autopilot.json` PASS for the empty no-submit plan with `orders is empty` warning. `PATH=/usr/local/bin:$PATH python3 scripts/check-universe-coverage.py --strict --json ...` PASS. `PATH=/usr/local/bin:$PATH python3 scripts/check-mcp-coverage.py --strict --json ...` PASS.
- Submit/reconcile: no `place_stock_order` call, no submit attempt, no new reconciliation required.
- Artifacts: `wiki/evidence-store/run-manifests/2026-05-28-2051-after-hours-autopilot.json`, `wiki/trade-ledger/orders/2026-05-28-2051-after-hours-autopilot.json`, [[2026-05-28-2051-after-hours-autopilot]].

## [2026-05-28 21:14 Asia/Seoul] after-hours-autopilot | 2026-05-28-2111-after-hours-autopilot scheduled after-hours paper autopilot

- Workflow: `harness/workflows/after-hours-autopilot.md`. Paper mode `ALPACA_PAPER_TRADE=true`; session=`after_hours`; artifact tag=`after-hours`; review bucket=`after_hours_validation`.
- Scheduler preflight: `wiki/evidence-store/sources/2026-05-28-2111-after-hours-autopilot-alpaca-core-preflight.json` and `wiki/evidence-store/sources/2026-05-28-2111-after-hours-autopilot-research-mcp-preflight.json` used. Alpaca core `first_blocking_gate=market_closed` was treated as expected non-blocking for after-hours because required account, positions, orders, asset, quote, and spread rows passed.
- Fresh Alpaca MCP checks: regular market closed at `2026-05-28T08:13:19.470071745-04:00`; account ACTIVE; positions fetched. Fresh open-order call was cancelled by the runtime safety monitor, so the scheduler-owned passing open-order row was used. Same-day after-hours validation fills remained `ah-20260528-1311-intc-buy-01` and `ah-20260528-1351-nok-buy-01`.
- Gates: universe strict PASS; MCP strict PASS with SEC EDGAR/FRED/Firecrawl/Yahoo pass and Alpha Vantage `empty_response` gap. Separate after-hours order budget FAIL because `risk_inputs.after_hours_new_orders_submitted_today=2` and session cap is 2.
- Risk validation: `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-05-28-2111-after-hours-autopilot.json` PASS for the empty no-submit plan with `orders is empty` warning. `PATH=/usr/local/bin:$PATH python3 scripts/check-universe-coverage.py --strict --json ...` PASS. `PATH=/usr/local/bin:$PATH python3 scripts/check-mcp-coverage.py --strict --json ...` PASS.
- Submit/reconcile: no `place_stock_order` call, no submit attempt, no new reconciliation required.
- Artifacts: `wiki/evidence-store/run-manifests/2026-05-28-2111-after-hours-autopilot.json`, `wiki/trade-ledger/orders/2026-05-28-2111-after-hours-autopilot.json`, [[2026-05-28-2111-after-hours-autopilot]].

## [2026-05-28 21:34 Asia/Seoul] after-hours-autopilot | 2026-05-28-2131-after-hours-autopilot scheduled after-hours paper autopilot

- Workflow: `harness/workflows/after-hours-autopilot.md`. Paper mode `ALPACA_PAPER_TRADE=true`; session=`after_hours`; artifact tag=`after-hours`; review bucket=`after_hours_validation`.
- Scheduler preflight: `wiki/evidence-store/sources/2026-05-28-2131-after-hours-autopilot-alpaca-core-preflight.json` and `wiki/evidence-store/sources/2026-05-28-2131-after-hours-autopilot-research-mcp-preflight.json` used. Alpaca core `first_blocking_gate=market_closed` was treated as expected non-blocking for after-hours because required account, positions, orders, asset, quote, and spread rows passed.
- Fresh Alpaca MCP checks: regular market closed at `2026-05-28T08:33:05.88208016-04:00`; account ACTIVE; positions fetched; open US equity orders empty; same-day after-hours validation fills reconciled by client order id for `ah-20260528-1311-intc-buy-01` and `ah-20260528-1351-nok-buy-01`.
- Gates: universe strict PASS; MCP strict PASS with SEC EDGAR/FRED/Firecrawl/Yahoo pass and Alpha Vantage `empty_response` gap. Separate after-hours order budget FAIL because `risk_inputs.after_hours_new_orders_submitted_today=2` and session cap is 2.
- Risk validation: `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-05-28-2131-after-hours-autopilot.json` PASS for the empty no-submit plan with `orders is empty` warning. `PATH=/usr/local/bin:$PATH python3 scripts/check-universe-coverage.py --strict --json ...` PASS. `PATH=/usr/local/bin:$PATH python3 scripts/check-mcp-coverage.py --strict --json ...` PASS.
- Submit/reconcile: no `place_stock_order` call, no submit attempt, no new reconciliation required.
- Artifacts: `wiki/evidence-store/run-manifests/2026-05-28-2131-after-hours-autopilot.json`, `wiki/trade-ledger/orders/2026-05-28-2131-after-hours-autopilot.json`, [[2026-05-28-2131-after-hours-autopilot]].

## [2026-05-28 21:53 Asia/Seoul] after-hours-autopilot | 2026-05-28-2151-after-hours-autopilot scheduled after-hours paper autopilot

- Workflow: `harness/workflows/after-hours-autopilot.md`. Paper mode `ALPACA_PAPER_TRADE=true`; session=`after_hours`; artifact tag=`after-hours`; review bucket=`after_hours_validation`.
- Scheduler preflight: `wiki/evidence-store/sources/2026-05-28-2151-after-hours-autopilot-alpaca-core-preflight.json` and `wiki/evidence-store/sources/2026-05-28-2151-after-hours-autopilot-research-mcp-preflight.json` used. Alpaca core `first_blocking_gate=market_closed` was treated as expected non-blocking for after-hours because required account, positions, orders, asset, quote, and spread rows passed.
- Fresh Alpaca MCP checks: positions fetched; open US equity orders empty; latest quote/snapshot fetched for the research shortlist; same-day after-hours validation fills reconciled by client order id for `ah-20260528-1311-intc-buy-01` and `ah-20260528-1351-nok-buy-01`. Fresh clock/account calls were cancelled by the runtime, so scheduler-owned passing rows were used.
- Gates: universe strict PASS; MCP strict PASS with SEC EDGAR/FRED/Firecrawl/Yahoo pass and Alpha Vantage `empty_response` gap. Separate after-hours order budget FAIL because `risk_inputs.after_hours_new_orders_submitted_today=2` and session cap is 2.
- Risk validation: `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-05-28-2151-after-hours-autopilot.json` PASS for the empty no-submit plan with `orders is empty` warning. `PATH=/usr/local/bin:$PATH python3 scripts/check-universe-coverage.py --strict --json ...` PASS. `PATH=/usr/local/bin:$PATH python3 scripts/check-mcp-coverage.py --strict --json ...` PASS.
- Submit/reconcile: no `place_stock_order` call, no submit attempt, no new reconciliation required.
- Artifacts: `wiki/evidence-store/run-manifests/2026-05-28-2151-after-hours-autopilot.json`, `wiki/trade-ledger/orders/2026-05-28-2151-after-hours-autopilot.json`, [[2026-05-28-2151-after-hours-autopilot]].

## [2026-05-28 22:42 Asia/Seoul] hourly-autopilot | 2026-05-28-2231-hourly-autopilot scheduled paper autopilot

- Workflow: `harness/workflows/hourly-autopilot.md`. Paper mode `ALPACA_PAPER_TRADE=true`; regular-session scheduled cadence authorized; Alpaca MCP only for account/market/order operations.
- Scheduler preflight: stale cleanup `pass`, Alpaca core hard gate PASS at `2026-05-28T09:31:17.465151556-04:00`, research MCP preflight used for symbols AAPL/BAC/NOK/HOOD/NEE/QQQ/META/PLTR/PFE/RGTI/NKE/WMT. Alpha Vantage had `empty_response`; SEC EDGAR/FRED/Firecrawl/Yahoo passed.
- Gates: universe strict PASS, MCP strict PASS, risk validator PASS, quote freshness PASS, spread PASS, open-order lifecycle PASS. Pre-submit order plan: `wiki/trade-ledger/orders/2026-05-28-2231-hourly-autopilot.json`.
- Submit: PLTR 1주 buy limit 135.41 filled at 134.94; QQQ first submit call `cancelled`, same client_order_id reconciliation returned not found, same-id retry filled 1주 at 728.36; BAC 1주 buy limit 50.89 submitted and remains open/new.
- Post-trade reconciliation: client-order-id lookup PASS, open orders PASS with BAC open, fill activities PASS for PLTR/QQQ. Fresh account and full positions refresh were `cancelled` by runtime monitor and recorded as `gap_category=cancelled`.
- Artifacts: `wiki/evidence-store/run-manifests/2026-05-28-2231-hourly-autopilot.json`, `wiki/trade-ledger/orders/2026-05-28-2231-hourly-autopilot.json`, `wiki/trade-ledger/positions/2026-05-28-2231-hourly-autopilot-post-trade.json`, [[2026-05-28-2231-hourly-autopilot]]. Review due: PLTR/QQQ `회고 대기`; BAC open-order lifecycle follow-up required.

## [2026-05-28 23:01 Asia/Seoul] hourly-autopilot | 2026-05-28-2251-hourly-autopilot scheduled paper autopilot

- Workflow: `harness/workflows/hourly-autopilot.md`. Paper mode `ALPACA_PAPER_TRADE=true`; regular-session scheduled cadence authorized; Alpaca MCP only for account/market/order operations.
- Scheduler preflight: stale cleanup `pass` with prior BAC open order fresh/not stale; Alpaca core hard gate PASS at `2026-05-28T09:51:16.272050313-04:00`; research MCP preflight used for symbols SPY/AAPL/NVDA/BAC/NEE/AMZN/TSLA/PFE/SO/CVX/NKE/FCX. Alpha Vantage had `empty_response`; SEC EDGAR/FRED/Firecrawl/Yahoo passed.
- Gates: universe strict PASS, MCP strict PASS, risk validator PASS, quote freshness PASS, spread PASS, open-order lifecycle PASS. Pre-submit order plan: `wiki/trade-ledger/orders/2026-05-28-2251-hourly-autopilot.json`.
- Submit: CVX 1주 buy limit 184.35 filled at 184.03; NEE 1주 buy limit 88.00 submitted and remains open/new; NKE 1주 buy limit 46.03 filled at 46.03.
- Post-trade reconciliation: client-order/fill/open-order checks completed; open orders are NEE and prior BAC. Fresh account and full positions refresh were `cancelled` by runtime monitor and recorded as `gap_category=cancelled`.
- Artifacts: `wiki/evidence-store/run-manifests/2026-05-28-2251-hourly-autopilot.json`, `wiki/trade-ledger/orders/2026-05-28-2251-hourly-autopilot.json`, `wiki/trade-ledger/positions/2026-05-28-2251-hourly-autopilot-post-trade.json`, [[2026-05-28-2251-hourly-autopilot]]. Review due: CVX/NKE `회고 대기`; NEE/BAC open-order lifecycle follow-up required.

## [2026-05-28 23:22 Asia/Seoul] hourly-autopilot | 2026-05-28-2311-hourly-autopilot scheduled paper autopilot

- Workflow: `harness/workflows/hourly-autopilot.md`. Paper mode `ALPACA_PAPER_TRADE=true`; regular-session scheduled cadence authorized; Alpaca MCP only for account/market/order operations.
- Scheduler preflight: stale cleanup `pass`; BAC stale open order appeared in cleanup's immediate remaining list but registered Alpaca MCP open-order reconciliation showed BAC no longer open. Alpaca core hard gate PASS at `2026-05-28T10:11:17.124578802-04:00`; research MCP preflight used for symbols SPY/QQQ/NVDA/AAPL/BAC/NKE/NEE/WMT/PLTR/PFE/INTC/FCX. Alpha Vantage had `empty_response`; SEC EDGAR/FRED/Firecrawl/Yahoo passed.
- Gates: universe strict PASS, MCP strict PASS, risk validator PASS, quote freshness PASS, spread PASS, open-order lifecycle PASS. Pre-submit order plan: `wiki/trade-ledger/orders/2026-05-28-2311-hourly-autopilot.json`.
- Submit: WMT first submit call `cancelled`, same client_order_id reconciliation returned not found, same-id retry accepted and remains open/new. PFE first submit call `cancelled`, same client_order_id reconciliation returned not found, same-id retry filled 1주 at 26.16.
- Post-trade reconciliation: client-order-id, open-order, account, and positions checks completed. Open orders are WMT and prior NEE. Fresh fill activity refresh was `cancelled` by runtime monitor and recorded as `gap_category=cancelled`.
- Artifacts: `wiki/evidence-store/run-manifests/2026-05-28-2311-hourly-autopilot.json`, `wiki/trade-ledger/orders/2026-05-28-2311-hourly-autopilot.json`, `wiki/trade-ledger/positions/2026-05-28-2311-hourly-autopilot-post-trade.json`, [[2026-05-28-2311-hourly-autopilot]]. Review due: PFE `회고 대기`; WMT/NEE open-order lifecycle follow-up required.

## [2026-05-28 23:43 Asia/Seoul] hourly-autopilot | 2026-05-28-2331-hourly-autopilot scheduled paper autopilot

- Workflow: `harness/workflows/hourly-autopilot.md`. Paper mode `ALPACA_PAPER_TRADE=true`; regular-session scheduled cadence authorized; Alpaca MCP only for account/market/order operations.
- Scheduler preflight: stale cleanup `2026-05-28-2331-hourly-autopilot-stale-order-cleanup.json` attempted stale NEE cancellation. Immediate cleanup output still listed NEE open, but registered Alpaca MCP `get_orders(status=open, asset_class=us_equity)` returned no open US equity orders, so `risk_open_order_lifecycle` passed. Alpaca core hard gate PASS; research MCP preflight used for QQQ/SPY/BAC/NKE/GOOGL/NEE/INTC/PFE/HOOD/AAPL/SO/PLTR with SEC EDGAR/FRED/Firecrawl/Yahoo pass and Alpha Vantage `empty_response`.
- Gates: universe strict PASS, MCP strict PASS, risk validator PASS, quote freshness PASS, spread PASS. Pre-submit order plan: `wiki/trade-ledger/orders/2026-05-28-2331-hourly-autopilot.json`.
- Submit: GOOGL 1주 buy limit 389.00 accepted and remains open/new. SO first submit `cancelled`; same client id reconciliation returned 404, same-id retry filled 1주 at 93.38. HOOD first submit `cancelled`; same client id reconciliation returned 404 and same-id retry was cancelled by the runtime safety monitor, so no HOOD order exists.
- Post-trade reconciliation: GOOGL/SO client-order checks completed, open orders show GOOGL only, FILL activities show SO fill, positions refresh passed. Fresh account refresh was `cancelled` twice by runtime monitor and recorded as `gap_category=cancelled`.
- Artifacts: `wiki/evidence-store/run-manifests/2026-05-28-2331-hourly-autopilot.json`, `wiki/trade-ledger/orders/2026-05-28-2331-hourly-autopilot.json`, `wiki/trade-ledger/positions/2026-05-28-2331-hourly-autopilot-post-trade.json`, [[2026-05-28-2331-hourly-autopilot]]. Review due: SO `회고 대기`; GOOGL open-order lifecycle follow-up required.

## [2026-05-29 00:01 Asia/Seoul] hourly-autopilot | 2026-05-28-2351-hourly-autopilot scheduled paper autopilot

- Workflow: `harness/workflows/hourly-autopilot.md`. Paper mode `ALPACA_PAPER_TRADE=true`; regular-session scheduled cadence authorized; Alpaca MCP only for account/market/order operations.
- Scheduler preflight: stale cleanup `pass` with no remaining open orders; Alpaca core hard gate PASS at `2026-05-28T10:51:19.851725879-04:00`; research MCP preflight used for AAPL/NVDA/GOOGL/WMT/AMZN/BAC/SPY/INTC/SO/QQQ/SLB/PFE with SEC EDGAR/FRED/Firecrawl/Yahoo pass and Alpha Vantage `empty_response`.
- Gates: universe strict PASS, MCP strict PASS, risk validator PASS, quote freshness PASS, spread PASS, open-order lifecycle PASS. Pre-submit order plan: `wiki/trade-ledger/orders/2026-05-28-2351-hourly-autopilot.json`.
- Submit: SPY first submit `cancelled`, same client id retry `timeout`, and reconciliation returned 404/not found so no SPY order exists. AAPL first submit `cancelled`, same client id reconciliation 404, same-id retry accepted and remains open/new. SLB 1주 buy limit 55.67 accepted and filled at 55.48.
- Post-trade reconciliation: SPY/AAPL/SLB client-order checks completed, open orders PASS with AAPL open, positions PASS with SLB included. Fresh account and fill activity refresh were `cancelled` by runtime monitor and recorded as `gap_category=cancelled`.
- Artifacts: `wiki/evidence-store/run-manifests/2026-05-28-2351-hourly-autopilot.json`, `wiki/trade-ledger/orders/2026-05-28-2351-hourly-autopilot.json`, `wiki/trade-ledger/positions/2026-05-28-2351-hourly-autopilot-post-trade.json`, [[2026-05-28-2351-hourly-autopilot]]. Review due: SLB `회고 대기`; AAPL open-order lifecycle follow-up required.

## [2026-05-29 00:21 Asia/Seoul] hourly-autopilot | 2026-05-29-0011-hourly-autopilot scheduled paper autopilot

- Workflow: `harness/workflows/hourly-autopilot.md`. Paper mode `ALPACA_PAPER_TRADE=true`; regular-session scheduled cadence authorized; Alpaca MCP only for account/market/order operations.
- Scheduler preflight: stale cleanup `pass` with fresh AAPL open order not stale; Alpaca core hard gate PASS at `2026-05-28T11:11:17.646180689-04:00`; research MCP preflight used for SPY/AAPL/NVDA/WMT/QQQ/SLB/AMZN/BAC/NKE/NEE/GOOGL/IONQ with SEC EDGAR/FRED/Firecrawl/Yahoo pass and Alpha Vantage `empty_response`.
- Gates: universe strict PASS, MCP strict PASS, risk validator PASS, quote freshness PASS, spread PASS, open-order lifecycle PASS. AAPL and same mega-cap tech cluster were avoided because prior AAPL order remained open/new. Pre-submit order plan: `wiki/trade-ledger/orders/2026-05-29-0011-hourly-autopilot.json`.
- Submit: SPY 1주 buy limit 753.38 filled at 753.38; BAC 1주 buy limit 51.17 filled at 51.14; NEE 1주 buy limit 87.83 accepted and remains open/new.
- Post-trade reconciliation: client-order-id checks completed for SPY/BAC/NEE, open orders PASS with NEE and prior AAPL, FILL activities show SPY/BAC fills, positions refresh PASS, account refresh PASS.
- Artifacts: `wiki/evidence-store/run-manifests/2026-05-29-0011-hourly-autopilot.json`, `wiki/trade-ledger/orders/2026-05-29-0011-hourly-autopilot.json`, `wiki/trade-ledger/positions/2026-05-29-0011-hourly-autopilot-post-trade.json`, [[2026-05-29-0011-hourly-autopilot]]. Review due: SPY/BAC `회고 대기`; NEE/AAPL open-order lifecycle follow-up required.

## [2026-05-29 00:27 Asia/Seoul] incident-retrospective | regular autopilot false failure notification

- Incident: `2026-05-29-0011-hourly-autopilot` completed order submission, reconciliation, and validators successfully, but the wrapper emitted `[regular autopilot] 실패` because the final dashboard build crashed.
- Root cause: `scripts/build-agent-dashboard.py` and the notification formatter assumed `risk_check_result` was always a mapping with `status`. Recent hourly manifests can store `risk_check_result` as the string `"pass"`, so post-run dashboard/notification code raised `AttributeError` after the trading workflow had already succeeded.
- Why verification missed it: validation covered runner syntax, selected unit tests, and direct dashboard generation after one artifact state, but did not include a regression test for the exact manifest schema variant produced by the latest successful regular-session run, nor an end-to-end post-run completion path check covering dashboard build plus completion notification formatting.
- Fix: normalize `risk_check_result` in dashboard and messenger notification code so both dict and string schema variants are accepted; reran dashboard build successfully; resent the corrected completion notification for `2026-05-29-0011-hourly-autopilot`; autopushed the recovered artifacts in commit `f5e3363`.
- Recurrence prevention: added `tests/test_autopilot_notification_schema.py` to lock the string-risk-result case for both dashboard normalization and completion notification rendering. Future scheduled-run changes must validate post-run artifact consumers, not only trading gates, before being marked complete.

## [2026-05-29 00:40 Asia/Seoul] hourly-autopilot | 2026-05-29-0031-hourly-autopilot scheduled paper autopilot

- Workflow: `harness/workflows/hourly-autopilot.md`. Paper mode `ALPACA_PAPER_TRADE=true`; regular-session scheduled cadence authorized; Alpaca MCP only for account/market/order operations.
- Scheduler preflight: stale cleanup `2026-05-29-0031-hourly-autopilot-stale-order-cleanup.json` cancelled stale AAPL order attempt; registered Alpaca MCP open-order reconciliation returned no open orders before risk validation. Alpaca core hard gate PASS at `2026-05-28T11:31:17.193870329-04:00`; research MCP preflight used for SPY/QQQ/AAPL/NVDA/GOOGL/WMT/SLB/BAC/NKE/TSLA/COP/SO with SEC EDGAR/FRED/Firecrawl/Yahoo pass and Alpha Vantage `empty_response`.
- Gates: universe strict PASS, MCP strict PASS, risk validator PASS, quote freshness PASS, spread PASS, open-order lifecycle PASS. Pre-submit order plan: `wiki/trade-ledger/orders/2026-05-29-0031-hourly-autopilot.json`.
- Submit: NVDA 1주 buy limit 212.87 filled at 212.55; COP 1주 buy limit 114.98 filled at 114.95; TSLA 1주 buy limit 441.45 accepted and remains open/new.
- Post-trade reconciliation: client-order-id, open-order, account, positions, and fill activity checks completed. Open order is TSLA only.
- Artifacts: `wiki/evidence-store/run-manifests/2026-05-29-0031-hourly-autopilot.json`, `wiki/trade-ledger/orders/2026-05-29-0031-hourly-autopilot.json`, `wiki/trade-ledger/positions/2026-05-29-0031-hourly-autopilot-post-trade.json`, [[2026-05-29-0031-hourly-autopilot]]. Review due: NVDA/COP `회고 대기`; TSLA open-order lifecycle follow-up required.

## [2026-05-29 00:59 Asia/Seoul] hourly-autopilot | 2026-05-29-0051-hourly-autopilot scheduled paper autopilot

- Workflow: `harness/workflows/hourly-autopilot.md`. Paper mode `ALPACA_PAPER_TRADE=true`; regular-session scheduled cadence authorized; Alpaca MCP only for account/market/order operations.
- Scheduler preflight: stale cleanup `wiki/evidence-store/sources/2026-05-29-0051-hourly-autopilot-stale-order-cleanup.json` status `pass` with no remaining open orders; Alpaca core hard gate PASS at `2026-05-28T11:51:17.944282587-04:00`; research MCP preflight used for QQQ/WMT/NVDA/SPY/AMZN/AAPL/GOOGL/SLB/BAC/NKE/PLTR/INTC with SEC EDGAR/FRED/Firecrawl/Yahoo pass and Alpha Vantage `empty_response`.
- Fresh registered Alpaca MCP checks: positions PASS, open US equity orders empty, AMZN/INTC quote refresh PASS. account refresh and FILL activity refresh were `cancelled` by runtime safety monitor and recorded as non-blocking gaps because scheduler-owned core preflight and client-order reconciliation covered the hard gate.
- Gates: universe strict PASS, MCP strict PASS, risk validator PASS, quote freshness PASS, spread PASS, open-order lifecycle PASS. Daily order cap before run was 18; plan contained two 1-share buys to cap at 20, but only AMZN was actually submitted/filled.
- Submit: AMZN first submit `cancelled`, same client id reconciliation returned 404/not found, same-id retry filled 1주 at 270.55. INTC first submit `cancelled`, same client id reconciliation returned 404/not found, same-id retry also `cancelled`; no INTC order exists and no further retry was made.
- Post-trade reconciliation: AMZN client-order PASS filled, INTC client-order 404/not found, open orders PASS empty, positions PASS with AMZN qty=2. Account and FILL activity refresh gaps classified `cancelled`.
- Artifacts: `wiki/evidence-store/run-manifests/2026-05-29-0051-hourly-autopilot.json`, `wiki/trade-ledger/orders/2026-05-29-0051-hourly-autopilot.json`, `wiki/trade-ledger/positions/2026-05-29-0051-hourly-autopilot-post-trade.json`, [[2026-05-29-0051-hourly-autopilot]]. Review due: AMZN `회고 대기`.

## [2026-05-29 01:18 Asia/Seoul] hourly-autopilot | 2026-05-29-0111-hourly-autopilot scheduled paper autopilot

- Workflow: `harness/workflows/hourly-autopilot.md`. Paper mode `ALPACA_PAPER_TRADE=true`; regular-session scheduled cadence authorized; Alpaca MCP only for account/market/order operations.
- Scheduler preflight: stale cleanup `wiki/evidence-store/sources/2026-05-29-0111-hourly-autopilot-stale-order-cleanup.json` status `pass` with no stale candidates and no remaining open orders. Alpaca core hard gate PASS at `2026-05-28T12:11:18.162315601-04:00`; research MCP preflight used for SPY/QQQ/AAPL/AMZN/COP/BAC/PLTR/INTC/XOM/NEE/SLB/CVX with SEC EDGAR/FRED/Firecrawl/Yahoo pass and Alpha Vantage `empty_response`.
- Fresh registered Alpaca MCP checks before submit: market clock open at `2026-05-28T12:15:00.685556747-04:00`, open US equity orders empty, XOM asset active/tradable, XOM quote bid 148.26 ask 148.37 with spread 0.0742%.
- Gates: universe strict PASS, MCP strict PASS, risk validator PASS, quote freshness PASS, spread PASS, open-order lifecycle PASS. Daily order count before run was 19, so only one 1-share validation buy was planned.
- Submit: XOM 1주 buy limit 148.37 submitted through Alpaca MCP with `client_order_id=hourly-20260529-0111-xom-buy-01`; client-order-id reconciliation confirmed filled at 148.37.
- Post-trade reconciliation: client-order-id PASS, open orders PASS empty, positions PASS with XOM qty=2, FILL activity PASS. Account refresh was `cancelled` by runtime monitor and recorded as a non-blocking gap using scheduler account preflight as fallback.
- Validators: `PATH=/usr/local/bin:$PATH python3 scripts/check-universe-coverage.py --strict --json ...` PASS; `check-mcp-coverage.py --strict --json ...` PASS; `check-risk-policy.py --json ...` PASS.
- Artifacts: `wiki/evidence-store/run-manifests/2026-05-29-0111-hourly-autopilot.json`, `wiki/trade-ledger/orders/2026-05-29-0111-hourly-autopilot.json`, `wiki/trade-ledger/positions/2026-05-29-0111-hourly-autopilot-post-trade.json`, [[2026-05-29-0111-hourly-autopilot]]. Review due: XOM `회고 대기`.

## [2026-05-29 01:33 Asia/Seoul] hourly-autopilot | 2026-05-29-0131-hourly-autopilot scheduled paper autopilot

- Workflow: `harness/workflows/hourly-autopilot.md`. Paper mode `ALPACA_PAPER_TRADE=true`; regular-session scheduled cadence authorized; Alpaca MCP only for account/market/order operations.
- Scheduler preflight: stale cleanup `wiki/evidence-store/sources/2026-05-29-0131-hourly-autopilot-stale-order-cleanup.json` status `pass` with remaining open orders empty. Alpaca core hard gate PASS at `2026-05-28T12:31:17.475666018-04:00`; research MCP preflight used for NVDA/QQQ/AAPL/NEE/SPY/INTC/WMT/SLB/BAC/XOM/NKE/PLTR with SEC EDGAR/FRED/Firecrawl/Yahoo pass and Alpha Vantage `empty_response`.
- Gates: universe strict PASS, MCP strict PASS, quote freshness PASS, spread evidence present, open-order lifecycle PASS, risk validator PASS for an empty order plan. First blocking gate for new orders was `risk_daily_new_orders_budget` because same ET-session new order count was already 20/20 after the prior XOM fill.
- Submit/reconcile: no `place_stock_order` call and no submit attempt. Scheduler Alpaca core preflight account/positions/open orders/recent activities rows were used as read-only reconciliation evidence; open orders were empty.
- Validators: `PATH=/usr/local/bin:$PATH python3 scripts/check-universe-coverage.py --strict --json ...` PASS; `check-mcp-coverage.py --strict --json ...` PASS; `check-risk-policy.py --json ...` PASS with `orders is empty` warning.
- Artifacts: `wiki/evidence-store/run-manifests/2026-05-29-0131-hourly-autopilot.json`, `wiki/trade-ledger/orders/2026-05-29-0131-hourly-autopilot.json`, [[2026-05-29-0131-hourly-autopilot]]. Review due: no new fills; existing validation fills remain `회고 대기`.

## [2026-05-29 01:53 Asia/Seoul] hourly-autopilot | 2026-05-29-0151-hourly-autopilot scheduled paper autopilot

- Workflow: `harness/workflows/hourly-autopilot.md`. Paper mode `ALPACA_PAPER_TRADE=true`; regular-session scheduled cadence authorized; Alpaca MCP only for account/market/order operations.
- Scheduler preflight: stale cleanup `wiki/evidence-store/sources/2026-05-29-0151-hourly-autopilot-stale-order-cleanup.json` status `pass` with no stale candidates and no remaining open orders. Alpaca core hard gate PASS at `2026-05-28T12:51:17.405273521-04:00`; research MCP preflight used for NVDA/INTC/MRK/QQQ/SLB/BAC/NKE/SO/NEE/TSLA/SPY/AMZN with SEC EDGAR/FRED/Firecrawl/Yahoo pass and Alpha Vantage `empty_response`.
- Gates: universe strict PASS, MCP strict PASS, quote freshness PASS, spread evidence present, open-order lifecycle PASS, risk validator PASS for an empty order plan. First blocking gate for new orders was `risk_daily_new_orders_budget` because same ET-session new order count was already 20/20.
- Submit/reconcile: no `place_stock_order` call and no submit attempt. Scheduler Alpaca core preflight account/positions/open orders/recent activities rows were used as read-only reconciliation evidence; open orders were empty.
- Validators: `PATH=/usr/local/bin:$PATH python3 scripts/check-universe-coverage.py --strict --json ...` PASS; `check-mcp-coverage.py --strict --json ...` PASS; `check-risk-policy.py --json ...` PASS with `orders is empty` warning.
- Artifacts: `wiki/evidence-store/run-manifests/2026-05-29-0151-hourly-autopilot.json`, `wiki/trade-ledger/orders/2026-05-29-0151-hourly-autopilot.json`, [[2026-05-29-0151-hourly-autopilot]]. Review due: no new fills; existing validation fills remain `회고 대기`.

## [2026-05-29 02:13 Asia/Seoul] hourly-autopilot | 2026-05-29-0211-hourly-autopilot scheduled paper autopilot

- Workflow: `harness/workflows/hourly-autopilot.md`. Paper mode `ALPACA_PAPER_TRADE=true`; regular-session scheduled cadence authorized; Alpaca MCP only for account/market/order operations.
- Scheduler preflight: stale cleanup `wiki/evidence-store/sources/2026-05-29-0211-hourly-autopilot-stale-order-cleanup.json` status `pass` with no stale candidates and no remaining open orders. Alpaca core hard gate PASS at `2026-05-28T13:11:19.099973182-04:00`; research MCP preflight used for SPY/QQQ/AAPL/AMZN/NEE/NVDA/INTC/COP/GOOGL/BAC/SO/XOM with SEC EDGAR/FRED/Firecrawl/Yahoo pass and Alpha Vantage `empty_response`.
- Gates: universe strict PASS, MCP strict PASS, quote freshness PASS, spread evidence present, open-order lifecycle PASS, risk validator PASS for an empty order plan. First blocking gate for new orders was `risk_daily_new_orders_budget` because same ET-session new order count was already 20/20.
- Submit/reconcile: no `place_stock_order` call and no submit attempt. Scheduler Alpaca core preflight account/positions/open orders/recent activities rows were used as read-only reconciliation evidence; open orders were empty.
- Validators: `PATH=/usr/local/bin:$PATH python3 scripts/check-universe-coverage.py --strict --json ...` PASS; `check-mcp-coverage.py --strict --json ...` PASS; `check-risk-policy.py --json ...` PASS with `orders is empty` warning.
- Artifacts: `wiki/evidence-store/run-manifests/2026-05-29-0211-hourly-autopilot.json`, `wiki/trade-ledger/orders/2026-05-29-0211-hourly-autopilot.json`, [[2026-05-29-0211-hourly-autopilot]]. Review due: no new fills; existing validation fills remain `회고 대기`.
