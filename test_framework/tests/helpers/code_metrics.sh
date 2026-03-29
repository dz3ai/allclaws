count_lines() {
    local dir="$1"
    local ext="$2"
    find "$dir" -maxdepth 4 \( -name ".git" -o -name "node_modules" -o -name "target" -o -name "vendor" -o -name "__pycache__" -o -name ".venv" -o -name "dist" -o -name "build" \) -prune -o -name "*.$ext" -type f -print 2>/dev/null | xargs wc -l 2>/dev/null | tail -1 | awk '{print $1}'
}
