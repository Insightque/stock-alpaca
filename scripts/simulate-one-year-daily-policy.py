#!/usr/bin/env python3
"""Run independent daily long-term policy simulations from captured daily bars."""

from __future__ import annotations

import argparse
import json
import math
import statistics
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml

from policy_simulation_lib import (
    apply_round_trip_cost,
    bootstrap_mean_ci,
    concentration_metrics,
    file_sha256,
    walk_forward_splits,
)


ROOT_DIR = Path(__file__).resolve().parents[1]
BENCHMARKS_DEFAULT = {"SPY", "QQQ", "SMH"}
CONFIDENCE_SCORE_BY_BUCKET = {"high": 0.85, "medium": 0.65, "low": 0.35}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-json", type=Path, required=True)
    parser.add_argument("--strategy-config", type=Path, default=ROOT_DIR / "harness/strategies/long-term-quality-momentum-v1.yaml")
    parser.add_argument("--metadata-yaml", type=Path, default=ROOT_DIR / "harness/symbol-metadata.yaml")
    parser.add_argument(
        "--event-features-json",
        type=Path,
        help="Optional point-in-time research MCP feature cache to join by symbol and as-of date.",
    )
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    parser.add_argument("--scorecard-json", type=Path)
    return parser.parse_args()


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a YAML object")
    return data


def pct(start: float, end: float) -> float:
    return (end / start - 1.0) * 100.0 if start else 0.0


def mean(values: list[float]) -> float | None:
    return sum(values) / len(values) if values else None


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
        if 0 < idx < len(rows):
            values.append(pct(float(rows[idx - 1]["close"]), float(rows[idx]["close"])))
    return values


def ret(rows: list[dict[str, Any]], idx: int, lookback: int) -> float | None:
    if idx - lookback < 0:
        return None
    return pct(float(rows[idx - lookback]["close"]), float(rows[idx]["close"]))


def avg_dollar_volume(rows: list[dict[str, Any]], idx: int, lookback: int = 20) -> float | None:
    if idx - lookback + 1 < 0:
        return None
    sample = rows[idx - lookback + 1 : idx + 1]
    values = [float(row["close"]) * float(row.get("volume", 0.0) or 0.0) for row in sample]
    return sum(values) / len(values) if values else None


def build_indices(rows: dict[str, list[dict[str, Any]]]) -> dict[str, dict[str, int]]:
    return {symbol: {str(row["date"]): idx for idx, row in enumerate(items)} for symbol, items in rows.items()}


def metadata_for(symbol: str, metadata: dict[str, Any]) -> dict[str, Any]:
    defaults = metadata.get("defaults", {})
    symbols = metadata.get("symbols", {})
    value = symbols.get(symbol, {})
    return {**defaults, **value}


def clamp_float(value: float, minimum: float, maximum: float) -> float:
    return max(minimum, min(maximum, value))


def parse_date_key(value: Any) -> str | None:
    if value in (None, ""):
        return None
    text = str(value)
    if len(text) >= 10 and text[4:5] == "-" and text[7:8] == "-":
        return text[:10]
    return None


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


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


def event_source_confidence_score(base_score: float, record: dict[str, Any] | None) -> float:
    if not record:
        return base_score
    if record.get("source_confidence_score") is not None:
        return clamp_float(as_float(record.get("source_confidence_score"), base_score), 0.0, 1.0)
    return clamp_float(base_score + as_float(record.get("source_confidence_delta")), 0.0, 1.0)


def score_candidate(row: dict[str, Any]) -> float:
    return (
        row["ret20"] * 0.34
        + row["ret40"] * 0.18
        + row["spy_excess20"] * 0.20
        + row["qqq_excess20"] * 0.16
        - row["vol20"] * 1.80
        + row["drawdown60"] * 0.10
        - max(row["ret20"] - 35.0, 0.0) * 1.25
        + row["source_confidence_score"] * 4.0
        + row.get("event_score_adjustment", 0.0)
    )


