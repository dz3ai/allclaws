# ZeroClaw - Zero-dependency Agent - Update Report

**Generated:** 2026-11-20 21:46:02
**Tracking Period:** 2026-11-13 to 2026-11-20

## Recent Commits

### fix(xtask): read the Windows prebuilt installer when the guide is rendered (#12571)
- **Date:** 2026-11-19
- **Author:** Tidux
- **Commit:** dfc70a2b499a5e5ad777a9174a216a29fda7aa35
### fix(deps): patch heapless and Wasmtime RustSec advisories (#12577)
- **Date:** 2026-11-19
- **Author:** CastelloBrancoTecnologia
- **Commit:** 597f53ba7e5b3396ad7b43460f65fd54887efc4c
### fix(gateway): keep per-connection task records out of the INFO trace (#12499)
- **Date:** 2026-11-19
- **Author:** JordanTheJet
- **Commit:** ad4c1f6c3a7d2f734c0b4dab0ff37533971eebb5
### feat(security): read POSIX commands in bash's grammar when bash runs them (#11994)
- **Date:** 2026-11-19
- **Author:** Tidux
- **Commit:** dfe8ab35bd682e3510fe81856f27c0926742cd25
### docs(runtime): correct the shell-grammar binding row before recording approval (#12395)
- **Date:** 2026-11-18
- **Author:** Tidux
- **Commit:** 1c8f2b59bae7d20ac4f8d548824792fd8b2f11e9
### fix(deps): patch SMTP advisories with a bounded base64 duplicate (#12552)
- **Date:** 2026-11-18
- **Author:** CastelloBrancoTecnologia
- **Commit:** 3773cae2d7288f9e6af1ad8414e6d2cd33e90451
### fix(install): verify Windows prebuilt release checksums (#12166)
- **Date:** 2026-11-18
- **Author:** Adam
- **Commit:** bec292f66722234df06fc4b09adf4ac1b625d9f5
### fix(tools): inherit headless SOP step scope on peer-send turns (#12170)
- **Date:** 2026-11-18
- **Author:** ump45nose
- **Commit:** 5e67c70ed99071959c6f5a1bc69a7ccea83f97d5
### fix(tools): require read access before uploads and edits (#12151)
- **Date:** 2026-11-18
- **Author:** Adam
- **Commit:** e59e65f04e05ad5e6950e525c1b4385594cdcbcd
### fix(mcp): confine SSE endpoints and redirects to the server origin (#12149)
- **Date:** 2026-11-18
- **Author:** Adam
- **Commit:** 3537a3533ed2d6e020e03915f7c15a0293609dca
### fix(gateway): treat forwarded loopback as non-local for SOP cancel (#12281)
- **Date:** 2026-11-18
- **Author:** ump45nose
- **Commit:** 1284c6075ba72a76c3a13f1151288fe9140d24fd
### fix(gateway): pin Scalar docs bundle with Subresource Integrity (#12115)
- **Date:** 2026-11-18
- **Author:** ump45nose
- **Commit:** 9426b99cf595caf0b769b5929709a8c70c7513ab
### fix(sop): use the fail-closed mode when the decision answers are unusable (#12237)
- **Date:** 2026-11-18
- **Author:** joalvaradon
- **Commit:** 115a03b51706d3ddbb9c6b7bb06ed2a8f2d1d4af
### fix(deps): update zip for RUSTSEC-2026-0548 and accept the chrono maintenance advisories (#12516)
- **Date:** 2026-11-18
- **Author:** JordanTheJet
- **Commit:** c66542445a3d4c60889c62bfd17aa995e5d8606a
### fix(web): keep paired WebSocket credentials out of URLs (#12335)
- **Date:** 2026-11-17
- **Author:** CastelloBrancoTecnologia
- **Commit:** cda933e6b9937deacbcc0d4d2cd7f1ae5bb4500e
### fix(web): close the model picker on Escape (#12375)
- **Date:** 2026-11-17
- **Author:** GaijinSystems
- **Commit:** b97fa49fe7d32d927a14c043658becc8905e9e39
### fix(web): show a check on the pressed "Keep thinking collapsed" button (#12374)
- **Date:** 2026-11-17
- **Author:** GaijinSystems
- **Commit:** 508e7b79af74d5841f699bf6af737cc189e3e68f
### feat(providers): send output_config.effort on Anthropic requests (#12379)
- **Date:** 2026-11-16
- **Author:** Alejandro Cárdenas
- **Commit:** 69ea0ae1ae6f662ea9952e6247c764289adfe6a2
### fix(zerocode): refresh the context budget after a trim (#12074)
- **Date:** 2026-11-15
- **Author:** Tidux
- **Commit:** 6e83982340297d4682c5399792549ee9e2f275f0
### docs(runtime): propose ADR-016 exception for plugin wake dispatch (#12417)
- **Date:** 2026-11-14
- **Author:** Tidux
- **Commit:** 3a3f2e35865579843e5c37d8eee2e612cd98cd26
... and more (showing recent 20 commits)

## Recent Releases

### v0.9.0
- **Date:** 2026-11-11
- **Description:** chore(docs): pin translations to v0.9.0 (#12380)
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

## Documentation Updates

- **docs/book/src/security/sandboxing.md** - Updated: 2026-11-19
- **crates/zeroclaw-runtime/AGENTS.md** - Updated: 2026-11-18
- **docs/book/src/setup/windows.md** - Updated: 2026-11-18
- **docs/book/src/agents/internals.md** - Updated: 2026-11-18
- **docs/book/src/tools/mcp.md** - Updated: 2026-11-18
- **docs/book/src/sop/decision-models.md** - Updated: 2026-11-18
- **docs/book/src/sop/syntax.md** - Updated: 2026-11-18
- **docs/maintainers/audit-policy.md** - Updated: 2026-11-18
