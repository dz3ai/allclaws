# Personal Agent Test Framework API Reference

## Agent Configuration API

### Agent JSON Schema

```json
{
  "type": "object",
  "required": ["name", "skills", "security"],
  "properties": {
    "name": {
      "type": "string",
      "description": "Unique agent identifier"
    },
    "version": {
      "type": "string",
      "description": "Agent version"
    },
    "skills": {
      "type": "object",
      "properties": {
        "required": {
          "type": "array",
          "items": {"type": "string"},
          "description": "Skills the agent must have"
        },
        "optional": {
          "type": "array",
          "items": {"type": "string"},
          "description": "Optional skills"
        }
      }
    },
    "security": {
      "type": "object",
      "properties": {
        "rules": {
          "type": "array",
          "items": {"type": "string"},
          "description": "Security rules to enforce"
        },
        "privileges": {
          "type": "array",
          "items": {"type": "string"},
          "description": "Approved system privileges"
        }
      }
    },
    "credentials": {
      "type": "object",
      "properties": {
        "encrypted": {"type": "boolean"},
        "providers": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "name": {"type": "string"},
              "type": {"type": "string"},
              "scopes": {"type": "array", "items": {"type": "string"}}
            }
          }
        }
      }
    },
    "benchmarks": {
      "type": "object",
      "properties": {
        "enabled": {"type": "array", "items": {"type": "string"}},
        "custom": {"type": "array", "items": {"type": "string"}}
      }
    }
  }
}
```

## Benchmark Task API

### Task Definition Schema

```json
{
  "type": "object",
  "required": ["id", "name", "description", "input", "metrics"],
  "properties": {
    "id": {"type": "string"},
    "name": {"type": "string"},
    "description": {"type": "string"},
    "input": {"type": "object"},
    "metrics": {
      "type": "object",
      "patternProperties": {
        ".*": {"type": "string"}
      }
    },
    "difficulty": {"enum": ["easy", "medium", "hard"]}
  }
}
```

## Security API

### Privilege Levels

- `minimal`: Basic read-only access
- `standard`: Standard personal assistant access
- `advanced`: Comprehensive management access
- `custom`: User-defined privileges

### Security Rules

Rules are enforced at runtime and include:
- Network access controls
- Filesystem permissions
- Command execution limits
- Communication encryption requirements

## Platform Integration API

### Supported Platforms

- **Zeroclaw**: Rust-based runtime
  - Command: `zeroclaw benchmark <task> --config <config> --output <output>`
- **Openclaw**: TypeScript CLI
  - Command: `pnpm openclaw benchmark <task> --config <config> --output <output>`
- **NanoClaw**: Node.js assistant
  - Command: `npm run benchmark <task> --config <config> --output <output>`

### Custom Platform Integration

To add a new platform, implement the benchmark runner interface:

```typescript
interface BenchmarkRunner {
  run(task: string, config: AgentConfig): Promise<BenchmarkResult>;
  validate(config: AgentConfig): boolean;
}
```

## Credential Management API

### Encryption

Credentials are encrypted using AES-256 with a master key stored in `credentials/.master_key`.

### Provider Types

- `oauth2`: OAuth 2.0 flow
- `api_key`: Static API key
- `basic_auth`: Username/password
- `certificate`: Client certificate

## Result Format

Benchmark results are stored in JSON format:

```json
{
  "task_id": "email_sorting",
  "agent": "PersonalAssistant",
  "platform": "zeroclaw",
  "timestamp": "2026-02-23T10:00:00Z",
  "metrics": {
    "accuracy": 0.95,
    "speed": 120.5,
    "security": true
  },
  "duration_ms": 15000,
  "status": "completed"
}
```