# 2026-06-05-0431-hourly-autopilot scheduled paper autopilot

## 요약

정규장 scheduled hourly autopilot을 실행했다. `.env`의 `ALPACA_PAPER_TRADE=true` 요구를 유지했고, scheduler-owned `0431` stale cleanup/core/research preflight를 우선 사용했다. runtime Alpaca clock `2026-06-04T15:34:34.668842082-04:00` 기준 미국 정규장은 열려 있었고, scheduler core preflight와 symbol-specific duplicate 점검 기준 open-order lifecycle도 유지됐다. research preflight는 `sec-edgar`, `fred`, `firecrawl`, `yahoo-finance` 4개 provider가 usable/pass였고, `alpha-vantage`는 `empty_response` nonblocking gap으로 남았다.

이번 run은 `submit` mode였다. sell/trim 후보를 먼저 평가했지만 `AVGO`, `SO`, `TSLA`는 여전히 decision-grade metric 또는 held-quantity gate에 막혔다. 같은 ET regular session same-day duplicate 규칙 때문에 `BAC`, `QQQ`, `SPY`와 2026-06-04 filled cohort는 재사용 우선순위를 낮췄다. `NVDA`는 ai_semiconductor_complex warning band와 기존 큰 보유 비중 때문에 신규 add 우선순위에서 밀렸고, `TSLA`는 speculative growth지만 약한 review 때문에 `PLTR`보다 낮게 평가했다. `PLTR`은 기존 1주 보유의 low-notional ai_software/speculative_growth 포지션으로, runtime quote `141.47/141.51`에서 spread `0.0283%`, scheduler asset check active/tradable, symbol-specific all-order 조회 기준 이번 ET session duplicate/open-order conflict 없음, review backlog throttle 통과, strict universe/MCP/risk gate 유지 조건을 모두 충족해 1주 validation buy를 제출했다. Alpaca MCP는 `order_id=257d23eb-d449-4e25-8276-efce67f15ace`를 생성했고 reconciliation 시점 상태는 `new`였다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env`의 `ALPACA_PAPER_TRADE=true` 확인 |
| Market clock | PASS | runtime `get_clock` `2026-06-04T15:34:34.668842082-04:00`, regular market open |
| Stale order lifecycle | PASS | scheduler cleanup pass, scheduler preflight open orders 0건, PLTR symbol-specific duplicate conflict 없음 |
| Alpaca core MCP | PASS | scheduler-owned core preflight hard gate pass, runtime `get_clock/get_account_info/get_stock_latest_quote/get_orders(symbol=PLTR)/get_asset(PLTR)` 보조 확인 |
| Research MCP | PASS tiered | SEC EDGAR/FRED/Firecrawl/Yahoo positive; Alpha Vantage는 `empty_response` nonblocking gap |
| Universe strict | PASS | metadata universe 62개, SPY/QQQ 포함 |
| Quote/spread | PASS for submitted order | PLTR runtime quote `2026-06-04T19:34:53.760810005Z`, spread `0.0283%` |
| Risk plan | PASS | PLTR 1주 buy notional `141.51`, cash/ticker/theme/factor/cluster caps 통과 |
| Final submit path | PASS | Alpaca MCP가 `PLTR` 1주 regular day limit buy를 생성했고 reconciliation 기준 `status=new`다 |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| PLTR | submitted_open | 0.0283% | existing ai_software/speculative_growth holding으로 runtime quote/asset check와 duplicate 재확인을 통과해 1주 floor-size learning add를 제출했고 reconciliation 시점에는 `status=new` open order다. |
| BAC | watch | 0.0185% | 같은 ET regular session 15:21 filled buy가 있어 duplicate discipline으로 재사용 우선순위를 낮췄다. |
| NVDA | watch | 0.0772% | 핵심 AI thesis는 유지되지만 ai_semiconductor_complex warning band와 기존 큰 보유 비중 때문에 add 우선순위를 낮췄다. |
| TSLA | watch | 0.0167% | speculative growth와 약한 review 때문에 floor-size learning order 우선순위에서는 밀렸다. |
| QQQ | blocked | 0.0040% | 같은 ET regular session 14:20 filled benchmark buy 이력 때문에 duplicate discipline을 유지했다. |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| AVGO | watch | decision_grade_metric_gap | AI semiconductor_complex 경고구간과 급락 반전으로 trim 재점검 대상이지만 decision-grade expected-excess와 replacement margin이 비어 있다. |
| SO | watch | decision_grade_metric_gap | defensive/utilities review 약세와 rate-sensitive 부담은 있지만 per-symbol decision-grade expected-excess 공백이 남아 있다. |
| TSLA | watch | held_quantity_and_metric_gap | 약한 validation review와 speculative growth 성격은 재점검 대상이지만 1주 보유라 whole-share trim 규칙을 만족시키기 어렵고 metric도 비어 있다. |

## 주문 제출과 reconciliation

- Submitted order: `PLTR` buy 1 @ `141.51` day limit
- Alpaca order id: `257d23eb-d449-4e25-8276-efce67f15ace`
- Client order id: `hourly-20260605-0431-buy-pltr`
- Pre-submit gate summary: paper mode `true`, market open, universe strict `PASS`, MCP strict `PASS`, risk `PASS`, PLTR quote freshness/spread `PASS`, same-day duplicate/open-order conflict 없음
- `place_stock_order`: 성공, initial response `pending_new`, repeated reconciliation 기준 `status=new`
- Reconciliation: `get_order_by_client_id`, `get_order_by_id`, `get_orders(status=open)`, `get_all_positions`, `get_account_info` 교차확인 기준 open order는 `PLTR` 1건이다. `get_orders(status=closed, symbols=PLTR)`는 prior 2026-05-28 fill만 보여 이번 주문 fill은 아직 없음을 확인했다. `PLTR` 보유수량은 여전히 1주이고, post-submit account snapshot은 cash `30,629.38`, portfolio value `103,753.74`, buying power `255,191.08`, long market value `73,124.36`이다.

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | 62 symbols, SPY/QQQ 포함, final candidates 5개 |
| `check-mcp-coverage.py --strict --json` | PASS | Alpaca core pass, positive research 4개, Alpha `empty_response` gap only |
| `check-risk-policy.py --json` | PASS | PLTR 1주 regular-session day limit buy 계획 통과 |

## 산출물

- Report: `wiki/current-runs/daily/2026-06-05-0431-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-05-0431-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-05-0431-hourly-autopilot.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-05-0431-hourly-autopilot-post-trade.json`

## 지표 설명

- `sell_candidate_diagnostics`: 보유 포지션 중 trim/exit 재점검이 필요한 상위 후보와 metric gap 사유를 남기는 audit trail이다.
- `empty_response`: 이번 cycle의 Alpha Vantage는 shortlisted symbols에서 usable `NEWS_SENTIMENT` item이 0건이라 nonblocking gap으로 남겼다.
- `same-day duplicate discipline`: 같은 ET regular session에서 이미 체결된 동일 symbol/side buy 또는 benchmark buy 재사용을 피하는 규칙이다.
- `portfolio_fit`: hard gate가 아니라 ranking/sizing 입력이다. 이번 run에서는 AI cluster warning이 있는 NVDA와 weak/speculative TSLA보다 PLTR을 floor-size learning add 우선순위로 선택했다.
