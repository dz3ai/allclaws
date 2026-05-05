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
- Future: Other harnesses as they emerge

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

*Last updated: 2026 May 5*
*Part of: AllClaws Personal AI Agent Ecosystem Research*
