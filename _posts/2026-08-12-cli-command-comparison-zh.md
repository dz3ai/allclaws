---
layout: post
title: "17 个 AI Agent 平台如何展示自己：CLI 命令对比"
date: 2026-08-12 17:10:00 +0800
author: Danny Zeng
categories: [研究, 对比]
tags: [cli, 命令行接口, agent平台, 对比, ux, 开发者体验]
lang: zh
---

每一个 AI agent 平台对同一个问题都有不同的答案：**用户如何与你交互？** 有的给你一条命令和一个聊天循环。有的给你 80 个子命令。有的给你 TUI，有的给你 REPL，有的只是往 stdout 打印文本。

在本机所有可安装的 CLI 上运行了 `--help`、并阅读了无法安装的那些的源代码之后，这里是一份关于 17 个 AI agent 平台如何向用户展示能力的结构化对比——以及这些选择揭示了怎样的设计哲学。

---

## 方法论

我从本机安装的五个平台（Hermes、kimi-cli、zeroclaw、opencode、reasonix）抓取了活的 `--help` 输出，并从 AllClaws 架构文档跟踪的其余平台的源代码和文档中提取了 CLI 架构细节。每个平台的条目涵盖：

- **命令名**：你输入什么来启动它
- **子命令数量**：有多少个不同的命令可用
- **调用模式**：REPL、TUI、one-shot、pipe 友好等
- **配置方式**：标志、配置文件、交互式设置
- **运维命令**：cron、监控、调试、备份
- **会话管理**：恢复、历史、导出

---

## 对比

### 1. Hermes-Agent (`hermes`)

**语言：** Python | **版本：** v0.20.0 | **子命令：** 81+

Hermes 拥有所有被跟踪平台中最庞大的 CLI。运行 `hermes --help` 会产出约 14,000 字符的输出，覆盖 81 个位置子命令和数十个标志。

**调用模式：**
- `hermes` — 经典 REPL（prompt_toolkit）
- `hermes --tui` — 现代终端 UI
- `hermes -z "prompt"` — One-shot 模式（仅 stdout，无 banner，无 spinner，面向脚本/管道）
- `hermes -w` — 隔离的 git worktree 模式（用于并行 agent）
- `hermes -s skill1,skill2` — 预加载技能

**按类别分组的关键子命令：**

| 类别 | 命令 |
|------|------|
| 核心 | `chat`、`model`、`fallback`、`moa`、`secrets` |
| 认证与凭据 | `auth`、`login`、`logout`、`egress` |
| 消息 | `gateway`、`send`、`whatsapp`、`whatsapp-cloud`、`slack`、`webhook`、`portal` |
| 调度 | `cron`、`pause`、`resume` |
| 项目管理 | `kanban`、`project`、`tasks` |
| 技能与插件 | `skills`、`bundles`、`plugins`、`curator` |
| 记忆与学习 | `memory`、`journey`、`learning`、`memory-graph` |
| 基础设施 | `proxy`、`lsp`、`mcp`、`computer-use`、`acp` |
| 监控 | `status`、`logs`、`sessions`、`insights`、`monitoring`、`dashboard` |
| 运维与调试 | `doctor`、`verify`、`security`、`approvals`、`dump`、`debug`、`backup`、`checkpoints`、`import` |
| 配置与 Profile | `config`、`profile`、`skin`、`completion`、`hooks` |
| 桌面与 GUI | `dashboard`、`serve`、`desktop`、`gui` |

**设计哲学：** "一切皆子命令。" Hermes 把 CLI 当作每个功能的主接口——消息、调度、技能、记忆、监控、桌面 GUI、MCP 服务器、安全审计。CLI 就是控制平面。不存在"面向用户的功能"与"管理员功能"之分——全在一个命名空间里。

**值得关注的设计选择：**
- `-z` one-shot 模式只把最终响应写入 stdout（管道友好，CI 兼容）
- `--usage-file` 用于脚本化运行的成本追踪
- `--safe-mode` 禁用所有自定义（排障用）
- `--yolo` 绕过所有审批 prompt
- `--worktree` 为并行 agent 创建隔离的 git worktree
- ACP 服务器模式（`hermes acp`）用于 IDE 集成

---

### 2. OpenClaw (`openclaw`)

