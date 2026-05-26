# Workflow: Analyst Review Cycle

Use this for scheduled analyst-style review of paper trades, open positions, skipped recommendations, and policy-learning signals.

## Goal

Repeatedly review whether paper buy/sell decisions were high-quality decisions based on the information available at the time. Record lessons without hindsight contamination, and only promote policy changes when evidence accumulates.

## Cadence

- Daily after US market close: post-trade reconciliation and review-due scan.
- 1D after fill/recommendation: interim decision-quality check.
- 5D after fill/recommendation: follow-through and adverse-move check.
- 20D after fill/recommendation or at close: full review.
- Weekly after Friday close: portfolio-level analyst review.
- Monthly: policy-learning summary, including evidence counts and rejected hypotheses.

## Required Inputs

- Alpaca MCP account, positions, orders, activities, portfolio history, and current market data.
- Relevant order plans in `wiki/trade-ledger/orders/`.
- Reports in `wiki/current-runs/daily/`.
- Source notes in `wiki/evidence-store/sources/`.
- Ticker notes in `wiki/research-notes/tickers/`.
- Existing reviews in `wiki/trade-ledger/reviews/`.
- `wiki/policy-book/recommendation-policy.md`
- `harness/recommendation-policy.yaml`

## Procedure

1. Read `AGENTS.md`, recent `wiki/log.md`, `harness/workflows/post-trade.md`, and `harness/workflows/trade-review.md`.
2. Confirm paper mode. This workflow never submits orders.
3. Use Alpaca MCP to reconcile:
   - current account value and cash
   - open orders
   - filled/canceled/rejected orders
   - positions
   - portfolio history when available
   - Retry transient Alpaca MCP timeout, cancellation, DNS, or network failures up to 2 times before declaring a data gap.
   - If reconciliation remains incomplete, write a data-gap review and do not mutate policy from incomplete evidence.
4. Identify review candidates:
   - newly filled orders with no review marker
   - open positions older than 1D/5D/20D review horizons
   - closed positions
   - positions with material unrealized P/L, adverse movement, thesis break, or major catalyst update
   - skipped high-ranked recommendations whose later performance suggests a policy miss
5. For each due item, reconstruct the original decision:
   - original recommendation/rank
   - source refs and MCP coverage
   - quote and spread state
   - risk gate result
   - sizing and entry/exit rationale
   - stated thesis and risks
6. Evaluate actual outcomes:
   - current or exit price
   - realized/unrealized P/L
   - 1D/5D/20D return when available
   - excess return versus `SPY`, `QQQ`, and relevant sector/theme ETF when available
   - maximum favorable/adverse move when available
7. Write reviews under `wiki/trade-ledger/reviews/`.
8. Update related ticker pages with a dated `회고 기록` entry.
9. Update policy only when the lesson is evidence-backed:
   - one-off result -> hypothesis
   - repeated pattern -> policy proposal
   - statistically or operationally useful repeated pattern -> active rule
10. Append `wiki/log.md` with review status, policy changes, and pending review dates.
11. Let the scheduled shell wrapper commit and push generated artifacts after the workflow exits successfully. Do not run ad hoc git commands inside this workflow unless explicitly requested.

## Policy-Learning Rules

- Profit does not automatically mean the decision was good.
- Loss does not automatically mean the decision was bad.
- Separate decision quality from outcome luck.
- Do not rewrite original recommendations, source notes, or order plans.
- Use later prices only in review documents.
- Keep policy changes small and traceable to review links.

## Stop Conditions

- Alpaca MCP unavailable and local artifacts are insufficient for a truthful review.
- Any workflow step would submit, replace, cancel, or close an order.
- Original decision artifacts cannot be found; write a data-gap review instead of guessing.
