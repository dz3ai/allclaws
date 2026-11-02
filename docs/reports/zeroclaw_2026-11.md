# ZeroClaw - Zero-dependency Agent - Update Report

**Generated:** 2026-11-02 22:11:45
**Tracking Period:** 2026-10-24 to 2026-11-02

## Recent Commits

### docs(plugins): correct the call_channel! note on results that fail to lift (#11686)
- **Date:** 2026-11-02
- **Author:** Iftekhar Uddin
- **Commit:** 9dbb57231f48e26fee56243de4f7845924ce4f04
### fix(install): show package version from zeroclaw --version field 2 (#12159)
- **Date:** 2026-11-01
- **Author:** ump45nose
- **Commit:** b28d1c3de99099fd565cdedd4d80d8cff7f6a855
### fix(enroll): redeem enrollment codes on the daemon's canonical pairing guard (#11940)
- **Date:** 2026-11-01
- **Author:** Tidux
- **Commit:** 0bb1d4a801ac7dbecc9e9a91128c0a96ace98ab3
### fix(security): split POSIX commands at substitution and subshell boundaries (#11822)
- **Date:** 2026-11-01
- **Author:** Tidux
- **Commit:** 4c9edcf33716381b2c3455649cbd0f3e6b3a38b1
### feat(zerocode): add /load-session to resume a saved session by name or id (#12071)
- **Date:** 2026-11-01
- **Author:** Tidux
- **Commit:** 0e931888de0862fe2143389a86077c28826e877e
### feat(install): install the CLI-only build and switch it to the standard build only on request (#1211
- **Date:** 2026-11-01
- **Author:** JordanTheJet
- **Commit:** df34caf27816fc468f2fde41f190216e8892fe02
### fix(deps): bump Wasmtime to 48.0.8 for RUSTSEC-2026-0420 to 0424 (#12129)
- **Date:** 2026-10-31
- **Author:** JordanTheJet
- **Commit:** f87368a6aa53d16b0bd7411b002331a22622c2a7
### fix(zerocode): clean active-turn clipboard temps on disconnect (#10485)
- **Date:** 2026-10-30
- **Author:** ump45nose
- **Commit:** 1c1cd118ac536a1dd1bc79b9cce69cbdc04e4f29
### fix(sop): match step scope groups to registered tool names (#11283)
- **Date:** 2026-10-30
- **Author:** Iftekhar Uddin
- **Commit:** 3047a6bb6101e90d9b0bb17874dcfe7bc8005c6f
### fix(rpc): refuse persisted log reads to scoped principals (#11326)
- **Date:** 2026-10-30
- **Author:** Iftekhar Uddin
- **Commit:** 8312ef098e07ade301ff268b0561f2d26b2b0dbd
### test(log): cover UTF-8 byte-offset pagination (#12030)
- **Date:** 2026-10-30
- **Author:** Leon-SK668
- **Commit:** 0e526f2aa3856a92429ba711981f2cde69aaf9e8
### test(memory): cover persisted redaction around Unicode text (#12029)
- **Date:** 2026-10-30
- **Author:** Leon-SK668
- **Commit:** 2bfa9ed71be25f0fae954a61514689ce7aac6dab
### fix(plugins): clear abandoned install stages on the next install (#11855)
- **Date:** 2026-10-29
- **Author:** JordanTheJet
- **Commit:** 5a51398dd52469644f2c2a017296b4ff89c8e02a
### ci(cli-only): build and test the CLI-only feature set with an artifact ratchet (#11976)
- **Date:** 2026-10-29
- **Author:** JordanTheJet
- **Commit:** 161ac74562f48e9f279bba6fa9571323fda29c39
### feat(cli): point builds without the gateway to the standard build (#11975)
- **Date:** 2026-10-29
- **Author:** JordanTheJet
- **Commit:** d4dcfa46c28ed48b5fbe200d2ed0eec873aa386c
### feat(channels/signal): add media attachment support (#11556)
- **Date:** 2026-10-29
- **Author:** GaijinSystems
- **Commit:** 3158c45d1d7b076abd9cfce682e4e9b4a9768d4d
### feat(skills): add built-in zeroclaw docs skill (#9579)
- **Date:** 2026-10-29
- **Author:** Cherilyn Buren
- **Commit:** c9dab92c33fc638e1b149a42fd891a93a0c218d8
### feat(telegram): make unauthorized notices configurable and authorization-aware (#11728)
- **Date:** 2026-10-29
- **Author:** Dan Gilles
- **Commit:** 5a28cda06e55af575fcb3c900340f140be465ebb
### fix(plugins): admit a component only beside the manifest that described it (#12040)
- **Date:** 2026-10-29
- **Author:** Magnus Hedemark
- **Commit:** 2161bfe35aac03d376d3e12da7bc8433ae56132c
### fix(tools): expose scenario routing requirements (#11720)
- **Date:** 2026-10-29
- **Author:** Dan Gilles
- **Commit:** 1449d3389f5da9553d9f49cd759251f12e685c93
... and more (showing recent 20 commits)

## Recent Releases

### v0.8.7
- **Date:** 2026-10-27
- **Description:** chore(docs): pin translations to v0.8.7 (#12019)
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

## Documentation Updates

- **docs/book/src/zerocode/secure-transport.md** - Updated: 2026-11-01
- **docs/book/src/zerocode/running.md** - Updated: 2026-11-01
- **docs/book/src/setup/linux.md** - Updated: 2026-11-01
- **docs/book/src/zerocode/remote.md** - Updated: 2026-11-01
- **docs/book/src/architecture/logging.md** - Updated: 2026-10-30
- **docs/book/src/security/authentication.md** - Updated: 2026-10-30
- **docs/book/src/developing/plugin-protocol.md** - Updated: 2026-10-29
- **docs/book/src/plugins/index.md** - Updated: 2026-10-29
- **docs/book/src/maintainers/ci-and-actions.md** - Updated: 2026-10-29
- **docs/book/src/channels/signal.md** - Updated: 2026-10-29
- **crates/zeroclaw-runtime/src/skills/assets/zeroclaw-docs/SKILL.md** - Updated: 2026-10-29
- **docs/book/src/tools/skills.md** - Updated: 2026-10-29
- **docs/book/src/channels/telegram.md** - Updated: 2026-10-29
- **docs/book/src/agents/internals.md** - Updated: 2026-10-29
- **crates/zeroclaw-runtime/AGENTS.md** - Updated: 2026-10-29
- **docs/book/src/architecture/runtime-state-and-persistence.md** - Updated: 2026-10-29
- **docs/book/src/zerocode/config.md** - Updated: 2026-10-29
- **CHANGELOG-next.md** - Updated: 2026-10-24
- **docs/book/src/architecture/rpc-socket.md** - Updated: 2026-10-24
- **docs/book/src/gateway/a2a-discovery.md** - Updated: 2026-10-24
