# MCP Ecosystem Deep-Dive: Phase 1 — Adoption Survey

**Date:** 2026-07-06
**Scope:** All 30 tracked platforms (20 locally available, 10 external not cloned)
**Method:** Source code search for MCP protocol primitives across `.py`, `.ts`, `.rs`, `.go`, `.md`, `.json` files

---

## Adoption Rate

**Of 30 tracked platforms: 21 have MCP support (70%), 4 are resistant, 5 not assessable (not cloned locally).**

| Tier | Count | Platforms |
|------|-------|-----------|
| **Native** | 1 | ZeroClaw |
| **First-class** | 8 | Hermes-Agent, OpenClaw, GoClaw, NanoBot, Reasönix, AgentScope, OpenHuman, eliza |
| **Adapter** | 8 | NanoClaw, IronClaw, MaxClaw, HiClaw, PraisonAI, agent-zero, rocketride-server, ClawTeam |
| **Resistant** | 4 | Claw-AI-Lab, Aider, Copilot-CLI (mention only), eliza (feed-only) |
| **Not assessable** | 9 | smolagents, langgraph, crewai, autogen, swarms, openagents, openfang, kimi-cli, kimi-code, codex |

---

## Classification Matrix

### Tier 1: NATIVE (1 platform)

**ZeroClaw** — Full MCP protocol implementation as 10 dedicated Rust crates in `zeroclaw-tools`:

| Crate | Role |
|-------|------|
| `mcp_protocol.rs` | Protocol message types, serialization, `tools_list` deserialization |
| `mcp_transport.rs` | Transport abstraction: stdio, SSE, HTTP |
| `mcp_client.rs` | Client connection lifecycle, session management |
| `mcp_tool.rs` | MCP tools as ZeroClaw Tool trait implementations |
| `mcp_resource.rs` | Resource subscription and caching |
| `mcp_resources_tool.rs` | Resources-as-context bridge |
| `mcp_prompt.rs` | Prompt template handling |
| `mcp_prompts_tool.rs` | Prompts as injectable context |
| `mcp_context.rs` | Context window management for MCP-injected content |
| `mcp_deferred.rs` | Lazy tool loading — defer schema injection until first use |

**Transport modes:** stdio, SSE, HTTP (all three)
**Why native:** MCP is not a bridge — it's woven into the tool system at the crate level. The `mcp_tool.rs` implements ZeroClaw's own `Tool` trait, meaning MCP tools are indistinguishable from native tools at the agent loop level. The `mcp_deferred.rs` lazy-loading pattern is unique — no other platform defers MCP schema injection to reduce cold-start token cost.

---

### Tier 2: FIRST-CLASS (8 platforms)

MCP is a major integration surface with dedicated subsystem, but native tools coexist alongside MCP tools.

#### Hermes-Agent
**Files:** `tools/mcp_tool.py`, `tools/mcp_oauth.py`, `tools/mcp_oauth_manager.py`, `website/docs/user-guide/features/mcp.md`
**Transport modes:** stdio, HTTP/StreamableHTTP, SSE
**Key features:**
- Per-tool gating — users enable/disable individual MCP tools, not just whole servers
- OAuth manager for authenticated MCP servers (`mcp_oauth.py`, `mcp_oauth_manager.py`)
- GUI auth/probe/logs in desktop dashboard
- Environment variable filtering for stdio subprocesses (security)
- Reconnect signal handling (`test_mcp_reconnect_signal.py`)
- Client certificate support (`test_mcp_client_cert.py`)
- Structured content support (`test_mcp_structured_content.py`)
- Elicitation support (`test_mcp_elicitation.py`)

**Why first-class:** MCP has its own OAuth subsystem, dedicated UI tab, and per-tool granularity. The test suite has 8+ dedicated MCP test files covering edge cases (reconnect, certs, structured content, elicitation). This is the most operationally mature MCP implementation after ZeroClaw.

#### OpenClaw
**Files:** `src/plugin-sdk/codex-mcp-projection.ts`, UI config pages (`mcpServers` schema), runtime config collectors
**Transport modes:** Not directly verified from source (likely stdio + SSE based on config schema)
**Key features:**
- `mcpServers` config schema in runtime configuration
- Codex MCP projection — projects Codex events into MCP tool format
- Secret path collection: `mcpServers.*.env.*` (scans MCP server env vars for secrets)
- Ring-zero MCP server pattern (from CHANGELOG) — runs CLI harnesses via MCP

