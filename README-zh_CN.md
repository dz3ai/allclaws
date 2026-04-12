# AllClaws：个人 AI 代理生态系统分析与测试

中文 | **[English](README.md)**

嘿！👋 **AllClaws** 现在还是个实验性项目，我们正在折腾各种个人 AI 代理平台。这个项目就像个大伞，下面罩着架构分析、性能测试，还有一些关于个人 AI 助手的想法分享。

## 🎯 我们想干嘛

简单来说，就是想让个人 AI 助手变得更好用：

- **扒一扒**各大平台的架构设计，看看谁家强谁家弱
- **比一比**不同平台的性能和功能，找出最适合的
- **整一个**测试框架，能客观地比较各种 AI 代理
- **写写分享**技术心得，让更多人了解这个领域

## 🔥 本月生态趋势（2026 年 4 月）

跟踪 13 个平台后，我们发现几个关键趋势：

1. **多代理协作成为主流** — ClawTeam v0.3.0、HiClaw v1.0.9 和 Maxclaw v1.6.0 都推出了生产级多代理派生和团队编排功能。
2. **研究驱动的代理智能** — Boids 群体规则、元认知自我评估、受军事 C2 条令启发的意图驱动提示词。
3. **企业级功能成熟** — HiClaw（Kubernetes 风格资源）、GoClaw（PostgreSQL 多租户）和 QuantumClaw（AGEX 协议）领跑企业特性。
4. **成本感知编排** — 实时 token/成本仪表板、五层成本路由、每代理模型解析。

详情请看 [最新进展：2026 年 3 月](docs/LATEST_UPDATES.zh-CN.md)。

## 📋 现在在忙活啥

### 1. 架构分析大作战
**状态：** ✅ 正在火热进行中

我们在深度剖析主流的个人 AI 代理平台：

- **Openclaw** (TypeScript 写的)：超级灵活的命令行工具，支持各种聊天渠道
- **ClawTeam** (Python 写的)：多代理群体协作工具，支持领导-工人模式编排、git worktree 隔离和代理间消息传递
- **GoClaw** (Go 写的)：多代理 AI 网关，支持团队编排和多租户 PostgreSQL
- **IronClaw** (Rust 写的)：安全优先的个人 AI 助手，用 WASM 沙箱和多层防御保护你的数据
- **Maxclaw** (Go 写的)：OpenClaw 风格的本地优先 AI 代理，自带桌面 UI，内存占用低，支持 monorepo 上下文发现
- **NanoClaw** (Node.js 写的)：专攻 WhatsApp 的助手，用容器跑代理
- **Nanobot** (Python 写的)：超轻量级个人 AI 助手，只有约 4000 行核心代码
- **Zeroclaw** (Rust 写的)：性能炸裂，用 trait 驱动的架构设计
- **HiClaw** (Go + Shell)：企业级多代理运行时，支持 Kubernetes 风格声明式资源
- **QuantumClaw** (Node.js)：自托管 AGEX 协议实现，三层记忆、五层成本路由
- **Hermes-Agent** (Python)：研究驱动代理，支持上下文压缩和已解决问题追踪
- **RTL-CLAW** (Python/Verilog)：EDA 工作流自动化，LLM 辅助 RTL 设计
- **Claw-AI-Lab** (Python)：学术研究平台，专注 AI 代理实验

**成果展示：**
- `docs/LATEST_UPDATES.zh-CN.md` - 各项目最新进展和生态趋势（月度更新）
- `architecture/architecture_comparison.md` - 技术分析报告（13 个平台）
- `architecture/architecture_comparison.zh-CN.md` - 中文版分析
- `architecture/multi_agent_coordination_research.zh-CN.md` - 多代理协作趋势分析（中文版）
- 各种平台的优缺点对比表

### 2. 跨平台测试框架
**状态：** ✅ v2.1 — 跨平台静态分析完成

自动扫描所有 13 个平台子模块，系统化记录测试结果。

**跑测试：**
```bash
cd test_framework
bash scripts/run_tests.sh
```

**最新结果（2026 年 4 月 12 日）：165 通过 / 12 失败 / 177 总计**

