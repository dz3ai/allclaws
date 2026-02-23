#!/bin/bash

# Personal Agent Test Framework Setup Script

echo "Setting up Personal Agent Test Framework..."

# Check dependencies
command -v jq >/dev/null 2>&1 || { echo "jq is required but not installed. Please install jq."; exit 1; }
command -v openssl >/dev/null 2>&1 || { echo "openssl is required but not installed. Please install openssl."; exit 1; }

# Create necessary directories
mkdir -p benchmarks/results
mkdir -p credentials/.encrypted
mkdir -p agents/templates
mkdir -p tmp

# Generate encryption key if not exists
if [ ! -f credentials/.master_key ]; then
    echo "Generating master encryption key..."
    openssl rand -hex 32 > credentials/.master_key
    chmod 600 credentials/.master_key
fi

# Set up basic configuration
cat > config.json << EOF
{
  "framework_version": "1.0.0",
  "encryption_enabled": true,
  "supported_platforms": ["zeroclaw", "openclaw", "nanoclaw"],
  "default_privilege_level": "standard",
  "audit_logging": true
}
EOF

echo "Setup complete!"
echo "Next steps:"
echo "1. Define your agent in agents/example_agent.json"
echo "2. Run validate_agent.sh to check configuration"
echo "3. Run run_benchmark.sh to test performance"