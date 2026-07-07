# MCP Ecosystem Deep-Dive: Phases 4-5 — Server Catalog & Synthesis

**Date:** 2026-07-06
**Scope:** All 30 tracked platforms
**Completes:** MCP Ecosystem Deep-Dive research (Phases 1-5)

---

## Phase 4: MCP Server Ecosystem Catalog

### Method

Searched all locally-available platforms for references to specific MCP server packages (`@modelcontextprotocol/server-*`, `mcp-server-*`, custom servers). Cataloged every server name found in source code, documentation, config examples, and test files.

### Server Catalog

#### Tier 1: Universal MCP Servers (referenced by 5+ platforms)

| Server | Package | Platforms Referencing | Category |
|--------|---------|-----------------------|----------|
| **filesystem** | `@modelcontextprotocol/server-filesystem` | 11 (OpenClaw, GoClaw, MaxClaw, NanoBot, Hermes, AgentScope, eliza, Reasönix, OpenHuman, PraisonAI, IronClaw) | File system |
| **github** | `@modelcontextprotocol/server-github` | 9 (OpenClaw, NanoClaw, NanoBot, Hermes, eliza, Reasönix, OpenHuman, PraisonAI, HiClaw) | Developer tools |
| **memory** | `@modelcontextprotocol/server-memory` | 6 (OpenClaw, NanoClaw, Hermes, eliza, Reasönix, OpenHuman) | Knowledge graph |
| **fetch** | `@modelcontextprotocol/server-fetch` | 4 (OpenClaw, Hermes, Reasönix, PraisonAI) | Web retrieval |
| **puppeteer** | `@modelcontextprotocol/server-puppeteer` | 3 (PraisonAI, Reasönix, Phase 3 benchmark) | Browser automation |
| **time** | `@modelcontextprotocol/server-time` | 3 (Hermes, OpenHuman, Phase 3 benchmark) | Utilities |
| **postgres** | `@modelcontextprotocol/server-postgres` | 2 (PraisonAI, Phase 3 benchmark) | Database |
| **sqlite** | `@modelcontextprotocol/server-sqlite` | 2 (agent-zero, Reasönix) | Database |
| **brave-search** | `@modelcontextprotocol/server-brave-search` | 2 (PraisonAI, Phase 3 benchmark) | Web search |

**Key finding:** `filesystem` and `github` are the de facto standard MCP servers — referenced by nearly every platform with MCP support. A platform that doesn't support these two is likely not production-tested with real MCP servers.

#### Tier 2: Specialized MCP Servers (referenced by 1-2 platforms)

| Server | Package | Platform(s) | Category |
|--------|---------|-------------|----------|
| **git** | `@modelcontextprotocol/server-git` | Hermes, eliza | Developer tools |
| **sequential-thinking** | `@modelcontextprotocol/server-sequential-thinking` | PraisonAI | Reasoning |
| **gdrive** | `@modelcontextprotocol/server-gdrive` | PraisonAI | Cloud storage |
| **google-maps** | `@modelcontextprotocol/server-google-maps` | PraisonAI | Geo |
| **everart** | `@modelcontextprotocol/server-everart` | PraisonAI | Image generation |
| **redis** | `@modelcontextprotocol/server-redis` | PraisonAI | Database |
| **gitlab** | `@modelcontextprotocol/server-gitlab` | PraisonAI | Developer tools |
| **aws-kb-retrieval** | `@modelcontextprotocol/server-aws-kb-retrieval` | PraisonAI | AWS |
| **everything** | `@modelcontextprotocol/server-everything` | PraisonAI, Reasönix | Test/demo |
| **linear** | `@linear/mcp-server` | Hermes | Project management |
| **supabase** | `mcp-server-supabase` | NanoBot | Database |
| **gmail-autoauth** | custom | NanoClaw | Email |
| **google-calendar** | `@cocal/google-calendar-mcp` | NanoClaw | Calendar |

#### Tier 3: Custom / Platform-Specific MCP

