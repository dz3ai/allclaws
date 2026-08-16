---
layout: post
title: "How 17 AI Agent Platforms Present Themselves: A CLI Command Comparison"
date: 2026-08-12 17:00:00 +0800
author: Danny Zeng
categories: [Research, Comparison]
tags: [cli, command-interface, agent-platform, comparison, ux, developer-experience]
---

Every AI agent platform has a different answer to the same question: **how does a user interact with you?** Some give you a single command and a chat loop. Some give you 80 subcommands. Some give you a TUI, some a REPL, some just print text to stdout.

After running `--help` on every available CLI and reading the source code of the ones we couldn't install, here is a structured comparison of how 17 AI agent platforms present their capabilities to users — and what those choices reveal about their design philosophy.

---

## Methodology

I captured live `--help` output from five platforms installed on this system (Hermes, kimi-cli, zeroclaw, opencode, reasonix), and extracted CLI architecture details from source code and documentation for the remaining platforms tracked in the AllClaws architecture docs. Each platform's entry covers:

- **Command name**: What you type to start it
- **Subcommand count**: How many distinct commands are available
- **Invocation modes**: REPL, TUI, one-shot, pipe-friendly, etc.
- **Configuration approach**: Flags, config files, interactive setup
- **Operational commands**: Cron, monitoring, debugging, backup
- **Session management**: Resume, history, export

---

## The Comparison

### 1. Hermes-Agent (`hermes`)

**Language:** Python | **Version:** v0.20.0 | **Subcommands:** 81+

Hermes has the most extensive CLI of any platform tracked. Running `hermes --help` produces ~14,000 characters of output covering 81 positional subcommands and dozens of flags.

**Invocation modes:**
- `hermes` — Classic REPL (prompt_toolkit)
- `hermes --tui` — Modern terminal UI
- `hermes -z "prompt"` — One-shot mode (stdout only, no banner, no spinner, intended for scripts/pipes)
- `hermes -w` — Isolated git worktree mode (for parallel agents)
- `hermes -s skill1,skill2` — Preload skills

**Key subcommands by category:**

| Category | Commands |
|----------|----------|
| Core | `chat`, `model`, `fallback`, `moa`, `secrets` |
| Auth & Credentials | `auth`, `login`, `logout`, `egress` |
| Messaging | `gateway`, `send`, `whatsapp`, `whatsapp-cloud`, `slack`, `webhook`, `portal` |
| Scheduling | `cron`, `pause`, `resume` |
| Project Mgmt | `kanban`, `project`, `tasks` |
| Skills & Plugins | `skills`, `bundles`, `plugins`, `curator` |
| Memory & Learning | `memory`, `journey`, `learning`, `memory-graph` |
| Infrastructure | `proxy`, `lsp`, `mcp`, `computer-use`, `acp` |
| Monitoring | `status`, `logs`, `sessions`, `insights`, `monitoring`, `dashboard` |
| Ops & Debug | `doctor`, `verify`, `security`, `approvals`, `dump`, `debug`, `backup`, `checkpoints`, `import` |
| Config & Profile | `config`, `profile`, `skin`, `completion`, `hooks` |
| Desktop & GUI | `dashboard`, `serve`, `desktop`, `gui` |

**Design philosophy:** "Everything is a subcommand." Hermes treats its CLI as the primary interface to every feature — messaging, scheduling, skills, memory, monitoring, desktop GUI, MCP servers, security audit. The CLI is the control plane. There is no distinction between "user-facing features" and "admin features" — it's all one namespace.

**Notable design choices:**
- `-z` one-shot mode writes only final response to stdout (pipe-friendly, CI-compatible)
- `--usage-file` for cost tracking in scripted runs
- `--safe-mode` disables all customizations (troubleshooting)
- `--yolo` bypasses all approval prompts
- `--worktree` creates an isolated git worktree for parallel agents
- ACP server mode (`hermes acp`) for IDE integration

---

### 2. OpenClaw (`openclaw`)

