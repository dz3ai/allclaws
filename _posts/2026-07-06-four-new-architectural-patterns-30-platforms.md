---
layout: post
title: "Four New Architectural Patterns: AllClaws Expands to 30 Platforms"
date: 2026-07-06 18:00:00 +0800
author: Danny Zeng
categories: [Platform Analysis]
tags: [eliza, agent-zero, praisonai, rocketride, architecture, new platforms]
---

## AllClaws Now Tracks 30 Platforms

AllClaws has expanded from 26 to **30 tracked platforms** with the addition of four external frameworks that each bring genuinely novel architectural patterns to the research corpus. This is not a rounding exercise — each addition was selected because it represents a design paradigm absent from the existing 26 platforms.

The four newcomers:

| Platform | Stars | Language | What's New |
|----------|-------|----------|------------|
| **eliza** (elizaOS) | 18.7K | TypeScript | Plugin-first agent operating system |
| **agent-zero** (agent0ai) | 18.3K | Python | Dual-runtime Docker isolation |
| **PraisonAI** (MervinPraison) | 8.4K | Python | Protocol-driven skill mutability |
| **rocketride-server** (rocketride-org) | 5.0K | Python/C++ | C++ execution engine + node-graph pipelines |

What follows is a deep-dive into the one architectural pattern from each platform that nothing else in the ecosystem is doing.

---

## 1. eliza — The Plugin-First Agent OS

Most agent frameworks have a core loop with plugins bolted on. Hermes calls this "the narrow waist" — the core stays small, capability lives at the edges. OpenClaw, ZeroClaw, GoClaw all follow this philosophy.

**eliza inverts it.**

The framework IS the plugin system. `AgentRuntime` in `@elizaos/core` defines five abstraction layers — actions, providers, evaluators, services, and models — and every capability in the 146-plugin ecosystem slots into one of them. The LLM providers themselves are plugins (`plugin-anthropic`, `plugin-openai`, `plugin-local-inference`). Channels are plugins (`plugin-discord`, `plugin-telegram`, `plugin-bluesky`). Tools are plugins (`plugin-browser`, `plugin-coding-tools`, `plugin-computeruse`).

The monorepo ships 25+ framework packages alongside those plugins: `core`, `agent`, `app-core`, `os`, `lifeops`, `contracts`, `evidence`, `registry`, `scenario-runner`, `cloud`. This is not a framework with extensions — it's an **operating system for agents**.

### What's genuinely new

Two patterns eliza brings that no Claw ecosystem platform has:

**Character definitions as first-class citizens.** Agents are defined by personality profiles — structured data objects that shape tone, decision-making, and knowledge domains. In the Claw ecosystem, personality lives in `SOUL.md` (GoClaw) or `MEMORY.md` (Hermes) as free text. eliza treats character as typed, validated, swappable configuration. An agent's identity is data, not prompt engineering.

**On-chain evidence and contracts.** The `packages/contracts/` and `packages/evidence/` directories bring blockchain-native patterns into the framework. This overlaps with IronClaw's attested signing series (covered in our [June-July report](_posts/2026-06-01-ai-agent-ecosystem-report-may-june-2026.md)), but where IronClaw built a 13-PR signing chain as a security feature, eliza ships provenance and attestation as framework primitives. The crypto heritage is real — this is the only tracked platform where on-chain integration is a core design assumption, not an enterprise add-on.

### Why it matters for the research

eliza fills the "large-scale TypeScript framework" gap in External Frameworks. Before this, the only major TS agent platform tracked was OpenClaw (itself a Claw ecosystem member). eliza gives us a comparison point from outside the Claw world — a platform with 18.7K stars, a plugin architecture philosophy diametrically opposed to the Claw "narrow waist" principle, and a crypto/social heritage that shapes every design decision.

---

## 2. agent-zero — Two Virtualenvs Are Better Than One

Agent isolation is an unsolved problem across the ecosystem. NanoClaw uses Docker containers per session. Hermes runs tools in the main process with permission gating. ZeroClaw isolates via WASM plugins. Every platform makes a different trade-off between safety and performance.

**agent-zero's answer: split the Python runtime itself.**

Inside each Docker container, agent-zero maintains **two separate virtualenvs**:

