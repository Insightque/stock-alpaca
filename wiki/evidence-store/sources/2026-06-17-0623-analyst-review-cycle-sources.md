---
id: 2026-06-17-0623-analyst-review-cycle-sources
created_at: 2026-06-16T21:23:55Z
workflow: analyst-review-cycle
paper: true
---

# 2026-06-17 06:23 KST analyst review cycle sources

## Alpaca MCP reconciliation

- `get_clock`: `2026-06-16T17:22:17.052741089-04:00`, `is_open=false`, next open `2026-06-17T09:30:00-04:00`
- `get_account_info`: status `ACTIVE`, cash `30,344.81`, portfolio value `100,693.70`, buying power `302,530.20`, long market value `70,348.89`
- `get_all_positions`: `33건`
- `get_orders(status=open)`: `0건`
- `get_orders(status=all, after=2026-06-10T00:00:00Z, limit=200)`: 2026-06-15 ET regular fill `18건`, 2026-06-16 ET regular sell/trim `3건`과 `RGTI` cancel `1건` 확인
- `get_account_activities(activity_types=FILL, after=2026-06-10T00:00:00Z, page_size=100)`: fill cross-check usable
- `get_stock_snapshot(feed=iex)`: `RGTI/BAC/WMT/AVGO/NEE/JPM/FCX/SLB/XOM/NKE/COP/V/SO/MSFT/GOOGL/AMZN/AAPL/PFE/NOK/SPY/QQQ` daily close 확인
- `get_watchlists`: `0건`
- `get_portfolio_history(period=1M,timeframe=1D,intraday_reporting=market_hours,pnl_reset=no_reset)`: initial + retry 1 + retry 2 모두 cancelled

## Review scan status

- closeout due now:
  - `2026-06-15 ET` regular fill cohort `1D` `18건`
  - `5D` due queue `14건`은 `2026-06-17 ET` close 이후
  - `20D` due queue `1건(NOK)`은 `2026-06-18 ET` close 이후
- due-index update target summary:
  - prior `pending_1d_count=18`, `pending_5d_count=19`, `pending_20d_count=1`
  - post-closeout target `pending_1d_count=0`, `pending_5d_count=37`, `pending_20d_count=1`
  - `blocked_add_symbols=[NOK]`

## 2026-06-15 ET fill cohort 1D closeout metrics

| symbol | side | fill | 2026-06-16 close | return |
| --- | --- | --- | --- | --- |
| `RGTI` | sell | `23.366667` | `20.63` | `-11.71%` |
| `BAC` | buy | `56.28` | `56.85` | `+1.01%` |
| `WMT` | buy | `120.20` | `121.07` | `+0.72%` |
| `AVGO` | sell | `392.14` | `376.53` | `-3.98%` |
| `NEE` | buy | `85.78` | `86.24` | `+0.54%` |
| `JPM` | buy | `321.53` | `331.14` | `+2.99%` |
| `FCX` | buy | `69.49` | `70.155` | `+0.96%` |
| `SLB` | buy | `54.03` | `53.085` | `-1.75%` |
| `XOM` | buy | `141.76` | `141.875` | `+0.08%` |
| `NKE` | buy | `45.36` | `45.04` | `-0.71%` |
| `COP` | buy | `112.62` | `111.33` | `-1.15%` |
| `V` | buy | `324.83` | `333.21` | `+2.58%` |
| `SO` | buy | `94.37` | `94.305` | `-0.07%` |
| `MSFT` | buy | `398.71` | `393.97` | `-1.19%` |
| `GOOGL` | buy | `371.22` | `373.37` | `+0.58%` |
| `AMZN` | buy | `246.19` | `246.15` | `-0.02%` |
| `AAPL` | buy | `296.11` | `299.26` | `+1.06%` |
| `PFE` | sell | `26.01` | `26.05` | `+0.15%` |

## Benchmark closeout context

- `SPY`: `754.75 -> 750.58`, `-0.55%`
- `QQQ`: `743.81 -> 729.87`, `-1.87%`

## Open-position monitor metrics

- `AAPL`: qty `6`, avg `301.965`, close `299.26`, unrealized 약 `-0.90%`
- `AVGO`: qty `1`, avg `435.995`, close `376.53`, unrealized 약 `-13.64%`
- `NOK`: qty `402`, avg `15.044527`, close `13.975`, unrealized 약 `-7.11%`
- `RGTI`: qty `28`, avg `25.569583`, close `20.63`, unrealized 약 `-19.32%`
- `FCX`: qty `6`, avg `65.675`, close `70.155`, unrealized 약 `+6.82%`

## Provider coverage

| provider | outcome | gap_category | note |
| --- | --- | --- | --- |
| `alpaca` | usable | `not_applicable` | core reconciliation usable, `portfolio_history`만 cancelled |
| `sec-edgar` | usable | `not_applicable` | `AVGO/AAPL/NOK` recent filings usable |
| `alpha-vantage` | gap | `provider_error` | required health-check 후 `EARNINGS(AAPL)` daily-rate-limit payload |
| `fred` | gap | `wrapper_error` | 등록 MCP callable surface 미노출 |
| `firecrawl` | gap | `wrapper_error` | 등록 MCP callable surface 미노출 |
| `yahoo-finance` | usable | `not_applicable` | `FCX/WMT/NOK` contextual signals usable |

## Research context

### Alpha Vantage

- health check sequence:
  - `TOOL_LIST` pass
  - `TOOL_GET(PING)` pass
  - `TOOL_CALL(PING,{})` -> `pong`
- candidate call:
  - `TOOL_GET(EARNINGS)` pass
  - `TOOL_CALL(EARNINGS,{symbol:"AAPL"})` -> daily rate-limit payload, `gap_category=provider_error`

### SEC EDGAR

- `AVGO`: recent `2026-06-16 Form 144 x2`, `2026-06-15 Form 4`, `2026-06-11 8-K`
- `AAPL`: recent `2026-05-29 Form 4`, `2026-05-28 SD`, `2026-05-27 Form 144`
- `NOK`: recent `2026-06-09 6-K`, `2026-06-05 6-K`, `2026-06-01 6-K`

### Yahoo Finance

- `FCX` 뉴스: copper tariff uncertainty와 commodity/materials rotation 맥락이 계속 보강된다.
- `WMT` 뉴스: consumer defensive rerating, World Cup demand, grocery delivery/product mix 기사와 legal noise가 혼재한다.
- `NOK` 추천 변경: `2026-06-12` JP Morgan `Overweight`, PT `14 -> 21`; `2026-04-27` Argus `Hold -> Buy`

## Skipped recommendation evidence

- `FCX`: backlog-throttle가 걸렸던 buy skip 이후에도 copper/materials 강세가 이어져 missed-upside 사례는 유지된다.
- `WMT`: 최근 skip cost는 제한적이고 consumer defensive tape는 여전히 완만하다.
- `NEE`: backlog-throttle가 풀리기 전 공격적으로 추격해야 할 구조적 missed-upside까지는 아니다.

## Data gaps

- `fred`, `firecrawl` callable MCP tool surface 미노출로 `wrapper_error`
- `alpaca get_portfolio_history` 3회 취소로 계좌 curve/MFE-MAE 확인 불가
- `alpha-vantage` non-PING candidate call은 daily rate limit payload로 종료했고 추가 Alpha 함수는 시도하지 않았다
