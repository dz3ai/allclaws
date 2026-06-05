---
layout: post
title: "AI Agent Ecosystem Report: May-June 2026"
date: 2026-06-01 09:00:00 +0800
author: Danny Zeng
categories: [Monthly Report]
tags: [AI agents, ecosystem, attestation, ironclaw, hermes, nanoclaw, split]
---

## Executive Summary

May-June 2026 saw explosive activity across the ecosystem with **28,000+ commits** across all tracked platforms. While the enterprise-vs-1PC fork continues to define the landscape, the most significant architectural story this month is **IronClaw's 13-PR Attested Signing chain** — a complete web3-native identity and authorization pipeline that may set a template for agent signing architecture industry-wide.

**Key Findings:**

- **IronClaw Attested Signing** — End-to-end chain: OAuth grant → webauthn challenge → wallet signing → durable stores. 13 sequential PRs, the most architecturally coherent feature delivery across any platform this period
- **Hermes-Agent Stabilization Sprint** — 2,839 commits but overwhelmingly bugfix, not new features. Curses UI rewritten, streaming duplications repaired, image size caps added
- **OpenClaw Breaks 16K Commits/Month** — 16136 non-merge commits, led by 3 core contributors (8K, 2.5K, 2.2K each). Session transcription rewrite, Android palette, Mattermost/Feishu/Telegram channel fixes
- **OpenHuman v0.57 Series** — 1,367 commits, 6 releases. Workflows unified with skills, memory sync indicators, font size accessibility
- **ZeroClaw v0.8.0-beta** — 298 commits. Memory strategy refactor, persistent RPC sessions, Windows CLI double-quote preservation
- **CLI Coding Agents Mature** — Reasonix v1.0/v1.1 with MCP schema canonicalization and checkpoint fork/summarize; Copilot-CLI v1.0.60; aider model list expansion
- **"Self-Improving" Claim Verification Stands** — No platform has credibly demonstrated autonomous learning since our Hermes analysis. Marketing claims continue but evidence remains absent

**What to Watch in July:**
1. IronClaw Attested Signing — will other platforms adopt the pattern?
2. OpenClaw's governance direction after creator's departure
3. Enterprise governance frameworks analysis (per Q3 roadmap)
4. MCP deep-dive preliminary findings per H2 priorities

---

## Cross-Cutting Trends

### 1. The Attested Signing Pattern: IronClaw Builds a Template

IronClaw's **13-PR attested signing series** is the month's most architecturally significant work. The chain runs:

```
OAuth Provider Trait → Wire Hardening → Grant Ledger → WebAuthn Challenge/Audit
→ Turns Resume → Chain Signing → Injected Provider → NEAR Redirect → WalletConnect
→ Reborn Runtime → WebUI Ingress → Durable Stores → Loop Raise
```

**What it enables:**
- End-to-end cryptographic attestation of agent actions
- Wallet-based identity (web3 model) for agent authorization
- Session persistence across authorization boundaries
- A reference architecture for any platform needing verifiable agent actions

**Why it matters:** No other tracked platform has attempted agent-level cryptographic attestation. If adopted broadly, this could become as important a pattern as MCP — but for identity and authorization rather than tool access.

**Risk:** 14 follow-up PRs remain in flight (multitenant model, KMS hardening, trust registration). The architecture is not yet production-hardened.

### 2. The Stabilization vs. Innovation Split

A clear divergence is emerging between **innovation-phase** platforms and **stabilization-phase** platforms:

| Phase | Platforms | Signal |
|-------|-----------|--------|
| **Innovation** | IronClaw (Attested Signing, WeCom), Reasonix (checkpoint), ZeroClaw (memory strategy) | New architecture patterns |
| **Stabilization** | Hermes (2,839 commits, mostly fixes), NanoClaw (bumping deps), GoClaw (vault hardening) | Bugfix density > feature density |
| **Stasis** | MaxClaw (0 commits), ClawTeam (8 commits, merge-only), aider (5 commits) | Maintenance mode |

**Implication:** The ecosystem is consolidating. Platforms that reached product-market fit are fixing bugs; platforms still seeking it are innovating. Platforms with zero activity are effectively dormant.

### 3. MCP: Schema Optimization Joins the Debate

