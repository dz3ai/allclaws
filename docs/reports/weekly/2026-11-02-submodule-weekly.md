# Weekly Submodule Report — 2026-11-02

**Scope:** the 8 projects tracked by `scripts/track-agent-updates.sh` (`openclaw`, `nanoclaw`, `ironclaw`, `goclaw`, `zeroclaw`, `nanobot`, `clawteam`, `maxclaw`). The branch map in `docs/reports/submodule-branch-map.json` covers all 29 submodules; the other 21 are not part of this run.

**Window:** 2026-10-24 → 2026-11-02 (9 days).

**Data source:** `./scripts/track-agent-updates.sh --since "2026-10-24"`, fetching each project's mapped **active line** (not the default branch). Per-project detail: `docs/reports/<project>_2026-11.md`. OpenClaw's submodule was re-seeded this week as a blobless shallow clone (see Sync notes) — no scratch-clone fallback was needed.

## Summary

| Project | Active line | Commits (9d) | Releases in window | Status |
|---|---|---:|---|---|
| OpenClaw | `main` | 5,833 | `v2026.10.10-beta.4` (10-26), `beta.5` (10-29) | active |
| NanoBot | `main` | 100 | `v0.4.0` (10-28) | active |
| ZeroClaw | `master` | 37 | `v0.8.7` (10-27) | active |
| NanoClaw | `main` | 3 | — (latest `v2026.10.1-rc.2`, 10-22) | active |
| GoClaw | `dev` | 2 | `v3.15.0-beta.230` (10-29), `beta.231` (10-30) | active |
| IronClaw | `release/*` | 0 | — (upstream `ironclaw-v1.4.1-rc.2`, 09-24) | stale |
| ClawTeam | `main` | 0 | — (latest `v0.3.0+openclaw2`, 07-04) | dormant |
| MaxClaw | `main` | 0 | — (latest `v0.1.2`, 03-18) | dormant |

