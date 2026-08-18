# Agent 框架与工具链

**[English](agent_harnesses.md)** | [中文](agent_harnesses.zh-CN.md)

> 用于大规模运行基于 CLI 的 AI 代理的基础设施和工具。与提供 AI 能力的代理平台不同，框架提供执行、协调和可观测性层。

---

## 概述

Agent 框架位于代理平台的**下方**：

```
┌─────────────────────────────────────────────────────────────┐
│  Agent Platforms (OpenClaw, ClawTeam, SmolAgents, etc.)    │
│  - 提供 AI 能力、工具和代理逻辑                              │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  Agent Harnesses & Toolchains (本文档)                      │
│  - 执行运行时、协调、可观测性                                │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  Foundation (LLM APIs, MCP, Docker, Git)                   │
└─────────────────────────────────────────────────────────────┘
```

**跟踪的生态系统：**
- **UltraWorkers 工具链** — Rust + Node.js 自主开发系统
- **Darwin Agent HarnessX** — Python agent harness foundry，具有可组合处理器和进化引擎
- **OmniCoreAgent** — Python 生产级 agent harness，MCP + memory + subagents
- **Harmonist** — Python 便携式多 agent 编排，机械化协议强制执行
- **SIA** — Python 自改进 AI 框架，harness + 权重双重改进
- **DeepSeek Harness (dsh)** — DeepSeek 官方 TypeScript 插件树 harness，基于 Cordis 组合框架（2026 年 8 月新增）
- **Pi** — Earendil Works 的 TypeScript 自扩展编程 agent harness（2026 年 8 月新增）

---

## DeepSeek Harness (dsh) 与 Pi — 2026 年 8 月新增

两大 2026 年 8 月评估的 harness 候选（Q4-7 类别缺口闭合），代表组合哲学的两个极端：

| 维度 | **DeepSeek Harness (dsh)** | **Pi** |
|------|------|------|
| 出品方 | DeepSeek 官方（模型厂商第一方 harness） | Earendil Works（badlogic 主导，mitsuhiko 为第二贡献者） |
| 发布 | 2026-08-13，4 天 158.8K 星；v0.1.0-rc.7 | 2025-08，一年 93.0K 星；正式 npm 多包发布 |
| 哲学 | *「一切皆插件」*——Cordis 组合框架（时空可组合性论文），无特权核心 | *「自扩展编程 agent」*——稳定核心 + TS 扩展模块在边缘生长 |
| 扩展模型 | 插件树 + 三类事件域（session/agent/capability），waterfall 事件强制 `next()` 委托 | `pi.registerTool()` / 事件订阅 / `ctx.ui` 自定义 TUI / `pi.appendEntry()` 持久化 |
| 状态管理 | append-only SessionEvent log，「model-visible means logged」运行时不变式；turn/step 显式状态机 | appendEntry + session-manager，tree 分支导航 |
| 护栏 | sandbox backend 缝隙 + approval policy（base bundle 内置） | **刻意不内置权限系统**——三种容器化模式外置隔离（Gondolin micro-VM / Docker / OpenShell） |
| 上下文 | prompt 分段装配 + `agent/pre-step` 可重写/拒绝输入 | 结构化压缩 + 分支摘要；**压缩请求禁用 prompt-cache 写**（cache 意识最细） |
| 遥测 | telemetry 插件 | pi-telemetry 包——vendor-neutral 契约 + 一致性测试 |
| 成熟度风险 | rc 版本，官方承诺破坏性变更 | 一年生产打磨，供应链加固（依赖钉死精确版本） |

**对 AllClaws 的意义**：dsh 是「harness 成为独立学科」的最强证据——前沿模型厂商断定差异化在 harness 层而非模型层；其组合代数把 HarnessX 理论化的替换属性工程化。Pi 代表应用极：在生产打磨最薄弱处（压缩细节、遥测契约、自扩展）恰好最深。两者的权限立场（缝隙内置 vs 刻意外置）恰好张开了 A2 护栏设计空间。**均为 Q4-7 harness 类别候选**：dsh 为组合形式化（MONITOR 级，rc 未稳），Pi 为扩展实用主义（可直接 TRACK）。

详见英文版完整章节：[agent_harnesses.md](agent_harnesses.md)

---

## UltraWorkers 工具链

**哲学：** *"人类设定方向；claws 执行工作。"*

### 三部分系统