def candidate_features(
    symbol: str,
    asof: str,
    rows: dict[str, list[dict[str, Any]]],
    indices: dict[str, dict[str, int]],
    metadata: dict[str, Any],
    event_features: dict[str, list[dict[str, Any]]] | None = None,
) -> dict[str, Any] | None:
    idx = indices.get(symbol, {}).get(asof)
    spy_idx = indices.get("SPY", {}).get(asof)
    qqq_idx = indices.get("QQQ", {}).get(asof)
    if idx is None or spy_idx is None or qqq_idx is None:
        return None
    symbol_rows = rows[symbol]
    spy_rows = rows["SPY"]
    qqq_rows = rows["QQQ"]
    values: dict[str, Any] = {"symbol": symbol, "asof_date": asof, "close": float(symbol_rows[idx]["close"])}
    for lookback in (5, 20, 40, 60):
        value = ret(symbol_rows, idx, lookback)
        if value is None:
            return None
        values[f"ret{lookback}"] = value
    spy20 = ret(spy_rows, spy_idx, 20)
    qqq20 = ret(qqq_rows, qqq_idx, 20)
    if spy20 is None or qqq20 is None:
        return None
    closes = [float(row["close"]) for row in symbol_rows[idx - 59 : idx + 1]]
    returns = daily_returns(symbol_rows, idx - 20, idx)
    adv = avg_dollar_volume(symbol_rows, idx, 20)
    if not closes or len(returns) < 2 or adv is None:
        return None
    meta = metadata_for(symbol, metadata)
    source_confidence = str(meta.get("source_confidence", "low"))
    base_source_confidence_score = CONFIDENCE_SCORE_BY_BUCKET.get(source_confidence, 0.35)
    event_feature = event_feature_for(symbol, asof, event_features)
    mcp_servers = [str(item) for item in as_list((event_feature or {}).get("mcp_servers_used"))]
    mcp_gaps = [str(item) for item in as_list((event_feature or {}).get("mcp_gaps") or (event_feature or {}).get("gap_flags"))]
    source_refs = [str(item) for item in as_list((event_feature or {}).get("source_refs"))]
    values.update(
        {
            "spy_ret20": spy20,
            "qqq_ret20": qqq20,
            "spy_excess20": values["ret20"] - spy20,
            "qqq_excess20": values["ret20"] - qqq20,
            "drawdown60": max_drawdown(closes),
            "vol20": statistics.pstdev(returns),
            "avg_daily_dollar_volume": adv,
            "theme": meta.get("theme", "unknown"),
            "factor": meta.get("factor", "unknown"),
            "volatility_bucket": meta.get("volatility_bucket", "high"),
            "speculative_flag": bool(meta.get("speculative_flag", True)),
            "source_confidence": source_confidence,
            "source_confidence_score": event_source_confidence_score(base_source_confidence_score, event_feature),
            "liquidity_bucket": meta.get("liquidity_bucket", "unknown"),
            "correlated_cluster": meta.get("correlated_cluster", "unknown"),
            "event_feature_present": event_feature is not None,
            "event_available_date": (event_feature or {}).get("available_date"),
            "event_score_adjustment": event_score_adjustment(event_feature),
            "event_exclude": bool((event_feature or {}).get("exclude", False)),
            "mcp_servers_used": mcp_servers,
            "mcp_gap_count": len(mcp_gaps),
            "mcp_gaps": mcp_gaps,
            "mcp_source_refs": source_refs,
        }
    )
    values["score"] = score_candidate(values)
    return values


def passes_filters(row: dict[str, Any], config: dict[str, Any]) -> bool:
    filters = config["filters"]
    if row.get("event_exclude"):
        return False
    if bool(filters.get("require_event_feature", False)) and not row.get("event_feature_present"):
        return False
    if row.get("mcp_gap_count", 0) > int(filters.get("max_mcp_gap_count", 999)):
        return False
    if row["spy_excess20"] < float(filters.get("min_ret20_vs_spy", 0.0)):
        return False
    if row["qqq_excess20"] < float(filters.get("min_ret20_vs_qqq", 0.0)):
        return False
    if row["ret40"] < float(filters.get("min_ret40", -999.0)):
        return False
    if row["vol20"] > float(filters.get("max_vol20", 999.0)):
        return False
    if row["drawdown60"] < float(filters.get("min_drawdown60", -999.0)):
        return False
    if row["ret20"] > float(filters.get("max_ret20_overheat", 999.0)):
        return False
    if row["ret5"] > float(filters.get("max_ret5_overheat", 999.0)):
        return False
    if row["source_confidence_score"] < float(filters.get("min_source_confidence_score", 0.0)):
        return False
    if row["avg_daily_dollar_volume"] < float(filters.get("min_avg_daily_dollar_volume", 0.0)):
        return False
    return True


def select_with_theme_cap(candidates: list[dict[str, Any]], top_n: int, theme_cap: int) -> list[dict[str, Any]]:
    selected = []
    theme_counts: Counter[str] = Counter()
    for row in sorted(candidates, key=lambda item: item["score"], reverse=True):
        theme = str(row["theme"])
        if theme_counts[theme] >= theme_cap:
            continue
        selected.append(row)
        theme_counts[theme] += 1
        if len(selected) >= top_n:
            break
    return selected


