"""openclaw driver — OpenClaw `agent exec` headless one-shot mode.

`openclaw agent exec` is purpose-built for reproducible headless runs
(openclaw.mjs agent exec --help: "Run one isolated headless embedded agent
turn"): positional prompt, `--cwd` binds BOTH the agent workspace and the
tool working directory, `--config <path>` pins the whole run to a config
file, `--json` emits a stable envelope, `--timeout` is the agent deadline.
No gateway daemon is needed (embedded agent).

Verified live 2026-11-22 against the fleet router (v2026.9.5, pinned
submodule @ e914feb, dist/ built via `pnpm build`):

- Provider wiring follows the canonical custom-endpoint recipe from
  docs/providers/vllm.md: models.providers.<name> = { baseUrl, apiKey
  "${OPENAI_API_KEY}", api: "openai-completions", timeoutSeconds, models:
  [{id, ...}] }. The driver writes a tier config (from OPENAI_API_BASE /
  OPENAI_API_KEY / LONGRUN_MODEL env) into openclaw/.benchbuild/ and
  passes --config (mutually exclusive with --isolated — verified error
  "--config cannot be combined with --isolated").
- `--model fleet/<bare-id>`: the router routes BY model id, so the tier
  pin's provider prefix is stripped and re-attached as the config provider
  key (LONGRUN_OPENCLAW_MODEL overrides LONGRUN_MODEL).
- Envelope (stdout JSON): ok/status/final/payloads/assistantTurns/model/
  provider/sessionId — assistantTurns drives turns; NO token usage is
  reported (verified), so tokens use the estimate_tokens chars/4 fallback.
- Each exec gets a fresh sessionId — no cross-run context pollution.
- ACP bridge "dispose hook failed" warnings on stderr after the envelope
  are post-run teardown noise (verified on a successful OK reply); the
  JSON envelope's "ok" is the source of truth, exit code follows it.
- contextWindow in the generated model entry defaults to 65536 (the
  fleet's smallest window; the router truncates server-side anyway).
"""

from __future__ import annotations

import json
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


class OpenclawDriver(DriverBase):
    name = "openclaw"

    def __init__(self, repo_root: Path):
        super().__init__(repo_root)
        self._repo = self.repo_root / "openclaw"
        self._entry = self._repo / "openclaw.mjs"
        self._bench = self._repo / ".benchbuild"
        self._config = self._bench / "longrun-config.json5"

    # ------------------------------------------------------------------
    def prepare(self, worktree: Path) -> None:
        if not self._entry.is_file():
            raise PrepareError(f"openclaw entry not found: {self._entry}")
        if not (self._repo / "dist").is_dir():
            raise PrepareError(
                f"openclaw dist/ missing — run `pnpm install && pnpm build` in {self._repo} "
                "(benchmark prerequisite; build takes ~10 min)"
            )
        if subprocess.run(["which", "node"], capture_output=True).returncode != 0:
            raise PrepareError("node not on PATH (openclaw requires node >= bundled .nvmrc)")

        base_url = os.environ.get("OPENAI_API_BASE", "")
        if not base_url:
            raise PrepareError(
                "openclaw: OPENAI_API_BASE not set — source longrun/<tier>_model.env first"
            )
        model = (os.environ.get("LONGRUN_OPENCLAW_MODEL")
                 or os.environ.get("LONGRUN_MODEL") or "")
        model = model.rsplit("/", 1)[-1] or "qwen3-coder-30b"

        self._bench.mkdir(parents=True, exist_ok=True)
        self._config.write_text(json.dumps({
            "models": {
                "providers": {
                    "fleet": {
                        "baseUrl": base_url,
                        "apiKey": "${OPENAI_API_KEY}",
                        "api": "openai-completions",
                        "timeoutSeconds": 300,
                        "models": [{
                            "id": model,
                            "name": f"{model} (longrun tier)",
                            "reasoning": False,
                            "input": ["text"],
                            "cost": {"input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0},
                            "contextWindow": 65536,
                            "maxTokens": 8192,
                        }],
                    },
                },
            },
        }, indent=2))
        self._model = model

    # ------------------------------------------------------------------
    def run(self, worktree: Path, spec: TaskSpec) -> ProcSpec:
        argv = [
            str(self._entry),
            "agent", "exec",
            "--config", str(self._config),
            "--cwd", str(worktree),
            "--model", f"fleet/{self._model}",
            "--json",
            "--timeout", str(int(spec.timeout_seconds)),
            spec.task_prompt,
        ]
        return ProcSpec(
            argv=argv,
            cwd=Path(worktree),
            env={
                "GIT_TERMINAL_PROMPT": "0",
                "NO_COLOR": "1",
                "TERM": "dumb",
                # apiKey "${OPENAI_API_KEY}" resolves from the process env
                "OPENAI_API_KEY": os.environ.get("OPENAI_API_KEY", "none"),
            },
            artifacts=[],
        )

    # ------------------------------------------------------------------
    def collect(self, worktree, outcome, proc, spec):
        stdout = ""
        try:
            stdout = outcome.stdout_path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            pass

        # Envelope is the FIRST top-level JSON object on stdout; teardown
        # noise follows after (module docstring).
        turns = None
        ok = None
        start, end = stdout.find("{"), stdout.rfind("}")
        if start >= 0 and end > start:
            try:
                env = json.loads(stdout[start:end + 1])
                turns = env.get("assistantTurns") or None
                ok = env.get("ok")
            except json.JSONDecodeError:
                pass

        size = 0
        for p in (outcome.stdout_path, outcome.stderr_path):
            try:
                size += p.stat().st_size
            except OSError:
                pass
        tokens_in = estimate_tokens(size)

        if outcome.timed_out:
            status = STATUS_TIMEOUT
        elif ok is True:
            status = STATUS_PASS
        elif ok is False:
            status = STATUS_FAIL
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
            tokens_out=None,
            notes=f"envelope ok={ok}" if ok is not None else "envelope unparsed",
        )
