#!/usr/bin/env python3
"""Build a self-contained static dashboard for agent run progress.

The generated HTML does not need a local server. It embeds the latest run
snapshot from wiki manifests, reports, order plans, and logs, then links back to
the underlying Markdown/JSON artifacts.
"""

from __future__ import annotations

import argparse
import html as html_lib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "ui" / "agent-dashboard.html"
BACKTEST_OUTPUT_DIR = ROOT / "ui" / "backtests"

AGENTS = [
    {
        "id": "coordinator",
        "name": "Coordinator",
        "label": "계좌",
        "section": "Coordinator Agent",
    },
    {
        "id": "universe",
        "name": "Universe",
        "label": "후보군",
        "section": "Universe Agent",
    },
    {
        "id": "market_data",
        "name": "Market Data",
        "label": "가격",
        "section": "Market Data Agent",
    },
    {
        "id": "web_research",
        "name": "Research",
        "label": "뉴스",
        "section": "Web Research Agent",
    },
    {
        "id": "trend",
        "name": "Trend",
        "label": "점수",
        "section": "Trend Agent",
    },
    {
        "id": "ticker_thesis",
        "name": "Thesis",
        "label": "티커",
        "section": "",
    },
    {
        "id": "risk",
        "name": "Risk",
        "label": "리스크",
        "section": "Portfolio/Risk Agent",
    },
    {
        "id": "executor",
        "name": "Executor",
        "label": "주문",
        "section": "Executor Agent",
    },
    {
        "id": "post_trade",
        "name": "Post-Trade",
        "label": "포지션",
        "section": "Post-Trade Agent",
    },
    {
        "id": "wiki",
        "name": "Wiki",
        "label": "기록",
        "section": "",
    },
]


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""


def load_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return {}
    if not isinstance(data, dict):
        return {}
    return data


def path_from_ref(ref: str) -> Path:
    clean = ref.strip().strip("`")
    return ROOT / clean


def repo_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def href_for(path: str) -> str:
    return "../" + path


def viewer_href(path: Path) -> str:
    return "backtests/" + path.name


def latest_manifest_path() -> Path | None:
    manifest_dir = ROOT / "wiki" / "evidence-store" / "run-manifests"
    candidates = sorted(manifest_dir.glob("*.json"))
    if not candidates:
        return None

    def parsed_time(value: Any) -> float:
        raw = str(value or "").strip()
        if not raw:
            return 0.0
        normalized = raw[:-1] + "+00:00" if raw.endswith("Z") else raw
        try:
            parsed = datetime.fromisoformat(normalized)
        except ValueError:
            return 0.0
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        return parsed.astimezone(timezone.utc).timestamp()

    def sort_key(path: Path) -> tuple[float, str]:
        created_at = load_json(path).get("created_at", "")
        return (parsed_time(created_at), path.name)

    return max(candidates, key=sort_key)


def find_report_path(manifest: dict[str, Any]) -> Path | None:
    for ref in manifest.get("source_refs", []):
        if isinstance(ref, str) and ref.startswith("wiki/current-runs/daily/") and ref.endswith(".md"):
            return path_from_ref(ref)
    for ref in manifest.get("source_refs", []):
        if not isinstance(ref, str) or not ref.startswith("wiki/") or not ref.endswith(".md"):
            continue
        if ref.startswith("wiki/evidence-store/"):
            continue
        path = path_from_ref(ref)
        if path.exists():
            return path
    reports = sorted((ROOT / "wiki" / "current-runs" / "daily").glob("*.md"))
    reports = [path for path in reports if path.name != "README.md"]
    return reports[-1] if reports else None


def extract_section(text: str, heading: str) -> str:
    if not heading:
        return ""
    pattern = rf"^## {re.escape(heading)}\s*$([\s\S]*?)(?=^## |\Z)"
    match = re.search(pattern, text, flags=re.MULTILINE)
    return match.group(1).strip() if match else ""


def parse_table(text: str, heading: str) -> list[dict[str, str]]:
    section = extract_section(text, heading)
    table_lines = [line.strip() for line in section.splitlines() if line.strip().startswith("|")]
    if len(table_lines) < 3:
        return []
    headers = [cell.strip() for cell in table_lines[0].strip("|").split("|")]
    rows: list[dict[str, str]] = []
    for line in table_lines[2:]:
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) != len(headers):
            continue
        rows.append(dict(zip(headers, cells, strict=True)))
    return rows


def frontmatter_value(text: str, key: str) -> str:
    match = re.search(rf"^{re.escape(key)}:\s*(.+)$", text, flags=re.MULTILINE)
    return match.group(1).strip().strip('"') if match else ""


