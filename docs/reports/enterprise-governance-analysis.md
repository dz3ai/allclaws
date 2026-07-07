# Enterprise Governance Frameworks Analysis

**Date:** 2026-07-07
**Scope:** Q3 2026 ROADMAP deliverable — credential isolation, HITL workflows, multi-tenant authorization, agent identity
**Platforms analyzed:** GoClaw, IronClaw, HiClaw, Hermes-Agent, NanoClaw, Nanobot, AgentScope

---

## Executive Summary

Enterprise agent governance has crystallized into four distinct architectural patterns, each solving a different governance dimension. No platform implements all four — the field is still fragmenting, not converging.

| Governance Dimension | Leading Platform | Pattern |
|---------------------|-----------------|---------|
| **Credential isolation** | IronClaw | Encrypted store + WASM injection (agent never sees secrets) |
| **Human-in-the-loop** | Hermes-Agent | Two-tier dangerous/hardline patterns + staged write approval |
| **Multi-tenant RBAC** | GoClaw | 5-layer permission model + per-tenant MCP grants |
| **Agent identity** | IronClaw | Attested signing chain (OAuth → WebAuthn → wallet) |

**The key finding:** governance maturity is bimodal. GoClaw, IronClaw, and Hermes have production-grade governance systems (400+ lines each, test-covered, audited). NanoClaw and Nanobot have adequate isolation but minimal governance. Orchestration frameworks (CrewAI, AutoGen, LangGraph) have almost no governance — they delegate to the application layer.

---

## Dimension 1: Credential Isolation

### The Problem

Agents need credentials to do useful work (API keys, OAuth tokens, database passwords). But giving an agent raw credentials creates two risks: (1) the agent leaks them via error messages, logs, or prompt injection; (2) the agent uses them for unauthorized actions.

### Pattern A: Encrypted Store + Host Injection (IronClaw)

**The most secure pattern — the agent never touches raw credentials.**

```
User stores secret → AES-256-GCM encrypt (per-secret HKDF-SHA256 key) → PostgreSQL
                                                                        ↓
WASM tool requests HTTP → Host checks allowed_secrets list → Decrypt in memory
                                                                        ↓
                                             Inject into HTTP request → WASM never sees value
                                                                        ↓
                                             Leak detector scans response → Return to WASM
```

| Component | File | Mechanism |
|-----------|------|-----------|
| Encryption | `src/secrets/crypto.rs` | AES-256-GCM with per-secret salt via HKDF-SHA256. Master key from OS keychain or `SECRETS_MASTER_KEY` env var. |
| Storage | `src/secrets/store.rs` | PostgreSQL `secrets` table with expiration checking and usage tracking |
| Access control | `allowed_secrets` column | Per-WASM-tool allowlist of which secrets it may use |
| Audit | `secret_usage_log` table | Every secret access logged: secret_id, wasm_tool_id, user_id, target_host |
| Leak detection | `leak_detection_events` table | Scans HTTP responses for secret values before returning to agent |

**Key code** (`src/secrets/mod.rs`):
```rust
//! WASM requests HTTP → Host checks allowlist → Decrypt secret (in memory only)
//! → Inject into request (WASM never sees value)
//! → Leak detector scans response for secrets
```

**Why it works:** WASM sandboxing means the agent code physically cannot access the host's memory. The host decrypts the secret, injects it into the HTTP request, and scans the response for leaks — all outside the WASM boundary.

### Pattern B: AI Gateway Proxy (HiClaw)

**Workers never see credentials — all tool calls are proxied.**

```
Worker agent → mcporter skill → Higress AI Gateway → MCP Server (GitHub, etc.)
                   ↓                                    ↑
             mcporter.json config              GitHub token injected here
             (no secrets, just server URLs)
```

| Component | File | Mechanism |
|-----------|------|-----------|
| mcporter CLI | `hiclaw/tests/test-12-github-mcp-tools.sh` | `docker exec Manager mcporter --config mcporter-servers.json call mcp-github.get_me` |
| Controller config | `hiclaw-controller/internal/agentconfig/mcporter.go` | Per-agent MCP server configuration, injected at container startup |
| Gateway | Higress AI Gateway | GitHub token lives in gateway config, not in worker container |

