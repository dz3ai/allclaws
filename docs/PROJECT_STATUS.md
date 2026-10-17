# AllClaws 项目状态 — 2026-10-18

## 总览
- 仓库: dz3ai/allclaws (GitHub)
- 平台数: **34** (11 Claw + 17 External + 5 CLI + 1 Digital Twin)
- 最近提交: `087e365` — report: exclude codex from this grid (per decision; protocol-incompatible)
- 分支: main
- 本周动作: **9 个子模块同步至最新** (901 个上游新提交), 其余 20 个因网络超时推迟

## 本周活动 (2026-10-12 → 10-18, 周日) — 子模块同步 + 周报
**子模块指针更新 (9/29, 共 901 个上游提交):**

| 子模块 | 旧 → 新 | Δ 提交 | 本周关键动态 |
|--------|---------|--------|--------------|
| agentscope (+mirror) | v2.0.8-66 → v2.0.10 | 128 | v2.0.10 发布 (10-12); mcp 2.x SDK 支持 (解除 mcp<2.0.0 锁定); ASR 转写接口 |
| agent-zero | v2.12 → v2.14 | 156 | v2.13/v2.14 发布 (10-13); Venice 缓存路由; ARM64 Xpra 签名包 |
| browser-use | 0.13.1-591 → 0.13.13 | 91 | 0.13.12/13 同日发布 (10-15); 浏览器重连清理; OpenAI 观测恢复 |
| copilot-cli | v1.0.88 → v1.0.100-0 | 11 | 突破 1.0.100 (10-14, 4 个 tag); 公开仓库仍仅见 changelog |
| openworker | v0.2.1-118 → v0.3.4 | 284 | 10-17 社区 PR 合并潮: Qwen3.8 Max GA id, DeepSeek V4 Pro 1,040,000 ctx |
| goclaw | beta.213 → beta.229 | 42 | 17 个 beta tag; beta.229 (10-17) 修复 StopFlusher 幂等 |
| hiclaw | v1.2.4-4 → v1.2.5 | 51 | v1.2.5 + Dashboard v1.3.1 (10-17); QwenPaw 两阶段原地升级+回滚; Node 22→24 |
| nanoclaw | v2.3.0-205 → v2026.10.0 | 138 | CalVer 首个稳定版 v2026.10.0; 审批卡线程修复; 清理 11 个 dev 依赖告警 |

**同步受阻 (20/29):** openclaw, hermes-agent, codex, reasonix, eliza, zeroclaw, dify, nanobot, ironclaw, maxclaw, nanobot 等 — GitHub 网络超时 (大仓库 fetch >90s×多轮均未完成), 指针保持在 10-06 快照。下周重试。

**本周新发布 (10-11 → 10-18, 已同步仓库):** agentscope v2.0.10, agent-zero v2.14, browser-use 0.13.12/0.13.13, copilot-cli 1.0.99/1.0.100, hiclaw v1.2.5, goclaw beta.229 — 共 9+ 个 tag。

**关键观察:**
- **hiclaw v1.2.5 是本周含金量最高的发布** — QwenPaw 原地运行时升级 (两阶段编排器 + 回滚), controller 经 container exec 管理任意厂商 coding CLI (runtime-agnostic)
- **agentscope 解锁 mcp 2.x** — 去掉 `mcp<2.0.0` 版本钉是 MCP 生态大版本迁移的先行信号
- **openworker 10-17 单日合并 8+ 社区 PR** — provider 元数据 (context window/vision 能力) 追赶模型发布节奏成为外部框架的持续负担
- **nanoclaw 完成版本体系切换** — semver → CalVer 后首个稳定版落地

## 已完成 (本周新增)
30. ✅ **9 子模块指针同步** — agentscope, agent-zero, browser-use, copilot-cli, openworker, goclaw, hiclaw, nanoclaw (+agentscope mirror) (10-18)
31. ✅ **本周亮点周报** — `_posts/2026-10-18-weekly-highlights-oct-week3.md` (10-18)

## ROADMAP 进度 (H2 2026)
**10/12 完成** — Q4 剩余 3 项:
- 🟡 Q4-4 Long-Running Agent Benchmarks — Phase 3 进行中 (上周: hermes 接入, 4/4 solved; codex 网格排除)
- 🟡 Q4-5 Protocol Wars (MCP vs A2A) — 未启动 (agentscope mcp 2.x 解钉是相关信号)
- 🟡 Q4-6 Platform Governance Thresholds — 未启动

## 进行中 / 待完成
1. 🟡 **20 个子模块同步推迟** — 网络超时, 指针停在 10-06; 下周优先重试 (openclaw/dify/eliza 为最大仓库, 需单独长超时)
2. 🟡 Q4-4/5/6 — 见 ROADMAP
3. 🟢 工作区干净 (本次同步提交后)
4. 🟢 CI 未在本轮查询 (上次 08-01 全绿)

## 关键文件
- test_framework/config.json — 34 platforms 配置
- .github/workflows/benchmark-suite.yml — CI workflow (Mon-Fri daily, Sat weekly, Sun submodule updates)
- architecture/platform_comparison.md — 平台对比矩阵
- docs/ROADMAP.md — 路线图 (10/12 完成)
- docs/LATEST_UPDATES.md — 最新动态
- docs/PROJECT_STATUS.md — 本文件
- _posts/2026-10-18-weekly-highlights-oct-week3.md — 本周亮点周报

## 工具链
- Go: ~/local/go/bin
- Python: system 3.12
- Node: system (v25.8.0)
- Rust: 1.95.0

## CI 状态（总览）
- Benchmark Suite: ✅ green (上次查询 #30704412369, 2026-08-01; 本轮未查询)
- Agent Platform Tests: ✅ green (上次查询 #30704412352, 2026-08-01; 本轮未查询)
- Deploy Jekyll: ✅ green (上次查询 #30704412354, 2026-08-01; 本轮未查询)