**语言：** TypeScript | **入口：** `src/cli` | **星标：** ~340K

OpenClaw 的 CLI 无法直接测试（npm 二进制启动的 TUI 在 WSL 里超时），但架构文档揭示了它的结构。

**架构：**
- 入口在 `src/cli`，命令在 `src/commands`
- 单 agent 架构 + channel/插件扩展
- 37+ 消息 channel（Telegram、Discord、Slack、Signal、iMessage、Web 等）
- 用于额外平台（MSTeams、Matrix）的扩展系统

**设计哲学：** "成为 channel。" OpenClaw 本质上是一个路由平台——它从任何 channel 接收输入，通过 AI agent 处理，再输出到任何 channel。CLI 是众多 channel 之一，而不是主要的那个。架构上 `src/provider-web.ts` 和 `src/routing` 的分量重过 `src/commands`。

**CLI 性格：** 极简而聚焦。OpenClaw 的 CLI 的存在是为了配置 channel、启动 agent 循环、管理插件。它不试图成为通用控制平面。37+ 个 channel 才是差异化所在，不是命令数量。

---

### 3. ClawTeam (`clawteam`)

**语言：** Python 3.10+ | **架构：** 多代理（Leader-Worker）

ClawTeam 的 CLI 是所有平台中最领域特定的——每个子命令都映射到一个多代理工作流概念。

**关键子命令组：**

| 组 | 命令 | 用途 |
|----|------|------|
| 团队生命周期 | `team spawn-team`、`team cleanup` | 创建/销毁 agent 团队 |
| agent 生成 | `spawn` | 通过 tmux 启动 worker |
| 任务管理 | `task create`、`task update`、`task wait` | 管理带依赖链的任务 |
| 代理间消息 | `inbox send`、`inbox broadcast` | P2P 与广播通信 |
| 监控 | `board show`、`board live`、`board serve` | kanban 看板、实时视图、Web UI |
| 工作区 | `workspace checkpoint`、`workspace merge` | git worktree 管理 |

**设计哲学：** "编排 agent，而不是成为 agent。" ClawTeam 的 CLI 是团队管理接口，不是 agent 聊天接口。你不通过 ClawTeam 与 AI 对话——你生成一个互相交谈的 agent 团队。CLI 子命令映射工作流：建团队、定义任务、看板、合并结果。

**值得关注：** 使用 TOML 团队模板（`clawteam launch hedge-fund --team fund1`）实现可复现的团队配置。ZeroMQ P2P 选项用于跨机器协调。kanban 看板（`board live`）提供所有 agent 的 tmux 平铺视图。

---

### 4. GoClaw (`goclaw`)

**语言：** Go 1.26 | **入口：** `cmd/goclaw/main.go` | **二进制大小：** ~25MB

GoClaw 的 CLI 反映了它作为网关服务器的身份——主命令启动网关，子命令管理周边基础设施。

**推断的 CLI 结构**（来自 `cmd/` 模块分析）：
- 网关启动（主命令——WS + HTTP 服务器）
- Onboarding 向导
- 迁移工具
- 配置管理（JSON5 + 环境变量）

**设计哲学：** "单一二进制，全栈。" GoClaw 以一个约 25MB 的 Go 二进制交付，内含网关服务器、agent 循环、提供商集成和管理工具。CLI 是部署工具。你运行 `goclaw` 启动网关，然后通过 Web 仪表盘、WebSocket RPC 或 HTTP API（`/v1/chat/completions`、`/v1/agents`、`/v1/skills`）与 agent 交互。

**CLI 性格：** 面向基础设施。与 Hermes（一切皆子命令）或 ClawTeam（编排即子命令）不同，GoClaw 的 CLI 关注部署和配置。agent 交互发生在网关的 RPC 和 HTTP 接口上，而不是 CLI 子命令里。这与它的企业定位一致——你不会 SSH 到生产服务器上跟 agent 聊天。

---

### 5. IronClaw (`ironclaw`)

**语言：** Rust | **入口：** `src/main.rs`

IronClaw 的 CLI 架构强调安全原语和沙箱管理。

**Channel 结构：**
- REPL（主要交互方式）
- HTTP webhook
- WASM channel（动态工具加载）
- Web 网关（SSE/WebSocket）

