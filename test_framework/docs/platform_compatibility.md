# Platform Compatibility Matrix

This document outlines the compatibility and requirements for each supported platform in the test framework.

## Platforms Overview

| Platform | Language | Binary/Package | Build Time | Dependencies | Database Required |
|----------|----------|----------------|------------|--------------|------------------|
| Zeroclaw | Rust | `target/release/zeroclaw` | ~5 min | Cargo, OpenSSL | Optional (SQLite) |
| Openclaw | TypeScript | `openclaw` (pnpm) | ~2 min | pnpm, Node.js 22+ | No |
| NanoClaw | TypeScript (Node.js) | `nanoclaw` (npm) | ~2 min | npm, Docker | SQLite |
| IronClaw | Rust | `target/release/ironclaw` | ~5 min | Cargo, PostgreSQL 15+ | Required (PostgreSQL 15+) |
| GoClaw | Go | `goclaw` (binary) | ~1 min | Go 1.26+, PostgreSQL 15+ | Required (PostgreSQL 15+) |
| Nanobot | Python | `nanobot-ai` (pip) | ~30 sec | Python 3.11+, pip | SQLite |

## Platform-Specific Requirements

### Zeroclaw
- **Build**: `cargo build --release`
- **Runtime**: Native binary
- **Features**: High performance, trait-based extensions, hardware peripherals
- **Memory**: Markdown/SQLite with embeddings
- **Security**: First-class, internet-adjacent

### Openclaw
- **Install**: `pnpm install`
- **Runtime**: Node.js 22+
- **Features**: 37+ channels, plugin system, media pipeline
- **Memory**: Not specified
- **Security**: CLI security, content redaction

### NanoClaw
- **Install**: `npm install`
- **Runtime**: Node.js, Docker containers
- **Features**: WhatsApp integration, group isolation, containerized agents
- **Memory**: Per-group CLAUDE.md
- **Security**: Container isolation, group-level permissions

### IronClaw
- **Build**: `cargo build --release`
- **Runtime**: Native binary, PostgreSQL 15+ required
- **Features**: WASM sandboxing, MCP protocol, defense-in-depth security
- **Memory**: PostgreSQL with pgvector
- **Security**: WASM sandbox, AES-256-GCM encryption, no telemetry

### GoClaw
- **Build**: `go build -o goclaw .`
- **Runtime**: Native binary, PostgreSQL 15+ required
- **Features**: Agent teams, multi-tenant PostgreSQL, 13+ LLM providers
- **Memory**: PostgreSQL with pgvector
- **Security**: 5-layer defense, prompt injection detection, SSRF protection

### Nanobot
- **Install**: `pip install nanobot-ai`
- **Runtime**: Python 3.11+
- **Features**: Ultra-lightweight (~4,000 LOC), ClawHub skills, MCP integration
- **Memory**: Session history, SQLite (local)
- **Security**: Security hardening, session isolation

## Benchmark Compatibility

| Benchmark Task | Zeroclaw | Openclaw | NanoClaw | IronClaw | GoClaw | Nanobot |
|---------------|-----------|----------|----------|----------|---------|---------|
| Email Processing | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ |
| Calendar Integration | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ |
| Task Management | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Messaging | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Web Research | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ |
| Document Processing | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ |
| Hardware Integration | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Agent Teams | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |
| Multi-Tenant | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ |

## Security Features Comparison

| Security Feature | Zeroclaw | Openclaw | NanoClaw | IronClaw | GoClaw | Nanobot |
|-----------------|-----------|----------|----------|----------|---------|---------|
| Container Isolation | ❌ | ❌ | ✅ | Partial | Partial | ❌ |
| WASM Sandbox | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ |
| Credential Encryption | ✅ | ❌ | ❌ | ✅ | ✅ | ✅ |
| Prompt Injection Defense | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ |
| SSRF Protection | ❌ | ❌ | ❌ | ✅ | ✅ | ❌ |
| Rate Limiting | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ |
| Audit Logging | ✅ | ✅ | ❌ | ✅ | ✅ | ❌ |

## Performance Characteristics

| Metric | Zeroclaw | Openclaw | NanoClaw | IronClaw | GoClaw | Nanobot |
|--------|----------|----------|----------|----------|---------|---------|
| Startup Time | < 10 ms | > 5 s | ~1 s | < 1 s | < 1 s | < 1 s |
| Memory Footprint (Idle) | < 5 MB | > 1 GB | ~100 MB | ~50 MB | ~35 MB | ~50 MB |
| Binary Size | ~3.4 MB | 28 MB + Node.js | ~50 MB | ~30 MB | ~25 MB | ~10 MB |
| Docker Image Size | ~50 MB | ~200 MB | ~150 MB | ~100 MB | ~50 MB | ~100 MB |

## Testing Guidelines

### Before Running Benchmarks

1. **Initialize Submodules**:
   ```bash
   git submodule update --init --recursive
   ```

2. **Install Dependencies**:
   - **Zeroclaw**: `cargo install --path ../zeroclaw`
   - **Openclaw**: `cd ../openclaw && pnpm install`
   - **NanoClaw**: `cd ../nanoclaw && npm install`
   - **IronClaw**: `cd ../ironclaw && cargo install --path .`
   - **GoClaw**: `cd ../goclaw && go build -o goclaw .`
   - **Nanobot**: `pip install nanobot-ai`

3. **Setup Databases** (if required):
   - **IronClaw/GoClaw**: PostgreSQL 15+ with pgvector
   - **Zeroclaw**: SQLite (optional)
   - **Nanobot/NanoClaw**: SQLite (optional)

### Running Benchmarks

```bash
cd test_framework

# Run validation
./scripts/validate_agent.sh agents/example_agent.json

# Run benchmarks for specific platform
./scripts/run_benchmark.sh agents/example_agent.json zeroclaw
./scripts/run_benchmark.sh agents/example_agent.json openclaw
./scripts/run_benchmark.sh agents/example_agent.json nanoclaw
./scripts/run_benchmark.sh agents/example_agent.json ironclaw
./scripts/run_benchmark.sh agents/example_agent.json goclaw
./scripts/run_benchmark.sh agents/example_agent.json nanobot
```

## Troubleshooting

### Common Issues

1. **Submodule not found**:
   ```
   Error: Zeroclaw submodule not found
   Solution: git submodule update --init --recursive
   ```

2. **Binary not found**:
   ```
   Error: Zeroclaw binary not found
   Solution: cd ../zeroclaw && cargo build --release
   ```

3. **Database not running** (IronClaw/GoClaw):
   ```
   Error: Cannot connect to PostgreSQL
   Solution: Start PostgreSQL 15+ service and create database
   ```

4. **Dependencies missing**:
   ```
   Error: jq is required but not installed
   Solution: sudo apt install jq (or brew install jq on macOS)
   ```

## Conclusion

This framework provides comprehensive testing capabilities across all 6 major personal AI agent platforms. Each platform has unique strengths:
- **Zeroclaw**: Performance and hardware integration
- **Openclaw**: Extensive channels and plugins
- **NanoClaw**: WhatsApp specialization
- **IronClaw**: Security and WASM sandboxing
- **GoClaw**: Multi-agent teams and multi-tenant architecture
- **Nanobot**: Ultra-lightweight and research-friendly

Choose the platform that best matches your use case and requirements.
