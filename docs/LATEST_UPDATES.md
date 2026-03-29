# Latest Updates: Personal AI Agent Ecosystem (March 2026)

English | **[中文](LATEST_UPDATES.zh-CN.md)**

> Tracking major changes across 8 personal AI agent platforms — architecture innovations, new features, performance improvements, and security hardening from February to March 2026.

---

## Cross-Cutting Themes

This month saw three dominant trends across the ecosystem:

1. **Security was the top priority** — OpenClaw disclosed critical CVEs (RCE, sandbox bypass), NanoClaw partnered with Docker for container-first security, Nanobot removed litellm over supply chain concerns, and IronClaw patched 5 critical vulnerabilities.
2. **Streaming became table stakes** — every active project shipped end-to-end streaming from provider to channel.
3. **Multi-provider LLM expansion** — Codex OAuth, GitHub Copilot, Gemini, AWS Bedrock, and more were added across the board.

---

## OpenClaw

**TypeScript | ~340K stars | v2026.3.24 "Rehabilitation" — Mar 25, 2026**

**Major Milestone:** Creator Peter Steinberger announced joining OpenAI (Feb 14); project transitioning to foundation governance.

### Architecture Changes
- **Channel Plugin Architecture** refactored — WhatsApp migrated to `@openclaw/whatsapp` plugin
- **ACP (Agent Control Protocol) + Channel Runtime** unified in post-release sprint (Mar 28)
- Node 22.14+ floor support (lowered from 24, while still recommending 24)
- `/v1/models` and `/v1/embeddings` gateway endpoints for RAG compatibility
- Native app architecture: iOS/Android/macOS as node devices via WebSocket to central gateway

### New Features
- Microsoft Teams SDK migration with AI-agent UX (streaming 1:1 replies, welcome cards, typing indicators)
- One-click skill install recipes (coding-agent, gh-issues, whisper-api, session-logs, etc.)
- Control UI: status-filter skill tabs, frosted backdrop design
- Discord autoThreadName with LLM-generated titles
- `before_dispatch` plugin hook with canonical inbound metadata
- `--container` / `OPENCLAW_CONTAINER` for running commands inside Docker/Podman
- macOS app: collapsible tree sidebar navigation

