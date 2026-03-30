#!/bin/bash
set -uo pipefail

FRAMEWORK_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ALLCLAWS_DIR="$(dirname "$FRAMEWORK_DIR")"
TIMESTAMP="$(date +%Y-%m-%dT%H:%M%S)"
RESULT_DIR="$FRAMEWORK_DIR/results/$TIMESTAMP"
REPORT_JSON="$RESULT_DIR/results.json"
REPORT_MD="$RESULT_DIR/results.md"

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

echo "=========================================="
echo " AllClaws Test Framework v2.0"
echo " $(date '+%Y-%m-%d %H:%M:%S')"
echo "=========================================="
echo ""

PASS_COUNT=0
FAIL_COUNT=0
SKIP_COUNT=0
TOTAL_COUNT=0
RESULTS="[]"

run_test() {
    local test_id="$1" test_desc="$2"
    shift 2
    TOTAL_COUNT=$((TOTAL_COUNT + 1))
    local status="pass" detail=""

    local output rc
    output=$("$@" 2>&1)
    rc=$?

    if [ $rc -eq 77 ]; then
        status="skip"
        SKIP_COUNT=$((SKIP_COUNT + 1))
    elif [ $rc -ne 0 ]; then
        status="fail"
        FAIL_COUNT=$((FAIL_COUNT + 1))
    else
        PASS_COUNT=$((PASS_COUNT + 1))
    fi
    detail="$output"

    local result="{\"id\":\"$test_id\",\"desc\":\"$test_desc\",\"status\":\"$status\",\"detail\":$(echo "$detail" | jq -Rs .)}"

    RESULTS=$(echo "$RESULTS" | jq --argjson r "$result" '. + [$r]')

    case "$status" in
        pass) echo "  [PASS] $test_id: $test_desc" ;;
        fail) echo "  [FAIL] $test_id: $test_desc" ;;
        skip) echo "  [SKIP] $test_id: $test_desc" ;;
    esac

    if [ "$status" != "pass" ] && [ -n "$detail" ]; then
        echo "         $detail" | head -3
    fi
}

source "$FRAMEWORK_DIR/tests/helpers/code_metrics.sh" 2>/dev/null || true

check_file_exists() {
    local dir="$1"
    local pattern="$2"
    local match
    match=$(find "$dir" -maxdepth 1 -name "*${pattern}*" 2>/dev/null | head -1)
    if [ -n "$match" ]; then
        echo "pass"
    else
        echo "FAIL: no file matching '$pattern' found"
        return 1
    fi
}

