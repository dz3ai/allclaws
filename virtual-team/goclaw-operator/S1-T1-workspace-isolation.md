# GoClaw Workspace Isolation Analysis

GoClaw implements a robust multi-tenant architecture using PostgreSQL as its primary isolation boundary. The platform organizes work into **per-user workspaces** at the database layer, ensuring complete tenant separation through PostgreSQL's native row-level isolation mechanisms.

## Multi-Tenant PostgreSQL Model

GoClaw requires PostgreSQL 15+ as a mandatory component for production deployment. Unlike single-agent platforms that rely on file-based isolation or SQLite, GoClaw's architecture is built around a **shared PostgreSQL instance with per-tenant isolation**. Each user/workspace receives a distinct TenantID that propagates through every context in the system—from the gateway layer through agent dispatch to database queries.

## Isolation Boundary

The workspace isolation boundary operates at multiple layers:

1. **Database Layer**: PostgreSQL row-level isolation with TenantID scoping on all queries (`store.WithTenantID`). All user data, agent sessions, tools, and credentials are partitioned by tenant.

2. **Session Layer**: Per-user isolated sessions ensure that no conversation context, memory, or active work bleeds between tenants even when agents run concurrently on the same gateway instance.

3. **Channel Layer**: Multi-channel support (Telegram, Feishu/Lark, Zalo, Discord, WhatsApp) routes to tenant-specific sessions, preventing cross-tenant message leakage.

## Single Binary Deployment

Despite the multi-tenant complexity, GoClaw deploys as a single ~25 MB Go binary with zero runtime dependencies (except the PostgreSQL database). This contrasts with platforms requiring multiple containers or complex orchestration—the gateway handles all logic while PostgreSQL handles all persistence.

## Enterprise-Ready Isolation

The PostgreSQL approach enables GoClaw to support enterprise multi-tenant deployments where multiple organizations or departments share infrastructure without data exposure. This architecture scales horizontally through PostgreSQL's connection pooling and replication, while maintaining strict tenant isolation for compliance and security requirements.

## Key Distinction from Peer Platforms

Unlike ClawTeam's file-based isolation (`~/.clawteam/`) or Maxclaw's single-user SQLite model, GoClaw's PostgreSQL approach provides true multi-tenant isolation suitable for SaaS and enterprise deployment patterns. The database-backed isolation also enables rich querying across agent history, task states, and team coordination that file-based systems cannot efficiently support.