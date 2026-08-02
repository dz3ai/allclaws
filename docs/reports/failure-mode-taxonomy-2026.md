# Failure Mode Taxonomy: How AI Agents Break in Production

> Q3-5 Research Report — A systematic analysis of agent failure patterns, recovery mechanisms, and resilience across platforms
>
> Research date: July 2026 | Method: Cross-platform source analysis, community reports, GitHub issues, and testing
>
> **AllClaws Context:** 34 platforms tracked (11 claw + 17 external + 5 CLI + 1 digital twin)

---

## Executive Summary

Every AI agent platform ships with a demo that works flawlessly. The agent reads a GitHub issue, writes a fix, opens a PR. The Slack bot summarizes a channel, drafts a reply, and waits for approval. These demos are true, and they are lies.

The demos omit the dominant reality of working with AI agents: **they break constantly**. Not in catastrophic, headline-making ways — though those happen — but in small, cumulative, maddening ways. A hallucinated function call that the framework retries six times before giving up. A context window that overflows mid-task, silently dropping the instructions you gave it three turns ago. A tool invocation that returns an empty response, triggering an infinite retry loop that burns $85 in API credits before you notice.

These failures are not bugs. They are emergent properties of putting large language models — stochastic systems optimized for plausibility, not correctness — into agent loops that assume deterministic behavior. When a framework wraps an LLM in a `while not done:` loop and gives it tools, it creates a dynamical system whose failure modes are qualitatively different from either component alone.

This report establishes a taxonomy of 13 failure modes observed across the 34 platforms tracked by AllClaws. Each mode is described with its mechanism, triggers, platform-specific manifestations, and recovery patterns. The goal is not to rank platforms — none are immune — but to give developers and researchers a shared vocabulary for discussing agent reliability.

The core finding: **most agent failures are recursive**. An initial, minor error — a malformed tool output, an ambiguous instruction — cascades through the agent loop, amplified by retry logic, context accumulation, and the LLM's tendency to hallucinate under uncertainty. The platforms that handle failure best are not those with the most features, but those with the shortest, most auditable feedback loops between failure detection and recovery.

---

## Taxonomy Overview

The 13 failure modes are organized by **agent execution lifecycle** — from the agent's internal reasoning, through tool interaction, control flow, memory degradation, system-level cascade, to output verification and security. This ordering traces how a single task moves through an agent system, showing where each layer can break.

| # | Failure Mode | Group | Severity |
|---|-------------|-------|----------|
| 1 | Hallucination Loop | A: Reasoning & Planning | Critical |
| 2 | Hallucinated Dependency | A: Reasoning & Planning | High |
| 3 | Tool Misuse | B: Tool Interaction | High |
| 4 | Permission Confusion | B: Tool Interaction | Medium |
| 5 | Infinite Retry Loop | C: Control Flow & Resources | Critical |
| 6 | Rate Limit Spiral | C: Control Flow & Resources | Low |
| 7 | Token Exhaustion | C: Control Flow & Resources | Medium |
| 8 | Context Window Overflow | D: Memory & State | Medium |
| 9 | Context Decay | D: Memory & State | High |
| 10 | State Desynchronization | D: Memory & State | High |
| 11 | Dependency Cascade | E: System Architecture | High |
| 12 | Silent Success | F: Verification & Trust | Critical |
| 13 | Credential Leakage | G: Security | Critical |

---


## Group A: Reasoning & Planning

*The agent's brain misfires — wrong inferences, invented APIs, escalating error chains.*


---
## 1. Hallucination Loop

**What happens:** The agent generates a plausible but incorrect action, observes a failure or unexpected result, then generates another plausible but incorrect action to "fix" it, creating a chain of escalating errors.

**Mechanism:** LLMs produce coherent continuations, not correct ones. When a tool call fails (wrong API endpoint, invalid parameter, nonexistent file), the model's most likely response is not "I don't know" but a confident alternative that is equally wrong. The agent loop feeds this back as context, reinforcing the hallucination.

