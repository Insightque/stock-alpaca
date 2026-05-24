# Workflow: Intraday Paper Dry-Run

Use this when the user asks to continue the intraday scalping policy work, or when running a live-session observation pass for `intraday-rs-breakout-v0` and `intraday-rs-breadth-vwap-v1`.

## Goal

Record real-time paper dry-run signals around 11:00 ET without submitting, replacing, canceling, or closing any order. The output is an observation log for policy learning, not an order plan.

## Safety Mode

- Paper-only observation.
- Strategy state: `auto_eligible=false`, `dry_run_only=true`, `policy_status=observation_only`.
- No Alpaca order tools.
- No Alpaca trading REST endpoints.
- No order-plan JSON unless a later separate workflow explicitly requests a no-submit allocation plan.
- No live, options, crypto, short, fractional-share, bracket, trailing-stop, or margin-specific action.
- If any step requires account mutation, stop and record `skipped_mutation=true`.

Allowed data operations:

- Alpaca MCP market data, asset lookup, clock, news, watchlist reads.
- Research MCP/web context only for source capture.
- Local scripts that read captured market data and write wiki notes.

Disallowed tools/actions:

- `place_stock_order`
- `replace_order_by_id`
- `cancel_order_by_id`
- `close_position`
- `close_all_positions`
- Custom REST calls to Alpaca trading endpoints.

## Timing

Run on US regular trading days.

| ET time | Action |
| --- | --- |
| 09:25-09:35 | Confirm `ALPACA_PAPER_TRADE=true`, market clock, candidate universe, and data source availability. |
| 10:55-11:05 | Capture 1Min bars through 10:59 ET, latest bid/ask/quote if available, and snapshots for QQQ, SMH, candidates, and breadth symbols. |
| 11:00-11:10 | Compute v0 and v1 signals. Record theoretical entry as the first regular-session 1Min open at or after 11:00 ET. |
| 12:00 ET | Optional status check only: current price vs theoretical entry, QQQ/SMH VWAP state, adverse move. Do not add new entries from this check. |
| 15:55-16:10 | Record theoretical EOD outcome, stop/take path if 1Min bars are available, and fill-quality observations. |

## Candidate Universe

Use the intersection of:

- Alpaca watchlist symbols or user-specified tickers.
- Active tradable US stocks/ETFs from Alpaca asset lookup.
- Existing intraday validation symbols unless the user expands the set: `NVDA`, `AMD`, `AVGO`, `TSM`, `LRCX`, `PLTR`, `TSLA`, `SMH`, `QQQ`.

For v1 breadth, always include:

- `SMH`, `NVDA`, `AMD`, `AVGO`, `TSM`, `LRCX`.

## v0 Signal Definition

Policy id: `intraday-rs-breakout-v0`

Use data known by 11:00 ET.

- QQQ 10:00-10:59 ET return is at least `+0.20%`.
- Candidate 10:00-10:59 ET return is at least `+0.90%`.
- Candidate return minus QQQ return is at least `+0.40%p`.
- Candidate 10:59 ET close is near or above the previous intraday bar high. Default near-high tolerance is `0.50%` below the 09:30-09:59 ET high.
- Rank candidates by relative strength, then candidate return.
- Track top3, and also top2 for comparison.

The 1-hour timestamp correction is mandatory: any signal based on the 10:00 hour bar can only be treated as executable after 11:00 ET.

## v1 Signal Definition

Policy id: `intraday-rs-breadth-vwap-v1`

Start from v0 pass symbols, then require:

- QQQ entry/reference price is above regular-session VWAP measured through 10:59 ET.
- SMH entry/reference price is above regular-session VWAP measured through 10:59 ET.
- Candidate entry/reference price is above its own regular-session VWAP measured through 10:59 ET.
- Semiconductor breadth is at least 4 of 6. Breadth symbols are `SMH`, `NVDA`, `AMD`, `AVGO`, `TSM`, `LRCX`; count a symbol when its 11:00 ET reference price is above its regular-session open.

Track both:

- `v1_top3`: maximum expected opportunity set.
- `v1_top2`: stability-first set from the latest backtest.

## Required Signal Record

Create a daily dry-run note at:

`wiki/analyses/YYYY-MM-DD-intraday-paper-dry-run.md`

