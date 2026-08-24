"""Run orchestration: worktree isolation, launch, timeout, scoring, ledger.

Per run (plan §Driver Architecture):
  1. worktree = copy of the pristine fixture (fixture keeps its own git init)
  2. driver.prepare(worktree) — platform one-time setup, network exempt
  3. driver.run(worktree, spec) -> ProcSpec; launch with stdin=/dev/null
  4. hard timeout = spec.timeout_seconds; on expiry kill process group
  5. driver.collect(...) -> RunResult (tokens/turns where the CLI reports)
  6. scoring.mount_acceptance + run hidden suite  → pass/fail
  7. ledger.record; abort the grid when the ceiling would be breached
"""

from __future__ import annotations

import json
import os
import shutil
import signal
import subprocess
import sys
import time
from pathlib import Path

from longrun import scoring
from longrun.cost import SpendLedger
from longrun.drivers import load_driver
from longrun.drivers.base import (
    STATUS_ERROR,
    STATUS_FAIL,
    STATUS_PASS,
    STATUS_TIMEOUT,
    DriverBase,
    DriverError,
    PrepareError,
    ProcOutcome,
    ProcSpec,
    RunResult,
)
from longrun.spec import TaskSpec, load_spec

DEFAULT_TASKS_ROOT = Path(__file__).resolve().parent.parent / "tasks"
DEFAULT_RESULTS_ROOT = Path(__file__).resolve().parent.parent / "benchmark_results" / "longrun"


class BudgetExhausted(RuntimeError):
    """Raised when the next run would breach the spend ceiling — grid aborts."""


def timestamp() -> str:
    """Colon-free timestamp per repo artifact convention (upload-artifact)."""
    return time.strftime("%Y-%m-%dT%H-%M-%S")


def make_worktree(spec: TaskSpec, scratch_root: Path) -> Path:
    """Copy the pristine fixture into a per-run scratch dir (never in-place).

    If the fixture template carries no .git (the committed form), the copy is
    git-inited here so scoring.diff_stats and agent git tooling work.
    """
    scratch_root.mkdir(parents=True, exist_ok=True)
    dest = scratch_root / f"{spec.id}-{os.getpid()}-{int(time.time() * 1000) % 100000}"
    shutil.copytree(spec.fixture_dir, dest, symlinks=True)
    if not (dest / ".git").exists():
        subprocess.run(["git", "init", "-q", "-b", "main"], cwd=str(dest), check=True)
        subprocess.run(["git", "add", "-A"], cwd=str(dest), check=True)
        subprocess.run(
            [
                "git",
                "-c",
                "user.name=longrun",
                "-c",
                "user.email=longrun@local",
                "commit",
                "-qm",
                "Initial commit",
            ],
            cwd=str(dest),
            check=True,
            env={**os.environ, "GIT_TERMINAL_PROMPT": "0"},
        )
    return dest


def cleanup_worktree(worktree: Path) -> None:
    shutil.rmtree(worktree, ignore_errors=True)


def merge_env(overlay: dict[str, str]) -> dict[str, str]:
    env = {k: v for k, v in os.environ.items() if k not in ("PS1",)}
    env.update(overlay)
    return env


def launch(
    proc_spec: ProcSpec,
    timeout_seconds: int,
    stdout_path: Path,
    stderr_path: Path,
) -> ProcOutcome:
    """Run one agent process to completion (or hard timeout). Runner-owned."""
    env = merge_env(proc_spec.env)
    with open(stdout_path, "wb") as out, open(stderr_path, "wb") as err:
        proc = subprocess.Popen(
            proc_spec.argv,
            cwd=str(proc_spec.cwd),
            env=env,
            stdin=subprocess.DEVNULL,
            stdout=out,
            stderr=err,
            start_new_session=True,  # own process group -> kill the whole tree
        )
        start = time.monotonic()
        timed_out = False
        try:
            proc.wait(timeout=timeout_seconds)
        except subprocess.TimeoutExpired:
            timed_out = True
            _kill_tree(proc)
        wall = time.monotonic() - start
    return ProcOutcome(
        exit_code=None if timed_out else proc.returncode,
        wall_seconds=wall,
        timed_out=timed_out,
        stdout_path=stdout_path,
        stderr_path=stderr_path,
    )


def _kill_tree(proc: subprocess.Popen) -> None:
    try:
        os.killpg(proc.pid, signal.SIGKILL)
    except (ProcessLookupError, PermissionError, OSError):
        proc.kill()
    try:
        proc.wait(timeout=10)
    except subprocess.TimeoutExpired:
        pass


