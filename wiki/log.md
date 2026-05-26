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
