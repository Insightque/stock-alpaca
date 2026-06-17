## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-17-1411-after-hours-autopilot]]
- Open/new: 없음. direct `get_orders(status=open)` 기준 open orders `0`건이었다.
- Filled: same `client_order_id=ah-20260617-1351-sell-pfe-01` reconciliation 기준 `PFE` after-hours trim 1주가 `filled_avg_price=26.03 USD`, `filled_at=2026-06-17T05:11:09.778969Z`로 체결된 것이 확인됐다. earlier same-session `RGTI` trim 1주 fill과 합쳐 `get_orders(status=all, after=2026-06-16T20:00:00-04:00)` 및 `get_account_activities(activity_types=[FILL], after=2026-06-16T20:00:00-04:00)` 기준 same-session after-hours submitted orders/fills는 모두 `2`건이다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: live `get_all_positions` 기준 positions `33`건이었다.
- Recent reconciliation scope: scheduler-owned `1411` core/research preflight를 우선 읽었지만 core preflight에는 expected `market_closed`만 남아 있어, direct Alpaca MCP `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-16T20:00:00-04:00)/get_order_by_client_id/get_account_activities(activity_types=[FILL])/get_watchlists` continuity로 missing required rows를 보강했다. direct reconciliation 기준 regular market closed, account `ACTIVE`, open orders `0`, watchlists `0`, `PFE qty=2`, `qty_available=2`, `RGTI qty=27`를 재확인했고 separate after-hours session submitted count는 `2/2`로 닫혔다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 1.
- Source note: `wiki/trade-ledger/positions/2026-06-17-1411-after-hours-autopilot-post-trade.json`

_Last updated: 2026-06-17 14:14 KST_

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-17-1351-after-hours-autopilot]]
- Open/new: `PFE` after-hours trim 1주가 `client_order_id=ah-20260617-1351-sell-pfe-01`, `order_id=c96904a2-deab-415b-9b27-a20660a043e4`로 제출됐고 immediate same-id reconciliation 기준 `status=new`, `filled_qty=0` open order다.
- Filled: 이번 cycle 신규 fill 없음. same-session after-hours fills는 earlier `RGTI` trim 1건만 유지된다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: submit 전 source-of-record positions는 `33`건이었고 submit 후에도 total positions count는 `33`건으로 유지됐다.
- Recent reconciliation scope: scheduler-owned `1351` core/research preflight를 source-of-record로 사용했고, direct Alpaca MCP continuity는 regular market closed, account `ACTIVE`, open orders `1`, same-session after-hours submitted orders `2`, same-session fills `1`, watchlists `0`, `PFE qty=3`, `qty_available=2`, overnight quote freshness 확인으로만 제한했다. separate after-hours session submitted count는 `1/2 -> 2/2`로 증가했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 1 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-17-1351-after-hours-autopilot-post-trade.json`

_Last updated: 2026-06-17 14:00 KST_

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-17-1331-after-hours-autopilot]]
- Open/new: 없음. direct `get_orders(status=open)` 기준 open orders `0`건이었다.
- Filled: `RGTI` after-hours trim 1주가 `client_order_id=ah-20260617-1331-sell-rgti-01`, `filled_avg_price=20.96 USD`로 즉시 체결됐다. `get_orders(status=all, after=2026-06-16T20:00:00-04:00)` 기준 same-session after-hours orders/fills는 모두 `1`건이다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: submit 전 `33`건이었고 체결 후에도 total positions count는 `33`건으로 유지됐다.
- Recent reconciliation scope: scheduler-owned `1331` core/research preflight를 사용했고, sparse Alpaca core preflight는 direct Alpaca MCP `get_clock/get_account_info/get_all_positions/get_orders/get_watchlists/get_asset/get_stock_latest_quote(feed=overnight)`로 보강했다. separate after-hours session submitted count는 `0/2 -> 1/2`로 변했고, `RGTI`는 fresh overnight quote `20.94/20.99`, spread `0.2385%`, active/tradable, same-session duplicate `0` 조건에서 sell-first trim으로 선택됐다. 체결 후 `get_account_info` 기준 cash는 `30,344.81 USD -> 30,365.77 USD`, portfolio value는 `101,176.88 USD -> 101,133.79 USD`, buying power는 `303,781.80 USD -> 303,720.06 USD`였다.
- Orders submitted/replaced/cancelled/closed by this workflow: 1 / 0 / 0 / 1.
- Source note: `wiki/trade-ledger/positions/2026-06-17-1331-after-hours-autopilot-post-trade.json`

_Last updated: 2026-06-17 13:40 KST_

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-17-1311-after-hours-autopilot]]
- Open/new: 없음. scheduler-owned `1311` preflight `get_orders(status=open)` source-of-record 기준 open orders `0`건이었고, live `get_orders(status=open)` 기준도 `0`건이었다.
- Filled: 이번 cycle 신규 after-hours fill 없음. live `get_orders(status=all, after=2026-06-16T20:00:00-04:00)` 기준 same-session after-hours orders `0`건이었고 submit path에도 진입하지 않아 same-session fills는 `0`으로 유지됐다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler core preflight `get_all_positions` 기준 positions `33`건이었다.
- Recent reconciliation scope: scheduler-owned `1311` core/research preflight를 source-of-record로 사용했고, 사용자가 같은 preflight의 passing account/positions/orders/asset/quote/spread rows를 submit-boundary evidence로 유지하라고 요구했으므로 live Alpaca continuity는 `get_orders(status=open)/get_orders(status=all, after=2026-06-16T20:00:00-04:00)/get_watchlists/get_stock_latest_quote(feed=iex, symbols=QQQ,IONQ,AVGO)/get_stock_snapshot(feed=overnight, symbols=QQQ,IONQ,AVGO)` 확인으로만 제한했다. separate after-hours session submitted count는 `0/2`로 열려 있었지만 `QQQ` freshest shortlist quote도 age 약 `439.93분`, `IONQ`는 `460.51분`, `QBTS/JPM/PFE`는 `469.33-490.50분`, `AVGO/SO/RGTI` sell-trim 후보는 `491분대` stale quote와 wide spread로 submit path에 진입하지 못했다. `get_account_info` source-of-record 기준 cash는 `30,344.81 USD`, portfolio value는 `101,144.59 USD`, buying power는 `303,680.13 USD`였다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-17-1311-after-hours-autopilot-post-trade.json`

_Last updated: 2026-06-17 13:15 KST_

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-17-1251-after-hours-autopilot]]
- Open/new: 없음. scheduler-owned `1251` preflight `get_orders(status=open)` source-of-record 기준 open orders `0`건이었고, live `get_orders(status=open)` 기준도 `0`건이었다.
- Filled: 이번 cycle 신규 after-hours fill 없음. live `get_orders(status=all, after=2026-06-16T20:00:00-04:00)`와 `get_account_activities(activity_types=[FILL], after=2026-06-16T20:00:00-04:00)` 기준 same-session after-hours orders/fills 모두 `0`건이었다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler core preflight `get_all_positions` 기준 positions `33`건이었고, live `get_all_positions` 기준 count도 `33`건으로 유지됐다.
- Recent reconciliation scope: scheduler-owned `1251` core/research preflight를 source-of-record로 사용했고, 사용자가 같은 preflight의 passing account/positions/orders/asset/quote/spread rows를 submit-boundary evidence로 유지하라고 요구했으므로 live Alpaca continuity는 `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-16T20:00:00-04:00)/get_account_activities(activity_types=[FILL], after=2026-06-16T20:00:00-04:00)/get_watchlists/get_stock_latest_quote(feed=iex, symbols=QQQ,IONQ,AVGO)/get_stock_snapshot(feed=overnight, symbols=QQQ,IONQ,AVGO)`로만 제한했다. separate after-hours session submitted count는 `0/2`로 열려 있었지만 `QQQ` freshest shortlist quote도 age 약 `419.58분`, `IONQ`는 `440.16분`, `QBTS/JPM/PFE`는 `448.98-470.14분`, `AVGO/SO/RGTI` sell-trim 후보는 `451-470분대` stale quote와 wide spread로 submit path에 진입하지 못했다. `get_account_info` source-of-record 기준 cash는 `30,344.81 USD`, portfolio value는 `101,083.72 USD`, buying power는 `303,554.72 USD`였고 live continuity 기준 account `ACTIVE`, open orders `0`, watchlists `0`, `QQQ/IONQ/AVGO` quote timestamp parity와 overnight snapshot continuity도 재확인했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-17-1251-after-hours-autopilot-post-trade.json`

_Last updated: 2026-06-17 12:53 KST_

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-17-1231-after-hours-autopilot]]
- Open/new: 없음. scheduler-owned `1231` preflight `get_orders(status=open)` source-of-record 기준 open orders `0`건이었고, live `get_orders(status=open)` 기준도 `0`건이었다.
- Filled: 이번 cycle 신규 after-hours fill 없음. live `get_orders(status=all, after=2026-06-16T20:00:00-04:00)`와 `get_account_activities(activity_types=[FILL], after=2026-06-16T20:00:00-04:00)` 기준 same-session after-hours orders/fills 모두 `0`건이었다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler core preflight `get_all_positions` 기준 positions `33`건이었고, live `get_all_positions` 기준 count도 `33`건으로 유지됐다.
- Recent reconciliation scope: scheduler-owned `1231` core/research preflight를 source-of-record로 사용했고, 사용자가 같은 preflight의 passing account/positions/orders/asset/quote/spread rows를 submit-boundary evidence로 유지하라고 요구했으므로 live Alpaca continuity는 `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-16T20:00:00-04:00)/get_account_activities(activity_types=[FILL], after=2026-06-16T20:00:00-04:00)/get_watchlists/get_stock_latest_quote(feed=iex, symbols=QQQ,IONQ,AVGO)/get_stock_snapshot(feed=overnight, symbols=QQQ,IONQ,AVGO)`로만 제한했다. separate after-hours session submitted count는 `0/2`로 열려 있었지만 `QQQ` freshest shortlist quote도 age 약 `399.58분`, `IONQ`는 `420.16분`, `QBTS/JPM/PFE`는 `429.31-450.48분`, `AVGO/SO/RGTI` sell-trim 후보는 `430-451분대` stale quote와 wide spread로 submit path에 진입하지 못했다. `get_account_info` source-of-record 기준 cash는 `30,344.81 USD`, portfolio value는 `100,999.83 USD`, buying power는 `303,331.09 USD`였고 live continuity 기준 account `ACTIVE`, open orders `0`, watchlists `0`, `QQQ/IONQ/AVGO` quote timestamp parity와 overnight snapshot continuity도 재확인했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-17-1231-after-hours-autopilot-post-trade.json`

_Last updated: 2026-06-17 12:33 KST_

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-17-1211-after-hours-autopilot]]
- Open/new: 없음. scheduler-owned `1211` preflight `get_orders(status=open)` source-of-record 기준 open orders `0`건이었고, live `get_orders(status=open)` 기준도 `0`건이었다.
- Filled: 이번 cycle 신규 after-hours fill 없음. live `get_orders(status=all, after=2026-06-16T20:00:00-04:00)`와 `get_account_activities(activity_types=[FILL], after=2026-06-16T20:00:00-04:00)` 기준 same-session after-hours orders/fills 모두 `0`건이었다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler core preflight `get_all_positions` 기준 positions `33`건이었고, live `get_all_positions` 기준 count도 `33`건으로 유지됐다.
- Recent reconciliation scope: scheduler-owned `1211` core/research preflight를 source-of-record로 사용했고, 사용자가 같은 preflight의 passing account/positions/orders/asset/quote/spread rows를 submit-boundary evidence로 유지하라고 요구했으므로 live Alpaca continuity는 `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-16T20:00:00-04:00)/get_account_activities(activity_types=[FILL], after=2026-06-16T20:00:00-04:00)/get_watchlists/get_stock_latest_quote(feed=iex, symbols=QQQ,IONQ,AVGO)`로만 제한했다. separate after-hours session submitted count는 `0/2`로 열려 있었지만 `QQQ` freshest shortlist quote도 age 약 `379.51분`, `IONQ`는 `400.09분`, `QBTS/JPM/PFE`는 `409.25-430.41분`, `AVGO/SO/RGTI` sell-trim 후보는 `411-431분대` stale quote와 wide spread로 submit path에 진입하지 못했다. `get_account_info` source-of-record 기준 cash는 `30,344.81 USD`, portfolio value는 `101,014.78 USD`, buying power는 `303,372.95 USD`였고 live continuity 기준 account `ACTIVE`, open orders `0`, watchlists `0`, `QQQ/IONQ/AVGO` quote timestamp parity도 재확인했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-17-1211-after-hours-autopilot-post-trade.json`

_Last updated: 2026-06-17 12:13 KST_

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-17-1151-after-hours-autopilot]]
- Open/new: 없음. scheduler-owned `1151` preflight `get_orders(status=open)` source-of-record 기준 open orders `0`건이었고, live `get_orders(status=open)` 기준도 `0`건이었다.
- Filled: 이번 cycle 신규 after-hours fill 없음. live `get_orders(status=all, after=2026-06-16T20:00:00-04:00)`와 `get_account_activities(activity_types=[FILL], after=2026-06-16T20:00:00-04:00)` 기준 same-session after-hours orders/fills 모두 `0`건이었다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler core preflight `get_all_positions` 기준 positions `33`건이었고, live `get_all_positions` 기준 count도 `33`건으로 유지됐다.
- Recent reconciliation scope: scheduler-owned `1151` core/research preflight를 source-of-record로 사용했고, 사용자가 같은 preflight의 passing account/positions/orders/asset/quote/spread rows를 submit-boundary evidence로 유지하라고 요구했으므로 live Alpaca continuity는 `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-16T20:00:00-04:00)/get_account_activities(activity_types=[FILL], after=2026-06-16T20:00:00-04:00)/get_watchlists/get_stock_latest_quote(feed=iex, symbols=QQQ,IONQ,AVGO)`로만 제한했다. separate after-hours session submitted count는 `0/2`로 열려 있었지만 `QQQ` freshest shortlist quote도 age 약 `359.85분`, `IONQ`는 `380.43분`, `QBTS/JPM/PFE`는 `389.25-410.41분`, `AVGO/SO/RGTI` sell-trim 후보는 `411분대` stale quote와 wide spread로 submit path에 진입하지 못했다. `get_account_info` source-of-record 기준 cash는 `30,344.81 USD`, portfolio value는 `101,013.82 USD`, buying power는 `303,392.77 USD`였고 live continuity 기준 account `ACTIVE`, open orders `0`, watchlists `0`, `QQQ/AVGO` quote timestamp parity도 재확인했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-17-1151-after-hours-autopilot-post-trade.json`

_Last updated: 2026-06-17 11:53 KST_

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-17-1131-after-hours-autopilot]]
- Open/new: 없음. scheduler-owned `1131` preflight `get_orders(status=open)` source-of-record 기준 open orders `0`건이었고, live `get_orders(status=open)` 기준도 `0`건이었다.
- Filled: 이번 cycle 신규 after-hours fill 없음. live `get_orders(status=all, after=2026-06-16T20:00:00-04:00)`와 `get_account_activities(activity_types=[FILL], after=2026-06-16T20:00:00-04:00)` 기준 same-session after-hours orders/fills 모두 `0`건이었다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler core preflight `get_all_positions` 기준 positions `33`건이었고, live `get_all_positions` 기준 count도 `33`건으로 유지됐다.
- Recent reconciliation scope: scheduler-owned `1131` core/research preflight를 source-of-record로 사용했고, 사용자가 같은 preflight의 passing account/positions/orders/asset/quote/spread rows를 submit-boundary evidence로 유지하라고 요구했으므로 live Alpaca continuity는 `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-16T20:00:00-04:00)/get_account_activities(activity_types=[FILL], after=2026-06-16T20:00:00-04:00)/get_watchlists/get_stock_latest_quote(feed=iex, symbols=QQQ,AVGO)`로만 제한했다. separate after-hours session submitted count는 `0/2`로 열려 있었지만 `QQQ` freshest shortlist quote도 age 약 `339.60분`, `IONQ`는 `360.18분`, `QBTS/JPM/PFE`는 `369.00-390.17분`, `AVGO/SO/RGTI` sell-trim 후보는 `391분대` stale quote와 wide spread로 submit path에 진입하지 못했다. `get_account_info` source-of-record 기준 cash는 `30,344.81 USD`, portfolio value는 `101,048.47 USD`, buying power는 `303,444.77 USD`였고 live continuity 기준 account `ACTIVE`, open orders `0`, watchlists `0`, `QQQ/AVGO` quote timestamp parity도 재확인했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-17-1131-after-hours-autopilot-post-trade.json`

_Last updated: 2026-06-17 11:35 KST_

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-17-1111-after-hours-autopilot]]
- Open/new: 없음. scheduler-owned `1111` preflight `get_orders(status=open)` source-of-record 기준 open orders `0`건이었다.
- Filled: 이번 cycle 신규 after-hours fill 없음. scheduler-owned `1111` preflight `get_account_activities(activity_types=[FILL])` 기준 cutoff `2026-06-16T20:00:00-04:00` 이후 same-session after-hours fill `0`건이었다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler core preflight `get_all_positions` 기준 positions `33`건이었고, live `get_all_positions` 기준 count도 `33`건으로 유지됐다.
- Recent reconciliation scope: scheduler-owned `1111` core/research preflight를 source-of-record로 사용했고, 사용자가 같은 preflight의 passing account/positions/orders/asset/quote/spread rows를 submit-boundary evidence로 유지하라고 요구했으므로 live Alpaca continuity는 `get_all_positions/get_watchlists/get_stock_latest_quote(feed=iex, symbols=QQQ,AVGO)` parity 확인으로만 제한했다. separate after-hours session submitted count는 `0/2`로 열려 있었지만 `QQQ` freshest shortlist quote도 age 약 `319.86분`, `IONQ`는 `340.44분`, `QBTS/JPM/PFE`는 `349.26-370.43분`, `AVGO/SO/RGTI` sell-trim 후보는 `371분대` stale quote와 wide spread로 submit path에 진입하지 못했다. `get_account_info` source-of-record 기준 cash는 `30,344.81 USD`, portfolio value는 `101,017.50 USD`, buying power는 `303,380.57 USD`였고 live `get_watchlists` 기준 watchlists `0`건, `QQQ`/`AVGO` quote timestamp parity도 재확인했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-17-1111-after-hours-autopilot-post-trade.json`

_Last updated: 2026-06-17 11:13 KST_

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-17-1051-after-hours-autopilot]]
- Open/new: 없음. scheduler-owned `1051` preflight `get_orders(status=open)` source-of-record 기준 open orders `0`건이었고, live `get_orders(status=open)` 기준도 `0`건이었다.
- Filled: 이번 cycle 신규 after-hours fill 없음. live `get_orders(status=all, after=2026-06-16T20:00:00-04:00)` 기준 same-session after-hours orders `0`건이었고, scheduler-owned `1051` preflight `get_account_activities(activity_types=[FILL])`에서는 `20:00 ET` 이후 after-hours fill이 `0`건이었다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler core preflight `get_all_positions` 기준 positions `33`건이었고, live `get_all_positions` 기준 count도 `33`건으로 유지됐다.
- Recent reconciliation scope: scheduler-owned `1051` core/research preflight를 source-of-record로 사용했고, 사용자가 같은 preflight의 passing account/positions/orders/asset/quote/spread rows를 submit-boundary evidence로 유지하라고 요구했으므로 live Alpaca continuity는 `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-16T20:00:00-04:00)/get_watchlists`로만 제한했다. separate after-hours session submitted count는 `0/2`로 열려 있었지만 `QQQ` freshest shortlist quote도 age 약 `299.55분`, `IONQ`는 `320.13분`, `QBTS/JPM/PFE`는 `328.95-350.12분`, `AVGO/SO/RGTI` sell-trim 후보는 `351분대` stale quote와 wide spread로 submit path에 진입하지 못했다. `get_account_info` source-of-record 기준 cash는 `30,344.81 USD`, portfolio value는 `100,983.53 USD`, buying power는 `303,319.20 USD`였고 live continuity 기준 portfolio value `100,986.65 USD`, buying power `303,327.96 USD`, watchlists `0`건도 재확인했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-17-1051-after-hours-autopilot-post-trade.json`

_Last updated: 2026-06-17 10:54 KST_

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-17-1031-after-hours-autopilot]]
- Open/new: 없음. scheduler-owned `1031` preflight `get_orders(status=open)` source-of-record 기준 open orders `0`건이었다.
- Filled: 이번 cycle 신규 after-hours fill 없음. scheduler-owned `1031` preflight `get_account_activities(activity_types=[FILL])` 기준 cutoff `2026-06-16T20:00:00-04:00` 이후 same-session after-hours fill `0`건이었고, live `get_account_activities` continuity 기준도 `0`건이었다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler core preflight `get_all_positions` 기준 positions `33`건이었고, live `get_all_positions` 기준 count도 `33`건으로 유지됐다.
- Recent reconciliation scope: scheduler-owned `1031` core/research preflight를 source-of-record로 사용했고, 사용자가 같은 preflight의 passing account/positions/orders/asset/quote/spread rows를 submit-boundary evidence로 유지하라고 요구했으므로 live Alpaca continuity는 `get_clock/get_account_info/get_all_positions/get_watchlists/get_account_activities(activity_types=[FILL], after=2026-06-16T20:00:00-04:00)`로만 제한했다. separate after-hours session submitted count는 `0/2`로 열려 있었지만 `QQQ` freshest shortlist quote도 age 약 `279.56분`, `IONQ`는 `300.14분`, `QBTS/JPM/PFE`는 `308.96-330.13분`, `AVGO/SO/RGTI` sell-trim 후보는 `331분대` stale quote와 wide spread로 submit path에 진입하지 못했다. `get_account_info` source-of-record 기준 cash는 `30,344.81 USD`, portfolio value는 `101,000.40 USD`였고 live continuity 기준 portfolio value `101,006.74 USD`, buying power `303,384.19 USD`, watchlists `0`건도 재확인했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-17-1031-after-hours-autopilot-post-trade.json`

_Last updated: 2026-06-17 10:34 KST_

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-17-1011-after-hours-autopilot]]
- Open/new: 없음. scheduler-owned `1011` preflight `get_orders(status=open)` source-of-record 기준 open orders `0`건이었다.
- Filled: 이번 cycle 신규 after-hours fill 없음. scheduler-owned `1011` preflight `get_account_activities(activity_types=[FILL])` 기준 cutoff `2026-06-16T20:00:00-04:00` 이후 same-session after-hours fill `0`건이었다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler core preflight `get_all_positions` 기준 positions `33`건이었다.
- Recent reconciliation scope: scheduler-owned `1011` core/research preflight를 source-of-record로 사용했고, 사용자가 같은 preflight의 passing account/positions/orders/asset/quote/spread rows를 submit-boundary evidence로 유지하라고 요구했으므로 live Alpaca continuity는 `get_clock/get_account_info/get_stock_latest_quote(feed=iex)/get_stock_snapshot(feed=iex)`로만 제한했다. separate after-hours session submitted count는 `0/2`로 열려 있었지만 `QQQ` freshest shortlist quote도 age 약 `259.59분`, `IONQ`는 `280.17분`, `QBTS/JPM/PFE`는 `288.99-310.15분`, `AVGO/SO/RGTI` sell-trim 후보는 `311분대` stale quote와 wide spread로 submit path에 진입하지 못했다. `get_account_info` source-of-record 기준 cash는 `30,344.81 USD`, portfolio value는 `100,909.53 USD`였고 live continuity 기준 portfolio value `100,903.59 USD`와 buying power `303,072.86 USD`도 재확인했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-17-1011-after-hours-autopilot-post-trade.json`

_Last updated: 2026-06-17 10:15 KST_

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-17-0951-after-hours-autopilot]]
- Open/new: 없음. scheduler-owned `0951` preflight `get_orders(status=open)` 기준 open orders `0`건이었고, live `get_orders(status=open)` 기준도 `0`건이었다.
- Filled: 이번 cycle 신규 after-hours fill 없음. live `get_orders(status=all, after=2026-06-16T20:00:00-04:00)`와 `get_account_activities(activity_types=[FILL], after=2026-06-16T20:00:00-04:00)` 기준 same-session after-hours orders/fills 모두 `0`건이었다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler core preflight `get_all_positions` 기준 positions `33`건이었고, live `get_all_positions` 기준 count도 `33`건으로 유지됐다.
- Recent reconciliation scope: scheduler-owned `0951` core/research preflight를 source-of-record로 사용했고, 사용자가 같은 preflight의 passing account/positions/orders/asset/quote/spread rows를 submit-boundary evidence로 유지하라고 요구했으므로 live Alpaca continuity는 `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-16T20:00:00-04:00)/get_account_activities(activity_types=[FILL], after=2026-06-16T20:00:00-04:00)/get_watchlists`로만 제한했다. separate after-hours session submitted count는 `0/2`로 열려 있었지만 `QQQ` freshest shortlist quote도 age 약 `242.05분`, `IONQ`는 `262.63분`, `QBTS/JPM/PFE`는 `271.45-292.62분`, `AVGO/SO/RGTI` sell-trim 후보는 `291분대` stale quote와 wide spread로 submit path에 진입하지 못했다. `get_account_info` source-of-record 기준 cash는 `30,344.81 USD`, portfolio value는 `100,877.66 USD`였고 live continuity 기준 watchlists `0`건, portfolio value `100,850.17 USD`도 재확인했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-17-0951-after-hours-autopilot-post-trade.json`

_Last updated: 2026-06-17 09:53 KST_

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-17-0931-after-hours-autopilot]]
- Open/new: 없음. scheduler-owned `0931` preflight `get_orders(status=open)` 기준 open orders `0`건이었고, live `get_orders(status=open)` 기준도 `0`건이었다.
- Filled: 이번 cycle 신규 after-hours fill 없음. live `get_orders(status=all, after=2026-06-16T20:00:00-04:00)` 기준 same-session after-hours orders/fills 모두 `0`건이었다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler core preflight `get_all_positions` 기준 positions `33`건이었고, live `get_all_positions` 기준 count도 `33`건으로 유지됐다.
- Recent reconciliation scope: scheduler-owned `0931` core/research preflight를 source-of-record로 사용했고, 사용자가 같은 preflight의 passing account/positions/orders/asset/quote/spread rows를 submit-boundary evidence로 유지하라고 요구했으므로 live Alpaca continuity는 `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-16T20:00:00-04:00)/get_watchlists`로만 제한했다. separate after-hours session submitted count는 `0/2`로 열려 있었지만 `QQQ` freshest shortlist quote도 age 약 `222.29분`, `IONQ`는 `242.87분`, `QBTS/JPM/PFE`는 `251.69-272.86분`, `AVGO/SO/RGTI` sell-trim 후보는 `274분대` stale quote와 wide spread로 submit path에 진입하지 못했다. `get_account_info` source-of-record 기준 cash는 `30,344.81 USD`, portfolio value는 `100,893.26 USD`였고 live continuity 기준 watchlists `0`건, portfolio value `100,914.39 USD`도 재확인했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-17-0931-after-hours-autopilot-post-trade.json`

_Last updated: 2026-06-17 09:33 KST_

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-17-0911-after-hours-autopilot]]
- Open/new: 없음. scheduler-owned `0911` preflight `get_orders(status=open)` 기준 open orders `0`건이었고, live `get_orders(status=open)` 기준도 `0`건이었다.
- Filled: 이번 cycle 신규 after-hours fill 없음. live `get_orders(status=all, after=2026-06-16T20:00:00-04:00)`와 `get_account_activities(activity_types=[FILL], after=2026-06-16T20:00:00-04:00)` 기준 same-session after-hours orders/fills 모두 `0`건이었다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler core preflight `get_all_positions` 기준 positions `33`건이었고, live `get_all_positions` 기준 count도 `33`건으로 유지됐다.
- Recent reconciliation scope: scheduler-owned `0911` core/research preflight를 source-of-record로 사용했고, 사용자가 같은 preflight의 passing account/positions/orders/asset/quote/spread rows를 submit-boundary evidence로 유지하라고 요구했으므로 live Alpaca continuity는 `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-16T20:00:00-04:00)/get_account_activities(activity_types=[FILL], after=2026-06-16T20:00:00-04:00)/get_watchlists`로만 제한했다. separate after-hours session submitted count는 `0/2`로 열려 있었지만 `QQQ` freshest shortlist quote도 age 약 `199.56분`, `IONQ`는 `220.14분`, `QBTS/JPM/PFE`는 `228.96-250.12분`, `AVGO/SO/RGTI` sell-trim 후보는 `251분대` stale quote와 wide spread로 submit path에 진입하지 못했다. `get_account_info` source-of-record 기준 cash는 `30,344.81 USD`, portfolio value는 `100,812.42 USD`였고 live continuity 기준 watchlists `0`건, portfolio value `100,831.88 USD`도 재확인했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-17-0911-after-hours-autopilot-post-trade.json`

_Last updated: 2026-06-17 09:13 KST_

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-17-0831-after-hours-autopilot]]
- Open/new: 없음. scheduler-owned `0831` preflight `get_orders(status=open)` 기준 open orders `0`건이었고, live `get_orders(status=open)` 기준도 `0`건이었다.
- Filled: 이번 cycle 신규 after-hours fill 없음. live `get_orders(status=all, after=2026-06-16T20:00:00-04:00)`와 `get_account_activities(activity_types=[FILL], after=2026-06-16T20:00:00-04:00)` 기준 same-session after-hours orders/fills 모두 `0`건이었다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler core preflight `get_all_positions` 기준 positions `33`건이었고, live `get_all_positions` 기준 count도 `33`건으로 유지됐다.
- Recent reconciliation scope: scheduler-owned `0831` core/research preflight를 source-of-record로 사용했고, 사용자가 같은 preflight의 passing account/positions/orders/asset/quote/spread rows를 submit-boundary evidence로 유지하라고 요구했으므로 live Alpaca continuity는 `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-16T20:00:00-04:00)/get_account_activities(activity_types=[FILL], after=2026-06-16T20:00:00-04:00)/get_watchlists`로만 제한했다. separate after-hours session submitted count는 `0/2`로 열려 있었지만 `QQQ` freshest shortlist quote도 age 약 `159.56분`, `IONQ`는 `180.14분`, `QBTS/JPM/PFE`는 `188.96-210.13분`, `AVGO/SO/RGTI` sell-trim 후보는 `211분대` stale quote와 wide spread로 submit path에 진입하지 못했다. `get_account_info` source-of-record 기준 cash는 `30,344.81 USD`, portfolio value는 `100,699.91 USD`였고 live continuity 기준 watchlists `0`건, portfolio value `100,706.83 USD`도 재확인했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-17-0831-after-hours-autopilot-post-trade.json`

_Last updated: 2026-06-17 08:33 KST_

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-17-0811-after-hours-autopilot]]
- Open/new: 없음. scheduler-owned `0811` preflight `get_orders(status=open)` 기준 open orders `0`건이었다.
- Filled: 이번 cycle 신규 after-hours fill 없음. submit boundary를 다시 열지 않았고 scheduler-owned preflight 기준 same-session after-hours fill은 `0`건으로 유지했다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler core preflight `get_all_positions` 기준 positions `33`건이었다.
- Recent reconciliation scope: scheduler-owned `0811` core/research preflight를 source-of-record로 사용했고, 사용자가 같은 preflight의 passing account/positions/orders/asset/quote/spread rows를 submit-boundary evidence로 유지하라고 요구했으므로 fresh live quote refresh나 추가 live continuity 없이 해당 row를 그대로 썼다. separate after-hours session submitted count는 `0/2`로 열려 있었지만 `QQQ` freshest shortlist quote도 age 약 `139.95분`, `IONQ`는 `160.53분`, `QBTS/JPM/PFE`는 `169.35-190.51분`, `AVGO/SO/RGTI` sell-trim 후보는 `191분대` stale quote와 wide spread로 submit path에 진입하지 못했다. `get_account_info` source-of-record 기준 cash는 `30,344.81 USD`, portfolio value는 `100,724.03 USD`였고 watchlists는 `0`건이었다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-17-0811-after-hours-autopilot-post-trade.json`

_Last updated: 2026-06-17 08:11 KST_

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-17-0751-after-hours-autopilot]]
- Open/new: 없음. scheduler-owned `0751` preflight `get_orders(status=open)` 기준 open orders `0`건이었고, live `get_orders(status=open)` 기준도 `0`건이었다.
- Filled: 이번 cycle 신규 after-hours fill 없음. live `get_account_activities(activity_types=[FILL], after=2026-06-16T20:00:00-04:00)` 기준 same-session fill `0`건이었다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler core preflight `get_all_positions` 기준 positions `33`건이었고, live `get_all_positions` 기준 count도 `33`건으로 유지됐다.
- Recent reconciliation scope: scheduler-owned `0751` core/research preflight를 source-of-record로 사용했고, 사용자가 같은 preflight의 passing account/positions/orders/asset/quote/spread rows를 submit-boundary evidence로 유지하라고 요구했으므로 fresh live quote refresh 없이 해당 row를 그대로 썼다. live continuity는 `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-16T20:00:00-04:00)/get_account_activities(activity_types=[FILL], after=2026-06-16T20:00:00-04:00)/get_watchlists`로만 제한했다. separate after-hours session submitted count는 `0/2`로 열려 있었지만 `QQQ` freshest shortlist quote도 age 약 `119.85분`, `IONQ`는 `140.43분`, `QBTS/JPM/PFE`는 `149.25-170.41분`, `AVGO/SO/RGTI` sell-trim 후보는 `171분대` stale quote와 wide spread로 submit path에 진입하지 못했다. `get_account_info` source-of-record 기준 cash는 `30,344.81 USD`, portfolio value는 `100,762.33 USD`였고 live `get_watchlists` 기준 watchlists `0`건도 재확인했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-17-0751-after-hours-autopilot-post-trade.json`

_Last updated: 2026-06-17 07:51 KST_

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-17-0731-after-hours-autopilot]]
- Open/new: 없음. scheduler-owned `0731` preflight `get_orders(status=open)` 기준 open orders `0`건이었고, live `get_orders(status=open)` 기준도 `0`건이었다.
- Filled: 이번 cycle 신규 after-hours fill 없음. live `get_account_activities(activity_types=[FILL], after=2026-06-16T20:00:00-04:00)` 기준 same-session fill `0`건이었다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler core preflight `get_all_positions` 기준 positions `33`건이었고, live `get_all_positions` 기준 count도 `33`건으로 유지됐다.
- Recent reconciliation scope: scheduler-owned `0731` core/research preflight를 source-of-record로 사용했고, 사용자가 같은 preflight의 passing account/positions/orders/asset/quote/spread rows를 submit-boundary evidence로 유지하라고 요구했으므로 fresh live quote refresh 없이 해당 row를 그대로 썼다. live continuity는 `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_account_activities(activity_types=[FILL], after=2026-06-16T20:00:00-04:00)/get_watchlists`로만 제한했다. separate after-hours session submitted count는 `0/2`로 열려 있었지만 `QQQ` freshest shortlist quote도 age 약 `99.98분`, `IONQ`는 `120.56분`, `QBTS/JPM/PFE`는 `129.38-150.55분`, `AVGO/SO/RGTI` sell-trim 후보는 `151분대` stale quote와 wide spread로 submit path에 진입하지 못했다. `get_account_info` source-of-record 기준 cash는 `30,344.81 USD`, portfolio value는 `100,761.09 USD`였고 live `get_watchlists` 기준 watchlists `0`건도 재확인했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-17-0731-after-hours-autopilot-post-trade.json`

_Last updated: 2026-06-17 07:31 KST_

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-17-0711-after-hours-autopilot]]
- Open/new: 없음. scheduler-owned `0711` preflight `get_orders(status=open)` 기준 open orders `0`건이었다.
- Filled: 이번 cycle 신규 after-hours fill 없음. `2026-06-16T20:00:00Z` 이후 same-session after-hours fill은 source-of-record preflight에서 관측되지 않았다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler core preflight `get_all_positions` 기준 positions `33`건이었고, live `get_all_positions` 기준 count도 `33`건으로 유지됐다.
- Recent reconciliation scope: scheduler-owned `0711` core/research preflight를 source-of-record로 사용했고, 사용자가 같은 preflight의 passing account/positions/orders/asset/quote/spread rows를 submit-boundary evidence로 유지하라고 요구했으므로 fresh live quote refresh 없이 해당 row를 그대로 썼다. live continuity는 `get_clock/get_all_positions/get_watchlists`로만 제한했다. separate after-hours session submitted count는 `0/2`로 열려 있었지만 `QQQ` freshest shortlist quote도 age 약 `79.88분`, `IONQ`는 `100.46분`, `QBTS/JPM/PFE`는 `109.28-130.45분`, `AVGO/SO/RGTI` sell-trim 후보는 `131분대` stale quote와 wide spread로 submit path에 진입하지 못했다. `get_account_info` source-of-record 기준 cash는 `30,344.81 USD`, portfolio value는 `100,716.67 USD`였고 live `get_watchlists` 기준 watchlists `0`건도 재확인했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-17-0711-after-hours-autopilot-post-trade.json`

_Last updated: 2026-06-17 07:11 KST_

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-17-0651-after-hours-autopilot]]
- Open/new: 없음. scheduler-owned `0651` preflight `get_orders(status=open)` 기준 open orders `0`건이었다.
- Filled: 이번 cycle 신규 after-hours fill 없음. `2026-06-16T20:00:00Z` 이후 same-session after-hours fill은 source-of-record preflight에서 관측되지 않았다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler core preflight `get_all_positions` 기준 positions `33`건이었고, live `get_all_positions` 기준 count도 `33`건으로 유지됐다.
- Recent reconciliation scope: scheduler-owned `0651` core/research preflight를 source-of-record로 사용했고, 사용자가 같은 preflight의 passing account/positions/orders/asset/quote/spread rows를 submit-boundary evidence로 유지하라고 요구했으므로 fresh live quote refresh 없이 해당 row를 그대로 썼다. live continuity는 `get_clock/get_all_positions/get_watchlists`로만 제한했다. separate after-hours session submitted count는 `0/2`로 열려 있었지만 `QQQ` freshest shortlist quote도 age 약 `60.00분`, `IONQ`는 `80.58분`, `QBTS/JPM/PFE`는 `89.40-110.56분`, `AVGO/SO/RGTI` sell-trim 후보는 `111분대` stale quote와 wide spread로 submit path에 진입하지 못했다. `get_account_info` source-of-record 기준 cash는 `30,344.81 USD`, portfolio value는 `100,710.76 USD`였고 live `get_watchlists` 기준 watchlists `0`건도 재확인했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-17-0651-after-hours-autopilot-post-trade.json`

_Last updated: 2026-06-17 06:51 KST_

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-17-0631-after-hours-autopilot]]
- Open/new: 없음. scheduler-owned `0631` preflight `get_orders(status=open)` 기준 open orders `0`건이었다.
- Filled: 이번 cycle 신규 after-hours fill 없음. `2026-06-16T20:00:00Z` 이후 same-session after-hours fill은 관측되지 않았다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler core preflight `get_all_positions` 기준 positions `33`건이었다.
- Recent reconciliation scope: scheduler-owned `0631` core/research preflight를 source-of-record로 사용했고, 사용자가 같은 preflight의 passing account/positions/orders/asset/quote/spread rows를 submit-boundary evidence로 유지하라고 요구했으므로 fresh live quote refresh 없이 해당 row를 그대로 썼다. separate after-hours session submitted count는 `0/2`로 열려 있었지만 `QQQ` freshest shortlist quote도 age 약 `39.85분`, `IONQ`는 `60.43분`, `QBTS/JPM/PFE`는 `69.25-90.41분`, `AVGO/SO/RGTI` sell-trim 후보는 `91분대` stale quote와 wide spread로 submit path에 진입하지 못했다. `get_account_info` 기준 cash는 `30,344.81 USD`, portfolio value는 `100,755.12 USD`였다. live `get_watchlists` 기준 watchlists `0`건도 재확인했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-17-0631-after-hours-autopilot-post-trade.json`

_Last updated: 2026-06-17 06:31 KST_

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-17-0611-after-hours-autopilot]]
- Open/new: 없음. live `get_orders(status=open)` 기준 open orders `0`건이었다.
- Filled: 이번 cycle 신규 after-hours fill 없음. live `get_account_activities(activity_types=[FILL], after=2026-06-16T20:00:00Z)` 기준 same-session fill `0`건이었다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: live `get_all_positions` 기준 positions `33`건, live `get_watchlists` 기준 watchlists `0`건이었다.
- Recent reconciliation scope: scheduler-owned `0611` core/research preflight를 source-of-record로 사용했고 live Alpaca `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-16T20:00:00Z)/get_account_activities(activity_types=[FILL], after=2026-06-16T20:00:00Z)/get_watchlists/get_stock_latest_quote(feed=iex|overnight)`로 continuity를 다시 열었다. after-hours separate session submitted count는 `0/2`로 열려 있었지만 `QQQ` freshest IEX quote도 age 약 `21.26분`, `IONQ`는 `41.84분`, `QBTS/JPM/PFE`는 `50.66-71.83분`, `AVGO/SO/RGTI` sell-trim 후보는 `72분대` stale quote와 wide spread로 submit path에 진입하지 못했다. `get_account_info` 기준 cash는 `30,344.81 USD`, portfolio value는 `100,701.96 USD`였다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-17-0611-after-hours-autopilot-post-trade.json`

_Last updated: 2026-06-17 06:18 KST_

# portfolio-current

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-17-0451-hourly-autopilot]]
- Open/new: 없음. scheduler-owned `0451` preflight `get_orders_open` 기준 open orders `0`건이었다.
- Filled: 이번 cycle 신규 fill 없음. same-day fill history는 `SO` sell 1건, `PFE` sell 1건, `AVGO` sell 1건만 유지됐다.
- Cancelled: 신규 취소 없음. `RGTI` same-day sell 7주는 earlier `0011` runtime recheck 기준 `canceled` 상태를 유지했고 duplicate-side blocker로만 재사용했다.
- Position count observed by Alpaca MCP: scheduler core preflight `get_all_positions` 기준 positions `33`건, `get_orders_open` 기준 open orders `0`건이었다.
- Recent reconciliation scope: scheduler-owned `0451` stale cleanup/core/research preflight를 source-of-record로 사용했고, quote rows가 decision time 기준 20분 이내라 추가 live Alpaca read-only call 없이 preflight submit boundary를 재사용했다. `SO`는 preflight quote `93.76/94.34` spread `0.6167%`가 policy cap `0.50%`를 넘어 trim gate를 먼저 닫았고, `PFE`는 same-day sell fill이 이미 있어 duplicate symbol/side discipline에 막혔다. `RGTI`는 `0011` cycle에서 확인된 same-day canceled sell history가 계속 duplicate blocker로 남았다. buy fallback에서는 `NEE/WMT/NKE/SLB`가 review backlog throttle에 막혔고 `SPY/QQQ`는 validation floor cap 초과, `NOK`는 lifecycle add-block 때문에 no-submit으로 종료했다. `get_account_info` 기준 cash는 `30,344.81 USD`, portfolio value는 `100,758.65 USD`였다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-17-0451-hourly-autopilot-post-trade.json`

_Last updated: 2026-06-17 04:54 KST_

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-17-0431-hourly-autopilot]]
- Open/new: 없음. scheduler-owned `0431` preflight `get_orders_open` 기준 open orders `0`건이었다.
- Filled: 이번 cycle 신규 fill 없음. same-day fill history는 `SO` sell 1건, `PFE` sell 1건, `AVGO` sell 1건만 유지됐다.
- Cancelled: 신규 취소 없음. `RGTI` same-day sell 7주는 earlier `0011` runtime recheck 기준 `canceled` 상태를 유지했고 duplicate-side blocker로만 재사용했다.
- Position count observed by Alpaca MCP: scheduler core preflight `get_all_positions` 기준 positions `33`건, `get_orders_open` 기준 open orders `0`건이었다.
- Recent reconciliation scope: scheduler-owned `0431` stale cleanup/core/research preflight를 source-of-record로 사용했고, quote rows가 decision time 기준 20분 이내라 추가 live Alpaca read-only call 없이 preflight submit boundary를 재사용했다. `SO`는 preflight quote `94.04/94.07` spread `0.0319%`로 trim gate를 통과했지만 same-day `SO` sell fill이 이미 있어 duplicate symbol/side discipline에 막혔고, `PFE`도 같은 duplicate gate를 유지했다. `RGTI`는 `0011` cycle에서 확인된 same-day canceled sell history가 계속 duplicate blocker로 남았다. buy fallback에서는 `NEE/WMT/NKE/SLB`가 review backlog throttle에 막혔고 `SPY/QQQ`는 validation floor cap 초과, `NOK`는 lifecycle add-block 때문에 no-submit으로 종료했다. `get_account_info` 기준 cash는 `30,344.81 USD`, portfolio value는 `100,975.13 USD`였다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-17-0431-hourly-autopilot-post-trade.json`

_Last updated: 2026-06-17 04:34 KST_

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-17-0411-hourly-autopilot]]
- Open/new: 없음. scheduler-owned `0411` preflight `get_orders_open` 기준 open orders `0`건이었다.
- Filled: 이번 cycle 신규 fill 없음. same-day fill history는 `SO` sell 1건, `PFE` sell 1건, `AVGO` sell 1건만 유지됐다.
- Cancelled: 신규 취소 없음. `RGTI` same-day sell 7주는 earlier `0011` runtime recheck 기준 `canceled` 상태를 유지했고 duplicate-side blocker로만 재사용했다.
- Position count observed by Alpaca MCP: scheduler core preflight `get_all_positions` 기준 positions `33`건, `get_orders_open` 기준 open orders `0`건이었다.
- Recent reconciliation scope: scheduler-owned `0411` stale cleanup/core/research preflight를 source-of-record로 사용했고, quote rows가 decision time 기준 20분 이내라 추가 live Alpaca read-only call 없이 preflight submit boundary를 재사용했다. `SO`는 preflight quote `94.08/94.10` spread `0.0213%`로 trim gate를 통과했지만 same-day `SO` sell fill이 이미 있어 duplicate symbol/side discipline에 막혔고, `PFE`도 같은 duplicate gate를 유지했다. `RGTI`는 `0011` cycle에서 확인된 same-day canceled sell history가 계속 duplicate blocker로 남았다. buy fallback에서는 `NEE/WMT/NKE/SLB`가 review backlog throttle에 막혔고 `SPY/QQQ`는 validation floor cap 초과, `NOK`는 lifecycle add-block 때문에 no-submit으로 종료했다. `get_account_info` 기준 cash는 `30,344.81 USD`, portfolio value는 `100,876.82 USD`였다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-17-0411-hourly-autopilot-post-trade.json`

_Last updated: 2026-06-17 04:18 KST_

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-17-0351-hourly-autopilot]]
- Open/new: 없음. scheduler-owned `0351` preflight `get_orders_open` 기준 open orders `0`건이었다.
- Filled: 이번 cycle 신규 fill 없음. same-day fill history는 `SO` sell 1건, `PFE` sell 1건, `AVGO` sell 1건만 유지됐다.
- Cancelled: 신규 취소 없음. `RGTI` same-day sell 7주는 earlier `0011` runtime recheck 기준 `canceled` 상태를 유지했고 duplicate-side blocker로만 재사용했다.
- Position count observed by Alpaca MCP: scheduler core preflight `get_all_positions` 기준 positions `33`건, `get_orders_open` 기준 open orders `0`건이었다.
- Recent reconciliation scope: scheduler-owned `0351` stale cleanup/core/research preflight를 source-of-record로 사용했고, quote rows가 decision time 기준 20분 이내라 추가 live Alpaca read-only call 없이 preflight submit boundary를 재사용했다. `SO`는 preflight quote `94.22/94.24` spread `0.0212%`로 trim gate를 통과했지만 same-day `SO` sell fill이 이미 있어 duplicate symbol/side discipline에 막혔고, `PFE`도 같은 duplicate gate를 유지했다. `RGTI`는 `0011` cycle에서 확인된 same-day canceled sell history가 계속 duplicate blocker로 남았다. buy fallback에서는 `NEE/WMT/NKE/SLB`가 review backlog throttle에 막혔고 `SPY/QQQ`는 validation floor cap 초과, `NOK`는 lifecycle add-block 때문에 no-submit으로 종료했다. `get_account_info` 기준 cash는 `30,344.81 USD`, portfolio value는 `100,998.06 USD`였다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-17-0351-hourly-autopilot-post-trade.json`

_Last updated: 2026-06-17 03:54 KST_

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-17-0331-hourly-autopilot]]
- Open/new: 없음. scheduler-owned `0331` preflight `get_orders_open` 기준 open orders `0`건이었다.
- Filled: 이번 cycle 신규 fill 없음. same-day fill history는 `SO` sell 1건, `PFE` sell 1건, `AVGO` sell 1건만 유지됐다.
- Cancelled: 신규 취소 없음. `RGTI` same-day sell 7주는 earlier `0011` runtime recheck 기준 `canceled` 상태를 유지했고 duplicate-side blocker로만 재사용했다.
- Position count observed by Alpaca MCP: scheduler core preflight `get_all_positions` 기준 positions `33`건, `get_orders_open` 기준 open orders `0`건이었다.
- Recent reconciliation scope: scheduler-owned `0331` stale cleanup/core/research preflight를 source-of-record로 사용했고, quote rows가 decision time 기준 20분 이내라 추가 live Alpaca read-only call 없이 preflight submit boundary를 재사용했다. `SO`는 preflight quote `94.35/94.37` spread `0.0212%`로 trim gate를 통과했지만 same-day `SO` sell fill이 이미 있어 duplicate symbol/side discipline에 막혔고, `PFE`도 같은 duplicate gate를 유지했다. `RGTI`는 `0011` cycle에서 확인된 same-day canceled sell history가 계속 duplicate blocker로 남았다. buy fallback에서는 `NEE/WMT/NKE/SLB`가 review backlog throttle에 막혔고 `SPY/QQQ`는 validation floor cap 초과, `NOK`는 lifecycle add-block 때문에 no-submit으로 종료했다. `get_account_info` 기준 cash는 `30,344.81 USD`, portfolio value는 `101,117.45 USD`였다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-17-0331-hourly-autopilot-post-trade.json`

_Last updated: 2026-06-17 03:34 KST_

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-17-0311-hourly-autopilot]]
- Open/new: 없음. scheduler-owned `0311` preflight `get_orders_open` 기준 open orders `0`건이었다.
- Filled: 이번 cycle 신규 fill 없음. same-day fill history는 `SO` sell 1건, `PFE` sell 1건, `AVGO` sell 1건만 유지됐다.
- Cancelled: 신규 취소 없음. `RGTI` same-day sell 7주는 earlier `0011` runtime recheck 기준 `canceled` 상태를 유지했고 duplicate-side blocker로만 재사용했다.
- Position count observed by Alpaca MCP: scheduler core preflight `get_all_positions` 기준 positions `33`건, `get_orders_open` 기준 open orders `0`건이었다.
- Recent reconciliation scope: scheduler-owned `0311` stale cleanup/core/research preflight를 source-of-record로 사용했고, quote rows가 decision time 기준 20분 이내라 추가 live Alpaca read-only call 없이 preflight submit boundary를 재사용했다. `SO`는 preflight quote `94.38/94.41` spread `0.0318%`로 trim gate를 통과했지만 same-day `SO` sell fill이 이미 있어 duplicate symbol/side discipline에 막혔고, `PFE`도 같은 duplicate gate를 유지했다. `RGTI`는 `0011` cycle에서 확인된 same-day canceled sell history가 계속 duplicate blocker로 남았다. buy fallback에서는 `NEE/WMT/NKE/SLB`가 review backlog throttle에 막혔고 `SPY/QQQ`는 validation floor cap 초과, `NOK`는 lifecycle add-block 때문에 no-submit으로 종료했다. `get_account_info` 기준 cash는 `30,344.81 USD`, portfolio value는 `101,188.48 USD`였다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-17-0311-hourly-autopilot-post-trade.json`

_Last updated: 2026-06-17 03:14 KST_

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-17-0251-hourly-autopilot]]
- Open/new: 없음. scheduler-owned `0251` preflight `get_orders_open` 기준 open orders `0`건이었다.
- Filled: 이번 cycle 신규 fill 없음. same-day fill history는 `SO` sell 1건, `PFE` sell 1건, `AVGO` sell 1건만 유지됐다.
- Cancelled: 신규 취소 없음. `RGTI` same-day sell 7주는 earlier `0011` runtime recheck 기준 `canceled` 상태를 유지했고 duplicate-side blocker로만 재사용했다.
- Position count observed by Alpaca MCP: scheduler core preflight `get_all_positions` 기준 positions `33`건, `get_orders_open` 기준 open orders `0`건이었다.
- Recent reconciliation scope: scheduler-owned `0251` stale cleanup/core/research preflight를 source-of-record로 사용했고, quote rows가 decision time 기준 20분 이내라 추가 live Alpaca read-only call 없이 preflight submit boundary를 재사용했다. `SO`는 preflight quote `94.45/94.47` spread `0.0212%`로 trim gate를 통과했지만 same-day `SO` sell fill이 이미 있어 duplicate symbol/side discipline에 막혔고, `PFE`도 같은 duplicate gate를 유지했다. `RGTI`는 `0011` cycle에서 확인된 same-day canceled sell history가 계속 duplicate blocker로 남았다. buy fallback에서는 `NEE/WMT/NKE/SLB`가 review backlog throttle에 막혔고 `SPY/QQQ`는 validation floor cap 초과, `NOK`는 lifecycle add-block 때문에 no-submit으로 종료했다. `get_account_info` 기준 cash는 `30,344.81 USD`, portfolio value는 `101,151.13 USD`였다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-17-0251-hourly-autopilot-post-trade.json`

_Last updated: 2026-06-17 02:53 KST_

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-17-0231-hourly-autopilot]]
- Open/new: 없음. scheduler-owned `0231` preflight `get_orders_open` 기준 open orders `0`건이었다.
- Filled: 이번 cycle 신규 fill 없음. same-day fill history는 `SO` sell 1건, `PFE` sell 1건, `AVGO` sell 1건만 유지됐다.
- Cancelled: 신규 취소 없음. `RGTI` same-day sell 7주는 earlier `0011` runtime recheck 기준 `canceled` 상태를 유지했고 duplicate-side blocker로만 재사용했다.
- Position count observed by Alpaca MCP: scheduler core preflight `get_all_positions` 기준 positions `33`건, `get_orders_open` 기준 open orders `0`건이었다.
- Recent reconciliation scope: scheduler-owned `0231` stale cleanup/core/research preflight를 source-of-record로 사용했고, quote rows가 decision time 기준 20분 이내라 추가 live Alpaca read-only call 없이 preflight submit boundary를 재사용했다. `SO`는 preflight quote `94.09/94.16` spread `0.0743%`로 trim gate를 통과했지만 same-day `SO` sell fill이 이미 있어 duplicate symbol/side discipline에 막혔고, `PFE`도 같은 duplicate gate를 유지했다. `RGTI`는 `0011` cycle에서 확인된 same-day canceled sell history가 계속 duplicate blocker로 남았다. buy fallback에서는 `NEE/WMT/NKE/SLB`가 review backlog throttle에 막혔고 `SPY/QQQ`는 validation floor cap 초과, `NOK`는 lifecycle add-block 때문에 no-submit으로 종료했다. `get_account_info` 기준 cash는 `30,344.81 USD`, portfolio value는 `101,102.87 USD`였다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-17-0231-hourly-autopilot-post-trade.json`

_Last updated: 2026-06-17 02:33 KST_

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-17-0211-hourly-autopilot]]
- Open/new: 없음. scheduler-owned `0211` preflight `get_orders_open` 기준 open orders `0`건이었다.
- Filled: 이번 cycle 신규 fill 없음. same-day fill history는 `SO` sell 1건, `PFE` sell 1건, `AVGO` sell 1건만 유지됐다.
- Cancelled: 신규 취소 없음. `RGTI` same-day sell 7주는 earlier `0011` runtime recheck 기준 `canceled` 상태를 유지했고 duplicate-side blocker로만 재사용했다.
- Position count observed by Alpaca MCP: scheduler core preflight `get_all_positions` 기준 positions `33`건, `get_orders_open` 기준 open orders `0`건이었다.
- Recent reconciliation scope: scheduler-owned `0211` stale cleanup/core/research preflight를 source-of-record로 사용했고, quote rows가 decision time 기준 20분 이내라 추가 live Alpaca read-only call 없이 preflight submit boundary를 재사용했다. `SO`는 preflight quote `94.27/94.30` spread `0.0318%`로 trim gate를 통과했지만 same-day `SO` sell fill이 이미 있어 duplicate symbol/side discipline에 막혔고, `PFE`도 같은 duplicate gate를 유지했다. `RGTI`는 `0011` cycle에서 확인된 same-day canceled sell history가 계속 duplicate blocker로 남았다. buy fallback에서는 `NEE/WMT/NKE/SLB`가 review backlog throttle에 막혔고 `SPY/QQQ`는 validation floor cap 초과, `NOK`는 lifecycle add-block 때문에 no-submit으로 종료했다. `get_account_info` 기준 cash는 `30,344.81 USD`, portfolio value는 `101,141.71 USD`였다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-17-0211-hourly-autopilot-post-trade.json`

_Last updated: 2026-06-17 02:12 KST_

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-17-0151-hourly-autopilot]]
- Open/new: 없음. scheduler-owned `0151` preflight `get_orders(status=open)` 기준 open orders `0`건이었다.
- Filled: 이번 cycle 신규 fill 없음. same-day fill history는 `SO` sell 1건, `PFE` sell 1건, `AVGO` sell 1건만 유지됐다.
- Cancelled: 신규 취소 없음. `RGTI` same-day sell 7주는 earlier `0011` runtime recheck 기준 `canceled` 상태를 유지했고 duplicate-side blocker로만 재사용했다.
- Position count observed by Alpaca MCP: scheduler core preflight `get_all_positions` 기준 positions `33`건, `get_orders(status=open)` 기준 open orders `0`건이었다.
- Recent reconciliation scope: scheduler-owned `0151` stale cleanup/core/research preflight를 source-of-record로 사용했고, quote rows가 decision time 기준 20분 이내라 추가 live Alpaca read-only call 없이 preflight submit boundary를 재사용했다. `SO`는 preflight quote `94.69/94.72` spread `0.0317%`로 trim gate를 통과했지만 same-day `SO` sell fill이 이미 있어 duplicate symbol/side discipline에 막혔고, `PFE`도 같은 duplicate gate를 유지했다. `RGTI`는 `0011` cycle에서 확인된 same-day canceled sell history가 계속 duplicate blocker로 남았다. buy fallback에서는 `NEE/WMT/NKE/SLB/COP/CVX`가 review backlog throttle에 막혔고 `SPY/QQQ`는 validation floor cap 초과, `NOK`는 lifecycle add-block 때문에 no-submit으로 종료했다. `get_account_info` 기준 cash는 `30,344.81 USD`, portfolio value는 `101,259.22 USD`였다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-17-0151-hourly-autopilot-post-trade.json`

_Last updated: 2026-06-17 01:52 KST_

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-17-0131-hourly-autopilot]]
- Open/new: 없음. scheduler-owned `0131` preflight `get_orders(status=open)` 기준 open orders `0`건이었다.
- Filled: 이번 cycle 신규 fill 없음. same-day fill history는 `SO` sell 1건, `PFE` sell 1건, `AVGO` sell 1건만 유지됐다.
- Cancelled: 신규 취소 없음. `RGTI` same-day sell 7주는 earlier `0011` runtime recheck 기준 `canceled` 상태를 유지했고 duplicate-side blocker로만 재사용했다.
- Position count observed by Alpaca MCP: scheduler core preflight `get_all_positions` 기준 positions `33`건, `get_orders(status=open)` 기준 open orders `0`건이었다.
- Recent reconciliation scope: scheduler-owned `0131` stale cleanup/core/research preflight를 source-of-record로 사용했고, quote rows가 decision time 기준 20분 이내라 추가 live Alpaca read-only call 없이 preflight submit boundary를 재사용했다. `SO`는 preflight quote `95.21/95.23` spread `0.0210%`로 trim gate를 통과했지만 same-day `SO` sell fill이 이미 있어 duplicate symbol/side discipline에 막혔고, `PFE`도 같은 duplicate gate를 유지했다. `RGTI`는 `0011` cycle에서 확인된 same-day canceled sell history가 계속 duplicate blocker로 남았다. `SPY/QQQ`는 validation floor cap 초과, `NOK`는 lifecycle add-block과 review backlog throttle 때문에 no-submit으로 종료했다. `get_account_info` 기준 cash는 `30,344.81 USD`, portfolio value는 `101,243.42 USD`였다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-17-0131-hourly-autopilot-post-trade.json`

_Last updated: 2026-06-17 01:32 KST_

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-17-0111-hourly-autopilot]]
- Open/new: 없음. scheduler-owned `0111` preflight `get_orders(status=open)` 기준 open orders `0`건이었다.
- Filled: 이번 cycle 신규 fill 없음. same-day fill history는 `SO` sell 1건, `PFE` sell 1건, `AVGO` sell 1건만 유지됐다.
- Cancelled: 신규 취소 없음. `RGTI` same-day sell 7주는 earlier `0011` runtime recheck 기준 `canceled` 상태를 유지했고 duplicate-side blocker로만 재사용했다.
- Position count observed by Alpaca MCP: scheduler core preflight `get_all_positions` 기준 positions `33`건, `get_orders(status=open)` 기준 open orders `0`건이었다.
- Recent reconciliation scope: scheduler-owned `0111` stale cleanup/core/research preflight를 source-of-record로 사용했고, quote rows가 decision time 기준 20분 이내라 추가 live Alpaca read-only call 없이 preflight submit boundary를 재사용했다. `SO`는 preflight quote `95.12/95.35` spread `0.2415%`로 trim gate를 통과했지만 same-day `SO` sell fill이 이미 있어 duplicate symbol/side discipline에 막혔고, `PFE`도 같은 duplicate gate를 유지했다. `RGTI`는 `0011` cycle에서 확인된 same-day canceled sell history가 계속 duplicate blocker로 남았다. `SPY/QQQ`는 validation floor cap 초과, `NOK`는 lifecycle add-block과 review backlog throttle 때문에 no-submit으로 종료했다. `get_account_info` 기준 cash는 `30,344.81 USD`, portfolio value는 `101,395.86 USD`였다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-17-0111-hourly-autopilot-post-trade.json`

_Last updated: 2026-06-17 01:12 KST_

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-17-0051-hourly-autopilot]]
- Open/new: 없음. scheduler-owned `0051` preflight `get_orders(status=open)` 기준 open orders `0`건이었다.
- Filled: 이번 cycle 신규 fill 없음. same-day fill history는 `SO` sell 1건, `PFE` sell 1건, `AVGO` sell 1건만 유지됐다.
- Cancelled: 신규 취소 없음. `RGTI` same-day sell 7주는 earlier `0011` runtime recheck 기준 `canceled` 상태를 유지했고 duplicate-side blocker로만 재사용했다.
- Position count observed by Alpaca MCP: scheduler core preflight `get_all_positions` 기준 positions `33`건, `get_orders(status=open)` 기준 open orders `0`건이었다.
- Recent reconciliation scope: scheduler-owned `0051` stale cleanup/core/research preflight를 source-of-record로 사용했고, quote rows가 decision time 기준 20분 이내라 추가 live Alpaca read-only call 없이 preflight submit boundary를 재사용했다. `SO`는 preflight quote `95.24/95.27` spread `0.0315%`로 trim gate를 통과했지만 same-day `SO` sell fill이 이미 있어 duplicate symbol/side discipline에 막혔고, `PFE`도 같은 duplicate gate를 유지했다. `RGTI`는 `0011` cycle에서 확인된 same-day canceled sell history가 계속 duplicate blocker로 남았다. `SPY/QQQ`는 validation floor cap 초과, `NOK`는 lifecycle add-block과 review backlog throttle 때문에 no-submit으로 종료했다. `get_account_info` 기준 cash는 `30,344.81 USD`, portfolio value는 `101,043.33 USD`였다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-17-0051-hourly-autopilot-post-trade.json`

_Last updated: 2026-06-17 00:52 KST_

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-17-0031-hourly-autopilot]]
- Open/new: 없음. scheduler-owned `0031` preflight `get_orders(status=open)` 기준 open orders `0`건이었다.
- Filled: 이번 cycle 신규 fill 없음. same-day fill history는 `SO` sell 1건, `PFE` sell 1건, `AVGO` sell 1건만 유지됐다.
- Cancelled: 신규 취소 없음. `RGTI` same-day sell 7주는 earlier `0011` runtime recheck 기준 `canceled` 상태를 유지했고 duplicate-side blocker로만 재사용했다.
- Position count observed by Alpaca MCP: scheduler core preflight `get_all_positions` 기준 positions `33`건, `get_orders(status=open)` 기준 open orders `0`건이었다.
- Recent reconciliation scope: scheduler-owned `0031` stale cleanup/core/research preflight를 source-of-record로 사용했고, quote rows가 decision time 기준 20분 이내라 추가 live Alpaca read-only call 없이 preflight submit boundary를 재사용했다. `SO`는 preflight quote `94.79/94.83` spread `0.0422%`로 trim gate를 통과했지만 same-day `SO` sell fill이 이미 있어 duplicate symbol/side discipline에 막혔고, `PFE`도 같은 duplicate gate를 유지했다. `RGTI`는 `0011` cycle에서 확인된 same-day canceled sell history가 계속 duplicate blocker로 남았다. `SPY/QQQ`는 validation floor cap 초과, `NOK`는 lifecycle add-block과 review backlog throttle 때문에 no-submit으로 종료했다. `get_account_info` 기준 cash는 `30,344.81 USD`, portfolio value는 `101,278.92 USD`였다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-17-0031-hourly-autopilot-post-trade.json`

_Last updated: 2026-06-17 00:32 KST_

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-17-0011-hourly-autopilot]]
- Open/new: 없음. live `get_orders(status=open)` 기준 open orders `0`건이었다.
- Filled: 이번 cycle 신규 fill 없음. same-day order history는 earlier `AVGO` sell 1건, `PFE` sell 1건, `SO` sell 1건, `RGTI` canceled 1건만 유지됐다.
- Cancelled: 신규 취소 없음. `RGTI` same-day sell 7주는 earlier cycle stale cleanup 결과 `canceled` 상태를 유지했다.
- Position count observed by Alpaca MCP: live `get_all_positions` 기준 positions `33`건, live `get_orders(status=open)` 기준 open orders `0`건이었다.
- Recent reconciliation scope: scheduler-owned `0011` stale cleanup/core/research preflight를 source-of-record로 사용했고 live Alpaca `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-16T13:11:00Z)/get_stock_latest_quote(feed=iex)/get_stock_snapshot(feed=iex)`로 submit boundary를 다시 열었다. `SO`는 quote `94.67/94.70` spread `0.0317%`로 trim gate를 통과했지만 same-day `SO` sell fill이 이미 생겨 duplicate symbol/side discipline에 막혔고, `RGTI`/`PFE`도 같은 duplicate gate를 유지했다. `SPY/QQQ`는 validation floor cap 초과, `NOK`는 lifecycle add-block과 review backlog throttle 때문에 no-submit으로 종료했다. `get_account_info` 기준 cash는 `30,344.81 USD`, portfolio value는 `101,506.73 USD`였다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-17-0011-hourly-autopilot-post-trade.json`

_Last updated: 2026-06-17 00:15 KST_

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-16-2351-hourly-autopilot]]
- Open/new: 없음. `client_order_id=hourly-20260616-2351-sell-so`는 same client id reconciliation 기준 즉시 `filled`였다.
- Filled: `SO` sell 1주 at `94.77 USD`
- Cancelled: 없음
- Position count observed by Alpaca MCP: live `get_all_positions` 기준 positions `33`건, live `get_orders(status=open)` 기준 open orders `0`건, live `get_account_activities(activity_types=[FILL], after=2026-06-16T13:51:00Z)` 기준 same-session fill `2`건(`PFE`, `SO`)이었다.
- Recent reconciliation scope: scheduler-owned `2351` stale cleanup/core/research preflight를 source-of-record로 사용했고 live Alpaca `get_clock/get_account_info/get_orders(status=open)/get_orders(status=all, after=2026-06-16T13:51:00Z)/get_account_activities(activity_types=[FILL], after=2026-06-16T13:51:00Z)/get_all_positions/get_stock_latest_quote(SO)/get_stock_snapshot(SO)`로 submit boundary를 다시 열었다. `SO` 주문은 `2026-06-16T14:58:02.526808Z`에 `filled_avg_price=94.77 USD`로 즉시 체결됐고, `get_all_positions` 기준 `SO qty 6 -> 5`, `qty_available=5`로 감소했다. `get_account_info` 기준 cash는 `30,344.81 USD`, portfolio value는 `101,432.05 USD`였다.
- Orders submitted/replaced/cancelled/closed by this workflow: 1 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-16-2351-hourly-autopilot-post-trade.json`

_Last updated: 2026-06-16 23:58 KST_

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-16-2331-hourly-autopilot]]
- Open/new: 없음. stale cleanup artifact에 남아 있던 `RGTI` sell 7주 (`client_order_id=hourly-20260616-2251-sell-rgti`)는 live Alpaca `get_orders(status=all, after=2026-06-16T13:31:00Z)` 기준 `2026-06-16T14:31:08.972628Z`에 `canceled`로 정리됐고, live `get_orders(status=open)`는 `0`건이었다.
- Filled: 이번 cycle 신규 fill 없음. same-day regular fill history는 earlier `AVGO` sell 1건, `PFE` sell 1건만 유지됐다.
- Cancelled: `RGTI` stale sell 7주가 stale cleanup/life-cycle reconcile 결과 `canceled`로 닫혔다.
- Position count observed by Alpaca MCP: live `get_all_positions` 기준 positions `33`건, live `get_orders(status=open)` 기준 open orders `0`건, live `get_account_activities(activity_types=[FILL], after=2026-06-16T13:31:00Z)` 기준 same-day fill `2`건(`AVGO`, `PFE`)이었다.
- Recent reconciliation scope: scheduler-owned `2331` stale cleanup/core/research preflight를 source-of-record로 사용했고 live Alpaca `get_clock/get_account_info/get_orders(status=open)/get_orders(status=all, after=2026-06-16T13:31:00Z)/get_account_activities(activity_types=[FILL], after=2026-06-16T13:31:00Z)/get_all_positions`로 재조정했다. regular market은 `2026-06-16T10:33:05.200440095-04:00` 기준 open, account `ACTIVE`, cash `30,250.04 USD`, portfolio value `101,378.20 USD`였다. `RGTI`/`PFE`는 same-day duplicate symbol/side discipline, `SO`는 spread fail, `SPY/QQQ/NOK`는 buy-side backlog/cap/add-block 때문에 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 1 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-16-2331-hourly-autopilot-post-trade.json`

_Last updated: 2026-06-16 23:34 KST_

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-16-2311-hourly-autopilot]]
- Open/new: `RGTI` sell 7주 at `22.07 USD` (`client_order_id=hourly-20260616-2251-sell-rgti`)가 여전히 `status=new` open order로 남아 있다.
- Filled: `PFE` sell 1주 at `25.94 USD`
- Cancelled: 없음
- Position count observed by Alpaca MCP: live `get_all_positions` 기준 positions `33`건, live `get_orders(status=open)` 기준 open orders `1`건, live `get_account_activities(activity_types=[FILL], after=2026-06-16T14:18:00Z)` 기준 새 fill `1`건(`PFE`)이었다.
- Recent reconciliation scope: scheduler-owned `2311` core/research preflight를 source-of-record로 사용했고 direct Alpaca submit-boundary check 뒤 `PFE` 1주 trim sell을 제출했다. same client id reconciliation 기준 주문은 `2026-06-16T14:18:55.368487606Z`에 `filled_avg_price=25.94 USD`로 즉시 체결됐고, `get_all_positions` 기준 `PFE qty 4 -> 3`, `qty_available=3`으로 감소했다. `RGTI`는 보유수량 `28주` 유지, `qty_available=21`만 예약 상태이며 `get_account_info` 기준 cash는 `30,250.04 USD`, portfolio value는 `101,888.16 USD`였다.
- Orders submitted/replaced/cancelled/closed by this workflow: 1 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-16-2311-hourly-autopilot-post-trade.json`

_Last updated: 2026-06-16 23:19 KST_

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-16-2251-hourly-autopilot]]
- Open/new: `RGTI` sell 7주 at `22.07 USD` (`client_order_id=hourly-20260616-2251-sell-rgti`)가 immediate reconciliation 기준 `status=new` open order다.
- Filled: 없음. same-session regular fill은 earlier `AVGO` trim 1건만 유지됐다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: live `get_all_positions` 기준 positions `33`건, live `get_watchlists` 기준 watchlists `0`건이었다. live `get_orders(status=open)` 기준 open orders `1`건, same-session `get_orders(status=all, after=2026-06-16T14:00:00Z)` 기준 `RGTI` sell 1건이 전부였다.
- Recent reconciliation scope: scheduler-owned `2251` core/research preflight를 source-of-record로 사용했고 direct Alpaca submit-boundary check 뒤 same `client_order_id` reconciliation을 수행했다. `RGTI`는 보유수량 `28주`를 유지한 채 `qty_available=21`만 예약 상태이며, `get_account_info` 기준 cash는 `30,224.10 USD`, portfolio value는 `102,087.01 USD`였다.
- Orders submitted/replaced/cancelled/closed by this workflow: 1 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-16-2251-hourly-autopilot-post-trade.json`

_Last updated: 2026-06-16 23:01 KST_

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-16-2231-hourly-autopilot]]
- Open/new: 없음. `client_order_id=hourly-20260616-2231-sell-avgo`는 immediate reconciliation 기준 이미 `filled`였다.
- Filled: `AVGO` sell 1주 at `387.76 USD`
- Cancelled: 없음
- Position count observed by Alpaca MCP: live `get_all_positions` 기준 positions `33`건, live `get_watchlists` baseline 기준 watchlists `0`건이었다. live `get_orders(status=open)` 기준 open orders `0`건, same-session `get_orders(status=all, after=2026-06-16T13:30:00Z)` 기준 `AVGO` sell 1건이 전부였다.
- Recent reconciliation scope: scheduler-owned `2231` core/research preflight를 source-of-record로 사용했고 direct Alpaca submit-boundary check로 `clock/account/orders/activities/quote`를 다시 열었다. `AVGO` 주문은 `2026-06-16T13:43:57.208757279Z`에 `filled_avg_price=387.76 USD`로 즉시 체결됐고, `get_all_positions` 기준 보유수량은 `2주 -> 1주`, `get_account_info` 기준 cash는 `30,224.10 USD`로 증가했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 1 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-16-2231-hourly-autopilot-post-trade.json`

_Last updated: 2026-06-16 22:44 KST_

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-16-2151-after-hours-autopilot]]
- Open/new: 없음. 이번 cycle에서는 `place_stock_order`를 호출하지 않았고 신규 `client_order_id`도 만들지 않았다.
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: live `get_all_positions` 기준 positions `33`건, live `get_watchlists` 기준 watchlists `0`건이었다. live `get_orders(status=open)`와 `get_orders(status=all, after=2026-06-15T20:00:00Z)` 기준 open orders `0`건, same-session after-hours orders `0`건이었다. live `get_account_activities(activity_types=[FILL], after=2026-06-15T20:00:00Z)` 기준 same-session after-hours fills도 `0`건이었다.
- Recent reconciliation scope: scheduler-owned `2151` core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. live `iex` quote check는 `SPY/QQQ/NOK/RGTI/GOOGL/TSLA/SMH/SLB`를 2026-06-16 21:55 KST에 재확인했다. `GOOGL/NOK`는 fresh quote까지 확보했지만 `GOOGL`은 spread cap과 same-session duplicate/review backlog, `NOK`는 add-block/review backlog, `QQQ/SPY/RGTI/TSLA/SMH/SLB`는 freshness·spread·notional cap 때문에 submit path가 열리지 않았다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-16-2151-after-hours-autopilot-post-trade.json`

_Last updated: 2026-06-16 21:55 KST_

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-16-2131-after-hours-autopilot]]
- Open/new: 없음. 이번 cycle에서는 `place_stock_order`를 호출하지 않았고 신규 `client_order_id`도 만들지 않았다.
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: live `get_all_positions` 기준 positions `33`건, live `get_watchlists` 기준 watchlists `0`건이었다. live `get_orders(status=open)`와 `get_orders(status=all, after=2026-06-15T20:00:00Z)` 기준 open orders `0`건, same-session after-hours orders `0`건이었다. live `get_account_activities(activity_types=[FILL], after=2026-06-15T20:00:00Z)` 기준 same-session after-hours fills도 `0`건이었다.
- Recent reconciliation scope: scheduler-owned `2131` core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. live `overnight` quote check는 `QQQ/RGTI/NOK/TSLA/SMH/SLB/AVGO/GE/SPY/MSFT/PFE`를 2026-06-16 21:34 KST에 재확인했지만 latest overnight quote timestamp가 모두 `2026-06-16T08:00:00Z` 부근에 머물러 fresh-quote hard gate가 약 `273.31`분 stale로 닫혀 있었다. `AVGO/RGTI/PFE`는 same-day duplicate sell discipline과 spread fail, `MSFT/NOK`는 review backlog throttle 또는 add-block, `QQQ/SPY/SMH`는 per-order cap 또는 spread fail, `TSLA`는 watch-only thesis, `SLB/GE`는 spread cap 때문에 submit path가 열리지 않았다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-16-2131-after-hours-autopilot-post-trade.json`

_Last updated: 2026-06-16 21:34 KST_

- Run: [[2026-06-16-2111-after-hours-autopilot]]
- Open/new: 없음. 이번 cycle에서는 `place_stock_order`를 호출하지 않았고 신규 `client_order_id`도 만들지 않았다.
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: live `get_all_positions` 기준 positions `33`건, live `get_watchlists` 기준 watchlists `0`건이었다. live `get_orders(status=open)`와 `get_orders(status=all, after=2026-06-15T20:00:00Z)` 기준 open orders `0`건, same-session after-hours orders `0`건이었다.
- Recent reconciliation scope: scheduler-owned `2111` core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. live `overnight` quote check는 `QQQ/RGTI/NOK/TSLA/SMH/SLB/AVGO/GE/SPY/MSFT/PFE`를 2026-06-16 21:14 KST에 재확인했지만 latest overnight quote timestamp가 모두 `2026-06-16T08:00:00Z` 부근에 머물러 fresh-quote hard gate가 약 `254.24-254.25`분 stale로 닫혀 있었다. `AVGO/RGTI/PFE`는 same-day duplicate sell discipline과 spread fail, `MSFT/NOK`는 review backlog throttle 또는 add-block, `QQQ/SPY/SMH`는 per-order cap 또는 spread fail, `TSLA`는 watch-only thesis, `SLB/GE`는 spread cap 때문에 submit path가 열리지 않았다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-16-2111-after-hours-autopilot-post-trade.json`

_Last updated: 2026-06-16 21:14 KST_

- Run: [[2026-06-16-2051-after-hours-autopilot]]
- Open/new: 없음. 이번 cycle에서는 `place_stock_order`를 호출하지 않았고 신규 `client_order_id`도 만들지 않았다.
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: live `get_all_positions` 기준 positions `33`건, live `get_watchlists` 기준 watchlists `0`건이었다. live `get_clock/get_account_info/get_orders(status=open)/get_orders(status=all, after=2026-06-15T20:00:00Z)/get_account_activities(activity_types=[FILL], after=2026-06-15T20:00:00Z)/get_stock_snapshot(feed=overnight)` continuity 기준 account `ACTIVE`, open orders `0`건, same-session after-hours orders `0`건, same-session after-hours fills `0`건이었다.
- Recent reconciliation scope: scheduler-owned `2051` core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. live `overnight` quote check는 `QQQ/RGTI/NOK/TSLA/SMH/SLB/AVGO/GE/SPY/MSFT/PFE`를 2026-06-16 20:53 KST에 재확인했지만 latest overnight quote timestamp가 모두 `2026-06-16T08:00:00Z` 부근에 머물러 fresh-quote hard gate가 약 `233.13`분 stale로 닫혀 있었다. `AVGO/RGTI/PFE`는 same-day duplicate sell discipline과 spread fail, `MSFT/NOK`는 review backlog throttle 또는 add-block, `QQQ/SPY/SMH`는 per-order cap 또는 spread fail, `TSLA`는 watch-only thesis, `SLB/GE`는 spread cap 때문에 submit path가 열리지 않았다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-16-2051-after-hours-autopilot-post-trade.json`

_Last updated: 2026-06-16 20:53 KST_

- Run: [[2026-06-16-2031-after-hours-autopilot]]
- Open/new: 없음. 이번 cycle에서는 `place_stock_order`를 호출하지 않았고 신규 `client_order_id`도 만들지 않았다.
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: live `get_all_positions` 기준 positions `33`건, live `get_watchlists` 기준 watchlists `0`건이었다. live `get_clock/get_account_info/get_orders(status=open)/get_orders(status=all, after=2026-06-15T20:00:00Z)/get_stock_snapshot(feed=overnight)` continuity 기준 account `ACTIVE`, open orders `0`건, same-session after-hours orders `0`건이었다.
- Recent reconciliation scope: scheduler-owned `2031` core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. live `overnight` quote check는 `QQQ/RGTI/NOK/TSLA/SMH/SLB/AVGO/GE/SPY/MSFT/PFE`를 2026-06-16 20:32 KST에 재확인했지만 latest overnight quote timestamp가 모두 `2026-06-16T08:00:00Z` 부근에 머물러 fresh-quote hard gate가 약 `212.82-212.84`분 stale로 닫혀 있었다. `AVGO/RGTI/PFE`는 same-day duplicate sell discipline과 spread fail, `MSFT/NOK`는 review backlog throttle 또는 add-block, `QQQ/SPY/SMH`는 per-order cap 또는 spread fail, `TSLA`는 watch-only thesis, `SLB/GE`는 spread cap 때문에 submit path가 열리지 않았다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-16-2031-after-hours-autopilot-post-trade.json`

_Last updated: 2026-06-16 20:32 KST_

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-16-2011-after-hours-autopilot]]
- Open/new: 없음. 이번 cycle에서는 `place_stock_order`를 호출하지 않았고 신규 `client_order_id`도 만들지 않았다.
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `2011` core preflight 기준 positions `33`건, watchlists `0`건이었다. live `get_clock/get_account_info/get_orders(status=open)/get_orders(status=all, after=2026-06-15T20:00:00Z)/get_stock_snapshot(feed=overnight)` continuity 기준 account `ACTIVE`, open orders `0`건, same-session after-hours orders/fills `0`건이었다.
- Recent reconciliation scope: scheduler-owned `2011` core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. live `overnight` quote check는 `QQQ/RGTI/NOK/TSLA/SMH/SLB/AVGO/GE/SPY/MSFT/PFE`를 2026-06-16 20:14 KST에 재확인했지만 latest overnight quote timestamp가 모두 `2026-06-16T08:00:00Z` 부근에 머물러 fresh-quote hard gate가 약 `193.17`분 stale로 닫혀 있었다. `AVGO/RGTI/PFE`는 same-day duplicate sell discipline과 spread fail, `MSFT/NOK`는 review backlog throttle 또는 add-block, `QQQ/SPY/SMH`는 per-order cap 또는 spread fail, `TSLA`는 watch-only thesis, `SLB/GE`는 spread cap 때문에 submit path가 열리지 않았다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-16-2011-after-hours-autopilot-post-trade.json`

_Last updated: 2026-06-16 20:14 KST_

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-16-1951-after-hours-autopilot]]
- Open/new: 없음. 이번 cycle에서는 `place_stock_order`를 호출하지 않았고 신규 `client_order_id`도 만들지 않았다.
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `1951` core preflight와 live `get_clock/get_account_info/get_all_positions/get_watchlists/get_stock_latest_quote(feed=overnight)/get_stock_snapshot(feed=overnight)` continuity 기준 account `ACTIVE`, positions `33`건, watchlists `0`건이었다. open orders `0`건과 same-session after-hours orders/fills `0`건은 same preflight baseline을 유지했다.
- Recent reconciliation scope: scheduler-owned `1951` core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. direct `overnight` quote check는 `QQQ/RGTI/NOK/TSLA/SMH/SLB/AVGO/GE/SPY/MSFT/PFE`를 2026-06-16 19:53 KST에 재확인했지만 latest overnight quote timestamp가 모두 `2026-06-16T08:00:00Z` 부근에 머물러 fresh-quote hard gate가 약 `173.96-173.99`분 stale로 닫혀 있었다. `AVGO/RGTI/PFE`는 same-day duplicate sell discipline과 spread fail, `MSFT/NOK`는 review backlog throttle 또는 add-block, `QQQ/SPY/SMH`는 per-order cap 또는 spread fail, `TSLA`는 watch-only thesis, `SLB/GE`는 spread cap 때문에 submit path가 열리지 않았다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-16-1951-after-hours-autopilot-post-trade.json`

_Last updated: 2026-06-16 19:53 KST_

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-16-1931-after-hours-autopilot]]
- Open/new: 없음. 이번 cycle에서는 `place_stock_order`를 호출하지 않았고 신규 `client_order_id`도 만들지 않았다.
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `1931` core preflight 기준 account `ACTIVE`, positions `33`건, watchlists `0`건, open orders `0`건, same-session after-hours orders/fills `0`건이었다.
- Recent reconciliation scope: scheduler-owned `1931` core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. same preflight latestQuote rows는 freshest `QQQ`도 약 `823.38`분 stale였고 나머지 candidate는 `861.22-873.90`분 stale였다. `AVGO/RGTI/PFE`는 same-day duplicate sell discipline과 spread fail, `MSFT/NOK`는 review backlog throttle 또는 add-block, `QQQ/SPY/SMH`는 per-order cap 또는 quote completeness fail, `TSLA`는 watch-only thesis, `SLB/GE`는 spread cap 때문에 submit path가 열리지 않았다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-16-1931-after-hours-autopilot-post-trade.json`

_Last updated: 2026-06-16 19:33 KST_

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-16-1911-after-hours-autopilot]]
- Open/new: 없음. 이번 cycle에서는 `place_stock_order`를 호출하지 않았고 신규 `client_order_id`도 만들지 않았다.
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `1911` core preflight와 direct `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-15T20:00:00Z)/get_stock_latest_quote(feed=overnight)/get_stock_snapshot(feed=overnight)` continuity 기준 account `ACTIVE`, positions `33`건, open orders `0`건, same-session after-hours orders `0`건이었다. watchlists `0` baseline은 same preflight rows를 재사용했다.
- Recent reconciliation scope: scheduler-owned `1911` core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. direct `overnight` quote check는 `QQQ/RGTI/NOK/TSLA/SMH/SLB/AVGO/GE/SPY/MSFT/PFE`를 2026-06-16 19:12 KST에 재확인했지만 latest overnight quote timestamp가 모두 `2026-06-16T08:00:00Z` 부근에 머물러 fresh-quote hard gate가 약 `132.69`분 stale로 닫혀 있었다. `AVGO/RGTI/PFE`는 same-day duplicate sell discipline과 spread fail, `MSFT/NOK`는 review backlog throttle 또는 add-block, `QQQ/SPY/SMH`는 per-order cap, `TSLA`는 watch-only thesis, `SLB/GE`는 spread cap 때문에 submit path가 열리지 않았다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-16-1911-after-hours-autopilot-post-trade.json`

_Last updated: 2026-06-16 19:13 KST_

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-16-1851-after-hours-autopilot]]
- Open/new: 없음. 이번 cycle에서는 `place_stock_order`를 호출하지 않았고 신규 `client_order_id`도 만들지 않았다.
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `1851` core preflight와 direct `get_clock/get_account_info/get_all_positions/get_watchlists/get_orders(status=open)/get_orders(status=all, after=2026-06-15T20:00:00Z)/get_stock_latest_quote(feed=overnight)/get_stock_snapshot(feed=overnight)` continuity 기준 account `ACTIVE`, positions `33`건, watchlists `0`건, open orders `0`건, same-session after-hours orders `0`건이었다.
- Recent reconciliation scope: scheduler-owned `1851` core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. direct `overnight` quote check는 `QQQ/RGTI/NOK/TSLA/SMH/SLB/AVGO/GE/SPY/MSFT/PFE`를 2026-06-16 18:52 KST에 재확인했지만 latest overnight quote timestamp가 모두 `2026-06-16T08:00:00Z` 부근에 머물러 fresh-quote hard gate가 약 `112.88`분 stale로 닫혀 있었다. `AVGO/RGTI/PFE`는 same-day duplicate sell discipline과 spread fail, `MSFT/NOK`는 review backlog throttle 또는 add-block, `QQQ/SPY/SMH`는 per-order cap, `TSLA`는 watch-only thesis, `SLB/GE`는 spread cap 때문에 submit path가 열리지 않았다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-16-1851-after-hours-autopilot-post-trade.json`

_Last updated: 2026-06-16 18:57 KST_

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-16-1831-after-hours-autopilot]]
- Open/new: 없음. 이번 cycle에서는 `place_stock_order`를 호출하지 않았고 신규 `client_order_id`도 만들지 않았다.
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `1831` core preflight 기준 account `ACTIVE`, positions `33`건, watchlists `0`건, open orders `0`건, same-session after-hours orders/fills `0`건이었다.
- Recent reconciliation scope: scheduler-owned `1831` core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. 다만 same preflight quote rows는 `QQQ/RGTI/NOK/TSLA/SMH/SLB/AVGO/GE/SPY/MSFT/PFE` 전반에서 약 `760.95-811.47`분 stale였고, `AVGO/RGTI/PFE`는 duplicate sell discipline과 spread fail, `MSFT/NOK`는 review backlog throttle 또는 add-block, `QQQ/SPY/SMH`는 per-order cap 또는 quote completeness fail, `TSLA`는 watch-only thesis, `SLB/GE`는 spread cap 때문에 submit path가 열리지 않았다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-16-1831-after-hours-autopilot-post-trade.json`

_Last updated: 2026-06-16 18:31 KST_

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-16-1811-after-hours-autopilot]]
- Open/new: 없음. 이번 cycle에서는 `place_stock_order`를 호출하지 않았고 신규 `client_order_id`도 만들지 않았다.
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `1811` core preflight와 direct `get_clock/get_account_info/get_all_positions/get_watchlists/get_orders(status=open)/get_orders(status=all, after=2026-06-15T20:00:00Z)/get_account_activities(activity_types=[FILL], after=2026-06-15T20:00:00Z)/get_stock_latest_quote(feed=overnight)/get_stock_snapshot(feed=overnight)` continuity 기준 account `ACTIVE`, positions `33`건, watchlists `0`건, open orders `0`건, same-session after-hours orders/fills `0`건이었다.
- Recent reconciliation scope: scheduler-owned `1811` core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. direct `overnight` quote check는 `QQQ/RGTI/NOK/TSLA/SMH/SLB/AVGO/GE/SPY/MSFT/PFE`를 2026-06-16 18:13 KST에 재확인했다. 다만 latest overnight quote timestamp가 모두 `2026-06-16T08:00:00Z` 부근에 머물러 fresh-quote hard gate가 약 `73.44`분 stale로 닫혀 있었고, `AVGO/RGTI/PFE`는 duplicate sell discipline과 spread fail, `MSFT/NOK`는 review backlog throttle 또는 add-block, `QQQ/SPY/SMH`는 per-order cap, `TSLA`는 watch-only thesis, `GE/SLB/NOK`는 spread cap 때문에 submit path가 열리지 않았다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-16-1811-after-hours-autopilot-post-trade.json`

_Last updated: 2026-06-16 18:13 KST_

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-16-1751-after-hours-autopilot]]
- Open/new: 없음. 이번 cycle에서는 `place_stock_order`를 호출하지 않았고 신규 `client_order_id`도 만들지 않았다.
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `1751` core preflight와 direct `get_clock/get_account_info/get_all_positions/get_watchlists/get_orders(status=open)/get_orders(status=all, after=2026-06-15T20:00:00Z)/get_stock_latest_quote(feed=overnight)/get_stock_snapshot(feed=overnight)` continuity 기준 account `ACTIVE`, positions `33`건, watchlists `0`건, open orders `0`건, same-session after-hours orders `0`건이었다.
- Recent reconciliation scope: scheduler-owned `1751` core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. direct `overnight` quote check는 `QQQ/RGTI/NOK/TSLA/SMH/SLB/AVGO/GE/SPY/MSFT/PFE`를 2026-06-16 17:56 KST에 재확인했다. 다만 latest overnight quote timestamp가 모두 `2026-06-16T08:00:00Z` 부근에 머물러 fresh-quote hard gate가 약 `53.80`분 stale로 닫혀 있었고, `AVGO/RGTI/PFE`는 duplicate sell discipline과 spread fail, `MSFT/NOK`는 review backlog throttle 또는 add-block, `QQQ/SPY/SMH`는 per-order cap, `TSLA`는 watch-only thesis, `GE/SLB/NOK`는 spread cap 때문에 submit path가 열리지 않았다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-16-1751-after-hours-autopilot-post-trade.json`

_Last updated: 2026-06-16 17:56 KST_

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-16-1731-after-hours-autopilot]]
- Open/new: 없음. 이번 cycle에서는 `place_stock_order`를 호출하지 않았고 신규 `client_order_id`도 만들지 않았다.
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `1731` core preflight와 direct `get_clock/get_account_info/get_all_positions/get_watchlists/get_orders(status=open)/get_orders(status=all, after=2026-06-15T20:00:00Z)/get_account_activities(activity_types=[FILL], after=2026-06-15T20:00:00Z)/get_stock_latest_quote(feed=overnight)/get_stock_snapshot(feed=overnight)` continuity 기준 account `ACTIVE`, positions `33`건, watchlists `0`건, open orders `0`건, same-session after-hours orders/fills `0`건이었다.
- Recent reconciliation scope: scheduler-owned `1731` core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. direct `overnight` quote check는 `QQQ/RGTI/NOK/TSLA/SMH/SLB/AVGO/GE/SPY/MSFT/PFE`를 2026-06-16 17:34 KST에 재확인했다. 다만 latest overnight quote timestamp가 모두 `2026-06-16T08:00:00Z` 부근에 머물러 fresh-quote hard gate가 약 `33.41`분 stale로 닫혀 있었고, `AVGO/RGTI/PFE`는 duplicate sell discipline과 spread fail, `MSFT/NOK`는 review backlog throttle 또는 add-block, `QQQ/SPY/SMH`는 per-order cap, `TSLA`는 watch-only thesis, `GE/SLB/NOK`는 spread cap 때문에 submit path가 열리지 않았다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-16-1731-after-hours-autopilot-post-trade.json`

_Last updated: 2026-06-16 17:34 KST_

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-16-1711-after-hours-autopilot]]
- Open/new: 없음. 이번 cycle에서는 `place_stock_order`를 호출하지 않았고 신규 `client_order_id`도 만들지 않았다.
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `1711` core preflight와 direct `get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-15T20:00:00Z)/get_watchlists/get_stock_latest_quote(feed=overnight)/get_stock_snapshot(feed=overnight)` continuity 기준 account `ACTIVE`, positions `33`건, watchlists `0`건, open orders `0`건, same-session after-hours orders `0`건이었다.
- Recent reconciliation scope: scheduler-owned `1711` core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. direct `overnight` quote check는 `QQQ/RGTI/NOK/TSLA/SMH/SLB/AVGO/GE/SPY/MSFT/PFE`를 2026-06-16 17:14 KST에 재확인했다. 다만 latest overnight quote timestamp가 모두 `2026-06-16T08:00:00Z` 부근에 머물러 fresh-quote hard gate가 약 `14.28-14.30`분 stale로 닫혀 있었고, `AVGO/RGTI/PFE`는 duplicate sell discipline과 spread fail, `MSFT/NOK`는 review backlog throttle 또는 add-block, `QQQ/SPY/SMH`는 per-order cap, `TSLA`는 watch-only thesis, `GE/SLB/NOK`는 spread cap 때문에 submit path가 열리지 않았다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-16-1711-after-hours-autopilot-post-trade.json`

_Last updated: 2026-06-16 17:14 KST_

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-16-1651-after-hours-autopilot]]
- Open/new: 없음. 이번 cycle에서는 `place_stock_order`를 호출하지 않았고 신규 `client_order_id`도 만들지 않았다.
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `1651` core preflight와 direct `get_clock/get_account_info/get_all_positions/get_watchlists/get_orders(status=open)/get_orders(status=all, after=2026-06-15T20:00:00Z)/get_account_activities(activity_types=[FILL], after=2026-06-15T20:00:00Z)/get_stock_latest_quote(feed=overnight)/get_stock_snapshot(feed=overnight)` continuity 기준 account `ACTIVE`, positions `33`건, watchlists `0`건, open orders `0`건, same-session after-hours orders/fills `0`건이었다.
- Recent reconciliation scope: scheduler-owned `1651` core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. direct `overnight` quote check는 `QQQ/RGTI/NOK/TSLA/SMH/SLB/AVGO/GE/SPY/MSFT/PFE`를 2026-06-16 16:53 KST에 재확인했다. `AVGO`는 same-day duplicate sell discipline, `RGTI/PFE`는 duplicate sell plus spread cap, `MSFT`는 same-day duplicate buy와 review backlog throttle, `NOK`는 add-block plus spread cap, `QQQ/SPY/SMH`는 per-order cap 또는 spread cap, `TSLA`는 watch-only thesis, `GE/SLB`는 spread cap 때문에 submit path가 열리지 않았다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-16-1651-after-hours-autopilot-post-trade.json`

_Last updated: 2026-06-16 16:53 KST_

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-16-1631-after-hours-autopilot]]
- Open/new: 없음. 이번 cycle에서는 `place_stock_order`를 호출하지 않았고 신규 `client_order_id`도 만들지 않았다.
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `1631` core preflight와 direct `get_watchlists/get_stock_latest_quote(feed=overnight)/get_stock_snapshot(feed=overnight)` continuity 기준 account `ACTIVE`, positions `33`건, watchlists `0`건, open orders `0`건, same-session after-hours orders `0`건이었다.
- Recent reconciliation scope: scheduler-owned `1631` core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. direct `overnight` quote check는 `QQQ/RGTI/NOK/TSLA/SMH/SLB/AVGO/GE/SPY/MSFT/PFE`를 2026-06-16 16:33 KST에 재확인했다. `AVGO/RGTI/PFE`는 same-day duplicate sell discipline, `MSFT`는 same-day duplicate buy와 review backlog throttle, `NOK`는 add-block plus spread cap, `QQQ/SPY/SMH`는 per-order cap, `TSLA`는 watch-only thesis, `GE/SLB/NOK`는 spread cap 때문에 submit path가 열리지 않았다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-16-1631-after-hours-autopilot-post-trade.json`

_Last updated: 2026-06-16 16:12 KST_

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-16-1611-after-hours-autopilot]]
- Open/new: 없음. 이번 cycle에서는 `place_stock_order`를 호출하지 않았고 신규 `client_order_id`도 만들지 않았다.
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `1611` core preflight와 direct `get_clock/get_account_info/get_all_positions/get_watchlists/get_orders(status=open)/get_orders(status=all, after=2026-06-15T20:00:00Z)/get_account_activities(activity_types=[FILL], after=2026-06-15T20:00:00Z)/get_stock_latest_quote(feed=overnight)/get_stock_snapshot(feed=overnight)` continuity 기준 account `ACTIVE`, positions `33`건, watchlists `0`건, open orders `0`건, same-session after-hours orders/fills `0`건이었다.
- Recent reconciliation scope: scheduler-owned `1611` core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. direct `overnight` quote check는 `QQQ/RGTI/NOK/TSLA/SMH/SLB/AVGO/GE/SPY/MSFT/PFE`를 2026-06-16 16:12 KST에 재확인했다. `AVGO/RGTI/PFE`는 same-day duplicate sell discipline, `MSFT`는 same-day duplicate buy와 review backlog throttle, `NOK`는 add-block plus spread cap, `QQQ/SPY/SMH`는 per-order cap, `TSLA`는 watch-only thesis, `GE/SLB/NOK`는 spread cap 때문에 submit path가 열리지 않았다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-16-1611-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-16-1551-after-hours-autopilot]]
- Open/new: 없음. 이번 cycle에서는 `place_stock_order`를 호출하지 않았고 신규 `client_order_id`도 만들지 않았다.
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `1551` core preflight와 direct `get_clock/get_account_info/get_all_positions/get_watchlists/get_orders(status=open)/get_orders(status=all, after=2026-06-15T20:00:00Z)/get_stock_latest_quote(feed=overnight)/get_stock_snapshot(feed=overnight)` continuity 기준 account `ACTIVE`, positions `33`건, watchlists `0`건, open orders `0`건, same-session after-hours orders `0`건이었다.
- Recent reconciliation scope: scheduler-owned `1551` core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. direct `overnight` quote check는 `QQQ/RGTI/NOK/TSLA/SMH/SLB/AVGO/GE/SPY/MSFT/PFE`를 2026-06-16 15:52 KST에 재확인했다. `AVGO/RGTI/PFE`는 same-day duplicate sell discipline 또는 spread cap, `MSFT/NOK`는 review backlog throttle 또는 add-block, `QQQ/SPY/SMH`는 per-order cap, `TSLA`는 watch-only thesis, `SLB/GE`는 spread cap 때문에 submit path가 열리지 않았다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-16-1551-after-hours-autopilot-post-trade.json`

- Run: [[2026-06-16-1531-after-hours-autopilot]]
- Open/new: 없음. 이번 cycle에서는 `place_stock_order`를 호출하지 않았고 신규 `client_order_id`도 만들지 않았다.
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `1531` core preflight와 direct `get_clock/get_account_info/get_all_positions/get_watchlists/get_orders(status=open)/get_orders(status=all, after=2026-06-15T20:00:00Z)/get_account_activities(activity_types=[FILL], after=2026-06-15T20:00:00Z)/get_stock_latest_quote(feed=overnight)/get_stock_snapshot(feed=overnight)` continuity 기준 account `ACTIVE`, positions `33`건, watchlists `0`건, open orders `0`건, same-session after-hours orders/fills `0`건이었다.
- Recent reconciliation scope: scheduler-owned `1531` core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. direct `overnight` quote check는 `QQQ/RGTI/NOK/TSLA/SMH/SLB/AVGO/GE/SPY/MSFT/PFE`를 2026-06-16 15:33 KST에 재확인했다. `AVGO/PFE/RGTI`는 same-day duplicate sell discipline, `MSFT/NOK`는 review backlog throttle 또는 add-block, `NOK/SLB/GE`는 spread 또는 freshness cap, `QQQ/SPY/SMH`는 per-order cap, `TSLA`는 watch-only thesis 때문에 submit path가 열리지 않았다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-16-1531-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-16-1511-after-hours-autopilot]]
- Open/new: 없음. 이번 cycle에서는 `place_stock_order`를 호출하지 않았고 신규 `client_order_id`도 만들지 않았다.
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `1511` core preflight와 direct `get_clock/get_account_info/get_all_positions/get_watchlists/get_orders(status=open)/get_orders(status=all, after=2026-06-15T20:00:00Z)/get_stock_latest_quote(feed=overnight)/get_stock_snapshot(feed=overnight)` continuity 기준 account `ACTIVE`, positions `33`건, watchlists `0`건, open orders `0`건, same-session after-hours orders `0`건이었다.
- Recent reconciliation scope: scheduler-owned `1511` core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. direct `overnight` quote check는 `QQQ/RGTI/NOK/TSLA/SMH/SLB/AVGO/GE/SPY/MSFT/PFE`를 2026-06-16 15:13 KST에 재확인했다. `AVGO/PFE`는 same-day duplicate sell discipline, `RGTI`는 duplicate sell plus spread cap, `MSFT/NOK`는 review backlog throttle 또는 add-block, `QQQ/SPY/SMH`는 per-order cap, `TSLA`는 watch-only thesis, `SLB/GE`는 spread 또는 freshness cap 때문에 submit path가 열리지 않았다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-16-1511-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-16-1451-after-hours-autopilot]]
- Open/new: 없음. 이번 cycle에서는 `place_stock_order`를 호출하지 않았고 신규 `client_order_id`도 만들지 않았다.
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `1451` core preflight와 direct `get_clock/get_account_info/get_all_positions/get_watchlists/get_orders(status=open)/get_orders(status=all, after=2026-06-15T20:00:00Z)/get_stock_latest_quote(feed=overnight)/get_stock_snapshot(feed=overnight)` continuity 기준 account `ACTIVE`, positions `33`건, watchlists `0`건, open orders `0`건, same-session after-hours orders `0`건이었다.
- Recent reconciliation scope: scheduler-owned `1451` core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. direct `overnight` quote check는 `QQQ/RGTI/NOK/TSLA/SMH/SLB/AVGO/GE/SPY/MSFT/PFE`를 2026-06-16 14:53 KST에 재확인했다. `AVGO/RGTI/PFE`는 same-day duplicate sell discipline, `MSFT/NOK`는 review backlog throttle 또는 add-block, `QQQ/SPY/SMH`는 per-order cap, `TSLA`는 watch-only thesis, `SLB/GE`는 freshness 또는 spread cap 때문에 submit path가 열리지 않았다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-16-1451-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-16-1431-after-hours-autopilot]]
- Open/new: 없음. 이번 cycle에서는 `place_stock_order`를 호출하지 않았고 신규 `client_order_id`도 만들지 않았다.
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `1431` core preflight와 direct `get_clock/get_account_info/get_all_positions/get_watchlists/get_orders(status=open)/get_orders(status=all, after=2026-06-15T20:00:00Z)/get_stock_latest_quote(feed=overnight)/get_stock_snapshot(feed=overnight)` continuity 기준 account `ACTIVE`, positions `33`건, watchlists `0`건, open orders `0`건, same-session after-hours orders `0`건이었다.
- Recent reconciliation scope: scheduler-owned `1431` core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. direct `overnight` quote check는 `QQQ/RGTI/NOK/TSLA/SMH/SLB/AVGO/GE/SPY/MSFT/PFE`를 재확인했고 freshness는 모두 5분 cap 안에 있었다. 다만 `AVGO/PFE`는 duplicate sell discipline, `RGTI/SLB/GE`는 spread cap, `MSFT/NOK`는 review backlog throttle 또는 add-block, `QQQ/SPY/SMH`는 per-order cap, `TSLA`는 watch-only thesis 때문에 submit path가 열리지 않았다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-16-1431-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-16-1411-after-hours-autopilot]]
- Open/new: 없음. 이번 cycle에서는 `place_stock_order`를 호출하지 않았고 신규 `client_order_id`도 만들지 않았다.
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `1411` core preflight와 direct `get_clock/get_account_info/get_all_positions/get_watchlists/get_orders(status=open)/get_orders(status=all, after=2026-06-15T20:00:00Z)/get_stock_latest_quote(feed=overnight)` continuity 기준 account `ACTIVE`, positions `33`건, watchlists `0`건, open orders `0`건, same-session after-hours orders `0`건이었다.
- Recent reconciliation scope: scheduler-owned `1411` core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. direct `overnight` quote check는 `QQQ/RGTI/NOK/TSLA/SMH/SLB/AVGO/GE/SPY/MSFT/PFE`를 재확인했고 freshness fail은 `SLB` 약 `9.75`분, `GE` 약 `12.58`분으로 남았다. `AVGO`는 spread cap plus duplicate sell, `RGTI/PFE`는 duplicate sell, `MSFT/NOK`는 review backlog throttle 또는 add-block, `QQQ/SPY/SMH`는 per-order cap, `TSLA`는 watch-only thesis 때문에 submit path가 열리지 않았다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-16-1411-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-16-1351-after-hours-autopilot]]
- Open/new: 없음. 이번 cycle에서는 `place_stock_order`를 호출하지 않았고 신규 `client_order_id`도 만들지 않았다.
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `1351` core preflight와 direct `get_clock/get_account_info/get_all_positions/get_watchlists/get_orders(status=open)/get_orders(status=all, after=2026-06-15T20:00:00Z)/get_stock_latest_quote(feed=overnight)/get_stock_snapshot(feed=overnight)` continuity 기준 account `ACTIVE`, positions `33`건, watchlists `0`건, open orders `0`건, same-session after-hours orders `0`건이었다.
- Recent reconciliation scope: scheduler-owned `1351` core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. direct `overnight` quote check는 `QQQ/RGTI/NOK/TSLA/SMH/SLB/AVGO/GE/SPY/MSFT/PFE`를 재확인했고 freshness는 모두 5분 cap 안에 있었다. 다만 `AVGO/PFE/SLB/GE`는 spread cap, `RGTI`는 same-day duplicate sell discipline, `MSFT/NOK`는 review backlog throttle 또는 add-block, `QQQ/SPY/SMH`는 per-order cap, `TSLA`는 watch-only thesis 때문에 submit path가 열리지 않았다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-16-1351-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-16-1311-after-hours-autopilot]]
- Open/new: 없음. 이번 cycle에서는 `place_stock_order`를 호출하지 않았고 신규 `client_order_id`도 만들지 않았다.
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `1311` core preflight와 direct `get_clock/get_account_info/get_all_positions/get_watchlists/get_orders(status=open)/get_orders(status=all, after=2026-06-15T20:00:00Z)/get_stock_latest_quote(feed=overnight)/get_stock_snapshot(feed=overnight)` continuity 기준 account `ACTIVE`, positions `33`건, watchlists `0`건, open orders `0`건, same-session after-hours orders `0`건이었다.
- Recent reconciliation scope: scheduler-owned `1311` core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. direct `overnight` quote check는 `QQQ/RGTI/NOK/TSLA/SMH/SLB/AVGO/GE/SPY/MSFT/PFE`를 재확인했고 freshness fail은 `SLB`만 약 `15.81`분 stale로 남았다. `AVGO/RGTI/PFE`는 same-day duplicate sell discipline 또는 spread cap, `MSFT`는 same-day duplicate buy와 review backlog throttle, `NOK`는 add-block plus spread cap, `QQQ/SPY/SMH`는 per-order cap 또는 spread cap, `TSLA`는 watch-only thesis, `GE`는 spread cap 때문에 submit path가 열리지 않았다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-16-1311-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-16-1251-after-hours-autopilot]]
- Open/new: 없음. 이번 cycle에서는 `place_stock_order`를 호출하지 않았고 신규 `client_order_id`도 만들지 않았다.
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `1251` core preflight와 direct `get_clock/get_account_info/get_all_positions/get_watchlists/get_orders(status=open)/get_orders(status=all, after=2026-06-15T20:00:00Z)/get_account_activities(activity_types=[FILL], after=2026-06-15T20:00:00Z)/get_stock_latest_quote(feed=overnight)/get_stock_snapshot(feed=overnight)` continuity 기준 account `ACTIVE`, positions `33`건, watchlists `0`건, open orders `0`건, same-session after-hours orders/fills `0`건이었다.
- Recent reconciliation scope: scheduler-owned `1251` core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. direct `overnight` quote check는 `QQQ/RGTI/NOK/TSLA/SMH/SLB/AVGO/GE/SPY/MSFT/PFE`를 재확인했고 freshness fail은 `GE`만 약 `6.76`분 stale로 남았다. `AVGO/RGTI`는 same-day duplicate sell discipline, `PFE`는 duplicate sell plus spread cap, `MSFT`는 same-day duplicate buy와 review backlog throttle, `NOK`는 add-block, `QQQ/SPY/SMH`는 per-order cap, `SMH/SLB/GE/PFE`는 spread 또는 freshness fail, `TSLA`는 watch-only thesis 때문에 submit path가 열리지 않았다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-16-1251-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-16-1231-after-hours-autopilot]]
- Open/new: 없음. 이번 cycle에서는 `place_stock_order`를 호출하지 않았고 신규 `client_order_id`도 만들지 않았다.
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `1231` core preflight와 direct `get_clock/get_account_info/get_all_positions/get_watchlists/get_orders(status=open)/get_orders(status=all, after=2026-06-15T20:00:00Z)/get_account_activities(activity_types=[FILL], after=2026-06-15T20:00:00Z)/get_stock_latest_quote(feed=overnight)/get_stock_snapshot(feed=overnight)` continuity 기준 account `ACTIVE`, positions `33`건, watchlists `0`건, open orders `0`건, same-session after-hours orders/fills `0`건이었다.
- Recent reconciliation scope: scheduler-owned `1231` core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. direct `overnight` quote check는 `QQQ/RGTI/NOK/TSLA/SMH/SLB/AVGO/GE/SPY/MSFT/PFE`를 재확인했고 freshness fail은 `SLB` 약 `11.55`분, `GE` 약 `7.20`분 stale로 남았다. `AVGO`는 same-day duplicate sell discipline, `RGTI/PFE`는 duplicate sell plus spread cap, `MSFT`는 same-day duplicate buy와 review backlog throttle, `NOK`는 add-block, `QQQ/SPY/SMH`는 per-order cap, `TSLA`는 watch-only thesis, `SLB/GE`는 freshness 또는 spread fail 때문에 submit path가 열리지 않았다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-16-1231-after-hours-autopilot-post-trade.json`

- Run: [[2026-06-16-1211-after-hours-autopilot]]
- Open/new: 없음. 이번 cycle에서는 `place_stock_order`를 호출하지 않았고 신규 `client_order_id`도 만들지 않았다.
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `1211` core preflight와 direct `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-15T20:00:00Z)/get_stock_latest_quote(feed=overnight)/get_stock_snapshot(feed=overnight)` continuity 기준 account `ACTIVE`, positions `33`건, open orders `0`건, same-session after-hours orders `0`건이었다. watchlists `0`건은 scheduler-owned core preflight row를 유지했다.
- Recent reconciliation scope: scheduler-owned `1211` core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. direct `overnight` quote check는 `QQQ/RGTI/NOK/TSLA/SMH/SLB/AVGO/GE/SPY/MSFT/PFE`를 재확인했고 freshness fail은 `SLB`만 약 `19.09`분 stale로 남았다. `AVGO/PFE`는 same-day duplicate sell discipline, `RGTI`는 duplicate sell plus spread cap, `MSFT`는 same-day duplicate buy와 review backlog throttle, `NOK`는 add-block, `QQQ/SPY/SMH`는 per-order cap, `TSLA`는 watch-only thesis, `SLB/GE`는 spread 또는 freshness fail 때문에 submit path가 열리지 않았다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-16-1211-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-16-1151-after-hours-autopilot]]
- Open/new: 없음. 이번 cycle에서는 `place_stock_order`를 호출하지 않았고 신규 `client_order_id`도 만들지 않았다.
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `1151` core preflight와 direct `get_all_positions/get_watchlists/get_orders(status=open)/get_orders(status=all, after=2026-06-15T20:00:00Z)/get_account_activities(activity_types=[FILL], after=2026-06-15T20:00:00Z)/get_stock_latest_quote(feed=overnight)/get_stock_snapshot(feed=overnight)` continuity 기준 account `ACTIVE`, positions `33`건, watchlists `0`건, same-session after-hours orders/fills `0`건이었다.
- Recent reconciliation scope: scheduler-owned `1151` core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. direct `overnight` quote check는 `QQQ/RGTI/NOK/TSLA/SMH/SLB/AVGO/GE/SPY/MSFT/PFE`를 재확인했고 freshness gate는 `GE`만 약 `35.74`분 stale로 실패했다. 다만 `AVGO/PFE`는 same-day duplicate sell discipline, `RGTI`는 duplicate sell plus spread cap, `MSFT`는 same-day duplicate buy와 review backlog throttle, `NOK`는 add-block, `QQQ/SPY/SMH`는 per-order cap, `TSLA`는 watch-only thesis, `SLB/GE`는 spread 또는 freshness fail 때문에 submit path가 열리지 않았다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-16-1151-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-16-1131-after-hours-autopilot]]
- Open/new: 없음. 이번 cycle에서는 `place_stock_order`를 호출하지 않았고 신규 `client_order_id`도 만들지 않았다.
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `1131` core preflight와 direct `get_clock/get_account_info/get_all_positions/get_watchlists/get_orders(status=open)/get_orders(status=all, after=2026-06-15T20:00:00Z)/get_account_activities(activity_types=[FILL], after=2026-06-15T20:00:00Z)/get_stock_latest_quote(feed=overnight)` continuity 기준 account `ACTIVE`, positions `33`건, watchlists `0`건, same-session after-hours orders/fills `0`건이었다.
- Recent reconciliation scope: scheduler-owned `1131` core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. direct `overnight` quote check는 `QQQ/RGTI/NOK/TSLA/SMH/SLB/AVGO/GE/SPY/MSFT/PFE`를 재확인했고 freshness gate는 `GE`만 약 `16.27`분 stale로 실패했다. 다만 `AVGO/PFE/SLB/GE`는 spread cap fail, `RGTI/AVGO/PFE`는 same-day duplicate sell discipline, `MSFT`는 same-day duplicate buy와 review backlog throttle, `NOK`는 add-block, `QQQ/SPY/SMH`는 per-order cap, `TSLA`는 watch-only thesis 때문에 submit path가 열리지 않았다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-16-1131-after-hours-autopilot-post-trade.json`

_Last updated: 2026-06-16 11:13 KST_

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-16-1111-after-hours-autopilot]]
- Open/new: 없음. 이번 cycle에서는 `place_stock_order`를 호출하지 않았고 신규 `client_order_id`도 만들지 않았다.
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `1111` core preflight와 direct `get_clock/get_account_info/get_all_positions/get_watchlists/get_orders(status=open)/get_orders(status=all, after=2026-06-15T20:00:00Z)/get_account_activities(activity_types=[FILL], after=2026-06-15T20:00:00Z)/get_stock_latest_quote(feed=overnight)` continuity 기준 account `ACTIVE`, positions `33`건, watchlists `0`건, same-session after-hours orders/fills `0`건이었다.
- Recent reconciliation scope: scheduler-owned `1111` core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. direct `overnight` quote check는 `QQQ/RGTI/NOK/TSLA/SMH/SLB/AVGO/SPY/MSFT/PFE` fresh quote를 재확인했지만 `AVGO/RGTI/PFE`는 same-day duplicate sell discipline과 refreshed spread cap, `MSFT`는 same-day duplicate buy와 review backlog throttle, `NOK`는 add-block, `QQQ/SPY/SMH`는 per-order cap, `TSLA`는 watch-only thesis, `SLB/GE`는 spread 또는 freshness fail 때문에 submit path가 열리지 않았다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-16-1111-after-hours-autopilot-post-trade.json`

_Last updated: 2026-06-16 10:55 KST_

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-16-1051-after-hours-autopilot]]
- Open/new: 없음. 이번 cycle에서는 `place_stock_order`를 호출하지 않았고 신규 `client_order_id`도 만들지 않았다.
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `1051` core preflight와 direct `get_clock/get_account_info/get_all_positions/get_watchlists/get_orders(status=open)/get_orders(status=all, after=2026-06-15T20:00:00Z)/get_account_activities(activity_types=[FILL], after=2026-06-15T20:00:00Z)/get_stock_latest_quote(feed=overnight)` continuity 기준 account `ACTIVE`, positions `33`건, watchlists `0`건, same-session after-hours orders `0`건이었다.
- Recent reconciliation scope: scheduler-owned `1051` core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. direct `overnight` quote check는 `QQQ/RGTI/NOK/TSLA/SMH/SLB/AVGO/GE/SPY/MSFT/PFE` fresh quote를 재확인했지만 `AVGO/RGTI/PFE`는 same-day duplicate sell discipline, `MSFT/NOK`는 review backlog/add-block, `QQQ/SPY/SMH`는 per-order cap 또는 spread cap, `TSLA`는 watch-only thesis 때문에 submit path가 열리지 않았다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-16-1051-after-hours-autopilot-post-trade.json`

_Last updated: 2026-06-16 10:33 KST_

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-16-1031-after-hours-autopilot]]
- Open/new: 없음. 이번 cycle에서는 `place_stock_order`를 호출하지 않았고 신규 `client_order_id`도 만들지 않았다.
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `1031` core preflight와 direct `get_clock/get_account_info/get_all_positions/get_watchlists/get_orders(status=open)/get_orders(status=all, after=2026-06-15T20:00:00Z)/get_stock_latest_quote(feed=overnight)` continuity 기준 account `ACTIVE`, positions `33`건, watchlists `0`건, same-session after-hours orders `0`건이었다.
- Recent reconciliation scope: scheduler-owned `1031` core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. direct `overnight` quote check는 `QQQ/RGTI/NOK/TSLA/SMH/SLB/AVGO/GE/SPY/MSFT/PFE` fresh quote를 재확인했지만 `AVGO/RGTI/PFE`는 duplicate sell discipline 또는 spread cap, `MSFT/NOK`는 review backlog/add-block, `QQQ/SPY/SMH`는 per-order cap, `TSLA`는 watch-only thesis 때문에 submit path가 열리지 않았다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-16-1031-after-hours-autopilot-post-trade.json`

_Last updated: 2026-06-16 09:53 KST_

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-16-0951-after-hours-autopilot]]
- Open/new: 없음. 이번 cycle에서는 `place_stock_order`를 호출하지 않았고 신규 `client_order_id`도 만들지 않았다.
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `0951` core preflight와 direct `get_clock/get_account_info/get_all_positions/get_watchlists/get_orders(status=open)/get_orders(status=all, after=2026-06-15T20:00:00Z)/get_stock_latest_quote(feed=overnight)/get_stock_snapshot(feed=overnight)` continuity 기준 account `ACTIVE`, positions `33`건, watchlists `0`건, same-session after-hours orders `0`건이었다.
- Recent reconciliation scope: scheduler-owned `0951` core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. direct `overnight` quote check는 `QQQ/RGTI/NOK/TSLA/SMH/AVGO/SPY/MSFT/PFE` fresh quote를 재확인했지만 `AVGO/RGTI/PFE`는 same-day duplicate sell discipline, `MSFT/NOK`는 review backlog/add-block, `QQQ/SPY/SMH`는 per-order cap, `NOK`는 spread cap 때문에 submit path가 열리지 않았다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-16-0951-after-hours-autopilot-post-trade.json`


_Last updated: 2026-06-16 09:33 KST_

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-16-0931-after-hours-autopilot]]
- Open/new: 없음. 이번 cycle에서는 `place_stock_order`를 호출하지 않았고 신규 `client_order_id`도 만들지 않았다.
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `0931` core preflight와 direct `get_clock/get_account_info/get_all_positions/get_watchlists/get_orders(status=open)/get_orders(status=all, after=2026-06-15T20:00:00Z)/get_stock_latest_quote(feed=overnight)/get_stock_snapshot(feed=overnight)` continuity 기준 account `ACTIVE`, positions `33`건, watchlists `0`건, same-session after-hours orders `0`건이었다.
- Recent reconciliation scope: scheduler-owned `0931` core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. direct `overnight` quote check는 `QQQ/MSFT/NOK/PFE/AVGO/TSLA/SPY/SMH` fresh quote를 재확인했지만 `AVGO/RGTI/PFE`는 same-day duplicate sell discipline 또는 spread cap, `MSFT/NOK`는 review backlog/add-block, `QQQ/SPY/SMH`는 per-order cap 때문에 submit path가 열리지 않았다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-16-0931-after-hours-autopilot-post-trade.json`


## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-16-0911-after-hours-autopilot]]
- Open/new: 없음. 이번 cycle에서는 `place_stock_order`를 호출하지 않았고 신규 `client_order_id`도 만들지 않았다.
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `0911` core preflight와 direct `get_clock/get_account_info/get_all_positions/get_watchlists/get_orders(status=open)/get_orders(status=all, after=2026-06-15T20:00:00Z)/get_stock_latest_quote(feed=iex, overnight)/get_stock_snapshot(feed=iex)` continuity 기준 account `ACTIVE`, positions `33`건, watchlists `0`건, same-session after-hours orders `0`건이었다.
- Recent reconciliation scope: scheduler-owned `0911` core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. direct `overnight` quote check는 `QQQ/MSFT/NOK/AVGO/TSLA/SPY` fresh quote를 회복했지만 `AVGO/RGTI/PFE`는 same-day duplicate sell discipline 또는 spread cap, `MSFT/NOK/QQQ/SPY`는 review backlog throttle, add-block, per-order cap 때문에 submit path가 열리지 않았다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-16-0911-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-16-0851-after-hours-autopilot]]
- Open/new: 없음. 이번 cycle에서는 `place_stock_order`를 호출하지 않았고 신규 `client_order_id`도 만들지 않았다.
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `0851` core preflight와 direct `get_clock/get_account_info/get_all_positions/get_watchlists/get_orders(status=open)/get_orders(status=all, after=2026-06-15T20:00:00Z)/get_account_activities(activity_types=[FILL], after=2026-06-15T20:00:00Z)` continuity 기준 account `ACTIVE`, positions `33`건, watchlists `0`건, same-session after-hours orders/fills `0`건이었다.
- Recent reconciliation scope: scheduler-owned `0851` core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. same preflight quote 기준 freshest `QQQ`도 약 `180.64`분 stale였고 direct Alpaca MCP continuity quote check도 더 나은 submit-boundary quote를 주지 못했다. `RGTI/NOK/SLB/AVGO/PFE/MSFT/TSLA/GE/SMH`는 spread 또는 freshness cap을 동시에 위반했고 `SPY`는 bid-only quote라 submit path가 열리지 않았다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-16-0851-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-16-0831-after-hours-autopilot]]
- Open/new: 없음. 이번 cycle에서는 `place_stock_order`를 호출하지 않았고 신규 `client_order_id`도 만들지 않았다.
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `0831` core preflight 기준 account `ACTIVE`, positions `33`건, watchlists `0`건, same-session after-hours orders `0`건이었다.
- Recent reconciliation scope: scheduler-owned `0831` core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. same preflight quote 기준 freshest `QQQ`도 약 `160.63`분 stale였고 `RGTI/NOK/SLB/AVGO/PFE/MSFT/TSLA/GE/SMH`는 spread 또는 freshness cap을 동시에 위반했다. `SPY`는 bid-only quote라 submit path가 열리지 않았다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-16-0831-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-16-0811-after-hours-autopilot]]
- Open/new: 없음. 이번 cycle에서는 `place_stock_order`를 호출하지 않았고 신규 `client_order_id`도 만들지 않았다.
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `0811` core preflight 기준 account `ACTIVE`, positions `33`건, watchlists `0`건, same-session after-hours orders `0`건이었다.
- Recent reconciliation scope: scheduler-owned `0811` core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. same preflight quote 기준 freshest `QQQ`도 약 `140.63`분 stale였고 `RGTI/NOK/SLB/AVGO/PFE/MSFT/TSLA/GE/SMH`는 spread 또는 freshness cap을 동시에 위반했다. `SPY`는 bid-only quote라 submit path가 열리지 않았다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-16-0811-after-hours-autopilot-post-trade.json`

_Last updated: 2026-06-16 07:53 KST_

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-16-0751-after-hours-autopilot]]
- Open/new: 없음. 이번 cycle에서는 `place_stock_order`를 호출하지 않았고 신규 `client_order_id`도 만들지 않았다.
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `0751` core preflight와 direct `get_clock/get_account_info/get_all_positions/get_watchlists/get_orders(status=all, after=2026-06-15T20:00:00Z)/get_orders(status=open)` continuity 기준 account `ACTIVE`, positions `33`건, watchlists `0`건, same-session after-hours orders `0`건이었다.
- Recent reconciliation scope: scheduler-owned `0751` core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. direct `get_stock_latest_quote(feed=iex)` readback 기준 freshest `QQQ`도 약 `123.13`분 stale였고 `RGTI/NOK/SLB/AVGO/PFE/MSFT/TSLA/GE/SMH`는 spread 또는 freshness cap을 동시에 위반했다. `overnight` feed와 `get_stock_snapshot(feed=overnight)`도 더 나은 submit-boundary quote를 주지 못했고 `boats`는 subscription `403`으로 unavailable이라 submit path가 열리지 않았다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-16-0751-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-16-0731-after-hours-autopilot]]
- Open/new: 없음. 이번 cycle에서는 `place_stock_order`를 호출하지 않았고 신규 `client_order_id`도 만들지 않았다.
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `0731` core preflight와 direct `get_clock/get_account_info/get_all_positions/get_watchlists/get_orders(status=all, after=2026-06-15T20:00:00Z)/get_orders(status=open)` continuity 기준 account `ACTIVE`, positions `33`건, watchlists `0`건, same-session after-hours orders `0`건이었다.
- Recent reconciliation scope: scheduler-owned `0731` core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. direct `get_stock_latest_quote(feed=iex)` readback 기준 freshest `QQQ`도 약 `102.45`분 stale였고 `RGTI/NOK/SLB/AVGO/PFE/MSFT/TSLA/GE/SMH`는 spread 또는 freshness cap을 동시에 위반했다. `overnight` feed와 `get_stock_snapshot(feed=overnight)`도 더 나은 submit-boundary quote를 주지 못했고 `boats`는 subscription `403`으로 unavailable이라 submit path가 열리지 않았다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-16-0731-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-16-0711-after-hours-autopilot]]
- Open/new: 없음. 이번 cycle에서는 `place_stock_order`를 호출하지 않았고 신규 `client_order_id`도 만들지 않았다.
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `0711` core preflight와 direct `get_clock/get_account_info/get_all_positions/get_watchlists/get_orders(status=all, after=2026-06-15T20:00:00Z)/get_orders(status=open)` continuity 기준 account `ACTIVE`, positions `33`건, watchlists `0`건, same-session after-hours orders `0`건이었다.
- Recent reconciliation scope: scheduler-owned `0711` core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. direct `get_stock_latest_quote(feed=iex)` readback 기준 freshest `QQQ`도 약 `83.15`분 stale였고 `RGTI/NOK/SLB/AVGO/PFE/MSFT/TSLA/GE/SMH`는 spread 또는 freshness cap을 동시에 위반했다. `overnight` feed와 `get_stock_snapshot(feed=overnight)`도 더 나은 submit-boundary quote를 주지 못해 submit path가 열리지 않았다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-16-0711-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-16-0651-after-hours-autopilot]]
- Open/new: 없음. 이번 cycle에서는 `place_stock_order`를 호출하지 않았고 신규 `client_order_id`도 만들지 않았다.
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `0651` core preflight와 direct `get_clock/get_account_info/get_all_positions/get_watchlists/get_account_activities(activity_types=[FILL], after=2026-06-15T20:00:00Z)` continuity 기준 account `ACTIVE`, positions `33`건, watchlists `0`건, same-session after-hours fills `0`건이었다.
- Recent reconciliation scope: scheduler-owned `0651` core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. direct `get_stock_latest_quote(feed=iex)` readback 기준 freshest `QQQ`도 약 `62.84`분 stale였고 `RGTI/NOK/SLB/AVGO/PFE/MSFT/TSLA/GE/SMH`는 spread 또는 freshness cap을 동시에 위반해 submit path가 열리지 않았다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-16-0651-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-16-0631-after-hours-autopilot]]
- Open/new: 없음. 이번 cycle에서는 `place_stock_order`를 호출하지 않았고 신규 `client_order_id`도 만들지 않았다.
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `0631` core preflight와 direct `get_clock/get_account_info/get_all_positions/get_watchlists/get_orders(status=all, after=2026-06-15T20:00:00Z)/get_orders(status=open)` continuity 기준 account `ACTIVE`, positions `33`건, watchlists `0`건, same-session after-hours orders `0`건이었다.
- Recent reconciliation scope: scheduler-owned `0631` core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 after-hours expected nonblocking으로 처리했다. direct `get_stock_latest_quote(feed=iex)`와 `get_stock_snapshot(feed=iex)` readback 기준 freshest `QQQ`도 약 `42.29`분 stale였고 `RGTI/NOK/SLB/AVGO/PFE/MSFT/TSLA/GE/SMH`는 spread 또는 freshness cap을 동시에 위반해 submit path가 열리지 않았다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-16-0631-after-hours-autopilot-post-trade.json`

_Last updated: 2026-06-16 04:59 KST_

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-16-0451-hourly-autopilot]]
- Open/new: 없음. direct Alpaca MCP `get_order_by_client_id`와 `get_orders(status=open)` reconciliation 기준 신규 open order는 남지 않았다.
- Filled: `PFE` sell `1주`가 `filled_avg_price=26.01 USD`로 즉시 체결됐다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: direct `get_account_info/get_all_positions/get_order_by_client_id/get_orders(status=open)` reconciliation 기준 account `ACTIVE`, positions `33`건, open orders `0`건, `PFE qty=4`, `avg_entry_price=25.972`, cash `29,836.36 USD`였다.
- Recent reconciliation scope: scheduler-owned `0451` stale cleanup/core/research preflight를 source-of-record로 사용했고 actual submit은 `2026-06-15T19:59:38.494910487Z`에 `client_order_id=hourly-20260616-0451-sell-pfe`로 수행했다. direct Alpaca MCP `get_order_by_client_id` 기준 same order는 `2026-06-15T19:59:48.06371096Z`에 `status=filled`, `filled_qty=1`, `filled_avg_price=26.01 USD`로 확정됐다.
- Orders submitted/replaced/cancelled/closed by this workflow: 1 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-16-0451-hourly-autopilot-post-trade.json`

_Last updated: 2026-06-16 04:39 KST_

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-16-0431-hourly-autopilot]]
- Open/new: 없음. direct Alpaca MCP `get_order_by_client_id`와 `get_orders(status=open)` reconciliation 기준 신규 open order는 남지 않았다.
- Filled: `AAPL` buy `1주`가 `filled_avg_price=296.11 USD`로 즉시 체결됐다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: direct `get_account_info/get_all_positions/get_order_by_client_id/get_orders(status=open)` reconciliation 기준 account `ACTIVE`, positions `33`건, open orders `0`건, `AAPL qty=6`, `avg_entry_price=301.965`, cash `29,810.35 USD`였다.
- Recent reconciliation scope: scheduler-owned `0431` stale cleanup/core/research preflight를 source-of-record로 사용했고 actual submit은 `2026-06-15T19:39:21.509318894Z`에 `client_order_id=hourly-20260616-0431-buy-aapl`로 수행했다. direct Alpaca MCP `get_order_by_client_id` 기준 same order는 `2026-06-15T19:39:22.121175974Z`에 `status=filled`, `filled_qty=1`, `filled_avg_price=296.11 USD`로 확정됐다.
- Orders submitted/replaced/cancelled/closed by this workflow: 1 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-16-0431-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-16-0411-hourly-autopilot]]
- Open/new: 없음. direct Alpaca MCP `get_order_by_client_id`와 `get_orders(status=open)` reconciliation 기준 신규 open order는 남지 않았다.
- Filled: `AMZN` buy `1주`가 `filled_avg_price=246.19 USD`로 즉시 체결됐다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: direct `get_account_info/get_all_positions/get_order_by_client_id/get_orders(status=open)` reconciliation 기준 account `ACTIVE`, positions `33`건, open orders `0`건, `AMZN qty=7`, `avg_entry_price=256.778571`, cash `30,106.46 USD`였다.
- Recent reconciliation scope: scheduler-owned `0411` stale cleanup/core/research preflight를 source-of-record로 사용했고 actual submit은 `2026-06-15T19:19:09.55429596Z`에 `client_order_id=hourly-20260616-0411-buy-amzn`로 수행했다. direct Alpaca MCP `get_order_by_client_id` 기준 same order는 `2026-06-15T19:19:10.463829694Z`에 `status=filled`, `filled_qty=1`, `filled_avg_price=246.19 USD`로 확정됐다.
- Orders submitted/replaced/cancelled/closed by this workflow: 1 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-16-0411-hourly-autopilot-post-trade.json`


_Last updated: 2026-06-16 03:59 KST_

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-16-0351-hourly-autopilot]]
- Open/new: 없음. direct Alpaca MCP `get_order_by_client_id` 최종 상태와 `get_all_positions` reconciliation 기준 신규 open order는 남지 않았다.
- Filled: `GOOGL` buy `1주`가 `filled_avg_price=371.22 USD`로 즉시 체결됐다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned core preflight + direct `get_order_by_client_id/get_all_positions` reconciliation 기준 positions `33`건, `GOOGL qty=4`, `avg_entry_price=378.945`였다. post-submit `get_account_info`는 이 runtime에 노출되지 않아 cash는 pre-submit `30,723.87 USD`에서 fill `371.22 USD`를 차감한 `30,352.65 USD` 추정치로 기록한다.
- Recent reconciliation scope: scheduler-owned `0351` stale cleanup/core/research preflight를 source-of-record로 사용했고 actual submit은 `2026-06-15T18:58:46.497795092Z`에 `client_order_id=hourly-20260616-0351-buy-googl`로 수행했다. direct Alpaca MCP `get_order_by_client_id` 기준 same order는 `2026-06-15T18:58:47.524255326Z`에 `status=filled`, `filled_qty=1`, `filled_avg_price=371.22 USD`로 확정됐다.
- Orders submitted/replaced/cancelled/closed by this workflow: 1 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-16-0351-hourly-autopilot-post-trade.json`


_Last updated: 2026-06-16 03:39 KST_

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-16-0331-hourly-autopilot]]
- Open/new: 없음. direct Alpaca MCP `get_orders(status=open)` 기준 open orders `0`건이다.
- Filled: `MSFT` buy `1주`가 `filled_avg_price=398.71 USD`로 즉시 체결됐다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: direct `get_account_info/get_all_positions/get_order_by_client_id/get_orders(status=open)` reconciliation 기준 account `ACTIVE`, positions `33`건, open orders `0`건, `MSFT qty=4`, cash `30,723.87 USD`였다.
- Recent reconciliation scope: scheduler-owned `0331` stale cleanup/core/research preflight를 source-of-record로 사용했고 actual submit은 `2026-06-15T18:39:13.500811516Z`에 `client_order_id=hourly-20260616-0331-buy-msft`로 수행했다. direct Alpaca MCP `get_order_by_client_id` 기준 same order는 `2026-06-15T18:39:13.952806277Z`에 `status=filled`, `filled_qty=1`, `filled_avg_price=398.71 USD`로 확정됐다.
- Orders submitted/replaced/cancelled/closed by this workflow: 1 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-16-0331-hourly-autopilot-post-trade.json`

_Last updated: 2026-06-16 03:18 KST_

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-16-0311-hourly-autopilot]]
- Open/new: `SO` buy `1주`가 `status=new` open order로 생성됐다. direct Alpaca MCP `get_orders(status=open)` 기준 open orders `1`건이다.
- Filled: immediate reconciliation 시점 신규 fill 없음.
- Cancelled: 없음
- Position count observed by Alpaca MCP: direct `get_account_info/get_all_positions/get_order_by_client_id/get_orders(status=open)` reconciliation 기준 account `ACTIVE`, positions `33`건, open orders `1`건, `SO qty=5`, `qty_available=5`, cash `31,216.95 USD`였다.
- Recent reconciliation scope: scheduler-owned `0311` stale cleanup/core/research preflight를 source-of-record로 사용했고 actual submit은 `2026-06-15T18:18:29.236351179Z`에 `client_order_id=hourly-20260616-0311-buy-so`로 수행했다. direct Alpaca MCP `get_order_by_client_id` 기준 same order는 immediate reconciliation 시점 `status=new`, `filled_qty=0`, `limit_price=94.37 USD`였다.
- Orders submitted/replaced/cancelled/closed by this workflow: 1 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-16-0311-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-16-0251-hourly-autopilot]]
- Open/new: 없음. direct Alpaca MCP `get_orders(status=open)` 기준 open orders `0`건이다.
- Filled: `V` buy `1주`가 `filled_avg_price=324.83 USD`로 즉시 체결됐다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: direct `get_account_info/get_all_positions/get_order_by_id/get_orders(status=open)` reconciliation 기준 account `ACTIVE`, positions `33`건, open orders `0`건, `V qty=5`, cash `31,216.95 USD`였다.
- Recent reconciliation scope: scheduler-owned `0251` stale cleanup/core/research preflight를 source-of-record로 사용했고 actual submit은 `2026-06-15T17:55:48.301773194Z`에 `client_order_id=hourly-20260616-0251-buy-v`로 수행했다. direct Alpaca MCP `get_order_by_id` 기준 same order는 `2026-06-15T17:55:48.922618101Z`에 `status=filled`, `filled_qty=1`, `filled_avg_price=324.83 USD`로 확정됐다.
- Orders submitted/replaced/cancelled/closed by this workflow: 1 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-16-0251-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-16-0231-hourly-autopilot]]
- Open/new: 없음. direct Alpaca MCP `get_orders(status=open)` 기준 open orders `0`건이다.
- Filled: `COP` buy `1주`가 `filled_avg_price=112.62 USD`로 즉시 체결됐다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: direct `get_account_info/get_all_positions/get_order_by_client_id/get_orders(status=open)` reconciliation 기준 account `ACTIVE`, positions `33`건, open orders `0`건, `COP qty=6`, cash `31,541.78 USD`였다.
- Recent reconciliation scope: scheduler-owned `0231` stale cleanup/core/research preflight를 source-of-record로 사용했고 actual submit은 `2026-06-15T17:39:15.392200739Z`에 `client_order_id=hourly-20260616-0231-buy-cop`로 수행했다. direct Alpaca MCP `get_order_by_client_id` 기준 same order는 `2026-06-15T17:39:15.996053768Z`에 `status=filled`, `filled_qty=1`, `filled_avg_price=112.62 USD`로 확정됐다.
- Orders submitted/replaced/cancelled/closed by this workflow: 1 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-16-0231-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-16-0211-hourly-autopilot]]
- Open/new: 없음. direct Alpaca MCP `get_orders(status=open)` 기준 open orders `0`건이다.
- Filled: `NKE` buy `1주`가 `filled_avg_price=45.36 USD`로 즉시 체결됐다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: direct `get_account_info/get_all_positions/get_order_by_client_id/get_orders(status=open)` reconciliation 기준 account `ACTIVE`, positions `33`건, open orders `0`건, `NKE qty=6`, cash `31,654.40 USD`였다.
- Recent reconciliation scope: scheduler-owned `0211` stale cleanup/core/research preflight를 source-of-record로 사용했고 actual submit은 `2026-06-15T17:18:02.588739065Z`에 `client_order_id=hourly-20260616-0211-buy-nke`로 수행했다. direct Alpaca MCP `get_order_by_client_id` 기준 same order는 `2026-06-15T17:18:03.494379872Z`에 `status=filled`, `filled_qty=1`, `filled_avg_price=45.36 USD`로 확정됐다.
- Orders submitted/replaced/cancelled/closed by this workflow: 1 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-16-0211-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-16-0131-hourly-autopilot]]
- Open/new: 없음. direct Alpaca MCP `get_orders(status=open)` 기준 open orders `0`건이다.
- Filled: `SLB` buy `1주`가 `filled_avg_price=54.03 USD`로 즉시 체결됐다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: direct `get_account_info/get_all_positions/get_order_by_client_id/get_orders(status=open)` reconciliation 기준 account `ACTIVE`, positions `33`건, open orders `0`건, `SLB qty=7`, cash `31,841.52 USD`였다.
- Recent reconciliation scope: scheduler-owned `0131` stale cleanup/core/research preflight를 source-of-record로 사용했고 actual submit은 `2026-06-15T16:41:54.112515184Z`에 `client_order_id=hourly-20260616-0131-buy-slb`로 수행했다. direct Alpaca MCP `get_order_by_client_id` 기준 same order는 `2026-06-15T16:41:54.775972455Z`에 `status=filled`, `filled_qty=1`, `filled_avg_price=54.03 USD`로 확정됐다.
- Orders submitted/replaced/cancelled/closed by this workflow: 1 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-16-0131-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-16-0111-hourly-autopilot]]
- Open/new: `FCX` buy `1주`가 `status=new` open order로 생성됐다.
- Filled: immediate reconciliation 시점 신규 fill 없음.
- Cancelled: 없음
- Position count observed by Alpaca MCP: direct `get_account_info/get_all_positions/get_order_by_client_id/get_orders(status=open)` reconciliation 기준 account `ACTIVE`, positions `33`건, open orders `1`건, `FCX qty=5`, cash `31,965.04 USD`였다.
- Recent reconciliation scope: scheduler-owned `0111` stale cleanup/core/research preflight를 source-of-record로 사용했고 actual submit은 `2026-06-15T16:21:07.887496306Z`에 `client_order_id=hourly-20260616-0111-buy-fcx`로 수행했다. direct Alpaca MCP `get_order_by_client_id` 기준 same order는 immediate reconciliation 시점 `status=new`, `filled_qty=0`, `limit_price=69.49 USD`였다.
- Orders submitted/replaced/cancelled/closed by this workflow: 1 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-16-0111-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-16-0051-hourly-autopilot]]
- Open/new: 없음. direct Alpaca MCP `get_orders(status=open)` 기준 open orders `0`건이다.
- Filled: `JPM` buy `1주`가 `filled_avg_price=321.53 USD`로 즉시 체결됐다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: direct `get_account_info/get_all_positions/get_order_by_client_id/get_orders(status=open)` reconciliation 기준 account `ACTIVE`, positions `33`건, open orders `0`건, `JPM qty=2`, cash `31,965.04 USD`였다.
- Recent reconciliation scope: scheduler-owned `0051` stale cleanup/core/research preflight를 source-of-record로 사용했고 actual submit은 `2026-06-15T16:00:27.504281013Z`에 `client_order_id=hourly-20260616-0051-buy-jpm`로 수행했다. direct Alpaca MCP `get_order_by_client_id` 기준 same order는 `2026-06-15T16:00:28.027169137Z`에 `status=filled`, `filled_qty=1`, `filled_avg_price=321.53 USD`로 확정됐다.
- Orders submitted/replaced/cancelled/closed by this workflow: 1 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-16-0051-hourly-autopilot-post-trade.json`

_Last updated: 2026-06-16 00:38 KST_

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-16-0031-hourly-autopilot]]
- Open/new: 없음. direct Alpaca MCP `get_orders(status=open)` 기준 open orders `0`건이다.
- Filled: `NEE` buy `1주`가 `filled_avg_price=85.78 USD`로 즉시 체결됐다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: direct `get_account_info/get_all_positions/get_order_by_client_id/get_orders(status=open)` reconciliation 기준 account `ACTIVE`, positions `33`건, open orders `0`건, `NEE qty=6`, cash `32,286.57 USD`였다.
- Recent reconciliation scope: scheduler-owned `0031` stale cleanup/core/research preflight를 source-of-record로 사용했고 actual submit은 `2026-06-15T15:37:52.039512771Z`에 `client_order_id=hourly-20260616-0031-buy-nee`로 수행했다. direct Alpaca MCP `get_order_by_client_id` 기준 same order는 `2026-06-15T15:37:52.982253179Z`에 `status=filled`, `filled_qty=1`, `filled_avg_price=85.78 USD`로 확정됐다.
- Orders submitted/replaced/cancelled/closed by this workflow: 1 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-16-0031-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-16-0011-hourly-autopilot]]
- Open/new: 없음. direct Alpaca MCP `get_orders(status=open)` 기준 open orders `0`건이다.
- Filled: `AVGO` sell `1주`가 `filled_avg_price=392.14 USD`로 즉시 체결됐다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: direct `get_account_info/get_all_positions/get_order_by_client_id/get_orders(status=open)` reconciliation 기준 account `ACTIVE`, positions `33`건, open orders `0`건, `AVGO qty=2`, cash `32,372.35 USD`였다.
- Recent reconciliation scope: scheduler-owned `0011` stale cleanup/core/research preflight를 source-of-record로 사용했고 actual submit은 `2026-06-15T15:18:03.437536674Z`에 `client_order_id=hourly-20260616-0011-sell-avgo`로 수행했다. direct Alpaca MCP `get_order_by_client_id` 기준 same order는 `2026-06-15T15:18:03.982786708Z`에 `status=filled`, `filled_qty=1`, `filled_avg_price=392.14 USD`로 확정됐다.
- Orders submitted/replaced/cancelled/closed by this workflow: 1 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-16-0011-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-15-2351-hourly-autopilot]]
- Open/new: 신규 submit 없음. scheduler-owned core preflight `get_orders_open` row는 `0`건이지만, stale cleanup artifact에는 `AVGO` sell `1주`가 `status=pending_cancel` remaining open order로 남았다.
- Filled: scheduler-owned core preflight `get_account_activities` 기준 same-session `WMT` buy `1주`(`120.20 USD`)와 `BAC` buy `1주`(`56.28 USD`) 체결이 반영됐다.
- Cancelled: scheduler-owned stale cleanup은 `AVGO` stale sell cancel attempt를 `pass`로 기록했지만 artifact 시점에는 lifecycle 정리가 끝나지 않았다.
- Position count observed by Alpaca MCP: scheduler-owned core preflight 기준 account `ACTIVE`, positions `33`건, open orders row `0`건, `WMT qty=9`, `BAC qty=7`, `AVGO qty=3`, cash `31,980.21 USD`였다.
- Recent reconciliation scope: scheduler-owned `2351` stale cleanup/core/research preflight를 source-of-record로 사용했다. workflow-required stale cleanup artifact가 unresolved `pending_cancel`을 남겨 `risk_open_order_lifecycle` hard gate가 발생했고, 이번 cycle은 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-15-2351-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-15-2331-hourly-autopilot]]
- Open/new: `WMT` buy `1주`가 `status=new` open order로 생성됐고, earlier `AVGO` sell `1주` open order도 유지됐다.
- Filled: immediate reconciliation 시점 신규 fill 없음.
- Cancelled: 없음
- Position count observed by Alpaca MCP: direct `get_account_info/get_all_positions/get_order_by_client_id/get_orders(status=open)` reconciliation 기준 account `ACTIVE`, positions `33`건, open orders `2`건, `WMT qty=8`, `AVGO qty=3`, `AVGO qty_available=2`, cash `32100.41 USD`였다.
- Recent reconciliation scope: scheduler-owned `2331` stale cleanup/core/research preflight를 source-of-record로 사용했고 actual submit은 `2026-06-15T14:40:08.28247584Z`에 `client_order_id=hourly-20260615-2331-buy-wmt`로 수행했다. direct Alpaca MCP `get_order_by_client_id` 기준 same order는 immediate reconciliation 시점 `status=new`, `filled_qty=0`, `limit_price=120.20 USD`였다.
- Orders submitted/replaced/cancelled/closed by this workflow: 1 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-15-2331-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-15-2311-hourly-autopilot]]
- Open/new: `BAC` buy `1주`가 `status=new` open order로 생성됐고, earlier `AVGO` sell `1주` open order도 유지됐다.
- Filled: immediate reconciliation 시점 신규 fill 없음.
- Cancelled: 없음
- Position count observed by Alpaca MCP: direct `get_account_info/get_all_positions/get_order_by_client_id/get_orders(status=open)` reconciliation 기준 account `ACTIVE`, positions `33`건, open orders `2`건, `BAC qty=6`, `AVGO qty=3`, `AVGO qty_available=2`, cash `32156.69 USD`였다.
- Recent reconciliation scope: scheduler-owned `2311` stale cleanup/core/research preflight를 source-of-record로 사용했고 actual submit은 `2026-06-15T14:19:38.883379405Z`에 `client_order_id=hourly-20260615-2311-buy-bac`로 수행했다. direct Alpaca MCP `get_order_by_client_id` 기준 same order는 immediate reconciliation 시점 `status=new`, `filled_qty=0`, `limit_price=56.28 USD`였다.
- Orders submitted/replaced/cancelled/closed by this workflow: 1 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-15-2311-hourly-autopilot-post-trade.json`


## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-15-2251-hourly-autopilot]]
- Open/new: `AVGO` sell `1주`가 `status=new` open order로 생성됐다.
- Filled: immediate reconciliation 시점 신규 fill 없음.
- Cancelled: 없음
- Position count observed by Alpaca MCP: direct `get_account_info/get_all_positions/get_order_by_client_id/get_account_activities` reconciliation 기준 account `ACTIVE`, positions `33`건, `AVGO qty=3`, `qty_available=2`, cash `32156.69 USD`였다.
- Recent reconciliation scope: scheduler-owned `2251` stale cleanup/core/research preflight를 source-of-record로 사용했고 actual submit은 `2026-06-15T14:02:23.793160947Z`에 `client_order_id=hourly-20260615-2251-sell-avgo`로 수행했다. direct Alpaca MCP `get_order_by_client_id` 기준 same order는 immediate reconciliation 시점 `status=new`, `filled_qty=0`, `limit_price=394.9 USD`였고 `get_account_activities(activity_types=FILL, after=2026-06-15T14:02:00Z)`에는 아직 새 fill row가 없었다.
- Orders submitted/replaced/cancelled/closed by this workflow: 1 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-15-2251-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-15-2231-hourly-autopilot]]
- Open/new: 없음
- Filled: `RGTI` sell `9주`가 `filled_avg_price=23.366667 USD`로 즉시 체결됐다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: submit 직후 `get_account_info/get_all_positions/get_orders(status=open)` reconciliation 기준 account `ACTIVE`, positions `33`건, open orders `0`건이었다.
- Recent reconciliation scope: scheduler-owned `2231` stale cleanup/core/research preflight를 source-of-record로 사용했고 actual submit은 `2026-06-15T13:41:41.654523Z`에 `client_order_id=hourly-20260615-2231-sell-rgti`로 수행했다. direct Alpaca MCP `get_order_by_id/get_orders(status=all, symbols=RGTI, after=2026-06-15T13:25:00Z)/get_orders(status=open)/get_account_info/get_all_positions` reconciliation 기준 same order는 `2026-06-15T13:41:43.341983Z`에 `status=filled`, `filled_qty=9`, `filled_avg_price=23.366667 USD`로 확인됐고 `RGTI` 보유수량은 `37주 -> 28주`, cash는 `32156.69 USD`로 증가했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 1 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-15-2231-hourly-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-15-2151-after-hours-autopilot]]
- Open/new: 없음
- Filled: direct Alpaca MCP `get_orders(status=all, after=2026-06-14T20:00:00Z)`와 direct `get_order_by_client_id` readback 기준 earlier same-session fills `MSFT` buy `1주`(`395.87 USD`), `AVGO` sell `1주`(`391.92 USD`)가 모두 유지됐다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `get_clock/get_account_info/get_all_positions/get_orders_open/get_watchlists` preflight와 direct Alpaca MCP `get_all_positions/get_orders(status=open)/get_watchlists` 기준 regular market closed, account `ACTIVE`, positions `33`건, open orders `0`건, watchlists `0`건이었다.
- Recent reconciliation scope: scheduler-owned `2151` after-hours core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 expected nonblocking으로 처리했다. direct Alpaca MCP `get_clock/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-14T20:00:00Z)/get_watchlists/get_order_by_client_id/get_stock_latest_quote(feed=overnight)/get_stock_snapshot(feed=overnight)` continuity는 same-session fill continuity와 current position/open-order/watchlist count, overnight shortlist quote/trade continuity 재확인에만 사용했다. separate after-hours session budget은 `2/2`로 닫혀 있어 이번 cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-15-2151-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-15-2131-after-hours-autopilot]]
- Open/new: 없음
- Filled: direct Alpaca MCP `get_order_by_client_id` readback 기준 earlier same-session fills `MSFT` buy `1주`(`395.87 USD`), `AVGO` sell `1주`(`391.92 USD`)가 모두 유지됐다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `get_clock/get_account_info/get_all_positions/get_orders_open/get_watchlists` preflight와 direct Alpaca MCP `get_clock/get_all_positions/get_watchlists` 기준 regular market closed, account `ACTIVE`, positions `33`건, open orders `0`건, watchlists `0`건이었다.
- Recent reconciliation scope: scheduler-owned `2131` after-hours core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 expected nonblocking으로 처리했다. direct Alpaca MCP `get_clock/get_all_positions/get_watchlists/get_order_by_client_id/get_stock_latest_quote(feed=overnight)/get_stock_snapshot(feed=overnight)` continuity는 same-session fill continuity와 current position/watchlist count, overnight shortlist quote/trade continuity 재확인에만 사용했다. separate after-hours session budget은 `2/2`로 닫혀 있어 이번 cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-15-2131-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-15-2111-after-hours-autopilot]]
- Open/new: 없음
- Filled: direct Alpaca MCP `get_orders(status=all, after=2026-06-14T20:00:00Z)`와 direct `get_order_by_client_id` readback 기준 earlier same-session fills `MSFT` buy `1주`(`395.87 USD`), `AVGO` sell `1주`(`391.92 USD`)가 모두 유지됐다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `get_clock/get_account_info/get_all_positions/get_orders_open/get_watchlists` preflight와 direct Alpaca MCP `get_all_positions/get_orders(status=open)/get_watchlists` 기준 regular market closed, account `ACTIVE`, positions `33`건, open orders `0`건, watchlists `0`건이었다.
- Recent reconciliation scope: scheduler-owned `2111` after-hours core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 expected nonblocking으로 처리했다. direct Alpaca MCP `get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-14T20:00:00Z)/get_watchlists/get_order_by_client_id/get_stock_latest_quote(feed=overnight)/get_stock_snapshot(feed=overnight)` continuity는 same-session fill continuity와 current position/open-order/watchlist count, overnight shortlist quote/trade continuity 재확인에만 사용했다. separate after-hours session budget은 `2/2`로 닫혀 있어 이번 cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-15-2111-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-15-2051-after-hours-autopilot]]
- Open/new: 없음
- Filled: direct Alpaca MCP `get_orders(status=all, after=2026-06-14T20:00:00Z)`와 direct `get_order_by_client_id` readback 기준 same-session fills `MSFT` buy `1주`(`395.87 USD`), `AVGO` sell `1주`(`391.92 USD`)가 모두 유지됐다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `get_clock/get_account_info/get_all_positions/get_orders_open/get_watchlists` preflight와 direct Alpaca MCP `get_all_positions/get_orders(status=open)/get_watchlists` 기준 regular market closed, account `ACTIVE`, positions `33`건, open orders `0`건, watchlists `0`건이었다.
- Recent reconciliation scope: scheduler-owned `2051` after-hours core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 expected nonblocking으로 처리했다. direct Alpaca MCP `get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-14T20:00:00Z)/get_watchlists/get_order_by_client_id/get_stock_latest_quote(feed=overnight)/get_stock_snapshot(feed=overnight)` continuity는 same-session fill continuity와 current position/open-order/watchlist count, overnight shortlist quote/trade continuity 재확인에만 사용했다. separate after-hours session budget은 `2/2`로 닫혀 있어 이번 cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-15-2051-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-15-2011-after-hours-autopilot]]
- Open/new: 없음
- Filled: direct Alpaca MCP `get_orders(status=all, after=2026-06-14T20:00:00Z)`와 direct `get_order_by_client_id` readback 기준 earlier same-session fills `MSFT` buy `1주`(`395.87 USD`), `AVGO` sell `1주`(`391.92 USD`)가 모두 유지됐다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `get_clock/get_account_info/get_all_positions/get_orders_open/get_watchlists` preflight와 direct Alpaca MCP `get_all_positions/get_orders(status=open)/get_watchlists` 기준 regular market closed, account `ACTIVE`, positions `33`건, open orders `0`건, watchlists `0`건이었다.
- Recent reconciliation scope: scheduler-owned `2011` after-hours core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 expected nonblocking으로 처리했다. direct Alpaca MCP `get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-14T20:00:00Z)/get_watchlists/get_order_by_client_id/get_stock_latest_quote(feed=overnight)/get_stock_snapshot(feed=overnight)` continuity는 same-session fill continuity와 current position/open-order/watchlist count, overnight shortlist quote/trade continuity 재확인에만 사용했다. separate after-hours session budget은 `2/2`로 닫혀 있어 이번 cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-15-2011-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-15-1951-after-hours-autopilot]]
- Open/new: 없음
- Filled: direct Alpaca MCP `get_order_by_client_id` readback 기준 earlier same-session fills `MSFT` buy `1주`(`395.87 USD`), `AVGO` sell `1주`(`391.92 USD`)가 모두 유지됐다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `get_clock/get_account_info/get_all_positions/get_orders_open/get_watchlists` preflight와 direct Alpaca MCP `get_all_positions/get_orders(status=open)/get_watchlists` 기준 regular market closed, account `ACTIVE`, positions `33`건, open orders `0`건, watchlists `0`건이었다.
- Recent reconciliation scope: scheduler-owned `1951` after-hours core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 expected nonblocking으로 처리했다. direct Alpaca MCP `get_all_positions/get_orders(status=open)/get_watchlists/get_order_by_client_id/get_stock_latest_quote(feed=overnight)/get_stock_snapshot(feed=overnight)` continuity는 same-session fill continuity와 current position/open-order/watchlist count, overnight shortlist quote/trade continuity 재확인에만 사용했다. separate after-hours session budget은 `2/2`로 닫혀 있어 이번 cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-15-1951-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-15-1931-after-hours-autopilot]]
- Open/new: 없음
- Filled: scheduler-owned `get_account_activities(activity_types=FILL)` preflight row 기준 earlier same-session fills `MSFT` buy `1주`(`395.87 USD`), `AVGO` sell `1주`(`391.92 USD`)가 모두 유지됐다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `get_clock/get_account_info/get_all_positions/get_orders_open/get_watchlists` preflight와 direct Alpaca MCP `get_watchlists` 기준 regular market closed, account `ACTIVE`, positions `33`건, open orders `0`건, watchlists `0`건이었다.
- Recent reconciliation scope: scheduler-owned `1931` after-hours core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 expected nonblocking으로 처리했다. direct Alpaca MCP `get_watchlists/get_stock_latest_quote(feed=overnight)/get_stock_snapshot(feed=overnight)` spot-check는 watchlists `0`건과 overnight shortlist quote/trade continuity 재확인에만 사용했다. separate after-hours session budget은 `2/2`로 닫혀 있어 이번 cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-15-1931-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-15-1911-after-hours-autopilot]]
- Open/new: 없음
- Filled: direct Alpaca MCP `get_orders(status=all, after=2026-06-14T20:00:00Z)`와 direct `get_order_by_client_id` readback 기준 earlier same-session fills `MSFT` buy `1주`(`395.87 USD`), `AVGO` sell `1주`(`391.92 USD`)가 모두 유지됐다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `get_clock/get_account_info/get_all_positions/get_orders_open/get_watchlists` preflight와 direct Alpaca MCP `get_all_positions/get_orders(status=open)/get_watchlists` 기준 regular market closed, account `ACTIVE`, positions `33`건, open orders `0`건, watchlists `0`건이었다.
- Recent reconciliation scope: scheduler-owned `1911` after-hours core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 expected nonblocking으로 처리했다. direct Alpaca MCP `get_all_positions/get_orders(status=open)/get_watchlists/get_orders(status=all, after=2026-06-14T20:00:00Z)/get_order_by_client_id` continuity는 same-session fill continuity와 current position/open-order/watchlist count 재확인에만 사용했다. separate after-hours session budget은 `2/2`로 닫혀 있어 이번 cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-15-1911-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-15-1851-after-hours-autopilot]]
- Open/new: 없음
- Filled: scheduler-owned `get_account_activities(activity_types=FILL)` row와 direct Alpaca MCP `get_order_by_client_id` readback 기준 earlier same-session fills `MSFT` buy `1주`(`395.87 USD`), `AVGO` sell `1주`(`391.92 USD`)가 모두 유지됐다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `get_clock/get_account_info/get_all_positions/get_orders_open/get_watchlists` preflight와 direct Alpaca MCP `get_all_positions/get_orders(status=open)/get_watchlists` 기준 regular market closed, account `ACTIVE`, positions `33`건, open orders `0`건, watchlists `0`건이었다.
- Recent reconciliation scope: scheduler-owned `1851` after-hours core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 expected nonblocking으로 처리했다. direct Alpaca MCP `get_all_positions/get_orders(status=open)/get_watchlists/get_order_by_client_id` continuity는 same-session fill continuity와 current position/open-order/watchlist count 재확인에만 사용했다. separate after-hours session budget은 `2/2`로 닫혀 있어 이번 cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-15-1851-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-15-1831-after-hours-autopilot]]
- Open/new: 없음
- Filled: direct Alpaca MCP `get_order_by_client_id` readback 기준 earlier same-session fills `MSFT` buy `1주`(`395.87 USD`), `AVGO` sell `1주`(`391.92 USD`)가 모두 유지됐다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `get_clock/get_account_info/get_orders_open` preflight와 direct Alpaca MCP `get_all_positions/get_watchlists` 기준 regular market closed, account `ACTIVE`, positions `33`건, open orders `0`건, watchlists `0`건이었다.
- Recent reconciliation scope: scheduler-owned `1831` after-hours core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 expected nonblocking으로 처리했다. direct Alpaca MCP `get_all_positions/get_watchlists/get_order_by_client_id` continuity는 same-session fill continuity와 current position/watchlist count 재확인에만 사용했다. separate after-hours session budget은 `2/2`로 닫혀 있어 이번 cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-15-1831-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-15-1811-after-hours-autopilot]]
- Open/new: 없음
- Filled: scheduler-owned `get_account_activities(activity_types=FILL)` row 기준 earlier same-session fills `MSFT` buy `1주`(`395.87 USD`), `AVGO` sell `1주`(`391.92 USD`)가 모두 유지됐다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `get_clock/get_account_info/get_all_positions/get_orders_open/get_watchlists` 기준 regular market closed, account `ACTIVE`, positions `33`건, open orders `0`건, watchlists `0`건이었다.
- Recent reconciliation scope: scheduler-owned `1811` after-hours core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 expected nonblocking으로 처리했다. 같은 preflight의 passing account/positions/open-orders/recent-activities/watchlist/quote/snapshot/trade rows가 same-session fill continuity까지 포함했고, separate after-hours session budget은 `2/2`로 닫혀 있어 이번 cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-15-1811-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-15-1751-after-hours-autopilot]]
- Open/new: 없음
- Filled: direct `get_orders(status=all, after=2026-06-14T20:00:00Z)` 및 direct `get_account_activities(activity_types=FILL, after=2026-06-14T20:00:00Z)` readback 기준 earlier same-session fills `MSFT` buy `1주`(`395.87 USD`), `AVGO` sell `1주`(`391.92 USD`)가 모두 유지됐다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `get_clock/get_account_info/get_all_positions/get_orders_open/get_watchlists` 기준 regular market closed, account `ACTIVE`, positions `33`건, open orders `0`건, watchlists `0`건이었다.
- Recent reconciliation scope: scheduler-owned `1751` after-hours core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 expected nonblocking으로 처리했다. 같은 preflight의 passing account/positions/open-orders/watchlist/quote/snapshot/trade rows는 유지했지만 same-session fill continuity는 비어 있어 direct `get_orders(status=all/open)` 및 direct `get_account_activities(activity_types=FILL, after=2026-06-14T20:00:00Z)`로만 보강했다. separate after-hours session budget은 `2/2`로 닫혀 있어 이번 cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-15-1751-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-15-1731-after-hours-autopilot]]
- Open/new: 없음
- Filled: scheduler-owned `get_account_activities(activity_types=FILL)` row 기준 earlier same-session fills `AVGO` sell `1주`(`391.92 USD`), `MSFT` buy `1주`(`395.87 USD`)가 모두 유지됐다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `get_clock/get_account_info/get_all_positions/get_orders_open/get_watchlists` 기준 regular market closed, account `ACTIVE`, positions `33`건, open orders `0`건, watchlists `0`건이었다.
- Recent reconciliation scope: scheduler-owned `1731` after-hours core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 expected nonblocking으로 처리했다. 같은 preflight의 passing account/positions/open-orders/recent-activities/watchlist/quote/snapshot/trade rows를 유지했고, separate after-hours session budget은 `2/2`로 닫혀 있어 이번 cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-15-1731-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-15-1711-after-hours-autopilot]]
- Open/new: 없음
- Filled: scheduler-owned `get_account_activities(activity_types=FILL, after=2026-06-14T20:00:00Z)` row 기준 earlier same-session fills `AVGO` sell `1주`(`391.92 USD`), `MSFT` buy `1주`(`395.87 USD`)가 모두 유지됐다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `get_clock/get_account_info/get_all_positions/get_orders_open/get_watchlists` 기준 regular market closed, account `ACTIVE`, positions `33`건, open orders `0`건, watchlists `0`건이었다.
- Recent reconciliation scope: scheduler-owned `1711` after-hours core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 expected nonblocking으로 처리했다. 이번 cycle은 같은 preflight의 passing account/positions/open-orders/recent-activities/watchlist/quote/snapshot/trade rows를 유지했고, 별도 direct continuity read 없이 same preflight activity/open-order rows로 same-session order history를 재확인했다. separate after-hours session budget은 `2/2`로 닫혀 있어 이번 cycle은 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-15-1711-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-15-1631-after-hours-autopilot]]
- Open/new: 없음
- Filled: direct `get_order_by_client_id` 및 direct `get_account_activities(activity_types=FILL, after=2026-06-14T20:00:00Z)` readback 기준 earlier same-session fills `AVGO` sell `1주`(`391.92 USD`), `MSFT` buy `1주`(`395.87 USD`)가 모두 유지됐다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `get_clock/get_account_info/get_all_positions/get_orders_open/get_watchlists` 기준 regular market closed, account `ACTIVE`, positions `33`건, open orders `0`건, watchlists `0`건이었다.
- Recent reconciliation scope: scheduler-owned `1631` after-hours core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 expected nonblocking으로 처리했다. direct `get_orders(status=all, after=2026-06-14T20:00:00Z)/get_orders(status=open)/get_account_activities(activity_types=FILL, after=2026-06-14T20:00:00Z)/get_order_by_client_id` continuity는 same-session order history와 filled `client_order_id` 확인에만 사용했다. separate after-hours session budget은 `2/2`로 닫혀 있어 이번 cycle은 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-15-1631-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-15-1611-after-hours-autopilot]]
- Open/new: 없음
- Filled: direct `get_order_by_client_id` 및 direct `get_account_activities(activity_types=FILL, after=2026-06-14T20:00:00Z)` readback 기준 earlier same-session fills `AVGO` sell `1주`(`391.92 USD`), `MSFT` buy `1주`(`395.87 USD`)가 모두 유지됐다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `get_clock/get_account_info/get_all_positions/get_orders_open/get_watchlists` 기준 regular market closed, account `ACTIVE`, positions `33`건, open orders `0`건, watchlists `0`건이었다.
- Recent reconciliation scope: scheduler-owned `1611` after-hours core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 expected nonblocking으로 처리했다. direct `get_orders(status=all, after=2026-06-14T20:00:00Z)/get_orders(status=open)/get_account_activities(activity_types=FILL, after=2026-06-14T20:00:00Z)/get_order_by_client_id` continuity는 same-session order history와 filled `client_order_id` 확인에만 사용했다. separate after-hours session budget은 `2/2`로 닫혀 있어 이번 cycle은 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-15-1611-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-15-1551-after-hours-autopilot]]
- Open/new: 없음
- Filled: scheduler-owned `get_account_activities(activity_types=FILL, after=2026-06-14T20:00:00Z)` row 기준 earlier same-session fills `AVGO` sell `1주`(`391.92 USD`), `MSFT` buy `1주`(`395.87 USD`)가 모두 유지됐다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `get_clock/get_account_info/get_all_positions/get_orders_open/get_watchlists` 기준 regular market closed, account `ACTIVE`, positions `33`건, open orders `0`건, watchlists `0`건이었다.
- Recent reconciliation scope: scheduler-owned `1551` after-hours core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 expected nonblocking으로 처리했다. 이번 cycle은 같은 preflight의 passing account/positions/open-orders/recent-activities/watchlist/asset/quote/snapshot rows를 유지했고, 별도 direct continuity read 없이 same preflight activity/open-order rows로 same-session order history를 재확인했다. separate after-hours session budget은 `2/2`로 닫혀 있어 이번 cycle은 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-15-1551-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-15-1531-after-hours-autopilot]]
- Open/new: 없음
- Filled: direct `get_order_by_client_id` 및 direct `get_account_activities(activity_types=FILL, after=2026-06-14T20:00:00Z)` readback 기준 earlier same-session fills `AVGO` sell `1주`(`391.92 USD`), `MSFT` buy `1주`(`395.87 USD`)가 모두 유지됐다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_watchlists` 기준 regular market closed, account `ACTIVE`, positions `33`건, open orders `0`건, watchlists `0`건이었다.
- Recent reconciliation scope: scheduler-owned `1531` after-hours core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 expected nonblocking으로 처리했다. direct `get_orders(status=all, after=2026-06-14T20:00:00Z)/get_orders(status=open)/get_account_activities(activity_types=FILL, after=2026-06-14T20:00:00Z)/get_order_by_client_id` continuity는 same-session order history와 filled `client_order_id` 확인에만 사용했다. separate after-hours session budget은 `2/2`로 닫혀 있어 이번 cycle은 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-15-1531-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-15-1511-after-hours-autopilot]]
- Open/new: 없음
- Filled: scheduler-owned `get_account_activities(activity_types=FILL, after=2026-06-14T20:00:00Z)` row 기준 earlier same-session fills `AVGO` sell `1주`(`391.92 USD`), `MSFT` buy `1주`(`395.87 USD`)가 모두 유지됐다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_watchlists` 기준 regular market closed, account `ACTIVE`, positions `33`건, open orders `0`건, watchlists `0`건이었다.
- Recent reconciliation scope: scheduler-owned `1511` after-hours core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 expected nonblocking으로 처리했다. 이번 cycle은 같은 preflight의 passing account/positions/open-orders/recent-activities/watchlist/asset/quote/snapshot rows를 유지했고, 추가 Alpaca runtime read는 수행하지 않았다. separate after-hours session budget은 `2/2`로 닫혀 있어 이번 cycle은 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-15-1511-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-15-1411-after-hours-autopilot]]
- Open/new: 없음
- Filled: direct `get_order_by_client_id` readback 기준 earlier same-session fills `AVGO` sell `1주`(`391.92 USD`), `MSFT` buy `1주`(`395.87 USD`)가 모두 유지됐다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_watchlists` 기준 regular market closed, account `ACTIVE`, positions `33`건, open orders `0`건, watchlists `0`건이었다.
- Recent reconciliation scope: scheduler-owned `1411` after-hours core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 expected nonblocking으로 처리했다. 이번 cycle은 같은 preflight의 passing account/positions/open-orders/recent-activities/watchlist/asset/quote/snapshot rows를 유지했고, direct `get_orders(status=all, after=2026-06-14T20:00:00Z)/get_orders(status=open)/get_account_activities(activity_types=FILL, after=2026-06-14T20:00:00Z)/get_watchlists/get_order_by_client_id` continuity는 same-session order history와 fill/client_order_id reconciliation에만 사용했다. separate after-hours session budget은 `2/2`로 닫혀 있어 이번 cycle은 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-15-1411-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-15-1351-after-hours-autopilot]]
- Open/new: 없음
- Filled: direct `get_order_by_client_id` readback 기준 earlier same-session fills `AVGO` sell `1주`(`391.92 USD`), `MSFT` buy `1주`(`395.87 USD`)가 모두 유지됐다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_watchlists` 기준 regular market closed, account `ACTIVE`, positions `33`건, open orders `0`건, watchlists `0`건이었다.
- Recent reconciliation scope: scheduler-owned `1351` after-hours core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 expected nonblocking으로 처리했다. 이번 cycle은 같은 preflight의 passing account/positions/open-orders/recent-activities/asset/quote/snapshot rows를 유지했고, direct `get_orders(status=all, after=2026-06-14T20:00:00Z)/get_orders(status=open)/get_watchlists/get_order_by_client_id` continuity는 same-session order history와 `client_order_id` reconciliation에만 사용했다. separate after-hours session budget은 `2/2`로 닫혀 있어 이번 cycle은 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-15-1351-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-15-1331-after-hours-autopilot]]
- Open/new: 없음
- Filled: direct `get_order_by_client_id` readback 기준 earlier same-session fills `AVGO` sell `1주`(`391.92 USD`), `MSFT` buy `1주`(`395.87 USD`)가 모두 유지됐다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_watchlists` 기준 regular market closed, account `ACTIVE`, positions `33`건, open orders `0`건, watchlists `0`건이었다.
- Recent reconciliation scope: scheduler-owned `1331` after-hours core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 expected nonblocking으로 처리했다. 이번 cycle은 같은 preflight의 passing account/positions/open-orders/recent-activities/asset/quote/snapshot rows를 유지했고, direct `get_orders(status=all, after=2026-06-14T20:00:00Z)/get_account_activities(activity_types=FILL, after=2026-06-14T20:00:00Z)/get_order_by_client_id` continuity는 same-session order history와 `client_order_id` reconciliation에만 사용했다. separate after-hours session budget은 `2/2`로 닫혀 있어 이번 cycle은 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-15-1331-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-15-1311-after-hours-autopilot]]
- Open/new: 없음
- Filled: direct `get_order_by_client_id` readback 기준 earlier same-session fills `AVGO` sell `1주`(`391.92 USD`), `MSFT` buy `1주`(`395.87 USD`)가 모두 유지됐다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_watchlists` 기준 regular market closed, account `ACTIVE`, positions `33`건, open orders `0`건, watchlists `0`건이었다.
- Recent reconciliation scope: scheduler-owned `1311` after-hours core/research preflight를 source-of-record로 사용했고 Alpaca core `first_blocking_gate=market_closed`는 expected nonblocking으로 처리했다. 이번 cycle은 같은 preflight의 passing account/positions/open-orders/recent-activities/asset/quote/snapshot rows를 유지했고, direct `get_orders(status=all, after=2026-06-14T20:00:00Z)/get_account_activities(activity_types=FILL, after=2026-06-14T20:00:00Z)/get_order_by_client_id` continuity는 same-session order history와 `client_order_id` reconciliation에만 사용했다. separate after-hours session budget은 `2/2`로 닫혀 있어 이번 cycle은 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-15-1311-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-15-1251-after-hours-autopilot]]
- Open/new: 없음
- Filled: direct `get_order_by_client_id` readback 기준 earlier same-session fills `AVGO` sell `1주`(`391.92 USD`), `MSFT` buy `1주`(`395.87 USD`)가 모두 유지됐다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: direct `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_watchlists` 기준 regular market closed, account `ACTIVE`, positions `33`건, open orders `0`건, watchlists `0`건이었다.
- Recent reconciliation scope: scheduler-owned `1251` after-hours core/research preflight를 source-of-record로 사용했지만 passing rows는 비어 있었고, direct `get_orders(status=all, after=2026-06-14T20:00:00Z)/get_account_activities(activity_types=FILL, after=2026-06-14T20:00:00Z)/get_asset/get_stock_latest_quote(feed=overnight)/get_stock_snapshot/get_order_by_client_id` continuity가 missing after-hours-required rows를 보강했다. separate after-hours session budget은 `2/2`로 닫혀 있어 이번 cycle은 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-15-1251-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-15-1231-after-hours-autopilot]]
- Open/new: 없음
- Filled: direct `get_order_by_client_id` readback 기준 earlier same-session fills `AVGO` sell `1주`(`391.92 USD`), `MSFT` buy `1주`(`395.87 USD`)가 모두 유지됐다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: direct `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_watchlists` 기준 regular market closed, account `ACTIVE`, positions `33`건, open orders `0`건, watchlists `0`건이었다.
- Recent reconciliation scope: scheduler-owned `1231` after-hours core/research preflight를 source-of-record로 사용했지만 passing rows는 비어 있었고, direct `get_orders(status=all, after=2026-06-14T20:00:00Z)/get_account_activities(activity_types=FILL, after=2026-06-14T20:00:00Z)/get_asset/get_stock_latest_quote/get_stock_snapshot/get_order_by_client_id` continuity가 missing after-hours-required rows를 보강했다. separate after-hours session budget은 `2/2`로 닫혀 있어 이번 cycle은 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-15-1231-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-15-1211-after-hours-autopilot]]
- Open/new: 없음
- Filled: direct `get_order_by_client_id` readback 기준 earlier same-session fills `AVGO` sell `1주`(`391.92 USD`), `MSFT` buy `1주`(`395.87 USD`)가 모두 유지됐다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: direct `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_watchlists` 기준 regular market closed, account `ACTIVE`, positions `33`건, open orders `0`건, watchlists `0`건이었다.
- Recent reconciliation scope: scheduler-owned `1211` after-hours core/research preflight를 source-of-record로 사용했고 direct `get_order_by_client_id` readback은 same-session after-hours client order ids `ah-20260615-0951-sell-avgo-01`, `ah-20260615-1011-buy-msft-01`가 모두 filled임을 재확인하는 데만 사용했다. separate after-hours session budget은 `2/2`로 닫혀 있어 이번 cycle은 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-15-1211-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-15-1151-after-hours-autopilot]]
- Open/new: 없음
- Filled: direct `get_order_by_client_id` readback 기준 earlier same-session fills `AVGO` sell `1주`(`391.92 USD`), `MSFT` buy `1주`(`395.87 USD`)가 모두 유지됐다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: direct `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_watchlists` 기준 regular market closed, account `ACTIVE`, positions `33`건, open orders `0`건, watchlists `0`건이었다.
- Recent reconciliation scope: scheduler-owned `1151` after-hours core/research preflight를 source-of-record로 사용했고 direct `get_order_by_client_id` readback은 same-session after-hours client order ids `ah-20260615-0951-sell-avgo-01`, `ah-20260615-1011-buy-msft-01`가 모두 filled임을 재확인하는 데만 사용했다. separate after-hours session budget은 `2/2`로 닫혀 있어 이번 cycle은 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-15-1151-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-15-1131-after-hours-autopilot]]
- Open/new: 없음
- Filled: direct `get_order_by_client_id` readback 기준 earlier same-session fills `AVGO` sell `1주`(`391.92 USD`), `MSFT` buy `1주`(`395.87 USD`)가 모두 유지됐다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: direct `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_watchlists` 기준 regular market closed, account `ACTIVE`, positions `33`건, open orders `0`건, watchlists `0`건이었다.
- Recent reconciliation scope: scheduler-owned `1131` after-hours core/research preflight를 source-of-record로 사용했고 direct `get_order_by_client_id` readback은 same-session after-hours client order ids `ah-20260615-0951-sell-avgo-01`, `ah-20260615-1011-buy-msft-01`가 모두 filled임을 재확인하는 데만 사용했다. separate after-hours session budget은 `2/2`로 닫혀 있어 이번 cycle은 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-15-1131-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-15-1111-after-hours-autopilot]]
- Open/new: 없음
- Filled: direct `get_order_by_client_id` readback 기준 earlier same-session fills `AVGO` sell `1주`(`391.92 USD`), `MSFT` buy `1주`(`395.87 USD`)가 모두 유지됐다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `1111` `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_watchlists` passing rows 기준 regular market closed, account `ACTIVE`, positions `33`건, open orders `0`건, watchlists `0`건이었다.
- Recent reconciliation scope: scheduler-owned `1111` after-hours core/research preflight를 source-of-record로 사용했고 direct `get_order_by_client_id` readback은 same-session after-hours client order ids `ah-20260615-0951-sell-avgo-01`, `ah-20260615-1011-buy-msft-01`가 모두 filled임을 재확인하는 데만 사용했다. separate after-hours session budget은 `2/2`로 닫혀 있어 이번 cycle은 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-15-1111-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-15-1051-after-hours-autopilot]]
- Open/new: 없음
- Filled: direct `get_order_by_client_id` readback 기준 earlier same-session fills `AVGO` sell `1주`(`391.92 USD`), `MSFT` buy `1주`(`395.87 USD`)가 모두 유지됐다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `1051` `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_watchlists` passing rows 기준 regular market closed, account `ACTIVE`, positions `33`건, open orders `0`건, watchlists `0`건이었다.
- Recent reconciliation scope: scheduler-owned `1051` after-hours core/research preflight를 source-of-record로 사용했고 direct `get_order_by_client_id` readback은 same-session after-hours client order ids `ah-20260615-0951-sell-avgo-01`, `ah-20260615-1011-buy-msft-01`가 모두 filled임을 재확인하는 데만 사용했다. separate after-hours session budget은 `2/2`로 닫혀 있어 이번 cycle은 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-15-1051-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-15-1031-after-hours-autopilot]]
- Open/new: 없음
- Filled: direct `get_order_by_client_id` readback 기준 earlier same-session fills `AVGO` sell `1주`(`391.92 USD`), `MSFT` buy `1주`(`395.87 USD`)가 모두 유지됐다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `1031` `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_watchlists` passing rows 기준 regular market closed, account `ACTIVE`, positions `33`건, open orders `0`건, watchlists `0`건이었다.
- Recent reconciliation scope: scheduler-owned `1031` after-hours core/research preflight를 source-of-record로 사용했고 direct `get_order_by_client_id` readback은 same-session after-hours client order ids `ah-20260615-0951-sell-avgo-01`, `ah-20260615-1011-buy-msft-01`가 모두 filled임을 재확인하는 데만 사용했다. separate after-hours session budget은 `2/2`로 닫혀 있어 이번 cycle은 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-15-1031-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-15-1011-after-hours-autopilot]]
- Open/new: `MSFT` buy `1주`, `limit_price=395.96 USD`, `client_order_id=ah-20260615-1011-buy-msft-01`, immediate readback `status=new`
- Filled: direct `get_account_activities(activity_types=FILL, after=2026-06-14T20:00:00Z)` 기준 이번 cycle 신규 fill 없음. same-session fill은 `0951` `AVGO` sell `1주`(`391.92 USD`)만 유지됐다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: direct `get_clock`, `get_account_info`, `get_all_positions`, `get_orders(status=open)`, `get_watchlists` 기준 regular market closed, account `ACTIVE`, positions `33`건, open orders `1`건, watchlists `0`건이었다. immediate post-submit에도 `MSFT total qty=2`, `qty_available=2`가 유지돼 아직 fill이 없음을 재확인했다.
- Recent reconciliation scope: scheduler-owned `1011` after-hours core/research preflight를 source-of-record로 사용했고 direct live Alpaca MCP continuity는 same-session after-hours orders `2`, same-session fills `1`, shortlist `QQQ/MSFT/SMH/SPY/AVGO/SO/INTC/MU`의 fresh overnight quote를 재확인했다. strict universe/MCP/risk validator가 모두 PASS했고, `AVGO` sell-first path는 `0951` same-day filled trim 때문에 duplicate-side discipline으로 제외했다. remaining session budget `1/2`를 `MSFT` buy fallback 1주에 사용했고 immediate readback은 `status=new`, `filled_qty=0`였다.
- Orders submitted/replaced/cancelled/closed by this workflow: 1 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-15-1011-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-15-0951-after-hours-autopilot]]
- Open/new: `AVGO` sell `1주`, `limit_price=391.91 USD`, `client_order_id=ah-20260615-0951-sell-avgo-01`, immediate readback `status=new`
- Filled: direct `get_account_activities(activity_types=FILL, after=2026-06-14T20:00:00Z)` 기준 이번 cycle 신규 fill 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: direct `get_clock`, `get_account_info`, `get_all_positions`, `get_orders(status=open)`, `get_watchlists` 기준 regular market closed, account `ACTIVE`, positions `33`건, watchlists `0`건이었다. submit 후 `AVGO` total qty는 `4주`를 유지했고 `qty_available`만 `3주`로 감소해 open sell reservation을 재확인했다.
- Recent reconciliation scope: scheduler-owned `0951` after-hours core/research preflight를 source-of-record로 사용했다. 다만 core preflight는 expected `market_closed` 외 passing row를 비워 두어, direct Alpaca MCP continuity로 missing account/positions/open-orders/asset/quote rows를 한 번만 보강했다. direct overnight latestQuote `AVGO 391.91/392.07`은 spread `0.0408%`, quote age 약 `0.32`분으로 after-hours hard gate를 통과했고, strict universe/MCP/risk validator도 모두 PASS였다. same `client_order_id`에 대한 direct `get_order_by_client_id`와 direct `get_orders(status=all|open, symbols=AVGO)` readback은 `status=new`, `filled_qty=0`를 확인했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 1 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-15-0951-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-15-0931-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음. direct `get_orders(status=all, after=2026-06-14T20:00:00Z)`와 direct `get_account_activities(activity_types=FILL, after=2026-06-14T20:00:00Z)`가 모두 빈 결과여서 same-session after-hours order/fill continuity를 직접 재확인했다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: direct `get_clock`, `get_account_info`, `get_all_positions`, `get_orders(status=open)`, `get_watchlists` 기준 regular market closed, account `ACTIVE`, positions `33`건, open orders `0`건, watchlists `0`건이었다.
- Recent reconciliation scope: scheduler-owned `0931` after-hours core/research preflight를 source-of-record로 사용했고 direct live Alpaca MCP continuity는 same-session after-hours orders `0`, same-session fills `0`, shortlist `QQQ/MSFT/SMH/SPY/AVGO/SO/INTC/MU`의 live IEX readback과 live `overnight` latestQuote readback을 재확인했다. live `overnight` latestQuote는 `2026-06-15T00:33Z`대로 전진했지만 사용자 지시대로 scheduler-owned `0931` quote/spread rows를 submit-boundary source-of-record로 유지했다. separate after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned submit-boundary quote rows 기준 `QQQ`가 약 `3093.50`분 stale, `MSFT/SMH`가 `3108.57/3096.50`분 stale, `SPY/AVGO/SO/INTC/MU`는 약 `3151.11-3151.13`분 stale 또는 spread/notional cap fail이라 submit path에 진입하지 못했다. research preflight에서는 `alpha-vantage`가 `provider_error`(`Alpha Vantage daily API rate limit reached; NEWS_SENTIMENT data unavailable.`) gap을 기록했지만 `sec-edgar/fred/firecrawl/yahoo-finance` pass로 strict MCP gate는 유지됐다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-15-0931-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-15-0911-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음. direct `get_orders(status=all, after=2026-06-14T20:00:00Z)`와 direct `get_account_activities(activity_types=FILL, after=2026-06-14T20:00:00Z)`가 모두 빈 결과여서 same-session after-hours order/fill continuity를 직접 재확인했다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: direct `get_clock`, `get_account_info`, `get_all_positions`, `get_orders(status=open)`, `get_watchlists` 기준 regular market closed, account `ACTIVE`, positions `33`건, open orders `0`건, watchlists `0`건이었다.
- Recent reconciliation scope: scheduler-owned `0911` after-hours core/research preflight를 source-of-record로 사용했고 direct live Alpaca MCP continuity는 same-session after-hours orders `0`, same-session fills `0`, shortlist `QQQ/MSFT/SMH/SPY/AVGO/SO/INTC/MU`의 live IEX readback을 재확인했다. live `overnight` latestQuote는 `2026-06-15T00:13Z`대로 전진했지만 사용자 지시대로 scheduler-owned `0911` quote/spread rows를 submit-boundary source-of-record로 유지했다. separate after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned submit-boundary quote rows 기준 `QQQ`가 약 `3075.17`분 stale, `MSFT/SMH`가 `3090.24/3078.16`분 stale, `SPY/AVGO/SO/INTC/MU`는 약 `3132.77-3132.79`분 stale 또는 spread/notional cap fail이라 submit path에 진입하지 못했다. research preflight에서는 `alpha-vantage`가 `provider_error`(`Alpha Vantage daily API rate limit reached; NEWS_SENTIMENT data unavailable.`) gap을 기록했지만 `sec-edgar/fred/firecrawl/yahoo-finance` pass로 strict MCP gate는 유지됐다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-15-0911-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-15-0851-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음. direct `get_orders(status=all, after=2026-06-14T20:00:00Z)`와 direct `get_account_activities(activity_types=FILL, after=2026-06-14T20:00:00Z)`가 모두 빈 결과여서 same-session after-hours order/fill continuity를 직접 재확인했다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: direct `get_clock`, `get_account_info`, `get_all_positions`, `get_orders(status=open)`, `get_watchlists` 기준 regular market closed, account `ACTIVE`, positions `33`건, open orders `0`건, watchlists `0`건이었다.
- Recent reconciliation scope: scheduler-owned `0851` after-hours core/research preflight를 source-of-record로 사용했고 direct live Alpaca MCP continuity는 same-session after-hours orders `0`, same-session fills `0`, shortlist `QQQ/MSFT/SMH/SPY/AVGO/SO/INTC/MU`의 live IEX/overnight quote parity를 재확인했다. separate after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned submit-boundary quote rows 기준 `QQQ`가 약 `3055.35`분 stale, `MSFT/SMH`가 `3070.42/3058.35`분 stale, `SPY/AVGO/SO/INTC/MU`는 약 `3112.96-3112.98`분 stale 또는 spread/notional cap fail이라 submit path에 진입하지 못했다. research preflight에서는 `alpha-vantage`가 `provider_error`(`Alpha Vantage daily API rate limit reached; NEWS_SENTIMENT data unavailable.`) gap을 기록했지만 `sec-edgar/fred/firecrawl/yahoo-finance` pass로 strict MCP gate는 유지됐다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-15-0851-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-15-0831-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음. direct `get_orders(status=all, after=2026-06-14T20:00:00Z)`와 direct `get_account_activities(activity_types=FILL, after=2026-06-14T20:00:00Z)`가 모두 빈 결과여서 same-session after-hours order/fill continuity를 직접 재확인했다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: direct `get_clock`, `get_account_info`, `get_all_positions`, `get_orders(status=open)`, `get_watchlists` 기준 regular market closed, account `ACTIVE`, positions `33`건, open orders `0`건, watchlists `0`건이었다.
- Recent reconciliation scope: scheduler-owned `0831` after-hours core/research preflight를 source-of-record로 사용했고 direct live Alpaca MCP continuity는 same-session after-hours orders `0`, same-session fills `0`, shortlist `QQQ/MSFT/SMH/SPY/AVGO/SO/INTC/MU`의 live IEX/overnight quote parity를 재확인했다. separate after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned submit-boundary quote rows 기준 `QQQ`가 약 `3035.61`분 stale, `MSFT/SMH`가 `3050.68/3038.6`분 stale, `SPY/AVGO/SO/INTC/MU`는 약 `3093.21-3093.23`분 stale 또는 spread/notional cap fail이라 submit path에 진입하지 못했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-15-0831-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-15-0811-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음. direct `get_orders(status=all, after=2026-06-14T20:00:00Z)`와 direct `get_account_activities(activity_types=FILL, after=2026-06-14T20:00:00Z)`가 모두 빈 결과여서 same-session after-hours order/fill continuity를 직접 재확인했다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: direct `get_clock`, `get_account_info`, `get_all_positions`, `get_orders(status=open)`, `get_watchlists` 기준 regular market closed, account `ACTIVE`, positions `33`건, open orders `0`건, watchlists `0`건이었다.
- Recent reconciliation scope: scheduler-owned `0811` after-hours core/research preflight를 source-of-record로 사용했고 direct live Alpaca MCP continuity는 same-session after-hours orders `0`, same-session fills `0`, shortlist `QQQ/MSFT/SMH/SPY/AVGO/SO/INTC/MU`의 live IEX/overnight quote parity를 재확인했다. separate after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned submit-boundary quote rows 기준 `QQQ`가 약 `3015.51`분 stale, `MSFT/SMH`가 `3030.58/3018.5`분 stale, `SPY/AVGO/SO/INTC/MU`는 약 `3073.11-3073.13`분 stale 또는 spread/notional cap fail이라 submit path에 진입하지 못했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-15-0811-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-15-0751-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음. direct `get_orders(status=all, after=2026-06-14T20:00:00Z)`와 direct `get_account_activities(activity_types=FILL, after=2026-06-14T20:00:00Z)`가 모두 빈 결과여서 same-session after-hours order/fill continuity를 직접 재확인했다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: direct `get_clock`, `get_account_info`, `get_all_positions`, `get_orders(status=open)`, `get_watchlists` 기준 regular market closed, account `ACTIVE`, positions `33`건, open orders `0`건, watchlists `0`건이었다.
- Recent reconciliation scope: scheduler-owned `0751` after-hours core/research preflight를 source-of-record로 사용했고 direct live Alpaca MCP continuity는 same-session after-hours orders `0`, same-session fills `0`, shortlist `QQQ/MSFT/SMH/SPY/AVGO/SO/INTC/MU`의 live IEX/overnight quote parity를 재확인했다. separate after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned submit-boundary quote rows 기준 `QQQ`가 약 `2995.26`분 stale, `MSFT/SMH`가 `3010.33/2998.26`분 stale, `SPY/AVGO/SO/INTC/MU`는 약 `3052.86-3052.89`분 stale 또는 spread/notional cap fail이라 submit path에 진입하지 못했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-15-0751-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-15-0731-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음. direct `get_orders(status=all, after=2026-06-14T20:00:00Z)`와 direct `get_account_activities(activity_types=FILL, after=2026-06-14T20:00:00Z)`가 모두 빈 결과여서 same-session after-hours order/fill continuity를 직접 재확인했다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: direct `get_clock`, `get_account_info`, `get_all_positions`, `get_orders(status=open)`, `get_watchlists` 기준 regular market closed, account `ACTIVE`, positions `33`건, open orders `0`건, watchlists `0`건이었다.
- Recent reconciliation scope: scheduler-owned `0731` after-hours core/research preflight를 source-of-record로 사용했고 direct live Alpaca MCP continuity는 same-session after-hours orders `0`, same-session fills `0`, shortlist `QQQ/MSFT/SMH/SPY/AVGO/SO/INTC/MU`의 live IEX/overnight quote parity를 재확인했다. separate after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned submit-boundary quote rows 기준 `QQQ`가 약 `2975.71`분 stale, `MSFT/SMH`가 `2990.78/2978.71`분 stale, `SPY/AVGO/SO/INTC/MU`는 약 `3033.32-3033.34`분 stale 또는 spread/notional cap fail이라 submit path에 진입하지 못했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-15-0731-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-15-0711-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음. direct `get_orders(status=all, after=2026-06-14T20:00:00Z)`와 direct `get_account_activities(activity_types=FILL, after=2026-06-14T20:00:00Z)`가 모두 빈 결과여서 same-session after-hours order/fill continuity를 직접 재확인했다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: direct `get_clock`, `get_account_info`, `get_all_positions`, `get_orders(status=open)`, `get_watchlists` 기준 regular market closed, account `ACTIVE`, positions `33`건, open orders `0`건, watchlists `0`건이었다.
- Recent reconciliation scope: scheduler-owned `0711` after-hours core/research preflight를 source-of-record로 사용했고 direct live Alpaca MCP continuity는 same-session after-hours orders `0`, same-session fills `0`, shortlist `QQQ/MSFT/SMH/SPY/AVGO/SO/INTC/MU`의 live IEX/overnight quote parity를 재확인했다. separate after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned submit-boundary quote rows 기준 `QQQ`가 약 `2954.75`분 stale, `MSFT/SMH`가 `2969.82/2957.74`분 stale, `SPY/AVGO/SO/INTC/MU`는 약 `3012.35-3012.37`분 stale 또는 spread/notional cap fail이라 submit path에 진입하지 못했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-15-0711-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-15-0651-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음. direct `get_orders(status=all, after=2026-06-14T20:00:00Z)`와 direct `get_account_activities(activity_types=FILL, after=2026-06-14T20:00:00Z)`가 모두 빈 결과여서 same-session after-hours order/fill continuity를 직접 재확인했다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: direct `get_clock`, `get_account_info`, `get_all_positions`, `get_orders(status=open)`, `get_watchlists` 기준 regular market closed, account `ACTIVE`, positions `33`건, open orders `0`건, watchlists `0`건이었다.
- Recent reconciliation scope: scheduler-owned `0651` after-hours core/research preflight를 source-of-record로 사용했고 direct live Alpaca MCP continuity는 same-session after-hours orders `0`, same-session fills `0`, shortlist `QQQ/MSFT/SMH/SPY/AVGO/SO/INTC/MU`의 live IEX/overnight quote parity를 재확인했다. separate after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned submit-boundary quote rows 기준 `QQQ`가 약 `2935.70`분 stale, `MSFT/SMH`가 `2950.77/2938.69`분 stale, `SPY/AVGO/SO/INTC/MU`는 약 `2993.32-2993.30`분 stale 또는 spread/notional cap fail이라 submit path에 진입하지 못했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-15-0651-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-15-0631-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음. direct `get_orders(status=all, after=2026-06-14T20:00:00Z)`와 direct `get_account_activities(activity_types=FILL, after=2026-06-14T20:00:00Z)`가 모두 빈 결과여서 same-session after-hours order/fill continuity를 직접 재확인했다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: direct `get_clock`, `get_account_info`, `get_all_positions`, `get_orders(status=open)`, `get_watchlists` 기준 regular market closed, account `ACTIVE`, positions `33`건, open orders `0`건, watchlists `0`건이었다.
- Recent reconciliation scope: scheduler-owned `0631` after-hours core/research preflight를 source-of-record로 사용했고 direct live Alpaca MCP continuity는 same-session after-hours orders `0`, same-session fills `0`, shortlist `QQQ/MSFT/SMH/SPY/AVGO/SO/INTC/MU`의 live IEX/overnight quote parity를 재확인했다. separate after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned submit-boundary quote rows 기준 `QQQ`가 약 `2914.98`분 stale, `MSFT/SMH`가 `2930.05/2917.97`분 stale, `SPY/AVGO/SO/INTC/MU`는 약 `2972.60-2972.58`분 stale 또는 spread/notional cap fail이라 submit path에 진입하지 못했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-15-0631-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-15-0611-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음. direct `get_orders(status=all, after=2026-06-14T20:00:00Z)`와 direct `get_account_activities(activity_types=FILL, after=2026-06-14T20:00:00Z)`가 모두 빈 결과여서 same-session after-hours order/fill continuity를 직접 재확인했다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: direct `get_clock`, `get_account_info`, `get_all_positions`, `get_orders(status=open)`, `get_watchlists` 기준 regular market closed, account `ACTIVE`, positions `33`건, open orders `0`건, watchlists `0`건이었다.
- Recent reconciliation scope: scheduler-owned `0611` after-hours core/research preflight를 source-of-record로 사용했고 direct live Alpaca MCP continuity는 same-session after-hours orders `0`, same-session fills `0`, shortlist `QQQ/MSFT/SMH/SPY/AVGO/SO/INTC/MU`의 live IEX/overnight quote parity를 재확인했다. separate after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned submit-boundary quote rows 기준 `QQQ`가 약 `2895.82`분 stale, `MSFT/SMH`가 `2910.89/2898.81`분 stale, `SPY/AVGO/SO/INTC/MU`는 약 `2953.44-2953.42`분 stale 또는 spread/notional cap fail이라 submit path에 진입하지 못했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-15-0611-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-14-2151-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음. direct `get_orders(status=all, after=2026-06-13T20:00:00Z)`와 direct `get_account_activities(activity_types=FILL, after=2026-06-13T20:00:00Z)`가 모두 빈 결과여서 same-session after-hours order/fill continuity를 직접 재확인했다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: direct `get_clock`, `get_account_info`, `get_all_positions`, `get_orders(status=open)`, `get_watchlists` 기준 regular market closed, account `ACTIVE`, positions `33`건, open orders `0`건, watchlists `0`건이었다.
- Recent reconciliation scope: scheduler-owned `2151` after-hours core/research preflight를 source-of-record로 사용했고 direct live Alpaca MCP continuity는 same-session after-hours orders `0`, same-session fills `0`, shortlist `QQQ/MSFT/SMH/SPY/AVGO/SO/INTC/MU`의 live IEX/overnight quote parity를 재확인했다. separate after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned submit-boundary quote rows 기준 `QQQ`가 약 `2395.11`분 stale, `MSFT/SMH`가 `2410.18/2398.10`분 stale, `SPY/AVGO/SO/INTC/MU`는 약 `2452.73-2452.71`분 stale 또는 spread/notional cap fail이라 submit path에 진입하지 못했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-14-2151-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-14-2131-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음. direct `get_orders(status=all, after=2026-06-13T20:00:00Z)`와 direct `get_account_activities(activity_types=FILL, after=2026-06-13T20:00:00Z)`가 모두 빈 결과여서 same-session after-hours order/fill continuity를 직접 재확인했다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: direct `get_clock`, `get_account_info`, `get_all_positions`, `get_orders(status=open)`, `get_watchlists` 기준 regular market closed, account `ACTIVE`, positions `33`건, open orders `0`건, watchlists `0`건이었다.
- Recent reconciliation scope: scheduler-owned `2131` after-hours core/research preflight를 source-of-record로 사용했고 direct live Alpaca MCP continuity는 same-session after-hours orders `0`, same-session fills `0`, shortlist `QQQ/MSFT/SMH/SPY/AVGO/SO/INTC/MU`의 live IEX/overnight quote parity를 재확인했다. separate after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned submit-boundary quote rows 기준 `QQQ`가 약 `2375.59`분 stale, `MSFT/SMH`가 `2390.66/2378.59`분 stale, `SPY/AVGO/SO/INTC/MU`는 약 `2433.22-2433.20`분 stale 또는 spread/notional cap fail이라 submit path에 진입하지 못했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-14-2131-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-14-2111-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음. direct `get_orders(status=all, after=2026-06-13T20:00:00Z)`와 direct `get_account_activities(activity_types=FILL, after=2026-06-13T20:00:00Z)`가 모두 빈 결과여서 same-session after-hours order/fill continuity를 직접 재확인했다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: direct `get_clock`, `get_account_info`, `get_all_positions`, `get_orders(status=open)`, `get_watchlists` 기준 regular market closed, account `ACTIVE`, positions `33`건, open orders `0`건, watchlists `0`건이었다.
- Recent reconciliation scope: scheduler-owned `2111` after-hours core/research preflight를 source-of-record로 사용했고 direct live Alpaca MCP continuity는 same-session after-hours orders `0`, same-session fills `0`, shortlist `QQQ/MSFT/SMH/SPY/AVGO/SO/INTC/MU`의 live IEX/overnight quote parity를 재확인했다. separate after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned submit-boundary quote rows 기준 `QQQ`가 약 `2355.02`분 stale, `MSFT/SMH`가 `2370.09/2358.02`분 stale, `SPY/AVGO/SO/INTC/MU`는 약 `2412.65-2412.63`분 stale 또는 spread/notional cap fail이라 submit path에 진입하지 못했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-14-2111-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-14-2051-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음. scheduler-owned `2051` preflight는 same-session after-hours submitted orders `0`를 유지했고, direct live `get_account_activities(activity_types=FILL, after=2026-06-13T20:00:00Z)`도 빈 결과여서 same-session fill `0`을 재확인했다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `2051` `get_clock/get_account_info/get_orders_open` rows 기준 regular market closed, account `ACTIVE`, open orders `0`건이었고 direct live `get_all_positions/get_watchlists`는 positions `33`건, watchlists `0`건을 재확인했다.
- Recent reconciliation scope: scheduler-owned `2051` after-hours core/research preflight를 source-of-record로 사용했고 direct live Alpaca MCP continuity는 same-session after-hours fills `0`, shortlist `QQQ/MSFT/SMH/SPY/AVGO/SO/INTC/MU`의 live IEX/overnight quote parity를 재확인했다. separate after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned submit-boundary quote rows 기준 `QQQ`가 약 `2333.53`분 stale, `MSFT/SMH`가 `2348.60/2336.53`분 stale, `SPY/AVGO/SO/INTC/MU`는 약 `2391.16-2391.14`분 stale 또는 spread/notional cap fail이라 submit path에 진입하지 못했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-14-2051-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-14-2031-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음. live `get_orders(status=all, after=2026-06-13T20:00:00Z)`와 live `get_account_activities(activity_types=FILL, after=2026-06-13T20:00:00Z)`가 모두 빈 결과여서 same-session after-hours order/fill continuity를 직접 재확인했다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: live `get_clock`, `get_account_info`, `get_all_positions`, `get_orders(status=open)`, `get_watchlists` 기준 regular market closed, account `ACTIVE`, positions `33`건, open orders `0`건, watchlists `0`건이었다.
- Recent reconciliation scope: scheduler-owned `2031` after-hours core/research preflight를 source-of-record로 사용했고 live Alpaca MCP continuity check는 same-session after-hours orders `0`, same-session fills `0`, shortlist `QQQ/MSFT/SMH/SPY/AVGO/SO/INTC/MU`의 live IEX/overnight quote parity를 재확인했다. separate after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned submit-boundary quote rows 기준 `QQQ`가 약 `2315.22`분 stale, `MSFT/SMH`가 `2330.29/2318.21`분 stale, `SPY/AVGO/SO/INTC/MU`는 약 `2372.84-2372.82`분 stale 또는 spread/notional cap fail이라 submit path에 진입하지 못했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-14-2031-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-14-2011-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음. live `get_orders(status=all, after=2026-06-13T20:00:00Z)`는 빈 결과였고, 이번 turn에 live `get_account_activities` 도구가 노출되지 않아 same-session after-hours fill continuity는 scheduler-owned `2011` recent-activity row를 source-of-record로 유지했다. 해당 row를 same-session boundary로 재해석해도 신규 fill은 `0`건이었다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: live `get_clock`, `get_account_info`, `get_all_positions`, `get_orders(status=open)`, `get_watchlists` 기준 regular market closed, account `ACTIVE`, positions `33`건, open orders `0`건, watchlists `0`건이었다.
- Recent reconciliation scope: scheduler-owned `2011` after-hours core/research preflight를 source-of-record로 사용했고 live Alpaca MCP continuity check는 same-session after-hours orders `0`, shortlist `QQQ/MSFT/SMH/SPY/AVGO/SO/INTC/MU`의 live IEX/overnight quote parity를 재확인했다. separate after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned submit-boundary quote rows 기준 `QQQ`가 약 `2295.93`분 stale, `MSFT/SMH`가 `2311.00/2298.92`분 stale, `SPY/AVGO/SO/INTC/MU`는 약 `2353.55-2353.53`분 stale 또는 spread/notional cap fail이라 submit path에 진입하지 못했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-14-2011-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-14-1951-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음. live `get_orders(status=all, after=2026-06-13T20:00:00Z)`와 live `get_account_activities(activity_types=FILL, after=2026-06-13T20:00:00Z)`가 모두 빈 결과였고 same-session after-hours order/fill continuity를 직접 재확인했다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: live `get_clock`, `get_account_info`, `get_all_positions`, `get_orders(status=open)`, `get_watchlists` 기준 regular market closed, account `ACTIVE`, positions `33`건, open orders `0`건, watchlists `0`건이었다.
- Recent reconciliation scope: scheduler-owned `1951` after-hours core/research preflight를 source-of-record로 사용했고 live Alpaca MCP continuity check는 same-session after-hours orders `0`, same-session fills `0`, shortlist `QQQ/MSFT/SMH/SPY/AVGO/SO/INTC/MU`의 live IEX quote parity, 그리고 `feed=overnight`의 더 오래된 readback을 재확인했다. separate after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned submit-boundary quote rows 기준 `QQQ`가 약 `2274.88`분 stale, `MSFT/SMH`가 `2289.95/2277.88`분 stale, `SPY/AVGO/SO/INTC/MU`는 약 `2332.51-2332.49`분 stale 또는 spread/notional cap fail이라 submit path에 진입하지 못했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-14-1951-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-14-1931-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음. live `get_orders(status=all, after=2026-06-13T20:00:00Z)`와 live `get_account_activities(activity_types=FILL, after=2026-06-13T20:00:00Z)`가 모두 빈 결과였고 same-session after-hours order/fill continuity를 직접 재확인했다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: live `get_clock`, `get_account_info`, `get_all_positions`, `get_orders(status=open)`, `get_watchlists` 기준 regular market closed, account `ACTIVE`, positions `33`건, open orders `0`건, watchlists `0`건이었다.
- Recent reconciliation scope: scheduler-owned `1931` after-hours core/research preflight를 source-of-record로 사용했고 live Alpaca MCP continuity check는 same-session after-hours orders `0`, same-session fills `0`, shortlist `QQQ/MSFT/SMH/SPY/AVGO/SO/INTC/MU`의 live IEX quote parity, 그리고 `feed=overnight`의 더 오래된 readback을 재확인했다. separate after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned submit-boundary quote rows 기준 `QQQ`가 약 `2255.31`분 stale, `MSFT/SMH`가 `2270.38/2258.30`분 stale, `SPY/AVGO/SO/INTC/MU`는 약 `2312.93-2312.91`분 stale 또는 spread/notional cap fail이라 submit path에 진입하지 못했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-14-1931-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-14-1911-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음. live `get_orders(status=all, after=2026-06-13T20:00:00Z)`와 live `get_account_activities(activity_types=FILL, after=2026-06-13T20:00:00Z)`가 모두 빈 결과였고 same-session after-hours order/fill continuity를 직접 재확인했다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: live `get_clock`, `get_account_info`, `get_all_positions`, `get_orders(status=open)`, `get_watchlists` 기준 regular market closed, account `ACTIVE`, positions `33`건, open orders `0`건, watchlists `0`건이었다.
- Recent reconciliation scope: scheduler-owned `1911` after-hours core/research preflight를 source-of-record로 사용했고 live Alpaca MCP continuity check는 same-session after-hours orders `0`, same-session fills `0`, shortlist `QQQ/MSFT/SMH/SPY/AVGO/SO/INTC/MU`의 live IEX quote parity, 그리고 `feed=overnight`의 더 오래된 readback을 재확인했다. separate after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned submit-boundary quote rows 기준 `QQQ`가 약 `2233.52`분 stale, `MSFT/SMH`가 `2248.59/2236.51`분 stale, `SPY/AVGO/SO/INTC/MU`는 약 `2291.14-2291.12`분 stale 또는 spread/notional cap fail이라 submit path에 진입하지 못했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-14-1911-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-14-1851-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음. live `get_orders(status=all, after=2026-06-13T20:00:00Z)`와 live `get_account_activities(activity_types=FILL, after=2026-06-13T20:00:00Z)`가 모두 빈 결과였고 same-session after-hours order/fill continuity를 직접 재확인했다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: live `get_clock`, `get_account_info`, `get_all_positions`, `get_orders(status=open)`, `get_watchlists` 기준 regular market closed, account `ACTIVE`, positions `33`건, open orders `0`건, watchlists `0`건이었다.
- Recent reconciliation scope: scheduler-owned `1851` after-hours core/research preflight를 source-of-record로 사용했고 live Alpaca MCP continuity check는 same-session after-hours orders `0`, same-session fills `0`, shortlist `QQQ/MSFT/SMH/SPY/AVGO/SO/INTC/MU`의 live IEX quote parity, 그리고 `feed=overnight`의 더 오래된 readback을 재확인했다. separate after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned submit-boundary quote rows 기준 `QQQ`가 약 `2215.89`분 stale, `MSFT/SMH`가 `2230.96/2218.89`분 stale, `SPY/AVGO/SO/INTC/MU`는 약 `2273.52-2273.49`분 stale 또는 spread/notional cap fail이라 submit path에 진입하지 못했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-14-1851-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-14-1831-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음. live `get_orders(status=all, after=2026-06-13T20:00:00Z)`와 live `get_account_activities(activity_types=FILL, after=2026-06-13T20:00:00Z)`가 모두 빈 결과였고 same-session after-hours order/fill continuity를 직접 재확인했다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: live `get_clock`, `get_account_info`, `get_all_positions`, `get_orders(status=open)`, `get_watchlists` 기준 regular market closed, account `ACTIVE`, positions `33`건, open orders `0`건, watchlists `0`건이었다.
- Recent reconciliation scope: scheduler-owned `1831` after-hours core/research preflight를 source-of-record로 사용했고 live Alpaca MCP continuity check는 same-session after-hours orders `0`, same-session fills `0`, shortlist `QQQ/MSFT/SMH/SPY/AVGO/SO/INTC/MU`의 live IEX quote parity, 그리고 `feed=overnight`의 더 오래된 readback을 재확인했다. separate after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned submit-boundary quote rows 기준 `QQQ`가 약 `2193.54`분 stale, `MSFT/SMH`가 `2208.61/2196.53`분 stale, `SPY/AVGO/SO/INTC/MU`는 약 `2251.16-2251.14`분 stale 또는 spread/notional cap fail이라 submit path에 진입하지 못했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-14-1831-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-14-1751-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음. direct Alpaca MCP `get_watchlists`는 `0`건을 반환했고, same-session after-hours order/fill continuity는 scheduler-owned `1751` `orders_submitted=0` 및 passing `get_account_activities(activity_types=FILL, after=2026-06-13T20:00:00Z)` row를 source-of-record로 유지했다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `1751` preflight rows 기준 regular market closed, account `ACTIVE`, positions `33`건, open orders `0`건이었고 direct `get_watchlists`는 `0`건이었다.
- Recent reconciliation scope: scheduler-owned `1751` after-hours core/research preflight를 source-of-record로 사용했고 direct live Alpaca MCP continuity는 `get_watchlists=0`만 재확인했다. separate after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned submit-boundary quote rows 기준 `QQQ`가 약 `2153.79`분 stale, `MSFT/SMH`가 `2168.86/2156.79`분 stale, `SPY/AVGO/SO/INTC/MU`는 약 `2211.42-2211.40`분 stale 또는 spread/notional cap fail이라 submit path에 진입하지 못했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-14-1751-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-14-1731-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음. 이번 turn에는 live Alpaca MCP continuity 도구가 노출되지 않아 same-session after-hours order/fill continuity는 scheduler-owned `1731` `orders_submitted=0` 및 passing `get_account_activities(activity_types=FILL, after=2026-06-13T20:00:00Z)` row를 source-of-record로 유지했다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `1731` preflight rows 기준 regular market closed, account `ACTIVE`, positions `33`건, open orders `0`건, watchlists `0`건이었다.
- Recent reconciliation scope: scheduler-owned `1731` after-hours core/research preflight를 source-of-record로 사용했다. separate after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned submit-boundary quote rows 기준 `QQQ`가 약 `2133.49`분 stale, `MSFT/SMH`가 `2148.56/2136.49`분 stale, `SPY/AVGO/SO/INTC/MU`는 약 `2191.12-2191.10`분 stale 또는 spread/notional cap fail이라 submit path에 진입하지 못했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-14-1731-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-14-1711-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음. live `get_orders(status=all, after=2026-06-13T20:00:00Z)`와 live `get_account_activities(activity_types=FILL, after=2026-06-13T20:00:00Z)`가 모두 빈 결과였다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `1711` `get_clock/get_account_info/get_asset/get_stock_snapshot` rows를 submit-boundary source-of-record로 유지했고, live `get_clock`, `get_account_info`, `get_all_positions`, `get_orders(status=open)`, `get_watchlists`는 regular market closed, account `ACTIVE`, positions `33`건, open orders `0`건, watchlists `0`건을 재확인했다.
- Recent reconciliation scope: scheduler-owned `1711` after-hours core/research preflight를 source-of-record로 사용했고 live Alpaca MCP continuity check는 same-session after-hours orders `0`, same-session fills `0`, shortlist `QQQ/MSFT/SMH/SPY/AVGO/SO/INTC/MU`의 live IEX quote parity, 그리고 `feed=overnight` quote/snapshot stale 상태를 재확인했다. separate after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned submit-boundary quote rows 기준 `QQQ`가 약 `2115.91`분 stale, `MSFT/SMH`가 `2130.98/2118.91`분 stale, `SPY/AVGO/SO/INTC/MU`는 약 `2173.54-2173.52`분 stale 또는 spread/notional cap fail이라 submit path에 진입하지 못했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-14-1711-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-14-1651-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음. live Alpaca MCP continuity는 `get_clock`, `get_account_info`, `get_all_positions`, `get_watchlists`, `get_stock_snapshot(feed=iex|overnight)` 범위에서 regular market closed, account `ACTIVE`, positions `33`, watchlists `0`, live IEX quote parity를 재확인했다. same-session after-hours order/fill continuity는 이번 turn에 live order-history list tool이 없어 scheduler-owned `1651` `orders_submitted=0` 및 `get_account_activities(activity_types=FILL)` row를 source-of-record로 유지했다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: live `get_all_positions` 기준 positions `33`건이었고 scheduler-owned `1651` account/open-order rows도 unchanged였다.
- Recent reconciliation scope: scheduler-owned `1651` after-hours core/research preflight를 source-of-record로 사용했고, live Alpaca MCP continuity check는 shortlist `QQQ/MSFT/SMH/SPY/AVGO/SO/INTC/MU`의 live IEX quote parity와 `feed=overnight` stale readback을 재확인했다. separate after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned submit-boundary quote rows 기준 `QQQ`가 약 `2095.40`분 stale, `MSFT/SMH`가 `2110.47/2098.39`분 stale, `SPY/AVGO/SO/INTC/MU`는 약 `2153.02-2153.00`분 stale 또는 spread/notional cap fail이라 submit path에 진입하지 못했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-14-1651-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-14-1631-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음. live continuity 도구가 노출되지 않아 same-session after-hours order/fill continuity는 scheduler-owned `1631` `orders_submitted=0` 및 `get_account_activities(activity_types=FILL)` timestamp inspection을 source-of-record로 유지했다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `1631` preflight rows 기준 regular market closed, account `ACTIVE`, positions `33`건, open orders `0`건, watchlists `0`건이었다.
- Recent reconciliation scope: scheduler-owned `1631` after-hours core/research preflight를 source-of-record로 사용했다. separate after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned submit-boundary quote rows 기준 `QQQ`가 약 `2073.52`분 stale, `MSFT/SMH`가 `2088.59/2076.52`분 stale, `SPY/AVGO/SO/INTC/MU`는 약 `2131.15-2131.13`분 stale 또는 spread/notional cap fail이라 submit path에 진입하지 못했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-14-1631-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-14-1611-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음. live `get_orders(status=all, after=2026-06-13T20:00:00Z)`와 live `get_account_activities(activity_types=FILL, after=2026-06-13T20:00:00Z)`가 모두 빈 결과였다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `1611` `get_clock/get_asset` rows를 submit-boundary source-of-record로 유지했고, live `get_clock`, `get_account_info`, `get_all_positions`, `get_orders(status=open)`, `get_watchlists`는 regular market closed, account `ACTIVE`, positions `33`건, open orders `0`건, watchlists `0`건을 재확인했다.
- Recent reconciliation scope: scheduler-owned `1611` after-hours core/research preflight를 source-of-record로 사용했고 live Alpaca MCP continuity check는 same-session after-hours orders `0`, same-session fills `0`, shortlist `QQQ/MSFT/SMH/SPY/AVGO/SO/INTC/MU`의 live IEX quote parity, 그리고 `feed=overnight` quote/snapshot readback의 더 오래된 timestamp를 재확인했다. separate after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned submit-boundary quote rows 기준 `QQQ`가 약 `2053.49`분 stale, `MSFT/SMH`가 `2068.56/2056.49`분 stale, `SPY/AVGO/SO/INTC/MU`는 약 `2111.12-2111.10`분 stale 또는 spread/notional cap fail이라 submit path에 진입하지 못했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-14-1611-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-14-1551-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음. 이번 turn에는 live Alpaca MCP 도구가 노출되지 않아 same-session after-hours order/fill continuity는 scheduler-owned `1551` preflight `orders_submitted=0` 및 passing `recent_activities` row를 source-of-record로 유지했다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `1551` preflight rows 기준 regular market closed, account `ACTIVE`, positions `33`건, open orders `0`건, watchlists `0`건이었다.
- Recent reconciliation scope: scheduler-owned `1551` after-hours core/research preflight를 source-of-record로 사용했다. separate after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned submit-boundary quote rows 기준 `QQQ`가 약 `2033.52`분 stale, `MSFT/SMH`가 `2048.59/2036.51`분 stale, `SPY/AVGO/SO/INTC/MU`는 약 `2091.14-2091.12`분 stale 또는 spread/notional cap fail이라 submit path에 진입하지 못했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-14-1551-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-14-1531-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음. 이번 turn에는 live `get_orders`/`get_account_activities` 도구가 노출되지 않아 same-session after-hours order/fill continuity는 scheduler-owned `1531` preflight `orders_submitted=0` 및 passing `recent_activities` row를 source-of-record로 유지했다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `1531` `get_clock/get_account_info/get_orders_open/get_asset` rows를 source-of-record로 유지했고, live `get_clock`, `get_all_positions`, `get_watchlists`는 regular market closed, positions `33`건, watchlists `0`건을 재확인했다.
- Recent reconciliation scope: scheduler-owned `1531` after-hours core/research preflight를 source-of-record로 사용했고 live Alpaca MCP continuity check는 shortlist `QQQ/MSFT/SMH/SPY/AVGO/SO/INTC/MU`의 live IEX quote parity와 `feed=overnight` quote/snapshot stale 상태를 재확인했다. separate after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned submit-boundary quote rows 기준 `QQQ`가 약 `2013.54`분 stale, `MSFT/SMH`가 `2028.61/2016.53`분 stale, `SPY/AVGO/SO/INTC/MU`는 약 `2071.16-2071.14`분 stale 또는 spread/notional cap fail이라 submit path에 진입하지 못했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-14-1531-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-14-1511-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음. live `get_orders(status=all, after=2026-06-13T20:00:00Z)`와 live `get_account_activities(activity_types=FILL, after=2026-06-13T20:00:00Z)`가 모두 빈 결과였고 scheduler-owned `1511` `orders_submitted=0`도 유지됐다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `1511` `get_clock`와 `get_orders_open`를 market-clock/open-order source-of-record로 유지했고, live `get_clock`, `get_account_info`, `get_all_positions`, `get_orders(status=open)`, `get_watchlists`는 regular market closed, account `ACTIVE`, positions `33`건, open orders `0`건, watchlists `0`건을 재확인했다.
- Recent reconciliation scope: scheduler-owned `1511` after-hours core/research preflight를 source-of-record로 사용했고 live Alpaca MCP continuity check는 same-session after-hours orders `0`, same-session fills `0`, shortlist `QQQ/MSFT/SMH/SPY/AVGO/SO/INTC/MU`의 live IEX quote parity, 그리고 `feed=overnight` quote/snapshot stale 상태를 재확인했다. separate after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned submit-boundary quote rows 기준 `QQQ`가 약 `1993.54`분 stale, `MSFT/SMH`가 `2008.61/1996.53`분 stale, `SPY/AVGO/SO/INTC/MU`는 약 `2051.16-2051.14`분 stale 또는 spread/notional cap fail이라 submit path에 진입하지 못했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-14-1511-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-14-1451-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음. live `get_orders(status=all, after=2026-06-13T20:00:00Z)`가 빈 결과였고 scheduler-owned `1451` `orders_submitted=0`도 유지됐다. 이번 세션에 노출된 Alpaca MCP 도구셋에는 `get_account_activities`가 없어 fills는 scheduler-owned `1451` `recent_activities` passing row와 unchanged positions/open orders로 연속성 확인을 유지했다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `1451` `get_clock`와 `get_orders_open`를 market-clock/open-order source-of-record로 유지했고, live `get_clock`, `get_account_info`, `get_all_positions`, `get_orders(status=open)`는 regular market closed, account `ACTIVE`, positions `33`건, open orders `0`건을 재확인했다.
- Recent reconciliation scope: scheduler-owned `1451` after-hours core/research preflight를 source-of-record로 사용했고 live Alpaca MCP continuity check는 same-session after-hours orders `0`, shortlist `QQQ/MSFT/SMH/SPY/AVGO/SO/INTC/MU`의 live IEX quote parity, 그리고 `feed=overnight` quote/snapshot stale 상태를 재확인했다. 이번 세션 도구셋에는 `get_watchlists`가 없어 watchlists continuity는 scheduler-owned `1451` preflight의 passing row `0`건을 그대로 유지했다. separate after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned submit-boundary quote rows 기준 `QQQ`가 약 `1973.52`분 stale, `MSFT/SMH`가 `1988.59/1976.51`분 stale, `SPY/AVGO/SO/INTC/MU`는 약 `2031.14-2031.12`분 stale 또는 spread/notional cap fail이라 submit path에 진입하지 못했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-14-1451-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-14-1431-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음. live `get_orders(status=all, after=2026-06-13T20:00:00Z)`와 `get_account_activities(activity_types=FILL, after=2026-06-13T20:00:00Z)`가 모두 빈 결과였고 scheduler-owned `1431` `orders_submitted=0`도 유지됐다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `1431` `get_clock`와 `get_orders_open`를 market-clock/open-order source-of-record로 유지했고, live `get_clock`, `get_account_info`, `get_all_positions`, `get_orders(status=open)`, `get_watchlists`는 regular market closed, account `ACTIVE`, positions `33`건, open orders `0`건, watchlists `0`건을 재확인했다.
- Recent reconciliation scope: scheduler-owned `1431` after-hours core/research preflight를 source-of-record로 사용했고 live Alpaca MCP continuity check는 same-session after-hours orders `0`, same-session fills `0`, shortlist `QQQ/MSFT/SMH/SPY/AVGO/SO/INTC/MU`의 live IEX quote parity, 그리고 `feed=overnight` quote/snapshot stale 상태를 재확인했다. separate after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned submit-boundary quote rows 기준 `QQQ`가 약 `1953.51`분 stale, `MSFT/SMH`가 `1968.58/1956.51`분 stale, `SPY/AVGO/SO/INTC/MU`는 약 `2011.14-2011.12`분 stale 또는 spread/notional cap fail이라 submit path에 진입하지 못했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-14-1431-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-14-1411-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음. live `get_orders(status=all, after=2026-06-13T20:00:00Z)`와 `get_account_activities(activity_types=FILL, after=2026-06-13T20:00:00Z)`가 모두 빈 결과였고 scheduler-owned `1411` `orders_submitted=0`도 유지됐다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `1411` `get_clock`와 `get_orders_open`를 market-clock/open-order source-of-record로 유지했고, live `get_clock`, `get_account_info`, `get_all_positions`, `get_orders(status=open)`, `get_watchlists`는 regular market closed, account `ACTIVE`, positions `33`건, open orders `0`건, watchlists `0`건을 재확인했다.
- Recent reconciliation scope: scheduler-owned `1411` after-hours core/research preflight를 source-of-record로 사용했고 live Alpaca MCP continuity check는 same-session after-hours orders `0`, same-session fills `0`, shortlist `QQQ/MSFT/SMH/SPY/AVGO/SO/INTC/MU`의 live IEX quote parity, 그리고 `feed=overnight` quote/snapshot stale 상태를 재확인했다. separate after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned submit-boundary quote rows 기준 `QQQ`가 약 `1933.53`분 stale, `MSFT/SMH`가 `1948.60/1936.53`분 stale, `SPY/AVGO/SO/INTC/MU`는 약 `1991.16-1991.13`분 stale 또는 spread/notional cap fail이라 submit path에 진입하지 못했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-14-1411-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-14-1351-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음. live `get_account_activities(activity_types=FILL, after=2026-06-13T20:00:00Z)` 결과가 빈 배열이었고 scheduler-owned `1351` `orders_submitted=0`도 유지됐다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `1351` `get_clock`와 `get_orders_open`를 market-clock/open-order source-of-record로 유지했고, live `get_account_info`, `get_all_positions`, `get_watchlists`는 account `ACTIVE`, positions `33`건, watchlists `0`건을 재확인했다.
- Recent reconciliation scope: scheduler-owned `1351` after-hours core/research preflight를 source-of-record로 사용했고 live Alpaca MCP continuity check는 same-session after-hours fills `0`, shortlist `QQQ/MSFT/SMH/SPY/AVGO/SO/INTC/MU`의 live IEX quote parity, 그리고 `feed=overnight` quote/snapshot stale 상태를 재확인했다. separate after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned submit-boundary quote rows 기준 `QQQ`가 약 `1913.50`분 stale, `MSFT/SMH`가 `1928.57/1916.50`분 stale, `SPY/AVGO/SO/INTC/MU`는 약 `1971.13-1971.11`분 stale 또는 spread/notional cap fail이라 submit path에 진입하지 못했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-14-1351-after-hours-autopilot-post-trade.json`

## 직전 after-hours-autopilot reconciliation

- Run: [[2026-06-14-1331-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음. live `get_orders(status=all, after=2026-06-13T20:00:00Z)`가 빈 결과였고 same-session after-hours submitted orders도 `0`건이었다. 이번 세션에 노출된 Alpaca MCP 도구셋에는 `get_account_activities`가 없어 fills는 empty same-session order history와 unchanged positions `33`건으로 간접 확인했다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `1331` `get_clock`를 market-clock source-of-record로 유지했고, live `get_clock`, `get_account_info`, `get_all_positions`, `get_orders(status=open)`, `get_watchlists`는 regular market closed, account `ACTIVE`, positions `33`건, open orders `0`건, watchlists `0`건을 재확인했다.
- Recent reconciliation scope: scheduler-owned `1331` after-hours core/research preflight를 source-of-record로 사용했고 live Alpaca MCP continuity check는 same-session after-hours submitted orders `0`, shortlist `QQQ/MSFT/SMH/SPY/AVGO/SO/INTC/MU`의 live IEX quote parity, 그리고 `feed=overnight` quote/snapshot stale 상태를 재확인했다. separate after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned submit-boundary quote rows 기준 `QQQ`가 약 `1893.55`분 stale, `MSFT/SMH`가 `1908.62/1896.54`분 stale, `SPY/AVGO/SO/INTC/MU`는 약 `1951.17-1951.15`분 stale 또는 spread/notional cap fail이라 submit path에 진입하지 못했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-14-1331-after-hours-autopilot-post-trade.json`

- Run: [[2026-06-14-1311-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음. live `get_orders(status=all, after=2026-06-13T20:00:00Z)`와 `get_account_activities(activity_types=FILL, after=2026-06-13T20:00:00Z)` 기준 same-session after-hours order/fill history도 `0`건이었다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `1311` `get_clock`를 market-clock source-of-record로 유지했고, live `get_clock`, `get_account_info`, `get_all_positions`, `get_orders(status=open)`, `get_watchlists`는 regular market closed, account `ACTIVE`, positions `33`건, open orders `0`건, watchlists `0`건을 재확인했다.
- Recent reconciliation scope: scheduler-owned `1311` after-hours core/research preflight를 source-of-record로 사용했고 live Alpaca MCP continuity check는 same-session after-hours submitted orders `0`, same-session fills `0`, shortlist `QQQ/MSFT/SMH/SPY/AVGO/SO/INTC/MU`의 live IEX quote parity, 그리고 `feed=overnight` quote/snapshot stale 상태를 재확인했다. separate after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned submit-boundary quote rows 기준 `QQQ`가 약 `1873.51`분 stale, `MSFT/SMH`가 `1888.58/1876.51`분 stale, `SPY/AVGO/SO/INTC/MU`는 약 `1931.14-1931.12`분 stale 또는 spread/notional cap fail이라 submit path에 진입하지 못했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-14-1311-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-14-1251-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음. live `get_orders(status=all, after=2026-06-13T20:00:00Z)`와 scheduler-owned `1251` `orders_submitted=0` 기준 same-session after-hours order/fill history도 `0`건이었다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `1251` `get_clock`를 market-clock source-of-record로 유지했고, live `get_account_info`, `get_all_positions`, `get_orders(status=open)`, `get_watchlists`는 account `ACTIVE`, positions `33`건, open orders `0`건, watchlists `0`건을 재확인했다.
- Recent reconciliation scope: scheduler-owned `1251` after-hours core/research preflight를 source-of-record로 사용했고 live Alpaca MCP continuity check는 same-session after-hours submitted orders `0`, shortlist `QQQ/MSFT/SMH/SPY/AVGO/SO/INTC/MU`의 live IEX quote parity, 그리고 `feed=overnight` quote/snapshot stale 상태를 재확인했다. separate after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned submit-boundary quote rows 기준 `QQQ`가 약 `1853.53`분 stale, `MSFT/SMH`가 `1868.60/1856.53`분 stale, `SPY/AVGO/SO/INTC/MU`는 약 `1911.16-1911.14`분 stale 또는 spread/notional cap fail이라 submit path에 진입하지 못했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-14-1251-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-14-1231-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음. live Alpaca MCP `get_orders(status=all, after=2026-06-13T20:00:00Z)`와 scheduler-owned `1231` `orders_submitted=0` 기준 same-session after-hours order/fill history도 `0`건이었다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: live `get_clock`, `get_account_info`, `get_all_positions`, `get_orders(status=open)`, `get_watchlists`와 scheduler-owned `1231` `get_all_positions`/`get_orders_open`/`get_watchlists`가 모두 regular market closed, account `ACTIVE`, positions `33`건, open orders `0`건, watchlists `0`건으로 일치했다.
- Recent reconciliation scope: scheduler-owned `1231` after-hours core/research preflight를 source-of-record로 사용했고 live Alpaca MCP continuity check는 same-session after-hours submitted orders `0`, shortlist `QQQ/MSFT/SMH/SPY/AVGO/SO/INTC/MU`의 live IEX quote parity, 그리고 `feed=overnight` quote/snapshot stale 상태를 재확인했다. separate after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned submit-boundary quote rows 기준 `QQQ`가 약 `1833.49`분 stale, `MSFT/SMH`가 `1848.56/1836.49`분 stale, `SPY/AVGO/SO/INTC/MU`는 약 `1891.12-1891.10`분 stale 또는 spread/notional cap fail이라 submit path에 진입하지 못했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-14-1231-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-14-1211-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음. scheduler-owned `1211` `orders_submitted=0`와 same-session after-hours fill summary 기준 same-session after-hours order/fill history도 `0`건이었다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `1211` `get_clock`, `get_account_info`, `get_all_positions`, `get_orders(status=open)`, `get_watchlists` 기준 regular market closed, account `ACTIVE`, positions `33`건, open orders `0`건, watchlists `0`건이었다.
- Recent reconciliation scope: scheduler-owned `1211` after-hours core/research preflight를 source-of-record로 사용했다. 이번 turn의 local sandbox `python3` 환경에는 `mcp` 모듈이 없어 별도 live Alpaca MCP continuity spot check는 재실행하지 않았고, 그 대신 scheduler-owned passing account/positions/open-order/activity/watchlist/asset/quote/spread rows를 유지했다. separate after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned submit-boundary quote rows 기준 `QQQ`가 약 `1813.50`분 stale, `MSFT/SMH`가 `1828.57/1816.50`분 stale, `SPY/AVGO/SO/INTC/MU`는 약 `1871.13-1871.10`분 stale 또는 spread/notional cap fail이라 submit path에 진입하지 못했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-14-1211-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-14-1151-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음. direct Alpaca MCP `get_orders(status=all, after=2026-06-12T20:00:00Z)`와 `get_account_activities(activity_types=FILL, after=2026-06-12T20:00:00Z)` 기준 same-session after-hours order/fill history도 `0`건이었다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: direct `get_clock`, `get_account_info`, `get_all_positions`, `get_orders(status=open)`와 scheduler-owned `1151` `get_all_positions`가 모두 regular market closed, account `ACTIVE`, positions `33`건, open orders `0`건으로 일치했다.
- Recent reconciliation scope: scheduler-owned `1151` after-hours core/research preflight를 source-of-record로 사용했고, direct Alpaca MCP continuity check는 same-session after-hours submitted orders `0`, same-session fills `0`, shortlist `QQQ/MSFT/SMH/SPY/AVGO/SO/INTC/MU`의 live IEX quote parity, 그리고 `feed=overnight` quote/snapshot stale 상태를 재확인했다. separate after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned submit-boundary quote rows 기준 `QQQ`가 약 `1793.53`분 stale, `MSFT/SMH`가 `1808.60/1796.52`분 stale, `SPY/AVGO/SO/INTC/MU`는 약 `1851.15-1851.13`분 stale 또는 spread/notional cap fail이라 submit path에 진입하지 못했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-14-1151-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-14-1131-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음. direct Alpaca MCP `get_orders(status=all, after=2026-06-12T20:00:00Z)`와 `get_account_activities(activity_types=FILL, after=2026-06-12T20:00:00Z)` 기준 same-session after-hours order/fill history도 `0`건이었다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: direct `get_clock`, `get_account_info`, `get_all_positions`, `get_orders(status=open)`, `get_watchlists`와 scheduler-owned `1131` `get_all_positions`/`get_watchlists`가 모두 regular market closed, account `ACTIVE`, positions `33`건, open orders `0`건, watchlists `0`건으로 일치했다.
- Recent reconciliation scope: scheduler-owned `1131` after-hours core/research preflight를 source-of-record로 사용했고, direct Alpaca MCP continuity check는 same-session after-hours submitted orders `0`, same-session fills `0`, shortlist `QQQ/MSFT/SMH/SPY/AVGO/SO/INTC/MU`의 live IEX quote parity, 그리고 `feed=overnight` quote/snapshot stale 상태를 재확인했다. separate after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned submit-boundary quote rows 기준 `QQQ`가 약 `1775.73`분 stale, `MSFT/SMH`가 `1790.80/1778.73`분 stale, `SPY/AVGO/SO/INTC/MU`는 약 `1833.36-1833.34`분 stale 또는 spread/notional cap fail이라 submit path에 진입하지 못했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-14-1131-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-14-1111-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음. direct Alpaca MCP `get_orders(status=all, after=2026-06-12T20:00:00Z)`와 scheduler-owned `1111` `orders_submitted=0` 기준 same-session after-hours order history도 `0`건이었다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: direct `get_clock`, `get_account_info`, `get_all_positions`, `get_orders(status=open)`, `get_watchlists`와 scheduler-owned `1111` `get_all_positions`/`get_watchlists`가 모두 regular market closed, account `ACTIVE`, positions `33`건, open orders `0`건, watchlists `0`건으로 일치했다.
- Recent reconciliation scope: scheduler-owned `1111` after-hours core/research preflight를 source-of-record로 사용했고, direct Alpaca MCP continuity check는 same-session after-hours orders `0`, positions `33`, open orders `0`, watchlists `0`를 재확인했다. separate after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned submit-boundary quote rows 기준 `QQQ`가 약 `1753.52`분 stale, `MSFT/SMH`가 `1768.59/1756.51`분 stale, `SPY/AVGO/SO/INTC/MU`는 약 `1811.14-1811.12`분 stale 또는 spread/notional cap fail이라 submit path에 진입하지 못했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-14-1111-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-14-1051-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음. direct Alpaca MCP `get_orders(status=all, after=2026-06-12T20:00:00Z)`와 `get_account_activities(activity_types=FILL, after=2026-06-12T20:00:00Z)` 기준 same-session after-hours order/fill history도 `0`건이었다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: direct `get_clock`, `get_account_info`, `get_all_positions`, `get_orders(status=open)`, `get_watchlists`와 scheduler-owned `1051` `get_all_positions`/`get_watchlists`가 모두 regular market closed, account `ACTIVE`, positions `33`건, open orders `0`건, watchlists `0`건으로 일치했다.
- Recent reconciliation scope: scheduler-owned `1051` after-hours core/research preflight를 source-of-record로 사용했고, direct Alpaca MCP continuity check는 same-session after-hours submitted orders `0`, same-session fills `0`, shortlist `QQQ/MSFT/SMH/SPY/AVGO/SO/INTC/MU`의 live IEX quote parity, 그리고 `feed=overnight` quote/snapshot stale 상태를 재확인했다. separate after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned submit-boundary quote rows 기준 `QQQ`가 약 `1733.52`분 stale, `MSFT/SMH`가 `1748.59/1736.52`분 stale, `SPY/AVGO/SO/INTC/MU`는 약 `1791.15-1791.12`분 stale 또는 spread/notional cap fail이라 submit path에 진입하지 못했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-14-1051-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-14-1031-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음. direct Alpaca MCP `get_orders(status=all, after=2026-06-12T20:00:00Z)`와 `get_account_activities(activity_types=FILL, after=2026-06-12T20:00:00Z)` 기준 same-session after-hours order/fill history도 `0`건이었다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: direct `get_all_positions`, `get_watchlists`와 scheduler-owned `1031` `get_all_positions`/`get_watchlists`가 모두 positions `33`건, watchlists `0`건으로 일치했다.
- Recent reconciliation scope: scheduler-owned `1031` after-hours core/research preflight를 source-of-record로 사용했고, direct Alpaca MCP continuity check는 open orders `0`, same-session after-hours orders `0`, same-session fills `0`, shortlist `QQQ/MSFT/SMH/SPY/AVGO/SO/INTC/MU`의 live IEX quote parity, 그리고 `feed=overnight` readback stale 상태를 재확인했다. separate after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned submit-boundary quote rows 기준 `QQQ`가 약 `1713.52`분 stale, `MSFT/SMH`가 `1728.59/1716.52`분 stale, `SPY/AVGO/SO/INTC/MU`는 약 `1771.15-1771.13`분 stale 또는 spread/notional cap fail이라 submit path에 진입하지 못했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-14-1031-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-14-1011-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음. direct Alpaca MCP `get_orders(status=all, after=2026-06-12T20:00:00Z)`와 `get_account_activities(activity_types=FILL, after=2026-06-12T20:00:00Z)` 기준 same-session after-hours order/fill history도 `0`건이었다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: direct `get_clock`, `get_account_info`, `get_all_positions`, `get_orders(status=open)`, `get_watchlists` 기준 regular market closed, account `ACTIVE`, positions `33`건, open orders `0`건, watchlists `0`건이었다.
- Recent reconciliation scope: scheduler-owned `1011` after-hours core/research preflight를 source-of-record로 사용했고, direct Alpaca MCP continuity check는 same-session after-hours submitted orders `0`, same-session fills `0`, live overnight quote/snapshot readback stale 상태를 재확인했다. separate after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned submit-boundary quote rows 기준 `QQQ`가 약 `1693.51`분 stale, `MSFT/SMH`가 `1708.58/1696.51`분 stale, `SPY/AVGO/SO/INTC/MU`는 약 `1751.14-1751.12`분 stale 또는 spread/notional cap fail이라 submit path에 진입하지 못했다. live overnight quote readback도 shortlist 전 종목에서 `2026-06-12T08:00:00Z` 부근 timestamp만 반환해 current clock 기준 약 `2472.66`분 stale였다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-14-1011-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-14-0951-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음. scheduler-owned `0951` `orders_submitted=0`, `get_orders_open=0` 기준 same-session after-hours order/fill history도 추가되지 않았다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: direct `get_all_positions`와 scheduler-owned `0951` `get_all_positions`가 모두 positions `33`건으로 일치했고, direct `get_watchlists`도 `0`건이었다.
- Recent reconciliation scope: scheduler-owned `0951` after-hours core/research preflight를 source-of-record로 사용했다. regular market closed, account `ACTIVE`, cash `31950.34 USD`, portfolio value `100415.12 USD`, buying power `302843.86 USD`, long market value `68464.78 USD`였다. 별도 after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned submit-boundary quote rows 기준 `QQQ`가 약 `1673.49`분 stale, `MSFT/SMH`가 `1688.56/1676.49`분 stale, `SPY/AVGO/SO/INTC/MU`는 약 `1731.12-1731.10`분 stale 또는 spread/notional cap fail이라 submit path에 진입하지 못했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-14-0951-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-14-0931-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음. scheduler-owned `0931` `orders_submitted=0`, `get_orders_open=0`, `get_watchlists=0` 기준 same-session after-hours order/fill history도 추가되지 않았다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `0931` `get_all_positions` 기준 positions `33`건, open orders `0`건, watchlists `0`건이었다.
- Recent reconciliation scope: scheduler-owned `0931` after-hours core/research preflight를 source-of-record로 사용했다. regular market closed, account `ACTIVE`, cash `31950.34 USD`, portfolio value `100415.12 USD`, buying power `302843.86 USD`, long market value `68464.78 USD`였다. 별도 after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned submit-boundary quote rows 기준 `QQQ`가 약 `1653.52`분 stale, `MSFT/SMH`가 `1668.59/1656.52`분 stale, `SPY/AVGO/SO/INTC/MU`는 약 `1711.15-1711.13`분 stale 또는 spread/notional cap fail이라 submit path에 진입하지 못했다. 이번 turn의 local sandbox `python3` 환경에는 `mcp` 모듈이 없어 별도 live Alpaca MCP continuity spot check는 재실행하지 않았다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-14-0931-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-14-0911-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음. live `get_orders(status=all, after=2026-06-12T20:00:00Z)`와 `get_account_activities(activity_types=FILL, after=2026-06-12T20:00:00Z)` 기준 same-session after-hours order/fill history도 `0`건이었다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `0911` `get_all_positions` 기준 positions `33`건이었고 live continuity check도 account `ACTIVE`, positions `33`, open orders `0`, watchlists `0`를 재확인했다. live overnight quote readback은 shortlist 전 종목에서 `2026-06-12T08:00:00Z` 부근의 더 오래된 timestamp만 반환했다.
- Recent reconciliation scope: scheduler-owned `0911` after-hours core/research preflight를 source-of-record로 사용했고 live Alpaca MCP `get_clock`, `get_account_info`, `get_all_positions`, `get_orders(status=open)`, `get_orders(status=all, after=2026-06-12T20:00:00Z)`, `get_account_activities(activity_types=FILL, after=2026-06-12T20:00:00Z)`, `get_watchlists`, `get_stock_latest_quote(feed=overnight)`, `get_stock_latest_quote(feed=iex)`로 continuity를 재확인했다. regular market closed, account `ACTIVE`, cash `31950.34 USD`, portfolio value `100415.12 USD`, buying power `302843.86 USD`, long market value `68464.78 USD`였다. 별도 after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned submit-boundary quote rows 기준 `QQQ`가 약 `1633.51`분 stale, `MSFT/SMH`가 `1648.59/1636.51`분 stale, `SPY/AVGO/SO/INTC/MU`는 약 `1691.14-1691.12`분 stale 또는 spread/notional cap fail이라 submit path에 진입하지 못했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-14-0911-after-hours-autopilot-post-trade.json`

- Run: [[2026-06-14-0851-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음. live `get_orders(status=all, after=2026-06-12T20:00:00Z)` 기준 same-session after-hours order/fill history도 `0`건이었다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `0851` `get_all_positions` 기준 positions `33`건이었다.
- Recent reconciliation scope: scheduler-owned `0851` after-hours core/research preflight를 source-of-record로 사용했고 live Alpaca MCP `get_orders(status=open)`, `get_orders(status=all, after=2026-06-12T20:00:00Z)`, `get_watchlists`로 continuity를 재확인했다. regular market closed, account `ACTIVE`, cash `31950.34 USD`, portfolio value `100415.12 USD`, buying power `302843.86 USD`, long market value `68464.78 USD`였다. 별도 after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned submit-boundary quote rows 기준 `QQQ`가 약 `1613.53`분 stale, `MSFT/SMH`가 `1628.60/1616.52`분 stale, `SPY/AVGO/SO/INTC/MU`는 약 `1671.15-1671.13`분 stale 또는 spread/notional cap fail이라 submit path에 진입하지 못했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-14-0851-after-hours-autopilot-post-trade.json`

- Run: [[2026-06-14-0831-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음. live `get_orders(status=all, after=2026-06-12T20:00:00Z)` 기준 same-session after-hours order/fill history도 `0`건이었다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `0831` `get_all_positions` 기준 positions `33`건이었고 live continuity check도 account `ACTIVE`, positions `33`, open orders `0`, watchlists `0`를 재확인했다. live overnight quote readback은 shortlist 전 종목에서 `2026-06-12T08:00:00Z` 부근의 더 오래된 timestamp만 반환했다.
- Recent reconciliation scope: scheduler-owned `0831` after-hours core/research preflight를 source-of-record로 사용했고 live Alpaca MCP `get_clock`, `get_account_info`, `get_all_positions`, `get_orders(status=open)`, `get_orders(status=all, after=2026-06-12T20:00:00Z)`, `get_watchlists`, `get_stock_latest_quote(feed=overnight)`, `get_stock_snapshot(feed=overnight)`로 continuity를 재확인했다. regular market closed, account `ACTIVE`, cash `31950.34 USD`, portfolio value `100415.12 USD`, buying power `302843.86 USD`, long market value `68464.78 USD`였다. 별도 after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned submit-boundary quote rows 기준 `QQQ`가 약 `1593.51`분 stale, `MSFT/SMH`가 `1608.59/1596.51`분 stale, `SPY/AVGO/SO/INTC/MU`는 약 `1651.14-1651.12`분 stale 또는 spread/notional cap fail이라 submit path에 진입하지 못했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-14-0831-after-hours-autopilot-post-trade.json`

- Run: [[2026-06-14-0811-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음. scheduler-owned `0811` `get_account_activities(activity_types=FILL, after=2026-06-12T20:00:00Z)` 기준 same-session after-hours fill history도 `0`건이었다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `0811` `get_all_positions` 기준 positions `33`건이었고 live continuity check도 account `ACTIVE`, positions `33`, open orders `0`, watchlists `0`를 재확인했다. live overnight quote readback은 shortlist 전 종목에서 `2026-06-12T08:00:00Z` 부근의 더 오래된 timestamp만 반환했다.
- Recent reconciliation scope: scheduler-owned `0811` after-hours core/research preflight를 source-of-record로 사용했고 live Alpaca MCP `get_clock`, `get_account_info`, `get_all_positions`, `get_orders(status=open)`, `get_orders(status=all, after=2026-06-12T20:00:00Z)`, `get_watchlists`, `get_asset`, `get_stock_latest_quote(feed=overnight)`, `get_stock_snapshot(feed=overnight)`로 continuity를 재확인했다. regular market closed, account `ACTIVE`, cash `31950.34 USD`, portfolio value `100415.12 USD`, buying power `302843.86 USD`, long market value `68464.78 USD`였다. 별도 after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned submit-boundary quote rows 기준 `QQQ`가 약 `1573.49`분 stale, `MSFT/SMH`가 `1588.57/1576.49`분 stale, `SPY/AVGO/SO/INTC/MU`는 약 `1631.12-1631.10`분 stale 또는 spread/notional cap fail이라 submit path에 진입하지 못했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-14-0811-after-hours-autopilot-post-trade.json`

- Run: [[2026-06-14-0751-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음. scheduler-owned `0751` `get_account_activities(activity_types=FILL, after=2026-06-12T20:00:00Z)` 기준 same-session after-hours fill history도 `0`건이었다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `0751` `get_all_positions` 기준 positions `33`건, open orders `0`건, watchlists `0`건이었다.
- Recent reconciliation scope: scheduler-owned `0751` after-hours core/research preflight를 source-of-record로 사용했고, regular market closed는 scheduler-owned `get_clock`=`2026-06-13T18:51:08.877176532-04:00` 기준 유지했다. account `ACTIVE`, cash `31950.34 USD`, portfolio value `100415.12 USD`, buying power `302843.86 USD`, long market value `68464.78 USD`였다. 별도 after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned submit-boundary quote rows 기준 `QQQ`가 약 `1553.52`분 stale, `MSFT/SMH`가 `1568.59/1556.52`분 stale, `SPY/AVGO/SO/INTC/MU`는 약 `1611.15-1611.13`분 stale 또는 spread/notional cap fail이라 submit path에 진입하지 못했다. 이번 turn의 local sandbox `python3` 환경에는 `mcp` 모듈이 없어 별도 read-only spot-check는 재실행하지 않았다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-14-0751-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-14-0731-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음. scheduler-owned `0731` `get_account_activities(activity_types=FILL, after=2026-06-12T20:00:00Z)` 기준 same-session after-hours fill history도 `0`건이었다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `0731` `get_all_positions` 기준 positions `33`건, open orders `0`건, watchlists `0`건이었다. live Alpaca MCP spot check는 `get_stock_latest_quote(feed=overnight)`와 `get_stock_snapshot(feed=overnight)`만 재실행했고 shortlist 전 종목에서 `2026-06-12T08:00:00Z` 부근의 더 오래된 overnight quote timestamp만 다시 반환했다.
- Recent reconciliation scope: scheduler-owned `0731` after-hours core/research preflight를 source-of-record로 사용했고, regular market closed는 scheduler-owned `get_clock`=`2026-06-13T18:31:09.64924439-04:00` 기준 유지했다. account `ACTIVE`, cash `31950.34 USD`, portfolio value `100415.12 USD`, buying power `302843.86 USD`, long market value `68464.78 USD`였다. 별도 after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned submit-boundary quote rows 기준 `QQQ`가 약 `1533.54`분 stale, `MSFT/SMH`가 `1548.61/1536.53`분 stale, `SPY/AVGO/SO/INTC/MU`는 약 `1591.16-1591.14`분 stale 또는 spread/notional cap fail이라 submit path에 진입하지 못했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-14-0731-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-14-0651-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음. live Alpaca MCP `get_account_activities(activity_types=FILL, after=2026-06-12T20:00:00Z)` 기준 same-session after-hours fill history도 `0`건이었다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `0651` `get_all_positions` 기준 positions `33`건, open orders `0`건이었고 live continuity check도 account `ACTIVE`, positions `33`, watchlists `0`를 재확인했다.
- Recent reconciliation scope: scheduler-owned `0651` after-hours core/research preflight를 source-of-record로 사용했고 live Alpaca MCP `get_account_info`, `get_all_positions`, `get_account_activities(activity_types=FILL, after=2026-06-12T20:00:00Z)`, `get_watchlists`, `get_stock_latest_quote(feed=overnight)`, `get_stock_snapshot(feed=overnight)`로 continuity를 재확인했다. regular market closed는 scheduler-owned `get_clock` 기준 유지했고, account `ACTIVE`, cash `31950.34 USD`, portfolio value `100415.12 USD`, buying power `302843.86 USD`, long market value `68464.78 USD`였다. 별도 after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned submit-boundary quote rows 기준 `QQQ`가 약 `1493.51`분 stale, `MSFT/SMH`가 `1508.58/1496.51`분 stale, `SPY/AVGO/SO/INTC/MU`는 약 `1551.14-1551.12`분 stale 또는 spread/notional cap fail이라 submit path에 진입하지 못했다. live overnight quote readback도 shortlist 전 종목에서 `2026-06-12T08:00:00Z` 부근의 더 오래된 timestamp만 반환했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-14-0651-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-14-0631-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음. same-session after-hours submitted order history도 `0`건이었다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `0631` `get_all_positions` 기준 positions `33`건, open orders `0`건이었고 live continuity check도 account `ACTIVE`, positions `33`, open orders `0`, same-session after-hours orders `0`, watchlists `0`를 재확인했다.
- Recent reconciliation scope: scheduler-owned `0631` after-hours core/research preflight를 source-of-record로 사용했고 live Alpaca MCP `get_clock`, `get_account_info`, `get_all_positions`, `get_orders(status=open)`, `get_orders(status=all, after=2026-06-12T20:00:00Z)`, `get_watchlists`로 continuity를 재확인했다. regular market closed, account `ACTIVE`, cash `31950.34 USD`, portfolio value `100415.12 USD`, buying power `302843.86 USD`, long market value `68464.78 USD`였다. 별도 after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned submit-boundary quote rows 기준 `QQQ`가 약 `1473.52`분 stale, `MSFT/SMH`가 `1488.59/1476.52`분 stale, `SPY/AVGO/SO/INTC/MU`는 약 `1531.15-1531.13`분 stale 또는 spread/notional cap fail이라 submit path에 진입하지 못했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-14-0631-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-14-0611-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음. same-session after-hours submitted order history도 `0`건이었다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `0611` `get_all_positions` 기준 positions `33`건, open orders `0`건이었고 live continuity check도 positions `33`, watchlists `0`를 재확인했다.
- Recent reconciliation scope: scheduler-owned `0611` after-hours core/research preflight를 source-of-record로 사용했고 live Alpaca MCP `get_clock`, `get_all_positions`, `get_watchlists`로 continuity를 재확인했다. regular market closed, account `ACTIVE`, cash `31950.34 USD`, portfolio value `100415.12 USD`, buying power `302843.86 USD`, long market value `68464.78 USD`였다. 별도 after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned submit-boundary quote rows 기준 `QQQ`가 약 `1453.52`분 stale, `MSFT/SMH`가 `1468.59/1456.52`분 stale, `SPY/AVGO/SO/INTC/MU`는 약 `1511.15-1511.13`분 stale 또는 spread/notional cap fail이라 submit path에 진입하지 못했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-14-0611-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-13-2011-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음. same-session after-hours submitted order history도 `0`건이었다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `2011` `get_all_positions` 기준 positions `33`건, open orders `0`건, `AVGO 4주`, `RGTI 37주`, `PFE 5주`였다. live continuity check도 account `ACTIVE`, open orders `0`, same-session after-hours orders `0`, watchlists `0`를 재확인했다.
- Recent reconciliation scope: scheduler-owned `2011` after-hours core/research preflight를 source-of-record로 사용했고 live Alpaca MCP `get_clock`, `get_account_info`, `get_all_positions`, `get_orders(status=open)`, `get_orders(status=all, after=2026-06-12T20:00:00Z)`, `get_watchlists`, `get_stock_latest_quote(feed=overnight)`로 continuity를 재확인했다. regular market closed, account `ACTIVE`, cash `31950.34 USD`, portfolio value `100415.12 USD`, buying power `302843.86 USD`, long market value `68464.78 USD`, watchlists `0`였다. 별도 after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned submit-boundary quote rows 기준 `QQQ`가 약 `853.52`분 stale, `MSFT/SMH`가 `868.59/856.52`분 stale, `SPY/AVGO/SO/INTC/MU`는 약 `911.15-911.13`분 stale 또는 spread/notional cap fail이라 submit path에 진입하지 못했다. live overnight quote readback도 더 오래된 timestamp만 반환해 submit 경로를 다시 열지 못했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-13-2011-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-13-1951-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음. same-session after-hours submitted order history도 `0`건이었다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `1951` `get_all_positions` 기준 positions `33`건, open orders `0`건, `AVGO 4주`, `RGTI 37주`, `PFE 5주`였다. live continuity check도 account `ACTIVE`, open orders `0`, same-session after-hours orders `0`, watchlists `0`를 재확인했다.
- Recent reconciliation scope: scheduler-owned `1951` after-hours core/research preflight를 source-of-record로 사용했고 live Alpaca MCP `get_clock`, `get_account_info`, `get_all_positions`, `get_orders(status=open)`, `get_orders(status=all, after=2026-06-12T20:00:00Z)`, `get_watchlists`, `get_stock_latest_quote(feed=overnight)`로 continuity를 재확인했다. regular market closed, account `ACTIVE`, cash `31950.34 USD`, portfolio value `100415.12 USD`, buying power `302843.86 USD`, long market value `68464.78 USD`, watchlists `0`였다. 별도 after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned submit-boundary quote rows 기준 `QQQ`가 약 `833.52`분 stale, `MSFT/SMH`가 `848.59/836.51`분 stale, `SPY/AVGO/SO/INTC/MU`는 약 `891.14-891.12`분 stale 또는 spread/notional cap fail이라 submit path에 진입하지 못했다. live overnight quote readback도 더 오래된 timestamp만 반환해 submit 경로를 다시 열지 못했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-13-1951-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-13-1931-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음. same-session after-hours submitted order history도 `0`건이었다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `1931` `get_all_positions` 기준 positions `33`건, open orders `0`건, `AVGO 4주`, `RGTI 37주`, `PFE 5주`였다. live continuity check도 open orders `0`, same-session after-hours orders `0`, watchlists `0`를 재확인했다.
- Recent reconciliation scope: scheduler-owned `1931` after-hours core/research preflight를 source-of-record로 사용했고 live Alpaca MCP `get_clock`, `get_all_positions`, `get_orders(status=open)`, `get_orders(status=all, after=2026-06-12T20:00:00Z)`, `get_watchlists`로 continuity를 재확인했다. regular market closed, account `ACTIVE`, cash `31950.34 USD`, portfolio value `100415.12 USD`, buying power `302843.86 USD`, long market value `68464.78 USD`, watchlists `0`였다. 별도 after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned submit-boundary quote rows 기준 `QQQ`가 약 `813.50`분 stale, `MSFT/SMH`가 `828.57/816.50`분 stale, `SPY/AVGO/SO/INTC/MU`는 약 `871.13-871.11`분 stale 또는 spread/notional cap fail이라 submit path에 진입하지 못했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-13-1931-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-13-1851-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음. same-session after-hours submitted order history도 `0`건이었다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `1851` `get_all_positions` 기준 positions `33`건, open orders `0`건, `AVGO 4주`, `RGTI 37주`, `PFE 5주`였다.
- Recent reconciliation scope: scheduler-owned `1851` after-hours core/research preflight를 source-of-record로 사용했다. regular market closed, account `ACTIVE`, cash `31950.34 USD`, portfolio value `100415.12 USD`, buying power `302843.86 USD`, long market value `68464.78 USD`, watchlists `0`였다. 별도 after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned submit-boundary quote rows 기준 `QQQ`가 약 `773.50`분 stale, `MSFT/SMH`가 `788.57/776.49`분 stale, `SPY/AVGO/SO/INTC/MU`는 약 `831.12-831.10`분 stale 또는 spread/notional cap fail이라 submit path에 진입하지 못했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-13-1851-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-13-1831-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음. same-session after-hours submitted order history도 `0`건이었다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `1831` `get_all_positions` 기준 positions `33`건, open orders `0`건, `AVGO 4주`, `RGTI 37주`, `PFE 5주`였다.
- Recent reconciliation scope: scheduler-owned `1831` after-hours core/research preflight를 source-of-record로 사용했다. regular market closed, account `ACTIVE`, cash `31950.34 USD`, portfolio value `100415.12 USD`, buying power `302843.86 USD`, long market value `68464.78 USD`, watchlists `0`였다. 별도 after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned submit-boundary quote rows 기준 `QQQ`가 약 `753.51`분 stale, `MSFT/SMH`가 `768.58/756.51`분 stale, `SPY/AVGO/SO/INTC/MU`는 약 `811.14-811.12`분 stale 또는 spread/notional cap fail이라 submit path에 진입하지 못했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-13-1831-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-13-1811-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음. same-session after-hours order history도 `0`건이었다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `1811` `get_all_positions` 기준 positions `33`건, open orders `0`건, `AVGO 4주`, `RGTI 37주`, `PFE 5주`였다.
- Recent reconciliation scope: scheduler-owned `1811` after-hours core/research preflight를 source-of-record로 사용했다. regular market closed, account `ACTIVE`, cash `31950.34 USD`, portfolio value `100415.12 USD`, buying power `302843.86 USD`, long market value `68464.78 USD`, watchlists `0`였다. 별도 after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned submit-boundary quote rows 기준 `QQQ`가 약 `733.45`분 stale, `MSFT/SMH`가 `748.52/736.44`분 stale, `SPY/AVGO/SO/INTC/MU`는 약 `791.07-791.05`분 stale 또는 spread/notional cap fail이라 submit path에 진입하지 못했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-13-1811-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-13-1651-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음. same-session after-hours order history도 `0`건이었다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `1651` `get_all_positions` 기준 positions `33`건, open orders `0`건, `AVGO 4주`, `RGTI 37주`, `PFE 5주`였다. live continuity check도 open orders `0`, same-session after-hours orders `0`, watchlists `0`를 재확인했다.
- Recent reconciliation scope: scheduler-owned `1651` after-hours core/research preflight를 source-of-record로 사용했고 live Alpaca MCP `get_clock`, `get_account_info`, `get_all_positions`, `get_orders(status=open)`, `get_orders(status=all, after=2026-06-12T20:00:00Z)`, `get_watchlists`, `get_stock_latest_quote(feed=overnight)` spot check로 continuity를 재확인했다. regular market closed, account `ACTIVE`, cash `31,950.36 USD`, portfolio value `100,415.14 USD`, buying power `302,843.94 USD`, long market value `68,464.78 USD`, watchlists `0`였다. 별도 after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned submit-boundary quote rows 기준 `QQQ`가 약 `653.51`분 stale, `MSFT/SMH`가 `668.58/656.50`분 stale, `SPY/AVGO/SO/INTC/MU`는 약 `711.13-711.11`분 stale 또는 spread/notional cap fail이라 submit path에 진입하지 못했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-13-1651-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-13-1551-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음. same-session after-hours order history도 `0`건이었다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `1551` `get_all_positions` 기준 positions `33`건, open orders `0`건, `AVGO 4주`, `RGTI 37주`, `PFE 5주`였다. live continuity check도 open orders `0`, same-session after-hours orders `0`, watchlists `0`를 재확인했다.
- Recent reconciliation scope: scheduler-owned `1551` after-hours core/research preflight를 source-of-record로 사용했고 live Alpaca MCP `get_orders(status=open)`, `get_orders(status=all, after=2026-06-12T20:00:00Z)`, `get_watchlists`, `get_stock_latest_quote(feed=overnight)` spot check로 continuity를 재확인했다. regular market closed, account `ACTIVE`, cash `31,950.36 USD`, portfolio value `100,415.14 USD`, buying power `302,843.94 USD`, long market value `68,464.78 USD`, watchlists `0`였다. 별도 after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned submit-boundary quote rows 기준 `QQQ`가 약 `593.53`분 stale, `MSFT/SMH`가 `608.60/596.52`분 stale, `SPY/AVGO/SO/INTC/MU`는 약 `651.15-651.13`분 stale 또는 spread/notional cap fail이라 submit path에 진입하지 못했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-13-1551-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-13-1531-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음. same-session after-hours order history도 `0`건이었다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `1531` `get_all_positions` 기준 positions `33`건, open orders `0`건, `AVGO 4주`, `RGTI 37주`, `PFE 5주`였다.
- Recent reconciliation scope: scheduler-owned `1531` after-hours core/research preflight를 source-of-record로 사용했다. regular market closed, account `ACTIVE`, cash `31,950.36 USD`, portfolio value `100,415.14 USD`, buying power `302,843.94 USD`, long market value `68,464.78 USD`, watchlists `0`였다. 별도 after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned submit-boundary quote rows 기준 `QQQ`가 약 `573.49`분 stale, `MSFT/SMH`가 `588.56/576.49`분 stale, `SPY/AVGO/SO/INTC/MU`는 약 `631.12/631.12/631.12/631.12/631.10`분 stale 또는 spread/notional cap fail이라 submit path에 진입하지 못했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-13-1531-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-13-1511-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음. same-session after-hours order history도 `0`건이었다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `1511` `get_all_positions` 기준 positions `33`건, open orders `0`건, `AVGO 4주`, `RGTI 37주`, `PFE 5주`였다. live continuity readback도 동일했다.
- Recent reconciliation scope: scheduler-owned `1511` after-hours core/research preflight를 source-of-record로 사용했고 live Alpaca MCP `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-12T20:00:00Z)/get_watchlists`로 continuity를 재확인했다. regular market closed, account `ACTIVE`, cash `31,950.36 USD`, portfolio value `100,415.14 USD`, buying power `302,843.94 USD`, long market value `68,464.78 USD`, watchlists `0`였다. 별도 after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned submit-boundary quote rows 기준 `QQQ`가 약 `556.59`분 stale, `MSFT/SMH`가 `571.66/559.58`분 stale, `SPY/AVGO/SO/INTC/MU`는 약 `614.21-614.19`분 stale 또는 spread/notional cap fail이라 submit path에 진입하지 못했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-13-1511-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-13-1451-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음. same-session after-hours order history도 `0`건이었다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `1451` `get_all_positions` 기준 positions `33`건, open orders `0`건, `AVGO 4주`, `RGTI 37주`, `PFE 5주`였다. live continuity readback도 동일했다.
- Recent reconciliation scope: scheduler-owned `1451` after-hours core/research preflight를 source-of-record로 사용했고 live Alpaca MCP `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-12T20:00:00Z)/get_watchlists`로 continuity를 재확인했다. regular market closed, account `ACTIVE`, cash `31,950.36 USD`, portfolio value `100,415.14 USD`, buying power `302,843.94 USD`, long market value `68,464.78 USD`, watchlists `0`였다. 별도 after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned submit-boundary quote rows 기준 `QQQ`가 약 `535.29`분 stale, `MSFT/SMH`가 `550.36/538.29`분 stale, `SPY/AVGO/SO/INTC/MU`는 약 `592.92-592.89`분 stale 또는 spread/notional cap fail이라 submit path에 진입하지 못했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-13-1451-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-13-1431-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음. same-session after-hours order history도 `0`건이었다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `1431` `get_all_positions` 기준 positions `33`건, open orders `0`건, `AVGO 4주`, `RGTI 37주`, `PFE 5주`였다. live continuity readback도 동일했다.
- Recent reconciliation scope: scheduler-owned `1431` after-hours core/research preflight를 source-of-record로 사용했고 live Alpaca MCP `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-12T20:00:00Z)/get_watchlists`로 continuity를 재확인했다. regular market closed, account `ACTIVE`, cash `31,950.36 USD`, portfolio value `100,415.14 USD`, buying power `302,843.94 USD`, long market value `68,464.78 USD`, watchlists `0`였다. 별도 after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned submit-boundary quote rows 기준 `QQQ`가 약 `514.77`분 stale, `MSFT/SMH`가 `529.84/517.77`분 stale, `SPY/AVGO/SO/INTC/MU`는 약 `572.40-572.38`분 stale 또는 spread/notional cap fail이라 submit path에 진입하지 못했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-13-1431-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-13-1411-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음. same-session after-hours order history도 `0`건이었다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `1411` `get_all_positions` 기준 positions `33`건, open orders `0`건, `AVGO 4주`, `RGTI 37주`, `PFE 5주`였다. live continuity readback도 동일했다.
- Recent reconciliation scope: scheduler-owned `1411` after-hours core/research preflight를 source-of-record로 사용했고 live Alpaca MCP `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-12T20:00:00Z)/get_watchlists`로 continuity를 재확인했다. regular market closed, account `ACTIVE`, cash `31,950.36 USD`, portfolio value `100,415.14 USD`, buying power `302,843.94 USD`, long market value `68,464.78 USD`, watchlists `0`였다. 별도 after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned submit-boundary quote rows 기준 `QQQ`가 약 `495.71`분 stale, `MSFT/SMH`가 `510.78/498.71`분 stale, `SPY/AVGO/SO/INTC/MU`는 약 `553.34-553.31`분 stale 또는 spread/notional cap fail이라 submit path에 진입하지 못했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-13-1411-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-13-1351-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음. same-session after-hours order history도 `0`건이었다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `1351` `get_all_positions` 기준 positions `33`건, open orders `0`건, `AVGO 4주`, `RGTI 37주`, `PFE 5주`였다. live continuity readback도 동일했다.
- Recent reconciliation scope: scheduler-owned `1351` after-hours core/research preflight를 source-of-record로 사용했고 live Alpaca MCP `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-12T20:00:00Z)/get_watchlists`로 continuity를 재확인했다. regular market closed, account `ACTIVE`, cash `31,950.36 USD`, portfolio value `100,415.14 USD`, buying power `302,843.94 USD`, long market value `68,464.78 USD`, watchlists `0`였다. 별도 after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned submit-boundary quote rows 기준 `QQQ`가 약 `475.03`분 stale, `MSFT/SMH`가 `490.10/478.02`분 stale, `SPY/AVGO/SO/INTC/MU`는 약 `532.65-532.63`분 stale 또는 spread/notional cap fail이라 submit path에 진입하지 못했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-13-1351-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-13-1331-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음. same-session after-hours order history도 `0`건이었다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `1331` `get_all_positions` 기준 positions `33`건, open orders `0`건, `AVGO 4주`, `RGTI 37주`, `PFE 5주`였다. live continuity readback도 동일했다.
- Recent reconciliation scope: scheduler-owned `1331` after-hours core/research preflight를 source-of-record로 사용했고 live Alpaca MCP `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-12T20:00:00Z)/get_watchlists`로 continuity를 재확인했다. regular market closed, account `ACTIVE`, cash `31,950.36 USD`, portfolio value `100,415.14 USD`, buying power `302,843.94 USD`, long market value `68,464.78 USD`, watchlists `0`였다. 별도 after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned submit-boundary quote rows 기준 `QQQ`가 약 `456.61`분 stale, `MSFT/SMH`가 `471.68/459.60`분 stale, `SPY/AVGO/SO/INTC/MU`는 약 `514.23-514.21`분 stale 또는 spread/notional cap fail이라 submit path에 진입하지 못했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-13-1331-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-13-1311-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음. same-session after-hours order history도 `0`건이었다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `1311` `get_all_positions` 기준 positions `33`건, open orders `0`건, `AVGO 4주`, `RGTI 37주`, `PFE 5주`였다. live continuity readback도 동일했다.
- Recent reconciliation scope: scheduler-owned `1311` after-hours core/research preflight를 source-of-record로 사용했고 live Alpaca MCP `get_clock/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-12T20:00:00Z)/get_watchlists`로 continuity를 재확인했다. regular market closed, account `ACTIVE`, cash `31,950.36 USD`, portfolio value `100,415.14 USD`, buying power `302,843.94 USD`, long market value `68,464.78 USD`, watchlists `0`였다. 별도 after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned submit-boundary quote rows 기준 `QQQ`가 약 `435.87`분 stale, `MSFT/SMH`가 `450.94/438.87`분 stale, `SPY/AVGO/SO/INTC/MU`는 약 `493.50-493.47`분 stale 또는 spread/notional cap fail이라 submit path에 진입하지 못했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-13-1311-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-13-1251-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음. same-session after-hours order history도 `0`건이었다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `1251` `get_all_positions` 기준 positions `33`건, open orders `0`건, `AVGO 4주`, `RGTI 37주`, `PFE 5주`였다. live continuity readback도 동일했다.
- Recent reconciliation scope: scheduler-owned `1251` after-hours core/research preflight를 source-of-record로 사용했고 live Alpaca MCP `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-12T20:00:00Z)/get_watchlists`로 continuity를 재확인했다. regular market closed, account `ACTIVE`, cash `31,950.36 USD`, portfolio value `100,415.14 USD`, buying power `302,843.94 USD`, long market value `68,464.78 USD`, watchlists `0`였다. 별도 after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned submit-boundary quote rows 기준 `QQQ`가 약 `413.65`분 stale, `MSFT/SMH`가 `428.72/416.64`분 stale, `SPY/AVGO/SO/INTC/MU`는 약 `471.27-471.25`분 stale 또는 spread/notional cap fail이라 submit path에 진입하지 못했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-13-1251-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-13-1231-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음. same-session after-hours order history도 `0`건이었다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `1231` `get_all_positions` 기준 positions `33`건, open orders `0`건, `AVGO 4주`, `RGTI 37주`, `PFE 5주`였다. live continuity readback도 동일했다.
- Recent reconciliation scope: scheduler-owned `1231` after-hours core/research preflight를 source-of-record로 사용했고 live Alpaca MCP `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-12T20:00:00Z)/get_watchlists`로 continuity를 재확인했다. regular market closed, account `ACTIVE`, cash `31,950.36 USD`, portfolio value `100,415.14 USD`, buying power `302,843.94 USD`, long market value `68,464.78 USD`, watchlists `0`였다. 별도 after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned submit-boundary quote rows 기준 `QQQ`가 약 `393.52`분 stale, `MSFT/SMH`가 `408.59/396.52`분 stale, `SPY/AVGO/SO/INTC/MU`는 약 `451.14-451.12`분 stale 또는 spread/notional cap fail이라 submit path에 진입하지 못했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-13-1231-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-13-1211-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음. same-session after-hours order history도 `0`건이었다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `1211` `get_all_positions` 기준 positions `33`건, open orders `0`건, `AVGO 4주`, `RGTI 37주`, `PFE 5주`였다. live continuity readback도 동일했다.
- Recent reconciliation scope: scheduler-owned `1211` after-hours core/research preflight를 source-of-record로 사용했고 live Alpaca MCP `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-12T20:00:00Z)/get_watchlists`로 continuity를 재확인했다. regular market closed, account `ACTIVE`, cash `31,950.36 USD`, portfolio value `100,415.14 USD`, buying power `302,843.94 USD`, long market value `68,464.78 USD`, watchlists `0`였다. 별도 after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned submit-boundary quote rows 기준 `QQQ`가 약 `373.51`분 stale, `MSFT/SMH`가 `388.59/376.51`분 stale, `SPY/AVGO/SO/INTC/MU`는 약 `431.14-431.12`분 stale 또는 spread/notional cap fail이라 submit path에 진입하지 못했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-13-1211-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-13-1151-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음. same-session after-hours order history도 `0`건이었다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `1151` `get_all_positions` 기준 positions `33`건, open orders `0`건, `AVGO 4주`, `RGTI 37주`, `PFE 5주`였다.
- Recent reconciliation scope: scheduler-owned `1151` after-hours core/research preflight를 source-of-record로 사용했다. regular market closed, account `ACTIVE`, cash `31,950.36 USD`, portfolio value `100,415.14 USD`, buying power `302,843.94 USD`, long market value `68,464.78 USD`, watchlists `0`였다. 별도 after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned submit-boundary quote rows 기준 `QQQ`가 약 `353.52`분 stale, `MSFT/SMH`가 `368.59/356.52`분 stale, `SPY/AVGO/SO/INTC/MU`는 약 `411.15-411.13`분 stale 또는 spread/notional cap fail이라 submit path에 진입하지 못했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-13-1151-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-13-1131-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음. same-session after-hours order history도 `0`건이었다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `1131` `get_all_positions` 기준 positions `33`건, open orders `0`건, `AVGO 4주`, `RGTI 37주`, `PFE 5주`였다.
- Recent reconciliation scope: scheduler-owned `1131` after-hours core/research preflight를 source-of-record로 사용했다. regular market closed, account `ACTIVE`, cash `31,950.36 USD`, portfolio value `100,415.14 USD`, buying power `302,843.94 USD`, long market value `68,464.78 USD`, watchlists `0`였다. 별도 after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned submit-boundary quote rows 기준 `QQQ`가 약 `333.45`분 stale, `MSFT/SMH`가 `348.52/336.44`분 stale, `SPY/AVGO/SO/INTC/MU`는 약 `391.07-391.05`분 stale 또는 spread/notional cap fail이라 submit path에 진입하지 못했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-13-1131-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-13-1111-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음. same-session after-hours order history도 `0`건이었다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `1111` `get_all_positions` 기준 positions `33`건, open orders `0`건, `AVGO 4주`, `RGTI 37주`, `PFE 5주`였다.
- Recent reconciliation scope: scheduler-owned `1111` after-hours core/research preflight를 source-of-record로 사용했다. regular market closed, account `ACTIVE`, cash `31,950.36 USD`, portfolio value `100,415.14 USD`, buying power `302,843.94 USD`, long market value `68,464.78 USD`, watchlists `0`였다. 별도 after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned submit-boundary quote rows 기준 `QQQ`가 약 `313.48`분 stale, `MSFT/SMH`가 `328.55/316.47`분 stale, `SPY/AVGO/SO/INTC/MU`는 약 `371.1-371.08`분 stale 또는 spread/notional cap fail이라 submit path에 진입하지 못했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-13-1111-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-13-1051-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음. same-session after-hours order history도 `0`건이었다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `1051` `get_all_positions` 기준 positions `33`건, open orders `0`건, `AVGO 4주`, `RGTI 37주`, `PFE 5주`였다.
- Recent reconciliation scope: scheduler-owned `1051` after-hours core/research preflight를 source-of-record로 사용했다. regular market closed, account `ACTIVE`, cash `31,950.36 USD`, portfolio value `100,646.86 USD`, buying power `303,392.01 USD`, long market value `68,696.50 USD`, watchlists `0`였다. 별도 after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned submit-boundary quote rows 기준 `QQQ`가 약 `293.54`분 stale, `MSFT/SMH`가 `308.61/296.53`분 stale, `SPY/AVGO/SO/INTC/MU`는 약 `351.16-351.14`분 stale 또는 spread/notional cap fail이라 submit path에 진입하지 못했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-13-1051-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-13-1031-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음. same-session after-hours order history도 `0`건이었다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: live `get_all_positions` 기준 positions `33`건, open orders `0`건, `AVGO 4주`, `RGTI 37주`, `PFE 5주`였다.
- Recent reconciliation scope: scheduler-owned `1031` after-hours core/research preflight를 source-of-record로 사용했고 live Alpaca MCP `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-12T20:00:00Z)/get_watchlists`로 continuity를 재확인했다. regular market closed, account `ACTIVE`, cash `31,950.36 USD`, portfolio value `100,646.86 USD`, buying power `303,392.01 USD`, long market value `68,696.50 USD`, watchlists `0`였다. 별도 after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned submit-boundary quote rows 기준 `QQQ`가 약 `275.20`분 stale, `MSFT/SMH`가 `290.27/278.20`분 stale, `SPY/AVGO/SO/INTC/MU`는 약 `332.81-332.83`분 stale 또는 spread/notional cap fail이라 submit path에 진입하지 못했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-13-1031-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-13-1011-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음. same-session after-hours order history도 `0`건이었다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: live `get_all_positions` 기준 positions `33`건, open orders `0`건, `AVGO 4주`, `RGTI 37주`, `PFE 5주`였다.
- Recent reconciliation scope: scheduler-owned `1011` after-hours core/research preflight를 source-of-record로 사용했고 live Alpaca MCP `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-12T20:00:00Z)/get_watchlists`로 continuity를 재확인했다. regular market closed, account `ACTIVE`, cash `31,950.36 USD`, portfolio value `100,646.86 USD`, buying power `303,392.01 USD`, long market value `68,696.50 USD`, watchlists `0`였다. 별도 after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned submit-boundary quote rows 기준 `QQQ`가 약 `255.51`분 stale, `MSFT/SMH`가 `270.58/258.51`분 stale, `SPY/AVGO/SO/INTC/MU`는 약 `313.12-313.14`분 stale 또는 spread/notional cap fail이라 submit path에 진입하지 못했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-13-1011-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-13-0951-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음. same-session after-hours order history도 `0`건이었다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: live `get_all_positions` 기준 positions `33`건, open orders `0`건, `AVGO 4주`, `RGTI 37주`, `PFE 5주`였다.
- Recent reconciliation scope: scheduler-owned `0951` after-hours core/research preflight를 source-of-record로 사용했고 live Alpaca MCP `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-12T20:00:00Z)/get_watchlists`로 continuity를 재확인했다. regular market closed, account `ACTIVE`, cash `31,950.36 USD`, portfolio value `100,646.86 USD`, buying power `303,392.01 USD`, long market value `68,696.50 USD`, watchlists `0`였다. 별도 after-hours order budget은 `0/2`로 열려 있었지만 scheduler-owned submit-boundary quote rows 기준 `QQQ`가 약 `233.51`분 stale, `MSFT/SMH`가 `248.58/236.51`분 stale, `SPY/AVGO/SO/INTC/MU`는 약 `291.12-291.14`분 stale 또는 spread/notional cap fail이라 submit path에 진입하지 못했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-13-0951-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-13-0911-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음. same-session after-hours order history도 `0`건이었다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: live `get_all_positions` 기준 positions `33`건, open orders `0`건, `AVGO 4주`, `RGTI 37주`, `PFE 5주`였다.
- Recent reconciliation scope: scheduler-owned `0911` after-hours core/research preflight를 source-of-record로 사용했고 live Alpaca MCP `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-12T20:00:00Z)/get_watchlists/get_stock_latest_quote(feed=iex)/get_stock_latest_quote(feed=overnight)`로 continuity와 quote boundary를 재확인했다. regular market closed, account `ACTIVE`, cash `31,950.36 USD`, portfolio value `100,646.86 USD`, buying power `303,392.01 USD`, long market value `68,696.50 USD`, watchlists `0`였다. 별도 after-hours order budget은 `0/2`로 열려 있었지만 freshest scheduler-owned IEX quote `QQQ 722.00/722.21`도 약 `195.39`분 stale이었고 `MSFT/SMH`도 `210.46/198.39`분 stale, `SPY/AVGO/SO/INTC/MU`는 약 `253.02`분 stale 또는 spread/notional cap fail이었으며, live `overnight` quote는 `2026-06-12T08:00:00Z` snapshot만 반환해 submit path를 열지 못했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-13-0911-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-13-0851-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음. same-session after-hours order history도 `0`건이었다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: live `get_all_positions` 기준 positions `33`건, open orders `0`건, `AVGO 4주`, `RGTI 37주`, `PFE 5주`였다.
- Recent reconciliation scope: scheduler-owned `0851` after-hours core/research preflight를 source-of-record로 사용했고 live Alpaca MCP `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-12T20:00:00Z)/get_watchlists/get_stock_latest_quote(feed=iex)/get_stock_latest_quote(feed=overnight)`로 continuity와 quote boundary를 재확인했다. regular market closed, account `ACTIVE`, cash `31,950.36 USD`, portfolio value `100,671.85 USD`, buying power `303,450.17 USD`, long market value `68,721.49 USD`, watchlists `0`였다. 별도 after-hours order budget은 `0/2`로 열려 있었지만 freshest scheduler-owned IEX quote `QQQ 722.00/722.21`도 약 `173.52`분 stale이었고 `MSFT/SMH`도 `188.59/176.51`분 stale, `SPY/AVGO/SO/INTC/MU`는 약 `231`분 stale 또는 spread/notional cap fail이었으며, live `overnight` quote는 `2026-06-12T08:00:00Z` snapshot만 반환해 submit path를 열지 못했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-13-0851-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-13-0831-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음. same-session after-hours order history도 `0`건이었다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: live `get_all_positions` 기준 positions `33`건, open orders `0`건, `AVGO 4주`, `RGTI 37주`, `PFE 5주`였다.
- Recent reconciliation scope: scheduler-owned `0831` after-hours core/research preflight를 source-of-record로 사용했고 live Alpaca MCP `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-12T20:00:00Z)/get_watchlists`로 continuity를 재확인했다. regular market closed, account `ACTIVE`, cash `31,950.36 USD`, portfolio value `100,631.97 USD`, buying power `303,315.98 USD`, long market value `68,681.61 USD`, watchlists `0`였다. 별도 after-hours order budget은 `0/2`로 열려 있었지만 freshest shortlisted quote `QQQ 722.00/722.21`도 약 `153.53`분 stale이었고 `MSFT/SMH`도 `168.60/156.52`분 stale, `SPY/AVGO/SO/INTC/MU`는 약 `211`분 stale 또는 spread/notional cap fail이라 submit path에 진입하지 못했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-13-0831-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-13-0811-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음. same-session after-hours order history도 `0`건이었다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: live `get_all_positions` 기준 positions `33`건, open orders `0`건, `AVGO 4주`, `RGTI 37주`, `PFE 5주`였다.
- Recent reconciliation scope: scheduler-owned `0811` after-hours core/research preflight를 source-of-record로 사용했고 live Alpaca MCP `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-12T20:00:00Z)/get_watchlists`로 continuity를 재확인했다. regular market closed, account `ACTIVE`, cash `31,950.36 USD`, portfolio value `100,568.87 USD`, buying power `303,195.59 USD`, long market value `68,618.51 USD`, watchlists `0`였다. 별도 after-hours order budget은 `0/2`로 열려 있었지만 freshest shortlisted quote `QQQ 722.00/722.21`도 약 `133.52`분 stale이었고 `MSFT/SMH`도 `148.59/136.51`분 stale, `SPY/AVGO/SO/INTC/MU`는 약 `191`분 stale 또는 spread/notional cap fail이라 submit path에 진입하지 못했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-13-0811-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-13-0751-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음. same-session after-hours order history도 `0`건이었다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `0751` `get_all_positions` 기준 positions `33`건, open orders `0`건, `AVGO 4주`, `RGTI 37주`, `PFE 5주`였다.
- Recent reconciliation scope: scheduler-owned `0751` after-hours core/research preflight를 source-of-record로 사용했다. regular market closed, account `ACTIVE`, cash `31,950.36 USD`, portfolio value `100,550.26 USD`, buying power `303,166.01 USD`, long market value `68,599.90 USD`, watchlists `0`였다. 별도 after-hours order budget은 `0/2`로 열려 있었지만 freshest shortlisted quote `QQQ 722.00/722.21`도 약 `113.51`분 stale이었고 runtime `overnight` quote는 `08:00Z` snapshot만 반환했으며 `boats`는 subscription 403이라 submit path에 진입하지 못했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-13-0751-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-13-0731-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음. same-session after-hours order history도 `0`건이었다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `0731` `get_all_positions` 기준 positions `33`건, open orders `0`건, `AVGO 4주`, `RGTI 37주`, `PFE 5주`였다.
- Recent reconciliation scope: scheduler-owned `0731` after-hours core/research preflight를 source-of-record로 사용했다. regular market closed, account `ACTIVE`, cash `31,950.36 USD`, portfolio value `100,545.98 USD`, buying power `303,120.24 USD`, long market value `68,595.62 USD`, watchlists `0`였다. 별도 after-hours order budget은 `0/2`로 열려 있었지만 freshest shortlisted quote `QQQ 722.00/722.21`도 약 `93.53`분 stale이라 submit path에 진입하지 못했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-13-0731-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-13-0711-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음. same-session after-hours order history도 `0`건이었다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `0711` `get_all_positions` 기준 positions `33`건, open orders `0`건, `AVGO 4주`, `RGTI 37주`, `PFE 5주`였다.
- Recent reconciliation scope: scheduler-owned `0711` after-hours core/research preflight를 source-of-record로 사용했다. regular market closed, account `ACTIVE`, cash `31,950.36 USD`, portfolio value `100,495.93 USD`, buying power `302,991.36 USD`, long market value `68,545.57 USD`, watchlists `0`였다. 별도 after-hours order budget은 `0/2`로 열려 있었지만 freshest shortlisted quote `QQQ 722.00/722.21`도 약 `73.52`분 stale이라 submit path에 진입하지 못했다. manual runtime Alpaca MCP retry는 DNS ConnectError로 실패했지만 submit path를 다시 열지는 못했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-13-0711-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-13-0651-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음. same-session after-hours order history도 `0`건이었다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime `get_all_positions` 기준 positions `33`건, open orders `0`건, `AVGO 4주`, `RGTI 37주`, `PFE 5주`였다.
- Recent reconciliation scope: scheduler-owned `0651` after-hours core/research preflight를 source-of-record로 사용했고 runtime Alpaca MCP `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-12T20:00:00Z)/get_watchlists`로 continuity만 재확인했다. regular market closed, account `ACTIVE`, cash `31,950.36 USD`, portfolio value `100,506.80 USD`, buying power `303,022.13 USD`, long market value `68,556.44 USD`, watchlists `0`였다. 별도 after-hours order budget은 `0/2`로 열려 있었지만 freshest shortlisted quote `QQQ 722.00/722.21`도 약 `55.52`분 stale이라 submit path에 진입하지 못했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-13-0651-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-13-0631-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음. same-session after-hours order history도 `0`건이었다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime `get_all_positions` 기준 positions `33`건, open orders `0`건, `AVGO 4주`, `RGTI 37주`, `PFE 5주`였다.
- Recent reconciliation scope: scheduler-owned `0631` after-hours core/research preflight를 source-of-record로 사용했고 runtime Alpaca MCP `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-12T20:00:00Z)/get_watchlists`로 continuity만 재확인했다. regular market closed, account `ACTIVE`, cash `31,950.36 USD`, portfolio value `100,481.76 USD`, buying power `302,940.31 USD`, long market value `68,531.40 USD`, watchlists `0`였다. 별도 after-hours order budget은 `0/2`로 열려 있었지만 freshest shortlisted quote `QQQ 722.00/722.21`도 약 `33.54`분 stale이라 submit path에 진입하지 못했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-13-0631-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-13-0611-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음. same-session after-hours order history도 `0`건이었다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime `get_all_positions` 기준 positions `33`건, open orders `0`건, `AVGO 4주`, `RGTI 37주`, `PFE 5주`였다.
- Recent reconciliation scope: scheduler-owned `0611` after-hours core/research preflight를 source-of-record로 사용했고 runtime Alpaca MCP `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-12T20:00:00Z)/get_watchlists`로 continuity만 재확인했다. regular market closed, account `ACTIVE`, cash `31,950.36 USD`, portfolio value `100,493.58 USD`, buying power `303,018.54 USD`, long market value `68,543.22 USD`, watchlists `0`였다. 별도 after-hours order budget은 `0/2`로 열려 있었지만 freshest shortlisted quote `QQQ 722.00/722.21`도 약 `15.98`분 stale이라 submit path에 진입하지 못했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-13-0611-after-hours-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-13-0451-hourly-autopilot]]
- Open/new: 없음. scheduler-owned `0451` stale cleanup과 core preflight 모두 open orders `0`을 반환했다.
- Filled: 이번 cycle 신규 체결 없음. same-day fill history로 `RGTI` sell 12주 `filled_avg_price=21.0108 USD`, `AVGO` sell 1주 `387.06 USD`, `PFE` sell 1주 `26.13 USD`가 계속 확인됐다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `0451` core preflight decision snapshot 기준 positions `33`건, open orders `0`건, `RGTI 37주`, `AVGO 4주`, `PFE 5주`였다.
- Recent reconciliation scope: scheduler-owned `0451` stale cleanup/core/research preflight를 source-of-record로 사용했다. live Alpaca readback 추가 호출은 필요하지 않았고, passing core preflight rows만으로 regular market open, account `ACTIVE`, cash `31,950.36 USD`, portfolio value `100,427.19 USD`, buying power `302,798.90 USD`, long market value `68,476.83 USD`, watchlists `0`, same-day fills 상태를 재확인했다. sell-first path는 `AVGO/RGTI` same-day duplicate sell discipline과 `SO` trim metric gap 때문에 막혔고, buy path는 `FCX/NEE` review backlog throttle, `WMT` spread fail, `SPY/QQQ` floor cap, `NOK` add-block 때문에 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-13-0451-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-13-0431-hourly-autopilot]]
- Open/new: 없음. scheduler-owned `0431` stale cleanup과 core preflight 모두 open orders `0`을 반환했다.
- Filled: 이번 cycle 신규 체결 없음. same-day fill history로 `RGTI` sell 12주 `filled_avg_price=21.0108 USD`, `AVGO` sell 1주 `387.06 USD`, `PFE` sell 1주 `26.13 USD`가 계속 확인됐다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `0431` core preflight decision snapshot 기준 positions `33`건, open orders `0`건, `RGTI 37주`, `AVGO 4주`, `PFE 5주`였다.
- Recent reconciliation scope: scheduler-owned `0431` stale cleanup/core/research preflight를 source-of-record로 사용했다. live Alpaca readback 추가 호출은 필요하지 않았고, passing core preflight rows만으로 regular market open, account `ACTIVE`, cash `31,950.36 USD`, portfolio value `100,495.30 USD`, buying power `302,882.66 USD`, long market value `68,544.94 USD`, watchlists `0`, same-day fills 상태를 재확인했다. sell-first path는 `AVGO/RGTI` same-day duplicate sell discipline과 `SO` trim metric gap 때문에 막혔고, buy path는 `FCX/WMT/NEE` review backlog throttle, `SPY/QQQ` floor cap, `NOK` add-block 때문에 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-13-0431-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-13-0411-hourly-autopilot]]
- Open/new: 없음. scheduler-owned `0411` stale cleanup과 core preflight 모두 open orders `0`을 반환했다.
- Filled: 이번 cycle 신규 체결 없음. same-day fill history로 `RGTI` sell 12주 `filled_avg_price=21.0108 USD`, `AVGO` sell 1주 `387.06 USD`, `PFE` sell 1주 `26.13 USD`가 계속 확인됐다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `0411` core preflight decision snapshot 기준 positions `33`건, open orders `0`건, `RGTI 37주`, `AVGO 4주`, `PFE 5주`였다.
- Recent reconciliation scope: scheduler-owned `0411` stale cleanup/core/research preflight를 source-of-record로 사용했다. live Alpaca readback 추가 호출은 필요하지 않았고, passing core preflight rows만으로 regular market open, account `ACTIVE`, cash `31,950.36 USD`, portfolio value `100,527.44 USD`, buying power `302,978.28 USD`, long market value `68,577.08 USD`, watchlists `0`, same-day fills 상태를 재확인했다. sell-first path는 `AVGO` spread `1.4745%` fail plus same-day sell discipline, `RGTI` same-day duplicate sell discipline, `SO` trim metric gap 때문에 막혔고, buy path는 `FCX/WMT/NEE` review backlog throttle, `SPY/QQQ` floor cap, `NOK` add-block 때문에 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-13-0411-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-13-0351-hourly-autopilot]]
- Open/new: 없음. scheduler-owned `0351` stale cleanup과 core preflight 모두 open orders `0`을 반환했다.
- Filled: 이번 cycle 신규 체결 없음. same-day fill history로 `RGTI` sell 12주 `filled_avg_price=21.0108 USD`, `AVGO` sell 1주 `387.06 USD`, `PFE` sell 1주 `26.13 USD`가 계속 확인됐다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `0351` core preflight decision snapshot 기준 positions `33`건, open orders `0`건, `RGTI 37주`, `AVGO 4주`, `PFE 5주`였다.
- Recent reconciliation scope: scheduler-owned `0351` stale cleanup/core/research preflight를 source-of-record로 사용했다. live Alpaca readback 추가 호출은 필요하지 않았고, passing core preflight rows만으로 regular market open, account `ACTIVE`, cash `31,950.36 USD`, portfolio value `100,590.03 USD`, buying power `303,142.28 USD`, long market value `68,639.67 USD`, watchlists `0`, same-day fills 상태를 재확인했다. sell-first path는 `AVGO/RGTI` same-day duplicate sell discipline과 `SO` trim metric gap 때문에 막혔고, buy path는 `FCX/WMT/NEE` review backlog throttle, `SPY/QQQ` floor cap, `NOK` add-block 때문에 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-13-0351-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-13-0331-hourly-autopilot]]
- Open/new: 없음. scheduler-owned `0331` stale cleanup과 core preflight 모두 open orders `0`을 반환했다.
- Filled: 이번 cycle 신규 체결 없음. same-day fill history로 `RGTI` sell 20주 weighted avg `20.6845 USD`, `AVGO` sell 2주 weighted avg `383.745 USD`, `PFE` sell 1주 `26.13 USD`가 계속 확인됐다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `0331` core preflight decision snapshot 기준 positions `33`건, open orders `0`건, `RGTI 37주`, `AVGO 4주`, `PFE 5주`였다.
- Recent reconciliation scope: scheduler-owned `0331` stale cleanup/core/research preflight를 source-of-record로 사용했다. live Alpaca readback 추가 호출은 필요하지 않았고, passing core preflight rows만으로 regular market open, account `ACTIVE`, cash `31,950.36 USD`, portfolio value `100599.79 USD`, buying power `303130.21 USD`, long market value `68649.43 USD`, watchlists `0`, same-day fills 상태를 재확인했다. sell-first path는 `AVGO/RGTI` same-day duplicate sell discipline과 `SO` trim metric gap 때문에 막혔고, buy path는 `FCX` spread `5.6607%` fail과 `WMT/NEE` review backlog throttle, `SPY/QQQ` floor cap, `NOK` add-block 때문에 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-13-0331-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-13-0311-hourly-autopilot]]
- Open/new: 없음. scheduler-owned `0311` stale cleanup과 core preflight 모두 open orders `0`을 반환했다.
- Filled: 이번 cycle 신규 체결 없음. same-day fill history로 `RGTI` sell 12주 `filled_avg_price=21.010833 USD`, `AVGO` sell 1주 `387.06 USD`, `PFE` sell 1주 `26.13 USD`가 계속 확인됐다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `0311` core preflight decision snapshot 기준 positions `33`건, open orders `0`건, `RGTI 37주`, `AVGO 4주`, `PFE 5주`였다.
- Recent reconciliation scope: scheduler-owned `0311` stale cleanup/core/research preflight를 source-of-record로 사용했다. live Alpaca readback 추가 호출은 필요하지 않았고, passing core preflight rows만으로 regular market open, account `ACTIVE`, cash `31,950.36 USD`, portfolio value `100,664.28 USD`, buying power `303,292.22 USD`, long market value `68,713.92 USD`, watchlists `0`, same-day fills 상태를 재확인했다. buy path는 `pending_1d_count=14` review backlog throttle이 그대로 차단했고, sell-first path도 `AVGO` spread fail plus same-day sell discipline, `RGTI` same-day duplicate sell discipline, `SO` trim metric gap 때문에 executable order가 남지 않아 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-13-0311-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-13-0251-hourly-autopilot]]
- Open/new: 없음. scheduler-owned `0251` stale cleanup과 core preflight 모두 open orders `0`을 반환했다.
- Filled: 이번 cycle 신규 체결 없음. same-day fill history로 `RGTI` sell 12주 `filled_avg_price=21.010833 USD`, `AVGO` sell 1주 `387.06 USD`, `PFE` sell 1주 `26.13 USD`가 계속 확인됐다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `0251` core preflight decision snapshot 기준 positions `33`건, open orders `0`건, `RGTI 37주`, `AVGO 4주`, `PFE 5주`였다.
- Recent reconciliation scope: scheduler-owned `0251` stale cleanup/core/research preflight를 source-of-record로 사용했다. live Alpaca readback 추가 호출은 필요하지 않았고, passing core preflight rows만으로 regular market open, account `ACTIVE`, cash `31,950.36 USD`, portfolio value `100,740.51 USD`, buying power `303,521.18 USD`, long market value `68,790.15 USD`, watchlists `0`, same-day fills 상태를 재확인했다. buy path는 `pending_1d_count=14` review backlog throttle이 그대로 차단했고, sell-first path도 `AVGO` spread fail plus same-day sell discipline, `RGTI` same-day duplicate sell discipline, `SO` trim metric gap 때문에 executable order가 남지 않아 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-13-0251-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-13-0231-hourly-autopilot]]
- Open/new: 없음. scheduler-owned `0231` stale cleanup과 core preflight 모두 open orders `0`을 반환했다.
- Filled: 이번 cycle 신규 체결 없음. same-day fill history로 `RGTI` sell 12주 `filled_avg_price=21.010833 USD`, `AVGO` sell 1주 `387.06 USD`, `PFE` sell 1주 `26.13 USD`가 계속 확인됐다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `0231` core preflight decision snapshot 기준 positions `33`건, open orders `0`건, `RGTI 37주`, `AVGO 4주`, `PFE 5주`였다.
- Recent reconciliation scope: scheduler-owned `0231` stale cleanup/core/research preflight를 source-of-record로 사용했다. live Alpaca readback 추가 호출은 필요하지 않았고, passing core preflight rows만으로 regular market open, account `ACTIVE`, cash `31,950.36 USD`, portfolio value `100,693.91 USD`, buying power `303,427.51 USD`, long market value `68,743.55 USD`, watchlists `0`, same-day fills 상태를 재확인했다. buy path는 `pending_1d_count=14` review backlog throttle이 그대로 차단했고, sell-first path도 `AVGO` spread fail plus same-day sell discipline, `RGTI` same-day duplicate sell discipline, `SO` trim metric gap 때문에 executable order가 남지 않아 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-13-0231-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-13-0211-hourly-autopilot]]
- Open/new: 없음. scheduler-owned `0211` stale cleanup과 core preflight 모두 open orders `0`을 반환했다.
- Filled: 이번 cycle 신규 체결 없음. same-day fill history로 `RGTI` sell 12주 `filled_avg_price=21.010833 USD`, `AVGO` sell 1주 `387.06 USD`, `PFE` sell 1주 `26.13 USD`가 계속 확인됐다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `0211` core preflight decision snapshot 기준 positions `33`건, open orders `0`건, `RGTI 37주`, `AVGO 4주`, `PFE 5주`였다.
- Recent reconciliation scope: scheduler-owned `0211` stale cleanup/core/research preflight를 source-of-record로 사용했다. live Alpaca readback 추가 호출은 필요하지 않았고, passing core preflight rows만으로 regular market open, account `ACTIVE`, cash `31,950.36 USD`, portfolio value `100,645.26 USD`, buying power `303,385.17 USD`, long market value `68,694.90 USD`, watchlists `0`, same-day fills 상태를 재확인했다. buy path는 `pending_1d_count=14` review backlog throttle이 그대로 차단했고, sell-first path도 `AVGO` spread fail plus same-day sell discipline, `RGTI` same-day duplicate sell discipline, `SO` trim metric gap 때문에 executable order가 남지 않아 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-13-0211-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-13-0151-hourly-autopilot]]
- Open/new: 없음. scheduler-owned `0151` stale cleanup과 core preflight 모두 open orders `0`을 반환했다.
- Filled: 이번 cycle 신규 체결 없음. same-day fill history로 `RGTI` sell 12주 `filled_avg_price=21.010833 USD`, `AVGO` sell 1주 `387.06 USD`, `PFE` sell 1주 `26.13 USD`가 계속 확인됐다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `0151` core preflight decision snapshot 기준 positions `33`건, open orders `0`건, `RGTI 37주`, `AVGO 4주`, `PFE 5주`였다.
- Recent reconciliation scope: scheduler-owned `0151` stale cleanup/core/research preflight를 source-of-record로 사용했다. live Alpaca readback 추가 호출은 필요하지 않았고, passing core preflight rows만으로 regular market open, account `ACTIVE`, cash `31,950.36 USD`, portfolio value `100,543.37 USD`, buying power `303,186.12 USD`, long market value `68,593.01 USD`, watchlists `0`, same-day fills 상태를 재확인했다. buy path는 `pending_1d_count=14` review backlog throttle이 그대로 차단했고, sell-first path도 `AVGO/RGTI` same-day duplicate sell discipline과 `SO` trim metric gap 때문에 executable order가 남지 않아 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-13-0151-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-13-0131-hourly-autopilot]]
- Open/new: 없음. scheduler-owned `0131` stale cleanup과 core preflight 모두 open orders `0`을 반환했다.
- Filled: 이번 cycle 신규 체결 없음. same-day fill history로 `RGTI` sell 12주 `filled_avg_price=21.010833 USD`, `AVGO` sell 1주 `387.06 USD`, `PFE` sell 1주 `26.13 USD`가 계속 확인됐다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `0131` core preflight decision snapshot 기준 positions `33`건, open orders `0`건, `RGTI 37주`, `AVGO 4주`, `PFE 5주`였다.
- Recent reconciliation scope: scheduler-owned `0131` stale cleanup/core/research preflight를 source-of-record로 사용했다. live Alpaca readback 추가 호출은 필요하지 않았고, passing core preflight rows만으로 regular market open, account `ACTIVE`, cash `31,950.36 USD`, portfolio value `100,470.77 USD`, buying power `302,999.82 USD`, long market value `68,520.41 USD`, watchlists `0`, same-day fills 상태를 재확인했다. buy path는 `pending_1d_count=14` review backlog throttle이 그대로 차단했고, sell-first path도 `AVGO` spread fail, `RGTI` same-day duplicate sell discipline, `SO` trim metric gap 때문에 executable order가 남지 않아 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-13-0131-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-13-0111-hourly-autopilot]]
- Open/new: 없음. scheduler-owned `0111` stale cleanup과 core preflight 모두 open orders `0`을 반환했다.
- Filled: 이번 cycle 신규 체결 없음. same-day fill history로 `RGTI` sell 12주 `filled_avg_price=21.010833 USD`, `AVGO` sell 1주 `387.06 USD`, `PFE` sell 1주 `26.13 USD`가 계속 확인됐다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `0111` core preflight decision snapshot 기준 positions `33`건, open orders `0`건, `RGTI 37주`, `AVGO 4주`, `PFE 5주`였다.
- Recent reconciliation scope: scheduler-owned `0111` stale cleanup/core/research preflight를 source-of-record로 사용했다. live Alpaca readback 추가 호출은 필요하지 않았고, passing core preflight rows만으로 regular market open, account `ACTIVE`, cash `31,950.36 USD`, portfolio value `100,304.86 USD`, buying power `302,512.53 USD`, long market value `68,354.50 USD`, watchlists `0`, same-day fills 상태를 재확인했다. buy path는 `pending_1d_count=14` review backlog throttle이 그대로 차단했고, sell-first path도 `AVGO` spread fail, `RGTI` same-day duplicate sell discipline, `SO` trim metric gap 때문에 executable order가 남지 않아 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-13-0111-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-13-0051-hourly-autopilot]]
- Open/new: 없음. scheduler-owned `0051` stale cleanup과 core preflight 모두 open orders `0`을 반환했다.
- Filled: 이번 cycle 신규 체결 없음. same-day fill history로 `RGTI` sell 12주 `filled_avg_price=21.010833 USD`, `AVGO` sell 1주 `387.06 USD`, `PFE` sell 1주 `26.13 USD`가 계속 확인됐다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `0051` core preflight decision snapshot 기준 positions `33`건, open orders `0`건, `RGTI 37주`, `AVGO 4주`, `PFE 5주`였다.
- Recent reconciliation scope: scheduler-owned `0051` stale cleanup/core/research preflight를 source-of-record로 사용했다. live Alpaca readback 추가 호출은 필요하지 않았고, passing core preflight rows만으로 regular market open, account `ACTIVE`, cash `31,950.36 USD`, portfolio value `100,325.65 USD`, buying power `302,542.71 USD`, long market value `68,375.29 USD`, watchlists `0`, same-day fills 상태를 재확인했다. review backlog throttle이 `pending_1d_count=14`로 신규 buy를 차단했고, sell-first path도 `AVGO/RGTI` same-day duplicate sell discipline과 `SO` trim metric gap 때문에 executable order가 남지 않아 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-13-0051-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-13-0031-hourly-autopilot]]
- Open/new: 없음. scheduler-owned `0031` stale cleanup과 core preflight 모두 open orders `0`을 반환했다.
- Filled: 이번 cycle 신규 체결 없음. same-day fill history로 `RGTI` sell 12주 `filled_avg_price=21.010833 USD`, `AVGO` sell 1주 `387.06 USD`, `PFE` sell 1주 `26.13 USD`가 계속 확인됐다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `0031` core preflight decision snapshot 기준 positions `33`건, open orders `0`건, `RGTI 37주`, `AVGO 4주`, `PFE 5주`였다.
- Recent reconciliation scope: scheduler-owned `0031` stale cleanup/core/research preflight를 source-of-record로 사용했다. live Alpaca readback 추가 호출은 필요하지 않았고, passing core preflight rows만으로 regular market open, account `ACTIVE`, cash `31,950.36 USD`, portfolio value `100,912.91 USD`, buying power `303,956.29 USD`, long market value `68,962.55 USD`, watchlists `0`, same-day fills 상태를 재확인했다. review backlog throttle이 `pending_1d_count=14`로 신규 buy를 차단했고, sell-first path도 `AVGO` spread fail, `RGTI` same-day duplicate sell discipline, `SO` spread fail plus metric gap으로 executable order가 남지 않아 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-13-0031-hourly-autopilot-post-trade.json`

- Run: [[2026-06-12-2351-hourly-autopilot]]
- Open/new: 없음. scheduler-owned `2351` stale cleanup과 core preflight 모두 open orders `0`을 반환했다.
- Filled: 이번 cycle 신규 체결 없음. same-day fill history로 `RGTI` sell 12주 `filled_avg_price=21.010833 USD`, `AVGO` sell 1주 `387.06 USD`, `PFE` sell 1주 `26.13 USD`가 계속 확인됐다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `2351` core preflight decision snapshot 기준 positions `33`건, open orders `0`건, `RGTI 37주`, `AVGO 4주`, `PFE 5주`였다.
- Recent reconciliation scope: scheduler-owned `2351` stale cleanup/core/research preflight를 source-of-record로 사용했다. live Alpaca readback 추가 호출은 필요하지 않았고, passing core preflight rows만으로 regular market open, account `ACTIVE`, cash `31,950.36 USD`, portfolio value `100,202.02 USD`, buying power `302,247.54 USD`, long market value `68,251.66 USD`, watchlists `0`, same-day fills 상태를 재확인했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-2351-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-12-2331-hourly-autopilot]]
- Open/new: 없음. scheduler-owned `2331` stale cleanup과 core preflight 모두 open orders `0`을 반환했다.
- Filled: 이번 cycle 신규 체결 없음. same-day fill history로 `RGTI` sell 12주 `filled_avg_price=21.010833 USD`, `AVGO` sell 1주 `387.06 USD`, `PFE` sell 1주 `26.13 USD`가 계속 확인됐다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `2331` core preflight decision snapshot 기준 positions `33`건, open orders `0`건, `RGTI 37주`, `AVGO 4주`, `PFE 5주`였다.
- Recent reconciliation scope: scheduler-owned `2331` stale cleanup/core/research preflight를 source-of-record로 사용했다. live Alpaca readback 추가 호출은 필요하지 않았고, passing core preflight rows만으로 regular market open, account `ACTIVE`, cash `31,950.36 USD`, portfolio value `100,503.29 USD`, buying power `303,028.86 USD`, long market value `68,552.93 USD`, watchlists `0`, same-day fills 상태를 재확인했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-2331-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-12-2311-hourly-autopilot]]
- Open/new: 없음. `2231` cycle의 `RGTI` sell open order는 더 이상 남아 있지 않다.
- Filled: prior `RGTI` sell 12주 `limit 21.01 USD`, `client_order_id=hourly-20260612-2231-sell-rgti`가 `filled_avg_price=21.010833 USD`, `filled_at=2026-06-12T14:10:47.740608Z`로 체결된 것을 이번 cycle에서 재확인했다. same-day earlier fills `AVGO` sell 1주 `387.06 USD`, `PFE` sell 1주 `26.13 USD`도 유지됐다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `2311` core preflight decision snapshot 기준 positions `33`건, open orders `0`건, `RGTI 37주`, `AVGO 4주`, `PFE 5주`였다. runtime reconciliation 기준도 positions `33`, open orders `0`이 유지됐다.
- Recent reconciliation scope: scheduler-owned `2311` stale cleanup/core/research preflight를 source-of-record로 사용했고, runtime Alpaca MCP `get_orders(status=all, symbols=RGTI, after=2026-06-12T13:30:00Z)`, `get_account_info`, `get_all_positions` readback을 추가해 prior `RGTI` trim fill과 현재 계좌 상태를 재확인했다. runtime account 기준 portfolio value `100,469.09 USD`, cash `31,950.36 USD`, buying power `302,893.71 USD`, long market value `68,518.73 USD`, watchlists `0`이었다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-2311-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-12-2251-hourly-autopilot]]
- Open/new: 기존 `RGTI` sell 12주 limit `21.01 USD`, `client_order_id=hourly-20260612-2231-sell-rgti`, `status=new`가 유지됐다.
- Filled: 이번 cycle 신규 체결 없음. same-day earlier fills는 `AVGO` sell 1주 `387.06 USD`, `PFE` sell 1주 `26.13 USD`다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `2251` core preflight current snapshot 기준 positions `33`건, open orders `1`건, `RGTI 49주`와 `qty_available=37`, `AVGO 4주`, `PFE 5주`였다.
- Recent reconciliation scope: scheduler-owned `2251` stale cleanup/core/research preflight를 source-of-record로 사용했다. stale cleanup은 `RGTI` open sell age 약 `9.9분`이라 stale candidate 없이 pass했고, core preflight는 regular market open, account `ACTIVE`, portfolio value `99,943.63 USD`, cash `31,698.23 USD`, buying power `301,286.79 USD`, watchlists `0`를 재확인했다. 이번 cycle은 신규 submit 없이 exact gate blockers만 기록했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-2251-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-12-2231-hourly-autopilot]]
- Open/new: `RGTI` sell 12주 limit `21.01 USD`, `client_order_id=hourly-20260612-2231-sell-rgti`, `status=new`.
- Filled: submit 직후 신규 fill 없음. `filled_qty=0`, `filled_avg_price=null`.
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `2231` core preflight pre-submit snapshot 기준 positions `33`건, `RGTI 49주`, open orders `0`건이었다. submit 후 nested Codex readback은 order-level로만 가능했고 same client id readback에서 open order가 확인됐다.
- Recent reconciliation scope: scheduler-owned `2231` stale cleanup/core/research preflight를 source-of-record로 사용했고, submit 직후 `get_order_by_client_id`와 `get_orders(status=all, symbols=RGTI, after=2026-06-12T13:30:00Z)` readback으로 `order_id=1f49ece2-83b5-4136-bf38-e3794c1184fb`, `submitted_at=2026-06-12T13:41:09.3025829Z`, `status=new`, `expires_at=2026-06-12T20:00:00Z`를 재확인했다. account/positions refresh는 다음 scheduler core preflight 또는 후속 reconciliation cycle에서 확정한다.
- Orders submitted/replaced/cancelled/closed by this workflow: 1 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-2231-hourly-autopilot-post-trade.json`

_Last updated: 2026-06-12 21:53 KST_

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-12-2151-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음. same-session earlier fills `PFE`, `AVGO`는 유지됐고 두 주문 모두 exact filled readback을 다시 확인했다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime `get_all_positions` 기준 positions `33`건 유지, `AVGO 4주`, `PFE 5주`, open orders `0`건이다.
- Recent reconciliation scope: scheduler-owned `2151` core/research preflight를 source-of-record로 사용했다. `2151` Alpaca core preflight는 expected `market_closed`와 함께 passing account/positions/open-order/activity/watchlist/asset/quote/trade rows를 남겼고, runtime Alpaca MCP `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-11T20:00:00Z)/get_watchlists` cross-check는 regular market closed, account `ACTIVE`, cash `31,698.23 USD`, portfolio value `99,754.39 USD`, long market value `68,056.16 USD`, watchlists `0`, same-session after-hours fills `2`를 재확인했다. earlier fills `PFE`, `AVGO`가 여전히 `2/2`라 separate session budget이 계속 닫혀 있었으므로 이번 `2151` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-2151-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-12-2131-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음. same-session earlier fills `PFE`, `AVGO`는 유지됐고 두 주문 모두 exact filled readback을 다시 확인했다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime `get_all_positions` 기준 positions `33`건 유지, `AVGO 4주`, `PFE 5주`, open orders `0`건이다.
- Recent reconciliation scope: scheduler-owned `2131` core/research preflight를 source-of-record로 사용했다. `2131` Alpaca core preflight는 expected `market_closed`와 함께 passing account/positions/open-order/activity/watchlist/asset/quote/trade rows를 남겼고, runtime Alpaca MCP `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-11T20:00:00Z)/get_watchlists/get_order_by_client_id` cross-check는 regular market closed, account `ACTIVE`, cash `31,698.23 USD`, portfolio value `99,848.91 USD`, long market value `68,150.68 USD`, watchlists `0`, same-session after-hours fills `2`를 재확인했다. earlier fills `PFE`, `AVGO`가 여전히 `2/2`라 separate session budget이 계속 닫혀 있었으므로 이번 `2131` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-2131-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-12-2111-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음. same-session earlier fills `PFE`, `AVGO`는 유지됐고 두 주문 모두 exact filled readback을 다시 확인했다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime `get_all_positions` 기준 positions `33`건 유지, `AVGO 4주`, `PFE 5주`, open orders `0`건이다.
- Recent reconciliation scope: scheduler-owned `2111` core/research preflight를 source-of-record로 사용했다. `2111` Alpaca core preflight는 expected `market_closed`와 함께 passing account/positions/open-order/activity/watchlist/asset/quote/trade rows를 남겼고, runtime Alpaca MCP `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-11T20:00:00Z)/get_watchlists/get_order_by_client_id` cross-check는 regular market closed, account `ACTIVE`, cash `31,698.23 USD`, portfolio value `100,077.64 USD`, long market value `68,379.41 USD`, watchlists `0`, same-session after-hours fills `2`를 재확인했다. earlier fills `PFE`, `AVGO`가 여전히 `2/2`라 separate session budget이 계속 닫혀 있었으므로 이번 `2111` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-2111-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-12-2051-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음. same-session earlier fills `PFE`, `AVGO`는 유지됐고 두 주문 모두 exact filled readback을 다시 확인했다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime `get_all_positions` 기준 positions `33`건 유지, `AVGO 4주`, `PFE 5주`, open orders `0`건이다.
- Recent reconciliation scope: scheduler-owned `2051` core/research preflight를 source-of-record로 사용했다. `2051` Alpaca core preflight는 expected `market_closed`와 함께 passing account/positions/open-order/activity/watchlist/asset/quote/trade rows를 남겼고, runtime Alpaca MCP `get_clock/get_account_info/get_all_positions/get_watchlists/get_order_by_client_id` cross-check는 regular market closed, account `ACTIVE`, cash `31,698.23 USD`, portfolio value `100,175.37 USD`, long market value `68,477.14 USD`, watchlists `0`, same-session after-hours fills `2`를 재확인했다. earlier fills `PFE`, `AVGO`가 여전히 `2/2`라 separate session budget이 계속 닫혀 있었으므로 이번 `2051` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-2051-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-12-2031-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음. same-session earlier fills `PFE`, `AVGO`는 유지됐고 두 주문 모두 exact filled readback을 다시 확인했다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime `get_all_positions` 기준 positions `33`건 유지, `AVGO 4주`, `PFE 5주`, open orders `0`건이다.
- Recent reconciliation scope: scheduler-owned `2031` core/research preflight를 source-of-record로 사용했다. `2031` Alpaca core preflight는 expected `market_closed`와 함께 passing account/positions/open-order/activity/watchlist/asset/quote/trade rows를 남겼고, runtime Alpaca MCP `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-11T20:00:00Z)/get_watchlists/get_order_by_client_id` cross-check는 regular market closed, account `ACTIVE`, cash `31,698.23 USD`, portfolio value `100,196.76 USD`, long market value `68,498.53 USD`, watchlists `0`, same-session after-hours fills `2`를 재확인했다. earlier fills `PFE`, `AVGO`가 여전히 `2/2`라 separate session budget이 계속 닫혀 있었으므로 이번 `2031` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-2031-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-12-2011-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음. same-session earlier fills `PFE`, `AVGO`는 유지됐고 두 주문 모두 exact filled readback을 다시 확인했다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime `get_all_positions` 기준 positions `33`건 유지, `AVGO 4주`, `PFE 5주`, open orders `0`건이다.
- Recent reconciliation scope: scheduler-owned `2011` core/research preflight를 source-of-record로 사용했다. `2011` Alpaca core preflight는 expected `market_closed`와 함께 passing account/positions/open-order/activity/watchlist/asset/quote/trade rows를 남겼고, runtime Alpaca MCP `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-11T20:00:00Z)/get_watchlists/get_order_by_client_id` cross-check는 regular market closed, account `ACTIVE`, cash `31,698.23 USD`, portfolio value `100,122.79 USD`, long market value `68,424.56 USD`, watchlists `0`, same-session after-hours fills `2`를 재확인했다. earlier fills `PFE`, `AVGO`가 여전히 `2/2`라 separate session budget이 계속 닫혀 있었으므로 이번 `2011` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-2011-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-12-1951-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음. same-session earlier fills `PFE`, `AVGO`는 유지됐고 두 주문 모두 exact filled readback을 다시 확인했다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime `get_all_positions` 기준 positions `33`건 유지, `AVGO 4주`, `PFE 5주`, open orders `0`건이다.
- Recent reconciliation scope: scheduler-owned `1951` core/research preflight를 source-of-record로 사용했다. `1951` Alpaca core preflight는 expected `market_closed`와 함께 passing account/positions/open-order/activity/watchlist/asset/quote/trade rows를 남겼고, runtime Alpaca MCP `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-11T20:00:00Z)/get_watchlists` cross-check는 regular market closed, account `ACTIVE`, cash `31,698.23 USD`, portfolio value `100,006.94 USD`, long market value `68,308.71 USD`, watchlists `0`, same-session after-hours fills `2`를 재확인했다. earlier fills `PFE`, `AVGO`가 여전히 `2/2`라 separate session budget이 계속 닫혀 있었으므로 이번 `1951` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-1951-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-12-1931-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음. same-session earlier fills `PFE`, `AVGO`는 유지됐고 두 주문 모두 exact filled readback을 다시 확인했다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime `get_all_positions` 기준 positions `33`건 유지, `AVGO 4주`, `PFE 5주`, open orders `0`건이다.
- Recent reconciliation scope: scheduler-owned `1931` core/research preflight를 source-of-record로 사용했다. `1931` Alpaca core preflight는 expected `market_closed`와 함께 passing account/positions/open-order/activity/watchlist/asset/quote/trade rows를 남겼고, runtime Alpaca MCP `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-11T20:00:00Z)/get_watchlists` cross-check는 regular market closed, account `ACTIVE`, cash `31,698.23 USD`, portfolio value `100,027.75 USD`, long market value `68,329.52 USD`, watchlists `0`, same-session after-hours fills `2`를 재확인했다. earlier fills `PFE`, `AVGO`가 여전히 `2/2`라 separate session budget이 계속 닫혀 있었으므로 이번 `1931` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-1931-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-12-1911-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음. same-session earlier fills `PFE`, `AVGO`는 유지됐고 두 주문 모두 exact filled readback을 다시 확인했다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime `get_all_positions` 기준 positions `33`건 유지, `AVGO 4주`, `PFE 5주`, open orders `0`건이다.
- Recent reconciliation scope: scheduler-owned `1911` core/research preflight를 source-of-record로 사용했다. `1911` Alpaca core preflight는 expected `market_closed`와 함께 passing account/positions/open-order/activity/watchlist/asset/quote/snapshot/trade rows를 남겼고, runtime Alpaca MCP `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-11T20:00:00Z)/get_watchlists/get_order_by_client_id` cross-check는 regular market closed, account `ACTIVE`, cash `31,698.23 USD`, portfolio value `100,238.73 USD`, long market value `68,540.50 USD`, watchlists `0`, same-session after-hours fills `2`를 재확인했다. earlier fills `PFE`, `AVGO`가 여전히 `2/2`라 separate session budget이 계속 닫혀 있었으므로 이번 `1911` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-1911-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-12-1851-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음. same-session earlier fills `PFE`, `AVGO`는 유지됐고 두 주문 모두 exact filled readback을 다시 확인했다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime `get_all_positions` 기준 positions `33`건 유지, `AVGO 4주`, `PFE 5주`, open orders `0`건이다.
- Recent reconciliation scope: scheduler-owned `1851` core/research preflight를 source-of-record로 사용했다. `1851` Alpaca core preflight는 expected `market_closed`와 함께 passing account/positions/open-order/activity/watchlist/asset/quote/snapshot/trade rows를 남겼고, runtime Alpaca MCP `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-11T20:00:00Z)/get_watchlists/get_order_by_client_id` cross-check는 regular market closed, account `ACTIVE`, cash `31,698.23 USD`, portfolio value `100,151.61 USD`, long market value `68,453.38 USD`, watchlists `0`, same-session after-hours fills `2`를 재확인했다. earlier fills `PFE`, `AVGO`가 여전히 `2/2`라 separate session budget이 계속 닫혀 있었으므로 이번 `1851` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-1851-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-12-1831-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음. same-session earlier fills `PFE`, `AVGO`는 유지됐고 두 주문 모두 exact filled readback을 다시 확인했다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime `get_all_positions` 기준 positions `33`건 유지, `AVGO 4주`, `PFE 5주`, open orders `0`건이다.
- Recent reconciliation scope: scheduler-owned `1831` core/research preflight를 source-of-record로 사용했다. `1831` Alpaca core preflight는 expected `market_closed`와 함께 passing account/positions/open-order/activity/watchlist/asset/quote/snapshot/trade rows를 남겼고, runtime Alpaca MCP `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-11T20:00:00Z)/get_watchlists/get_order_by_client_id` cross-check는 regular market closed, account `ACTIVE`, cash `31,698.23 USD`, portfolio value `100,242.45 USD`, long market value `68,544.22 USD`, watchlists `0`, same-session after-hours fills `2`를 재확인했다. earlier fills `PFE`, `AVGO`가 여전히 `2/2`라 separate session budget이 계속 닫혀 있었으므로 이번 `1831` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-1831-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-12-1811-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음. same-session earlier fills `PFE`, `AVGO`는 유지됐고 두 주문 모두 exact filled readback을 다시 확인했다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime `get_all_positions` 기준 positions `33`건 유지, `AVGO 4주`, `PFE 5주`, open orders `0`건이다.
- Recent reconciliation scope: scheduler-owned `1811` core/research preflight를 source-of-record로 사용했다. `1811` Alpaca core preflight는 expected `market_closed`와 함께 passing account/positions/open-order/activity/watchlist/asset/quote/snapshot/trade rows를 남겼고, runtime Alpaca MCP `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-11T20:00:00Z)/get_watchlists/get_order_by_client_id` cross-check는 regular market closed, account `ACTIVE`, cash `31,698.23 USD`, portfolio value `99,996.71 USD`, long market value `68,298.48 USD`, watchlists `0`, same-session after-hours fills `2`를 재확인했다. earlier fills `PFE`, `AVGO`가 여전히 `2/2`라 separate session budget이 계속 닫혀 있었으므로 이번 `1811` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-1811-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-12-1751-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음. same-session earlier fills `PFE`, `AVGO`는 유지됐고 두 주문 모두 exact filled readback을 다시 확인했다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime `get_all_positions` 기준 positions `33`건 유지, `AVGO 4주`, `PFE 5주`, open orders `0`건이다.
- Recent reconciliation scope: scheduler-owned `1751` core/research preflight를 source-of-record로 사용했다. `1751` Alpaca core preflight는 expected `market_closed`와 함께 passing account/positions/open-order/activity/watchlist/asset/quote/trade rows를 남겼고, runtime Alpaca MCP `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-11T20:00:00Z)/get_watchlists/get_order_by_client_id` cross-check는 regular market closed, account `ACTIVE`, cash `31,698.23 USD`, portfolio value `99,759.28 USD`, long market value `68,061.05 USD`, watchlists `0`, same-session after-hours fills `2`를 재확인했다. earlier fills `PFE`, `AVGO`가 여전히 `2/2`라 separate session budget이 계속 닫혀 있었으므로 이번 `1751` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-1751-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-12-1731-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음. same-session earlier fills `PFE`, `AVGO`는 유지됐고 두 주문 모두 exact filled readback을 다시 확인했다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime `get_all_positions` 기준 positions `33`건 유지, `AVGO 4주`, `PFE 5주`, open orders `0`건이다.
- Recent reconciliation scope: scheduler-owned `1731` core/research preflight를 source-of-record로 사용했다. `1731` Alpaca core preflight는 expected `market_closed`와 함께 passing account/positions/open-order/activity/watchlist/asset/quote/snapshot/trade rows를 남겼고, runtime Alpaca MCP `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-11T20:00:00Z)/get_order_by_client_id` cross-check는 regular market closed, account `ACTIVE`, cash `31,698.23 USD`, portfolio value `99,861.20 USD`, long market value `68,162.97 USD`, same-session after-hours fills `2`를 재확인했다. watchlists `0`은 scheduler-owned preflight `get_watchlists` pass row를 재사용했다. earlier fills `PFE`, `AVGO`가 여전히 `2/2`라 separate session budget이 계속 닫혀 있었으므로 이번 `1731` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-1731-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-12-1711-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음. same-session earlier fills `PFE`, `AVGO`는 유지됐고 두 주문 모두 exact filled readback을 다시 확인했다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime `get_all_positions` 기준 positions `33`건 유지, `AVGO 4주`, `PFE 5주`, open orders `0`건이다.
- Recent reconciliation scope: scheduler-owned `1711` core/research preflight를 source-of-record로 사용했다. `1711` Alpaca core preflight는 expected `market_closed`와 함께 passing account/positions/open-order/activity/watchlist/asset/quote/snapshot/trade rows를 남겼고, runtime Alpaca MCP `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-11T20:00:00Z)/get_watchlists/get_order_by_client_id` cross-check는 regular market closed, account `ACTIVE`, cash `31,698.25 USD`, portfolio value `99,719.74 USD`, long market value `68,021.49 USD`, watchlists `0`, same-session after-hours fills `2`를 재확인했다. earlier fills `PFE`, `AVGO`가 여전히 `2/2`라 separate session budget이 계속 닫혀 있었으므로 이번 `1711` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-1711-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-12-1651-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음. same-session earlier fills `PFE`, `AVGO`는 유지됐고 두 주문 모두 exact filled readback을 다시 확인했다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime `get_all_positions` 기준 positions `33`건 유지, `AVGO 4주`, `PFE 5주`, open orders `0`건이다.
- Recent reconciliation scope: scheduler-owned `1651` core/research preflight를 source-of-record로 사용했다. `1651` Alpaca core preflight는 expected `market_closed`와 함께 passing account/positions/open-order/activity/watchlist/asset/quote/snapshot/trade rows를 남겼고, runtime Alpaca MCP `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-11T20:00:00Z)/get_watchlists/get_order_by_client_id` cross-check는 regular market closed, account `ACTIVE`, cash `31,698.25 USD`, portfolio value `99,445.98 USD`, long market value `67,747.73 USD`, watchlists `0`, same-session after-hours fills `2`를 재확인했다. earlier fills `PFE`, `AVGO`가 여전히 `2/2`라 separate session budget이 계속 닫혀 있었으므로 이번 `1651` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-1651-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-12-1631-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음. same-session earlier fills `PFE`, `AVGO`는 유지됐고 두 주문 모두 exact filled readback을 다시 확인했다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime `get_all_positions` 기준 positions `33`건 유지, `AVGO 4주`, `PFE 5주`, open orders `0`건이다.
- Recent reconciliation scope: scheduler-owned `1631` core/research preflight를 source-of-record로 사용했다. `1631` Alpaca core preflight는 expected `market_closed`와 함께 passing account/positions/open-order/activity/watchlist/asset/quote/snapshot/trade rows를 남겼고, runtime Alpaca MCP `get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-11T20:00:00Z)/get_watchlists/get_order_by_client_id` cross-check는 account `ACTIVE`, cash `31,698.25 USD`, portfolio value `99,265.24 USD`, long market value `67,566.99 USD`, watchlists `0`, same-session after-hours fills `2`를 재확인했다. earlier fills `PFE`, `AVGO`가 여전히 `2/2`라 separate session budget이 계속 닫혀 있었으므로 이번 `1631` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-1631-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-12-1611-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음. same-session earlier fills `PFE`, `AVGO`는 유지됐고 두 주문 모두 exact filled readback을 다시 확인했다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime `get_all_positions` 기준 positions `33`건 유지, `AVGO 4주`, `PFE 5주`, open orders `0`건이다.
- Recent reconciliation scope: scheduler-owned `1611` core/research preflight를 source-of-record로 사용했다. `1611` Alpaca core preflight는 expected `market_closed`와 함께 passing account/positions/open-order/activity/watchlist/asset/quote/snapshot/trade rows를 남겼고, runtime Alpaca MCP `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-11T20:00:00Z)/get_watchlists` cross-check는 regular market closed, account `ACTIVE`, cash `31,698.25 USD`, portfolio value `99,190.62 USD`, long market value `67,492.37 USD`, watchlists `0`, same-session after-hours fills `2`를 재확인했다. earlier fills `PFE`, `AVGO`가 여전히 `2/2`라 separate session budget이 계속 닫혀 있었으므로 이번 `1611` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-1611-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-12-1551-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음. same-session earlier fills `PFE`, `AVGO`는 유지됐고 두 주문 모두 exact filled readback을 다시 확인했다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime `get_all_positions` 기준 positions `33`건 유지, `AVGO 4주`, `PFE 5주`, open orders `0`건이다.
- Recent reconciliation scope: scheduler-owned `1551` core/research preflight를 source-of-record로 사용했다. `1551` Alpaca core preflight는 expected `market_closed`와 함께 passing account/positions/open-order/activity/watchlist/asset/quote/snapshot/trade rows를 남겼고, runtime Alpaca MCP `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-11T20:00:00Z)/get_account_activities(activity_types=FILL, after=2026-06-11T20:00:00Z)/get_watchlists` cross-check는 regular market closed, account `ACTIVE`, cash `31,698.25 USD`, portfolio value `99,425.71 USD`, long market value `67,727.46 USD`, watchlists `0`, same-session after-hours fills `2`를 재확인했다. earlier fills `PFE`, `AVGO`가 여전히 `2/2`라 separate session budget이 계속 닫혀 있었으므로 이번 `1551` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-1551-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-12-1531-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음. same-session earlier fills `PFE`, `AVGO`는 유지됐고 두 주문 모두 exact filled readback을 다시 확인했다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime `get_all_positions` 기준 positions `33`건 유지, `AVGO 4주`, `PFE 5주`, open orders `0`건이다.
- Recent reconciliation scope: scheduler-owned `1531` core/research preflight를 source-of-record로 사용했다. `1531` Alpaca core preflight는 expected `market_closed`와 함께 passing account/positions/open-order/activity/watchlist/asset/quote rows를 남겼고, runtime Alpaca MCP `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-11T20:00:00Z)/get_watchlists` cross-check는 regular market closed, account `ACTIVE`, cash `31,698.25 USD`, portfolio value `99,594.28 USD`, long market value `67,896.03 USD`, watchlists `0`, same-session after-hours fills `2`를 재확인했다. earlier fills `PFE`, `AVGO`가 여전히 `2/2`라 separate session budget이 계속 닫혀 있었으므로 이번 `1531` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-1531-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-12-1511-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음. same-session earlier fills `PFE`, `AVGO`는 유지됐고 두 주문 모두 exact filled readback을 다시 확인했다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime `get_all_positions` 기준 positions `33`건 유지, `AVGO 4주`, `PFE 5주`, open orders `0`건이다.
- Recent reconciliation scope: scheduler-owned `1511` core/research preflight를 우선 읽었다. 다만 `1511` Alpaca core preflight는 expected `market_closed` 외에 재사용 가능한 passing row를 남기지 않아, runtime Alpaca MCP `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-11T20:00:00Z)/get_watchlists` cross-check로 after-hours required rows를 보강했다. regular market closed, account `ACTIVE`, cash `31,698.25 USD`, portfolio value `99,677.55 USD`, long market value `67,979.30 USD`, watchlists `0`을 재확인했고 same-session after-hours fills는 여전히 `PFE` 1건과 `AVGO` 1건으로 `2/2`라 separate session budget이 계속 닫혀 있었으므로 이번 `1511` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-1511-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-12-1451-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음. same-session earlier fills `PFE`, `AVGO`는 유지됐고 두 주문 모두 exact filled readback을 재확인했다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime `get_all_positions` 기준 positions `33`건 유지, `AVGO 4주`, `PFE 5주`, open orders `0`건이다.
- Recent reconciliation scope: scheduler-owned `1451` core/research preflight를 source-of-record로 사용했다. runtime Alpaca MCP `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-11T20:00:00Z)/get_watchlists` cross-check 기준 regular market closed, account `ACTIVE`, cash `31,698.25 USD`, portfolio value `99,659.28 USD`, long market value `67,961.03 USD`, watchlists `0`이었다. same-session after-hours fills는 `PFE` 1건과 `AVGO` 1건으로 여전히 `2/2`라 separate session budget이 계속 닫혀 있었고, 이번 `1451` cycle은 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-1451-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-12-1431-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음. same-session earlier fills `PFE`, `AVGO`는 유지됐고 `AVGO` readback exact `filled_avg_price=387.06 USD`를 확인했다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime `get_all_positions` 기준 positions `33`건 유지, `AVGO 4주`, `PFE 5주`, open orders `0`건이다.
- Recent reconciliation scope: scheduler-owned `1431` core/research preflight를 source-of-record로 사용했다. runtime Alpaca MCP `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-11T20:00:00Z)/get_watchlists` cross-check 기준 regular market closed, account `ACTIVE`, cash `31,698.25 USD`, portfolio value `99,939.70 USD`, long market value `68,241.45 USD`, watchlists `0`이었다. same-session after-hours fills는 `PFE` 1건과 `AVGO` 1건으로 `2/2`가 되어 separate session budget이 닫혔고, 이번 `1431` cycle은 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-1431-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-12-1411-after-hours-autopilot]]
- Open/new: 없음
- Filled: `AVGO` 1주 trim. `client_order_id=ah-20260612-1411-sell-avgo-01`, `order_id=ecdd85cb-0b94-410c-b9f8-5e29f4a8ee2b`
- Cancelled: 없음
- Position count observed by Alpaca MCP: immediate post-trade `get_all_positions` 기준 positions `33`건을 유지했고 `AVGO`는 `5주 -> 4주`, `qty_available=4`로 감소했다.
- Recent reconciliation scope: scheduler-owned `1411` core/research preflight를 source-of-record로 사용했다. regular market은 closed, pre-submit account는 `ACTIVE`, cash `31,311.19 USD`, portfolio value `99,971.25 USD`, long market value `68,660.06 USD`, watchlists `0`이었다. submit는 planned `client_order_id`로 1회만 수행했고 exposed runtime surface에는 post-submit `get_order_by_client_id`/`get_orders` readback이 없어 exact `filled_avg_price`는 확인하지 못했지만, immediate Alpaca MCP `get_all_positions`에서 `AVGO 5 -> 4`가 확인돼 filled reconciliation으로 기록한다. same-session after-hours fills는 earlier `PFE` 1건과 이번 `AVGO` 1건으로 `2/2`가 됐다.
- Orders submitted/replaced/cancelled/closed by this workflow: 1 / 0 / 0 / 1.
- Source note: `wiki/trade-ledger/positions/2026-06-12-1411-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-12-1351-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `1351` core preflight 기준 `33` positions 유지, open orders `0`건이다. `PFE`는 `5주`, `qty_available=5`를 유지했고 same-session after-hours fill ledger는 earlier `1011` `PFE` trim 1건만 유지됐다.
- Recent reconciliation scope: scheduler-owned `1351` core/research preflight를 source-of-record로 사용했다. regular market은 closed, account `ACTIVE`, cash `31,311.19 USD`, portfolio value `100,023.24 USD`, long market value `68,712.05 USD`, watchlists `0`이었다. direct Alpaca MCP `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-11T20:00:00Z)/get_watchlists` cross-check도 regular market closed, account `ACTIVE`, positions `33`, open orders `0`, same-session after-hours fill `1`(`PFE`), watchlists `0`를 유지했다. separate session budget은 `1/2`가 남아 있었지만 submit-boundary IEX quote stack은 freshest `ADBE 20:55:03Z`, `RGTI 20:54:49Z`조차 약 `476`분 stale였고 `PFE/AVGO/RGTI/SO/ORCL`은 spread도 실패해 이번 `1351` cycle은 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-1351-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-12-1331-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `1331` core preflight 기준 `33` positions 유지, open orders `0`건이다. `PFE`는 `5주`, `qty_available=5`를 유지했고 same-session after-hours fill ledger는 earlier `1011` `PFE` trim 1건만 유지됐다.
- Recent reconciliation scope: scheduler-owned `1331` core/research preflight를 source-of-record로 사용했다. regular market은 closed, account `ACTIVE`, cash `31,311.19 USD`, portfolio value `99,990.23 USD`, long market value `68,679.04 USD`, watchlists `0`이었다. direct Alpaca MCP `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-11T20:00:00Z)/get_watchlists` cross-check도 regular market closed, account `ACTIVE`, positions `33`, open orders `0`, same-session after-hours fill `1`(`PFE`), watchlists `0`를 유지했다. separate session budget은 `1/2`가 남아 있었지만 submit-boundary IEX quote stack은 freshest `ADBE 20:55:03Z`, `RGTI 20:54:49Z`조차 약 `456`분 stale였고 `PFE/AVGO/RGTI/SO/ORCL`은 spread도 실패해 이번 `1331` cycle은 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-1331-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-12-1311-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `1311` core preflight 기준 `33` positions 유지, open orders `0`건이다. `PFE`는 `5주`, `qty_available=5`를 유지했고 same-session after-hours fill ledger는 earlier `1011` `PFE` trim 1건만 유지됐다.
- Recent reconciliation scope: scheduler-owned `1311` core/research preflight를 source-of-record로 사용했다. regular market은 closed, account `ACTIVE`, cash `31,311.19 USD`, portfolio value `99,909.68 USD`, long market value `68,598.49 USD`, watchlists `0`이었다. direct Alpaca MCP `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-11T20:00:00Z)/get_watchlists` cross-check도 regular market closed, account `ACTIVE`, positions `33`, open orders `0`, same-session after-hours fill `1`(`PFE`), watchlists `0`를 유지했다. separate session budget은 `1/2`가 남아 있었지만 submit-boundary IEX quote stack은 freshest `ADBE 20:55:03Z`, `RGTI 20:54:49Z`조차 약 `436`분 stale였고 `PFE/AVGO/RGTI/SO/ORCL`은 spread도 실패해 이번 `1311` cycle은 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-1311-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-12-1251-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `1251` core preflight 기준 `33` positions 유지, open orders `0`건이다. `PFE`는 `5주`, `qty_available=5`를 유지했고 same-session after-hours fill ledger는 earlier `1011` `PFE` trim 1건만 유지됐다.
- Recent reconciliation scope: scheduler-owned `1251` core/research preflight를 source-of-record로 사용했다. regular market은 closed, account `ACTIVE`, cash `31,311.19 USD`, portfolio value `99,937.55 USD`, long market value `68,626.36 USD`, watchlists `0`이었다. runtime Alpaca MCP `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_account_activities(activity_types=FILL, after=2026-06-11T20:00:00Z)/get_watchlists` cross-check도 regular market closed, account `ACTIVE`, positions `33`, open orders `0`, same-session after-hours fill `1`(`PFE`), watchlists `0`를 유지했다. separate session budget은 `1/2`가 남아 있었지만 submit-boundary IEX quote stack은 freshest `ADBE 20:55:03Z`, `RGTI 20:54:49Z`조차 약 `416`분 stale였고 `PFE/AVGO/RGTI/SO/ORCL`은 spread도 실패해 이번 `1251` cycle은 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-1251-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-12-1231-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `1231` core preflight 기준 `33` positions 유지, open orders `0`건이다. `PFE`는 `5주`, `qty_available=5`를 유지했고 same-session after-hours fill ledger는 earlier `1011` `PFE` trim 1건만 유지됐다.
- Recent reconciliation scope: scheduler-owned `1231` core/research preflight를 source-of-record로 사용했다. regular market은 closed, account `ACTIVE`, cash `31,311.19 USD`, portfolio value `99,969.36 USD`, long market value `68,658.17 USD`, watchlists `0`이었다. direct Alpaca MCP `get_clock/get_account_info` cross-check도 regular market closed와 account `ACTIVE`를 유지했고, same-session after-hours fill은 `PFE` 1건이라 separate session budget은 `1/2`가 남아 있었다. 다만 submit-boundary IEX quote stack은 freshest `ADBE 20:55:03Z`, `RGTI 20:54:49Z`조차 약 `396`분 stale였고 `PFE/AVGO/RGTI/SO/ORCL`은 spread도 실패해 이번 `1231` cycle은 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-1231-after-hours-autopilot-post-trade.json`

- Run: [[2026-06-12-1211-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `1211` core preflight 기준 `33` positions 유지, open orders `0`건이다. `PFE`는 `5주`, `qty_available=5`를 유지했고 same-session after-hours fill ledger는 earlier `1011` `PFE` trim 1건만 유지됐다.
- Recent reconciliation scope: scheduler-owned `1211` core/research preflight를 source-of-record로 사용했다. regular market은 closed, account `ACTIVE`, cash `31,311.19 USD`, portfolio value `100,025.68 USD`, long market value `68,714.49 USD`, watchlists `0`이었다. same-session after-hours fill은 `PFE` 1건이라 separate session budget은 `1/2`가 남아 있었지만, submit-boundary IEX quote stack은 freshest `ADBE 20:55:03Z`, `RGTI 20:54:49Z`조차 약 `376`분 stale였고 `PFE/AVGO/RGTI/SO/ORCL`은 spread도 실패해 이번 `1211` cycle은 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-1211-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-12-1151-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `1151` core preflight 기준 `33` positions 유지, open orders `0`건이다. `PFE`는 `5주`, `qty_available=5`를 유지했고 same-session after-hours fill ledger는 earlier `1011` `PFE` trim 1건만 유지됐다.
- Recent reconciliation scope: scheduler-owned `1151` core/research preflight를 source-of-record로 사용했다. regular market은 closed, account `ACTIVE`, cash `31,311.19 USD`, portfolio value `100,006.39 USD`, long market value `68,695.20 USD`, watchlists `0`이었다. same-session after-hours fill은 `PFE` 1건이라 separate session budget은 `1/2`가 남아 있었지만, submit-boundary IEX quote stack은 freshest `ADBE 20:55:03Z`, `RGTI 20:54:49Z`조차 약 `356`분 stale였고 `PFE/AVGO/RGTI/SO/ORCL`은 spread도 실패해 이번 `1151` cycle은 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-1151-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-12-1131-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `1131` core preflight 기준 `33` positions 유지, open orders `0`건이다. `PFE`는 `5주`, `qty_available=5`를 유지했고 same-session after-hours fill ledger는 earlier `1011` `PFE` trim 1건만 유지됐다.
- Recent reconciliation scope: scheduler-owned `1131` core/research preflight를 source-of-record로 사용했다. regular market은 closed, account `ACTIVE`, cash `31,311.19 USD`, portfolio value `99,897.29 USD`, long market value `68,586.10 USD`, watchlists `0`이었다. same-session after-hours fill은 `PFE` 1건이라 separate session budget은 `1/2`가 남아 있었지만, submit-boundary IEX quote stack은 freshest `ADBE 20:55:03Z`, `RGTI 20:54:49Z`조차 약 `336`분 stale였고 `PFE/AVGO/RGTI/SO/ORCL`은 spread도 실패해 이번 `1131` cycle은 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-1131-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-12-1111-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `1111` core preflight 기준 `33` positions 유지, open orders `0`건이다. `PFE`는 `5주`, `qty_available=5`를 유지했고 same-session after-hours fill ledger는 earlier `1011` `PFE` trim 1건만 유지됐다.
- Recent reconciliation scope: scheduler-owned `1111` core/research preflight를 source-of-record로 사용했다. regular market은 closed, account `ACTIVE`, cash `31,311.19 USD`, portfolio value `100,020.62 USD`, long market value `68,709.43 USD`, watchlists `0`이었다. same-session after-hours fill은 `PFE` 1건이라 separate session budget은 `1/2`가 남아 있었지만, submit-boundary IEX quote stack은 freshest `ADBE 20:55:03Z`, `RGTI 20:54:49Z`조차 약 `316`분 stale였고 `PFE/AVGO/RGTI/SO/ORCL`은 spread도 실패해 이번 `1111` cycle은 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-1111-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-12-1051-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `1051` core preflight 기준 `33` positions 유지, open orders `0`건이다. `PFE`는 `5주`, `qty_available=5`를 유지했고 same-session after-hours fill ledger는 earlier `1011` `PFE` trim 1건만 유지됐다.
- Recent reconciliation scope: scheduler-owned `1051` core/research preflight를 source-of-record로 사용했다. regular market은 closed, account `ACTIVE`, cash `31,311.19 USD`, portfolio value `99,916.37 USD`, long market value `68,605.18 USD`, watchlists `0`이었다. same-session after-hours fill은 `PFE` 1건이라 separate session budget은 `1/2`가 남아 있었지만, submit-boundary IEX quote stack은 freshest `ADBE 20:55:03Z`, `RGTI 20:54:49Z`조차 약 `296`분 stale였고 `PFE/AVGO/RGTI/SO/ORCL`은 spread도 실패해 이번 `1051` cycle은 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-1051-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-12-1031-after-hours-autopilot]]
- Open/new: 없음
- Filled: 이번 cycle 신규 체결 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `1031` core preflight 기준 `33` positions 유지, open orders `0`건이다. `PFE`는 `5주`, `qty_available=5`를 유지했고 earlier `1011` fill `ah-20260612-1011-sell-pfe-01`은 `get_order_by_client_id` 기준 여전히 `filled`였다.
- Recent reconciliation scope: scheduler-owned `1031` core/research preflight를 source-of-record로 사용했다. regular market은 closed, account `ACTIVE`, cash `31,311.19 USD`, portfolio value `99,821.57 USD`, long market value `68,510.38 USD`, watchlists `0`이었다. same-session after-hours fill은 `PFE` 1건이라 separate session budget은 `1/2`가 남아 있었지만, submit-boundary IEX quote stack은 freshest `ADBE 20:55:03Z`, `RGTI 20:54:49Z`조차 약 `276`분 stale였고 `PFE/AVGO/RGTI/SO/ORCL`은 spread도 실패해 이번 `1031` cycle은 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-1031-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-12-1011-after-hours-autopilot]]
- Open/new: 없음
- Filled: `PFE` 1주 sell @ `26.13 USD`
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime account/positions reconciliation 기준 `33` positions 유지, open orders `0`건이다. `PFE`는 `6주 -> 5주`, `qty_available=5`로 감소했고 `AVGO 5주`, `RGTI 49주`, `SO 5주`는 unchanged였다.
- Recent reconciliation scope: scheduler-owned `1011` core/research preflight를 source-of-record로 사용했고 runtime Alpaca MCP `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-11T20:00:00Z)/get_account_activities(activity_types=FILL, after=2026-06-11T20:00:00Z)/get_watchlists/get_stock_latest_quote(feed=iex)/get_stock_snapshot(feed=iex)/get_stock_latest_quote(feed=overnight)`로 same-session order budget과 submit-boundary quote freshness를 재확인했다. regular market은 closed, account `ACTIVE`, positions `33`, open orders `0`, watchlists `0`이었다. buy path는 `review_backlog_pending_1d_count=14`로 차단됐지만 sell-first 재평가에서 `PFE`가 repeated weak-review evidence와 overnight quote `26.12/26.16`, spread `0.1529%`를 충족해 1주 trim sell이 즉시 체결됐다. separate session budget은 `0/2 -> 1/2`가 됐다.
- Orders submitted/replaced/cancelled/closed by this workflow: 1 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-1011-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-12-0951-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned account + runtime positions reconciliation 기준 `33` positions 유지, open orders `0`건이다. `AVGO`는 `5주`, `qty_available=5`, `RGTI`는 `49주`, `qty_available=49`, `SO`는 `5주`, `qty_available=5`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `0951` core/research preflight를 source-of-record로 사용했고 runtime Alpaca MCP `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-11T20:00:00Z)/get_account_activities(activity_types=FILL, after=2026-06-11T20:00:00Z)/get_watchlists/get_stock_latest_quote(feed=iex)/get_stock_snapshot(feed=iex)`로 same-session order budget과 submit-boundary quote freshness를 재확인했다. regular market은 closed, account `ACTIVE`, positions `33`, open orders `0`, same-session after-hours orders `0`, same-session fills `0`, watchlists `0`이었다. separate session budget `0/2`는 열려 있었지만 freshest IEX quote도 `ADBE 20:55:03Z`, `RGTI 20:54:49Z`로 이미 약 `238분` stale였고 `PLTR/QQQ/SPY`도 모두 5분 cap을 넘겨 이번 `0951` cycle은 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-0951-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-12-0931-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned account + runtime positions reconciliation 기준 `33` positions 유지, open orders `0`건이다. `AVGO`는 `5주`, `qty_available=5`, `RGTI`는 `49주`, `qty_available=49`, `SO`는 `5주`, `qty_available=5`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `0931` core/research preflight를 source-of-record로 사용했고 runtime Alpaca MCP `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-11T20:00:00Z)/get_watchlists/get_stock_latest_quote(feed=iex)/get_stock_snapshot(feed=iex)`로 same-session order budget과 submit-boundary quote freshness를 재확인했다. regular market은 closed, account `ACTIVE`, positions `33`, open orders `0`, same-session after-hours orders `0`, watchlists `0`이었다. separate session budget `0/2`는 열려 있었지만 freshest IEX quote도 `ADBE 20:55:03Z`, `RGTI 20:54:49Z`로 이미 약 `218분` stale였고 `PLTR/QQQ/SPY`도 모두 5분 cap을 넘겨 이번 `0931` cycle은 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-0931-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-12-0911-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned account + runtime positions reconciliation 기준 `33` positions 유지, open orders `0`건이다. `AVGO`는 `5주`, `qty_available=5`, `RGTI`는 `49주`, `qty_available=49`, `SO`는 `5주`, `qty_available=5`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `0911` core/research preflight를 source-of-record로 사용했고 runtime Alpaca MCP `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-11T20:00:00Z)/get_account_activities(activity_types=FILL, after=2026-06-11T20:00:00Z)/get_watchlists/get_stock_latest_quote(feed=iex)/get_stock_snapshot(feed=iex)`로 same-session order budget과 submit-boundary quote freshness를 재확인했다. regular market은 closed, account `ACTIVE`, positions `33`, open orders `0`, same-session after-hours fills `0`, watchlists `0`이었다. separate session budget `0/2`는 열려 있었지만 freshest IEX quote도 `ADBE 20:55:03Z`, `RGTI 20:54:49Z`로 이미 약 `197분` stale였고 `PLTR/QQQ/SPY`도 모두 5분 cap을 넘겨 이번 `0911` cycle은 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-0911-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-12-0851-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned account + runtime positions reconciliation 기준 `33` positions 유지, open orders `0`건이다. `AVGO`는 `5주`, `qty_available=5`, `RGTI`는 `49주`, `qty_available=49`, `SO`는 `5주`, `qty_available=5`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `0851` core/research preflight를 source-of-record로 사용했고 runtime Alpaca MCP `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-11T20:00:00Z)/get_account_activities(activity_types=FILL, after=2026-06-11T20:00:00Z)/get_asset/get_stock_latest_quote(feed=iex)/get_stock_snapshot(feed=iex)`로 same-session order budget과 submit-boundary quote freshness를 재확인했다. regular market은 closed, account `ACTIVE`, positions `33`, open orders `0`, same-session after-hours fills `0`이었다. separate session budget `0/2`는 열려 있었지만 freshest IEX quote도 `ADBE 20:55:03Z`, `RGTI 20:54:49Z`로 이미 약 `178분` stale였고 `PLTR/QQQ/SPY`도 모두 5분 cap을 넘겨 이번 `0851` cycle은 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-0851-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-12-0831-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned account + runtime positions reconciliation 기준 `33` positions 유지, open orders `0`건이다. `AVGO`는 `5주`, `qty_available=5`, `RGTI`는 `49주`, `qty_available=49`, `SO`는 `5주`, `qty_available=5`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `0831` core/research preflight를 source-of-record로 사용했고 runtime Alpaca MCP `get_all_positions/get_watchlists/get_account_activities(activity_types=FILL, after=2026-06-11T20:00:00Z)/get_asset/get_stock_latest_quote(feed=iex)/get_stock_snapshot(feed=iex)`로 same-session order budget과 submit-boundary quote freshness를 재확인했다. regular market은 closed, account `ACTIVE`, positions `33`, open orders `0`, same-session after-hours fills `0`, watchlists `0`이었다. separate session budget `0/2`는 열려 있었지만 freshest IEX quote도 `ADBE 20:55:03Z`, `RGTI 20:54:49Z`로 이미 약 `156분` stale였고 `PLTR/QQQ/SPY`도 모두 5분 cap을 넘겨 이번 `0831` cycle은 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-0831-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-12-0811-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime account/positions reconciliation 기준 `33` positions 유지, open orders `0`건이다. `AVGO`는 `5주`, `qty_available=5`, `RGTI`는 `49주`, `qty_available=49`, `SO`는 `5주`, `qty_available=5`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `0811` core/research preflight를 source-of-record로 사용했고 runtime Alpaca MCP `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-11T20:00:00Z)/get_watchlists`로 same-session order budget과 submit boundary를 재확인했다. regular market은 closed, account `ACTIVE`, positions `33`, open orders `0`, same-session after-hours orders `0`, watchlists `0`이었다. separate session budget `0/2`는 열려 있었지만 scheduler-owned IEX quote 기준 freshest `ADBE 20:55:03Z`, `RGTI 20:54:49Z`도 이미 약 `138분` stale였고 `PLTR/QQQ/SPY`도 모두 5분 cap을 넘겨 이번 `0811` cycle은 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-0811-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-12-0751-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime account/positions reconciliation 기준 `33` positions 유지, open orders `0`건이다. `AVGO`는 `5주`, `qty_available=5`, `RGTI`는 `49주`, `qty_available=49`, `SO`는 `5주`, `qty_available=5`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `0751` core/research preflight를 source-of-record로 사용했고 runtime Alpaca MCP `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-11T20:00:00Z)`로 same-session order budget과 submit boundary를 재확인했다. regular market은 closed, account `ACTIVE`, positions `33`, open orders `0`, same-session after-hours orders `0`이었다. separate session budget `0/2`는 열려 있었지만 scheduler-owned IEX quote 기준 freshest `ADBE 20:55:03Z`, `RGTI 20:54:49Z`도 이미 약 `118분` stale였고 `PLTR/QQQ/SPY`도 모두 5분 cap을 넘겨 이번 `0751` cycle은 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-0751-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-12-0731-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime account/positions reconciliation 기준 `33` positions 유지, open orders `0`건이다. `AVGO`는 `5주`, `qty_available=5`, `RGTI`는 `49주`, `qty_available=49`, `SO`는 `5주`, `qty_available=5`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `0731` core/research preflight를 source-of-record로 사용했고 runtime Alpaca MCP `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-11T20:00:00Z)/get_watchlists/get_asset(RGTI/ADBE/PLTR/AVGO/SO)/get_stock_latest_quote(feed=iex)/get_stock_snapshot(feed=iex)/get_stock_latest_quote(feed=overnight)`로 same-session order budget과 submit-boundary quote freshness를 재확인했다. regular market은 closed, account `ACTIVE`, positions `33`, open orders `0`, same-session after-hours orders `0`, watchlists `0`이었다. separate session budget `0/2`는 열려 있었지만 freshest IEX quote도 `ADBE 20:55:03Z`, `RGTI 20:54:49Z`로 이미 약 `99분` stale였고 `PLTR/QQQ/SPY`도 모두 5분 cap을 넘겨 이번 `0731` cycle은 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-0731-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-12-0711-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime account/positions reconciliation 기준 `33` positions 유지, open orders `0`건이다. `AVGO`는 `5주`, `qty_available=5`, `RGTI`는 `49주`, `qty_available=49`, `SO`는 `5주`, `qty_available=5`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `0711` core/research preflight를 source-of-record로 사용했고 runtime Alpaca MCP `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-11T20:00:00Z)/get_watchlists/get_asset(RGTI/ADBE/PLTR/AVGO/SO)/get_stock_latest_quote(feed=iex)/get_stock_snapshot(feed=iex)/get_stock_latest_quote(feed=overnight)`로 same-session order budget과 submit-boundary quote freshness를 재확인했다. regular market은 closed, account `ACTIVE`, positions `33`, open orders `0`, same-session after-hours orders `0`, watchlists `0`이었다. separate session budget `0/2`는 열려 있었지만 freshest IEX quote도 `ADBE 20:55:03Z`, `RGTI 20:54:49Z`로 이미 약 `77분` stale였고 `PLTR/QQQ/SPY`도 모두 5분 cap을 넘겨 이번 `0711` cycle은 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-0711-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-12-0651-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime account/positions reconciliation 기준 `33` positions 유지, open orders `0`건이다. `AVGO`는 `5주`, `qty_available=5`, `RGTI`는 `49주`, `qty_available=49`, `SO`는 `5주`, `qty_available=5`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `0651` core/research preflight를 source-of-record로 사용했고 runtime Alpaca MCP `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-11T20:00:00Z)/get_watchlists/get_asset(RGTI/ADBE/PLTR/AVGO/SO)/get_stock_latest_quote(feed=iex)/get_stock_snapshot(feed=iex)/get_stock_latest_quote(feed=overnight)`로 same-session order budget과 submit-boundary quote freshness를 재확인했다. regular market은 closed, account `ACTIVE`, positions `33`, open orders `0`, same-session after-hours orders `0`, watchlists `0`이었다. separate session budget `0/2`는 열려 있었지만 freshest IEX quote도 `ADBE 20:55:03Z`, `RGTI 20:54:49Z`로 이미 약 `58분` stale였고 `PLTR/QQQ/SPY`도 모두 5분 cap을 넘겨 이번 `0651` cycle은 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-0651-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-12-0631-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime account/positions reconciliation 기준 `33` positions 유지, open orders `0`건이다. `AVGO`는 `5주`, `qty_available=5`, `RGTI`는 `49주`, `qty_available=49`, `SO`는 `5주`, `qty_available=5`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `0631` core/research preflight를 source-of-record로 사용했고 runtime Alpaca MCP `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-11T20:00:00Z)/get_watchlists/get_asset(RGTI/ADBE/PLTR/AVGO/SO)/get_stock_latest_quote(feed=iex)/get_stock_snapshot(feed=iex)/get_stock_latest_quote(feed=overnight)`로 same-session order budget과 submit-boundary quote freshness를 재확인했다. regular market은 closed, account `ACTIVE`, positions `33`, open orders `0`, same-session after-hours orders `0`, watchlists `0`이었다. separate session budget `0/2`는 열려 있었지만 freshest IEX quote도 `ADBE 20:55:03Z`, `RGTI 20:54:49Z`로 이미 약 `38분` stale였고 `PLTR/QQQ/SPY`도 모두 5분 cap을 넘겨 이번 `0631` cycle은 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-0631-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-12-0611-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime account/positions reconciliation 기준 `33` positions 유지, open orders `0`건이다. `AVGO`는 `5주`, `qty_available=5`, `RGTI`는 `49주`, `qty_available=49`, `SO`는 `5주`, `qty_available=5`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `0611` core/research preflight를 source-of-record로 사용했고 runtime Alpaca MCP `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-11T20:00:00Z)/get_watchlists/get_asset(RGTI/ADBE/PLTR)/get_stock_latest_quote(feed=iex)/get_stock_snapshot(feed=iex)/get_stock_latest_quote(feed=overnight)`로 same-session order budget과 submit-boundary quote freshness를 재확인했다. regular market은 closed, account `ACTIVE`, positions `33`, open orders `0`, same-session after-hours orders `0`, watchlists `0`이었다. separate session budget `0/2`는 열려 있었지만 freshest IEX quote도 `ADBE 20:55:03Z`, `RGTI 20:54:49Z`로 약 `20분` stale였고 `PLTR/QQQ/SPY`도 모두 5분 cap을 넘겨 이번 `0611` cycle은 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-0611-after-hours-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-12-0451-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned core preflight reconciliation 기준 `33` positions 유지, open orders `0`건이다. `AVGO`는 `5주`, `qty_available=5`, `RGTI`는 `49주`, `qty_available=49`, `SO`는 `5주`, `qty_available=5`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `0451` stale cleanup/core/research preflight를 source-of-record로 사용했고 scheduler-owned Alpaca core `get_clock/get_account_info/get_orders_open/get_all_positions/get_account_activities/get_stock_latest_quote/get_stock_snapshot` rows로 same-day fill discipline과 submit-boundary quote/spread를 재확인했다. same-day regular-session `AVGO` trim 1건과 after-hours `RGTI` trim fills 2건은 그대로 유지됐고, `AVGO`는 spread 0.0882%가 policy cap 이내지만 duplicate sell discipline, `RGTI`는 duplicate sell discipline, `SO`는 spread 6.2780% fail + trim metric gap, 신규 buy path는 `review_backlog_pending_1d_count=14`와 benchmark floor cap에 막혀 이번 `0451` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-0451-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-12-0431-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned core preflight reconciliation 기준 `33` positions 유지, open orders `0`건이다. `AVGO`는 `5주`, `qty_available=5`, `RGTI`는 `49주`, `qty_available=49`, `SO`는 `5주`, `qty_available=5`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `0431` stale cleanup/core/research preflight를 source-of-record로 사용했고 scheduler-owned Alpaca core `get_clock/get_account_info/get_orders_open/get_all_positions/get_account_activities/get_stock_latest_quote/get_stock_snapshot` rows로 same-day fill discipline과 submit-boundary quote/spread를 재확인했다. same-day regular-session `AVGO` trim 1건과 after-hours `RGTI` trim fills 2건은 그대로 유지됐고, `AVGO`는 spread `0.1729%`가 policy cap 이내지만 duplicate sell discipline, `RGTI`는 duplicate sell discipline, `SO`는 trim metric gap, 신규 buy path는 `review_backlog_pending_1d_count=14`와 benchmark floor cap에 막혀 이번 `0431` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-0431-hourly-autopilot-post-trade.json`

- Run: [[2026-06-12-0411-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned core preflight reconciliation 기준 `33` positions 유지, open orders `0`건이다. `AVGO`는 `5주`, `qty_available=5`, `RGTI`는 `49주`, `qty_available=49`, `SO`는 `5주`, `qty_available=5`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `0411` stale cleanup/core/research preflight를 source-of-record로 사용했고 scheduler-owned Alpaca core `get_clock/get_account_info/get_orders_open/get_all_positions/get_account_activities/get_stock_latest_quote/get_stock_snapshot` rows로 same-day fill discipline과 submit-boundary quote/spread를 재확인했다. same-day regular-session `AVGO` trim 1건과 after-hours `RGTI` trim fills 2건은 그대로 유지됐고, `AVGO`는 spread `0.2933%`가 policy cap 이내지만 duplicate sell discipline, `RGTI`는 duplicate sell discipline, `SO`는 trim metric gap, 신규 buy path는 `review_backlog_pending_1d_count=14`와 benchmark floor cap에 막혀 이번 `0411` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-0411-hourly-autopilot-post-trade.json`

- Run: [[2026-06-12-0351-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned core preflight reconciliation 기준 `33` positions 유지, open orders `0`건이다. `AVGO`는 `5주`, `qty_available=5`, `RGTI`는 `49주`, `qty_available=49`, `SO`는 `5주`, `qty_available=5`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `0351` stale cleanup/core/research preflight를 source-of-record로 사용했고 scheduler-owned Alpaca core `get_clock/get_account_info/get_orders_open/get_all_positions/get_account_activities/get_stock_latest_quote/get_stock_snapshot` rows로 same-day fill discipline과 submit-boundary quote/spread를 재확인했다. same-day regular-session `AVGO` trim 1건과 after-hours `RGTI` trim fills 2건은 그대로 유지됐고, `AVGO`는 spread `0.3037%`가 policy cap 이내로 회복됐지만 duplicate sell discipline, `RGTI`는 duplicate sell discipline, `SO`는 trim metric gap, 신규 buy path는 `review_backlog_pending_1d_count=14`와 benchmark floor cap에 막혀 이번 `0351` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-0351-hourly-autopilot-post-trade.json`

- Run: [[2026-06-12-0331-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned core preflight reconciliation 기준 `33` positions 유지, open orders `0`건이다. `AVGO`는 `5주`, `qty_available=5`, `RGTI`는 `49주`, `qty_available=49`, `SO`는 `5주`, `qty_available=5`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `0331` stale cleanup/core/research preflight를 source-of-record로 사용했고 scheduler-owned Alpaca core `get_clock/get_account_info/get_orders_open/get_all_positions/get_account_activities/get_stock_latest_quote/get_stock_snapshot` rows로 same-day fill discipline과 submit-boundary quote/spread를 재확인했다. same-day regular-session `AVGO` trim 1건과 after-hours `RGTI` trim fills 2건은 그대로 유지됐고, `AVGO`는 spread `1.7255%`가 policy cap을 크게 넘겨 trim hard gate fail, `RGTI`는 duplicate sell discipline, `SO`는 spread 회복 후에도 trim metric gap, 신규 buy path는 `review_backlog_pending_1d_count=14`와 benchmark floor cap에 막혀 이번 `0331` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-0331-hourly-autopilot-post-trade.json`

- Run: [[2026-06-12-0311-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned core preflight reconciliation 기준 `33` positions 유지, open orders `0`건이다. `AVGO`는 `5주`, `qty_available=5`, `RGTI`는 `49주`, `qty_available=49`, `SO`는 `5주`, `qty_available=5`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `0311` stale cleanup/core/research preflight를 source-of-record로 사용했고 scheduler-owned Alpaca core `get_clock/get_account_info/get_orders_open/get_all_positions/get_account_activities/get_stock_latest_quote/get_stock_snapshot` rows로 same-day fill discipline과 submit-boundary quote/spread를 재확인했다. same-day regular-session `AVGO` trim 1건과 after-hours `RGTI` trim fills 2건은 그대로 유지됐고, `AVGO`는 spread `1.8672%`가 policy cap을 크게 넘겨 trim hard gate fail, `RGTI`는 duplicate sell discipline, `SO`는 spread 회복 후에도 trim metric gap, 신규 buy path는 `review_backlog_pending_1d_count=14`와 benchmark floor cap에 막혀 이번 `0311` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-0311-hourly-autopilot-post-trade.json`

- Run: [[2026-06-12-0251-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned core preflight reconciliation 기준 `33` positions 유지, open orders `0`건이다. `AVGO`는 `5주`, `qty_available=5`, `RGTI`는 `49주`, `qty_available=49`, `SO`는 `5주`, `qty_available=5`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `0251` stale cleanup/core/research preflight를 source-of-record로 사용했고 scheduler-owned Alpaca core `get_clock/get_account_info/get_orders_open/get_all_positions/get_account_activities/get_stock_latest_quote/get_stock_snapshot` rows로 same-day fill discipline과 submit-boundary quote/spread를 재확인했다. same-day regular-session `AVGO` trim 1건과 after-hours `RGTI` trim fills 2건은 그대로 유지됐고, `AVGO`는 spread `4.6962%`가 policy cap을 크게 넘겨 trim hard gate fail, `RGTI`는 duplicate sell discipline, `SO`는 spread `2.0523%` fail + trim metric gap, 신규 buy path는 `review_backlog_pending_1d_count=14`와 benchmark floor cap에 막혀 이번 `0251` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-0251-hourly-autopilot-post-trade.json`

- Run: [[2026-06-12-0231-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned core preflight reconciliation 기준 `33` positions 유지, open orders `0`건이다. `AVGO`는 `5주`, `qty_available=5`, `RGTI`는 `49주`, `qty_available=49`, `SO`는 `5주`, `qty_available=5`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `0231` stale cleanup/core/research preflight를 source-of-record로 사용했고 scheduler-owned Alpaca core `get_clock/get_account_info/get_orders_open/get_all_positions/get_account_activities/get_stock_latest_quote/get_stock_snapshot` rows로 same-day fill discipline과 submit-boundary quote/spread를 재확인했다. same-day regular-session `AVGO` trim 1건과 after-hours `RGTI` trim fills 2건은 그대로 유지됐고, `AVGO`는 spread `2.5350%`가 policy cap을 크게 넘겨 trim hard gate fail, `RGTI`는 duplicate sell discipline, `SO`는 spread `1.9780%` fail + trim metric gap, 신규 buy path는 `review_backlog_pending_1d_count=14`와 benchmark floor cap에 막혀 이번 `0231` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-0231-hourly-autopilot-post-trade.json`

- Run: [[2026-06-12-0211-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned core preflight reconciliation 기준 `33` positions 유지, open orders `0`건이다. `AVGO`는 `5주`, `qty_available=5`, `RGTI`는 `49주`, `qty_available=49`, `SO`는 `5주`, `qty_available=5`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `0211` stale cleanup/core/research preflight를 source-of-record로 사용했고 scheduler-owned Alpaca core `get_clock/get_account_info/get_orders_open/get_all_positions/get_account_activities/get_stock_latest_quote/get_stock_snapshot` rows로 same-day fill discipline과 submit-boundary quote/spread를 재확인했다. same-day regular-session `AVGO` trim 1건과 after-hours `RGTI` trim fills 2건은 그대로 유지됐고, `AVGO`는 spread `1.0211%`가 policy cap을 다시 넘겨 trim hard gate fail, `RGTI`는 duplicate sell discipline, `SO`는 trim metric gap, 신규 buy path는 `review_backlog_pending_1d_count=14`와 benchmark floor cap에 막혀 이번 `0211` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-0211-hourly-autopilot-post-trade.json`

- Run: [[2026-06-12-0151-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned core preflight reconciliation 기준 `33` positions 유지, open orders `0`건이다. `AVGO`는 `5주`, `qty_available=5`, `RGTI`는 `49주`, `qty_available=49`, `SO`는 `5주`, `qty_available=5`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `0151` stale cleanup/core/research preflight를 source-of-record로 사용했고 scheduler-owned Alpaca core `get_clock/get_account_info/get_orders_open/get_all_positions/get_account_activities/get_stock_latest_quote/get_stock_snapshot` rows로 same-day fill discipline과 submit-boundary quote/spread를 재확인했다. same-day regular-session `AVGO` trim 1건과 after-hours `RGTI` trim fills 2건은 그대로 유지됐고, `AVGO`는 spread `0.6658%`가 policy cap을 다시 넘겨 trim hard gate fail, `RGTI`는 duplicate sell discipline, `SO`는 trim metric gap, 신규 buy path는 `review_backlog_pending_1d_count=14`와 benchmark floor cap에 막혀 이번 `0151` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-0151-hourly-autopilot-post-trade.json`

- Run: [[2026-06-12-0131-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned core preflight reconciliation 기준 `33` positions 유지, open orders `0`건이다. `AVGO`는 `5주`, `qty_available=5`, `RGTI`는 `49주`, `qty_available=49`, `SO`는 `5주`, `qty_available=5`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `0131` stale cleanup/core/research preflight를 source-of-record로 사용했고 scheduler-owned Alpaca core `get_clock/get_account_info/get_orders_open/get_all_positions/get_account_activities/get_stock_latest_quote/get_stock_snapshot` rows로 same-day fill discipline과 submit-boundary quote/spread를 재확인했다. same-day regular-session `AVGO` trim 1건과 after-hours `RGTI` trim fills 2건은 그대로 유지됐고, `AVGO`는 spread `0.3196%`가 정상 범위였지만 same-day duplicate sell discipline, `RGTI`는 duplicate sell discipline, `SO`는 trim metric gap, 신규 buy path는 `review_backlog_pending_1d_count=14`와 benchmark floor cap에 막혀 이번 `0131` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-0131-hourly-autopilot-post-trade.json`

- Run: [[2026-06-12-0111-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned core preflight reconciliation 기준 `33` positions 유지, open orders `0`건이다. `AVGO`는 `5주`, `qty_available=5`, `RGTI`는 `49주`, `qty_available=49`, `SO`는 `5주`, `qty_available=5`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `0111` stale cleanup/core/research preflight를 source-of-record로 사용했고 scheduler-owned Alpaca core `get_clock/get_account_info/get_orders_open/get_all_positions/get_account_activities/get_stock_latest_quote/get_stock_snapshot` rows로 same-day fill discipline과 submit-boundary quote/spread를 재확인했다. same-day regular-session `AVGO` trim 1건과 after-hours `RGTI` trim fills 2건은 그대로 유지됐고, `AVGO`는 spread `0.2166%`가 정상 범위였지만 same-day duplicate sell discipline, `RGTI`는 duplicate sell discipline, `SO`는 trim metric gap, 신규 buy path는 `review_backlog_pending_1d_count=14`와 benchmark floor cap에 막혀 이번 `0111` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-0111-hourly-autopilot-post-trade.json`

- Run: [[2026-06-12-0051-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned core preflight reconciliation 기준 `33` positions 유지, open orders `0`건이다. `AVGO`는 `5주`, `qty_available=5`, `RGTI`는 `49주`, `qty_available=49`, `SO`는 `5주`, `qty_available=5`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `0051` stale cleanup/core/research preflight를 source-of-record로 사용했고 scheduler-owned Alpaca core `get_clock/get_account_info/get_orders_open/get_all_positions/get_account_activities/get_stock_latest_quote/get_stock_snapshot` rows로 same-day fill discipline과 submit-boundary quote/spread를 재확인했다. same-day regular-session `AVGO` trim 1건과 after-hours `RGTI` trim fills 2건은 그대로 유지됐고, `AVGO`는 scheduler-owned spread `1.4676%` fail + duplicate sell recheck, `RGTI`는 duplicate sell discipline, `SO`는 spread 회복 후에도 trim metric gap, 신규 buy path는 `review_backlog_pending_1d_count=14`와 benchmark floor cap에 막혀 이번 `0051` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-0051-hourly-autopilot-post-trade.json`

- Run: [[2026-06-12-0031-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned core preflight reconciliation 기준 `33` positions 유지, open orders `0`건이다. `AVGO`는 `5주`, `qty_available=5`, `RGTI`는 `49주`, `qty_available=49`, `SO`는 `5주`, `qty_available=5`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `0031` stale cleanup/core/research preflight를 source-of-record로 사용했고 scheduler-owned Alpaca core `get_clock/get_account_info/get_orders_open/get_all_positions/get_account_activities/get_stock_latest_quote/get_stock_snapshot` rows로 same-day fill discipline과 submit-boundary quote/spread를 재확인했다. same-day regular-session `AVGO` trim 1건과 after-hours `RGTI` trim fills 2건은 그대로 유지됐고, `AVGO`는 scheduler-owned spread 1.8952% fail + duplicate sell recheck, `RGTI`는 duplicate sell discipline, `SO`는 spread 회복 후에도 trim metric gap, 신규 buy path는 `review_backlog_pending_1d_count=14`와 benchmark floor cap에 막혀 이번 `0031` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-0031-hourly-autopilot-post-trade.json`

- Run: [[2026-06-12-0011-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime account/positions reconciliation 기준 `33` positions 유지, open orders `0`건이다. `AVGO`는 `5주`, `qty_available=5`, `RGTI`는 `49주`, `qty_available=49`, `SO`는 `5주`, `qty_available=5`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `0011` stale cleanup/core/research preflight를 source-of-record로 사용했고 runtime Alpaca MCP `get_clock/get_account_info/get_orders(status=open)/get_all_positions/get_account_activities(activity_types=FILL, after=2026-06-11T00:00:00Z)/get_asset/get_stock_latest_quote/get_stock_snapshot`로 same-day fill discipline과 submit-boundary quote/spread를 재확인했다. same-day regular-session `AVGO` trim 1건과 after-hours `RGTI` trim fills 2건은 그대로 유지됐고, `AVGO`는 live spread `1.2372%` fail + duplicate sell recheck, `RGTI`는 duplicate sell discipline, `SO`는 live spread `1.9689%` fail + trim metric gap, 신규 buy path는 `review_backlog_pending_1d_count=14`와 benchmark floor cap에 막혀 이번 `0011` cycle은 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-0011-hourly-autopilot-post-trade.json`

- Run: [[2026-06-11-2351-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime account/positions reconciliation 기준 `33` positions 유지, open orders `0`건이다. `AVGO`는 `5주`, `qty_available=5`, `RGTI`는 `49주`, `qty_available=49`, `SO`는 `5주`, `qty_available=5`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `2351` stale cleanup/core/research preflight를 source-of-record로 사용했고 runtime Alpaca MCP `get_clock/get_account_info/get_orders(status=open)/get_all_positions/get_account_activities(activity_types=FILL, after=2026-06-11T00:00:00Z)/get_asset/get_stock_latest_quote/get_stock_snapshot`로 same-day fill discipline과 submit-boundary quote/spread를 재확인했다. same-day regular-session `AVGO` trim 1건과 after-hours `RGTI` trim fills 2건은 그대로 유지됐고, `AVGO`는 live spread `0.2206%`가 정상 범위였지만 same-day duplicate sell discipline, `RGTI`는 duplicate sell discipline, `SO`는 live spread `2.9231%` fail + trim metric gap, 신규 buy path는 `review_backlog_pending_1d_count=14`로 막혀 이번 `2351` cycle은 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-11-2351-hourly-autopilot-post-trade.json`

- Run: [[2026-06-11-2331-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime account/positions reconciliation 기준 `33` positions 유지, open orders `0`건이다. `AVGO`는 `5주`, `qty_available=5`, `RGTI`는 `49주`, `qty_available=49`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `2331` stale cleanup/core/research preflight를 source-of-record로 사용했고 runtime Alpaca MCP `get_clock/get_account_info/get_orders(status=open)/get_all_positions/get_account_activities(activity_types=FILL, after=2026-06-11T00:00:00Z)/get_asset/get_stock_latest_quote/get_stock_snapshot`로 same-day fill discipline과 submit-boundary quote/spread를 재확인했다. same-day regular-session `AVGO` trim 1건과 after-hours `RGTI` trim fills 2건은 그대로 유지됐고, `AVGO`는 live spread `0.7149%` fail, `RGTI`는 duplicate sell discipline, `SO`는 trim metric gap, 신규 buy path는 `review_backlog_pending_1d_count=14`로 막혀 이번 `2331` cycle은 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-11-2331-hourly-autopilot-post-trade.json`

- Run: [[2026-06-11-2311-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime account/positions reconciliation 기준 `33` positions 유지, open orders `0`건이다. `AVGO`는 `5주`, `qty_available=5`, `RGTI`는 `49주`, `qty_available=49`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `2311` stale cleanup/core/research preflight를 source-of-record로 사용했고 runtime Alpaca MCP `get_clock/get_account_info/get_orders(status=open)/get_all_positions/get_account_activities(activity_types=FILL, after=2026-06-11T00:00:00Z)/get_stock_latest_quote/get_stock_snapshot`로 same-day fill discipline과 submit-boundary quote/spread를 재확인했다. same-day regular-session `AVGO` trim fill 1건과 after-hours `RGTI` trim fills 2건이 그대로 남아 있었고, `AVGO`는 live spread `2.2097%` fail, `RGTI`는 duplicate sell discipline, `SO`는 trim metric gap, 신규 buy path는 `review_backlog_pending_1d_count=14`로 막혀 이번 `2311` cycle은 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-11-2311-hourly-autopilot-post-trade.json`

- Run: [[2026-06-11-2251-hourly-autopilot]]
- Open/new: 없음
- Filled: `AVGO` sell 1주 `filled_avg_price=380.43 USD`
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime account/positions reconciliation 기준 `33` positions 유지, open orders `0`건이다. `AVGO`는 `5주`, `qty_available=5`로 감소했다.
- Recent reconciliation scope: scheduler-owned `2251` stale cleanup/core/research preflight를 source-of-record로 사용했고 runtime Alpaca MCP `get_clock/get_account_info/get_orders(status=open)/get_all_positions/get_account_activities(activity_types=FILL, after=2026-06-11T00:00:00Z)/get_order_by_id(a4414ccd-c32c-48bb-97ec-189dc42f6cb8)`로 submit boundary와 체결 상태를 재확인했다. `review_backlog_pending_1d_count=14`는 신규 buy를 막았지만 sell-first path에서 `AVGO`는 spread `0.0342%`로 trim gate를 통과해 1주 trim이 즉시 체결됐다.
- Orders submitted/replaced/cancelled/closed by this workflow: 1 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-11-2251-hourly-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-11-2151-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime account/positions reconciliation 기준 `33` positions 유지, open orders `0`건이다. `RGTI`는 `49주`, `qty_available=49`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `2151` core/research preflight를 source-of-record로 사용했고 runtime Alpaca MCP `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_watchlists/get_order_by_client_id(ah-20260611-0951-sell-rgti)/get_order_by_client_id(ah-20260611-1011-sell-rgti)/get_asset(ORCL)/get_stock_latest_quote(feed=overnight)/get_stock_snapshot(feed=overnight)`로 장외 session budget과 prior client-order lifecycle를 재확인했다. same-session after-hours fills는 여전히 `2건`이었고 separate budget `2/2`가 유지돼 이번 `2151` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-11-2151-after-hours-autopilot-post-trade.json`

- Run: [[2026-06-11-2131-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime account/positions reconciliation 기준 `33` positions 유지, open orders `0`건이다. `RGTI`는 `49주`, `qty_available=49`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `2131` core/research preflight를 source-of-record로 사용했고 runtime Alpaca MCP `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_watchlists/get_order_by_client_id(ah-20260611-0951-sell-rgti)/get_order_by_client_id(ah-20260611-1011-sell-rgti)/get_asset(ORCL)/get_stock_latest_quote(feed=overnight)/get_stock_snapshot(feed=overnight)`로 장외 session budget과 prior client-order lifecycle를 재확인했다. same-session after-hours fills는 여전히 `2건`이었고 separate budget `2/2`가 유지돼 이번 `2131` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-11-2131-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-11-2111-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime account/positions reconciliation 기준 `33` positions 유지, open orders `0`건이다. `RGTI`는 `49주`, `qty_available=49`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `2111` core/research preflight를 source-of-record로 사용했고 runtime Alpaca MCP `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_watchlists/get_order_by_client_id(ah-20260611-0951-sell-rgti)/get_order_by_client_id(ah-20260611-1011-sell-rgti)/get_asset(ORCL)/get_stock_latest_quote(feed=overnight)/get_stock_snapshot(feed=overnight)`로 장외 session budget과 prior client-order lifecycle를 재확인했다. same-session after-hours fills는 여전히 `2건`이었고 separate budget `2/2`가 유지돼 이번 `2111` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-11-2111-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-11-2051-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime account/positions reconciliation 기준 `33` positions 유지, open orders `0`건이다. `RGTI`는 `49주`, `qty_available=49`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `2051` core/research preflight를 source-of-record로 사용했고 runtime Alpaca MCP `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_account_activities(activity_types=FILL, after=2026-06-10T20:00:00Z)/get_watchlists/get_order_by_client_id(ah-20260611-0951-sell-rgti)/get_order_by_client_id(ah-20260611-1011-sell-rgti)/get_asset(ORCL)/get_stock_latest_quote(feed=overnight)/get_stock_snapshot(feed=overnight)`로 장외 session budget과 prior client-order lifecycle를 재확인했다. same-session after-hours fills는 여전히 `2건`이었고 separate budget `2/2`가 유지돼 이번 `2051` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-11-2051-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-11-2031-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime account/positions reconciliation 기준 `33` positions 유지, open orders `0`건이다. `RGTI`는 `49주`, `qty_available=49`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `2031` core/research preflight를 source-of-record로 사용했고 runtime Alpaca MCP `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_watchlists/get_order_by_client_id(ah-20260611-0951-sell-rgti)/get_order_by_client_id(ah-20260611-1011-sell-rgti)/get_asset(ORCL)/get_stock_latest_quote(feed=overnight)/get_stock_snapshot(feed=overnight)`로 장외 session budget과 prior client-order lifecycle를 재확인했다. same-session after-hours fills는 여전히 `2건`이었고 separate budget `2/2`가 유지돼 이번 `2031` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-11-2031-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-11-2011-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime account/positions reconciliation 기준 `33` positions 유지, open orders `0`건이다. `RGTI`는 `49주`, `qty_available=49`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `2011` core/research preflight를 source-of-record로 사용했고 runtime Alpaca MCP `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_account_activities(activity_types=FILL, after=2026-06-10T20:00:00Z)/get_watchlists/get_order_by_client_id(ah-20260611-0951-sell-rgti)/get_order_by_client_id(ah-20260611-1011-sell-rgti)/get_stock_latest_quote(feed=overnight)/get_stock_snapshot(feed=overnight)`로 장외 session budget과 prior client-order lifecycle를 재확인했다. same-session after-hours fills는 여전히 `2건`이었고 separate budget `2/2`가 유지돼 이번 `2011` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-11-2011-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-11-1951-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime account/positions reconciliation 기준 `33` positions 유지, open orders `0`건이다. `RGTI`는 `49주`, `qty_available=49`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `1951` core/research preflight를 source-of-record로 사용했고 runtime Alpaca MCP `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_account_activities(activity_types=FILL, after=2026-06-10T20:00:00Z)/get_watchlists/get_order_by_client_id(ah-20260611-0951-sell-rgti)/get_order_by_client_id(ah-20260611-1011-sell-rgti)/get_stock_latest_quote(feed=overnight)/get_stock_snapshot(feed=overnight)`로 장외 session budget과 prior client-order lifecycle를 재확인했다. same-session after-hours fills는 여전히 `2건`이었고 separate budget `2/2`가 유지돼 이번 `1951` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-11-1951-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-11-1931-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime account/positions reconciliation 기준 `33` positions 유지, open orders `0`건이다. `RGTI`는 `49주`, `qty_available=49`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `1931` core/research preflight를 source-of-record로 사용했고 runtime Alpaca MCP `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_account_activities(activity_types=FILL, after=2026-06-10T20:00:00Z)/get_watchlists/get_order_by_client_id(ah-20260611-0951-sell-rgti)/get_order_by_client_id(ah-20260611-1011-sell-rgti)/get_stock_latest_quote(feed=overnight)/get_stock_snapshot(feed=overnight)`로 장외 session budget과 prior client-order lifecycle를 재확인했다. same-session after-hours fills는 여전히 `2건`이었고 separate budget `2/2`가 유지돼 이번 `1931` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-11-1931-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-11-1911-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned account/positions reconciliation 기준 `33` positions 유지, open orders `0`건이다. `RGTI`는 `49주`, `qty_available=49`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `1911` core/research preflight를 source-of-record로 사용했고 `get_clock/get_account_info/get_all_positions/get_orders_open/get_account_activities/get_watchlists` 기준 same-session after-hours fills `2건`, open orders `0`건을 유지했다. 이번 cycle Alpaca MCP `get_all_positions/get_watchlists/get_stock_latest_quote(feed=overnight)/get_stock_snapshot(feed=overnight)` 교차 확인에서도 positions `33`, watchlists `0`, `ORCL` overnight quote availability가 유지됐고 separate budget `2/2` exhausted 상태가 unchanged라 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-11-1911-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-11-1851-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime account/positions reconciliation 기준 `33` positions 유지, open orders `0`건이다. `RGTI`는 `49주`, `qty_available=49`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `1851` core/research preflight를 source-of-record로 사용했고 runtime Alpaca MCP `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_account_activities(activity_types=FILL, after=2026-06-10T20:00:00Z)/get_watchlists/get_order_by_client_id(ah-20260611-0951-sell-rgti)/get_order_by_client_id(ah-20260611-1011-sell-rgti)/get_asset(ORCL)/get_stock_latest_quote(feed=overnight)/get_stock_snapshot(feed=overnight)`로 장외 session budget과 prior client-order lifecycle를 재확인했다. same-session after-hours fills는 여전히 `2건`이었고 separate budget `2/2`가 유지돼 이번 `1851` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-11-1851-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-11-1831-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime account/positions reconciliation 기준 `33` positions 유지, open orders `0`건이다. `RGTI`는 `49주`, `qty_available=49`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `1831` core/research preflight를 source-of-record로 사용했고 runtime Alpaca MCP `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_account_activities(activity_types=FILL, after=2026-06-10T20:00:00Z)/get_watchlists/get_order_by_client_id(ah-20260611-0951-sell-rgti)/get_order_by_client_id(ah-20260611-1011-sell-rgti)/get_asset(ORCL)/get_stock_latest_quote(feed=overnight)/get_stock_snapshot(feed=overnight)`로 장외 session budget과 prior client-order lifecycle를 재확인했다. same-session after-hours fills는 여전히 `2건`이었고 separate budget `2/2`가 유지돼 이번 `1831` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-11-1831-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-11-1811-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime account/positions reconciliation 기준 `33` positions 유지, open orders `0`건이다. `RGTI`는 `49주`, `qty_available=49`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `1811` core/research preflight를 source-of-record로 사용했고 runtime Alpaca MCP `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_account_activities(activity_types=FILL, after=2026-06-10T20:00:00Z)/get_watchlists/get_order_by_client_id(ah-20260611-0951-sell-rgti)/get_order_by_client_id(ah-20260611-1011-sell-rgti)/get_asset(ORCL)/get_stock_latest_quote(feed=overnight)/get_stock_snapshot(feed=overnight)`로 장외 session budget과 prior client-order lifecycle를 재확인했다. same-session after-hours fills는 여전히 `2건`이었고 separate budget `2/2`가 유지돼 이번 `1811` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-11-1811-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-11-1751-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime account/positions reconciliation 기준 `33` positions 유지, open orders `0`건이다. `RGTI`는 `49주`, `qty_available=49`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `1751` core/research preflight를 source-of-record로 사용했고 runtime Alpaca MCP `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_account_activities(activity_types=FILL, after=2026-06-10T20:00:00Z)/get_watchlists/get_order_by_client_id(ah-20260611-0951-sell-rgti)/get_order_by_client_id(ah-20260611-1011-sell-rgti)/get_asset(ORCL)/get_stock_latest_quote(feed=overnight)/get_stock_snapshot(feed=overnight)`로 장외 session budget과 prior client-order lifecycle를 재확인했다. same-session after-hours fills는 여전히 `2건`이었고 separate budget `2/2`가 유지돼 이번 `1751` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-11-1751-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-11-1731-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned account/positions reconciliation 기준 `33` positions 유지, open orders `0`건이다. `RGTI`는 `49주`, `qty_available=49`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `1731` core/research preflight를 source-of-record로 사용했고 `get_account_info/get_all_positions/get_orders_open/get_account_activities/get_watchlists/get_asset/get_stock_latest_quote/get_stock_snapshot` 기준 same-session after-hours fills `2건`, open orders `0`건, watchlists `0`건을 유지했다. local Alpaca MCP `get_watchlists/get_order_by_client_id(ah-20260611-0951-sell-rgti)/get_order_by_client_id(ah-20260611-1011-sell-rgti)/get_stock_latest_quote(feed=overnight)/get_stock_snapshot(feed=overnight)` 교차 확인도 일치했고 separate budget `2/2` exhausted 상태가 unchanged라 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-11-1731-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-11-1711-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned account/positions reconciliation 기준 `33` positions 유지, open orders `0`건이다. `RGTI`는 `49주`, `qty_available=49`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `1711` core/research preflight를 source-of-record로 사용했고 `get_account_info/get_all_positions/get_orders_open/get_account_activities/get_watchlists/get_asset/get_stock_latest_quote/get_stock_snapshot` 기준 same-session after-hours fills `2건`, open orders `0`건, watchlists `0`건을 유지했다. 이번 cycle은 scheduler-owned passing rows만으로 required after-hours gates를 모두 충족했고 separate budget `2/2` exhausted 상태가 unchanged라 추가 local runtime Alpaca MCP read-only 재시도 없이 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-11-1711-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-11-1611-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime account/positions reconciliation 기준 `33` positions 유지, open orders `0`건이다. `RGTI`는 `49주`, `qty_available=49`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `1611` research preflight를 유지했고, Alpaca core preflight row 공백은 runtime Alpaca MCP `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-10T20:00:00Z)/get_account_activities(activity_types=FILL, after=2026-06-10T20:00:00Z)/get_watchlists/get_order_by_client_id(ah-20260611-0951-sell-rgti)/get_order_by_client_id(ah-20260611-1011-sell-rgti)/get_stock_latest_quote(feed=overnight)/get_stock_snapshot(feed=overnight)/get_asset(ORCL)`로 backfill했다. same-session after-hours fills는 여전히 `2건`이었고 separate budget `2/2`가 유지돼 이번 `1611` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-11-1611-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-11-1551-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime account/positions reconciliation 기준 `33` positions 유지, open orders `0`건이다. `RGTI`는 `49주`, `qty_available=49`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `1551` core/research preflight를 source-of-record로 사용했고 runtime Alpaca MCP `get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-10T20:00:00Z)/get_account_activities(activity_types=FILL, after=2026-06-10T20:00:00Z)/get_watchlists/get_order_by_client_id(ah-20260611-0951-sell-rgti)/get_order_by_client_id(ah-20260611-1011-sell-rgti)`로 장외 session budget과 prior client-order lifecycle를 재확인했다. same-session after-hours fills는 여전히 `2건`이었고 separate budget `2/2`가 유지돼 이번 `1551` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-11-1551-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-11-1531-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned account/positions reconciliation 기준 `33` positions 유지, open orders `0`건이다. `RGTI`는 `49주`, `qty_available=49`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `1531` core/research preflight를 source-of-record로 사용했고 `get_account_activities(activity_types=FILL)` 기준 same-session after-hours fills `2건`, `get_orders_open` 기준 open orders `0`건, `get_watchlists` 기준 watchlists `0`건을 유지했다. 이번 cycle은 scheduler-owned passing rows만으로 required after-hours gates를 모두 충족했고 separate budget `2/2` exhausted 상태가 unchanged라 추가 local runtime Alpaca MCP read-only 재시도 없이 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-11-1531-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-11-1511-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned account/positions reconciliation 기준 `33` positions 유지, open orders `0`건이다. `RGTI`는 `49주`, `qty_available=49`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `1511` core/research preflight를 source-of-record로 사용했고 `get_account_activities(activity_types=FILL)` 기준 same-session after-hours fills `2건`, `get_orders_open` 기준 open orders `0`건, `get_watchlists` 기준 watchlists `0`건을 유지했다. 이번 cycle은 scheduler-owned passing rows만으로 required after-hours gates를 모두 충족했고 separate budget `2/2` exhausted 상태가 unchanged라 추가 local runtime Alpaca MCP read-only 재시도 없이 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-11-1511-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-11-1451-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned account/positions reconciliation 기준 `33` positions 유지, open orders `0`건이다. `RGTI`는 `49주`, `qty_available=49`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `1451` core/research preflight를 source-of-record로 사용했고 `get_account_activities(activity_types=FILL)` 기준 same-session after-hours fills `2건`, `get_orders_open` 기준 open orders `0`건, `get_watchlists` 기준 watchlists `0`건을 유지했다. local runtime Alpaca MCP `get_clock/get_account_info/get_all_positions/get_orders/get_account_activities/get_watchlists/get_order_by_client_id` 재시도는 `gap_category=dns`로 실패했지만, required after-hours rows는 scheduler-owned preflight에서 모두 충족돼 separate budget `2/2` exhausted no-submit 결론은 unchanged였다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-11-1451-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-11-1431-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime account/positions reconciliation 기준 `33` positions 유지, open orders `0`건이다. `RGTI`는 `49주`, `qty_available=49`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `1431` core/research preflight를 source-of-record로 사용했고 runtime Alpaca MCP `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-10T20:00:00Z)/get_account_activities(activity_types=FILL, after=2026-06-10T20:00:00Z)/get_watchlists/get_order_by_client_id(ah-20260611-0951-sell-rgti)/get_order_by_client_id(ah-20260611-1011-sell-rgti)`로 장외 session budget과 prior client-order lifecycle를 재확인했다. same-session after-hours fills는 여전히 `2건`이었고 separate budget `2/2`가 유지돼 이번 `1431` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-11-1431-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-11-1411-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime account/positions reconciliation 기준 `33` positions 유지, open orders `0`건이다. `RGTI`는 `49주`, `qty_available=49`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `1411` core/research preflight를 source-of-record로 사용했고 runtime Alpaca MCP `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-10T20:00:00Z)/get_account_activities(activity_types=FILL, after=2026-06-10T20:00:00Z)/get_watchlists/get_order_by_client_id(ah-20260611-0951-sell-rgti)/get_order_by_client_id(ah-20260611-1011-sell-rgti)`로 장외 session budget과 prior client-order lifecycle를 재확인했다. same-session after-hours fills는 여전히 `2건`이었고 separate budget `2/2`가 유지돼 이번 `1411` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-11-1411-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-11-1351-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime account/positions reconciliation 기준 `33` positions 유지, open orders `0`건이다. `RGTI`는 `49주`, `qty_available=49`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `1351` core/research preflight를 source-of-record로 사용했고 runtime Alpaca MCP `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-10T20:00:00Z)/get_account_activities(activity_types=FILL, after=2026-06-10T20:00:00Z)/get_watchlists/get_order_by_client_id(ah-20260611-0951-sell-rgti)/get_order_by_client_id(ah-20260611-1011-sell-rgti)`로 장외 session budget과 prior client-order lifecycle를 재확인했다. same-session after-hours fills는 여전히 `2건`이었고 separate budget `2/2`가 유지돼 이번 `1351` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-11-1351-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-11-1331-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime account/positions reconciliation 기준 `33` positions 유지, open orders `0`건이다. `RGTI`는 `49주`, `qty_available=49`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `1331` core/research preflight를 source-of-record로 사용했고 runtime Alpaca MCP `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-10T20:00:00Z)/get_account_activities(activity_types=FILL, after=2026-06-10T20:00:00Z)/get_watchlists/get_order_by_client_id(ah-20260611-0951-sell-rgti)/get_order_by_client_id(ah-20260611-1011-sell-rgti)`로 장외 session budget과 prior client-order lifecycle를 재확인했다. same-session after-hours fills는 여전히 `2건`이었고 separate budget `2/2`가 유지돼 이번 `1331` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-11-1331-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-11-1311-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime account/positions reconciliation 기준 `33` positions 유지, open orders `0`건이다. `RGTI`는 `49주`, `qty_available=49`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `1311` core/research preflight를 source-of-record로 사용했고 runtime Alpaca MCP `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-10T20:00:00Z)/get_account_activities(activity_types=FILL, after=2026-06-10T20:00:00Z)/get_watchlists/get_order_by_client_id(ah-20260611-0951-sell-rgti)/get_order_by_client_id(ah-20260611-1011-sell-rgti)`로 장외 session budget과 prior client-order lifecycle를 재확인했다. same-session after-hours fills는 여전히 `2건`이었고 separate budget `2/2`가 유지돼 이번 `1311` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-11-1311-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-11-1251-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime account/positions reconciliation 기준 `33` positions 유지, open orders `0`건이다. `RGTI`는 `49주`, `qty_available=49`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `1251` core/research preflight를 source-of-record로 사용했고 runtime Alpaca MCP `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-10T20:00:00Z)/get_account_activities(activity_types=FILL, after=2026-06-10T20:00:00Z)/get_watchlists/get_order_by_client_id(ah-20260611-0951-sell-rgti)/get_order_by_client_id(ah-20260611-1011-sell-rgti)`로 장외 session budget과 prior client-order lifecycle를 재확인했다. same-session after-hours fills는 여전히 `2건`이었고 separate budget `2/2`가 유지돼 이번 `1251` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-11-1251-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-11-1231-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime account/positions reconciliation 기준 `33` positions 유지, open orders `0`건이다. `RGTI`는 `49주`, `qty_available=49`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `1231` core/research preflight를 source-of-record로 사용했고 runtime Alpaca MCP `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-10T20:00:00Z)/get_account_activities(activity_types=FILL, after=2026-06-10T20:00:00Z)/get_watchlists/get_order_by_client_id(ah-20260611-0951-sell-rgti)/get_order_by_client_id(ah-20260611-1011-sell-rgti)`로 장외 session budget과 prior client-order lifecycle를 재확인했다. same-session after-hours fills는 여전히 `2건`이었고 separate budget `2/2`가 유지돼 이번 `1231` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-11-1231-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-11-1211-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime account/positions reconciliation 기준 `33` positions 유지, open orders `0`건이다. `RGTI`는 `49주`, `qty_available=49`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `1211` core/research preflight를 source-of-record로 사용했고 runtime Alpaca MCP `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-10T20:00:00Z)/get_watchlists/get_order_by_client_id(ah-20260611-0951-sell-rgti)/get_order_by_client_id(ah-20260611-1011-sell-rgti)`로 장외 session budget과 prior client-order lifecycle를 재확인했다. same-session after-hours fills는 여전히 `2건`이었고 separate budget `2/2`가 유지돼 이번 `1211` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-11-1211-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-11-1151-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime account/positions reconciliation 기준 `33` positions 유지, open orders `0`건이다. `RGTI`는 `49주`, `qty_available=49`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `1151` core/research preflight를 source-of-record로 사용했고 runtime Alpaca MCP `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-10T20:00:00Z)/get_watchlists/get_order_by_client_id(ah-20260611-0951-sell-rgti)/get_order_by_client_id(ah-20260611-1011-sell-rgti)`로 장외 session budget과 prior client-order lifecycle를 재확인했다. same-session after-hours fills는 여전히 `2건`이었고 separate budget `2/2`가 유지돼 이번 `1151` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-11-1151-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-11-1131-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime account/positions reconciliation 기준 `33` positions 유지, open orders `0`건이다. `RGTI`는 `49주`, `qty_available=49`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `1131` core/research preflight를 source-of-record로 사용했고 runtime Alpaca MCP `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-10T20:00:00Z)/get_watchlists/get_order_by_client_id(ah-20260611-0951-sell-rgti)/get_order_by_client_id(ah-20260611-1011-sell-rgti)`로 장외 session budget과 prior client-order lifecycle를 재확인했다. same-session after-hours fills는 여전히 `2건`이었고 separate budget `2/2`가 유지돼 이번 `1131` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-11-1131-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-11-1111-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime account/positions reconciliation 기준 `33` positions 유지, open orders `0`건이다. `RGTI`는 `49주`, `qty_available=49`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `1111` core/research preflight를 source-of-record로 사용했고 runtime Alpaca MCP `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-10T20:00:00Z)/get_watchlists/get_order_by_client_id(ah-20260611-0951-sell-rgti)/get_order_by_client_id(ah-20260611-1011-sell-rgti)`로 장외 session budget과 prior client-order lifecycle를 재확인했다. same-session after-hours fills는 여전히 `2건`이었고 separate budget `2/2`가 유지돼 이번 `1111` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-11-1111-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-11-1051-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime account/positions reconciliation 기준 `33` positions 유지, open orders `0`건이다. `RGTI`는 `49주`, `qty_available=49`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `1051` core/research preflight를 source-of-record로 사용했고 runtime Alpaca MCP `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-10T20:00:00Z)/get_watchlists/get_order_by_client_id(ah-20260611-0951-sell-rgti)/get_order_by_client_id(ah-20260611-1011-sell-rgti)`로 장외 session budget과 prior client-order lifecycle를 재확인했다. same-session after-hours fills는 여전히 `2건`이었고 separate budget `2/2`가 유지돼 이번 `1051` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-11-1051-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-11-1031-after-hours-autopilot]]
- Open/new: 없음
- Filled: `RGTI` sell 1주 @ `19.78 USD` (`ah-20260611-1011-sell-rgti` prior open order fill 확인)
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime account/positions reconciliation 기준 `33` positions 유지, open orders `0`건이다. `RGTI`는 `50주 -> 49주`, `qty_available=49`로 감소했다.
- Recent reconciliation scope: scheduler-owned `1031` core/research preflight를 source-of-record로 사용했고 runtime Alpaca MCP `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-10T20:00:00Z)/get_watchlists/get_order_by_client_id(ah-20260611-0951-sell-rgti)/get_order_by_client_id(ah-20260611-1011-sell-rgti)`로 장외 session budget과 prior client-order lifecycle를 재확인했다. `ah-20260611-1011-sell-rgti`는 `2026-06-11T01:20:06.981355496Z`에 `19.78 USD`로 체결된 상태였고 same-session after-hours fills가 `2건`이 되어 separate budget `2/2`가 닫혀 이번 `1031` cycle은 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-11-1031-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-11-1011-after-hours-autopilot]]
- Open/new: `RGTI` sell 1주 @ `19.77 USD` (`status=new`)
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime account/positions reconciliation 기준 `33` positions 유지, open orders `1`건이다. `RGTI`는 총 `50주`로 unchanged이며 `qty_available=49`로 1주가 open sell order에 예약됐다.
- Recent reconciliation scope: scheduler-owned `1011` core/research preflight를 source-of-record로 사용했고 runtime Alpaca MCP `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-10T20:00:00Z)/get_watchlists/get_stock_latest_quote(feed=overnight)/get_stock_snapshot(feed=overnight)/place_stock_order/get_order_by_client_id`로 장외 submit boundary를 재확인했다. submit 직전 `AVGO` spread가 다시 cap을 넘겨 탈락했고 `RGTI`가 fresh overnight quote `19.77/19.78`와 residual speculative trim rationale를 충족해 `client_order_id=ah-20260611-1011-sell-rgti` 1주 sell이 제출됐다. same client id reconciliation 기준 주문은 아직 `status=new` open order이며 fill은 없었다.
- Orders submitted/replaced/cancelled/closed by this workflow: 1 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-11-1011-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-11-0951-after-hours-autopilot]]
- Open/new: 없음
- Filled: `RGTI` sell 1주 @ `19.50 USD`
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime account/positions reconciliation 기준 `33` positions 유지, open orders `0`건 유지. `RGTI`는 `51주 -> 50주`, `avg_entry_price=25.569583`, `qty_available=50`로 감소했다.
- Recent reconciliation scope: scheduler-owned `0951` core/research preflight를 source-of-record로 사용했고 runtime Alpaca MCP `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-10T20:00:00Z)/get_account_activities(activity_types=FILL, after=2026-06-10T20:00:00Z)/get_watchlists/get_stock_latest_quote(feed=overnight)/get_stock_snapshot(feed=overnight)`로 장외 submit boundary를 재확인했다. `RGTI`는 fresh overnight quote `19.47/19.48`와 speculative residual monitor trim rationale를 충족해 `client_order_id=ah-20260611-0951-sell-rgti` 1주 sell이 제출됐고, same client id reconciliation 기준 `filled_avg_price=19.50 USD`로 즉시 체결됐다.
- Orders submitted/replaced/cancelled/closed by this workflow: 1 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-11-0951-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-11-0931-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `0931` core preflight와 runtime account/positions reconciliation 기준 `33` positions 유지, open orders `0`건 유지.
- Recent reconciliation scope: scheduler-owned `0931` core/research preflight를 source-of-record로 사용했고 runtime Alpaca MCP `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-10T20:00:00Z)/get_account_activities(activity_types=FILL, after=2026-06-10T20:00:00Z)/get_watchlists/get_stock_latest_quote(feed=overnight)`로 장외 submit boundary를 재확인했다. `ORCL`은 fresh overnight quote `181.28/181.51`로 다시 executable buy fallback까지 올라왔지만 `review_backlog_pending_1d_count=14` 때문에 `check-risk-policy.py`가 신규 buy 슬롯을 `0`으로 계산했고, `AVGO/RGTI/SO` sell-first 재평가는 spread 또는 stale/two-sided quote 문제로 막혔다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-11-0931-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-11-0911-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime account/positions reconciliation 기준 `33` positions 유지, open orders `0`건 유지.
- Recent reconciliation scope: scheduler-owned `0911` core/research preflight를 source-of-record로 사용했고 runtime Alpaca MCP `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-10T20:00:00Z)/get_account_activities(activity_types=FILL, after=2026-06-10T20:00:00Z)/get_watchlists/get_stock_latest_quote(feed=overnight)`로 장외 submit boundary를 재확인했다. `ORCL`은 fresh overnight quote `181.15/181.50`로 executable buy fallback까지 올라왔지만 `review_backlog_pending_1d_count=14` 때문에 `check-risk-policy.py`가 신규 buy 슬롯을 `0`으로 계산했고, `AVGO/RGTI/SO` sell-first 재평가는 spread 또는 two-sided quote 문제로 막혔다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-11-0911-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-11-0851-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `0851` core preflight 기준 `33` positions 유지, open orders `0`건 유지.
- Recent reconciliation scope: scheduler-owned `0851` core/research preflight를 source-of-record로 사용했고 runtime Alpaca MCP `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-10T20:00:00Z)/get_account_activities(activity_types=FILL, after=2026-06-10T20:00:00Z)/get_watchlists/get_stock_latest_quote(feed=iex)/get_stock_latest_quote(feed=overnight)/get_stock_snapshot(feed=overnight)`로 장외 submit boundary를 재확인했다. `SPY/QQQ/NOK`는 spread는 정책 cap 이내였지만 모두 freshness cap을 넘겼고 `SPY/QQQ`는 per-order cap도 초과했다. `AVGO/RGTI/SO` sell-first 재평가 역시 stale/wide-spread 또는 bid-only quote 때문에 executable extended-hours sell로 전환되지 못했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-11-0851-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-11-0831-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `0831` core preflight 기준 `33` positions 유지, open orders `0`건 유지.
- Recent reconciliation scope: scheduler-owned `0831` core/research preflight를 source-of-record로 사용했고 runtime Alpaca MCP `get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-10T20:00:00Z)/get_account_activities(activity_types=FILL, after=2026-06-10T20:00:00Z)/get_watchlists/get_stock_latest_quote(feed=iex)/get_stock_latest_quote(feed=overnight)/get_stock_snapshot(feed=overnight)`로 장외 submit boundary를 재확인했다. `SPY/QQQ/NOK`는 spread는 정책 cap 이내였지만 모두 freshness cap을 넘겼고 `SPY/QQQ`는 per-order cap도 초과했다. `AVGO/RGTI/SO` sell-first 재평가 역시 stale/wide-spread 또는 bid-only quote 때문에 executable extended-hours sell로 전환되지 못했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-11-0831-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-11-0811-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `0811` core preflight 기준 `33` positions 유지, open orders `0`건 유지.
- Recent reconciliation scope: scheduler-owned `0811` core/research preflight를 source-of-record로 사용했고 runtime Alpaca MCP `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-10T20:00:00Z)/get_watchlists/get_stock_latest_quote(feed=iex)/get_stock_latest_quote(feed=overnight)`로 장외 submit boundary를 재확인했다. `SPY/QQQ/NOK`는 spread는 정책 cap 이내였지만 모두 freshness cap을 넘겼고 `SPY/QQQ`는 per-order cap도 초과했다. `AVGO/RGTI/SO` sell-first 재평가 역시 stale/wide-spread 또는 bid-only quote 때문에 executable extended-hours sell로 전환되지 못했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-11-0811-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-11-0751-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `0751` core preflight 기준 `33` positions 유지, open orders `0`건 유지.
- Recent reconciliation scope: scheduler-owned `0751` core/research preflight를 source-of-record로 사용했고 runtime Alpaca MCP `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-10T20:00:00Z)/get_account_activities(activity_types=FILL, after=2026-06-10T20:00:00Z)/get_watchlists/get_stock_latest_quote(feed=iex)/get_stock_latest_quote(feed=overnight)`로 장외 submit boundary를 재확인했다. `SPY/QQQ/NOK`는 spread는 정책 cap 이내였지만 모두 freshness cap을 넘겼고 `SPY/QQQ`는 per-order cap도 초과했다. `AVGO/RGTI/SO` sell-first 재평가 역시 stale/wide-spread 또는 bid-only quote 때문에 executable extended-hours sell로 전환되지 못했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-11-0751-after-hours-autopilot-post-trade.json`

## 최신 after-hours-autopilot reconciliation

- Run: [[2026-06-11-0731-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `0731` core preflight 기준 `33` positions 유지, open orders `0`건 유지.
- Recent reconciliation scope: scheduler-owned `0731` Alpaca core/research preflight를 source-of-record로 사용했고 runtime Alpaca MCP `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-10T20:00:00Z)/get_account_activities(activity_types=FILL, after=2026-06-10T20:00:00Z)/get_watchlists/get_stock_latest_quote(feed=iex)/get_stock_latest_quote(feed=overnight)`로 장외 submit boundary를 재확인했다. `SPY/QQQ/NOK`는 spread는 정책 cap 이내였지만 모두 freshness cap을 넘겼고 `SPY/QQQ`는 per-order cap도 초과했다. `AVGO/RGTI/SO` sell-first 재평가 역시 stale/wide-spread 또는 bid-only quote 때문에 executable extended-hours sell로 전환되지 못했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-11-0731-after-hours-autopilot-post-trade.json`

## 직전 after-hours-autopilot reconciliation

- Run: [[2026-06-11-0711-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `0711` core preflight 기준 `33` positions 유지, open orders `0`건 유지.
- Recent reconciliation scope: scheduler-owned `0711` Alpaca core/research preflight를 source-of-record로 사용했고 runtime Alpaca MCP `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-10T20:00:00Z)/get_watchlists`로 장외 submit boundary를 재확인했다. `SPY/QQQ/NOK`는 spread는 정책 cap 이내였지만 모두 freshness cap을 넘겼고 `SPY/QQQ`는 per-order cap도 초과했다. `AVGO/RGTI/SO` sell-first 재평가 역시 stale/wide-spread 또는 bid-only quote 때문에 executable extended-hours sell로 전환되지 못했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-11-0711-after-hours-autopilot-post-trade.json`

## 직전 after-hours-autopilot reconciliation

- Run: [[2026-06-11-0651-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `0651` core preflight 기준 `33` positions 유지, open orders `0`건 유지.
- Recent reconciliation scope: scheduler-owned `0651` Alpaca core/research preflight를 source-of-record로 사용했고 runtime Alpaca MCP `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-10T20:00:00Z)/get_account_activities(activity_types=FILL, after=2026-06-10T20:00:00Z)/get_watchlists/get_stock_latest_quote(feed=iex)/get_stock_latest_quote(feed=overnight)`로 장외 submit boundary를 재확인했다. `SPY/QQQ/NOK`는 spread는 정책 cap 이내였지만 모두 freshness cap을 넘겼고 `SPY/QQQ`는 per-order cap도 초과했다. `AVGO/RGTI/SO` sell-first 재평가 역시 stale/wide-spread 또는 bid-only quote 때문에 executable extended-hours sell로 전환되지 못했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-11-0651-after-hours-autopilot-post-trade.json`

## 직전 after-hours-autopilot reconciliation

- Run: [[2026-06-11-0631-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `0631` core preflight 기준 `33` positions 유지, open orders `0`건 유지.
- Recent reconciliation scope: scheduler-owned `0631` Alpaca core/research preflight를 source-of-record로 사용했고 runtime Alpaca MCP `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-10T20:00:00Z)/get_account_activities(activity_types=FILL, after=2026-06-10T20:00:00Z)/get_watchlists/get_stock_latest_quote(feed=iex)/get_stock_latest_quote(feed=overnight)`로 장외 submit boundary를 재확인했다. `SPY/QQQ/NOK`는 spread는 정책 cap 이내였지만 모두 freshness cap을 넘겼고 `SPY/QQQ`는 per-order cap도 초과했다. `AVGO/RGTI/SO` sell-first 재평가 역시 stale/wide-spread 또는 bid-only quote 때문에 executable extended-hours sell로 전환되지 못했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-11-0631-after-hours-autopilot-post-trade.json`

## 직전 after-hours-autopilot reconciliation

- Run: [[2026-06-11-0611-after-hours-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `0611` core preflight 기준 `33` positions 유지, open orders `0`건 유지.
- Recent reconciliation scope: scheduler-owned `0611` Alpaca core/research preflight를 source-of-record로 사용했고 runtime Alpaca MCP `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-10T20:00:00Z)/get_account_activities(activity_types=FILL, after=2026-06-10T20:00:00Z)/get_watchlists/get_stock_latest_quote(feed=iex)/get_stock_latest_quote(feed=overnight)`로 장외 submit boundary를 재확인했다. `SPY/QQQ/NOK`는 spread는 정책 cap 이내였지만 모두 freshness cap을 넘겼고 `SPY/QQQ`는 per-order cap도 초과했다. `AVGO/RGTI/SO` sell-first 재평가 역시 stale/wide-spread 또는 bid-only quote 때문에 executable extended-hours sell로 전환되지 못했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-11-0611-after-hours-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-12-0311-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned core preflight reconciliation 기준 `33` positions 유지, open orders `0`건이다. `AVGO`는 `5주`, `qty_available=5`, `RGTI`는 `49주`, `qty_available=49`, `SO`는 `5주`, `qty_available=5`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `0311` stale cleanup/core/research preflight를 source-of-record로 사용했고 scheduler-owned Alpaca core `get_clock/get_account_info/get_orders_open/get_all_positions/get_account_activities/get_stock_latest_quote/get_stock_snapshot` rows로 same-day fill discipline과 submit-boundary quote/spread를 재확인했다. same-day regular-session `AVGO` trim 1건과 after-hours `RGTI` trim fills 2건은 그대로 유지됐고, `AVGO`는 spread `1.8672%`가 policy cap을 크게 넘겨 trim hard gate fail, `RGTI`는 duplicate sell discipline, `SO`는 spread 회복 후에도 trim metric gap, 신규 buy path는 `review_backlog_pending_1d_count=14`와 benchmark floor cap에 막혀 이번 `0311` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-0311-hourly-autopilot-post-trade.json`

- Run: [[2026-06-11-0451-hourly-autopilot]]
- Open/new: 없음
- Filled: `MSFT` buy 1주 @ `398.38 USD` (`0431` cycle open order fill observed)
- Cancelled: 없음
- Position count observed by Alpaca MCP: close-boundary reconciliation 기준 `33` positions 유지. `MSFT`는 `1주 -> 2주`, `avg_entry_price=412.58`, `qty_available=2`로 증가했고 open orders는 `0`건이다.
- Recent reconciliation scope: scheduler-owned `0451` stale cleanup/core/research preflight를 source-of-record로 사용했고, live Alpaca MCP `get_clock/get_account_info/get_orders(status=open)/get_all_positions/get_account_activities(activity_types=FILL, after=2026-06-10T19:45:00Z)`로 submit boundary close와 fill/account/order state를 재확인했다. sell-first 재평가에서는 `AVGO`가 spread `0.6118%` + same-day sell duplicate, `RGTI`가 same-day sell duplicate, `SO`가 trim metric gap으로 blocked였고, buy fallback에서는 `UNH`가 최종 후보였지만 live regular market close로 submit이 차단됐다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-11-0451-hourly-autopilot-post-trade.json`

## 직전 hourly-autopilot reconciliation

- Run: [[2026-06-11-0431-hourly-autopilot]]
- Open/new: `MSFT` buy 1주 @ `398.38 USD` (`status=new`)
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: reconciliation 기준 `33` positions 유지. `MSFT`는 아직 `1주`, `avg_entry_price=426.78`, `qty_available=1`로 unchanged이며 새 open order는 `MSFT` 1건이다.
- Recent reconciliation scope: scheduler-owned `0431` stale cleanup/core/research preflight를 source-of-record로 사용했고 submit 직후 Alpaca MCP `get_order_by_client_id`, `get_orders(status=open)`, `get_orders(status=all, symbols=MSFT, after=2026-06-10T19:30:00Z)`, `get_all_positions`, `get_account_info`로 open-order/position/account 상태를 재확인했다. sell-first 재평가에서는 `AVGO`가 spread `0.7981%` + same-day sell duplicate, `RGTI`가 same-day sell duplicate, `SO`가 trim metric gap으로 blocked였고, buy fallback에서는 `FCX/WMT/AMZN/BAC/NEE` same-day buy duplicate, `GOOGL` weak review, `NVDA` same-cluster add block, `PLTR` low confidence, `INTC` prior weak exit-thesis, `SPY/QQQ` per-order cap이 남아 `MSFT`가 선택됐다.
- Orders submitted/replaced/cancelled/closed by this workflow: 1 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-11-0431-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-12-0311-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned core preflight reconciliation 기준 `33` positions 유지, open orders `0`건이다. `AVGO`는 `5주`, `qty_available=5`, `RGTI`는 `49주`, `qty_available=49`, `SO`는 `5주`, `qty_available=5`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `0311` stale cleanup/core/research preflight를 source-of-record로 사용했고 scheduler-owned Alpaca core `get_clock/get_account_info/get_orders_open/get_all_positions/get_account_activities/get_stock_latest_quote/get_stock_snapshot` rows로 same-day fill discipline과 submit-boundary quote/spread를 재확인했다. same-day regular-session `AVGO` trim 1건과 after-hours `RGTI` trim fills 2건은 그대로 유지됐고, `AVGO`는 spread `1.8672%`가 policy cap을 크게 넘겨 trim hard gate fail, `RGTI`는 duplicate sell discipline, `SO`는 spread 회복 후에도 trim metric gap, 신규 buy path는 `review_backlog_pending_1d_count=14`와 benchmark floor cap에 막혀 이번 `0311` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-0311-hourly-autopilot-post-trade.json`

- Run: [[2026-06-11-0411-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `0411` core preflight 기준 `33` positions 유지, open orders `0`건 유지.
- Recent reconciliation scope: scheduler-owned `0411` stale cleanup/core/research preflight를 source-of-record로 사용했다. sell-first 재평가에서는 `AVGO`와 `RGTI`가 spread 정상화 이후에도 same-day sell duplicate로 blocked였고, `SO`는 trim metric gap이 유지됐다. buy fallback에서는 `FCX/WMT/SLB/NKE/NEE/COP/AMZN/XOM` same-day buy duplicate, `MCD` spread `1.2599%` + thesis evidence 부족, `GOOGL` weak review, `NVDA` same-cluster add block, `SPY/QQQ` per-order cap이 남아 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-11-0411-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-12-0311-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned core preflight reconciliation 기준 `33` positions 유지, open orders `0`건이다. `AVGO`는 `5주`, `qty_available=5`, `RGTI`는 `49주`, `qty_available=49`, `SO`는 `5주`, `qty_available=5`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `0311` stale cleanup/core/research preflight를 source-of-record로 사용했고 scheduler-owned Alpaca core `get_clock/get_account_info/get_orders_open/get_all_positions/get_account_activities/get_stock_latest_quote/get_stock_snapshot` rows로 same-day fill discipline과 submit-boundary quote/spread를 재확인했다. same-day regular-session `AVGO` trim 1건과 after-hours `RGTI` trim fills 2건은 그대로 유지됐고, `AVGO`는 spread `1.8672%`가 policy cap을 크게 넘겨 trim hard gate fail, `RGTI`는 duplicate sell discipline, `SO`는 spread 회복 후에도 trim metric gap, 신규 buy path는 `review_backlog_pending_1d_count=14`와 benchmark floor cap에 막혀 이번 `0311` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-0311-hourly-autopilot-post-trade.json`

- Run: [[2026-06-11-0351-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `0351` core preflight 기준 `33` positions 유지, open orders `0`건 유지.
- Recent reconciliation scope: scheduler-owned `0351` stale cleanup/core/research preflight를 source-of-record로 사용했다. sell-first 재평가에서는 `AVGO`가 live spread `0.6425%`로 trim hard gate fail, `RGTI`가 same-day sell duplicate, `SO`가 trim metric gap으로 blocked였다. buy fallback에서는 `FCX/WMT/SLB/NKE/NEE/COP/AMZN` same-day buy duplicate, `XOM` duplicate+spread fail, `MCD` thesis evidence 부족, `GOOGL` weak review, `NVDA` same-cluster add block, `SPY/QQQ` per-order cap이 남아 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-11-0351-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-12-0311-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned core preflight reconciliation 기준 `33` positions 유지, open orders `0`건이다. `AVGO`는 `5주`, `qty_available=5`, `RGTI`는 `49주`, `qty_available=49`, `SO`는 `5주`, `qty_available=5`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `0311` stale cleanup/core/research preflight를 source-of-record로 사용했고 scheduler-owned Alpaca core `get_clock/get_account_info/get_orders_open/get_all_positions/get_account_activities/get_stock_latest_quote/get_stock_snapshot` rows로 same-day fill discipline과 submit-boundary quote/spread를 재확인했다. same-day regular-session `AVGO` trim 1건과 after-hours `RGTI` trim fills 2건은 그대로 유지됐고, `AVGO`는 spread `1.8672%`가 policy cap을 크게 넘겨 trim hard gate fail, `RGTI`는 duplicate sell discipline, `SO`는 spread 회복 후에도 trim metric gap, 신규 buy path는 `review_backlog_pending_1d_count=14`와 benchmark floor cap에 막혀 이번 `0311` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-0311-hourly-autopilot-post-trade.json`

- Run: [[2026-06-11-0331-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `0331` core preflight 기준 `33` positions 유지, open orders `0`건 유지.
- Recent reconciliation scope: scheduler-owned `0331` stale cleanup/core/research preflight를 source-of-record로 사용했다. sell-first 재평가에서는 `AVGO`가 live spread `1.9201%`로 trim hard gate fail, `RGTI`가 same-day sell duplicate, `SO`가 trim metric gap으로 blocked였다. buy fallback에서는 `FCX/WMT/SLB/NKE/NEE/COP/AMZN` same-day buy duplicate, `XOM` duplicate+spread fail, `GOOGL` weak review, `NVDA` same-cluster add block, `SPY/QQQ` per-order cap이 남아 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-11-0331-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-12-0311-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned core preflight reconciliation 기준 `33` positions 유지, open orders `0`건이다. `AVGO`는 `5주`, `qty_available=5`, `RGTI`는 `49주`, `qty_available=49`, `SO`는 `5주`, `qty_available=5`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `0311` stale cleanup/core/research preflight를 source-of-record로 사용했고 scheduler-owned Alpaca core `get_clock/get_account_info/get_orders_open/get_all_positions/get_account_activities/get_stock_latest_quote/get_stock_snapshot` rows로 same-day fill discipline과 submit-boundary quote/spread를 재확인했다. same-day regular-session `AVGO` trim 1건과 after-hours `RGTI` trim fills 2건은 그대로 유지됐고, `AVGO`는 spread `1.8672%`가 policy cap을 크게 넘겨 trim hard gate fail, `RGTI`는 duplicate sell discipline, `SO`는 spread 회복 후에도 trim metric gap, 신규 buy path는 `review_backlog_pending_1d_count=14`와 benchmark floor cap에 막혀 이번 `0311` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-0311-hourly-autopilot-post-trade.json`

- Run: [[2026-06-11-0311-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `0311` core preflight 기준 `33` positions 유지, open orders `0`건 유지.
- Recent reconciliation scope: scheduler-owned `0311` stale cleanup/core/research preflight를 source-of-record로 사용했다. sell-first 재평가에서는 `AVGO`와 `RGTI`가 모두 spread는 정상 범위였지만 `2026-06-10 ET` same-day sell duplicate로 blocked였고, `SO`는 trim metric gap이 유지됐다. buy fallback에서는 `FCX/WMT/SLB/XOM/NKE/NEE/COP/AMZN` same-day buy duplicate, `GOOGL` weak review, `NVDA` same-cluster add block, `SPY/QQQ` per-order cap이 남아 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-11-0311-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-12-0311-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned core preflight reconciliation 기준 `33` positions 유지, open orders `0`건이다. `AVGO`는 `5주`, `qty_available=5`, `RGTI`는 `49주`, `qty_available=49`, `SO`는 `5주`, `qty_available=5`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `0311` stale cleanup/core/research preflight를 source-of-record로 사용했고 scheduler-owned Alpaca core `get_clock/get_account_info/get_orders_open/get_all_positions/get_account_activities/get_stock_latest_quote/get_stock_snapshot` rows로 same-day fill discipline과 submit-boundary quote/spread를 재확인했다. same-day regular-session `AVGO` trim 1건과 after-hours `RGTI` trim fills 2건은 그대로 유지됐고, `AVGO`는 spread `1.8672%`가 policy cap을 크게 넘겨 trim hard gate fail, `RGTI`는 duplicate sell discipline, `SO`는 spread 회복 후에도 trim metric gap, 신규 buy path는 `review_backlog_pending_1d_count=14`와 benchmark floor cap에 막혀 이번 `0311` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-0311-hourly-autopilot-post-trade.json`

- Run: [[2026-06-11-0251-hourly-autopilot]]
- Open/new: 없음
- Filled: `NKE` buy 1주 @ `43.98 USD`
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `0251` core preflight 기준 `33` positions 유지. `NKE`는 `4주 -> 5주`, `avg_entry_price=45.202`, `qty_available=5`로 증가했고 open orders는 `0`건이다.
- Recent reconciliation scope: scheduler-owned `0251` stale cleanup/core/research preflight를 source-of-record로 사용했다. stale cleanup과 core preflight open-order row 모두 `0`건이었고, `hourly-20260611-0231-buy-nke`는 `2026-06-10T17:44:44.080648Z`에 `43.98 USD`로 체결된 것이 recent fills에 반영됐다. sell-first 재평가에서는 `AVGO`가 spread fail과 same-day sell duplicate, `RGTI`가 same-day sell duplicate, `SO`가 trim metric gap으로 blocked였고, buy fallback에서는 `NKE/NEE/FCX/AMZN/SLB/COP/JNJ/XOM/PFE/BAC/WMT/AAPL` same-day buy duplicate, `SPY/QQQ` per-order cap, `NOK` add-block, `INTC` recent weak exit-thesis가 남아 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-11-0251-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-12-0311-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned core preflight reconciliation 기준 `33` positions 유지, open orders `0`건이다. `AVGO`는 `5주`, `qty_available=5`, `RGTI`는 `49주`, `qty_available=49`, `SO`는 `5주`, `qty_available=5`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `0311` stale cleanup/core/research preflight를 source-of-record로 사용했고 scheduler-owned Alpaca core `get_clock/get_account_info/get_orders_open/get_all_positions/get_account_activities/get_stock_latest_quote/get_stock_snapshot` rows로 same-day fill discipline과 submit-boundary quote/spread를 재확인했다. same-day regular-session `AVGO` trim 1건과 after-hours `RGTI` trim fills 2건은 그대로 유지됐고, `AVGO`는 spread `1.8672%`가 policy cap을 크게 넘겨 trim hard gate fail, `RGTI`는 duplicate sell discipline, `SO`는 spread 회복 후에도 trim metric gap, 신규 buy path는 `review_backlog_pending_1d_count=14`와 benchmark floor cap에 막혀 이번 `0311` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-0311-hourly-autopilot-post-trade.json`

- Run: [[2026-06-11-0231-hourly-autopilot]]
- Open/new: `NKE` buy 1주 @ `43.99 USD` (`status=new`)
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime `get_all_positions` 기준 `33` positions 유지. `NKE`는 아직 `4주`, `avg_entry_price=45.5075`, `qty_available=4`로 unchanged이며 새 open order는 `NKE` 1건이다.
- Recent reconciliation scope: scheduler-owned `0231` stale cleanup/core/research preflight를 우선 사용했고, workflow 계약상 비어 있던 Alpaca core preflight tool row는 live Alpaca MCP `get_clock/get_account_info/get_orders(status=open)/get_all_positions/get_account_activities(activity_types=FILL, after=2026-06-10)/get_watchlists/get_stock_latest_quote(feed=iex)/get_asset(NKE)`로 보강했다. submit 직전 regular market open, ACTIVE account, open orders 0건, same-day fills `NEE/FCX/AMZN/SLB/COP/JNJ/XOM/PFE/BAC/RGTI/AVGO/WMT/AAPL/AAPL`, `NKE` quote `43.98/43.99`, active tradable NYSE stock을 재확인했다. sell-first 재평가에서는 `AVGO`가 spread fail과 same-day sell duplicate, `RGTI`가 same-day sell duplicate, `SO`가 trim metric gap으로 blocked였고, buy fallback에서는 `NEE/FCX/AMZN/SLB/COP/JNJ/XOM/PFE/BAC/WMT/AAPL` same-day buy duplicate, `SPY/QQQ` per-order cap, `CVX` spread fail이 남았다. `NKE`는 preflight-covered consumer diversifier floor-size buy로 선택됐고 direct Alpaca MCP submit 뒤 same order id reconciliation 기준 `order_id=9b08f07e-f93e-47d6-b1d1-5d707abec8eb`, `status=new`, `filled_qty=0` open order다.
- Orders submitted/replaced/cancelled/closed by this workflow: 1 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-11-0231-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-12-0311-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned core preflight reconciliation 기준 `33` positions 유지, open orders `0`건이다. `AVGO`는 `5주`, `qty_available=5`, `RGTI`는 `49주`, `qty_available=49`, `SO`는 `5주`, `qty_available=5`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `0311` stale cleanup/core/research preflight를 source-of-record로 사용했고 scheduler-owned Alpaca core `get_clock/get_account_info/get_orders_open/get_all_positions/get_account_activities/get_stock_latest_quote/get_stock_snapshot` rows로 same-day fill discipline과 submit-boundary quote/spread를 재확인했다. same-day regular-session `AVGO` trim 1건과 after-hours `RGTI` trim fills 2건은 그대로 유지됐고, `AVGO`는 spread `1.8672%`가 policy cap을 크게 넘겨 trim hard gate fail, `RGTI`는 duplicate sell discipline, `SO`는 spread 회복 후에도 trim metric gap, 신규 buy path는 `review_backlog_pending_1d_count=14`와 benchmark floor cap에 막혀 이번 `0311` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-0311-hourly-autopilot-post-trade.json`

- Run: [[2026-06-11-0211-hourly-autopilot]]
- Open/new: 없음
- Filled: `NEE` buy 1주 @ `85.22 USD`
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime `get_all_positions` 기준 `33` positions 유지. `NEE`는 `4주 -> 5주`, `avg_entry_price=86.44`, `qty_available=5`로 증가했다.
- Recent reconciliation scope: scheduler-owned `0211` stale cleanup/core/research preflight를 우선 사용했고 live Alpaca MCP submit-boundary check에서 regular market open, ACTIVE account, open orders 0건, same-day fills `FCX/AMZN/SLB/COP/JNJ/XOM/PFE/BAC/RGTI/AVGO/WMT/AAPL/AAPL`, `NEE` quote `85.27/85.29`, active tradable NYSE stock을 재확인했다. sell-first 재평가에서는 `AVGO`가 spread fail과 same-day sell duplicate, `RGTI`가 same-day sell duplicate, `SO`가 trim metric gap으로 blocked였고, buy fallback에서는 `FCX/AMZN/SLB/COP/JNJ/XOM/PFE/BAC/WMT/AAPL` same-day buy duplicate, `SPY/QQQ` per-order cap, `CVX/MCD` spread fail, `HOOD` thesis evidence 부족이 남았다. `NEE`는 FRED-confirmed utilities diversifier floor-size buy로 선택됐고 direct Alpaca MCP submit 뒤 same order/client id reconciliation 기준 `order_id=7fd2a9cf-bde9-454e-83f0-64a8a722409d`, `filled_avg_price=85.22 USD`로 즉시 전량 체결됐다.
- Orders submitted/replaced/cancelled/closed by this workflow: 1 / 0 / 0 / 1.
- Source note: `wiki/trade-ledger/positions/2026-06-11-0211-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-12-0311-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned core preflight reconciliation 기준 `33` positions 유지, open orders `0`건이다. `AVGO`는 `5주`, `qty_available=5`, `RGTI`는 `49주`, `qty_available=49`, `SO`는 `5주`, `qty_available=5`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `0311` stale cleanup/core/research preflight를 source-of-record로 사용했고 scheduler-owned Alpaca core `get_clock/get_account_info/get_orders_open/get_all_positions/get_account_activities/get_stock_latest_quote/get_stock_snapshot` rows로 same-day fill discipline과 submit-boundary quote/spread를 재확인했다. same-day regular-session `AVGO` trim 1건과 after-hours `RGTI` trim fills 2건은 그대로 유지됐고, `AVGO`는 spread `1.8672%`가 policy cap을 크게 넘겨 trim hard gate fail, `RGTI`는 duplicate sell discipline, `SO`는 spread 회복 후에도 trim metric gap, 신규 buy path는 `review_backlog_pending_1d_count=14`와 benchmark floor cap에 막혀 이번 `0311` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-0311-hourly-autopilot-post-trade.json`

- Run: [[2026-06-11-0151-hourly-autopilot]]
- Open/new: 없음
- Filled: `FCX` buy 1주 @ `62.21 USD`
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime `get_all_positions` 기준 `33` positions 유지. `FCX`는 `4주 -> 5주`, `avg_entry_price=64.912`, `qty_available=5`로 증가했다.
- Recent reconciliation scope: scheduler-owned `0151` stale cleanup/core/research preflight를 우선 사용했고 live Alpaca MCP submit-boundary check에서 regular market open, ACTIVE account, open orders 0건, same-day fills `AMZN/SLB/COP/JNJ/XOM/PFE/BAC/RGTI/AVGO/WMT/AAPL/AAPL`, `FCX` quote `62.19/62.22`, active tradable NYSE stock을 재확인했다. sell-first 재평가에서는 `AVGO`가 spread fail과 same-day sell duplicate, `RGTI`가 same-day sell duplicate, `SO`가 trim metric gap으로 blocked였고, `SPY/QQQ`는 per-order cap, `AAPL/BAC/WMT/SLB/AMZN`은 same-day buy duplicate가 남았다. `FCX`는 preflight-covered materials/mining diversifier floor-size buy로 선택됐고 direct Alpaca MCP submit 뒤 same order/client id reconciliation 기준 `order_id=dc2dd11d-89ef-4664-a300-65a801ee30e7`, `filled_avg_price=62.21 USD`로 즉시 전량 체결됐다.
- Orders submitted/replaced/cancelled/closed by this workflow: 1 / 0 / 0 / 1.
- Source note: `wiki/trade-ledger/positions/2026-06-11-0151-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-12-0311-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned core preflight reconciliation 기준 `33` positions 유지, open orders `0`건이다. `AVGO`는 `5주`, `qty_available=5`, `RGTI`는 `49주`, `qty_available=49`, `SO`는 `5주`, `qty_available=5`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `0311` stale cleanup/core/research preflight를 source-of-record로 사용했고 scheduler-owned Alpaca core `get_clock/get_account_info/get_orders_open/get_all_positions/get_account_activities/get_stock_latest_quote/get_stock_snapshot` rows로 same-day fill discipline과 submit-boundary quote/spread를 재확인했다. same-day regular-session `AVGO` trim 1건과 after-hours `RGTI` trim fills 2건은 그대로 유지됐고, `AVGO`는 spread `1.8672%`가 policy cap을 크게 넘겨 trim hard gate fail, `RGTI`는 duplicate sell discipline, `SO`는 spread 회복 후에도 trim metric gap, 신규 buy path는 `review_backlog_pending_1d_count=14`와 benchmark floor cap에 막혀 이번 `0311` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-0311-hourly-autopilot-post-trade.json`

- Run: [[2026-06-11-0131-hourly-autopilot]]
- Open/new: `AMZN` buy 1주 @ `239.33 USD` (`status=new`)
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime `get_all_positions` 기준 `33` positions 유지. `AMZN`은 아직 `5주`, `avg_entry_price=262.386`, `qty_available=5`로 unchanged이며 새 open order는 `AMZN` 1건이다.
- Recent reconciliation scope: scheduler-owned `0131` stale cleanup/core/research preflight를 우선 사용했고 live Alpaca MCP submit-boundary check에서 regular market open, ACTIVE account, open orders 0건, same-day fills `SLB/COP/JNJ/XOM/PFE/BAC/RGTI/AVGO/WMT/AAPL/AAPL`, `AMZN` quote `239.00/239.33`, active tradable NASDAQ stock을 재확인했다. sell-first 재평가에서는 `AVGO`와 `RGTI`가 same-day sell duplicate, `SO`가 trim metric gap으로 blocked였고, `SPY/QQQ`는 per-order cap, `COP/JNJ/XOM/PFE/BAC/WMT/SLB`는 same-day buy duplicate가 남았다. `CVX`는 spread는 정상화됐지만 same-day energy sleeve buy 누적으로 different-cluster fallback보다 우선순위가 낮아졌고, `AMZN`이 research-covered mega-cap AI/cloud floor-size buy로 선택됐다. direct Alpaca MCP submit 뒤 same client/order id reconciliation 기준 `order_id=d23787d5-be1a-4b35-a08e-b43670b24265`, `status=new`, `filled_qty=0` open order다.
- Orders submitted/replaced/cancelled/closed by this workflow: 1 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-11-0131-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-12-0311-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned core preflight reconciliation 기준 `33` positions 유지, open orders `0`건이다. `AVGO`는 `5주`, `qty_available=5`, `RGTI`는 `49주`, `qty_available=49`, `SO`는 `5주`, `qty_available=5`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `0311` stale cleanup/core/research preflight를 source-of-record로 사용했고 scheduler-owned Alpaca core `get_clock/get_account_info/get_orders_open/get_all_positions/get_account_activities/get_stock_latest_quote/get_stock_snapshot` rows로 same-day fill discipline과 submit-boundary quote/spread를 재확인했다. same-day regular-session `AVGO` trim 1건과 after-hours `RGTI` trim fills 2건은 그대로 유지됐고, `AVGO`는 spread `1.8672%`가 policy cap을 크게 넘겨 trim hard gate fail, `RGTI`는 duplicate sell discipline, `SO`는 spread 회복 후에도 trim metric gap, 신규 buy path는 `review_backlog_pending_1d_count=14`와 benchmark floor cap에 막혀 이번 `0311` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-0311-hourly-autopilot-post-trade.json`

- Run: [[2026-06-11-0111-hourly-autopilot]]
- Open/new: 없음
- Filled: `SLB` buy 1주 @ `56.45 USD`
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime `get_all_positions` 기준 `33` positions 유지. `SLB`는 `5주 -> 6주`, `avg_entry_price=55.858333`, `qty_available=6`으로 증가했다.
- Recent reconciliation scope: scheduler-owned `0111` stale cleanup/core/research preflight를 우선 사용했고 live Alpaca MCP submit-boundary check에서 regular market open, ACTIVE account, open orders 0건, same-day fills `COP/JNJ/XOM/PFE/BAC/RGTI/AVGO/WMT/AAPL/AAPL`, `SLB` quote `56.54/56.55`, active tradable NYSE stock을 재확인했다. sell-first 재평가에서는 `AVGO`와 `RGTI`가 same-day sell duplicate, `SO`가 trim metric gap으로 blocked였고, `SPY/QQQ`는 per-order cap, `COP/JNJ/XOM/PFE/BAC/WMT`는 same-day buy duplicate, `CVX`는 spread fail이 남았다. `SLB`는 positive recent review를 가진 energy-services existing diversifier floor-size add로 선택됐고 direct Alpaca MCP submit 뒤 immediate same-order-id reconciliation 기준 `order_id=14d20183-5063-4025-9114-5e82cbcf6386`, `filled_avg_price=56.45 USD`로 즉시 전량 체결됐다.
- Orders submitted/replaced/cancelled/closed by this workflow: 1 / 0 / 0 / 1.
- Source note: `wiki/trade-ledger/positions/2026-06-11-0111-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-12-0311-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned core preflight reconciliation 기준 `33` positions 유지, open orders `0`건이다. `AVGO`는 `5주`, `qty_available=5`, `RGTI`는 `49주`, `qty_available=49`, `SO`는 `5주`, `qty_available=5`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `0311` stale cleanup/core/research preflight를 source-of-record로 사용했고 scheduler-owned Alpaca core `get_clock/get_account_info/get_orders_open/get_all_positions/get_account_activities/get_stock_latest_quote/get_stock_snapshot` rows로 same-day fill discipline과 submit-boundary quote/spread를 재확인했다. same-day regular-session `AVGO` trim 1건과 after-hours `RGTI` trim fills 2건은 그대로 유지됐고, `AVGO`는 spread `1.8672%`가 policy cap을 크게 넘겨 trim hard gate fail, `RGTI`는 duplicate sell discipline, `SO`는 spread 회복 후에도 trim metric gap, 신규 buy path는 `review_backlog_pending_1d_count=14`와 benchmark floor cap에 막혀 이번 `0311` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-0311-hourly-autopilot-post-trade.json`

- Run: [[2026-06-11-0051-hourly-autopilot]]
- Open/new: 없음
- Filled: `COP` buy 1주 @ `121.05 USD`
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime `get_all_positions` 기준 `33` positions 유지. `COP`는 `4주 -> 5주`, `avg_entry_price=117.728`, `qty_available=5`로 증가했다.
- Recent reconciliation scope: scheduler-owned `0051` stale cleanup/core/research preflight를 우선 사용했고 live Alpaca MCP submit-boundary check에서 regular market open, ACTIVE account, open orders 0건, same-day fills `JNJ/XOM/PFE/BAC/RGTI/AVGO/WMT/AAPL/AAPL`, `COP` quote `121.15/121.20`, active tradable NYSE stock을 재확인했다. sell-first 재평가에서는 `AVGO`와 `RGTI`가 same-day sell duplicate, `SO`가 trim metric gap으로 blocked였고, `SPY/QQQ`는 per-order cap, `BAC/PFE/WMT/XOM/JNJ`는 same-day buy duplicate가 남았다. `COP`는 positive 1D review를 가진 energy/value existing diversifier floor-size add로 선택됐고 direct Alpaca MCP submit 뒤 immediate same-order-id reconciliation 기준 `order_id=998a7e94-7e3c-4737-bdd6-2bdc37dccfea`, `filled_avg_price=121.05 USD`로 즉시 전량 체결됐다.
- Orders submitted/replaced/cancelled/closed by this workflow: 1 / 0 / 0 / 1.
- Source note: `wiki/trade-ledger/positions/2026-06-11-0051-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-12-0311-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned core preflight reconciliation 기준 `33` positions 유지, open orders `0`건이다. `AVGO`는 `5주`, `qty_available=5`, `RGTI`는 `49주`, `qty_available=49`, `SO`는 `5주`, `qty_available=5`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `0311` stale cleanup/core/research preflight를 source-of-record로 사용했고 scheduler-owned Alpaca core `get_clock/get_account_info/get_orders_open/get_all_positions/get_account_activities/get_stock_latest_quote/get_stock_snapshot` rows로 same-day fill discipline과 submit-boundary quote/spread를 재확인했다. same-day regular-session `AVGO` trim 1건과 after-hours `RGTI` trim fills 2건은 그대로 유지됐고, `AVGO`는 spread `1.8672%`가 policy cap을 크게 넘겨 trim hard gate fail, `RGTI`는 duplicate sell discipline, `SO`는 spread 회복 후에도 trim metric gap, 신규 buy path는 `review_backlog_pending_1d_count=14`와 benchmark floor cap에 막혀 이번 `0311` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-0311-hourly-autopilot-post-trade.json`

- Run: [[2026-06-11-0031-hourly-autopilot]]
- Open/new: 없음
- Filled: `JNJ` buy 1주 @ `239.23 USD`
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime `get_all_positions` 기준 `33` positions 유지. `JNJ`는 `1주 -> 2주`, `avg_entry_price=238.385`, `qty_available=2`로 증가했다.
- Recent reconciliation scope: scheduler-owned `0031` stale cleanup/core/research preflight를 우선 사용했고 live Alpaca MCP submit-boundary check에서 regular market open, ACTIVE account, open orders 0건, same-day fills `XOM/PFE/BAC/RGTI/AVGO/WMT/AAPL/AAPL`, `JNJ` live quote `239.29/239.35`를 재확인했다. sell-first 재평가에서는 `AVGO`와 `RGTI`가 same-day sell duplicate, `SO`가 trim metric gap으로 blocked였고, `SPY/QQQ`는 per-order cap, `BAC/WMT/XOM`은 same-day buy duplicate가 남았다. `JNJ`는 healthcare defensive diversifier floor-size validation buy로 선택됐고 direct Alpaca MCP submit 뒤 immediate same-order-id reconciliation 기준 `order_id=c1075d80-4584-4f06-8e39-9182570e9f19`, `filled_avg_price=239.23 USD`로 즉시 전량 체결됐다.
- Orders submitted/replaced/cancelled/closed by this workflow: 1 / 0 / 0 / 1.
- Source note: `wiki/trade-ledger/positions/2026-06-11-0031-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-12-0311-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned core preflight reconciliation 기준 `33` positions 유지, open orders `0`건이다. `AVGO`는 `5주`, `qty_available=5`, `RGTI`는 `49주`, `qty_available=49`, `SO`는 `5주`, `qty_available=5`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `0311` stale cleanup/core/research preflight를 source-of-record로 사용했고 scheduler-owned Alpaca core `get_clock/get_account_info/get_orders_open/get_all_positions/get_account_activities/get_stock_latest_quote/get_stock_snapshot` rows로 same-day fill discipline과 submit-boundary quote/spread를 재확인했다. same-day regular-session `AVGO` trim 1건과 after-hours `RGTI` trim fills 2건은 그대로 유지됐고, `AVGO`는 spread `1.8672%`가 policy cap을 크게 넘겨 trim hard gate fail, `RGTI`는 duplicate sell discipline, `SO`는 spread 회복 후에도 trim metric gap, 신규 buy path는 `review_backlog_pending_1d_count=14`와 benchmark floor cap에 막혀 이번 `0311` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-0311-hourly-autopilot-post-trade.json`

- Run: [[2026-06-11-0011-hourly-autopilot]]
- Open/new: 없음
- Filled: `XOM` buy 1주 @ `151.41 USD`
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime `get_all_positions` 기준 `33` positions 유지. `XOM`은 `4주 -> 5주`, `avg_entry_price=149.692`, `qty_available=5`로 증가했다.
- Recent reconciliation scope: scheduler-owned `0011` stale cleanup/core/research preflight를 우선 사용했고 live Alpaca MCP submit-boundary check에서 regular market open, ACTIVE account, open orders 0건, same-day fills `PFE/BAC/RGTI/AVGO/WMT/AAPL/AAPL`, `XOM` quote `151.45/151.66`를 재확인했다. sell-first 재평가에서는 `AVGO`와 `RGTI`가 same-day sell duplicate, `SO`가 trim metric gap으로 blocked였고, `SPY/QQQ`는 per-order cap, `COP`는 spread fail이 남았다. `XOM`은 existing energy diversifier floor-size validation buy로 선택됐고 direct Alpaca MCP submit 뒤 immediate same-order-id reconciliation 기준 `order_id=1878c01b-3d57-400d-a66c-b9cbbce4d237`, `filled_avg_price=151.41 USD`로 즉시 전량 체결됐다.
- Orders submitted/replaced/cancelled/closed by this workflow: 1 / 0 / 0 / 1.
- Source note: `wiki/trade-ledger/positions/2026-06-11-0011-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-12-0311-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned core preflight reconciliation 기준 `33` positions 유지, open orders `0`건이다. `AVGO`는 `5주`, `qty_available=5`, `RGTI`는 `49주`, `qty_available=49`, `SO`는 `5주`, `qty_available=5`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `0311` stale cleanup/core/research preflight를 source-of-record로 사용했고 scheduler-owned Alpaca core `get_clock/get_account_info/get_orders_open/get_all_positions/get_account_activities/get_stock_latest_quote/get_stock_snapshot` rows로 same-day fill discipline과 submit-boundary quote/spread를 재확인했다. same-day regular-session `AVGO` trim 1건과 after-hours `RGTI` trim fills 2건은 그대로 유지됐고, `AVGO`는 spread `1.8672%`가 policy cap을 크게 넘겨 trim hard gate fail, `RGTI`는 duplicate sell discipline, `SO`는 spread 회복 후에도 trim metric gap, 신규 buy path는 `review_backlog_pending_1d_count=14`와 benchmark floor cap에 막혀 이번 `0311` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-0311-hourly-autopilot-post-trade.json`

- Run: [[2026-06-10-2351-hourly-autopilot]]
- Open/new: 없음
- Filled: `PFE` buy 1주 @ `25.70 USD`
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime `get_all_positions` 기준 `33` positions 유지. `PFE`는 `5주 -> 6주`, `avg_entry_price=26.033333`, `qty_available=6`으로 증가했다.
- Recent reconciliation scope: scheduler-owned `2351` stale cleanup/core/research preflight를 우선 사용했고 live Alpaca MCP submit-boundary check에서 regular market open, ACTIVE account, open orders 0건, same-day fills `BAC/RGTI/AVGO/WMT/AAPL/AAPL`, `PFE` live quote `25.71/25.72`를 재확인했다. sell-first 재평가에서는 `RGTI`와 `AVGO`가 same-day sell duplicate, `SO`가 trim metric gap으로 blocked였고, `BAC/WMT`는 same-day buy duplicate, `SPY/QQQ`는 per-order cap을 넘었다. `PFE`는 healthcare diversifier floor-size validation buy로 선택됐고 direct Alpaca MCP submit 뒤 immediate same-order-id reconciliation 기준 `order_id=e010464f-f482-491e-bc31-76dcffb1730c`, `filled_avg_price=25.70 USD`로 즉시 전량 체결됐다.
- Orders submitted/replaced/cancelled/closed by this workflow: 1 / 0 / 0 / 1.
- Source note: `wiki/trade-ledger/positions/2026-06-10-2351-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-12-0311-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned core preflight reconciliation 기준 `33` positions 유지, open orders `0`건이다. `AVGO`는 `5주`, `qty_available=5`, `RGTI`는 `49주`, `qty_available=49`, `SO`는 `5주`, `qty_available=5`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `0311` stale cleanup/core/research preflight를 source-of-record로 사용했고 scheduler-owned Alpaca core `get_clock/get_account_info/get_orders_open/get_all_positions/get_account_activities/get_stock_latest_quote/get_stock_snapshot` rows로 same-day fill discipline과 submit-boundary quote/spread를 재확인했다. same-day regular-session `AVGO` trim 1건과 after-hours `RGTI` trim fills 2건은 그대로 유지됐고, `AVGO`는 spread `1.8672%`가 policy cap을 크게 넘겨 trim hard gate fail, `RGTI`는 duplicate sell discipline, `SO`는 spread 회복 후에도 trim metric gap, 신규 buy path는 `review_backlog_pending_1d_count=14`와 benchmark floor cap에 막혀 이번 `0311` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-0311-hourly-autopilot-post-trade.json`

- Run: [[2026-06-10-2331-hourly-autopilot]]
- Open/new: 없음
- Filled: `BAC` buy 1주 @ `54.77 USD`
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime `get_all_positions` 기준 `33` positions 유지. `BAC`는 `5주 -> 6주`, `avg_entry_price=53.315`, `qty_available=6`으로 증가했다.
- Recent reconciliation scope: scheduler-owned `2331` stale cleanup/core/research preflight를 우선 사용했고 live Alpaca MCP submit-boundary check에서 regular market open, ACTIVE account, open orders 0건, same-day fills `RGTI/AVGO/WMT/AAPL`, `BAC` live quote `54.84/54.85`를 재확인했다. sell-first 재평가에서는 `RGTI`와 `AVGO`가 same-day sell duplicate, `SO`가 trim metric gap으로 blocked였고, `WMT`는 same-day buy duplicate, `SPY/QQQ`는 per-order cap을 넘었다. `BAC`는 financials diversifier floor-size validation buy로 선택됐고 direct Alpaca MCP submit 뒤 immediate same-order-id reconciliation 기준 `order_id=544dec18-dc40-499f-9085-e5ad37b50fef`, `filled_avg_price=54.77 USD`로 즉시 전량 체결됐다.
- Orders submitted/replaced/cancelled/closed by this workflow: 1 / 0 / 0 / 1.
- Source note: `wiki/trade-ledger/positions/2026-06-10-2331-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-12-0311-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned core preflight reconciliation 기준 `33` positions 유지, open orders `0`건이다. `AVGO`는 `5주`, `qty_available=5`, `RGTI`는 `49주`, `qty_available=49`, `SO`는 `5주`, `qty_available=5`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `0311` stale cleanup/core/research preflight를 source-of-record로 사용했고 scheduler-owned Alpaca core `get_clock/get_account_info/get_orders_open/get_all_positions/get_account_activities/get_stock_latest_quote/get_stock_snapshot` rows로 same-day fill discipline과 submit-boundary quote/spread를 재확인했다. same-day regular-session `AVGO` trim 1건과 after-hours `RGTI` trim fills 2건은 그대로 유지됐고, `AVGO`는 spread `1.8672%`가 policy cap을 크게 넘겨 trim hard gate fail, `RGTI`는 duplicate sell discipline, `SO`는 spread 회복 후에도 trim metric gap, 신규 buy path는 `review_backlog_pending_1d_count=14`와 benchmark floor cap에 막혀 이번 `0311` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-0311-hourly-autopilot-post-trade.json`

- Run: [[2026-06-10-2311-hourly-autopilot]]
- Open/new: 없음
- Filled: `RGTI` sell 17주 @ `20.38 USD`
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime `get_all_positions` 기준 `33` positions 유지. `RGTI`는 `68주 -> 51주`, `avg_entry_price=25.569583`, `qty_available=51`로 감소했다.
- Recent reconciliation scope: scheduler-owned `2311` stale cleanup/core/research preflight를 우선 사용했고 live Alpaca MCP submit-boundary check에서 regular market open, ACTIVE account, open orders 0건, same-day fills `AVGO/AVGO/WMT/AAPL/AAPL`, `RGTI` live quote `20.38/20.39`를 재확인했다. sell-first 재평가에서는 `RGTI`가 speculative loss-control trim trigger, 큰 미실현 손실, spread `0.0491%` 조건을 모두 만족했고 `AVGO`는 same-day sell duplicate, `SO`는 trim metric gap으로 blocked였다. direct Alpaca MCP submit 뒤 immediate same-order-id reconciliation 기준 `order_id=b9253931-4e50-45ec-a30b-972a4a76903e`, `filled_avg_price=20.38 USD`로 즉시 전량 체결됐다.
- Orders submitted/replaced/cancelled/closed by this workflow: 1 / 0 / 0 / 1.
- Source note: `wiki/trade-ledger/positions/2026-06-10-2311-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-12-0311-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned core preflight reconciliation 기준 `33` positions 유지, open orders `0`건이다. `AVGO`는 `5주`, `qty_available=5`, `RGTI`는 `49주`, `qty_available=49`, `SO`는 `5주`, `qty_available=5`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `0311` stale cleanup/core/research preflight를 source-of-record로 사용했고 scheduler-owned Alpaca core `get_clock/get_account_info/get_orders_open/get_all_positions/get_account_activities/get_stock_latest_quote/get_stock_snapshot` rows로 same-day fill discipline과 submit-boundary quote/spread를 재확인했다. same-day regular-session `AVGO` trim 1건과 after-hours `RGTI` trim fills 2건은 그대로 유지됐고, `AVGO`는 spread `1.8672%`가 policy cap을 크게 넘겨 trim hard gate fail, `RGTI`는 duplicate sell discipline, `SO`는 spread 회복 후에도 trim metric gap, 신규 buy path는 `review_backlog_pending_1d_count=14`와 benchmark floor cap에 막혀 이번 `0311` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-0311-hourly-autopilot-post-trade.json`

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

- Run: [[2026-06-12-0311-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned core preflight reconciliation 기준 `33` positions 유지, open orders `0`건이다. `AVGO`는 `5주`, `qty_available=5`, `RGTI`는 `49주`, `qty_available=49`, `SO`는 `5주`, `qty_available=5`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `0311` stale cleanup/core/research preflight를 source-of-record로 사용했고 scheduler-owned Alpaca core `get_clock/get_account_info/get_orders_open/get_all_positions/get_account_activities/get_stock_latest_quote/get_stock_snapshot` rows로 same-day fill discipline과 submit-boundary quote/spread를 재확인했다. same-day regular-session `AVGO` trim 1건과 after-hours `RGTI` trim fills 2건은 그대로 유지됐고, `AVGO`는 spread `1.8672%`가 policy cap을 크게 넘겨 trim hard gate fail, `RGTI`는 duplicate sell discipline, `SO`는 spread 회복 후에도 trim metric gap, 신규 buy path는 `review_backlog_pending_1d_count=14`와 benchmark floor cap에 막혀 이번 `0311` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-0311-hourly-autopilot-post-trade.json`

- Run: [[2026-06-10-2231-hourly-autopilot]]
- Open/new: 없음
- Filled: `WMT` buy 1주 @ `118.49 USD`
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime `get_all_positions` 기준 `33` positions 유지. `WMT`는 `7주 -> 8주`, `avg_entry_price=118.20625`, `qty_available=8`로 증가했다.
- Recent reconciliation scope: scheduler-owned `2231` stale cleanup/core/research preflight를 우선 사용했고 live Alpaca MCP submit-boundary check에서 regular market open, ACTIVE account, open orders 0건, same-day fills `AAPL/AAPL`, `WMT` live quote `118.75/118.79`를 재확인했다. sell-first 재평가에서는 `RGTI`가 spread `0.5063%`로 cap을 소폭 초과했고 `AVGO/SO`도 각각 spread hard gate에 막혀 executable trim이 남지 않았다. buy fallback에서는 `SPY/QQQ` per-order cap, `NOK` add-block, `BAC/PFE/PLTR` lower-rank가 남아 `WMT`를 floor-size defensive fallback으로 direct Alpaca MCP submit했고 immediate same-order-id reconciliation 기준 `order_id=8b189213-3d70-40a4-8957-2fcdd8b454fd`, `filled_avg_price=118.49 USD`로 즉시 체결됐다.
- Orders submitted/replaced/cancelled/closed by this workflow: 1 / 0 / 0 / 1.
- Source note: `wiki/trade-ledger/positions/2026-06-10-2231-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-12-0311-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned core preflight reconciliation 기준 `33` positions 유지, open orders `0`건이다. `AVGO`는 `5주`, `qty_available=5`, `RGTI`는 `49주`, `qty_available=49`, `SO`는 `5주`, `qty_available=5`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `0311` stale cleanup/core/research preflight를 source-of-record로 사용했고 scheduler-owned Alpaca core `get_clock/get_account_info/get_orders_open/get_all_positions/get_account_activities/get_stock_latest_quote/get_stock_snapshot` rows로 same-day fill discipline과 submit-boundary quote/spread를 재확인했다. same-day regular-session `AVGO` trim 1건과 after-hours `RGTI` trim fills 2건은 그대로 유지됐고, `AVGO`는 spread `1.8672%`가 policy cap을 크게 넘겨 trim hard gate fail, `RGTI`는 duplicate sell discipline, `SO`는 spread 회복 후에도 trim metric gap, 신규 buy path는 `review_backlog_pending_1d_count=14`와 benchmark floor cap에 막혀 이번 `0311` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-0311-hourly-autopilot-post-trade.json`

- Run: [[2026-06-10-0431-hourly-autopilot]]
- Open/new: 없음
- Filled: `XOM` buy 1주 @ `148.35 USD`
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime `get_all_positions` 기준 `33` positions 유지. `XOM`은 `3주 -> 4주`, `avg_entry_price=149.2625`, `qty_available=4`로 증가했다.
- Recent reconciliation scope: scheduler-owned `0431` stale cleanup/core/research preflight를 우선 사용했고 live Alpaca MCP submit-boundary check에서 regular market open, ACTIVE account, open orders 0건, same-day fills `FCX/JNJ/AMZN/COP/SLB/WMT/AVGO/PFE/BAC/RGTI`, `XOM` live quote `148.36/148.40`을 재확인했다. sell-first 재평가 결과 `AVGO`와 `RGTI`는 same-day sell duplicate, `SO`는 spread `1.0298%`와 trim metric gap으로 blocked였다. buy fallback에서는 `FCX/COP/SLB/WMT/PFE/BAC/AMZN/JNJ` same-day duplicate, `QQQ/SPY` per-order cap, `NVDA` same-cluster add block, `UNH` spread fail, `AAPL` 약세 review, `NEE` lower-rank watch가 남아 `XOM`을 energy diversifier floor-size add로 direct Alpaca MCP submit했고 immediate same-order-id reconciliation 기준 `order_id=5a36c3ae-d9e0-4af8-a378-b82ced709bb6`, `filled_avg_price=148.35 USD`로 즉시 체결됐다.
- Orders submitted/replaced/cancelled/closed by this workflow: 1 / 0 / 0 / 1.
- Source note: `wiki/trade-ledger/positions/2026-06-10-0431-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-12-0311-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned core preflight reconciliation 기준 `33` positions 유지, open orders `0`건이다. `AVGO`는 `5주`, `qty_available=5`, `RGTI`는 `49주`, `qty_available=49`, `SO`는 `5주`, `qty_available=5`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `0311` stale cleanup/core/research preflight를 source-of-record로 사용했고 scheduler-owned Alpaca core `get_clock/get_account_info/get_orders_open/get_all_positions/get_account_activities/get_stock_latest_quote/get_stock_snapshot` rows로 same-day fill discipline과 submit-boundary quote/spread를 재확인했다. same-day regular-session `AVGO` trim 1건과 after-hours `RGTI` trim fills 2건은 그대로 유지됐고, `AVGO`는 spread `1.8672%`가 policy cap을 크게 넘겨 trim hard gate fail, `RGTI`는 duplicate sell discipline, `SO`는 spread 회복 후에도 trim metric gap, 신규 buy path는 `review_backlog_pending_1d_count=14`와 benchmark floor cap에 막혀 이번 `0311` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-0311-hourly-autopilot-post-trade.json`

- Run: [[2026-06-10-0411-hourly-autopilot]]
- Open/new: 없음
- Filled: `FCX` buy 1주 @ `63.75 USD`
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime `get_all_positions` 기준 `33` positions 유지. `FCX`는 `3주 -> 4주`, `avg_entry_price=65.5875`, `qty_available=4`로 증가했다.
- Recent reconciliation scope: scheduler-owned `0411` stale cleanup/core/research preflight를 우선 사용했고 live Alpaca MCP submit-boundary check에서 regular market open, ACTIVE account, open orders 0건, same-day fills `JNJ/AMZN/COP/SLB/WMT/AVGO/PFE/BAC/RGTI`, `FCX` live quote `64.00/64.02`를 재확인했다. sell-first 재평가 결과 `AVGO`와 `RGTI`는 same-day sell duplicate, `SO`는 trim metric gap으로 blocked였다. buy fallback에서는 `BAC/COP/WMT/PFE/SLB/AMZN/JNJ` same-day duplicate, `QQQ/SMH` per-order cap, `NVDA` same-cluster add block, `AAPL/NKE/NEE` 약세/스프레드 문제, `SBUX` wiki thesis 부재가 남아 `FCX`를 materials/mining floor-size add로 direct Alpaca MCP submit했고 immediate same-client-id reconciliation 기준 `order_id=80a34b1a-5044-47cf-aadc-338e0db675f9`, `filled_avg_price=63.75 USD`로 즉시 체결됐다.
- Orders submitted/replaced/cancelled/closed by this workflow: 1 / 0 / 0 / 1.
- Source note: `wiki/trade-ledger/positions/2026-06-10-0411-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-12-0311-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned core preflight reconciliation 기준 `33` positions 유지, open orders `0`건이다. `AVGO`는 `5주`, `qty_available=5`, `RGTI`는 `49주`, `qty_available=49`, `SO`는 `5주`, `qty_available=5`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `0311` stale cleanup/core/research preflight를 source-of-record로 사용했고 scheduler-owned Alpaca core `get_clock/get_account_info/get_orders_open/get_all_positions/get_account_activities/get_stock_latest_quote/get_stock_snapshot` rows로 same-day fill discipline과 submit-boundary quote/spread를 재확인했다. same-day regular-session `AVGO` trim 1건과 after-hours `RGTI` trim fills 2건은 그대로 유지됐고, `AVGO`는 spread `1.8672%`가 policy cap을 크게 넘겨 trim hard gate fail, `RGTI`는 duplicate sell discipline, `SO`는 spread 회복 후에도 trim metric gap, 신규 buy path는 `review_backlog_pending_1d_count=14`와 benchmark floor cap에 막혀 이번 `0311` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-0311-hourly-autopilot-post-trade.json`

- Run: [[2026-06-10-0351-hourly-autopilot]]
- Open/new: 없음
- Filled: `JNJ` buy 1주 @ `237.54 USD`
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime `get_all_positions` 기준 `33` positions로 증가했다. `JNJ`는 신규 1주가 추가됐고 `avg_entry_price=237.54`, `qty_available=1`이다.
- Recent reconciliation scope: scheduler-owned `0351` stale cleanup/core/research preflight를 우선 사용했고 live Alpaca MCP submit-boundary check에서 regular market open, ACTIVE account, open orders 0건, stale `NVDA` buy cancel, same-day fills `AMZN/COP/SLB/WMT/AVGO/PFE/BAC/RGTI`, `JNJ` live/preflight quote `237.49/237.55`를 재확인했다. sell-first 재평가 결과 `AVGO`와 `RGTI`는 same-day sell duplicate, `SO`는 spread `2.3170%`와 trim metric gap으로 blocked였다. buy fallback에서는 `COP/SLB/WMT/PFE/BAC/AMZN` same-day duplicate, `SPY/QQQ` per-order cap, `NVDA` same-cluster add block, `AAPL/NKE/NEE` 약세가 남아 `JNJ`를 healthcare defensive diversifier floor-size add로 direct Alpaca MCP submit했고 immediate same-client-id reconciliation 기준 `order_id=6f39a832-aec9-4c63-96bb-491a32b8864b`, `filled_avg_price=237.54 USD`로 즉시 체결됐다.
- Orders submitted/replaced/cancelled/closed by this workflow: 1 / 0 / 0 / 1.
- Source note: `wiki/trade-ledger/positions/2026-06-10-0351-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-12-0311-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned core preflight reconciliation 기준 `33` positions 유지, open orders `0`건이다. `AVGO`는 `5주`, `qty_available=5`, `RGTI`는 `49주`, `qty_available=49`, `SO`는 `5주`, `qty_available=5`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `0311` stale cleanup/core/research preflight를 source-of-record로 사용했고 scheduler-owned Alpaca core `get_clock/get_account_info/get_orders_open/get_all_positions/get_account_activities/get_stock_latest_quote/get_stock_snapshot` rows로 same-day fill discipline과 submit-boundary quote/spread를 재확인했다. same-day regular-session `AVGO` trim 1건과 after-hours `RGTI` trim fills 2건은 그대로 유지됐고, `AVGO`는 spread `1.8672%`가 policy cap을 크게 넘겨 trim hard gate fail, `RGTI`는 duplicate sell discipline, `SO`는 spread 회복 후에도 trim metric gap, 신규 buy path는 `review_backlog_pending_1d_count=14`와 benchmark floor cap에 막혀 이번 `0311` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-0311-hourly-autopilot-post-trade.json`

- Run: [[2026-06-10-0311-hourly-autopilot]]
- Open/new: `NVDA` buy 1주 @ `205.40 USD` (`status=new`)
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime `get_all_positions` 기준 `32` positions 유지. `NVDA`는 아직 `38주`, `avg_entry_price=215.031579`, `qty_available=38`로 unchanged이며 open orders는 `NVDA` buy 1건이다.
- Recent reconciliation scope: scheduler-owned `0311` stale cleanup/core/research preflight를 우선 사용했고 live Alpaca MCP submit-boundary check에서 regular market open, ACTIVE account, open orders 0건, same-day fills `COP/SLB/WMT/AVGO/PFE/BAC/RGTI`, `NVDA` live IEX quote `205.37/205.40`를 재확인했다. sell-first 재평가 결과 `AVGO`와 `RGTI`는 same-day sell duplicate, `SO`는 trim metric gap으로 blocked였다. buy fallback에서는 `COP/SLB/WMT/PFE/BAC` same-day duplicate, `SPY/QQQ` per-order cap, `AAPL/AMZN/GOOGL/NKE` review 약세가 남아 `NVDA`를 floor-size AI core holding add로 direct Alpaca MCP submit했다. immediate same-order-id reconciliation 기준 `order_id=56d0bb25-b51d-40e5-8ba9-f76ab79d67ae`, `status=new`, `filled_qty=0` open order다.
- Orders submitted/replaced/cancelled/closed by this workflow: 1 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-10-0311-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-12-0311-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned core preflight reconciliation 기준 `33` positions 유지, open orders `0`건이다. `AVGO`는 `5주`, `qty_available=5`, `RGTI`는 `49주`, `qty_available=49`, `SO`는 `5주`, `qty_available=5`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `0311` stale cleanup/core/research preflight를 source-of-record로 사용했고 scheduler-owned Alpaca core `get_clock/get_account_info/get_orders_open/get_all_positions/get_account_activities/get_stock_latest_quote/get_stock_snapshot` rows로 same-day fill discipline과 submit-boundary quote/spread를 재확인했다. same-day regular-session `AVGO` trim 1건과 after-hours `RGTI` trim fills 2건은 그대로 유지됐고, `AVGO`는 spread `1.8672%`가 policy cap을 크게 넘겨 trim hard gate fail, `RGTI`는 duplicate sell discipline, `SO`는 spread 회복 후에도 trim metric gap, 신규 buy path는 `review_backlog_pending_1d_count=14`와 benchmark floor cap에 막혀 이번 `0311` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-0311-hourly-autopilot-post-trade.json`

- Run: [[2026-06-10-0251-hourly-autopilot]]
- Open/new: 없음
- Filled: `COP` buy 1주 @ `116.05 USD`
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime `get_all_positions` 기준 `32` positions 유지. `COP`는 `3주 -> 4주`, `avg_entry_price=116.8975`, `qty_available=4`로 증가했다.
- Recent reconciliation scope: scheduler-owned `0251` stale cleanup/core/research preflight를 우선 사용했고 live Alpaca MCP submit-boundary check에서 regular market open, ACTIVE account, open orders 0건, same-day fills `SLB/WMT/AVGO/PFE/BAC/RGTI`, `COP` live IEX quote `116.09/116.14`를 재확인했다. sell-first 재평가 결과 `AVGO`와 `RGTI`는 same-day sell duplicate, `SO`는 trim metric gap으로 blocked였다. buy fallback에서는 `SLB/WMT/PFE/BAC` same-day duplicate, `SPY/QQQ` per-order cap, `NOK` add-block이 남아 `COP`를 floor-size energy/value diversifier fallback buy로 direct Alpaca MCP submit했고 immediate same-client-id reconciliation 기준 `order_id=34da84fa-1653-4852-a955-6a1e0efd3fa8`, `filled_avg_price=116.05 USD`로 즉시 체결됐다.
- Orders submitted/replaced/cancelled/closed by this workflow: 1 / 0 / 0 / 1.
- Source note: `wiki/trade-ledger/positions/2026-06-10-0251-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-12-0311-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned core preflight reconciliation 기준 `33` positions 유지, open orders `0`건이다. `AVGO`는 `5주`, `qty_available=5`, `RGTI`는 `49주`, `qty_available=49`, `SO`는 `5주`, `qty_available=5`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `0311` stale cleanup/core/research preflight를 source-of-record로 사용했고 scheduler-owned Alpaca core `get_clock/get_account_info/get_orders_open/get_all_positions/get_account_activities/get_stock_latest_quote/get_stock_snapshot` rows로 same-day fill discipline과 submit-boundary quote/spread를 재확인했다. same-day regular-session `AVGO` trim 1건과 after-hours `RGTI` trim fills 2건은 그대로 유지됐고, `AVGO`는 spread `1.8672%`가 policy cap을 크게 넘겨 trim hard gate fail, `RGTI`는 duplicate sell discipline, `SO`는 spread 회복 후에도 trim metric gap, 신규 buy path는 `review_backlog_pending_1d_count=14`와 benchmark floor cap에 막혀 이번 `0311` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-0311-hourly-autopilot-post-trade.json`

- Run: [[2026-06-10-0231-hourly-autopilot]]
- Open/new: `SLB` buy 1주 @ `55.11 USD` (`status=new`)
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime `get_all_positions` 기준 `32` positions 유지. `SLB`는 아직 `4주`, `qty_available=4` 그대로이며 open orders는 `SLB` buy 1건이다.
- Recent reconciliation scope: scheduler-owned `0231` stale cleanup/core/research preflight를 우선 사용했고 live Alpaca MCP submit-boundary check에서 regular market open, ACTIVE account, open orders 0건, same-day fills `WMT/AVGO/PFE/BAC/RGTI`, `SLB` live quote `55.10/55.11`을 재확인했다. sell-first 재평가 결과 `AVGO`와 `RGTI`는 same-day sell duplicate, `SO`는 trim metric gap으로 blocked였다. buy fallback에서는 `WMT/PFE/BAC` same-day duplicate, `GOOGL` live spread fail, `SPY/QQQ` per-order cap, `NOK` add-block이 남아 `SLB`를 floor-size energy-services diversifier fallback buy로 direct Alpaca MCP submit했다. immediate reconciliation 기준 `order_id=d225a67d-6bc2-4488-99f3-d45a48bf6f4e`, `status=new`, `filled_qty=0` open order다.
- Orders submitted/replaced/cancelled/closed by this workflow: 1 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-10-0231-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-12-0311-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned core preflight reconciliation 기준 `33` positions 유지, open orders `0`건이다. `AVGO`는 `5주`, `qty_available=5`, `RGTI`는 `49주`, `qty_available=49`, `SO`는 `5주`, `qty_available=5`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `0311` stale cleanup/core/research preflight를 source-of-record로 사용했고 scheduler-owned Alpaca core `get_clock/get_account_info/get_orders_open/get_all_positions/get_account_activities/get_stock_latest_quote/get_stock_snapshot` rows로 same-day fill discipline과 submit-boundary quote/spread를 재확인했다. same-day regular-session `AVGO` trim 1건과 after-hours `RGTI` trim fills 2건은 그대로 유지됐고, `AVGO`는 spread `1.8672%`가 policy cap을 크게 넘겨 trim hard gate fail, `RGTI`는 duplicate sell discipline, `SO`는 spread 회복 후에도 trim metric gap, 신규 buy path는 `review_backlog_pending_1d_count=14`와 benchmark floor cap에 막혀 이번 `0311` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-0311-hourly-autopilot-post-trade.json`

- Run: [[2026-06-10-0211-hourly-autopilot]]
- Open/new: 없음
- Filled: `WMT` buy 1주 @ `118.70 USD`
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime `get_all_positions` 기준 `32` positions 유지. `WMT`는 `6주 -> 7주`, `avg_entry_price=118.165715`, `qty_available=7`로 증가했다.
- Recent reconciliation scope: scheduler-owned `0211` stale cleanup/core/research preflight를 우선 사용했고 sell-first 재평가에서 `AVGO`와 `RGTI`는 same-day sell duplicate, `SO`는 trim metric gap으로 각각 blocked였다. buy fallback에서는 `PFE/BAC` same-day duplicate, `GOOGL` spread fail, `SPY/QQQ` per-order cap, `NOK` add-block이 남아 `WMT`를 floor-size defensive fallback으로 direct Alpaca MCP submit했다. immediate same-client-id reconciliation 기준 `order_id=40066752-96cc-4225-aa77-0e6ba6c7ccb3`는 `filled_avg_price=118.70 USD`로 즉시 체결됐고 open order는 0건이다.
- Orders submitted/replaced/cancelled/closed by this workflow: 1 / 0 / 0 / 1.
- Source note: `wiki/trade-ledger/positions/2026-06-10-0211-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-12-0311-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned core preflight reconciliation 기준 `33` positions 유지, open orders `0`건이다. `AVGO`는 `5주`, `qty_available=5`, `RGTI`는 `49주`, `qty_available=49`, `SO`는 `5주`, `qty_available=5`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `0311` stale cleanup/core/research preflight를 source-of-record로 사용했고 scheduler-owned Alpaca core `get_clock/get_account_info/get_orders_open/get_all_positions/get_account_activities/get_stock_latest_quote/get_stock_snapshot` rows로 same-day fill discipline과 submit-boundary quote/spread를 재확인했다. same-day regular-session `AVGO` trim 1건과 after-hours `RGTI` trim fills 2건은 그대로 유지됐고, `AVGO`는 spread `1.8672%`가 policy cap을 크게 넘겨 trim hard gate fail, `RGTI`는 duplicate sell discipline, `SO`는 spread 회복 후에도 trim metric gap, 신규 buy path는 `review_backlog_pending_1d_count=14`와 benchmark floor cap에 막혀 이번 `0311` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-0311-hourly-autopilot-post-trade.json`

- Run: [[2026-06-10-0151-hourly-autopilot]]
- Open/new: 기존 `AVGO` sell 2주 @ `375.32 USD` (`status=new`)
- Filled: `PFE` buy 1주 @ `25.82 USD`
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime `get_all_positions` 기준 `32` positions 유지. `PFE`는 `5주`로 늘었고 `AVGO`는 `10주`, `qty_available`는 `8주`로 기존 open sell 2주가 예약된 상태다.
- Recent reconciliation scope: scheduler-owned `0151` stale cleanup/core/research preflight를 우선 사용했고 live Alpaca MCP submit-boundary check에서 stale `PFE` buy가 실제 canceled로 정리된 뒤 fresh `AVGO` sell 1건만 남아 있음을 재확인했다. sell-first 재평가 결과 `AVGO`는 spread 정상화 후에도 existing open sell duplicate로 추가 trim이 막혔고, `RGTI`는 same-day sell duplicate, `SO`는 trim metric gap으로 blocked였다. user directive에 따라 buy fallback을 재평가해 `PFE` 1주 buy를 direct Alpaca MCP submit했고 immediate reconciliation 기준 `order_id=3f342972-201b-4599-9209-ba6ec56f89eb`, `filled_avg_price=25.82 USD`로 즉시 체결됐다.
- Orders submitted/replaced/cancelled/closed by this workflow: 1 / 0 / 0 / 1.
- Source note: `wiki/trade-ledger/positions/2026-06-10-0151-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-12-0311-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned core preflight reconciliation 기준 `33` positions 유지, open orders `0`건이다. `AVGO`는 `5주`, `qty_available=5`, `RGTI`는 `49주`, `qty_available=49`, `SO`는 `5주`, `qty_available=5`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `0311` stale cleanup/core/research preflight를 source-of-record로 사용했고 scheduler-owned Alpaca core `get_clock/get_account_info/get_orders_open/get_all_positions/get_account_activities/get_stock_latest_quote/get_stock_snapshot` rows로 same-day fill discipline과 submit-boundary quote/spread를 재확인했다. same-day regular-session `AVGO` trim 1건과 after-hours `RGTI` trim fills 2건은 그대로 유지됐고, `AVGO`는 spread `1.8672%`가 policy cap을 크게 넘겨 trim hard gate fail, `RGTI`는 duplicate sell discipline, `SO`는 spread 회복 후에도 trim metric gap, 신규 buy path는 `review_backlog_pending_1d_count=14`와 benchmark floor cap에 막혀 이번 `0311` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-0311-hourly-autopilot-post-trade.json`

- Run: [[2026-06-10-0131-hourly-autopilot]]
- Open/new: `AVGO` sell 2주 @ `375.32 USD` (`status=new`), 기존 `PFE` buy 1주 @ `25.70 USD` (`status=new`)
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime `get_all_positions` 기준 `32` positions 유지. `AVGO`는 아직 `10주` 그대로이며 `qty_available`가 `8주`로 줄어 open sell 2주가 예약됐다. `PFE`는 `4주` 유지다.
- Recent reconciliation scope: scheduler-owned `0131` stale cleanup/core/research preflight를 우선 사용했고 direct Alpaca MCP live check에서 regular market open, ACTIVE account, fresh quotes, fresh `PFE` buy open order 1건, same-day fills `BAC`/`RGTI`를 재확인했다. sell-first 재평가 결과 `AVGO`는 live spread `0.0852%`로 trim hard gate를 통과했고, `RGTI`는 same-day sell duplicate conflict, `SO`는 trim metric gap으로 blocked였다. user directive에 따라 eligible risk-reducing sell을 우선 선택해 `AVGO` trim을 direct Alpaca MCP submit했고 immediate reconciliation 기준 `order_id=d850cf67-3c44-4a63-9f44-ef53c5fe8897`, `status=new`, `filled_qty=0` open order다.
- Orders submitted/replaced/cancelled/closed by this workflow: 1 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-10-0131-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-12-0311-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned core preflight reconciliation 기준 `33` positions 유지, open orders `0`건이다. `AVGO`는 `5주`, `qty_available=5`, `RGTI`는 `49주`, `qty_available=49`, `SO`는 `5주`, `qty_available=5`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `0311` stale cleanup/core/research preflight를 source-of-record로 사용했고 scheduler-owned Alpaca core `get_clock/get_account_info/get_orders_open/get_all_positions/get_account_activities/get_stock_latest_quote/get_stock_snapshot` rows로 same-day fill discipline과 submit-boundary quote/spread를 재확인했다. same-day regular-session `AVGO` trim 1건과 after-hours `RGTI` trim fills 2건은 그대로 유지됐고, `AVGO`는 spread `1.8672%`가 policy cap을 크게 넘겨 trim hard gate fail, `RGTI`는 duplicate sell discipline, `SO`는 spread 회복 후에도 trim metric gap, 신규 buy path는 `review_backlog_pending_1d_count=14`와 benchmark floor cap에 막혀 이번 `0311` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-0311-hourly-autopilot-post-trade.json`

- Run: [[2026-06-10-0111-hourly-autopilot]]
- Open/new: `PFE` buy 1주 @ `25.70 USD` (`status=new`)
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime `get_all_positions` 기준 `32` positions 유지. `PFE`는 아직 `4주` 그대로이고 신규 open order는 `PFE` 1건이다.
- Recent reconciliation scope: scheduler-owned `0111` stale cleanup/core/research preflight를 우선 사용했고 stale cleanup과 runtime `get_orders(status=open)`가 모두 open-order lifecycle PASS를 재확인했다. sell-first 재평가 결과 `AVGO`는 live spread `6.0276%`로 trim hard gate fail, `RGTI`는 same-day sell duplicate conflict, `SO`는 trim metric gap으로 blocked였다. `BAC`는 same-day buy duplicate, `SPY/QQQ`는 per-order cap 초과, `NOK`는 add-block이라 `PFE`가 floor-size healthcare fallback buy로 direct Alpaca MCP submit됐다. immediate reconciliation 기준 `order_id=df1b6130-1929-4189-9003-ad7f47add552`, `status=new`, `filled_qty=0` open order다.
- Orders submitted/replaced/cancelled/closed by this workflow: 1 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-10-0111-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-12-0311-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned core preflight reconciliation 기준 `33` positions 유지, open orders `0`건이다. `AVGO`는 `5주`, `qty_available=5`, `RGTI`는 `49주`, `qty_available=49`, `SO`는 `5주`, `qty_available=5`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `0311` stale cleanup/core/research preflight를 source-of-record로 사용했고 scheduler-owned Alpaca core `get_clock/get_account_info/get_orders_open/get_all_positions/get_account_activities/get_stock_latest_quote/get_stock_snapshot` rows로 same-day fill discipline과 submit-boundary quote/spread를 재확인했다. same-day regular-session `AVGO` trim 1건과 after-hours `RGTI` trim fills 2건은 그대로 유지됐고, `AVGO`는 spread `1.8672%`가 policy cap을 크게 넘겨 trim hard gate fail, `RGTI`는 duplicate sell discipline, `SO`는 spread 회복 후에도 trim metric gap, 신규 buy path는 `review_backlog_pending_1d_count=14`와 benchmark floor cap에 막혀 이번 `0311` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-0311-hourly-autopilot-post-trade.json`

- Run: [[2026-06-10-0051-hourly-autopilot]]
- Open/new: `WMT` buy 1주 @ `118.99 USD` (`status=new`)
- Filled: 없음
- Cancelled: scheduler-owned stale cleanup에서 `SO` buy 1주 @ `92.03 USD` open order 제거
- Position count observed by Alpaca MCP: scheduler-owned core preflight `get_all_positions` 기준 `32` positions 유지. `WMT`는 `6주` 그대로이고 remaining open order는 `WMT` 1건만 기록됐다.
- Recent reconciliation scope: scheduler-owned `0051` stale cleanup/core/research preflight를 우선 사용했다. stale cleanup report가 `WMT` open buy를 cancel attempt 이후에도 `remaining_open_orders`로 남겨 `risk_open_order_lifecycle` first blocking gate가 확정됐고, sell-first 재평가에서도 `AVGO`는 spread `4.7347%`, `RGTI`는 same-day sell duplicate, `SO`는 trim metric gap으로 각각 blocked됐다. `PFE`는 floor-size healthcare fallback buy 후보로 남았지만 신규 submit 없이 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 1 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-10-0051-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-12-0311-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned core preflight reconciliation 기준 `33` positions 유지, open orders `0`건이다. `AVGO`는 `5주`, `qty_available=5`, `RGTI`는 `49주`, `qty_available=49`, `SO`는 `5주`, `qty_available=5`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `0311` stale cleanup/core/research preflight를 source-of-record로 사용했고 scheduler-owned Alpaca core `get_clock/get_account_info/get_orders_open/get_all_positions/get_account_activities/get_stock_latest_quote/get_stock_snapshot` rows로 same-day fill discipline과 submit-boundary quote/spread를 재확인했다. same-day regular-session `AVGO` trim 1건과 after-hours `RGTI` trim fills 2건은 그대로 유지됐고, `AVGO`는 spread `1.8672%`가 policy cap을 크게 넘겨 trim hard gate fail, `RGTI`는 duplicate sell discipline, `SO`는 spread 회복 후에도 trim metric gap, 신규 buy path는 `review_backlog_pending_1d_count=14`와 benchmark floor cap에 막혀 이번 `0311` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-0311-hourly-autopilot-post-trade.json`

- Run: [[2026-06-10-0031-hourly-autopilot]]
- Open/new: `SO` buy 1주 @ `92.03 USD` (`status=new`), `WMT` buy 1주 @ `118.99 USD` (`status=new`)
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime `get_all_positions` 기준 `32` positions 유지. `SO`는 `5주`, `WMT`는 `6주` 그대로이며 open orders는 `SO/WMT` 2건이다.
- Recent reconciliation scope: scheduler-owned `0031` stale cleanup/core/research preflight를 우선 사용했고 sell-first 재평가 결과 `AVGO`는 live spread `4.7804%`로 trim hard gate fail, `RGTI`는 same-day sell duplicate conflict, `SO`는 same-day open buy와 trim metric gap으로 blocked였다. `PFE`는 floor-size healthcare fallback buy 후보로 승격됐지만 `check-risk-policy.py`가 `WMT` open order age `32.7`분을 lifecycle limit `30.0` 초과로 판정해 first blocking gate=`risk_open_order_lifecycle`가 됐고 신규 submit 없이 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-10-0031-hourly-autopilot-post-trade.json`


## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-12-0311-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned core preflight reconciliation 기준 `33` positions 유지, open orders `0`건이다. `AVGO`는 `5주`, `qty_available=5`, `RGTI`는 `49주`, `qty_available=49`, `SO`는 `5주`, `qty_available=5`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `0311` stale cleanup/core/research preflight를 source-of-record로 사용했고 scheduler-owned Alpaca core `get_clock/get_account_info/get_orders_open/get_all_positions/get_account_activities/get_stock_latest_quote/get_stock_snapshot` rows로 same-day fill discipline과 submit-boundary quote/spread를 재확인했다. same-day regular-session `AVGO` trim 1건과 after-hours `RGTI` trim fills 2건은 그대로 유지됐고, `AVGO`는 spread `1.8672%`가 policy cap을 크게 넘겨 trim hard gate fail, `RGTI`는 duplicate sell discipline, `SO`는 spread 회복 후에도 trim metric gap, 신규 buy path는 `review_backlog_pending_1d_count=14`와 benchmark floor cap에 막혀 이번 `0311` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-0311-hourly-autopilot-post-trade.json`

- Run: [[2026-06-10-0011-hourly-autopilot]]
- Open/new: `SO` buy 1주 @ `92.03 USD` (`status=new`), 기존 `WMT` buy 1주 @ `118.99 USD` (`status=new`)
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime `get_all_positions` 기준 `32` positions 유지. `SO`는 아직 `5주`, `WMT`는 `6주` 그대로이며 open orders는 `SO/WMT` 2건이다.
- Recent reconciliation scope: scheduler-owned `0011` stale cleanup/core/research preflight를 우선 사용했고 sell-first 재평가 결과 `AVGO`는 live spread `0.6251%`로 trim hard gate fail, `RGTI`는 same-day sell duplicate conflict, `SO`는 trim metric gap으로 blocked였다. buy fallback에서는 `WMT` fresh open-order duplicate, `BAC` same-day buy duplicate, `SPY/QQQ` per-order cap 초과, `NOK` add-block이 각각 남아 `SO`를 floor-size utilities diversifier fallback buy로 direct Alpaca MCP submit했다. immediate reconciliation 기준 `order_id=8775f764-2758-4958-9fa1-21a92e69fb91`, `status=new`, `filled_qty=0` open order다.
- Orders submitted/replaced/cancelled/closed by this workflow: 1 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-10-0011-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-12-0311-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned core preflight reconciliation 기준 `33` positions 유지, open orders `0`건이다. `AVGO`는 `5주`, `qty_available=5`, `RGTI`는 `49주`, `qty_available=49`, `SO`는 `5주`, `qty_available=5`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `0311` stale cleanup/core/research preflight를 source-of-record로 사용했고 scheduler-owned Alpaca core `get_clock/get_account_info/get_orders_open/get_all_positions/get_account_activities/get_stock_latest_quote/get_stock_snapshot` rows로 same-day fill discipline과 submit-boundary quote/spread를 재확인했다. same-day regular-session `AVGO` trim 1건과 after-hours `RGTI` trim fills 2건은 그대로 유지됐고, `AVGO`는 spread `1.8672%`가 policy cap을 크게 넘겨 trim hard gate fail, `RGTI`는 duplicate sell discipline, `SO`는 spread 회복 후에도 trim metric gap, 신규 buy path는 `review_backlog_pending_1d_count=14`와 benchmark floor cap에 막혀 이번 `0311` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-0311-hourly-autopilot-post-trade.json`

- Run: [[2026-06-09-2351-hourly-autopilot]]
- Open/new: `WMT` buy 1주 @ `118.99 USD` (`status=new`)
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime `get_all_positions` 기준 `32` positions 유지. `WMT`는 아직 `6주` 그대로이며 open orders는 `WMT` 1건이다.
- Recent reconciliation scope: scheduler-owned `2351` stale cleanup/core/research preflight를 우선 사용했고 sell-first 재평가 결과 `AVGO`는 live spread `3.5054%`로 hard gate fail, `RGTI`는 same-day sell duplicate conflict, `SO`는 decision-grade metric gap으로 blocked였다. `BAC`는 `2331` cycle buy 1주가 `2026-06-09T14:45:16Z` same-day fill로 확인돼 buy-side duplicate gate에 걸렸고, `SPY/QQQ`는 1주 ask가 validation floor per-order cap을 넘었다. 따라서 `WMT`를 floor-size defensive diversifier fallback buy로 제출했고 immediate reconciliation 기준 `order_id=487039ff-24cb-4094-9301-add50be8886c`, `status=new`, `filled_qty=0` open order다.
- Orders submitted/replaced/cancelled/closed by this workflow: 1 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-09-2351-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-12-0311-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned core preflight reconciliation 기준 `33` positions 유지, open orders `0`건이다. `AVGO`는 `5주`, `qty_available=5`, `RGTI`는 `49주`, `qty_available=49`, `SO`는 `5주`, `qty_available=5`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `0311` stale cleanup/core/research preflight를 source-of-record로 사용했고 scheduler-owned Alpaca core `get_clock/get_account_info/get_orders_open/get_all_positions/get_account_activities/get_stock_latest_quote/get_stock_snapshot` rows로 same-day fill discipline과 submit-boundary quote/spread를 재확인했다. same-day regular-session `AVGO` trim 1건과 after-hours `RGTI` trim fills 2건은 그대로 유지됐고, `AVGO`는 spread `1.8672%`가 policy cap을 크게 넘겨 trim hard gate fail, `RGTI`는 duplicate sell discipline, `SO`는 spread 회복 후에도 trim metric gap, 신규 buy path는 `review_backlog_pending_1d_count=14`와 benchmark floor cap에 막혀 이번 `0311` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-0311-hourly-autopilot-post-trade.json`

- Run: [[2026-06-09-2311-hourly-autopilot]]
- Open/new: `AVGO` sell 2주 @ `403.00 USD` (`status=new`, 기존 `2251` cycle order 유지)
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned `2311` core preflight 기준 `32` positions 유지. `AVGO` 총 보유수량은 `10주`, `qty_available`는 `8주`로 그대로이며 open orders는 `AVGO` 1건이다.
- Recent reconciliation scope: 이번 cycle은 신규 submit 없이 open-order lifecycle 재점검에 집중했다. scheduler-owned stale cleanup은 stale candidate 0건이었지만, core preflight는 직전 `hourly-20260609-2251-sell-avgo`가 여전히 `status=new` open order임을 보여줬다. `RGTI`는 same-day duplicate symbol/side conflict, `SO`는 decision-grade metric gap, `BAC` buy fallback은 unresolved open-order lifecycle 때문에 모두 미제출 처리했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-09-2311-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-12-0311-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned core preflight reconciliation 기준 `33` positions 유지, open orders `0`건이다. `AVGO`는 `5주`, `qty_available=5`, `RGTI`는 `49주`, `qty_available=49`, `SO`는 `5주`, `qty_available=5`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `0311` stale cleanup/core/research preflight를 source-of-record로 사용했고 scheduler-owned Alpaca core `get_clock/get_account_info/get_orders_open/get_all_positions/get_account_activities/get_stock_latest_quote/get_stock_snapshot` rows로 same-day fill discipline과 submit-boundary quote/spread를 재확인했다. same-day regular-session `AVGO` trim 1건과 after-hours `RGTI` trim fills 2건은 그대로 유지됐고, `AVGO`는 spread `1.8672%`가 policy cap을 크게 넘겨 trim hard gate fail, `RGTI`는 duplicate sell discipline, `SO`는 spread 회복 후에도 trim metric gap, 신규 buy path는 `review_backlog_pending_1d_count=14`와 benchmark floor cap에 막혀 이번 `0311` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-0311-hourly-autopilot-post-trade.json`

- Run: [[2026-06-09-2251-hourly-autopilot]]
- Open/new: `AVGO` sell 2주 @ `403.00 USD` (`status=new`)
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime `get_all_positions` 기준 `32` positions 유지. `AVGO` 총 보유수량은 `10주` 그대로지만 `qty_available`가 `10주 -> 8주`로 줄어 open sell 2주가 예약돼 있다. open orders는 `AVGO` 1건이다.
- Recent reconciliation scope: scheduler-owned `2251` regular-session core/research preflight를 우선 사용했고, registered Alpaca MCP live check로 market open, open orders 0건, same-day `RGTI` fill 2건, `AVGO` quote `403.00/403.66`를 재확인했다. `RGTI`는 same-day duplicate symbol/side conflict로 추가 trim에서 제외했고, spread가 정상화된 `AVGO`를 sell-first validation trim 후보로 선택해 direct registered Alpaca MCP submit을 수행했다. immediate reconciliation 기준 `AVGO` 주문은 `order_id=bf1247db-2054-4304-a16b-58ada7b39af7`, `status=new`, `filled_qty=0`이며 신규 fill은 아직 없다.
- Orders submitted/replaced/cancelled/closed by this workflow: 1 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-09-2251-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-12-0311-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned core preflight reconciliation 기준 `33` positions 유지, open orders `0`건이다. `AVGO`는 `5주`, `qty_available=5`, `RGTI`는 `49주`, `qty_available=49`, `SO`는 `5주`, `qty_available=5`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `0311` stale cleanup/core/research preflight를 source-of-record로 사용했고 scheduler-owned Alpaca core `get_clock/get_account_info/get_orders_open/get_all_positions/get_account_activities/get_stock_latest_quote/get_stock_snapshot` rows로 same-day fill discipline과 submit-boundary quote/spread를 재확인했다. same-day regular-session `AVGO` trim 1건과 after-hours `RGTI` trim fills 2건은 그대로 유지됐고, `AVGO`는 spread `1.8672%`가 policy cap을 크게 넘겨 trim hard gate fail, `RGTI`는 duplicate sell discipline, `SO`는 spread 회복 후에도 trim metric gap, 신규 buy path는 `review_backlog_pending_1d_count=14`와 benchmark floor cap에 막혀 이번 `0311` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-0311-hourly-autopilot-post-trade.json`

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

- Run: [[2026-06-12-0311-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned core preflight reconciliation 기준 `33` positions 유지, open orders `0`건이다. `AVGO`는 `5주`, `qty_available=5`, `RGTI`는 `49주`, `qty_available=49`, `SO`는 `5주`, `qty_available=5`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `0311` stale cleanup/core/research preflight를 source-of-record로 사용했고 scheduler-owned Alpaca core `get_clock/get_account_info/get_orders_open/get_all_positions/get_account_activities/get_stock_latest_quote/get_stock_snapshot` rows로 same-day fill discipline과 submit-boundary quote/spread를 재확인했다. same-day regular-session `AVGO` trim 1건과 after-hours `RGTI` trim fills 2건은 그대로 유지됐고, `AVGO`는 spread `1.8672%`가 policy cap을 크게 넘겨 trim hard gate fail, `RGTI`는 duplicate sell discipline, `SO`는 spread 회복 후에도 trim metric gap, 신규 buy path는 `review_backlog_pending_1d_count=14`와 benchmark floor cap에 막혀 이번 `0311` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-0311-hourly-autopilot-post-trade.json`

- Run: [[2026-06-09-0431-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler core preflight 기준 `32` positions 유지. open orders는 0건이고 `RGTI/AVGO/SO` 모두 신규 수량 변화 없이 유지됐다.
- Recent reconciliation scope: scheduler-owned `0431` stale cleanup/core/research preflight 기준 신규 buy는 `review_backlog_pending_1d_count=13` backlog throttle에 막혔고, sell-first 후보는 `RGTI` same-day duplicate, `AVGO` same-day duplicate, `SO` decision-grade metric gap 때문에 submit되지 않았다. same-day filled orders는 `AVGO` 장외 sell 2건, `TSLA` exit 1건, `RGTI` trim 1건으로 총 4건 재확인됐다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-09-0431-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-12-0311-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned core preflight reconciliation 기준 `33` positions 유지, open orders `0`건이다. `AVGO`는 `5주`, `qty_available=5`, `RGTI`는 `49주`, `qty_available=49`, `SO`는 `5주`, `qty_available=5`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `0311` stale cleanup/core/research preflight를 source-of-record로 사용했고 scheduler-owned Alpaca core `get_clock/get_account_info/get_orders_open/get_all_positions/get_account_activities/get_stock_latest_quote/get_stock_snapshot` rows로 same-day fill discipline과 submit-boundary quote/spread를 재확인했다. same-day regular-session `AVGO` trim 1건과 after-hours `RGTI` trim fills 2건은 그대로 유지됐고, `AVGO`는 spread `1.8672%`가 policy cap을 크게 넘겨 trim hard gate fail, `RGTI`는 duplicate sell discipline, `SO`는 spread 회복 후에도 trim metric gap, 신규 buy path는 `review_backlog_pending_1d_count=14`와 benchmark floor cap에 막혀 이번 `0311` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-0311-hourly-autopilot-post-trade.json`

- Run: [[2026-06-09-0411-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler core preflight 기준 `32` positions 유지. open orders는 0건이고 `RGTI/AVGO/SO` 모두 신규 수량 변화 없이 유지됐다.
- Recent reconciliation scope: scheduler-owned `0411` stale cleanup/core/research preflight 기준 신규 buy는 `review_backlog_pending_1d_count=13` backlog throttle에 막혔고, sell-first 후보는 `RGTI` same-day duplicate, `AVGO` duplicate+spread `0.5394%`, `SO` spread `2.1025%` + decision-grade metric gap 때문에 submit되지 않았다. same-day filled orders는 `AVGO` 장외 sell 2건, `TSLA` exit 1건, `RGTI` trim 1건으로 총 4건 재확인됐다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-09-0411-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-12-0311-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned core preflight reconciliation 기준 `33` positions 유지, open orders `0`건이다. `AVGO`는 `5주`, `qty_available=5`, `RGTI`는 `49주`, `qty_available=49`, `SO`는 `5주`, `qty_available=5`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `0311` stale cleanup/core/research preflight를 source-of-record로 사용했고 scheduler-owned Alpaca core `get_clock/get_account_info/get_orders_open/get_all_positions/get_account_activities/get_stock_latest_quote/get_stock_snapshot` rows로 same-day fill discipline과 submit-boundary quote/spread를 재확인했다. same-day regular-session `AVGO` trim 1건과 after-hours `RGTI` trim fills 2건은 그대로 유지됐고, `AVGO`는 spread `1.8672%`가 policy cap을 크게 넘겨 trim hard gate fail, `RGTI`는 duplicate sell discipline, `SO`는 spread 회복 후에도 trim metric gap, 신규 buy path는 `review_backlog_pending_1d_count=14`와 benchmark floor cap에 막혀 이번 `0311` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-0311-hourly-autopilot-post-trade.json`

- Run: [[2026-06-09-0351-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler core preflight 기준 `32` positions 유지. open orders는 0건이고 `RGTI/AVGO/SO` 모두 신규 수량 변화 없이 유지됐다.
- Recent reconciliation scope: scheduler-owned `0351` stale cleanup/core/research preflight 기준 신규 buy는 `review_backlog_pending_1d_count=13` backlog throttle에 막혔고, sell-first 후보는 `RGTI` same-day duplicate, `AVGO` duplicate+spread `0.9471%`, `SO` spread `1.0799%` + decision-grade metric gap 때문에 submit되지 않았다. same-day filled orders는 `AVGO` 장외 sell 2건, `TSLA` exit 1건, `RGTI` trim 1건으로 총 4건 재확인됐다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-09-0351-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-12-0311-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned core preflight reconciliation 기준 `33` positions 유지, open orders `0`건이다. `AVGO`는 `5주`, `qty_available=5`, `RGTI`는 `49주`, `qty_available=49`, `SO`는 `5주`, `qty_available=5`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `0311` stale cleanup/core/research preflight를 source-of-record로 사용했고 scheduler-owned Alpaca core `get_clock/get_account_info/get_orders_open/get_all_positions/get_account_activities/get_stock_latest_quote/get_stock_snapshot` rows로 same-day fill discipline과 submit-boundary quote/spread를 재확인했다. same-day regular-session `AVGO` trim 1건과 after-hours `RGTI` trim fills 2건은 그대로 유지됐고, `AVGO`는 spread `1.8672%`가 policy cap을 크게 넘겨 trim hard gate fail, `RGTI`는 duplicate sell discipline, `SO`는 spread 회복 후에도 trim metric gap, 신규 buy path는 `review_backlog_pending_1d_count=14`와 benchmark floor cap에 막혀 이번 `0311` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-0311-hourly-autopilot-post-trade.json`

- Run: [[2026-06-09-0311-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler core preflight 기준 `32` positions 유지. open orders는 0건이고 `RGTI/AVGO/SO` 모두 신규 수량 변화 없이 유지됐다.
- Recent reconciliation scope: scheduler-owned `0311` stale cleanup/core/research preflight 기준 신규 buy는 `review_backlog_pending_1d_count=13` backlog throttle에 막혔고, sell-first 후보는 `RGTI` same-day duplicate, `AVGO` duplicate+spread `0.8130%`, `SO` decision-grade metric gap 때문에 submit되지 않았다. same-day filled orders는 `AVGO` 장외 sell 2건, `TSLA` exit 1건, `RGTI` trim 1건으로 총 4건 재확인됐다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-09-0311-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-12-0311-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned core preflight reconciliation 기준 `33` positions 유지, open orders `0`건이다. `AVGO`는 `5주`, `qty_available=5`, `RGTI`는 `49주`, `qty_available=49`, `SO`는 `5주`, `qty_available=5`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `0311` stale cleanup/core/research preflight를 source-of-record로 사용했고 scheduler-owned Alpaca core `get_clock/get_account_info/get_orders_open/get_all_positions/get_account_activities/get_stock_latest_quote/get_stock_snapshot` rows로 same-day fill discipline과 submit-boundary quote/spread를 재확인했다. same-day regular-session `AVGO` trim 1건과 after-hours `RGTI` trim fills 2건은 그대로 유지됐고, `AVGO`는 spread `1.8672%`가 policy cap을 크게 넘겨 trim hard gate fail, `RGTI`는 duplicate sell discipline, `SO`는 spread 회복 후에도 trim metric gap, 신규 buy path는 `review_backlog_pending_1d_count=14`와 benchmark floor cap에 막혀 이번 `0311` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-0311-hourly-autopilot-post-trade.json`

- Run: [[2026-06-09-0251-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler core preflight 기준 `32` positions 유지. open orders는 0건이고 `RGTI/AVGO/SO` 모두 신규 수량 변화 없이 유지됐다.
- Recent reconciliation scope: scheduler-owned `0251` stale cleanup/core/research preflight 기준 신규 buy는 `review_backlog_pending_1d_count=13` backlog throttle에 막혔고, sell-first 후보는 `RGTI` same-day duplicate, `AVGO` duplicate+spread `1.3592%`, `SO` decision-grade metric gap 때문에 submit되지 않았다. same-day filled orders는 `AVGO` 장외 sell 2건, `TSLA` exit 1건, `RGTI` trim 1건으로 총 4건 재확인됐다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-09-0251-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-12-0311-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned core preflight reconciliation 기준 `33` positions 유지, open orders `0`건이다. `AVGO`는 `5주`, `qty_available=5`, `RGTI`는 `49주`, `qty_available=49`, `SO`는 `5주`, `qty_available=5`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `0311` stale cleanup/core/research preflight를 source-of-record로 사용했고 scheduler-owned Alpaca core `get_clock/get_account_info/get_orders_open/get_all_positions/get_account_activities/get_stock_latest_quote/get_stock_snapshot` rows로 same-day fill discipline과 submit-boundary quote/spread를 재확인했다. same-day regular-session `AVGO` trim 1건과 after-hours `RGTI` trim fills 2건은 그대로 유지됐고, `AVGO`는 spread `1.8672%`가 policy cap을 크게 넘겨 trim hard gate fail, `RGTI`는 duplicate sell discipline, `SO`는 spread 회복 후에도 trim metric gap, 신규 buy path는 `review_backlog_pending_1d_count=14`와 benchmark floor cap에 막혀 이번 `0311` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-0311-hourly-autopilot-post-trade.json`

- Run: [[2026-06-09-0231-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler core preflight 기준 `32` positions 유지. open orders는 0건이고 `RGTI/AVGO/SO` 모두 신규 수량 변화 없이 유지됐다.
- Recent reconciliation scope: scheduler-owned `0231` stale cleanup/core/research preflight 기준 신규 buy는 `review_backlog_pending_1d_count=13` backlog throttle에 막혔고, sell-first 후보는 `RGTI` same-day duplicate, `AVGO` duplicate+spread `0.7420%`, `SO` spread `0.9153%` + metric gap 때문에 submit되지 않았다. same-day filled orders는 `AVGO` 장외 sell 2건, `TSLA` exit 1건, `RGTI` trim 1건으로 총 4건 재확인됐다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-09-0231-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-12-0311-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned core preflight reconciliation 기준 `33` positions 유지, open orders `0`건이다. `AVGO`는 `5주`, `qty_available=5`, `RGTI`는 `49주`, `qty_available=49`, `SO`는 `5주`, `qty_available=5`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `0311` stale cleanup/core/research preflight를 source-of-record로 사용했고 scheduler-owned Alpaca core `get_clock/get_account_info/get_orders_open/get_all_positions/get_account_activities/get_stock_latest_quote/get_stock_snapshot` rows로 same-day fill discipline과 submit-boundary quote/spread를 재확인했다. same-day regular-session `AVGO` trim 1건과 after-hours `RGTI` trim fills 2건은 그대로 유지됐고, `AVGO`는 spread `1.8672%`가 policy cap을 크게 넘겨 trim hard gate fail, `RGTI`는 duplicate sell discipline, `SO`는 spread 회복 후에도 trim metric gap, 신규 buy path는 `review_backlog_pending_1d_count=14`와 benchmark floor cap에 막혀 이번 `0311` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-0311-hourly-autopilot-post-trade.json`

- Run: [[2026-06-09-0211-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler core preflight 기준 `32` positions 유지. open orders는 0건이고 `RGTI/AVGO/SO` 모두 신규 수량 변화 없이 유지됐다.
- Recent reconciliation scope: scheduler-owned `0211` stale cleanup/core/research preflight 기준 신규 buy는 `review_backlog_pending_1d_count=13` backlog throttle에 막혔고, sell-first 후보는 `RGTI` same-day duplicate, `AVGO` duplicate+spread `0.9100%`, `SO` metric gap 때문에 submit되지 않았다. same-day filled orders는 `AVGO` 장외 sell 2건, `TSLA` exit 1건, `RGTI` trim 1건으로 총 4건 재확인됐다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-09-0211-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-12-0311-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned core preflight reconciliation 기준 `33` positions 유지, open orders `0`건이다. `AVGO`는 `5주`, `qty_available=5`, `RGTI`는 `49주`, `qty_available=49`, `SO`는 `5주`, `qty_available=5`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `0311` stale cleanup/core/research preflight를 source-of-record로 사용했고 scheduler-owned Alpaca core `get_clock/get_account_info/get_orders_open/get_all_positions/get_account_activities/get_stock_latest_quote/get_stock_snapshot` rows로 same-day fill discipline과 submit-boundary quote/spread를 재확인했다. same-day regular-session `AVGO` trim 1건과 after-hours `RGTI` trim fills 2건은 그대로 유지됐고, `AVGO`는 spread `1.8672%`가 policy cap을 크게 넘겨 trim hard gate fail, `RGTI`는 duplicate sell discipline, `SO`는 spread 회복 후에도 trim metric gap, 신규 buy path는 `review_backlog_pending_1d_count=14`와 benchmark floor cap에 막혀 이번 `0311` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-0311-hourly-autopilot-post-trade.json`

- Run: [[2026-06-09-0151-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler core preflight 기준 `32` positions 유지. open orders는 0건이고 `RGTI/AVGO/SO` 모두 신규 수량 변화 없이 유지됐다.
- Recent reconciliation scope: scheduler-owned `0151` stale cleanup/core/research preflight 기준 신규 buy는 `review_backlog_pending_1d_count=13` backlog throttle에 막혔고, sell-first 후보는 `RGTI` same-day duplicate, `AVGO` duplicate+spread `1.6445%`, `SO` metric gap 때문에 submit되지 않았다. same-day filled orders는 `AVGO` 장외 sell 2건, `TSLA` exit 1건, `RGTI` trim 1건으로 총 4건 재확인됐다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-09-0151-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-12-0311-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned core preflight reconciliation 기준 `33` positions 유지, open orders `0`건이다. `AVGO`는 `5주`, `qty_available=5`, `RGTI`는 `49주`, `qty_available=49`, `SO`는 `5주`, `qty_available=5`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `0311` stale cleanup/core/research preflight를 source-of-record로 사용했고 scheduler-owned Alpaca core `get_clock/get_account_info/get_orders_open/get_all_positions/get_account_activities/get_stock_latest_quote/get_stock_snapshot` rows로 same-day fill discipline과 submit-boundary quote/spread를 재확인했다. same-day regular-session `AVGO` trim 1건과 after-hours `RGTI` trim fills 2건은 그대로 유지됐고, `AVGO`는 spread `1.8672%`가 policy cap을 크게 넘겨 trim hard gate fail, `RGTI`는 duplicate sell discipline, `SO`는 spread 회복 후에도 trim metric gap, 신규 buy path는 `review_backlog_pending_1d_count=14`와 benchmark floor cap에 막혀 이번 `0311` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-0311-hourly-autopilot-post-trade.json`

- Run: [[2026-06-09-0131-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler core preflight 기준 `32` positions 유지. open orders는 0건이고 `RGTI/AVGO/SO` 모두 신규 수량 변화 없이 유지됐다.
- Recent reconciliation scope: scheduler-owned `0131` stale cleanup/core/research preflight 기준 신규 buy는 `review_backlog_pending_1d_count=13` backlog throttle에 막혔고, sell-first 후보는 `RGTI` same-day duplicate, `AVGO` duplicate+spread `1.3737%`, `SO` metric gap 때문에 submit되지 않았다. same-day filled orders는 `AVGO` 장외 sell 2건, `TSLA` exit 1건, `RGTI` trim 1건으로 총 4건 재확인됐다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-09-0131-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-12-0311-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned core preflight reconciliation 기준 `33` positions 유지, open orders `0`건이다. `AVGO`는 `5주`, `qty_available=5`, `RGTI`는 `49주`, `qty_available=49`, `SO`는 `5주`, `qty_available=5`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `0311` stale cleanup/core/research preflight를 source-of-record로 사용했고 scheduler-owned Alpaca core `get_clock/get_account_info/get_orders_open/get_all_positions/get_account_activities/get_stock_latest_quote/get_stock_snapshot` rows로 same-day fill discipline과 submit-boundary quote/spread를 재확인했다. same-day regular-session `AVGO` trim 1건과 after-hours `RGTI` trim fills 2건은 그대로 유지됐고, `AVGO`는 spread `1.8672%`가 policy cap을 크게 넘겨 trim hard gate fail, `RGTI`는 duplicate sell discipline, `SO`는 spread 회복 후에도 trim metric gap, 신규 buy path는 `review_backlog_pending_1d_count=14`와 benchmark floor cap에 막혀 이번 `0311` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-0311-hourly-autopilot-post-trade.json`

- Run: [[2026-06-09-0111-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime `get_all_positions` 기준 `32` positions 유지. open orders는 0건이고 `RGTI/AVGO/SO` 모두 신규 수량 변화 없이 유지됐다.
- Recent reconciliation scope: scheduler-owned `0111` stale cleanup/core/research preflight와 runtime `get_clock/get_orders(status=open)/get_orders(status=all, after=2026-06-08T00:00:00Z)/get_account_activities(activity_types=FILL)/get_all_positions/get_account_info/get_watchlists/get_stock_latest_quote(feed=iex)` 확인 기준 신규 buy는 `review_backlog_pending_1d_count=13` backlog throttle에 막혔고, sell-first 후보는 `RGTI` same-day duplicate, `AVGO` same-day duplicate, `SO` spread `6.8511%` + metric gap 때문에 submit되지 않았다. same-day filled orders는 `AVGO` 장외 sell 2건, `TSLA` exit 1건, `RGTI` trim 1건으로 총 4건 재확인됐다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-09-0111-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-12-0311-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned core preflight reconciliation 기준 `33` positions 유지, open orders `0`건이다. `AVGO`는 `5주`, `qty_available=5`, `RGTI`는 `49주`, `qty_available=49`, `SO`는 `5주`, `qty_available=5`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `0311` stale cleanup/core/research preflight를 source-of-record로 사용했고 scheduler-owned Alpaca core `get_clock/get_account_info/get_orders_open/get_all_positions/get_account_activities/get_stock_latest_quote/get_stock_snapshot` rows로 same-day fill discipline과 submit-boundary quote/spread를 재확인했다. same-day regular-session `AVGO` trim 1건과 after-hours `RGTI` trim fills 2건은 그대로 유지됐고, `AVGO`는 spread `1.8672%`가 policy cap을 크게 넘겨 trim hard gate fail, `RGTI`는 duplicate sell discipline, `SO`는 spread 회복 후에도 trim metric gap, 신규 buy path는 `review_backlog_pending_1d_count=14`와 benchmark floor cap에 막혀 이번 `0311` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-0311-hourly-autopilot-post-trade.json`

- Run: [[2026-06-09-0011-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler core preflight 기준 `32` positions 유지. open orders는 0건이고 `RGTI/AVGO/SO` 모두 신규 수량 변화 없이 유지됐다.
- Recent reconciliation scope: scheduler-owned `0011` stale cleanup/core/research preflight 기준 신규 buy는 `review_backlog_pending_1d_count=13` backlog throttle에 막혔고, sell-first 후보는 `RGTI` same-day duplicate, `AVGO` duplicate+spread `0.9722%`, `SO` metric gap 때문에 submit되지 않았다. same-day filled orders는 `AVGO` 장외 sell 2건, `TSLA` exit 1건, `RGTI` trim 1건으로 총 4건 재확인됐다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-09-0011-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-12-0311-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned core preflight reconciliation 기준 `33` positions 유지, open orders `0`건이다. `AVGO`는 `5주`, `qty_available=5`, `RGTI`는 `49주`, `qty_available=49`, `SO`는 `5주`, `qty_available=5`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `0311` stale cleanup/core/research preflight를 source-of-record로 사용했고 scheduler-owned Alpaca core `get_clock/get_account_info/get_orders_open/get_all_positions/get_account_activities/get_stock_latest_quote/get_stock_snapshot` rows로 same-day fill discipline과 submit-boundary quote/spread를 재확인했다. same-day regular-session `AVGO` trim 1건과 after-hours `RGTI` trim fills 2건은 그대로 유지됐고, `AVGO`는 spread `1.8672%`가 policy cap을 크게 넘겨 trim hard gate fail, `RGTI`는 duplicate sell discipline, `SO`는 spread 회복 후에도 trim metric gap, 신규 buy path는 `review_backlog_pending_1d_count=14`와 benchmark floor cap에 막혀 이번 `0311` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-0311-hourly-autopilot-post-trade.json`

- Run: [[2026-06-08-2351-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime `get_all_positions` 기준 `32` positions 유지. open orders는 0건이고 `RGTI/AVGO/SO` 모두 신규 수량 변화 없이 유지됐다.
- Recent reconciliation scope: scheduler-owned `2351` stale cleanup/core/research preflight와 runtime `get_watchlists/get_orders(status=open)/get_orders(status=all, after=2026-06-08T00:00:00Z)/get_stock_latest_quote(feed=iex)/get_account_info/get_all_positions` 확인 기준 신규 buy는 `review_backlog_pending_1d_count=13` backlog throttle에 막혔고, sell-first 후보는 `RGTI` same-day duplicate, `AVGO` same-day duplicate, `SO` metric gap 때문에 submit되지 않았다. same-day filled orders는 `AVGO` 장외 sell 2건, `TSLA` exit 1건, `RGTI` trim 1건으로 총 4건 재확인됐다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-08-2351-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-12-0311-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned core preflight reconciliation 기준 `33` positions 유지, open orders `0`건이다. `AVGO`는 `5주`, `qty_available=5`, `RGTI`는 `49주`, `qty_available=49`, `SO`는 `5주`, `qty_available=5`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `0311` stale cleanup/core/research preflight를 source-of-record로 사용했고 scheduler-owned Alpaca core `get_clock/get_account_info/get_orders_open/get_all_positions/get_account_activities/get_stock_latest_quote/get_stock_snapshot` rows로 same-day fill discipline과 submit-boundary quote/spread를 재확인했다. same-day regular-session `AVGO` trim 1건과 after-hours `RGTI` trim fills 2건은 그대로 유지됐고, `AVGO`는 spread `1.8672%`가 policy cap을 크게 넘겨 trim hard gate fail, `RGTI`는 duplicate sell discipline, `SO`는 spread 회복 후에도 trim metric gap, 신규 buy path는 `review_backlog_pending_1d_count=14`와 benchmark floor cap에 막혀 이번 `0311` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-0311-hourly-autopilot-post-trade.json`

- Run: [[2026-06-08-2331-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler core preflight 기준 `32` positions 유지. open orders는 0건이고 `RGTI/AVGO/SO` 모두 신규 수량 변화 없이 유지됐다.
- Recent reconciliation scope: scheduler-owned `2331` stale cleanup/core/research preflight와 runtime `get_watchlists/get_orders(status=open)/get_orders(status=all, after=2026-06-08T00:00:00Z)/get_stock_latest_quote(feed=iex)` 확인 기준 신규 buy는 `review_backlog_pending_1d_count=13` backlog throttle에 막혔고, sell-first 후보는 `RGTI` same-day duplicate, `AVGO` duplicate+spread, `SO` metric gap 때문에 submit되지 않았다. same-day filled orders는 `AVGO` 장외 sell 2건, `TSLA` exit 1건, `RGTI` trim 1건으로 총 4건 재확인됐다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-08-2331-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-12-0311-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned core preflight reconciliation 기준 `33` positions 유지, open orders `0`건이다. `AVGO`는 `5주`, `qty_available=5`, `RGTI`는 `49주`, `qty_available=49`, `SO`는 `5주`, `qty_available=5`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `0311` stale cleanup/core/research preflight를 source-of-record로 사용했고 scheduler-owned Alpaca core `get_clock/get_account_info/get_orders_open/get_all_positions/get_account_activities/get_stock_latest_quote/get_stock_snapshot` rows로 same-day fill discipline과 submit-boundary quote/spread를 재확인했다. same-day regular-session `AVGO` trim 1건과 after-hours `RGTI` trim fills 2건은 그대로 유지됐고, `AVGO`는 spread `1.8672%`가 policy cap을 크게 넘겨 trim hard gate fail, `RGTI`는 duplicate sell discipline, `SO`는 spread 회복 후에도 trim metric gap, 신규 buy path는 `review_backlog_pending_1d_count=14`와 benchmark floor cap에 막혀 이번 `0311` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-0311-hourly-autopilot-post-trade.json`

- Run: [[2026-06-08-2311-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler core preflight 기준 `32` positions 유지. open orders는 0건이고 `RGTI/AVGO/SO` 모두 신규 수량 변화 없이 유지됐다.
- Recent reconciliation scope: scheduler-owned `2311` stale cleanup/core/research preflight와 runtime `get_watchlists/get_orders(status=open)/get_orders(status=all, after=2026-06-08T00:00:00Z)/get_stock_latest_quote(feed=iex)` 확인 기준 신규 buy는 `review_backlog_pending_1d_count=13` backlog throttle에 막혔고, sell-first 후보는 `RGTI` same-day duplicate, `AVGO` duplicate+spread, `SO` metric gap 때문에 submit되지 않았다. same-day filled orders는 `AVGO` 장외 sell 2건, `TSLA` exit 1건, `RGTI` trim 1건으로 총 4건 재확인됐다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-08-2311-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-12-0311-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned core preflight reconciliation 기준 `33` positions 유지, open orders `0`건이다. `AVGO`는 `5주`, `qty_available=5`, `RGTI`는 `49주`, `qty_available=49`, `SO`는 `5주`, `qty_available=5`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `0311` stale cleanup/core/research preflight를 source-of-record로 사용했고 scheduler-owned Alpaca core `get_clock/get_account_info/get_orders_open/get_all_positions/get_account_activities/get_stock_latest_quote/get_stock_snapshot` rows로 same-day fill discipline과 submit-boundary quote/spread를 재확인했다. same-day regular-session `AVGO` trim 1건과 after-hours `RGTI` trim fills 2건은 그대로 유지됐고, `AVGO`는 spread `1.8672%`가 policy cap을 크게 넘겨 trim hard gate fail, `RGTI`는 duplicate sell discipline, `SO`는 spread 회복 후에도 trim metric gap, 신규 buy path는 `review_backlog_pending_1d_count=14`와 benchmark floor cap에 막혀 이번 `0311` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-0311-hourly-autopilot-post-trade.json`

- Run: [[2026-06-08-2251-hourly-autopilot]]
- Open/new: 없음
- Filled: `RGTI` sell 30 @ `21.48` (`client_order_id=hourly-20260608-2251-sell-rgti`)가 regular-session runtime reconciliation 기준 전량 체결됐다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime `get_all_positions` 기준 `32` positions. `RGTI`는 `120 -> 90`으로 감소했고 open orders는 0건이다.
- Recent reconciliation scope: scheduler-owned `2251` stale cleanup/core/research preflight와 runtime `get_watchlists/get_orders(status=open)/get_orders(status=all, after=2026-06-08T00:00:00Z)/get_account_activities(activity_types=FILL, after=2026-06-08T00:00:00Z)/get_all_positions/get_account_info/place_stock_order` 확인 기준 review backlog throttle로 신규 buy는 계속 차단됐지만 risk-reducing sell 경로에서 `RGTI` 30주 trim이 허용됐다. post-trade account snapshot은 portfolio value `99,552.10 USD`, cash `31,774.85 USD`, buying power `300,430.68 USD`, long market value `67,777.25 USD`다.
- Orders submitted/replaced/cancelled/closed by this workflow: 1 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-08-2251-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-12-0311-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned core preflight reconciliation 기준 `33` positions 유지, open orders `0`건이다. `AVGO`는 `5주`, `qty_available=5`, `RGTI`는 `49주`, `qty_available=49`, `SO`는 `5주`, `qty_available=5`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `0311` stale cleanup/core/research preflight를 source-of-record로 사용했고 scheduler-owned Alpaca core `get_clock/get_account_info/get_orders_open/get_all_positions/get_account_activities/get_stock_latest_quote/get_stock_snapshot` rows로 same-day fill discipline과 submit-boundary quote/spread를 재확인했다. same-day regular-session `AVGO` trim 1건과 after-hours `RGTI` trim fills 2건은 그대로 유지됐고, `AVGO`는 spread `1.8672%`가 policy cap을 크게 넘겨 trim hard gate fail, `RGTI`는 duplicate sell discipline, `SO`는 spread 회복 후에도 trim metric gap, 신규 buy path는 `review_backlog_pending_1d_count=14`와 benchmark floor cap에 막혀 이번 `0311` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-0311-hourly-autopilot-post-trade.json`

- Run: [[2026-06-08-2231-hourly-autopilot]]
- Open/new: 없음
- Filled: `TSLA` sell 1 @ `398.59` (`client_order_id=hourly-20260608-2231-sell-tsla`)가 regular-session runtime reconciliation 기준 즉시 체결됐다.
- Cancelled: 없음
- Position count observed by Alpaca MCP: runtime `get_all_positions` 기준 `32` positions. `TSLA`는 계좌 포지션에서 제거됐고 open orders는 0건이다.
- Recent reconciliation scope: scheduler-owned `2231` stale cleanup/core/research preflight와 runtime `get_watchlists/get_orders(status=open)/get_orders(status=all, after=2026-06-08T00:00:00Z)/get_all_positions/get_account_info/place_stock_order` 확인 기준 review backlog throttle로 신규 buy는 차단됐지만 risk-reducing sell 경로에서 `TSLA` 1주 exit가 허용됐다. post-trade account snapshot은 portfolio value `99,862.11 USD`, cash `31,130.45 USD`, buying power `300,491.66 USD`, long market value `68,731.66 USD`다.
- Orders submitted/replaced/cancelled/closed by this workflow: 1 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-08-2231-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-12-0311-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned core preflight reconciliation 기준 `33` positions 유지, open orders `0`건이다. `AVGO`는 `5주`, `qty_available=5`, `RGTI`는 `49주`, `qty_available=49`, `SO`는 `5주`, `qty_available=5`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `0311` stale cleanup/core/research preflight를 source-of-record로 사용했고 scheduler-owned Alpaca core `get_clock/get_account_info/get_orders_open/get_all_positions/get_account_activities/get_stock_latest_quote/get_stock_snapshot` rows로 same-day fill discipline과 submit-boundary quote/spread를 재확인했다. same-day regular-session `AVGO` trim 1건과 after-hours `RGTI` trim fills 2건은 그대로 유지됐고, `AVGO`는 spread `1.8672%`가 policy cap을 크게 넘겨 trim hard gate fail, `RGTI`는 duplicate sell discipline, `SO`는 spread 회복 후에도 trim metric gap, 신규 buy path는 `review_backlog_pending_1d_count=14`와 benchmark floor cap에 막혀 이번 `0311` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-0311-hourly-autopilot-post-trade.json`

- Run: [[2026-06-06-0451-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: `NKE` buy 1 @ `43.20` (`client_order_id=hourly-20260606-0451-buy-nke`)는 actual submit timestamp가 `2026-06-05T20:00:07.873287392Z` (`16:00:07 ET`)로 regular close 이후에 기록돼 즉시 취소됐다.
- Position count observed by Alpaca MCP: latest confirmed `0451` scheduler core preflight 기준 `33` positions 유지. 추가 `NKE` fill은 없고 standing order도 남기지 않았다.
- Recent reconciliation scope: scheduler-owned `0451` stale cleanup/core/research preflight와 runtime `place_stock_order/get_order_by_client_id/get_order_by_id/get_clock/cancel_order_by_id/get_orders(status=all, symbols=NKE, after=2026-06-05T04:00:00Z)` 확인 기준 close-race submit을 cancel로 복구했다. last confirmed account snapshot은 portfolio value `98,361.48 USD`, cash `29,947.81 USD`, buying power `245,113.34 USD`, long market value `68,413.67 USD`다.
- Orders submitted/replaced/cancelled/closed by this workflow: 1 / 0 / 1 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-06-0451-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-12-0311-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned core preflight reconciliation 기준 `33` positions 유지, open orders `0`건이다. `AVGO`는 `5주`, `qty_available=5`, `RGTI`는 `49주`, `qty_available=49`, `SO`는 `5주`, `qty_available=5`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `0311` stale cleanup/core/research preflight를 source-of-record로 사용했고 scheduler-owned Alpaca core `get_clock/get_account_info/get_orders_open/get_all_positions/get_account_activities/get_stock_latest_quote/get_stock_snapshot` rows로 same-day fill discipline과 submit-boundary quote/spread를 재확인했다. same-day regular-session `AVGO` trim 1건과 after-hours `RGTI` trim fills 2건은 그대로 유지됐고, `AVGO`는 spread `1.8672%`가 policy cap을 크게 넘겨 trim hard gate fail, `RGTI`는 duplicate sell discipline, `SO`는 spread 회복 후에도 trim metric gap, 신규 buy path는 `review_backlog_pending_1d_count=14`와 benchmark floor cap에 막혀 이번 `0311` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-0311-hourly-autopilot-post-trade.json`

- Run: [[2026-06-06-0431-hourly-autopilot]]
- Open/new: 없음
- Filled: `INTC` sell 1 @ `99.93` (`client_order_id=hourly-20260606-0411-sell-intc`)가 0431 core preflight recent activities에서 confirmed fill로 확인됐다.
- Cancelled: `NEE` same-day buy `hourly-20260606-0231-buy-nee`는 `2026-06-05T18:31:08.289816Z` canceled 상태가 runtime all-orders reconciliation에서 재확인됐다.
- Position count observed by Alpaca MCP: scheduler core preflight 기준 `33` positions. `INTC`는 계좌 포지션에서 제거됐고 open orders는 0건이다.
- Recent reconciliation scope: scheduler-owned `0431` stale cleanup/core/research preflight와 runtime `get_clock/get_account_info/get_orders(status=all, symbols=NEE,NKE,TSLA,SO,AVGO, after=2026-06-05T04:00:00Z)` 확인 기준 새 submit attempt는 없었다. account snapshot은 portfolio value `98,445.76 USD`, cash `29,947.81 USD`, buying power `245,318.08 USD`, long market value `68,497.95 USD`다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-06-0431-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-12-0311-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned core preflight reconciliation 기준 `33` positions 유지, open orders `0`건이다. `AVGO`는 `5주`, `qty_available=5`, `RGTI`는 `49주`, `qty_available=49`, `SO`는 `5주`, `qty_available=5`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `0311` stale cleanup/core/research preflight를 source-of-record로 사용했고 scheduler-owned Alpaca core `get_clock/get_account_info/get_orders_open/get_all_positions/get_account_activities/get_stock_latest_quote/get_stock_snapshot` rows로 same-day fill discipline과 submit-boundary quote/spread를 재확인했다. same-day regular-session `AVGO` trim 1건과 after-hours `RGTI` trim fills 2건은 그대로 유지됐고, `AVGO`는 spread `1.8672%`가 policy cap을 크게 넘겨 trim hard gate fail, `RGTI`는 duplicate sell discipline, `SO`는 spread 회복 후에도 trim metric gap, 신규 buy path는 `review_backlog_pending_1d_count=14`와 benchmark floor cap에 막혀 이번 `0311` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-0311-hourly-autopilot-post-trade.json`

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

- Run: [[2026-06-12-0311-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned core preflight reconciliation 기준 `33` positions 유지, open orders `0`건이다. `AVGO`는 `5주`, `qty_available=5`, `RGTI`는 `49주`, `qty_available=49`, `SO`는 `5주`, `qty_available=5`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `0311` stale cleanup/core/research preflight를 source-of-record로 사용했고 scheduler-owned Alpaca core `get_clock/get_account_info/get_orders_open/get_all_positions/get_account_activities/get_stock_latest_quote/get_stock_snapshot` rows로 same-day fill discipline과 submit-boundary quote/spread를 재확인했다. same-day regular-session `AVGO` trim 1건과 after-hours `RGTI` trim fills 2건은 그대로 유지됐고, `AVGO`는 spread `1.8672%`가 policy cap을 크게 넘겨 trim hard gate fail, `RGTI`는 duplicate sell discipline, `SO`는 spread 회복 후에도 trim metric gap, 신규 buy path는 `review_backlog_pending_1d_count=14`와 benchmark floor cap에 막혀 이번 `0311` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-0311-hourly-autopilot-post-trade.json`

- Run: [[2026-06-06-0351-hourly-autopilot]]
- Open/new: 없음
- Filled: `JPM` buy 1 @ `311.81` (`client_order_id=hourly-20260606-0351-buy-jpm`)
- Cancelled: post-submit `get_orders(status=open, symbols=JPM)` 1건은 tool layer에서 cancelled 되었지만 filled lookup/positions/account reconciliation은 성공했다.
- Position count observed by Alpaca MCP: post-trade runtime `34` positions. `JPM` 신규 보유 `1주 @ 311.81`, `AVGO`는 직전 trim 이후 `12주` 유지다.
- Recent reconciliation scope: scheduler-owned `0351` stale cleanup/core/research preflight와 runtime `get_clock/place_stock_order/get_order_by_client_id/get_all_positions/get_account_info` 확인 기준 `JPM` 1주 regular-session validation buy가 Alpaca order id `dc6e7545-bf7d-47a1-a257-fc5c82866680`로 제출돼 `2026-06-05T19:02:33.577640965Z`에 `311.81 USD`로 체결됐다. post-trade `get_account_info`는 portfolio value `98,378.18 USD`, cash `29,847.88 USD`, buying power `244,983.06 USD`, long market value `68,530.30 USD`를 기록했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 1 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-06-0351-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-12-0311-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned core preflight reconciliation 기준 `33` positions 유지, open orders `0`건이다. `AVGO`는 `5주`, `qty_available=5`, `RGTI`는 `49주`, `qty_available=49`, `SO`는 `5주`, `qty_available=5`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `0311` stale cleanup/core/research preflight를 source-of-record로 사용했고 scheduler-owned Alpaca core `get_clock/get_account_info/get_orders_open/get_all_positions/get_account_activities/get_stock_latest_quote/get_stock_snapshot` rows로 same-day fill discipline과 submit-boundary quote/spread를 재확인했다. same-day regular-session `AVGO` trim 1건과 after-hours `RGTI` trim fills 2건은 그대로 유지됐고, `AVGO`는 spread `1.8672%`가 policy cap을 크게 넘겨 trim hard gate fail, `RGTI`는 duplicate sell discipline, `SO`는 spread 회복 후에도 trim metric gap, 신규 buy path는 `review_backlog_pending_1d_count=14`와 benchmark floor cap에 막혀 이번 `0311` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-0311-hourly-autopilot-post-trade.json`

- Run: [[2026-06-06-0331-hourly-autopilot]]
- Open/new: 없음
- Filled: `AVGO` sell 4 @ `389.25` (`client_order_id=hourly-20260606-0331-sell-avgo`)
- Cancelled: 첫 submit 시도 1건은 tool safety cancellation으로 반환됐지만 동일 idempotent client id reconciliation 후 재시도에서 실제 주문이 생성·체결됐다.
- Position count observed by Alpaca MCP: post-trade runtime `33` positions. `AVGO`는 `16주 -> 12주`, `SO`는 직전 fill 반영 상태인 `5주` 유지다.
- Recent reconciliation scope: scheduler-owned `0331` stale cleanup/core/research preflight와 runtime `get_clock/get_account_info/get_all_positions/get_orders(status=open)/get_orders(status=all, after=2026-06-05T04:00:00Z)/get_stock_latest_quote/get_asset/place_stock_order/get_order_by_client_id/get_order_by_id` 확인 기준 stale cleanup 파일의 `CVX`/`NEE` open-order 모순은 실제 Alpaca 상태에서 `2026-06-05T18:31:08Z` canceled로 해소됐다. 이후 `AVGO` 4주 regular-session trim이 Alpaca order id `3a911e61-97c5-4431-bff6-8c9c812ea311`로 제출돼 `2026-06-05T18:37:44.452055748Z`에 `389.25 USD`로 체결됐다. post-trade `get_account_info`는 portfolio value `98,237.81 USD`, cash `30,159.69 USD`, buying power `245,462.62 USD`, long market value `68,078.12 USD`를 기록했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 1 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-06-0331-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-12-0311-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned core preflight reconciliation 기준 `33` positions 유지, open orders `0`건이다. `AVGO`는 `5주`, `qty_available=5`, `RGTI`는 `49주`, `qty_available=49`, `SO`는 `5주`, `qty_available=5`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `0311` stale cleanup/core/research preflight를 source-of-record로 사용했고 scheduler-owned Alpaca core `get_clock/get_account_info/get_orders_open/get_all_positions/get_account_activities/get_stock_latest_quote/get_stock_snapshot` rows로 same-day fill discipline과 submit-boundary quote/spread를 재확인했다. same-day regular-session `AVGO` trim 1건과 after-hours `RGTI` trim fills 2건은 그대로 유지됐고, `AVGO`는 spread `1.8672%`가 policy cap을 크게 넘겨 trim hard gate fail, `RGTI`는 duplicate sell discipline, `SO`는 spread 회복 후에도 trim metric gap, 신규 buy path는 `review_backlog_pending_1d_count=14`와 benchmark floor cap에 막혀 이번 `0311` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-0311-hourly-autopilot-post-trade.json`

- Run: [[2026-06-06-0311-hourly-autopilot]]
- Open/new: `NEE` buy 1 @ `85.47` (`client_order_id=hourly-20260606-0231-buy-nee`, `status=new`), `CVX` buy 1 @ `187.68` (`client_order_id=hourly-20260606-0251-buy-cvx`, `status=new`), `SO` buy 1 @ `93.32` (`client_order_id=hourly-20260606-0311-buy-so`, `status=new`)
- Filled: 없음
- Cancelled: 첫 submit 시도 1건은 tool safety cancellation으로 반환됐지만 동일 idempotent client id reconcile 후 재시도에서 open order가 생성됐다.
- Position count observed by Alpaca MCP: latest confirmed pre-submit positions snapshot 기준 `33` positions 유지. `SO`는 아직 `4주 @ 92.54`다.
- Recent reconciliation scope: scheduler-owned `0311` stale cleanup/core/research preflight와 runtime `get_clock/get_account_info/get_orders(status=open)/get_stock_latest_quote/get_asset/get_order_by_client_id/get_order_by_id` 확인 기준 `SO` 1주 regular-session validation add가 Alpaca order id `dcf8d47c-979f-469c-a22c-06d04c5a25f1`로 생성됐고 direct lookup 기준 `status=new`, `filled_qty=0`이다. post-submit `get_all_positions`는 tool layer에서 cancelled 되었지만 post-submit `get_account_info`는 성공해 portfolio value `98,610.82 USD`, cash `28,696.01 USD`, buying power `242,395.53 USD`, long market value `69,914.81 USD`를 기록했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 1 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-06-0311-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-12-0311-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned core preflight reconciliation 기준 `33` positions 유지, open orders `0`건이다. `AVGO`는 `5주`, `qty_available=5`, `RGTI`는 `49주`, `qty_available=49`, `SO`는 `5주`, `qty_available=5`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `0311` stale cleanup/core/research preflight를 source-of-record로 사용했고 scheduler-owned Alpaca core `get_clock/get_account_info/get_orders_open/get_all_positions/get_account_activities/get_stock_latest_quote/get_stock_snapshot` rows로 same-day fill discipline과 submit-boundary quote/spread를 재확인했다. same-day regular-session `AVGO` trim 1건과 after-hours `RGTI` trim fills 2건은 그대로 유지됐고, `AVGO`는 spread `1.8672%`가 policy cap을 크게 넘겨 trim hard gate fail, `RGTI`는 duplicate sell discipline, `SO`는 spread 회복 후에도 trim metric gap, 신규 buy path는 `review_backlog_pending_1d_count=14`와 benchmark floor cap에 막혀 이번 `0311` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-0311-hourly-autopilot-post-trade.json`

- Run: [[2026-06-06-0251-hourly-autopilot]]
- Open/new: `NEE` buy 1 @ `85.47` (`client_order_id=hourly-20260606-0231-buy-nee`, `status=new`), `CVX` buy 1 @ `187.68` (`client_order_id=hourly-20260606-0251-buy-cvx`, `status=new`)
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: latest confirmed positions snapshot 기준 `33` positions 유지. `CVX`는 아직 `1주 @ 184.03`이다.
- Recent reconciliation scope: scheduler-owned `0251` stale cleanup/core/research preflight와 runtime `place_stock_order/get_order_by_client_id/get_order_by_id` 확인 기준 `CVX` 1주 regular-session validation add가 Alpaca order id `5fbf3e4a-cd4d-4551-88ef-d14fb2dd78fe`로 생성됐고 direct lookup 기준 `status=new`, `filled_qty=0`이다. post-submit `get_all_positions/get_open_position/get_stock_latest_trade`는 tool layer에서 cancelled 되어 계좌 수치는 last confirmed pre-submit snapshot인 portfolio value `99,069.12 USD`, cash `28,696.01 USD`, buying power `243,685.21 USD`, long market value `70,373.11 USD`를 유지 기록한다.
- Orders submitted/replaced/cancelled/closed by this workflow: 1 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-06-0251-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-12-0311-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned core preflight reconciliation 기준 `33` positions 유지, open orders `0`건이다. `AVGO`는 `5주`, `qty_available=5`, `RGTI`는 `49주`, `qty_available=49`, `SO`는 `5주`, `qty_available=5`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `0311` stale cleanup/core/research preflight를 source-of-record로 사용했고 scheduler-owned Alpaca core `get_clock/get_account_info/get_orders_open/get_all_positions/get_account_activities/get_stock_latest_quote/get_stock_snapshot` rows로 same-day fill discipline과 submit-boundary quote/spread를 재확인했다. same-day regular-session `AVGO` trim 1건과 after-hours `RGTI` trim fills 2건은 그대로 유지됐고, `AVGO`는 spread `1.8672%`가 policy cap을 크게 넘겨 trim hard gate fail, `RGTI`는 duplicate sell discipline, `SO`는 spread 회복 후에도 trim metric gap, 신규 buy path는 `review_backlog_pending_1d_count=14`와 benchmark floor cap에 막혀 이번 `0311` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-0311-hourly-autopilot-post-trade.json`

- Run: [[2026-06-06-0231-hourly-autopilot]]
- Open/new: `NEE` buy 1 @ `85.47` (`client_order_id=hourly-20260606-0231-buy-nee`, `status=new`)
- Filled: 없음
- Cancelled: 첫 submit 시도 1건은 safety cancellation으로 반환됐지만 동일 idempotent client id reconcile 후 재시도에서 open order가 생성됐다.
- Position count observed by Alpaca MCP: scheduler core preflight 기준 `33` positions 유지. `NEE`는 latest confirmed positions snapshot 기준 아직 `4주`다.
- Recent reconciliation scope: scheduler-owned `0231` stale cleanup/core/research preflight와 runtime `place_stock_order/get_order_by_client_id/get_order_by_id/get_orders(status=all, symbols=NEE, after=2026-06-05T04:00:00Z)/get_orders(status=all, symbols=NEE, after=2026-06-05T17:40:00Z)` 확인 기준 첫 submit cancellation 후 `hourly-20260606-0231-buy-nee`를 동일 id로 1회만 재시도했고, Alpaca order id `202d7a0d-c061-4385-a693-b91f403a2b4f`가 `2026-06-05T17:43:45.162494138Z`에 `status=new`로 생성됐다. `get_orders(status=open, symbols=NEE)`와 post-submit market/account/positions refresh는 tool layer에서 cancelled 되어 계좌 수치는 last confirmed pre-submit snapshot인 portfolio value `99,123.29 USD`, cash `28,696.01 USD`, buying power `243,948.52 USD`, long market value `70,427.28 USD`를 유지 기록했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 1 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-06-0231-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-12-0311-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned core preflight reconciliation 기준 `33` positions 유지, open orders `0`건이다. `AVGO`는 `5주`, `qty_available=5`, `RGTI`는 `49주`, `qty_available=49`, `SO`는 `5주`, `qty_available=5`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `0311` stale cleanup/core/research preflight를 source-of-record로 사용했고 scheduler-owned Alpaca core `get_clock/get_account_info/get_orders_open/get_all_positions/get_account_activities/get_stock_latest_quote/get_stock_snapshot` rows로 same-day fill discipline과 submit-boundary quote/spread를 재확인했다. same-day regular-session `AVGO` trim 1건과 after-hours `RGTI` trim fills 2건은 그대로 유지됐고, `AVGO`는 spread `1.8672%`가 policy cap을 크게 넘겨 trim hard gate fail, `RGTI`는 duplicate sell discipline, `SO`는 spread 회복 후에도 trim metric gap, 신규 buy path는 `review_backlog_pending_1d_count=14`와 benchmark floor cap에 막혀 이번 `0311` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-0311-hourly-autopilot-post-trade.json`

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

- Run: [[2026-06-12-0311-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned core preflight reconciliation 기준 `33` positions 유지, open orders `0`건이다. `AVGO`는 `5주`, `qty_available=5`, `RGTI`는 `49주`, `qty_available=49`, `SO`는 `5주`, `qty_available=5`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `0311` stale cleanup/core/research preflight를 source-of-record로 사용했고 scheduler-owned Alpaca core `get_clock/get_account_info/get_orders_open/get_all_positions/get_account_activities/get_stock_latest_quote/get_stock_snapshot` rows로 same-day fill discipline과 submit-boundary quote/spread를 재확인했다. same-day regular-session `AVGO` trim 1건과 after-hours `RGTI` trim fills 2건은 그대로 유지됐고, `AVGO`는 spread `1.8672%`가 policy cap을 크게 넘겨 trim hard gate fail, `RGTI`는 duplicate sell discipline, `SO`는 spread 회복 후에도 trim metric gap, 신규 buy path는 `review_backlog_pending_1d_count=14`와 benchmark floor cap에 막혀 이번 `0311` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-0311-hourly-autopilot-post-trade.json`

- Run: [[2026-06-06-0151-hourly-autopilot]]
- Open/new: 없음
- Filled: `AMZN` buy 1 @ `253.17` (`client_order_id=hourly-20260606-0151-buy-amzn`)
- Cancelled: 없음
- Position count observed by Alpaca MCP: post-submit runtime `33` positions. `AMZN`은 `3주 -> 4주`, 평균단가 `271.12 -> 266.6325`로 갱신됐다.
- Recent reconciliation scope: scheduler-owned `0151` stale cleanup/core/research preflight와 runtime `get_account_info/get_orders(status=open)/place_stock_order/get_order_by_client_id/get_orders(status=all, symbols=AMZN, after=2026-06-05T04:00:00Z)/get_account_activities(FILL)/get_all_positions` 확인 기준 `AMZN` 1주 regular-session validation add가 Alpaca order id `ccfc1bb3-2f8a-4752-8185-a6b230ef6bad`로 제출됐고 `2026-06-05T17:01:54.545263432Z`에 `253.17 USD`로 체결됐다. post-submit `get_account_info` refresh는 tool safety monitor가 막혀 cash는 pre-submit `28,975.27 USD`에서 confirmed fill notional을 차감한 `28,722.10 USD` 추정치로 기록했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 1 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-06-0151-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-12-0311-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned core preflight reconciliation 기준 `33` positions 유지, open orders `0`건이다. `AVGO`는 `5주`, `qty_available=5`, `RGTI`는 `49주`, `qty_available=49`, `SO`는 `5주`, `qty_available=5`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `0311` stale cleanup/core/research preflight를 source-of-record로 사용했고 scheduler-owned Alpaca core `get_clock/get_account_info/get_orders_open/get_all_positions/get_account_activities/get_stock_latest_quote/get_stock_snapshot` rows로 same-day fill discipline과 submit-boundary quote/spread를 재확인했다. same-day regular-session `AVGO` trim 1건과 after-hours `RGTI` trim fills 2건은 그대로 유지됐고, `AVGO`는 spread `1.8672%`가 policy cap을 크게 넘겨 trim hard gate fail, `RGTI`는 duplicate sell discipline, `SO`는 spread 회복 후에도 trim metric gap, 신규 buy path는 `review_backlog_pending_1d_count=14`와 benchmark floor cap에 막혀 이번 `0311` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-0311-hourly-autopilot-post-trade.json`

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

- Run: [[2026-06-12-0311-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned core preflight reconciliation 기준 `33` positions 유지, open orders `0`건이다. `AVGO`는 `5주`, `qty_available=5`, `RGTI`는 `49주`, `qty_available=49`, `SO`는 `5주`, `qty_available=5`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `0311` stale cleanup/core/research preflight를 source-of-record로 사용했고 scheduler-owned Alpaca core `get_clock/get_account_info/get_orders_open/get_all_positions/get_account_activities/get_stock_latest_quote/get_stock_snapshot` rows로 same-day fill discipline과 submit-boundary quote/spread를 재확인했다. same-day regular-session `AVGO` trim 1건과 after-hours `RGTI` trim fills 2건은 그대로 유지됐고, `AVGO`는 spread `1.8672%`가 policy cap을 크게 넘겨 trim hard gate fail, `RGTI`는 duplicate sell discipline, `SO`는 spread 회복 후에도 trim metric gap, 신규 buy path는 `review_backlog_pending_1d_count=14`와 benchmark floor cap에 막혀 이번 `0311` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-0311-hourly-autopilot-post-trade.json`

- Run: [[2026-06-06-0051-hourly-autopilot]]
- Open/new: `NVDA` buy 1 @ `208.80` (`client_order_id=hourly-20260606-0051-buy-nvda`, `status=new`)
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: 33 positions 유지. `NVDA`는 runtime `get_all_positions` 기준 아직 37주이며 신규 주문은 미체결 상태다.
- Recent reconciliation scope: scheduler-owned `0051` stale cleanup/core/research preflight와 runtime `get_clock/get_orders(status=open)/get_orders(status=all, after=2026-06-05T04:00:00Z)/get_account_activities(FILL)/place_stock_order/get_order_by_client_id/get_orders(status=open, symbols=NVDA)/get_orders(status=all, symbols=NVDA, after=2026-06-05T04:00:00Z)/get_all_positions` 확인 기준 `NVDA` 1주 regular-session validation add를 제출했고 Alpaca order id `93f2530d-3f49-4705-8640-664357426b14`가 `2026-06-05T15:59:35.508322723Z`에 `status=new`로 생성됐다. post-submit `get_account_info`와 `get_account_activities(FILL)` refresh는 safety monitor가 취소돼 계좌 수치는 last confirmed pre-submit snapshot인 portfolio value `99,938.01 USD`, cash `29,357.09 USD`, buying power `246,445.79 USD`, long market value `70,580.92 USD`를 유지 기록했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 1 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-06-0051-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-12-0311-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned core preflight reconciliation 기준 `33` positions 유지, open orders `0`건이다. `AVGO`는 `5주`, `qty_available=5`, `RGTI`는 `49주`, `qty_available=49`, `SO`는 `5주`, `qty_available=5`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `0311` stale cleanup/core/research preflight를 source-of-record로 사용했고 scheduler-owned Alpaca core `get_clock/get_account_info/get_orders_open/get_all_positions/get_account_activities/get_stock_latest_quote/get_stock_snapshot` rows로 same-day fill discipline과 submit-boundary quote/spread를 재확인했다. same-day regular-session `AVGO` trim 1건과 after-hours `RGTI` trim fills 2건은 그대로 유지됐고, `AVGO`는 spread `1.8672%`가 policy cap을 크게 넘겨 trim hard gate fail, `RGTI`는 duplicate sell discipline, `SO`는 spread 회복 후에도 trim metric gap, 신규 buy path는 `review_backlog_pending_1d_count=14`와 benchmark floor cap에 막혀 이번 `0311` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-0311-hourly-autopilot-post-trade.json`

- Run: [[2026-06-06-0031-hourly-autopilot]]
- Open/new: 없음
- Filled: `V` buy 1 @ `321.90` (`client_order_id=hourly-20260606-0031-buy-v`)
- Cancelled: 없음
- Position count observed by Alpaca MCP: 33 positions 유지. `V`는 runtime `get_all_positions` 기준 3주에서 4주, 평균단가 `326.946667`에서 `325.685`로 갱신됐다.
- Recent reconciliation scope: scheduler-owned `0031` stale cleanup/core/research preflight와 runtime `get_orders(status=open)/get_orders(status=all, after=2026-06-05T04:00:00Z)/place_stock_order/get_order_by_client_id/get_orders(status=open, symbols=V)/get_orders(status=all, symbols=V, after=2026-06-05T04:00:00Z)/get_all_positions` 확인 기준 `V` 1주 regular-session validation add가 `2026-06-05T15:37:28.378344604Z`에 `321.90 USD`로 즉시 체결됐다. post-submit `get_account_info`와 `get_account_activities(FILL)`는 tool layer에서 cancelled 되었지만, last confirmed pre-submit account snapshot과 confirmed fill, 최신 포지션 합계를 결합해 cash `29,357.09 USD`, inferred portfolio value `100,055.85 USD`, long market value `70,698.76 USD`로 기록했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 1 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-06-0031-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-12-0311-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned core preflight reconciliation 기준 `33` positions 유지, open orders `0`건이다. `AVGO`는 `5주`, `qty_available=5`, `RGTI`는 `49주`, `qty_available=49`, `SO`는 `5주`, `qty_available=5`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `0311` stale cleanup/core/research preflight를 source-of-record로 사용했고 scheduler-owned Alpaca core `get_clock/get_account_info/get_orders_open/get_all_positions/get_account_activities/get_stock_latest_quote/get_stock_snapshot` rows로 same-day fill discipline과 submit-boundary quote/spread를 재확인했다. same-day regular-session `AVGO` trim 1건과 after-hours `RGTI` trim fills 2건은 그대로 유지됐고, `AVGO`는 spread `1.8672%`가 policy cap을 크게 넘겨 trim hard gate fail, `RGTI`는 duplicate sell discipline, `SO`는 spread 회복 후에도 trim metric gap, 신규 buy path는 `review_backlog_pending_1d_count=14`와 benchmark floor cap에 막혀 이번 `0311` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-0311-hourly-autopilot-post-trade.json`

- Run: [[2026-06-06-0011-hourly-autopilot]]
- Open/new: 없음
- Filled: `AAPL` buy 1 @ `313.27` (`client_order_id=hourly-20260606-0011-buy-aapl`)
- Cancelled: 없음
- Position count observed by Alpaca MCP: 33 positions 유지. `AAPL`는 runtime `get_all_positions` 기준 2주에서 3주, 평균단가 `309.76`에서 `310.93`으로 갱신됐다.
- Recent reconciliation scope: scheduler-owned `0011` stale cleanup/core/research preflight와 runtime `get_clock/get_account_info/get_orders(status=all, after=2026-06-05T04:00:00Z)/get_stock_latest_quote(AAPL,COP,NVDA,AMZN,NKE,SLB,QQQ,SPY,INTC,TSLA)/place_stock_order/get_order_by_client_id/get_account_activities(FILL)/get_orders(status=open)/get_all_positions/get_account_info` 확인 기준 `AAPL` 1주 regular-session validation add가 `2026-06-05T15:19:25.344149286Z`에 `313.27 USD`로 즉시 체결됐다. `get_open_position(AAPL)`는 runtime safety monitor가 취소했지만 `get_all_positions`와 post-submit `get_account_info`는 성공해 최종 snapshot을 runtime MCP 기준으로 기록했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 1 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-06-0011-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-12-0311-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned core preflight reconciliation 기준 `33` positions 유지, open orders `0`건이다. `AVGO`는 `5주`, `qty_available=5`, `RGTI`는 `49주`, `qty_available=49`, `SO`는 `5주`, `qty_available=5`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `0311` stale cleanup/core/research preflight를 source-of-record로 사용했고 scheduler-owned Alpaca core `get_clock/get_account_info/get_orders_open/get_all_positions/get_account_activities/get_stock_latest_quote/get_stock_snapshot` rows로 same-day fill discipline과 submit-boundary quote/spread를 재확인했다. same-day regular-session `AVGO` trim 1건과 after-hours `RGTI` trim fills 2건은 그대로 유지됐고, `AVGO`는 spread `1.8672%`가 policy cap을 크게 넘겨 trim hard gate fail, `RGTI`는 duplicate sell discipline, `SO`는 spread 회복 후에도 trim metric gap, 신규 buy path는 `review_backlog_pending_1d_count=14`와 benchmark floor cap에 막혀 이번 `0311` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-0311-hourly-autopilot-post-trade.json`

- Run: [[2026-06-05-2351-hourly-autopilot]]
- Open/new: `PLTR` buy 1 @ `138.56` (`client_order_id=hourly-20260605-2351-buy-pltr`, `status=new`)
- Filled: 없음
- Cancelled: 첫 submit 시도 1건은 runtime safety cancellation으로 반환됐지만 reconcile 후 동일 idempotent client id 재시도에서 open order가 생성됐다.
- Position count observed by Alpaca MCP: 33 positions 유지. `PLTR`는 runtime `get_all_positions` 기준 아직 2주이며 신규 주문은 미체결 상태다.
- Recent reconciliation scope: scheduler-owned `2351` stale cleanup/core/research preflight와 runtime `get_clock/get_orders(status=open)/get_orders(status=all, after=2026-06-05T04:00:00Z)/get_asset(PLTR)/get_stock_latest_quote(PLTR)/place_stock_order/get_order_by_client_id/get_all_positions/get_account_activities(FILL)` 확인 기준 첫 submit cancellation 후 `hourly-20260605-2351-buy-pltr`를 동일 id로 1회만 재시도했고, Alpaca order id `a89c2fdb-979b-42e1-a5ff-050916aa6257`가 `2026-06-05T15:00:44.444163302Z`에 `status=new`로 생성됐다. direct post-submit `get_orders(status=all, symbols=PLTR, after=2026-06-05T04:00:00Z)`와 `get_account_info` refresh는 runtime safety monitor가 취소돼 계좌 수치는 pre-submit runtime snapshot을 유지했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 1 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-05-2351-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-12-0311-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned core preflight reconciliation 기준 `33` positions 유지, open orders `0`건이다. `AVGO`는 `5주`, `qty_available=5`, `RGTI`는 `49주`, `qty_available=49`, `SO`는 `5주`, `qty_available=5`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `0311` stale cleanup/core/research preflight를 source-of-record로 사용했고 scheduler-owned Alpaca core `get_clock/get_account_info/get_orders_open/get_all_positions/get_account_activities/get_stock_latest_quote/get_stock_snapshot` rows로 same-day fill discipline과 submit-boundary quote/spread를 재확인했다. same-day regular-session `AVGO` trim 1건과 after-hours `RGTI` trim fills 2건은 그대로 유지됐고, `AVGO`는 spread `1.8672%`가 policy cap을 크게 넘겨 trim hard gate fail, `RGTI`는 duplicate sell discipline, `SO`는 spread 회복 후에도 trim metric gap, 신규 buy path는 `review_backlog_pending_1d_count=14`와 benchmark floor cap에 막혀 이번 `0311` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-0311-hourly-autopilot-post-trade.json`

- Run: [[2026-06-05-2331-hourly-autopilot]]
- Open/new: 없음
- Filled: `FCX` buy 1 @ `65.15` (`client_order_id=hourly-20260605-2331-buy-fcx`)
- Cancelled: 없음
- Position count observed by Alpaca MCP: 33 positions 유지. `FCX`는 scheduler core preflight 기준 2주에서 confirmed fill 반영 후 3주로 증가했다.
- Recent reconciliation scope: scheduler-owned `2331` stale cleanup/core/research preflight와 runtime `get_clock/get_orders(status=open)/get_orders(status=all, after=2026-06-05T04:00:00Z)/get_asset(FCX)/place_stock_order/get_order_by_client_id` 확인 기준 `FCX` 1주 regular-session validation buy가 `2026-06-05T14:39:22.134743752Z`에 `65.15 USD`로 체결됐다. direct post-fill `get_orders(status=open)`, `get_all_positions`, `get_account_info` refresh는 runtime safety monitor가 취소해 account/position snapshot은 fresh 2331 core preflight에 confirmed fill을 결합해 기록했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 1 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-05-2331-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-12-0311-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned core preflight reconciliation 기준 `33` positions 유지, open orders `0`건이다. `AVGO`는 `5주`, `qty_available=5`, `RGTI`는 `49주`, `qty_available=49`, `SO`는 `5주`, `qty_available=5`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `0311` stale cleanup/core/research preflight를 source-of-record로 사용했고 scheduler-owned Alpaca core `get_clock/get_account_info/get_orders_open/get_all_positions/get_account_activities/get_stock_latest_quote/get_stock_snapshot` rows로 same-day fill discipline과 submit-boundary quote/spread를 재확인했다. same-day regular-session `AVGO` trim 1건과 after-hours `RGTI` trim fills 2건은 그대로 유지됐고, `AVGO`는 spread `1.8672%`가 policy cap을 크게 넘겨 trim hard gate fail, `RGTI`는 duplicate sell discipline, `SO`는 spread 회복 후에도 trim metric gap, 신규 buy path는 `review_backlog_pending_1d_count=14`와 benchmark floor cap에 막혀 이번 `0311` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-0311-hourly-autopilot-post-trade.json`

- Run: [[2026-06-05-2311-hourly-autopilot]]
- Open/new: 없음
- Filled: `WMT` buy 1 @ `119.78` (`client_order_id=hourly-20260605-2311-buy-wmt`)
- Cancelled: 첫 submit 시도 1건은 runtime safety cancellation으로 반환됐지만 동일 idempotent client id reconcile 후 재시도에서 체결
- Position count observed by Alpaca MCP: 33 positions 유지. `WMT`는 scheduler core preflight 기준 5주에서 confirmed fill 반영 후 6주로 증가했다.
- Recent reconciliation scope: scheduler-owned `2311` stale cleanup/core/research preflight와 runtime `get_clock/get_orders(status=all, after=2026-06-05T04:00:00Z)/get_asset(WMT)/place_stock_order/get_order_by_client_id/get_orders(status=open)` 확인 기준 `WMT` 1주 regular-session validation buy가 첫 cancellation 후 동일 `client_order_id=hourly-20260605-2311-buy-wmt`로 1회만 재시도돼 `2026-06-05T14:17:18.858272769Z`에 `119.78 USD`로 체결됐다. direct post-fill `get_orders(status=all, symbols=WMT, after=2026-06-05T04:00:00Z)`와 `get_open_position(WMT)` refresh는 runtime safety monitor가 취소해 account/position snapshot은 fresh 2311 core preflight에 confirmed fill을 결합해 기록했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 1 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-05-2311-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-12-0311-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned core preflight reconciliation 기준 `33` positions 유지, open orders `0`건이다. `AVGO`는 `5주`, `qty_available=5`, `RGTI`는 `49주`, `qty_available=49`, `SO`는 `5주`, `qty_available=5`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `0311` stale cleanup/core/research preflight를 source-of-record로 사용했고 scheduler-owned Alpaca core `get_clock/get_account_info/get_orders_open/get_all_positions/get_account_activities/get_stock_latest_quote/get_stock_snapshot` rows로 same-day fill discipline과 submit-boundary quote/spread를 재확인했다. same-day regular-session `AVGO` trim 1건과 after-hours `RGTI` trim fills 2건은 그대로 유지됐고, `AVGO`는 spread `1.8672%`가 policy cap을 크게 넘겨 trim hard gate fail, `RGTI`는 duplicate sell discipline, `SO`는 spread 회복 후에도 trim metric gap, 신규 buy path는 `review_backlog_pending_1d_count=14`와 benchmark floor cap에 막혀 이번 `0311` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-0311-hourly-autopilot-post-trade.json`

- Run: [[2026-06-05-2251-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: 33 positions 유지. `SLB`는 여전히 3주이며 `hourly-20260605-2251-buy-slb`에 해당하는 신규 주문은 생성되지 않았다.
- Recent reconciliation scope: scheduler-owned `2251` stale cleanup/core/research preflight와 runtime `get_orders(status=all, after=2026-06-05T04:00:00Z)/get_asset(SLB)/get_stock_latest_quote(SLB)/get_order_by_client_id/get_all_positions/get_account_info` 확인 기준 `SLB` 1주 regular-session validation buy 계획은 hard gate와 validator를 모두 통과했지만 `place_stock_order`가 runtime safety cancellation으로 두 차례 모두 submit되지 않았다. `get_order_by_client_id(hourly-20260605-2251-buy-slb)`는 404, `get_orders(status=all, symbols=SLB, after=2026-06-05T04:00:00Z)`는 0건이어서 실제 Alpaca 주문 미생성을 확인했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-05-2251-hourly-autopilot-post-trade.json`

## 최신 hourly-autopilot reconciliation

- Run: [[2026-06-12-0311-hourly-autopilot]]
- Open/new: 없음
- Filled: 없음
- Cancelled: 없음
- Position count observed by Alpaca MCP: scheduler-owned core preflight reconciliation 기준 `33` positions 유지, open orders `0`건이다. `AVGO`는 `5주`, `qty_available=5`, `RGTI`는 `49주`, `qty_available=49`, `SO`는 `5주`, `qty_available=5`로 unchanged였다.
- Recent reconciliation scope: scheduler-owned `0311` stale cleanup/core/research preflight를 source-of-record로 사용했고 scheduler-owned Alpaca core `get_clock/get_account_info/get_orders_open/get_all_positions/get_account_activities/get_stock_latest_quote/get_stock_snapshot` rows로 same-day fill discipline과 submit-boundary quote/spread를 재확인했다. same-day regular-session `AVGO` trim 1건과 after-hours `RGTI` trim fills 2건은 그대로 유지됐고, `AVGO`는 spread `1.8672%`가 policy cap을 크게 넘겨 trim hard gate fail, `RGTI`는 duplicate sell discipline, `SO`는 spread 회복 후에도 trim metric gap, 신규 buy path는 `review_backlog_pending_1d_count=14`와 benchmark floor cap에 막혀 이번 `0311` cycle도 no-submit으로 종료했다.
- Orders submitted/replaced/cancelled/closed by this workflow: 0 / 0 / 0 / 0.
- Source note: `wiki/trade-ledger/positions/2026-06-12-0311-hourly-autopilot-post-trade.json`

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
