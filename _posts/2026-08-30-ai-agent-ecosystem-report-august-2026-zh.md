---
layout: post
title: "AI Agent 生态月报:2026 年 8 月"
date: 2026-08-30 23:55:00 +0800
author: Danny Zeng
categories: [Monthly Report]
tags: [ecosystem, monthly-report, ironclaw, kimi-code, codex, agentscope, governance, protocol-wars, long-running-benchmarks, divergence]
---

2026 年 8 月,生态劈成了两种速度。一边是少数平台以重新定义"活跃"的节奏出货——IronClaw 跨过 1.0 门槛、kimi-code 三十天打了十六个版本、codex 合并了上千个提交;另一边,一批昔日的高飞平台集体沉默:aider、reasonix、ClawTeam、Qwen-Agent 整月零提交。中间地带被掏空了。也是第一次,AllClaws 需要一套治理模型才能描述眼前的局面——因为"这个平台还活着吗"已经不是看一眼 star 数就能回答的问题。

本月报还标志了一次方法论升级。下面这些原始数字比以往任何月份都大——但其中约三分之一来自机器人提交、release bot 和给自家仓库干活的 triage agent。我们现在把"人类节奏的开发"与"机器节奏的空转"分开统计,而两者的分化本身就是个发现。

---

## 趋势 1:IronClaw 1.0,与"默认分支静默切换"陷阱

8 月的头条事件:**IronClaw 发布 v1.0.0**(7 月 27 日打 tag,之后一个月持续加固到 8 月 29 日)。这个在"最活跃平台"位置上坐了十八个月的平台,正式跨入生产级——类型化的 e2e provider journey、通知自动化、extension 输出所有权、以及校验集成组拓扑的 CI。

更隐蔽的故事是我们差点错过它。IronClaw 上游把默认分支切到了 `staging`——那个分支自 5 月起纹丝不动——而真正的开发在 `main` 上继续。我们的 submodule 钉在死分支上,读出来是"7 月 30 日后零提交",直到与 GitHub API 交叉核对才发现推送天天在落。同样的模式又揪出两个平台:ZeroClaw 的活跃分支是 `master`(本月 388 提交)而非 `main`,Rocketride 在 `develop` 上开发(108 提交)而 `main` 冻结。三个平台,三次无声的默认分支切换。

这值得单独立一个趋势,因为它正在变成生态习惯:团队把默认分支当发布面,在别处开发——这会悄悄弄坏每一个"默认分支 == 主干"假设的天真追踪器。我们已修复追踪(三个平台的分支配置现在都指向真实主干),并把它写进治理清单:*每季度评审必须验证默认分支就是开发主干*。

## 趋势 2:编码代理赛道,垂直起飞

如果说 7 月的主题是上下文压缩,8 月的主题就是编码代理赛道的原始速度:

- **codex** — 本月 1,202 提交。亮点不在量,而在 **Guardian V2**(#41100、#41392、#41422):共享 transcript 收集、上下文原语、以及为监督层服务的决策指标——一个审查主 agent 自身行为的第二 agent。codex 在造一个盯着第一个 agent 看的 agent。
- **kimi-code** — 300 提交,版本从 0.32.0 一路打到 0.39.1。架构上的大动作:**agent-core-v2**,一个 DI×Scope 引擎,四个生命周期层级(App/Workspace/Session/Agent),各 agent domain 正在迁移上去(#3175)。再加上自愈 wire journal(#3281)、远程控制 web tunnel(#3034)、服务端本地路径附件——MoonshotAI 交付的已经是一个 agent 平台,不只是一个 CLI。
- **Dify** — 792 提交,v1.17.0。8 月是巩固月:controller 与 service API 的深度依赖注入重构、权限门控的 skill 入口、session 作用域的 workflow 访问器。整个代码库在为多租户规模做加固。
- **AgentScope** — v2.0.7,新增 **GoalPipeline**(#2428)、钉钉渠道(#2285)、workspace 池化(#1755)、以及把长连接交给专职 worker 的 channel-worker 架构(#2390)。

编码代理类别现在是整个追踪集里最快的赛道,而且差距不小。

## 趋势 3:沉默层——停滞第一次有了定义

8 月也是一批平台地板塌陷的月份。报告窗口内上游零提交:

| 平台 | 最后提交 | 沉默时长 | 备注 |
|------|---------|---------|------|
| reasonix | 2026-05-29 | 3 个月 | CLI 品类先驱;如今是被追踪 CLI agent 里最停滞的 |
| aider | 2026-05-22 | 3+ 个月 | 曾经是 git 感知结对编程的默认推荐 |
| ClawTeam | 2026-07-04 | ~2 个月 | 发完 v0.3.0 就安静了 |
| Qwen-Agent | 2026-03-04 | ~6 个月 | 本月跨过 6 个月线 |
| MetaGPT | 2026-01-21 | 7 个月 | 仍被 2 份报告引用为核心证据——保留观察,不归档 |
| MaxClaw / Claw-AI-Lab / Rocketride-main | 6-7 月 | 1.5-2 个月 | 准停滞观察 |

Qwen-Agent 跨线影响最大:它是中生态代表,按治理规则,除了"战略意义"这条有争议的标准,其余归档条件全部满足——9 月评审必须做出这个裁量。而"停滞定义从 6 个月收紧到 4 个月"的修订案(8 月 19 日提出)如果今天就生效,reasonix 和 aider 已经落网;这份提案现在有三个真实案例,不再是假想题。

其中一个案例还是我们自己的:本报纠正了 Rocketride 的记录。之前判"停滞"是因为追踪 `main` 而开发早已搬到 `develop`——108 个提交的活跃开发,差点被我们归档。

## 趋势 4:盯着 agent 的 agent

在快速层平台里,同一个架构赌注独立出现了三次:

- **codex Guardian V2** — 带独立 transcript 收集与决策指标的监督 agent,门控主 agent 的动作。
- **OpenWorker 分层安全语料** — 301 行 gate/reviewer/sequence 评测数据接入 harness,外加 shell-escape 语料。他们不是在写安全模块,是在写安全模块的测试集。
- **IronClaw 通知自动化** — 预运行失败发布(#7899)加持久化授权门(#7901):监督面被当成一等子系统对待。

7 月的压缩竞赛解决的是"agent 塞不塞得进上下文窗口"。8 月的静默共识是:下一个瓶颈是**信任**——而正在成形的答案,是让第二个模型盯着第一个,并留下自己的证据链。我们的失败模式分类学预言过这一层的到来;一个月内在三处落地,说明这是波浪,不是巧合。

## 趋势 5:Claw 生态的机舱仍在运转

头条数字之下,核心 claw 平台继续以健康的人类节奏出货:

- **OpenClaw** — 本月 10,425 提交(351 位作者;Peter Steinberger 一人 6,197——整个生态最高产的个人)。特性主线:浏览器受控文档转换、context-engine 宿主参数投影、control-UI 的云 worker 可见性。
- **Hermes-Agent** — 6,208 提交(Teknium 1,670)。一天之内连落多个 provider 插件:Nebius Token Factory、Ramp Router、Router User-Agent 身份标识,外加 todo 嵌套子任务和 relay 的可加删除算子。
- **NanoClaw** — 254 提交,全是分布式系统纪律:会话 claim 对 spawn/adopt/finish 加栅栏、投递尝试计数落盘并成为重启后的权威、协调状态在内存 map 旁影子写。runner 正在变得形式化正确。
- **Nanobot** — 471 提交:OAuth 模型目录在线发现、Grok 4.6 订阅模型、TUI 剪贴板图片粘贴、按需文档检索(#5525)。
- **ZeroClaw** — 388 提交:ScopedToolRegistry 封装(#9319)、SOP 任务的认证操作员取消(#9476)、agent 派发前的认证 webhook 入口(#9744)、ZeroRouter 预置与公共目录(#9645)。
- **OpenHuman** — 4,884 提交,但其中 4,547 来自一位作者——围绕移除屏幕感知、重构捕获面的个人攻坚。
- **HiClaw** — 活跃分支上 38 提交,仍在消化 v1.2.0 的 K8s operator 重写。
- **GoClaw** — 4 提交;追踪以来最安静的一个月。列入观察。

## 平台活跃度总表

| 平台 | 提交数(8 月) | 活跃度 |
|------|--------------|--------|
| OpenClaw | 10,425(351 位作者) | 🔴 极高 |
| Eliza | 7,482(119 位作者) | 🔴 极高 |
| Hermes-Agent | 6,208(859 位作者) | 🔴 极高 |
| OpenHuman | 4,884(14 位作者) | 🟠 高* |
| PraisonAI | 1,376(65% 为 triage bot) | 🟠 高 |
| IronClaw | 300+(经 API 验证) | 🟠 高 |
| codex | 1,202 | 🟠 高 |
| Dify | 792 | 🟠 高 |
| Nanobot | 471 | 🟡 中 |
| ZeroClaw | 388 | 🟡 中 |
| kimi-code | 300 | 🟡 中 |
| NanoClaw | 254 | 🟡 中 |
| OpenWorker | 203 | 🟡 中 |
| Agent Zero | 142 | 🟡 中 |
| Rocketride(develop) | 108 | 🟡 中 |
| AgentScope | 79 | 🟡 中 |
| browser-use | 45 | 🟡 中 |
| HiClaw | 38 | 🟢 低 |
| copilot-cli | 9(仅 changelog) | 🟢 低 |
| GoClaw | 4 | 🟢 低 |
| kimi-cli | 2 | 🟢 低 |
| MaxClaw / Claw-AI-Lab / ClawTeam / aider / reasonix / MetaGPT / Qwen-Agent | 0 | ⚫ 沉默 |

*OpenHuman 的数字是一位作者的重构运动——按人类节奏视为中等。

## AllClaws 项目更新

**平台**:追踪 35 个(Tier-1 上限于 8 月 18 日随 browser-use——首个计算机操作代表——录满)。这是新三层治理模型下的第一份月报。

**8 月交付的研究**(4 份报告):
- Protocol Wars 2026(Q4-5)—— MCP/ACP/A2A 的结论是分层,不是战争
- 平台治理模型(Q4-6)—— 三层追踪、准入标准、观察名单
- 品类覆盖缺口闭合(Q4-7)—— 评估 6 个候选,browser-use 入列
- Harness 工程比较 —— 被追踪平台中的"演化式 harness"模式

**博客**:6 篇(16 平台 CLI 命令对比、虚拟团队实验、harness 工程比较——各配中英文)。

**基础设施**:长时基准测试(Q4-4,ROADMAP 最后一个开放项)交付 Phase 1 MVP——1,038 行场景规格、驱动器(aider/codex/kimi-cli)、runner、成本核算与评分。Phase 2(疲劳协议、8 平台矩阵)和 Phase 3(CI + 报告)随后。另外:README 重构为"只留要点"版,LATEST_UPDATES.md 成为时效性内容的主界面;CI 的 gitlink 事件(fixture 目录被当 submodule 提交)已根因定位并修复——最新一次 run 全部 13 个 job 全绿。

**CI 健康**:本月 agent-tests 20 次 run,15 绿 / 4 失败(全部发生在 gitlink 事件期间,已修复)/ 1 取消。benchmark 套件 10/10 全绿。

## 展望:2026 年 9 月

1. **停滞定义表决** — Qwen-Agent 已过线,reasonix/aider 是活案例,9 月评审将决定 6 个月还是 4 个月。归档队列可能首次开启。
2. **Guardian 级监督** — 如果"盯着 agent"的模式继续以这个速率落地,跨平台监督架构将成为研究项(并可能成为 platform_comparison 的新维度)。
3. **Q4-4 Phase 2** — 疲劳协议加 8 平台 × 5 场景矩阵。落地则 ROADMAP 达成 13/13,H2 2026 全部交付收官。
4. **观察:GoClaw 与 kimi-cli** — 两个历来可靠的出货者交出了近零月份。一个月安静是噪音,两个月是信号。

---

*AllClaws 以三层治理模型追踪 4 大类 35 个 AI agent 平台。数据采集于 2026 年 8 月 30 日,经本地 submodule 日志与 GitHub API 交叉验证,并做了机器人提交分离。完整研究报告见 [github.com/dz3ai/allclaws](https://github.com/dz3ai/allclaws)。*
