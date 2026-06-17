---
symbol: MRK
asset_type: stock
---

# MRK

## 2026-06-18 03:36 KST hourly-autopilot 사전 메모

`MRK`는 `2026-06-18-0331-hourly-autopilot` cycle에서 regular-session floor-size validation buy 후보로 다시 승격됐다. scheduler-owned `0331` Alpaca core preflight 기준 market open, account `ACTIVE`, open orders `0`, latest IEX quote `115.16/115.21`, spread `0.0434%`, active tradable US equity 조건이 모두 유지된다. 같은 cycle research preflight에서도 `MRK`가 symbol scope 안에 포함됐고 `SEC EDGAR`, `FRED`, `Yahoo Finance`가 positive confirmation을 제공한다. `Alpha Vantage`는 hourly throttle `provider_error`, `Firecrawl`은 credit 부족 `unknown` gap이지만 tiered MCP submit threshold 3개는 충족한다.

현재 포트폴리오는 같은 미국 거래일에 `AMZN/BAC/WMT/NKE/NEE/SO/COP/GOOGL/AAPL/XOM/MSFT/FCX/SLB` buy fill이 이미 누적돼 duplicate buy gate가 많고, `RGTI/PFE`는 same-day duplicate sell, `SO`는 same-day buy-for-trim과 trim metric gap으로 sell-first path가 막혀 있다. `MRK`는 기존 AI semiconductor/mega-cap/growth 노출을 늘리지 않으면서 `healthcare_pharma/defensive_healthcare` 분산 표본을 추가할 수 있는 몇 안 되는 preflight-covered executable 후보다. `paper_validation_execution.learning_trade_directive` 기준 eligible sell이 없는 cycle에서 남은 floor-size buy fallback 중 가장 실행 가능성이 높다.

출처: `wiki/evidence-store/sources/2026-06-18-0331-hourly-autopilot-alpaca-core-preflight.json`, `wiki/evidence-store/sources/2026-06-18-0331-hourly-autopilot-research-mcp-preflight.json`, `harness/recommendation-policy.yaml`, `harness/risk-policy.yaml`, `harness/symbol-metadata.yaml`

## 2026-06-18 03:40 KST hourly-autopilot 제출 결과

Alpaca MCP `place_stock_order`로 `MRK` 1주 regular-session day limit buy를 `115.21 USD`에 제출했다. `client_order_id=hourly-20260618-0331-buy-mrk`, `order_id=1bea80db-11a3-4441-9589-24d4a36f5fc7`이며 immediate reconciliation 기준 상태는 `new`, `filled_qty=0`, `filled_avg_price=null`이다. `get_orders(status=open)` 기준 현재 open US-equity order는 이 `MRK` buy 1건뿐이고, `get_all_positions` 기준 positions count는 여전히 `33`이라 이번 cycle 종료 시점에는 아직 fill되지 않은 open validation order로 남아 있다.

출처: [[2026-06-18-0331-hourly-autopilot]], `wiki/trade-ledger/positions/2026-06-18-0331-hourly-autopilot-post-trade.json`

## 이전 자동운영 이력

2026-05-30 00:31 KST hourly-autopilot에서 `MRK` 1주 day limit validation buy가 한 차례 제출됐지만 same-session open/new 상태 뒤 stale cleanup 경로에서 정리됐고 체결로 이어지지 않았다. 이후 여러 cycle에서는 위키 thesis page 부재 때문에 submit 후보 승격이 반복적으로 차단됐다. 이번 note는 그 결손을 메우는 현재-cycle 근거 페이지다.

출처: [[2026-05-30-0031-hourly-autopilot]], [[2026-05-30-0051-hourly-autopilot]], [[2026-05-30-0131-hourly-autopilot]], [[2026-06-18-0111-hourly-autopilot]]
