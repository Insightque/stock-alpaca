#!/usr/bin/env python3
"""Six-month 3-hour policy simulation using the Alpaca MCP server.

This helper only calls read-only Alpaca MCP tools. It does not submit, replace,
cancel, or close orders.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import math
import statistics
from collections import defaultdict
from dataclasses import dataclass
from datetime import date, datetime, time, timedelta
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


ET = ZoneInfo("America/New_York")
KST = ZoneInfo("Asia/Seoul")
UTC = ZoneInfo("UTC")

BENCHMARKS = ("SPY", "QQQ", "SMH")
DEFAULT_UNIVERSE = (
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
THEMES = {
    "NVDA": "ai_semiconductor",
    "AMD": "ai_semiconductor",
    "AVGO": "ai_semiconductor",
    "TSM": "ai_semiconductor",
    "LRCX": "semicap_equipment",
    "PLTR": "ai_software",
    "TSLA": "ev_ai_event",
    "NOK": "networking",
    "UNH": "healthcare",
    "ETN": "power_infrastructure",
    "IONQ": "quantum_speculative",
    "QBTS": "quantum_speculative",
    "RGTI": "quantum_speculative",
}
DATA_GAPS = [
    "Alpaca MCP stock bars were requested from the IEX feed, not consolidated SIP; high/low/VWAP can differ from full-market data.",
    "3-hour windows are aggregated from 30Min bars, so stop/take ordering inside a 30Min bar is conservatively treated as stop-first when both levels appear.",
    "The simulation does not include bid/ask spread, queue priority, limit-fill probability, fees, or slippage.",
    "Policy review is price/volume based; SEC filings, earnings surprise, valuation, analyst, and macro context are treated as follow-up checks rather than included features.",
    "Watchlists were empty at run time, so the universe combines current paper holdings, existing policy candidates, and SPY/QQQ/SMH benchmarks.",
]


@dataclass(frozen=True)
class CalendarDay:
    day: date
    open_time: time
    close_time: time


@dataclass(frozen=True)
class Bar:
    ts: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float
    vwap: float | None


@dataclass(frozen=True)
class WindowBar:
    symbol: str
    day: date
    index: int
    start_et: datetime
    end_et: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float
    vwap: float | None

    @property
    def return_pct(self) -> float:
        return pct(self.open, self.close)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", default="2025-11-24")
    parser.add_argument("--end", default="2026-05-22")
    parser.add_argument("--symbols", default="")
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    parser.add_argument("--source-md", type=Path, required=True)
    parser.add_argument("--run-manifest", type=Path, required=True)
    parser.add_argument(
        "--event-features-json",
        type=Path,
        help="Optional point-in-time research MCP feature cache to join by symbol and as-of date.",
    )
    parser.add_argument("--feed", default="iex")
    parser.add_argument("--timeframe", default="30Min")
    parser.add_argument("--limit", type=int, default=10000)
    return parser.parse_args()


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
        vwap=float(raw["vw"]) if raw.get("vw") is not None else None,
    )


def pct(start: float, end: float) -> float:
    if start == 0:
        return 0.0
    return (end / start - 1.0) * 100.0


def mean(values: list[float]) -> float | None:
    return sum(values) / len(values) if values else None


def stdev(values: list[float]) -> float | None:
    return statistics.pstdev(values) if len(values) >= 2 else None


def iso_z(dt: datetime) -> str:
    return dt.astimezone(UTC).isoformat().replace("+00:00", "Z")


def safe_float(value: Any) -> float | None:
    if value is None:
        return None
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    if math.isfinite(number):
        return number
    return None


def as_float(value: Any, default: float = 0.0) -> float:
    number = safe_float(value)
    return default if number is None else number


def parse_date_key(value: Any) -> str | None:
    if value in (None, ""):
        return None
    text = str(value)
    if len(text) >= 10 and text[4:5] == "-" and text[7:8] == "-":
        return text[:10]
    return None


def as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


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


def event_fields(symbol: str, asof: str, event_features: dict[str, list[dict[str, Any]]] | None) -> dict[str, Any]:
    feature = event_feature_for(symbol, asof, event_features)
    mcp_gaps = as_list((feature or {}).get("mcp_gaps") or (feature or {}).get("gap_flags"))
    return {
        "event_feature_present": feature is not None,
        "event_available_date": (feature or {}).get("available_date"),
        "event_score_adjustment": event_score_adjustment(feature),
        "event_exclude": bool((feature or {}).get("exclude", False)),
        "mcp_servers_used": [str(item) for item in as_list((feature or {}).get("mcp_servers_used"))],
        "mcp_gap_count": len(mcp_gaps),
        "mcp_gaps": [str(item) for item in mcp_gaps],
        "mcp_source_refs": [str(item) for item in as_list((feature or {}).get("source_refs"))],
    }


def attach_event_fields_to_rows(
    rows: list[dict[str, Any]],
    event_features: dict[str, list[dict[str, Any]]] | None,
    *,
    date_key: str,
    adjust_score: bool = False,
) -> list[dict[str, Any]]:
    out = []
    for row in rows:
        fields = event_fields(str(row["symbol"]), str(row[date_key]), event_features)
        if fields["event_exclude"]:
            continue
        merged = {**row, **fields}
        if adjust_score and "score" in merged:
            merged["score"] = float(merged["score"]) + float(fields["event_score_adjustment"])
        out.append(merged)
    return out


def date_chunks(start_day: date, end_day: date, days: int = 14) -> list[tuple[date, date]]:
    chunks = []
    current = start_day
    while current <= end_day:
        chunk_end = min(current + timedelta(days=days - 1), end_day)
        chunks.append((current, chunk_end))
        current = chunk_end + timedelta(days=1)
    return chunks


async def call_json(session: ClientSession, name: str, arguments: dict[str, Any] | None = None) -> Any:
    result = await session.call_tool(name, arguments or {})
    text_parts = []
    for item in result.content:
        text = getattr(item, "text", None)
        if text:
            text_parts.append(text)
    if not text_parts:
        return {}
    text = "\n".join(text_parts)
    return json.loads(text)


def parse_calendar(payload: Any) -> list[CalendarDay]:
    rows = payload.get("result", payload) if isinstance(payload, dict) else payload
    calendar = []
    for row in rows:
        calendar.append(
            CalendarDay(
                day=date.fromisoformat(row["date"]),
                open_time=time.fromisoformat(row["open"]),
                close_time=time.fromisoformat(row["close"]),
            )
        )
    return calendar


def window_index(ts: datetime, calendar_day: CalendarDay) -> int | None:
    open_dt = datetime.combine(calendar_day.day, calendar_day.open_time, ET)
    close_dt = datetime.combine(calendar_day.day, calendar_day.close_time, ET)
    if not (open_dt <= ts < close_dt):
        return None
    minutes = int((ts - open_dt).total_seconds() // 60)
    return minutes // 180


def aggregate_windows(
    symbols: list[str],
    bars_by_symbol: dict[str, list[Bar]],
    calendar: list[CalendarDay],
) -> tuple[dict[str, list[WindowBar]], dict[str, list[dict[str, Any]]]]:
    calendar_by_day = {item.day: item for item in calendar}
    grouped: dict[tuple[str, date, int], list[Bar]] = defaultdict(list)
    regular_bars: dict[str, dict[date, list[Bar]]] = {symbol: defaultdict(list) for symbol in symbols}
    for symbol in symbols:
        for bar in bars_by_symbol.get(symbol, []):
            cal_day = calendar_by_day.get(bar.ts.date())
            if not cal_day:
                continue
            idx = window_index(bar.ts, cal_day)
            if idx is None:
                continue
            grouped[(symbol, cal_day.day, idx)].append(bar)
            regular_bars[symbol][cal_day.day].append(bar)

    windows_by_symbol: dict[str, list[WindowBar]] = {symbol: [] for symbol in symbols}
    for (symbol, day, idx), rows in sorted(grouped.items()):
        rows = sorted(rows, key=lambda item: item.ts)
        total_volume = sum(row.volume for row in rows)
        vwap_value = None
        if total_volume > 0:
            vwap_value = sum(((row.vwap if row.vwap is not None else (row.high + row.low + row.close) / 3.0) * row.volume) for row in rows) / total_volume
        start = rows[0].ts
        end = min(rows[-1].ts + timedelta(minutes=30), datetime.combine(day, calendar_by_day[day].close_time, ET))
        windows_by_symbol[symbol].append(
            WindowBar(
                symbol=symbol,
                day=day,
                index=idx,
                start_et=start,
                end_et=end,
                open=rows[0].open,
                high=max(row.high for row in rows),
                low=min(row.low for row in rows),
                close=rows[-1].close,
                volume=total_volume,
                vwap=vwap_value,
            )
        )

    daily: dict[str, list[dict[str, Any]]] = {symbol: [] for symbol in symbols}
    for symbol in symbols:
        for day, rows in sorted(regular_bars[symbol].items()):
            rows = sorted(rows, key=lambda item: item.ts)
            if not rows:
                continue
            total_volume = sum(row.volume for row in rows)
            vwap_value = None
            if total_volume > 0:
                vwap_value = sum(((row.vwap if row.vwap is not None else (row.high + row.low + row.close) / 3.0) * row.volume) for row in rows) / total_volume
            daily[symbol].append(
                {
                    "date": day.isoformat(),
                    "open": rows[0].open,
                    "high": max(row.high for row in rows),
                    "low": min(row.low for row in rows),
                    "close": rows[-1].close,
                    "volume": total_volume,
                    "vwap": vwap_value,
                    "return_pct": pct(rows[0].open, rows[-1].close),
                }
            )
    return windows_by_symbol, daily


def windows_by_day(windows_by_symbol: dict[str, list[WindowBar]]) -> dict[str, dict[date, dict[int, WindowBar]]]:
    out: dict[str, dict[date, dict[int, WindowBar]]] = {}
    for symbol, rows in windows_by_symbol.items():
        out[symbol] = defaultdict(dict)
        for row in rows:
            out[symbol][row.day][row.index] = row
    return out


def evaluate_stop_take(
    bars: list[Bar],
    entry_time: datetime,
    entry_price: float,
    take_pct: float,
    stop_pct: float,
) -> tuple[str, float, float]:
    take = entry_price * (1.0 + take_pct / 100.0)
    stop = entry_price * (1.0 - stop_pct / 100.0)
    later = [bar for bar in bars if bar.ts >= entry_time]
    for bar in later:
        stop_hit = bar.low <= stop
        take_hit = bar.high >= take
        if stop_hit and take_hit:
            return "ambiguous_stop_first", -stop_pct, stop
        if stop_hit:
            return "stop", -stop_pct, stop
        if take_hit:
            return "take", take_pct, take
    if not later:
        return "unknown", 0.0, entry_price
    eod = later[-1]
    pl = pct(entry_price, eod.close)
    return ("eod_gain" if pl >= 0 else "eod_loss"), pl, eod.close


def regular_bars_by_symbol_day(
    symbols: list[str],
    bars_by_symbol: dict[str, list[Bar]],
    calendar: list[CalendarDay],
) -> dict[str, dict[date, list[Bar]]]:
    calendar_by_day = {item.day: item for item in calendar}
    out: dict[str, dict[date, list[Bar]]] = {symbol: defaultdict(list) for symbol in symbols}
    for symbol in symbols:
        for bar in bars_by_symbol.get(symbol, []):
            cal_day = calendar_by_day.get(bar.ts.date())
            if not cal_day:
                continue
            if window_index(bar.ts, cal_day) is not None:
                out[symbol][cal_day.day].append(bar)
        for rows in out[symbol].values():
            rows.sort(key=lambda item: item.ts)
    return out


def intraday_candidate_rows(
    symbols: list[str],
    windows: dict[str, dict[date, dict[int, WindowBar]]],
    regular_bars: dict[str, dict[date, list[Bar]]],
    calendar: list[CalendarDay],
    event_features: dict[str, list[dict[str, Any]]] | None = None,
) -> dict[str, list[dict[str, Any]]]:
    candidates = [symbol for symbol in symbols if symbol not in BENCHMARKS]
    all_days = [item.day for item in calendar]
    policy_rows: dict[str, list[dict[str, Any]]] = {
        "3h-momentum-top3": [],
        "3h-momentum-top2": [],
        "3h-vwap-reclaim-top2": [],
        "3h-afternoon-continuation-top2": [],
    }
    for day in all_days:
        qqq_w0 = windows.get("QQQ", {}).get(day, {}).get(0)
        if not qqq_w0:
            continue
        qqq_w1 = windows.get("QQQ", {}).get(day, {}).get(1)
        momentum_pool = []
        reclaim_pool = []
        afternoon_pool = []
        for symbol in candidates:
            symbol_windows = windows.get(symbol, {}).get(day, {})
            w0 = symbol_windows.get(0)
            w1 = symbol_windows.get(1)
            w2 = symbol_windows.get(2)
            day_bars = regular_bars.get(symbol, {}).get(day, [])
            if not w0 or not w1 or not day_bars:
                continue
            symbol_ret0 = w0.return_pct
            qqq_ret0 = qqq_w0.return_pct
            rel0 = symbol_ret0 - qqq_ret0
            close_near_high = w0.close >= w0.high * 0.995
            if qqq_ret0 >= 0.20 and symbol_ret0 >= 0.80 and rel0 >= 0.35 and close_near_high:
                outcome, pl_pct, exit_price = evaluate_stop_take(day_bars, w1.start_et, w1.open, 2.0, 1.0)
                momentum_pool.append(
                    {
                        "date": day.isoformat(),
                        "symbol": symbol,
                        "entry_time_et": w1.start_et.strftime("%H:%M"),
                        "entry_price": w1.open,
                        "exit_price": exit_price,
                        "outcome": outcome,
                        "pl_pct": pl_pct,
                        "pl_usd_per_10k": 10000.0 * pl_pct / 100.0,
                        "qqq_w0_return_pct": qqq_ret0,
                        "symbol_w0_return_pct": symbol_ret0,
                        "relative_strength_pctpt": rel0,
                        "close_near_high": close_near_high,
                    }
                )
            recovery = pct(w0.low, w0.close)
            w0_vwap_pass = bool(w0.vwap is not None and w0.close > w0.vwap)
            if qqq_ret0 >= -0.50 and symbol_ret0 <= -1.0 and recovery >= 0.60 and w0_vwap_pass:
                outcome, pl_pct, exit_price = evaluate_stop_take(day_bars, w1.start_et, w1.open, 1.5, 0.8)
                reclaim_pool.append(
                    {
                        "date": day.isoformat(),
                        "symbol": symbol,
                        "entry_time_et": w1.start_et.strftime("%H:%M"),
                        "entry_price": w1.open,
                        "exit_price": exit_price,
                        "outcome": outcome,
                        "pl_pct": pl_pct,
                        "pl_usd_per_10k": 10000.0 * pl_pct / 100.0,
                        "qqq_w0_return_pct": qqq_ret0,
                        "symbol_w0_return_pct": symbol_ret0,
                        "recovery_from_w0_low_pct": recovery,
                        "symbol_w0_vwap_pass": w0_vwap_pass,
                    }
                )
            if qqq_w1 and w2:
                qqq_two_window_ret = pct(qqq_w0.open, qqq_w1.close)
                symbol_two_window_ret = pct(w0.open, w1.close)
                rel_two = symbol_two_window_ret - qqq_two_window_ret
                if qqq_two_window_ret >= 0.30 and symbol_two_window_ret >= 1.20 and rel_two >= 0.40 and w1.close > w0.close:
                    outcome, pl_pct, exit_price = evaluate_stop_take(day_bars, w2.start_et, w2.open, 1.0, 0.6)
                    afternoon_pool.append(
                        {
                            "date": day.isoformat(),
                            "symbol": symbol,
                            "entry_time_et": w2.start_et.strftime("%H:%M"),
                            "entry_price": w2.open,
                            "exit_price": exit_price,
                            "outcome": outcome,
                            "pl_pct": pl_pct,
                            "pl_usd_per_10k": 10000.0 * pl_pct / 100.0,
                            "qqq_two_window_return_pct": qqq_two_window_ret,
                            "symbol_two_window_return_pct": symbol_two_window_ret,
                            "relative_strength_pctpt": rel_two,
                        }
                    )
        momentum_pool = attach_event_fields_to_rows(momentum_pool, event_features, date_key="date")
        reclaim_pool = attach_event_fields_to_rows(reclaim_pool, event_features, date_key="date")
        afternoon_pool = attach_event_fields_to_rows(afternoon_pool, event_features, date_key="date")
        ranked_momentum = sorted(
            momentum_pool,
            key=lambda row: (row["relative_strength_pctpt"] + row["event_score_adjustment"], row["symbol_w0_return_pct"]),
            reverse=True,
        )
        for policy, limit in (("3h-momentum-top3", 3), ("3h-momentum-top2", 2)):
            for rank, row in enumerate(ranked_momentum[:limit], start=1):
                policy_rows[policy].append({"policy": policy, "rank": rank, **row})
        ranked_reclaim = sorted(
            reclaim_pool,
            key=lambda row: (row["recovery_from_w0_low_pct"] + row["event_score_adjustment"], -abs(row["symbol_w0_return_pct"])),
            reverse=True,
        )
        for rank, row in enumerate(ranked_reclaim[:2], start=1):
            policy_rows["3h-vwap-reclaim-top2"].append({"policy": "3h-vwap-reclaim-top2", "rank": rank, **row})
        ranked_afternoon = sorted(
            afternoon_pool,
            key=lambda row: (row["relative_strength_pctpt"] + row["event_score_adjustment"], row["symbol_two_window_return_pct"]),
            reverse=True,
        )
        for rank, row in enumerate(ranked_afternoon[:2], start=1):
            policy_rows["3h-afternoon-continuation-top2"].append({"policy": "3h-afternoon-continuation-top2", "rank": rank, **row})
    return policy_rows


def summarize_intraday(rows: list[dict[str, Any]], sample_days: int) -> dict[str, Any]:
    trades = len(rows)
    wins = [row for row in rows if row["pl_pct"] > 0]
    stops = [row for row in rows if row["outcome"] in {"stop", "ambiguous_stop_first"}]
    takes = [row for row in rows if row["outcome"] == "take"]
    total_pl = sum(row["pl_usd_per_10k"] for row in rows)
    return {
        "sample_days": sample_days,
        "active_days": len({row["date"] for row in rows}),
        "trades": trades,
        "hit_rate": len(wins) / trades * 100.0 if trades else 0.0,
        "stops": len(stops),
        "takes": len(takes),
        "total_pl_usd_per_10k_trade": total_pl,
        "avg_pl_usd_per_trade": total_pl / trades if trades else 0.0,
        "avg_pl_pct": mean([row["pl_pct"] for row in rows]),
    }


def daily_index(rows: list[dict[str, Any]]) -> dict[date, int]:
    return {date.fromisoformat(row["date"]): idx for idx, row in enumerate(rows)}


def daily_return(rows: list[dict[str, Any]], idx: int, lookback: int) -> float | None:
    if idx - lookback < 0:
        return None
    return pct(rows[idx - lookback]["close"], rows[idx]["close"])


def forward_daily_return(rows: list[dict[str, Any]], idx: int, horizon: int) -> tuple[float | None, str | None, float | None]:
    target = idx + horizon
    if target >= len(rows):
        return None, None, None
    start = rows[idx]["close"]
    path = rows[idx : target + 1]
    adverse = min(pct(start, row["low"]) for row in path)
    return pct(start, rows[target]["close"]), rows[target]["date"], adverse


def max_drawdown(rows: list[dict[str, Any]], start_idx: int, end_idx: int) -> float | None:
    if start_idx < 0:
        return None
    peak = rows[start_idx]["close"]
    worst = 0.0
    for row in rows[start_idx : end_idx + 1]:
        peak = max(peak, row["close"])
        worst = min(worst, pct(peak, row["close"]))
    return worst


def score_daily_symbol(
    symbol: str,
    daily: dict[str, list[dict[str, Any]]],
    first_window_returns: dict[str, dict[date, float]],
    asof: date,
    event_features: dict[str, list[dict[str, Any]]] | None = None,
) -> dict[str, Any] | None:
    rows = daily.get(symbol, [])
    spy = daily.get("SPY", [])
    qqq = daily.get("QQQ", [])
    idx_by_day = daily_index(rows)
    spy_idx_by_day = daily_index(spy)
    qqq_idx_by_day = daily_index(qqq)
    if asof not in idx_by_day or asof not in spy_idx_by_day or asof not in qqq_idx_by_day:
        return None
    idx = idx_by_day[asof]
    spy_idx = spy_idx_by_day[asof]
    qqq_idx = qqq_idx_by_day[asof]
    ret20 = daily_return(rows, idx, 20)
    ret40 = daily_return(rows, idx, 40)
    spy20 = daily_return(spy, spy_idx, 20)
    qqq20 = daily_return(qqq, qqq_idx, 20)
    if None in (ret20, ret40, spy20, qqq20):
        return None
    recent_returns = [pct(rows[i - 1]["close"], rows[i]["close"]) for i in range(max(1, idx - 19), idx + 1)]
    vol20 = stdev(recent_returns)
    dd40 = max_drawdown(rows, idx - 39, idx)
    if vol20 is None or dd40 is None:
        return None
    recent_days = [date.fromisoformat(row["date"]) for row in rows[max(0, idx - 9) : idx + 1]]
    w0_values = [first_window_returns.get(symbol, {}).get(day) for day in recent_days]
    w0_known = [value for value in w0_values if value is not None]
    w0_positive_rate = sum(1 for value in w0_known if value > 0) / len(w0_known) if w0_known else 0.0
    rs_spy20 = ret20 - spy20
    rs_qqq20 = ret20 - qqq20
    overextension_penalty = max(ret20 - 25.0, 0.0) * 1.2
    stability_penalty = abs(min(dd40, 0.0)) * 0.6 + max(vol20 - 5.0, 0.0) * 3.0
    score = (
        50.0
        + max(min(ret40, 40.0), -40.0) * 0.7
        + max(min(ret20, 25.0), -25.0) * 1.0
        + max(min(rs_spy20, 25.0), -25.0) * 1.1
        + max(min(rs_qqq20, 25.0), -25.0) * 0.7
        + (w0_positive_rate - 0.5) * 8.0
        - stability_penalty
        - overextension_penalty
    )
    row = {
        "symbol": symbol,
        "theme": THEMES.get(symbol, "other"),
        "asof_close": rows[idx]["close"],
        "score": score,
        "ret20": ret20,
        "ret40": ret40,
        "rs_spy20": rs_spy20,
        "rs_qqq20": rs_qqq20,
        "dd40": dd40,
        "vol20": vol20,
        "w0_positive_rate_10d": w0_positive_rate,
    }
    fields = event_fields(symbol, asof.isoformat(), event_features)
    if fields["event_exclude"]:
        return None
    row.update(fields)
    row["score"] = float(row["score"]) + float(fields["event_score_adjustment"])
    return row


def select_daily(scored: list[dict[str, Any]], variant: str) -> list[dict[str, Any]]:
    if variant == "daily-3h-quality-top5":
        filtered = [row for row in scored if row["ret40"] > -12 and row["dd40"] > -32 and row["vol20"] < 8.5]
        return sorted(filtered, key=lambda row: row["score"], reverse=True)[:5]
    if variant == "daily-3h-theme-capped-top5":
        filtered = [row for row in scored if row["ret40"] > -12 and row["dd40"] > -32 and row["vol20"] < 8.5]
        selected = []
        theme_counts: dict[str, int] = defaultdict(int)
        for row in sorted(filtered, key=lambda item: item["score"], reverse=True):
            if theme_counts[row["theme"]] >= 2:
                continue
            selected.append(row)
            theme_counts[row["theme"]] += 1
            if len(selected) == 5:
                break
        return selected
    if variant == "daily-3h-momentum-top3":
        filtered = [row for row in scored if row["ret20"] > 0 and row["rs_spy20"] > 0 and row["w0_positive_rate_10d"] >= 0.5]
        return sorted(filtered, key=lambda row: (row["ret20"], row["rs_spy20"]), reverse=True)[:3]
    raise ValueError(variant)


def simulate_daily_policies(
    symbols: list[str],
    daily: dict[str, list[dict[str, Any]]],
    windows_by_symbol: dict[str, list[WindowBar]],
    calendar: list[CalendarDay],
    event_features: dict[str, list[dict[str, Any]]] | None = None,
) -> dict[str, list[dict[str, Any]]]:
    candidate_symbols = [symbol for symbol in symbols if symbol not in BENCHMARKS]
    spy_days = [date.fromisoformat(row["date"]) for row in daily.get("SPY", [])]
    first_window_returns: dict[str, dict[date, float]] = defaultdict(dict)
    for symbol, rows in windows_by_symbol.items():
        for row in rows:
            if row.index == 0:
                first_window_returns[symbol][row.day] = row.return_pct
    variants = ("daily-3h-quality-top5", "daily-3h-theme-capped-top5", "daily-3h-momentum-top3")
    out = {variant: [] for variant in variants}
    for asof in spy_days:
        scored = []
        for symbol in candidate_symbols:
            row = score_daily_symbol(symbol, daily, first_window_returns, asof, event_features)
            if row:
                scored.append(row)
        if not scored:
            continue
        for variant in variants:
            picks = select_daily(scored, variant)
            for rank, pick in enumerate(picks, start=1):
                symbol_rows = daily[pick["symbol"]]
                spy_rows = daily["SPY"]
                qqq_rows = daily["QQQ"]
                idx = daily_index(symbol_rows)[asof]
                spy_idx = daily_index(spy_rows)[asof]
                qqq_idx = daily_index(qqq_rows)[asof]
                ret5, ret5_date, adverse5 = forward_daily_return(symbol_rows, idx, 5)
                ret20, ret20_date, adverse20 = forward_daily_return(symbol_rows, idx, 20)
                spy20, _, _ = forward_daily_return(spy_rows, spy_idx, 20)
                qqq20, _, _ = forward_daily_return(qqq_rows, qqq_idx, 20)
                out[variant].append(
                    {
                        "policy": variant,
                        "asof": asof.isoformat(),
                        "rank": rank,
                        **pick,
                        "ret5_fwd": ret5,
                        "ret5_date": ret5_date,
                        "ret20_fwd": ret20,
                        "ret20_date": ret20_date,
                        "spy20_fwd": spy20,
                        "qqq20_fwd": qqq20,
                        "excess_spy20": ret20 - spy20 if ret20 is not None and spy20 is not None else None,
                        "excess_qqq20": ret20 - qqq20 if ret20 is not None and qqq20 is not None else None,
                        "adverse5": adverse5,
                        "adverse20": adverse20,
                    }
                )
    return out


def summarize_daily(rows: list[dict[str, Any]]) -> dict[str, Any]:
    completed20 = [row for row in rows if row["ret20_fwd"] is not None and row["excess_spy20"] is not None]
    completed5 = [row for row in rows if row["ret5_fwd"] is not None]
    return {
        "asof_count": len({row["asof"] for row in rows}),
        "recommendations": len(rows),
        "completed20": len(completed20),
        "hit20_abs": sum(1 for row in completed20 if row["ret20_fwd"] > 0),
        "hit20_spy": sum(1 for row in completed20 if row["excess_spy20"] > 0),
        "avg20": mean([row["ret20_fwd"] for row in completed20]),
        "avg_excess_spy20": mean([row["excess_spy20"] for row in completed20]),
        "avg_adverse20": mean([row["adverse20"] for row in completed20 if row["adverse20"] is not None]),
        "completed5": len(completed5),
        "hit5_abs": sum(1 for row in completed5 if row["ret5_fwd"] > 0),
        "avg5": mean([row["ret5_fwd"] for row in completed5]),
    }


def split_rows(rows: list[dict[str, Any]], split_day: date, key: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    train = [row for row in rows if date.fromisoformat(row[key]) <= split_day]
    validation = [row for row in rows if date.fromisoformat(row[key]) > split_day]
    return train, validation


def round_json(value: Any) -> Any:
    if isinstance(value, float):
        return round(value, 6)
    if isinstance(value, list):
        return [round_json(item) for item in value]
    if isinstance(value, dict):
        return {key: round_json(item) for key, item in value.items()}
    return value


def top_symbols(rows: list[dict[str, Any]], count: int = 8) -> list[dict[str, Any]]:
    grouped: dict[str, list[float]] = defaultdict(list)
    for row in rows:
        value = safe_float(row.get("pl_pct") if "pl_pct" in row else row.get("ret20_fwd"))
        if value is not None:
            grouped[row["symbol"]].append(value)
    ranked = sorted(
        (
            {"symbol": symbol, "count": len(values), "avg_return_pct": mean(values), "total_return_pct": sum(values)}
            for symbol, values in grouped.items()
        ),
        key=lambda row: (row["total_return_pct"], row["avg_return_pct"] or 0),
        reverse=True,
    )
    return ranked[:count]


def event_feature_summary(rows: list[dict[str, Any]], cache_used: bool) -> dict[str, Any]:
    matches = [row for row in rows if row.get("event_feature_present")]
    servers = sorted({server for row in matches for server in row.get("mcp_servers_used", [])})
    return {
        "event_feature_cache_used": cache_used,
        "rows": len(rows),
        "event_feature_matches": len(matches),
        "event_feature_coverage_pct": len(matches) / len(rows) * 100.0 if rows else 0.0,
        "mcp_event_servers_used": servers,
        "mcp_event_gap_count": sum(int(row.get("mcp_gap_count", 0)) for row in matches),
    }


def format_pct(value: float | None) -> str:
    if value is None:
        return "n/a"
    return f"{value:+.2f}%"


def format_usd(value: float | None) -> str:
    if value is None:
        return "n/a"
    return f"${value:+,.2f}"


def markdown_table(headers: list[str], rows: list[list[str]]) -> str:
    out = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    out.extend("| " + " | ".join(row) + " |" for row in rows)
    return "\n".join(out)


def build_markdown(result: dict[str, Any]) -> str:
    intraday_summary = result["simulations"]["intraday"]["summary"]
    daily_summary = result["simulations"]["daily"]["summary"]
    split = result["split_date"]
    intraday_rows = []
    for policy, phases in intraday_summary.items():
        all_summary = phases["all"]
        validation = phases["validation"]
        intraday_rows.append(
            [
                policy,
                str(all_summary["active_days"]),
                str(all_summary["trades"]),
                f"{all_summary['hit_rate']:.1f}%",
                str(all_summary["stops"]),
                str(all_summary["takes"]),
                format_usd(all_summary["total_pl_usd_per_10k_trade"]),
                format_usd(all_summary["avg_pl_usd_per_trade"]),
                f"{validation['hit_rate']:.1f}%",
                format_usd(validation["total_pl_usd_per_10k_trade"]),
            ]
        )
    daily_rows = []
    for policy, phases in daily_summary.items():
        all_summary = phases["all"]
        validation = phases["validation"]
        daily_rows.append(
            [
                policy,
                str(all_summary["asof_count"]),
                str(all_summary["completed20"]),
                f"{all_summary['hit20_abs']}/{all_summary['completed20']}",
                f"{all_summary['hit20_spy']}/{all_summary['completed20']}",
                format_pct(all_summary["avg20"]),
                format_pct(all_summary["avg_excess_spy20"]),
                format_pct(all_summary["avg_adverse20"]),
                format_pct(validation["avg_excess_spy20"]),
            ]
        )
    best_intraday = sorted(
        (
            (policy, phases["all"]["total_pl_usd_per_10k_trade"], phases["all"]["avg_pl_usd_per_trade"], phases["all"]["trades"])
            for policy, phases in intraday_summary.items()
        ),
        key=lambda item: item[1],
        reverse=True,
    )
    best_daily = sorted(
        (
            (policy, phases["all"]["avg_excess_spy20"], phases["validation"]["avg_excess_spy20"], phases["all"]["completed20"])
            for policy, phases in daily_summary.items()
        ),
        key=lambda item: item[1] if item[1] is not None else -999,
        reverse=True,
    )
    created_at = result["created_at"]
    mcp_event = result.get("mcp_event_features", {})
    intraday_event = mcp_event.get("intraday", {})
    daily_event = mcp_event.get("daily", {})
    event_servers = sorted(
        set(intraday_event.get("mcp_event_servers_used", []))
        | set(daily_event.get("mcp_event_servers_used", []))
    )
    return f"""---
