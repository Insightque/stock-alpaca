# 2026-06-11-2231-hourly-autopilot

## 요약

`2231` scheduled hourly-autopilot은 scheduler-owned stale cleanup/core/research preflight를 source-of-record로 사용했고, submit boundary에서는 registered Alpaca MCP `get_clock/get_account_info/get_orders(status=open)/get_all_positions/get_account_activities/get_stock_latest_quote/get_stock_snapshot/get_asset`만 짧게 재호출했다. paper mode, market open, core MCP, research tiered MCP, universe strict, stale-order lifecycle는 모두 PASS였다.

sell-first 재평가에서는 `AVGO`가 live IEX quote `355.00/379.54`로 spread `6.4666%`를 보여 즉시 spread hard gate에 막혔고, `RGTI`는 same-day after-hours trim fills 두 건이 남아 duplicate sell discipline이 추가 trim을 막았다. `SO`는 live quote `94.51/94.70`, spread `0.2006%`로 quote gate는 통과했지만 반복된 weak validation review 이후 trim decision-grade expected-excess/replacement margin metric gap이 계속돼 executable trim으로 승격되지 못했다.

buy fallback은 정책상 이번 cycle에서 차단된다. `review_backlog_pending_1d_count=14`가 YAML `stop_new_buys_at_pending_1d=12`를 초과해 신규 validation buy slot이 0으로 닫혔다. 따라서 `SPY/QQQ` benchmark fallback이나 `MSFT` existing holding add는 최종 submit 분기까지 갈 수 없었고, 이번 cycle은 exact blocker를 남긴 채 `orders: []` no-submit으로 종료한다.

연구 MCP는 tiered PASS를 유지했다. scheduler research preflight 기준 `SEC EDGAR/FRED/Firecrawl/Yahoo Finance`는 pass, `Alpha Vantage`는 `empty_response` gap만 남아 최소 confirmation 수 `3` 이상을 충족했다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env`와 workflow policy 기준 `ALPACA_PAPER_TRADE=true` |
| Market clock | PASS | live Alpaca clock `2026-06-11T09:35:25.257724947-04:00`, regular market open |
| Stale order lifecycle | PASS | stale cleanup artifact와 live `get_orders(status=open)` 모두 open orders `0`건 |
| Alpaca core MCP | PASS | scheduler core preflight hard gate `pass`, live clock/account/positions/open-orders/fills 교차 확인 |
| Research MCP | PASS tiered | SEC EDGAR/FRED/Firecrawl/Yahoo positive, Alpha `empty_response` gap only |
| Universe strict | PASS | broad metadata universe `62`개, SPY/QQQ 포함 |
| Review backlog throttle | BUY BLOCK | `pending_1d_count=14`가 stop threshold `12` 초과, sell/trim에는 비적용 |
| Quote/spread | MIXED PASS | `SO`/`SPY`/`QQQ`는 cap 이내, `AVGO`/`MSFT`/`UNH`는 live spread fail |
| Risk plan | PASS | `check-risk-policy.py --json` 기준 현재 포지션 포함, orders `0` 허용 |
| Final submit path | BLOCK | sell path는 `spread_within_policy`, `duplicate_symbol_side_same_day`, `sell_metric_gap`; buy path는 `review_backlog_throttle` |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| AVGO | blocked_spread_fail | 6.4666% | ai_semiconductor warning-band trim rationale는 유지되지만 live spread가 policy cap `0.50%`를 크게 초과한다 |
| RGTI | blocked_duplicate_same_day | 0.1021% | speculative loss-control trim trigger는 active지만 same-day after-hours sell fills가 이미 있다 |
| SO | blocked_metric_gap | 0.2006% | quote/spread는 통과했지만 trim decision-grade expected-excess/replacement margin 공백 지속 |
| MSFT | blocked_same_day_duplicate_and_spread | 2.0837% | same-day buy fill이 남고 live spread도 cap을 초과한다 |
| SPY | blocked_floor_cap | 0.0083% | 1주 ask `726.98 USD`가 validation floor per-order cap 약 `489.70 USD`를 초과 |
| QQQ | blocked_floor_cap | 0.0759% | 1주 ask `697.98 USD`가 validation floor per-order cap 약 `489.70 USD`를 초과 |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| AVGO | watch | spread_within_policy | active trim trigger는 유지되지만 live spread hard gate가 먼저 닫혔다 |
| RGTI | watch | duplicate_symbol_side_same_day | speculative de-risking rationale는 유효하지만 same-day fill 2건이 추가 trim을 막는다 |
| SO | watch | sell_metric_gap | quote/spread는 통과했지만 trim decision-grade metric이 비어 있다 |

## 주문/체결

- Planned orders: 0
- Submitted orders: 0
- `place_stock_order` 호출: 없음
- Pre-submit gate summary: 어떤 주문도 최종 hard gate를 통과하지 못해 작성/호출 대상이 없었다. sell path는 `AVGO spread_within_policy`, `RGTI duplicate_symbol_side_same_day`, `SO sell_metric_gap`에 막혔고 buy path는 `review_backlog_throttle`에 막혔다.
- Post-trade reconciliation: submit attempt가 없어 추가 reconciliation은 수행하지 않았다. live Alpaca MCP 기준 account `ACTIVE`, positions `33`, open orders `0`, cash `30,904.63 USD`, portfolio value `97,940.37 USD`, long market value `67,035.74 USD`다.

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | 62 symbols, SPY/QQQ 포함, final candidates 3개 |
| `check-mcp-coverage.py --strict --json` | PASS | Alpaca core pass, positive research 4개, Alpha empty-response gap only |
| `check-risk-policy.py --json` | PASS | 주문 0건, 현재 포지션 포함 |

## 산출물

- Report: `wiki/current-runs/daily/2026-06-11-2231-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-11-2231-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-11-2231-hourly-autopilot.json`
- Runtime gate evaluation: `wiki/evidence-store/sources/2026-06-11-2231-hourly-autopilot-runtime-gate-evaluation.json`

## 지표 설명

- `review_backlog_pending_1d_count`: validation buy 1D review backlog count다. 이번 cycle에서는 `14`라 YAML stop threshold `12`를 넘어 신규 buy가 차단됐다.
- `sell_candidate_diagnostics`: 실행하지 않은 trim 후보도 why-not evidence를 남겨 후속 analyst review와 policy learning에 사용한다.
- `validation_floor_per_order_cap`: `confidence_tiers.validation_floor.max_notional_pct=0.005`에 따라 계좌 가치의 0.5%를 넘는 1주 benchmark fallback 매수는 막힌다.
- `sell_metric_gap`: quote/spread와 held quantity는 통과해도 trim justification용 decision-grade expected-excess/replacement margin evidence가 비어 있으면 submit하지 않는다는 뜻이다.
