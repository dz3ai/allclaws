#!/bin/bash
set -uo pipefail

FRAMEWORK_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ALLCLAWS_DIR="$(dirname "$FRAMEWORK_DIR")"
TIMESTAMP="$(date +%Y-%m-%dT%H:%M%S)"
RESULT_DIR="$FRAMEWORK_DIR/benchmark_results/$TIMESTAMP"
REPORT_JSON="$RESULT_DIR/benchmark_results.json"
REPORT_MD="$RESULT_DIR/benchmark_results.md"

mkdir -p "$RESULT_DIR"

if ! command -v jq >/dev/null 2>&1; then
    echo "ERROR: jq is required. Install with: brew install jq"
    exit 1
fi

PLATFORMS=(
    openclaw:TypeScript
    clawteam:Python
    goclaw:Go
    ironclaw:Rust
    maxclaw:Go
    nanoclaw:TypeScript
    nanobot:Python
    zeroclaw:Rust
)

METRICS="[]"

echo "=========================================="
echo " AllClaws Benchmark Engine v1.0"
echo " $(date '+%Y-%m-%d %H:%M:%S')"
echo "=========================================="
echo ""

metric() {
    local platform="$1" name="$2" value="${3:-0}" unit="$4" notes="${5:-}"
    value=$(echo "$value" | grep -oE '^[0-9]+' || echo "0")
    local m="{\"platform\":\"$platform\",\"metric\":\"$name\",\"value\":$value,\"unit\":\"$unit\""
    if [ -n "$notes" ]; then
        m="$m,\"notes\":$(echo "$notes" | jq -Rs .)"
    fi
    m="$m}"
    METRICS=$(echo "$METRICS" | jq --argjson r "$m" '. + [$r]')
    printf "  %-12s %-28s %10s %6s\n" "$platform" "$name" "$value" "$unit"
}

count_files() {
    local dir="$1" ext="$2" maxdepth="${3:-5}"
    find "$dir" -maxdepth "$maxdepth" \
        \( -name ".git" -o -name "node_modules" -o -name "target" -o -name "vendor" \
        -o -name "__pycache__" -o -name ".venv" -o -name "dist" -o -name "build" \
        -o -name ".next" -o -name "coverage" -o -name ".turbo" -o -name ".claude" \) -prune \
        -o -name "*.$ext" -type f -print 2>/dev/null | wc -l | tr -d ' ' | grep -oE '^[0-9]+' || echo "0"
}

count_loc() {
    local dir="$1" ext="$2" maxdepth="${3:-5}"
    local lines
    lines=$(find "$dir" -maxdepth "$maxdepth" \
        \( -name ".git" -o -name "node_modules" -o -name "target" -o -name "vendor" \
        -o -name "__pycache__" -o -name ".venv" -o -name "dist" -o -name "build" \
        -o -name ".next" -o -name "coverage" -o -name ".turbo" -o -name ".claude" \) -prune \
        -o -name "*.$ext" -type f -print 2>/dev/null \
        | xargs wc -l 2>/dev/null | tail -1 | awk '{print $1}')
    echo "${lines:-0}"
}

count_dirs() {
    local dir="$1" maxdepth="${2:-1}"
    find "$dir" -maxdepth "$maxdepth" -type d 2>/dev/null | wc -l | tr -d ' '
}

count_test_files() {
    local dir="$1"
    local count=0
    count=$((count + $(find "$dir" -maxdepth 5 -name "*_test.go" -type f 2>/dev/null | wc -l | tr -d ' ')))
    count=$((count + $(find "$dir" -maxdepth 5 -name "test_*.py" -type f 2>/dev/null | wc -l | tr -d ' ')))
    local ts_tests
    ts_tests=$(find "$dir" -maxdepth 5 \( -name "*.test.ts" -o -name "*.test.tsx" -o -name "*.spec.ts" -o -name "*.spec.tsx" \) -type f 2>/dev/null | wc -l | tr -d ' ')
    count=$((count + ts_tests))
    count=$((count + $(find "$dir" -maxdepth 5 -path "*/tests/*" -name "*.rs" -type f 2>/dev/null | wc -l | tr -d ' ')))
    echo "$count"
}

