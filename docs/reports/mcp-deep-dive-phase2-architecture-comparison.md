# MCP Ecosystem Deep-Dive: Phase 2 — Architecture Comparison

**Date:** 2026-07-06
**Scope:** Deep-dive into 4 platforms: ZeroClaw (Native), Hermes (First-class), GoClaw (First-class), Reasönix (First-class)
**Method:** Source code analysis of MCP subsystem internals — transport, lifecycle, tool discovery, caching, security, and auth

---

## Executive Summary

The four platforms represent four fundamentally different answers to the same question: how should an agent runtime integrate MCP tools? Each answer optimizes for a different constraint:

| Platform | Optimization Target | Core Innovation |
|----------|-------------------|-----------------|
| **ZeroClaw** | Token efficiency at scale | Deferred loading + `tool_search` activation |
| **Hermes** | Operational maturity | OAuth + per-tool gating + sampling |
| **GoClaw** | Enterprise multi-tenancy | BM25 tool search + bridge server + grant checker |
| **Reasönix** | Prompt cache stability | Schema canonicalization for cache prefixes |

These are not incremental differences. Each platform's MCP architecture shapes the entire user experience — from how many tokens a conversation costs, to whether MCP tools work behind enterprise auth, to whether reordering a config file invalidates the prompt cache.

---

## Dimension 1: Transport Architecture

### ZeroClaw — Trait-Based Multi-Transport

```
McpTransportConn (trait)
├── StdioTransport    (tokio process + AsyncBufReadExt)
├── SseTransport      (reqwest + SSE stream)
└── HttpTransport     (reqwest + Mcp-Session-Id header)
```

ZeroClaw defines a `McpTransportConn` trait with `send_and_recv()` and `reset()`. Each transport is a separate struct implementing the trait. The `reset()` method re-establishes sessions for stateful transports (HTTP/SSE) and is a no-op for stdio.

**Error recovery:** `McpTransportError` distinguishes `StaleSession` (HTTP 404/410 — server restarted) from `TransportClosed` (SSE EOF). Both are recoverable by reconnecting and re-running the MCP handshake. This is the only platform with explicit stale-session detection.

**Timeout granularity:** Tool calls use per-server configurable timeouts (`tool_timeout_secs`). Non-tool requests (init/list) use a fixed 30-second timeout. HTTP transport default is 120 seconds.

### Hermes — Background Event Loop

```
_mcp_loop (daemon thread asyncio event loop)
├── Server 1: stdio_client(command, args)
├── Server 2: streamable_http_client(url)
├── Server 3: sse_client(url)
└── ... (one long-lived asyncio Task per server)
```

Hermes runs all MCP servers on a single dedicated background event loop in a daemon thread. Each server is a long-lived asyncio Task. Tool calls are scheduled onto the loop via `run_coroutine_threadsafe()`.

**Security:** Environment variable filtering for stdio subprocesses — only explicitly configured `env` keys are passed, preventing credential leakage from the parent process.

**Reconnection:** Automatic exponential backoff (up to 5 retries). The background loop survives individual server failures.

**Sampling:** MCP servers can request LLM completions via `sampling/createMessage`. The config schema supports per-server sampling overrides: model selection, max_tokens cap, timeout, rate limiting (max RPM), allowed model whitelist, tool loop limit, and audit logging. This is the only platform where MCP servers can call back to the LLM with controlled parameters.

### GoClaw — Manager + Connection Pool

```
Manager (goroutine-safe)
├── pool.go        — connection pooling
├── manager_connect.go — transport-specific connect logic
├── stdio: exponential backoff retry (slow-starting servers)
├── SSE/HTTP: definitive failure (no retry)
└── session_reset.go — clean MCP state on session boundary
```

GoClaw treats MCP connections as pooled resources. The manager handles connection lifecycle with transport-specific error semantics: stdio servers get exponential backoff retry (because they may be slow to start), while SSE/HTTP failures are definitive (connection errors mean the server is down, not slow).

**Session boundaries:** `session_reset.go` explicitly cleans MCP server state at session boundaries, preventing cross-session state leakage — critical for multi-tenant deployments.

### Reasönix — CLI-Native Transport Parsing