def simulate(
    rows: dict[str, list[dict[str, Any]]],
    config: dict[str, Any],
    metadata: dict[str, Any],
    event_features: dict[str, list[dict[str, Any]]] | None = None,
) -> dict[str, Any]:
    indices = build_indices(rows)
    benchmarks = set(config.get("benchmarks", [])) | BENCHMARKS_DEFAULT
    symbols = [symbol for symbol in rows if symbol not in benchmarks]
    asof_dates = [str(row["date"]) for row in rows["SPY"]]
    recommendations = []
    skipped_missing_dates = 0
    for asof in asof_dates:
        candidates = []
        for symbol in symbols:
            features = candidate_features(symbol, asof, rows, indices, metadata, event_features)
            if not features:
                if indices.get(symbol, {}).get(asof) is None:
                    skipped_missing_dates += 1
                continue
            if passes_filters(features, config):
                candidates.append(features)
        selected = select_with_theme_cap(
            candidates,
            int(config["selection"]["top_n"]),
            int(config["selection"]["theme_cap"]),
        )
        for rank, item in enumerate(selected, start=1):
            out = dict(item)
            out["rank"] = rank
            out["strategy_id"] = config["strategy_id"]
            out["policy_status"] = config["policy_status"]
            out["independent_run_id"] = f"{config['strategy_id']}:{asof}"
            symbol_idx = indices[item["symbol"]][asof]
            spy_idx = indices["SPY"][asof]
            if symbol_idx + 20 < len(rows[item["symbol"]]) and spy_idx + 20 < len(rows["SPY"]):
                forward = pct(float(rows[item["symbol"]][symbol_idx]["close"]), float(rows[item["symbol"]][symbol_idx + 20]["close"]))
                spy_forward = pct(float(rows["SPY"][spy_idx]["close"]), float(rows["SPY"][spy_idx + 20]["close"]))
                lows = [float(row["low"]) for row in rows[item["symbol"]][symbol_idx + 1 : symbol_idx + 21]]
                out["forward_20d_return_pct"] = round(forward, 6)
                out["forward_20d_return_after_cost_pct"] = round(apply_round_trip_cost(forward, config["cost_model"]), 6)
                out["forward_20d_spy_pct"] = round(spy_forward, 6)
                out["forward_20d_excess_spy_pct"] = round(forward - spy_forward, 6)
                out["forward_20d_excess_spy_after_cost_pct"] = round(
                    apply_round_trip_cost(forward - spy_forward, config["cost_model"]), 6
                )
                out["forward_20d_adverse_move_pct"] = round(pct(float(rows[item["symbol"]][symbol_idx]["close"]), min(lows)), 6)
            else:
                out["forward_20d_return_pct"] = None
                out["forward_20d_return_after_cost_pct"] = None
                out["forward_20d_spy_pct"] = None
                out["forward_20d_excess_spy_pct"] = None
                out["forward_20d_excess_spy_after_cost_pct"] = None
                out["forward_20d_adverse_move_pct"] = None
            recommendations.append(out)
    completed = [row for row in recommendations if row.get("forward_20d_excess_spy_after_cost_pct") is not None]
    excess_after_cost = [float(row["forward_20d_excess_spy_after_cost_pct"]) for row in completed]
    adverse = [float(row["forward_20d_adverse_move_pct"]) for row in completed]
    event_feature_matches = sum(1 for row in recommendations if row.get("event_feature_present"))
    mcp_event_servers = sorted(
        {
            server
            for row in recommendations
            for server in row.get("mcp_servers_used", [])
        }
    )
    ci_low, ci_high = bootstrap_mean_ci(excess_after_cost)
    windows = walk_forward_splits(
        asof_dates,
        train_months=int(config["train_validation"]["train_months"]),
        validation_months=int(config["train_validation"]["validation_months"]),
        step_months=int(config["train_validation"].get("rolling_step_months", 1)),
    )
    window_summaries = []
    for window in windows:
        subset = [
            row
            for row in completed
            if window["validation_start"] <= str(row["asof_date"]) <= window["validation_end"]
        ]
        vals = [float(row["forward_20d_excess_spy_after_cost_pct"]) for row in subset]
        window_summaries.append(
            {
                **window,
                "completed": len(subset),
                "avg_excess_after_cost_pct": round(mean(vals) or 0.0, 6) if vals else None,
                "hit_rate_after_cost_pct": round(sum(1 for value in vals if value > 0) / len(vals) * 100.0, 6)
                if vals
                else None,
            }
        )
    return {
        "summary": {
            "strategy_id": config["strategy_id"],
            "policy_status": config["policy_status"],
            "auto_orders_allowed": bool(config.get("auto_orders_allowed", False)),
            "daily_independent_runs": len(set(row["asof_date"] for row in recommendations)),
            "recommendations": len(recommendations),
            "completed": len(completed),
            "hit_rate_after_cost_pct": round(sum(1 for value in excess_after_cost if value > 0) / len(excess_after_cost) * 100.0, 6)
            if excess_after_cost
            else None,
            "avg_excess_after_cost_pct": round(mean(excess_after_cost) or 0.0, 6) if excess_after_cost else None,
            "median_excess_after_cost_pct": round(statistics.median(excess_after_cost), 6) if excess_after_cost else None,
            "bootstrap_95_ci_excess_after_cost_pct": [
                round(ci_low, 6) if ci_low is not None else None,
                round(ci_high, 6) if ci_high is not None else None,
            ],
            "avg_adverse_move_20d_pct": round(mean(adverse) or 0.0, 6) if adverse else None,
            "skipped_missing_symbol_dates": skipped_missing_dates,
            "event_feature_cache_used": bool(event_features),
            "event_feature_matches": event_feature_matches,
            "event_feature_coverage_pct": round(event_feature_matches / len(recommendations) * 100.0, 6)
            if recommendations
            else 0.0,
            "mcp_event_servers_used": mcp_event_servers,
            "mcp_event_gap_count": sum(int(row.get("mcp_gap_count", 0)) for row in recommendations),
            "concentration": concentration_metrics(completed, "forward_20d_excess_spy_after_cost_pct"),
            "walk_forward": window_summaries,
        },
        "recommendations": recommendations,
    }


