---
layout: post
title: "The Model×Harness Interaction Nobody Saw Coming"
date: 2026-11-18 10:00:00 +0800
author: Danny Zeng
categories: [Test Platform, Benchmarking]
tags: [test-platform, benchmark, agent-benchmark, glm-5.3, local-models, hermes, aider, longrun]
---

The allclaws test platform was built to answer a simple question: which CLI agent framework is best at solving real code tasks? After closing our first task cohort (five tasks, 40 single-tier runs, 13/13 local PASS, $0 spent) we knew the answer would be incomplete without a second data point. So we ran the same four frameworks — **hermes, aider, kimi_code, reasonix** — against a frontier model in the cloud (**glm-5.3**) and compared against our local 35B baseline (**qwen36-35b-mtp**).

80 runs total. 2 tiers. 4 drivers. 5 tasks. **What we found inverted our rankings.**

## The matrix, compressed

Local = qwen36-35b (localhost:8080). Cloud = glm-5.3 (Zhipu coding-plan). Each cell shows two letters: repeat 1 and repeat 2. P = pass, F = fail.

| driver | gh-issue | refactor-multi | triage-burndown | feature-crud | legacy-migrate | L | C |
|---|---|---|---|---|---|---|---|
| **hermes** | PP | FF → **PP** ✨ | PP | PP | PP | 8/10 | **10/10** |
| **reasonix** | PP | FF → **PF** | PP | PP | PP | 8/10 | 9/10 |
| **kimi_code** | PP | FF | PP | PP | PP | 8/10 | 8/10 |
| **aider** | PP | FF | PP | PP | **PP → FF** ⚠️ | 8/10 | 6/10 |

**Headline numbers:** local tier was 40/40 (all drivers cleared every task on the 35B). Cloud tier was 33/40. Three drivers got better or stayed equal on the stronger model. **Aider got worse.**

The two stars and the warning mark are the interesting parts. Let's go.

## Finding 1 — refactor-multi is a model×harness interaction

The `refactor-multi` task is the platform's stress test: extract an engine module from a monolithic calculator, deduplicate a percentage formula into a single helper, and add typed models. The acceptance suite has 28 behavioral tests. And one structural constraint:

> **`test_percentage_formula_appears_at_most_once`** — the percentage math helper may appear at most once across the entire package. Route all percentage calculations through it.

On the local 35B, this test killed **all four drivers, 0/8** — every single run duplicated the formula across multiple files. The obvious explanation was "the 35B can't do this."

The cloud data disproved that. On glm-5.3, **hermes cleared it 2/2** and reasonix cleared it 1/2 (rep1 pass, rep2 fail on the structural check but the behavioral tests still passed — 27/28). kimi_code and aider still failed it on both repeats.

Same model. Same task. Different harnesses. Different outcomes.

**What this means:** For kimi_code and aider, the bottleneck isn't model capability — it's how the harness communicates quality-shape constraints to the model. Even a frontier model can't satisfy a constraint the harness doesn't successfully transmit. For hermes, the harness design matters more than the raw model for this particular task shape.

The wall-time data tells a supporting story: hermes's refactor runs were 1830s and 417s (13 turns then 11 turns), while kimi_code did it in 137s and 126s. Hermes spent more time iterating — and iteration is where the constraint got enforced. kimi_code's faster wall time came at the cost of missing the structural check entirely.

## Finding 2 — aider inverts on legacy-migrate

The `legacy-migrate` task is the hardest in the cohort: migrate an application from a legacy ORM (oldorm 0.x) to its successor (neworm 2.x), following a migration guide. The acceptance suite runs a static scanner for deprecated API usage (`session.query`, `Model.validate`, `model.dict`, `session.save`, `class Meta`, old hook callbacks) plus behavioral tests.

**Aider+35B: passed 2/2.** Legacy-migrate was one of the tasks the 35B handled cleanly.

**Aider+glm-5.3: failed 2/2.** Same harness, stronger model — half-migrated tree. The scanner detected oldorm imports still in `inventory/__init__.py` (line 13), and cascading behavior failures followed: stock issue/guard tests, validation tests, listing tests, and the full order lifecycle all red. Exit code 0 — the tool reported success on a broken tree.

Both cloud rep1 and rep2 produced nearly identical artifacts: 6 files touched, 77 lines added, 62 removed — essentially the same partial migration attempted twice. The scratch directories from both runs have no `oldorm` imports detectable via grep, but the acceptance scanner (which uses AST-based pattern matching on the actual imported module) still found violations. This means aider did edit most files but left a residual import or import-adjacent construct in `__init__.py`.