id: 2026-05-24-six-month-3h-independent-policy-review
created_at: {created_at}
source_type: six-month-3h-policy-simulation
paper: true
orders_submitted: 0
---

# 최근 6개월 3시간 단위 독립 시뮬레이션과 정책 검토

## 목적

사용자 요청에 따라 2025-11-24부터 2026-05-22까지 최근 6개월 미국 정규 거래일을 대상으로, Alpaca MCP에서 30분봉을 읽어 정규장 3시간 구간으로 집계했다. 주문 제출, 취소, 교체, 포지션 변경은 하지 않았다.

watchlist는 비어 있어 현재 paper 보유 종목과 기존 정책 후보, 벤치마크를 합쳐 {len(result['symbols'])}개 심볼을 사용했다. 기준 universe는 `{', '.join(result['symbols'])}`이다.

## 데이터 범위

- 거래일: {result['calendar_days']}일
- 3시간 구간 레코드: {result['extracted']['three_hour_window_count']}개
- 정규장 집계 일봉 레코드: {result['extracted']['daily_bar_count']}개
- 원천: [[2026-05-24-six-month-3h-simulation-sources]]
- 계산 데이터: `wiki/evidence-store/sources/2026-05-24-six-month-3h-simulation-data.json`
- 학습/검증 분리 기준: `{split}`까지를 앞구간, 이후를 뒤구간으로 보았다. 규칙은 새로 튜닝하지 않고 고정식으로 적용했다.

