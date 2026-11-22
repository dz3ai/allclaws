"""goclaw driver — GoClaw gateway agent in one-shot `agent chat -m` mode.

GoClaw is GATEWAY-CENTRIC: `goclaw agent chat` is a WebSocket client to a
running gateway daemon, not a standalone CLI (cmd/agent_chat.go:44
"Chat with an agent via the running gateway"; without one it exits
"the gateway must be running"). This driver therefore owns three pieces
of platform state in prepare() — the gateway process, the provider +
agent registry entries, and the workspace symlink — while the per-run
process remains runner-owned (contract: drivers never manage per-run
processes; the gateway is shared infrastructure, same role as nanobot's
internal gateway).

Verified live 2026-11-22 against the fleet router (probe transcript in
/tmp/opencode/goclaw-probe):

- Binary: `go build -tags sqlite` from the pinned submodule — the DEFAULT
  build is postgres-only and exits demanding GOCLAW_POSTGRES_DSN even with
  GOCLAW_STORAGE_BACKEND=sqlite (cmd/gateway_stores_sqlite.go:1 build tag).
  modernc.org/sqlite makes the tagged build pure-Go (no cgo).
- Gateway: `GOCLAW_CONFIG=<cfg> GOCLAW_STORAGE_BACKEND=sqlite goclaw`
  (bare invocation = foreground gateway). Config pins
  gateway.host/port (default 127.0.0.1:18923 for the benchmark).
- Provider registry is DB state, NOT config: config.json providers only
  feed fallbacks. POST /v1/providers {name, provider_type: "openai_compat",
  api_key, base_url, enabled} (internal/store/provider_store.go:13
  ProviderOpenAICompat = "openai_compat"; "openai" is rejected).
- Agent: POST /v1/agents {agent_key: "default", agent_type: "predefined",
  provider: "openai_compat", model}. Both POSTs need the
  `X-GoClaw-User-Id` header (internal/http error otherwise).
- Workspace: the agent's file tools operate under
  ~/.goclaw/workspace/<agent_key>/ws/system/ — the trailing segment is the
  chat OWNER ("system" for direct CLI chat), independent of the -s session
  key (verified: -s bench and -s bench2 both wrote via ws/system). The
  driver re-points ws/system as a symlink to the task worktree in
  prepare(); writes follow the link (verified: file landed in the
  worktree, not beside the link).
- Context isolation across runs: the CLI's auto session key is
  deterministic (BuildSessionKey(agent, "cli", PeerDirect, "local")), so
  repeated runs would share one conversation. The driver passes a unique
  -s <run-key> per invocation.
- Model: no --model flag; the driver honors LONGRUN_GOCRAW_MODEL /
  LONGRUN_MODEL (provider prefix stripped) by re-POSTing the agent with
  the new model in prepare() (per-batch model pinning).
- collect(): stdout lists `[tool] <name>` lines per tool call (observed:
  "[tool] list_files", "[tool] write_file") → turns = count + 1; no token
  summary is printed → estimate_tokens chars/4 fallback.
"""

from __future__ import annotations

import json
import os
import re
import socket
import subprocess
import time
import urllib.error
import urllib.request
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

_GOCRAW_PORT = 18923
_BASE = f"http://127.0.0.1:{_GOCRAW_PORT}"
_HEADERS = {"Content-Type": "application/json", "X-GoClaw-User-Id": "longrun-bench"}
_WORKSPACE_LINK = Path.home() / ".goclaw" / "workspace" / "default" / "ws" / "system"


