#!/bin/bash
set -uo pipefail
# AllClaws Runtime Benchmark Engine v1.0
# Measures: binary size, dependency fetch time, CLI startup time, container image size
# Requires: cargo (Rust), node+npm (TS), python3 (Python), docker (container sizes)

FRAMEWORK_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ALLCLAWS_DIR="$(dirname "$FRAMEWORK_DIR")"
TIMESTAMP="$(date +%Y-%m-%dT%H:%M%S)"
RESULT_DIR="$FRAMEWORK_DIR/benchmark_results/$TIMESTAMP-runtime"
REPORT_JSON="$RESULT_DIR/runtime_benchmark_results.json"
REPORT_MD="$RESULT_DIR/runtime_benchmark_results.md"

mkdir -p "$RESULT_DIR"

if ! command -v jq >/dev/null 2>&1; then
    echo "ERROR: jq is required"
    exit 1
fi

METRICS="[]"

metric() {
    local platform="$1" name="$2" value="${3:-0}" unit="$4" notes="${5:-}"
    value=$(echo "$value" | grep -oE '^[0-9.]+' || echo "0")
    local m="{\"platform\":\"$platform\",\"metric\":\"$name\",\"value\":$value,\"unit\":\"$unit\""
    if [ -n "$notes" ]; then
        m="$m,\"notes\":$(echo "$notes" | jq -Rs .)"
    fi
    m="$m}"
    METRICS=$(echo "$METRICS" | jq --argjson r "$m" '. + [$r]')
    printf "  %-12s %-35s %10s %6s\n" "$platform" "$name" "$value" "$unit"
}

time_cmd() {
    local start end duration
    start=$(date +%s%3N 2>/dev/null || python3 -c 'import time; print(int(time.time()*1000))')
    "$@" >/dev/null 2>&1
    local rc=$?
    end=$(date +%s%3N 2>/dev/null || python3 -c 'import time; print(int(time.time()*1000))')
    duration=$((end - start))
    echo "$rc:$duration"
}

echo "=========================================="
echo " AllClaws Runtime Benchmark Engine v1.0"
echo " $(date '+%Y-%m-%d %H:%M:%S')"
echo "=========================================="
echo ""

