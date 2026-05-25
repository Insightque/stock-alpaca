# Workflow: One-Year Daily Independent Policy Simulation

Use this when testing whether recommendation-policy changes survive a one-year, day-by-day dry-run simulation. This workflow is research/backtest only.

## Safety Mode

- Paper-only backtest.
- No Alpaca order tools.
- No Alpaca trading REST endpoints.
- Market data must be captured through Alpaca MCP, normally via `scripts/fetch-alpaca-bars-mcp.py`.
- `orders_submitted=0` must appear in every output artifact.

## Inputs

- Strategy config: `harness/strategies/long-term-quality-momentum-v1.yaml`.
- Symbol metadata: `harness/symbol-metadata.yaml`.
- Recommendation policy: `harness/recommendation-policy.yaml`.
- Optional but recommended research MCP event feature cache: `wiki/evidence-store/sources/YYYY-MM-DD-event-feature-cache.json`, shaped like `harness/templates/event-feature-cache.json`.
- Universe: expanded US liquid universe from `harness/symbol-metadata.yaml`, plus `SPY`, `QQQ`, and `SMH` benchmarks.

## Steps

1. Confirm `ALPACA_PAPER_TRADE=true`.
2. Capture daily adjusted Alpaca MCP bars for the past one year:

```bash
python3 scripts/fetch-alpaca-bars-mcp.py \
  --symbols "AAPL,ABBV,ADBE,AMAT,AMD,AMZN,ASML,AVGO,BA,BAC,CAT,COIN,COP,COST,CRM,CVX,ETN,FCX,GE,GOOGL,GS,HD,HON,HOOD,INTC,IONQ,ISRG,JNJ,JPM,KLAC,LIN,LLY,LRCX,MA,MCD,META,MRK,MS,MSFT,MU,NEE,NKE,NOK,NVDA,ORCL,PFE,PLTR,QBTS,QQQ,RGTI,RTX,SBUX,SLB,SMH,SO,SPY,TSLA,TSM,UNH,V,WMT,XOM" \
  --start YYYY-MM-DDT00:00:00Z \
  --end YYYY-MM-DDT23:59:59Z \
  --timeframe 1Day \
  --feed iex \
  --adjustment all \
  --output-json wiki/evidence-store/sources/YYYY-MM-DD-one-year-daily-bars.json
```

3. Build or refresh an as-of research MCP event feature cache when using SEC, earnings, macro, IR, Yahoo analyst/news, or valuation context in the score. Each event row must have `available_at` at or before the simulated as-of date. Use `mcp_gaps` rather than guessing missing provider data.

Required MCP coverage for a full feature cache:

- `sec-edgar`: filings, Form 4/insider, XBRL or filing-grounded risk signals.
- `alpha-vantage`: earnings calendar/history/surprise and earnings-related overextension signals.
- `fred`: macro regime series such as DGS10, DGS2, FEDFUNDS, CPIAUCSL, UNRATE, NFCI.
- `firecrawl`: official IR, press release, and earnings presentation page capture.
- `yahoo-finance`: analyst/news/holder supplemental context.

4. Run the independent daily simulation:

```bash
python3 scripts/simulate-one-year-daily-policy.py \
  --input-json wiki/evidence-store/sources/YYYY-MM-DD-one-year-daily-bars.json \
  --strategy-config harness/strategies/long-term-quality-momentum-v1.yaml \
  --metadata-yaml harness/symbol-metadata.yaml \
  --event-features-json wiki/evidence-store/sources/YYYY-MM-DD-event-feature-cache.json \
  --output-json wiki/evidence-store/sources/YYYY-MM-DD-one-year-daily-policy-simulation-data.json \
  --output-md wiki/backtest-runs/results/YYYY-MM-DD-one-year-daily-policy-simulation.md \
  --scorecard-json wiki/evidence-store/sources/YYYY-MM-DD-one-year-policy-scorecard.json
```

5. Review the result against `harness/recommendation-policy.yaml` promotion criteria.
6. If a rule change is warranted, create a proposal from `wiki/policy-book/proposals/TEMPLATE-policy-change.md`; do not silently promote a strategy from one simulation.
7. Update `wiki/index.md` and append `wiki/log.md`.

## Required Output Checks

- The simulation must record `daily_independent_runs`.
- Every recommendation row must include `independent_run_id`.
- Results must show whether costs were applied.
- Results must show `data_manifest.source_feed`, `bar_interval`, `fill_model`, and `slippage_model` or an explicit data gap.
- Results must show whether an MCP event feature cache was used, how many selected recommendations matched it, and which research MCP servers contributed to matched features.
- Intraday strategies remain `observation_only`; a one-year daily simulation cannot promote intraday automation.
