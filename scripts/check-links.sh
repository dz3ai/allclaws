#!/bin/bash
# Link checker for AllClaws blog posts
# Validates internal and external links in markdown files

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Counters
TOTAL=0
VALID=0
INVALID=0
SKIPPED=0

echo "🔍 AllClaws Blog Link Checker"
echo "================================"
echo ""

# Check if file provided
if [ $# -eq 0 ]; then
    echo "Usage: $0 <markdown-file>"
    echo ""
    echo "Example:"
    echo "  $0 _posts/2026-04-02-ai-agent-ecosystem-report-march-2026.md"
    exit 1
fi

FILE="$1"

if [ ! -f "$FILE" ]; then
    echo -e "${RED}Error: File not found: $FILE${NC}"
    exit 1
fi

echo "Checking: $FILE"
echo ""

# Extract all markdown links
LINKS=$(grep -oP '\[([^\]]+)\]\(([^)]+)\)' "$FILE" | sed 's/.*](\(.*\))/\1/')

if [ -z "$LINKS" ]; then
    echo "No links found in file."
    exit 0
fi

echo "Found $(echo "$LINKS" | wc -l) links to check"
echo ""

# Check each link
while IFS= read -r link; do
    TOTAL=$((TOTAL + 1))

    # Skip empty links
    if [ -z "$link" ]; then
        continue
    fi

    # Internal relative links
    if [[ ! "$link" =~ ^https?:// ]]; then
        # Convert to absolute path relative to script location
        SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
        PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

        if [ -f "$PROJECT_ROOT/$link" ] || [ -d "$PROJECT_ROOT/$link" ]; then
            echo -e "${GREEN}✓${NC} $link (internal)"
            VALID=$((VALID + 1))
        else
            echo -e "${YELLOW}?${NC} $link (internal, not found - may be valid after Jekyll build)"
            SKIPPED=$((SKIPPED + 1))
        fi
    else
        # External links - do a quick check with curl
        HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" -L --connect-timeout 5 "$link" 2>/dev/null || echo "000")

        if [ "$HTTP_CODE" = "200" ] || [ "$HTTP_CODE" = "301" ] || [ "$HTTP_CODE" = "302" ]; then
            echo -e "${GREEN}✓${NC} $link ($HTTP_CODE)"
            VALID=$((VALID + 1))
        elif [ "$HTTP_CODE" = "404" ]; then
            echo -e "${RED}✗${NC} $link ($HTTP_CODE)"
            INVALID=$((INVALID + 1))
        elif [ "$HTTP_CODE" = "000" ]; then
            echo -e "${YELLOW}?${NC} $link (network error)"
            SKIPPED=$((SKIPPED + 1))
        else
            echo -e "${YELLOW}?${NC} $link ($HTTP_CODE)"
            SKIPPED=$((SKIPPED + 1))
        fi
    fi
done <<< "$LINKS"

echo ""
echo "================================"
echo "Summary:"
echo -e "  Total:   $TOTAL"
echo -e "${GREEN}  Valid:   $VALID${NC}"
echo -e "${RED}  Invalid: $INVALID${NC}"
echo -e "${YELLOW}  Skipped: $SKIPPED${NC}"
echo "================================"

if [ $INVALID -gt 0 ]; then
    exit 1
fi

exit 0