**设计哲学：** "安全第一，CLI 只是众多 channel 之一。" IronClaw 把 REPL 当作与 HTTP webhook 和 WASM channel 并列的 channel——不是主接口。架构重心在沙箱编排器（Docker）、工具注册表（内置 + MCP + WASM）和安全层（prompt 注入防御、宿主边界的凭据注入）。

---

### 6. ZeroClaw (`zeroclaw`)

**语言：** Rust | **版本：** 0.1.7 | **星标：** ~29K | **内存：** <5MB | **冷启动：** <10ms

ZeroClaw 拥有所有平台中最*一致*的 CLI——干净、结构良好、基于 Rust clap 的帮助输出，每个子命令都带示例。

**子命令（22 个）：**

| 类别 | 命令 |
|------|------|
| 核心 agent | `onboard`、`agent`、`daemon`、`service` |
| 网关与 channel | `gateway`、`channel`、`integrations` |
| 调度 | `cron`（list、add、add-at、add-every、once、remove、update、pause、resume） |
| 记忆与技能 | `memory`、`skills`（list、audit、install、remove） |
| 模型与提供商 | `models`、`providers`、`auth` |
| 硬件 | `hardware`、`peripheral`（STM32、RPi GPIO） |
| 运维 | `status`、`doctor`、`estop`、`config`、`completions`、`migrate` |

**设计哲学：** "快、小、完整。" ZeroClaw 的 CLI 胜在平衡——22 个子命令覆盖完整 agent 生命周期（onboarding、agent 循环、daemon、调度、技能、硬件、监控），没有 Hermes 81+ 命令的蔓延。每个子命令的 `--help` 输出都带示例。

**值得关注的设计选择：**
- `agent -m "prompt"` 单次执行，不进入交互模式
- `estop` 紧急停止 daemon 和 channel
- 硬件外设支持（STM32、RPi GPIO）——生态中独此一家
- `daemon` 是一等命令（网关 + channel + 心跳 + 调度器作为单一长驻进程）

---

### 7. OpenCode (`opencode`)

**语言：** TypeScript | **版本：** v1.18.18 | **星标：** ~198K

OpenCode 是"开源编程 agent"——TUI 优先的编程助手，支持 ACP 和 MCP，外加独特的 headless 服务器模式用于远程协作。

**子命令（21 个）：**

| 类别 | 命令 |
|------|------|
| 核心 | `opencode [project]`（TUI，默认）、`run [message..]`、`attach <url>` |
| 服务器 | `serve`（headless）、`web`（服务器 + 浏览器 UI） |
| 协议 | `acp`（ACP 服务器）、`mcp`（MCP 管理） |
| 提供商与模型 | `providers`（即 `auth`）、`models [provider]` |
| GitHub | `github`（GitHub agent）、`pr <number>`（拉取 PR 分支后进入 TUI） |
| 会话 | `session`（管理）、`export [sessionID]`、`import <file>` |
| Agent 与插件 | `agent`（管理 agent）、`plugin <module>`（安装与配置） |
| 运维 | `debug`、`stats`（token 用量/成本）、`db`、`upgrade`、`uninstall`、`completion` |

**调用模式：**
- `opencode` — 启动 TUI（默认）
- `opencode run "prompt"` — 带消息运行（非交互）
- `opencode serve` — headless 服务器
- `opencode web` — 服务器 + 浏览器 UI
- `opencode attach <url>` — 连接远程服务器
- `opencode --mini` — 最小交互界面
- `opencode -c` / `-s <id>` — 继续上一个或指定会话

**值得关注的设计选择：**
- `--fork` 在继续会话时 fork（从先前状态分叉）
- `--pure` 不加载外部插件运行
- `--mdns` 用于局域网 mDNS 服务发现（找到运行中的实例）
- `--cors` 用于 headless 服务器的跨域配置
- `--auto` 自动批准所有未被显式拒绝的权限（文档明示危险的模式）
- `--port` / `--hostname` 显式绑定服务器；`--mdns-domain` 自定义发现域名
- `--replay-limit` 限制 mini 模式恢复时的会话回放条数
- `pr <number>` 拉取 GitHub PR 分支后启动 TUI——其他平台没有的工作流专属命令
- `stats` 把 token 用量和成本追踪作为一等命令