for entry in "${PLATFORMS[@]}"; do
    platform="${entry%%:*}"
    language="${entry##*:}"
    platform_path="$ALLCLAWS_DIR/$platform"

    echo "--- $platform ($language) ---"

    if [ ! -d "$platform_path" ] || [ -z "$(ls -A "$platform_path" 2>/dev/null)" ]; then
        run_test "$platform.init" "Submodule exists" exit 77
        echo ""
        continue
    fi

    run_test "$platform.init" "Submodule exists and populated" true

    case "$language" in
        Rust)
            source "$FRAMEWORK_DIR/tests/test_rust.sh"
            run_test "$platform.manifest" "Has Cargo.toml" test_rust_manifest "$platform_path"
            run_test "$platform.workspace" "Workspace structure" test_rust_workspace "$platform_path"
            run_test "$platform.source" "Has Rust source files" test_rust_crates "$platform_path"
            run_test "$platform.lock" "Has Cargo.lock" test_rust_lock "$platform_path"
            run_test "$platform.clippy" "Has clippy config" test_rust_clippy "$platform_path"
            run_test "$platform.ci_lang" "Has Rust CI" test_rust_ci "$platform_path"
            run_test "$platform.deny" "Has cargo-deny" test_rust_deny "$platform_path"
            ;;
        TypeScript)
            source "$FRAMEWORK_DIR/tests/test_typescript.sh"
            run_test "$platform.manifest" "Has package.json" test_typescript_manifest "$platform_path"
            run_test "$platform.source" "Has TypeScript source" test_typescript_source "$platform_path"
            run_test "$platform.lock" "Has lockfile" test_typescript_lock "$platform_path"
            run_test "$platform.ci_lang" "Has TS CI" test_typescript_ci "$platform_path"
            run_test "$platform.docker" "Has Docker" test_typescript_docker "$platform_path"
            ;;
        Go)
            source "$FRAMEWORK_DIR/tests/test_go.sh"
            run_test "$platform.manifest" "Has go.mod" test_go_module "$platform_path"
            run_test "$platform.source" "Has Go source files" test_go_source "$platform_path"
            run_test "$platform.sum" "Has go.sum" test_go_sum "$platform_path"
            run_test "$platform.ci_lang" "Has Go CI" test_go_ci "$platform_path"
            run_test "$platform.docker" "Has Docker" test_go_docker "$platform_path"
            run_test "$platform.makefile" "Has Makefile" test_go_makefile "$platform_path"
            ;;
        Python)
            source "$FRAMEWORK_DIR/tests/test_python.sh"
            run_test "$platform.manifest" "Has Python manifest" test_python_manifest "$platform_path"
            run_test "$platform.source" "Has Python source" test_python_source "$platform_path"
            run_test "$platform.docker" "Has Docker" test_python_docker "$platform_path"
            run_test "$platform.ci_lang" "Has Python CI" test_python_ci "$platform_path"
            run_test "$platform.tests_dir" "Has tests directory" test_python_tests_dir "$platform_path"
            ;;
    esac

    run_test "$platform.license" "Has open-source license" check_file_exists "$platform_path" LICENSE
    run_test "$platform.readme" "Has README" check_file_exists "$platform_path" README
    run_test "$platform.changelog" "Has CHANGELOG" check_file_exists "$platform_path" CHANGELOG
    run_test "$platform.contributing" "Has CONTRIBUTING" check_file_exists "$platform_path" CONTRIBUTING
    run_test "$platform.gitignore" "Has .gitignore" check_file_exists "$platform_path" .gitignore
    run_test "$platform.ci" "Has CI configuration" check_file_exists "$platform_path" .github

    echo ""
done

echo "=========================================="
echo " RESULTS: $PASS_COUNT pass, $FAIL_COUNT fail, $SKIP_COUNT skip ($TOTAL_COUNT total)"
echo " Report: $REPORT_MD"
echo "=========================================="

jq -n \
    --arg timestamp "$TIMESTAMP" \
    --arg total "$TOTAL_COUNT" \
    --arg pass "$PASS_COUNT" \
    --arg fail "$FAIL_COUNT" \
    --arg skip "$SKIP_COUNT" \
    --argjson results "$RESULTS" \
    '{
        timestamp: $timestamp,
        total: ($total | tonumber),
        passed: ($pass | tonumber),
        failed: ($fail | tonumber),
        skipped: ($skip | tonumber),
        results: $results
    }' > "$REPORT_JSON"

echo "# Test Results — $TIMESTAMP" > "$REPORT_MD"
echo "" >> "$REPORT_MD"
echo "| Status | Count |" >> "$REPORT_MD"
echo "|--------|-------|" >> "$REPORT_MD"
echo "| PASS   | $PASS_COUNT |" >> "$REPORT_MD"
echo "| FAIL   | $FAIL_COUNT |" >> "$REPORT_MD"
echo "| SKIP   | $SKIP_COUNT |" >> "$REPORT_MD"
echo "| **Total** | **$TOTAL_COUNT** |" >> "$REPORT_MD"
echo "" >> "$REPORT_MD"

echo "## All Results" >> "$REPORT_MD"
echo "" >> "$REPORT_MD"
echo "| Status | Test ID | Description | Detail |" >> "$REPORT_MD"
echo "|--------|---------|-------------|--------|" >> "$REPORT_MD"
echo "$RESULTS" | jq -r '.[] | "| \(.status | ascii_upcase) | \(.id) | \(.desc) | \(.detail[:100]) |"' >> "$REPORT_MD"
echo "" >> "$REPORT_MD"

echo "Full JSON: $REPORT_JSON"
