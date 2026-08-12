# S1-T1: Workspace Isolation in Hermes-Agent

## Profile-Based Isolation

Hermes-Agent implements workspace isolation through a **profile system** as its primary boundary. According to the AllClaws architecture docs and confirmed by the live installation, each profile resides at `~/.hermes/profiles/<name>/` and provides **fully isolated configuration, credentials, skills, memory, and sessions**.

### Profile Structure
Each profile contains independent instances of:
- `config.yaml` — Model settings, toolsets, personalities
- `auth.json` — Credential pools with automatic rotation
- `.env` — Provider-specific secrets
- `skills/` — Profile-specific procedural knowledge
- `sessions/` — Isolated conversation history
- `state.db` — SQLite session and memory database
- `projects.db` — Project tracking

The installation confirms two active profiles: `personal` and `work`, each with their own `state.db` (1.9MB vs 368KB WAL sizes) and `.env` files. This **multi-profile design enables clean separation** between personal and professional contexts without cross-contamination.

### Project System
Hermes extends profile isolation through a **project system** that groups related folders within a profile. Projects can reference context files like `AGENTS.md` and `CLAUDE.md` for monorepo-aware discovery, similar to Maxclaw's approach. However, unlike ClawTeam's git worktree isolation, Hermes projects share the same profile-level state and credentials.

### Comparison to Ecosystem
- **GoClaw**: PostgreSQL multi-tenant workspaces — more enterprise-grade, heavier setup
- **ClawTeam**: Git worktrees per agent — zero-conflict isolation but requires git knowledge
- **NanoClaw**: Per-group container isolation — heaviest resource footprint
- **Hermes**: Profile-level filesystem isolation — simple, lightweight, no database dependency

The profile boundary is both the **strength and limitation** of Hermes' isolation model. It excels at separating user contexts but lacks per-workspace credential segregation within a single profile. For multi-team enterprises, GoClaw's PostgreSQL approach provides finer-grained access control.