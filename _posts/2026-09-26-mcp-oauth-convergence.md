---
layout: post
title: "Three Threads, One Standard: MCP's Authorization Lifecycle Has Converged"
date: 2026-09-26 10:20:00 +0800
author: Danny Zeng
categories: [Ecosystem Analysis]
tags: [mcp, oauth, sep-2207, kimi-code, hermes-agent, codex, standardization, architecture]
---

There's an unremarkable changeset in the kimi-code repository, one sentence long: "Fix MCP OAuth not requesting the offline_access scope, which caused hourly browser re-authorization with providers like Vercel."

Hourly login prompts. Picture the experience: you configure an MCP server for your agent, authorization succeeds, everything works — and then, every hour, the browser pops up on schedule demanding authorization again. Nobody did anything wrong: the client never requested a refresh token, the authorization server followed OIDC convention and didn't issue one, the access token expired, and the cycle restarted from zero. This is not a bug. It's the combined output of three components failing to talk to each other.

The changeset corresponds to kimi-code commit [#3979](https://github.com/MoonshotAI/kimi-code/pull/3979) (landed 09-22), which we mentioned in passing as the "third thread" in the first post of this series. This post takes it apart — because taken apart, it turns out not to be an isolated thread but **the junction point where three threads converge**. The MCP productization series covered three: dependency contracts (Hermes), identity and audit (Codex), authorization lifecycle (kimi-code). The threads looked independent. Put #3979 under the spotlight and you see the convergence has already happened — not as a forecast, but as a sequence of dated facts.

*This is the third and final post in the MCP productization series.* *[中文版](/allclaws/blog/2026/09/26/mcp-oauth-convergence-zh/)*

---

## Where the three threads stand

Align the progress bars first.

**Thread one, dependency contracts.** Hermes's Connectors trilogy promoted the MCP server from "process configuration" to an "application-dependency object": manifest-declared dependencies, install-time refusal on incompatible hosts, continuous endpoint probing. Solving: "are the tools there?"

**Thread two, identity and audit.** Codex's app-server v2 added explicit app/account targets to MCP requests, an attribution ledger that survives compaction, and trace context that crosses transport queues. Solving: "whose account does this debit, and can it be traced?"

**Thread three, authorization lifecycle.** kimi-code's offline_access and 401-to-needs-auth degradation. Solving: "when the token expires, is the tool chain still alive?"

Of the three, the first two still carry strong platform-private coloring: Hermes's manifest is its own format; Codex's targets and attribution live in its own protocol extensions. Only the third thread, halfway along its path, ran into a public standard that already existed. This post's through-line is that collision — and the standardization path it reveals for the whole ecosystem.

---

## The standard was already waiting: SEP-2207

The problem in that kimi-code commit has a formal name in the MCP repository: **SEP-2207, "OIDC-Flavored Refresh Token Guidance"**, initiated 2026-02-04, status Final. It attacks exactly the "hourly login" problem from our opening, and dissects it more thoroughly.

The background: MCP's authorization builds on OAuth 2.1, but real-world authorization servers mostly implement OIDC as well. The two treat refresh tokens differently in a subtle way: in pure OAuth 2.1, **there is no standard mechanism for a client to explicitly request a refresh token** — the server issues one or not, per its own policies. OIDC convention, by contrast, has the client attach the `offline_access` scope to mean "I want a long-lived credential." The difference is harmless until it produces three ecosystem-level problems, which the SEP counts precisely:

**One, the big clients aren't asking.** Major MCP clients — Cursor, Claude, VS Code — never explicitly request refresh tokens, because they don't know whether the authorization server on the other end supports, expects, or requires the scope. Every client guesses; a wrong guess bills the user one login per hour.

**Two, resource servers shouldn't speak for clients.** `offline_access` is not a permission any resource needs; it's a matter between the client and the authorization server. So an MCP server including it in the 401's `WWW-Authenticate` header or in Protected Resource Metadata's `scopes_supported` is semantically wrong — a resource never needs "long-term access." That's the client's wish.

**Three, server behavior is inconsistent.** For the same authorization-code request, different servers differ on whether and when they issue refresh tokens.

SEP-2207's remedy is almost naively simple, but every MUST/SHOULD sits in an exact spot:

**Clients** that intend to use refresh tokens and can store them securely SHOULD declare `refresh_token` in their `grant_types` client metadata; MAY append `offline_access` to the requested scopes when the authorization server's `scopes_supported` advertises it; and MUST NOT assume that requesting guarantees issuance — the server keeps discretion.

**Servers** (acting as OAuth protected resources) SHOULD NOT include `offline_access` in `WWW-Authenticate` or resource metadata — for the reason above: it's not the resource's wish.

And it's in the formal specification: the 2026-07-28 MCP spec's Authorization chapter carries a complete Refresh Tokens section, word-for-word consistent with the SEP. Reference implementations landed in the official SDKs — the TypeScript SDK PR merged March 30, Python SDK followed April 14, both with a client-conformance test to validate implementations.

---

## The landing: how kimi-code implements the SEP

Back to the September 22 commit. Reading its diff, you find a textbook "implement the standard."

The core is a `resolveRequestScope` method in three steps. Step one, **discover** — obtain the authorization server's metadata via the MCP SDK's `discoverOAuthServerInfo` and cache it. Step two, **check the table** — look for `offline_access` in the metadata's `scopes_supported`; if absent, add nothing (the server didn't advertise, so the client doesn't shove — exactly the precondition of the SEP's MAY branch). Step three, **idempotent append** — join `offline_access` onto the base scopes, but only after checking it isn't already there.