| Pattern | Platform | Notes |
|---------|----------|-------|
| **mcporter** (GitHub MCP proxy) | HiClaw, OpenClaw | MCP server gateway proxied through Higress AI gateway. Workers never see real credentials |
| **bridge server** (GoClaw's own tools) | GoClaw | GoClaw exposes `read_file`, `exec`, `web_search`, `browser`, `cron`, `message` etc. as an MCP server via StreamableHTTP |
| **ring-zero MCP** (CLI harness) | OpenClaw | MCP as execution protocol for the agent's own operation loop |
| **mcp-github** (via Higress) | HiClaw | GitHub MCP server accessed through Higress MCP gateway with credential isolation |

### Server Adoption Patterns

**PraisonAI is the most MCP-server-diverse platform**, referencing 15 different official servers in its example/test code. This reflects its position as a framework that showcases MCP compatibility — it tests against more servers than any other platform.

**Reasönix is the most operationally complete**, with 7 servers referenced across test files that specifically test runtime behavior (stdio close, cache canonicalization, reconnect, TUI survival).

**HiClaw's mcporter pattern is unique** — MCP servers are accessed through an AI gateway proxy rather than directly. Workers use a skill to discover and call MCP tools, with all traffic routed through Higress. This means credentials never reach the agent container.

---

## Phase 5: Synthesis

### ROADMAP Research Questions Answered

#### Q1: What is the actual token overhead of MCP in production deployments?

**~73 tokens per MCP tool per turn.** At 10 servers (56 tools), that's 3,998 tokens injected into every API call — more than most system prompts.

With optimization:
- **No optimization:** 3,998 tokens (baseline)
- **Deferred loading (ZeroClaw):** 1,107 tokens (72.3% savings)
- **Search mode (GoClaw):** 183 tokens (95.4% savings)
- **Canonicalization (Reasönix):** 3,859 tokens (3.5% savings, but cache stability)

**Verdict:** MCP token overhead is significant but solvable. Platforms that don't implement deferred loading or search will become prohibitively expensive at scale. The technology to solve this already exists — it just needs wider adoption.

#### Q2: Which MCP servers are most widely adopted?

**Tier 1 (universal):** filesystem (11 platforms), github (9 platforms), memory (6 platforms), fetch (4 platforms).

These four servers are the de facto standard. Any MCP-compatible platform should be tested against at minimum filesystem and github. The official `@modelcontextprotocol/servers` repository is the canonical source.

#### Q3: How do MCP-native frameworks differ from MCP-adapter approaches?

| Dimension | Native (ZeroClaw) | First-class (Hermes, GoClaw) | Adapter (NanoClaw, agent-zero) |
|-----------|-------------------|------------------------------|--------------------------------|
| **Integration depth** | MCP tools = native tools (same trait) | MCP subsystem alongside native tools | MCP bridge wrapping external servers |
| **Tool discovery** | Deferred + `tool_search` | Eager or threshold-based | Eager |
| **Transport** | All 3 (stdio/SSE/HTTP) | All 3 | Typically stdio only |
| **Security** | Built into tool execution | OAuth, per-tool gating, env filtering | Minimal |
| **Lifecycle** | Stale session detection, auto-reconnect | Pool management, session reset | Basic |

**Native vs adapter is not just an implementation detail — it shapes the entire user experience.** ZeroClaw's native approach enables lazy loading and seamless integration. Adapter approaches inherit the limitations of the bridge pattern (eager loading, no per-tool control, limited transport support).

#### Q4: What is the rate of MCP adoption across tracked platforms?

**70% adoption** (21 of 30 locally-assessable platforms). Breakdown:
- 1 Native (ZeroClaw)
- 8 First-class (Hermes, OpenClaw, GoClaw, NanoBot, Reasönix, AgentScope, OpenHuman, eliza)
- 8 Adapter (NanoClaw, IronClaw, MaxClaw, HiClaw, PraisonAI, agent-zero, rocketride-server, ClawTeam)
- 4 Resistant (Claw-AI-Lab, Aider, Copilot-CLI, eliza core)
- 9 Not assessable (external frameworks not cloned)

MCP has crossed the chasm. The question is no longer "should we adopt MCP?" but "how should we optimize MCP?"

---

### The Three MCP Innovation Frontiers

The research reveals three distinct innovation frontiers, each solved by a different platform:

**Frontier 1: Token Scalability**
- Problem: MCP schemas grow linearly, becoming prohibitively expensive
- Solved by: ZeroClaw (deferred stubs) and GoClaw (BM25 search mode)
- Remaining gap: No platform combines deferred loading with BM25 search

**Frontier 2: Cache Stability**
- Problem: MCP server restarts/reordering invalidate prompt caches
- Solved by: Reasönix (schema canonicalization)
- Remaining gap: Only Reasönix implements this. Every other platform is vulnerable.

**Frontier 3: Enterprise Security**
- Problem: Multi-tenant MCP authorization and authenticated servers
- Solved by: GoClaw (per-tenant grants + allow/deny filter) and Hermes (OAuth + sampling control)
- Remaining gap: No platform combines both GoClaw's grant system with Hermes' OAuth flow

### Recommendations

**For platform developers:**
1. Implement deferred loading before supporting more than 5 MCP servers. The token cost of eager loading at scale is unsustainable.
2. Canonicalize MCP tool schemas before injecting into LLM context. The 3% token overhead is negligible; the cache stability benefit is enormous.
3. For enterprise deployments, implement per-tenant tool filtering. GoClaw's allow/deny pattern is the reference.

**For users:**
1. Start with filesystem and github servers — they're the most tested.
2. Prefer platforms with deferred loading (ZeroClaw) or search mode (GoClaw) if you plan to use many MCP servers.
3. On Anthropic models, prefer Reasönix or manually canonicalize your MCP config — cache invalidation is the hidden cost.

**For the MCP protocol team:**
1. The canonical ordering problem is real. Consider mandating alphabetical key ordering in the MCP spec to make Reasönix's canonicalization unnecessary.
2. A standardized `tool_search` protocol method would help — currently each platform implements its own search.
3. The `sampling/createMessage` pattern (Hermes) should be promoted — it makes MCP servers active participants, not just passive tool providers.

### The Ideal MCP Implementation (Does Not Exist Yet)

| Capability | Best Implementation | Status |
|-----------|---------------------|--------|
| Deferred tool loading | ZeroClaw (`mcp_deferred.rs`) | ✅ Ships |
| BM25 tool search | GoClaw (`mcp_tool_search.go`) | ✅ Ships |
| Schema canonicalization | Reasönix (`canonicalizeSchemaForCache`) | ✅ Ships |
| Per-tenant authorization | GoClaw (`grant_checker.go`) | ✅ Ships |
| OAuth for authenticated servers | Hermes (`mcp_oauth.py`) | ✅ Ships |
| Sampling with controls | Hermes (config schema) | ✅ Ships |
| Stale session detection | ZeroClaw (`McpTransportError`) | ✅ Ships |
| Bridge server (dual role) | GoClaw (`bridge_server.go`) | ✅ Ships |
| OSV malware preflight | Hermes (stdio startup) | ✅ Ships |
| **ALL OF THE ABOVE** | — | ❌ No platform |

Every key MCP innovation exists in production today — but no single platform has adopted them all. The platform that combines ZeroClaw's deferred loading + GoClaw's BM25 search + Reasönix's canonicalization + Hermes' OAuth/sampling will have a decisive architectural advantage.

---

### MCP vs Alternative Tool Systems

The research also reveals three alternative approaches to tool extensibility that compete with MCP:

| Alternative | Platform | Trade-off vs MCP |
|-------------|----------|------------------|
| **Plugin SDK** | OpenClaw (plugin-sdk), eliza (146 plugins) | Tighter integration, no token overhead, but no interoperability |
| **WASM plugins** | IronClaw, ZeroClaw | Sandboxed execution, language-agnostic, but no standard tool protocol |
| **Skills (Markdown)** | Hermes, ZeroClaw, PraisonAI | Zero token overhead (loaded on demand), but no executable capability |

MCP's unique value is **interoperability** — the same MCP server works across every MCP-compatible platform. Plugin SDKs and WASM are platform-specific. Skills are portable but non-executable. MCP is the only pattern that gives both executability and cross-platform compatibility.

The trade-off: MCP's token overhead (even optimized) is always higher than zero. Platforms optimizing for minimal footprint (ZeroClaw's <5MB target) will continue to treat MCP as optional, not default.