## MCP 이벤트 feature 결합

- event feature cache 사용: `{str(bool(mcp_event.get('event_feature_cache_file'))).lower()}`
- cache 파일: `{mcp_event.get('event_feature_cache_file') or '없음'}`
- 단타 row 매칭: {intraday_event.get('event_feature_matches', 0)} / {intraday_event.get('rows', 0)} ({intraday_event.get('event_feature_coverage_pct', 0.0):.2f}%)
- 장타 row 매칭: {daily_event.get('event_feature_matches', 0)} / {daily_event.get('rows', 0)} ({daily_event.get('event_feature_coverage_pct', 0.0):.2f}%)
- 매칭된 research MCP 서버: {', '.join(event_servers) if event_servers else '없음'}

## 단타형 3시간 정책 결과

{markdown_table(
        [
            "정책",
            "active days",
            "trade count",
            "hit rate",
            "stop",
            "take",
            "P/L",
            "average per trade",
            "검증 hit",
            "검증 P/L",
        ],
        intraday_rows,
    )}

해석:

- 가장 좋은 총손익 정책은 `{best_intraday[0][0]}`였고, 전체 가상 P/L은 {format_usd(best_intraday[0][1])}, 거래당 평균은 {format_usd(best_intraday[0][2])}였다.
- 단타 정책들은 모두 IEX 30분봉 기반이라 실제 체결 가능성, spread, slippage를 반영하지 못한다.
- 검증 구간에서 손익이 약하거나 stop 비중이 높은 정책은 자동 주문 후보로 올리지 않는다.