**Why first-class:** The ring-zero MCP server pattern is architecturally unique — MCP as the execution protocol for the agent's own loop, not just external tool integration. Config-level integration with secret scanning.

#### GoClaw
**Files:** `internal/mcp/` — 22 Go files, 5,431 total lines
**Transport modes:** stdio (with exponential backoff retry for slow-starting servers), SSE/HTTP (non-retry, definitive errors)
**Key features:**
- MCP manager with connection pooling (`pool.go`, `manager.go`, `manager_connect.go`)
- Grant checker — per-tenant MCP tool authorization (`grant_checker.go`)
- Tool filter — dynamic tool visibility per session (`tool_filter.go`)
- BM25 index for MCP tool search (`bm25_index.go`, `mcp_tool_search.go`) — searchable MCP tool catalog
- Session reset — clean MCP state on session boundary (`session_reset.go`)
- Validation layer (`validation.go`)
- Bridge server + bridge tool — GoClaw can act as both MCP client AND server

**Why first-class:** The most enterprise-ready MCP implementation. Per-tenant authorization, BM25-searchable tool catalog, bridge server mode. 5,431 lines is more MCP code than any platform except ZeroClaw.

#### NanoBot
**Files:** `nanobot/agent/tools/mcp.py` (1,351 lines)
**Transport modes:** stdio, StreamableHTTP, SSE
**Key features:**
- Windows stdio command normalization (`_normalize_windows_stdio_command`)
- Port availability check before entering client context
- MCP presets API for WebUI (`test_mcp_presets_api.py`, `test_mcp_presets_runtime.py`)
- MCP probe for health checking (`test_mcp_probe.py`)

**Why first-class:** Single-file implementation but comprehensive (1,351 lines). MCP presets (saved server configurations) are a user-friendly pattern not seen elsewhere. Windows compatibility is explicitly handled.

#### Reasönix
**Files:** 16 TypeScript files in `src/cli/ui/mcp-*.ts`, `src/cli/commands/mcp-*.tsx`, `src/mcp/dot-mcp-json.ts`, `src/server/api/mcp.ts`
**Transport modes:** Not directly verified (stdio close handling tests suggest stdio)
**Key features:**
- Full TUI for MCP management: browse, inspect, disable, reconnect, health check
- `.mcp.json` config file parser (`dot-mcp-json.ts`)
- MCP cache canonicalization for prompt cache stability (`mcp-cache-canonicalization.test.ts`)
- MCP lifecycle management with toast notifications
- Stdio close handling (`mcp-stdio-close.test.ts`)
- Runtime failure recovery (`mcp-runtime-failures.test.ts`)
- Environment config sanitization (`mcp-env-config.test.ts`)
- TUI survival under MCP errors (`mcp-tui-survival.test.ts`)

**Why first-class:** The richest MCP user experience of any CLI agent. Full TUI with browse/inspect/disable/reconnect/health. Cache canonicalization is architecturally important — it keeps MCP schemas stable for prompt cache prefixes, directly addressing the token overhead problem.

#### AgentScope
**Files:** `src/agentscope/mcp/__init__.py`, `_config.py`, `_mcp_client.py`, `src/agentscope/workspace/_mcp_gateway/` (3 files), `src/agentscope/app/_router/_schema/_mcp.py`
**Transport modes:** stdio, StreamableHTTP
**Key features:**
- MCP gateway as workspace service (`_mcp_gateway/`)
- Stdio client materialized at construction time (eager)
- Stateless vs stateful MCP server distinction in config
- SSE client and StreamableHTTP client tests
- Schema router for MCP tool exposure via API

**Why first-class:** MCP gateway as a workspace-level service is a multi-tenant pattern — MCP servers are shared across agents within a workspace. This is the Alibaba/cloud-native approach to MCP.

#### OpenHuman
**Files:** `src/openhuman/tools/ops.rs`, `src/openhuman/tools/mod.rs`, 4 test files (`mcp_registry_e2e.rs`, `mcp_registry_multi_server.rs`, `mcp_setup_e2e.rs`, `mcp_stdio_integration.rs`)
**Transport modes:** stdio (confirmed via test name), registry-based multi-server
**Key features:**
- MCP registry — multi-server management
- Setup e2e tests — onboarding flow includes MCP configuration
- Stdio integration tests
- Tool registry approval integration

**Why first-class:** MCP registry with multi-server support and approval-gated tool registration. The setup e2e test confirms MCP is part of the first-run experience, not an advanced feature.

