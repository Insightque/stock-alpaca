# 2026-06-12-0131-hourly-autopilot

## 요약

`0131` scheduled hourly-autopilot은 scheduler-owned stale cleanup/core/research preflight를 source-of-record로 사용했다. 이번 cycle은 preflight clock `2026-06-11T12:31:11.513259585-04:00`, account `ACTIVE`, positions `33`, open orders `0`, fresh IEX quote rows가 모두 20분 이내라 Alpaca core hard gate를 그대로 PASS 처리했다. Research tiered gate도 `SEC EDGAR/FRED/Firecrawl/Yahoo Finance` pass, `Alpha Vantage`는 one-call-per-hour throttle에 따른 `provider_error` gap only로 유지돼 strict submit threshold `3` confirmations를 충족했다.

sell-first 재평가에서는 `AVGO`가 scheduler-owned IEX quote `377.99/379.20`로 spread `0.3196%`를 보여 policy cap `0.50%` 이내였지만, 같은 거래일 regular-session trim fill 1건이 duplicate sell discipline을 유지해 executable trim으로 승격되지 못했다. `RGTI`는 spread `0.0503%`로 정상 범위였지만 same-day after-hours trim fills 두 건이 duplicate sell discipline을 유지했다. `SO`는 이번 cycle에서 quote `94.21/94.23`, spread `0.0212%`로 정상 범위지만 trim decision-grade expected-excess/replacement margin metric gap이 여전히 남아 첫 executable sell로 전환되지 못했다.

