# AllClaws: Personal AI Agent Ecosystem Analysis & Testing

**[中文](README-zh_CN.md)** | English

**AllClaws** is a comprehensive research and development project focused on analyzing, comparing, and testing personal AI agent platforms. This umbrella project brings together architecture analysis, performance benchmarking, and thought leadership in the personal AI assistant space.

## 🎯 Mission

AllClaws conducts independent research on AI agent architectures and deployment models, with emphasis on understanding the emerging distinction between **personal-force-multiplier** and **enterprise-automation** paradigms. We track 35 platforms across both claw ecosystem and external frameworks to provide objective analysis of real capabilities versus marketing claims.

**Full Mission:** [docs/MISSION.md](docs/MISSION.md)

## 🗂️ What We Track

**35 Tier-1 platforms** in four categories (plus 7 harness ecosystems, see [governance](docs/governance.md)):

**Claw Ecosystem (11):** OpenClaw, ClawTeam, GoClaw, IronClaw, Maxclaw, NanoClaw, Nanobot, ZeroClaw, HiClaw, Hermes-Agent, Claw-AI-Lab

**External Frameworks (18):** SmolAgents, LangGraph, CrewAI, AutoGen, Swarms, OpenAgents, OpenFang, kimi-code, AgentScope, Eliza, Agent Zero, PraisonAI, Rocketride, OpenWorker, Dify, MetaGPT, Qwen-Agent, browser-use

**CLI Coding Agents (5):** aider, copilot-cli, reasonix, kimi-cli, codex

**Human Digital Twin (1):** openhuman

Platform URLs are listed in [architecture/platform_comparison.md](architecture/platform_comparison.md) — the canonical comparison covering all 35 platforms (EN + ZH).

## 🔥 Key Insights

1. **The Personal vs Enterprise Fork** — Clear divergence between personal-force-multiplier (1PC) and enterprise-automation paradigms
2. **MCP Debate Intensifies** — Model Context Protocol gaining enterprise adoption but facing resistance from local-first agents over token overhead
3. **"Self-Improving" Claims Scrutiny** — After Hermes-Agent source code analysis, distinction between procedural memory and autonomous learning is critical
4. **Protocol Layering, Not War** — MCP owns tools (13 impls), ACP owns client↔agent (5 impls), A2A owns discovery (1 production impl); vendor APIs remain the default
5. **Evolutionary Harness Architectures** — HarnessX (arXiv:2606.14249) formalizes the harness as a first-class evolvable object

> 📊 **Latest ecosystem changes, platform-by-platform details, and the comparative snapshot table live in [docs/LATEST_UPDATES.md](docs/LATEST_UPDATES.md)** (monthly refresh, EN + ZH).

## 📋 Current Work

### 1. Architecture Analysis & Comparison — ✅ Active
Unified comparison of all 35 tracked platforms: classification, core architecture, mermaid diagrams, and 5 comparison matrices.
- [architecture/platform_comparison.md](architecture/platform_comparison.md) — canonical, EN + ZH
- [architecture/agent_harnesses.md](architecture/agent_harnesses.md) — harness ecosystems & toolchains
- [architecture/multi_agent_coordination_research.md](architecture/multi_agent_coordination_research.md) — coordination trend analysis

### 2. Test Framework — ✅ v2.1
Static analysis across the 11 claw ecosystem submodules (language-level + project health checks).
```bash
cd test_framework
bash scripts/run_tests.sh
```

### 3. Benchmark Engine — ✅ v3.0 Python
140 runtime metrics across 26 platforms: cold start, memory, latency, binary size (N=5 sampling with stats).
```bash
cd test_framework
python3 -m benchmark.cli runtime --runs 5
python3 -m benchmark.cli static
python3 -m benchmark.cli report --last 5 --regression 20
```

