# Personal Agent Test Framework Examples

## Basic Agent Definition

Create `agents/my_agent.json`:

```json
{
  "name": "MyPersonalAgent",
  "version": "1.0.0",
  "skills": {
    "required": ["email_processing", "task_management"],
    "optional": ["calendar_integration"]
  },
  "security": {
    "rules": ["no_external_network", "read_only_filesystem"],
    "privileges": ["read_home_dir", "access_calendar_api"]
  },
  "credentials": {
    "encrypted": true,
    "providers": [
      {
        "name": "gmail",
        "type": "oauth2",
        "scopes": ["read", "send"]
      }
    ]
  },
  "benchmarks": {
    "enabled": ["email_sorting", "task_prioritization"],
    "custom": []
  }
}
```

## Setup and Validation

```bash
# Setup the framework
./scripts/setup.sh

# Validate agent configuration
./scripts/validate_agent.sh agents/my_agent.json
```

## Running Benchmarks

```bash
# Run benchmarks on Zeroclaw
./scripts/run_benchmark.sh agents/my_agent.json zeroclaw

# Run on Openclaw
./scripts/run_benchmark.sh agents/my_agent.json openclaw

# Run on NanoClaw
./scripts/run_benchmark.sh agents/my_agent.json nanoclaw
```

## Custom Benchmark Task

Create `benchmarks/custom_tasks/my_task.json`:

```json
{
  "id": "custom_productivity",
  "name": "Custom Productivity Analysis",
  "description": "Analyze personal productivity patterns",
  "input": {
    "data_points": 100,
    "time_range": "30_days"
  },
  "metrics": {
    "insights_generated": "count",
    "accuracy": "percentage",
    "usefulness": "rating"
  },
  "difficulty": "medium"
}
```

Then add to agent config:

```json
"benchmarks": {
  "enabled": ["email_sorting"],
  "custom": ["custom_productivity"]
}
```

## Security Configuration

Define custom security rules in `security/rules.json`:

```json
{
  "rules": [
    {
      "id": "custom_network_restriction",
      "name": "Custom Network Restriction",
      "description": "Only allow access to approved domains",
      "severity": "high",
      "enforcement": "runtime_block"
    }
  ]
}
```

## Credential Management

Store encrypted credentials:

```bash
# The framework automatically encrypts credentials
# Master key is generated during setup
# Credentials are stored in credentials/.encrypted/
```

## Advanced Platform Integration

For custom platforms, create a runner script:

```bash
#!/bin/bash
# custom_platform_runner.sh

TASK=$1
CONFIG=$2
OUTPUT=$3

# Your custom benchmark logic here
# ...

echo "{\"result\": \"completed\", \"score\": 95}" > "$OUTPUT"
```

Then modify `run_benchmark.sh` to support your platform.

## Result Analysis

After running benchmarks, check results:

```bash
# View summary
cat benchmarks/results/20260223_100000_zeroclaw/summary.md

# Analyze specific results
jq . benchmarks/results/20260223_100000_zeroclaw/email_sorting.json
```

## Troubleshooting

### Common Issues

1. **Validation fails**: Check JSON syntax and required fields
2. **Platform not found**: Ensure the platform binary is in PATH
3. **Permission denied**: Check file permissions and security settings
4. **Benchmark timeout**: Increase timeout in runner script

### Debug Mode

Enable debug logging:

```bash
export DEBUG=1
./scripts/run_benchmark.sh agents/my_agent.json zeroclaw
```