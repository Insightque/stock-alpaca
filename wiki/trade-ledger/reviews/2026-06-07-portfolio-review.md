---
id: 2026-06-07-portfolio-review
review_type: waiting
reviewed_at: 2026-06-06T21:23:41Z
paper: true
decision_date: 2026-06-05/2026-06-06
entry_date: multiple
exit_date:
---

# 2026-06-07 analyst review cycle

## 요약 판단

- 결론: 대기 상태다. `2026-06-06` 미국 정규장 close 기준 새로 maturity에 도달한 `1D/5D/20D` review는 없었고, 이번 run의 핵심은 read-only reconciliation, review backlog scan, open-position catalyst monitor, skipped recommendation 재점검이다.
- 현재 해석: `AVGO`의 post-earnings drawdown은 여전히 경계 구간이지만 `2026-06-06 03:37 KST` trim 이후 추가 행동 근거는 아직 부족하다. `JPM`과 `SO`는 첫 close 관찰이 나쁘지 않았지만 둘 다 공식 1D horizon 전이므로 `회고 대기`를 유지한다. `NOK`는 add-block 해제 근거가 없고 `2026-06-18` 20D까지 기다리는 편이 맞다.
- 정책 반영 여부: 보류. Alpaca `portfolio_history`가 3회 연속 cancelled였고, SEC EDGAR는 current-run query가 cancelled, Alpha Vantage는 first non-PING call이 provider-error, `fred/firecrawl`은 namespace 미노출 `wrapper_error`라 active rule 승격 근거가 없다.

## Reconciliation

| 항목 | 값 |
| --- | --- |
| Paper mode | `ALPACA_PAPER_TRADE=true` |
| Alpaca clock | `2026-06-06 17:21 ET` closed, next open `2026-06-08 09:30 ET` |
| Account status | ACTIVE |
| Portfolio value | `98,156.33 USD` |
| Cash | `29,947.79 USD` |
| Buying power | `294,276.14 USD` |
| Long market value | `68,208.54 USD` |
| Open US equity orders | 0 |
| Position count | 33 |
| Recent FILL scope | `2026-06-04T00:00:00Z` 이후 direct `FILL` ledger 확인 성공 |
| Portfolio history | cancelled gap after initial + 2 retries |
| Orders submitted/replaced/cancelled/closed by this workflow | 0 / 0 / 0 / 0 |

## Review-due scan

`2026-06-05 ET` fill cohort `JPM/SO/PFE/AMZN/COP/SLB/NVDA/V/AAPL/PLTR/FCX/WMT/BAC`의 1D는 `2026-06-08` 미국 정규장 close 이후에야 닫을 수 있다. 따라서 이번 run에서는 decision-quality를 새로 확정하지 않고 대기 상태를 정리하는 데 집중했다.

현재 add-blocking review는 `NOK` 하나뿐이다. `NOK` 20D는 `2026-06-18` 미국 정규장 close 이후까지 남아 있고, 이번 close에서 추가적인 unblock 증거는 없었다.

## Open-position catalyst review

| Symbol | 현재 상태 | 회고 |
| --- | --- | --- |
| AVGO | 보유 12주, avg entry `414.940833 USD`, `2026-06-05` close/current `385.73 USD`, 미실현 `-7.04%` | `2026-06-05 ET` close 기준 drawdown은 여전히 크다. 다만 이미 4주 trim으로 size reduction을 했고, 이번 run에는 새 due horizon이나 fresh filing confirmation이 없어 추가 규칙 승격 없이 `post-earnings risk watch`로만 유지한다. |
| JPM | 보유 1주, avg entry `311.81 USD`, `2026-06-05` close `312.38 USD`, 미실현 `+0.18%` | first close 자체는 financials diversifier thesis에 우호적이지만 공식 1D horizon은 아직 아니다. `2026-06-08` 미국 정규장 close 이후에만 interim verdict를 내린다. |
| SO | 보유 5주, avg entry `92.696 USD`, `2026-06-05` close `92.64 USD`, 미실현 `-0.10%` | 반복된 weak-to-neutral review 이력에도 `2026-06-05` shock day에서는 `XLU`와 함께 상대 방어가 나왔다. 하지만 이것만으로 utilities negative narrative를 뒤집지는 않는다. `회고 대기`를 유지한다. |
| NOK | 보유 402주, avg entry `15.044527 USD`, `2026-06-05` close/current `14.35 USD`, 미실현 `-4.42%` | overheat unwind가 계속 진행 중이고, 기존 가설인 `existing-position-breakout-add-penalty`를 철회할 근거가 없다. 20D due 전까지 add-block 유지가 맞다. |

## Skipped recommendation review

