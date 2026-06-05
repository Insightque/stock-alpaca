# 2026-06-06-0051-hourly-autopilot scheduled paper autopilot

## 요약

정규장 scheduled hourly autopilot을 실행했다. `.env`의 `ALPACA_PAPER_TRADE=true` 요구를 확인했고, scheduler-owned `0051` stale cleanup/core/research preflight를 우선 사용했다. core preflight hard gate는 `pass`, stale cleanup은 open order 0건, research preflight는 `sec-edgar`, `fred`, `firecrawl`, `yahoo-finance` 4개 provider가 usable/pass였으며 `alpha-vantage`는 `empty_response` nonblocking gap으로 남았다.

이번 run은 sell/trim 후보를 먼저 평가했지만 `AVGO`, `SO`, `TSLA`는 여전히 decision-grade metric 또는 held-quantity gate에 막혔다. same-day ET session duplicate 규칙 때문에 `BAC`, `WMT`, `FCX`, `PLTR`, `AAPL`, `V`는 추가 buy 대상에서 제외했고, `QQQ`와 `SPY`는 1주 ask가 validation per-order cap 약 `499.69 USD`를 초과했다. `SO`, `NEE`, `NKE`, `AMZN`, `INTC`, `TSLA`는 최근 review 약세나 cluster/speculative 부담으로 `NVDA`보다 replacement rank가 낮았다. 반면 `NVDA`는 research preflight shortlist 포함 기존 AI core holding으로서 preflight quote `208.76/208.80`, quote age 약 `2.6`분, spread `0.0192%`, asset active/tradable, same-day duplicate/open-order conflict 없음, review backlog throttle 통과 조건을 충족해 1주 floor-size validation buy 후보로 승격했다. ai_semiconductor_complex warning band를 고려해 size는 1주로 제한했다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env`의 `ALPACA_PAPER_TRADE=true` 확인 |
| Market clock pre-submit | PASS | runtime `get_clock` timestamp `2026-06-05T11:54:10.423037555-04:00`, regular market open |
| Stale order lifecycle | PASS | scheduler cleanup pass, remaining stale autopilot orders 0건 |
| Alpaca core MCP | PASS | scheduler-owned core preflight hard gate pass + runtime `get_orders(status=open)`, `get_orders(status=all, after=2026-06-05T04:00:00Z)`, `get_account_activities(FILL)` reconciliation |
| Research MCP | PASS tiered | SEC EDGAR/FRED/Firecrawl/Yahoo positive; Alpha Vantage `empty_response` nonblocking gap |
| Universe strict | PASS | metadata universe 62개, SPY/QQQ 포함 |
| Quote/spread | PASS for planned order | NVDA preflight quote `2026-06-05T15:51:32.772992847Z`, spread `0.0192%` |
| Risk plan | PASS | `check-risk-policy.py --json` PASS |
| Final submit path | PASS | `place_stock_order` accepted, immediate reconciliation에서 `status=new` open order 확인 |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| NVDA | open_order_new | 0.0192% | existing AI core holding으로 5D review 양호, same-day duplicate/open-order conflict 없고 1주 floor-size로 concentration discipline을 유지할 수 있다. `15:59:35Z` submit 이후 현재 `status=new` open order다. |
| SO | watch_review_weak | 0.0216% | macro row는 있지만 utilities validation cohort가 반복적으로 약해 NVDA보다 replacement rank가 낮다. |
| NEE | watch_review_weak | 0.0234% | utilities diversifier지만 최근 review가 약하고 benchmark 상대우위가 부족하다. |
| NKE | watch_review_weak | 0.0233% | consumer rebound thesis가 5D에서도 약해 우선순위를 낮췄다. |
| AMZN | watch_review_weak | 0.0277% | mega-cap AI/cloud label 대비 최근 validation cohort 성과가 계속 약했다. |
| QQQ | watch_notional_cap | 0.0097% | benchmark fallback은 유효했지만 1주 ask `721.07 USD`가 validation per-order cap을 초과했다. |
| SPY | watch_notional_cap | 0.0040% | benchmark fallback은 유효했지만 1주 ask `746.59 USD`가 validation per-order cap을 초과했다. |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| AVGO | watch | decision_grade_metric_gap | AI semiconductor_complex 경고구간과 earnings-event drawdown은 보이지만 즉시 trim을 정당화할 decision-grade expected-excess와 replacement margin이 비어 있다. |
| SO | watch | decision_grade_metric_gap | defensive/utilities validation review 약세와 rate-sensitive 부담은 남아 있지만 per-symbol decision-grade expected-excess 공백이 있다. |
| TSLA | watch | held_quantity_and_metric_gap | 약한 validation review와 speculative growth 성격은 재점검 대상이지만 1주 보유라 whole-share trim 규칙을 만족시키기 어렵고 metric도 비어 있다. |

## 주문 제출과 reconciliation

- Submitted order: `NVDA` buy 1 @ `208.80` day limit
- Alpaca order id: `93f2530d-3f49-4705-8640-664357426b14`
- Client order id: `hourly-20260606-0051-buy-nvda`
- Pre-submit gate summary: paper mode `true`, market open, order plan path `wiki/trade-ledger/orders/2026-06-06-0051-hourly-autopilot.json`, universe strict `PASS`, MCP strict `PASS`, risk `PASS`, NVDA quote freshness 약 `2.6`분 및 spread `PASS`, order shape `buy 1 share / limit / day / stock`, duplicate/open-order check `PASS`, source refs는 `0051` stale cleanup/core/research preflight와 policy/review/NVDA artifacts
- `place_stock_order`: accepted on first submit, retry 불필요
- Reconciliation: `get_order_by_client_id(hourly-20260606-0051-buy-nvda)`와 `get_orders(status=open, symbols=NVDA)` 기준 현재 `status=new`, `filled_qty=0` open order다. `get_orders(status=all, symbols=NVDA, after=2026-06-05T04:00:00Z)`도 동일 주문 1건만 반환했다. post-submit `get_account_info`와 `get_account_activities(FILL)`는 safety monitor에서 cancelled 되어 last confirmed pre-submit account snapshot과 unchanged positions를 유지 기록했다.

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | 62 symbols, SPY/QQQ 포함, final candidates 5개 |
| `check-mcp-coverage.py --strict --json` | PASS | Alpaca core pass, positive research 4개, Alpha `empty_response` gap only |
| `check-risk-policy.py --json` | PASS | NVDA 1주 regular-session day limit buy 계획 통과 |

## 산출물

- Report: `wiki/current-runs/daily/2026-06-06-0051-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-06-0051-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-06-0051-hourly-autopilot.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-06-0051-hourly-autopilot-post-trade.json`

## 지표 설명

- `sell_candidate_diagnostics`: 보유 포지션 중 trim/exit 재점검이 필요한 상위 후보와 metric gap 사유를 남기는 audit trail이다.
- `empty_response`: 이번 cycle의 Alpha Vantage는 shortlist 대상에 대해 usable candidate news item을 반환하지 않았고, tiered research gate 하에서는 nonblocking gap으로 기록됐다.
- `review_backlog_throttle`: pending review 개수에 따라 신규 validation buy 슬롯을 줄이거나 막는 정책인데, 이번 run은 `pending_1d_count=0`이라 buy stop 조건에 닿지 않았다.
- `validation per-order cap`: floor-size learning buy라도 `paper_validation_execution.validation_order_sizing`의 per-order notional cap은 유지되므로 `QQQ/SPY` 1주 fallback은 이번 cycle에서 예산 초과로 남겼다.
