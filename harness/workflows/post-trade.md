# Workflow: Post-Trade Check

Use this when the user says `포트폴리오 점검해줘`, `거래 후 점검해줘`, or asks for a post-trade check.

## Goal

Reconcile submitted orders, fills, current positions, cash, buying power, and portfolio state after a trading workflow.

## Required Outputs

- Updated `wiki/portfolio/current.md`
- Updated relevant daily report if one exists
- Updated ticker pages for symbols with fills or open orders
- Trade review due markers for filled symbols when enough outcome data exists
- Updated `wiki/index.md`
- Appended `wiki/log.md` entry

## Procedure

1. Read `AGENTS.md`, `wiki/index.md`, recent reports, and recent order plans.
2. Use Alpaca MCP to get account info, open orders, recent filled/canceled orders, account activities, and all positions.
3. Compare actual orders/fills against the latest order plan.
4. Update `wiki/portfolio/current.md` using `harness/templates/portfolio-state.md`.
5. If a daily report exists for today, update its submitted orders, skipped orders, and unresolved issues sections.
6. Update ticker pages touched by fills or open orders.
7. Check whether a trade review is due:
   - Mark new fills as `회고 대기` until there is enough outcome data.
   - If a position is closed, or if an open position has meaningful unrealized P/L, holding-period drift, thesis break, or a major catalyst update, run or schedule `harness/workflows/trade-review.md`.
   - Do not force a final judgment on newly opened positions.
8. Append a log entry with:
   - Account value and cash.
   - Position count.
   - Filled/open/canceled order counts.
   - Any reconciliation mismatch.
   - Trade review status: not due, interim review written, final review written, or skipped with reason.

## Hard Rule

Do not submit new orders in this workflow.