**设计哲学：** "TUI 优先，服务器可选。" OpenCode 的默认体验是 TUI，但它独特地同时提供 headless `serve` 模式和带浏览器 UI 的 `web` 模式。`attach <url>` 命令和 mDNS 发现暗示了一个同时支持本地开发和远程协作的设计——你可以在服务器上运行 opencode，从笔记本 attach 上去。`pr` 命令把 GitHub 工作流接进 agent 循环，把 PR 审查当作一等用例。

---

### 8. Nanobot (`nanobot`)

**语言：** Python 3.11+ | **星标：** ~37K | **入口：** `nanobot/__main__.py`（Typer）

Nanobot 把"超轻量"哲学带进了 CLI 设计。

**架构：**
- CLI 用 Python Typer（从类型提示自动生成帮助）
- 单 agent + subagent 支持
- 8+ channel（Telegram、Discord、Slack、WhatsApp、飞书、QQ、Email、Matrix、CLI）
- MCP 桥接（可用但非核心）
- LiteLLM 多提供商支持

**设计哲学：** "一条命令，一个 agent。" Nanobot 的 CLI 是极简的，因为平台本身就是极简的（核心约 4,000 行）。Typer 从类型注解自动提供良好的帮助输出。重心在 `pip install nanobot-ai` 和开箱即用，而不是全面的子命令覆盖。

---

### 9. Maxclaw (`maxclaw`)

**语言：** Go 1.24+ | **星标：** ~189 | **二进制：** `maxclaw`、`maxclaw-gateway`

Maxclaw 交付两个二进制——一个给 agent，一个给网关。

**架构：**
- `cmd/main.go` — agent CLI，支持子会话生成
- `maxclaw-gateway` — 独立网关二进制
- 桌面 UI + Web UI 同端口
- Monorepo 上下文发现（AGENTS.md、CLAUDE.md）
- 分层记忆（MEMORY.md、HISTORY.md、heartbeat.md）

**设计哲学：** "本地优先，配视觉界面。" Maxclaw 独特地把桌面 UI 和 Web UI 绑定在同一端口。CLI 是与视觉界面并列的一种界面。子会话生成让单个 maxclaw 实例内可以跑并行 agent。

---

### 10. NanoClaw (`nanoclaw`)

**语言：** TypeScript（Node.js） | **入口：** `src/index.ts`

NanoClaw 是最以容器为中心的平台——它的"CLI"本质上是一个编排器进程。

**架构：**
- 单 Node.js 编排器进程
- Claude Agent SDK 在每组隔离容器中运行
- 每组一个 CLAUDE.md 作为记忆
- IPC watcher 用于进程间通信
- 任务调度器
- WhatsApp 作为主 channel

**设计哲学：** "容器，而非命令。" NanoClaw 的 CLI 是一个生成容器化 agent 实例的 IPC 编排器。"命令"就是容器生命周期管理——启动、停止、监控。传统意义上的 REPL 不存在；你通过 WhatsApp 群组交互，每个群组一个隔离在自己容器里的 Claude agent。

---

### 11. HiClaw (`hiclaw`)

**语言：** Go + Shell | **部署：** Docker Compose / Kubernetes

HiClaw 是唯一使用 Kubernetes 风格声明式资源的平台。

**架构：**
- `hiclaw` CLI 配 Docker Compose
- YAML 资源定义（Worker、Team、Human）
- Worker 模板市场
- 基于 Nacos 的技能发现
- Manager-Workers 运行时（CoPaw）

**设计哲学：** "给 agent 的声明式基础设施。" HiClaw 的 CLI 最接近 `kubectl`——你把 worker、team 和 human-in-the-loop 资源定义为 YAML 文件然后 apply。CLI 管理资源生命周期而非 agent 交互。这是企业自动化范式推到逻辑终点：agent 就是 Kubernetes 资源。

---

### 12. Hermes-Agent（源码分析 vs 实测抓取）

架构文档把 Hermes 描述得比实测 `--help` 揭示的更简单。文档记的是：
- 入口：`hermes` CLI
- 架构：带上下文管理的单 agent
- MCP 原生集成

