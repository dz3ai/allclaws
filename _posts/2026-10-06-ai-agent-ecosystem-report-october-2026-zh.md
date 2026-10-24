---
layout: post
title: "AI Agent 生态月报:2026 年 10 月 —— 从正确性到节奏"
lang: zh
date: 2026-10-06 22:37:00 +0800
author: Danny Zeng
categories: [月度报告]
tags: [ecosystem, monthly-report, release-train, guardian-v2, deslop, anti-mock, kimi-cli, reasonix-studio, billing-transparency, openclaw, hermes, codex]
---

九月月报给这个季度定名的模式是**正确性攻坚**——头部平台在清偿长周期运行暴露的工程债。进入十月两周,这场攻坚没有结束,而是被*制度化*了。Hermes 现在几乎每天打一个 canary tag,八天里为 v0.21.5 烧掉 28 个 release candidate——光 9 月 29 日一天就 16 个——几乎每个都留下一块 `abandoned-rc.*` 墓碑 tag,而正式版至今未发。Codex 十四天发了十个正式版(rust-v0.156.1 → v0.160.1),同时并行推进一条深达十五个构建的 alpha 列车。OpenClaw 同时维护四条版本线——v2026.7.35、v2026.8.33–35、v2026.9.6–9.8、v2026.10.1-beta.1——并且本窗口 8,262 个 commit 里有 440 个的标题共用同一个动词:*deslop*(去糊)。

本报告数据窗口 **9 月 20 日 – 10 月 6 日**(29 个 submodule,远端分支日志 10 月 6 日采集,与 09-22 周报交叉验证)。核心论点:正确性是九月的故事,**节奏**——发布通道、质量教义、审查流水线、账单可见性——是十月的。挺过正确性攻坚的平台,正在把它转化为流程。

---

## 发布列车到站

本窗口最醒目的跨生态变化:*发布不再是事件,而是通道*。

**Hermes-Agent**(9,001 commits)跑着最显式的列车:窗口内 11 个 `v0.21.4+canary.<date>` tag,大多盖在 07:00Z 前后几分钟;八天内 rc.7 到 rc.35 冲向 v0.21.5;以及最关键的细节——29 个 `abandoned-rc.*` tag 被保留而非删除。失败的发布候选留作墓碑,这是带审计轨迹的发布工程,不是打版本号。

