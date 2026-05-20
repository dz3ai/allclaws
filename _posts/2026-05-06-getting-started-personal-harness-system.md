---
layout: post
title: "Getting Started with My Personal Harness System"
date: 2026-05-06 09:00:00 +0800
author: Danny Zeng
categories: [tutorial]
tags: [agent-harness, personal-ai, automation, claw-code, 1PC, getting-started]
---

## The Problem: Your Agent Works, But You're Still the Bottleneck

You have an AI agent. It writes code, runs commands, opens PRs. But you're still:

- Watching the terminal to see if it finished
- Retrying when a tool call times out
- Copy-pasting status updates into Discord
- Starting every session with the same "here's the repo, here's the branch, here's what we're doing" preamble
- Waking up to a blocked agent that failed on step 2 and sat idle for six hours

Your agent is an engine. What you're missing is the transmission, dashboard, and pit crew -- the **harness**.

---

## What a Harness Is (and Isn't)

A harness sits **below** your agent platform in the stack:

```
+------------------------------------------+
|  Agent Platform (claude, codex, openclaw)|  <-- Intelligence, tools, reasoning
+------------------------------------------+
                    |
                    v
+------------------------------------------+
|  Harness (what you're building)          |  <-- Execution, recovery, notification
+------------------------------------------+
                    |
                    v
+------------------------------------------+
|  Foundation (LLM APIs, Git, Docker)      |
+------------------------------------------+
```

A harness does not replace your agent. It wraps it. The agent stays focused on the work. The harness handles everything around the work.

The UltraWorkers toolchain calls this the **clawable** checklist. A clawable harness is:

- **Deterministic to start** -- boots the same way every time, no "remind me what we're doing"
- **Machine-readable in state** -- structured JSON, not prose logs to grep
- **Recoverable without human watching** -- retries known failure patterns, escalates only when stuck
- **Branch-aware** -- one git branch per task, no merge conflicts
- **Event-first** -- emits typed events, not terminal scrollback
- **Capable of autonomous next-step** -- when one task finishes, it knows what's next

You don't need all of that on day one. You need enough to walk away from the terminal.

---

## Step 1: The 30-Line Harness You Can Build Tonight

Start with a shell script. Not Rust. Not Go. A shell script that wraps your existing agent CLI.

Here's the minimum:

```bash
#!/bin/bash
# ~/harness/run.sh -- your first harness

TASK="$1"
WORKDIR="${2:-.}"
SESSION_ID="$(date +%s)"
HARNESS_DIR="$HOME/.harness/sessions"

mkdir -p "$HARNESS_DIR"

# 1. Structured boot -- same preamble every time
BOOT_PROMPT="Session: $SESSION_ID
Work directory: $(pwd)
Branch: $(git branch --show-current)
Task: $TASK

On failure: retry transient errors once.
On completion: write a 3-line summary to $HARNESS_DIR/$SESSION_ID/summary.md
On blockage: write what's blocking you to $HARNESS_DIR/$SESSION_ID/blocked.md"

# 2. Run the agent
your-agent-cli --prompt "$BOOT_PROMPT" 2>&1 | tee "$HARNESS_DIR/$SESSION_ID/raw.log"

EXIT_CODE=${PIPESTATUS[0]}

# 3. One-retry recovery for transient failures
if [ $EXIT_CODE -ne 0 ]; then
    if grep -qiE "rate.limit|timeout|connection.refused|502|503" "$HARNESS_DIR/$SESSION_ID/raw.log"; then
        echo "[harness] Transient failure detected, retrying in 30s..."
        sleep 30
        your-agent-cli --prompt "$BOOT_PROMPT" 2>&1 | tee -a "$HARNESS_DIR/$SESSION_ID/raw.log"
        EXIT_CODE=${PIPESTATUS[0]}
    fi
fi

# 4. Phone notification -- outside agent context
if [ $EXIT_CODE -eq 0 ]; then
    STATUS="✅ completed"
else
    STATUS="❌ blocked"
fi

curl -s -X POST "$DISCORD_WEBHOOK_URL"     -H "Content-Type: application/json"     -d "{\"content\": \"**$SESSION_ID**: $STATUS\nTask: $TASK\nBranch: $(git branch --show-current)\"}"

echo "[harness] Session $SESSION_ID: $STATUS"
```

