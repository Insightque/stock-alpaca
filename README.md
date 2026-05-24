# Alpaca MCP Paper Trading Harness

## 한국어 버전

이 저장소는 Alpaca 공식 MCP 서버를 paper trading 모드로 사용하고, Codex를 여러 역할의 trading harness처럼 운용하기 위한 작업공간입니다. 목적은 자동 수익을 약속하는 것이 아니라, 추천과 결과를 기록하고 회고하면서 정책을 점진적으로 개선하는 것입니다.

핵심 루프는 블랙박스 RL 모델이 아니라 reinforcement-style 피드백 루프입니다. 에이전트가 paper-only 추천을 만들고, 당시 알 수 있었던 정보와 근거를 저장한 뒤, 이후 1D/5D/20D 성과를 검토합니다. 충분한 증거가 쌓인 정책 신호만 다음 추천 정책에 반영합니다.

모든 종목 리서치, 추세 분석, 배분 메모, 주문 계획, 시뮬레이션 리뷰, 정책 교훈, 실행 결과는 `wiki/` 아래 llm-wiki 형태로 보관합니다.

### 학습 루프

1. 보유 종목, watchlist, wiki 이력, 사용자가 지정한 티커로 후보군을 구성합니다.
2. 기준 시점의 시장 데이터, 뉴스, 실적, 공시, 매크로 맥락, 포트폴리오 제약을 수집합니다.
3. paper-only 추천과 dry-run 주문 계획을 만듭니다.
4. 이후 1D/5D/20D 성과를 SPY, QQQ, 섹터 벤치마크와 비교합니다.
5. 맞았던 점, 틀렸던 점, 강화/약화/검증 유지할 정책 신호를 기록합니다.

이 프로젝트는 수익을 보장하지 않습니다. 목표는 paper trading, 미래 정보 누출 없는 과거 시뮬레이션, 정책 개선을 위한 절제된 피드백 시스템입니다.

### MCP 설정

1. `.env` 파일을 엽니다.
2. Alpaca paper trading 키를 `ALPACA_API_KEY`, `ALPACA_SECRET_KEY`에 입력합니다.
3. VS Code를 재시작하거나 MCP 서버 목록에서 `alpaca` 서버를 재시작합니다.

`.env`에는 `ALPACA_PAPER_TRADE=true`가 설정되어 있어야 합니다. 이 값이 없거나 `true`가 아니면 trading workflow는 중단되어야 합니다.

선택형 리서치 MCP는 `.env.example`과 `.vscode/mcp.json`에 정리되어 있습니다. 키가 없으면 해당 MCP 실패를 raw source의 데이터 공백으로 기록하고, 사용 가능한 원천으로 계속 진행합니다.

### 간단한 Codex 명령

Codex에게 아래처럼 짧게 말하면 됩니다.

- `오늘 분석해줘`
- `관심종목 분석해줘`
- `AAPL 분석해줘`
- `포트폴리오 점검해줘`
- `리밸런싱 계획 짜줘`
- `paper 주문까지 실행해줘`
- `거래 후 점검해줘`
- `위키 정리해줘`

Codex는 `AGENTS.md`를 따르고, `harness/simple-commands.md`에서 명령을 해석한 뒤, `harness/workflows/`의 맞는 워크플로우를 실행합니다.

에이전트에게 업무를 지시하는 예시는 `harness/agent-tasking-guide.md`를 참고하세요.

### 안전 모델

- Paper trading만 허용합니다.
- 미국 주식/ETF만 허용합니다.
- Long-only, whole-share, day limit order만 허용합니다.
- 포트폴리오 투자 비중은 최대 80%, 현금 보유는 최소 20%, 단일 티커 비중은 최대 15%입니다.
- `medium-risk-v1.1` 정책으로 theme, factor, speculative, correlated-cluster, liquidity, spread, source-confidence 검사를 강제합니다.
- 한 번의 run에서 신규 주문은 최대 10개입니다.
- 주문 계획은 반드시 `scripts/check-risk-policy.py`를 통과해야 합니다. CI나 agent-readable 출력이 필요하면 `--json`을 사용합니다.
- 신규 주문 계획은 `harness/order-plan.schema.json`을 따라야 하며 account, market, quote, asset 확인 원천을 인용해야 합니다.
- 주문 제출은 Alpaca MCP를 통해서만 가능합니다. Alpaca trading REST endpoint를 직접 호출하는 custom trading 코드는 금지합니다.
- 과거 1년 정책 검증은 `harness/workflows/one-year-daily-simulation.md`를 사용하며, 각 기준일을 독립적으로 시뮬레이션합니다.

주문 계획 검증:

```bash
python3 scripts/check-risk-policy.py harness/examples/order-plan.example.json
python3 scripts/check-risk-policy.py --json harness/examples/order-plan.example.json
```

### Wiki 구조

- `wiki/evidence-store/sources/`: 수정하지 않는 원천 캡처 자료.
- `wiki/research-notes/tickers/`: 종목별 thesis와 추세 페이지.
- `wiki/research-notes/portfolio/`: 다음 판단에 재사용할 포트폴리오 해석과 배분 메모.
- `wiki/current-runs/daily/`: 현재 계좌와 현재 시장을 대상으로 실행한 일일 trading workflow 결과만 저장합니다.
- `wiki/research-notes/analyses/`: 종목 간 비교, 매크로 메모, 제안서, MCP/source 품질 감사.
- `wiki/backtest-runs/`: 과거 기준 실험, 모의 의사결정, 사후 검증 결과.
- `wiki/backtest-runs/decisions/`: 기준 시점 이후 정보를 쓰지 않는 과거 모의 의사결정.
- `wiki/backtest-runs/results/`: 미래 결과를 쓰는 모든 백테스트 결과. 개별 1D/5D/20D 회고와 1년 정책 검증 모두 여기에 둡니다.
- `wiki/trade-ledger/orders/`: 실제 paper 주문과 dry-run 주문 계획 장부.
- `wiki/trade-ledger/positions/`: 실제 paper 포지션과 계좌 상태 스냅샷.
- `wiki/trade-ledger/reviews/`: 실제 paper 거래의 사후 회고.
- `wiki/policy-book/`: 앞으로 적용할 추천/리스크/실행 규칙.
- `wiki/evidence-store/run-manifests/`: machine-readable run manifest.
- `wiki/index.md`: 콘텐츠 인덱스.
- `wiki/log.md`: append-only 활동 로그.

