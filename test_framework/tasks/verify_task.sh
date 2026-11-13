#!/usr/bin/env bash
# Verify a task fixture: (1) existing tests pass on pristine tree,
# (2) hidden acceptance FAILS on pristine tree, (3) trees are git-committed.
# All operations are forward-only (init/add/commit + pytest). No rollbacks.
# Usage: verify_task.sh <task-dir>   e.g. verify_task.sh tasks/gh-issue-001
set -u
TASK_DIR="${1:?usage: verify_task.sh <task-dir>}"
FIXTURE="$TASK_DIR/fixture"
ACCEPTANCE="$TASK_DIR/acceptance"

fail() { echo "VERIFY_FAIL: $*"; exit 1; }

TASK_DIR="$(cd "$TASK_DIR" && pwd)"   # absolutize before any cd
FIXTURE="$TASK_DIR/fixture"
ACCEPTANCE="$TASK_DIR/acceptance"

[ -d "$FIXTURE" ] || fail "no fixture at $FIXTURE"
[ -d "$ACCEPTANCE/tests" ] || fail "no acceptance tests at $ACCEPTANCE/tests"

# --- 1. git init the fixture if not already a repo (pristine baseline) ----
if [ ! -d "$FIXTURE/.git" ]; then
  git -C "$FIXTURE" init -q -b main
  git -C "$FIXTURE" add -A
  git -C "$FIXTURE" -c user.name=allclaws -c user.email=allclaws@local \
    commit -qm "Initial commit"
fi

# clean pycache so the tree stays pristine between checks
find "$FIXTURE" -name '__pycache__' -type d -prune -exec rm -rf {} + 2>/dev/null || true
find "$FIXTURE" -name '.pytest_cache' -type d -prune -exec rm -rf {} + 2>/dev/null || true

# --- 2. existing suite: PASS, or PASS-except-documented-bug-tests -------
# Expected-red tests come from spec.json "existing_suite_allow_red" (list of
# node ids, e.g. "test_app.py::TestUsers::test_x"); the ALLOW_RED env var
# (space-separated test names) is a legacy fallback.
ALLOW_RED="${ALLOW_RED:-}"
if [ -z "$ALLOW_RED" ] && [ -f "$TASK_DIR/spec.json" ]; then
  ALLOW_RED=$(jq -r '(.existing_suite_allow_red // []) | join(" ")' "$TASK_DIR/spec.json" 2>/dev/null || true)
fi
cd "$FIXTURE"
if /usr/bin/python3 -m pytest tests/ -q > "$TASK_DIR/.verify_existing.log" 2>&1; then
  echo "existing suite: PASS ($(tail -1 "$TASK_DIR/.verify_existing.log"))"
else
  actual_red=$(grep '^FAILED' "$TASK_DIR/.verify_existing.log" | sed 's/^FAILED tests\///; s/ - .*//' | sort)
  expected_red=$(echo "$ALLOW_RED" | tr ' ' '\n' | grep -v '^$' | sort)
  if [ -n "$expected_red" ] && [ "$actual_red" == "$expected_red" ]; then
    echo "existing suite: PASS with $(echo "$expected_red" | wc -l) documented bug-test(s) red — as designed"
  else
    fail "existing suite fails beyond documented bugs — see $TASK_DIR/.verify_existing.log (got: $actual_red)"
  fi
fi

# --- 3. hidden acceptance must FAIL on pristine --------------------------
rm -rf acceptance_run
mkdir -p acceptance_run
cp -r "$ACCEPTANCE/tests" acceptance_run/
if /usr/bin/python3 -m pytest acceptance_run/tests -q > "$TASK_DIR/.verify_acceptance.log" 2>&1; then
  fail "acceptance PASSED on pristine fixture — it must fail there (discriminates fixed vs unfixed)"
else
  # Count assertion failures AND collection errors (an ImportError during
  # collection reports as ERROR, not FAILED — both mean "red on pristine").
  red=$(grep -cE '^(FAILED|ERROR)' "$TASK_DIR/.verify_acceptance.log" 2>/dev/null || true)
  echo "acceptance vs pristine: FAIL as expected (${red:-?} failing checks)"
fi

# --- 4. restore pristine: never leave hidden tests inside the fixture ----
# The runner copies this fixture into agent worktrees; a leftover
# acceptance_run/ would leak the hidden suite to the agent.
rm -rf "$FIXTURE/acceptance_run"

echo "VERIFY_OK: $TASK_DIR"
