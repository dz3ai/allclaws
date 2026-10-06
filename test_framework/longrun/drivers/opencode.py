"""opencode driver — installed reference platform (untracked), sst/opencode.

Reference-platform status (plan §Scope Ruling + §Risk Register): opencode
participates in the long-run benchmark as an UNTRACKED REFERENCE POINT and is
EXCLUDED FROM RANKINGS ("opencode reference bias — labeled untracked,
excluded from rankings"). collect() notes carry that label on every result.

Invocation evidence from the installed CLI (opencode 1.18.34 at
~/.opencode/bin/opencode; `opencode run --help` captured 2026-10-06):
- Usage: `opencode run [message..]` — the prompt is the POSITIONAL `message`
  array ("message to send"); there is no dedicated prompt flag.
- `-m, --model` — "model to use in the format of provider/model".
- `--auto` — "auto-approve permissions that are not explicitly denied
  (dangerous!)" [boolean, default false] — the only documented approve flag;
  required so the agent can edit fixture files unattended.
- `-i, --interactive` [boolean, default false] — run mode is non-interactive
  by default, so no flag is passed.
- `--format` [choices: "default", "json"] — default prints formatted output;
  run --help exposes no usage/token summary flag, so collect() falls back to
  the chars/4 estimate (base.py contract).
- `--` end-of-options sentinel, verified live (2026-10-06):
  `opencode run -m does-not-exist/x "-DASHTEST"` makes yargs dump the usage
  screen (the leading-dash positional gets flag-parsed), while
  `opencode run -m does-not-exist/x -- "-DASHTEST"` parses clean and only
  fails later at model resolution. The driver therefore guards task_prompt
  with `--` so it is passed VERBATIM even when it starts with "-".

Model mapping: env LONGRUN_MODEL only (never hardcoded) -> `--model
provider/model` per the --help format above. Credentials are already
configured on this host (opencode auth list); the driver never touches them.
"""

from __future__ import annotations

import os
import shutil
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

REFERENCE_NOTE = "untracked reference — excluded from rankings (plan risk table)"


class OpencodeDriver(DriverBase):
    name = "opencode"
    binary = "opencode"  # PATH-resolved in prepare()

    def __init__(self, repo_root: Path):
        super().__init__(repo_root)
        self._binary_path: str | None = None
        self.version: str | None = None

    # ------------------------------------------------------------------
    def prepare(self, worktree: Path) -> None:
        """Idempotent: resolve the CLI on PATH, probe `--version` (non-fatal)."""
        exe = shutil.which("opencode")
        if exe is None:
            raise PrepareError(
                "opencode: CLI not found on PATH (expected at "
                "~/.opencode/bin/opencode)"
            )
        try:
            proc = subprocess.run(
                [exe, "--version"],
                capture_output=True,
                text=True,
                timeout=30,
            )
        except (subprocess.TimeoutExpired, OSError) as e:
            # version probe is advisory; a hang here must not kill the runner
            self.version = None
            del e
        else:
            self.version = (
                (proc.stdout or proc.stderr or "").strip() or None
                if proc.returncode == 0
                else None
            )
        self._binary_path = exe

    # ------------------------------------------------------------------
    def run(self, worktree: Path, spec: TaskSpec) -> ProcSpec:
        assert self._binary_path is not None, "prepare() not called"
        argv = [
            self._binary_path,
            "run",        # one-shot subcommand (`opencode run [message..]`)
            "--auto",     # auto-approve permissions (run --help); unattended writes
        ]
        model = os.environ.get("LONGRUN_MODEL")
        if model:
            argv += ["--model", model]  # provider/model format per run --help
        # `--` sentinel (verified live, see module docstring): stops yargs
        # flag-parsing so a leading '-' in the prompt stays positional.
        argv += ["--", spec.task_prompt]  # positional message, VERBATIM
        return ProcSpec(
            argv=argv,
            cwd=Path(worktree),
            env={
                "GIT_TERMINAL_PROMPT": "0",
                "NO_COLOR": "1",
                "TERM": "dumb",
                # provider credentials injected by the runner via os.environ
            },
            artifacts=[],  # session data lives in ~/.local/share/opencode (outside cwd)
        )

    # ------------------------------------------------------------------
    def collect(
        self, worktree: Path, outcome: ProcOutcome, proc: ProcSpec, spec: TaskSpec
    ) -> RunResult:
        chars = 0
        for p in (outcome.stdout_path, outcome.stderr_path):
            try:
                chars += p.stat().st_size
            except OSError:
                pass

        if outcome.timed_out:
            status = STATUS_TIMEOUT
        else:
            status = STATUS_PASS if outcome.exit_code == 0 else STATUS_FAIL

        version = f"opencode {self.version}; " if self.version else ""
        return RunResult(
            platform=self.name,
            task_id=spec.id,
            status=status,
            exit_code=outcome.exit_code,
            wall_seconds=outcome.wall_seconds,
            tokens_in=estimate_tokens(chars),
            notes=(
                f"{version}chars/4 estimate (no usage output); {REFERENCE_NOTE}"
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
    driver = OpencodeDriver(repo_root=Path(__file__).resolve().parents[3])
    driver._binary_path = shutil.which("opencode") or "opencode"
    ps = driver.run(Path(tempfile.mkdtemp()), fake)
    print("argv:", ps.argv)
    print("env keys:", sorted(ps.env.keys()))
    assert ps.argv[-1] == "smoke test prompt", "prompt not verbatim"
    assert ps.argv[-2] == "--", "missing -- separator before prompt"
    print("verbatim prompt OK (after --)")
