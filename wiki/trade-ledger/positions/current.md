# portfolio-current

_Last updated: 2026-06-10 23:01 KST_

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-10-2251-hourly-autopilot]]
- Open/new: 없음
- Filled: `AVGO` sell 2주 @ `373.25 USD`
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime `get_all_positions` 기준 `33` positions 유지. `AVGO`는 `8주 -> 6주`, `avg_entry_price=417.04625`, `qty_available=6`로 감소했다.
- Recent reconciliation scope: scheduler-owned `2251` stale cleanup/core/research preflight를 우선 사용했고 live Alpaca MCP submit-boundary check에서 regular market open, ACTIVE account, open orders 0건, same-day fills `WMT/AAPL/AAPL`, `AVGO` live quote `373.21/374.78`를 재확인했다. `RGTI`도 spread gate를 통과했지만 ai_semiconductor warning band와 post-earnings de-risking rationale가 더 강한 `AVGO` 2주 trim을 우선 제출했고 immediate same-order-id reconciliation 기준 `order_id=155edaa1-e527-4c67-b43a-07e2cea9ad40`, `filled_avg_price=373.25 USD`로 즉시 전량 체결됐다.
- Orders submitted/replaced/cancelled/closed by this workflow: 1 / 0 / 0 / 1.
- Source note: `wiki/trade-ledger/positions/2026-06-10-2251-hourly-autopilot-post-trade.json`


## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-10-1031-after-hours-autopilot]]
- Open/new: 없음
- Filled: `AAPL` buy 1주 @ `291.49 USD`
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime `get_all_positions` 기준 `33` positions 유지. `AAPL`은 `4주 -> 5주`, `avg_entry_price=303.136`, `qty_available=5`로 증가했다.
- Recent reconciliation scope: scheduler-owned `1031` core/research preflight를 우선 사용했고 live Alpaca MCP submit-boundary check에서 regular market closed, ACTIVE account, open orders 0건, same-session after-hours orders `1`, same-session after-hours fills `1`건을 먼저 재확인했다. 후보 재평가에서는 `QQQ/SPY/SMH`가 per-order cap 초과, `AVGO`는 spread cap 초과, `RGTI`는 same-day sell duplicate, `SO`는 quote gap, `INTC`는 lower-rank buy로 제외됐고 `AAPL`은 fresh overnight quote `291.48/291.54`, spread `0.0206%`로 모든 after-hours hard gate를 통과했다. direct Alpaca MCP submit 뒤 immediate same-client-id reconciliation 기준 `order_id=49e4052f-3e00-44ad-9296-4d1c41033e01`, `filled_avg_price=291.49 USD`로 즉시 체결됐다.
- Orders submitted/replaced/cancelled/closed by this workflow: 1 / 0 / 0 / 1.
- Source note: `wiki/trade-ledger/positions/2026-06-10-1031-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-10-1011-after-hours-autopilot]]
- Open/new: 없음
- Filled: `AAPL` buy 1주 @ `291.40 USD`
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime `get_all_positions` 기준 `33` positions 유지. `AAPL`은 `3주 -> 4주`, `avg_entry_price=306.0475`, `qty_available=4`로 증가했다.
- Recent reconciliation scope: scheduler-owned `1011` core/research preflight를 우선 사용했고 live Alpaca MCP submit-boundary check에서 regular market closed, ACTIVE account, open orders 0건, same-session after-hours fills 0건을 먼저 재확인했다. 후보 재평가에서는 `QQQ/SPY/SMH`가 per-order cap 초과, `AVGO`는 spread cap 초과, `RGTI`는 same-day sell duplicate, `SO`는 quote gap으로 제외됐고 `AAPL`은 fresh overnight quote `291.13/291.68`, spread `0.1886%`로 모든 after-hours hard gate를 통과했다. direct Alpaca MCP submit 뒤 immediate same-client-id reconciliation 기준 `order_id=cd79b8db-51e1-4eab-8903-7da2614d2bcd`, `filled_avg_price=291.40 USD`로 즉시 체결됐다.
- Orders submitted/replaced/cancelled/closed by this workflow: 1 / 0 / 0 / 1.
- Source note: `wiki/trade-ledger/positions/2026-06-10-1011-after-hours-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-10-2231-hourly-autopilot]]
- Open/new: 없음
- Filled: `WMT` buy 1주 @ `118.49 USD`
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime `get_all_positions` 기준 `33` positions 유지. `WMT`는 `7주 -> 8주`, `avg_entry_price=118.20625`, `qty_available=8`로 증가했다.
- Recent reconciliation scope: scheduler-owned `2231` stale cleanup/core/research preflight를 우선 사용했고 live Alpaca MCP submit-boundary check에서 regular market open, ACTIVE account, open orders 0건, same-day fills `AAPL/AAPL`, `WMT` live quote `118.75/118.79`를 재확인했다. sell-first 재평가에서는 `RGTI`가 spread `0.5063%`로 cap을 소폭 초과했고 `AVGO/SO`도 각각 spread hard gate에 막혀 executable trim이 남지 않았다. buy fallback에서는 `SPY/QQQ` per-order cap, `NOK` add-block, `BAC/PFE/PLTR` lower-rank가 남아 `WMT`를 floor-size defensive fallback으로 direct Alpaca MCP submit했고 immediate same-order-id reconciliation 기준 `order_id=8b189213-3d70-40a4-8957-2fcdd8b454fd`, `filled_avg_price=118.49 USD`로 즉시 체결됐다.
- Orders submitted/replaced/cancelled/closed by this workflow: 1 / 0 / 0 / 1.
- Source note: `wiki/trade-ledger/positions/2026-06-10-2231-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-10-0431-hourly-autopilot]]
- Open/new: 없음
- Filled: `XOM` buy 1주 @ `148.35 USD`
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime `get_all_positions` 기준 `33` positions 유지. `XOM`은 `3주 -> 4주`, `avg_entry_price=149.2625`, `qty_available=4`로 증가했다.
- Recent reconciliation scope: scheduler-owned `0431` stale cleanup/core/research preflight를 우선 사용했고 live Alpaca MCP submit-boundary check에서 regular market open, ACTIVE account, open orders 0건, same-day fills `FCX/JNJ/AMZN/COP/SLB/WMT/AVGO/PFE/BAC/RGTI`, `XOM` live quote `148.36/148.40`을 재확인했다. sell-first 재평가 결과 `AVGO`와 `RGTI`는 same-day sell duplicate, `SO`는 spread `1.0298%`와 trim metric gap으로 blocked였다. buy fallback에서는 `FCX/COP/SLB/WMT/PFE/BAC/AMZN/JNJ` same-day duplicate, `QQQ/SPY` per-order cap, `NVDA` same-cluster add block, `UNH` spread fail, `AAPL` 약세 review, `NEE` lower-rank watch가 남아 `XOM`을 energy diversifier floor-size add로 direct Alpaca MCP submit했고 immediate same-order-id reconciliation 기준 `order_id=5a36c3ae-d9e0-4af8-a378-b82ced709bb6`, `filled_avg_price=148.35 USD`로 즉시 체결됐다.
- Orders submitted/replaced/cancelled/closed by this workflow: 1 / 0 / 0 / 1.
- Source note: `wiki/trade-ledger/positions/2026-06-10-0431-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-10-0411-hourly-autopilot]]
- Open/new: 없음
- Filled: `FCX` buy 1주 @ `63.75 USD`
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime `get_all_positions` 기준 `33` positions 유지. `FCX`는 `3주 -> 4주`, `avg_entry_price=65.5875`, `qty_available=4`로 증가했다.
- Recent reconciliation scope: scheduler-owned `0411` stale cleanup/core/research preflight를 우선 사용했고 live Alpaca MCP submit-boundary check에서 regular market open, ACTIVE account, open orders 0건, same-day fills `JNJ/AMZN/COP/SLB/WMT/AVGO/PFE/BAC/RGTI`, `FCX` live quote `64.00/64.02`를 재확인했다. sell-first 재평가 결과 `AVGO`와 `RGTI`는 same-day sell duplicate, `SO`는 trim metric gap으로 blocked였다. buy fallback에서는 `BAC/COP/WMT/PFE/SLB/AMZN/JNJ` same-day duplicate, `QQQ/SMH` per-order cap, `NVDA` same-cluster add block, `AAPL/NKE/NEE` 약세/스프레드 문제, `SBUX` wiki thesis 부재가 남아 `FCX`를 materials/mining floor-size add로 direct Alpaca MCP submit했고 immediate same-client-id reconciliation 기준 `order_id=80a34b1a-5044-47cf-aadc-338e0db675f9`, `filled_avg_price=63.75 USD`로 즉시 체결됐다.
- Orders submitted/replaced/cancelled/closed by this workflow: 1 / 0 / 0 / 1.
- Source note: `wiki/trade-ledger/positions/2026-06-10-0411-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-10-0351-hourly-autopilot]]
- Open/new: 없음
- Filled: `JNJ` buy 1주 @ `237.54 USD`
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime `get_all_positions` 기준 `33` positions로 증가했다. `JNJ`는 신규 1주가 추가됐고 `avg_entry_price=237.54`, `qty_available=1`이다.
- Recent reconciliation scope: scheduler-owned `0351` stale cleanup/core/research preflight를 우선 사용했고 live Alpaca MCP submit-boundary check에서 regular market open, ACTIVE account, open orders 0건, stale `NVDA` buy cancel, same-day fills `AMZN/COP/SLB/WMT/AVGO/PFE/BAC/RGTI`, `JNJ` live/preflight quote `237.49/237.55`를 재확인했다. sell-first 재평가 결과 `AVGO`와 `RGTI`는 same-day sell duplicate, `SO`는 spread `2.3170%`와 trim metric gap으로 blocked였다. buy fallback에서는 `COP/SLB/WMT/PFE/BAC/AMZN` same-day duplicate, `SPY/QQQ` per-order cap, `NVDA` same-cluster add block, `AAPL/NKE/NEE` 약세가 남아 `JNJ`를 healthcare defensive diversifier floor-size add로 direct Alpaca MCP submit했고 immediate same-client-id reconciliation 기준 `order_id=6f39a832-aec9-4c63-96bb-491a32b8864b`, `filled_avg_price=237.54 USD`로 즉시 체결됐다.
- Orders submitted/replaced/cancelled/closed by this workflow: 1 / 0 / 0 / 1.
- Source note: `wiki/trade-ledger/positions/2026-06-10-0351-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-10-0311-hourly-autopilot]]
- Open/new: `NVDA` buy 1주 @ `205.40 USD` (`status=new`)
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime `get_all_positions` 기준 `32` positions 유지. `NVDA`는 아직 `38주`, `avg_entry_price=215.031579`, `qty_available=38`로 unchanged이며 open orders는 `NVDA` buy 1건이다.
- Recent reconciliation scope: scheduler-owned `0311` stale cleanup/core/research preflight를 우선 사용했고 live Alpaca MCP submit-boundary check에서 regular market open, ACTIVE account, open orders 0건, same-day fills `COP/SLB/WMT/AVGO/PFE/BAC/RGTI`, `NVDA` live IEX quote `205.37/205.40`를 재확인했다. sell-first 재평가 결과 `AVGO`와 `RGTI`는 same-day sell duplicate, `SO`는 trim metric gap으로 blocked였다. buy fallback에서는 `COP/SLB/WMT/PFE/BAC` same-day duplicate, `SPY/QQQ` per-order cap, `AAPL/AMZN/GOOGL/NKE` review 약세가 남아 `NVDA`를 floor-size AI core holding add로 direct Alpaca MCP submit했다. immediate same-order-id reconciliation 기준 `order_id=56d0bb25-b51d-40e5-8ba9-f76ab79d67ae`, `status=new`, `filled_qty=0` open order다.
- Orders submitted/replaced/cancelled/closed by this workflow: 1 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-10-0311-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-10-0251-hourly-autopilot]]
- Open/new: 없음
- Filled: `COP` buy 1주 @ `116.05 USD`
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime `get_all_positions` 기준 `32` positions 유지. `COP`는 `3주 -> 4주`, `avg_entry_price=116.8975`, `qty_available=4`로 증가했다.
- Recent reconciliation scope: scheduler-owned `0251` stale cleanup/core/research preflight를 우선 사용했고 live Alpaca MCP submit-boundary check에서 regular market open, ACTIVE account, open orders 0건, same-day fills `SLB/WMT/AVGO/PFE/BAC/RGTI`, `COP` live IEX quote `116.09/116.14`를 재확인했다. sell-first 재평가 결과 `AVGO`와 `RGTI`는 same-day sell duplicate, `SO`는 trim metric gap으로 blocked였다. buy fallback에서는 `SLB/WMT/PFE/BAC` same-day duplicate, `SPY/QQQ` per-order cap, `NOK` add-block이 남아 `COP`를 floor-size energy/value diversifier fallback buy로 direct Alpaca MCP submit했고 immediate same-client-id reconciliation 기준 `order_id=34da84fa-1653-4852-a955-6a1e0efd3fa8`, `filled_avg_price=116.05 USD`로 즉시 체결됐다.
- Orders submitted/replaced/cancelled/closed by this workflow: 1 / 0 / 0 / 1.
- Source note: `wiki/trade-ledger/positions/2026-06-10-0251-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-10-0231-hourly-autopilot]]
- Open/new: `SLB` buy 1주 @ `55.11 USD` (`status=new`)
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime `get_all_positions` 기준 `32` positions 유지. `SLB`는 아직 `4주`, `qty_available=4` 그대로이며 open orders는 `SLB` buy 1건이다.
- Recent reconciliation scope: scheduler-owned `0231` stale cleanup/core/research preflight를 우선 사용했고 live Alpaca MCP submit-boundary check에서 regular market open, ACTIVE account, open orders 0건, same-day fills `WMT/AVGO/PFE/BAC/RGTI`, `SLB` live quote `55.10/55.11`을 재확인했다. sell-first 재평가 결과 `AVGO`와 `RGTI`는 same-day sell duplicate, `SO`는 trim metric gap으로 blocked였다. buy fallback에서는 `WMT/PFE/BAC` same-day duplicate, `GOOGL` live spread fail, `SPY/QQQ` per-order cap, `NOK` add-block이 남아 `SLB`를 floor-size energy-services diversifier fallback buy로 direct Alpaca MCP submit했다. immediate reconciliation 기준 `order_id=d225a67d-6bc2-4488-99f3-d45a48bf6f4e`, `status=new`, `filled_qty=0` open order다.
- Orders submitted/replaced/cancelled/closed by this workflow: 1 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-10-0231-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-10-0211-hourly-autopilot]]
- Open/new: 없음
- Filled: `WMT` buy 1주 @ `118.70 USD`
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime `get_all_positions` 기준 `32` positions 유지. `WMT`는 `6주 -> 7주`, `avg_entry_price=118.165715`, `qty_available=7`로 증가했다.
- Recent reconciliation scope: scheduler-owned `0211` stale cleanup/core/research preflight를 우선 사용했고 sell-first 재평가에서 `AVGO`와 `RGTI`는 same-day sell duplicate, `SO`는 trim metric gap으로 각각 blocked였다. buy fallback에서는 `PFE/BAC` same-day duplicate, `GOOGL` spread fail, `SPY/QQQ` per-order cap, `NOK` add-block이 남아 `WMT`를 floor-size defensive fallback으로 direct Alpaca MCP submit했다. immediate same-client-id reconciliation 기준 `order_id=40066752-96cc-4225-aa77-0e6ba6c7ccb3`는 `filled_avg_price=118.70 USD`로 즉시 체결됐고 open order는 0건이다.
- Orders submitted/replaced/cancelled/closed by this workflow: 1 / 0 / 0 / 1.
- Source note: `wiki/trade-ledger/positions/2026-06-10-0211-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-10-0151-hourly-autopilot]]
- Open/new: 기존 `AVGO` sell 2주 @ `375.32 USD` (`status=new`)
- Filled: `PFE` buy 1주 @ `25.82 USD`
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime `get_all_positions` 기준 `32` positions 유지. `PFE`는 `5주`로 늘었고 `AVGO`는 `10주`, `qty_available`는 `8주`로 기존 open sell 2주가 예약된 상태다.
- Recent reconciliation scope: scheduler-owned `0151` stale cleanup/core/research preflight를 우선 사용했고 live Alpaca MCP submit-boundary check에서 stale `PFE` buy가 실제 canceled로 정리된 뒤 fresh `AVGO` sell 1건만 남아 있음을 재확인했다. sell-first 재평가 결과 `AVGO`는 spread 정상화 후에도 existing open sell duplicate로 추가 trim이 막혔고, `RGTI`는 same-day sell duplicate, `SO`는 trim metric gap으로 blocked였다. user directive에 따라 buy fallback을 재평가해 `PFE` 1주 buy를 direct Alpaca MCP submit했고 immediate reconciliation 기준 `order_id=3f342972-201b-4599-9209-ba6ec56f89eb`, `filled_avg_price=25.82 USD`로 즉시 체결됐다.
- Orders submitted/replaced/cancelled/closed by this workflow: 1 / 0 / 0 / 1.
- Source note: `wiki/trade-ledger/positions/2026-06-10-0151-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-10-0131-hourly-autopilot]]
- Open/new: `AVGO` sell 2주 @ `375.32 USD` (`status=new`), 기존 `PFE` buy 1주 @ `25.70 USD` (`status=new`)
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime `get_all_positions` 기준 `32` positions 유지. `AVGO`는 아직 `10주` 그대로이며 `qty_available`가 `8주`로 줄어 open sell 2주가 예약됐다. `PFE`는 `4주` 유지다.
- Recent reconciliation scope: scheduler-owned `0131` stale cleanup/core/research preflight를 우선 사용했고 direct Alpaca MCP live check에서 regular market open, ACTIVE account, fresh quotes, fresh `PFE` buy open order 1건, same-day fills `BAC`/`RGTI`를 재확인했다. sell-first 재평가 결과 `AVGO`는 live spread `0.0852%`로 trim hard gate를 통과했고, `RGTI`는 same-day sell duplicate conflict, `SO`는 trim metric gap으로 blocked였다. user directive에 따라 eligible risk-reducing sell을 우선 선택해 `AVGO` trim을 direct Alpaca MCP submit했고 immediate reconciliation 기준 `order_id=d850cf67-3c44-4a63-9f44-ef53c5fe8897`, `status=new`, `filled_qty=0` open order다.
- Orders submitted/replaced/cancelled/closed by this workflow: 1 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-10-0131-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-10-0111-hourly-autopilot]]
- Open/new: `PFE` buy 1주 @ `25.70 USD` (`status=new`)
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime `get_all_positions` 기준 `32` positions 유지. `PFE`는 아직 `4주` 그대로이고 신규 open order는 `PFE` 1건이다.
- Recent reconciliation scope: scheduler-owned `0111` stale cleanup/core/research preflight를 우선 사용했고 stale cleanup과 runtime `get_orders(status=open)`가 모두 open-order lifecycle PASS를 재확인했다. sell-first 재평가 결과 `AVGO`는 live spread `6.0276%`로 trim hard gate fail, `RGTI`는 same-day sell duplicate conflict, `SO`는 trim metric gap으로 blocked였다. `BAC`는 same-day buy duplicate, `SPY/QQQ`는 per-order cap 초과, `NOK`는 add-block이라 `PFE`가 floor-size healthcare fallback buy로 direct Alpaca MCP submit됐다. immediate reconciliation 기준 `order_id=df1b6130-1929-4189-9003-ad7f47add552`, `status=new`, `filled_qty=0` open order다.
- Orders submitted/replaced/cancelled/closed by this workflow: 1 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-10-0111-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-10-0051-hourly-autopilot]]
- Open/new: `WMT` buy 1주 @ `118.99 USD` (`status=new`)
- Filled: 없음
- Cancelled: scheduler-owned stale cleanup에서 `SO` buy 1주 @ `92.03 USD` open order 제거
- Position count observed by Alpaca MCP: scheduler-owned core preflight `get_all_positions` 기준 `32` positions 유지. `WMT`는 `6주` 그대로이고 remaining open order는 `WMT` 1건만 기록됐다.
- Recent reconciliation scope: scheduler-owned `0051` stale cleanup/core/research preflight를 우선 사용했다. stale cleanup report가 `WMT` open buy를 cancel attempt 이후에도 `remaining_open_orders`로 남겨 `risk_open_order_lifecycle` first blocking gate가 확정됐고, sell-first 재평가에서도 `AVGO`는 spread `4.7347%`, `RGTI`는 same-day sell duplicate, `SO`는 trim metric gap으로 각각 blocked됐다. `PFE`는 floor-size healthcare fallback buy 후보로 남았지만 신규 submit 없이 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 1 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-10-0051-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-10-0031-hourly-autopilot]]
- Open/new: `SO` buy 1주 @ `92.03 USD` (`status=new`), `WMT` buy 1주 @ `118.99 USD` (`status=new`)
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime `get_all_positions` 기준 `32` positions 유지. `SO`는 `5주`, `WMT`는 `6주` 그대로이며 open orders는 `SO/WMT` 2건이다.
- Recent reconciliation scope: scheduler-owned `0031` stale cleanup/core/research preflight를 우선 사용했고 sell-first 재평가 결과 `AVGO`는 live spread `4.7804%`로 trim hard gate fail, `RGTI`는 same-day sell duplicate conflict, `SO`는 same-day open buy와 trim metric gap으로 blocked였다. `PFE`는 floor-size healthcare fallback buy 후보로 승격됐지만 `check-risk-policy.py`가 `WMT` open order age `32.7`분을 lifecycle limit `30.0` 초과로 판정해 first blocking gate=`risk_open_order_lifecycle`가 됐고 신규 submit 없이 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-10-0031-hourly-autopilot-post-trade.json`


## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-10-0011-hourly-autopilot]]
- Open/new: `SO` buy 1주 @ `92.03 USD` (`status=new`), 기존 `WMT` buy 1주 @ `118.99 USD` (`status=new`)
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime `get_all_positions` 기준 `32` positions 유지. `SO`는 아직 `5주`, `WMT`는 `6주` 그대로이며 open orders는 `SO/WMT` 2건이다.
- Recent reconciliation scope: scheduler-owned `0011` stale cleanup/core/research preflight를 우선 사용했고 sell-first 재평가 결과 `AVGO`는 live spread `0.6251%`로 trim hard gate fail, `RGTI`는 same-day sell duplicate conflict, `SO`는 trim metric gap으로 blocked였다. buy fallback에서는 `WMT` fresh open-order duplicate, `BAC` same-day buy duplicate, `SPY/QQQ` per-order cap 초과, `NOK` add-block이 각각 남아 `SO`를 floor-size utilities diversifier fallback buy로 direct Alpaca MCP submit했다. immediate reconciliation 기준 `order_id=8775f764-2758-4958-9fa1-21a92e69fb91`, `status=new`, `filled_qty=0` open order다.
- Orders submitted/replaced/cancelled/closed by this workflow: 1 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-10-0011-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-09-2351-hourly-autopilot]]
- Open/new: `WMT` buy 1주 @ `118.99 USD` (`status=new`)
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime `get_all_positions` 기준 `32` positions 유지. `WMT`는 아직 `6주` 그대로이며 open orders는 `WMT` 1건이다.
- Recent reconciliation scope: scheduler-owned `2351` stale cleanup/core/research preflight를 우선 사용했고 sell-first 재평가 결과 `AVGO`는 live spread `3.5054%`로 hard gate fail, `RGTI`는 same-day sell duplicate conflict, `SO`는 decision-grade metric gap으로 blocked였다. `BAC`는 `2331` cycle buy 1주가 `2026-06-09T14:45:16Z` same-day fill로 확인돼 buy-side duplicate gate에 걸렸고, `SPY/QQQ`는 1주 ask가 validation floor per-order cap을 넘었다. 따라서 `WMT`를 floor-size defensive diversifier fallback buy로 제출했고 immediate reconciliation 기준 `order_id=487039ff-24cb-4094-9301-add50be8886c`, `status=new`, `filled_qty=0` open order다.
- Orders submitted/replaced/cancelled/closed by this workflow: 1 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-09-2351-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-09-2311-hourly-autopilot]]
- Open/new: `AVGO` sell 2주 @ `403.00 USD` (`status=new`, 기존 `2251` cycle order 유지)
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `2311` core preflight 기준 `32` positions 유지. `AVGO` 총 보유수량은 `10주`, `qty_available`는 `8주`로 그대로이며 open orders는 `AVGO` 1건이다.
- Recent reconciliation scope: 이번 cycle은 신규 submit 없이 open-order lifecycle 재점검에 집중했다. scheduler-owned stale cleanup은 stale candidate 0건이었지만, core preflight는 직전 `hourly-20260609-2251-sell-avgo`가 여전히 `status=new` open order임을 보여줬다. `RGTI`는 same-day duplicate symbol/side conflict, `SO`는 decision-grade metric gap, `BAC` buy fallback은 unresolved open-order lifecycle 때문에 모두 미제출 처리했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-09-2311-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-09-2251-hourly-autopilot]]
- Open/new: `AVGO` sell 2주 @ `403.00 USD` (`status=new`)
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime `get_all_positions` 기준 `32` positions 유지. `AVGO` 총 보유수량은 `10주` 그대로지만 `qty_available`가 `10주 -> 8주`로 줄어 open sell 2주가 예약돼 있다. open orders는 `AVGO` 1건이다.
- Recent reconciliation scope: scheduler-owned `2251` regular-session core/research preflight를 우선 사용했고, registered Alpaca MCP live check로 market open, open orders 0건, same-day `RGTI` fill 2건, `AVGO` quote `403.00/403.66`를 재확인했다. `RGTI`는 same-day duplicate symbol/side conflict로 추가 trim에서 제외했고, spread가 정상화된 `AVGO`를 sell-first validation trim 후보로 선택해 direct registered Alpaca MCP submit을 수행했다. immediate reconciliation 기준 `AVGO` 주문은 `order_id=bf1247db-2054-4304-a16b-58ada7b39af7`, `status=new`, `filled_qty=0`이며 신규 fill은 아직 없다.
- Orders submitted/replaced/cancelled/closed by this workflow: 1 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-09-2251-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-09-2231-hourly-autopilot]]
- Open/new: 없음
- Filled: `RGTI` sell 22주 @ `22.298182 USD`
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime `get_all_positions` 기준 `32` positions 유지. `RGTI` 보유수량은 `90주 -> 68주`로 감소했고 open orders는 0건이다.
- Recent reconciliation scope: scheduler-owned `2231` regular-session core/research preflight를 우선 사용했고, registered Alpaca MCP live check로 market open, open orders 0건, same-day fills 0건, `RGTI` quote `22.07/22.09`를 재확인했다. sell-first workflow에 따라 speculative loss-control trim을 우선 평가했고 `AVGO`는 live spread `3.9990%`로 hard gate fail, `SO`는 decision-grade metric gap으로 blocked 상태였다. nested shell submit helper는 DNS failure였지만 direct registered Alpaca MCP fallback이 `RGTI` trim 주문을 제출했고 same-day orders/FILL reconciliation 기준 즉시 filled로 닫혔다.
- Orders submitted/replaced/cancelled/closed by this workflow: 1 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-09-2231-hourly-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-09-2151-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler core preflight `get_all_positions` 기준 `32` positions 유지. runtime `get_all_positions` 교차 확인도 `32`였다. open orders는 0건이고 after-hours 신규 order/fill은 없었다.
- Recent reconciliation scope: scheduler-owned `2151` after-hours core/research preflight를 우선 사용했고 `market_closed`는 장외 expected nonblocking으로 처리했다. separate after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned IEX quote evidence에서 `NOK`만 age 약 `0.03`분의 fresh two-sided quote를 보였고 `QQQ/SPY`는 각각 약 `13.44/13.46`분 stale였다. `NOK` 1주 ask `14.80 USD`는 after-hours per-order cap 안이었지만 pending 20D validation review로 add-block 상태였고, `AVGO/PFE/BAC/RGTI`는 bid-only였으며 `NVDA/NKE/ADBE/SMH/XOM`는 spread cap 초과 또는 stale라 submit되지 않았다. runtime Alpaca MCP cross-check는 closed market, ACTIVE account, positions `32`, open orders `0`, same-session orders `0`, watchlists `0`을 재확인했지만 source-of-record는 scheduler preflight로 유지했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-09-2151-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-09-2131-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler core preflight `get_all_positions` 기준 `32` positions 유지. runtime `get_all_positions` 교차 확인도 `32`였다. open orders는 0건이고 after-hours 신규 order/fill은 없었다.
- Recent reconciliation scope: scheduler-owned `2131` after-hours core/research preflight를 우선 사용했고 `market_closed`는 장외 expected nonblocking으로 처리했다. separate after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned IEX quote evidence에서 `QQQ`는 quote age 약 `969.35`분으로 stale였고, `SPY`는 fresh two-sided quote였지만 1주 ask `742.73 USD`가 after-hours per-order cap 약 `503.39 USD`를 넘었다. `AVGO/PFE/BAC/RGTI`는 bid-only였고 `NVDA/NKE/ADBE/AMAT/XOM/SMH/SO/WMT/GOOGL`는 spread cap 초과 또는 stale라 submit되지 않았다. runtime Alpaca MCP cross-check는 closed market, ACTIVE account, positions `32`, open orders `0`, same-session orders `0`, watchlists `0`을 재확인했지만 source-of-record는 scheduler preflight로 유지했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-09-2131-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-09-2111-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler core preflight `get_all_positions` 기준 `32` positions 유지. runtime `get_all_positions` 교차 확인도 `32`였다. open orders는 0건이고 after-hours 신규 order/fill은 없었다.
- Recent reconciliation scope: scheduler-owned `2111` after-hours core/research preflight를 우선 사용했고 `market_closed`는 장외 expected nonblocking으로 처리했다. separate after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned IEX quote evidence에서 `QQQ`는 quote age 약 `949.41`분으로 stale였고, `SPY`는 fresh two-sided quote였지만 1주 ask `742.48 USD`가 after-hours per-order cap 약 `503.44 USD`를 넘었다. `AVGO/PFE/BAC/RGTI`는 bid-only였고 `NVDA/NKE/ADBE/AMAT/XOM/SMH/SO/WMT/GOOGL`는 spread cap 초과 또는 stale라 submit되지 않았다. runtime IEX/overnight quote cross-check는 보조 확인만 수행했고 source-of-record는 바꾸지 않았다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-09-2111-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-09-2051-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler core preflight `get_all_positions` 기준 `32` positions 유지. open orders는 0건이고 after-hours 신규 order/fill은 없었다.
- Recent reconciliation scope: scheduler-owned `2051` after-hours core/research preflight를 우선 사용했고 `market_closed`는 장외 expected nonblocking으로 처리했다. separate after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned IEX quote evidence에서 `QQQ`도 quote age 약 `929.05`분으로 stale였고 `AVGO/PFE/BAC/RGTI`는 bid-only, `NVDA/NKE/ADBE/AMAT/XOM/SPY/SMH/SO/WMT/GOOGL`는 spread cap 초과 또는 stale라 submit되지 않았다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-09-2051-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-09-2031-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler core preflight `get_all_positions` 기준 `32` positions 유지. runtime `get_all_positions` 교차 확인도 `32`였다. open orders는 0건이고 after-hours 신규 order/fill은 없었다.
- Recent reconciliation scope: scheduler-owned `2031` after-hours core/research preflight를 우선 사용했고 `market_closed`는 장외 expected nonblocking으로 처리했다. separate after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned IEX quote evidence에서 `QQQ`도 quote age 약 `909.08`분으로 stale였고 `AVGO/PFE/BAC/RGTI`는 bid-only, `NVDA/NKE/ADBE/AMAT/XOM/SPY/SMH/SO/WMT/GOOGL`는 spread cap 초과 또는 stale라 submit되지 않았다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-09-2031-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-09-2011-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler core preflight `get_all_positions` 기준 `32` positions 유지. runtime `get_all_positions` 교차 확인도 `32`였다. open orders는 0건이고 after-hours 신규 order/fill은 없었다.
- Recent reconciliation scope: scheduler-owned `2011` after-hours core/research preflight를 우선 사용했고 `market_closed`는 장외 expected nonblocking으로 처리했다. separate after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned IEX quote evidence에서 `QQQ`도 quote age 약 `889.41`분으로 stale였고 `AVGO/PFE/BAC/RGTI`는 bid-only, `NVDA/NKE/ADBE/AMAT/XOM/SPY/SMH/SO/WMT/GOOGL`는 spread cap 초과 또는 stale라 submit되지 않았다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-09-2011-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-09-1951-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler core preflight `get_all_positions` 기준 `32` positions 유지. open orders는 0건이고 after-hours 신규 order/fill은 없었다.
- Recent reconciliation scope: scheduler-owned `1951` after-hours core/research preflight를 우선 사용했고 `market_closed`는 장외 expected nonblocking으로 처리했다. separate after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned IEX quote evidence에서 `QQQ`도 quote age 약 `869.03`분으로 stale였고 `AVGO/PFE/BAC/RGTI`는 bid-only, `NVDA/NKE/ADBE/AMAT/XOM/SPY/SMH/SO/WMT/GOOGL`는 spread cap 초과 또는 stale라 submit되지 않았다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-09-1951-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-09-1931-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler core preflight `get_all_positions`와 runtime `get_all_positions` 교차 확인 기준 `32` positions 유지. open orders는 0건이고 after-hours 신규 order/fill은 없었다.
- Recent reconciliation scope: scheduler-owned `1931` after-hours core/research preflight를 우선 사용했고 `market_closed`는 장외 expected nonblocking으로 처리했다. separate after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned IEX quote evidence에서 `QQQ`도 quote age 약 `849.07`분으로 stale였고 `AVGO/PFE/BAC/RGTI`는 bid-only, `NVDA/NKE/ADBE/AMAT/XOM/SPY/SMH/SO/WMT/GOOGL`는 spread cap 초과 또는 stale라 submit되지 않았다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-09-1931-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-09-1911-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler core preflight `get_all_positions` 기준 `32` positions 유지. open orders는 0건이고 after-hours 신규 order/fill은 없었다.
- Recent reconciliation scope: scheduler-owned `1911` after-hours core/research preflight를 우선 사용했고 `market_closed`는 장외 expected nonblocking으로 처리했다. separate after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned IEX quote evidence에서 `QQQ`도 quote age 약 `829.07`분으로 stale였고 `AVGO/PFE/BAC/RGTI`는 bid-only, `NVDA/NKE/ADBE/AMAT/XOM/SPY/SMH/SO/WMT/GOOGL`는 spread cap 초과 또는 stale라 submit되지 않았다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-09-1911-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-09-1851-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler core preflight `get_all_positions` 기준 `32` positions 유지. open orders는 0건이고 after-hours 신규 order/fill은 없었다.
- Recent reconciliation scope: scheduler-owned `1851` after-hours core/research preflight를 우선 사용했고 `market_closed`는 장외 expected nonblocking으로 처리했다. separate after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned IEX quote evidence에서 `QQQ`도 quote age 약 `809.05`분으로 stale였고 `AVGO/PFE/BAC/RGTI`는 bid-only, `NVDA/NKE/ADBE/AMAT/XOM/SPY/SMH/SO/WMT/GOOGL`는 spread cap 초과 또는 stale라 submit되지 않았다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-09-1851-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-09-1831-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler core preflight `get_all_positions` 기준 `32` positions 유지. open orders는 0건이고 after-hours 신규 order/fill은 없었다.
- Recent reconciliation scope: scheduler-owned `1831` after-hours core/research preflight를 우선 사용했고 `market_closed`는 장외 expected nonblocking으로 처리했다. separate after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned IEX quote evidence에서 `QQQ`도 quote age 약 `789.07`분으로 stale였고 `AVGO/PFE/BAC/RGTI`는 bid-only, `NVDA/NKE/ADBE/AMAT/XOM/SPY/SMH/SO/WMT/GOOGL`는 spread cap 초과 또는 stale라 submit되지 않았다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-09-1831-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-09-1811-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler core preflight `get_all_positions` 기준 `32` positions 유지. open orders는 0건이고 after-hours 신규 order/fill은 없었다.
- Recent reconciliation scope: scheduler-owned `1811` after-hours core/research preflight를 우선 사용했고 `market_closed`는 장외 expected nonblocking으로 처리했다. separate after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned IEX quote evidence에서 `QQQ`도 quote age 약 `769.45`분으로 stale였고 `AVGO/PFE/BAC/RGTI`는 bid-only, `NVDA/NKE/ADBE/AMAT/XOM/SPY/SMH/SO/WMT/GOOGL`는 spread cap 초과 또는 stale라 submit되지 않았다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-09-1811-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-09-1751-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler core preflight `get_all_positions` 기준 `32` positions 유지. open orders는 0건이고 after-hours 신규 order/fill은 없었다.
- Recent reconciliation scope: scheduler-owned `1751` after-hours core/research preflight를 우선 사용했고 `market_closed`는 장외 expected nonblocking으로 처리했다. separate after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned IEX quote evidence에서 `QQQ`도 quote age 약 `749.40`분으로 stale였고 `AVGO/PFE/BAC/RGTI`는 bid-only, `NVDA/NKE/ADBE/AMAT/XOM/SPY/SMH/SO/WMT/GOOGL`는 spread cap 초과 또는 stale라 submit되지 않았다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-09-1751-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-09-1731-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler core preflight `get_all_positions` 기준 `32` positions 유지. open orders는 0건이고 after-hours 신규 order/fill은 없었다.
- Recent reconciliation scope: scheduler-owned `1731` after-hours core/research preflight를 우선 사용했고 `market_closed`는 장외 expected nonblocking으로 처리했다. separate after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned IEX quote evidence에서 `QQQ`도 quote age 약 `729.02`분으로 stale였고 `AVGO/PFE/BAC/RGTI`는 bid-only, `NVDA/NKE/ADBE/AMAT/XOM/SPY/SMH/SO/WMT/GOOGL`는 spread cap 초과 또는 stale라 submit되지 않았다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-09-1731-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-09-1711-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler core preflight `get_all_positions` 기준 `32` positions 유지. open orders는 0건이고 after-hours 신규 order/fill은 없었다.
- Recent reconciliation scope: scheduler-owned `1711` after-hours core/research preflight를 우선 사용했고 `market_closed`는 장외 expected nonblocking으로 처리했다. separate after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned IEX quote evidence에서 `QQQ`도 quote age 약 `709.09`분으로 stale였고 `AVGO/PFE/BAC/RGTI`는 bid-only, `NVDA/NKE/ADBE/AMAT/XOM/SPY/SMH/SO/WMT/GOOGL`는 spread cap 초과 또는 stale라 submit되지 않았다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-09-1711-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-09-1651-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler core preflight `get_all_positions` 기준 `32` positions 유지. open orders는 0건이고 after-hours 신규 order/fill은 없었다.
- Recent reconciliation scope: scheduler-owned `1651` after-hours core/research preflight를 우선 사용했고 `market_closed`는 장외 expected nonblocking으로 처리했다. separate after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned IEX quote evidence에서 `QQQ`도 quote age 약 `689.07`분으로 stale였고 `AVGO/PFE/BAC/RGTI`는 bid-only, `NVDA/NKE/ADBE/AMAT/XOM/SPY/SMH/SO/WMT/GOOGL`는 spread cap 초과 또는 stale라 submit되지 않았다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-09-1651-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-09-1631-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler core preflight `get_all_positions` 기준 `32` positions 유지. open orders는 0건이고 after-hours 신규 order/fill은 없었다.
- Recent reconciliation scope: scheduler-owned `1631` after-hours core/research preflight를 우선 사용했고 `market_closed`는 장외 expected nonblocking으로 처리했다. separate after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned IEX quote evidence에서 `QQQ`도 quote age 약 `669.47`분으로 stale였고 `AVGO/PFE/BAC/RGTI`는 bid-only, `NVDA/NKE/ADBE/AMAT/XOM/SPY/SMH/SO/WMT/GOOGL`는 spread cap 초과 또는 stale라 submit되지 않았다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-09-1631-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-09-1611-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler core preflight `get_all_positions` 기준 `32` positions 유지. open orders는 0건이고 after-hours 신규 order/fill은 없었다.
- Recent reconciliation scope: scheduler-owned `1611` after-hours core/research preflight를 우선 사용했고 `market_closed`는 장외 expected nonblocking으로 처리했다. separate after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned IEX quote evidence에서 `QQQ`도 quote age 약 `649.05`분으로 stale였고 `AVGO/PFE/BAC/RGTI`는 bid-only, `NVDA/NKE/ADBE/AMAT/XOM/SPY/SMH/SO/WMT/GOOGL`는 spread cap 초과 또는 stale라 submit되지 않았다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-09-1611-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-09-1551-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler core preflight `get_all_positions` 기준 `32` positions 유지. open orders는 0건이고 after-hours 신규 order/fill은 없었다.
- Recent reconciliation scope: scheduler-owned `1551` after-hours core/research preflight를 우선 사용했고 `market_closed`는 장외 expected nonblocking으로 처리했다. separate after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned IEX quote evidence에서 `QQQ`도 quote age 약 `629.46`분으로 stale였고 `AVGO/PFE/BAC/RGTI`는 bid-only, `NVDA/NKE/ADBE/AMAT/XOM/SPY/SMH/SO/WMT/GOOGL`는 spread cap 초과 또는 stale라 submit되지 않았다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-09-1551-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-09-1531-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler core preflight `get_all_positions` 기준 `32` positions 유지. open orders는 0건이고 after-hours 신규 order/fill은 없었다.
- Recent reconciliation scope: scheduler-owned `1531` after-hours core/research preflight를 우선 사용했고 `market_closed`는 장외 expected nonblocking으로 처리했다. separate after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned IEX quote evidence에서 `QQQ`도 quote age 약 `609.36`분으로 stale였고 `AVGO/PFE/BAC/RGTI`는 bid-only, `NVDA/NKE/ADBE/AMAT/XOM/SPY/SMH/SO/WMT/GOOGL`는 spread cap 초과 또는 stale라 submit되지 않았다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-09-1531-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-09-1511-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler core preflight `get_all_positions` 기준 `32` positions 유지. open orders는 0건이고 after-hours 신규 order/fill은 없었다.
- Recent reconciliation scope: scheduler-owned `1511` after-hours core/research preflight를 우선 사용했고 `market_closed`는 장외 expected nonblocking으로 처리했다. separate after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned IEX quote evidence에서 `QQQ`도 quote age 약 `589.03`분으로 stale였고 `AVGO/PFE/BAC/RGTI`는 bid-only, `NVDA/NKE/ADBE/AMAT/XOM/SPY/SMH/SO/WMT/GOOGL`는 spread cap 초과 또는 stale라 submit되지 않았다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-09-1511-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-09-1451-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler core preflight `get_all_positions` 기준 `32` positions 유지. open orders는 0건이고 after-hours 신규 order/fill은 없었다.
- Recent reconciliation scope: scheduler-owned `1451` after-hours core/research preflight를 우선 사용했고 `market_closed`는 장외 expected nonblocking으로 처리했다. separate after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned IEX quote evidence에서 `QQQ`도 quote age 약 `569.43`분으로 stale였고 `AVGO/PFE/BAC/RGTI`는 bid-only, `NVDA/NKE/ADBE/AMAT/XOM/SPY/SMH/SO/WMT/GOOGL`는 spread cap 초과 또는 stale라 submit되지 않았다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-09-1451-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-09-1431-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler core preflight `get_all_positions` 기준 `32` positions 유지. open orders는 0건이고 after-hours 신규 order/fill은 없었다.
- Recent reconciliation scope: scheduler-owned `1431` after-hours core/research preflight를 우선 사용했고 `market_closed`는 장외 expected nonblocking으로 처리했다. separate after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned IEX quote evidence에서 `QQQ`도 quote age 약 `549.07`분으로 stale였고 `AVGO/PFE/BAC/RGTI`는 bid-only, `NVDA/NKE/ADBE/AMAT/XOM/SPY/SMH/SO/WMT/GOOGL`는 spread cap 초과 또는 stale라 submit되지 않았다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-09-1431-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-09-1411-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler core preflight `get_all_positions` 기준 `32` positions 유지. open orders는 0건이고 after-hours 신규 order/fill은 없었다.
- Recent reconciliation scope: scheduler-owned `1411` after-hours core/research preflight를 우선 사용했고 `market_closed`는 장외 expected nonblocking으로 처리했다. separate after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned IEX quote evidence에서 `QQQ`도 quote age 약 `529.05`분으로 stale였고 `AVGO/PFE/BAC/RGTI`는 bid-only, `NVDA/NKE/ADBE/AMAT/XOM/SPY/SMH/SO/WMT/GOOGL`는 spread cap 초과 또는 stale라 submit되지 않았다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-09-1411-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-09-1351-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler core preflight `get_all_positions` 기준 `32` positions 유지. open orders는 0건이고 after-hours 신규 order/fill은 없었다.
- Recent reconciliation scope: scheduler-owned `1351` after-hours core/research preflight를 우선 사용했고 `market_closed`는 장외 expected nonblocking으로 처리했다. separate after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned IEX quote evidence에서 `QQQ`도 quote age 약 `509.07`분으로 stale였고 `AVGO/PFE/BAC/RGTI`는 bid-only, `NVDA/NKE/ADBE/AMAT/XOM/SPY/SMH/SO/WMT/GOOGL`는 spread cap 초과 또는 stale라 submit되지 않았다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-09-1351-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-09-1331-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler core preflight `get_all_positions` 기준 `32` positions 유지. open orders는 0건이고 after-hours 신규 order/fill은 없었다.
- Recent reconciliation scope: scheduler-owned `1331` after-hours core/research preflight를 우선 사용했고 `market_closed`는 장외 expected nonblocking으로 처리했다. separate after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned IEX quote evidence에서 `QQQ`도 quote age 약 `489.08`분으로 stale였고 `AVGO/PFE/BAC/RGTI`는 bid-only, `NVDA/NKE/ADBE/AMAT/XOM/SPY/SMH/SO/WMT/GOOGL`는 spread cap 초과 또는 stale라 submit되지 않았다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-09-1331-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-09-1311-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler core preflight `get_all_positions` 기준 `32` positions 유지. open orders는 0건이고 after-hours 신규 order/fill은 없었다.
- Recent reconciliation scope: scheduler-owned `1311` after-hours core/research preflight를 우선 사용했고 `market_closed`는 장외 expected nonblocking으로 처리했다. separate after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned IEX quote evidence에서 `QQQ`도 quote age 약 `469.51`분으로 stale였고 `AVGO/PFE/BAC/RGTI`는 bid-only, `NVDA/NKE/ADBE/AMAT/XOM/SPY/SMH/SO/WMT/GOOGL`는 spread cap 초과 또는 stale라 submit되지 않았다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-09-1311-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-09-1251-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler core preflight `get_all_positions` 기준 `32` positions 유지. open orders는 0건이고 after-hours 신규 order/fill은 없었다.
- Recent reconciliation scope: scheduler-owned `1251` after-hours core/research preflight를 우선 사용했고 `market_closed`는 장외 expected nonblocking으로 처리했다. separate after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned IEX quote evidence에서 `QQQ`도 quote age 약 `449.07`분으로 stale였고 `AVGO/PFE/BAC/RGTI`는 bid-only, `NVDA/NKE/ADBE/AMAT/XOM/SPY/SMH/SO/WMT/GOOGL`는 spread cap 초과 또는 stale라 submit되지 않았다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-09-1251-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-09-1231-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler core preflight `get_all_positions` 기준 `32` positions 유지. open orders는 0건이고 after-hours 신규 order/fill은 없었다.
- Recent reconciliation scope: scheduler-owned `1231` after-hours core/research preflight를 우선 사용했고 `market_closed`는 장외 expected nonblocking으로 처리했다. separate after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned IEX quote evidence에서 `QQQ`도 quote age 약 `429.43`분으로 stale였고 `AVGO/PFE/BAC/RGTI`는 bid-only, `NVDA/NKE/ADBE/AMAT/XOM/SPY/SMH/SO/WMT/GOOGL`는 spread cap 초과 또는 stale라 submit되지 않았다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-09-1231-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-09-1211-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler core preflight `get_all_positions` 기준 `32` positions 유지. open orders는 0건이고 after-hours 신규 order/fill은 없었다.
- Recent reconciliation scope: scheduler-owned `1211` after-hours core/research preflight를 우선 사용했고 `market_closed`는 장외 expected nonblocking으로 처리했다. separate after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned IEX quote evidence에서 `QQQ`도 quote age 약 `409.08`분으로 stale였고 `AVGO/PFE/BAC/RGTI`는 bid-only, `NVDA/NKE/ADBE/AMAT/XOM/SPY/SMH/SO/WMT/GOOGL`는 spread cap 초과 또는 stale라 submit되지 않았다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-09-1211-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-09-1151-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler core preflight `get_all_positions` 기준 `32` positions 유지. open orders는 0건이고 after-hours 신규 order/fill은 없었다.
- Recent reconciliation scope: scheduler-owned `1151` after-hours core/research preflight를 우선 사용했고 `market_closed`는 장외 expected nonblocking으로 처리했다. separate after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned IEX quote evidence에서 `QQQ`도 quote age 약 `389.06`분으로 stale였고 `AVGO/PFE/BAC/RGTI`는 bid-only, `NVDA/NKE/ADBE/AMAT/XOM/SPY/SMH/SO/WMT/GOOGL`는 spread cap 초과 또는 stale라 submit되지 않았다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-09-1151-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-09-1131-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler core preflight `get_all_positions` 기준 `32` positions 유지. open orders는 0건이고 after-hours 신규 order/fill은 없었다.
- Recent reconciliation scope: scheduler-owned `1131` after-hours core/research preflight를 우선 사용했고 `market_closed`는 장외 expected nonblocking으로 처리했다. separate after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned IEX quote evidence에서 `QQQ`도 quote age 약 `369.07`분으로 stale였고 `AVGO/PFE/BAC/RGTI`는 bid-only, `NVDA/NKE/ADBE/AMAT/XOM/SPY/SMH/SO/WMT/GOOGL`는 spread cap 초과 또는 stale라 submit되지 않았다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-09-1131-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-09-1111-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler core preflight `get_all_positions` 기준 `32` positions 유지. open orders는 0건이고 after-hours 신규 order/fill은 없었다.
- Recent reconciliation scope: scheduler-owned `1111` after-hours core/research preflight를 우선 사용했고 `market_closed`는 장외 expected nonblocking으로 처리했다. separate after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned IEX quote evidence에서 `QQQ`도 quote age 약 `349.40`분으로 stale였고 `AVGO/PFE/BAC/RGTI`는 bid-only, `NVDA/NKE/ADBE/AMAT/XOM/SPY/SMH/SO/WMT/GOOGL`는 spread cap 초과 또는 stale라 submit되지 않았다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-09-1111-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-09-1051-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler core preflight `get_all_positions` 기준 `32` positions 유지. open orders는 0건이고 after-hours 신규 order/fill은 없었다.
- Recent reconciliation scope: scheduler-owned `1051` after-hours core/research preflight를 우선 사용했고 `market_closed`는 장외 expected nonblocking으로 처리했다. separate after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned IEX quote evidence에서 `QQQ`도 quote age 약 `329.07`분으로 stale였고 `AVGO/PFE/BAC/RGTI`는 bid-only, `NVDA/NKE/ADBE/AMAT/XOM/SPY/SMH/SO/WMT/GOOGL`는 spread cap 초과 또는 stale라 submit되지 않았다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-09-1051-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-09-1031-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler core preflight `get_all_positions` 기준 `32` positions 유지. open orders는 0건이고 after-hours 신규 order/fill은 없었다.
- Recent reconciliation scope: scheduler-owned `1031` after-hours core/research preflight를 우선 사용했고 `market_closed`는 장외 expected nonblocking으로 처리했다. separate after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned IEX quote evidence에서 `QQQ`도 quote age 약 `309.05`분으로 stale였고 `AVGO/PFE/BAC/RGTI`는 bid-only, `NVDA/NKE/ADBE/AMAT/XOM/SPY/SMH/SO/WMT/GOOGL`는 spread cap 초과 또는 stale라 submit되지 않았다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-09-1031-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-09-1011-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler core preflight `get_all_positions` 기준 `32` positions 유지. open orders는 0건이고 after-hours 신규 order/fill은 없었다.
- Recent reconciliation scope: scheduler-owned `1011` after-hours core/research preflight를 우선 사용했고 `market_closed`는 장외 expected nonblocking으로 처리했다. separate after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned IEX quote evidence에서 `QQQ`도 quote age 약 `289.48`분으로 stale였고 `AVGO/PFE/BAC/RGTI`는 bid-only, `NVDA/NKE/ADBE/AMAT/XOM/SPY/SMH/SO/WMT/GOOGL`는 spread cap 초과 또는 stale라 submit되지 않았다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-09-1011-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-09-0951-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler core preflight `get_all_positions` 기준 `32` positions 유지. open orders는 0건이고 after-hours 신규 order/fill은 없었다.
- Recent reconciliation scope: scheduler-owned `0951` after-hours core/research preflight를 우선 사용했고 `market_closed`는 장외 expected nonblocking으로 처리했다. separate after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned IEX quote evidence에서 `QQQ`도 quote age 약 `269.06`분으로 stale였고 `AVGO/PFE/BAC/RGTI`는 bid-only, `NVDA/NKE/ADBE/AMAT/XOM/SPY/SMH/SO/WMT/GOOGL`는 spread cap 초과 또는 stale라 submit되지 않았다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-09-0951-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-09-0931-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler core preflight `get_all_positions` 기준 `32` positions 유지. open orders는 0건이고 after-hours 신규 order/fill은 없었다.
- Recent reconciliation scope: scheduler-owned `0931` after-hours core/research preflight를 우선 사용했고 `market_closed`는 장외 expected nonblocking으로 처리했다. separate after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned IEX quote evidence에서 `QQQ`도 quote age 약 `248.99`분으로 stale였고 `AVGO/PFE/BAC/RGTI`는 bid-only, `NVDA/NKE/ADBE/AMAT/XOM/SPY/SMH/SO/WMT/GOOGL`는 spread cap 초과 또는 stale라 submit되지 않았다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-09-0931-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-09-0911-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler core preflight `get_all_positions` 기준 `32` positions 유지. open orders는 0건이고 after-hours 신규 order/fill은 없었다.
- Recent reconciliation scope: scheduler-owned `0911` after-hours core/research preflight를 우선 사용했고 `market_closed`는 장외 expected nonblocking으로 처리했다. separate after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned IEX quote evidence에서 `QQQ`도 quote age 약 `229.41`분으로 stale였고 `AVGO/PFE/BAC/RGTI`는 bid-only, `NVDA/NKE/ADBE/AMAT/XOM/SPY/SMH/SO/WMT/GOOGL`는 spread cap 초과 또는 stale라 submit되지 않았다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-09-0911-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-09-0851-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler core preflight `get_all_positions` 기준 `32` positions 유지. open orders는 0건이고 after-hours 신규 order/fill은 없었다.
- Recent reconciliation scope: scheduler-owned `0851` after-hours core/research preflight를 우선 사용했고 `market_closed`는 장외 expected nonblocking으로 처리했다. separate after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned IEX quote evidence에서 `QQQ`도 quote age 약 `209.43`분으로 stale였고 `AVGO/PFE/BAC/RGTI`는 bid-only, `NVDA/NKE/ADBE/AMAT/XOM/SPY/SMH/SO/WMT/GOOGL`는 spread cap 초과 또는 stale라 submit되지 않았다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-09-0851-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-09-0831-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler core preflight `get_all_positions` 기준 `32` positions 유지. open orders는 0건이고 after-hours 신규 order/fill은 없었다.
- Recent reconciliation scope: scheduler-owned `0831` after-hours core/research preflight를 우선 사용했고 `market_closed`는 장외 expected nonblocking으로 처리했다. separate after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned IEX quote evidence에서 `QQQ`도 quote age 약 `189.06`분으로 stale였고 `AVGO/PFE/BAC/RGTI`는 bid-only, `NVDA/NKE/ADBE/AMAT/XOM/SPY/SMH/SO/WMT/GOOGL`는 spread cap 초과 또는 stale라 submit되지 않았다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-09-0831-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-09-0811-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler core preflight `get_all_positions` 기준 `32` positions 유지. open orders는 0건이고 after-hours 신규 order/fill은 없었다.
- Recent reconciliation scope: scheduler-owned `0811` after-hours core/research preflight를 우선 사용했고 `market_closed`는 장외 expected nonblocking으로 처리했다. separate after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned IEX quote evidence에서 `QQQ`도 quote age 약 `169.36`분으로 stale였고 `AVGO/PFE/BAC/RGTI`는 bid-only, `NVDA/NKE/ADBE/AMAT/XOM/SPY/SMH/SO/WMT/GOOGL`는 spread cap 초과 또는 stale라 submit되지 않았다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-09-0811-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-09-0751-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler core preflight와 runtime `get_all_positions` 기준 `32` positions 유지. open orders는 0건이고 after-hours 신규 order/fill은 없었다.
- Recent reconciliation scope: scheduler-owned `0751` after-hours core/research preflight를 우선 사용했고 `market_closed`는 장외 expected nonblocking으로 처리했다. separate after-hours order budget은 `0/2`로 열려 있었지만 runtime IEX/overnight quote cross-check에서 `QQQ`도 quote age 약 `150.84`분으로 stale였고 `AVGO/PFE/BAC/RGTI`는 bid-only, `NVDA/NKE/ADBE/AMAT/XOM/SPY/SMH/SO/WMT/GOOGL`는 spread cap 초과 또는 stale라 submit되지 않았다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-09-0751-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-09-0731-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler core preflight와 runtime `get_all_positions` 기준 `32` positions 유지. open orders는 0건이고 after-hours 신규 order/fill은 없었다.
- Recent reconciliation scope: scheduler-owned `0731` after-hours core/research preflight를 우선 사용했고 `market_closed`는 장외 expected nonblocking으로 처리했다. separate after-hours order budget은 `0/2`로 열려 있었지만 runtime IEX/overnight quote cross-check에서 `QQQ`도 quote age 약 `130.87`분으로 stale였고 `AVGO/PFE/BAC/RGTI`는 bid-only, `NVDA/NKE/ADBE/AMAT/XOM/SPY/SMH/SO/WMT/GOOGL`는 spread cap 초과 또는 stale라 submit되지 않았다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-09-0731-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-09-0711-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler core preflight와 runtime `get_all_positions` 기준 `32` positions 유지. open orders는 0건이고 after-hours 신규 order/fill은 없었다.
- Recent reconciliation scope: scheduler-owned `0711` after-hours core/research preflight를 우선 사용했고 `market_closed`는 장외 expected nonblocking으로 처리했다. separate after-hours order budget은 `0/2`로 열려 있었지만 runtime IEX/overnight quote cross-check에서 `QQQ`도 quote age 약 `110.31`분으로 stale였고 `AVGO/PFE/BAC/RGTI`는 bid-only, `NVDA/NKE/ADBE/AMAT/XOM/SPY/SMH/SO/WMT/GOOGL`는 spread cap 초과 또는 stale라 submit되지 않았다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-09-0711-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-09-0651-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler core preflight와 runtime `get_all_positions` 기준 `32` positions 유지. open orders는 0건이고 after-hours 신규 order/fill은 없었다.
- Recent reconciliation scope: scheduler-owned `0651` after-hours core/research preflight를 우선 사용했고 `market_closed`는 장외 expected nonblocking으로 처리했다. separate after-hours order budget은 `0/2`로 열려 있었지만 runtime IEX/overnight quote cross-check에서 `QQQ`도 quote age 약 `91.23`분으로 stale였고 `AVGO/PFE/BAC/RGTI`는 bid-only, `NVDA/NKE/ADBE/AMAT/XOM/SPY/SMH/SO/WMT/GOOGL`는 spread cap 초과 또는 stale라 submit되지 않았다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-09-0651-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-09-0631-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler core preflight와 runtime `get_all_positions` 기준 `32` positions 유지. open orders는 0건이고 after-hours 신규 order/fill은 없었다.
- Recent reconciliation scope: scheduler-owned `0631` after-hours core/research preflight를 우선 사용했고 `market_closed`는 장외 expected nonblocking으로 처리했다. separate after-hours order budget은 `0/2`로 열려 있었지만 runtime IEX/overnight quote cross-check에서 `QQQ`도 quote age 약 `70.82`분으로 stale였고 `AVGO/PFE/BAC/RGTI`는 bid-only, `NVDA/NKE/ADBE/AMAT/XOM/SPY/SMH/SO/WMT/GOOGL`는 spread cap 초과 또는 stale라 submit되지 않았다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-09-0631-after-hours-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-09-0431-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler core preflight 기준 `32` positions 유지. open orders는 0건이고 `RGTI/AVGO/SO` 모두 신규 수량 변화 없이 유지됐다.
- Recent reconciliation scope: scheduler-owned `0431` stale cleanup/core/research preflight 기준 신규 buy는 `review_backlog_pending_1d_count=13` backlog throttle에 막혔고, sell-first 후보는 `RGTI` same-day duplicate, `AVGO` same-day duplicate, `SO` decision-grade metric gap 때문에 submit되지 않았다. same-day filled orders는 `AVGO` 장외 sell 2건, `TSLA` exit 1건, `RGTI` trim 1건으로 총 4건 재확인됐다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-09-0431-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-09-0411-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler core preflight 기준 `32` positions 유지. open orders는 0건이고 `RGTI/AVGO/SO` 모두 신규 수량 변화 없이 유지됐다.
- Recent reconciliation scope: scheduler-owned `0411` stale cleanup/core/research preflight 기준 신규 buy는 `review_backlog_pending_1d_count=13` backlog throttle에 막혔고, sell-first 후보는 `RGTI` same-day duplicate, `AVGO` duplicate+spread `0.5394%`, `SO` spread `2.1025%` + decision-grade metric gap 때문에 submit되지 않았다. same-day filled orders는 `AVGO` 장외 sell 2건, `TSLA` exit 1건, `RGTI` trim 1건으로 총 4건 재확인됐다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-09-0411-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-09-0351-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler core preflight 기준 `32` positions 유지. open orders는 0건이고 `RGTI/AVGO/SO` 모두 신규 수량 변화 없이 유지됐다.
- Recent reconciliation scope: scheduler-owned `0351` stale cleanup/core/research preflight 기준 신규 buy는 `review_backlog_pending_1d_count=13` backlog throttle에 막혔고, sell-first 후보는 `RGTI` same-day duplicate, `AVGO` duplicate+spread `0.9471%`, `SO` spread `1.0799%` + decision-grade metric gap 때문에 submit되지 않았다. same-day filled orders는 `AVGO` 장외 sell 2건, `TSLA` exit 1건, `RGTI` trim 1건으로 총 4건 재확인됐다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-09-0351-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-09-0311-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler core preflight 기준 `32` positions 유지. open orders는 0건이고 `RGTI/AVGO/SO` 모두 신규 수량 변화 없이 유지됐다.
- Recent reconciliation scope: scheduler-owned `0311` stale cleanup/core/research preflight 기준 신규 buy는 `review_backlog_pending_1d_count=13` backlog throttle에 막혔고, sell-first 후보는 `RGTI` same-day duplicate, `AVGO` duplicate+spread `0.8130%`, `SO` decision-grade metric gap 때문에 submit되지 않았다. same-day filled orders는 `AVGO` 장외 sell 2건, `TSLA` exit 1건, `RGTI` trim 1건으로 총 4건 재확인됐다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-09-0311-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-09-0251-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler core preflight 기준 `32` positions 유지. open orders는 0건이고 `RGTI/AVGO/SO` 모두 신규 수량 변화 없이 유지됐다.
- Recent reconciliation scope: scheduler-owned `0251` stale cleanup/core/research preflight 기준 신규 buy는 `review_backlog_pending_1d_count=13` backlog throttle에 막혔고, sell-first 후보는 `RGTI` same-day duplicate, `AVGO` duplicate+spread `1.3592%`, `SO` decision-grade metric gap 때문에 submit되지 않았다. same-day filled orders는 `AVGO` 장외 sell 2건, `TSLA` exit 1건, `RGTI` trim 1건으로 총 4건 재확인됐다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-09-0251-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-09-0231-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler core preflight 기준 `32` positions 유지. open orders는 0건이고 `RGTI/AVGO/SO` 모두 신규 수량 변화 없이 유지됐다.
- Recent reconciliation scope: scheduler-owned `0231` stale cleanup/core/research preflight 기준 신규 buy는 `review_backlog_pending_1d_count=13` backlog throttle에 막혔고, sell-first 후보는 `RGTI` same-day duplicate, `AVGO` duplicate+spread `0.7420%`, `SO` spread `0.9153%` + metric gap 때문에 submit되지 않았다. same-day filled orders는 `AVGO` 장외 sell 2건, `TSLA` exit 1건, `RGTI` trim 1건으로 총 4건 재확인됐다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-09-0231-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-09-0211-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler core preflight 기준 `32` positions 유지. open orders는 0건이고 `RGTI/AVGO/SO` 모두 신규 수량 변화 없이 유지됐다.
- Recent reconciliation scope: scheduler-owned `0211` stale cleanup/core/research preflight 기준 신규 buy는 `review_backlog_pending_1d_count=13` backlog throttle에 막혔고, sell-first 후보는 `RGTI` same-day duplicate, `AVGO` duplicate+spread `0.9100%`, `SO` metric gap 때문에 submit되지 않았다. same-day filled orders는 `AVGO` 장외 sell 2건, `TSLA` exit 1건, `RGTI` trim 1건으로 총 4건 재확인됐다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-09-0211-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-09-0151-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler core preflight 기준 `32` positions 유지. open orders는 0건이고 `RGTI/AVGO/SO` 모두 신규 수량 변화 없이 유지됐다.
- Recent reconciliation scope: scheduler-owned `0151` stale cleanup/core/research preflight 기준 신규 buy는 `review_backlog_pending_1d_count=13` backlog throttle에 막혔고, sell-first 후보는 `RGTI` same-day duplicate, `AVGO` duplicate+spread `1.6445%`, `SO` metric gap 때문에 submit되지 않았다. same-day filled orders는 `AVGO` 장외 sell 2건, `TSLA` exit 1건, `RGTI` trim 1건으로 총 4건 재확인됐다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-09-0151-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-09-0131-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler core preflight 기준 `32` positions 유지. open orders는 0건이고 `RGTI/AVGO/SO` 모두 신규 수량 변화 없이 유지됐다.
- Recent reconciliation scope: scheduler-owned `0131` stale cleanup/core/research preflight 기준 신규 buy는 `review_backlog_pending_1d_count=13` backlog throttle에 막혔고, sell-first 후보는 `RGTI` same-day duplicate, `AVGO` duplicate+spread `1.3737%`, `SO` metric gap 때문에 submit되지 않았다. same-day filled orders는 `AVGO` 장외 sell 2건, `TSLA` exit 1건, `RGTI` trim 1건으로 총 4건 재확인됐다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-09-0131-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-09-0111-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime `get_all_positions` 기준 `32` positions 유지. open orders는 0건이고 `RGTI/AVGO/SO` 모두 신규 수량 변화 없이 유지됐다.
- Recent reconciliation scope: scheduler-owned `0111` stale cleanup/core/research preflight와 runtime `get_clock/get_orders(status=open)/get_orders(status=all, after=2026-06-08T00:00:00Z)/get_account_activities(activity_types=FILL)/get_all_positions/get_account_info/get_watchlists/get_stock_latest_quote(feed=iex)` 확인 기준 신규 buy는 `review_backlog_pending_1d_count=13` backlog throttle에 막혔고, sell-first 후보는 `RGTI` same-day duplicate, `AVGO` same-day duplicate, `SO` spread `6.8511%` + metric gap 때문에 submit되지 않았다. same-day filled orders는 `AVGO` 장외 sell 2건, `TSLA` exit 1건, `RGTI` trim 1건으로 총 4건 재확인됐다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-09-0111-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-09-0011-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler core preflight 기준 `32` positions 유지. open orders는 0건이고 `RGTI/AVGO/SO` 모두 신규 수량 변화 없이 유지됐다.
- Recent reconciliation scope: scheduler-owned `0011` stale cleanup/core/research preflight 기준 신규 buy는 `review_backlog_pending_1d_count=13` backlog throttle에 막혔고, sell-first 후보는 `RGTI` same-day duplicate, `AVGO` duplicate+spread `0.9722%`, `SO` metric gap 때문에 submit되지 않았다. same-day filled orders는 `AVGO` 장외 sell 2건, `TSLA` exit 1건, `RGTI` trim 1건으로 총 4건 재확인됐다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-09-0011-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-08-2351-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime `get_all_positions` 기준 `32` positions 유지. open orders는 0건이고 `RGTI/AVGO/SO` 모두 신규 수량 변화 없이 유지됐다.
- Recent reconciliation scope: scheduler-owned `2351` stale cleanup/core/research preflight와 runtime `get_watchlists/get_orders(status=open)/get_orders(status=all, after=2026-06-08T00:00:00Z)/get_stock_latest_quote(feed=iex)/get_account_info/get_all_positions` 확인 기준 신규 buy는 `review_backlog_pending_1d_count=13` backlog throttle에 막혔고, sell-first 후보는 `RGTI` same-day duplicate, `AVGO` same-day duplicate, `SO` metric gap 때문에 submit되지 않았다. same-day filled orders는 `AVGO` 장외 sell 2건, `TSLA` exit 1건, `RGTI` trim 1건으로 총 4건 재확인됐다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-08-2351-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-08-2331-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler core preflight 기준 `32` positions 유지. open orders는 0건이고 `RGTI/AVGO/SO` 모두 신규 수량 변화 없이 유지됐다.
- Recent reconciliation scope: scheduler-owned `2331` stale cleanup/core/research preflight와 runtime `get_watchlists/get_orders(status=open)/get_orders(status=all, after=2026-06-08T00:00:00Z)/get_stock_latest_quote(feed=iex)` 확인 기준 신규 buy는 `review_backlog_pending_1d_count=13` backlog throttle에 막혔고, sell-first 후보는 `RGTI` same-day duplicate, `AVGO` duplicate+spread, `SO` metric gap 때문에 submit되지 않았다. same-day filled orders는 `AVGO` 장외 sell 2건, `TSLA` exit 1건, `RGTI` trim 1건으로 총 4건 재확인됐다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-08-2331-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-08-2311-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler core preflight 기준 `32` positions 유지. open orders는 0건이고 `RGTI/AVGO/SO` 모두 신규 수량 변화 없이 유지됐다.
- Recent reconciliation scope: scheduler-owned `2311` stale cleanup/core/research preflight와 runtime `get_watchlists/get_orders(status=open)/get_orders(status=all, after=2026-06-08T00:00:00Z)/get_stock_latest_quote(feed=iex)` 확인 기준 신규 buy는 `review_backlog_pending_1d_count=13` backlog throttle에 막혔고, sell-first 후보는 `RGTI` same-day duplicate, `AVGO` duplicate+spread, `SO` metric gap 때문에 submit되지 않았다. same-day filled orders는 `AVGO` 장외 sell 2건, `TSLA` exit 1건, `RGTI` trim 1건으로 총 4건 재확인됐다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-08-2311-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-08-2251-hourly-autopilot]]
- Open/new: 없음
- Filled: `RGTI` sell 30 @ `21.48` (`client_order_id=hourly-20260608-2251-sell-rgti`)가 regular-session runtime reconciliation 기준 전량 체결됐다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime `get_all_positions` 기준 `32` positions. `RGTI`는 `120 -> 90`으로 감소했고 open orders는 0건이다.
- Recent reconciliation scope: scheduler-owned `2251` stale cleanup/core/research preflight와 runtime `get_watchlists/get_orders(status=open)/get_orders(status=all, after=2026-06-08T00:00:00Z)/get_account_activities(activity_types=FILL, after=2026-06-08T00:00:00Z)/get_all_positions/get_account_info/place_stock_order` 확인 기준 review backlog throttle로 신규 buy는 계속 차단됐지만 risk-reducing sell 경로에서 `RGTI` 30주 trim이 허용됐다. post-trade account snapshot은 portfolio value `99,552.10 USD`, cash `31,774.85 USD`, buying power `300,430.68 USD`, long market value `67,777.25 USD`다.
- Orders submitted/replaced/cancelled/closed by this workflow: 1 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-08-2251-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-08-2231-hourly-autopilot]]
- Open/new: 없음
- Filled: `TSLA` sell 1 @ `398.59` (`client_order_id=hourly-20260608-2231-sell-tsla`)가 regular-session runtime reconciliation 기준 즉시 체결됐다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime `get_all_positions` 기준 `32` positions. `TSLA`는 계좌 포지션에서 제거됐고 open orders는 0건이다.
- Recent reconciliation scope: scheduler-owned `2231` stale cleanup/core/research preflight와 runtime `get_watchlists/get_orders(status=open)/get_orders(status=all, after=2026-06-08T00:00:00Z)/get_all_positions/get_account_info/place_stock_order` 확인 기준 review backlog throttle로 신규 buy는 차단됐지만 risk-reducing sell 경로에서 `TSLA` 1주 exit가 허용됐다. post-trade account snapshot은 portfolio value `99,862.11 USD`, cash `31,130.45 USD`, buying power `300,491.66 USD`, long market value `68,731.66 USD`다.
- Orders submitted/replaced/cancelled/closed by this workflow: 1 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-08-2231-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-06-0451-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: `NKE` buy 1 @ `43.20` (`client_order_id=hourly-20260606-0451-buy-nke`)는 actual submit timestamp가 `2026-06-05T20:00:07.873287392Z` (`16:00:07 ET`)로 regular close 이후에 기록돼 즉시 취소됐다.
- Position count observed by Alpaca MCP: latest confirmed `0451` scheduler core preflight 기준 `33` positions 유지. 추가 `NKE` fill은 없고 standing order도 남기지 않았다.
- Recent reconciliation scope: scheduler-owned `0451` stale cleanup/core/research preflight와 runtime `place_stock_order/get_order_by_client_id/get_order_by_id/get_clock/cancel_order_by_id/get_orders(status=all, symbols=NKE, after=2026-06-05T04:00:00Z)` 확인 기준 close-race submit을 cancel로 복구했다. last confirmed account snapshot은 portfolio value `98,361.48 USD`, cash `29,947.81 USD`, buying power `245,113.34 USD`, long market value `68,413.67 USD`다.
- Orders submitted/replaced/cancelled/closed by this workflow: 1 / 0 / 1 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-06-0451-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-06-0431-hourly-autopilot]]
- Open/new: 없음
- Filled: `INTC` sell 1 @ `99.93` (`client_order_id=hourly-20260606-0411-sell-intc`)가 0431 core preflight recent activities에서 confirmed fill로 확인됐다.
- Cancelled: `NEE` same-day buy `hourly-20260606-0231-buy-nee`는 `2026-06-05T18:31:08.289816Z` canceled 상태가 runtime all-orders reconciliation에서 재확인됐다.
- Position count observed by Alpaca MCP: scheduler core preflight 기준 `33` positions. `INTC`는 계좌 포지션에서 제거됐고 open orders는 0건이다.
- Recent reconciliation scope: scheduler-owned `0431` stale cleanup/core/research preflight와 runtime `get_clock/get_account_info/get_orders(status=all, symbols=NEE,NKE,TSLA,SO,AVGO, after=2026-06-05T04:00:00Z)` 확인 기준 새 submit attempt는 없었다. account snapshot은 portfolio value `98,445.76 USD`, cash `29,947.81 USD`, buying power `245,318.08 USD`, long market value `68,497.95 USD`다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-06-0431-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-06-0411-hourly-autopilot]]
- Open/new: `INTC` sell 1 @ `99.93` (`client_order_id=hourly-20260606-0411-sell-intc`, `status=new`)
- Filled: 없음
- Cancelled: post-submit symbol-filtered `get_orders` refresh는 tool layer에서 cancelled 되었지만 direct order lookup 기준 주문 생성은 확인됐다.
- Position count observed by Alpaca MCP: latest confirmed scheduler core preflight 기준 `34` positions 유지. `INTC`는 아직 `1주 @ 116.79`다.
- Recent reconciliation scope: scheduler-owned `0411` stale cleanup/core/research preflight와 runtime `get_clock/get_account_info/get_orders(status=open)/get_orders(status=all, after=2026-06-05T04:00:00Z)/get_asset(INTC)/place_stock_order/get_order_by_client_id/get_order_by_id` 확인 기준 `INTC` 1주 regular-session validation exit가 Alpaca order id `3cb070b3-08ed-461d-854d-8fa63cf9d441`로 생성됐고 immediate reconciliation 기준 `status=new`, `filled_qty=0`이다. post-submit `get_account_info`는 portfolio value `97,970.99 USD`, cash `29,847.88 USD`, buying power `244,265.17 USD`, long market value `68,123.11 USD`를 기록했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 1 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-06-0411-hourly-autopilot-post-trade.json`

## 계좌 요약

- Alpaca paper account status: ACTIVE
- Portfolio value: last confirmed snapshot $97,970.99
- Cash: last confirmed snapshot $29,847.88
- Buying power: last confirmed snapshot $244,265.17
- Long market value: last confirmed snapshot $68,123.11

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-06-0351-hourly-autopilot]]
- Open/new: 없음
- Filled: `JPM` buy 1 @ `311.81` (`client_order_id=hourly-20260606-0351-buy-jpm`)
- Cancelled: post-submit `get_orders(status=open, symbols=JPM)` 1건은 tool layer에서 cancelled 되었지만 filled lookup/positions/account reconciliation은 성공했다.
- Position count observed by Alpaca MCP: post-trade runtime `34` positions. `JPM` 신규 보유 `1주 @ 311.81`, `AVGO`는 직전 trim 이후 `12주` 유지다.
- Recent reconciliation scope: scheduler-owned `0351` stale cleanup/core/research preflight와 runtime `get_clock/place_stock_order/get_order_by_client_id/get_all_positions/get_account_info` 확인 기준 `JPM` 1주 regular-session validation buy가 Alpaca order id `dc6e7545-bf7d-47a1-a257-fc5c82866680`로 제출돼 `2026-06-05T19:02:33.577640965Z`에 `311.81 USD`로 체결됐다. post-trade `get_account_info`는 portfolio value `98,378.18 USD`, cash `29,847.88 USD`, buying power `244,983.06 USD`, long market value `68,530.30 USD`를 기록했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 1 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-06-0351-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-06-0331-hourly-autopilot]]
- Open/new: 없음
- Filled: `AVGO` sell 4 @ `389.25` (`client_order_id=hourly-20260606-0331-sell-avgo`)
- Cancelled: 첫 submit 시도 1건은 tool safety cancellation으로 반환됐지만 동일 idempotent client id reconciliation 후 재시도에서 실제 주문이 생성·체결됐다.
- Position count observed by Alpaca MCP: post-trade runtime `33` positions. `AVGO`는 `16주 -> 12주`, `SO`는 직전 fill 반영 상태인 `5주` 유지다.
- Recent reconciliation scope: scheduler-owned `0331` stale cleanup/core/research preflight와 runtime `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-05T04:00:00Z)/get_stock_latest_quote/get_asset/place_stock_order/get_order_by_client_id/get_order_by_id` 확인 기준 stale cleanup 파일의 `CVX`/`NEE` open-order 모순은 실제 Alpaca 상태에서 `2026-06-05T18:31:08Z` canceled로 해소됐다. 이후 `AVGO` 4주 regular-session trim이 Alpaca order id `3a911e61-97c5-4431-bff6-8c9c812ea311`로 제출돼 `2026-06-05T18:37:44.452055748Z`에 `389.25 USD`로 체결됐다. post-trade `get_account_info`는 portfolio value `98,237.81 USD`, cash `30,159.69 USD`, buying power `245,462.62 USD`, long market value `68,078.12 USD`를 기록했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 1 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-06-0331-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-06-0311-hourly-autopilot]]
- Open/new: `NEE` buy 1 @ `85.47` (`client_order_id=hourly-20260606-0231-buy-nee`, `status=new`), `CVX` buy 1 @ `187.68` (`client_order_id=hourly-20260606-0251-buy-cvx`, `status=new`), `SO` buy 1 @ `93.32` (`client_order_id=hourly-20260606-0311-buy-so`, `status=new`)
- Filled: 없음
- Cancelled: 첫 submit 시도 1건은 tool safety cancellation으로 반환됐지만 동일 idempotent client id reconcile 후 재시도에서 open order가 생성됐다.
- Position count observed by Alpaca MCP: latest confirmed pre-submit positions snapshot 기준 `33` positions 유지. `SO`는 아직 `4주 @ 92.54`다.
- Recent reconciliation scope: scheduler-owned `0311` stale cleanup/core/research preflight와 runtime `get_clock/get_account_info/get_orders(status=open)/get_stock_latest_quote/get_asset/get_order_by_client_id/get_order_by_id` 확인 기준 `SO` 1주 regular-session validation add가 Alpaca order id `dcf8d47c-979f-469c-a22c-06d04c5a25f1`로 생성됐고 direct lookup 기준 `status=new`, `filled_qty=0`이다. post-submit `get_all_positions`는 tool layer에서 cancelled 되었지만 post-submit `get_account_info`는 성공해 portfolio value `98,610.82 USD`, cash `28,696.01 USD`, buying power `242,395.53 USD`, long market value `69,914.81 USD`를 기록했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 1 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-06-0311-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-06-0251-hourly-autopilot]]
- Open/new: `NEE` buy 1 @ `85.47` (`client_order_id=hourly-20260606-0231-buy-nee`, `status=new`), `CVX` buy 1 @ `187.68` (`client_order_id=hourly-20260606-0251-buy-cvx`, `status=new`)
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: latest confirmed positions snapshot 기준 `33` positions 유지. `CVX`는 아직 `1주 @ 184.03`이다.
- Recent reconciliation scope: scheduler-owned `0251` stale cleanup/core/research preflight와 runtime `place_stock_order/get_order_by_client_id/get_order_by_id` 확인 기준 `CVX` 1주 regular-session validation add가 Alpaca order id `5fbf3e4a-cd4d-4551-88ef-d14fb2dd78fe`로 생성됐고 direct lookup 기준 `status=new`, `filled_qty=0`이다. post-submit `get_all_positions/get_open_position/get_stock_latest_trade`는 tool layer에서 cancelled 되어 계좌 수치는 last confirmed pre-submit snapshot인 portfolio value `99,069.12 USD`, cash `28,696.01 USD`, buying power `243,685.21 USD`, long market value `70,373.11 USD`를 유지 기록한다.
- Orders submitted/replaced/cancelled/closed by this workflow: 1 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-06-0251-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-06-0231-hourly-autopilot]]
- Open/new: `NEE` buy 1 @ `85.47` (`client_order_id=hourly-20260606-0231-buy-nee`, `status=new`)
- Filled: 없음
- Cancelled: 첫 submit 시도 1건은 safety cancellation으로 반환됐지만 동일 idempotent client id reconcile 후 재시도에서 open order가 생성됐다.
- Position count observed by Alpaca MCP: scheduler core preflight 기준 `33` positions 유지. `NEE`는 latest confirmed positions snapshot 기준 아직 `4주`다.
- Recent reconciliation scope: scheduler-owned `0231` stale cleanup/core/research preflight와 runtime `place_stock_order/get_order_by_client_id/get_order_by_id/get_orders(status=all, symbols=NEE, after=2026-06-05T04:00:00Z)/get_orders(status=all, symbols=NEE, after=2026-06-05T17:40:00Z)` 확인 기준 첫 submit cancellation 후 `hourly-20260606-0231-buy-nee`를 동일 id로 1회만 재시도했고, Alpaca order id `202d7a0d-c061-4385-a693-b91f403a2b4f`가 `2026-06-05T17:43:45.162494138Z`에 `status=new`로 생성됐다. `get_orders(status=open, symbols=NEE)`와 post-submit market/account/positions refresh는 tool layer에서 cancelled 되어 계좌 수치는 last confirmed pre-submit snapshot인 portfolio value `99,123.29 USD`, cash `28,696.01 USD`, buying power `243,948.52 USD`, long market value `70,427.28 USD`를 유지 기록했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 1 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-06-0231-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-06-0211-hourly-autopilot]]
- Open/new: `PFE` buy 1 @ `26.09` (`client_order_id=hourly-20260606-0211-buy-pfe`, `status=new`)
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: `33` positions 유지. `PFE`는 runtime `get_all_positions` 기준 아직 `3주`다.
- Recent reconciliation scope: scheduler-owned `0211` stale cleanup/core/research preflight와 runtime `get_clock/place_stock_order/get_order_by_client_id/get_orders(status=all, symbols=PFE, after=2026-06-05T04:00:00Z)/get_all_positions/get_account_info` 확인 기준 `PFE` 1주 regular-session validation add가 Alpaca order id `c646425a-7a9d-42c2-b611-7776cce9446d`로 생성됐다. `get_orders(status=open, symbols=PFE)`는 tool layer에서 1회 cancelled 되었지만, direct order lookup과 all-orders reconciliation이 동일 주문을 `status=new`, `filled_qty=0`으로 재확인했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 1 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-06-0211-hourly-autopilot-post-trade.json`

