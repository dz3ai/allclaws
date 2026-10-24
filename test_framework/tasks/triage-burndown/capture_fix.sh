#!/usr/bin/env bash
# S4 (triage-burndown) reference-fix pipeline:
#   1. generate a COMPLETE patch (all 5 bug fixes vs the pristine commit)
#   2. SELF-VERIFY the patch on a scratch copy of the pristine tree:
#        apply patch -> acceptance PASS (incl. check_windows all-solved)
#                       + existing suite PASS (former bug tests now green)
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
rm -rf metricslite/__pycache__ tests/__pycache__ .pytest_cache acceptance_run
for p in metricslite/__pycache__ tests/__pycache__ .pytest_cache; do
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
cp "$TASK/acceptance/check_windows.py" acceptance_run/

echo "--- acceptance on patched scratch (must PASS) ---"
/usr/bin/python3 -m pytest acceptance_run/tests -q

echo "--- check_windows on patched scratch (all 5 windows must be solved) ---"
/usr/bin/python3 - <<'PYEOF'
import json
import subprocess
import sys

proc = subprocess.run(
    [sys.executable, "acceptance_run/check_windows.py"],
    capture_output=True, text=True, timeout=120,
)
line = proc.stdout.strip().splitlines()[-1]
data = json.loads(line)
assert list(data) == ["windows"], data
assert [w["window"] for w in data["windows"]] == [1, 2, 3, 4, 5], data
assert all(w["solved"] is True for w in data["windows"]), data
print("check_windows: all 5 windows solved —", line)
PYEOF

echo "--- existing suite on patched scratch (must PASS, incl. former bug tests) ---"
/usr/bin/python3 -m pytest tests/ -q

# ---- restore pristine -------------------------------------------------------
cd "$FIXTURE"
git checkout -- .
rm -rf acceptance_run metricslite/__pycache__ tests/__pycache__ .pytest_cache
rm -rf "$SCRATCH"
echo "--- pristine restored ---"
git status --short || true
