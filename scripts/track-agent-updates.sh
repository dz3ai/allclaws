#!/bin/bash

###############################################################################
# Track Agent Updates Skill
# Monitors AI agent project submodules for changes and updates research documents
#
# Usage:
#   ./scripts/track-agent-updates.sh [options]
#
# Options:
#   --since <date>          Only show changes since this date (default: last run)
#   --blog                  Create blog post for significant changes
#   --report-only           Only generate report, don't update documents
#   --force                 Force check all projects (ignore cache)
#   --show-branch-map       Print the parsed submodule branch map and exit
#   --validate-branch-map   Validate the branch map against .gitmodules and exit
#   --help                  Show this help message
#
# Environment:
#   TRACKER_STATE_FILE:  Path to state tracking file (default: .tracker-state.json)
#   TRACKER_BRANCH_MAP:  Path to branch map JSON (default: docs/reports/submodule-branch-map.json)
###############################################################################

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
STATE_FILE="${TRACKER_STATE_FILE:-$PROJECT_ROOT/.tracker-state.json}"
REPORT_DIR="$PROJECT_ROOT/docs/reports"
BLOG_DIR="$PROJECT_ROOT/_posts"
CURRENT_DATE=$(date +%Y-%m-%d)
CURRENT_MONTH=$(date +%Y-%m)

BRANCH_MAP_FILE="${TRACKER_BRANCH_MAP:-$REPORT_DIR/submodule-branch-map.json}"
declare -A BRANCH_MAP_DEFAULT=()
declare -A BRANCH_MAP_ACTIVE=()
declare -A BRANCH_MAP_STABLE=()
declare -A BRANCH_MAP_RELEASE=()
declare -A BRANCH_MAP_STATUS=()

# Agent projects being tracked
declare -A AGENT_PROJECTS=(
  ["openclaw"]="OpenClaw - TypeScript AI Agent Platform"
  ["nanoclaw"]="NanoClaw - Lightweight Python Agent"
  ["ironclaw"]="IronClaw - Rust-based Agent Framework"
  ["goclaw"]="GoClaw - Go-based Agent"
  ["zeroclaw"]="ZeroClaw - Zero-dependency Agent"
  ["nanobot"]="Nanobot - Multi-agent Research"
  ["clawteam"]="ClawTeam - OpenClaw Extensions"
  ["maxclaw"]="MaxClaw - Enhanced Agent Framework"
)

# CLI parsing
SINCE_DATE=""
CREATE_BLOG=false
REPORT_ONLY=false
FORCE_CHECK=false
SHOW_BRANCH_MAP=false
VALIDATE_BRANCH_MAP=false

while [[ $# -gt 0 ]]; do
  case $1 in
    --since)
      SINCE_DATE="$2"
      shift 2
      ;;
    --blog)
      CREATE_BLOG=true
      shift
      ;;
    --report-only)
      REPORT_ONLY=true
      shift
      ;;
    --force)
      FORCE_CHECK=true
      shift
      ;;
    --show-branch-map)
      SHOW_BRANCH_MAP=true
      shift
      ;;
    --validate-branch-map)
      VALIDATE_BRANCH_MAP=true
      shift
      ;;
    --help)
      grep '^#' "$0" | tail -n +2 | sed 's/^# //' | sed 's/^#//'
      exit 0
      ;;
    *)
      echo -e "${RED}Unknown option: $1${NC}"
      exit 1
      ;;
  esac
done

# Logging functions
log_info() {
  echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
  echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
  echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
  echo -e "${RED}[ERROR]${NC} $1"
}

load_branch_map() {
  if [[ ! -f "$BRANCH_MAP_FILE" ]]; then
    log_warning "Branch map not found: $BRANCH_MAP_FILE"
    return 0
  fi

  if ! jq -e '.submodules | type == "object"' "$BRANCH_MAP_FILE" >/dev/null 2>&1; then
    log_error "Invalid branch map JSON: $BRANCH_MAP_FILE"
    return 1
  fi

  local path default_branch active_branch stable release status
  while IFS=$'\t' read -r path default_branch active_branch stable release status; do
    [[ -z "$path" ]] && continue
    BRANCH_MAP_DEFAULT["$path"]="$default_branch"
    BRANCH_MAP_ACTIVE["$path"]="$active_branch"
    BRANCH_MAP_STABLE["$path"]="$stable"
    BRANCH_MAP_RELEASE["$path"]="$release"
    BRANCH_MAP_STATUS["$path"]="$status"
  done < <(jq -r '.submodules | to_entries[] | [.key, (.value.default_branch // ""), (.value.active_branch // ""), ((.value.stable_branches // []) | join(",") | if . == "" then "-" else . end), ((.value.release_patterns // []) | join(",") | if . == "" then "-" else . end), (.value.status // "")] | @tsv' "$BRANCH_MAP_FILE")

  log_info "Loaded branch map: ${#BRANCH_MAP_DEFAULT[@]} submodules from $BRANCH_MAP_FILE"
}

