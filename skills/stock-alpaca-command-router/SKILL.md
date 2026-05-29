---
name: stock-alpaca-command-router
description: Route Korean stock-alpaca user commands to the correct harness workflow. Use when the user gives short Korean trading/research commands such as 오늘 분석해줘, 포트폴리오 점검해줘, paper 주문까지 실행해줘, 자동 운영, or historical simulation/review requests.
---

# Stock Alpaca Command Router

Use this skill to classify the user's intent before running a stock-alpaca workflow.

## Boundary

This skill routes the request. It does not validate risk, decide provider coverage, format notifications, or submit orders. After routing, hand off to the narrower operational skill.

## Route

1. Work from the stock-alpaca repo root. If the current directory is not the repo, use `/Users/insightque/stock-alpaca` when it exists.
2. Read `AGENTS.md` and `harness/simple-commands.md` before interpreting the command.
3. Map exact or near-exact Korean commands to the workflow named in `harness/simple-commands.md`.
4. Treat requests without explicit `주문`, `매수`, `매도`, `실행`, or `submit` as no-submit analysis.
5. For custom variants, preserve the same safety gates and record the deviation in `wiki/log.md`.

## Order Intent

- `오늘 분석해줘`, `관심종목 분석해줘`, ticker analysis, portfolio checks, rebalance planning, historical simulations, and wiki cleanup do not submit orders by default.
- `paper 주문까지 실행해줘` can submit only from a validated order plan or submit-mode rebalance workflow.
- `시간 단위로 자동 운영해줘` and `자동으로 매입/매도해줘` use the hourly autopilot wrapper, not ad hoc scripts.
- `장외 자동 운영해줘` uses the after-hours autopilot workflow and separate after-hours policy profile.

## Handoff

After routing, trigger the narrower skill for the task:

- Order or submit intent: use `stock-alpaca-paper-trading-safety` and `stock-alpaca-risk-order-plan`.
- Autopilot or scheduler: use `stock-alpaca-autopilot-runtime`.
- Research/current-market coverage: use `stock-alpaca-mcp-research-gate`.
- Wiki mutation: use `stock-alpaca-wiki-ledger`.
- Trade review or policy learning: use `stock-alpaca-review-policy-learning`.
