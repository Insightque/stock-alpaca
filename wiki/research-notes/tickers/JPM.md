---
symbol: JPM
asset_type: stock
---

# JPM

## 현재 Thesis

`JPM`은 정규장 scheduled hourly autopilot의 0351 cycle에서 financials diversifier floor-size validation 후보로 승격됐다. scheduler-owned 0351 core/research preflight 기준 `JPM`은 active/tradable US equity이고 latest quote가 `311.98/312.04`, spread 약 `0.0192%`로 policy cap 안에 있었다. `2026-06-05` portfolio review는 financials late-follow-through (`BAC` 사례)를 긍정적으로 기록했고, 0351 research preflight는 `sec-edgar`, `fred`, `firecrawl`, `yahoo-finance`를 usable confirmation으로 남겼다.

## 포트폴리오 맥락

- 역할: `financials` cluster diversifier
- sizing 해석: `paper_validation_execution.validation_order_sizing.validation_floor` 1주
- hard gate 메모: same-day duplicate buy 없음, open order 0건, review backlog throttle pass, per-order validation cap 이내

## 리스크

- bank_rate_sensitive factor라 macro/rates headwind에 민감하다.
- financials cluster existing exposure(`BAC`, `V`) 위에 add되는 만큼 후속 1D/5D/20D validation review가 필요하다.
- Alpha Vantage는 0351 preflight에서 one-call throttle `provider_error` gap으로 남아 earnings/news 보강은 제한적이다.

## 출처

- [[2026-06-05-portfolio-review]]
- `wiki/evidence-store/sources/2026-06-06-0351-hourly-autopilot-alpaca-core-preflight.json`
- `wiki/evidence-store/sources/2026-06-06-0351-hourly-autopilot-research-mcp-preflight.json`
- `harness/recommendation-policy.yaml`
- `harness/risk-policy.yaml`

## 거래 기록

- 2026-06-06 04:02 KST: scheduled hourly-autopilot에서 `hourly-20260606-0351-buy-jpm` 1주 regular-session day limit buy가 `311.81 USD`에 체결됐다.
- 주문/체결 출처: [[2026-06-06-0351-hourly-autopilot]], `wiki/trade-ledger/positions/2026-06-06-0351-hourly-autopilot-post-trade.json`

## 회고 기록

### 2026-06-06 analyst review cycle

`JPM` 신규 1주는 `311.81 USD` 진입 뒤 첫 close `312.38 USD`로 day-one 절대손익은 소폭 플러스였다. Yahoo Finance는 financials rotation headline과 recommendation breadth `strongBuy 4 / buy 8 / hold 12 / sell 0 / strongSell 0`를 보였고, Alpaca recent fill ledger도 immediate fill을 확인했다. 다만 아직 1D horizon 전이므로 판단은 `회고 대기`다.

출처: [[2026-06-06-portfolio-review]], [[2026-06-06-0626-analyst-review-cycle-sources]]

### 2026-06-07 analyst review cycle

`2026-06-06` 미국 정규장 close 기준 `JPM` 1주의 공식 1D horizon은 아직 도래하지 않았다. current Alpaca snapshot close/current는 `312.38 USD`로 평균단가 `311.81 USD` 대비 `+0.18%`이며, financials benchmark `XLF`도 같은 날 `+0.18%`였다. 따라서 현재 평가는 `회고 대기 유지`다.

출처: [[2026-06-07-portfolio-review]], [[2026-06-07-0623-analyst-review-cycle-sources]]

### 2026-06-08 analyst review cycle

`2026-06-07 17:22 ET` closed-market scan 기준 `JPM` 1주의 공식 1D horizon은 여전히 열리지 않았다. current close/current `312.37 USD`는 평균단가 `311.81 USD` 대비 `+0.18%`로 사실상 전일과 같은 수준이고, Yahoo recommendation breadth도 `strongBuy 4 / buy 8 / hold 12 / sell 0 / strongSell 0`로 급격한 악화는 없다. 이번 run의 판단도 `회고 대기 유지`다.

출처: [[2026-06-08-portfolio-review]], [[2026-06-08-0622-analyst-review-cycle-sources]]

### 2026-06-09 analyst review cycle

`2026-06-05 ET` fill 1D는 `311.81 USD -> 311.11 USD`로 `-0.22%`였다. 절대수익은 소폭 음수지만 `SPY +0.24%`, `QQQ +1.51%`와 비교한 underperformance보다 `XLF -0.59%` 대비 상대방어가 더 중요했다. financials diversifier floor-size validation으로는 `중립 양호`이며 5D는 `2026-06-12 ET` close 이후 다시 본다.

출처: [[2026-06-09-portfolio-review]], [[2026-06-09-0623-analyst-review-cycle-sources]]

### 2026-06-13 analyst review cycle

`2026-06-05 ET` fill 5D는 `311.81 USD -> 320.71 USD`로 `+2.85%`였다. `SPY` 대비 `+2.28%p`, `QQQ` 대비 `+0.59%p`라 이번 cycle에서는 financials diversifier 표본 중 가장 깔끔한 쪽에 속한다. 공격적 승격 근거까지는 아니어도 hold-quality는 `양호`로 한 단계 더 명확해졌다.

출처: [[2026-06-13-portfolio-review]], [[2026-06-13-0622-analyst-review-cycle-sources]]


## 2026-06-16 01:00 KST hourly-autopilot

`JPM` 1주 regular-session day limit buy가 `321.54 USD` limit으로 제출됐고, Alpaca MCP 기준 `client_order_id=hourly-20260616-0051-buy-jpm`, `order_id=c489bba3-0a3c-4623-8435-87a7bbacf894`가 생성된 뒤 same client id reconciliation에서 `2026-06-15T16:00:28.027169137Z`에 `321.53 USD`로 즉시 체결됐다. 근거는 scheduler-owned `0051` stale cleanup/core/research preflight와 direct Alpaca submit-boundary check 기준 paper mode/market open/universe strict/MCP strict/risk strict 모두 통과했고, sell-first 재평가에서 `AVGO/RGTI`는 same-day duplicate sell, `SO`는 trim metric gap, `NEE/BAC/WMT`는 same-day duplicate buy에 막힌 뒤 `JPM`이 existing financials diversifier 중 가장 깔끔한 floor-size learning buy로 남았다는 점이다. post-trade 기준 보유 수량은 `1주 -> 2주`, 평균단가는 `316.67 USD`로 갱신됐다.

출처: [[2026-06-16-0051-hourly-autopilot]], `wiki/trade-ledger/positions/2026-06-16-0051-hourly-autopilot-post-trade.json`
