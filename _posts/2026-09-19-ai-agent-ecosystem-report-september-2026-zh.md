---
layout: post
title: "AI Agent 生态月报:2026 年 9 月 —— Q3 综述"
lang: zh
date: 2026-09-19 20:37:00 +0800
author: Danny Zeng
categories: [月度报告]
tags: [ecosystem, monthly-report, q3-synthesis, guardian, session-log, correctness, codex, reasonix, hermes, openclaw, paradigms]
---

九月为这个季度收了尾。AllClaws 在 Q3 立下的问题——*编目完成之后,研究该往哪走?*——答案写在三周周报里:头部平台集体进入了一个功能清单无法描述的阶段,**正确性攻坚**。OpenClaw 每周四千个 commit,花在收敛资源占用而不是堆新功能;Hermes 把 cron 调度器的边界条件逐条封死——早触发、手工触发、时钟偏移、未来实例污染;Reasonix 重写了会话 turn 权威模型;Codex 用八个连续提交把审查能力收敛成一个 extension。这些改动没有一项能放上产品幻灯片,但每一项都在决定:平台跑到第七天,还是不是对的。

本报告综合九月(数据窗口 9 月 1–19 日)与 Q3 研究主线。月报节奏从"每月第一个周一"滑到了 9 月 19 日——这个延迟本身就是本季度真实故事的注脚:AllClaws 从月度快照转向了周度仪器,而周度信号才是新闻发生的地方。

---

## 正确性攻坚

九月的定义性模式:头部平台在清偿长周期运行暴露的工程债。

**OpenClaw**(单周 4,208 commits)像一本成熟期教科书:sessions 复用已编译的 transcript 元数据、reminder 维护时少拉数据、participants 少写数据库、cron 在 pruning 忙时跳过可用性检查。**Hermes**(2,401 commits)的 cron 正确性修复链,commit message 读起来像形式化证明——"skewed early fire owns its armed slot"、"manual fires must not consume the next occurrence"、"reject impossible occurrence completions"——随后把 MoA 与 approval 行为包进不变量测试,最关键的一条:unattended 模式下 pattern-key allowlist 必须成立。不是写在文档里,是断言在测试里。

最有说服力的细节是*没发生*的事:顶级平台本月没有一个在发布新的 agent 范式。范式是八月来的;九月的话题是让它们在 uptime 面前活下来。这正是 ROADMAP Q4-4(long-running benchmarks)划定的问题空间——平台已经用 commit 队列投了票。

## Agent 审查 Agent

九月的第二个信号在 9 月 18 日结晶:Codex **Guardian** 的源码深读笔记落入 `docs/reports/guardian-deep-dive-notes.md`。发现的东西描述了一条两级审查流水线:非阻塞的 async scorer 加阻塞的 sync reviewer,证据按信任分级(只有用户与 developer 消息、AGENTS.md、显式用户输入回复算数),四级 user authorization 评分,以及一个熔断器——连续拒绝 3 次或 50 事件滑动窗口内拒绝 10 次,中断当前 turn。

突出的不是机械,而是姿态:**审查者本身被当作不可信**。它会轮换、可被熔断、拒绝有账可查,它读的 transcript 被当成不可信输入处理——防的正是通过被审历史注入的 prompt injection。Guardian 是制度设计,不是模型能力。

同一周,**OpenClaw** 关闭了一个 2,500 评论的 issue,打开了自己的 PR autofix 流水线——自家 agent 修自家仓库的 PR;**HiClaw** 把人类审批下沉到 team 作用域;PraisonAI、RocketRide、ZeroClaw 三家在同一窗口各自加固了 SSRF 防御。层级正在叠起来:底部硬 guardrail,往上制度约束,再往人签字,最上面 AI 盯 AI。

## Session 成为基础设施

本季度最强的趋同信号:会话数据正在成为有版本、可分叉、可审计的数据结构。

**Reasonix** schema-2 把 session 做成 append-only DAG——fork 和 rewind 是挪指针,投影免重放;本月工作继续推进,SessionID-only persistence 与 harness 式 turn 循环落地(v1.38.9,发布在 AllClaws 钉住的 `main-v2` 分支上——钉住之前,追踪指针在一条死分支后面落后了 6,621 个 commit)。**Codex** 发了 Memory v2——consolidation 与 read prompts、human-evidence 优先、版本化隔离存储——外加 Guardian context profiles。**NanoBot** 让压缩可见;**Hermes** 给 subagent 装了 live-tail dock,可 steer 可 stop。**Kimi-Code** 补上了资源治理的角度:completed subagent scope 的 LRU 驱逐、按 agent id 分片的 session event bus、MCP 工具延迟披露以削减首屏 token。

