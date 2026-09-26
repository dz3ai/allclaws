---
layout: post
title: "一个 Agent 背后站着十个账号：Codex 把 MCP 当多租户协议来治"
lang: zh
date: 2026-09-26 09:35:00 +0800
author: Danny Zeng
categories: [生态分析]
tags: [mcp, codex, hermes-agent, kimi-code, multi-tenancy, audit, trace-context, oauth, architecture]
---

上一篇讲了 Hermes 的答案：MCP server 从「进程配置」被提升为「应用依赖对象」——装不装看依赖声明，活不活看应用状态，为什么挂有明确解释。那条路线解决的是单机用户的痛。

但 MCP 产品化的拼图还有另一半。设想另一种部署形态：agent 不是趴在你的桌面上，而是作为**服务**跑在别人的环境里——IDE 集成它，桌面应用集成它，云端插件也集成它。它背后连着一队 MCP server，每个 server 又连着不同的应用、不同的账号。这时问题变了。不再是「这个工具能不能用」，而是——

**这次资源读取，读的是谁账号下的东西？这次工具调用，事后算在谁头上？出了事故，能把 agent 的一步行为串到下游那次 HTTP 请求吗？**

三个问题，一句话：MCP 请求开始需要身份。而这周 **Codex**（OpenAI）落地的一组改动，正好是这三个问题的三份答卷——近 7 天 409 commits，app-server v2 持续演进，rust-v0.155.1 于 09-18 发布。

*本文是「MCP 产品化观察」系列第 2 篇。第 1 篇讲了 Hermes 那条「应用依赖」路线；下一篇看第三条线：授权生命周期，以及三条线怎么汇流。*

---

## 第一问：这次读的是谁的资源？

