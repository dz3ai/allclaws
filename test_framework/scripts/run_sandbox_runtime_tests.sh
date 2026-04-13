#!/bin/bash
# AllClaws Sandbox Runtime Tests
# Tests applications running inside Docker/Podman sandboxes
# Captures environment issues, build failures, and runtime findings

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FRAMEWORK_DIR="$(dirname "$SCRIPT_DIR")"
ALLCLAWS_DIR="$(dirname "$FRAMEWORK_DIR")"

TIMESTAMP="$(date +%Y-%m-%dT%H:%M%S)"
FINDINGS_DIR="$FRAMEWORK_DIR/results/$TIMESTAMP"
FINDINGS_JSON="$FINDINGS_DIR/sandbox_findings.json"
FINDINGS_MD="$FINDINGS_DIR/sandbox_findings.md"

mkdir -p "$FINDINGS_DIR"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Container runtime (auto-detect)
if command -v podman >/dev/null 2>&1; then
    CONTAINER_CMD="podman"
    COMPOSE_CMD="podman-compose"
elif command -v docker >/dev/null 2>&1; then
    CONTAINER_CMD="docker"
    COMPOSE_CMD="docker-compose"
else
    echo "ERROR: No container runtime found (podman or docker required)"
    exit 1
fi

# Language-specific test functions
test_rust_project() {
    local platform=$1
    local container="${platform}-test"
    local findings="[]"

    echo -e "${BLUE}Testing Rust: $platform${NC}"

    # Check container exists and is running
    if ! $CONTAINER_CMD ps --format "{{.Names}}" | grep -q "^${container}$"; then
        echo "  ${RED}✗ Container not running${NC}"
        jq -n --arg p "$platform" \
            --arg category "container" \
            --arg severity "critical" \
            --arg message "Container not running" \
            --arg action "Start with: $COMPOSE_CMD up -d ${platform}-sandbox" \
            '{platform: $p, category: $category, severity: $severity, message: $message, action: $action}' | \
            jq --argjson findings "$findings" '$findings + [.]' > /tmp/findings.json
        findings=$(cat /tmp/findings.json)
        echo "$findings" > "$FINDINGS_JSON"
        return 1
    fi

    # Check Rust version
    local rust_version=$($CONTAINER_CMD exec "$container" cargo --version 2>/dev/null | grep -oP 'cargo \K[0-9.]+' || echo "unknown")
    echo "  Rust: $rust_version"

    # Check if Cargo.toml has edition2024 requirement
    if $CONTAINER_CMD exec "$container" grep -q 'edition = "2024"' /workspace/Cargo.toml 2>/dev/null; then
        local major=$(echo "$rust_version" | cut -d. -f1)
        local minor=$(echo "$rust_version" | cut -d. -f2)

        if [[ "$major" -lt 1 ]] || [[ "$major" -eq 1 && "$minor" -lt 84 ]]; then
            echo "  ${YELLOW}⚠ edition2024 requires Rust 1.84+${NC}"
            jq -n --arg p "$platform" \
                --arg category "build" \
                --arg severity "error" \
                --arg message "Rust $rust_version doesn't support edition2024 (requires 1.84+)" \
                --arg action "Update docker-compose.yml: rust:alpine (latest)" \
                '{platform: $p, category: $category, severity: $severity, message: $message, action: $action}' | \
                jq --argjson findings "$findings" '$findings + [.]' > /tmp/findings.json
            findings=$(cat /tmp/findings.json)
        fi
    fi

    # Check for web/dist/ (RustEmbed requirement)
    if $CONTAINER_CMD exec "$container" grep -q "RustEmbed" /workspace/src/**/*.rs 2>/dev/null; then
        if ! $CONTAINER_CMD exec "$container" test -d /workspace/web/dist; then
            echo "  ${YELLOW}⚠ web/dist/ missing for RustEmbed${NC}"
            jq -n --var p "$platform" \
                --arg category "build" \
                --arg severity "error" \
                --arg message "RustEmbed folder 'web/dist/' does not exist" \
                --arg action "Run 'npm run build' in web/ directory first" \
                '{platform: $p, category: $category, severity: $severity, message: $message, action: $action}' | \
                jq --argjson findings "$findings" '$findings + [.]' > /tmp/findings.json
            findings=$(cat /tmp/findings.json)
        fi
    fi

    # Try cargo check (quick compile check)
    echo "  Running cargo check..."
    if $CONTAINER_CMD exec "$container" cargo check 2>&1 | grep -q "error:"; then
        echo "  ${RED}✗ cargo check failed${NC}"
        jq -n --var p "$platform" \
            --arg category "build" \
            --arg severity "error" \
            --arg message "cargo check failed" \
            --arg action "Check Cargo.toml dependencies and Rust version" \
            '{platform: $p, category: $category, severity: $severity, message: $message, action: $action}' | \
            jq --argjson findings "$findings" '$findings + [.]' > /tmp/findings.json
        findings=$(cat /tmp/findings.json)
    else
        echo "  ${GREEN}✓ cargo check passed${NC}"
        jq -n --var p "$platform" \
            --arg category "build" \
            --arg severity "success" \
            --arg message "cargo check passed" \
            --arg action "" \
            '{platform: $p, category: $category, severity: $severity, message: $message, action: $action}' | \
            jq --argjson findings "$findings" '$findings + [.]' > /tmp/findings.json
        findings=$(cat /tmp/findings.json)
    fi

    echo "$findings" > "$FINDINGS_JSON"
}