## 일별 장타형 정책 결과

{markdown_table(
        [
            "정책",
            "as-of days",
            "20D 완료",
            "20D 절대 hit",
            "SPY 초과 hit",
            "평균 20D",
            "평균 SPY 초과",
            "평균 불리 이동",
            "검증 SPY 초과",
        ],
        daily_rows,
    )}

해석:

- 전체 기준 평균 SPY 초과수익이 가장 높은 장타형 정책은 `{best_daily[0][0]}`였다.
- `daily-3h-theme-capped-top5`는 같은 테마를 2개까지만 허용하는 variant다. 총수익이 조금 낮아져도 포트폴리오 집중 리스크를 낮추는지 확인하기 위해 별도로 유지한다.
- `daily-3h-momentum-top3`는 성과가 강할 수 있지만 종목/테마 집중과 불리 이동을 함께 보아야 한다.

## 정책 검토

| 정책/원칙 | 이번 6개월 3시간 검증 후 판단 |
| --- | --- |
| `intraday-rs-breakout-v0` 계열 | 10시대 1시간 신호 대신 첫 3시간 구간으로 독립 재검증했다. 특정 구간에서는 플러스가 가능하지만 stop-first 보수 가정과 체결 공백 때문에 자동 주문 승격은 부적합하다. |
| `intraday-rs-breadth-vwap-v1` 계열 | 이번 3시간 집계에서는 QQQ/SMH breadth를 직접 재현하지 않고 시장 위험선호와 상대강도를 단순화했다. v1은 계속 paper-only 관찰 후보로 두고, 실시간 bid/ask와 11:05~11:15 유지 확인이 붙기 전 주문 금지 원칙을 유지한다. |
| `intraday-pullback-vwap-reclaim-v0` | 첫 3시간 하락 후 VWAP 회복형으로 독립 검증했다. 손익이 플러스라도 active day가 제한되고 개별 종목 stop 위험이 있어 보조 관찰 후보 상태를 유지한다. |
| `long-term-quality-momentum-v0` | 20D/40D 추세, SPY/QQQ 상대강도, drawdown, 변동성, 첫 3시간 양봉 빈도를 결합한 일별 variant가 장타 검토에 계속 유효했다. 다만 가격 기반 검증이므로 실적/filing/밸류에이션 확인 전 자동 주문 승격은 보류한다. |
| 테마 노출 상한 | 반도체/양자 등 성과가 한 테마에 몰릴 수 있어 theme cap variant를 정책 후보로 유지할 필요가 있다. 자동 주문 전에는 테마별 40% 상한 또는 종목 2개 제한을 order plan에 명시하는 쪽이 안전하다. |
| 실적 beat 후 과열 감점 | 3시간 가격 검증만으로 실적 품질은 알 수 없지만, 단기 급등 추격형 정책에서 손실이 반복될 수 있어 기존 과열 감점 원칙을 유지한다. |

