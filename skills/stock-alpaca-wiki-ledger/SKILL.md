---
name: stock-alpaca-wiki-ledger
description: Maintain the stock-alpaca llm-wiki knowledge layer. Use when a task creates or changes reports, raw sources, run manifests, order plans, position snapshots, reviews, policy-book entries, wiki/index.md, or wiki/log.md.
---

# Stock Alpaca Wiki Ledger

Use this skill for durable knowledge and audit trails.

## Boundary

This is a cross-cutting recordkeeping skill. It does not decide trading actions, provider coverage, or risk policy; it records the outcome of those workflows and preserves source traceability.

## Rules

1. Read `wiki/index.md` and recent `wiki/log.md` before meaningful trading/research runs.
2. Write wiki content in Korean by default.
3. Keep raw source notes under `wiki/evidence-store/sources/` immutable after capture except formatting fixes.
4. Append to `wiki/log.md`; do not rewrite old log entries.
5. Update `wiki/index.md` when new reusable pages, reports, reviews, or policy pages are added.
6. Use wiki links where helpful while keeping Markdown readable.
7. Do not rewrite old thesis pages to look smarter in hindsight.

## Artifact Placement

- Current daily reports: `wiki/current-runs/daily/`
- Run manifests: `wiki/evidence-store/run-manifests/`
- Raw sources: `wiki/evidence-store/sources/`
- Order plans: `wiki/trade-ledger/orders/`
- Position/account snapshots: `wiki/trade-ledger/positions/`
- Reviews: `wiki/trade-ledger/reviews/`
- Historical decisions: `wiki/backtest-runs/decisions/`
- Historical results: `wiki/backtest-runs/results/`
- Living policy: `wiki/policy-book/recommendation-policy.md`

## Log Entry

For meaningful runs, append:

```markdown
## [YYYY-MM-DD HH:MM TZ] type | title

- What ran or changed.
- Key gates/results.
- Artifacts created or updated.
- Tests or validators run.
```
