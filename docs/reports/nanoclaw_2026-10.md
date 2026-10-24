# NanoClaw - Lightweight Python Agent - Update Report

**Generated:** 2026-10-24 23:15:26
**Tracking Period:** 7 days ago to 2026-10-24

## Recent Commits

### Merge pull request #4196 from nanocoai/fix/dial-delete-guard
- **Date:** 2026-10-23
- **Author:** glifocat
- **Commit:** b1a9b65806d2c4d3c6981bd96448068fb6c62606
### ci: put the jobs added by #4191 on Bun 1.4.4 (#4208)
- **Date:** 2026-10-23
- **Author:** glifocat
- **Commit:** 57c4440a95acc2f06079bab337ecffafd2483c35
### ci: cut the PR gate from 7.5 to 2.5 minutes with sharded tests and a cached image (#4191)
- **Date:** 2026-10-23
- **Author:** zvi-fried
- **Commit:** 40547e147142c51920531e8f3b54b22a13e1351f
### docs(add-onecli): clearer order for a gateway older than 1.42
- **Date:** 2026-10-23
- **Author:** glifocat
- **Commit:** 478f7d532c0143cce71df409681395d2dd5c16cb
### fix(add-onecli): inspect the gateway container only through the checked Docker endpoint (review roun
- **Date:** 2026-10-23
- **Author:** glifocat
- **Commit:** 673c96fa5cdd64c36010457c98ade53d1def91ef
### fix(add-onecli): pin a localhost GW to the address its container binds (review round 11)
- **Date:** 2026-10-23
- **Author:** glifocat
- **Commit:** df4be0f3c6d7d49c9b165f9e033136ca3bae1446
### fix(add-onecli): only a TCP binding on GW's address family proves the container (review round 10)
- **Date:** 2026-10-23
- **Author:** glifocat
- **Commit:** 0390293680ef9a224fc168f1073f2b191b0df980
### fix(add-onecli): trust only a local Docker daemon; true progress after a mid-delete conversion (revi
- **Date:** 2026-10-23
- **Author:** glifocat
- **Commit:** 43649ee9170187e7064d4f20893a4c282192dbe2
### fix(add-onecli): a localhost gateway matches its 127.0.0.1 port binding
- **Date:** 2026-10-23
- **Author:** glifocat
- **Commit:** 32aa2689aa847def8bcf991e3d1aca70a41f25b2
### fix(add-onecli): Dial check deletes whenever old rules may decide (review round 8)
- **Date:** 2026-10-23
- **Author:** glifocat
- **Commit:** 7bd56c55d98a35652a6f0cc7481ecc4811e3b53c
### fix(add-onecli): Dial check deletes when old rules decide, trusts only the gateway's own container (
- **Date:** 2026-10-23
- **Author:** glifocat
- **Commit:** 48191af298f607ff1c520c1d32d58752b782d196
### fix(add-onecli): count old Dial rules only while they apply (review round 6)
- **Date:** 2026-10-23
- **Author:** glifocat
- **Commit:** 1e56363f044bad70e1f541e186f4b0a078757685
### fix(add-onecli): Dial check counts only restricting rules, reads old rules, guards partial deletes (
- **Date:** 2026-10-23
- **Author:** glifocat
- **Commit:** c9d5640c7f0ddb247bcf69b0f6330c5e2e7ee296
### fix(add-onecli): Dial check handles pre-1.42 gateways and deletes only for Dial findings (remote rev
- **Date:** 2026-10-23
- **Author:** glifocat
- **Commit:** f2b27f0057a8007617599bfadeb2066834cdd218
### chore(container): bump Bun to 1.4.4 for the eMudhra root removal (#4193)
- **Date:** 2026-10-22
- **Author:** glifocat
- **Commit:** b622660ce3636a6e616cbaeef095b1299e1e68c7
### fix(add-onecli): a Dial-only host pattern must stay inside getdial.ai (review round 3)
- **Date:** 2026-10-22
- **Author:** glifocat
- **Commit:** 617170c3302c360584cecf2fae5032027033ee69
### fix(add-onecli): Dial key check follows OneCLI's own matcher and modes (review round 2)
- **Date:** 2026-10-22
- **Author:** glifocat
- **Commit:** d54528717c5f925d829653d4e9e06bd80733f9bc
### fix(add-onecli): harden the Dial key check (review follow-ups)
- **Date:** 2026-10-22
- **Author:** glifocat
- **Commit:** 0f7d625e679ac18654d2e120b555297a836c6b70
### fix(add-onecli): delete the Dial key on upgrade only when the conversion could widen it
- **Date:** 2026-10-22
- **Author:** glifocat
- **Commit:** 6babea5d2e6229440f24cb5a2d5d0cc1396c4931
### chore(release): v2026.10.1-rc.2 (#4190)
- **Date:** 2026-10-22
- **Author:** glifocat
- **Commit:** bf46086e6c3fc64510c571d0cab07455a8c593b7
... and more (showing recent 20 commits)

## Recent Releases

