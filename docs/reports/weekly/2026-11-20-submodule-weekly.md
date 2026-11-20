# Weekly Submodule Report — 2026-11-20

**Scope:** the 8 projects tracked by `scripts/track-agent-updates.sh` (`openclaw`, `nanoclaw`, `ironclaw`, `goclaw`, `zeroclaw`, `nanobot`, `clawteam`, `maxclaw`). The branch map in `docs/reports/submodule-branch-map.json` covers all 29 submodules; the other 21 are not part of this run.

**Window:** 2026-11-13 → 2026-11-20 (7 days).

**Data source:** `./scripts/track-agent-updates.sh --since "2026-11-13"`, fetching each project's mapped **active line** (not the default branch). Per-project detail: `docs/reports/<project>_2026-11.md`. All 8 fetches went clean over SSH (global `url."git@github.com:".insteadOf` rewrite in effect) — no ref corrections needed this week, unlike the Nov 13 run.

## Summary

| Project | Active line | Commits (7d) | Releases in window | Status |
|---|---|---:|---|---|
| OpenClaw | `main` | 2,353 | **7 tags**: `v2026.11.5-beta.3/.4`, `v2026.11.4`, `v2026.11.5`, `v2026.10.33` (Oct-line backport), `v2026.11.6`, `v2026.11.10-beta.1` | active |
| NanoBot | `main` | 100 | — (latest `v0.4.1`, 11-06) | active |
| NanoClaw | `main` | 86 | `v2026.11.0-beta.3/.4`, **`rc.1`/`rc.2`/`rc.3`** (11-14 → 11-19) | active |
| ZeroClaw | `master` | 21 | — (`v0.9.0` landed 11-11, just before the window) | active |
| GoClaw | `dev` | 5 | `v3.15.0-beta.247` → `.250` (11-13 → 11-19) | active |
| IronClaw | `release/2026-08-26` | 0 | — (head still 09-29) | dormant |
| ClawTeam | `main` | 0 | — (head 11-07) | dormant |
| MaxClaw | `main` | 0 | — (head 06-13) | dormant |

**Verdict:** OpenClaw ran a full release train in one week — seven tags including two stable patches (`v2026.11.5`, `v2026.11.6`), a backport on the October line (`v2026.10.33`), and the first beta of the next train (`v2026.11.10-beta.1`). NanoClaw's `v2026.11.0` went beta.3 → rc.3 in six days; final looks imminent. ZeroClaw spent the week after `v0.9.0` on a security-hardening sweep (six RustSec advisory patches plus MCP/web confinement fixes). NanoBot shipped a WebUI sprint with no tag. GoClaw ticked four more betas. The dormant three stayed dormant.

## OpenClaw — `main` (2,353 commits, 7 tags)

Volume held monorepo scale. Commit mix leans hard into fixes: 1,616 `fix` / 143 `improve` / 139 `test` / 117 `perf` / 115 `feat` / 70 `refactor`.

`v2026.11.6` (11-19) is the headline — **386 PRs, 48 direct commits, 157 contributors** per its changelog. Dominant themes:

- **Release-train mechanics:** the 2026.11.5 updater bridges to the current release path; Git-release installs build and serve outside `node_modules` and keep legacy Git services on their release launcher; Windows notifies after core readback. The 11.5 release notes themselves were restored and repaired mid-window.
- **Gateway resilience:** startup memory pressure and resident memory reduced on constrained hosts; unused local credential runtimes deferred; plugin tool discovery no longer blocks the Gateway; session cgroups retired when idle.
- **Turn durability:** subagent and background turns survive configuration edits; final answers deliver when a Gateway restart interrupts sending; subagent results survive Gateway restarts without replaying consumed results; append-only provider history and exact Responses tool-argument bytes preserved through long, tool-heavy Claude CLI turns.
- **ChatGPT/Codex alignment:** Sign-in-with-ChatGPT label refresh, bundled Codex support updated for newer ChatGPT models, the numeric OpenClaw release sent as the ChatGPT version header, and a test catching lost GPT-6.2 prompt-cache reads.
- **Security/robustness:** inline environment credentials redacted in configuration reads; SecretRef-backed skill API keys preserved; malformed UTF-8 config sources preserved on write; PostgreSQL upgrade halts before replacing a still-serving install when its backup can't run; large file reads stop after the requested text page.

The `v2026.11.10-beta.1` tag (same day as `.6`) opens the next train — the version jump suggests the calendar-versioned cadence is compressing further. `v2026.10.33` backports fixes to the October line, i.e. three release lines are being maintained in parallel right now.

