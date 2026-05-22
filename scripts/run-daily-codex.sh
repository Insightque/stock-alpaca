#!/usr/bin/env bash
set -euo pipefail

export PATH="/opt/homebrew/bin:/usr/local/bin:/Library/Frameworks/Python.framework/Versions/3.11/bin:${PATH}"

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PROMPT_FILE="${ROOT_DIR}/harness/workflows/daily.md"

cd "${ROOT_DIR}"

exec codex --search exec -C "${ROOT_DIR}" --skip-git-repo-check - < "${PROMPT_FILE}"
