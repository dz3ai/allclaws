# Runtime Benchmark Methodology

This document explains how the AllClaws agent runtime benchmark system works, what each metric measures, and how to interpret the results.

## Overview

The agent runtime benchmark engine (`scripts/run_agent_runtime_benchmarks.sh`) measures **runtime performance characteristics** of each AllClaws platform. Unlike the static analysis benchmarks (`run_benchmarks.sh`) which measure code size and structure, these benchmarks capture how the platform performs when actually invoked.

## Running the Benchmarks

```bash
cd test_framework/
./scripts/run_agent_runtime_benchmarks.sh
```

Results are written to `benchmark_results/<timestamp>-agent-runtime/` as both JSON and Markdown.

## Metrics Explained

### Cold Start Time (`cold_start_time_ms`)

**What it measures:** Time from invoking the platform's CLI entry point to the process completing its initial startup.

**How it's measured:**
- **Rust platforms** (`ironclaw`, `zeroclaw`): `time <binary> --help` — measures process spawn + argument parsing.
- **Go platforms** (`goclaw`, `maxclaw`, `hiclaw`): Same approach if a pre-built binary exists.
- **TypeScript platforms** (`openclaw`, `nanoclaw`, `quantumclaw`): `node -e "require('src/index.ts')"` — measures Node.js startup + module parse time (not full runtime init, since TypeScript requires transpilation).
- **Python platforms** (`clawteam`, `nanobot`, `hermes-agent`, `claw-ai-lab`): `python3 -c "import <module>"` — measures interpreter startup + module import.

**Limitations:**
- Does not include LLM API call time (no network requests are made).
- TypeScript platforms only measure Node.js parse time, not the full compiled runtime.
- Python platforms only measure import, not the full agent initialization (which may load configs, connect to databases, etc.).

### Memory Usage (`memory_idle_mb`, `memory_active_mb`)

**What it measures:**
- **Idle:** Peak RSS (Resident Set Size) of a minimal process invocation.
- **Active:** Peak RSS after loading common stdlib modules (json, os, re, pathlib, etc.).

**How it's measured:** Uses `/usr/bin/time -v` to capture "Maximum resident set size" from the kernel. Falls back to `ps -o rss` polling if `/usr/bin/time -v` is unavailable (Linux/GNU only).

**Limitations:**
- Idle memory reflects the bare runtime, not the full agent with all dependencies loaded.
- Active memory only loads stdlib modules, not third-party packages (which often dominate real-world RSS).
- Measurements are single-point, not averaged over multiple runs.
- RSS values include shared library pages that may be overcounted across processes.

### Response Latency (`response_latency_ms`)

**What it measures:** Time-to-first-output for a trivial echo command. This is a proxy for the overhead of spawning the runtime and producing output, not actual LLM response time.

**How it's measured:**
- **Python:** `time python3 -c "sys.stdout.write('READY\n'); sys.stdout.flush()"`
- **Node.js:** `time node -e "console.log('READY'); process.exit(0)"`

**Limitations:**
- This is a minimal benchmark that measures runtime spawn + stdout write, not actual LLM response latency.
- Real-world latency depends on the LLM provider, network conditions, prompt complexity, and context length.
- P50/P95/P99 percentiles are not measured — only a single-shot timing.

### Token Efficiency (`token_efficiency_ratio`)

**What it measures:** Output tokens generated divided by input tokens consumed (output/input ratio).

**How it's measured:** Currently not implemented. This would require actual LLM API calls with a standardized prompt, which is outside the scope of local benchmarking. This metric is reserved for future integration with the eval/test suite.

### Binary Size (`binary_size_kb`)

**What it measures:** Size of the compiled binary or build output.

**How it's measured:**
- **Rust:** `du -k target/release/<binary>` — release build binary.
- **Go:** `du -k bin/<binary>` or any executable found in the project.
- **TypeScript:** `du -k dist/` or `du -k build/` — compiled JS output.
- **Python:** Not directly applicable (interpreted). Install footprint is used instead.

### Installation Size (`install_size_kb`)

**What it measures:** Total disk footprint of dependencies/build artifacts.

**How it's measured:**
- **Rust:** `du -k target/` — full build cache.
- **Go:** `du -k vendor/` — vendored dependencies (if vendored).
- **TypeScript:** `du -k node_modules/` — npm-installed packages.
- **Python:** `du -k .venv/` or `du -k venv/` — virtual environment. Estimated from dependency count if no venv exists (~2MB per dep average).

