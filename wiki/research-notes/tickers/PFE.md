---
symbol: PFE
asset_type: stock
---

# PFE

## 2026-06-18 12:15 KST after-hours-autopilot reconciliation

`2026-06-18 12:11 KST` after-hours cycle은 scheduler-owned `1211` core/research preflight를 source-of-record로 유지했고 Alpaca core `first_blocking_gate=market_closed`는 장외 워크플로우에서 expected nonblocking으로 처리했다. live Alpaca continuity `get_order_by_client_id(ah-20260618-1111-sell-pfe-01)` 기준 earlier trim 1주는 `2026-06-18T02:58:29.784751618Z`에 `filled_avg_price=25.97 USD`로 체결 완료됐다. same-session after-hours submitted orders는 이미 `2/2`였고 `RGTI` stale open-order lifecycle이 risk FAIL로 남아 이번 cycle 신규 submit은 없었다. `get_all_positions` 기준 `PFE` 보유수량은 `2주 -> 1주`, `qty_available=1`로 감소했고 해석은 `repeated weak-review trim fill confirmed, residual 1-share hold`다.

출처: [[2026-06-18-1211-after-hours-autopilot]], `wiki/trade-ledger/positions/2026-06-18-1211-after-hours-autopilot-post-trade.json`

## 2026-06-18 23:01 KST hourly-autopilot

`2026-06-18 22:51 KST` regular-session cycle은 scheduler-owned `2251` stale/core/research preflight를 source-of-record로 사용했고 `Yahoo Finance` pass 복구로 strict MCP submit gate가 다시 열렸다. buy side는 `review_backlog_pending_1d_count=17`로 계속 차단됐고, sell-first 재평가에서는 `PFE` 잔여 1주가 repeated weak-review precedent, fresh quote `25.24/25.25`, spread `0.0396%`, same US-date duplicate sell `0`, open orders `0` 조건을 모두 충족해 `entry_style=exit` regular-session validation close-out으로 승격됐다. `client_order_id=hourly-20260618-2251-sell-pfe`, `limit=25.24 USD`로 제출된 주문은 same client id reconciliation 기준 `2026-06-18T14:01:07.126808291Z`에 `filled_avg_price=25.28 USD`로 즉시 체결됐고, live `get_all_positions`에서는 `PFE`가 사라져 보유수량이 `1주 -> 0주`로 닫혔다. 해석은 `repeated weak-review residual hold fully closed after strict submit gate recovery`다.

출처: [[2026-06-18-2251-hourly-autopilot]], `wiki/trade-ledger/positions/2026-06-18-2251-hourly-autopilot-post-trade.json`

## 2026-06-18 11:19 KST after-hours-autopilot

`2026-06-18 11:11 KST` after-hours cycle은 scheduler-owned `1111` core/research preflight를 source-of-record로 유지했고 Alpaca core `first_blocking_gate=market_closed`는 장외 워크플로우에서 expected nonblocking으로 처리했다. 이번 cycle에서는 direct Alpaca overnight continuity가 `PFE` quote를 `25.97/25.98`, spread `0.0385%`로 회복했고 strict universe/MCP/risk gate가 모두 통과해 repeated weak-review defensive holding trim 경로를 다시 열었다. 이에 `client_order_id=ah-20260618-1111-sell-pfe-01`, `limit=25.97 USD`, `extended_hours=true` 조건으로 1주 trim sell을 제출했다. immediate same client id reconciliation 기준 주문은 `order_id=d3b37f0b-4efa-406a-994f-432ae6b8b8a0`, `status=new`, `filled_qty=0` open order이며 direct `get_all_positions` 기준 보유수량은 아직 `2주`, `qty_available=1`이다. 해석은 `repeated weak-review trim submit 완료, next cycle fill/open-order lifecycle 추적 필요`다.

출처: [[2026-06-18-1111-after-hours-autopilot]], `wiki/trade-ledger/positions/2026-06-18-1111-after-hours-autopilot-post-trade.json`

## 2026-06-17 14:14 KST after-hours-autopilot

