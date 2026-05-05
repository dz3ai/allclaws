# 外部 AI 代理框架：比较分析

**[中文](external_frameworks.zh-CN.md)** | English

> AllClaws 跟踪的主要外部 AI 代理框架分析，用于生态系统比较。这些框架代表行业标准，与 claw 生态平台互补。

---

## 概述

本文档提供 7 个重要外部 AI 代理框架的详细分析：

| 框架 | 语言 | Stars | 主要关注点 | 跟踪级别 |
|------|------|-------|-----------|----------|
| **SmolAgents** | Python | ~26.7k | 轻量级代码代理 | 完整 |
| **LangGraph** | Python/TS | N/A | 有状态多代理工作流 | 完整 |
| **mcp-agent** | Python | ~8.2k | MCP 原生代理 | 完整 |
| **CrewAI** | Python | N/A | 角色扮演自主代理 | 完整 |
| **AutoGen** | Python | N/A | 多代理对话 | 完整 |
| **Swarms** | Python | ~5k | 企业编排 | 完整 |
| **OpenAgents** | TypeScript | N/A | 分布式代理网络 | 摘要 |

**集成级别：** 外部框架通过文档分析而非 git 子模块跟踪。它们代表与 claw 生态平台进行比较的行业标准。

---

## 1. SmolAgents (Hugging Face)

