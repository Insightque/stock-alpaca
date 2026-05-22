# Workflow: Lint Trading Wiki

Use this when the user says `Lint trading wiki`.

## Goal

Health-check the llm-wiki for stale, missing, contradictory, orphaned, or uncited trading knowledge.

## Required Outputs

- A lint report in `wiki/analyses/YYYY-MM-DD-wiki-lint.md`
- Fixes to index/log references when safe
- Updated pages only when the fix is mechanical or clearly source-backed
- Appended `wiki/log.md` entry

## Checks

- Every ticker in reports or order plans has a page in `wiki/tickers/`.
- Every ticker page has at least one source note or explicit Alpaca MCP citation.
- `wiki/index.md` lists all ticker pages, daily reports, analyses, and important raw source groups.
- `wiki/log.md` has an entry for each daily report and rebalance run.
- Raw source notes are not edited after capture except formatting fixes.
- Claims marked current are not older than 7 calendar days unless explicitly labeled long-term.
- Contradictions are listed as contested claims with source references.
- Orphan pages are either linked from index or marked archived.

## Procedure

1. Read `AGENTS.md`, `wiki/index.md`, and `wiki/log.md`.
2. Search the wiki for ticker symbols, report references, order-plan paths, and source links.
3. Produce a lint report with findings grouped as: blocking, stale, missing source, contradiction, orphan, and cleanup.
4. Fix only safe mechanical issues in the same run.
5. Do not trade, create order plans, or alter raw source meaning.