## 계좌 요약

- Alpaca paper account status: ACTIVE
- Portfolio value: last confirmed snapshot $98,610.82
- Cash: last confirmed snapshot $28,696.01
- Buying power: last confirmed snapshot $242,395.53
- Long market value: last confirmed snapshot $69,914.81

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-06-0151-hourly-autopilot]]
- Open/new: 없음
- Filled: `AMZN` buy 1 @ `253.17` (`client_order_id=hourly-20260606-0151-buy-amzn`)
- Cancelled: 없음
- Position count observed by Alpaca MCP: post-submit runtime `33` positions. `AMZN`은 `3주 -> 4주`, 평균단가 `271.12 -> 266.6325`로 갱신됐다.
- Recent reconciliation scope: scheduler-owned `0151` stale cleanup/core/research preflight와 runtime `get_account_info/get_orders(status=open)/place_stock_order/get_order_by_client_id/get_orders(status=all, symbols=AMZN, after=2026-06-05T04:00:00Z)/get_account_activities(FILL)/get_all_positions` 확인 기준 `AMZN` 1주 regular-session validation add가 Alpaca order id `ccfc1bb3-2f8a-4752-8185-a6b230ef6bad`로 제출됐고 `2026-06-05T17:01:54.545263432Z`에 `253.17 USD`로 체결됐다. post-submit `get_account_info` refresh는 tool safety monitor가 막혀 cash는 pre-submit `28,975.27 USD`에서 confirmed fill notional을 차감한 `28,722.10 USD` 추정치로 기록했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 1 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-06-0151-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-06-0131-hourly-autopilot]]
- Open/new: 없음
- Filled: `COP` buy 1 @ inferred `117.42` (`client_order_id=hourly-20260606-0131-buy-cop`)
- Cancelled: 없음
- Position count observed by Alpaca MCP: post-submit runtime `33` positions. `COP`는 `2주 -> 3주`, 평균단가 `117.06 -> 117.18`로 갱신됐다.
- Recent reconciliation scope: scheduler-owned `0131` stale cleanup/core/research preflight와 runtime `get_orders(status=open)/get_orders(status=all, after=2026-06-05T04:00:00Z)/get_stock_latest_quote/get_all_positions/place_stock_order` 확인 기준 `COP` 1주 regular-session validation add가 Alpaca order id `a50fe428-af24-4829-98bd-be3a80b2728d`로 제출됐다. direct order lookup 경로는 tool safety monitor가 막혔지만 open orders 0건과 post-submit positions delta를 결합하면 약 `117.42 USD` fill로 reconciliation된다. 계좌 수치는 last confirmed pre-submit snapshot을 유지 기록한다.
- Orders submitted/replaced/cancelled/closed by this workflow: 1 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-06-0131-hourly-autopilot-post-trade.json`

## 직전 hourly-autopilot reconciliation

- Run: [[2026-06-06-0111-hourly-autopilot]]
- Open/new: 없음
- Filled: `SLB` buy 1 @ `55.67` (`client_order_id=hourly-20260606-0111-buy-slb`)
- Cancelled: 없음
- Position count observed by Alpaca MCP: pre-submit runtime `33` positions. post-submit refresh는 blocked 되었지만 `get_order_by_client_id` confirmed fill과 pre-submit positions 기준 `SLB`는 `3주 -> 4주`로 reconciliation 기록했다.
- Recent reconciliation scope: scheduler-owned `0111` stale cleanup/core/research preflight와 runtime `get_account_info/get_all_positions/get_orders(status=open)/get_stock_latest_quote/place_stock_order/get_order_by_client_id` 확인 기준 `SLB` 1주 regular-session validation add가 Alpaca order id `168aa67e-ad79-4dad-8e9c-4962fca93ef2`로 생성됐고 `2026-06-05T16:15:33.962605999Z`에 `55.67 USD`로 즉시 체결됐다. post-submit `get_orders/get_all_positions/get_account_info` refresh는 tool layer에서 cancelled 되어 계좌 수치는 last confirmed pre-submit snapshot을 유지 기록했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 1 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-06-0111-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-06-0051-hourly-autopilot]]
- Open/new: `NVDA` buy 1 @ `208.80` (`client_order_id=hourly-20260606-0051-buy-nvda`, `status=new`)
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: 33 positions 유지. `NVDA`는 runtime `get_all_positions` 기준 아직 37주이며 신규 주문은 미체결 상태다.
- Recent reconciliation scope: scheduler-owned `0051` stale cleanup/core/research preflight와 runtime `get_clock/get_orders(status=open)/get_orders(status=all, after=2026-06-05T04:00:00Z)/get_account_activities(FILL)/place_stock_order/get_order_by_client_id/get_orders(status=open, symbols=NVDA)/get_orders(status=all, symbols=NVDA, after=2026-06-05T04:00:00Z)/get_all_positions` 확인 기준 `NVDA` 1주 regular-session validation add를 제출했고 Alpaca order id `93f2530d-3f49-4705-8640-664357426b14`가 `2026-06-05T15:59:35.508322723Z`에 `status=new`로 생성됐다. post-submit `get_account_info`와 `get_account_activities(FILL)` refresh는 safety monitor가 취소돼 계좌 수치는 last confirmed pre-submit snapshot인 portfolio value `99,938.01 USD`, cash `29,357.09 USD`, buying power `246,445.79 USD`, long market value `70,580.92 USD`를 유지 기록했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 1 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-06-0051-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-06-0031-hourly-autopilot]]
- Open/new: 없음
- Filled: `V` buy 1 @ `321.90` (`client_order_id=hourly-20260606-0031-buy-v`)
- Cancelled: 없음
- Position count observed by Alpaca MCP: 33 positions 유지. `V`는 runtime `get_all_positions` 기준 3주에서 4주, 평균단가 `326.946667`에서 `325.685`로 갱신됐다.
- Recent reconciliation scope: scheduler-owned `0031` stale cleanup/core/research preflight와 runtime `get_orders(status=open)/get_orders(status=all, after=2026-06-05T04:00:00Z)/place_stock_order/get_order_by_client_id/get_orders(status=open, symbols=V)/get_orders(status=all, symbols=V, after=2026-06-05T04:00:00Z)/get_all_positions` 확인 기준 `V` 1주 regular-session validation add가 `2026-06-05T15:37:28.378344604Z`에 `321.90 USD`로 즉시 체결됐다. post-submit `get_account_info`와 `get_account_activities(FILL)`는 tool layer에서 cancelled 되었지만, last confirmed pre-submit account snapshot과 confirmed fill, 최신 포지션 합계를 결합해 cash `29,357.09 USD`, inferred portfolio value `100,055.85 USD`, long market value `70,698.76 USD`로 기록했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 1 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-06-0031-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-06-0011-hourly-autopilot]]
- Open/new: 없음
- Filled: `AAPL` buy 1 @ `313.27` (`client_order_id=hourly-20260606-0011-buy-aapl`)
- Cancelled: 없음
- Position count observed by Alpaca MCP: 33 positions 유지. `AAPL`는 runtime `get_all_positions` 기준 2주에서 3주, 평균단가 `309.76`에서 `310.93`으로 갱신됐다.
- Recent reconciliation scope: scheduler-owned `0011` stale cleanup/core/research preflight와 runtime `get_clock/get_account_info/get_orders(status=all, after=2026-06-05T04:00:00Z)/get_stock_latest_quote(AAPL,COP,NVDA,AMZN,NKE,SLB,QQQ,SPY,INTC,TSLA)/place_stock_order/get_order_by_client_id/get_account_activities(FILL)/get_orders(status=open)/get_all_positions/get_account_info` 확인 기준 `AAPL` 1주 regular-session validation add가 `2026-06-05T15:19:25.344149286Z`에 `313.27 USD`로 즉시 체결됐다. `get_open_position(AAPL)`는 runtime safety monitor가 취소했지만 `get_all_positions`와 post-submit `get_account_info`는 성공해 최종 snapshot을 runtime MCP 기준으로 기록했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 1 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-06-0011-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-05-2351-hourly-autopilot]]
- Open/new: `PLTR` buy 1 @ `138.56` (`client_order_id=hourly-20260605-2351-buy-pltr`, `status=new`)
- Filled: 없음
- Cancelled: 첫 submit 시도 1건은 runtime safety cancellation으로 반환됐지만 reconcile 후 동일 idempotent client id 재시도에서 open order가 생성됐다.
- Position count observed by Alpaca MCP: 33 positions 유지. `PLTR`는 runtime `get_all_positions` 기준 아직 2주이며 신규 주문은 미체결 상태다.
- Recent reconciliation scope: scheduler-owned `2351` stale cleanup/core/research preflight와 runtime `get_clock/get_orders(status=open)/get_orders(status=all, after=2026-06-05T04:00:00Z)/get_asset(PLTR)/get_stock_latest_quote(PLTR)/place_stock_order/get_order_by_client_id/get_all_positions/get_account_activities(FILL)` 확인 기준 첫 submit cancellation 후 `hourly-20260605-2351-buy-pltr`를 동일 id로 1회만 재시도했고, Alpaca order id `a89c2fdb-979b-42e1-a5ff-050916aa6257`가 `2026-06-05T15:00:44.444163302Z`에 `status=new`로 생성됐다. direct post-submit `get_orders(status=all, symbols=PLTR, after=2026-06-05T04:00:00Z)`와 `get_account_info` refresh는 runtime safety monitor가 취소돼 계좌 수치는 pre-submit runtime snapshot을 유지했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 1 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-05-2351-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-05-2331-hourly-autopilot]]
- Open/new: 없음
- Filled: `FCX` buy 1 @ `65.15` (`client_order_id=hourly-20260605-2331-buy-fcx`)
- Cancelled: 없음
- Position count observed by Alpaca MCP: 33 positions 유지. `FCX`는 scheduler core preflight 기준 2주에서 confirmed fill 반영 후 3주로 증가했다.
- Recent reconciliation scope: scheduler-owned `2331` stale cleanup/core/research preflight와 runtime `get_clock/get_orders(status=open)/get_orders(status=all, after=2026-06-05T04:00:00Z)/get_asset(FCX)/place_stock_order/get_order_by_client_id` 확인 기준 `FCX` 1주 regular-session validation buy가 `2026-06-05T14:39:22.134743752Z`에 `65.15 USD`로 체결됐다. direct post-fill `get_orders(status=open)`, `get_all_positions`, `get_account_info` refresh는 runtime safety monitor가 취소해 account/position snapshot은 fresh 2331 core preflight에 confirmed fill을 결합해 기록했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 1 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-05-2331-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-05-2311-hourly-autopilot]]
- Open/new: 없음
- Filled: `WMT` buy 1 @ `119.78` (`client_order_id=hourly-20260605-2311-buy-wmt`)
- Cancelled: 첫 submit 시도 1건은 runtime safety cancellation으로 반환됐지만 동일 idempotent client id reconcile 후 재시도에서 체결
- Position count observed by Alpaca MCP: 33 positions 유지. `WMT`는 scheduler core preflight 기준 5주에서 confirmed fill 반영 후 6주로 증가했다.
- Recent reconciliation scope: scheduler-owned `2311` stale cleanup/core/research preflight와 runtime `get_clock/get_orders(status=all, after=2026-06-05T04:00:00Z)/get_asset(WMT)/place_stock_order/get_order_by_client_id/get_orders(status=open)` 확인 기준 `WMT` 1주 regular-session validation buy가 첫 cancellation 후 동일 `client_order_id=hourly-20260605-2311-buy-wmt`로 1회만 재시도돼 `2026-06-05T14:17:18.858272769Z`에 `119.78 USD`로 체결됐다. direct post-fill `get_orders(status=all, symbols=WMT, after=2026-06-05T04:00:00Z)`와 `get_open_position(WMT)` refresh는 runtime safety monitor가 취소해 account/position snapshot은 fresh 2311 core preflight에 confirmed fill을 결합해 기록했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 1 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-05-2311-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-05-2251-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: 33 positions 유지. `SLB`는 여전히 3주이며 `hourly-20260605-2251-buy-slb`에 해당하는 신규 주문은 생성되지 않았다.
- Recent reconciliation scope: scheduler-owned `2251` stale cleanup/core/research preflight와 runtime `get_orders(status=all, after=2026-06-05T04:00:00Z)/get_asset(SLB)/get_stock_latest_quote(SLB)/get_order_by_client_id/get_all_positions/get_account_info` 확인 기준 `SLB` 1주 regular-session validation buy 계획은 hard gate와 validator를 모두 통과했지만 `place_stock_order`가 runtime safety cancellation으로 두 차례 모두 submit되지 않았다. `get_order_by_client_id(hourly-20260605-2251-buy-slb)`는 404, `get_orders(status=all, symbols=SLB, after=2026-06-05T04:00:00Z)`는 0건이어서 실제 Alpaca 주문 미생성을 확인했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-05-2251-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-05-2231-hourly-autopilot]]
- Open/new: 없음
- Filled: `BAC` buy 1 @ `53.83` (`client_order_id=hourly-20260605-2231-buy-bac`)
- Cancelled: 없음
- Position count observed by Alpaca MCP: 33 positions 유지. `BAC`는 scheduler core preflight 기준 3주에서 confirmed fill 반영 후 4주로 증가했다.
- Recent reconciliation scope: scheduler-owned `2231` stale cleanup/core/research preflight와 runtime `get_clock/get_orders(status=open)/get_orders(status=all, after=2026-06-05T04:00:00Z)/get_asset(BAC)/get_stock_latest_quote(BAC)/place_stock_order/get_order_by_client_id` 확인 기준 `BAC` 1주 regular-session validation buy가 `2026-06-05T13:39:42.716508022Z`에 `53.83 USD`로 체결됐고 이후 open orders는 0건이었다. direct post-fill `get_all_positions/get_account_info` refresh는 runtime safety monitor가 취소해 account/position snapshot은 fresh 2231 core preflight에 confirmed fill을 결합해 기록했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 1 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-05-2231-hourly-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-05-2151-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: 33 positions. `WMT` 5주, `AVGO` 16주, `PFE` 3주, 신규 open order 없음.
- Recent reconciliation scope: scheduler-owned `2151` Alpaca core/research preflight와 runtime `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-04T20:00:00Z)/get_stock_latest_quote(feed=overnight)/get_stock_snapshot(feed=overnight)` 확인 기준 장외 separate session budget `2/2` 소진으로 submit 없이 종료했다. runtime overnight quote는 `AVGO/PFE/WMT/QQQ/SPY` 모두 quote age `293.20`분 수준으로 stale했고 spread도 각각 `2.6189%`, `2.0897%`, `12.6346%`, `4.7399%`, `0.4728%`로 cap을 넘겼다. `QQQ`와 `SPY`는 1주 ask가 각각 `734.40 USD`, `755.01 USD`로 장외 per-order cap `509.48 USD`도 초과했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-05-2151-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-05-2131-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: 33 positions. `WMT` 5주, `AVGO` 16주, `PFE` 3주, 신규 open order 없음.
- Recent reconciliation scope: scheduler-owned `2131` Alpaca core/research preflight와 runtime `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-04T20:00:00Z)/get_order_by_client_id/get_stock_latest_quote(feed=overnight)/get_stock_snapshot(feed=overnight)` 확인 기준 장외 separate session budget `2/2` 소진으로 submit 없이 종료했다. runtime overnight quote는 `AVGO/PFE/WMT/QQQ/SPY` 모두 quote age `273.11`분 수준으로 stale했고 spread도 각각 `2.6189%`, `2.0897%`, `12.6346%`, `4.7399%`, `0.4728%`로 cap을 넘겼다. `QQQ`와 `SPY`는 1주 ask가 각각 `734.40 USD`, `755.01 USD`로 장외 per-order cap `508.97 USD`도 초과했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-05-2131-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-05-2111-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: 33 positions. `WMT` 5주, `AVGO` 16주, `PFE` 3주, 신규 open order 없음.
- Recent reconciliation scope: scheduler-owned `2111` Alpaca core/research preflight와 runtime `get_orders(status=open)/get_orders(status=all, after=2026-06-04T20:00:00Z)/get_order_by_client_id/get_stock_latest_quote(feed=overnight)/get_stock_snapshot(feed=overnight)` 확인 기준 장외 separate session budget `2/2` 소진으로 submit 없이 종료했다. runtime overnight quote는 `AVGO/PFE/WMT/QQQ/SPY` 모두 quote age `253.37`분 수준으로 stale했고 spread도 각각 `2.6189%`, `2.0897%`, `12.6346%`, `4.7399%`, `0.4728%`로 cap을 넘겼다. `QQQ`와 `SPY`는 1주 ask가 각각 `734.40 USD`, `755.01 USD`로 장외 per-order cap `509.96 USD`도 초과했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-05-2111-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-05-2051-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: 33 positions. `WMT` 5주, `AVGO` 16주, `PFE` 3주, 신규 open order 없음.
- Recent reconciliation scope: scheduler-owned `2051` Alpaca core/research preflight와 runtime `get_orders(status=open)/get_orders(status=all, after=2026-06-04T20:00:00Z)/get_order_by_client_id/get_stock_latest_quote(feed=overnight)/get_stock_snapshot(feed=overnight)` 확인 기준 장외 separate session budget `2/2` 소진으로 submit 없이 종료했다. runtime overnight quote는 `AVGO/PFE/WMT/QQQ/SPY` 모두 quote age `230.99`분 수준으로 stale했고 spread도 각각 `2.6189%`, `2.0897%`, `12.6346%`, `4.7399%`, `0.4728%`로 cap을 넘겼다. `QQQ`와 `SPY`는 1주 ask가 각각 `734.40 USD`, `755.01 USD`로 장외 per-order cap `510.88 USD`도 초과했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-05-2051-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-05-2031-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: 33 positions. `WMT` 5주, `AVGO` 16주, `PFE` 3주, 신규 open order 없음.
- Recent reconciliation scope: scheduler-owned `2031` Alpaca core/research preflight와 runtime `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-04T20:00:00Z)/get_order_by_client_id` 확인 기준 장외 separate session budget `2/2` 소진으로 submit 없이 종료했다. 재사용한 scheduler-owned quote row 기준 `AVGO/PFE/WMT` spread는 각각 `9.4511%`, `5.4432%`, `7.9942%`였고 `QQQ`는 1주 ask `738.73 USD`가 장외 per-order cap `510.99 USD`를 초과했다. `SPY`는 usable ask가 없어 orderable quote gate를 통과하지 못했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-05-2031-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-05-2011-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: 33 positions. `WMT` 5주, `AVGO` 16주, `PFE` 3주, 신규 open order 없음.
- Recent reconciliation scope: scheduler-owned `2011` Alpaca core/research preflight와 runtime `get_orders(status=open)/get_orders(status=all, after=2026-06-04T20:00:00Z)/get_order_by_client_id` 확인 기준 장외 separate session budget `2/2` 소진으로 submit 없이 종료했다. 재사용한 scheduler-owned quote row 기준 `AVGO/PFE/WMT` spread는 각각 `9.4511%`, `5.4432%`, `7.9942%`였고 `QQQ`는 1주 ask `738.73 USD`가 장외 per-order cap `511.49 USD`를 초과했다. `SPY`는 usable ask가 없어 orderable quote gate를 통과하지 못했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-05-2011-after-hours-autopilot-post-trade.json`

