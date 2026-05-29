#!/usr/bin/env python3
from __future__ import annotations

import argparse
from datetime import datetime
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]


def load_json(path: Path) -> dict[str, Any]:
    try:
        with path.open("r", encoding="utf-8") as handle:
            payload = json.load(handle)
    except (OSError, json.JSONDecodeError):
        return {}
    return payload if isinstance(payload, dict) else {}


def first_match(pattern: str, text: str) -> str:
    match = re.search(pattern, text, flags=re.IGNORECASE)
    return match.group(1).strip() if match else ""


def compact_client_id(client_id: str) -> str:
    if len(client_id) <= 34:
        return client_id
    return client_id[:31] + "..."


def to_float(value: Any) -> float | None:
    if isinstance(value, (int, float)):
        return float(value)
    if value is None:
        return None
    text = str(value).replace(",", "").replace("$", "").replace("%", "").strip()
    match = re.search(r"-?\d+(?:\.\d+)?", text)
    return float(match.group(0)) if match else None


def fmt_usd(value: Any) -> str:
    number = to_float(value)
    if number is None:
        return "확인불가"
    sign = "-" if number < 0 else ""
    return f"{sign}${abs(number):,.0f}"


def fmt_pct(value: Any) -> str:
    number = to_float(value)
    if number is None:
        return "확인불가"
    return f"{number:+.1f}%"


def fmt_pct_plain(value: Any) -> str:
    number = to_float(value)
    if number is None:
        return "확인불가"
    return f"{number:.1f}%"


def one_line(text: Any, fallback: str = "조건 미충족") -> str:
    cleaned = re.sub(r"\s+", " ", str(text or "")).strip()
    if not cleaned:
        return fallback
    first = re.split(r"(?<=[.!?다])\s+", cleaned, maxsplit=1)[0].strip()
    return first[:36]


def run_time_label(run_id: str) -> str:
    match = re.match(r"(\d{4}-\d{2}-\d{2})-(\d{2})(\d{2})", run_id)
    if match:
        return f"{match.group(1)} {match.group(2)}:{match.group(3)} KST"
    return datetime.now().astimezone().strftime("%Y-%m-%d %H:%M %Z")


def current_position_text(root: Path) -> str:
    path = root / "wiki" / "trade-ledger" / "positions" / "current.md"
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return ""


def account_from_current_md(text: str) -> dict[str, Any]:
    match = re.search(
        r"Account:\s*`?([^,`]+)`?,\s*portfolio_value\s+([0-9.]+),\s*cash\s+([0-9.]+),\s*buying_power\s+([0-9.]+),\s*long_market_value\s+([0-9.]+)",
        text,
    )
    count_match = re.search(r"총 position symbols\s+([0-9]+)개", text)
    if not match:
        return {"positions_count": int(count_match.group(1)) if count_match else None}
    return {
        "portfolio_value": to_float(match.group(2)),
        "cash": to_float(match.group(3)),
        "buying_power": to_float(match.group(4)),
        "long_market_value": to_float(match.group(5)),
        "positions_count": int(count_match.group(1)) if count_match else None,
    }


def latest_positions(root: Path, current_run_id: str, order_plan: dict[str, Any]) -> list[dict[str, Any]]:
    positions = order_plan.get("positions") if isinstance(order_plan.get("positions"), list) else []
    if positions:
        return [row for row in positions if isinstance(row, dict)]
    paths = sorted((root / "wiki" / "trade-ledger" / "orders").glob("*.json"), reverse=True)
    for path in paths:
        if current_run_id in path.name:
            continue
        payload = load_json(path)
        rows = payload.get("positions") if isinstance(payload.get("positions"), list) else []
        if rows:
            return [row for row in rows if isinstance(row, dict)]
    return []


def alpaca_account_from_preflight(root: Path, run_id: str) -> dict[str, Any]:
    path = root / "wiki" / "evidence-store" / "sources" / f"{run_id}-alpaca-core-preflight.json"
    payload = load_json(path)
    tool_results = payload.get("tool_results") if isinstance(payload.get("tool_results"), dict) else {}
    account_result = tool_results.get("get_account_info") if isinstance(tool_results.get("get_account_info"), dict) else {}
    account = account_result.get("payload") if isinstance(account_result.get("payload"), dict) else {}
    return account


