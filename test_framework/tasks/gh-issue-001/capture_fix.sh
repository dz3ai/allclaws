#!/usr/bin/env bash
# S1 (gh-issue-001) reference-fix pipeline:
#   complete patch -> self-verify on scratch copy (acceptance PASS + existing
#   suite PASS) -> restore pristine fixture.
set -eu
TASK=/home/dannyz/src/github/allclaws/test_framework/tasks/gh-issue-001
cd "$TASK/fixture"

# drop stale bytecode caches before diffing (never part of the fixture).
# NOTE: S1's initial commit accidentally tracked some caches — remove them
# from the INDEX one path at a time (git rm aborts ALL paths if one misses).
rm -rf tinyweb/__pycache__ tests/__pycache__ .pytest_cache acceptance_run
for p in tinyweb/__pycache__ tests/__pycache__ .pytest_cache; do
  git rm -r -q --cached "$p" 2>/dev/null || true
done

git diff > "$TASK/acceptance/reference_fix.patch"
echo "patch: $(wc -l < "$TASK/acceptance/reference_fix.patch") lines"

SCRATCH=$(mktemp -d)
git archive HEAD | tar -x -C "$SCRATCH"
cd "$SCRATCH"
git apply "$TASK/acceptance/reference_fix.patch"
mkdir -p acceptance_run && cp -r "$TASK/acceptance/tests" acceptance_run/
echo "--- acceptance on patched scratch (must PASS) ---"
/usr/bin/python3 -m pytest acceptance_run/tests -q
echo "--- existing suite on patched scratch (must PASS, incl. former bug tests) ---"
/usr/bin/python3 -m pytest tests/ -q
rm -rf "$SCRATCH"

cd "$TASK/fixture"
git checkout -- .
rm -rf acceptance_run tinyweb/__pycache__ tests/__pycache__ .pytest_cache
echo "--- pristine restored ---"
git status --short || true