count_ci_workflows() {
    local dir="$1"
    find "$dir/.github/workflows" -name "*.yml" -o -name "*.yaml" 2>/dev/null | wc -l | tr -d ' '
}

count_i18n_files() {
    local dir="$1"
    local count=0
    count=$((count + $(find "$dir" -maxdepth 3 -name "*.zh-CN.md" -o -name "*.zh_CN.md" -o -name "*.zh.md" 2>/dev/null | wc -l | tr -d ' ')))
    count=$((count + $(find "$dir" -maxdepth 4 -path "*/i18n/*" -o -path "*/locales/*" -o -path "*/messages/*" 2>/dev/null | head -1 | wc -l | tr -d ' ')))
    if [ "$count" -gt 0 ]; then echo "$count"; else echo "0"; fi
}

get_readme_lines() {
    local dir="$1"
    local readme
    readme=$(find "$dir" -maxdepth 1 -iname "README*" -type f 2>/dev/null | head -1)
    if [ -n "$readme" ]; then
        wc -l < "$readme" | tr -d ' '
    else
        echo "0"
    fi
}

get_docs_size() {
    local dir="$1"
    if [ -d "$dir/docs" ]; then
        du -sk "$dir/docs" 2>/dev/null | awk '{print $1}'
    else
        echo "0"
    fi
}

