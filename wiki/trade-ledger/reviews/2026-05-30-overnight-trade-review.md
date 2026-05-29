---
id: 2026-05-30-overnight-trade-review
review_type: waiting
reviewed_at: 2026-05-29T22:25:00Z
paper: true
decision_date: 2026-05-29
entry_date: 2026-05-29
exit_date:
---

# 2026-05-29 밤 정규장/장외 거래 회고

## 요약 판단

- 결론: 판단 보류. 지난 밤 실제 체결은 모두 1주 단위 validation buy이며, 아직 1D/5D/20D 성과 판단 시점이 아니다.
- 실행 품질: 대체로 양호. 모든 실제 체결은 paper, long-only, whole-share, day limit이며 Alpaca MCP를 통해 제출됐다.
- 임시 성과: Alpaca read-only current price 기준 체결 10건 합산 약 -7.22 USD, -0.34%.
- 정책 반영 여부: 보류. 단일 야간 cohort이고, 1D close 이후 회고가 아직 필요하다.

## 거래 개요

범위는 2026-05-29 22:31 KST 정규장 자동운영부터 2026-05-30 06:51 KST 장외 자동운영까지다. Alpaca MCP FILL 활동 기준 실제 체결은 10건, 전부 buy다. 매도 체결은 없었다.

| Symbol | KST fill window | Qty | Fill | Review price | 임시 P/L | 임시 수익률 | 판단 |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| PFE | 22:41 | 1 | 26.09 | 26.13 | +0.04 | +0.16% | 대기 |
| NKE | 22:57 | 1 | 46.59 | 46.28 | -0.31 | -0.67% | 대기 |
| SO | 22:57 | 1 | 91.55 | 91.66 | +0.11 | +0.12% | 대기 |
| SLB | 22:57 | 1 | 54.79 | 54.55 | -0.24 | -0.44% | 대기 |
| AMZN | 23:01 | 1 | 272.76 | 270.52 | -2.24 | -0.82% | 대기 |
| QQQ | 00:01 | 1 | 737.62 | 737.95 | +0.33 | +0.04% | 대기 |
| V | 00:01 | 1 | 331.00 | 327.66 | -3.34 | -1.01% | 대기 |
| GOOGL | 00:18 | 1 | 383.13 | 380.51 | -2.62 | -0.68% | 대기 |
| NEE | 00:19 | 1 | 86.46 | 86.70 | +0.24 | +0.28% | 대기 |
| WMT | 00:19 | 1 | 115.00 | 115.81 | +0.81 | +0.70% | 대기 |

MRK는 2026-05-30 00:31 KST run에서 1주 buy가 제출됐지만 체결되지 않았고, Alpaca read-only 조회 기준 `canceled`, filled_qty 0이다. 장외 06:11/06:31/06:51 runs는 stale overnight quote 때문에 신규 주문이 없었다.

## 당시 판단 복원

- 22:31 run: SPY/AMZN/NKE/PFE/BAC를 계획했지만 PFE만 즉시 체결됐고, AMZN은 이후 체결됐다. NKE는 최초 run에서는 not submitted였으나 22:51 run의 동일 client-id retry에서 체결됐다. SPY/BAC는 stale/open lifecycle에서 후속 차단과 정리 대상이 됐다.
- 22:51 run: NKE/SO/SLB를 서로 다른 cluster의 소액 validation buy로 체결했다. SPY/AMZN/BAC fresh open orders는 duplicate/cluster buy를 막는 역할을 했다.
- 23:11/23:31 runs: SPY/BAC open-order lifecycle 때문에 신규 submit을 막았다. 이는 정상적인 보호 차단이었다.
- 23:51 run: open-order lifecycle이 해소된 뒤 QQQ/V를 체결했다. AAPL/COP/NOK는 1D lifecycle review 미작성으로 add 차단됐다.
- 00:11 run: GOOGL/WMT/NEE를 1주씩 체결했다. WMT는 safety-monitor cancelled 후 same-client-id reconciliation과 1회 retry로 체결됐다.
- 00:31 run: MRK 1주 buy는 제출됐지만 미체결 후 취소됐다.
- 00:51 이후 정규장 runs: MRK fresh/open 또는 cleanup 이후 no-force-replace, same-session exposure, lifecycle review, thesis/target-band 제약으로 신규 주문 없음.
- 장외 runs: quote freshness 5분 cap을 통과하지 못해 주문 없음. BOATS/overnight quote source gap을 submit 근거로 쓰지 않은 것은 타당했다.

## 잘한 점

