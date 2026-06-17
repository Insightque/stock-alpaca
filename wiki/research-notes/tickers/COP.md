---
symbol: COP
asset_type: stock
---

# COP

## 2026-06-16 02:39 KST hourly-autopilot

`COP` 1주 regular-session day limit buy가 `112.81 USD` limit으로 제출됐고, direct Alpaca MCP reconciliation 기준 `client_order_id=hourly-20260616-0231-buy-cop`, `order_id=a3bc930e-4eef-4f8a-a3bb-6b1333b36e69`가 `2026-06-15T17:39:15.996053768Z`에 `112.62 USD`로 즉시 체결됐다. 근거는 scheduler-owned `0231` stale cleanup/core/research preflight 재사용, direct Alpaca submit-boundary check 기준 regular market open, open orders `0`, same-day `COP` duplicate `0`, quote `112.78/112.81`, spread `0.0266%`, active tradable NYSE stock, 그리고 `[[COP]]` 및 `2026-06-15` portfolio review에서 `2026-06-10 ET` fill 1D가 `+1.28%`, `SPY 대비 +1.04%p`로 양호했다고 확인된 점이다. sell-first 평가에서는 `AVGO/RGTI` same-day sell duplicate와 `SO` trim metric gap이 유지돼 executable risk-reducing sell이 남지 않았고, buy fallback에서는 `XOM/SLB/FCX/JPM/NEE/BAC/WMT/NKE` same-day duplicate, `SPY/QQQ` per-order cap, `NVDA` cluster warning, `AAPL` weak-review history가 차례로 막혀 `COP`가 가장 실행 가능한 existing energy/value diversifier floor-size add로 승격됐다. 이 fill 후 `get_all_positions` 기준 `COP qty=5 -> 6`, `avg_entry_price=116.876667`로 갱신됐다.

출처: [[2026-06-16-0231-hourly-autopilot]], `wiki/trade-ledger/positions/2026-06-16-0231-hourly-autopilot-post-trade.json`

## 2026-06-18 02:00 KST hourly-autopilot

`COP` 1주 regular-session day limit buy가 `110.93 USD` limit으로 제출됐고, same `client_order_id=hourly-20260618-0151-buy-cop` reconciliation 기준 `2026-06-17T16:59:32.674078658Z`에 `110.83 USD`로 즉시 체결됐다. 근거는 scheduler-owned `0151` stale cleanup/core/research preflight 기준 hard gate pass, live continuity 기준 직전 `GOOGL` fill 이후 open orders `0` 재확인, `SO/RGTI/PFE` sell-first 경로가 각각 metric gap과 same-day duplicate sell gate로 막혔다는 점, 그리고 `COP`가 same-day duplicate/open-order conflict가 없는 existing energy/value diversifier로 live quote `110.83/110.93` spread `0.0902%`, active tradable NYSE stock, `2026-06-17` portfolio review의 `중립 약함` history, `SEC/FRED/Yahoo` 3-provider positive confirmation을 유지해 current invested ratio가 acceleration threshold 아래인 상태에서 floor-size learning fallback으로 가장 executable했다는 점이다. immediate reconciliation 기준 보유 수량은 `6주 -> 7주`, `avg_entry_price=116.012857`로 갱신됐다.

출처: [[2026-06-18-0151-hourly-autopilot]], `wiki/trade-ledger/orders/2026-06-18-0151-hourly-autopilot.json`, `wiki/trade-ledger/positions/2026-06-18-0151-hourly-autopilot-post-trade.json`

## 2026-06-11 00:58 KST hourly-autopilot

`COP` 1주 regular-session day limit buy가 `121.20 USD` limit으로 제출됐고, direct Alpaca MCP reconciliation 기준 `client_order_id=hourly-20260611-0051-buy-cop`, `order_id=998a7e94-7e3c-4737-bdd6-2bdc37dccfea`가 `2026-06-10T15:58:00.532764086Z`에 `121.05 USD`로 즉시 체결됐다. 근거는 scheduler-owned `0051` stale cleanup/core/research preflight 재사용, regular market open과 open orders `0`건 재확인, `AVGO/RGTI` same-day sell duplicate 및 `SO` trim metric gap 이후에도 learning_trade_directive가 최소 1건 validation order를 요구한다는 점, 그리고 `COP`가 2026-06-09 analyst review 기준 `2026-06-05 ET` fill 1D `+1.28%`, `SPY` 대비 `+1.04%p`, live IEX quote `121.15/121.20` spread `0.0413%`, same-day duplicate/open-order conflict 부재를 보여 existing energy/value sleeve add로 가장 executable했다는 점이다. 체결 후 보유수량은 `4주 -> 5주`, 평균단가는 `117.728 USD`로 갱신됐다.

출처: [[2026-06-11-0051-hourly-autopilot]], `wiki/trade-ledger/positions/2026-06-11-0051-hourly-autopilot-post-trade.json`

