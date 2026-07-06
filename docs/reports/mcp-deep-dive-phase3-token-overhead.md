# MCP Ecosystem Deep-Dive: Phase 3 — Token Overhead Analysis

**Date:** 2026-07-06
**Method:** Static reconstruction — build representative MCP payloads from 10 official servers, transform through each platform's processing logic, count tokens with cl100k_base
**Measurement script:** `docs/reports/mcp_phase3_measure.py`

---

## Executive Summary

The numbers are definitive. Deferred tool loading is not a marginal optimization — it is the difference between affordable and unaffordable MCP at scale.

**Key finding: GoClaw's search mode reduces token overhead by 95.4% at 10 servers.** The agent sees a single search tool (183 tokens) regardless of how many MCP servers are configured. ZeroClaw's deferred mode achieves 72.3% savings while keeping tool stubs visible.

---

## Methodology

### Representative MCP Servers

10 official `@modelcontextprotocol/servers` with 56 total tools:

| Server | Tools | Typical Use |
|--------|-------|-------------|
| filesystem | 8 | File read/write/edit/search |
| github | 11 | Issues, PRs, branches, commits |
| postgres | 7 | SQL query, schema inspection |
| brave-search | 3 | Web search, URL fetch |
| slack | 8 | Messages, channels, files |
| sqlite | 4 | Lightweight SQL |
| memory | 5 | Knowledge graph entities/relations |
| fetch | 1 | URL content fetch |
| puppeteer | 7 | Browser automation |
| time | 2 | Timezone queries |

### Measurement Process

For each platform, at each N value (0, 1, 3, 5, 10 servers):
1. Select the first N servers from the set
2. Build the tool definitions payload as the platform would produce it
3. Serialize to JSON
4. Count tokens with `tiktoken` cl100k_base encoding (GPT-4/Claude-family approximation)

### Limitations

- **Static reconstruction** — does not capture runtime overhead (connection, handshake, error messages)
- **cl100k_base approximation** — actual token counts vary by model; Claude uses a different tokenizer. Relative comparisons between platforms remain valid.
- **Representative schemas** — actual MCP servers may have more or fewer properties per tool. The 56-tool set is calibrated to match real-world server complexity.
- **Cache stability not measured in tokens** — Reasönix's canonicalization saves tokens indirectly through cache hits, which requires live API calls to measure.

---

## Results

### Token Count Matrix

| Platform | N=0 | N=1 | N=3 | N=5 | N=10 |
|----------|-----|-----|-----|-----|------|
| **Hermes** (baseline) | 1 | 560 | 2,034 | 2,821 | 3,998 |
| **ZeroClaw** (eager) | 1 | 560 | 2,034 | 2,821 | 3,998 |
| **ZeroClaw** (deferred) | 110 | 271 | 581 | 775 | 1,107 |
| **GoClaw** (eager) | 1 | 560 | 2,034 | 2,821 | 3,998 |
| **GoClaw** (search mode) | 183 | 183 | 183 | 183 | 183 |
| **Reasönix** (raw) | 1 | 560 | 2,034 | 2,821 | 3,998 |
| **Reasönix** (canonicalized) | 1 | 544 | 1,979 | 2,735 | 3,859 |

### Per-Tool Token Cost (baseline)

| N servers | Tools | Total tokens | Tokens/tool |
|-----------|-------|-------------|-------------|
| 1 | 8 | 560 | 70 |
| 3 | 26 | 2,034 | 78 |
| 5 | 37 | 2,821 | 76 |
| 10 | 56 | 3,998 | 71 |

Average: **~73 tokens per MCP tool** in the eager (baseline) approach.

---

## Analysis

### 1. ZeroClaw Deferred Loading — 72% Savings

| N servers | Eager | Deferred | Saved | Reduction |
|-----------|-------|----------|-------|-----------|
| 1 | 560 | 271 | 289 | 51.6% |
| 3 | 2,034 | 581 | 1,453 | 71.4% |
| 5 | 2,821 | 775 | 2,046 | 72.5% |
| 10 | 3,998 | 1,107 | 2,891 | 72.3% |

ZeroClaw's deferred loading consistently saves ~72% at scale. The LLM sees lightweight stubs (name + description only) plus a `tool_search` tool. The stubs still grow linearly with tool count, but at a much lower rate (~15 tokens/stub vs ~73 tokens/full-schema).

**Trade-off:** The LLM must call `tool_search` before using any MCP tool, adding one round-trip. In a 10-turn conversation where the LLM uses 3 MCP tools, this adds 3 search calls. The token cost of those calls (~150 tokens each) is still far less than carrying 56 full schemas in every turn.

### 2. GoClaw Search Mode — 95% Savings, Constant Cost

| N servers | Eager | Search mode | Saved | Reduction |
|-----------|-------|-------------|-------|-----------|
| 1 | 560 | 183 | 377 | 67.3% |
| 3 | 2,034 | 183 | 1,851 | 91.0% |
| 5 | 2,821 | 183 | 2,638 | 93.5% |
| 10 | 3,998 | 183 | 3,815 | 95.4% |

GoClaw's search mode is the most aggressive optimization: **constant 183 tokens regardless of server count.** The agent sees only the `mcp_tool_search` tool definition. Individual tool schemas are never in the context until the LLM explicitly searches for them.

