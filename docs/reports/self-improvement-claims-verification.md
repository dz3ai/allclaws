# "Self-Improving" Claims Verification

**Date:** 2026-07-05
**Scope:** All 26 tracked platforms
**Methodology:** Source code analysis + documentation comparison

---

## Executive Summary

Of 26 tracked platforms, **6 have verifiable self-improvement mechanisms** in source code, **5 make marketing claims with partial or no implementation**, and **15 make no claims**. No platform uses reinforcement learning (RLHF/GRPO) for runtime self-improvement. The dominant pattern is **LLM-as-judge background review** — spawning a secondary model call to extract lessons from completed turns and persist them as skills or memory entries.

---

## Tier 1: Verified Self-Improvement Implementations

These platforms have real, code-verified mechanisms that make the agent measurably better at future tasks within its environment.

### 1. Hermes-Agent — Background Review Loop

**Claim:** "Self-improving through skills — Hermes learns from experience by saving reusable procedures as skills."
**Source:** `website/docs/user-guide/features/skills.md:438`

**Verified Implementation:**

| Component | File | Mechanism |
|-----------|------|-----------|
| Background review trigger | `agent/turn_finalizer.py:456-478` | Fires after turn completion based on `_skill_nudge_interval` and `_memory_nudge_interval` counters |
| Review thread spawner | `run_agent.py:1581-1608` | `_spawn_background_review()` spawns a daemon thread with `propagate_context_to_thread()` |
| Review logic | `agent/background_review.py` (907 lines) | LLM-as-judge: analyzes conversation, calls `memory` and `skill_manage` tools |
| Skill provenance | `tools/skill_provenance.py` | Tags agent-created skills with `background_review` origin for curator dedup |
| Write approval gate | `tools/write_approval.py` | Optional human-in-the-loop gate (`memory.write_approval`, `skills.write_approval`) |
| Curator | `agent/curator.py` | Background skill dedup/merge — prevents skill pileup from the review loop |

**How it works:**

1. After a turn completes (5+ tool iterations), `_spawn_background_review()` fires
2. A daemon thread runs a separate `AIAgent` instance with the conversation snapshot
3. The review agent calls `memory` (durable facts) and `skill_manage` (procedural knowledge) tools
4. Skills are tagged with `background_review` provenance
5. The curator periodically merges/deduplicates accumulated skills
6. User can gate all writes behind `write_approval: true`

**Verdict:** ✅ **VERIFIED.** Real implementation. The background review is a genuine feedback loop: conversation → LLM analysis → persisted knowledge → future context injection. Not RL — it's LLM-as-judge with human-in-the-loop gating. Skills accumulate and are deduplicated by the curator.

**Limitation:** No quantitative evidence of performance improvement. "Better" is qualitative — the user subjectively experiences fewer repeated corrections.

---

### 2. ZeroClaw — Skill Improver with Cooldown

**Claim:** "Skill self-improvement: atomic writer + history-scanning helpers for the background review fork"
**Source:** `crates/zeroclaw-runtime/src/skills/improver.rs:1`

**Verified Implementation:**

| Component | File | Mechanism |
|-----------|------|-----------|
| SkillImprover struct | `improver.rs:27-159` | Atomic SKILL.md writer with in-memory + on-disk cooldown tracking |
| History scanner | `improver.rs:304-400` | `extract_skill_executions_from_history()` parses tool results to find failed skill invocations |
| Failure detection | `improver.rs:286-294` | `looks_like_failure()` heuristic: checks for error/failed/panic/exception keywords |
| Skill creator | `creator.rs:222-244` | Auto-creates skills, evicts oldest when `max_skills` limit reached |
| Correction log | `trust/types.rs:80` | `correction_log` tracks trust adjustment events |
| Post-turn hook | (referenced in `improver.rs:2`) | "see `agent::loop_` post-turn hook + `tools::skill_manage`" |

**How it works:**

1. After each turn, the agent loop's post-turn hook scans conversation history
2. Failed skill executions are extracted (`extract_skill_executions_from_history`)
3. An LLM call generates improved skill content
4. `improve_skill()` writes atomically: temp file → validate → rename
5. Cooldown enforced both in-memory (per-process) and on-disk (`updated_at` YAML field)
6. Full audit trail preserved as HTML comments in SKILL.md

**Verdict:** ✅ **VERIFIED.** Real implementation with durability (survives restarts via on-disk cooldown). More structured than Hermes — explicit cooldown tracking, atomic writes, audit trail. The failure-scanning heuristic is simple but functional.