`2026-06-17 14:00 KST` cycle에서 제출된 `PFE` 1주 after-hours day limit trim sell(`client_order_id=ah-20260617-1351-sell-pfe-01`, `limit=26.01 USD`, `extended_hours=true`)은 다음 `1411` after-hours-autopilot reconciliation 기준 `2026-06-17T05:11:09.778969Z`에 `filled_avg_price=26.03 USD`로 체결된 것이 확인됐다. `1411` scheduler-owned Alpaca core preflight는 expected `market_closed`만 남기고 passing row가 없었으므로 direct Alpaca MCP continuity로 same client id readback, same-session fill ledger, positions/open-orders/account 상태를 보강했다. 체결 확인 후 `get_all_positions` 기준 보유수량은 `3주 -> 2주`, `qty_available=2`로 감소했고 direct `get_account_info` 기준 cash는 `30,391.80 USD`, portfolio value는 `101,225.69 USD`, buying power는 `303,952.34 USD`였다. 해석은 `repeated weak-review trim fill confirmed`; 같은 after-hours 세션의 earlier `RGTI` trim fill과 합쳐 separate session budget이 `2/2`로 닫혀 `1411` cycle에서는 신규 주문이 열리지 않았다.

출처: [[2026-06-17-1411-after-hours-autopilot]], `wiki/trade-ledger/positions/2026-06-17-1411-after-hours-autopilot-post-trade.json`

## 2026-06-16 23:19 KST hourly-autopilot

`PFE` 1주 regular-session day limit trim sell이 `25.90 USD` limit, `client_order_id=hourly-20260616-2311-sell-pfe`로 제출됐고 direct Alpaca MCP reconciliation 기준 `2026-06-16T14:18:55.368487606Z`에 `filled_avg_price=25.94 USD`로 즉시 체결됐다. 근거는 scheduler-owned `2311` stale cleanup/core/research preflight와 direct Alpaca submit-boundary check 기준 paper mode, regular market open, existing open order는 `RGTI` trim 1건뿐이며 `PFE` same-day sell duplicate는 `0`, direct quote `25.90/25.91` spread `0.0386%`, active tradable NYSE stock, strict universe/MCP/risk gate 통과, 그리고 `2026-06-04` 5D review와 `2026-06-09` 1D review에 누적된 defensive-diversification 약세 해석이 유지됐다는 점이다. `RGTI`는 fresh same-symbol open sell 때문에 재제출 대상이 아니었고 `SO`는 live spread fail로 탈락했다. post-trade `get_all_positions` 기준 보유수량은 `4주 -> 3주`, `avg_entry_price=25.925`, `qty_available=3`으로 감소했고 `get_account_info` 기준 cash는 `30,224.10 USD -> 30,250.04 USD`로 증가했다.

출처: [[2026-06-16-2311-hourly-autopilot]], `wiki/trade-ledger/positions/2026-06-16-2311-hourly-autopilot-post-trade.json`

## 2026-06-16 04:59 KST hourly-autopilot

`PFE` 1주 regular-session day limit trim sell이 `26.01 USD` limit, `client_order_id=hourly-20260616-0451-sell-pfe`로 제출됐고 direct Alpaca MCP `get_order_by_client_id` 기준 `2026-06-15T19:59:48.06371096Z`에 `filled_avg_price=26.01 USD`로 즉시 체결됐다. 근거는 scheduler-owned `0451` stale cleanup/core/research preflight와 direct Alpaca submit-boundary check 기준 paper mode, regular market open, open orders `0`, same-day `PFE sell` duplicate `0`, direct quote `26.01/26.02` spread `0.0384%`, active tradable NYSE stock, strict universe/MCP/risk gate 통과, 그리고 `2026-06-04` 5D review와 `2026-06-09` 1D review에 누적된 defensive-diversification 약세 해석 및 `2026-06-12` after-hours trim precedent가 유지됐다는 점이다. post-trade `get_all_positions` 기준 보유수량은 `5주 -> 4주`, `avg_entry_price=25.972`, `qty_available=4`로 감소했고 `get_account_info` 기준 cash는 `29,810.35 USD -> 29,836.36 USD`로 증가했다.

출처: [[2026-06-16-0451-hourly-autopilot]], `wiki/trade-ledger/positions/2026-06-16-0451-hourly-autopilot-post-trade.json`

## 2026-06-12 10:21 KST after-hours-autopilot

