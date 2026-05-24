from __future__ import annotations

import hashlib
import math
import random
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any, Iterable


def apply_round_trip_cost(return_pct: float, cost_model: dict[str, Any]) -> float:
    """Subtract simple round-trip spread/slippage/fee costs from a percent return."""
    slippage_bps = float(cost_model.get("slippage_bps", 0.0) or 0.0)
    spread_bps = float(cost_model.get("spread_bps", 0.0) or 0.0)
    fee_bps = float(cost_model.get("fee_bps", 0.0) or 0.0)
    round_trip_bps = 2.0 * slippage_bps + spread_bps + fee_bps
    return return_pct - (round_trip_bps / 100.0)


def conservative_stop_take_exit(entry: float, high: float, low: float, close: float, stop: float, take: float) -> tuple[float, str]:
    """Resolve same-bar stop/take ambiguity conservatively for a long position."""
    stop_hit = low <= stop
    take_hit = high >= take
    if stop_hit and take_hit:
        return stop, "stop_before_take_conservative"
    if stop_hit:
        return stop, "stop"
    if take_hit:
        return take, "take"
    return close, "eod"


def bootstrap_mean_ci(
    values: list[float],
    *,
    iterations: int = 1000,
    confidence: float = 0.95,
    seed: int = 7,
) -> tuple[float | None, float | None]:
    if not values:
        return None, None
    rng = random.Random(seed)
    means = []
    for _ in range(iterations):
        sample = [values[rng.randrange(len(values))] for _ in values]
        means.append(sum(sample) / len(sample))
    means.sort()
    tail = (1.0 - confidence) / 2.0
    lower_idx = max(0, min(len(means) - 1, int(math.floor(tail * len(means)))))
    upper_idx = max(0, min(len(means) - 1, int(math.ceil((1.0 - tail) * len(means))) - 1))
    return means[lower_idx], means[upper_idx]


def concentration_metrics(rows: Iterable[dict[str, Any]], value_key: str = "forward_20d_excess_spy_pct") -> dict[str, Any]:
    completed = [row for row in rows if row.get(value_key) is not None]
    symbol_counts: Counter[str] = Counter(str(row.get("symbol", "")) for row in completed)
    theme_counts: Counter[str] = Counter(str(row.get("theme", "")) for row in completed)
    total = len(completed)
    if not total:
        return {
            "completed": 0,
            "max_single_symbol_recommendation_pct": 0.0,
            "max_single_theme_recommendation_pct": 0.0,
            "top_symbols": [],
            "top_themes": [],
        }
    return {
        "completed": total,
        "max_single_symbol_recommendation_pct": max(symbol_counts.values()) / total * 100.0,
        "max_single_theme_recommendation_pct": max(theme_counts.values()) / total * 100.0,
        "top_symbols": symbol_counts.most_common(8),
        "top_themes": theme_counts.most_common(8),
    }


def month_index(value: str | date) -> int:
    parsed = date.fromisoformat(value) if isinstance(value, str) else value
    return parsed.year * 12 + parsed.month


def walk_forward_splits(
    dates: list[str],
    *,
    train_months: int,
    validation_months: int,
    step_months: int = 1,
) -> list[dict[str, str]]:
    if not dates:
        return []
    unique_dates = sorted(set(dates))
    first_month = month_index(unique_dates[0])
    last_month = month_index(unique_dates[-1])
    windows = []
    start_month = first_month
    while start_month + train_months + validation_months - 1 <= last_month:
        train_start = start_month
        train_end = start_month + train_months - 1
        validation_start = train_end + 1
        validation_end = validation_start + validation_months - 1
        train_dates = [d for d in unique_dates if train_start <= month_index(d) <= train_end]
        validation_dates = [d for d in unique_dates if validation_start <= month_index(d) <= validation_end]
        if train_dates and validation_dates:
            windows.append(
                {
                    "train_start": train_dates[0],
                    "train_end": train_dates[-1],
                    "validation_start": validation_dates[0],
                    "validation_end": validation_dates[-1],
                }
            )
        start_month += step_months
    return windows


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return "sha256:" + digest.hexdigest()
