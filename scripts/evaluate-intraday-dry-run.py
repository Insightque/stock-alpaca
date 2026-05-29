#!/usr/bin/env python3
"""Evaluate intraday paper dry-run signals from captured market data.

This script never calls Alpaca APIs and never submits, replaces, cancels, or
closes orders. It reads a local JSON capture of 1Min bars and optional quotes,
then writes v0/v1 signal records for wiki review.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import date, datetime, time, timedelta
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo


ET = ZoneInfo("America/New_York")
BREADTH_SYMBOLS = ("SMH", "NVDA", "AMD", "AVGO", "TSM", "LRCX")
DEFAULT_CANDIDATES = ("NVDA", "AMD", "AVGO", "TSM", "LRCX", "PLTR", "TSLA", "SMH")


@dataclass(frozen=True)
class Bar:
    ts: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float


def parse_timestamp(value: str) -> datetime:
    ts = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if ts.tzinfo is None:
        ts = ts.replace(tzinfo=ET)
    return ts.astimezone(ET)


def parse_bar(raw: dict[str, Any]) -> Bar:
    return Bar(
        ts=parse_timestamp(str(raw.get("t") or raw.get("timestamp") or raw.get("time"))),
        open=float(raw.get("o", raw.get("open"))),
        high=float(raw.get("h", raw.get("high"))),
        low=float(raw.get("l", raw.get("low"))),
        close=float(raw.get("c", raw.get("close"))),
        volume=float(raw.get("v", raw.get("volume", 0)) or 0),
    )


def load_capture(path: Path) -> tuple[dict[str, list[Bar]], dict[str, dict[str, Any]]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    symbols_raw = payload.get("symbols", payload)
    quotes = payload.get("quotes", {}) if isinstance(payload, dict) else {}
    bars: dict[str, list[Bar]] = {}
    for symbol, rows in symbols_raw.items():
        if symbol == "quotes" or not isinstance(rows, list):
            continue
        parsed = [parse_bar(row) for row in rows]
        bars[symbol.upper()] = sorted(parsed, key=lambda item: item.ts)
    return bars, {str(k).upper(): v for k, v in quotes.items()}


def in_window(bar: Bar, day: date, start: time, end: time) -> bool:
    local = bar.ts.astimezone(ET)
    return local.date() == day and start <= local.time() <= end


def bars_between(bars: list[Bar], day: date, start: time, end: time) -> list[Bar]:
    return [bar for bar in bars if in_window(bar, day, start, end)]


def first_at_or_after(bars: list[Bar], day: date, target: time) -> Bar | None:
    same_day = [bar for bar in bars if bar.ts.date() == day and bar.ts.time() >= target]
    return min(same_day, key=lambda item: item.ts, default=None)


def last_at_or_before(bars: list[Bar], day: date, target: time) -> Bar | None:
    same_day = [bar for bar in bars if bar.ts.date() == day and bar.ts.time() <= target]
    return max(same_day, key=lambda item: item.ts, default=None)


def pct_return(open_price: float, close_price: float) -> float:
    return (close_price / open_price - 1.0) * 100.0


def parse_hhmm(value: str) -> time:
    return datetime.strptime(value, "%H:%M").time()


def apply_strategy_exit_rules(args: argparse.Namespace) -> None:
    if not args.strategy_config:
        return
    try:
        import yaml
    except ImportError as exc:  # pragma: no cover - exercised only in minimal local envs
        raise SystemExit("--strategy-config requires PyYAML") from exc
    config = yaml.safe_load(Path(args.strategy_config).read_text(encoding="utf-8")) or {}
    exit_rules = config.get("exit_rules") or {}
    if "take_profit_pct" in exit_rules:
        args.take_profit_pct = float(exit_rules["take_profit_pct"])
    if "stop_loss_pct" in exit_rules:
        args.stop_loss_pct = float(exit_rules["stop_loss_pct"])
    if "time_stop_minutes" in exit_rules:
        args.time_stop_minutes = int(exit_rules["time_stop_minutes"])
    if "fallback_exit_time_et" in exit_rules:
        args.fallback_exit_time_et = str(exit_rules["fallback_exit_time_et"])


def vwap(bars: list[Bar]) -> float | None:
    total_volume = sum(max(bar.volume, 0.0) for bar in bars)
    if total_volume <= 0:
        return None
    total_value = sum(((bar.high + bar.low + bar.close) / 3.0) * max(bar.volume, 0.0) for bar in bars)
    return total_value / total_volume


def quote_metrics(symbol: str, quotes: dict[str, dict[str, Any]]) -> tuple[Any, Any, Any, str, str]:
    quote = quotes.get(symbol, {})
    bid = quote.get("bid") or quote.get("bp") or quote.get("bid_price")
    ask = quote.get("ask") or quote.get("ap") or quote.get("ask_price")
    if bid is None or ask is None:
        return bid, ask, None, "unknown", "bid/ask 미수집"
    bid_f = float(bid)
    ask_f = float(ask)
    mid = (bid_f + ask_f) / 2.0
    spread_pct = ((ask_f - bid_f) / mid * 100.0) if mid > 0 else None
    if spread_pct is None:
        feasibility = "unknown"
    elif spread_pct <= 0.10:
        feasibility = "likely"
    elif spread_pct <= 0.30:
        feasibility = "uncertain"
    else:
        feasibility = "poor"
    return bid_f, ask_f, spread_pct, feasibility, f"spread_pct={spread_pct:.3f}" if spread_pct is not None else "spread 계산 불가"


def theoretical_outcome(
    day_bars: list[Bar],
    entry: Bar,
    *,
    take_profit_pct: float = 2.0,
    stop_loss_pct: float = 1.0,
    time_stop_minutes: int | None = None,
) -> tuple[str, float | None, float | None]:
    entry_price = entry.open
    take = entry_price * (1.0 + take_profit_pct / 100.0)
    stop = entry_price * (1.0 - stop_loss_pct / 100.0)
    time_stop_at = entry.ts + timedelta(minutes=time_stop_minutes) if time_stop_minutes else None
    later = [bar for bar in day_bars if bar.ts >= entry.ts]
    for bar in later:
        stop_hit = bar.low <= stop
        take_hit = bar.high >= take
        if stop_hit and take_hit:
            return "ambiguous_stop_first", -stop_loss_pct, stop
        if stop_hit:
            return "stop", -stop_loss_pct, stop
        if take_hit:
            return "take", take_profit_pct, take
        if time_stop_at and bar.ts >= time_stop_at:
            pl_pct = pct_return(entry_price, bar.close)
            return ("time_stop_gain" if pl_pct >= 0 else "time_stop_loss"), pl_pct, bar.close
    eod = max(later, key=lambda item: item.ts, default=None)
    if eod is None:
        return "unknown", None, None
    pl_pct = pct_return(entry_price, eod.close)
    return ("eod_gain" if pl_pct >= 0 else "eod_loss"), pl_pct, eod.close


def evaluate(args: argparse.Namespace) -> dict[str, Any]:
    bars_by_symbol, quotes = load_capture(Path(args.bars_json))
    market_day = date.fromisoformat(args.date)
    fallback_exit_time = parse_hhmm(args.fallback_exit_time_et)
    candidates = [item.strip().upper() for item in args.candidates.split(",") if item.strip()]
    qqq = bars_by_symbol.get("QQQ", [])
    smh = bars_by_symbol.get("SMH", [])
    qqq_signal = bars_between(qqq, market_day, time(10, 0), time(10, 59))
    if not qqq_signal:
        raise SystemExit("QQQ 10:00-10:59 ET bars are required")
    qqq_return = pct_return(qqq_signal[0].open, qqq_signal[-1].close)
    qqq_vwap = vwap(bars_between(qqq, market_day, time(9, 30), time(10, 59)))
    smh_vwap = vwap(bars_between(smh, market_day, time(9, 30), time(10, 59)))
    qqq_entry = first_at_or_after(qqq, market_day, time(11, 0))
    smh_entry = first_at_or_after(smh, market_day, time(11, 0))

    breadth_count = 0
    for symbol in BREADTH_SYMBOLS:
        symbol_bars = bars_by_symbol.get(symbol, [])
        day_open_bar = first_at_or_after(symbol_bars, market_day, time(9, 30))
        entry_bar = first_at_or_after(symbol_bars, market_day, time(11, 0))
        if day_open_bar and entry_bar and entry_bar.open > day_open_bar.open:
            breadth_count += 1

    rows: list[dict[str, Any]] = []
    base_candidates: list[dict[str, Any]] = []
    for symbol in candidates:
        symbol_bars = bars_by_symbol.get(symbol, [])
        signal = bars_between(symbol_bars, market_day, time(10, 0), time(10, 59))
        previous = bars_between(symbol_bars, market_day, time(9, 30), time(9, 59))
        entry = first_at_or_after(symbol_bars, market_day, time(11, 0))
        if not signal or not previous or entry is None:
            continue
        symbol_return = pct_return(signal[0].open, signal[-1].close)
        relative_strength = symbol_return - qqq_return
        previous_high = max(bar.high for bar in previous)
        breakout_pass = signal[-1].close >= previous_high * (1.0 - args.near_high_tolerance_bps / 10000.0)
        v0_pass = (
            qqq_return >= args.qqq_return_threshold
            and symbol_return >= args.symbol_return_threshold
            and relative_strength >= args.relative_strength_threshold
            and breakout_pass
        )
        symbol_vwap = vwap(bars_between(symbol_bars, market_day, time(9, 30), time(10, 59)))
        qqq_vwap_pass = bool(qqq_entry and qqq_vwap and qqq_entry.open > qqq_vwap)
        smh_vwap_pass = bool(smh_entry and smh_vwap and smh_entry.open > smh_vwap)
        symbol_vwap_pass = bool(symbol_vwap and entry.open > symbol_vwap)
        v1_pass = v0_pass and qqq_vwap_pass and smh_vwap_pass and symbol_vwap_pass and breadth_count >= args.breadth_threshold
        bid, ask, spread_pct, fill_feasibility, fill_notes = quote_metrics(symbol, quotes)
        outcome, pl_pct, exit_reference_price = theoretical_outcome(
            bars_between(symbol_bars, market_day, time(9, 30), fallback_exit_time),
            entry,
            take_profit_pct=args.take_profit_pct,
            stop_loss_pct=args.stop_loss_pct,
            time_stop_minutes=args.time_stop_minutes,
        )
        base_candidates.append(
            {
                "symbol": symbol,
                "v0_pass": v0_pass,
                "v1_pass": v1_pass,
                "symbol_10h_return_pct": symbol_return,
                "relative_strength_pctpt": relative_strength,
                "breakout_pass": breakout_pass,
                "qqq_vwap_pass": qqq_vwap_pass,
                "smh_vwap_pass": smh_vwap_pass,
                "symbol_vwap_pass": symbol_vwap_pass,
                "semi_breadth_count": breadth_count,
                "entry_reference_time_et": entry.ts.strftime("%H:%M"),
                "entry_reference_price": entry.open,
                "bid": bid,
                "ask": ask,
                "spread_pct": spread_pct,
                "fill_feasibility": fill_feasibility,
                "fill_notes": fill_notes,
                "take_profit_pct": args.take_profit_pct,
                "stop_loss_pct": args.stop_loss_pct,
                "time_stop_minutes": args.time_stop_minutes,
                "fallback_exit_time_et": args.fallback_exit_time_et,
                "take_price": entry.open * (1.0 + args.take_profit_pct / 100.0),
                "stop_price": entry.open * (1.0 - args.stop_loss_pct / 100.0),
                "exit_reference_price": exit_reference_price,
                "eod_reference_price": exit_reference_price,
                "theoretical_outcome": outcome,
                "theoretical_pl_pct": pl_pct,
            }
        )

    ranked_v0 = sorted(
        [row for row in base_candidates if row["v0_pass"]],
        key=lambda row: (row["relative_strength_pctpt"], row["symbol_10h_return_pct"]),
        reverse=True,
    )
    ranked_v1 = [row for row in ranked_v0 if row["v1_pass"]]
    for policy, ranked, limit in (
        ("v0_top3", ranked_v0, 3),
        ("v0_top2", ranked_v0, 2),
        ("v1_top3", ranked_v1, 3),
        ("v1_top2", ranked_v1, 2),
    ):
        for rank, row in enumerate(ranked[:limit], start=1):
            rows.append({"policy": policy, "rank": rank, "qqq_10h_return_pct": qqq_return, **row})

    return {
        "market_date": args.date,
        "captured_at_et": args.captured_at_et,
        "orders_submitted": 0,
        "qqq_10h_return_pct": qqq_return,
        "semi_breadth_count": breadth_count,
        "exit_rules": {
            "take_profit_pct": args.take_profit_pct,
            "stop_loss_pct": args.stop_loss_pct,
            "time_stop_minutes": args.time_stop_minutes,
            "fallback_exit_time_et": args.fallback_exit_time_et,
        },
        "rows": rows,
    }


def write_json(path: Path, result: dict[str, Any]) -> None:
    path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def fmt(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, float):
        return f"{value:.4f}"
    return str(value)


def write_markdown(path: Path, result: dict[str, Any]) -> None:
    lines = [
        "---",
        f"id: {result['market_date']}-intraday-paper-dry-run",
        f"created_at: {datetime.now().astimezone().isoformat(timespec='seconds')}",
        "source_type: intraday-paper-dry-run",
        "paper: true",
        "orders_submitted: 0",
        "---",
        "",
        f"# {result['market_date']} 단타 paper dry-run",
        "",
        "실제 주문, 취소, 수정, 포지션 변경은 수행하지 않았다.",
        "",
        "## 요약",
        "",
        f"- captured_at_et: `{result['captured_at_et']}`",
        f"- QQQ 10:00-10:59 ET return: `{result['qqq_10h_return_pct']:.4f}%`",
        f"- semi_breadth_count: `{result['semi_breadth_count']}`",
        f"- exit_rules: `{result['exit_rules']}`",
        f"- orders_submitted: `0`",
        "",
        "## 신호 기록",
        "",
        "| policy | rank | symbol | qqq_10h_return_pct | symbol_10h_return_pct | relative_strength_pctpt | breakout_pass | qqq_vwap_pass | smh_vwap_pass | symbol_vwap_pass | semi_breadth_count | entry_reference_time_et | entry_reference_price | bid | ask | spread_pct | fill_feasibility | take_profit_pct | stop_loss_pct | time_stop_minutes | fallback_exit_time_et | take_price | stop_price | theoretical_outcome | theoretical_pl_pct |",
        "| --- | ---: | --- | ---: | ---: | ---: | --- | --- | --- | --- | ---: | --- | ---: | ---: | ---: | ---: | --- | ---: | ---: | ---: | --- | ---: | ---: | --- | ---: |",
    ]
    for row in result["rows"]:
        lines.append(
            "| "
            + " | ".join(
                fmt(row.get(key))
                for key in (
                    "policy",
                    "rank",
                    "symbol",
                    "qqq_10h_return_pct",
                    "symbol_10h_return_pct",
                    "relative_strength_pctpt",
                    "breakout_pass",
                    "qqq_vwap_pass",
                    "smh_vwap_pass",
                    "symbol_vwap_pass",
                    "semi_breadth_count",
                    "entry_reference_time_et",
                    "entry_reference_price",
                    "bid",
                    "ask",
                    "spread_pct",
                    "fill_feasibility",
                    "take_profit_pct",
                    "stop_loss_pct",
                    "time_stop_minutes",
                    "fallback_exit_time_et",
                    "take_price",
                    "stop_price",
                    "theoretical_outcome",
                    "theoretical_pl_pct",
                )
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Fill 관찰 메모",
            "",
            "bid/ask가 비어 있으면 fill 가능성은 `unknown`으로 유지한다. 실제 주문 판단에 사용하지 않는다.",
            "",
            "## 연결",
            "",
            "- [[recommendation-policy]]",
            "- [[2026-05-23-intraday-scalping-feature-filter-simulation]]",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bars-json", required=True, help="Local JSON capture with 1Min bars by symbol")
    parser.add_argument("--date", required=True, help="Market date, YYYY-MM-DD")
    parser.add_argument("--captured-at-et", default="11:00", help="Capture time label in ET")
    parser.add_argument("--candidates", default=",".join(DEFAULT_CANDIDATES), help="Comma-separated candidate symbols")
    parser.add_argument("--output-json", help="Optional JSON output path")
    parser.add_argument("--output-md", help="Optional Markdown output path")
    parser.add_argument("--strategy-config", help="Optional strategy YAML whose exit_rules override CLI defaults")
    parser.add_argument("--qqq-return-threshold", type=float, default=0.20)
    parser.add_argument("--symbol-return-threshold", type=float, default=0.90)
    parser.add_argument("--relative-strength-threshold", type=float, default=0.40)
    parser.add_argument("--near-high-tolerance-bps", type=float, default=50.0)
    parser.add_argument("--breadth-threshold", type=int, default=4)
    parser.add_argument("--take-profit-pct", type=float, default=2.0)
    parser.add_argument("--stop-loss-pct", type=float, default=1.0)
    parser.add_argument("--time-stop-minutes", type=int)
    parser.add_argument("--fallback-exit-time-et", default="15:59")
    args = parser.parse_args()
    apply_strategy_exit_rules(args)

    result = evaluate(args)
    if args.output_json:
        write_json(Path(args.output_json), result)
    if args.output_md:
        write_markdown(Path(args.output_md), result)
    if not args.output_json and not args.output_md:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
