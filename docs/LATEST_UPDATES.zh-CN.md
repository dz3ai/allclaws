# 最新进展：个人 AI 代理生态系统（2026 年 4-5 月）

**[English](LATEST_UPDATES.md)** | 中文

> 追踪 11 个 claw 生态平台、18 个外部框架、5 个 CLI 编程代理和 1 个人类数字孪生平台的重大更新 — 架构革新、MCP 采用争论、企业 vs 个人模式、安全发展（2026 年 4-8 月）。

---

## 本月趋势

2026 年 4-5 月呈现了塑造生态系统的四大趋势：

1. **MCP 争论激化** — 模型上下文协议在企业获得采用（IronClaw、GoClaw、ZeroClaw），但本地优先代理（NanoClaw）因 20-30% 的 token 开销而抵制
2. **"自我改进"声明受质疑** — Hermes-Agent 源代码分析揭示程序记忆 ≠ 自主学习；这一区别现在被广泛认可
3. **企业 vs 一人公司分叉** — 企业自动化（治理、云、MCP）与个人力量倍增器（速度、本地、CLI）模式之间出现明显分歧
4. **外部框架纳入跟踪** — SmolAgents、LangGraph、CrewAI、AutoGen、Swarms、OpenAgents、OpenFang、AgentScope、Eliza、Agent Zero、PraisonAI、Rocketride 加入生态系统比较
5. **Agent 框架类别添加** — UltraWorkers 工具链（claw-code、oh-my-codex、clawhip、oh-my-openagent）被认可为独特的基础设施层
6. **CLI 编程代理添加** — aider（约 68K 星，git 感知 AI 结对编程）、copilot-cli（GitHub Copilot 终端代理）、reasonix（DeepSeek 原生编程代理，约 11.3K 星）作为新类别添加
7. **人类数字孪生添加** — openhuman（Rust，人类数字孪生）作为学术/研究平台添加
8. **MoonshotAI 平台添加** — kimi-cli（Python，CLI 编程代理，约 8.8K 星，ACP 支持）和 kimi-code（TypeScript，下一代代理框架，约 1.4K 星，MCP + 插件架构）添加
9. **AgentScope 添加** — AgentScope（Python，阿里巴巴达摩院，约 25.8K 星）作为第 9 个外部框架添加；分布式多代理协作，消息中心和管道工作流
10. **Eliza 添加** — Eliza（TypeScript，eliza-os，MIT）作为第 10 个外部框架添加；多平台 AI 代理框架，插件架构
11. **Agent Zero 添加** — Agent Zero（Python，frdel，MIT）作为第 11 个外部框架添加；自主 AI 代理框架，具备工具使用能力
12. **PraisonAI 添加** — PraisonAI（Python，MervinPraison，MIT）作为第 12 个外部框架添加；多代理 LLM 框架，低代码工作流构建器
13. **Rocketride 添加** — Rocketride（TypeScript，nearai，MIT）作为第 13 个外部框架添加；near.ai 代理服务器，自主任务执行
14. **browser-use 添加（2026 年 8 月）** — browser-use（Python，MIT，约 11 万星）作为第 18 个外部框架、第 35 号平台添加；依据治理 Q4-7 裁决成为首个计算机操作（浏览器）类别代表。Chromium CDP 代理循环、类型化动作 schema，以 MCP server 形态发布
15. **Harness 生态扩张（2026 年 8 月）** — DeepSeek Harness（dsh，首个厂商一方 harness，基于 Cordis 插件树组合）与 Pi（Earendil Works，自扩展 harness）作为 harness 生态 #6-7 添加；Pi 列 Tier 2，dsh 待 1.0 前列 Tier 3

---

## 研究里程碑（H2 2026）

平台跟踪之外的已完成研究——完整路线图状态见 [ROADMAP.zh-CN.md](ROADMAP.zh-CN.md)（13 项已完成 12 项）：