Codex 在 `mcpServer/resource/read` 协议里加了一个显式的 `target` 字段（[#47248](https://github.com/openai/codex/pull/47248)）：`{connectorId, linkId}`。拆开看，每个字段都在回答一个身份问题。

`connectorId` 说的是「哪个应用」；`linkId` 说的是「哪个账号」——传一个字符串，就是选定某个已授权账号去读；传 `null`，语义是「不走授权的匿名访问」，能不能真这么做，由后端策略说了算。也就是说，**一个资源读取请求，从协议层面就必须说清楚「以哪个应用、哪个账号的身份」**。

几个细节能看出设计上的克制：直接 target 只对 `codex_apps` 这一类 hosted 应用开放，空的 connectorId、空的 linkId、合成出来的 linkId 一律拒绝；带上 `originCallId` 和 `threadId` 时，请求会保留发起方的 app/account 作用域——谁发起的，身份就跟着谁走；而不传 `target` 时，一切照旧，走原来的 discovery 流程。协议长了新维度，但老用法一条都没断。

这行 `linkId` 值得单独说一句。在它存在之前，MCP 的资源读取默认就是「这个连接配好的那个身份」——单租户思维。当同一个 connector 下可以挂多个账号、还能显式声明「这次不要授权」时，MCP 请求才第一次有了**账号粒度**。这就是多租户的地基。

---

## 第二问：这件事到底是谁干的？

第二个问题更隐蔽，也更要命：**审计**。agent 一场会话里调了十几次 MCP 工具，事后你要回答「这笔调用是谁发起的、走的哪个连接器」，才发现会话早就被压缩过了——历史被裁剪、重写、分叉，账本都被重抄过几遍，原始记录去哪了？

Codex 的答案是给 MCP 调用建一本「压缩冲不掉的底账」（[#47081](https://github.com/openai/codex/pull/47081)）。每次 MCP 调用——包括直连的、走 Code Mode 的、返回了错误的、结果没打印出来的——都记录来源和首次出现的轮次，带上 connector 和 plugin 标识。关键在后半句：这些 attribution 会**持久化为检查点，并在 compaction、resume、fork 之后照常恢复**，哪怕 fork 只带最近几轮。会话怎么折腾，账不会丢。

然后是这页账本的用途：它会作为 `mcp_attribution` 附加到 Responses API 的 `client_metadata` 里——注意，是放在**模型可见内容之外**的元数据通道。这个位置选择很有讲究：审计信息是给云端和运维看的，不该塞进上下文里污染模型，更不该让模型「看到自己被记账」。同时传输只发往许可名单内的 OpenAI HTTPS 目的地，旧历史没有检查点、attribution 畸形冲突、序列化超过 16 KiB，都会明确报 `attribution_error` 而不是默默吞掉。

一套完整的审计设计要同时回答「记什么、跟着什么活、发给谁、坏了怎么办」——这四个格子，Codex 全填了。

---

## 第三问：出事了，查得到吗？

第三个问题是可追溯性，而它输在一个很不起眼的地方：队列。

app-server 的 MCP 请求要穿过后台的 transport 队列。HTTP 请求从调用方出发，排了个队，再发出去——W3C 的 trace 上下文不会自己跟着排队走，于是发出去的请求和最初发起的调用之间，trace 血缘断了。日志里两截孤零零的 span，谁也认不出谁是谁的孩子。监控做得再全，链条在队列里断了一节，排障就变成考古。

[#47212](https://github.com/openai/codex/pull/47212) 干的就是接链的事：在请求元数据里显式捕获 W3C trace context（工具调用、资源操作、自定义请求、事件流全覆盖），在真正发 HTTP POST 的地方用一个 `mcp.http.request` span 把它恢复出来，让出站的 HTTP trace 显式挂回原始请求；应用元数据保留，trace 字段换成当前调用方的，过期的 `tracestate` 清掉。新旧两种协议模式（legacy 和 `2026-07-28`）都有集成测试压着。

把三问连起来看，你会发现在 Codex 眼里，MCP 集成的第一性问题根本不是「工具多不多、server 死没死」，而是：**当一个 agent 服务多个应用、多个账号、多个并发会话时，每个请求的归属和来路必须自始至终说得清。**这是把 MCP 当基础设施来治理的视角——基础设施的第一美德不是功能多，是每一笔都可归属、可追责。

---

## 配套件：让身份体系真的能用

光有协议字段还不行，这周还有三件配套落地，凑成一套可用的身份体系。

**子 agent 也能要用户输入了**（[#46877](https://github.com/openai/codex/pull/46877)）。之前 MCP 请求需要用户交互时，子 agent 会直接失败，提示「去问父 agent」——浏览器登录、表单填写、交互式工具审批，在子线程里全是死路。现在 root-only 的守卫拆掉了，子 agent 可以在既有的审批策略和自动审查规则下发起提示、等待响应。为什么这事排在多租户叙事里？因为**多 agent 是多租户的前奏**：身份体系先得能区分「哪个 agent」，才谈得上「哪个账号」。

**网关 OAuth 登录的显式控制**（[#47207](https://github.com/openai/codex/pull/47207)）。带登录 UI 的客户端现在可以声明 `explicitGatewayOauth` 能力，自己决定浏览器授权什么时候开始、发起认证请求前先确认凭证就绪；授权 URL 只发给发起连接，连接断开自动取消登录，后面的连接也撤销不了已声明的 opt-in。一句话：**授权的发起权从框架手里交还给客户端**——这正是多租户系统的日常：什么时候弹登录框，是租户的事，不是平台的事。

**MCP server 状态里露出了 HTTP origin**（[#47159](https://github.com/openai/codex/pull/47159)）。`McpServerStatus` 新增可空的 `httpOrigin`，只返回 HTTP(S) origin 本身，凭证、路径、查询串、fragment 一概不带；stdio transport 返回 null。让「这个工具背后连的是哪个域」变成安全审计可以直接读的字段，而不是要人去配置文件里翻端点 URL。

---

## 两条路线，一张完整的图

把上一篇和这一篇合上，两条路线可以对齐着看。

**Hermes：应用依赖路线。** 核心比喻：MCP server 是应用的依赖项，像 package.json 管依赖。关键机制：manifest 声明依赖 + 安装时拒绝 + endpoint 持续探测 + 工具目录伸缩。解决什么：单机用户的「server 装不上、悄悄死、说不出原因」。

**Codex：多租户协议路线。** 核心比喻：MCP 是多租户协议，每个请求要有身份、有底账、有来路。关键机制：resource reads 带 app/account targets + 累计 attribution 持久化 + W3C trace context 跨队列保留。解决什么：一个 agent 服务多个应用、多个账号时的请求归属、审计与可追溯。

两条路线不互斥，甚至不在同一层。Hermes 管的是**本地可靠性**——工具什么时候可用；Codex 管的是**服务端正确性**——每个请求算谁的账。一个是「手」的工程，一个是「账」的工程。完整的 MCP 集成体系，早晚两样都要。

为什么两家各选了一头？看形态就懂。Hermes 的主战场是个人桌面 agent，用户痛的是「我这台机器上 server 怎么又挂了」。Codex 的 app-server 是被 IDE、桌面应用、云端插件集成的**服务**，天然多租户——当你的 agent runtime 是基础设施，「每个请求属于谁」就不是高级需求，是第一行代码就该想清楚的事。

---

## 为什么是现在

这组改动不是孤立的。同周的周报里，两个信号在给它铺路。

一个是 agent 形态本身的演化：Codex 这周把 AgentControl 抽象落地——`LocalAgentControl` 集中 agent resume 处理、多 agent spawning 统一走 SpawnRequest、agent snapshots 从 close_agent 返回并流式订阅。多 agent 生命周期收敛为单一控制面，意味着**并发跑着的 agent 越来越多**，每个都在发 MCP 请求——没有归属和审计，多 agent 就是多份糊涂账。Guardian 体系同周默认启用（#47275），自审要有意义，前提恰恰是「谁干的」查得出来。

另一个是授权生命周期的行业呼应：kimi-code 同周给 MCP OAuth 请求加了 `offline_access`（#3979）——令牌过期了 server 还能不能干活，也是授权问题的一部分。加上上一篇的两条路线，图景更清晰了：**MCP 集成正在从「进程启动时挂载」演进为有依赖契约、有身份、有审计、有 OAuth 生命周期的完整集成体系。**四根柱子，这周你能看着一家在砌「契约」，另一家在砌「身份 + 审计 + 授权」。

---

## 给你的 MCP 集成问三个问题

不用等协议标准化，今天就可以拿这三个问题审自己的集成。

**每次工具调用，能归到一个明确的身份吗？** 你的集成里，「这次调用用的是哪个连接器、哪个账号」是显式字段，还是散落在初始化配置里的隐式默认？如果多个账号共享一个连接，账号粒度的 target 现在就该进你的路线图——协议已经给出了语法，`{connectorId, linkId}` 就是样板。

**会话被压缩、恢复、分叉之后，调用记录还在吗？** 长会话必然被 compaction，历史重写时你的 MCP 调用账本跟着重写还是独立持久化？Codex 的做法值得抄：attribution 做成检查点，跨 compaction/resume/fork 恢复——审计数据的第一属性是**能从重抄的账本里活下来**。

**出了事，能把 agent 的一步行为串到下游那次 HTTP 请求吗？** 中间有队列、有异步、有 transport worker 的架构，trace context 不会自己跨过去。检查你的链路：出站请求的 trace 有没有显式挂回调用方？断了一节，可观测性就是装修。

三个问题如果都是「说不清」，你的 MCP 集成还停在「进程配置」时代——能跑，但经不起审计。而这正是这周两家头部平台用两部重构同时指向的未来：MCP 不会停在「协议」，它正在长成一套有契约、有身份、有底账的集成体系。到那时，「这个调用是谁发的」说不清的 agent，就像今天不写 package.json 的前端项目一样——不是不能活，是没人敢接手。

---

*[English version](/allclaws/blog/2026/09/26/codex-mcp-multitenant/)*

*基于本周 submodule 周报与微信草稿改写。数据来源：[周报 2026-09-22](https://github.com/dz3ai/allclaws/blob/main/docs/reports/weekly/2026-09-22-submodule-weekly.md)。*
