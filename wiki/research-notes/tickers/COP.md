---
symbol: COP
asset_type: stock
---

# COP

## 2026-06-06 01:37 KST hourly-autopilot

`COP` 1주 regular-session day limit buy가 `117.51 USD` limit으로 제출됐다. direct `get_order_by_client_id` 경로는 tool safety monitor가 막혔지만, post-submit Alpaca MCP `get_all_positions` 기준 `COP` 보유수량이 `2주 -> 3주`, 평균단가가 `117.06 -> 117.18`로 갱신돼 이번 1주 validation add가 약 `117.42 USD`에 체결된 것으로 추정 기록했다. 근거는 scheduler-owned stale cleanup/core/research preflight, strict universe/MCP/risk gate 통과, runtime IEX quote `117.49/117.51` 기준 spread `0.0170%`, 그리고 2026-06-05 portfolio review의 5D follow-through 양호다.

## 회고 기록

### 2026-05-30 analyst review cycle

2026-05-28 validation buy 1주는 114.95 USD 진입 대비 2026-05-29 close/current 114.36 USD로 -0.51%, SPY 대비 -0.71%p였다. 손실은 작지만 energy/value hedge 후보로서 1D 우위는 확인되지 않았다. 판단은 `중립 약함`이며 5D/20D 대기.

출처: [[2026-05-30-portfolio-review]], [[2026-05-30-0625-analyst-review-cycle-sources]]
