test_typescript_manifest() {
    local dir="$1"
    if [ -f "$dir/package.json" ]; then
        echo "pass (package.json found)"
    else
        echo "FAIL: package.json not found"
        return 1
    fi
}

test_typescript_lock() {
    local dir="$1"
    if [ -f "$dir/package-lock.json" ] || [ -f "$dir/pnpm-lock.yaml" ] || [ -f "$dir/yarn.lock" ] || [ -f "$dir/bun.lockb" ]; then
        echo "pass"
    else
        echo "WARN: no lockfile found"
    fi
}

test_typescript_source() {
    local dir="$1"
    count=$(find "$dir" \( -name ".git" -o -name "node_modules" -o -name "dist" \) -prune -o \( -name "*.ts" -o -name "*.tsx" \) -print 2>/dev/null | wc -l | tr -d ' ')
    if [ "$count" -gt 0 ] 2>/dev/null; then
        echo "pass ($count TypeScript files)"
    else
        echo "FAIL: no TypeScript source files"
        return 1
    fi
}

test_typescript_ci() {
    local dir="$1"
    if [ -d "$dir/.github/workflows" ]; then
        count=$(find "$dir/.github/workflows" -name "*.yml" -o -name "*.yaml" 2>/dev/null | wc -l | tr -d ' ')
        echo "pass ($count GitHub Actions workflows)"
    elif [ -f "$dir/.gitlab-ci.yml" ]; then
        echo "pass (GitLab CI)"
    else
        echo "WARN: no CI detected"
    fi
}

test_typescript_docker() {
    local dir="$1"
    if [ -f "$dir/Dockerfile" ] || [ -f "$dir/docker-compose.yml" ]; then
        echo "pass (Docker config found)"
    else
        echo "WARN: no Dockerfile"
    fi
}

test_typescript_loc() {
    local dir="$1"
    source "$FRAMEWORK_DIR/tests/helpers/code_metrics.sh"
    local loc
    loc=$(count_lines "$dir" "ts")
    if [ -n "$loc" ] && [ "$loc" -gt 0 ] 2>/dev/null; then
        echo "pass ($loc lines of TypeScript)"
    else
        echo "WARN: could not count TypeScript LOC"
    fi
}
