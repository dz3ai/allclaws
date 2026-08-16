# GoClaw Multi-Task Coordination Analysis

GoClaw implements multi-task coordination through a **lane-based scheduler** combined with agent teams and shared task boards. The platform enables concurrent task execution across multiple agents while maintaining safety and visibility.

## Agent Teams Architecture

GoClaw uses JSON-based team definitions to configure agent teams. Unlike ClawTeam's TOML-based templates or LangGraph's graph nodes, GoClaw's teams are declarative JSON configurations that specify:

- Team composition (agent count, roles)
- Agent-level model assignments (support for 13+ LLM providers)
- Tool permissions per agent
- Coordination patterns (delegation, parallel execution)

This JSON approach enables teams to be dynamically composed and reconfigured without code changes, supporting both human-curated teams and algorithmically generated team structures.

## Lane-Based Concurrency Scheduler

The core coordination mechanism is GoClaw's lane-based scheduler (`internal/scheduler/`), which manages four distinct execution lanes:

1. **Main Lane**: Primary user-facing agent interactions
2. **Subagent Lane**: Delegated sub-tasks spawned by main agents
3. **Delegate Lane**: Inter-agent delegation and handoff
4. **Cron Lane**: Scheduled and recurring tasks

This lane architecture prevents resource contention by isolating different task types into dedicated execution paths, ensuring that interactive user tasks aren't starved by background cron jobs or heavy delegation work.

## Shared Task Boards

Team coordination occurs through shared task boards persisted in PostgreSQL. Unlike ClawTeam's file-based inboxes, GoClaw's task boards provide:

- **Persistent state**: Tasks survive gateway restarts and crashes
- **Team visibility**: All agents in a team see the same task state
- **Dependency tracking**: Tasks can declare blocking relationships
- **Audit trails**: Every task transition is logged (key for compliance)

The shared task board enables agents to coordinate without direct messaging—an agent can claim a task, update its status, and release it for others to pick up, with all changes visible team-wide.

## Gateway Routing and Inter-Agent Communication

The gateway layer handles routing messages between agents, channels, and task boards. The architecture supports:

- **WebSocket RPC**: Real-time bidirectional communication for streaming responses
- **HTTP API**: REST endpoints for integrations and monitoring
- **Channel Manager**: Multi-channel support (Telegram, Discord, Slack, Feishu/Lark, Zalo, WhatsApp)

Inter-agent delegation occurs through the gateway's method router, which dispatches `delegate` tool calls to the appropriate agent lane. The gateway maintains the conversation context across delegation hops, enabling seamless handoffs between specialized agents.

## Parallel Execution Safety

GoClaw addresses parallel execution safety through multiple mechanisms:

1. **PostgreSQL row locking**: Concurrent task updates are serialized at the database layer
2. **Tenant scoping**: All operations are tenant-scoped, preventing cross-tenant interference
3. **Agent isolation**: Each agent operates with its own session context and tool permissions
4. **Rate limiting**: Per-session tool rate limiting prevents any single agent from monopolizing resources

## Key Distinction from Peer Platforms

GoClaw's multi-task coordination differs significantly from peer platforms:

- **vs ClawTeam**: GoClaw uses PostgreSQL-backed shared state vs ClawTeam's file-based inboxes, enabling richer querying and persistence at the cost of database dependency
- **vs Maxclaw**: GoClaw supports true concurrent multi-agent teams vs Maxclaw's sub-session spawning, with formal lane-based scheduling
- **vs LangGraph**: GoClaw's team-based pattern vs LangGraph's graph orchestration, with JSON team definitions instead of StateGraph nodes

The lane-based scheduler combined with PostgreSQL-backed task boards makes GoClaw particularly well-suited for enterprise deployments requiring durable coordination, audit trails, and high concurrency.