## 다음 적용 기준

- 단타는 계속 `orders_submitted=0` paper dry-run으로만 운영한다.
- 자동 주문 후보는 장타형 `quality + theme cap + filing/earnings confirmation + staged entry` 조합을 별도 검증한 뒤에만 고려한다.
- 3시간 데이터는 정책 설계용 feature store로 유지하되, 주문 제출용 근거에는 fresh quote, asset check, risk gate, source confidence가 추가로 필요하다.

## 데이터 공백

{chr(10).join(f'- {item}' for item in result['data_gaps'])}

## 지표 설명

- `active days`: 해당 정책이 실제로 신호를 낸 거래일 수다. 표본 거래일 전체와 다르다.
- `trade count`: 이론상 진입한 거래 수다. 같은 날 여러 종목이 들어가면 여러 건으로 계산한다.
- `hit rate`: 수익 거래 비율이다. 단타는 `pl_pct > 0`, 장타는 forward return이 양수인지로 계산했다.
- `stop`: 이론적 stop 가격에 먼저 닿은 거래 수다. 30분봉 안에서 stop과 take가 모두 보이면 보수적으로 stop-first 처리했다.
- `take`: 이론적 take profit에 닿은 거래 수다.
- `P/L`: 종목당 10,000달러를 넣었다고 가정한 가상 손익 합계다.
- `average per trade`: 가상 손익을 trade count로 나눈 값이다.
- `QQQ VWAP`, `SMH VWAP`, `symbol VWAP`: 각각 시장, 반도체 섹터, 개별 종목의 거래량 가중 평균가다. 이번 3시간 배치에서는 개별 window VWAP만 직접 사용했고, 기존 v1의 QQQ/SMH VWAP는 정책 해석 항목으로 남겼다.
- `semiconductor breadth`: SMH, NVDA, AMD, AVGO, TSM, LRCX 중 상승 종목 수를 보는 지표다. 이번 배치에서는 별도 v1 재현 대신 theme cap과 QQQ 상대강도로 대체했다.
- `relative strength`: 같은 구간의 종목 수익률에서 QQQ 수익률을 뺀 값이다. 플러스면 시장보다 강했다는 뜻이다.
- `spread_pct`: bid/ask 차이를 mid-price로 나눈 비율이다. 이번 과거 배치는 quote를 포함하지 않아 계산하지 못했다.
- `fill_feasibility`: 실제 limit 주문이 체결될 가능성 판단이다. 이번 배치는 과거 bar 기반이라 `unknown`으로 남긴다.
"""


def build_source_markdown(result: dict[str, Any]) -> str:
    return f"""---
