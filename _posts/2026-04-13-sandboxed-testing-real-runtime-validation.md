---
layout: post
title: "Beyond Static Analysis: Real Sandbox Testing for 13 AI Agent Platforms"
date: 2026-04-13 21:00:00 +0800
author: Danny Zeng
categories: [testing]
tags: [AllClaws, sandbox-testing, docker, podman, runtime-validation, test-framework]
---

## Executive Summary

Static analysis tells you what *should* work. Sandbox testing reveals what *actually* works.

Today, we expanded the AllClaws test framework beyond static checks into **real runtime validation** using Docker/Podman sandboxes. This shift uncovered critical environment issues that static analysis cannot detect—version mismatches, build failures, and configuration problems that only appear when you actually run the code.

**Key Findings:**
- **Go version mismatch**: goclaw requires Go 1.26.0, sandbox has 1.23.12
- **Rust edition2024**: Requires Rust 1.84+, old `rust:1.80-alpine` images don't support it
- **Volume mount paths**: `./platform` in docker-compose.yml resolves to test_framework/platform, not allclaws/platform
- **Read-only mounts**: Source mounted as `:ro` prevents `cargo build` from writing target/

This post covers the sandbox testing framework we built, the issues we discovered, and how we fixed them.

---

## Why Sandbox Testing Matters

### The Static Analysis Limitation

Our existing test framework performed comprehensive static analysis:
- Source file presence (count by language)
- Lockfiles (package-lock.json, Cargo.lock, go.sum)
- CI/CD configuration (.github/workflows)
- Documentation (README, LICENSE, CHANGELOG)

**Problem:** A green checkmark on static analysis doesn't mean the code actually runs.

### What We Were Missing

| Static Analysis Says | Sandbox Reality |
|---------------------|-----------------|
| ✅ Cargo.toml exists | ❌ Rust edition2024 requires 1.84+, container has 1.80 |
| ✅ go.mod present | ❌ go.mod requires 1.26.0, container has 1.23.12 |
| ✅ Dockerfile exists | ❌ Volume mount points to wrong directory |
| ✅ src/**/*.rs files | ❌ Read-only mount prevents compilation |

**The gap:** Static analysis validates *presence*. Sandbox testing validates *execution*.

---

## The Sandbox Testing Framework

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    GitHub Actions (CI/CD)                    │
│  - Static analysis tests                                      │
│  - Benchmark metrics                                          │
│  + NEW: Sandbox runtime tests                                 │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                  Docker/Podman Compose                       │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            │
│  │ zeroclaw    │  │ goclaw      │  │ openclaw    │            │
│  │ (Rust)      │  │ (Go)        │  │ (Node:22)   │            │
│  └─────────────┘  └─────────────┘  └─────────────┘            │
│  Source: ../platform (read-only)                               │
│  Build output: Named volume (writable)                         │
└─────────────────────────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                    Findings Capture                           │
│  - JSON: structured data for automation                       │
│  - Markdown: human-readable report                            │
│  - results/latest/: symlink to newest results                 │
└─────────────────────────────────────────────────────────────┘
```

### The Script: `run_sandbox_runtime_tests.sh`

We created a new script that:

1. **Auto-detects container runtime** (podman or docker)
2. **Runs language-specific tests**:
   - Rust: `cargo check`, edition2024 validation
   - Go: `go build`, version comparison
   - Python: Module import, pytest detection
   - TypeScript: package.json validation, node_modules check
3. **Captures findings** as JSON + Markdown
4. **Categorizes by severity**: critical, error, warning, success

---

## Today's Key Findings

### 1. Volume Mount Path Resolution

**The Bug:**

```yaml
# docker-compose.yml (WRONG)
volumes:
  - ./zeroclaw:/workspace:ro
```

**What Happens:**
- Working directory: `/home/dannyz/src/github/allclaws/test_framework`
- `./zeroclaw` resolves to: `/home/dannyz/src/github/allclaws/test_framework/zeroclaw` (empty)
- Actual code is at: `/home/dannyz/src/github/allclaws/zeroclaw`

**The Fix:**

```yaml
# docker-compose.yml (CORRECT)
volumes:
  - ../zeroclaw:/workspace:ro
