# S1-T4: Profile Identity and User Context in Hermes-Agent

## Profile System as Identity Boundary

Hermes-Agent uses **profiles** as its primary identity and context separation mechanism. Each profile represents a distinct user or operational context with its own:

- `config.yaml` — Independent model settings, toolsets, personalities
- `.env` — Separate credential environment variables
- `auth.json` — Isolated credential pools
- `skills/` — Profile-specific procedural knowledge (15 vs 16 skills in personal/work)
- `memories/` — Context-specific long-term memory
- `sessions/` — Isolated conversation histories
- `state.db` — SQLite database for session and memory persistence

The live installation confirms two active profiles (`personal` and `work`) with completely isolated state. The `personal` profile has a larger `state.db-wal` (3.2MB) than `work` (1.9MB), indicating more accumulated context. This **multi-profile architecture enables clean identity separation** without cross-contamination of sessions, memory, or credentials.

## Profile-Level Configuration

Each profile inherits from a `profile.yaml` configuration file but overrides with local settings. The architecture docs reference `default`, `personal`, and `work` as common profile names. Unlike GoClaw's per-user workspaces in PostgreSQL or HiClaw's worker resources, Hermes profiles are **filesystem-based and require no database setup**.

## Project Context Files

Hermes supports **project-level context** through monorepo-aware discovery of `AGENTS.md` and `CLAUDE.md` files. These files provide project-specific instructions and context that apply across all sessions working in that directory. The AGENTS.md file in the Hermes codebase itself (79KB) demonstrates this pattern, serving as context for AI assistants working on the Hermes codebase.

### Comparison to Maxclaw
Maxclaw implements similar context discovery with `AGENTS.md` and `CLAUDE.md` but adds `memory/heartbeat.md` for active context tracking. Hermes lacks the heartbeat pattern but shares the monorepo-aware approach.

## Cross-Session Persistence

Hermes provides **two persistence layers** that survive across sessions:

1. **Memory system** — Stored in `memories/` directory, accessible via `session_search()` tool. The architecture docs mention FTS5-backed retrieval over SQLite session databases, enabling full-text search of past conversations.

2. **Skills system** — Stored in `skills/` directory as SKILL.md files. Skills persist across profiles (can be copied or symlinked) and represent reusable procedural knowledge. The `.skills_prompt_snapshot.json` file (45KB in personal, 44KB in work) tracks skill prompt optimization.

The architecture docs note Hermes "learns across sessions (memory + skills)" — this is the **primary persistence mechanism**, distinct from GoClaw's PostgreSQL-backed knowledge graphs or ClawTeam's JSON state files.

## Identity vs. Multi-Tenancy

Hermes' profile system provides **identity separation** but **not multi-tenancy**. Multiple humans can run Hermes simultaneously with different profiles, but a single Hermes instance does not support concurrent user sessions within one profile. This contrasts with GoClaw's PostgreSQL multi-tenant architecture, which supports per-user workspaces and team-based access control.

## What Persists Across Sessions

- **Session history** — All conversations in `sessions/` directory
- **Skills** — All SKILL.md files in `skills/` directory
- **Memories** — Context saved via memory tools
- **Credentials** — auth.json credential pools
- **Project context** — AGENTS.md, CLAUDE.md discovered per directory
- **Configuration** — config.yaml settings

**What does NOT persist**: Temporary cache files, process state, uncommitted file changes. This aligns with Hermes' local-first design — all meaningful state is in the profile directory.

## User/Context Separation Summary

| Aspect | Implementation | Isolation Level |
|--------|----------------|-----------------|
| **Identity** | Profile system (~/.hermes/profiles/*) | Complete filesystem isolation |
| **Context** | AGENTS.md/CLAUDE.md + memories | Project-level shared context |
| **Persistence** | SQLite state.db + skills/ | Cross-session, not cross-profile |
| **Multi-user** | Separate profiles only | No single-instance multi-tenancy |

Hermes' profile identity model is **simple and effective for personal agents** but lacks enterprise-grade multi-user capabilities found in GoClaw and HiClaw.