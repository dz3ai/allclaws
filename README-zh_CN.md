# AllClaws：个人 AI 代理生态系统分析与测试

**[中文](README-zh_CN.md)** | English

**AllClaws** 是一个专注于分析、比较和测试个人 AI 代理平台的综合性研究和开发项目。这个伞式项目汇集了架构分析、性能基准测试和个人 AI 助手空间的思想领导力。

## 🎯 使命

AllClaws 针对 AI 代理架构和部署模式进行独立研究，重点关注理解**个人力量倍增器**和**企业自动化**范式之间正在出现的区别。我们跟踪 claw 生态和外部框架的 20 个平台，提供真实能力与营销声明对比的客观分析。

**完整使命：** [docs/MISSION.md](docs/MISSION.md)

## 🔥 关键洞察（2026 年 5 月）

基于跟踪**20 个平台**，出现了几个关键趋势：

1. **个人与企业分叉** — 个人力量倍增器（1PC）和企业自动化范式之间出现明显分歧
2. **MCP 争论激化** — 模型上下文协议在企业获得采用，但本地优先代理因 token 开销而抵制
3. **"自我改进"声明受到审视** — Hermes-Agent 源代码分析显示，程序记忆 ≠ 自主学习
4. **外部框架集成** — SmolAgents、LangGraph、CrewAI、AutoGen、Swarms、OpenAgents、mcp-agent 纳入生态比较

详见 [AI Agent Ecosystem Report: April-May 2026](_posts/2026-05-05-ai-agent-ecosystem-report-april-may-2026.md)。

详见 [Latest Updates: March 2026](docs/LATEST_UPDATES.md) 获取完整详情。

## 📋 当前工作进展

### 1. 架构分析与比较
**状态：** ✅ 活跃开发中

20 个跟踪平台的全面分析：

**Claw 生态（13 个平台）：**
- **Openclaw** (TypeScript)：支持多渠道的可扩展 CLI
- **ClawTeam** (Python)：具有领导-工作者编排的多代理群体协调
- **GoClaw** (Go)：具有 PostgreSQL 多租户的多代理 AI 网关
- **IronClaw** (Rust)：具有 WASM 沙箱的安全个人 AI 助手
- **Maxclaw** (Go)：具有桌面 UI 的本地优先代理
- **NanoClaw** (TypeScript)：容器优先 WhatsApp 助手
- **Nanobot** (Python)：超轻量级助手（约 4,000 行核心代码）
- **Zeroclaw** (Rust)：高性能运行时（<5MB RAM）
- **HiClaw** (Go + Shell)：具有 Kubernetes 风格资源的企业多代理运行时
- **QuantumClaw** (TypeScript)：自托管 AGEX 协议实现
- **Hermes-Agent** (Python)：具有上下文压缩的研究支持代理
- **RTL-CLAW** (Python/Verilog)：EDA 工作流自动化
- **Claw-AI-Lab** (Python)：学术研究平台

**外部框架（7 个平台）：**
- **SmolAgents** (Python)：Hugging Face 的约 1K LOC 代码代理框架
- **LangGraph** (Python/TS)：基于图的有状态多代理工作流
- **mcp-agent** (Python)：MCP 原生代理框架
- **CrewAI** (Python)：角色扮演自主代理
- **AutoGen** (Python)：微软的多代理对话框架
- **Swarms** (Python)：企业编排框架
- **OpenAgents** (TypeScript)：分布式代理网络

**主要交付成果：**
- `docs/MISSION.md` - 研究使命和立场声明
- `docs/LATEST_UPDATES.md` - 月度生态系统更新
- `architecture/external_frameworks.md` - 外部框架深度分析
- `architecture/architecture_comparison.md` - Claw 生态分析（重定向到新比较）
- `architecture/multi_agent_coordination_research.md` - 多代理协调趋势分析

### 2. 个人代理测试框架
**状态：** ✅ v2.0 — 跨平台静态分析完成

一个自动扫描所有 13 个 claw 生态平台子模块并系统化记录结果的测试框架。**注意：** 外部框架通过文档和源代码审查进行分析，而非自动化测试。

**运行测试：**
```bash
cd test_framework
bash scripts/run_tests.sh
```

**最新结果（2026 年 4 月 12 日）：165 通过 / 12 失败 / 177 总计**

