#!/bin/bash
set -euo pipefail
# AllClaws Runtime Benchmark Engine
# Wrapper for v3.0 Python benchmark suite
# Usage: ./run_runtime_benchmarks.sh [--runs N] [--platform P] [--skip S]

FRAMEWORK_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ALLCLAWS_DIR="$(dirname "$FRAMEWORK_DIR")"

cd "$FRAMEWORK_DIR"

exec python3 -m benchmark.cli runtime \
  --config "$FRAMEWORK_DIR/config.json" \
  --output-dir "$FRAMEWORK_DIR/benchmark_results" \
  "$@"