| 대상 | 당시 이유 | 현재 회고 |
| --- | --- | --- |
| JNJ `2026-06-05 04:51 KST` close-race cancel | actual submit timestamp가 `2026-06-04 16:02:59 ET`로 밀려 market-close hard gate 복구 | `2026-06-05` close `232.71 USD`는 planned limit `229.25 USD` 대비 `+1.51%`라 결과만 보면 miss다. 그래도 close-after-submit 허용보다 규율 유지가 더 중요했으므로 policy miss로 보지 않는다. |
| NKE `2026-06-06 04:51 KST` close-race cancel | regular close 이후 submit되어 즉시 cancel | `2026-06-05` close `42.98 USD`는 canceled limit `43.20 USD`보다 `-0.51%`라 miss가 아니다. 복구 cancel이 맞았다. |
| CVX `2026-06-06 02:51 KST` same-session cancel | stale/open-order lifecycle 정리 후 no fill | `2026-06-05` close `187.31 USD`는 planned limit `187.68 USD`보다 `-0.20%`라 강한 missed opportunity는 아니다. |
| NEE `2026-06-06 02:31 KST` same-session cancel | stale/open-order lifecycle 정리 후 no fill | `2026-06-05` close `85.825 USD`는 planned limit `85.47 USD`보다 `+0.42%`지만, lifecycle cleanup 직후 재진입 회피를 policy miss로 볼 정도는 아니다. |

## Provider coverage와 data gaps

- Alpaca core는 account, positions, orders, fill ledger, snapshots까지는 usable이었다. 다만 `get_portfolio_history`는 initial + 2 retries 모두 cancelled였다.
- SEC EDGAR는 current-run `get_insider_summary(AVGO, 30)`가 initial + 2 retries 모두 cancelled라 filing-grounded refresh를 완료하지 못했다.
- Alpha Vantage는 required `PING` health check는 통과했지만 첫 non-PING `EARNINGS(AVGO)` call이 daily-rate-limit payload를 반환해 `provider_error`로 종료했다.
- `fred`와 `firecrawl`은 callable namespace가 이 runtime에 노출되지 않아 `wrapper_error`로 분류했다.
- Yahoo Finance는 `AVGO/JPM/SO` news와 `JPM` recommendations breadth를 제공해 open-position context 보강에는 usable했다.

## 잘한 점

- 이번 run은 order mutation 없이 계좌, 포지션, 체결, 취소 상태를 다시 맞췄고 open orders 0건을 재확인했다.
- `새 due 없음`을 명확히 기록해 회고와 가격 모니터링을 섞지 않았다.
- `AVGO/JPM/SO/NOK`를 서로 다른 상태의 open-position 사례로 분리해 적었다.

## 부족했던 점

- account-level drawdown path를 확인할 `portfolio_history`가 여전히 비었다.
- SEC/Alpha/FRED/Firecrawl 공백 때문에 filing/macro/IR 보강이 current-run evidence로는 약하다.
- review backlog는 구조상 줄었지만, `2026-06-05 ET` fill cohort 13개가 다음 미국 정규장 close 이후 한 번에 1D review로 몰릴 예정이다.

## 정책학습 판단

- `post-earnings validation adds must stay small` 가설은 `AVGO` 사례 때문에 계속 유지한다. 다만 오늘 새로 닫힌 horizon이 없어서 active rule로 승격하지 않는다.
- `shock-day defensive resilience` 관찰은 `SO`와 `XLU` 쪽에 남지만, 단일 close 기준이라 아직 가설 단계다.
- `existing-position-breakout-add-penalty`는 `NOK` add-block을 유지할 만큼은 유효하지만, 오늘 새 evidence가 없어 정책 문서 업데이트로 연결하지 않는다.

## 다음 review due

- `2026-06-05 ET` fill cohort 1D: `JPM`, `SO`, `PFE`, `AMZN`, `COP`, `SLB`, `NVDA`, `V`, `AAPL`, `PLTR`, `FCX`, `WMT`, `BAC`는 `2026-06-08` 미국 정규장 close 이후 평가 가능하다.
- `NOK` 20D add-block review는 `2026-06-18` 미국 정규장 close 이후다.
- 그 전까지는 read-only monitoring만 수행하고, 이번 run에서는 주문 mutation이 없다.

## 연결 문서

- 원천 자료: [[2026-06-07-0623-analyst-review-cycle-sources]]
- Run manifest: `wiki/evidence-store/run-manifests/2026-06-07-0623-analyst-review-cycle.json`
- 이전 회고: [[2026-06-06-portfolio-review]], [[2026-06-05-portfolio-review]], [[2026-06-04-portfolio-review]]
