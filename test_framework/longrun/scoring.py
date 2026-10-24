"""Acceptance scoring for long-run benchmark runs.

Philosophy (from the plan): acceptance tests are HIDDEN from the agent and
mounted into the run worktree only at scoring time. The scorer:

1. copies tasks/<id>/acceptance/ into <worktree>/acceptance/
2. runs the spec's acceptance.command with cwd=<worktree>
3. exit 0 => pass

Scenario 4 (triage-burndown) extends this with per-window scoring —
score_windows() implements it (plan §Fatigue Detection Protocol): the
hidden acceptance dir ships check_windows.py, which prints ONE JSON line
{"windows": [{"window": N, "solved": bool}, ...]}.
"""

from __future__ import annotations

import json
import shutil
import subprocess
from dataclasses import dataclass, field
from pathlib import Path

from longrun.spec import TaskSpec

ACCEPTANCE_DIRNAME = "acceptance"
SCORING_TIMEOUT_SECONDS = 600  # generous: hidden suites are small
WINDOW_SCORING_TIMEOUT_SECONDS = 300  # per-window checker budget (task-7 brief)
PYTHON_BIN = "/usr/bin/python3"  # repo convention: stdlib checks use system python3
WINDOW_CHECKER = "check_windows.py"


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


def score_windows(
    spec: TaskSpec,
    worktree: Path,
    run_dir: Path,
    window_metrics: list[dict | None] | None = None,
) -> list[dict]:
    """Per-window scoring for triage-burndown (plan §Fatigue Detection Protocol).

    Runs <worktree>/acceptance/check_windows.py (mount_acceptance is done by
    the runner before scoring) and parses the LAST stdout line that is valid
    JSON carrying a windows list. Every returned dict honors the hard
    contract consumed by longrun.fatigue and report.py:

        {"window": int, "solved": bool,
         "tokens": int|None, "turns": int|None, "wall_seconds": float|None}

    window_metrics: the run's result.extra["window_metrics"] (driver-recorded
    per-window metrics, list aligned by window number, may be partial or
    absent) — merged in here because the RunResult itself is not reachable
    from this signature; runner.run_one passes it through.

    Failure contract: returns [] — never raises — when the spec is not
    triage-burndown, the checker is missing, it exits nonzero / times out /
    hits an OS error, or its output cannot be parsed (run_one adds the note).
    """
    if spec.type != "triage-burndown":
        return []
    checker = worktree / ACCEPTANCE_DIRNAME / WINDOW_CHECKER
    if not checker.is_file():
        return []
    try:
        proc = subprocess.run(
            [PYTHON_BIN, f"{ACCEPTANCE_DIRNAME}/{WINDOW_CHECKER}"],
            cwd=str(worktree),
            stdin=subprocess.DEVNULL,
            capture_output=True,
            text=True,
            timeout=WINDOW_SCORING_TIMEOUT_SECONDS,
        )
    except (subprocess.TimeoutExpired, OSError):
        return []
    _write_checker_log(run_dir, proc)
    if proc.returncode != 0:
        return []
    windows = _parse_windows_stdout(proc.stdout)
    return merge_window_metrics(windows, window_metrics)


def _write_checker_log(run_dir: Path, proc: subprocess.CompletedProcess) -> None:
    """Persist raw checker output beside the other run artifacts (best effort)."""
    try:
        (run_dir / "windows.log").write_text(
            f"$ {PYTHON_BIN} {ACCEPTANCE_DIRNAME}/{WINDOW_CHECKER}\n"
            f"exit={proc.returncode}\n"
            f"--- stdout ---\n{proc.stdout}\n--- stderr ---\n{proc.stderr}",
            encoding="utf-8",
        )
    except OSError:
        pass


def _parse_windows_stdout(stdout: str) -> list[dict]:
    """Parse the LAST stdout line that is valid JSON with a windows list.

    Defensive (task-7 bar): every field is type-gated (type(x) is int / is
    bool, which also rejects bool masquerading as int), malformed lines and
    entries are skipped, and no match yields [] instead of raising.
    """
    for line in reversed(stdout.splitlines()):
        line = line.strip()
        if not line:
            continue
        try:
            payload = json.loads(line)
        except json.JSONDecodeError:
            continue
        if type(payload) is not dict or type(payload.get("windows")) is not list:
            continue
        windows: list[dict] = []
        for item in payload["windows"]:
            if type(item) is not dict:
                continue
            number = item.get("window")
            solved = item.get("solved")
            if type(number) is not int or type(solved) is not bool:
                continue
            windows.append(
                {
                    "window": number,
                    "solved": solved,
                    "tokens": None,
                    "turns": None,
                    "wall_seconds": None,
                }
            )
        return windows
    return []


def merge_window_metrics(
    windows: list[dict], metrics: list[dict | None] | None
) -> list[dict]:
    """Overlay driver-recorded per-window metrics onto checker window dicts.

    metrics is result.extra["window_metrics"]: a list aligned by window
    number (index i -> window i+1); drivers emit shorter/partial lists or
    None. An entry may carry "tokens" (int), "turns" (int) and
    "wall_seconds" (int|float, coerced to float); anything else keeps the
    None placeholder. Returns NEW dicts — neither input is mutated.
    """
    merged = [dict(w) for w in windows]
    if type(metrics) is not list:
        return merged
    for w in merged:
        number = w.get("window")
        if type(number) is not int or not 1 <= number <= len(metrics):
            continue
        entry = metrics[number - 1]
        if type(entry) is not dict:
            continue
        declared = entry.get("window")
        if type(declared) is int and declared != number:
            continue  # entry self-declares a different window: do not guess
        tokens = entry.get("tokens")
        if type(tokens) is int:
            w["tokens"] = tokens
        turns = entry.get("turns")
        if type(turns) is int:
            w["turns"] = turns
        wall = entry.get("wall_seconds")
        if type(wall) is int or type(wall) is float:
            w["wall_seconds"] = float(wall)
    return merged
