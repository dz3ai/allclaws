"""Smoke verification for the longrun package (Phase 2 wiring, no launches).

Checks:
1. all longrun modules compile + import
2. all 7 drivers load and build a ProcSpec from a fake TaskSpec:
   - aider/codex/kimi_cli: Phase 1 checks kept (codex calls real prepare)
   - reasonix: stubbed _binary_path (no Go toolchain needed for argv build)
   - opencode: REAL prepare (CLI installed on this host)
   - smolagents + hermes: stubbed venv python path
   Phase 2 drivers assert: verbatim prompt, non-interactive env keys, and
   LONGRUN_MODEL mapping (--model ONLY when the env var is set; empty-string
   treated as unset where the driver documents that, smolagents + hermes).
3. codex driver resolves the real entry (bin/codex.js via package.json)
4. all 5 task specs validate against the contract (fixture/ + acceptance/)

Run: /usr/bin/python3 test_framework/longrun/smoke.py
"""

import os
import sys
import tempfile
from pathlib import Path

TEST_FRAMEWORK = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(TEST_FRAMEWORK))

from longrun.drivers import load_driver  # noqa: E402
from longrun.spec import SpecError, TaskSpec, load_all_tasks  # noqa: E402

REPO_ROOT = TEST_FRAMEWORK.parent

NON_INTERACTIVE_ENV = {"GIT_TERMINAL_PROMPT": "0", "NO_COLOR": "1", "TERM": "dumb"}

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


def assert_non_interactive(ps):
    for key, expected in NON_INTERACTIVE_ENV.items():
        assert ps.env.get(key) == expected, (key, ps.env)


def model_env_restored(fn):
    """Run fn with LONGRUN_MODEL controlled: env -u semantics (pop/restore)."""

    def wrapper():
        saved = os.environ.pop("LONGRUN_MODEL", None)
        try:
            fn()
        finally:
            if saved is not None:
                os.environ["LONGRUN_MODEL"] = saved
            else:
                os.environ.pop("LONGRUN_MODEL", None)

    return wrapper


def assert_model_mapping(d, worktree, spec, empty_as_unset=False):
    """--model appears ONLY when LONGRUN_MODEL is set (and non-empty when the
    driver documents empty-as-unset)."""
    saved = os.environ.pop("LONGRUN_MODEL", None)
    try:
        ps = d.run(worktree, spec)
        assert "--model" not in ps.argv, ps.argv
        if empty_as_unset:
            os.environ["LONGRUN_MODEL"] = ""
            ps = d.run(worktree, spec)
            assert "--model" not in ps.argv, ps.argv
        os.environ["LONGRUN_MODEL"] = "test-provider/test-model"
        ps = d.run(worktree, spec)
        assert ps.argv[-2:] == ["--model", "test-provider/test-model"], ps.argv
    finally:
        if saved is not None:
            os.environ["LONGRUN_MODEL"] = saved
        else:
            os.environ.pop("LONGRUN_MODEL", None)


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


@model_env_restored
def t_reasonix():
    d = load_driver("reasonix", REPO_ROOT)
    d._binary_path = Path("/nonexistent-but-set")  # stub: no Go toolchain needed
    wt = Path(tempfile.mkdtemp())
    ps = d.run(wt, fake_spec())
    assert ps.argv[-2:] == ["--", "p"], ps.argv  # verbatim prompt after --
    assert "run" in ps.argv and "--permission-mode" in ps.argv, ps.argv
    assert "--metrics" in ps.argv, ps.argv
    assert "--model" not in ps.argv, ps.argv  # LONGRUN_MODEL unset
    assert_non_interactive(ps)
    os.environ["LONGRUN_MODEL"] = "test-provider/test-model"
    ps = d.run(wt, fake_spec())
    assert ps.argv[-2:] == ["--", "p"], ps.argv  # prompt still last, verbatim
    assert ps.argv[ps.argv.index("--model") + 1] == "test-provider/test-model"


