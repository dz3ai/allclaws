#!/bin/bash

# Benchmark Runner Script

AGENT_CONFIG=$1
PLATFORM=$2

if [ -z "$AGENT_CONFIG" ] || [ -z "$PLATFORM" ]; then
    echo "Usage: $0 <agent_config.json> <platform>"
    echo "Platforms: zeroclaw, openclaw, nanoclaw"
    exit 1
fi

if [ ! -f "$AGENT_CONFIG" ]; then
    echo "Agent config file not found: $AGENT_CONFIG"
    exit 1
fi

# Validate platform
case $PLATFORM in
    zeroclaw|openclaw|nanoclaw)
        ;;
    *)
        echo "Unsupported platform: $PLATFORM"
        echo "Supported: zeroclaw, openclaw, nanoclaw"
        exit 1
        ;;
esac

echo "Running benchmarks for agent: $(jq -r '.name' "$AGENT_CONFIG") on platform: $PLATFORM"

# Get enabled benchmarks
BENCHMARKS=$(jq -r '.benchmarks.enabled | join(" ")' "$AGENT_CONFIG")

if [ -z "$BENCHMARKS" ]; then
    echo "No benchmarks enabled in agent config"
    exit 1
fi

# Create results directory
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
RESULT_DIR="benchmarks/results/${TIMESTAMP}_${PLATFORM}"
mkdir -p "$RESULT_DIR"

echo "Results will be saved to: $RESULT_DIR"

# Run each benchmark
for benchmark in $BENCHMARKS; do
    echo "Running benchmark: $benchmark"

    case $PLATFORM in
        zeroclaw)
            # Assume zeroclaw binary is available
            if command -v zeroclaw >/dev/null 2>&1; then
                zeroclaw benchmark "$benchmark" --config "$AGENT_CONFIG" --output "$RESULT_DIR/${benchmark}.json"
            else
                echo "Zeroclaw binary not found. Please build zeroclaw first."
                exit 1
            fi
            ;;
        openclaw)
            # Assume openclaw is available via pnpm
            if command -v pnpm >/dev/null 2>&1; then
                cd /home/dannyz/local/src/openclaw
                pnpm openclaw benchmark "$benchmark" --config "../../../allclaws/test_framework/$AGENT_CONFIG" --output "../../../allclaws/test_framework/$RESULT_DIR/${benchmark}.json"
                cd - >/dev/null
            else
                echo "pnpm not found. Please install pnpm."
                exit 1
            fi
            ;;
        nanoclaw)
            # Assume nanoclaw is available
            if [ -f "/home/dannyz/local/src/nanoclaw/package.json" ]; then
                cd /home/dannyz/local/src/nanoclaw
                npm run benchmark "$benchmark" --config "../../../allclaws/test_framework/$AGENT_CONFIG" --output "../../../allclaws/test_framework/$RESULT_DIR/${benchmark}.json"
                cd - >/dev/null
            else
                echo "NanoClaw not found."
                exit 1
            fi
            ;;
    esac

    echo "Completed benchmark: $benchmark"
done

echo "All benchmarks completed!"
echo "Results: $RESULT_DIR"

# Generate summary
echo "Generating summary report..."
cat > "$RESULT_DIR/summary.md" << EOF
# Benchmark Results Summary

Agent: $(jq -r '.name' "$AGENT_CONFIG")
Platform: $PLATFORM
Timestamp: $TIMESTAMP

## Enabled Benchmarks
$(for b in $BENCHMARKS; do echo "- $b"; done)

## Results
$(for b in $BENCHMARKS; do
    if [ -f "$RESULT_DIR/${b}.json" ]; then
        echo "### $b"
        echo "\`\`\`json"
        cat "$RESULT_DIR/${b}.json"
        echo "\`\`\`"
    fi
done)
EOF

echo "Summary report: $RESULT_DIR/summary.md"