**Verdict:** a release week — four of the five active projects shipped (NanoBot's `v0.4.0` minor is the headline, first since `v0.3.5` in September), alongside OpenClaw's continuing beta train, ZeroClaw's patch, and two GoClaw betas. Thematically the hardening line from October continues: replay/retry safety in NanoBot, command-injection boundaries and RUSTSEC bumps in ZeroClaw, plugin-lifecycle and startup-stall fixes in OpenClaw.

## OpenClaw — `main` (5,833 commits)

Volume remains monorepo-scale (merge/CI noise included). Plugin lifecycle, Gateway startup and backup correctness dominate the tail of the window:

- `395a8c13` fix(doctor): historical import coverage times out in CI (#191129)
- `5a160d1a` fix(plugins): detach retained consumer cleanup from caller scope (#191126)
- `47ccc4e2` fix(plugins): distinguish CLI inspection from Gateway state (#191095)
- `e68dfaf7` fix: avoid state database clone stalls during Gateway startup (#190918)
- `e4758f1f` fix(backup): release unselected verification candidates (#191107)
- `1940af24` fix: reduce shared-session context preparation overhead (#191105)
- `ee3d681d` perf(control-ui): paint cached context usage with the composer (#190824)
- `c6ad0a95` fix(openai): avoid repacing GPT-Live carrier audio (#189029)

Releases: `v2026.10.10-beta.4` (2026-10-26), `v2026.10.10-beta.5` (2026-10-29). Current tip `395a8c13`.

## NanoBot — `main` (100 commits)

The `v0.4.0` release week, with runtime-safety fixes landing right up to the tag:

- `384b7638` fix(runtime): preserve recovery history and prevent unsafe MCP replays (#6537)
- `4e77d9c3` fix(retry): prevent replay amplification and isolate backoff (NAN-313)
- `3e406841` refactor(agent): delegate recovery channel eligibility to admission
- `1c28b20c` fix(gateway): reuse Windows-safe atomic lease I/O
- `2853287e` perf(gateway): avoid unchanged client lease writes
- `8a989d5a` feat(matrix): per-room group policy overrides (#6287)
- `cb3ba453` refactor: remove legacy history and proxy migrations (#6518)

Release: `v0.4.0` (2026-10-28) — first minor since `v0.3.5` (2026-09-16).

## ZeroClaw — `master` (37 commits)

Security boundaries and supply chain, plus zerocode session UX:

- `4c9edcf3` fix(security): split POSIX commands at substitution and subshell boundaries (#11822)
- `f87368a6` fix(deps): bump Wasmtime to 48.0.8 for RUSTSEC-2026-0420–0424 (#12129)
- `0bb1d4a8` fix(enroll): redeem enrollment codes on the daemon's canonical pairing guard (#11940)
- `8312ef09` fix(rpc): refuse persisted log reads to scoped principals (#11326)
- `0e931888` feat(zerocode): add /load-session to resume a saved session by name or id (#12071)
- `df34caf2` feat(install): install the CLI-only build and switch it to the standard build only on request (#12111)

Release: `v0.8.7` (2026-10-27).

## NanoClaw — `main` (3 commits)

A quiet week after the October RC train — setup UX polish and the routine image refresh:

- `acc2b1c8` agent-images: v2026.10.0 -> v2026.10.0-20261026T0306 (#4226)
- `4d7bd0ad` fix(setup): name the signed-in account and let setup switch it (#4225)
- `818632dd` fix(setup): print the device code beside the portal link (#4224)

No release in the window; `v2026.10.1-rc.2` remains latest (2026-10-22).

## GoClaw — `dev` (2 commits)

Two commits but two beta tags — the release train runs ahead of `dev` merge volume:

- `22e71c80` feat(providers/acp): stream thinking and tool call progress updates (#1618)
- `7cb374a7` fix(channels): scope Slack placeholders per reply thread (#1476) (#1643)

Releases: `v3.15.0-beta.230` (2026-10-29), `v3.15.0-beta.231` (2026-10-30).

## IronClaw — `release/*` (0 commits)

No movement in the window. Per the branch map, `main` is unchanged since 2026-09-10 and `release/2026-08-26` last moved 2026-09-29; upstream's newest tag `ironclaw-v1.4.1-rc.2` (2026-09-24) is outside the window.

## ClawTeam — `main` (0 commits)

Dormant. Last commit 2026-07-04 (`v0.3.0+openclaw2`).

## MaxClaw — `main` (0 commits)

Dormant. Last commit 2026-06-13 (`v0.1.2`).

## Releases this week

| Project | Release | Date |
|---|---|---|
| OpenClaw | `v2026.10.10-beta.4` | 2026-10-26 |
| OpenClaw | `v2026.10.10-beta.5` | 2026-10-29 |
| NanoBot | `v0.4.0` | 2026-10-28 |
| ZeroClaw | `v0.8.7` | 2026-10-27 |
| GoClaw | `v3.15.0-beta.230` | 2026-10-29 |
| GoClaw | `v3.15.0-beta.231` | 2026-10-30 |

## Sync notes

- **OpenClaw re-seeded as a blobless shallow clone.** The Nov 1 run died mid-clone of the full ~12.4 GB repo. The submodule was rebuilt manually with `git clone --filter=blob:none --shallow-since=2026-09-15 --no-checkout` (153 MB, ~1 min) and absorbed into `.git/modules/openclaw`; the tracker's init check passes and its fetch is now a small blobless delta. The clone has no working tree — metadata (log/tags) only, which is all the tracker reads. The pinned gitlink (`e914feb1`, Oct pointer) differs from the checked-out tip, so the parent repo shows `openclaw` modified until the next sync run; this commit deliberately leaves the pin unmoved.
- **HTTPS git to GitHub is blocked in this environment again** (web 200, smart-HTTP connect fails). A persistent global rewrite is now configured: `url."git@github.com:".insteadOf "https://github.com/"` — all submodule fetches go over SSH. Previous runs applied this per-run.
- This run completes the window the interrupted Nov 1 run started (it had produced only `nanoclaw`/`maxclaw` reports); all 8 reports were regenerated for 2026-10-24 → 2026-11-02.
- `clawteam` and `goclaw` were freshly cloned during the run — all 8 tracked submodules are now initialized locally.
- State: global `last_check` advanced to 2026-11-02 for the five projects with commits (`openclaw`, `nanobot`, `zeroclaw`, `nanoclaw`, `goclaw`); quiet projects (`ironclaw`, `clawteam`, `maxclaw`) keep stale dates by design.
