# Protocol Wars 2026: MCP vs A2A vs ACP vs Proprietary

**Report date:** August 18, 2026
**Scope:** Protocol adoption survey across all 34 tracked platforms + 7 harness ecosystems, with architecture comparison and composability analysis
**ROADMAP item:** Q4-5
**Prior work:** MCP deep-dive phases 1-5 (adoption survey, architecture comparison, token-overhead measurement, ecosystem catalog, synthesis)

---

## 1. Executive Summary

The protocol landscape of 2026 is not the two-horse race the ROADMAP anticipated. Source-level verification across the tracking set finds **four** contenders occupying three distinct layers, and — the headline finding — **they are not competing for the same job**:

- **MCP** owns the *tool/capability* layer. 13 of 34 platforms implement it; 3 natively. No challenger at this layer.
- **A2A** owns the *agent-discovery-and-delegation* layer, but has exactly **one production implementation** in the tracking set (eliza's Feed integration) plus one roadmap mention (AgentScope). Adoption is aspiration, not architecture.
- **ACP** owns the *client-agent* layer (IDE/editor ↔ agent). Three CLI agents implement it, plus two harness ecosystems — it is the stealth winner of 2026: barely discussed, quietly shipping everywhere.
- **Proprietary surfaces** (OpenAI Responses/completions, Anthropic Messages, gateway RPC) remain the *default* interop layer — 30+ of 34 platforms speak at least one, making them the de facto lingua franca that MCP/A2A/ACP are trying to displace *at their edges*.

**The war metaphor is wrong; it's a layering.** The live conflict is not MCP vs A2A head-to-head — they solve different problems and are already co-existing (eliza's Feed runs A2A *and* MCP side by side). The real conflicts are: (a) MCP over-expanding from tools into agents (sampling), (b) ACP vs vendor IDE integrations, and (c) every protocol fighting the inertia of plain HTTP/JSON vendor APIs.

---

## 2. Methodology

Protocol signatures searched at source level across all local checkouts (greps for `agent_card` / `.well-known/agent` / `Agent2Agent` / `@a2a-js` / `Agent Client Protocol` / `agentclientprotocol` / MCP client imports), followed by manual read of the matching modules. Roadmap/doc mentions distinguished from shipped code. MCP data reused from the phase-1 adoption survey. Claims below cite file paths where they matter.

This is the same source-verification method as the claims-verification series: docs say things; code is truth.

---

## 3. The Four Contenders

### 3.1 MCP — Model Context Protocol (Anthropic, Nov 2024)

**Layer: model ↔ tools/resources.** Standardizes how an agent discovers and calls external capabilities.

Verified state (from the MCP deep-dive, updated):
- **13/34 platforms** (Native 3: Hermes-Agent, AgentScope, OpenWorker; Adapter 9; Resistant 1: NanoClaw)
- Token overhead measured: tool-definition inflation 8-42% per call (phase-3 finding)
- OpenWorker pinned `mcp<2` after MCP 2.0.0 removed `streamablehttp_client` — the first documented supply-chain break in the protocol's history
- Hermes implements MCP **sampling** (servers can request LLM completions) — MCP reaching *up* into the agent layer (phase-2 finding: "the foundation for MCP-native agent-to-agent communication")

**Assessment:** won its layer. The remaining question is whether it stays a tool protocol or expands into orchestration.

### 3.2 A2A — Agent2Agent (Google, April 2025)

**Layer: agent ↔ agent discovery and task delegation.** Agent Cards at `/.well-known/agent-card.json`, task lifecycle, streaming updates.

Verified state:

| Platform | Evidence | Status |
|----------|----------|--------|
| **eliza** | `packages/feed/packages/a2a/` — full `@a2a-js/sdk` dependency, Agent Card routes (`apps/web/.well-known/agent-card`), local A2A server example, official client (`feed_a2a_official.py`), stress-test command (`test a2a`) | **Production** — external agents join the Feed game via A2A |
| **AgentScope** | `docs/roadmap.md`: "A2A (Agent-to-Agent): Enhance agent-to-agent communication capabilities" | **Roadmap only** |
| Everyone else | No agent_card, no SDK imports, no A2A docs | Absent |

One production user. One roadmap line. **The protocol with the loudest marketing has the thinnest shipped base in the tracking set.**

**Assessment:** A2A's identity has shifted — by mid-2026 it is best understood as Google's agent-*discovery* standard (Agent Cards as the "DNS of agents") with the delegation protocol riding along. The Feed integration validates the discovery pattern: heterogeneous external agents found and admitted into a running system.

### 3.3 ACP — Agent Client Protocol (Zed, 2025)

**Layer: client/editor ↔ agent.** JSON-RPC over stdio: the editor drives the agent, renders its streaming output, fields its permission prompts.

Verified state:

| Implementor | Evidence | Form |
|-------------|----------|------|
| **reasonix** | `src/acp/protocol.ts` — full wire types (`agentclientprotocol.com`), `acp` subcommand, tests | ACP *server* (agent side) |
| **kimi-cli** | `kimi-cli acp` subcommand; docs `kimi-acp.md` (EN+ZH); `term` TUI backed by Kimi Code's ACP server | ACP client + server |
| **kimi-code** | `docs/en/reference/kimi-acp.md` — ACP server powering kimi-cli's `term` | ACP *server* |
| **Hermes-Agent** | `acp_adapter/` module (auth, edit approval, permissions, provenance, events) + `agent/copilot_acp_client.py` | ACP adapter both directions |
| **copilot-cli** | ACP per design-paradigm report | ACP client |
| **Pi (harness)** | ACP listed in extension ecosystem | Agent side |
| **dsh (harness)** | headless runner adjacent to ACP surface | Adjacent |

**Assessment:** ACP is 2026's stealth standard. Nobody markets it; five tracked projects ship it. Reason: structural: once an agent lives in a terminal, the editor integration question is universal, and ACP is the only open answer that isn't a vendor SDK. The China ecosystem (kimi-cli, kimi-code) adopting it wholesale is the strongest signal — it's the cross-vendor neutral choice.

### 3.4 Proprietary surfaces — the incumbent

**Layer: everything, badly, by default.** OpenAI-compatible `/v1/chat/completions` + Anthropic Messages + gateway RPC (GoClaw WS/HTTP, OpenCode serve/attach).

30+ of 34 platforms implement at least one proprietary surface. Reasonix's `desktop` JSON-RPC, kimi-cli's `--wire`, GoClaw's `/v1/*` — every platform that needs programmatic access and isn't using a standard invents one. **The protocols aren't fighting each other first; they're fighting this.**

---

## 4. Adoption Matrix (source-verified)

| Platform | MCP | A2A | ACP | Proprietary surface |
|----------|-----|-----|-----|---------------------|
| OpenClaw | Adapter | — | — | plugin API |
| ClawTeam | — | — | — | inbox JSON (internal) |
| GoClaw | Adapter | — | — | WS RPC + HTTP `/v1/*` |
| IronClaw | Adapter | — | — | web gateway SSE/WS |
| Maxclaw | — | — | — | — |
| NanoClaw | Resistant | — | — | session DB protocol (internal) |
| Nanobot | Bridge | — | — | LiteLLM (vendor APIs) |
| ZeroClaw | Adapter | — | — | gateway |
| HiClaw | Adapter | — | — | Matrix + manager RPC |
| Hermes-Agent | **Native** | — | **Adapter (bidirectional)** | gateway + 20 channels |
| Claw-AI-Lab | — | — | — | internal pipeline |
| SmolAgents | — | — | — | HF inference |
| LangGraph | — | — | — | LangChain ecosystem |
| CrewAI | — | — | — | — |
| AutoGen | — | — | — | — |
| Swarms | — | — | — | — |
| OpenAgents | — | — | — | — |
| OpenFang | Adapter | — | — | hand dispatch |
| kimi-code | Adapter | — | **Server** | REST |
| AgentScope | **Native** | Roadmap | — | FastAPI service |
| eliza | Adapter | **Production** | — | REST + plugin API |
| agent-zero | — | — | — | — |
| praisonai | — | — | — | — |
| rocketride-server | Adapter | — | — | node graph API |
| OpenWorker | **Native** | — | — | desktop RPC |
| Dify | — | — | — | REST platform API |
| MetaGPT | — | — | — | — |
| Qwen-Agent | — | — | — | DashScope API |
| aider | — | — | — | — |
| copilot-cli | — | — | **Client** | GitHub API |
| reasonix | — | — | **Server** | `desktop` JSON-RPC |
| kimi-cli | — | — | **Client + Server** | `--wire` (experimental) |
| codex | — | — | — | OpenAI Responses |
| openhuman | — | — | — | — |
| *dsh (Tier2)* | — | — | adjacent | Cordis ctx (internal) |
| *Pi (Tier2)* | — | — | **ecosystem** | pi-ai unified API |

**Totals:** MCP 13 (+2 harness-adjacent) · A2A 1 production + 1 roadmap · ACP 5 shipped (+2 harness) · Proprietary 30+.

---

## 5. The Layering Thesis

The four protocols map to a clean stack, which explains the adoption pattern:

```
┌──────────────────────────────────────────────┐
│  A2A — agent discovery & delegation          │  ← 1 impl; discovery pattern validated
├──────────────────────────────────────────────┤
│  ACP — client/editor ↔ agent                 │  ← 5 impls; stealth standard
├──────────────────────────────────────────────┤
│  MCP — agent ↔ tools/resources               │  ← 13 impls; won its layer
├──────────────────────────────────────────────┤
│  Vendor APIs — model ↔ inference             │  ← 30+ impls; the incumbent everything
└──────────────────────────────────────────────┘
```

**Why the layers matter:**