```
parseMcpSpec(input: string) → McpSpec
├── "name=npx -y @server"        → StdioMcpSpec
├── "name=https://server/sse"    → SseMcpSpec
├── "name=streamable+https://..." → StreamableHttpMcpSpec
└── --mcp flag on CLI
```

Reasönix parses MCP server specs from CLI flags (`--mcp`). Transport type is inferred from the URL: `streamable+` prefix for Streamable HTTP, plain `http://` for SSE (backwards compat), everything else is shell-split into a stdio command.

**Key design:** Transport selection is declarative, not configurational. Users don't specify `transport: "sse"` — they just use an SSE URL. This is the most user-friendly transport selection mechanism.

### Comparison

| Feature | ZeroClaw | Hermes | GoClaw | Reasönix |
|---------|----------|--------|--------|----------|
| stdio | ✅ | ✅ | ✅ | ✅ |
| SSE | ✅ | ✅ | ✅ | ✅ |
| StreamableHTTP | ✅ | ✅ | ❓ | ✅ |
| Stale session detection | ✅ | ❌ | ❌ | ❌ |
| Exponential backoff | ✅ | ✅ (5 retries) | ✅ (stdio only) | ✅ (reconnect.ts) |
| Env var filtering | ❌ | ✅ | ❌ | ❌ |
| Connection pooling | ❌ | ❌ | ✅ | ❌ |
| Session reset | ❌ | ❌ | ✅ | ❌ |

---

## Dimension 2: Tool Discovery & Token Management

This is where the architectures diverge most sharply. Each platform handles the "how does the LLM know what MCP tools exist" problem differently.

### ZeroClaw — Deferred Loading with `tool_search`

**The most token-efficient pattern.**

When `mcp.deferred_loading` is enabled:

1. At startup, ZeroClaw connects to all MCP servers and calls `tools/list`
2. Instead of injecting all tool schemas into the LLM context, it creates `DeferredMcpToolStub` objects containing only the tool name + description
3. Only these lightweight stubs appear in the system prompt
4. A built-in `tool_search` tool is registered — the LLM calls it with keywords to find relevant MCP tools
5. `DeferredMcpToolSet::search()` does keyword matching (case-insensitive term hits) and returns ranked results
6. When a tool is "activated," its full JSON schema is fetched from the stub's stored definition and added to the `ActivatedToolSet` (per-conversation mutable state)
7. The agent loop consults `ActivatedToolSet` each iteration to determine which tool specs to include

**Token impact:** With 10 MCP servers × 5 tools each = 50 tools, the eager approach injects 50 full JSON schemas. ZeroClaw's deferred approach injects 50 name+description pairs (much smaller) + 1 `tool_search` tool definition. The full schemas are loaded only for tools the LLM actually uses.

**Key code** (`mcp_deferred.rs:1-7`):
```
//! When `mcp.deferred_loading` is enabled, MCP tool schemas are NOT eagerly
//! included in the LLM context window. Instead, only lightweight stubs (name +
//! description) are exposed in the system prompt. The LLM must call the built-in
//! `tool_search` tool to fetch full schemas, which moves them into the
//! [`ActivatedToolSet`] for the current conversation.
```

### GoClaw — BM25-Indexed Tool Search

**The most searchable pattern.**

GoClaw implements the same deferred-loading concept as ZeroClaw but uses a proper BM25 ranking algorithm instead of simple keyword matching.

1. When the total MCP tool count exceeds an inline threshold, GoClaw switches to "search mode"
2. A BM25 index (`bm25_index.go`) is built from all deferred tool names + descriptions
3. The `mcp_tool_search` tool replaces individual MCP tools in the registry
4. The tool's description explicitly instructs the LLM: "Before performing any external service operation, you MUST search here first"
5. BM25 search returns ranked results, which are activated in the registry
6. Activated tools become available on the next agent loop iteration

**Key code** (`mcp_tool_search.go:39-48`):
```go
func (t *MCPToolSearchTool) Description() string {
    return "Search for available external integration tools (MCP) by keyword. " +
        "IMPORTANT: You have access to external service integrations " +
        "(databases, APIs, file systems, messaging, etc.) through MCP tools " +
        "that are NOT loaded by default. Before performing any external service " +
        "operation, you MUST search here first to discover available tools."
}
```

