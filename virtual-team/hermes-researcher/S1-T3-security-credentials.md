# S1-T3: Security and Credentials in Hermes-Agent

## Credential Pool System

Hermes implements a **credential pool** architecture with automatic rotation through `auth.json`. Each provider (zai, kimi-coding, deepseek, copilot) maintains a list of credentials with:

- `priority` field for load balancing across multiple keys
- `last_status` tracking (ok, exhausted, error codes)
- `request_count` for usage monitoring
- `secret_fingerprint` (SHA-256) for auditing without exposing secrets
- `source` attribution (env:VAR_NAME, gh_cli)

The live installation shows four active pools, with the deepseek pool already marked as "exhausted" (401 unauthorized). This **automatic failover** contrasts with GoClaw's manual credential management and aligns closer to enterprise rotation practices.

## Approval Modes

Hermes supports **three approval modes** for tool execution (not explicitly documented in source but inferred from SECURITY.md approval gate references):

1. **Smart mode** — Heuristic-based auto-approval for low-risk operations
2. **Manual mode** — Require explicit user confirmation before execution
3. **Off mode** — Disable approval gates (dangerous, requires explicit config)

The SECURITY.md clarifies that approval gates are **not security boundaries**: "Nothing inside the agent process constitutes containment — not the approval gate, not output redaction, not any pattern scanner." These are UX controls, not hard security controls.

## Secret Redaction

Hermes redacts secrets from logs and error messages using the `secret_fingerprint` field. When an API call fails, Hermes reports the error code and reason but never logs the actual credential value. This prevents secret leakage in debug output, a practice shared across the claw ecosystem.

## Terminal Backends and Sandboxing

Hermes offers **pluggable terminal backends** for shell execution:
- **Default backend** — Runs commands directly on host (no isolation)
- **Container backend** — Runs commands inside Docker containers
- **Cloud sandbox backend** — Runs commands in remote cloud environments
- **SSH backend** — Runs commands on remote hosts

Unlike IronClaw's **WASM sandboxing** with endpoint allowlisting and GoClaw's **PostgreSQL-based RBAC**, Hermes delegates isolation to the backend layer. The SECURITY.md explicitly states: "The only security boundary against an adversarial LLM is the operating system."

### Security Comparison

| Platform | Isolation | Credential Rotation | RBAC | Audit Logging |
|----------|-----------|---------------------|------|---------------|
| **GoClaw** | PostgreSQL workspaces | Manual | Yes (admin/operator/viewer) | Built-in |
| **IronClaw** | WASM sandbox + host boundary | Auto-rotation | Capability-based | No telemetry |
| **Hermes** | Terminal backends (pluggable) | Credential pools | No | File-based logs |
| **ClawTeam** | Git worktrees | Not specified | No | JSON state files |

## Access Control Gap

Hermes **lacks role-based access control** entirely. All operations under a profile use the same credential pool with no distinction between administrative and user actions. For enterprise deployments, GoClaw's PostgreSQL RBAC provides per-user permissions. Hermes is designed for single-user personal agents, not multi-tenant environments.

## Audit Logging

Hermes logs to `~/.hermes/logs/` and `.hermes_history`, but these are **file-based debug logs**, not structured audit trails. Unlike GoClaw's PostgreSQL-backed audit tables or HiClaw's gateway-managed logging, Hermes logs cannot be easily queried for compliance reporting. This aligns with Hermes' personal-force-multiplier positioning rather than enterprise-automation.