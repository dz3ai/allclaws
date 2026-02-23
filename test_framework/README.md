# Personal Agent Test Framework

This framework allows users to define, configure, and benchmark personal AI agents across different platforms (Zeroclaw, Openclaw, NanoClaw, and others). It emphasizes security, skill validation, and performance testing.

## Overview

The framework provides:
- **Agent Definition**: Specify required skills, security rules, system privileges, and credentials
- **Security Validation**: Ensure agents operate within approved boundaries
- **Benchmark Suite**: Common personal tasks for performance comparison
- **Multi-Platform Support**: Run benchmarks on Zeroclaw (Rust), Openclaw (TypeScript), NanoClaw (Node.js), or custom agents

## Directory Structure

```
test_framework/
├── README.md              # This file
├── agents/                # Agent definitions
│   ├── example_agent.json # Sample agent config
│   └── templates/         # Config templates
├── benchmarks/            # Benchmark tasks
│   ├── common_tasks.json  # Standard personal tasks
│   ├── custom_tasks/      # User-defined tasks
│   └── results/           # Benchmark results
├── security/              # Security configurations
│   ├── rules.json         # Security rules
│   └── privileges.json    # System privileges
├── credentials/           # Secure credential storage (encrypted)
│   └── .encrypted/        # Encrypted credential files
├── scripts/               # Execution scripts
│   ├── run_benchmark.sh   # Main benchmark runner
│   ├── validate_agent.sh  # Agent validation
│   └── setup.sh           # Framework setup
├── tmp/                   # Temporary files directory
└── docs/                  # Documentation
    ├── api.md             # API reference
    └── examples.md        # Usage examples
```

## Quick Start

1. **Setup**: Run `./scripts/setup.sh` to initialize the framework
2. **Define Agent**: Create an agent config in `agents/`
3. **Validate**: Run `./scripts/validate_agent.sh <agent_config>`
4. **Benchmark**: Run `./scripts/run_benchmark.sh <agent_config> <platform>`

## Prerequisites

- **jq**: JSON processor for configuration validation
  - Ubuntu/Debian: `sudo apt install jq`
  - macOS: `brew install jq`
  - Other systems: Download from [stedolan.github.io/jq](https://stedolan.github.io/jq/)

## Agent Configuration

Agents are defined in JSON format with the following structure:

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

## Security Features

- **Privilege Levels**: Define what system access the agent has
- **Credential Encryption**: Secure storage using AES-256
- **Rule Enforcement**: Runtime validation of security boundaries
- **Audit Logging**: Track all agent actions

## Benchmark Suite

Common personal tasks include:
- Email processing and prioritization
- Calendar scheduling and conflict resolution
- Task management and reminders
- Document summarization
- Web research (with safety limits)
- Data organization

## Supported Platforms

- **Zeroclaw**: Rust-based, high-performance runtime
- **Openclaw**: TypeScript CLI with extensive channels
- **NanoClaw**: Node.js WhatsApp assistant
- **Custom**: Any agent with HTTP API

## API Reference

See `docs/api.md` for detailed API documentation.

## Examples

See `docs/examples.md` for usage examples and sample configurations.