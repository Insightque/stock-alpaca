---
id: 2026-05-25-one-year-hourly-buy-sell-trend-enhanced-simulation
created_at: 2026-05-25T21:47:28+09:00
source_type: one-year-hourly-buy-sell-simulation
paper: true
orders_submitted: 0
---

# 과거 1년 1시간봉 일별 매입/매도 dry-run 시뮬레이션

## 결론

- 전략: `one-year-hourly-buy-sell-v1`
- 정책 상태: `research_dry_run_observation_only`
- 일별 독립 run 수: 210
- 전체 추천: 2100개, virtual buy 1050개, virtual sell 1050개
- 20D 완료 평가: 1900개
- 20D 방향성 hit rate: 53.21%
- 20D 평균 방향성 SPY 초과수익: +0.57%

virtual sell은 short 주문이 아니라 기존 long 보유분을 팔거나 신규 매수를 피하는 dry-run 판단으로 평가했다. 따라서 sell 평가의 방향성 수익은 해당 종목이 이후 SPY보다 부진했는지를 보는 회피 성과다.

## 단기/장기 평가

| action | horizon | completed | directional hit | avg directional SPY excess | avg long P/L | avg adverse/opportunity |
| --- | --- | --- | --- | --- | --- | --- |
| virtual_buy | same_day | 1050 | 40.57% | -0.22% | -0.20% | -1.55% |
| virtual_buy | 1D | 1045 | 47.56% | -0.02% | +0.09% | -2.51% |
| virtual_buy | 5D | 1025 | 51.51% | +0.41% | +0.84% | -4.60% |
| virtual_buy | 20D | 950 | 53.26% | +3.28% | +4.91% | -7.66% |
| virtual_buy | 60D | 750 | 71.07% | +14.81% | +17.71% | -10.47% |
| virtual_sell | same_day | 1050 | 57.81% | +0.14% | +0.00% | +2.11% |
| virtual_sell | 1D | 1045 | 52.54% | -0.03% | +0.00% | +3.60% |
| virtual_sell | 5D | 1025 | 52.68% | -0.49% | +0.00% | +7.32% |
| virtual_sell | 20D | 950 | 53.16% | -2.14% | +0.00% | +17.45% |
| virtual_sell | 60D | 750 | 60.80% | +0.85% | +0.00% | +31.50% |

## 상위 20D 방향성 결과

| asof | action | symbol | rank | 20D directional | 5D directional |
| --- | --- | --- | --- | --- | --- |
| 2026-04-07 | virtual_buy | INTC | 5 | +100.61% | +16.35% |
| 2026-04-13 | virtual_buy | INTC | 1 | +93.57% | -1.43% |
| 2026-04-10 | virtual_buy | INTC | 1 | +91.29% | +4.41% |
| 2026-04-08 | virtual_buy | INTC | 2 | +85.90% | +9.21% |
| 2026-04-14 | virtual_buy | INTC | 3 | +83.34% | +2.27% |
| 2026-04-13 | virtual_buy | AMD | 3 | +78.81% | +8.02% |
| 2026-04-15 | virtual_buy | INTC | 1 | +76.92% | -2.52% |
| 2026-04-10 | virtual_buy | AMD | 3 | +74.53% | +7.40% |
| 2026-04-09 | virtual_buy | INTC | 1 | +73.30% | +9.39% |
| 2026-04-14 | virtual_buy | AMD | 2 | +72.81% | +12.08% |

## 에이전트 진행 기록

- 일별 agent report: 251일치가 JSON에 저장됐다.
- Coordinator/Universe/Market Data/Web Research/Simulation/Risk-Policy Agent가 각 기준일 상태를 기록했다.
- 실행 중 Codex 작업창에는 Market Data Agent와 Simulation Agent 진행 줄을 출력하도록 `--progress`를 사용했다.

## 데이터 품질과 MCP

- source feed: `alpaca_iex`
- bar interval: `1Hour`
- symbols loaded: 62 / 62
- hourly bars loaded: 114060
- fill model: virtual entry at second available 1Hour bar close; horizon exits at regular-session daily close
- slippage model: strategy config round-trip spread/slippage bps applied to directional evaluation
- event feature cache 사용: true
- event feature 매칭: 2100 / 2100 (100.00%)
- research MCP 서버: alpaca
- 원천 hash: `sha256:20f49fc662e0153d8aaa357961b94a37867cddf60e76dd4cacff9eb9c079c7c1`

## 정책 반영

- 이 결과는 research/backtest 전용이며 `orders_submitted=0`이다.
- 1시간봉 기반 판단은 자동 주문 후보로 승격하지 않고 `observation_only`로 유지한다.
- 실제 정책 변경은 별도 proposal과 추가 out-of-sample 검증이 필요하다.
