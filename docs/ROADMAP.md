# AllClaws Research Roadmap

**[中文](ROADMAP.zh-CN.md)** | English

> Strategic priorities and research focus areas for the second half of 2026.

---

## H2 2026 Priorities

### Theme: From Cataloguing to Understanding

The initial phase of AllClaws catalogued 31 platforms and analyzed their architectures. The remaining H2 2026 (July-December) shifts focus **from what exists to how agents fail, interoperate, and mature in production.**

**Key Questions:**
1. How do agents fail in real-world production scenarios? Can we build a systematic taxonomy?
2. How are the protocol wars shaping agent interoperability (MCP vs A2A vs proprietary)?
3. What are the real economics of running agent systems — not just API costs but maintenance, review, and technical debt?
4. What does the Chinese AI agent ecosystem look like beyond the 31 currently tracked platforms?

---

## Q3 2026 (July-September)

### 1. Complete Unified Platform Comparison

**Status:** Completed ✅
**Target:** Complete architecture documentation for all 31 platforms

**Deliverables:**
- [x] `architecture/platform_comparison.md` — Unified comparison of all 31 platforms
- [x] Standardized format for each platform (classification, architecture, diagrams)
- [x] Cross-platform comparison matrices
- [x] Chinese translation (`platform_comparison.zh-CN.md`)

**Scope:**
- **Claw Ecosystem (11):** OpenClaw, ClawTeam, GoClaw, IronClaw, Maxclaw, NanoClaw, Nanobot, ZeroClaw, HiClaw, Hermes-Agent, Claw-AI-Lab
- **CLI Coding Agents (5):** aider, copilot-cli, reasonix, kimi-cli, codex
- **Human Digital Twin (1):** openhuman
- **External Frameworks (13):** SmolAgents, LangGraph, CrewAI, AutoGen, Swarms, OpenAgents, OpenFang, kimi-code, AgentScope, Eliza, Agent Zero, PraisonAI, Rocketride

### 2. MCP Ecosystem Deep-Dive

**Status:** Completed ✅
**Target:** Comprehensive analysis of MCP protocol adoption and resistance

**Research Questions:**
- What is the actual token overhead of MCP in production deployments?
- Which MCP servers are most widely adopted?
- How do MCP-native frameworks differ from MCP-adapter approaches?
- What is the rate of MCP adoption across the 31 tracked platforms?

**Deliverables:**
- MCP adoption report (native vs adapter vs resistant)
- Token cost analysis
- MCP server ecosystem catalog
- Recommendations for MCP evaluation

### 3. Enterprise Governance Frameworks Analysis

**Status:** Completed ✅
**Target:** Document emerging enterprise AI agent governance approaches

### 4. Evolutionary Harness Architectures

**Status:** ✅ Completed (July 2026)
**Target:** Analyze emerging research on harness evolution, auto-optimization, and harness-model co-evolution.

Leverages the HarnessX paper (arXiv 2606.14249, July 2026) as the primary academic reference for:
- Formal harness taxonomy (9 behavioral dimensions)
- Trace-driven harness evolution (AEGIS engine)
- Harness-model co-evolution via shared replay buffer
- Variant isolation for heterogeneous task sets

**Deliverables:**
- [x] `architecture/agent_harnesses.md` — New "Evolutionary Harness Architectures" section (July 2026)
- [x] HarnessX paper notes and findings captured

### 5. Agent Failure Mode Taxonomy

**Status:** Planned
**Target:** Build a systematic taxonomy of how AI agents break in production

Rather than cataloguing platforms, this focuses on **failure modes** — the concrete ways agents go wrong in real-world scenarios. Each failure mode is studied across multiple platforms.

**Research Questions:**
- What are the recurring failure patterns? (hallucination loops, tool misuse, context decay, infinite retries)
- Which failures are platform-specific vs universal?
- How do different architectures handle the same failure type?
- What recovery patterns work best?

**Deliverables:**
- Failure mode taxonomy (10-15 categories) with platform-specific examples
- Recovery pattern catalog
- Platform comparison by failure resilience
- Report: `docs/reports/failure-mode-taxonomy-2026.md`

### 6. China AI Agent Ecosystem Deep-Dive

**Status:** Completed ✅ (July 2026)
**Target:** Document the rapidly growing Chinese AI agent ecosystem
**Report:** `docs/reports/china-agent-ecosystem-2026.md`

Currently only AgentScope represents the Chinese ecosystem among 31 tracked platforms. Major active projects (Qwen-Agent, Dify, ModelScope, ByteDance agent tools) and the unique constraints of the GFW — limited access to OpenAI APIs, reliance on domestic models (GLM, Qwen, DeepSeek) — create a parallel ecosystem worth studying.

**Research Scope:**
- Map 10-15 active Chinese AI agent projects (open-source and notable closed-source)
- Analyze how the GFW shapes architecture decisions (local model preference, censorship bypass patterns)
- Compare Chinese agent design patterns vs Western equivalents
- Document government AI governance impact on agent development

**Deliverables:**
- Chinese ecosystem landscape report
- Architecture comparison: Chinese vs Western agent patterns
- Platform recommendations for AllClaws tracking (add 3-5 new platforms)
- Bilingual blog post (EN + ZH)

---

## Q4 2026 (October-December)

### 1. Personal-Force-Multiplier Case Studies

**Status:** Completed ✅ (July 2026)
**Target:** Document 1PC (one-person company) success stories
**Report:** `docs/reports/1pc-case-studies-2026.md`

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

