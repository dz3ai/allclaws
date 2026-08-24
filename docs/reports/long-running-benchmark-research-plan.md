# Long-Running Agent Benchmarks: Research & Execution Plan

**Status:** In progress (Q4 2026 ROADMAP item Q4-4 — the last open item)
**Plan written:** August 20, 2026
**Prerequisites:** ✅ v3.0 benchmark engine (runtime/static/sandbox), ✅ CLI agent submodules built (aider venv, codex/reasonix/kimi-cli), ✅ podman sandbox, ✅ config.json platform paths + language dispatch pattern

---

## Research Questions (from ROADMAP Q4-4)

1. How do agents perform on tasks lasting 30+ minutes (GitHub issue resolution, multi-file refactoring)?
2. What is the token cost vs outcome quality curve?
3. How does technical debt accumulate across agent sessions?
4. Can we detect "agent fatigue" — quality degradation over long sessions?

## Scope Ruling (pragmatic, made in this plan)

**35-platform full comparison is out of scope.** Library frameworks (LangGraph, CrewAI, AutoGen, Swarms, Dify, MetaGPT...) each require a bespoke harness script — cost far exceeds research value. The benchmark targets **agents that already run as executable CLIs or single-file entry points**:

| In-scope platforms (8) | Type | Driver effort |
|---|---|---|
| aider | Python CLI (venv ready) | Low |
| codex | Node CLI (submodule built) | Low |
| kimi-cli | Python CLI (venv ready) | Low |
| reasonix | Node CLI (npm build needed) | Medium |
| opencode (reference, untracked) | Go CLI (installed) | Low |
| smolagents | Library → single-file harness | Medium |
| hermes-agent | Library → single-file harness | Medium |
| zeroclaw | Rust binary (needs MCP config) | High — optional stretch |

CLI coding agents are the core cohort (5); library frameworks get thin single-file harnesses only if time permits. opencode participates as an untracked reference point.

## Task Scenario Design

### Task spec format (`test_framework/tasks/<task-id>/spec.json`)

```json
{
  "id": "gh-issue-001",
  "type": "github-issue",
  "fixture_repo": "fixtures/tiny-web-app",
  "task_prompt": "Fix issue #1: ... (full issue text)",
  "timeout_minutes": 45,
  "max_turns": 200,
  "acceptance": {
    "method": "pytest",
    "command": "python -m pytest tests/test_issue001.py -q",
    "pass_criteria": "exit 0"
  },
  "cost_cap_usd": 2.0
}
```

### Scenario portfolio (5, machine-checkable)

| # | ID | Type | Duration target | Acceptance method |
|---|---|---|---|---|
| 1 | `gh-issue-001` | Bug fix from issue text (failing test exists) | 10-20 min | pytest green |
| 2 | `refactor-multi` | Multi-file refactor (extract module, keep API) | 20-40 min | existing test suite green + diff shape check |
| 3 | `feature-crud` | Implement CRUD endpoint + tests | 30-45 min | new pytest suite written by us, must pass |
| 4 | `triage-burndown` | 5 small issues in sequence (session length probe) | 45+ min | per-issue checks, scored incrementally |
| 5 | `legacy-migrate` | Dependency upgrade w/ breaking changes (e.g. pydantic v1→v2 subset) | 30-60 min | pytest green + no deprecated imports |

Scenario rules:
- **Fixtures are deterministic** — pinned deps (requirements.lock), no network at test time, small (<5K LOC) Python/TS repos we author ourselves
- **Every fixture repo ships with hidden acceptance tests** (not visible to the agent in the repo tree — mounted at eval time into a separate path)
- Difficulty ladder: S1 easy → S5 hard. Agents get identical prompts (prompt text lives in the spec, not hand-typed per agent)

### Metrics collected per run

