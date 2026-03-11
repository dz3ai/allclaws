#!/bin/bash

# Platform Setup Script
# This script initializes and sets up all platform submodules

set -e

FRAMEWORK_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PARENT_DIR="$(dirname "$FRAMEWORK_DIR")"

echo "=========================================="
echo "Setting up all AI agent platforms..."
echo "=========================================="

# Update git submodules
echo ""
echo "Step 1: Initializing git submodules..."
cd "$PARENT_DIR"
git submodule update --init --recursive

# Zeroclaw setup
echo ""
echo "Step 2: Setting up Zeroclaw (Rust)..."
if [ -d "zeroclaw" ]; then
    cd zeroclaw
    if command -v cargo >/dev/null 2>&1; then
        echo "Building Zeroclaw..."
        cargo build --release
        echo "Zeroclaw built successfully: target/release/zeroclaw"
    else
        echo "Warning: cargo not found. Skipping Zeroclaw build."
        echo "Install Rust from https://rustup.rs/"
    fi
    cd "$PARENT_DIR"
else
    echo "Warning: Zeroclaw submodule not found"
fi

# Openclaw setup
echo ""
echo "Step 3: Setting up Openclaw (TypeScript)..."
if [ -d "openclaw" ]; then
    cd openclaw
    if command -v pnpm >/dev/null 2>&1; then
        echo "Installing Openclaw dependencies..."
        pnpm install
        echo "Openclaw setup complete"
    else
        echo "Warning: pnpm not found. Skipping Openclaw setup."
        echo "Install pnpm: npm install -g pnpm"
    fi
    cd "$PARENT_DIR"
else
    echo "Warning: Openclaw submodule not found"
fi

# NanoClaw setup
echo ""
echo "Step 4: Setting up NanoClaw (Node.js)..."
if [ -d "nanoclaw" ]; then
    cd nanoclaw
    if command -v npm >/dev/null 2>&1; then
        echo "Installing NanoClaw dependencies..."
        npm install
        echo "NanoClaw setup complete"
    else
        echo "Warning: npm not found. Skipping NanoClaw setup."
        echo "Install Node.js from https://nodejs.org/"
    fi
    cd "$PARENT_DIR"
else
    echo "Warning: NanoClaw submodule not found"
fi

# IronClaw setup
echo ""
echo "Step 5: Setting up IronClaw (Rust)..."
if [ -d "ironclaw" ]; then
    cd ironclaw
    if command -v cargo >/dev/null 2>&1; then
        echo "Building IronClaw..."
        cargo build --release
        echo "IronClaw built successfully: target/release/ironclaw"
    else
        echo "Warning: cargo not found. Skipping IronClaw build."
    fi
    cd "$PARENT_DIR"
else
    echo "Warning: IronClaw submodule not found"
fi

# GoClaw setup
echo ""
echo "Step 6: Setting up GoClaw (Go)..."
if [ -d "goclaw" ]; then
    cd goclaw
    if command -v go >/dev/null 2>&1; then
        echo "Building GoClaw..."
        go build -o goclaw .
        echo "GoClaw built successfully: goclaw"
    else
        echo "Warning: go not found. Skipping GoClaw build."
        echo "Install Go from https://go.dev/"
    fi
    cd "$PARENT_DIR"
else
    echo "Warning: GoClaw submodule not found"
fi

# Nanobot setup
echo ""
echo "Step 7: Setting up Nanobot (Python)..."
if [ -d "nanobot" ]; then
    cd nanobot
    if command -v python3 >/dev/null 2>&1; then
        echo "Installing Nanobot..."
        pip3 install -e .
        echo "Nanobot installed successfully"
    else
        echo "Warning: python3 not found. Skipping Nanobot setup."
        echo "Install Python from https://www.python.org/"
    fi
    cd "$PARENT_DIR"
else
    echo "Warning: Nanobot submodule not found"
fi

echo ""
echo "=========================================="
echo "Platform setup complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Run test framework setup: cd test_framework && ./scripts/setup.sh"
echo "2. Create an agent configuration in agents/"
echo "3. Run validation: ./scripts/validate_agent.sh <agent_config>"
echo "4. Run benchmarks: ./scripts/run_benchmark.sh <agent_config> <platform>"
echo ""
echo "Available platforms: zeroclaw, openclaw, nanoclaw, ironclaw, goclaw, nanobot"
