# GoClaw Profile & Identity Analysis

GoClaw implements user identity and profile management through its PostgreSQL-backed persistence layer, enabling multi-tenant deployments with per-user state, cost tracking, and cross-session continuity.

## PostgreSQL Persistence Layer

GoClaw requires PostgreSQL 15+ as its primary data store, not as an optional add-on. All user state—including identity, sessions, memories, tools, credentials, and cost tracking—persists in PostgreSQL with pgvector extension for hybrid search capabilities. The persistence architecture spans multiple tables:

- **Users/tenants**: Identity and authentication data
- **Sessions**: Conversation history with full context retention
- **Memories**: Hybrid search using pgvector for semantic + full-text retrieval
- **Tools**: Custom tool definitions and MCP server configurations
- **Credentials**: AES-256-GCM encrypted secrets per user
- **Activity logs**: Audit trails for compliance and debugging

This database-backed approach ensures that user state survives gateway restarts, enables complex queries across historical data, and supports enterprise-scale deployments with high availability through PostgreSQL replication.

## User Identity and Separation

GoClaw separates users through a **TenantID** that propagates through every layer of the system:

1. **Gateway layer**: WebSocket RPC and HTTP API requests include TenantID for request routing
2. **Agent layer**: Agent sessions are scoped to TenantID, preventing cross-tenant context contamination
3. **Database layer**: All queries use `store.WithTenantID` to enforce row-level isolation
4. **Audit layer**: Activity logs are tenant-scoped, enabling per-organization compliance reports

Unlike personal agent platforms that assume a single user (e.g., Maxclaw's local-first model, Nanobot's per-user CLI), GoClaw is designed from the ground up for multi-user environments where multiple organizations or departments share the same gateway instance without data exposure.

## Cross-Session Continuity

GoClaw provides **persistent user identity** across sessions through several mechanisms:

- **Session continuity**: Conversation history persists in PostgreSQL, allowing users to resume conversations across browser sessions, devices, or days
- **Memory layer**: Long-term knowledge storage using pgvector enables semantic search across all historical interactions
- **Skill system**: User-defined SKILL.md files with BM25 search persist per tenant, enabling reusable workflows and knowledge
- **Config persistence**: User configurations (provider settings, channel bindings, team definitions) survive gateway restarts

The platform does not implement ephemeral sessions by default—all state is persistent, which suits enterprise use cases where history preservation and auditability are requirements.

## Per-User Cost Tracking

GoClaw tracks costs on a per-user basis, enabling:

- **Token/cost aggregation by agent**: Track which agents consume the most tokens
- **Cost aggregation by model**: Compare usage across different LLM providers (13+ supported)
- **Cost aggregation by task**: Attribute costs to specific work items or projects

This cost tracking is implemented at the PostgreSQL layer with per-tenant queries, enabling organizations to bill departments accurately, identify expensive workflows, and optimize model selection. The cost data integrates with the audit logging system, providing a complete picture of resource consumption alongside operational logs.

## Comparison to Peer Platforms

GoClaw's profile and identity approach differs significantly from personal agent platforms:

- **vs Maxclaw**: GoClaw provides PostgreSQL-backed multi-user identity vs Maxclaw's single-user local filesystem (MEMORY.md, HISTORY.md); GoClaw scales to hundreds of users, Maxclaw is optimized for one developer
- **vs Nanobot**: GoClaw has database-backed cost tracking vs Nanobot's minimal state model; GoClaw targets enterprise billing, Nanobot targets individual productivity
- **vs IronClaw**: Both use PostgreSQL for persistence, but GoClaw focuses on multi-tenant identity while IronClaw emphasizes local-first data sovereignty with system keychain integration
- **vs OpenClaw**: GoClaw has built-in user identity and cost tracking vs OpenClaw's single-user CLI paradigm; GoClaw is enterprise-grade by design, OpenClaw is personal-force-multiplier focused

The PostgreSQL persistence layer combined with per-user cost tracking makes GoClaw uniquely suited for organizations that need to operationalize AI agents at scale—where accountability, cost attribution, and auditability are non-negotiable requirements.

## Browser Pairing for Identity Establishment

GoClaw supports browser-based pairing using 8-character codes for initial identity establishment. This mechanism allows users to connect web dashboards or mobile interfaces to their gateway instance without complex authentication setup, making onboarding accessible while maintaining the underlying PostgreSQL-backed identity model.