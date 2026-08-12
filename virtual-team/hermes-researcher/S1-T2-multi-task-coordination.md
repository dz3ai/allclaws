# S1-T2: Multi-Task Coordination in Hermes-Agent

## Delegate Task System

Hermes-Agent supports concurrent task execution through **delegate_task tool spawning**. Unlike ClawTeam's leader-worker swarm pattern with explicit task boards, Hermes uses a simpler model: the main agent can spawn subagent processes to handle independent workloads. The `run_agent.py` codebase shows `_cap_delegate_task_calls()` and `_get_max_concurrent_children()` functions, enforcing a hard cap on parallel child tasks to prevent resource exhaustion.

### Inter-Agent Communication
Hermes does **not implement a dedicated inter-agent messaging protocol** like ClawTeam's inbox/broadcast system. Instead, child agents operate independently with isolated contexts. Communication between parent and child is implicit through delegated task descriptions, not real-time message passing. This contrasts with GoClaw's shared PostgreSQL state and ClawTeam's file-based JSON inboxes.

### Task Dependency Tracking
Unlike ClawTeam's explicit `blocked-by` task chains with auto-unblock, Hermes **lacks first-class task dependency management**. Subagents spawn in parallel but cannot declare or wait for dependencies. The architecture docs note Hermes as a "single-agent with context management" platform, not a multi-agent coordination system. Workflows requiring sequential execution must be orchestrated by the main agent through manual sequencing, not automated dependency resolution.

## Cron and Scheduled Jobs

Hermes provides **cron scheduling** through `~/.hermes/cron/jobs.json` and a ticker system (`ticker_heartbeat`, `ticker_last_success`). Scheduled jobs run as separate agent invocations with their own isolated sessions, enabling background task execution without blocking the main agent loop. This parallels Maxclaw's cron/once/every scheduling but lacks ClawTeam's real-time kanban board visualization.

## Parallel Execution Safety

Hermes enforces parallel safety through:
1. **Profile isolation** — Each subagent runs in its own profile context
2. **File locking** — Uses fcntl-style locks (`.auth.lock`, `.restart_pending.json`)
3. **State database isolation** — SQLite WAL files (`state.db-wal`, `state.db-shm`) handle concurrent reads
4. **Session isolation** — Child agents get independent session histories

However, unlike GoClaw's PostgreSQL ACID guarantees or IronClaw's WASM sandboxing, Hermes provides **no process-level containment**. The SECURITY.md confirms: "The only security boundary against an adversarial LLM is the operating system." Parallel tasks share the same Python interpreter environment.

## Comparison to Ecosystem

| Platform | Coordination | Dependency Tracking | Communication | Safety |
|----------|--------------|---------------------|---------------|--------|
| **ClawTeam** | Leader-worker swarms | Explicit `blocked-by` chains | Inbox/broadcast + P2P | Git worktree isolation |
| **GoClaw** | Lane-based scheduler | Shared task boards | PostgreSQL + WebSocket | Multi-tenant workspaces |
| **Hermes** | Delegate task spawning | Manual sequencing | Implicit (none) | Profile isolation only |

**Key Gap**: Hermes lacks enterprise-grade multi-agent coordination primitives. For complex parallel workflows with dependencies, ClawTeam or GoClaw are better choices. Hermes excels at single-agent context management, not multi-agent orchestration.