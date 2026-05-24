#!/usr/bin/env python3
"""Backtest additional intraday policy candidates with Alpaca market data.

This script only reads Alpaca stock bars. It never submits, replaces, cancels,
or closes orders.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import urllib.parse
from dataclasses import dataclass
from datetime import date, datetime, time, timedelta
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo


ET = ZoneInfo("America/New_York")
UTC = ZoneInfo("UTC")
UNIVERSE = ("NVDA", "AMD", "AVGO", "TSM", "LRCX", "PLTR", "TSLA")
CONTEXT = ("QQQ", "SMH")
TRAIN_DATES = ("2026-03-03", "2026-03-09", "2026-03-10", "2026-03-19", "2026-03-25")
VALIDATION_DATES = ("2026-04-01", "2026-04-09", "2026-04-10", "2026-04-14", "2026-04-17")


@dataclass(frozen=True)
class Bar:
    ts: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float


def parse_timestamp(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(ET)


def parse_bar(raw: dict[str, Any]) -> Bar:
    return Bar(
        ts=parse_timestamp(raw["t"]),
        open=float(raw["o"]),
        high=float(raw["h"]),
        low=float(raw["l"]),
        close=float(raw["c"]),
        volume=float(raw.get("v", 0.0) or 0.0),
    )


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


def market_window(day: date) -> tuple[str, str]:
    start = datetime.combine(day, time(9, 30), ET).astimezone(UTC).isoformat().replace("+00:00", "Z")
    end = datetime.combine(day, time(16, 0), ET).astimezone(UTC).isoformat().replace("+00:00", "Z")
    return start, end


def fetch_bars(root: Path, symbols: tuple[str, ...], day: date) -> dict[str, list[Bar]]:
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
    return {
        symbol.upper(): [parse_bar(row) for row in rows]
        for symbol, rows in payload.get("bars", {}).items()
    }


def in_window(bar: Bar, day: date, start: time, end: time) -> bool:
    return bar.ts.date() == day and start <= bar.ts.time() <= end


def bars_between(bars: list[Bar], day: date, start: time, end: time) -> list[Bar]:
    return [bar for bar in bars if in_window(bar, day, start, end)]


def first_at_or_after(bars: list[Bar], day: date, target: time) -> Bar | None:
    same_day = [bar for bar in bars if bar.ts.date() == day and bar.ts.time() >= target]
    return min(same_day, key=lambda item: item.ts, default=None)


def vwap(bars: list[Bar]) -> float | None:
    total_volume = sum(max(bar.volume, 0.0) for bar in bars)
    if total_volume <= 0:
        return None
    return sum(((bar.high + bar.low + bar.close) / 3.0) * max(bar.volume, 0.0) for bar in bars) / total_volume


def pct(a: float, b: float) -> float:
    return (b / a - 1.0) * 100.0


def evaluate_trade(day_bars: list[Bar], entry: Bar, take_pct: float, stop_pct: float) -> tuple[str, float, float]:
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
    pl = pct(entry.open, eod.close)
    return ("eod_gain" if pl >= 0 else "eod_loss"), pl, eod.close


def volume_ratio(first: list[Bar], recent: list[Bar]) -> float | None:
    if not first or not recent:
        return None
    first_avg = sum(bar.volume for bar in first) / len(first)
    recent_avg = sum(bar.volume for bar in recent) / len(recent)
    if first_avg <= 0:
        return None
    return recent_avg / first_avg


def build_rows(policy: str, day: date, candidates: list[dict[str, Any]], top_n: int, take: float, stop: float) -> list[dict[str, Any]]:
    rows = []
    for rank, item in enumerate(candidates[:top_n], start=1):
        outcome, pl_pct, exit_price = evaluate_trade(item["day_bars"], item["entry_bar"], take, stop)
        rows.append(
            {
                "date": day.isoformat(),
                "policy": policy,
                "rank": rank,
                "symbol": item["symbol"],
                "entry_time": item["entry_bar"].ts.strftime("%H:%M"),
                "entry_price": item["entry_bar"].open,
                "exit_price": exit_price,
                "outcome": outcome,
                "pl_pct": pl_pct,
                "pl_usd": 10000.0 * pl_pct / 100.0,
                **item["metrics"],
            }
        )
    return rows


def signals_for_day(day: date, bars: dict[str, list[Bar]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    qqq = bars.get("QQQ", [])
    smh = bars.get("SMH", [])
    qqq_entry_11 = first_at_or_after(qqq, day, time(11, 0))
    qqq_entry_13 = first_at_or_after(qqq, day, time(13, 0))
    qqq_vwap_11 = vwap(bars_between(qqq, day, time(9, 30), time(10, 59)))
    qqq_vwap_13 = vwap(bars_between(qqq, day, time(9, 30), time(12, 59)))
    qqq_open = first_at_or_after(qqq, day, time(9, 30))
    smh_entry_11 = first_at_or_after(smh, day, time(11, 0))
    smh_vwap_11 = vwap(bars_between(smh, day, time(9, 30), time(10, 59)))

    qqq_vwap_pass_11 = bool(qqq_entry_11 and qqq_vwap_11 and qqq_entry_11.open > qqq_vwap_11)
    smh_vwap_pass_11 = bool(smh_entry_11 and smh_vwap_11 and smh_entry_11.open > smh_vwap_11)
    qqq_vwap_pass_13 = bool(qqq_entry_13 and qqq_vwap_13 and qqq_entry_13.open > qqq_vwap_13)
    qqq_day_ret_11 = pct(qqq_open.open, qqq_entry_11.open) if qqq_open and qqq_entry_11 else 0.0

    morning_reclaim: list[dict[str, Any]] = []
    midday_reversal: list[dict[str, Any]] = []
    volume_momentum: list[dict[str, Any]] = []

    for symbol in UNIVERSE:
        symbol_bars = bars.get(symbol, [])
        day_bars = bars_between(symbol_bars, day, time(9, 30), time(15, 59))
        open_bar = first_at_or_after(symbol_bars, day, time(9, 30))
        entry_11 = first_at_or_after(symbol_bars, day, time(11, 0))
        entry_13 = first_at_or_after(symbol_bars, day, time(13, 0))
        if not day_bars or not open_bar:
            continue

        first_30 = bars_between(symbol_bars, day, time(9, 30), time(9, 59))
        recent_30 = bars_between(symbol_bars, day, time(10, 30), time(10, 59))
        hour_10 = bars_between(symbol_bars, day, time(10, 0), time(10, 59))
        morning = bars_between(symbol_bars, day, time(9, 30), time(10, 59))
        pre_13 = bars_between(symbol_bars, day, time(9, 30), time(12, 59))
        symbol_vwap_11 = vwap(morning)
        symbol_vwap_13 = vwap(pre_13)
        ratio = volume_ratio(first_30, recent_30)

        if entry_11 and morning and symbol_vwap_11:
            morning_low = min(bar.low for bar in morning)
            recovery_from_low = pct(morning_low, entry_11.open)
            early_drawdown = pct(open_bar.open, morning_low)
            reclaim_pass = entry_11.open > symbol_vwap_11
            if (
                qqq_vwap_pass_11
                and smh_vwap_pass_11
                and -1.0 <= qqq_day_ret_11 <= 1.0
                and early_drawdown <= -1.0
                and recovery_from_low >= 0.8
                and reclaim_pass
                and entry_11.open <= open_bar.open * 1.01
            ):
                morning_reclaim.append(
                    {
                        "symbol": symbol,
                        "entry_bar": entry_11,
                        "day_bars": day_bars,
                        "metrics": {
                            "early_drawdown_pct": early_drawdown,
                            "recovery_from_low_pct": recovery_from_low,
                            "symbol_vwap_pass": reclaim_pass,
                            "qqq_vwap_pass": qqq_vwap_pass_11,
                            "smh_vwap_pass": smh_vwap_pass_11,
                            "volume_ratio": ratio,
                        },
                    }
                )

        if entry_13 and pre_13 and symbol_vwap_13:
            pre_low = min(bar.low for bar in pre_13)
            recovery_from_low = pct(pre_low, entry_13.open)
            early_drawdown = pct(open_bar.open, pre_low)
            if (
                qqq_vwap_pass_13
                and early_drawdown <= -2.0
                and recovery_from_low >= 1.2
                and entry_13.open > symbol_vwap_13
                and entry_13.open <= open_bar.open * 1.005
            ):
                midday_reversal.append(
                    {
                        "symbol": symbol,
                        "entry_bar": entry_13,
                        "day_bars": day_bars,
                        "metrics": {
                            "early_drawdown_pct": early_drawdown,
                            "recovery_from_low_pct": recovery_from_low,
                            "symbol_vwap_pass": True,
                            "qqq_vwap_pass": qqq_vwap_pass_13,
                            "volume_ratio": ratio,
                        },
                    }
                )

        if entry_11 and hour_10 and ratio is not None and symbol_vwap_11:
            hour_ret = pct(hour_10[0].open, hour_10[-1].close)
            relative_to_qqq = hour_ret - qqq_day_ret_11
            if qqq_vwap_pass_11 and smh_vwap_pass_11 and hour_ret >= 0.70 and relative_to_qqq >= 0.40 and ratio >= 1.25:
                volume_momentum.append(
                    {
                        "symbol": symbol,
                        "entry_bar": entry_11,
                        "day_bars": day_bars,
                        "metrics": {
                            "hour_return_pct": hour_ret,
                            "relative_to_qqq_pctpt": relative_to_qqq,
                            "symbol_vwap_pass": entry_11.open > symbol_vwap_11,
                            "qqq_vwap_pass": qqq_vwap_pass_11,
                            "smh_vwap_pass": smh_vwap_pass_11,
                            "volume_ratio": ratio,
                        },
                    }
                )

    morning_reclaim.sort(key=lambda item: (item["metrics"]["recovery_from_low_pct"], item["metrics"]["early_drawdown_pct"]), reverse=True)
    midday_reversal.sort(key=lambda item: (item["metrics"]["recovery_from_low_pct"], item["metrics"]["early_drawdown_pct"]), reverse=True)
    volume_momentum.sort(key=lambda item: (item["metrics"]["volume_ratio"] or 0, item["metrics"]["hour_return_pct"]), reverse=True)

    rows.extend(build_rows("pullback-vwap-reclaim-morning", day, morning_reclaim, 2, 1.5, 0.8))
    rows.extend(build_rows("midday-vwap-reversal", day, midday_reversal, 2, 1.2, 0.8))
    rows.extend(build_rows("volume-confirmed-momentum", day, volume_momentum, 2, 1.5, 0.8))
    return rows


def summarize(rows: list[dict[str, Any]], dates: tuple[str, ...]) -> list[dict[str, Any]]:
    summary = []
    for policy in sorted({row["policy"] for row in rows} | {"pullback-vwap-reclaim-morning", "midday-vwap-reversal", "volume-confirmed-momentum"}):
        subset = [row for row in rows if row["policy"] == policy]
        active_days = len({row["date"] for row in subset})
        trades = len(subset)
        wins = sum(1 for row in subset if row["pl_pct"] > 0)
        stops = sum(1 for row in subset if row["outcome"] in {"stop", "ambiguous_stop_first"})
        takes = sum(1 for row in subset if row["outcome"] == "take")
        pl = sum(row["pl_usd"] for row in subset)
        summary.append(
            {
                "policy": policy,
                "sample_days": len(dates),
                "active_days": active_days,
                "trades": trades,
                "hit_rate": (wins / trades * 100.0) if trades else 0.0,
                "stop": stops,
                "take": takes,
                "pl_usd": pl,
                "avg_per_trade": (pl / trades) if trades else 0.0,
            }
        )
    return summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--cache-json", type=Path, required=True)
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    symbols = CONTEXT + UNIVERSE
    cache: dict[str, Any] = {"symbols": symbols, "dates": {}}
    all_rows: list[dict[str, Any]] = []
    for date_text in TRAIN_DATES + VALIDATION_DATES:
        day = date.fromisoformat(date_text)
        bars = fetch_bars(root, symbols, day)
        cache["dates"][date_text] = {
            symbol: [
                {
                    "t": bar.ts.astimezone(UTC).isoformat().replace("+00:00", "Z"),
                    "o": bar.open,
                    "h": bar.high,
                    "l": bar.low,
                    "c": bar.close,
                    "v": bar.volume,
                }
                for bar in rows
            ]
            for symbol, rows in bars.items()
        }
        all_rows.extend(signals_for_day(day, bars))

    train_rows = [row for row in all_rows if row["date"] in TRAIN_DATES]
    validation_rows = [row for row in all_rows if row["date"] in VALIDATION_DATES]
    result = {
        "created_at": datetime.now(ET).isoformat(),
        "source": "Alpaca Market Data API IEX 1Min bars",
        "universe": symbols,
        "train_dates": TRAIN_DATES,
        "validation_dates": VALIDATION_DATES,
        "train_summary": summarize(train_rows, TRAIN_DATES),
        "validation_summary": summarize(validation_rows, VALIDATION_DATES),
        "train_trades": train_rows,
        "validation_trades": validation_rows,
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    args.cache_json.parent.mkdir(parents=True, exist_ok=True)
    args.cache_json.write_text(json.dumps(cache, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"train": result["train_summary"], "validation": result["validation_summary"]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
