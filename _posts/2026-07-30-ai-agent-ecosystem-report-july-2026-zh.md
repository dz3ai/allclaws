---
layout: post
title: "AI Agent 生态报告：2026 年 7 月"
date: 2026-07-30 23:55:00 +0800
author: Danny Zeng
categories: [月度报告]
tags: [生态系统, 月度报告, dify, openworker, nanobot, agentscope, mcp, 上下文压缩, 基准测试, 架构]
lang: zh
---

2026 年 7 月，是 AI agent 平台走向成熟的一个月。不是能力上的成熟——它们早就足够强大了——而是在那些不那么光鲜、却真正区分 demo 与生产系统的工程工作上成熟了。上下文压缩（context compaction）成为平台的一等公民。安全加固从"事后想到"变成了发布阻塞项。中国生态展示了它作为拥有独立引力的平行宇宙。而支撑这一切跟踪的基准测试基础设施，平台覆盖率从 26% 跃升至 76%。

本月 AllClaws 跟踪了 34 个平台（7 月初为 30 个），新增 7 个 submodule，发布 7 份研究报告，产出 6 篇博客，并将基准测试引擎升级到覆盖 34 个平台中的 26 个、140 项真实指标。以下是这个月生态圈发生的事情。

---

## 趋势一：上下文压缩军备竞赛

2026 年 7 月最重要的技术主题，是全行业把上下文管理当作核心平台能力的转向。

**OpenWorker** 发布了四部曲的压缩系列（OPE-27）：加固 smoke test 以应对每轮事件循环、新增带测试的纯压缩模块、构建带失败策略和持久化的引擎钩子，以及接入设置覆盖和 GUI 分隔线。这不是一个补丁——这是一套完整的架构，专门管理 agent 上下文窗口填满之后会发生什么。

**Nanobot**（HKUDS，v0.3.0）发布了"保留 Responses 推理状态并压缩上下文"——让 agent 在上下文压缩边界之间维持推理链。他们 7 月 25 日的 v0.3.0 是发布以来最重要的一次更新，还包括会话空闲锁、缓冲输出边界和无效空闲压缩时间戳容忍的修复。这个版本引入的 AgentLoop/AgentRunner 分离，是我们目前在所有 Python agent 平台中见过的最干净的职责分离。

**Hermes-Agent** 修复了压缩摘要的角色选择——按模板可见的交替来选择摘要角色，而不是简单复用最后一个角色。修复很细微，但它防止了压缩破坏对话语义。

这为什么重要？我们跟踪的每一个 agent 平台最终都会撞上同一堵墙：上下文窗口是有限的，任务是无界的，而粗暴截断会搞坏 agent。把压缩解决好的平台，才可能在真实的、长达数小时的任务上工作。解决不好的，会一直困在 demo 模式里。

---

## 趋势二：生产级安全加固

2026 年 7 月，多个平台把安全不再当作功能，而是当作前提。

**Nanoclaw** 合并了加固 agent 镜像的 PR——用拉取预加固的容器镜像取代之前的"自己构建"方案。他们新增了 `--init` 和 `--shm-size` 标志，移除了按组覆盖，并将加固与主线对齐。传递的信息是：安全默认值应该来自平台，而不是用户的 Dockerfile。

**AgentScope** 在中间件层新增了 `on_check_permission` 钩子（PR #2001）——为授权 agent 行为提供了程序化的控制点。加上本月新增的 Apple Container 和 Bubblewrap 工作区后端，AgentScope 正在为分布式 agent 构建一个严肃的安全故事。

**Agent Zero** 加固了远程 Linux computer-use 的目标定位——正是那种 agent 控制远程机器时、一旦定位不准就可能造成破坏的场景。

**OpenWorker** 将 `mcp<2` 锁定，因为发现 MCP 2.0.0 移除了 `streamablehttp_client`——一个可能静默破坏生产集成的破坏性变更。这种供应链意识，正是生产软件与研究代码的分水岭。

---

## 趋势三：模型提供商爆炸

各平台竞相支持所有可用的模型提供商。"只支持 OpenAI"的假设已经死了。

**Agent Zero** 新增 Cerebras 作为模型提供商——把超低延迟推理带进 agent 工作流。

**AgentScope** 新增 Kimi K3（Moonshot）支持，并重构了 OpenAI 客户端以在多次调用间复用 `AsyncClient` 实例，而不是每次调用都新建（PR #2063）——这个性能修复让多代理系统的连接开销降低了数量级。