buy fallback은 여전히 hard-block이다. `review_backlog_pending_1d_count=14`가 YAML `stop_new_buys_at_pending_1d=12`를 초과해 신규 validation buy slot이 `0`으로 닫혔다. `SPY/QQQ`는 1주 ask가 validation floor per-order cap 약 `490.38 USD`를 넘고, `WMT`는 quote `120.85/120.90` spread `0.0414%`, `NEE`는 quote `84.99/85.01` spread `0.0235%`로 모두 executable quote/cap 조건은 충족했지만 buy-side hard gate인 review backlog throttle이 열리지 않았다. 따라서 이번 cycle은 exact blocker를 남긴 채 `orders: []` no-submit으로 종료한다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env`와 workflow policy 기준 `ALPACA_PAPER_TRADE=true` |
| Market clock | PASS | scheduler-owned Alpaca clock `2026-06-11T12:31:11.513259585-04:00`, regular market open |
| Stale order lifecycle | PASS | stale cleanup artifact와 core preflight open order row 모두 open orders `0`건 |
| Alpaca core MCP | PASS | scheduler core preflight hard gate `pass`, quote row age 약 0.0분 |
| Research MCP | PASS tiered | SEC EDGAR/FRED/Firecrawl/Yahoo positive, Alpha는 one-call-per-hour throttle `provider_error` gap only |
| Universe strict | PASS | broad metadata universe `62`개, SPY/QQQ 포함 |
| Review backlog throttle | BUY BLOCK | `pending_1d_count=14`가 stop threshold `12` 초과, sell/trim에는 비적용 |
| Quote/spread | MIXED PASS | `AVGO`/`RGTI`/`SO`/`WMT`/`NEE`/`SPY`/`QQQ` 모두 spread cap 이내 |
| Risk plan | PASS | `check-risk-policy.py --json` 기준 현재 포지션 포함, orders `0` 허용 |
| Final submit path | BLOCK | sell path는 `duplicate_symbol_side_same_day`, `sell_metric_gap`; buy path는 `review_backlog_throttle`, `validation_floor_per_order_cap` |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| AVGO | blocked_duplicate_same_day | 0.3196% | ai_semiconductor warning-band trim rationale는 유지되지만 same-day regular-session trim fill 1건이 추가 trim을 막는다 |
| RGTI | blocked_duplicate_same_day | 0.0503% | speculative loss-control trim trigger는 active지만 same-day sell fills 두 건이 duplicate discipline을 유지한다 |
| SO | blocked_metric_gap_only | 0.0212% | spread는 정상 범위지만 trim decision-grade metric gap이 남는다 |
| WMT | blocked_review_backlog_only | 0.0414% | 1주 ask `120.90 USD`와 spread는 floor-size add 요건을 통과했지만 review backlog throttle이 신규 buy를 막는다 |
| SPY | blocked_floor_cap_and_review_backlog | 0.0041% | 1주 ask `727.95 USD`가 validation floor per-order cap 약 `490.38 USD`를 초과 |
| QQQ | blocked_floor_cap_and_review_backlog | 0.0570% | 1주 ask `701.82 USD`가 validation floor per-order cap 약 `490.38 USD`를 초과 |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| AVGO | watch | duplicate_symbol_side_same_day | spread는 정상화됐지만 이번 cycle의 첫 hard blocker는 same-day duplicate sell discipline이다 |
| RGTI | watch | duplicate_symbol_side_same_day | speculative de-risking rationale는 유효하지만 same-day fill 2건이 추가 trim을 막음 |
| SO | watch | sell_metric_gap | spread는 정상 범위지만 trim metric gap이 남아 이번 cycle도 executable trim으로 승격되지 못함 |

## 주문/체결

- Planned orders: 0
- Submitted orders: 0
- `place_stock_order` 호출: 없음
- Pre-submit gate summary: 어떤 주문도 최종 hard gate를 통과하지 못해 작성/호출 대상이 없었다. paper mode `PASS`, market clock `2026-06-11T12:31:11.513259585-04:00`, order plan `wiki/trade-ledger/orders/2026-06-12-0131-hourly-autopilot.json`, universe strict `PASS`, MCP strict `PASS`, risk validator `PASS`, quote freshness `PASS`, spread `PASS`, order shape는 whole-share/day-limit stock-or-ETF only로 유지됐다. duplicate/open-order check는 `AVGO` sell과 `RGTI` sell에서 same-day discipline이 걸렸고, source refs는 scheduler-owned `0131` stale/core/research preflight와 ticker notes였다.
- Post-trade reconciliation: submit attempt는 없었지만 same-day fills가 있어 scheduler-owned Alpaca core preflight account/positions/open-orders/fill ledger를 다시 기록했다. account `ACTIVE`, positions `33`, open orders `0`, cash `31,285.06 USD`, portfolio value `98,075.80 USD`, long market value `66,790.74 USD`다.

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | 62 symbols, SPY/QQQ 포함, final candidates 6개 |
| `check-mcp-coverage.py --strict --json` | PASS | Alpaca core pass, positive research 4개, Alpha `provider_error` gap only |
| `check-risk-policy.py --json` | PASS | 주문 0건, 현재 포지션 포함 |

## 산출물

- Report: `wiki/current-runs/daily/2026-06-12-0131-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-12-0131-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-12-0131-hourly-autopilot.json`
- Runtime gate evaluation: `wiki/evidence-store/sources/2026-06-12-0131-hourly-autopilot-runtime-gate-evaluation.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-12-0131-hourly-autopilot-post-trade.json`

## 지표 설명

- `review_backlog_pending_1d_count`: validation buy 1D review backlog count다. 이번 cycle에서는 `14`라 YAML stop threshold `12`를 넘어 신규 buy가 차단됐다.
- `sell_candidate_diagnostics`: 실행하지 않은 trim 후보도 why-not evidence를 남겨 후속 analyst review와 policy learning에 사용한다.
- `validation_floor_per_order_cap`: `confidence_tiers.validation_floor.max_notional_pct=0.005`에 따라 계좌 가치의 0.5%를 넘는 1주 benchmark fallback 매수는 막힌다. 이번 cycle 기준 약 `490.38 USD`다.
- `provider_error`: 이번 run의 Alpha Vantage는 one-call-per-hour throttle을 지키기 위해 재호출하지 않았고 `provider_error` gap으로 기록됐다. 나머지 4개 research confirmations가 유지돼 strict MCP gate는 통과했다.