resolve_tracking_branch() {
  local project=$1
  local repo="$PROJECT_ROOT/$project"
  local branch="${BRANCH_MAP_ACTIVE[$project]:-}"

  [[ "$branch" == "-" ]] && branch=""

  if [[ "$branch" == *'*'* ]]; then
    branch=$(git -C "$repo" for-each-ref --sort=-committerdate \
      --format='%(refname:short)' "refs/remotes/origin/${branch}" 2>/dev/null | head -1)
  fi

  if [[ -z "$branch" || "$branch" == "-" ]]; then
    branch="${BRANCH_MAP_DEFAULT[$project]:-}"
    [[ "$branch" == "-" ]] && branch=""
  fi

  branch="${branch#origin/}"

  if [[ -n "$branch" ]] && git -C "$repo" rev-parse --verify --quiet "origin/$branch" >/dev/null 2>&1; then
    echo "origin/$branch"
    return 0
  fi

  local candidate
  for candidate in main master develop; do
    if git -C "$repo" rev-parse --verify --quiet "origin/$candidate" >/dev/null 2>&1; then
      echo "origin/$candidate"
      return 0
    fi
  done

  echo "origin/HEAD"
}

show_branch_map() {
  local p resolved
  printf '%-46s %-16s %-16s %-16s %-10s\n' "path" "default" "active" "resolved" "status"
  printf '%-46s %-16s %-16s %-16s %-10s\n' "----" "-------" "------" "--------" "------"
  for p in $(printf '%s\n' "${!BRANCH_MAP_DEFAULT[@]}" | sort); do
    if [[ -e "$PROJECT_ROOT/$p/.git" ]]; then
      resolved=$(resolve_tracking_branch "$p")
    else
      resolved="(not initialized)"
    fi
    printf '%-46s %-16s %-16s %-16s %-10s\n' \
      "$p" "${BRANCH_MAP_DEFAULT[$p]}" "${BRANCH_MAP_ACTIVE[$p]}" "$resolved" "${BRANCH_MAP_STATUS[$p]}"
  done
}

validate_branch_map() {
  if [[ ! -f "$BRANCH_MAP_FILE" ]]; then
    log_error "Branch map not found: $BRANCH_MAP_FILE"
    return 1
  fi

  if ! jq -e '.submodules | type == "object"' "$BRANCH_MAP_FILE" >/dev/null 2>&1; then
    log_error "Invalid branch map JSON: $BRANCH_MAP_FILE"
    return 1
  fi

  local expected mapped missing extra p
  expected=$(git -C "$PROJECT_ROOT" config --file .gitmodules --get-regexp path | awk '{print $2}' | sort)
  mapped=$(jq -r '.submodules | keys[]' "$BRANCH_MAP_FILE" | sort)

  missing=$(comm -23 <(printf '%s\n' "$expected") <(printf '%s\n' "$mapped"))
  extra=$(comm -13 <(printf '%s\n' "$expected") <(printf '%s\n' "$mapped"))

  if [[ -n "$missing" ]]; then
    while IFS= read -r p; do [[ -n "$p" ]] && log_warning "Unmapped submodule: $p"; done <<< "$missing"
  fi
  if [[ -n "$extra" ]]; then
    while IFS= read -r p; do [[ -n "$p" ]] && log_warning "Unknown path in map: $p"; done <<< "$extra"
  fi

  log_success "Branch map valid: ${#BRANCH_MAP_DEFAULT[@]} entries, $(printf '%s\n' "$expected" | wc -l) submodules in .gitmodules"
}

