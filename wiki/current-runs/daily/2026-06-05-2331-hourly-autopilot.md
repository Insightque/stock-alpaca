# 2026-06-05-2331-hourly-autopilot scheduled paper autopilot

## 요약

정규장 scheduled hourly autopilot을 실행했다. `.env`의 `ALPACA_PAPER_TRADE=true` 요구를 확인했고, scheduler-owned `2331` stale cleanup/core/research preflight를 우선 사용했다. runtime Alpaca clock `2026-06-05T10:35:59.598753296-04:00` 기준 미국 정규장은 열려 있었고, research preflight는 `sec-edgar`, `fred`, `firecrawl`, `yahoo-finance` 4개 provider가 usable/pass였으며 `alpha-vantage`는 `provider_error` nonblocking gap으로 남았다.

이번 run은 sell/trim 후보를 먼저 평가했지만 `AVGO`, `SO`, `TSLA`는 여전히 decision-grade metric 또는 held-quantity gate에 막혔다. `BAC`와 `WMT`는 같은 ET regular session same-day filled buy라 duplicate symbol/side gate에 걸렸고, `QQQ`와 `SPY`는 1주 ask가 validation floor per-order cap 약 `502.63 USD`를 초과했다. `NVDA`는 ai_semiconductor_complex warning band와 기존 큰 보유 비중 때문에 신규 add 우선순위에서 밀렸고, `PLTR`은 software/AI momentum은 유지됐지만 `FCX`보다 correlation 분산 기여가 낮았다. 반면 `FCX`는 research preflight shortlist 포함 기존 materials/mining holding으로서 scheduler quote `65.28/65.31`, quote age 약 `4.5`분, spread `0.0460%`, review backlog throttle 통과, same-day duplicate/open-order conflict 없음, 그리고 2026-06-05 portfolio review 기준 기존 materials/copper validation 표본이 유지 가능해 floor-size learning buy 1주로 승격했다. `place_stock_order`는 cancellation 없이 수락됐고 `get_order_by_client_id(hourly-20260605-2331-buy-fcx)` 기준 `2026-06-05T14:39:22.134743752Z`에 `65.15 USD`로 즉시 체결됐다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env`의 `ALPACA_PAPER_TRADE=true` 확인 |
| Market clock pre-submit | PASS | runtime `get_clock` `2026-06-05T10:35:59.598753296-04:00`, regular market open |
| Stale order lifecycle | PASS | scheduler cleanup pass, remaining stale autopilot orders 0건 |
| Alpaca core MCP | PASS | scheduler-owned core preflight hard gate pass + runtime `get_clock/get_orders(status=open)/get_orders(status=all, after=2026-06-05T04:00:00Z)/get_asset(FCX)` |
| Research MCP | PASS tiered | SEC EDGAR/FRED/Firecrawl/Yahoo positive; Alpha Vantage `provider_error` nonblocking gap |
| Universe strict | PASS | metadata universe 62개, SPY/QQQ 포함 |
| Quote/spread | PASS for planned order | FCX scheduler quote `2026-06-05T14:31:28.415840617Z`, spread `0.0460%` |
| Risk plan | PASS | FCX 1주 buy notional `65.31`, cash/ticker/theme/factor/cluster caps 통과 |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| FCX | submitted_filled | 0.0460% | existing materials/mining diversifier로 quote/spread, duplicate/open-order, review backlog, validation sizing을 모두 통과했고 `65.15 USD`에 체결됐다. |
| BAC | watch_duplicate_block | 0.0185% | 2231 cycle same-day filled buy가 있어 이번 cycle 추가 BAC buy는 duplicate symbol/side gate에 걸렸다. |
| WMT | watch_duplicate_block | 0.0415% | 2311 cycle same-day filled buy가 있어 이번 cycle 추가 WMT buy는 duplicate symbol/side gate에 걸렸다. |
| PLTR | watch_portfolio_rank | 0.0361% | software/AI momentum은 유지됐지만 이번 cycle에서는 FCX의 낮은 상관관계와 diversification 기여가 더 컸다. |
| NVDA | watch_cluster_warning | 0.0142% | ai_semiconductor_complex warning band와 기존 큰 보유 비중 때문에 신규 add 우선순위를 낮췄다. |
| QQQ | watch_notional_cap | 0.0069% | benchmark fallback은 유효했지만 1주 ask `725.54 USD`가 validation floor per-order cap을 초과했다. |
| SPY | watch_notional_cap | 0.0040% | benchmark fallback은 유효했지만 1주 ask `749.62 USD`가 validation floor per-order cap을 초과했다. |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| AVGO | watch | decision_grade_metric_gap | AI semiconductor_complex 경고구간과 earnings-event drawdown은 보이지만 즉시 trim을 정당화할 decision-grade expected-excess와 replacement margin이 비어 있다. |
| SO | watch | decision_grade_metric_gap | defensive/utilities validation review 약세와 rate-sensitive 부담은 남아 있지만 per-symbol decision-grade expected-excess 공백이 있다. |
| TSLA | watch | held_quantity_and_metric_gap | 약한 validation review와 speculative growth 성격은 재점검 대상이지만 1주 보유라 whole-share trim 규칙을 만족시키기 어렵고 metric도 비어 있다. |

## 주문 제출과 reconciliation

- Planned order: `FCX` buy 1 @ `65.31` day limit
- Alpaca order id: `c5f66d6e-f506-4d4c-8fa3-bdc1ee3cf885`
- Client order id: `hourly-20260605-2331-buy-fcx`
- Pre-submit gate summary: paper mode `true`, market open, universe strict `PASS`, MCP strict `PASS`, risk `PASS`, FCX quote freshness 약 `4.5`분 및 spread `PASS`, same-day duplicate/open-order conflict 없음, source refs는 `2331` stale cleanup/core/research preflight와 policy/review/ticker artifacts
- `place_stock_order`: 첫 시도에서 cancellation 없이 accepted 됐고, `get_order_by_client_id(hourly-20260605-2331-buy-fcx)` 기준 `2026-06-05T14:39:22.134743752Z`에 `65.15 USD`로 filled 됐다.
- Reconciliation: direct post-fill `get_orders(status=open)`, `get_all_positions`, `get_account_info` refresh는 runtime safety monitor가 취소했다. 따라서 post-trade snapshot은 fresh 2331 core preflight 계좌/포지션과 confirmed FCX fill을 결합해 기록했다. `FCX` 보유수량은 2주에서 3주로 증가했고 평균단가는 `66.20 USD`로 조정했다.

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | 62 symbols, SPY/QQQ 포함, final candidates 5개 |
| `check-mcp-coverage.py --strict --json` | PASS | Alpaca core pass, positive research 4개, Alpha `provider_error` gap only |
| `check-risk-policy.py --json` | PASS | FCX 1주 regular-session day limit buy 계획 통과 |

## 산출물

- Report: `wiki/current-runs/daily/2026-06-05-2331-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-05-2331-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-05-2331-hourly-autopilot.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-05-2331-hourly-autopilot-post-trade.json`

## 지표 설명

- `sell_candidate_diagnostics`: 보유 포지션 중 trim/exit 재점검이 필요한 상위 후보와 metric gap 사유를 남기는 audit trail이다.
- `provider_error`: 이번 cycle의 Alpha Vantage는 scheduler preflight 단계에서 nonblocking provider gap으로 남았고, tiered research gate 하에서는 주문을 막지 않았다.
- `review_backlog_throttle`: pending review 개수에 따라 신규 validation buy 슬롯을 줄이거나 막는 정책인데, 이번 run은 `pending_1d_count=0`이라 buy stop 조건에 닿지 않았다.
- `validation_floor per-order cap`: floor-size learning buy라도 `paper_validation_execution.validation_order_sizing`의 per-order notional cap은 유지되므로 `QQQ/SPY` 1주 fallback은 이번 cycle에서 예산 초과로 남겼다.
