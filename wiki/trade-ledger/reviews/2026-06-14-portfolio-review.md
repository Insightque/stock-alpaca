---
id: 2026-06-14-portfolio-review
review_type: interim
reviewed_at: 2026-06-13T21:23:31Z
paper: true
decision_date: 2026-06-12/2026-06-13
entry_date: multiple
exit_date: partial
---

# 2026-06-14 analyst review cycle

## 요약 판단

- 결론: live Alpaca clock이 `2026-06-13 17:22 ET` 토요일 closed 상태로 고정돼 있었고, 지난 cycle 이후 새로운 미국 정규장 close가 없었다. 따라서 이번 cycle은 새 `1D/5D/20D` closeout 추가 없이 backlog 유지, open-position monitor, skipped recommendation 재점검 중심으로 닫았다.
- `RGTI`의 `2026-06-12 ET` regular-session trim 12주는 여전히 첫 `1D` horizon 대기 상태이며, due date는 `2026-06-15` 미국 정규장 close 이후다.
- `AAPL`과 `AVGO`는 각각 미실현 약 `-3.96%`, `-9.75%`로 여전히 판단 보수 구간이다. `NOK`는 `JP Morgan Overweight/PT 21` 보강에도 add-block을 유지한다.
- skipped recommendation 쪽에서는 `FCX` missed upside와 `NEE` flat tape가 그대로 남아 있지만, 토요일 clock 기준 새 가격 진행이 없어서 전일 결론을 바꿀 근거는 생기지 않았다.
- 정책 반영 여부: 없음. 새 closeout 표본이 없고 `portfolio_history`는 3회 연속 cancelled, `sec-edgar`도 callable surface partial 상태에서 probe가 cancelled라 policy-book 증거 임계치를 충족하지 못했다.

## Reconciliation

| 항목 | 값 |
| --- | --- |
| Paper mode | `ALPACA_PAPER_TRADE=true` |
| Alpaca clock | `2026-06-13 17:22 ET` closed, next open `2026-06-15 09:30 ET` |
| Account status | ACTIVE |
| Portfolio value | `100,415.12 USD` |
| Cash | `31,950.34 USD` |
| Buying power | `302,843.86 USD` |
| Long market value | `68,464.78 USD` |
| Open US equity orders | 0 |
| Position count | 33 |
| Recent fill scope | `2026-06-12T00:00:00Z` 이후 direct `FILL` ledger usable |
| New fills since prior analyst cycle | 없음. `PFE/AVGO/RGTI` 3건만 유지 |
| Portfolio history | initial + retry 1 + retry 2 모두 `cancelled` |
| Orders submitted/replaced/cancelled/closed by this workflow | 0 / 0 / 0 / 0 |

## Due horizon scan

- 새 미국 정규장 close가 없어서 이번 cycle에 새로 닫힌 `1D/5D/20D` horizon은 없다.
- `review-due-index`는 `pending_1d_count=1`, `pending_5d_count=16`, `pending_20d_count=1`로 유지했다.
- `blocked_add_symbols`는 `NOK` 단일 심볼 유지다.

## Open-position monitor

| Symbol | 현재 상태 | 해석 |
| --- | --- | --- |
| AAPL | `5주`, avg entry `303.136 USD`, current `291.13 USD`, 미실현 `-3.96%` | Alpha Vantage `EARNINGS` 기준 latest quarter `reportedDate=2026-04-30`, `reportedEPS=2.01`, `estimatedEPS=1.94`, `surprisePercentage=+3.61%`였지만, Yahoo Finance 기사 흐름은 AI spending restraint 긍정과 pricing/supply-chain 부담이 병존한다. 토요일 clock 기준 새 tape 개선이 없어 `mega-cap quality averaging-down`은 계속 관찰 가설이다. |
| AVGO | `4주`, avg entry `423.3625 USD`, current `382.07 USD`, 미실현 `-9.75%` | staged de-risking 뒤에도 recovery confirmation은 부족하다. Friday close 대비 새 regular-session 데이터가 없어 `post-earnings staged de-risking` 해석을 유지한다. |
| NOK | `402주`, avg entry `15.044527 USD`, current `14.80 USD`, 미실현 `-1.63%` | Yahoo Finance recommendation summary의 `2026-06-12 JP Morgan Overweight / PT 21`는 우호적이지만, 미국 정규장 추가 확인 없이 lifecycle add-block을 풀지는 않는다. 다음 정식 review는 `2026-06-18` 미국 정규장 close 이후다. |
| RGTI | `37주`, avg entry `25.569583 USD`, current `20.98 USD`, 미실현 `-17.95%` | `2026-06-12 ET` trim 12주 이후 residual speculative sleeve 해석을 유지한다. 첫 `1D` closeout은 주말을 지나 `2026-06-15` 미국 정규장 close에 닫힌다. |

