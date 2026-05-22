---
id: 2026-05-22-alpaca-market-data
source_type: alpaca
captured_at: 2026-05-22T13:39:00Z
source_url: ""
tool: "mcp__alpaca__.get_most_active_stocks; mcp__alpaca__.get_market_movers; mcp__alpaca__.get_stock_snapshot; mcp__alpaca__.get_stock_bars; mcp__alpaca__.get_asset"
tickers: [SPY, QQQ, SMH, SOXS, RGTI, FUTU, TIGR, LFS, QTEX, BIYA]
immutable: true
---

# Alpaca Market Data Snapshot

## Summary

- Watchlists were empty, so the run used broad proxies plus Alpaca most-active/mover symbols.
- Broad proxies: SPY, QQQ, SMH.
- Event/momentum symbols reviewed: SOXS, RGTI, FUTU, TIGR, LFS, QTEX, BIYA.
- Most-active by volume included MEHA, QTEX, WOK, LFS, SOXS, BIYA, TIGR, KIDZ, RGTI, FUTU.
- Top movers included LFS, QTEX, BIYA, FUTU, TIGR, and other highly speculative low-priced names.

## Key Evidence

- SPY latest trade 747.59 at `2026-05-22T13:38:53Z`; daily close-to-snapshot was up from prior daily close 742.71 to 747.70.
- QQQ latest trade 720.52 at `2026-05-22T13:38:52Z`; prior daily close 714.41, snapshot daily 720.46.
- SMH latest trade 576.72 at `2026-05-22T13:38:43Z`; prior daily close 567.44, snapshot daily 576.67.
- SOXS latest trade 7.86 at `2026-05-22T13:38:53Z`; prior daily close 8.27, snapshot daily 7.83.
- RGTI latest trade 24.80 at `2026-05-22T13:38:52Z`; prior daily close 22.04, snapshot daily 24.88.
- FUTU latest trade 87.24 at `2026-05-22T13:38:53Z`; prior daily close 123.82, snapshot daily 87.045.
- TIGR latest trade 4.19 at `2026-05-22T13:38:54Z`; prior daily close 5.84, snapshot daily 4.105.
- LFS latest trade 4.03 at `2026-05-22T13:38:39Z`; prior daily close 1.85, snapshot daily 4.08.
- QTEX latest trade 0.5089 at `2026-05-22T13:38:25Z`; prior daily close 0.306, snapshot daily 0.5104.
- BIYA latest trade 1.07 at `2026-05-22T13:38:52Z`; prior daily close 0.62, snapshot daily 1.04.

## Tickers Mentioned

- SPY, QQQ, SMH, SOXS, RGTI, FUTU, TIGR, LFS, QTEX, BIYA.

## Notes For Wiki Integration

- Broad proxies were in confirmed short-term uptrends during the snapshot.
- SOXS is a 3x inverse semiconductor ETF; it is unsuitable as a core long holding.
- LFS, QTEX, and BIYA were tradable but low-priced, volatile, and non-fractionable; they should be treated as speculative only.
