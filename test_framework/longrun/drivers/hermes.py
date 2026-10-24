"""hermes driver — NousResearch hermes-agent, single-file harness over run_agent.main.

Plan §Scope Ruling: hermes-agent is a LIBRARY → single-file harness. Source
verification (2026-10-07, submodule at hermes-agent, v2026.9.21-414-ge2f8a0731b):

- Entries (pyproject.toml:432-435): `hermes = "hermes_cli.main:main"` is the
  interactive CLI launcher (no subcommand → chat REPL, hermes_cli/main.py:
  3505-3509, argparse at :344); `hermes-agent = "run_agent:main"`. cli.py:855
  `class HermesCLI` is the interactive REPL (slash dispatch) — not used here.
- Console-script footgun: console scripts call main() with NO arguments, so
  `hermes-agent` would run run_agent.main's DEFAULT demo query (query=None →
  "Tell me about the latest developments in Python 3.13 ...", run_agent.py:
  1543-1544) — unusable for verbatim prompts.
- fire IS a declared dependency (`"fire==0.7.1"`, pyproject.toml:43; mirrored
  in uv.lock), so `python run_agent.py --query=...` would work. The harness
  still calls run_agent.main(query=..., model=..., max_turns=...) directly
  (_hermes_harness.py, sibling file): fire's argv scanning re-tokenizes a
  multi-KB verbatim prompt (flag-like substrings and legacy fire formatting
  inside the prompt text are exactly the fragility a benchmark must not
  inherit), a direct kwarg call passes the prompt with zero argv mangling,
  and the console-script demo-query footgun above stands independently.
- ONE prompt, non-interactive: run_agent.main (run_agent.py:1490-1494) takes
  query=..., builds ONE AIAgent (run_agent.py:1533-1538) and runs one
  conversation (agent.run_conversation, run_agent.py:1548) — no stdin read,
  no REPL. Tool calls execute inside the turn loop via
  model_tools.handle_function_call (agent/tool_executor.py:1637); there is
  NO approval prompt on this path (yolo_mode is a CLI/gateway SESSION
  concern, run_agent.py:329-335), so no auto-approve flag exists or is
  needed for run_agent.main.
- Model/provider mechanism: run_agent.py:1500-1503 — model is OpenRouter
  format "provider/model"; api_key falls back to the OPENROUTER_API_KEY env
  var; base_url defaults to https://openrouter.ai/api/v1. run() maps
  LONGRUN_MODEL (present AND non-empty) → harness --model → main(model=...).
  Credentials are never set by the driver: the runner injects them via
  os.environ, and hermes additionally loads ~/.hermes/.env at import time
  (run_agent.py:112-117; the home .env OVERRIDES stale shell exports —
  hermes_cli/env_loader.py:391-398). Mitigation on hosts with a stale
  ~/.hermes/.env: point HERMES_HOME at a scratch dir — the env passthrough
  (ProcSpec.env merges OVER os.environ) reroutes hermes' dotenv/state root.
- Missing keys are NOT a PrepareError: AIAgent construction raises
  RuntimeError when no provider is configured (agent/agent_init.py:882-888,
  "No LLM provider configured. Run `hermes model` ..."), and run_agent.main
  catches RuntimeError, prints "❌ Failed to initialize agent: ..." and
  RETURNS (run_agent.py:1539-1541) → the process still EXITS 0. The exit
  code cannot see this; the banner lands on stdout. Real runs must inject
  provider keys; a key-less invocation is a run-time config error, not a
  prepare-time tooling failure.
- max_turns: main's own default is 10 API iterations (run_agent.py:1491) —
  far below long-run budgets — so run() forwards spec.max_turns (the task
  fixture's declared iteration budget, e.g. gh-issue-001 = 150) →
  --max-turns → main(max_turns=...) → AIAgent(max_iterations=...)
  (run_agent.py:1535). Same field for every agent; no driver-side budgets.

prepare(): hermes-agent is a uv-managed PROJECT (pyproject [tool.uv] at
pyproject.toml:437 holds override-dependencies only; there is NO
[tool.uv.workspace] table) with a committed uv.lock and a setuptools
[build-system] (pyproject.toml:424-431). `uv sync --project <submodule>`
with UV_PROJECT_ENVIRONMENT pointed at
test_framework/longrun/_venvs/hermes (gitignored; platform tooling belongs
to the main checkout, run isolation applies to fixtures only) installs the
dependency tree into ONE venv; UV_PROJECT_ENVIRONMENT was live-verified
2026-10-07 (uv 0.10.8): the env is created exactly at the given path and no
<project>/.venv is created. uv is resolved via shutil.which — NEVER
Path.home() (uv 0.10.8 lives at ~/.cargo/bin/uv on this host;
~/.local/bin/uv does not exist; the kimi_cli.py:34 hardcoded path is the
known anti-pattern). Idempotent: skipped when <venv>/bin/python exists AND
`import run_agent` succeeds through that interpreter with cwd=hermes-agent
(module import per brief; the console script is deliberately NOT probed —
footgun above). Probe failures (nonzero exit, subprocess.TimeoutExpired,
OSError) fall through to (re)create the venv instead of escaping prepare()
(runner.run_one only catches PrepareError). Network AT PREPARE TIME ONLY.
PrepareError carries the stderr tail on failure.

collect(): run_agent.main prints a human transcript; its summary block
prints "Completed / API Calls / Messages" (run_agent.py:1550-1551). No
token usage is printed (the agent tracks session_total_tokens internally
but main() never emits it), so tokens use the chars/4 estimate (base.py
contract). turns are parsed ONLY inside the window between the LAST
"CONVERSATION SUMMARY" marker and the LAST "FINAL RESPONSE" marker — the
final answer is printed AFTER the summary (run_agent.py:1552-1553) and may
itself contain decoy "API Calls:" text, which this window excludes.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

from longrun.drivers.base import (
    STATUS_FAIL,
    STATUS_PARTIAL,
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

HARNESS_PATH = Path(__file__).resolve().parent / "_hermes_harness.py"
VENV_DIR = Path("test_framework") / "longrun" / "_venvs" / "hermes"
SUBMODULE_DIR = Path("hermes-agent")
SUMMARY_MARKER = "CONVERSATION SUMMARY"
FINAL_MARKER = "FINAL RESPONSE"
API_CALLS_PREFIX = "API Calls:"


class HermesDriver(DriverBase):
    name = "hermes"
    binary = ""  # resolved in prepare(): the venv's python interpreter

    def __init__(self, repo_root: Path):
        super().__init__(repo_root)
        self._submodule = self.repo_root / SUBMODULE_DIR
        self._venv = self.repo_root / VENV_DIR
        self._python: Path | None = None

    # ------------------------------------------------------------------
    def _import_probe(self) -> tuple[bool, str]:
        """`import run_agent` through the venv python (cwd=submodule).

        Returns (ok, diagnostic). Errors become diagnostics, never exceptions:
        the caller recreates the venv on any probe failure.
        """
        venv_python = self._venv / "bin" / "python"
        try:
            probe = subprocess.run(
                [str(venv_python), "-c", "import run_agent"],
                cwd=str(self._submodule),
                capture_output=True,
                text=True,
                timeout=120,
            )
        except (subprocess.TimeoutExpired, OSError) as e:
            return False, str(e)
        if probe.returncode == 0:
            return True, ""
        return False, (probe.stderr or probe.stdout or "").strip()

    # ------------------------------------------------------------------
    def prepare(self, worktree: Path) -> None:
        """Idempotent: UV_PROJECT_ENVIRONMENT venv via `uv sync --project`."""
        if not HARNESS_PATH.is_file():
            raise PrepareError(f"hermes harness missing at {HARNESS_PATH}")
        if not (self._submodule / "pyproject.toml").is_file() or not (
            self._submodule / "run_agent.py"
        ).is_file():
            raise PrepareError(f"hermes-agent submodule missing at {self._submodule}")

        if (self._venv / "bin" / "python").is_file():
            ok, diag = self._import_probe()
            if ok:
                self._python = self._venv / "bin" / "python"
                return
            if diag:
                tail = diag.strip().splitlines()[-3:]
                print(
                    "hermes: import probe failed, recreating venv: "
                    + " | ".join(tail),
                    file=sys.stderr,
                )

        uv = shutil.which("uv")
        if uv is None:
            raise PrepareError(
                "hermes: uv not found on PATH (this host: ~/.cargo/bin/uv; "
                "required for `uv sync --project hermes-agent`)"
            )
        venv_python = self._venv / "bin" / "python"
        try:
            proc = subprocess.run(
                [uv, "sync", "--project", str(self._submodule)],
                cwd=str(self.repo_root),
                env={**os.environ, "UV_PROJECT_ENVIRONMENT": str(self._venv)},
                capture_output=True,
                text=True,
                timeout=1800,  # cold start resolves the full locked dep tree
            )
        except (subprocess.TimeoutExpired, OSError) as e:
            # runner.run_one only catches PrepareError; a hung/failed sync
            # must degrade, not crash the runner.
            raise PrepareError(f"hermes: uv sync failed: {e}") from e
        if proc.returncode != 0 or not venv_python.is_file():
            tail = (proc.stderr or proc.stdout or "").strip().splitlines()[-3:]
            raise PrepareError(
                "hermes: uv sync failed for hermes-agent: " + " | ".join(tail)
            )

        ok, diag = self._import_probe()
        if not ok:
            tail = (diag or "import run_agent failed").strip().splitlines()[-3:]
            raise PrepareError(
                "hermes: post-sync `import run_agent` probe failed: "
                + " | ".join(tail)
            )
        self._python = venv_python

    # ------------------------------------------------------------------
    def run(self, worktree: Path, spec: TaskSpec) -> ProcSpec:
        """Build ProcSpec; LONGRUN_MODEL, when present and non-empty, maps to
        --model (empty LONGRUN_MODEL treated as unset). The prompt rides in a
        single `--prompt=<verbatim>` argv token: argparse takes everything
        after the first '=' as the value, so a leading '-' in the prompt
        cannot be flag-parsed (space-separated values starting with '-'
        would be rejected by argparse)."""
        assert self._python is not None, "prepare() not called"
        argv = [
            str(self._python),
            str(HARNESS_PATH),
            f"--prompt={spec.task_prompt}",  # verbatim, '='-joined channel
            "--max-turns", str(spec.max_turns),  # task fixture budget → main(max_turns=)
        ]
        model = os.environ.get("LONGRUN_MODEL")
        if model is not None and model != "":  # explicit: present and non-empty
            argv += ["--model", model]
        return ProcSpec(
            argv=argv,
            cwd=Path(worktree),
            env={
                "GIT_TERMINAL_PROMPT": "0",
                "NO_COLOR": "1",
                "TERM": "dumb",
                # hermes' file tools + context-file loader resolve against
                # TERMINAL_CWD in preference to the process cwd (source:
                # hermes_cli/kanban_db_dispatch.py:2823-2835 pins TERMINAL_CWD
                # to the task workspace for exactly this reason). Without it,
                # the first live run edited the parent-repo fixture template
                # instead of the worktree copy (caught by the runner's
                # fixture-drift guard on 2026-10-08).
                "TERMINAL_CWD": str(worktree),
                # provider credentials + optional HERMES_HOME injected by the
                # runner via os.environ (hermes also reads its own dotenv
                # chain at import — see module docstring)
            },
            artifacts=[],  # transcript is stdout; hermes state lives under HERMES_HOME
        )

    # ------------------------------------------------------------------
    @staticmethod
    def _parse_turns(stdout: str) -> int | None:
        """API-calls count from the LAST summary block, decoy-safe.

        run_agent.py:1550-1551 prints "📞 API Calls: N" inside the summary;
        the final answer (which may itself contain "API Calls:" decoy text)
        is printed AFTER it (run_agent.py:1552-1553). Parsing is bounded to
        the window [last CONVERSATION SUMMARY, last FINAL RESPONSE) so neither
        mid-transcript echoes nor the final answer can be mistaken for the
        summary. Absent/malformed markers → None (fallback stays chars/4).
        """
        start = stdout.rfind(SUMMARY_MARKER)
        if start < 0:
            return None
        end = stdout.rfind(FINAL_MARKER, start)
        window = stdout[start:end] if end > start else stdout[start:]
        idx = window.find(API_CALLS_PREFIX)
        if idx < 0:
            return None
        digits = window[idx + len(API_CALLS_PREFIX):].lstrip()
        n = ""
        for ch in digits:
            if ch.isdigit():
                n += ch
            else:
                break
        return int(n) if n else None

    # ------------------------------------------------------------------
    def collect(
        self, worktree: Path, outcome: ProcOutcome, proc: ProcSpec, spec: TaskSpec
    ) -> RunResult:
        try:
            stdout = outcome.stdout_path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            stdout = ""
        turns = self._parse_turns(stdout)

        chars = len(stdout)
        try:
            # decode stderr the same way so both streams are counted in
            # characters (st_size would mix bytes into a char count)
            chars += len(
                outcome.stderr_path.read_text(encoding="utf-8", errors="replace")
            )
        except OSError:
            pass

        if outcome.timed_out:
            status = STATUS_TIMEOUT
        elif outcome.exit_code == 0 and turns is None:
            # exit 0 alone is NOT trustworthy here: run_agent.main swallows
            # agent-init RuntimeError (no provider keys) and still exits 0
            # (run_agent.py:1539-1541). No summary block → nothing ran.
            status = STATUS_PARTIAL
        else:
            status = STATUS_PASS if outcome.exit_code == 0 else STATUS_FAIL

        return RunResult(
            platform=self.name,
            task_id=spec.id,
            status=status,
            exit_code=outcome.exit_code,
            wall_seconds=outcome.wall_seconds,
            turns=turns,
            tokens_in=estimate_tokens(chars),
            transcript_path=None,
            notes=(
                "hermes: chars/4 estimate"
                + (", turns from summary block" if turns is not None else "")
                + ("; NOTE exit 0 also occurs when agent init fails without "
                   "provider keys (run_agent.py:1539-1541 banner on stdout)"
                   if outcome.exit_code == 0 and turns is None else "")
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
        max_turns=150,
        acceptance={"method": "pytest", "command": "true", "pass_criteria": "exit 0"},
        cost_cap_usd=1.0,
        task_dir=Path(tempfile.mkdtemp()),
    )
    driver = HermesDriver(repo_root=Path(__file__).resolve().parents[3])
    driver._python = driver._venv / "bin" / "python"  # stub: no venv needed

    saved_model = os.environ.pop("LONGRUN_MODEL", None)
    ps = driver.run(Path(tempfile.mkdtemp()), fake)
    print("[LONGRUN_MODEL unset]")
    print("argv:", ps.argv)
    print("env keys:", sorted(ps.env.keys()))
    assert ps.argv[2] == "--prompt=smoke test prompt", "prompt not verbatim"
    assert "--model" not in ps.argv, "--model present without LONGRUN_MODEL"
    assert ps.argv[ps.argv.index("--max-turns") + 1] == "150", "max-turns wrong"

    os.environ["LONGRUN_MODEL"] = "openai/gpt-5.4"
    ps = driver.run(Path(tempfile.mkdtemp()), fake)
    print("[LONGRUN_MODEL=openai/gpt-5.4]")
    print("argv:", ps.argv)
    assert ps.argv[-2:] == ["--model", "openai/gpt-5.4"], "--model missing/wrong"

    if saved_model is not None:
        os.environ["LONGRUN_MODEL"] = saved_model
    else:
        del os.environ["LONGRUN_MODEL"]

    turns = HermesDriver._parse_turns(
        "noise\n== CONVERSATION SUMMARY ==\n✅ Completed: True\n"
        "📞 API Calls: 42\n💬 Messages: 9\n🎯 FINAL RESPONSE:\n"
        "decoy API Calls: 999\n"
    )
    assert turns == 42, f"turns parse broken: {turns}"
    assert HermesDriver._parse_turns("no summary here") is None
    print("verbatim prompt OK (equals-form --prompt); max-turns forwarded; "
          "decoy-safe turns parse OK")
