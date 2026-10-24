# ZeroClaw - Zero-dependency Agent - Update Report

**Generated:** 2026-10-24 23:16:26
**Tracking Period:** 7 days ago to 2026-10-24

## Recent Commits

### fix(config): move the lifecycle lock into an owner-only data/.lifecycle directory (#11803)
- **Date:** 2026-10-24
- **Author:** JordanTheJet
- **Commit:** 4db7afdcfa9a4b07d55dc6df4331d8076b64c2cb
### fix(tools): probe the saved provider alias after a model-routing update (#10034)
- **Date:** 2026-10-24
- **Author:** Iftekhar Uddin
- **Commit:** 2ae6857099d5452f2bbe003cd64df373bc421215
### fix(gateway): admit no new request after the gateway stops, and drain its connections (#11901)
- **Date:** 2026-10-24
- **Author:** JordanTheJet
- **Commit:** 23950c9a1df0e1ab32bc3ff9879121d54012a0dc
### fix(sop): keep a stale run copy from reviving or overwriting a run (#11861)
- **Date:** 2026-10-24
- **Author:** JordanTheJet
- **Commit:** 850f1c7b4b39bb6df6d818b028c5d9ee949bb623
### fix(containers): refresh runtime CA stores after emSign distrust (#11925)
- **Date:** 2026-10-24
- **Author:** JordanTheJet
- **Commit:** 028c50f5eb96856e3b97cee6256b1342e4ed1914
### fix(deps): bump ctutils and tokio for RUSTSEC-2026-0385 and RUSTSEC-2026-0386 (#12010)
- **Date:** 2026-10-24
- **Author:** JordanTheJet
- **Commit:** df64213016834a0ab69d0c7fbde0e95dccee3ea4
### fix(deps): bump ctutils to 0.4.5 for RUSTSEC-2026-0385 (#11998)
- **Date:** 2026-10-24
- **Author:** mov-xound-glitch
- **Commit:** 0a6974d3e3f43a4066c7d646ecb69c65d003ac6f
### fix(plugins): report the runtime's config refusal in plugin info and list --verify (#11811)
- **Date:** 2026-10-23
- **Author:** JordanTheJet
- **Commit:** 3c18211b9f104c7bb3184ddb7dccae56a97949ee
### test(runtime): make the receipt-bound late_tool_search tests opt-in (#11863)
- **Date:** 2026-10-22
- **Author:** JordanTheJet
- **Commit:** 6a99c3dee4440cf7d052e5bb61836adcf1085582
### fix(plugins): name the sender in plugin_channel_sender_denied records (#11848)
- **Date:** 2026-10-22
- **Author:** JordanTheJet
- **Commit:** 842c71e714dc76c65a374bd75ca050f8f749cc50
### docs(changelog): match the v0.8.6 In brief wording on OIDC (#11841)
- **Date:** 2026-10-22
- **Author:** JordanTheJet
- **Commit:** 40935ae506d9f300b949d9a3a156e992533524af
### ci(plugins): raise the cranelift runtime leg timeout to 30 minutes (#11941)
- **Date:** 2026-10-22
- **Author:** JordanTheJet
- **Commit:** 8858541298c0fd70c94179bb221db0cc43d2f76c
### ci(docker): bound arm64 build memory and add a dry-run dispatch to docker-publish (#11833)
- **Date:** 2026-10-22
- **Author:** JordanTheJet
- **Commit:** 7f2fe028a330c7a46683db6bb1b67ff78bafb1ce
### fix(ci): run the crates.io preflight only for a pull request's own version bump (#11967)
- **Date:** 2026-10-22
- **Author:** JordanTheJet
- **Commit:** 448b9584cfd9363b9e369c17d5ea9426ad016e73
### ci(release): raise the macOS universal desktop job timeout to 240 minutes (#11854)
- **Date:** 2026-10-22
- **Author:** JordanTheJet
- **Commit:** 8f03c962dc45231db567fe67c168e7aae95f806d
### fix(security): share one JWKS fetch among concurrent token checks (#11903)
- **Date:** 2026-10-22
- **Author:** JordanTheJet
- **Commit:** eea20ebf17ab4396d8d5b56e3f40b25eb8b636de
### fix(plugins): remove a loaded plugin from the directory it was loaded from (#11809)
- **Date:** 2026-10-22
- **Author:** JordanTheJet
- **Commit:** 02bb0752602b089bb063fcfde057586c44b38cfd
### ci(security): audit the full lockfile in the daily scan (#11927)
- **Date:** 2026-10-22
- **Author:** JordanTheJet
- **Commit:** b882455d7f853147dce0d32716eba92338193344
### fix(plugins): reserve peripheral, skill and MCP capability tool names before plugin tools register (
- **Date:** 2026-10-22
- **Author:** JordanTheJet
- **Commit:** 65672a33a9d9a1b7d8cf6bb750b8046e670f1a0d
### test(daemon): retain the listener through bind classification (#11929)
- **Date:** 2026-10-22
- **Author:** JordanTheJet
- **Commit:** f3c6682dac9824cc5ab2e9412ddc8c4b36d700da
... and more (showing recent 20 commits)

