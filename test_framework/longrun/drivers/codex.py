"""Codex driver — Node CLI in monorepo at coding-agents/cli-agents/codex.

Entry resolution (verified in earlier benchmark work, re-checked in prepare):
the repo root is `private: true` with no bin; the real CLI lives in
`codex-cli/` — we read its package.json bin field at prepare() time.

Non-interactive mode: `codex exec --json` (NDJSON event stream on stdout).
Sandbox: workspace-write so the agent can edit the worktree but stay off
the network. Model pin via LONGRUN_CODEX_MODEL env (driver reads, never
hardcodes) — passed with --model when the exec subcommand supports it.
"""

from __future__ import annotations

import json
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

DEFAULT_ENTRY = Path("codex-cli") / "codex.js"


class CodexDriver(DriverBase):
    name = "codex"
    binary = "node"  # argv[0]; real entry resolved in prepare()

    def __init__(self, repo_root: Path):
        super().__init__(repo_root)
        self._submodule = self.repo_root / "coding-agents" / "cli-agents" / "codex"
        self._entry: Path | None = None
        self._exec_supports_model = False

    # ------------------------------------------------------------------
    def prepare(self, worktree: Path) -> None:
        if not (self._submodule / "package.json").is_file():
            raise PrepareError(f"codex submodule missing at {self._submodule}")
        self._entry = self._resolve_entry()
        if self._entry is None:
            raise PrepareError("could not resolve codex CLI entry (no bin in codex-cli/package.json)")
        if not self._entry.is_file():
            raise PrepareError(f"codex entry not found: {self._entry}")
        if not self._which("node"):
            raise PrepareError("node not found on PATH")
        # probe exec flags once from source (cheap, offline)
        src = ""
        cli_rs = self._submodule / "codex-rs" / "exec" / "src" / "cli.rs"
        pkg = self._submodule / "codex-cli"
        for probe in (cli_rs,):
            try:
                src += probe.read_text(encoding="utf-8", errors="replace")
            except OSError:
                pass
        # TypeScript fallback probe
        for js in pkg.rglob("codex.js"):
            try:
                src += js.read_text(encoding="utf-8", errors="replace")[:20000]
            except OSError:
                pass
            break
        self._exec_supports_model = bool(re.search(r"--model", src))

    def _resolve_entry(self) -> Path | None:
        pkg_dir = self._submodule / "codex-cli"
        manifest = pkg_dir / "package.json"
        if manifest.is_file():
            try:
                data = json.loads(manifest.read_text(encoding="utf-8"))
                bin_field = data.get("bin")
                if isinstance(bin_field, str):
                    return pkg_dir / bin_field
                if isinstance(bin_field, dict) and bin_field:
                    return pkg_dir / next(iter(bin_field.values()))
            except (json.JSONDecodeError, OSError):
                pass
        fallback = self._submodule / DEFAULT_ENTRY
        return fallback if fallback.is_file() else None

    # ------------------------------------------------------------------
    def run(self, worktree: Path, spec: TaskSpec) -> ProcSpec:
        assert self._entry is not None, "prepare() not called"
        argv = [
            "node",
            str(self._entry),
            "exec",
            "--json",
            "--skip-git-repo-check",
            "-C", str(worktree),
            "--sandbox", "workspace-write",
        ]
        model = os.environ.get("LONGRUN_CODEX_MODEL")
        if model and self._exec_supports_model:
            argv += ["--model", model]
        argv.append(spec.task_prompt)
        return ProcSpec(
            argv=argv,
            cwd=Path(worktree),
            env={
                "GIT_TERMINAL_PROMPT": "0",
                "NO_COLOR": "1",
                "TERM": "dumb",
            },
            artifacts=[],
        )

    # ------------------------------------------------------------------
    def collect(self, worktree, outcome, proc, spec):
        tokens_in = tokens_out = None
        turns = None
        session_id = None
        events = 0
        try:
            text = outcome.stdout_path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            text = ""

        for line in text.splitlines():
            line = line.strip()
            if not line.startswith("{"):
                continue
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            events += 1
            session_id = session_id or event.get("session_id") or (
                event.get("info") or {}).get("session_id") or event.get("thread_id")
            usage = event.get("token_usage") or event.get("usage") or (
                (event.get("info") or {}).get("total_token_usage")
            )
            if isinstance(usage, dict):
                got_in = usage.get("input_tokens") or usage.get("prompt_tokens")
                got_out = usage.get("output_tokens") or usage.get("completion_tokens")
                if got_in is not None:
                    tokens_in = int(got_in) + (tokens_in or 0)
                    if "cached" in str(usage):
                        pass
                if got_out is not None:
                    tokens_out = int(got_out) + (tokens_out or 0)
                cached = usage.get("cached_input_tokens") or usage.get("cache_read_input_tokens")
                if cached:
                    pass
            if event.get("type") in ("item.completed", "item_complete"):
                turns = (turns or 0) + 1

        if tokens_in is None and tokens_out is None:
            tokens_in = estimate_tokens(len(text))

        if outcome.timed_out:
            status = STATUS_TIMEOUT
        else:
            status = STATUS_PASS if outcome.exit_code == 0 else STATUS_FAIL

        extra_notes = []
        if session_id:
            extra_notes.append(f"session {session_id[:8]}")
        if self._exec_supports_model is False:
            extra_notes.append("exec --model not detected in source; model via env only")

        return RunResult(
            platform=self.name,
            task_id=spec.id,
            status=status,
            exit_code=outcome.exit_code,
            wall_seconds=outcome.wall_seconds,
            turns=turns,
            tokens_in=tokens_in,
            tokens_out=tokens_out,
            notes="; ".join(extra_notes) or "codex NDJSON parsed",
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
    driver = CodexDriver(repo_root=Path(__file__).resolve().parents[3])
    driver.prepare(Path(tempfile.mkdtemp()))
    ps = driver.run(Path(tempfile.mkdtemp()), fake)
    print("argv:", ps.argv)
    print("env keys:", sorted(ps.env.keys()))