Every step maps to a sentence of the SEP — no more, no less. The most instructive branch is the "don't add" one: if the server never advertised `offline_access`, kimi-code keeps the request as-is rather than "giving it a try." That restraint is what a standard is worth — it replaces "every client guesses" with "everyone reads the same table."

kimi-code's lifecycle work doesn't stop there. September 17's #3846 handles the runtime half: when an MCP tool call returns 401, the server flips to needs-auth, invalidates rejected tokens, distinguishes "fresh concurrent grants" from "freshly rejected ones" inside concurrent authorization windows — even future timestamps older than the scheduler's clock got their own fix. If `offline_access` is "how to extend a token's life," that cluster is "how the system finds out gracefully the moment a token dies, and recovers." One plus, one minus: a complete lifecycle.

One overlooked detail: kimi-code's MCP OAuth is built directly on the official `@modelcontextprotocol/sdk` — the same SDK that shipped the SEP-2207 reference implementation in March. The platform didn't invent authorization logic in a vacuum; it **stood on the standard's reference implementation and built its own runtime above it** (its proactive refresh, scheduler, and concurrent-grant windows are private layers on top of the SDK). The layering of standardization becomes visible: the spec governs interfaces, the official SDKs govern shared implementation, platforms govern their own increments.

---

## The convergence: a standardization pipeline in full working order

Lay the timeline out and you see a rare thing — a standardization pipeline running end to end:

**2026-02-04** — an ecosystem pain point is chartered as a SEP ("major clients are prompting logins hourly")
**2026-03-30 / 04-14** — official SDKs ship reference implementations and a conformance test
**2026-07-28** — the text enters the specification as a formal requirement
**2026-09-22** — a platform lands it (kimi-code), fixing its own users' real pain

Pain point to standard: under two months. Standard to head-platform production: under three. Backed the whole way by three artifacts — spec text, SDK code, conformance tests. This is neither "one big vendor invents and shoves," nor "every platform plays alone forever." It's open infrastructure at its ideal cadence: **standardize the problem first, follow with implementations, let the platforms benefit last.**

The contrast with the first two threads is telling. Hermes's dependency contracts and Codex's identity/audit designs are still platform-private — no SEP, no cross-platform fields, no conformance tests. The authorization thread got here first not because it matters most, but because its problem is the oldest: the community has stepped in OAuth's potholes for twenty years; `offline_access`'s semantics were written down in OIDC long ago. MCP's job was just to inherit them and draw the resource/client boundary. Problems on mature soil standardize fast; problems on new land need a few more harvests.

But the direction is visible. Across all three threads, the same skeleton keeps appearing inside private implementations — declaration (Hermes's manifest fields / Codex's protocol capabilities / kimi's scope negotiation), probing (kimi's metadata discovery / Hermes's endpoint probe), lifecycle (token renewal / application liveness / authorization revocation). A skeleton that repeats across platforms is the raw material of the next SEP. When Hermes promotes dependency declaration into a common manifest field, and Codex brings app/account targets to the standards table — those are the two moves to watch.

A closing footnote closes the loop: Codex's trace-context commit has integration tests explicitly marked as covering the `2026-07-28` protocol mode — the same spec version that gained the refresh-token section. Platforms have started labeling their behavior with "which spec version I'm compatible with." That, too, is evidence of convergence.

---

## What you should do now that the standard exists

**If your product contains an MCP client**: audit your OAuth — do you declare the `refresh_token` grant type? Do you append `offline_access` when the server's `scopes_supported` advertises it? Do you assume requesting guarantees issuance? Walk through the spec's Refresh Tokens section and your users stop logging in hourly.

**If your product contains an MCP server**: check two things — `offline_access` must not appear in your `WWW-Authenticate` or Protected Resource Metadata (it's not your scope); and your 401/403 responses should carry `WWW-Authenticate` with scope hints per the spec. A resource server's job is to state what it needs, not to demand long-lived credentials on the client's behalf.

**If you build a platform**: check whether your problem has a SEP. If yes, implement the standard before stacking private layers (the kimi-code route: official SDK as the base, private increments above). If no — and your pain point is common enough — you're writing this ecosystem's next SEP. Extract the shared skeleton from your private design and propose it upward (Codex's capability declaration and Hermes's dependency manifest are ready-made candidates).

Three posts in, the series compresses to one sentence: **MCP is turning from a protocol into an integration system, and every pillar of that system — contracts, identity, audit, authorization — walks the same road: private implementations hit a shared pain point, the pain point grows a SEP, the SEP lands in SDKs, the SDKs grow back into platforms.** The authorization thread has completed the full circuit. The other pillars are on their way. The day all four pillars have their own SEP, MCP integration is truly standardized — and stories like "prompted to log in every hour" will look as distant as a frontend project without a package.json looks today.

---

*[中文版](/allclaws/blog/2026/09/26/mcp-oauth-convergence-zh/)*

*Based on the weekly submodule report and WeChat draft. Sources: [SEP-2207](https://modelcontextprotocol.io/seps/2207-oidc-refresh-token-guidance), [MCP spec 2026-07-28 Authorization](https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization), [Weekly Report 2026-09-22](https://github.com/dz3ai/allclaws/blob/main/docs/reports/weekly/2026-09-22-submodule-weekly.md).*
