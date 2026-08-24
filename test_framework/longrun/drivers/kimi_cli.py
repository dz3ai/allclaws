"""Kimi-CLI driver — uv workspace Python CLI at coding-agents/cli-agents/kimi-cli.

LIVE-MODE note: no venv exists yet (audited 2026-08-24). prepare() creates
one via `uv sync` inside the submodule (network-using BY DESIGN — dependency
install happens at prepare time, never at run time). This writes untracked
files (.venv/, uv.lock updates) inside the submodule worktree, which is
acceptable per the long-run plan: platform tooling lives in the main
checkout; run isolation applies to fixtures only.

Entry + one-shot mode were verified from source (2026-08-24):
- [project.scripts] kimi = "kimi_cli.__main__:kimi"  (root pyproject.toml)
- Typer CLI: `kimi --print` enters the non-interactive print UI (one prompt,
  run, exit) — see src/kimi_cli/cli/__init__.py + ui/print.
"""

from __future__ import annotations

import os
import subprocess
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

UV = Path.home() / ".local" / "bin" / "uv"


class KimiCliDriver(DriverBase):
    name = "kimi_cli"
    binary = ""  # resolved in prepare()

    def __init__(self, repo_root: Path):
        super().__init__(repo_root)
        self._submodule = self.repo_root / "coding-agents" / "cli-agents" / "kimi-cli"
        self._binary_path: Path | None = None

    # ------------------------------------------------------------------
    def prepare(self, worktree: Path) -> None:
        """Idempotent: create .venv via uv sync if missing (network exempt)."""
        if not self._submodule.is_dir():
            raise PrepareError(f"kimi-cli submodule missing at {self._submodule}")
        if not UV.is_file():
            raise PrepareError(f"uv not found at {UV}")

        candidate = self._submodule / ".venv" / "bin" / "kimi"
        if not candidate.is_file():
            # uv sync resolves the workspace and installs console scripts.
            proc = subprocess.run(
                [str(UV), "sync"],
                cwd=str(self._submodule),
                capture_output=True,
                text=True,
                timeout=900,  # first run downloads + builds workspace deps
            )
            if proc.returncode != 0 or not candidate.is_file():
                tail = (proc.stderr or proc.stdout or "").strip().splitlines()[-3:]
                raise PrepareError(
                    "uv sync failed for kimi-cli: " + " | ".join(tail)
                )
        self._binary_path = candidate

    # ------------------------------------------------------------------
    def run(self, worktree: Path, spec: TaskSpec) -> ProcSpec:
        assert self._binary_path is not None, "prepare() not called"
        argv = [
            str(self._binary_path),
            "--print",           # non-interactive print UI: one prompt, exit
            "--afk",             # auto-approve tool calls + auto-dismiss questions
            "--prompt", spec.task_prompt,   # verified: typer Option, NOT positional
        ]
        return ProcSpec(
            argv=argv,
            cwd=Path(worktree),
            env={
                "GIT_TERMINAL_PROMPT": "0",
                "NO_COLOR": "1",
                "TERM": "dumb",
                # model/provider credentials injected by the runner via os.environ
            },
            artifacts=[],
        )

    # ------------------------------------------------------------------
    def collect(self, worktree, outcome, proc, spec):
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

        return RunResult(
            platform=self.name,
            task_id=spec.id,
            status=status,
            exit_code=outcome.exit_code,
            wall_seconds=outcome.wall_seconds,
            tokens_in=estimate_tokens(chars),
            notes="kimi print-UI: chars/4 estimate (no structured usage yet)",
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
    driver = KimiCliDriver(repo_root=Path(__file__).resolve().parents[3])
    ps = driver.run(Path(tempfile.mkdtemp()), fake)
    print("argv:", ps.argv)
    print("env keys:", sorted(ps.env.keys()))
