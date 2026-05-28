# 2026-05-28-2311-hourly-autopilot scheduled paper autopilot

## 요약

- Paper mode: `ALPACA_PAPER_TRADE=true`. 정규장 clock은 `2026-05-28T10:15:52.783464074-04:00` 기준 open=true.
- Scheduler stale cleanup: `pass`로 기록됐지만 BAC stale cancel 직후 파일에는 BAC가 남아 있었다. 등록된 Alpaca MCP `get_orders` 재조정에서 현재 open order는 NEE 1건뿐으로 확인되어 BAC는 새 주문 차단 사유가 아니었다.
- Alpaca core gate: PASS. scheduler core preflight와 등록 Alpaca MCP clock/positions/orders/quotes/snapshots/fills를 사용했다. Account fresh call은 계획 전에는 `cancelled`였지만 post-trade account refresh는 ACTIVE, cash 39,924.27, portfolio value 101,471.45로 확인됐다.
- Research MCP gate: SEC EDGAR, FRED, Firecrawl, Yahoo Finance PASS; Alpha Vantage는 `empty_response` gap. 4개 usable/pass로 submit 기준 3개를 충족했다.
- 실행 결과: WMT 1주 buy limit 118.63은 첫 submit `cancelled` 후 같은 client id 재시도에서 open/new. PFE 1주 buy limit 26.18은 첫 submit `cancelled` 후 같은 client id 재시도에서 26.16 체결.

## 후보 및 주문 계획

| Symbol | Action | Qty | Limit | Spread % | 근거 |
| --- | --- | ---: | ---: | ---: | --- |
| WMT | buy | 1 | 118.63 | 0.0253 | 소비 방어/defensive quality 클러스터의 소액 추가 검증 후보. WMT는 오늘 같은 심볼/side 주문이 없고, NEE open order와 클러스터가 다르며, quote age 1분 미만과 spread 0.03% 미만으로 제출 조건을 충족했다. |
| PFE | buy | 1 | 26.18 | 0.0382 | 방어적 헬스케어 클러스터의 저가 1주 검증 후보. PFE는 같은 날 regular-session buy가 없고, 현재 포트폴리오의 고베타/반도체 비중을 희석한다. |

## 게이트

- Universe strict: PASS. 62개 metadata universe, SPY/QQQ 포함, pre-MCP shortlist 10개, final candidates 3개.
- MCP strict: PASS. Alpaca core PASS + research usable/pass 4개. Alpha Vantage gap은 `empty_response`로 기록하고 점수에는 미사용.
- Risk validator: PASS. 계획 buy notional 144.81, post-cash 39,805.62, post-invested 61,700.35로 medium-risk-v1.1 한도 안이다.
- Open-order lifecycle: NEE open buy는 계획 시점 약 18분으로 stale 한도 30분 이내였고, WMT/PFE와 심볼/클러스터가 달라 중복 차단 대상이 아니었다.

## 지표 설명

- `spread_pct`: Alpaca latest quote의 bid/ask 중간값 대비 스프레드. 0.50% 이하여야 제출 가능하다.
- `quote_age_minutes`: 주문 계획 생성 시점 기준 quote 경과 시간. 정책상 20분 이하여야 한다.
- `research confirmations`: SEC EDGAR, Alpha Vantage, FRED, Firecrawl, Yahoo Finance 중 usable/pass로 확인된 provider 수. Buy 제출은 3개 이상이 필요하다.
- `risk_open_order_lifecycle`: stale unfilled autopilot order가 취소 또는 조정되지 않아 새 주문을 막는 상태. 이번 run에서는 BAC stale 주문이 재조정에서 open이 아니고 NEE는 fresh여서 발생하지 않았다.

## 제출 및 사후 점검

| Symbol | Client order id | Status | Filled qty | Fill price | 비고 |
| --- | --- | --- | ---: | ---: | --- |
| WMT | `hourly-20260528-2311-wmt-buy-01` | new/open | 0 |  | 첫 submit `cancelled`, 같은 client id 재시도 accepted |
| PFE | `hourly-20260528-2311-pfe-buy-01` | filled | 1 | 26.16 | 첫 submit `cancelled`, 같은 client id 재시도 후 order-by-client-id에서 체결 확인 |

- 남은 open order: WMT 1주 limit 118.63, prior NEE 1주 limit 88.00.
- Post-trade account/positions/open-order reconciliation: PASS. Fresh fill activity refresh만 runtime에서 `cancelled`; PFE fill은 order-by-client-id와 positions에서 확인했다.
- Review due: PFE `회고 대기`; WMT/NEE open-order lifecycle follow-up 필요.