```

**Lesson Learned:** Docker Compose volume paths resolve relative to the *working directory* at runtime, not the location of the docker-compose.yml file.

### 2. Rust Edition2024 Compatibility

**The Error:**
```
error: edition 2024 is unstable and requires -Z unstable-options
```

**Root Cause:**
- ZeroClaw uses `edition = "2024"` in Cargo.toml
- Sandbox image: `rust:1.80-alpine`
- Edition 2024 requires Rust 1.84+

**The Fix:**

```yaml
# docker-compose.yml
zeroclaw-sandbox:
  image: rust:alpine  # Was: rust:1.80-alpine
```

**Impact:** Applied to all Rust platforms (zeroclaw, ironclaw)

### 3. Read-Only Mount + Build Outputs

**The Error:**
```
error: could not write to /workspace/target: Read-only file system
```

**Root Cause:** Source mounted as `:ro` for security, but `cargo build` needs to write `target/`

**The Fix:**

```yaml
# docker-compose.yml
zeroclaw-sandbox:
  volumes:
    - ../zeroclaw:/workspace:ro           # Source: read-only
    - zeroclaw-target:/workspace/target    # Build output: writable volume
```

**Result:** Source stays protected, builds can write to named volume.

### 4. Go Version Mismatch

**The Finding:**
```
goclaw/go.mod: requires go 1.26.0
sandbox image: golang:1.23-alpine
```

**Status:** Documented as finding, not fixed (would require updating base image)

**Action:** Update docker-compose.yml to `golang:1.26-alpine` or `golang:latest`

---

## Platform-by-Platform Results

### Rust Platforms (zeroclaw, ironclaw)

| Check | Result | Notes |
|-------|--------|-------|
| Container running | ✅ | Podman on WSL2 |
| Rust version | ✅ | Latest via `rust:alpine` |
| Edition 2024 support | ✅ | After image update |
| Cargo check | ⚠️ | Requires web/dist/ for RustEmbed |

### Go Platforms (goclaw, maxclaw, hiclaw)

| Check | Result | Notes |
|-------|--------|-------|
| Container running | ✅ | |
| Go version | ⚠️ | goclaw needs 1.26+, has 1.23 |
| go build | ⚠️ | Version mismatch blocks compile |

### TypeScript Platforms (openclaw, nanoclaw, quantumclaw)

| Check | Result | Notes |
|-------|--------|-------|
| Container running | ✅ | |
| Node version | ✅ | v22 via `node:22-alpine` |
| package.json | ✅ | |
| node_modules | ⚠️ | Read-only mount prevents npm install |

### Python Platforms (clawteam, nanobot, claw-ai-lab, hermes-agent)

| Check | Result | Notes |
|-------|--------|-------|
| Container running | ✅ | |
| Python version | ✅ | 3.11 via `python:3.11-slim` |
| pytest | ⚠️ | Not installed in base image |
| Module import | ✅ | |

---

## Framework Updates

### New Script Structure

```
test_framework/scripts/
├── run_sandboxed_tests.sh      # Main orchestrator (updated)
├── run_sandbox_runtime_tests.sh # NEW: Runtime testing
├── run_tests.sh                 # Static analysis (unchanged)
└── run_benchmarks.sh            # Benchmark metrics (unchanged)
```

### Integration Flow

```bash
# 1. Static analysis (existing)
bash scripts/run_tests.sh [platform...]

# 2. Benchmarks (existing)
bash scripts/run_benchmarks.sh [platform...]

# 3. Sandbox runtime tests (NEW)
bash scripts/run_sandbox_runtime_tests.sh [platform...]

# 4. All at once (orchestrator)
bash scripts/run_sandboxed_tests.sh [platform...]
```

### Results Capture

```
test_framework/results/
└── 2026-04-13T22:0647/
    ├── results.json           # Static analysis results
    ├── results.md             # Human-readable summary
    └── sandbox_findings.md    # NEW: Runtime findings
```

---

## Container Runtime: Docker vs Podman

### Why Podman?

The framework auto-detects available container runtimes:

```bash
# Prefer Podman if available
if command -v podman >/dev/null 2>&1; then
    CONTAINER_CMD="podman"
    COMPOSE_CMD="podman-compose"
fi
```

**Podman advantages:**
- Daemonless architecture (no root daemon)
- Better OCI compliance
- Native systemd integration
- Compatible with Docker CLI

**WSL2 Notes:**
- Podman on WSL2 requires `podman.socket` service
- Volume paths work the same as Docker
- `podman-compose` behaves identically to `docker-compose`

---

## What We Learned

### 1. Static Analysis ≠ Runtime Validation

You can't `grep` your way to runtime correctness. Real execution reveals:
- Version incompatibilities
- Missing build artifacts
- Filesystem permission issues
- Network connectivity problems

### 2. Docker Compose Path Resolution is Tricky

Relative paths in docker-compose.yml resolve from **working directory**, not **compose file location**. This caught us because:

```bash
# We run tests from here:
cd /home/dannyz/src/github/allclaws/test_framework