- Outcome: pass/fail/partial (per-issue for S4), wall time, turns
- Tokens: input/output/cached per run (from agent's own usage report where available; else estimated from transcript char count / 4)
- Cost: USD at list price, per model
- Quality-of-diff: LOC changed, files touched, tests added/removed (via `git diff --stat` in the worktree)
- Technical debt proxy: lint warnings delta (ruff/eslint before vs after)

## Driver Architecture

One Python package, mirroring the v3.0 engine layout:

```
test_framework/longrun/
├── __init__.py
├── cli.py            # argparse: run / report / list
├── spec.py           # task spec load + validate
├── drivers/
│   ├── base.py       # DriverBase: prepare worktree → launch → await → collect
│   ├── aider.py      # `aider --yes-always --message <prompt>` in venv
│   ├── codex.py      # `codex exec --json <prompt>`, parse events
│   ├── kimi_cli.py   # TUI-less mode / -p flag
│   ├── reasonix.py   # npm run build first, then CLI invoke
│   ├── opencode.py   # `opencode run <prompt>` (reference)
│   ├── smolagents.py # single-file harness calling CodeAgent
│   └── hermes.py     # single-file harness calling run_agent main
├── runner.py         # orchestration: worktree, timeout, retry, cost cap
├── scoring.py        # acceptance execution + per-window scoring (fatigue)
└── cost.py           # token → USD table, per-model pricing
```

Key runner behaviors:
- `git worktree add` per run → pristine fixture never touched; worktree removed after
- Hard timeout (subprocess kill) + max_turns + cost_cap_usd enforcement where the CLI exposes limits
- All runs logged to `benchmark_results/longrun/<timestamp>/<platform>/<task-id>/` (gitignored, colon-free timestamps per repo convention)
- Driver interface is 3 methods: `prepare(worktree)`, `run(prompt) -> proc`, `collect() -> RunResult` — adding a platform = one new file

## Fatigue Detection Protocol (Q4-4 research question 4)

- Scenario 4 (`triage-burndown`) is the instrument: 5 sequential issues, one continuous session per agent
- Score each issue window: solved(yes/no), tokens, turns, wall time
- Fatigue signals: window-over-window solve-rate drop, token inflation (same-difficulty issues costing more), turn count growth
- Secondary: split S2 into 3 checkpoints (plan/execute/verify) and score transcript quality at each — measures coherence drift, not just outcomes
- Statistics: 3 repeats per agent; report median + spread; flag fatigue only if monotone decline across repeats

## Cost Model & Budget

Pricing assumptions (list, subject to re-check at execution):

| Model class | ~tokens per S2-S5 run | $/run | Notes |
|---|---|---|---|
| GLM-4.x / DeepSeek tier | 0.5-2M in + 50-200K out | ¥0.3-2 (~$0.05-0.3) | primary statistical cohort |
| Claude/GPT frontier tier | same | $1-5 | spot-check contrast only |

Full grid: 5 tasks × 3 repeats × 8 platforms ≈ 120 runs.
- Domestic-model core: ≈ ¥100-300 total
- Frontier spot-check (2 platforms × 2 tasks × 1 repeat): ≈ $20-60
- **Total budget ceiling: ~$150 / ¥1000. Hard stop if reached.**

Guardrails: per-run `cost_cap_usd`, weekly spend tally in report job, nightly-rate-limit window (01:00-07:00 local), sequential runs per platform (no parallel burn).

## Execution Phases

| Phase | Content | Effort | Exit criteria |
|---|---|---|---|
| 1. MVP | spec format + 3 scenarios (S1/S2/S3) + drivers (aider, codex, kimi-cli) + runner + cost report | 3-5 sessions | one command runs the full S1-S3 × 3 agents grid; smoke report generated |
| 2. Expansion | drivers (reasonix, opencode, smolagents) + S4/S5 + fatigue protocol | ~1 week | 8 platforms × 5 scenarios coverage ≥70%; fatigue data for 2+ platforms |
| 3. CI + report | weekly long-run workflow (manual dispatch) + `long-running-benchmarks-2026.md` | 2-3 sessions | workflow merged; report published; ROADMAP flipped to ✅ |

**Parallelization matrix:**

- Phase 1 scenarios S1/S2/S3: 3 parallel subagents (each owns one fixture + acceptance test)
- Phase 1 drivers aider/codex/kimi-cli: 3 parallel subagents (same DriverBase spec, different CLIs)
- Phase 2 fatigue protocol vs scenario S5: parallelizable
- Phase 3: sequential (needs stable Phase 1+2 outputs)

**Delegation pattern** (per skill guidance): subagents do mechanical work (fixture repos, driver shells, result parsers); research writing (fatigue analysis, final report) stays in the main session.

## Risk Register

| Risk | Likelihood | Mitigation |
|---|---|---|
| Agent destroys fixture repo | High | git worktree per run; pristine fixture is read-only |
| Runaway token spend | High | per-run cost cap + max_turns + timeout; weekly spend report; hard budget stop |
| CLI hangs on interactive prompt | High | stdin=/dev/null, non-interactive flags, hard timeout kill |
| Flaky acceptance tests | Medium | deterministic fixtures (pinned deps, no network), max 2 attempts |
| Sandbox escape / file damage | Medium | podman container per run, workspace volume only |
| GLM/DeepSeek rate limits | Medium | exponential backoff, nightly window, sequential per-platform |
| Model version drift mid-study | Medium | pin model version per batch; record model+version in every result |
| opencode reference bias | Low | labeled untracked, excluded from rankings |
| Subagent timeout on fixture authoring | Medium | one fixture per subagent; main session reviews + commits |

## Success Criteria

1. ≥5 scenarios with machine-checkable acceptance, all runnable via one command
2. ≥5 platforms (4 tracked CLI agents + ≥1 library harness) completing runs on ≥3 scenarios
3. Token cost vs quality curve plotted for ≥3 platforms
4. Fatigue signal (or its absence) documented with per-window scores for ≥2 platforms
5. Weekly long-run CI workflow merged (manual dispatch trigger)
6. Report `docs/reports/long-running-benchmarks-2026.md` published; ROADMAP Q4-4 → Completed ✅ (both languages)

---

*Execution begins with Phase 1. Scenario and driver subagent briefs derive from this plan; do not re-scope without updating this file.*
