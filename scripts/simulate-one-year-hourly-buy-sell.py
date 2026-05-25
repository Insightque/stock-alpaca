#!/usr/bin/env python3
"""Run one-year daily buy/sell dry-run decisions from captured 1Hour bars.

This is a research/backtest helper. It consumes bars captured through Alpaca
MCP, creates daily independent virtual buy and sell/avoid decisions, and
evaluates each decision over short and long forward horizons. It never submits,
replaces, cancels, or closes orders.
"""

from __future__ import annotations

import argparse
import json
import math
import statistics
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

import yaml

from policy_simulation_lib import apply_round_trip_cost, bootstrap_mean_ci, file_sha256


ROOT_DIR = Path(__file__).resolve().parents[1]
ET = ZoneInfo("America/New_York")
BENCHMARKS_DEFAULT = {"SPY", "QQQ", "SMH"}
CONFIDENCE_SCORE_BY_BUCKET = {"high": 0.85, "medium": 0.65, "low": 0.35}
HORIZONS = (("same_day", 0), ("1D", 1), ("5D", 5), ("20D", 20), ("60D", 60))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-json", type=Path, required=True)
    parser.add_argument("--strategy-config", type=Path, default=ROOT_DIR / "harness/strategies/long-term-quality-momentum-v1.yaml")
    parser.add_argument("--metadata-yaml", type=Path, default=ROOT_DIR / "harness/symbol-metadata.yaml")
    parser.add_argument("--recommendation-policy-yaml", type=Path, default=ROOT_DIR / "harness/recommendation-policy.yaml")
    parser.add_argument("--risk-policy-yaml", type=Path, default=ROOT_DIR / "harness/risk-policy.yaml")
    parser.add_argument(
        "--event-features-json",
        type=Path,
        help="Optional point-in-time research MCP feature cache to join by symbol and as-of date.",
    )
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    parser.add_argument("--source-md", type=Path, required=True)
    parser.add_argument("--scorecard-json", type=Path)
    parser.add_argument("--run-manifest", type=Path)
    parser.add_argument("--run-id", default="2026-05-25-one-year-hourly-buy-sell-simulation")
    parser.add_argument("--progress", action="store_true", help="Print agent-style daily progress lines.")
    return parser.parse_args()


def progress(enabled: bool, agent: str, message: str) -> None:
    if enabled:
        print(f"[{agent}] {message}", flush=True)


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a YAML object")
    return data


def pct(start: float, end: float) -> float:
    return (end / start - 1.0) * 100.0 if start else 0.0


def mean(values: list[float]) -> float | None:
    return sum(values) / len(values) if values else None


def safe_float(value: Any) -> float | None:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) else None


def as_float(value: Any, default: float = 0.0) -> float:
    number = safe_float(value)
    return default if number is None else number


