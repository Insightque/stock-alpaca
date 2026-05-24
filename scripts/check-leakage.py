#!/usr/bin/env python3
"""Check historical simulation artifacts for obvious future-data leakage.

The checker is intentionally conservative and local-only. It never calls Alpaca
or web services; it scans supplied Markdown/JSON files for timestamps after the
historical as-of point and for review-only outcome fields inside simulation
artifacts.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DATE_RE = re.compile(r"\b(20\d{2}-\d{2}-\d{2})(?:[T ](\d{2}:\d{2}(?::\d{2})?(?:Z|[+-]\d{2}:\d{2})?))?\b")
ASOF_KEY_RE = re.compile(r"\b(?:historical_asof|as_of|asof|기준 시점)\s*[:=]\s*['\"]?([^'\"\n]+)")
REVIEW_ONLY_PATTERNS = [
    "post_news_1d_return",
    "post_news_5d_return",
    "later_price",
    "actual_return",
    "benchmark_relative_return",
    "future outcome",
    "later outcome",
    "이후 수익률",
    "실제 수익률",
    "사후 수익률",
]
ALLOWED_FUTURE_CONTEXT = [
    "review_horizons",
    "review horizon",
    "review_horizon",
    "회고 예정",
    "검토 예정",
    "예정일",
]


def parse_datetime(value: str) -> datetime:
    raw = value.strip().strip("'\"")
    if re.fullmatch(r"20\d{2}-\d{2}-\d{2}", raw):
        raw = f"{raw}T23:59:59Z"
    normalized = raw[:-1] + "+00:00" if raw.endswith("Z") else raw
    parsed = datetime.fromisoformat(normalized)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def iter_json_values(value: Any) -> Any:
    if isinstance(value, dict):
        for item in value.values():
            yield from iter_json_values(item)
    elif isinstance(value, list):
        for item in value:
            yield from iter_json_values(item)
    else:
        yield value


def infer_asof_from_json(value: Any) -> datetime | None:
    if isinstance(value, dict):
        for key, item in value.items():
            if key in {"historical_asof", "as_of", "asof"} and isinstance(item, str):
                return parse_datetime(item)
            found = infer_asof_from_json(item)
            if found:
                return found
    elif isinstance(value, list):
        for item in value:
            found = infer_asof_from_json(item)
            if found:
                return found
    return None


def infer_asof(path: Path, text: str) -> datetime | None:
    if path.suffix == ".json":
        try:
            parsed = json.loads(text)
        except json.JSONDecodeError:
            parsed = None
        if parsed is not None:
            found = infer_asof_from_json(parsed)
            if found:
                return found
    match = ASOF_KEY_RE.search(text)
    if match:
        candidate = match.group(1).strip()
        candidate = candidate.split()[0] if re.fullmatch(r"20\d{2}-\d{2}-\d{2}.*", candidate) else candidate
        return parse_datetime(candidate)
    return None


def line_allows_future_date(line: str) -> bool:
    lowered = line.lower()
    return any(token in lowered for token in ALLOWED_FUTURE_CONTEXT)


def check_text_dates(path: Path, text: str, asof: datetime) -> list[str]:
    errors: list[str] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        if line_allows_future_date(line):
            continue
        for match in DATE_RE.finditer(line):
            date_text = match.group(0)
            try:
                found = parse_datetime(date_text)
            except ValueError:
                continue
            if found > asof:
                errors.append(f"{path}:{line_number}: date {date_text} is after as-of {asof.isoformat()}")
    return errors


def check_review_only_fields(path: Path, text: str) -> list[str]:
    lowered = text.lower()
    errors: list[str] = []
    is_simulation = "/backtest-runs/decisions/" in str(path) or "historical-decision" in path.name
    if not is_simulation:
        return errors
    for pattern in REVIEW_ONLY_PATTERNS:
        if pattern.lower() in lowered:
            errors.append(f"{path}: review-only field or phrase appears in simulation artifact: {pattern}")
    return errors


def check_json_timestamps(path: Path, text: str, asof: datetime) -> list[str]:
    errors: list[str] = []
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        return errors

    def visit(value: Any, keys: list[str]) -> None:
        if isinstance(value, dict):
            for key, item in value.items():
                visit(item, [*keys, key])
        elif isinstance(value, list):
            for index, item in enumerate(value):
                visit(item, [*keys, str(index)])
        elif isinstance(value, str) and keys[-1:] and keys[-1] in {
            "captured_at",
            "quote_captured_at",
            "asset_checked_at",
            "market_clock_checked_at",
            "data_cutoff_time",
        }:
            try:
                found = parse_datetime(value)
            except ValueError:
                errors.append(f"{path}: {'.'.join(keys)} is not an ISO datetime")
                return
            if found > asof:
                errors.append(f"{path}: {'.'.join(keys)} {value} is after as-of {asof.isoformat()}")

    visit(parsed, [])
    return errors


def check_file(path: Path, forced_asof: datetime | None) -> tuple[list[str], datetime | None]:
    text = path.read_text(encoding="utf-8")
    asof = forced_asof or infer_asof(path, text)
    errors: list[str] = []
    if asof is None:
        return [f"{path}: could not infer historical as-of; pass --asof"], None
    errors.extend(check_text_dates(path, text, asof))
    errors.extend(check_review_only_fields(path, text))
    errors.extend(check_json_timestamps(path, text, asof))
    return errors, asof


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Check historical artifacts for future-data leakage.")
    parser.add_argument("--asof", help="historical as-of datetime, e.g. 2026-05-08T20:00:00Z")
    parser.add_argument("--json", action="store_true", help="print a machine-readable result")
    parser.add_argument("paths", nargs="+", help="Markdown or JSON files to check")
    args = parser.parse_args(argv[1:])

    forced_asof = parse_datetime(args.asof) if args.asof else None
    all_errors: list[str] = []
    checked: list[str] = []
    inferred_asofs: dict[str, str] = {}

    for raw_path in args.paths:
        path = Path(raw_path)
        errors, asof = check_file(path, forced_asof)
        checked.append(str(path))
        if asof:
            inferred_asofs[str(path)] = asof.isoformat()
        all_errors.extend(errors)

    result = {
        "status": "FAIL" if all_errors else "PASS",
        "checked": checked,
        "asofs": inferred_asofs,
        "errors": all_errors,
    }

    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(f"Leakage check: {result['status']}")
        for error in all_errors:
            print(f"- {error}")
    return 1 if all_errors else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