This month introduces a new axis to the MCP debate: **schema optimization**.

- **Reasonix** canonicalized MCP JSON schemas specifically for **stable cache prefixes**, directly addressing the token bloat problem flagged in April-May
- **GoClaw** eliminated spurious MCP grant-revoked errors
- **NanoClaw** continues to bypass MCP entirely, preferring direct claude-code integration

**Updated Framework:**

```
Enterprise/Cloud → MCP adoption (interoperability > cost)
Schema optimizers → MCP adoption + schema compaction (compromise)
Local/Personal → MCP resistance (efficiency > everything)
```

### 4. Container-Native vs. Bare-Metal Divergence

The deployment model split is now visible in commit patterns:

- **Container-native** (NanoClaw: 279 commits, Docker partnership, claude-code bumps) — optimizing for orchestrated environments
- **Bare-metal/desktop** (Reasonix: 84 commits, desktop v1.0/v1.1, Tauri-based) — optimizing for local UX
- **Hybrid** (IronClaw, GoClaw, ZeroClaw, OpenClaw) — supporting both with increasing complexity

---

## Platform Deep-Dives

### IronClaw — The Attested Signing Era

**Commits:** 88 | **Release:** ironclaw-v0.29.1 | **Theme:** Cryptographic identity

The 13-PR attested signing series consumed most architectural energy, but other highlights include:

- **WeCom (WeChat Work) channel** — Enterprise China channel integration
- **Temperature plumbing** — Full Responses API temperature passthrough
- **Cargo-deny advisory resolved** — wasmtime dependency upgrade
- **CI improvements** — benchmark comment automation, pull-requests write permission

**Key takeaway:** IronClaw is positioning as the security/identity reference for the ecosystem. The attested signing architecture, if completed, gives it a differentiated advantage over every other tracked platform.

### Hermes-Agent — Stabilization at Scale

**Commits:** 2,839 | **Release:** v2026.5.29.2 | **Theme:** Bugfix density

Hermes remains the most active platform by commit count, but the nature of work has shifted:

**Major fixes landed:**
- Curses UI: replaced `simple_term_menu` with custom curses driver (keyboard decoding, model/provider pickers)
- Gateway: LRU cache normalization, O(n²) watcher recovery fixed
- MCP auth: replaced `time.sleep(0.25)` with `asyncio.sleep` in reconnect poll
- Streaming: stopped duplicating tool-call args from cumulative-resend providers
- Vision: capped embedded image size to prevent session wedging
- Feishu/BlueBubbles: LRU-eviction caps on message caches (unbounded growth fixed)
- Config: `tool_output_limits` no longer caches stale values

**Features:**
- Kanban `goal_mode` — workers run in a `/goal` loop
- Model catalog refreshes hourly (was daily)
- Nous Tool Gateway UI — always show backends, login on select

**Assessment:** Hermes is paying down technical debt. The commit velocity is impressive but the ratio of fixes to features suggests a stabilization phase after rapid earlier growth. The Nous Tool Gateway UI signals a push toward platform-agnostic tool access.

### OpenClaw — Monolithic Activity

**Commits:** 16,136 (non-merge) | **Release:** v2026.6.5-alpha.1 | **Theme:** Scale

Three contributors account for 74% of all commits, making OpenClaw the most concentrated development effort in the ecosystem:

**Notable changes:**
- Session transcription rewrite (registry, terminal markers, stale reconciliation)
- Android provider palette — expiring provider visibility
- Channel fixes across Mattermost, Feishu, Telegram
- Shared codex model visibility in gateway
- Unknown model auth fail-closed

**Concern:** Extremely high commit volume makes review quality hard to assess. 16K non-merge commits/month by 3 primary developers is an unusual ratio. Some may represent automated or bot-assisted contributions.

### ZeroClaw — v0.8.0 Beta

**Commits:** 298 | **Release:** v0.8.0-beta.2 | **Theme:** Memory-first

- Memory strategy refactor: `Agent::turn load_context` migrated to `MemoryStrategy` trait
- Persistent RPC sessions with admin kill
- Windows shell fix: use `raw_arg` to preserve double quotes
- `react-router` bumped to 7.16.0 (5 advisories cleared)
- Ollama fixes: master build compilation, structured tools prompt-guided
- Credential-shaped config surface classification