**Language:** TypeScript | **Entry Point:** `src/cli` | **Stars:** ~340K

OpenClaw's CLI was not directly testable (the npm binary launches a TUI that times out from WSL), but the architecture docs reveal its structure.

**Architecture:**
- Entry point via `src/cli`, commands in `src/commands`
- Single-agent architecture with channel/plugin extensions
- 37+ messaging channels (Telegram, Discord, Slack, Signal, iMessage, Web, etc.)
- Extensions system for additional platforms (MSTeams, Matrix)

**Design philosophy:** "Be the channel." OpenClaw is fundamentally a routing platform — it takes input from any channel, processes it through an AI agent, and outputs to any channel. The CLI is one of many channels, not the primary one. The architecture emphasizes `src/provider-web.ts` and `src/routing` over `src/commands`.

**CLI character:** Minimal and focused. OpenClaw's CLI exists to configure channels, start the agent loop, and manage plugins. It does not attempt to be a general-purpose control plane. The 37+ channels are the differentiator, not the command count.

---

### 3. ClawTeam (`clawteam`)

**Language:** Python 3.10+ | **Architecture:** Multi-agent (Leader-Worker)

ClawTeam's CLI is the most domain-specific of any platform — every subcommand maps to a multi-agent workflow concept.

**Key subcommand groups:**

| Group | Commands | Purpose |
|-------|----------|---------|
| Team lifecycle | `team spawn-team`, `team cleanup` | Create/destroy agent teams |
| Agent spawning | `spawn` | Launch workers via tmux |
| Task management | `task create`, `task update`, `task wait` | Manage tasks with dependency chains |
| Inter-agent messaging | `inbox send`, `inbox broadcast` | P2P and broadcast communication |
| Monitoring | `board show`, `board live`, `board serve` | Kanban board, live view, web UI |
| Workspace | `workspace checkpoint`, `workspace merge` | Git worktree management |

**Design philosophy:** "Orchestrate agents, don't be one." ClawTeam's CLI is a team management interface, not an agent chat interface. You don't talk to an AI through ClawTeam — you spawn a team of agents that talk to each other. The CLI subcommands mirror the workflow: create a team, define tasks, watch the board, merge the results.

**Notable:** Uses TOML team templates (`clawteam launch hedge-fund --team fund1`) for reproducible team configurations. ZeroMQ P2P option for cross-machine coordination. The kanban board (`board live`) provides a tmux tiled view of all agents simultaneously.

---

### 4. GoClaw (`goclaw`)

**Language:** Go 1.26 | **Entry Point:** `cmd/goclaw/main.go` | **Binary size:** ~25MB

GoClaw's CLI reflects its identity as a gateway server — the primary command launches the gateway, and subcommands manage the infrastructure around it.

**Inferred CLI structure** (from `cmd/` module analysis):
- Gateway startup (primary command — WS + HTTP server)
- Onboarding wizard
- Migration tools
- Configuration management (JSON5 + env vars)

**Design philosophy:** "Single binary, full stack." GoClaw ships as one ~25MB Go binary that includes the gateway server, agent loop, provider integrations, and management tools. The CLI is the deployment tool. You run `goclaw` to start the gateway, then interact with agents through the web dashboard, WebSocket RPC, or HTTP API (`/v1/chat/completions`, `/v1/agents`, `/v1/skills`).

**CLI character:** Infrastructure-oriented. Unlike Hermes (which exposes everything as subcommands) or ClawTeam (which exposes orchestration as subcommands), GoClaw's CLI is about deployment and configuration. The agent interaction happens through the gateway's RPC and HTTP interfaces, not through CLI subcommands. This is consistent with its enterprise focus — you don't SSH into a production server to chat with an agent.

---

### 5. IronClaw (`ironclaw`)

**Language:** Rust | **Entry Point:** `src/main.rs`

IronClaw's CLI architecture emphasizes security primitives and sandbox management.