**Codex**(806 commits)每 1–2 天一个正式版,同时 `0.162.0-alpha.5 → alpha.15` 列车已跑到两个 minor 之后。**GoClaw** 窗口内打了 16 个 tag(v3.15.0-beta.213 → beta.228),日更 beta,正式版呼之欲出。**Copilot-CLI** 发布 `1.0.92-0` 到 `-5` 六个后缀构建——一个版本六个 build——公开仓库里只见 changelog commit,真实开发显然在别处进行。**NanoClaw** 做了件更罕见的:从 semver(v2.4.0,9 月 23 日)迁到 CalVer(v2026.10.0-rc.1/rc.2),*同一周*还上线了默认跟随 release tag 的 update channels(#3986)——版本体系与分发体系一起重设计。

**Reasonix**(623 commits)现在跑四条并行线:核心 `v1.38.12 → v1.39.7`(九个版本)、`desktop-`/`npm-` 镜像线,以及 `studio-` 线——八月 v2.0.0 起就在日更,窗口内 `v2.19.0 → v2.28.0`,十二天十四版——直到 10 月 4 日,studio 的版本号直接成了仓库不带前缀的 `v2.28.0` tag。**OpenClaw** 的四条线里包含*backport 维护*:v2026.8.34/35 和 v2026.7.35 与 9.x 线在同一双周内发布——不管叫不叫 LTS,这就是 LTS 的样子。

合起来读:版本号正在变成基础设施。问题不再是"什么时候发版",而是"你在哪条通道上"。

## 质量教义

九月的正确性修复是战术性的;这个窗口它们有了名字——而名字就是教义。

**OpenClaw** 的叫 *deslop*:440 个 commit(`deslop commands #165696`、`deslop error handling and normalization #165601`、`deslop UI accidental complexity #165647`、`deslop non-channel tools #165707`),外加 674 个 `perf(...)`——sessions 共享列表视图、models 复用已编译的 catalog routing facts。用词本身就是宣言:agent 时代积累的代码是*糊*,糊要一个子系统一个子系统地系统性清除。

**Dify**(407 commits)的叫*反 mock*:窗口内 53 个 commit 把测试从 spec-based mock 改写为真实边界——"use real data source auth gateways"、"use real object storage SDK responses"、"use real HTTP responses and plugin tool clients"——并用 ast-grep 守卫(#43232)*机器强制*封禁 mock 构造器。测试套件正在去虚构化,而且规则由工具执行,不靠 reviewer 把关。

**Eliza**(develop 分支 4,838 commits)的叫*整合*:142 个 commit 扁平化包结构、合并 CLI helper、统一 OS 工具链,都在上月成文的 crash-only 错误教义之下。**ZeroClaw**(210 commits,v0.8.5 后无发布)把治理本身做成了 commit 流:六个 `docs(runtime)` commit 提议对组合规则的*有界豁免*——并把每一项的"Core Team 批准"记录进仓库(#11521)。一部带成文修正程序的宪法,写在 git 里。

一个需要延续的警告:**OpenHuman** 的 9,729 个 commit 里有 470 个是自动生成的 `chore: files changed ...`;八月定下的 bot 折扣规则比以往任何时候都更需要。那里的真实信号是 v0.64.x 线(五个版本)和自设"layout limit"纪律下的 memory-v2 spec 工作。

## Guardian 长大成人

Codex 十六天记了 **63 个 Guardian commit**。我们在[《谁来审查审查者?》](/allclaws/blog/2026/09/21/agent-reviews-agent-part1/)(9 月 21 日发布,系列第一篇)里解剖过的审查流水线,正在公开地硬化:**Guardian V2** 的响应计时锚定 snapshot 采样(#51065)、审查可从父检查点恢复且每次尝试的 flag 相互隔离(#51137/#51139/#51140)、Decisions 可回退到 `OPENAI_API_KEY`(#51133)、审查请求保留 trusted-tool 上下文(#51070)、MCP elicitation 审查携带发起步骤上下文(#51067)。恢复、隔离、回退、上下文溯源——这是一套跑在生产里的审查系统的失败模式,正被逐个关闭。

反例同样有教育意义:**Kimi-Code** 上线 workspace trust 边界加固后*回滚*(#4013,9 月 24 日),四天后以 opt-in 环境变量(#4059,9 月 28 日)+ 展示配置来源的 trust summary(#4056)重新落地。破坏工作流的安全加固会被撤回,并以"可见性优先"重新接近。连 2.0 时代的 Moonshot 工具也在公开学习 guardrail 的用户体验。

## 账单变得可见

九月月报把账单不透明列为生态里最响亮的未满足需求。两周之内,第一批具体答案落地了——落在 Hermes:桌面端出现**在订阅撞上用量墙之前预警的 progress chip**,模型选择器里**被限流的 provider 会说明原因和截止时间**(均为 10 月 5 日)。ZeroClaw 则修复了 delegation-chain 成本上限——重访的 alias 花费只计一次(#11287)——多 agent 成本核算获得了与会话相同的身份语义。还不是 token 级记账,但方向已经调头:用量状态从用户翻日志挖,变成平台主动*展示*。

## 合并、复活、吸收

**Kimi-CLI 死了;Kimi-Code 万岁。**09-22 周报预告的归档已完成:1.51.0 是最后一次功能版本,1.52.0(9 月 22 日)是墓碑版,入口 short-circuit 到 Kimi Code 安装器(#2666)。这是 Tier-1 追踪名单中**第一个被上游正式归档的平台**——AllClaws 的治理规则(Q4-6)在季度 review 迎来第一个真实的移除决定。

**Browser-Use 醒了。**一个月 docs-only 静默之后,38 个 commit 汇成 **Anthropic browser toolset driver**(#5966,10 月 1 日)加一整套文档战役。九月的"产品叙事调整期"原来是集成准备期。

**OpenWorker**(146 commits,v0.3.0)整个窗口扑在 **OpenShell** 上——带站点 allowlist 的沙箱 shell、Docker Desktop host-networking 安装流、发布的 CLI 镜像。**RocketRide** 一次性发齐整个客户端家族(server-v3.4.0、TypeScript/Python v1.4.0、MCP v1.5.0、n8n-nodes v0.1.0),并启动了下一班的 prerelease 列车。

前沿模型的吸收速度还在压缩:GoClaw 上线 **Claude Opus 4.7+ 与 Claude 5 的 adaptive thinking**(9 月 29 日),同一簇 commit 里还有 redacted-thinking 回放和 dated-snapshot 处理;Nanobot 加入 **GPT-6 temperature 限制**;AgentScope 在服务层 SOP 与 TeamPipeline 之外官宣 **MiniMax 支持**(v2.0.9)。新模型发布现在是按天计的平台工作项,不再按季度。

## 平台活跃度总览

| 平台 | 关键变化 | 活跃度 |
|----------|-------------|----------|
| OpenClaw | 四条版本线;deslop 战役(440);v2026.9.6–9.8、v2026.10.1-beta.1 | 🔴 |
| Hermes-Agent | 近乎每日 canary;28 个 RC + 29 块 abandoned-rc 墓碑;用量墙 UX | 🔴 |
| OpenHuman | v0.64.0–0.64.10;memory-v2 spec;layout-limit 纪律 | 🔴 |
| Eliza | 整合/扁平化(142);crash-only 教义;云账单证据留存 | 🔴 |
| Codex | 10 个正式版;Guardian V2 硬化(63 commits);rust-v0.160.1 | 🔴 |
| Reasonix | Studio v2.19→2.28(十二天十四版);核心 v1.39.7;九个核心版本 | 🟠 |
| PraisonAI | 会话/transcript 持久化修复;v4.7.10–4.7.12 | 🟠 |
| Dify | 反 mock 测试战役(53);strict typing;1.17.1 后无发布 | 🟠 |
| Nanobot | subagent 任务消息 + 取消;WebUI 触屏 blitz;GPT-6 限制 | 🟠 |
| ZeroClaw | RPC fencing;typed stop taxonomy;有界豁免治理 | 🟠 |
| OpenWorker | v0.3.0;OpenShell 沙箱 + allowlist UX;CLI 镜像 | 🟡 |
| NanoClaw | CalVer 切换 + update channels;v2026.10.0-rc.2;Baileys spoofing pin | 🟡 |
| AgentScope | v2.0.9;服务层 SOP;TeamPipeline;MiniMax | 🟡 |
| RocketRide | 客户端家族齐发;n8n nodes;C++ Microsoft nodes | 🟡 |
| GoClaw | 16 个 tag(beta.213→228);Claude 5 / Opus 4.7 adaptive thinking | 🟡 |
| Browser-Use | 复活:Anthropic browser toolset driver;文档战役 | 🟡 |
| Kimi-Code | 2.1.0/2.1.1;workspace-trust 回滚→重落地;tower 中断 | 🟡 |
| HiClaw | v1.2.4;matrix-channel 与 teamharness 修复流 | 🟡 |
| Agent-Zero | v2.13(9 月 23 日)后 main 静默;活动移至 `ready` 分支 | 🟢 |
| IronClaw | v1.4.1 发在 `release/2026-08-26`;tracked main 自 9 月 10 日冻结 | 🟢 |
| Copilot-CLI | 1.0.89–1.0.92 仅 changelog;1.0.92 六个构建 | 🟢 |
| Kimi-CLI | **上游正式归档**(9 月 21 日);终版 1.52.0 | ⚫ |
| ClawTeam / MaxClaw / Claw-AI-Lab / Aider / MetaGPT / Qwen-Agent | 休眠(13 周 – 8+ 个月) | ⚫ |

## AllClaws 项目动态

发布流水线交付了两篇系列文章:**《谁来审查审查者?》**(9 月 21 日,Agent 审查 Agent 系列第一篇,四个平台的审查架构对比)和**《MCP 是协议——那你为什么还在看护进程?》**(9 月 24 日,中英双语,由每周微信草稿转化——Hermes Connectors 与 MCP 依赖化转向)。09-22 周报记录了 kimi-cli 归档,并把模型路由定名为最强跨项目范式信号。

**Q4-4(long-running benchmarks)于 10 月 6 日进入 Phase 2**,交付 S4 `triage-burndown` fixture——疲劳测量仪:一个 376 行、纯标准库的 metrics 库,种入 5 个相互独立、同难度的 bug,每个配 issue 文档和 documented-red 测试;隐藏验收套件在原始仓库上必 FAIL、打上参考补丁后 PASS;`check_windows.py` 是疲劳引擎的按窗口评分契约(scratch 上验证 58/58)。Phase 1(S1–S3 场景、aider/codex/kimi-cli 驱动、runner + cost + scoring)于 8 月 24 日交付。Phase 2 剩余:reasonix/opencode/smolagents 驱动、S5 `legacy-migrate`,然后是第一个真实的 long-run 网格。

追踪卫生:IronClaw 分支漂移加深(v1.4.1 发在 `release/2026-08-26`,tracked `main` 自 9 月 10 日冻结)——季度 review 应决定是否重新 pin。Agent-Zero 出现同款的早期症状(main 自 9 月 23 日静默,`ready` 分支活跃)。

## 展望十月余下

**(1)** Q4-8 范式持久性复查,本月到期:模型路由持续扩散(Agent-Zero 的 scoped subagent presets、GoClaw 的按模型 thinking 策略),案情加强;其余四个范式等判决。**(2)** Phase 2 驱动落地后的首批 Q4-4 long-run 结果——deslop/反 mock 教义在 45 分钟会话里、按窗口测量,到底站不站得住?**(3)** 治理季度 review:kimi-cli 移除(Tier-1 首个上游归档)加上九月悬置的 MetaGPT/Qwen-Agent 裁决。**(4)** 发车表:Hermes v0.21.5 正式版、NanoClaw v2026.10.0、GoClaw 3.15.0、OpenClaw v2026.10.1——四班列车同时进站。

---

*[English version](/allclaws/blog/2026/10/06/ai-agent-ecosystem-report-october-2026/)*

*数据来源:2026-10-06 采集的 29 个 submodule 远端分支日志(窗口 9 月 20 日 – 10 月 6 日)、09-22 submodule 周报、GitHub tag/release 交叉验证。commit 计数在注明处包含 CI/merge 噪声。项目:[dz3ai/allclaws](https://github.com/dz3ai/allclaws)。*
