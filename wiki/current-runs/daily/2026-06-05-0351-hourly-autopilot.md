# 2026-06-05-0351-hourly-autopilot scheduled paper autopilot

## 요약

정규장 scheduled hourly autopilot을 실행했다. `.env`의 `ALPACA_PAPER_TRADE=true` 요구를 확인했고, scheduler-owned `0351` stale cleanup/core/research preflight를 우선 사용했다. runtime Alpaca clock `2026-06-04T14:55:05.687995495-04:00` 기준 미국 정규장은 열려 있었고, scheduler core preflight와 runtime `get_orders(status=open)` 기준 open-order lifecycle도 유지됐다. research preflight는 `sec-edgar`, `fred`, `firecrawl`, `yahoo-finance` 4개 provider가 usable/pass였고, `alpha-vantage`는 one-call-per-hour throttle 때문에 `provider_error` nonblocking gap으로 남았다.

이번 run은 `submit` mode였다. sell/trim 후보를 먼저 평가했지만 `AVGO`, `SO`, `TSLA`는 여전히 decision-grade metric 또는 held-quantity gate에 막혔다. `QQQ`, `SPY`, `SLB`, `AAPL`, `XOM`, `WMT`, `FCX`, `COP`, `GOOGL`, `MSFT`, `NEE`, `V`, `NKE`는 같은 ET regular session same-day filled buy라 duplicate discipline 때문에 제외했고, `BAC`는 같은 세션 earlier submit/cancel 이력으로 재사용 우선순위를 낮췄다. `NVDA`는 AI semiconductor_complex warning band와 기존 큰 보유 비중 때문에 신규 add 우선순위에서 밀렸다. `TSLA`는 speculative growth와 약한 review 때문에 `SO`보다 ranking이 낮았다. `SO`는 research preflight shortlist 포함, runtime quote `90.97/90.98`에서 spread `0.0110%`, scheduler core asset check active/tradable, same-day duplicate/open-order 충돌 없음, review backlog throttle 통과, strict universe/MCP/risk gate 유지 조건을 모두 충족해 1주 validation buy를 제출했고 same-minute fill로 정리됐다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env`의 `ALPACA_PAPER_TRADE=true` 확인 |
| Market clock | PASS | runtime `get_clock` `2026-06-04T14:55:05.687995495-04:00`, regular market open |
| Stale order lifecycle | PASS | scheduler cleanup pass, core preflight open orders 0건, runtime `get_orders(status=open)` 0건 |
| Alpaca core MCP | PASS | scheduler-owned core preflight hard gate pass, runtime `get_clock/get_orders/get_account_activities/get_account_info/get_stock_latest_quote` 보조 확인 |
| Research MCP | PASS tiered | SEC EDGAR/FRED/Firecrawl/Yahoo positive; Alpha Vantage는 `provider_error` nonblocking gap |
| Universe strict | PASS | metadata universe 62개, SPY/QQQ 포함 |
| Quote/spread | PASS for submitted order | SO runtime quote `2026-06-04T18:55:24.067393645Z`, spread `0.0110%` |
| Risk plan | PASS | SO 1주 buy notional `90.98`, cash/ticker/theme/factor/cluster caps 통과 |
| Final submit path | PASS | Alpaca MCP가 `SO` 1주 regular day limit buy를 생성했고 reconciliation 기준 `filled_avg_price=90.95`다 |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| SO | submitted_filled | 0.0110% | utilities diversifier existing holding으로 runtime quote/asset check와 duplicate/open-order 재확인을 통과해 1주 validation buy를 제출했고 same-minute filled 상태다. |
| BAC | watch | 0.0185% | financials diversifier지만 같은 ET 세션 earlier submit/cancel 이력이 있어 duplicate-discipline 우선순위를 낮췄다. |
| NVDA | watch | 0.0272% | 핵심 AI thesis는 유지되지만 ai_semiconductor_complex warning band와 기존 큰 보유 비중 때문에 add 우선순위를 낮췄다. |
| TSLA | watch | 0.0286% | speculative growth와 약한 review 때문에 floor-size learning order 우선순위에서는 밀렸다. |
| MRK | blocked | n/a | research shortlist에는 있었지만 이번 run 시점 위키 thesis/risk page가 없어 제출 후보로 승격하지 않았다. |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| AVGO | watch | decision_grade_metric_gap | AI semiconductor_complex 경고구간과 급락 반전으로 trim 재점검 대상이지만 decision-grade expected-excess와 replacement margin이 비어 있다. |
| SO | watch | decision_grade_metric_gap | defensive/utilities review 약세와 rate-sensitive 부담은 있지만 per-symbol decision-grade expected-excess 공백이 남아 있다. |
| TSLA | watch | held_quantity_and_metric_gap | 약한 validation review와 speculative growth 성격은 재점검 대상이지만 1주 보유라 whole-share trim 규칙을 만족시키기 어렵고 metric도 비어 있다. |

## 주문 제출과 reconciliation

- Submitted order: `SO` buy 1 @ `90.98` day limit
- Alpaca order id: `18694d74-dc58-44a9-9e81-65c35faeefe6`
- Client order id: `hourly-20260605-0351-buy-so`
- Pre-submit gate summary: paper mode `true`, market open, universe strict `PASS`, MCP strict `PASS`, risk `PASS`, SO quote freshness/spread `PASS`, same-day duplicate/open-order conflict 없음
- 첫 `place_stock_order`: tool-layer `cancelled`. 동일 `client_order_id`에 대해 `get_order_by_client_id` 404, `get_orders(symbol=SO)` 빈 결과, FILL activity 없음, cash unchanged를 확인한 뒤 동일 id로 1회만 재시도했다.
- 두 번째 `place_stock_order`: 성공, initial response `pending_new`, repeated reconciliation 기준 `status=filled`, `filled_avg_price=90.95`
- Reconciliation: `get_order_by_client_id`, `get_account_activities(FILL)`, `get_all_positions`, `get_account_info` 기준 SO 보유수량은 4주가 됐고 open orders는 0건이다. post-submit account snapshot은 cash `30,683.40`, portfolio value `103,530.26`, buying power `255,210.85`, long market value `72,846.86`였다.

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | 62 symbols, SPY/QQQ 포함, final candidates 5개 |
| `check-mcp-coverage.py --strict --json` | PASS | Alpaca core pass, positive research 4개, Alpha `provider_error` gap only |
| `check-risk-policy.py --json` | PASS | SO 1주 regular-session day limit buy 계획 통과 |

## 산출물

- Report: `wiki/current-runs/daily/2026-06-05-0351-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-05-0351-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-05-0351-hourly-autopilot.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-05-0351-hourly-autopilot-post-trade.json`

## 지표 설명

- `sell_candidate_diagnostics`: 보유 포지션 중 trim/exit 재점검이 필요한 상위 후보와 metric gap 사유를 남기는 audit trail이다.
- `provider_error`: 이번 cycle의 Alpha Vantage는 one-call-per-hour throttle 때문에 재호출하지 않고 nonblocking gap으로 남겼다.
- `same-day duplicate discipline`: 같은 ET regular session에서 이미 체결된 동일 symbol/side buy를 추가 validation buy로 재사용하지 않는 규칙이다.
- `portfolio_fit`: hard gate가 아니라 ranking/sizing 입력이다. 이번 run에서는 AI cluster warning이 있는 NVDA와 weak/speculative TSLA보다 SO를 floor-size learning order 우선순위로 선택했다.