- [x] MCP 生态深度分析（5 个阶段）— [reports/mcp-deep-dive-phase4-5-synthesis.md](reports/mcp-deep-dive-phase4-5-synthesis.md)
- [x] 企业治理框架分析 — [reports/enterprise-governance-analysis.md](reports/enterprise-governance-analysis.md)
- [x] 1PC（一人公司）案例研究 — [reports/1pc-case-studies-2026.md](reports/1pc-case-studies-2026.md)
- [x] 代理失败模式分类（35 个平台 13 种失败模式）— [reports/failure-mode-taxonomy-2026.md](reports/failure-mode-taxonomy-2026.md)
- [x] 中国 AI 代理生态深度分析（14 个项目，35 万+ 累计星标）— [reports/china-agent-ecosystem-2026.md](reports/china-agent-ecosystem-2026.md)
- [x] Harness 工程对比 — [reports/harness-engineering-comparison.md](reports/harness-engineering-comparison.md)
- [x] 协议之争分析（Q4-5）— MCP/ACP/A2A 分层而非战争 — [reports/protocol-wars-2026.md](reports/protocol-wars-2026.md)
- [x] 平台治理与质量门槛（Q4-6）— 三层跟踪模型、Tier-1 上限 35 — [governance.zh-CN.md](governance.zh-CN.md)
- [x] 品类覆盖缺口闭合（Q4-7）— 评估 6 个候选，browser-use 以 #35 入选（首个 computer-use 代表）
- [ ] 长时运行代理基准测试（Q4-4）— 进行中，路线图最后一个未完成项

## 测试与基准结果

**静态测试（2026 年 4 月 12 日）：165 通过 / 12 失败 / 177 总计**，覆盖 11 个 claw 平台。

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
| Hermes-Agent | Python | ~60 .py | 11/13 通过 |
| Claw-AI-Lab | Python | ~50 .py | 11/13 通过 |

**运行时基准（v3.0 Python 引擎）：26 个平台 140 项指标** — 冷启动、内存、延迟、二进制大小，N=5 采样 + 统计分析。最新数据在 CI 产物中（`benchmark-suite.yml`，每日）；方法论见 [test_framework/docs/runtime_benchmark_methodology.md](../test_framework/docs/runtime_benchmark_methodology.md)。

**静态仓库指标（2026 年 4 月 12 日）：13 个平台 182 项指标**

| 平台 | 仓库大小 (KB) | 源文件数 | 代码行数 | 依赖数 | 测试文件数 |
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
| Hermes-Agent | ~8,000 | ~60 .py | ~8,000 | ~15 pip | ~12 |
| Claw-AI-Lab | ~10,000 | ~50 .py | ~7,000 | ~25 pip | ~8 |

---

## Agent 框架与工具链

> **新类别：** Agent 框架位于代理平台下方，提供执行运行时、协调和可观测性。

### UltraWorkers 工具链

**哲学：** *"人类设定方向；claws 执行工作。"*

