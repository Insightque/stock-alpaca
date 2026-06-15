---
symbol: V
asset_type: stock
---

# V

## 2026-06-16 02:55 KST hourly-autopilot

`V` 1주 regular-session day limit buy가 `325.01 USD` limit으로 제출됐고, direct Alpaca MCP reconciliation 기준 `client_order_id=hourly-20260616-0251-buy-v`, `order_id=f62ee7ea-b0a4-4765-88e7-630ff20bf0e8`가 `2026-06-15T17:55:48.922618101Z`에 `324.83 USD`로 즉시 체결됐다. 근거는 scheduler-owned `0251` stale cleanup/core/research preflight 재사용, direct Alpaca submit-boundary check 기준 regular market open, open orders `0`, same-day `V` duplicate `0`, quote `324.89/325.01`, spread `0.0369%`, active tradable NYSE stock, 그리고 `[[V]]`의 `2026-06-09` analyst review에서 `2026-06-05 ET` fill 1D가 `중립 양호`였다는 점이다. sell-first 평가에서는 `AVGO/RGTI` same-day sell duplicate와 `SO` trim metric gap이 유지돼 executable risk-reducing sell이 남지 않았고, buy fallback에서는 `COP/XOM/SLB/FCX/JPM/NEE/BAC/WMT/NKE` same-day duplicate, `SPY/QQQ` per-order cap, `NVDA` cluster warning이 차례로 막혀 `V`가 가장 실행 가능한 existing payments diversifier floor-size add로 승격됐다. 이 fill 후 `get_all_positions` 기준 `V qty=4 -> 5`, `avg_entry_price=325.514`로 갱신됐다.

출처: [[2026-06-16-0251-hourly-autopilot]], `wiki/trade-ledger/positions/2026-06-16-0251-hourly-autopilot-post-trade.json`

## 회고 기록

### 2026-05-29 analyst review cycle

2026-05-27 validation buy 1주는 2026-05-28 close 기준 -1.54%로 SPY/QQQ 대비 약했다. Payments quality thesis는 1D에는 확인되지 않았고, Alpaca news의 의회 매도/crypto card volume 이슈는 혼재 신호로만 남긴다.

출처: [[2026-05-29-portfolio-review]], [[2026-05-29-0625-analyst-review-cycle-sources]]

### 2026-05-31 analyst review cycle

2026-05-29 validation add 1주는 331.00 USD 체결 후 주말 현재 326.36 USD reference로 -1.40%지만, 다음 미국 정규장 close 전이라 1D 판단은 보류한다. Payments/growth-quality thesis는 2026-06-01 close 이후 benchmark 대비로 재점검한다.

출처: [[2026-05-31-portfolio-review]], [[2026-05-31-0624-analyst-review-cycle-sources]]
### 2026-06-02 analyst review cycle

2026-05-29 validation add 1주는 331.00 USD 진입 대비 2026-06-01 close 322.73 USD로 -2.50%였다. quality/financial network defensive 성격이 1D에서 SPY/QQQ 대비 방어로 작동하지 않아 `약함`으로 분류한다. 5D/20D 대기.

출처: [[2026-06-02-portfolio-review]], [[2026-06-02-0624-analyst-review-cycle-sources]]
### 2026-06-04 analyst review cycle

2026-05-29 validation add 1주는 331.00 USD 진입 대비 2026-06-03 close 313.635 USD로 -5.25%였다. payments/quality thesis는 5D에서도 SPY/QQQ 대비 방어력을 보여주지 못했다. 판단은 `약함`, 20D까지는 신규 add 근거로 쓰지 않는다.

출처: [[2026-06-04-portfolio-review]], [[2026-06-04-0624-analyst-review-cycle-sources]]


## 2026-06-05 03:11 KST hourly autopilot

2026-06-05 03:11 KST hourly autopilot에서 `V` 1주 regular-session day limit buy를 제출했고, reconciliation 시점 상태는 `new` open order다. 근거는 scheduler research preflight 4/5 usable/pass, runtime spread 0.0375%, same-day duplicate/open-order conflict 없음, payments diversifier floor-size validation 목적이었다.

## 2026-06-06 00:39 KST hourly autopilot

2026-06-06 00:39 KST hourly autopilot에서 `V` 1주 regular-session day limit buy를 `322.41 USD` limit으로 제출했고, Alpaca `client_order_id=hourly-20260606-0031-buy-v`는 `2026-06-05T15:37:28.378344604Z`에 `321.90 USD`로 즉시 체결됐다. 근거는 scheduler research preflight 4/5 usable/pass, preflight quote `322.35/322.41` 기준 spread `0.0186%`, same-day duplicate/open-order conflict 없음, payments diversifier floor-size validation 목적이었다. reconciliation 기준 `V` 보유수량은 4주, 평균단가는 `325.685 USD`다.

### 2026-06-09 analyst review cycle

`2026-06-05 ET` fill 1D는 `321.90 USD -> 319.72 USD`로 `-0.68%`였다. 절대수익은 음수지만 `SPY` 대비 `-0.92%p`, `QQQ` 대비 `-2.19%p`로 drawdown은 제한됐다. payments diversifier validation으로는 `중립 양호`이며, stronger follow-through가 나오는지 5D까지 기다린다.

출처: [[2026-06-09-portfolio-review]], [[2026-06-09-0623-analyst-review-cycle-sources]]
