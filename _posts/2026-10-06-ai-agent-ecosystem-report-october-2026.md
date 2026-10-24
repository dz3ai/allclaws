---
layout: post
title: "AI Agent Ecosystem Report: October 2026 — From Correctness to Cadence"
date: 2026-10-06 22:30:00 +0800
author: Danny Zeng
categories: [Monthly Report]
tags: [ecosystem, monthly-report, release-train, guardian-v2, deslop, anti-mock, kimi-cli, reasonix-studio, billing-transparency, openclaw, hermes, codex]
---

September's report named the quarter's defining pattern: the **correctness campaign** — head platforms paying down the debt that long-running operation exposes. Two weeks into October, the campaign hasn't ended. It has been *institutionalized*. Hermes now cuts a near-daily canary tag and burned through 28 release candidates toward v0.21.5 in eight days — sixteen on September 29 alone — leaving an `abandoned-rc.*` tombstone for nearly every one, the stable still unshipped. Codex shipped ten stable releases in fourteen days (rust-v0.156.1 → v0.160.1) while running a parallel alpha train fifteen builds deep. OpenClaw maintains four version lines simultaneously — v2026.7.35, v2026.8.33–35, v2026.9.6–9.8, and v2026.10.1-beta.1 — while 440 of its 8,262 commits in this window carry a single verb in the subject line: *deslop*.

This report covers the window **Sep 20 – Oct 6** (29 submodules, remote-branch logs collected Oct 6, cross-checked against the 2026-09-22 weekly). The thesis: correctness was September's story; **cadence** — release channels, quality doctrine, review pipelines, billing visibility — is October's. The platforms that survived the correctness campaign are now converting it into process.

---

## The release train arrives

The most striking cross-ecosystem shift of the window is that *the release itself stopped being an event and became a channel*.

**Hermes-Agent** (9,001 commits) runs the most explicit train: eleven `v0.21.4+canary.<date>` tags in the window, most stamped within minutes of 07:00Z; rc.7 through rc.35 for v0.21.5 inside eight days; and — the detail that matters — 29 `abandoned-rc.*` tags preserved rather than deleted. Failed release candidates are kept as tombstones. That is release engineering with an audit trail, not versioning.

