# NanoClaw - Lightweight Python Agent - Update Report

**Generated:** 2026-11-13 21:31:29
**Tracking Period:** 2026-11-02 to 2026-11-13

## Recent Commits

### chore(release): v2026.11.0-beta.2 (#4343)
- **Date:** 2026-11-12
- **Author:** glifocat
- **Commit:** 0ede4cf61c139879024a941ebbfe1c90b626c7fb
### fix(router): stop holding sticky follow-ups behind a pending command gate (#4335)
- **Date:** 2026-11-11
- **Author:** glifocat
- **Commit:** 62dc09057b792291c887df5caac059f57347849b
### fix: run docker build and pkill without a shell (#4317)
- **Date:** 2026-11-11
- **Author:** glifocat
- **Commit:** 321d1843b9a3f085f1760d2f9cb1be4d54347f56
### fix(questions): keep the question on an answered ask_user_question card (#4328)
- **Date:** 2026-11-11
- **Author:** glifocat
- **Commit:** f2717cfe5611a717c75b221e97952a960e5dbb34
### test(onecli): drop a replace that changed nothing (#4319)
- **Date:** 2026-11-11
- **Author:** glifocat
- **Commit:** 4923dd3eafa07298466f7b42ab8973670c9a6050
### test(add-resend): copy and run the Resend delivery test (#4188)
- **Date:** 2026-11-11
- **Author:** glifocat
- **Commit:** dbdca4baec8c76ccaa2e595973aee71859010c6e
### ci: read-only token for CI; check the release target before running it (#4318)
- **Date:** 2026-11-11
- **Author:** glifocat
- **Commit:** afabbe58be9cb0c6de9a8cb87acea89181556946
### chore(deps-dev): bump prettier to 3.9.10 and reformat src (#4293)
- **Date:** 2026-11-11
- **Author:** glifocat
- **Commit:** 60efd61b3c7939fd9910df72a1cb66923ca40dac
### fix(onecli): warn when a remote gateway points agents at their own machine (#4203)
- **Date:** 2026-11-10
- **Author:** glifocat
- **Commit:** df750f67ab4dffbd28a30d30f06560e82a6f450b
### fix(add-dial): write the default-sender pin's auth file private (#4315)
- **Date:** 2026-11-10
- **Author:** glifocat
- **Commit:** 97ad69bd06a39106321b91ce94e6cf986b42a7ff
### fix(router): mention-sticky follows a thread only after the agent was woken there (#3802)
- **Date:** 2026-11-10
- **Author:** glifocat
- **Commit:** fcee84833935f6e3138476a4fb34baa1525f8342
### fix(setup): install jq so channel setup works on WSL and minimal Linux images (#4202)
- **Date:** 2026-11-10
- **Author:** glifocat
- **Commit:** 535d9de2bcb22e51b373a819fcac7f3f84fa1d13
### fix(setup): restart the host after provider-auth installs a provider (#4213)
- **Date:** 2026-11-10
- **Author:** glifocat
- **Commit:** 99eb65ae64a7c6992a5a4602f067ec67063d1cab
### fix(update): regenerate lockfile-only merge conflicts (#4312)
- **Date:** 2026-11-10
- **Author:** glifocat
- **Commit:** adbc791cc4810eb55972f2fb1dad9d75db287442
### chore(container): bump Claude Code to 2.1.321 and the Agent SDK to 0.3.321 (#4332)
- **Date:** 2026-11-10
- **Author:** Daniel Milliner
- **Commit:** 7929e3f8a996c69f4688d6df47e56804df05afb5
### fix(release): refuse a pre-release that sorts below an existing tag (#4330)
- **Date:** 2026-11-09
- **Author:** glifocat
- **Commit:** 2fa8d69a3e9f8d870f10c233c6ba23b6c7110753
### Reply in the language of the message being answered (#4329)
- **Date:** 2026-11-09
- **Author:** joel-nanoco
- **Commit:** 6f5d71ff031cf3f99c8d4921840360856ebef16d
### chore(release): v2026.11.0-beta.1 (#4326)
- **Date:** 2026-11-09
- **Author:** glifocat
- **Commit:** bdfb2f1df70cfa49b7141bb59ec886dbacfbc366
### feat(release): accept vX.Y.Z-beta.N pre-release tags (#4313)
- **Date:** 2026-11-09
- **Author:** glifocat
- **Commit:** 3d027f5098f32cf88a805fd33b9ed8d8b2ca492a
### fix(setup): reach Docker from the user service when the docker group was just added (#4201)
- **Date:** 2026-11-09
- **Author:** glifocat
- **Commit:** 59beda1706554128048413289e89e32ff70c4f7f
... and more (showing recent 20 commits)

## Recent Releases

### v2026.11.0-beta.2
- **Date:** 2026-11-12
- **Description:** Release v2026.11.0-beta.2
### v2026.11.0-beta.1
- **Date:** 2026-11-09
- **Description:** Release v2026.11.0-beta.1
### v2026.10.1-rc.2
- **Date:** 2026-10-22
- **Description:** Release v2026.10.1-rc.2
### v2026.10.1-rc.1
- **Date:** 2026-10-20
- **Description:** Release v2026.10.1-rc.1
### v2026.10.0-rc.2
- **Date:** 2026-10-05
- **Description:** Release v2026.10.0-rc.2

## Documentation Updates

- **CHANGELOG.md** - Updated: 2026-11-12
- **docs/db-central.md** - Updated: 2026-11-11
- **.claude/skills/add-resend/REMOVE.md** - Updated: 2026-11-11
- **.claude/skills/add-resend/SKILL.md** - Updated: 2026-11-11
- **.claude/skills/add-onecli/SKILL.md** - Updated: 2026-11-10
- **.claude/skills/add-onecli/payload/docs/onecli-upgrades.md** - Updated: 2026-11-10
- **.claude/skills/add-dial/SKILL.md** - Updated: 2026-11-10
- **.claude/skills/add-discord/SKILL.md** - Updated: 2026-11-10
- **.claude/skills/add-slack/SKILL.md** - Updated: 2026-11-10
- **README.md** - Updated: 2026-11-10
- **docs/setup-flow.md** - Updated: 2026-11-10
- **.claude/skills/add-codex/SKILL.md** - Updated: 2026-11-10
- **.claude/skills/add-cursor/SKILL.md** - Updated: 2026-11-10
- **.claude/skills/add-opencode/SKILL.md** - Updated: 2026-11-10
- **docs/provider-host-maintenance.md** - Updated: 2026-11-10
- **.claude/skills/update-nanoclaw/SKILL.md** - Updated: 2026-11-10
- **RELEASING.md** - Updated: 2026-11-09
- **container/CLAUDE.md** - Updated: 2026-11-09
- **docs/build-and-runtime.md** - Updated: 2026-11-08
- **container/agent-runner/src/mcp-tools/interactive.instructions.md** - Updated: 2026-11-08
- **CLAUDE.md** - Updated: 2026-11-05
- **CONTRIBUTING.md** - Updated: 2026-11-05
- **.claude/skills/add-discord/REMOVE.md** - Updated: 2026-11-03