That's it. Replace `your-agent-cli` with whatever you use (claude, codex, openclaw, goclaw). Set `DISCORD_WEBHOOK_URL` in your environment. Run:

```bash
harness/run.sh "Add rate limiting to /auth endpoints" ~/projects/myapp
```

You now have: consistent boot, one-retry recovery, and a notification on your phone when work finishes or blocks. That's already more than most agent users have.

---

## Step 2: Structured State (So You Can Resume)

Raw logs tell you what happened. Structured state tells you what to do next.

Replace the log-only approach with a session file your harness writes and reads:

```json
// ~/.harness/sessions/1716500000.json
{
  "id": "1716500000",
  "task": "Add rate limiting to /auth endpoints",
  "status": "completed",
  "branch": "feat/rate-limit-auth",
  "exit_code": 0,
  "summary": "Added token bucket rate limiter to /auth/* with Redis backend",
  "pr_url": "https://github.com/you/repo/pull/42",
  "started_at": "2026-05-06T14:30:00Z",
  "duration_seconds": 187
}
```

Now add a `list` command:

```bash
#!/bin/bash
# ~/harness/list.sh
for f in ~/.harness/sessions/*.json; do
    jq -r '\(.id)  \(.status)\t\(.branch)\t\(.task)' "$f"
done
```

And a `resume` command:

```bash
#!/bin/bash
# ~/harness/resume.sh
SESSION_ID="$1"
STATE_FILE="$HOME/.harness/sessions/$SESSION_ID.json"

if [ ! -f "$STATE_FILE" ]; then
    echo "Session not found: $SESSION_ID"
    exit 1
fi

STATUS=$(jq -r .status "$STATE_FILE")
if [ "$STATUS" = "blocked" ]; then
    echo "Resuming blocked session $SESSION_ID..."
    BLOCKED_REASON=$(cat "$HOME/.harness/sessions/$SESSION_ID/blocked.md")
    harness/run.sh "Previous session $SESSION_ID was blocked. Reason: $BLOCKED_REASON. Continue the work."
else
    echo "Session $SESSION_ID is $STATUS, not blocked. Nothing to resume."
fi
```

You can now check status with `harness list` and pick up a blocked session with `harness resume 1716500000` -- from your phone, while the agent runs on a machine you haven't looked at in hours.

---

## Step 3: One Branch Per Task

The simplest coordination pattern that prevents merge conflicts: every harness session gets its own git branch.

```bash
# At the top of run.sh, after setting SESSION_ID:
BRANCH="harness/$SESSION_ID"
git checkout -b "$BRANCH" 2>/dev/null || git checkout "$BRANCH"

# At the bottom, on success:
if [ $EXIT_CODE -eq 0 ]; then
    git push origin "$BRANCH"
    gh pr create \
        --title "$TASK" \
        --body "Auto-generated by harness session $SESSION_ID. $(cat "$HARNESS_DIR/$SESSION_ID/summary.md")" \
        --base main \
        --head "$BRANCH"
fi
```

Now you can run multiple harness sessions in parallel -- different worktrees, different branches, no conflicts. This is the ClawTeam pattern applied to a single user.

---

## Step 4: Event Routing (the clawhip Pattern)

Thus far your harness script posts to Discord directly. That works for one harness, but doesn't scale. The next step: a small event router that sits between your agent and your notifications.

```bash
# In run.sh, replace the direct curl with a pipe:
your-agent-cli --prompt "$BOOT_PROMPT" 2>&1 | harness-events --session "$SESSION_ID"
```

Where `harness-events` is a small program (choose your language):

```
stdin -> parse known patterns -> emit typed events -> route to sinks
```

The events look like this:

```
session.started   {id, task, branch, timestamp}
tool.used         {name, args, duration_ms}
tool.failed       {name, error, retry}
session.completed {id, summary, pr_url, duration_s}
session.blocked   {id, reason, last_tool}
```

The router maps events to actions:

| Event | Action |
|-------|--------|
| `session.completed` | Post summary to Discord, open PR |
| `session.blocked` | DM you on Discord with the blocking reason |
| `tool.failed` | If retryable, tell agent to retry |
| `session.started` | Post brief status to a #harness-log channel |