**Channel structure:**
- REPL (primary interaction)
- HTTP webhooks
- WASM channels (dynamic tool loading)
- Web gateway (SSE/WebSocket)

**Design philosophy:** "Security first, CLI as one of many channels." IronClaw treats the REPL as a channel alongside HTTP webhooks and WASM channels — not as the primary interface. The architecture emphasizes the sandbox orchestrator (Docker), tool registry (built-in + MCP + WASM), and safety layer (prompt injection defense, credential injection at host boundary).

---

### 6. ZeroClaw (`zeroclaw`)

**Language:** Rust | **Version:** 0.1.7 | **Stars:** ~29K | **RAM:** <5MB | **Cold start:** <10ms

ZeroClaw has the most *consistent* CLI of any platform — clean, well-structured, Rust clap-based help output with examples for every subcommand.

**Subcommands (22):**

| Category | Commands |
|----------|----------|
| Core agent | `onboard`, `agent`, `daemon`, `service` |
| Gateway & channels | `gateway`, `channel`, `integrations` |
| Scheduling | `cron` (list, add, add-at, add-every, once, remove, update, pause, resume) |
| Memory & skills | `memory`, `skills` (list, audit, install, remove) |
| Models & providers | `models`, `providers`, `auth` |
| Hardware | `hardware`, `peripheral` (STM32, RPi GPIO) |
| Ops | `status`, `doctor`, `estop`, `config`, `completions`, `migrate` |

**Design philosophy:** "Fast, small, complete." ZeroClaw's CLI is notable for its balance — 22 subcommands covering the full agent lifecycle (onboarding, agent loop, daemon, scheduling, skills, hardware, monitoring) without the sprawl of Hermes' 81+ commands. Every subcommand has examples in its `--help` output.

**Notable design choices:**
- `agent -m "prompt"` for single-shot without entering interactive mode
- `estop` for emergency stop of the daemon and channels
- Hardware peripheral support (STM32, RPi GPIO) — unique in the ecosystem
- `daemon` as a first-class command (gateway + channels + heartbeat + scheduler as a single long-running process)

---

### 7. OpenCode (`opencode`)

**Language:** TypeScript | **Version:** v1.18.18 | **Stars:** ~198K

OpenCode is "the open source coding agent" — a TUI-first coding assistant with ACP and MCP support, plus a unique headless server mode for remote collaboration.

**Subcommands (21):**

| Category | Commands |
|----------|----------|
| Core | `opencode [project]` (TUI, default), `run [message..]`, `attach <url>` |
| Server | `serve` (headless), `web` (server + browser UI) |
| Protocol | `acp` (ACP server), `mcp` (MCP management) |
| Providers & Models | `providers` (a.k.a. `auth`), `models [provider]` |
| GitHub | `github` (GitHub agent), `pr <number>` (fetch PR branch, then TUI) |
| Session | `session` (manage), `export [sessionID]`, `import <file>` |
| Agent & Plugins | `agent` (manage agents), `plugin <module>` (install & configure) |
| Ops | `debug`, `stats` (token usage/cost), `db`, `upgrade`, `uninstall`, `completion` |

**Invocation modes:**
- `opencode` — Launch TUI (default)
- `opencode run "prompt"` — Run with a message (non-interactive)
- `opencode serve` — Headless server
- `opencode web` — Server + browser UI
- `opencode attach <url>` — Connect to remote server
- `opencode --mini` — Minimal interactive interface
- `opencode -c` / `-s <id>` — Continue last or specific session

**Notable design choices:**
- `--fork` to fork a session when continuing (branch from a previous state)
- `--pure` to run without external plugins
- `--mdns` for mDNS service discovery on local network (find running instances)
- `--cors` for cross-origin configuration on the headless server
- `--auto` to auto-approve any permission not explicitly denied (the documented-dangerous mode)
- `--port` / `--hostname` to bind the server explicitly; `--mdns-domain` to customize discovery
- `--replay-limit` to cap mini-mode session replay on resume
- `pr <number>` fetches a GitHub PR branch then launches the TUI — a workflow-specific command no other platform has
- `stats` for token usage and cost tracking as a first-class command