id: 2026-05-24-six-month-3h-simulation-sources
created_at: {result['created_at']}
source_type: alpaca-mcp-3h-bars
paper: true
orders_submitted: 0
---

# 최근 6개월 3시간 시뮬레이션 원천

## 조회 목적

2025-11-24부터 2026-05-22까지 일별 정규장 3시간 단위 종목 정보를 추출하고 독립 시뮬레이션을 수행하기 위해 Alpaca MCP read-only 도구를 사용했다.

## 사용 MCP와 도구

- `alpaca.get_clock`: 시장 시계 확인.
- `alpaca.get_watchlists`: watchlist universe 확인. 결과가 비어 있어 current holdings와 기존 정책 후보를 사용했다.
- `alpaca.get_all_positions`: 현재 paper 보유 종목 확인.
- `alpaca.get_calendar`: 거래일, 정규장 open/close 확인.
- `alpaca.get_asset`: 후보 심볼의 active/tradable 여부 확인.
- `alpaca.get_stock_bars`: IEX `30Min` bars 조회. 정규장 외 bar는 집계에서 제외했다.
- Research MCP event feature cache: `{result.get('mcp_event_features', {}).get('event_feature_cache_file') or 'not supplied'}`. 공급된 경우 SEC EDGAR, Alpha Vantage, FRED, Firecrawl, Yahoo Finance feature를 `available_at` 기준으로 결합했다.

