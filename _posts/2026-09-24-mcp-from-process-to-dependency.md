---
layout: post
title: "MCP Is a Protocol — So Why Are You Babysitting Processes?"
date: 2026-09-24 10:05:00 +0800
author: Danny Zeng
categories: [Ecosystem Analysis]
tags: [mcp, hermes-agent, codex, kimi-code, connectors, dependency-management, token-overhead, architecture]
---

You gave your agent seven MCP servers — filesystem, browser, database, GitHub — and wrote the config once, then once more for each new machine. Then one day the agent quietly gets dumber. A server died. Half the tool catalog vanished. The agent never mentions it; it just starts saying "I can't do that" more often. An hour of log-digging later you find the cause: the local application behind that server was never running.

Or the config you imported onto a new machine fails wholesale, because the file records *how to start a process* and nothing about *what that process needs in order to exist*. Commands copy. Dependencies don't.

And then there's the bill. Every turn of every conversation, the agent's context carries the full schema of every mounted tool — whether or not this turn uses any of them. These aren't abstract complaints; they're numbers we counted one by one with tiktoken in our July MCP deep-dive.

All three symptoms share a root cause, and this week **Hermes-Agent** — one of the 35 platforms we track — answered it with an architecture-level restructuring: **MCP servers have been managed as processes, and the process is the wrong abstraction.**

*This is the first post in a short series on MCP productization. The next one digs into the Codex route — MCP as a multi-tenant protocol.*

---

## Three blind spots

What exactly is wrong with treating an MCP server as a process? Unpacked, it's three blind spots that nobody owns.

The **existence blind spot**: the config says "run this command," but it never answers "is the application this server depends on actually installed on this machine?" If it isn't, you get a failed spawn and an error line that explains nothing. Configs aren't portable across machines because the concept of a dependency declaration doesn't exist in the format at all.

The **liveness blind spot**: once the server starts, its lifecycle and the agent's go their separate ways. The application behind it exits? The server becomes a zombie, its tool catalog still mounted in the agent's context, spending tokens and advertising capabilities that no longer exist. The agent has no perception of *why its tools vanished* — it just performs "getting dumber."

The **dependency blind spot**: an MCP server is usually the terminal block of some application — browser servers depend on the browser, code servers depend on the IDE. But in today's integration layers that relationship is invisible: nobody declares it, nobody checks it, nobody follows it.

Stack the three together and you get the opening scene: you are the dependency manager, manual and uncredited. You remember which server needs which app, you discover deaths by eyeballing, you guess causes from experience. The human is doing the machine's job — and doing the most tedious part of it.

Three blind spots, one conclusion: **MCP integration doesn't need more servers. It needs a dependency-management layer.**

---

## The bill: zombie tools charge by the token

Before the architecture, the accounting. Our MCP deep-dive Phase 3 report — static reconstruction: representative payloads from ten official MCP servers, each platform's context-processing logic replicated, counted with tiktoken cl100k_base — produced hard numbers for the eager-mount-everything baseline. One server: 8 tools, 560 tokens, about 70 per tool. Three servers: 26 tools, 2,034 tokens. Five: 37 tools, 2,821. Ten: 56 tools, 3,998 tokens — roughly **73 tokens per tool schema**, every turn, no discount for the tools you didn't use. That's the real invoice of a zombie tool: it doesn't just block the road, it bills per conversation turn.

The industry isn't lying down. The same measurement found **ZeroClaw**'s deferred loading (lightweight stubs plus a `tool_search` tool) cutting N=10 overhead to 1,107 tokens — **72.3% saved**. **GoClaw**'s search mode is more radical: the agent sees exactly one search tool, a constant **183 tokens** no matter how many servers are configured — **95.4% saved**. And there's a middle case: **Reasönix**'s canonicalized schemas compress N=10 from 3,998 to 3,859, a mere 3.5% — but its real savings are indirect, in cache-hit rates that only show up in live API traffic.

Neither approach is free. ZeroClaw's deferred mode costs a round trip: before using an MCP tool, the model must call `tool_search` — about 150 tokens per search. Three MCP tool uses in a ten-turn conversation means three extra searches, which is still overwhelmingly cheaper than hauling 56 full schemas (3,998 tokens) through every turn; the stubs themselves grow linearly, just with the slope dropping from ~73 to ~15 tokens per tool. GoClaw's constant-183 mode is the most thorough, but the agent loses the map of its own toolbox: tool selection goes from reading a menu to asking the kitchen what they can make — more planning burden on the model.

No silver bullet, then: what you save in context you pay in round trips or planning complexity. But the direction is settled — eager full mounting is on its way out.

These numbers and this week's Connectors restructuring are two faces of one coin. Token optimization decides *how large the catalog is*; Connectors decides *what in the catalog is real*. Volume and truth — until both are solved, MCP integration isn't engineering.

---

## Hermes's answer: the Connectors trilogy

Inside this week's Hermes-Agent release — 4,844 commits over seven days on main, v2026.9.21 shipped on 09-21 in its steady weekly cadence — the through-line isn't patchwork. It's a numbered trio of architecture moves, NS-941/942/943, product-named **Connectors**. Three moves, one per blind spot.