**vs ZeroClaw:** BM25 is more sophisticated than ZeroClaw's term-hit counting. BM25 accounts for term frequency, inverse document frequency, and document length normalization. For large tool catalogs (50+ tools), BM25 will surface more relevant results.

### Hermes — Per-Server, Per-Tool Gating

**The most operationally mature pattern.**

Hermes doesn't defer tool loading — it loads all configured MCP tool schemas eagerly. But it provides two levels of gating:

1. **Per-server:** Enable/disable entire MCP servers in config (`disabled: true`)
2. **Per-tool:** Enable/disable individual tools within a server (via the desktop dashboard UI)

Users who want zero MCP token overhead simply disable the servers they don't need. Users who want fine-grained control disable specific tools within active servers.

**Parallel tool calls:** Per-server `supports_parallel_tool_calls` flag. When enabled, tools from the same server can execute concurrently. This is unique — other platforms treat MCP tool calls as sequential.

### Reasönix — Schema Canonicalization for Cache Stability

**The most prompt-cache-aware pattern.**

Reasönix solves a different problem: not "how many tokens" but "do the tokens change between turns."

MCP tool schemas are JSON objects. JSON object keys have no inherent ordering. Two `tools/list` calls to the same MCP server can return schemas with keys in different order — `{required: ["b", "a"], properties: {...}}` vs `{required: ["a", "b"], properties: {...}}`. This difference is semantically meaningless but byte-significant: it invalidates the prompt cache prefix, forcing a full reprocessing of the context.

Reasönix's `canonicalizeSchemaForCache()` solves this:

1. **Sort all object keys** alphabetically (recursively)
2. **Sort `required` arrays** alphabetically
3. **Sort `dependentRequired` inner arrays** alphabetically
4. **Preserve `enum` order** (enums are NOT sorted — their order may be semantically meaningful as a priority hint)
5. **Sort set-like arrays** (`SET_LIKE_SCHEMA_ARRAY_KEYS`) when all elements are scalars
6. **Sort bridged tools** by their final registered name in the registry

**Key code** (`registry.ts:218-242`):
```typescript
export function canonicalizeSchemaForCache(value: unknown, parentKey?: string): unknown {
  if (Array.isArray(value)) {
    const mapped = value.map((item) => canonicalizeSchemaForCache(item));
    if (parentKey && SET_LIKE_SCHEMA_ARRAY_KEYS.has(parentKey) && mapped.every(isScalar)) {
      return [...mapped].sort((a, b) => String(a).localeCompare(String(b)));
    }
    return mapped;
  }
  // ... recursive key sorting
}
```

**Impact:** Without canonicalization, adding a new MCP server or restarting an MCP server (which may change tool ordering) invalidates the prompt cache, potentially costing thousands of tokens for reprocessing. With canonicalization, the cache prefix is stable as long as the same set of tools exists, regardless of discovery order.

### Comparison

| Feature | ZeroClaw | Hermes | GoClaw | Reasönix |
|---------|----------|--------|--------|----------|
| Eager loading | Optional (default: deferred) | ✅ | Threshold-based | ✅ |
| Deferred loading | ✅ (`mcp.deferred_loading`) | ❌ | ✅ (search mode) | ❌ |
| Tool search algorithm | Keyword term-hits | N/A | BM25 | N/A |
| Per-tool gating | ❌ | ✅ (UI) | ✅ (allow/deny filter) | ❌ |
| Cache canonicalization | ❌ | ❌ | ❌ | ✅ |
| Parallel tool calls | ❌ | ✅ (per-server) | ❌ | ❌ |
| Tool prefix collision | `<server>__<tool>` naming | Namespaced | Registry namespaced | `srv_` prefix |

---

## Dimension 3: Lifecycle & Health

### ZeroClaw

- **Connection:** Per-server connection with `McpRegistry` tracking all active connections
- **Health:** Stale session detection (HTTP 404/410) triggers automatic reconnection
- **Recovery:** Transport errors (`StaleSession`, `TransportClosed`) are caught and retried with session reset
- **Shutdown:** Server Tasks are signaled to exit their `async with` blocks in the owning task

