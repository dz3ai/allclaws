# Latest Updates: Personal AI Agent Ecosystem (April-May 2026)

English | **[中文](LATEST_UPDATES.zh-CN.md)**

> Tracking major changes across 11 claw ecosystem platforms, 18 external frameworks, 5 CLI coding agents, and 1 human digital twin platform — architecture innovations, MCP adoption debates, enterprise vs personal patterns, and security developments from April to August 2026.

---

## Cross-Cutting Themes

April-May 2026 revealed four defining trends shaping the ecosystem:

1. **The MCP Debate Intensified** — Model Context Protocol gained enterprise adoption (IronClaw, GoClaw, ZeroClaw) but faced resistance from local-first agents (NanoClaw) over 20-30% token overhead
2. **"Self-Improving" Claims Under Scrutiny** — Hermes-Agent source code analysis revealed procedural memory ≠ autonomous learning; distinction now widely recognized
3. **Enterprise vs 1PC Fork** — Clear divergence between enterprise-automation (governance, cloud, MCP) and personal-force-multiplier (speed, local, CLI) paradigms
4. **External Framework Recognition** — SmolAgents, LangGraph, CrewAI, AutoGen, Swarms, OpenAgents, OpenFang, AgentScope, Eliza, Agent Zero, PraisonAI, Rocketride added for ecosystem comparison
5. **Agent Harnesses Category Added** — UltraWorkers toolchain (claw-code, oh-my-codex, clawhip, oh-my-openagent) recognized as distinct infrastructure layer
6. **CLI Coding Agents Added** — aider (~68K stars, git-aware AI pair programming), copilot-cli (GitHub Copilot terminal agent), reasonix (DeepSeek-native coding agent, ~11.3K stars) added as new category
7. **Human Digital Twin Added** — openhuman (Rust, 人类数字孪生) added as academic/research platform
8. **MoonshotAI Platforms Added** — kimi-cli (Python, CLI coding agent, ~8.8K stars, ACP support) and kimi-code (TypeScript, next-gen agent framework, ~1.4K stars, MCP + plugin architecture) added
9. **AgentScope Added** — AgentScope (Python, Alibaba DAMO Academy, ~25.8K stars) added as 9th external framework; distributed multi-agent collaboration with message hub and pipeline workflows
10. **Eliza Added** — Eliza (TypeScript, eliza-os, MIT) added as 10th external framework; multi-platform AI agent framework with plugin architecture
11. **Agent Zero Added** — Agent Zero (Python, frdel, MIT) added as 11th external framework; autonomous AI agent framework with tool-use capabilities
12. **PraisonAI Added** — PraisonAI (Python, MervinPraison, MIT) added as 12th external framework; multi-agent LLM framework with low-code workflow builder
13. **Rocketride Added** — Rocketride (TypeScript, nearai, MIT) added as 13th external framework; near.ai agent server for autonomous task execution
14. **browser-use Added (August 2026)** — browser-use (Python, MIT, ~110K stars) added as 18th external framework and platform #35; first computer-use (browser) representative per governance Q4-7 ruling. Chromium CDP agent loop, typed action schemas, ships as MCP server
15. **Harness Ecosystems Expanded (August 2026)** — DeepSeek Harness (dsh, first-party frontier-vendor harness on Cordis plugin-tree composition) and Pi (Earendil Works, self-extensible harness) added as harness ecosystems #6-7; Pi Tier 2, dsh Tier 3 until 1.0

---

## Research Milestones (H2 2026)

Completed research beyond platform tracking — full roadmap status in [ROADMAP.md](ROADMAP.md) (12 of 13 items done):

