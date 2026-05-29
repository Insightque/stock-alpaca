---
id: ADBE
updated_at: 2026-05-29T09:15:00+09:00
symbol: ADBE
asset_type: stock
---

# ADBE

## 현재 Thesis

ADBE는 after-hours validation bucket에서 소액으로만 확인할 수 있는 software/growth_quality 후보로 둔다. 2026-05-29 09:11 KST scheduler preflight와 fresh Alpaca MCP overnight quote에서 active/tradable US equity이고, 1주 notional이 after-hours per-order cap 안에 들어왔다.

## 추세

- 일간: fresh overnight quote 기준 bid/ask가 좁고 체결 가능성은 양호하지만, 장외 유동성은 정규장보다 얕다.
- 주간/월간: broad universe 후보 중 AI semiconductor 집중을 늘리지 않는 성장 소프트웨어 분산 후보로 취급한다.

## 촉매

- Software/growth_quality factor에 대한 분산 노출.
- ADBE는 현재 paper 계좌에 없는 신규 validation 표본이라, 기존 NVDA/AMD/AVGO/LRCX 중심 반도체 cluster와 분리된 학습 표본을 만든다.

## 리스크

- 장외 quote는 빠르게 stale 또는 wide spread로 바뀔 수 있다.
- Alpha Vantage는 이번 run에서 `empty_response`, FRED는 504 `provider_error`였으므로 SEC EDGAR/Firecrawl/Yahoo Finance 확인에 의존한다.
- validation 목적의 1주 주문 외 추가 sizing 근거는 아직 없다.

## 포트폴리오 맥락

- 현재 노출: 0주.
- 제안 역할: after-hours validation bucket의 software/growth_quality 신규 표본.
- 현재 조치: risk/universe/MCP gate 통과 시 1주 extended-hours day limit buy만 허용.

## 점수

- 점수: 76/100
- 신뢰도: 중간

## 출처

- [[2026-05-29-0911-after-hours-autopilot]]
- `wiki/evidence-store/sources/2026-05-29-0911-after-hours-autopilot-alpaca-core-preflight.json`
- `wiki/evidence-store/sources/2026-05-29-0911-after-hours-autopilot-research-mcp-preflight.json`