# But compose file is here:
/home/dannyz/src/github/allclaws/test_framework/docker-compose.yml

# And source code is here:
/home/dannyz/src/github/allclaws/zeroclaw

# So ./zeroclaw becomes:
/home/dannyz/src/github/allclaws/test_framework/zeroclaw  # WRONG
```

### 3. Latest ≠ Stable

Using `rust:alpine` (latest) instead of `rust:1.80-alpine` (pinned) gave us edition2024 support. But it also means:
- ✅ Always supports newest Rust features
- ⚠️ Reproducibility varies over time
- ⚠️ CI may behave differently than local

**Recommendation:** Pin major versions (`rust:1-alpine`), let patch auto-update.

### 4. Read-Only Mounts Need Careful Planning

Mounting source as `:ro` is good for security, but:
- Build outputs need writable volumes
- `node_modules` can't be created
- Lockfiles can't be updated

**Pattern:** Read-only source + named volume for outputs

---

## Updated Documentation

All documentation has been refreshed:

### README.md (EN + ZH)

- Updated to reflect actual framework structure
- Added all 13 platforms with container images
- Documented new `run_sandbox_runtime_tests.sh`
- Added Docker/Podman auto-detection notes

### sandboxes-testing-guide.md (ZH)

- Comprehensive sandbox testing workflow
- Container runtime comparison
- Troubleshooting common issues

### Memory: test_framework_skills.md

Captured lessons learned:
- Docker Compose volume paths
- Podman WSL2 considerations
- Rust edition2024 requirements
- Read-only mount patterns

---

## Next Steps

### Immediate (This Week)

1. **Fix Go version mismatch**: Update goclaw sandbox to `golang:1.26-alpine`
2. **Add RustEmbed web/dist detection**: Warn when folder is missing before build
3. **Run full suite**: Test all 13 platforms with runtime validation
4. **CI integration**: Add sandbox tests to GitHub Actions

### Short Term (April)

1. **Multi-stage builds**: Use builder pattern for TypeScript platforms
2. **Dependency caching**: Speed up builds with volume caches
3. **Network tests**: Verify MCP server connectivity in sandbox
4. **Performance metrics**: Measure container startup, build times

### Long Term (May+)

1. **Cross-platform agent federation**: Can agents from different platforms work together?
2. **Security audit**: Comparative vulnerability assessment
3. **Cost optimization**: Token efficiency across platforms
4. **Real-world benchmarks**: Runtime performance metrics

---

## How to Run Sandbox Tests

### Quick Start

```bash
cd test_framework

# Test all 13 platforms
bash scripts/run_sandbox_runtime_tests.sh

# Test specific platforms only
bash scripts/run_sandbox_runtime_tests.sh goclaw zeroclaw openclaw

# View findings
cat results/latest/sandbox_findings.md
```

### Requirements

```bash
# Ubuntu/Debian
sudo apt install jq docker.io docker-compose

# macOS
brew install jq docker docker-compose

# With Podman (recommended)
sudo apt install jq podman podman-compose
```

---

## Conclusion

Static analysis is a good starting point, but it can't catch runtime issues. Today's sandbox testing uncovered critical problems that were invisible to `grep` and `find`:

- **Version mismatches** that block compilation
- **Volume path issues** that mount empty directories
- **Filesystem permissions** that prevent builds

**The big picture:** If you're not running your code in an environment similar to production, you're not really testing it. Static analysis gives you confidence; sandbox testing gives you certainty.

**What this means for the AllClaws ecosystem:** We now have a framework that validates both *presence* and *execution*. The 13 platforms we track will be tested not just for having the right files, but for actually working in containerized environments.

**Next update:** May 2026 (First Monday of May)

---

*This research is made possible by the open source community. The sandbox testing framework is available at [github.com/dz3ai/allclaws](https://github.com/dz3ai/allclaws).*

*Methodology: We test 13 AI agent platforms through static analysis (139 tests), benchmark metrics (181 data points), and sandbox runtime validation (containerized execution). Full research available in our GitHub repository.*
