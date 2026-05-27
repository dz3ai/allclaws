# Runtime Benchmark Results — 2026-05-23T16-11-44

Engine v3.0.0 | 59 metrics across 12 platforms

## Toolchain

| Tool | Available |
|------|-----------|
| python3 | true |
| cargo | true |
| node | true |
| go | true |
| docker | true |
| podman | true |
| ps | true |
| time_v | true |

## Cold Start Time (ms)

| Platform | Cold Start (ms) | Notes |
|----------|-----------------|-------|
| clawteam | 7.65 | python import clawteam |
| goclaw | 0 | binary not built |
| hermes-agent | 509.33 | python from run_agent import main |
| ironclaw | 0 | binary not built |
| maxclaw | 0 | binary not built |
| nanobot | 267.28 | python import nanobot |
| nanoclaw | 64.91 | node parse time (no runtime init) |
| openclaw | 75.15 | node parse time (no runtime init) |
| openhuman | 0 | binary not built |
| quantumclaw | 74.99 | node parse time (no runtime init) |
| zeroclaw | 0 | binary not built |

## Memory Usage

| Platform | Idle (MB) | Active (MB) | Notes |
|----------|-----------|-------------|-------|
| clawteam | 11.6 | 9.0 | bare python process |
| hermes-agent | 11.6 | 45.9 | bare python process |
| nanobot | 11.5 | 49.3 | bare python process |
| nanoclaw | 38.5 | 0 |  |
| openclaw | 38.4 | 0 |  |
| quantumclaw | 38.6 | 0 |  |

## Binary / Installation Size

| Platform | Binary Size (KB) | Install Footprint (KB) | Notes |
|----------|------------------|------------------------|-------|
| goclaw | 0 | 0 | no vendor/; go mod download pr |
| ironclaw | 0 | 3831495 | target/ directory |
| maxclaw | 0 | 0 | no vendor/; go mod download pr |
| nanoclaw | 0 | 162533 | node_modules/ |
| openclaw | 0 | 572770 | node_modules/ |
| openhuman | 0 | 0 | target/ directory |
| quantumclaw | 0 | 74892 | node_modules/ |
| zeroclaw | 0 | 1804439 | target/ directory |

## Response Latency (ms)

| Platform | Latency (ms) | Notes |
|----------|--------------|-------|
| clawteam | 32.31 | echo benchmark |
| hermes-agent | 32.69 | echo benchmark |
| nanobot | 32.26 | echo benchmark |
| nanoclaw | 32.43 | echo benchmark |
| openclaw | 32.66 | echo benchmark |
| quantumclaw | 32.47 | echo benchmark |

## Build Proxy Time (ms)

| Platform | Build Time (ms) | Notes |
|----------|-----------------|-------|
| goclaw | 115.041834 | go vet failed (rc=1) |
| ironclaw | 38.96 | cargo check failed (rc=101) |
| maxclaw | 8.067914 | go vet failed (rc=1) |
| openhuman | 39.36 | cargo check failed (rc=101) |
| zeroclaw | 32.49 | cargo check failed (rc=101) |

## All Metrics (Raw)

