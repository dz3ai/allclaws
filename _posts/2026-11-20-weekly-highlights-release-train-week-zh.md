---
layout: post
title: "周报亮点：发车的一周（2026 年 11 月 13–20 日）"
lang: zh
date: 2026-11-20 21:00:00 +0800
author: Danny Zeng
categories: [周报]
tags: [weekly-highlights, releases, openclaw, nanoclaw, zeroclaw, nanobot, goclaw, security, rustsec, gpt-6.2, codex]
---

十月的月报给这个生态下的判词是 **cadence（节奏）**。本周窗口——**11 月 13–20 日**，覆盖 tracker 盯着的八个项目——给这句话补了一个更锋利的从句：节奏已经**多轨化**。最重的那个项目不再只跑一条发布线，而是同时跑三条：给十月线打 backport，给十一月稳定版打 patch，同时开下一趟车的 beta。其余项目也各自归位：按点发车的、发完车加固的、以及闷头写码不打 tag 的。

## OpenClaw：七个 tag、三条线、一个星期

`main` 七天吃进 **2,353 个 commit**——commit 类型分布说明了力气花在哪：**1,616 个 `fix`**、143 `improve`、139 `test`、117 `perf`、115 `feat`。这是一个全面进入持续维护态的代码库，窗口内产出了**七个 tagged release**：`v2026.11.5-beta.3`/`beta.4`、`v2026.11.4`、`v2026.11.5`、十月线的 backport `v2026.10.33`、`v2026.11.6`、以及开出下一趟车的 `v2026.11.10-beta.1`——最后两个落在同一天。

头条是 `v2026.11.6`（11 月 19 日）：一个 *patch* release 装着 **386 个 PR、48 个直接 commit、157 位贡献者**。它的 changelog 读起来像一份围绕 agent 循环周边所有东西的事后复盘：

- **Turn 存活率**——subagent 与后台 turn 在配置变更中存活；Gateway 重启打断发送时最终答案仍能送达；subagent 结果跨重启存活且*不重放已消费的结果*；长链条、重工具的 Claude CLI turn 保住了 append-only 的 provider 历史和逐字节精确的 Responses 工具参数。「投递失败」和「已被成功消费」被区分开——这种正确性只在重启之下才显形。
- **Gateway 减重**——受限主机上启动内存压力与常驻内存下降，未用到的本地凭据 runtime 延迟加载，插件工具发现不再阻塞 Gateway。
- **发车机械**——2026.11.5 的 updater 桥接到当前发布路径；Git-release 安装在 `node_modules` 之外构建与伺服；Windows 在 core readback 后才通知。11.5 的 release notes 本身还在窗口内被恢复又修补了一遍——发布工程在修发布工程。
- **对齐 ChatGPT**——数字版 OpenClaw release 作为 ChatGPT version header 发送，模型目录带 release 版本列出，新增测试捕捉 GPT-6.2 prompt cache 读丢失。
- **信任面**——配置读取中内联环境凭据被脱敏；SecretRef 支撑的 skill API key 保留引用而不被压平成明文；PostgreSQL 升级在备份跑不动时会停在「仍在服务的实例」之前。

三条并行发布线才是真正的故事：十月线拿 backport、十一月稳定版拿两个 patch、下一趟车拿首个 beta——*同一天*。这个规模的 cadence 已经不是速度问题，是车道纪律问题。

## NanoClaw：六天从 beta.3 到 rc.3

`v2026.11.0` 列车从 `beta.3`（11-14）一路过 `beta.4`、`rc.1`、`rc.2`，到 `rc.3`（11-19）——final 在望。背后 86 个 commit 大半在 add-codex/OneCLI 这一层，其中一条的生态相关度最高：**把 Codex 钉在 0.169.0，「让 ChatGPT 登录用上 GPT-6.2」**（`ab9551f0`）。

