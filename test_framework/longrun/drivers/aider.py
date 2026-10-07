"""Aider driver — Python CLI with ready venv at coding-agents/cli-agents/aider.

Non-interactive invocation per plan §drivers:
    aider --yes-always --no-git --no-auto-commits [chat files...] \
        --message <prompt> --model <m>

One-shot `--message` mode with no chat files does NOT explore the repo: it
replies by asking the user to /add files (observed live: exit 0 in ~15s,
zero diff). run() therefore enumerates the worktree's text files and passes
them as positional chat-file arguments (see run() docstring for the
fairness rationale).

Token parsing: aider prints a usage summary line on exit, e.g.
    Tokens: 1.9k sent, 176 received. Cost: $0.00062 message, $0.00062 session.
We parse sent (tokens_in), received (tokens_out) and the SESSION cost
(cost_usd), accepting plain numbers, comma groups and k/m suffixes
("1.9k" -> 1900); the legacy "N tokens sent" style is kept as a fallback.
"""

from __future__ import annotations

import os
import re
import subprocess
from pathlib import Path, PurePosixPath

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

# Usage summary: "Tokens: 1.9k sent, 176 received." (aider >= 0.5x style).
_SUMMARY_RE = re.compile(
    r"Tokens?\s*:\s*"
    r"(?P<sent>[\d][\d,]*(?:\.\d+)?)\s*(?P<sent_suf>[kKmM]?)\s*sent\b\s*,\s*"
    r"(?P<recv>[\d][\d,]*(?:\.\d+)?)\s*(?P<recv_suf>[kKmM]?)\s*received\b",
    re.IGNORECASE,
)
# Session cost: "Cost: $0.00062 message, $0.00062 session." -> take session.
_SESSION_COST_RE = re.compile(
    r"Cost\s*:\s*\$[\d.]+\s*message\s*,\s*\$([\d.]+)\s*session\b", re.IGNORECASE
)
# Legacy style fallback: "1234 tokens sent, 567 tokens received".
_NUM = r"(?P<num>[\d][\d,]*(?:\.\d+)?)\s*(?P<suf>[kKmM]?)"
SENT_RE = re.compile(_NUM + r"\s*tokens?\s*sent\b", re.IGNORECASE)
RECEIVED_RE = re.compile(_NUM + r"\s*tokens?\s*received\b", re.IGNORECASE)

# Chat-file discovery: fixtures are tiny (<5K LOC) but one-shot aider never
# explores on its own, so we hand it the tree. Text-source extensions only —
# binary/irrelevant junk (.bin, .pyc, images, lockfiles) stays out.
_CHAT_FILE_EXTS = {
    ".py", ".md", ".txt", ".toml", ".cfg", ".ini", ".json",
    ".yaml", ".yml", ".ts", ".js", ".go", ".rs",
}
_CHAT_FILE_NAMES = {"Makefile"}
# Never add to the chat: git internals, hidden acceptance suite (must stay
# invisible to the agent pre-scoring), tool caches.
_CHAT_FILE_EXCLUDED_DIRS = {".git", "acceptance", "__pycache__", ".pytest_cache"}
_CHAT_FILE_CAP = 200


