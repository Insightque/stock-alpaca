---
id: 2026-05-23-intraday-scalping-minute-validation-sources
created_at: 2026-05-23T18:15:00+09:00
source_type: alpaca-market-data-rest
paper: true
---

# 시간별 단타 정책 분봉 검증 원천

## 목적

이전 `intraday-rs-breakout-v0` 검증의 다음 단계로, Alpaca `1Hour` bar timestamp 해석을 보정하고 Alpaca `1Min` bars로 stop/take 체결 순서를 확인하기 위한 원천 기록이다.

## 데이터 원천

- 가격: Alpaca Market Data API, IEX feed.
- 사용 bars:
  - `1Hour`: signal 생성.
  - `1Min`: 진입 이후 stop/take/EOD 체결 순서 검증.
- 조회 범위: 2026-02-01~2026-05-23.
- 후보군: QQQ, SMH, NVDA, AMD, TSLA, PLTR, AVGO, TSM, LRCX.
- 검증 표본: 기존 1차, 2차, 무작위 5회 반복에서 사용한 28개 거래일.

## timestamp 보정

Alpaca `1Hour` bar의 timestamp는 해당 시간봉의 시작 시각으로 해석했다.

- `09:00` bar close는 10:00 이후에 알 수 있다.
- `10:00` bar close는 11:00 이후에 알 수 있다.
- `11:00` bar close는 12:00 이후에 알 수 있다.

따라서 기존 정책의 실전 가능 해석은 다음과 같다.

- 초기 risk filter와 후보 점수: `10:00` hour bar close 사용.
- 실제 진입 가능 시각: 11:00 ET 이후.
- confirmation 버전: `11:00` hour bar close까지 확인 후 12:00 ET 이후 진입.

## 검증한 variants

| variant | 설명 |
| --- | --- |
| `v0_correct_11entry_top3_take2` | 기존 v0를 timestamp 보정. 11:00 이후 진입, 상위 3개, +2% take / -1% stop |
| `v1_12confirm_top3_take2` | 12:00 이후 진입. QQQ/SMH/종목 확인 유지, 상위 3개, +2% take |
| `v2_12confirm_top2_take2` | 12:00 이후 진입. confirmation, 상위 2개, +2% take |
| `v3_12confirm_top1_take2` | 12:00 이후 진입. confirmation, 상위 1개, +2% take |
| `v4_12confirm_top2_take15` | 12:00 이후 진입. confirmation, 상위 2개, +1.5% take |

## 데이터 공백과 한계

- IEX feed 기준이므로 전체 SIP 체결량과 다를 수 있다.
- 1분봉 안에서 stop과 take가 동시에 가능한 경우는 보수적으로 stop first로 처리했다.
- 실제 주문에서는 스프레드, 슬리피지, limit fill 실패, 부분체결이 추가로 발생할 수 있다.
- 이번 검증은 과거 market data 기반 dry-run이며 실제 주문 제출은 없었다.
