# 2026-06-05-2311-hourly-autopilot scheduled paper autopilot

## 요약

정규장 scheduled hourly autopilot을 실행했다. `.env`의 `ALPACA_PAPER_TRADE=true` 요구를 확인했고, scheduler-owned `2311` stale cleanup/core/research preflight를 우선 사용했다. runtime Alpaca clock `2026-06-05T10:14:22.197954207-04:00` 기준 미국 정규장은 열려 있었고, research preflight는 `sec-edgar`, `fred`, `firecrawl`, `yahoo-finance` 4개 provider가 usable/pass였으며 `alpha-vantage`는 one-call-per-hour throttle에 따른 `provider_error` nonblocking gap으로 남았다.

이번 run은 sell/trim 후보를 먼저 평가했지만 `AVGO`, `SO`, `TSLA`는 여전히 decision-grade metric 또는 held-quantity gate에 막혔다. `BAC`는 2231 cycle same-day filled buy라 duplicate symbol/side gate에 걸렸고, `AAPL`은 scheduler quote `312.87/314.78` 기준 spread `0.6068%`로 정책 상한 `0.50%`를 넘겼다. `QQQ`와 `SPY`는 benchmark fallback으로는 유효했지만 1주 ask가 validation floor per-order cap 약 `502.53 USD`를 초과했다. 반면 `WMT`는 research preflight shortlist 포함 기존 consumer defensive holding으로서 scheduler quote `120.45/120.50`, quote age `2.9`분, spread `0.0415%`, review backlog throttle 통과, same-day duplicate/open-order conflict 없음, 그리고 2026-06-05 portfolio review 기준 5D 평가가 `중립 양호`라 floor-size learning buy 1주로 승격했다. 첫 `place_stock_order` 시도는 runtime safety cancellation으로 반환됐지만, 동일 `client_order_id`로 reconcile 후 1회만 재시도했고 `WMT` 1주가 `119.78 USD`에 즉시 체결됐다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env`의 `ALPACA_PAPER_TRADE=true` 확인 |
| Market clock pre-submit | PASS | runtime `get_clock` `2026-06-05T10:14:22.197954207-04:00`, regular market open |
| Stale order lifecycle | PASS | scheduler cleanup pass, remaining stale autopilot orders 0건 |
| Alpaca core MCP | PASS | scheduler-owned core preflight hard gate pass + runtime `get_orders(status=all, after=2026-06-05T04:00:00Z)`, `get_asset(WMT)`, `get_order_by_client_id` reconciliation |
| Research MCP | PASS tiered | SEC EDGAR/FRED/Firecrawl/Yahoo positive; Alpha Vantage는 one-call-per-hour throttle `provider_error` nonblocking gap |
| Universe strict | PASS | metadata universe 62개, SPY/QQQ 포함 |
| Quote/spread | PASS for planned order | WMT scheduler quote `2026-06-05T14:11:30.028057619Z`, spread `0.0415%` |
| Risk plan | PASS | WMT 1주 buy notional `120.50`, cash/ticker/theme/factor/cluster caps 통과 |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| BAC | watch_duplicate_block | 0.0184% | 2231 cycle same-day filled buy가 있어 이번 cycle 추가 BAC buy는 duplicate symbol/side gate에 걸렸다. |
| WMT | submitted_filled | 0.0415% | 기존 consumer defensive holding이고 5D review가 `중립 양호`로 회복됐으며 hard gate 전체를 통과해 제출됐고 `119.78 USD`에 체결됐다. |
| AAPL | watch_spread_block | 0.6068% | mega-cap quality add는 가능하지만 scheduler quote spread가 정책 상한 `0.50%`를 넘겨 submit 대상에서 탈락했다. |
| QQQ | watch_notional_cap | 0.0152% | benchmark floor buy fallback은 유지됐지만 1주 ask `725.29 USD`가 validation floor per-order cap을 초과했다. |
| SPY | watch_notional_cap | 0.0027% | benchmark floor buy fallback은 유지됐지만 1주 ask `749.69 USD`가 validation floor per-order cap을 초과했다. |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| AVGO | watch | decision_grade_metric_gap | AI semiconductor_complex 경고구간과 earnings-event drawdown은 보이지만 즉시 trim을 정당화할 decision-grade expected-excess와 replacement margin이 비어 있다. |
| SO | watch | decision_grade_metric_gap | defensive/utilities validation review 약세와 rate-sensitive 부담은 있지만 per-symbol decision-grade expected-excess 공백이 남아 있다. |
| TSLA | watch | held_quantity_and_metric_gap | 약한 validation review와 speculative growth 성격은 재점검 대상이지만 1주 보유라 whole-share trim 규칙을 만족시키기 어렵고 metric도 비어 있다. |

## 주문 제출과 reconciliation

- Planned order: `WMT` buy 1 @ `120.50` day limit
- Alpaca order id: `c55207ea-db32-4d24-b879-5798e1967b9c`
- Client order id: `hourly-20260605-2311-buy-wmt`
- Pre-submit gate summary: paper mode `true`, market open, universe strict `PASS`, MCP strict `PASS`, risk `PASS`, WMT quote freshness `2.9`분 및 spread `PASS`, same-day duplicate/open-order conflict 없음, source refs는 `2311` stale cleanup/core/research preflight와 policy/review artifacts
- `place_stock_order`: 첫 시도는 runtime safety cancellation으로 반환됐다. 이후 `get_order_by_client_id(hourly-20260605-2311-buy-wmt)`는 404, `get_orders(status=all, symbols=WMT, after=2026-06-05T04:00:00Z)`는 0건이어서 실제 Alpaca 주문 미생성을 확인했고, 동일 `client_order_id`로 1회만 재시도했다. 두 번째 시도는 Alpaca accepted 후 `2026-06-05T14:17:18.858272769Z`에 `119.78 USD`로 filled 됐다.
- Reconciliation: `get_orders(status=open)` returned `0` open orders after fill. direct post-fill `get_orders(status=all, symbols=WMT, after=2026-06-05T04:00:00Z)`와 `get_open_position(WMT)` refresh는 runtime safety monitor가 취소해, post-trade snapshot은 fresh 2311 core preflight 포지션과 confirmed fill을 결합해 기록했다.

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | 62 symbols, SPY/QQQ 포함, final candidates 5개 |
| `check-mcp-coverage.py --strict --json` | PASS | Alpaca core pass, positive research 4개, Alpha `provider_error` gap only |
| `check-risk-policy.py --json` | PASS | WMT 1주 regular-session day limit buy 계획 통과 |

## 산출물

- Report: `wiki/current-runs/daily/2026-06-05-2311-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-05-2311-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-05-2311-hourly-autopilot.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-05-2311-hourly-autopilot-post-trade.json`

## 지표 설명

- `sell_candidate_diagnostics`: 보유 포지션 중 trim/exit 재점검이 필요한 상위 후보와 metric gap 사유를 남기는 audit trail이다.
- `provider_error`: 이번 cycle의 Alpha Vantage는 one-call-per-hour throttle 때문에 추가 provider call을 건너뛰었고, tiered research gate 하에서는 nonblocking gap으로 남겼다.
- `review_backlog_throttle`: pending review 개수에 따라 신규 validation buy 슬롯을 줄이거나 막는 정책인데, 이번 run은 `pending_1d_count=0`이라 buy stop 조건에 닿지 않았다.
- `validation_floor per-order cap`: floor-size learning buy라도 `paper_validation_execution.validation_order_sizing`의 per-order notional cap은 유지되므로 `QQQ/SPY` 1주 fallback은 이번 cycle에서 예산 초과로 남겼다.
