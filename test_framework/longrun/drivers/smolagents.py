"""smolagents driver — HF library framework via single-file harness.

Plan §Scope Ruling: smolagents is a LIBRARY (pip-installable), not a CLI, so
its "binary" is a bespoke single-file harness: _smolagents_harness.py (next to
this module) run under a dedicated venv. Network is used AT PREPARE TIME ONLY
(venv creation + `pip install smolagents`; kimi uv-sync precedent) — never at
run time. The venv lives at test_framework/longrun/_venvs/smolagents
(gitignored; platform tooling belongs to the main checkout, run isolation
applies to fixtures only). Nothing is resolved from Path.home() — the venv
path is repo-relative and the venv's own python is invoked explicitly.

Usage contract (harness -> collect()): the harness prints the agent's final
answer to stdout, then exactly one machine-readable line
    LONGRUN_USAGE {"tokens_in": <int|null>, "tokens_out": <int|null>}
collect() scans stdout for that line; when absent (or nulls) it falls back to
the chars/4 estimate per base.py.
"""

from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

from longrun.drivers.base import (
    STATUS_FAIL,
    STATUS_PASS,
    STATUS_TIMEOUT,
    DriverBase,
    PrepareError,
    ProcOutcome,
    ProcSpec,
    RunResult,
    estimate_tokens,
)
from longrun.spec import TaskSpec

HARNESS_PATH = Path(__file__).resolve().parent / "_smolagents_harness.py"
VENV_DIR = Path("test_framework") / "longrun" / "_venvs" / "smolagents"
USAGE_PREFIX = "LONGRUN_USAGE "


class SmolagentsDriver(DriverBase):
    name = "smolagents"
    binary = ""  # resolved in prepare(): the venv's python interpreter

    def __init__(self, repo_root: Path):
        super().__init__(repo_root)
        self._venv = self.repo_root / VENV_DIR
        self._python: Path | None = None

    # ------------------------------------------------------------------
    def prepare(self, worktree: Path) -> None:
        """Idempotent: create the venv + install smolagents (network exempt).

        Skips creation when <venv>/bin/python exists AND `import smolagents`
        succeeds through that interpreter. Uses /usr/bin/python3 -m venv and
        the venv's own pip — nothing from Path.home().
        """
        if not HARNESS_PATH.is_file():
            raise PrepareError(f"smolagents harness missing at {HARNESS_PATH}")

        venv_python = self._venv / "bin" / "python"
        if venv_python.is_file():
            probe = subprocess.run(
                [str(venv_python), "-c", "import smolagents"],
                capture_output=True,
                text=True,
                timeout=120,
            )
            if probe.returncode == 0:
                self._python = venv_python
                return

        try:
            proc = subprocess.run(
                ["/usr/bin/python3", "-m", "venv", str(self._venv)],
                capture_output=True,
                text=True,
                timeout=300,
            )
        except (subprocess.TimeoutExpired, OSError) as e:
            # runner.run_one only catches PrepareError; a failed/hung venv
            # creation must degrade, not crash the runner.
            raise PrepareError(f"smolagents: venv creation failed: {e}") from e
        if proc.returncode != 0 or not venv_python.is_file():
            tail = (proc.stderr or proc.stdout or "").strip().splitlines()[-3:]
            raise PrepareError(
                "smolagents: venv creation failed: " + " | ".join(tail)
            )

        try:
            proc = subprocess.run(
                [str(self._venv / "bin" / "pip"), "install", "smolagents"],
                capture_output=True,
                text=True,
                timeout=1800,  # cold start downloads the full dep tree
            )
        except (subprocess.TimeoutExpired, OSError) as e:
            raise PrepareError(f"smolagents: pip install failed: {e}") from e
        if proc.returncode != 0:
            tail = (proc.stderr or proc.stdout or "").strip().splitlines()[-3:]
            raise PrepareError(
                "smolagents: pip install smolagents failed: " + " | ".join(tail)
            )
        self._python = venv_python

    # ------------------------------------------------------------------
    def run(self, worktree: Path, spec: TaskSpec) -> ProcSpec:
        assert self._python is not None, "prepare() not called"
        argv = [
            str(self._python),
            str(HARNESS_PATH),
            "--prompt", spec.task_prompt,  # verbatim, explicit flag channel
        ]
        model = os.environ.get("LONGRUN_MODEL")
        if model:
            argv += ["--model", model]
        return ProcSpec(
            argv=argv,
            cwd=Path(worktree),
            env={
                "GIT_TERMINAL_PROMPT": "0",
                "NO_COLOR": "1",
                "TERM": "dumb",
                # provider credentials injected by the runner via os.environ
            },
            artifacts=[],
        )

    # ------------------------------------------------------------------
    def collect(
        self, worktree: Path, outcome: ProcOutcome, proc: ProcSpec, spec: TaskSpec
    ) -> RunResult:
        tokens_in = tokens_out = None
        try:
            stdout = outcome.stdout_path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            stdout = ""
        for line in stdout.splitlines():
            if line.startswith(USAGE_PREFIX):
                try:
                    data = json.loads(line[len(USAGE_PREFIX):])
                except ValueError:
                    data = {}
                if isinstance(data, dict):
                    # type(x) is int (not isinstance) so JSON true/false can't pass
                    if type(data.get("tokens_in")) is int:
                        tokens_in = data["tokens_in"]
                    if type(data.get("tokens_out")) is int:
                        tokens_out = data["tokens_out"]

        if tokens_in is None and tokens_out is None:
            chars = len(stdout)
            try:
                chars += outcome.stderr_path.stat().st_size
            except OSError:
                pass
            tokens_in = estimate_tokens(chars)

        if outcome.timed_out:
            status = STATUS_TIMEOUT
        else:
            status = STATUS_PASS if outcome.exit_code == 0 else STATUS_FAIL

        return RunResult(
            platform=self.name,
            task_id=spec.id,
            status=status,
            exit_code=outcome.exit_code,
            wall_seconds=outcome.wall_seconds,
            tokens_in=tokens_in,
            tokens_out=tokens_out,
            transcript_path=None,
            notes=(
                "smolagents LONGRUN_USAGE line parsed"
                if tokens_out is not None
                else "smolagents: chars/4 estimate (no usable usage line)"
            ),
        )


if __name__ == "__main__":
    import tempfile

    fake = TaskSpec(
        id="smoke",
        type="github-issue",
        fixture_repo="fixture",
        task_prompt="smoke test prompt",
        timeout_minutes=1,
        max_turns=10,
        acceptance={"method": "pytest", "command": "true", "pass_criteria": "exit 0"},
        cost_cap_usd=1.0,
        task_dir=Path(tempfile.mkdtemp()),
    )
    driver = SmolagentsDriver(repo_root=Path(__file__).resolve().parents[3])
    driver._python = driver._venv / "bin" / "python"  # stub: no venv needed
    ps = driver.run(Path(tempfile.mkdtemp()), fake)
    print("argv:", ps.argv)
    print("env keys:", sorted(ps.env.keys()))
    assert ps.argv[ps.argv.index("--prompt") + 1] == "smoke test prompt", (
        "prompt not verbatim"
    )
    if "LONGRUN_MODEL" in os.environ:
        model = os.environ["LONGRUN_MODEL"]
        assert ps.argv[-2:] == ["--model", model], "--model missing/wrong"
        print(f"--model OK: {model}")
    else:
        assert "--model" not in ps.argv, "--model present without LONGRUN_MODEL"
        print("no --model without LONGRUN_MODEL: OK")
    print("verbatim prompt OK (explicit --prompt channel)")
