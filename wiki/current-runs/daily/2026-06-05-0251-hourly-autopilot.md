# 2026-06-05-0251-hourly-autopilot scheduled paper autopilot

## 요약

정규장 scheduled hourly autopilot을 실행했다. `.env`의 `ALPACA_PAPER_TRADE=true` 요구는 scheduler workflow contract 기준으로 유지했고, scheduler-owned `0251` stale cleanup/core/research preflight를 우선 사용했다. stale cleanup 기준 미체결 autopilot order는 없었고, scheduler Alpaca core preflight는 market/account/positions/open-orders/quotes hard gate를 모두 `pass`로 기록했다. research preflight는 `sec-edgar`, `fred`, `firecrawl`, `yahoo-finance` 4개 provider pass, `alpha-vantage`는 one-call-per-hour throttle에 따른 `provider_error` gap이었다.

이번 run은 `submit` mode였다. sell/trim 후보를 먼저 평가했지만 `AVGO`, `SO`, `TSLA`는 여전히 decision-grade metric 또는 held-quantity gate에 막혔다. `QQQ`, `SPY`, `AAPL`, `COP`, `WMT`, `GOOGL`, `MSFT`는 같은 ET regular session same-day filled buy라 duplicate discipline 때문에 제외했고, `BAC`는 같은 세션 same-side submit/cancel 이력으로 재사용하지 않았다. `NVDA`와 `INTC`는 AI semiconductor_complex warning band와 기존 보유 비중 때문에 신규 add 우선순위에서 밀렸다. `NKE`는 2026-06-04 5D review 약세가 이어졌고 `AMZN`은 mega-cap quality 보조 후보지만 diversification 기여가 약해 `NEE`보다 replacement rank가 낮았다. `NEE`는 research preflight shortlist 포함, 기존 utilities diversifier holding, runtime quote `85.34/85.36`에서 spread `0.0234%`, FRED macro row pass, same-day duplicate/open-order 충돌이 없어 1주 validation buy를 제출했다.

## 게이트

| Gate | 결과 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | `.env`의 `ALPACA_PAPER_TRADE=true` 확인 |
| Market clock | PASS | runtime `get_clock` `2026-06-04T13:56:21.78948551-04:00`, regular market open |
| Stale order lifecycle | PASS | scheduler cleanup 기준 stale candidate/open order 없음, submit 전 runtime `get_orders(status=open)` 0건 |
| Alpaca core MCP | PASS | scheduler-owned core preflight hard gate pass, runtime `get_clock/get_orders/get_asset/get_stock_latest_quote/get_stock_snapshot` 보조 확인 |
| Research MCP | PASS tiered | SEC EDGAR/FRED/Firecrawl/Yahoo 4개 positive; Alpha Vantage는 `provider_error` throttle gap |
| Universe strict | PASS | metadata universe 62개, SPY/QQQ 포함 |
| Quote/spread | PASS for submitted order | NEE runtime quote `2026-06-04T17:54:41.913383064Z`, spread `0.0234%`, quote age `1.7m` |
| Risk plan | PASS | `NEE` 1주 buy_notional `85.36`, cash/ticker/theme/factor/cluster caps 통과 |
| Final submit path | PASS | Alpaca MCP가 `NEE` 1주 regular day limit buy를 생성했고 reconciliation 기준 `status=new` open order다 |

## 후보와 판단

| Symbol | 판단 | Spread | 이유 |
| --- | --- | ---: | --- |
| NEE | submitted_open | 0.0234% | 기존 utilities diversifier holding에 대한 floor-size validation add로 제출됐고 현재 open/new 상태다. |
| NKE | watch | 0.0231% | consumer diversifier지만 2026-06-04 5D review 약세와 lower replacement rank 때문에 NEE보다 우선순위가 낮다. |
| AMZN | watch | 0.0236% | mega-cap quality 보조 후보지만 기존 tech 노출 대비 diversification 기여가 약하다. |
| NVDA | watch | 0.0137% | 핵심 AI thesis는 유지되지만 cluster warning band와 기존 큰 보유 비중 때문에 이번 cycle 신규 add는 보수적으로 유지했다. |
| INTC | watch | 0.0268% | 반도체 cluster 내 약한 review와 sector headline 부담 때문에 NEE보다 ranking이 낮다. |

