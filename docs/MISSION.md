# AllClaws Research Mission

**[中文](MISSION.zh-CN.md)** | English

---

## Mission Statement

AllClaws conducts independent research on AI agent architectures and deployment models, with emphasis on understanding the emerging distinction between **personal-force-multiplier** and **enterprise-automation** paradigms. We track 20 platforms across both claw ecosystem and external frameworks to provide objective analysis of real capabilities versus marketing claims.

---

## Vision

A world where AI agent platforms are understood by their actual capabilities, not marketing claims. Where developers can choose between personal-force-multiplier and enterprise-automation paradigms with clear eyes about trade-offs. Where the community has honest analysis of what these systems can and cannot do.

---

## What We Do

### Core Activities

1. **Architecture Analysis** — Deep-dive technical analysis of AI agent platforms, documenting design decisions, trade-offs, and implementation patterns.

2. **Benchmarking** — Systematic comparison of functionality, performance, and security across platforms through automated testing frameworks.

3. **Ecosystem Tracking** — Monthly updates on platform developments, emerging trends, and cross-platform innovations.

4. **Claims Verification** — Independent verification of marketing claims against source code and actual implementation.

### Scope

**20 Platforms Tracked:**
- **Claw Ecosystem (13):** OpenClaw, ClawTeam, GoClaw, IronClaw, Maxclaw, NanoClaw, Nanobot, ZeroClaw, HiClaw, QuantumClaw, Hermes-Agent, RTL-CLAW, Claw-AI-Lab
- **External Frameworks (7):** SmolAgents, LangGraph, mcp-agent, CrewAI, AutoGen, Swarms, OpenAgents

**What We Cover:**
- Architecture and design patterns
- Security and safety mechanisms
- Performance and resource usage
- Multi-agent coordination approaches
- Memory and context management
- Tool/capability integration

**What We Don't Cover:**
- Endorsements or recommendations
- Commercial partnerships
- Vendor-specific training
- Non-technical comparisons (pricing tiers, support plans)

---

## Position Statements

### On Platform Coverage

We track both claw-ecosystem platforms (13) and significant external frameworks (7) to provide comprehensive ecosystem coverage. Our focus is on understanding architectural patterns, not promoting any specific implementation.

**Rationale:** The distinction between "claw" and "external" is historical, not qualitative. External frameworks like LangGraph and CrewAI represent industry standards that must be understood for complete ecosystem analysis.

### On External Frameworks

LangGraph, CrewAI, AutoGen, SmolAgents, Swarms, OpenAgents, and mcp-agent represent industry standards and reference implementations. We analyze them to understand broader ecosystem patterns and compare against claw ecosystem innovations.

**Rationale:** Tracking only claw-ecosystem platforms would create blind spots. External frameworks often pioneer patterns (MCP-native, graph orchestration) that later influence or compete with claw platforms.

### On MCP Protocol

MCP represents a fork in the road: standardization vs local control. We track both approaches (mcp-agent, IronClaw, GoClaw, ZeroClaw adopt MCP; NanoClaw, local-first agents resist) without advocating for either.

**Our Analysis:**
- **MCP adoption** is gaining in enterprise/cloud contexts where interoperability matters
- **MCP resistance** persists in local-first agents where CLI tools and direct execution are preferred
- **Token overhead** (20-30% from MCP metadata) remains a concern for resource-constrained deployments

### On "Self-Improving" Claims

We verify marketing claims against actual implementations. "Context management" is not "autonomous learning"—we make these distinctions clear through source code analysis.

**Example:** Hermes-Agent claims "self-improving AI agent with built-in learning loop." Our analysis found:
- ✅ Skill curation and nudges exist
- ✅ Cross-session memory works
- ❌ No autonomous skill improvement
- ❌ No RL-based learning

**Position:** We distinguish between "procedural memory" (saved workflows) and "autonomous learning" (performance improvement from experience).

### On Personal vs Enterprise

We believe the fork between personal-force-multiplier (1PC) and enterprise-automation agents is the most important trend in 2026. Allclaws exists to document and analyze this divergence.

**Personal-Force-Multiplier Pattern:**
- Single user or small team
- Direct tool/CLI access
- Local data preference
- Minimal governance overhead
- Examples: OpenClaw, Nanobot, SmolAgents

**Enterprise-Automation Pattern:**
- Multi-user environments
- Protocol-based tool access (MCP)
- Cloud-deployed infrastructure
- Governance and compliance focus
- Examples: LangGraph, Swarms, HiClaw, GoClaw

---

## Research Principles

### Independence

We maintain independence from all tracked platforms. No platform receives preferential treatment in our analysis. Claims are verified against source code and observable behavior, not marketing materials.

### Evidence-Based

All conclusions are backed by:
- Source code analysis
- Test framework results
- Git commit histories
- Official documentation
- Reproducible benchmarks

### Transparency

Our methodologies, testing frameworks, and analysis processes are open source. Readers can verify our conclusions and contribute improvements.

---

## What Makes AllClaws Unique

### 1. Fork Analysis

We explicitly track the personal vs enterprise fork in AI agent development. Most research covers one or the other; we cover both and their interactions.

### 2. Claims Verification

We don't repeat marketing claims. We verify them against implementation and call out overstated features (e.g., "self-improving" without autonomous learning).

### 3. Source-Code Deep Dives

Our architecture analysis comes from reading actual source code, not README files. This reveals real trade-offs that documentation glosses over.

### 4. Comprehensive Coverage

20 platforms across both specialized claw ecosystem and major external frameworks provides unparalleled ecosystem visibility.

---

## Success Metrics

We measure success by:

1. **Accuracy** — Our analysis correctly predicts platform capabilities and limitations
2. **Independence** — No perceived or actual bias toward any platform
3. **Impact** — Developers make better platform choices based on our research
4. **Transparency** — Our methods are reproducible and our data is verifiable

---

## Non-Goals

To maintain focus, AllClaws explicitly does **not**:

1. **Rate platforms** — No "best platform" rankings
2. **Provide tutorials** — Other sources cover how-to guides
3. **Offer consulting** — We research, we don't advise deployments
4. **Predict markets** — We analyze technology, not investment potential

---

## Contact

AllClaws is an independent research project. For discussions, questions, or collaboration opportunities, please refer to the GitHub repository: [github.com/dz3ai/allclaws](https://github.com/dz3ai/allclaws)

---

*Last updated: May 5, 2026*