def first_heading(text: str) -> str:
    match = re.search(r"^#\s+(.+)$", text, flags=re.MULTILINE)
    return match.group(1).strip() if match else ""


def bullet_metrics(text: str, heading: str = "결론", limit: int = 4) -> list[str]:
    section = extract_section(text, heading)
    metrics: list[str] = []
    for line in section.splitlines():
        stripped = line.strip()
        if not stripped.startswith("- "):
            continue
        metric = stripped[2:].strip()
        if metric:
            metrics.append(metric)
        if len(metrics) >= limit:
            break
    return metrics


def select_key_metrics(metrics: list[str], limit: int = 3) -> list[str]:
    priority = [
        "hit rate",
        "평균 SPY 초과",
        "평균 초과",
        "SPY 초과수익",
        "P/L",
        "정책 상태",
        "평균 20D 불리",
        "검증",
    ]
    selected: list[str] = []
    for key in priority:
        for metric in metrics:
            if key.lower() in metric.lower() and metric not in selected:
                selected.append(metric)
            if len(selected) >= limit:
                return selected
    for metric in metrics:
        if metric not in selected:
            selected.append(metric)
        if len(selected) >= limit:
            break
    return selected


def strip_frontmatter(text: str) -> str:
    match = re.match(r"^---\s*\n[\s\S]*?\n---\s*\n?", text)
    return text[match.end() :] if match else text


def markdown_href(value: str) -> str:
    href = value.strip()
    if href.startswith(("http://", "https://", "mailto:", "#")):
        return href
    if href.startswith(("../", "./")):
        return href
    if href.startswith(("wiki/", "harness/", "scripts/", "ui/")):
        return "../../" + href
    return href


def render_inline(text: str) -> str:
    rendered = html_lib.escape(text)
    rendered = re.sub(r"`([^`]+)`", r"<code>\1</code>", rendered)
    rendered = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", rendered)
    rendered = re.sub(
        r"\[([^\]]+)\]\(([^)]+)\)",
        lambda match: (
            f'<a href="{html_lib.escape(markdown_href(match.group(2)), quote=True)}">'
            f"{match.group(1)}</a>"
        ),
        rendered,
    )
    rendered = re.sub(r"\[\[([^\]]+)\]\]", r"\1", rendered)
    return rendered


def split_table_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def is_table_separator(line: str) -> bool:
    cells = split_table_row(line)
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", cell.replace(" ", "")) for cell in cells)


def render_table(lines: list[str]) -> str:
    headers = split_table_row(lines[0])
    rows = [split_table_row(line) for line in lines[2:]]
    head = "".join(f"<th>{render_inline(cell)}</th>" for cell in headers)
    body_rows: list[str] = []
    for row in rows:
        padded = row + [""] * max(0, len(headers) - len(row))
        cells = "".join(f"<td>{render_inline(cell)}</td>" for cell in padded[: len(headers)])
        body_rows.append(f"<tr>{cells}</tr>")
    body = "".join(body_rows)
    return f'<div class="table-scroll"><table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>'


def markdown_to_html(text: str) -> str:
    lines = strip_frontmatter(text).strip().splitlines()
    blocks: list[str] = []
    i = 0
    skipped_title = False

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        if not stripped:
            i += 1
            continue

        if stripped.startswith("```"):
            code_lines: list[str] = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                code_lines.append(lines[i])
                i += 1
            if i < len(lines):
                i += 1
            code = html_lib.escape("\n".join(code_lines))
            blocks.append(f"<pre><code>{code}</code></pre>")
            continue

        heading = re.match(r"^(#{1,4})\s+(.+)$", stripped)
        if heading:
            level = len(heading.group(1))
            if level == 1 and not skipped_title:
                skipped_title = True
                i += 1
                continue
            blocks.append(f"<h{level}>{render_inline(heading.group(2))}</h{level}>")
            i += 1
            continue

        if stripped.startswith("|") and i + 1 < len(lines) and is_table_separator(lines[i + 1]):
            table_lines = [stripped, lines[i + 1].strip()]
            i += 2
            while i < len(lines) and lines[i].strip().startswith("|"):
                table_lines.append(lines[i].strip())
                i += 1
            blocks.append(render_table(table_lines))
            continue

        if re.match(r"^\s*[-*]\s+", line):
            items: list[str] = []
            while i < len(lines) and re.match(r"^\s*[-*]\s+", lines[i]):
                item = re.sub(r"^\s*[-*]\s+", "", lines[i]).strip()
                items.append(f"<li>{render_inline(item)}</li>")
                i += 1
            blocks.append(f"<ul>{''.join(items)}</ul>")
            continue

        paragraph: list[str] = [stripped]
        i += 1
        while i < len(lines):
            candidate = lines[i].strip()
            if not candidate:
                break
            if candidate.startswith(("```", "#", "|")) or re.match(r"^\s*[-*]\s+", lines[i]):
                break
            paragraph.append(candidate)
            i += 1
        blocks.append(f"<p>{render_inline(' '.join(paragraph))}</p>")

    return "\n".join(blocks)