def portfolio_metrics(root: Path, run_id: str, order_plan: dict[str, Any]) -> dict[str, Any]:
    current_account = account_from_current_md(current_position_text(root))
    preflight_account = alpaca_account_from_preflight(root, run_id)
    account = order_plan.get("account") if isinstance(order_plan.get("account"), dict) else {}
    portfolio_value = (
        to_float(account.get("portfolio_value"))
        or to_float(preflight_account.get("portfolio_value"))
        or to_float(current_account.get("portfolio_value"))
    )
    cash = to_float(account.get("cash")) or to_float(preflight_account.get("cash")) or to_float(current_account.get("cash"))
    buying_power = (
        to_float(account.get("buying_power"))
        or to_float(preflight_account.get("buying_power"))
        or to_float(current_account.get("buying_power"))
        or cash
    )
    positions = latest_positions(root, run_id, order_plan)
    positions_count = len(positions) or current_account.get("positions_count")
    cost_basis = 0.0
    unrealized = 0.0
    invested = 0.0
    for position in positions:
        qty = to_float(position.get("qty")) or 0.0
        market_value = to_float(position.get("market_value")) or 0.0
        current_price = to_float(position.get("current_price"))
        avg_entry = to_float(position.get("avg_entry_price"))
        invested += market_value
        if qty and avg_entry is not None and current_price is not None:
            cost = qty * avg_entry
            cost_basis += cost
            unrealized += qty * (current_price - avg_entry)
    total_return = unrealized / cost_basis * 100 if cost_basis else None
    day_pl = None
    last_equity = to_float(account.get("last_equity")) or to_float(preflight_account.get("last_equity"))
    if portfolio_value is not None and last_equity:
        day_pl = portfolio_value - last_equity
    cash_ratio = cash / portfolio_value * 100 if cash is not None and portfolio_value else None
    invested_ratio = invested / portfolio_value * 100 if invested and portfolio_value else None
    return {
        "portfolio_value": portfolio_value,
        "total_return": total_return,
        "day_pl": day_pl,
        "cash": cash,
        "buying_power": buying_power,
        "positions_count": positions_count,
        "cash_ratio": cash_ratio,
        "invested_ratio": invested_ratio,
        "positions": positions,
    }


def top_holdings_line(metrics: dict[str, Any]) -> str:
    portfolio_value = metrics.get("portfolio_value")
    positions = sorted(
        metrics.get("positions") or [],
        key=lambda row: to_float(row.get("market_value")) or 0.0,
        reverse=True,
    )
    bits = []
    for position in positions[:3]:
        symbol = position.get("symbol", "?")
        market_value = to_float(position.get("market_value")) or 0.0
        weight = market_value / portfolio_value * 100 if portfolio_value else None
        bits.append(f"{symbol} {fmt_pct_plain(weight)}")
    return "📈 Top: " + (", ".join(bits) if bits else "확인불가")


def exposure_line(metrics: dict[str, Any]) -> str:
    portfolio_value = metrics.get("portfolio_value")
    buckets: dict[str, float] = {}
    for position in metrics.get("positions") or []:
        theme = str(position.get("theme") or position.get("correlated_cluster") or "기타")
        buckets[theme] = buckets.get(theme, 0.0) + (to_float(position.get("market_value")) or 0.0)
    bits = []
    if metrics.get("cash_ratio") is not None:
        bits.append(f"현금 {fmt_pct_plain(metrics['cash_ratio'])}")
    for theme, value in sorted(buckets.items(), key=lambda item: item[1], reverse=True)[:2]:
        pct = value / portfolio_value * 100 if portfolio_value else None
        bits.append(f"{theme} {fmt_pct_plain(pct)}")
    return "📊 Exposure: " + (", ".join(bits) if bits else "확인불가")


def order_amount(order: dict[str, Any]) -> float | None:
    qty = to_float(order.get("qty"))
    price = to_float(order.get("limit_price")) or to_float(order.get("reference_price"))
    if qty is None or price is None:
        return None
    return qty * price


def order_line(order: dict[str, Any]) -> str:
    symbol = order.get("symbol", "UNKNOWN")
    amount = fmt_usd(order_amount(order))
    reason = one_line(order.get("rationale") or order.get("sizing_basis") or order.get("reason"), "검증 주문")
    return f"{symbol} | {amount} | {reason}"