**Why it works:** The credential never enters the worker container. The worker calls `mcporter`, which routes through Higress, which injects the token. If the worker is compromised, there are no credentials to steal.

### Pattern C: AES Encryption + Env Filtering (GoClaw)

**API keys encrypted at rest; MCP server env vars validated.**

| Component | File | Mechanism |
|-----------|------|-----------|
| Encryption | `internal/crypto/aes.go` | AES-256-GCM with `"aes-gcm:"` prefix. API keys stored encrypted in `llm_providers` table. |
| Env denylist | `internal/crypto/env_denylist.go` | Blocks dangerous env vars: `PATH`, `HOME`, `LD_PRELOAD`, `NODE_OPTIONS`, `PYTHONPATH`, `BASH_ENV`, `GIT_SSH_COMMAND`, `SSH_AUTH_SOCK` |
| Per-user credentials | `internal/mcp/manager.go:219` | `resolveServerCredentials()` merges server defaults with per-user credentials. Servers requiring per-user credentials are not connected at startup — connections created via `pool.AcquireUser()`. |

**Env denylist** (`env_denylist.go`): 25+ blocked env vars including Shellshock-class injection vectors (`BASH_ENV`, `ENV`), path hijacking (`LD_PRELOAD`, `LD_LIBRARY_PATH`), and interpreter injection (`NODE_OPTIONS`, `PYTHONPATH`).

### Pattern D: Config-Based + OSV Preflight (Hermes-Agent)

**Lightweight isolation — env filtering + malware scanning for stdio MCP servers.**

| Component | File | Mechanism |
|-----------|------|-----------|
| Env filtering | `tools/mcp_tool.py` | Only explicitly configured `env` keys passed to stdio subprocesses |
| OSV malware check | `tools/mcp_tool.py:112` | 12-second timeout, fail-open — checks MCP server package against OSV vulnerability database |
| Suspicious server filter | `tools/mcp_tool.py:3315` | `_filter_suspicious_mcp_servers()` rejects servers with suspicious patterns |

### Comparison

| Feature | IronClaw | HiClaw | GoClaw | Hermes |
|---------|----------|--------|--------|--------|
| Encryption at rest | ✅ AES-256-GCM + HKDF | N/A (gateway holds) | ✅ AES-256-GCM | ❌ |
| Agent sees credentials | ❌ Never (WASM) | ❌ Never (proxy) | ✅ At runtime | ✅ At runtime |
| Per-user credentials | ✅ | ✅ (per-worker) | ✅ | ❌ |
| Env var filtering | ❌ | N/A | ✅ (25+ blocked) | ✅ |
| Secret usage audit | ✅ (DB table) | ❌ | ❌ | ❌ |
| Leak detection | ✅ (response scanning) | ❌ | ❌ | ❌ |
| Malware preflight | ❌ | ❌ | ❌ | ✅ (OSV) |

---

## Dimension 2: Human-in-the-Loop (HITL) Approval Workflows

### Pattern A: Two-Tier Dangerous/Hardline (Hermes-Agent)

**The most nuanced approval system — distinguishes "dangerous" from "unconditionally blocked."**

| Layer | Pattern | Action |
|-------|---------|--------|
| `HARDLINE_PATTERNS` | `rm -rf /`, `mkfs`, `dd of=/dev/sd*`, fork bombs, shutdown, `sudo -S` | **Unconditional block** — no bypass possible, not even YOLO mode |
| `DANGEROUS_PATTERNS` | Writes to `~/.ssh/`, `.env`, `config.yaml`, shell RCs, `/etc/` | **Approval-gated** — user must approve; YOLO mode bypasses |

**Write approval gates:** Separate gates for memory (`memory.write_approval`) and skills (`skills.write_approval`). When enabled, all writes stage to `~/.hermes/pending/` for review via `/memory pending` or `/skills pending`.

