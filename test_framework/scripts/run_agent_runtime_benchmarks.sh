#!/bin/bash
set -uo pipefail
# AllClaws Agent Runtime Benchmark Engine v2.0
# Measures: cold start time, memory usage (idle/active), response latency,
#           binary/dependency sizes, installation footprint
# Requires: jq, python3; optionally: cargo, node, go, /usr/bin/time -v

FRAMEWORK_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ALLCLAWS_DIR="$(dirname "$FRAMEWORK_DIR")"
TIMESTAMP="$(date +%Y-%m-%dT%H:%M%S)"
RESULT_DIR="$FRAMEWORK_DIR/benchmark_results/$TIMESTAMP-agent-runtime"
REPORT_JSON="$RESULT_DIR/agent_runtime_benchmark_results.json"
REPORT_MD="$RESULT_DIR/agent_runtime_benchmark_results.md"

mkdir -p "$RESULT_DIR"

# --- Dependency checks (warn, don't fail) ---
HAS_JQ=true
HAS_PYTHON3=true
HAS_TIME_V=false
HAS_CARGO=false
HAS_NODE=false
HAS_GO=false
HAS_PS=true

if ! command -v jq >/dev/null 2>&1; then
    HAS_JQ=false
    echo "WARN: jq not found — JSON report will be skipped"
fi
if ! command -v python3 >/dev/null 2>&1; then
    HAS_PYTHON3=false
    echo "WARN: python3 not found — startup/memory measurements unavailable"
fi
if /usr/bin/time -v true 2>&1 | grep -q "Maximum resident"; then
    HAS_TIME_V=true
fi
if ! command -v ps >/dev/null 2>&1; then
    HAS_PS=false
fi
if command -v cargo >/dev/null 2>&1; then
    HAS_CARGO=true
fi
if command -v node >/dev/null 2>&1; then
    HAS_NODE=true
fi
if command -v go >/dev/null 2>&1; then
    HAS_GO=true
fi

METRICS="[]"
SKIPPED="[]"

# ============================================================
# Helper functions
# ============================================================

metric() {
    # $1=platform $2=metric_name $3=value $4=unit $5=notes (optional)
    local platform="$1" name="$2" value="${3:-0}" unit="$4" notes="${5:-}"
    # Sanitize value to numeric
    value=$(echo "$value" | grep -oE '^[0-9]+\.?[0-9]*' || echo "0")
    if [ "$HAS_JQ" = true ]; then
        local m="{\"platform\":\"$platform\",\"metric\":\"$name\",\"value\":$value,\"unit\":\"$unit\""
        if [ -n "$notes" ]; then
            # Trim trailing whitespace/newlines to avoid extra column in tables
            notes=$(echo "$notes" | sed 's/[[:space:]]*$//')
            m="$m,\"notes\":$(echo "$notes" | jq -Rs .)"
        fi
        m="$m}"
        METRICS=$(echo "$METRICS" | jq --argjson r "$m" '. + [$r]')
    fi
    printf "  %-14s %-38s %12s %8s\n" "$platform" "$name" "$value" "$unit"
}

skip_platform() {
    local platform="$1" reason="$2"
    echo "  SKIP: $reason"
    if [ "$HAS_JQ" = true ]; then
        SKIPPED=$(echo "$SKIPPED" | jq --arg p "$platform" --arg r "$reason" '. + [{platform: $p, reason: $r}]')
    fi
}

time_ms() {
    # Run a command and return elapsed milliseconds
    local start end
    start=$(date +%s%3N 2>/dev/null || python3 -c 'import time; print(int(time.time()*1000))' 2>/dev/null || echo "0")
    "$@" >/dev/null 2>&1
    local rc=$?
    end=$(date +%s%3N 2>/dev/null || python3 -c 'import time; print(int(time.time()*1000))' 2>/dev/null || echo "0")
    local duration=$((end - start))
    echo "$rc:$duration"
}

get_rss_mb() {
    # Get RSS of a PID in MB using ps
    local pid="$1"
    if [ "$HAS_PS" = true ] && kill -0 "$pid" 2>/dev/null; then
        # Linux ps: RSS in KB
        local rss_kb
        rss_kb=$(ps -o rss= -p "$pid" 2>/dev/null | tr -d ' ')
        if [ -n "$rss_kb" ] && [ "$rss_kb" -gt 0 ] 2>/dev/null; then
            echo "$rss_kb"
        else
            echo "0"
        fi
    else
        echo "0"
    fi
}

measure_memory_wrapper() {
    # Run a command with /usr/bin/time -v to get peak RSS
    # Returns "exit_code:peak_rss_kb"
    local cmd=("$@")
    if [ "$HAS_TIME_V" = true ]; then
        local output
        output=$(/usr/bin/time -v "${cmd[@]}" 2>&1)
        local rc=$?
        local peak_kb
        peak_kb=$(echo "$output" | grep "Maximum resident" | awk '{print $NF}' || echo "0")
        echo "$rc:${peak_kb:-0}"
    else
        # Fallback: spawn process, measure via ps quickly
        "${cmd[@]}" &
        local child=$!
        sleep 0.5 2>/dev/null || true
        local rss_kb
        rss_kb=$(get_rss_mb "$child")
        kill "$child" 2>/dev/null || true
        wait "$child" 2>/dev/null || true
        echo "0:$rss_kb"
    fi
}

size_kb_of() {
    local path="$1"
    if [ -e "$path" ]; then
        du -k "$path" 2>/dev/null | awk '{print $1}'
    else
        echo "0"
    fi
}

# ============================================================
# Header
# ============================================================

echo "============================================================"
echo " AllClaws Agent Runtime Benchmark Engine v2.0"
echo " $(date '+%Y-%m-%d %H:%M:%S')"
echo "============================================================"
echo ""
echo "Toolchain availability:"
echo "  jq:        $HAS_JQ"
echo "  python3:   $HAS_PYTHON3"
echo "  /usr/bin/time -v: $HAS_TIME_V"
echo "  cargo:     $HAS_CARGO"
echo "  node:      $HAS_NODE"
echo "  go:        $HAS_GO"
echo "  ps:        $HAS_PS"
echo ""

# ============================================================
# Load config for platform list
# ============================================================

