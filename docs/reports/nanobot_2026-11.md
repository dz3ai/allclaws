# Nanobot - Multi-agent Research - Update Report

**Generated:** 2026-11-02 22:11:24
**Tracking Period:** 2026-10-24 to 2026-11-02

## Recent Commits

### fix(runtime): preserve recovery history and prevent unsafe MCP replays (#6537)
- **Date:** 2026-11-02
- **Author:** chengyongru
- **Commit:** 384b7638307e5c9279286df78ace5759311ea603
### fix(webui): avoid remounting outgoing conversations (#6540)
- **Date:** 2026-11-02
- **Author:** chengyongru
- **Commit:** c1ed649b81906394e35d553ae2a3319ebfe7b935
### fix(providers): tighten tool calls and compatibility fallbacks
- **Date:** 2026-10-10
- **Author:** chengyongru
- **Commit:** 8b37976d36c2812c62b464321e729a88872b60f9
### refactor(agent): delegate recovery channel eligibility to admission
- **Date:** 2026-10-30
- **Author:** chengyongru
- **Commit:** 3e4068411275fac02fbc109926fffea855a94961
### fix(tools): correct DeepSeek Search rate-limit guidance
- **Date:** 2026-10-30
- **Author:** chengyongru
- **Commit:** 29d0023fcadf7fecd595f32f999d8e9b83392e8c
### docs: add nanobot WeChat community QR entry
- **Date:** 2026-10-30
- **Author:** Xubin Ren
- **Commit:** 7eacc789d426a8293459d0ed0d5ca48c0c65ce1d
### refactor: remove redundant comments and docstrings (#6527)
- **Date:** 2026-10-30
- **Author:** chengyongru
- **Commit:** a4d2430140735a85cf0634d8ae888cd42f1913bf
### refactor: remove legacy history and proxy migrations (#6518)
- **Date:** 2026-10-29
- **Author:** chengyongru
- **Commit:** cb3ba4531761b49f61568754eb3d3ce84db4b75d
### fix(gateway): reuse Windows-safe atomic lease I/O
- **Date:** 2026-10-29
- **Author:** chengyongru
- **Commit:** 1c28b20c7e11c06b5f589259e62be238da387b11
### perf(gateway): avoid unchanged client lease writes
- **Date:** 2026-10-29
- **Author:** chengyongru
- **Commit:** 2853287ed79d9abe997bb98e8163ad79419a4cbd
### feat(matrix): per-room group policy overrides (groupPolicyOverrides) (#6287)
- **Date:** 2026-10-28
- **Author:** Orrin Witt
- **Commit:** 8a989d5adf1aebf497288351582572c342d794ed
### feat(matrix): make non-threaded reply quoting optional
- **Date:** 2026-10-29
- **Author:** chengyongru
- **Commit:** c5cee9f204b6788a8384fb41375f3cb5ce0d36f7
### fix(retry): prevent replay amplification and isolate backoff (NAN-313)
- **Date:** 2026-10-21
- **Author:** chengyongru
- **Commit:** 4e77d9c3f2bc6b7a77f4e9f3640a98ef19ce80e0
### refactor(sessions): discover target handles through search (#6315)
- **Date:** 2026-10-29
- **Author:** david
- **Commit:** b6d9009bb472f25cc1e89623d254a0ec16d96d0f
### refactor(channels): move tool hint rendering out of core (#6498)
- **Date:** 2026-10-29
- **Author:** chengyongru
- **Commit:** acc3750c281a322f9647fc7285ed6647c4d214bf
### feat(matrix): add "listen" group policy (observe room, reply on mention) (#6289)
- **Date:** 2026-10-28
- **Author:** Orrin Witt
- **Commit:** b1cc89e9220f31a9af32f2d3abb76185a1eb13ce
### docs: refresh README news and WebUI gallery
- **Date:** 2026-10-28
- **Author:** chengyongru
- **Commit:** 55210eb9f1217bcddb53b8987bcd74ecadd975af
### refactor(webui): centralize outbound delivery (NAN-365)
- **Date:** 2026-10-27
- **Author:** chengyongru
- **Commit:** 2a3d29ce73bb7649faba089aba23e351fed3e67f
### fix(webui): keep saved topics bound to their project (#6509)
- **Date:** 2026-10-28
- **Author:** chengyongru
- **Commit:** 4a14faa47e9af06a66968cb59f5b5d46754dc6fe
### fix(build): fetch locked WebUI packages from npm registry
- **Date:** 2026-10-28
- **Author:** Xubin Ren
- **Commit:** 8f7a7d17590de7ab187650381894dba2b9e060ab
... and more (showing recent 20 commits)

## Recent Releases

### v0.4.0
- **Date:** 2026-10-28
- **Description:** nanobot v0.4.0
### v0.3.5
- **Date:** 2026-09-16
- **Description:** nanobot v0.3.5
### v0.3.0
- **Date:** 2026-07-25
- **Description:** nanobot v0.3.0 - The Agency Release
### v0.2.2
- **Date:** 2026-06-22
- **Description:** v0.2.2
### v0.2.1
- **Date:** 2026-06-01
- **Description:** v0.2.1

## Documentation Updates

- **docs/configuration.md** - Updated: 2026-10-10
- **docs/providers.md** - Updated: 2026-10-10
- **COMMUNICATION.md** - Updated: 2026-10-30
- **README.md** - Updated: 2026-10-30
- **docs/architecture.md** - Updated: 2026-10-29
- **docs/cli-reference.md** - Updated: 2026-10-29
- **docs/releases/0.4.0.md** - Updated: 2026-10-29
- **docs/releasing.md** - Updated: 2026-10-29
- **docs/chat-apps.md** - Updated: 2026-10-28
- **docs/channel-package-guide.md** - Updated: 2026-10-29
- **docs/release-archive.md** - Updated: 2026-10-28
- **.agent/design.md** - Updated: 2026-10-27
- **docs/webui.md** - Updated: 2026-10-28
- **tui/README.md** - Updated: 2026-10-28
- **nanobot/skills/update-setup/SKILL.md** - Updated: 2026-10-28
- **CONTRIBUTING.md** - Updated: 2026-10-27
- **.agent/gotchas.md** - Updated: 2026-10-26
- **docs/my-tool.md** - Updated: 2026-10-26
- **nanobot/skills/my/SKILL.md** - Updated: 2026-10-26
- **nanobot/skills/my/references/examples.md** - Updated: 2026-10-26
- **webui/COMPONENTS.md** - Updated: 2026-10-25
- **docs/websocket.md** - Updated: 2026-10-25
- **docs/automations.md** - Updated: 2026-10-20
- **nanobot/skills/cron/SKILL.md** - Updated: 2026-10-20
- **tui/RELINKING.md** - Updated: 2026-10-24