## NanoClaw — `main` (86 commits, 5 tags)

The `v2026.11.0` release train: `beta.3` (11-14) → `beta.4` (11-16) → `rc.1` (11-17) → `rc.2` (11-18) → `rc.3` (11-19). Window themes:

- **add-codex / OneCLI hardening:** sign in via the pinned Codex CLI through `pnpm dlx` outside `/tmp`; **pin Codex 0.169.0 so ChatGPT logins can use GPT-6.2** (`ab9551f0`); raise the Codex AGENTS.md cap to 64 KiB; built-in image generation works behind OneCLI; block `~/.onecli` mounts and refuse masked database-password changes.
- **Setup robustness:** a setup step ends only once its raw log is written; linger verified without interactive polkit prompts; provider image rebuild visible in the progress window.
- **Agent-runner:** never block or follow links on the Claude `settings.json`; typecheck with the pinned Bun when the host has none; CLI entry points run from checkouts with spaces or symlinks.
- **Fixes:** one task payload per recurring mailbox series; extra mounts of driver-protected paths rejected.

The Codex 0.169 pin matches what our benchmark tier found from the other side — ≥0.169 removed the chat wire API, so NanoClaw is pinning the last version that still accepts ChatGPT OAuth for its add-codex flow.

## NanoBot — `main` (100 commits, no tag)

A WebUI sprint week, still rolling after `v0.4.1` (11-06):

- **Composer and palettes:** slash/skill/mention palettes refined; goal island redesigned as a "floating vibrancy platter"; custom reasoning-effort picker themed.
- **Reconnect semantics:** running turns reconciled on reconnect; queued messages use live turns and show when the agent picks them up; keyboard focus restored after pointer use; focus indicators gated on keyboard modality.
- **Security/session:** malformed hostnames rejected **before DNS resolution** (`085521823`); user images replayed from stored attachments; response inputs identified on model request start; side-channel command replies keep their routing.
- Refactors: gateway mutations separated from UI state; unreachable code and redundant tests removed; user docs cleaned of internal technical detail.

## ZeroClaw — `master` (21 commits, no tag)

Post-`v0.9.0` stabilization with a distinct security flavor:

- **RustSec sweep:** heapless + Wasmtime advisories patched; SMTP advisories patched with a bounded base64 duplicate; zip updated for RUSTSEC-2026-0548 (chrono maintenance advisories accepted); quinn-udp bumped for RUSTSEC-2026-0538.
- **Confinement:** MCP SSE endpoints and redirects confined to the server origin; per-connection task records kept out of INFO traces; forwarded loopback treated as non-local for SOP cancel; paired WebSocket credentials kept out of URLs; Scalar docs bundle pinned with Subresource Integrity.
- **Access control:** read access required before uploads and edits; headless SOP step scope inherited on peer-send turns; fail-closed mode when SOP decision answers are unusable.
- **Features:** POSIX commands read in bash's grammar when bash runs them (`dfe8ab35b`); Anthropic `output_config.effort` sent on requests.
- **Windows:** prebuilt installer checksums verified; the Windows installer read when the guide is rendered.

## GoClaw — `dev` (5 commits, 4 betas)

`v3.15.0-beta.247` → `.250` (11-13 → 11-19), all provider/tooling accounting fixes: Ollama tool schemas keep enum/items/nested shape and `[]any` required fields; Gemini thinking tokens counted in native media usage; Claude CLI cache tokens counted in context usage; cron rejects overlapping manual runs in SQLite and honors `due` run mode in the PG and SQLite stores.

## Dormant

- **IronClaw** — `release/2026-08-26`, head unchanged since 09-29; latest tag `v0.21.0` (03-20).
- **ClawTeam** — `main`, head 11-07; latest tag `v0.3.0+openclaw2` (07-04).
- **MaxClaw** — `main`, head 06-13; latest tag `v0.1.2` (03-18).

## Cross-project notes

- **GPT-6.2 + Codex 0.169 alignment:** OpenClaw refreshed ChatGPT model lists and GPT-6.2 cache tests while NanoClaw pinned Codex 0.169.0 for ChatGPT logins — both projects are tracking the same upstream OpenAI release wave. NanoClaw's pin corroborates the hard Feb-2026 chat-wire removal our benchmark tier hit with the codex driver.
- **Three parallel OpenClaw release lines** (October backport line, current 11.x stable, next-train beta) plus a 7-tag week — release cadence is the story for the ecosystem's largest project.
- **Security-week pattern:** ZeroClaw's RustSec sweep and NanoBot's pre-DNS hostname validation are the two standout hardening commits of the week.
