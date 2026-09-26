---
layout: post
title: "One Agent, Ten Accounts: Codex Treats MCP as a Multi-Tenant Protocol"
date: 2026-09-26 09:30:00 +0800
author: Danny Zeng
categories: [Ecosystem Analysis]
tags: [mcp, codex, hermes-agent, kimi-code, multi-tenancy, audit, trace-context, oauth, architecture]
---

Last week's post argued that Hermes-Agent answered MCP's oldest question — *why do servers keep dying silently?* — by promoting the MCP server from "process configuration" to an application-dependency object: installation is decided by a declared dependency contract, liveness by the application's state, and failures come with stated causes. That route fixes the single-machine user's pain.

But the productization of MCP has another half. Picture a different deployment: the agent isn't sitting on your desktop — it runs as a *service*. An IDE integrates it. A desktop app integrates it. Cloud plugins integrate it. Behind it hangs a fleet of MCP servers, each connected to different applications and different accounts. Now the questions change. Not "does this tool work?" but:

**Whose account did that resource read touch? Whose ledger does that tool call land in? When something breaks, can you follow one step of agent behavior down to the exact downstream HTTP request?**

Three questions, one sentence: MCP requests have started to need identity. This week **Codex** (OpenAI) shipped a cluster of changes that answer them one by one — 409 commits over seven days on main, app-server v2 in continuous evolution, rust-v0.155.1 released 09-18.

*This is the second post in a short series on MCP productization. The first covered the Hermes route — MCP as an application-dependency problem. The next follows the third thread: authorization lifecycle, and where the routes converge.*

---

## First question: whose resource is this read touching?