### 선택형 스케줄러

기본 운용 방식은 Codex 수동 실행입니다. 선택형 macOS launchd 파일은 `scheduler/`에 있습니다.

---

## English Version

This repository is a Codex-first paper-trading harness built around Alpaca's official MCP server. Its goal is not to promise automated profits, but to record recommendations, review outcomes, and improve the recommendation policy over time.

The core loop is reinforcement-style rather than a black-box RL model. The agent produces paper-only recommendations, records the information available at decision time, reviews later 1D/5D/20D outcomes, assigns lessons to policy signals, and updates future recommendation policy only when evidence accumulates.

All ticker research, trend analysis, allocation notes, order plans, simulation reviews, policy lessons, and execution outcomes are stored in an llm-wiki under `wiki/`.

### Learning Loop

1. Build a candidate universe from holdings, watchlists, wiki history, and user-specified tickers.
2. Collect as-of market data, news, earnings, filings, macro context, and portfolio constraints.
3. Produce paper-only recommendations and dry-run order plans.
4. Review later 1D/5D/20D outcomes against SPY, QQQ, and sector benchmarks.
5. Record what worked, what failed, and which policy signals should be strengthened, weakened, or kept under validation.

This project is not a promise of profitable trading. It is a disciplined feedback harness for paper trading, leak-free historical simulation, and policy improvement.

### MCP Setup

1. Open `.env`.
2. Fill `ALPACA_API_KEY` and `ALPACA_SECRET_KEY` with your Alpaca paper trading keys.
3. Restart VS Code or restart the `alpaca` MCP server from the MCP server list.

`ALPACA_PAPER_TRADE=true` must be set in `.env`. If it is missing or not `true`, trading workflows should stop.

Optional research MCPs are listed in `.env.example` and `.vscode/mcp.json`. If their keys are absent, record the MCP failure as a data gap in the raw source note and continue with available sources.

### Simple Codex Commands

You can talk to Codex with short commands such as:

- `오늘 분석해줘`
- `관심종목 분석해줘`
- `AAPL 분석해줘`
- `포트폴리오 점검해줘`
- `리밸런싱 계획 짜줘`
- `paper 주문까지 실행해줘`
- `거래 후 점검해줘`
- `위키 정리해줘`

Codex follows `AGENTS.md`, interprets user commands through `harness/simple-commands.md`, and runs the matching workflow under `harness/workflows/`.

See `harness/agent-tasking-guide.md` for examples of assigning work to agents.

### Safety Model

- Paper trading only.
- US stocks/ETFs only.
- Long-only, whole-share, day limit orders only.
- Maximum 80% invested, minimum 20% cash reserve, maximum 15% per ticker.
- Theme, factor, speculative, correlated-cluster, liquidity, spread, and source-confidence checks are enforced by `medium-risk-v1.1`.
- Maximum 10 new orders per run.
- Orders must pass `scripts/check-risk-policy.py`; use `--json` for CI and agent-readable results.
- New order plans must conform to `harness/order-plan.schema.json` and cite source refs for account, market, quote, and asset checks.
- Orders must be submitted through Alpaca MCP only. Custom code must never call Alpaca trading REST endpoints directly.
- Historical one-year policy checks use `harness/workflows/one-year-daily-simulation.md` and run each as-of day independently.

Order-plan validation:

```bash
python3 scripts/check-risk-policy.py harness/examples/order-plan.example.json
python3 scripts/check-risk-policy.py --json harness/examples/order-plan.example.json
```

### Wiki Structure

- `wiki/evidence-store/sources/`: immutable captured sources.
- `wiki/research-notes/tickers/`: ticker thesis and trend pages.
- `wiki/research-notes/portfolio/`: reusable portfolio interpretation and allocation notes.
- `wiki/current-runs/daily/`: daily trading workflow outputs for the current account and current market only.
- `wiki/research-notes/analyses/`: cross-ticker comparisons, macro notes, proposal writeups, and MCP/source-quality audits.
- `wiki/backtest-runs/`: historical experiments, simulated decisions, and outcome validation.
- `wiki/backtest-runs/decisions/`: point-in-time historical decisions that exclude future outcome data.
- `wiki/backtest-runs/results/`: all backtest results that use future outcomes, including individual 1D/5D/20D reviews and one-year policy validations.
- `wiki/trade-ledger/orders/`: actual paper orders and dry-run order plans.
- `wiki/trade-ledger/positions/`: actual paper positions and account-state snapshots.
- `wiki/trade-ledger/reviews/`: post-trade reviews for actual paper trades.
- `wiki/policy-book/`: recommendation, risk, and execution rules to apply going forward.
- `wiki/evidence-store/run-manifests/`: machine-readable run manifests.
- `wiki/index.md`: content index.
- `wiki/log.md`: append-only activity log.

### Optional Scheduler

The default operating mode is manual execution through Codex. Optional macOS launchd files are available under `scheduler/`.