First, replace the mental model. The Desktop app's Connectors page formally retires the old MCP tab. Don't underestimate a renaming: the object of management shifts from "a pile of server processes" to "a set of connectors" — from processes to integration relationships. It sets the tone for everything that follows.

Second, NS-942: portable plugins declare their dependencies. A plugin's manifest must now state which application its server requires. The crucial part is the enforcement: **installation is refused outright on hosts that can't satisfy the dependency.** Note the direction — not "install, then fail at runtime, then read a cryptic log," but "you don't install at all." For the first time a config carries a portability contract: installable means dependencies met; unmet, you learn it at step one instead of diagnosing it at step three. That closes the existence blind spot.

Third, NS-943: application-backed MCP servers whose lifecycle follows the application. The live endpoint is probed on every connection attempt; the tool catalog expands and contracts with the application's state — app alive, tools present; app dead, tools leave the catalog instead of leaving a zombie on the payroll; error messages state the reason — *why* the connection failed, not just that it timed out. Liveness and dependency blind spots, closed together.

Read the trilogy as one sentence: **the MCP server is promoted from "process configuration" to "application-dependency object."** Whether it installs is decided by the declaration; whether it lives is decided by the application's state; why it failed is stated in the error. This is software engineering's most battle-tested idea — package.json for dependencies, container images for environments — arriving in the agent tool layer.

The track record deserves trust. Before npm, frontend developers downloaded scripts by hand into a `lib` directory. Before Docker, ops engineers wrote "deployment docs" and prayed the new machine reproduced the old one. Every migration from implicit dependency to explicit declaration pushed "but it works on my machine" one step closer to death. MCP now stands at the same threshold — and the agent case is more urgent, because an agent's tool catalog isn't static. It moves with the life and death of the applications behind it; without declaration and probing, the system can't even answer *what should currently be there.*

---

## Under the hood: a three-layer resolver

Declared dependencies still need someone to verify them. Alongside the trilogy landed `hermes_platform.resolver`, a three-layer structure: *locate* (find where the application lives), *inspect* (what version, what state), *probe* (is its endpoint reachable), plus an AppResolver abstraction and gh lookup.

Why is "probe" the core verb of dependency management? Because every design above — install-time refusal, catalog expansion and contraction, errors that explain themselves — feeds on probe results. Without the resolver, a manifest's dependency line is a comment. With continuous probing, the declaration becomes a live constraint.

It also explains why the changes shipped together with a cluster of kanban fixes (query keys reactively rebuilt around `activeConnectionId` when the connection switches). Once "connection" becomes a first-class object, every piece of state that orbits connections — boards, queries, subscriptions — has to follow it. This isn't one feature landing; it's the migration tax a new concept pays on entry.

---

## The same week, another route: Codex governs MCP as a protocol

The interesting part: in the same week, **Codex** (OpenAI) took a different road. Lay the two routes side by side and the full picture of MCP productization comes into focus.

**Hermes, the application-dependency route.** Metaphor: the MCP server is a dependency of an application, package.json-style. Mechanisms: manifest-declared dependencies, install-time refusal, continuous endpoint probing, catalog elasticity. What it fixes: the single-machine user's "won't install, dies silently, can't explain why." This week: the NS-941/942/943 trilogy plus the resolver, shipped in v2026.9.21.

**Codex, the multi-tenant protocol route.** Metaphor: MCP is a multi-tenant protocol; requests carry identity and context. Mechanisms: MCP resource reads with app/account targets, trace context preserved across transport workers. What it fixes: request ownership and traceability when one agent serves several applications and accounts. This week: continued app-server v2 evolution, rust-v0.155.1 released 09-18.

The fork is a disagreement about MCP integration's first-order question. Hermes says it's local dependency: the user's pain is "won't install, dies quietly." Codex says it's identity: when multiple apps and accounts stand behind one agent, *whose request is this and whose trace covers it* is the fundamental problem. The routes don't exclude each other — one owns local reliability, the other server-side correctness; together they're the whole picture.

