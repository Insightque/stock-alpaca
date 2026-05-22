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
