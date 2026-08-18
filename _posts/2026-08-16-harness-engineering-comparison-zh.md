---
layout: post
title: "可靠性从哪来：34 个 AI Agent 平台的 Harness 工程对比"
date: 2026-08-16 22:10:00 +0800
author: Danny Zeng
categories: [研究]
tags: [harness-engineering, 架构, agent可靠性, 验证, 预算, 上下文压缩]
lang: zh
---

Prompt engineering 教会我们「好好说话」。Harness engineering（驾驭工程）教会我们别再指望说话。

这正是当下 AI agent 平台几乎所有动向底层的那个转变。Prompt 是*建议*——模型可能尊重它、重新解读它，或者在上下文压力下悄悄无视它。Harness——包裹模型的运行时系统：工具循环、上下文组装、沙箱、权限、预算、追踪——是*法律*。它是概率核心外圈的确定性代码，决定模型的能力有多少能在真实任务的接触中幸存。

我们刚把 AllClaws 跟踪的全部 34 个平台按四域 harness 框架打完分：核心架构、安全与验证、执行控制与状态、企业集成与协调。完整报告里有 20×10 覆盖矩阵。这篇博客讲的是让我们意外的东西。

---

## 每家对可靠性的押注都不一样

把 34 个架构并排读完，第一件事你会发现：没有人就「可靠性从哪来」达成共识。每个平台的押注都不同。

**OpenClaw** 押路由——一个横跨 37+ channel、吸收复杂性的消息织物。**ClawTeam** 押编排——TOML 依赖链让 worker 在前置任务完成前*根本无法*启动。**GoClaw** 押治理——五层防御、按租户加密、审计日志。**IronClaw** 押隔离——每个工具调用包进带能力权限的 WASM 沙箱。**OpenWorker** 押人类——每个后果性动作一道审批门。**reasonix** 押钱——会话预算到 100% 时拒绝下一轮。**LangGraph** 押显式状态——类型化图的每个节点都有 checkpoint。

这些押注没有一个是错的。刺眼的是：没有一家覆盖全部四个域。生态没有在收敛于某个 harness 设计——它在并行投机，赌哪个单一控制点最重要。

---

## 状态机赢了。预算没来。

按「强实现数量」给各域排成熟度，结果清晰。执行状态——把 agent 运行时当状态机而非孤立 API 调用——是最成熟的能力，9 个强实现。上下文管理 8 个，紧随其后。

状态机故事有两个主角。**LangGraph** 是教科书版：类型化状态、每节点 checkpoint、human-in-the-loop 建模为图边。但更有意思的是 **NanoClaw** v2——它把状态机*物理*实现了：每个会话两个 SQLite 文件——host 写一个，容器写一个——每个文件恰好一个写者，奇偶序号。消息状态和执行状态在存储层分离。当你可以靠查数据库来审计对话时，「黑盒」这个反对意见就开始瓦解。

排名垫底的是预算。两个平台。在有像样 harness 故事的二十家里。

**reasonix** 是生态中唯一带硬性花费门禁的 CLI——`--budget <usd>` 在 80% 时警告，100% 时*拒绝下一轮*。不是警告，是拒绝。配上每次调用可设推理强度的 `--effort` 旋钮（harness 研究者所说的 Reasoning Compute Sandwich 的实操形态——规划和验证用强推理，中间执行用便宜的），它把 token 经济学当工程约束，而不是事后审的账单。**AgentScope** 把预算做成可组合的循环 middleware——同一想法的程序化版本。

那个最能预测 agent 能否在生产环境无人值守存活的能力，只有两个实现。生态早就解决了「别崩溃」，还没解决「别超支」。

---

## 危险的缺口：没人验证声明

这个发现应该让所有人不安。

我们今年早些时候的失败模式研究把 **Silent Success（静默成功）** 识别为生产 agent 最危险的失败：agent 报告任务完成，输出是错的或从未执行，用户信任了报告。解药是验证钩子——对*声明*而非动作的独立检查。

全部被跟踪平台中，有近似机制的只有四家。而**运行独立审计模型来检验主 agent 产出的，一家都没有。**

现有的机制拦的是别的东西。审批门（**OpenWorker**）在动作发生前拦*动作*——人类审命令。权限钩子（**AgentScope** 的 `on_check_permission`）以程序化方式拦*未授权调用*。审计日志（**GoClaw**）事后记录发生了什么。都有价值。没有一个回答那个真正要紧的问题：*agent 的成功报告是真的吗？*

不对称是结构性的。模型被训练得乐于助人；被问「你做了 X 吗？」时，先验答案是「是」。一个从不独立验证产出的 harness，对这种先验毫无防御。四域框架要求一个独立的审计模型来裁决输出。在被跟踪的平台里它不存在。这是生态最危险的洞，也是一片空旷的市场。

---

## 应验的预测，和没应验的

harness 框架给了一个具体的成本预测：子 agent 团队应该共享 KV cache——主 agent 和 worker 复用相同的已计算 prompt 前缀——让编排变得便宜。我们去找了。

它不存在。34 个平台里一个都没有。最近的邻居是 **reasonix** 的 cache-first 循环——规范化 prompt 以最大化 DeepSeek 上下文缓存命中——但只在单会话内，从不跨 agent。**ClawTeam** 的公开数据（5 个并行 agent 约 3 小时完成全栈应用，对比串行 8 小时以上，token 成本*相同*）纯靠并行达成。跨 agent 缓存共享是明晃晃摆在那里的未兑现价值。

有一个相关性成立，但框架里没写：语言预测 harness 哲学。Rust 平台（**IronClaw**、**ZeroClaw**、**codex**、**OpenFang**）把 harness 表达为*运行时属性*——沙箱、确定性、`estop` 紧急停止命令。Python 平台（**Hermes**、**Nanobot**、**AgentScope**）把它表达为*循环结构*——middleware、压缩引擎、AgentLoop/AgentRunner 分离。Go 平台（**GoClaw**、**HiClaw**）把它表达为*基础设施*——lane-based 调度器、Kubernetes 风格控制面。你用什么语言构建，决定了你甚至能*看见*哪些 harness 问题。

---

## 未探索的中间地带

门禁哲学最深的分裂，跑在「全部人类侧把关」和「全部机器侧把关」之间。**OpenWorker** 和 **NanoClaw** 的 guard seam（allow / hold / deny，还有别处不存在的自我修改防护）在每个后果性步骤放上人类或硬规则。**GoClaw** 的 RBAC 和 **IronClaw** 的能力系统把权限编码为机器强制执行的策略。

两者之间躺着一块未开发的设计空间：概率模型由概率裁判验证，只在两者分歧时才触发确定性门禁。一个审计模型读主 agent 的产出、挑战它、只在冲突时升级给人类。它会把个人范式的自主性和企业范式的保证结合起来。没有被跟踪的平台在做它。

补上验证缺口的平台——不是靠更大的模型或更好的 prompt，而是靠检查工作的 harness 代码——才是能从「令人惊艳」毕业到「值得信任」的那些。harness 才是发生这件事的地方。prompt 从来都不是。

---

*本文基于完整研究报告：[Harness Engineering Comparison: Philosophy, Design, and Features Across Tracked Platforms](https://github.com/dz3ai/allclaws/blob/main/docs/reports/harness-engineering-comparison.md)，含 20×10 覆盖矩阵与各平台评级。*

*[English version](/allclaws/blog/2026/08/16/harness-engineering-comparison/)*
