---
id: 2026-05-23-intraday-scalping-minute-validation
created_at: 2026-05-23T18:20:00+09:00
source_type: intraday-scalping-minute-validation
paper: true
---

# 시간별 단타 정책 분봉 검증과 다음 단계

## 목적

`intraday-rs-breakout-v0`의 다음 단계로, 1시간봉 timestamp를 실전 가능 시각으로 보정하고 1분봉으로 stop/take 순서를 검증했다. 검증 표본은 앞선 세 차례 분석에서 사용한 28개 거래일이다.

실제 주문은 제출하지 않았다.

## 중요 보정

Alpaca `1Hour` bar의 timestamp는 해당 시간봉의 시작 시각이다. 따라서 `10:00` bar close를 10:00에 알고 진입하는 것은 불가능하다. 이 값은 11:00 이후에만 알 수 있다.

보정 후 정책 해석:

- 기존 v0: 10:00~11:00 ET hour bar가 닫힌 뒤, 11:00 이후 진입.
- confirmation 버전: 11:00~12:00 ET hour bar까지 확인한 뒤, 12:00 이후 진입.

이 보정은 기존 문서의 “10:00 진입” 표현을 대체한다.

## variants 결과

| variant | active days | 거래 수 | hit rate | stop | take | 가상 P/L | 평균/거래 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| v0: 11:00 진입, top3, take +2% | 14 | 34 | 55.9% | 12 | 11 | +$1,410.00 | +$41.47 |
| v1: 12:00 confirmation, top3, take +2% | 10 | 25 | 44.0% | 8 | 5 | +$556.63 | +$22.27 |
| v2: 12:00 confirmation, top2, take +2% | 10 | 18 | 44.4% | 5 | 3 | +$488.35 | +$27.13 |
| v3: 12:00 confirmation, top1, take +2% | 10 | 10 | 30.0% | 4 | 1 | -$175.96 | -$17.60 |
| v4: 12:00 confirmation, top2, take +1.5% | 10 | 18 | 44.4% | 5 | 6 | +$444.87 | +$24.72 |

## 해석

1. timestamp를 보정해도 기존 v0의 누적 결과는 플러스였다.
   - 28거래일, 34거래, +$1,410.00.
   - 1분봉 기준으로 take 11건, stop 12건, 나머지는 EOD 청산이었다.

2. 12:00 confirmation은 손실일 일부를 걸렀지만, 수익일도 같이 줄였다.
   - v1/v2/v4는 모두 플러스지만 v0보다 기대값이 낮다.
   - 2026-04-02, 2026-02-20, 2026-04-29 같은 실패 confirm 회피는 도움이 됐다.
   - 반대로 2026-03-09, 2026-04-22 같은 강한 추세일의 수익 일부를 늦게 들어가며 포기했다.

3. top1 축소는 오히려 나빴다.
   - v3는 -$175.96으로 음수였다.
   - 단타에서는 단일 최고점수 종목 하나에 의존하면 종목별 노이즈가 커졌다.

4. take +1.5%는 take 횟수를 늘렸지만 총손익을 개선하지 못했다.
   - v4는 take 6건으로 v2보다 많았지만, 총손익은 +$444.87로 v2보다 낮았다.
   - +2% take의 손익비가 아직 더 낫다.

## 정책 판단

기존 `자동 주문 부적합` 판단은 유지한다. 다만 이유를 더 정확히 정리한다.

- 1분봉 검증상 v0 자체는 플러스 기대값 후보로 남아 있다.
- 하지만 IEX feed, 분봉 기준, 슬리피지 미반영, limit/stop 실제 체결 불확실성이 있다.
- confirmation variants가 v0보다 안정적으로 개선하지 못했다.
- 따라서 자동 주문보다는 `paper-only manual candidate`로 두고, 실시간 paper dry-run으로 먼저 검증해야 한다.

## 다음 실험 제안

1. 실시간 paper dry-run: 다음 미국 정규장 5~10일 동안 주문 제출 없이 11:00 ET 신호만 기록한다.
2. fill-aware paper micro-trade: 종목당 계좌 2~3% 이하, top2까지만, 실제 paper order fill을 관찰한다.
3. sector guard: QQQ뿐 아니라 SMH가 11:00 이후 양수이고 고점 근처일 때만 반도체 종목 진입.
4. same-day stop lockout: 첫 2개 포지션이 stop이면 당일 신규 진입 금지.
5. cooldown rule: 11:00 진입 후 첫 5분 안에 -0.4% 이상 밀리면 추가 진입 금지.

## 결론

분봉 검증의 결론은 “v0가 완전히 깨진 것은 아니지만, 자동화할 만큼 안정적이지 않다”이다. 현재 가장 합리적인 다음 단계는 주문 없는 실시간 paper dry-run으로 11:00 ET 신호와 실제 bid/ask, fill 가능성을 5~10일 모으는 것이다.

## 연결 원천

- [[2026-05-23-intraday-scalping-minute-validation-sources]]
- [[2026-05-23-random-intraday-scalping-5x-simulation]]
- [[recommendation-policy]]
