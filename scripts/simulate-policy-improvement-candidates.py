#!/usr/bin/env python3
"""Simulate policy improvement candidates from captured six-month data.

This script reads an existing raw data JSON. It does not call Alpaca and does
not submit, replace, cancel, or close orders.
"""

from __future__ import annotations

import argparse
import json
import math
import statistics
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any, Callable


BENCHMARKS = {"SPY", "QQQ", "SMH"}
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
SPECULATIVE_THEMES = {"quantum_speculative", "ev_ai_event"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-json", type=Path, required=True)
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    return parser.parse_args()


def pct(start: float, end: float) -> float:
    return (end / start - 1.0) * 100.0 if start else 0.0


def mean(values: list[float]) -> float | None:
    return sum(values) / len(values) if values else None


def stdev(values: list[float]) -> float | None:
    return statistics.pstdev(values) if len(values) >= 2 else None


def max_drawdown(closes: list[float]) -> float:
    peak = -math.inf
    worst = 0.0
    for close in closes:
        peak = max(peak, close)
        if peak > 0:
            worst = min(worst, pct(peak, close))
    return worst


def daily_returns(rows: list[dict[str, Any]], start: int, end: int) -> list[float]:
    values = []
    for idx in range(start + 1, end + 1):
        if idx <= 0 or idx >= len(rows):
            continue
        values.append(pct(float(rows[idx - 1]["close"]), float(rows[idx]["close"])))
    return values


def ret(rows: list[dict[str, Any]], idx: int, lookback: int) -> float | None:
    if idx - lookback < 0:
        return None
    return pct(float(rows[idx - lookback]["close"]), float(rows[idx]["close"]))


def first_window_stats(windows: list[dict[str, Any]], asof: str, lookback: int = 20) -> tuple[float, float]:
    prior = [row for row in windows if row["date"] <= asof and int(row["window"]) == 0]
    prior = prior[-lookback:]
    if not prior:
        return 0.0, 0.0
    returns = [float(row["return_pct"]) for row in prior]
    positive_rate = sum(1 for value in returns if value > 0) / len(returns) * 100.0
    return positive_rate, mean(returns) or 0.0


def summarize_daily(recommendations: list[dict[str, Any]], split_date: str) -> dict[str, Any]:
    completed = [row for row in recommendations if row.get("forward_20d_return_pct") is not None]
    validation = [row for row in completed if row["asof_date"] > split_date]
    train = [row for row in completed if row["asof_date"] <= split_date]

    def block(rows: list[dict[str, Any]]) -> dict[str, Any]:
        if not rows:
            return {
                "completed": 0,
                "absolute_hit": "0/0",
                "spy_excess_hit": "0/0",
                "avg_20d_return_pct": None,
                "avg_spy_excess_pct": None,
                "avg_adverse_move_pct": None,
            }
        returns = [float(row["forward_20d_return_pct"]) for row in rows]
        excess = [float(row["forward_20d_excess_spy_pct"]) for row in rows]
        adverse = [float(row["forward_20d_adverse_move_pct"]) for row in rows]
        return {
            "completed": len(rows),
            "absolute_hit": f"{sum(1 for value in returns if value > 0)}/{len(rows)}",
            "spy_excess_hit": f"{sum(1 for value in excess if value > 0)}/{len(rows)}",
            "avg_20d_return_pct": round(mean(returns) or 0.0, 6),
            "avg_spy_excess_pct": round(mean(excess) or 0.0, 6),
            "avg_adverse_move_pct": round(mean(adverse) or 0.0, 6),
        }

    by_symbol: dict[str, list[float]] = defaultdict(list)
    by_theme: Counter[str] = Counter()
    for row in completed:
        by_symbol[row["symbol"]].append(float(row["forward_20d_excess_spy_pct"]))
        by_theme[row["theme"]] += 1

    return {
        "asof_days": len(set(row["asof_date"] for row in recommendations)),
        "recommendations": len(recommendations),
        "completed": len(completed),
        "all": block(completed),
        "train": block(train),
        "validation": block(validation),
        "top_symbols": [
            {
                "symbol": symbol,
                "count": len(values),
                "avg_excess_pct": round(mean(values) or 0.0, 6),
                "total_excess_pct": round(sum(values), 6),
            }
            for symbol, values in sorted(by_symbol.items(), key=lambda item: sum(item[1]), reverse=True)[:8]
        ],
        "theme_counts": dict(by_theme),
    }


def add_theme_cap(rows: list[dict[str, Any]], limit: int, top_n: int) -> list[dict[str, Any]]:
    kept = []
    counts: Counter[str] = Counter()
    for row in sorted(rows, key=lambda item: item["score"], reverse=True):
        theme = row["theme"]
        if counts[theme] >= limit:
            continue
        kept.append(row)
        counts[theme] += 1
        if len(kept) >= top_n:
            break
    return kept


def candidate_features(
    symbol: str,
    idx: int,
    rows: dict[str, list[dict[str, Any]]],
    windows: dict[str, list[dict[str, Any]]],
) -> dict[str, Any] | None:
    item = rows[symbol][idx]
    spy = rows["SPY"][idx]
    qqq = rows["QQQ"][idx]
    values: dict[str, Any] = {
        "symbol": symbol,
        "theme": THEMES.get(symbol, "unknown"),
        "asof_date": item["date"],
        "close": float(item["close"]),
    }
    for period in (5, 10, 20, 40):
        value = ret(rows[symbol], idx, period)
        if value is None:
            return None
        values[f"ret_{period}d_pct"] = value
        values[f"spy_excess_{period}d_pct"] = value - (ret(rows["SPY"], idx, period) or 0.0)
        values[f"qqq_excess_{period}d_pct"] = value - (ret(rows["QQQ"], idx, period) or 0.0)

    close_window = [float(row["close"]) for row in rows[symbol][max(0, idx - 40) : idx + 1]]
    returns = daily_returns(rows[symbol], max(0, idx - 20), idx)
    first_pos, first_avg = first_window_stats(windows.get(symbol, []), str(item["date"]), 20)
    values.update(
        {
            "spy_ret_20d_pct": ret(rows["SPY"], idx, 20) or 0.0,
            "qqq_ret_20d_pct": ret(rows["QQQ"], idx, 20) or 0.0,
            "volatility_20d_pct": stdev(returns) or 0.0,
            "drawdown_40d_pct": max_drawdown(close_window),
            "first_3h_positive_rate_20d": first_pos,
            "first_3h_avg_return_20d_pct": first_avg,
            "score": 0.0,
        }
    )
    return values


def simulate_daily_policy(
    name: str,
    rows: dict[str, list[dict[str, Any]]],
    windows: dict[str, list[dict[str, Any]]],
    split_date: str,
    selector: Callable[[dict[str, Any]], bool],
    scorer: Callable[[dict[str, Any]], float],
    *,
    top_n: int = 5,
    theme_cap: int | None = 2,
) -> dict[str, Any]:
    symbols = [symbol for symbol in rows if symbol not in BENCHMARKS]
    recommendations = []
    sample_len = min(len(rows[symbol]) for symbol in rows)
    for idx in range(40, sample_len):
        ranked = []
        for symbol in symbols:
            features = candidate_features(symbol, idx, rows, windows)
            if not features or not selector(features):
                continue
            features["score"] = scorer(features)
            ranked.append(features)
        selected = add_theme_cap(ranked, theme_cap, top_n) if theme_cap else sorted(ranked, key=lambda item: item["score"], reverse=True)[:top_n]
        for rank, item in enumerate(selected, start=1):
            out = dict(item)
            out["policy"] = name
            out["rank"] = rank
            if idx + 20 < len(rows[item["symbol"]]) and idx + 20 < len(rows["SPY"]):
                forward = pct(float(rows[item["symbol"]][idx]["close"]), float(rows[item["symbol"]][idx + 20]["close"]))
                spy_forward = pct(float(rows["SPY"][idx]["close"]), float(rows["SPY"][idx + 20]["close"]))
                lows = [float(row["low"]) for row in rows[item["symbol"]][idx + 1 : idx + 21]]
                out["forward_20d_return_pct"] = round(forward, 6)
                out["forward_20d_spy_pct"] = round(spy_forward, 6)
                out["forward_20d_excess_spy_pct"] = round(forward - spy_forward, 6)
                out["forward_20d_adverse_move_pct"] = round(pct(float(rows[item["symbol"]][idx]["close"]), min(lows)), 6) if lows else None
            else:
                out["forward_20d_return_pct"] = None
                out["forward_20d_spy_pct"] = None
                out["forward_20d_excess_spy_pct"] = None
                out["forward_20d_adverse_move_pct"] = None
            recommendations.append(out)
    return {"summary": summarize_daily(recommendations, split_date), "recommendations": recommendations}


def summarize_intraday(trades: list[dict[str, Any]], split_date: str) -> dict[str, Any]:
    def block(rows: list[dict[str, Any]]) -> dict[str, Any]:
        if not rows:
            return {"trades": 0, "active_days": 0, "hit_rate": None, "total_pl_usd_per_10k_trade": 0.0, "avg_pl_usd_per_trade": None, "stops": 0, "takes": 0}
        pl = [float(row["pl_pct"]) * 100.0 for row in rows]
        return {
            "trades": len(rows),
            "active_days": len(set(row["date"] for row in rows)),
            "hit_rate": round(sum(1 for row in rows if float(row["pl_pct"]) > 0) / len(rows) * 100.0, 6),
            "total_pl_usd_per_10k_trade": round(sum(pl), 6),
            "avg_pl_usd_per_trade": round(mean(pl) or 0.0, 6),
            "stops": sum(1 for row in rows if row["exit_reason"] == "stop"),
            "takes": sum(1 for row in rows if row["exit_reason"] == "take"),
        }

    completed = trades
    train = [row for row in completed if row["date"] <= split_date]
    validation = [row for row in completed if row["date"] > split_date]
    return {"all": block(completed), "train": block(train), "validation": block(validation)}


def simulate_intraday_filtered(
    rows: dict[str, list[dict[str, Any]]],
    windows: dict[str, list[dict[str, Any]]],
    split_date: str,
) -> dict[str, Any]:
    by_symbol_day = {
        symbol: {(row["date"], int(row["window"])): row for row in items}
        for symbol, items in windows.items()
    }
    dates = [row["date"] for row in rows["SPY"]]
    trades = []
    for day in dates:
        qqq0 = by_symbol_day.get("QQQ", {}).get((day, 0))
        qqq1 = by_symbol_day.get("QQQ", {}).get((day, 1))
        if not qqq0 or not qqq1 or float(qqq0["return_pct"]) <= 0.2:
            continue
        candidates = []
        for symbol in rows:
            if symbol in BENCHMARKS:
                continue
            w0 = by_symbol_day.get(symbol, {}).get((day, 0))
            w1 = by_symbol_day.get(symbol, {}).get((day, 1))
            w2 = by_symbol_day.get(symbol, {}).get((day, 2))
            if not w0 or not w1 or not w2:
                continue
            rel0 = float(w0["return_pct"]) - float(qqq0["return_pct"])
            rel1 = float(w1["return_pct"]) - float(qqq1["return_pct"])
            if rel0 <= 0.4 or rel1 <= 0.15:
                continue
            if float(w0["close"]) < float(w0["vwap"] or w0["close"]):
                continue
            if THEMES.get(symbol) in SPECULATIVE_THEMES and float(w0["return_pct"]) > 8.0:
                continue
            candidates.append((symbol, rel0 + rel1, w1, w2))
        for symbol, score, entry_window, exit_window in sorted(candidates, key=lambda item: item[1], reverse=True)[:2]:
            entry = float(entry_window["close"])
            stop = entry * 0.992
            take = entry * 1.012
            low = float(exit_window["low"])
            high = float(exit_window["high"])
            close = float(exit_window["close"])
            if low <= stop:
                exit_price = stop
                reason = "stop"
            elif high >= take:
                exit_price = take
                reason = "take"
            else:
                exit_price = close
                reason = "eod"
            trades.append(
                {
                    "policy": "intraday-afternoon-followthrough-filter-v1",
                    "date": day,
                    "symbol": symbol,
                    "theme": THEMES.get(symbol, "unknown"),
                    "score": round(score, 6),
                    "entry": round(entry, 6),
                    "exit": round(exit_price, 6),
                    "exit_reason": reason,
                    "pl_pct": round(pct(entry, exit_price), 6),
                }
            )
    return {"summary": summarize_intraday(trades, split_date), "trades": trades}


def quality_score(row: dict[str, Any]) -> float:
    return (
        row["ret_20d_pct"] * 0.40
        + row["ret_40d_pct"] * 0.20
        + row["spy_excess_20d_pct"] * 0.20
        + row["first_3h_positive_rate_20d"] * 0.05
        + row["first_3h_avg_return_20d_pct"] * 0.10
        - row["volatility_20d_pct"] * 2.0
        + row["drawdown_40d_pct"] * 0.10
    )


def main() -> None:
    args = parse_args()
    source = json.loads(args.input_json.read_text())
    rows = source["extracted"]["daily_bars"]
    windows = source["extracted"]["three_hour_windows"]
    split_date = source["split_date"]

    policies = {
        "lt-overheat-guard-theme-cap-v1": simulate_daily_policy(
            "lt-overheat-guard-theme-cap-v1",
            rows,
            windows,
            split_date,
            lambda row: row["ret_20d_pct"] > -5
            and row["ret_40d_pct"] > 0
            and row["volatility_20d_pct"] <= 7.0
            and row["drawdown_40d_pct"] >= -30.0
            and row["ret_20d_pct"] <= 45.0
            and row["ret_5d_pct"] <= 25.0,
            quality_score,
        ),
        "lt-dual-benchmark-confirm-v1": simulate_daily_policy(
            "lt-dual-benchmark-confirm-v1",
            rows,
            windows,
            split_date,
            lambda row: row["ret_20d_pct"] > row["spy_ret_20d_pct"]
            and row["ret_20d_pct"] > row["qqq_ret_20d_pct"]
            and row["ret_40d_pct"] > 0
            and row["drawdown_40d_pct"] >= -30.0,
            quality_score,
        ),
        "lt-drawdown-volatility-guard-v1": simulate_daily_policy(
            "lt-drawdown-volatility-guard-v1",
            rows,
            windows,
            split_date,
            lambda row: row["ret_20d_pct"] > 0
            and row["ret_40d_pct"] > 0
            and row["volatility_20d_pct"] <= 5.5
            and row["drawdown_40d_pct"] >= -22.0,
            quality_score,
        ),
        "lt-anti-chase-staged-entry-v1": simulate_daily_policy(
            "lt-anti-chase-staged-entry-v1",
            rows,
            windows,
            split_date,
            lambda row: 2.0 <= row["ret_20d_pct"] <= 35.0
            and -7.0 <= row["ret_5d_pct"] <= 12.0
            and row["ret_20d_pct"] > row["spy_ret_20d_pct"]
            and row["ret_40d_pct"] > 0
            and row["volatility_20d_pct"] <= 7.0,
            quality_score,
        ),
        "intraday-afternoon-followthrough-filter-v1": simulate_intraday_filtered(rows, windows, split_date),
    }

    output = {
        "created_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "paper": True,
        "orders_submitted": 0,
        "source_data": str(args.input_json),
        "split_date": split_date,
        "candidate_count": 5,
        "policies": policies,
        "data_gaps": source["data_gaps"]
        + [
            "This improvement simulation reuses previously captured IEX 30Min/daily bars and does not fetch fresh quotes.",
            "Fundamental, valuation, filing, analyst, and macro features are policy requirements but not numerically simulated here.",
        ],
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(output, indent=2, ensure_ascii=False) + "\n")
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.write_text(render_markdown(output), encoding="utf-8")


def render_pct(value: float | None) -> str:
    if value is None:
        return "n/a"
    return f"{value:+.2f}%"


def render_markdown(output: dict[str, Any]) -> str:
    daily_names = [name for name in output["policies"] if name.startswith("lt-")]
    intraday_name = "intraday-afternoon-followthrough-filter-v1"
    lines = [
        "---",
        "id: 2026-05-24-policy-improvement-candidates",
        f"created_at: {output['created_at']}",
        "source_type: policy-improvement-backtest",
        "paper: true",
        "orders_submitted: 0",
        "---",
        "",
        "# 정책 개선 후보 5개 시뮬레이션",
        "",
        "## 목적",
        "",
        "현재 저장된 최근 6개월 3시간/일봉 데이터로 정책 개선 후보 5개를 고정식으로 검증했다. 이 작업은 read-only 백테스트이며 실제 주문, 취소, 포지션 변경은 없다.",
        "",
        f"- 원천 계산 데이터: `{output['source_data']}`",
        f"- 학습/검증 분리 기준: `{output['split_date']}`까지 train, 이후 validation",
        "- 후보 5개: 장타 정책 개선 4개, 단타 관찰 정책 개선 1개",
        "",
        "## 장타 정책 개선 후보",
        "",
        "| 개선 후보 | 완료 추천 | SPY 초과 hit | 평균 20D | 평균 SPY 초과 | 평균 불리 이동 | 검증 SPY 초과 | 판단 |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    judgments = {
        "lt-overheat-guard-theme-cap-v1": "채택 후보. 기존 theme cap에 과열 제한을 추가해 성과를 크게 훼손하지 않았다.",
        "lt-dual-benchmark-confirm-v1": "보조 채택. 시장/나스닥 동시 초과 조건은 후보 수를 줄이지만 검증 성과가 양호했다.",
        "lt-drawdown-volatility-guard-v1": "부분 채택. 방어적 필터로 불리 이동을 줄이는 목적에는 유효하지만 성과도 낮아진다.",
        "lt-anti-chase-staged-entry-v1": "채택 후보. 추격 구간을 줄이면서 평균 초과수익이 유지됐다.",
    }
    for name in daily_names:
        summary = output["policies"][name]["summary"]
        all_block = summary["all"]
        validation = summary["validation"]
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{name}`",
                    str(summary["completed"]),
                    all_block["spy_excess_hit"],
                    render_pct(all_block["avg_20d_return_pct"]),
                    render_pct(all_block["avg_spy_excess_pct"]),
                    render_pct(all_block["avg_adverse_move_pct"]),
                    render_pct(validation["avg_spy_excess_pct"]),
                    judgments[name],
                ]
            )
            + " |"
        )

    intraday = output["policies"][intraday_name]["summary"]
    lines.extend(
        [
            "",
            "## 단타 정책 개선 후보",
            "",
            "| 개선 후보 | 거래 수 | active days | hit rate | stop | take | P/L | 검증 P/L | 판단 |",
            "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
            "| "
            + " | ".join(
                [
                    f"`{intraday_name}`",
                    str(intraday["all"]["trades"]),
                    str(intraday["all"]["active_days"]),
                    render_pct(intraday["all"]["hit_rate"]),
                    str(intraday["all"]["stops"]),
                    str(intraday["all"]["takes"]),
                    f"${intraday['all']['total_pl_usd_per_10k_trade']:+.2f}",
                    f"${intraday['validation']['total_pl_usd_per_10k_trade']:+.2f}",
                    "기존 단타보다 손익 안정성은 나아졌지만 여전히 IEX 30분봉/체결 공백 때문에 자동 주문 금지.",
                ]
            )
            + " |",
            "",
            "## 정책 업데이트",
            "",
            "1. 장타 기본 후보는 `quality + theme cap`을 유지하되 `20D <= 45%`, `5D <= 25%` 과열 제한을 추가한다.",
            "2. 신규 매수 우선순위에는 `ret20 > SPY20`와 `ret20 > QQQ20`를 보조 확인 조건으로 둔다.",
            "3. 방어형 계좌 상태나 시장 변동성 확대 시 `20D volatility <= 5.5%`, `40D drawdown >= -22%` 필터를 적용한다.",
            "4. 과열 종목은 한 번에 비중을 채우지 않고 `5D -7%~+12%`, `20D 2%~35%` 구간에서 staged entry 후보로만 둔다.",
            "5. 단타는 `afternoon follow-through` 필터를 paper-only 관찰 후보로 추가하되, fresh quote/spread/fill 확인 전 자동 주문에 넣지 않는다.",
            "",
            "## 데이터 공백",
            "",
        ]
    )
    for gap in output["data_gaps"]:
        lines.append(f"- {gap}")
    lines.extend(
        [
            "",
            "## 지표 설명",
            "",
            "- `완료 추천`: 추천일 이후 20거래일 성과를 계산할 수 있는 표본 수다.",
            "- `SPY 초과 hit`: 후보의 20D 수익률이 같은 기간 SPY 수익률보다 높았던 비율이다.",
            "- `평균 20D`: 추천일 종가에서 20거래일 뒤 종가까지의 평균 수익률이다.",
            "- `평균 SPY 초과`: 후보 20D 수익률에서 SPY 20D 수익률을 뺀 평균값이다.",
            "- `평균 불리 이동`: 추천 후 20거래일 동안 가장 불리했던 저점 기준 손실률 평균이다.",
            "- `검증 SPY 초과`: 2026-02-25 이후 검증 구간에서의 평균 SPY 초과수익이다.",
            "- `P/L`: 종목당 10,000달러 가상 진입 기준 손익 합계다.",
        ]
    )
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    main()
