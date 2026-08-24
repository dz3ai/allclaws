#!/usr/bin/env bash
# Post-strip regression: after removing fixture/.git (commit form), re-verify
# task S2 end-to-end and re-run the 9-cell dry-run grid (runner now lazily
# git-inits worktree copies).
set -eu
bash /home/dannyz/src/github/allclaws/test_framework/tasks/verify_task.sh \
  /home/dannyz/src/github/allclaws/test_framework/tasks/refactor-multi

cd /home/dannyz/src/github/allclaws/test_framework
rm -rf benchmark_results/longrun   # gitignored; runner recreates
/usr/bin/python3 -m longrun.cli run \
  --drivers aider,codex,kimi_cli \
  --tasks gh-issue-001,refactor-multi,feature-crud \
  --dry-run 2>&1 | tail -2
