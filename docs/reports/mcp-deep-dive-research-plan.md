# MCP Ecosystem Deep-Dive: Research Plan

**Status:** Planned (Q3 2026 ROADMAP item)
**Target deliverable date:** July 2026 monthly report
**Prerequisites:** ✅ Submodule sync complete, ✅ 26 platforms available locally

---

## Research Questions (from ROADMAP)

1. What is the actual token overhead of MCP in production deployments?
2. Which MCP servers are most widely adopted?
3. How do MCP-native frameworks differ from MCP-adapter approaches?
4. What is the rate of MCP adoption across the 26 tracked platforms?

---

## Phase 1: Adoption Survey (code-level)

**Goal:** Classify all 26 platforms as native / adapter / resistant and map MCP touchpoints.

**Method:** For each platform, search source for MCP protocol primitives:
- `initialize`, `tools/list`, `tools/call`, `resources/list`, `prompts/list`
- `mcp_transport`, `mcp_client`, `mcp_server`, `mcporter`
- `stdio`, `SSE`, `StreamableHTTP` transport implementations
- MCP config schema (`mcpServers`, `mcp_servers`)

**Classification criteria:**

| Tier | Definition |
|------|-----------|
| **Native** | MCP is the primary tool protocol; tools are defined as MCP servers; agent loop speaks MCP natively |
| **First-class** | Dedicated MCP subsystem (transport, client, config, UI); MCP is a major integration surface but not the only tool protocol |
| **Adapter** | MCP bridge/adapter wraps external servers, but core tools are non-MCP |
| **Resistant** | Explicitly chose not to implement MCP; or no MCP code at all |

**Preliminary signals from submodule sync:**

| Platform | Signal | Likely Tier |
|----------|--------|-------------|
| ZeroClaw | 12+ MCP Rust crates (`mcp_transport`, `mcp_tool`, `mcp_resources_tool`, `mcp_protocol`, `mcp_client`, `mcp_context`, `mcp_deferred`, `mcp_prompts_tool`, `mcp_prompt`) | **Native** |
| Hermes-Agent | "first-class MCP tab — catalog, GUI auth/probe/logs, per-tool gating"; `mcporter` CLI; native MCP client (stdio/HTTP) | **First-class** |
| OpenClaw | "ring-zero MCP server" for in-loop CLI harness execution; `mcporter` referenced in HiClaw base image | **First-class** |
| IronClaw | "MCP" referenced in tool registry docs; WASM tool/MCP dichotomy in AGENTS.md | **Adapter** (needs verification) |
| GoClaw | `internal/mcp/` — "Model Context Protocol bridge/server" per AGENTS.md | **Adapter** |
| AgentScope | RAG module, MCP integration in middleware | **Adapter** (needs verification) |
| NanoBot | `MCP servers` listed under tools in AGENTS.md | **Adapter** |
| HiClaw | `mcporter` in openclaw-base image; Worker skill for MCP tool discovery | **Adapter** (via OpenClaw base) |

**Remaining 18 platforms need surveying.**

**Deliverable:** MCP adoption matrix (26 platforms × tier + evidence)

---

## Phase 2: Architecture Comparison

**Goal:** Compare how native vs adapter platforms implement MCP differently.

**Sub-questions:**
- How does tool schema injection work in native vs adapter approaches?
- What happens to prompt caching when MCP tools are dynamically discovered?
- How do platforms handle MCP server lifecycle (startup, health, restart)?
- What transport modes are supported (stdio, SSE, StreamableHTTP)?

**Platforms to deep-dive:**
- ZeroClaw (native) — 12+ MCP crates, fullest implementation
- Hermes-Agent (first-class) — catalog + GUI auth + per-tool gating
- OpenClaw (first-class) — ring-zero MCP server pattern
- GoClaw (adapter) — MCP bridge in Go

**Deliverable:** Architecture comparison table (transport, lifecycle, caching impact, auth, resource handling)

---

## Phase 3: Token Overhead Analysis

**Goal:** Measure the actual token cost of MCP tool schemas in agent context.

**Method:**

1. **Static analysis:** For each platform with MCP support, count the tokens in the MCP-injected tool schemas by:
   - Starting the platform with N MCP servers configured
   - Capturing the system prompt + tool definitions sent to the LLM
   - Counting tokens with tiktoken (OpenAI) / anthropic tokenizer

