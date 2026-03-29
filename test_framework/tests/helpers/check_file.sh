#!/bin/bash
DIR="$1"
PATTERN="$2"

if [ -z "$DIR" ] || [ ! -d "$DIR" ]; then
    echo "SKIP: directory not found: $DIR"
    exit 77
fi

match=$(find "$DIR" -maxdepth 1 -name "*${PATTERN}*" 2>/dev/null | head -1)
if [ -n "$match" ]; then
    echo "pass"
else
    echo "FAIL: no file matching '$PATTERN' found in $DIR"
    exit 1
fi