**Dual-channel delivery:**
- CLI: synchronous blocking via prompt_toolkit callback
- Gateway/messaging: enqueues approval, agent thread blocks on `threading.Event` (5-min timeout), user approves via `/approve` or `/deny` in chat

### Pattern B: Composable Gate Pipeline (IronClaw)

**The most extensible approval system — priority-sorted gates, first Pause/Deny wins.**

```
GatePipeline (sorted by priority)
├── RateLimitGate (50)        → per-user per-tool rate limiting
├── RelayChannelGate (80)     → auto-deny approval-requiring tools on relay channels
├── ApprovalGate (100)        → core HITL check
├── AuthenticationGate (200)  → credential presence
└── HookGate (300)            → BeforeToolCall hooks (fail-open)
```

Four execution modes change the decision matrix:

| Mode | UnlessAutoApproved | Always |
|------|-------------------|--------|
| `Interactive` | Pauses for approval | Always pauses |
| `InteractiveAutoApprove` | Auto-allows | Still pauses |
| `Autonomous` | Allowed | **Denied** (cannot run) |
| `Container` | Allow all | Allow all |

Per-tool `requires_approval(params) → ApprovalRequirement`: `Never`, `UnlessAutoApproved`, `Always`. "Always allow" decisions persisted to DB (survives crashes).

### Pattern C: Admin Hierarchy DM Routing (NanoClaw)

**The most messaging-native approval system — designed for platform-as-channel deployments.**

Approver resolution: `pickApprover()` walks scoped admins → global admins → owners. Deliveries via DM cards with `Approve` / `Reject` / `Reject with reason` buttons.

### Pattern D: Static Sandbox Policy (Nanobot)

**No human in the loop — automated policy enforcement via sandboxing.**

- `bubblewrap` (bwrap) sandbox: read-only system mounts, tmpfs workspace masking
- `deny_patterns` (blacklist) + `allow_patterns` (whitelist, takes priority)
- Chained-command protection: `echo hello; rm -rf /` still blocked

### Pattern E: RBAC + WebSocket (GoClaw)

**Enterprise approval with role-based access control.**

5-layer permission model:
1. Gateway Auth (token scopes: admin/read/write/approvals/pairing/provision)
2. Global Tool Policy (allow/deny lists)
3. Per-Agent Policy
4. Per-Channel Policy
5. Owner-Only Tools

Roles: Owner(4) > Admin(3) > Operator(2) > Viewer(1). Fail-closed: unclassified methods return `RoleNone` → denied for everyone.

### Pattern F: Mode-Driven Permission Engine (AgentScope)

**5 permission modes with 3 rule layers (deny/ask/allow):**

| Mode | Behavior |
|------|----------|
| `DEFAULT` | Most restrictive — every operation asks |
| `EXPLORE` | Read-only — writes denied |
| `ACCEPT_EDITS` | Working-directory writes auto-allowed |
| `BYPASS` | Safety-ASK immunity disabled (deny rules remain as guardrails) |
| `DONT_ASK` | No user available — ASK converted to DENY |

Bypass-immune ASK: dangerous operations that no allow rule can convert. In `DONT_ASK` mode, converted to DENY (fail-safe).

### Comparison

| Feature | Hermes | IronClaw | NanoClaw | Nanobot | GoClaw | AgentScope |
|---------|--------|----------|----------|---------|--------|-----------|
| **Gated actions** | Shell, memory, skills | All tools | Self-mod, credentials | Shell (static) | Shell (exec) | All tools |
| **Approver** | User inline | User via web/TUI | Admins via DM | None (automated) | Operator+ via WS | User (mode-driven) |
| **Sync model** | Sync blocking | Async (Pause/Resume) | Async (fire-and-forget) | Sync (immediate) | Sync blocking | Mode-dependent |
| **Persistence** | config.yaml + pending/ | DB (crash-safe) | SQLite table | None | In-memory only | Mode context |
| **Unconditional floor** | ✅ Hardline blocklist | Autonomous denies Always | Privilege-based | Built-in deny_patterns | safeBins/allowlist | Bypass-immune ASK |
| **Multi-approver** | ❌ | ❌ | ✅ (admin hierarchy) | N/A | ✅ (RBAC roles) | ❌ |
| **Audit trail** | ❌ | ✅ (DB) | ✅ (SQLite) | ❌ | ✅ (event bus) | ❌ |