def backtest_view_html(source_path: Path, title: str, body_html: str) -> str:
    safe_title = html_lib.escape(title)
    source_label = html_lib.escape(repo_path(source_path))
    return f"""<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{safe_title}</title>
  <style>
    :root {{
      color-scheme: light;
      --bg: #f7f7f4;
      --ink: #202523;
      --muted: #68716d;
      --line: #dde2da;
      --panel: #ffffff;
      --soft: #eef2ec;
      --blue: #1f5f99;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      min-height: 100vh;
      background: var(--bg);
      color: var(--ink);
      font: 15px/1.55 ui-sans-serif, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }}
    a {{ color: var(--blue); text-decoration: none; }}
    .page {{ width: min(980px, calc(100vw - 28px)); margin: 0 auto; padding: 22px 0 44px; }}
    header {{
      display: flex;
      align-items: flex-start;
      justify-content: space-between;
      gap: 16px;
      margin-bottom: 18px;
    }}
    .source {{ color: var(--muted); font-size: 12px; word-break: break-all; margin-top: 7px; }}
    h1 {{ margin: 0; font-size: clamp(26px, 4vw, 42px); line-height: 1.08; letter-spacing: 0; }}
    .actions {{ display: flex; gap: 8px; flex-wrap: wrap; justify-content: flex-end; }}
    .btn {{
      display: inline-flex;
      align-items: center;
      height: 36px;
      padding: 0 11px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: var(--panel);
      color: var(--ink);
      font-size: 13px;
      white-space: nowrap;
    }}
    main {{
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: clamp(16px, 3vw, 28px);
    }}
    main h1 {{ font-size: clamp(24px, 3vw, 34px); margin: 0 0 18px; }}
    h2 {{ margin: 28px 0 10px; font-size: 20px; letter-spacing: 0; }}
    h3 {{ margin: 22px 0 8px; font-size: 17px; letter-spacing: 0; }}
    h4 {{ margin: 18px 0 8px; font-size: 15px; letter-spacing: 0; }}
    p {{ margin: 10px 0; }}
    ul {{ margin: 8px 0 16px; padding-left: 20px; }}
    li {{ margin: 5px 0; }}
    code {{
      background: var(--soft);
      border-radius: 5px;
      padding: 1px 5px;
      font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
      font-size: 0.92em;
    }}
    pre {{
      overflow: auto;
      background: #202523;
      color: #f7f7f4;
      border-radius: 8px;
      padding: 14px;
    }}
    pre code {{ background: transparent; color: inherit; padding: 0; }}
    .table-scroll {{ overflow-x: auto; margin: 12px 0 20px; border: 1px solid var(--line); border-radius: 8px; }}
    table {{ width: 100%; border-collapse: collapse; min-width: 620px; }}
    th, td {{ border-bottom: 1px solid var(--line); padding: 9px 10px; text-align: left; vertical-align: top; }}
    th {{ background: var(--soft); font-size: 12px; color: var(--muted); }}
    tr:last-child td {{ border-bottom: 0; }}
    @media (max-width: 620px) {{
      header {{ display: block; }}
      .actions {{ justify-content: flex-start; margin-top: 12px; }}
      main {{ padding: 14px; }}
    }}
  </style>
</head>
<body>
  <div class="page">
    <header>
      <div>
        <h1>{safe_title}</h1>
        <div class="source">{source_label}</div>
      </div>
      <nav class="actions" aria-label="문서 이동">
        <a class="btn" href="../agent-dashboard.html">Dashboard</a>
      </nav>
    </header>
    <main>
{body_html}
    </main>
  </div>
</body>
</html>
"""


def write_backtest_view(path: Path) -> Path:
    text = read_text(path)
    title = first_heading(text) or path.stem
    BACKTEST_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output = BACKTEST_OUTPUT_DIR / f"{path.stem}.html"
    output.write_text(backtest_view_html(path, title, markdown_to_html(text)), encoding="utf-8")
    return output