The key insight from clawhip: **keep monitoring and delivery outside the agent's context window**. The agent shouldn't burn tokens formatting Discord messages. A 50-line event parser does that job for free.

Minimal implementation in Python:

```python
#!/usr/bin/env python3
import sys, json, re, os, requests, time

WEBHOOK = os.environ["DISCORD_WEBHOOK_URL"]
SESSION = sys.argv[2] if len(sys.argv) > 2 else "unknown"

PATTERNS = {
    "tool.used": re.compile(r"Running tool: (\w+)"),
    "tool.failed": re.compile(r"Error running tool (\w+): (.+)"),
    "session.completed": re.compile(r"Task completed"),
    "session.blocked": re.compile(r"Cannot proceed: (.+)"),
}

def emit(event_type, data=None):
    event = {"type": event_type, "session": SESSION, "ts": time.time()}
    if data: event["data"] = data
    print(json.dumps(event))

    msgs = {
        "session.completed": f"✅ **{SESSION}**: Task completed",
        "session.blocked": f"❌ **{SESSION}**: Blocked -- {data}",
    }
    if event_type in msgs:
        requests.post(WEBHOOK, json={"content": msgs[event_type]})

for line in sys.stdin:
    for event_type, pattern in PATTERNS.items():
        m = pattern.search(line)
        if m:
            emit(event_type, m.group(1) if m.lastindex else None)
            break
```

This is ~30 lines. It gives you typed events, structured logging, and Discord routing -- none of which the agent had to think about.

---

## What NOT to Build First

After reading the UltraWorkers architecture, it's tempting to build the whole stack: OmX workflow layer, clawhip event router, OmO multi-agent coordinator, plus a clean-room Rust agent harness. Don't.

| Don't build | Why | Build instead |
|-------------|-----|---------------|
| A multi-agent coordinator | Single-agent harness is useful today | `run.sh` |
| A clean-room agent rewrite | Your existing agent CLI works | Wrap it |
| A full event pipeline | Shell + webhook = 80% of value | `harness-events` (30 lines) |
| A workflow DSL | Natural language tasks work fine for one person | Plain English task strings |

The UltraWorkers stack exists because it coordinates agents across a team. For a personal harness, the minimal version is the right version.

---

## Stack Choices by Your Comfort Zone

| Your Language | Harness Approach | Why |
|---------------|-----------------|-----|
| **Shell / Python** | Bash wrapper + Python state manager | Fastest path to a working prototype |
| **Go** | Single Go binary | Maxclaw-style; good fit for long-running daemons |
| **Rust** | Rust binary | ZeroClaw-style; the claw-code reference (48K LOC) is in Rust |
| **TypeScript** | Node.js daemon | Easy Discord/webhook integration; OpenClaw ecosystem |

Start with whatever you'd use to write a cron job. The harness is infrastructure -- reliability matters more than features.

---

## The Endgame: Type a Sentence, Walk Away

What you're building toward, one step at a time:

```
You (on phone, 10pm):
  "add two-factor auth with TOTP, write tests, open PR"

Harness (on your machine):
  1. Boots agent with structured context
  2. Creates branch harness/1716500000
  3. Agent writes code, runs tests, fixes failures
  4. Harness retries transient errors without waking you
  5. Agent finishes, writes summary
  6. Harness opens PR, posts to Discord
  7. You wake up to: ✅ feat/2fa-totp ready for review

You (on phone, 7am):
  "lgtm, merge it"
```

That's not science fiction. It's a shell script, a structured state file, a git branch, and a webhook -- each piece under 50 lines. The harness doesn't need to be smart. It needs to be reliable, recoverable, and event-driven. The agent provides the intelligence. The harness provides everything else.

---

## Further Reading

- [Agent Harnesses & Toolchains](/architecture/agent_harnesses.md) -- Full architecture reference for the UltraWorkers stack (claw-code, clawhip, OmX, OmO)
- [Unified Platform Comparison](/architecture/platform_comparison.md) -- Compare 20 agent platforms to find the right engine for your harness
- [Latest Ecosystem Updates](/docs/LATEST_UPDATES.md) -- What's changing across the platforms you might wrap

---

*Part of: AllClaws Personal AI Agent Ecosystem Research*
*Methodology: Patterns synthesized from the UltraWorkers toolchain and claw ecosystem coordination research.*
