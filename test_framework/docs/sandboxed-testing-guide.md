# AllClaws 沙盒化测试方案

本文档说明如何使用 Docker Compose + DeepEval + GitHub Actions 进行自动化 Agent 平台测试。

---

## 🏗️ 架构概览

```
┌─────────────────────────────────────────────────────────────┐
│                    GitHub Actions (CI/CD)                    │
│  - 每周日自动运行                                        │
│  - PR 触发增量测试                                      │
│  - 手动触发完整测试                                      │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                  Docker Compose 沙盒环境                      │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            │
│  │ openclaw    │  │ zeroclaw    │  │ ironclaw    │            │
│  │ (Node:22)   │  │ (Rust)      │  │ (Rust)      │            │
│  └─────────────┘  └─────────────┘  └─────────────┘            │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            │
│  │ goclaw      │  │ nanoclaw    │  │ nanobot     │            │
│  │ (Go)        │  │ (Node)      │  │ (Python)    │            │
│  └─────────────┘  └─────────────┘  └─────────────┘            │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            │
│  │ DeepEval    │  │ Results     │  │ Nginx       │            │
│  │ Runner      │  │ Collector   │  │ Server      │            │
│  └─────────────┘  └─────────────┘  └─────────────┘            │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 快速开始

### 1. 本地运行沙盒测试

```bash
cd test_framework

# 启动所有沙盒环境
docker-compose up -d

# 查看运行状态
docker-compose ps

# 运行测试
bash scripts/run_sandboxed_tests.sh

# 清理
docker-compose down
```

### 2. 运行单个平台测试

```bash
# 测试 OpenClaw
docker-compose exec openclaw-sandbox npm test

# 测试 ZeroClaw
docker-compose exec zeroclaw-sandbox cargo test

# 测试 GoClaw
docker-compose exec goclaw-sandbox go test ./...
```

### 3. 运行 DeepEval 评估

```bash
cd test_framework/evals

# 安装依赖
pip install -r requirements.txt

# 设置 API 密钥
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-..."

# 运行评估（需要先启动 Agent）
python agent_eval.py
```

---

## 📊 GitHub Actions 工作流

### 自动触发

| 事件 | 说明 |
|------|------|
| `push to main` | 运行所有测试 |
| `pull_request` | 运行静态分析和基准测试 |
| `每周日 00:00` | 运行完整沙盒测试 |

### 手动触发

```bash
gh workflow run agent-tests.yml
```

---

## 🧪 测试类型

### 1. 静态分析 (Static Analysis)

检查项目健康度：
- ✅ LICENSE, README, CHANGELOG
- ✅ 构建配置 (package.json, Cargo.toml)
- ✅ CI/CD 配置

### 2. 基准测试 (Benchmarks)

测量平台规模：
- 📁 仓库大小
- 📝 代码行数
- 📦 依赖数量
- 🧪 测试文件数量

### 3. DeepEval 评估

评估 Agent 能力：
- 🎯 Faithfulness (忠实度)
- 📌 Relevancy (相关性)
- 📚 Contextual Recall (上下文召回)

---

## 📁 文件结构

```
test_framework/
├── docker-compose.yml          # 沙盒环境定义
├── evals/                       # DeepEval 评估
│   ├── agent_eval.py           # 评估脚本
│   ├── config.yaml             # 配置文件
│   └── requirements.txt        # Python 依赖
├── scripts/
│   └── run_sandboxed_tests.sh  # 测试运行脚本
└── .github/workflows/
    └── agent-tests.yml          # GitHub Actions 配置
```

---

## 🔧 配置说明

### Docker Compose 服务

| 服务 | 镜像 | 端口 | 说明 |
|------|------|------|------|
| `*-sandbox` | 语言原生 | - | 各平台测试沙盒 |
| `deepeval-runner` | Python 3.11 | - | 评估执行器 |
| `results-collector` | Nginx | 8080 | 结果服务器 |

### 环境变量

```bash
# DeepEval 配置
DEEPEVAL_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-...

# OpenAI (用于 GPT-4 评审)
OPENAI_API_KEY=sk-...
```

---

## 📈 结果查看

### 本地测试

```bash
# 查看最新结果
cat test_framework/results/latest/results.md
cat test_framework/benchmark_results/latest/benchmark_results.md

# 或通过 Nginx 服务器
http://localhost:8080
```

### CI/CD 结果

1. 进入 GitHub Actions 页面
2. 选择最近的 `agent-tests` 工作流
3. 下载 Artifacts 查看

---

## 🛠️ 故障排除

### 沙盒无法启动

```bash
# 检查日志
docker-compose logs [service-name]

# 重建
docker-compose down
docker-compose up -d --build
```

### DeepEval API 错误

```bash
# 检查 API 密钥
echo $OPENAI_API_KEY

# 测试连接
curl https://api.openai.com/v1/models
```

### Submodule 未初始化

```bash
git submodule update --init --recursive
```

---

## 📚 相关资源

- [DeepEval 文档](https://docs.confident-ai.com/)
- [Docker Compose 文档](https://docs.docker.com/compose/)
- [GitHub Actions 文档](https://docs.github.com/en/actions)
