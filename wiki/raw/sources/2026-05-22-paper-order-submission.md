---
id: 2026-05-22-paper-order-submission
captured_at: 2026-05-22T14:26:30Z
source: alpaca-mcp
paper: true
immutable: true
---

# 2026-05-22 Paper Order Submission

## 실행 전 확인

- `.env` 기준 `ALPACA_PAPER_TRADE=true` 확인.
- Alpaca clock: `is_open=true`, timestamp `2026-05-22T10:24:13.986725767-04:00`, next close `2026-05-22T16:00:00-04:00`.
- Alpaca account: status `ACTIVE`, portfolio value `100000`, cash `100000`, buying power `200000`.
- 모든 주문 후보는 Alpaca asset 기준 `class=us_equity`, `status=active`, `tradable=true`.
- `python3 scripts/check-risk-policy.py wiki/portfolio/order-plans/2026-05-22-stock-only-proposal.json` 결과: PASS.
- 리스크 검증 시 buy notional `56098.45`, 주문 후 예상 cash `43901.55`, 주문 후 예상 invested `56098.45`.

## 제출 주문

모든 주문은 Alpaca MCP `place_stock_order`를 통해 제출한 day limit, whole-share, long-only paper order다.

| 티커 | 수량 | 지정가 | client_order_id | 제출 ID |
| --- | ---: | ---: | --- | --- |
| NVDA | 35 | 215.32 | stock-only-20260522-nvda-1421 | 71b18158-1e5f-48c5-9626-532bb3ec076c |
| AMD | 14 | 465.00 | stock-only-20260522-amd-1421 | 16ffb224-70b4-413e-ae65-47c5f848167c |
| AVGO | 15 | 411.44 | stock-only-20260522-avgo-1421 | d27eab24-01be-4232-8d6c-db52b3ab1aa3 |
| LRCX | 20 | 309.00 | stock-only-20260522-lrcx-1421 | 60016930-4b6e-4715-97c7-7f6f7cd1de00 |
| TSM | 15 | 405.50 | stock-only-20260522-tsm-1421 | d778222d-256e-499e-bf4f-b80e1fc060dc |
| NOK | 400 | 15.05 | stock-only-20260522-nok-1421 | 26980874-ad48-4b47-b64b-d89ebddd7c48 |
| UNH | 15 | 389.00 | stock-only-20260522-unh-1421 | e399fcf3-def7-4d63-9f19-72680e1c7700 |
| ETN | 15 | 388.25 | stock-only-20260522-etn-1421 | 6586fb41-fe83-43a1-8194-7d03679e4908 |
| RGTI | 120 | 25.57 | stock-only-20260522-rgti-1421 | 5c5c0ba6-3ee0-4549-b45a-e1af91c7f0db |
| IONQ | 45 | 63.80 | stock-only-20260522-ionq-1421 | 1da0ff0c-5b44-47e9-9a19-de38a215c677 |

## 사후 주문 상태

2026-05-22T14:26:30Z 기준:

| 티커 | 상태 | 체결 수량 | 평균 체결가 |
| --- | --- | ---: | ---: |
| NVDA | new | 0 | - |
| AMD | filled | 14 | 462.73 |
| AVGO | filled | 15 | 410.73 |
| LRCX | filled | 20 | 307.91 |
| TSM | filled | 15 | 405.20 |
| NOK | filled | 400 | 15.04 |
| UNH | filled | 15 | 386.56 |
| ETN | filled | 15 | 387.90 |
| RGTI | filled | 120 | 25.569584 |
| IONQ | filled | 45 | 63.48 |

## 사후 계좌와 포지션

- Account after check: portfolio value `100041.52`, cash `51566.78`, buying power `138036.10`, long market value `48474.74`.
- 체결 포지션: AMD, AVGO, LRCX, TSM, NOK, UNH, ETN, RGTI, IONQ.
- NVDA 주문은 미체결 open order로 남아 있다.
