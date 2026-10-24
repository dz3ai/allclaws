# AllClaws 项目状态 — 2026-10-18

## 总览
- 仓库: dz3ai/allclaws (GitHub)
- 平台数: **34** (11 Claw + 17 External + 5 CLI + 1 Digital Twin)
- 最近提交: `087e365` — report: exclude codex from this grid (per decision; protocol-incompatible)
- 分支: main
- 本周动作: **三轮重试后 23/29 子模块完成同步** (15 个指针前进, 共吸收 ~4,400 个上游提交), 6 个大仓库因链路限速 (~20KiB/s) 无法在 15 分钟 fetch 预算内完成

## 本周活动 (2026-10-12 → 10-18, 周日) — 子模块同步 + 周报
**子模块指针更新 (15/29, 共 ~4,400 个上游提交):**

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
| codex | (voice-*) → +1152 | 1152 | 本周 223 提交; feature-flag 纪律 (zstd WebSocket 压缩/唤醒空闲会话均门控); 模型目录缓存跨凭证轮换保留 |
| praisonai | v4.7.10 → v4.7.15 | 1053 | 近日更; #5872 外来源工作的独立安全层; frecency 排序补全 |
| dify | 1.17.1 → 1.17.1+709 | 709 | 严格类型测试改造延续 anti-mock 路线; 归档删除失败重试而非谎报成功; MCP union 类型 list 参数修复 |
| nanobot | v0.3.5 → v0.3.5+412 | 412 | 本周 103 提交; WebUI 冲刺 (侧栏 topic 内联重命名); 假绿测试→行为覆盖 (#6282) |
| kimi-code | @2.0.2 → @2.1.1 | 72 | /reload 通知外部变更; remote-control 分块流式 100 MiB; dangerous-command guard 策略化开关 |
| rocketride-server | client-ts-v1.0.2 → client-mcp-v1.5.0-pre | 98 | server 3.5.0 / clients 1.5.0 (10-16); rocketride_vector 暴露为 agent 工具 (写默认关闭) |

**已 fetch 但无新提交 (8):** ironclaw, maxclaw, kimi-cli, aider, clawteam, claw-ai-lab, metagpt, qwen-agent — 保持原指针。

**同步受阻 (6/29, 三轮重试未果):** openclaw, eliza, hermes-agent, zeroclaw, reasonix, openhuman — 增量过大 (codex 单仓 1152 提交在 15 分钟内可完成, 但此 6 仓库 pack 更大), 指针保持在 10-06 快照。下周单独长超时重试。

**本周新发布 (10-11 → 10-18, 已同步仓库):** agentscope v2.0.10, agent-zero v2.14, browser-use 0.13.12/0.13.13, copilot-cli 1.0.99/1.0.100, hiclaw v1.2.5, goclaw beta.229, praisonai v4.7.13-15, rocketride server 3.5.0/clients 1.5.0 — 共 12+ 个 tag/发布。

**关键观察:**
- **hiclaw v1.2.5 是本周含金量最高的发布** — QwenPaw 原地运行时升级 (两阶段编排器 + 回滚), controller 经 container exec 管理任意厂商 coding CLI (runtime-agnostic)
- **agentscope 解锁 mcp 2.x** — 去掉 `mcp<2.0.0` 版本钉是 MCP 生态大版本迁移的先行信号
- **codex 的 feature-flag 纪律** — zstd WebSocket 压缩、agent 消息唤醒空闲会话全部门控上线 (ship-dark, enable-when-ready)
- **诚实失败上报成为跨生态主题** — dify 归档删除重试、goclaw StopFlusher 幂等、nanoclaw 修复回复丢失、browser-use 重连清理顺序
- **praisonai #5872** — 个人项目率先引入外来源工作的独立 CI 安全层 (供应链治理前置)
- **openworker 10-17 单日合并 8+ 社区 PR** — provider 元数据 (context window/vision 能力) 追赶模型发布节奏成为外部框架的持续负担

## 已完成 (本周新增)
30. ✅ **15 子模块指针同步** — 第一轮 9 个 + 重试轮 6 个 (codex/praisonai/dify/nanobot/kimi-code/rocketride) (10-18)
31. ✅ **本周亮点周报** — `_posts/2026-10-18-weekly-highlights-oct-week3.md` (10-18)

## ROADMAP 进度 (H2 2026)
**10/12 完成** — Q4 剩余 3 项:
- 🟡 Q4-4 Long-Running Agent Benchmarks — Phase 3 进行中 (上周: hermes 接入, 4/4 solved; codex 网格排除)
- 🟡 Q4-5 Protocol Wars (MCP vs A2A) — 未启动 (agentscope mcp 2.x 解钉是相关信号)
- 🟡 Q4-6 Platform Governance Thresholds — 未启动

## 进行中 / 待完成
1. 🟡 **6 个子模块同步推迟** — openclaw, eliza, hermes-agent, zeroclaw, reasonix, openhuman; 增量过大 + 链路限速, 指针停在 10-06; 下周单独长超时重试
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
