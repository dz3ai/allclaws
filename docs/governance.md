# Platform Governance: Admission, Tracking Tiers, and Archival

**[中文](governance.zh-CN.md)** | English

> Q4-6 deliverable — the governance rules for a maturing platform catalog. Draft for review, August 18, 2026.
> Companion to ROADMAP Q4-7 (category coverage gap-closure) and the platform evaluation rubric.

---

## Why Governance, Now

AllClaws tracks 34 platforms across 4 categories, plus 7 harness ecosystems in `architecture/agent_harnesses.md`. The August 2026 coverage audit queued 8 candidates (Q4-7). Meanwhile 5 tracked platforms sit in the stale queue. Without explicit rules, every admission and archival is an ad-hoc judgment — fine at 20 platforms, unsustainable at 34+.

This document resolves the four Q4-6 research questions: the platform cap, admission criteria, stale-platform handling, and the minimum viable analysis.

---

## 1. The Cap Ruling: 35 Full Platforms

**Ruling: the 35-platform cap applies to Full-Platform tracking only** (Tier 1 below). It is a quality budget, not a growth limit on the research itself.

Rationale:

- The 14-file admission checklist (config.json + comparison docs + README/MISSION/ROADMAP/LATEST_UPDATES in both languages) costs a full working session per platform and creates permanent sync debt. Each addition also grows 5 comparison matrices. Beyond ~35, per-platform attention thins below the quality bar AllClaws publishes at.
- The cap does NOT constrain Tier 2 (harness ecosystems, lightweight sections in one architecture doc) or Tier 3 (watchlist, one table row). Research breadth continues through tiers, not through Tier-1 inflation.
- When Tier 1 is full, a new admission requires a reciprocal archival (see §5) — the catalog becomes replaceable, not frozen.

Current state: 34/35 Tier-1 slots filled. One slot remains.

## 2. Three Tracking Tiers

The binary "tracked / not tracked" is retired. Three tiers, three levels of obligation:

| Tier | What it is | Where it lives | Obligation | Cap |
|------|-----------|----------------|------------|-----|
| **Tier 1 — Full Platform** | Standalone agent platform with local checkout and benchmark integration | `config.json` + submodule + full architecture entry + 5 matrices + all overview docs (14 files, EN+ZH) | Monthly update cycle; benchmark coverage where feasible | **35** |
| **Tier 2 — Ecosystem Track** | Harness/toolchain ecosystems and category representatives that merit structured analysis but not full infrastructure | One section in the relevant `architecture/` doc (e.g., `agent_harnesses.md`) with Relevance-to-AllClaws note; counted in MISSION scope list | Reviewed at least quarterly; updated when materially changed | Soft (review at 15) |
| **Tier 3 — Watchlist (MONITOR)** | Candidates that fail a hard criterion today (too new, rc status, uncertain trajectory) but are architecturally significant | A table row in `docs/governance.md` §7 + one-line entry in LATEST_UPDATES when status changes | Re-evaluate every quarter; promote or drop within 2 cycles | None |

Promotion path: Tier 3 → Tier 2 → Tier 1, each requiring the criteria in §3. Demotion: Tier 1 → archived (§5) or Tier 1 → Tier 2 (for platforms that shrink in relevance but retain historical value).

**Category coverage rule:** Tier 1 admissions are prioritized by category gap, not by star count. A candidate representing an untracked category (per the Q4-7 matrix) outranks a higher-starred candidate in a covered category.

## 3. Admission Criteria (codified)

These formalize the rubric refined through the 2026-07-06 and 2026-07-28 evaluation batches. Five dimensions:

| Dimension | Weight | Criterion |
|-----------|--------|-----------|
| Architectural distinctiveness | **High** | Novel pattern not already covered by tracked platforms (per the category coverage matrix) |
| Active development | **High** | Commits within the last 30 days, sustained — not burst-then-silence (check 90-day trajectory) |
| Form factor fit | **High** | Standalone platform/CLI/framework with an independent agent runtime. NOT an IDE extension, plugin layer, agent-fleet manager, or thin LLM SDK wrapper |
| Community traction | Medium | Real stars/forks/contributors (not bot-farmed); no minimum bar — a 189-star platform with a novel pattern (Maxclaw) outranks a dormant 69K-star one (MetaGPT) |
| License | Medium | MIT/Apache-2.0 preferred; custom or NOASSERTION licenses require an explicit flag in the entry |

