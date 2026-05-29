---
name: stock-alpaca-review-policy-learning
description: Review stock-alpaca trades and update policy-learning artifacts. Use for 거래 회고, post-trade checks, analyst review cycle, 1D/5D/20D reviews, still-held position reviews, recommendation-policy updates, or policy-book evidence rules.
---

# Stock Alpaca Review Policy Learning

Use this skill when later outcomes should be compared with prior decisions.

## Boundary

This skill owns reviews of actual paper trades and evidence-backed policy learning. Use `stock-alpaca-simulation-lab` for historical dry-run simulations and simulated outcome studies.

## Review Scope

1. Review both closed trades and still-held traded stocks.
2. Mark open-position conclusions as interim.
3. Compare against the original decision context: ticker page, daily report, order plan, raw sources, account snapshot, market data, and risk policy available at decision time.
4. Record what worked, what failed, what was unknowable, and what should change.
5. Do not edit the original recommendation to include later outcomes.

## Policy Update Rule

- Treat a single trade as a hypothesis unless impact is clearly material.
- Update `wiki/policy-book/recommendation-policy.md` only when evidence is useful for future decisions.
- Include evidence count, hit rate, average excess return, and status when promoting a lesson.
- Keep after-hours validation separate from regular-session policy learning.

## Analyst Review Runtime

For scheduled analyst review work, read:

- `harness/workflows/analyst-review-cycle.md`
- `scheduler/README.md`
- Relevant order, position, and review artifacts

This workflow never submits, replaces, cancels, or closes orders.