def as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def parse_timestamp(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(ET)


def parse_date_key(value: Any) -> str | None:
    if value in (None, ""):
        return None
    text = str(value)
    if len(text) >= 10 and text[4:5] == "-" and text[7:8] == "-":
        return text[:10]
    return None


def round_json(value: Any) -> Any:
    if isinstance(value, float):
        return round(value, 6)
    if isinstance(value, list):
        return [round_json(item) for item in value]
    if isinstance(value, dict):
        return {key: round_json(item) for key, item in value.items()}
    return value


def metadata_for(symbol: str, metadata: dict[str, Any]) -> dict[str, Any]:
    defaults = metadata.get("defaults", {})
    symbols = metadata.get("symbols", {})
    value = symbols.get(symbol, {})
    return {**defaults, **value}


def normalize_event_features(raw: dict[str, Any] | None) -> dict[str, list[dict[str, Any]]]:
    if not raw:
        return {}
    normalized: dict[str, list[dict[str, Any]]] = defaultdict(list)

    def add_record(symbol_hint: str | None, date_hint: str | None, record: Any) -> None:
        if not isinstance(record, dict):
            return
        row = dict(record)
        symbol = str(row.get("symbol") or symbol_hint or "").upper().strip()
        if not symbol:
            return
        available_date = (
            parse_date_key(row.get("available_at"))
            or parse_date_key(row.get("asof_date"))
            or parse_date_key(row.get("date"))
            or parse_date_key(date_hint)
        )
        if not available_date:
            return
        row["symbol"] = symbol
        row["available_date"] = available_date
        normalized[symbol].append(row)

    features = raw.get("features")
    if isinstance(features, dict):
        for symbol, value in features.items():
            if isinstance(value, list):
                for record in value:
                    add_record(str(symbol), None, record)
            elif isinstance(value, dict):
                for date_key, record in value.items():
                    add_record(str(symbol), str(date_key), record)
    for record in as_list(raw.get("records")):
        add_record(None, None, record)
    for rows in normalized.values():
        rows.sort(key=lambda item: str(item["available_date"]))
    return dict(normalized)


def load_event_features(path: Path | None) -> dict[str, list[dict[str, Any]]]:
    if not path:
        return {}
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return normalize_event_features(raw)


def event_feature_for(
    symbol: str,
    asof: str,
    event_features: dict[str, list[dict[str, Any]]] | None,
) -> dict[str, Any] | None:
    if not event_features:
        return None
    eligible = [
        row
        for row in event_features.get(symbol.upper(), [])
        if str(row.get("available_date", "")) <= asof
    ]
    return eligible[-1] if eligible else None


def event_score_adjustment(record: dict[str, Any] | None) -> float:
    if not record:
        return 0.0
    total = as_float(record.get("score_adjustment"))
    for key in (
        "earnings_score_adjustment",
        "sec_score_adjustment",
        "macro_score_adjustment",
        "ir_score_adjustment",
        "analyst_score_adjustment",
        "news_score_adjustment",
        "valuation_score_adjustment",
    ):
        total += as_float(record.get(key))
    return total


def event_fields(
    symbol: str,
    asof: str,
    base_source_confidence_score: float,
    event_features: dict[str, list[dict[str, Any]]] | None,
) -> dict[str, Any]:
    feature = event_feature_for(symbol, asof, event_features)
    mcp_gaps = as_list((feature or {}).get("mcp_gaps") or (feature or {}).get("gap_flags"))
    if feature and feature.get("source_confidence_score") is not None:
        source_confidence_score = max(0.0, min(1.0, as_float(feature.get("source_confidence_score"), base_source_confidence_score)))
    else:
        source_confidence_score = max(0.0, min(1.0, base_source_confidence_score + as_float((feature or {}).get("source_confidence_delta"))))
    return {
        "source_confidence_score": source_confidence_score,
        "event_feature_present": feature is not None,
        "event_available_date": (feature or {}).get("available_date"),
        "event_score_adjustment": event_score_adjustment(feature),
        "event_exclude": bool((feature or {}).get("exclude", False)),
        "mcp_servers_used": [str(item) for item in as_list((feature or {}).get("mcp_servers_used"))],
        "mcp_gap_count": len(mcp_gaps),
        "mcp_gaps": [str(item) for item in mcp_gaps],
        "mcp_source_refs": [str(item) for item in as_list((feature or {}).get("source_refs"))],
    }


def build_hourly_by_day(raw_rows: dict[str, list[dict[str, Any]]]) -> dict[str, dict[str, list[dict[str, Any]]]]:
    out: dict[str, dict[str, list[dict[str, Any]]]] = {}
    for symbol, rows in raw_rows.items():
        by_day: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for row in rows:
            timestamp = str(row.get("timestamp") or row.get("t"))
            if not timestamp:
                continue
            dt_et = parse_timestamp(timestamp)
            parsed = {
                "timestamp": timestamp,
                "dt_et": dt_et,
                "date": dt_et.date().isoformat(),
                "time_et": dt_et.strftime("%H:%M:%S"),
                "open": as_float(row.get("open", row.get("o"))),
                "high": as_float(row.get("high", row.get("h"))),
                "low": as_float(row.get("low", row.get("l"))),
                "close": as_float(row.get("close", row.get("c"))),
                "volume": as_float(row.get("volume", row.get("v"))),
                "vwap": safe_float(row.get("vwap", row.get("vw"))),
            }
            by_day[parsed["date"]].append(parsed)
        out[symbol.upper()] = {
            day: sorted(items, key=lambda item: item["dt_et"])
            for day, items in sorted(by_day.items())
        }
    return out


def aggregate_daily(hourly_by_day: dict[str, dict[str, list[dict[str, Any]]]]) -> dict[str, list[dict[str, Any]]]:
    daily: dict[str, list[dict[str, Any]]] = {}
    for symbol, by_day in hourly_by_day.items():
        rows = []
        for day, items in sorted(by_day.items()):
            if not items:
                continue
            total_volume = sum(float(row["volume"]) for row in items)
            vwap_value = None
            if total_volume > 0:
                vwap_value = sum(
                    (float(row["vwap"]) if row.get("vwap") is not None else (row["high"] + row["low"] + row["close"]) / 3.0)
                    * float(row["volume"])
                    for row in items
                ) / total_volume
            first = items[0]
            last = items[-1]
            rows.append(
                {
                    "date": day,
                    "open": float(first["open"]),
                    "high": max(float(row["high"]) for row in items),
                    "low": min(float(row["low"]) for row in items),
                    "close": float(last["close"]),
                    "volume": total_volume,
                    "vwap": vwap_value,
                    "hourly_count": len(items),
                    "first_hour_return_pct": pct(float(first["open"]), float(first["close"])),
                    "day_return_pct": pct(float(first["open"]), float(last["close"])),
                    "last_hour_return_pct": pct(float(last["open"]), float(last["close"])),
                }
            )
        daily[symbol] = rows
    return daily


def index_by_date(rows: dict[str, list[dict[str, Any]]]) -> dict[str, dict[str, int]]:
    return {symbol: {str(row["date"]): idx for idx, row in enumerate(items)} for symbol, items in rows.items()}


def ret_at(rows: list[dict[str, Any]], idx: int, lookback: int) -> float | None:
    if idx - lookback < 0:
        return None
    return pct(float(rows[idx - lookback]["close"]), float(rows[idx]["close"]))


def daily_returns(rows: list[dict[str, Any]], start: int, end: int) -> list[float]:
    values = []
    for idx in range(start + 1, end + 1):
        if 0 < idx < len(rows):
            values.append(pct(float(rows[idx - 1]["close"]), float(rows[idx]["close"])))
    return values


def max_drawdown(closes: list[float]) -> float:
    peak = -math.inf
    worst = 0.0
    for close in closes:
        peak = max(peak, close)
        if peak > 0:
            worst = min(worst, pct(peak, close))
    return worst


def avg_dollar_volume(rows: list[dict[str, Any]], idx: int, lookback: int = 20) -> float | None:
    if idx - lookback + 1 < 0:
        return None
    sample = rows[idx - lookback + 1 : idx + 1]
    values = [float(row["close"]) * float(row.get("volume", 0.0) or 0.0) for row in sample]
    return sum(values) / len(values) if values else None


def entry_bar_for(day_rows: list[dict[str, Any]]) -> dict[str, Any] | None:
    if len(day_rows) >= 2:
        return day_rows[1]
    if day_rows:
        return day_rows[0]
    return None


def first_window_positive_rate(
    daily_rows: list[dict[str, Any]],
    idx: int,
    lookback: int = 10,
) -> float:
    start = max(0, idx - lookback + 1)
    sample = daily_rows[start : idx + 1]
    if not sample:
        return 0.0
    return sum(1 for row in sample if float(row.get("first_hour_return_pct", 0.0)) > 0.0) / len(sample)


def candidate_features(
    symbol: str,
    asof: str,
    daily: dict[str, list[dict[str, Any]]],
    indices: dict[str, dict[str, int]],
    hourly_by_day: dict[str, dict[str, list[dict[str, Any]]]],
    metadata: dict[str, Any],
    event_features: dict[str, list[dict[str, Any]]] | None,
) -> dict[str, Any] | None:
    idx = indices.get(symbol, {}).get(asof)
    spy_idx = indices.get("SPY", {}).get(asof)
    qqq_idx = indices.get("QQQ", {}).get(asof)
    if idx is None or spy_idx is None or qqq_idx is None:
        return None
    previous_idx = idx - 1
    spy_previous_idx = spy_idx - 1
    qqq_previous_idx = qqq_idx - 1
    if previous_idx < 40 or spy_previous_idx < 40 or qqq_previous_idx < 40:
        return None
    symbol_daily = daily[symbol]
    spy_daily = daily["SPY"]
    qqq_daily = daily["QQQ"]
    symbol_day_rows = hourly_by_day.get(symbol, {}).get(asof, [])
    spy_day_rows = hourly_by_day.get("SPY", {}).get(asof, [])
    qqq_day_rows = hourly_by_day.get("QQQ", {}).get(asof, [])
    entry = entry_bar_for(symbol_day_rows)
    spy_entry = entry_bar_for(spy_day_rows)
    qqq_entry = entry_bar_for(qqq_day_rows)
    if not entry or not spy_entry or not qqq_entry:
        return None

    values: dict[str, Any] = {
        "symbol": symbol,
        "asof_date": asof,
        "asof_datetime_et": entry["dt_et"].isoformat(timespec="seconds"),
        "entry_time_et": entry["time_et"][:5],
        "entry_price": float(entry["close"]),
        "entry_bar_count": len(symbol_day_rows),
    }
    for lookback in (5, 20, 40):
        value = ret_at(symbol_daily, previous_idx, lookback)
        if value is None:
            return None
        values[f"ret{lookback}_prev_close"] = value
    spy20 = ret_at(spy_daily, spy_previous_idx, 20)
    qqq20 = ret_at(qqq_daily, qqq_previous_idx, 20)
    if spy20 is None or qqq20 is None:
        return None
    closes = [float(row["close"]) for row in symbol_daily[previous_idx - 39 : previous_idx + 1]]
    returns = daily_returns(symbol_daily, previous_idx - 20, previous_idx)
    adv = avg_dollar_volume(symbol_daily, previous_idx, 20)
    if not closes or len(returns) < 2 or adv is None:
        return None
    first = symbol_day_rows[0]
    spy_first = spy_day_rows[0]
    qqq_first = qqq_day_rows[0]
    morning_return = pct(float(first["open"]), float(entry["close"]))
    spy_morning_return = pct(float(spy_first["open"]), float(spy_entry["close"]))
    qqq_morning_return = pct(float(qqq_first["open"]), float(qqq_entry["close"]))
    meta = metadata_for(symbol, metadata)
    source_confidence = str(meta.get("source_confidence", "low"))
    base_source_confidence_score = CONFIDENCE_SCORE_BY_BUCKET.get(source_confidence, 0.35)
    event = event_fields(symbol, asof, base_source_confidence_score, event_features)
    values.update(
        {
            "spy_ret20_prev_close": spy20,
            "qqq_ret20_prev_close": qqq20,
            "spy_excess20_prev_close": values["ret20_prev_close"] - spy20,
            "qqq_excess20_prev_close": values["ret20_prev_close"] - qqq20,
            "drawdown40_prev_close": max_drawdown(closes),
            "vol20_prev_close": statistics.pstdev(returns),
            "avg_daily_dollar_volume": adv,
            "first_hour_positive_rate_10d": first_window_positive_rate(symbol_daily, previous_idx, 10),
            "morning_return_pct": morning_return,
            "morning_excess_spy_pct": morning_return - spy_morning_return,
            "morning_excess_qqq_pct": morning_return - qqq_morning_return,
            "prev_close_to_entry_pct": pct(float(symbol_daily[previous_idx]["close"]), float(entry["close"])),
            "theme": meta.get("theme", "unknown"),
            "factor": meta.get("factor", "unknown"),
            "volatility_bucket": meta.get("volatility_bucket", "high"),
            "speculative_flag": bool(meta.get("speculative_flag", True)),
            "source_confidence": source_confidence,
            "liquidity_bucket": meta.get("liquidity_bucket", "unknown"),
            "correlated_cluster": meta.get("correlated_cluster", "unknown"),
            **event,
        }
    )
    if values["event_exclude"]:
        return None
    values["score"] = score_candidate(values)
    values["sell_risk_score"] = sell_risk_score(values)
    return values


def score_candidate(row: dict[str, Any]) -> float:
    overheat_penalty = max(float(row["ret20_prev_close"]) - 35.0, 0.0) * 1.15 + max(float(row["morning_return_pct"]) - 8.0, 0.0) * 1.6
    return (
        row["ret20_prev_close"] * 0.34
        + row["ret40_prev_close"] * 0.18
        + row["spy_excess20_prev_close"] * 0.20
        + row["qqq_excess20_prev_close"] * 0.16
        - row["vol20_prev_close"] * 1.55
        + row["drawdown40_prev_close"] * 0.08
        + (row["first_hour_positive_rate_10d"] - 0.5) * 5.0
        + row["morning_excess_spy_pct"] * 0.55
        + row["morning_excess_qqq_pct"] * 0.35
        + row["source_confidence_score"] * 4.0
        + row["event_score_adjustment"]
        - overheat_penalty
    )


def sell_risk_score(row: dict[str, Any]) -> float:
    breakdown = max(-float(row["ret20_prev_close"]), 0.0) * 0.28
    benchmark_lag = max(-float(row["spy_excess20_prev_close"]), 0.0) * 0.24 + max(-float(row["qqq_excess20_prev_close"]), 0.0) * 0.18
    drawdown = max(-float(row["drawdown40_prev_close"]) - 8.0, 0.0) * 0.18
    instability = max(float(row["vol20_prev_close"]) - 4.0, 0.0) * 0.45
    morning_failure = max(-float(row["morning_excess_spy_pct"]), 0.0) * 0.35
    confidence_penalty = (1.0 - float(row["source_confidence_score"])) * 2.0
    return breakdown + benchmark_lag + drawdown + instability + morning_failure + confidence_penalty - row["event_score_adjustment"]


def buy_candidates(rows: list[dict[str, Any]], config: dict[str, Any]) -> list[dict[str, Any]]:
    filters = config.get("filters", {})
    minimum_adv = float(filters.get("min_avg_daily_dollar_volume", 50_000_000.0))
    max_vol = float(filters.get("max_vol20", 8.5))
    minimum_confidence = float(filters.get("min_source_confidence_score", 0.50))
    filtered = [
        row
        for row in rows
        if row["avg_daily_dollar_volume"] >= minimum_adv
        and row["vol20_prev_close"] <= max_vol
        and row["ret40_prev_close"] > -12.0
        and row["ret20_prev_close"] > -3.0
        and row["source_confidence_score"] >= minimum_confidence
        and row.get("mcp_gap_count", 0) <= int(filters.get("max_mcp_gap_count", 999))
    ]
    top_n = int(config.get("selection", {}).get("top_n", 5))
    theme_cap = int(config.get("selection", {}).get("theme_cap", 2))
    selected = []
    theme_counts: Counter[str] = Counter()
    for row in sorted(filtered, key=lambda item: item["score"], reverse=True):
        theme = str(row["theme"])
        if theme_counts[theme] >= theme_cap:
            continue
        selected.append(row)
        theme_counts[theme] += 1
        if len(selected) >= top_n:
            break
    return selected


def sell_candidates(rows: list[dict[str, Any]], buy_symbols: set[str], config: dict[str, Any]) -> list[dict[str, Any]]:
    top_n = int(config.get("selection", {}).get("top_n", 5))
    filtered = [
        row
        for row in rows
        if row["symbol"] not in buy_symbols
        and (
            row["ret20_prev_close"] < 0.0
            or row["spy_excess20_prev_close"] < -2.0
            or row["qqq_excess20_prev_close"] < -2.0
            or row["drawdown40_prev_close"] < -12.0
            or row["sell_risk_score"] > 5.0
        )
    ]
    return sorted(filtered, key=lambda item: (item["sell_risk_score"], -item["score"]), reverse=True)[:top_n]


def path_rows_for_horizon(
    symbol: str,
    asof: str,
    horizon_days: int,
    indices: dict[str, dict[str, int]],
    daily: dict[str, list[dict[str, Any]]],
    hourly_by_day: dict[str, dict[str, list[dict[str, Any]]]],
    entry_dt: datetime,
) -> list[dict[str, Any]]:
    idx = indices[symbol][asof]
    target_idx = idx + horizon_days
    if target_idx >= len(daily[symbol]):
        return []
    target_date = str(daily[symbol][target_idx]["date"])
    dates = [str(row["date"]) for row in daily[symbol][idx : target_idx + 1]]
    rows = []
    for day in dates:
        for row in hourly_by_day.get(symbol, {}).get(day, []):
            if day == asof and row["dt_et"] < entry_dt:
                continue
            if day > target_date:
                continue
            rows.append(row)
    return rows


def evaluate_horizon(
    decision: dict[str, Any],
    horizon_name: str,
    horizon_days: int,
    indices: dict[str, dict[str, int]],
    daily: dict[str, list[dict[str, Any]]],
    hourly_by_day: dict[str, dict[str, list[dict[str, Any]]]],
    cost_model: dict[str, Any],
) -> dict[str, Any]:
    symbol = str(decision["symbol"])
    asof = str(decision["asof_date"])
    action = str(decision["action"])
    idx = indices[symbol][asof]
    spy_idx = indices["SPY"][asof]
    target_idx = idx + horizon_days
    spy_target_idx = spy_idx + horizon_days
    if target_idx >= len(daily[symbol]) or spy_target_idx >= len(daily["SPY"]):
        return {"horizon": horizon_name, "completed": False}
    entry_dt = datetime.fromisoformat(str(decision["asof_datetime_et"]))
    entry_price = float(decision["entry_price"])
    spy_entry = entry_bar_for(hourly_by_day.get("SPY", {}).get(asof, []))
    if not spy_entry:
        return {"horizon": horizon_name, "completed": False}
    exit_row = daily[symbol][target_idx]
    spy_exit_row = daily["SPY"][spy_target_idx]
    raw_return = pct(entry_price, float(exit_row["close"]))
    raw_after_cost = apply_round_trip_cost(raw_return, cost_model)
    spy_return = pct(float(spy_entry["close"]), float(spy_exit_row["close"]))
    excess = raw_return - spy_return
    excess_after_cost = raw_after_cost - spy_return
    if action == "virtual_buy":
        directional = excess_after_cost
        pl_pct = raw_return
        pl_after_cost = raw_after_cost
        avoided_return = None
    else:
        directional = -excess_after_cost
        pl_pct = 0.0
        pl_after_cost = 0.0
        avoided_return = -raw_after_cost
    path_rows = path_rows_for_horizon(symbol, asof, horizon_days, indices, daily, hourly_by_day, entry_dt)
    lows = [float(row["low"]) for row in path_rows]
    highs = [float(row["high"]) for row in path_rows]
    adverse_move = pct(entry_price, min(lows)) if lows and action == "virtual_buy" else None
    opportunity_cost = pct(entry_price, max(highs)) if highs and action == "virtual_sell" else None
    return {
        "horizon": horizon_name,
        "completed": True,
        "exit_date": str(exit_row["date"]),
        "exit_price": float(exit_row["close"]),
        "exit_reason": "horizon_close",
        "pl_pct": pl_pct,
        "pl_after_cost_pct": pl_after_cost,
        "avoided_return_after_cost_pct": avoided_return,
        "benchmark_return_pct": spy_return,
        "excess_spy_pct": excess,
        "excess_spy_after_cost_pct": excess_after_cost,
        "directional_excess_spy_after_cost_pct": directional,
        "adverse_move_pct": adverse_move,
        "opportunity_cost_max_rally_pct": opportunity_cost,
    }


def flatten_horizons(decision: dict[str, Any]) -> dict[str, Any]:
    out = dict(decision)
    for name, result in decision.get("horizon_results", {}).items():
        for key in ("pl_pct", "pl_after_cost_pct", "avoided_return_after_cost_pct", "benchmark_return_pct", "excess_spy_pct", "directional_excess_spy_after_cost_pct"):
            out[f"{name}_{key}"] = result.get(key)
    return out


def summarize_decisions(recommendations: list[dict[str, Any]], action: str | None = None) -> dict[str, Any]:
    subset = [row for row in recommendations if action is None or row["action"] == action]
    by_horizon: dict[str, Any] = {}
    for horizon_name, _ in HORIZONS:
        completed = [row["horizon_results"][horizon_name] for row in subset if row["horizon_results"][horizon_name].get("completed")]
        directional = [float(row["directional_excess_spy_after_cost_pct"]) for row in completed]
        raw_returns = [float(row["pl_after_cost_pct"]) for row in completed if row.get("pl_after_cost_pct") is not None]
        excess = [float(row["excess_spy_after_cost_pct"]) for row in completed if row.get("excess_spy_after_cost_pct") is not None]
        adverse = [float(row["adverse_move_pct"]) for row in completed if row.get("adverse_move_pct") is not None]
        opportunity = [float(row["opportunity_cost_max_rally_pct"]) for row in completed if row.get("opportunity_cost_max_rally_pct") is not None]
        ci_low, ci_high = bootstrap_mean_ci(directional) if directional else (None, None)
        by_horizon[horizon_name] = {
            "completed": len(completed),
            "hit_rate_directional_after_cost_pct": sum(1 for value in directional if value > 0.0) / len(directional) * 100.0 if directional else None,
            "avg_pl_after_cost_pct": mean(raw_returns),
            "avg_excess_spy_after_cost_pct": mean(excess),
            "avg_directional_excess_spy_after_cost_pct": mean(directional),
            "bootstrap_95_ci_directional_excess_pct": [ci_low, ci_high],
            "avg_adverse_move_pct": mean(adverse),
            "avg_opportunity_cost_max_rally_pct": mean(opportunity),
        }
    return {
        "action": action or "all",
        "asof_count": len({row["asof_date"] for row in subset}),
        "recommendations": len(subset),
        "by_horizon": by_horizon,
    }


def event_feature_summary(recommendations: list[dict[str, Any]], cache_used: bool) -> dict[str, Any]:
    matches = [row for row in recommendations if row.get("event_feature_present")]
    servers = sorted({server for row in matches for server in row.get("mcp_servers_used", [])})
    return {
        "event_feature_cache_used": cache_used,
        "recommendation_rows": len(recommendations),
        "event_feature_matches": len(matches),
        "event_feature_coverage_pct": len(matches) / len(recommendations) * 100.0 if recommendations else 0.0,
        "mcp_event_servers_used": servers,
        "mcp_event_gap_count": sum(int(row.get("mcp_gap_count", 0)) for row in matches),
    }


def daily_agent_report(asof: str, scored: list[dict[str, Any]], buys: list[dict[str, Any]], sells: list[dict[str, Any]], event_features: bool) -> dict[str, Any]:
    return {
        "date": asof,
        "agents": [
            {
                "agent": "Coordinator Agent",
                "status": "completed",
                "task": "paper-only dry-run 범위와 독립 기준일 확인",
                "findings": f"{asof} 기준 주문 제출 없이 독립 run 처리",
            },
            {
                "agent": "Universe Agent",
                "status": "completed",
                "task": "거래 가능 후보 universe 필터",
                "findings": f"scored={len(scored)}, buy_candidates={len(buys)}, sell_candidates={len(sells)}",
            },
            {
                "agent": "Market Data Agent",
                "status": "completed",
                "task": "Alpaca MCP 1Hour bars 기반 feature 생성",
                "findings": "전일 종가 lookback과 당일 오전 hourly feature 사용",
            },
            {
                "agent": "Web Research Agent",
                "status": "completed" if event_features else "data_gap",
                "task": "research MCP event feature cache 결합",
                "findings": "point-in-time feature cache 사용" if event_features else "event feature cache 미제공; metadata confidence만 사용",
            },
            {
                "agent": "Simulation Agent",
                "status": "completed",
                "task": "가상 매수/매도 선택 및 forward horizon 평가 준비",
                "findings": f"virtual_buy={len(buys)}, virtual_sell={len(sells)}",
            },
            {
                "agent": "Risk/Policy Agent",
                "status": "completed",
                "task": "주문 제출 차단과 정책 상태 확인",
                "findings": "orders_submitted=0; 단타/시간봉 기반 자동주문 승격 불가",
            },
        ],
    }


def simulate(
    hourly_by_day: dict[str, dict[str, list[dict[str, Any]]]],
    daily: dict[str, list[dict[str, Any]]],
    config: dict[str, Any],
    metadata: dict[str, Any],
    event_features: dict[str, list[dict[str, Any]]] | None = None,
    *,
    progress_enabled: bool = False,
) -> dict[str, Any]:
    indices = index_by_date(daily)
    benchmarks = set(config.get("benchmarks", [])) | BENCHMARKS_DEFAULT
    symbols = [symbol for symbol in sorted(daily) if symbol not in benchmarks]
    asof_dates = [str(row["date"]) for row in daily["SPY"]]
    recommendations: list[dict[str, Any]] = []
    agent_reports: list[dict[str, Any]] = []
    skipped_missing_dates = 0
    for asof in asof_dates:
        scored = []
        for symbol in symbols:
            features = candidate_features(symbol, asof, daily, indices, hourly_by_day, metadata, event_features)
            if features:
                scored.append(features)
            elif indices.get(symbol, {}).get(asof) is None:
                skipped_missing_dates += 1
        buys = buy_candidates(scored, config)
        sells = sell_candidates(scored, {row["symbol"] for row in buys}, config)
        if buys or sells:
            progress(
                progress_enabled,
                "Simulation Agent",
                f"{asof}: scored {len(scored)}개, virtual_buy {len(buys)}개, virtual_sell {len(sells)}개 평가",
            )
        agent_reports.append(daily_agent_report(asof, scored, buys, sells, bool(event_features)))
        for action, rows in (("virtual_buy", buys), ("virtual_sell", sells)):
            for rank, item in enumerate(rows, start=1):
                decision = dict(item)
                decision.update(
                    {
                        "action": action,
                        "rank": rank,
                        "strategy_id": "one-year-hourly-buy-sell-v1",
                        "policy_status": "research_dry_run_observation_only",
                        "independent_run_id": f"one-year-hourly-buy-sell-v1:{asof}:{action}",
                        "orders_submitted": 0,
                        "order_submission_allowed": False,
                        "position_effect": "open_virtual_long" if action == "virtual_buy" else "sell_or_avoid_existing_long_only_no_short",
                    }
                )
                decision["horizon_results"] = {
                    horizon_name: evaluate_horizon(
                        decision,
                        horizon_name,
                        horizon_days,
                        indices,
                        daily,
                        hourly_by_day,
                        config.get("cost_model", {}),
                    )
                    for horizon_name, horizon_days in HORIZONS
                }
                recommendations.append(round_json(decision))
    flattened = [flatten_horizons(row) for row in recommendations]
    completed_20d = [
        float(row["horizon_results"]["20D"]["directional_excess_spy_after_cost_pct"])
        for row in recommendations
        if row["horizon_results"]["20D"].get("completed")
    ]
    return {
        "summary": {
            "strategy_id": "one-year-hourly-buy-sell-v1",
            "policy_status": "research_dry_run_observation_only",
            "auto_orders_allowed": False,
            "daily_independent_runs": len({row["asof_date"] for row in recommendations}),
            "recommendations": len(recommendations),
            "virtual_buy_recommendations": sum(1 for row in recommendations if row["action"] == "virtual_buy"),
            "virtual_sell_recommendations": sum(1 for row in recommendations if row["action"] == "virtual_sell"),
            "completed_20d": len(completed_20d),
            "hit_rate_20d_directional_after_cost_pct": sum(1 for value in completed_20d if value > 0.0) / len(completed_20d) * 100.0 if completed_20d else None,
            "avg_20d_directional_excess_after_cost_pct": mean(completed_20d),
            "skipped_missing_symbol_dates": skipped_missing_dates,
            "costs_applied": True,
            "fill_model": "virtual entry at second available 1Hour bar close; horizon exits at regular-session daily close",
            "slippage_model": "strategy config round-trip spread/slippage bps applied to directional evaluation",
            "event_features": event_feature_summary(recommendations, bool(event_features)),
            "actions": {
                "all": summarize_decisions(recommendations),
                "virtual_buy": summarize_decisions(recommendations, "virtual_buy"),
                "virtual_sell": summarize_decisions(recommendations, "virtual_sell"),
            },
        },
        "recommendations": recommendations,
        "recommendations_flat": round_json(flattened),
        "agent_daily_reports": agent_reports,
    }


def format_pct(value: float | None) -> str:
    if value is None:
        return "n/a"
    return f"{value:+.2f}%"


def table(headers: list[str], rows: list[list[str]]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    lines.extend("| " + " | ".join(row) + " |" for row in rows)
    return "\n".join(lines)


def render_markdown(output: dict[str, Any]) -> str:
    summary = output["simulation"]["summary"]
    manifest = output["data_manifest"]
    action_rows = []
    for action_label in ("virtual_buy", "virtual_sell"):
        action_summary = summary["actions"][action_label]
        horizons = action_summary["by_horizon"]
        for horizon in ("same_day", "1D", "5D", "20D", "60D"):
            row = horizons[horizon]
            action_rows.append(
                [
                    action_label,
                    horizon,
                    str(row["completed"]),
                    "n/a" if row["hit_rate_directional_after_cost_pct"] is None else f"{row['hit_rate_directional_after_cost_pct']:.2f}%",
                    format_pct(row["avg_directional_excess_spy_after_cost_pct"]),
                    format_pct(row["avg_pl_after_cost_pct"]),
                    format_pct(row["avg_adverse_move_pct"] if action_label == "virtual_buy" else row["avg_opportunity_cost_max_rally_pct"]),
                ]
            )
    top20 = []
    for row in output["simulation"]["recommendations"][:]:
        result = row["horizon_results"].get("20D", {})
        if result.get("completed"):
            top20.append((row, float(result["directional_excess_spy_after_cost_pct"])))
    top20 = sorted(top20, key=lambda item: item[1], reverse=True)[:10]
    top_rows = [
        [
            row["asof_date"],
            row["action"],
            row["symbol"],
            str(row["rank"]),
            format_pct(value),
            format_pct(row["horizon_results"]["5D"].get("directional_excess_spy_after_cost_pct")),
        ]
        for row, value in top20
    ]
    event = summary["event_features"]
    return "\n".join(
        [
            "---",
            f"id: {output['run_id']}",
            f"created_at: {output['created_at']}",
            "source_type: one-year-hourly-buy-sell-simulation",
            "paper: true",
            "orders_submitted: 0",
            "---",
            "",
            "# 과거 1년 1시간봉 일별 매입/매도 dry-run 시뮬레이션",
            "",
            "## 결론",
            "",
            f"- 전략: `{summary['strategy_id']}`",
            f"- 정책 상태: `{summary['policy_status']}`",
            f"- 일별 독립 run 수: {summary['daily_independent_runs']}",
            f"- 전체 추천: {summary['recommendations']}개, virtual buy {summary['virtual_buy_recommendations']}개, virtual sell {summary['virtual_sell_recommendations']}개",
            f"- 20D 완료 평가: {summary['completed_20d']}개",
            f"- 20D 방향성 hit rate: {summary['hit_rate_20d_directional_after_cost_pct']:.2f}%" if summary["hit_rate_20d_directional_after_cost_pct"] is not None else "- 20D 방향성 hit rate: n/a",
            f"- 20D 평균 방향성 SPY 초과수익: {summary['avg_20d_directional_excess_after_cost_pct']:+.2f}%" if summary["avg_20d_directional_excess_after_cost_pct"] is not None else "- 20D 평균 방향성 SPY 초과수익: n/a",
            "",
            "virtual sell은 short 주문이 아니라 기존 long 보유분을 팔거나 신규 매수를 피하는 dry-run 판단으로 평가했다. 따라서 sell 평가의 방향성 수익은 해당 종목이 이후 SPY보다 부진했는지를 보는 회피 성과다.",
            "",
            "## 단기/장기 평가",
            "",
            table(
                ["action", "horizon", "completed", "directional hit", "avg directional SPY excess", "avg long P/L", "avg adverse/opportunity"],
                action_rows,
            ),
            "",
            "## 상위 20D 방향성 결과",
            "",
            table(["asof", "action", "symbol", "rank", "20D directional", "5D directional"], top_rows) if top_rows else "완료된 20D 결과가 없다.",
            "",
            "## 에이전트 진행 기록",
            "",
            f"- 일별 agent report: {len(output['simulation']['agent_daily_reports'])}일치가 JSON에 저장됐다.",
            "- Coordinator/Universe/Market Data/Web Research/Simulation/Risk-Policy Agent가 각 기준일 상태를 기록했다.",
            "- 실행 중 Codex 작업창에는 Market Data Agent와 Simulation Agent 진행 줄을 출력하도록 `--progress`를 사용했다.",
            "",
            "## 데이터 품질과 MCP",
            "",
            f"- source feed: `{manifest.get('source_feed')}`",
            f"- bar interval: `{manifest.get('bar_interval')}`",
            f"- symbols loaded: {manifest.get('symbols_loaded')} / {manifest.get('symbols_requested')}",
            f"- hourly bars loaded: {manifest.get('bars_loaded')}",
            f"- fill model: {summary['fill_model']}",
            f"- slippage model: {summary['slippage_model']}",
            f"- event feature cache 사용: {str(event['event_feature_cache_used']).lower()}",
            f"- event feature 매칭: {event['event_feature_matches']} / {event['recommendation_rows']} ({event['event_feature_coverage_pct']:.2f}%)",
            f"- research MCP 서버: {', '.join(event['mcp_event_servers_used']) if event['mcp_event_servers_used'] else '없음'}",
            f"- 원천 hash: `{manifest.get('dataset_hash')}`",
            "",
            "## 정책 반영",
            "",
            "- 이 결과는 research/backtest 전용이며 `orders_submitted=0`이다.",
            "- 1시간봉 기반 판단은 자동 주문 후보로 승격하지 않고 `observation_only`로 유지한다.",
            "- 실제 정책 변경은 별도 proposal과 추가 out-of-sample 검증이 필요하다.",
            "",
        ]
    )


def render_source_markdown(output: dict[str, Any]) -> str:
    manifest = output["data_manifest"]
    return "\n".join(
        [
            "---",
            f"id: {output['run_id']}-sources",
            f"created_at: {output['created_at']}",
            "source_type: alpaca-mcp-hourly-backtest-source",
            "paper: true",
            "orders_submitted: 0",
            "---",
            "",
            "# 과거 1년 1시간봉 매입/매도 시뮬레이션 원천",
            "",
            "## 조회 원천",
            "",
            "- Alpaca MCP: `get_stock_bars`",
            "- 캡처 스크립트: `scripts/fetch-alpaca-hourly-bars-mcp.py`",
            f"- 기간: {output['data_window']['start']} ~ {output['data_window']['end']}",
            f"- time frame: `{manifest.get('bar_interval')}`",
            f"- feed: `{manifest.get('source_feed')}`",
            f"- adjustment: `{output['data_window']['adjustment']}`",
            f"- raw JSON: `{manifest.get('raw_input_file')}`",
            f"- simulation JSON: `{output['output_json']}`",
            f"- scorecard JSON: `{output.get('scorecard_json') or '없음'}`",
            "",
            "## 데이터 품질",
            "",
            f"- symbols_requested: {manifest.get('symbols_requested')}",
            f"- symbols_loaded: {manifest.get('symbols_loaded')}",
            f"- hourly bars loaded: {manifest.get('bars_loaded')}",
            f"- missing_symbols: {manifest.get('missing_symbols')}",
            f"- stale_quotes: {manifest.get('stale_quotes')}",
            f"- corporate_actions_checked: {str(manifest.get('corporate_actions_checked')).lower()}",
            f"- survivorship_bias_controlled: {str(manifest.get('survivorship_bias_controlled')).lower()}",
            f"- dataset_hash: `{manifest.get('dataset_hash')}`",
            "",
            "## 데이터 공백",
            "",
            "- 1시간봉에는 quote-level bid/ask, queue priority, limit-fill probability가 없다.",
            "- IEX feed는 SIP 통합 체결/거래량과 다를 수 있다.",
            "- 현재 중앙 universe 기준이므로 survivorship bias 통제가 완전하지 않다.",
            "- event feature cache가 없으면 SEC/실적/애널리스트/밸류에이션/매크로 맥락은 점수에 직접 반영되지 않는다.",
            "",
        ]
    )


def manifest_output(output: dict[str, Any], args: argparse.Namespace) -> dict[str, Any]:
    risk_policy = load_yaml(args.risk_policy_yaml)
    return {
        "run_id": output["run_id"],
        "mode": "research",
        "paper": True,
        "orders_submitted": 0,
        "created_at": output["created_at"],
        "schema_version": "1.1",
        "risk_policy_version": risk_policy.get("policy_version", risk_policy.get("version", "unknown")),
        "recommendation_policy_sha": file_sha256(args.recommendation_policy_yaml),
        "mcp_servers_used": ["alpaca"],
        "mcp_failures": [],
        "data_cutoff_time": output["data_window"]["end"],
        "source_refs": [
            str(args.source_md),
            str(args.input_json),
            str(args.output_json),
            str(args.output_md),
        ]
        + ([str(args.event_features_json)] if args.event_features_json else [])
        + ([str(args.scorecard_json)] if args.scorecard_json else []),
        "risk_check_result": {
            "status": "NOT_APPLICABLE",
            "reason": "research hourly backtest only; no order plan generated",
        },
        "data_manifest": output["data_manifest"],
        "submitted_order_ids": [],
        "post_trade_check_path": "",
    }


def main() -> None:
    args = parse_args()
    source = json.loads(args.input_json.read_text(encoding="utf-8"))
    config = load_yaml(args.strategy_config)
    metadata = load_yaml(args.metadata_yaml)
    event_features = load_event_features(args.event_features_json)
    raw_rows = source.get("extracted", {}).get("hourly_bars")
    if not isinstance(raw_rows, dict) or "SPY" not in raw_rows or "QQQ" not in raw_rows:
        raise SystemExit("input JSON must contain extracted.hourly_bars with SPY and QQQ")

    progress(args.progress, "Coordinator Agent", "hourly raw source 확인 완료; 일별 집계와 feature 생성을 시작합니다.")
    hourly_by_day = build_hourly_by_day(raw_rows)
    daily = aggregate_daily(hourly_by_day)
    progress(args.progress, "Market Data Agent", f"{len(daily)}개 심볼의 1Hour bars를 일별 feature로 집계했습니다.")
    simulation = simulate(hourly_by_day, daily, config, metadata, event_features, progress_enabled=args.progress)
    data_manifest = {
        **source.get("data_manifest", {}),
        "dataset_hash": file_sha256(args.input_json),
        "raw_input_file": str(args.input_json),
        "fill_model": simulation["summary"]["fill_model"],
        "slippage_model": simulation["summary"]["slippage_model"],
        "daily_bar_count_from_hourly": sum(len(rows) for rows in daily.values()),
    }
    if args.event_features_json:
        data_manifest["event_feature_cache_file"] = str(args.event_features_json)
        data_manifest["event_feature_cache_hash"] = file_sha256(args.event_features_json)
    output = {
        "run_id": args.run_id,
        "created_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "paper": True,
        "orders_submitted": 0,
        "strategy_config": str(args.strategy_config),
        "metadata_yaml": str(args.metadata_yaml),
        "event_features_json": str(args.event_features_json) if args.event_features_json else "",
        "data_window": {
            "start": source.get("request", {}).get("start"),
            "end": source.get("request", {}).get("end"),
            "timeframe": source.get("request", {}).get("timeframe"),
            "feed": source.get("request", {}).get("feed"),
            "adjustment": source.get("request", {}).get("adjustment"),
        },
        "data_manifest": data_manifest,
        "data_gaps": source.get("data_gaps", [])
        + [
            "Hourly bar dry-run cannot prove quote-level fill probability.",
            "Virtual sell recommendations are long-only sell/avoid signals, not short-sale simulations.",
        ],
        "simulation": simulation,
        "output_json": str(args.output_json),
        "output_md": str(args.output_md),
        "source_md": str(args.source_md),
        "scorecard_json": str(args.scorecard_json) if args.scorecard_json else "",
    }

    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(round_json(output), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.write_text(render_markdown(round_json(output)), encoding="utf-8")
    args.source_md.parent.mkdir(parents=True, exist_ok=True)
    args.source_md.write_text(render_source_markdown(round_json(output)), encoding="utf-8")
    if args.scorecard_json:
        scorecard = {
            "created_at": output["created_at"],
            "strategy_id": simulation["summary"]["strategy_id"],
            "policy_status": simulation["summary"]["policy_status"],
            "summary": simulation["summary"],
            "promotion_decision": "observation_only",
            "promotion_reason": "hourly buy/sell dry-run uses virtual fills and long-only sell/avoid signals; not eligible for automatic orders",
            "event_feature_cache_used": bool(args.event_features_json),
            "orders_submitted": 0,
        }
        args.scorecard_json.parent.mkdir(parents=True, exist_ok=True)
        args.scorecard_json.write_text(json.dumps(round_json(scorecard), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    if args.run_manifest:
        manifest = manifest_output(round_json(output), args)
        args.run_manifest.parent.mkdir(parents=True, exist_ok=True)
        args.run_manifest.write_text(json.dumps(round_json(manifest), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    progress(args.progress, "Wiki Curator Agent", "결과 Markdown, source note, scorecard, run manifest 생성을 완료했습니다.")


if __name__ == "__main__":
    main()
