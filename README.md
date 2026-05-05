# AllClaws: Personal AI Agent Ecosystem Analysis & Testing

**[中文](README-zh_CN.md)** | English

**AllClaws** is a comprehensive research and development project focused on analyzing, comparing, and testing personal AI agent platforms. This umbrella project brings together architecture analysis, performance benchmarking, and thought leadership in the personal AI assistant space.

## 🎯 Mission

AllClaws conducts independent research on AI agent architectures and deployment models, with emphasis on understanding the emerging distinction between **personal-force-multiplier** and **enterprise-automation** paradigms. We track 20 platforms across both claw ecosystem and external frameworks to provide objective analysis of real capabilities versus marketing claims.

**Full Mission:** [docs/MISSION.md](docs/MISSION.md)

## 🔥 Key Insights (May 2026)

Based on tracking **20 platforms**, several key trends have emerged:

1. **The Personal vs Enterprise Fork** — Clear divergence between personal-force-multiplier (1PC) and enterprise-automation paradigms
2. **MCP Debate Intensifies** — Model Context Protocol gaining enterprise adoption but facing resistance from local-first agents over token overhead
3. **"Self-Improving" Claims Scrutiny** — After Hermes-Agent source code analysis, distinction between procedural memory and autonomous learning is critical
4. **External Framework Integration** — SmolAgents, LangGraph, CrewAI, AutoGen, Swarms, OpenAgents, mcp-agent tracked for ecosystem comparison

See [AI Agent Ecosystem Report: April-May 2026](_posts/2026-05-05-ai-agent-ecosystem-report-april-may-2026.md) for full details.

See [Latest Updates: March 2026](docs/LATEST_UPDATES.md) for full details.

## 📋 Current Work in Progress

### 1. Architecture Analysis & Comparison
**Status:** ✅ Active Development

Comprehensive analysis of AI agent platforms across 20 tracked frameworks:

**Claw Ecosystem (13 platforms):**
- **Openclaw** (TypeScript): Extensible CLI with multi-channel support
- **ClawTeam** (Python): Multi-agent swarm coordination with leader-worker orchestration
- **GoClaw** (Go): Multi-agent AI gateway with PostgreSQL multi-tenancy
- **IronClaw** (Rust): Secure personal AI assistant with WASM sandboxing
- **Maxclaw** (Go): Local-first agent with desktop UI
- **NanoClaw** (TypeScript): Container-first WhatsApp assistant
- **Nanobot** (Python): Ultra-lightweight assistant (~4,000 LOC core)
- **Zeroclaw** (Rust): High-performance runtime (<5MB RAM)
- **HiClaw** (Go + Shell): Enterprise multi-agent runtime with Kubernetes-style resources
- **QuantumClaw** (TypeScript): Self-hosted AGEX protocol implementation
- **Hermes-Agent** (Python): Research-backed agent with context compaction
- **RTL-CLAW** (Python/Verilog): EDA workflow automation
- **Claw-AI-Lab** (Python): Academic research platform

**External Frameworks (7 platforms):**
- **SmolAgents** (Python): Hugging Face's ~1K LOC code-agent framework
- **LangGraph** (Python/TS): Graph-based stateful multi-agent workflows
- **mcp-agent** (Python): MCP-native agent framework
- **CrewAI** (Python): Role-playing autonomous agents
- **AutoGen** (Python): Microsoft's multi-agent conversation framework
- **Swarms** (Python): Enterprise orchestration framework
- **OpenAgents** (TypeScript): Distributed agent networks

**Agent Harnesses & Toolchains:**
- **UltraWorkers Toolchain** — Rust + Node.js autonomous development system
  - **claw-code** (Rust): CLI agent harness, clean-room Claude Code rewrite
  - **oh-my-codex** (Node.js): Workflow layer with canonical execution patterns
  - **clawhip** (Rust): Event routing daemon with Discord/Slack delivery
  - **oh-my-openagent** (Node.js): Multi-agent coordination layer

**Key Deliverables:**
- `docs/MISSION.md` - Research mission and position statements
- `docs/LATEST_UPDATES.md` - Monthly ecosystem updates
- `architecture/external_frameworks.md` - External frameworks deep-dive
- `architecture/agent_harnesses.md` - Agent harnesses and toolchains analysis
- `architecture/architecture_comparison.md` - Claw ecosystem analysis (redirect to new comparison)
- `architecture/multi_agent_coordination_research.md` - Multi-agent coordination trend analysis

### 2. Personal Agent Test Framework
**Status:** ✅ v2.0 — Cross-Platform Static Analysis Complete

A testing framework that scans all 13 claw ecosystem platform submodules and records results systematically. **Note:** External frameworks are analyzed via documentation and source code review, not automated testing.

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
| QuantumClaw | TypeScript | ~150 .ts | 12/13 pass |
| Hermes-Agent | Python | ~60 .py | 11/13 pass |
| RTL-CLAW | Python/Verilog | ~80 mixed | 10/13 pass |
| Claw-AI-Lab | Python | ~50 .py | 11/13 pass |

**What gets tested per platform:**
- **Language-level**: build manifest, lockfile, source file count, CI config, clippy/deny (Rust), Makefile (Go)
- **Project health**: LICENSE, README, CHANGELOG, CONTRIBUTING, .gitignore, CI workflows
- **Output**: timestamped JSON + Markdown reports in `test_framework/results/`

