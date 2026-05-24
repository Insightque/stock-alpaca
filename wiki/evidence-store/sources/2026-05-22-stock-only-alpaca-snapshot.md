---
id: 2026-05-22-stock-only-alpaca-snapshot
source_type: alpaca
captured_at: 2026-05-22T14:10:00Z
source_url: ""
tool: "mcp__alpaca__.get_account_info; mcp__alpaca__.get_clock; mcp__alpaca__.get_most_active_stocks; mcp__alpaca__.get_market_movers; mcp__alpaca__.get_asset; mcp__alpaca__.get_stock_snapshot; mcp__alpaca__.get_stock_bars; mcp__alpaca__.get_news"
tickers: [NVDA, RGTI, IONQ, QBTS, AMD, MU, INTC, TSLA, RKLB, NOK, NIO, GOVX]
immutable: true
---

# 주식 중심 Alpaca 스냅샷

## 요약

- 사용자는 ETF가 아니라 주식 중심의 금일 유망 종목 분석과 거래 제안을 요청했다.
- Paper mode는 `.env` 기준 `ALPACA_PAPER_TRADE=true`로 확인했다.
- Alpaca market clock은 `2026-05-22T10:05:00-04:00` 기준 장중이었다.
- 계좌는 포트폴리오 가치 100000 USD, 현금 100000 USD, 포지션 없음, 미체결 주문 없음이었다.
- 거래량/체결수 상위와 mover에서 ETF 및 warrant 성격을 제외하고 개별 주식을 검토했다.

## 핵심 근거

- 체결수 상위 주식 후보: NVDA, LFS, RGTI, FUTU, PCLA, QTEX, IONQ, QBTS, GOVX, AMD, MU, INTC, TSLA, RKLB, BIYA.
- 정책상 제외한 유형: ETF, warrant, 1달러 미만, 출처 부족 급등주, 유동성/스프레드 품질이 낮은 급등주.
- NVDA 최신 체결가 216.52, 전일 종가 219.47, 뉴스는 강한 실적/가이던스와 AI 수요를 강조했다.
- AMD 최신 체결가 464.20, 전일 종가 449.44, AI 반도체 동반 모멘텀을 받았다.
- NOK 최신 체결가 15.175, 전일 종가 14.18, Nvidia의 AI 인프라 관련 뉴스 맥락에 포함됐다.
- RGTI 최신 체결가 25.76, 전일 종가 22.04, 연방 양자컴퓨팅/CHIPS Act 촉매가 있었다.
- IONQ 최신 체결가 62.90, 전일 종가 58.87, 양자컴퓨팅 섹터 동반 강세 후보였다.
- QBTS 최신 체결가 29.21, 전일 종가 25.72, D-Wave 관련 CHIPS Act funding 뉴스가 있었다.
- RKLB는 SpaceX IPO 관심과 AI/space 내러티브가 있으나 $3B stock offering 뉴스가 리스크였다.
- NIO는 Q1 revenue beat 뉴스가 있었지만 당일 가격 흐름은 약했다.
- GOVX는 급등했지만 fractional 불가, 낮은 가격대, 이벤트성 mover 성격 때문에 제외했다.

## 언급된 티커

- NVDA, RGTI, IONQ, QBTS, AMD, MU, INTC, TSLA, RKLB, NOK, NIO, GOVX.

## 위키 반영 메모

- 최종 dry-run 거래 제안은 NVDA, AMD, NOK, RGTI, IONQ 다섯 종목으로 구성했다.
- QBTS는 강하지만 RGTI/IONQ와 촉매가 중복되어 watchlist로만 남겼다.
- 총 제안 투자액은 약 39%로 제한해 신규 stock-only 포트폴리오의 변동성 리스크를 낮췄다.
