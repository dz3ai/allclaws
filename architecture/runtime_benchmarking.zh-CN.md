# 运行时性能基准测试：方法论与结果

**[English](runtime_benchmarking.md)** | 中文

> 跨 AI 代理平台的可复现运行时性能测量框架。涵盖源码复杂度指标、构建计时、导入解析速度、容器镜像估算，以及需要 LLM API 访问权限的指标的文档化方法论。2026 年 5 月。

---

## 执行摘要

AI 代理平台的运行时性能基准测试分为两个层级：

1. **第一层（自动化）：** 无需 LLM 访问即可测量的指标——源码复杂度、依赖数量、构建/检查计时、导入解析速度、容器镜像估算。
2. **第二层（手动方法论）：** 需要 LLM API 访问的指标——冷启动到首次响应、内存使用、响应延迟（p50/p95/p99）、token 效率。

本文档提供 2026 年 5 月 7 日的第一层结果，并记录第二层协议供未来测量使用。

---

## 第一部分：第一层结果

### Rust 平台

| 平台 | 源文件 | 依赖 | Cargo Check 时间 | Dockerfile |
|------|--------|------|-----------------|------------|
| **IronClaw** | 838 .rs | 56 cargo | 959.6s（~16 分钟） | 是 |
| **ZeroClaw** | 710 .rs | 60 cargo | 失败 | 否 |

### Go 平台（Go 工具链不可用）

| 平台 | 源文件 | 依赖 | Go 版本 | Dockerfile |
|------|--------|------|---------|------------|
| **GoClaw** | 1,721 .go | 203 go mod | 1.26.0 | 是 |
| **Maxclaw** | 129 .go | 33 go mod | 1.24.0 | 否 |
| **HiClaw** | 151 .go | N/A | N/A | 是 |

### TypeScript 平台

| 平台 | 源文件 | 依赖 | Dockerfile |
|------|--------|------|------------|
| **OpenClaw** | 14,505 .ts | 82 npm | 是 |
| **NanoClaw** | 225 .ts | 19 npm | 是 |
| **QuantumClaw** | 0 .ts | 12 npm | 否 |

### Python 平台

| 平台 | 源文件 | 依赖 | 导入时间 | Python CI |
|------|--------|------|---------|-----------|
| **ClawTeam** | 92 .py | 19 pip | 204ms | 是 |
| **Nanobot** | 263 .py | 80 pip | 21ms | 是 |
| **Hermes-Agent** | 1,441 .py | 63 pip | 21ms | 是 |

### 跨语言平均值

| 语言 | 平均源文件数 | 平均依赖数 | Dockerfile 比例 |
|------|------------|-----------|-----------------|
| Rust | 774 | 58 | 50% |
| Go | 667 | 118 | 67% |
| TypeScript | 4,910 | 38 | 67% |
| Python | 449 | 54 | 75% |

### 源码复杂度 Top 5

| 排名 | 平台 | 源文件数 | 语言 |
|------|------|---------|------|
| 1 | OpenClaw | 14,505 | TypeScript |
| 2 | GoClaw | 1,721 | Go |
| 3 | Hermes-Agent | 1,441 | Python |
| 4 | IronClaw | 838 | Rust |
| 5 | ZeroClaw | 710 | Rust |

---

## 第二部分：第二层方法论

对于需要实时 LLM 访问的指标：

**冷启动时间：** `time (agent-cli --version)` 用于二进制文件；`time (agent-cli --prompt "ping" | grep -m1 response)` 用于首次响应。目标平台：GoClaw、IronClaw、ZeroClaw、Maxclaw、OpenClaw、Nanobot。

**内存使用：** 通过 `ps -o rss=` 在空闲（启动后 5 秒）和负载下（工具执行期间）测量 RSS。对比 Rust vs Go vs Node.js vs Python 的内存基线。

**响应延迟：** 使用固定提示（"2+2 等于多少？"）进行 100 次迭代，含预热。测量首次 token 时间。从分布中计算 p50/p95/p99。

**Token 效率：** 跨平台 5 个标准任务，使用相同的 LLM 模型。测量输入 token（提示 + 上下文 + 工具 schema）和输出 token。计算效率 = 输出/输入。

---

## 第三部分：建议

- **源文件数量代表复杂度，而非质量。** OpenClaw 的 14,505 个文件提供 37+ 个频道；NanoClaw 的 225 个文件提供 WhatsApp 到 Claude 的桥接。
- **依赖数量与攻击面相关。** GoClaw（203 个依赖）和 Nanobot（80 个依赖）应优先考虑供应链审计。
- **Dockerfile 覆盖率很高（67%）。** 容器化现已成为可复现部署的基本要求。
- **冷启动对 CLI 代理重要，对守护进程不重要。** 对于按任务调用的场景，选择 Rust 或 Go 二进制文件；对于长时间运行的服务，Python/Node.js 的启动时间已摊销。

---

## 参见

- [统一平台比较](platform_comparison.zh-CN.md) — 完整的架构比较
- [测试框架](../test_framework/) — 静态分析结果
- [路线图：2026 年 Q4](../docs/ROADMAP.zh-CN.md) — 性能基准测试目标

---

*最后更新：2026 年 5 月 7 日*
*可用工具链：cargo、node、python3、docker（缺少 Go）*
*所属：AllClaws 个人 AI 代理生态系统研究*