test_go_project() {
    local platform=$1
    local container="${platform}-test"
    local findings=$(cat "$FINDINGS_JSON" 2>/dev/null || echo "[]")

    echo -e "${BLUE}Testing Go: $platform${NC}"

    if ! $CONTAINER_CMD ps --format "{{.Names}}" | grep -q "^${container}$"; then
        echo "  ${RED}✗ Container not running${NC}"
        return 1
    fi

    # Check Go version
    local go_version=$($CONTAINER_CMD exec "$container" go version 2>/dev/null | grep -oP 'go[0-9.]+' | head -1 || echo "unknown")
    echo "  Go: $go_version"

    # Check go.mod version requirement
    local required_version=$($CONTAINER_CMD exec "$container" grep -oP 'go \K[0-9.]+' /workspace/go.mod 2>/dev/null || echo "unknown")
    echo "  Required: go $required_version"

    # Parse versions for comparison
    local current_major=$(echo "$go_version" | sed 's/go//' | cut -d. -f1)
    local current_minor=$(echo "$go_version" | sed 's/go//' | cut -d. -f2)
    local required_major=$(echo "$required_version" | cut -d. -f1)
    local required_minor=$(echo "$required_version" | cut -d. -f2)

    if [[ "$current_major" -lt "$required_major" ]] || \
       [[ "$current_major" -eq "$required_major" && "$current_minor" -lt "$required_minor" ]]; then
        echo "  ${RED}✗ Go version mismatch${NC}"
        jq -n --var p "$platform" \
            --arg category "build" \
            --arg severity "error" \
            --arg message "go.mod requires go $required_version, sandbox has $go_version" \
            --arg action "Update docker-compose.yml: golang:1.$required_minor-alpine or golang:latest" \
            '{platform: $p, category: $category, severity: $severity, message: $message, action: $action}' | \
            jq --argjson findings "$findings" '$findings + [.]' > /tmp/findings.json
        findings=$(cat /tmp/findings.json)
    fi

    # Try go build
    echo "  Running go build..."
    if $CONTAINER_CMD exec "$container" go build -v ./... 2>&1 | grep -q "error"; then
        echo "  ${RED}✗ go build failed${NC}"
        jq -n --var p "$platform" \
            --arg category "build" \
            --arg severity "error" \
            --arg message "go build failed" \
            --arg action "Check go.mod dependencies and Go version" \
            '{platform: $p, category: $category, severity: $severity, message: $message, action: $action}' | \
            jq --argjson findings "$findings" '$findings + [.]' > /tmp/findings.json
        findings=$(cat /tmp/findings.json)
    else
        echo "  ${GREEN}✓ go build passed${NC}"
        jq -n --var p "$platform" \
            --arg category "build" \
            --arg severity "success" \
            --arg message "go build passed" \
            --arg action "" \
            '{platform: $p, category: $category, severity: $severity, message: $message, action: $action}' | \
            jq --argjson findings "$findings" '$findings + [.]' > /tmp/findings.json
        findings=$(cat /tmp/findings.json)
    fi

    echo "$findings" > "$FINDINGS_JSON"
}

