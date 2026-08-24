"""Aider driver — Python CLI with ready venv at coding-agents/cli-agents/aider.

Non-interactive invocation per plan §drivers:
    aider --yes-always --no-git --no-auto-commits --message <prompt> --model <m>

Token parsing: aider prints a summary line on exit; we scan stdout for
"N tokens sent" / "N tokens received" style lines (both comma-grouped and
plain digits accepted) and fall back to the chars/4 estimate.
"""

from __future__ import annotations

import os
import re
from pathlib import Path

from longrun.drivers.base import (
    STATUS_FAIL,
    STATUS_PASS,
    STATUS_TIMEOUT,
    DriverBase,
    PrepareError,
    ProcSpec,
    RunResult,
    estimate_tokens,
)
from longrun.spec import TaskSpec

SENT_RE = re.compile(r"([\d,.]+)\s*tokens?\s*sent", re.IGNORECASE)
RECEIVED_RE = re.compile(r"([\d,.]+)\s*tokens?\s*received", re.IGNORECASE)


class AiderDriver(DriverBase):
    name = "aider"
    # resolved in prepare(): repo_root is only known at construction time
    binary = ""

    def __init__(self, repo_root: Path):
        super().__init__(repo_root)
        self._binary_path = (
            self.repo_root / "coding-agents" / "cli-agents" / "aider" / ".venv" / "bin" / "aider"
        )

    # ------------------------------------------------------------------
    def prepare(self, worktree: Path) -> None:
        if not self._binary_path.is_file():
            raise PrepareError(
                f"aider venv binary not found at {self._binary_path} "
                "(expected prebuilt venv per benchmark prerequisites)"
            )
        if not os.access(self._binary_path, os.X_OK):
            raise PrepareError(f"aider binary not executable: {self._binary_path}")

    # ------------------------------------------------------------------
    def run(self, worktree: Path, spec: TaskSpec) -> ProcSpec:
        model = os.environ.get("LONGRUN_AIDER_MODEL", "gpt-5.2")
        argv = [
            str(self._binary_path),
            "--yes-always",
            "--no-git",
            "--no-auto-commits",
            "--no-check-update",
            "--no-suggest-shell-commands",
            "--no-fancy-input",
            "--message", spec.task_prompt,
            "--model", model,
        ]
        return ProcSpec(
            argv=argv,
            cwd=Path(worktree),
            env={
                "GIT_TERMINAL_PROMPT": "0",
                "NO_COLOR": "1",
                "TERM": "dumb",
                # credentials injected by the runner via os.environ
            },
            artifacts=[".aider.chat.history.md", ".aider.input.history"],
        )

    # ------------------------------------------------------------------
    def collect(self, worktree, outcome, proc, spec):
        stdout = ""
        try:
            stdout = outcome.stdout_path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            pass

        tokens_in = tokens_out = None
        m = SENT_RE.search(stdout)
        if m:
            tokens_in = _to_int(m.group(1))
        m = RECEIVED_RE.search(stdout)
        if m:
            tokens_out = _to_int(m.group(1))
        if tokens_in is None and tokens_out is None:
            size = 0
            for p in (outcome.stdout_path, outcome.stderr_path):
                try:
                    size += p.stat().st_size
                except OSError:
                    pass
            tokens_in = estimate_tokens(size)

        transcript = None
        for rel in proc.artifacts:
            candidate = worktree / rel
            if candidate.is_file():
                transcript = str(candidate)
                break

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
            transcript_path=transcript,
            notes="aider token summary parsed" if tokens_in else "chars/4 estimate",
        )


def _to_int(group: str) -> int:
    return int(group.replace(",", "").replace(".", ""))


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
    driver = AiderDriver(repo_root=Path(__file__).resolve().parents[3])
    ps = driver.run(Path(tempfile.mkdtemp()), fake)
    print("argv:", ps.argv)
    print("env keys:", sorted(ps.env.keys()))
    print("cwd:", ps.cwd)
