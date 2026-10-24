# Weekly Submodule Report — 2026-10-24

**Scope:** the 8 projects tracked by `scripts/track-agent-updates.sh` (`openclaw`, `nanoclaw`, `ironclaw`, `goclaw`, `zeroclaw`, `nanobot`, `clawteam`, `maxclaw`). The branch map in `docs/reports/submodule-branch-map.json` covers all 29 submodules; the other 21 are not part of this run.

**Window:** 2026-10-17 → 2026-10-24 (7 days).

**Data source:** `./scripts/track-agent-updates.sh --report-only --since "7 days ago"`, fetching each project's mapped **active line** (not the default branch). Per-project detail: `docs/reports/<project>_2026-10.md`. OpenClaw's full fetch exceeded the 45s budget, so its weekly count was taken from a blobless `--shallow-since="7 days ago"` fetch in a scratch clone.

## Summary

| Project | Active line | Commits (7d) | Releases in window | Status |
|---|---|---:|---|---|
| OpenClaw | `main` | 5,069 | `v2026.10.10-beta.3` (10-20) | active |
| NanoBot | `main` | 157 | — (latest `v0.3.5`, 09-16) | active |
| ZeroClaw | `master` | 87 | `v0.8.6` (10-18) | active |
| NanoClaw | `main` | 78 | `v2026.10.1-rc.1` (10-20), `rc.2` (10-22) | active |
| GoClaw | `dev` | 3 | `v3.15.0-beta.229` (10-17) | active |
| IronClaw | `release/*` | 0 | — (upstream `v1.4.1-rc.2`, 09-24) | stale |
| ClawTeam | `main` | 0 | — (latest `v0.3.0+openclaw2`, 07-04) | dormant |
| MaxClaw | `main` | 0 | — (latest `v0.1.2`, 03-18) | dormant |

**Verdict:** five of eight are active, and the week's theme is **failure-path hardening** — shutdown/drain ordering, credential fencing, symlink auditing, lifecycle locks, and dependency security. Two release trains advanced (NanoClaw CalVer RCs, ZeroClaw patch) plus OpenClaw's beta train. IronClaw, ClawTeam and MaxClaw were quiet.

## OpenClaw — `main` (5,069 commits)

Volume remains monorepo-scale (merge/CI noise included). The week's work is security and resilience:

- `a9ecba94` fix(security): audit symlinked workspace skill roots (#182384)
- `7f919ca7` fix(update): fence readiness credentials at transport send (#182343)
- `012d92f5` fix(standalone): Doctor and backup workers fail to start (#182405)
- `7d8cc22f` refactor(config): share pending-history snapshot gates (#182605)
- `2e267509`, `0367b98b`, `e2d74912` — accessibility/mobile UI corrections
- `fe8d4597` ci: lower test-lines ceiling to 6,480,000 (#182653)

Release: `v2026.10.10-beta.3` (2026-10-20). Current tip `7d8cc22f`.

## NanoBot — `main` (157 commits)

A performance and agent-lifecycle week, mostly WebUI/TUI:

- `ae7fed88e` perf(tui): shrink standalone builds and target native bindings (#6432)
- `4bd1b74c6` perf(webui): defer non-chat startup interfaces
- `67f6a0d26` perf(sdk): reuse consecutive effective model overrides (#6434)
- `f4aacdbec` fix(agent): don't resume abandoned work after `max_iterations`
- `ce885fa31` fix(agent): preserve goal continuation lifecycle
- `0e0df327c` fix(api): route each `session_id` to its own chat
- `60420b45c` fix(webui): keep MCP connection rows compact (NAN-321)

No release in the window; `v0.3.5` remains the latest tag (2026-09-16).

## ZeroClaw — `master` (87 commits)

Correctness work around shutdown, locks and supply chain:

- `23950c9a1` fix(gateway): admit no new request after the gateway stops, and drain its connections (#11901)
- `4db7afdcf` fix(config): move the lifecycle lock into an owner-only `data/.lifecycle` directory (#11803)
- `850f1c7b4` fix(sop): keep a stale run copy from reviving or overwriting a run (#11861)
- `028c50f5e` fix(containers): refresh runtime CA stores after emSign distrust (#11925)
- `df6421301` / `0a6974d3e` — bump `ctutils`/`tokio` for RUSTSEC-2026-0385 and RUSTSEC-2026-0386
- `3c18211b9` fix(plugins): report the runtime's config refusal in `plugin info` and `list --verify` (#11811)

Release: `v0.8.6` (2026-10-18).

## NanoClaw — `main` (78 commits)

Two themes: a CI speed-up and a long review cycle on `add-onecli` safety.

- `40547e14` ci: cut the PR gate from 7.5 to 2.5 minutes with sharded tests and a cached image (#4191)
- `57c4440a` ci: put the jobs added by #4191 on Bun 1.4.4 (#4208)
- `673c96fa` … `7bd56c55` — `add-onecli` dial/delete guard, iterated through review rounds 9–12 (Docker endpoint inspection, address-family checks, localhost binding)
- `b1a9b658` merge of `fix/dial-delete-guard` (#4196)

Releases: `v2026.10.1-rc.1` (10-20), `v2026.10.1-rc.2` (10-22).

## GoClaw — `dev` (3 commits)

Small, integration-focused week:

- `1fc98bcd` fix(channels): split a threaded chat ID before posting to Slack (#1476) (#1637)
- `21a2e8c6` Identify goclaw in Parallel Search requests (#1607)
- `8b1a4766` fix(usage): ignore negative OpenRouter prices instead of dropping the model (#1629)

Release: `v3.15.0-beta.229` (2026-10-17).

## IronClaw — `release/*` (0 commits)

No movement in the window. `main` has been unchanged since 2026-09-10 and the local release surface `release/2026-08-26` last moved 2026-09-29. Upstream's newest tag is `ironclaw-v1.4.1-rc.2` (2026-09-24), also outside the window. The final run's tag-aware fetch hit the 45s budget; the prior run confirmed zero commits either way.

## ClawTeam — `main` (0 commits)

Dormant. Last commit 2026-07-04 (`v0.3.0+openclaw2`).

## MaxClaw — `main` (0 commits)

Dormant. Last commit 2026-06-13 (`v0.1.2`).

## Releases this week

| Project | Release | Date |
|---|---|---|
| OpenClaw | `v2026.10.10-beta.3` | 2026-10-20 |
| NanoClaw | `v2026.10.1-rc.1` | 2026-10-20 |
| NanoClaw | `v2026.10.1-rc.2` | 2026-10-22 |
| ZeroClaw | `v0.8.6` | 2026-10-18 |
| GoClaw | `v3.15.0-beta.229` | 2026-10-17 |

## Sync notes

- Tracking now follows the mapped active line, not the default branch: OpenClaw/NanoBot/NanoClaw on `main`, ZeroClaw on `master`, GoClaw on `dev`, IronClaw on `release/*`.
- The run is branch-scoped with a fetch budget (`TRACKER_FETCH_TIMEOUT=45` here; default 120s). OpenClaw's branch delta exceeds it; its numbers above come from a blobless shallow-since fetch.
- Fetch transport was HTTPS→SSH rewritten for this run (HTTPS to GitHub is blocked in this environment).
- Running the tracker checked out the tracked submodules to their recorded pins (`nanoclaw`, `goclaw`, `nanobot` moved from September to their Oct-18 pointers); the other 21 submodules were not touched.