**Assessment:** ZeroClaw's <5MB RAM positioning remains unique. The memory strategy refactor suggests the minimal-footprint approach is being extended to more sophisticated memory handling without the bloat.

### OpenHuman — Skills + Workflows Unification

**Commits:** 1,367 | **Release:** v0.57.13 | **Theme:** Integration

- **Major architecture**: Workflows merged into unified skills primitive
- Memory sync: reliable per-source sync indicators and counters
- Memory tab stripped to core view, analysis sub-pills hidden
- Agent run ledger state persistence
- Composio connection picker enriched with cached account identity
- Global font size accessibility setting

**Assessment:** OpenHuman is maturing from academic prototype to production-ready architecture. The workflows-skills merge is a significant simplification. v0.57.x release cadence (6 releases) confirms active ship cycle.

### GoClaw — Vault Hardening

**Commits:** 98 | **Release:** v3.13.0-beta.2 | **Theme:** Security

- Vault: symlink containment hardening, content persistence on POST/PUT
- Vault: non-master tenant 500 error fixed (O_NOFOLLOW, slog, *string content)
- Secure-CLI: credential adapters framework + git adapter
- MCP: spurious grant-revoked errors eliminated (tool filter + session reset + system-user bypass)
- Channels: multi-attachment inbound coalescing

**Assessment:** The vault/document subsystem received comprehensive hardening. Secure-CLI credential adapters lay groundwork for credential isolation patterns that become critical in multi-tenant deployments.

### HiClaw — v1.1.2 Release

**Commits:** 72 | **Release:** v1.1.2 | **Theme:** Operations

- Worker `--network hiclaw-net` flag for container networking
- Controller: worker creation no longer triggers phantom spec changes
- Gateway: AI route authorization serialized
- Installer: admin username normalization
- Tests: Manager no longer asks 4-input confirmation during worker creation

**Assessment:** v1.1.2 is an operations-focused release. The test improvements (eliminating manual confirmation prompts) suggest a push toward CI/CD automation.

### NanoClaw — Dependency Tracking

**Commits:** 279 | **Release:** v2.0.71 | **Theme:** Integration

- claude-code bumped to 2.1.154
- Groups delete cascade fix
- DB self-restart malformed state fix
- Context window: 179K tokens / 89% utilization

**Assessment:** NanoClaw's Docker partnership and claude-code integration form a defensible moat. At 89% context window utilization, the question becomes whether users actually need more or the current window is sufficient for container-first workflows.

### CLI Coding Agents

| Agent | Commits | Version | Key Changes |
|-------|---------|---------|-------------|
| **Reasonix** | 84 | v1.0.0, v1.1.0 | MCP schema canonicalization, checkpoint fork/summarize, desktop rewind UI |
| **Copilot-CLI** | 15 | v1.0.57 → v1.0.60-0 | 3 minor releases |
| **Aider** | 5 | — | Model list expansion, bash tree-sitter for repomap |

**Reasonix checkpoint feature** is architecturally notable: fork-from-here + summarize-from/up-to-here replicates Claude Code's checkpoint workflow on a DeepSeek-native stack. Combined with MCP schema canonicalization for cache stability, this positions Reasonix as the most feature-complete non-OpenAI coding agent on the market.

### Other Platforms

| Platform | Commits | Notes |
|----------|---------|-------|
| **Nanobot** | 410 | Auth required for WS tokens, heartbeat fix, Matrix SAS verification |
| **ClawTeam** | 8 | Upstream merge (197 commits) + skill install scripts |
| **MaxClaw** | 0 | No activity |
| **Claw-AI-Lab** | 0 | No tags released |

---

## Health Check: Test Framework Results

**Latest Results: 165/177 pass (93%)** — unchanged from April-May

| Platform | Tests | Pass Rate | Health |
|----------|-------|-----------|--------|
| Openclaw | 13/13 | 100% | Excellent |
| IronClaw | 14/14 | 100% | Excellent |
| ZeroClaw | 14/14 | 100% | Excellent |
| NanoClaw | 13/13 | 100% | Excellent |
| Maxclaw | 13/14 | 93% | Good |
| ClawTeam | 12/13 | 92% | Good |
| GoClaw | 11/14 | 79% | Fair |
| Hermes-Agent | 11/13 | 85% | Good |
| Claw-AI-Lab | 11/13 | 85% | Good |
| HiClaw | 13/14 | 93% | Good |
| Nanobot | 10/13 | 77% | Fair |

