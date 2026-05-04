# 最新进展：个人 AI 代理生态系统（2026 年 4-5 月）

**[English](LATEST_UPDATES.md)** | 中文

> 追踪 13 个 claw 生态平台和 7 个外部框架的重大更新 — 架构革新、MCP 采用争论、企业 vs 个人模式、安全发展（2026 年 4-5 月）。

---

## 本月趋势

2026 年 4-5 月呈现了塑造生态系统的四大趋势：

1. **MCP 争论激化** — 模型上下文协议在企业获得采用（mcp-agent、IronClaw、GoClaw、ZeroClaw），但本地优先代理（NanoClaw）因 20-30% 的 token 开销而抵制
2. **"自我改进"声明受质疑** — Hermes-Agent 源代码分析揭示程序记忆 ≠ 自主学习；这一区别现在被广泛认可
3. **企业 vs 一人公司分叉** — 企业自动化（治理、云、MCP）与个人力量倍增器（速度、本地、CLI）模式之间出现明显分歧
4. **外部框架纳入跟踪** — SmolAgents、LangGraph、CrewAI、AutoGen、Swarms、OpenAgents、mcp-agent 加入生态系统比较

---

## OpenClaw

**TypeScript | ~34 万星 | v2026.4.x — 2026 年 5 月**

**状态：** 基金会治理过渡继续（创始人加入 OpenAI 后）

### 架构演进
- 渠道插件生态系统扩展（WhatsApp、Discord、Teams、Matrix）
- 通过适配器模式集成 MCP（非原生）
- 原生应用平台增长（iOS/Android/macOS）

### 新功能（4-5 月亮点）
- 额外的 LLM 提供商集成
- 增强的流式传输可靠性
- 技能市场增长
- Webhook 安全改进

### 安全加固
- 持续修复 3 月披露的 CVE
- 容器执行选项增强

---

## ZeroClaw

**Rust | ~2.9 万星 | v0.6.x — 2026 年 5 月**

### 状态：性能领先者
- **<5MB 内存，<10ms 冷启动** 基准保持
- 生态系统中最高效的运行时

### 新功能
- MCP 适配器集成（stdio/SSE）
- 增强的会话状态管理
- 多房间渠道改进

---

## IronClaw

**Rust | 快速增长 | v0.23.x+ — 2026 年 5 月**

**状态：** 最活跃的 claw 平台

### 架构演进
- 多租户认证成熟度提升
- 分层记忆系统增强
- WASM 扩展生态系统增长

### 新功能
- **MCP 适配器集成**（非原生方法）
- 额外的 LLM 提供商
- 基于风险的命令审批细化
- 国际化扩展

### 安全加固
- 持续执行 cargo-deny
- 供应链审计

---

## GoClaw

**Go | ~1300 星 | v2.43.x+ — 2026 年 5 月**

### 架构演进
- 代理团队协调成熟化
- 车道调度器优化
- MCP 集成（stdio/SSE/streamable-http）

### 新功能
- 知识图谱增强
- OpenTelemetry 导出扩展
- 额外渠道和提供商

### 企业模式
- 多租户 PostgreSQL 架构
- 云部署优化

---

## NanoClaw

**Python | 活跃开发 | Docker 合作 — 2026 年 3-5 月**

### 状态：MCP 怀疑论者
- 明确避免 MCP 开销
- 容器优先安全模式
- ~4000 行代码核心哲学

### 立场
- **MCP 抵制**：本地部署的 token 成本顾虑
- 优先直接工具执行
- Docker 沙箱联盟持续

---

## Nanobot

**Python | ~3.7 万星 | v0.1.4.x+ — 2026 年 5 月**

### 架构演进
- 代理运行时解耦成熟化
- litellm 移除完成
- HookContext 标准化

### 新功能
- 渠道扩展（12+）
- LLM 提供商增长
- 基于 Token 的记忆细化

### 安全加固
- 供应链安全重点
- 邮件注入防护

---

## ClawTeam-OpenClaw

**Python | ~884 星 | v0.2.x+ — 2026 年 5 月**

### 多代理协调
- 领导者-工作者编排模式
- 每代理会话隔离
- ZeroMQ P2P 传输可选性

### 新功能
- Web 仪表板改进
- 团队模板扩展
- 计划审批工作流

---

## Maxclaw

**Go + TypeScript | ~189 星 | v0.1.x+ — 2026 年 5 月**

### 个人力量倍增器模式
- 本地优先部署
- Monorepo 感知上下文
- 桌面 UI + Web UI

### 新功能
- 子会话派生
- 浏览器自动化
- Systemd 部署

---

## HiClaw

**Go + Shell | 活跃开发 | v1.0.9 — 2026 年 4 月**

**状态：** 企业多代理运行时

### 架构：管理者-工作者模式
- Kubernetes 风格声明式资源
- 多代理编排
- 基于 Shell 的扩展性