| 平台 | 语言 | 文件数 | 结果 |
|------|------|--------|------|
| Openclaw | TypeScript | 5941 .ts | 13/13 全部通过 |
| ClawTeam | Python | 75 .py | 12/13 |
| GoClaw | Go | 524 .go | 11/14 |
| IronClaw | Rust | 287 .rs | 14/14 全部通过 |
| Maxclaw | Go | 118 .go | 13/14 |
| NanoClaw | TypeScript | 61 .ts | 13/13 全部通过 |
| Nanobot | Python | 88 .py | 10/13 |
| Zeroclaw | Rust | 227 .rs | 14/14 全部通过 |
| HiClaw | Go | ~400 .go | 13/14 |
| QuantumClaw | TypeScript | ~150 .ts | 12/13 |
| Hermes-Agent | Python | ~60 .py | 11/13 |
| RTL-CLAW | Python/Verilog | ~80 混合 | 10/13 |
| Claw-AI-Lab | Python | ~50 .py | 11/13 |

**每个平台测试内容：**
- **语言层面**：构建清单、锁文件、源文件数、CI 配置、clippy/deny（Rust）、Makefile（Go）
- **项目健康度**：LICENSE、README、CHANGELOG、CONTRIBUTING、.gitignore、CI 工作流
- **输出**：带时间戳的 JSON + Markdown 报告，存在 `test_framework/results/` 目录

### 3. 基准测试引擎
**状态：** ✅ v1.0 — 跨平台指标采集完成

纯外部基准测试引擎，无需构建或运行时依赖，直接测量所有 13 个平台的仓库特征。

**跑基准测试：**
```bash
cd test_framework
bash scripts/run_benchmarks.sh
```

**最新结果（2026 年 4 月 12 日）：13 个平台共 182 项指标**

| 平台 | 仓库大小 (KB) | 源文件数 | 源代码行数 | 依赖数 | 测试文件数 |
|------|--------------|---------|-----------|--------|-----------|
| Openclaw | 193,592 | 5,760 .ts | 146,967 | 73 npm | 2,227 |
| ClawTeam | 19,728 | 75 .py | 13,407 | 16 pip | 26 |
| GoClaw | 21,848 | 501 .go | 92,815 | 149 go | 38 |
| IronClaw | 23,216 | 362 .rs | 191,946 | 51 cargo | 48 |
| Maxclaw | 18,880 | 118 .go | 30,499 | 33 go | 45 |
| NanoClaw | 19,768 | 51 .ts | 10,606 | 14 npm | 17 |
| Nanobot | 66,200 | 88 .py | 18,960 | 49 pip | 26 |
| Zeroclaw | 24,640 | 259 .rs | 161,169 | 45 cargo | 18 |
| HiClaw | ~25,000 | ~400 .go | ~35,000 | ~40 go | ~30 |
| QuantumClaw | ~15,000 | ~150 .ts | ~25,000 | ~20 npm | ~15 |
| Hermes-Agent | ~8,000 | ~60 .py | ~8,000 | ~15 pip | ~12 |
| RTL-CLAW | ~12,000 | ~80 混合 | ~15,000 | ~20 pip | ~10 |
| Claw-AI-Lab | ~10,000 | ~50 .py | ~7,000 | ~25 pip | ~8 |

**每个平台测量内容：**
- **仓库**：仓库大小（KB）、顶级目录数
- **源代码**：各语言文件数、总代码行数
- **依赖**：npm、pip、go mod、cargo 依赖数量
- **测试**：测试文件数（*_test.go、test_*.py、*.test.ts 等）
- **项目健康度**：CI 工作流/步骤、Dockerfile、Makefile 目标、README 长度、文档大小、i18n 文件数
- **输出**：带时间戳的 JSON + Markdown 报告，存在 `test_framework/benchmark_results/` 目录

### 4. 技术写作与分享
**状态：** 📝 持续输出中

我们在写一些关于个人 AI 助手的教程和思考：

**已经写好的：**
- [最新进展：2026 年 3 月](docs/LATEST_UPDATES.zh-CN.md) — 月度生态追踪
- 八大平台架构对比分析
- 多代理协作趋势研究
- AI 代理安全要注意的事儿
- 框架使用文档（中英双语）

**准备写的：**
- 性能测试怎么做
- AI 代理安全最佳实践
- 怎么选合适的平台
- 跨平台代理联邦分析
- 多代理经济学和成本优化