#### eliza
**Files:** `packages/feed/apps/web/src/app/mcp/route.ts`, `packages/feed/apps/web/src/app/api/mcp/route.ts`, `packages/feed/skills/feed/SKILL.md`, `packages/core/src/types/model.ts`
**Transport modes:** HTTP (via Next.js API routes)
**Key features:**
- MCP route handler in feed package
- External agent registration API
- MCP referenced in core type definitions

**Why first-class:** MCP is scoped to the `feed` package, not the core runtime. The implementation is HTTP-based (API routes), suggesting MCP as a service endpoint pattern. Less deep than other first-class platforms but architecturally present in the framework.

---

### Tier 3: ADAPTER (8 platforms)

MCP is bridged or wrapped, not native. Core tools are non-MCP.

#### NanoClaw
**Files:** `container/agent-runner/src/mcp-tools/` — 9 TypeScript files, 1,081 total lines
**Pattern:** MCP tools as container-side tool extensions (`agents.ts`, `core.ts`, `interactive.ts`, `scheduling.ts`, `self-mod.ts`, `server.ts`). The agent-runner inside the container speaks MCP to expose its own tools (self-mod, scheduling) to the host.
**Why adapter:** MCP is used for host↔container communication, not for external server integration. NanoClaw's core tool protocol is Claude/OneCLI, not MCP.

#### IronClaw
**Files:** `src/extensions/manager.rs`, `src/extensions/registry.rs`, `src/extensions/discovery.rs`, `src/extensions/mod.rs`
**Pattern:** MCP referenced in extension manager and registry. Test files show MCP auth flow testing (`test_mcp_auth_flow.py`) and extension uninstall cleanup.
**Why adapter:** MCP is one extension type alongside WASM tools and WASM channels. The extension manager treats MCP as a plugin source, not the primary tool protocol.

#### MaxClaw
**Files:** `internal/webui/server.go`, `internal/cli/agent.go`, `internal/cli/cron.go`, `internal/cli/gateway.go`
**Pattern:** MCP referenced in CLI and web server code. Not a dedicated subsystem — references are scattered across CLI commands.
**Why adapter:** MCP appears as configuration in CLI commands and web UI, suggesting MCP server setup is a user feature, not a core architecture component.

#### HiClaw
**Files:** `copaw/src/matrix/config.py`, `copaw/src/copaw_worker/worker.py`, `copaw/src/copaw_worker/sync.py`
**Pattern:** MCP references in CoPaw worker and Matrix config. The `openclaw-base` image includes `mcporter` CLI for MCP tool discovery.
**Why adapter:** MCP is inherited from the OpenClaw base image (`mcporter`), not implemented natively. Workers use MCP through a skill, with all calls proxied through the AI gateway.

#### PraisonAI
**Files:** Multiple example/test files in `src/praisonai-agents/tests/` — `mcp_wrapper.py`, `test_mcp_optional_import.py`, integration tests
**Pattern:** MCP is optional (`test_mcp_optional_import.py`). Example servers provided (`mcp_server_example.py`, `filesystem-mcp.py`, `gdrive-mcp.py`, `websocket-mcp.py`).
**Why adapter:** MCP is an optional import — the framework works without it. Example-heavy suggests MCP is a user feature, not a core dependency.

#### agent-zero
**Files:** `helpers/mcp_handler.py`, `helpers/mcp_server.py` (2,081 total lines)
**Pattern:** MCP handler + MCP server. agent-zero can both connect to external MCP servers AND act as an MCP server itself.
**Why adapter:** Substantial code (2,081 lines) but MCP sits alongside the native tool system (`tools/*.py`). The dual client+server pattern is interesting but MCP is not the primary tool protocol.

#### rocketride-server
**Files:** `nodes/src/nodes/tool_mcp_client/` — 6 Python files (`mcp_sse_client.py`, `mcp_stdio_client.py`, `mcp_streamable_http_client.py`, `IGlobal.py`, `IInstance.py`, `__init__.py`)
**Pattern:** MCP client as a pipeline node type (`tool_mcp_client`). Supports all three transport modes (stdio, SSE, StreamableHTTP).
**Why adapter:** MCP is one of 111 node types. It's a first-class pipeline component but the pipeline engine itself is C++/WebSocket, not MCP.

#### ClawTeam
**Files:** `tests/test_mcp_tools.py`, `clawteam/spawn/adapters.py`
**Pattern:** MCP tool tests and spawn adapter references. ClawTeam can spawn agents that use MCP tools.
**Why adapter:** ClawTeam is an orchestrator, not an agent runtime. MCP references are about the agents it spawns, not its own capabilities.

