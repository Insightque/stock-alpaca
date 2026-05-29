# 2026-05-29 정책 학습 및 아키텍처 전면 점검

## 결론

현재까지의 정책 개선 방향은 타당하다. 매도 판단이 매수 budget이나 entry window에 종속되던 위험을 줄이고, `sell_candidate_diagnostics`, validation lifecycle, rotation trim, target band를 추가한 것은 buy-only drift를 학습 가능한 형태로 바꾸는 데 필요했다.

다만 구조상 남은 핵심 문제는 risk gate가 정상적으로 주문을 막은 run이 runtime failure 알림으로 표시되는 점, run manifest schema drift가 validator에서 잡히지 않는 점, sell 진단이 아직 정량 학습 데이터로 충분히 강제되지 않는 점이다.

## 주요 발견사항

1. High - risk blocker와 runtime failure가 섞인다.
   - 2026-05-29 23:11 run은 Alpaca core/universe/MCP는 통과했고 BAC/SPY open order age 때문에 `risk_open_order_lifecycle`에서 의도적으로 차단됐다.
   - 하지만 wrapper는 nested Codex non-zero exit을 모두 `failed`로 알림 처리한다. 이러면 정책 학습 원장에서 "정상적인 보호 차단"과 "런타임 장애"가 섞인다.
   - 근거: `scripts/run-hourly-autopilot-codex.sh`, `scripts/send-openclaw-autopilot-update.py`, `wiki/current-runs/daily/2026-05-29-2311-hourly-autopilot.md`.

2. High - run manifest schema drift가 자동 검증되지 않는다.
   - 최신 23:11 manifest는 `schema_version=1.0`인데 schema는 `1.1`, `1.2`, `1.3`만 허용한다.
   - universe/MCP validator는 PASS했지만 manifest schema 자체 검증이 없어서 drift가 통과했다.
   - 근거: `wiki/evidence-store/run-manifests/2026-05-29-2311-hourly-autopilot.json`, `harness/run-manifest.schema.json`, `scripts/check-mcp-coverage.py`.

3. Medium - sell 진단은 기록되지만 아직 학습 강제력이 약하다.
   - workflow는 매 completed run에 `sell_candidate_diagnostics`를 요구하지만, order-plan/manifest schema의 root required에는 들어가 있지 않다.
   - 따라서 향후 run이 진단을 누락해도 schema/risk validator만으로는 놓칠 수 있다.
   - 근거: `harness/workflows/hourly-autopilot.md`, `harness/order-plan.schema.json`, `harness/run-manifest.schema.json`.

4. Medium - sell 후보의 정량값이 아직 학습 feature로 부족하다.
   - 23:11 run의 PLTR/RGTI/AMD 진단은 유용한 감시 기록이지만 `expected_excess_return_20d_pct`, `relative_to_spy_20d_pct`가 0으로 기록되어 실제 회고 feature로는 약하다.
   - 값이 없으면 `null`과 gap reason으로 남기거나, 계산 가능하면 동일한 방법으로 산출해야 한다.

5. Medium - stale order cleanup 이후 최종 reconciliation 의미가 불명확하다.
   - cleanup은 SPY cancel attempt를 pass로 남겼지만 같은 artifact와 Alpaca core preflight는 SPY를 여전히 open `new`로 기록했다.
   - 새 주문을 막은 것은 맞지만, 다음 run에서 해결됐는지, cancel accepted 후 지연인지, stale state인지가 더 명확히 분류되어야 한다.

6. Low - 운영 산출물과 정책 commit이 분리된 상태다.
   - 정책 hardening commit은 존재하지만 23:11 runtime artifacts는 아직 working tree에 남아 있다.
   - 실패 알림으로 autopush가 멈춘 결과로 보이며, 다음 정리/commit 때 정책 변경과 runtime 산출물이 섞이지 않게 주의가 필요하다.

## 좋은 점

- `risk_trim_policy`가 buy entry window와 buy budget에서 분리됐다.
- 23:11 run에서 실제로 매수 전 sell/trim 진단이 먼저 수행됐다.
- Alpha Vantage `provider_error`는 nonblocking provider gap으로 유지됐고, SEC EDGAR/FRED/Firecrawl/Yahoo로 MCP strict 기준은 충족했다.
- risk validator가 stale/open order lifecycle을 막아 중복 주문 확대를 방지했다.

## 권장 후속 조치

1. wrapper/notification에 `blocked` 또는 `completed_blocked` 상태를 추가해 risk FAIL no-submit을 runtime failure와 분리한다.
2. run manifest schema validator를 추가하고 scheduled run 완료 조건에 포함한다.
3. hourly-autopilot submit-mode 산출물에는 `sell_candidate_diagnostics`와 `validation_lifecycle`를 필수화한다.
4. sell 진단의 expected/relative metric 산출 기준을 정하거나, 산출 불가 시 gap reason을 필수화한다.
5. stale cleanup artifact에 cancel attempt, final open-order state, reconciliation confidence를 분리 기록한다.

## 검증

- `PATH=/usr/local/bin:$PATH python3 -m unittest discover tests` PASS, 121 tests.
- `PATH=/usr/local/bin:$PATH python3 scripts/check-policy-source-of-truth.py` PASS.
- `PATH=/usr/local/bin:$PATH python3 scripts/check-universe-coverage.py --strict wiki/evidence-store/run-manifests/2026-05-29-2311-hourly-autopilot.json` PASS.
- `PATH=/usr/local/bin:$PATH python3 scripts/check-mcp-coverage.py --strict wiki/evidence-store/run-manifests/2026-05-29-2311-hourly-autopilot.json` PASS.
- `PATH=/usr/local/bin:$PATH python3 scripts/check-risk-policy.py --json wiki/trade-ledger/orders/2026-05-29-2311-hourly-autopilot.json` FAIL. BAC/SPY open-order age가 lifecycle 30분 한도를 초과한 의도된 hard gate다.

주문 제출, 취소, 계좌 변경은 수행하지 않았다.