**Design philosophy:** "TUI-first, server-optional." OpenCode's default experience is a TUI, but it uniquely offers both a headless `serve` mode and a `web` mode with browser UI. The `attach <url>` command and mDNS discovery suggest a design that supports both local development and remote collaboration — you can run opencode on a server and attach to it from your laptop. The `pr` command bridges GitHub workflow into the agent loop, treating PR review as a first-class use case.

---

### 8. Nanobot (`nanobot`)

**Language:** Python 3.11+ | **Stars:** ~37K | **Entry Point:** `nanobot/__main__.py` (Typer)

Nanobot takes the "ultra-lightweight" philosophy into its CLI design.

**Architecture:**
- CLI via Python Typer (auto-generated help from type hints)
- Single-agent with subagent support
- 8+ channels (Telegram, Discord, Slack, WhatsApp, Feishu, QQ, Email, Matrix, CLI)
- MCP bridge (available but not core)
- LiteLLM for multi-provider support

**Design philosophy:** "One command, one agent." Nanobot's CLI is minimal because the platform itself is minimal (~4,000 LOC core). Typer provides good help output automatically from type annotations. The focus is on `pip install nanobot-ai` and immediate usability, not comprehensive subcommand coverage.

---

### 9. Maxclaw (`maxclaw`)

**Language:** Go 1.24+ | **Stars:** ~189 | **Binaries:** `maxclaw`, `maxclaw-gateway`

Maxclaw ships two binaries — one for the agent, one for the gateway.

**Architecture:**
- `cmd/main.go` — Agent CLI with sub-session spawning
- `maxclaw-gateway` — Separate gateway binary
- Desktop UI + Web UI on same port
- Monorepo context discovery (AGENTS.md, CLAUDE.md)
- Layered memory (MEMORY.md, HISTORY.md, heartbeat.md)

**Design philosophy:** "Local-first with visual interfaces." Maxclaw uniquely bundles a desktop UI and web UI on the same port. The CLI is one interface alongside visual ones. Sub-session spawning enables parallel agents within a single maxclaw instance.

---

### 10. NanoClaw (`nanoclaw`)

**Language:** TypeScript (Node.js) | **Entry Point:** `src/index.ts`

NanoClaw is the most container-centric platform — its "CLI" is fundamentally an orchestrator process.

**Architecture:**
- Single Node.js orchestrator process
- Claude Agent SDK running in isolated containers per group
- Per-group CLAUDE.md for memory
- IPC watcher for inter-process communication
- Task scheduler
- WhatsApp as primary channel

**Design philosophy:** "Containers, not commands." NanoClaw's CLI is an IPC orchestrator that spawns containerized agent instances. The "commands" are container lifecycle management — start, stop, monitor. There is no REPL in the traditional sense; you interact through WhatsApp groups, each with an isolated Claude agent in its own container.

---

### 11. HiClaw (`hiclaw`)

**Language:** Go + Shell | **Deployment:** Docker Compose / Kubernetes

HiClaw is the only platform to use Kubernetes-style declarative resources.

**Architecture:**
- `hiclaw` CLI with Docker Compose
- YAML resource definitions (Worker, Team, Human)
- Worker template marketplace
- Nacos-based skill discovery
- Manager-Workers runtime (CoPaw)

**Design philosophy:** "Declarative infrastructure for agents." HiClaw's CLI is closest to `kubectl` — you define workers, teams, and human-in-the-loop resources as YAML files and apply them. The CLI manages resource lifecycle rather than agent interaction. This is the enterprise-automation paradigm taken to its logical conclusion: agents are Kubernetes resources.

---

### 12. Hermes-Agent (Source Analysis vs Live Capture)

The architecture docs describe Hermes as a simpler platform than what the live `--help` reveals. The docs note:
- Entry point: `hermes` CLI
- Architecture: Single-agent with context management
- MCP native integration