A third footnote: **kimi-code** added offline_access to its MCP OAuth request (#3979) — MCP authorization now has to think about OAuth lifecycle questions like "the token expired; can the server still work?" Stacked on last week's per-server MCP deferred disclosure (tool schemas disclosed lazily per server to cut first-screen token overhead), the token-slimming thread keeps extending.

Three threads, one judgment: **MCP integration is evolving from "mount at process launch" into a full integration system — with dependency contracts, with identity, with OAuth lifecycle.** Hermes takes dependency contracts, Codex takes identity and tracing, kimi-code takes authorization lifecycle: three vendors climbing toward the same layer from three different entrances.

---

## Back on the ecosystem map

None of this happened in a vacuum. By our 2026-09-22 submodule weekly report (29 repository paths, 35 platforms), thirteen platforms committed this week and eleven shipped releases — openclaw v2026.9.5, reasonix v1.38.11, hiclaw v1.2.4, nanobot v0.3.5, praisonai with a three-release week (4.7.8/9/10), and Moonshot formally archiving kimi-cli while kimi-code jumped versioning straight to 2.0 (0.43.x → 2.0, architecture swapped to agent-core-v2).

Amid the noise, MCP productization is one of the few themes where multiple platforms advanced in the same week *and* the directions stack. While model routing — the week's other paradigm signal, with **HiClaw** and **AgentScope** both promoting "which agent uses which model" into an explicit routing layer — decides *who does the work*, this MCP layer decides something more basic about the agent's hands: when the tool layer is available, why it isn't, and whether it still will be on a different machine. Foundation work. Un glamorous, and it decides how many floors you can build above.

Worth a sidebar: kimi-code 2.0's agent-core-v2 (the DI × Scope four-layer engine) is a session-management move, but it's the matching half of the tool-layer story. Its transcript subsystem got a four-layer data design — L1 granular storage up to L4 framework-agnostic views — giving tool-call recording, replay, and audit a structured foundation. A catalog that stretches and contracts is a dynamic behavior; it needs exactly this kind of storage to answer "who remembers it changed, and how to change it back." Session architecture and tool architecture upgrading simultaneously isn't a coincidence; multi-agent systems as a whole are moving from "works" to "operable."

Even the governance surface echoed the same week: RocketRide shipped client-mcp-v1.5.0-prerelease (09-14), and OpenClaw's root AGENTS.md now carries a "Codex sibling runtime hard gate" — any change touching Codex protocol behavior must be verified against `../codex` source before conclusions. Tool-ecosystem interdependence has grown strong enough to be written into agent collaboration norms.

---

## Why now: cost pressure is reaching the architecture layer

Look back and this wave didn't come from nowhere. The same weekly report carries a cross-project insight: **a prompt/token slimming movement is spreading across the head platforms.** OpenHuman merged its hermes-prompt-diet PR, cutting prompt budget ceilings across agents and tools; Eliza now declares its batch-scope rules once per prompt instead of repeating them; ZeroClaw changed history trimming from "trim to the cap" to "trim to a low-water target"; kimi-code dedicated work to CLI startup time and memory reduction.

Four platforms, unrelated, all doing the same thing in the same month: cutting context and startup overhead. That's token cost pressure conducting directly into architecture. And the MCP tool catalog is the deadest weight in the context — by our earlier measurement, ten servers are a standing burden of nearly 4,000 tokens, heavier the more ecosystems you plug in.

One layer deeper, there's a structural driver: the agent's capability radius is expanding. This week ZeroClaw made WhatsApp a first-class citizen (native polls, inline image previews, WhatsApp-dialect Markdown rendering); nanobot completed the full browser flow for Copilot device sign-in; Reasonix kept grinding the desktop deep end. The more external systems an agent touches, the more MCP servers hang off it — catalog bloat is the inevitable byproduct of capability expansion. Without dependency management and catalog elasticity, "connect more ecosystems" and "context explosion" are the same coin: take one, get both.

So the timing of Connectors makes sense. While every platform puts its context on a diet, MCP — the biggest fat deposit — goes first. And the diet has two halves that must happen together: shrink the volume (deferred/search modes) and verify the truth (dependency contracts, liveness probing). Volume alone, and the saved tokens get re-occupied by zombie stubs; truth alone, and the honest catalog is still huge. This week Hermes chose the second half; last week kimi-code's deferred disclosure walked the first. Both legs are moving.

---

## Three checks for your MCP config

You don't need to wait for Hermes's model to land on your desk. Audit your own MCP integration today with three questions.

**Is your config a process list or a dependency list?** If it holds only command/args/env and not one line answering "this depends on which application, at what version," your config isn't portable — the new-machine failure is coming; it's only a matter of when. A hand-written dependency comment per server beats nothing.

**When a server dies, does your agent know?** Is the tool catalog mounted once at startup, or does it track liveness? If the agent keeps conversing with a zombie's schema, it not only can't do the task — it keeps paying the bill we computed, ~73 tokens per zombie tool, present every turn. Health checks plus catalog sync are the two most valuable patches. And mind the volume: past five servers, deferred or search modes belong on your shortlist — 72–95% context savings is not a rounding error.

**When something fails, does the error state the cause?** "Connection failed" and "target application not running — start it first" are two different ops experiences. Borrow the resolver's locate/inspect/probe layering and your errors graduate from symptom to cause. Then make probing routine — not on incident, but on every connection attempt, with the catalog following the probe results. That's the full loop Hermes shipped.

Three checks later, you'll know which side of the gap you're on: managing a pile of processes, or a set of contracted dependencies. That gap is what one architecture restructuring demonstrated this week.

Where does this go next? Extrapolate the three threads: dependency contracts get standardized into common manifest fields; identity and tracing follow app/account targets into the protocol layer; token volume pushes deferred/search modes toward defaults. When all three mature, MCP finally grows from a protocol into an integration system — and nobody will remember we ever ran it with process configs.

*Based on the weekly submodule report and WeChat draft. Source: [Weekly Report](https://github.com/dz3ai/allclaws/blob/main/docs/reports/weekly/2026-09-22-submodule-weekly.md).*
