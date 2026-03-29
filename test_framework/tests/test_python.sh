test_python_manifest() {
    local dir="$1"
    if [ -f "$dir/pyproject.toml" ] || [ -f "$dir/setup.py" ] || [ -f "$dir/setup.cfg" ]; then
        echo "pass"
    else
        echo "FAIL: no Python package manifest found"
        return 1
    fi
}

test_python_source() {
    local dir="$1"
    count=$(find "$dir" \( -name ".git" -o -name "node_modules" -o -name "__pycache__" -o -name ".venv" -o -name "venv" \) -prune -o -name "*.py" -print 2>/dev/null | wc -l | tr -d ' ')
    if [ "$count" -gt 0 ] 2>/dev/null; then
        echo "pass ($count Python source files)"
    else
        echo "FAIL: no Python source files"
        return 1
    fi
}

test_python_docker() {
    local dir="$1"
    if [ -f "$dir/Dockerfile" ] || [ -f "$dir/docker-compose.yml" ]; then
        echo "pass (Docker config found)"
    else
        echo "WARN: no Dockerfile"
    fi
}

test_python_ci() {
    local dir="$1"
    if [ -d "$dir/.github/workflows" ]; then
        count=$(find "$dir/.github/workflows" -name "*.yml" -o -name "*.yaml" 2>/dev/null | wc -l | tr -d ' ')
        echo "pass ($count GitHub Actions workflows)"
    else
        echo "WARN: no CI detected"
    fi
}

test_python_loc() {
    local dir="$1"
    source "$FRAMEWORK_DIR/tests/helpers/code_metrics.sh"
    local loc
    loc=$(count_lines "$dir" "py")
    if [ -n "$loc" ] && [ "$loc" -gt 0 ] 2>/dev/null; then
        echo "pass ($loc lines of Python)"
    else
        echo "WARN: could not count Python LOC"
    fi
}

test_python_tests_dir() {
    local dir="$1"
    if [ -d "$dir/tests" ] || [ -d "$dir/test" ]; then
        count=$(find "$dir/tests" "$dir/test" -name "*.py" 2>/dev/null | wc -l | tr -d ' ')
        echo "pass ($count test files)"
    else
        echo "WARN: no tests/ directory"
    fi
}
