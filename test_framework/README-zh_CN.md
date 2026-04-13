# AllClaws 测试框架

一个涵盖 13 个 AI Agent 平台的综合测试和基准测试框架，支持多种编程语言（Rust、Go、Python、TypeScript、Verilog）。

## 概述

该框架提供：
- **沙盒化测试**：通过 Docker/Podman 容器进行隔离的平台测试
- **静态分析**：项目健康检查（LICENSE、README、CI、依赖）
- **基准测试**：代码库指标（代码行数、依赖、测试数量）
- **运行时测试**：容器内实际执行测试
- **DeepEval 集成**：基于 LLM 的 Agent 能力评估

## 支持的平台（13个）

| 平台 | 语言 | 容器镜像 |
|------|------|---------|
| openclaw | TypeScript | node:22-alpine |
| nanoclaw | TypeScript | node:22-alpine |
| quantumclaw | TypeScript | node:22-alpine |
| zeroclaw | Rust | rust:alpine |
| ironclaw | Rust | rust:alpine |
| goclaw | Go | golang:1.23-alpine |
| maxclaw | Go | golang:1.23-alpine |
| hiclaw | Go | golang:1.23-alpine |
| clawteam | Python | python:3.11-slim |
| nanobot | Python | python:3.11-slim |
| claw-ai-lab | Python | python:3.11-slim |
| hermes-agent | Python | python:3.11-slim |
| rtl-claw | Verilog | localhost/openclaw:local |

## 目录结构

```
test_framework/
├── README.md                       # 本文件
├── README-zh_CN.md                 # 中文版
├── docker-compose.yml              # 沙盒环境定义
├── scripts/
│   ├── run_sandboxed_tests.sh      # 主编排脚本
│   ├── run_sandbox_runtime_tests.sh # 运行时测试
│   ├── run_tests.sh                # 静态分析
│   ├── run_benchmarks.sh           # 基准指标
│   ├── setup.sh                    # 框架设置
│   ├── setup_platforms.sh          # 子模块初始化
│   ├── run_benchmark.sh            # 遗留基准运行器
│   └── validate_agent.sh           # Agent 验证
├── results/                        # 测试结果（带时间戳）
│   └── latest/                     # 指向最新结果的符号链接
├── benchmark_results/              # 基准指标
│   └── latest/                     # 指向最新基准的符号链接
├── evals/                          # DeepEval 评估
├── docs/
│   ├── api.md                      # API 参考
│   ├── examples.md                 # 使用示例
│   ├── sandboxed-testing-guide.md  # 沙盒测试指南
│   ├── platform_compatibility.md   # 平台兼容性
│   └── FAQ.md                      # 常见问题
└── config.json                     # 平台配置
```

## 快速开始

### 1. 设置

```bash
cd test_framework

# 初始化子模块（如果尚未完成）
bash scripts/setup_platforms.sh

# 安装依赖
sudo apt install jq docker-compose  # 或 podman-compose
```

### 2. 运行所有测试

```bash
# 测试所有 13 个平台
bash scripts/run_sandboxed_tests.sh

# 仅测试指定平台
bash scripts/run_sandboxed_tests.sh openclaw zeroclaw goclaw
```

### 3. 查看结果

```bash
# 测试结果
cat results/latest/results.md

# 基准指标
cat benchmark_results/latest/benchmark_results.md

# 沙盒运行时发现
cat results/latest/sandbox_findings.md

# 或通过 Web 服务器（如果正在运行）
http://localhost:8080
```

## 测试类型

### 1. 静态分析

不运行代码检查项目健康状况：
- 源文件存在（按语言计数）
- 锁定文件（package-lock.json、Cargo.lock、go.sum）
- CI/CD 配置（.github/workflows）
- 文档（README、LICENSE、CHANGELOG、CONTRIBUTING）
- Docker 配置

### 2. 基准测试

测量代码库规模：
- 代码行数（按语言）
- 依赖数量
- 测试文件数量
- 仓库大小

### 3. 沙盒运行时测试

在容器中运行应用程序并检测：
- 版本不匹配（Rust edition2024、Go 版本）
- 构建失败（cargo check、go build）
- 缺失依赖
- 配置问题

## 先决条件

- **Docker** 或 **Podman**：容器运行时
- **docker-compose** 或 **podman-compose**：多容器编排
- **jq**：JSON 处理器

```bash
# Ubuntu/Debian
sudo apt install jq docker.io docker-compose

# macOS
brew install jq docker docker-compose

# 使用 Podman
sudo apt install jq podman podman-compose
```

## 容器运行时

框架自动检测您的容器运行时：
- 优先使用 `podman`（如果可用）
- 否则回退到 `docker`
- 使用相应的 compose 命令（`podman-compose` 或 `docker-compose`）

## 配置

### Docker Compose 服务

| 服务 | 描述 | 挂载卷 |
|------|------|--------|
| `*-sandbox` | 平台测试容器 | 源码（只读）、构建输出（可写） |
| `deepeval-runner` | 评估运行器 | evals/、results/、Docker 套接字 |
| `results-collector` | Nginx 结果服务器 | results/（端口 8080） |

### 环境变量

```bash
# DeepEval（可选）
DEEPEVAL_API_KEY=your_key

# 用于评估的 LLM API
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-...
```

## 独立测试脚本

```bash
# 仅静态分析
bash scripts/run_tests.sh

# 仅基准测试
bash scripts/run_benchmarks.sh

# 仅运行时测试
bash scripts/run_sandbox_runtime_tests.sh [平台...]

# 单个平台测试
bash scripts/run_tests.sh openclaw
bash scripts/run_benchmarks.sh zeroclaw
```

## 清理

```bash
# 停止所有容器
docker-compose down

# 删除卷
docker-compose down -v

# 清理旧结果（保留最新 5 个）
ls -t results/ | tail -n +6 | xargs -I {} rm -rf results/{}
```

## GitHub Actions

该框架包含 CI/CD 工作流：
- **推送到 main**：完整测试套件
- **Pull requests**：静态分析 + 基准测试
- **每周计划**：完整沙盒测试
- **手动触发**：按需测试

```bash
# 手动触发
gh workflow run agent-tests.yml
```

## 故障排除

### 容器无法启动

```bash
# 查看日志
docker-compose logs [服务名]

# 验证卷路径
docker-compose config
```

### 子模块未找到

```bash
git submodule update --init --recursive
```

### 权限被拒绝

```bash
# 将用户添加到 docker 组
sudo usermod -aG docker $USER
newgrp docker

# 或使用 sudo
sudo docker-compose up -d
```

## 文档

- [沙盒测试指南](docs/sandboxed-testing-guide.md) - 详细的沙盒测试说明
- [API 参考](docs/api.md) - 框架 API
- [示例](docs/examples.md) - 使用示例
- [平台兼容性](docs/platform_compatibility.md) - 平台特定说明
- [FAQ](docs/FAQ.md) - 常见问题

## 许可证

MIT