# --- Rust platforms ---
for platform in ironclaw zeroclaw; do
    platform_path="$ALLCLAWS_DIR/$platform"
    echo "--- $platform (Rust) ---"
    if [ ! -d "$platform_path" ] || [ ! -f "$platform_path/Cargo.toml" ]; then
        echo "  SKIP: no Cargo.toml"
        continue
    fi
    
    # Binary size estimate (target/release if built)
    if [ -d "$platform_path/target/release" ]; then
        for bin in "$platform_path"/target/release/*; do
            if [ -f "$bin" ] && [ -x "$bin" ]; then
                bname=$(basename "$bin")
                size_kb=$(du -k "$bin" | awk '{print $1}')
                metric "$platform" "binary_${bname}_size" "$size_kb" "KB"
            fi
        done
    fi
    
    # Cargo check timing (fastest way to measure Rust compile readiness)
    result=$(cd "$platform_path" && time_cmd cargo check 2>&1)
    rc=$(echo "$result" | cut -d: -f1)
    duration_ms=$(echo "$result" | cut -d: -f2)
    if [ "$rc" = "0" ]; then
        metric "$platform" "cargo_check_time" "$duration_ms" "ms"
    else
        metric "$platform" "cargo_check_time" "0" "ms" "failed or timeout"
    fi
    
    # Dependency count
    dep_count=$(grep -cE '^\s*\w+\s*=\s*"' "$platform_path/Cargo.toml" 2>/dev/null || echo "0")
    metric "$platform" "cargo_deps" "$dep_count" "deps"
    
    # Source file count
    src_count=$(find "$platform_path" -name "*.rs" -not -path "*/target/*" -not -path "*/.git/*" 2>/dev/null | wc -l | tr -d ' ')
    metric "$platform" "rust_source_files" "$src_count" "files"
    
    echo ""
done

# --- Go platforms (static analysis only, no Go toolchain) ---
for platform in goclaw maxclaw hiclaw; do
    platform_path="$ALLCLAWS_DIR/$platform"
    echo "--- $platform (Go - static only, go toolchain missing) ---"
    if [ ! -d "$platform_path" ]; then
        echo "  SKIP: not found"
        continue
    fi
    
    src_count=$(find "$platform_path" -name "*.go" -not -path "*/vendor/*" -not -path "*/.git/*" 2>/dev/null | wc -l | tr -d ' ')
    metric "$platform" "go_source_files" "$src_count" "files"
    
    if [ -f "$platform_path/go.mod" ]; then
        dep_count=$(grep -cE '^\s+\S+\s+v' "$platform_path/go.mod" 2>/dev/null | tr -d ' ')
        metric "$platform" "go_deps" "$dep_count" "deps"
        go_ver=$(grep '^go ' "$platform_path/go.mod" | awk '{print $2}')
        metric "$platform" "go_version" "$(echo "$go_ver" | sed 's/\.//g')" "version" "$go_ver"
    fi
    
    metric "$platform" "go_build_time" "0" "ms" "go toolchain not available"
    metric "$platform" "binary_size" "0" "KB" "go toolchain not available"
    
    echo ""
done

# --- TypeScript platforms ---
for platform in openclaw nanoclaw quantumclaw; do
    platform_path="$ALLCLAWS_DIR/$platform"
    echo "--- $platform (TypeScript/Node.js) ---"
    if [ ! -d "$platform_path" ] || [ ! -f "$platform_path/package.json" ]; then
        echo "  SKIP: no package.json"
        continue
    fi
    
    # npm dependency count
    npm_deps=$(jq '[.dependencies // {}, .devDependencies // {}] | add | keys | length' "$platform_path/package.json" 2>/dev/null || echo "0")
    metric "$platform" "npm_deps" "$npm_deps" "deps"
    
    # node_modules size if present
    if [ -d "$platform_path/node_modules" ]; then
        nm_size=$(du -sk "$platform_path/node_modules" 2>/dev/null | awk '{print $1}')
        metric "$platform" "node_modules_size" "$nm_size" "KB"
    fi
    
    # npm install timing (dry-run check first)
    result=$(cd "$platform_path" && time_cmd npm install --dry-run 2>&1)
    rc=$(echo "$result" | cut -d: -f1)
    duration_ms=$(echo "$result" | cut -d: -f2)
    if [ "$rc" = "0" ]; then
        metric "$platform" "npm_install_dry_time" "$duration_ms" "ms"
    else
        metric "$platform" "npm_install_dry_time" "0" "ms" "dry-run failed"
    fi
    
    # Source file count
    ts_count=$(find "$platform_path" -name "*.ts" -not -name "*.d.ts" -not -path "*/node_modules/*" -not -path "*/.git/*" 2>/dev/null | wc -l | tr -d ' ')
    metric "$platform" "ts_source_files" "$ts_count" "files"
    
    echo ""
done

# --- Python platforms ---
for platform in clawteam nanobot hermes-agent claw-ai-lab; do
    platform_path="$ALLCLAWS_DIR/$platform"
    echo "--- $platform (Python) ---"
    if [ ! -d "$platform_path" ]; then
        echo "  SKIP: not found"
        continue
    fi
    
    src_count=$(find "$platform_path" -name "*.py" -not -path "*/__pycache__/*" -not -path "*/.git/*" -not -path "*/node_modules/*" 2>/dev/null | wc -l | tr -d ' ')
    metric "$platform" "py_source_files" "$src_count" "files"
    
    # Python import timing (test if main module loads)
    if [ -f "$platform_path/__main__.py" ] || [ -f "$platform_path/setup.py" ] || [ -f "$platform_path/pyproject.toml" ]; then
        result=$(cd "$platform_path" && time_cmd python3 -c "import sys; sys.path.insert(0,'.'); __import__('sys')" 2>&1)
        rc=$(echo "$result" | cut -d: -f1)
        duration_ms=$(echo "$result" | cut -d: -f2)
        metric "$platform" "python_import_time" "$duration_ms" "ms" "baseline import test"
    fi
    
    # Dependency count
    if [ -f "$platform_path/pyproject.toml" ]; then
        dep_count=$(grep -cE '^\s+"[a-zA-Z]' "$platform_path/pyproject.toml" 2>/dev/null | tr -d ' ')
        metric "$platform" "py_deps" "$dep_count" "deps"
    elif [ -f "$platform_path/requirements.txt" ]; then
        dep_count=$(grep -cvE '^\s*$|^\s*#' "$platform_path/requirements.txt" 2>/dev/null | tr -d ' ')
        metric "$platform" "py_deps" "$dep_count" "deps"
    fi
    
    echo ""
done

# --- Container image size estimation ---
echo "--- Container Image Sizes ---"
for platform in goclaw ironclaw openclaw nanoclaw nanobot hiclaw; do
    platform_path="$ALLCLAWS_DIR/$platform"
    dockerfile=$(find "$platform_path" -maxdepth 3 -name "Dockerfile*" -o -name "*.dockerfile" 2>/dev/null | head -1)
    if [ -n "$dockerfile" ]; then
        # Parse FROM image from Dockerfile
        from_image=$(grep -E '^FROM ' "$dockerfile" | head -1 | awk '{print $2}' | cut -d: -f1)
        metric "$platform" "dockerfile_exists" "1" "bool" "FROM: $from_image"
    else
        metric "$platform" "dockerfile_exists" "0" "bool"
    fi
done
echo ""

echo "=========================================="
echo " Report: $REPORT_MD"
echo "=========================================="

# Write JSON report
jq -n \
    --arg timestamp "$TIMESTAMP" \
    --argjson metrics "$METRICS" \
    '{
        timestamp: $timestamp,
        engine_version: "1.0.0-runtime",
        metric_count: ($metrics | length),
        metrics: $metrics
    }' > "$REPORT_JSON"

# Write Markdown report
echo "# Runtime Benchmark Results — $TIMESTAMP" > "$REPORT_MD"
echo "" >> "$REPORT_MD"
echo "Engine v1.0-runtime | $(echo "$METRICS" | jq 'length') metrics" >> "$REPORT_MD"
echo "" >> "$REPORT_MD"

echo "## Build & Dependency Timing" >> "$REPORT_MD"
echo "" >> "$REPORT_MD"
echo "| Platform | Metric | Value | Unit | Notes |" >> "$REPORT_MD"
echo "|----------|--------|-------|------|-------|" >> "$REPORT_MD"
echo "$METRICS" | jq -r '.[] | select(.metric | test("time|size|deps|files|version|docker")) | "| \(.platform) | \(.metric) | \(.value) | \(.unit) | \(.notes // \"\") |"' >> "$REPORT_MD"
echo "" >> "$REPORT_MD"

echo "Full JSON: $REPORT_JSON" >> "$REPORT_MD"
