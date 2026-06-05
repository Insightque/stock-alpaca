# 2026-06-05-2351-hourly-autopilot scheduled paper autopilot

## 요약

정규장 scheduled hourly autopilot을 실행했다. `.env`의 `ALPACA_PAPER_TRADE=true` 요구를 확인했고, scheduler-owned `2351` stale cleanup/core/research preflight를 우선 사용했다. runtime Alpaca clock `2026-06-05T10:55:18.15841437-04:00` 기준 미국 정규장은 열려 있었고, research preflight는 `sec-edgar`, `fred`, `firecrawl`, `yahoo-finance` 4개 provider가 usable/pass였으며 `alpha-vantage`는 `empty_response` nonblocking gap으로 남았다.

이번 run은 sell/trim 후보를 먼저 평가했지만 `AVGO`, `SO`, `TSLA`는 여전히 decision-grade metric 또는 held-quantity gate에 막혔다. same-day ET session duplicate 규칙 때문에 `BAC`, `WMT`, `FCX`는 추가 buy 대상에서 제외했고, `QQQ`와 `SPY`는 1주 ask가 validation floor per-order cap 약 `503.50 USD`를 초과했다. `NVDA`는 ai_semiconductor_complex warning band와 기존 큰 보유 비중 때문에 신규 add 우선순위에서 밀렸고, `COP`은 직전 `FCX` fill과 같은 energy_commodity cluster 재사용이라 우선순위가 낮아졌다. `AAPL`은 중립 양호였지만 mega-cap tech add보다 bucket observation 가치가 낮았다. 반면 `PLTR`은 research preflight shortlist 포함 기존 low-notional ai_software/speculative_growth holding으로서 runtime quote `138.50/138.56`, quote age 약 `0.1`분, spread `0.0433%`, review backlog throttle 통과, same-day duplicate/open-order conflict 없음, 그리고 2026-06-05 portfolio review 기준 5D cohort 양호라는 조건이 겹쳐 floor-size learning buy 1주 후보로 승격했다. 첫 `place_stock_order`는 runtime safety cancellation으로 반환됐지만, 즉시 같은 `client_order_id`로 reconciliation 후 1회만 재시도했고 Alpaca는 `status=new` open order를 생성했다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env`의 `ALPACA_PAPER_TRADE=true` 확인 |
| Market clock pre-submit | PASS | runtime `get_clock` `2026-06-05T10:55:18.15841437-04:00`, regular market open |
| Stale order lifecycle | PASS | scheduler cleanup pass, remaining stale autopilot orders 0건 |
| Alpaca core MCP | PASS | scheduler-owned core preflight hard gate pass + runtime `get_clock/get_orders(status=open)/get_orders(status=all, after=2026-06-05T04:00:00Z)/get_asset(PLTR)/get_stock_latest_quote(PLTR)` |
| Research MCP | PASS tiered | SEC EDGAR/FRED/Firecrawl/Yahoo positive; Alpha Vantage `empty_response` nonblocking gap |
| Universe strict | PASS | metadata universe 62개, SPY/QQQ 포함 |
| Quote/spread | PASS for submitted order | PLTR runtime quote `2026-06-05T14:55:35.110309741Z`, spread `0.0433%` |
| Risk plan | PASS | PLTR 1주 buy notional `138.56`, cash/ticker/theme/factor/cluster caps 통과 |
| Final submit path | PASS | first submit cancelled without Alpaca order creation, single idempotent retry created `status=new` PLTR day-limit buy |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| PLTR | submitted_open | 0.0433% | existing ai_software/speculative_growth holding으로 quote/spread, duplicate/open-order, review backlog, validation sizing을 모두 통과했고 single retry 후 open order가 생성됐다. |
| AAPL | watch_portfolio_rank | 0.0128% | neutral-positive mega-cap add보다 PLTR의 bucket observation value가 더 컸다. |
| COP | watch_cluster_reuse | 0.0253% | 5D review는 양호했지만 직전 FCX fill과 같은 energy_commodity cluster 재사용보다 PLTR이 우선이었다. |
| NVDA | watch_cluster_warning | 0.0142% | ai_semiconductor_complex warning band와 기존 큰 보유 비중 때문에 신규 add 우선순위를 낮췄다. |
| QQQ | watch_notional_cap | 0.0055% | benchmark fallback은 유효했지만 1주 ask `725.62 USD`가 validation floor per-order cap을 초과했다. |
| SPY | watch_notional_cap | 0.0027% | benchmark fallback은 유효했지만 1주 ask `749.75 USD`가 validation floor per-order cap을 초과했다. |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| AVGO | watch | decision_grade_metric_gap | AI semiconductor_complex 경고구간과 earnings-event drawdown은 보이지만 즉시 trim을 정당화할 decision-grade expected-excess와 replacement margin이 비어 있다. |
| SO | watch | decision_grade_metric_gap | defensive/utilities validation review 약세와 rate-sensitive 부담은 남아 있지만 per-symbol decision-grade expected-excess 공백이 있다. |
| TSLA | watch | held_quantity_and_metric_gap | 약한 validation review와 speculative growth 성격은 재점검 대상이지만 1주 보유라 whole-share trim 규칙을 만족시키기 어렵고 metric도 비어 있다. |

## 주문 제출과 reconciliation

- Submitted order: `PLTR` buy 1 @ `138.56` day limit
- Alpaca order id: `a89c2fdb-979b-42e1-a5ff-050916aa6257`
- Client order id: `hourly-20260605-2351-buy-pltr`
- Pre-submit gate summary: paper mode `true`, market open, order plan path `wiki/trade-ledger/orders/2026-06-05-2351-hourly-autopilot.json`, universe strict `PASS`, MCP strict `PASS`, risk `PASS`, PLTR quote freshness 약 `0.1`분 및 spread `PASS`, order shape `buy 1 share / limit / day / stock`, duplicate/open-order check `PASS`, source refs는 `2351` stale cleanup/core/research preflight와 policy/review/ticker artifacts
- `place_stock_order`: 첫 시도는 runtime safety cancellation으로 반환됐다. 이후 `get_order_by_client_id(hourly-20260605-2351-buy-pltr)`는 404, symbol-specific same-day `get_orders`는 0건, `get_orders(status=open, symbols=PLTR)`도 0건이어서 실제 Alpaca 주문 미생성을 확인했고, 동일 `client_order_id`로 1회만 재시도했다. 두 번째 시도는 accepted 됐고 reconciliation 기준 `status=new`, `filled_qty=0` open order다.
- Reconciliation: `get_order_by_client_id`와 `get_orders(status=open)`는 동일 PLTR order 1건을 `status=new`로 반환했다. `get_account_activities(FILL)`는 빈 결과였고 `get_all_positions` 기준 PLTR 보유수량은 아직 2주로 유지됐다. direct post-submit `get_orders(status=all, symbols=PLTR, after=2026-06-05T04:00:00Z)`와 `get_account_info`는 runtime safety monitor가 취소해 account snapshot은 pre-submit runtime `get_account_info` 값인 portfolio value `100670.12`, cash `30130.79`, buying power `249228.27`, long market value `70539.33`을 last confirmed state로 유지했다.

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | 62 symbols, SPY/QQQ 포함, final candidates 6개 |
| `check-mcp-coverage.py --strict --json` | PASS | Alpaca core pass, positive research 4개, Alpha `empty_response` gap only |
| `check-risk-policy.py --json` | PASS | PLTR 1주 regular-session day limit buy 계획 통과 |

## 산출물

- Report: `wiki/current-runs/daily/2026-06-05-2351-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-05-2351-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-05-2351-hourly-autopilot.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-05-2351-hourly-autopilot-post-trade.json`

## 지표 설명

- `sell_candidate_diagnostics`: 보유 포지션 중 trim/exit 재점검이 필요한 상위 후보와 metric gap 사유를 남기는 audit trail이다.
- `empty_response`: 이번 cycle의 Alpha Vantage는 scheduler preflight 단계에서 비어 있는 provider 결과로 남았고, tiered research gate 하에서는 주문을 막지 않았다.
- `review_backlog_throttle`: pending review 개수에 따라 신규 validation buy 슬롯을 줄이거나 막는 정책인데, 이번 run은 `pending_1d_count=0`이라 buy stop 조건에 닿지 않았다.
- `validation_floor per-order cap`: floor-size learning buy라도 `paper_validation_execution.validation_order_sizing`의 per-order notional cap은 유지되므로 `QQQ/SPY` 1주 fallback은 이번 cycle에서 예산 초과로 남겼다.