#### claw-code (Rust)
- **仓库：** [ultraworkers/claw-code](https://github.com/ultraworkers/claw-code)
- **状态：** 活跃（声称约 100K stars）
- **概述：** Claude Code agent harness 架构的 clean-room 重写
- **关键数据：** 48,599 行 Rust 代码，9 个 crates，40 个工具规范（2026 年 4 月）
- **9 车道 Parity：** Bash 验证、文件工具、TaskRegistry、team/cron、MCP 生命周期、LSP 客户端、权限执行

#### oh-my-codex (Node.js)
- **仓库：** [Yeachan-Heo/oh-my-codex](https://github.com/Yeachan-Heo/oh-my-codex)
- **角色：** OpenAI Codex CLI 的工作流层
- **规范工作流：** `$deep-interview`、`$ralplan`、`$team`、`$ralph`

#### clawhip (Rust)
- **仓库：** [Yeachan-Heo/clawhip](https://github.com/Yeachan-Heo/clawhip)
- **角色：** 事件和通知路由器 (v0.3.0)
- **关键特性：** 类型化事件模型、多交付路由器、源提取

#### oh-my-openagent (Node.js)
- **仓库：** [code-yeongyu/oh-my-openagent](https://github.com/code-yeongyu/oh-my-openagent)
- **角色：** 多代理协调（Architect → Executor → Reviewer 收敛）

**完整分析：** [architecture/agent_harnesses.zh-CN.md](../architecture/agent_harnesses.zh-CN.md)

---

## OpenClaw

**TypeScript | ~34 万星 | v2026.4.x — 2026 年 5 月**

**状态：** 基金会治理过渡继续（创始人加入 OpenAI 后）

### 架构演进
- 渠道插件生态系统扩展（WhatsApp、Discord、Teams、Matrix）
- 通过适配器模式集成 MCP（非原生）
- 原生应用平台增长（iOS/Android/macOS）

### 新功能（4-5 月亮点）
- 额外的 LLM 提供商集成
- 增强的流式传输可靠性
- 技能市场增长
- Webhook 安全改进

### 安全加固
- 持续修复 3 月披露的 CVE
- 容器执行选项增强

---

## ZeroClaw

**Rust | ~2.9 万星 | v0.7.5 — 2026 年 5 月**

### 状态：性能领先者
- **<5MB 内存，<10ms 冷启动** 基准保持
- 生态系统中最高效的运行时

### 新功能
- MCP 适配器集成（stdio/SSE）
- 增强的会话状态管理
- 多房间渠道改进

---

## IronClaw

**Rust | 快速增长 | v1.0.0 — 2026 年 8 月**

**状态：** 已发布 1.0 — v1.0.0 于 2026-07-27 打 tag,8 月持续加固(经 API 验证月均 300+ 提交)。追踪分支已修正:`staging` → `main`(上游切换了默认分支;staging 自 5 月起冻结)

### 架构演进
- 类型化的 e2e provider journey(由类型化事实组合而成)
- 带持久化授权门的通知自动化
- extension 输出所有权强制

### 历史(pre-1.0)
- 多租户认证成熟度、分层记忆系统、WASM 扩展生态
- MCP 适配器集成(非原生方法)、基于风险的命令审批

### 安全加固
- 持续执行 cargo-deny
- 供应链审计

---

## GoClaw

**Go | ~1300 星 | lite-v3.9.1 — 2026 年 5 月**

### 架构演进
- 代理团队协调成熟化
- 车道调度器优化
- MCP 集成（stdio/SSE/streamable-http）

### 新功能
- 知识图谱增强
- OpenTelemetry 导出扩展
- 额外渠道和提供商

### 企业模式
- 多租户 PostgreSQL 架构
- 云部署优化

---

## NanoClaw

**TypeScript | 活跃开发 | Docker 合作 — 2026 年 3-5 月**

### 状态：MCP 怀疑论者
- 明确避免 MCP 开销
- 容器优先安全模式
- ~4000 行代码核心哲学

### 立场
- **MCP 抵制**：本地部署的 token 成本顾虑
- 优先直接工具执行
- Docker 沙箱联盟持续

---

## Nanobot

**Python | ~3.7 万星 | v0.2.0 — 2026 年 5 月**

### 架构演进
- 代理运行时解耦成熟化
- litellm 移除完成
- HookContext 标准化

### 新功能
- 渠道扩展（12+）
- LLM 提供商增长
- 基于 Token 的记忆细化

### 安全加固
- 供应链安全重点
- 邮件注入防护

---

## ClawTeam-OpenClaw

**Python | ~884 星 | v0.2.x+ — 2026 年 5 月**

### 多代理协调
- 领导者-工作者编排模式
- 每代理会话隔离
- ZeroMQ P2P 传输可选性

### 新功能
- Web 仪表板改进
- 团队模板扩展
- 计划审批工作流

---

## Maxclaw

**Go + TypeScript | ~189 星 | v0.1.x+ — 2026 年 5 月**

### 个人力量倍增器模式
- 本地优先部署
- Monorepo 感知上下文
- 桌面 UI + Web UI

### 新功能
- 子会话派生
- 浏览器自动化
- Systemd 部署

---

## HiClaw

**Go + Shell | 活跃开发 | v1.1.1 — 2026 年 4 月**

**状态：** 企业多代理运行时

### 架构：管理者-工作者模式
- Kubernetes 风格声明式资源
- 多代理编排
- 基于 Shell 的扩展性

### 关键功能
- 声明式资源定义
- 代理生命周期管理
- 企业部署重点

---

## Hermes-Agent

**Python | 研究支持 | v2026.5.16 — 2026 年 5 月**

**状态：** 声明验证完成

### 存在的功能
- ✅ 技能策展系统
- ✅ 跨会话记忆（FTS5 + LLM）
- ✅ MCP 集成
- ✅ 技能中心

### 缺失的功能
- ❌ 自主技能改进
- ❌ 基于强化学习的学习
- ❌ 性能跟踪

### 结论
**程序记忆 ≠ 自主学习** — "自我改进"声明被夸大

---

## Claw-AI-Lab

**Python | 学术研究 | 活跃开发**

**状态：** 教育研究平台

### 重点
- AI 代理教育
- 研究实验
- 学术合作

---

## CLI 编程代理

> **新类别：** 在终端中直接与开发者结对编程的 AI 编程助手。

### aider

**Python | 约 68K 星 | v0.86.3.dev — 2026 年 5 月**

**状态：** 活跃 — 最受欢迎的 AI 结对编程工具

### 概述
aider 是一个在终端中工作的 AI 结对编程工具，使开发者能够与 LLM 配对编程，直接编辑本地 git 仓库中的代码。支持 Claude、GPT-4 等模型。

### 关键特性
- **Git 感知** — 自动创建带有合理消息的提交
- **多模型** — 支持 Claude、GPT-4、DeepSeek 及 20+ LLM
- **代码生成模式** — AI 直接在仓库中编辑代码
- **全仓库上下文** — 可理解整个代码库
- **Map/架构模式** — 大型代码库的成本优化策略

### 架构
- **语言：** Python
- **入口：** `aider` CLI
- **架构模式：** REPL 结对编程 + git 集成
- **MCP 状态：** 无
- **部署：** 本地（pip install）

---

### copilot-cli

**TypeScript | GitHub 原生 | v1.0.49 — 2026 年 5 月**

**状态：** 活跃 — GitHub 官方 CLI 代理

### 概述
copilot-cli 是 GitHub 的 Copilot 驱动终端代理，将 AI 辅助直接带入命令行。使用 ACP（代理通信协议）实现结构化交互。

### 关键特性
- **GitHub 原生** — 深度集成 GitHub 工作流
- **ACP 协议** — 代理通信协议实现结构化终端交互
- **终端集成** — 在 shell 环境中原生工作
- **GitHub 生态** — 利用 GitHub Copilot 基础设施

### 架构
- **语言：** TypeScript
- **入口：** CLI
- **架构模式：** 终端代理 + ACP 协议
- **MCP 状态：** GitHub 原生（ACP 协议）
- **部署：** npm install

---

### reasonix

**TypeScript | 约 11.3K 星 | 2026 年 5 月**

**状态：** 活跃 — DeepSeek 原生编程代理

### 概述
reasonix（DeepSeek-Reasonix）是一个面向终端的 DeepSeek 原生 AI 编程代理。围绕前缀缓存稳定性设计，实现长会话中的低 token 成本，达到约 99.82% 的缓存命中率。使用 Ink（React for CLI）构建 TUI 界面。

### 关键特性
- **DeepSeek R1/v4 优化** — 专为 DeepSeek 推理模型构建
- **前缀缓存不变性** — 为最大前缀缓存稳定性而设计
- **SEARCH/REPLACE 编辑** — 精确代码修改的专注编辑策略
- **99.82% 缓存命中率** — 长编程会话中的低 token 成本
- **Ink TUI** — 基于 React 的终端 UI
- **Monorepo（npm）** — TypeScript 架构，Node ≥ 22

### 架构
- **语言：** TypeScript（Node ≥ 22）
- **入口：** `reasonix` CLI（npm 包：`reasonix`）
- **架构模式：** CLI 优先终端编程代理
- **MCP 状态：** 无
- **部署：** npm install（`npm install -g reasonix`）
- **LLM 支持：** DeepSeek（R1、v4）
- **许可：** MIT

---

## openhuman

**Rust | 学术/研究 | v0.53.49-staging — 2026 年 5 月**

**状态：** 活跃 — 研究平台

### 概述
openhuman 是一个基于 Rust 的人类数字孪生平台（人类数字孪生），旨在创建人类的数字表示，用于研究和模拟。

### 关键特性
- **人类数字孪生** — 数字表示范式
- **Rust 原生** — 高性能和内存安全
- **学术/研究重点** — 科学模拟和建模
- **Staging 分支活跃** — 在 staging 上积极开发

### 架构
- **语言：** Rust
- **入口：** 应用程序二进制
- **架构模式：** 数字孪生模拟平台
- **MCP 状态：** N/A
- **部署：** 本地

---

## Kimi CLI

**Python | 约 8.8K 星 | Apache-2.0 — 2026 年 5 月**

**状态：** 活跃 — MoonshotAI CLI 编程代理

### 概述
kimi-cli 是 MoonshotAI 的基于 CLI 的编程代理。基于 Python，支持 ACP（代理通信协议），提供终端 TUI 界面用于交互式编程会话。

### 关键特性
- **基于 Python** — 纯 Python 实现，易于扩展
- **ACP 支持** — 代理通信协议实现结构化交互
- **终端 TUI** — 交互式终端用户界面
- **MoonshotAI 集成** — 为 Moonshot AI 模型优化

### 架构
- **语言：** Python
- **入口：** CLI
- **架构模式：** 终端编程代理 + TUI
- **MCP 状态：** ACP 支持
- **部署：** pip install
- **LLM 支持：** MoonshotAI (Kimi)
- **许可：** Apache-2.0

---

## Codex CLI

**Rust | 约 86.9K 星 | Apache-2.0 — 2026 年 5 月**

**状态：** 活跃 — OpenAI 官方 CLI 编程代理

### 概述

codex 是 OpenAI 的轻量级编程代理，在终端中运行。使用 Rust 构建以实现高性能，提供沙箱执行确保安全的代码操作。AllClaws 跟踪的最高星 CLI 编程代理。

### 关键特性
- **Rust 原生** — 高性能 Rust 实现
- **沙箱执行** — 隔离环境中的安全代码操作
- **轻量级** — 最小化终端代理足迹
- **OpenAI 集成** — 为 OpenAI 模型（GPT-4、o 系列）优化

### 架构
- **语言：** Rust
- **入口：** CLI
- **架构模式：** 终端编程代理 + 沙箱执行
- **MCP 状态：** 无
- **部署：** 二进制安装
- **LLM 支持：** OpenAI（GPT-4、o 系列）
- **许可：** Apache-2.0

---

## Kimi Code

**TypeScript | 约 1.4K 星 | MIT — 2026 年 5 月**

**状态：** 活跃 — MoonshotAI 下一代代理框架

### 概述
kimi-code 是 MoonshotAI 的下一代代理框架。TypeScript monorepo，具有插件架构和 MCP（模型上下文协议）支持，用于构建可扩展的 AI 代理系统。

### 关键特性
- **插件架构** — 可扩展插件系统，支持自定义能力
- **MCP 支持** — 模型上下文协议，用于工具/上下文集成
- **TypeScript monorepo** — 现代、类型安全的实现
- **下一代框架** — 为构建多用途 AI 代理而设计

### 架构
- **语言：** TypeScript
- **入口：** 应用程序
- **架构模式：** 基于插件的代理框架
- **MCP 状态：** 原生
- **部署：** npm install
- **LLM 支持：** MoonshotAI (Kimi)
- **许可：** MIT

---

## 外部框架（新增跟踪）

### SmolAgents（Hugging Face）
**Python | ~26.7 万星 | ~1K 行代码核心**

- 代码生成模式（代理编写 Python）
- 最小可行框架参考
- 比较：Nanobot 工具调用 vs SmolAgents 代码生成

### LangGraph
**Python/TS | 企业采用**

- 基于图的编排
- 有状态工作流
- 企业模式比较

### CrewAI
**Python | 角色扮演重点**

- 带角色的自主代理
- 多代理协调
- 企业用例

### AutoGen
**Python | 微软起源**

- 对话式代理框架
- 多代理对话模式
- 企业集成

### Swarms
**Python | ~5000 星 | 企业重点**

- 企业编排
- 云部署模式
- 治理框架对齐

### OpenAgents
**TypeScript | 分布式网络**

- 分布式代理架构
- 云原生设计
- 基于网络的协调

### OpenFang
**Rust | 约 17.6K 星 | v0.6.9 — 2026 年 5 月**

**状态：** 活跃 — Agent OS

### 概述
OpenFang 是一个基于 Rust 的 Agent OS，作为单一二进制文件部署（约 32MB，14 个 crate 中共 137K 行代码）。采用"Hands"架构——用于特定任务的自主能力包。支持 27 个 LLM 提供商和 123+ 模型。兼容 OpenClaw（SKILL.md、ClawHub）。

### 关键特性
- **7 个预构建 Hands** — Lead、Clip、Researcher、Collector、Predictor、Twitter、Browser
- **单一二进制文件** — 跨平台部署（macOS、Linux、Windows）
- **27 个 LLM 提供商，123+ 模型** — 最广泛的提供商覆盖
- **Web 仪表板** — 内置管理 UI
- **WhatsApp 网关** — 原生消息集成
- **兼容 OpenClaw** — SKILL.md 格式、ClawHub、`migrate --from openclaw`
- **护栏** — 敏感操作的购买审批门控

### 架构
- **语言：** Rust
- **入口：** 单一二进制文件
- **架构模式：** Agent OS + Hands（自主能力包）
- **MCP 状态：** 适配器（topic tagged）
- **部署：** 跨平台单一二进制文件（约 32MB）
- **LLM 支持：** 27 个提供商，123+ 模型
- **数据库：** SQLite

---

## AgentScope

**Python | 约 25.8K 星 | Apache-2.0 — 2026 年 5 月**

**状态：** 活跃 — 阿里巴巴达摩院多代理框架

### 概述
AgentScope 是阿里巴巴达摩院开发的分布式多代理框架。提供消息中心架构用于代理通信，以及基于管道的工作流用于组合多代理协作模式。兼顾研究和生产使用。

### 关键特性
- **分布式多代理协作** — 代理通过集中式消息中心通信
- **消息中心架构** — 通过消息传递实现代理间解耦通信
- **管道工作流** — 可组合的管道模式，用于构建多代理交互结构
- **Python 原生** — 纯 Python 实现，便于研究扩展
- **生产就绪** — 支持分布式部署场景

### 架构
- **语言：** Python
- **入口：** Python API
- **架构模式：** 分布式多代理 + 消息中心 + 管道工作流
- **MCP 状态：** N/A
- **部署：** pip install
- **LLM 支持：** 多提供商
- **许可：** Apache-2.0

---

## Eliza

**TypeScript | MIT — 2026 年 5 月**

**状态：** 活跃 — 多平台 AI 代理框架

### 概述
Eliza 是由 eliza-os 开发的基于 TypeScript 的多平台 AI 代理框架。提供插件架构，用于构建可跨多个平台和通信渠道运行的 AI 代理。

### 关键特性
- **多平台支持** — 代理可在 Discord、Telegram、Twitter 等平台运行
- **插件架构** — 可扩展插件系统，支持自定义能力
- **TypeScript 原生** — 现代、类型安全的实现
- **MIT 许可** — 开源，宽松许可

### 架构
- **语言：** TypeScript
- **入口：** 应用程序
- **架构模式：** 基于插件的多平台代理框架
- **MCP 状态：** N/A
- **部署：** npm install
- **许可：** MIT

---

## Agent Zero

**Python | MIT — 2026 年 5 月**

**状态：** 活跃 — 自主 AI 代理框架

### 概述
Agent Zero 是由 frdel 开发的基于 Python 的自主 AI 代理框架。提供工具使用能力，用于构建可自主执行任务的代理。

### 关键特性
- **自主操作** — 代理可独立朝目标工作
- **工具使用能力** — 内置支持使用工具和 API
- **Python 原生** — 纯 Python 实现，易于扩展
- **MIT 许可** — 开源，宽松许可

### 架构
- **语言：** Python
- **入口：** Python API
- **架构模式：** 自主代理 + 工具使用
- **MCP 状态：** N/A
- **部署：** pip install
- **许可：** MIT

---

## PraisonAI

**Python | MIT — 2026 年 5 月**

**状态：** 活跃 — 多代理 LLM 框架

### 概述
PraisonAI 是由 MervinPraison 开发的基于 Python 的多代理 LLM 框架。具有低代码工作流构建器，可最小化配置创建多代理系统。

### 关键特性
- **低代码工作流构建器** — 最少编码创建多代理工作流
- **多代理编排** — 协调多个代理执行复杂任务
- **Python 原生** — 纯 Python 实现
- **MIT 许可** — 开源，宽松许可

### 架构
- **语言：** Python
- **入口：** Python API / CLI
- **架构模式：** 多代理 LLM 框架 + 低代码工作流
- **MCP 状态：** N/A
- **部署：** pip install
- **许可：** MIT

---

## Rocketride

**TypeScript | MIT — 2026 年 5 月**

**状态：** 活跃 — near.ai 代理服务器

### 概述
Rocketride 是由 nearai 为 near.ai 平台开发的基于 TypeScript 的代理服务器。提供服务器端运行时，用于 AI 代理自主执行任务。

### 关键特性
- **服务器端运行时** — 在服务器环境中运行代理
- **自主任务执行** — 代理可自主执行任务
- **TypeScript 原生** — 现代、类型安全的实现
- **near.ai 集成** — 为 near.ai 生态系统构建

### 架构
- **语言：** TypeScript
- **入口：** 服务器应用程序
- **架构模式：** 自主任务执行代理服务器
- **MCP 状态：** N/A
- **部署：** npm install
- **许可：** MIT

---

## 分叉分析：个人 vs 企业

| 方面 | 个人力量倍增器 | 企业自动化 |
|------|---------------|-----------|
| **主要关注点** | 速度、成本 | 治理、合规 |
| **部署** | 本地、单用户 | 云、多租户 |
| **工具访问** | CLI、直接执行 | MCP、协议 |
| **示例** | OpenClaw、Nanobot、SmolAgents、Maxclaw、IronClaw、ZeroClaw、NanoClaw | LangGraph、Swarms、HiClaw、GoClaw、CrewAI、AutoGen、AgentScope |

---

## 对比总览

| 项目 | 星数 | 语言 | MCP 状态 | 模式 |
|------|------|------|---------|------|
| OpenClaw | ~34 万 | TypeScript | 适配器 | 个人 |
| ZeroClaw | ~2.9 万 | Rust | 适配器 | 个人 |
| IronClaw | 增长中 | Rust | 适配器 | 个人/企业 |
| GoClaw | ~1300 | Go | 适配器 | 企业 |
| Nanobot | ~3.7 万 | Python | 无 | 个人 |
| NanoClaw | N/A | TypeScript | 抵制 | 个人 |
| ClawTeam | ~884 | Python | 无 | 个人 |
| Maxclaw | ~189 | Go+TS | 无 | 个人 |
| HiClaw | N/A | Go+Shell | 适配器 | 企业 |
| Hermes-Agent | N/A | Python | 原生 | 个人 |
| Claw-AI-Lab | N/A | Python | N/A | 学术 |
| SmolAgents | ~26.7 万 | Python | N/A | 个人 |
| LangGraph | N/A | Py/TS | N/A | 企业 |
| CrewAI | N/A | Python | N/A | 企业 |
| AutoGen | N/A | Python | N/A | 企业 |
| Swarms | ~5000 | Python | N/A | 企业 |
| OpenAgents | N/A | TypeScript | N/A | 企业 |
| OpenFang | 约 17.6K | Rust | 适配器 | 个人 |
| aider | 约 68K | Python | 无 | 个人 |
| copilot-cli | N/A | TypeScript | ACP | 个人 |
| reasonix | 约 11.3K | TypeScript | 无 | 个人 |
| openhuman | N/A | Rust | N/A | 学术 |
| Kimi CLI | 约 8.8K | Python | ACP | 个人 |
| Kimi Code | 约 1.4K | TypeScript | 原生 | 个人/企业 |
| Codex CLI | 约 86.9K | Rust | 无 | 个人 |
| AgentScope | 约 25.8K | Python | N/A | 企业 |
| Eliza | N/A | TypeScript | N/A | 个人/企业 |
| Agent Zero | N/A | Python | N/A | 个人 |
| PraisonAI | N/A | Python | N/A | 个人/企业 |
| Rocketride | N/A | TypeScript | N/A | 企业 |
| OpenWorker | 约 9.8K | Python/Rust | 原生 | 个人/企业 |
| Dify | 约 15 万 | TypeScript/Python | 原生 | 企业 |
| MetaGPT | 约 6.9 万 | Python | N/A | 企业 |
| Qwen-Agent | 约 1.6 万 | Python | 原生 | 个人/企业 |
| browser-use | 约 11 万 | Python | 原生（server）| 个人 |

---

*最后更新：2026 年 8 月 20 日*
*所属：AllClaws 个人 AI 代理生态系统研究*
*跟踪平台：35 个（11 个 claw 生态 + 18 个外部框架 + 5 个 CLI 编程代理 + 1 个人类数字孪生）*
*下次更新：2026 年 9 月*
