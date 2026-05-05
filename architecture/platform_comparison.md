# Unified Platform Comparison: All 20 AI Agent Platforms

**[中文](platform_comparison.zh-CN.md)** | English

> Standardized architecture comparison across all 20 platforms tracked by AllClaws — 13 claw ecosystem platforms and 7 external frameworks. Updated May 2026.

---

## Overview

This document provides a standardized, side-by-side architecture comparison of all 20 AI agent platforms tracked by the AllClaws research project. Each platform entry follows a uniform format covering classification, design principles, core architecture, and an architecture diagram (where available).

The 20 platforms divide into two groups:

- **Claw Ecosystem (13):** Platforms originating within or closely associated with the Claw/OpenClaw ecosystem.
- **External Frameworks (7):** Industry-reference frameworks tracked for ecosystem comparison.

### Key Cross-Cutting Patterns (May 2026)

**Convergence — what all platforms agree on:**
1. Streaming responses are table stakes
2. Multi-LLM provider support is the norm
3. Security sandboxing is essential (containers, WASM, or isolation layers)
4. Cross-session memory/persistence is universal

**Divergence — where the ecosystem is splitting:**
1. **MCP** — Native vs. Adapter vs. Resistant
2. **Deployment** — Local-first vs. Cloud
3. **Use case** — Personal-Force-Multiplier vs. Enterprise-Automation
4. **Architecture** — Single-agent vs. Multi-agent

**The defining trend of 2026:** The fork between personal-force-multiplier and enterprise-automation paradigms.

---

## Taxonomy

### By Field (Use Case)

| Field | Description | Examples |
|-------|-------------|----------|
| **Personal-Force-Multiplier** | Single user or small team; CLI-first; local deployment | OpenClaw, Nanobot, SmolAgents, Maxclaw, ZeroClaw, NanoClaw |
| **Enterprise-Automation** | Multi-user; cloud-deployed; governance focus | GoClaw, LangGraph, Swarms, HiClaw, CrewAI, AutoGen |
| **Personal/Enterprise (Hybrid)** | Spans both paradigms | IronClaw |
| **Academic** | Research and education focused | RTL-CLAW, Claw-AI-Lab |

### By MCP Relationship

| Status | Meaning | Examples |
|--------|---------|----------|
| **Native** | Framework built around MCP protocol | mcp-agent, Hermes-Agent |
| **Adapter** | MCP supported as integration layer | IronClaw, GoClaw, ZeroClaw, OpenClaw, HiClaw |
| **Resistant** | Explicitly avoids MCP overhead | NanoClaw |
| **None** | No MCP integration | ClawTeam, Maxclaw, Nanobot, QuantumClaw |
| **N/A** | Domain-specific; MCP not relevant | RTL-CLAW, Claw-AI-Lab |

---

## Part 1: Claw Ecosystem (13 Platforms)

---

## OpenClaw