### Build Proxy Time (`build_proxy_time_ms`)

**What it measures:** Time for a fast build-check command. Used as a proxy for compilation speed since full builds are too slow for regular benchmarking.

**How it's measured:**
- **Rust:** `cargo check` — type-checks without producing binaries.
- **Go:** `go vet ./...` — static analysis; falls back to `go build -o /dev/null` if vet fails.

### Module Download Time (`mod_download_time_ms`)

**What it measures:** Time to download dependencies (with cache).

**How it's measured:** `go mod download` for Go platforms. For other platforms, npm/pip equivalents are not measured to avoid side effects.

## Platform Coverage

| Platform | Language | Cold Start | Memory | Binary Size | Install Size | Build Proxy |
|----------|----------|------------|--------|-------------|--------------|-------------|
| ironclaw | Rust | Yes (if built) | Yes | Yes | Yes | Yes |
| zeroclaw | Rust | Yes (if built) | Yes | Yes | Yes | Yes |
| openclaw | TypeScript | Yes (parse) | Yes | dist/ | node_modules/ | No |
| nanoclaw | TypeScript | Yes (parse) | Yes | dist/ | node_modules/ | No |
| quantumclaw | TypeScript | Yes (parse) | Yes | build/ | node_modules/ | No |
| goclaw | Go | Yes (if built) | Yes | Yes | vendor/ | Yes |
| maxclaw | Go | Yes (if built) | Yes | Yes | vendor/ | Yes |
| hiclaw | Go | Yes (if built) | Yes | Yes | vendor/ | Yes |
| clawteam | Python | Yes (import) | Yes | N/A | venv/ | N/A |
| nanobot | Python | Yes (import) | Yes | N/A | venv/ | N/A |
| hermes-agent | Python | Yes (import) | Yes | N/A | venv/ | N/A |
| claw-ai-lab | Python | Yes (import) | Yes | N/A | est. | N/A |
| rtl-claw | Verilog | Skipped | Skipped | Skipped | Skipped | Skipped |

## Toolchain Dependencies

| Tool | Required For | Fallback |
|------|-------------|----------|
| `jq` | JSON report generation | Markdown-only output |
| `python3` | Startup timing, memory measurement | Skip Python metrics |
| `/usr/bin/time -v` | Accurate RSS measurement | `ps -o rss` polling |
| `cargo` | Rust build proxy | Skip build time |
| `node` | TypeScript startup timing | Skip TS cold start |
| `go` | Go build proxy, mod download | Skip Go build time |

The script is designed to **never fail** — missing toolchains result in skipped measurements with notes, not errors.

## Interpretation Guide

- **Cold start < 500ms:** Excellent for CLI tools. Most agent CLIs target < 1s.
- **Cold start 500ms–2s:** Acceptable for complex agent frameworks.
- **Cold start > 2s:** May indicate heavy initialization (DB connections, large module loading).
- **Idle memory < 50MB:** Very lean runtime.
- **Idle memory 50–200MB:** Typical for agent frameworks with moderate dependencies.
- **Idle memory > 200MB:** Heavy framework — may need optimization for constrained environments.
- **Install size < 100MB:** Minimal footprint.
- **Install size 100–500MB:** Typical for frameworks with many dependencies.
- **Install size > 500MB:** Heavy — consider whether all dependencies are necessary.

## Limitations

1. **No LLM API calls:** These benchmarks measure local runtime behavior only. Actual agent performance depends heavily on the LLM provider, model, and network latency.

2. **Single-shot measurements:** Each metric is measured once, not averaged. Results may vary between runs due to system load, filesystem cache, etc.

3. **Build state dependent:** Binary size and cold start measurements require pre-built artifacts. If platforms haven't been built, those metrics are skipped.

4. **Environment dependent:** Results vary by OS, CPU, disk speed, and system load. For reproducible comparisons, run on the same machine under similar conditions.

5. **Import-time != runtime-time:** Python and Node.js cold start measures import/parse time, not the full agent initialization which may include database connections, config loading, and more.

6. **Memory measurement precision:** `/usr/bin/time -v` reports peak RSS, which includes shared pages. On Linux, shared library pages counted by RSS may be shared between processes, overcounting total memory use.