**GoClaw** 为 Codex 瞬时响应失败增加了重试逻辑，并支持免重启刷新每用户 MCP 凭据——对凭据轮换不应意味着停机的生产部署至关重要。

**Hermes-Agent** 合并了 composer 一致性修复，并清理了过期的提供商告警。

模式很清晰：agent 不能再假设单一模型后端。多模型支持已经是基本盘，而能优雅处理模型切换的平台（连接池、重试逻辑、凭据管理）正在拉开差距。

---

## 趋势四：中国生态进入焦点

本月 AllClaws 新增了三个中国平台——Dify、MetaGPT 和 Qwen-Agent——此前我们的 Q3-6 研究揭示了这个合计 GitHub 星标超过 35 万的生态。

**Dify** 发布了 v1.16.0（7 月 17 日）和 v1.16.1（7 月 28 日，缺陷修复与安全增强）。这个发布节奏——大版本，然后 11 天后的安全补丁——反映了生产成熟度。他们的提交记录展示了深度重构：治理公共组件 API、收窄应用列表上下文、让技能包上传大小可配置。

**Coze Studio**（字节跳动）自 4 月以来没有推送，让人对其开源承诺产生疑问。商业版 Coze 产品大概率仍然活跃，但开源仓库可能处于定期同步而非持续开发的状态。

**MetaGPT** 仍处于开发暂停——最后一次推送是 2026 年 1 月，最后一次发版是 2025 年 3 月（v0.8.2）。坐拥 69K 星，它是 agent 生态中知名度最高的停摆项目。

---

## 趋势五：大稳定化

多个平台发布了专注于稳定性而非功能的版本：

- **HiClaw v1.2.0** — Worker 存储同步的 I/O 放大修复、诊断循环预防、旧版存储前缀兼容。更大的故事是 v1.1.0：从单容器单体完全重写为无状态 worker 的 Kubernetes CRD operator 模式。
- **Dify v1.16.1** — 安全修复与缺陷修复
- **Nanobot v0.3.0** — 推理状态保留、会话锁修复、输出边界
- **OpenWorker v0.1.6** — 压缩加固、MCP 版本锁定

行业正在从"快速发布功能"转向"让已有功能真正可用"。这正是 agent 平台从实验品变成基础设施的拐点。

---

## 趋势六：基准测试基础设施成熟化

本月 AllClaws 内部最大的变化是基准测试覆盖率的跃升。运行时基准测试引擎从 9 个平台的原型进化为 26 个平台的生产系统：

- **58 → 140 项指标**：清理幽灵平台引用（quantumclaw、mcp-agent、rtl-claw），新增 monorepo 路径解析、`setup.py` 支持、递归 manifest 搜索
- **CLI agent 基准测试**：新的 `_run_cli_platforms()` 方法通过分发逻辑处理 Node、Rust 和 Python CLI agent。kimi-cli、kimi-code、codex、reasonix 和 rocketride-server 全部产出真实数据
- **真实冷启动测量**：reasonix（npm install + build 之后 287ms、81.8MB）和 codex（pnpm install 之后 32.5ms、52.7MB）——项目中第一批真实的 CLI agent 性能数据
- **Docker 沙箱扩容**：11 → 15 个沙箱服务，现已覆盖 Dify、MetaGPT、Qwen-Agent 和 OpenWorker

基准测试的缺口正在收窄。34 个跟踪平台中，26 个已有真实指标（76% 覆盖率）。其余 8 个要么没有本地检出（5 个外部框架），要么是纯文档仓库（copilot-cli、openagents、openfang）。

---

## 平台活跃度总览