- [x] MCP ecosystem deep-dive (5 phases) — [reports/mcp-deep-dive-phase4-5-synthesis.md](reports/mcp-deep-dive-phase4-5-synthesis.md)
- [x] Enterprise governance framework analysis — [reports/enterprise-governance-analysis.md](reports/enterprise-governance-analysis.md)
- [x] 1PC (one-person company) case studies — [reports/1pc-case-studies-2026.md](reports/1pc-case-studies-2026.md)
- [x] Agent failure mode taxonomy (13 failure modes across 35 platforms) — [reports/failure-mode-taxonomy-2026.md](reports/failure-mode-taxonomy-2026.md)
- [x] China AI agent ecosystem deep-dive (14 projects, 350K+ combined stars) — [reports/china-agent-ecosystem-2026.md](reports/china-agent-ecosystem-2026.md)
- [x] Harness engineering comparison — [reports/harness-engineering-comparison.md](reports/harness-engineering-comparison.md)
- [x] Protocol wars analysis (Q4-5) — MCP/ACP/A2A layering, not war — [reports/protocol-wars-2026.md](reports/protocol-wars-2026.md)
- [x] Platform governance & quality thresholds (Q4-6) — three-tier tracking model, Tier-1 cap of 35 — [governance.md](governance.md)
- [x] Category coverage gap-closure (Q4-7) — 6 candidates evaluated, browser-use admitted as #35 (first computer-use representative)
- [ ] Long-running agent benchmarks (Q4-4) — in progress, the last open roadmap item

## Test & Benchmark Results

**Static tests (April 12, 2026): 165 pass / 12 fail / 177 total** across 11 claw platforms.

| Platform | Language | Files | Result |
|----------|----------|-------|--------|
| Openclaw | TypeScript | 5941 .ts | 13/13 pass |
| ClawTeam | Python | 75 .py | 12/13 pass |
| GoClaw | Go | 524 .go | 11/14 pass |
| IronClaw | Rust | 287 .rs | 14/14 pass |
| Maxclaw | Go | 118 .go | 13/14 pass |
| NanoClaw | TypeScript | 61 .ts | 13/13 pass |
| Nanobot | Python | 88 .py | 10/13 pass |
| Zeroclaw | Rust | 227 .rs | 14/14 pass |
| HiClaw | Go | ~400 .go | 13/14 pass |
| Hermes-Agent | Python | ~60 .py | 11/13 pass |
| Claw-AI-Lab | Python | ~50 .py | 11/13 pass |

**Runtime benchmarks (v3.0 Python engine): 140 metrics across 26 platforms** — cold start, memory, latency, binary size, N=5 sampling with statistics. Latest numbers live in CI artifacts (`benchmark-suite.yml`, daily); methodology in [test_framework/docs/runtime_benchmark_methodology.md](../test_framework/docs/runtime_benchmark_methodology.md).

**Static repository metrics (April 12, 2026): 182 metrics across 13 platforms**

| Platform | Repo Size (KB) | Source Files | Source LOC | Dependencies | Test Files |
|----------|----------------|-------------|-----------|--------------|-----------|
| Openclaw | 193,592 | 5,760 .ts | 146,967 | 73 npm | 2,227 |
| ClawTeam | 19,728 | 75 .py | 13,407 | 16 pip | 26 |
| GoClaw | 21,848 | 501 .go | 92,815 | 149 go | 38 |
| IronClaw | 23,216 | 362 .rs | 191,946 | 51 cargo | 48 |
| Maxclaw | 18,880 | 118 .go | 30,499 | 33 go | 45 |
| NanoClaw | 19,768 | 51 .ts | 10,606 | 14 npm | 17 |
| Nanobot | 66,200 | 88 .py | 18,960 | 49 pip | 26 |
| Zeroclaw | 24,640 | 259 .rs | 161,169 | 45 cargo | 18 |
| HiClaw | ~25,000 | ~400 .go | ~35,000 | ~40 go | ~30 |
| Hermes-Agent | ~8,000 | ~60 .py | ~8,000 | ~15 pip | ~12 |
| Claw-AI-Lab | ~10,000 | ~50 .py | ~7,000 | ~25 pip | ~8 |

---

## Agent Harnesses & Toolchains

> **New Category:** Agent harnesses sit below agent platforms, providing execution runtime, coordination, and observability.

### UltraWorkers Toolchain

**Philosophy:** *"Humans set direction; claws perform the labor."*

