# 最新进展：个人 AI 代理生态系统（2026 年 3 月）

中文 | **[English](LATEST_UPDATES.md)**

> 追踪 8 个个人 AI 代理平台的重大更新 — 架构革新、新增功能、性能提升和安全加固（2026 年 2-3 月）。

---

## 本月趋势

本月整个生态系统呈现出三大趋势：

1. **安全是头等大事** — OpenClaw 披露了多个关键 CVE（远程代码执行、沙箱绕过），NanoClaw 与 Docker 合作推出容器优先安全方案，Nanobot 因供应链安全问题移除了 litellm，IronClaw 修复了 5 个关键安全漏洞。
2. **端到端流式传输已成标配** — 每个活跃项目都实现了从模型到渠道的端到端流式传输。
3. **多模型提供商持续扩展** — 各项目纷纷接入 Codex OAuth、GitHub Copilot、Gemini、AWS Bedrock 等新后端。

---

## OpenClaw

**TypeScript | ~34 万星 | v2026.3.24 "Rehabilitation" — 2026 年 3 月 25 日**

**重大里程碑：** 创始人 Peter Steinberger 宣布加入 OpenAI（2 月 14 日），项目过渡至基金会治理。

### 架构革新
- **渠道插件架构重构** — WhatsApp 迁移至 `@openclaw/whatsapp` 插件
- **ACP（代理控制协议）+ 渠道运行时** 在发布后冲刺中统一（3 月 28 日）
- Node 22.14+ 最低版本支持（从 24 降低，但仍推荐 24）
- 新增 `/v1/models` 和 `/v1/embeddings` 网关端点，支持 RAG 兼容
- 原生应用架构：iOS/Android/macOS 作为节点设备通过 WebSocket 连接中央网关

### 新功能
- Microsoft Teams SDK 迁移，支持 AI 代理体验（流式一对一回复、欢迎卡片、输入指示器）
- 一键技能安装配方（coding-agent、gh-issues、whisper-api、session-logs 等）
- 控制面板 UI：状态筛选技能标签、磨砂玻璃背景设计
- Discord 自动线程命名（LLM 生成标题）
- `before_dispatch` 插件钩子
- `--container` / `OPENCLAW_CONTAINER` 支持 Docker/Podman 内运行命令
- macOS 应用：可折叠树形侧边栏