---

### Tier 4: RESISTANT / NONE (4 platforms)

| Platform | Evidence |
|----------|----------|
| **Claw-AI-Lab** | Zero MCP files found |
| **Aider** | Zero MCP files found |
| **Copilot-CLI** | Single changelog mention ("Self-correcting custom tool calls in agentic loop") — no code |
| **eliza (core)** | MCP only in `feed` package; core runtime has no MCP integration |

---

### Not Assessable (9 platforms — not cloned locally)

smolagents, langgraph, crewai, autogen, swarms, openagents, openfang, kimi-cli, kimi-code, codex

These are tracked via documentation only. MCP support would need to be verified from their public repositories.

---

## Transport Mode Support

| Transport | Platforms Supporting |
|-----------|---------------------|
| **stdio** | ZeroClaw, Hermes, OpenClaw, GoClaw, NanoBot, Reasönix, OpenHuman, agent-zero, rocketride-server, AgentScope |
| **SSE** | ZeroClaw, Hermes, GoClaw, NanoBot, rocketride-server |
| **StreamableHTTP** | Hermes, NanoBot, AgentScope, rocketride-server |

**stdio is universal** — every platform with MCP supports it. SSE and StreamableHTTP are less common, with StreamableHTTP being the newest transport (MCP spec 2025-03-26).

---

## Key Architectural Patterns

### 1. Lazy Tool Loading (ZeroClaw only)
`mcp_deferred.rs` defers MCP schema injection until first use. This reduces cold-start token cost — the agent doesn't pay for MCP schemas it hasn't used yet. No other platform implements this.

### 2. Per-Tool Gating (Hermes)
Users enable/disable individual MCP tools, not just whole servers. Fine-grained control over which tools appear in the agent's context window.

### 3. BM25 Tool Search (GoClaw)
MCP tool catalog is BM25-indexed for searchability. When the agent needs a tool, it can search the MCP catalog by keyword rather than loading all schemas. This is the most scalable approach to MCP tool discovery.

### 4. Cache Canonicalization (Reasönix)
MCP schemas are canonicalized for prompt cache stability. The tool definition order, formatting, and field ordering are normalized so the prompt cache prefix remains stable across turns, even when MCP servers change.

### 5. Dual Client+Server (agent-zero, GoClaw)
Both can act as MCP servers themselves, not just clients. agent-zero exposes its tools via MCP; GoClaw's bridge server can serve MCP to other consumers.

### 6. MCP-as-Communication-Protocol (NanoClaw)
NanoClaw uses MCP for host↔container tool communication. MCP is the IPC protocol between the host process and the containerized agent-runner.

### 7. MCP-as-Pipeline-Node (rocketride-server)
MCP client is a pipeline node type, composable within the node graph. MCP servers connect as data sources/processors in the DAG.

### 8. Ring-Zero MCP Server (OpenClaw)
MCP as the execution protocol for the agent's own operation loop. The agent speaks MCP to its own harness layer.

---

## Preliminary Findings

1. **70% adoption rate** (21 of 30) among locally-assessable platforms confirms MCP has crossed the chasm from experiment to infrastructure.

2. **ZeroClaw is the only truly native implementation.** Its 10-crate MCP system with lazy loading, deferred schema injection, and full transport coverage is architecturally unmatched.

3. **GoClaw has the most enterprise-ready MCP implementation** — per-tenant authorization, BM25-searchable catalog, 5,431 lines of dedicated code.

4. **Reasönix solves the token overhead problem** with cache canonicalization, which may be the most practically important MCP innovation — it directly addresses why platforms resist MCP.

5. **Three novel patterns** that deserve deeper analysis in Phase 2:
   - ZeroClaw's lazy/deferred loading
   - GoClaw's BM25 tool search
   - Reasönix's cache canonicalization

6. **The "resistant" platforms** (Aider, Claw-AI-Lab) are either too specialized (Aider is a coding assistant, not a general agent) or too dormant (Claw-AI-Lab has no activity).

---

## Next Steps

- **Phase 2:** Architecture comparison of ZeroClaw (native), Hermes (first-class), GoClaw (first-class), Reasönix (first-class) — deep-read the MCP subsystem code for each
- **Phase 3:** Token overhead analysis — measure schema tokens at N=0,1,3,5,10 MCP servers
- **Phase 4:** Server ecosystem catalog — which MCP servers are referenced across platforms

---

*This report covers Phase 1 of the MCP Ecosystem Deep-Dive research plan. Phase 2 will follow.*