**Classification:** TypeScript | ~340K stars | Personal-Force-Multiplier
**Repository:** [github.com/openclaw/openclaw](https://github.com/openclaw/openclaw)
**Status:** Active

### Overview

OpenClaw is the foundational TypeScript CLI application for autonomous AI agents. It supports 37+ messaging channels, an extensive plugin ecosystem, and cross-platform deployment including mobile (iOS/Android). Foundation governance transition is ongoing following the creator's move to OpenAI.

### Key Principles

- TypeScript (ESM), strict typing, no `any`
- Functional array methods, early returns, `const` over `let`
- Formatting via Oxlint/Oxfmt
- No prototype mutation for class behavior
- Concise files (~700 LOC), extract helpers

### Core Architecture

- **Language:** TypeScript (ESM)
- **Entry Point:** CLI via `src/cli`
- **Architecture Pattern:** Single-agent with channel/plugin extensions
- **Key Modules:** `src/provider-web.ts`, `src/infra`, `src/media`, channel modules (Telegram, Discord, Slack, Signal, iMessage, Web), extensions (MSTeams, Matrix, Zalo)
- **MCP Status:** Adapter — via plugin extension, not native
- **Deployment:** Cross-platform (Mac, Windows, Linux, iOS, Android)
- **LLM Support:** Web provider
- **Memory:** Not specified
- **Database:** Not specified
- **Security:** CLI security, redaction
- **Testing:** Vitest (coverage 70%), e2e, live tests

### Architecture Diagram

```mermaid
graph TD
    A[CLI Entry: src/cli] --> B[Commands: src/commands]
    B --> C[Provider Web: src/provider-web.ts]
    B --> D[Infra: src/infra]
    B --> E[Media Pipeline: src/media]
    B --> F[Channels: src/channels]
    F --> G[Telegram]
    F --> H[Discord]
    F --> I[Slack]
    F --> J[Signal]
    F --> K[iMessage]
    F --> L[Web]
    B --> M[Routing: src/routing]
    B --> N[Extensions: extensions/*]
    N --> O[Plugins e.g. MSTeams, Matrix]
```

---

## ClawTeam

**Classification:** Python 3.10+ | ~884 stars | Personal-Force-Multiplier
**Repository:** [github.com/win4r/ClawTeam-OpenClaw](https://github.com/win4r/ClawTeam-OpenClaw)
**Status:** Active

### Overview

ClawTeam is a multi-agent swarm coordination layer that transforms single AI agents into self-organizing teams with leader-worker orchestration, task dependencies, inter-agent messaging, and git worktree isolation for parallel development.

### Key Principles

- Agent self-organization (AI agents orchestrate themselves)
- Zero-config setup with TOML team templates
- File-based state with fcntl locking (no database)
- Git worktree isolation for parallel agents
- Multi-agent support (OpenClaw, Claude Code, Codex, Nanobot, Cursor)

### Core Architecture

- **Language:** Python 3.10+
- **Entry Point:** `clawteam` CLI
- **Architecture Pattern:** Multi-agent (Leader-Worker)
- **Key Modules:** Team lifecycle, agent spawning (tmux), task management, inter-agent messaging (inbox), monitoring dashboards, workspace management
- **MCP Status:** None
- **Deployment:** Local; optional ZeroMQ P2P for cross-machine
- **LLM Support:** Agent-dependent (OpenClaw, Claude Code, Codex, Nanobot, Cursor)
- **Memory:** JSON files under `~/.clawteam/`
- **Database:** JSON files (file-based)
- **Security:** Agent isolation via git worktrees
- **Testing:** 453 tests pass

### Architecture Diagram

```mermaid
graph TB
    A[Human Prompt] --> B[Leader Agent]
    B --> C[Task Creation]
    C --> D{Dependencies}
    D -->|Blocked| E[Task Queue]
    D -->|Ready| F[Worker Spawn]
    F --> F1[Worker Agent 1]
    F --> F2[Worker Agent 2]
    F --> F3[Worker Agent N]
    F1 --> G1[Git Worktree 1]
    F2 --> G2[Git Worktree 2]
    F3 --> G3[Git Worktree N]
    F1 -.->|Status| C
    F2 -.->|Status| C
    F3 -.->|Status| C
    F1 -.->|Message| I[Inboxes]
    B --> J[Monitoring]
    J --> J1[Kanban Board]
    J --> J2[Web UI Dashboard]
```

---

## GoClaw

**Classification:** Go 1.26 | ~1.3K stars | Enterprise-Automation
**Repository:** [github.com/nextlevelbuilder/goclaw](https://github.com/nextlevelbuilder/goclaw)
**Status:** Active

### Overview

GoClaw is a multi-agent AI gateway deployed as a single Go binary (~25 MB) with zero runtime dependencies. It orchestrates agent teams, inter-agent delegation, and quality-gated workflows across 13+ LLM providers with full multi-tenant PostgreSQL isolation.

### Key Principles

- Agent Teams & Orchestration with shared task boards
- Multi-tenant PostgreSQL with per-user workspaces
- Single binary deployment (~25 MB)
- 5-layer production security defense
- 13+ LLM providers with native Anthropic support

### Core Architecture

- **Language:** Go 1.26
- **Entry Point:** `cmd/goclaw/main.go`
- **Architecture Pattern:** Multi-agent gateway with lane-based scheduler
- **Key Modules:** gateway (WS + HTTP), agent loop (think-act-observe), providers (Anthropic native, OpenAI-compat), tool registry (fs, exec, web, memory, MCP), store (PostgreSQL), channels (Telegram, Feishu, Zalo, Discord, WhatsApp), scheduler (lane-based), skills (SKILL.md + BM25), memory (pgvector)
- **MCP Status:** Adapter — stdio/SSE/streamable-http
- **Deployment:** Binary + Docker (~50 MB Alpine)
- **LLM Support:** 13+ providers
- **Memory:** PostgreSQL + pgvector (hybrid search)
- **Database:** PostgreSQL 15+ (required)
- **Security:** 5-layer defense — rate limiting, prompt injection, SSRF protection, shell deny, AES-256-GCM
- **Testing:** `go test`, integration tests with race detector

### Architecture Diagram

```mermaid
graph TB
    subgraph Clients
        WEB["Web Dashboard"]
        TG["Telegram"]
        DC["Discord"]
        SL["Slack"]
        API["HTTP API"]
    end
    subgraph Gateway["GoClaw Gateway"]
        WS["WebSocket RPC"]
        REST["HTTP Server"]
        CM["Channel Manager"]
        BUS["Message Bus"]
        SCHED["Lane-based Scheduler"]
        ROUTER["Agent Router"]
        LOOP["Agent Loop"]
        TOOLS["Tool Registry"]
        LLM["LLM Providers"]
    end
    subgraph Storage
        PG["PostgreSQL + pgvector"]
    end
    WEB --> WS
    TG & DC & SL --> CM
    API --> REST
    WS & REST & CM --> BUS
    BUS --> SCHED
    SCHED --> ROUTER
    ROUTER --> LOOP
    LOOP --> TOOLS
    LOOP --> LLM
    LOOP --> PG
```

---

## IronClaw

**Classification:** Rust | Rapid growth | Personal/Enterprise (Hybrid)
**Repository:** [github.com/nearai/ironclaw](https://github.com/nearai/ironclaw)
**Status:** Active

### Overview

IronClaw is a Rust-based secure personal AI assistant with WASM sandboxing for tool execution and PostgreSQL for persistence. It is the most active claw platform with 8 releases in a single month, prioritizing data protection and self-expanding capabilities.

### Key Principles

- Security first with defense in depth
- Your data stays yours (local, encrypted, no telemetry)
- Self-expanding capabilities through dynamic tool building
- Transparency by design (open source, auditable)
- Capability-based permissions for WASM tools

### Core Architecture

- **Language:** Rust
- **Entry Point:** `src/main.rs`
- **Architecture Pattern:** Single-agent with WASM sandboxing
- **Key Modules:** agent orchestration, channels (REPL, HTTP, WASM), sandbox (WASM), orchestrator (Docker), safety (prompt injection defense), secrets (AES-256-GCM), database (PostgreSQL + pgvector)
- **MCP Status:** Adapter — MCP servers alongside WASM tools
- **Deployment:** Cross-platform (Mac, Win, Linux)
- **LLM Support:** Multi-provider (NEAR AI, OpenAI-compatible)
- **Memory:** PostgreSQL with pgvector (full-text + vector)
- **Database:** PostgreSQL 15+ (required)
- **Security:** WASM sandbox with endpoint allowlisting, credential injection at host boundary, prompt injection defense, no telemetry
- **Testing:** `cargo test`, integration tests with testcontainers

### Architecture Diagram

```mermaid
graph TD
    A[CLI Entry: main.rs] --> B[Bootstrap: bootstrap.rs]
    B --> C[App: app.rs]
    C --> D[Channels]
    D --> D1[REPL]
    D --> D2[HTTP Webhooks]
    D --> D3[WASM Channels]
    D --> D4[Web Gateway SSE/WS]
    C --> E[Agent Loop]
    E --> F[Router Intent Classification]
    E --> G[Scheduler Parallel Jobs]
    G --> I[Workers]
    I --> J[Orchestrator]
    J --> K[Docker Sandbox]
    J --> L[Tool Registry]
    L --> L1[Built-in Tools]
    L --> L2[MCP Servers]
    L --> L3[WASM Tools]
    C --> M[Workspace Memory]
    C --> N[Safety Layer]
    C --> O[DB PostgreSQL pgvector]
```

---

## Maxclaw

**Classification:** Go 1.24+ | ~189 stars | Personal-Force-Multiplier
**Repository:** [github.com/Lichas/maxclaw](https://github.com/Lichas/maxclaw)
**Status:** Active

### Overview

Maxclaw is an OpenClaw-style local-first AI agent written in Go, emphasizing low memory footprint, fully local workflow, and visual interfaces (desktop UI + web UI). It provides autonomous execution, spawnable sub-sessions, and monorepo-aware context discovery.

### Key Principles

- Go-native resource efficiency
- Fully local execution (sessions, memory, logs)
- Desktop UI + Web UI on same port
- Monorepo context awareness (AGENTS.md, CLAUDE.md)
- Autonomous mode with task scheduling

### Core Architecture

- **Language:** Go 1.24+
- **Entry Point:** `cmd/main.go`
- **Architecture Pattern:** Single-agent with sub-session spawning
- **Key Modules:** agent loop, tool system, memory (MEMORY.md + HISTORY.md), channels (Telegram, WhatsApp, Discord, WebSocket), scheduler (cron/once/every), monorepo context discovery
- **MCP Status:** None
- **Deployment:** Local (cross-platform); binaries: `maxclaw` and `maxclaw-gateway`
- **LLM Support:** Anthropic + OpenAI native SDKs
- **Memory:** Layered — MEMORY.md (long-term), HISTORY.md (session), heartbeat.md (active)
- **Database:** SQLite
- **Security:** Fully local execution only
- **Testing:** Go tests

### Architecture Diagram

```mermaid
graph TB
    A[CLI Entry: cmd/main.go] --> B[Agent Loop]
    B --> C[Reasoning Engine]
    B --> D[Tool Execution]
    B --> E[Session Manager]
    B --> F[Memory Layer]
    B --> G[Scheduler]
    B --> H[Channel Manager]
    C --> C1[Tool Registry]
    D --> D1[Skills]
    D --> D2[MCP Bridge]
    D --> D3[Custom Tools]
    E --> E1[Spawn Sub-Sessions]
    E --> E2[Independent Context]
    F --> F1[MEMORY.md]
    F --> F2[HISTORY.md]
    F --> F3[memory/heartbeat.md]
    G --> G1[Cron Jobs]
    G --> G2[Once Tasks]
    H --> H1[Telegram]
    H --> H2[WhatsApp Bridge]
    H --> H3[Discord]
    H --> H4[WebSocket]
    B --> I[Desktop UI + Web UI]
    B --> J[Monorepo Context Discovery]
```

---

## NanoClaw

**Classification:** TypeScript (Node.js) | Docker Partnership | Personal-Force-Multiplier
**Status:** Active

### Overview

NanoClaw is a personal Claude assistant as a single Node.js process connecting WhatsApp to Claude Agent SDK running in isolated containers. It provides per-group isolated filesystem and memory — the most prominent MCP resister in the ecosystem.

### Key Principles

- Single process architecture for simplicity
- Containerization for agent isolation
- Per-group memory and filesystem isolation
- WhatsApp as primary channel
- Explicitly avoiding MCP overhead

### Core Architecture

- **Language:** TypeScript (Node.js)
- **Entry Point:** `src/index.ts`
- **Architecture Pattern:** Single-agent with container isolation
- **Key Modules:** WhatsApp channel, IPC watcher, message router, container runner, task scheduler, SQLite database
- **MCP Status:** Resistant — CLI-first, container-based, direct tool execution preferred
- **Deployment:** macOS (launchctl) + containerized agents
- **LLM Support:** Claude Agent SDK
- **Memory:** Per-group CLAUDE.md files
- **Database:** SQLite
- **Security:** Container isolation per group
- **Testing:** Not specified

### Architecture Diagram

```mermaid
graph TD
    A[Orchestrator: src/index.ts] --> B[WhatsApp Channel]
    A --> C[IPC Watcher: src/ipc.ts]
    A --> D[Message Router: src/router.ts]
    A --> E[Config: src/config.ts]
    A --> F[Container Runner]
    A --> G[Task Scheduler]
    A --> H[Database: src/db.ts]
    F --> I[Claude Agent SDK in Containers]
    I --> J[Isolated Filesystem per Group]
    I --> K[Per-Group Memory: CLAUDE.md]
    I --> L[Browser Automation]
```

---

## Nanobot

**Classification:** Python 3.11+ | ~37K stars | Personal-Force-Multiplier
**Status:** Active

### Overview

Nanobot is an ultra-lightweight personal AI assistant with ~4,000 lines of core agent code — 99% smaller than OpenClaw. Delivers core agent functionality with minimal footprint. Installed via `pip install nanobot-ai`.

### Key Principles

- Ultra-lightweight (~4,000 LOC core)
- Research-ready with clean, readable code
- Easy one-click deployment
- MCP protocol support
- Multiple LLM providers via LiteLLM

### Core Architecture

- **Language:** Python 3.11+
- **Entry Point:** `nanobot/__main__.py` (CLI via Typer)
- **Architecture Pattern:** Single-agent with subagent support
- **Key Modules:** agent orchestrator, channels (8+: Telegram, Discord, Slack, WhatsApp, Feishu, QQ, Email, Matrix), providers (LiteLLM), skills (ClawHub), session manager, MCP bridge
- **MCP Status:** None — MCP bridge available but not core
- **Deployment:** Cross-platform (Python + Docker)
- **LLM Support:** Multiple via LiteLLM (Anthropic, OpenAI, DeepSeek, Qwen, Moonshot, etc.)
- **Memory:** Session history with configurable retention
- **Database:** SQLite
- **Security:** Security hardening
- **Testing:** tests/ directory

### Architecture Diagram

```mermaid
graph TB
    A[CLI Entry: __main__.py] --> B[Agent Orchestrator]
    B --> C[Reasoning Engine]
    C --> D[Tool Execution]
    D --> D1[Skills]
    D --> D2[MCP Bridge]
    B --> E[Session Manager]
    B --> F[Cron Scheduler]
    B --> G[Channel Manager]
    G --> G1[Telegram]
    G --> G2[Discord]
    G --> G3[Slack]
    G --> G4[WhatsApp]
    G --> G5[Feishu]
    G --> G9[CLI]
    B --> H[Provider Manager]
    H --> H1[Anthropic]
    H --> H2[OpenAI]
    H --> H3[DeepSeek]
    B --> I[ClawHub Integration]
```

---

## ZeroClaw

**Classification:** Rust | ~29K stars | Personal-Force-Multiplier
**Status:** Active

### Overview

ZeroClaw is a Rust-first autonomous agent runtime designed for high performance and efficiency — <5MB RAM, <10ms cold start. Uses trait-driven, modular architecture for pluggable components. Current performance leader in the ecosystem.

### Key Principles

- KISS (Keep It Simple, Stupid)
- YAGNI + DRY + Rule of Three
- SRP + ISP (Single Responsibility + Interface Segregation)
- Fail Fast + Explicit Errors
- Secure by Default + Least Privilege
- Determinism + Reproducibility

### Core Architecture

- **Language:** Rust
- **Entry Point:** `src/main.rs`
- **Architecture Pattern:** Single-agent with trait-based extensions
- **Key Modules:** config, agent orchestration, gateway (webhook server), security (policy, pairing, secrets), memory (markdown/sqlite + embeddings), providers, channels (15+), tools (shell, file, memory, browser), peripherals (STM32, RPi GPIO)
- **MCP Status:** Adapter — stdio/SSE
- **Deployment:** Native (Linux, etc.); cross-platform
- **LLM Support:** 8 native + 29 compatible providers
- **Memory:** Markdown/SQLite with embeddings and vector merge
- **Database:** SQLite
- **Security:** First-class, internet-adjacent; policy-based
- **Testing:** Rust tests

### Architecture Diagram

*No diagram available in source.*

---

## HiClaw

**Classification:** Go + Shell | Active development | Enterprise-Automation
**Status:** Active

### Overview

HiClaw is an enterprise-grade multi-agent runtime bringing Kubernetes-style declarative resources to AI agent orchestration. Manager-Workers architecture with team templates, worker marketplace, and Nacos-based skill registry.

### Key Principles

- Kubernetes-style declarative resources (YAML)
- Manager-Workers orchestration pattern
- Enterprise-grade multi-tenant support
- Worker template marketplace
- Nacos-based skill discovery

### Core Architecture

- **Language:** Go + Shell scripts
- **Entry Point:** `hiclaw` CLI with Docker Compose
- **Architecture Pattern:** Manager-Workers
- **Key Modules:** Worker resources (YAML), Team resources, Human resources (HITL), Manager CoPaw runtime, Nacos skills registry, Worker template marketplace
- **MCP Status:** Adapter
- **Deployment:** Docker Compose (dev), Kubernetes (production)
- **LLM Support:** Gateway-managed
- **Memory:** MinIO shared filesystem
- **Database:** PostgreSQL + MinIO
- **Security:** Gateway credential isolation; multi-tenant workspace isolation
- **Testing:** Not specified

### Architecture Diagram

```mermaid
graph TB
    A[CLI Entry: hiclaw] --> B[Resource Manager]
    B --> C[Worker Resources]
    B --> D[Team Resources]
    B --> E[Human Resources]
    C --> F[Worker Templates]
    D --> G[Team Definitions]
    E --> H[Human Agents]
    B --> I[Manager CoPaw Runtime]
    I --> J[Nacos Skills Registry]
    I --> K[PostgreSQL State]
    I --> L[MinIO File Storage]
    B --> M[Docker/Kubernetes Deploy]
```

---

## QuantumClaw

**Classification:** Node.js (TypeScript) | Active development | Personal-Force-Multiplier
**Status:** Active

### Overview

QuantumClaw is a self-hosted AGEX (Agent Gateway EXchange) protocol implementation focused on agent identity, trust, and cost-aware orchestration. Provides 3-layer memory, 5-tier cost routing, and ClawHub integration (3,286+ skills).

### Key Principles

- AGEX protocol for agent identity and trust
- Cost-aware model routing
- Three-layer memory architecture
- Self-hosted with minimal dependencies
- ClawHub skill marketplace integration

### Core Architecture

- **Language:** Node.js (TypeScript)
- **Entry Point:** `quantumclaw` CLI
- **Architecture Pattern:** Multi-agent spawning with AGEX protocol
- **Key Modules:** AGEX protocol (identity + trust), 3-layer memory (vector + structured + knowledge graph), 5-tier cost routing (reflex → simple → standard → complex → expert), Live Canvas dashboard, ClawHub integration, 12 MCP servers
- **MCP Status:** None — AGEX protocol, not MCP
- **Deployment:** Self-hosted (Linux, VPS, RPi, Android)
- **LLM Support:** 8+ providers
- **Memory:** 3-layer (vector search, structured knowledge, knowledge graph)
- **Database:** SQLite
- **Security:** Trust kernel (VALUES.md)
- **Testing:** Not specified

### Architecture Diagram

```mermaid
graph TB
    A[CLI Entry: quantumclaw] --> B[AGEX Protocol Layer]
    B --> C[Agent Identity]
    B --> D[Trust Kernel]
    B --> E[Cost Router]
    E --> F[Tier 1: Reflex]
    E --> G[Tier 2: Simple]
    E --> H[Tier 3: Standard]
    E --> I[Tier 4: Complex]
    E --> J[Tier 5: Expert]
    A --> K[3-Layer Memory]
    K --> K1[Vector Search]
    K --> K2[Structured Knowledge]
    K --> K3[Knowledge Graph]
    A --> L[ClawHub Integration]
    L --> M[3,286+ Skills]
    A --> N[Live Canvas Dashboard]
```

---

## Hermes-Agent

**Classification:** Python | Research-backed | Personal-Force-Multiplier
**Status:** Active

### Overview

Hermes-Agent is a research-backed personal AI agent implementing advanced context management — context compaction, resolved questions tracking, and context separators. AllClaws verification (May 2026) found it delivers on infrastructure but overstates "self-improving" claims.

### Key Principles

- Research-backed prompt engineering
- Context compaction to prevent stale answers
- Resolved questions tracking
- Clear context separators
- Competitor-inspired techniques

### Core Architecture

- **Language:** Python
- **Entry Point:** `hermes` CLI
- **Architecture Pattern:** Single-agent with context management
- **Key Modules:** Context compaction engine, resolved questions tracker, context separator system, prompt engineering layer, conversation manager, tool executor (MCP + custom tools)
- **MCP Status:** Native — MCP integration for tool execution
- **Deployment:** Linux, macOS, cloud
- **LLM Support:** Anthropic, OpenAI, OpenRouter
- **Memory:** Conversation history + file-based persistence
- **Database:** SQLite
- **Security:** Research-backed safety checks
- **Testing:** pytest

### Architecture Diagram

```mermaid
graph TD
    A[CLI Entry: hermes] --> B[Context Manager]
    B --> C[Context Compaction]
    B --> D[Resolved Questions Tracker]
    B --> E[Context Separators]
    A --> F[Prompt Engineering Layer]
    F --> G[Competitor-Inspired Prompts]
    F --> H[Safety Checks]
    A --> I[Conversation Manager]
    I --> J[Session Persistence]
    I --> K[History Management]
    A --> L[Tool Executor]
    L --> M[MCP Servers]
    L --> N[Custom Tools]
    A --> O[Channel Manager]
    O --> P[Telegram]
    O --> Q[Discord]
```

---

## RTL-CLAW

**Classification:** Python + Verilog | Academic | Academic
**Status:** Active

### Overview

RTL-CLAW is an AI-agent-driven framework for automated IC design flow, developed collaboratively by Tongji EDA Lab and CUHK. Built on OpenClaw, it demonstrates AI-driven RTL design automation, verification, and synthesis targeting ASAP7nm PDK.

### Key Principles

- Research-oriented EDA toolchain on OpenClaw
- Layered design: Interaction → Agent Core → Tool/Data Flow
- Modular plugin architecture
- Integration of open-source and commercial EDA tools

### Core Architecture

- **Language:** Python + Verilog
- **Entry Point:** Docker Compose
- **Architecture Pattern:** Layered pipeline (Interaction → Agent Core → Tool/Data Flow)
- **Key Modules:** Interaction Layer, Agent Core Layer (task planning/execution), Tool & Data Flow Layer (RTL analysis, Verilog partition, optimization, testbench generation, Yosys synthesis)
- **MCP Status:** N/A
- **Deployment:** Docker-based
- **LLM Support:** OpenClaw provider
- **Memory:** Workspace-based
- **Database:** Not specified
- **Security:** Docker-based isolation
- **Testing:** Not specified

### Architecture Diagram

```mermaid
graph TB
    A[Docker Compose Entry] --> B[RTL-CLAW CLI]
    A --> C[RTL-CLAW Gateway]
    B --> D[Interaction Layer]
    C --> E[Web UI]
    D --> F[Agent Core Layer]
    F --> G[Task Planning]
    F --> H[Task Execution]
    F --> I[Tool & Data Flow Layer]
    I --> J[RTL Analysis]
    I --> K[Verilog Partition]
    I --> L[Optimization]
    I --> M[Testbench Generation]
    I --> N[Yosys Synthesis]
    I --> O[Open-Source EDA Tools]
    I --> P[Commercial EDA Tools]
```

---

## Claw-AI-Lab

**Classification:** Python 3.11+ + Node.js 18+ | Academic | Academic
**Status:** Active

### Overview

Claw-AI-Lab is a lab-native multi-agent research platform for interactive, scalable AI-driven science. Create a full AI research lab from a single prompt with customizable roles and FIFO-based scheduling across three research modes: Explore, Discussion, Reproduce.

### Key Principles

- Lab-native multi-agent research platform
- FIFO-based scheduling for parallel execution
- Human-in-the-loop with intervention capabilities
- Cross-project knowledge sharing
- Three research modes: Explore, Discussion, Reproduce

### Core Architecture

- **Language:** Python 3.11+ (backend), Node.js 18+ (frontend)
- **Entry Point:** `start.sh`
- **Architecture Pattern:** Multi-agent research pipeline (FIFO-scheduled)
- **Key Modules:** multi-agent orchestrator, Claw Code Harness, sandbox executor, knowledge base (Markdown/Obsidian), React web dashboard, LLM provider manager with fallback chain
- **MCP Status:** N/A
- **Deployment:** Cross-platform (Python + Node.js)
- **LLM Support:** Multi-model with fallback chain
- **Memory:** Knowledge base (Markdown/Obsidian)
- **Database:** Project-based storage
- **Security:** HITL gates + sandboxed execution
- **Testing:** End-to-end pipeline testing

### Architecture Diagram

```mermaid
graph TB
    A[start.sh Entry] --> B[Backend Python]
    A --> C[Frontend Node.js]
    B --> D[Multi-Agent Orchestrator]
    D --> E[Claw Code Harness]
    D --> F[Sandbox Executor]
    D --> G[Knowledge Base]
    D --> H[LLM Provider Manager]
    E --> I[Local Codebases]
    F --> L[Experiment Runner]
    C --> M[Web Dashboard]
    M --> N[Event Stream]
    M --> P[Artifact Inspector]
    M --> Q[Rollback & Resume]
    H --> R[Primary Model]
    H --> S[Coding Model]
    H --> T[Image Model]
    H --> U[Fallback Chain]
```

---

## Part 2: External Frameworks (7 Platforms)

---

## SmolAgents

**Classification:** Python | ~26.7K stars | Personal-Force-Multiplier
**Repository:** [github.com/huggingface/smolagents](https://github.com/huggingface/smolagents)
**Status:** Active

### Overview

Hugging Face's ultra-lightweight AI agent library (~1,000 LOC core). Its defining characteristic is the code-first paradigm — agents express actions as executable Python code rather than abstract tool calls. Demonstrates how minimal an agent framework can be.

### Key Principles

- Minimal core (~1,000 lines)
- Code-first paradigm — agents write and execute Python
- Zero-to-hero simplicity
- Hugging Face ecosystem integration
- E2B sandbox execution

### Core Architecture

- **Language:** Python
- **Entry Point:** Library import (`from smolagents import CodeAgent`)
- **Architecture Pattern:** Single-agent (code generation)
- **Key Modules:** CodeAgent, HfApiModel, sandboxed tool execution, memory system
- **MCP Status:** N/A
- **Deployment:** Hybrid
- **LLM Support:** Hugging Face inference API (free tier)
- **Memory:** Conversation context and results tracking
- **Database:** Not specified
- **Security:** E2B sandbox
- **Testing:** Not specified

### Claw Ecosystem Comparison

| Aspect | SmolAgents | Nanobot | NanoClaw |
|--------|------------|---------|----------|
| **Core LOC** | ~1,000 | ~4,000 | ~10,600 |
| **Paradigm** | Code generation | Tool calling | Container-first |
| **Sandbox** | E2B | Native | Docker |
| **Ecosystem** | Hugging Face Hub | Custom | Custom |

---

## LangGraph

**Classification:** Python, TypeScript | Enterprise adoption | Enterprise-Automation
**Repository:** [github.com/langchain-ai/langgraph](https://github.com/langchain-ai/langgraph)
**Status:** Active

### Overview

Graph-based orchestration framework for stateful, multi-agent AI applications. Built on LangChain, it models AI workflows as directed graphs with checkpointing for persistence. Enterprise leader via LangChain ecosystem.

### Key Principles

- Graph-based workflows
- Stateful execution with checkpointing
- Human-in-the-loop patterns
- Parallel execution support
- Enterprise-ready production patterns

### Core Architecture

- **Language:** Python, TypeScript
- **Entry Point:** Library import
- **Architecture Pattern:** Graph-orchestration
- **Key Modules:** StateGraph (typed state), Nodes (agents/tools), Edges (conditional routing), Checkpointing, Subgraphs
- **MCP Status:** N/A
- **Deployment:** Cloud
- **LLM Support:** Via LangChain ecosystem
- **Memory:** Built-in checkpointing
- **Database:** Not specified
- **Security:** Not specified
- **Testing:** Not specified

### Claw Ecosystem Comparison

| Aspect | LangGraph | ClawTeam | GoClaw |
|--------|-----------|----------|--------|
| **Orchestration** | Graph-based | Leader-worker | Team-based |
| **State** | Checkpointed | Git worktrees | PostgreSQL |
| **Type Safety** | Typed state | Untyped | Go types |

---

## mcp-agent

**Classification:** Python | ~8.2K stars | Enterprise-Automation
**Repository:** [github.com/lastmile-ai/mcp-agent](https://github.com/lastmile-ai/mcp-agent)
**Status:** Active

### Overview

The reference implementation for MCP-native AI agents. Built by LastMile AI with a planner-executor model, built-in memory, and simple composition. Vision: "MCP is all you need."

### Key Principles

- MCP-native design
- Planner-executor model
- Built-in memory system
- Simple composition from MCP servers

### Core Architecture

- **Language:** Python
- **Entry Point:** Library import
- **Architecture Pattern:** Planner-executor (single-agent)
- **Key Modules:** MCP Client, Planner (task decomposition), Executor (MCP tool calls), Memory
- **MCP Status:** Native — reference implementation
- **Deployment:** Cloud
- **LLM Support:** Not specified
- **Memory:** Integrated memory system
- **Database:** Not specified
- **Security:** Not specified
- **Testing:** Not specified

### Claw Ecosystem Comparison

| Platform | MCP Support | Type |
|----------|-------------|------|
| **mcp-agent** | Native (reference) | Framework built around MCP |
| **IronClaw** | Adapter | stdio/SSE/streamable-http |
| **GoClaw** | Adapter | stdio/SSE/streamable-http |
| **ZeroClaw** | Adapter | stdio/SSE/streamable-http |
| **OpenClaw** | Plugin | Via extension |
| **NanoClaw** | None | CLI-first, resistant |

---

## CrewAI

**Classification:** Python | Active development | Enterprise-Automation
**Repository:** [github.com/crewaiinc/crewai](https://github.com/crewaiinc/crewai)
**Status:** Active

### Overview

Python framework for orchestrating role-playing autonomous AI agents. Each agent has a defined role, goal, and backstory. Pioneered the role-based approach to multi-agent systems.

### Key Principles

- Role-based agents (role, goal, backstory)
- Automatic task delegation
- Sequential/parallel workflows
- External tool usage
- Human-in-the-loop approval

### Core Architecture

- **Language:** Python
- **Entry Point:** Library import (`from crewai import Agent, Task, Crew`)
- **Architecture Pattern:** Multi-agent (Role-based)
- **Key Modules:** Agent (role-based entity), Task (work unit), Crew (agent collection), Process (sequential/parallel/hierarchical)
- **MCP Status:** N/A
- **Deployment:** Hybrid
- **LLM Support:** Not specified
- **Memory:** In-memory state
- **Database:** Not specified
- **Security:** HITL approval gates
- **Testing:** Not specified

### Claw Ecosystem Comparison

| Aspect | CrewAI | ClawTeam |
|--------|--------|----------|
| **Coordination** | Role-based stories | Leader-worker |
| **State** | In-memory | Git worktrees |
| **Communication** | Direct messages | Inbox system |
| **Isolation** | Process-level | Filesystem (worktrees) |

---

## AutoGen

**Classification:** Python | Microsoft Research | Enterprise-Automation
**Repository:** [github.com/microsoft/autogen](https://github.com/microsoft/autogen)
**Status:** Active

### Overview

Microsoft Research's multi-agent conversation framework. Agents communicate through messages to solve tasks, with human-in-the-loop, Docker code execution, and multi-modal support.

### Key Principles

- Conversation-based agent communication
- Human-in-the-loop via UserProxy agent
- Docker-based safe code execution
- Multi-modal (text, images, code)
- LLM flexibility

### Core Architecture

- **Language:** Python
- **Entry Point:** Library import
- **Architecture Pattern:** Multi-agent (Conversational)
- **Key Modules:** Agent, Conversation, UserProxyAgent, CodeExecutor (Docker)
- **MCP Status:** N/A
- **Deployment:** Cloud
- **LLM Support:** Various providers
- **Memory:** Conversation-based state
- **Database:** Not specified
- **Security:** Docker code execution sandbox
- **Testing:** Not specified

### Claw Ecosystem Comparison

| Aspect | AutoGen | ClawTeam | CrewAI |
|--------|---------|----------|--------|
| **Communication** | Conversational messages | Inbox system | Direct calls |
| **Human role** | UserProxy agent | Separate from agents | Optional approval |
| **Code execution** | Built-in Docker | Via agent tools | Via agent tools |

---

## Swarms

**Classification:** Python | ~5K stars | Enterprise-Automation
**Repository:** [github.com/kyegomez/swarms](https://github.com/kyegomez/swarms)
**Status:** Active

### Overview

Enterprise-grade, production-ready multi-agent orchestration framework. Focuses on scalability and reliability for large-scale deployments. Describes itself as "the most reliable, scalable, and flexible multi-agent orchestration framework."

### Key Principles

- Enterprise-grade reliability
- Large-scale agent deployments
- Async sub-agents (v10+)
- SkillOrchestra for capabilities
- "Agentic economy" vision

### Core Architecture

- **Language:** Python
- **Entry Point:** Library import
- **Architecture Pattern:** Multi-agent (Async orchestration)
- **Key Modules:** Swarm (agent collection), Orchestrator (lifecycle), Skills (reusable capabilities), Tools (external integrations)
- **MCP Status:** N/A
- **Deployment:** Cloud
- **LLM Support:** Not specified
- **Memory:** Not specified
- **Database:** Not specified
- **Security:** Not specified
- **Testing:** Not specified

### Claw Ecosystem Comparison

| Aspect | Swarms | GoClaw | HiClaw |
|--------|--------|--------|--------|
| **Target** | Enterprise orchestration | Multi-agent gateway | Multi-agent runtime |
| **Language** | Python | Go | Go + Shell |
| **Architecture** | Async skills | Lane-based scheduler | Manager-workers |

---

## OpenAgents

**Classification:** TypeScript | Active development | Enterprise-Automation
**Repository:** [github.com/openagents-org/openagents](https://github.com/openagents-org/openagents)
**Status:** Active

### Overview

TypeScript-based framework for distributed AI agent networks. Philosophy: "Your agents are everywhere" — agents across distributed infrastructure handle databases, marketing, and user replies. Demonstrates TypeScript as a first-class agent framework language.

### Key Principles

- Distributed agents on different servers
- TypeScript-first implementation
- Cloud-native design
- Multi-location deployment

### Core Architecture

- **Language:** TypeScript
- **Entry Point:** Library import
- **Architecture Pattern:** Multi-agent (Distributed network)
- **Key Modules:** Agent workspace, network coordination, cloud integration
- **MCP Status:** N/A
- **Deployment:** Cloud (distributed)
- **LLM Support:** Not specified
- **Memory:** Not specified
- **Database:** Not specified
- **Security:** Not specified
- **Testing:** Not specified

### Claw Ecosystem Comparison

| Aspect | OpenAgents | QuantumClaw |
|--------|------------|-------------|
| **Deployment** | Distributed cloud | Local-first |
| **Protocol** | Custom | AGEX |
| **Language** | TypeScript | TypeScript |
| **Focus** | Distributed scale | Privacy |

---

## Part 3: Cross-Platform Comparison Matrices

### Language & Field Matrix

| Platform | Language | Field | Stars |
|----------|----------|-------|-------|
| OpenClaw | TypeScript | Personal-Force-Multiplier | ~340K |
| ClawTeam | Python 3.10+ | Personal-Force-Multiplier | ~884 |
| GoClaw | Go 1.26 | Enterprise-Automation | ~1.3K |
| IronClaw | Rust | Personal/Enterprise (Hybrid) | Growing |
| Maxclaw | Go 1.24+ | Personal-Force-Multiplier | ~189 |
| NanoClaw | TypeScript (Node.js) | Personal-Force-Multiplier | N/A |
| Nanobot | Python 3.11+ | Personal-Force-Multiplier | ~37K |
| ZeroClaw | Rust | Personal-Force-Multiplier | ~29K |
| HiClaw | Go + Shell | Enterprise-Automation | N/A |
| QuantumClaw | Node.js (TypeScript) | Personal-Force-Multiplier | N/A |
| Hermes-Agent | Python | Personal-Force-Multiplier | N/A |
| RTL-CLAW | Python + Verilog | Academic | N/A |
| Claw-AI-Lab | Python 3.11+ + Node.js 18+ | Academic | N/A |
| SmolAgents | Python | Personal-Force-Multiplier | ~26.7K |
| LangGraph | Python/TypeScript | Enterprise-Automation | N/A |
| mcp-agent | Python | Enterprise-Automation | ~8.2K |
| CrewAI | Python | Enterprise-Automation | N/A |
| AutoGen | Python | Enterprise-Automation | N/A |
| Swarms | Python | Enterprise-Automation | ~5K |
| OpenAgents | TypeScript | Enterprise-Automation | N/A |

### MCP Adoption Matrix

| MCP Status | Platforms |
|------------|-----------|
| **Native** | mcp-agent, Hermes-Agent |
| **Adapter** | OpenClaw, GoClaw, IronClaw, ZeroClaw, HiClaw |
| **Resistant** | NanoClaw |
| **None** | ClawTeam, Maxclaw, Nanobot, QuantumClaw |
| **N/A** | RTL-CLAW, Claw-AI-Lab, SmolAgents, LangGraph, CrewAI, AutoGen, Swarms, OpenAgents |

### Architecture Pattern Matrix

| Pattern | Platforms |
|---------|-----------|
| **Single-agent** | OpenClaw, IronClaw, Maxclaw, NanoClaw, Nanobot, ZeroClaw, Hermes-Agent |
| **Leader-Worker** | ClawTeam |
| **Gateway/Teams** | GoClaw |
| **Manager-Workers** | HiClaw |
| **Multi-agent spawning** | QuantumClaw |
| **Role-based multi-agent** | CrewAI |
| **Conversational multi-agent** | AutoGen |
| **Async orchestration** | Swarms |
| **Distributed network** | OpenAgents |
| **Graph-orchestration** | LangGraph |
| **Planner-executor** | mcp-agent |
| **Code generation** | SmolAgents |
| **Layered pipeline** | RTL-CLAW |
| **Research pipeline** | Claw-AI-Lab |

### Deployment & Database Matrix

| Platform | Deployment | Database | Containerization |
|----------|------------|----------|------------------|
| OpenClaw | Cross-platform (Mac, Win, Linux, mobile) | Not specified | Not specified |
| ClawTeam | Local + optional ZeroMQ P2P | JSON files | None (git worktrees) |
| GoClaw | Binary + Docker | PostgreSQL 15+ | Docker sandbox |
| IronClaw | Cross-platform | PostgreSQL 15+ | Docker + WASM |
| Maxclaw | Local (cross-platform) | SQLite | None |
| NanoClaw | macOS + containers | SQLite | Linux VMs/containers |
| Nanobot | Cross-platform (Python + Docker) | SQLite | Docker |
| ZeroClaw | Native (Linux, etc.) | SQLite | None |
| HiClaw | Docker + Kubernetes | PostgreSQL + MinIO | Docker/K8s |
| QuantumClaw | Self-hosted (Linux, VPS, RPi) | SQLite | None |
| Hermes-Agent | Linux, macOS, cloud | SQLite | None |
| RTL-CLAW | Docker | Not specified | Docker |
| Claw-AI-Lab | Cross-platform | Project-based | Sandbox executor |
| SmolAgents | Hybrid | Not specified | E2B sandbox |
| LangGraph | Cloud | Not specified | Not specified |
| mcp-agent | Cloud | Not specified | Not specified |
| CrewAI | Hybrid | Not specified | Not specified |
| AutoGen | Cloud | Not specified | Docker |
| Swarms | Cloud | Not specified | Not specified |
| OpenAgents | Cloud (distributed) | Not specified | Not specified |

### Full 20-Platform Comparison Table

| Platform | Language | Stars | MCP | Architecture | Deployment | Field |
|----------|----------|-------|-----|-------------|------------|-------|
| OpenClaw | TypeScript | ~340K | Adapter | Single + plugins | Cross-platform | Personal |
| ClawTeam | Python | ~884 | None | Leader-Worker | Local | Personal |
| GoClaw | Go | ~1.3K | Adapter | Gateway + Teams | Binary + Docker | Enterprise |
| IronClaw | Rust | Growing | Adapter | Single + WASM | Cross-platform | Hybrid |
| Maxclaw | Go | ~189 | None | Single + sub-sessions | Local | Personal |
| NanoClaw | TypeScript | N/A | Resistant | Single + containers | macOS + containers | Personal |
| Nanobot | Python | ~37K | None | Single + subagent | Cross-platform | Personal |
| ZeroClaw | Rust | ~29K | Adapter | Single + traits | Native | Personal |
| HiClaw | Go+Shell | N/A | Adapter | Manager-Workers | Docker/K8s | Enterprise |
| QuantumClaw | TypeScript | N/A | None | Multi-agent spawning | Self-hosted | Personal |
| Hermes-Agent | Python | N/A | Native | Single + context | Linux/macOS/cloud | Personal |
| RTL-CLAW | Py+Verilog | N/A | N/A | Layered pipeline | Docker | Academic |
| Claw-AI-Lab | Py+Node.js | N/A | N/A | Research pipeline | Cross-platform | Academic |
| SmolAgents | Python | ~26.7K | N/A | Code generation | Hybrid | Personal |
| LangGraph | Py/TS | N/A | N/A | Graph-orchestration | Cloud | Enterprise |
| mcp-agent | Python | ~8.2K | Native | Planner-executor | Cloud | Enterprise |
| CrewAI | Python | N/A | N/A | Role-based | Hybrid | Enterprise |
| AutoGen | Python | N/A | N/A | Conversational | Cloud | Enterprise |
| Swarms | Python | ~5K | N/A | Async orchestration | Cloud | Enterprise |
| OpenAgents | TypeScript | N/A | N/A | Distributed | Cloud | Enterprise |

---

## See Also

- **Monthly Ecosystem Reports:** [_posts/](../_posts/) — Cross-cutting trends and platform updates
- **Latest Updates:** [docs/LATEST_UPDATES.md](../docs/LATEST_UPDATES.md) — Per-platform change tracking
- **Multi-Agent Coordination Research:** [multi_agent_coordination_research.md](multi_agent_coordination_research.md) — Deep-dive on coordination patterns
- **Research Roadmap:** [docs/ROADMAP.md](../docs/ROADMAP.md) — H2 2026 priorities
- **Original architecture docs (now superseded):** [architecture_comparison.md](architecture_comparison.md), [external_frameworks.md](external_frameworks.md)

---

*Last updated: May 2026*
*Platforms tracked: 20 (13 claw ecosystem + 7 external frameworks)*
*Part of: AllClaws Personal AI Agent Ecosystem Research*
