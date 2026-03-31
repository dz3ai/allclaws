# Baseline Test Scenario: Agent Updates Tracking

**Purpose:** Test agent behavior WITHOUT skill to identify baseline failures

## Test Setup

**Context:** allclaws project tracks 8 AI agent platforms as git submodules. Research needs monthly updates on changes across these projects.

**Scenario 1: Academic Knowledge Test**
> "We track OpenClaw, NanoClaw, IronClaw, GoClaw, ZeroClaw, Nanobot, ClawTeam, and MaxClaw projects. The user wants to know what changed in the last month. How do you get that information?"

**Expected Baseline Failures:**
- Manual git log in each submodule (tedious, error-prone)
- Misses releases, tags, documentation updates
- No structured output for research docs
- Doesn't track what was already reported
- No significance detection (critical vs trivial changes)

**Scenario 2: Time Pressure + Complexity**
> "User needs monthly research update in 5 minutes. 8 projects to check. Research document needs updating. What do you do?"

**Expected Baseline Failures:**
- Rush through checks, miss important changes
- Update docs without verification
- Skip checking all projects
- Provide incomplete summary

**Scenario 3: Ongoing Research Workflow**
> "This is a recurring monthly task. Last month we checked on March 1. Now it's April 1. How do you avoid reporting the same changes twice?"

**Expected Baseline Failures:**
- No state tracking (doesn't remember last check)
- Reports duplicate commits
- Wastes time on already-reported changes
- No incremental update capability

**Scenario 4: Significance Filtering**
> "User wants to know about CRITICAL changes only - security issues, breaking changes, architecture shifts. How do you identify these from 500+ commits?"

**Expected Baseline Failures:**
- Can't filter significance from raw commit list
- Misses CVE mentions in commit messages
- Doesn't prioritize by impact
- Provides overwhelming raw data

## Running the Baseline Test

Dispatch subagent WITHOUT skill present:

```
Task: Research agent project changes and update docs
Context: 8 submodules, last checked March 1, now April 1
Time: 5 minutes
Deliverable: Updated LATEST_UPDATES.md with significant findings
```

## What to Document

After running baseline, document:
1. **Process used** - How did they approach the task?
2. **Rationalizations** - What shortcuts did they take?
3. **Missed items** - What important things did they skip?
4. **Quality issues** - What was incomplete or wrong?
5. **Time pressures** - How did time pressure affect quality?

This documentation feeds into skill creation to address specific failures.
