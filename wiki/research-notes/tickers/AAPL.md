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

## 2026-06-10 10:17 KST after-hours-autopilot

`AAPL` 1주 after-hours day limit buy가 `291.68 USD` limit으로 제출됐고, Alpaca MCP 기준 `2026-06-10T01:17:49.685900178Z`에 `291.40 USD`로 즉시 체결됐다. 근거는 scheduler-owned `1011` core/research preflight와 strict universe/MCP/risk gate 통과, runtime overnight quote `291.13/291.68`에서 spread `0.1886%`, per-order notional cap 통과, same-day duplicate/open-order conflict 부재, 그리고 `QQQ/SPY/SMH` per-order cap 초과 및 `AVGO/RGTI/SO` sell-side gate 실패 이후 남은 가장 보수적인 mega-cap quality floor-size add였다는 점이다. 이 체결 후 runtime `get_all_positions` 기준 `AAPL` 보유수량은 4주, 평균단가는 `306.0475 USD`로 낮아졌다.

출처: [[2026-06-10-1011-after-hours-autopilot]], `wiki/trade-ledger/positions/2026-06-10-1011-after-hours-autopilot-post-trade.json`

## 2026-06-10 10:35 KST after-hours-autopilot

`AAPL` 1주 after-hours day limit buy가 `291.54 USD` limit으로 제출됐고, Alpaca MCP 기준 `2026-06-10T01:35:02.497251991Z`에 `291.49 USD`로 즉시 체결됐다. 근거는 scheduler-owned `1031` core/research preflight와 strict universe/MCP/risk gate 통과, runtime overnight quote `291.48/291.54`에서 spread `0.0206%`, separate after-hours order budget의 마지막 슬롯 사용, same-day duplicate/open-order conflict 부재, 그리고 `QQQ/SPY/SMH` per-order cap 초과 및 `AVGO/RGTI/SO` sell-side gate 실패 이후 남은 가장 보수적인 mega-cap quality floor-size add였다는 점이다. `INTC`도 cap 안이었지만 shortlist 우선순위와 liquidity quality에서 `AAPL`이 앞섰다. 이 체결 후 runtime `get_all_positions` 기준 `AAPL` 보유수량은 5주, 평균단가는 `303.136 USD`로 더 낮아졌다.

출처: [[2026-06-10-1031-after-hours-autopilot]], `wiki/trade-ledger/positions/2026-06-10-1031-after-hours-autopilot-post-trade.json`

## 2026-06-16 04:39 KST hourly-autopilot

`AAPL` 1주 regular-session day limit add가 `296.15 USD` limit으로 제출됐고, Alpaca MCP 기준 `2026-06-15T19:39:22.121175974Z`에 `296.11 USD`로 즉시 체결됐다. 근거는 scheduler-owned `0431` stale cleanup/core/research preflight와 strict universe/MCP/risk gate 통과, direct quote `296.12/296.15`에서 spread `0.0101%`, same-day duplicate/open-order conflict 부재, 그리고 `AMZN/GOOGL/MSFT/SO/V/COP/NKE/XOM/SLB/FCX/JPM/NEE/WMT/BAC` duplicate buy, `SPY/QQQ` per-order cap 초과, `NVDA` cluster warning 이후 남은 가장 보수적인 mega-cap quality floor-size add였다는 점이다. repeated weak-review history는 ranking note로만 남기고 hard gate를 막지는 않았다. 이 체결 후 runtime `get_all_positions` 기준 `AAPL` 보유수량은 `5주 -> 6주`, 평균단가는 `303.136 USD -> 301.965 USD`로 낮아졌다.

출처: [[2026-06-16-0431-hourly-autopilot]], `wiki/trade-ledger/positions/2026-06-16-0431-hourly-autopilot-post-trade.json`

### 2026-06-11 analyst review cycle

`2026-06-09 ET` after-hours add 2건은 `291.40 USD`, `291.49 USD` 체결 대비 `2026-06-10 ET` close `291.48 USD`로 각각 `+0.03%`, `-0.00%`였다. 절대성과는 flat이지만 `SPY -1.56%`, `QQQ -2.00%` 하락일에 benchmark relative는 방어적이었다. 다만 기존 `2026-06-05 ET` regular-session add 1D `약함` 이력은 그대로라, cost-basis 개선과 `quality dip-buy cadence` 검증은 분리해서 봐야 한다.

