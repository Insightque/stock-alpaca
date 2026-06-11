# 2026-06-11-2351-hourly-autopilot

## 요약

`2351` scheduled hourly-autopilot은 scheduler-owned stale cleanup/core/research preflight를 source-of-record로 사용했고, submit boundary에서는 registered Alpaca MCP `get_clock/get_account_info/get_orders(status=open)/get_all_positions/get_account_activities(activity_types=FILL, after=2026-06-11T00:00:00Z)/get_asset/get_stock_latest_quote/get_stock_snapshot`만 짧게 재호출했다. paper mode, market open, core MCP, research tiered MCP, universe strict, stale-order lifecycle는 모두 PASS였다.

sell-first 재평가에서는 `AVGO`가 live IEX quote `375.49/376.32`로 spread `0.2206%`를 보여 quote hard gate는 통과했지만, `2251` cycle same-day filled trim 1건이 남아 duplicate sell discipline이 추가 trim을 막았다. `RGTI`는 same-day after-hours trim fills 두 건이 남아 duplicate sell discipline이 추가 trim을 막았고, `SO`는 live quote `94.65/97.50`로 spread `2.9231%`가 policy cap `0.50%`를 크게 초과한 데다 trim decision-grade expected-excess/replacement margin metric gap도 계속돼 executable trim으로 승격되지 못했다.

buy fallback은 정책상 이번 cycle에서도 차단된다. `review_backlog_pending_1d_count=14`가 YAML `stop_new_buys_at_pending_1d=12`를 초과해 신규 validation buy slot이 0으로 닫혔다. 따라서 `SPY/QQQ` benchmark fallback이나 `MSFT` existing holding add는 최종 submit 분기까지 갈 수 없었고, 이번 cycle은 exact blocker를 남긴 채 `orders: []` no-submit으로 종료한다.

연구 MCP는 tiered PASS를 유지했다. scheduler research preflight 기준 `SEC EDGAR/FRED/Firecrawl/Yahoo Finance`는 pass, `Alpha Vantage`는 `NEWS_SENTIMENT` 후보 뉴스 0건으로 `empty_response` gap만 남아 최소 confirmation 수 `3` 이상을 충족했다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env`와 workflow policy 기준 `ALPACA_PAPER_TRADE=true` |
| Market clock | PASS | live Alpaca clock `2026-06-11T10:53:26.9765081-04:00`, regular market open |
| Stale order lifecycle | PASS | stale cleanup artifact와 live `get_orders(status=open)` 모두 open orders `0`건 |
| Alpaca core MCP | PASS | scheduler core preflight hard gate `pass`, live clock/account/positions/open-orders/fills 교차 확인 |
| Research MCP | PASS tiered | SEC EDGAR/FRED/Firecrawl/Yahoo positive, Alpha `empty_response` gap only |
| Universe strict | PASS | broad metadata universe `62`개, SPY/QQQ 포함 |
| Review backlog throttle | BUY BLOCK | `pending_1d_count=14`가 stop threshold `12` 초과, sell/trim에는 비적용 |
| Quote/spread | MIXED PASS | `AVGO`/`RGTI`/`SPY`/`QQQ`/`MSFT`는 cap 이내, `SO`는 live spread fail |
| Risk plan | PASS | `check-risk-policy.py --json` 기준 현재 포지션 포함, orders `0` 허용 |
| Final submit path | BLOCK | sell path는 `duplicate_symbol_side_same_day`, `spread_within_policy`, `sell_metric_gap`; buy path는 `review_backlog_throttle` |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| AVGO | blocked_duplicate_same_day | 0.2206% | ai_semiconductor warning-band trim rationale는 유지되지만 `2251` cycle same-day trim fill이 남아 추가 sell이 차단된다 |
| RGTI | blocked_duplicate_same_day | 0.0501% | speculative loss-control trim trigger는 active지만 same-day sell fills 두 건이 duplicate discipline을 유지한다 |
| SO | blocked_spread_and_metric_gap | 2.9231% | live spread가 policy cap `0.50%`를 크게 초과하고 trim decision-grade metric gap도 남는다 |
| MSFT | blocked_same_day_duplicate_and_review_backlog | 0.1673% | spread는 정상 범위지만 same-day buy discipline과 review backlog throttle 때문에 신규 add가 차단된다 |
| SPY | blocked_floor_cap_and_review_backlog | 0.0055% | 1주 ask `727.51 USD`가 validation floor per-order cap 약 `490.99 USD`를 초과 |
| QQQ | blocked_floor_cap_and_review_backlog | 0.0300% | 1주 ask `699.74 USD`가 validation floor per-order cap 약 `490.99 USD`를 초과 |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| AVGO | watch | duplicate_symbol_side_same_day | spread는 정상 범위지만 same-day trim fill이 남아 추가 trim 불가 |
| RGTI | watch | duplicate_symbol_side_same_day | speculative de-risking rationale는 유효하지만 same-day fill 2건이 추가 trim을 막음 |
| SO | watch | spread_within_policy | trim metric gap이 남아 있는 상태에서 live spread까지 `2.9231%`로 악화됐다 |

## 주문/체결

- Planned orders: 0
- Submitted orders: 0
- `place_stock_order` 호출: 없음
- Pre-submit gate summary: 어떤 주문도 최종 hard gate를 통과하지 못해 작성/호출 대상이 없었다. sell path는 `AVGO duplicate_symbol_side_same_day`, `RGTI duplicate_symbol_side_same_day`, `SO spread_within_policy + sell_metric_gap`에 막혔고 buy path는 `review_backlog_throttle`에 막혔다.
- Post-trade reconciliation: submit attempt는 없었지만 same-day fills가 있어 account/positions/open-orders/fill ledger를 live Alpaca MCP로 다시 확인했다. account `ACTIVE`, positions `33`, open orders `0`, cash `31,285.06 USD`, portfolio value `98,198.60 USD`, long market value `66,913.54 USD`다.

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | 62 symbols, SPY/QQQ 포함, final candidates 3개 |
| `check-mcp-coverage.py --strict --json` | PASS | Alpaca core pass, positive research 4개, Alpha empty-response gap only |
| `check-risk-policy.py --json` | PASS | 주문 0건, 현재 포지션 포함 |

## 산출물

- Report: `wiki/current-runs/daily/2026-06-11-2351-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-11-2351-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-11-2351-hourly-autopilot.json`
- Runtime gate evaluation: `wiki/evidence-store/sources/2026-06-11-2351-hourly-autopilot-runtime-gate-evaluation.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-11-2351-hourly-autopilot-post-trade.json`

## 지표 설명

- `review_backlog_pending_1d_count`: validation buy 1D review backlog count다. 이번 cycle에서는 `14`라 YAML stop threshold `12`를 넘어 신규 buy가 차단됐다.
- `sell_candidate_diagnostics`: 실행하지 않은 trim 후보도 why-not evidence를 남겨 후속 analyst review와 policy learning에 사용한다.
- `validation_floor_per_order_cap`: `confidence_tiers.validation_floor.max_notional_pct=0.005`에 따라 계좌 가치의 0.5%를 넘는 1주 benchmark fallback 매수는 막힌다. 이번 cycle 기준 약 `490.99 USD`다.
- `empty_response`: 이번 run의 Alpha Vantage는 `NEWS_SENTIMENT` 후보 뉴스 0건으로 `empty_response` gap을 남겼고, 나머지 4개 research confirmations가 유지돼 strict MCP gate는 통과했다.