### 3. Benchmark Engine
**Status:** ✅ v1.0 — Cross-Platform Metrics Collection Complete

A pure-external benchmark engine that measures repository characteristics across all 13 platforms without requiring builds or runtime dependencies.

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
| QuantumClaw | ~15,000 | ~150 .ts | ~25,000 | ~20 npm | ~15 |
| Hermes-Agent | ~8,000 | ~60 .py | ~8,000 | ~15 pip | ~12 |
| RTL-CLAW | ~12,000 | ~80 mixed | ~15,000 | ~20 pip | ~10 |
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
- [Latest Updates: March 2026](docs/LATEST_UPDATES.md) — Monthly ecosystem tracking
- Architecture comparison analysis (8 platforms)
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
cat architecture/architecture_comparison.md

# View Chinese translation
cat architecture/architecture_comparison.zh-CN.md
```

### For Testing Framework
```bash
cd test_framework

# Run cross-platform tests (v2.0)
bash scripts/run_tests.sh

# Run benchmarks (v1.0)
bash scripts/run_benchmarks.sh

# Legacy: setup and validate
./scripts/setup.sh
./scripts/validate_agent.sh agents/example_agent.json
bash tests/test_security_privileges.sh
bash tests/test_agent_validation.sh
```

## 📊 Current Status & Roadmap

### ✅ Completed
- [x] Architecture analysis of 20 platforms (13 claw ecosystem + 7 external frameworks)
- [x] External frameworks integration (SmolAgents, LangGraph, mcp-agent, CrewAI, AutoGen, Swarms, OpenAgents)
- [x] Multi-agent coordination trend research
- [x] Monthly ecosystem updates tracking (EN + ZH)
- [x] Cross-platform static analysis test framework (v2.1, 165/177 pass for 13 claw platforms)
- [x] Benchmark execution engine (v1.0, 182 metrics across 13 claw platforms)
- [x] Refined mission statement (personal vs enterprise paradigm analysis)
- [x] Claims verification (Hermes-Agent "self-improving" analysis)
- [x] Multi-agent coordination trend research
- [x] Monthly ecosystem updates tracking (EN + ZH)
- [x] Cross-platform static analysis test framework (v2.1, 165/177 pass)
- [x] Benchmark execution engine (v1.0, 182 metrics across 13 platforms)
- [x] Agent configuration schema and validation
- [x] Security privilege and rule enforcement
- [x] Comprehensive .gitignore for sensitive data protection
- [x] Bilingual documentation (English + Chinese)

### 🔄 In Progress
- [ ] Unified platform comparison (all 20 platforms in single document)
- [ ] Chinese translations (external_frameworks.zh-CN.md, MISSION.zh-CN.md, ROADMAP.zh-CN.md)

### 📋 Planned
- [ ] Cross-platform performance metrics (runtime benchmarks)
- [ ] MCP ecosystem deep-dive report
- [ ] Enterprise governance framework analysis
- [ ] 1PC (one-person company) case studies
- [ ] Runtime performance benchmarking extension

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

**Claw Ecosystem (13 platforms):**
- **Openclaw**: https://github.com/openclaw/openclaw
- **ClawTeam**: https://github.com/win4r/ClawTeam-OpenClaw
- **GoClaw**: https://github.com/nextlevelbuilder/goclaw
- **IronClaw**: https://github.com/nearai/ironclaw
- **Maxclaw**: https://github.com/Lichas/maxclaw
- **NanoClaw**: https://github.com/qwibitai/nanoclaw
- **Nanobot**: https://github.com/HKUDS/nanobot
- **Zeroclaw**: https://github.com/zeroclaw-labs/zeroclaw
- **HiClaw**: https://github.com/hiclaw-org/hiclaw
- **QuantumClaw**: https://github.com/quantumclaw/quantumclaw
- **Hermes-Agent**: https://github.com/NousResearch/hermes-agent
- **RTL-CLAW**: https://github.com/rtl-claw/rtl-claw
- **Claw-AI-Lab**: https://github.com/Claw-AI-Lab/Claw-AI-Lab

**External Frameworks (7 platforms):**
- **SmolAgents**: https://github.com/huggingface/smolagents
- **LangGraph**: https://github.com/langchain-ai/langgraph
- **mcp-agent**: https://github.com/lastmile-ai/mcp-agent
- **CrewAI**: https://github.com/crewaiinc/crewai
- **AutoGen**: https://github.com/microsoft/autogen
- **Swarms**: https://github.com/kyegomez/swarms
- **OpenAgents**: https://github.com/openagents-org/openagents

## 📞 Contact & Discussion

This project represents ongoing research into AI agent architectures. For discussions, questions, or collaboration opportunities, please refer to the individual platform repositories or create issues in this analysis repository.

**Full Documentation:**
- Mission: [docs/MISSION.md](docs/MISSION.md)
- Roadmap: [docs/ROADMAP.md](docs/ROADMAP.md)
- External Frameworks: [architecture/external_frameworks.md](architecture/external_frameworks.md)
- Latest Updates: [docs/LATEST_UPDATES.md](docs/LATEST_UPDATES.md)

---

*Last updated: May 5, 2026*