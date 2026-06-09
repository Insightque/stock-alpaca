# AAPL

Apple paper validation 후보. 2026-05-26 hourly autopilot에서 mega-cap quality, agentic AI optionality, SEC/Yahoo/FRED 확인을 근거로 1주 validation buy가 체결됐다.

## 회고 기록

- 2026-05-28: [[2026-05-28-portfolio-review]]에서 2026-05-26 validation buy 1D interim review를 작성했다. 309.45 USD 진입 대비 2026-05-27 close 310.93 USD로 +0.48%, SPY 대비 +0.46%p였다. AI semiconductor cluster가 아닌 mega-cap quality 분산 목적은 1D 기준 양호했다.


## 2026-06-05 00:31 KST hourly-autopilot

`AAPL` 1주 regular-session day limit buy가 `310.10 USD` limit으로 제출됐고, Alpaca MCP 기준 `2026-06-04T15:41:26.912888446Z`에 `310.07 USD`로 즉시 체결됐다. 근거는 stale BAC open order 취소 후 open-order lifecycle gate 복구, runtime Alpaca quote `310.06/310.10`에서 spread `0.0129%`, scheduler core/research preflight와 strict universe/MCP/risk gate 통과, 그리고 기존 mega-cap quality validation holding으로서 duplicate-free add가 가능했다는 점이다. 이 체결은 새 validation lifecycle 표본으로 기록하며 1D/5D/20D review를 추적한다.

출처: [[2026-06-05-0031-hourly-autopilot]], `wiki/trade-ledger/positions/2026-06-05-0031-hourly-autopilot-post-trade.json`

## 2026-06-06 00:19 KST hourly-autopilot

`AAPL` 1주 regular-session day limit add가 `314.25 USD` limit으로 제출됐고, Alpaca MCP 기준 `2026-06-05T15:19:25.344149286Z`에 `313.27 USD`로 즉시 체결됐다. 근거는 scheduler-owned `0011` core/research preflight와 strict universe/MCP/risk gate 통과, runtime quote `313.02/314.25`에서 spread `0.3929%`, same-day duplicate/open-order conflict 부재, 그리고 `PLTR/BAC/WMT/FCX` duplicate block 및 `QQQ/SPY` notional cap 초과 이후 남은 가장 보수적인 mega-cap quality floor-size validation add였다는 점이다. 이 체결 후 runtime `get_all_positions` 기준 `AAPL` 보유수량은 3주, 평균단가는 `310.93 USD`로 갱신됐다.

출처: [[2026-06-06-0011-hourly-autopilot]], `wiki/trade-ledger/positions/2026-06-06-0011-hourly-autopilot-post-trade.json`

### 2026-06-09 analyst review cycle

`2026-06-05 ET` fill 1D는 `313.27 USD -> 301.57 USD`로 `-3.73%`였다. `SPY` 대비 `-3.98%p`, `QQQ` 대비 `-5.25%p`라 mega-cap quality add의 immediate timing은 좋지 않았다. 판단은 `약함`이며, broad tech dip에서 quality label만으로 추가 진입 cadence를 높이면 안 된다는 표본으로 남긴다.

출처: [[2026-06-09-portfolio-review]], [[2026-06-09-0623-analyst-review-cycle-sources]]

### 2026-06-10 analyst review cycle

current Alpaca snapshot상 `AAPL`은 `3주`, 평균단가 `310.93 USD`, current `290.913 USD`로 미실현 `-6.44%`다. `2026-06-05 ET` add 1D의 `약함` 판단 뒤에도 하루 더 밀렸기 때문에, mega-cap quality label만으로 add cadence를 높이지 않는다는 해석이 더 강화됐다. `2026-06-12 ET` 5D review 전까지는 recovery confirmation이 필요하다.

출처: [[2026-06-10-portfolio-review]], [[2026-06-10-0622-analyst-review-cycle-sources]]
