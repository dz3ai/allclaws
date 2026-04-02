#!/bin/bash
# Simple link checker for allclaws Jekyll blog
# Usage: ./scripts/test_links.sh [--build]

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
SITE_DIR="$PROJECT_ROOT/_site"

# Parse arguments
BUILD=false
SKIP_EXTERNAL=false

while [[ $# -gt 0 ]]; do
  case $1 in
    --build)
      BUILD=true
      shift
      ;;
    --skip-external)
      SKIP_EXTERNAL=true
      shift
      ;;
    *)
      echo "Unknown option: $1"
      exit 1
      ;;
  esac
done

# Build Jekyll site if requested
if [ "$BUILD" = true ]; then
  echo "Building Jekyll site..."
  cd "$PROJECT_ROOT"
  bundle exec jekyll build
fi

# Check if site directory exists
if [ ! -d "$SITE_DIR" ]; then
  echo "Error: Site directory not found: $SITE_DIR"
  echo "Run with --build to build the Jekyll site first"
  exit 1
fi

echo "Checking links in: $SITE_DIR"
echo

# Counters
total_links=0
valid_links=0
invalid_links=0
internal_broken=0
external_errors=0

# Temporary file for results
RESULTS_FILE=$(mktemp)
trap "rm -f $RESULTS_FILE" EXIT

# Function to check internal link
check_internal_link() {
  local link="$1"
  local source_file="$2"

  # Remove fragment
  local clean_link="${link%%\#*}"

  # Skip root
  if [ -z "$clean_link" ] || [ "$clean_link" = "/" ]; then
    return 0
  fi

  # Build target path
  if [[ "$clean_link" == /* ]]; then
    local target_path="$SITE_DIR${clean_link}"
  else
    local source_dir="$(dirname "$source_file")"
    local target_path="$source_dir/$clean_link"
  fi

  # Check if file exists
  if [ -f "$target_path" ]; then
    return 0
  fi

  # Try with .html extension
  if [ -f "$target_path.html" ]; then
    return 0
  fi

  # Check if it's a directory with index.html
  if [ -d "$target_path" ] && [ -f "$target_path/index.html" ]; then
    return 0
  fi

  return 1
}

# Find all HTML files
echo "Scanning HTML files..."
while IFS= read -r -d '' html_file; do
  relative_file="${html_file#$SITE_DIR/}"

  # Extract all href, src, and cite attributes
  while IFS= read -r line; do
    # Extract URL from various attributes
    for attr in href src cite; do
      if [[ "$line" =~ $attr=\"([^\"]+)\" ]] || [[ "$line" =~ $attr=\'([^\']+)\' ]]; then
        link="${BASH_REMATCH[1]}"
        ((total_links++))

        link_type="unknown"
        [[ "$line" =~ \<a ]] && link_type="a"
        [[ "$line" =~ \<link ]] && link_type="link"
        [[ "$line" =~ \<script ]] && link_type="script"
        [[ "$line" =~ \<img ]] && link_type="img"

        # Skip empty links, anchors, and special protocols
        if [[ -z "$link" ]] || [[ "$link" == "#"* ]] || \
           [[ "$link" == mailto:* ]] || [[ "$link" == tel:* ]] || \
           [[ "$link" == javascript:* ]] || [[ "$link" == data:* ]]; then
          ((valid_links++))
          continue
        fi

        # Check link type
        if [[ "$link" == https://* ]] || [[ "$link" == http://* ]]; then
          # External link
          if [ "$SKIP_EXTERNAL" = true ]; then
            ((valid_links++))
          else
            echo "[$relative_file] EXTERNAL: $link"
            # Note: We're not actually checking external links in this simple version
            # Just reporting them
          fi
        else
          # Internal link
          if check_internal_link "$link" "$html_file"; then
            ((valid_links++))
          else
            echo "[BROKEN] $relative_file -> $link"
            echo "  [$link_type] $link" >> "$RESULTS_FILE"
            ((invalid_links++))
            ((internal_broken++))
          fi
        fi
      fi
    done
  done < <(grep -E '(href|src|cite)=' "$html_file")
done < <(find "$SITE_DIR" -name "*.html" -print0)

# Print summary
echo
echo "================================================================================"
echo "LINK CHECK RESULTS"
echo "================================================================================"
echo "Total links found:     $total_links"
echo "Valid links:           $valid_links"
echo "Invalid internal links: $internal_broken"

if [ -f "$RESULTS_FILE" ] && [ -s "$RESULTS_FILE" ]; then
  echo
  echo "--------------------------------------------------------------------------------"
  echo "BROKEN LINKS DETAILS:"
  echo "--------------------------------------------------------------------------------"
  cat "$RESULTS_FILE"
fi

echo "================================================================================"

# Exit with error if broken links found
if [ $internal_broken -gt 0 ]; then
  echo "FAILED: Found $internal_broken broken internal link(s)"
  exit 1
else
  echo "SUCCESS: All internal links are valid!"
  exit 0
fi
