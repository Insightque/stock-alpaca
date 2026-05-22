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
