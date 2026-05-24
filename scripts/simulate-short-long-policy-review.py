#!/usr/bin/env python3
"""Simulate current intraday and long-term paper policies.

This script uses read-only Alpaca market data bars and local captured caches.
It never submits, replaces, cancels, or closes orders.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import urllib.parse
from dataclasses import dataclass
from datetime import date, datetime, time
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo


ET = ZoneInfo("America/New_York")
UTC = ZoneInfo("UTC")
INTRADAY_CONTEXT = ("QQQ", "SMH")
INTRADAY_CANDIDATES = ("NVDA", "AMD", "AVGO", "TSM", "LRCX", "PLTR", "TSLA")
BREADTH_SYMBOLS = ("SMH", "NVDA", "AMD", "AVGO", "TSM", "LRCX")
INTRADAY_TRAIN_DATES = (
    "2026-02-03",
    "2026-02-12",
    "2026-02-20",
    "2026-03-03",
    "2026-03-09",
    "2026-03-19",
    "2026-03-26",
    "2026-03-31",
)
INTRADAY_VALIDATION_DATES = (
    "2026-04-01",
    "2026-04-09",
    "2026-04-14",
    "2026-04-17",
    "2026-04-29",
    "2026-05-04",
    "2026-05-08",
    "2026-05-13",
    "2026-05-21",
    "2026-05-22",
)


@dataclass(frozen=True)
class Bar:
    ts: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float


def read_env(root: Path) -> dict[str, str]:
    env = os.environ.copy()
    env_file = root / ".env"
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            if not line or line.strip().startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            env.setdefault(key.strip(), value.strip().strip('"').strip("'"))
    return env


def parse_timestamp(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(ET)


def parse_bar(raw: dict[str, Any]) -> Bar:
    return Bar(
        ts=parse_timestamp(str(raw["t"])),
        open=float(raw["o"]),
        high=float(raw["h"]),
        low=float(raw["l"]),
        close=float(raw["c"]),
        volume=float(raw.get("v", 0.0) or 0.0),
    )


def serialize_bar(bar: Bar) -> dict[str, Any]:
    return {
        "t": bar.ts.astimezone(UTC).isoformat().replace("+00:00", "Z"),
        "o": bar.open,
        "h": bar.high,
        "l": bar.low,
        "c": bar.close,
        "v": bar.volume,
    }


def market_window(day: date) -> tuple[str, str]:
    start = datetime.combine(day, time(9, 30), ET).astimezone(UTC).isoformat().replace("+00:00", "Z")
    end = datetime.combine(day, time(16, 0), ET).astimezone(UTC).isoformat().replace("+00:00", "Z")
    return start, end


def fetch_intraday_bars(root: Path, symbols: tuple[str, ...], day: date) -> dict[str, list[Bar]]:
    env = read_env(root)
    key = env.get("ALPACA_API_KEY")
    secret = env.get("ALPACA_SECRET_KEY")
    if not key or not secret:
        raise SystemExit("Missing ALPACA_API_KEY or ALPACA_SECRET_KEY")
    start, end = market_window(day)
    params = urllib.parse.urlencode(
        {
            "symbols": ",".join(symbols),
            "timeframe": "1Min",
            "start": start,
            "end": end,
            "feed": "iex",
            "limit": "10000",
        }
    )
    cmd = [
        "curl",
        "-sS",
        "--fail",
        "-H",
        f"APCA-API-KEY-ID: {key}",
        "-H",
        f"APCA-API-SECRET-KEY: {secret}",
        f"https://data.alpaca.markets/v2/stocks/bars?{params}",
    ]
    completed = subprocess.run(cmd, check=False, capture_output=True, text=True)
    if completed.returncode != 0:
        raise SystemExit(
            f"Alpaca market data fetch failed for {day.isoformat()} "
            f"with curl exit {completed.returncode}; credentials were not printed."
        )
    payload = json.loads(completed.stdout)
    return {symbol.upper(): [parse_bar(row) for row in rows] for symbol, rows in payload.get("bars", {}).items()}


def load_intraday_cache(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"symbols": list(INTRADAY_CONTEXT + INTRADAY_CANDIDATES), "dates": {}}
    return json.loads(path.read_text(encoding="utf-8"))


def bars_for_day(root: Path, cache: dict[str, Any], day_text: str) -> dict[str, list[Bar]]:
    if day_text not in cache["dates"]:
        symbols = INTRADAY_CONTEXT + INTRADAY_CANDIDATES
        fetched = fetch_intraday_bars(root, symbols, date.fromisoformat(day_text))
        cache["dates"][day_text] = {
            symbol: [serialize_bar(bar) for bar in rows]
            for symbol, rows in fetched.items()
        }
    return {
        symbol: [parse_bar(row) for row in rows]
        for symbol, rows in cache["dates"][day_text].items()
    }


def in_window(bar: Bar, day: date, start: time, end: time) -> bool:
    return bar.ts.date() == day and start <= bar.ts.time() <= end


def bars_between(bars: list[Bar], day: date, start: time, end: time) -> list[Bar]:
    return [bar for bar in bars if in_window(bar, day, start, end)]


def first_at_or_after(bars: list[Bar], day: date, target: time) -> Bar | None:
    same_day = [bar for bar in bars if bar.ts.date() == day and bar.ts.time() >= target]
    return min(same_day, key=lambda item: item.ts, default=None)


def pct(start: float, end: float) -> float:
    return (end / start - 1.0) * 100.0


def vwap(bars: list[Bar]) -> float | None:
    total_volume = sum(max(bar.volume, 0.0) for bar in bars)
    if total_volume <= 0:
        return None
    return sum(((bar.high + bar.low + bar.close) / 3.0) * max(bar.volume, 0.0) for bar in bars) / total_volume


def theoretical_outcome(day_bars: list[Bar], entry: Bar, take_pct: float = 2.0, stop_pct: float = 1.0) -> tuple[str, float, float]:
    take = entry.open * (1.0 + take_pct / 100.0)
    stop = entry.open * (1.0 - stop_pct / 100.0)
    later = [bar for bar in day_bars if bar.ts >= entry.ts]
    for bar in later:
        stop_hit = bar.low <= stop
        take_hit = bar.high >= take
        if stop_hit and take_hit:
            return "ambiguous_stop_first", -stop_pct, stop
        if stop_hit:
            return "stop", -stop_pct, stop
        if take_hit:
            return "take", take_pct, take
    eod = max(later, key=lambda item: item.ts, default=None)
    if not eod:
        return "unknown", 0.0, entry.open
    pl_pct = pct(entry.open, eod.close)
    return ("eod_gain" if pl_pct >= 0 else "eod_loss"), pl_pct, eod.close


def evaluate_intraday_day(day_text: str, bars: dict[str, list[Bar]]) -> list[dict[str, Any]]:
    day = date.fromisoformat(day_text)
    qqq = bars.get("QQQ", [])
    smh = bars.get("SMH", [])
    qqq_signal = bars_between(qqq, day, time(10, 0), time(10, 59))
    qqq_entry = first_at_or_after(qqq, day, time(11, 0))
    smh_entry = first_at_or_after(smh, day, time(11, 0))
    if not qqq_signal or not qqq_entry or not smh_entry:
        return []

    qqq_return = pct(qqq_signal[0].open, qqq_signal[-1].close)
    qqq_vwap = vwap(bars_between(qqq, day, time(9, 30), time(10, 59)))
    smh_vwap = vwap(bars_between(smh, day, time(9, 30), time(10, 59)))
    qqq_vwap_pass = bool(qqq_vwap and qqq_entry.open > qqq_vwap)
    smh_vwap_pass = bool(smh_vwap and smh_entry.open > smh_vwap)

    breadth_count = 0
    for symbol in BREADTH_SYMBOLS:
        symbol_bars = bars.get(symbol, [])
        open_bar = first_at_or_after(symbol_bars, day, time(9, 30))
        entry_bar = first_at_or_after(symbol_bars, day, time(11, 0))
        if open_bar and entry_bar and entry_bar.open > open_bar.open:
            breadth_count += 1

    candidates: list[dict[str, Any]] = []
    for symbol in INTRADAY_CANDIDATES:
        symbol_bars = bars.get(symbol, [])
        signal = bars_between(symbol_bars, day, time(10, 0), time(10, 59))
        previous = bars_between(symbol_bars, day, time(9, 30), time(9, 59))
        day_bars = bars_between(symbol_bars, day, time(9, 30), time(15, 59))
        entry = first_at_or_after(symbol_bars, day, time(11, 0))
        if not signal or not previous or not day_bars or not entry:
            continue
        symbol_return = pct(signal[0].open, signal[-1].close)
        relative_strength = symbol_return - qqq_return
        previous_high = max(bar.high for bar in previous)
        breakout_pass = signal[-1].close >= previous_high * 0.999
        symbol_vwap = vwap(bars_between(symbol_bars, day, time(9, 30), time(10, 59)))
        symbol_vwap_pass = bool(symbol_vwap and entry.open > symbol_vwap)
        v0_pass = (
            qqq_return >= 0.20
            and symbol_return >= 0.90
            and relative_strength >= 0.40
            and breakout_pass
        )
        v1_pass = v0_pass and qqq_vwap_pass and smh_vwap_pass and symbol_vwap_pass and breadth_count >= 4
        outcome, pl_pct, exit_price = theoretical_outcome(day_bars, entry)
        candidates.append(
            {
                "date": day_text,
                "symbol": symbol,
                "qqq_10h_return_pct": qqq_return,
                "symbol_10h_return_pct": symbol_return,
                "relative_strength_pctpt": relative_strength,
                "breakout_pass": breakout_pass,
                "qqq_vwap_pass": qqq_vwap_pass,
                "smh_vwap_pass": smh_vwap_pass,
                "symbol_vwap_pass": symbol_vwap_pass,
                "semi_breadth_count": breadth_count,
                "entry_time_et": entry.ts.strftime("%H:%M"),
                "entry_price": entry.open,
                "exit_price": exit_price,
                "outcome": outcome,
                "pl_pct": pl_pct,
                "pl_usd_per_10k": 10000.0 * pl_pct / 100.0,
                "v0_pass": v0_pass,
                "v1_pass": v1_pass,
            }
        )

    ranked_v0 = sorted(
        [row for row in candidates if row["v0_pass"]],
        key=lambda row: (row["relative_strength_pctpt"], row["symbol_10h_return_pct"]),
        reverse=True,
    )
    ranked_v1 = [row for row in ranked_v0 if row["v1_pass"]]
    rows: list[dict[str, Any]] = []
    for policy, ranked, limit in (
        ("intraday-rs-breakout-v0-top3", ranked_v0, 3),
        ("intraday-rs-breakout-v0-top2", ranked_v0, 2),
        ("intraday-rs-breadth-vwap-v1-top3", ranked_v1, 3),
        ("intraday-rs-breadth-vwap-v1-top2", ranked_v1, 2),
    ):
        for rank, row in enumerate(ranked[:limit], start=1):
            clean = {key: value for key, value in row.items() if key not in {"v0_pass", "v1_pass"}}
            rows.append({"policy": policy, "rank": rank, **clean})
    return rows


def summarize_intraday(rows: list[dict[str, Any]], dates: tuple[str, ...]) -> list[dict[str, Any]]:
    policies = (
        "intraday-rs-breakout-v0-top3",
        "intraday-rs-breakout-v0-top2",
        "intraday-rs-breadth-vwap-v1-top3",
        "intraday-rs-breadth-vwap-v1-top2",
    )
    out = []
    for policy in policies:
        subset = [row for row in rows if row["policy"] == policy]
        trades = len(subset)
        wins = sum(1 for row in subset if row["pl_pct"] > 0)
        stops = sum(1 for row in subset if row["outcome"] in {"stop", "ambiguous_stop_first"})
        takes = sum(1 for row in subset if row["outcome"] == "take")
        total_pl = sum(row["pl_usd_per_10k"] for row in subset)
        out.append(
            {
                "policy": policy,
                "sample_days": len(dates),
                "active_days": len({row["date"] for row in subset}),
                "trades": trades,
                "hit_rate": wins / trades * 100.0 if trades else 0.0,
                "stops": stops,
                "takes": takes,
                "pl_usd_per_10k_trade": total_pl,
                "avg_pl_usd_per_trade": total_pl / trades if trades else 0.0,
            }
        )
    return out


def summarize_long_term(source: dict[str, Any], variant: str = "quality_top5") -> dict[str, Any]:
    def calc(rows: list[dict[str, Any]], phase: str) -> dict[str, Any]:
        subset = [row for row in rows if row["variant"] == variant]
        completed20 = [row for row in subset if row["ret20_fwd"] is not None]
        completed10 = [row for row in subset if row["ret10_fwd"] is not None]
        completed5 = [row for row in subset if row["ret5_fwd"] is not None]
        return {
            "phase": phase,
            "variant": variant,
            "asof_count": len({row["asof"] for row in subset}),
            "recommendations": len(subset),
            "completed20": len(completed20),
            "hit20_abs": sum(1 for row in completed20 if row["ret20_fwd"] > 0),
            "hit20_spy": sum(1 for row in completed20 if row["excess_spy20"] and row["excess_spy20"] > 0),
            "avg20": sum(row["ret20_fwd"] for row in completed20) / len(completed20) if completed20 else None,
            "avg_excess_spy20": sum(row["excess_spy20"] for row in completed20) / len(completed20) if completed20 else None,
            "avg_adverse20": sum(row["adverse20"] for row in completed20) / len(completed20) if completed20 else None,
            "pl20_usd_per_10k_pick": sum(10000.0 * row["ret20_fwd"] / 100.0 for row in completed20),
            "completed10": len(completed10),
            "avg10": sum(row["ret10_fwd"] for row in completed10) / len(completed10) if completed10 else None,
            "completed5": len(completed5),
            "avg5": sum(row["ret5_fwd"] for row in completed5) / len(completed5) if completed5 else None,
        }

    return {
        "source_file": "wiki/raw/sources/2026-05-23-long-term-feb-mar-apr-may-simulation-data.json",
        "train_dates": source["train_dates"],
        "validation_dates": source["validation_dates"],
        "train_summary": calc(source["train_recommendations"], "train"),
        "validation_summary": calc(source["validation_recommendations"], "validation"),
        "top_validation_picks": sorted(
            [
                row
                for row in source["validation_recommendations"]
                if row["variant"] == variant and row["ret20_fwd"] is not None
            ],
            key=lambda row: row["ret20_fwd"],
            reverse=True,
        )[:10],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--intraday-cache-json", type=Path, required=True)
    parser.add_argument(
        "--long-term-source-json",
        type=Path,
        default=Path("wiki/raw/sources/2026-05-23-long-term-feb-mar-apr-may-simulation-data.json"),
    )
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    cache = load_intraday_cache(args.intraday_cache_json)
    all_rows: list[dict[str, Any]] = []
    for day_text in INTRADAY_TRAIN_DATES + INTRADAY_VALIDATION_DATES:
        bars = bars_for_day(root, cache, day_text)
        all_rows.extend(evaluate_intraday_day(day_text, bars))

    args.intraday_cache_json.parent.mkdir(parents=True, exist_ok=True)
    args.intraday_cache_json.write_text(json.dumps(cache, ensure_ascii=False), encoding="utf-8")

    train_rows = [row for row in all_rows if row["date"] in INTRADAY_TRAIN_DATES]
    validation_rows = [row for row in all_rows if row["date"] in INTRADAY_VALIDATION_DATES]
    long_term_source = json.loads(args.long_term_source_json.read_text(encoding="utf-8"))
    result = {
        "created_at": datetime.now(ET).isoformat(),
        "paper": True,
        "orders_submitted": 0,
        "source": {
            "intraday": "Alpaca Market Data API IEX 1Min bars, read-only; selected Feb/Mar and Apr/May dates",
            "long_term": "Existing Alpaca IEX 1Day bar simulation data from 2026-05-23 raw source",
        },
        "intraday": {
            "train_dates": INTRADAY_TRAIN_DATES,
            "validation_dates": INTRADAY_VALIDATION_DATES,
            "train_summary": summarize_intraday(train_rows, INTRADAY_TRAIN_DATES),
            "validation_summary": summarize_intraday(validation_rows, INTRADAY_VALIDATION_DATES),
            "train_trades": train_rows,
            "validation_trades": validation_rows,
        },
        "long_term": summarize_long_term(long_term_source),
        "data_gaps": [
            "Intraday bars use IEX feed, not full SIP; VWAP and high/low can differ from consolidated market data.",
            "Intraday simulation does not include bid/ask spread, limit-fill probability, queue position, or slippage.",
            "Long-term validation for some May as-of dates still lacks completed 20D outcomes.",
            "Long-term scoring is price/volume based and does not yet include earnings, valuation, SEC filing, macro, or analyst context.",
        ],
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({
        "intraday_train": result["intraday"]["train_summary"],
        "intraday_validation": result["intraday"]["validation_summary"],
        "long_term": {
            "train": result["long_term"]["train_summary"],
            "validation": result["long_term"]["validation_summary"],
        },
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