**Note:** Agent Platform Tests CI still failing on the Openclaw step (YAML runner path issue inherited from previous cleanup). Benchmark Suite CI remains green.

---

## Platform Categorization Update

Since the April-May report expanded from 13 to 25 platforms, tracking has stabilized. Current platform categories stand at **23 tracked platforms** (after removing 3 inactive: rtl-claw, quantumclaw, mcp-agent; adding OpenAI Codex CLI).

| Category | Count | Examples |
|----------|-------|----------|
| Claw Ecosystem | 11 | OpenClaw, IronClaw, ZeroClaw, NanoClaw, ... |
| CLI Coding Agents | 5 | Reasonix, Copilot-CLI, Aider, Codex CLI, Kimi-CLI |
| Human Digital Twin | 1 | OpenHuman |
| External Frameworks | 6 | SmolAgents, LangGraph, CrewAI, AutoGen, Swarms, OpenAgents |

---

## Emerging Patterns

### 1. Agent Authorization: The Next Frontier

IronClaw's attested signing chain and GoClaw's secure-CLI credential adapters both address the same problem from different angles: **how do agents securely prove identity and authority?**

- IronClaw: Cryptographic attestation (web3 model)
- GoClaw: Credential adapter framework (pluggable)
- ZeroClaw: Credential-shaped config surface classification
- Hermes-Agent: Nous Tool Gateway (platform-agnostic tool backend)

This is emerging as a new ecosystem dimension alongside MCP and memory. Expect it to be a major topic in the July report.

### 2. Desktop Agent UX Maturation

- Reasonix desktop v1.0/v1.1 with Tauri-based rewind/fork/summarize dropdowns
- OpenHuman desktop with accessibility font sizing and agent run ledger
- NanoClaw containers serve headless use, desktop remains fragmented

The desktop agent UI space is still wide open — no platform has achieved "IDE of agents" status.

### 3. China Market Channels

- IronClaw: WeCom (WeChat Work) channel
- OpenClaw: Feishu channel fixes
- ZeroClaw: Windows shell compatibility

Enterprise China integrations are quietly progressing across the Rust/TypeScript platforms. This may become a distinguishing factor for adoption in Asia-Pacific markets.

---

## Looking Ahead: July 2026 Priorities

Per the H2 2026 roadmap:

1. **MCP Ecosystem Deep-Dive** — Comprehensive analysis of MCP adoption, token overhead, and server ecosystem. Preliminary findings due this month
2. **Enterprise Governance Frameworks** — Analysis of Okta AI identity, HiClaw/GoClaw enterprise patterns, human-in-the-loop workflows
3. **Attested Signing Follow-up** — Whether IronClaw's pattern inspires adoption in other platforms
4. **Benchmark refresh** — Updated runtime benchmarks with Codex CLI and latest platform versions

---

## Methodology

**Data Collection:**
- Commit counts via `git log --since` per submodule
- Tag analysis via `git tag --sort=-creatordate`
- All counts cover 2026-05-05 to 2026-06-05

**Platform Coverage:**
- 19 git submodules updated and analyzed
- OpenClaw, OpenHuman, ZeroClaw freshly synced for this report
- External frameworks tracked via documentation and source code analysis

**Test Framework:**
- 177 tests across 13 claw ecosystem platforms
- Docker sandboxed runtime testing
- Static analysis: build manifest, health docs, CI config

---

**Next Report:** First Monday of July 2026 — MCP Deep-Dive Special

---

**Stay Updated:**
- GitHub: [dz3ai/allclaws](https://github.com/dz3ai/allclaws)
- Detailed tracker: [docs/LATEST_UPDATES.md](https://github.com/dz3ai/allclaws/blob/main/docs/LATEST_UPDATES.md)
- Roadmap: [docs/ROADMAP.md](https://github.com/dz3ai/allclaws/blob/main/docs/ROADMAP.md)

*Methodology: We track 23 AI agent platforms through automated git analysis, significance filtering, and sandboxed integration testing. Full research available in our GitHub repository.*