实测 CLI（v0.20.0）展示的是一个远超"带上下文管理的单 agent"的平台——一个完整的 agent 操作系统，81+ 子命令横跨消息、调度、技能、记忆、监控、桌面 GUI 和 MCP 服务器管理。

---

### 13. aider (`aider`)

**语言：** Python | **星标：** ~68K | **入口：** `aider` CLI

aider 是最聚焦的 CLI——它只做一件事（AI 编辑代码），并通过聊天界面完成。

**架构：**
- REPL 结对编程循环
- git 感知（用合理的 message 自动提交）
- 编辑模式：Whole Edit、Diff Edit、Architect
- Repo Map 用于大代码库上下文
- 20+ LLM 提供商

**设计哲学：** "结对编程，不是平台。" aider 没有调度、技能、消息或监控的子命令。它是一个带 git 集成的聊天循环。你说，它改代码，git 提交结果。极简就是重点——68K 星来自把一件事做到极致。

---

### 14. Claude Code (`claude`)

**语言：** TypeScript（Anthropic） | **入口：** `claude`

Claude Code 是 Anthropic 官方 CLI 编程 agent。无法从 WSL 直接测试（启动的 TUI 会超时）。

**架构：**
- 终端编程 agent
- ACP 协议支持
- 沙箱执行
- 交互式审批循环

**设计哲学：** "Anthropic 的终端 agent。" Claude Code 是 Anthropic 终端 AI 编程愿景的参考实现。它遵循极简 CLI 表面的模式——你运行 `claude`，它开启会话，你写代码。简单是刻意为之。

---

### 15. kimi-cli (`kimi-cli`)

**语言：** Python | **星标：** ~8.8K | **版本：** 1.24.0

来自 MoonshotAI 的 kimi-cli，相对其子命令数量，拥有所有平台中*选项最密集*的帮助输出。

**调用模式：**
- `kimi-cli` — 交互 agent（默认）
- `kimi-cli -p "prompt"` / `-c "prompt"` — 单次 prompt
- `kimi-cli --print` — 打印模式（非交互，隐含 `--yolo`）
- `kimi-cli --quiet` — `--print --output-format text --final-message-only` 的简写
- `kimi-cli --acp` — ACP 服务器模式（已弃用，现为 `kimi-cli acp`）
- `kimi-cli --wire` — Wire 服务器（实验性）

**子命令（9 个）：**

| 命令 | 用途 |
|------|------|
| `login` / `logout` | 账号管理 |
| `term` | Toad TUI，由 Kimi Code ACP 服务器支撑 |
| `acp` | ACP 服务器 |
| `info` | 版本与协议信息 |
| `export` | 会话数据导出 |
| `mcp` | MCP 服务器配置管理 |
| `vis` | agent 追踪可视化 |
| `web` | Web 界面 |

**值得关注的设计选择：**
- `--agent [default|okabe]` 和 `--agent-file FILE` 用于自定义 agent 规格
- `--input-format [text|stream-json]` 和 `--output-format [text|stream-json]` 用于管道集成
- `--mcp-config-file FILE`（可重复）用于多个 MCP 配置
- `--skills-dir DIRECTORY` 用于技能发现
- `--thinking` / `--no-thinking` 推理模式开关
- `--max-steps-per-turn`、`--max-retries-per-step`、`--max-ralph-iterations` 细粒度控制

**设计哲学：** "可配置的 agent，多界面。" kimi-cli 提供所有平台中最细粒度的每次调用配置。agent 行为的每个方面都可以通过标志调——模型、思考模式、步数上限、重试上限、MCP 配置、agent 规格、技能目录。三种界面模式（交互、print、wire/ACP）加上 agent 追踪可视化（`vis`），暗示这是一个同时为终端用户编程和开发者工具链设计的平台。

---

### 16. Codex (`codex`)

**语言：** Rust | **星标：** ~86.9K | **入口：** `codex` CLI

OpenAI 的 Codex 是星标最多的 CLI agent，也是架构上最简单的。

**架构：**
- 简单的 CLI → LLM → shell 执行循环
- 沙箱执行（所有代码在隔离环境中运行）
- 单二进制，零运行时开销
- 模型：GPT-4o、o3、o4-mini

**设计哲学：** "单二进制，单循环。" Codex 是反 Hermes。一条命令，一个循环，沙箱执行，完事。没有技能、调度、消息或监控的子命令。沙箱是差异化所在——每次代码执行都是隔离的，对 CI/CD 管道是安全的。