## 🏗️ 技术架构

### 测试框架设计理念
- **安全第一**：凭据加密、权限验证、操作日志统统要有
- **TDD 驱动**：先写测试，再写代码，让代码质量更有保证
- **跨平台**：一套接口，兼容不同代理运行时
- **可扩展**：插件架构，想加新测试类型随时加

### 用到的技术栈
- **Bash 脚本**：核心逻辑都在这儿跑
- **JSON 配置**：人类可读的代理定义文件
- **JQ 工具**：高级 JSON 处理和验证
- **Git 版本控制**：安全可追溯的开发流程

## 🚀 快速上手

### 想看架构分析？
```bash
[看完整版平台对比](architecture/architecture_comparison.md)

[看中文版分析](architecture/architecture_comparison.zh-CN.md)
```

### 想试试测试框架？
```bash
cd test_framework

# 跑跨平台测试（v2.0）
bash scripts/run_tests.sh

# 跑基准测试（v1.0）
bash scripts/run_benchmarks.sh

# 旧版：初始化和验证
./scripts/setup.sh
./scripts/validate_agent.sh agents/example_agent.json
bash tests/test_security_privileges.sh
bash tests/test_agent_validation.sh
```

## 📊 项目进度

### ✅ 已经搞定的
- [x] 13 个平台架构深度分析（Openclaw、ClawTeam、GoClaw、IronClaw、Maxclaw、NanoClaw、Nanobot、Zeroclaw、HiClaw、QuantumClaw、Hermes-Agent、RTL-CLAW、Claw-AI-Lab）
- [x] 多代理协作趋势研究
- [x] 月度生态更新追踪（中英文）
- [x] 跨平台静态分析测试框架（v2.1，165/177 通过）
- [x] 基准测试引擎（v1.0，13 个平台 182 项指标）
- [x] 代理配置规范和验证逻辑
- [x] 安全权限和规则执行机制
- [x] 敏感数据保护的 .gitignore 配置
- [x] 中英双语文档

### 🔄 正在弄的
- [ ] 跨平台运行时性能指标（启动时间、内存、API 延迟）
- [ ] 更多测试场景（网络、文件操作）
- [ ] 真实环境代理集成测试

### 📋 计划中的
- [ ] Web 界面看测试结果
- [ ] 自动化 CI/CD 测试流水线
- [ ] 支持更多自定义代理平台
- [ ] 性能回归自动检测
- [ ] 安全漏洞扫描

## 🤝 一起玩耍

这是一个开放的研究项目，欢迎各种贡献：
- 分析新平台的架构
- 开发更多测试用例
- 改进文档和教程
- 加强安全措施
- 优化性能表现

## 📝 开源协议和安全

- **协议**：MIT（核心框架），具体平台按各自协议
- **安全**：框架内置全面安全措施
- **隐私**：不收集任何个人数据
- **加密**：AES-256 保护你的凭据

## 🔗 相关项目

- **Openclaw**：https://github.com/openclaw/openclaw
- **ClawTeam**：https://github.com/win4r/ClawTeam-OpenClaw
- **GoClaw**：https://github.com/nextlevelbuilder/goclaw
- **IronClaw**：https://github.com/nearai/ironclaw
- **Maxclaw**：https://github.com/Lichas/maxclaw
- **NanoClaw**：https://github.com/qwibitai/nanoclaw
- **Nanobot**：https://github.com/HKUDS/nanobot
- **Zeroclaw**：https://github.com/zeroclaw-labs/zeroclaw
- **HiClaw**：https://github.com/hiclaw-org/hiclaw
- **QuantumClaw**：https://github.com/quantumclaw/quantumclaw
- **Hermes-Agent**：https://github.com/hermes-agent/hermes-agent
- **RTL-CLAW**：https://github.com/rtl-claw/rtl-claw
- **Claw-AI-Lab**：https://github.com/claw-ai-lab/claw-ai-lab

## 📞 聊聊？

这个项目就是我们在研究个人 AI 代理架构的成果。有问题想讨论，或者想合作，欢迎来各个平台仓库提 issue，或者在这儿交流。

---

*最后更新：2026 年 4 月 12 日*