`PFE` 1주 after-hours day limit trim sell이 `26.12 USD` limit, `extended_hours=true`, `client_order_id=ah-20260612-1011-sell-pfe-01`로 제출됐고 same client id reconciliation 기준 `filled_avg_price=26.13 USD`로 즉시 체결됐다. buy fallback은 `review_backlog_pending_1d_count=14`에 따른 risk backlog throttle로 차단됐지만, `2026-06-09`, `2026-06-05`, `2026-06-04` portfolio review에 반복 약세로 남아 있던 defensive-diversification validation holding이라는 점, runtime overnight quote `26.12/26.16` spread `0.1529%`, open-order duplicate 없음이 확인돼 sell-first floor-size trim으로 승격됐다. post-trade `get_all_positions` 기준 보유수량은 `6주 -> 5주`, `avg_entry_price=26.033333`, `qty_available=5`로 감소했고 review bucket은 `after_hours_validation`을 유지한다.

출처: [[2026-06-12-1011-after-hours-autopilot]], `wiki/trade-ledger/positions/2026-06-12-1011-after-hours-autopilot-post-trade.json`

## 2026-06-10 23:54 KST hourly-autopilot

`PFE` 1주 regular-session day limit buy가 `25.72 USD` limit으로 제출됐고 immediate reconciliation 기준 `filled_avg_price=25.70 USD`로 즉시 체결됐다. scheduler-owned `2351` stale cleanup/core/research preflight와 strict universe/MCP/risk gate가 모두 통과했고, sell-first에서는 `RGTI`와 `AVGO`가 same-day sell duplicate, `SO`가 trim metric gap으로 blocked였다. buy fallback에서는 `BAC/WMT` same-day duplicate, `SPY/QQQ` per-order cap 초과가 남아 `PFE`가 healthcare diversifier floor-size learning order로 승격됐다. post-trade `get_all_positions` 기준 보유수량은 `5주 -> 6주`, `avg_entry_price=26.033333`, `qty_available=6`으로 증가했고 review status는 `회고 대기(1D/5D/20D)`다.

출처: [[2026-06-10-2351-hourly-autopilot]], `wiki/trade-ledger/positions/2026-06-10-2351-hourly-autopilot-post-trade.json`

## 2026-06-06 02:20 KST hourly-autopilot

`PFE` 1주 regular-session day limit buy가 `26.09 USD` limit으로 제출됐다. scheduler-owned `0211` stale cleanup/core/research preflight와 strict universe/MCP/risk gate가 모두 통과했고, same-day duplicate/open-order conflict가 없으며 Yahoo Finance preflight에서 Chai AI drug discovery license headline과 usable recommendation breadth가 확인됐다. immediate reconciliation 기준 Alpaca order id `c646425a-7a9d-42c2-b611-7776cce9446d`, `client_order_id=hourly-20260606-0211-buy-pfe`는 `status=new`, `filled_qty=0` open order다. `get_all_positions` 기준 보유수량은 아직 3주이고, post-submit `get_account_info`는 성공했지만 체결은 아직 확인되지 않았다.

출처: [[2026-06-06-0211-hourly-autopilot]], `wiki/trade-ledger/positions/2026-06-06-0211-hourly-autopilot-post-trade.json`

## 회고 기록

### 2026-05-29 analyst review cycle

2026-05-27 validation buy 1주는 2026-05-28 close 기준 -0.72%로 SPY/QQQ를 하회했다. 손실은 작지만 defensive healthcare thesis가 1D에는 확인되지 않아 5D/20D 회고 대기로 둔다.

출처: [[2026-05-29-portfolio-review]], [[2026-05-29-0625-analyst-review-cycle-sources]]

### 2026-05-30 analyst review cycle

2026-05-28 validation buy 1주는 26.16 USD 진입 대비 2026-05-29 close/current 26.16 USD로 보합, SPY 대비 -0.20%p였다. Defensive healthcare 표본으로 계좌 위험은 작았지만 1D 초과수익 근거는 없다.

출처: [[2026-05-30-portfolio-review]], [[2026-05-30-0625-analyst-review-cycle-sources]]

### 2026-05-31 analyst review cycle

2026-05-29 validation add 1주는 26.09 USD 체결 후 주말 현재 26.18 USD reference로 +0.34%지만, 다음 미국 정규장 close 전이라 1D 판단은 보류한다. Defensive healthcare thesis는 2026-06-01 close 이후 재점검한다.

출처: [[2026-05-31-portfolio-review]], [[2026-05-31-0624-analyst-review-cycle-sources]]
### 2026-06-02 analyst review cycle