# Initialize state file
init_state() {
  if [[ ! -f "$STATE_FILE" ]]; then
    log_info "Initializing state file..."
    cat > "$STATE_FILE" << EOF
{
  "last_check": "$CURRENT_DATE",
  "projects": {}
}
EOF
    log_success "State file initialized at $STATE_FILE"
  fi
}

# Get last check date for a project
get_last_check() {
  local project=$1
  if [[ -f "$STATE_FILE" ]]; then
    jq -r ".projects.\"$project\".last_check // \"\"" "$STATE_FILE" 2>/dev/null || echo ""
  fi
}

# Update last check date for a project
update_last_check() {
  local project=$1
  local last_commit=$2
  local temp_file=$(mktemp)

  if [[ -f "$STATE_FILE" ]]; then
    jq --arg project "$project" \
       --arg date "$CURRENT_DATE" \
       --arg commit "$last_commit" \
       '.projects[$project] = {"last_check": $date, "last_commit": $commit}' \
       "$STATE_FILE" > "$temp_file"
    mv "$temp_file" "$STATE_FILE"
  fi
}

# Check if submodule exists and is accessible
check_submodule() {
  local project=$1
  local project_path="$PROJECT_ROOT/$project"

  if [[ ! -d "$project_path" ]]; then
    log_warning "Submodule $project not found. Initializing..."
    cd "$PROJECT_ROOT"
    git submodule update --init "$project" || {
      log_error "Failed to initialize submodule $project"
      return 1
    }
  fi

  if [[ ! -e "$project_path/.git" ]]; then
    log_warning "Submodule $project not initialized. Initializing..."
    cd "$PROJECT_ROOT"
    git submodule update --init "$project" || {
      log_error "Failed to initialize submodule $project"
      return 1
    }
  fi

  return 0
}

# Fetch latest changes for a project
fetch_changes() {
  local project=$1
  local project_path="$PROJECT_ROOT/$project"
  local branch fetch_timeout="${TRACKER_FETCH_TIMEOUT:-120}"

  check_submodule "$project" || return 1

  branch=$(resolve_tracking_branch "$project")
  branch="${branch#origin/}"

  cd "$project_path"

  timeout "$fetch_timeout" git fetch --tags origin "$branch" >/dev/null 2>&1 || {
    log_error "Failed to fetch updates for $project ($branch, ${fetch_timeout}s)"
    return 1
  }

  return 0
}

# Get commits since last check
get_commits() {
  local project=$1
  local since_date=$2
  local project_path="$PROJECT_ROOT/$project"
  local branch ref chosen=""

  branch=$(resolve_tracking_branch "$project")

  for ref in "$branch" origin/main origin/master; do
    [[ -z "$ref" ]] && continue
    if git -C "$project_path" rev-parse --verify --quiet "$ref" >/dev/null 2>&1; then
      chosen="$ref"
      break
    fi
  done
  chosen="${chosen:-$branch}"

  cd "$project_path"

  if [[ -n "$since_date" ]]; then
    git log --since="$since_date" --pretty=format:"%H|%ai|%s|%an" "$chosen" 2>/dev/null
  else
    git log --pretty=format:"%H|%ai|%s|%an" "$chosen" 2>/dev/null | head -20
  fi
}

# Get recent releases
get_releases() {
  local project=$1
  local project_path="$PROJECT_ROOT/$project"

  cd "$project_path"

  # Get git tags as releases
  git tag --sort=-version:refname | head -5 | while read -r tag; do
    local tag_date=$(git log -1 --format=%ai "$tag" 2>/dev/null || echo "unknown")
    local tag_message=$(git tag -l "$tag" --format='%(contents:subject)' 2>/dev/null || echo "$tag")
    echo "$tag|$tag_date|$tag_message"
  done
}

# Get documentation updates
get_doc_updates() {
  local project=$1
  local since_date=$2
  local project_path="$PROJECT_ROOT/$project"
  local branch

  [[ -z "$since_date" ]] && return 0

  cd "$project_path"

  branch=$(resolve_tracking_branch "$project")

  git log --since="$since_date" --name-only --pretty=format:'%H|%ai' "$branch" 2>/dev/null | \
    awk -F'|' '
      /^[0-9a-f]{40}\|/ { hash=$1; date=$2; next }
      /(^|\/)(node_modules|\.git)\// { next }
      /(\.md$|README|CHANGELOG)/ && !seen[$0]++ { print $0"|"date"|"hash }
    '
}