这场合流的五个范式已于 9 月 8 日正式立为 ROADMAP **Q4-8**:append-only DAG session log、memory 分层管道、subagent 可观测性、realtime voice、本地模型接入成标配。四周持久性复查定在十月初。

## 度量问题在加深

九月给八月开启的方法论故事(bot 提交打折)又添了两章。

**分支漂移从异常变成常态。** Reasonix 事件最锋利:被追踪的 `main` 分支自五月冻结,而 `main-v2` 每周跑 302 个 commit——平台天天在发货,读数却是死的。IronClaw 默认分支切回 `main`(staging 冻结在五月);Eliza 的发布面移到了 Cloud 产品上,不在 repo tag 里;Browser-Use 整月代码静默、文档重写转向 self-hosting 叙事。"这个项目还活着吗"已经无法从任何单一分支、tag 流或 star 数回答。

**计费透明度成了最响的用户痛点。** Codex 的头部 issue 是 responses 后端 404(1,123 评论)、rate-limit 成本跳升 10–20 倍(211)、以及长期占据热度榜的 token 消耗线程;ZeroClaw 社区在要求 history-trim 事件的 token 记账(113)。Agent 拿到了任意 URL 访问能力,SSRF 成了共性攻击面;账单成了黑箱。用量可观测性——*token 去了哪里*——是一个跨生态的未满足需求。

## 平台活动总览

| 平台 | 本期要点 | 活跃度 |
|------|---------|--------|
| OpenClaw | 稳定性收敛;PR autofix 上线;v2026.9.4 | 🔴 |
| Hermes-Agent | cron 正确性链条;MoA 不变量;v0.21.3 | 🔴 |
| OpenHuman | 桌面文件体验;覆盖矩阵纪律;v0.63.26 | 🔴 |
| Eliza | Cloud 上市收尾;本地推理打磨 | 🔴 |
| Reasonix | v1.38.9;SessionID-only persistence;harness turn loop | 🟠 |
| Codex | Guardian reviewer extension;Windows sandbox;rust-v0.154.0 | 🟠 |
| ZeroClaw | provider 一波;安全默认值;v0.8.5 | 🟠 |
| PraisonAI | 质量收敛;SSRF 修复;v4.7.8 | 🟠 |
| Nanobot | 修复面铺得宽;移动端 WebUI 打磨 | 🟠 |
| Dify | OpenShell runtime;协作合并;v1.17.1 | 🟠 |
| AgentScope | realtime voice 稳定性;v2.0.8 | 🟡 |
| Kimi-Code | agent-core-v2 资源治理;0.43.1 | 🟡 |
| GoClaw / NanoClaw / HiClaw / RocketRide / Browser-Use | teams 治理;OpenCode 宿主化;mermaid TaskFlow;otel bridge | 🟡 |
| Kimi-CLI / Copilot-CLI / OpenWorker | 维护级 | 🟢 |
| Aider / MetaGPT / Qwen-Agent / ClawTeam / MaxClaw / Claw-AI-Lab | 沉寂(60–140+ 天) | ⚫ |

## AllClaws 项目动态

Q3 完整收官:六项既定条目加扩展全部交付——统一对比、MCP 深度分析(5 阶段)、企业治理、失败模式分类法、中国生态、harness 架构。Q4 的 1–3 与 5–7 已在八月完成;**Q4-4(long-running benchmarks)**进行中,Phase 1 MVP 已交付;**Q4-8(新兴范式深研)**9 月 8 日立项。

基础设施长出了一条周更流水线:周二 submodule 周报(cron,首跑 9 月 8 日)、周三微信选题与草稿、周四双语博客转化。Guardian 深读笔记(9 月 18 日)支撑着一个两篇的「Agent 审查 Agent」公开系列。追踪卫生:Reasonix 钉住 `main-v2`,平台数稳定在 Tier-1 上限 35/35。

## 展望十月

三件事值得盯:**(1)** Q4-8 范式持久性复查——五个范式哪些经得起一个月的审视;**(2)** Q4-4 Phase 2 的首批 long-running benchmark 结果——正确性攻坚到底有没有回报,数据说话;**(3)** MetaGPT 与 Qwen-Agent 的治理裁决(双双越过停滞线,又都因报告引用被保留)——Q4-6 交付的归档规则迎来的第一次真实考验。

---

*[English version](/allclaws/blog/2026/09/19/ai-agent-ecosystem-report-september-2026/)*

*数据来源:周报 2026-09-08 与 2026-09-15(29 个 submodule,远端分支日志与 GitHub API 交叉验证)、Guardian 源码深读笔记。项目:[dz3ai/allclaws](https://github.com/dz3ai/allclaws)。*