def _http(method: str, path: str, body: dict | None = None, timeout: float = 15) -> tuple[int, dict | list | None]:
    req = urllib.request.Request(
        _BASE + path,
        data=json.dumps(body).encode() if body is not None else None,
        headers=_HEADERS,
        method=method,
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read()
            return resp.status, (json.loads(raw) if raw else None)
    except urllib.error.HTTPError as e:
        return e.code, None
    except (urllib.error.URLError, socket.timeout, ConnectionError):
        return 0, None


def _port_open() -> bool:
    with socket.socket() as s:
        s.settimeout(1.0)
        return s.connect_ex(("127.0.0.1", _GOCRAW_PORT)) == 0


class GoclawDriver(DriverBase):
    name = "goclaw"

    def __init__(self, repo_root: Path):
        super().__init__(repo_root)
        self._repo = self.repo_root / "goclaw"
        self._binary = self._repo / ".gobuild" / "goclaw"
        self._config = self._repo / ".gobuild" / "longrun-config.json"
        self._turns_re = re.compile(r"^\s*\[tool\]\s+(\S+)", re.MULTILINE)

    # ------------------------------------------------------------------
    def prepare(self, worktree: Path) -> None:
        gobuild = self._repo / ".gobuild"
        if not self._binary.is_file():
            gobuild.mkdir(parents=True, exist_ok=True)
            env = {**os.environ, "GOPROXY": "https://goproxy.cn,direct"}
            # -tags sqlite is load-bearing: default build is postgres-only
            # (module docstring).
            r = subprocess.run(
                ["go", "build", "-tags", "sqlite", "-o", str(self._binary), "."],
                cwd=self._repo, env=env, capture_output=True, text=True, timeout=1200,
            )
            if r.returncode != 0:
                raise PrepareError(f"goclaw build failed: {r.stderr[-500:]}")

        # Benchmark gateway config. Endpoint rides the CONFIG PROVIDER
        # FALLBACK (gateway_http_wiring.go: SetAPIBaseFallback) — DB
        # provider instances shadow it AND their base_url does not persist
        # through POST /v1/providers (verified live: a DB instance sent the
        # request to api.openai.com), so the driver keeps the DB clean and
        # pins everything via config. Rewritten whenever the tier env
        # changes; a running gateway reads config only at boot, so the
        # driver restarts it after a rewrite.
        base_url = os.environ.get("OPENAI_API_BASE", "")
        api_key = os.environ.get("OPENAI_API_KEY", "none")
        if not base_url:
            raise PrepareError(
                "goclaw: OPENAI_API_BASE not set — source longrun/<tier>_model.env first"
            )
        model_pre = (os.environ.get("LONGRUN_GOCRAW_MODEL") or os.environ.get("LONGRUN_MODEL") or "")
        model_pre = model_pre.rsplit("/", 1)[-1] or "qwen3-coder-30b"
        config_body = {
            "gateway": {"host": "127.0.0.1", "port": _GOCRAW_PORT},
            "providers": {"openai": {"api_key": api_key, "api_base": base_url}},
            # agents.defaults is what made the probe work: it registers the
            # config provider with the agent resolver when the DB registry
            # is empty ("no providers configured for agent" otherwise).
            "agents": {"defaults": {"provider": "openai", "model": model_pre}},
        }
        stamp = gobuild / "config.stamp"
        config_changed = not (self._config.is_file() and stamp.is_file()
                              and stamp.read_text() == json.dumps(config_body, sort_keys=True))
        if config_changed:
            self._config.write_text(json.dumps(config_body, indent=2))
            stamp.parent.mkdir(parents=True, exist_ok=True)
            stamp.write_text(json.dumps(config_body, sort_keys=True))

        # Gateway up? (shared infra; started detached, survives the grid.
        # Restart on config change — the fallback binds at boot. The
        # restart WAITS for the old process to finish draining: a dying
        # gateway still holds the port and serves "no providers" errors.)
        if _port_open() and config_changed:
            subprocess.run(["pkill", "-x", "goclaw"], check=False)
            for _ in range(30):
                if not _port_open():
                    break
                time.sleep(0.5)
            time.sleep(1.0)
        if not _port_open():
            env = {
                **os.environ,
                "GOCLAW_CONFIG": str(self._config),
                "GOCLAW_STORAGE_BACKEND": "sqlite",
            }
            subprocess.Popen(
                [str(self._binary)],
                cwd=gobuild, env=env,
                stdout=(gobuild / "gateway.log").open("ab"),
                stderr=subprocess.STDOUT,
                start_new_session=True,
            )
        for _ in range(30):
            if _port_open():
                break
            time.sleep(1.0)
        else:
            raise PrepareError(f"goclaw gateway did not listen on {_GOCRAW_PORT} (see {gobuild}/gateway.log)")

        # Provider registry: keep it EMPTY of OpenAI-compatible instances —
        # any DB instance shadows the config fallback and loses its
        # base_url (module docstring). The benchmark gateway is exclusively
        # ours, so sweep them all.
        code, providers = _http("GET", "/v1/providers")
        for p in (providers or {}).get("providers", []):
            if p.get("provider_type") in ("openai_compat", "openai") and p.get("id"):
                _http("DELETE", f"/v1/providers/{p['id']}")

        # Agent: provider "openai" resolves through the config fallback
        # (probe-verified: zero DB providers + agent provider "openai" +
        # config api_base = requests reach the tier endpoint). Model honors
        # the tier pin (prefix stripped — the router routes BY model id and
        # 404s "local/..." forms). POST is create-only; agents with session
        # history cannot be DELETEd (500, FK). PUT takes partial updates
        # and force-sets restrict_to_workspace=true (verified live) —
        # which locks the agent inside the symlinked workspace.
        model = model_pre
        agent_body = {
            "agent_key": "default",
            "display_name": "default",
            "agent_type": "predefined",
            "provider": "openai",
            "model": model,
        }
        code, _ = _http("POST", "/v1/agents", agent_body)
        if code == 409:
            code, agents = _http("GET", "/v1/agents")
            ags = agents.get("agents", []) if isinstance(agents, dict) else (agents or [])
            ag_id = next((a.get("id") for a in ags if a.get("agent_key") == "default"), None)
            if ag_id:
                code, _ = _http("PUT", f"/v1/agents/{ag_id}",
                                {"model": model, "provider": "openai"})
        if code not in (200, 201):
            raise PrepareError(f"goclaw: agent create/refresh failed ({code})")

        # Workspace binding: ws/system -> this run's worktree (module
        # docstring; verified live). Idempotent re-point per run.
        _WORKSPACE_LINK.parent.mkdir(parents=True, exist_ok=True)
        if _WORKSPACE_LINK.is_symlink() or _WORKSPACE_LINK.exists():
            if _WORKSPACE_LINK.is_symlink() and os.readlink(_WORKSPACE_LINK) == str(worktree):
                return
            _WORKSPACE_LINK.unlink()
        _WORKSPACE_LINK.symlink_to(worktree, target_is_directory=True)

    # ------------------------------------------------------------------
    def run(self, worktree: Path, spec: TaskSpec) -> ProcSpec:
        # Unique session per invocation: the CLI's auto key is deterministic
        # and would share one conversation across runs (module docstring).
        session = f"longrun-{os.getpid()}-{int(time.time())}"
        argv = [
            str(self._binary),
            "agent", "chat",
            "-m", spec.task_prompt,
            "-s", session,
        ]
        return ProcSpec(
            argv=argv,
            cwd=Path(worktree),
            env={
                "GIT_TERMINAL_PROMPT": "0",
                "NO_COLOR": "1",
                "TERM": "dumb",
                "GOCLAW_CONFIG": str(self._config),
                "GOCLAW_STORAGE_BACKEND": "sqlite",
            },
            artifacts=[],
        )

    # ------------------------------------------------------------------
    def collect(self, worktree, outcome, proc, spec):
        stdout = ""
        stderr = ""
        try:
            stdout = outcome.stdout_path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            pass
        try:
            stderr = outcome.stderr_path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            pass

        # [tool] progress lines ride STDERR (verified live: 35 [tool] lines
        # on a passing gh-issue-001 run, zero on stdout); final answer on
        # stdout.
        tool_calls = len(self._turns_re.findall(stdout)) + len(self._turns_re.findall(stderr))
        turns = tool_calls + 1 if tool_calls else None

        size = 0
        for p in (outcome.stdout_path, outcome.stderr_path):
            try:
                size += p.stat().st_size
            except OSError:
                pass
        tokens_in = estimate_tokens(size)

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
            tokens_out=None,
            notes=f"gateway-workspace=symlink tool_calls={tool_calls}",
        )
