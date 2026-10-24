#!/usr/bin/env bash
# Acceptance runner: mount hidden tests into a worktree and score it.
# Usage: acceptance/run.sh <worktree-root>
set -u
WT="${1:?usage: run.sh <worktree-root>}"
HERE="$(cd "$(dirname "$0")" && pwd)"

mkdir -p "$WT/acceptance_run"
cp -r "$HERE/tests" "$WT/acceptance_run/"

cd "$WT"
if /usr/bin/python3 -m pytest acceptance_run/tests -q; then
  echo "ACCEPTANCE: PASS"
  exit 0
else
  echo "ACCEPTANCE: FAIL"
  exit 1
fi