### 4. Research Reports — ✅ Ongoing
Investigations beyond cataloguing — how agents fail, interoperate, and are governed. Key reports:
- Failure mode taxonomy (13 modes across 35 platforms) — [docs/reports/failure-mode-taxonomy-2026.md](docs/reports/failure-mode-taxonomy-2026.md)
- China AI agent ecosystem (14 projects) — [docs/reports/china-agent-ecosystem-2026.md](docs/reports/china-agent-ecosystem-2026.md)
- Protocol wars (MCP/ACP/A2A) — [docs/reports/protocol-wars-2026.md](docs/reports/protocol-wars-2026.md)
- MCP deep-dive (5 phases) — [docs/reports/mcp-deep-dive-phase4-5-synthesis.md](docs/reports/mcp-deep-dive-phase4-5-synthesis.md)
- Full index: [docs/reports/](docs/reports/)

### 5. Technical Writing & Thought Leadership — 📝 Ongoing
- Monthly ecosystem reports in [`_posts/`](_posts/) (EN + ZH)
- [Latest Updates](docs/LATEST_UPDATES.md) — monthly platform-by-platform tracking

## 📊 Current Status & Roadmap

H2 2026 research plan: **12 of 13 items completed**. Only Q4-4 (long-running agent benchmarks) remains.

### ✅ Completed (selected)
- [x] Architecture analysis of 35 platforms (11 claw + 18 external + 5 CLI coding agents + 1 human digital twin)
- [x] Unified platform comparison (all 35 platforms, EN + ZH)
- [x] Benchmark engine v3.0 (140 runtime metrics / 26 platforms) + CI integration
- [x] MCP ecosystem deep-dive (5 phases) & enterprise governance analysis
- [x] Failure mode taxonomy (13 modes across 35 platforms)
- [x] China ecosystem deep-dive → added Dify, MetaGPT, Qwen-Agent; browser-use (#35, first computer-use representative)
- [x] Protocol wars analysis (Q4-5) — layering, not war
- [x] Platform governance (Q4-6) — three-tier tracking model, Tier-1 cap of 35
- [x] Category coverage gap-closure (Q4-7) — browser-use admitted, 6 candidates evaluated

### 🔄 In Progress (H2 2026)
- [ ] Q4-4: Long-running agent benchmarks (end-to-end task evaluation, 30+ min tasks)

### 📋 Planned (H1 2027 Preview)
- [ ] Agent economics — real cost models beyond API pricing
- [ ] Multi-agent orchestration patterns
- [ ] Multi-agent economics and cost optimization
- [ ] Agent security & supply chain analysis

**Full roadmap:** [docs/ROADMAP.md](docs/ROADMAP.md)

## 🚀 Quick Start

```bash
# Read the comprehensive platform comparison
cat architecture/platform_comparison.md

# Run tests and benchmarks
cd test_framework
bash scripts/run_tests.sh
python3 -m benchmark.cli runtime --runs 5
```

## 🤝 Contributing

This is an active research project. Contributions welcome in:
- Platform architecture analysis
- Test case development
- Documentation improvements
- Claims verification research

## 📝 License & Security

- **License**: MIT (core framework), platform-specific licenses apply
- **Privacy**: No personal data collection or storage

## 🔗 Related Projects

- **Sibling repo**: [dz3ai/coder_arena](https://github.com/dz3ai/coder_arena) — AI coding agent submodules (coding agents only, no blog)
- All 35 platform URLs: [architecture/platform_comparison.md](architecture/platform_comparison.md)
- Research reports index: [docs/reports/](docs/reports/)

## 📞 Contact & Discussion

For discussions, questions, or collaboration opportunities, please refer to the individual platform repositories or create issues in this analysis repository.

**Full Documentation:**
- Mission: [docs/MISSION.md](docs/MISSION.md)
- Roadmap: [docs/ROADMAP.md](docs/ROADMAP.md)
- Governance: [docs/governance.md](docs/governance.md)
- Latest Updates: [docs/LATEST_UPDATES.md](docs/LATEST_UPDATES.md)

---

*Last updated: August 20, 2026*