출처: [[2026-06-11-portfolio-review]], [[2026-06-11-0622-analyst-review-cycle-sources]]

### 2026-06-12 analyst review cycle

`2026-06-05 ET` regular-session add 1주는 `313.27 USD` 진입 대비 `2026-06-11 ET` close/current `295.5 USD`로 `-5.67%`였다. `SPY` 대비 `-5.73%p`, `QQQ` 대비 `-7.23%p`라 5D 기준으로도 mega-cap quality averaging-down cadence는 약했다. after-hours add로 평균단가를 낮춘 효과는 별개지만, 새로운 add 근거로 쓰기에는 아직 회복 증거가 부족하다.

출처: [[2026-06-12-portfolio-review]], [[2026-06-12-0632-analyst-review-cycle-sources]]

### 2026-06-13 analyst review cycle

current Alpaca snapshot 기준 `AAPL`은 `5주`, 평균단가 `303.136 USD`, current `291.37 USD`로 미실현 약 `-3.88%`다. Yahoo Finance 기사에는 AI memory cost와 pricing dilemma, WWDC 이후 devices/services refocus narrative가 함께 잡혔고, analyst action도 `2026-06-09` target raise 다수와 `Rosenblatt Neutral`, `Needham Hold`가 병존한다. 따라서 이번 cycle에서도 `mega-cap quality averaging-down`은 관찰 가설로만 남긴다.

출처: [[2026-06-13-portfolio-review]], [[2026-06-13-0622-analyst-review-cycle-sources]]

### 2026-06-14 analyst review cycle

live Alpaca clock이 `2026-06-13 17:22 ET` 토요일 closed 상태라 지난 cycle 이후 새 미국 정규장 close가 없었다. current snapshot 기준 `AAPL`은 `5주`, 평균단가 `303.136 USD`, current `291.13 USD`, 미실현 약 `-3.96%`이며, Alpha Vantage latest quarter EPS beat(`2026-04-30`, `2.01 vs 1.94`)에도 불구하고 `mega-cap quality averaging-down`을 강화할 새 tape confirmation은 생기지 않았다.

출처: [[2026-06-14-portfolio-review]], [[2026-06-14-0623-analyst-review-cycle-sources]]

### 2026-06-15 analyst review cycle

live Alpaca clock이 `2026-06-14 17:21 ET` 일요일 closed 상태라 새 미국 정규장 closeout은 여전히 없었다. current snapshot 기준 `AAPL`은 `5주`, 평균단가 `303.136 USD`, current `291.13 USD`, 미실현 약 `-3.96%`이며, Alpaca IEX daily bar `291.085`는 전일 대비 `-1.49%`였다. SEC EDGAR 최근 filing은 `2026-05-29` Form 4까지 확인됐고, Yahoo Finance 기사도 AI narrative 개선 기대와 India 공급망 부담이 병존해 `mega-cap quality averaging-down`은 계속 관찰 가설로만 둔다.

출처: [[2026-06-15-portfolio-review]], [[2026-06-15-0624-analyst-review-cycle-sources]]

### 2026-06-16 analyst review cycle

current Alpaca snapshot 기준 `AAPL`은 `6주`, 평균단가 `301.965 USD`, `2026-06-15 ET` close `296.53 USD`로 미실현 약 `-1.80%`다. Alpha Vantage latest quarter는 `2026-04-30` reported EPS `2.01`로 estimate `1.94`를 상회했고, SEC EDGAR recent filings는 `2026-05-29` Form 4까지 확인됐다. 다만 Yahoo Finance 기사에서는 mega-cap valuation headwind와 공급망/메모리 비용 부담이 계속 병존해 `2026-06-15 ET` add 1주를 새 `1D` 대기 표본으로만 등록한다. 평균단가 낮추기 가설은 아직 검증 전이다.

출처: [[2026-06-16-portfolio-review]], [[2026-06-16-0621-analyst-review-cycle-sources]], [[2026-06-16-0431-hourly-autopilot]]
