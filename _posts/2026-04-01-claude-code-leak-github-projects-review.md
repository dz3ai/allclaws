---
layout: post
title: "Claude Code 源代码泄露：GitHub 研究项目全景分析"
date: 2026-04-01 14:00:00 +0800
author: Danny Zeng
categories: [Security Research]
tags: [Claude Code, source leak, security research, supply chain, GitHub]
---

## Executive Summary

2026年3月31日，Claude Code 的完整源代码通过 npm source map 意外泄露。这一事件迅速引发了安全社区的广泛关注，GitHub 上出现了多个研究仓库。本文将对这些项目进行全面梳理和对比分析，并介绍我们项目（[dz3ai/claudecode-leaks](https://github.com/dz3ai/claudecode-leaks)）的独特价值。

**核心发现：**
- **泄露规模**：~1,906 个文件，512,000+ 行 TypeScript 代码
- **GitHub 响应**：多个研究仓库迅速出现，获得数千星标
- **项目类型**：源码归档、技术分析、逆向工程、工具开发
- **独特定位**：我们的项目提供系统化的双语研究指南

---

## 事件背景

### 泄露机制

**披露时间**：2026年3月31日

**发现者**：[Chaofan Shou (@Fried_rice)](https://x.com/Fried_rice)

**泄露原因**：Anthropic 在发布的 npm 包 `@anthropic-ai/claude-code` v2.1.88 中意外包含了 59.8MB 的 source map 文件（`cli.js.map`），该文件引用了托管在 R2 存储桶中的完整 TypeScript 源代码。

**影响范围**：
- ✅ 完整的工具系统实现（43 个工具）
- ✅ 查询引擎核心逻辑
- ✅ 权限系统架构
- ✅ IDE 桥接系统
- ✅ MCP 和 LSP 集成代码
- ❌ 未暴露：API 密钥、用户数据、模型权重

### 社区反应

泄露事件在技术社区迅速传播：
- **Reddit**：多个深度讨论帖
- **Twitter/X**：安全研究者广泛转发
- **GitHub**：仓库被 fork 1,900+ 次
- **技术媒体**：Ars Technica, The Register, Dev.to 等报道

---

## GitHub 研究项目全景

### 📊 项目分类统计

我们识别了 8+ 个主要的 GitHub 仓库，按类型分类如下：

| 类型 | 数量 | 代表项目 |
|------|------|---------|
| 源代码归档 | 4 个 | leeyeel, AprilNEA, hangman, ringmast4r |
| 技术分析 | 2 个 | Kuberwastaken, ThreeFish-AI |
| 工具开发 | 2 个 | instructkr (Python port), 提取脚本 |
| 系统化指南 | 1 个 | **dz3ai/claudecode-leaks (我们的项目)** |

### 🔍 详细项目分析

#### 1. 源代码归档类项目

##### **[leeyeel/claude-code-sourcemap](https://github.com/leeyeel/claude-code-sourcemap)**

- **⭐ Stars**: 1,100+
- **📦 内容**: 完整的原始源代码提取
- **🎯 重点**: 直接镜像泄露的源代码
- **📝 特点**:
  - 保留原始目录结构
  - 包含 ~1,900 个文件
  - 可直接浏览和搜索

##### **[AprilNEA/claude-code-source](https://github.com/AprilNEA/claude-code-source)**

- **📦 内容**: 从 source map 提取的源码
- **🎯 重点**: 源代码归档
- **📝 特点**: 与 leeyeel 类似的归档项目

##### **[hangsman/claude-code-source](https://github.com/hangsman/claude-code-source)**

- **📦 内容**: Fork 的源代码仓库
- **🎯 重点**: 提供访问镜像
- **📝 描述**: "Claude Code is an agentic coding tool that lives in your terminal"

##### **[ringmast4r/Cshaoguang-claude-code-sourcemap](https://github.com/ringmast4r/Cshaoguang-claude-code-sourcemap)**

- **⚠️ 声明**: 非官方，重构版本
- **📦 来源**: 从 npm 包和 source map 分析重构
- **🎓 用途**: 研究目的

#### 2. 技术分析类项目

##### **[Kuberwastaken/claude-code](https://github.com/Kuberwastaken/claude-code)** ⭐

- **🎯 重点**: 技术分解 + Rust 实现
- **📝 描述**: "Claude Code's Entire Source Code Got Leaked via a Sourcemap in npm, Let's Talk About It. Technical Breakdown."
- **💡 特色**:
  - 泄露事件的技术分析
  - Claude Code 的 Rust 重新实现
  - 工作原理深入讲解
  - 架构设计解读

##### **[ThreeFish-AI/analysis_claude_code](https://github.com/ThreeFish-AI/analysis_claude_code)** ⭐

- **🔬 重点**: 逆向工程研究
- **📊 内容**:
  - 静态代码分析
  - LLM 辅助分析
  - 交叉验证研究
  - 深度技术挖掘
- **🎓 价值**: 研究方法论展示

#### 3. 工具开发类项目

##### **[instructkr/claude-code](https://github.com/instructkr/claude-code)**

- **🐍 语言**: Python 移植
- **📝 描述**: Python porting workspace for Claude Code
- **⏰ 时间**: 承认基于 2026年3月31日源代码暴露
- **🎯 目标**: 代码语言移植研究

##### **GitHub Gist: sorrycc/extract-claude-code**

- **📜 类型**: 提取脚本
- **📄 文件**: `extract-claude-code.mjs`
- **💡 功能**: 自动化提取流程
  - 从 npm 下载包
  - 解析 source map
  - 提取 TypeScript 源代码

---

## 🌟 我们项目的独特价值

### [dz3ai/claudecode-leaks](https://github.com/dz3ai/claudecode-leaks)

在众多研究项目中，我们的项目提供了**独特且系统化的研究方法**：

#### 核心特色

##### 1. 📚 双语完整指南

**唯一提供系统化中英文双语指南的项目**

- ✅ **中文指南**：28,000+ 字
- ✅ **English Guide**: 18,800+ words
- ✅ 完全对等的内容结构
- ✅ 术语翻译准确一致

##### 2. 🎯 渐进式学习路径

**三条精心设计的学习路径**

| 路径 | 时间 | 目标受众 | 预期收获 |
|------|------|---------|---------|
| 🌱 初学者路径 | 4-6 小时 | 安全研究新手 | 理解核心概念和基本流程 |
| 🚀 进阶路径 | 8-12 小时 | 开发者、架构师 | 深入理解架构和实现 |
| 🔬 专家路径 | 16-20 小时 | 安全专家、研究者 | 全面掌握，提炼模式 |

##### 3. 🔬 深度架构分析

**5 大核心系统完整解析**

- ✅ **3.1 工具系统**（Tool System）
  - 6 个子章节
  - 接口定义详解
  - 权限模型实现
  - 核心工具案例

- ✅ **3.2 查询引擎**（Query Engine）
  - 8 个子章节
  - 核心架构（1,295 行代码分析）
  - 查询循环流程
  - 流式响应处理
  - 成本追踪与预算控制

- ✅ **3.3 命令系统**（Command System）
  - 5 个子章节
  - 110 个命令实现
  - PromptCommand vs BuiltInCommand
  - 命令注册表

- ✅ **3.4 权限系统**（Permission System）
  - 5 个子章节
  - 5 层安全检查
  - 规则匹配引擎
  - 沙箱机制

- ✅ **3.5 桥接系统**（Bridge System）
  - 5 个子章节
  - IDE 集成架构
  - JWT 认证
  - 消息协议

**统计数据：**
- 📊 基于 ~8,000 行源代码分析
- 🎨 10 个详细流程图
- 💻 50+ 真实代码示例
- 🏗️ 28 种设计模式提炼

##### 4. 🛡️ 供应链安全重点

**不仅分析"是什么"，更关注"为什么"和"如何避免"**

- ✅ Source map 风险详解
- ✅ 构建配置最佳实践
- ✅ CI/CD 安全检查点
- ✅ 包发布验证流程
- ✅ 实际代码示例和检查清单

##### 5. 📖 实战导向

**4 个完整的代码追踪案例**（计划中）

- ⏳ 案例 1：从用户输入到工具执行
- ⏳ 案例 2：权限检查流程
- ⏳ 案例 3：流式响应处理
- ⏳ 案例 4：MCP 服务器连接

##### 6. 📊 持续更新

**进度透明，持续完善**

- ✅ 进度跟踪文档
- ✅ 已完成 42%（第一至三部分）
- ✅ 明确的里程碑
- ✅ 社区贡献欢迎

### 项目对比表

| 特性 | 源码归档 | 技术分析 | 工具开发 | **我们的项目** |
|------|---------|---------|---------|------------|
| 完整源码访问 | ✅ | ✅ | ❌ | ✅ |
| 技术分析 | ❌ | ✅ | ❌ | ✅ |
| 双语指南 | ❌ | ❌ | ❌ | ✅ |
| 学习路径 | ❌ | ❌ | ❌ | ✅ |
| 代码案例 | ❌ | ⚠️ 少 | ❌ | ✅ |
| 设计模式总结 | ❌ | ⚠️ 少 | ❌ | ✅ |
| 供应链安全 | ⚠️ 部分 | ⚠️ 部分 | ❌ | ✅ 重点 |
| 进度跟踪 | ❌ | ❌ | ❌ | ✅ |
| 持续更新 | ❌ | ❌ | ⚠️ 部分 | ✅ |

---

## 🎓 各项目适用场景

### 如果您是...

##### 🔰 安全研究新手
**推荐路径：**
1. 先读我们的**第一部分**：了解事件背景
2. 跟随我们的**初学者路径**：建立整体认知
3. 参考 **leeyeel/claude-code-sourcemap**：浏览实际代码
4. 阅读 **Kuberwastaken** 的技术分析

##### 💻 开发者
**推荐路径：**
1. 我们的**进阶路径**：深入理解架构
2. **ThreeFish-AI** 的逆向工程研究
3. **Kuberwastaken** 的 Rust 实现
4. **instructkr** 的 Python 移植

##### 🎓 学术研究者
**推荐路径：**
1. 我们的**专家路径**：全面掌握系统
2. **ThreeFish-AI** 的研究方法论
3. 我们的供应链安全章节
4. 撰写论文时引用我们的 BibTeX 格式

##### 🔒 企业安全团队
**推荐路径：**
1. 我们的**第五部分**（供应链安全 Lessons）
2. 检查清单和最佳实践
3. 评估自身供应链安全
4. 建立代码审查机制

---

## 📈 项目生态影响

### 对 AI Agent 生态的影响

这次泄露事件和相关研究项目对 AI Agent 生态系统产生了深远影响：

#### 1. 🔓 透明度提升

- ✅ 开发了闭源工具的实现细节
- ✅ 揭示了产业级的架构模式
- ✅ 促进了最佳实践的共享

#### 2. 🛡️ 安全意识增强

- ✅ Source map 风险受到广泛关注
- ✅ CI/CD 安全检查变得重要
- ✅ 供应链安全成为竞争要素

#### 3. 🔄 创新加速

- ✅ 多个语言移植项目出现
- ✅ 架构模式被学习和改进
- ✅ 新工具基于泄露代码开发

#### 4. ⚖️ 知识产权争议

- ⚠️ 法律边界需要明确
- ⚠️ 商业化使用受到限制
- ⚠️ 需要尊重原始开发者权益

---

## 🔮 未来展望

### 研究趋势

基于当前项目生态，我们预测以下趋势：

#### 1. 深度技术分析持续

- 更多架构设计模式提炼
- 性能优化研究
- 安全机制改进建议

#### 2. 工具和框架发展

- 多语言实现增加
- 开源替代项目启动
- 插件生态扩展

#### 3. 标准化和规范

- 供应链安全标准
- Source map 管理规范
- CI/CD 检查清单

#### 4. 学术研究产出

- 论文引用增加
- 案例研究发表
- 会议演讲分享

### 我们的后续计划

**第四至七部分开发中：**

- 📝 第四部分：关键技术专题（React+Ink, Bun, MCP）
- 📝 第五部分：供应链安全 Lessons
- 📝 第六部分：代码阅读实战
- 📝 第七部分：研究资源索引

**预计完成时间：** 2026年4月2日

**预计总字数：** 中文 ~40,000 字 / 英文 ~27,000 词

---

## 🤝 社区贡献

### 如何参与

我们欢迎社区贡献：

1. **改进指南内容**
   - 修正错误
   - 补充案例
   - 翻译优化

2. **创建资源**
   - 架构图和流程图
   - 代码示例
   - 分析工具

3. **分享反馈**
   - GitHub Issues
   - Pull Requests
   - 讨论区

### 相关资源

- **GitHub**: https://github.com/dz3ai/claudecode-leaks
- **研究指南**: [docs/guide/](https://github.com/dz3ai/claudecode-leaks/tree/main/docs/guide)
- **进度跟踪**: [PROGRESS.md](https://github.com/dz3ai/claudecode-leaks/blob/main/docs/guide/PROGRESS.md)

---

## 结论

Claude Code 源代码泄露事件是 2026 年 AI Agent 生态系统的重要事件。GitHub 上涌现的多个研究项目展示了安全社区的快速响应能力。

**我们的项目（dz3ai/claudecode-leaks）**在众多项目中独树一帜：

- 📚 唯一提供**系统化双语指南**
- 🎯 设计**三条渐进学习路径**
- 🔬 完成**5 大核心系统深度分析**
- 🛡️ 聚焦**供应链安全最佳实践**
- 📊 提供**进度跟踪和持续更新**

我们希望这个项目能够：
- 帮助研究者理解泄露的代码
- 促进供应链安全改进
- 为 AI Agent 生态提供学习资源
- 推动负责任的安全研究实践

**免责声明**：本项目仅用于教育和安全研究目的。原始代码版权归 Anthropic 所有。请遵守研究伦理，不将代码用于恶意目的。

---

## 相关链接

### GitHub 仓库
- [dz3ai/claudecode-leaks](https://github.com/dz3ai/claudecode-leaks) - 我们的项目
- [leeyeel/claude-code-sourcemap](https://github.com/leeyeel/claude-code-sourcemap) - 源码归档
- [Kuberwastaken/claude-code](https://github.com/Kuberwastaken/claude-code) - 技术分析 + Rust
- [ThreeFish-AI/analysis_claude_code](https://github.com/ThreeFish-AI/analysis_claude_code) - 逆向工程
- [instructkr/claude-code](https://github.com/instructkr/claude-code) - Python 移植

### 参考资料
- [Claude Code 官方文档](https://docs.anthropic.com)
- [MCP 协议](https://modelcontextprotocol.io)
- [SLSA 供应链安全框架](https://slsa.dev)

---

**作者**: Danny Zeng
**日期**: 2026-04-01
**项目**: allclaws AI Agent 生态系统跟踪
**仓库**: https://github.com/dz3ai/allclaws

---

<p align="center">
  <sub>🔍 持续跟踪 AI Agent 生态系统发展</sub><br>
  <sub>📚 深入分析技术趋势和架构演进</sub>
</p>