def backtest_results(limit: int = 4) -> list[dict[str, Any]]:
    result_dir = ROOT / "wiki" / "backtest-runs" / "results"
    paths = sorted(path for path in result_dir.glob("*.md") if path.name != "README.md")

    def sort_key(path: Path) -> tuple[str, str]:
        text = read_text(path)
        created_at = frontmatter_value(text, "created_at")
        return (created_at or path.name[:10], path.name)

    items: list[dict[str, Any]] = []
    for path in sorted(paths, key=sort_key, reverse=True)[:limit]:
        text = read_text(path)
        view_path = write_backtest_view(path)
        metrics = select_key_metrics(bullet_metrics(text, limit=12))
        if not metrics:
            table = parse_table(text, "일별 장타형 정책 결과") or parse_table(text, "단타형 3시간 정책 결과")
            for row in table[:2]:
                policy = row.get("정책", "")
                value = row.get("평균 SPY 초과") or row.get("P/L") or row.get("hit rate") or ""
                if policy and value:
                    metrics.append(f"{policy}: {value}")
        items.append(
            {
                "title": first_heading(text) or path.stem,
                "type": frontmatter_value(text, "source_type") or "backtest",
                "created_at": frontmatter_value(text, "created_at") or path.name[:10],
                "metrics": metrics[:4],
                "path": repo_path(path),
                "href": viewer_href(view_path),
            }
        )
    return items


def log_entries(limit: int = 3) -> list[dict[str, str]]:
    text = read_text(ROOT / "wiki" / "log.md")
    matches = list(re.finditer(r"^## \[(?P<time>[^\]]+)\]\s+(?P<type>[^|]+)\|\s+(?P<title>.+)$", text, re.M))
    entries: list[dict[str, str]] = []
    for match in matches[-limit:][::-1]:
        entries.append(
            {
                "time": match.group("time").strip(),
                "type": match.group("type").strip(),
                "title": match.group("title").strip(),
            }
        )
    return entries


def to_float(value: Any) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def pct_text(value: float | None) -> str:
    return "-" if value is None else f"{value:.0f}%"


def account_snapshot(order_plan: dict[str, Any]) -> dict[str, Any]:
    account = order_plan.get("account", {}) if isinstance(order_plan.get("account"), dict) else {}
    positions = order_plan.get("positions", []) if isinstance(order_plan.get("positions"), list) else []
    portfolio_value = to_float(account.get("portfolio_value")) or 0.0
    cash = to_float(account.get("cash")) or 0.0
    invested = sum(to_float(position.get("market_value")) or 0.0 for position in positions if isinstance(position, dict))
    cash_ratio = cash / portfolio_value * 100 if portfolio_value else None
    invested_ratio = invested / portfolio_value * 100 if portfolio_value else None
    return {
        "portfolio_value": portfolio_value,
        "cash": cash,
        "invested": invested,
        "cash_ratio": cash_ratio,
        "invested_ratio": invested_ratio,
    }


def enriched_picks(report_text: str) -> list[dict[str, str]]:
    rec_rows = parse_table(report_text, "추천 조치")
    market_rows = {row.get("심볼", ""): row for row in parse_table(report_text, "Market Data Agent")}
    trend_rows = {row.get("심볼", ""): row for row in parse_table(report_text, "Trend Agent")}
    picks: list[dict[str, str]] = []
    for row in rec_rows[:3]:
        symbol = row.get("심볼", "")
        market = market_rows.get(symbol, {})
        trend = trend_rows.get(symbol, {})
        picks.append(
            {
                "symbol": symbol,
                "action": row.get("조치", ""),
                "reason": row.get("이유", ""),
                "score": trend.get("점수", ""),
                "confidence": trend.get("신뢰도", ""),
                "return_20d": market.get("20D", ""),
                "vs_spy_20d": market.get("SPY 대비 20D", ""),
                "risk": trend.get("판단", ""),
            }
        )
    return picks


