# Agent Harnesses & Toolchains

**[English](agent_harnesses.md)** | [中文](agent_harnesses.zh-CN.md)

> Infrastructure and tooling for running CLI-based AI agents at scale. Unlike agent platforms that provide the AI capabilities, harnesses provide the execution, coordination, and observability layer.

---

## Overview

Agent harnesses sit **below** agent platforms in the stack:

```
┌─────────────────────────────────────────────────────────────┐
│  Agent Platforms (OpenClaw, ClawTeam, SmolAgents, etc.)    │
│  - Provide AI capabilities, tools, and agent logic          │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  Agent Harnesses & Toolchains (this document)               │
│  - Execution runtime, coordination, observability           │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  Foundation (LLM APIs, MCP, Docker, Git)                   │
└─────────────────────────────────────────────────────────────┘
```

**Tracked Ecosystems:**
- **UltraWorkers Toolchain** — Rust + Node.js autonomous development system
- **Darwin Agent HarnessX** — Python agent harness foundry with composable processors and evolution engine
- **OmniCoreAgent** — Python production agent harness with MCP, memory, subagents, REST serving
- **Harmonist** — Python portable multi-agent orchestration with mechanical protocol enforcement
- **SIA** — Python self-improving AI framework with harness + weight co-improvement
- **DeepSeek Harness (dsh)** — TypeScript plugin-tree harness from DeepSeek, built on Cordis composition (added August 2026)
- **Pi** — TypeScript self-extensible coding-agent harness from Earendil Works (added August 2026)

---

## UltraWorkers Toolchain

**Philosophy:** *"Humans set direction; claws perform the labor."*

### The Three-Part System

```
┌──────────────────────────────────────────────────────────────┐
│                     Discord Chat Interface                    │
│  (Human types directive from phone, walks away)             │
└──────────────────────────────────────────────────────────────┘
                            ↓
┌──────────────┬──────────────┬────────────────────────────────┐
│   OmX        │   clawhip    │            OmO                 │
│ (oh-my-codex) │              │   (oh-my-openagent)            │
│              │              │                                │
│  Workflow    │   Event      │   Multi-Agent                  │
│    Layer     │   Router     │   Coordination                 │
│              │              │                                │
│  Planning →  │  Git/GitHub/ │   Architect → Executor →        │
│  Execution   │  tmux/Agent  │   Reviewer convergence         │
│    modes     │   events     │                                │
└──────────────┴──────────────┴────────────────────────────────┘
                            ↓
┌──────────────────────────────────────────────────────────────┐
│                    claw-code (Rust CLI)                      │
│              The actual agent harness                        │
└──────────────────────────────────────────────────────────────┘
```

### 1. claw-code

