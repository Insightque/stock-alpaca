# 2026-05-27 01:59 KST hourly autopilot

## 요약

- 실행 모드: scheduled Alpaca paper autopilot, submit gate 검증.
- Paper mode: `.env`의 `ALPACA_PAPER_TRADE=true` 확인.
- Market clock: 2026-05-26 13:00:24 ET 기준 open, next close 16:00 ET.
- Alpaca core: fail. `get_clock`, `get_account_activities`, `get_stock_latest_quote`, `get_stock_bars`, `get_news`는 usable했지만 `get_account_info`, `get_all_positions`, `get_orders`, `get_watchlists`, `get_stock_snapshot`, `get_stock_latest_trade`, `get_asset`이 cancelled였다.
- First blocking gate: `alpaca_account`.
- Research MCP: SEC EDGAR pass, Yahoo Finance pass, FRED preflight pass, Alpha Vantage cancelled, Firecrawl wrapper_error.
- Universe gate: 62개 metadata universe와 `SPY`, `QQQ` 포함.
- 주문: 제출 없음. Alpaca account/order/position/asset hard gate가 미확정이라 paper validation order를 만들지 않았다.

## 추천 Shortlist

| 순위 | 티커 | 판단 | 근거 | 차단/주의 |
| ---: | --- | --- | --- | --- |
| 1 | NOK | recheck | 52-week high 관련 Alpaca news, Yahoo AI infrastructure/news, SEC 6-K recent filing, quote spread 0.060% | 이미 400주 보유, account/order/position/asset gate cancelled |
| 2 | SMH | recheck | 반도체 ETF 모멘텀, quote spread 0.025%, AI semiconductor basket proxy | 기존 AMD/AVGO/LRCX/NVDA/TSM 보유로 cluster 집중, SEC ETF lookup 없음 |
| 3 | FCX | recheck | quote spread 0.016%, 보유 1주 validation fill 이후 materials/mining 분산 후보 | 직전 run 신규 매수 직후라 duplicate/same-day order gate 확인 필요하나 open-order check cancelled |
| 4 | NVDA | recheck | fresh tight quote, AI semiconductor quality 후보 | 기존 보유와 반도체 cluster 집중 |
| 5 | AAPL | recheck | fresh quote와 mega-cap liquidity | catalyst 점수는 NOK/SMH/FCX보다 낮음 |

## 주문 계획

| 티커 | Side | Qty | Type | Limit | Reference | Spread | Rationale |
| --- | --- | ---: | --- | ---: | ---: | ---: | --- |
| 없음 | - | 0 | - | - | - | - | Alpaca account, positions, open orders, asset tradability gate가 cancelled되어 duplicate/order/risk submit state를 확정할 수 없다. |

## 제출/스킵

- 제출 전 gate summary는 작성하지 않았다. 제출 후보가 없고, `place_stock_order`를 호출하지 않았기 때문이다.
- 제출 차단: `alpaca_account`가 첫 hard gate로 실패했고, `alpaca_positions`, `alpaca_open_orders`, `alpaca_asset_tradability`도 실패했다.
- Quote/spread는 `NOK`, `SMH`, `FCX`, `NVDA`, `AAPL`, `INTC`가 pass였지만 core submit gate 실패가 우선한다.
- `MU`, `LLY`, `AVGO`, `PLTR`는 spread가 0.50%를 넘어 submit 불가다.
- Same-day fills: `LLY` 1주 buy, `FCX` 1주 buy를 Alpaca activities에서 확인했다.
- Validator: universe strict PASS, MCP strict FAIL, empty-order risk policy PASS.

## MCP Coverage

| MCP | Outcome | Used | Gap category | Note |
| --- | --- | --- | --- | --- |
| alpaca | failed | no | cancelled | clock/activities/quotes/bars/news usable, account/positions/orders/watchlists/snapshot/trade/assets cancelled |
| sec-edgar | pass | yes | not_applicable | local CIK cache로 `NOK -> 0000924613` 확인 후 company/recent filings 조회 |
| alpha-vantage | failed | no | cancelled | PING은 pass, 첫 non-PING candidate data call cancelled 후 retry 중단 |
| fred | pass | yes | not_applicable | scheduler preflight `get_macro_snapshot` pass |
| firecrawl | failed | no | wrapper_error | Codex tool catalog에 registered Firecrawl MCP tool 미노출 |
| yahoo-finance | pass | yes | not_applicable | NOK news와 recommendations 조회 |

## 지표 설명

- `spread_pct`: `(ask - bid) / midpoint * 100`. Risk policy의 submit 상한은 0.50%다.
- `quote_age_minutes`: 주문 제출 후보는 quote/snapshot 기준 20분 이내여야 한다.
- `first_blocking_gate`: 주문 제출을 중단시킨 첫 hard gate다. 이번 run은 `alpaca_account`다.
- `research MCP confirmation`: SEC EDGAR, Alpha Vantage, FRED, Firecrawl, Yahoo Finance 중 usable/pass인 provider 수다. 이번 run은 SEC/Yahoo/FRED 3개가 pass지만 Alpaca core가 fail이라 actionable order가 아니다.
- `recheck`: 가격/뉴스상 관찰 가치가 있지만 주문 제출 hard gate 또는 포트폴리오 제약 때문에 이번 run에서 주문하지 않는 상태다.

## 산출물

- Source note: `wiki/evidence-store/sources/2026-05-27-0159-hourly-autopilot-sources.md`
- Manifest: `wiki/evidence-store/run-manifests/2026-05-27-0159-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-05-27-0159-hourly-autopilot.json`
