---
layout: post
title: "周报：密集发版的一周（2026 年 11 月 13–20 日）"
lang: zh
date: 2026-11-20 21:00:00 +0800
author: Danny Zeng
categories: [周报]
tags: [weekly-highlights, releases, openclaw, nanoclaw, zeroclaw, nanobot, goclaw, security, rustsec, gpt-6.2, codex]
---

十月的月报说，这个生态的关键词是「节奏」（cadence）。本周（11 月 13–20 日，我们跟踪的 8 个项目）把这个判断又推进了一步：节奏不只是快，而是同时跑好几条线。OpenClaw 一边给十月版本打补丁、一边修十一月稳定版、一边开了下一版的 beta。其他项目也各有分工：有按计划发版的，有发完版专心修安全的，也有闷头开发不发版的。

## OpenClaw：一周七个版本，三条线并行

`main` 分支这七天合入了 2,353 个 commit。从类型分布能看出力气花在哪：1,616 个是 `fix`，143 个 `improve`，139 个 `test`，117 个 `perf`，115 个 `feat`。代码库已经进入持续维护状态。这一周发了七个带 tag 的版本：`v2026.11.5-beta.3`、`beta.4`、`v2026.11.4`、`v2026.11.5`、十月线的补丁 `v2026.10.33`、`v2026.11.6`，以及下一版的第一个 beta `v2026.11.10-beta.1`。最后两个在同一天发布。

重点是 `v2026.11.6`（11 月 19 日）：一个补丁版装了 386 个 PR、48 个直接 commit、157 位贡献者。它的 changelog 主要在修 agent 循环周边的基础设施：

- **任务可靠性**：改配置不再打断 subagent 和后台任务；Gateway 重启时，最终回复仍能送达；subagent 的结果跨重启保留，已消费的结果不会重复执行；长任务里 Claude CLI 的对话历史和工具参数按原始字节保留，不做改写。「投递失败」和「已经成功消费」被区分开——这类问题平时看不出来，只有重启时才暴露。
- **Gateway 减负**：受限主机上，启动内存和常驻内存都降了；用不到的本地凭据延迟加载；插件的工具发现不再阻塞 Gateway。
- **发布流程本身**：2026.11.5 的升级器能桥接到当前发布路径；Git 方式安装的版本在 `node_modules` 之外构建和运行；Windows 改为核心读回后再通知。连 11.5 的 release notes 本身都在这周内修了两遍。
- **对接 ChatGPT**：把 OpenClaw 的数字版本号作为 ChatGPT 的 version header 发送；模型目录带版本号列出；新增测试，检查 GPT-6.2 的 prompt cache 是否丢失。
- **安全**：读配置时，内联的环境凭据会先脱敏；skill 的 API key 保留 SecretRef 引用，不会被压成明文；PostgreSQL 升级时，如果备份跑不了，会停在还在服务的实例之前，不强行替换。

三条线并行才是本周真正的故事：十月线拿补丁、十一月稳定版拿两个补丁、下一版拿首个 beta，全部落在同一天。版本密到这个程度，考验的不是速度，是同时维护几条线不出错的纪律。

## NanoClaw：六天从 beta.3 到 rc.3

`v2026.11.0` 的发布节奏：11 月 14 日 `beta.3`，接着 `beta.4`、`rc.1`、`rc.2`，11 月 19 日 `rc.3`。正式版很近了。

背后 86 个 commit 多数在改 add-codex 和 OneCLI。最值得注意的是：把 Codex 固定在 0.169.0，提交说明写的是「让 ChatGPT 登录用上 GPT-6.2」（`ab9551f0`）。

这个版本固定和我们在 benchmark 里遇到的是同一件事：上游 Codex 在 2026 年 2 月删掉了 chat 接口，想用 ChatGPT OAuth 的客户端只能守住最后一个还支持它的版本。NanoClaw 做得比较完整：登录走固定版本的 CLI，通过 `pnpm dlx` 在 `/tmp` 之外执行；Codex 的 AGENTS.md 大小上限提到 64 KiB；内置图像生成也能在 OneCLI 后面用。其他改动：setup 步骤要等原始日志写完才算结束；检查 linger 时不再弹交互式 polkit；agent-runner 读 Claude 的 `settings.json` 时既不阻塞、也不跟随软链接；周期性邮箱任务每次运行只保留一条任务记录。

## ZeroClaw：安全加固周

21 个 commit，没有发版。`v0.9.0` 之后的一周全用在加固上。

一半是 Rust 生态的例行安全公告，共六个 RustSec 修补：heapless、Wasmtime、SMTP（用一个有界的 base64 副本堵住）、zip 的 RUSTSEC-2026-0548、quinn-udp 的 RUSTSEC-2026-0538；chrono 的维护性公告评估后接受。

另一半是收紧访问范围：MCP 的 SSE 端点和重定向只能访问 server 自己的 origin；每连接的任务记录不再写进 INFO 日志；经过转发的 loopback 地址，在取消 SOP 时按非本地处理；WebSocket 的配对凭据从 URL 里移走；Scalar 文档用 Subresource Integrity 固定版本。权限也收紧了：上传和编辑之前必须先有读权限；SOP 决策的答案不可用时直接失败，不猜测。同一批里还落了两个功能：bash 执行 POSIX 命令时，按 bash 自己的语法解析命令；Anthropic 请求带上了 `output_config.effort` 参数。

## NanoBot：一百个 commit，没有发版

`v0.4.1`（11 月 6 日）之后继续开发。这一周主要在做 webui：composer 里的 slash、skill、mention 三个自动补全面板；goal 页重做成一个悬浮面板；重连逻辑重做——重连时，正在运行的任务会对账，排队的消息在 agent 接手时会显示出来。

有一条值得单独说：畸形的主机名在 DNS 解析之前就会被拒绝。把校验放在最早的一步，是最省事也最安全的位置。另外：会话里的用户图片改从已存附件回放；gateway 的数据操作和 UI 状态做了分离——和 OpenClaw 这周对 transcript 做的拆分是同一个思路。

## GoClaw 和安静的三家

GoClaw 从 `beta.247` 发到 `beta.250`，五个补丁都在修用量统计：Ollama 的工具 schema 不再丢失 enum、嵌套结构和 `[]any` 必填字段；Gemini 的思考 token 计入用量；Claude CLI 的缓存 token 计入上下文用量；cron 在 SQLite 里拒绝重叠的手动运行，PG 和 SQLite 两个存储都正确处理 `due` 模式。都是小修补，但正是 beta 阶段该有的样子。

IronClaw（代码停在 9 月 29 日）、ClawTeam（11 月 7 日）、MaxClaw（6 月 13 日）这周没有动静。

## 这周的暗线：GPT-6.2

把最忙的两个项目放在一起看，会发现它们在追同一个上游变化：OpenClaw 在改 ChatGPT 的模型列表和 version header，还加了 GPT-6.2 缓存的测试；NanoClaw 为 ChatGPT 登录固定了 Codex 0.169.0。最大的项目和一个跑得很快的小项目同时追同一个外部变化，说明是上游的发布节奏在拉动整个生态。接下来几周，大概率会看到其他项目用各自的方式跟上来。

---

*[English version](/allclaws/blog/2026/11/20/weekly-highlights-release-train-week/)*

*数据：[周报 digest 2026-11-20](https://github.com/dz3ai/allclaws/blob/main/docs/reports/weekly/2026-11-20-submodule-weekly.md)及 [docs/reports](https://github.com/dz3ai/allclaws/tree/main/docs/reports) 下各项目月报。窗口 2026 年 11 月 13–20 日，共 8 个追踪项目。*