```
┌──────────────────────────────────────────────────────────────┐
│                     Discord Chat Interface                    │
│  (人类从手机输入指令，然后离开)                              │
└──────────────────────────────────────────────────────────────┘
                            ↓
┌──────────────┬──────────────┬────────────────────────────────┐
│   OmX        │   clawhip    │            OmO                 │
│ (oh-my-codex) │              │   (oh-my-openagent)            │
│              │              │                                │
│  Workflow    │   Event      │   Multi-Agent                  │
│    Layer     │   Router     │   Coordination                 │
│              │              │                                │
│  Planning →  │  Git/GitHub/ │   Architect → Executor →        │
│  Execution   │  tmux/Agent  │   Reviewer convergence         │
│    modes     │   events     │                                │
└──────────────┴──────────────┴────────────────────────────────┘
                            ↓
┌──────────────────────────────────────────────────────────────┐
│                    claw-code (Rust CLI)                      │
│              实际的 agent harness                            │
└──────────────────────────────────────────────────────────────┘
```

### 1. claw-code

**仓库：** [ultraworkers/claw-code](https://github.com/ultraworkers/claw-code)
**语言：** Rust
**状态：** 活跃（声称约 100K stars）

**概述：**
"claw CLI agent harness" 的公共 Rust 实现 —— Claude Code agent harness 架构的 clean-room 重写。

**关键数据（2026 年 4 月）：**
- main 分支 292 次提交 / 所有分支 293 次
- 9 个 crates，48,599 行跟踪的 Rust 代码
- 2,568 行测试代码
- 3 位作者（2026 年 3 月 31 日 - 4 月 3 日开发爆发）

**架构：**

```rust
// 核心组件
rust/
├── crates/
│   ├── rusty-claude-cli/     // 主 CLI 二进制
│   ├── runtime/              // Bash、沙箱、任务注册表
│   ├── tools/                // 40 个暴露的工具规范
│   ├── mock-anthropic-service/  // 测试框架
│   └── ... (5 个更多 crates)
```

**关键特性：**
- **9 车道 parity 检查点**与 Claude Code 架构
- **40 个工具规范**包括 bash、文件操作、MCP、LSP、team/cron
- **Mock parity 框架**用于确定性测试
- **权限执行**层与工作区边界
- **MCP 生命周期桥**用于工具表面集成

**"Clawable" 哲学：**

一个 clawable 的框架是：
- 启动时确定性
- 状态和失败模式机器可读
- 无需人类监视终端即可恢复
- 分支/测试/worktree 感知
- 插件/MCP 生命周期感知
- 事件优先，而非日志优先
- 能够自主执行下一步

**路线图亮点：**

| 阶段 | 重点 | 状态 |
|------|------|--------|
| 1 | 可靠 Worker 启动 | 🔄 进行中 |
| 2 | 事件原生 clawhip 集成 | 🔄 进行中 |
| 3 | 分支/测试感知 | 计划中 |
| 4 | Claws 优先任务执行 | 计划中 |
| 5 | 插件/MCP 生命周期成熟 | 计划中 |

**隶属关系：** 明确**不隶属于** Anthropic —— 包含所有权免责声明。

---

### 2. oh-my-codex (OMX)

**仓库：** [Yeachan-Heo/oh-my-codex](https://github.com/Yeachan-Heo/oh-my-codex)
**语言：** Node.js (TypeScript)
**角色：** 工作流层

**概述：**
OMX 是 OpenAI Codex CLI 的工作流层。它保持 Codex 作为执行引擎，并添加：
- 更强的默认会话启动
- 规范工作流（`$deep-interview`、`$ralplan`、`$team`、`$ralph`）
- 通过作用域 `AGENTS.md` 的项目指导
- `.omx/` 下的持久状态

**规范工作流：**

```bash
# 强力启动 OMX
omx --madmax --high

# 然后使用规范工作流：
$deep-interview "clarify the authentication change"
$ralplan "approve the safest implementation path"
$ralph "carry the approved plan to completion"
$team 3:executor "execute in parallel"
```

**OMX 的作用：**
- 将短指令转换为结构化执行
- 规划关键词、执行模式、持久验证循环
- 并行多代理工作流
- 基于角色的专家调用

**设计哲学：**
OMX **不**替代 Codex。它添加：
- 更好的任务路由
- 更好的工作流
- 更好的运行时

---

### 3. clawhip

**仓库：** [Yeachan-Heo/clawhip](https://github.com/Yeachan-Heo/clawhip)
**语言：** Rust
**角色：** 事件和通知路由器

**概述：**
守护进程优先的 Discord 通知路由器，具有类型化事件管道、提取的源和干净的渲染器/接收器分离。

**系统模型：**

```
[CLI / webhook / git / GitHub / tmux]
           ↓
    [sources]
           ↓
    [mpsc queue]
           ↓
   [dispatcher]
           ↓
[router → renderer → Discord/Slack sink]
           ↓
[Discord REST / Slack webhook delivery]
```

**关键特性 (v0.3.0)：**
- **类型化事件模型** — 标准化和验证的信封
- **多交付路由器** — 一个事件 → 零个、一个或多个交付
- **源提取** — git、GitHub、tmux 作为显式源
- **接收器/渲染分离** — 渲染与传输分离

**提供者原生挂钩：**

Codex + Claude 的共享 v1 挂钩事件：
- `SessionStart`
- `PreToolUse`
- `PostToolUse`
- `UserPromptSubmit`
- `Stop`

**哲学：**
Clawhip 将监控和交付保持在编码代理的上下文窗口**之外**，以便代理可以专注于实现，而不是状态格式化和通知路由。

---

### 4. oh-my-openagent (OmO)

**仓库：** [code-yeongyu/oh-my-openagent](https://github.com/code-yeongyu/oh-my-openagent)
**角色：** 多代理协调

**概述：**
处理代理之间的规划、交接、分歧解决和验证循环。

**当 Architect、Executor 和 Reviewer 不同意时，OmO 为该循环提供收敛而不是崩溃的结构。**

---

## 与代理平台的比较

| 方面 | Agent Platforms | Agent Harnesses |
|------|----------------|-----------------|
| **目的** | 提供 AI 能力 | 提供执行/协调 |
| **核心价值** | 智能、工具、技能 | 可靠性、可观测性、自动化 |
| **用户界面** | 聊天、CLI、API | 事件、挂钩、API |
| **典型用户** | 最终用户、开发者 | 代理、编排器、运维 |
| **示例** | OpenClaw、SmolAgents | claw-code、clawhip |
| **类比** | 引擎 | 变速箱、仪表板、维修团队 |

---

## 关键模式

### 1. 事件优先架构

框架发出类型化事件，而不是日志文本：
- `lane.started`、`lane.ready`、`lane.blocked`
- `agent.started`、`agent.blocked`、`agent.finished`
- `git.commit`、`github.pr-opened`

这实现了机器可读状态，而不是扫描散文。

### 2. 升级前恢复

已知的失败模式应该在请求帮助之前自动恢复一次：
- 信任提示解决
- 提示传递错误检测
- 陈旧分支检测
- MCP 启动失败

### 3. Discord 作为人类界面

重要的界面不是 tmux、Vim 或 SSH。它是一个 Discord 频道：
- 从手机输入一句话
- 走开、睡觉或做其他事情
- Claws 读取指令，分解任务，分配角色
- 编写代码，运行测试，争论失败
- 恢复并在工作通过时推送

### 4. 三部分协调

1. **OmX** — 指令 → 结构化工作协议
2. **clawhip** — 代理上下文之外的事件路由
3. **OmO** — 多代理收敛

---

## 新兴趋势

### 1. Rust 采用

claw-code (48K+ LOC) 展示了 Rust 作为代理框架语言的严肃性：
- 长时间运行守护进程的内存安全
- 事件路由的性能
- 事件模式的类型安全

### 2. Clean-Room 重新实现

claw-code 是 "Claude Code agent harness 架构的 clean-room 重写" —— 表明：
- 对开放替代方案的强烈需求
- 值得复制的架构模式
- 社区基础设施所有权

### 3. Discord 作为运营中心

将人类监督从终端转移到聊天：
- 异步通知
- 多设备访问（手机、桌面）
- 机器人友好的 API
- 持久上下文

### 4. 机器可读状态

从人类可读日志转移到结构化事件：
- 启用代理到代理通信
- 自动恢复
- 仪表板层与数据分离

---

## 未来方向

### 开放问题

1. **标准化：** agent framework 协议会标准化吗（类似于 MCP）？
2. **多框架：** 一个平台可以与多个框架一起工作吗？
3. **平台收敛：** agent 平台会直接构建框架功能吗？
4. **企业与 1PC：** 企业和个人使用之间的框架需求有何不同？

### 潜在添加

新的框架生态系统可能会根据以下条件添加：
- 活跃开发（当年有提交）
- 独特的架构模式
- 社区采用
- 与跟踪的代理平台的相关性

---

## 相关文档

- [平台比较](../architecture/platform_comparison.md) — 完整的代理平台覆盖
- [外部框架](../architecture/external_frameworks.md) — LangGraph、SmolAgents 等
- [最新更新](../docs/LATEST_UPDATES.md) — 月度生态系统跟踪

---

*最后更新：2026 年 8 月 18 日*
*属于：AllClaws 个人 AI 代理生态系统研究*