The live CLI (v0.20.0) shows a platform that has evolved far beyond "single-agent with context management" into a full-featured agent operating system with 81+ subcommands spanning messaging, scheduling, skills, memory, monitoring, desktop GUI, and MCP server management.

---

### 13. aider (`aider`)

**Language:** Python | **Stars:** ~68K | **Entry Point:** `aider` CLI

aider is the most focused CLI — it does one thing (code editing with AI) and does it through a chat interface.

**Architecture:**
- REPL pair-programming loop
- Git-aware (auto-commits with sensible messages)
- Edit modes: Whole Edit, Diff Edit, Architect
- Repo Map for large codebase context
- 20+ LLM providers

**Design philosophy:** "Pair programming, not a platform." aider has no subcommands for scheduling, skills, messaging, or monitoring. It's a chat loop with git integration. You talk, it edits code, git commits the result. The minimalism is the point — 68K stars from doing one thing extremely well.

---

### 14. Claude Code (`claude`)

**Language:** TypeScript (Anthropic) | **Entry Point:** `claude`

Claude Code is Anthropic's official CLI coding agent. Not directly testable from WSL (launches a TUI that times out).

**Architecture:**
- Terminal-based coding agent
- ACP protocol support
- Sandboxed execution
- Interactive approval loop

**Design philosophy:** "Anthropic's terminal agent." Claude Code is the reference implementation of Anthropic's vision for terminal-based AI coding. It follows the pattern of minimal CLI surface — you run `claude`, it starts a session, you code. The simplicity is by design.

---

### 15. kimi-cli (`kimi-cli`)

**Language:** Python | **Stars:** ~8.8K | **Version:** 1.24.0

kimi-cli from MoonshotAI has the most *options-dense* help of any platform relative to its subcommand count.

**Invocation modes:**
- `kimi-cli` — Interactive agent (default)
- `kimi-cli -p "prompt"` / `-c "prompt"` — Single prompt
- `kimi-cli --print` — Print mode (non-interactive, implies `--yolo`)
- `kimi-cli --quiet` — Shorthand for `--print --output-format text --final-message-only`
- `kimi-cli --acp` — ACP server mode (deprecated, now `kimi-cli acp`)
- `kimi-cli --wire` — Wire server (experimental)

**Subcommands (9):**

| Command | Purpose |
|---------|---------|
| `login` / `logout` | Account management |
| `term` | Toad TUI backed by Kimi Code ACP server |
| `acp` | ACP server |
| `info` | Version and protocol info |
| `export` | Session data export |
| `mcp` | MCP server configuration management |
| `vis` | Agent tracing visualizer |
| `web` | Web interface |

**Notable design choices:**
- `--agent [default|okabe]` and `--agent-file FILE` for custom agent specifications
- `--input-format [text|stream-json]` and `--output-format [text|stream-json]` for pipe integration
- `--mcp-config-file FILE` (repeatable) for multiple MCP configs
- `--skills-dir DIRECTORY` for skills discovery
- `--thinking` / `--no-thinking` for reasoning mode toggle
- `--max-steps-per-turn`, `--max-retries-per-step`, `--max-ralph-iterations` for fine-grained control

**Design philosophy:** "Configurable agent, multiple interfaces." kimi-cli provides the most granular per-invocation configuration of any platform. Every aspect of the agent's behavior can be tuned via flags — model, thinking mode, step limits, retry limits, MCP configs, agent specification, skills directory. The three interface modes (interactive, print, wire/ACP) and the agent tracing visualizer (`vis`) suggest a platform designed for both end-user coding and developer tooling.

---

### 16. Codex (`codex`)

**Language:** Rust | **Stars:** ~86.9K | **Entry Point:** `codex` CLI

OpenAI's Codex is the most starred CLI agent and the simplest architecturally.

**Architecture:**
- Simple CLI → LLM → Shell execution loop
- Sandboxed execution (all code runs in isolated environments)
- Single binary, zero runtime overhead
- Models: GPT-4o, o3, o4-mini