```
/opt/venv-a0   (Python 3.12)  →  Framework runtime (agent.py, WebUI, plugins)
/opt/venv      (Python 3.13)  →  Agent execution runtime (pip installs, user code)
```

When the agent runs `pip install pandas` during a task, the package lands in `/opt/venv` — the execution environment. The framework runtime at `/opt/venv-a0` is untouched. Framework imports never break from agent-installed dependencies. A botched `pip install` in one task cannot corrupt the agent's ability to function.

### Why this is architecturally significant

Every other Python-based platform (Hermes, NanoBot, AgentScope, PraisonAI) runs framework code and agent-executed code in the same Python process. When the agent installs a conflicting package, the framework can crash. When the agent runs `sys.exit()`, the framework dies. agent-zero's dual-venv pattern solves this at the environment level — no process-level sandboxing needed, no WASM complexity, just two pip environments.

The pattern extends to agent self-knowledge. The `knowledge/main/about/` directory contains files written **for the agent, not the user**: `identity.md` (philosophy, principles), `architecture.md` (how the agent loop works), `capabilities.md` (what it can and cannot do), `configuration.md` (provider setup). This is structured introspection — the agent reads its own instruction manual. No other platform has this explicit self-knowledge layer; the closest analog is Hermes' MEMORY.md, but that's user-facing persistent memory, not agent-internal reference material.

### Why it matters for the research

agent-zero represents the "minimal-footprint autonomous agent" design school — a single `agent.py` entry point, flat directory structure, Docker-isolated tool execution. It's the architectural opposite of eliza's 146-plugin monorepo. Having both in the research corpus lets us compare what happens when you start from "one file" vs "25 packages" and both arrive at functional autonomous agents.

---

## 3. PraisonAI — Protocol-Driven Skill Governance

We just completed a [systematic verification of "self-improvement" claims](/allclaws/docs/reports/self-improvement-claims-verification/) across all tracked platforms. Six platforms have real implementations; the rest are marketing. PraisonAI claims "self-improving" — so we checked the code.

**The claim holds up.** But what's more interesting than the self-improvement loop itself is the architectural pattern that enables it.

### Skill operations as Python Protocols

PraisonAI defines skill management through three PEP 544 Protocol classes:

```python
class SkillSourceProtocol(Protocol):
    """Abstract source of skills — filesystem, HTTP registry, enterprise server."""
    def discover(self) -> Iterable[SkillProperties]: ...
    def load_instructions(self, name: str) -> Optional[str]: ...

class SkillInvocationPolicyProtocol(Protocol):
    """Gatekeeps whether model or user can invoke a given skill."""
    def can_model_invoke(self, props: SkillProperties) -> bool: ...
    def can_user_invoke(self, props: SkillProperties) -> bool: ...

class SkillMutatorProtocol(Protocol):
    """Agent-managed skill CRUD with propose=True staging."""
    def create(self, name, content, category, propose=True) -> str: ...
    def patch(self, name, old_string, new_string, propose=True) -> str: ...
```

The `SkillMutatorProtocol` is particularly notable. Every mutation defaults to `propose=True`, meaning skill changes are **staged for human approval** before writing to disk. This is the same pattern Hermes uses (`write_approval` gate) and ZeroClaw uses (on-disk cooldown), but PraisonAI expresses it as a typed interface that any implementation must satisfy.

### The self-improvement loop, verified

```python
class DefaultSkillReviewPolicy:
    def should_review(self, context) -> bool:
        return len(context.get("tools_used", [])) >= self.min_tool_calls

    def review_prompt(self, context) -> str:
        return f"... skill_manage ... NO_SKILL ..."
```

Tests confirm: `self_improve` defaults to `False` on the Agent class. When enabled, the policy fires after tasks that used tools, builds a review prompt referencing the `skill_manage` tool, and the agent creates or patches skills based on what it learned. This is the same LLM-as-judge pattern as Hermes' background review, but with a pluggable policy interface — you can substitute `DefaultSkillReviewPolicy` with any custom implementation.

### Why it matters for the research

The protocol-driven design means skill storage can be swapped from filesystem to HTTP registry to enterprise policy server without touching core code. Hermes and ZeroClaw have filesystem-locked skill stores. PraisonAI's abstraction enables **centralized skill governance** — an enterprise deployment can serve skills from a central server, audit every mutation, and enforce invocation policies per-team. This is the architectural foundation for "skill management as a service," a pattern no other tracked platform supports without forking.

