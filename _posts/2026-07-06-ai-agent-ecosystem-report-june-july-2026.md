---
layout: post
title: "AI Agent Ecosystem Report: June-July 2026"
date: 2026-07-06 09:00:00 +0800
author: Danny Zeng
categories: [Monthly Report]
tags: [AI agents, ecosystem, mcp, self-improvement, openclaw, hermes, zeroclaw, openhuman, agentscope]
---

## Executive Summary

June-July 2026 was the most architecturally consequential period AllClaws has tracked. **~8,668 new commits** landed across 11 active platforms, and the themes were unmistakable: **memory systems came of age**, **MCP crossed the chasm from integration afterthought to core architecture**, and **self-improvement claims were finally subjected to source-code verification** — with surprising results.

**Key Findings:**

- **ZeroClaw's Memory Overhaul** — 800 commits delivered a complete durable memory store seam with supersede/dedup/budget/policy-gate, WASM plugin channel bindings, and the return of zeroclaw-desktop. The Rust-first agent is now the most memory-architected platform in the ecosystem
- **OpenClaw Breaks 31K Commits** — 4,352 new commits including a ring-zero MCP server for in-loop CLI harness execution and an embedded operator terminal with PTY. The scale is staggering
- **Hermes v2026.7.1** — 2,360 commits brought desktop/CLI parity (skills hub, MCP tab, log filters), stacked slash-skill invocations (`/skill-a /skill-b`), and native WhatsApp polls via Baileys
- **OpenHuman's TinyAgents Migration** — 694 commits ported the entire agent harness to TinyAgents v1.7.1, with full Langfuse observability and a Rhai-based scripting DSL
- **Self-Improvement Claims Verified** — Of 26 platforms, only 6 have real self-improvement mechanisms in source code. Zero use RLHF/GRPO. The "self-improving agent" is, in every case, LLM-as-judge with persisted memory
- **MCP Adoption Deepens** — OpenClaw's ring-zero MCP server, Hermes' first-class MCP tab, and ZeroClaw's 12-crate MCP implementation signal the protocol has moved from experiment to infrastructure
- **AgentScope Joins as Platform #26** — Alibaba's multi-agent framework (~25.8K stars) with event-driven streaming and a new RAG module

**What to Watch in August:**
1. MCP ecosystem deep-dive — token overhead analysis across native vs adapter platforms
2. Enterprise governance frameworks — credential isolation patterns (IronClaw, GoClaw, HiClaw)
3. ZeroClaw's WASM plugin system — will it reach production maturity for v1.0.0?
4. The self-improvement gap — will any platform attempt actual RL-based learning?

---

## Cross-Cutting Trends

### 1. The Memory Architecture Wars

If May-June was about attested signing and identity, June-July was about **memory**. Three platforms shipped fundamental memory rewrites:

| Platform | What Changed | Architecture |
|----------|-------------|--------------|
| **ZeroClaw** | Durable memory store seam | Supersede + dedup + budget + policy-gate; memory survives process restarts |
| **AgentScope** | ReMe long-term memory middleware | Middleware-layer memory with RAG module (distributed, multi-tenant, multi-session) |
| **OpenHuman** | W3 chunk store flip | Delegated `get_chunks_batch` + `list_chunks` — memory backend abstraction |
| **Hermes** | Background review loop matures | LLM-as-judge extracts lessons after turns → persisted as skills/memory with curator dedup |
| **MaxClaw** | EvolutionTracker (587 lines) | Statistical: records every API call, error, tool execution → recommends best recovery strategy |

**Why this matters:** Memory is the substrate of agent improvement. The platforms investing in memory architecture now are building the foundation for cross-session learning that will differentiate them in 12-18 months. MaxClaw's statistical approach (tracking recovery success rates, model performance rankings) is unique — it's the only platform where "improvement" is quantitatively measurable rather than qualitative.

### 2. MCP: From Adapter to Architecture

The MCP protocol has crossed a critical threshold. It's no longer just a tool integration bridge — it's becoming the **connective tissue of agent runtimes**:

- **OpenClaw** introduced a "ring-zero MCP server" that runs CLI harnesses inside the agent loop itself. This blurs the line between "tool" and "agent runtime" — the agent loop speaks MCP to its own execution layer
- **Hermes** shipped a first-class MCP tab with GUI auth/probe/logs and per-tool gating. The per-tool gating solves the token overhead problem pragmatically: users selectively enable individual MCP tools rather than loading all schemas every turn
- **ZeroClaw** has 12+ dedicated Rust crates for MCP (`mcp_transport`, `mcp_tool`, `mcp_resources_tool`, `mcp_protocol`, `mcp_client`, `mcp_context`, `mcp_deferred`, `mcp_prompts_tool`, `mcp_prompt`). This is a full protocol implementation, not an adapter
- **AgentScope** added a RAG module that leverages MCP-style resource patterns for distributed, multi-tenant retrieval

