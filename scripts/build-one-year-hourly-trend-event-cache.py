#!/usr/bin/env python3
"""Build point-in-time daily trend event features for hourly simulations.

The cache combines two as-of inputs:

- Alpaca MCP historical news headlines/summaries.
- Previous-close market and sector trend features derived from captured
  Alpaca MCP 1Hour bars.

This helper is read-only. It never submits, replaces, cancels, or closes orders.
"""

from __future__ import annotations

import argparse
import asyncio
import html
import json
import math
import os
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, time, timedelta, timezone
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


ROOT_DIR = Path(__file__).resolve().parents[1]
ET = ZoneInfo("America/New_York")
UTC = ZoneInfo("UTC")
BENCHMARKS = {"SPY", "QQQ", "SMH"}
SEMIS = {"AMD", "AMAT", "ASML", "AVGO", "INTC", "KLAC", "LRCX", "MU", "NVDA", "SMH", "TSM"}

POSITIVE_WORDS = {
    "accelerate",
    "approval",
    "beat",
    "beats",
    "boost",
    "bullish",
    "buy",
    "growth",
    "higher",
    "jump",
    "jumps",
    "outperform",
    "partnership",
    "profit",
    "raise",
    "raises",
    "record",
    "rises",
    "strong",
    "surge",
    "surges",
    "upgrade",
    "upside",
    "win",
    "wins",
}
NEGATIVE_WORDS = {
    "bearish",
    "cut",
    "cuts",
    "downgrade",
    "drop",
    "drops",
    "fall",
    "falls",
    "investigation",
    "lawsuit",
    "miss",
    "misses",
    "plunge",
    "plunges",
    "probe",
    "recall",
    "risk",
    "sell",
    "slump",
    "slumps",
    "tariff",
    "weak",
    "warn",
    "warns",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--hourly-bars-json", type=Path, required=True)
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--raw-news-json", type=Path, required=True)
    parser.add_argument("--source-md", type=Path, required=True)
    parser.add_argument("--batch-symbols", type=int, default=62)
    parser.add_argument("--chunk-days", type=int, default=14)
    parser.add_argument("--news-limit", type=int, default=50)
    parser.add_argument("--reuse-raw-news-json", action="store_true", help="Reuse an existing Alpaca MCP raw news JSON instead of fetching again.")
    parser.add_argument("--progress", action="store_true")
    return parser.parse_args()


def progress(enabled: bool, agent: str, message: str) -> None:
    if enabled:
        print(f"[{agent}] {message}", flush=True)


def read_env() -> dict[str, str]:
    env = os.environ.copy()
    env_file = ROOT_DIR / ".env"
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            if not stripped or stripped.startswith("#") or "=" not in stripped:
                continue
            key, value = stripped.split("=", 1)
            env.setdefault(key.strip(), value.strip().strip('"').strip("'"))
    return env


def parse_tool_payload(result: Any) -> dict[str, Any]:
    for item in getattr(result, "content", []):
        text = getattr(item, "text", None)
        if not text:
            continue
        try:
            payload = json.loads(text)
        except json.JSONDecodeError:
            continue
        if isinstance(payload, dict):
            return payload
    dumped = result.model_dump() if hasattr(result, "model_dump") else {"result": str(result)}
    raise RuntimeError(f"Could not parse MCP tool response as JSON: {dumped}")


def parse_timestamp(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(ET)


def pct(start: float, end: float) -> float:
    return (end / start - 1.0) * 100.0 if start else 0.0


def safe_float(value: Any) -> float | None:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) else None


def as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def market_open_available_at(day: str) -> str:
    return datetime.combine(datetime.fromisoformat(day).date(), time(9, 30), ET).astimezone(UTC).isoformat().replace("+00:00", "Z")


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
                "open": safe_float(row.get("open", row.get("o"))) or 0.0,
                "high": safe_float(row.get("high", row.get("h"))) or 0.0,
                "low": safe_float(row.get("low", row.get("l"))) or 0.0,
                "close": safe_float(row.get("close", row.get("c"))) or 0.0,
                "volume": safe_float(row.get("volume", row.get("v"))) or 0.0,
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
            rows.append(
                {
                    "date": day,
                    "open": float(items[0]["open"]),
                    "high": max(float(row["high"]) for row in items),
                    "low": min(float(row["low"]) for row in items),
                    "close": float(items[-1]["close"]),
                    "volume": sum(float(row["volume"]) for row in items),
                }
            )
        daily[symbol] = rows
    return daily


def fixed_index_by_date(daily: dict[str, list[dict[str, Any]]]) -> dict[str, dict[str, int]]:
    return {symbol: {str(row["date"]): idx for idx, row in enumerate(rows)} for symbol, rows in daily.items()}


def ret(rows: list[dict[str, Any]], idx: int, lookback: int) -> float | None:
    if idx - lookback < 0:
        return None
    return pct(float(rows[idx - lookback]["close"]), float(rows[idx]["close"]))


def avg(values: list[float]) -> float | None:
    return sum(values) / len(values) if values else None


def market_regime_features(daily: dict[str, list[dict[str, Any]]]) -> dict[str, dict[str, Any]]:
    indices = fixed_index_by_date(daily)
    spy_dates = [str(row["date"]) for row in daily["SPY"]]
    out: dict[str, dict[str, Any]] = {}
    for day in spy_dates:
        spy_idx = indices["SPY"].get(day)
        qqq_idx = indices["QQQ"].get(day)
        smh_idx = indices["SMH"].get(day)
        if spy_idx is None or qqq_idx is None or smh_idx is None:
            continue
        prev_spy = spy_idx - 1
        prev_qqq = qqq_idx - 1
        prev_smh = smh_idx - 1
        if prev_spy < 20 or prev_qqq < 20 or prev_smh < 20:
            continue
        spy20 = ret(daily["SPY"], prev_spy, 20)
        qqq20 = ret(daily["QQQ"], prev_qqq, 20)
        smh20 = ret(daily["SMH"], prev_smh, 20)
        if spy20 is None or qqq20 is None or smh20 is None:
            continue
        breadth_values = []
        semi_values = []
        for symbol, rows in daily.items():
            if symbol in BENCHMARKS:
                continue
            idx = indices.get(symbol, {}).get(day)
            if idx is None or idx - 1 < 20:
                continue
            value = ret(rows, idx - 1, 20)
            if value is None:
                continue
            breadth_values.append(value)
            if symbol in SEMIS:
                semi_values.append(value)
        breadth_positive = sum(1 for value in breadth_values if value > 0.0) / len(breadth_values) if breadth_values else 0.0
        semi_breadth_positive = sum(1 for value in semi_values if value > 0.0) / len(semi_values) if semi_values else 0.0
        risk_on = spy20 > 0.0 and qqq20 > 0.0 and breadth_positive >= 0.50
        risk_off = spy20 < -3.0 and qqq20 < -3.0 and breadth_positive < 0.45
        score = 0.0
        if risk_on:
            score += 0.25
        if risk_off:
            score -= 0.45
        if smh20 > 4.0 and semi_breadth_positive >= 0.55:
            score += 0.15
        if smh20 < -4.0 and semi_breadth_positive < 0.45:
            score -= 0.20
        out[day] = {
            "spy20_prev_close_pct": spy20,
            "qqq20_prev_close_pct": qqq20,
            "smh20_prev_close_pct": smh20,
            "breadth20_positive_rate": breadth_positive,
            "semi_breadth20_positive_rate": semi_breadth_positive,
            "market_regime_score_adjustment": score,
            "market_regime": "risk_off" if risk_off else "risk_on" if risk_on else "mixed",
        }
    return out


def tokenize(text: str) -> list[str]:
    return re.findall(r"[a-zA-Z][a-zA-Z'-]+", text.lower())


def news_sentiment_score(article: dict[str, Any]) -> float:
    text = html.unescape(" ".join(str(article.get(key, "")) for key in ("headline", "summary")))
    tokens = tokenize(text)
    counter = Counter(tokens)
    pos = sum(counter[word] for word in POSITIVE_WORDS)
    neg = sum(counter[word] for word in NEGATIVE_WORDS)
    raw = (pos - neg) * 0.18
    return max(-0.9, min(0.9, raw))


def iter_date_chunks(start: str, end: str, chunk_days: int) -> list[tuple[str, str]]:
    start_date = datetime.fromisoformat(start).date()
    end_date = datetime.fromisoformat(end).date()
    chunks = []
    current = start_date
    while current <= end_date:
        chunk_end = min(current + timedelta(days=chunk_days - 1), end_date)
        chunks.append((current.isoformat(), chunk_end.isoformat()))
        current = chunk_end + timedelta(days=1)
    return chunks


async def fetch_news_page(
    session: ClientSession,
    *,
    symbols: list[str],
    start: str,
    end: str,
    limit: int,
    page_token: str | None = None,
) -> dict[str, Any]:
    args: dict[str, Any] = {
        "symbols": ",".join(symbols),
        "start": start,
        "end": end,
        "sort": "asc",
        "limit": limit,
        "include_content": False,
        "exclude_contentless": False,
    }
    if page_token:
        args["page_token"] = page_token
    result = await session.call_tool("get_news", args)
    parsed = parse_tool_payload(result)
    if parsed.get("error"):
        raise RuntimeError(f"MCP get_news returned error: {parsed['error']}")
    return parsed


async def fetch_news(
    symbols: list[str],
    start: str,
    end: str,
    *,
    batch_symbols: int,
    chunk_days: int,
    limit: int,
    progress_enabled: bool,
) -> tuple[list[dict[str, Any]], list[str]]:
    env = read_env()
    if env.get("ALPACA_PAPER_TRADE") != "true":
        raise SystemExit("ALPACA_PAPER_TRADE must be true before fetching Alpaca MCP news.")
    params = StdioServerParameters(
        command=str(ROOT_DIR / "scripts" / "alpaca-mcp.sh"),
        args=[],
        env=env,
        cwd=str(ROOT_DIR),
    )
    articles_by_id: dict[str, dict[str, Any]] = {}
    failures: list[str] = []
    chunks = iter_date_chunks(start, end, chunk_days)
    async with stdio_client(params, errlog=sys.stderr) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            for chunk_index, (chunk_start, chunk_end) in enumerate(chunks, start=1):
                for offset in range(0, len(symbols), batch_symbols):
                    batch = symbols[offset : offset + batch_symbols]
                    progress(
                        progress_enabled,
                        "Web Research Agent",
                        f"Alpaca 뉴스 조회 chunk {chunk_index}/{len(chunks)} {chunk_start}~{chunk_end}, symbols {offset + 1}-{min(offset + batch_symbols, len(symbols))}/{len(symbols)}",
                    )
                    page_token = None
                    page_count = 0
                    while True:
                        page_count += 1
                        try:
                            payload = await fetch_news_page(
                                session,
                                symbols=batch,
                                start=chunk_start,
                                end=chunk_end,
                                limit=limit,
                                page_token=page_token,
                            )
                        except Exception as exc:  # noqa: BLE001
                            failures.append(f"{chunk_start}~{chunk_end} {','.join(batch)} page={page_count}: {exc}")
                            break
                        for article in payload.get("news", []):
                            key = str(article.get("id") or article.get("url") or article.get("headline"))
                            articles_by_id[key] = article
                        page_token = payload.get("next_page_token")
                        if not page_token:
                            break
    return list(articles_by_id.values()), failures


def parse_article_timestamp(article: dict[str, Any]) -> datetime | None:
    value = str(article.get("created_at") or article.get("updated_at") or "")
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(UTC)
    except ValueError:
        return None


def build_news_index(articles: list[dict[str, Any]], universe: set[str]) -> dict[str, list[tuple[datetime, dict[str, Any]]]]:
    indexed: dict[str, list[tuple[datetime, dict[str, Any]]]] = defaultdict(list)
    for article in articles:
        published_at = parse_article_timestamp(article)
        if not published_at:
            continue
        symbols = {str(symbol).upper() for symbol in article.get("symbols", []) if str(symbol).upper() in universe}
        for symbol in symbols:
            indexed[symbol].append((published_at, article))
    return {symbol: sorted(rows, key=lambda item: item[0]) for symbol, rows in indexed.items()}


def news_feature_asof(
    news_index: dict[str, list[tuple[datetime, dict[str, Any]]]],
    symbol: str,
    available_at: datetime,
    *,
    lookback_days: int = 3,
) -> dict[str, Any]:
    window_start = available_at - timedelta(days=lookback_days)
    rows = [
        article
        for published_at, article in news_index.get(symbol, [])
        if window_start <= published_at < available_at
    ]
    scored = [news_sentiment_score(row) for row in rows]
    urls = []
    headlines = []
    for row in rows[:5]:
        if row.get("url"):
            urls.append(str(row["url"]))
        if row.get("headline"):
            headlines.append(html.unescape(str(row["headline"]))[:180])
    return {
        "news_count": len(rows),
        "news_score_adjustment": max(-1.5, min(1.5, sum(scored))),
        "news_positive_articles": sum(1 for value in scored if value > 0),
        "news_negative_articles": sum(1 for value in scored if value < 0),
        "news_headlines_sample": headlines,
        "news_urls_sample": urls,
        "news_lookback_days": lookback_days,
    }


def build_event_cache(
    hourly_source: dict[str, Any],
    news_articles: list[dict[str, Any]],
    news_failures: list[str],
    *,
    hourly_bars_path: Path,
    raw_news_path: Path,
    source_md_path: Path,
) -> dict[str, Any]:
    raw_rows = hourly_source.get("extracted", {}).get("hourly_bars")
    if not isinstance(raw_rows, dict):
        raise ValueError("hourly source must contain extracted.hourly_bars")
    hourly_by_day = build_hourly_by_day(raw_rows)
    daily = aggregate_daily(hourly_by_day)
    indices = fixed_index_by_date(daily)
    universe = set(raw_rows)
    dates = [str(row["date"]) for row in daily["SPY"]]
    regime_by_day = market_regime_features(daily)
    news_index = build_news_index(news_articles, universe)
    features: dict[str, dict[str, Any]] = defaultdict(dict)
    for symbol in sorted(universe):
        if symbol in BENCHMARKS:
            continue
        for day in dates:
            idx = indices.get(symbol, {}).get(day)
            if idx is None or idx < 21 or day not in regime_by_day:
                continue
            regime = regime_by_day[day]
            available_at = market_open_available_at(day)
            available_at_dt = datetime.fromisoformat(available_at.replace("Z", "+00:00")).astimezone(UTC)
            news = news_feature_asof(news_index, symbol, available_at_dt)
            theme_adjustment = 0.0
            if symbol in SEMIS:
                theme_adjustment += 0.12 if regime["smh20_prev_close_pct"] > 4.0 else 0.0
                theme_adjustment -= 0.15 if regime["smh20_prev_close_pct"] < -4.0 else 0.0
            total_adjustment = (
                float(regime["market_regime_score_adjustment"])
                + float(news.get("news_score_adjustment", 0.0))
                + theme_adjustment
            )
            mcp_gaps = [
                "sec-edgar not included in this broad daily trend cache",
                "alpha-vantage earnings calendar/history not included in this broad daily trend cache",
                "fred macro series not included; market regime derived from Alpaca bars",
                "firecrawl IR/press-release capture not included in this broad daily trend cache",
                "yahoo-finance analyst/news not included in this broad daily trend cache",
            ]
            if news_failures:
                mcp_gaps.append("some Alpaca news pages failed; see raw news data_gaps")
            features[symbol][day] = {
                "available_at": available_at,
                "mcp_servers_used": ["alpaca"],
                "source_refs": [
                    str(raw_news_path),
                    str(source_md_path),
                    str(hourly_bars_path),
                ],
                "score_adjustment": round(total_adjustment, 6),
                "source_confidence_delta": 0.03 if news else 0.0,
                "news_score_adjustment": round(float(news.get("news_score_adjustment", 0.0)), 6),
                "macro_score_adjustment": round(float(regime["market_regime_score_adjustment"]) + theme_adjustment, 6),
                "mcp_gaps": mcp_gaps,
                "exclude": False,
                "notes": (
                    f"Alpaca MCP daily trend: market={regime['market_regime']}, "
                    f"news_count={int(news.get('news_count', 0))}, "
                    f"SPY20={regime['spy20_prev_close_pct']:+.2f}%, "
                    f"QQQ20={regime['qqq20_prev_close_pct']:+.2f}%, "
                    f"breadth={regime['breadth20_positive_rate']:.2f}"
                ),
                "trend_features": {
                    **regime,
                    "symbol_news_count": int(news.get("news_count", 0)),
                    "symbol_news_positive_articles": int(news.get("news_positive_articles", 0)),
                    "symbol_news_negative_articles": int(news.get("news_negative_articles", 0)),
                    "symbol_news_lookback_days": int(news.get("news_lookback_days", 0)),
                    "symbol_news_headlines_sample": news.get("news_headlines_sample", []),
                    "symbol_news_urls_sample": news.get("news_urls_sample", []),
                },
            }
    return {
        "schema_version": "event-feature-cache-v1",
        "created_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "paper": True,
        "orders_submitted": 0,
        "description": "Point-in-time daily trend feature cache for one-year hourly buy/sell simulation. Alpaca MCP news plus previous-close market/sector trend features.",
        "mcp_servers_used": ["alpaca"],
        "mcp_gaps": [
            "This is not a full research MCP cache; SEC EDGAR, Alpha Vantage, FRED, Firecrawl, and Yahoo Finance are recorded as gaps per row.",
            "News sentiment is keyword-based and should be treated as a coarse feature, not a factual thesis.",
        ],
        "features": dict(features),
    }


def render_source_md(
    *,
    output_json: Path,
    raw_news_json: Path,
    hourly_bars_json: Path,
    source_md: Path,
    article_count: int,
    failures: list[str],
    event_rows: int,
) -> str:
    return "\n".join(
        [
            "---",
            "id: 2026-05-25-one-year-hourly-trend-event-cache-sources",
            f"created_at: {datetime.now().astimezone().isoformat(timespec='seconds')}",
            "source_type: alpaca-mcp-trend-event-feature-cache",
            "paper: true",
            "orders_submitted: 0",
            "---",
            "",
            "# 과거 1년 1시간봉 시뮬레이션용 일별 동향 feature cache 원천",
            "",
            "## 조회 원천",
            "",
            "- Alpaca MCP: `get_news`",
            "- Alpaca MCP hourly bars: previous-close market/sector trend 계산에 사용",
            f"- hourly bars JSON: `{hourly_bars_json}`",
            f"- raw news JSON: `{raw_news_json}`",
            f"- event cache JSON: `{output_json}`",
            f"- source note: `{source_md}`",
            "",
            "## 캡처 결과",
            "",
            f"- Alpaca news articles captured: {article_count}",
            f"- event feature rows: {event_rows}",
            f"- failed news pages: {len(failures)}",
            "",
            "## 데이터 공백",
            "",
            "- 이번 cache는 광범위한 일별 동향 1차 보강이다.",
            "- SEC filing, Alpha Vantage earnings, FRED macro, Firecrawl IR, Yahoo Finance analyst/news는 전 종목/전일자 풀 coverage로 결합하지 않았다.",
            "- 뉴스 감성 점수는 headline/summary 키워드 기반의 보조 feature다.",
            "- 모든 row의 `available_at`은 해당 미국 거래일 장 시작 시각으로 두고, 뉴스는 `available_at` 이전 3일 window만 집계했다.",
            "",
            "## 실패 기록",
            "",
        ]
        + ([f"- {item}" for item in failures[:50]] if failures else ["- 없음"])
        + [""]
    )


async def main_async(args: argparse.Namespace) -> None:
    source = json.loads(args.hourly_bars_json.read_text(encoding="utf-8"))
    symbols = source.get("request", {}).get("symbols")
    if not isinstance(symbols, list):
        raw_rows = source.get("extracted", {}).get("hourly_bars", {})
        symbols = sorted(raw_rows)
    start = str(source.get("request", {}).get("start", ""))[:10]
    end = str(source.get("request", {}).get("end", ""))[:10]
    if not start or not end:
        raise SystemExit("hourly source request.start/request.end are required")
    if args.reuse_raw_news_json and args.raw_news_json.exists():
        progress(args.progress, "Web Research Agent", "기존 Alpaca MCP raw news JSON을 재사용합니다.")
        raw_news = json.loads(args.raw_news_json.read_text(encoding="utf-8"))
        articles = as_list(raw_news.get("news"))
        failures = [str(item) for item in as_list(raw_news.get("data_gaps"))]
    else:
        progress(args.progress, "Web Research Agent", "Alpaca MCP 과거 뉴스 캡처를 시작합니다.")
        articles, failures = await fetch_news(
            [str(symbol) for symbol in symbols],
            start,
            end,
            batch_symbols=args.batch_symbols,
            chunk_days=args.chunk_days,
            limit=args.news_limit,
            progress_enabled=args.progress,
        )
        raw_news = {
            "created_at": datetime.now().astimezone().isoformat(timespec="seconds"),
            "paper": True,
            "orders_submitted": 0,
            "source": "Alpaca MCP get_news",
            "request": {
                "symbols": symbols,
                "start": start,
                "end": end,
                "batch_symbols": args.batch_symbols,
                "chunk_days": args.chunk_days,
                "limit": args.news_limit,
            },
            "news": articles,
            "data_gaps": failures,
        }
        args.raw_news_json.parent.mkdir(parents=True, exist_ok=True)
        args.raw_news_json.write_text(json.dumps(raw_news, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    progress(args.progress, "Trend Agent", f"뉴스 {len(articles)}개와 hourly trend를 event feature로 변환합니다.")
    cache = build_event_cache(
        source,
        articles,
        failures,
        hourly_bars_path=args.hourly_bars_json,
        raw_news_path=args.raw_news_json,
        source_md_path=args.source_md,
    )
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(cache, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    event_rows = sum(len(rows) for rows in cache["features"].values())
    args.source_md.parent.mkdir(parents=True, exist_ok=True)
    args.source_md.write_text(
        render_source_md(
            output_json=args.output_json,
            raw_news_json=args.raw_news_json,
            hourly_bars_json=args.hourly_bars_json,
            source_md=args.source_md,
            article_count=len(articles),
            failures=failures,
            event_rows=event_rows,
        ),
        encoding="utf-8",
    )
    progress(args.progress, "Trend Agent", f"event feature cache 생성 완료: {event_rows}개 row.")


def main() -> None:
    asyncio.run(main_async(parse_args()))


if __name__ == "__main__":
    main()
