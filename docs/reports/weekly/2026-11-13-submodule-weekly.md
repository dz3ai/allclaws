# Weekly Submodule Report — 2026-11-13

**Scope:** the 8 projects tracked by `scripts/track-agent-updates.sh` (`openclaw`, `nanoclaw`, `ironclaw`, `goclaw`, `zeroclaw`, `nanobot`, `clawteam`, `maxclaw`). The branch map in `docs/reports/submodule-branch-map.json` covers all 29 submodules; the other 21 are not part of this run.

**Window:** 2026-11-02 → 2026-11-13 (11 days).

**Data source:** `./scripts/track-agent-updates.sh --since "2026-11-02"`, fetching each project's mapped **active line** (not the default branch). Per-project detail: `docs/reports/<project>_2026-11.md`. OpenClaw fetched via SSH (HTTPS to GitHub blocked again — persistent global `url."git@github.com:".insteadOf "https://github.com/"` rewrite in effect). OpenClaw's blobless shallow clone ref was corrected during fetch (the Nov 12 fetch produced `origin/main` at `8ae9d35bd53`; local HEAD remains at the Nov 2 pin `395a8c13b04` pending the next full sync).

## Summary

| Project | Active line | Commits (11d) | Releases in window | Status |
|---|---|---:|---|---|
| OpenClaw | `main` | 4,019 | — (latest `v2026.10.10-beta.5`, 10-29; 2026.11.4 perf waiver landed) | active |
| NanoBot | `main` | 100+ | `v0.4.1` (11-06) | active |
| ZeroClaw | `master` | 100+ | `v0.9.0` (11-11) | active |
| NanoClaw | `main` | 20+ | `v2026.11.0-beta.1` (11-09), `beta.2` (11-12) | active |
| GoClaw | `dev` | 16 | `v3.15.0-beta.242` → `.246` (11-09 → 11-13) | active |
| IronClaw | `release/*` | 0 | — (latest `v0.21.0`, 03-20) | dormant |
| ClawTeam | `main` | 13 | — (latest `v0.3.0+openclaw2`, 07-04) | dormant |
| MaxClaw | `main` | 0 | — (latest `v0.1.2`, 03-18) | dormant |

**Verdict:** a release-heavy week — every active project shipped at least one tag. The headline is ZeroClaw's major `v0.9.0` (first since `v0.8.7` on Oct 27, a 15-day gap) with a massive docs overhaul and OIDC pairing-free login; NanoBot's `v0.4.1` patch closes the `v0.4.0` gap in 16 days; NanoClaw's beta train continues (`beta.1` → `beta.2`); GoClaw ran 5 rapid betas (`.242` → `.246`). OpenClaw moved monorepo-scale (4,019 commits) without a new tagged release — the 2026.11.4 performance waiver is the main landing. ClawTeam's only activity was a Bilibili-link docs update.

## OpenClaw — `main` (4,019 commits)

Volume remains monorepo-scale. The tail of the window is dominated by UI polish, Telegram fixes, and the 2026.11.4 performance waiver rollout:

- `8ae9d35b` chore(ui): refresh control ui locales (#198280)
- `68a839b9` fix: isolate held agent databases until explicit restoration (#198180)
- `b9f1e62e` test(release): remove waiver regression coverage (#198274)
- `514a224c` fix(release): apply 2026.11.4 performance waiver release-wide (#198271)
- `9b114651` feat(ui): switch command palette between Search and Compose (#186059)
- `eb1a592f` fix(ui): chat cost popover hides the session's total spend (#198261)
- `69a232ff` fix(telegram): keep callback controls when replacement delivery fails (#193948)
- `da0e0ba8` fix(update): roll back activated releases that fail Doctor or Gateway startup (#197851)

Key themes: Telegram reliability (inline buttons, widget routing, callback controls, /commands fix), UI command palette rework, database isolation hardening, and the performance waiver that landed across the entire fleet. OpenClaw ID sign-in continues to roll out (`feat(openclaw-id): sign in with OpenClaw ID over a verified personal sign-in` #197559, `#197628`).

No new release tag in the window. Latest tagged release remains `v2026.10.10-beta.5` (2026-10-29).

## NanoBot — `main` (100+ commits)

The `v0.4.1` patch landed on Nov 6, with extensive webui, subagent, and documentation work through the window:

- `3f65a8f8` fix(models): route image input by preset capability (#6651)
- `6a24b176` feat(webui): refresh the empty chat welcome (#6650)
- `90d69e7a` refactor(exec): share the sandbox launch path with settings checks (#6645)
- `0f5e56ed` refactor(execution): share bounded HTTP redirects (#6637)
- `eb8546c3` perf(subagent): read saved task history by loaded turns (#6634)
- `e6b23c73` feat(webui): show the full token-usage picture in settings (#6638)
- `e6b0aec2` refactor(sessions)!: retire the global shared session (#6621)

Key themes: WebUI improvements (token usage, welcome screen, session cache, model presets), subagent deduplication and performance, and the breaking refactor retiring the global shared session.

Release: `v0.4.1` (2026-11-06) — patch on top of `v0.4.0` (2026-10-28).

## ZeroClaw — `master` (100+ commits)

ZeroClaw's major `v0.9.0` release on Nov 11 is the week's standout. A massive docs overhaul (book/src) runs alongside gateway, provider, and zerocode improvements:

- `2c0a8c26` chore(deps): bump the web-minor-patch group across 1 directory with 21 updates (#11842)
- `1a79f89d` chore(release): bump version to v0.9.0 (#12377)
- `b4ea9059` feat(zerocode): add pairing-free OIDC login and saved remote credentials (#12317)
- `a11a5ce5` feat(gateway): scoped dashboard chat through the core, on a shared RPC client (#12244)
- `77571338` fix(deps): bump rustix to 1.1.6 for RUSTSEC-2026-0486 (#12392)
- `461b9728` fix(providers): recognize claude-opus-5-5 and other adaptive-only models (#12352)

Key themes: OIDC pairing-free login (zerocode), scoped dashboard chat, RUSTSEC bumps, Claude Opus 5.5 recognition, and a thorough docs book rewrite.

Release: `v0.9.0` (2026-11-11) — first major since `v0.8.7` (2026-10-27).

## NanoClaw — `main` (20+ commits)

A steady beta train week with router fixes, setup UX polish, and CI hardening:

- `0ede4cf6` chore(release): v2026.11.0-beta.2 (#4343)
- `62dc0905` fix(router): stop holding sticky follow-ups behind a pending command gate (#4335)
- `f2717cfe` fix(questions): keep the question on an answered ask_user_question card (#4328)
- `df750f67` fix(onecli): warn when a remote gateway points agents at their own machine (#4203)
- `6f5d71ff` Reply in the language of the message being answered (#4329)

Key themes: Router correctness (sticky follow-ups, mention-sticky thread affinity), setup improvements (jq install on WSL, provider-auth restart), and CI security (read-only token).

Releases: `v2026.11.0-beta.1` (2026-11-09), `v2026.11.0-beta.2` (2026-11-12).

## GoClaw — `dev` (16 commits)

Five rapid betas (`.242` → `.246`) with provider, channel, and gateway improvements:

- `9aa045c4` fix(providers): map Anthropic context-window cutoff to length (#1675)
- `b4699c45` feat(channels): add Mattermost channel (#1624)
- `ac2e3055` fix(agent): don't treat identical successful exec results as a runaway loop (#1674)
- `04db3f8b` fix(providers): keep Codex streamed tool calls in model order (#1669)
- `d898d7dc` fix(gateway): fail gateway startup when configured sandbox is unavailable (#1663)

Key themes: Provider correctness (Anthropic context window, Codex tool ordering, MiniMax preference), new Mattermost channel, gateway sandbox availability check, and runaway loop prevention.

Releases: `v3.15.0-beta.242` (11-09), `.243` (11-09), `.244` (11-12), `.245` (11-13), `.246` (11-13).

## IronClaw — `release/*` (0 commits)

No movement. Per the branch map, `main` is unchanged since 2026-09-10 and `release/2026-08-26` last moved 2026-09-29; latest tag `v0.21.0` (2026-03-20) is well outside the window.

## ClawTeam — `main` (13 commits)

Dormant in terms of code — only documentation activity this week:

- `0e933f31` docs: add Bilibili profile link at top of READMEs (2026-11-07)

Twelve additional commits duplicate this change across localized READMEs (CN, KR, JA, FR, DE, ES, IT, PT-BR, RU, TW).

No release; latest `v0.3.0+openclaw2` (2026-07-04) remains unchanged.

## MaxClaw — `main` (0 commits)

Dormant. Last commit 2026-06-13 (`v0.1.2`).

## Releases this week

| Project | Release | Date |
|---|---|---|
| ZeroClaw | `v0.9.0` | 2026-11-11 |
| NanoBot | `v0.4.1` | 2026-11-06 |
| NanoClaw | `v2026.11.0-beta.1` | 2026-11-09 |
| NanoClaw | `v2026.11.0-beta.2` | 2026-11-12 |
| GoClaw | `v3.15.0-beta.242` | 2026-11-09 |
| GoClaw | `v3.15.0-beta.243` | 2026-11-09 |
| GoClaw | `v3.15.0-beta.244` | 2026-11-12 |
| GoClaw | `v3.15.0-beta.245` | 2026-11-13 |
| GoClaw | `v3.15.0-beta.246` | 2026-11-13 |

## Sync notes

- **OpenClaw fetch via SSH succeeded.** The blobless shallow clone's ref was stale (`395a8c13b04`), causing the "incorrect old value" error. The fetch completed to `origin/main` at `8ae9d35bd53` (11 days of changes); local HEAD remains at the Nov 2 pin pending the next full sync cycle.
- **HTTPS git to GitHub is blocked** (web 200, smart-HTTP connect fails). Persistent global rewrite `url."git@github.com:".insteadOf "https://github.com/"` is in effect — all submodule fetches go over SSH.
- **Global `last_check` advanced to 2026-11-13** for the five projects with commits (`openclaw`, `nanobot`, `zeroclaw`, `nanoclaw`, `goclaw`); quiet projects (`ironclaw`, `clawteam`, `maxclaw`) keep stale dates by design.