**The new taxonomy:** Native (ZeroClaw) → First-class (Hermes, OpenClaw) → Adapter (GoClaw, NanoBot) → Resistant (NanoClaw, OpenHuman). A full MCP deep-dive is planned for the August report.

### 3. The Desktop Resurgence

After a period where messaging gateways and CLI dominated, desktop is back:

- **ZeroClaw** reintroduced zeroclaw-desktop as a self-contained, Quickstart-first companion
- **Hermes** achieved full CLI/dashboard parity — skills hub, MCP management, maintenance ops, and log filters all work from the desktop app
- **OpenClaw** shipped a dockable ghostty-web terminal panel for mobile WebView
- **NanoBot** added a safe WebUI first-run launcher with improved onboarding

The desktop agent UI space remains fragmented, but the investment level signals that platforms are taking the "IDE of agents" goal seriously.

### 4. "Self-Improving" Claims: The Verification

This month, AllClaws conducted the first systematic source-code verification of "self-improvement" claims across all 26 tracked platforms. The results were revealing:

**6 platforms have verified implementations:**
- **Hermes** — 907-line background review loop (LLM-as-judge + curator dedup)
- **ZeroClaw** — SkillImprover with atomic writes, dual cooldown (in-memory + on-disk), audit trail
- **IronClaw** — Graduated risk model: prompt → config → code (propose only)
- **MaxClaw** — EvolutionTracker with statistical recovery recommendations
- **GoClaw** — skill_evolve foundation + SOUL.md personality self-evolution
- **OpenClaw** — Memory dreaming with reinforcement-based promotion

**5 marketing claims are unverified or misleading:**
- NanoBot claims "self-improvement" in README with no corresponding code
- OpenHuman explicitly removed its self-healing retry interceptor
- Copilot-CLI and Reasönix use "self-correcting" to mean in-turn error retry

**Critical finding:** Zero platforms use RLHF, GRPO, or reward models. All "self-improvement" is either LLM-as-judge background review or statistical tracking. The improvement is bounded by context window injection — the agent loads more relevant information, but the underlying model never changes.