**Status:** Completed ✅ (May 2026)

**Current State:** Runtime benchmarks fully operational
- 59 metrics collected across 13+ platforms with real environments
- N=5 sampling with statistical analysis (mean, std dev, CV)
- Local test environments: Python venvs, Node modules, Go toolchain, Rust targets
- CI integration via `run_benchmarks.yml` (weekly cron + manual dispatch)
- Benchmark results gitignored (CI artifacts only)

**Metrics Tracked:**
- Cold start time (ms)
- Memory usage — active (MB)
- Response latency (p50, p95, p99)
- Token efficiency (output/input ratio)

**Deliverables:**
- [x] Performance comparison across 31 platforms
- [x] Benchmark methodology documentation (EN + ZH)
- [x] Performance regression detection (CI integration)
- [x] Local benchmark environment setup

### 3. "Self-Improving" Claims Verification Series

**Status:** Completed ✅
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

### 4. Long-Running Agent Benchmarks

**Status:** Planned
**Target:** Upgrade benchmark suite from micro-benchmarks to end-to-end task evaluation

Current benchmarks measure startup time and dependencies — informative but disconnected from real work. The next evolution tracks agents completing sustained, realistic tasks.

**Research Questions:**
- How do agents perform on tasks lasting 30+ minutes (GitHub issue resolution, multi-file refactoring)?
- What is the token cost vs outcome quality curve?
- How does technical debt accumulate across agent sessions?
- Can we detect "agent fatigue" — quality degradation over long sessions?

**Deliverables:**
- Long-running benchmark suite (5+ realistic task scenarios)
- Token cost modeling tool (estimated API spend per task type)
- Comparison of agent quality maintenance across platforms
- CI integration for weekly long-run benchmarking

### 5. Protocol Wars: MCP vs A2A vs Proprietary

**Status:** Planned
**Target:** Analyze the emerging battle over agent communication standards

Google's Agent-to-Agent (A2A) protocol, Anthropic's MCP, and proprietary solutions from OpenAI/Cursor are vying to become the standard for how agents communicate and share tools. This is a foundational infrastructure decision affecting all 31 tracked platforms.

**Research Questions:**
- How do MCP, A2A, and proprietary protocols differ in latency, security, and expressiveness?
- Which platforms are adopting which protocol? Is bifurcation forming?
- What does protocol choice mean for agent composability?
- How does the protocol choice affect the 1PC vs Enterprise fork identified in H1 2026?

**Deliverables:**
- Protocol comparison matrix (MCP vs A2A vs proprietary)
- Platform adoption survey across 31 tracked projects
- Recommendations for protocol evaluation
- Report: `docs/reports/protocol-wars-2026.md`

### 6. Platform Governance & Quality Thresholds

**Status:** Planned
**Target:** Establish governance rules for a maturing platform catalog

At 31 platforms with growth momentum, AllClaws needs governance to maintain quality. This project formalizes: which platforms earn a spot, which get archived, and what "good" documentation looks like.

**Research Questions:**
- Should AllClaws cap at 35 platforms? What are the admission criteria?
- How to handle platforms that go stale (last commit > 6 months)?
- What is a minimum viable platform analysis?
- When does a platform "earn" its own architecture doc vs a footnote?

**Deliverables:**
- Platform admission policy (documented criteria)
- Quarterly stale-platform review process
- Quality checklist for platform analysis
- Stale project archiving criteria and timeline

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
- CLI Coding Agents (aider, copilot-cli, reasonix, kimi-cli, codex) are tracked via documentation review rather than automated tests, as they are external frameworks without local test targets
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

## Future Directions (H1 2027 Preview)

These directions may become formal H1 2027 targets, depending on H2 2026 findings:

1. **Agent Economics** — Real cost models beyond API pricing (maintenance overhead, review cost, technical debt accumulation)
2. **Multi-Agent Orchestration Patterns** — Emergent design patterns for coordinating 3+ agents in production
3. **Mobile-First Agents** — AI agents optimized for mobile and edge deployment
4. **Agent Security & Supply Chain** — Vulnerability analysis of agent plugin ecosystems
5. **Vertical-Specific Deep-Dives** — Healthcare, finance, legal AI agent analysis

### Expansion Criteria

New platforms may be added based on:
- Active development (commits in current year)
- Strategic significance (novel patterns, reference implementations)
- Community traction (stars, forks, discussion)
- Architectural distinctiveness (represents different approach)

---

## Stale / Inactive Projects

The following projects have had no recent activity and are candidates for archiving under the new quarterly review process:

| Project | Last Activity | Stars | Status |
|---------|--------------|-------|--------|
| Claw-AI-Lab | No tags released | ~10K | ⚠️ Review Q3 2026 |
| ClawTeam | Apr 14, 2026 | 19.7K | ⚠️ Review Q3 2026 |
| GoClaw | Apr 27, 2026 | 3.2K | ⚠️ Review Q3 2026 |
| MaxClaw | May 5, 2026 | 228 | ⚠️ Low impact, review Q3 2026 |
| AutoGen | Apr 6, 2026 | 58.5K | ⚠️ Maintenance mode, review Q4 2026 |

**Archiving criteria:** Projects with no commits for 6+ months and no strategic significance may be archived (removing submodule, noting in history). Archived projects remain in documentation for historical comparison.

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

*Last updated: July 19, 2026*
