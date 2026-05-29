---
id: 2026-05-30-overnight-trade-review-alpaca-readonly
created_at: 2026-05-30T07:25:00+09:00
source: alpaca_mcp_readonly
paper: true
---

# 2026-05-30 지난 밤 거래 회고용 Alpaca read-only 확인

## 범위

2026-05-29 22:31 KST부터 2026-05-30 06:51 KST까지 정규장/장외 자동운영 거래를 회고하기 위해 Alpaca MCP read-only 도구만 사용했다. 주문 제출, 교체, 취소, 청산 도구는 호출하지 않았다.

## 계좌 확인

- Account status: ACTIVE.
- Portfolio value: 101,970.93 USD.
- Cash: 34,800.26 USD.
- Buying power: 130,769.33 USD.
- Long market value: 67,170.67 USD.

## FILL 활동

조회 범위는 `2026-05-29T13:30:00Z`부터 `2026-05-29T20:00:00Z`까지다.

| UTC time | Symbol | Side | Qty | Price |
| --- | --- | --- | ---: | ---: |
| 2026-05-29T13:41:55Z | PFE | buy | 1 | 26.09 |
| 2026-05-29T13:57:30Z | NKE | buy | 1 | 46.59 |
| 2026-05-29T13:57:42Z | SO | buy | 1 | 91.55 |
| 2026-05-29T13:57:56Z | SLB | buy | 1 | 54.79 |
| 2026-05-29T14:01:11Z | AMZN | buy | 1 | 272.76 |
| 2026-05-29T15:01:43Z | QQQ | buy | 1 | 737.62 |
| 2026-05-29T15:01:55Z | V | buy | 1 | 331.00 |
| 2026-05-29T15:18:01Z | GOOGL | buy | 1 | 383.13 |
| 2026-05-29T15:19:11Z | NEE | buy | 1 | 86.46 |
| 2026-05-29T15:19:29Z | WMT | buy | 1 | 115.00 |

총 10건, 총 체결 원금은 약 2,144.99 USD다.

## 미체결 주문 확인

- `hourly-20260530-0031-buy-mrk`: MRK 1주 day limit buy, limit 118.35 USD.
- Filled qty: 0.
- Status: canceled.
- Canceled at: 2026-05-29T16:11:12Z.

## 보유 가격 확인

Alpaca `get_open_position` current_price 기준으로 위 10건을 1주 단위로 단순 mark-to-market하면 약 -7.22 USD, -0.34%다. 이는 공식 1D 회고가 아니라 회고 시점 read-only 현재가 기반의 임시 표시다.
