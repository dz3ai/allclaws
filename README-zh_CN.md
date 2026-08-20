# AllClaws：个人 AI 代理生态系统分析与测试

**[中文](README-zh_CN.md)** | English

**AllClaws** 是一个专注于分析、比较和测试个人 AI 代理平台的综合性研究和开发项目。这个伞式项目汇集了架构分析、性能基准测试和个人 AI 助手空间的思想领导力。

## 🎯 使命

AllClaws 针对 AI 代理架构和部署模式进行独立研究，重点关注理解**个人力量倍增器**和**企业自动化**范式之间正在出现的区别。我们跟踪 claw 生态和外部框架的 35 个平台，提供真实能力与营销声明对比的客观分析。

**完整使命：** [docs/MISSION.md](docs/MISSION.md)

## 🗂️ 跟踪范围

**35 个 Tier-1 平台**，分四个类别（另有 7 个 harness 生态，见[治理规则](docs/governance.zh-CN.md)）：

**Claw 生态（11 个）：** OpenClaw、ClawTeam、GoClaw、IronClaw、Maxclaw、NanoClaw、Nanobot、ZeroClaw、HiClaw、Hermes-Agent、Claw-AI-Lab

**外部框架（18 个）：** SmolAgents、LangGraph、CrewAI、AutoGen、Swarms、OpenAgents、OpenFang、kimi-code、AgentScope、Eliza、Agent Zero、PraisonAI、Rocketride、OpenWorker、Dify、MetaGPT、Qwen-Agent、browser-use

**CLI 编程代理（5 个）：** aider、copilot-cli、reasonix、kimi-cli、codex

**人类数字孪生（1 个）：** openhuman

各平台仓库地址见 [architecture/platform_comparison.zh-CN.md](architecture/platform_comparison.zh-CN.md) —— 覆盖全部 35 个平台的权威比较文档（中英文）。

## 🔥 关键洞察

1. **个人与企业分叉** — 个人力量倍增器（1PC）和企业自动化范式之间出现明显分歧
2. **MCP 争论激化** — 模型上下文协议在企业获得采用，但本地优先代理因 token 开销而抵制
3. **"自我改进"声明受到审视** — Hermes-Agent 源代码分析显示，程序记忆 ≠ 自主学习
4. **协议分层而非战争** — MCP 占据工具层（13 个实现），ACP 占据 client↔agent 层（5 个实现），A2A 占据发现层（1 个生产实现）；厂商私有 API 仍是默认
5. **进化式 Harness 架构** — HarnessX（arXiv:2606.14249）将 harness 形式化为一等可进化对象

> 📊 **最新生态动态、平台逐项详情与对比总览表见 [docs/LATEST_UPDATES.zh-CN.md](docs/LATEST_UPDATES.zh-CN.md)**（每月刷新，中英文）。

## 📋 当前工作

### 1. 架构分析与比较 — ✅ 活跃
全部 35 个跟踪平台的统一比较：分类、核心架构、mermaid 图和 5 个对比矩阵。
- [architecture/platform_comparison.zh-CN.md](architecture/platform_comparison.zh-CN.md) — 权威文档，中英文
- [architecture/agent_harnesses.md](architecture/agent_harnesses.md) — harness 生态与工具链
- [architecture/multi_agent_coordination_research.md](architecture/multi_agent_coordination_research.md) — 协调趋势分析

### 2. 测试框架 — ✅ v2.1
覆盖 11 个 claw 生态子模块的静态分析（语言层 + 项目健康度检查）。
```bash
cd test_framework
bash scripts/run_tests.sh
```

### 3. 基准测试引擎 — ✅ v3.0 Python
26 个平台 140 项运行时指标：冷启动、内存、延迟、二进制大小（N=5 采样 + 统计分析）。
```bash
cd test_framework
python3 -m benchmark.cli runtime --runs 5
python3 -m benchmark.cli static
python3 -m benchmark.cli report --last 5 --regression 20
```

