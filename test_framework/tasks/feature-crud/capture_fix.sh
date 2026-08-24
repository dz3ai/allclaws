#!/usr/bin/env bash
# S3 (feature-crud) reference-fix pipeline:
#   complete patch -> self-verify on scratch copy (acceptance PASS + existing
#   suite PASS) -> restore pristine fixture.
set -eu
TASK=/home/dannyz/src/github/allclaws/test_framework/tasks/feature-crud
cd "$TASK/fixture"

# drop stale bytecode caches before diffing (never part of the fixture)
rm -rf taskboard/__pycache__ tests/__pycache__ .pytest_cache acceptance_run
git rm -r -q --cached taskboard/__pycache__ tests/__pycache__ .pytest_cache 2>/dev/null || true

git diff > "$TASK/acceptance/reference_fix.patch"
echo "patch: $(wc -l < "$TASK/acceptance/reference_fix.patch") lines"

SCRATCH=$(mktemp -d)
git archive HEAD | tar -x -C "$SCRATCH"
cd "$SCRATCH"
git apply "$TASK/acceptance/reference_fix.patch"
mkdir -p acceptance_run && cp -r "$TASK/acceptance/tests" acceptance_run/
echo "--- acceptance on patched scratch (must PASS) ---"
/usr/bin/python3 -m pytest acceptance_run/tests -q
echo "--- existing suite on patched scratch (must PASS) ---"
/usr/bin/python3 -m pytest tests/ -q
rm -rf "$SCRATCH"

cd "$TASK/fixture"
git checkout -- .
rm -rf acceptance_run taskboard/__pycache__ tests/__pycache__ .pytest_cache
echo "--- pristine restored ---"
git status --short || true
