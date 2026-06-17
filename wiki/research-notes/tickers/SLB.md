---
symbol: SLB
asset_type: stock
---

# SLB

## 2026-06-18 02:39 KST hourly-autopilot

`SLB` 1주 regular-session day limit buy가 `51.33 USD` limit으로 제출됐고, same `client_order_id=hourly-20260618-0231-buy-slb` reconciliation 기준 `2026-06-17T17:39:03.382610403Z`에 `filled_avg_price=51.32 USD`로 즉시 체결됐다. 근거는 scheduler-owned `0231` stale cleanup/core/research preflight 기준 hard gate pass, direct Alpaca continuity 기준 same US-date duplicate/open-order stack 재확인, `SO`가 same-day buy-for-trim gate와 trim metric gap에, `RGTI/PFE`가 same-day duplicate sell gate에 막혀 executable trim이 없었다는 점, 그리고 `SLB`가 live quote `51.32/51.33` spread `0.0195%`, active tradable NYSE stock, `SEC/FRED/Yahoo` 3-provider positive confirmation, review backlog throttle 비차단, existing energy-services diversifier 역할을 유지해 남은 floor-size learning fallback 중 가장 executable했다는 점이다. immediate reconciliation 기준 보유 수량은 `7주 -> 8주`, `avg_entry_price=55.0625`로 갱신됐다.

출처: [[2026-06-18-0231-hourly-autopilot]], `wiki/trade-ledger/positions/2026-06-18-0231-hourly-autopilot-post-trade.json`

## 2026-06-16 01:42 KST hourly-autopilot

`SLB` 1주 regular-session day limit buy가 `54.04 USD` limit으로 제출됐고, Alpaca MCP `get_order_by_client_id`와 `get_orders(status=all, symbols=SLB, after=2026-06-15T16:40:00Z)` 기준 `client_order_id=hourly-20260616-0131-buy-slb`, `order_id=a92f261b-aaee-4b4d-af16-0c1dd4c81b30`, `filled_avg_price=54.03 USD`로 즉시 체결됐다. 근거는 scheduler-owned `0131` stale cleanup/core/research preflight와 strict universe/MCP/risk gate 통과, same-day `FCX/NEE/BAC/WMT/JPM` buy duplicate 및 `AVGO/RGTI` sell duplicate 이후에도 learning_trade_directive가 최소 1건 validation order를 요구한다는 점, 그리고 `SLB`가 current research-preflight symbol이면서 2026-06-09 analyst review 기준 1D relative outcome이 양호하고 live quote `54.03/54.04` spread `0.0185%`, energy-services diversifier 역할, same-day duplicate/open-order conflict 없음으로 가장 executable했다는 점이다. 이 fill 후 `get_all_positions` 기준 `SLB qty=6 -> 7`, `avg_entry_price=55.597143`로 갱신됐다.

출처: [[2026-06-16-0131-hourly-autopilot]], `wiki/trade-ledger/positions/2026-06-16-0131-hourly-autopilot-post-trade.json`

## 2026-06-11 01:19 KST hourly-autopilot

`SLB` 1주 regular-session day limit buy가 `56.55 USD` limit으로 제출됐고, Alpaca MCP `get_order_by_client_id`와 `get_order_by_id` 기준 `client_order_id=hourly-20260611-0111-buy-slb`, `order_id=14d20183-5063-4025-9114-5e82cbcf6386`, `filled_avg_price=56.45 USD`로 즉시 체결됐다. 근거는 scheduler-owned `0111` stale cleanup/core/research preflight와 strict universe/MCP/risk gate 통과, same-day `COP/JNJ/XOM/PFE/BAC/WMT` buy duplicate 및 `AVGO/RGTI` sell duplicate 이후에도 learning_trade_directive가 최소 1건 validation order를 요구한다는 점, 그리고 `SLB`가 2026-06-09 analyst review 기준 1D `양호`, live quote `56.54/56.55` spread `0.0177%`, energy-services diversifier 역할, same-day duplicate/open-order conflict 없음으로 가장 executable했다는 점이다. 이 fill은 새 validation lifecycle 표본으로 기록하며 1D/5D/20D review를 추적한다.

출처: [[2026-06-11-0111-hourly-autopilot]], `wiki/trade-ledger/positions/2026-06-11-0111-hourly-autopilot-post-trade.json`

## 2026-06-10 02:40 KST hourly-autopilot

`SLB` 1주 regular-session day limit buy가 `55.11 USD` limit으로 제출됐고, Alpaca MCP 기준 `client_order_id=hourly-20260610-0231-buy-slb`, `order_id=d225a67d-6bc2-4488-99f3-d45a48bf6f4e`가 생성됐다. immediate reconciliation 시점에는 same client id 기준 `status=new`, `filled_qty=0` open order이며 신규 fill은 아직 없다. 근거는 scheduler-owned `0231` stale cleanup/core/research preflight와 strict universe/MCP/risk gate 통과, `AVGO/RGTI` sell duplicate 및 `SO` trim metric gap 이후에도 learning_trade_directive가 최소 1건 validation order를 요구한다는 점, 그리고 `SLB`가 2026-06-09 analyst review 기준 1D `양호`, live quote `55.10/55.11` spread `0.0181%`, energy-services diversifier 역할, same-day duplicate/open-order conflict 없음으로 가장 executable했다는 점이다.