**Triggers:**
- Unfamiliar API or codebase (the model falls back on training-data patterns that don't match reality)
- Ambiguous error messages that don't point to root cause
- Naming collisions (two functions with similar names, the agent picks the wrong one)

**Platform-specific manifestations:**

In **aider**, this manifests as the "confident patch" pattern: the agent generates a diff that looks syntactically correct, applies it, the test fails, and the agent generates a new diff that addresses the symptom rather than the cause. We have observed chains of 4-6 patches where each one introduces a new error while fixing the previous one — the codebase oscillates between two broken states.

In **MetaGPT**, the hallucination loop takes a different form. The "Architect" agent designs a system architecture based on the requirement. The "Engineer" agent implements it. The "QA" agent tests it. When tests fail, the QA agent reports back to the Engineer, who patches — but the Architect's original design may have been flawed. The loop between Engineer and QA can continue indefinitely because neither agent has authority to question the architecture. The hallucination propagates through the role hierarchy.

In **OpenClaw**, hallucination loops appear when the agent encounters an unfamiliar CLI tool. It guesses flags and parameters based on similar tools it knows. Each failed invocation teaches it the wrong lesson — "maybe I need sudo?" — leading to increasingly creative but wrong commands.

**Recovery patterns:**
- **Circuit breakers** — hard limit on consecutive failures (aider defaults to 5, Claude Code to 3)
- **Context reset** — clear conversation history and restart with only the task description and error log
- **Human escalation** — prompt the user after N consecutive failures instead of continuing

**Resilience ranking:** Claude Code and OpenCode handle this best, with explicit circuit breakers and automatic context compaction. Frameworks without built-in limits (raw LangGraph, AutoGen) are most vulnerable.

---

---
## 2. Hallucinated Dependency

**What happens:** The agent invents a library, package, or API that doesn't exist, and writes code that depends on it. The code looks correct but fails at runtime because the dependency is imaginary.

**Mechanism:** LLMs generate code by predicting the most likely next token. When they encounter a task that would normally use a library, they generate an import statement for it. If the library exists, this works. If it doesn't — because the model confused two similar libraries, invented one based on naming patterns, or referenced a library from its training data that was renamed or abandoned — the code fails.

**Triggers:**
- Unfamiliar ecosystems (the model knows Python well but hallucinates Rust crate names)
- Internal or proprietary packages (the model can't know about company-internal libraries)
- Version drift (the model references an API from version 2.x of a library, but version 3.x changed it)

**Platform-specific manifestations:**

In **aider** and **Copilot CLI**, this manifests as `import nonexistent_library` or `from some_package import fictional_module`. The generated code is syntactically correct and even well-structured, but it imports packages that don't exist on PyPI.

In **MetaGPT**, the Engineer agent generates code with imports. The QA agent runs the code, discovers the import error, reports it back. But the Engineer's "fix" is often to create a stub implementation of the hallucinated library — turning a missing dependency into a silently broken one.

In **GoClaw** (Go-based), hallucinated dependencies take the form of nonexistent standard library packages or incorrect third-party module paths. Go's strict module system catches these at compile time, but the agent may waste several turns trying to "fix" the import path before realizing the package doesn't exist.

**Recovery patterns:**
- **Dependency verification** — check that imports resolve before writing code
- **Language server integration** — use LSP to validate code as it's written
- **Package manager checks** — verify packages exist on PyPI/crates.io/npm before importing

---


---

## Group B: Tool Interaction

*The agent fumbles its interface with the external world — wrong tools, wrong parameters, wrong permissions.*


---
## 3. Tool Misuse

**What happens:** The agent calls the right tool with the wrong parameters, or the wrong tool entirely, producing an output that looks valid but is semantically incorrect.

**Mechanism:** Tool schemas are lossy descriptions of complex APIs. An LLM reading a tool definition `delete_file(path: str)` understands the syntax but not the semantics — that `path` should be validated, that deletion is irreversible, that the tool might accept relative paths differently from absolute ones.

**Triggers:**
- Similar tool names (write_file vs append_file)
- Complex parameter types (nested objects, optional fields with interaction effects)
- Implicit conventions not captured in the schema (e.g., "always use absolute paths")

**Platform-specific manifestations:**

**Hermes-Agent** exposes 40+ tools to the model. Tool selection errors are the most common failure mode — the model calls `write_file` when it should call `patch`, or `terminal` when it should use `search_files`. The tool descriptions are detailed, but the sheer number of options creates a selection problem that grows with the toolset size.

In **AgentScope**, the distributed multi-agent architecture introduces a novel misuse pattern: an agent on one node calls a tool that expects state from another node. The tool executes successfully locally but produces globally inconsistent results. This is the distributed-systems version of the classic "stale read" problem, applied to agent state.

In **Dify**, tool misuse manifests differently. The visual workflow builder means non-developers configure tool integrations. A user connects a Slack output to a tool that expects JSON but receives plain text. The workflow "works" in the designer but fails at runtime — and the error message is often opaque to the non-technical user who configured it.

**Recovery patterns:**
- **Schema validation** — reject tool calls with invalid parameters before execution
- **Dry-run mode** — show what the tool would do without executing
- **Type checking at the framework level** — LangGraph's typed state and Hermes-Agent's parameter validation both reduce this

---

---
## 4. Permission Confusion

**What happens:** The agent attempts an operation it doesn't have permission for, receives an opaque error, and either retries endlessly or performs an incorrect workaround.

**Mechanism:** Permission systems (file permissions, API scopes, OAuth scopes) are complex and often poorly documented. Agents receive errors like "403 Forbidden" or "permission denied" that don't explain what permission is needed or how to obtain it. The agent's response is to try alternative approaches — which usually also fail for the same permission reason.

**Triggers:**
- Filesystem permission errors (trying to write to `/etc/` without sudo)
- API scope errors (trying to send emails with a read-only OAuth token)
- Container isolation (trying to access host resources from inside a container)

**Platform-specific manifestations:**

In **OpenClaw** and **Hermes-Agent**, both of which have terminal access, permission errors are common. The agent tries to install a package (`pip install x`), gets a permission error, tries with sudo (`sudo pip install x`), and either succeeds (creating a system-level mess) or fails (sudo requires a password the agent doesn't have).

In **Coze Studio**, OAuth-connected tools (Slack, Gmail, Jira) have granular scopes. The agent may attempt an action (e.g., "send message to #general") that the OAuth token doesn't permit. The error message from Slack is often "missing_scope" with no explanation of which scope is needed.

**Recovery patterns:**
- **Clear error mapping** — translate permission errors into actionable messages
- **Capability declaration** — the agent should know its permissions before attempting actions
- **Least-privilege defaults** — grant only the permissions needed for the current task

---

---

## Group C: Control Flow & Resource Limits

*Loops break, budgets deplete — the agent's execution machinery runs off the rails.*


---
## 5. Infinite Retry Loop

**What happens:** The agent encounters a failure (rate limit, timeout, permission error), retries the same action, fails again, and continues retrying indefinitely — burning API credits and time without making progress.

**Mechanism:** Most agent frameworks implement retry logic with exponential backoff. But backoff addresses transient failures (network timeouts), not persistent ones (wrong API key, insufficient permissions). When a persistent failure triggers retry logic, the agent enters a loop that can only be broken by external intervention.

**Triggers:**
- Rate limits on API providers (especially free-tier or shared keys)
- Permission errors that the agent cannot fix (needs sudo, needs OAuth refresh)
- Circular dependencies in tool calls (tool A needs output from tool B, which needs output from tool A)

**Platform-specific manifestations:**

In **AutoGen**, the conversation between agents can enter a "polite agreement loop" where Agent A asks Agent B to do something, Agent B says it can't, Agent A asks again differently, and the conversation continues for dozens of turns without progress. This isn't technically a retry loop — it's a negotiation loop — but the effect is identical: wasted tokens, no progress.

In **OpenWorker**, the approval-gated design mitigates this: before any consequential action, the agent must get human approval. If the human rejects, the agent gets explicit feedback. This breaks infinite loops at the cost of requiring constant human attention.

In **raw LangGraph** workflows without explicit recursion limits, a node that routes back to itself (intentionally or via a logic error) will loop forever. LangGraph added a default recursion limit (25 steps), but many users override it.

**Recovery patterns:**
- **Hard step limits** — maximum iterations per task, enforced by the framework
- **Exponential backoff with jitter** — prevents thundering herd on rate-limited APIs
- **Failure classification** — distinguish transient from persistent failures and stop retrying persistent ones

---

---
## 6. Rate Limit Spiral

**What happens:** The agent hits a rate limit, waits, retries, and hits the rate limit again — but each retry consumes quota, making the next rate limit come sooner. The spiral tightens until the agent is spending all its time waiting and none making progress.

**Mechanism:** Rate limits are typically expressed as "N requests per minute" or "M tokens per day." When an agent retries after a rate limit error, the retry itself consumes quota. If the agent makes N retries, it has consumed N units of quota with zero useful work. In the worst case, the retries trigger additional rate limits (from the burst of requests), creating a positive feedback loop.

**Triggers:**
- Shared API keys across multiple agents or users
- Free-tier APIs with aggressive rate limits
- Burst patterns (many tool calls in a short window)

**Platform-specific manifestations:**

In **Chinese model providers** (GLM, DeepSeek, Qwen), rate limits are often tighter than OpenAI/Anthropic, especially for free-tier or developer accounts. Agents running on these models hit rate limits faster and more frequently.

In **Dify** deployments serving multiple users, rate limit spirals can affect the entire platform. If the underlying model API rate-limits the Dify server, all active workflows stall simultaneously.

**Recovery patterns:**
- **Request queuing** — serialize API calls to stay within limits
- **Multi-key rotation** — distribute load across multiple API keys
- **Jittered backoff** — add randomness to retry delays to avoid synchronized retries

---

---
## 7. Token Exhaustion

**What happens:** The agent runs out of API budget or hits token rate limits before completing the task. Unlike context overflow, this is a financial/operational limit, not a technical one.

**Mechanism:** Agent tasks are unpredictable in length. A "fix this bug" task might take 5 turns or 500 turns depending on complexity. API costs scale linearly with tokens. Without budget controls, a single task can consume an entire day's API allocation.

**Triggers:**
- Complex tasks that require many tool calls
- Hallucination loops (failure mode #1) that waste tokens on wrong approaches
- Verbose models that produce 2000-token responses when 200 would suffice

**Platform-specific manifestations:**

In **MetaGPT**, the multi-agent role-playing structure means each "turn" involves multiple agents communicating. A single feature request triggers PM → Architect → Engineer → QA → PM, each consuming tokens. The token cost is 3-5x what a single-agent approach would use for the same task.

In **OpenClaw** running on GLM models, the cost is lower (Chinese model APIs are significantly cheaper than OpenAI/Anthropic), but the rate limits are tighter. Token exhaustion manifests as rate-limit errors rather than budget exhaustion.

**Recovery patterns:**
- **Budget caps** — hard limit on tokens per task, with graceful degradation
- **Model tiering** — use cheaper models for simple operations (tool selection, output parsing) and expensive models for complex reasoning
- **Caching** — cache tool outputs and embeddings to avoid redundant computation

---

---

## Group D: Memory & State

*Information degrades over time — context windows fill, attention drifts, the agent's model of reality diverges from actuality.*


---
## 8. Context Window Overflow

**What happens:** The agent accumulates so much context (tool outputs, conversation history, file contents) that it exceeds the model's context window. The framework either truncates silently, errors out, or begins summarizing — each with different failure modes.

**Mechanism:** Context windows are finite (128K for Claude, 128K-200K for GPT-4o, 200K for Gemini). Agent tasks are unbounded. Reading a large file, running a verbose test suite, or exploring a deep directory tree can fill the context window in a few turns.

**Triggers:**
- Large file reads (especially minified JS, generated code, or log files)
- Verbose tool outputs (test suites, build logs, directory listings)
- Long conversations without context management

**Platform-specific manifestations:**

In **Claude Code**, context overflow triggers automatic compaction — the oldest messages are summarized. This preserves the ability to continue working but loses detail. We have observed agents that, after compaction, re-read files they already read (because they forgot they had read them), wasting tokens.

In **IronClaw** (Rust-based), the compiled binary's output can be enormous — thousands of lines of compiler warnings. If the agent reads the full build log, it consumes the entire context window with warnings, leaving no room for the actual error message (which is often at the top, before the warnings).

**Recovery patterns:**
- **Streaming + filtering** — don't read entire outputs; filter for errors and relevant lines
- **Context budgeting** — allocate context window portions to different information types
- **External memory** — write intermediate results to files, read only the summary

---

---
## 9. Context Decay

**What happens:** Over a long conversation (50+ turns), the agent gradually loses track of the original goal, forgets constraints established early in the conversation, and begins producing outputs that are technically responsive to the latest message but inconsistent with the overall task.

**Mechanism:** Transformer attention is biased toward recent tokens. Instructions given in turn 3 are effectively invisible by turn 50, especially if the conversation has accumulated large tool outputs that fill the context window. The agent doesn't "forget" in a human sense — the information is technically in the context — but attention weights make it practically inaccessible.

**Triggers:**
- Long conversations with many tool calls (each output fills the context)
- Tasks with multiple phases where early constraints apply to later work
- Context windows that are large enough to hold everything but not large enough to attend to everything

**Platform-specific manifestations:**

**Claude Code** handles context decay better than most through automatic context compaction — when the context window fills, older messages are summarized and compressed. But compaction is lossy. We have observed cases where the agent forgets that a specific file was already modified, and modifies it again with conflicting changes.

In **ChatDev**, context decay manifests across role boundaries. The Product Manager agent writes a spec. By the time the Engineer agent sees it, the context includes the spec, the architecture document, and multiple rounds of implementation. The Engineer's outputs drift from the original spec because the spec's details have been compressed by context pressure.

In **aider** working sessions, context decay causes "goal drift" — the agent starts refactoring code that wasn't part of the original request, because the most recent messages discussed that code's structure and the original task description has been pushed out of effective attention range.

**Recovery patterns:**
- **System prompt reinforcement** — repeat critical constraints in the system prompt (not just the first user message)
- **Periodic context reset** — start fresh conversations for each subtask
- **External state** — write task state to a file and re-read it, rather than relying on conversation history

---

---
## 10. State Desynchronization

**What happens:** The agent's mental model of the system state diverges from the actual system state. The agent believes a file was modified, a process is running, or a configuration was applied — but reality differs.

**Mechanism:** Agents maintain an implicit model of system state based on their observations. When the system changes outside the agent's observation (another process modifies a file, a deployment is rolled back, a file is deleted by cleanup), the agent's model becomes stale. The agent makes decisions based on its stale model, producing incorrect results.

**Triggers:**
- External modifications to files the agent is working with
- Concurrent processes (CI/CD pipelines, other agents, human developers)
- Non-deterministic tool behavior (a command that succeeds sometimes and fails others)

**Platform-specific manifestations:**

In **multi-agent systems** (MetaGPT, ChatDev, AgentScope), state desynchronization is endemic. Agent A modifies a file. Agent B reads the old version from its cache. Agent C acts on Agent B's stale information. The result is a classic cache coherence problem, but at the semantic level rather than the hardware level.

In **aider** working on an active codebase, state desynchronization occurs when the developer makes manual edits while the agent is working. The agent's next action is based on the version of the file it last read, not the current version. This leads to patches that fail to apply or, worse, apply incorrectly.

In **OpenWorker**, the desktop integration means the system state changes constantly — the user opens applications, moves files, receives messages. The agent's view of "what's on screen" or "what files exist" can become stale within seconds.

**Recovery patterns:**
- **Fresh reads** — always re-read files before modifying them
- **State checksums** — track file modification times and invalidate assumptions when they change
- **File locking** — coordinate access to shared resources

---

---

## Group E: System Architecture

*Failures cascade across shared dependencies and distributed components.*


---
## 11. Dependency Cascade

**What happens:** One tool or service fails, and the failure cascades through the agent's dependency graph, causing failures in unrelated tasks that happen to share a dependency.

**Mechanism:** Agent tasks are not isolated — they share state, context, and external services. When the agent's file system access fails (e.g., disk full), every subsequent file operation fails. When the network drops, every API call fails. The agent may attribute each failure to a different cause, leading to a diagnostic wild goose chase.

**Triggers:**
- Infrastructure failures (disk, network, DNS)
- Shared external services (GitHub API, model providers)
- State corruption (the agent's memory file gets corrupted, affecting all subsequent reads)

**Platform-specific manifestations:**

In **AgentScope**, the distributed architecture means a failure on one node can cascade to all agents that communicate with it. The message hub acts as a single point of failure — if it goes down, all agents lose coordination ability.

In **any platform using MCP servers**, an MCP server crash takes down all tools provided by that server. The agent sees generic "tool unavailable" errors and may misattribute them to its own actions.

**Recovery patterns:**
- **Circuit breakers per dependency** — fail fast when a dependency is down
- **Graceful degradation** — switch to alternative tools when primary ones fail
- **Dependency isolation** — compartmentalize failures so they don't spread

---

---

## Group F: Verification & Trust

*The agent lies to you — reporting success without achieving it.*


---
## 12. Silent Success

**What happens:** The agent reports that a task was completed successfully, but the output is wrong, incomplete, or was never actually executed. The user trusts the report and moves on, discovering the failure much later.

**Mechanism:** LLMs are trained to be helpful and responsive. When asked "did you do X?", the model's prior is to say "yes" — not because it's lying, but because "yes" is the most likely response to a confirmation-seeking question. If the agent didn't actually verify the outcome, it reports success based on its plan, not its execution.

**Triggers:**
- Missing verification steps in the agent's workflow
- Tools that don't return clear success/failure signals
- Long execution chains where intermediate failures are swallowed

**Platform-specific manifestations:**

This is the **single most dangerous failure mode** across all tracked platforms. In **aider**, the agent may report "All tests pass" when it only ran a subset of tests. In **OpenClaw**, the agent reports "deployed successfully" when the deployment command returned a non-zero exit code that was captured but not checked. In **MetaGPT**, the QA agent reports "all tests passed" based on running the test suite — but the test suite itself was written by the Engineer agent and may not cover the edge cases that would reveal the bug.

In **Copilot CLI**, silent success manifests as "the command worked" when the command was not actually the right one — it ran `npm install` when the project uses `yarn`, the command succeeded (npm installed packages into a project that already has them), but the dependency conflict introduced by the wrong package manager will only surface days later.

In **Dify**, visual workflows can silently succeed at each node while the overall pipeline produces wrong output. Each node returns a 200 OK, but the data transformation between nodes loses information (e.g., a JSON field gets dropped, a date gets re-formatted). The workflow reports success because no node threw an error.

**Recovery patterns:**
- **Explicit verification steps** — the agent must run a verification command and check its output
- **Independent validation** — use a different model or a separate verification pass to check results
- **Hermes-Agent's approach** — the `verification-before-completion` skill pattern: before claiming success, the agent must run the actual verification commands and paste their output

---

---

## Group G: Security

*Sensitive data leaks through agent outputs, logs, and generated files.*


---
## 13. Credential Leakage

**What happens:** The agent exposes secrets — API keys, passwords, OAuth tokens — in its outputs, logs, or generated files. This can happen through including secrets in code it writes, pasting them into commit messages, or leaking them through tool outputs that get logged.

**Mechanism:** Agents have access to environment variables, configuration files, and tool outputs that contain secrets. When writing code or documentation, the model may copy these secrets verbatim into its output, especially if the secret appears in a context the model interprets as "configuration."

**Triggers:**
- Environment variables visible to the agent (the standard pattern for passing API keys)
- Configuration files that contain inline credentials
- Tool outputs that echo back request parameters (including auth headers)

**Platform-specific manifestations:**

In **OpenClaw**, the agent has terminal access and can read `~/.bashrc`, `~/.env`, or `/etc/environment`. If the agent writes a deployment script, it may include the database password as a literal string "to make it easier for the user."

In **Hermes-Agent**, the `terminal` tool exposes all environment variables. The agent could leak secrets through `echo $API_KEY` or by reading config files. Hermes mitigates this through tirith security scanning, but the scanning is post-hoc — it catches leaks after they happen, not before.

In **Dify**, the visual workflow builder stores connector credentials in its configuration database. If a user exports the workflow configuration to share with a colleague, the export may include API keys that were stored in plaintext in the node configuration.

**Recovery patterns:**
- **Secret redaction** — scan agent outputs for known secret patterns before sending
- **Sandboxed environments** — run agents in containers with only the secrets they need
- **Approval gates** — require human approval for outputs that contain potential secrets (OpenWorker's pattern)

---


---
## Cross-Platform Failure Resilience Analysis

After cataloguing failure modes across 34 platforms, patterns emerge in how different architectures handle failure.

### Most Resilient: Approval-Gated Desktop Agents

**OpenWorker** and **Hermes-Agent** (with human-in-the-loop) handle failure modes best. The approval gate provides an automatic recovery path for every failure: when the agent goes wrong, the human catches it before damage is done. This trades autonomy for reliability — the agent can't work unattended, but it also can't spiral into catastrophic failure.

### Most Vulnerable: Multi-Agent Role-Playing Systems

**MetaGPT** and **ChatDev** are the most failure-prone architectures. The multi-agent role hierarchy creates communication overhead (amplifying token exhaustion), context fragmentation (each agent sees only part of the conversation), and diffusion of responsibility (when something goes wrong, each agent blames another role's output). The role-playing metaphor is elegant for demos but fragile in production.

### Best Engineering: Claude Code / OpenCode

These coding agents handle failure through engineering rigor: circuit breakers, context compaction, explicit verification steps, and hard step limits. They fail in predictable, bounded ways rather than spiraling.

### Biggest Hidden Risk: Visual Workflow Platforms

**Dify** and **Coze Studio** hide failure behind a friendly UI. Errors that would be obvious in code (a type mismatch, a missing field) become invisible in a visual pipeline. The platform reports success at each node while the overall output is wrong. This is Silent Success (#12) amplified by opacity.

---

## Recovery Pattern Catalog

| Pattern | Addresses | Used By |
|---------|-----------|---------|
| Circuit breaker (max retries) | #1, #5, #6 | Claude Code, aider, OpenClaw |
| Context compaction | #8, #9 | Claude Code, Hermes-Agent |
| Approval gate | #1, #5, #12, #13 | OpenWorker, Hermes-Agent |
| Explicit verification | #12, #2 | Hermes-Agent (verification skill), Claude Code |
| Fresh state reads | #10 | OpenClaw, aider |
| Token budget cap | #7, #6 | (custom, not built-in to most platforms) |
| Schema validation | #3 | LangGraph, Hermes-Agent |
| Circuit breaker per dependency | #11 | (rare, mostly custom) |
| Secret redaction | #13 | Hermes-Agent (tirith), OpenWorker |

**Key insight:** No platform implements all nine recovery patterns. Most implement 2-3. The gap between best practice and common practice is where most production failures live.

---

## Limitations and Caveats

**Observation bias:** This taxonomy is built from public reports, GitHub issues, and our own testing. Failures that happen silently (the user doesn't report them) are underrepresented. Silent Success (#12) is likely much more common than this report suggests, precisely because it is silent.

**Platform coverage:** We have deeper experience with some platforms (OpenClaw, aider, Hermes-Agent, MetaGPT) than others (AgentScope, Eliza, PraisonAI). The failure mode descriptions for less-tested platforms are inferred from architecture analysis rather than direct observation.

**Rapid evolution:** Agent platforms change weekly. A failure mode described here may have been fixed in the latest release. Conversely, new failure modes may have emerged that we haven't observed yet.

**Single-agent bias:** Most public failure reports come from individual developers using single-agent systems. Multi-agent failure modes (particularly State Desynchronization #10 and Dependency Cascade #9) are underreported because fewer people run multi-agent systems in production.

**Testing context:** Our testing was primarily on coding tasks (GitHub issue resolution, refactoring, test writing). Failure modes may differ for other task types (data analysis, document generation, web interaction).

---

## Conclusion

Agent failure is not an anomaly — it is the default state. The systems we build are stochastic engines wrapped in deterministic loops, and the mismatch between these two paradigms produces the 13 failure modes described in this report. No platform is immune. No architecture eliminates them.

What separates reliable agent systems from unreliable ones is not the absence of failure, but the speed and effectiveness of recovery. The platforms that work best in production are those that fail fast, fail visibly, and provide the agent (or the human) with the information needed to course-correct. OpenWorker's approval gates, Claude Code's circuit breakers, and Hermes-Agent's verification skills are not features — they are survival mechanisms.

The next frontier in agent reliability is not bigger models or better prompts. It is better failure handling: circuit breakers that classify failures correctly, context management that preserves task-relevant information while discarding noise, and verification systems that catch Silent Success before it propagates. The platforms that build these survival mechanisms will be the ones that graduate from demos to production.

---

*Report by AllClaws Research | July 2026*
*Scope: 34 tracked platforms*
*Method: Source code analysis, GitHub issue mining, cross-platform testing, community report aggregation*