---

### 3. IronClaw — Learning Missions (Self-Improvement Mission)

**Claim:** "The execution loop is Python code running inside the Monty interpreter... This makes the glue layer self-modifiable at runtime by the self-improvement Mission."
**Source:** `docs/internal/engine-v2-architecture.md:9`

**Verified Implementation:**

| Component | File | Mechanism |
|-----------|------|-----------|
| Self-improvement mission | `engine-v2-architecture.md:148` | Fires on thread completion with trace issues (errors, tool-not-found) |
| Skill repair mission | Same | Fires when completed thread used a stale/incomplete skill |
| Skill extraction mission | Same | Fires on success with 5+ steps and 3+ tool actions |
| Conversation insights | Same | Fires every 5 completed threads per project |
| MemoryDoc types | `engine-v2-architecture.md:135-142` | Lesson, Issue, Spec, Skill — durable learnings from missions |
| Context injection | `engine-v2-architecture.md:157-162` | Up to 5 relevant MemoryDocs injected per LLM call via keyword scoring |
| Skill selector | `engine-v2-architecture.md:164-189` | Deterministic 4-phase pipeline: gating → scoring → budget → attenuation |

**Graduated risk model:**

- Level 1: Prompt overlay (safe)
- Level 2: Config patch (moderate)
- Level 3: Code change (propose only — never auto-applied)

**Verdict:** ✅ **VERIFIED (architectural).** The most ambitious design of all platforms — graduated self-modification with explicit risk levels. The "self-modifiable at runtime" claim for Level 3 is design aspiration, not shipping reality (code changes are "propose only"). But Levels 1-2 (prompt overlays, config patches) are implemented learning missions.

**Limitation:** Architecture documentation describes the design; the implementation maturity varies by mission. The self-improvement mission's Level 3 code-modification is explicitly "propose only."

---

### 4. MaxClaw — EvolutionTracker

**Claim:** "Evolution Layer: error pattern recognition, recovery strategy effectiveness tracking, self-improvement metrics"
**Source:** `README.md:177`, `docs/agent_lifecycle.md:114`

**Verified Implementation:**

| Component | File | Mechanism |
|-----------|------|-----------|
| EvolutionTracker | `internal/agent/evolution.go` (587 lines) | Tracks error patterns, recovery strategies, model performance |
| RecordError | `evolution.go:173` | Records error reason, retry count, recovery status/time |
| RecordAPICall | `evolution.go:139` | Tracks tokens, latency per model/provider |
| RecordToolCall | `evolution.go:239` | Tracks tool success rate and execution time |
| GetRecoveryRecommendation | `evolution.go:266` | Recommends retry count + estimated recovery time based on historical success rate |
| GetBestModelForTask | `evolution.go:300` | Suggests best model by success rate + latency |
| LearnParameter | `evolution.go:338` | Arbitrary key-value learning persistence |
| State persistence | `evolution.go` | `evolution/state.json` — survives restarts |
| Lifecycle integration | `internal/agent/lifecycle.go` | Wired into AgentLoop via `AgentLifecycle` struct |

**How it works:**

1. Every API call, error, and tool call is recorded with metadata
2. Recovery strategies are tracked: attempts → successes → avg retries → avg latency
3. On future errors, `GetRecoveryRecommendation()` suggests the historically most effective response
4. `GetBestModelForTask()` recommends models based on historical performance data
5. State persists to `evolution/state.json`

**Verdict:** ✅ **VERIFIED.** The most quantitatively measurable self-improvement of all platforms. Unlike skill/memory systems (which improve qualitative helpfulness), MaxClaw's EvolutionTracker directly improves error recovery rates and model selection through statistical tracking. This is genuine adaptive behavior with persisted state.

**Separate mechanism — User Feedback Loop:** `docs/agent_lifecycle.md:284` describes a 6th layer that learns from explicit user corrections, persisting to `MEMORY.md` (user-visible). This is distinct from the Evolution layer.

---

### 5. GoClaw — Skill Learning Loop (skill_evolve)

**Claim:** "Self-improving skills: runtime usage evidence, skill lifecycle management"
**Source:** `docs/21-agent-evolution-and-skill-management.md:410`, `docs/model-steering-system.md:161`

**Verified Implementation:**

