#!/usr/bin/env python3
"""Collect point-in-time MCP context for the 2026-05-15 decision report.

The script only uses read-only MCP tools. It does not submit, replace, cancel,
or close orders.
"""

from __future__ import annotations

import asyncio
import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


ASOF_DATE = "2026-05-15"
ASOF_CUTOFF_UTC = "2026-05-15T20:00:00Z"
NEWS_START = "2026-05-01"
SYMBOLS = ["NOK", "UNH", "GOOGL", "AMD", "MU", "NVDA", "RGTI", "ETN"]


def parse_mcp_text(result: Any) -> Any:
    texts = [getattr(item, "text", None) for item in result.content if getattr(item, "text", None)]
    if not texts:
        return {}
    text = "\n".join(texts)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {"raw_text": text}


async def call_json(session: ClientSession, tool: str, arguments: dict[str, Any] | None = None) -> Any:
    return parse_mcp_text(await session.call_tool(tool, arguments or {}))


def is_asof_available(value: str | None) -> bool:
    if not value:
        return True
    normalized = value.replace("Z", "+00:00")
    try:
        stamp = datetime.fromisoformat(normalized)
    except ValueError:
        return value[:10] <= ASOF_DATE
    cutoff = datetime.fromisoformat(ASOF_CUTOFF_UTC.replace("Z", "+00:00"))
    if stamp.tzinfo is None:
        stamp = stamp.replace(tzinfo=timezone.utc)
    return stamp <= cutoff


async def collect_alpaca(root: Path) -> dict[str, Any]:
    out: dict[str, Any] = {"assets": {}, "news": [], "corporate_actions": {}, "errors": []}
    params = StdioServerParameters(command=str(root / "scripts/alpaca-mcp.sh"), args=[], cwd=root)
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            for symbol in SYMBOLS:
                try:
                    out["assets"][symbol] = await call_json(session, "get_asset", {"symbol_or_asset_id": symbol})
                except Exception as exc:
                    out["errors"].append({"tool": "get_asset", "symbol": symbol, "error": str(exc)})
                try:
                    out["corporate_actions"][symbol] = await call_json(
                        session,
                        "get_corporate_action_announcements",
                        {
                            "ca_types": "Dividend,Merger,Spinoff,Split",
                            "since": NEWS_START,
                            "until": ASOF_DATE,
                            "symbol": symbol,
                        },
                    )
                except Exception as exc:
                    out["errors"].append({"tool": "get_corporate_action_announcements", "symbol": symbol, "error": str(exc)})
            try:
                news = await call_json(
                    session,
                    "get_news",
                    {
                        "symbols": ",".join(SYMBOLS),
                        "start": NEWS_START,
                        "end": ASOF_CUTOFF_UTC,
                        "limit": 50,
                        "sort": "desc",
                        "include_content": False,
                    },
                )
                rows = news.get("news", news if isinstance(news, list) else [])
                out["news"] = [
                    {
                        "created_at": row.get("created_at"),
                        "updated_at": row.get("updated_at"),
                        "headline": row.get("headline"),
                        "summary": row.get("summary") or "",
                        "symbols": row.get("symbols", []),
                        "source": row.get("source"),
                        "url": row.get("url"),
                    }
                    for row in rows
                    if is_asof_available(row.get("created_at"))
                ]
            except Exception as exc:
                out["errors"].append({"tool": "get_news", "symbols": SYMBOLS, "error": str(exc)})
    return out


async def collect_sec(root: Path) -> dict[str, Any]:
    out: dict[str, Any] = {"companies": {}, "filings": {}, "errors": []}
    params = StdioServerParameters(command=str(root / "scripts/mcp-sec-edgar.sh"), args=[], cwd=root)
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            for symbol in SYMBOLS:
                try:
                    out["companies"][symbol] = await call_json(session, "get_company_info", {"identifier": symbol})
                except Exception as exc:
                    out["errors"].append({"tool": "get_company_info", "symbol": symbol, "error": str(exc)})
                try:
                    filings = await call_json(session, "get_recent_filings", {"identifier": symbol, "days": 90, "limit": 12})
                    rows = filings.get("filings", [])
                    out["filings"][symbol] = [
                        row
                        for row in rows
                        if row.get("filing_date", "") <= ASOF_DATE and is_asof_available(row.get("acceptance_datetime"))
                    ][:6]
                except Exception as exc:
                    out["errors"].append({"tool": "get_recent_filings", "symbol": symbol, "error": str(exc)})
    return out


