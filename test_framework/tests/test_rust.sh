test_rust_manifest() {
    local dir="$1"
    if [ -f "$dir/Cargo.toml" ]; then
        echo "pass (Cargo.toml found)"
    else
        echo "FAIL: Cargo.toml not found"
        return 1
    fi
}

test_rust_workspace() {
    local dir="$1"
    if [ -f "$dir/Cargo.toml" ] && grep -q "workspace" "$dir/Cargo.toml" 2>/dev/null; then
        echo "pass (workspace detected)"
    else
        echo "pass (single crate)"
    fi
}

test_rust_crates() {
    local dir="$1"
    if [ -d "$dir/crates" ] || [ -d "$dir/src" ]; then
        count=$(find "$dir/crates" "$dir/src" -name "*.rs" 2>/dev/null | wc -l | tr -d ' ')
        echo "pass ($count Rust source files)"
    else
        echo "FAIL: no crates/ or src/ directory"
        return 1
    fi
}

test_rust_lock() {
    local dir="$1"
    if [ -f "$dir/Cargo.lock" ]; then
        echo "pass"
    else
        echo "FAIL: Cargo.lock not found"
        return 1
    fi
}

test_rust_clippy() {
    local dir="$1"
    if [ -f "$dir/clippy.toml" ] || [ -f "$dir/.clippy.toml" ]; then
        echo "pass (clippy config found)"
    else
        echo "WARN: no clippy.toml"
    fi
}

test_rust_ci() {
    local dir="$1"
    if [ -d "$dir/.github/workflows" ]; then
        count=$(find "$dir/.github/workflows" -name "*.yml" -o -name "*.yaml" 2>/dev/null | wc -l | tr -d ' ')
        echo "pass ($count GitHub Actions workflows)"
    else
        echo "WARN: no .github/workflows"
    fi
}

test_rust_deny() {
    local dir="$1"
    if [ -f "$dir/deny.toml" ] || [ -f "$dir/.cargo/deny.toml" ]; then
        echo "pass (cargo-deny config found)"
    else
        echo "WARN: no cargo-deny config"
    fi
}

test_rust_loc() {
    local dir="$1"
    source "$FRAMEWORK_DIR/tests/helpers/code_metrics.sh"
    local loc
    loc=$(count_lines "$dir" "rs")
    if [ -n "$loc" ] && [ "$loc" -gt 0 ] 2>/dev/null; then
        echo "pass ($loc lines of Rust)"
    else
        echo "WARN: could not count Rust LOC"
    fi
}