This also makes PraisonAI the **7th platform with a verified self-improvement mechanism**, updating our verification report.

---

## 4. rocketride-server — The Anti-Conversation Architecture

Every other tracked platform — all 29 of them — is built around a conversation loop. User sends message, agent processes, agent responds. The agent loop is fundamentally serial: think → act → observe → repeat.

**rocketride-server is not a conversation agent. It's a pipeline engine.**

### The C++ core

The execution engine is written in C++ (`apps/engine/src/main.cpp`), exposing a WebSocket protocol on port 5565. Python nodes — 111 of them — connect to this engine as extendable workers. The engine handles scheduling, memory management, and I/O at native speed. Python handles LLM calls and business logic.

This is the only tracked platform with a C++ execution core. Every other high-performance platform (ZeroClaw, IronClaw, OpenClaw) uses Rust or Go for the runtime, but rocketride's C++ heritage means it can leverage decades of performance optimization tooling — profilers, memory allocators, SIMD intrinsics — that younger ecosystems are still building.

### Node-graph composition

Agents are defined as `.pipe` JSON files — visual node graphs composed in a VS Code extension:

```json
{
  "name": "Git Agent",
  "components": [
    {"id": "chat_1", "provider": "chat", "type": "chat"},
    {"id": "agent_langchain_1", "provider": "agent_langchain"}
  ]
}
```

A pipeline might flow: chat trigger → LangChain agent → Anthropic LLM → output formatter. Each node is a black box with typed inputs and outputs. You compose agents by wiring nodes together, not by writing loop logic.

### Cross-framework agent nodes

The most disruptive pattern: `agent_crewai`, `agent_langchain`, `agent_deepagent`, `agent_llamaindex`, and `agent_rocketride` are all first-class node types. A single pipeline can invoke a CrewAI agent, feed its output to a LangChain retriever, pass that to an LLM, and format the result — all in one `.pipe` file.

No other tracked platform does this. CrewAI is already in AllClaws as a standalone framework. LangGraph is tracked separately. But rocketride treats them as interchangeable components in a larger pipeline. It's not competing with these frameworks — it's **orchestrating them**.

### Why it matters for the research

rocketride fills a fundamental gap: the "high-performance pipeline engine" pattern. Every other platform asks "how do we make the conversation loop better?" rocketride asks "what if the agent isn't a conversation at all?" The node-graph paradigm is closer to Apache Airflow or Prefect than to Claude or ChatGPT — and that's exactly why it belongs in the research corpus. It represents a design school that the conversation-loop platforms haven't considered.

---

## What These Additions Mean for AllClaws Research

The four additions expand the architectural diversity of AllClaws in four distinct directions:

| Direction | Platform | New Axis |
|-----------|----------|----------|
| Plugin-first vs narrow-waist | eliza | Inverted extension philosophy |
| Runtime isolation granularity | agent-zero | Dual-venv within single container |
| Skill governance abstraction | PraisonAI | Protocol-driven enterprise skill management |
| Execution paradigm | rocketride-server | Pipeline/DAG vs conversation loop |

With 30 platforms now tracked, AllClaws covers the full spectrum of agent architecture: from ZeroClaw's <5MB Rust microkernel to OpenClaw's 31K-commit monolith, from Hermes' personal assistant to HiClaw's multi-agent enterprise teams, and now from eliza's plugin-everything philosophy to rocketride's pipeline-first paradigm.

The [MCP ecosystem deep-dive](https://github.com/dz3ai/allclaws/blob/main/docs/reports/mcp-deep-dive-research-plan.md) (scheduled for August) will examine how these new platforms interact with MCP — early signals suggest eliza's plugin model and rocketride's node system both have interesting MCP stories to tell.

---

**Explore the full comparison:** [platform_comparison.md](https://github.com/dz3ai/allclaws/blob/main/architecture/platform_comparison.md) — all 30 platforms, EN + ZH.

**Self-improvement verification updated:** PraisonAI is now the 7th platform with a verified implementation. [Full report](https://github.com/dz3ai/allclaws/blob/main/docs/reports/self-improvement-claims-verification.md).