### Hermes

- **Connection:** Dedicated background event loop, one asyncio Task per server
- **Health:** Reconnect signal handling (`test_mcp_reconnect_signal.py`), client certificate support
- **Recovery:** Exponential backoff (up to 5 retries), credential stripping in error messages returned to LLM
- **Security preflight:** OSV malware check during stdio startup (12s timeout, fail-open)
- **Shutdown:** Each server Task exits its `async with` block; anyio cancel-scope cleanup runs in the owning Task

### GoClaw

- **Connection:** Manager + connection pool, transport-specific connect logic
- **Health:** Session reset at session boundaries prevents cross-session state leakage
- **Recovery:** stdio gets exponential backoff; SSE/HTTP errors are definitive
- **Bridge server:** GoClaw can act as an MCP server, exposing 24 internal tools via StreamableHTTP

### Reasönix

- **Connection:** Per-server client with transport-specific connection logic
- **Health:** Drift detection (`drift.ts`), latency monitoring (`latency.ts`), health check (`mcp-health.ts`), reconnect (`reconnect.ts`)
- **Recovery:** Reconnect kickoff UI (`mcp-reconnect-kickoff.ts`), runtime failure recovery (`mcp-runtime-failures.test.ts`)
- **TUI:** Full MCP lifecycle management — browse, inspect, disable, reconnect, health check — all from the CLI

---

## Dimension 4: Security & Auth

### GoClaw — Enterprise-Grade

**Grant checker** (`grant_checker.go`): Per-tenant MCP tool authorization. Each tenant can have allow/deny lists for MCP tools.

**Tool filter** (`tool_filter.go`): Dynamic tool visibility per session. Non-allowed tools never reach the LLM — filtered at registration time.

**Semantics:**
- Empty allow + empty deny → allowed (no filter)
- Tool in deny → denied (deny takes priority)
- Non-empty allow + tool NOT in allow → denied
- Otherwise → allowed

### Hermes — OAuth + Sampling Control

**OAuth manager** (`mcp_oauth.py`, `mcp_oauth_manager.py`): Full OAuth flow for authenticated MCP servers. The only platform with dedicated MCP OAuth support.

**Sampling controls:** When MCP servers request LLM completions via `sampling/createMessage`, Hermes enforces:
- Model override (optional)
- max_tokens cap
- Timeout
- Rate limiting (max RPM)
- Model whitelist (empty = all)
- Tool loop limit
- Audit log level

This prevents MCP servers from consuming unlimited LLM tokens.

### ZeroClaw — Approved-Field Stripping

**Security model integration:** ZeroClaw's security model injects `approved: bool` into tool calls for supervised-mode confirmation. MCP servers don't know about this field and would reject calls containing it. The `McpToolWrapper::execute()` strips it before forwarding to the MCP server (`mcp_tool.rs:55-66`).

### Reasönix

**Preflight** (`preflight.ts`): Pre-connection validation checks.

### Comparison

| Feature | ZeroClaw | Hermes | GoClaw | Reasönix |
|---------|----------|--------|--------|----------|
| Per-tenant authorization | ❌ | ❌ | ✅ | ❌ |
| OAuth | ❌ | ✅ | ❌ | ❌ |
| Sampling control | ❌ | ✅ | ❌ | ❌ |
| Tool allow/deny filter | ❌ | ✅ (per-tool UI) | ✅ (grant-based) | ❌ |
| Env var filtering | ❌ | ✅ | ❌ | ❌ |
| OSV malware check | ❌ | ✅ | ❌ | ❌ |

---

## Dimension 5: Unique Patterns Not Seen Elsewhere

### ZeroClaw — Deferred Tool Resolution
`ActivatedToolSet::get_resolved()` resolves tools by exact name first, then by unique MCP suffix. This handles a real bug: some model providers strip the `<server>__` prefix when calling a deferred MCP tool. If the suffix maps to exactly one activated tool, the call proceeds. This is defensive programming for model provider inconsistency — a problem no other platform addresses.

### Hermes — Server-Initiated LLM Requests (Sampling)
MCP servers can call `sampling/createMessage` to request LLM completions. Hermes routes these through its provider system with full controls (model override, token cap, rate limit, model whitelist, tool loop limit, audit log). This makes MCP servers first-class participants in the agent loop, not just tool providers.

