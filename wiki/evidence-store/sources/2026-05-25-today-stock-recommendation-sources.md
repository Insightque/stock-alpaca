---
id: 2026-05-25-today-stock-recommendation-sources
source_type: alpaca|mcp
captured_at: 2026-05-25T13:06:06Z
source_url: ""
tool: "alpaca.get_clock|get_account_info|get_all_positions|get_orders|get_stock_latest_quote|get_news|yahoo_finance.get_yahoo_finance_news"
tickers: [AMD, AVGO, ETN, IONQ, LRCX, NOK, NVDA, QBTS, RGTI, SPY, QQQ, TSLA, TSM, UNH]
immutable: true
---

# 2026-05-25 오늘 종목추천 재점검 원천

## 요약

- `.env`의 `ALPACA_PAPER_TRADE=true`는 이전 오늘 run에서 확인됐고, 이번 재점검도 paper/no-submit 기준으로 수행했다.
- Alpaca clock 기준 `2026-05-25T09:06:06-04:00`에 미국 정규장은 닫혀 있었고, 다음 정규장 개장은 `2026-05-26T09:30:00-04:00`이다.
- Alpaca account는 ACTIVE이며 portfolio value 100418.67 USD, cash 44030.58 USD, long market value 56388.09 USD다.
- 현재 포지션은 AMD, AVGO, ETN, IONQ, LRCX, NOK, NVDA, RGTI, TSM, UNH 10개 long이고 미체결 주문은 없다.
- 가격 지표는 오늘 오전 캡처한 Alpaca MCP IEX adjusted 1Day bars `wiki/evidence-store/sources/2026-05-25-current-recommendation-bars.json`를 재사용했다. 2026-05-25은 미국 휴장이라 최신 정규장 종가는 2026-05-22다.
- 최신 Alpaca IEX quote는 모두 `2026-05-22` 장마감 부근 timestamp이며, 일부 후보는 ask=0 또는 매우 넓은 spread라 주문 근거로 사용하지 않았다.
- 주문 제출은 없었다. `orders_submitted=0`.

## 재확인된 계좌/포지션

| 항목 | 값 |
| --- | ---: |
| Portfolio value | 100418.67 USD |
| Cash | 44030.58 USD |
| Buying power | 138261.25 USD |
| Long market value | 56388.09 USD |
| Open orders | 0 |
| Invested ratio | 약 56.2% |

| 티커 | 수량 | 현재가 | 시장 가치 | 미실현 손익률 |
| --- | ---: | ---: | ---: | ---: |
| AMD | 14 | 467.51 | 6545.14 | +1.03% |
| AVGO | 15 | 414.14 | 6212.10 | +0.83% |
| ETN | 15 | 391.35 | 5870.25 | +0.89% |
| IONQ | 45 | 63.64 | 2863.80 | +0.25% |
| LRCX | 20 | 305.35 | 6107.00 | -0.83% |
| NOK | 400 | 15.47 | 6188.00 | +2.86% |
| NVDA | 35 | 215.33 | 7536.55 | +0.01% |
| RGTI | 120 | 26.42 | 3170.40 | +3.33% |
| TSM | 15 | 404.52 | 6067.80 | -0.17% |
| UNH | 15 | 388.47 | 5827.05 | +0.49% |

## 가격/정책 필터

| 티커 | 2026-05-22 종가 | 5D | 20D | 40D | 20D SPY 대비 | 20D QQQ 대비 | 판단 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| LRCX | 305.43 | +7.41% | +14.17% | +44.26% | +9.73%p | +6.10%p | 추천 1순위 |
| UNH | 388.55 | -1.27% | +9.48% | +44.98% | +5.04%p | +1.42%p | 추천 2순위 |
| AMD | 467.64 | +10.30% | +34.46% | +129.53% | +30.02%p | +26.40%p | 소액 staged only |
| TSLA | 425.95 | +0.87% | +13.21% | +14.49% | +8.77%p | +5.15%p | 관찰, source 보강 필요 |
| NVDA | 215.34 | -4.42% | +3.44% | +25.76% | -1.00%p | -4.63%p | 보유, 추가 보류 |
| NOK | 15.46 | +10.79% | +48.18% | +87.04% | +43.74%p | +40.11%p | 과열 추격 금지 |
| IONQ | 63.58 | +22.43% | +49.06% | +113.03% | +44.62%p | +40.99%p | 과열/투기 추격 금지 |
| RGTI | 26.41 | +48.04% | +59.05% | +83.02% | +54.61%p | +50.98%p | 과열/투기 추격 금지 |
| QBTS | 29.34 | +44.25% | +58.77% | +100.00% | +54.33%p | +50.70%p | watch-only |

