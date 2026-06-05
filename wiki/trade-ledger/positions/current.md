# portfolio-current

_Last updated: 2026-06-06 00:01 KST_

## 계좌 요약

- Alpaca paper account status: ACTIVE
- Portfolio value: $100,670.12
- Cash: $30,130.79
- Buying power: $249,228.27
- Long market value: $70,539.33

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
