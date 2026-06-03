---
id: 2026-06-04-0624-analyst-review-cycle-sources
created_at: 2026-06-03T21:24:26Z
workflow: analyst-review-cycle
paper: true
---

# 2026-06-04 analyst review cycle sources

## Alpaca MCP reconciliation

- Paper mode: `ALPACA_PAPER_TRADE=true`.
- Clock: 2026-06-03 17:21 ET 기준 market closed, next open 2026-06-04 09:30 ET, next close 2026-06-04 16:00 ET.
- Account: ACTIVE, portfolio value 102,969.30 USD, cash 34,339.00 USD, buying power 130,747.66 USD, long market value 68,630.30 USD.
- Open US equity orders: 0.
- Current positions: 32 symbols.
- Recent FILL activities after 2026-05-22: reviewed scope에서 sell fill 없음. 신규 due item은 AVGO after-hours fill 1건과 2026-05-29 validation fill cohort다.
- Portfolio history: initial call + 2 retries 모두 cancelled라 계좌 단위 MFE/MAE와 equity path 증거에서는 제외했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.

## Daily bar evidence

Alpaca MCP `get_stock_bars` with `feed=iex`, `timeframe=1Day`, `start=2026-05-22T00:00:00Z`, `end=2026-06-04T00:00:00Z` was used for the due 5D and AVGO review calculations.

Benchmark closes:

| Symbol | 2026-05-29 close | 2026-06-01 close | 2026-06-03 close |
| --- | ---: | ---: | ---: |
| SPY | 756.34 | 758.44 | 754.18 |
| QQQ | 738.21 | 742.60 | 744.205 |

## Provider coverage

| MCP | 상태 | gap_category | retry_count | 메모 |
| --- | --- | --- | ---: | --- |
| alpaca | usable | cancelled | 2 | core reconciliation, fills, orders, positions, news, daily bars usable; portfolio history cancelled after 3 total attempts. |
| sec-edgar | gap | cancelled | 1 | `get_insider_summary(AVGO, 30)` 재시도까지 모두 cancelled라 filing-grounded catalyst 보강에 쓰지 않았다. |
| alpha-vantage | gap | cancelled | 1 | Required `TOOL_LIST -> TOOL_GET("PING") -> TOOL_CALL("PING", {})` sequence를 수행했지만 PING TOOL_CALL이 cancelled되어 non-PING Alpha calls를 중단했다. |
| fred | gap | wrapper_error | 0 | Registered callable namespace가 노출되지 않아 shell/curl probing 없이 wrapper error로 분류했다. |
| firecrawl | gap | wrapper_error | 0 | Registered callable namespace가 노출되지 않아 shell/curl probing 없이 wrapper error로 분류했다. |
| yahoo-finance | usable | not_applicable | 0 | AVGO stock info와 WMT news 조회는 성공했다. AVGO post-market 급락과 WMT retail headline을 보조 컨텍스트로 사용했다. |

## News and event context

- Alpaca news는 2026-06-03 ET 장중 rate-hike bets와 oil 상승, AI/semiconductor earnings preview, Walmart strength, Alphabet weakness를 함께 보여줬다.
- AVGO는 Alpaca news에서 earnings preview와 AI custom-chip narrative가 있었고, 같은 날 after-close headline에서는 mixed Q2 results에도 AI revenue surge가 확인됐지만 post-close 가격 반응은 약했다.
- WMT는 Yahoo Finance에서 analyst bullishness와 retail resilience 기사 흐름이 확인됐다. 5D 결과가 소폭 양호했던 배경 설명에는 도움이 되지만 policy 승격 증거는 아니다.
- AMZN/GOOGL/NKE/PFE/SO/NEE/V는 2026-05-29 validation add 이후 2026-06-03 close까지 SPY/QQQ 대비 약했다. defensive/quality label만으로 risk-on tape를 이기지 못했다.
- SLB는 energy/oil headline의 도움으로 5D 절대수익과 benchmark 초과가 개선됐다.

## Data gaps

- Alpaca portfolio history remained cancelled after the allowed retry count, so this review uses positions/orders/fills and symbol daily bars instead of account-level path metrics.
- SEC EDGAR and Alpha Vantage calls both ended in cancelled gaps, so no filing/earnings-provider detail was promoted into policy evidence.
- FRED and Firecrawl were not exposed as registered callable tools in this runtime and were classified as wrapper errors.
