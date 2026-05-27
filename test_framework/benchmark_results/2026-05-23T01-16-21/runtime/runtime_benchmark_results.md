# Runtime Benchmark Results — 2026-05-23T01:16:24

Engine v3.0.0 | 18 metrics across 3 platforms

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
| hermes-agent | 16.0 | import failed (from run_agent import main) — not i |
| nanobot | 32.44 | import failed (import nanobot) — not installed |
| openclaw | 64.35 | node parse time (no runtime init) |

## Memory Usage

| Platform | Idle (MB) | Active (MB) | Notes |
|----------|-----------|-------------|-------|
| hermes-agent | 11.5 | 11.5 | bare python process |
| nanobot | 11.6 | 11.5 | bare python process |
| openclaw | 38.7 | 0 |  |

## Binary / Installation Size

| Platform | Binary Size (KB) | Install Footprint (KB) | Notes |
|----------|------------------|------------------------|-------|
| openclaw | 0 | 0 | node_modules/ not installed |

## Response Latency (ms)

| Platform | Latency (ms) | Notes |
|----------|--------------|-------|
| hermes-agent | 26.79 | echo benchmark |
| nanobot | 32.87 | echo benchmark |
| openclaw | 32.4 | echo benchmark |

## Build Proxy Time (ms)

| Platform | Build Time (ms) | Notes |
|----------|-----------------|-------|

## All Metrics (Raw)

| Platform | Metric | Value | Unit | Notes |
|----------|--------|-------|------|-------|
| openclaw | install_footprint | 0 | KB | node_modules/ not installed |
| openclaw | npm_deps | 73 | deps |  |
| openclaw | binary_size | 0 | KB | no dist/ or build/ directory |
| openclaw | cold_start_time | 64.35 | ms | node parse time (no runtime init) |
| openclaw | response_latency_ms | 32.4 | ms | echo benchmark |
| openclaw | memory_idle_mb | 38.7 | MB |  |
| nanobot | py_deps | 86 | deps |  |
| nanobot | install_footprint | 0 | KB | no venv found |
| nanobot | cold_start_time | 32.44 | ms | import failed (import nanobot) — not installed |
| nanobot | response_latency_ms | 32.87 | ms | echo benchmark |
| nanobot | memory_idle_mb | 11.6 | MB | bare python process |
| nanobot | memory_active_mb | 11.5 | MB | python import nanobot (system) |
| hermes-agent | py_deps | 53 | deps |  |
| hermes-agent | install_footprint | 0 | KB | no venv found |
| hermes-agent | cold_start_time | 16.0 | ms | import failed (from run_agent import main) — not installed |
| hermes-agent | response_latency_ms | 26.79 | ms | echo benchmark |
| hermes-agent | memory_idle_mb | 11.5 | MB | bare python process |
| hermes-agent | memory_active_mb | 11.5 | MB | python from run_agent import main (system) |