| Platform | Metric | Value | Unit | Notes |
|----------|--------|-------|------|-------|
| ironclaw | binary_size | 0 | KB | no target/release (not built) |
| ironclaw | install_footprint | 3831495 | KB | target/ directory |
| ironclaw | build_proxy_time | 38.96 | ms | cargo check failed (rc=101) |
| ironclaw | cold_start_time | 0 | ms | binary not built |
| zeroclaw | binary_size | 0 | KB | no target/release (not built) |
| zeroclaw | install_footprint | 1804439 | KB | target/ directory |
| zeroclaw | build_proxy_time | 32.49 | ms | cargo check failed (rc=101) |
| zeroclaw | cold_start_time | 0 | ms | binary not built |
| openhuman | binary_size | 0 | KB | no target/release (not built) |
| openhuman | install_footprint | 0 | KB | target/ directory |
| openhuman | build_proxy_time | 39.36 | ms | cargo check failed (rc=101) |
| openhuman | cold_start_time | 0 | ms | binary not built |
| goclaw | binary_size | 0 | KB | not built |
| goclaw | install_footprint | 0 | KB | no vendor/; go mod download proxy |
| goclaw | build_proxy_time | 115.041834 | ms | go vet failed (rc=1) |
| goclaw | mod_download_time | 3.85 | ms | go mod download |
| goclaw | cold_start_time | 0 | ms | binary not built |
| maxclaw | binary_size | 0 | KB | not built |
| maxclaw | install_footprint | 0 | KB | no vendor/; go mod download proxy |
| maxclaw | build_proxy_time | 8.067914 | ms | go vet failed (rc=1) |
| maxclaw | mod_download_time | 3.7 | ms | go mod download |
| maxclaw | cold_start_time | 0 | ms | binary not built |
| openclaw | install_footprint | 572770 | KB | node_modules/ |
| openclaw | npm_deps | 73 | deps |  |
| openclaw | binary_size | 0 | KB | no dist/ or build/ directory |
| openclaw | cold_start_time | 75.15 | ms | node parse time (no runtime init) |
| openclaw | response_latency_ms | 32.66 | ms | echo benchmark |
| openclaw | memory_idle_mb | 38.4 | MB |  |
| nanoclaw | install_footprint | 162533 | KB | node_modules/ |
| nanoclaw | npm_deps | 19 | deps |  |
| nanoclaw | binary_size | 0 | KB | no dist/ or build/ directory |
| nanoclaw | cold_start_time | 64.91 | ms | node parse time (no runtime init) |
| nanoclaw | response_latency_ms | 32.43 | ms | echo benchmark |
| nanoclaw | memory_idle_mb | 38.5 | MB |  |
| quantumclaw | install_footprint | 74892 | KB | node_modules/ |
| quantumclaw | npm_deps | 12 | deps |  |
| quantumclaw | binary_size | 0 | KB | no dist/ or build/ directory |
| quantumclaw | cold_start_time | 74.99 | ms | node parse time (no runtime init) |
| quantumclaw | response_latency_ms | 32.47 | ms | echo benchmark |
| quantumclaw | memory_idle_mb | 38.6 | MB |  |
| clawteam | py_deps | 19 | deps |  |
| clawteam | install_footprint | 58507 | KB | .venv/ |
| clawteam | cold_start_time | 7.65 | ms | python import clawteam |
| clawteam | response_latency_ms | 32.31 | ms | echo benchmark |
| clawteam | memory_idle_mb | 11.6 | MB | bare python process |
| clawteam | memory_active_mb | 9.0 | MB | python import clawteam (venv) |
| nanobot | py_deps | 86 | deps |  |
| nanobot | install_footprint | 299548 | KB | .venv/ |
| nanobot | cold_start_time | 267.28 | ms | python import nanobot |
| nanobot | response_latency_ms | 32.26 | ms | echo benchmark |
| nanobot | memory_idle_mb | 11.5 | MB | bare python process |
| nanobot | memory_active_mb | 49.3 | MB | python import nanobot (venv) |
| hermes-agent | py_deps | 53 | deps |  |
| hermes-agent | install_footprint | 103253 | KB | .venv/ |
| hermes-agent | cold_start_time | 509.33 | ms | python from run_agent import main |
| hermes-agent | response_latency_ms | 32.69 | ms | echo benchmark |
| hermes-agent | memory_idle_mb | 11.6 | MB | bare python process |
| hermes-agent | memory_active_mb | 45.9 | MB | python from run_agent import main (venv) |
| rtl-claw | runtime_benchmarks | 0 | N/A | hardware description language, no runtime |

## Skipped Platforms

- **openfang**: not found or no Cargo.toml
- **hiclaw**: not found or no go.mod
- **openagents**: not found or no package.json
- **copilot-cli**: not found or no package.json
- **claw-ai-lab**: no pyproject.toml or requirements.txt
- **smolagents**: not checked out — tracked via documentation only
- **langgraph**: not checked out — tracked via documentation only
- **mcp-agent**: not checked out — tracked via documentation only
- **crewai**: not checked out — tracked via documentation only
- **autogen**: not checked out — tracked via documentation only
- **swarms**: not checked out — tracked via documentation only
- **aider**: not checked out — tracked via documentation only
- **rtl-claw**: build-tool only — no runtime agent metrics applicable