CONFIG_FILE="$FRAMEWORK_DIR/config.json"
if [ -f "$CONFIG_FILE" ] && [ "$HAS_JQ" = true ]; then
    SUPPORTED_PLATFORMS=($(jq -r '.supported_platforms[]' "$CONFIG_FILE"))
else
    SUPPORTED_PLATFORMS=(ironclaw zeroclaw openfang openhuman openclaw nanoclaw quantumclaw openagents copilot-cli goclaw maxclaw hiclaw clawteam nanobot hermes-agent claw-ai-lab smolagents langgraph mcp-agent crewai autogen swarms aider rtl-claw)
fi

# Full ordered list for report tables (all 24 platforms)
ALL_PLATFORMS=(ironclaw zeroclaw openfang openhuman openclaw nanoclaw quantumclaw openagents copilot-cli goclaw maxclaw hiclaw clawteam nanobot hermes-agent claw-ai-lab smolagents langgraph mcp-agent crewai autogen swarms aider rtl-claw)

# ============================================================
# Rust Platforms: ironclaw, zeroclaw
# ============================================================

for platform in ironclaw zeroclaw; do
    platform_path="$ALLCLAWS_DIR/$platform"
    echo "--- $platform (Rust) ---"

    if [ ! -d "$platform_path" ] || [ ! -f "$platform_path/Cargo.toml" ]; then
        skip_platform "$platform" "submodule not populated or no Cargo.toml"
        echo ""
        continue
    fi

    # --- Binary size ---
    if [ -d "$platform_path/target/release" ]; then
        for bin in "$platform_path"/target/release/*; do
            if [ -f "$bin" ] && [ -x "$bin" ]; then
                bname=$(basename "$bin")
                size=$(du -k "$bin" | awk '{print $1}')
                metric "$platform" "binary_${bname}_size" "$size" "KB"
            fi
        done
    else
        metric "$platform" "binary_size" "0" "KB" "no target/release (not built)"
    fi

    # --- Installation footprint (target/ size) ---
    target_size=$(size_kb_of "$platform_path/target")
    metric "$platform" "install_footprint" "$target_size" "KB" "target/ directory"

    # --- Cargo check time (build proxy) ---
    if [ "$HAS_CARGO" = true ]; then
        result=$(cd "$platform_path" && time_ms cargo check 2>&1)
        rc=$(echo "$result" | cut -d: -f1)
        duration_ms=$(echo "$result" | cut -d: -f2)
        if [ "$rc" = "0" ]; then
            metric "$platform" "build_proxy_time" "$duration_ms" "ms" "cargo check"
        else
            metric "$platform" "build_proxy_time" "$duration_ms" "ms" "cargo check failed (rc=$rc)"
        fi
    else
        metric "$platform" "build_proxy_time" "0" "ms" "cargo not available"
    fi

    # --- Cold start time (binary invocation if built) ---
    if [ -d "$platform_path/target/release" ]; then
        main_bin=$(ls "$platform_path/target/release/$platform" "$platform_path/target/release/main" 2>/dev/null | head -1)
        if [ -n "$main_bin" ] && [ -x "$main_bin" ]; then
            result=$(time_ms timeout 5 "$main_bin" --help 2>&1)
            rc=$(echo "$result" | cut -d: -f1)
            duration_ms=$(echo "$result" | cut -d: -f2)
            metric "$platform" "cold_start_time" "$duration_ms" "ms" "$main_bin --help"
        else
            metric "$platform" "cold_start_time" "0" "ms" "no executable binary found"
        fi
    else
        metric "$platform" "cold_start_time" "0" "ms" "binary not built"
    fi

    # --- Memory measurement (idle RSS of --help invocation) ---
    if [ "$HAS_TIME_V" = true ] && [ -d "$platform_path/target/release" ]; then
        main_bin=$(ls "$platform_path/target/release/$platform" "$platform_path/target/release/main" 2>/dev/null | head -1)
        if [ -n "$main_bin" ] && [ -x "$main_bin" ]; then
            mem_result=$(measure_memory_wrapper timeout 5 "$main_bin" --help 2>&1)
            peak_kb=$(echo "$mem_result" | cut -d: -f2)
            if [ "$peak_kb" -gt 0 ] 2>/dev/null; then
                # Convert KB to MB (1 decimal)
                peak_mb=$(echo "$peak_kb" | awk '{printf "%.1f", $1/1024}')
                metric "$platform" "memory_idle_mb" "$peak_mb" "MB"
            else
                metric "$platform" "memory_idle_mb" "0" "MB" "measurement failed"
            fi
        fi
    elif [ "$HAS_PYTHON3" = false ] && [ "$HAS_TIME_V" = false ]; then
        metric "$platform" "memory_idle_mb" "0" "MB" "/usr/bin/time -v not available"
    fi

    echo ""
done

# ============================================================
# Rust Platforms (External): openfang, openhuman
# ============================================================

for platform in openfang openhuman; do
    # External frameworks live at ../PLATFORM relative to allclaws (except openhuman which is inside)
    if [ "$platform" = "openhuman" ]; then
        platform_path="$ALLCLAWS_DIR/$platform"
    else
        platform_path="$(dirname "$ALLCLAWS_DIR")/$platform"
    fi
    echo "--- $platform (Rust) ---"

    if [ ! -d "$platform_path" ] || [ ! -f "$platform_path/Cargo.toml" ]; then
        skip_platform "$platform" "not checked out — tracked via documentation only"
        echo ""
        continue
    fi

    # --- Binary size ---
    if [ -d "$platform_path/target/release" ]; then
        for bin in "$platform_path"/target/release/*; do
            if [ -f "$bin" ] && [ -x "$bin" ]; then
                bname=$(basename "$bin")
                size=$(du -k "$bin" | awk '{print $1}')
                metric "$platform" "binary_${bname}_size" "$size" "KB"
            fi
        done
    else
        metric "$platform" "binary_size" "0" "KB" "no target/release (not built)"
    fi

    # --- Installation footprint (target/ size) ---
    target_size=$(size_kb_of "$platform_path/target")
    metric "$platform" "install_footprint" "$target_size" "KB" "target/ directory"

    # --- Cargo check time (build proxy) ---
    if [ "$HAS_CARGO" = true ]; then
        result=$(cd "$platform_path" && time_ms cargo check 2>&1)
        rc=$(echo "$result" | cut -d: -f1)
        duration_ms=$(echo "$result" | cut -d: -f2)
        if [ "$rc" = "0" ]; then
            metric "$platform" "build_proxy_time" "$duration_ms" "ms" "cargo check"
        else
            metric "$platform" "build_proxy_time" "$duration_ms" "ms" "cargo check failed (rc=$rc)"
        fi
    else
        metric "$platform" "build_proxy_time" "0" "ms" "cargo not available"
    fi

    # --- Cold start time ---
    if [ -d "$platform_path/target/release" ]; then
        main_bin=$(ls "$platform_path/target/release/$platform" "$platform_path/target/release/main" 2>/dev/null | head -1)
        if [ -n "$main_bin" ] && [ -x "$main_bin" ]; then
            result=$(time_ms timeout 5 "$main_bin" --help 2>&1)
            rc=$(echo "$result" | cut -d: -f1)
            duration_ms=$(echo "$result" | cut -d: -f2)
            metric "$platform" "cold_start_time" "$duration_ms" "ms" "$main_bin --help"
        else
            metric "$platform" "cold_start_time" "0" "ms" "no executable binary found"
        fi
    else
        metric "$platform" "cold_start_time" "0" "ms" "binary not built"
    fi

    # --- Memory measurement ---
    if [ "$HAS_TIME_V" = true ] && [ -d "$platform_path/target/release" ]; then
        main_bin=$(ls "$platform_path/target/release/$platform" "$platform_path/target/release/main" 2>/dev/null | head -1)
        if [ -n "$main_bin" ] && [ -x "$main_bin" ]; then
            mem_result=$(measure_memory_wrapper timeout 5 "$main_bin" --help 2>&1)
            peak_kb=$(echo "$mem_result" | cut -d: -f2)
            if [ "$peak_kb" -gt 0 ] 2>/dev/null; then
                peak_mb=$(echo "$peak_kb" | awk '{printf "%.1f", $1/1024}')
                metric "$platform" "memory_idle_mb" "$peak_mb" "MB"
            else
                metric "$platform" "memory_idle_mb" "0" "MB" "measurement failed"
            fi
        fi
    fi

    echo ""
done

# ============================================================
# Go Platforms: goclaw, maxclaw, hiclaw
# ============================================================

for platform in goclaw maxclaw hiclaw; do
    platform_path="$ALLCLAWS_DIR/$platform"
    echo "--- $platform (Go) ---"

    if [ ! -d "$platform_path" ]; then
        skip_platform "$platform" "submodule not populated"
        echo ""
        continue
    fi

    if [ ! -f "$platform_path/go.mod" ]; then
        skip_platform "$platform" "no go.mod found"
        echo ""
        continue
    fi

    # --- Binary size (if pre-built) ---
    built_bins=()
    for candidate in "$platform_path"/bin/* "$platform_path"/$platform; do
        if [ -f "$candidate" ] && [ -x "$candidate" ]; then
            built_bins+=("$candidate")
        fi
    done
    if [ ${#built_bins[@]} -gt 0 ]; then
        for bin in "${built_bins[@]}"; do
            bname=$(basename "$bin")
            size=$(du -k "$bin" | awk '{print $1}')
            metric "$platform" "binary_${bname}_size" "$size" "KB"
        done
    else
        metric "$platform" "binary_size" "0" "KB" "not built"
    fi

    # --- Installation footprint (vendor/ size) ---
    vendor_size=$(size_kb_of "$platform_path/vendor")
    if [ "$vendor_size" -gt 0 ] 2>/dev/null; then
        metric "$platform" "install_footprint" "$vendor_size" "KB" "vendor/ directory"
    else
        # Estimate: GOMODCACHE size for this module
        metric "$platform" "install_footprint" "0" "KB" "no vendor/; go mod download proxy"
    fi

    # --- Go build/check proxy time ---
    if [ "$HAS_GO" = true ]; then
        # go vet is a quick compilation check
        result=$(cd "$platform_path" && time_ms go vet ./... 2>&1)
        rc=$(echo "$result" | cut -d: -f1)
        duration_ms=$(echo "$result" | cut -d: -f2)
        if [ "$rc" = "0" ]; then
            metric "$platform" "build_proxy_time" "$duration_ms" "ms" "go vet ./..."
        else
            # go vet may fail due to missing deps; try go build -o /dev/null
            result=$(cd "$platform_path" && time_ms go build -o /dev/null ./... 2>&1)
            rc2=$(echo "$result" | cut -d: -f1)
            duration_ms2=$(echo "$result" | cut -d: -f2)
            if [ "$rc2" = "0" ]; then
                metric "$platform" "build_proxy_time" "$duration_ms2" "ms" "go build (vet failed)"
            else
                metric "$platform" "build_proxy_time" "$duration_ms" "ms" "go vet failed (rc=$rc)"
            fi
        fi

        # --- Go mod download proxy time ---
        result=$(cd "$platform_path" && time_ms go mod download 2>&1)
        rc=$(echo "$result" | cut -d: -f1)
        duration_ms=$(echo "$result" | cut -d: -f2)
        metric "$platform" "mod_download_time" "$duration_ms" "ms" "go mod download"
    else
        metric "$platform" "build_proxy_time" "0" "ms" "go toolchain not available"
        metric "$platform" "mod_download_time" "0" "ms" "go toolchain not available"
    fi

    # --- Cold start time (if binary exists) ---
    if [ ${#built_bins[@]} -gt 0 ]; then
        main_bin="${built_bins[0]}"
        result=$(time_ms timeout 5 "$main_bin" --help 2>&1)
        rc=$(echo "$result" | cut -d: -f1)
        duration_ms=$(echo "$result" | cut -d: -f2)
        metric "$platform" "cold_start_time" "$duration_ms" "ms" "$(basename "$main_bin") --help"
    else
        metric "$platform" "cold_start_time" "0" "ms" "binary not built"
    fi

    # --- Memory measurement ---
    if [ "$HAS_TIME_V" = true ] && [ ${#built_bins[@]} -gt 0 ]; then
        main_bin="${built_bins[0]}"
        mem_result=$(measure_memory_wrapper timeout 5 "$main_bin" --help 2>&1)
        peak_kb=$(echo "$mem_result" | cut -d: -f2)
        if [ "$peak_kb" -gt 0 ] 2>/dev/null; then
            peak_mb=$(echo "$peak_kb" | awk '{printf "%.1f", $1/1024}')
            metric "$platform" "memory_idle_mb" "$peak_mb" "MB"
        else
            metric "$platform" "memory_idle_mb" "0" "MB" "measurement failed"
        fi
    fi

    echo ""
done

# ============================================================
# TypeScript Platforms: openclaw, nanoclaw, quantumclaw
# ============================================================

for platform in openclaw nanoclaw quantumclaw; do
    platform_path="$ALLCLAWS_DIR/$platform"
    echo "--- $platform (TypeScript) ---"

    if [ ! -d "$platform_path" ] || [ ! -f "$platform_path/package.json" ]; then
        skip_platform "$platform" "submodule not populated or no package.json"
        echo ""
        continue
    fi

    # --- node_modules size ---
    if [ -d "$platform_path/node_modules" ]; then
        nm_size=$(size_kb_of "$platform_path/node_modules")
        metric "$platform" "install_footprint" "$nm_size" "KB" "node_modules/"
    else
        metric "$platform" "install_footprint" "0" "KB" "node_modules/ not installed"
    fi

    # --- Dependency count ---
    npm_deps=$(jq '[.dependencies // {}, .devDependencies // {}] | add | keys | length' "$platform_path/package.json" 2>/dev/null || echo "0")
    metric "$platform" "npm_deps" "$npm_deps" "deps"

    # --- Binary size (dist/ if exists) ---
    if [ -d "$platform_path/dist" ]; then
        dist_size=$(size_kb_of "$platform_path/dist")
        metric "$platform" "binary_size" "$dist_size" "KB" "dist/ directory"
    elif [ -d "$platform_path/build" ]; then
        build_size=$(size_kb_of "$platform_path/build")
        metric "$platform" "binary_size" "$build_size" "KB" "build/ directory"
    else
        metric "$platform" "binary_size" "0" "KB" "no dist/ or build/ directory"
    fi

    # --- Cold start time (node startup for main entry) ---
    if [ "$HAS_NODE" = true ]; then
        # Find the main entry point
        main_entry=""
        if [ -f "$platform_path/src/index.ts" ]; then
            main_entry="$platform_path/src/index.ts"
        elif [ -f "$platform_path/src/index.js" ]; then
            main_entry="$platform_path/src/index.js"
        elif [ -f "$platform_path/src/main.ts" ]; then
            main_entry="$platform_path/src/main.ts"
        elif [ -f "$platform_path/src/main.js" ]; then
            main_entry="$platform_path/src/main.js"
        fi

        if [ -n "$main_entry" ]; then
            # Measure Node.js startup + module parse time (failures expected without full build)
            result=$(cd "$platform_path" && time_ms timeout 10 node -e "
                try {
                    require('${main_entry}');
                } catch(e) {
                    // Expected: import errors without build, we only measure parse time
                }
                process.exit(0);
            " 2>&1)
            rc=$(echo "$result" | cut -d: -f1)
            duration_ms=$(echo "$result" | cut -d: -f2)
            metric "$platform" "cold_start_time" "$duration_ms" "ms" "node parse time (no runtime init)"
        else
            # Fallback: measure bare node startup
            result=$(time_ms node -e "process.exit(0)" 2>&1)
            duration_ms=$(echo "$result" | cut -d: -f2)
            metric "$platform" "cold_start_time" "$duration_ms" "ms" "bare node startup (no entry found)"
        fi
    else
        metric "$platform" "cold_start_time" "0" "ms" "node not available"
    fi

    # --- Response latency proxy (node startup for simple script) ---
    if [ "$HAS_NODE" = true ]; then
        # Measure time from process spawn to first output (echo test)
        result=$(time_ms timeout 10 node -e "console.log('READY'); process.exit(0)" 2>&1)
        duration_ms=$(echo "$result" | cut -d: -f2)
        metric "$platform" "response_latency_ms" "$duration_ms" "ms" "echo benchmark"
    fi

    # --- Memory measurement ---
    if [ "$HAS_TIME_V" = true ] && [ "$HAS_NODE" = true ]; then
        mem_result=$(measure_memory_wrapper node -e "
            const fs = require('fs');
            const path = require('path');
            // Simulate idle: load some modules
            process.exit(0);
        " 2>&1)
        peak_kb=$(echo "$mem_result" | cut -d: -f2)
        if [ "$peak_kb" -gt 0 ] 2>/dev/null; then
            peak_mb=$(echo "$peak_kb" | awk '{printf "%.1f", $1/1024}')
            metric "$platform" "memory_idle_mb" "$peak_mb" "MB"
        else
            metric "$platform" "memory_idle_mb" "0" "MB" "measurement failed"
        fi
    fi

    echo ""
done

# ============================================================
# TypeScript Platforms (External): openagents, copilot-cli
# ============================================================

for platform in openagents copilot-cli; do
    # openagents: external at ../openagents; copilot-cli: inside allclaws
    if [ "$platform" = "copilot-cli" ]; then
        platform_path="$ALLCLAWS_DIR/coding-agents/cli-agents/$platform"
    else
        platform_path="$(dirname "$ALLCLAWS_DIR")/$platform"
    fi
    echo "--- $platform (TypeScript) ---"

    if [ ! -d "$platform_path" ] || [ ! -f "$platform_path/package.json" ]; then
        skip_platform "$platform" "not checked out — tracked via documentation only"
        echo ""
        continue
    fi

    # --- node_modules size ---
    if [ -d "$platform_path/node_modules" ]; then
        nm_size=$(size_kb_of "$platform_path/node_modules")
        metric "$platform" "install_footprint" "$nm_size" "KB" "node_modules/"
    else
        metric "$platform" "install_footprint" "0" "KB" "node_modules/ not installed"
    fi

    # --- Dependency count ---
    npm_deps=$(jq '[.dependencies // {}, .devDependencies // {}] | add | keys | length' "$platform_path/package.json" 2>/dev/null || echo "0")
    metric "$platform" "npm_deps" "$npm_deps" "deps"

    # --- Binary size ---
    if [ -d "$platform_path/dist" ]; then
        dist_size=$(size_kb_of "$platform_path/dist")
        metric "$platform" "binary_size" "$dist_size" "KB" "dist/ directory"
    elif [ -d "$platform_path/build" ]; then
        build_size=$(size_kb_of "$platform_path/build")
        metric "$platform" "binary_size" "$build_size" "KB" "build/ directory"
    else
        metric "$platform" "binary_size" "0" "KB" "no dist/ or build/ directory"
    fi

    # --- Cold start time ---
    if [ "$HAS_NODE" = true ]; then
        main_entry=""
        for candidate in src/index.ts src/index.js src/main.ts src/main.js src/cli.ts src/cli.js; do
            if [ -f "$platform_path/$candidate" ]; then
                main_entry="$platform_path/$candidate"
                break
            fi
        done

        if [ -n "$main_entry" ]; then
            result=$(cd "$platform_path" && time_ms timeout 10 node -e "
                try {
                    require('${main_entry}');
                } catch(e) {
                    // Expected without build
                }
                process.exit(0);
            " 2>&1)
            rc=$(echo "$result" | cut -d: -f1)
            duration_ms=$(echo "$result" | cut -d: -f2)
            metric "$platform" "cold_start_time" "$duration_ms" "ms" "node parse time (no runtime init)"
        else
            result=$(time_ms node -e "process.exit(0)" 2>&1)
            duration_ms=$(echo "$result" | cut -d: -f2)
            metric "$platform" "cold_start_time" "$duration_ms" "ms" "bare node startup (no entry found)"
        fi
    else
        metric "$platform" "cold_start_time" "0" "ms" "node not available"
    fi

    # --- Response latency proxy ---
    if [ "$HAS_NODE" = true ]; then
        result=$(time_ms timeout 10 node -e "console.log('READY'); process.exit(0)" 2>&1)
        duration_ms=$(echo "$result" | cut -d: -f2)
        metric "$platform" "response_latency_ms" "$duration_ms" "ms" "echo benchmark"
    fi

    # --- Memory measurement ---
    if [ "$HAS_TIME_V" = true ] && [ "$HAS_NODE" = true ]; then
        mem_result=$(measure_memory_wrapper node -e "
            const fs = require('fs');
            const path = require('path');
            process.exit(0);
        " 2>&1)
        peak_kb=$(echo "$mem_result" | cut -d: -f2)
        if [ "$peak_kb" -gt 0 ] 2>/dev/null; then
            peak_mb=$(echo "$peak_kb" | awk '{printf "%.1f", $1/1024}')
            metric "$platform" "memory_idle_mb" "$peak_mb" "MB"
        else
            metric "$platform" "memory_idle_mb" "0" "MB" "measurement failed"
        fi
    fi

    echo ""
done

# ============================================================
# Python Platforms: clawteam, nanobot, hermes-agent, claw-ai-lab
# ============================================================

for platform in clawteam nanobot hermes-agent claw-ai-lab; do
    platform_path="$ALLCLAWS_DIR/$platform"
    echo "--- $platform (Python) ---"

    if [ ! -d "$platform_path" ]; then
        skip_platform "$platform" "submodule not populated"
        echo ""
        continue
    fi

    # --- Determine if installable ---
    has_pyproject=false
    has_requirements=false
    if [ -f "$platform_path/pyproject.toml" ]; then
        has_pyproject=true
    fi
    if [ -f "$platform_path/requirements.txt" ]; then
        has_requirements=true
    fi

    if [ "$has_pyproject" = false ] && [ "$has_requirements" = false ]; then
        skip_platform "$platform" "no pyproject.toml or requirements.txt"
        echo ""
        continue
    fi

    # --- Dependency count ---
    if [ "$has_pyproject" = true ]; then
        dep_count=$(grep -cE '^\s+"[a-zA-Z]' "$platform_path/pyproject.toml" 2>/dev/null | tr -d ' ')
        metric "$platform" "py_deps" "$dep_count" "deps"
    elif [ "$has_requirements" = true ]; then
        dep_count=$(grep -cvE '^\s*$|^\s*#' "$platform_path/requirements.txt" 2>/dev/null | tr -d ' ')
        metric "$platform" "py_deps" "$dep_count" "deps"
    fi

    # --- Installation footprint estimate ---
    # Try to find site-packages or .venv
    site_size=0
    if [ -d "$platform_path/.venv" ]; then
        site_size=$(size_kb_of "$platform_path/.venv")
        metric "$platform" "install_footprint" "$site_size" "KB" ".venv/"
    elif [ -d "$platform_path/venv" ]; then
        site_size=$(size_kb_of "$platform_path/venv")
        metric "$platform" "install_footprint" "$site_size" "KB" "venv/"
    elif [ "$has_pyproject" = true ]; then
        # Estimate from dependency count (rough: ~2MB per dep average)
        est_deps=${dep_count:-5}
        est_size=$((est_deps * 2048))
        metric "$platform" "install_footprint" "$est_size" "KB" "estimated (${est_deps} deps x ~2MB)"
    else
        metric "$platform" "install_footprint" "0" "KB" "no venv found"
    fi

    # --- Cold start time (python -c import test) ---
    if [ "$HAS_PYTHON3" = true ]; then
        # Determine the real package import for each platform.
        # These must match the actual installable package names.
        # Platform -> (import_statement, venv_python_path, package_description)
        case "$platform" in
            clawteam)
                import_stmt="import clawteam"
                import_desc="import clawteam"
                ;;
            nanobot)
                import_stmt="import nanobot"
                import_desc="import nanobot"
                ;;
            hermes-agent)
                import_stmt="from run_agent import main"
                import_desc="from run_agent import main"
                ;;
            claw-ai-lab)
                import_stmt="import researchclaw"
                import_desc="import researchclaw"
                ;;
            *)
                import_stmt=""
                import_desc=""
                ;;
        esac

        # Try the platform's venv first, fall back to system python3
        venv_python=""
        if [ -x "$platform_path/.venv/bin/python3" ]; then
            venv_python="$platform_path/.venv/bin/python3"
        elif [ -x "$platform_path/venv/bin/python3" ]; then
            venv_python="$platform_path/venv/bin/python3"
        fi

        if [ -n "$import_stmt" ]; then
            # Try with venv python first (where package is actually installed)
            import_ok=false
            if [ -n "$venv_python" ]; then
                result=$(cd "$platform_path" && PYTHONPATH=. time_ms timeout 10 "$venv_python" -c "
import sys
try:
    $import_stmt
except Exception as e:
    sys.exit(2)
sys.exit(0)
" 2>&1)
                rc=$(echo "$result" | cut -d: -f1)
                if [ "$rc" != "2" ]; then
                    import_ok=true
                fi
            fi

            # Fall back to system python3 with PYTHONPATH
            if [ "$import_ok" = false ]; then
                result=$(cd "$platform_path" && PYTHONPATH=. time_ms timeout 10 python3 -c "
import sys
try:
    $import_stmt
except Exception as e:
    sys.exit(2)
sys.exit(0)
" 2>&1)
                rc=$(echo "$result" | cut -d: -f1)
            fi

            duration_ms=$(echo "$result" | cut -d: -f2)
            if [ "$rc" = "2" ]; then
                metric "$platform" "cold_start_time" "$duration_ms" "ms" "import failed ($import_desc) — package not installed"
            else
                metric "$platform" "cold_start_time" "$duration_ms" "ms" "python $import_desc"
            fi
        else
            # Fallback: baseline Python startup
            result=$(time_ms python3 -c "pass" 2>&1)
            duration_ms=$(echo "$result" | cut -d: -f2)
            metric "$platform" "cold_start_time" "$duration_ms" "ms" "bare python startup (no module found)"
        fi
    else
        metric "$platform" "cold_start_time" "0" "ms" "python3 not available"
    fi

    # --- Response latency proxy (simple print test) ---
    if [ "$HAS_PYTHON3" = true ]; then
        result=$(cd "$platform_path" && time_ms timeout 10 python3 -c "
import sys
sys.stdout.write('READY\n')
sys.stdout.flush()
" 2>&1)
        duration_ms=$(echo "$result" | cut -d: -f2)
        metric "$platform" "response_latency_ms" "$duration_ms" "ms" "echo benchmark"
    fi

    # --- Memory: idle Python process ---
    if [ "$HAS_TIME_V" = true ] && [ "$HAS_PYTHON3" = true ]; then
        mem_result=$(measure_memory_wrapper timeout 10 python3 -c "
import sys, os
sys.path.insert(0, '${platform_path}')
# Attempt to load the main module
try:
    pass
except:
    pass
import time
time.sleep(0.5)
" 2>&1)
        peak_kb=$(echo "$mem_result" | cut -d: -f2)
        if [ "$peak_kb" -gt 0 ] 2>/dev/null; then
            peak_mb=$(echo "$peak_kb" | awk '{printf "%.1f", $1/1024}')
            metric "$platform" "memory_idle_mb" "$peak_mb" "MB" "bare python process"
        else
            metric "$platform" "memory_idle_mb" "0" "MB" "measurement failed"
        fi

        # --- Memory: active (with real platform package import) ---
        # Try venv python first (where the package is installed), then system python
        mem_python="${venv_python:-python3}"
        if [ -n "$import_stmt" ] && [ -x "$mem_python" ]; then
            mem_result=$(measure_memory_wrapper timeout 10 "$mem_python" -c "
import sys, time
sys.path.insert(0, '${platform_path}')
try:
    $import_stmt
except Exception:
    pass
time.sleep(0.3)
" 2>&1)
            peak_kb=$(echo "$mem_result" | cut -d: -f2)
            if [ "$peak_kb" -gt 0 ] 2>/dev/null; then
                peak_mb=$(echo "$peak_kb" | awk '{printf "%.1f", $1/1024}')
                metric "$platform" "memory_active_mb" "$peak_mb" "MB" "python $import_desc ($([ -n \"$venv_python\" ] && echo 'venv' || echo 'system'))"
            else
                metric "$platform" "memory_active_mb" "0" "MB" "package not importable (not installed)"
            fi
        else
            metric "$platform" "memory_active_mb" "0" "MB" "package not importable (no venv or module unknown)"
        fi
    fi

    echo ""
done

# ============================================================
# Python Platforms (External): smolagents, langgraph, mcp-agent,
#   crewai, autogen, swarms, aider
# ============================================================

for platform in smolagents langgraph mcp-agent crewai autogen swarms aider; do
    # External frameworks at ../PLATFORM; aider inside coding-agents/
    if [ "$platform" = "aider" ]; then
        platform_path="$ALLCLAWS_DIR/coding-agents/cli-agents/$platform"
    else
        platform_path="$(dirname "$ALLCLAWS_DIR")/$platform"
    fi
    echo "--- $platform (Python) ---"

    if [ ! -d "$platform_path" ]; then
        skip_platform "$platform" "not checked out — tracked via documentation only"
        echo ""
        continue
    fi

    # --- Determine if installable ---
    has_pyproject=false
    has_requirements=false
    if [ -f "$platform_path/pyproject.toml" ]; then
        has_pyproject=true
    fi
    if [ -f "$platform_path/requirements.txt" ]; then
        has_requirements=true
    fi

    if [ "$has_pyproject" = false ] && [ "$has_requirements" = false ]; then
        skip_platform "$platform" "no pyproject.toml or requirements.txt"
        echo ""
        continue
    fi

    # --- Dependency count ---
    if [ "$has_pyproject" = true ]; then
        dep_count=$(grep -cE '^\s+"[a-zA-Z]' "$platform_path/pyproject.toml" 2>/dev/null | tr -d ' ')
        metric "$platform" "py_deps" "$dep_count" "deps"
    elif [ "$has_requirements" = true ]; then
        dep_count=$(grep -cvE '^\s*$|^\s*#' "$platform_path/requirements.txt" 2>/dev/null | tr -d ' ')
        metric "$platform" "py_deps" "$dep_count" "deps"
    fi

    # --- Installation footprint estimate ---
    if [ -d "$platform_path/.venv" ]; then
        site_size=$(size_kb_of "$platform_path/.venv")
        metric "$platform" "install_footprint" "$site_size" "KB" ".venv/"
    elif [ -d "$platform_path/venv" ]; then
        site_size=$(size_kb_of "$platform_path/venv")
        metric "$platform" "install_footprint" "$site_size" "KB" "venv/"
    else
        metric "$platform" "install_footprint" "0" "KB" "no venv found"
    fi

    # --- Cold start time (python -c import test) ---
    if [ "$HAS_PYTHON3" = true ]; then
        case "$platform" in
            smolagents) import_stmt="import smolagents"; import_desc="import smolagents" ;;
            langgraph)  import_stmt="import langgraph";  import_desc="import langgraph" ;;
            mcp-agent)  import_stmt="import mcp_agent";   import_desc="import mcp_agent" ;;
            crewai)     import_stmt="import crewai";      import_desc="import crewai" ;;
            autogen)    import_stmt="import autogen";     import_desc="import autogen" ;;
            swarms)     import_stmt="import swarms";      import_desc="import swarms" ;;
            aider)      import_stmt="import aider";       import_desc="import aider" ;;
            *)          import_stmt=""; import_desc="" ;;
        esac

        # Try venv first, fall back to system python3
        venv_python=""
        if [ -x "$platform_path/.venv/bin/python3" ]; then
            venv_python="$platform_path/.venv/bin/python3"
        elif [ -x "$platform_path/venv/bin/python3" ]; then
            venv_python="$platform_path/venv/bin/python3"
        fi

        if [ -n "$import_stmt" ]; then
            import_ok=false
            if [ -n "$venv_python" ]; then
                result=$(cd "$platform_path" && PYTHONPATH=. time_ms timeout 10 "$venv_python" -c "
import sys
try:
    $import_stmt
except Exception as e:
    sys.exit(2)
sys.exit(0)
" 2>&1)
                rc=$(echo "$result" | cut -d: -f1)
                if [ "$rc" != "2" ]; then
                    import_ok=true
                fi
            fi

            if [ "$import_ok" = false ]; then
                result=$(cd "$platform_path" && PYTHONPATH=. time_ms timeout 10 python3 -c "
import sys
try:
    $import_stmt
except Exception as e:
    sys.exit(2)
sys.exit(0)
" 2>&1)
                rc=$(echo "$result" | cut -d: -f1)
            fi

            duration_ms=$(echo "$result" | cut -d: -f2)
            if [ "$rc" = "2" ]; then
                metric "$platform" "cold_start_time" "$duration_ms" "ms" "import failed ($import_desc) — package not installed"
            else
                metric "$platform" "cold_start_time" "$duration_ms" "ms" "python $import_desc"
            fi
        else
            result=$(time_ms python3 -c "pass" 2>&1)
            duration_ms=$(echo "$result" | cut -d: -f2)
            metric "$platform" "cold_start_time" "$duration_ms" "ms" "bare python startup (no module found)"
        fi
    else
        metric "$platform" "cold_start_time" "0" "ms" "python3 not available"
    fi

    # --- Response latency proxy ---
    if [ "$HAS_PYTHON3" = true ]; then
        result=$(cd "$platform_path" && time_ms timeout 10 python3 -c "
import sys
sys.stdout.write('READY\n')
sys.stdout.flush()
" 2>&1)
        duration_ms=$(echo "$result" | cut -d: -f2)
        metric "$platform" "response_latency_ms" "$duration_ms" "ms" "echo benchmark"
    fi

    # --- Memory: idle Python process ---
    if [ "$HAS_TIME_V" = true ] && [ "$HAS_PYTHON3" = true ]; then
        mem_result=$(measure_memory_wrapper timeout 10 python3 -c "
import sys, os
sys.path.insert(0, '${platform_path}')
time.sleep(0.5)
" 2>&1)
        peak_kb=$(echo "$mem_result" | cut -d: -f2)
        if [ "$peak_kb" -gt 0 ] 2>/dev/null; then
            peak_mb=$(echo "$peak_kb" | awk '{printf "%.1f", $1/1024}')
            metric "$platform" "memory_idle_mb" "$peak_mb" "MB" "bare python process"
        else
            metric "$platform" "memory_idle_mb" "0" "MB" "measurement failed"
        fi

        # --- Memory: active (with platform package import) ---
        mem_python="${venv_python:-python3}"
        if [ -n "$import_stmt" ] && [ -x "$mem_python" ]; then
            mem_result=$(measure_memory_wrapper timeout 10 "$mem_python" -c "
import sys, time
sys.path.insert(0, '${platform_path}')
try:
    $import_stmt
except Exception:
    pass
time.sleep(0.3)
" 2>&1)
            peak_kb=$(echo "$mem_result" | cut -d: -f2)
            if [ "$peak_kb" -gt 0 ] 2>/dev/null; then
                peak_mb=$(echo "$peak_kb" | awk '{printf "%.1f", $1/1024}')
                metric "$platform" "memory_active_mb" "$peak_mb" "MB" "python $import_desc ($([ -n "$venv_python" ] && echo 'venv' || echo 'system'))"
            else
                metric "$platform" "memory_active_mb" "0" "MB" "package not importable (not installed)"
            fi
        else
            metric "$platform" "memory_active_mb" "0" "MB" "package not importable (no venv or module unknown)"
        fi
    fi

    echo ""
done

# ============================================================
# Verilog Platform: rtl-claw (build-tool only, skip runtime)
# ============================================================

echo "--- rtl-claw (Verilog) ---"
skip_platform "rtl-claw" "build-tool only — no runtime agent metrics applicable"
metric "rtl-claw" "runtime_benchmarks" "0" "N/A" "hardware description language, no runtime"
echo ""

# ============================================================
# Generate Reports
# ============================================================

echo "============================================================"
echo " Report: $REPORT_MD"
echo " JSON:  $REPORT_JSON"
echo "============================================================"

if [ "$HAS_JQ" = true ]; then
    metric_count=$(echo "$METRICS" | jq 'length')
    skip_count=$(echo "$SKIPPED" | jq 'length')

    # --- JSON Report ---
    jq -n \
        --arg timestamp "$TIMESTAMP" \
        --argjson metrics "$METRICS" \
        --argjson skipped "$SKIPPED" \
        --arg engine_version "2.0.0-agent-runtime" \
        --arg has_time_v "$HAS_TIME_V" \
        --arg has_cargo "$HAS_CARGO" \
        --arg has_node "$HAS_NODE" \
        --arg has_go "$HAS_GO" \
        --arg has_python3 "$HAS_PYTHON3" \
        '{
            timestamp: $timestamp,
            engine_version: $engine_version,
            metric_count: ($metrics | length),
            skipped_count: ($skipped | length),
            toolchain: {
                time_v: ($has_time_v == "true"),
                cargo: ($has_cargo == "true"),
                node: ($has_node == "true"),
                go: ($has_go == "true"),
                python3: ($has_python3 == "true")
            },
            metrics: $metrics,
            skipped: $skipped
        }' > "$REPORT_JSON"

    # --- Markdown Report ---
    {
        echo "# Agent Runtime Benchmark Results — $TIMESTAMP"
        echo ""
        echo "Engine v2.0.0-agent-runtime | $metric_count metrics across ${#SUPPORTED_PLATFORMS[@]} platforms"
        echo ""
        echo "## Toolchain"
        echo ""
        echo "| Tool | Available |"
        echo "|------|-----------|"
        echo "| /usr/bin/time -v | $HAS_TIME_V |"
        echo "| cargo | $HAS_CARGO |"
        echo "| node | $HAS_NODE |"
        echo "| go | $HAS_GO |"
        echo "| python3 | $HAS_PYTHON3 |"
        echo ""

        echo "## Cold Start Time (ms)"
        echo ""
        echo "| Platform | Cold Start (ms) | Notes |"
        echo "|----------|-----------------|-------|"
        for plat in "${ALL_PLATFORMS[@]}"; do
            val=$(echo "$METRICS" | jq -r --arg p "$plat" '.[] | select(.platform==$p and .metric=="cold_start_time") | .value // "0"' 2>/dev/null)
            notes=$(echo "$METRICS" | jq -r --arg p "$plat" '.[] | select(.platform==$p and .metric=="cold_start_time") | .notes // ""' 2>/dev/null)
            if [ -n "$val" ] && [ "$val" != "null" ]; then
                echo "| $plat | $val | $notes |"
            fi
        done
        echo ""

        echo "## Memory Usage"
        echo ""
        echo "| Platform | Idle (MB) | Active (MB) | Notes |"
        echo "|----------|-----------|-------------|-------|"
        for plat in "${ALL_PLATFORMS[@]}"; do
            idle=$(echo "$METRICS" | jq -r --arg p "$plat" '.[] | select(.platform==$p and .metric=="memory_idle_mb") | .value // "0"' 2>/dev/null)
            active=$(echo "$METRICS" | jq -r --arg p "$plat" '.[] | select(.platform==$p and .metric=="memory_active_mb") | .value // "0"' 2>/dev/null)
            notes=$(echo "$METRICS" | jq -r --arg p "$plat" '.[] | select(.platform==$p and .metric=="memory_idle_mb") | .notes // ""' 2>/dev/null)
            if [ -n "$idle" ] && [ "$idle" != "null" ]; then
                echo "| $plat | $idle | $active | $notes |"
            fi
        done
        echo ""

        echo "## Binary / Installation Size"
        echo ""
        echo "| Platform | Binary Size (KB) | Install Footprint (KB) | Notes |"
        echo "|----------|------------------|------------------------|-------|"
        for plat in "${ALL_PLATFORMS[@]}"; do
            bin_size=$(echo "$METRICS" | jq -r --arg p "$plat" '.[] | select(.platform==$p and (.metric | startswith("binary"))) | .value // "0"' 2>/dev/null | head -1)
            inst_size=$(echo "$METRICS" | jq -r --arg p "$plat" '.[] | select(.platform==$p and .metric=="install_footprint") | .value // "0"' 2>/dev/null)
            notes=$(echo "$METRICS" | jq -r --arg p "$plat" '.[] | select(.platform==$p and .metric=="install_footprint") | .notes // ""' 2>/dev/null)
            if [ -n "$bin_size" ] && [ "$bin_size" != "null" ]; then
                echo "| $plat | $bin_size | $inst_size | $notes |"
            fi
        done
        echo ""

        echo "## Response Latency (Echo Benchmark)"
        echo ""
        echo "| Platform | Latency (ms) | Notes |"
        echo "|----------|--------------|-------|"
        for plat in "${ALL_PLATFORMS[@]}"; do
            val=$(echo "$METRICS" | jq -r --arg p "$plat" '.[] | select(.platform==$p and .metric=="response_latency_ms") | .value // "0"' 2>/dev/null)
            notes=$(echo "$METRICS" | jq -r --arg p "$plat" '.[] | select(.platform==$p and .metric=="response_latency_ms") | .notes // ""' 2>/dev/null)
            if [ -n "$val" ] && [ "$val" != "null" ]; then
                echo "| $plat | $val | $notes |"
            fi
        done
        echo ""

        echo "## Build Proxy Time"
        echo ""
        echo "| Platform | Build Time (ms) | Notes |"
        echo "|----------|----------------|-------|"
        for plat in "${ALL_PLATFORMS[@]}"; do
            val=$(echo "$METRICS" | jq -r --arg p "$plat" '.[] | select(.platform==$p and .metric=="build_proxy_time") | .value // "0"' 2>/dev/null)
            notes=$(echo "$METRICS" | jq -r --arg p "$plat" '.[] | select(.platform==$p and .metric=="build_proxy_time") | .notes // ""' 2>/dev/null)
            if [ -n "$val" ] && [ "$val" != "null" ]; then
                echo "| $plat | $val | $notes |"
            fi
        done
        echo ""

        echo "## All Metrics (Raw)"
        echo ""
        echo "| Platform | Metric | Value | Unit | Notes |"
        echo "|----------|--------|-------|------|-------|"
        echo "$METRICS" | jq -r '.[] | "| \(.platform) | \(.metric) | \(.value) | \(.unit) | \(.notes // "") |"'
        echo ""

        if [ "$skip_count" -gt 0 ] 2>/dev/null; then
            echo "## Skipped Platforms"
            echo ""
            echo "$SKIPPED" | jq -r '.[] | "- **\(.platform)**: \(.reason)"'
            echo ""
        fi

        echo "Full JSON: \`$REPORT_JSON\`"
    } > "$REPORT_MD"
else
    echo "WARN: jq not available — markdown report not generated"
    # Write a minimal markdown report without jq
    echo "# Agent Runtime Benchmark Results — $TIMESTAMP" > "$REPORT_MD"
    echo "" >> "$REPORT_MD"
    echo "Engine v2.0.0 | jq not available — only console output recorded" >> "$REPORT_MD"
fi

echo ""
echo "Done. Collected $metric_count metrics."