### Security
- CVE-2026-25253: One-click RCE via token theft (disclosed Feb 2026)
- CVE-2026-32038: Sandbox network isolation bypass
- Media sandbox bypass closed (`mediaUrl/fileUrl` alias path) (#54034)
- WhatsApp echo loop bugs (6 issues reported Mar 22-27)

### Breaking Changes
18 breaking changes in v2026.3.24 including plugin system migration, `/tools` endpoint redesign, and Teams SDK migration.

---

## ZeroClaw

**Rust | ~29.1K stars | v0.6.5 — Mar 27, 2026 (218 commits)**

### Architecture Changes
- **Session state machine** with idle/running/error tracking
- **Per-session actor queue** for concurrent turn serialization
- **Shared iteration budget** for parent/subagent coordination
- **Context overflow recovery** — preemptive check before provider calls, fast-path tool result trimming

### New Features
- Matrix channel: automatic E2EE recovery, multi-room listening, masked secrets
- Slack permalink resolution via API
- Web dashboard: persistent Agent Chat history across navigation/refresh
- Marketplace templates for Coolify, Dokploy, EasyPanel
- Inbound message debouncing for rapid senders

### Performance
- **<5MB RAM, <10ms cold start** on 0.8GHz — 99% less memory than OpenClaw
- ~8.8MB binary, single static Rust binary with zero runtime dependencies

### Security
- Gateway auth rate limiting for brute-force protection
- Impersonation warning (Feb 19): zeroclaw.org/net domains not affiliated

---

## IronClaw

**Rust | Rapid growth | v0.23.0 — Mar 27, 2026**

> Most active project this month: **8 releases in March alone** (v0.15.0 → v0.23.0).

### Architecture Changes
- **Multi-tenant auth** with per-user workspace isolation
- **Layered memory** with sensitivity-based privacy redirect
- **Unified thread model** for web gateway
- Feishu/Lark WASM channel plugin
- WASM extension versioning with WIT compatibility checks
- AppEvent extracted to `crates/ironclaw_common`
- Cargo-deny for supply chain safety

### New Features (highlights from v0.22.0)
- Thread per-tool reasoning through provider/session/surfaces
- Complete UX overhaul — design system, onboarding, web polish
- Gemini CLI OAuth integration with Cloud Code API
- Low/Medium/High risk **command approval levels**
- GitHub Copilot + OpenAI Codex as LLM providers
- Public webhook trigger endpoint for routines
- 13-dimension complexity scorer for smart routing
- Import OpenClaw memory, history, settings
- i18n support (Chinese + English)
- AWS Bedrock LLM provider via native Converse API
- HMAC-SHA256 webhook signature validation for Slack

### Security (5 critical fixes)
- Validate embedding base URLs to prevent SSRF
- Escape tool output XML content
- Reject malformed OAuth states
- Patch rustls-webpki vulnerability (RUSTSEC-2026-0049)
- OsRng for all security-critical key/token generation
- Auth bypass, relay failures, unbounded recursion, context growth — all fixed

### Performance
- Complete LLM response cache (set_model invalidation, stats logging)
- Arc-based embedding cache to avoid clones on miss path
- Criterion benchmarks for safety layer hot paths

---

## GoClaw

**Go | ~1.3K stars | v2.43.1 — Mar 29, 2026 (355 total releases)**

### Architecture Changes
- **Lane-based scheduler** (main/subagent/team/cron lanes)
- **Agent Teams**: shared task boards, inter-agent delegation (sync/async), hybrid discovery
- **GoClaw Lite (Desktop Edition)**: Wails v2 + React, ~30MB, SQLite, max 5 agents

### New Features
- **20+ LLM providers** (Anthropic native HTTP+SSE with prompt caching, OpenAI, Groq, DeepSeek, Gemini, Mistral, xAI, MiniMax, etc.)
- **7 messaging channels** (Telegram, Discord, Slack, Zalo, Feishu/Lark, WhatsApp, QQ)
- Extended thinking per-provider (Anthropic budget tokens, OpenAI reasoning effort)
- **Knowledge graph** with LLM extraction + traversal (pgvector hybrid BM25 + embeddings)
- Skill system with BM25 + pgvector hybrid search
- Heartbeat system with HEARTBEAT.md checklists
- OpenTelemetry OTLP export
- MCP integration (stdio/SSE/streamable-http)
- TTS with 4 providers, media generation (image/audio/video), browser automation

### Performance
- ~35MB idle RAM, <1s startup, ~25-36MB binary

---

## NanoClaw

**Python | Active dev | Docker Partnership announced Mar 13, 2026**

### Architecture Changes
- **Container-first execution** — everything runs in containers by default
- Core engine ~4,000 LOC (auditable, fits in AI agent context window)
- Andrej Karpathy publicly endorsed: *"core engine ~4000 LOC that can fit in my head"*

### New Features
- Docker Sandbox integration (partnership with Docker Inc.)
- WhatsApp support via Baileys integration (merged Mar 26)
- Agent social network linking (Moltbook, ClawdChat)

### Security
- Container-first model is a direct response to OpenClaw's CVE-2026-25253 (token theft → RCE) and CVE-2026-32038 (sandbox bypass)
- Cohen (creator) publicly criticized OpenClaw for storing WhatsApp messages in plaintext
- Enterprise sandbox alliance with Docker

---

## Nanobot

**Python | ~36.9K stars | v0.1.4.post6 — Mar 27, 2026 (57 PRs, 27 new contributors)**

### Architecture Changes
- **Agent runtime decomposed**: shared `AgentRunner` extracted, lifecycle hooks unified into `HookContext`
- Command routing refactored into plugin-friendly structure
- **litellm fully removed** — replaced with native OpenAI + Anthropic SDKs (v0.1.4+)
- Subagent progress now preserved on failure

### New Features
- **End-to-end streaming** (provider → channel → CLI)
- **WeChat (Weixin)** full channel support (HTTP long-poll, QR login)
- Feishu CardKit streaming support
- Full-featured onboard wizard
- Per-session concurrent dispatch
- Native multimodal sensory capabilities
- GitHub Copilot OAuth login + OpenAI Codex provider
- **12+ channels**: Telegram, Discord, Slack, WhatsApp, WeChat, Feishu, DingTalk, QQ, WeCom, Matrix, Email, Mochat
- ClawHub skill integration
- VolcEngine, MiniMax, Gemini, DeepSeek, Qwen, Zhipu, Moonshot, Mistral, OVMS, Step Fun providers
- Token-based memory system

### Security
- GHSA-4gmr-2vc8-7qh3: Email injection/spoofing — SPF/DKIM verification enforced by default
- Email content tagged `[EMAIL-CONTEXT]` to prevent LLM prompt injection
- litellm supply chain poisoning advisory — fully removed since v0.1.4.post6
- Zombie process reaping, session poisoning fix, safer default access control

### Performance
- Prompt cache optimization for Anthropic models
- Stream delta coalescing to reduce API calls
- Memory consolidation with completion headroom reservation

---

## ClawTeam-OpenClaw

**Python | ~884 stars | v0.2.0+openclaw.1 — Mar 28, 2026**

### Architecture Changes
- Per-agent session isolation via git worktrees
- Exec approval auto-config for OpenClaw agents
- Production-hardened spawn backends

### New Features
- **ZeroMQ P2P transport** (optional `pip install -e ".[p2p]"`)
- **Web dashboard** (`clawteam board serve --port 8080`)
- **Team templates** (TOML-based, e.g., hedge-fund, ML research)
- **Per-agent model assignment** (preview on `feat/per-agent-model-assignment` branch)
- Plan approval workflows (submit/approve/reject)
- Cross-machine support (NFS/SSHFS or P2P)
- Multi-user namespacing
- `fcntl` file locking for concurrent safety

### Supported Agents
OpenClaw (default), Claude Code, Codex, nanobot, Cursor, custom scripts

---

## Maxclaw

**Go + TypeScript | ~189 stars | v0.1.2 — Mar 17, 2026**

### New Features
- Multi-channel: Telegram, WhatsApp (Bridge), Discord, WebSocket
- Cron/Once/Every scheduler + daily memory digest
- `executionMode=auto` for unattended tasks
- Automatic task titles (summarizes sessions without overwriting content)
- Monorepo-aware recursive context discovery (AGENTS.md / CLAUDE.md)
- Sub-session spawning with independent context/model/source
- Desktop UI + Web UI + API (same port)
- Browser automation
- One-command install script (Linux/macOS)
- Systemd deployment support

---

## Comparative Snapshot

| Project | Stars | Language | Latest Release | Releases in Mar | RAM Usage |
|---------|-------|----------|---------------|-----------------|-----------|
| OpenClaw | ~340K | TypeScript | Mar 25 | 1 major | High |
| ZeroClaw | ~29.1K | Rust | Mar 27 | 1 | **<5MB** |
| IronClaw | Rapid growth | Rust | Mar 27 | **8** | Moderate |
| GoClaw | ~1.3K | Go | Mar 29 | ~30 | ~35MB |
| Nanobot | ~36.9K | Python | Mar 27 | 4 | Moderate |
| NanoClaw | N/A | Python | Active | Partnership-driven | Container-based |
| ClawTeam | ~884 | Python | Mar 28 | 1 | Minimal (CLI) |
| Maxclaw | ~189 | Go+TS | Mar 17 | 1 | Low |

---

*Last updated: March 29, 2026*
*Part of: AllClaws Personal AI Agent Ecosystem Research*
*Next update: April 2026*