def render_markdown(output: dict[str, Any]) -> str:
    summary = output["simulation"]["summary"]
    ci = summary["bootstrap_95_ci_excess_after_cost_pct"]
    lines = [
        "---",
        f"id: {output['run_id']}",
        f"created_at: {output['created_at']}",
        "source_type: one-year-daily-independent-policy-simulation",
        "paper: true",
        "orders_submitted: 0",
        "---",
        "",
        "# 과거 1년 일별 독립 정책 시뮬레이션",
        "",
        "## 결론",
        "",
        f"- 전략: `{summary['strategy_id']}`",
        f"- 정책 상태: `{summary['policy_status']}`",
        f"- 일별 독립 run 수: {summary['daily_independent_runs']}",
        f"- 완료 추천: {summary['completed']} / 전체 추천 {summary['recommendations']}",
        f"- 비용 차감 후 SPY 초과 hit rate: {summary['hit_rate_after_cost_pct']:.2f}%" if summary["hit_rate_after_cost_pct"] is not None else "- 비용 차감 후 SPY 초과 hit rate: n/a",
        f"- 비용 차감 후 평균 SPY 초과수익: {summary['avg_excess_after_cost_pct']:+.2f}%" if summary["avg_excess_after_cost_pct"] is not None else "- 비용 차감 후 평균 SPY 초과수익: n/a",
        f"- bootstrap 95% CI: {ci[0]:+.2f}% ~ {ci[1]:+.2f}%" if ci[0] is not None and ci[1] is not None else "- bootstrap 95% CI: n/a",
        f"- 평균 20D 불리 이동: {summary['avg_adverse_move_20d_pct']:+.2f}%" if summary["avg_adverse_move_20d_pct"] is not None else "- 평균 20D 불리 이동: n/a",
        "",
        "이 시뮬레이션은 각 기준일을 독립 run으로 취급했다. 과거 하루의 추천은 다음 날 추천 상태를 이어받지 않으며, 보유/현금/체결 상태도 누적하지 않는다.",
        "",
        "## Walk-Forward 검증",
        "",
        "| train | validation | 완료 추천 | 평균 비용차감 SPY 초과 | hit rate |",
        "| --- | --- | ---: | ---: | ---: |",
    ]
    for window in summary["walk_forward"]:
        avg = window["avg_excess_after_cost_pct"]
        hit = window["hit_rate_after_cost_pct"]
        lines.append(
            "| "
            + " | ".join(
                [
                    f"{window['train_start']}~{window['train_end']}",
                    f"{window['validation_start']}~{window['validation_end']}",
                    str(window["completed"]),
                    "n/a" if avg is None else f"{avg:+.2f}%",
                    "n/a" if hit is None else f"{hit:.2f}%",
                ]
            )
            + " |"
        )
    concentration = summary["concentration"]
    lines.extend(
        [
            "",
            "## 집중도와 데이터 품질",
            "",
            f"- 최대 단일 심볼 추천 비중: {concentration['max_single_symbol_recommendation_pct']:.2f}%",
            f"- 최대 단일 테마 추천 비중: {concentration['max_single_theme_recommendation_pct']:.2f}%",
            f"- MCP event feature cache 사용: {str(summary['event_feature_cache_used']).lower()}",
            f"- MCP event feature 매칭 추천: {summary['event_feature_matches']}개 ({summary['event_feature_coverage_pct']:.2f}%)",
            f"- MCP event feature 서버: {', '.join(summary['mcp_event_servers_used']) if summary['mcp_event_servers_used'] else '없음'}",
            f"- 원천 데이터 hash: `{output['data_manifest']['dataset_hash']}`",
            f"- 원천 파일: `{output['data_manifest']['raw_input_file']}`",
            f"- source feed: `{output['data_manifest']['source_feed']}`, bar interval: `{output['data_manifest']['bar_interval']}`",
            "- fill model: 없음. 일봉 정책 검증이며 실제 limit fill probability는 아직 별도 검증 필요.",
            "- slippage model: strategy config의 spread/slippage bps를 단순 비용으로 차감.",
            "",
            "## 정책 반영 검토",
            "",
            "- intraday 전략은 이 결과와 무관하게 `observation_only`이며 자동주문 대상이 아니다.",
            "- 장기 전략은 비용 차감 walk-forward와 집중도 지표를 추가로 기록했지만, quote-level spread/fill 및 공시/실적/밸류에이션 feature가 아직 완전하지 않아 `active_dry_run_candidate` 상태를 유지한다.",
            "- 정책 업데이트는 `harness/recommendation-policy.yaml`의 승격 기준을 기준으로 별도 proposal을 통과해야 한다.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    args = parse_args()
    source = json.loads(args.input_json.read_text(encoding="utf-8"))
    config = load_yaml(args.strategy_config)
    metadata = load_yaml(args.metadata_yaml)
    event_features = load_event_features(args.event_features_json)
    rows = source.get("extracted", {}).get("daily_bars")
    if not isinstance(rows, dict) or "SPY" not in rows or "QQQ" not in rows:
        raise SystemExit("input JSON must contain extracted.daily_bars with SPY and QQQ")
    simulation = simulate(rows, config, metadata, event_features)
    data_manifest = {
        **source.get("data_manifest", {}),
        "dataset_hash": file_sha256(args.input_json),
        "raw_input_file": str(args.input_json),
    }
    if args.event_features_json:
        data_manifest["event_feature_cache_file"] = str(args.event_features_json)
        data_manifest["event_feature_cache_hash"] = file_sha256(args.event_features_json)
    data_gaps = source.get("data_gaps", []) + [
        "Daily bar simulation cannot prove quote-level fill probability.",
    ]
    if args.event_features_json:
        data_gaps.append(
            "Research MCP event features are joined point-in-time by available_at/asof date; missing symbols keep metadata source confidence."
        )
    else:
        data_gaps.append(
            "No research MCP event feature cache was supplied; source confidence uses central symbol metadata buckets."
        )
    output = {
        "run_id": "2026-05-25-one-year-daily-independent-policy-simulation",
        "created_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "paper": True,
        "orders_submitted": 0,
        "strategy_config": str(args.strategy_config),
        "metadata_yaml": str(args.metadata_yaml),
        "event_features_json": str(args.event_features_json) if args.event_features_json else "",
        "data_manifest": data_manifest,
        "data_gaps": data_gaps,
        "simulation": simulation,
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(output, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.write_text(render_markdown(output), encoding="utf-8")
    if args.scorecard_json:
        scorecard = {
            "created_at": output["created_at"],
            "strategy_id": config["strategy_id"],
            "policy_status": config["policy_status"],
            "summary": simulation["summary"],
            "promotion_decision": "active_dry_run_candidate",
            "promotion_reason": "cost-adjusted daily walk-forward recorded, but fill/source/valuation requirements remain incomplete",
            "event_feature_cache_used": bool(args.event_features_json),
        }
        args.scorecard_json.parent.mkdir(parents=True, exist_ok=True)
        args.scorecard_json.write_text(json.dumps(scorecard, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
