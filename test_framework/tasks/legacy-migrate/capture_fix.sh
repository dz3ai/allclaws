#!/usr/bin/env bash
# S5 (legacy-migrate) reference-fix pipeline:
#   1. generate a COMPLETE patch (the full oldorm->neworm migration of
#      inventory/ vs the pristine commit)
#   2. SELF-VERIFY the patch on a scratch copy of the pristine tree:
#        apply patch -> hidden acceptance PASS (behavior + deprecated-surface
#                       scanner) + existing fixture suite PASS
#   3. restore the fixture to pristine state
# Paths derive from this script's location (no hardcoded absolute paths).
set -eu
HERE="$(cd "$(dirname "$0")" && pwd)"
TASK="$HERE"
FIXTURE="$TASK/fixture"
cd "$FIXTURE"

# drop stale bytecode caches before diffing (never part of the fixture).
# Remove from the INDEX too, one path at a time (git rm aborts ALL paths if
# one is missing) — a pristine-vs-fixed diff must never contain caches.
rm -rf oldorm/__pycache__ neworm/__pycache__ inventory/__pycache__ \
  tests/__pycache__ .pytest_cache acceptance_run
for p in oldorm/__pycache__ neworm/__pycache__ inventory/__pycache__ \
  tests/__pycache__ .pytest_cache; do
  git rm -r -q --cached "$p" 2>/dev/null || true
done

git diff > "$TASK/acceptance/reference_fix.patch"
echo "patch: $(wc -l < "$TASK/acceptance/reference_fix.patch") lines, $(grep -c '^+++ b/' "$TASK/acceptance/reference_fix.patch") files"

# ---- self-verify on a scratch copy ----------------------------------------
SCRATCH=$(mktemp -d)
git archive HEAD | tar -x -C "$SCRATCH"
cd "$SCRATCH"
git apply "$TASK/acceptance/reference_fix.patch"
mkdir -p acceptance_run
cp -r "$TASK/acceptance/tests" acceptance_run/

echo "--- acceptance on patched scratch (must PASS, incl. scanner) ---"
/usr/bin/python3 -m pytest acceptance_run/tests -q

echo "--- existing suite on patched scratch (must PASS, unchanged) ---"
/usr/bin/python3 -m pytest tests/ -q

# ---- restore pristine -------------------------------------------------------
cd "$FIXTURE"
git checkout -- .
rm -rf acceptance_run oldorm/__pycache__ neworm/__pycache__ \
  inventory/__pycache__ tests/__pycache__ .pytest_cache
rm -rf "$SCRATCH"
echo "--- pristine restored ---"
git status --short || true
