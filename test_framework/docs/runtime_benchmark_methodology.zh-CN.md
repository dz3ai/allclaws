# 运行时基准测试方法论

本文档说明 AllClaws 代理运行时基准测试系统的工作原理、每项指标的含义以及如何解读结果。

## 概述

代理运行时基准测试引擎（`scripts/run_agent_runtime_benchmarks.sh`）测量每个 AllClaws 平台的**运行时性能特征**。与静态分析基准测试（`run_benchmarks.sh`）测量代码规模和结构不同，这些基准测试捕捉平台实际调用时的性能表现。

## 运行基准测试

```bash
cd test_framework/
./scripts/run_agent_runtime_benchmarks.sh
```

结果以 JSON 和 Markdown 格式写入 `benchmark_results/<timestamp>-agent-runtime/` 目录。

## 指标说明

### 冷启动时间 (`cold_start_time_ms`)

**测量内容：** 从调用平台 CLI 入口点到进程完成初始启动的时间。

**测量方式：**
- **Rust 平台**（`ironclaw`、`zeroclaw`）：`time <binary> --help` — 测量进程创建 + 参数解析时间。
- **Go 平台**（`goclaw`、`maxclaw`、`hiclaw`）：如果存在预编译二进制，采用同样方式。
- **TypeScript 平台**（`openclaw`、`nanoclaw`、`quantumclaw`）：`node -e "require('src/index.ts')"` — 测量 Node.js 启动 + 模块解析时间（非完整运行时初始化，因为 TypeScript 需要转译）。
- **Python 平台**（`clawteam`、`nanobot`、`hermes-agent`、`claw-ai-lab`）：`python3 -c "import <module>"` — 测量解释器启动 + 模块导入时间。

**局限性：**
- 不包含 LLM API 调用时间（不发起网络请求）。
- TypeScript 平台仅测量 Node.js 解析时间，而非完整的编译后运行时。
- Python 平台仅测量导入时间，而非完整的代理初始化（可能包括加载配置、连接数据库等）。

### 内存使用 (`memory_idle_mb`、`memory_active_mb`)

**测量内容：**
- **空闲态：** 最小化进程调用的峰值 RSS（常驻内存集大小）。
- **活跃态：** 加载常用标准库模块（json、os、re、pathlib 等）后的峰值 RSS。

**测量方式：** 使用 `/usr/bin/time -v` 从内核获取"Maximum resident set size"。如果 `/usr/bin/time -v` 不可用（仅限 Linux/GNU），则回退到 `ps -o rss` 轮询。

**局限性：**
- 空闲内存反映的是裸运行时，而非加载所有依赖的完整代理。
- 活跃内存仅加载标准库模块，不加载第三方包（这些包通常在真实场景中占据大部分 RSS）。
- 测量值为单次采样，非多次运行的平均值。
- RSS 值包含共享库页面，跨进程可能存在重复计算。

### 响应延迟 (`response_latency_ms`)

**测量内容：** 简单 echo 命令的首次输出时间。这是运行时启动开销的代理指标，而非实际 LLM 响应时间。

**测量方式：**
- **Python：** `time python3 -c "sys.stdout.write('READY\n'); sys.stdout.flush()"`
- **Node.js：** `time node -e "console.log('READY'); process.exit(0)"`

**局限性：**
- 这是一个最小化基准测试，仅测量运行时启动 + stdout 写入时间。
- 真实延迟取决于 LLM 提供商、网络条件、提示词复杂度和上下文长度。
- 未测量 P50/P95/P99 分位数 — 仅单次计时。

### Token 效率 (`token_efficiency_ratio`)

**测量内容：** 生成的输出 token 数除以消耗的输入 token 数（输出/输入比率）。

**测量方式：** 目前未实现。这需要使用标准化提示词进行实际 LLM API 调用，超出了本地基准测试的范围。此指标保留供将来与 eval/test 套件集成。

### 二进制大小 (`binary_size_kb`)

**测量内容：** 编译后的二进制文件或构建输出的大小。

**测量方式：**
- **Rust：** `du -k target/release/<binary>` — release 构建二进制。
- **Go：** `du -k bin/<binary>` 或项目中找到的任何可执行文件。
- **TypeScript：** `du -k dist/` 或 `du -k build/` — 编译后的 JS 输出。
- **Python：** 不直接适用（解释型语言）。改用安装足迹。

### 安装大小 (`install_size_kb`)

**测量内容：** 依赖项/构建产物的总磁盘占用。

**测量方式：**
- **Rust：** `du -k target/` — 完整构建缓存。
- **Go：** `du -k vendor/` — vendored 依赖（如果使用了 vendor）。
- **TypeScript：** `du -k node_modules/` — npm 安装的包。
- **Python：** `du -k .venv/` 或 `du -k venv/` — 虚拟环境。如果不存在 venv，则根据依赖数量估算（平均每个依赖约 2MB）。

