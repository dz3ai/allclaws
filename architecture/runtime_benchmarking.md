# Runtime Performance Benchmarking: Methodology & Results

**[中文](runtime_benchmarking.zh-CN.md)** | English

> Framework for reproducible runtime performance measurement across AI agent platforms. Covers source complexity metrics, build timing, import resolution speed, container image estimation, and documented methodology for metrics requiring LLM API access. May 2026.

---

## Executive Summary

Runtime performance benchmarking of AI agent platforms has two tiers:

1. **Tier 1 (Automated):** Metrics measurable without LLM access — source complexity, dependency counts, build/check timing, import resolution speed, container image estimation.
2. **Tier 2 (Manual methodology):** Metrics requiring LLM API access — cold start to first response, memory usage, response latency (p50/p95/p99), token efficiency.

This document delivers Tier 1 results from May 7, 2026 and documents the Tier 2 protocol for future measurement.

---

## Part 1: Tier 1 Results

### Rust Platforms

| Platform | Source Files | Dependencies | Cargo Check Time | Dockerfile |
|----------|-------------|-------------|-----------------|------------|
| **IronClaw** | 838 .rs | 56 cargo | 959.6s (~16 min) | Yes |
| **ZeroClaw** | 710 .rs | 60 cargo | Failed | No |

### Go Platforms (Go toolchain unavailable)

| Platform | Source Files | Dependencies | Go Version | Dockerfile |
|----------|-------------|-------------|-----------|------------|
| **GoClaw** | 1,721 .go | 203 go mod | 1.26.0 | Yes |
| **Maxclaw** | 129 .go | 33 go mod | 1.24.0 | No |
| **HiClaw** | 151 .go | N/A | N/A | Yes |

### TypeScript Platforms

| Platform | Source Files | Dependencies | Dockerfile |
|----------|-------------|-------------|------------|
| **OpenClaw** | 14,505 .ts | 82 npm | Yes |
| **NanoClaw** | 225 .ts | 19 npm | Yes |
| **QuantumClaw** | 0 .ts | 12 npm | No |

### Python Platforms

| Platform | Source Files | Dependencies | Import Time | Python CI |
|----------|-------------|-------------|------------|-----------|
| **ClawTeam** | 92 .py | 19 pip | 204ms | Yes |
| **Nanobot** | 263 .py | 80 pip | 21ms | Yes |
| **Hermes-Agent** | 1,441 .py | 63 pip | 21ms | Yes |

### Cross-Language Averages

| Language | Avg Source Files | Avg Dependencies | Dockerfile Rate |
|----------|-----------------|-----------------|-----------------|
| Rust | 774 | 58 | 50% |
| Go | 667 | 118 | 67% |
| TypeScript | 4,910 | 38 | 67% |
| Python | 449 | 54 | 75% |

### Source Complexity Top 5

| Rank | Platform | Source Files | Language |
|------|----------|-------------|----------|
| 1 | OpenClaw | 14,505 | TypeScript |
| 2 | GoClaw | 1,721 | Go |
| 3 | Hermes-Agent | 1,441 | Python |
| 4 | IronClaw | 838 | Rust |
| 5 | ZeroClaw | 710 | Rust |

---

## Part 2: Tier 2 Methodology

For metrics requiring live LLM access:

**Cold Start Time:** `time (agent-cli --version)` for binary; `time (agent-cli --prompt "ping" | grep -m1 response)` for first response. Target platforms: GoClaw, IronClaw, ZeroClaw, Maxclaw, OpenClaw, Nanobot.

**Memory Usage:** RSS via `ps -o rss=` at idle (5s after launch) and under load (during tool execution). Compare Rust vs Go vs Node.js vs Python memory baselines.

**Response Latency:** 100 iterations of fixed prompt ("What is 2+2?") with warmup. Measure time to first token. Calculate p50/p95/p99 from distribution.

**Token Efficiency:** 5 standard tasks across platforms, same LLM model. Measure input tokens (prompt + context + tool schemas) and output tokens. Calculate efficiency = output/input.

---

## Part 3: Recommendations

- **Source file count proxies complexity, not quality.** OpenClaw's 14,505 files deliver 37+ channels; NanoClaw's 225 files deliver WhatsApp-to-Claude bridging.
- **Dependency count correlates with attack surface.** GoClaw (203 deps) and Nanobot (80 deps) should prioritize supply chain auditing.
- **Dockerfile presence is high (67%).** Containerization is now table stakes for reproducible deployment.
- **Cold start matters for CLI agents, less for daemons.** Choose Rust/Go binaries for per-task invocation; Python/Node.js for long-running services.

---

## See Also

- [Unified Platform Comparison](platform_comparison.md) — Full architecture comparison
- [Test Framework](../test_framework/) — Static analysis results
- [ROADMAP: Q4 2026](../docs/ROADMAP.md) — Performance benchmarking target

---

*Last updated: May 7, 2026*
*Toolchains available: cargo, node, python3, docker (Go missing)*
*Part of: AllClaws Personal AI Agent Ecosystem Research*