---

### 17. Reasonix (`reasonix` / `dsnix`)

**语言：** TypeScript | **版本：** v0.52.0 | **星标：** ~34.6K | **入口：** `dist/cli/index.js` | **冷启动：** ~287ms

Reasonix（esengine/DeepSeek-Reasonix）是"DeepSeek 原生编程 agent"——也是本次对比中唯一拥有**两个命令名**的平台：`reasonix` 和 `dsnix` 指向同一个二进制。它的 CLI 哲学围绕一个经济性理念构建：DeepSeek 的上下文缓存。子命令的存在就是为了让缓存命中率可见、可干预。

**子命令（19 个）：**

| 类别 | 命令 |
|------|------|
| 安装与健康 | `setup`（交互式向导）、`doctor`、`doctor-cache`、`update`、`version` |
| 核心聊天 | `chat`（带实时缓存/成本面板的 Ink TUI）、`code [dir]`（带文件系统工具的编程聊天） |
| 非交互 | `run <task>`（流式 one-shot）、`desktop`（面向桌面客户端的 headless JSON-RPC） |
| ACP | `acp`（stdio NDJSON 上的 Agent Client Protocol） |
| 可观测性 | `stats [transcript]`（使用情况仪表盘）、`events <name>`（内核事件日志美化打印）、`replay <transcript>`（转录稿浏览 TUI）、`diff <a> <b>`（分栏转录稿对比） |
| 会话 | `sessions`、`prune-sessions`（删除空闲 ≥N 天的会话，`--dry-run`）、`-c/--continue`、`-r/--resume`、`-n/--new` |
| 成本与数据 | `commit`（从暂存 diff 起草提交消息）、`mcp`（MCP 发现 + 配置测试）、`index`（本地语义搜索索引） |

**设计哲学：** "成本是一等公民。" Reasonix 是这里唯一把**会话美元预算内置到调用里**的 CLI：`--budget <usd>` 在 80% 时警告，100% 时*拒绝下一轮*（不只是警告——是硬门禁）。`chat` TUI 在你输入时显示实时缓存命中/成本面板，`stats` 把历史转录稿变成使用仪表盘，`doctor-cache` 是专门针对缓存稳定性的健康检查。kimi-cli 让每个*行为*可配置，Reasonix 让每个*成本维度*可见：预算上限、按转录稿记账、缓存健康。它是 kimi-cli 配置优先设计的经济学优先对照。

**值得关注的设计选择：**
- `--budget <usd>` — 每会话花费上限，80% 警告，100% 硬拒绝
- `--effort low|medium|high|max` — 每种调用模式都有的推理强度旋钮
- `--no-mouse` — 关闭 SGR 鼠标跟踪，恢复终端原生拖选（其他 CLI 都没处理的痛点）
- `--no-proxy` — 单次运行绕过代理，适合 GFW 邻近网络
- `--dashboard-port` / `--dashboard-host` — 内嵌 Web 仪表盘的固定端口 + 局域网绑定（SSH 隧道友好）
- `--mcp <spec>` 可重复，配 `--mcp-prefix` 给工具名加命名空间
- `--profile` — 记录 V8 CPU profile，用于性能 bug 报告
- 双语帮助输出（中文描述 + 英文命令名）
- `diff <a> <b>` — 唯一能*分栏对比两份 agent 转录稿*的 CLI
- `code` 上的 `dry-run` 标志用于 ssh:// 目标——解析 URI、检查本地 SSH、打印计划步骤，不执行任何远程命令

**交叉引用：** Reasonix 实现了 one-shot（`run`）、TUI（`chat`）、ACP 服务器（`acp`）、MCP 管理（`mcp`）、会话恢复（`-c`/`-r`）和自更新（`update`）——与 Hermes 和 OpenCode 相同的六个能力点，代码量只是零头。


---

## 跨平台分析

### 子命令数量光谱

```
Hermes       ████████████████████████████████████████████  81+
OpenCode     ████████████████████████  21
ZeroClaw     ██████████████████  22
Reasonix     ██████████████████  19
kimi-cli     ████████  9
ClawTeam     ████████  ~8 组
GoClaw       █████  ~5
codex        ██  1-2
aider        ██  1
```