def compact_agent_result(agent_id: str, manifest: dict[str, Any], report_text: str, order_plan: dict[str, Any]) -> str:
    risk = manifest.get("risk_check_result", {})
    data_manifest = manifest.get("data_manifest", {})
    orders = order_plan.get("orders", []) if isinstance(order_plan.get("orders"), list) else []
    submitted = manifest.get("submitted_order_ids", [])
    mcp_used = manifest.get("mcp_servers_used", [])

    if agent_id == "coordinator":
        market = order_plan.get("market", {}) if isinstance(order_plan.get("market"), dict) else {}
        return "open" if market.get("is_open") else "closed"
    if agent_id == "universe":
        loaded = data_manifest.get("symbols_loaded", "")
        return f"{loaded} symbols" if loaded != "" else "ready"
    if agent_id == "market_data":
        feed = data_manifest.get("source_feed", "data")
        interval = data_manifest.get("bar_interval", "")
        return f"{feed} {interval}".strip()
    if agent_id == "web_research":
        return " + ".join(mcp_used) if mcp_used else "sources"
    if agent_id == "trend":
        rows = parse_table(report_text, "Trend Agent")
        top = [row.get("심볼", "") for row in rows[:3] if row.get("심볼")]
        return " / ".join(top) if top else "scored"
    if agent_id == "ticker_thesis":
        rows = parse_table(report_text, "추천 조치")
        top = [row.get("심볼", "") for row in rows[:3] if row.get("심볼")]
        return " / ".join(top) if top else "notes"
    if agent_id == "risk":
        return str(risk.get("status", "check"))
    if agent_id == "executor":
        return f"{len(submitted)} submitted"
    if agent_id == "post_trade":
        return "positions"
    if agent_id == "wiki":
        return "index + log"
    return "ready"


def agent_cards(manifest: dict[str, Any], report_text: str, order_plan: dict[str, Any]) -> list[dict[str, Any]]:
    mcp_failures = manifest.get("mcp_failures", [])
    report_has_run = bool(report_text)
    order_plan_exists = bool(order_plan)
    risk_status = str(manifest.get("risk_check_result", {}).get("status", "")).upper()
    submitted = manifest.get("submitted_order_ids", [])
    log_text = read_text(ROOT / "wiki" / "log.md")
    run_id = str(manifest.get("run_id", ""))

    cards: list[dict[str, Any]] = []
    for agent in AGENTS:
        section_done = bool(agent["section"] and extract_section(report_text, agent["section"]))
        status = "waiting"
        progress = 20

        if section_done:
            status = "done"
            progress = 100
        if agent["id"] == "ticker_thesis" and report_has_run:
            status = "done"
            progress = 100
        if agent["id"] == "risk" and order_plan_exists:
            status = "done" if risk_status == "PASS" else "blocked"
            progress = 100
        if agent["id"] == "executor" and report_has_run:
            status = "skipped" if not submitted else "done"
            progress = 100
        if agent["id"] == "post_trade" and report_has_run:
            status = "done"
            progress = 100
        if agent["id"] == "wiki" and run_id and run_id in log_text:
            status = "done"
            progress = 100
        if agent["id"] == "web_research" and mcp_failures and status == "done":
            status = "watch"
            progress = 90

        cards.append(
            {
                "id": agent["id"],
                "name": agent["name"],
                "label": agent["label"],
                "status": status,
                "progress": progress,
                "result": compact_agent_result(agent["id"], manifest, report_text, order_plan),
            }
        )
    return cards


def link_item(label: str, path: str) -> dict[str, str]:
    return {"label": label, "path": path, "href": href_for(path)}


def build_dashboard_data() -> dict[str, Any]:
    manifest_path = latest_manifest_path()
    manifest = load_json(manifest_path) if manifest_path else {}
    report_path = find_report_path(manifest) if manifest else None
    report_text = read_text(report_path) if report_path else ""

    order_plan_path_raw = manifest.get("order_plan_path", "")
    order_plan_path = path_from_ref(order_plan_path_raw) if order_plan_path_raw else None
    order_plan = load_json(order_plan_path) if order_plan_path else {}

    recommendation_rows = parse_table(report_text, "추천 조치")
    trend_rows = parse_table(report_text, "Trend Agent")
    risk = manifest.get("risk_check_result", {})
    market = order_plan.get("market", {}) if isinstance(order_plan.get("market"), dict) else {}
    data_manifest = manifest.get("data_manifest", {})
    orders = order_plan.get("orders", []) if isinstance(order_plan.get("orders"), list) else []
    submitted = manifest.get("submitted_order_ids", [])
    account = account_snapshot(order_plan)
    warnings = risk.get("warnings", []) + [item.get("reason", "") for item in manifest.get("mcp_failures", [])]
    market_closed = not bool(market.get("is_open"))
    no_orders = len(orders) == 0 and len(submitted) == 0
    if market_closed and no_orders:
        action_label = "관망"
        action_reason = "장 닫힘 · 현재가 확인 대기"
    elif no_orders:
        action_label = "검토"
        action_reason = "주문 후보 없음"
    else:
        action_label = "주문 후보"
        action_reason = f"{len(orders)}건"

    links: list[dict[str, str]] = []
    if report_path:
        links.append(link_item("리포트", repo_path(report_path)))
    if order_plan_path:
        links.append(link_item("주문계획", repo_path(order_plan_path)))
    if manifest_path:
        links.append(link_item("Manifest", repo_path(manifest_path)))
    position_path = ROOT / "wiki" / "trade-ledger" / "positions" / "current.md"
    if position_path.exists():
        links.append(link_item("포지션", repo_path(position_path)))
    for ref in manifest.get("source_refs", []):
        if isinstance(ref, str) and ref.startswith("wiki/evidence-store/sources/"):
            path = path_from_ref(ref)
            if path.exists():
                links.append(link_item(path.name, repo_path(path)))

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "run": {
            "run_id": manifest.get("run_id", "no-run"),
            "mode": manifest.get("mode", ""),
            "created_at": manifest.get("created_at", ""),
            "paper": bool(manifest.get("paper", False)),
            "risk_status": risk.get("status", "UNKNOWN"),
            "market": "open" if market.get("is_open") else "closed",
            "next_open": market.get("next_open", ""),
            "orders_planned": len(orders),
            "orders_submitted": len(submitted),
            "symbols_loaded": data_manifest.get("symbols_loaded", 0),
            "cash_ratio": account.get("cash_ratio"),
            "invested_ratio": account.get("invested_ratio"),
            "action_label": action_label,
            "action_reason": action_reason,
        },
        "account": account,
        "agents": agent_cards(manifest, report_text, order_plan),
        "picks": enriched_picks(report_text),
        "recommendations": recommendation_rows,
        "scores": trend_rows,
        "links": links,
        "timeline": log_entries(),
        "backtests": backtest_results(),
        "warnings": warnings,
    }


