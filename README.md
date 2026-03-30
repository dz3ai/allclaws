# AllClaws: Personal AI Agent Ecosystem Analysis & Testing

**[中文](README-zh_CN.md)** | English

**AllClaws** is a comprehensive research and development project focused on analyzing, comparing, and testing personal AI agent platforms. This umbrella project brings together architecture analysis, performance benchmarking, and thought leadership in the personal AI assistant space.

## 🎯 Mission

To advance the field of personal AI assistants by:
- **Analyzing** existing platforms' architectures and design decisions
- **Benchmarking** functionality and performance across different implementations
- **Developing** testing frameworks for objective comparison
- **Sharing** insights through technical writing and documentation

## 🔥 Cross-Cutting Trends (March 2026)

Based on tracking 8 platforms, three dominant trends emerged this month:

1. **Security was the top priority** — OpenClaw disclosed critical CVEs (RCE, sandbox bypass), NanoClaw partnered with Docker for container-first security, Nanobot removed litellm over supply chain concerns, IronClaw patched 5 critical vulnerabilities.
2. **Streaming became table stakes** — every active project shipped end-to-end streaming from provider to channel.
3. **Multi-provider LLM expansion** — Codex OAuth, GitHub Copilot, Gemini, AWS Bedrock, and more were added across the board.

See [Latest Updates: March 2026](docs/LATEST_UPDATES.md) for full details.

## 📋 Current Work in Progress

### 1. Architecture Analysis & Comparison
**Status:** ✅ Active Development

Comprehensive analysis of personal AI agent platforms including:

- **Openclaw** (TypeScript): Extensible CLI with multi-channel support
- **ClawTeam** (Python-based): Multi-agent swarm coordination with leader-worker orchestration, git worktree isolation, and inter-agent messaging
- **GoClaw** (Go-based): Multi-agent AI gateway with teams, orchestration, and multi-tenant PostgreSQL
- **IronClaw** (Rust-based): Secure personal AI assistant with WASM sandboxing and defense-in-depth security
- **Maxclaw** (Go-based): OpenClaw-style local-first agent with desktop UI, low memory footprint, and monorepo-aware context discovery
- **NanoClaw** (Node.js): WhatsApp-focused assistant with containerized agents
- **Nanobot** (Python-based): Ultra-lightweight personal AI assistant with ~4,000 LOC core code
- **Zeroclaw** (Rust-based): High-performance runtime with trait-driven architecture

**Key Deliverables:**
- `docs/LATEST_UPDATES.md` - Latest project updates and ecosystem trends (monthly)
- `architecture/architecture_comparison.md` - Detailed technical analysis (8 platforms)
- `architecture/architecture_comparison.zh-CN.md` - Chinese translation
- `architecture/multi_agent_coordination_research.md` - Multi-agent coordination trend analysis (EN + ZH)
- Platform capability matrices and trade-off analysis

### 2. Personal Agent Test Framework
**Status:** ✅ v2.0 — Cross-Platform Static Analysis Complete

A testing framework that scans all 8 platform submodules and records results systematically.

**Run tests:**
```bash
cd test_framework
bash scripts/run_tests.sh
```

**Latest Results (March 29, 2026): 93 pass / 9 fail / 102 total**

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

**What gets tested per platform:**
- **Language-level**: build manifest, lockfile, source file count, CI config, clippy/deny (Rust), Makefile (Go)
- **Project health**: LICENSE, README, CHANGELOG, CONTRIBUTING, .gitignore, CI workflows
- **Output**: timestamped JSON + Markdown reports in `test_framework/results/`

### 3. Benchmark Engine
**Status:** ✅ v1.0 — Cross-Platform Metrics Collection Complete

A pure-external benchmark engine that measures repository characteristics across all 8 platforms without requiring builds or runtime dependencies.

**Run benchmarks:**
```bash
cd test_framework
bash scripts/run_benchmarks.sh
```

**Latest Results (March 30, 2026): 112 metrics across 8 platforms**

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
- [x] Architecture analysis of 8 major platforms (Openclaw, ClawTeam, GoClaw, IronClaw, Maxclaw, NanoClaw, Nanobot, Zeroclaw)
- [x] Multi-agent coordination trend research
- [x] Monthly ecosystem updates tracking (EN + ZH)
- [x] Cross-platform static analysis test framework (v2.0, 93/102 pass)
- [x] Benchmark execution engine (v1.0, 112 metrics across 8 platforms)
- [x] Agent configuration schema and validation
- [x] Security privilege and rule enforcement
- [x] Comprehensive .gitignore for sensitive data protection
- [x] Bilingual documentation (English + Chinese)

### 🔄 In Progress
- [ ] Cross-platform performance metrics (runtime benchmarks)
- [ ] Extended test coverage (networking, file operations)
- [ ] Real-world agent integration testing

### 📋 Planned
- [ ] Web-based dashboard for test results
- [ ] Automated CI/CD pipeline for testing
- [ ] Additional platform support (custom agents)
- [ ] Performance regression detection
- [ ] Security vulnerability testing

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

- **Openclaw**: https://github.com/openclaw/openclaw
- **ClawTeam**: https://github.com/win4r/ClawTeam-OpenClaw
- **GoClaw**: https://github.com/nextlevelbuilder/goclaw
- **IronClaw**: https://github.com/nearai/ironclaw
- **Maxclaw**: https://github.com/Lichas/maxclaw
- **NanoClaw**: https://github.com/qwibitai/nanoclaw
- **Nanobot**: https://github.com/HKUDS/nanobot
- **Zeroclaw**: https://github.com/zeroclaw-labs/zeroclaw

## 📞 Contact & Discussion

This project represents ongoing research into personal AI agent architectures. For discussions, questions, or collaboration opportunities, please refer to the individual platform repositories or create issues in this analysis repository.

---

*Last updated: March 30, 2026*