Recommended table columns:

| field | meaning |
| --- | --- |
| `captured_at_et` | Market-data capture timestamp in ET. |
| `symbol` | Candidate ticker. |
| `policy` | `v0_top3`, `v0_top2`, `v1_top3`, or `v1_top2`. |
| `rank` | Rank within that policy set. |
| `qqq_10h_return_pct` | QQQ 10:00-10:59 ET return. |
| `symbol_10h_return_pct` | Candidate 10:00-10:59 ET return. |
| `relative_strength_pctpt` | Candidate return minus QQQ return. |
| `breakout_pass` | Whether close is near/above previous bar high. |
| `qqq_vwap_pass` | v1 market VWAP check. |
| `smh_vwap_pass` | v1 sector VWAP check. |
| `symbol_vwap_pass` | v1 candidate VWAP check. |
| `semi_breadth_count` | 0-6 breadth count. |
| `entry_reference_time_et` | First regular-session 1Min bar at or after 11:00 ET. |
| `entry_reference_price` | Theoretical entry reference; not an order. |
| `bid` | Latest bid near capture time, if available. |
| `ask` | Latest ask near capture time, if available. |
| `spread_pct` | `(ask - bid) / mid * 100`, if available. |
| `fill_feasibility` | `likely`, `uncertain`, `poor`, or `unknown`. |
| `fill_notes` | Spread, quote freshness, slippage, or missing quote notes. |
| `take_price` | Theoretical `entry * 1.02`. |
| `stop_price` | Theoretical `entry * 0.99`. |
| `eod_reference_price` | 15:59 ET close or latest available EOD proxy. |
| `theoretical_outcome` | `take`, `stop`, `eod_gain`, `eod_loss`, `open`, or `unknown`. |
| `theoretical_pl_pct` | Theoretical percent return, after stop/take/EOD logic. |
| `signal_log` | Machine-readable signal state for later fill-quality learning. |
| `skip_reason` | Why a symbol did not become an observation candidate. Use explicit values such as `spread_missing`, `fill_probability_unknown`, `stale_quote`, `minute_ordering_unknown`, or `policy_blocked`. |
| `spread_fill_observation` | Bid/ask spread, quote freshness, partial-fill likelihood, and any queue/slippage note. |

Do not use this workflow to create an order-plan entry. Intraday observations are evidence collection, not allocation recommendations. A future promotion proposal must show quote-level validation, spread history, limit-fill probability, minute-level stop/take ordering, and positive cost-adjusted walk-forward results across at least three independent periods.

At the bottom of every dry-run analysis note, add a Korean `## 지표 설명` section. Explain the metrics and analysis fields in plain language so the user can read the result without asking a separate follow-up. Include at least these terms when present: `active days`, `trade count`, `hit rate`, `stop`, `take`, `P/L`, `average per trade`, `QQQ VWAP`, `SMH VWAP`, `symbol VWAP`, `semiconductor breadth`, `relative strength`, `spread_pct`, and `fill_feasibility`.

## Local Helper Script

If 1Min bars are already captured to local JSON, run:

```bash
python3 scripts/evaluate-intraday-dry-run.py \
  --bars-json path/to/captured-1min-bars.json \
  --date YYYY-MM-DD \
  --output-md wiki/analyses/YYYY-MM-DD-intraday-paper-dry-run.md \
  --output-json wiki/analyses/YYYY-MM-DD-intraday-paper-dry-run.json
```

The helper script must not call Alpaca APIs. It reads captured bars and optional quotes only.

## Wiki Updates

After each dry-run:

1. Add the daily dry-run note to `wiki/index.md`.
2. Append a `wiki/log.md` entry with:
   - market date,
   - candidate count,
   - v0 signal count,
   - v1 signal count,
   - whether bid/ask data was captured,
   - explicit `orders_submitted=0`.
3. If the run reveals a repeated issue, add it as a hypothesis in `wiki/policies/recommendation-policy.md`; do not promote it to a current rule until evidence accumulates.

## Stop Conditions

- `ALPACA_PAPER_TRADE` is missing or not `true`.
- Any requested action would mutate account/order/position state.
- Market data is unavailable or stale enough that 11:00 ET signal quality cannot be assessed.
- Candidate asset cannot be confirmed as active, tradable, US stock/ETF.
