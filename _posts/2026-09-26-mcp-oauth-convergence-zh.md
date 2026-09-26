---
layout: post
title: "三条线，一个标准：MCP 授权生命周期已经汇流了"
lang: zh
date: 2026-09-26 10:12:00 +0800
author: Danny Zeng
categories: [生态分析]
tags: [mcp, oauth, sep-2207, kimi-code, hermes-agent, codex, 标准化, agent 架构, architecture]
---

kimi-code 仓库里有一条不起眼的 changeset，一句话：「修复 MCP OAuth 不请求 offline_access scope 的问题——此前导致像 Vercel 这样的 provider 每小时都要重新弹浏览器授权」。

每小时弹一次登录。想象这个体验：你给 agent 配了一个 MCP server，授权成功，一切正常——然后每个小时，浏览器准时弹出来找你要一次授权。没有人做错了什么：client 没请求 refresh token，authorization server 按 OIDC 惯例不给，access token 过期，一切从头再来。这不是 bug，是三个互相对话失败的组件的合力。

这条 changeset 对应的 commit 是 kimi-code 的 [#3979](https://github.com/MoonshotAI/kimi-code/pull/3979)（09-22 落地），我们在 MCP 产品化观察第 1 篇里把它当作一条「第三线索」提过一嘴。这一篇我们把它拆开——因为拆开之后你会发现，它不是一条孤立的线索，而是**三条线索在此汇合的那个点**。MCP 产品化观察系列讲了三篇：依赖契约（Hermes）、身份与审计（Codex）、授权生命周期（kimi-code）。这三条线看起来各修各的，但把 #3979 这条 commit 放到聚光灯下，你会看到「汇流」已经发生了——不是预测，是时间线上的事实。

*本文是「MCP 产品化观察」系列第 3 篇，也是收官篇。*[English version](/allclaws/blog/2026/09/26/mcp-oauth-convergence/)

---

## 复盘：三条线各自走到了哪

先把三条线的进度条对齐一下。

**第一条线，依赖契约。** Hermes 的 Connectors 三部曲把 MCP server 从「进程配置」提升为「应用依赖对象」：manifest 声明依赖、安装时拒绝不兼容主机、endpoint 持续探测。解决的是「工具在不在」。

**第二条线，身份与审计。** Codex 的 app-server v2 给 MCP 请求加了显式的 app/account target、跨 compaction 存活的 attribution 底账、跨 transport 队列的 trace context。解决的是「这笔账算谁的、出事了查不查得到」。

**第三条线，授权生命周期。** kimi-code 的 offline_access、401 自动降级 needs-auth——解决的是「token 过期之后，这条工具链还活着吗」。

三条线里，前两条都还带着强烈的平台私有色彩：Hermes 的 manifest 是自己的格式，Codex 的 target/attribution 长在自己的协议扩展里。唯独第三条线，走到一半的时候撞进了一个已经存在的公共标准。这一篇的主线，就是讲这次「撞上」——以及它揭示的整个生态的标准化路径。

---

## 标准早就等着：SEP-2207

kimi-code 那条 commit 修的问题，在 MCP 官方仓库里有一个正式的名字：**SEP-2207，《OIDC-Flavored Refresh Token Guidance》**，2026 年 2 月 4 日立项，状态已经是 Final。它解决的问题和我们开头那个「每小时弹登录」一模一样，而且拆得更透。

背景是这样的：MCP 的授权机制建在 OAuth 2.1 上，但现实世界的 authorization server 大多同时实现 OIDC。两者对 refresh token 的态度有个微妙差异：纯 OAuth 2.1 里**没有标准机制让客户端主动要 refresh token**——发不发，server 看心情（和策略）；而 OIDC 的惯例是，客户端带上 `offline_access` scope，就表示「我要一个长期凭证」。差异本身无害，但它制造了三个生态级问题，SEP 原文数得很清楚：

**一，大客户端都没在要。** Cursor、Claude、VS Code 这些主流 MCP client 都没有显式请求 refresh token——因为它们不知道对面的 authorization server 支持不支持、期待不期待这个 scope。每个 client 都在猜，猜错的代价就是用户每小时登录一次。

**二，资源端不该替客户端表态。** `offline_access` 不是某个资源需要的权限，它是 client 和 authorization server 之间的事。所以 MCP server 把它写进 401 响应的 `WWW-Authenticate` 或资源元数据的 `scopes_supported` 里，语义上是错的——资源永远不需要「长期访问」，那是客户端自己的愿望。

**三，各家 server 行为不一致。** 同样的授权码请求，不同的 server 发不发 refresh token、什么条件发，各不相同。

SEP-2207 给出的解法简单到近乎朴素，但每个 MUST/SHOULD 都卡在精确的位置：

**客户端**：想用 refresh token 且能安全存它的，应该在 client metadata 的 `grant_types` 里声明 `refresh_token`（SHOULD）；发现 authorization server 的 `scopes_supported` 里有 `offline_access`，就可以把它追加到请求 scope 里（MAY）；但**绝不能假定请求了就一定发**——发不发，server 保留裁量权（MUST NOT assume）。

**服务端（作为资源服务器的 MCP server）**：不应该把 `offline_access` 放进 `WWW-Authenticate` 或资源元数据（SHOULD NOT）——理由就是我们上面说的，那不是资源的诉求。

而且它写进了正式规范：2026-07-28 版 MCP 规范的 Authorization 章节已经有完整的 Refresh Tokens 一节，表述与 SEP 一字不差。配套的参考实现落在了官方 SDK 里——TypeScript SDK 的实现 PR 在 3 月 30 日合并，Python SDK 在 4 月 14 日跟上，还附带一个客户端一致性测试，专门用来验证 SDK 实现得对不对。

---

## 落地：kimi-code 怎么实现 SEP

现在把镜头拉回 9 月 22 日那条 commit。读它的 diff，你会看到一个教科书级的「按标准实现」。

核心是一个 `resolveRequestScope` 方法，逻辑分三步：第一步，**发现**——通过 MCP SDK 的 `discoverOAuthServerInfo` 拿到 authorization server 的元数据，缓存下来；第二步，**对表**——检查元数据的 `scopes_supported` 里有没有 `offline_access`，没有就不加（server 没 advertise，client 不硬塞，这正是 SEP 的 MAY 分支的前置条件）；第三步，**幂等追加**——把 `offline_access` 接到基础 scope 后面，但先检查基础 scope 里是不是已经有了，有了就不重复加。

三步里每一步都对应 SEP 的一句要求，不多做，不少做。特别值得看的是那个「不加」的分支：如果 server 没有声明支持 `offline_access`，kimi-code 的选择是**保持原样**，而不是「试试呗」。这个克制就是标准的价值——它把「每个 client 自己猜」变成了「大家都查同一张表」。

kimi-code 的授权生命周期工程也不止这一处。9 月 17 日的 #3846 处理的是运行时那一半：一个 MCP 工具调用返回 401 时，server 要自动切到 needs-auth 状态、作废被拒绝的 token、在并发授权窗口里区分「新鲜的授权」和「刚被拒绝的」——连「授权时间早于调度器时钟的未来时间戳」这种边界都单独修了一条。如果说 offline_access 是「怎么把 token 的命续上」，那这一组就是「token 死掉的瞬间，系统怎么优雅地知道并恢复」。一加一减，凑成完整的生命周期。

还有一个容易被忽略的细节：kimi-code 的 MCP OAuth 直接构建在官方的 `@modelcontextprotocol/sdk` 上——也就是那个 3 月就内置了 SEP-2207 参考实现的 SDK。平台不是自己在真空里发明授权逻辑，而是**踩着标准的参考实现往上盖自己的运行时**（它自己的 proactive refresh、调度器、并发授权窗口都是 SDK 之上的私有层）。标准的分层就这样显形：协议规范管接口，官方 SDK 管公共实现，平台管自己的增量。

---

## 汇流：一条完整的标准化流水线

把时间线排成一列，会看到一条罕见的、完整运转的标准化流水线：

**2026-02-04** — 生态痛点立项为 SEP（「主流 client 都在每小时弹登录」）
**2026-03-30 / 04-14** — 官方 SDK 出参考实现和一致性测试
**2026-07-28** — 正文进规范，成为正式要求
**2026-09-22** — 平台落地（kimi-code），修的是自己用户的真实痛点

从痛点到标准用了不到两个月，从标准到头部平台落地用了不到三个月，全程有规范文本、SDK 代码、一致性测试三样东西兜底。这不是「某大厂发明然后强推」的模式，也不是「各平台永远各玩各的」的模式——是开源基础设施最理想的那种节奏：**问题先标准化，实现再跟进，平台最后受益。**

对比之下，前两条线的状态就很说明问题。Hermes 的依赖契约和 Codex 的身份审计，目前都还是平台私有设计——没有 SEP，没有跨平台字段，没有一致性测试。授权生命周期这条线跑在了前面，不是因为它更重要，而是因为它的问题**最古老**：OAuth 的坑社区踩了二十年，`offline_access` 的语义在 OIDC 里早就写好了，MCP 要做的只是接过来、划清「资源」和「客户端」的边界。成熟土壤上的问题，标准化得快；新大陆上的问题，还得各家长几茬庄稼。

但方向已经能看出来了。三条线在各自平台的私有实现里长出了同样的骨架——声明（Hermes 的 manifest 字段 / Codex 的 protocol capability / kimi 的 scope 协商）、探测（kimi 的元数据发现 / Hermes 的 endpoint probe）、生命周期（token 续期 / 应用存活 / 授权撤销）。同样的骨架重复出现，就是下一个 SEP 的原材料。Hermes 什么时候把「依赖声明」提成 manifest 通用字段，Codex 什么时候把 app/account target 提给规范委员会，是接下来两个最值得盯的动作。

顺带一个闭环的小注脚：Codex 的 trace context commit 里，集成测试明确标注覆盖 `2026-07-28` 协议模式——和收到 refresh token 那节的是同一个规范版本。平台们已经开始用「我兼容哪一版规范」来标注自己的行为了，这本身就是汇流的证据。

---

## 标准来了，你该做什么

**如果你的产品里有 MCP client**：去查你的 OAuth 实现——是否声明了 `refresh_token` grant type？是否在 authorization server 的 `scopes_supported` 里有 `offline_access` 时追加请求？是否犯了「假定请求就一定发」的错误？照着 2026-07-28 规范的 Refresh Tokens 一节过一遍，你的用户就不用每小时登录一次了。

**如果你的产品里有 MCP server**：检查两件事——`WWW-Authenticate` 和 Protected Resource Metadata 里**不要**出现 `offline_access`（那不是你的 scope）；401/403 的错误响应是否按规范带了 `WWW-Authenticate` 和 scope 提示。资源端的本分是把「我需要什么」说清楚，而不是替客户端去要长期凭证。

**如果你在做平台**：看你解决的问题有没有对应的 SEP。有，先实现标准再叠私有层（kimi-code 路线：官方 SDK 打底，私有增量盖在上面）；没有，而你的痛点又足够普遍，那就是你在给这个生态写下一个 SEP——把私有设计里的通用骨架抽出来提上去（Codex 的 capability 声明和 Hermes 的依赖 manifest 都是现成候选）。

MCP 产品化观察写到第三篇，系列的判断可以收拢成一句话：**MCP 正在从协议变成集成体系，而集成体系的每一根柱子——契约、身份、审计、授权——都在走同一条路：私有实现撞上共性痛点，痛点长出 SEP，SEP 落进 SDK，SDK 长回平台。**授权生命周期这条线已经走完了全程，后面几根柱子正在路上。到四根柱子都有自己的 SEP 那天，MCP 集成就真正标准化了——到那时再看今天这些「每小时弹一次登录」的故事，大概就像今天看没有 package.json 的前端项目一样遥远。

---

*[English version](/allclaws/blog/2026/09/26/mcp-oauth-convergence/)*

*基于本周 submodule 周报与微信草稿改写。数据来源：[SEP-2207](https://modelcontextprotocol.io/seps/2207-oidc-refresh-token-guidance)、[MCP 规范 2026-07-28 Authorization](https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization)、[周报 2026-09-22](https://github.com/dz3ai/allclaws/blob/main/docs/reports/weekly/2026-09-22-submodule-weekly.md)。*
