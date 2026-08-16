# S1-T5: Cross-Platform Synthesis — GoClaw vs ClawTeam vs Hermes-Agent

> Synthesis of 12 analysis files produced by the AllClaws virtual research team. Each member analyzed their assigned platform across four dimensions: workspace isolation, multi-task coordination, security/credentials, and profile/identity. This document cross-references their findings.

---

## 1. Workspace Isolation: Three Paradigms

The three platforms represent fundamentally different answers to "what is a workspace?"

| Dimension | GoClaw | ClawTeam | Hermes-Agent |
|-----------|--------|----------|--------------|
| **Isolation unit** | Per-user tenant (PostgreSQL row-level) | Per-agent git worktree | Per-profile directory tree |
| **Boundary mechanism** | Database TenantID propagation | Filesystem (worktree) + git refs | Filesystem (~/.hermes/profiles/...) |
| **State storage** | PostgreSQL 15+ with pgvector | JSON files under ~/.clawteam/ | SQLite (state.db) + JSON |
| **Multi-user** | Yes (native multi-tenant) | No (single user, shared ~/.clawteam/) | No (profiles are per-user, not multi-user) |
| **Setup cost** | High (requires PostgreSQL) | Low (git only) | Low (filesystem only) |

GoClaw's goclaw-operator analysis identifies the key architectural commitment: TenantID propagates through every layer — gateway routing, agent dispatch, database queries (`store.WithTenantID`), and audit logging. This is database-tenant isolation, the heaviest but most complete model.

ClawTeam's clawteam-lead analysis documents a worktree-agent model: each worker agent gets its own git worktree, eliminating merge conflicts. State lives as JSON files in `~/.clawteam/` (teams/, tasks/, inboxes/, workspaces/). The isolation boundary is the git ref, not a database row.

Hermes-Agent's hermes-researcher analysis confirms a profile-context model: each profile at `~/.hermes/profiles/<name>/` is a self-contained directory with its own config.yaml, .env, auth.json, skills/, sessions/, and state.db. The live installation shows two active profiles (personal at 1.9MB, work at 368KB WAL), proving clean separation between contexts.

**The fundamental fork**: GoClaw isolates by identity (who you are), ClawTeam isolates by task (what you're doing), Hermes isolates by context (which role you're in). GoClaw's database approach scales to hundreds of tenants. ClawTeam's worktree approach scales to dozens of parallel agents. Hermes' profile approach scales to a handful of user contexts.

---

## 2. Multi-Task Coordination: From Swarms to Subagents

| Dimension | GoClaw | ClawTeam | Hermes-Agent |
|-----------|--------|----------|--------------|
| **Pattern** | Gateway-routed agent teams | Leader-worker swarm | Delegate-and-merge subagents |
| **Task tracking** | Shared PostgreSQL task boards | TOML blocked-by dependency chains | In-session todo list |
| **Dependency mgmt** | Implicit (team coordination) | Explicit (auto-unblock chains) | Explicit (todo blocked-by) |
| **Parallel safety** | PostgreSQL locking | Git worktree isolation | Separate sessions + terminals |
| **Inter-agent comms** | PostgreSQL + WebSocket | JSON file inboxes + broadcast | None (fire-and-forget delegation) |
| **Monitoring** | Gateway dashboard | Kanban board + tmux tiled view | Session transcripts |

ClawTeam has the most sophisticated coordination. The clawteam-lead analysis documents TOML dependency chains where task completion auto-unblocks dependents (auth-module → api-endpoints → frontend). Workers communicate through P2P inboxes and broadcast messages. The AllClaws research quantifies this: 5 parallel agents complete a full-stack app in ~3 hours vs 8+ hours sequential — a 2.7x speedup at the same token cost.

GoClaw routes tasks through a gateway to agent teams. The goclaw-operator analysis describes a lane-based scheduler (main/subagent/delegate/cron lanes) backed by PostgreSQL shared state. This is enterprise-grade but heavier — coordination goes through the database, not direct messaging.

Hermes takes the simplest approach. The hermes-researcher analysis documents delegate_task for spawning subagents, cron for scheduled jobs, and tmux sessions for interactive agents. But there is no inter-agent communication channel — delegated tasks are fire-and-forget with results merged on completion. No inboxes, no broadcast, no shared task board.

**Trade-off**: ClawTeam's coordination richness (dependencies, inboxes, monitoring) comes at the cost of setup complexity. Hermes' simplicity (delegate, merge, done) comes at the cost of coordination capability. GoClaw occupies the middle: structured team coordination without ClawTeam's swarm intelligence, but with persistent shared state.

---

## 3. Security & Credentials: Enterprise vs Personal