def run_one(
    driver: DriverBase,
    spec: TaskSpec,
    results_root: Path,
    scratch_root: Path | None = None,
    skip_scoring: bool = False,
    dry_run: bool = False,
) -> dict:
    """Full lifecycle for one (platform, task) run. Returns the result dict."""
    run_dir = results_root / driver.name / spec.id
    run_dir.mkdir(parents=True, exist_ok=True)
    scratch_root = scratch_root or (results_root / "_scratch")
    worktree = None

    try:
        # 1-2. isolation + platform prep
        worktree = make_worktree(spec, scratch_root)
        driver.prepare(worktree)

        if dry_run:
            proc_spec = driver.run(worktree, spec)
            payload = {
                "platform": driver.name,
                "task_id": spec.id,
                "status": "dry-run",
                "argv": proc_spec.argv,
                "env_keys": sorted(proc_spec.env.keys()),
                "cwd": str(proc_spec.cwd),
            }
            (run_dir / "result.json").write_text(
                json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8"
            )
            cleanup_worktree(worktree)
            return payload

        # 3-4. launch with hard timeout
        proc_spec = driver.run(worktree, spec)
        (run_dir / "argv.json").write_text(
            json.dumps(
                {"argv": proc_spec.argv, "cwd": str(proc_spec.cwd), "env_keys": sorted(proc_spec.env)},
                indent=2,
            ),
            encoding="utf-8",
        )
        outcome = launch(
            proc_spec,
            timeout_seconds=spec.timeout_seconds,
            stdout_path=run_dir / "stdout.log",
            stderr_path=run_dir / "stderr.log",
        )

        # 5. driver-side parsing
        result = driver.collect(worktree, outcome, proc_spec, spec)

        # 6. hidden acceptance scoring
        if not skip_scoring:
            try:
                score = scoring.run_acceptance(spec, worktree, run_dir)
            except subprocess.TimeoutExpired:
                score = None
                result.notes += " | acceptance scoring timed out"
            if score is not None:
                result.extra["score"] = score.to_dict()
        result.extra.setdefault("score", {"passed": False, "details": "not scored"})
        result.extra["diff_stats"] = scoring.diff_stats(worktree)

    except PrepareError as e:
        result = RunResult(
            platform=driver.name,
            task_id=spec.id,
            status=STATUS_ERROR,
            notes=f"prepare failed: {e}",
        )
        result.extra = {"score": {"passed": False, "details": "prepare failed"}}
    except BudgetExhausted:
        if worktree:
            cleanup_worktree(worktree)
        raise
    finally:
        # 7. preserve artifacts from the worktree before cleanup
        if worktree and worktree.exists():
            for rel in ("aider", ".aider.chat.history.md", ".aider.input.history"):
                pass  # transcript paths recorded by drivers via RunResult
            _archive_artifacts(run_dir, worktree, proc_spec_artifacts(result) if 'result' in dir() else [])
            cleanup_worktree(worktree)

    _write_result(run_dir, result)
    return result.to_dict() | {"score": result.extra.get("score", {})}


def proc_spec_artifacts(result: RunResult) -> list[str]:
    return []


def _archive_artifacts(run_dir: Path, worktree: Path, artifacts: list[str]) -> None:
    """Copy driver-declared artifact files from worktree into run_dir."""
    if not artifacts:
        return
    keep = run_dir / "artifacts"
    keep.mkdir(parents=True, exist_ok=True)
    for rel in artifacts:
        src = worktree / rel
        if src.is_file():
            shutil.copy2(src, keep / Path(rel).name)


def _write_result(run_dir: Path, result: RunResult) -> None:
    payload = result.to_dict()
    payload["extra"] = result.extra
    (run_dir / "result.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8"
    )


def run_grid(
    drivers: list[str],
    task_ids: list[str],
    tasks_root: Path = DEFAULT_TASKS_ROOT,
    results_root: Path | None = None,
    ledger_path: Path | None = None,
    dry_run: bool = False,
    repeats: int = 1,
    model: str | None = None,
) -> dict:
    """Run a (drivers × tasks × repeats) grid under the spend ceiling.

    Sequential per-platform (plan guardrail: no parallel burn). Every launch
    checks the ledger first; ceiling breach aborts the whole grid.
    """
    results_root = results_root or DEFAULT_RESULTS_ROOT
    stamp = timestamp()
    run_root = results_root / stamp
    ledger = SpendLedger(ledger_path or (results_root / "spend_ledger.json"))

    # env pin for this batch (drivers read, never hardcode)
    if model:
        os.environ["LONGRUN_MODEL"] = model

    all_results = []
    for repeat in range(1, max(1, repeats) + 1):
        for task_id in task_ids:
            spec = load_spec(tasks_root / task_id / "spec.json")
            for driver_name in drivers:
                ok, why = ledger.check_run_allowed(spec.cost_cap_usd)
                if not ok:
                    raise BudgetExhausted(why)
                print(
                    f"[longrun] {stamp} rep{repeat} {driver_name} x {task_id} "
                    f"(budget left ${ledger.remaining_budget():.2f})",
                    flush=True,
                )
                try:
                    driver = load_driver(driver_name, repo_root=tasks_root.parent.parent)
                except DriverError as e:
                    print(f"[longrun] SKIP {driver_name}: {e}", flush=True)
                    continue
                res = run_one(driver, spec, run_root, dry_run=dry_run)
                res["repeat"] = repeat
                all_results.append(res)
                # record spend from reported tokens (model-pinned per batch)
                model_name = model or os.environ.get("LONGRUN_MODEL", "_default")
                if res.get("tokens_in") or res.get("tokens_out"):
                    ledger.record(
                        platform=driver_name,
                        task_id=task_id,
                        model=model_name,
                        tokens_in=res.get("tokens_in") or 0,
                        tokens_out=res.get("tokens_out") or 0,
                    )
    summary_path = run_root / "grid_summary.json"
    run_root.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(
        json.dumps({"timestamp": stamp, "runs": all_results}, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    return {"run_root": str(run_root), "runs": all_results}