## Skipped recommendation review

| 대상 | 당시 이유 | 현재 회고 |
| --- | --- | --- |
| `2026-06-13-0451` regular-session `FCX` 신규 buy | `review_backlog_pending_1d_count=14`로 backlog throttle 활성 | current `68.41 USD`로 hindsight상 missed upside는 남아 있다. 다만 live Alpaca clock이 토요일 `2026-06-13 17:22 ET`라 새 closeout 없이 throttle 비용만 추가 확인된 상태다. 다음 regular-session close 뒤에도 relative strength가 유지되는지 봐야 한다. |
| `2026-06-13-0451` regular-session `NEE` 신규 buy | `review_backlog_pending_1d_count=14`로 backlog throttle 활성 | current `85.99 USD`로 급한 missed upside는 아니다. hindsight 비용은 `FCX`보다 작고, backlog 우선순위 자체를 뒤집을 정도는 아니다. |
| `2026-06-14-0611` after-hours `QQQ/MSFT` | quote freshness stale | 미국 정규장 새 close가 없어서 전일 판단이 그대로 유지된다. stale overnight quote를 무시하고 진입하지 않은 결정이 오늘 새 반증을 남기지는 않았다. |

## Provider coverage와 data gaps

- Alpaca core는 `get_clock`, `get_account_info`, `get_all_positions`, `get_orders`, `get_account_activities`, `get_watchlists`가 모두 usable이었다.
- Alpaca `get_portfolio_history(period=1M,timeframe=1D)`는 initial + 2 retries 모두 `cancelled`였다. account-level equity path와 exact portfolio MFE/MAE는 계속 current-run gap이다.
- Alpha Vantage는 user-required health check `TOOL_LIST -> TOOL_GET(PING) -> TOOL_CALL(PING,{})`를 통과했고, 직후 `TOOL_GET(EARNINGS)` 다음 `TOOL_CALL(EARNINGS,{symbol:"AAPL"})`도 성공했다.
- SEC EDGAR는 현재 runtime에서 issuer-level filing fetch surface가 노출되지 않았고, exposed tool `get_recommended_tools(form_type=4)` probe도 cancelled였다. 이번 cycle filing overlay는 partial gap으로 남긴다.
- `fred`와 `firecrawl`은 registered callable namespace가 이 runtime에 노출되지 않아 둘 다 `gap_category=wrapper_error`로 기록한다. shell/curl probe는 수행하지 않았다.
- Yahoo Finance는 `AAPL` news와 `NOK` upgrades/downgrades summary 보강에 usable이었다.

## 정책학습 판단

- 새 due horizon closeout이 없어 active rule 승격이나 완화는 없다.
- `review_backlog_throttle`는 여전히 운영상 유효하지만, `FCX` missed upside 비용은 추가 누적 표본으로 계속 추적한다.
- `mega-cap quality averaging-down`과 `post-earnings staged de-risking`은 둘 다 새 정규장 데이터 전까지 기존 판단을 유지한다.

## 다음 review due

- `RGTI` `2026-06-12 ET` trim 12주 `1D`: `2026-06-15` 미국 정규장 close 이후.
- `2026-06-10 ET` fill cohort `5D`: `WMT/AVGO/RGTI/BAC/PFE/XOM/JNJ/COP/SLB/AMZN/FCX/NEE/NKE/MSFT`는 `2026-06-17` 미국 정규장 close 이후.
- `NOK` `20D` add-block review: `2026-06-18` 미국 정규장 close 이후.
- `2026-06-11 ET` after-hours trim cohort `5D`: `PFE/AVGO`는 `2026-06-19` 미국 정규장 close 이후.

## 연결 문서

- 원천 자료: [[2026-06-14-0623-analyst-review-cycle-sources]]
- Run manifest: `wiki/evidence-store/run-manifests/2026-06-14-0623-analyst-review-cycle.json`
- 이전 회고: [[2026-06-13-portfolio-review]], [[2026-06-12-portfolio-review]]
