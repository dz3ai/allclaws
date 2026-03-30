#!/bin/bash

# Blog Site Validation Script
echo "🔍 Validating allclaws blog site..."
echo ""

BASE_URL="https://dz3ai.github.io/allclaws"
ERRORS=0
WARNINGS=0

# Function to check URL
check_url() {
  local url="$1"
  local name="$2"
  local response=$(curl -s -o /dev/null -w "%{http_code}" "$url")

  if [ "$response" = "200" ]; then
    echo "✅ $name: $response OK"
    return 0
  elif [ "$response" = "404" ]; then
    echo "❌ $name: $response NOT FOUND"
    ((ERRORS++))
    return 1
  else
    echo "⚠️  $name: $response"
    ((WARNINGS++))
    return 2
  fi
}

echo "=== Core Pages ==="
check_url "$BASE_URL/" "Homepage"
check_url "$BASE_URL/blog/" "Blog Index"
check_url "$BASE_URL/announcement/2026/03/30/welcome-to-allclaws.html" "Blog Post"
check_url "$BASE_URL/assets/css/style.css" "CSS Stylesheet"

echo ""
echo "=== Navigation Links ==="
# Extract and check links from homepage
echo "Checking homepage links..."
HOMEPAGE_LINKS=$(curl -s "$BASE_URL/" | grep -oP 'href="[^"]*"' | cut -d'"' -f2 | sort -u)

for link in $HOMEPAGE_LINKS; do
  if [[ $link == http* ]]; then
    # External link
    check_url "$link" "External: $link"
  elif [[ $link == /* ]]; then
    # Internal absolute link
    check_url "$BASE_URL$link" "Internal: $link"
  fi
done

echo ""
echo "=== Blog Page Links ==="
# Extract and check links from blog page
echo "Checking blog page links..."
BLOG_LINKS=$(curl -s "$BASE_URL/blog/" | grep -oP 'href="[^"]*"' | cut -d'"' -f2 | sort -u)

for link in $BLOG_LINKS; do
  if [[ $link == http* ]] && [[ $link != *jekyllrb.com ]]; then
    # External link (skip Jekyll docs)
    check_url "$link" "Blog link: $link"
  elif [[ $link == /* ]] && [[ $link != /feed.xml ]]; then
    # Internal link (skip feed)
    check_url "$BASE_URL$link" "Blog internal: $link"
  fi
done

echo ""
echo "=== Summary ==="
echo "Errors: $ERRORS"
echo "Warnings: $WARNINGS"

if [ $ERRORS -eq 0 ]; then
  echo "✅ All critical pages accessible!"
  exit 0
else
  echo "❌ Found $ERRORS errors that need fixing"
  exit 1
fi
