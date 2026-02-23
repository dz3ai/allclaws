# 个人代理测试框架

此框架允许用户跨不同平台（Zeroclaw、Openclaw、NanoClaw 等）定义、配置和基准测试个人 AI 代理。它强调安全性、技能验证和性能测试。

## 概述

该框架提供：
- **代理定义**：指定所需技能、安全规则、系统权限和凭据
- **安全验证**：确保代理在批准的边界内运行
- **基准套件**：用于性能比较的常见个人任务
- **多平台支持**：在 Zeroclaw (Rust)、Openclaw (TypeScript)、NanoClaw (Node.js) 或自定义代理上运行基准测试

## 目录结构

```
test_framework/
├── README.md              # 此文件
├── agents/                # 代理定义
│   ├── example_agent.json # 示例代理配置
│   └── templates/         # 配置模板
├── benchmarks/            # 基准任务
│   ├── common_tasks.json  # 标准个人任务
│   ├── custom_tasks/      # 用户定义任务
│   └── results/           # 基准测试结果
├── security/              # 安全配置
│   ├── rules.json         # 安全规则
│   └── privileges.json    # 系统权限
├── credentials/           # 安全凭据存储（加密）
│   └── .encrypted/        # 加密凭据文件
├── scripts/               # 执行脚本
│   ├── run_benchmark.sh   # 主要基准测试运行器
│   ├── validate_agent.sh  # 代理验证
│   └── setup.sh           # 框架设置
├── tmp/                   # 临时文件目录
└── docs/                  # 文档
    ├── api.md             # API 参考
    └── examples.md        # 使用示例
```

## 快速开始

1. **设置**：运行 `./scripts/setup.sh` 初始化框架
2. **定义代理**：在 `agents/` 中创建代理配置
3. **验证**：运行 `./scripts/validate_agent.sh <agent_config>`
4. **基准测试**：运行 `./scripts/run_benchmark.sh <agent_config> <platform>`

## 先决条件

- **jq**：用于配置验证的 JSON 处理器
  - Ubuntu/Debian: `sudo apt install jq`
  - macOS: `brew install jq`
  - 其他系统：从 [stedolan.github.io/jq](https://stedolan.github.io/jq/) 下载

## 代理配置

代理以 JSON 格式定义，具有以下结构：

```json
{
  "name": "MyPersonalAgent",
  "version": "1.0.0",
  "skills": {
    "required": ["task_management", "email_processing", "calendar_integration"],
    "optional": ["web_scraping", "data_analysis"]
  },
  "security": {
    "rules": ["no_external_network", "read_only_filesystem"],
    "privileges": ["read_home_dir", "execute_safe_commands"]
  },
  "credentials": {
    "encrypted": true,
    "providers": ["gmail_api", "calendar_api"]
  },
  "benchmarks": {
    "enabled": ["email_sorting", "schedule_optimization"],
    "custom": []
  }
}
```

## 安全特性

- **权限级别**：定义代理具有的系统访问权限
- **凭据加密**：使用 AES-256 的安全存储
- **规则执行**：运行时验证安全边界
- **审计日志**：跟踪所有代理操作

## 基准套件

常见个人任务包括：
- 电子邮件处理和优先级排序
- 日历安排和冲突解决
- 任务管理和提醒
- 文档摘要
- 网络研究（有安全限制）
- 数据组织

## 支持的平台

- **Zeroclaw**：基于 Rust 的高性能运行时
- **Openclaw**：具有广泛渠道的 TypeScript CLI
- **NanoClaw**：Node.js WhatsApp 助手
- **自定义**：任何具有 HTTP API 的代理

## API 参考

有关详细的 API 文档，请参见 `docs/api.md`。

## 示例

有关使用示例和示例配置，请参见 `docs/examples.md`。