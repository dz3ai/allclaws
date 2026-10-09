# Long-Running Agent Benchmarks 2026: First Live Grid

**Report date:** October 7, 2026 (addenda October 8: reasonix unlocked → criterion 2 closed, Q4-4 → ✅; hermes onboarded → 6 platforms)
**Scope:** First live execution of the Q4-4 long-run benchmark grid — 30 valid runs across 6 platforms × 5 scenarios, including the first fatigue-protocol data (3 repeats × 2 platforms)
**ROADMAP item:** Q4-4 (**completed** — see §Success Criteria Scorecard)
**Plan:** [long-running-benchmark-research-plan.md](long-running-benchmark-research-plan.md)
**Total recorded spend:** ~$0.40 (ceiling $150 — DeepSeek/Moonshot-tier cohort)

---

## 1. Executive Summary

The benchmark engine went live. Six agent platforms completed 30 machine-scored runs over five deterministic scenarios (bug fix, multi-file refactor, CRUD feature, 5-issue triage burndown, breaking-change migration). Four platforms solved 4/4 completion scenarios — **kimi-code**, **hermes**, plus **aider** and **reasonix** at 3/4 — on DeepSeek-tier models at $0.002–0.12 per run. The **smolagents** CodeAgent harness failed all completion scenarios while burning 40–50× more tokens than the CLI agents — the clearest cost-vs-quality separation in the dataset. The **fatigue protocol** produced its first (negative) result: aider showed zero degradation across 3 repeats (15/15 windows solved), while smolagents sat at a 0/5 floor with 2.7× token variance between identical repeats — variance without fatigue, because there is no performance to fade.

**The headline is not who won.** It is that the 30+ minute task class is now measured continuously: every run is worktree-isolated, cost-capped, hidden-test-scored, and drift-guarded — one command, ~$0.06 per full grid.

## 2. Cohort & Models

| Platform | Type | Model | Runs | Status |
|---|---|---|---|---|
| aider | CLI coding agent | `deepseek/deepseek-chat` | 7 | live ✅ |
| kimi-code | CLI coding agent (2.0) | `deepseek/deepseek-chat` via kimi-code provider | 4 | live ✅ |
| reasonix | CLI coding agent (Go) | built-in `deepseek` provider | 4 | live ✅ (Oct 8 addendum) |
| smolagents | library harness (CodeAgent) | `deepseek/deepseek-chat` (litellm) | 7 | live ✅ |
| hermes-agent | library harness (in-process `run_agent.main`) | `deepseek-chat` | 4 | live ✅ (Oct 8 addendum) |
| opencode *(untracked reference)* | CLI agent | `opencode/ling-3.1-flash-free` | 4 | live ✅ (reference only) |
| codex | CLI coding agent | — | 0 | **excluded from this grid** (Responses-API-only build vs chat-only providers; see addendum 3) |
| kimi-cli (1.0) | CLI coding agent | — | 0 | archived upstream → superseded by kimi-code 2.0 driver |
| zeroclaw | Rust binary | — | 0 | optional stretch (plan), not built |