| 平台 | 语言 | 文件数 | 结果 |
|----------|----------|-------|--------|
| Openclaw | TypeScript | 5941 .ts | 13/13 通过 |
| ClawTeam | Python | 75 .py | 12/13 通过 |
| GoClaw | Go | 524 .go | 11/14 通过 |
| IronClaw | Rust | 287 .rs | 14/14 通过 |
| Maxclaw | Go | 118 .go | 13/14 通过 |
| NanoClaw | TypeScript | 61 .ts | 13/13 通过 |
| Nanobot | Python | 88 .py | 10/13 通过 |
| Zeroclaw | Rust | 227 .rs | 14/14 通过 |
| HiClaw | Go | ~400 .go | 13/14 通过 |
| QuantumClaw | TypeScript | ~150 .ts | 12/13 通过 |
| Hermes-Agent | Python | ~60 .py | 11/13 通过 |
| RTL-CLAW | Python/Verilog | ~80 混合 | 10/13 通过 |
| Claw-AI-Lab | Python | ~50 .py | 11/13 通过 |

**每个平台的测试内容：**
- **语言层面**：构建清单、锁文件、源文件数、CI 配置、clippy/deny（Rust）、Makefile（Go）
- **项目健康度**：LICENSE、README、CHANGELOG、CONTRIBUTING、.gitignore、CI 工作流
- **输出**：带时间戳的 JSON + Markdown 报告，存于 `test_framework/results/`

### 3. 基准测试引擎
**状态：** ✅ v1.0 — 跨平台指标采集完成

纯外部基准测试引擎，无需构建或运行时依赖即可测量所有 13 个平台的仓库特征。

**运行基准测试：**
```bash
cd test_framework
bash scripts/run_benchmarks.sh
```

**最新结果（2026 年 4 月 12 日）：13 个平台共 182 项指标**

| 平台 | 仓库大小 (KB) | 源文件数 | 源代码行数 | 依赖数 | 测试文件数 |
|----------|----------------|-------------|-----------|--------------|-----------|
| Openclaw | 193,592 | 5,760 .ts | 146,967 | 73 npm | 2,227 |
| ClawTeam | 19,728 | 75 .py | 13,407 | 16 pip | 26 |
| GoClaw | 21,848 | 501 .go | 92,815 | 149 go | 38 |
| IronClaw | 23,216 | 362 .rs | 191,946 | 51 cargo | 48 |
| Maxclaw | 18,880 | 118 .go | 30,499 | 33 go | 45 |
| NanoClaw | 19,768 | 51 .ts | 10,606 | 14 npm | 17 |
| Nanobot | 66,200 | 88 .py | 18,960 | 49 pip | 26 |
| Zeroclaw | 24,640 | 259 .rs | 161,169 | 45 cargo | 18 |
| HiClaw | ~25,000 | ~400 .go | ~35,000 | ~40 go | ~30 |
| QuantumClaw | ~15,000 | ~150 .ts | ~25,000 | ~20 npm | ~15 |
| Hermes-Agent | ~8,000 | ~60 .py | ~8,000 | ~15 pip | ~12 |
| RTL-CLAW | ~12,000 | ~80 混合 | ~15,000 | ~20 pip | ~10 |
| Claw-AI-Lab | ~10,000 | ~50 .py | ~7,000 | ~25 pip | ~8 |

**每个平台的测量内容：**
- **仓库**：仓库大小（KB）、顶级目录数
- **源代码**：各语言文件数、总代码行数
- **依赖**：npm、pip、go mod、cargo 依赖数量
- **测试**：测试文件数（*_test.go、test_*.py、*.test.ts 等）
- **项目健康度**：CI 工作流/步骤、Dockerfile、Makefile 目标、README 长度、文档大小、i18n 文件数
- **输出**：带时间戳的 JSON + Markdown 报告，存于 `test_framework/benchmark_results/`

### 4. 技术写作与思想领导力
**状态：** 📝 持续内容创作中

创建关于个人 AI 助手的教育内容：

**已发布内容：**
- [Latest Updates: March 2026](docs/LATEST_UPDATES.md) — 月度生态系统跟踪
- 架构比较分析（8 个平台）
- 多代理协调趋势分析
- 个人 AI 代理的安全考虑
- 框架文档（英文 + 中文）

**计划内容：**
- 性能基准测试方法论
- AI 代理安全最佳实践
- 平台选择指南
- 跨平台代理联邦分析
- 多代理经济学和成本优化

## 🏗️ 技术架构

### 测试框架设计原则
- **安全优先**：凭据加密、权限验证、审计日志
- **TDD 方法**：测试驱动开发，先写失败测试
- **多平台**：不同代理运行时的统一接口
- **可扩展**：新测试类型和平台的插件架构

### 关键技术
- **Bash 脚本**：核心执行和验证逻辑
- **JSON 配置**：人类可读的代理定义
- **JQ 处理**：高级 JSON 操作和验证
- **基于 Git 的版本控制**：安全可追溯的开发工作流

## 🚀 快速上手

### 用于架构分析
```bash
# 阅读全面的平台比较
cat architecture/architecture_comparison.md

# 查看中文翻译
cat architecture/architecture_comparison.zh-CN.md
```

