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
