# 2026-05-27-0411-hourly-autopilot sources

- Run id: `2026-05-27-0411-hourly-autopilot`
- 조회 시각: 2026-05-27 04:12-04:14 KST
- 기준 시장 시각: 2026-05-26T15:11:05.905788802-04:00, market open
- Paper mode: `.env`의 `ALPACA_PAPER_TRADE=true` 확인. API key 값은 출력하거나 기록하지 않았다.

## Alpaca MCP core preflight

Scheduler-owned read-only preflight `wiki/evidence-store/sources/2026-05-27-0411-hourly-autopilot-alpaca-core-preflight.json`을 먼저 읽었다. `hard_gate_summary.status=pass`이고 clock/account/positions/open orders/recent activities/quotes가 모두 pass였다.

- Account: portfolio value 101684.58 USD, cash 42347.59 USD, buying power 137455.77 USD.
- Positions: 13개 long US equity/ETF positions. Short/crypto/options position 없음.
- Open orders: 0건.
- Recent same-day fills: LLY, FCX, NOK, NVDA, AAPL buy fills.
- AMZN asset check: active/tradable US equity, Alpaca `get_asset` preflight pass.
- AMZN quote: bid 263.06, ask 263.10, midpoint 263.08, spread 0.0152%, quote time 2026-05-26T19:11:29.894160025Z.

## Universe screen

`harness/symbol-metadata.yaml`, current positions, Alpaca preflight universe, `SPY`, `QQQ`를 포함해 62개 symbol을 broad universe로 확인했다. Pre-MCP shortlist는 current momentum, quote/spread, duplicate-order avoidance, cluster diversification을 같이 반영했다.

- Pre-MCP shortlist: `MU`, `AMD`, `KLAC`, `NOK`, `LRCX`, `AMAT`, `SMH`, `FCX`, `AMZN`, `INTC`
- Final candidates: `AMZN`, `INTC`, `AMAT`
- 제외 근거: `MU`, `AMD`, `KLAC`, `LRCX`는 momentum은 강하지만 spread 또는 semiconductor cluster 부담이 컸다. `NOK`, `FCX`는 같은 거래일 validation buy duplicate 회피. `SMH`는 ETF 분산 후보지만 이미 AI semiconductor complex가 큰 상태라 이번 validation 우선순위에서 제외.

## SEC EDGAR MCP

Local SEC CIK cache `harness/sec-ticker-cik-map.json`에서 `AMZN -> 0001018724`를 먼저 확인했다.

- `sec-edgar.get_company_info(identifier=0001018724)`: pass. SEC records 기준 company `AMAZON COM INC`, CIK 1018724, ticker AMZN, fiscal year end 1231.
- `sec-edgar.get_recent_filings(identifier=0001018724, days=30, limit=5)`: pass. 최근 30일 내 2026-05-22 8-K 및 Form 144 filings 확인.

## Alpha Vantage MCP

요구 순서대로 `TOOL_LIST`, `TOOL_GET("PING")`, `TOOL_CALL("PING", {})`, `TOOL_GET("NEWS_SENTIMENT")`를 실행했다. PING은 `pong`으로 pass였다. 이어진 첫 non-PING `TOOL_CALL("NEWS_SENTIMENT", {"tickers":"AMZN","sort":"LATEST","limit":10})`는 wrapper safety cancellation을 반환했다. 요구사항에 따라 Alpha candidate data retry는 중단하고 `gap_category=cancelled`로 분류했다.

## FRED MCP

Registered FRED MCP tool은 Codex tool catalog에 노출되지 않았다. Scheduler-owned research preflight `wiki/evidence-store/sources/2026-05-27-0411-hourly-autopilot-research-mcp-preflight.json`의 FRED `get_macro_snapshot` row가 pass이므로 usable macro evidence로 사용했다.

- DGS10 latest 4.57, DGS2 latest 4.08, CPIAUCSL latest 332.407, UNRATE latest 4.3, NFCI latest -0.52300.

## Firecrawl MCP

Registered Firecrawl MCP tool은 Codex tool catalog에 노출되지 않았다. Shell/curl/local wrapper 사용은 금지되어 있으므로 호출하지 않았고 `gap_category=wrapper_error`로 분류했다.

## Yahoo Finance MCP

- `yahoo-finance.get_yahoo_finance_news(ticker=AMZN)`: usable. Amazon 관련 market/profit, growth stock, AI/job, buy-zone 뉴스 헤드라인 다수 확인.
- `yahoo-finance.get_recommendations(ticker=AMZN, recommendation_type=recommendations, months_back=3)`: usable. 현재 period `strongBuy=15`, `buy=47`, `hold=4`, `sell=0`, `strongSell=0`.

## Decision summary

AMZN은 paper mode, market open, Alpaca core, active/tradable asset, no open order, fresh quote, 0.0152% spread, SEC, FRED, Yahoo usable/pass, universe strict, MCP strict, risk policy를 모두 통과할 경우 1-share paper validation buy 후보로 채택한다. Alpha와 Firecrawl 공백은 연구 MCP 3개 이상 usable/pass 조건을 깨지 않지만 review에서 재점검할 provider gap으로 남긴다.

## Validators and submission

- Universe strict: PASS.
- MCP strict: PASS.
- Risk validator: PASS. Buy notional 263.10 USD, post-order cash 42084.49 USD, post-order invested exposure 59606.024 USD.
- Pre-submit gate summary: `.env ALPACA_PAPER_TRADE=true`, market open, order plan `wiki/trade-ledger/orders/2026-05-27-0411-hourly-autopilot.json`, universe/MCP/risk validators PASS, quote age 약 7.4분 at submit, spread 0.0152%, whole-share day limit stock order, no AMZN duplicate/open-order conflict, source refs는 Alpaca core preflight/research preflight/source note.
- Submitted through Alpaca MCP `place_stock_order` only: AMZN buy 1, day limit, limit 263.10, client_order_id `hourly-20260527-0411-amzn-buy-1`.
- Submit response: order id `642f83f9-cce5-4555-b4eb-9bee644d8545`, status `pending_new`, submitted_at `2026-05-26T19:19:07.508236707Z`, filled_qty 0.
- Post-trade reconciliation: `get_orders(status=open)` returned the same order id/client id with status `new`, filled_qty 0, expires_at `2026-05-26T20:00:00Z`.
- Post-trade FILL activity query after `2026-05-26T19:10:00Z` returned no fills.
- Reconciliation gaps: symbol-filtered `get_orders(status=open/all, symbols=AMZN)`, `get_order_by_id`, post-submit `get_all_positions`, and post-submit `get_account_info` had wrapper/user cancellation. These are classified as `gap_category=cancelled`; they do not change the open-order evidence from `get_orders(status=open)`.