벤치마크 20D 수익률은 SPY +4.44%, QQQ +8.07%다. 정책 v1.2 기준 hourly buy/sell 결과는 `observation_only`이므로 오늘 추천에는 보조 확인 신호로만 취급했다. 주 신호는 long-term quality momentum dry-run 후보 필터다.

## Quote 상태

| 티커 | bid | ask | timestamp | 주문 판단 |
| --- | ---: | ---: | --- | --- |
| LRCX | 289.85 | 0.00 | 2026-05-22T20:00:03Z | ask=0, 주문 불가 |
| UNH | 370.75 | 0.00 | 2026-05-22T20:00:04Z | ask=0, 주문 불가 |
| AMD | 446.78 | 493.73 | 2026-05-22T20:00:00Z | stale/wide spread |
| NVDA | 205.63 | 227.80 | 2026-05-22T20:00:01Z | stale/wide spread |
| QQQ | 716.79 | 716.88 | 2026-05-22T20:49:26Z | stale quote |

## 뉴스/이벤트 맥락

- Alpaca/Benzinga는 2026-05-24에 Goldman Sachs가 liquid cooling을 다음 AI trade로 보았다는 맥락을 제공했고 AMD/NVDA가 관련 심볼에 포함됐다.
- Alpaca/Benzinga는 2026-05-23에 NVDA가 earnings 이후 pullback을 보이며 CPU market 기대가 남아 있다는 맥락을 제공했다.
- Alpaca/Benzinga는 2026-05-23에 quantum stocks의 short interest 증가와 valuation concern을 함께 제시했다.
- Alpaca/Benzinga는 2026-05-22에 UBS가 UNH Buy를 유지하고 price target을 460으로 상향했다는 헤드라인을 제공했다.
- Yahoo Finance MCP는 LRCX의 AI-era tools, advanced packaging R&D, capital return, Morgan Stanley upgrade 맥락을 보강했다.
- Yahoo Finance MCP는 UNH의 dividend/valuation/turnaround narrative와 Medicare Advantage overpayment 정책 리스크를 함께 제공했다.
- Yahoo Finance MCP는 AMD/NVDA/AVGO 비교와 AMD의 AI chip cycle 노출을 보강했으나, AMD는 이미 가격 모멘텀이 강해 staged only로 낮췄다.

## 데이터 공백

- SEC/Alpha Vantage/FRED/Firecrawl은 이번 빠른 no-submit 추천 재점검에서 신규 긍정 근거로 사용하지 않았다.
- TSLA는 가격 필터만 보면 통과하지만, 이번 run에서 별도 이벤트/밸류에이션 원천을 캡처하지 않아 추천 상위권에 올리지 않았다.
- Fresh quote, 정상 bid/ask spread, active tradable 재확인은 다음 정규장 submit-mode 전에 필요하다.

## 외부 URL

- Alpaca/Benzinga AI liquid cooling: https://www.benzinga.com/markets/equities/26/05/52764221/top-stocks-to-benefit-as-goldman-sachs-touts-liquid-cooling-as-the-next-ai-trade
- Alpaca/Benzinga NVDA CPU market: https://www.benzinga.com/markets/equities/26/05/52762982/nvidia-stock-nears-key-price-as-huang-pitches-200-billion-cpu-market
- Alpaca/Benzinga quantum valuation concern: https://www.benzinga.com/markets/equities/26/05/52762946/quantum-computing-stocks-short-interest-jumps-amid-valuation-concerns
- Yahoo Finance LRCX AI-era tools/capital return: https://finance.yahoo.com/markets/stocks/articles/does-lam-research-lrcx-playbook-151046844.html
- Yahoo Finance UNH valuation check: https://finance.yahoo.com/markets/stocks/articles/unitedhealth-group-unh-valuation-check-081306938.html

## 위키 반영 메모

- 추천 리포트: `wiki/current-runs/daily/2026-05-25.md`
- dry-run 주문계획: `wiki/trade-ledger/orders/2026-05-25-2206-today-stock-recommendation.json`
- 실행 manifest: `wiki/evidence-store/run-manifests/2026-05-25-2206-today-stock-recommendation.json`
- 실제 주문, 취소, 포지션 변경은 없었다.