test_python_project() {
    local platform=$1
    local container="${platform}-test"
    local findings=$(cat "$FINDINGS_JSON" 2>/dev/null || echo "[]")

    echo -e "${BLUE}Testing Python: $platform${NC}"

    if ! $CONTAINER_CMD ps --format "{{.Names}}" | grep -q "^${container}$"; then
        echo "  ${RED}✗ Container not running${NC}"
        return 1
    fi

    local python_version=$($CONTAINER_CMD exec "$container" python --version 2>&1 || echo "unknown")
    echo "  $python_version"

    # Check for pytest
    if ! $CONTAINER_CMD exec "$container" python -c "import pytest" 2>/dev/null; then
        echo "  ${YELLOW}⚠ pytest not installed${NC}"
        jq -n --var p "$platform" \
            --arg category "test" \
            --arg severity "warning" \
            --arg message "pytest not installed in sandbox" \
            --arg action "Add to requirements.txt or Dockerfile" \
            '{platform: $p, category: $category, severity: $severity, message: $message, action: $action}' | \
            jq --argjson findings "$findings" '$findings + [.]' > /tmp/findings.json
        findings=$(cat /tmp/findings.json)
    fi

    # Check if pyproject.toml or requirements.txt exists
    if $CONTAINER_CMD exec "$container" test -f /workspace/pyproject.toml; then
        echo "  Found pyproject.toml"
    elif $CONTAINER_CMD exec "$container" test -f /workspace/requirements.txt; then
        echo "  Found requirements.txt"
    else
        echo "  ${YELLOW}⚠ No Python manifest found${NC}"
        jq -n --var p "$platform" \
            --arg category "build" \
            --arg severity "warning" \
            --arg message "No pyproject.toml or requirements.txt" \
            --arg action "Add Python dependency manifest" \
            '{platform: $p, category: $category, severity: $severity, message: $message, action: $action}' | \
            jq --argjson findings "$findings" '$findings + [.]' > /tmp/findings.json
        findings=$(cat /tmp/findings.json)
    fi

    # Try importing main module
    local module_name=$(echo "$platform" | tr -d '-')
    if $CONTAINER_CMD exec "$container" python -c "import $module_name" 2>/dev/null; then
        echo "  ${GREEN}✓ Module import successful${NC}"
        jq -n --var p "$platform" \
            --arg category "build" \
            --arg severity "success" \
            --arg message "Module import successful" \
            --arg action "" \
            '{platform: $p, category: $category, severity: $severity, message: $message, action: $action}' | \
            jq --argjson findings "$findings" '$findings + [.]' > /tmp/findings.json
        findings=$(cat /tmp/findings.json)
    fi

    echo "$findings" > "$FINDINGS_JSON"
}

test_typescript_project() {
    local platform=$1
    local container="${platform}-test"
    local findings=$(cat "$FINDINGS_JSON" 2>/dev/null || echo "[]")

    echo -e "${BLUE}Testing TypeScript: $platform${NC}"

    if ! $CONTAINER_CMD ps --format "{{.Names}}" | grep -q "^${container}$"; then
        echo "  ${RED}✗ Container not running${NC}"
        return 1
    fi

    local node_version=$($CONTAINER_CMD exec "$container" node --version 2>/dev/null || echo "unknown")
    echo "  Node: $node_version"

    # Check package.json exists
    if $CONTAINER_CMD exec "$container" test -f /workspace/package.json; then
        echo "  Found package.json"

        # Check for build scripts
        if $CONTAINER_CMD exec "$container" grep -q '"build"' /workspace/package.json; then
            echo "  Build script found"

            # Check if node_modules exists
            if $CONTAINER_CMD exec "$container" test -d /workspace/node_modules; then
                echo "  ${GREEN}✓ node_modules present${NC}"
                jq -n --var p "$platform" \
                    --arg category "build" \
                    --arg severity "success" \
                    --arg message "Dependencies installed" \
                    --arg action "" \
                    '{platform: $p, category: $category, severity: $severity, message: $message, action: $action}' | \
                    jq --argjson findings "$findings" '$findings + [.]' > /tmp/findings.json
                findings=$(cat /tmp/findings.json)
            else
                echo "  ${YELLOW}⚠ node_modules missing (read-only mount)${NC}"
                jq -n --var p "$platform" \
                    --arg category "build" \
                    --arg severity "warning" \
                    --arg message "node_modules missing (read-only mount prevents npm install)" \
                    --arg action "Add writable volume for node_modules or use multi-stage build" \
                    '{platform: $p, category: $category, severity: $severity, message: $message, action: $action}' | \
                    jq --argjson findings "$findings" '$findings + [.]' > /tmp/findings.json
                findings=$(cat /tmp/findings.json)
            fi
        fi
    fi

    echo "$findings" > "$FINDINGS_JSON"
}

