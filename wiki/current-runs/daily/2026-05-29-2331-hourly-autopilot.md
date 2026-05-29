# 2026-05-29-2331-hourly-autopilot scheduled paper autopilot

## 요약

- 실행 모드: regular-session hourly autopilot, `mode=submit`, paper only.
- Paper gate: `ALPACA_PAPER_TRADE=true` 확인.
- 시장 clock: Alpaca MCP preflight 기준 `is_open=true`, timestamp `2026-05-29T10:31:09.628139421-04:00`.
- Alpaca core: scheduler-owned Alpaca MCP preflight hard gate `pass` 사용. account, positions, recent activities, watchlists, asset checks, latest quote/snapshot/trade rows가 read-only MCP evidence로 존재한다.
- Research MCP: SEC EDGAR/FRED/Firecrawl/Yahoo Finance usable/pass, Alpha Vantage는 daily rate-limit `provider_error` 공백이다. 최소 3개 research confirmation은 충족했다.
- 주문 결정: stale order cleanup이 `hourly-20260529-2231-buy-bac` 취소 시도를 `pass`로 기록했지만 같은 cleanup artifact가 BAC를 계속 `new` open으로 보여 `risk_open_order_lifecycle`에서 신규 주문을 모두 차단했다.

## 게이트 상태

| Gate | 상태 | 근거 |
| --- | --- | --- |
| Paper mode | PASS | 환경값 `ALPACA_PAPER_TRADE=true` |
| Market open | PASS | `wiki/evidence-store/sources/2026-05-29-2331-hourly-autopilot-alpaca-core-preflight.json` |
| Alpaca core MCP | PASS | account/positions/open orders/recent activities/watchlists/assets/quotes/snapshots/trades preflight |
| Open-order lifecycle | BLOCK | stale BAC cancel attempt 후에도 cleanup `remaining_open_orders`에 BAC `new`가 남음 |
| Universe strict | PASS | broad universe 62개, SPY/QQQ 포함 |
| Research MCP tiered | PASS | 4 usable/pass providers, Alpha Vantage provider_error gap |
| Quote freshness/spread | BLOCK FOR SUBMIT | core quote gate는 pass지만 open-order lifecycle hard gate로 주문별 quote/spread submit 판단을 진행하지 않음 |
| Risk validator | PENDING | order plan 작성 후 validator 실행 |
| Submit | SKIPPED | first_blocking_gate=`risk_open_order_lifecycle` |

## sell/trim 진단

보유 포지션을 신규 매수보다 먼저 점검했다. AI semiconductor theme은 target-band warning 구간으로 진입했지만, 정상 sell gate 중 open-order lifecycle/risk gate가 막혀 trim 주문은 만들지 않았다. PLTR과 RGTI는 각각 과열/투기 약세 watch 대상이나 YAML trigger 조건은 충족하지 못했다.

| Symbol | Held qty | Weight % | Trigger | 판단 |
| --- | ---: | ---: | --- | --- |
| AMD | 14 | 7.050 | blocked_by_gate | AI semiconductor target-band warning, lifecycle blocker 때문에 trim 없음 |
| PLTR | 1 | 0.153 | sell_trigger_none | 이익 과열 watch, reversal trigger 미확인 |
| RGTI | 120 | 2.932 | sell_trigger_none | 투기 포지션 약세 watch, speculative-loss trigger 미충족 |

## 후보 및 주문 판단

| Symbol | 판단 |
| --- | --- |
| QQQ | 벤치마크/성장 recheck 후보, lifecycle blocker 때문에 주문 없음 |
| AAPL | mega-cap quality recheck 후보, lifecycle blocker 때문에 주문 없음 |
| NKE | 최근 validation fill 보유, 추가 매수는 lifecycle blocker 및 lifecycle review 대기 때문에 없음 |

기존 stale/open 주문은 BAC 1주 limit $50.72이다. cleanup artifact가 취소 시도 `pass`를 기록했지만 BAC가 `remaining_open_orders`에 남아 이번 run의 신규 submit을 막았다.

## validation lifecycle

`risk_trim_policy.validation_lifecycle`를 적용했다. 2026-05-27 validation buy의 1D 회고는 `wiki/index.md` 기준 NKE/PFE/SO/WMT/NEE/AMZN/BAC/XOM/V에 기록되어 있고, same-day fill인 PFE/NKE/SO/SLB/AMZN은 아직 1D/5D/20D review due가 아니다. 누락 due review로 추가 매수를 차단해야 하는 symbol은 없지만, open-order lifecycle이 전체 신규 주문을 차단했다.

## MCP 공백

- `alpha-vantage`: `provider_error`. Alpha Vantage daily API rate limit 때문에 NEWS_SENTIMENT data를 사용할 수 없었다. 비차단 공백이며 retry_count=0, source_ref `wiki/evidence-store/sources/2026-05-29-2331-hourly-autopilot-research-mcp-preflight.json`.
- 나머지 research MCP: SEC EDGAR, FRED, Firecrawl, Yahoo Finance는 scheduler research preflight에서 usable/pass로 반영했다.

## 주문 계획

- Order plan: `wiki/trade-ledger/orders/2026-05-29-2331-hourly-autopilot.json`
- Planned orders: 0
- Submitted orders: 0
- First blocking gate: `risk_open_order_lifecycle`
- Next action: stale BAC order의 실제 취소/체결/만료 상태가 다음 scheduler preflight에서 reconcile될 때까지 신규 submit 금지.

## 검증 결과

- Universe validator: `PATH=/usr/local/bin:$PATH python3 scripts/check-universe-coverage.py --strict --json ...` PASS.
- MCP validator: `PATH=/usr/local/bin:$PATH python3 scripts/check-mcp-coverage.py --strict --json ...` PASS.
- Risk validator: `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json ...` FAIL. BAC open order age 51.8분이 `order_lifecycle.max_open_order_age_minutes=30`을 초과했고, empty order warning도 기록됐다.

## 지표 설명

- `spread_pct`: `(ask - bid) / midpoint * 100`으로 계산한 호가 스프레드다. 정책 상한은 0.50%다.
- `quote_age_minutes`: order plan 작성 시점과 quote timestamp의 차이다. submit 상한은 20분이다.
- `mcp_coverage.used_in_score`: 해당 MCP evidence가 점수, confidence, risk, allocation 판단에 반영됐는지를 뜻한다.
- `sell_trigger_none`: risk trim policy의 활성 매도/축소 사유가 현재 evidence로 확인되지 않았다는 뜻이다.
- `risk_open_order_lifecycle`: stale/open order 정리 또는 reconciliation이 불확실해서 신규 주문을 막는 hard gate다.

## 산출물

- Manifest: `wiki/evidence-store/run-manifests/2026-05-29-2331-hourly-autopilot.json`
- Order plan: `wiki/trade-ledger/orders/2026-05-29-2331-hourly-autopilot.json`
- Report: `wiki/current-runs/daily/2026-05-29-2331-hourly-autopilot.md`