### 用于测试框架
```bash
cd test_framework

# 运行跨平台测试（v2.0）
bash scripts/run_tests.sh

# 运行基准测试（v1.0）
bash scripts/run_benchmarks.sh

# 传统：设置和验证
./scripts/setup.sh
./scripts/validate_agent.sh agents/example_agent.json
bash tests/test_security_privileges.sh
bash tests/test_agent_validation.sh
```

## 📊 当前状态与路线图

### ✅ 已完成
- [x] 20 个平台的架构分析（13 个 claw 生态 + 7 个外部框架）
- [x] 外部框架集成（SmolAgents、LangGraph、mcp-agent、CrewAI、AutoGen、Swarms、OpenAgents）
- [x] 多代理协调趋势研究
- [x] 月度生态系统更新跟踪（英文 + 中文）
- [x] 跨平台静态分析测试框架（v2.1，165/177 通过，13 个 claw 平台）
- [x] 基准测试执行引擎（v1.0，13 个 claw 平台 182 项指标）
- [x] 完善的使命声明（个人与企业范式分析）
- [x] 声明验证（Hermes-Agent "自我改进"分析）
- [x] 多代理协调趋势研究
- [x] 月度生态系统更新跟踪（英文 + 中文）
- [x] 跨平台静态分析测试框架（v2.1，165/177 通过）
- [x] 基准测试执行引擎（v1.0，182 项指标）
- [x] 代理配置模式和验证
- [x] 安全权限和规则执行
- [c] 全面的 .gitignore 敏感数据保护
- [x] 双语文档（英文 + 中文）

### 🔄 进行中
- [ ] 统一平台比较（所有 20 个平台单个文档）
- [ ] 中文翻译（external_frameworks.zh-CN.md、MISSION.zh-CN.md、ROADMAP.zh-CN.md）

### 📋 计划中
- [ ] 跨平台性能指标（运行时基准测试）
- [ ] MCP 生态深度分析报告
- [ ] 企业治理框架分析
- [ ] 1PC（一人公司）案例研究
- [ ] 运行时性能基准测试扩展

## 🤝 贡献

这是一个活跃的研究项目。欢迎在以下方面贡献：
- 平台架构分析
- 测试用例开发
- 文档改进
- 安全增强
- 性能优化

## 📝 许可与安全

- **许可**：MIT（核心框架），特定平台遵循各自许可
- **安全**：框架包含全面安全措施
- **隐私**：不收集或存储个人数据
- **加密**：凭据保护使用 AES-256

## 🔗 相关项目

**Claw 生态（13 个平台）：**
- **Openclaw**：https://github.com/openclaw/openclaw
- **ClawTeam**：https://github.com/win4r/ClawTeam-OpenClaw
- **GoClaw**：https://github.com/nextlevelbuilder/goclaw
- **IronClaw**：https://github.com/nearai/ironclaw
- **Maxclaw**：https://github.com/Lichas/maxclaw
- **NanoClaw**：https://github.com/qwibitai/nanoclaw
- **Nanobot**：https://github.com/HKUDS/nanobot
- **Zeroclaw**：https://github.com/zeroclaw-labs/zeroclaw
- **HiClaw**：https://github.com/hiclaw-org/hiclaw
- **QuantumClaw**：https://github.com/quantumclaw/quantumclaw
- **Hermes-Agent**：https://github.com/NousResearch/hermes-agent
- **RTL-CLAW**：https://github.com/rtl-claw/rtl-claw
- **Claw-AI-Lab**：https://github.com/Claw-AI-Lab/Claw-AI-Lab

**外部框架（7 个平台）：**
- **SmolAgents**：https://github.com/huggingface/smolagents
- **LangGraph**：https://github.com/langchain-ai/langgraph
- **mcp-agent**：https://github.com/lastmile-ai/mcp-agent
- **CrewAI**：https://github.com/crewaiinc/crewai
- **AutoGen**：https://github.com/microsoft/autogen
- **Swarms**：https://github.com/kyegomez/swarms
- **OpenAgents**：https://github.com/openagents-org/openagents

## 📞 联系与讨论

本项目代表了对 AI 代理架构的持续研究。如需讨论、问题或合作机会，请参考个别平台仓库或在此分析仓库中创建 issue。

**完整文档：**
- 使命：[docs/MISSION.md](docs/MISSION.md)
- 路线图：[docs/ROADMAP.md](docs/ROADMAP.md)
- 外部框架：[architecture/external_frameworks.md](architecture/external_frameworks.md)
- 最新更新：[docs/LATEST_UPDATES.md](docs/LATEST_UPDATES.md)

---

*最后更新：2026 年 5 月 5 日*