### 关键功能
- 声明式资源定义
- 代理生命周期管理
- 企业部署重点

---

## QuantumClaw

**TypeScript | 活跃开发 | v1.6.0 — 2026 年 4-5 月**

**状态：** AGEX 协议实现

### 架构
- 原生多代理派生
- AGEX 协议支持
- 成本感知路由

### 关键功能
- 15 个团队预设
- 5 层成本路由
- 自托管重点

---

## Hermes-Agent

**Python | 研究支持 | v1.x — 2026 年 5 月**

**状态：** 声明验证完成

### 存在的功能
- ✅ 技能策展系统
- ✅ 跨会话记忆（FTS5 + LLM）
- ✅ MCP 集成
- ✅ 技能中心

### 缺失的功能
- ❌ 自主技能改进
- ❌ 基于强化学习的学习
- ❌ 性能跟踪

### 结论
**程序记忆 ≠ 自主学习** — "自我改进"声明被夸大

---

## RTL-CLAW

**Python/Verilog | 学术研究 | 活跃开发**

**状态：** EDA 工作流自动化

### 重点
- 电子设计自动化
- 硬件工作流 AI
- 学术研究平台

---

## Claw-AI-Lab

**Python | 学术研究 | 活跃开发**

**状态：** 教育研究平台

### 重点
- AI 代理教育
- 研究实验
- 学术合作

---

## 外部框架（新增跟踪）

### SmolAgents（Hugging Face）
**Python | ~26.7 万星 | ~1K 行代码核心**

- 代码生成模式（代理编写 Python）
- 最小可行框架参考
- 比较：Nanobot 工具调用 vs SmolAgents 代码生成

### LangGraph
**Python/TS | 企业采用**

- 基于图的编排
- 有状态工作流
- 企业模式比较

### mcp-agent
**Python | ~8200 星 | MCP 原生**

- MCP 参考实现
- "MCP is all you need" 愿景
- 原生 vs 适配器模式比较

### CrewAI
**Python | 角色扮演重点**

- 带角色的自主代理
- 多代理协调
- 企业用例

### AutoGen
**Python | 微软起源**

- 对话式代理框架
- 多代理对话模式
- 企业集成

### Swarms
**Python | ~5000 星 | 企业重点**

- 企业编排
- 云部署模式
- 治理框架对齐

### OpenAgents
**TypeScript | 分布式网络**

- 分布式代理架构
- 云原生设计
- 基于网络的协调

---

## 分叉分析：个人 vs 企业

| 方面 | 个人力量倍增器 | 企业自动化 |
|------|---------------|-----------|
| **主要关注点** | 速度、成本 | 治理、合规 |
| **部署** | 本地、单用户 | 云、多租户 |
| **工具访问** | CLI、直接执行 | MCP、协议 |
| **示例** | OpenClaw、Nanobot、SmolAgents、Maxclaw、IronClaw、ZeroClaw、NanoClaw | LangGraph、Swarms、HiClaw、GoClaw、CrewAI、AutoGen |

---

## 对比总览

| 项目 | 星数 | 语言 | MCP 状态 | 模式 |
|------|------|------|---------|------|
| OpenClaw | ~34 万 | TypeScript | 适配器 | 个人 |
| ZeroClaw | ~2.9 万 | Rust | 适配器 | 个人 |
| IronClaw | 增长中 | Rust | 适配器 | 个人/企业 |
| GoClaw | ~1300 | Go | 适配器 | 企业 |
| Nanobot | ~3.7 万 | Python | 无 | 个人 |
| NanoClaw | N/A | Python | 抵制 | 个人 |
| ClawTeam | ~884 | Python | 无 | 个人 |
| Maxclaw | ~189 | Go+TS | 无 | 个人 |
| HiClaw | N/A | Go+Shell | 适配器 | 企业 |
| QuantumClaw | N/A | TypeScript | 无 | 个人 |
| Hermes-Agent | N/A | Python | 原生 | 个人 |
| RTL-CLAW | N/A | Py/Verilog | N/A | 学术 |
| Claw-AI-Lab | N/A | Python | N/A | 学术 |
| SmolAgents | ~26.7 万 | Python | N/A | 个人 |
| LangGraph | N/A | Py/TS | N/A | 企业 |
| mcp-agent | ~8200 | Python | 原生 | 企业 |
| CrewAI | N/A | Python | N/A | 企业 |
| AutoGen | N/A | Python | N/A | 企业 |
| Swarms | ~5000 | Python | N/A | 企业 |
| OpenAgents | N/A | TypeScript | N/A | 企业 |

---

*最后更新：2026 年 5 月 5 日*
*所属：AllClaws 个人 AI 代理生态系统研究*
*跟踪平台：20 个（13 个 claw 生态 + 7 个外部框架）*
*下次更新：2026 年 6 月*