#### claw-code (Rust)
- **Repository:** [ultraworkers/claw-code](https://github.com/ultraworkers/claw-code)
- **Status:** Active (~100K stars claimed)
- **Overview:** Clean-room rewrite of Claude Code agent harness architecture
- **Key Stats:** 48,599 LOC Rust, 9 crates, 40 tool specs (April 2026)
- **9-Lane Parity:** Bash validation, file-tool, TaskRegistry, team/cron, MCP lifecycle, LSP client, permission enforcement

#### oh-my-codex (Node.js)
- **Repository:** [Yeachan-Heo/oh-my-codex](https://github.com/Yeachan-Heo/oh-my-codex)
- **Role:** Workflow layer for OpenAI Codex CLI
- **Canonical Workflows:** `$deep-interview`, `$ralplan`, `$team`, `$ralph`

#### clawhip (Rust)
- **Repository:** [Yeachan-Heo/clawhip](https://github.com/Yeachan-Heo/clawhip)
- **Role:** Event and notification router (v0.3.0)
- **Key Features:** Typed event model, multi-delivery router, source extraction

#### oh-my-openagent (Node.js)
- **Repository:** [code-yeongyu/oh-my-openagent](https://github.com/code-yeongyu/oh-my-openagent)
- **Role:** Multi-agent coordination (Architect → Executor → Reviewer convergence)

**Full Analysis:** [architecture/agent_harnesses.md](../architecture/agent_harnesses.md)

---

## OpenClaw

**TypeScript | ~340K stars | v2026.4.x — May 2026**

**Status:** Foundation governance transition continues following creator's OpenAI joining

### Architecture Evolution
- Channel plugin ecosystem expansion (WhatsApp, Discord, Teams, Matrix)
- MCP integration via adapter pattern (not native)
- Native app platform growth (iOS/Android/macOS)

### New Features (April-May Highlights)
- Additional LLM provider integrations
- Enhanced streaming reliability
- Skill marketplace growth
- Webhook security improvements

### Security
- Continued CVE remediation from March disclosures
- Container execution options enhanced

---

## ZeroClaw

**Rust | ~29K stars | v0.7.5 — May 2026**

### Status: Performance Leader
- **<5MB RAM, <10ms cold start** benchmark maintained
- Most efficient runtime in ecosystem

### New Features
- MCP adapter integration (stdio/SSE)
- Enhanced session state management
- Multi-room channel improvements

---

## IronClaw

**Rust | Rapid growth | v0.28.2 — May 2026**

**Status:** Most active claw platform

### Architecture Evolution
- Multi-tenant auth maturity
- Layered memory system enhancements
- WASM extension ecosystem growth

### New Features
- **MCP adapter integration** (non-native approach)
- Additional LLM providers
- Risk-based command approval refinement
- i18n expansion

### Security
- Continued cargo-d enforcement
- Supply chain auditing

---

## GoClaw

**Go | ~1.3K stars | lite-v3.9.1 — May 2026**

### Architecture Evolution
- Agent Teams coordination maturity
- Lane-based scheduler refinement
- MCP integration (stdio/SSE/streamable-http)

### New Features
- Knowledge graph enhancements
- OpenTelemetry export expansion
- Additional channels and providers

### Enterprise Pattern
- Multi-tenant PostgreSQL architecture
- Cloud deployment optimizations

---

## NanoClaw

**TypeScript | Active dev | Docker Partnership — March-May 2026**

### Status: MCP Skeptic
- Explicitly avoiding MCP overhead
- Container-first security model
- ~4,000 LOC core philosophy

### Position
- **MCP resistance**: Token cost concerns for local deployment
- Direct tool execution preferred
- Docker sandbox alliance continued

---

## Nanobot

**Python | ~37K stars | v0.2.0 — May 2026**

### Architecture Evolution
- Agent runtime decomposition maturity
- litellm removal completed
- HookContext standardization

### New Features
- Channel expansion (12+)
- LLM provider growth
- Token-based memory refinement

### Security
- Supply chain security focus
- Email injection protection

---

## ClawTeam-OpenClaw

**Python | ~884 stars | v0.2.x+ — May 2026**

### Multi-Agent Coordination
- Leader-worker orchestration pattern
- Per-agent session isolation
- ZeroMQ P2P transport optionality

### New Features
- Web dashboard improvements
- Team template expansion
- Plan approval workflows

---

## Maxclaw

**Go + TypeScript | ~189 stars | v0.1.x+ — May 2026**

### Personal-Force-Multiplier Pattern
- Local-first deployment
- Monorepo-aware context
- Desktop UI + Web UI

### New Features
- Sub-session spawning
- Browser automation
- Systemd deployment

---

## HiClaw

**Go + Shell | Active dev | v1.1.1 — April 2026**

**Status:** Enterprise multi-agent runtime

### Architecture: Manager-Workers Pattern
- Kubernetes-style declarative resources
- Multi-agent orchestration
- Shell-based extensibility

### Key Features
- Declarative resource definitions
- Agent lifecycle management
- Enterprise deployment focus

---

## Hermes-Agent

**Python | Research-backed | v2026.5.16 — May 2026**

**Status:** Claims Verification Complete

### What Exists
- ✅ Skill curation system
- ✅ Cross-session memory (FTS5 + LLM)
- ✅ MCP integration
- ✅ Skills Hub

### What's Missing
- ❌ Autonomous skill improvement
- ❌ RL-based learning
- ❌ Performance tracking

### Verdict
**Procedural memory ≠ autonomous learning** — "self-improving" claims overstated

---

## Claw-AI-Lab

**Python | Academic | Active dev**

**Status:** Educational research platform

### Focus
- AI agent education
- Research experimentation
- Academic collaboration

---

## CLI Coding Agents

> **New Category:** AI-powered terminal-based coding assistants that pair-program with developers directly in the CLI.

### aider

**Python | ~68K stars | v0.86.3.dev — May 2026**

**Status:** Active — Most popular AI pair programming tool

### Overview
aider is an AI pair programming tool that works in your terminal, enabling developers to pair-program with LLMs to edit code in local git repositories. It supports Claude, GPT-4, and other models.

### Key Features
- **Git-aware** — Automatically creates commits with sensible messages
- **Multi-model** — Supports Claude, GPT-4, DeepSeek, and 20+ LLMs via API or local models
- **Code-gen paradigm** — AI edits code directly in your repo
- **Whole-repo context** — Can understand entire codebase
- **Map/Architecture modes** — Cost-effective strategies for large codebases

### Architecture
- **Language:** Python
- **Entry Point:** `aider` CLI
- **Architecture Pattern:** REPL pair-programming with git integration
- **MCP Status:** None
- **Deployment:** Local (pip install)
- **LLM Support:** 20+ providers (Claude, GPT-4, DeepSeek, local via ollama)

---

### copilot-cli

**TypeScript | GitHub-native | v1.0.49 — May 2026**

**Status:** Active — GitHub's official CLI agent

### Overview
copilot-cli is GitHub's Copilot-powered terminal agent that brings AI assistance directly to the command line. Built with ACP (Agent Communication Protocol) for structured interactions.

### Key Features
- **GitHub-native** — Deep integration with GitHub workflows
- **ACP protocol** — Agent Communication Protocol for structured terminal interactions
- **Terminal integration** — Works natively in shell environments
- **GitHub ecosystem** — Leverages GitHub Copilot infrastructure

### Architecture
- **Language:** TypeScript
- **Entry Point:** CLI
- **Architecture Pattern:** Terminal agent with ACP protocol
- **MCP Status:** GitHub-native (ACP protocol)
- **Deployment:** npm install

---

### reasonix

**TypeScript | ~11.3K stars | May 2026**

**Status:** Active — DeepSeek-native coding agent

### Overview
reasonix (DeepSeek-Reasonix) is a DeepSeek-native AI coding agent for the terminal. Engineered around prefix-cache stability for low token costs across long sessions, it achieves ~99.82% cache hit rates. Built with Ink (React for CLI) for its TUI.

### Key Features
- **DeepSeek R1/v4 optimized** — Purpose-built for DeepSeek's reasoning models
- **Prefix-cache invariant** — Engineered for maximum prefix-cache stability
- **SEARCH/REPLACE edits** — Focused edit strategy for precision code changes
- **99.82% cache hit rates** — Low token costs across long coding sessions
- **TUI with Ink** — React-based terminal UI
- **Monorepo (npm)** — TypeScript architecture, Node ≥ 22

### Architecture
- **Language:** TypeScript (Node ≥ 22)
- **Entry Point:** `reasonix` CLI (npm package: `reasonix`)
- **Architecture Pattern:** CLI-first terminal coding agent
- **MCP Status:** None
- **Deployment:** npm install (`npm install -g reasonix`)
- **LLM Support:** DeepSeek (R1, v4)
- **License:** MIT

---

## openhuman

**Rust | Academic/Research | v0.53.49-staging — May 2026**

**Status:** Active — Research platform

### Overview
openhuman is a Rust-based Human Digital Twin platform (人类数字孪生) designed for creating digital representations of humans for research and simulation purposes.

### Key Features
- **Human Digital Twin** — Digital representation paradigm
- **Rust-native** — High performance and memory safety
- **Academic/research focus** — Scientific simulation and modeling
- **Staging branch active** — Active development on staging

### Architecture
- **Language:** Rust
- **Entry Point:** Application binary
- **Architecture Pattern:** Digital twin simulation platform
- **MCP Status:** N/A
- **Deployment:** Local

---

## Kimi CLI

**Python | ~8.8K stars | Apache-2.0 — May 2026**

**Status:** Active — MoonshotAI's CLI coding agent

### Overview
kimi-cli is MoonshotAI's CLI-based coding agent. Python-based with ACP (Agent Communication Protocol) support and a terminal TUI interface for interactive coding sessions.

### Key Features
- **Python-based** — Pure Python implementation for extensibility
- **ACP support** — Agent Communication Protocol for structured interactions
- **Terminal TUI** — Interactive terminal user interface
- **MoonshotAI integration** — Optimized for Moonshot AI models

### Architecture
- **Language:** Python
- **Entry Point:** CLI
- **Architecture Pattern:** Terminal coding agent with TUI
- **MCP Status:** ACP support
- **Deployment:** pip install
- **LLM Support:** MoonshotAI (Kimi)
- **License:** Apache-2.0

---

## Codex CLI

**Rust | ~86.9K stars | Apache-2.0 — May 2026**

**Status:** Active — OpenAI's official CLI coding agent

### Overview

codex is OpenAI's lightweight coding agent that runs in your terminal. Built in Rust for performance, it provides sandboxed execution for safe code operations. The highest-star CLI coding agent tracked by AllClaws.

### Key Features
- **Rust-native** — High-performance implementation in Rust
- **Sandboxed execution** — Safe code operations with isolation
- **Lightweight** — Minimal footprint terminal agent
- **OpenAI integration** — Optimized for OpenAI models (GPT-4, o-series)

### Architecture
- **Language:** Rust
- **Entry Point:** CLI
- **Architecture Pattern:** Terminal coding agent with sandboxed execution
- **MCP Status:** None
- **Deployment:** Binary install
- **LLM Support:** OpenAI (GPT-4, o-series)
- **License:** Apache-2.0

---

## Kimi Code

**TypeScript | ~1.4K stars | MIT — May 2026**

**Status:** Active — MoonshotAI's next-gen agent framework

### Overview
kimi-code is MoonshotAI's next-generation agent framework. A TypeScript monorepo with plugin architecture and MCP (Model Context Protocol) support for building extensible AI agent systems.

### Key Features
- **Plugin architecture** — Extensible plugin system for custom capabilities
- **MCP support** — Model Context Protocol for tool/context integration
- **TypeScript monorepo** — Modern, type-safe implementation
- **Next-gen framework** — Designed for building multi-purpose AI agents

### Architecture
- **Language:** TypeScript
- **Entry Point:** Application
- **Architecture Pattern:** Plugin-based agent framework
- **MCP Status:** Native
- **Deployment:** npm install
- **LLM Support:** MoonshotAI (Kimi)
- **License:** MIT

---

## External Frameworks (New Tracking)

### SmolAgents (Hugging Face)
**Python | ~26.7K stars | ~1K LOC core**

- Code-gen paradigm (agents write Python)
- Minimal viable framework reference
- Comparison: Nanobot tool-calling vs SmolAgents code-gen

### LangGraph
**Python/TS | Enterprise adoption**

- Graph-based orchestration
- Stateful workflows
- Enterprise pattern comparison

### CrewAI
**Python | Role-playing focus**

- Autonomous agents with roles
- Multi-agent coordination
- Enterprise use cases

### AutoGen
**Python | Microsoft origin**

- Conversational agent framework
- Multi-agent dialogue patterns
- Enterprise integration

### Swarms
**Python | ~5K stars | Enterprise focus**

- Enterprise orchestration
- Cloud deployment patterns
- Governance framework alignment

### OpenAgents
**TypeScript | Distributed networks**

- Distributed agent architecture
- Cloud-native design
- Network-based coordination

### OpenFang
**Rust | ~17.6K stars | v0.6.9 — May 2026**

**Status:** Active — Agent OS

### Overview
OpenFang is a Rust-based Agent OS deployed as a single binary (~32MB, 137K LOC across 14 crates). It uses a "Hands" architecture — autonomous capability packages for specific tasks — and supports 27 LLM providers with 123+ models. OpenClaw-compatible (SKILL.md, ClawHub).

### Key Features
- **7 pre-built Hands** — Lead, Clip, Researcher, Collector, Predictor, Twitter, Browser
- **Single binary** — Cross-platform deployment (macOS, Linux, Windows)
- **27 LLM providers, 123+ models** — Broadest provider coverage
- **Web dashboard** — Built-in management UI
- **WhatsApp gateway** — Native messaging integration
- **OpenClaw-compatible** — SKILL.md format, ClawHub, `migrate --from openclaw`
- **Guardrails** — Purchase approval gates for sensitive actions

### Architecture
- **Language:** Rust
- **Entry Point:** Single binary
- **Architecture Pattern:** Agent OS with Hands (autonomous capability packages)
- **MCP Status:** Adapter (topic tagged)
- **Deployment:** Cross-platform single binary (~32MB)
- **LLM Support:** 27 providers, 123+ models
- **Database:** SQLite

---

## AgentScope

**Python | ~25.8K stars | Apache-2.0 — May 2026**

**Status:** Active — Alibaba DAMO Academy's multi-agent framework

### Overview
AgentScope is a distributed multi-agent framework developed by Alibaba DAMO Academy. It provides a message hub architecture for agent communication and pipeline-based workflows for composing multi-agent collaboration patterns. Designed for both research and production use.

### Key Features
- **Distributed multi-agent collaboration** — Agents communicate via a centralized message hub
- **Message hub architecture** — Decoupled agent communication through message passing
- **Pipeline workflows** — Composable pipeline patterns for structuring multi-agent interactions
- **Python-native** — Pure Python implementation for research extensibility
- **Production-ready** — Supports distributed deployment scenarios

### Architecture
- **Language:** Python
- **Entry Point:** Python API
- **Architecture Pattern:** Distributed multi-agent with message hub + pipeline workflows
- **MCP Status:** N/A
- **Deployment:** pip install
- **LLM Support:** Multiple providers
- **License:** Apache-2.0

---

## Eliza

**TypeScript | MIT — May 2026**

**Status:** Active — Multi-platform AI agent framework

### Overview
Eliza is a TypeScript-based multi-platform AI agent framework developed by eliza-os. It provides a plugin architecture for building AI agents that can operate across multiple platforms and communication channels.

### Key Features
- **Multi-platform support** — Agents can operate across Discord, Telegram, Twitter, and more
- **Plugin architecture** — Extensible plugin system for custom capabilities
- **TypeScript-native** — Modern, type-safe implementation
- **MIT licensed** — Open-source with permissive licensing

### Architecture
- **Language:** TypeScript
- **Entry Point:** Application
- **Architecture Pattern:** Plugin-based multi-platform agent framework
- **MCP Status:** N/A
- **Deployment:** npm install
- **License:** MIT

---

## Agent Zero

**Python | MIT — May 2026**

**Status:** Active — Autonomous AI agent framework

### Overview
Agent Zero is a Python-based autonomous AI agent framework developed by frdel. It provides tool-use capabilities for building agents that can autonomously perform tasks using various tools and APIs.

### Key Features
- **Autonomous operation** — Agents can work independently toward goals
- **Tool-use capabilities** — Built-in support for using tools and APIs
- **Python-native** — Pure Python implementation for extensibility
- **MIT licensed** — Open-source with permissive licensing

### Architecture
- **Language:** Python
- **Entry Point:** Python API
- **Architecture Pattern:** Autonomous agent with tool-use
- **MCP Status:** N/A
- **Deployment:** pip install
- **License:** MIT

---

## PraisonAI

**Python | MIT — May 2026**

**Status:** Active — Multi-agent LLM framework

### Overview
PraisonAI is a Python-based multi-agent LLM framework developed by MervinPraison. It features a low-code workflow builder for creating multi-agent systems with minimal configuration.

### Key Features
- **Low-code workflow builder** — Create multi-agent workflows with minimal coding
- **Multi-agent orchestration** — Coordinate multiple agents for complex tasks
- **Python-native** — Pure Python implementation
- **MIT licensed** — Open-source with permissive licensing

### Architecture
- **Language:** Python
- **Entry Point:** Python API / CLI
- **Architecture Pattern:** Multi-agent LLM framework with low-code workflows
- **MCP Status:** N/A
- **Deployment:** pip install
- **License:** MIT

---

## Rocketride

**TypeScript | MIT — May 2026**

**Status:** Active — near.ai agent server

### Overview
Rocketride is a TypeScript-based agent server developed by nearai for the near.ai platform. It provides a server-side runtime for autonomous task execution by AI agents.

### Key Features
- **Server-side runtime** — Runs agents in a server environment
- **Autonomous task execution** — Agents can perform tasks autonomously
- **TypeScript-native** — Modern, type-safe implementation
- **near.ai integration** — Built for the near.ai ecosystem

### Architecture
- **Language:** TypeScript
- **Entry Point:** Server application
- **Architecture Pattern:** Agent server for autonomous task execution
- **MCP Status:** N/A
- **Deployment:** npm install
- **License:** MIT

---

## Fork Analysis: Personal vs Enterprise

| Aspect | Personal-Force-Multiplier | Enterprise-Automation |
|--------|-------------------------|----------------------|
| **Primary Concern** | Speed, cost | Governance, compliance |
| **Deployment** | Local, single-user | Cloud, multi-tenant |
| **Tool Access** | CLI, direct execution | MCP, protocols |
| **Examples** | OpenClaw, Nanobot, SmolAgents, Maxclaw, IronClaw, ZeroClaw, NanoClaw | LangGraph, Swarms, HiClaw, GoClaw, CrewAI, AutoGen, AgentScope |

---

## Comparative Snapshot

| Project | Stars | Language | MCP Status | Pattern |
|---------|-------|----------|-----------|---------|
| OpenClaw | ~340K | TypeScript | Adapter | Personal |
| ZeroClaw | ~29K | Rust | Adapter | Personal |
| IronClaw | Growing | Rust | Adapter | Personal/Enterprise |
| GoClaw | ~1.3K | Go | Adapter | Enterprise |
| Nanobot | ~37K | Python | None | Personal |
| NanoClaw | N/A | TypeScript | Resistant | Personal |
| ClawTeam | ~884 | Python | None | Personal |
| Maxclaw | ~189 | Go+TS | None | Personal |
| HiClaw | N/A | Go+Shell | Adapter | Enterprise |
| Hermes-Agent | N/A | Python | Native | Personal |
| Claw-AI-Lab | N/A | Python | N/A | Academic |
| SmolAgents | ~26.7K | Python | N/A | Personal |
| LangGraph | N/A | Py/TS | N/A | Enterprise |
| CrewAI | N/A | Python | N/A | Enterprise |
| AutoGen | N/A | Python | N/A | Enterprise |
| Swarms | ~5K | Python | N/A | Enterprise |
| OpenAgents | N/A | TypeScript | N/A | Enterprise |
| OpenFang | ~17.6K | Rust | Adapter | Personal |
| aider | ~68K | Python | None | Personal |
| copilot-cli | N/A | TypeScript | ACP | Personal |
| reasonix | ~11.3K | TypeScript | None | Personal |
| openhuman | N/A | Rust | N/A | Academic |
| Kimi CLI | ~8.8K | Python | ACP | Personal |
| Kimi Code | ~1.4K | TypeScript | Native | Personal/Enterprise |
| Codex CLI | ~86.9K | Rust | None | Personal |
| AgentScope | ~25.8K | Python | N/A | Enterprise |
| Eliza | N/A | TypeScript | N/A | Personal/Enterprise |
| Agent Zero | N/A | Python | N/A | Personal |
| PraisonAI | N/A | Python | N/A | Personal/Enterprise |
| Rocketride | N/A | TypeScript | N/A | Enterprise |
| OpenWorker | ~9.8K | Python/Rust | Native | Personal/Enterprise |
| Dify | ~150K | TypeScript/Python | Native | Enterprise |
| MetaGPT | ~69K | Python | N/A | Enterprise |
| Qwen-Agent | ~16K | Python | Native | Personal/Enterprise |
| browser-use | ~110K | Python | Native (server) | Personal |

---

*Last updated: August 20, 2026*
*Part of: AllClaws Personal AI Agent Ecosystem Research*
*Platforms tracked: 35 (11 claw ecosystem + 18 external frameworks + 5 CLI coding agents + 1 human digital twin)*
*Next update: September 2026*