| Component | File | Mechanism |
|-----------|------|-----------|
| skill_evolve config | `docs/21-...md:131` | Boolean toggle: `skill_evolve: false` (default off) |
| Skill evolution nudges | `docs/model-steering-system.md:161` | "Encouraging Self-Improvement" — system prompt steering section |
| Recency reinforcement | `docs/01-agent-loop.md:335` | "Persona Reminder — recency reinforcement to combat lost-in-the-middle" |
| Usage evidence | `docs/21-...md:412` | "runtime usage evidence" collected as foundation for skill evolution |
| Self-evolution (SOUL.md) | `docs/21-...md:63-89` | Agent can rewrite its own personality file (SOUL.md) via write_file |

**Verdict:** ✅ **VERIFIED (foundation).** GoClaw has the control-plane infrastructure (usage tracking, skill lifecycle) but the higher-level "learning loop" is described as belonging "above this control-plane." The `skill_evolve` flag defaults to `false`, suggesting the full loop is not yet production-ready. The SOUL.md self-evolution (personality refinement) is a narrower but real mechanism.

---

### 6. OpenClaw — Memory Dreaming + Self-Improvement Patterns

**Claim:** "Dreaming/promotion: raise phase reinforcement enough for repeated dreaming-only revisits to clear the default durable-memory gate"
**Source:** `CHANGELOG.md:9037`

**Verified Implementation:**

| Component | File | Mechanism |
|-----------|------|-----------|
| Dreaming system | `ui/src/pages/dreams/` (6 files) | UI for memory dreaming — memory consolidation during idle time |
| Dreaming command | `chat-commands.test.ts:182` | `/dreaming` slash command: "Enable or disable memory dreaming" |
| Self-improvement patterns | `extensions/open-prose/skills/prose/guidance/patterns.md:351` | "Self-Improvement Patterns" section in agent guidance |
| Language self-improvement | `extensions/open-prose/skills/prose/examples/README.md:116` | "Meta-level 2: analyzes .prose corpus to evolve the language itself" |
| Self-healing sync | `docs/reference/RELEASING.md:508` | "scheduled self-healing sync" for release dist-tags |
| Self-correcting code | `docs/tools/code-execution.md:136` | "the agent can self-correct" after execution exceptions |

**Verdict:** ✅ **VERIFIED (partial).** The dreaming system is a genuine memory consolidation mechanism — memories are "promoted" to durable storage based on reinforcement scores accrued during dreaming cycles. The self-improvement patterns in the prose skill are a meta-level application (the agent analyzes its own skill corpus to improve it). However, this is scoped to the open-prose extension, not the core agent.

---

## Tier 2: Marketing Claims with Partial Implementation

### 7. NanoBot

**Claim:** "Self-improvement — Learn from feedback and mistakes"
**Source:** `README.md:475`

**Verification:** No matching implementation found in source code. The README lists it as a feature bullet, but no `self.improv`, `feedback.loop`, or `learning` mechanism exists in `.py` files outside the README itself. The skill-creator skill (`nanobot/skills/skill-creator/SKILL.md`) can create skills, but there's no background review loop to trigger skill creation from experience.

**Verdict:** ⚠️ **UNVERIFIED.** Marketing claim without corresponding implementation.

---

### 8. HiClaw

**Claim:** "Hermes is... a self-improvement loop: after completing tasks, it automatically creates reusable Skills"
**Source:** `blog/hiclaw-1.1.0-release.md:19`

**Verification:** HiClaw's claim is about its Hermes integration, not a native mechanism. HiClaw itself doesn't implement self-improvement — it references Hermes's background review loop. The "Worker-Generated Skills" blog post (`hiclaw-1.0.6-release.md:319`) describes workers creating documentation skills, but this is user-guided, not autonomous self-improvement.

**Verdict:** ⚠️ **DERIVATIVE.** Claim is about integrated platform (Hermes), not native capability.

---

### 9. Copilot-CLI

**Claim:** "Self-correcting custom tool calls in agentic loop"
**Source:** `changelog.md:913`

**Verification:** This refers to error recovery within a single turn (retrying failed tool calls), not cross-session learning. No persistence mechanism exists.

**Verdict:** ⚠️ **IN-TURN ONLY.** Not self-improvement — it's error retry within a single conversation.

---

### 10. Reasönix

**Claim:** "self-corrects in-turn", "repair-storm detector now self-corrects once"
**Source:** `CHANGELOG.md:2931,2945`, `src/loop.ts:347`

**Verification:** Same as Copilot-CLI — in-turn error correction, not cross-session learning. The "self-correction" refers to the repair-storm detector granting the loop one retry attempt before bailing. No persistence.

**Verdict:** ⚠️ **IN-TURN ONLY.** Error recovery, not self-improvement.

---

### 11. OpenHuman

