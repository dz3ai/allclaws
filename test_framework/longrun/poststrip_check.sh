#!/usr/bin/env bash
# Post-strip regression: after removing fixture/.git (commit form), re-verify
# task S2 end-to-end and re-run the 9-cell dry-run grid (runner now lazily
# git-inits worktree copies).
set -eu
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FRAMEWORK_DIR="$(dirname "$HERE")"
bash "$FRAMEWORK_DIR/tasks/verify_task.sh" \
  "$FRAMEWORK_DIR/tasks/refactor-multi"

cd "$FRAMEWORK_DIR"
rm -rf benchmark_results/longrun   # gitignored; runner recreates
/usr/bin/python3 -m longrun.cli run \
  --drivers aider,codex,kimi_cli \
  --tasks gh-issue-001,refactor-multi,feature-crud \
  --dry-run 2>&1 | tail -2
