#!/usr/bin/env python3
"""Submit a validated Alpaca paper order plan through MCP.

This helper is intentionally narrow: it only submits orders from an order-plan
JSON file that already passes the local risk validator, and it uses Alpaca MCP
stdio directly. It never calls Alpaca REST endpoints.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


ROOT_DIR = Path(__file__).resolve().parents[1]
MCP_TIMEOUT_SECONDS = 35
EXIT_VALIDATION_FAILED = 64
EXIT_MCP_FAILED = 70


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def read_env(root: Path = ROOT_DIR) -> dict[str, str]:
    env = os.environ.copy()
    env_file = root / ".env"
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            if not stripped or stripped.startswith("#") or "=" not in stripped:
                continue
            key, value = stripped.split("=", 1)
            env.setdefault(key.strip(), value.strip().strip('"').strip("'"))
    return env


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Submit a validated scheduled autopilot paper order plan.")
    parser.add_argument("--order-plan", type=Path, required=True)
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--run-id", default="")
    parser.add_argument("--timeout", type=int, default=MCP_TIMEOUT_SECONDS)
    parser.add_argument(
        "--max-plan-age-minutes",
        type=float,
        default=20.0,
        help="Reject submit if plan created_at/data_cutoff_time is older than this; use 0 to disable.",
    )
    parser.add_argument("--execute", action="store_true", help="Actually submit eligible paper orders.")
    return parser.parse_args()


def classify_error(exc: BaseException) -> str:
    text = str(exc).lower()
    if "cancelled" in text or "canceled" in text or "user cancelled" in text:
        return "cancelled"
    if "could not resolve host" in text or "nodename nor servname" in text or "name resolution" in text:
        return "dns"
    if "unauthorized" in text or "forbidden" in text or "api_key" in text or "secret" in text:
        return "auth"
    if "timed out" in text or "timeout" in text:
        return "timeout"
    if "iserror" in text or "api request failed" in text or "request error" in text:
        return "provider_error"
    return "unknown"


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return payload


def parse_datetime(value: Any) -> datetime | None:
    if not isinstance(value, str) or not value.strip():
        return None
    raw = value.strip()
    normalized = raw[:-1] + "+00:00" if raw.endswith("Z") else raw
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def parse_tool_payload(result: Any, *, allow_text: bool = False) -> dict[str, Any] | list[Any]:
    if bool(getattr(result, "isError", False)):
        for item in getattr(result, "content", []):
            text = getattr(item, "text", None)
            if text:
                raise RuntimeError(str(text)[:500])
        raise RuntimeError("MCP tool returned isError=true")

    text_errors: list[str] = []
    for item in getattr(result, "content", []):
        text = getattr(item, "text", None)
        if not text:
            continue
        try:
            payload = json.loads(text)
        except json.JSONDecodeError:
            text_errors.append(str(text)[:500])
            continue
        if isinstance(payload, (dict, list)):
            if isinstance(payload, dict) and payload.get("error"):
                raise RuntimeError(str(payload["error"])[:500])
            return payload
    if text_errors:
        if allow_text:
            return {"text": text_errors[0]}
        raise RuntimeError(text_errors[0])
    if allow_text:
        return {}
    raise RuntimeError("Could not parse MCP tool response as JSON")


async def call_tool(
    session: ClientSession,
    name: str,
    arguments: dict[str, Any] | None = None,
    *,
    timeout: int,
    allow_text: bool = False,
) -> dict[str, Any]:
    checked_at = now_utc()
    try:
        result = await asyncio.wait_for(session.call_tool(name, arguments or {}), timeout=timeout)
        payload = parse_tool_payload(result, allow_text=allow_text)
    except Exception as exc:  # noqa: BLE001 - scheduler report should classify all gaps.
        return {
            "tool": name,
            "outcome": "failed",
            "checked_at": checked_at,
            "gap_category": classify_error(exc),
            "gap_reason": str(exc)[:500],
        }
    return {
        "tool": name,
        "outcome": "pass",
        "checked_at": checked_at,
        "gap_category": "not_applicable",
        "gap_reason": "",
        "payload": payload,
    }


def normalize_clock(payload: Any) -> dict[str, Any]:
    data = payload if isinstance(payload, dict) else {}
    clock = data.get("clock") if isinstance(data.get("clock"), dict) else data
    is_open = clock.get("is_open")
    if is_open is None:
        is_open = clock.get("isOpen")
    return {
        "is_open": bool(is_open),
        "timestamp": clock.get("timestamp") or clock.get("time"),
        "next_open": clock.get("next_open") or clock.get("nextOpen"),
        "next_close": clock.get("next_close") or clock.get("nextClose"),
    }


def extract_order_id(payload: Any) -> str:
    if not isinstance(payload, dict):
        return ""
    for key in ("id", "order_id"):
        value = payload.get(key)
        if value:
            return str(value)
    for key in ("result", "order"):
        value = payload.get(key)
        if isinstance(value, dict):
            order_id = extract_order_id(value)
            if order_id:
                return order_id
    return ""


def order_request_from_plan_order(order: dict[str, Any]) -> dict[str, Any]:
    return {
        "symbol": str(order["symbol"]).upper(),
        "side": str(order["side"]).lower(),
        "qty": str(order["qty"]),
        "type": str(order["order_type"]).lower(),
        "time_in_force": str(order["time_in_force"]).lower(),
        "limit_price": str(order["limit_price"]),
        "extended_hours": bool(order.get("extended_hours", False)),
        "client_order_id": str(order["client_order_id"]),
    }


def run_risk_validator(order_plan_path: Path) -> dict[str, Any]:
    completed = subprocess.run(
        [
            sys.executable,
            str(ROOT_DIR / "scripts" / "check-risk-policy.py"),
            "--json",
            str(order_plan_path),
        ],
        cwd=ROOT_DIR,
        text=True,
        capture_output=True,
        check=False,
    )
    try:
        payload = json.loads(completed.stdout or "{}")
    except json.JSONDecodeError:
        payload = {"raw_stdout": completed.stdout}
    payload["returncode"] = completed.returncode
    if completed.stderr:
        payload["stderr"] = completed.stderr[-1000:]
    return payload


def validate_static_guards(plan: dict[str, Any], env: dict[str, str], *, max_plan_age_minutes: float) -> list[str]:
    errors: list[str] = []
    if env.get("ALPACA_PAPER_TRADE") != "true":
        errors.append("ALPACA_PAPER_TRADE=true is required")
    if plan.get("paper") is not True:
        errors.append("order plan must set paper=true")
    if str(plan.get("mode") or "").lower() != "submit":
        errors.append("order plan mode must be submit")
    plan_timestamp = parse_datetime(plan.get("created_at")) or parse_datetime(plan.get("data_cutoff_time"))
    if max_plan_age_minutes > 0:
        if plan_timestamp is None:
            errors.append("order plan must include created_at or data_cutoff_time for freshness guard")
        else:
            plan_age_minutes = (datetime.now(timezone.utc) - plan_timestamp).total_seconds() / 60.0
            if plan_age_minutes > max_plan_age_minutes:
                errors.append(
                    f"order plan age {plan_age_minutes:.1f} minutes exceeds freshness limit "
                    f"{max_plan_age_minutes:.1f}"
                )
    orders = plan.get("orders", [])
    if not isinstance(orders, list):
        errors.append("orders must be an array")
        return errors
    for index, order in enumerate(orders):
        if not isinstance(order, dict):
            errors.append(f"orders[{index}] must be an object")
            continue
        if not str(order.get("client_order_id") or "").strip():
            errors.append(f"orders[{index}] missing client_order_id")
        if str(order.get("order_type") or "").lower() != "limit":
            errors.append(f"orders[{index}] must be a limit order")
        if str(order.get("time_in_force") or "").lower() != "day":
            errors.append(f"orders[{index}] must use time_in_force=day")
        if str(order.get("side") or "").lower() not in {"buy", "sell"}:
            errors.append(f"orders[{index}] side must be buy or sell")
    return errors


def write_output(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")


async def submit_orders(args: argparse.Namespace) -> tuple[int, dict[str, Any]]:
    env = read_env()
    plan = load_json(args.order_plan)
    run_id = args.run_id or str(plan.get("run_id") or args.order_plan.stem)
    raw_orders = plan.get("orders", [])
    orders = raw_orders if isinstance(raw_orders, list) else []
    output: dict[str, Any] = {
        "run_id": run_id,
        "created_at": now_utc(),
        "paper": True,
        "alpaca_mcp_only": True,
        "execute": bool(args.execute),
        "order_plan_path": str(args.order_plan),
        "status": "dry_run" if not args.execute else "failed",
        "gap_category": "not_applicable",
        "gap_reason": "",
        "risk_validator": {},
        "clock": {},
        "orders": [],
        "post_reconcile": {},
    }

    guard_errors = validate_static_guards(plan, env, max_plan_age_minutes=args.max_plan_age_minutes)
    if guard_errors:
        output["status"] = "failed"
        output["gap_category"] = "static_guard_failed"
        output["gap_reason"] = "; ".join(guard_errors)
        return EXIT_VALIDATION_FAILED, output

    validator = run_risk_validator(args.order_plan)
    output["risk_validator"] = validator
    validator_passed = validator.get("ok") is True or str(validator.get("status") or "").upper() == "PASS"
    if validator.get("returncode") != 0 or not validator_passed:
        output["status"] = "failed"
        output["gap_category"] = "risk_validator_failed"
        output["gap_reason"] = json.dumps(validator.get("errors") or validator, ensure_ascii=False)[:500]
        return EXIT_VALIDATION_FAILED, output

    if not orders:
        output["status"] = "no_orders"
        output["gap_reason"] = "validated order plan contains no orders"
        return 0, output

    server = StdioServerParameters(
        command=str(ROOT_DIR / "scripts" / "alpaca-mcp.sh"),
        args=[],
        env=env,
        cwd=str(ROOT_DIR),
    )

    try:
        with open(os.devnull, "w", encoding="utf-8") as errlog:
            async with stdio_client(server, errlog=errlog) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    clock_row = await call_tool(session, "get_clock", timeout=args.timeout)
                    output["clock"] = clock_row
                    if clock_row["outcome"] != "pass":
                        raise RuntimeError(clock_row.get("gap_reason") or "get_clock failed")
                    clock = normalize_clock(clock_row.get("payload"))
                    market = plan.get("market", {}) if isinstance(plan.get("market"), dict) else {}
                    market_session = str(market.get("session") or "regular").lower()
                    if market_session == "regular" and not clock["is_open"]:
                        raise RuntimeError("regular-session order plan cannot submit while Alpaca market clock is closed")
                    if market_session == "after_hours" and clock["is_open"]:
                        raise RuntimeError("after-hours order plan cannot submit while Alpaca regular market clock is open")

                    for order in orders:
                        request = order_request_from_plan_order(order)
                        row: dict[str, Any] = {
                            "symbol": request["symbol"],
                            "side": request["side"],
                            "client_order_id": request["client_order_id"],
                            "order_request": request,
                            "existing_order": {},
                            "submit": {},
                            "reconcile": {},
                            "status": "dry_run" if not args.execute else "pending",
                        }
                        existing = await call_tool(
                            session,
                            "get_order_by_client_id",
                            {"client_order_id": request["client_order_id"]},
                            timeout=args.timeout,
                        )
                        row["existing_order"] = existing
                        if existing["outcome"] == "pass" and extract_order_id(existing.get("payload")):
                            row["status"] = "already_exists"
                            output["orders"].append(row)
                            continue
                        if not args.execute:
                            output["orders"].append(row)
                            continue

                        submit = await call_tool(session, "place_stock_order", request, timeout=args.timeout)
                        row["submit"] = submit
                        if submit["outcome"] != "pass":
                            row["status"] = "submit_failed"
                            output["orders"].append(row)
                            raise RuntimeError(submit.get("gap_reason") or "place_stock_order failed")

                        reconcile = await call_tool(
                            session,
                            "get_order_by_client_id",
                            {"client_order_id": request["client_order_id"]},
                            timeout=args.timeout,
                        )
                        row["reconcile"] = reconcile
                        if reconcile["outcome"] != "pass" or not extract_order_id(reconcile.get("payload")):
                            row["status"] = "reconcile_failed"
                            output["orders"].append(row)
                            raise RuntimeError(reconcile.get("gap_reason") or "post-submit reconcile failed")
                        row["status"] = "submitted"
                        output["orders"].append(row)

                    output["post_reconcile"]["account"] = await call_tool(
                        session, "get_account_info", timeout=args.timeout
                    )
                    output["post_reconcile"]["positions"] = await call_tool(
                        session, "get_all_positions", timeout=args.timeout
                    )
                    output["post_reconcile"]["open_orders"] = await call_tool(
                        session, "get_orders", {"status": "open", "limit": 100}, timeout=args.timeout
                    )
                    statuses = {str(row.get("status")) for row in output["orders"]}
                    if "submitted" in statuses:
                        output["status"] = "submitted"
                    elif "already_exists" in statuses:
                        output["status"] = "already_exists"
                    elif args.execute:
                        output["status"] = "no_new_submit"
                    else:
                        output["status"] = "dry_run"
    except Exception as exc:  # noqa: BLE001 - runtime report must explain failure.
        output["status"] = "failed"
        output["gap_category"] = classify_error(exc)
        output["gap_reason"] = str(exc)[:500]
        return EXIT_MCP_FAILED, output

    return 0, output


def main() -> None:
    args = parse_args()
    code, output = asyncio.run(submit_orders(args))
    write_output(args.output_json, output)
    print(
        json.dumps(
            {
                "run_id": output["run_id"],
                "status": output["status"],
                "orders": [
                    {
                        "symbol": row.get("symbol"),
                        "side": row.get("side"),
                        "client_order_id": row.get("client_order_id"),
                        "status": row.get("status"),
                    }
                    for row in output.get("orders", [])
                ],
                "output_json": str(args.output_json),
                "gap_category": output.get("gap_category"),
                "gap_reason": output.get("gap_reason"),
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    raise SystemExit(code)


if __name__ == "__main__":
    main()
