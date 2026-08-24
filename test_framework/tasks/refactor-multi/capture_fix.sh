#!/usr/bin/env bash
# S2 reference-fix pipeline:
#   1. keep human-readable copies of the two NEW modules under acceptance/reference/
#   2. generate a COMPLETE patch (intent-to-add so new files are included)
#   3. SELF-VERIFY the patch on a scratch copy of the pristine tree:
#        apply patch -> acceptance PASS + existing suite PASS
#   4. restore the fixture to pristine state
set -eu
TASK=/home/dannyz/src/github/allclaws/test_framework/tasks/refactor-multi
cd "$TASK"

mkdir -p acceptance/reference
cp fixture/invcalc/engine.py acceptance/reference/engine.py
cp fixture/invcalc/compat.py acceptance/reference/compat.py

cd fixture
git add -N invcalc/engine.py invcalc/compat.py
git diff > "$TASK/acceptance/reference_fix.patch"
git reset -q

echo "patch: $(wc -l < "$TASK/acceptance/reference_fix.patch") lines, $(grep -c '^+++ b/' "$TASK/acceptance/reference_fix.patch") files"

# ---- self-verify on a scratch copy --------------------------------------
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

# ---- restore pristine -----------------------------------------------------
cd "$TASK/fixture"
git checkout -- .
rm -f invcalc/engine.py invcalc/compat.py
rm -rf acceptance_run invcalc/__pycache__ tests/__pycache__ .pytest_cache
echo "--- pristine restored ---"
git status --short || true
ls invcalc/