출처: [[2026-06-10-0231-hourly-autopilot]], `wiki/trade-ledger/positions/2026-06-10-0231-hourly-autopilot-post-trade.json`

## 회고 기록

### 2026-05-30 analyst review cycle

2026-05-28 validation buy 1주는 55.48 USD 진입 대비 2026-05-29 close/current 54.55 USD로 -1.68%, SPY 대비 -1.87%p였다. 에너지 서비스 분산 후보였지만 1D에서는 약했고, XOM/CVX와 함께 macro headline 민감성이 컸다. 판단은 `약함`이며 5D/20D 대기.

출처: [[2026-05-30-portfolio-review]], [[2026-05-30-0625-analyst-review-cycle-sources]]

### 2026-05-31 analyst review cycle

2026-05-29 validation add 1주는 54.79 USD 체결 후 주말 현재 54.55 USD reference로 -0.44%지만, 다음 미국 정규장 close 전이라 1D 판단은 보류한다. Energy services diversification thesis는 2026-06-01 close 이후 재확인한다.

출처: [[2026-05-31-portfolio-review]], [[2026-05-31-0624-analyst-review-cycle-sources]]
### 2026-06-02 analyst review cycle

2026-05-29 validation add 1주는 54.79 USD 진입 대비 2026-06-01 close 54.77 USD로 -0.04%였다. 절대 손실은 작지만 SPY/QQQ 대비 약했고, mixed shelf filing headline과 energy macro 민감성이 남아 있어 `중립 약함`으로 둔다. 5D/20D 대기.

출처: [[2026-06-02-portfolio-review]], [[2026-06-02-0624-analyst-review-cycle-sources]]
### 2026-06-04 analyst review cycle

2026-05-29 validation add 1주는 54.79 USD 진입 대비 2026-06-03 close 56.86 USD로 +3.78%였다. SPY 대비 +4.06%p, QQQ 대비 +2.97%p로 5D follow-through는 양호하다. 다만 oil/energy headline 의존도가 높아 단일 사례만으로 active rule 승격 근거로 쓰지 않는다.

출처: [[2026-06-04-portfolio-review]], [[2026-06-04-0624-analyst-review-cycle-sources]]

## 2026-06-05 00:11 KST hourly-autopilot

`SLB` 1주 regular-session day limit buy가 `57.66 USD` limit으로 제출됐고, Alpaca MCP 기준 `2026-06-04T15:20:39.771624551Z`에 `57.65 USD`로 즉시 체결됐다. 근거는 2026-06-04 portfolio review의 5D follow-through 양호, runtime Alpaca quote `57.65/57.66`에서 spread `0.0173%`, stale order cleanup/core/research/risk gate 통과다. 이 체결은 새 validation lifecycle 표본으로 기록하며 1D/5D/20D review를 추적한다.

출처: [[2026-06-05-0011-hourly-autopilot]], `wiki/trade-ledger/positions/2026-06-05-0011-hourly-autopilot-post-trade.json`

## 2026-06-06 01:15 KST hourly-autopilot

`SLB` 1주 regular-session day limit buy가 `55.70 USD` limit으로 제출됐고, Alpaca MCP `get_order_by_client_id` 기준 `2026-06-05T16:15:33.962605999Z`에 `55.67 USD`로 즉시 체결됐다. 근거는 2026-06-05 portfolio review의 5D follow-through 양호, runtime Alpaca quote `55.68/55.70`에서 spread `0.0359%`, scheduler-owned stale cleanup/core/research preflight와 risk gate 통과다. 이 체결은 같은 energy-services validation 표본의 추가 learning fill로 기록하며 1D/5D/20D review를 추적한다.

출처: [[2026-06-06-0111-hourly-autopilot]], `wiki/trade-ledger/positions/2026-06-06-0111-hourly-autopilot-post-trade.json`

### 2026-06-09 analyst review cycle

`2026-06-05 ET` fill 1D는 `55.67 USD -> 56.55 USD`로 `+1.58%`였다. `SPY` 대비 `+1.34%p`, `QQQ` 대비 `+0.07%p`라 절대수익과 상대수익이 모두 양호했다. 에너지 서비스 validation add는 이번 1D에서는 `양호`이며, oil headline 의존성이 여전히 큰지만 5D에서 다시 본다.

출처: [[2026-06-09-portfolio-review]], [[2026-06-09-0623-analyst-review-cycle-sources]]

### 2026-06-11 analyst review cycle

`2026-06-09 ET` buy 1주는 `55.11 USD` 진입 대비 `2026-06-10 ET` close `55.52 USD`로 `+0.74%`였다. `SPY` 대비 `+2.30%p`, `QQQ` 대비 `+2.74%p`로 energy-services validation은 여전히 benchmark relative가 견조하다. 다만 oil/energy headline 의존성이 큰 점은 유지되며, `2026-06-10 ET` 추가 fill `56.45 USD`는 새 1D 대기 표본이다.

출처: [[2026-06-11-portfolio-review]], [[2026-06-11-0622-analyst-review-cycle-sources]]