def blocking_reason(manifest: dict[str, Any], fallback: str) -> str:
    for key in ("first_blocking_gate", "block_reason"):
        value = manifest.get(key)
        if value:
            return str(value)
    gates = manifest.get("gates") if isinstance(manifest.get("gates"), dict) else {}
    value = gates.get("first_blocking_gate")
    if value:
        return str(value)
    submit = manifest.get("submit_summary") if isinstance(manifest.get("submit_summary"), dict) else {}
    if submit.get("reason"):
        return str(submit["reason"])
    diagnostics = manifest.get("candidate_diagnostics") if isinstance(manifest.get("candidate_diagnostics"), list) else []
    for item in diagnostics:
        if isinstance(item, dict) and item.get("reason"):
            return str(item["reason"])
    return fallback


def alert_line(manifest: dict[str, Any], metrics: dict[str, Any]) -> str:
    alerts = []
    failures = manifest.get("mcp_failures") if isinstance(manifest.get("mcp_failures"), list) else []
    coverage = manifest.get("mcp_coverage") if isinstance(manifest.get("mcp_coverage"), list) else []
    for row in failures + coverage:
        if not isinstance(row, dict):
            continue
        outcome = str(row.get("outcome", "")).lower()
        category = row.get("gap_category")
        if outcome in {"gap", "failed", "unavailable"} or category not in {None, "", "not_applicable"}:
            server = row.get("server", "data")
            alerts.append(f"{server}:{category or outcome}")
    if metrics.get("day_pl") is None:
        alerts.append("당일손익 데이터 없음")
    deduped = list(dict.fromkeys(alerts))
    return ", ".join(deduped[:3]) if deduped else "없음"


def next_action_line(orders: list[dict[str, Any]], manifest: dict[str, Any]) -> str:
    if orders:
        return "체결 확인 후 1D/5D/20D 회고 대기"
    reason = blocking_reason(manifest, "")
    lower = reason.lower()
    if "fresh_quote" in lower or "quote" in lower:
        return "fresh quote 확보 후 재평가"
    if "budget" in lower or "cap" in lower:
        return "주문 budget reset 후 재평가"
    if "market" in lower:
        return "다음 정규장 open 후 재평가"
    return "신규 buy와 risk-trim trigger 계속 감시"


def normalize_risk_check_result(manifest: dict[str, Any]) -> dict[str, Any]:
    risk = manifest.get("risk_check_result", {})
    if isinstance(risk, dict):
        return risk
    if isinstance(risk, str):
        return {"status": risk.upper(), "warnings": []}
    return {"status": "unknown", "warnings": []}


def build_completed_message(root: Path, run_id: str, session: str) -> str:
    return build_stock_train_message(root, run_id, session, "completed", "")