def html_template(data: dict[str, Any]) -> str:
    embedded = json.dumps(data, ensure_ascii=False, indent=2).replace("</", "<\\/")
    return f"""<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Agent Run Board</title>
  <style>
    :root {{
      color-scheme: light;
      --bg: #f7f7f4;
      --ink: #1f2423;
      --muted: #69736f;
      --line: #dfe3dc;
      --panel: #ffffff;
      --soft: #eef2ec;
      --done: #16845b;
      --watch: #b7791f;
      --skip: #52677a;
      --wait: #929b96;
      --blocked: #be3a34;
      --blue: #1f5f99;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      min-height: 100vh;
      background: var(--bg);
      color: var(--ink);
      font: 14px/1.35 ui-sans-serif, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }}
    a {{ color: inherit; text-decoration: none; }}
    .wrap {{ width: min(1120px, calc(100vw - 28px)); margin: 0 auto; padding: 22px 0 32px; }}
    header {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 14px;
      padding: 4px 0 18px;
    }}
    h1 {{ margin: 0; font-size: clamp(26px, 4vw, 42px); letter-spacing: 0; line-height: 1; }}
    .sub {{ margin-top: 7px; color: var(--muted); font-size: 13px; }}
    .icon-btn {{
      width: 40px;
      height: 40px;
      border: 1px solid var(--line);
      background: var(--panel);
      color: var(--ink);
      border-radius: 8px;
      cursor: pointer;
      font-size: 18px;
    }}
    .topline {{
      display: grid;
      grid-template-columns: repeat(4, minmax(130px, 1fr));
      gap: 8px;
      margin-bottom: 14px;
    }}
    .pill {{
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 12px 14px;
      min-height: 68px;
    }}
    .pill span {{ color: var(--muted); display: block; font-size: 12px; }}
    .pill b {{ display: block; font-size: 24px; line-height: 1.1; margin-top: 4px; }}
    .decision {{
      display: grid;
      grid-template-columns: 150px 1fr;
      gap: 8px;
      align-items: center;
      background: var(--ink);
      color: white;
      border-radius: 8px;
      padding: 13px 15px;
      margin-bottom: 10px;
    }}
    .decision b {{ font-size: 25px; line-height: 1; }}
    .decision span {{ color: #dbe3dd; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }}
    .rail {{
      display: grid;
      grid-template-columns: repeat(10, minmax(72px, 1fr));
      gap: 6px;
      margin: 0 0 18px;
    }}
    .stage {{
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      min-height: 84px;
      padding: 10px 8px;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      gap: 7px;
    }}
    .dot {{
      width: 18px;
      height: 18px;
      border-radius: 50%;
      background: var(--wait);
    }}
    .stage.done .dot {{ background: var(--done); }}
    .stage.watch .dot {{ background: var(--watch); }}
    .stage.skipped .dot {{ background: var(--skip); }}
    .stage.blocked .dot {{ background: var(--blocked); }}
    .stage b {{ font-size: 12px; letter-spacing: 0; }}
    .stage span {{ color: var(--muted); font-size: 11px; max-width: 100%; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }}
    .main {{
      display: grid;
      grid-template-columns: minmax(0, 0.95fr) minmax(0, 1.05fr);
      gap: 14px;
      align-items: start;
    }}
    .panel {{
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 14px;
    }}
    h2 {{ margin: 0 0 12px; font-size: 13px; color: var(--muted); font-weight: 800; letter-spacing: 0; }}
    .rank-list {{ display: grid; gap: 8px; }}
    .pick {{
      display: grid;
      grid-template-columns: 80px 1fr;
      gap: 10px;
      background: var(--soft);
      border-radius: 8px;
      padding: 10px;
      min-height: 92px;
    }}
    .symbol {{ font-size: 25px; font-weight: 900; letter-spacing: 0; }}
    .pick-side {{ display: flex; flex-direction: column; justify-content: center; gap: 5px; }}
    .score {{ color: var(--blue); font-size: 12px; font-weight: 800; }}
    .pick-main {{ min-width: 0; display: grid; gap: 7px; }}
    .action {{ font-weight: 800; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }}
    .reason {{ color: var(--muted); overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }}
    .chips {{ display: flex; gap: 5px; flex-wrap: wrap; }}
    .chip {{
      display: inline-flex;
      align-items: center;
      min-height: 24px;
      padding: 0 8px;
      border-radius: 999px;
      background: white;
      color: var(--muted);
      font-size: 12px;
      border: 1px solid var(--line);
    }}
    .backtests {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 8px; }}
    .backtest {{
      background: var(--soft);
      border-radius: 8px;
      padding: 11px;
      min-height: 104px;
      overflow: hidden;
    }}
    .backtest b {{
      display: block;
      font-size: 14px;
      line-height: 1.2;
      height: 34px;
      overflow: hidden;
    }}
    .backtest span {{ display: block; color: var(--muted); font-size: 11px; margin: 5px 0 7px; }}
    .backtest ul {{ margin: 0; padding: 0; list-style: none; display: grid; gap: 3px; color: var(--ink); }}
    .backtest li {{
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
      font-size: 12px;
    }}
    .dock {{
      display: grid;
      grid-template-columns: minmax(0, 1.1fr) minmax(260px, 0.9fr);
      gap: 14px;
      margin-top: 14px;
    }}
    .links {{
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
    }}
    .file {{
      display: inline-flex;
      align-items: center;
      height: 34px;
      padding: 0 11px;
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      max-width: 190px;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
      font-size: 12px;
    }}
    .mini-log {{ display: grid; gap: 6px; }}
    .time {{ color: var(--muted); font-size: 12px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }}
    details {{
      margin-top: 10px;
      color: var(--muted);
      font-size: 12px;
    }}
    summary {{ cursor: pointer; }}
    .warning {{ margin-top: 6px; color: #604715; background: #fff8e8; padding: 8px; border-radius: 6px; }}
    @media (max-width: 960px) {{
      .topline, .main, .dock {{ grid-template-columns: 1fr; }}
      .rail {{ grid-template-columns: repeat(5, minmax(64px, 1fr)); }}
    }}
    @media (max-width: 560px) {{
      .wrap {{ width: min(100vw - 20px, 1120px); padding-top: 14px; }}
      header {{ align-items: flex-start; }}
      .rail {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
      .backtests {{ grid-template-columns: 1fr; }}
      .pick {{ grid-template-columns: 1fr; }}
      .decision {{ grid-template-columns: 1fr; }}
      .symbol {{ font-size: 18px; }}
      .pill b {{ font-size: 20px; }}
    }}
  </style>
</head>
<body>
  <div class="wrap">
    <header>
      <div>
        <h1>Run Board</h1>
        <div class="sub" id="subtitle"></div>
      </div>
      <button class="icon-btn" title="새로고침" aria-label="새로고침" onclick="location.reload()">↻</button>
    </header>

    <div class="decision"><b id="decision-label"></b><span id="decision-reason"></span></div>
    <div class="topline" id="metrics"></div>
    <div class="rail" id="agents"></div>

    <div class="main">
      <section class="panel">
        <h2>Today</h2>
        <div class="rank-list" id="recommendations"></div>
      </section>
      <section class="panel">
        <h2>Backtests</h2>
        <div class="backtests" id="backtests"></div>
      </section>
    </div>

    <div class="dock">
      <section class="panel">
        <h2>Files</h2>
        <div class="links" id="files"></div>
      </section>
      <section class="panel">
        <h2>Log</h2>
        <div class="mini-log" id="timeline"></div>
        <details id="warning-box">
          <summary id="warning-summary"></summary>
          <div id="warnings"></div>
        </details>
      </section>
    </div>
  </div>

  <script type="application/json" id="dashboard-data">{embedded}</script>
  <script>
    const data = JSON.parse(document.getElementById('dashboard-data').textContent);
    const byId = (id) => document.getElementById(id);
    const esc = (value) => String(value ?? '').replace(/[&<>"']/g, (ch) => ({{
      '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
    }}[ch]));
    const compact = (value, max = 34) => {{
      const text = String(value ?? '').replace(/`/g, '').trim();
      return text.length > max ? `${{text.slice(0, max - 1)}}…` : text;
    }};
    const cleanTitle = (value) => compact(String(value ?? '').replace(/^과거\\s*/, ''), 32);

    byId('subtitle').textContent = `${{data.run.mode || '-'}} · ${{data.run.run_id}}`;

    byId('decision-label').textContent = data.run.action_label || '-';
    byId('decision-reason').textContent = data.run.action_reason || '';

    const metrics = [
      ['장', data.run.market === 'closed' ? '닫힘' : '열림'],
      ['리스크', data.run.risk_status || '-'],
      ['투자', `${{Math.round(data.run.invested_ratio || 0)}}%`],
      ['현금', `${{Math.round(data.run.cash_ratio || 0)}}%`],
    ];
    byId('metrics').innerHTML = metrics.map(([label, value]) =>
      `<div class="pill"><span>${{esc(label)}}</span><b>${{esc(value)}}</b></div>`
    ).join('');

    byId('agents').innerHTML = data.agents.map((agent) => `
      <article class="stage ${{esc(agent.status)}}" title="${{esc(agent.name)}} · ${{esc(agent.result)}} · ${{esc(agent.status)}}">
        <div class="dot"></div>
        <b>${{esc(agent.label)}}</b>
        <span>${{esc(compact(agent.result, 14))}}</span>
      </article>
    `).join('');

    const recs = data.picks.length ? data.picks : [];
    byId('recommendations').innerHTML = recs.length ? recs.map((pick) => `
      <div class="pick" title="${{esc(pick.reason || pick.risk)}}">
        <div class="pick-side">
          <div class="symbol">${{esc(pick.symbol || '-')}}</div>
          <div class="score">점수 ${{esc(pick.score || '-')}} · ${{esc(pick.confidence || '-')}}</div>
        </div>
        <div class="pick-main">
          <div class="action">${{esc(compact(pick.action, 42))}}</div>
          <div class="reason">${{esc(compact(pick.reason, 54))}}</div>
          <div class="chips">
            <span class="chip">20D ${{esc(pick.return_20d || '-')}}</span>
            <span class="chip">시장대비 ${{esc(pick.vs_spy_20d || '-')}}</span>
          </div>
        </div>
      </div>
    `).join('') : '<div class="pick"><div class="symbol">-</div><div class="action">No pick</div></div>';

    byId('backtests').innerHTML = data.backtests.map((item) => `
      <a class="backtest" href="${{esc(item.href)}}" target="_blank" title="${{esc(item.path)}}">
        <b>${{esc(cleanTitle(item.title))}}</b>
        <span>${{esc(compact(item.type, 26))}}</span>
        <ul>${{(item.metrics || []).slice(0, 2).map((metric) => `<li>${{esc(compact(metric, 46))}}</li>`).join('')}}</ul>
      </a>
    `).join('');

    byId('files').innerHTML = data.links.slice(0, 8).map((link) =>
      `<a class="file" href="${{esc(link.href)}}" target="_blank" title="${{esc(link.path)}}">${{esc(compact(link.label, 22))}}</a>`
    ).join('');

    byId('timeline').innerHTML = data.timeline.map((item) =>
      `<div class="time" title="${{esc(item.time)}} · ${{esc(item.type)}}">${{esc(compact(item.title, 46))}}</div>`
    ).join('');

    byId('warning-summary').textContent = data.warnings.length ? `주의 ${{data.warnings.length}}건` : '주의 없음';
    byId('warnings').innerHTML = data.warnings.slice(0, 5).map((item) =>
      `<div class="warning">${{esc(compact(item, 120))}}</div>`
    ).join('');
  </script>
</body>
</html>
"""


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a static agent dashboard HTML file.")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    data = build_dashboard_data()
    output = args.output if args.output.is_absolute() else ROOT / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(html_template(data), encoding="utf-8")
    print(repo_path(output))


if __name__ == "__main__":
    main()
