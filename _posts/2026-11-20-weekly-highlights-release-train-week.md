---
layout: post
title: "Weekly Highlights: The Release-Train Week (Nov 13–20, 2026)"
date: 2026-11-20 21:08:00 +0800
author: Danny Zeng
categories: [Weekly Update]
tags: [weekly-highlights, releases, openclaw, nanoclaw, zeroclaw, nanobot, goclaw, security, rustsec, gpt-6.2, codex]
---

October's monthly report named **cadence** as this ecosystem's operating doctrine. This week's window — **Nov 13–20**, across the eight projects our tracker watches — adds a sharper clause to that sentence: cadence has gone *multi-track*. The heavyweight no longer runs one release line; it runs three simultaneously, backporting to October while patching November stable while opening the next train's beta. And the rest of the cohort sorted itself into a familiar division of labor: those that ship on schedule, those that harden after shipping, and those that build without tagging at all.

## OpenClaw: seven tags, three lines, one week

**2,353 commits** landed on `main` in seven days — and the commit-type mix tells you where the effort went: **1,616 `fix`**, 143 `improve`, 139 `test`, 117 `perf`, 115 `feat`. This is a codebase in continuous-maintenance mode, and it produced **seven tagged releases** in the window: `v2026.11.5-beta.3`/`beta.4`, `v2026.11.4`, `v2026.11.5`, a `v2026.10.33` **backport on the October line**, `v2026.11.6`, and `v2026.11.10-beta.1` opening the next train — the last two on the same day.

The headline is `v2026.11.6` (Nov 19): **386 pull requests, 48 direct commits, 157 contributors** in a *patch* release. Its changelog reads like a post-incident review of everything around the agent loop:

- **Turn durability** — subagent and background turns survive configuration edits mid-flight; final answers still deliver when a Gateway restart interrupts sending; subagent results survive restarts *without replaying already-consumed results*; append-only provider history and exact Responses tool-argument bytes are preserved through long, tool-heavy Claude CLI turns. Distinguishing "delivery failed" from "already consumed successfully" is the kind of correctness that only shows up under restarts — the changelog credits it across multiple PRs.
- **Gateway weight** — startup memory pressure and resident memory reduced on constrained hosts, unused local credential runtimes deferred, plugin tool discovery no longer blocks the Gateway.
- **Release-train mechanics** — the 2026.11.5 updater bridges to the current release path; Git-release installs build and serve outside `node_modules`; Windows notifies after core readback. The 11.5 release notes themselves were restored and repaired mid-window — release engineering fixing its own release engineering.
- **ChatGPT alignment** — the numeric OpenClaw release is now sent as the ChatGPT version header, model catalogs are listed with the release version, and a new test catches lost GPT-6.2 prompt-cache reads.
- **Trust** — inline environment credentials redacted in configuration reads; SecretRef-backed skill API keys preserved instead of being flattened to plaintext; PostgreSQL upgrades halt before replacing a still-serving installation when its backup can't run.

Three parallel release lines is the real story: the October line got a backport, the November stable got two patches, and the next train got its first beta — *on the same day*. Cadence at this scale isn't speed anymore; it's lane discipline.

## NanoClaw: beta.3 → rc.3 in six days

The `v2026.11.0` train moved from `beta.3` (Nov 14) through `beta.4`, `rc.1`, `rc.2`, to `rc.3` (Nov 19) — final looks imminent. The 86 commits behind it are dominated by the add-codex/OneCLI surface, and one stands out for ecosystem relevance: **pinning Codex 0.169.0 "so ChatGPT logins can use GPT-6.2"** (`ab9551f0`).

That pin is the other half of a fact we hit independently in our benchmarking work: upstream Codex removed the chat wire API in a hard February-2026 cutoff, so clients that speak ChatGPT OAuth have to hold the last version that still accepts it. NanoClaw's workaround is thorough — sign-in runs via the pinned CLI through `pnpm dlx` outside `/tmp`, the Codex AGENTS.md cap is raised to 64 KiB, and built-in image generation works behind OneCLI. Around it: setup steps now end only once their raw log is written, linger is verified without interactive polkit prompts, the agent-runner never blocks on or follows links in Claude's `settings.json`, and recurring mailbox series keep exactly one task payload per run.

## ZeroClaw: the security week

Twenty-one commits, zero tags — the week after `v0.9.0` was a hardening sweep with a distinctly Rust flavor: **six RustSec advisory patches** (heapless, Wasmtime, SMTP via a bounded base64 duplicate, zip for RUSTSEC-2026-0548 with chrono's maintenance advisories accepted, quinn-udp for RUSTSEC-2026-0538).

The more interesting half is confinement work: MCP SSE endpoints and their redirects are confined to the server origin; per-connection task records are kept out of INFO traces; forwarded loopback is treated as non-local for SOP cancellation; paired WebSocket credentials moved out of URLs; the Scalar docs bundle is pinned with Subresource Integrity. Access control tightened too — read access is now required before uploads and edits, and SOP decisions fail closed when their answers are unusable. Two features landed quietly in the same sweep: POSIX commands are read in bash's own grammar when bash runs them, and Anthropic requests now send `output_config.effort`.

## NanoBot: a hundred commits, no tag

Still rolling after `v0.4.1` (Nov 6), NanoBot spent the window on its webui: composer palettes for slash, skills, and mentions; the goal island redesigned as a "floating vibrancy platter"; reconnect semantics rebuilt so running turns reconcile on reconnect and queued messages show when the agent picks them up. The commit we'd single out is quieter: **malformed hostnames are rejected before DNS resolution** — validation moved to the earliest possible point, which is where it belongs. Session user images now replay from stored attachments, and gateway mutations were separated from UI state — the same data/control separation OpenClaw's transcript refactor is performing on its side.

## GoClaw and the quiet three

GoClaw ticked `beta.247` → `beta.250` with five accounting-grade fixes: Ollama tool schemas keep their enum/items/nested shape and `[]any` required fields; Gemini thinking tokens count in native media usage; Claude CLI cache tokens count in context usage; cron rejects overlapping manual runs and honors `due` mode in both the PG and SQLite stores. Small, unglamorous, exactly what a mature beta train looks like.

IronClaw (head since Sep 29), ClawTeam (Nov 7), and MaxClaw (June 13) stayed dormant.

## The thread underneath: GPT-6.2 alignment

Read the two busiest projects together and one upstream event explains both: OpenClaw refreshing ChatGPT model lists, version headers, and GPT-6.2 cache tests while NanoClaw pins Codex 0.169.0 for ChatGPT logins. When the ecosystem's largest project and a fast-moving smaller one converge on the same external release wave from opposite directions, that's not coincidence — it's dependency gravity. Expect the next few weekly windows to show the rest of the cohort absorbing the same wave, each in its own idiom.

---

*[中文版](/allclaws/blog/2026/11/20/weekly-highlights-release-train-week-zh/)*

*Data: [weekly submodule digest 2026-11-20](https://github.com/dz3ai/allclaws/blob/main/docs/reports/weekly/2026-11-20-submodule-weekly.md) and per-project reports in [docs/reports](https://github.com/dz3ai/allclaws/tree/main/docs/reports). Window Nov 13–20, 2026; 8 tracked projects.*