**Codex** (806 commits) ships a stable every 1–2 days while its `0.162.0-alpha.5 → alpha.15` train runs two minors ahead. **GoClaw** cut 16 tags in the window (v3.15.0-beta.213 → beta.228), a daily beta cadence with the stable clearly imminent. **Copilot-CLI** publishes `1.0.92-0` through `-5` suffixes — six builds of one version — with the public repo showing only changelog commits, the actual development evidently living elsewhere. **NanoClaw** did something rarer: migrated from semver (v2.4.0, Sep 23) to CalVer (v2026.10.0-rc.1/rc.2) *and* shipped update channels that follow release tags by default (#3986) — versioning and distribution redesigned in the same week.

**Reasonix** (623 commits) now runs four parallel lines: core `v1.38.12 → v1.39.7` (nine releases), `desktop-`/`npm-` mirrors, and the `studio-` line — daily-shipping since its v2.0.0 launch in August — going `v2.19.0 → v2.28.0`, fourteen releases in twelve days, until on Oct 4 the studio version doubled as the repo's bare `v2.28.0` tag. **OpenClaw**'s four concurrent lines include *backport maintenance* — v2026.8.34/35 and v2026.7.35 shipped in the same fortnight as the 9.x line, which is what an LTS policy looks like whether or not it's called one.

Read together: version numbers are becoming infrastructure. The question is no longer "when is the release" but "which channel are you on."

## Quality doctrine

September's correctness fixes were tactical. This window they acquired names — and the names are doctrine.

**OpenClaw**'s is *deslop*: 440 commits (`deslop commands #165696`, `deslop error handling and normalization #165601`, `deslop UI accidental complexity #165647`, `deslop non-channel tools #165707`) plus 674 `perf(...)` commits — sessions sharing list views, models reusing prepared catalog routing facts. The word choice is a statement: accumulated agent-era code is *slop*, and slop gets systematically removed, subsystem by subsystem.

**Dify**'s (407 commits) is *anti-mock*: 53 commits in the window rewrite tests from spec-based mocks to real boundaries — "use real data source auth gateways", "use real object storage SDK responses", "use real HTTP responses and plugin tool clients" — with an ast-grep guard (#43232) now *machine-enforcing* the ban on mock constructors. The test suite is being de-fictionalized, and the rule is checked by tooling, not reviewers.

**Eliza**'s (4,838 commits on `develop`) is *consolidation*: 142 commits flatten package layout, merge CLI helpers, and unify OS tooling, under the crash-only error doctrine formalized last month. **ZeroClaw** (210 commits, no release since v0.8.5) turned governance itself into a commit stream: six `docs(runtime)` commits propose *bounded exceptions* to its composition rules — and record "the Core Team approval" of each one in-repo (#11521). A constitution with a documented amendment process, in git.

One caution carried forward: **OpenHuman**'s 9,729 commits include 470 auto-generated `chore: files changed ...` entries; the bot-discount rule from August applies harder than ever. Real signal there is the v0.64.x line (five releases) and memory-v2 spec work under a self-imposed "layout limit" discipline.

## Guardian grows up

Codex logged **63 Guardian commits** in 16 days. The reviewer pipeline we dissected in [*Who Reviews the Reviewer?*](/allclaws/blog/2026/09/21/agent-reviews-agent-part1/) (published Sep 21, part 1 of this series) is now hardening in public: **Guardian V2** response timing scoped to snapshot sampling (#51065), reviews recoverable from parent checkpoints with per-attempt flag isolation (#51137/#51139/#51140), Decisions falling back to `OPENAI_API_KEY` (#51133), trusted-tool context preserved in review requests (#51070), and MCP elicitation reviewed with issuing-step context (#51067). Recovery, isolation, fallback, context provenance — these are the failure modes of a review system that runs in production, being closed one by one.

The counter-case is instructive: **Kimi-Code** shipped workspace trust-boundary hardening, *reverted it* (#4013, Sep 24), then re-landed it days later as an opt-in env var (#4059, Sep 28) plus a trust summary showing configuration sources (#4056). Security hardening that breaks workflows gets rolled back and re-approached with visibility first. Even 2.0-era Moonshot tooling is learning guardrail UX in public.

## The bill becomes visible

September flagged billing opacity as the loudest unmet demand in the ecosystem. The first concrete answers landed within two weeks — at Hermes, of all places: a desktop **progress chip that warns before a subscription hits its usage wall**, and model pickers where **a rate-limited provider says why and until when** (both Oct 5). ZeroClaw, meanwhile, fixed delegation-chain cost ceilings so a revisited alias's spend counts once (#11287) — multi-agent cost accounting getting the same identity semantics its sessions got last quarter. Not token-level accounting yet, but the direction flipped: usage state is now something platforms *show*, not something users dig out of logs.

## Consolidation, revival, absorption

**Kimi-CLI is dead; long live Kimi-Code.** The archival previewed in the Sep 22 weekly completed: 1.51.0 as the final feature bump, 1.52.0 (Sep 22) as the tombstone release, entry points short-circuited to the Kimi Code installer (#2666). This is the first Tier-1 tracked platform formally archived by its upstream — and AllClaws' governance rules (Q4-6) now face their first real removal decision at the quarterly review.

**Browser-Use woke up.** After a month of docs-only silence, 38 commits culminated in the **Anthropic browser toolset driver** (#5966, Oct 1) plus a full documentation campaign. The "product narrative adjustment" of September turns out to have been integration prep.

**OpenWorker** (146 commits, v0.3.0) spent the window on **OpenShell** — a sandboxed shell with a site allowlist, Docker Desktop host-networking setup flows, and a published CLI image. **RocketRide** shipped its whole client family at once (server-v3.4.0, TypeScript/Python v1.4.0, MCP v1.5.0, n8n-nodes v0.1.0) and started a prerelease train for the next.

And the frontier-model absorption rate keeps compressing: GoClaw shipped **adaptive thinking for Claude Opus 4.7+ and Claude 5** (Sep 29), with redacted-thinking replay and dated-snapshot handling in the same cluster; Nanobot added **GPT-6 temperature restrictions**; AgentScope announced **MiniMax support** alongside its service-layer SOPs and TeamPipeline (v2.0.9). New model releases are now platform work items measured in days, not quarters.

## Platform activity summary

| Platform | Key changes | Activity |
|----------|-------------|----------|
| OpenClaw | 4 version lines; deslop campaign (440); v2026.9.6–9.8, v2026.10.1-beta.1 | 🔴 |
| Hermes-Agent | Near-daily canaries; 28 RCs + 29 abandoned-rc tombstones; usage-wall UX | 🔴 |
| OpenHuman | v0.64.0–0.64.10; memory-v2 spec; layout-limit discipline | 🔴 |
| Eliza | Consolidation/flattening (142); crash-only doctrine; cloud billing evidence | 🔴 |
| Codex | 10 stable releases; Guardian V2 hardening (63 commits); rust-v0.160.1 | 🔴 |
| Reasonix | Studio v2.19→2.28 (14 in 12 days); core v1.39.7; 9 core releases | 🟠 |
| PraisonAI | Session/transcript persistence fixes; v4.7.10–4.7.12 | 🟠 |
| Dify | Anti-mock test campaign (53); strict typing; no release since 1.17.1 | 🟠 |
| Nanobot | Subagent task messaging + cancellation; WebUI touch blitz; GPT-6 limits | 🟠 |
| ZeroClaw | RPC fencing; typed stop taxonomy; bounded-exception governance | 🟠 |
| OpenWorker | v0.3.0; OpenShell sandbox + allowlist UX; CLI image | 🟡 |
| NanoClaw | CalVer switch + update channels; v2026.10.0-rc.2; Baileys spoofing pin | 🟡 |
| AgentScope | v2.0.9; service-layer SOPs; TeamPipeline; MiniMax | 🟡 |
| RocketRide | Full client family release; n8n nodes; C++ Microsoft nodes | 🟡 |
| GoClaw | 16 tags (beta.213→228); Claude 5 / Opus 4.7 adaptive thinking | 🟡 |
| Browser-Use | Revival: Anthropic browser toolset driver; docs campaign | 🟡 |
| Kimi-Code | 2.1.0/2.1.1; workspace-trust revert→re-land; tower interrupts | 🟡 |
| HiClaw | v1.2.4; matrix-channel and teamharness fix stream | 🟡 |
| Agent-Zero | v2.13 (Sep 23) then main quiet; activity moved to `ready` branch | 🟢 |
| IronClaw | v1.4.1 shipped on `release/2026-08-26`; tracked main frozen since Sep 10 | 🟢 |
| Copilot-CLI | 1.0.89–1.0.92 changelog-only; six builds of 1.0.92 | 🟢 |
| Kimi-CLI | **Archived by upstream** (Sep 21); final 1.52.0 | ⚫ |
| ClawTeam / MaxClaw / Claw-AI-Lab / Aider / MetaGPT / Qwen-Agent | Dormant (13 weeks – 8+ months) | ⚫ |

## AllClaws project updates

The publication pipeline delivered two new series entries: **Who Reviews the Reviewer?** (Sep 21, part 1 of Agent-Reviews-Agent, four platforms' review architectures compared) and **MCP Is a Protocol — So Why Are You Babysitting Processes?** (Sep 24, EN + ZH, from the weekly WeChat draft — Hermes Connectors and the MCP-as-dependency shift). The Sep 22 weekly report documented the kimi-cli archival and named model routing the strongest cross-project paradigm signal.

**Q4-4 (long-running benchmarks) entered Phase 2** on Oct 6 with the S4 `triage-burndown` fixture — the fatigue instrument: a 376-LOC stdlib-only metrics library seeded with 5 independent same-difficulty bugs, each with an issue doc and a documented-red test; a hidden acceptance suite that fails on the pristine repo and passes with the reference patch; and `check_windows.py`, the per-window scoring contract for the fatigue engine (verified 58/58 on scratch). Phase 1 (S1–S3 scenarios, aider/codex/kimi-cli drivers, runner + cost + scoring) shipped Aug 24. Remaining Phase 2 work: reasonix/opencode/smolagents drivers, S5 `legacy-migrate`, then the first real long-run grid.

Tracking hygiene: the IronClaw branch-drift case deepened (v1.4.1 released on `release/2026-08-26` while tracked `main` sits frozen since Sep 10) — the quarterly review should decide whether to re-pin. Agent-Zero shows the same pattern in embryonic form (main quiet since Sep 23, `ready` branch active).

## Looking forward — rest of October

**(1)** The Q4-8 paradigm durability re-check, due this month: model routing has kept spreading (Agent-Zero's scoped subagent presets, GoClaw's per-model thinking policies), which strengthens its case; the other four paradigms get their verdicts. **(2)** First Q4-4 long-run results once Phase 2 drivers land — does the deslop/anti-mock doctrine actually hold up over 45-minute sessions, measured per window? **(3)** Governance quarter-review: the kimi-cli removal (first upstream archival of a Tier-1 member) plus the MetaGPT/Qwen-Agent decisions held over from September. **(4)** Release-watch: Hermes v0.21.5 stable, NanoClaw v2026.10.0, GoClaw 3.15.0, OpenClaw v2026.10.1 — four trains arriving at once.

---

*Data: remote-branch logs collected 2026-10-06 across 29 submodules (window Sep 20 – Oct 6), weekly submodule report 2026-09-22, GitHub tags/releases cross-check. Commit counts include CI/merge noise where noted. Project: [dz3ai/allclaws](https://github.com/dz3ai/allclaws).*