### 安全加固
- CVE-2026-25253：通过令牌窃取实现一键远程代码执行（2 月披露）
- CVE-2026-32038：沙箱网络隔离绕过
- 修复媒体沙箱绕过（`mediaUrl/fileUrl` 别名路径）(#54034)
- WhatsApp 回声循环 bug（3 月 22-27 日报告 6 个问题）

### 破坏性变更
v2026.3.24 包含 18 个破坏性变更：插件系统迁移、`/tools` 端点重设计、Teams SDK 迁移等。

---

## ZeroClaw

**Rust | ~2.91 万星 | v0.6.5 — 2026 年 3 月 27 日（218 次提交）**

### 架构革新
- **会话状态机**，支持 idle/running/error 状态追踪
- **每会话 Actor 队列**，实现并发对话序列化
- **共享迭代预算**，用于父代理/子代理协调
- **上下文溢出恢复** — 在调用模型前预检查，工具结果快速裁剪

### 新功能
- Matrix 渠道：自动端到端加密恢复、多房间监听、密钥遮蔽
- Slack 永久链接解析
- Web 仪表板：跨导航/刷新保持 Agent 聊天历史
- Coolify、Dokploy、EasyPanel 市场部署模板
- 快速发送者消息去抖

### 性能提升
- **<5MB 内存，<10ms 冷启动**（0.8GHz）— 内存占用比 OpenClaw 低 99%
- ~8.8MB 二进制文件，单个静态 Rust 二进制，零运行时依赖

### 安全加固
- 网关认证速率限制，防止暴力破解
- 冒充警告（2 月 19 日）：zeroclaw.org/net 域名非官方关联

---

## IronClaw

**Rust | 快速增长 | v0.23.0 — 2026 年 3 月 27 日**

> 本月最活跃项目：**3 月发布 8 个版本**（v0.15.0 → v0.23.0）。

### 架构革新
- **多租户认证**，按用户工作空间隔离
- **分层记忆**，基于敏感度自动隐私重定向
- **统一线程模型**用于 Web 网关
- 飞书/Lark WASM 渠道插件
- WASM 扩展版本控制（WIT 兼容性检查）
- AppEvent 提取至 `crates/ironclaw_common`
- Cargo-deny 供应链安全检查

### 新功能（v0.22.0 亮点）
- 每工具线程级推理（provider/session/surfaces）
- 完整 UX 大改版 — 设计系统、引导流程、Web 界面打磨
- Gemini CLI OAuth 集成（Cloud Code API）
- 低/中/高风险**命令审批级别**
- GitHub Copilot + OpenAI Codex 作为 LLM 提供商
- 公开 Webhook 触发端点（用于例程）
- 13 维复杂度评分器用于智能路由
- 导入 OpenClaw 记忆、历史、设置
- 国际化支持（中文 + 英文）
- AWS Bedrock LLM 提供商（原生 Converse API）
- Slack HMAC-SHA256 Webhook 签名验证

### 安全加固（修复 5 个关键漏洞）
- 验证嵌入基础 URL 防止 SSRF
- 转义工具输出 XML 内容
- 拒绝格式错误的 OAuth 状态
- 修复 rustls-webpki 漏洞（RUSTSEC-2026-0049）
- 所有安全关键密钥/令牌生成使用 OsRng
- 认证绕过、中继故障、无限递归、上下文膨胀 — 全部修复

### 性能提升
- 完整 LLM 响应缓存（set_model 失效、统计日志）
- Arc 嵌入缓存，避免未命中时的克隆
- 安全层热路径 Criterion 基准测试

---

## GoClaw

**Go | ~1300 星 | v2.43.1 — 2026 年 3 月 29 日（共 355 个版本）**

### 架构革新
- **车道调度器**（main/subagent/team/cron 车道）
- **代理团队**：共享任务板、代理间委派（同步/异步）、混合发现
- **GoClaw Lite 桌面版**：Wails v2 + React，~30MB，SQLite，最多 5 个代理

### 新功能
- **20+ LLM 提供商**（Anthropic 原生 HTTP+SSE 带提示缓存、OpenAI、Groq、DeepSeek、Gemini、Mistral、xAI、MiniMax 等）
- **7 个消息渠道**（Telegram、Discord、Slack、Zalo、飞书/Lark、WhatsApp、QQ）
- 按提供商扩展思维（Anthropic 预算 token、OpenAI 推理力度）
- **知识图谱**（LLM 提取 + 遍历，pgvector 混合 BM25 + 嵌入）
- BM25 + pgvector 混合搜索技能系统
- 心跳系统（HEARTBEAT.md 清单）
- OpenTelemetry OTLP 导出
- MCP 集成（stdio/SSE/streamable-http）
- 4 家 TTS 提供商，媒体生成（图片/音频/视频），浏览器自动化

### 性能
- ~35MB 空闲内存，<1s 启动，~25-36MB 二进制

---

## NanoClaw

**Python | 活跃开发中 | Docker 合作公告 — 2026 年 3 月 13 日**

### 架构革新
- **容器优先执行** — 默认所有操作在容器中运行
- 核心引擎约 4000 行代码（可审计，可放入 AI 代理上下文窗口）
- Andrej Karpathy 公开认可：*"核心引擎约 4000 行代码，能装进我脑子里"*

### 新功能
- Docker 沙箱集成（与 Docker Inc. 合作）
- 通过 Baileys 集成支持 WhatsApp（3 月 26 日合并）
- 代理社交网络连接（Moltbook、ClawdChat）

### 安全加固
- 容器优先模式是对 OpenClaw CVE-2026-25253（令牌窃取→RCE）和 CVE-2026-32038（沙箱绕过）的直接回应
- 创始人 Cohen 公开批评 OpenClaw 以明文存储 WhatsApp 消息
- 与 Docker 的企业沙箱联盟

---

## Nanobot

**Python | ~3.69 万星 | v0.1.4.post6 — 2026 年 3 月 27 日（57 个 PR，27 位新贡献者）**

### 架构革新
- **代理运行时解耦**：提取共享 `AgentRunner`，生命周期钩子统一为 `HookContext`
- 命令路由重构为插件友好结构
- **litellm 完全移除** — 替换为原生 OpenAI + Anthropic SDK（v0.1.4+）
- 子代理失败时进度保留

### 新功能
- **端到端流式传输**（provider → channel → CLI）
- **微信（Weixin）** 完整渠道支持（HTTP 长轮询、扫码登录）
- 飞书 CardKit 流式支持
- 完整引导向导
- 每会话并发调度
- 原生多模态感知能力
- GitHub Copilot OAuth 登录 + OpenAI Codex 提供商
- **12+ 渠道**：Telegram、Discord、Slack、WhatsApp、微信、飞书、钉钉、QQ、企微、Matrix、邮件、Mochat
- ClawHub 技能集成
- 火山引擎、MiniMax、Gemini、DeepSeek、Qwen、智谱、Moonshot、Mistral、OVMS、Step Fun 提供商
- 基于 Token 的记忆系统

### 安全加固
- GHSA-4gmr-2vc8-7qh3：邮件注入/伪造 — 默认强制 SPF/DKIM 验证
- 邮件内容标记 `[EMAIL-CONTEXT]` 防止 LLM 提示注入
- litellm 供应链投毒通告 — v0.1.4.post6 起完全移除
- 僵尸进程回收、会话投毒修复、更安全的默认访问控制

### 性能提升
- Anthropic 模型提示缓存优化
- 流式增量合并减少 API 调用
- 带完成余量预留的记忆整合
- Token 估算覆盖所有消息字段

---

## ClawTeam-OpenClaw

**Python | ~884 星 | v0.2.0+openclaw.1 — 2026 年 3 月 28 日**

### 架构革新
- 通过 git worktree 实现每代理会话隔离
- OpenClaw 代理的执行审批自动配置
- 生产级加固的 spawn 后端

### 新功能
- **ZeroMQ P2P 传输**（可选 `pip install -e ".[p2p]"`）
- **Web 仪表板**（`clawteam board serve --port 8080`）
- **团队模板**（TOML 格式，如 hedge-fund、ML research）
- **按代理模型分配**（预览分支 `feat/per-agent-model-assignment`）
- 计划审批工作流（提交/批准/拒绝）
- 跨机器支持（NFS/SSHFS 或 P2P）
- 多用户命名空间
- `fcntl` 文件锁保证并发安全

### 支持的代理
OpenClaw（默认）、Claude Code、Codex、nanobot、Cursor、自定义脚本

---

## Maxclaw

**Go + TypeScript | ~189 星 | v0.1.2 — 2026 年 3 月 17 日**

### 新功能
- 多渠道：Telegram、WhatsApp（Bridge）、Discord、WebSocket
- Cron/Once/Every 调度器 + 每日记忆摘要
- `executionMode=auto` 用于无人值守任务
- 自动任务标题（总结会话但不覆盖内容）
- Monorepo 感知递归上下文发现（AGENTS.md / CLAUDE.md）
- 子会话派生，独立上下文/模型/来源
- 桌面 UI + Web UI + API（同一端口）
- 浏览器自动化
- 一键安装脚本（Linux/macOS）
- Systemd 部署支持

---

## 对比总览

| 项目 | 星数 | 语言 | 最新版本 | 3 月发布数 | 内存占用 |
|------|------|------|---------|-----------|---------|
| OpenClaw | ~34 万 | TypeScript | 3 月 25 日 | 1 个大版本 | 高 |
| ZeroClaw | ~2.91 万 | Rust | 3 月 27 日 | 1 | **<5MB** |
| IronClaw | 快速增长 | Rust | 3 月 27 日 | **8** | 中等 |
| GoClaw | ~1300 | Go | 3 月 29 日 | ~30 | ~35MB |
| Nanobot | ~3.69 万 | Python | 3 月 27 日 | 4 | 中等 |
| NanoClaw | N/A | Python | 活跃开发 | 合作驱动 | 容器级 |
| ClawTeam | ~884 | Python | 3 月 28 日 | 1 | 极低（CLI） |
| Maxclaw | ~189 | Go+TS | 3 月 17 日 | 1 | 低 |

---

*最后更新：2026 年 3 月 29 日*
*所属：AllClaws 个人 AI 代理生态系统研究*
*下次更新：2026 年 4 月*