**Repository:** [ultraworkers/claw-code](https://github.com/ultraworkers/claw-code)
**Language:** Rust
**Status:** Active (~100K stars claimed)

**Overview:**
Public Rust implementation of the "claw CLI agent harness" — a clean-room rewrite of the Claude Code agent harness architecture.

**Key Stats (April 2026):**
- 292 commits on main / 293 across all branches
- 9 crates, 48,599 tracked Rust LOC
- 2,568 test LOC
- 3 authors (Mar 31 - Apr 3, 2026 development burst)

**Architecture:**

```rust
// Core components
rust/
├── crates/
│   ├── rusty-claude-cli/     // Main CLI binary
│   ├── runtime/              // Bash, sandbox, task registry
│   ├── tools/                // 40 exposed tool specs
│   ├── mock-anthropic-service/  // Testing harness
│   └── ... (5 more crates)
```

**Key Features:**
- **9-lane parity checkpoint** with Claude Code architecture
- **40 tool specs** including bash, file ops, MCP, LSP, team/cron
- **Mock parity harness** for deterministic testing
- **Permission enforcement** layer with workspace boundaries
- **MCP lifecycle bridge** for tool surface integration

**The "Clawable" Philosophy:**

A clawable harness is:
- Deterministic to start
- Machine-readable in state and failure modes
- Recoverable without human watching terminal
- Branch/test/worktree aware
- Plugin/MCP lifecycle aware
- Event-first, not log-first
- Capable of autonomous next-step execution

**Roadmap Highlights:**

| Phase | Focus | Status |
|-------|-------|--------|
| 1 | Reliable Worker Boot | 🔄 In progress |
| 2 | Event-Native clawhip Integration | 🔄 In progress |
| 3 | Branch/Test Awareness | Planned |
| 4 | Claws-First Task Execution | Planned |
| 5 | Plugin/MCP Lifecycle Maturity | Planned |

**Affiliation:** Explicitly NOT affiliated with Anthropic — ownership disclaimer included.

---

### 2. oh-my-codex (OMX)

**Repository:** [Yeachan-Heo/oh-my-codex](https://github.com/Yeachan-Heo/oh-my-codex)
**Language:** Node.js (TypeScript)
**Role:** Workflow layer

**Overview:**
OMX is a workflow layer for OpenAI Codex CLI. It keeps Codex as the execution engine and adds:
- Stronger default session startup
- Canonical workflows (`$deep-interview`, `$ralplan`, `$team`, `$ralph`)
- Project guidance through scoped `AGENTS.md`
- Durable state under `.omx/`

**Canonical Workflow:**

```bash
# Start OMX strongly
omx --madmax --high

# Then use the canonical workflow:
$deep-interview "clarify the authentication change"
$ralplan "approve the safest implementation path"
$ralph "carry the approved plan to completion"
$team 3:executor "execute in parallel"
```

**What OMX Does:**
- Converts short directives into structured execution
- Planning keywords, execution modes, persistent verification loops
- Parallel multi-agent workflows
- Role-based specialist invocation

**Design Philosophy:**
OMX does NOT replace Codex. It adds:
- Better task routing
- Better workflow
- Better runtime

---

### 3. clawhip

**Repository:** [Yeachan-Heo/clawhip](https://github.com/Yeachan-Heo/clawhip)
**Language:** Rust
**Role:** Event and notification router

**Overview:**
Daemon-first Discord notification router with a typed event pipeline, extracted sources, and clean renderer/sink split.

**System Model:**

```
[CLI / webhook / git / GitHub / tmux]
           ↓
    [sources]
           ↓
    [mpsc queue]
           ↓
   [dispatcher]
           ↓
[router → renderer → Discord/Slack sink]
           ↓
[Discord REST / Slack webhook delivery]
```

**Key Features (v0.3.0):**
- **Typed event model** — normalized and validated envelopes
- **Multi-delivery router** — one event → zero, one, or many deliveries
- **Source extraction** — git, GitHub, tmux as explicit sources
- **Sink/render split** — rendering separated from transport

**Provider-Native Hooks:**

Shared v1 hook events for Codex + Claude:
- `SessionStart`
- `PreToolUse`
- `PostToolUse`
- `UserPromptSubmit`
- `Stop`

**Philosophy:**
Clawhip keeps monitoring and delivery **outside** the coding agent's context window so agents can stay focused on implementation instead of status formatting and notification routing.

---

### 4. oh-my-openagent (OmO)

**Repository:** [code-yeongyu/oh-my-openagent](https://github.com/code-yeongyu/oh-my-openagent)
**Role:** Multi-agent coordination

**Overview:**
Handles planning, handoffs, disagreement resolution, and verification loops across agents.

**When Architect, Executor, and Reviewer disagree, OmO provides the structure for that loop to converge instead of collapse.**

---

## Darwin Agent HarnessX

**Repository:** [Darwin-Agent/HarnessX](https://github.com/Darwin-Agent/HarnessX)
**Language:** Python 3.11+
**License:** MIT
**Stars:** 241
**Created:** April 2026

**Philosophy:** *"The harness — not just the model — determines agent performance."*

### Overview

HarnessX is a **harness foundry**: a framework for composing, adapting, and evolving agent harnesses independently of the underlying model. It formalizes the harness as a first-class typed object with nine behavioral dimensions, each implemented as pluggable processors attached to lifecycle hooks.

The core insight: `agent = model.agentic(harness)` — model configuration and harness configuration are orthogonal concerns, independently substitutable.

### Architecture

```
harnessx/
├── core/              # Harness, Builder, RunLoop, State, Events, Trajectory
├── processors/        # 7 categories × multiple processors
│   ├── context/       # System prompt, history, user wrapper
│   ├── control/       # 13 safety & reliability processors
│   ├── evaluation/    # LLM judge, PRM, self-verify
│   ├── memory/        # Extraction, retrieval, 5 strategies
│   ├── multi_model/   # Model routing
│   ├── observability/ # OTel, checkpoints, metrics
│   └── tools/         # Skill loader, schema adapter, filters
├── providers/         # 6 model backends + agentic mixin
├── plugins/           # Plugin base, discovery, builtins, dimensions
├── sandbox/           # Local, Docker, E2B
├── tracing/           # Journal, OTel, null tracer
├── rl/                # RLConfigSpec, TaskBuilder
└── bundles/           # Pre-composed capability bundles
```

### Key Features

- **9-dimension behavior pipeline** — model, context, memory, tools, execution env, evaluation, control/safety, observability, training bridge
- **Processor composition** — processors combine with `|` operator; attach to 8 lifecycle hooks (task_start through task_end)
- **MetaHarness** — the agent observes its own trajectories and proposes harness config changes; sandboxed promotion loop with deterministic gating
- **Harness Evolution** — trace-driven auto-optimization: Qwen 3.5 9B on GAIA goes from 33% → 47% with zero model changes; GPT-5 goes from 62% → 84%
- **Model-Harness Co-Evolution** — interleaved GRPO training over shared replay buffer: Qwen 3.5 9B on GAIA reaches 55.77% (+64% relative)
- **Lab UI** — React + TypeScript browser interface for harness configuration (`hx lab`)
- **IM Gateway** — connects agents to Feishu, Telegram, Slack, Discord, DingTalk
- **Plugin system** — dimensions, processors, memory backends all pluggable
- **Benchmark suite** — GAIA, ALFWorld, SWE-bench Verified, LoCoMo integrations

### Key Stats (July 2026)

- 868 files, ~60 MB
- 505 Python source files
- Extensive test suite (test_processor, test_builder, test_model_router, test_journal, etc.)
- MIT License — fully open-source

### Comparison with UltraWorkers

| Aspect | UltraWorkers (claw-code) | HarnessX |
|--------|--------------------------|----------|
| **Approach** | Production harness for CLI agents | Research framework for harness composition |
| **Language** | Rust (48K+ LOC) | Python 3.11+ |
| **Composability** | Crate-level modularity | Processor-level composition with substitution algebra |
| **Evolution** | Manual iteration | Trace-driven AEGIS-style auto-optimization |
| **Model Training** | N/A | Built-in GRPO co-evolution bridge via VERL |
| **UI** | Discord-first | CLI + Lab UI + IM Gateway |
| **Target** | Deploy and run agents at scale | Research, experiment, and evolve harness design |
| **Licensing** | Public (disclaimed) | MIT |

### Roadmap

| Phase | Focus | Status |
|-------|-------|--------|
| 1 | Core pipeline, 13 processors, 4 benchmarks, Lab UI, SFT/RL bridge | Current |
| 2 | Bayesian Optimization, MetaHarness, auto config search | In progress |
| 3 | Closed-loop self-evolution, HarnessHUB marketplace (`hx pull coding-agent@v1.2`) | Planned |
| 4 | Multimodal memory, third-party integrations (VERL, SuperMemory, OpenVKing) | Planned |

### Relevance to AllClaws

HarnessX is the **academic reference implementation** for the evolutionary harness concepts discussed in the "Evolutionary Harness Architectures" section below. It provides:
- Production-grade code validating the harness-as-first-class-object thesis
- Empirical evidence for the inverse-scaling pattern (weaker models gain more from harness evolution)
- A clean plugin architecture that could inform future AllClaws benchmark harness design
- The MetaHarness component as a working example of trace-driven self-optimization

### Reference

```bibtex
@software{harnessx2026,
  title   = {HarnessX: A Composable, Self-Evolving Agent Harness Foundry},
  author  = {Darwin Agent Team},
  year    = {2026},
  url     = {https://github.com/Darwin-Agent/HarnessX},
  license = {MIT},
}
```

---

## OmniCoreAgent

**Repository:** [omnirexflora-labs/omnicoreagent](https://github.com/omnirexflora-labs/omnicoreagent)
**Language:** Python 3.10+
**License:** MIT
**Stars:** 244
**Created:** March 2025

**Philosophy:** *"A library gives you pieces to assemble. A harness gives you the runtime boundary that makes a model usable inside an application."*

### Overview

OmniCoreAgent is the most explicitly harness-labeled project in the open-source ecosystem — it self-identifies as "The Open Production Agent Harness for Python." It distinguishes itself from agent libraries by providing a complete runtime boundary rather than a toolkit you assemble yourself.

### Architecture

The harness layers around a model:

```
model
  + prompt contract
  + reasoning loop
  + local tools
  + MCP tools
  + parallel tool batches
  + structured observations
  + memory
  + context control
  + workspace files
  + tool-output offloading
  + guardrails
  + events
  + subagents
  + background tasks
  + REST/SSE serving (OmniServe)
```

### Key Features

- **Parallel tool batching** — executes independent tool calls concurrently
- **Structured observations** — typed observation schemas instead of raw tool output
- **Signature loop detection** — catches and breaks infinite reasoning loops
- **MCP integration** — native MCP client for external tool servers
- **Memory & workspace** — persistent context and file-based workspace
- **Subagents** — spawn child agents for decomposed tasks
- **Background tasks** — async task execution outside the main reasoning loop
- **Guardrails** — configurable safety rules and constraints
- **OmniServe** — REST/SSE serving boundary for production deployment
- **Explicit layer separation** — model intelligence vs harness infrastructure clearly delineated

### Key Stats (July 2026)

- 244 ⭐, 57 forks
- PyPI package: `omnicoreagent`
- Published on PyPI with download tracking
- Online docs at docs-omnicoreagent.omnirexfloralabs.com

### Relevance to AllClaws

OmniCoreAgent is the most architecturally pure example of the harness-as-distinct-layer philosophy that AllClaws studies. Its explicit split between "agent harness" and "serving boundary" layers, combined with MCP integration, makes it a reference point for evaluating how other ecosystems (claw, UltraWorkers, HarnessX) implement the same concepts.

---

## Harmonist

**Repository:** [GammaLabTechnologies/harmonist](https://github.com/GammaLabTechnologies/harmonist)
**Language:** Python 3.9+
**License:** MIT
**Stars:** 2,292
**Created:** April 2026

**Philosophy:** *"Most AI coding frameworks trust the language model to follow the rules. Harmonist refuses to let it skip them."*

### Overview

Harmonist is a drop-in multi-agent orchestration framework for AI coding assistants (Cursor, Claude Code, Copilot, Windsurf, Aider). Its defining innovation is **mechanical protocol enforcement**: every code-changing turn is gated by hooks that verify reviewers ran, memory was updated, and every shipped file's supply chain is intact — before the turn completes.

### Architecture

```
harmonist/
├── agents/          # 193+ pre-built agent definitions
├── hooks/           # Mechanical enforcement gates
├── memory/          # Structured validated memory system
├── protocols/       # Per-agent protocol definitions
└── integration/     # Drop-in integrations for IDEs
```

### Key Features

- **193+ pre-built agents** — catalogued, versioned agent definitions
- **Mechanical protocol enforcement** — hooks gate every code-changing turn, not prompt suggestions
- **Zero runtime dependencies** — stdlib-only Python, no pip install required
- **550+ tests** — comprehensive test coverage
- **Drop-in integration** — works with Cursor, Claude Code, Copilot, Windsurf, Aider
- **Structured validated memory** — memory updates are verified, not just requested
- **Supply chain integrity** — every shipped file must pass protocol checks
- **Built by GammaLab** — commercially maintained with CI/CD

### Key Stats (July 2026)

- 2,292 ⭐, 229 forks
- v1.2.3 release
- 193 agents catalogued
- 550+ tests
- stdlib-only — zero pip dependencies

### Relevance to AllClaws

Harmonist is the largest open-source multi-agent orchestration framework by adoption. Its mechanical enforcement approach — protocol gates that cannot be skipped by the model — is a concrete implementation of the "deterministic gating" concept from HarnessX's AEGIS. It also validates AllClaws' observation that multi-agent coordination is a distinct harness concern requiring its own infrastructure layer.

---

## SIA (Self-Improving AI)

**Repository:** [hexo-ai/sia](https://github.com/hexo-ai/sia)
**Language:** Python 3.11+
**License:** MIT
**Stars:** 2,018
**Created:** March 2026

**Paper:** arXiv:2605.27276 (Hebbar et al., 2026)

**Philosophy:** *"SIA is a self-improving loop where a language-model agent updates both the harness and the weights of a task-specific agent."*

### Overview

SIA is the closest open-source counterpart to HarnessX's co-evolution concept. It implements a three-agent improvement loop (Meta, Target, Feedback) that autonomously refines a task-specific agent through successive generations — improving both the agent's configuration (harness) and its model weights.

### Architecture

```
Meta-Agent          Target Agent         Feedback Agent
    │                    │                     │
    │ generates initial   │ attempts task       │ reviews logs
    │ Target Agent ──────►│ and records ───────►│ proposes improvements
    │                    │ actions              │ updates Target
    │                    │                     │
    └──── iteration loop over generations ──────┘
```

### Key Features

- **Meta-Agent** — reads task description, generates initial Target Agent
- **Target Agent** — task-specific agent that executes and records
- **Feedback Agent** — reviews performance logs, identifies improvements, updates Target
- **Harness + weight co-improvement** — both configuration and model weights evolve
- **Built-in task suite** — ships with benchmark tasks for immediate evaluation
- **Visualizer** — run visualization tool for monitoring improvement trajectories
- **PyPI package** — `sia-agent` for easy installation
- **Paper-backed** — full academic paper with benchmark results

### Published Results (from arXiv:2605.27276)

| Benchmark | Gain |
|-----------|------|
| LawBench | +56.6% |
| GPU Kernels (runtime reduction) | −91.9% |
| Single-cell RNA denoising | +502% |
| MLE-Bench Hard (Kaggle) | Competitive |

### Key Stats (July 2026)

- 2,018 ⭐, 241 forks
- PyPI: `sia-agent`
- 16 open issues
- Active CI pipeline

### Relevance to AllClaws

SIA is the open-source counterpart to HarnessX's co-evolution research. While HarnessX provides the theoretical framework (operational mirror, AEGIS, cross-harness GRPO), SIA provides the engineering counterpart with a simpler three-agent architecture and demonstrated gains across diverse domains (legal, systems, bio). The pair together — HarnessX for theory, SIA for practice — covers the full spectrum of self-improving harness research that AllClaws tracks.

### Reference

```bibtex
@article{hebbar2026sia,
  title   = {SIA: Self Improving AI with Harness & Weight Updates},
  author  = {Hebbar et al.},
  year    = {2026},
  journal = {arXiv:2605.27276},
}
```

---

## DeepSeek Harness (dsh)

**Repository:** [deepseek-ai/deepseek-harness](https://github.com/deepseek-ai/deepseek-harness)
**Language:** TypeScript (pnpm monorepo) + Python SDK
**License:** MIT
**Stars:** ~158.8K (as of August 17, 2026)
**Created:** August 13, 2026
**Version:** v0.1.0-rc.7 (developer preview — breaking changes expected)

**Philosophy:** *"Everything is a Plugin."*

### Overview

DeepSeek Harness is the first first-party agent harness from a frontier model vendor. Built on [Cordis](https://github.com/cordiverse/cordis) — a composition framework described in the paper *A Programming Paradigm for Spatiotemporal Composability* — dsh treats the entire product as a plugin tree: the model adapter, tool registry, session log, and the agent loop itself are all plugins, replaceable from configuration. There is no privileged core to patch.

### Architecture

- **Cordis context**: plugins contribute services, typed events, and reversible effects to a shared context; registrations unwind when their plugin unloads
- **Three event domains**: session events (durable, appended to the log), agent events (`agent/*` — observe/intercept in-flight work), capability events (`fs/*`, `tools/*`, `telemetry/*` — attach policy at seams without importing the loop). Waterfall events (`agent/pre-step`, `agent/request`, `llm/stream`, `tools/*`) require `next()` delegation
- **Turn/step state machine**: a turn opens before its first input claim and closes once nothing is owed; `agent/pre-step` may rewrite or reject claimed messages — a rejected turn still closes durably, recording the attempt
- **Session log as single source of truth**: "Model-visible means logged" is a runtime-inforced invariant — fork, resume, transcripts, telemetry, and persistence all derive from the append-only `SessionEvent` stream
- **Capability seams**: swappable Service Definition / Provider / Consumer triples; pointing `ctx.fs` + `ctx.subprocess` at a remote sandbox moves Bash, PTY, and LSP together with no provider forks. Subagent providers range from child agents to delegated turns in another product
- **Profile/bundle layering**: compositions of ordered bundle layers (`dsh-base` → `dsh-web-app` / `dsh-headless`), every config row patchable by higher layers

### Key Stats (August 2026)

- 158.8K stars, 16.5K forks within 4 days of release — the fastest launch in the harness category
- Web UI first (`dsh web`), headless one-shot runner, Python SDK
- Bilingual documentation (EN/ZH) with generated config catalog and extension cookbook

### Relevance to AllClaws

dsh is the strongest evidence yet for harness engineering as a distinct discipline: a frontier model vendor concluded that the harness layer — not the model — is where product differentiation lives. Its "everything is a plugin" composition algebra operationalizes the substitution property HarnessX theorized (typed, independently replaceable processors). The rc status makes it a MONITOR-tier candidate under Q4-7: architecturally essential, version-wise premature. Its event-waterfall design (mandatory `next()` delegation) is the most formal interception seam in any tracked or candidate harness.

---

## Pi

**Repository:** [earendil-works/pi](https://github.com/earendil-works/pi)
**Language:** TypeScript (npm monorepo)
**License:** MIT
**Stars:** ~93.0K (as of August 18, 2026)
**Created:** August 2025 (one year of production iteration)
**Version:** Multi-package npm releases with SHA256SUMS-signed source archives

**Philosophy:** *"A self-extensible coding agent — ask it to build the extension you need."*

### Overview

Pi is a pragmatic agent harness from Earendil Works (led by Mario Zechner/badlogic, with Armin Ronacher/mitsuhiko as the #2 contributor). Where dsh is a composition constitution, Pi is a layered toolkit: five packages (pi-agent-core, pi-ai, pi-coding-agent, pi-tui, pi-telemetry) with a stable core and TypeScript-module extensions growing at the edges.

### Architecture

- **Extension model**: TS modules registering tools (`pi.registerTool()`), commands, event subscriptions (block/modify tool calls, inject context, customize compaction), custom TUI components (`ctx.ui`), and session-persistent state (`pi.appendEntry()`) — hot-reloadable from `~/.pi/agent/extensions/` or `.pi/extensions/`
- **Self-extension as paradigm**: the README's first extension doc line is "pi can create extensions — ask it to build one for your use case." The agent authoring its own harness extensions is the product thesis
- **Deliberately no permission system**: filesystem/process/network/credential boundaries are out of harness scope; three documented containerization patterns (Gondolin micro-VM extension, plain Docker, OpenShell policy sandbox) externalize isolation
- **Compaction engineering**: auto-compaction plus branch summarization with structured summary formats, cumulative file tracking, and cache-aware one-off prompts — compaction and branch-summary requests use fresh routing session IDs and disable prompt-cache writes because they won't be reused
- **Vendor-neutral telemetry**: pi-telemetry defines provider-independent contracts, a reference adapter, conformance tests, and typed schemas — telemetry as a first-class package
- **Supply-chain hardening**: dependencies pinned to exact versions, npm changes treated as reviewed code changes, reproducible offline builds from signed source archives

### Key Stats (August 2026)

- 93.0K stars, 11.5K forks, 1 year old
- Top contributors: badlogic (3,539 commits), mitsuhiko (526), christianklotz (142)
- Test suite with faux provider (no real API calls or paid tokens in CI)

### Relevance to AllClaws

Pi represents the applied pole of the harness discipline: a year of production polish in exactly the areas the 34-platform comparison found weakest — compaction detail (cache-aware summarization), telemetry contracts, and self-extension. Its refusal to ship a permission system is a philosophical position ("boundaries are a deployment concern, not a harness concern") that inverts dsh's sandbox-seam approach — the two stances bracket the A2 guardrail design space. With a one-year history, 93K stars, and Ronacher's involvement, Pi passes the admission bar without the "too new" caveat that dsh carries. Both are Q4-7 harness-category candidates: dsh as composition formalism, Pi as extension pragmatism.

---

## Comparison with Agent Platforms

| Aspect | Agent Platforms | Agent Harnesses |
|--------|----------------|-----------------|
| **Purpose** | Provide AI capabilities | Provide execution/coordination |
| **Core Value** | Intelligence, tools, skills | Reliability, observability, automation |
| **User Interface** | Chat, CLI, API | Events, hooks, APIs |
| **Typical User** | End users, developers | Agents, orchestrators, ops |
| **Example** | OpenClaw, SmolAgents | claw-code, clawhip |
| **Analogy** | The engine | The transmission, dashboard, pit crew |

---

## Key Patterns

### 1. Event-First Architecture

Harnesses emit typed events, not log text:
- `lane.started`, `lane.ready`, `lane.blocked`
- `agent.started`, `agent.blocked`, `agent.finished`
- `git.commit`, `github.pr-opened`

This enables machine-readable state instead of scraping prose.

### 2. Recovery Before Escalation

Known failure modes should auto-heal once before asking for help:
- Trust prompt resolution
- Prompt misdelivery detection
- Stale branch detection
- MCP startup failures

### 3. Discord as Human Interface

The important interface is not tmux, Vim, or SSH. It's a Discord channel:
- Type a sentence from phone
- Walk away, sleep, do something else
- Claws read directive, break into tasks, assign roles
- Write code, run tests, argue over failures
- Recover and push when work passes

### 4. Three-Part Coordination

1. **OmX** — Directive → structured work protocol
2. **clawhip** — Event routing outside agent context
3. **OmO** — Multi-agent convergence

---

## Emerging Trends

### 1. Rust Adoption

claw-code (48K+ LOC) demonstrates Rust as a serious language for agent harnesses:
- Memory safety for long-running daemons
- Performance for event routing
- Type safety for event schemas

### 2. Clean-Room Reimplementations

claw-code is a "clean-room rewrite of Claude Code agent harness architecture" — suggesting:
- Strong demand for open alternatives
- Architectural patterns worth replicating
- Community ownership of infrastructure

### 3. Discord as Operations Center

Moving human oversight from terminal to chat:
- Asynchronous notification
- Multi-device access (phone, desktop)
- Bot-friendly API
- Persistent context

### 4. Machine-Readable State

Shift from human-readable logs to structured events:
- Enables agent-to-agent communication
- Automated recovery
- Dashboard layer separate from data

---

## Evolutionary Harness Architectures

> Trace-driven, self-adapting harnesses that improve through structured execution feedback — a paradigm shift from static hand-engineering to learned optimization.

### The Static-Harness Problem

Every agent harness in production today is **hand-crafted and frozen**: prompts, tool wrappers, retry policies, and memory strategies are authored once and never improve from execution experience. When a model version changes, a new tool appears, or a task domain shifts, the harness requires bespoke manual re-engineering. Execution traces — which contain rich diagnostic signal about *why* an agent succeeded or failed — are discarded.

The HarnessX paper (Darwin Agent Team, "HarnessX: A Composable, Adaptive, and Evolvable Agent Harness Foundry", arXiv:2606.14249, July 2026) establishes the theoretical foundation for moving beyond this ceiling: **harness evolution as a first-class learning problem**.

### The Nine-Dimensional Harness Taxonomy

HarnessX formalizes a harness as a typed, composable object spanning nine behavioral dimensions:

| Dimension | Role | What It Controls |
|-----------|------|-----------------|
| D1: Model Selection | Which model serves which role | Main agent, judge, evaluator, fallback policies |
| D2: Context Assembly | What the model sees | System prompt, history editing, context window trimming |
| D3: Memory Management | What persists across steps/sessions | Working memory, long-term store, retrieval policies |
| D4: Tool Ecosystem | What the agent can invoke | Tool registry, schemas, MCP servers, sandboxed execution |
| D5: Execution Environment | Where side-effects materialize | Sandbox, workspace, filesystem boundaries |
| D6: Evaluation & Reward | How outcomes are judged | Verifiers, scoring functions, pass/fail criteria |
| D7: Control & Safety | Rules constraining execution | Budget limits, loop detection, approval gates, permission policies |
| D8: Observability | What gets recorded | Full execution traces, event logs, structured diagnostics |
| D9: Training Bridge | Feedback → model signal | Trajectory records, replay buffer, RL training loop |

Each dimension is implemented as typed **processors** attached to lifecycle hooks (task_start, step_start, before_model, after_model, before_tool, after_tool, step_end, task_end). Processors are independently substitutable — a key property enabling programmatic evolution.

### Trace-Driven Harness Evolution (AEGIS)

AEGIS (Adaptive Engine for General Intelligence Scaffolding) is HarnessX's evolution engine. It operates as a four-stage pipeline, all driven by a single meta-agent LLM:

```
Digester           Planner            Evolver             Critic + Gate
  │                   │                   │                     │
  │ compresses        │ constructs        │ produces typed      │ validates and
  │ raw traces →      │ adaptation        │ builder edits       │ deterministically
  │ structured        │ landscape         │ with change         │ ships or rejects
  │ summaries         │ (what failed,     │ manifests           │ (seesaw constraint)
  │                   │  what's untried)  │                     │
```

**The Operational Mirror.** AEGIS maps harness evolution onto RL concepts:
- Harness configuration = state
- Typed harness edit = action
- Execution trace + verifier score = feedback
- Deterministic acceptance gate = transition function

This mapping is predictive: three well-known RL pathologies reappear in symbolic harness evolution and each requires a dedicated defense:
1. **Reward hacking** — edits that exploit verifier format rather than solving tasks → Critic catches via trace inspection
2. **Catastrophic forgetting** — edits improving one task silently regress another → deterministic gating enforces "no regression on previously solved tasks"
3. **Under-exploration** — pipeline converges on low-risk local edits (prompt tweaks) → Planner constructs landscape spanning structural changes before edit generation

### Empirical Results

Across five benchmarks (GAIA, ALFWorld, WebShop, τ³-Bench, SWE-bench Verified) and three task-agent families (Claude Sonnet 4.6, GPT-5.4, Qwen3.5-9B):

| Benchmark | Avg Gain | Max Gain | Key Insight |
|-----------|----------|----------|-------------|
| ALFWorld | +25.4% | +44.0% (Qwen3.5-9B) | Weaker models benefit most — harness closes behavioral gaps |
| WebShop | +15.7% | +18.0% | Prompt + processor edits reduce search/pagination loops |
| GAIA | +8.9% | +17.1% (Qwen3.5-9B) | Tool-level edits (WikiTextFetch) unlock retrieval failures |
| SWE-bench | +15.8% | +18.2% | Gains only for capable models; 9B model hits capability floor |
| τ³-Bench | +7.0% | +14.5% | Near-ceiling baselines leave less headroom |

**The Inverse-Scaling Pattern.** Gains scale inversely with baseline performance. Qwen3.5-9B, the weakest task agent, gains +44.0% on ALFWorld — the evolved harness provides structural support that the model's own reasoning cannot supply. Stronger models (Sonnet 4.6) gain less because they self-correct more failures internally.

**Variant Isolation.** On heterogeneous benchmarks like GAIA (103 tasks spanning retrieval, reasoning, visual, document-parsing), a single harness cannot improve all tasks simultaneously — edits helping one cluster silently regress another. HarnessX introduces **ensemble routing**: maintain up to K harness variants, route each task to the variant with highest prior success, and fork new variants when an edit improves a subset while regressing another. On GAIA + GPT-5.4, this lifts a stagnating ∆=0.0 to +13.6% with a non-degrading trajectory.

### Harness-Model Co-Evolution

The most advanced mode interleaves harness evolution with model reinforcement learning over a shared replay buffer:

```
         ┌─────────────────────────────────────────┐
         │           Shared Replay Buffer            │
         │  (trajectories from multiple harness      │
         │   versions + model checkpoints)           │
         └──────────────┬──────────────────────────┘
                        │
          ┌─────────────┴─────────────┐
          │                           │
    ┌─────▼──────┐            ┌───────▼───────┐
    │   AEGIS    │            │ Cross-Harness │
    │  Harness   │            │    GRPO       │
    │  Evolution │            │ Model Training│
    └────────────┘            └───────────────┘
```

Cross-harness GRPO groups trajectories by task identity across harness versions, computing group-relative advantages so the model learns successful strategies regardless of which harness version produced them. Co-evolution adds +4.7% over harness-only evolution by breaking two ceilings simultaneously:
- **Scaffolding ceiling**: a frozen model eventually cannot exploit further harness improvements
- **Training-signal ceiling**: a fixed harness never surfaces context that would exercise newly trained capabilities

### Relevance to AllClaws Research

The HarnessX framework directly validates and extends several AllClaws research themes:

1. **The Harness as a Distinct Layer.** AllClaws already positions harnesses below agent platforms in the stack. HarnessX formalizes *why* this separation matters: the harness is an independent optimization surface with its own composition algebra, learning dynamics, and failure modes.

2. **The 1PC vs Enterprise Fork.** The inverse-scaling result suggests a new dimension to the fork: **small-model + evolved-harness** may be the economical path for personal (1PC) deployments, while **large-model + static-harness** characterizes enterprise deployments where hand-tuning is amortized across many users. HarnessX's variant isolation also provides a mechanism for the multi-tenant harness problem (different users need different harness behaviors).

3. **Claims Verification.** HarnessX distinguishes between *procedural memory* (AEGIS — symbolic harness adaptation using execution traces) and *autonomous learning* (cross-harness GRPO — model parameters improve from experience). This is precisely the distinction AllClaws' MISSION draws when evaluating "self-improving" claims.

4. **MCP and Tool Ecosystems.** D4 (Tool Ecosystem) in HarnessX's taxonomy formalizes what AllClaws tracks as MCP adoption vs resistance. The substitution algebra lets tools be swapped without touching other harness components — the theoretical backing for the MCP lifecycle bridge in claw-code.

5. **Observability as a First-Class Concern.** D8 (Observability) confirms AllClaws' emphasis on event-first architectures: structured traces are not merely debugging aids but the *fuel* for harness evolution. clawhip's typed event pipeline and claw-code's mock parity harness are concrete instantiations of this principle.

### Open Questions

1. **Meta-agent capability floor.** HarnessX uses Claude Opus 4.6 as the meta-agent. Can weaker/cheaper meta-agents drive evolution with comparable gains? This directly affects the economics of 1PC harness evolution.
2. **Held-out generalization.** HarnessX reports gains only on the same task set used for evolution. Does an evolved harness generalize to unseen tasks in the same domain?
3. **Long-horizon stability.** Variant isolation resolves GAIA stagnation over 15 rounds; does it hold over 100+ rounds, or do variants over-specialize?
4. **Multi-platform harness.** HarnessX evolves harnesses for a single platform. Can evolved harness components transfer across platforms (e.g., a processor that works for both claw-code and Claude Code)?

### References

- Darwin Agent Team. "HarnessX: A Composable, Adaptive, and Evolvable Agent Harness Foundry." arXiv:2606.14249, July 2026.
- Fernando et al. "Promptbreeder: Self-Referential Self-Improvement Via Prompt Evolution." arXiv:2309.16797, 2023.
- Khattab et al. "DSPy: Compiling Declarative Language Model Calls into Self-Improving Pipelines." arXiv:2310.03714, 2023.
- Ouyang, Zhang et al. "SICA: Self-Improving Code Agent." arXiv:2505.17029, 2025.

---

## Future Directions

### Open Questions

1. **Standardization:** Will agent harness protocols standardize (similar to MCP)?
2. **Multi-Harness:** Can one platform work with multiple harnesses?
3. **Platform Convergence:** Will agent platforms build harness features directly?
4. **Enterprise vs 1PC:** How do harness needs differ between enterprise and personal use?

### Potential Additions

New harness ecosystems may be added based on:
- Active development (commits in current year)
- Unique architectural patterns
- Community adoption
- Relevance to tracked agent platforms

---

## Related Documentation

- [Platform Comparison](../architecture/platform_comparison.md) — Full agent platform coverage
- [External Frameworks](../architecture/external_frameworks.md) — LangGraph, SmolAgents, etc.
- [Latest Updates](../docs/LATEST_UPDATES.md) — Monthly ecosystem tracking

---

*Last updated: August 18, 2026*
*Part of: AllClaws Personal AI Agent Ecosystem Research*
