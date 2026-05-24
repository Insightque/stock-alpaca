#!/usr/bin/env python3
"""Simulate long-horizon equity selection policies with Alpaca daily bars.

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
from datetime import date, datetime, timedelta
from pathlib import Path
from statistics import pstdev
from typing import Any


UNIVERSE = (
    "NVDA",
    "AMD",
    "AVGO",
    "TSM",
    "LRCX",
    "PLTR",
    "TSLA",
    "NOK",
    "UNH",
    "ETN",
    "IONQ",
    "QBTS",
    "RGTI",
)
BENCHMARKS = ("SPY", "QQQ", "SMH")
SYMBOLS = BENCHMARKS + UNIVERSE
TRAIN_DATES = (
    "2026-02-05",
    "2026-02-09",
    "2026-02-12",
    "2026-02-17",
    "2026-02-20",
    "2026-02-25",
    "2026-03-02",
    "2026-03-06",
    "2026-03-11",
    "2026-03-16",
    "2026-03-20",
    "2026-03-25",
    "2026-03-30",
)
VALIDATION_DATES = (
    "2026-04-01",
    "2026-04-06",
    "2026-04-10",
    "2026-04-15",
    "2026-04-20",
    "2026-04-24",
    "2026-04-29",
    "2026-05-04",
    "2026-05-08",
    "2026-05-13",
)


@dataclass(frozen=True)
class Bar:
    day: date
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


def parse_bar(raw: dict[str, Any]) -> Bar:
    ts = datetime.fromisoformat(raw["t"].replace("Z", "+00:00"))
    return Bar(
        day=ts.date(),
        open=float(raw["o"]),
        high=float(raw["h"]),
        low=float(raw["l"]),
        close=float(raw["c"]),
        volume=float(raw.get("v", 0.0) or 0.0),
    )


def fetch_daily_bars(root: Path, start: str, end: str) -> dict[str, list[Bar]]:
    env = read_env(root)
    key = env.get("ALPACA_API_KEY")
    secret = env.get("ALPACA_SECRET_KEY")
    if not key or not secret:
        raise SystemExit("Missing ALPACA_API_KEY or ALPACA_SECRET_KEY")
    params = urllib.parse.urlencode(
        {
            "symbols": ",".join(SYMBOLS),
            "timeframe": "1Day",
            "start": f"{start}T00:00:00Z",
            "end": f"{end}T23:59:59Z",
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
            f"Alpaca market data fetch failed with curl exit {completed.returncode}; "
            "credentials were not printed."
        )
    payload = json.loads(completed.stdout)
    return {symbol: [parse_bar(row) for row in rows] for symbol, rows in payload.get("bars", {}).items()}


def index_by_day(bars: list[Bar]) -> dict[date, int]:
    return {bar.day: idx for idx, bar in enumerate(bars)}


def nearest_on_or_before(trading_days: list[date], target: date) -> date | None:
    prior = [day for day in trading_days if day <= target]
    return max(prior, default=None)


def pct_return(start: float, end: float) -> float:
    return (end / start - 1.0) * 100.0


def window_return(bars: list[Bar], idx: int, lookback: int) -> float | None:
    if idx - lookback < 0:
        return None
    return pct_return(bars[idx - lookback].close, bars[idx].close)


def max_drawdown_pct(bars: list[Bar]) -> float:
    peak = bars[0].close
    worst = 0.0
    for bar in bars:
        peak = max(peak, bar.close)
        drawdown = (bar.close / peak - 1.0) * 100.0
        worst = min(worst, drawdown)
    return worst


def avg_volume_ratio(bars: list[Bar], idx: int) -> float | None:
    if idx - 40 < 0:
        return None
    recent = bars[idx - 19 : idx + 1]
    older = bars[idx - 39 : idx - 19]
    older_avg = sum(bar.volume for bar in older) / len(older)
    if older_avg <= 0:
        return None
    return (sum(bar.volume for bar in recent) / len(recent)) / older_avg


def volatility_pct(bars: list[Bar], idx: int, lookback: int = 20) -> float | None:
    if idx - lookback < 0:
        return None
    returns = [pct_return(bars[i - 1].close, bars[i].close) for i in range(idx - lookback + 1, idx + 1)]
    return pstdev(returns) if len(returns) >= 2 else None


def forward_return(bars: list[Bar], idx: int, horizon: int) -> tuple[float | None, date | None, float | None]:
    target_idx = idx + horizon
    if target_idx >= len(bars):
        return None, None, None
    start = bars[idx].close
    end = bars[target_idx].close
    path = bars[idx : target_idx + 1]
    adverse = min((bar.low / start - 1.0) * 100.0 for bar in path)
    return pct_return(start, end), bars[target_idx].day, adverse


def score_symbol(
    symbol: str,
    symbol_bars: list[Bar],
    spy_bars: list[Bar],
    qqq_bars: list[Bar],
    asof: date,
    trading_index: dict[date, int],
) -> dict[str, Any] | None:
    idx_by_day = index_by_day(symbol_bars)
    spy_idx_by_day = index_by_day(spy_bars)
    qqq_idx_by_day = index_by_day(qqq_bars)
    if asof not in idx_by_day or asof not in spy_idx_by_day or asof not in qqq_idx_by_day:
        return None
    idx = idx_by_day[asof]
    spy_idx = spy_idx_by_day[asof]
    qqq_idx = qqq_idx_by_day[asof]
    ret20 = window_return(symbol_bars, idx, 20)
    ret40 = window_return(symbol_bars, idx, 40)
    ret60 = window_return(symbol_bars, idx, 60)
    spy20 = window_return(spy_bars, spy_idx, 20)
    qqq20 = window_return(qqq_bars, qqq_idx, 20)
    vol20 = volatility_pct(symbol_bars, idx, 20)
    vol_ratio = avg_volume_ratio(symbol_bars, idx)
    if None in (ret20, ret40, ret60, spy20, qqq20, vol20, vol_ratio):
        return None
    dd60 = max_drawdown_pct(symbol_bars[idx - 59 : idx + 1])
    rs_spy20 = ret20 - spy20
    rs_qqq20 = ret20 - qqq20
    trend_bonus = 0.0
    trend_bonus += max(min(ret60, 40.0), -40.0) * 0.8
    trend_bonus += max(min(ret20, 25.0), -25.0) * 1.0
    trend_bonus += max(min(rs_spy20, 25.0), -25.0) * 1.2
    trend_bonus += max(min(rs_qqq20, 25.0), -25.0) * 0.8
    stability_penalty = abs(min(dd60, 0.0)) * 0.7 + max(vol20 - 4.0, 0.0) * 4.0
    overextension_penalty = max(ret20 - 35.0, 0.0) * 1.2
    liquidity_bonus = min(max((vol_ratio - 0.8) * 8.0, -6.0), 8.0)
    score = 50.0 + trend_bonus + liquidity_bonus - stability_penalty - overextension_penalty
    return {
        "symbol": symbol,
        "asof_close": symbol_bars[idx].close,
        "score": score,
        "ret20": ret20,
        "ret40": ret40,
        "ret60": ret60,
        "rs_spy20": rs_spy20,
        "rs_qqq20": rs_qqq20,
        "dd60": dd60,
        "vol20": vol20,
        "volume_ratio": vol_ratio,
    }


def select_portfolio(scored: list[dict[str, Any]], variant: str) -> list[dict[str, Any]]:
    if variant == "balanced_top3":
        filtered = [row for row in scored if row["ret60"] > -5 and row["dd60"] > -35 and row["vol20"] < 8.5]
        return sorted(filtered, key=lambda row: row["score"], reverse=True)[:3]
    if variant == "quality_top5":
        filtered = [row for row in scored if row["ret60"] > -10 and row["dd60"] > -30 and row["vol20"] < 7.0]
        return sorted(filtered, key=lambda row: row["score"] - max(row["ret20"] - 25, 0) * 1.5, reverse=True)[:5]
    if variant == "momentum_top3":
        filtered = [row for row in scored if row["ret20"] > 0 and row["rs_spy20"] > 0]
        return sorted(filtered, key=lambda row: (row["ret20"], row["rs_spy20"]), reverse=True)[:3]
    raise ValueError(variant)


def simulate_dates(bars_by_symbol: dict[str, list[Bar]], dates: tuple[str, ...], variants: tuple[str, ...]) -> list[dict[str, Any]]:
    spy = bars_by_symbol["SPY"]
    qqq = bars_by_symbol["QQQ"]
    spy_index = index_by_day(spy)
    trading_days = sorted(spy_index)
    rows: list[dict[str, Any]] = []
    for date_text in dates:
        requested = date.fromisoformat(date_text)
        asof = nearest_on_or_before(trading_days, requested)
        if asof is None:
            continue
        scored = []
        for symbol in UNIVERSE:
            row = score_symbol(symbol, bars_by_symbol.get(symbol, []), spy, qqq, asof, spy_index)
            if row:
                scored.append(row)
        scored.sort(key=lambda row: row["score"], reverse=True)
        for variant in variants:
            picks = select_portfolio(scored, variant)
            for rank, pick in enumerate(picks, start=1):
                symbol_bars = bars_by_symbol[pick["symbol"]]
                idx = index_by_day(symbol_bars)[asof]
                spy_idx = spy_index[asof]
                qqq_idx = index_by_day(qqq)[asof]
                ret5, date5, adverse5 = forward_return(symbol_bars, idx, 5)
                ret10, date10, adverse10 = forward_return(symbol_bars, idx, 10)
                ret20, date20, adverse20 = forward_return(symbol_bars, idx, 20)
                spy20, _, _ = forward_return(spy, spy_idx, 20)
                qqq20, _, _ = forward_return(qqq, qqq_idx, 20)
                rows.append(
                    {
                        "requested_asof": date_text,
                        "asof": asof.isoformat(),
                        "variant": variant,
                        "rank": rank,
                        **pick,
                        "ret5_fwd": ret5,
                        "ret5_date": date5.isoformat() if date5 else None,
                        "ret10_fwd": ret10,
                        "ret10_date": date10.isoformat() if date10 else None,
                        "ret20_fwd": ret20,
                        "ret20_date": date20.isoformat() if date20 else None,
                        "spy20_fwd": spy20,
                        "qqq20_fwd": qqq20,
                        "excess_spy20": ret20 - spy20 if ret20 is not None and spy20 is not None else None,
                        "excess_qqq20": ret20 - qqq20 if ret20 is not None and qqq20 is not None else None,
                        "adverse20": adverse20,
                    }
                )
    return rows


def summarize(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out = []
    for variant in sorted({row["variant"] for row in rows}):
        subset = [row for row in rows if row["variant"] == variant]
        completed20 = [row for row in subset if row["ret20_fwd"] is not None and row["excess_spy20"] is not None]
        completed10 = [row for row in subset if row["ret10_fwd"] is not None]
        completed5 = [row for row in subset if row["ret5_fwd"] is not None]
        out.append(
            {
                "variant": variant,
                "asof_count": len({row["asof"] for row in subset}),
                "recommendations": len(subset),
                "completed20": len(completed20),
                "hit20_abs": sum(1 for row in completed20 if row["ret20_fwd"] > 0),
                "hit20_spy": sum(1 for row in completed20 if row["excess_spy20"] > 0),
                "avg20": sum(row["ret20_fwd"] for row in completed20) / len(completed20) if completed20 else None,
                "avg_excess_spy20": sum(row["excess_spy20"] for row in completed20) / len(completed20) if completed20 else None,
                "avg_adverse20": sum(row["adverse20"] for row in completed20 if row["adverse20"] is not None) / len(completed20) if completed20 else None,
                "completed10": len(completed10),
                "avg10": sum(row["ret10_fwd"] for row in completed10) / len(completed10) if completed10 else None,
                "completed5": len(completed5),
                "avg5": sum(row["ret5_fwd"] for row in completed5) / len(completed5) if completed5 else None,
            }
        )
    return out


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--cache-json", type=Path, required=True)
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    bars = fetch_daily_bars(root, "2025-11-01", "2026-05-23")
    variants = ("balanced_top3", "quality_top5", "momentum_top3")
    train_rows = simulate_dates(bars, TRAIN_DATES, variants)
    validation_rows = simulate_dates(bars, VALIDATION_DATES, variants)
    result = {
        "created_at": datetime.now().isoformat(),
        "source": "Alpaca Market Data API IEX 1Day bars",
        "universe": UNIVERSE,
        "benchmarks": BENCHMARKS,
        "train_dates": TRAIN_DATES,
        "validation_dates": VALIDATION_DATES,
        "variants": list(variants),
        "train_summary": summarize(train_rows),
        "validation_summary": summarize(validation_rows),
        "train_recommendations": train_rows,
        "validation_recommendations": validation_rows,
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    compact_cache = {
        symbol: [
            {"t": bar.day.isoformat(), "o": bar.open, "h": bar.high, "l": bar.low, "c": bar.close, "v": bar.volume}
            for bar in rows
        ]
        for symbol, rows in bars.items()
    }
    args.cache_json.parent.mkdir(parents=True, exist_ok=True)
    args.cache_json.write_text(json.dumps(compact_cache, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"train": result["train_summary"], "validation": result["validation_summary"]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