### 调用模式矩阵

| 平台 | REPL | TUI | One-shot | Print/管道 | git worktree | ACP 服务器 | Wire 协议 |
|------|------|-----|----------|-----------|-------------|------------|-----------|
| **Hermes** | ✓ | ✓ | `-z` | ✓ | `-w` | `acp` | ✗ |
| **OpenCode** | ✗ | ✓ | `run` | ✗ | `--fork` | `acp` | ✗ |
| **kimi-cli** | ✓ | `term` | `-p` | `--print` / `--quiet` | ✗ | `acp` | `--wire` |
| **Reasonix** | ✗ | `chat`/`code` | `run` | ✗ | ✗ | `acp` | `desktop` JSON-RPC |
| **ZeroClaw** | ✓ | ✗ | `-m` | ✗ | ✗ | ✗ | ✗ |
| **aider** | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| **codex** | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| **OpenClaw** | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| **ClawTeam** | ✗ | ✗ | ✗ | ✗ | 每 agent | ✗ | ✗ |
| **GoClaw** | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | RPC |

### 配置方式

| 方式 | 平台 | 说明 |
|------|------|------|
| 标志优先 | kimi-cli、ZeroClaw | 每个选项都是 CLI 标志，配置文件可选 |
| 标志优先、成本感知 | Reasonix | 每个选项都是标志，外加每会话 `--budget` 上限 |
| 配置文件优先 | GoClaw、HiClaw | JSON5/YAML 配置文件，CLI 用于覆盖 |
| 交互优先 | Hermes、OpenClaw | `setup` 向导，然后是配置文件 |
| 零配置 | ClawTeam、Nanobot | 安装后立即可用 |
| 环境变量 | IronClaw、NanoClaw | 环境变量存密钥 |

### 运维命令覆盖

| 能力 | Hermes | ZeroClaw | kimi-cli | OpenCode | ClawTeam | GoClaw | aider | codex | Reasonix |
|------|--------|----------|----------|----------|----------|--------|-------|-------|----------|
| Cron/调度 | ✓ | ✓ | ✗ | ✗ | ✓（tasks） | ✓ | ✗ | ✗ | ✗ |
| 监控/仪表盘 | ✓ | ✓ | ✓（vis） | ✓（stats） | ✓（board） | ✓ | ✗ | ✗ | ✓（stats + Web 仪表盘） |
| 会话恢复 | ✓ | ✗ | ✓（`-S`、`-C`） | ✓（`-c`、`-s`） | ✗ | ✗ | ✗ | ✗ | ✓（`-c`、`-r`） |
| 会话导出 | ✓ | ✗ | ✓（`export`） | ✓（`export`） | ✗ | ✗ | ✗ | ✗ | ✓（`--transcript` JSONL） |
| 成本/预算上限 | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✓（`--budget`） |
| 备份/恢复 | ✓ | ✓（migrate） | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| Doctor/调试 | ✓ | ✓ | ✗ | ✓（`debug`） | ✗ | ✗ | ✗ | ✗ | ✓（`doctor`、`doctor-cache`） |
| 安全审计 | ✓ | ✗ | ✗ | ✗ | ✗ | ✓ | ✗ | ✗ | ✗ |
| MCP 管理 | ✓ | ✗ | ✓（`mcp`） | ✓（`mcp`） | ✗ | ✓ | ✗ | ✗ | ✓（`mcp`） |
| 技能/插件 | ✓ | ✓ | ✓（`--skills-dir`） | ✓（`plugin`） | ✗ | ✓ | ✗ | ✗ | ✗ |
| Shell 补全 | ✓ | ✓ | ✗ | ✓（`completion`） | ✗ | ✗ | ✗ | ✗ | ✗ |

---

## CLI 揭示的平台哲学

### Unix 哲学光谱

**Hermes** 在一个极端："一切通过 CLI。" 81+ 子命令，每个功能都暴露，从 `hermes dashboard` 到 `hermes pets`。CLI 即平台。

**Codex 和 aider** 在另一个极端："通过 CLI 只做一件事。" 聊天循环，git 集成，完事。CLI 是核心 agent 循环外面的一层薄壳。