---

## Dimension 3: Multi-Tenant Authorization & Identity

### GoClaw — The Reference Enterprise RBAC

**5-layer permission model with hierarchical roles and per-tenant MCP grants:**

```
Layer 1: Gateway Auth (token + scopes)
Layer 2: Global Tool Policy (allow/deny lists, profile)
Layer 3: Per-Agent Policy (agents.list[].tools.allow/deny)
Layer 4: Per-Channel/Group Policy (channels.*.groups.*.tools.policy)
Layer 5: Owner-Only Tools (senderIsOwner check)
```

**MCP per-tenant authorization** (`grant_checker.go`): Each tenant can have allow/deny lists for MCP tools. Semantics: deny takes priority; non-empty allow means only listed tools visible; empty allow+deny means no filter.

**Tenant isolation:** Multi-tenant deployment mode with per-tenant tool visibility, memory isolation, and rate limiting.

### IronClaw — Attested Signing + Multi-Tenant Admin Policy

**The only platform with cryptographic agent identity.**

Multi-tenant mode (`main.rs:836`): `config.is_multi_tenant_deployment()` enables admin tool policy filtering. `SystemScope` tracks per-tenant rate limits (`TenantRateRegistry`).

**Secret model** (`secrets/types.rs`): Secrets are per-user (`user_id`), with per-WASM-tool access control (`allowed_secrets`). The `secret_usage_log` table provides full audit trail.

**Attested signing chain** (from June-July report):
```
OAuth Provider Trait → Wire Hardening → Grant Ledger → WebAuthn Challenge/Audit
→ Turns Resume → Chain Signing → Injected Provider → NEAR Redirect → WalletConnect
→ Reborn Runtime → WebUI Ingress → Durable Stores → Loop Raise
```

This gives IronClaw the only cryptographic agent identity system: agents prove who they are via wallet-based signing, and their actions are attested on-chain.

### HiClaw — Kubernetes CRD Model

**Agent identity expressed as Kubernetes Custom Resource Definitions:**

| CRD | Represents |
|-----|-----------|
| `Worker` | An AI agent worker (spec: runtime, image, config) |
| `Manager` | An orchestrator agent (spec: runtime, skills) |
| `Team` | A collection of workers + manager (spec: members, lead) |
| `Human` | A human participant (spec: role, matrix ID) |

Human roles are first-class Kubernetes objects — not just config entries. This means RBAC, audit, and lifecycle management leverage the entire Kubernetes operator ecosystem.

### AgentScope — Mode-Driven Permission Engine

**5 permission modes with 3-layer rule evaluation:**

```
PermissionRule evaluation order:
1. DENY rules (always block)
2. ALLOW rules (auto-approve)
3. ASK rules (prompt user, subject to mode rules)
4. PASSTHROUGH (no rule matches → mode default)
```

The `bypass_immune` flag on ASK rules prevents even BYPASS mode from auto-approving dangerous operations. This is a sophisticated safety mechanism — the system can say "this is always dangerous, regardless of user mode."

---

## Governance Maturity Matrix

| Dimension | GoClaw | IronClaw | HiClaw | Hermes | NanoClaw | Nanobot | AgentScope |
|-----------|--------|----------|--------|--------|----------|---------|-----------|
| **Credential isolation** | ★★★ | ★★★★★ | ★★★★ | ★★ | ★★★ | ★★ | ★ |
| **HITL approval** | ★★★★ | ★★★★ | ★★★ | ★★★★★ | ★★★ | ★★ | ★★★★ |
| **Multi-tenant RBAC** | ★★★★★ | ★★★★ | ★★★★ | ★ | ★★ | ★ | ★★★ |
| **Agent identity** | ★★ | ★★★★★ | ★★★★ | ★ | ★★ | ★ | ★ |
| **Audit trail** | ★★★ | ★★★★★ | ★★ | ★ | ★★★ | ★ | ★ |
| **Overall** | ★★★★ | ★★★★★ | ★★★★ | ★★★ | ★★★ | ★★ | ★★★ |