2. **Progressive overhead:** Measure at N=0, 1, 3, 5, 10 MCP servers to plot overhead growth curve

3. **Comparison:** MCP tool schema tokens vs equivalent native tool definition tokens for the same capability

**Candidate platforms for measurement:**
- Hermes-Agent (has `hermes mcp` catalog, can configure servers via config.yaml)
- ZeroClaw (has MCP config in schema)
- NanoBot (Python, easy to instrument)

**Deliverable:** Token overhead table + growth curve chart

**Limitation:** This requires running platforms locally with real MCP server configurations. Some platforms may not be buildable in this environment (Rust toolchain issues). Fallback: extract schema JSON from source code and count tokens statically.

---

## Phase 4: MCP Server Ecosystem Catalog

**Goal:** Identify which MCP servers are referenced, recommended, or bundled across platforms.

**Method:**

1. Search all platforms for MCP server names/configs:
   - `mcporter` catalogs
   - Config examples mentioning specific servers (filesystem, github, postgres, etc.)
   - Documentation recommending specific MCP servers

2. Cross-reference with the public MCP server registry (modelcontextprotocol/servers)

3. Categorize by type: developer tools, databases, cloud services, communication, file systems

**Deliverable:** MCP server ecosystem catalog (server name, type, platforms referencing it, adoption signal)

---

## Phase 5: Synthesis and Recommendations

**Goal:** Answer the strategic questions for the monthly report.

**Analysis:**

1. **Adoption rate:** X of 26 platforms (Y%) have MCP support. Of those, Z are native.

2. **The native-vs-adapter tradeoff:**
   - Native (ZeroClaw): maximum flexibility, but every tool pays MCP schema overhead
   - First-class (Hermes, OpenClaw): MCP alongside native tools, user chooses
   - Adapter (GoClaw, NanoBot): MCP as bridge, minimal architecture change

3. **Token cost verdict:** Is MCP's schema overhead justified by interoperability gains?

4. **MCP vs alternatives:** How does MCP compare to OpenClaw's plugin SDK, Hermes' skill system, IronClaw's WASM tools?

5. **Recommendations:**
   - For platform developers: when to adopt MCP vs build native tools
   - For users: which platforms offer the best MCP experience
   - For the MCP protocol team: what gaps exist in current adoption

**Deliverable:** Full MCP deep-dive report for July 2026 monthly report

---

## Execution Plan

| Phase | Method | Estimated effort | Dependency |
|-------|--------|-----------------|------------|
| 1. Adoption Survey | `grep` + `read_file` across 26 platforms | 1 subagent dispatch | None |
| 2. Architecture Comparison | Deep-read 4 platform MCP implementations | 1 subagent dispatch | Phase 1 |
| 3. Token Overhead | Run platforms + tiktoken, or static schema extraction | Code execution | Phase 1 |
| 4. Server Catalog | `grep` for server names + cross-reference registry | 1 subagent dispatch | None |
| 5. Synthesis | Write report from Phases 1-4 | Manual | All |

**Parallelizable:** Phases 1 and 4 can run concurrently. Phase 2 depends on Phase 1 results.

---

## Preliminary Observations (from submodule sync data)

1. **ZeroClaw has the deepest MCP investment** — 12+ dedicated Rust crates covering transport, tools, resources, prompts, context, deferred resolution. This is a full protocol implementation, not an adapter.

2. **The "ring-zero MCP server" pattern (OpenClaw)** is novel — using MCP as the protocol for in-agent-loop CLI harness execution, not just for external tool integration. This blurs the line between "tool" and "agent runtime."

3. **Hermes' per-tool gating** solves the token overhead problem pragmatically — users can selectively enable/disable individual MCP tools rather than loading all schemas every turn.

4. **GoClaw treats MCP as a bridge** (`internal/mcp/` — "bridge/server"), suggesting MCP sits alongside native Go tool implementations rather than replacing them.

5. **HiClaw's `mcporter` integration** shows MCP being used in multi-agent orchestration — Workers discover and use MCP tools through a skill, with all calls proxied through an AI gateway for credential isolation.

---

*This plan will be executed as the July 2026 monthly report research cycle.*