**ZeroClaw** 和 **kimi-cli** 占据中间地带：足够覆盖 agent 生命周期（调度、技能、监控）的子命令，没有蔓延。ZeroClaw 的 22 个命令和 kimi-cli 的 9 个命令 + 丰富标志集，暗示一种刻意的设计约束——足够有用，不至于令人不知所措。

### "操作系统"与"工具"的分野

Hermes、ZeroClaw 和 GoClaw 表现得像 agent 的操作系统——它们管理完整生命周期：安装、配置、调度、监控、调试、备份、更新。它们的 CLI 反映了这一点：`doctor`、`backup`、`update`、`migrate`、`estop`。

aider、codex 和 Claude Code 表现得像工具——需要时运行，做完工作，退出。没有 daemon，没有调度器，没有备份。它们的 CLI 反映了这一点：表面极简，交互聚焦。

ClawTeam 占据独特位置：它是*其他* agent 的操作系统，不是自己的。它的 CLI 管理 aider/Codex/OpenClaw 实例的团队。它没有 AI 聊天循环——它有的是团队生命周期管理。

### 收敛模式

三种 CLI 模式正在生态中收敛：

1. **One-shot 模式**（Hermes `-z`、kimi-cli `--print`、ZeroClaw `-m`）——每个平台最终都会为脚本和 CI 集成添加非交互模式。

2. **ACP/Wire 协议**（Hermes `acp`、kimi-cli `acp`/`--wire`、copilot-cli ACP）——Agent Communication Protocol 正在成为 IDE 集成的标准，kimi-cli 在 wire 协议实验上领先。

3. **MCP 配置成为 CLI 职责**（Hermes `mcp`、kimi-cli `mcp`、GoClaw adapter）——管理 MCP 服务器正在成为一等 CLI 操作，不再只是配置文件的事。

### 缺失的命令

每个平台都缺了点什么：

- **aider 和 codex** 没有调度。你不能说"每天早上跑这个编程任务"。它们是纯交互的。
- **ClawTeam** 没有凭据管理 CLI。凭据在 TOML 文件或环境变量里。
- **GoClaw** 没有备份/恢复。企业基础设施被假定由外部管理。
- **Hermes** 没有 one-shot *纯打印*模式下同时输出 JSON 的能力（kimi-cli 的 `--output-format stream-json` 更管道友好）。
- **ZeroClaw** 没有会话恢复。每次 `agent` 调用都是全新的。
- **kimi-cli** 尽管有最丰富的每次调用配置，却没有 cron 或调度。
- **Reasonix** 没有调度，也没有 shell 补全。它的成本工具无可匹敌，但你说不了"每天早上跑这个"——预期模式是用系统 cron 驱动它的 `run` one-shot。

---

## 结论

CLI 是一个平台最诚实的接口。文档可以夸大能力。营销可以误导。但 `--help` 输出是用户实际看到的，它揭示了真实的优先级：

- **Hermes** 优先完整性——每个功能都有命令
- **ZeroClaw** 优先一致性——每个命令都有示例和干净的帮助
- **kimi-cli** 优先可配置性——每次调用都可以精细调校
- **OpenCode** 优先远程协作——serve、attach、mDNS 发现
- **aider** 优先聚焦——一个循环，做到极致
- **codex** 优先安全——单二进制，沙箱，极简
- **ClawTeam** 优先编排——命令面向团队，而非聊天
- **GoClaw** 优先基础设施——命令面向部署，而非交互
- **Reasonix** 优先经济学——每次调用都有预算上限和缓存可见性

2026 年最好的 CLI 会把 Hermes 的完整性、ZeroClaw 的一致性、kimi-cli 的可配置性、OpenCode 的远程协作和 Reasonix 的成本纪律结合起来。还没有人做到全部五点。

---

*实测 CLI 抓取自 Hermes v0.20.0、OpenCode v1.18.18、kimi-cli v1.24.0、zeroclaw v0.1.7、reasonix v0.52.0。架构文档来自覆盖所有被跟踪平台的 AllClaws 平台对比。完整架构细节见 [platform_comparison.md](https://github.com/dz3ai/allclaws/blob/main/architecture/platform_comparison.md)。*

*[English version](/allclaws/blog/2026/08/12/cli-command-comparison/)*
