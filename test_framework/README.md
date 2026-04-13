# AllClaws Test Framework

A comprehensive testing and benchmarking framework for 13 AI Agent platforms across multiple programming languages (Rust, Go, Python, TypeScript, Verilog).

## Overview

The framework provides:
- **Sandboxed Testing**: Docker/Podman containers for isolated platform testing
- **Static Analysis**: Project health checks (LICENSE, README, CI, dependencies)
- **Benchmarks**: Codebase metrics (LOC, dependencies, test counts)
- **Runtime Testing**: Real execution tests inside containers
- **DeepEval Integration**: LLM-based agent capability evaluation

## Supported Platforms (13)

| Platform | Language | Container Image |
|----------|----------|-----------------|
| openclaw | TypeScript | node:22-alpine |
| nanoclaw | TypeScript | node:22-alpine |
| quantumclaw | TypeScript | node:22-alpine |
| zeroclaw | Rust | rust:alpine |
| ironclaw | Rust | rust:alpine |
| goclaw | Go | golang:1.23-alpine |
| maxclaw | Go | golang:1.23-alpine |
| hiclaw | Go | golang:1.23-alpine |
| clawteam | Python | python:3.11-slim |
| nanobot | Python | python:3.11-slim |
| claw-ai-lab | Python | python:3.11-slim |
| hermes-agent | Python | python:3.11-slim |
| rtl-claw | Verilog | localhost/openclaw:local |

## Directory Structure

```
test_framework/
├── README.md                       # This file
├── README-zh_CN.md                 # Chinese version
├── docker-compose.yml              # Sandbox environment definitions
├── scripts/
│   ├── run_sandboxed_tests.sh      # Main orchestrator
│   ├── run_sandbox_runtime_tests.sh # Runtime testing
│   ├── run_tests.sh                # Static analysis
│   ├── run_benchmarks.sh           # Benchmark metrics
│   ├── setup.sh                    # Framework setup
│   ├── setup_platforms.sh          # Submodule initialization
│   ├── run_benchmark.sh            # Legacy benchmark runner
│   └── validate_agent.sh           # Agent validation
├── results/                        # Test results (timestamped)
│   └── latest/                     # Symlink to latest results
├── benchmark_results/              # Benchmark metrics
│   └── latest/                     # Symlink to latest benchmarks
├── evals/                          # DeepEval evaluations
├── docs/
│   ├── api.md                      # API reference
│   ├── examples.md                 # Usage examples
│   ├── sandboxed-testing-guide.md  # Sandbox testing guide
│   ├── platform_compatibility.md   # Platform compatibility
│   └── FAQ.md                      # Frequently asked questions
└── config.json                     # Platform configurations
```

## Quick Start

### 1. Setup

```bash
cd test_framework

# Initialize submodules (if not already done)
bash scripts/setup_platforms.sh

# Install dependencies
sudo apt install jq docker-compose  # or podman-compose
```

### 2. Run All Tests

```bash
# Test all 13 platforms
bash scripts/run_sandboxed_tests.sh

# Test specific platforms only
bash scripts/run_sandboxed_tests.sh openclaw zeroclaw goclaw
```

### 3. View Results

```bash
# Test results
cat results/latest/results.md

# Benchmark metrics
cat benchmark_results/latest/benchmark_results.md

# Sandbox runtime findings
cat results/latest/sandbox_findings.md

# Or via web server (if running)
http://localhost:8080
```

## Test Types

### 1. Static Analysis

Checks project health without running code:
- Source files present (count by language)
- Lockfiles (package-lock.json, Cargo.lock, go.sum)
- CI/CD configuration (.github/workflows)
- Documentation (README, LICENSE, CHANGELOG, CONTRIBUTING)
- Docker configuration

### 2. Benchmarks

Measures codebase scale:
- Lines of code (by language)
- Dependency counts
- Test file counts
- Repository size

### 3. Sandbox Runtime Tests

Runs applications in containers and detects:
- Version mismatches (Rust edition2024, Go version)
- Build failures (cargo check, go build)
- Missing dependencies
- Configuration issues

## Prerequisites

- **Docker** or **Podman**: Container runtime
- **docker-compose** or **podman-compose**: Multi-container orchestration
- **jq**: JSON processor

```bash
# Ubuntu/Debian
sudo apt install jq docker.io docker-compose

# macOS
brew install jq docker docker-compose

# With Podman
sudo apt install jq podman podman-compose
```

## Container Runtime

The framework auto-detects your container runtime:
- Prefers `podman` if available
- Falls back to `docker` otherwise
- Uses corresponding compose command (`podman-compose` or `docker-compose`)

## Configuration

### Docker Compose Services

| Service | Description | Volumes |
|---------|-------------|---------|
| `*-sandbox` | Platform test container | Source (read-only), build output (writable) |
| `deepeval-runner` | Evaluation runner | evals/, results/, Docker socket |
| `results-collector` | Nginx result server | results/ (port 8080) |

### Environment Variables

```bash
# DeepEval (optional)
DEEPEVAL_API_KEY=your_key

# LLM APIs for evaluation
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-...
```

## Individual Test Scripts

```bash
# Static analysis only
bash scripts/run_tests.sh

# Benchmarks only
bash scripts/run_benchmarks.sh

# Runtime testing only
bash scripts/run_sandbox_runtime_tests.sh [platform...]

# Single platform tests
bash scripts/run_tests.sh openclaw
bash scripts/run_benchmarks.sh zeroclaw
```

## Cleanup

```bash
# Stop all containers
docker-compose down

# Remove volumes
docker-compose down -v

# Clean up old results (keep latest 5)
ls -t results/ | tail -n +6 | xargs -I {} rm -rf results/{}
```

## GitHub Actions

The framework includes CI/CD workflows:
- **Push to main**: Full test suite
- **Pull requests**: Static analysis + benchmarks
- **Weekly schedule**: Complete sandboxed testing
- **Manual trigger**: On-demand testing

```bash
# Trigger manually
gh workflow run agent-tests.yml
```

## Troubleshooting

### Container not starting

```bash
# Check logs
docker-compose logs [service-name]

# Verify volume paths
docker-compose config
```

### Submodule not found

```bash
git submodule update --init --recursive
```

### Permission denied

```bash
# Add user to docker group
sudo usermod -aG docker $USER
newgrp docker

# Or use sudo
sudo docker-compose up -d
```

## Documentation

- [Sandboxed Testing Guide](docs/sandboxed-testing-guide.md) - Detailed sandbox testing
- [API Reference](docs/api.md) - Framework API
- [Examples](docs/examples.md) - Usage examples
- [Platform Compatibility](docs/platform_compatibility.md) - Platform-specific notes
- [FAQ](docs/FAQ.md) - Common questions

## License

MIT
