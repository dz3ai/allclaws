#!/bin/bash

# Benchmark Runner Script

AGENT_CONFIG=$1
PLATFORM=$2

if [ -z "$AGENT_CONFIG" ] || [ -z "$PLATFORM" ]; then
    echo "Usage: $0 <agent_config.json> <platform>"
    echo "Platforms: zeroclaw, openclaw, nanoclaw, ironclaw, goclaw, nanobot"
    exit 1
fi

if [ ! -f "$AGENT_CONFIG" ]; then
    echo "Agent config file not found: $AGENT_CONFIG"
    exit 1
fi

# Validate platform
case $PLATFORM in
    zeroclaw|openclaw|nanoclaw|ironclaw|goclaw|nanobot)
        ;;
    *)
        echo "Unsupported platform: $PLATFORM"
        echo "Supported: zeroclaw, openclaw, nanoclaw, ironclaw, goclaw, nanobot"
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
            # Use local zeroclaw submodule
            if [ -f "../zeroclaw/Cargo.toml" ]; then
                cd ../zeroclaw
                if [ -f "target/release/zeroclaw" ]; then
                    ./target/release/zeroclaw benchmark "$benchmark" --config "../test_framework/$AGENT_CONFIG" --output "../test_framework/$RESULT_DIR/${benchmark}.json"
                else
                    echo "Zeroclaw binary not found. Building zeroclaw..."
                    cargo build --release
                    ./target/release/zeroclaw benchmark "$benchmark" --config "../test_framework/$AGENT_CONFIG" --output "../test_framework/$RESULT_DIR/${benchmark}.json"
                fi
                cd test_framework
            else
                echo "Zeroclaw submodule not found. Please run: git submodule update --init --recursive"
                exit 1
            fi
            ;;
        openclaw)
            # Use local openclaw submodule
            if [ -f "../openclaw/package.json" ]; then
                cd ../openclaw
                if command -v pnpm >/dev/null 2>&1; then
                    pnpm openclaw benchmark "$benchmark" --config "../test_framework/$AGENT_CONFIG" --output "../test_framework/$RESULT_DIR/${benchmark}.json"
                else
                    echo "pnpm not found. Please install pnpm."
                    cd test_framework
                    exit 1
                fi
                cd test_framework
            else
                echo "Openclaw submodule not found. Please run: git submodule update --init --recursive"
                exit 1
            fi
            ;;
        nanoclaw)
            # Use local nanoclaw submodule
            if [ -f "../nanoclaw/package.json" ]; then
                cd ../nanoclaw
                npm run benchmark "$benchmark" --config "../test_framework/$AGENT_CONFIG" --output "../test_framework/$RESULT_DIR/${benchmark}.json"
                cd test_framework
            else
                echo "NanoClaw submodule not found. Please run: git submodule update --init --recursive"
                exit 1
            fi
            ;;
        ironclaw)
            # Use local ironclaw submodule
            if [ -f "../ironclaw/Cargo.toml" ]; then
                cd ../ironclaw
                if [ -f "target/release/ironclaw" ]; then
                    ./target/release/ironclaw benchmark "$benchmark" --config "../test_framework/$AGENT_CONFIG" --output "../test_framework/$RESULT_DIR/${benchmark}.json"
                else
                    echo "IronClaw binary not found. Building ironclaw..."
                    cargo build --release
                    ./target/release/ironclaw benchmark "$benchmark" --config "../test_framework/$AGENT_CONFIG" --output "../test_framework/$RESULT_DIR/${benchmark}.json"
                fi
                cd test_framework
            else
                echo "IronClaw submodule not found. Please run: git submodule update --init --recursive"
                exit 1
            fi
            ;;
        goclaw)
            # Use local goclaw submodule
            if [ -f "../goclaw/go.mod" ]; then
                cd ../goclaw
                if [ -f "goclaw" ]; then
                    ./goclaw benchmark "$benchmark" --config "../test_framework/$AGENT_CONFIG" --output "../test_framework/$RESULT_DIR/${benchmark}.json"
                else
                    echo "GoClaw binary not found. Building goclaw..."
                    go build -o goclaw .
                    ./goclaw benchmark "$benchmark" --config "../test_framework/$AGENT_CONFIG" --output "../test_framework/$RESULT_DIR/${benchmark}.json"
                fi
                cd test_framework
            else
                echo "GoClaw submodule not found. Please run: git submodule update --init --recursive"
                exit 1
            fi
            ;;
        nanobot)
            # Use local nanobot submodule
            if [ -f "../nanobot/pyproject.toml" ]; then
                cd ../nanobot
                python -m nanobot benchmark "$benchmark" --config "../test_framework/$AGENT_CONFIG" --output "../test_framework/$RESULT_DIR/${benchmark}.json"
                cd test_framework
            else
                echo "Nanobot submodule not found. Please run: git submodule update --init --recursive"
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