# Runtime Benchmark Results — 2026-05-23T15-33-32

Engine v3.0.0 | 59 metrics across 12 platforms

## Toolchain

| Tool | Available |
|------|-----------|
| python3 | true |
| cargo | true |
| node | true |
| go | false |
| docker | true |
| podman | true |
| ps | true |
| time_v | true |

## Cold Start Time (ms)

| Platform | Cold Start (ms) | Notes |
|----------|-----------------|-------|
| clawteam | 27.37 | import failed (import clawteam) — not installed |
| goclaw | 0 | binary not built |
| hermes-agent | 32.74 | import failed (from run_agent import main) — not i |
| ironclaw | 0 | binary not built |
| maxclaw | 0 | binary not built |
| nanobot | 32.64 | import failed (import nanobot) — not installed |
| nanoclaw | 64.86 | node parse time (no runtime init) |
| openclaw | 65.26 | node parse time (no runtime init) |
| openhuman | 0 | binary not built |
| quantumclaw | 82.06 | node parse time (no runtime init) |
| zeroclaw | 0 | binary not built |

## Memory Usage

| Platform | Idle (MB) | Active (MB) | Notes |
|----------|-----------|-------------|-------|
| clawteam | 11.5 | 11.5 | bare python process |
| hermes-agent | 11.5 | 11.6 | bare python process |
| nanobot | 11.5 | 11.6 | bare python process |
| nanoclaw | 38.6 | 0 |  |
| openclaw | 38.7 | 0 |  |
| quantumclaw | 38.6 | 0 |  |

## Binary / Installation Size

| Platform | Binary Size (KB) | Install Footprint (KB) | Notes |
|----------|------------------|------------------------|-------|
| goclaw | 0 | 0 | no vendor/; go mod download pr |
| ironclaw | 0 | 3831495 | target/ directory |
| maxclaw | 0 | 0 | no vendor/; go mod download pr |
| nanoclaw | 0 | 0 | node_modules/ not installed |
| openclaw | 0 | 0 | node_modules/ not installed |
| openhuman | 0 | 0 | target/ directory |
| quantumclaw | 0 | 0 | node_modules/ not installed |
| zeroclaw | 0 | 1804439 | target/ directory |

## Response Latency (ms)

| Platform | Latency (ms) | Notes |
|----------|--------------|-------|
| clawteam | 32.53 | echo benchmark |
| hermes-agent | 33.19 | echo benchmark |
| nanobot | 33.06 | echo benchmark |
| nanoclaw | 32.68 | echo benchmark |
| openclaw | 27.32 | echo benchmark |
| quantumclaw | 33.0 | echo benchmark |

## Build Proxy Time (ms)

| Platform | Build Time (ms) | Notes |
|----------|-----------------|-------|
| goclaw | 0 | go toolchain not available |
| ironclaw | 43.83 | cargo check failed (rc=101) |
| maxclaw | 0 | go toolchain not available |
| openhuman | 32.85 | cargo check failed (rc=101) |
| zeroclaw | 33.14 | cargo check failed (rc=101) |

## All Metrics (Raw)

| Platform | Metric | Value | Unit | Notes |
|----------|--------|-------|------|-------|
| ironclaw | binary_size | 0 | KB | no target/release (not built) |
| ironclaw | install_footprint | 3831495 | KB | target/ directory |
| ironclaw | build_proxy_time | 43.83 | ms | cargo check failed (rc=101) |
| ironclaw | cold_start_time | 0 | ms | binary not built |
| zeroclaw | binary_size | 0 | KB | no target/release (not built) |
| zeroclaw | install_footprint | 1804439 | KB | target/ directory |
| zeroclaw | build_proxy_time | 33.14 | ms | cargo check failed (rc=101) |
| zeroclaw | cold_start_time | 0 | ms | binary not built |
| openhuman | binary_size | 0 | KB | no target/release (not built) |
| openhuman | install_footprint | 0 | KB | target/ directory |
| openhuman | build_proxy_time | 32.85 | ms | cargo check failed (rc=101) |
| openhuman | cold_start_time | 0 | ms | binary not built |
| goclaw | binary_size | 0 | KB | not built |
| goclaw | install_footprint | 0 | KB | no vendor/; go mod download proxy |
| goclaw | build_proxy_time | 0 | ms | go toolchain not available |
| goclaw | mod_download_time | 0 | ms | go toolchain not available |
| goclaw | cold_start_time | 0 | ms | binary not built |
| maxclaw | binary_size | 0 | KB | not built |
| maxclaw | install_footprint | 0 | KB | no vendor/; go mod download proxy |
| maxclaw | build_proxy_time | 0 | ms | go toolchain not available |
| maxclaw | mod_download_time | 0 | ms | go toolchain not available |
| maxclaw | cold_start_time | 0 | ms | binary not built |
| openclaw | install_footprint | 0 | KB | node_modules/ not installed |
| openclaw | npm_deps | 73 | deps |  |
| openclaw | binary_size | 0 | KB | no dist/ or build/ directory |
| openclaw | cold_start_time | 65.26 | ms | node parse time (no runtime init) |
| openclaw | response_latency_ms | 27.32 | ms | echo benchmark |
| openclaw | memory_idle_mb | 38.7 | MB |  |
| nanoclaw | install_footprint | 0 | KB | node_modules/ not installed |
| nanoclaw | npm_deps | 19 | deps |  |
| nanoclaw | binary_size | 0 | KB | no dist/ or build/ directory |
| nanoclaw | cold_start_time | 64.86 | ms | node parse time (no runtime init) |
| nanoclaw | response_latency_ms | 32.68 | ms | echo benchmark |
| nanoclaw | memory_idle_mb | 38.6 | MB |  |
| quantumclaw | install_footprint | 0 | KB | node_modules/ not installed |
| quantumclaw | npm_deps | 12 | deps |  |
| quantumclaw | binary_size | 0 | KB | no dist/ or build/ directory |
| quantumclaw | cold_start_time | 82.06 | ms | node parse time (no runtime init) |
| quantumclaw | response_latency_ms | 33.0 | ms | echo benchmark |
| quantumclaw | memory_idle_mb | 38.6 | MB |  |
| clawteam | py_deps | 19 | deps |  |
| clawteam | install_footprint | 0 | KB | no venv found |
| clawteam | cold_start_time | 27.37 | ms | import failed (import clawteam) — not installed |
| clawteam | response_latency_ms | 32.53 | ms | echo benchmark |
| clawteam | memory_idle_mb | 11.5 | MB | bare python process |
| clawteam | memory_active_mb | 11.5 | MB | python import clawteam (system) |
| nanobot | py_deps | 86 | deps |  |
| nanobot | install_footprint | 0 | KB | no venv found |
| nanobot | cold_start_time | 32.64 | ms | import failed (import nanobot) — not installed |
| nanobot | response_latency_ms | 33.06 | ms | echo benchmark |
| nanobot | memory_idle_mb | 11.5 | MB | bare python process |
| nanobot | memory_active_mb | 11.6 | MB | python import nanobot (system) |
| hermes-agent | py_deps | 53 | deps |  |
| hermes-agent | install_footprint | 0 | KB | no venv found |
| hermes-agent | cold_start_time | 32.74 | ms | import failed (from run_agent import main) — not installed |
| hermes-agent | response_latency_ms | 33.19 | ms | echo benchmark |
| hermes-agent | memory_idle_mb | 11.5 | MB | bare python process |
| hermes-agent | memory_active_mb | 11.6 | MB | python from run_agent import main (system) |
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
