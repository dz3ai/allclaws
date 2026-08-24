"""Driver contract for long-running agent benchmarks (Q4-4).

Every platform driver implements DriverBase with three methods:

    prepare(worktree)   - idempotent one-time setup per platform (venv, build,
                          CLI availability check). Raise PrepareError if the
                          platform cannot run at all.
    run(worktree, spec) - build the launch spec (argv/env/cwd/artifacts) for
                          ONE task run. Must be non-interactive: no TTY, no
                          stdin prompts (runner sets stdin to /dev/null).
    collect(...)        - parse the outcome + artifacts into a RunResult
                          (tokens, turns, cost where the CLI reports them).

The RUNNER owns process lifecycle (spawn, hard timeout, kill), worktree
isolation, acceptance scoring and cost-cap enforcement. Drivers must NEVER
manage processes, timeouts or budgets themselves.

Token estimation: when a CLI does not report usage, drivers call
estimate_tokens() on transcript/stdout characters (chars/4 heuristic per plan).
"""

from __future__ import annotations

import abc
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, ClassVar

from longrun.spec import TaskSpec

# Status values used across runner/scoring/reporting.
STATUS_PASS = "pass"
STATUS_FAIL = "fail"
STATUS_PARTIAL = "partial"
STATUS_ERROR = "error"
STATUS_TIMEOUT = "timeout"


class DriverError(RuntimeError):
    """Driver could not be loaded or constructed."""


class PrepareError(RuntimeError):
    """Platform cannot run (missing CLI, build failed, no credentials)."""


@dataclass
class ProcSpec:
    """How to launch the agent for one run. Returned by DriverBase.run()."""

    argv: list[str]
    cwd: Path
    env: dict[str, str] = field(default_factory=dict)  # merged OVER os.environ
    artifacts: list[str] = field(default_factory=list)  # transcript/log paths
    # (relative to cwd) the driver wants preserved + parsed in collect()


@dataclass
class ProcOutcome:
    """Raw process result produced by the runner, consumed by collect()."""

    exit_code: int | None  # None when killed on timeout
    wall_seconds: float
    timed_out: bool
    stdout_path: Path
    stderr_path: Path


@dataclass
class RunResult:
    platform: str
    task_id: str
    status: str = STATUS_ERROR
    exit_code: int | None = None
    wall_seconds: float = 0.0
    turns: int | None = None
    tokens_in: int | None = None
    tokens_out: int | None = None
    tokens_cached: int | None = None
    cost_usd: float | None = None
    transcript_path: str | None = None
    notes: str = ""
    extra: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "platform": self.platform,
            "task_id": self.task_id,
            "status": self.status,
            "exit_code": self.exit_code,
            "wall_seconds": round(self.wall_seconds, 2),
            "turns": self.turns,
            "tokens_in": self.tokens_in,
            "tokens_out": self.tokens_out,
            "tokens_cached": self.tokens_cached,
            "cost_usd": self.cost_usd,
            "transcript_path": self.transcript_path,
            "notes": self.notes,
            "extra": self.extra,
        }


def estimate_tokens(char_count: int) -> int:
    """chars/4 heuristic from the plan (used when CLI reports no usage)."""
    return max(0, char_count) // 4


class DriverBase(abc.ABC):
    """Base class for all platform drivers.

    Class attributes every driver MUST set:
        name   - registry name (matches module filename, e.g. "kimi_cli")
        binary - absolute path (or PATH-resolvable name) of the agent CLI
    """

    name: ClassVar[str] = "base"
    binary: ClassVar[str] = ""

    def __init__(self, repo_root: Path):
        self.repo_root = Path(repo_root).resolve()

    # ------------------------------------------------------------------
    def prepare(self, worktree: Path) -> None:
        """One-time per-platform setup. Default: assert self.binary resolves.

        Override to build deps / create venvs. MUST be idempotent and fast
        when already prepared. Raise PrepareError (not OSError) on failure.
        """
        if not self.binary:
            raise PrepareError(f"{type(self).__name__}: class attribute 'binary' unset")
        exe = Path(self.binary)
        if not exe.is_absolute() and not self._which(self.binary):
            raise PrepareError(f"{self.name}: CLI {self.binary!r} not found on PATH")
        if exe.is_absolute() and not exe.exists():
            raise PrepareError(f"{self.name}: CLI not found at {self.binary}")

    # ------------------------------------------------------------------
    @abc.abstractmethod
    def run(self, worktree: Path, spec: TaskSpec) -> ProcSpec:
        """Build the launch spec for one task run in `worktree`.

        Rules:
        - Fully non-interactive: pass --yes/--no-input style flags, set
          GIT_TERMINAL_PROMPT=0 etc. The runner runs with stdin=/dev/null.
        - The prompt comes from spec.task_prompt VERBATIM (identical across
          all agents — no per-agent prompt massaging).
        - Model selection flows through env (e.g. AIDER_MODEL) so the runner
          can pin it per batch; drivers only read, never hardcode keys.
        """

    # ------------------------------------------------------------------
    def collect(
        self, worktree: Path, outcome: ProcOutcome, proc: ProcSpec, spec: TaskSpec
    ) -> RunResult:
        """Parse outcome + artifacts into RunResult. Default: minimal result
        with chars/4 token estimate from stdout. Override for CLIs that emit
        structured usage (aider summary line, codex --json events, ...)."""
        chars = 0
        for p in (outcome.stdout_path, outcome.stderr_path):
            try:
                chars += p.stat().st_size
            except OSError:
                pass
        transcript = next(
            (str(worktree / a) for a in proc.artifacts if (worktree / a).exists()),
            None,
        )
        return RunResult(
            platform=self.name,
            task_id=spec.id,
            status=(STATUS_TIMEOUT if outcome.timed_out else
                    STATUS_PASS if outcome.exit_code == 0 else STATUS_FAIL),
            exit_code=outcome.exit_code,
            wall_seconds=outcome.wall_seconds,
            tokens_in=estimate_tokens(chars),
            transcript_path=transcript,
            notes="default collect (chars/4 estimate)",
        )

    # ------------------------------------------------------------------
    @staticmethod
    def _which(binary: str) -> str | None:
        import shutil

        return shutil.which(binary)