**Working hypothesis (unverified from transcripts):** glm-5.3's reasoning output interferes with aider's SEARCH/REPLACE parsing — its thinking content may introduce formatting patterns that cause aider to skip or misparse the final edit block needed to clean up the `__init__.py` import. The `.aider.chat.history.md` transcripts from both rep1 and rep2 are archived for post-publication verification.

**The inversion is the point:** we expected a stronger model to be strictly better or equal. Aider getting worse on the stronger model is the kind of interaction you only see with two tiers. It suggests the edit-format pipeline has a failure mode that a particular reasoning pattern can trigger — something invisible in a single-model benchmark.

## Finding 3 — fatigue is zero everywhere

Across both tiers (80 runs), the `triage-burndown` task — five sequential bug fixes in a single agent session — was solved completely every time. 80/80 triage windows solved, all four drivers, both models, both repeats. No sequential degradation on either model or any harness.

This is worth noting because fatigue is often the invisible killer of agent benchmarks. An agent might solve issue 1 fine, then progressively forget earlier context by issue 5. Our data shows no such effect at either model scale for this cohort.

## The full story — local tier recap

On the local 35B, all four drivers passed all five tasks (40/40). The only discriminator was the `refactor-multi` structural constraint, which none could satisfy (0/8 across all drivers). The wall times were tight:

| driver | gh-issue | refactor | triage | feature | legacy | median |
|---|---|---|---|---|---|---|
| kimi_code | 62s | 289s | 136s | 162s | 172s | 162s |
| reasonix | 52s | 467s | 153s | 198s | 211s | 198s |
| hermes | 262s | 686s | 97s | 163s | 172s | 172s |
| aider | 208s | 1390s | 315s | 334s | 290s | 302s |

All four cleared the behavioral acceptance suites on every task. The platform's first cohort closed on this data — 13/13 valid agent runs passed, every reference patch re-validated byte-identical, four harness bugs found and fixed along the way.

## Token accounting (with caveats)

Only aider reports token usage (via its built-in usage summary). Medians on cloud tier: **aider 6.2K in / 10.3K out**. kimi_code and hermes report `null` (no token counter). reasonix reports 386K in / 8.3K out — but this is an estimate inflated by its character-to-token conversion heuristic. **Do not rank on tokens yet.**

## Rankings (this cohort, with asterisks)

1. **hermes** — 18/20. Only harness to clear refactor on cloud. No inversions. Token-agnostic (no counter).
2. **reasonix** — 17/20. Strong overall, but the 1/2 structural miss on refactor rep2 shows it's not reliably eliciting the constraint.
3. **kimi_code** — 16/20. Fastest median walls (104s cloud), but refactor blind spot is a real gap.
4. **aider** — 14/20. Reasoning-model edit-format fragility on legacy-migrate. Its unknown-model warning (fixed in [commit 6f8cd07](https://github.com/dz3ai/allclaws/commit/6f8cd07)) also disables its window guard — a latent risk for future runs.

*The asterisks: reasonix's token medians remain unnormalized, kimi_code's speed could be a trade-off (fewer iteration turns = fewer constraint enforcement opportunities), and aider's inversion needs transcript verification before we commit to the mechanism.*

## What this design existed for

This two-tier setup — local 35B vs cloud frontier, same tasks, same harnesses — is expensive in compute but cheap in dollar terms ($0 both tiers, the coding plan covers it). The value is in the interactions it surfaces:

- **refactor-multi** wouldn't have been flagged as model×harness without the cloud tier. A single-model benchmark would conclude "the 35B can't do this" — a false conclusion.
- **aider's inversion** on legacy-migrate is the kind of regression that a single-tier benchmark can never catch. It only appears when the same harness meets a different model.
- **hermes's refactor clearance** on the cloud tier is equally invisible without two tiers. On the 35B, all harnesses looked equivalent (8/10 each). The cloud tier differentiated them.

The design is simple: run the same grid on two models, one local and one cloud, and look for cells that move. Those movers are the interesting ones.

## Run directories

- Local tier: `test_framework/benchmark_results/longrun/2026-11-16T22-59-59`
- Cloud tier: `test_framework/benchmark_results/longrun/2026-11-17T21-50-22`

All raw results, acceptance logs, and transcripts are in the repo.