## 2026-06-10 03:01 KST hourly-autopilot

`COP` 1주 regular-session day limit buy가 `116.14 USD` limit으로 제출됐고, Alpaca MCP 기준 `client_order_id=hourly-20260610-0251-buy-cop`, `order_id=34da84fa-1653-4852-a955-6a1e0efd3fa8`가 생성된 뒤 same client id reconciliation에서 `2026-06-09T18:00:39.436794108Z`에 `116.05 USD`로 즉시 체결됐다. 근거는 scheduler-owned `0251` stale cleanup/core/research preflight와 strict universe/MCP/risk gate 통과, `AVGO/RGTI` sell duplicate 및 `SO` trim metric gap 이후에도 learning_trade_directive가 최소 1건 validation order를 요구한다는 점, 그리고 `COP`가 2026-06-09 analyst review 기준 `2026-06-05 ET` fill 1D `+1.28%`, `SPY` 대비 `+1.04%p`, live IEX quote `116.09/116.14` spread `0.0431%`, same-day duplicate/open-order conflict 부재를 보여 energy/value diversifier fallback으로 가장 executable했다는 점이다.

출처: [[2026-06-10-0251-hourly-autopilot]], `wiki/trade-ledger/positions/2026-06-10-0251-hourly-autopilot-post-trade.json`

## 2026-06-06 01:37 KST hourly-autopilot

`COP` 1주 regular-session day limit buy가 `117.51 USD` limit으로 제출됐다. direct `get_order_by_client_id` 경로는 tool safety monitor가 막혔지만, post-submit Alpaca MCP `get_all_positions` 기준 `COP` 보유수량이 `2주 -> 3주`, 평균단가가 `117.06 -> 117.18`로 갱신돼 이번 1주 validation add가 약 `117.42 USD`에 체결된 것으로 추정 기록했다. 근거는 scheduler-owned stale cleanup/core/research preflight, strict universe/MCP/risk gate 통과, runtime IEX quote `117.49/117.51` 기준 spread `0.0170%`, 그리고 2026-06-05 portfolio review의 5D follow-through 양호다.

## 회고 기록

### 2026-05-30 analyst review cycle

2026-05-28 validation buy 1주는 114.95 USD 진입 대비 2026-05-29 close/current 114.36 USD로 -0.51%, SPY 대비 -0.71%p였다. 손실은 작지만 energy/value hedge 후보로서 1D 우위는 확인되지 않았다. 판단은 `중립 약함`이며 5D/20D 대기.

출처: [[2026-05-30-portfolio-review]], [[2026-05-30-0625-analyst-review-cycle-sources]]

### 2026-06-09 analyst review cycle

`2026-06-05 ET` fill 1D는 `117.42 USD -> 118.92 USD`로 `+1.28%`였다. `SPY` 대비 `+1.04%p`, `QQQ` 대비 `-0.24%p`라 broad risk-on을 거의 따라가면서 energy/value hedge 역할도 유지했다. 판단은 `양호`이며 5D에서도 energy sleeve가 계속 버티는지 확인한다.

출처: [[2026-06-09-portfolio-review]], [[2026-06-09-0623-analyst-review-cycle-sources]]

### 2026-06-11 analyst review cycle

`2026-06-09 ET` buy 1주는 `116.05 USD` 진입 대비 `2026-06-10 ET` close `119.91 USD`로 `+3.33%`였다. `SPY` 대비 `+4.89%p`, `QQQ` 대비 `+5.33%p`로 이번 1D cohort에서 가장 강한 follow-through 중 하나였다. energy/value sleeve의 selection value는 강화됐지만, `2026-06-10 ET` 추가 fill `121.05 USD`는 별도 1D horizon으로 다시 본다.

출처: [[2026-06-11-portfolio-review]], [[2026-06-11-0622-analyst-review-cycle-sources]]

### 2026-06-12 analyst review cycle

`2026-06-10 ET` add 1주는 `121.05 USD` 대비 `2026-06-11 ET` close/current `115.7518 USD`로 `-4.38%`였고, `2026-06-05 ET` fill 5D도 `117.42 USD -> 115.7518 USD`로 `-1.42%`였다. 전일 강한 1D follow-through가 바로 되돌려졌기 때문에 energy/value sleeve add cadence는 다시 보수적으로 본다.

출처: [[2026-06-12-portfolio-review]], [[2026-06-12-0632-analyst-review-cycle-sources]]

### 2026-06-18 analyst review cycle

`2026-06-10 ET` add 1주는 `121.05 USD -> 111.19 USD`로 `-8.15%`였다. `SPY/QQQ` 대비 열위도 커서 energy/value sleeve add cadence는 이번 5D closeout에서 명확한 `약세` 사례로 남긴다.

출처: [[2026-06-18-portfolio-review]], [[2026-06-18-0621-analyst-review-cycle-sources]]
