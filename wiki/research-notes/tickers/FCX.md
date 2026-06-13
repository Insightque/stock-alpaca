# FCX

Freeport-McMoRan paper validation 후보. 2026-05-26 hourly autopilot에서 materials/mining 및 commodity-cyclical 분산, SEC/Yahoo/FRED 확인을 근거로 1주 validation buy가 체결됐다.

## 2026-06-05 01:31 KST hourly-autopilot

`FCX` 1주 regular-session day limit buy가 `69.58 USD` limit으로 제출됐고, Alpaca MCP 기준 `2026-06-04T16:41:07.019702918Z`에 `69.51 USD`로 즉시 체결됐다. 근거는 scheduler core/research preflight와 strict universe/MCP/risk gate 통과, same-day duplicate가 없는 기존 materials/mining holding, 그리고 runtime IEX quote `69.56/69.58` 기준 spread `0.0288%`가 policy 한도 이내였다는 점이다. 이 체결은 새 validation lifecycle 표본으로 기록하며 1D/5D/20D review를 추적한다.

출처: [[2026-06-05-0131-hourly-autopilot]], `wiki/trade-ledger/positions/2026-06-05-0131-hourly-autopilot-post-trade.json`

## 2026-06-05 23:31 KST hourly-autopilot

`FCX` 1주 regular-session day limit buy가 `65.31 USD` limit으로 제출됐고, Alpaca MCP `get_order_by_client_id` 기준 `2026-06-05T14:39:22.134743752Z`에 `65.15 USD`로 즉시 체결됐다. 근거는 scheduler-owned `2331` core/research preflight, strict universe/MCP/risk gate 통과, 같은 ET session `BAC`/`WMT` duplicate 제외 이후에도 남는 materials/mining diversifier 수요, 그리고 scheduler quote `65.28/65.31` 기준 spread `0.0460%`가 policy 한도 이내였다는 점이다. direct post-fill `get_all_positions/get_account_info` refresh는 runtime safety monitor가 취소돼 post-trade snapshot은 fresh 2331 preflight에 confirmed fill을 결합해 기록했다.

출처: [[2026-06-05-2331-hourly-autopilot]], `wiki/trade-ledger/positions/2026-06-05-2331-hourly-autopilot-post-trade.json`

## 회고 기록

- 2026-05-28: [[2026-05-28-portfolio-review]]에서 2026-05-26 validation buy 1D interim review를 작성했다. 63.94 USD 진입 대비 2026-05-27 close 63.625 USD로 -0.49%, SPY 대비 -0.51%p였다. 손실은 작지만 commodity 분산 thesis의 우위는 1D에 확인되지 않아 5D/20D 대기다.

### 2026-06-09 analyst review cycle

`2026-06-05 ET` fill 1D는 `65.15 USD -> 63.88 USD`로 `-1.95%`였다. `SPY` 대비 `-2.19%p`, `QQQ` 대비 `-3.46%p`라 materials/mining diversifier add는 첫날 우위를 보여주지 못했다. 판단은 `중립 약함`이며 commodity follow-through는 5D까지 더 봐야 한다.

출처: [[2026-06-09-portfolio-review]], [[2026-06-09-0623-analyst-review-cycle-sources]]

## 2026-06-10 04:18 KST hourly-autopilot

`FCX` 1주 regular-session day limit buy가 `64.02 USD` limit으로 제출됐고, Alpaca MCP 기준 `client_order_id=hourly-20260610-0411-buy-fcx`, `order_id=80a34b1a-5044-47cf-aadc-338e0db675f9`가 생성된 뒤 same client id reconciliation에서 `2026-06-09T19:18:02.754609037Z`에 `63.75 USD`로 즉시 체결됐다. 근거는 scheduler-owned `0411` stale cleanup/core/research preflight와 live Alpaca MCP submit-boundary check 기준 paper mode/market open/universe strict/MCP strict/risk strict 모두 통과했고, sell-first 재평가에서 executable risk-reducing sell이 남지 않은 뒤 same-day duplicate가 없는 materials/mining existing holding floor-size add가 learning_trade_directive를 가장 보수적으로 충족했다는 점이다.

출처: [[2026-06-10-0411-hourly-autopilot]], `wiki/trade-ledger/positions/2026-06-10-0411-hourly-autopilot-post-trade.json`

### 2026-06-11 analyst review cycle

`2026-06-09 ET` buy 1주는 `63.75 USD` 진입 대비 `2026-06-10 ET` close `62.07 USD`로 `-2.64%`였다. `SPY` 대비 `-1.08%p`, `QQQ` 대비 `-0.63%p`로 broad market보단 약간 덜 약했지만 commodity/materials diversifier의 clear edge는 아니었다. 판단은 `중립 약함` 유지이며 `2026-06-10 ET` 추가 fill `62.21 USD`도 별도 1D 대기 표본이다.

출처: [[2026-06-11-portfolio-review]], [[2026-06-11-0622-analyst-review-cycle-sources]]

### 2026-06-12 analyst review cycle

`2026-06-10 ET` add 1주는 `62.21 USD` 대비 `2026-06-11 ET` close/current `66.24 USD`로 `+6.48%`였고, `2026-06-05 ET` fill 5D도 `65.15 USD -> 66.24 USD`로 `+1.67%`였다. 이번 cycle에서는 materials/mining diversifier가 가장 선명한 회복 표본이었다. 다만 commodity sleeve 특성상 변동성이 큰 만큼 즉시 정책 승격까지는 가지 않는다.

출처: [[2026-06-12-portfolio-review]], [[2026-06-12-0632-analyst-review-cycle-sources]]

### 2026-06-13 analyst review cycle

`2026-06-05 ET` fill 5D는 `65.15 USD -> 68.40 USD`로 `+4.99%`까지 확장됐다. `SPY` 대비 `+4.42%p`, `QQQ` 대비 `+2.73%p`라 기존 materials/copper diversifier 가설을 가장 강하게 지지한 표본이다. 다만 review backlog 아래에서 hindsight 강세 표본이 된 만큼, 다음 cycle에서는 selection alpha와 backlog throttle 비용을 함께 추적한다.

출처: [[2026-06-13-portfolio-review]], [[2026-06-13-0622-analyst-review-cycle-sources]]

### 2026-06-14 analyst review cycle

토요일 Alpaca clock 기준 새 미국 정규장 close가 없어 `FCX` hindsight 강세 표본 해석만 유지했다. current snapshot 기준 `FCX`는 `5주`, 평균단가 `64.912 USD`, current `68.41 USD`, 미실현 약 `+5.39%`로 backlog throttle의 missed-upside 비용을 계속 보여주지만, 단일 추가 표본만으로 throttle policy를 완화하지는 않는다.

출처: [[2026-06-14-portfolio-review]], [[2026-06-14-0623-analyst-review-cycle-sources]]