# Analyze changes for significance
analyze_changes() {
  local commits=$1
  local significant=false

  while IFS='|' read -r hash date subject author; do
    # Check for significant keywords
    local keywords=("breaking" "security" "CVE" "critical" "major" "release" "architecture" "performance" "vulnerability")

    for keyword in "${keywords[@]}"; do
      if [[ "${subject,,}" == *"$keyword"* ]]; then
        significant=true
        break
      fi
    done

    if [[ "$significant" == "true" ]]; then
      break
    fi
  done <<< "$commits"

  echo "$significant"
}

# Generate report for a project
generate_project_report() {
  local project=$1
  local since_date=$2
  local project_description="${AGENT_PROJECTS[$project]}"

  log_info "Analyzing $project: $project_description"

  # Get changes
  local commits=$(get_commits "$project" "$since_date")
  local releases=$(get_releases "$project")
  local doc_updates=$(get_doc_updates "$project" "$since_date")

  # Check if there are any changes
  if [[ -z "$commits" && -z "$releases" && -z "$doc_updates" ]]; then
    log_info "No changes found for $project"
    return 0
  fi

  # Generate report
  local report="$REPORT_DIR/${project}_${CURRENT_MONTH}.md"

  mkdir -p "$REPORT_DIR"

  cat > "$report" << EOF
# ${project_description} - Update Report

**Generated:** $(date +%Y-%m-%d\ %H:%M:%S)
**Tracking Period:** ${since_date:-Since beginning} to $(date +%Y-%m-%d)

EOF

  # Add commits section
  if [[ -n "$commits" ]]; then
    cat >> "$report" << EOF
## Recent Commits

EOF

    local commit_count=0
    while IFS='|' read -r hash date subject author; do
      if [[ -n "$hash" ]]; then
        cat >> "$report" << EOF
### ${subject:0:100}
- **Date:** ${date:0:10}
- **Author:** $author
- **Commit:** $hash
EOF
        commit_count=$((commit_count + 1))
        if [[ $commit_count -ge 20 ]]; then
          echo "... and more (showing recent 20 commits)" >> "$report"
          break
        fi
      fi
    done <<< "$commits"
  fi

  # Add releases section
  if [[ -n "$releases" ]]; then
    cat >> "$report" << EOF

## Recent Releases

EOF
    while IFS='|' read -r tag date message; do
      cat >> "$report" << EOF
### $tag
- **Date:** ${date:0:10}
- **Description:** $message
EOF
    done <<< "$releases"
  fi

  # Add documentation updates
  if [[ -n "$doc_updates" ]]; then
    cat >> "$report" << EOF

## Documentation Updates

EOF
    while IFS='|' read -r file date commit; do
      cat >> "$report" << EOF
- **$file** - Updated: ${date:0:10}
EOF
    done <<< "$doc_updates"
  fi

  log_success "Report generated: $report"
}

# Update main LATEST_UPDATES document
update_latest_updates() {
  local update_month="$1"
  local significant_findings="$2"

  if [[ "$REPORT_ONLY" == "true" ]]; then
    log_info "Report-only mode: skipping LATEST_UPDATES.md update"
    return 0
  fi

  local latest_file="$PROJECT_ROOT/docs/LATEST_UPDATES.md"

  if [[ ! -f "$latest_file" ]]; then
    log_warning "LATEST_UPDATES.md not found. Skipping update."
    return 0
  fi

  log_info "Updating $latest_file..."

  # Check if monthly section already exists
  if grep -q "## $update_month" "$latest_file"; then
    log_info "Monthly section for $update_month already exists. Skipping."
    return 0
  fi

  # Add new monthly section at the top
  local temp_file=$(mktemp)

  # Extract header
  head -n 8 "$latest_file" > "$temp_file"

  # Add new section
  cat >> "$temp_file" << EOF

## $update_month

_Updated on $(date +%Y-%m-%d)_

**Key Findings:**
$significant_findings

---

EOF

  # Add rest of the file
  tail -n +9 "$latest_file" >> "$temp_file"

  mv "$temp_file" "$latest_file"

  log_success "Updated LATEST_UPDATES.md with $update_month section"
}