**Decision matrix:**

- **TRACK** (Tier 1 or 2 by form): meets all three high-weight criteria AND fills a category gap or represents a genuinely novel pattern.
- **TIER-2**: meets high-weight criteria but is a harness/toolchain/subsystem (not a full platform), OR meets criteria but Tier 1 is at cap.
- **MONITOR** (Tier 3): architecturally significant but fails one hard criterion today — created <1 month ago, pre-1.0 rc with declared breaking changes, or <90-day sustained activity evidence. Re-evaluate quarterly.
- **SKIP**: fails form factor, dormant, red flags.

**Red flags (auto-SKIP, unchanged from the July rubric):** obfuscated JS payloads; bot-farmed commits; no real code (<200KB marketing shell); self-described "methodology, not platform"; VS Code/IDE extension form factor; dormant-then-sudden-rewrite activity pattern.

**Standing reversals (documented precedents):** the low-code rejection was narrowed in July 2026 — visual platforms with a full agent runtime + tool calling (Dify) are NOT just flow designers. Personal assistants, extension layers, fleet managers, and domain-specific non-agent tools remain excluded.

## 4. Minimum Viable Platform Analysis

The 14-file checklist is the Tier-1 standard. The **minimum viable analysis** for any tier entry is:

1. **Classification line** — language, scale, category
2. **Philosophy** — the one-sentence reliability bet (from the harness comparison's philosophy map)
3. **Architecture facts** — entry point, pattern, key modules, MCP status, deployment, DB, security (the platform_comparison field set)
4. **Relevance to AllClaws** — why this is tracked; which research question it informs
5. **One verified data point** — at least one number (stars, LOC, benchmark metric, release cadence) checked against the source at writing time

An entry missing #4 or #5 is a placeholder, not an analysis. Tier-2 sections must meet the same minimum in their architecture-doc section.

## 5. Stale Platforms and Archival

**Stale definition:** no commits for 6+ months. The quarterly review (§6) moves stale platforms to a decision, not automatically to archival.

**Archival criteria — ALL must hold:**

1. Stale (6+ months no commits), AND
2. No strategic significance (not a reference implementation, not the sole representative of a tracked category, not cited as evidence in 2+ research reports), AND
3. No pending roadmap relevance (not an input to an open research item)

**Archival mechanics:** remove submodule + config.json + matrices + doc sections (the 12-file removal checklist); move the platform entry to the historical appendix of `platform_comparison.md` with one line on why it was archived; keep research reports untouched (they are historical artifacts). Archival frees a Tier-1 slot.

**Demotion alternative:** a stale platform with historical significance demotes to Tier 2 (section retained in architecture docs, infrastructure removed) instead of full archival.

**Current queue (August 2026):**

| Platform | Last activity | Review | Notes |
|----------|--------------|--------|-------|
| Claw-AI-Lab | No tags | Q3 2026 | Academic; retained for lab-pipeline pattern |
| ClawTeam | Apr 2026 | Q3 2026 | Orchchestration reference; virtual-team experiment evidence |
| GoClaw | Apr 2026 | Q3 2026 | Enterprise-governance reference (Q3-3 report) |
| MaxClaw | May 2026 | Q3 2026 | Low impact; weakest retention case |
| AutoGen | Apr 2026 | Q4 2026 | Maintenance mode; enterprise multi-agent reference |

## 6. Quarterly Review Process

**Trigger:** first Monday of each quarter-month (Jan/Apr/Jul/Oct), piggybacked on the monthly ecosystem report cycle.

**Procedure (one session, checklist-driven):**

1. **Stale sweep** — `git submodule status` + per-platform `git log -1` dates; flag everything ≥6 months stale
2. **Watchlist sweep** — re-evaluate every Tier-3 entry: promote (criteria now met), hold (one-line reason), or drop (2 cycles expired)
3. **Tier-2 sweep** — check each ecosystem section for staleness; update or annotate
4. **Slot accounting** — Tier-1 count vs cap; if full and candidates are pending, decide archival/demotion to free slots
5. **Output** — a dated section in `docs/PROJECT_STATUS.md` + updates to the tables in this document; commits reference this doc

**Time budget:** the sweep itself is mechanical (~30 min with the drift-check script); decisions are the only judgment calls.

## 7. Watchlist (Tier 3) — Initial State

The Q4-7 candidate pool, plus the two harness evaluations from August 2026, ruled under §3:

| Candidate | Category | Tier ruling | Reasoning | Re-evaluate |
|-----------|----------|-------------|-----------|-------------|
| **Pi** (earendil-works/pi) | Harness — extension pragmatism | **Tier 2 now** (TRACK) | 1yr sustained, 93K★, novel self-extension + telemetry contracts; harness form → Tier 2, not Tier 1 | — (done: `agent_harnesses.md` §Pi) |
| **browser-use** | Computer-use (browser) | **Tier 1 — ADMITTED Aug 18, 2026** | Category gap (Q4-7); ~109.7K★, MIT, daily commits, sustained 2024-10→now; fills the computer-use paradigm, the largest untracked category | — (done: platform #35, full checklist) |
| **deepseek-harness (dsh)** | Harness — composition formalism | **Tier 3 → Tier 2 on 1.0** | First-party frontier-vendor harness, 158.8K★, but v0.1.0-rc with declared breaking changes | 2026-Q4 or first stable release |
| **UI-TARS** (bytedance) | Computer-use (GUI) | **Tier 3 → hold (verified stale)** | Re-verified 2026-08-18: last source commit 2025-09-05, ~1 year dormant — fails the active-development hard criterion. Computer-use category covered by browser-use | Q4 review (if revived) |
| **ChatDev** (OpenBMB) | Multi-agent SOP (China) | **Tier 3 → Tier 2 candidate** | Overlaps MetaGPT (SOP role-play) + stale risk (XAgent sibling dead); Tier 2 suffices | Q4-6 review |
| **LangBot** (langbot-app) | Messaging bridge (WeChat) | **Tier 3 → Tier 1 candidate** | Category gap (WeChat first-class); verify enterprise relevance | Q4-6 review |
| **Letta** (ex-MemGPT) | Memory infrastructure | **Tier 3 → Tier 2 candidate** | Memory layer distinct from platforms (A1 context evidence); Tier 2 as category representative | Q4-6 review |
| **Mem0** | Memory infrastructure | **Tier 3** | Overlaps Letta; one memory representative likely enough | Q4-6 review |

**Tier-1 slot note:** with 34/35 filled, at most one of the Tier-1 candidates (browser-use / UI-TARS / LangBot) enters before an archival frees a second slot. Priority follows the category rule (§2): computer-use is the largest untracked paradigm; browser-use has the strongest activity profile — but the Q4-6 review verifies before admitting.

## 8. Intentionally Excluded Categories

Confirmed exclusions (do not re-evaluate without new evidence): observability/ops tooling (Langfuse), sandbox infrastructure (E2B), voice-first consumer assistants, robotics/embodied AI (robot-toolkit is a separate project), agent fleet managers/ADEs, IDE extensions, thin LLM SDK wrappers.

---

## Change Log

| Date | Change |
|------|--------|
| 2026-08-18 | Initial draft: 35-cap ruling (Tier-1 only), three-tier model, codified admission criteria, minimum viable analysis, archival criteria, quarterly process, 8-candidate watchlist |

*Part of: AllClaws Personal AI Agent Ecosystem Research. Companion docs: [ROADMAP.md](ROADMAP.md) (Q4-6, Q4-7), [MISSION.md](MISSION.md) (scope).*