---

## Research Summary

| Phase | Finding |
|-------|---------|
| **1. Adoption Survey** | 70% of platforms support MCP (21/30). ZeroClaw is the only truly native implementation. |
| **2. Architecture Comparison** | Four platforms solved four different problems. No platform combines all innovations. |
| **3. Token Overhead** | ~73 tokens/tool baseline. GoClaw search mode achieves 95.4% savings. Deferred loading is not optional at scale. |
| **4. Server Catalog** | filesystem + github are universal (referenced by 9-11 platforms). PraisonAI tests against 15 different servers. |
| **5. Synthesis** | MCP has crossed the chasm. The innovation frontier has shifted from "should we adopt?" to "how do we optimize?" |

---

*This report completes the MCP Ecosystem Deep-Dive (Phases 1-5) planned in `docs/reports/mcp-deep-dive-research-plan.md`.*

*Phase reports:*
- *[Phase 1: Adoption Survey](mcp-deep-dive-phase1-adoption-survey.md)*
- *[Phase 2: Architecture Comparison](mcp-deep-dive-phase2-architecture-comparison.md)*
- *[Phase 3: Token Overhead Analysis](mcp-deep-dive-phase3-token-overhead.md)*
- *Phase 4-5: Server Catalog & Synthesis (this document)*
