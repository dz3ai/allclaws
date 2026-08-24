#!/usr/bin/env bash
# Prepare the tasks/ tree for parent-repo commit:
#   - strip fixture/.git dirs (committed fixtures are plain source trees;
#     runner.make_worktree lazily git-inits each run copy)
#   - drop test-run droppings (.verify logs, caches, acceptance_run)
set -eu
cd /home/dannyz/src/github/allclaws/test_framework/tasks

for d in gh-issue-001 refactor-multi feature-crud; do
  rm -rf "$d/fixture/.git"
  rm -f "$d/.verify_existing.log" "$d/.verify_acceptance.log"
  rm -rf "$d/fixture/acceptance_run" "$d/fixture/.pytest_cache"
  find "$d" -name '__pycache__' -type d -prune -exec rm -rf {} + 2>/dev/null || true
done

echo "--- tasks/ tree ready for commit ---"
find . -name '.git' -o -name '__pycache__' -o -name '*.log' | head
echo "done"
