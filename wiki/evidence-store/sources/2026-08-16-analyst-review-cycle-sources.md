---
id: 2026-08-16-analyst-review-cycle-sources
created_at: 2026-08-16T23:49:49Z
workflow: analyst-review-cycle
paper: true
---

# 2026-08-16 analyst review cycle sources

## Runtime anchor

- evaluated runtime date: `Sunday, August 16, 2026 ET`
- last settled US regular-session close used for bars: `Friday, August 14, 2026 ET`
- workflow checksum: `f2e0c827a703feff49efe3fa2abc70a65a80f55da47e28ce4a26699a174bc0c9`

## Paper mode

- `ALPACA_PAPER_TRADE=true`

## Alpaca MCP reconciliation

- `get_clock`: `2026-08-16T19:48:09.647245343-04:00`, `is_open=false`, next open `2026-08-17T09:30:00-04:00`, next close `2026-08-17T16:00:00-04:00`
- `get_account_info`: status `ACTIVE`, cash `29,036.76`, portfolio value `100,806.67`, buying power `305,111.84`, long market value `71,769.91`, `balance_asof=2026-08-14`
- `get_orders(status=open)`: `0건`
- `get_orders(status=all, after=2026-07-20T00:00:00Z)`: recent filled review cohort `NOK 4건`, `AVGO 1건`
- `get_account_activities(activity_types=[FILL], after=2026-07-20T00:00:00Z)`: same fill continuity usable
- `get_all_positions`: `31건`
- `get_stock_bars(feed=iex, symbols=NOK,IONQ,GOOGL,WMT,MCD,SPY,QQQ,SMH, start=2026-08-10, end=2026-08-15)`: open-position monitor와 skipped recommendation 재점검에 사용
- `get_stock_snapshot(feed=iex, symbols=NOK,IONQ,GOOGL,WMT,MCD,SPY,QQQ,SMH)`: latest trade/quote continuity에 사용
- `get_news(symbols=NOK,IONQ,GOOGL,WMT,MCD, start=2026-08-10, end=2026-08-16)`: current catalyst monitor에 사용
- `get_portfolio_history`: cancelled `3회`. initial call과 2회 retry가 모두 `user cancelled MCP tool call`이었다.

## Due review state

- carry-forward due now:
  - none
- pending after this run:
  - `2026-08-21 US regular-session close`: `NOK` `20D`

## Fill continuity

| symbol | fill timestamp | fill | order id | client order id |
| --- | --- | ---: | --- | --- |
| `NOK` | `2026-07-24T13:17:49.876154Z` | `9.67` | `e91d0b66-f1b4-49a1-bcd8-7c2283132857` | `ah-20260723-2151-sell-nok-01` |
| `NOK` | `2026-07-23T03:18:44.891868Z` | `10.78` | `d249fed3-33a1-4b84-b84d-4902851737c9` | `ah-20260722-1211-sell-nok-01` |
| `NOK` | `2026-07-23T01:16:18.201350Z` | `10.95` | `87eea18c-86c7-47b6-8565-4e5b56fef08b` | `ah-20260722-0931-sell-nok-01` |
| `NOK` | `2026-07-22T12:30:02.329191Z` | `10.33` | `78270797-caec-4673-a861-69f4db403bc0` | `ah-20260722-2111-sell-nok-01` |
| `AVGO` | `2026-07-22T01:48:58.933756Z` | `384.14` | `aea04b7c-a44e-470d-b6a0-bfa05827fd4a` | `ah-20260722-0911-sell-avgo-01` |

## Open-position monitor calculations

| symbol | qty | avg | `2026-08-10 ET` close | `2026-08-14 ET` close | latest trade | move vs `2026-08-10` | unrealized |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `NOK` | 398 | `15.044573` | `9.12` | `10.77` | `10.78` | `+18.09%` | about `-28.48%` |
| `IONQ` | 45 | `63.48` | `42.51` | `46.30` | `46.30` | `+8.92%` | about `-27.11%` |
| `GOOGL` | 5 | `376.204` | `357.545` | `345.86` | `345.33` | `-3.27%` | about `-8.21%` |

## Skipped recommendation calculations

| symbol | basis close | `2026-08-14 ET` close | return |
| --- | ---: | ---: | ---: |
| `WMT` | `109.46` (`2026-07-24 ET`) | `115.27` | `+5.31%` |
| `MCD` | `264.715` (`2026-07-24 ET`) | `272.825` | `+3.06%` |

## Benchmark window `2026-08-10 ET` -> `2026-08-14 ET`

- `SPY 773.02 -> 776.30` = `+0.42%`
- `QQQ 720.805 -> 731.045` = `+1.42%`
- `SMH 569.46 -> 587.78` = `+3.22%`

## Current Alpaca news continuity

- `NOK`
  - `2026-08-13`: `Why Is Nokia Stock Surging on Thursday?`
- `IONQ`
  - no symbol-specific Alpaca news returned in this query window
- `GOOGL`
  - `2026-08-15`: `Consumer Tech (Aug 10-14): ...`
  - `2026-08-14`: `Bill Ackman Exits Alphabet, Raises Bets on Microsoft & Meta`
  - `2026-08-14`: `MSFT Could Emerge as Big Tech's Free Cash Flow King in 2027 While GOOGL, META Stay Negative: Analyst`
- `WMT`
  - `2026-08-15`: `Earnings Volatility Watch: Wolfspeed and 9 Other Stocks Could Swing Up to 17% this Week`
- `MCD`
  - no symbol-specific Alpaca news returned in this query window

## Provider coverage

| provider | outcome | gap_category | note |
| --- | --- | --- | --- |
| `alpaca` | usable | `not_applicable` | account/order/fill/position/bars/snapshot/news usable, portfolio history cancelled |
| `sec-edgar` | gap | `wrapper_error` | registered server exists in `.vscode/mcp.json`, but callable Codex tool namespace was not exposed in this session |
| `alpha-vantage` | gap | `wrapper_error` | registered server exists, but mandatory `TOOL_LIST/TOOL_GET/TOOL_CALL(PING)` surface was not exposed |
| `fred` | gap | `wrapper_error` | registered callable tool surface 미노출 |
| `firecrawl` | gap | `wrapper_error` | registered callable tool surface 미노출 |
| `yahoo-finance` | gap | `wrapper_error` | registered callable tool surface 미노출 |

## Data gaps

- `alpaca get_portfolio_history` cancelled `3회`
- `tool_search` query `alpaca sec edgar alpha vantage fred firecrawl yahoo finance MCP tools` returned `0 tools found`
- research MCP tool discovery returned no callable surface for `sec-edgar`, `alpha-vantage`, `fred`, `firecrawl`, `yahoo-finance`