**Trade-off:** More friction than ZeroClaw. The LLM has zero visibility into what MCP tools exist — it must guess keywords. ZeroClaw's stubs at least show tool names and descriptions, giving the LLM hints about what's available. GoClaw's tool description compensates with strong guidance: "Before performing any external service operation, you MUST search here first."

**When GoClaw activates:** This mode triggers only when the total MCP tool count exceeds an inline threshold. Below the threshold, GoClaw behaves like the eager baseline.

### 3. Reasönix Canonicalization — 3% Token Reduction + Cache Stability

| N servers | Raw | Canonicalized | Difference |
|-----------|-----|---------------|------------|
| 1 | 560 | 544 | -16 (2.9%) |
| 3 | 2,034 | 1,979 | -55 (2.7%) |
| 5 | 2,821 | 2,735 | -86 (3.0%) |
| 10 | 3,998 | 3,859 | -139 (3.5%) |

Canonicalization slightly reduces token count (~3%) because alphabetically sorted keys produce shorter JSON (common prefixes cluster together in tokenization). But the real value isn't in the 3% token reduction — **it's in prompt cache stability.**

**The hidden cost of uncanonicalized schemas:** When an MCP server restarts and returns tools in a different order, the prompt cache prefix changes. On Anthropic's API with a 100K-token conversation:
- Cache miss: full reprocessing of ~100K tokens
- Cache hit: ~10% cost of the cached portion
- One cache invalidation from MCP reordering: ~$0.30-$0.50 per occurrence (at Claude Sonnet pricing)

Canonicalization prevents this entirely. Over a long conversation with multiple MCP server restarts, the cache savings dwarf the 3% token reduction.

### 4. Growth Rate Comparison (N=1 → N=10)

| Platform | N=1 | N=10 | Growth |
|----------|-----|------|--------|
| Hermes (baseline) | 560 | 3,998 | 7.1x |
| ZeroClaw (eager) | 560 | 3,998 | 7.1x |
| ZeroClaw (deferred) | 271 | 1,107 | 4.1x |
| GoClaw (eager) | 560 | 3,998 | 7.1x |
| GoClaw (search mode) | 183 | 183 | 1.0x |
| Reasönix (raw) | 560 | 3,998 | 7.1x |
| Reasönix (canonicalized) | 544 | 3,859 | 7.1x |

**GoClaw search mode is the only approach with O(1) growth.** Every other approach (including ZeroClaw's deferred loading) grows linearly with server count. At 50+ servers, GoClaw's advantage becomes enormous — 183 tokens vs ~20,000 tokens for the baseline.

---

## The Combined Approach

No platform implements all optimizations. The theoretical ideal:

| Layer | Source | Token Impact |
|-------|--------|-------------|
| Deferred loading | ZeroClaw | -72% at scale |
| Search-based discovery | GoClaw | -95% at scale |
| Schema canonicalization | Reasönix | -3% tokens + cache stability |
| Per-tool gating | Hermes | User-controlled reduction |
| OAuth + sampling control | Hermes | No token change; enables authenticated servers |

If GoClaw's search mode (183 tokens constant) were combined with Reasönix's canonicalization (cache stability), an agent could run 50 MCP servers with less token overhead than 1 unoptimized server — and never invalidate the prompt cache.

---

## Cost Projection

At Claude Sonnet pricing ($3/M input, $15/M output), in a 20-turn conversation:

| Platform approach | MCP tokens/turn | 20-turn MCP cost | vs Baseline |
|-------------------|----------------|-----------------|-------------|
| Hermes (baseline) | 3,998 | $0.24 | — |
| ZeroClaw (deferred) | 1,107 | $0.07 | -71% |
| GoClaw (search) | 183 | $0.01 | -95% |
| Reasönix (canonicalized) | 3,859 | $0.23 | -3% (+ cache savings) |

Note: These are MCP-schema-only costs. Total conversation cost includes system prompt, user messages, tool results, and model output. MCP schema overhead is additive to all of these, every turn.

---

## Conclusions

1. **Deferred loading is not optional for MCP at scale.** At 10 servers (56 tools), the baseline costs 3,998 tokens/turn. ZeroClaw's deferred approach cuts this to 1,107. GoClaw's search approach cuts it to 183. Platforms that load all schemas eagerly will become prohibitively expensive as MCP ecosystems grow.

2. **GoClaw's O(1) search mode is the most scalable pattern.** Constant 183 tokens regardless of server count. The trade-off (zero tool visibility without explicit search) is acceptable for enterprise deployments where the agent's task is well-defined.

3. **ZeroClaw's deferred stubs are the best balance.** Tool names and descriptions remain visible (helping the LLM discover tools naturally), while full schemas are loaded on demand. 72% savings with less friction than GoClaw's blind search.

4. **Reasönix's canonicalization is the cheapest insurance.** 3% token reduction is marginal, but preventing cache invalidation in long conversations can save orders of magnitude more than any token reduction. Every platform should canonicalize.

5. **The ~73 tokens/tool baseline is the universal constant.** Any platform using eager loading pays ~73 tokens per MCP tool per turn. This is the number that should drive adoption of deferred/search patterns.

---

*Measurement script: `docs/reports/mcp_phase3_measure.py`*
*Phase 4 (Server Ecosystem Catalog) and Phase 5 (Synthesis) will follow.*
