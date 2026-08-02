# Architecture Drift Report: Submodule Updates vs Documentation Coverage

> August 2026 — Analysis of architectural changes across tracked platforms
> since last architecture doc update (July 15, 2026)

---

## Executive Summary

AllClaws architecture documentation was last updated July 15, 2026.
Since then, 4 new platforms were added (OpenWorker, Dify, MetaGPT, Qwen-Agent),
and at least 5 existing platforms shipped significant architectural changes.
This report maps the drift and identifies documentation priorities.

> **UPDATE (August 2, 2026):** All 5 identified documentation gaps have been
> resolved. Architecture docs now cover all 34 platforms (EN + ZH).
> See [Part 6: Resolution Status](#part-6-resolution-status) for details.

**Original coverage gap (now resolved):** 4 platforms with zero architecture
documentation, 5 platforms with outdated documentation.

---

## Part 1: New Platforms (Zero Documentation)

These 4 platforms were added in late July but have no architecture analysis
in any document under `architecture/`.

### 1. OpenWorker (Platform #31)

**Architecture:** Desktop-native agent coworker built on aisuite.

| Component | Technology | Role |
|-----------|-----------|------|
| `coworker/` | Python | Agent engine, model providers, connectors, MCP client, memory, automations |
| `surfaces/gui/` | React + Tauri | Desktop app UI, supervises the server |
| `stt/` | Rust | Speech-to-text sidecar for voice input |

**Key design decisions:**
- **aisuite foundation** — Not a custom agent loop. Uses Andrew Ng's aisuite
  library for unified chat-completions API across LLM providers.
- **Approval-gated actions** — Writes, sends, and shell commands require human
  approval. Unattended runs park requests in an inbox.
- **MCP native** — Any MCP-compatible tool plugs in with per-tool control.
- **BYO model** — OpenAI, Anthropic, GLM, DeepSeek, Kimi, Qwen, Ollama.

**Context compaction:** Shipped OPE-27 (4-part series) — pure compaction
module, engine hook with failure policy, persistence, settings overrides.
This is the most sophisticated compaction architecture we've seen in the
tracked ecosystem.

**Architecture classification:** Desktop-native, human-in-the-loop, single-agent.

### 2. Dify (Platform #32)

**Architecture:** Visual workflow platform for LLM applications.

| Component | Technology | Role |
|-----------|-----------|------|
| `api/` | Python (uv, not poetry since v1.3.0) | Backend API, workflow engine, RAG |
| `web/` | TypeScript (React, pnpm) | Visual workflow builder UI |
| `docker/` | Docker Compose | Middleware orchestration |

**Infrastructure stack:** PostgreSQL, Redis, Weaviate (vector DB).

**Key design decisions:**
- **Visual pipeline** — Drag-and-drop workflow nodes, not code. Each node
  returns 200 OK individually, making failure debugging harder.
- **Skill packages** — v1.16.0 introduced configurable upload size limits
  for skill packages, treating skills as first-class deployable artifacts.
- **Open-core licensing** — Modified Apache 2.0 with multi-tenant and LOGO
  restrictions. The most commercially oriented platform we track.

**Architecture classification:** Visual workflow, platform-as-a-service, multi-tenant.

### 3. MetaGPT (Platform #33)

**Architecture:** Role-playing multi-agent framework (SOP-driven).

| Component | Technology | Role |
|-----------|-----------|------|
| `metagpt/actions/` | Python | Action primitives (WriteCode, WriteTest, etc.) |
| `metagpt/environment/` | Python | Shared environment for agent communication |
| `metagpt/configs/` | Python | Model and tool configuration |
| `metagpt/document_store/` | Python | RAG and document retrieval |

**Key design decisions:**
- **SOP (Standard Operating Procedure) metaphor** — Agents follow
  pre-defined role sequences: Product Manager → Architect → Engineer →
  QA Engineer. Each role has specific actions and deliverables.
- **Role hierarchy creates communication overhead** — When tests fail,
  QA reports to Engineer, but nobody can question the architecture.
  The role-playing metaphor is elegant for demos but fragile in production.
- **Data Interpreter** — v0.8.0 added a separate data analysis mode
  alongside the multi-agent software development mode.

**Current status:** Stalled. Last commit January 2026, last release
March 2025 (v0.8.2). 69K stars but 6+ months of inactivity.

**Architecture classification:** Multi-agent role-playing, SOP-driven, research-oriented.

### 4. Qwen-Agent (Platform #34)

**Architecture:** Framework for building agents with Alibaba's Qwen models.

| Component | Technology | Role |
|-----------|-----------|------|
| `qwen_agent/agents/` | Python | Agent implementations (ReAct, tool-calling) |
| `qwen_agent/llm/` | Python | LLM backend (Qwen, OpenAI-compatible) |
| `qwen_agent/tools/` | Python | Built-in tools + tool registration |
| `qwen_agent/memory/` | Python | Conversation memory management |
| `qwen_agent/multi_agent_hub.py` | Python | Multi-agent coordination |

**Key design decisions:**
- **Model-coupled design** — Optimized for Qwen model family (Qwen-2.5,
  Qwen-VL). The framework and the model are co-designed, unlike
  model-agnostic frameworks.
- **setup.py (not pyproject.toml)** — Older Python packaging style,
  consistent with Alibaba's internal conventions.
- **GUI included** — `qwen_agent/gui/` ships a web interface, unlike
  most frameworks that delegate UI to separate projects.

**Architecture classification:** Model-coupled framework, single + multi-agent.

---

## Part 2: Existing Platforms with Significant Architecture Changes

### 5. HiClaw — v1.1.0 Multi-Container Rewrite

**Before:** Single all-in-one container bundling Higress gateway, Tuwunel
Matrix homeserver, MinIO storage, Element Web, and the agent controller.

**After (v1.1.0):** Split into specialized containers:

| Container | Role |
|-----------|------|
| `agentteams-controller` | Go operator: reconciles Worker/Manager/Team/Human CRDs, REST API |
| `agentteams-controller-embedded` | Local mode: controller + all infra in one image |
| `agentteams-manager` | OpenClaw/Node-based coordinator agent |
| `agentteams-manager-copaw` | QwenPaw/Python-based coordinator |
| `agentteams-worker` | Task executor (stateless, on-demand) |

**Architectural shift:** From monolith to Kubernetes-native operator pattern.
Workers are now stateless containers created on demand, with config and
artifacts on object storage. The Manager can be either Node-based or
Python-based — a significant flexibility improvement.

**Impact on existing docs:** `architecture_comparison.md` and
`governance_frameworks_analysis.md` describe the old single-container model.

### 6. Nanobot — v0.3.0 Context Compaction + Agent Runner Split

**Before:** Monolithic agent loop with basic tool calling.

**After (v0.3.0):** Clean separation of concerns:

```
Channel → MessageBus → AgentLoop → AgentRunner → Provider (LLM)
                                         ↓
                                      Tools (files, shell, web, MCP, cron)
```

**Key changes:**
- **AgentLoop vs AgentRunner** — AgentLoop owns the channel-facing turn
  (receives messages, manages session). AgentRunner owns the provider/tool
  conversation loop (calls LLM, executes tools). This separation makes
  each component independently testable.
- **Context compaction** — v0.3.0 preserves Responses reasoning state
  across context compression. Session manager handles compaction with
  idle-compaction timestamp tolerance.
- **Session lock fixes** — Idle session locks and buffered output bounds
  prevent resource leaks in long-running deployments.

**Impact on existing docs:** `architecture_comparison.md` describes the
old monolithic loop without the AgentRunner separation.

### 7. AgentScope — Workspace Backend Abstraction

**New architectural features (July 2026):**
- **`on_check_permission` middleware hook** — Programmatic choke point
  for authorizing agent actions (PR #2001)
- **Workspace backend abstraction** — Apple Container, Bubblewrap, and
  Docker backends. Agents run in isolated workspace environments with
  pluggable isolation technology.
- **AsyncClient reuse** — OpenAI client instances now reused across calls
  instead of creating new ones per call (PR #2063), reducing connection
  overhead by orders of magnitude.
- **Kimi K3 support** — MoonshotChatModel class extended for K3.

**Impact on existing docs:** AgentScope is mentioned in
`platform_comparison.md` but the workspace backend architecture and
permission hook system are not documented.

### 8. Nanoclaw — Hardened Container Architecture

**Before:** Build-it-yourself container approach.

**After:** Pre-hardened agent image fetched at setup time, with `--init`
and `--shm-size` flags, aligned with main. Security defaults come from
the platform, not from user Dockerfiles.

**Impact on existing docs:** Container hardening model not reflected
in `architecture_comparison.md`.

### 9. Hermes-Agent — Compression Summary Role Selection

**Change:** Compression now chooses summary role by template-visible
alternation rather than naively reusing the last role. Prevents
compaction from corrupting conversation semantics.

**Impact on existing docs:** Minor — compression behavior is mentioned
but the role-alternation fix is too detailed for the comparison doc.

---

## Part 3: Documentation Coverage Matrix

| Document | Last Updated | Platforms Covered | Gap |
|----------|-------------|-------------------|-----|
| `platform_comparison.md` | Jul 12 | 13 platforms | Missing: OpenWorker, Dify, MetaGPT, Qwen-Agent |
| `architecture_comparison.md` | Jul 15 | 11 claw platforms | Missing: all 4 new + outdated hiclaw/nanobot |
| `external_frameworks.md` | Jul 6 | 7 frameworks | Missing: OpenWorker, Dify, MetaGPT, Qwen-Agent |
| `mcp_ecosystem_deep_dive.md` | Jun 17 | 11 claw platforms | Missing: MCP adoption in new platforms |
| `governance_frameworks_analysis.md` | Jul 15 | 4 platforms | Missing: AgentScope permission hooks |
| `multi_agent_coordination_research.md` | Jul 15 | 6 platforms | Missing: MetaGPT role hierarchy, OpenWorker single-agent |
| `agent_harnesses.md` | Jul 15 | 3 platforms | Missing: all CLI agents |
| `runtime_benchmarking.md` | Jul 15 | 10 platforms | Missing: real cold-start data for CLI agents |

---

## Part 4: Architectural Trends Identified

### Trend A: Compaction as Architecture (Not Feature)

Three platforms independently shipped compaction systems this month:
- OpenWorker: OPE-27 pure module + engine hook + failure policy + persistence
- Nanobot: AgentRunner-aware compaction preserving reasoning state
- Hermes-Agent: Template-visible role alternation for summary messages

**Pattern:** Compaction is being treated as a first-class architectural
concern, not a runtime optimization. The platforms that solve this well
will handle multi-hour tasks; the rest stay in demo mode.

### Trend B: Operator Pattern for Agent Orchestration

HiClaw v1.1.0 adopted Kubernetes CRD-based orchestration:
Worker/Manager/Team/Human are custom resources reconciled by a Go operator.
This mirrors how cloud-native platforms manage stateful workloads.

**Contrast:** MetaGPT uses in-process role hierarchy. AgentScope uses
middleware hooks. The ecosystem is diverging between "agent as Kubernetes
resource" and "agent as library function."

### Trend C: Workspace Isolation as Security Boundary

AgentScope's workspace backend abstraction (Apple Container, Bubblewrap,
Docker) and Nanoclaw's hardened agent image represent a convergence:
agent execution environments are becoming sandboxed by default.

**Gap:** No platform implements all three isolation modes (filesystem,
network, process). The security model is still incomplete.

### Trend D: Visual vs Code Agent Definition

Dify (visual workflow nodes) vs MetaGPT (Python role definitions) vs
OpenWorker (aisuite toolkits) represent fundamentally different paradigms
for defining agent behavior. The ecosystem has not converged on a
declarative agent definition format — MCP standardizes tools but not agents.

---

## Part 5: Recommended Documentation Updates — ALL COMPLETED ✅

> All 5 priorities were resolved on August 2, 2026 (commits `ae37fa0`, `3604868`, `b0f88e9`).

### ✅ Priority 1: Add 4 New Platforms to `external_frameworks.md`
**Done.** Added OpenWorker (#8), Dify (#9), MetaGPT (#10), Qwen-Agent (#11) sections
with Overview, Architecture, Key Design Decisions, Comparison to Claw Ecosystem,
and Strategic Value. EN + ZH synced. 7→11 frameworks. (+245 lines each)

### ✅ Priority 2: Update `architecture_comparison.md` for HiClaw v1.1.0
**Done.** Replaced single-container description with multi-container CRD operator
architecture: agentteams-controller, stateless workers, embedded vs Kubernetes modes.
Comparison matrix expanded from 13 to 17 platform columns. (+156 lines changed)

### ✅ Priority 3: Update `architecture_comparison.md` for Nanobot v0.3.0
**Done.** Added AgentLoop/AgentRunner separation diagram, context compaction
preserving reasoning state, session lock fixes. Updated modularity row in
comparison matrix.

### ✅ Priority 4: Add compaction architecture to `mcp_ecosystem_deep_dive.md`
**Done.** Added Part 6: Context Compaction & MCP Tool State. Covers OpenWorker
OPE-27 (pure module + engine hook + failure policy + persistence), Nanobot
AgentRunner-aware compaction, Hermes-Agent role alternation, and the key insight
that compaction must preserve MCP tool registration state. EN + ZH synced. (+54 lines EN, +25 lines ZH)

### ✅ Priority 5: Add AgentScope workspace backends to `governance_frameworks_analysis.md`
**Done.** Added AgentScope section under Part 5: Deployment & Isolation. Covers
workspace backend abstraction (Apple Container, Bubblewrap, Docker), `on_check_permission`
middleware hook (PR #2001), AsyncClient reuse (PR #2063). EN + ZH synced. (+25 lines EN, +16 lines ZH)

---

## Part 6: Resolution Status

| Document | Change | Lines | Commit |
|----------|--------|-------|--------|
| `external_frameworks.md` + `.zh-CN.md` | +4 platform sections, updated analysis & conclusion | +245 each | `ae37fa0` |
| `architecture_comparison.md` | HiClaw v1.1.0 rewrite, Nanobot v0.3.0 split, matrix +4 columns | +156 changed | `ae37fa0`, `3604868` |
| `governance_frameworks_analysis.md` + `.zh-CN.md` | AgentScope workspace + permission hooks | +25 EN, +16 ZH | `ae37fa0`, `b0f88e9` |
| `mcp_ecosystem_deep_dive.md` + `.zh-CN.md` | Part 6: Compaction & MCP Tool State | +54 EN, +25 ZH | `ae37fa0`, `b0f88e9` |

**Total: 5 documents updated, +642 insertions, -83 deletions (EN). ZH synced separately (+41 lines).**

### Additional work since original report

- **Failure Mode Taxonomy reorganized** (`failure-mode-taxonomy-2026.md`): 13 modes reordered from random sequence into 7 logical groups following agent execution lifecycle (Reasoning → Tool Interaction → Control Flow → Memory → Architecture → Verification → Security). All cross-references renumbered. Commit `800c4ea`.
- **Benchmark engine upgraded**: Coverage 58→140 metrics (26%→76%), CLI agent benchmarking added, real cold-start data for reasonix (287ms) and codex (32.5ms). Commits `7e28878`, `178ddb9`, `10a4472`.
- **July monthly report updated**: Added Trend 6 (benchmark infrastructure), expanded project updates with architecture doc work. Commit `23fac48`.
