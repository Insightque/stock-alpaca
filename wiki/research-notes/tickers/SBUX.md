---
symbol: SBUX
asset_type: stock
---

# SBUX

## 2026-06-18 04:54 KST hourly-autopilot 사전 메모

`SBUX`는 `2026-06-18-0451-hourly-autopilot` cycle에서 current-cycle scheduler research preflight symbol scope 안에 포함된 신규 regular-session floor-size validation buy 후보다. scheduler-owned `0451` Alpaca core preflight 기준 market open, account `ACTIVE`, open orders `0`, broad universe `62` symbols, latest quote rows fresh 조건이 유지됐고, live Alpaca submit-boundary continuity에서도 `2026-06-17T15:54:24.777131681-04:00` market open, `SBUX` same-day order history `0`, active tradable NASDAQ stock, IEX quote `99.56/99.59`, spread `0.0301%`가 재확인됐다.

current-cycle research preflight에서는 `SBUX`에 대해 `Yahoo Finance` recommendation breadth가 `strongBuy 5 / buy 12 / hold 16 / sell 2 / strongSell 2`로 mixed-positive usable row를 남겼고, `FRED` macro snapshot도 `DGS10 4.47`, `DGS2 4.07`, `NFCI -0.505`로 금리 환경 확인을 제공한다. `SEC EDGAR` lightweight row는 local CIK cache `0000829224`를 통해 symbol resolution은 되었지만 wrapper payload 상세는 비어 있어 filing-grounded upside를 과대평가하지 않는다. `Alpha Vantage`는 `empty_response`, `Firecrawl`은 credit 부족 `unknown` gap이지만 tiered MCP submit threshold `3` confirmations는 `SEC/FRED/Yahoo`로 충족된다.

현재 포트폴리오는 invested ratio 약 `72.03%`로 staged exposure path의 acceleration 구간에 있고, 같은 미국 거래일 buy fill은 `BAC/WMT/FCX/NKE/NEE/AMZN/MSFT/XOM/AAPL/GOOGL/COP/SO/SLB/MRK/NVDA`에 이미 누적돼 duplicate buy gate가 많다. sell-first 경로에서는 `SO`가 same-day buy-for-trim과 metric gap, `RGTI/PFE`가 same-day duplicate sell gate로 계속 막혀 executable trim이 없다. `SBUX`는 `consumer_cyclical / consumer_rate_sensitive / consumer_discretionary` cluster의 신규 분산 표본으로서 같은 cycle research coverage, 정상 spread, same-day duplicate 부재, review backlog nonblocking, validation floor cap `약 500.64 USD` 이하의 1주 notional을 동시에 충족하는 남은 가장 보수적인 learning-trade fallback이다.

출처: `wiki/evidence-store/sources/2026-06-18-0451-hourly-autopilot-alpaca-core-preflight.json`, `wiki/evidence-store/sources/2026-06-18-0451-hourly-autopilot-research-mcp-preflight.json`, `wiki/evidence-store/sources/2026-06-18-0451-hourly-autopilot-runtime-gate-evaluation.json`, `harness/recommendation-policy.yaml`, `harness/risk-policy.yaml`, `harness/symbol-metadata.yaml`

## 2026-06-18 05:02 KST hourly-autopilot 제출 결과

Alpaca MCP `place_stock_order`로 `SBUX` 1주 regular-session day limit buy를 `99.59 USD`에 제출했지만 actual `submitted_at`이 `2026-06-17T20:01:40.378968465Z` (`16:01:40 ET`)로 정규장 종료 뒤였다. live clock 재확인 결과 `2026-06-17T16:02:00.785015971-04:00`, `is_open=false`가 확인되어 workflow hard gate 위반을 즉시 교정했다. 같은 `order_id=bf29b7a9-3ddb-4fbc-8aca-6efc70d2cff6`, `client_order_id=hourly-20260618-0451-buy-sbux`에 대해 Alpaca MCP `cancel_order_by_id`를 호출했고, post-trade reconciliation 기준 주문은 `canceled_at=2026-06-17T20:02:04.050879938Z`, `filled_qty=0`, `filled_avg_price=null`, `open orders=0`으로 정리됐다.

해석은 `candidate passed pre-submit research/risk gates but missed actual regular-session close boundary`; 따라서 이번 cycle은 신규 `SBUX` 포지션이나 fill observation을 남기지 못했고, 다음 regular-session cycle에서는 close-boundary drift를 먼저 확인해야 한다.

출처: [[2026-06-18-0451-hourly-autopilot]], `wiki/trade-ledger/positions/2026-06-18-0451-hourly-autopilot-post-trade.json`