这个 pin 是我们在 benchmark 工作里独立撞上的那个事实的另一半：上游 Codex 在 2026 年 2 月硬切断了 chat wire API，于是所有说 ChatGPT OAuth 的客户端都得守住最后一个还收它的版本。NanoClaw 的处置相当完整——登录走钉住的 CLI、经 `pnpm dlx` 在 `/tmp` 之外执行；Codex AGENTS.md 上限提到 64 KiB；内置图像生成在 OneCLI 后面可用。外围还有：setup 步骤只有原始日志落盘才算结束；linger 校验不再触发交互式 polkit；agent-runner 对 Claude 的 `settings.json` 既不阻塞也不跟随链接；周期性 mailbox 系列每次运行只留一个 task payload。

## ZeroClaw：安全周

二十一个 commit、零 tag——`v0.9.0` 之后的这一周是一场 Rust 味很浓的加固：**六个 RustSec advisory 修补**（heapless、Wasmtime、SMTP 用有界 base64 副本堵住、zip 对应 RUSTSEC-2026-0548、quinn-udp 对应 RUSTSEC-2026-0538，chrono 的维护性 advisory 被评估接受）。

更有意思的一半是 confinement：MCP SSE 端点及其重定向被限制在 server origin 内；每连接的 task 记录移出 INFO trace；转发的 loopback 在 SOP 取消判定里按非本地处理；配对的 WebSocket 凭据移出 URL；Scalar 文档 bundle 用 Subresource Integrity 钉住。访问控制同步收紧——上传与编辑前必须先有读权限；SOP 决策答案不可用时走 fail-closed。同一批里悄悄落了两个 feature：bash 执行 POSIX 命令时按 bash 自己的语法读命令；Anthropic 请求开始携带 `output_config.effort`。

## NanoBot：一百个 commit，没有 tag

`v0.4.1`（11-06）之后继续滚，NanoBot 这一周泡在 webui 里：composer 的 slash/skill/mention 三个 palette；goal island 重做成「浮动的 vibrancy platter」；重连语义重做——运行中的 turn 在重连时对账，排队消息在 agent 接手时可见。我们想单独点名的一条更安静：**畸形主机名在 DNS 解析之前就被拒绝**——校验搬到了最早的位子，也就是它该在的位子。会话的用户图片改从存储附件回放；gateway mutation 与 UI state 分离——和 OpenClaw 那边 transcript 重构在做的是同一种数据/控制分离。

## GoClaw 与安静的三家

GoClaw 从 `beta.247` 点到 `beta.250`，五个会计级修补：Ollama 工具 schema 保住 enum/items/嵌套结构和 `[]any` required 字段；Gemini 思考 token 计入原生媒体用量；Claude CLI 缓存 token 计入上下文用量；cron 在 SQLite 里拒绝重叠的手动运行、在 PG 和 SQLite 两个存储里都尊重 `due` 模式。小、不花哨，恰是一列成熟 beta 列车该有的样子。

IronClaw（HEAD 停在 9 月 29 日）、ClawTeam（11 月 7 日）、MaxClaw（6 月 13 日）继续休眠。

## 底下的那条线：GPT-6.2 对齐

把最忙的两个项目放在一起读，一个上游事件就同时解释了它们：OpenClaw 在刷 ChatGPT 模型列表、version header、GPT-6.2 缓存测试，NanoClaw 在为 ChatGPT 登录钉 Codex 0.169.0。当生态里最大的项目和一个跑得飞快的小项目从相反方向汇到同一个外部发布波上，那不是巧合——那是依赖引力。接下来几个周报窗口，大概率会看到其余项目以各自的方言吸收同一波。

---

*[English version](/allclaws/blog/2026/11/20/weekly-highlights-release-train-week/)*

*数据：[周报 digest 2026-11-20](https://github.com/dz3ai/allclaws/blob/main/docs/reports/weekly/2026-11-20-submodule-weekly.md)及 [docs/reports](https://github.com/dz3ai/allclaws/tree/main/docs/reports) 下各项目月报。窗口 2026-11-13 至 11-20，共 8 个追踪项目。*