**状态：** 活跃 | **语言：** Python | **Stars：** ~26.7k
**仓库：** [github.com/huggingface/smolagents](https://github.com/huggingface/smolagents)
**文档：** [huggingface.co/docs/smolagents](https://huggingface.co/docs/smolagents/index)

### 概述

SmolAgents 是 Hugging Face 的超轻量级 AI 代理库，旨在使构建代理极其简单。其核心哲学是"用代码思考的代理"——代理将操作表达为可执行的 Python 代码，而不是抽象的工具调用。

### 关键原则

- **最小核心** — 核心引擎约 1,000 行代码
- **代码优先范式** — 代理编写并执行 Python 代码
- **从零到英雄的简洁性** — 用最少的样板代码构建健壮的代理
- **Hugging Face 生态** — 与 HF Hub 和推理 API 原生集成
- **沙箱执行** — E2B 集成，用于安全代码执行

### 架构

```python
# 典型的 SmolAgents 使用模式
from smolagents import CodeAgent, HfApiModel

agent = CodeAgent(model=HfApiModel())
agent.run("生成股价走势图")
```

**核心组件：**
- **CodeAgent** — 解释任务并生成代码的主要代理类
- **HfApiModel** — Hugging Face 推理接口（提供免费层级）
- **工具执行** — 在沙箱环境中运行生成的代码
- **记忆系统** — 跟踪对话上下文和结果

### 与 Claw 生态的比较

| 方面 | SmolAgents | Nanobot | NanoClaw |
|------|------------|---------|----------|
| **核心 LOC** | ~1,000 | ~4,000 | ~10,600 |
| **范式** | 代码生成 | 工具调用 | 容器优先 |
| **沙箱** | E2B | 原生 | Docker |
| **生态** | Hugging Face Hub | 自定义 | 自定义 |

### 战略价值

SmolAgents 代表了**代码即操作**范式，与 claw 生态平台中主导的**工具调用**方法不同。其约 1,000 LOC 的核心展示了代理框架在保持功能的同时可以多么精简——这是架构比较的宝贵参考。

---

## 2. LangGraph (LangChain)

**状态：** 活跃 | **语言：** Python、TypeScript | **仓库：** [github.com/langchain-ai/langgraph](https://github.com/langchain-ai/langgraph)
**文档：** [langchain-ai.github.io/langgraph](https://langchain-ai.github.io/langgraph/)

### 概述

LangGraph 是一个基于图的编排框架，用于构建有状态的多代理 AI 应用程序。基于 LangChain 构建，它将 AI 工作流建模为有向图，其中节点代表处理步骤，边定义它们之间的流程。

### 关键原则

- **基于图的工作流** — 将代理建模为图结构
- **有状态执行** — 检查点用于持久化和恢复
- **人在环路** — 人工干预模式
- **并行执行** — 并发操作支持
- **企业就绪** — 经过生产测试的模式

### 架构

```python
# LangGraph 工作流模式
from langgraph.graph import StateGraph, START, END

workflow = StateGraph(AgentState)
workflow.add_node("agent", agent_node)
workflow.add_node("tools", tool_node)
workflow.add_edge(START, "agent")
workflow.add_conditional_edges("agent", should_continue)
```

**核心组件：**
- **StateGraph** — 具有类型化状态的主要图构建器
- **节点** — 代理、工具或处理函数
- **边** — 节点之间的条件路由
- **检查点** — 跨执行的状态持久化
- **子图** — 嵌套工作流组合

### 与多代理 Claw 平台的比较

| 方面 | LangGraph | ClawTeam | GoClaw |
|------|-----------|----------|--------|
| **编排** | 基于图 | 领导-工作者 | 基于团队 |
| **状态** | 检查点 | Git worktrees | PostgreSQL |
| **持久化** | 内置 | 基于文件 | 数据库 |
| **类型安全** | 类型化状态 | 无类型 | Go 类型 |

### 战略价值

LangGraph 代表多代理系统的**图编排**方法，与 ClawTeam 的**领导-工作者**和 GoClaw 的**基于团队**模式形成对比。其通过 LangChain 生态系统的企业采用使其成为生产多代理架构的关键参考。

---

## 3. mcp-agent (LastMile AI)

**状态：** 活跃 | **语言：** Python | **Stars：** ~8.2k
**仓库：** [github.com/lastmile-ai/mcp-agent](https://github.com/lastmile-ai/mcp-agent)

### 概述

mcp-agent 是一个使用模型上下文协议（MCP）构建 AI 代理的 Python 框架。它提供了简化的 MCP 方法，MCP 本身非常底层。该框架的愿景："MCP is all you need."

### 关键原则

- **MCP 原生** — 专为 MCP 协议设计
- **规划器-执行器模型** — 模块化规划和执行
- **内置记忆** — 集成记忆系统
- **简单组合** — 从 MCP 服务器构建代理

### 架构

```python
# mcp-agent 使用模式
from mcp_agent import MCPAgent

agent = MCPAgent(
    mcp_servers=["filesystem", "github", "postgres"]
)
agent.run("分析仓库并总结")
```

**核心组件：**
- **MCP 客户端** — 连接到 MCP 服务器
- **规划器** — 将任务分解为 MCP 工具调用
- **执行器** — 通过 MCP 协议执行工具
- **记忆** — 跨会话跟踪上下文

### MCP 支持比较

| 平台 | MCP 支持 | 类型 |
|------|----------|------|
| **mcp-agent** | 原生（参考） | 围绕 MCP 构建的框架 |
| **IronClaw** | 适配器 | stdio/SSE/streamable-http |
| **GoClaw** | 适配器 | stdio/SSE/streamable-http |
| **ZeroClaw** | 适配器 | stdio/SSE/streamable-http |
| **OpenClaw** | 插件 | 通过扩展 |
| **NanoClaw** | 无 | CLI 优先，抵制 |

### 战略价值

mcp-agent 是 MCP 原生代理的**参考实现**。它展示了完全围绕 MCP 构建的框架与添加 MCP 作为适配器的框架有何不同。对于理解 MCP 生态系统的方向至关重要。

---

## 4. CrewAI

**状态：** 活跃 | **语言：** Python | **仓库：** [github.com/crewaiinc/crewai](https://github.com/crewaiinc/crewai)

### 概述

CrewAI 是一个用于编排角色扮演自主 AI 代理的 Python 框架。它使开发者能够创建多代理系统，其中代理承担特定角色（研究员、作家、分析师），协作完成任务，并通过沟通实现目标。

### 关键原则

- **基于角色的代理** — 每个代理都有定义的角色、目标、背景故事
- **任务委派** — 代理之间的自动任务分配
- **顺序/并行执行** — 灵活的工作流模式
- **工具使用** — 代理可以使用外部工具
- **人在环路** — 在关键步骤可选的人工批准

### 架构

```python
# CrewAI 使用模式
from crewai import Agent, Task, Crew

researcher = Agent(
    role="研究员",
    goal="找到相关信息",
    backstory="经验丰富的研究员"
)

task = Task(
    description="研究 AI 框架",
    agent=researcher
)

crew = Crew(agents=[researcher], tasks=[task])
crew.kickoff()
```

**核心组件：**
- **Agent** — 具有目标、背景故事、工具的基于角色的实体
- **Task** — 分配给代理的工作单元
- **Crew** — 一起工作的代理集合
- **Process** — 执行流程（顺序、并行、分层）

### 与 ClawTeam 的比较

| 方面 | CrewAI | ClawTeam |
|------|--------|----------|
| **协调** | 基于角色的故事 | 领导-工作者 |
| **状态** | 内存中 | Git worktrees + 文件 |
| **沟通** | 直接消息 | 收件箱系统 |
| **隔离** | 进程级 | 文件系统（worktrees） |

### 战略价值

CrewAI 的**角色扮演**范式与 ClawTeam 的**领导-工作者**模式形成对比。两者都实现了多代理协调，但通过不同的哲学方法——CrewAI 强调角色个性，ClawTeam 强调任务依赖。

---

## 5. AutoGen (Microsoft)

**状态：** 活跃 | **语言：** Python | **仓库：** [github.com/microsoft/autogen](https://github.com/microsoft/autogen)

### 概述

AutoGen 是微软研究院的多代理对话框架。它使代理能够通过对话相互沟通来解决问题，支持人在环路交互和代码执行。

### 关键原则

- **基于对话** — 代理通过消息沟通
- **人在环路** — 人类可以加入对话
- **代码执行** — 在 Docker 中安全执行代码
- **多模态** — 文本、图像、代码
- **LLM 灵活性** — 适用于各种 LLM 提供商

### 架构

```python
# AutoGen 使用模式
from autogen import AssistantAgent, UserProxyAgent

assistant = AssistantAgent(
    name="assistant",
    llm_config={"model": "gpt-4"}
)

user_proxy = UserProxyAgent(
    name="user",
    code_execution_config={"use_docker": True}
)

user_proxy.initiate_chat(
    assistant,
    message="解决这个编码问题"
)
```

**核心组件：**
- **Agent** — 具有配置的对话实体
- **Conversation** — 代理之间的消息序列
- **UserProxyAgent** — 人类代表
- **CodeExecutor** — 安全代码执行环境

### 与多代理平台的比较

| 方面 | AutoGen | ClawTeam | CrewAI |
|------|---------|----------|--------|
| **沟通** | 对话消息 | 收件箱系统 | 直接调用 |
| **人类角色** | UserProxy 代理 | 与代理分离 | 可选批准 |
| **代码执行** | 内置 Docker | 通过代理工具 | 通过代理工具 |

### 战略价值

AutoGen 代表多代理协调的**对话**方法，与 ClawTeam 的**任务队列**和 CrewAI 的**基于角色**方法不同。微软研究院的支持使其成为重要的行业参考。

---

## 6. Swarms

**状态：** 活跃 | **语言：** Python | **Stars：** ~5k
**仓库：** [github.com/kyegomez/swarms](https://github.com/kyegomez/swarms)
**网站：** [swarms.ai](https://swarms.ai)

### 概述

Swarms 是一个企业级、生产就绪的多代理编排框架。它专注于生产部署的可扩展性、可靠性和开发者体验。该项目将自己描述为"最可靠、可扩展和灵活的多代理编排框架"。

### 关键原则

- **企业级** — 生产就绪的可靠性
- **可扩展性** — 处理大规模代理部署
- **异步编排** — 异步子代理（v10+）
- **技能编排** — SkillOrchestra 用于代理能力
- **代理经济** — 基于代理的经济系统愿景

### 架构

```
Swarms v10 架构：
- 异步子代理
- SkillOrchestra（能力管理）
- 重建的核心系统
- 新的编排原语
```

**核心组件：**
- **Swarm** — 一起工作的代理集合
- **Orchestrator** — 管理代理生命周期和沟通
- **Skills** — 可重用的代理能力
- **Tools** — 外部服务集成

### 与 GoClaw/HiClaw 的比较

| 方面 | Swarms | GoClaw | HiClaw |
|------|--------|--------|--------|
| **目标** | 企业编排 | 多代理网关 | 多代理运行时 |
| **语言** | Python | Go | Go + Shell |
| **架构** | 异步技能 | 基于车道调度器 | 管理-工作者 |
| **数据库** | 未知 | PostgreSQL | MinIO + Matrix |

### 战略价值

Swarms 代表多代理编排的 **Python 企业**方法，在企业领域与 GoClaw 和 HiClaw 竞争。其"代理经济"愿景和对生产可靠性的关注使其成为企业部署模式的关键参考。

---

## 7. OpenAgents

**状态：** 活跃 | **语言：** TypeScript | **仓库：** [github.com/openagents-org/openagents](https://github.com/openagents-org/openagents)

### 概述

OpenAgents 是一个用于分布式 AI 代理网络的基于 TypeScript 的框架。其哲学："Your agents are everywhere"——代理可以在服务器上维护数据库、管理营销，并在分布式基础设施中回复用户。

### 关键原则

- **分布式代理** — 代理位于不同的服务器上
- **TypeScript 优先** — 原生 TypeScript 实现
- **云原生** — 为分布式部署设计
- **多位置** — 跨不同基础设施的代理

### 架构

```
OpenAgents 分布式模型：
- 服务器 A 上的代理：维护数据库
- 服务器 B 上的代理：处理营销
- 服务器 C 上的代理：回复用户
- 跨分布式网络的协调
```

**核心组件：**
- **代理工作区** — 分布式代理部署
- **网络协调** — 跨代理通信
- **云集成** — 多云部署

### 与 QuantumClaw 的比较

| 方面 | OpenAgents | QuantumClaw |
|------|------------|-------------|
| **部署** | 分布式云 | 本地优先 |
| **协议** | 自定义 | AGEX |
| **语言** | TypeScript | TypeScript |
| **关注点** | 分布式规模 | 隐私 |

### 战略价值

OpenAgents 代表代理部署的**分布式云**方法，与 QuantumClaw 的**本地优先**哲学形成对比。它展示了 TypeScript 如何成为 OpenClaw 之外代理框架的一流语言。

---

## 跨框架分析

### 分类法比较

| 框架 | 部署 | 协议 | 用例 | 架构 |
|------|------|------|------|------|
| **SmolAgents** | 混合 | 代码生成 | 研究 | 单一 |
| **LangGraph** | 云 | 图 | 企业 | 多 |
| **mcp-agent** | 云 | MCP | 两者 | 单一 |
| **CrewAI** | 混合 | 自定义 | 两者 | 多 |
| **AutoGen** | 云 | 对话 | 两者 | 多 |
| **Swarms** | 云 | 自定义 | 企业 | 多 |
| **OpenAgents** | 云 | 自定义 | 企业 | 多 |

### 关键见解

1. **MCP 生态** — mcp-agent 代表 MCP 原生方法；claw 平台将 MCP 添加为适配器
2. **多代理模式** — 四种不同的模式：对话式（AutoGen）、基于角色（CrewAI）、领导-工作者（ClawTeam）、基于图（LangGraph）
3. **企业 vs 个人** — 企业编排（LangGraph、Swarms）和个人助手（SmolAgents、mcp-agent）之间存在明显分歧
4. **语言分化** — Python 主导外部框架；TypeScript 正在增长（OpenAgents）

### 与 Claw 生态的集成

**竞争分析：**
- **SmolAgents vs Nanobot** — 不同的极简主义方法（代码生成 vs 工具调用）
- **LangGraph vs ClawTeam** — 图 vs 领导-工作者协调
- **mcp-agent vs 启用 MCP 的 claws** — 原生 vs 适配器方法
- **CrewAI vs ClawTeam** — 角色扮演 vs 任务依赖协调
- **Swarms vs GoClaw/HiClaw** — Python vs Go 企业编排

---

## 结论

这 7 个外部框架代表了 AI 代理开发的重要行业方法：

- **SmolAgents** 演示了最小代码生成方法
- **LangGraph** 领导基于图的编排
- **mcp-agent** 是 MCP 参考实现
- **CrewAI** 开创了基于角色的多代理系统
- **AutoGen** 代表对话式代理协调
- **Swarms** 专注于 Python 企业编排
- **OpenAgents** 探索分布式云部署

与 13 个 claw 生态平台一起跟踪这些框架，提供了 2026 年 AI 代理格局的全面覆盖。

---

*最后更新：2026 年 5 月 5 日*
*所属：AllClaws 个人 AI 代理生态系统研究*
