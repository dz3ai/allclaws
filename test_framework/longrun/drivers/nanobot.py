"""nanobot driver — NanoBot CLI in one-shot --message mode.

Contract mapping (verified against nanobot v0.3.5, pinned submodule at
nanobot/ @ 74942bd1, editable venv install):

- Binary: nanobot/.venv/bin/nanobot (prepare() checks; venv is a benchmark
  prerequisite, same doctrine as aider's prebuilt venv).
- One-shot: `nanobot agent --message <prompt>` — nanobot/cli/agent.py:55.
  With --message the native TUI is skipped entirely (agent.py:79
  `native_tui = message is None and not classic`), so no TTY is needed;
  runner sets stdin=/dev/null which the classic prompt path tolerates.
- Workspace binding: `--workspace/-w <dir>` (agent.py:57) — the agent's
  file tools operate in the given directory, which is how the task
  worktree is bound. NanoBot creates bootstrap files (AGENTS.md,
  HEARTBEAT.md, memory/) in a fresh workspace on first use — observed
  live 2026-11-22; harmless for acceptance (runner scores via pytest on
  the worktree; the extra dotfiles don't affect the hidden tests).
- Model/provider: config-file doctrine (like kimi-code/reasonix) — nanobot
  has NO --model flag; provider/model live in ~/.nanobot/config.json
  (providers.<name>.apiBase + modelPresets + agents.defaults.modelPreset).
  The tier wires the fleet router there (local_model.env documents it);
  this driver reads the configured model for metadata via `nanobot status`
  once per grid in prepare().
- LONGRUN_MODEL contract: nanobot ignores it (documented divergence —
  same class as kimi-code reading bare aliases). The runner still stamps
  it into ledger metadata; per-batch model switching requires editing
  ~/.nanobot/config.json.
- Usage parsing: the one-shot classic output does not print a token
  summary (verified live); collect() falls back to estimate_tokens()
  chars/4 on the transcript, the contract-sanctioned path.
"""

from __future__ import annotations

import os
import re
import subprocess
from pathlib import Path

from longrun.drivers.base import (
    DriverBase,
    PrepareError,
    ProcSpec,
    RunResult,
    STATUS_FAIL,
    STATUS_PASS,
    STATUS_TIMEOUT,
    estimate_tokens,
)
from longrun.spec import TaskSpec


class NanobotDriver(DriverBase):
    name = "nanobot"

    def __init__(self, repo_root: Path):
        super().__init__(repo_root)
        self._binary_path = (
            self.repo_root / "nanobot" / ".venv" / "bin" / "nanobot"
        )
        self._model_label = ""

    # ------------------------------------------------------------------
    def prepare(self, worktree: Path) -> None:
        if not self._binary_path.is_file():
            raise PrepareError(
                f"nanobot venv binary not found at {self._binary_path} "
                "(expected editable venv per benchmark prerequisites)"
            )
        if not os.access(self._binary_path, os.X_OK):
            raise PrepareError(f"nanobot binary not executable: {self._binary_path}")
        # Resolve the configured model once for metadata; failure is
        # non-fatal (status is advisory, the run itself surfaces config
        # problems loudly).
        try:
            out = subprocess.run(
                [str(self._binary_path), "status"],
                capture_output=True, text=True, timeout=60,
                env={**os.environ, "NO_COLOR": "1", "TERM": "dumb"},
            )
            m = re.search(r"(?:model|Model)[:=]\s*([^\s,]+)", out.stdout)
            if m:
                self._model_label = m.group(1)
        except Exception:
            pass

    # ------------------------------------------------------------------
    def run(self, worktree: Path, spec: TaskSpec) -> ProcSpec:
        argv = [
            str(self._binary_path),
            "--classic",
            "--no-markdown",
            "--workspace", str(worktree),
            "--message", spec.task_prompt,
        ]
        return ProcSpec(
            argv=argv,
            cwd=Path(worktree),
            env={
                "GIT_TERMINAL_PROMPT": "0",
                "NO_COLOR": "1",
                "TERM": "dumb",
                # model/provider credentials resolved by nanobot from
                # ~/.nanobot/config.json (config-file doctrine; see module
                # docstring — no shell credential overrides are honoured)
            },
            artifacts=[".nanobot-transcript.txt"],
        )

    # ------------------------------------------------------------------
    def collect(self, worktree, outcome, proc, spec):
        stdout = ""
        try:
            stdout = outcome.stdout_path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            pass

        # NanoBot's one-shot output carries no token summary (module
        # docstring); contract-sanctioned chars/4 estimate over stdout+stderr.
        tokens_in = tokens_out = None
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
            notes=f"model={self._model_label}" if self._model_label else "model=config-default",
        )
