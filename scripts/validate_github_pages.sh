#!/bin/bash
# GitHub Pages deployment validator
# Checks deployed site for 404 errors and common config issues

BASE_URL="${1:-https://dz3ai.github.io/allclaws}"
FAILED=0
PASSED=0

echo "=============================================================="
echo "GitHub Pages Validation: $BASE_URL"
echo "=============================================================="
echo

# Function to check URL
check_url() {
    local url="$1"
    local name="$2"

    echo -n "Checking [$name]: $url ... "

    status=$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 -L "$url" 2>/dev/null || echo "000")

    if [ "$status" = "200" ] || [ "$status" = "301" ] || [ "$status" = "302" ]; then
        echo "✓ OK ($status)"
        ((PASSED++))
        return 0
    else
        echo "✗ FAILED ($status)"
        ((FAILED++))
        return 1
    fi
}

# Function to extract and check links from a page
check_page_links() {
    local page="$1"
    local max_links="${2:-10}"

    echo
    echo "Checking links from: $BASE_URL$page"
    echo "--------------------------------------------------------------"

    # Get page content
    content=$(curl -s -L --max-time 10 "$BASE_URL$page" 2>/dev/null)
    if [ -z "$content" ]; then
        echo "  ✗ Failed to load page"
        ((FAILED++))
        return 1
    fi

    # Extract href links
    links=$(echo "$content" | grep -oP 'href="[^"]*"' | cut -d'"' -f2 | head -n "$max_links")

    count=0
    for link in $links; do
        # Skip anchors, mailto, tel, javascript
        [[ "$link" =~ ^# ]] && continue
        [[ "$link" =~ ^mailto: ]] && continue
        [[ "$link" =~ ^tel: ]] && continue
        [[ "$link" =~ ^javascript: ]] && continue

        # Build full URL for relative links
        if [[ "$link" =~ ^https?:// ]]; then
            full_url="$link"
        elif [[ "$link" =~ ^// ]]; then
            full_url="https:$link"
        else
            full_url="$BASE_URL$link"
        fi

        # Only check internal links
        if [[ "$full_url" =~ ^$BASE_URL ]]; then
            count=$((count + 1))
            echo -n "  [$count] $link ... "

            status=$(curl -s -o /dev/null -w "%{http_code}" -L --max-time 5 "$full_url" 2>/dev/null || echo "000")

            if [ "$status" = "200" ]; then
                echo "✓"
                ((PASSED++))
            else
                echo "✗ ($status)"
                ((FAILED++))
            fi
        fi
    done
}

# Function to diagnose config issues
diagnose_issues() {
    echo
    echo "Configuration Diagnosis:"
    echo "--------------------------------------------------------------"

    # Check if baseurl might be wrong
    base_status=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL" 2>/dev/null)
    if [ "$base_status" = "404" ]; then
        echo "  ⚠️  Root URL returns 404"
        echo "      → Check GitHub Pages source branch settings"
    fi

    # Check blog index
    blog_status=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/blog/" 2>/dev/null)
    if [ "$blog_status" = "404" ]; then
        echo "  ⚠️  /blog/ returns 404"
        echo "      → Check permalink setting in _config.yml"
    fi

    # Extract baseurl from patterns
    if [[ "$BASE_URL" =~ ^https://[^/]+/([^/]+) ]]; then
        repo_name="${BASH_REMATCH[1]}"

        # Check if links work without repo name (wrong baseurl)
        if [ "$blog_status" != "200" ]; then
            no_repo_url="https://$(echo "$BASE_URL" | sed 's|https://||' | cut -d'/' -f1)/blog/"
            no_repo_status=$(curl -s -o /dev/null -w "%{http_code}" "$no_repo_url" 2>/dev/null)

            if [ "$no_repo_status" = "200" ]; then
                echo "  ⚠️  LINKS MISSING BASEURL DETECTED"
                echo "      → /blog/ works at $no_repo_url"
                echo "      → But fails at $BASE_URL/blog/"
                echo ""
                echo "      FIX: Add | relative_url filter to all links:"
                echo "        Wrong: href=\"{{ post.url }}\""
                echo "        Right: href=\"{{ post.url | relative_url }}\""
                echo ""
                echo "      FIX: Check _config.yml has:"
                echo "        baseurl: \"/$repo_name\""
            fi
        fi
    fi
}

# Run checks
check_url "$BASE_URL" "Root"
check_url "$BASE_URL/blog/" "Blog Index"
check_url "$BASE_URL/feed.xml" "RSS Feed"

# Check a sample post if exists
check_url "$BASE_URL/blog/2026/04/02/claude-code-leak-creative-projects/" "Sample Post"

# Check links from blog page
check_page_links "/blog/" 15

# Diagnose configuration issues
diagnose_issues

# Summary
echo
echo "=============================================================="
echo "Summary:"
echo "  Passed: $PASSED"
echo "  Failed: $FAILED"
echo "=============================================================="

if [ $FAILED -eq 0 ]; then
    echo "✓ All checks passed!"
    exit 0
else
    echo "✗ Some checks failed - see details above"
    exit 1
fi
