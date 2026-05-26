# 2026-05-27 02:51 KST hourly autopilot sources

- run_id: `2026-05-27-0251-hourly-autopilot`
- 기준 시각: 2026-05-26 13:56 ET / 2026-05-27 02:56 KST
- paper mode: `.env`에서 `ALPACA_PAPER_TRADE=true` 확인. API key 값은 출력하지 않음.

## Alpaca MCP

- Scheduler-owned Alpaca core preflight: `wiki/evidence-store/sources/2026-05-27-0251-hourly-autopilot-alpaca-core-preflight.json`
- Preflight hard gate: pass.
- Market clock: `2026-05-26T13:51:08.757165289-04:00`, `is_open=true`, next close `2026-05-26T16:00:00-04:00`.
- 추가 market clock refresh: Alpaca MCP `get_clock` returned `is_open=true`, timestamp `2026-05-26T13:58:37.983877701-04:00`, next close `2026-05-26T16:00:00-04:00`.
- Account: portfolio value 101662.85 USD, cash 42657.04 USD, buying power 137687.35 USD, long market value 59005.81 USD.
- Positions: 12개 long US equity positions.
- Open orders: 0건.
- Recent fills: 2026-05-26 regular session에 LLY, FCX, NOK, NVDA paper validation buy fills 존재.
- Universe quote/snapshot/latest trade/asset/watchlist rows: preflight pass, 62/62 symbols loaded.
- 추가 AAPL quote refresh: Alpaca MCP `get_stock_latest_quote(symbols=AAPL, feed=iex)` returned bid 309.43, ask 309.46, quote timestamp `2026-05-26T17:56:03.094445033Z`.
- Alpaca news MCP: AAPL, INTC, SMH, AMZN, FCX, NOK, NVDA, LLY 대상으로 2026-05-26 13:30Z-17:53Z 조회. AAPL 관련 BofA Buy/price target raise 및 agentic AI valuation 기사, INTC/NVDA/MU 관련 AI capex/semiconductor 기사, NOK 52-week high 기사 확인.

## SEC EDGAR MCP

- Local SEC ticker cache fallback 확인: `harness/sec-ticker-cik-map.json`에서 `AAPL -> 0000320193`.
- SEC EDGAR `get_company_info(identifier=AAPL)`: success, Apple Inc., CIK 320193.
- SEC EDGAR `get_recent_filings(identifier=AAPL, days=30, limit=5)`: success. 최근 filing에는 2026-05-01 10-Q, 2026-05-05/06 Form 144, 2026-05-08/12 Form 4 포함.

## Alpha Vantage MCP

- `TOOL_LIST`: pass.
- `TOOL_GET("PING")`: pass.
- `TOOL_CALL("PING", {})`: pass, `pong`.
- Candidate data 단계 `TOOL_GET("NEWS_SENTIMENT")`: `user cancelled MCP tool call`.
- Workflow rule에 따라 candidate Alpha retries/function changes 없이 중단. `gap_category=cancelled`.

## FRED MCP

- Scheduler-owned research MCP preflight: `wiki/evidence-store/sources/2026-05-27-0251-hourly-autopilot-research-mcp-preflight.json`
- FRED `get_macro_snapshot`: pass.
- 사용 가능한 series: DGS10 4.57, DGS2 4.08, FEDFUNDS 3.64, CPIAUCSL 332.407, UNRATE 4.3, NFCI -0.52300.

## Firecrawl MCP

- Codex tool catalog에 registered Firecrawl MCP tool이 노출되지 않음.
- Workflow 요구에 따라 shell/curl/local wrapper는 호출하지 않음.
- `gap_category=wrapper_error`.

## Yahoo Finance MCP

- Yahoo Finance `get_yahoo_finance_news(AAPL)`: pass. Apple AI strategy, BofA AI potential, China shipment, analyst AI winner 관련 기사 확인.
- Yahoo Finance `get_recommendations(AAPL, recommendations, 12 months)`: pass. Current period counts: strongBuy 7, buy 23, hold 16, sell 1, strongSell 1.

## Candidate 판단 메모

- `AAPL`: no same-day duplicate buy, bid 309.43, ask 309.46, spread 0.0097%, quote fresh, SEC/Yahoo/FRED usable. 1주 validation buy 후보.
- `SMH`: price momentum과 spread는 좋지만 ETF라 SEC issuer confirmation이 제한되고 AI semiconductor cluster가 이미 큼. Recheck.
- `INTC`: spread 0.1144%와 당일 상대강도는 통과하지만 high-volatility 반도체 laggard thesis confidence가 AAPL보다 낮음. Recheck.
- `MU`: 당일 수익률은 강하지만 spread 0.765%로 risk policy spread 상한 0.50% 초과. Skip.
- `FCX`, `NOK`, `NVDA`, `LLY`: 같은 거래일 buy fill이 있어 duplicate buy 회피.

## Submit 및 post-trade reconciliation

- 제출 전 `get_orders(status=open, symbols=AAPL)`: 0건.
- 첫 `place_stock_order` call: `user cancelled MCP tool call`. Same client id 기준 reconciliation 전에는 다른 client id로 재시도하지 않음.
- Cancelled submit reconciliation:
  - `get_orders(status=all, symbols=AAPL)`: 0건.
  - `get_all_positions`: AAPL position 없음.
- 같은 `client_order_id=hourly-20260527-0251-aapl-buy-1`로 1회 재시도.
- Retry submit result: Alpaca order id `dda2173a-f512-4ee1-80a9-7e99a4bdfd7c`, status `pending_new`, submitted at `2026-05-26T18:00:09.297012573Z`, limit 309.46, qty 1.
- Post-submit `get_orders(status=all, symbols=AAPL)`: same order id/client id, status `new`, filled_qty 0.
- Post-submit `get_orders(status=open, symbols=AAPL)`: same order id/client id, status `new`.
- Post-submit `get_account_activities(activity_types=FILL, after=2026-05-26T17:55:00Z)`: 0건.
- Post-submit `get_all_positions`: AAPL position 없음.
- Post-submit `get_account_info`: MCP wrapper safety cancellation. `gap_category=cancelled`.