def compact_news_by_symbol(news: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in news:
        for symbol in row.get("symbols", []):
            if symbol in SYMBOLS and len(grouped[symbol]) < 5:
                grouped[symbol].append(row)
    return dict(grouped)


def render_markdown(data: dict[str, Any]) -> str:
    lines = [
        "---",
        "id: 2026-05-24-may-15-mcp-context-sources",
        f"created_at: {data['created_at']}",
        "source_type: mcp-context-for-historical-decision",
        "historical_asof: 2026-05-15",
        "paper: true",
        "orders_submitted: 0",
        "---",
        "",
        "# 2026-05-15 의사결정용 MCP 보강 원천",
        "",
        "## 조회 범위",
        "",
        f"- 기준 시점: `{ASOF_CUTOFF_UTC}`",
        f"- 대상 심볼: `{', '.join(SYMBOLS)}`",
        "- 사용 MCP: Alpaca, SEC EDGAR",
        "- 실제 주문, 취소, 포지션 변경 없음.",
        "",
        "## Alpaca Asset 상태",
        "",
        "| 심볼 | 이름 | 거래 가능 | marginable | shortable | fractionable | 주요 속성 |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for symbol in SYMBOLS:
        asset = data["alpaca"]["assets"].get(symbol, {})
        lines.append(
            "| "
            + " | ".join(
                [
                    symbol,
                    str(asset.get("name", ""))[:80],
                    str(asset.get("tradable", "")),
                    str(asset.get("marginable", "")),
                    str(asset.get("shortable", "")),
                    str(asset.get("fractionable", "")),
                    ", ".join(asset.get("attributes", [])[:4]),
                ]
            )
            + " |"
        )
    lines.extend(["", "## Alpaca News", ""])
    grouped_news = compact_news_by_symbol(data["alpaca"]["news"])
    for symbol in SYMBOLS:
        lines.append(f"### {symbol}")
        rows = grouped_news.get(symbol, [])
        if not rows:
            lines.append("- 기준 기간 내 Alpaca 뉴스 없음.")
        for row in rows:
            summary = (row.get("summary") or "").replace("\n", " ").strip()
            lines.append(f"- `{row.get('created_at')}` {row.get('headline')} ({row.get('source')})")
            if summary:
                lines.append(f"  - 요약: {summary[:220]}")
            if row.get("url"):
                lines.append(f"  - URL: {row.get('url')}")
        lines.append("")
    lines.extend(["## SEC EDGAR 회사/filing", ""])
    for symbol in SYMBOLS:
        company = data["sec"]["companies"].get(symbol, {}).get("company", {})
        lines.append(f"### {symbol}")
        if company:
            lines.append(
                f"- 회사명: {company.get('name')} / CIK: {company.get('cik')} / SIC: {company.get('sic')} / fiscal year end: {company.get('fiscal_year_end')}"
            )
        filings = data["sec"]["filings"].get(symbol, [])
        if not filings:
            lines.append("- 기준 시점까지 사용 가능한 최근 SEC filing 없음.")
        for row in filings:
            lines.append(
                f"- `{row.get('acceptance_datetime')}` {row.get('form_type')} accession `{row.get('accession_number')}`, filing date `{row.get('filing_date')}`, period `{row.get('period_of_report')}`"
            )
        lines.append("")
    lines.extend(["## 데이터 공백", ""])
    if data["alpaca"].get("errors") or data["sec"].get("errors"):
        for err in data["alpaca"].get("errors", []) + data["sec"].get("errors", []):
            lines.append(f"- {err}")
    else:
        lines.append("- Alpaca/SEC MCP 호출은 성공했다.")
    lines.extend(
        [
            "- Alpha Vantage, Yahoo Finance, Firecrawl, FRED는 이번 보강 리포트의 판단 근거에는 포함하지 않았다. 기준 시점 이전 정보만 엄격히 분리하기 위해 Alpaca historical news와 SEC acceptance time 기준 filing을 우선 사용했다.",
            "- SEC filing은 `acceptance_datetime <= 2026-05-15T20:00:00Z`인 항목만 의사결정 근거로 분류했다.",
            "- 뉴스 본문 전문은 저장하지 않고 headline/summary/source/url만 기록했다.",
        ]
    )
    return "\n".join(lines) + "\n"


async def main() -> None:
    root = Path(__file__).resolve().parents[1]
    data = {
        "created_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "historical_asof": ASOF_DATE,
        "asof_cutoff_utc": ASOF_CUTOFF_UTC,
        "symbols": SYMBOLS,
        "alpaca": await collect_alpaca(root),
        "sec": await collect_sec(root),
    }
    out_json = root / "wiki/raw/sources/2026-05-24-may-15-mcp-context-data.json"
    out_md = root / "wiki/raw/sources/2026-05-24-may-15-mcp-context-sources.md"
    out_json.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    out_md.write_text(render_markdown(data), encoding="utf-8")
    print(json.dumps({"json": str(out_json), "md": str(out_md), "news_count": len(data["alpaca"]["news"])}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
