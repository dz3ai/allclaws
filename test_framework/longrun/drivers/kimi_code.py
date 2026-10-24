"""kimi-code 2.0 driver — installed native CLI (MoonshotAI/kimi-code submodule).

Successor of the archived kimi-cli (drivers/kimi_cli.py, unmodified). Source
verification (2026-10-07, submodule coding-agents/kimi-code, app version
2.0.2 per apps/kimi-code/package.json "version"; installed binary
~/.kimi-code/bin/kimi reports 0.34.0):

- Entry chain: src/main.ts:87-88 — when validateOptions() sets
  uiMode='print' (src/cli/options.ts:120, iff --prompt is present) main()
  awaits runPrompt(), which forwards to the native v2 runner runV2Print()
  (src/cli/run-prompt.ts:40-47).
- One-shot flag: `-p, --prompt <prompt>` — "Run one prompt non-interactively
  and print the response." (src/cli/commands.ts:63-68). The driver passes
  the equals form `--prompt=<verbatim>`: commander takes everything after
  the first '=' as the value (equals-form parsing covered in
  test/cli/options.test.ts:251-253), so a leading '-' in the prompt cannot
  be flag-parsed — the same decoy-safe channel as the hermes driver.
- No approval flag exists for prompt mode: --yolo/--auto/--plan all raise
  OptionConflictError with --prompt (src/cli/options.ts:79-87). Print mode
  is autonomous by itself — runV2Print forces the agent's permission mode
  to 'auto' (src/cli/v2/run-v2-print.ts:481 on fresh sessions, forceAuto()
  at :407-418 on resume paths).
- Deterministic text output: `--output-format <text|stream-json>` is
  prompt-mode-only (src/cli/options.ts:76-78) and an ambient
  KIMI_MODEL_OUTPUT_FORMAT env would otherwise pick the format
  (resolveOutputFormat, src/cli/options.ts:16-34 — explicit flag wins over
  env). run() pins --output-format=text so stdout is the plain transcript
  regardless of host environment.
- Model: `-m, --model <model>` — "LLM model alias ... Defaults to
  default_model in config.toml" (src/cli/commands.ts:57-62); applied via
  applyModelOverride -> profile.setModel (run-v2-print.ts:392-397) and
  fresh-session requireConfiguredModel(opts.model, defaultModel)
  (run-v2-print.ts:470). run() maps LONGRUN_MODEL (present AND non-empty)
  to --model=<alias>; empty string is treated as unset so the CLI falls
  back to its config default.
- Credentials/config: the built-in kimi provider reads the KIMI_API_KEY env
  (packages/agent-core-v2/src/llm-adapter/provider/provider-definition.ts:44
  `apiKeyEnv: 'KIMI_API_KEY'`; packages/kosong/src/providers/kimi.ts:432);
  the state home is $KIMI_CODE_HOME else ~/.kimi-code
  (packages/agent-core-v2/src/app/bootstrap/bootstrap.ts:168-172
  resolveKimiHome; config.toml resolved at :174-176). The driver never
  reads or writes credentials — the runner injects env and host auth
  (~/.kimi-code/) is honored as-is.
- No structured usage in the -p surface: text mode writes assistant/
  thinking blocks only (PromptTranscriptWriter, src/cli/prompt-render.ts:101-147);
  stream-json mode emits assistant/tool lines plus meta lines
  turn.step.retrying / session.resume_hint / system.version
  (prompt-render.ts:89-99, :149-267, :358-370) — none carry token usage.
  collect() therefore uses the chars/4 estimate (base.py contract).

prepare(): the CLI is a preinstalled native binary (no build step, no venv).
Resolution order: shutil.which("kimi") first; fallback candidate
<KIMI_CODE_HOME or ~/.kimi-code>/bin/kimi — the install layout observed on
this host, expressed through the SAME root the CLI itself honors
(resolveKimiHome above) and resolved from the environment at call time,
never a hardcoded Path.home() literal (known anti-pattern, see the hermes
driver docstring). Anything found is probed with `kimi --version` under
try/except (subprocess.TimeoutExpired, OSError); the probe is advisory
(opencode precedent) and never escapes prepare() — only a missing binary
raises PrepareError.
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
    ProcOutcome,
    ProcSpec,
    RunResult,
    estimate_tokens,
)
from longrun.spec import TaskSpec


class KimiCodeDriver(DriverBase):
    name = "kimi_code"
    binary = "kimi"  # PATH-resolved in prepare(); known-location fallback

    def __init__(self, repo_root: Path):
        super().__init__(repo_root)
        self._binary_path: str | None = None
        self.version: str | None = None

    # ------------------------------------------------------------------
    def _known_location(self) -> Path:
        """Install-root candidate: $KIMI_CODE_HOME else ~/.kimi-code.

        Mirrors the CLI's own resolveKimiHome precedence
        (bootstrap.ts:168-172) so a relocated install is still found; the
        path is derived from the environment, never hardcoded.
        """
        root = os.environ.get("KIMI_CODE_HOME") or os.path.expanduser(
            "~/.kimi-code"
        )
        return Path(root) / "bin" / "kimi"

    # ------------------------------------------------------------------
    def prepare(self, worktree: Path) -> None:
        """Idempotent: resolve the CLI, probe `--version` (non-fatal)."""
        exe = shutil.which(self.binary)
        if exe is None:
            candidate = self._known_location()
            if candidate.is_file():
                exe = str(candidate)
        if exe is None:
            raise PrepareError(
                "kimi_code: CLI not found (shutil.which('kimi') missed and "
                f"known location {self._known_location()} absent)"
            )
        try:
            proc = subprocess.run(
                [exe, "--version"],
                capture_output=True,
                text=True,
                timeout=30,
            )
        except (subprocess.TimeoutExpired, OSError) as e:
            # version probe is advisory; a hang here must not kill the runner
            self.version = None
            del e
        else:
            self.version = (
                (proc.stdout or proc.stderr or "").strip() or None
                if proc.returncode == 0
                else None
            )
        self._binary_path = exe

    # ------------------------------------------------------------------
    def run(self, worktree: Path, spec: TaskSpec) -> ProcSpec:
        """Build ProcSpec; LONGRUN_MODEL (present and non-empty) maps to
        --model=<alias> (empty string treated as unset -> config default)."""
        assert self._binary_path is not None, "prepare() not called"
        argv = [
            self._binary_path,
            f"--prompt={spec.task_prompt}",  # verbatim, '='-joined channel
            "--output-format=text",  # pin: beats ambient KIMI_MODEL_OUTPUT_FORMAT
        ]
        model = os.environ.get("LONGRUN_MODEL")
        if model is not None and model != "":  # explicit: present and non-empty
            argv += [f"--model={model}"]
        return ProcSpec(
            argv=argv,
            cwd=Path(worktree),
            env={
                "GIT_TERMINAL_PROMPT": "0",
                "NO_COLOR": "1",
                "TERM": "dumb",
                # KIMI_API_KEY / host auth injected by the runner via os.environ
            },
            artifacts=[],  # transcript is stdout; sessions live under ~/.kimi-code
        )

    # ------------------------------------------------------------------
    def collect(
        self, worktree: Path, outcome: ProcOutcome, proc: ProcSpec, spec: TaskSpec
    ) -> RunResult:
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

        version = f"kimi-code {self.version}; " if self.version else ""
        return RunResult(
            platform=self.name,
            task_id=spec.id,
            status=status,
            exit_code=outcome.exit_code,
            wall_seconds=outcome.wall_seconds,
            tokens_in=estimate_tokens(chars),
            notes=(
                f"{version}chars/4 estimate (no usage in -p output; "
                "prompt-render.ts emits no token events)"
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
    driver = KimiCodeDriver(repo_root=Path(__file__).resolve().parents[3])
    driver._binary_path = shutil.which("kimi") or "kimi"  # stub: argv build only

    saved_model = os.environ.pop("LONGRUN_MODEL", None)
    ps = driver.run(Path(tempfile.mkdtemp()), fake)
    print("[LONGRUN_MODEL unset]")
    print("argv:", ps.argv)
    print("env keys:", sorted(ps.env.keys()))
    assert ps.argv[1] == "--prompt=smoke test prompt", "prompt not verbatim"
    assert "--output-format=text" in ps.argv, "output format not pinned"
    assert not any(a.startswith("--model") for a in ps.argv), (
        "--model present without LONGRUN_MODEL"
    )

    os.environ["LONGRUN_MODEL"] = ""
    ps = driver.run(Path(tempfile.mkdtemp()), fake)  # empty treated as unset
    assert not any(a.startswith("--model") for a in ps.argv), ps.argv

    os.environ["LONGRUN_MODEL"] = "kimi-k2-turbo"
    ps = driver.run(Path(tempfile.mkdtemp()), fake)
    print("[LONGRUN_MODEL=kimi-k2-turbo]")
    print("argv:", ps.argv)
    assert ps.argv[-1] == "--model=kimi-k2-turbo", "--model missing/wrong"

    if saved_model is not None:
        os.environ["LONGRUN_MODEL"] = saved_model
    else:
        os.environ.pop("LONGRUN_MODEL", None)

    print("verbatim prompt OK (equals-form --prompt); output-format pinned; "
          "model mapping OK")
