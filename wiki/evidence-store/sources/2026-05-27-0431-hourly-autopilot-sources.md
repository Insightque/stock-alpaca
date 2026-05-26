# 2026-05-27-0431-hourly-autopilot source capture

- 생성 시각: `2026-05-26T19:35:30Z`
- Workflow: `harness/workflows/hourly-autopilot.md`
- Paper mode: `.env`에서 `ALPACA_PAPER_TRADE=true` 확인. API key 값은 출력하거나 기록하지 않음.

## Alpaca core preflight

- Source ref: `wiki/evidence-store/sources/2026-05-27-0431-hourly-autopilot-alpaca-core-preflight.json`
- Hard gate: `pass`
- Clock: `2026-05-26T15:31:09.123434238-04:00`, market open `true`, next close `2026-05-26T20:00:00Z`
- Account: portfolio value `101631.14`, cash `42347.59`, buying power `137133.22`
- Positions: 13개. Open orders: AMZN buy 1주 order `hourly-20260527-0411-amzn-buy-1` status `new`.
- Universe symbols: 62개, `SPY`/`QQQ` 포함. Asset/quote/snapshot/latest trade rows all pass.

## Candidate quote snapshot

- INTC: bid `123.32`, ask `123.35`, midpoint `123.335`, spread `0.0243%`, quote time `2026-05-26T19:31:32.567873288Z`.
- AMAT: spread `0.5212%`, risk policy max `0.50%` 초과로 skip.
- SMH: spread `0.0282%`, semiconductor cluster exposure recheck candidate.
- AMZN: open buy order exists from prior run, duplicate/additional order skipped.

## SEC EDGAR

- Local ticker-CIK fallback: `INTC -> 0000050863` from `harness/sec-ticker-cik-map.json`.
- `get_company_info(identifier=0000050863)` pass: company `INTEL CORP`, CIK `50863`, fiscal year end `1227`.
- `get_recent_filings(identifier=0000050863, days=30, limit=5)` pass: recent forms included Form 3 on 2026-05-22, SD on 2026-05-19, and Form 4 filings on 2026-05-15.

## Alpha Vantage

- Required sequence attempted: `TOOL_LIST` -> `TOOL_GET("PING")` -> `TOOL_CALL("PING", {})` -> `TOOL_GET("NEWS_SENTIMENT")` -> `TOOL_CALL("NEWS_SENTIMENT", {"tickers":"INTC","sort":"LATEST","limit":5})`.
- PING returned `pong`. First non-PING candidate call was cancelled by wrapper safety; classification `gap_category=cancelled`, retry_count `0`, and no second Alpha function was attempted.

## FRED

- Source ref: `wiki/evidence-store/sources/2026-05-27-0431-hourly-autopilot-research-mcp-preflight.json`
- Scheduler research preflight provider `fred/get_macro_snapshot` pass. Latest rows included DGS10 `4.57` for 2026-05-21, DGS2 `4.08` for 2026-05-21, FEDFUNDS `3.64` for 2026-04-01, CPIAUCSL `332.407` for 2026-04-01, UNRATE `4.3` for 2026-04-01, and NFCI `-0.52300` for 2026-05-15.

## Yahoo Finance

- `get_yahoo_finance_news(ticker=INTC)` usable. Current articles included Intel foundry/Apple deal context and an Intel valuation-downgrade headline.
- `get_recommendations(ticker=INTC, recommendation_type=recommendations, months_back=12)` usable. Current row: strongBuy `2`, buy `11`, hold `30`, sell `2`, strongSell `3`.

## Firecrawl

- Tool catalog search did not expose a registered Firecrawl MCP tool. Per workflow, shell/curl/local wrapper was not called. Classification `gap_category=wrapper_error`.

## 제출 전 gate summary

- paper mode: `.env`의 `ALPACA_PAPER_TRADE=true` 확인.
- market clock: Alpaca preflight timestamp `2026-05-26T15:31:09.123434238-04:00`, market open true, next close `2026-05-26T20:00:00Z`.
- order plan path: `wiki/trade-ledger/orders/2026-05-27-0431-hourly-autopilot.json`.
- validators: universe strict PASS, MCP strict PASS, risk-check PASS.
- quote freshness/spread: INTC quote `2026-05-26T19:31:32.567873288Z`, quote age 0.09 minutes versus market.checked_at, bid 123.32, ask 123.35, spread 0.0243%.
- order shape: stock buy, whole share qty 1, day limit, limit 123.35, extended_hours false, client_order_id `hourly-20260527-0431-intc-buy-1`.
- duplicate/open-order check: current open order is AMZN buy 1주 only; no open INTC buy/sell order and no same-day INTC validation buy recorded in current open-order evidence.
- source refs: `wiki/evidence-store/sources/2026-05-27-0431-hourly-autopilot-alpaca-core-preflight.json`, `wiki/evidence-store/sources/2026-05-27-0431-hourly-autopilot-research-mcp-preflight.json`, `wiki/evidence-store/sources/2026-05-27-0431-hourly-autopilot-sources.md`.

## 제출 및 사후 점검

- `place_stock_order` 1차 호출: `user cancelled MCP tool call`.
- 같은 client_order_id `hourly-20260527-0431-intc-buy-1`로 재시도하기 전 reconcile 수행: `get_orders(status=all, symbols=INTC)`는 empty, pre-submit/then-live positions에서 INTC position 없음, `get_order_by_client_id`는 cancelled로 gap 기록.
- 동일 client_order_id 1회 retry: 다시 `user cancelled MCP tool call`. 추가 submit retry 없음.
- Post-attempt reconciliation: `get_orders(status=all, symbols=INTC)` empty, `get_account_activities(FILL, after=2026-05-26T19:30:00Z)` empty, `get_all_positions` pass 및 INTC position 없음.
- 제출 결과: 실제 생성된 INTC 주문 없음, 체결 없음. `orders_submitted=0`.
