---
layout: post
title: "I Put Three AI Agents on a Team. Here's What They Taught Me About the Future of Agent Platforms."
date: 2026-08-12 15:30:00 +0800
author: Danny Zeng
categories: [Research, Experiment]
tags: [multi-agent, virtual-team, platform-comparison, goclaw, clawteam, hermes-agent, architecture, experiment]
---

I've spent six months tracking 30 AI agent platforms for the AllClaws project. I've read their source code, compared their architectures, cataloged their failure modes. But reading about how agents work is different from watching them work. So I tried something unusual: I built a virtual research team where three different AI agent platforms collaborated on the same research tasks, and I tracked everything they produced.

The experiment was simple in concept. I created three team members, each powered by a different platform from a fundamentally different architectural paradigm:

| Member | Platform | Language | Paradigm |
|--------|----------|----------|----------|
| **goclaw-operator** | GoClaw | Go | Enterprise multi-tenant gateway |
| **clawteam-lead** | ClawTeam | Python | Multi-agent swarm coordination |
| **hermes-researcher** | Hermes-Agent | Python | Profile-based personal agent |

I gave them a shared task board with four research questions about their own platforms — workspace isolation, multi-task coordination, security, and identity models — then a fifth synthesis task that required reading each other's output. Each member investigated their own platform's internals and committed findings as markdown files.

Over the course of a sprint, the team produced 13 markdown files: 4 per member plus a cross-platform synthesis. Here's what I learned.

---

## The Experiment: Structure and Setup

The task board was straightforward. Each member received identical research prompts about four dimensions of their platform:

1. **S1-T1: Workspace & Project Isolation** — How does the platform organize work? What is the isolation boundary?
2. **S1-T2: Multi-Task & Multi-Agent Coordination** — How does it handle concurrent tasks? Inter-agent communication?
3. **S1-T3: Security & Credential Management** — How does it handle secrets, sandboxing, audit?
4. **S1-T4: Profile / Identity Model** — How are users and contexts separated?

The fifth task (S1-T5) was a synthesis — compare all three approaches, identify trade-offs, and suggest what each platform could learn from the others.

Each member worked from the same source material: the AllClaws architecture documentation and the actual platform source code (available as git submodules in the parent repo). They couldn't talk to each other directly. Coordination happened through commit messages referencing other members' work.

The whole thing lived in a git repo with structured naming: `virtual-team/<member>/S1-T<task#>-<short-name>.md`. No project management tool. No Slack channel. No standup meetings. Just git commits and markdown files.

---

## What Happened

### The Three Paradigms, Through Their Own Eyes

Each member produced detailed technical analysis rooted in actual code — not marketing copy, not documentation summaries, but architecture drawn from reading source.

**goclaw-operator** delivered enterprise-grade analysis befitting its platform. Its workspace isolation analysis documented how GoClaw propagates a TenantID through every layer — gateway routing, agent dispatch, database queries (`store.WithTenantID`), and audit logging. Its security analysis was the most thorough of any member, detailing a 5-layer defense: AES-256-GCM encryption, RBAC (admin/operator/viewer), exec approval allowlists, buffered audit logging via Go channels (capacity 256), and rate limiting. The analysis read like a security audit — precise, implementation-specific, and unsparing.

**clawteam-lead** produced analysis focused on coordination primitives. Its workspace isolation document explained git worktree-based architecture — each worker agent gets its own worktree from the parent repo, eliminating merge conflicts. Its multi-task coordination analysis was the richest of any member, documenting TOML-based `blocked-by` dependency chains with automatic unblocking, dual-mode inter-agent communication (point-to-point inboxes plus broadcast), and a concrete performance claim: 5 parallel agents completing a full-stack app in ~3 hours vs 8+ hours sequential, a 2.7x speedup at the same token cost.

**hermes-researcher** delivered the most introspective analysis, grounded in an actual running installation. It confirmed two active profiles (`personal` at 1.9MB state.db, `work` at 368KB WAL), documented credential pool rotation (mark 401, rotate to next key), and provided the clearest explanation of how profile-based isolation works in practice. Its analysis was the most candid about limitations: "Nothing inside the agent process constitutes containment," quoting directly from the platform's SECURITY.md.

### The Synthesis: Where the Three Paradigms Collide

The cross-platform synthesis (S1-T5) was the payoff. It compared all three platforms across each dimension and produced the most useful output of the entire experiment: a structured matrix of trade-offs.

Here's what emerged:

**On workspace isolation, the fundamental fork revealed itself.** GoClaw isolates by *identity* (who you are — TenantID in every database query). ClawTeam isolates by *task* (what you're doing — git worktree per agent). Hermes isolates by *context* (which role you're in — profile directory per use case). None of the three does all three. GoClaw cannot separate contexts for the same user. ClawTeam cannot separate users. Hermes cannot separate tasks.

**On coordination, the maturity spectrum was stark.** ClawTeam has the most sophisticated system: explicit dependency chains, inter-agent inboxes, broadcast messaging, kanban monitoring. GoClaw has database-backed team coordination without direct messaging. Hermes has fire-and-forget delegation with no inter-agent communication at all. The gap between ClawTeam's "agents exchange intermediate results" and Hermes' "agents return final summaries" is not incremental — it's architectural.

**On security, the divide between enterprise and personal was obvious but not simple.** GoClaw leads decisively: encrypted credentials, RBAC, structured audit logging, per-tenant isolation. But the synthesis highlighted an interesting middle position. Hermes' automatic credential pool rotation — exhausting a 401'd key and rotating to the next — is *more operationally mature* than GoClaw's manual credential management. The best security model would combine GoClaw's governance with Hermes' operational automation.

**On identity, each platform answers a different question.** GoClaw: "Who are you?" (TenantID). ClawTeam: "What team are you on?" (TOML template). Hermes: "What hat are you wearing?" (profile directory). The insight is that these are not competing answers — they're answering different questions that real users have simultaneously.

---

## The Meta-Lesson: Agents Can Do Comparative Research

Before discussing platform implications, there's a meta-level finding: **the experiment worked**.

Three AI agents, each with access to the same source material but running on different platforms with different prompting strategies, produced 13 files of grounded technical analysis. The synthesis document cross-referenced findings across members, identified non-obvious trade-offs, and suggested actionable improvements for each platform — all without a human writing a single paragraph.

This matters because comparative platform analysis is exactly the kind of work that is:
- **Labor-intensive**: Reading source code across three codebases is hours of human effort
- **Structured**: The output format is well-defined (markdown, tables, comparisons)
- **Grounded**: You can verify claims against actual code
- **Boring**: Nobody wants to spend a weekend comparing RBAC implementations

AI agents are good at all four of these properties. The key was providing structured task definitions, a shared evidence base, and a clear output format. The agents did the rest.

But — and this is critical — the synthesis quality depended entirely on the individual analysis quality. When clawteam-lead was specific about TOML dependency chains, the synthesis could compare them precisely. When goclaw-operator detailed the audit pipeline (EventEmitter -> Buffered Channel -> PostgreSQL), the synthesis could contrast it accurately. Vague analysis would have produced vague synthesis. The structure of the experiment mattered as much as the agents.

---

## Implications for Agent Platform Design

### 1. The Fork Is Real, and It's Hardening

The AllClaws research has identified a defining trend: the fork between **personal-force-multiplier** and **enterprise-automation** paradigms. This experiment made the fork visible in a new way — not by reading documentation, but by watching how agents from each paradigm reason about the same problems.

GoClaw's goclaw-operator thinks in terms of tenants, policies, and compliance. ClawTeam's clawteam-lead thinks in terms of agents, tasks, and merge conflicts. Hermes' hermes-researcher thinks in terms of profiles, memory, and context switching. These are not different implementations of the same abstraction — they are different *abstractions entirely*.

The implication: we are not converging on a single agent platform architecture. We are diverging into at least three distinct ones, each optimized for a different deployment reality. GoClaw's PostgreSQL commitment makes it impossible to be zero-config. ClawTeam's git worktree model makes it impossible to be multi-tenant. Hermes' filesystem profile model makes it impossible to do real-time inter-agent coordination.

### 2. Nobody Does All Three Separations

The synthesis identified a gap that no tracked platform fills: **simultaneous user separation, task separation, and context separation**.

In the real world, developers need all three. I need my work API keys isolated from my personal ones (user separation). I need parallel agents working on different features without conflicts (task separation). I need my "code review" context to have different tools and permissions than my "research" context (context separation).

GoClaw separates users. ClawTeam separates tasks. Hermes separates contexts. The platform that does all three — without requiring PostgreSQL, git expertise, and filesystem management respectively — will have a genuine architectural advantage.

### 3. Coordination Is the Underserved Middle Ground

The experiment revealed a surprising asymmetry. GoClaw has enterprise governance but no swarm coordination. ClawTeam has swarm coordination but no enterprise governance. Hermes has neither but excels at individual productivity.

The underserved space is **structured coordination for small teams** — not 500-user enterprise deployments (GoClaw's territory), not solo developers with parallel agents (ClawTeam's territory), but teams of 3-10 humans who need their agents to collaborate across organizational boundaries with some governance.

