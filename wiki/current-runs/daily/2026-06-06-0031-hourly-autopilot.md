# 2026-06-06-0031-hourly-autopilot scheduled paper autopilot

## 요약

정규장 scheduled hourly autopilot을 실행했다. `.env`의 `ALPACA_PAPER_TRADE=true` 요구를 확인했고, scheduler-owned `0031` stale cleanup/core/research preflight를 우선 사용했다. core preflight hard gate는 `pass`, stale cleanup은 open order 0건, research preflight는 `sec-edgar`, `fred`, `firecrawl`, `yahoo-finance` 4개 provider가 usable/pass였으며 `alpha-vantage`는 one-call throttle로 `provider_error` nonblocking gap으로 남았다.

이번 run은 sell/trim 후보를 먼저 평가했지만 `AVGO`, `SO`, `TSLA`는 여전히 decision-grade metric 또는 held-quantity gate에 막혔다. same-day ET session duplicate 규칙 때문에 `BAC`, `WMT`, `FCX`, `PLTR`, `AAPL`은 추가 buy 대상에서 제외했고, `QQQ`와 `SPY`는 1주 ask가 validation floor per-order cap 약 `500.28 USD`를 초과했다. `NVDA`는 ai_semiconductor_complex warning band와 기존 큰 보유 비중 때문에 신규 add 우선순위에서 밀렸고, `COP`은 직전 materials/energy 계열 표본 누적 때문에 cluster 재사용 부담이 남았다. `NEE`와 `NKE`는 quote/spread는 양호했지만 최근 review 약세로 `V`보다 replacement rank가 낮았다. 반면 `V`는 research preflight shortlist 포함 기존 payments diversifier holding으로서 preflight quote `322.35/322.41`, quote age 약 `5.6`분, spread `0.0186%`, asset active/tradable, same-day duplicate/open-order conflict 없음, review backlog throttle 통과, 1주 validation floor cap 통과 조건을 모두 충족해 floor-size learning buy 1주 후보로 승격했고, `321.90 USD`에 즉시 체결됐다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env`의 `ALPACA_PAPER_TRADE=true` 확인 |
| Market clock pre-submit | PASS | scheduler core preflight clock `2026-06-05T11:31:11.538155727-04:00`, regular market open |
| Stale order lifecycle | PASS | scheduler cleanup pass, remaining stale autopilot orders 0건 |
| Alpaca core MCP | PASS | scheduler-owned core preflight hard gate pass + runtime `get_orders(status=open)`, `get_orders(status=all, after=2026-06-05T04:00:00Z)` reconciliation |
| Research MCP | PASS tiered | SEC EDGAR/FRED/Firecrawl/Yahoo positive; Alpha Vantage `provider_error` nonblocking gap |
| Universe strict | PASS | metadata universe 62개, SPY/QQQ 포함 |
| Quote/spread | PASS for submitted order | V preflight quote `2026-06-05T15:31:29.795035147Z`, spread `0.0186%` |
| Risk plan | PASS | V 1주 buy notional `322.41`, cash/ticker/theme/factor/cluster caps 통과 |
| Final submit path | PASS | `place_stock_order` accepted 후 immediate reconciliation에서 `filled` 확인 |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| V | filled | 0.0186% | existing payments diversifier holding으로 quote/spread, duplicate/open-order, review backlog, validation sizing을 모두 통과했고 `321.90 USD`에 체결됐다. |
| COP | watch_cluster_reuse | 0.0253% | quote/spread는 양호했지만 직전 energy/materials 계열 표본 누적 뒤 같은 cluster 재사용보다 V의 분산 기여가 더 컸다. |
| NVDA | watch_cluster_warning | 0.0144% | 핵심 AI thesis는 유지되지만 ai_semiconductor_complex warning band와 기존 큰 보유 비중 때문에 신규 add 우선순위를 낮췄다. |
| NEE | watch_review_weak | 0.0117% | utilities diversifier지만 최근 validation review가 약해 V보다 replacement rank가 낮았다. |
| NKE | watch_review_weak | 0.0232% | consumer diversifier지만 최근 review 약세와 낮은 포트폴리오 기여도로 V보다 우선순위가 낮았다. |
| QQQ | watch_notional_cap | 0.0055% | benchmark fallback은 유효했지만 1주 ask `722.80 USD`가 validation floor per-order cap을 초과했다. |
| SPY | watch_notional_cap | 0.0027% | benchmark fallback은 유효했지만 1주 ask `748.40 USD`가 validation floor per-order cap을 초과했다. |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| AVGO | watch | decision_grade_metric_gap | AI semiconductor_complex 경고구간과 earnings-event drawdown은 보이지만 즉시 trim을 정당화할 decision-grade expected-excess와 replacement margin이 비어 있다. |
| SO | watch | decision_grade_metric_gap | defensive/utilities validation review 약세와 rate-sensitive 부담은 남아 있지만 per-symbol decision-grade expected-excess 공백이 있다. |
| TSLA | watch | held_quantity_and_metric_gap | 약한 validation review와 speculative growth 성격은 재점검 대상이지만 1주 보유라 whole-share trim 규칙을 만족시키기 어렵고 metric도 비어 있다. |

## 주문 제출과 reconciliation

- Submitted order: `V` buy 1 @ `322.41` day limit
- Alpaca order id: `5b3210f1-f85c-4b68-b85d-3f8d3c384629`
- Client order id: `hourly-20260606-0031-buy-v`
- Pre-submit gate summary: paper mode `true`, market open, order plan path `wiki/trade-ledger/orders/2026-06-06-0031-hourly-autopilot.json`, universe strict `PASS`, MCP strict `PASS`, risk `PASS`, V quote freshness 약 `5.6`분 및 spread `PASS`, order shape `buy 1 share / limit / day / stock`, duplicate/open-order check `PASS`, source refs는 `0031` stale cleanup/core/research preflight와 policy/review/V artifacts
- `place_stock_order`: 첫 submit에서 바로 accepted 됐고 retry는 필요 없었다.
- Reconciliation: `get_order_by_client_id(hourly-20260606-0031-buy-v)`는 `status=filled`, `filled_avg_price=321.90`, `filled_at=2026-06-05T15:37:28.378344604Z`를 반환했다. `get_orders(status=open, symbols=V)`는 0건, `get_orders(status=all, symbols=V, after=2026-06-05T04:00:00Z)`는 동일 filled order 1건을 반환했다. `get_all_positions` 기준 V 보유수량은 4주, 평균단가는 `325.685 USD`로 갱신됐다. `get_account_activities(FILL)`와 post-submit `get_account_info` refresh는 tool layer에서 cancelled 되었지만, last confirmed pre-submit account snapshot과 confirmed fill, 그리고 current positions 합계를 결합해 post-trade snapshot을 기록했다.
- Account snapshot after fill: inferred portfolio value `100055.85 USD`, inferred cash `29357.09 USD`, long market value `70698.76 USD`, buying power는 last confirmed pre-submit `247108.30 USD`를 유지 기록했다.

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | 62 symbols, SPY/QQQ 포함, final candidates 5개 |
| `check-mcp-coverage.py --strict --json` | PASS | Alpaca core pass, positive research 4개, Alpha `provider_error` gap only |
| `check-risk-policy.py --json` | PASS | V 1주 regular-session day limit buy 계획 통과 |

## 산출물

- Report: `wiki/current-runs/daily/2026-06-06-0031-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-06-0031-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-06-0031-hourly-autopilot.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-06-0031-hourly-autopilot-post-trade.json`

## 지표 설명

- `sell_candidate_diagnostics`: 보유 포지션 중 trim/exit 재점검이 필요한 상위 후보와 metric gap 사유를 남기는 audit trail이다.
- `provider_error`: 이번 cycle의 Alpha Vantage는 scheduler preflight 단계에서 one-call throttle 정책 때문에 provider_error로 남았고, tiered research gate 하에서는 주문을 막지 않았다.
- `review_backlog_throttle`: pending review 개수에 따라 신규 validation buy 슬롯을 줄이거나 막는 정책인데, 이번 run은 `pending_1d_count=0`이라 buy stop 조건에 닿지 않았다.
- `validation_floor per-order cap`: floor-size learning buy라도 `paper_validation_execution.validation_order_sizing`의 per-order notional cap은 유지되므로 `QQQ/SPY` 1주 fallback은 이번 cycle에서 예산 초과로 남겼다.
