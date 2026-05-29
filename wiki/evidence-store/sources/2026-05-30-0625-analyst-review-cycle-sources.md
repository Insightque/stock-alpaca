---
id: 2026-05-30-0625-analyst-review-cycle-sources
created_at: 2026-05-29T21:25:00Z
workflow: analyst-review-cycle
paper: true
---

# 2026-05-30 analyst review cycle sources

## 범위

2026-05-30 06:25 KST scheduled analyst review cycle은 주문 제출, 교체, 취소, 청산 없이 read-only reconciliation만 수행했다. `ALPACA_PAPER_TRADE=true`를 확인했고, Alpaca clock은 2026-05-29 17:21 ET 기준 closed, next open 2026-06-01 09:30 ET였다.

## Alpaca MCP reconciliation

- Account status: ACTIVE.
- Portfolio value: 102,008.32 USD.
- Cash: 34,800.26 USD.
- Buying power: 130,798.68 USD.
- Long market value: 67,208.06 USD.
- Open US equity orders: 0.
- Current positions: 32.
- Recent FILL activities after 2026-05-26: read successfully.
- Recent closed US equity orders after 2026-05-26: read successfully.
- Portfolio history: `get_portfolio_history(period=1W,timeframe=1D)` was cancelled on initial call and two retries. Gap category `cancelled`, retry_count 2.

## Research MCP coverage

| provider | queried | outcome | gap_category | retry_count | notes |
| --- | --- | --- | --- | ---: | --- |
| alpaca | true | usable | cancelled | 2 | Core account/orders/positions/fills/news usable; portfolio-history gap only. |
| sec-edgar | true | usable | not_applicable | 0 | Recent filings checked for ADBE, PLTR, INTC. |
| alpha-vantage | true | gap | cancelled | 0 | `TOOL_LIST -> TOOL_GET("PING") -> TOOL_CALL("PING", {})` returned pong. First non-PING candidate call was cancelled, so retries stopped. |
| fred | false | gap | wrapper_error | 0 | Registered callable FRED namespace was not exposed in this session; no shell/curl probing. |
| firecrawl | false | gap | wrapper_error | 0 | Registered callable Firecrawl namespace was not exposed in this session; no shell/curl probing. |
| yahoo-finance | true | usable | not_applicable | 0 | News checked for ADBE, PLTR, INTC. |

## Current event notes used

- Alpaca news on 2026-05-29 showed broad AI-market strength, Dell/Micron/Snowflake-driven AI spending momentum, and macro/Iran headlines affecting SPY/USO context.
- Yahoo Finance news for PLTR showed a software-sector rally, Dell AI Factory partnership validation, defense-tech momentum, and valuation disagreement.
- Yahoo Finance news for ADBE showed AI-agent/Firefly optimism mixed with concern that generative AI disrupts stock-photo economics.
- Yahoo Finance news for INTC was mostly indirect semiconductor/AI infrastructure context rather than a clean ticker-specific positive catalyst.
- SEC EDGAR recent filings:
  - ADBE: recent Form 4/Form 144/Schedule 13G/S-8 items in late April/early May; no new 2026-05-29 operating catalyst.
  - PLTR: 2026-05-29 Form 144 plus prior May Form 4 filings; useful as insider/sale-context risk, not a buy catalyst by itself.
  - INTC: 2026-05-29 Form 144 plus May Form 3/4/SD filings; no direct 1D positive catalyst identified from filings.

## Data gaps

- FRED and Firecrawl were expected by policy but not exposed as registered callable tools in this Codex session.
- Alpha Vantage candidate data was not available after one cancelled non-PING call.
- Alpaca portfolio history cancellation prevents full account-level MFE/MAE and cashflow-adjusted review.
