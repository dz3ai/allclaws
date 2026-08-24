"""Acceptance scoring for long-run benchmark runs.

Philosophy (from the plan): acceptance tests are HIDDEN from the agent and
mounted into the run worktree only at scoring time. The scorer:

1. copies tasks/<id>/acceptance/ into <worktree>/acceptance/
2. runs the spec's acceptance.command with cwd=<worktree>
3. exit 0 => pass

Scenario 4 (triage-burndown) extends this with per-window scoring — the
extension point is score_windows(); Phase 2 wires it up.
"""

from __future__ import annotations

import shutil
import subprocess
from dataclasses import dataclass, field
from pathlib import Path

from longrun.spec import TaskSpec

ACCEPTANCE_DIRNAME = "acceptance"
SCORING_TIMEOUT_SECONDS = 600  # generous: hidden suites are small


@dataclass
class ScoringResult:
    passed: bool
    command: str
    exit_code: int | None = None
    log_path: str | None = None
    details: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "passed": self.passed,
            "command": self.command,
            "exit_code": self.exit_code,
            "log_path": self.log_path,
            "details": self.details,
        }


def mount_acceptance(spec: TaskSpec, worktree: Path) -> Path:
    """Copy the hidden acceptance suite into the worktree (scoring time only)."""
    dest = worktree / ACCEPTANCE_DIRNAME
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(spec.acceptance_dir, dest)
    return dest


def run_acceptance(spec: TaskSpec, worktree: Path, run_dir: Path) -> ScoringResult:
    """Mount hidden tests + execute the spec acceptance command in worktree."""
    mount_acceptance(spec, worktree)
    cmd = spec.acceptance["command"]
    proc = subprocess.run(
        cmd,
        shell=True,
        cwd=str(worktree),
        stdin=subprocess.DEVNULL,
        capture_output=True,
        text=True,
        timeout=SCORING_TIMEOUT_SECONDS,
    )
    log_path = run_dir / "acceptance.log"
    log_path.write_text(
        f"$ {cmd}\n--- stdout ---\n{proc.stdout}\n--- stderr ---\n{proc.stderr}",
        encoding="utf-8",
    )
    return ScoringResult(
        passed=proc.returncode == 0,
        command=cmd,
        exit_code=proc.returncode,
        log_path=str(log_path),
    )


def diff_stats(worktree: Path) -> dict:
    """Quality-of-diff metrics from the agent's changes vs the pristine copy.

    Uses git against the fixture's 'Initial commit' — fixtures are git-inited
    by contract, and the worktree is a copy including .git.
    """
    stats = {"files_touched": 0, "lines_added": 0, "lines_removed": 0}
    try:
        proc = subprocess.run(
            ["git", "diff", "--numstat", "HEAD"],
            cwd=str(worktree),
            capture_output=True,
            text=True,
            timeout=60,
        )
        if proc.returncode == 0:
            for line in proc.stdout.splitlines():
                parts = line.split("\t")
                if len(parts) == 3:
                    stats["files_touched"] += 1
                    a, r = parts[0], parts[1]
                    stats["lines_added"] += int(a) if a.isdigit() else 0
                    stats["lines_removed"] += int(r) if r.isdigit() else 0
    except (subprocess.TimeoutExpired, OSError):
        pass
    return stats


def score_windows(spec: TaskSpec, worktree: Path, run_dir: Path) -> list[dict]:
    """Per-window scoring for triage-burndown (Phase 2 fatigue protocol).

    Each window = one issue in the 5-issue sequence. Returns one dict per
    window: solved, tokens, turns, wall_seconds. Placeholder until S4 lands.
    """
    raise NotImplementedError("S4 per-window scoring lands in Phase 2")
