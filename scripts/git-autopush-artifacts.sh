#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RUN_KIND="${1:-scheduled-run}"

cd "${ROOT_DIR}"

now_iso() {
  date '+%Y-%m-%dT%H:%M:%S%z'
}

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "$(now_iso) git autopush skipped: not a git work tree"
  exit 0
fi

if ! git diff --quiet -- .gitignore 2>/dev/null; then
  echo "$(now_iso) git autopush warning: .gitignore has local changes; leaving unstaged"
fi

TRACKABLE_PATHS=()
for path in \
  wiki/index.md \
  wiki/log.md \
  wiki/current-runs \
  wiki/evidence-store \
  wiki/research-notes \
  wiki/trade-ledger \
  wiki/policy-book \
  wiki/backtest-runs \
  harness/recommendation-policy.yaml \
  harness/strategies
do
  if [[ -e "${path}" ]]; then
    TRACKABLE_PATHS+=("${path}")
  fi
done

if [[ "${#TRACKABLE_PATHS[@]}" -eq 0 ]]; then
  echo "$(now_iso) git autopush skipped: no artifact paths exist"
  exit 0
fi

git add -- "${TRACKABLE_PATHS[@]}"

if git diff --cached --quiet; then
  echo "$(now_iso) git autopush skipped: no scheduled artifact changes"
  exit 0
fi

timestamp="$(TZ=Asia/Seoul date '+%Y-%m-%d %H:%M KST')"
git commit -m "Record ${RUN_KIND} artifacts (${timestamp})"

branch="$(git branch --show-current)"
if [[ -z "${branch}" ]]; then
  echo "$(now_iso) git autopush skipped: detached HEAD"
  exit 0
fi

git push origin "${branch}"