**Design philosophy:** "Single binary, single loop." Codex is the anti-Hermes. One command, one loop, sandboxed execution, done. No subcommands for skills, scheduling, messaging, or monitoring. The sandbox is the differentiator — every code execution is isolated, making it safe for CI/CD pipelines.

---

### 17. Reasonix (`reasonix` / `dsnix`)

**Language:** TypeScript | **Version:** v0.52.0 | **Stars:** ~34.6K | **Entry Point:** `dist/cli/index.js` | **Cold start:** ~287ms

Reasonix (esengine/DeepSeek-Reasonix) is the "DeepSeek-native coding agent" — and the only platform in this comparison with **two command names**: both `reasonix` and `dsnix` map to the same binary. Its CLI philosophy is built around one economic idea: DeepSeek's context cache. Subcommands exist to make cache hit rates visible and steerable.

**Subcommands (19):**

| Category | Commands |
|----------|----------|
| Setup & health | `setup` (interactive wizard), `doctor`, `doctor-cache`, `update`, `version` |
| Core chat | `chat` (Ink TUI with live cache/cost panel), `code [dir]` (coding chat with filesystem tools) |
| Non-interactive | `run <task>` (streaming one-shot), `desktop` (headless JSON-RPC for desktop client) |
| ACP | `acp` (Agent Client Protocol over stdio NDJSON) |
| Observability | `stats [transcript]` (usage dashboard), `events <name>` (kernel event log pretty-printer), `replay <transcript>` (transcript browser TUI), `diff <a> <b>` (side-by-side transcript comparison) |
| Sessions | `sessions`, `prune-sessions` (delete idle ≥N days, `--dry-run`), `-c/--continue`, `-r/--resume`, `-n/--new` |
| Cost & data | `commit` (draft commit messages from staged diff), `mcp` (MCP discovery + setup test), `index` (local semantic search index) |

**Design philosophy:** "Cost as a first-class citizen." Reasonix is the only CLI here with a **session dollar budget built into the invocation**: `--budget <usd>` warns at 80% and *refuses the next turn* at 100% (not just warns — a hard gate). The `chat` TUI shows a live cache-hit/cost panel while you type, `stats` turns historical transcripts into a usage dashboard, and `doctor-cache` is a dedicated health check for cache stability. Where kimi-cli makes every *behavior* configurable, Reasonix makes every *cost dimension* visible: budget caps, per-transcript accounting, cache health. It's the economics-first counterpart to kimi-cli's configuration-first design.

**Notable design choices:**
- `--budget <usd>` — per-session spend cap with 80% warning and hard refusal at 100%
- `--effort low|medium|high|max` — reasoning-effort dial on every invocation mode
- `--no-mouse` — disables SGR mouse tracking to restore native terminal selection (a pain point no other CLI addresses)
- `--no-proxy` — per-run proxy bypass, useful behind GFW-adjacent networks
- `--dashboard-port` / `--dashboard-host` — stable port + LAN binding for the embedded web dashboard (SSH-tunnel friendly)
- `--mcp <spec>` repeatable with `--mcp-prefix` to namespace tool names
- `--profile` — records a V8 CPU profile for perf-bug reports
- Bilingual help output (Chinese descriptions with English command names)
- `diff <a> <b>` — the only CLI that can *diff two agent transcripts* side-by-side
- `dry-run` flag on `code` for ssh:// targets — parse the URI, check local SSH, print planned steps, execute nothing

**Cross-links:** Reasonix implements one-shot (`run`), TUI (`chat`), ACP server (`acp`), MCP management (`mcp`), session resume (`-c`/`-r`), and self-update (`update`) — the same six capability points as Hermes and OpenCode, in a fraction of the codebase.


---

## Cross-Platform Analysis

### Subcommand Count Spectrum

