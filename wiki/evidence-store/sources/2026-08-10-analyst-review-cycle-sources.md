---
id: 2026-08-10-analyst-review-cycle-sources
created_at: 2026-08-10T23:24:00Z
workflow: analyst-review-cycle
paper: true
---

# 2026-08-10 analyst review cycle sources

## Runtime anchor

- evaluated market session: `Monday, August 10, 2026 ET`
- workflow checksum: `f2e0c827a703feff49efe3fa2abc70a65a80f55da47e28ce4a26699a174bc0c9`

## Paper mode

- `ALPACA_PAPER_TRADE=true`

## Alpaca MCP reconciliation

- `get_clock`: `2026-08-10T19:21:56.338499944-04:00`, `is_open=false`, next open `2026-08-11T09:30:00-04:00`
- `get_account_info`: status `ACTIVE`, cash `29,036.76`, portfolio value `98,640.81`, buying power `300,863.91`, long market value `69,604.05`, last equity `99,181.77`
- `get_orders(status=open)`: `0건`
- `get_orders(status=all, after=2026-07-22T00:00:00Z)`: recent filled review cohort `AVGO 1건`, `NOK 4건`
- `get_account_activities(activity_types=[FILL], after=2026-07-22T00:00:00Z)`: same fill continuity usable
- `get_all_positions`: `31건`
- `get_watchlists`: `0건`
- `get_stock_bars(feed=iex, symbols=AVGO,NOK,SPY,QQQ,SMH,IONQ,GOOGL,WMT,MCD, start=2026-07-22, end=2026-08-10)`: due horizon closeout 계산과 benchmark cross-check에 사용
- `get_stock_snapshot(feed=iex, symbols=NOK,IONQ,GOOGL,WMT,MCD,AVGO,SPY,QQQ,SMH)`: current open-position monitor와 latest trade/quote cross-check에 사용
- `get_news(symbols=NOK,IONQ,GOOGL,AVGO,WMT,MCD, start=2026-07-22, end=2026-08-10)`: current catalyst monitor에 사용
- `get_portfolio_history`: cancelled `3회`. account curve 기반 attribution은 이번 run에서 보강하지 못했다.

## Due review closeout status

- immediate due now:
  - `AVGO` `2026-07-22 ET` trim cohort `5D`
  - `NOK` `2026-07-22 ET` trim cohort `5D`
  - `NOK` `2026-07-24 ET` trim `1D`
  - `NOK` `2026-07-24 ET` trim `5D`
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

## Due closeout calculations

### `2026-07-22 ET` trim cohort `5D`

| symbol | fill basis | `2026-07-29 ET` close | return |
| --- | --- | ---: | ---: |
| `AVGO` | `384.14` | `370.33` | `-3.59%` |
| `NOK` | `10.95`, `10.78` | `8.40` | 평균 `-22.69%` |

- benchmark window:
  - `SPY 747.49 -> 729.57` = `-2.40%`
  - `QQQ 705.19 -> 661.60` = `-6.18%`
  - `SMH 586.90 -> 503.73` = `-14.17%`

### `2026-07-24 ET` `NOK` trim `1D/5D`

| horizon | fill | closeout close | return |
| --- | ---: | ---: | ---: |
| `1D` (`2026-07-27 ET`) | `9.67` | `9.27` | `-4.14%` |
| `5D` (`2026-07-31 ET`) | `9.67` | `9.10` | `-5.89%` |

- benchmark windows:
  - `1D`: `SPY 738.90 -> 738.85` = `-0.01%`, `QQQ 684.33 -> 682.13` = `-0.32%`
  - `5D`: `SPY 738.90 -> 746.79` = `+1.07%`, `QQQ 684.33 -> 687.89` = `+0.52%`

## Current snapshot bundle

- `NOK`: daily close `9.12`, prev close `9.36`, latest trade `9.12`, latest quote `9.10 / 9.18`
- `IONQ`: daily close `42.51`, prev close `44.43`, latest trade `42.54`
- `GOOGL`: daily close `357.545`, prev close `354.35`, latest trade `357.03`
- `AVGO`: daily close `422.375`, prev close `427.57`, latest trade `422.375`
- `WMT`: daily close `112.67`, prev close `111.82`
- `MCD`: daily close `273.675`, prev close `274.48`
- `SPY`: daily close `773.02`
- `QQQ`: daily close `720.805`
- `SMH`: daily close `569.46`

## Open-position monitor bundle

- `NOK`: `398주`, avg `15.044573`, current `9.12`, unrealized about `-39.38%`
- `IONQ`: `45주`, avg `63.48`, current `42.54`, unrealized about `-33.03%`
- `GOOGL`: `5주`, avg `376.204`, current `357.03`, unrealized about `-4.96%`
- `AMD`: `14주`, avg `462.73`, current `469.67`, unrealized about `+1.50%`

## Current Alpaca news continuity

- `IONQ`
  - `2026-08-05`: `IonQ Posts Q2 Double Beat, Raises 2026 Outlook, Shares Rise`
  - `2026-08-07`: `Why Is IonQ Stock Surging Friday?`
- `GOOGL`
  - `2026-08-05`: `Alphabet Stock Dives as Key AI Leadership Exits`
  - `2026-08-06`: `GOOGL Stock Declined Last Month on Gemini 3.5 Pro Launch Delay Reports`
- `AVGO`
  - `2026-08-05`: `Broadcom, Marvell And Nvidia Could Feel the Impact of US Ban on Chinese AI Components`
  - `2026-08-07`: `Why Is Broadcom Stock Surging Friday?`
- `MCD`
  - `2026-08-05`: `McDonald’s Long-Term Strategy 'Coming Into Greater Focus'`
- `WMT`
  - `2026-08-08`: `BofA Sounds Alarm On Extreme Bullishness. These ETFs Offer a Defensive Play`

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
- research MCP tool discovery returned no callable surface for `sec-edgar`, `alpha-vantage`, `fred`, `firecrawl`, `yahoo-finance`