Codex added an explicit `target` field to the `mcpServer/resource/read` protocol ([#47248](https://github.com/openai/codex/pull/47248)): `{connectorId, linkId}`. Unpacked, every field answers an identity question.

`connectorId` says *which application*. `linkId` says *which account* — pass a string and the read selects a specific authorized account; pass `null` and the semantics become "no-auth access," allowed or refused at the backend's discretion. In other words, **a resource read must now state, at the protocol level, which application and which account it acts as.**

The design is notably restrained. Direct targets are restricted to `codex_apps` hosted applications; empty connector IDs, empty link IDs, and synthetic link IDs are rejected outright. Supply `originCallId` and `threadId` and the request preserves the originating app/account scope — whoever initiated the call, the identity follows them. Omit `target` entirely and everything works exactly as before, through the discovery flow. The protocol grew a dimension without breaking a single old call.

That `linkId` deserves a sentence of its own. Before it existed, an MCP resource read implicitly meant "whatever identity this connection was configured with" — single-tenant thinking by default. When one connector can carry multiple accounts, plus an explicit "this time, no authorization," the MCP request gains **account granularity** for the first time. That is the foundation multi-tenancy is built on.

---

## Second question: who actually did this?

The second question is subtler and more dangerous: **audit**. An agent makes a dozen MCP calls in one session; afterwards you need to answer "who initiated this, through which connector" — and discover the session has long since been compacted. History was trimmed, rewritten, forked; the ledger has been recopied several times. Where did the original record go?

Codex's answer is a ledger that compaction cannot erase ([#47081](https://github.com/openai/codex/pull/47081)). Every MCP call — direct ones, Code Mode ones, ones that returned errors, ones whose results were never printed — records its source and its first turn, with connector and plugin identifiers attached. The crucial part: attributions are **persisted as checkpoints and restored across compaction, resume, and forks**, including forks limited to recent turns. Torture the session however you like; the accounts survive.

Then comes the purpose of the ledger. Attribution attaches to Responses API requests as `mcp_attribution` inside `client_metadata` — note the placement: **outside model-visible content**. That choice is deliberate. Audit data exists for the cloud and the operator, not for the context window; the model should neither be polluted by its own bookkeeping nor get to *see* that it's being recorded. Transmission is restricted to allowlisted OpenAI HTTPS destinations, and legacy history without checkpoints, malformed or conflicting attribution, and serialized attribution over 16 KiB all fail loudly with `attribution_error` instead of being swallowed.

A complete audit design must answer four things: what to record, what it survives with, who receives it, and what happens when it breaks. Codex filled in all four boxes.

---

## Third question: when it breaks, can you trace it?

The third problem is traceability, and it loses in an unglamorous place: the queue.

app-server's MCP requests pass through background transport queues. An HTTP request leaves its caller, waits in line, and goes out — and W3C trace context doesn't queue on its own. The outbound request and the originating call end up as two orphaned spans, neither recognizing the other. However complete your monitoring, one broken link in the queue turns troubleshooting into archaeology.

[#47212](https://github.com/openai/codex/pull/47212) is the link-splicer: capture W3C trace context explicitly in request metadata (tool and resource operations, custom requests, event streams alike), then restore it at the HTTP POST site inside an `mcp.http.request` span, so the outbound trace explicitly hangs off the originating request. Application metadata is preserved while trace fields are replaced with the current caller's context and stale `tracestate` is dropped. Integration tests cover both the legacy and `2026-07-28` protocol modes.

Read the three answers together and Codex's first-order question comes into focus. It is not "are the tools many?" or "do servers die quietly?" — it is: **when one agent serves multiple applications, multiple accounts, and multiple concurrent sessions, every request's ownership and provenance must remain answerable end to end.** This is MCP treated as infrastructure, and infrastructure's first virtue isn't feature count — it's that every transaction can be attributed and audited.

---

## The supporting cast: making identity actually usable

Protocol fields alone don't make an identity system. Three companion changes landed this week.

**Subagents can now request user input** ([#46877](https://github.com/openai/codex/pull/46877)). MCP requests that needed user interaction used to fail outright in subagents with guidance to "ask the parent agent" — browser sign-in, form input, interactive tool approval: all dead ends in a child thread. The root-only guard is gone; subagents now surface prompts and wait for responses under the existing approval policy and automatic review rules. Why does this belong in a multi-tenancy story? Because **multi-agent is the prelude to multi-tenant**: an identity system first has to distinguish *which agent* before it can distinguish *which account*.

**Explicit gateway OAuth sign-in** ([#47207](https://github.com/openai/codex/pull/47207)). Clients with a sign-in UI can now declare the `explicitGatewayOauth` capability and decide for themselves when browser authorization begins and whether credentials are ready before the first authenticated request. The authorization URL goes only to the initiating connection; the login cancels on disconnect; later connections cannot undo the opt-in. One sentence: **the right to initiate authorization moves from the framework to the client** — which is multi-tenancy's daily bread, since when the login prompt appears is the tenant's business, not the platform's.

**MCP server status exposes its HTTP origin** ([#47159](https://github.com/openai/codex/pull/47159)). `McpServerStatus` gained a nullable `httpOrigin` derived from the effective endpoint — origin only, with credentials, path, query, and fragment stripped; `null` for stdio transports. "Which domain does this tool actually talk to" becomes a field a security audit can read directly, instead of a URL a human digs out of a config file.

---

## Two routes, one complete picture

Put last week's post next to this one and the two routes align cleanly.

**Hermes, the application-dependency route.** Metaphor: the MCP server is a dependency of an application, package.json-style. Mechanisms: manifest-declared dependencies, install-time refusal, continuous endpoint probing, catalog elasticity. What it fixes: the single-machine user's "won't install, dies silently, can't explain why."

**Codex, the multi-tenant protocol route.** Metaphor: MCP is a multi-tenant protocol; every request carries identity, a ledger entry, and a provenance chain. Mechanisms: resource reads with app/account targets, cumulative attribution persisted across compaction, W3C trace context preserved across queues. What it fixes: request ownership, audit, and traceability when one agent serves many applications and accounts.

The routes don't compete — they aren't even on the same layer. Hermes owns **local reliability**: when the tool layer is available. Codex owns **server-side correctness**: whose account every request debits. One is the engineering of the hand; the other, the engineering of the ledger. A complete MCP integration system will eventually need both.

Why did each pick a different half? Look at the shape of the product. Hermes's home turf is the personal desktop agent, where the pain is "the server on *my* machine died again." Codex's app-server is a *service* — integrated by IDEs, desktop apps, and cloud plugins, multi-tenant by nature. When your agent runtime is infrastructure, "whose request is this" isn't an advanced requirement; it's something you settle in the first line of code.

---

## Why now

None of this landed in a vacuum. Two signals in the same weekly report paved the way.

First, the agent's own shape is evolving. Codex landed its AgentControl abstraction this week — `LocalAgentControl` centralizing agent resume, multi-agent spawning unified through SpawnRequest, agent snapshots returned from close_agent and streamed by subscription. Multi-agent lifecycle is converging on a single control plane, which means **more agents running concurrently**, each issuing MCP requests — without ownership and audit, more agents is just more confusion. The Guardian self-review system also flipped to default-on (#47275); self-review is only meaningful when "who did this" is answerable.

Second, the industry echoed on the authorization axis: kimi-code added `offline_access` to its MCP OAuth requests (#3979) — "the token expired; can the server still work?" is part of the same lifecycle problem. Stacked on the two routes from the previous post, the picture sharpens: **MCP integration is evolving from "mount at process launch" into a full integration system — with dependency contracts, with identity, with audit, with OAuth lifecycle.** Four pillars; this week you can watch one vendor laying the contract and another laying identity, audit, and authorization.

---

## Three questions for your MCP integration

You don't need to wait for protocol standardization. Audit your own integration today.

**Can every tool call be attributed to an explicit identity?** In your integration, is "which connector, which account" an explicit field — or an implicit default buried in initialization config? If multiple accounts share one connection, account-granularity targets deserve a place on your roadmap; `{connectorId, linkId}` is the syntax the protocol has already shown you.

**Do call records survive compaction, resume, and forks?** Long sessions get compacted — when history is rewritten, does your MCP call ledger get rewritten with it, or does it persist independently? Codex's approach is worth copying: attribution as checkpoints, restored across compaction/resume/fork. The first property of audit data is that it **survives the recopied ledger**.

**When something breaks, can one step of agent behavior be joined to the downstream HTTP request?** Any architecture with queues, async boundaries, or transport workers will not carry trace context across by itself. Check your chain: does the outbound trace explicitly link back to its caller? One broken link, and observability is interior decoration.

Three "can't say" answers, and your MCP integration is still in the process-config era — it runs, but it won't survive an audit. That's the future both head platforms pointed at with this week's two restructurings: MCP won't stay a protocol; it's growing into an integration system with contracts, identity, and ledgers. And when it arrives, an agent that can't answer "who sent this call" will be like a frontend project without a package.json today — not unable to live, but untouchable.

---

*Based on the weekly submodule report and WeChat draft. Source: [Weekly Report](https://github.com/dz3ai/allclaws/blob/main/docs/reports/weekly/2026-09-22-submodule-weekly.md).*
