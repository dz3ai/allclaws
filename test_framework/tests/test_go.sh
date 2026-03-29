test_go_module() {
    local dir="$1"
    if [ -f "$dir/go.mod" ]; then
        echo "pass (go.mod found)"
    else
        echo "FAIL: go.mod not found"
        return 1
    fi
}

test_go_source() {
    local dir="$1"
    count=$(find "$dir" \( -name ".git" -o -name "vendor" -o -name "node_modules" \) -prune -o -name "*.go" -print 2>/dev/null | wc -l | tr -d ' ')
    if [ "$count" -gt 0 ] 2>/dev/null; then
        echo "pass ($count Go source files)"
    else
        echo "FAIL: no Go source files"
        return 1
    fi
}

test_go_sum() {
    local dir="$1"
    if [ -f "$dir/go.sum" ]; then
        echo "pass"
    else
        echo "WARN: no go.sum"
    fi
}

test_go_ci() {
    local dir="$1"
    if [ -d "$dir/.github/workflows" ]; then
        count=$(find "$dir/.github/workflows" -name "*.yml" -o -name "*.yaml" 2>/dev/null | wc -l | tr -d ' ')
        echo "pass ($count GitHub Actions workflows)"
    else
        echo "WARN: no CI detected"
    fi
}

test_go_docker() {
    local dir="$1"
    if [ -f "$dir/Dockerfile" ]; then
        echo "pass (Dockerfile found)"
    else
        echo "WARN: no Dockerfile"
    fi
}

test_go_loc() {
    local dir="$1"
    source "$FRAMEWORK_DIR/tests/helpers/code_metrics.sh"
    local loc
    loc=$(count_lines "$dir" "go")
    if [ -n "$loc" ] && [ "$loc" -gt 0 ] 2>/dev/null; then
        echo "pass ($loc lines of Go)"
    else
        echo "WARN: could not count Go LOC"
    fi
}

test_go_makefile() {
    local dir="$1"
    if [ -f "$dir/Makefile" ] || [ -f "$dir/makefile" ]; then
        echo "pass"
    else
        echo "WARN: no Makefile"
    fi
}