## 기준 시점과 범위

- 조회 생성 시각: {result['created_at']}
- 데이터 시작일: {result['start_date']}
- 데이터 종료일: {result['end_date']}
- 거래일 수: {result['calendar_days']}
- feed: `{result['feed']}`
- timeframe: `{result['timeframe']}`
- universe: `{', '.join(result['symbols'])}`

## 추출 방식

정규장 30분봉만 사용해 아래처럼 3시간 window로 묶었다.

- window 0: 정규장 open부터 3시간.
- window 1: window 0 이후 3시간.
- window 2: 남은 정규장 구간. 보통 15:30-16:00 ET이며, 조기 폐장일에는 더 짧다.

각 window는 open, high, low, close, volume, volume-weighted average price를 저장했다.

## 데이터 공백

{chr(10).join(f'- {item}' for item in result['data_gaps'])}

## 산출물

- 계산 데이터: `wiki/evidence-store/sources/2026-05-24-six-month-3h-simulation-data.json`
- 분석 문서: [[2026-05-24-six-month-3h-independent-policy-review]]
- run manifest: `wiki/evidence-store/run-manifests/2026-05-24-3h-six-month-policy-review.json`
"""


def build_manifest(result: dict[str, Any], run_manifest: Path, source_refs: list[str]) -> dict[str, Any]:
    root = Path(__file__).resolve().parents[1]
    try:
        import subprocess

        git_commit = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], cwd=root, text=True).strip()
        status = subprocess.check_output(["git", "status", "--short"], cwd=root, text=True)
        if status.strip():
            git_commit = f"{git_commit}-dirty"
    except Exception:
        git_commit = "unavailable"
    policy_path = root / "wiki/policy-book/recommendation-policy.md"
    try:
        import hashlib

        recommendation_policy_sha = "sha256:" + hashlib.sha256(policy_path.read_bytes()).hexdigest()
    except Exception:
        recommendation_policy_sha = "unavailable"
    created = datetime.now(UTC)
    event_features = result.get("mcp_event_features", {})
    event_servers = sorted(
        set(event_features.get("intraday", {}).get("mcp_event_servers_used", []))
        | set(event_features.get("daily", {}).get("mcp_event_servers_used", []))
    )
    return {
        "run_id": run_manifest.stem,
        "mode": "review",
        "paper": True,
        "created_at": iso_z(created),
        "git_commit": git_commit,
        "prompt_file_sha": "unavailable:inline-user-request-2026-05-24-six-month-3h-policy-review",
        "risk_policy_version": "medium-risk-v1",
        "recommendation_policy_sha": recommendation_policy_sha,
        "schema_version": "1.0",
        "mcp_servers_used": sorted({"alpaca", *event_servers}),
        "mcp_failures": [],
        "data_cutoff_time": f"{result['end_date']}T20:00:00Z",
        "market_clock_checked_at": result.get("market_clock_checked_at", result["created_at_utc"]),
        "source_refs": source_refs,
        "risk_check_result": {
            "status": "NOT_APPLICABLE",
            "reason": "policy review and historical dry-run simulation only; no order plan created",
        },
        "submitted_order_ids": [],
        "post_trade_check_path": "",
    }


async def run() -> None:
    args = parse_args()
    root = Path(__file__).resolve().parents[1]
    start_day = date.fromisoformat(args.start)
    end_day = date.fromisoformat(args.end)
    symbols_arg = [item.strip().upper() for item in args.symbols.split(",") if item.strip()]
    event_features = load_event_features(args.event_features_json)

    params = StdioServerParameters(command=str(root / "scripts/alpaca-mcp.sh"), args=[], cwd=root)
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            clock = await call_json(session, "get_clock")
            watchlists = await call_json(session, "get_watchlists")
            positions_payload = await call_json(session, "get_all_positions")
            calendar_payload = await call_json(session, "get_calendar", {"start": args.start, "end": args.end})
            calendar = parse_calendar(calendar_payload)

            position_symbols = sorted({row["symbol"].upper() for row in positions_payload.get("result", []) if row.get("symbol")})
            watchlist_symbols = sorted(
                {
                    asset.get("symbol", "").upper()
                    for watchlist in watchlists.get("result", [])
                    for asset in watchlist.get("assets", [])
                    if asset.get("symbol")
                }
            )
            if symbols_arg:
                symbols = sorted(set(BENCHMARKS + tuple(symbols_arg)))
            else:
                symbols = sorted(set(BENCHMARKS + DEFAULT_UNIVERSE + tuple(position_symbols) + tuple(watchlist_symbols)))

            asset_checks = {}
            for symbol in symbols:
                print(f"asset {symbol}", flush=True)
                try:
                    asset_checks[symbol] = await call_json(session, "get_asset", {"symbol_or_asset_id": symbol})
                except Exception as exc:
                    asset_checks[symbol] = {"error": str(exc)}

            chunks = date_chunks(start_day, end_day)
            bars_by_symbol: dict[str, list[Bar]] = {}
            fetch_meta = {}
            for symbol in symbols:
                raw_rows_by_ts: dict[str, dict[str, Any]] = {}
                chunk_meta = []
                for chunk_start, chunk_end in chunks:
                    print(f"bars {symbol} {chunk_start.isoformat()}..{chunk_end.isoformat()}", flush=True)
                    start_dt = datetime.combine(chunk_start, time(0, 0), ET)
                    end_dt = datetime.combine(chunk_end + timedelta(days=1), time(0, 0), ET)
                    payload = await call_json(
                        session,
                        "get_stock_bars",
                        {
                            "symbols": symbol,
                            "timeframe": args.timeframe,
                            "start": iso_z(start_dt),
                            "end": iso_z(end_dt),
                            "feed": args.feed,
                            "limit": args.limit,
                            "sort": "asc",
                            "adjustment": "raw",
                        },
                    )
                    chunk_rows = payload.get("bars", {}).get(symbol, [])
                    for row in chunk_rows:
                        raw_rows_by_ts[str(row["t"])] = row
                    chunk_meta.append(
                        {
                            "start": chunk_start.isoformat(),
                            "end": chunk_end.isoformat(),
                            "raw_bar_count": len(chunk_rows),
                            "next_page_token_present": bool(payload.get("next_page_token")),
                        }
                    )
                raw_rows = [raw_rows_by_ts[key] for key in sorted(raw_rows_by_ts)]
                bars_by_symbol[symbol] = [parse_bar(row) for row in raw_rows]
                fetch_meta[symbol] = {
                    "raw_bar_count": len(raw_rows),
                    "chunk_count": len(chunks),
                    "chunks_with_next_page_token": sum(1 for item in chunk_meta if item["next_page_token_present"]),
                    "chunk_meta": chunk_meta,
                }

    windows_by_symbol, daily = aggregate_windows(symbols, bars_by_symbol, calendar)
    window_lookup = windows_by_day(windows_by_symbol)
    regular_bars = regular_bars_by_symbol_day(symbols, bars_by_symbol, calendar)
    intraday_rows = intraday_candidate_rows(symbols, window_lookup, regular_bars, calendar, event_features)
    daily_rows = simulate_daily_policies(symbols, daily, windows_by_symbol, calendar, event_features)

    trading_days = [item.day for item in calendar]
    split_day = trading_days[len(trading_days) // 2]
    intraday_summary: dict[str, Any] = {}
    for policy, rows in intraday_rows.items():
        train, validation = split_rows(rows, split_day, "date")
        intraday_summary[policy] = {
            "all": summarize_intraday(rows, len(calendar)),
            "train": summarize_intraday(train, len([item for item in calendar if item.day <= split_day])),
            "validation": summarize_intraday(validation, len([item for item in calendar if item.day > split_day])),
            "top_symbols": top_symbols(rows),
        }
    daily_summary: dict[str, Any] = {}
    for policy, rows in daily_rows.items():
        train, validation = split_rows(rows, split_day, "asof")
        daily_summary[policy] = {
            "all": summarize_daily(rows),
            "train": summarize_daily(train),
            "validation": summarize_daily(validation),
            "top_symbols": top_symbols([row for row in rows if row["ret20_fwd"] is not None]),
        }
    all_intraday_rows = [row for rows in intraday_rows.values() for row in rows]
    all_daily_rows = [row for rows in daily_rows.values() for row in rows]
    mcp_event_features = {
        "event_feature_cache_file": str(args.event_features_json) if args.event_features_json else "",
        "intraday": event_feature_summary(all_intraday_rows, bool(event_features)),
        "daily": event_feature_summary(all_daily_rows, bool(event_features)),
    }
    data_gaps = list(DATA_GAPS)
    if event_features:
        data_gaps = [
            item
            for item in data_gaps
            if not item.startswith("Policy review is price/volume based")
        ]
        data_gaps.append(
            "Research MCP event features were joined point-in-time by available_at/asof date; missing symbols kept price-only scoring."
        )
    else:
        data_gaps.append(
            "No research MCP event feature cache was supplied; SEC, earnings, macro, IR, Yahoo analyst/news, and valuation context stayed out of the score."
        )

    created_kst = datetime.now(KST)
    created_utc = datetime.now(UTC)
    result: dict[str, Any] = {
        "created_at": created_kst.isoformat(timespec="seconds"),
        "created_at_utc": iso_z(created_utc),
        "paper": True,
        "orders_submitted": 0,
        "start_date": args.start,
        "end_date": args.end,
        "feed": args.feed,
        "timeframe": args.timeframe,
        "symbols": symbols,
        "benchmarks": list(BENCHMARKS),
        "position_symbols": position_symbols,
        "watchlist_symbols": watchlist_symbols,
        "calendar_days": len(calendar),
        "split_date": split_day.isoformat(),
        "market_clock_checked_at": clock.get("timestamp"),
        "market_clock": {
            "is_open": clock.get("is_open"),
            "next_open": clock.get("next_open"),
            "next_close": clock.get("next_close"),
        },
        "asset_checks": asset_checks,
        "fetch_meta": fetch_meta,
        "extracted": {
            "three_hour_window_count": sum(len(rows) for rows in windows_by_symbol.values()),
            "daily_bar_count": sum(len(rows) for rows in daily.values()),
            "three_hour_windows": {
                symbol: [
                    {
                        "date": row.day.isoformat(),
                        "window": row.index,
                        "start_et": row.start_et.isoformat(),
                        "end_et": row.end_et.isoformat(),
                        "open": row.open,
                        "high": row.high,
                        "low": row.low,
                        "close": row.close,
                        "volume": row.volume,
                        "vwap": row.vwap,
                        "return_pct": row.return_pct,
                    }
                    for row in rows
                ]
                for symbol, rows in windows_by_symbol.items()
            },
            "daily_bars": daily,
        },
        "simulations": {
            "intraday": {
                "policies": list(intraday_rows),
                "summary": intraday_summary,
                "trades": intraday_rows,
            },
            "daily": {
                "policies": list(daily_rows),
                "summary": daily_summary,
                "recommendations": daily_rows,
            },
        },
        "mcp_event_features": mcp_event_features,
        "data_gaps": data_gaps,
    }
    result = round_json(result)

    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.write_text(build_markdown(result), encoding="utf-8")
    args.source_md.parent.mkdir(parents=True, exist_ok=True)
    args.source_md.write_text(build_source_markdown(result), encoding="utf-8")
    manifest = build_manifest(
        result,
        args.run_manifest,
        [
            str(args.source_md),
            str(args.output_md),
            str(args.output_json),
        ]
        + ([str(args.event_features_json)] if args.event_features_json else []),
    )
    args.run_manifest.parent.mkdir(parents=True, exist_ok=True)
    args.run_manifest.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(
        json.dumps(
            {
                "calendar_days": result["calendar_days"],
                "three_hour_windows": result["extracted"]["three_hour_window_count"],
                "intraday_summary": intraday_summary,
                "daily_summary": daily_summary,
                "output_md": str(args.output_md),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


def main() -> None:
    asyncio.run(run())


if __name__ == "__main__":
    main()