- 체결 규모가 모두 1주 validation이라, 후보가 일부 약해도 계좌 손상은 작았다.
- 정규장 중반부터 `sell_candidate_diagnostics`를 먼저 기록했고, 신규 매수와 별도로 sell/trim을 점검했다.
- SPY/BAC stale/open order lifecycle 차단은 중복 주문과 불확실한 주문 상태 확대를 막았다.
- AAPL/COP/NOK 추가매수를 due lifecycle review 전까지 막은 것은 정책학습 관점에서 좋았다.
- 장외 자동운영은 stale quote와 subscription gap을 이유로 강제 주문하지 않았다.

## 부족했던 점

- 한 밤에 10건의 신규 validation fills가 쌓였다. 1주 단위라도 회고 대기열이 커져 다음 1D/5D 분석의 노이즈가 늘 수 있다.
- V, GOOGL, AMZN이 임시 mark-to-market 손실의 대부분을 만들었다. 성장/quality label만으로 단기 진입 우위가 보장되지는 않았다.
- Defensive/diversification 후보인 NKE/SO/SLB/NEE/WMT/PFE는 방향이 섞였다. 분산 목적은 맞지만 alpha 근거는 아직 약하다.
- sell 진단의 `expected_excess_return_20d_pct`와 `relative_to_spy_20d_pct`가 아직 0 또는 정성 진단 중심이라, 향후 회고 feature로는 약하다.
- Tool safety monitor cancellation 후 same-client-id retry가 여러 차례 필요했다. 중복 주문을 만들지는 않았지만 실행 로그 해석을 어렵게 한다.

## 운 또는 당시 알기 어려웠던 점

- 2026-05-29 장중 AI/growth 선호가 정규장 후반까지 얼마나 유지될지는 주문 시점에 확정하기 어려웠다.
- MRK는 defensiveness를 늘리는 방향이었지만, 장 후반 limit가 체결되지 않았다. 미체결 자체는 손익 영향이 없고, 무리한 재주문을 하지 않은 점이 더 중요하다.
- 장외 quote가 오래된 상태였던 것은 runtime에서 확인 전까지 주문 가능성처럼 보일 수 있었지만, 정책상 submit 금지로 처리됐다.

## 다음 추천 정책에 줄 교훈

- 지난 밤 결과만으로 정책을 바꾸지는 않는다.
- 다만 `review_backlog_throttle` 가설은 남긴다. 같은 ET session에서 1D review가 쌓이기 전에 신규 validation fill이 과도하게 누적되면, 다음 buy slot을 더 엄격히 제한할 수 있다.
- `same-client-id retry`는 계속 유지한다. 다른 client id로 재시도하지 않은 덕분에 중복 주문을 피했다.
- sell/trim 자체는 강제할 근거가 아직 없다. 현재 데이터로는 "팔 것이 없어서 안 판 것"에 가깝지만, sell 후보 정량 feature는 개선 대상이다.

## 정책 업데이트 제안

- 상태: 보류.
- 제안: `recommendation-policy.md` 또는 YAML 변경 없음.
- 근거: 이번 거래들은 아직 1D 결과가 완성되지 않았고, 미실현 임시 손익도 -0.34% 수준이다. 2026-06-01 정규장 close 이후 1D 회고에서 hold/add/trim/close 결정을 내려야 한다.

## 다음 review due

- 2026-05-29 밤 체결 10건: 다음 미국 정규장 close 이후 1D 회고 due.
- QQQ/V/GOOGL/WMT/NEE는 이미 `wiki/trade-ledger/reviews/2026-05-30-portfolio-review.md`에서 다음 1D 회고 대기로 표시되어 있다.
- PFE/NKE/SO/SLB/AMZN도 같은 cohort로 묶어 1D/5D/20D lifecycle 판단이 필요하다.

## 연결 문서

- 주문 계획: `wiki/trade-ledger/orders/2026-05-29-2231-hourly-autopilot.json`, `wiki/trade-ledger/orders/2026-05-29-2251-hourly-autopilot.json`, `wiki/trade-ledger/orders/2026-05-29-2351-hourly-autopilot.json`, `wiki/trade-ledger/orders/2026-05-30-0011-hourly-autopilot.json`, `wiki/trade-ledger/orders/2026-05-30-0031-hourly-autopilot.json`
- 당시 리포트: [[2026-05-29-2231-hourly-autopilot]], [[2026-05-29-2251-hourly-autopilot]], [[2026-05-29-2311-hourly-autopilot]], [[2026-05-29-2331-hourly-autopilot]], [[2026-05-29-2351-hourly-autopilot]], [[2026-05-30-0011-hourly-autopilot]], [[2026-05-30-0031-hourly-autopilot]], [[2026-05-30-0611-after-hours-autopilot]], [[2026-05-30-0631-after-hours-autopilot]], [[2026-05-30-0651-after-hours-autopilot]]
- 원천 자료: [[2026-05-30-overnight-trade-review-alpaca-readonly]], [[2026-05-30-0625-analyst-review-cycle-sources]]
- 포트폴리오: [[portfolio-current]]