def build_stock_train_message(root: Path, run_id: str, session: str, status: str, reason: str) -> str:
    report_path = root / "wiki" / "current-runs" / "daily" / f"{run_id}.md"
    order_plan_path = root / "wiki" / "trade-ledger" / "orders" / f"{run_id}.json"
    manifest_path = root / "wiki" / "evidence-store" / "run-manifests" / f"{run_id}.json"
    report = report_path.read_text(encoding="utf-8") if report_path.exists() else ""
    order_plan = load_json(order_plan_path)
    manifest = load_json(manifest_path)
    metrics = portfolio_metrics(root, run_id, order_plan)
    orders = order_plan.get("orders") or []
    orders = [order for order in orders if isinstance(order, dict)]
    buys = [order for order in orders if str(order.get("side", "")).lower() == "buy"]
    sells = [order for order in orders if str(order.get("side", "")).lower() == "sell"]
    block = blocking_reason(manifest, reason or "조건 미충족")
    day_pl_text = "확인불가"
    if metrics.get("day_pl") is not None:
        portfolio_value = metrics.get("portfolio_value")
        day_pct = metrics["day_pl"] / portfolio_value * 100 if portfolio_value else None
        day_pl_text = f"{fmt_usd(metrics['day_pl'])} ({fmt_pct(day_pct)})"
    status_note = {
        "completed": "완료",
        "started": "시작",
        "skipped": "스킵",
        "failed": "실패",
    }.get(status, status)
    if status in {"failed", "skipped"} and reason:
        manifest = {**manifest, "runtime_reason": reason}
    summary = summary_line(status_note, buys, sells, block, session)
    alerts = alert_line(manifest, metrics)
    if status in {"failed", "skipped"} and reason:
        alerts = f"{reason}, {alerts}" if alerts != "없음" else reason
    lines = [
        f"[STOCK-TRAIN] {run_time_label(run_id)} | {session} {status_note}",
        "💰 Portfolio",
        f"총자산: {fmt_usd(metrics.get('portfolio_value'))} | 총수익률: {fmt_pct(metrics.get('total_return'))} | 당일손익: {day_pl_text}",
        f"현금: {fmt_usd(metrics.get('cash'))} | 투자가능금액: {fmt_usd(metrics.get('buying_power'))} | 보유종목: {metrics.get('positions_count') or '확인불가'}개",
        top_holdings_line(metrics),
        exposure_line(metrics),
        f"🟢 Buy ({len(buys)})",
    ]
    if buys:
        lines.extend(order_line(order) for order in buys[:2])
        if len(buys) > 2:
            lines.append(f"외 {len(buys) - 2}건")
    else:
        lines.append(f"신규 진입 조건 미충족: {one_line(block)}")
    lines.append(f"🔴 Sell ({len(sells)})")
    if sells:
        lines.extend(order_line(order) for order in sells[:2])
        if len(sells) > 2:
            lines.append(f"외 {len(sells) - 2}건")
    else:
        lines.append("청산 조건 미충족")
    lines.extend(
        [
            "📊 Summary",
            summary,
            "⚠️ Alerts",
            alerts,
            "🎯 Next Action",
            next_action_line(orders, manifest),
        ]
    )
    return "\n".join(lines[:20])


def summary_line(status_note: str, buys: list[dict[str, Any]], sells: list[dict[str, Any]], block: str, session: str) -> str:
    if buys or sells:
        parts = []
        if buys:
            parts.append(f"매수 {len(buys)}건")
        if sells:
            parts.append(f"매도 {len(sells)}건")
        if not sells:
            parts.append("매도 trigger 없음")
        return f"{', '.join(parts)}; {session} 검증 운용"
    if status_note == "실패":
        return "실행 실패, 주문 없음"
    if status_note == "스킵":
        return "실행 조건 미충족, 주문 없음"
    return f"현금 유지, 신규 주문 보류: {one_line(block)}"


def build_message(args: argparse.Namespace) -> str:
    session = args.session
    run_id = args.run_id
    return build_stock_train_message(args.root, run_id, session, args.status, args.reason)


def send_message(message: str, args: argparse.Namespace) -> int:
    target = args.target or os.environ.get("OPENCLAW_AUTOPILOT_NOTIFY_TARGET") or os.environ.get("OPENCLAW_NOTIFY_TARGET")
    if not target:
        print("OpenClaw notify target is unset; skipping message send.", file=sys.stderr)
        return 0

    channel = args.channel or os.environ.get("OPENCLAW_AUTOPILOT_NOTIFY_CHANNEL") or "telegram"
    account = args.account or os.environ.get("OPENCLAW_AUTOPILOT_NOTIFY_ACCOUNT")
    openclaw_bin = os.environ.get("OPENCLAW_BIN", "openclaw")
    command = [
        openclaw_bin,
        "message",
        "send",
        "--channel",
        channel,
        "--target",
        target,
        "--message",
        message,
    ]
    if account:
        command.extend(["--account", account])
    if args.dry_run:
        command.append("--dry-run")

    completed = subprocess.run(command, text=True, capture_output=True, check=False)
    if completed.stdout:
        print(completed.stdout.strip())
    if completed.stderr:
        print(completed.stderr.strip(), file=sys.stderr)
    return completed.returncode


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Send a concise OpenClaw messenger update for an autopilot run.")
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--session", default="after_hours")
    parser.add_argument("--status", choices=["started", "completed", "skipped", "failed"], required=True)
    parser.add_argument("--reason", default="")
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--channel", default="")
    parser.add_argument("--target", default="")
    parser.add_argument("--account", default="")
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    args.root = args.root.resolve()
    message = build_message(args)
    print(message)
    return send_message(message, args)


if __name__ == "__main__":
    raise SystemExit(main())
