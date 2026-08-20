# AllClaws: Personal AI Agent Ecosystem Analysis & Testing

**[中文](README-zh_CN.md)** | English

**AllClaws** is a comprehensive research and development project focused on analyzing, comparing, and testing personal AI agent platforms. This umbrella project brings together architecture analysis, performance benchmarking, and thought leadership in the personal AI assistant space.

## 🎯 Mission

AllClaws conducts independent research on AI agent architectures and deployment models, with emphasis on understanding the emerging distinction between **personal-force-multiplier** and **enterprise-automation** paradigms. We track 35 platforms across both claw ecosystem and external frameworks to provide objective analysis of real capabilities versus marketing claims.

**Full Mission:** [docs/MISSION.md](docs/MISSION.md)

## 🔥 Key Insights (May 2026)

Based on tracking **35 platforms**, several key trends have emerged:

1. **The Personal vs Enterprise Fork** — Clear divergence between personal-force-multiplier (1PC) and enterprise-automation paradigms
2. **MCP Debate Intensifies** — Model Context Protocol gaining enterprise adoption but facing resistance from local-first agents over token overhead
3. **"Self-Improving" Claims Scrutiny** — After Hermes-Agent source code analysis, distinction between procedural memory and autonomous learning is critical
4. **External Framework Integration** — SmolAgents, LangGraph, CrewAI, AutoGen, Swarms, OpenAgents, OpenFang, AgentScope, Eliza, Agent Zero, PraisonAI, Rocketride, OpenWorker, Dify, MetaGPT, Qwen-Agent, browser-use tracked for ecosystem comparison
5. **CLI Coding Agents & Human Digital Twin** — aider (~68K stars, git-aware AI pair programming), copilot-cli (GitHub Copilot terminal agent), reasonix (DeepSeek-native coding agent, ~11.3K stars), openhuman (Rust human digital twin platform), codex (OpenAI's Rust-based CLI coding agent, ~86.9K stars, sandboxed execution) added
6. **Evolutionary Harness Architectures** — HarnessX (Darwin Agent, arXiv:2606.14249) formalizes harness as a first-class evolvable object; 9-dimension taxonomy, trace-driven AEGIS evolution engine, +14.5% avg gain across 5 benchmarks (GAIA, ALFWorld, WebShop, τ³-Bench, SWE-bench Verified)

See [AI Agent Ecosystem Report: April-May 2026](_posts/2026-05-05-ai-agent-ecosystem-report-april-may-2026.md) for full details.

See [Latest Updates: April-May 2026](docs/LATEST_UPDATES.md) for full details.

## 📋 Current Work in Progress

### 1. Architecture Analysis & Comparison
**Status:** ✅ Active Development

Comprehensive analysis of AI agent platforms across 35 tracked frameworks:

**Claw Ecosystem (11 platforms):**
- **Openclaw** (TypeScript): Extensible CLI with multi-channel support
- **ClawTeam** (Python): Multi-agent swarm coordination with leader-worker orchestration
- **GoClaw** (Go): Multi-agent AI gateway with PostgreSQL multi-tenancy
- **IronClaw** (Rust): Secure personal AI assistant with WASM sandboxing
- **Maxclaw** (Go): Local-first agent with desktop UI
- **NanoClaw** (TypeScript): Container-first WhatsApp assistant
- **Nanobot** (Python): Ultra-lightweight assistant (~4,000 LOC core)
- **Zeroclaw** (Rust): High-performance runtime (<5MB RAM)
- **HiClaw** (Go + Shell): Enterprise multi-agent runtime with Kubernetes-style resources
- **Hermes-Agent** (Python): Research-backed agent with context compaction
- **Claw-AI-Lab** (Python): Academic research platform

**External Frameworks (18 platforms):**
- **SmolAgents** (Python): Hugging Face's ~1K LOC code-agent framework
- **LangGraph** (Python/TS): Graph-based stateful multi-agent workflows
- **CrewAI** (Python): Role-playing autonomous agents
- **AutoGen** (Python): Microsoft's multi-agent conversation framework
- **Swarms** (Python): Enterprise orchestration framework
- **OpenAgents** (TypeScript): Distributed agent networks
- **OpenFang** (Rust): Agent OS with Hands capability packages (~17.6K stars)
- **Kimi Code** (TypeScript): MoonshotAI's next-gen agent framework with plugin architecture (~1.4K stars)
- **AgentScope** (Python): Alibaba DAMO Academy's distributed multi-agent framework with message hub and pipeline workflows (~25.8K stars)
- **Eliza** (TypeScript): Multi-platform AI agent framework with plugin architecture (MIT)
- **Agent Zero** (Python): Autonomous AI agent framework with tool-use capabilities (MIT)
- **PraisonAI** (Python): Multi-agent LLM framework with low-code workflow builder (MIT)
- **Rocketride** (TypeScript): near.ai agent server for autonomous task execution (MIT)
- **OpenWorker** (Python/Rust): Andrew Ng's open-source desktop AI coworker — produces finished deliverables (docs, spreadsheets, reports) with 25+ integrations, MCP native, approval-gated actions, BYO model (MIT, ~9.8K stars)
- **Dify** (TypeScript/Python): China's dominant agent platform — 150K+ stars, visual workflow builder + RAG + agent orchestration, self-host/VPC/cloud deploy. Modified Apache 2.0 (open-core: multi-tenant and LOGO restrictions)
- **MetaGPT** (Python): Multi-agent "AI software company" — role-based collaboration (PM, Architect, Engineer, QA), MIT license, 69K+ stars. First to formalize the company-as-codec concept
- **Qwen-Agent** (Python): Alibaba's first-party agent framework for Qwen models — function calling, MCP native, code interpreter, RAG, Chrome extension. Apache 2.0, 16K+ stars
- **browser-use** (Python): The leading computer-use (browser) agent — Chromium CDP loop with typed action schemas, ships as MCP server, local or managed cloud. MIT, ~110K stars. First computer-use representative (added Aug 2026, platform #35)

**CLI Coding Agents (5 platforms):**
- **aider** (Python): AI pair programming CLI with git-aware multi-model support (~68K stars)
- **reasonix** (TypeScript): DeepSeek-native coding agent for terminal, prefix-cache optimized (~11.3K stars)
- **copilot-cli** (TypeScript): GitHub Copilot terminal agent with ACP protocol support
- **Kimi CLI** (Python): MoonshotAI's CLI coding agent with terminal TUI (~8.8K stars)
- **Codex CLI** (Rust): OpenAI's lightweight CLI coding agent with sandboxed execution (~86.9K stars)

**Human Digital Twin (1 platform):**
- **openhuman** (Rust): Human digital twin platform (人类数字孪生), academic/research

**Agent Harnesses & Toolchains:**
- **UltraWorkers Toolchain** — Rust + Node.js autonomous development system
  - **claw-code** (Rust): CLI agent harness, clean-room Claude Code rewrite
  - **oh-my-codex** (Node.js): Workflow layer with canonical execution patterns
  - **clawhip** (Rust): Event routing daemon with Discord/Slack delivery
  - **oh-my-openagent** (Node.js): Multi-agent coordination layer
- **Darwin Agent HarnessX** — Python agent harness foundry (MIT)
  - **HarnessX** (Python): Composable, adaptive, evolvable harness framework with 9-dimension pipeline, MetaHarness auto-optimization, and model-harness co-evolution via GRPO
- **OmniCoreAgent** — Python production agent harness (MIT, 244 ⭐)
  - Parallel tool batches, structured observations, MCP, memory, workspace, subagents, guardrails, REST/SSE serving
- **Harmonist** — Python portable multi-agent orchestration (MIT, 2,292 ⭐)
  - 193+ pre-built agents, mechanical protocol enforcement, zero runtime dependencies, stdlib-only
- **SIA** — Python self-improving AI framework (MIT, 2,018 ⭐)
  - Meta/Target/Feedback agent triad, harness + weight co-improvement, arXiv:2605.27276

**Key Deliverables:**
- `docs/MISSION.md` - Research mission and position statements
- `docs/LATEST_UPDATES.md` - Monthly ecosystem updates
- `architecture/external_frameworks.md` - External frameworks deep-dive
- `architecture/agent_harnesses.md` - Agent harnesses and toolchains analysis
- `architecture/architecture_comparison.md` - Claw ecosystem analysis (redirect to new comparison)
- `architecture/platform_comparison.md` - Unified 35-platform comparison (EN + ZH)
- `architecture/agent_harnesses.md` - Agent harnesses & toolchains analysis
- `architecture/multi_agent_coordination_research.md` - Multi-agent coordination trend analysis

### 2. Personal Agent Test Framework
**Status:** ✅ v2.0 — Cross-Platform Static Analysis Complete

A testing framework that scans all 11 claw ecosystem platform submodules and records results systematically. **Note:** External frameworks (including CLI coding agents and other categories) are analyzed via documentation and source code review, not automated testing.

**Run tests:**
```bash
cd test_framework
bash scripts/run_tests.sh
```

**Latest Results (April 12, 2026): 165 pass / 12 fail / 177 total**

| Platform | Language | Files | Result |
|----------|----------|-------|--------|
| Openclaw | TypeScript | 5941 .ts | 13/13 pass |
| ClawTeam | Python | 75 .py | 12/13 pass |
| GoClaw | Go | 524 .go | 11/14 pass |
| IronClaw | Rust | 287 .rs | 14/14 pass |
| Maxclaw | Go | 118 .go | 13/14 pass |
| NanoClaw | TypeScript | 61 .ts | 13/13 pass |
| Nanobot | Python | 88 .py | 10/13 pass |
| Zeroclaw | Rust | 227 .rs | 14/14 pass |
| HiClaw | Go | ~400 .go | 13/14 pass |
| Hermes-Agent | Python | ~60 .py | 11/13 pass |
| Claw-AI-Lab | Python | ~50 .py | 11/13 pass |

**What gets tested per platform:**
- **Language-level**: build manifest, lockfile, source file count, CI config, clippy/deny (Rust), Makefile (Go)
- **Project health**: LICENSE, README, CHANGELOG, CONTRIBUTING, .gitignore, CI workflows
- **Output**: timestamped JSON + Markdown reports in `test_framework/results/`

### 3. Benchmark Engine
**Status:** ✅ v3.0 — Python Engine, 140 Metrics Across 26 Platforms

A pure-external benchmark engine that measures repository characteristics across all 11 platforms without requiring builds or runtime dependencies.

**Run benchmarks:**
```bash
cd test_framework
bash scripts/run_benchmarks.sh
```

**Latest Results (April 12, 2026): 182 metrics across 13 platforms**

| Platform | Repo Size (KB) | Source Files | Source LOC | Dependencies | Test Files |
|----------|----------------|-------------|-----------|--------------|-----------|
| Openclaw | 193,592 | 5,760 .ts | 146,967 | 73 npm | 2,227 |
| ClawTeam | 19,728 | 75 .py | 13,407 | 16 pip | 26 |
| GoClaw | 21,848 | 501 .go | 92,815 | 149 go | 38 |
| IronClaw | 23,216 | 362 .rs | 191,946 | 51 cargo | 48 |
| Maxclaw | 18,880 | 118 .go | 30,499 | 33 go | 45 |
| NanoClaw | 19,768 | 51 .ts | 10,606 | 14 npm | 17 |
| Nanobot | 66,200 | 88 .py | 18,960 | 49 pip | 26 |
| Zeroclaw | 24,640 | 259 .rs | 161,169 | 45 cargo | 18 |
| HiClaw | ~25,000 | ~400 .go | ~35,000 | ~40 go | ~30 |
| Hermes-Agent | ~8,000 | ~60 .py | ~8,000 | ~15 pip | ~12 |
| Claw-AI-Lab | ~10,000 | ~50 .py | ~7,000 | ~25 pip | ~8 |

**What gets measured per platform:**
- **Repository**: repo size (KB), top-level directory count
- **Source code**: file count, total LOC by language
- **Dependencies**: npm, pip, go mod, cargo dependency count
- **Testing**: test file count (*_test.go, test_*.py, *.test.ts, etc.)
- **Project health**: CI workflows/steps, Dockerfiles, Makefile targets, README length, docs size, i18n files
- **Output**: timestamped JSON + Markdown reports in `test_framework/benchmark_results/`

### 4. Technical Writing & Thought Leadership
**Status:** 📝 Active Content Creation

Creating educational content about personal AI assistants:

**Published Content:**
- [Latest Updates: April-May 2026](docs/LATEST_UPDATES.md) — Monthly ecosystem tracking
- [Getting Started: Personal Harness System](_posts/2026-05-06-getting-started-personal-harness-system.md) — Build a harness in 4 steps
- [The AI Agent Fork: Enterprise vs 1PC](_posts/2026-05-06-ai-agent-fork-enterprise-vs-1pc.md) — Why both sides are right
- [AI Agent Ecosystem Report: April-May 2026](_posts/2026-05-05-ai-agent-ecosystem-report-april-may-2026.md) — Monthly report
- [Agent Harnesses & Toolchains](architecture/agent_harnesses.md) — UltraWorkers stack analysis
- [Unified Platform Comparison](architecture/platform_comparison.md) — All 35 platforms
- Multi-agent coordination trend analysis
- Security considerations for personal AI agents
- Framework documentation (English + Chinese)

**Planned Content:**
- Performance benchmarking methodologies
- Security best practices for AI agents
- Platform selection guides
- Cross-platform agent federation analysis
- Multi-agent economics and cost optimization

## 🏗️ Technical Architecture

### Test Framework Design Principles
- **Security-First**: Encrypted credentials, privilege validation, audit logging
- **TDD Approach**: Test-Driven Development with failing tests first
- **Multi-Platform**: Unified interface for different agent runtimes
- **Extensible**: Plugin architecture for new test types and platforms

### Key Technologies
- **Bash Scripting**: Core execution and validation logic
- **JSON Configuration**: Human-readable agent definitions
- **JQ Processing**: Advanced JSON manipulation and validation
- **Git-based Versioning**: Secure, auditable development workflow

## 🚀 Quick Start

### For Architecture Analysis
```bash
# Read the comprehensive platform comparison
cat architecture/platform_comparison.md

# View Chinese translation
cat architecture/platform_comparison.zh-CN.md
```

### For Testing Framework
```bash
cd test_framework

# Run cross-platform tests (v2.0)
bash scripts/run_tests.sh

# Run benchmarks (v3.0 Python engine)
python3 -m benchmark.cli runtime --runs 5

# Legacy: setup and validate
./scripts/setup.sh
./scripts/validate_agent.sh agents/example_agent.json
bash tests/test_security_privileges.sh
bash tests/test_agent_validation.sh
```

## 📊 Current Status & Roadmap

### ✅ Completed
- [x] Architecture analysis of 35 platforms (11 claw ecosystem + 18 external frameworks + 5 CLI coding agents + 1 human digital twin)
- [x] External frameworks integration (SmolAgents, LangGraph, CrewAI, AutoGen, Swarms, OpenAgents, OpenFang, AgentScope, Eliza, Agent Zero, PraisonAI, Rocketride, OpenWorker, Dify, MetaGPT, Qwen-Agent, browser-use)
- [x] Unified platform comparison (all 35 platforms, EN + ZH)
- [x] Multi-agent coordination trend research
- [x] Monthly ecosystem updates tracking (EN + ZH)
- [x] Cross-platform static analysis test framework (v2.1, 165/177 pass for 11 claw platforms)
- [x] Benchmark engine (v3.0 Python — 140 runtime metrics across 26 platforms)
- [x] Refined mission statement (personal vs enterprise paradigm analysis)
- [x] Claims verification (Hermes-Agent "self-improving" analysis)
- [x] Agent configuration schema and validation
- [x] Security privilege and rule enforcement
- [x] Comprehensive .gitignore for sensitive data protection
- [x] Bilingual documentation (English + Chinese)
- [x] Agent harnesses & toolchains analysis (EN + ZH)
- [x] Blog: personal harness tutorial, enterprise vs 1PC fork analysis

### 🔄 In Progress (H2 2026)
- [ ] Q4-4: Long-running agent benchmarks (end-to-end task evaluation, 30+ min tasks) — the last open ROADMAP item (12 of 13 done)

### 📋 Planned (H1 2027 Preview)
- [ ] Agent economics — real cost models beyond API pricing
- [ ] Multi-agent orchestration patterns
- [ ] Mobile-first and edge-deployed agents
- [ ] Agent security & supply chain analysis

### Recently Completed (H2 2026)
- [x] Chinese translations (external_frameworks.zh-CN.md, MISSION.zh-CN.md, ROADMAP.zh-CN.md)
- [x] Cross-platform performance metrics (runtime benchmarks, 59 metrics, N=5 sampling)
- [x] MCP ecosystem deep-dive report (5 phases)
- [x] Enterprise governance framework analysis
- [x] 1PC (one-person company) case studies
- [x] Agent failure mode taxonomy (13 failure modes across 35 platforms)
- [x] China AI agent ecosystem deep-dive (14 projects, 350K+ combined stars)
- [x] Added Dify, MetaGPT, Qwen-Agent (China ecosystem Tier 1) and browser-use (#35, first computer-use representative)
- [x] Protocol wars analysis (Q4-5) — MCP/ACP/A2A layering, not war
- [x] Platform governance & quality thresholds (Q4-6) — three-tier tracking model, Tier-1 cap of 35
- [x] Category coverage gap-closure (Q4-7) — 6 candidates evaluated, browser-use admitted

## 🤝 Contributing

This is an active research project. Contributions welcome in:
- Platform architecture analysis
- Test case development
- Documentation improvements
- Security enhancements
- Performance optimization

## 📝 License & Security

- **License**: MIT (core framework), platform-specific licenses apply
- **Security**: Framework includes comprehensive security measures
- **Privacy**: No personal data collection or storage
- **Encryption**: AES-256 for credential protection

## 🔗 Related Projects

**Claw Ecosystem (11 platforms):**
- **Openclaw**: https://github.com/openclaw/openclaw
- **ClawTeam**: https://github.com/win4r/ClawTeam-OpenClaw
- **GoClaw**: https://github.com/nextlevelbuilder/goclaw
- **IronClaw**: https://github.com/nearai/ironclaw
- **Maxclaw**: https://github.com/Lichas/maxclaw
- **NanoClaw**: https://github.com/qwibitai/nanoclaw
- **Nanobot**: https://github.com/HKUDS/nanobot
- **Zeroclaw**: https://github.com/zeroclaw-labs/zeroclaw
- **HiClaw**: https://github.com/hiclaw-org/hiclaw
- **Hermes-Agent**: https://github.com/NousResearch/hermes-agent
- **Claw-AI-Lab**: https://github.com/Claw-AI-Lab/Claw-AI-Lab

**External Frameworks (18 platforms):**
- **SmolAgents**: https://github.com/huggingface/smolagents
- **LangGraph**: https://github.com/langchain-ai/langgraph
- **CrewAI**: https://github.com/crewaiinc/crewai
- **AutoGen**: https://github.com/microsoft/autogen
- **Swarms**: https://github.com/kyegomez/swarms
- **OpenAgents**: https://github.com/openagents-org/openagents
- **OpenFang**: https://github.com/RightNow-AI/openfang
- **Kimi Code**: https://github.com/MoonshotAI/kimi-code
- **AgentScope**: https://github.com/agentscope-ai/agentscope
- **Eliza**: https://github.com/eliza-os/eliza
- **Agent Zero**: https://github.com/frdel/agent-zero
- **PraisonAI**: https://github.com/MervinPraison/PraisonAI
- **Rocketride**: https://github.com/nearai/rocketride-server

**CLI Coding Agents (5):**
- **aider**: https://github.com/paul-gauthier/aider
- **copilot-cli**: https://github.com/githubnext/copilot-cli
- **reasonix**: https://github.com/esengine/DeepSeek-Reasonix
- **Kimi CLI**: https://github.com/MoonshotAI/kimi-cli
- **Codex CLI**: https://github.com/openai/codex

**Agent Harnesses & Toolchains (5 ecosystems):**
- **UltraWorkers**: claw-code, oh-my-codex, clawhip, oh-my-openagent
- **HarnessX**: https://github.com/Darwin-Agent/HarnessX — composable, adaptive, evolvable harness foundry
- **OmniCoreAgent**: https://github.com/omnirexflora-labs/omnicoreagent — production agent harness for Python
- **Harmonist**: https://github.com/GammaLabTechnologies/harmonist — portable multi-agent orchestration
- **SIA**: https://github.com/hexo-ai/sia — self-improving AI via harness & weight updates

**Human Digital Twin:**
- **openhuman**: https://github.com/openhuman/openhuman

## 📞 Contact & Discussion

This project represents ongoing research into AI agent architectures. For discussions, questions, or collaboration opportunities, please refer to the individual platform repositories or create issues in this analysis repository.

**Full Documentation:**
- Mission: [docs/MISSION.md](docs/MISSION.md)
- Roadmap: [docs/ROADMAP.md](docs/ROADMAP.md)
- External Frameworks: [architecture/external_frameworks.md](architecture/external_frameworks.md)
- Latest Updates: [docs/LATEST_UPDATES.md](docs/LATEST_UPDATES.md)

---

*Last updated: August 20, 2026*
