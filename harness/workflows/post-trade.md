# Workflow: Post-Trade Check

Use this when the user says `Post-trade check`.

## Goal

Reconcile submitted orders, fills, current positions, cash, buying power, and portfolio state after a trading workflow.

## Required Outputs

- Updated `wiki/portfolio/current.md`
- Updated relevant daily report if one exists
- Updated ticker pages for symbols with fills or open orders
- Updated `wiki/index.md`
- Appended `wiki/log.md` entry

## Procedure

1. Read `AGENTS.md`, `wiki/index.md`, recent reports, and recent order plans.
2. Use Alpaca MCP to get account info, open orders, recent filled/canceled orders, account activities, and all positions.
3. Compare actual orders/fills against the latest order plan.
4. Update `wiki/portfolio/current.md` using `harness/templates/portfolio-state.md`.
5. If a daily report exists for today, update its submitted orders, skipped orders, and unresolved issues sections.
6. Update ticker pages touched by fills or open orders.
7. Append a log entry with:
   - Account value and cash.
   - Position count.
   - Filled/open/canceled order counts.
   - Any reconciliation mismatch.

## Hard Rule

Do not submit new orders in this workflow.