| Dimension | GoClaw | ClawTeam | Hermes-Agent |
|-----------|--------|----------|--------------|
| **Credential storage** | AES-256-GCM encrypted, per-user | Plaintext in TOML/config files | Credential pools in auth.json |
| **Rotation** | Manual | None | Automatic (exhaustion-based) |
| **RBAC** | Yes (admin/operator/viewer) | No | No |
| **Sandboxing** | Per-user PostgreSQL workspaces | Git worktrees (no process isolation) | Pluggable terminal backends (Docker/SSH) |
| **Audit logging** | Buffered persistence (channel 256) | JSON state files (not structured) | File-based debug logs |
| **Secret redaction** | Per-user encryption | None | SHA-256 fingerprints |
| **Trust model** | Zero-trust multi-tenant | Trusted subprocesses | Single-user, OS-is-boundary |

GoClaw leads decisively. The goclaw-operator analysis documents a 5-layer security defense: AES-256-GCM encryption, RBAC with three roles, exec approval allowlists, buffered audit logging (Go-style channel with capacity 256), and tool rate limiting. Credential isolation is per-tenant — secrets never cross workspace boundaries.

ClawTeam's clawteam-lead analysis is candid about limitations: "file-based state without encryption, no RBAC, no audit logging — makes it unsuitable for regulated environments." Each agent manages its own API keys, typically as environment variables. The trust model assumes all agents are trusted subprocesses.

