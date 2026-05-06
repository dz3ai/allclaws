# AllClaws Research Roadmap

**[中文](ROADMAP.zh-CN.md)** | English

> Strategic priorities and research focus areas for the second half of 2026.

---

## H2 2026 Priorities

### Theme: The Personal vs Enterprise Fork

The primary focus for H2 2026 is documenting and analyzing the emerging fork between **personal-force-multiplier** and **enterprise-automation** AI agent paradigms.

**Key Questions:**
1. How do these paradigms differ architecturally?
2. What trade-offs do developers make when choosing one over the other?
3. Will the ecosystems converge or diverge further?
4. What patterns transfer between paradigms?

---

## Q3 2026 (July-September)

### 1. Complete Unified Platform Comparison

**Status:** Completed ✅
**Target:** Complete architecture documentation for all 20 platforms

**Deliverables:**
- [x] `architecture/platform_comparison.md` — Unified comparison of all 20 platforms
- [x] Standardized format for each platform (classification, architecture, diagrams)
- [x] Cross-platform comparison matrices
- [x] Chinese translation (`platform_comparison.zh-CN.md`)

**Scope:**
- **Claw Ecosystem (13):** OpenClaw, ClawTeam, GoClaw, IronClaw, Maxclaw, NanoClaw, Nanobot, ZeroClaw, HiClaw, QuantumClaw, Hermes-Agent, RTL-CLAW, Claw-AI-Lab
- **External Frameworks (7):** SmolAgents, LangGraph, mcp-agent, CrewAI, AutoGen, Swarms, OpenAgents

### 2. MCP Ecosystem Deep-Dive

**Status:** Planned
**Target:** Comprehensive analysis of MCP protocol adoption and resistance

**Research Questions:**
- What is the actual token overhead of MCP in production deployments?
- Which MCP servers are most widely adopted?
- How do MCP-native frameworks (mcp-agent) differ from MCP-adapter approaches?
- What is the rate of MCP adoption across the 20 tracked platforms?

**Deliverables:**
- MCP adoption report (native vs adapter vs resistant)
- Token cost analysis
- MCP server ecosystem catalog
- Recommendations for MCP evaluation

### 3. Enterprise Governance Frameworks Analysis

**Status:** Planned
**Target:** Document emerging enterprise AI agent governance approaches

**Research Scope:**
- Okta's AI agent identity framework
- Enterprise deployment patterns (HiClaw, GoClaw, LangGraph, Swarms)
- Human-in-the-loop workflows
- Credential isolation patterns

**Deliverables:**
- Enterprise governance comparison matrix
- Best practices documentation
- Risk analysis frameworks

---

## Q4 2026 (October-December)

### 1. Personal-Force-Multiplier Case Studies

**Status:** Planned
**Target:** Document 1PC (one-person company) success stories

**Research Scope:**
- Interview solo founders using AI agents
- Document workflows and toolchains
- Analyze cost/benefit vs traditional hiring
- Identify platform preferences in 1PC context

**Deliverables:**
- 5-10 case studies
- Common patterns analysis
- Platform recommendations for 1PCs
- ROI analysis

### 2. Runtime Performance Benchmarking

**Status:** Planned
**Target:** Extend test framework for runtime performance metrics

**Current State:** Test framework covers static analysis (177 tests, 165 pass)
**Target State:** Add runtime performance metrics

**Metrics to Track:**
- Cold start time
- Memory usage (idle and active)
- Response latency (p50, p95, p99)
- Token efficiency (output/input ratio)

**Deliverables:**
- Performance comparison across 20 platforms
- Benchmark methodology documentation
- Performance regression detection

### 3. "Self-Improving" Claims Verification Series

**Status:** Planned
**Target:** Systematic verification of autonomous learning claims

**Following:** Hermes-Agent analysis (May 2026)

**Platforms to Verify:**
- Any platform claiming "self-improving" capabilities
- RL-based learning systems
- Adaptive skill systems
- Performance optimization claims

**Methodology:**
- Source code analysis
- Documentation vs implementation comparison
- Evidence of actual performance improvement over time

---

## Ongoing Activities

### Monthly Ecosystem Reports

**Frequency:** First Monday of each month
**Scope:**
- Platform updates (releases, CVEs, features)
- Cross-cutting trends
- Test framework results
- Emerging patterns

**Next Reports:**
- July 2026: MCP deep-dive preliminary findings
- August 2026: Enterprise governance frameworks
- September 2026: Q3 synthesis
- October 2026: 1PC case studies kickoff
- November 2026: Performance benchmarking preview
- December 2026: 2026 Year-in-Review

### Test Framework Maintenance

**Frequency:** Weekly
**Activities:**
- Run test suite on all 13 claw ecosystem platforms
- Track test pass/fail rates
- Investigate failures
- Update test cases as platforms evolve

**Current Status:** 165/177 pass (93% pass rate)

### Claims Verification

**Frequency:** Ad-hoc, triggered by marketing claims
**Methodology:**
- Identify claim
- Analyze source code
- Compare to documentation
- Publish findings

---

## Future Directions (2027+)

### Potential Focus Areas

1. **Mobile-First Agents** — AI agents optimized for mobile deployment
2. **Edge Computing Agents** — Resource-constrained agent deployments
3. **Blockchain-Integrated Agents** — Agents with blockchain-based identity/coordination
4. **Vertical-Specific Analysis** — Healthcare, finance, legal AI agents
5. **Agent Interoperability** — Cross-platform agent communication protocols

### Expansion Criteria

New platforms may be added based on:
- Active development (commits in current year)
- Strategic significance (novel patterns, reference implementations)
- Community traction (stars, forks, discussion)
- Architectural distinctiveness (represents different approach)

---

## Non-Goals

To maintain focus, AllClaws explicitly does **not** plan to:

1. **Rate platforms** — No "best platform" rankings
2. **Provide tutorials** — Other sources cover how-to guides
3. **Offer consulting** — We research, we don't advise deployments
4. **Predict markets** — We analyze technology, not investment potential

---

## Contribution Guidelines

We welcome contributions in:

- Platform architecture analysis
- Test case development
- Documentation improvements
- Claims verification research
- Translation (English/Chinese)

See [CONTRIBUTING.md](../CONTRIBUTING.md) for details.

---

## Contact

For discussions, questions, or collaboration opportunities:
- GitHub: [github.com/dz3ai/allclaws](https://github.com/dz3ai/allclaws)
- Issues: [github.com/dz3ai/allclaws/issues](https://github.com/dz3ai/allclaws/issues)

---

*Last updated: May 6, 2026*
