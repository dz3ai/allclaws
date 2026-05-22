# Agent Runtime Benchmark Results — 2026-05-21T08:3228

Engine v2.0.0-agent-runtime | 55 metrics across 13 platforms

## Toolchain

| Tool | Available |
|------|-----------|
| /usr/bin/time -v | true |
| cargo | true |
| node | true |
| go | false |
| python3 | true |

## Cold Start Time (ms)

| Platform | Cold Start (ms) | Notes |
|----------|-----------------|-------|
| ironclaw | 0 | binary not built |
| zeroclaw | 0 | binary not built |
| goclaw | 0 | binary not built |
| maxclaw | 0 | binary not built |
| openclaw | 66 | node parse time (no runtime init) |
| nanoclaw | 41 | node parse time (no runtime init) |
| quantumclaw | 71 | node parse time (no runtime init) |
| clawteam | 41 | python import clawteam |
| nanobot | 90 | python import nanobot |
| hermes-agent | 921 | python import run_agent |

## Memory Usage

| Platform | Idle (MB) | Active (MB) | Notes |
|----------|-----------|-------------|-------|
| openclaw | 38.7 |  |  |
| nanoclaw | 38.7 |  |  |
| quantumclaw | 38.7 |  |  |
| clawteam | 9.9 | 18.2 | bare python process |
| nanobot | 9.9 | 18.2 | bare python process |
| hermes-agent | 9.9 | 18.2 | bare python process |

## Binary / Installation Size

| Platform | Binary Size (KB) | Install Footprint (KB) | Notes |
|----------|------------------|------------------------|-------|
| ironclaw | 0 | 4 | target/ directory |
| zeroclaw | 0 | 4 | target/ directory |
| goclaw | 0 | 0 | no vendor/; go mod download proxy |
| maxclaw | 0 | 0 | no vendor/; go mod download proxy |
| openclaw | 0 | 0 | node_modules/ not installed |
| nanoclaw | 0 | 0 | node_modules/ not installed |
| quantumclaw | 0 | 0 | node_modules/ not installed |

## Response Latency (Echo Benchmark)

| Platform | Latency (ms) | Notes |
|----------|--------------|-------|
| openclaw | 19 | echo benchmark |
| nanoclaw | 22 | echo benchmark |
| quantumclaw | 20 | echo benchmark |
| clawteam | 12 | echo benchmark |
| nanobot | 12 | echo benchmark |
| hermes-agent | 12 | echo benchmark |

## Build Proxy Time

| Platform | Build Time (ms) | Notes |
|----------|----------------|-------|
| ironclaw | 188304 | cargo check |
| zeroclaw | 75374 | cargo check |
| goclaw | 0 | go toolchain not available |
| maxclaw | 0 | go toolchain not available |

## All Metrics (Raw)

| Platform | Metric | Value | Unit | Notes |
|----------|--------|-------|------|-------|
| ironclaw | binary_size | 0 | KB | no target/release (not built)
 |
| ironclaw | install_footprint | 4 | KB | target/ directory
 |
| ironclaw | build_proxy_time | 188304 | ms | cargo check
 |
| ironclaw | cold_start_time | 0 | ms | binary not built
 |
| zeroclaw | binary_size | 0 | KB | no target/release (not built)
 |
| zeroclaw | install_footprint | 4 | KB | target/ directory
 |
| zeroclaw | build_proxy_time | 75374 | ms | cargo check
 |
| zeroclaw | cold_start_time | 0 | ms | binary not built
 |
| goclaw | binary_size | 0 | KB | not built
 |
| goclaw | install_footprint | 0 | KB | no vendor/; go mod download proxy
 |
| goclaw | build_proxy_time | 0 | ms | go toolchain not available
 |
| goclaw | mod_download_time | 0 | ms | go toolchain not available
 |
| goclaw | cold_start_time | 0 | ms | binary not built
 |
| maxclaw | binary_size | 0 | KB | not built
 |
| maxclaw | install_footprint | 0 | KB | no vendor/; go mod download proxy
 |
| maxclaw | build_proxy_time | 0 | ms | go toolchain not available
 |
| maxclaw | mod_download_time | 0 | ms | go toolchain not available
 |
| maxclaw | cold_start_time | 0 | ms | binary not built
 |
| openclaw | install_footprint | 0 | KB | node_modules/ not installed
 |
| openclaw | npm_deps | 73 | deps |  |
| openclaw | binary_size | 0 | KB | no dist/ or build/ directory
 |
| openclaw | cold_start_time | 66 | ms | node parse time (no runtime init)
 |
| openclaw | response_latency_ms | 19 | ms | echo benchmark
 |
| openclaw | memory_idle_mb | 38.7 | MB |  |
| nanoclaw | install_footprint | 0 | KB | node_modules/ not installed
 |
| nanoclaw | npm_deps | 19 | deps |  |
| nanoclaw | binary_size | 0 | KB | no dist/ or build/ directory
 |
| nanoclaw | cold_start_time | 41 | ms | node parse time (no runtime init)
 |
| nanoclaw | response_latency_ms | 22 | ms | echo benchmark
 |
| nanoclaw | memory_idle_mb | 38.7 | MB |  |
| quantumclaw | install_footprint | 0 | KB | node_modules/ not installed
 |
| quantumclaw | npm_deps | 12 | deps |  |
| quantumclaw | binary_size | 0 | KB | no dist/ or build/ directory
 |
| quantumclaw | cold_start_time | 71 | ms | node parse time (no runtime init)
 |
| quantumclaw | response_latency_ms | 20 | ms | echo benchmark
 |
| quantumclaw | memory_idle_mb | 38.7 | MB |  |
| clawteam | py_deps | 19 | deps |  |
| clawteam | install_footprint | 38912 | KB | estimated (19 deps x ~2MB)
 |
| clawteam | cold_start_time | 41 | ms | python import clawteam
 |
| clawteam | response_latency_ms | 12 | ms | echo benchmark
 |
| clawteam | memory_idle_mb | 9.9 | MB | bare python process
 |
| clawteam | memory_active_mb | 18.2 | MB | python + stdlib modules
 |
| nanobot | py_deps | 84 | deps |  |
| nanobot | install_footprint | 172032 | KB | estimated (84 deps x ~2MB)
 |
| nanobot | cold_start_time | 90 | ms | python import nanobot
 |
| nanobot | response_latency_ms | 12 | ms | echo benchmark
 |
| nanobot | memory_idle_mb | 9.9 | MB | bare python process
 |
| nanobot | memory_active_mb | 18.2 | MB | python + stdlib modules
 |
| hermes-agent | py_deps | 49 | deps |  |
| hermes-agent | install_footprint | 100352 | KB | estimated (49 deps x ~2MB)
 |
| hermes-agent | cold_start_time | 921 | ms | python import run_agent
 |
| hermes-agent | response_latency_ms | 12 | ms | echo benchmark
 |
| hermes-agent | memory_idle_mb | 9.9 | MB | bare python process
 |
| hermes-agent | memory_active_mb | 18.2 | MB | python + stdlib modules
 |
| rtl-claw | runtime_benchmarks | 0 | N/A | hardware description language, no runtime
 |

## Skipped Platforms

- **hiclaw**: no go.mod found
- **claw-ai-lab**: no pyproject.toml or requirements.txt
- **rtl-claw**: build-tool only — no runtime agent metrics applicable

Full JSON: `/home/dannyz/src/github/allclaws/test_framework/benchmark_results/2026-05-21T08:3228-agent-runtime/agent_runtime_benchmark_results.json`