| 平台 | 关键变化 | 活跃度 |
|------|---------|--------|
| Dify | v1.16.0 + v1.16.1，UI 重构，技能包 | 🔴 极高 |
| OpenWorker | 压缩引擎（OPE-27），MCP<2 锁定，v0.1.6 | 🔴 极高 |
| Nanobot | v0.3.0，AgentLoop/Runner 分离，上下文压缩 | 🟠 高 |
| AgentScope | Kimi K3，权限钩子，工作区后端 | 🟠 高 |
| Hermes-Agent | 压缩修复，composer 一致性，CI 加固 | 🟠 高 |
| HiClaw | v1.2.0 缺陷修复 + v1.1.0 K8s operator 重写 | 🟡 中 |
| GoClaw | MCP 凭据刷新，Codex 重试，Upsert store | 🟡 中 |
| Agent Zero | Cerebras 提供商，代理支持，Linux 加固 | 🟡 中 |
| Nanoclaw | 加固 agent 镜像，容器加固 | 🟡 中 |
| Eliza | CI 稳定化，多提供商重写，e2e 修复 | 🟡 中 |
| Copilot CLI | v1.0.69-76（7 个版本，仅 changelog） | 🟢 低 |
| MetaGPT | 无活动（2026 年 1 月起停摆） | ⚫ 停滞 |
| Coze Studio | 2026 年 4 月起无活动 | ⚫ 停滞 |

---

## AllClaws 项目更新

本月 AllClaws 自身也发生了重大变化：

**平台**：30 → 34（新增 OpenWorker、Dify、MetaGPT、Qwen-Agent）。同时将 kimi-cli、kimi-code 和 codex 检出为完整 submodule。

**研究报告**：本月发布 7 份报告：
- Q3-5 失败模式分类（34 个平台中的 13 种失败模式，441 行）
- Q3-6 中国 AI Agent 生态（14 个项目，合计 35 万+ 星标，325 行）
- 架构漂移报告（分析 9 个平台，识别 4 个趋势，285 行）
- 以及此前 4 个 MCP 深度 dive 阶段和设计范式分析

**博客**：6 篇新文章——中国生态、失败模式、2 篇生态分析、月度报告，以及生态报告本身。

**架构文档**：5 份文档全面更新（+642 行，中英同步）：
- `external_frameworks.md` — 7 → 11 个框架（新增 OpenWorker、Dify、MetaGPT、Qwen-Agent）
- `architecture_comparison.md` — HiClaw v1.1.0 多容器重写、Nanobot v0.3.0 AgentLoop/AgentRunner、对比矩阵扩展到 17 列
- `governance_frameworks_analysis.md` — AgentScope 工作区后端 + 权限钩子
- `mcp_ecosystem_deep_dive.md` — 第 6 部分：上下文压缩与 MCP 工具状态

**基准测试引擎**：v3.0.0 Python 套件，26 个平台 140 项指标（76% 覆盖率），带 monorepo 入口解析的 CLI agent 基准测试，reasonix 和 codex 的真实冷启动数据。

**CI**：所有 workflow 全绿——修复了 Jekyll Pages 部署（时区）、Node 24 迁移（FORCE_JAVASCRIPT_ACTIONS_TO_NODE24）、沙箱健康检查（15 个容器）、Benchmark Suite 每日运行通过。

**ROADMAP**：原 H2 2026 全部 7 项完成。新增 6 项（Q3-5/Q3-6 已完成，Q4-4/Q4-5/Q4-6 已规划）。README 的 roadmap 部分已更新以反映实际交付状态。

---

## 展望：2026 年 8 月

四件值得关注的事：

1. **MCP 2.0 余波** — OpenWorker 锁定 `mcp<2` 表明 MCP 2.0 存在破坏性变更。随着更多平台遇到这个问题，预期会出现一波兼容性修复（或一次协调迁移）。

2. **MetaGPT 的命运** — 69K 星、6 个月无活动，MetaGPT 正在逼近"归档"阈值。如果 8 月在没有提交的情况下过去，它将进入我们的停滞复审队列。

3. **上下文压缩收敛** — OpenWorker、Nanobot 和 Hermes-Agent 在独立解决同一个问题。预期会出现共享模式，可能以 MCP 扩展或跨平台标准的形式正式化。我们的架构文档现在在三份文档中跟踪这一趋势。

4. **基准测试覆盖天花板** — 在 76%（26/34）的覆盖率下，剩余缺口要么需要 submodule 检出（5 个外部框架），要么需要根本性的结构变化（copilot-cli 是纯文档仓库）。下一个前沿是为所有 Node 平台执行 npm install + build，以获得整个生态的真实冷启动数据。

---

*AllClaws 跟踪 5 大类别的 34 个 AI agent 平台。数据通过 GitHub API 和本地基准测试套件收集，2026 年 8 月 1 日。完整研究报告见 [github.com/dz3ai/allclaws](https://github.com/dz3ai/allclaws)。*

*[English version](/allclaws/blog/2026/07/30/ai-agent-ecosystem-report-july-2026/)*
