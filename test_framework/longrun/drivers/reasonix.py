"""Reasonix driver — Go CLI submodule at coding-agents/cli-agents/reasonix.

Plan adaptation: the plan calls reasonix a "Node CLI (npm build needed)"; the
submodule is actually Go (go.mod, cmd/reasonix, Makefile). Build = the Makefile
`build` target's first line (Makefile:14-15):
`CGO_ENABLED=0 go build -o bin/reasonix ./cmd/reasonix`.

Non-interactive invocation verified from source (2026-10-06), cmd/reasonix:
- Entry chain: cmd/reasonix/main.go:40-49 -> cli.RunWithBuildInfo
  (main.go:32-38); `case "run": return runAgent(rest, version)` —
  internal/cli/cli.go:126-127.
- Prompt channel: POSITIONAL argument, not a flag —
  `prompt := strings.TrimSpace(strings.Join(fs.Args(), " "))`, stdin fallback
  when empty, usage error + exit 2 when both empty (internal/cli/cli.go:558-565).
  Usage line: `reasonix run [--model NAME] ... <task>`
  (internal/i18n/messages_en.go:627). Note: argv edges get TrimSpace'd and
  multiple positionals are joined with single spaces (cli.go:558).
- Approval: `reasonix run` is headless — "there is no key loop to answer
  approval or ask prompts" (internal/cli/cli.go:661-670). Unattended mode is
  selected via permission mode; we pass `--permission-mode workspace-write`
  explicitly (flag default cli.go:491; maps to
  control.ToolApprovalWorkspaceWrite at cli.go:336-337). `--auto/-y` exists
  but is hidden + deprecated and resolves to the same workspace-write
  (cli.go:492-493, cli.go:357-365), so we use the supported spelling.
- Model: `--model NAME` flag (cli.go:479, "provider name (default: config
  default_model)"). No env-based model override exists in the source (grepped
  internal/ for env config; only provider KEY vars, e.g. DEEPSEEK_API_KEY,
  internal/i18n/messages_en.go:446) — so LONGRUN_MODEL maps to `--model`.
- Structured usage: `--metrics PATH` writes a JSON token/cache/cost summary
  (cli.go:482-483; RunMetrics fields prompt_tokens / completion_tokens /
  cache_hit_tokens / steps / cost — internal/cli/run_metrics.go:32-46,
  written for benchmark harnesses per run_metrics.go:32-33). Parent dirs are
  auto-created (internal/fileutil/atomicwrite.go:162), so collect() parses
  .longrun/reasonix-metrics.json and falls back to chars/4.

Graceful degrade: no Go toolchain is installed on this host (verified
2026-10-06) — prepare() raises PrepareError naming `go` when bin/reasonix is
absent and shutil.which("go") finds nothing. argv construction stays
smoke-testable via a stubbed _binary_path (kimi_cli.py precedent).
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
    ProcSpec,
    RunResult,
    estimate_tokens,
)
from longrun.spec import TaskSpec

METRICS_REL = ".longrun/reasonix-metrics.json"  # relative to cwd (the worktree)


class ReasonixDriver(DriverBase):
    name = "reasonix"
    binary = ""  # resolved in prepare()

    def __init__(self, repo_root: Path):
        super().__init__(repo_root)
        self._submodule = self.repo_root / "coding-agents" / "cli-agents" / "reasonix"
        self._binary_path: Path | None = None

    # ------------------------------------------------------------------
    def prepare(self, worktree: Path) -> None:
        """Idempotent: build bin/reasonix via `go build` when missing."""
        if not (self._submodule / "go.mod").is_file():
            raise PrepareError(f"reasonix submodule missing at {self._submodule}")

        candidate = self._submodule / "bin" / "reasonix"
        if not candidate.is_file():
            go = shutil.which("go")
            if go is None:
                raise PrepareError(
                    "reasonix: Go toolchain not found on PATH — required to build "
                    f"{candidate} (Makefile build target: CGO_ENABLED=0 go build "
                    "-o bin/reasonix ./cmd/reasonix)"
                )
            proc = subprocess.run(
                [go, "build", "-o", str(candidate), "./cmd/reasonix"],
                cwd=str(self._submodule),
                env={**os.environ, "CGO_ENABLED": "0"},
                capture_output=True,
                text=True,
                timeout=900,
            )
            if proc.returncode != 0 or not candidate.is_file():
                tail = (proc.stderr or proc.stdout or "").strip().splitlines()[-3:]
                raise PrepareError(
                    "go build failed for reasonix: " + " | ".join(tail)
                )
        self._binary_path = candidate

    # ------------------------------------------------------------------
    def run(self, worktree: Path, spec: TaskSpec) -> ProcSpec:
        assert self._binary_path is not None, "prepare() not called"
        argv = [
            str(self._binary_path),
            "run",                        # headless one-shot subcommand (cli.go:126-127)
            "--permission-mode", "workspace-write",  # unattended writes (cli.go:491)
        ]
        model = os.environ.get("LONGRUN_MODEL")
        if model:
            argv += ["--model", model]    # verified flag (cli.go:479)
        argv += ["--metrics", METRICS_REL]  # JSON usage summary (cli.go:482)
        argv.append(spec.task_prompt)     # positional prompt, VERBATIM (cli.go:558)
        return ProcSpec(
            argv=argv,
            cwd=Path(worktree),
            env={
                "GIT_TERMINAL_PROMPT": "0",
                "NO_COLOR": "1",
                "TERM": "dumb",
                # provider credentials injected by the runner via os.environ
            },
            artifacts=[METRICS_REL],
        )

    # ------------------------------------------------------------------
    def collect(self, worktree, outcome, proc, spec):
        tokens_in = tokens_out = tokens_cached = None
        turns = None
        cost_usd = None
        metrics_path = worktree / METRICS_REL
        if metrics_path.is_file():
            import json

            try:
                data = json.loads(metrics_path.read_text(encoding="utf-8"))
            except (OSError, ValueError):
                data = {}
            if isinstance(data, dict):
                if isinstance(data.get("prompt_tokens"), int):
                    tokens_in = data["prompt_tokens"]
                if isinstance(data.get("completion_tokens"), int):
                    tokens_out = data["completion_tokens"]
                if isinstance(data.get("cache_hit_tokens"), int):
                    tokens_cached = data["cache_hit_tokens"]
                if isinstance(data.get("steps"), int):
                    turns = data["steps"]
                if isinstance(data.get("cost"), (int, float)):
                    cost_usd = float(data["cost"])

        if tokens_in is None and tokens_out is None:
            chars = 0
            for p in (outcome.stdout_path, outcome.stderr_path):
                try:
                    chars += p.stat().st_size
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
            turns=turns,
            tokens_in=tokens_in,
            tokens_out=tokens_out,
            tokens_cached=tokens_cached,
            cost_usd=cost_usd,
            transcript_path=(
                str(metrics_path) if metrics_path.is_file() else None
            ),
            notes=(
                "reasonix --metrics JSON parsed"
                if cost_usd is not None or turns is not None
                else "reasonix: chars/4 estimate (no metrics file)"
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
    driver = ReasonixDriver(repo_root=Path(__file__).resolve().parents[3])
    driver._binary_path = (  # stub: no Go toolchain needed for argv construction
        driver._submodule / "bin" / "reasonix"
    )
    ps = driver.run(Path(tempfile.mkdtemp()), fake)
    print("argv:", ps.argv)
    print("env keys:", sorted(ps.env.keys()))
    print("artifacts:", ps.artifacts)
    assert ps.argv[-1] == "smoke test prompt", "prompt not verbatim"
    print("verbatim prompt OK")