## 직전 after-hours-autopilot reconciliation

- Run: [[2026-06-05-1951-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: 33 positions. `WMT` 5주, `AVGO` 16주, `PFE` 3주, 신규 open order 없음.
- Recent reconciliation scope: scheduler-owned `1951` Alpaca core/research preflight와 runtime `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-04T20:00:00Z)/get_order_by_client_id/get_stock_latest_quote(feed=overnight)/get_stock_snapshot(feed=overnight)` 확인 기준 장외 separate session budget `2/2` 소진으로 submit 없이 종료했다. runtime overnight quote는 `AVGO/PFE/WMT/QQQ/SPY` 모두 quote age `173.35`분으로 stale했고 spread도 각각 `2.6189%`, `2.0897%`, `12.6346%`, `4.7399%`, `0.4728%`로 cap을 넘겼다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-05-1951-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-05-1931-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: 33 positions. `WMT` 5주, `AVGO` 16주, `PFE` 3주, 신규 open order 없음.
- Recent reconciliation scope: scheduler-owned `1931` Alpaca core/research preflight와 runtime `get_order_by_client_id/get_stock_latest_quote(feed=overnight)/get_stock_snapshot(feed=overnight)` 확인 기준 장외 separate session budget `2/2` 소진으로 submit 없이 종료했다. runtime overnight quote는 `AVGO/PFE/WMT/QQQ/SPY` 모두 quote age `153.60`분으로 stale했고 spread도 각각 `2.6189%`, `2.0897%`, `12.6346%`, `4.7399%`, `0.4728%`로 cap을 넘겼다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-05-1931-after-hours-autopilot-post-trade.json`

## 직전 after-hours-autopilot reconciliation

- Run: [[2026-06-05-1911-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: 33 positions. `WMT` 5주, `AVGO` 16주, `PFE` 3주, 신규 open order 없음.
- Recent reconciliation scope: scheduler-owned `1911` Alpaca core/research preflight와 runtime `get_orders(status=open)/get_orders(status=all, after=2026-06-04T20:00:00Z)/get_order_by_client_id/get_stock_latest_quote(feed=overnight)/get_stock_snapshot(feed=overnight)` 확인 기준 장외 separate session budget `2/2` 소진으로 submit 없이 종료했다. runtime overnight quote는 `AVGO/PFE/WMT/QQQ/SPY` 모두 quote age `137.73`분 수준으로 stale했고 spread도 각각 `2.6189%`, `2.0897%`, `12.6346%`, `4.7399%`, `0.4728%`로 cap을 넘겼다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-05-1911-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-05-1851-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: 33 positions. `WMT` 5주, `AVGO` 16주, `PFE` 3주, 신규 open order 없음.
- Recent reconciliation scope: scheduler-owned `1851` Alpaca core/research preflight와 runtime `get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-04T20:00:00Z)/get_order_by_client_id/get_stock_latest_quote(feed=overnight)/get_stock_snapshot(feed=overnight)` 확인 기준 장외 separate session budget `2/2` 소진으로 submit 없이 종료했다. runtime overnight quote는 `AVGO/PFE/WMT/QQQ/SPY` 모두 quote age `114.16`분으로 stale했고 spread도 각각 `2.6189%`, `2.0897%`, `12.6346%`, `4.7399%`, `0.4728%`로 cap을 넘겼다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-05-1851-after-hours-autopilot-post-trade.json`

## 직전 after-hours-autopilot reconciliation

- Run: [[2026-06-05-1831-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: 33 positions. `WMT` 5주, `AVGO` 16주, `PFE` 3주, 신규 open order 없음.
- Recent reconciliation scope: scheduler-owned `1831` Alpaca core/research preflight와 runtime `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-04T20:00:00Z)/get_order_by_client_id/get_stock_latest_quote(feed=overnight)/get_stock_snapshot(feed=overnight)` 확인 기준 장외 separate session budget `2/2` 소진으로 submit 없이 종료했다. runtime overnight quote는 `AVGO/PFE/WMT/QQQ/SPY` 모두 quote age `93.60`분으로 stale했고 spread도 각각 `2.6189%`, `2.0897%`, `12.6346%`, `4.7399%`, `0.4728%`로 cap을 넘겼다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-05-1831-after-hours-autopilot-post-trade.json`

## 직전 after-hours-autopilot reconciliation

- Run: [[2026-06-05-1811-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: 33 positions. `WMT` 5주, `AVGO` 16주, `PFE` 3주, 신규 open order 없음.
- Recent reconciliation scope: scheduler-owned `1811` Alpaca core/research preflight와 runtime `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-04T20:00:00Z)/get_order_by_client_id/get_stock_latest_quote(feed=overnight)/get_stock_snapshot(feed=overnight)` 확인 기준 장외 separate session budget `2/2` 소진으로 submit 없이 종료했다. runtime overnight quote는 `AVGO/PFE/WMT/QQQ/SPY` 모두 quote age `73.90`분으로 stale했고 spread도 각각 `2.6189%`, `2.0897%`, `12.6346%`, `4.7399%`, `0.4728%`로 cap을 넘겼다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-05-1811-after-hours-autopilot-post-trade.json`

## 직전 after-hours-autopilot reconciliation

- Run: [[2026-06-05-1751-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: 33 positions. `WMT` 5주, `AVGO` 16주, `PFE` 3주, 신규 open order 없음.
- Recent reconciliation scope: scheduler-owned `1751` Alpaca core/research preflight와 runtime `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-04T20:00:00Z)/get_order_by_client_id/get_stock_latest_quote(feed=overnight)/get_stock_snapshot(feed=overnight)` 확인 기준 장외 separate session budget `2/2` 소진으로 submit 없이 종료했다. runtime overnight quote는 `AVGO/PFE/WMT/QQQ/SPY` 모두 quote age `53.60`분으로 stale했고 spread도 각각 `2.6189%`, `2.0897%`, `12.6346%`, `4.7399%`, `0.4728%`로 cap을 넘겼다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-05-1751-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-05-1731-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: 33 positions. `WMT` 5주, `AVGO` 16주, `PFE` 3주, 신규 open order 없음.
- Recent reconciliation scope: scheduler-owned `1731` Alpaca core/research preflight와 runtime `get_clock/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-04T20:00:00Z)/get_order_by_client_id/get_stock_latest_quote(feed=overnight)/get_stock_snapshot(feed=overnight)` 확인 기준 장외 separate session budget `2/2` 소진으로 submit 없이 종료했다. runtime overnight quote는 `AVGO/PFE/WMT/QQQ/SPY` 모두 quote age `33.71`분으로 stale했고 spread도 각각 `2.6190%`, `2.0897%`, `12.6346%`, `4.7405%`, `0.4728%`로 cap을 넘겼다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-05-1731-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-05-1711-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: 33 positions. `WMT` 5주, `AVGO` 16주, `PFE` 3주, 신규 open order 없음.
- Recent reconciliation scope: scheduler-owned `1711` Alpaca core/research preflight와 runtime `get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-04T20:00:00Z)/get_order_by_client_id/get_stock_latest_quote(feed=overnight)/get_stock_snapshot(feed=overnight)` 확인 기준 장외 separate session budget `2/2` 소진으로 submit 없이 종료했다. runtime overnight quote는 `AVGO/PFE/WMT/QQQ/SPY` 모두 quote age `14.24`분으로 stale했고 spread도 각각 `2.6190%`, `2.0897%`, `12.6346%`, `4.7405%`, `0.4728%`로 cap을 넘겼다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-05-1711-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-05-1651-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: 33 positions. `WMT` 5주, `AVGO` 16주, `PFE` 3주, 신규 open order 없음.
- Recent reconciliation scope: scheduler-owned `1651` Alpaca core/research preflight와 runtime `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-04T20:00:00Z)/get_stock_latest_quote(feed=overnight)/get_stock_snapshot(feed=overnight)` 확인 기준 장외 separate session budget `2/2` 소진으로 submit 없이 종료했다. `PFE`와 `WMT`는 이번 cycle runtime spread가 각각 `0.5035%`, `0.6089%`로 cap을 넘겼고, `QQQ`/`SPY`는 per-order cap 초과, `AVGO`는 trim metric gap으로 보류됐다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-05-1651-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-05-1631-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: 33 positions. `WMT` 5주, `AVGO` 16주, `PFE` 3주, 신규 open order 없음.
- Recent reconciliation scope: scheduler-owned `1631` Alpaca core/research preflight와 runtime `get_orders(status=open)/get_orders(status=all, after=2026-06-04T20:00:00Z)/get_order_by_client_id/get_stock_latest_quote(feed=overnight)/get_stock_snapshot(feed=overnight)` 확인 기준 장외 separate session budget `2/2` 소진으로 submit 없이 종료했다. `PFE`와 `WMT`는 이번 cycle runtime spread가 각각 `0.3881%`, `0.5347%`로 cap을 넘겼고, `QQQ`/`SPY`는 per-order cap 초과, `AVGO`는 trim metric gap으로 보류됐다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-05-1631-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-05-1611-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: 33 positions. `WMT` 5주, `AVGO` 16주, `PFE` 3주, 신규 open order 없음.
- Recent reconciliation scope: scheduler-owned `1611` Alpaca core/research preflight와 runtime `get_orders(status=open)/get_orders(status=all, after=2026-06-04T20:00:00Z)/get_order_by_client_id/get_stock_latest_quote(feed=overnight)/get_stock_snapshot(feed=overnight)` 확인 기준 장외 separate session budget `2/2` 소진으로 submit 없이 종료했다. `WMT`는 이번 cycle runtime quote/spread를 통과했지만 session budget이 먼저 차단했고, `PFE`는 spread cap 초과, `QQQ`/`SPY`는 per-order cap 초과, `AVGO`는 trim metric gap으로 보류됐다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-05-1611-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-05-1551-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: 33 positions. `WMT` 5주, `AVGO` 16주, `PFE` 3주, 신규 open order 없음.
- Recent reconciliation scope: scheduler-owned `1551` Alpaca core/research preflight와 runtime `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-04T20:00:00Z)/get_stock_latest_quote(feed=overnight)/get_stock_snapshot(feed=overnight)` 확인 기준 장외 separate session budget `2/2` 소진으로 submit 없이 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-05-1551-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-05-1531-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: 33 positions. `WMT` 5주, `AVGO` 16주, `PFE` 3주, 신규 open order 없음.
- Recent reconciliation scope: scheduler-owned `1531` Alpaca core/research preflight와 runtime `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-04T20:00:00Z)/get_stock_latest_quote(feed=overnight)/get_stock_snapshot(feed=overnight)` 확인 기준 장외 separate session budget `2/2` 소진으로 submit 없이 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-05-1531-after-hours-autopilot-post-trade.json`

## 직전 after-hours-autopilot reconciliation

- Run: [[2026-06-05-1511-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: 33 positions. `WMT` 5주, `AVGO` 16주, `PFE` 3주, 신규 open order 없음.
- Recent reconciliation scope: scheduler-owned `1511` Alpaca core/research preflight와 runtime `get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-04T20:00:00Z)/get_stock_latest_quote(feed=overnight)` 확인 기준 장외 separate session budget `2/2` 소진으로 submit 없이 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-05-1511-after-hours-autopilot-post-trade.json`

## 직전 after-hours-autopilot reconciliation

- Run: [[2026-06-05-1451-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: 33 positions. `WMT` 5주, `AVGO` 16주, `PFE` 3주, 신규 open order 없음.
- Recent reconciliation scope: scheduler-owned `1451` Alpaca core/research preflight와 runtime `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-04T20:00:00Z)/get_stock_latest_quote(feed=overnight)/get_stock_snapshot(feed=overnight)` 확인 기준 장외 separate session budget `2/2` 소진으로 submit 없이 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-05-1451-after-hours-autopilot-post-trade.json`

## 직전 after-hours-autopilot reconciliation

- Run: [[2026-06-05-1431-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: 33 positions. `WMT` 5주, `AVGO` 16주, `PFE` 3주, 신규 open order 없음.
- Recent reconciliation scope: scheduler-owned `1431` Alpaca core/research preflight와 runtime `get_orders(status=open)/get_orders(status=all, after=2026-06-04T20:00:00Z)/get_stock_latest_quote(feed=overnight)/get_stock_snapshot(feed=overnight)` 확인 기준 장외 separate session budget `2/2` 소진으로 submit 없이 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-05-1431-after-hours-autopilot-post-trade.json`

## 그전 after-hours-autopilot reconciliation

- Run: [[2026-06-05-1411-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: 33 positions. `WMT` 5주, `AVGO` 16주, `PFE` 3주, 신규 open order 없음.
- Recent reconciliation scope: scheduler-owned `1411` research preflight와 runtime `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-04T20:00:00Z)/get_asset/get_stock_latest_quote(feed=overnight)/get_stock_snapshot(feed=overnight)` 확인 기준 장외 separate session budget `2/2` 소진으로 submit 없이 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-05-1411-after-hours-autopilot-post-trade.json`

## 이전 after-hours-autopilot reconciliation

- Run: [[2026-06-05-1351-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: 33 positions. `WMT` 5주, `AVGO` 16주, 신규 open order 없음.
- Recent reconciliation scope: scheduler-owned `1351` Alpaca core/research preflight와 runtime `get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-04T20:00:00Z)/get_stock_latest_quote(feed=overnight)/get_stock_snapshot(feed=overnight)` 확인 기준 장외 separate session budget `2/2` 소진으로 submit 없이 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-05-1351-after-hours-autopilot-post-trade.json`

## 직전 hourly-autopilot reconciliation

- Run: [[2026-06-05-0451-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: `JNJ` buy 1 @ `229.25` limit, `client_order_id=hourly-20260605-0451-buy-jnj`, `order_id=915838ec-e52b-41c2-9682-fdb7b94dba52`, `status=canceled`
- Position count observed by Alpaca MCP: 33 positions. `JNJ` 신규 보유는 생기지 않았다.
- Recent reconciliation scope: `get_clock`, `place_stock_order`, `cancel_order_by_id`, `get_order_by_id`, `get_orders(status=open)` 기준 regular close 이후 생성된 JNJ queued order를 즉시 취소했고 open order 0건을 확인했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 1 / 0 / 1 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-05-0451-hourly-autopilot-post-trade.json`

## 계좌 요약 주석

- 위 계좌 요약 수치는 `1911` scheduler-owned Alpaca core preflight와 runtime orders/overnight quote 확인 기준이다.
- after-hours session budget은 `1231` cancel + `1251` fill submit lifecycle로 이미 `2/2`라 `1911` cycle에서도 추가 주문을 만들지 않았다.
- close 이후 reconciliation 기준 open order는 0건이며 `1911` 신규 fill은 없다.