### v2026.10.1-rc.2
- **Date:** 2026-10-22
- **Description:** Release v2026.10.1-rc.2
### v2026.10.1-rc.1
- **Date:** 2026-10-20
- **Description:** Release v2026.10.1-rc.1
### v2026.10.0-rc.2
- **Date:** 2026-10-05
- **Description:** Release v2026.10.0-rc.2
### v2026.10.0-rc.1
- **Date:** 2026-10-04
- **Description:** Release v2026.10.0-rc.1
### v2026.10.0
- **Date:** 2026-10-09
- **Description:** Release v2026.10.0

## Documentation Updates

- **.claude/skills/add-onecli/payload/docs/onecli-upgrades.md** - Updated: 2026-10-23
- **CHANGELOG.md** - Updated: 2026-10-22
- **.claude/skills/add-vercel/SKILL.md** - Updated: 2026-10-22
- **.claude/skills/migrate-from-openclaw/SKILL.md** - Updated: 2026-10-22
- **docs/setup-flow.md** - Updated: 2026-10-22
- **.claude/skills/add-dial-tool/SKILL.md** - Updated: 2026-10-22
- **.claude/skills/add-dial-tool/REMOVE.md** - Updated: 2026-10-22
- **.claude/skills/add-dial-tool/container-skills/dial-cli/SKILL.md** - Updated: 2026-10-22
- **.claude/skills/add-dial/SKILL.md** - Updated: 2026-10-22
- **README.md** - Updated: 2026-10-22
- **docs/build-and-runtime.md** - Updated: 2026-10-22
- **.claude/skills/add-onecli/SKILL.md** - Updated: 2026-10-22
- **.claude/skills/add-onecli/references/chatgpt-oauth-refresh.md** - Updated: 2026-10-22
- **.claude/skills/add-tavily-tool/SKILL.md** - Updated: 2026-10-22
- **.claude/skills/add-tavily-tool/upgrade-instructions.md** - Updated: 2026-10-22
- **.claude/skills/add-vercel/REMOVE.md** - Updated: 2026-10-22
- **.claude/skills/debug/SKILL.md** - Updated: 2026-10-22
- **docs/gateway-seam.md** - Updated: 2026-10-22
- **docs/v1-to-v2-changes.md** - Updated: 2026-10-22
- **docs/SECURITY.md** - Updated: 2026-10-22
- **.claude/skills/add-gchat/SKILL.md** - Updated: 2026-10-22
- **.claude/skills/add-github/SKILL.md** - Updated: 2026-10-22
- **.claude/skills/add-linear/SKILL.md** - Updated: 2026-10-22
- **.claude/skills/add-mattermost/SKILL.md** - Updated: 2026-10-22
- **.claude/skills/add-resend/SKILL.md** - Updated: 2026-10-22
- **.claude/skills/add-slack/SKILL.md** - Updated: 2026-10-22
- **.claude/skills/add-teams/SKILL.md** - Updated: 2026-10-22
- **.claude/skills/add-webex/SKILL.md** - Updated: 2026-10-22
- **.claude/skills/add-whatsapp-cloud/SKILL.md** - Updated: 2026-10-22
- **setup/channels/fixtures/mattermost/README.md** - Updated: 2026-10-22
- **.claude/skills/add-opencode/REMOVE.md** - Updated: 2026-10-22
- **.claude/skills/add-opencode/SKILL.md** - Updated: 2026-10-22
- **.claude/skills/add-gchat/REMOVE.md** - Updated: 2026-10-21
- **.claude/skills/add-imessage/REMOVE.md** - Updated: 2026-10-21
- **.claude/skills/slack-agent-flow/SKILL.md** - Updated: 2026-10-21
- **.claude/skills/update-skills/SKILL.md** - Updated: 2026-10-20
- **CLAUDE.md** - Updated: 2026-10-20
- **CONTRIBUTING.md** - Updated: 2026-10-20
- **docs/BRANCH-FORK-MAINTENANCE.md** - Updated: 2026-10-20
- **docs/agent-runner-details.md** - Updated: 2026-10-20
- **docs/central-db-async-migration.md** - Updated: 2026-10-20
- **docs/provider-host-maintenance.md** - Updated: 2026-10-20
- **docs/skill-guidelines.md** - Updated: 2026-10-20
- **docs/skills-model.md** - Updated: 2026-10-20
- **.claude/skills/add-codex/SKILL.md** - Updated: 2026-10-19
- **.claude/skills/add-iron-proxy/SKILL.md** - Updated: 2026-10-19
- **.claude/skills/add-cursor/REMOVE.md** - Updated: 2026-10-19
- **.claude/skills/add-cursor/SKILL.md** - Updated: 2026-10-19
- **docs/hardened-image.md** - Updated: 2026-10-19
- **.claude/skills/slack-a2a-rooms/SKILL.md** - Updated: 2026-10-19
- **container/agent-runner/src/mcp-tools/agents.instructions.md** - Updated: 2026-10-18
- **docs/setup-wiring.md** - Updated: 2026-10-18
- **docs/templates.md** - Updated: 2026-10-18
- **templates/README.md** - Updated: 2026-10-18
