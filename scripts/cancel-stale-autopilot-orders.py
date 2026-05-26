#!/usr/bin/env python3
"""Cancel stale unfilled paper autopilot orders through Alpaca MCP.

This helper is intentionally narrow. It only cancels open, unfilled, day limit
US-equity orders whose client_order_id starts with the scheduled autopilot
prefix. It never calls Alpaca REST directly and it never touches live trading.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


ROOT_DIR = Path(__file__).resolve().parents[1]
DEFAULT_POLICY_PATH = ROOT_DIR / "harness" / "risk-policy.yaml"
EXIT_MCP_UNAVAILABLE = 70
MCP_TIMEOUT_SECONDS = 35
AUTOPILOT_CLIENT_PREFIX = "hourly-"


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


def load_lifecycle_policy(path: Path = DEFAULT_POLICY_PATH) -> dict[str, Any]:
    try:
        import yaml

        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        lifecycle = data.get("order_lifecycle", {})
        if isinstance(lifecycle, dict):
            return lifecycle
    except Exception:
        pass
    return {
        "max_open_order_age_minutes": 30,
        "cancel_stale_unfilled_orders": True,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Cancel stale scheduled autopilot paper orders.")
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--policy", type=Path, default=DEFAULT_POLICY_PATH)
    parser.add_argument("--timeout", type=int, default=MCP_TIMEOUT_SECONDS)
    parser.add_argument("--client-prefix", default=AUTOPILOT_CLIENT_PREFIX)
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def parse_dt(value: Any) -> datetime | None:
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
    except Exception as exc:  # noqa: BLE001 - scheduler guard should classify failure.
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


def extract_result_list(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, dict) and isinstance(payload.get("result"), list):
        return [item for item in payload["result"] if isinstance(item, dict)]
    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, dict)]
    return []


def order_age_minutes(order: dict[str, Any], now: datetime) -> float | None:
    submitted = parse_dt(order.get("submitted_at") or order.get("created_at"))
    if not submitted:
        return None
    return (now - submitted).total_seconds() / 60.0


def is_unfilled_day_limit_equity(order: dict[str, Any]) -> bool:
    status = str(order.get("status") or "").lower()
    if status not in {"new", "accepted", "pending_new", "held"}:
        return False
    if str(order.get("asset_class") or "").lower() not in {"us_equity", ""}:
        return False
    if str(order.get("type") or order.get("order_type") or "").lower() != "limit":
        return False
    if str(order.get("time_in_force") or "").lower() != "day":
        return False
    try:
        filled_qty = float(order.get("filled_qty") or 0)
    except (TypeError, ValueError):
        return False
    return filled_qty == 0


def stale_autopilot_orders(
    orders: list[dict[str, Any]],
    *,
    now: datetime,
    max_age_minutes: float,
    client_prefix: str = AUTOPILOT_CLIENT_PREFIX,
) -> list[dict[str, Any]]:
    stale: list[dict[str, Any]] = []
    for order in orders:
        client_order_id = str(order.get("client_order_id") or "")
        if not client_order_id.startswith(client_prefix):
            continue
        if not is_unfilled_day_limit_equity(order):
            continue
        age = order_age_minutes(order, now)
        if age is None or age <= max_age_minutes:
            continue
        stale.append(
            {
                "id": order.get("id"),
                "client_order_id": client_order_id,
                "symbol": order.get("symbol"),
                "side": order.get("side"),
                "status": order.get("status"),
                "submitted_at": order.get("submitted_at") or order.get("created_at"),
                "age_minutes": round(age, 2),
            }
        )
    return stale


def normalize_clock(row: dict[str, Any]) -> dict[str, Any]:
    payload = row.get("payload")
    if not isinstance(payload, dict):
        return {"is_open": False}
    clock = payload.get("clock") if isinstance(payload.get("clock"), dict) else payload
    is_open = clock.get("is_open")
    if is_open is None:
        is_open = clock.get("isOpen")
    return {
        "is_open": bool(is_open),
        "timestamp": clock.get("timestamp") or clock.get("time"),
        "next_open": clock.get("next_open") or clock.get("nextOpen"),
        "next_close": clock.get("next_close") or clock.get("nextClose"),
    }


async def main_async(args: argparse.Namespace) -> int:
    env = read_env()
    if env.get("ALPACA_PAPER_TRADE") != "true":
        print("ALPACA_PAPER_TRADE=true is required.", file=sys.stderr)
        return 64

    lifecycle = load_lifecycle_policy(args.policy)
    max_age = float(lifecycle.get("max_open_order_age_minutes", 30))
    cancel_enabled = bool(lifecycle.get("cancel_stale_unfilled_orders", True))

    server = StdioServerParameters(
        command=str(ROOT_DIR / "scripts" / "alpaca-mcp.sh"),
        args=[],
        env=env,
        cwd=str(ROOT_DIR),
    )

    created_at = now_utc()
    output: dict[str, Any] = {
        "run_id": args.run_id,
        "created_at": created_at,
        "paper": True,
        "source": "scheduler Alpaca MCP stale autopilot order cleanup",
        "alpaca_mcp_only": True,
        "dry_run": args.dry_run,
        "policy": {
            "max_open_order_age_minutes": max_age,
            "cancel_stale_unfilled_orders": cancel_enabled,
            "client_order_id_prefix": args.client_prefix,
        },
        "clock": {},
        "initial_open_orders": [],
        "stale_candidates": [],
        "cancel_attempts": [],
        "remaining_open_orders": [],
        "status": "pass",
        "gap_category": "not_applicable",
        "gap_reason": "",
    }

    try:
        with open(os.devnull, "w", encoding="utf-8") as errlog:
            async with stdio_client(server, errlog=errlog) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    clock_row = await call_tool(session, "get_clock", timeout=args.timeout)
                    output["clock"] = normalize_clock(clock_row)
                    orders_row = await call_tool(
                        session,
                        "get_orders",
                        {"status": "open", "limit": 100, "direction": "desc"},
                        timeout=args.timeout,
                    )
                    if orders_row["outcome"] != "pass":
                        raise RuntimeError(orders_row.get("gap_reason") or "get_orders failed")
                    open_orders = extract_result_list(orders_row.get("payload"))
                    output["initial_open_orders"] = open_orders
                    now_value = parse_dt(output["clock"].get("timestamp")) or datetime.now(timezone.utc)
                    stale = stale_autopilot_orders(
                        open_orders,
                        now=now_value,
                        max_age_minutes=max_age,
                        client_prefix=args.client_prefix,
                    )
                    output["stale_candidates"] = stale

                    if cancel_enabled and not args.dry_run:
                        for order in stale:
                            order_id = str(order.get("id") or "").strip()
                            if not order_id:
                                output["cancel_attempts"].append(
                                    {
                                        "order": order,
                                        "outcome": "failed",
                                        "gap_category": "empty_response",
                                        "gap_reason": "stale order did not include order id",
                                    }
                                )
                                continue
                            cancel_row = await call_tool(
                                session,
                                "cancel_order_by_id",
                                {"order_id": order_id},
                                timeout=args.timeout,
                                allow_text=True,
                            )
                            output["cancel_attempts"].append(
                                {
                                    "order": order,
                                    "outcome": cancel_row["outcome"],
                                    "gap_category": cancel_row.get("gap_category", "unknown"),
                                    "gap_reason": cancel_row.get("gap_reason", ""),
                                    "checked_at": cancel_row.get("checked_at"),
                                }
                            )

                    final_orders_row = await call_tool(
                        session,
                        "get_orders",
                        {"status": "open", "limit": 100, "direction": "desc"},
                        timeout=args.timeout,
                    )
                    if final_orders_row["outcome"] == "pass":
                        output["remaining_open_orders"] = extract_result_list(final_orders_row.get("payload"))
                    else:
                        output["status"] = "failed"
                        output["gap_category"] = final_orders_row.get("gap_category", "unknown")
                        output["gap_reason"] = final_orders_row.get("gap_reason", "post-cancel get_orders failed")
    except Exception as exc:  # noqa: BLE001 - record and fail closed.
        output["status"] = "failed"
        output["gap_category"] = classify_error(exc)
        output["gap_reason"] = str(exc)[:500]

    failed_cancels = [row for row in output["cancel_attempts"] if row.get("outcome") != "pass"]
    if failed_cancels:
        output["status"] = "failed"
        output["gap_category"] = failed_cancels[0].get("gap_category", "unknown")
        output["gap_reason"] = failed_cancels[0].get("gap_reason", "failed to cancel stale autopilot order")

    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(output, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(
        json.dumps(
            {
                "run_id": args.run_id,
                "status": output["status"],
                "stale_candidates": len(output["stale_candidates"]),
                "cancel_attempts": len(output["cancel_attempts"]),
                "remaining_open_orders": len(output["remaining_open_orders"]),
            },
            ensure_ascii=False,
        )
    )
    return 0 if output["status"] == "pass" else EXIT_MCP_UNAVAILABLE


def main() -> None:
    raise SystemExit(asyncio.run(main_async(parse_args())))


if __name__ == "__main__":
    main()