# Create blog post for significant changes
create_blog_post() {
  local month=$1
  local findings=$2

  if [[ "$CREATE_BLOG" != "true" ]]; then
    return 0
  fi

  local blog_file="$BLOG_DIR/${CURRENT_DATE}-agent-ecosystem-update-${month}.md"

  mkdir -p "$BLOG_DIR"

  cat > "$blog_file" << EOF
---
layout: post
title: "AI Agent Ecosystem Update: ${month}"
date: $(date +%Y-%m-%d\ %H:%M:%S) +0800
author: Danny Zeng
categories: [Monthly Update]
tags: [AI agents, ecosystem, research, ${month}]
---

This month's update covers significant developments across the personal AI agent ecosystem we're tracking in the allclaws project.

## Overview

${findings}

## Detailed Analysis

For comprehensive analysis of each platform, check out the detailed reports in the [docs/reports](https://github.com/dz3ai/allclaws/tree/main/docs/reports) directory.

## Stay Updated

Follow our research on [GitHub](https://github.com/dz3ai/allclaws) or subscribe to the [RSS feed](https://dz3ai.github.io/allclaws/feed.xml).

---

*Methodology: We track 8 AI agent platforms through their git repositories, analyzing commits, releases, and documentation updates to identify trends and innovations.*
EOF

  log_success "Blog post created: $blog_file"
}

# Main execution
main() {
  log_info "=== Agent Updates Tracker ==="
  log_info "Checking ${#AGENT_PROJECTS[@]} agent projects..."
  log_info ""

  load_branch_map

  if [[ "$SHOW_BRANCH_MAP" == "true" ]]; then
    show_branch_map
    return 0
  fi

  if [[ "$VALIDATE_BRANCH_MAP" == "true" ]]; then
    validate_branch_map
    return 0
  fi

  # Initialize state
  init_state

  # Determine since date
  local check_since="$SINCE_DATE"
  if [[ -z "$check_since" && "$FORCE_CHECK" != "true" ]]; then
    # Use last check from state file
    check_since=$(jq -r '.last_check // "7 days ago"' "$STATE_FILE" 2>/dev/null || echo "7 days ago")
  fi

  if [[ -z "$check_since" ]]; then
    check_since="30 days ago"
  fi

  log_info "Checking for changes since: $check_since"
  log_info ""

  # Track significant findings
  local all_significant=""

  # Check each project
  for project in "${!AGENT_PROJECTS[@]}"; do
    local last_commit=""
    local project_changed=false

    # Fetch changes
    if fetch_changes "$project"; then
      # Generate report
      generate_project_report "$project" "$check_since"

      # Check if project has changes
      local commits=$(get_commits "$project" "$check_since")
      if [[ -n "$commits" ]]; then
        project_changed=true
        last_commit=$(echo "$commits" | head -1 | cut -d'|' -f1)

        # Check for significance
        local significant=$(analyze_changes "$commits")
        if [[ "$significant" == "true" ]]; then
          all_significant+="\n- **$project**: Found significant changes (check report for details)"
        fi
      fi

      # Update state
      if [[ "$project_changed" == "true" && -n "$last_commit" ]]; then
        update_last_check "$project" "$last_commit"
      fi
    fi
  done

  # Update main tracking date
  local temp_file=$(mktemp)
  jq --arg date "$CURRENT_DATE" '.last_check = $date' "$STATE_FILE" > "$temp_file"
  mv "$temp_file" "$STATE_FILE"

  log_info ""
  log_info "=== Summary ==="

  if [[ -n "$all_significant" ]]; then
    log_success "Found significant changes in some projects!"
    echo -e "${GREEN}$all_significant${NC}"

    # Update documents
    update_latest_updates "$CURRENT_MONTH" "$all_significant"

    # Create blog post if requested
    create_blog_post "$CURRENT_MONTH" "$all_significant"
  else
    log_info "No significant changes detected across all projects"
  fi

  log_success "Tracking complete!"
  log_info "Reports saved to: $REPORT_DIR/"
  if [[ "$CREATE_BLOG" == "true" ]]; then
    log_info "Blog post: $BLOG_DIR/${CURRENT_DATE}-agent-ecosystem-update-${CURRENT_MONTH}.md"
  fi
}

# Run main function
main "$@"