# Platform language mapping
declare -A PLATFORM_LANGUAGES=(
    ["openclaw"]="typescript"
    ["nanoclaw"]="typescript"
    ["quantumclaw"]="typescript"
    ["zeroclaw"]="rust"
    ["ironclaw"]="rust"
    ["goclaw"]="go"
    ["maxclaw"]="go"
    ["hiclaw"]="go"
    ["clawteam"]="python"
    ["nanobot"]="python"
    ["claw-ai-lab"]="python"
    ["hermes-agent"]="python"
    ["rtl-claw"]="verilog"
)

# Main test function
test_platform() {
    local platform=$1
    local lang=${PLATFORM_LANGUAGES[$platform]:-}

    case "$lang" in
        rust) test_rust_project "$platform" ;;
        go) test_go_project "$platform" ;;
        python) test_python_project "$platform" ;;
        typescript) test_typescript_project "$platform" ;;
        *) echo "  ${YELLOW}⚠ Unknown language: $lang${NC}" ;;
    esac
}

# Generate markdown report
generate_report() {
    local findings=$(cat "$FINDINGS_JSON" 2>/dev/null || echo "[]")

    cat > "$FINDINGS_MD" << EOF
# Sandbox Runtime Findings — $TIMESTAMP

## Summary

| Severity | Count |
|----------|-------|
| 🚨 Critical | $(echo "$findings" | jq '[.[] | select(.severity == "critical")] | length') |
| ❌ Error | $(echo "$findings" | jq '[.[] | select(.severity == "error")] | length') |
| ⚠️ Warning | $(echo "$findings" | jq '[.[] | select(.severity == "warning")] | length') |
| ✅ Success | $(echo "$findings" | jq '[.[] | select(.severity == "success")] | length') |

---

EOF

    # Group by platform
    for platform in "${!PLATFORM_LANGUAGES[@]}"; do
        local platform_findings=$(echo "$findings" | jq "[.[] | select(.platform == \"$platform\")]")

        if [ "$(echo "$platform_findings" | jq 'length')" -gt 0 ]; then
            echo "## $platform" >> "$FINDINGS_MD"
            echo "" >> "$FINDINGS_MD"

            echo "$platform_findings" | jq -r '.[] | |
                "### \(.category | ascii_upcase)\n" +
                "**Severity:** \(.severity)\n" +
                "**Message:** \(.message)\n" +
                (if .action != "" then "**Action:** `\(.action)`\n" else "" end)' >> "$FINDINGS_MD"
            echo "" >> "$FINDINGS_MD"
        fi
    done

    echo "Report saved to: $FINDINGS_MD"
}

# Main
echo "=========================================="
echo " AllClaws Sandbox Runtime Tests"
echo " $(date '+%Y-%m-%d %H:%M:%S')"
echo "=========================================="
echo ""

# Initialize empty findings
echo "[]" > "$FINDINGS_JSON"

# Get platforms to test
PLATFORMS=("${@:-}")
if [ ${#PLATFORMS[@]} -eq 0 ]; then
    PLATFORMS=("${!PLATFORM_LANGUAGES[@]}")
fi

# Run tests
for platform in "${PLATFORMS[@]}"; do
    echo ""
    test_platform "$platform"
done

# Generate report
echo ""
echo "=========================================="
echo " Generating Report..."
echo "=========================================="
generate_report

echo ""
echo "Findings saved to:"
echo "  JSON: $FINDINGS_JSON"
echo "  Markdown: $FINDINGS_MD"
echo ""
