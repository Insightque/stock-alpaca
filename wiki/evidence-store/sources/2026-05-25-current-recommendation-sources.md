---
id: 2026-05-25-current-recommendation-sources
source_type: alpaca|mcp|web
captured_at: 2026-05-24T23:42:18Z
source_url: ""
tool: "alpaca.get_account_info|get_clock|get_all_positions|get_orders|get_stock_bars|get_stock_snapshot|get_news|yahoo_finance.get_yahoo_finance_news|web"
tickers: [AMD, AVGO, ETN, IONQ, LRCX, NOK, NVDA, QBTS, RGTI, SMH, SPY, QQQ, TSLA, TSM, UNH]
immutable: true
---

# 2026-05-25 현재 종목 추천 원천

## 요약

- `.env`에서 `ALPACA_PAPER_TRADE=true`를 확인했다.
- Alpaca clock 기준 미국 동부 2026-05-24 19:37:59에 정규장은 닫혀 있었고, 다음 정규장 개장은 `2026-05-26T09:30:00-04:00`이다.
- Alpaca account는 ACTIVE이며 portfolio value 100418.67 USD, cash 44030.58 USD, long market value 56388.09 USD다.
- 현재 포지션은 AMD, AVGO, ETN, IONQ, LRCX, NOK, NVDA, RGTI, TSM, UNH 10개 long 포지션이고 미체결 주문은 없다.
- Alpaca MCP로 2026-02-01~2026-05-24 IEX adjusted 1Day bars를 `wiki/evidence-store/sources/2026-05-25-current-recommendation-bars.json`에 캡처했다.
- 장 마감 후 quote는 일부 종목의 ask가 0이거나 스프레드가 비정상적으로 넓어 submit-mode 근거로 쓰지 않았다. 이번 결과는 no-submit 추천과 dry-run 검토다.

## 핵심 근거

- SPY 20D 수익률은 +4.44%, QQQ 20D 수익률은 +8.07%였다.
- LRCX는 20D +14.17%, SPY 대비 +9.73%p, QQQ 대비 +6.10%p로 장기 후보 필터를 통과했다.
- UNH는 20D +9.48%, SPY 대비 +5.04%p, QQQ 대비 +1.42%p이고 5D -1.27%라 과열 추격 위험이 낮다.
- AMD는 20D +34.46%, SPY 대비 +30.02%p로 강하지만 5D +10.30%, 63D +137.84%라 staged entry만 적합하다.
- NOK, IONQ, RGTI, QBTS는 20D 모멘텀이 매우 강하지만 20D +45% 전후 또는 그 이상으로 과열/valuation/short-interest 리스크가 커 신규 추격 후보에서 제외했다.
- Alpaca/Benzinga 뉴스는 NVDA의 CPU 시장 기대, quantum stocks short interest/valuation concern, AMD 2nm Venice CPU/Taiwan AI 투자, RGTI/QBTS quantum funding 맥락을 제공했다.
- Yahoo Finance MCP는 LRCX의 AI-era tools/capital return, Morgan Stanley upgrade, UNH의 turnaround/valuation 및 Medicare Advantage 정책 리스크, AMD의 2nm Venice CPU와 대만 AI 투자 맥락을 보강했다.
- 웹 확인은 Alpaca 뉴스 URL과 NYSE holiday calendar를 보조 원천으로 확인하는 데 사용했다.

## 구조화 시그널