---

## Emerging Patterns

### 1. The Two-Excellence Gap

No platform excels at all four governance dimensions. The closest:
- **IronClaw** — 5 stars on credentials and identity, 4 on RBAC and HITL
- **GoClaw** — 5 stars on RBAC, 4 on HITL, 3 on credentials and identity

These two platforms are converging on the "enterprise agent gateway" position but from opposite directions: IronClaw from security/identity, GoClaw from multi-tenancy/operations.

### 2. The Sandbox-vs-Approval Divergence

Two fundamentally different philosophies for agent safety:

| Philosophy | Platforms | Approach |
|-----------|----------|----------|
| **Approve everything dangerous** | Hermes, IronClaw, GoClaw | Interactive HITL — ask the human |
| **Sandbox everything untrusted** | Nanobot, agent-zero, NanoClaw | Container/bwrap isolation — no human needed |

Nanobot's approach (sandbox + static policy, no human) is simpler but less flexible. The approve-everything approach is more powerful but requires a human in the loop, which doesn't scale to autonomous deployments.

### 3. AgentScope's Mode System is the Most Nuanced

AgentScope's 5 permission modes (DEFAULT → EXPLORE → ACCEPT_EDITS → BYPASS → DONT_ASK) represent the most sophisticated approach to the "how much should the agent be allowed to do" question. The `bypass_immune` flag — operations that even BYPASS mode cannot auto-approve — is a pattern every platform should adopt.

### 4. Credential Proximity Determines Risk

The platforms rank cleanly by how close the agent gets to raw credentials:

```
IronClaw (never sees) → HiClaw (never sees) → GoClaw (sees at runtime) → Hermes (sees at runtime) → Nanobot (has filesystem access)
```

IronClaw's WASM boundary and HiClaw's gateway proxy are architecturally superior to runtime decryption — the agent literally cannot leak what it cannot access.

---

## Recommendations

### For Platform Developers

1. **Adopt the bypass-immune pattern** (AgentScope). Every approval system needs operations that no mode can auto-approve. Hermes' hardline blocklist is the simplest version; AgentScope's per-rule flag is the most flexible.

2. **Persist approval state to a database** (IronClaw pattern). GoClaw loses pending approvals on restart — unacceptable for audit compliance.

3. **Implement credential proximity minimization.** The further credentials are from the agent runtime, the better. IronClaw's WASM injection and HiClaw's gateway proxy are the gold standards.

4. **Adopt composable gate pipelines** (IronClaw pattern) instead of monolithic approval functions. Priority-sorted gates allow incremental addition of governance policies without rewriting the core.

### For Enterprise Deployers

1. **GoClaw is the most operationally ready** for multi-tenant deployments with its 5-layer permission model and per-tenant MCP grants.

2. **IronClaw is the most security-ready** with encrypted credential storage, WASM isolation, attested signing, and full audit trails.

3. **HiClaw is the most Kubernetes-native** with CRD-based agent identity and operator-managed lifecycle.

4. **Hermes is the best for personal-sovereign deployments** where the user is the approver, with the most nuanced dangerous/hardline pattern distinction.

### The Unfilled Gap

No platform combines:
- IronClaw's WASM credential isolation
- Hermes' two-tier dangerous/hardline approval
- GoClaw's 5-layer multi-tenant RBAC
- AgentScope's bypass-immune mode system
- HiClaw's K8s-native agent identity

The first platform to integrate all five will define the enterprise agent governance standard.

---

*This report completes the Q3 2026 ROADMAP item #3: Enterprise Governance Frameworks Analysis.*
*Related: [Design Paradigm Analysis](design-paradigm-analysis-30-platforms.md), [MCP Deep-Dive](mcp-deep-dive-phase4-5-synthesis.md)*