### 构建代理时间 (`build_proxy_time_ms`)

**测量内容：** 快速构建检查命令的耗时。用作编译速度的代理指标，因为完整构建对于常规基准测试来说太慢。

**测量方式：**
- **Rust：** `cargo check` — 类型检查，不生成二进制。
- **Go：** `go vet ./...` — 静态分析；如果 vet 失败则回退到 `go build -o /dev/null`。

### 模块下载时间 (`mod_download_time_ms`)

**测量内容：** 下载依赖的时间（使用缓存）。

**测量方式：** Go 平台使用 `go mod download`。其他平台不测量 npm/pip 等效操作，以避免副作用。

## 平台覆盖

| 平台 | 语言 | 冷启动 | 内存 | 二进制大小 | 安装大小 | 构建代理 |
|------|------|--------|------|-----------|---------|---------|
| ironclaw | Rust | 是（需编译） | 是 | 是 | 是 | 是 |
| zeroclaw | Rust | 是（需编译） | 是 | 是 | 是 | 是 |
| openclaw | TypeScript | 是（解析） | 是 | dist/ | node_modules/ | 否 |
| nanoclaw | TypeScript | 是（解析） | 是 | dist/ | node_modules/ | 否 |
| quantumclaw | TypeScript | 是（解析） | 是 | build/ | node_modules/ | 否 |
| goclaw | Go | 是（需编译） | 是 | 是 | vendor/ | 是 |
| maxclaw | Go | 是（需编译） | 是 | 是 | vendor/ | 是 |
| hiclaw | Go | 是（需编译） | 是 | 是 | vendor/ | 是 |
| clawteam | Python | 是（导入） | 是 | 不适用 | venv/ | 不适用 |
| nanobot | Python | 是（导入） | 是 | 不适用 | venv/ | 不适用 |
| hermes-agent | Python | 是（导入） | 是 | 不适用 | venv/ | 不适用 |
| claw-ai-lab | Python | 是（导入） | 是 | 不适用 | 估算 | 不适用 |
| rtl-claw | Verilog | 跳过 | 跳过 | 跳过 | 跳过 | 跳过 |

## 工具链依赖

| 工具 | 用于 | 回退方案 |
|------|------|---------|
| `jq` | JSON 报告生成 | 仅 Markdown 输出 |
| `python3` | 启动计时、内存测量 | 跳过 Python 指标 |
| `/usr/bin/time -v` | 精确 RSS 测量 | `ps -o rss` 轮询 |
| `cargo` | Rust 构建代理 | 跳过构建时间 |
| `node` | TypeScript 启动计时 | 跳过 TS 冷启动 |
| `go` | Go 构建代理、mod download | 跳过 Go 构建时间 |

脚本设计为**永不失败** — 缺失的工具链会导致带有注释的跳过测量，而非错误。

## 结果解读指南

- **冷启动 < 500ms：** CLI 工具表现优秀。大多数代理 CLI 目标为 < 1s。
- **冷启动 500ms–2s：** 对于复杂代理框架可接受。
- **冷启动 > 2s：** 可能存在繁重的初始化（数据库连接、大型模块加载）。
- **空闲内存 < 50MB：** 非常精简的运行时。
- **空闲内存 50–200MB：** 具有中等依赖的代理框架典型值。
- **空闲内存 > 200MB：** 重量级框架 — 在资源受限环境中可能需要优化。
- **安装大小 < 100MB：** 最小化足迹。
- **安装大小 100–500MB：** 具有众多依赖的框架典型值。
- **安装大小 > 500MB：** 重量级 — 建议评估是否所有依赖都是必要的。

## 局限性

1. **无 LLM API 调用：** 这些基准测试仅测量本地运行时行为。实际代理性能在很大程度上取决于 LLM 提供商、模型和网络延迟。

2. **单次测量：** 每项指标仅测量一次，非多次平均值。由于系统负载、文件系统缓存等原因，不同运行之间的结果可能有所差异。

3. **依赖构建状态：** 二进制大小和冷启动测量需要预构建产物。如果平台未构建，相关指标将被跳过。

4. **环境依赖：** 结果随操作系统、CPU、磁盘速度和系统负载而变化。为了可重复的比较，请在相同机器的类似条件下运行。

5. **导入时间 ≠ 运行时：** Python 和 Node.js 的冷启动测量导入/解析时间，而非完整的代理初始化（可能包括数据库连接、配置加载等）。

6. **内存测量精度：** `/usr/bin/time -v` 报告峰值 RSS，其中包含共享页面。在 Linux 上，RSS 计算的共享库页面可能在进程间共享，导致总内存使用量被高估。