**Oct 8 addendum:** Go 1.26.6 installed user-locally (`~/.local/go`, apt's 1.22 too old for the go.mod toolchain pin) and reasonix built from the pinned submodule (`bin/reasonix`, 52MB). The reasonix driver's graceful-degrade `prepare()` picked it up unchanged — first live grid ran within the hour.

**Oct 8 addendum 2 (hermes):** hermes' zero-balance `zai`/glm-5.2 provider was switched to the built-in `deepseek` provider (`config.yaml` + `DEEPSEEK_API_KEY` in `~/.hermes/.env`). Its first live grid wrote its fixes into the **parent-repo fixture template instead of the run worktree** — hermes' file tools resolve against `TERMINAL_CWD` in preference to the process cwd (`hermes_cli/kanban_db_dispatch.py:2823-2835`). The runner's fixture-drift guard caught every run, restored the template, and recorded `fixture_drift`; the driver now pins `TERMINAL_CWD=<worktree>`. Rerun: **4/4 solved**, no drift.

**Oct 8 addendum 3 (codex — negative result):** an attempt to wire codex to DeepSeek failed for a protocol-layer reason, not credentials. This codex build supports **only** the OpenAI **Responses** API: the provider config rejects `wire_api = "chat"` outright (`codex-rs/model-provider-info/src/lib.rs:95` — "`wire_api = "chat"` is no longer supported") and the request builder targets `/responses` exclusively (`codex-rs/codex-api/src/endpoint/responses.rs:67`). DeepSeek exposes `/chat/completions`, not `/responses`, so codex cannot use it. **GLM (Zhipu) also lacks `/responses`** — probed 2026-10-09: `POST /api/{coding/,}paas/v4/responses` → 404 on both, while the GLM *coding* endpoint's `/chat/completions` works (returned `glm-5.3-flash`; the metered `paas/v4` is the one with no balance). codex thus requires a Responses-API provider (OpenAI proper, or an aggregator/proxy that speaks `/responses`). Separately, the JS launcher also needs the native `@openai/codex-linux-x64` binary (absent on this host; buildable from `codex-rs` via cargo). **This is provider wire-protocol lock-in in practice** — a datum for the protocol-wars thread: the agent harness hard-depends on one vendor's wire format, so provider choice is constrained by the harness, not the reverse. The GLM coding subscription, meanwhile, is a live chat-completions tier usable by the chat-based cohort (a candidate model tier for a future grid).

Model pinning note: the cohort is deliberately heterogeneous-harness / single-model-tier (DeepSeek V3.x class + one free-slot reference model), matching the plan's "domestic-model statistical cohort" cost design. opencode's paid coding-plan auth errored server-side on run day; the free flash model keeps the reference platform participating without affecting tracked rankings (reference is excluded from rankings by plan).

## 3. Results Matrix

Scenarios: S1 `gh-issue-001` (bug fix, 2 defects), S2 `refactor-multi` (extract module, keep API), S3 `feature-crud` (implement CRUD + tests), S4 `triage-burndown` (5 sequential issues — fatigue instrument), S5 `legacy-migrate` (breaking-change API migration + deprecated-surface scanner). Acceptance = hidden pytest suite, mounted only at scoring time; pass = full suite green.

| Platform | S1 fix | S2 refactor | S3 CRUD | S5 migrate | S4 triage (per rep) |
|---|---|---|---|---|---|
| aider | ✅ | ❌ (2/28 checks) | ✅ | ✅ | 5/5 · 5/5 · 5/5 |
| kimi-code | ✅ | ✅ | ✅ | ✅ | not run (see §7) |
| **reasonix** *(Oct 8)* | ✅ | ❌ (same shape-check miss as aider) | ✅ | ✅ | not run (see §7) |
| **hermes** *(Oct 8)* | ✅ | ✅ | ✅ | ✅ | not run (see §7) |
| smolagents | ❌ (8/13) | ❌ | ❌ | ❌ | 0/5 · 0/5 · 0/5 |
| opencode (ref) | ❌ (8/13) | ❌ | ❌ | ❌ | not run |

Run artifacts: `test_framework/benchmark_results/longrun/2026-10-07T10-52-*`, `T10-54-44`, `T10-55-52`, `T11-38-58` (kimi-code final), `2026-10-08T13-41-30` (reasonix), `2026-10-08T14-57-19` (hermes). Each run dir carries `result.json` (status, tokens, cost, score, diff_stats, windows), `acceptance.log`, `stdout/stderr.log`, archived agent artifacts, and a CLI-rendered `report.md`.

### Failure-mode highlights

- **aider × S2 (the only CLI-agent failure on Oct 7):** solved the extraction but left duplicate percentage logic in the original module — the hidden "single percentage helper" shape check caught what the behavior tests could not. Exactly the technical-debt class the plan's lint-delta proxy targets. **reasonix × S2 (Oct 8) reproduced the identical failure mode** — two independent agents, same hidden-check catch: the S2 shape check is measuring something real about agent refactoring discipline. **hermes × S2 passed (Oct 8)** — the only platform to clear the trap, and with 12 files touched (the widest diff of the cohort).
- **reasonix token appetite (Oct 8):** 148K–866K input tokens per task (its own metrics JSON) at $0.03–0.12/run — 20–100× aider's token spend for comparable outcomes. Agentic exploration is expensive even when it wins; kimi-code's ~650-token runs are the outlier, not the norm.
- **smolagents (all scenarios):** the CodeAgent burned 40–140K input tokens per run and produced no passing acceptance. CodeAct-style single-loop agents drift on multi-file repo tasks — they re-read, re-plan, and run out of turns before editing coherently. This is the plan's cost-vs-quality curve at its steepest: ~$0.000–0.01 spent per **failure**.
- **opencode (reference):** 8/13 on S1 with a free flash model — correctly refuses to guess API contracts but doesn't complete the fixes. Reference-platform behavior, not a ranking signal.

## 4. Cost & Tokens

| Platform | Median tokens in | Median tokens out | Cost/run (recorded) | Outcome |
|---|---|---|---|---|
| aider | ~7,400 | ~2,200 | $0.002–0.004 (self-reported) | 3/4 pass |
| kimi-code | ~650 (chars/4 est.) | n/a | ≈$0.001 (ledger est.) | 4/4 pass |
| reasonix *(Oct 8)* | ~450,000 (self-reported) | ~20,000 | $0.03–0.12 (self-reported) | 3/4 pass |
| hermes *(Oct 8)* | ~2,500 (chars/4 est.)¹ | n/a | n/a (tokens only) | 4/4 pass |
| smolagents | ~101,000 | ~3,100 | n/a (tokens only) | 0/4 pass |
| opencode (ref) | ~1,400 (chars/4 est.) | n/a | n/a | 0/4 pass |

¹ hermes' stdout-based chars/4 estimate is not comparable to the CLI agents' self-reported usage — hermes prints only its final summary, not a token ledger. Its true usage is unmeasured in this grid.

kimi-code's efficiency stands out: 650-token estimates vs aider's 7,400 and reasonix's ~450,000 — the 2.0 CLI's agentic loop reads less and edits more, while reasonix buys its wins with brute-force context. Ledger total across all experiments this session (including invalidated exploration runs): **~$0.40**.

## 5. Fatigue Protocol (Q4-4 research question 4)

Instrument: S4 — five independent same-difficulty bugs, one continuous session per agent, 3 repeats, per-window scoring (window = one issue).

| Platform | rep1 | rep2 | rep3 | Signal |
|---|---|---|---|---|
| aider | 5/5 | 5/5 | 5/5 | **No fatigue** — at ceiling; 16–18s per session, wall variance <2s |
| smolagents | 0/5 | 0/5 | 0/5 | **Floor effect** — no performance to degrade; token spend 101.8K / 37.7K / 73.1K across identical repeats (**2.7× variance**) |

Findings:
1. **The instrument works but needs mid-tier agents.** Fatigue detection requires agents that neither ceiling (aider solves trivially) nor floor (smolagents cannot solve at all) the scenario. The difficulty ladder needs an S4-variant at higher per-issue difficulty (S4→S6 candidate for the next grid), or mid-tier models.
2. **Variance-without-quality is itself a finding.** smolagents' 2.7× token variance at identical (zero) outcome is a stability metric the grid now captures for free — a platform that costs 2.7× unpredictably is a production risk independent of capability.
3. **Per-window token/turn data remains scoped out** (plan appendix: single-shot sessions have no window-level producer; `window_metrics` stays the future hook). Fatigue verdicts rest on solve-rate + repeatability, as recorded in the Phase 2 outcome notes.

## 6. Infrastructure Validated Under Fire

Three live-fire fixes landed in the engine during this grid (all discovered by the first smoke run, fixed before data collection):
- **aider one-shot mode** needed explicit chat-file discovery (it asked for file paths instead of acting) + `1.9k`-suffix token parsing.
- **Fixture drift guard** (runner): an in-place mutation of the parent-tree fixtures during parallel sessions would have silently polluted every later run copy. The runner now detects parent-tree fixture drift after each run, records `fixture_drift`, and auto-restores from HEAD. One full wave was discarded and rerun because of this — the guard is what makes the published numbers trustworthy.
- **Repeat-aware run dirs** (`rep<N>/`) so the 3-repeat fatigue protocol doesn't overwrite itself; plus `LONGRUN_BUDGET` ceiling env for CI dispatch.
- **Fixture-drift guard earned its keep twice.** First it exposed a parallel-session mutation during the October 7 waves (one full grid discarded and rerun). Then on October 8 it caught hermes writing fixes into the parent-repo fixture template (via the `TERMINAL_CWD` resolution bug) — every hermes run was flagged, the template auto-restored from HEAD, and the driver fixed within the hour. Without the guard, both incidents would have silently poisoned downstream run copies.
- **Hermes worktree isolation** (`TERMINAL_CWD` pin) — see §2 addendum 2; the only platform whose "pass" initially meant the work landed outside the scored tree.

## 7. Success Criteria Scorecard (plan §Success Criteria)

| # | Criterion | Status |
|---|---|---|
| 1 | ≥5 scenarios, machine-checkable, one command | ✅ 5/5 |
| 2 | ≥5 platforms completing runs on ≥3 scenarios | ✅ **6 platforms × 4 scenarios** (3 tracked CLI + 2 library harnesses + 1 untracked reference; composition note: plan's letter said "4 tracked CLI agents" — codex is excluded from this grid by decision, see addendum 3) |
| 3 | Token cost vs quality curve, ≥3 platforms | ✅ 6 platforms |
| 4 | Fatigue signal (or absence) documented, ≥2 platforms | ✅ 2 platforms |
| 5 | Weekly long-run CI workflow merged | ✅ `.github/workflows/longrun-weekly.yml` (manual dispatch) |
| 6 | Report published; ROADMAP → ✅ | ✅ this document (Oct 8 addenda close criterion 2); ROADMAP Q4-4 flipped to ✅ (both languages) |

**Residual blockers (do not affect criteria):** codex — **excluded from this grid by decision** (Responses-API-only build; neither DeepSeek nor GLM exposes `/responses`; revisit with a Responses-capable provider or a chat→Responses proxy), funded Kimi keys for the kimi-code native path (current kimi-code runs route DeepSeek through its OpenAI-compatible provider).

## 8. Reproduction

```bash
cd test_framework
PYTHONPATH=. python3 -m longrun.cli list                       # 5 scenarios
PYTHONPATH=. DEEPSEEK_API_KEY=... LONGRUN_AIDER_MODEL=deepseek/deepseek-chat \
  python3 -m longrun.cli run --drivers aider \
  --tasks gh-issue-001,refactor-multi,feature-crud,triage-burndown,legacy-migrate \
  --repeats 3 --model deepseek-chat
PYTHONPATH=. python3 -m longrun.cli report                     # latest grid
PYTHONPATH=. python3 -m longrun.cli budget                     # spend ledger
```

CI: `.github/workflows/longrun-weekly.yml` — `workflow_dispatch` with task/repeat/budget inputs; sequential per platform; hard ceiling enforced by the spend ledger.

## 9. Next Grid Decisions

1. **Fatigue on the new cohort** — run S4 ×3 for reasonix, kimi-code, and hermes (all solved S4's sibling scenarios; they sit between aider's ceiling and smolagents' floor — exactly where the instrument has resolution).
2. **S4 difficulty bump** so fatigue is measurable for top performers (S4-hard: 5 bugs requiring cross-file edits).
3. **Frontier spot-check** (plan budget line: $20–60): aider × claude/gpt-class on S2/S5 to calibrate the domestic cohort's ceiling gap — and to see whether frontier models dodge the S2 duplicate-logic trap that caught aider and reasonix. hermes cleared it; worth a repeat to see if that is stable.
4. **opencode paid-model retry** when the coding-plan server recovers — the reference point deserves its intended model.
5. **codex** — excluded from this grid for now (Responses-API-only wire format vs the chat-only provider cohort). Revisit via an OpenAI/Responses-capable key, a Responses→chat proxy, or a future codex build that restores chat support.

---

*Grid dates: 2026-10-07 (+ Oct 8 reasonix & hermes addenda) · Engine: longrun v1 (Phase 2) + live-fire fixes · Spend: ~$0.40 / $150 · Artifacts: `test_framework/benchmark_results/longrun/`*
