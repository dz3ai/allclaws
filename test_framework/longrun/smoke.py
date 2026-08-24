"""Smoke verification for the longrun package (Phase 1 wiring, no launches).

Checks:
1. all longrun modules compile + import
2. all 3 drivers load and build a ProcSpec from a fake TaskSpec
3. codex driver resolves the real entry (bin/codex.js via package.json)
4. all 3 task specs validate against the contract (fixture/ + acceptance/)

Run: /usr/bin/python3 test_framework/longrun/smoke.py
"""

import sys
import tempfile
from pathlib import Path

TEST_FRAMEWORK = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(TEST_FRAMEWORK))

from longrun.drivers import load_driver  # noqa: E402
from longrun.spec import SpecError, TaskSpec, load_all_tasks  # noqa: E402

REPO_ROOT = TEST_FRAMEWORK.parent

failures = []


def check(label, fn):
    try:
        fn()
        print(f"  ok  {label}")
    except Exception as e:  # noqa: BLE001
        failures.append(label)
        print(f"FAIL  {label}: {type(e).__name__}: {e}")


def fake_spec():
    return TaskSpec(
        id="smoke",
        type="github-issue",
        fixture_repo="fixture",
        task_prompt="p",
        timeout_minutes=1,
        max_turns=5,
        acceptance={"method": "pytest", "command": "true", "pass_criteria": "exit 0"},
        cost_cap_usd=1.0,
        task_dir=Path(tempfile.mkdtemp()),
    )


print("== drivers ==")


def t_aider():
    d = load_driver("aider", REPO_ROOT)
    ps = d.run(Path(tempfile.mkdtemp()), fake_spec())
    assert "--yes-always" in ps.argv and "--message" in ps.argv, ps.argv
    assert "p" in ps.argv  # prompt passed via --message value


def t_codex():
    d = load_driver("codex", REPO_ROOT)
    d.prepare(Path(tempfile.mkdtemp()))
    assert d._entry is not None and d._entry.is_file(), d._entry
    ps = d.run(Path(tempfile.mkdtemp()), fake_spec())
    assert "exec" in ps.argv and "--json" in ps.argv, ps.argv


def t_kimi():
    d = load_driver("kimi_cli", REPO_ROOT)
    d._binary_path = Path("/nonexistent-but-set")  # satisfy run()'s assert
    ps = d.run(Path(tempfile.mkdtemp()), fake_spec())
    assert "--print" in ps.argv and "--afk" in ps.argv, ps.argv
    assert "p" in ps.argv  # prompt via --prompt value


check("aider ProcSpec", t_aider)
check("codex prepare + ProcSpec", t_codex)
check("kimi_cli ProcSpec", t_kimi)

print("== task specs ==")


def t_specs():
    tasks = load_all_tasks(TEST_FRAMEWORK / "tasks")
    ids = [t.id for t in tasks]
    assert ids == ["feature-crud", "gh-issue-001", "refactor-multi"], ids
    for t in tasks:
        assert t.fixture_dir.is_dir(), t.fixture_dir
        assert t.acceptance_dir.is_dir(), t.acceptance_dir


check("3 specs validate (fixture/ + acceptance/ present)", t_specs)

print()
if failures:
    print(f"{len(failures)} FAILURES")
    sys.exit(1)
print("ALL SMOKE CHECKS PASSED")
