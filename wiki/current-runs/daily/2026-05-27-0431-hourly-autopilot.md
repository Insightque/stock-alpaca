# 2026-05-27 04:31 KST hourly autopilot

## 요약

- Run id: `2026-05-27-0431-hourly-autopilot`
- 실행 모드: submit 후보 평가. `.env`에서 paper mode를 확인했지만, 주문 전에는 universe/MCP/risk/quote/spread/open-order gate를 모두 재검증한다.
- 시장 시계: Alpaca preflight 기준 `2026-05-26T15:31:09.123434238-04:00`, 정규장 open, next close `2026-05-26T20:00:00Z`.
- 계좌: portfolio value `101631.14` USD, cash `42347.59` USD, buying power `137133.22` USD.
- 현재 포지션: 13개. 미체결 주문: AMZN buy 1주 `new`.

## Universe 및 후보

Broad universe는 `harness/symbol-metadata.yaml` 62개와 benchmark `SPY`, `QQQ`를 포함해 통과했다. Pre-MCP shortlist는 `MU`, `AMD`, `KLAC`, `LRCX`, `SMH`, `INTC`, `AMAT`, `AMZN`, `AAPL`, `NVDA`였고, 최종 후보는 `INTC`, `SMH`, `AMAT`로 기록했다.

| 순위 | 심볼 | 판단 | 근거 |
|---:|---|---|---|
| 1 | INTC | 1주 validation buy 후보 | quote age 3.96분, spread 0.0243%, SEC/FRED/Yahoo usable, 중복 INTC 주문 없음 |
| 2 | SMH | 재점검 | spread는 좋지만 기존 AI semiconductor cluster exposure가 높음 |
| 3 | AMAT | 제외 | spread 0.5212%로 risk policy 0.50% 초과 |

## MCP Coverage

| 서버 | 결과 | 사용 | gap_category | 비고 |
|---|---|---:|---|---|
| Alpaca | pass | yes | not_applicable | scheduler core preflight hard gate pass |
| SEC EDGAR | pass | yes | not_applicable | local CIK fallback `INTC -> 0000050863`, company/recent filings pass |
| Alpha Vantage | failed | no | cancelled | health check 후 첫 NEWS_SENTIMENT call cancelled, 추가 Alpha retry 중단 |
| FRED | pass | yes | not_applicable | scheduler research preflight `get_macro_snapshot` pass |
| Firecrawl | failed | no | wrapper_error | registered Codex MCP tool 미노출, shell/curl 미사용 |
| Yahoo Finance | usable | yes | not_applicable | INTC news/recommendations usable |

## 주문 계획

- 제안 주문: INTC 1주 buy, day limit, limit `123.35`, client_order_id `hourly-20260527-0431-intc-buy-1`.
- 상세 rationale: INTC는 fresh quote, 낮은 spread, active/tradable US equity, SEC/FRED/Yahoo 3개 research confirmation을 충족했다. 다만 Yahoo headline에 valuation downgrade가 있고 analyst consensus가 hold-heavy라 확신 점수는 `0.54`로 제한하고 1주 검증 주문만 계획했다. 기존 semiconductor cluster exposure는 약 33.19%로 45% cap 아래이며, INTC 1주 추가 후에도 cap을 넘지 않는다.
- AMZN은 기존 open buy order가 있어 추가 주문을 만들지 않았다.

## 검증 상태

검증 결과: universe strict PASS, MCP strict PASS, risk-check PASS. 이후 제출을 시도했지만 Alpaca MCP wrapper가 두 번 모두 cancelled를 반환했고, post-attempt reconciliation에서 INTC 주문/체결/포지션은 확인되지 않았다.

## 지표 설명

- `quote_age_minutes`: Alpaca quote timestamp와 decision timestamp 사이의 분 단위 차이다. Submit gate는 20분 이내만 허용한다.
- `spread_pct`: `(ask - bid) / midpoint * 100`이다. Risk policy max는 0.50%다.
- `confidence_score`: 가격/추세, MCP source confirmation, 중복 주문, 포트폴리오 집중도를 반영한 workflow 내부 점수다. 0.50 이상만 validation buy 후보가 된다.
- `used_in_score`: MCP 결과가 실제 후보 점수와 actionable 판단에 반영됐는지 나타낸다.

## 제출 전 gate summary

- paper mode: `.env`의 `ALPACA_PAPER_TRADE=true` 확인.
- market clock: Alpaca preflight timestamp `2026-05-26T15:31:09.123434238-04:00`, market open true, next close `2026-05-26T20:00:00Z`.
- order plan path: `wiki/trade-ledger/orders/2026-05-27-0431-hourly-autopilot.json`.
- validators: universe strict PASS, MCP strict PASS, risk-check PASS.
- quote freshness/spread: INTC quote `2026-05-26T19:31:32.567873288Z`, quote age 0.09 minutes versus market.checked_at, bid 123.32, ask 123.35, spread 0.0243%.
- order shape: stock buy, whole share qty 1, day limit, limit 123.35, extended_hours false, client_order_id `hourly-20260527-0431-intc-buy-1`.
- duplicate/open-order check: current open order is AMZN buy 1주 only; no open INTC buy/sell order and no same-day INTC validation buy recorded in current open-order evidence.
- source refs: `wiki/evidence-store/sources/2026-05-27-0431-hourly-autopilot-alpaca-core-preflight.json`, `wiki/evidence-store/sources/2026-05-27-0431-hourly-autopilot-research-mcp-preflight.json`, `wiki/evidence-store/sources/2026-05-27-0431-hourly-autopilot-sources.md`.

## 제출 및 사후 점검

- `place_stock_order` 1차 호출: `user cancelled MCP tool call`.
- 같은 client_order_id `hourly-20260527-0431-intc-buy-1`로 재시도하기 전 reconcile 수행: `get_orders(status=all, symbols=INTC)`는 empty, pre-submit/then-live positions에서 INTC position 없음, `get_order_by_client_id`는 cancelled로 gap 기록.
- 동일 client_order_id 1회 retry: 다시 `user cancelled MCP tool call`. 추가 submit retry 없음.
- Post-attempt reconciliation: `get_orders(status=all, symbols=INTC)` empty, `get_account_activities(FILL, after=2026-05-26T19:30:00Z)` empty, `get_all_positions` pass 및 INTC position 없음.
- 제출 결과: 실제 생성된 INTC 주문 없음, 체결 없음. `orders_submitted=0`.