| ticker | asof | signal_type | value | confidence | source_ref | notes |
| --- | --- | --- | --- | --- | --- | --- |
| LRCX | 2026-05-22 close | price_momentum | 20D +14.17%, SPY 대비 +9.73%p, QQQ 대비 +6.10%p | high | `2026-05-25-current-recommendation-bars.json` | 추가매수 1순위 후보, fresh quote 전 주문 없음 |
| UNH | 2026-05-22 close | price_momentum | 20D +9.48%, 5D -1.27%, SPY 대비 +5.04%p | high | `2026-05-25-current-recommendation-bars.json` | 방어적 분산 추가 후보 |
| AMD | 2026-05-22 close | price_momentum | 20D +34.46%, 5D +10.30%, SPY 대비 +30.02%p | medium | `2026-05-25-current-recommendation-bars.json` | 촉매 강하지만 과열 근접, staged only |
| AMD | 2026-05-22~2026-05-24 | news_event | 2nm Venice CPU, Taiwan AI supply chain investment | medium | Alpaca/Yahoo Finance MCP | 긍정 촉매지만 가격 선반영 가능성 감점 |
| NVDA | 2026-05-22~2026-05-23 | news_event | CPU market pitch, post-earnings pullback/support narrative | medium | Alpaca/Benzinga | 핵심 thesis 유지, 신규추가보다 확인 필요 |
| NOK | 2026-05-22 close | risk | 20D +48.18%, 63D +104.46% | medium | `2026-05-25-current-recommendation-bars.json` | overheat guard로 신규 추격 보류 |
| IONQ | 2026-05-22 close | risk | 20D +49.06%, 5D +22.43% | medium | Alpaca/Benzinga | quantum valuation/short-interest concern |
| RGTI | 2026-05-22 close | risk | 20D +59.05%, 5D +48.04% | medium | Alpaca/Benzinga | 급등 후 신규 추격 금지 |
| QBTS | 2026-05-22 close | risk | 20D +58.77%, 5D +44.25% | medium | Alpaca/Benzinga | watch-only |
| LFS/QTEX/BIYA/TIGR | 2026-05-22 close | liquidity | price below risk-policy minimum or low ADV/high spread | high | Alpaca MCP | 주문 후보 제외 |

## 언급된 티커

- 추천 후보: LRCX, UNH, AMD.
- 보유/확인 후보: NVDA, TSM, AVGO, ETN, NOK.
- 관찰/추격 금지: IONQ, RGTI, QBTS, PLTR, TSLA, LFS, QTEX, BIYA, TIGR, FUTU, SOXS.
- 벤치마크: SPY, QQQ, SMH.

## 데이터 공백

- 현재 미국 정규장이 닫혀 있고 2026-05-25은 미국 휴장이라 fresh quote가 없다.
- Alpaca IEX 장마감/extended quote는 일부 ask=0 또는 비정상 스프레드가 있어 submit-mode spread check에 사용할 수 없다.
- 이번 quick recommendation run에서는 SEC filing, Alpha Vantage earnings, FRED macro, Firecrawl IR 원문 캡처를 긍정 근거로 사용하지 않았다. 해당 공백은 신규 주문 전 보강 대상이다.

## 외부 URL

- Alpaca/Benzinga NVDA CPU market: https://www.benzinga.com/markets/equities/26/05/52762982/nvidia-stock-nears-key-price-as-huang-pitches-200-billion-cpu-market
- Alpaca/Benzinga quantum short-interest/valuation: https://www.benzinga.com/markets/equities/26/05/52762946/quantum-computing-stocks-short-interest-jumps-amid-valuation-concerns
- Alpaca/Benzinga AMD 2nm Venice CPU: https://www.benzinga.com/markets/tech/26/05/52741867/what-is-going-on-with-amd-stock-on-friday-3
- Yahoo Finance LRCX AI-era tools/capital return: https://finance.yahoo.com/markets/stocks/articles/does-lam-research-lrcx-playbook-151046844.html
- Yahoo Finance UNH valuation check: https://finance.yahoo.com/markets/stocks/articles/unitedhealth-group-unh-valuation-check-081306938.html
- NYSE holiday calendar: https://markethours.io/market-holidays/nyse

## 위키 반영 메모

- 추천 리포트: `wiki/current-runs/daily/2026-05-25.md`
- dry-run 주문계획: `wiki/trade-ledger/orders/2026-05-25-current-recommendations.json`
- 실행 manifest: `wiki/evidence-store/run-manifests/2026-05-25-0842-current-recommendations.json`
- 실제 주문, 취소, 포지션 변경은 없었다.