### GoClaw — Bridge Server (Dual Client+Server)
GoClaw exposes 24 internal tools (`read_file`, `write_file`, `exec`, `web_search`, `memory_search`, `browser`, `cron`, `message`, `sessions_*`, `team_tasks`) as an MCP server via StreamableHTTP. Other MCP clients can connect to GoClaw and use its capabilities. This is the only platform that is both a significant MCP client AND server.

### Reasönix — Enum Order Preservation
During schema canonicalization, Reasönix explicitly preserves `enum` array order while sorting everything else. The insight: enum ordering may be semantically meaningful (priority hints, default-first ordering). Sorting enums could change LLM behavior. This is a subtle correctness concern that no other platform considers.

---

## Architecture Comparison Matrix

| Dimension | ZeroClaw (Native) | Hermes (First-class) | GoClaw (First-class) | Reasönix (First-class) |
|-----------|-------------------|----------------------|----------------------|------------------------|
| **LOC** | ~3,500 (10 crates) | ~5,087 (3 files) | ~5,431 (22 files) | ~2,500 (23 files) |
| **Transport** | All 3 + session header | All 3 + keepalive | stdio (retry) + SSE/HTTP (definitive) | All 3 via CLI flag |
| **Tool loading** | Deferred (keyword search) | Eager (per-tool gating) | Threshold → BM25 search | Eager (cache canonicalized) |
| **Token optimization** | Best (stubs + search) | Good (disable unused) | Best (BM25 search) | Good (cache stability) |
| **Cache stability** | ❌ | ❌ | ❌ | ✅ (canonicalization) |
| **Security** | Approved-field strip | OAuth + env filter + OSV | Per-tenant grants + allow/deny | Preflight |
| **Dual client/server** | ❌ | ❌ | ✅ (bridge server) | ❌ |
| **Sampling** | ❌ | ✅ (with controls) | ❌ | ❌ |
| **Best for** | Token-critical / many tools | Authenticated MCP servers | Enterprise multi-tenant | CLI users with prompt caching |

---

## Key Findings

1. **The deferred-loading pattern (ZeroClaw + GoClaw) is the answer to the token overhead problem.** Both platforms avoid injecting all MCP schemas by default. ZeroClaw uses keyword search; GoClaw uses BM25. This is the pattern most likely to be adopted by other platforms as MCP tool catalogs grow.

2. **Reasönix's cache canonicalization is the unsung hero.** Token overhead gets the attention, but cache invalidation is the silent cost. Reasönix is the only platform that ensures MCP tool schemas don't break prompt caching — potentially saving more tokens than deferred loading in long conversations.

3. **GoClaw's bridge server redefines the MCP boundary.** By exposing its own tools as an MCP server, GoClaw makes the agent itself a composable MCP component. This blurs the client/server distinction in a way no other platform does.

4. **Hermes' sampling support makes MCP servers active participants.** Instead of MCP servers passively responding to tool calls, they can request LLM completions — with Hermes controlling model, token budget, rate limits, and audit trail. This is the foundation for MCP-native agent-to-agent communication.

5. **No platform combines all innovations.** The ideal MCP implementation would have ZeroClaw's deferred loading + Reasönix's cache canonicalization + GoClaw's BM25 search + Hermes' OAuth/sampling. Each platform has solved a different piece of the puzzle.

---

## Implications for Phase 3 (Token Overhead)

The Phase 2 findings directly shape the Phase 3 measurement plan:

1. **ZeroClaw's deferred mode must be measured separately from eager mode** — the token difference should be dramatic
2. **GoClaw's threshold-based search mode** should be measured at N < threshold (eager) vs N > threshold (search)
3. **Reasönix's canonicalization** doesn't reduce token count but reduces cache misses — the measurement should track cache hit rate, not just token count
4. **Hermes' per-tool gating** means the "all tools enabled" vs "no tools enabled" range is the interesting comparison

---

*This report covers Phase 2 of the MCP Ecosystem Deep-Dive. Phase 3 (Token Overhead Analysis) will follow.*