### 4. 研究报告 — ✅ 持续
超越编目的调查研究——代理如何失败、互操作和被治理。核心报告：
- 代理失败模式分类（35 个平台 13 种模式）— [docs/reports/failure-mode-taxonomy-2026.md](docs/reports/failure-mode-taxonomy-2026.md)
- 中国 AI 代理生态（14 个项目）— [docs/reports/china-agent-ecosystem-2026.md](docs/reports/china-agent-ecosystem-2026.md)
- 协议之争（MCP/ACP/A2A）— [docs/reports/protocol-wars-2026.md](docs/reports/protocol-wars-2026.md)
- MCP 生态深度分析（5 个阶段）— [docs/reports/mcp-deep-dive-phase4-5-synthesis.md](docs/reports/mcp-deep-dive-phase4-5-synthesis.md)
- 完整索引：[docs/reports/](docs/reports/)

### 5. 技术写作与思想领导力 — 📝 持续
- [`_posts/`](_posts/) 月度生态报告（中英文）
- [最新进展](docs/LATEST_UPDATES.zh-CN.md) — 每月平台逐项跟踪

## 📊 当前状态与路线图

H2 2026 研究计划：**13 项已完成 12 项**。仅剩 Q4-4（长时运行代理基准测试）。

### ✅ 已完成（精选）
- [x] 35 个平台的架构分析（11 claw + 18 外部框架 + 5 CLI 编程代理 + 1 人类数字孪生）
- [x] 统一平台比较（全部 35 个平台，中英文）
- [x] 基准引擎 v3.0（26 平台 140 项运行时指标）+ CI 集成
- [x] MCP 生态深度分析（5 阶段）与企业治理框架分析
- [x] 代理失败模式分类（35 个平台 13 种失败模式）
- [x] 中国生态深度分析 → 新增 Dify、MetaGPT、Qwen-Agent；browser-use（#35，首个 computer-use 代表）
- [x] 协议之争分析（Q4-5）——分层而非战争
- [x] 平台治理（Q4-6）——三层跟踪模型、Tier-1 上限 35
- [x] 品类覆盖缺口闭合（Q4-7）——browser-use 入选，评估 6 个候选

### 🔄 进行中（H2 2026）
- [ ] Q4-4：长时运行代理基准测试（端到端任务评估，30+ 分钟任务）

### 📋 计划中（H1 2027 预览）
- [ ] 代理经济学——超越 API 定价的真实成本模型
- [ ] 多代理编排模式
- [ ] 多代理经济学与成本优化
- [ ] 代理安全与供应链分析

**完整路线图：** [docs/ROADMAP.zh-CN.md](docs/ROADMAP.zh-CN.md)

## 🚀 快速上手

```bash
# 阅读全面的平台比较
cat architecture/platform_comparison.zh-CN.md

# 运行测试和基准
cd test_framework
bash scripts/run_tests.sh
python3 -m benchmark.cli runtime --runs 5
```

## 🤝 贡献

这是一个活跃的研究项目。欢迎在以下方面贡献：
- 平台架构分析
- 测试用例开发
- 文档改进
- 声明验证研究

## 📝 许可与安全

- **许可**：MIT（核心框架），特定平台遵循各自许可
- **隐私**：不收集或存储个人数据

## 🔗 相关项目

- **兄弟仓库**：[dz3ai/coder_arena](https://github.com/dz3ai/coder_arena) — AI 编程代理子模块（仅编程代理，无博客）
- 全部 35 个平台地址：[architecture/platform_comparison.zh-CN.md](architecture/platform_comparison.zh-CN.md)
- 研究报告索引：[docs/reports/](docs/reports/)

## 📞 联系与讨论

如需讨论、问题或合作机会，请参考个别平台仓库或在此分析仓库中创建 issue。

**完整文档：**
- 使命：[docs/MISSION.zh-CN.md](docs/MISSION.zh-CN.md)
- 路线图：[docs/ROADMAP.zh-CN.md](docs/ROADMAP.zh-CN.md)
- 治理：[docs/governance.zh-CN.md](docs/governance.zh-CN.md)
- 最新进展：[docs/LATEST_UPDATES.zh-CN.md](docs/LATEST_UPDATES.zh-CN.md)

---

*最后更新：2026 年 8 月 20 日*