@model_env_restored
def t_opencode():
    d = load_driver("opencode", REPO_ROOT)
    d.prepare(Path(tempfile.mkdtemp()))  # REAL prepare: binary installed here
    assert d._binary_path, "prepare() must resolve the CLI"
    wt = Path(tempfile.mkdtemp())
    ps = d.run(wt, fake_spec())
    assert ps.argv[-2:] == ["--", "p"], ps.argv  # verbatim prompt after --
    assert "run" in ps.argv and "--auto" in ps.argv, ps.argv
    assert "--model" not in ps.argv, ps.argv  # LONGRUN_MODEL unset
    assert_non_interactive(ps)
    os.environ["LONGRUN_MODEL"] = "test-provider/test-model"
    ps = d.run(wt, fake_spec())
    assert ps.argv[ps.argv.index("--model") + 1] == "test-provider/test-model"
    assert ps.argv[-2:] == ["--", "p"], ps.argv


@model_env_restored
def t_smolagents():
    d = load_driver("smolagents", REPO_ROOT)
    d._python = d._venv / "bin" / "python"  # stub venv path: argv build only
    wt = Path(tempfile.mkdtemp())
    ps = d.run(wt, fake_spec())
    assert ps.argv[ps.argv.index("--prompt") + 1] == "p", ps.argv  # verbatim
    assert "--model" not in ps.argv, ps.argv  # LONGRUN_MODEL unset
    assert_non_interactive(ps)
    os.environ["LONGRUN_MODEL"] = ""
    ps = d.run(wt, fake_spec())  # empty LONGRUN_MODEL treated as unset
    assert "--model" not in ps.argv, ps.argv
    os.environ["LONGRUN_MODEL"] = "test-provider/test-model"
    ps = d.run(wt, fake_spec())
    assert ps.argv[-2:] == ["--model", "test-provider/test-model"], ps.argv


@model_env_restored
def t_hermes():
    d = load_driver("hermes", REPO_ROOT)
    d._python = d._venv / "bin" / "python"  # stub venv path: argv build only
    wt = Path(tempfile.mkdtemp())
    spec = fake_spec()
    ps = d.run(wt, spec)
    assert ps.argv[ps.argv.index("--max-turns") + 1] == str(spec.max_turns), ps.argv
    assert ps.argv[2] == "--prompt=p", ps.argv  # verbatim, '='-joined channel
    assert "--model" not in ps.argv, ps.argv  # LONGRUN_MODEL unset
    assert_non_interactive(ps)
    os.environ["LONGRUN_MODEL"] = ""
    ps = d.run(wt, fake_spec())  # empty LONGRUN_MODEL treated as unset
    assert "--model" not in ps.argv, ps.argv
    os.environ["LONGRUN_MODEL"] = "test-provider/test-model"
    ps = d.run(wt, fake_spec())
    assert ps.argv[-2:] == ["--model", "test-provider/test-model"], ps.argv


check("aider ProcSpec", t_aider)
check("codex prepare + ProcSpec", t_codex)
check("kimi_cli ProcSpec", t_kimi)
check("reasonix ProcSpec (stubbed binary)", t_reasonix)
check("opencode REAL prepare + ProcSpec", t_opencode)
check("smolagents ProcSpec (stubbed venv)", t_smolagents)
check("hermes ProcSpec (stubbed venv)", t_hermes)

print("== task specs ==")


def t_specs():
    tasks = load_all_tasks(TEST_FRAMEWORK / "tasks")
    ids = [t.id for t in tasks]
    assert ids == [
        "feature-crud",
        "gh-issue-001",
        "legacy-migrate",
        "refactor-multi",
        "triage-burndown",
    ], ids
    for t in tasks:
        assert t.fixture_dir.is_dir(), t.fixture_dir
        assert t.acceptance_dir.is_dir(), t.acceptance_dir


check("5 specs validate (fixture/ + acceptance/ present)", t_specs)

print()
if failures:
    print(f"{len(failures)} FAILURES")
    sys.exit(1)
print("ALL SMOKE CHECKS PASSED")