## Sell/Trim 진단

| Symbol | 판단 | Gate | 설명 |
| --- | --- | --- | --- |
| AVGO | watch | decision_grade_metric_gap | AI semiconductor_complex 경고구간과 급락 반전으로 trim 재점검 대상이지만 decision-grade expected-excess와 replacement margin이 비어 있다. |
| SO | watch | decision_grade_metric_gap | defensive/utilities review 약세와 rate-sensitive 부담은 있지만 per-symbol decision-grade expected-excess 공백이 남아 있다. |
| TSLA | watch | held_quantity_and_metric_gap | 약한 validation review와 speculative growth 성격은 재점검 대상이지만 1주 보유라 whole-share trim 규칙을 만족시키기 어렵고 metric도 비어 있다. |

## 주문 제출과 reconciliation

- Submitted order: `NEE` buy 1 @ `85.36` day limit
- Alpaca order id: `bcd3b9a7-78d4-43d2-a540-4825f572e8fa`
- Client order id: `hourly-20260605-0251-buy-nee`
- Pre-submit gate summary: paper mode `true`, market open, universe strict `PASS`, MCP strict `PASS`, risk `PASS`, NEE quote freshness/spread `PASS`, same-day duplicate/open-order conflict 없음
- `place_stock_order`: 성공, initial response `pending_new`, reconciliation 기준 `status=new`, `filled_qty=0`
- Reconciliation: `get_orders(symbol=NEE)`와 `get_orders(status=open)`가 모두 동일 order를 `status=new`로 반환했고, `get_account_info`는 cash `31222.79`, portfolio value `103696.12`, buying power `256417.16`, long market value `72473.33`를 보여 아직 fill 없이 open order만 생성됐음을 확인했다. direct `get_order_by_client_id`는 tool-layer `cancelled`로 남아 `gap_category=cancelled`를 기록했다.

## 검증 결과

| Validator | 결과 | 비고 |
| --- | --- | --- |
| `check-universe-coverage.py --strict --json` | PASS | 62 symbols, SPY/QQQ 포함, final candidates 5개 |
| `check-mcp-coverage.py --strict --json` | PASS | Alpaca core pass, positive research 4개, Alpha `provider_error` gap only |
| `check-risk-policy.py --json` | PASS | NEE 1주 regular-session day limit buy 계획 통과 |

## 산출물

- Report: `wiki/current-runs/daily/2026-06-05-0251-hourly-autopilot.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-06-05-0251-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-06-05-0251-hourly-autopilot.json`
- Post-trade snapshot: `wiki/trade-ledger/positions/2026-06-05-0251-hourly-autopilot-post-trade.json`

## 지표 설명

- `sell_candidate_diagnostics`: 보유 포지션 중 trim/exit 재점검이 필요한 상위 후보와 metric gap 사유를 남기는 audit trail이다.
- `provider_error`: 이번 cycle의 Alpha Vantage는 scheduler one-call-per-hour throttle 때문에 추가 provider call을 생략했고 `provider_error` gap으로 남았다.
- `same-day duplicate discipline`: 같은 ET regular session에서 이미 제출되었거나 체결된 동일 symbol/side buy를 추가 validation buy로 재사용하지 않는 규칙이다.
- `portfolio_fit`: hard gate가 아니라 ranking/sizing 입력이다. 이번 run에서는 weak-review diversifier 후보들 가운데 duplicate-free이고 macro gate가 유지된 NEE를 floor-size learning order로 선택했다.