Hermes occupies an interesting middle position. The hermes-researcher analysis finds credential pools with automatic rotation (when a key returns 401, it's marked "exhausted" and the next key is tried), secret fingerprints for auditing without exposure, and pluggable terminal backends including Docker and SSH. But the SECURITY.md is explicit: "Nothing inside the agent process constitutes containment." Hermes has no RBAC, no multi-tenant isolation, and its audit logs are debug-grade, not compliance-grade.

**The maturity gap**: GoClaw treats security as an architecture concern (database-level isolation, encryption at rest, structured audit). ClawTeam treats security as a git concern (worktree isolation prevents conflicts). Hermes treats security as an operations concern (credential rotation, approval gates, pluggable backends). Only GoClaw is enterprise-ready.

---

## 4. Profile & Identity: Who Are You?

| Dimension | GoClaw | ClawTeam | Hermes-Agent |
|-----------|--------|----------|--------------|
| **Identity scope** | User (TenantID) | Team (TOML template) | Profile (directory) |
| **Multi-user** | Yes (native) | No (single user implicit) | No (one user, multiple profiles) |
| **Per-user cost tracking** | Yes (token/model/task) | Partial (cost dashboard MVP) | No |
| **Cross-session persistence** | Full (PostgreSQL) | Partial (JSON state files) | Full (memory + skills + sessions) |
| **Context files** | User configs in DB | Team templates (TOML) | AGENTS.md / CLAUDE.md |
| **Model flexibility** | 13+ providers | 7-level resolution chain | Per-profile provider + model |

GoClaw answers "who are you?" with a TenantID — a database identity that propagates through every layer, tracks costs per user, and persists across sessions and devices. This is enterprise identity management.

ClawTeam answers "who are you?" with a team template — a TOML file that defines agent roles and model assignments. Identity is team-scoped, not user-scoped. The 7-level model resolution chain (CLI > agent model > agent tier > template strategy > template model > config default > None) enables mixed-model teams where Claude, GPT, and Qwen collaborate.

Hermes answers "who are you?" with a profile — a self-contained directory that separates personal from work contexts. Each profile has its own model, provider, keys, skills, and memory. The hermes-researcher analysis confirms: AGENTS.md and CLAUDE.md provide project-level context that persists across sessions alongside memory and skills.

**The key insight**: GoClaw separates users. ClawTeam separates agents. Hermes separates contexts. None of the three does all three.

---

## 5. Key Trade-offs Matrix

| Dimension | GoClaw | ClawTeam | Hermes-Agent |
|-----------|--------|----------|--------------|
| **Isolation strength** | ★★★★★ | ★★★☆☆ | ★★★★☆ |
| **Multi-user support** | ★★★★★ | ★☆☆☆☆ | ★★☆☆☆ |
| **Setup complexity** | ★★★★★ (hard) | ★★☆☆☆ (easy) | ★★☆☆☆ (easy) |
| **Scalability** | ★★★★★ | ★★★★☆ | ★★★☆☆ |
| **Security maturity** | ★★★★★ | ★★☆☆☆ | ★★★☆☆ |
| **State persistence** | ★★★★★ (PostgreSQL) | ★★★☆☆ (JSON files) | ★★★★☆ (SQLite + memory) |
| **Coordination overhead** | ★★★★☆ (heavy) | ★★★☆☆ (moderate) | ★★☆☆☆ (light) |
| **Best-fit team size** | 10-500 users | 1-5 parallel agents | 1 user, 2-5 contexts |
| **Credential management** | ★★★★★ | ★☆☆☆☆ | ★★★★☆ |

---

## 6. What Each Platform Can Learn from the Others

### GoClaw can learn from ClawTeam:
1. **Task dependency chains** — ClawTeam's TOML blocked-by chains with auto-unblock are more expressive than GoClaw's implicit team coordination. GoClaw could add explicit dependency tracking to its shared task boards.
2. **Cost dashboard** — ClawTeam v0.3.0's real-time cost aggregation by agent/model/task with circuit breaker states provides operational visibility that GoClaw's per-user cost tracking lacks at the agent level.

### GoClaw can learn from Hermes:
1. **Credential pool rotation** — Hermes' automatic failover on exhausted credentials (mark 401, rotate to next key) is more resilient than GoClaw's manual credential management.

### ClawTeam can learn from GoClaw:
1. **Credential encryption** — ClawTeam's plaintext TOML configs are a critical gap. GoClaw's AES-256-GCM per-user encryption should be adopted.
2. **Multi-tenant isolation** — ClawTeam's shared `~/.clawteam/` directory means all users on a shared system can see each other's state. GoClaw's per-tenant isolation model is needed for any team deployment.
3. **Audit logging** — ClawTeam's JSON state files are not structured audit trails. GoClaw's buffered persistence model enables compliance reporting.

### ClawTeam can learn from Hermes:
1. **Profile/context separation** — ClawTeam has no concept of separating personal from work contexts. Hermes' profile model would let teams operate under different configurations.

### Hermes can learn from ClawTeam:
1. **Inter-agent communication** — Hermes' delegate_task is fire-and-forget. ClawTeam's inbox + broadcast messaging enables agents to exchange intermediate results, not just final summaries.
2. **Task dependency tracking** — Hermes' todo list is flat. ClawTeam's dependency chains with auto-unblock would make multi-step delegation more autonomous.
3. **Monitoring visibility** — Hermes provides session transcripts. ClawTeam's kanban board + tiled tmux view gives real-time visibility into all agents simultaneously.

### Hermes can learn from GoClaw:
1. **RBAC** — Hermes lacks any role-based access control. Even a single-user agent could benefit from permission scopes (e.g., "read-only" for research profiles, "full-access" for dev profiles).
2. **Structured audit logging** — Hermes' debug logs cannot serve compliance needs. GoClaw's database-backed audit trail model is worth adopting for enterprise profiles.

---

## 7. Conclusion: The Fork Revisited

The AllClaws research thesis identifies a defining trend: the fork between personal-force-multiplier (1PC) and enterprise-automation paradigms. These three platforms illustrate the fork with unusual clarity:

**GoClaw** is unambiguously enterprise. PostgreSQL multi-tenancy, RBAC, AES-256-GCM encryption, buffered audit logging, per-user cost tracking — every architectural decision optimizes for the scenario where multiple organizations share infrastructure and accountability is non-negotiable. The cost is operational complexity: you need a database server, someone to maintain it, and a deployment model that justifies the overhead.

**ClawTeam** is a personal platform that reaches toward team coordination. It gives a single user the ability to spawn parallel agents, track dependencies, and merge results — the multi-agent intelligence that GoClaw lacks — but without any of the security or identity infrastructure that makes that safe at organizational scale. It is the best tool for a solo developer who wants swarm intelligence without enterprise overhead.

**Hermes-Agent** is a personal platform that reaches toward knowledge management. Its profile system provides the cleanest context separation of the three, its memory + skills system provides the richest cross-session persistence, and its credential pool rotation is the most operationally mature. But it has no multi-user story, no inter-agent communication, and no enterprise governance.

The fork is real, and no platform has bridged it yet. GoClaw cannot do swarm coordination. ClawTeam cannot do enterprise security. Hermes cannot do multi-tenant isolation. A platform that combined GoClaw's governance, ClawTeam's coordination, and Hermes' context management would represent a genuine synthesis — but the architectural commitments that make each good at its thing (PostgreSQL for GoClaw, git worktrees for ClawTeam, filesystem profiles for Hermes) are mutually exclusive at the implementation level.

The future likely belongs to platforms that adopt the *patterns* from each paradigm without the *implementation constraints*. Hermes adding RBAC and structured audit logging. ClawTeam adding credential encryption. GoClaw adding task dependency chains. The convergence has begun — the question is whether it accelerates or whether the fork hardens into permanently separate ecosystems.

---

*Synthesized from 12 analysis files across 3 virtual team members. All source material grounded in AllClaws architecture documentation at /home/dannyzeng/src/allclaws/architecture/.*
