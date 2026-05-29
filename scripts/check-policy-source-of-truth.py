#!/usr/bin/env python3
"""Fail when active instructions duplicate numeric policy caps.

The harness has machine-readable policy files. Active Markdown instructions
must point to those files instead of carrying copied limits that can drift.
Historical wiki reports are excluded because they are factual run records.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]

DEFAULT_PATHS = [
    "AGENTS.md",
    "README.md",
    "harness/README.md",
    "harness/agent-tasking-guide.md",
    "harness/mcp-source-map.md",
    "harness/risk-policy.md",
    "harness/simple-commands.md",
    "harness/templates",
    "harness/workflows",
    "scheduler/README.md",
]

SOURCE_OF_TRUTH_PATHS = {
    "harness/risk-policy.yaml",
    "harness/recommendation-policy.yaml",
}

STRATEGY_SOURCE_DIR = "harness/strategies"

FORBIDDEN_PATTERNS = [
    re.compile(r"\b(?:80|75|70|50|45|40|35|30|25|20|15|12|10|8|7|5|3|2|1)\s*%"),
    re.compile(r"\b0\.(?:50|5)\s*%"),
    re.compile(r"\b(?:20|30|15|10|5|3|1)\s*(?:minutes?|분)\b", re.IGNORECASE),
    re.compile(r"\b(?:10|20|5|3|1)\s*(?:orders?|buys?|slots?|건|개|주)\b", re.IGNORECASE),
    re.compile(r"\b(?:10|20|5|3|1)\s+\w+\s+(?:orders?|buys?|slots?)\b", re.IGNORECASE),
    re.compile(r"\b(?:at least|minimum|min(?:imum)?|최소)\s*(?:3|5|10|20)\b", re.IGNORECASE),
    re.compile(r"\b(?:at most|up to|maximum|max(?:imum)?|최대)\s*(?:3|5|10|15|20|80)\b", re.IGNORECASE),
    re.compile(r"\bevery\s*20\s*minutes?\b", re.IGNORECASE),
    re.compile(r"\bminute-?31\b", re.IGNORECASE),
    re.compile(r"\b22:31\b"),
    re.compile(r"\b0\.5\b"),
    re.compile(r"\$5\b"),
    re.compile(r"\b50,000,000\b"),
]

ALLOWED_LINE_PATTERNS = [
    re.compile(r"^\s*#"),
    re.compile(r"source of truth", re.IGNORECASE),
    re.compile(r"defined (?:only )?in `?harness/(?:risk-policy|recommendation-policy)\.yaml`?", re.IGNORECASE),
    re.compile(r"from `?harness/(?:risk-policy|recommendation-policy)\.yaml`?", re.IGNORECASE),
    re.compile(r"`harness/strategies/[^`]+\.yaml`"),
    re.compile(r"\b1D/5D/20D\b"),
]


def iter_files(paths: list[str]) -> list[Path]:
    files: list[Path] = []
    for raw in paths:
        path = (ROOT_DIR / raw).resolve()
        if not path.exists():
            continue
        if path.is_dir():
            files.extend(sorted(item for item in path.rglob("*.md") if item.is_file()))
        elif path.is_file():
            files.append(path)
    return files


def is_exempt(path: Path) -> bool:
    rel = path.relative_to(ROOT_DIR).as_posix()
    return rel in SOURCE_OF_TRUTH_PATHS or rel.startswith(f"{STRATEGY_SOURCE_DIR}/")


def line_allowed(line: str) -> bool:
    return any(pattern.search(line) for pattern in ALLOWED_LINE_PATTERNS)


def check_file(path: Path) -> list[str]:
    if is_exempt(path):
        return []
    findings: list[str] = []
    for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if line_allowed(line):
            continue
        for pattern in FORBIDDEN_PATTERNS:
            if pattern.search(line):
                rel = path.relative_to(ROOT_DIR).as_posix()
                findings.append(f"{rel}:{lineno}: hardcoded policy-like numeric value: {line.strip()}")
                break
    return findings


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="*", help="Optional files/directories to scan relative to repo root.")
    args = parser.parse_args()

    paths = args.paths or DEFAULT_PATHS
    findings: list[str] = []
    for path in iter_files(paths):
        findings.extend(check_file(path))

    if findings:
        print("Policy source-of-truth check failed:")
        for finding in findings:
            print(f"- {finding}")
        print("\nMove active numeric caps/thresholds into the relevant YAML source of truth.")
        return 1

    print("Policy source-of-truth check PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