## Recent Releases

### v0.8.6
- **Date:** 2026-10-18
- **Description:** fix(release): bound memory for the Stable aarch64 musl build (#11837)
### v0.8.5
- **Date:** 2026-09-05
- **Description:** chore(release): bump version to v0.8.5 (#10632)
### v0.8.4
- **Date:** 2026-08-03
- **Description:** chore(release): bump version to v0.8.4 (#9648)
### v0.8.3
- **Date:** 2026-07-15
- **Description:** ci(release): raise build matrix timeout to 90 minutes (#9098)
### v0.8.2
- **Date:** 2026-06-26
- **Description:** ci(release): raise binary size hard limit to 64MB (#8342)

## Documentation Updates

- **docs/maintainers/audit-policy.md** - Updated: 2026-10-24
- **docs/book/src/plugins/index.md** - Updated: 2026-10-23
- **crates/zeroclaw-runtime/tests/fixtures/r5-namespace/README.md** - Updated: 2026-10-22
- **CHANGELOG-next.md** - Updated: 2026-10-22
- **docs/book/src/developing/how-plugins-work.md** - Updated: 2026-10-22
- **docs/book/src/plugins/writing-a-tool-plugin.md** - Updated: 2026-10-22
- **docs/book/src/developing/plugin-protocol.md** - Updated: 2026-10-22
- **docs/book/src/contributing/pr-review-protocol.md** - Updated: 2026-10-22
- **docs/book/src/getting-started/quickstart.md** - Updated: 2026-10-22
- **docs/book/src/channels/mqtt.md** - Updated: 2026-10-21
- **docs/book/src/SUMMARY.md** - Updated: 2026-10-20
- **docs/book/src/channels/discord.md** - Updated: 2026-10-20
- **docs/book/src/maintainers/index.md** - Updated: 2026-10-20
- **docs/book/src/maintainers/plugin-release-acceptance.md** - Updated: 2026-10-20
- **docs/book/src/plugins/distributing-plugins.md** - Updated: 2026-10-20
- **apps/tauri/TESTING.md** - Updated: 2026-10-19
- **docs/book/src/security/model.md** - Updated: 2026-10-19
- **docs/book/src/security/sandboxing.md** - Updated: 2026-10-19
- **docs/book/src/ops/network-deployment.md** - Updated: 2026-10-19
- **docs/book/src/channels/matrix.md** - Updated: 2026-10-19
- **docs/book/src/architecture/config-lifecycle.md** - Updated: 2026-10-18
- **docs/book/src/architecture/logging.md** - Updated: 2026-10-17
- **docs/book/src/architecture/rpc-socket.md** - Updated: 2026-10-17
- **docs/book/src/gateway/a2a-discovery.md** - Updated: 2026-10-17
- **.github/workflows/README.md** - Updated: 2026-10-18
- **docs/book/src/_snippets/plugin-install-layout.md** - Updated: 2026-10-18
- **docs/book/src/maintainers/ci-and-actions.md** - Updated: 2026-10-18
- **docs/book/src/maintainers/release-runbook.md** - Updated: 2026-10-18
- **docs/book/src/philosophy/minimal.md** - Updated: 2026-10-18
- **docs/book/src/tools/skill-bundles.md** - Updated: 2026-10-18
- **docs/book/src/tools/skills.md** - Updated: 2026-10-18
- **nix/README.md** - Updated: 2026-10-18
- **docs/book/src/developing/tool-inventory.md** - Updated: 2026-10-17
- **docs/book/src/setup/linux.md** - Updated: 2026-10-17
- **docs/book/src/setup/macos.md** - Updated: 2026-10-17
- **docs/book/src/setup/windows.md** - Updated: 2026-10-17
- **docs/book/src/tools/overview.md** - Updated: 2026-10-17