Imagine: ClawTeam's dependency chains and inbox system, but with GoClaw's credential isolation and audit logging, running inside Hermes' profile model so each team member gets a consistent context. That product doesn't exist. The closest approximation requires duct-taping three platforms together.

### 4. Security Practices Should Decouple from Architecture

GoClaw's security is the most complete because it's baked into PostgreSQL — tenant-scoped encryption, tenant-scoped audit logs, RBAC enforcement at the RPC layer. But this means you need PostgreSQL to get security.

The synthesis showed that some security practices are architecture-independent:
- **Credential pool rotation** (Hermes) works with any storage backend
- **Secret redaction via fingerprints** (Hermes) works without encryption
- **Exec approval allowlists** (GoClaw) work without a database
- **Structured audit logging** (GoClaw) could use SQLite instead of PostgreSQL

The implication: security maturity should not require a specific architectural commitment. Platforms like ClawTeam that store credentials in plaintext TOML files could adopt Hermes' pool rotation and GoClaw's audit patterns without changing their core architecture. The fact that they haven't suggests that security is treated as an afterthought in personal-agent platforms — a habit that will become unsustainable as these agents handle more sensitive operations.

### 5. Profile-as-Workspace Is the Right Default for Personal Agents

Hermes' profile model — a self-contained directory with config, credentials, skills, memory, and session state — is the cleanest isolation primitive I've seen for personal use. ClawTeam's worktree model is brilliant for parallel code work but doesn't separate contexts. GoClaw's tenant model is overkill for a single user.

The profile approach has a property that the others lack: **zero-config context switching**. I can have a "research" profile with a cheaper model and read-only tools, and a "coding" profile with a powerful model and full terminal access. Switching between them is changing a directory, not provisioning infrastructure.

This suggests a convergence point: personal platforms should adopt profile-based isolation as the default, with optional worktree isolation for parallel coding tasks and optional tenant isolation for team deployments. Hermes provides the foundation; the others provide the optional layers.

---

## What Each Platform Should Steal

The synthesis produced a specific, actionable list:

**GoClaw should steal from ClawTeam:**
- Task dependency chains with auto-unblock (more expressive than implicit team coordination)
- Agent-level cost dashboards with circuit breaker states

**GoClaw should steal from Hermes:**
- Automatic credential pool rotation (replace manual key management)

**ClawTeam should steal from GoClaw:**
- AES-256-GCM credential encryption (the plaintext TOML problem is a showstopper for any shared system)
- Structured audit logging (JSON state files are not audit trails)

**ClawTeam should steal from Hermes:**
- Profile/context separation (let agents operate under different configurations for different tasks)

**Hermes should steal from ClawTeam:**
- Inter-agent communication (inboxes and broadcast, not just fire-and-forget delegation)
- Task dependency tracking (blocked-by chains, not flat todo lists)
- Multi-agent monitoring (kanban board view of all running tasks)

**Hermes should steal from GoClaw:**
- RBAC with permission scopes (read-only for research, full-access for development)
- Structured audit logging for enterprise profiles

---

## The Real Takeaway

I set out to learn about AI agent platforms by putting three of them to work on the same problem. I learned what I expected — the platforms have different strengths, different weaknesses, different architectural commitments. The comparison matrices confirmed the analysis I'd already done manually.

But I also learned something I didn't expect: **the way each agent *thought* about the problem revealed more about the platform than any feature comparison ever could.**

GoClaw's agent wrote about security the way a security engineer writes about security — layered defenses, threat models, compliance requirements. ClawTeam's agent wrote about coordination the way a systems architect writes about distributed systems — message passing, isolation boundaries, failure recovery. Hermes' agent wrote about identity the way a product designer writes about UX — user contexts, mental models, switching costs.

These aren't coincidences. Each platform shapes how its agents reason about problems. GoClaw's database-centric architecture naturally produces database-centric analysis. ClawTeam's git-centric architecture naturally produces git-centric analysis. Hermes' profile-centric architecture naturally produces profile-centric analysis.

The platforms don't just provide different tools — they provide different *lenses*. And the most useful thing about this experiment wasn't learning what each platform does. It was learning what each platform *sees*.

---

*All 13 analysis files are available in the [virtual-team directory](https://github.com/dz3ai/allclaws/tree/main/virtual-team) of the AllClaws repository. The cross-platform synthesis at `virtual-team/S1-T5-cross-platform-synthesis.md` contains the full comparison matrices and trade-off analysis.*