get_ci_steps() {
    local dir="$1"
    local steps=0
    if [ -d "$dir/.github/workflows" ]; then
        steps=$(grep -c "^\s*-\s*uses:\|^\s*-\s*run:" "$dir"/.github/workflows/*.yml "$dir"/.github/workflows/*.yaml 2>/dev/null | awk -F: '{sum+=$NF}END{print sum+0}')
    fi
    echo "$steps"
}

get_repo_size_kb() {
    local dir="$1"
    local size
    size=$(find "$dir" -maxdepth 1 \
        ! -name "node_modules" ! -name "target" ! -name "vendor" \
        ! -name "dist" ! -name "build" ! -name ".next" \
        ! -name "__pycache__" ! -name ".venv" ! -name "coverage" \
        -exec du -sk {} + 2>/dev/null \
        | awk '{sum+=$1}END{print sum+0}')
    echo "${size:-0}"
}

get_dockerfile_count() {
    local dir="$1"
    find "$dir" -maxdepth 4 \( -name "Dockerfile*" -o -name "*.dockerfile" \) -type f 2>/dev/null | wc -l | tr -d ' '
}

get_makefile_targets() {
    local dir="$1"
    if [ -f "$dir/Makefile" ]; then
        grep -cE '^[a-zA-Z_-]+:' "$dir/Makefile" 2>/dev/null | tr -d ' '
    else
        echo "0"
    fi
}

for entry in "${PLATFORMS[@]}"; do
    platform="${entry%%:*}"
    language="${entry##*:}"
    platform_path="$ALLCLAWS_DIR/$platform"

    echo "--- $platform ($language) ---"

    if [ ! -d "$platform_path" ] || [ -z "$(ls -A "$platform_path" 2>/dev/null)" ]; then
        echo "  SKIP: submodule not populated"
        echo ""
        continue
    fi

    repo_size=$(get_repo_size_kb "$platform_path")
    metric "$platform" "repo_size" "$repo_size" "KB"

    readme_lines=$(get_readme_lines "$platform_path")
    metric "$platform" "readme_lines" "$readme_lines" "lines"

    docs_size=$(get_docs_size "$platform_path")
    metric "$platform" "docs_size" "$docs_size" "KB"

    ci_workflows=$(count_ci_workflows "$platform_path")
    metric "$platform" "ci_workflows" "$ci_workflows" "files"

    ci_steps=$(get_ci_steps "$platform_path")
    metric "$platform" "ci_steps" "$ci_steps" "steps"

    dockerfiles=$(get_dockerfile_count "$platform_path")
    metric "$platform" "dockerfiles" "$dockerfiles" "files"

    makefile_targets=$(get_makefile_targets "$platform_path")
    metric "$platform" "makefile_targets" "$makefile_targets" "targets"

    test_files=$(count_test_files "$platform_path")
    metric "$platform" "test_files" "$test_files" "files"

    i18n=$(count_i18n_files "$platform_path")
    metric "$platform" "i18n_files" "$i18n" "files"

    top_level_dirs=$(count_dirs "$platform_path" 2)
    metric "$platform" "top_level_dirs" "$top_level_dirs" "dirs"

    case "$language" in
        Rust)
            rs_files=$(count_files "$platform_path" rs)
            metric "$platform" "rust_files" "$rs_files" "files"

            rs_loc=$(count_loc "$platform_path" rs)
            metric "$platform" "rust_loc" "$rs_loc" "lines"

            toml_files=$(count_files "$platform_path" toml)
            metric "$platform" "toml_files" "$toml_files" "files"

            cargo_deps=0
            if [ -f "$platform_path/Cargo.toml" ]; then
                cargo_deps=$(grep -cE '^\w+\s*=\s*"' "$platform_path/Cargo.toml" 2>/dev/null | tr -d ' ')
            fi
            if [ "$cargo_deps" -eq 0 ] && [ -f "$platform_path/Cargo.toml" ]; then
                cargo_deps=$(grep -cE '\"[a-zA-Z]' "$platform_path/Cargo.toml" 2>/dev/null | tr -d ' ')
            fi
            metric "$platform" "cargo_deps" "$cargo_deps" "deps"
            ;;
        TypeScript)
            ts_files=$(count_files "$platform_path" ts)
            metric "$platform" "ts_files" "$ts_files" "files"

            ts_loc=$(count_loc "$platform_path" ts)
            metric "$platform" "ts_loc" "$ts_loc" "lines"

            tsx_files=$(count_files "$platform_path" tsx)
            metric "$platform" "tsx_files" "$tsx_files" "files"

            tsx_loc=$(count_loc "$platform_path" tsx)
            metric "$platform" "tsx_loc" "$tsx_loc" "lines"

            json_files=$(count_files "$platform_path" json)
            metric "$platform" "json_files" "$json_files" "files"

            npm_deps=0
            if [ -f "$platform_path/package.json" ]; then
                npm_deps=$(jq '[.dependencies // {}, .devDependencies // {}] | add | keys | length' "$platform_path/package.json" 2>/dev/null || echo "0")
            fi
            metric "$platform" "npm_deps" "$npm_deps" "deps"
            ;;
        Go)
            go_files=$(count_files "$platform_path" go)
            metric "$platform" "go_files" "$go_files" "files"

            go_loc=$(count_loc "$platform_path" go)
            metric "$platform" "go_loc" "$go_loc" "lines"

            go_mod_deps=0
            if [ -f "$platform_path/go.mod" ]; then
                go_mod_deps=$(grep -cE '^\s+\S+\s+v' "$platform_path/go.mod" 2>/dev/null | tr -d ' ')
            fi
            metric "$platform" "go_deps" "$go_mod_deps" "deps"
            ;;
        Python)
            py_files=$(count_files "$platform_path" py)
            metric "$platform" "py_files" "$py_files" "files"

            py_loc=$(count_loc "$platform_path" py)
            metric "$platform" "py_loc" "$py_loc" "lines"

            py_deps=0
            if [ -f "$platform_path/pyproject.toml" ]; then
                py_deps=$(grep -cE '^\s+"[a-zA-Z]' "$platform_path/pyproject.toml" 2>/dev/null | tr -d ' ')
            elif [ -f "$platform_path/requirements.txt" ]; then
                py_deps=$(grep -cvE '^\s*$|^\s*#' "$platform_path/requirements.txt" 2>/dev/null | tr -d ' ')
            fi
            metric "$platform" "py_deps" "$py_deps" "deps"
            ;;
    esac

    echo ""
done

echo "=========================================="
echo " Report: $REPORT_MD"
echo "=========================================="

jq -n \
    --arg timestamp "$TIMESTAMP" \
    --argjson metrics "$METRICS" \
    '{
        timestamp: $timestamp,
        engine_version: "1.0.0",
        metric_count: ($metrics | length),
        metrics: $metrics
    }' > "$REPORT_JSON"

echo "# Benchmark Results — $TIMESTAMP" > "$REPORT_MD"
echo "" >> "$REPORT_MD"
echo "Engine v1.0.0 | $(echo "$METRICS" | jq 'length') metrics across 8 platforms" >> "$REPORT_MD"
echo "" >> "$REPORT_MD"

echo "## Repository Size" >> "$REPORT_MD"
echo "" >> "$REPORT_MD"
echo "| Platform | Repo Size (KB) | Source Files | Source LOC | Dependencies | Test Files |" >> "$REPORT_MD"
echo "|----------|----------------|-------------|-----------|--------------|-----------|" >> "$REPORT_MD"

for entry in "${PLATFORMS[@]}"; do
    platform="${entry%%:*}"
    language="${entry##*:}"

    case "$language" in
        Rust) src_col="rust_files"; loc_col="rust_loc"; dep_col="cargo_deps" ;;
        TypeScript) src_col="ts_files"; loc_col="ts_loc"; dep_col="npm_deps" ;;
        Go) src_col="go_files"; loc_col="go_loc"; dep_col="go_deps" ;;
        Python) src_col="py_files"; loc_col="py_loc"; dep_col="py_deps" ;;
    esac

    repo_size=$(echo "$METRICS" | jq -r --arg p "$platform" '.[] | select(.platform==$p and .metric=="repo_size") | .value // "0"')
    src_files=$(echo "$METRICS" | jq -r --arg p "$platform" --arg c "$src_col" '.[] | select(.platform==$p and .metric==$c) | .value // "0"')
    src_loc=$(echo "$METRICS" | jq -r --arg p "$platform" --arg c "$loc_col" '.[] | select(.platform==$p and .metric==$c) | .value // "0"')
    deps=$(echo "$METRICS" | jq -r --arg p "$platform" --arg c "$dep_col" '.[] | select(.platform==$p and .metric==$c) | .value // "0"')
    tests=$(echo "$METRICS" | jq -r --arg p "$platform" '.[] | select(.platform==$p and .metric=="test_files") | .value // "0"')

    echo "| $platform | $repo_size | $src_files | $src_loc | $deps | $tests |" >> "$REPORT_MD"
done
echo "" >> "$REPORT_MD"

echo "## Project Health" >> "$REPORT_MD"
echo "" >> "$REPORT_MD"
echo "| Platform | CI Workflows | CI Steps | Dockerfiles | Makefile Targets | README Lines | Docs (KB) | i18n Files |" >> "$REPORT_MD"
echo "|----------|---------------|----------|-------------|-----------------|-------------|-----------|------------|" >> "$REPORT_MD"

for entry in "${PLATFORMS[@]}"; do
    platform="${entry%%:*}"

    ci_wf=$(echo "$METRICS" | jq -r --arg p "$platform" '.[] | select(.platform==$p and .metric=="ci_workflows") | .value')
    ci_st=$(echo "$METRICS" | jq -r --arg p "$platform" '.[] | select(.platform==$p and .metric=="ci_steps") | .value')
    df=$(echo "$METRICS" | jq -r --arg p "$platform" '.[] | select(.platform==$p and .metric=="dockerfiles") | .value')
    mf=$(echo "$METRICS" | jq -r --arg p "$platform" '.[] | select(.platform==$p and .metric=="makefile_targets") | .value')
    rl=$(echo "$METRICS" | jq -r --arg p "$platform" '.[] | select(.platform==$p and .metric=="readme_lines") | .value')
    ds=$(echo "$METRICS" | jq -r --arg p "$platform" '.[] | select(.platform==$p and .metric=="docs_size") | .value')
    i18=$(echo "$METRICS" | jq -r --arg p "$platform" '.[] | select(.platform==$p and .metric=="i18n_files") | .value')

    echo "| $platform | $ci_wf | $ci_st | $df | $mf | $rl | $ds | $i18 |" >> "$REPORT_MD"
done
echo "" >> "$REPORT_MD"

echo "## All Metrics (Raw)" >> "$REPORT_MD"
echo "" >> "$REPORT_MD"
echo "| Platform | Metric | Value | Unit |" >> "$REPORT_MD"
echo "|----------|--------|-------|------|" >> "$REPORT_MD"
echo "$METRICS" | jq -r '.[] | "| \(.platform) | \(.metric) | \(.value) | \(.unit) |"' >> "$REPORT_MD"
echo "" >> "$REPORT_MD"

echo "Full JSON: $REPORT_JSON"