2026-05-29 validation add 1주는 26.09 USD 진입 대비 2026-06-01 close 25.64 USD로 -1.72%였다. 방어적 healthcare 분산 thesis는 1D에서 작동하지 않았고 SPY/QQQ 대비 약했다. 판단은 `약함`, 5D/20D 대기.

출처: [[2026-06-02-portfolio-review]], [[2026-06-02-0624-analyst-review-cycle-sources]]
### 2026-06-04 analyst review cycle

2026-05-29 validation add 1주는 26.09 USD 진입 대비 2026-06-03 close 25.36 USD로 -2.80%였다. defensive healthcare 분산 thesis는 5D에서도 SPY/QQQ를 모두 하회했다. 판단은 `약함`, 20D review 전 add 또는 정책 승격 근거로 쓰지 않는다.

출처: [[2026-06-04-portfolio-review]], [[2026-06-04-0624-analyst-review-cycle-sources]]

### 2026-06-09 analyst review cycle

`2026-06-05 ET` fill 1D는 `26.09 USD -> 25.61 USD`로 `-1.84%`였다. 절대 손실과 `SPY/QQQ` 대비 부진이 동시에 남아 defensive healthcare 분산 thesis의 개선 증거가 되지 못했다. 판단은 `약함`이며 5D close 전까지 추가 승격 근거로 쓰지 않는다.

출처: [[2026-06-09-portfolio-review]], [[2026-06-09-0623-analyst-review-cycle-sources]]

### 2026-06-11 analyst review cycle

`2026-06-09 ET` buy 1주는 `25.82 USD` 진입 대비 `2026-06-10 ET` close `25.61 USD`로 `-0.81%`였다. 절대수익은 음수지만 `SPY` 대비 `+0.75%p`, `QQQ` 대비 `+1.19%p`라 broad selloff 대비 방어는 있었다. 다만 prior weak review가 누적돼 defensive healthcare add의 edge가 확인됐다고 보긴 어렵고, `2026-06-10 ET` 추가 fill `25.70 USD`도 별도 1D 대기로 둔다.

출처: [[2026-06-11-portfolio-review]], [[2026-06-11-0622-analyst-review-cycle-sources]]

### 2026-06-13 analyst review cycle

`2026-06-11 ET` after-hours trim 1주는 `26.13 USD` 체결 대비 `2026-06-12 ET` close/current `26.21 USD`로 `+0.31%`였다. sell 뒤 소폭 반등이 나와 exact timing edge는 제한적이지만, upside 규모가 작고 기존 반복 약세 review를 감안하면 trim 해석을 뒤집을 정도는 아니다. 다음 lifecycle closeout은 `2026-06-19` 미국 정규장 close의 5D horizon이다.

출처: [[2026-06-13-portfolio-review]], [[2026-06-13-0622-analyst-review-cycle-sources]]


## 2026-06-17 14:00 KST after-hours-autopilot

`PFE` 1주 after-hours day limit trim sell이 `26.01 USD` limit, `extended_hours=true`, `client_order_id=ah-20260617-1351-sell-pfe-01`로 제출됐다. 이번 cycle은 scheduler-owned `1351` core/research preflight를 source-of-record로 유지했고, direct Alpaca overnight continuity 기준 `26.01/26.07` quote, spread `0.2307%`, same-session `PFE` sell duplicate `0`, open orders `0`, repeated weak-review defensive holding trim rationale가 확인돼 sell-first floor-size trim으로 승격됐다. immediate same client id reconciliation 기준 주문은 `order_id=c96904a2-deab-415b-9b27-a20660a043e4`, `status=new`, `filled_qty=0` open order이며 `get_all_positions` 기준 보유수량은 아직 `3주`, `qty_available=2`로 1주만 예약 상태다. 해석은 `repeated weak-review trim submit 완료, next cycle fill/open-order lifecycle 추적 필요`다.

출처: [[2026-06-17-1351-after-hours-autopilot]], `wiki/trade-ledger/positions/2026-06-17-1351-after-hours-autopilot-post-trade.json`

### 2026-06-18 analyst review cycle

`2026-06-10 ET` trim 1주는 `25.94 USD -> 25.93 USD`로 sell 이후 사실상 보합이었다. trim timing edge는 거의 없지만 repeated weak-review defensive holding을 줄인 해석을 뒤집을 정도도 아니라 이번 5D closeout은 `중립`으로 둔다.

출처: [[2026-06-18-portfolio-review]], [[2026-06-18-0621-analyst-review-cycle-sources]]