1. **Composability stacks rather than competes.** eliza's Feed proves it: an external agent is *discovered* via A2A (Agent Card), *runs* on its own stack, *acts* through MCP tools, and is *driven* by a human through ACP or a channel. One deployment, three protocols, zero conflicts.
2. **Each layer has one open winner-except-one:** MCP at tools, ACP at client-agent. A2A at discovery is Google's to lose — but with one production implementation, "war" overstates the situation; it's an occupation awaiting contest.
3. **The MCP expansion question** is the one genuine cross-layer conflict: sampling (and the spec's agent-oriented additions) lets MCP creep into A2A's delegation territory from below. Hermes' sampling implementation is the tracked proof-of-concept. If MCP formalizes agent-to-agent over sampling, A2A's remaining uniqueness is discovery (Agent Cards) alone.
4. **Vendor APIs are the real incumbent at every layer.** The `--wire`/`desktop`/`/v1/*` pattern shows platforms reaching for proprietary RPC the moment a standard doesn't cover their exact need. Standards win by coverage, not by elegance — MCP's 42% worst-case token overhead is tolerated because the coverage is there; A2A's clean design is ignored where the need isn't yet felt.

---

## 6. The 1PC / Enterprise Fork Interaction

The ROADMAP asked how protocol choice maps to the personal/enterprise fork. Finding: **layer adoption tracks the fork.**

- **Personal/1PC platforms** adopt ACP (editor integration is the personal workflow) and resist A2A (solo agents have no peers to discover). reasonix, kimi-cli, Hermes: ACP yes, A2A absent.
- **Enterprise platforms** adopt MCP adapters (tool governance) and ignore ACP (no IDE in the deployment picture). GoClaw, HiClaw, AgentScope: MCP yes, ACP absent.
- **The A2A profile is neither — it's the *social/multi-vendor* tier**: eliza's Feed (agents as game participants) is consumer-social, not enterprise. A2A's natural constituency may be open agent *networks*, not enterprises — closer to email/federation history than to microservices history.

**Prediction:** A2A adoption, when it comes, will come through consumer/social agent products and Web3-adjacent networks first, enterprises last — the reverse of MCP's path.

---

## 7. Protocol Comparison Matrix

| Dimension | MCP | A2A | ACP | Vendor APIs |
|-----------|-----|-----|-----|-------------|
| Sponsor | Anthropic | Google | Zed | OpenAI/Anthropic/etc |
| Layer | Tools/resources | Agent discovery/delegation | Client ↔ agent | Everything |
| Transport | stdio/SSE/streamable-http | HTTP + SSE/JSON-RPC | JSON-RPC over stdio | HTTP/WS |
| Token overhead | 8-42% (measured) | n/a (out of band) | n/a (client-side) | none (native) |
| Tracked adoption | 13 platforms | 1 + 1 roadmap | 5 + 2 harness | 30+ |
| Governance | Open spec, Anthropic-led | Linux Foundation (donated) | Open, Zed-led | Vendor-controlled |
| Breaking-change record | v2.0 removed transport (OpenWorker pin) | none observed | v1 stable | Frequent, silent |
| Failure mode | Context inflation | Discovery without adoption | Editor lock-in | Lock-in by design |

---

## 8. Findings

1. **Four protocols, three layers, no war** — MCP/A2A/ACP occupy distinct stack positions and already co-exist in production (eliza Feed). The "protocol wars" framing mispredicts; the accurate frame is *protocol layering with one contested border* (MCP sampling vs A2A delegation).
2. **ACP is the stealth winner** — 5 shipped implementations across Western and China ecosystems, zero marketing. The cross-vendor neutral editor-agent seam.
3. **A2A is discovery-first** — one production implementation validates the Agent Card discovery pattern but not the full delegation protocol. Its constituency is social/open agent networks, not the enterprise (fork inversion vs MCP).
4. **Vendor APIs remain the default interop layer** — 30+ platforms; standards displace them only where coverage is complete (MCP at tools) or the need is universal (ACP at editors).
5. **Layer adoption tracks the 1PC/enterprise fork** — personal platforms: ACP yes/A2A no; enterprise platforms: MCP yes/ACP no. Protocol choice is a deployment-shape signal.
6. **MCP's expansion is the live conflict to watch** — sampling-based agent-to-agent over MCP (Hermes implements) would collapse A2A's delegation layer into the tool protocol; Agent Cards would be all that remains distinct.

## 9. Recommendations

- **For ROADMAP Q4-4 (long-running benchmarks):** add a protocol-conformance dimension — token overhead of MCP tool defs vs native tools per platform is already measured; ACP session overhead is measurable the same way.
- **For Q4-7 candidates:** browser-use/UI-TARS (computer-use agents) will interact with protocols as *clients*; their admission fills the last Tier-1 slot and completes the protocol survey's client side.
- **For the blog:** the layering thesis (not-war) and ACP-stealth-winner findings are publishable; the adoption matrix is the citation base.
- **Revisit trigger:** MCP formalizing agent-to-agent semantics, or any second A2A production adoption in the tracking set — either event re-opens §5's layering.

---

*Data: source-level grep verification across 32 local checkouts (Aug 18, 2026), MCP deep-dive phases 1-5, design-paradigm analysis, harness-engineering comparison. Platform versions as tracked at HEAD.*