```
Hermes       ████████████████████████████████████████████  81+
OpenCode     ████████████████████████  21
ZeroClaw     ██████████████████  22
Reasonix     ██████████████████  19
kimi-cli     ████████  9
ClawTeam     ████████  ~8 groups
GoClaw       █████  ~5
codex        ██  1-2
aider        ██  1
```

### Invocation Mode Matrix

| Platform | REPL | TUI | One-shot | Print/Pipe | Git worktree | ACP server | Wire protocol |
|----------|------|-----|----------|------------|-------------|------------|---------------|
| **Hermes** | Yes | Yes | `-z` | Yes | `-w` | `acp` | No |
| **OpenCode** | No | Yes | `run` | No | `--fork` | `acp` | No |
| **kimi-cli** | Yes | `term` | `-p` | `--print` / `--quiet` | No | `acp` | `--wire` |
| **Reasonix** | No | `chat`/`code` | `run` | No | No | `acp` | `desktop` JSON-RPC |
| **ZeroClaw** | Yes | No | `-m` | No | No | No | No |
| **aider** | Yes | No | No | No | No | No | No |
| **codex** | Yes | No | No | No | No | No | No |
| **OpenClaw** | Yes | No | No | No | No | No | No |
| **ClawTeam** | No | No | No | No | Per-agent | No | No |
| **GoClaw** | No | No | No | No | No | No | RPC |

### Configuration Approach

| Approach | Platforms | Notes |
|----------|-----------|-------|
| Flags-first | kimi-cli, ZeroClaw | Every option is a CLI flag, config files optional |
| Flags-first, cost-aware | Reasonix | Every option is a flag plus per-session `--budget` caps |
| Config-file-first | GoClaw, HiClaw | JSON5/YAML config files, CLI for overrides |
| Interactive-first | Hermes, OpenClaw | `setup` wizard, then config file |
| Zero-config | ClawTeam, Nanobot | Works immediately after install |
| Env-vars | IronClaw, NanoClaw | Environment variables for secrets |

### Operational Commands Coverage

| Capability | Hermes | ZeroClaw | kimi-cli | OpenCode | ClawTeam | GoClaw | aider | codex | Reasonix |
|-----------|--------|----------|----------|----------|----------|--------|-------|-------|----------|
| Cron/scheduling | Yes | Yes | No | No | Yes (tasks) | Yes | No | No | No |
| Monitoring/dashboard | Yes | Yes | Yes (vis) | Yes (stats) | Yes (board) | Yes | No | No | Yes (stats + web dashboard) |
| Session resume | Yes | No | Yes (`-S`, `-C`) | Yes (`-c`, `-s`) | No | No | No | No | Yes (`-c`, `-r`) |
| Session export | Yes | No | Yes (`export`) | Yes (`export`) | No | No | No | No | Yes (`--transcript` JSONL) |
| Cost/budget cap | No | No | No | No | No | No | No | No | Yes (`--budget`) |
| Backup/restore | Yes | Yes (migrate) | No | No | No | No | No | No | No |
| Doctor/debug | Yes | Yes | No | Yes (`debug`) | No | No | No | No | Yes (`doctor`, `doctor-cache`) |
| Security audit | Yes | No | No | No | No | Yes | No | No | No |
| MCP management | Yes | No | Yes (`mcp`) | Yes (`mcp`) | No | Yes | No | No | Yes (`mcp`) |
| Skills/plugins | Yes | Yes | Yes (`--skills-dir`) | Yes (`plugin`) | No | Yes | No | No | No |
| Shell completion | Yes | Yes | No | Yes (`completion`) | No | No | No | No | No |

---

## What the CLI Reveals About Platform Philosophy

### The Unix Philosophy Spectrum

**Hermes** is at one extreme: "Do everything through the CLI." 81+ subcommands, every feature exposed, from `hermes dashboard` to `hermes pets`. The CLI IS the platform.

**Codex and aider** are at the other extreme: "Do one thing through the CLI." A chat loop, git integration, done. The CLI is a thin shell around the core agent loop.

