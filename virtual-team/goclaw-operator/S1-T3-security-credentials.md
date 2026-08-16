# GoClaw Security & Credentials Analysis

GoClaw implements a **5-layer production security defense** framework that addresses the hardest enterprise AI governance challenges: credential isolation, audit logging, access control, and execution safety. The platform's security model is designed for multi-tenant deployments where multiple organizations share infrastructure.

## Credential Management and Encryption

GoClaw stores secrets using **AES-256-GCM encryption** with per-user credential isolation. The architecture follows a critical security principle: credentials never cross the LLM boundary. Instead, credentials are:

1. Stored encrypted at rest in the PostgreSQL `config_secrets` table
2. Retrieved only during tool execution (not exposed to agent reasoning)
3. Injected at the call time directly to the tool, bypassing the LLM context

This approach ensures that even if an LLM is prompted to reveal credentials, the credentials are never present in the agent's conversation context. The per-user isolation guarantees that Tenant A's API keys cannot be accessed by Tenant B's agents, even through misconfiguration or bugs.

## RBAC: Admin/Operator/Viewer Model

GoClaw implements a three-tier RBAC system with `permissions.PolicyEngine` enforcing role-based permissions:

- **Admin**: Full system access, can modify all configurations, override approval gates
- **Operator**: Can execute most operations but limited to specific actions
- **Viewer**: Read-only access for monitoring and auditing

The RBAC system operates at multiple granularities:

- **Tenant-level**: Roles control access to entire tenant workspaces
- **Agent-level**: Permissions can be scoped to specific agents within a tenant
- **Tool-level**: Fine-grained control over which agents can use which tools

Every RPC method call checks RBAC permissions before execution, with owner IDs propagated through all request contexts for authorization decisions.

## Exec Approval and Allowlists

GoClaw provides configurable execution approval modes for controlling shell commands and risky operations:

```go
type ExecAskMode string
const (
    ExecAskNever  ExecAskMode = "never"   // Auto-approve all
    ExecAskAlways ExecAskMode = "always"  // Ask for every exec
    ExecAskRisky  ExecAskMode = "risky"   // Ask for non-allowlisted
)
```

The **exec approval allowlist** allows pre-approved commands (e.g., `git`, `npm`, `cargo`, `go`) to execute without manual approval, while blocking or prompting for unknown commands. Admins and operators can bypass approval gates based on role—this provides flexibility for trusted users while maintaining safety controls for broader access.

## Audit Logging Architecture

GoClaw has the most complete audit implementation among tracked platforms, with a pipeline that ensures comprehensive event capture without blocking agent execution:

```
EventEmitter -> MessageBus (TopicAudit)
    -> Buffered Channel (256)
        -> ActivityLog Persister (PostgreSQL)
            -> activity_logs table (tenant-scoped)
```

Key audit event types include:

- **MCP server lifecycle**: `created/updated/deleted/reconnected`
- **MCP grants**: `agent_granted/revoked`, `user_granted/revoked`
- **Team task events**: All lifecycle state changes
- **Security events**: `mcp.server_rejected`, `mcp_bridge_disabled`

The buffered channel (capacity 256) prevents audit from blocking agent execution during high-throughput periods. When the queue fills, GoClaw emits a warning (`audit.queue_full`) but continues operation rather than blocking agents. All audit entries are tenant-scoped, and graceful shutdown flushes pending entries before exit.

## Additional Security Layers

GoClaw's 5-layer defense includes:

1. **Rate limiting**: Per-session tool rate limiting with sliding window prevents DoS attacks and resource exhaustion
2. **Prompt injection detection**: Input sanitization identifies and blocks adversarial prompts
3. **SSRF protection**: Internal network boundary prevents agents from accessing internal services
4. **Shell deny patterns**: Command-level filtering blocks dangerous shell constructs
5. **AES-256-GCM encryption**: Secrets encrypted at rest with per-tenant keys

## Key Distinction from Peer Platforms

GoClaw's security model differs significantly from alternatives:

- **vs IronClaw**: GoClaw uses encrypted PostgreSQL storage vs IronClaw's host-boundary injection; both prevent LLM exposure but GoClaw trades WASM security for database portability
- **vs HiClaw**: GoClaw's RBAC is per-tenant/per-agent/per-tool vs HiClaw's per-team/pod model; GoClaw provides finer granularity within a shared database
- **vs LangGraph/CrewAI**: GoClaw has comprehensive audit logging and credential encryption vs minimal security infrastructure in external frameworks

The combination of AES-256-GCM encryption, comprehensive audit logging, multi-layer RBAC, and exec approval controls makes GoClaw the most enterprise-ready platform in the AllClaws ecosystem for regulated environments requiring strong governance.