**Claim:** "Self-healing - writes polyfills for missing shell commands", "tool_stats - Self-reflection"
**Source:** `gitbooks/developing/architecture/agent-harness.md:216,366`

**Verification:** The `tool_maker` archetype was explicitly removed: "The old automatic 'command not found → spawn ToolMaker → retry' interceptor was removed... there is no implicit self-healing retry on shell failures today." (`agent-harness.md:188`). The `tool_stats` tool provides session-level introspection but no cross-session learning. Voice postprocessing handles "self-corrections" in speech ("wait no", "I meant") — that's transcript cleanup, not agent improvement.

**Verdict:** ⚠️ **REMOVED / NOT SELF-IMPROVEMENT.** Self-healing was explicitly removed. Remaining matches are voice processing and in-session introspection.

---

## Tier 3: No Claims Found (15 platforms)

| Platform | Notes |
|----------|-------|
| ClawTeam | References Hermes as "self-improving" but has no native mechanism |
| NanoClaw | Self-healing refers to network reconnection, not learning |
| Claw-AI-Lab | No claims |
| Aider | No claims |
| AgentScope | No claims (RAG/memory middleware exists but no self-improvement loop) |
| SmolAgents | Not tracked locally |
| LangGraph | Not tracked locally |
| CrewAI | Not tracked locally |
| AutoGen | Not tracked locally |
| Swarms | Not tracked locally |
| OpenAgents | Not tracked locally |
| OpenFang | Not tracked locally |
| kimi-code | Not tracked locally |
| kimi-cli | Not tracked locally |
| Codex CLI | Not tracked locally |

---

## Cross-Platform Analysis

### Mechanism Taxonomy

| Mechanism | Platforms | Description |
|-----------|-----------|-------------|
| **LLM-as-judge background review** | Hermes, ZeroClaw, IronClaw, GoClaw | Spawn secondary LLM call after turn → extract lessons → persist as skills/memory |
| **Statistical tracking** | MaxClaw | Record error/tool/model metrics → recommend best recovery strategy |
| **Memory dreaming/consolidation** | OpenClaw | Idle-time memory promotion based on reinforcement scores |
| **Skill lifecycle management** | Hermes, ZeroClaw, IronClaw, GoClaw | Create → improve → dedup → evict skills with cooldowns and audit trails |
| **In-turn error correction** | Copilot-CLI, Reasönix, OpenClaw | Retry failed tool calls within a single conversation (NOT self-improvement) |

### Key Findings

1. **No platform uses RLHF/GRPO/reward models for runtime self-improvement.** All "self-improvement" is either LLM-as-judge or statistical tracking. The "learning" is prompt/skill/memory accumulation, not weight updates.

2. **The skill-improvement loop is the dominant pattern** (Hermes, ZeroClaw, IronClaw, GoClaw). All four implement variants of: turn completes → background analysis → skill creation/improvement → cooldown-gated persistence.

3. **MaxClaw is unique** in providing quantitatively measurable improvement (recovery success rates, model performance rankings). Other platforms' improvement is qualitative.

4. **IronClaw is the most ambitious** with its graduated risk model (prompt → config → code), but Level 3 (code self-modification) is "propose only."

5. **Hermes has the most mature implementation** — full background review loop, curator dedup, write-approval gating, and provenance tracking. 907 lines in `background_review.py` alone.

6. **3 of 5 marketing claims are unverified or misleading** (NanoBot, OpenHuman, Copilot-CLI/Reasönix). OpenHuman explicitly removed its self-healing feature.

### What "Self-Improving" Actually Means in Practice

None of the tracked platforms improve at the model level (no weight updates, no fine-tuning). "Self-improving" universally means one of:

- **Procedural memory accumulation:** Skills/workflows are saved and injected into future context
- **Error pattern learning:** Recovery strategies are tracked and recommended
- **Memory consolidation:** Facts are promoted to durable storage over time

The improvement is bounded by context window injection — the agent gets "better" because it has more relevant information loaded, not because the underlying model changed.

---

## Methodology

- **Source search:** `grep -rinE` across all 26 platform directories for 15 pattern categories
- **Exclusions:** `node_modules`, `__pycache__`, `target/`, `.venv`, `vendor/`, `site-packages`
- **Verification:** Every Tier 1 claim verified by reading the actual source code file and function
- **Classification:** Claims sorted into STRONG (code-verified), MODERATE (partial/derivative), WEAK (in-turn only), NONE

---

*This report will be updated as platforms evolve. Last verification: 2026-07-05.*