**ZeroClaw** and **kimi-cli** occupy the middle ground: enough subcommands to cover the agent lifecycle (scheduling, skills, monitoring) without the sprawl. ZeroClaw's 22 commands and kimi-cli's 9 commands + rich flag set suggest a deliberate design constraint — enough to be useful, not enough to be overwhelming.

### The "Operating System" vs "Tool" Divide

Hermes, ZeroClaw, and GoClaw behave like operating systems for agents — they manage the full lifecycle: installation, configuration, scheduling, monitoring, debugging, backup, update. Their CLIs reflect this: `doctor`, `backup`, `update`, `migrate`, `estop`.

aider, codex, and Claude Code behave like tools — you run them when you need them, they do their job, they exit. No daemon, no scheduler, no backup. Their CLIs reflect this: minimal surface, focused interaction.

ClawTeam occupies a unique position: it's an operating system for *other* agents, not for itself. Its CLI manages teams of aider/Codex/OpenClaw instances. It doesn't have an AI chat loop — it has team lifecycle management.

### The Convergence Pattern

Three CLI patterns are converging across the ecosystem:

1. **One-shot mode** (Hermes `-z`, kimi-cli `--print`, ZeroClaw `-m`) — Every platform eventually adds a non-interactive mode for scripting and CI integration.

2. **ACP/Wire protocol** (Hermes `acp`, kimi-cli `acp`/`--wire`, copilot-cli ACP) — Agent Communication Protocol is becoming the standard for IDE integration, with kimi-cli leading on wire protocol experimentation.

3. **MCP configuration as a CLI concern** (Hermes `mcp`, kimi-cli `mcp`, GoClaw adapter) — Managing MCP servers is becoming a first-class CLI operation, not a config-file-only concern.

### The Missing Commands

Every platform is missing something:

- **aider and codex** have no scheduling. You cannot say "run this coding task every morning." They are purely interactive.
- **ClawTeam** has no credential management CLI. Credentials are in TOML files or environment variables.
- **GoClaw** has no backup/restore. Enterprise infrastructure is assumed to be externally managed.
- **Hermes** has no one-shot *print-only* mode that also outputs JSON (kimi-cli's `--output-format stream-json` is more pipe-friendly).
- **ZeroClaw** has no session resume. Each `agent` invocation is fresh.
- **kimi-cli** has no cron or scheduling despite having the richest per-invocation configuration.
- **Reasonix** has no scheduling and no shell completion. Its cost tooling is unmatched, but you can't say "run this every morning" — the expected pattern is its `run` one-shot driven by system cron.

---

## The Bottom Line

The CLI is the most honest interface a platform has. Documentation can overstate capabilities. Marketing can mislead. But `--help` output is what users actually see, and it reveals the real priorities:

- **Hermes** prioritizes completeness — every feature gets a command
- **ZeroClaw** prioritizes consistency — every command has examples and clean help
- **kimi-cli** prioritizes configurability — every invocation can be finely tuned
- **OpenCode** prioritizes remote collaboration — serve, attach, mDNS discovery
- **aider** prioritizes focus — one loop, done well
- **codex** prioritizes safety — one binary, sandboxed, minimal
- **ClawTeam** prioritizes orchestration — commands for teams, not for chat
- **GoClaw** prioritizes infrastructure — commands for deployment, not interaction
- **Reasonix** prioritizes economics — budget caps and cache visibility in every invocation

The best CLIs of 2026 combine Hermes' completeness with ZeroClaw's consistency, kimi-cli's configurability, OpenCode's remote collaboration, and Reasonix's cost discipline. Nobody has done all five yet.

---

*Live CLI captures from Hermes v0.20.0, OpenCode v1.18.18, kimi-cli v1.24.0, zeroclaw v0.1.7, reasonix v0.52.0. Architecture documentation from the AllClaws platform comparison covering all tracked platforms. See [platform_comparison.md](https://github.com/dz3ai/allclaws/blob/main/architecture/platform_comparison.md) for full architecture details.*