class AiderDriver(DriverBase):
    name = "aider"
    # resolved in prepare(): repo_root is only known at construction time
    binary = ""

    def __init__(self, repo_root: Path):
        super().__init__(repo_root)
        self._binary_path = (
            self.repo_root / "coding-agents" / "cli-agents" / "aider" / ".venv" / "bin" / "aider"
        )

    # ------------------------------------------------------------------
    def prepare(self, worktree: Path) -> None:
        if not self._binary_path.is_file():
            raise PrepareError(
                f"aider venv binary not found at {self._binary_path} "
                "(expected prebuilt venv per benchmark prerequisites)"
            )
        if not os.access(self._binary_path, os.X_OK):
            raise PrepareError(f"aider binary not executable: {self._binary_path}")

    # ------------------------------------------------------------------
    def run(self, worktree: Path, spec: TaskSpec) -> ProcSpec:
        """Launch aider in one-shot --message mode over the fixture tree.

        One-shot `aider --message` with NO chat files does not explore the
        repo on its own — it replies by asking the user to provide file
        paths (observed live: exit 0, zero diff, zero edits). To make the
        one-shot driver effective we enumerate the worktree's files (subprocess
        `git ls-files` — fixtures are git-inited by the runner; rglob fallback
        when git fails or returns nothing) and pass them as positional
        chat-file arguments before --message, excluding .git internals,
        acceptance/ (hidden tests must not be visible pre-scoring), caches
        (__pycache__, .pytest_cache) and binary/irrelevant junk, capped at
        200 files.

        Fairness rationale: this hands aider the same information an
        exploring agent would gather by itself — a task-level, not
        agent-level, information advantage. Every other agent is free to
        read the same tree; the benchmark contract only fixes the prompt,
        not how the platform reaches the code.
        """
        model = os.environ.get("LONGRUN_AIDER_MODEL", "gpt-5.2")
        argv = [
            str(self._binary_path),
            "--yes-always",
            "--no-git",
            "--no-auto-commits",
            "--no-check-update",
            "--no-suggest-shell-commands",
            "--no-fancy-input",
            *_list_chat_files(worktree),
            "--message", spec.task_prompt,
            "--model", model,
        ]
        return ProcSpec(
            argv=argv,
            cwd=Path(worktree),
            env={
                "GIT_TERMINAL_PROMPT": "0",
                "NO_COLOR": "1",
                "TERM": "dumb",
                # credentials injected by the runner via os.environ
            },
            artifacts=[".aider.chat.history.md", ".aider.input.history"],
        )

    # ------------------------------------------------------------------
    def collect(self, worktree, outcome, proc, spec):
        stdout = ""
        try:
            stdout = outcome.stdout_path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            pass

        tokens_in = tokens_out = None
        cost_usd = None
        m = _SUMMARY_RE.search(stdout)
        if m:
            tokens_in = _to_int(m.group("sent"), m.group("sent_suf"))
            tokens_out = _to_int(m.group("recv"), m.group("recv_suf"))
        else:
            m = SENT_RE.search(stdout)
            if m:
                tokens_in = _to_int(m.group("num"), m.group("suf"))
            m = RECEIVED_RE.search(stdout)
            if m:
                tokens_out = _to_int(m.group("num"), m.group("suf"))
        m = _SESSION_COST_RE.search(stdout)
        if m:
            cost_usd = float(m.group(1))
        if tokens_in is None and tokens_out is None:
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
            cost_usd=cost_usd,
            transcript_path=transcript,
            notes=(
                "aider usage summary parsed"
                if tokens_in is not None
                else "chars/4 estimate"
            ),
        )


def _to_int(number: str, suffix: str = "") -> int:
    """Parse an aider token count: plain, comma-grouped, or k/m-suffixed.

    "176" -> 176, "1,234" -> 1234, "1.9k" -> 1900, "19k" -> 19000,
    "1.2M" -> 1200000.
    """
    value = float(number.replace(",", ""))
    multiplier = {"": 1, "k": 1_000, "m": 1_000_000}.get(suffix.lower(), 1)
    return round(value * multiplier)


def _list_chat_files(worktree: Path) -> list[str]:
    """Relative text-file paths in `worktree` to feed aider as chat files.

    Order: `git ls-files` (authoritative for a git-inited fixture); falls
    back to rglob when git is unavailable or returns nothing. Filtered to
    text source extensions + Makefile; .git internals, acceptance/, caches
    and everything else excluded. Capped at _CHAT_FILE_CAP entries.
    """
    rels: list[str] = []
    try:
        res = subprocess.run(
            ["git", "-C", str(worktree), "ls-files"],
            capture_output=True,
            text=True,
            timeout=30,
            check=True,
        )
        rels = [line.strip() for line in res.stdout.splitlines() if line.strip()]
    except (OSError, subprocess.SubprocessError):
        rels = []
    if not rels:
        for p in sorted(worktree.rglob("*")):
            if p.is_file():
                rels.append(p.relative_to(worktree).as_posix())

    kept: list[str] = []
    for rel in rels:
        if len(kept) >= _CHAT_FILE_CAP:
            break
        parts = PurePosixPath(rel).parts
        if not parts or any(seg in _CHAT_FILE_EXCLUDED_DIRS for seg in parts):
            continue
        if parts[-1] in _CHAT_FILE_NAMES:
            kept.append(rel)
            continue
        if Path(rel).suffix.lower() in _CHAT_FILE_EXTS:
            kept.append(rel)
    return kept


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
    driver = AiderDriver(repo_root=Path(__file__).resolve().parents[3])
    ps = driver.run(Path(tempfile.mkdtemp()), fake)
    print("argv:", ps.argv)
    print("env keys:", sorted(ps.env.keys()))
    print("cwd:", ps.cwd)
