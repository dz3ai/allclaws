# OpenClaw - TypeScript AI Agent Platform - Update Report

**Generated:** 2026-11-13 21:45:00
**Tracking Period:** 2026-11-02 to 2026-11-13

## Recent Commits

### chore(ui): refresh control ui locales (#198280)
- **Date:** 2026-11-13
- **Author:** openclaw-mantis[bot]
- **Commit:** 8ae9d35bd53b98072e72f5793eb41de5ddc0ddaf
### fix: isolate held agent databases until explicit restoration (#198180)
- **Date:** 2026-11-13
- **Author:** Peter Steinberger
- **Commit:** 68a839b937868db841ae65af2b4c85b2ff8d7e9c
### test(release): remove waiver regression coverage (#198274)
- **Date:** 2026-11-13
- **Author:** Dallin Romney
- **Commit:** b9f1e62e00d81cf1048af24aaecb47c97afe15c1
### fix(release): apply 2026.11.4 performance waiver release-wide (#198271)
- **Date:** 2026-11-13
- **Author:** Dallin Romney
- **Commit:** 514a224c6eab039a926e4c47b22bb42e51484408
### improve: compact person activity cards (#198040)
- **Date:** 2026-11-13
- **Author:** RoboClaw
- **Commit:** 439a9c3552da1e939803fc3c69d87bc6e16a6553
### improve(ui): keep flat-reply reactions under the reply and the reaction picker in place (#198252)
- **Date:** 2026-11-13
- **Author:** RoboClaw
- **Commit:** 60aead2d9454cbd26c4101ecf8613599c540d6b2
### feat(ui): switch command palette between Search and Compose (#186059)
- **Date:** 2026-11-13
- **Author:** Vyctor H. Brzezowski
- **Commit:** 9b11465147cb3e6567940da1ea9f6ff0616d4d7c
### test(agents): account for Anthropic cache checkpoints in forks
- **Date:** 2026-11-13
- **Author:** Vincent Koc
- **Commit:** 94018632e72d8cb6aca3c8af3da52f7bea8d3462
### fix(ui): chat cost popover hides the session's total spend (#198261)
- **Date:** 2026-11-13
- **Author:** Ayaan Zaidi
- **Commit:** eb1a592fc06233963cb8b70ad998f271b8e2da81
### fix(telegram): keep callback controls when replacement delivery fails (#193948)
- **Date:** 2026-11-13
- **Author:** AmelioMansour
- **Commit:** 69a232ff34c8df4083dc422dd1787e819c2ffd99
### fix(telegram): disabled buttons render as active and stay clickable (#191647)
- **Date:** 2026-11-13
- **Author:** Arseniy Palagin
- **Commit:** f978e54df2d81b21d1cc55ac83ebc68fada97a6c
### fix(auto-reply): keep group-thread digest/reply truncation surrogate-safe (#198200)
- **Date:** 2026-11-13
- **Author:** SunnyShu
- **Commit:** 3dce8063a241793feb9abc9e2bc4383d86723f13
### test(talk): retire native fixture prompt observations (#198248)
- **Date:** 2026-11-13
- **Author:** RoboClaw
- **Commit:** f52d9254a99cd061f19f24459fa48fd5704e8cc5
### fix(media): downscale tall screenshots instead of dropping them (#198250)
- **Date:** 2026-11-13
- **Author:** Ayaan Zaidi
- **Commit:** 777c036d592808418f95da97cf6b4ee6af614bbc
### fix(gateway): keep ACP bridge photos in the Control UI chat history (#193703)
- **Date:** 2026-11-13
- **Author:** weiqinl
- **Commit:** 9d28854c4322988d1ad1443604e365547224695
### fix(telegram): drop native commands from DM senders dmPolicy does not admit (#182128)
- **Date:** 2026-11-13
- **Author:** mushuiyu886
- **Commit:** d5d77e181a2eb67ba71852e51c68b5ab018a326f
### chore(ui): refresh control ui locales (#198249)
- **Date:** 2026-11-13
- **Author:** openclaw-mantis[bot]
- **Commit:** c0a4b4bf6496217e9a5cd91f0cc8f29c64b83d
### test(auto-reply): scope memory carriers to the current human turn (#198242)
- **Date:** 2026-11-13
- **Author:** RoboClaw
- **Commit:** 6399d3151e1dd64a1dd188feee53172368ccdb7e
### fix(workspaces): let checkpoints progress during manifest sweeps (#198157)
- **Date:** 2026-11-13
- **Author:** Peter Steinberger
- **Commit:** 3e0130930848d53adcdf0198157
### feat(database): hold Gateway state ownership in PostgreSQL on all-PostgreSQL installs (#196237)
- **Date:** 2026-11-13
- **Author:** Mitchell Etzel
- **Commit:** c886f82c779386cc320195732b6d1b74ad5d05ae
### a71fd0b7326 fix(mattermost): answer shows twice when a post lands below the streaming preview (#198206)
- **Date:** 2026-11-12
- **Author:** Peter Steinberger
- **Commit:** a71fd0b7326
### e9f72a9f29b fix(telegram): a bare `<word` hides later tags in Markdown replies (#196281)
- **Date:** 2026-11-12
- **Author:** Peter Steinberger
- **Commit:** e9f72a9f29b
### def307d6d73 fix(worktrees): resume bounded pack retirement before batching (#198236)
- **Date:** 2026-11-12
- **Author:** Peter Steinberger
- **Commit:** def307d6d73
### 84727572dd0 fix(test): detect caller header mutation on redirects (#198181)
- **Date:** 2026-11-12
- **Author:** Peter Steinberger
- **Commit:** 84727572dd0
### 8ff37a6828b fix(sandbox): keep agents running during atomic workspace snapshots (#198128)
- **Date:** 2026-11-12
- **Author:** Peter Steinberger
- **Commit:** 8ff37a6828b
### 6057a3b2529 feat: keep creative projects grounded in their visual references (#198229)
- **Date:** 2026-11-12
- **Author:** Peter Steinberger
- **Commit:** 6057a3b2529
### 4f8df80bd00 fix(cli): Claude CLI conversation keeps failing after one live-session cleanup failure (#198224)
- **Date:** 2026-11-12
- **Author:** Peter Steinberger
- **Commit:** 4f8df80bd00
### 928c118f64d fix(telegram): agent inline button taps expire instead of reaching the agent (#196217)
- **Date:** 2026-11-12
- **Author:** Peter Steinberger
- **Commit:** 928c118f64d
### aab5100b8a5 fix(skills): skills update --all keeps replacing skills after Ctrl+C (#198163)
- **Date:** 2026-11-12
- **Author:** Peter Steinberger
- **Commit:** aab5100b8a5
### c4f355c2 fix: honor corrected image references and generation options (#198196)
- **Date:** 2026-11-12
- **Author:** Peter Steinberger
- **Commit:** c4f355c2
### f86e06de8c7 improve(ui): show plugin guidance as a quiet aside in the transcript (#198215)
- **Date:** 2026-11-12
- **Author:** Peter Steinberger
- **Commit:** f86e06de8c7
### 3370acfc747 fix(ui): name the subagent a live activity line addresses, not its key suffix (#198213)
- **Date:** 2026-11-12
- **Author:** Peter Steinberger
- **Commit:** 3370acfc747
### 1ec9d7b379e fix(update): retain failed preflight cleanup ownership (#198217)
- **Date:** 2026-11-12
- **Author:** Peter Steinberger
- **Commit:** 1ec9d7b379e
### 4a24e68929d fix(qa): ignore appended prompt updates when selecting tasks (#198177)
- **Date:** 2026-11-12
- **Author:** Peter Steinberger
- **Commit:** 4a24e68929d
### 32527d0af04 docs(ios): agent skill and pnpm ios:sim:pair for simulator proof (#198186)
- **Date:** 2026-11-12
- **Author:** Peter Steinberger
- **Commit:** 32527d0af04
### f4e9c2731b1 test(ui): await pending input dismissal request receipt (#198209)
- **Date:** 2026-11-12
- **Author:** Peter Steinberger
- **Commit:** f4e9c2731b1
### de02a1f5749 fix(system-agent): reply with rescue command findings when the command exits non-zero (#195451)
- **Date:** 2026-11-12
- **Author:** Peter Steinberger
- **Commit:** de02a1f5749
### 4aa0168e1f2 chore(ui): refresh control ui locales (#198211)
- **Date:** 2026-11-12
- **Author:** Peter Steinberger
- **Commit:** 4aa0168e1f2
### 986f9ed766d fix(agents): stop warning that documented core tool groups need a plugin (#161245) (#161362)
- **Date:** 2026-11-12
- **Author:** Peter Steinberger
- **Commit:** 986f9ed766d
### 46b5a3b3558 fix(skills): reject missing values for telegram e2e runner options (#197627)
- **Date:** 2026-11-12
- **Author:** Peter Steinberger
- **Commit:** 46b5a3b3558
### 31f619ac1b4 test(gateway): align continuation skip with pinned prompts (#198199)
- **Date:** 2026-11-12
- **Author:** Peter Steinberger
- **Commit:** 31f619ac1b4
### d4efc84735c fix(exec): keep line-continued commands intact during shell preflight (#166714)
- **Date:** 2026-11-12
- **Author:** Peter Steinberger
- **Commit:** d4efc84735c
### f5ceb2dc770 fix(worktrees): report scratch deferrals before the GC backlog (#198165)
- **Date:** 2026-11-12
- **Author:** Peter Steinberger
- **Commit:** f5ceb2dc770
### 2ff4256ae37 feat(database): keep PostgreSQL rollback captures in PostgreSQL (#196236)
- **Date:** 2026-11-12
- **Author:** Peter Steinberger
- **Commit:** 2ff4256ae37
### 0f17a804ea3 fix: configured extra bootstrap files are skipped without a warning (#188295)
- **Date:** 2026-11-12
- **Author:** Peter Steinberger
- **Commit:** 0f17a804ea3
### a7d05c7af04 test(ui): follow ordered browser input in route handoff (#198192)
- **Date:** 2026-11-12
- **Author:** Peter Steinberger
- **Commit:** a7d05c7af04
### 5da97e5b0bb fix(ui): keep dictated text when the window loses focus (#197852)
- **Date:** 2026-11-12
- **Author:** Peter Steinberger
- **Commit:** 5da97e5b0bb
### 08103c5df8b test(agents): preserve BTW user context boundaries
- **Date:** 2026-11-12
- **Author:** Peter Steinberger
- **Commit:** 08103c5df8b
### e1bfcc0887d fix(ci): bound planner benchmark dispatch inputs (#198147)
- **Date:** 2026-11-12
- **Author:** Peter Steinberger
- **Commit:** e1bfcc0887d
### 96c685be0e0 feat(backup): restore PostgreSQL stores into a staging database for restore drills (#194808)
- **Date:** 2026-11-12
- **Author:** Peter Steinberger
- **Commit:** 96c685be0e0
### af98b870029 fix(auth): report named profile expiry in fallback status JSON (#197113)
- **Date:** 2026-11-12
- **Author:** Peter Steinberger
- **Commit:** af98b870029

... and more (showing recent 49 of 4,019 commits)

## Releases

No new tagged release in the window. Latest: `v2026.10.10-beta.5` (2026-10-29).

The `2026.11.4` performance waiver landed as a release-wide fix (#198271) without a new tag.

## Documentation Updates

- **docs/ios/AGENTS.md** - Updated: 2026-11-12
- **docs/ios/AGENTS.md** - Updated: 2026-11-12
- **CLAUDE.md** - Updated: 2026-11-05 (estimated from commit pattern)
