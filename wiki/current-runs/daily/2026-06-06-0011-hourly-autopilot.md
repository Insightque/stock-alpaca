# 2026-06-06-0011-hourly-autopilot scheduled paper autopilot

## 요약

정규장 scheduled hourly autopilot을 실행했다. `.env`의 `ALPACA_PAPER_TRADE=true` 요구를 확인했고, scheduler-owned `0011` stale cleanup/core/research preflight를 우선 사용했다. runtime Alpaca clock `2026-06-05T11:14:05.052341097-04:00` 기준 미국 정규장은 열려 있었고, research preflight는 `sec-edgar`, `fred`, `firecrawl`, `yahoo-finance` 4개 provider가 usable/pass였으며 `alpha-vantage`는 `provider_error` nonblocking gap으로 남았다.

이번 run은 sell/trim 후보를 먼저 평가했지만 `AVGO`, `SO`, `TSLA`는 여전히 decision-grade metric 또는 held-quantity gate에 막혔다. same-day ET session duplicate 규칙 때문에 `PLTR`, `BAC`, `WMT`, `FCX`는 추가 buy 대상에서 제외했고, `QQQ`와 `SPY`는 1주 ask가 validation floor per-order cap 약 `500.86 USD`를 초과했다. `NVDA`와 `INTC`는 ai_semiconductor_complex warning band와 기존 semiconductor 노출 때문에 신규 add 우선순위에서 밀렸고, `COP`/`SLB`는 energy_commodity cluster 재사용 부담이 남았다. 반면 `AAPL`은 research preflight shortlist 포함 기존 mega-cap quality holding으로서 runtime quote `313.02/314.25`, quote age 약 `0.3`분, spread `0.3929%`, review backlog throttle 통과, same-day duplicate/open-order conflict 없음 조건을 충족해 floor-size learning buy 1주 후보로 승격했고, 첫 submit에서 바로 `313.27 USD`에 체결됐다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env`의 `ALPACA_PAPER_TRADE=true` 확인 |
| Market clock pre-submit | PASS | runtime `get_clock` `2026-06-05T11:14:05.052341097-04:00`, regular market open |
| Stale order lifecycle | PASS | scheduler cleanup pass, remaining stale autopilot orders 0건 |
| Alpaca core MCP | PASS | scheduler-owned core preflight hard gate pass + runtime `get_clock/get_account_info/get_orders(status=all, after=2026-06-05T04:00:00Z)/get_stock_latest_quote(...)` |
| Research MCP | PASS tiered | SEC EDGAR/FRED/Firecrawl/Yahoo positive; Alpha Vantage `provider_error` nonblocking gap |
| Universe strict | PASS | metadata universe 62개, SPY/QQQ 포함 |
| Quote/spread | PASS for submitted order | AAPL runtime quote `2026-06-05T15:14:48.864617637Z`, spread `0.3929%` |
| Risk plan | PASS | AAPL 1주 buy notional `314.25`, cash/ticker/theme/factor/cluster caps 통과 |
| Final submit path | PASS | `place_stock_order` first attempt accepted, immediate reconciliation confirmed fill |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| AAPL | filled | 0.3929% | existing mega-cap quality holding으로 quote/spread, duplicate/open-order, review backlog, validation sizing을 모두 통과했고 1주 validation add가 즉시 체결됐다. |
| PLTR | watch_duplicate_block | 0.0289% | same-day filled buy `2026-06-05T15:07:07.519766Z`가 duplicate symbol/side gate를 발동했다. |
| COP | watch_cluster_reuse | 0.0337% | 5D review는 양호했지만 same-session FCX fill 이후 energy_commodity cluster 재사용보다 AAPL이 더 깨끗했다. |
| NVDA | watch_cluster_warning | 0.0143% | ai_semiconductor_complex warning band와 기존 큰 보유 비중 때문에 신규 add 우선순위를 낮췄다. |
| QQQ | watch_notional_cap | 0.0055% | benchmark fallback은 유효했지만 1주 ask `722.70 USD`가 validation floor per-order cap을 초과했다. |
| SPY | watch_notional_cap | 0.0200% | benchmark fallback은 유효했지만 1주 ask `748.51 USD`가 validation floor per-order cap을 초과했다. |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| AVGO | watch | decision_grade_metric_gap | AI semiconductor_complex 경고구간과 earnings-event drawdown은 보이지만 즉시 trim을 정당화할 decision-grade expected-excess와 replacement margin이 비어 있다. |
| SO | watch | decision_grade_metric_gap | defensive/utilities validation review 약세와 rate-sensitive 부담은 남아 있지만 per-symbol decision-grade expected-excess 공백이 있다. |
| TSLA | watch | held_quantity_and_metric_gap | 약한 validation review와 speculative growth 성격은 재점검 대상이지만 1주 보유라 whole-share trim 규칙을 만족시키기 어렵고 metric도 비어 있다. |

## 주문 제출과 reconciliation

- Submitted order: `AAPL` buy 1 @ `314.25` day limit
- Alpaca order id: `7f76779b-289d-4fcb-ba49-b4e4f0e2f6eb`
- Client order id: `hourly-20260606-0011-buy-aapl`
- Pre-submit gate summary: paper mode `true`, market open, order plan path `wiki/trade-ledger/orders/2026-06-06-0011-hourly-autopilot.json`, universe strict `PASS`, MCP strict `PASS`, risk `PASS`, AAPL quote freshness 약 `0.3`분 및 spread `PASS`, order shape `buy 1 share / limit / day / stock`, duplicate/open-order check `PASS`, source refs는 `0011` stale cleanup/core/research preflight와 policy/review/AAPL artifacts
- `place_stock_order`: 첫 submit에서 바로 accepted 됐고 retry는 필요 없었다.
- Reconciliation: `get_order_by_client_id(hourly-20260606-0011-buy-aapl)`는 `status=filled`, `filled_avg_price=313.27`, `filled_at=2026-06-05T15:19:25.344149286Z`를 반환했다. `get_account_activities(FILL)`도 같은 체결 1건을 확인했고, `get_orders(status=open)`는 0건이었다. `get_all_positions` 기준 AAPL 보유수량은 3주, 평균단가는 `310.93 USD`로 갱신됐다. `get_open_position(AAPL)`는 runtime safety monitor에 의해 cancelled 되었지만 `get_all_positions`와 `get_account_info`가 모두 성공해 post-trade snapshot은 runtime MCP 기준으로 기록했다.
- Account snapshot after fill: portfolio value `100190.83 USD`, cash `29678.99 USD`, buying power `247546.97 USD`, long market value `70511.84 USD`.

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | 62 symbols, SPY/QQQ 포함, final candidates 5개 |
| `check-mcp-coverage.py --strict --json` | PASS | Alpaca core pass, positive research 4개, Alpha `provider_error` gap only |
| `check-risk-policy.py --json` | PASS | AAPL 1주 regular-session day limit buy 계획 통과 |

## 산출물

- Report: `wiki/current-runs/daily/2026-06-06-0011-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-06-0011-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-06-0011-hourly-autopilot.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-06-0011-hourly-autopilot-post-trade.json`

## 지표 설명

- `sell_candidate_diagnostics`: 보유 포지션 중 trim/exit 재점검이 필요한 상위 후보와 metric gap 사유를 남기는 audit trail이다.
- `provider_error`: 이번 cycle의 Alpha Vantage는 scheduler preflight 단계에서 provider_error로 남았고, tiered research gate 하에서는 주문을 막지 않았다.
- `review_backlog_throttle`: pending review 개수에 따라 신규 validation buy 슬롯을 줄이거나 막는 정책인데, 이번 run은 `pending_1d_count=0`이라 buy stop 조건에 닿지 않았다.
- `validation_floor per-order cap`: floor-size learning buy라도 `paper_validation_execution.validation_order_sizing`의 per-order notional cap은 유지되므로 `QQQ/SPY` 1주 fallback은 이번 cycle에서 예산 초과로 남겼다.
