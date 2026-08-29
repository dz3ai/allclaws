---
layout: post
title: "AI Agent Ecosystem Report: August 2026"
date: 2026-08-30 23:50:00 +0800
author: Danny Zeng
categories: [Monthly Report]
tags: [ecosystem, monthly-report, ironclaw, kimi-code, codex, agentscope, governance, protocol-wars, long-running-benchmarks, divergence]
---

August 2026 was the month the ecosystem split into two speeds. On one side, a handful of platforms shipped at a pace that redefined "active" — IronClaw crossed its 1.0 threshold, kimi-code tagged sixteen releases in thirty days, and codex merged over a thousand commits. On the other side, a quiet tier of former high-flyers went dark: aider, reasonix, ClawTeam, Qwen-Agent all posted zero commits for the month. The middle hollowed out. And for the first time, AllClaws needed a governance model to describe what it was seeing — because "is this platform alive?" stopped being a question you could answer from a star count.

This report also marks a methodology upgrade. The raw numbers below are larger than any prior month — but a third of them are bot commits, release bots, and triage agents committing to their own repositories. We now separate human-paced development from machine-paced churn, and the divergence between the two is itself a finding.

---

## Trend 1: IronClaw 1.0 — and the Quietest-Right New Default Branch Problem

The headline event of August: **IronClaw shipped v1.0.0** (July 27 tag, with a month of hardening commits through August 29). The platform that spent eighteen months as "the most actively updated tracker" crossed into production territory — typed e2e provider journeys, notification automation, extension output ownership, and CI that validates integration group topology.

The subtler story is how we almost missed it. IronClaw's upstream switched its default branch to `staging` — where nothing has moved since May — while real development continued on `main`. Our submodule was pinned to the dead branch and read as "zero commits since July 30" until a cross-check against the GitHub API showed pushes landing daily. The same pattern surfaced in two more platforms: ZeroClaw's live branch is `master` (388 commits this month) not `main`, and Rocketride develops on `develop` (108 commits) while its `main` sat frozen. Three platforms, three silent default-branch switches.

This is worth a trend because it's becoming an ecosystem habit: teams use their default branch as a release surface and develop elsewhere, which quietly breaks every naive tracker that assumes default-branch == trunk. We've fixed our tracking (branch config now points at the live trunk for all three) and added it to the governance checklist: *verify the default branch is the development trunk at every quarterly review*.

## Trend 2: The Coding-Agent Vertical Went Vertical

If July's story was context compaction, August's is raw velocity in the coding-agent vertical:

- **codex** — 1,202 commits this month. The highlight isn't volume; it's **Guardian V2** (#41100, #41392, #41422): shared transcript collection, context primitives, and decision metrics for an oversight layer that reviews the agent's own actions. Codex is building a second agent to watch the first.
- **kimi-code** — 300 commits and tags 0.32.0 through 0.39.1. The big architectural move: **agent-core-v2**, a DI×Scope engine with four lifecycle tiers (App/Workspace/Session/Agent) that agent domains are migrating onto (#3175). Add self-healing wire journals (#3281), a remote-control web tunnel (#3034), and server-local path attachments — MoonshotAI is shipping an agent platform, not a CLI.
- **Dify** — 792 commits, v1.17.0. August was a consolidation month: deep dependency-injection refactors across controllers and service APIs, permission-gated skill entries, session-scoped workflow accessors. The codebase is being hardened for multi-tenant scale.
- **AgentScope** — v2.0.7 with a new **GoalPipeline** (#2428), DingTalk channel support (#2285), workspace pooling (#1755), and a channel-worker architecture that holds long connections in a dedicated worker (#2390).

The coding-agent category is now the fastest-moving vertical we track, and it's not close.

## Trend 3: The Silence Tier — Staleness Gets a Definition

August is also the month the floor dropped out for a tier of platforms. Zero upstream commits in the reporting window:

| Platform | Last commit | Silent for | Notes |
|----------|-------------|------------|-------|
| reasonix | 2026-05-29 | 3 months | CLI category pioneer; now the stalest tracked CLI agent |
| aider | 2026-05-22 | 3+ months | Former default recommendation for git-aware pair programming |
| ClawTeam | 2026-07-04 | ~2 months | Shipped v0.3.0, then went quiet |
| Qwen-Agent | 2026-03-04 | ~6 months | Crossed the 6-month bar this month |
| MetaGPT | 2026-01-21 | 7 months | Still cited as core evidence in 2 reports — held, not archived |
| MaxClaw / Claw-AI-Lab / Rocketride-main | Jun–Jul | 1.5–2 months | Pre-stale watch |

Qwen-Agent crossing the six-month line matters most: it's a China-ecosystem representative, and under the governance rules it fails no archival criterion except strategic significance — a contested call the September review will have to make. The 4-month stale definition revision (proposed August 19) would already capture reasonix and aider today; that proposal is now live with three real test cases instead of a hypothetical.

One of those three test cases belongs to us: this report corrects the record on Rocketride. Our previous "stale" reading came from tracking `main` while development moved to `develop` — 108 commits of live work we nearly archived.

## Trend 4: Agents That Watch Agents

Across the fast tier, the same architectural bet appeared three times, independently:

- **codex Guardian V2** — an oversight agent with its own transcript collection and decision metrics, gating the primary agent's actions.
- **OpenWorker layered security corpora** — 301 rows of gate/reviewer/sequence eval data wired through the harness, plus shell-escape corpus rows. They're not writing a safety module; they're writing the test suite for one.
- **IronClaw notification automation** — pre-run failure publishing (#7899) with persisted auth gates (#7901): the supervisory surface is being treated as a first-class subsystem.

July's compaction race was about making agents fit in their context windows. August's quiet consensus is that the next bottleneck is **trust** — and the emerging answer is a second model watching the first, with its own evidence trail. Our failure-mode taxonomy predicted this layer would arrive; seeing it land in three places in one month suggests it's a wave, not a coincidence.

## Trend 5: The Claw Ecosystem's Engine Room Keeps Turning

Under the headline numbers, the core claw platforms continued shipping at a healthy human pace:

- **OpenClaw** — 10,425 commits this month (351 authors; Peter Steinberger alone landed 6,197 — the ecosystem's single most productive human). Feature thread: browser/commanded document transitions, context-engine host parameter projection, control-UI cloud worker visibility.
- **Hermes-Agent** — 6,208 commits (Teknium 1,670). New provider plugins landed in a single day: Nebius Token Factory, Ramp Router, Router User-Agent identity, plus nested subtasks in todo and additive delete ops in relay.
- **NanoClaw** — 254 commits of distributed-systems discipline: session claims that fence spawn/adoption/finish, durable delivery-attempt rows surviving restarts, shadow-written coordination state alongside in-memory maps. The runner is becoming formally correct.
- **Nanobot** — 471 commits: OAuth model catalog discovery, Grok 4.6 subscription support, TUI clipboard-image paste, demand-driven document retrieval (#5525).
- **ZeroClaw** — 388 commits: ScopedToolRegistry sealing (#9319), authenticated operator cancellation for SOP jobs (#9476), authenticated webhook ingress before agent dispatch (#9744), ZeroRouter preset + public catalog (#9645).
- **OpenHuman** — 4,884 commits, but 4,547 are one author — a solo build-out of screen-capture removal and capture-surface refactoring.
- **HiClaw** — 38 commits on the live branch, still digesting its v1.2.0 K8s operator rewrite.
- **GoClaw** — 4 commits; the quietest month since tracking began. Watch status.

## Platform Activity Summary

| Platform | Commits (Aug) | Activity Level |
|----------|---------------|----------------|
| OpenClaw | 10,425 (351 authors) | 🔴 Very High |
| Eliza | 7,482 (119 authors) | 🔴 Very High |
| Hermes-Agent | 6,208 (859 authors) | 🔴 Very High |
| OpenHuman | 4,884 (14 authors) | 🟠 High* |
| PraisonAI | 1,376 (65% triage bot) | 🟠 High |
| IronClaw | 300+ (API-verified) | 🟠 High |
| codex | 1,202 | 🟠 High |
| Dify | 792 | 🟠 High |
| Nanobot | 471 | 🟡 Medium |
| ZeroClaw | 388 | 🟡 Medium |
| kimi-code | 300 | 🟡 Medium |
| NanoClaw | 254 | 🟡 Medium |
| OpenWorker | 203 | 🟡 Medium |
| Agent Zero | 142 | 🟡 Medium |
| Rocketride (develop) | 108 | 🟡 Medium |
| AgentScope | 79 | 🟡 Medium |
| browser-use | 45 | 🟡 Medium |
| HiClaw | 38 | 🟢 Low |
| copilot-cli | 9 (changelog-only) | 🟢 Low |
| GoClaw | 4 | 🟢 Low |
| kimi-cli | 2 | 🟢 Low |
| MaxClaw / Claw-AI-Lab / ClawTeam / aider / reasonix / MetaGPT / Qwen-Agent | 0 | ⚫ Silent |

*OpenHuman's number is one author's refactor campaign — treat as medium human pace.

## AllClaws Project Updates

**Platforms**: 35 tracked (Tier-1 cap reached August 18 with browser-use, the first computer-use representative). First monthly report under the new three-tier governance model.

**Research delivered in August** (4 reports):
- Protocol Wars 2026 (Q4-5) — MCP/ACP/A2A resolve to layering, not war
- Platform Governance model (Q4-6) — three-tier tracking, admission criteria, watchlist
- Category Coverage Gap-Closure (Q4-7) — 6 candidates evaluated, browser-use admitted
- Harness Engineering Comparison — the "evolutionary harness" pattern across tracked platforms

**Blog posts**: 6 (CLI command comparison across 16 platforms, virtual team experiment, harness engineering — each EN + ZH).

**Infrastructure**: Long-Running Agent Benchmarks (Q4-4, the last open roadmap item) shipped Phase 1 MVP — 1,038 lines of scenario specs, drivers (aider/codex/kimi-cli), runner, cost accounting, and scoring. Phase 2 (fatigue protocol, 8-platform grid) and Phase 3 (CI + report) follow. Also: README restructured to essentials-only, LATEST_UPDATES.md became the recency surface, and the CI gitlink incident (fixture directories committed as submodules) was root-caused and fixed — latest run fully green across all 13 jobs.

**CI health**: 20 agent-tests runs this month, 15 green / 4 failed (all during the gitlink breakage, fixed) / 1 cancelled. Benchmark suite 10/10 green.

## Looking Forward: September 2026

1. **The stale-definition vote** — with Qwen-Agent over the line and reasonix/aider as live test cases, the September review decides 6mo vs 4mo. Archival queue could open for the first time.
2. **Guardian-class oversight** — if the watch-the-agent pattern keeps landing at this rate, cross-platform oversight architecture becomes a research item (and possibly a new comparison dimension in platform_comparison).
3. **Q4-4 Phase 2** — fatigue protocol plus the 8-platform × 5-scenario grid. If it lands, ROADMAP hits 13/13 and H2 2026 closes with every item delivered.
4. **Watch: GoClaw and kimi-cli** — two historically reliable shippers posted near-zero months. One quiet month is noise; two is a signal.

---

*AllClaws tracks 35 AI agent platforms across 4 categories under a three-tier governance model. Data collected August 30, 2026, via local submodule logs and GitHub API cross-verification, with bot-commit separation. Full research reports at [github.com/dz3ai/allclaws](https://github.com/dz3ai/allclaws).*