Full report: [Self-Improvement Claims Verification](https://github.com/dz3ai/allclaws/blob/main/docs/reports/self-improvement-claims-verification.md)

---

## Platform Deep-Dives

### OpenClaw — The Leviathan

**Commits:** 4,352 | **Version:** v2026.4.19-beta.2 (31810 commits ahead of beta tag) | **Theme:** Infrastructure as agent loop

OpenClaw's scale defies comparison. At 31,810 commits past its last beta tag, it operates in a different regime from every other tracked platform. The June-July cycle delivered two architecturally novel features:

**Ring-Zero MCP Server:** OpenClaw now runs CLI harnesses on the agent loop via a ring-zero MCP server. This is not MCP as a tool bridge — it's MCP as the execution protocol for the agent's own operation loop. The agent loop speaks MCP to its own harness layer, making the execution boundary itself MCP-native. No other platform has attempted this pattern.

**Embedded Operator Terminal:** A full PTY terminal with fail-closed isolation and kill switch, capable of detach/reattach. Combined with the dockable ghostty-web terminal panel for mobile WebView, OpenClaw now has terminal presence from mobile to desktop to operator console.

Additional highlights: context usage monitoring UI, animated mascot (brand polish), and continued stabilization across Feishu, Telegram, and Mattermost channels.

**Assessment:** OpenClaw is building infrastructure that other platforms haven't started designing. The ring-zero MCP pattern, if proven, could redefine how agent runtimes think about their own execution model. The concern remains review quality at this commit volume.

### Hermes-Agent — Desktop Parity Achieved

**Commits:** 2,360 | **Version:** v2026.7.1 | **Theme:** The agent that grows with you

Hermes reached a milestone: **full parity between CLI and desktop**. The desktop app now has skills hub, MCP test/toggle/catalog, maintenance ops, and log filters — everything the CLI can do, the dashboard can do too.

**Stacked Slash-Skills:** The most innovative feature this cycle. Users can now chain skills: `/skill-a /skill-b do XYZ` loads both skills and executes the task. This is skill composition at the invocation layer — a simple idea with deep implications for workflow automation.

**WhatsApp Enhancement:** Native Baileys polls, clarify-as-poll, locations, and rich inbound metadata. WhatsApp is now a first-class Hermes platform, not just a messaging afterthought.

**CLI Autocomplete:** Ghost text autocomplete for stacked slash-skill invocations makes skill chaining discoverable. The CLI now guides users toward composition patterns they didn't know existed.

**Background Review Maturity:** The self-improvement loop is now the most mature in the ecosystem (907 lines in `background_review.py`). The curator dedup system prevents skill pileup, write-approval gating enables human-in-the-loop, and skill provenance tracking tags every agent-created skill with its origin.

**Assessment:** Hermes has transitioned from rapid feature growth to architectural deepening. The stacked slash-skills pattern, combined with the matured background review loop, positions Hermes as the reference implementation for how agents learn procedural knowledge.

### ZeroClaw — The Memory-First Architecture

**Commits:** 800 | **Version:** v0.8.0-beta.2 → v0.8.2 | **Theme:** Durable memory + WASM plugins

ZeroClaw's 800-commit cycle was the most architecturally dense of any platform this period. Three major subsystems shipped:

**Durable Memory Store Seam:** A complete memory overhaul with supersede (old entries are superseded, not deleted), dedup (automatic near-duplicate detection), budget (memory size limits with intelligent eviction), and policy-gate (configurable rules for what gets persisted). Memory survives process restarts via on-disk persistence. This is the most sophisticated memory lifecycle management in the ecosystem.

**WASM Plugin Channels:** Channel host bindings for `wasi:http`, inbound queue, config jail, and a registration API. Plugins can now handle HTTP requests, queue messages, and run in isolated config environments. This is the foundation for ZeroClaw's v1.0.0 plugin ecosystem.

**Skill Improver:** The `SkillImprover` struct provides atomic SKILL.md writes with dual cooldown tracking (in-memory per-process + on-disk via YAML `updated_at` field), full audit trail as HTML comments, and failure-scanning from conversation history. The implementation is more structured than Hermes' approach — explicit cooldowns, validation, and atomicity guarantees.

**RFC-6969 Output Routing:** Per-turn output routing via `send_via` with voice delivery fixes. Agents can now dynamically choose how to deliver each response — text, voice, or structured output.

**Assessment:** ZeroClaw is building the most architecturally rigorous agent runtime in the ecosystem. The memory-first philosophy, combined with WASM plugin isolation and the 12-crate MCP implementation, positions ZeroClaw as the platform for developers who care about architectural purity. The question is whether the <5MB RAM positioning can survive the feature growth implied by these additions.

### OpenHuman — The TinyAgents Migration

**Commits:** 694 | **Version:** v0.57.13 → v0.58.7 | **Theme:** Foundation rebuild

OpenHuman undertook the most ambitious refactoring of the cycle: porting its entire agent harness to TinyAgents.

**TinyAgents Phase 0/1 Cutover:** The agent harness was migrated to TinyAgents v1.7.1, with crate-back SchemaCleanr, model-context, and observed stream. This is a foundational architecture change — the execution layer was rebuilt while maintaining the Tauri/React frontend. The migration suggests confidence in TinyAgents as a long-term runtime.

**Memory W3 Chunk Store Flip:** The memory backend was flipped: `get_chunks_batch` and `list_chunks` are now delegated operations, completing the W3 migration phase. The memory abstraction is now clean enough to swap backends without touching the agent loop.

**Full Langfuse Tracing:** Complete observability with cost telemetry. Every agent call is now traced with full-content Langfuse integration. This is the most comprehensive observability story of any tracked platform — OpenHuman can tell you exactly how much each conversation costs, not just how many tokens were used.

**Rhai DSL Scripting:** Language-based workflows via Rhai `.ragsh` REPL as a first-class runtime tool. Users can now write scripts that automate agent workflows in a lightweight embedded language, without the overhead of Python or Rust plugins.

**Assessment:** OpenHuman is rebuilding its foundation while shipping. The TinyAgents migration is risky — changing the execution layer mid-flight — but the payoff is a cleaner architecture that can support the community-focused features that differentiate OpenHuman. The Langfuse tracing is the gold standard for agent observability.

### NanoBot — Event-Driven Architecture

**Commits:** 295 | **Version:** v0.2.1 → v0.2.2 | **Theme:** Triggers and workspaces

NanoBot shipped a series of features that move it closer to event-driven agent architecture:

- **Session-bound local triggers** — Event-driven automation that fires within a session based on conditions
- **Workspace Dream prompt override** — Per-workspace memory tuning, allowing different Dream (memory consolidation) configurations
- **API key security hardening** — `api_key` now required when binding to all interfaces, parity with WebSocket gateway
- **Safe WebUI first-run launcher** — Improved onboarding with guided setup
- **Dollar skill shortcuts** — Quick invocation of frequently-used skills

**Assessment:** NanoBot is quietly building the most user-friendly agent framework for non-technical users. The trigger system and workspace-level memory configuration are features that matter to end users, not just developers.

### AgentScope — The Newcomer

**Commits:** 38 (since addition) | **Version:** v2.0.2 → v2.0.3 | **Theme:** RAG + Memory

AgentScope joined AllClaws as platform #26 this month. The Alibaba-backed multi-agent framework shipped several notable additions:

- **ReMe long-term memory middleware** — A middleware-layer memory system that sits between the agent and the LLM
- **RAG module** — Distributed, multi-tenant, multi-session retrieval-augmented generation. This is the most comprehensive RAG implementation among tracked platforms
- **Milvus Lite vector store** — A new vector database backend for the RAG module
- **DashScope CosyVoice TTS** — Text-to-speech via Alibaba's CosyVoice model
- **Resizable WebUI right panel** — UI enhancement to display task, permission context, MCP, and skills

**Assessment:** AgentScope brings the Alibaba ecosystem into AllClaws tracking. The RAG module's multi-tenant design is architecturally distinct from the personal-memory approaches of Hermes and ZeroClaw — it's built for platform deployments, not individual users. The CosyVoice TTS integration signals a China-market focus.

### NanoClaw — Template System

**Commits:** 100 | **Version:** v2.1.17 (+170 dev commits) | **Theme:** Provider-agnostic personas

- **Local template loader** with `ncl --template` flag and provider-agnostic persona/skills seams
- **Colored approval buttons** on Slack (primary/danger)
- **Async agent image builds** — No longer blocks the host during container creation
- **Mount allowlist readOnly fix** — Security hardening

### GoClaw — Targeted Fixes

**Commits:** 6 | **Version:** v3.14.0 patches | **Theme:** Reliability

- Stale provider alert cleanup
- Codex response retry for transient failures
- venv python interpreter exempted from `.goclaw/` path deny
- ACP session/update tool_call notifications at Info level
- Cron stateless gate inverted to match UI label

### ClawTeam — v0.3.0

**Commits:** 4 | **Version:** v0.2.0 → v0.3.0+openclaw2 | **Theme:** Compatibility

- Tmux respawn fix: keep respawned agents addressable
- OpenClaw >= 2026.6 compatibility (TUI form adaptation)

### CLI Coding Agents

| Agent | Commits | Version | Key Changes |
|-------|---------|---------|-------------|
| **Copilot-CLI** | 5 | v1.0.64 → v1.0.69 | 5 patch releases (changelog bumps) |
| **Aider** | 0 | — | Unchanged |
| **Reasönix** | 0 | — | Unchanged |
| **Codex CLI** | 0 | — | Unchanged |

The CLI coding agent category was quiet this cycle. Copilot-CLI shipped routine patch releases. The major CLI agent activity (Reasönix checkpoint, Codex CLI addition) happened in the May-June cycle.

### Other Platforms

| Platform | Commits | Notes |
|----------|---------|-------|
| **IronClaw** | 0 | Unchanged (consolidating after attested signing series) |
| **MaxClaw** | 0 | Unchanged |
| **Claw-AI-Lab** | 0 | No tags released |

---

## Health Check: Test Framework Results

**Agent Platform Tests CI: ✅ FULLY REPAIRED** — After 17+ days of continuous failure, the agent-tests.yml workflow is now green. Three root causes were identified and fixed:

1. **Timestamp colons** — `run_tests.sh` created directories with colons in timestamps, which `upload-artifact@v4` rejects. Fixed by using dashes.
2. **Matrix scope** — Each of 11 matrix jobs was running all 26 platforms instead of just `matrix.platform`. Added `--platform` flag to filter.
3. **Report aggregation** — The Generate Report job referenced non-existent paths and used a fragile `jq -s` slurp that broke on merged artifacts. Replaced with per-file loop.

**Benchmark Suite CI: ✅ Green** — Weekly reports and daily benchmarks running cleanly with the v3.0 Python engine (zero dependencies, 2210 lines).

---

## Platform Categorization Update

AllClaws now tracks **26 platforms** across four categories:

| Category | Count | Examples |
|----------|-------|----------|
| Claw Ecosystem | 11 | OpenClaw, Hermes-Agent, ZeroClaw, NanoClaw, NanoBot, GoClaw, IronClaw, MaxClaw, HiClaw, ClawTeam, Claw-AI-Lab |
| External Frameworks | 9 | AgentScope, SmolAgents, LangGraph, CrewAI, AutoGen, Swarms, OpenAgents, OpenFang, kimi-code |
| CLI Coding Agents | 5 | Reasönix, Copilot-CLI, Aider, Codex CLI, Kimi-CLI |
| Human Digital Twin | 1 | OpenHuman |

**New this month:** AgentScope (platform #26, External Frameworks)

---

## Emerging Patterns

### 1. The Skill Composition Era

Hermes' stacked slash-skills (`/skill-a /skill-b do XYZ`) represents a new paradigm: skills as composable building blocks rather than standalone workflows. Combined with ZeroClaw's skill improver (which patches existing skills based on failure analysis) and IronClaw's skill extraction mission (which creates skills from successful multi-step workflows), the skill system is evolving from static documentation to dynamic, self-modifying procedural memory.

### 2. Observability as Differentiator

OpenHuman's full Langfuse tracing with cost telemetry sets a new bar. As agents move into production, the ability to trace every call, understand every cost, and debug every failure becomes critical. Hermes' `display.memory_notifications` (off/on/verbose) and ZeroClaw's audit trail are steps in this direction, but OpenHuman has the most complete story.

### 3. The China Stack Consolidation

AgentScope (Alibaba), GoClaw (Feishu/WeChat), HiClaw (Higress/Matrix), and OpenHuman (Tauri/Rust) form an emerging China-stack cluster. AgentScope's CosyVoice TTS and DashScope integration, combined with GoClaw's multi-channel China messaging support, suggest a coherent alternative ecosystem forming alongside the US/EU platforms.

---

## Looking Ahead: August 2026 Priorities

Per the H2 2026 roadmap:

1. **MCP Ecosystem Deep-Dive** — Full execution of the 5-phase research plan: adoption survey across all 26 platforms, architecture comparison (native vs adapter), token overhead measurement, server ecosystem catalog, and synthesis. [Research plan](https://github.com/dz3ai/allclaws/blob/main/docs/reports/mcp-deep-dive-research-plan.md)
2. **Enterprise Governance Frameworks** — Okta AI identity, HiClaw/GoClaw enterprise patterns, human-in-the-loop workflows, credential isolation
3. **Self-Improvement Follow-up** — Monitor whether any platform attempts actual RL-based learning in response to the verification findings
4. **Monthly submodule sync** — Continue tracking the ~8K commit/month velocity

---

## Methodology

**Data Collection:**
- Monthly submodule sync via `git submodule update --remote --recursive`
- Commit counts via `git log OLD..NEW --no-merges` per submodule
- Self-improvement claims verified by reading actual source code (not just documentation)
- All data covers 2026-06-17 to 2026-07-05

**Platform Coverage:**
- 16 git submodules updated and analyzed
- 11 platforms with new commits; 5 unchanged
- ~8,668 total new commits across changed platforms

**Self-Improvement Verification:**
- Source search across all 26 platform directories for 15 pattern categories
- Every Tier 1 claim verified by reading the actual source code file and function
- Classification: STRONG (code-verified), MODERATE (partial/derivative), WEAK (in-turn only), NONE

---

**Next Report:** First Monday of August 2026 — MCP Deep-Dive Special

---

**Stay Updated:**
- GitHub: [dz3ai/allclaws](https://github.com/dz3ai/allclaws)
- Detailed tracker: [docs/LATEST_UPDATES.md](https://github.com/dz3ai/allclaws/blob/main/docs/LATEST_UPDATES.md)
- Roadmap: [docs/ROADMAP.md](https://github.com/dz3ai/allclaws/blob/main/docs/ROADMAP.md)
- Self-Improvement Report: [docs/reports/self-improvement-claims-verification.md](https://github.com/dz3ai/allclaws/blob/main/docs/reports/self-improvement-claims-verification.md)
- MCP Research Plan: [docs/reports/mcp-deep-dive-research-plan.md](https://github.com/dz3ai/allclaws/blob/main/docs/reports/mcp-deep-dive-research-plan.md)
