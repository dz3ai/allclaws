# Track Agent Updates Skill

**Purpose:** Automatically monitor AI agent project repositories for changes and update research documents.

## Overview

This skill monitors 8 AI agent platforms (OpenClaw, NanoClaw, IronClaw, GoClaw, ZeroClaw, Nanobot, ClawTeam, MaxClaw) tracked in the allclaws project, analyzes their changes, and updates research documentation with findings.

## What It Does

1. **Monitors submodules** - Checks git submodules for new commits, releases, and documentation updates
2. **Analyzes changes** - Identifies significant updates (breaking changes, security fixes, architecture changes)
3. **Generates reports** - Creates detailed monthly reports for each project
4. **Updates documentation** - Updates `docs/LATEST_UPDATES.md` with monthly summaries
5. **Creates blog posts** - Optionally generates blog posts for significant ecosystem changes
6. **Tracks state** - Remembers last check to avoid duplicate reporting

## Usage

### Basic Usage

Check all projects for updates since last run:

```bash
./scripts/track-agent-updates.sh
```

### Advanced Options

Check for changes since a specific date:

```bash
./scripts/track-agent-updates.sh --since "2026-03-01"
```

Generate report and create blog post for significant changes:

```bash
./scripts/track-agent-updates.sh --blog
```

Generate report only (don't update documents):

```bash
./scripts/track-agent-updates.sh --report-only
```

Force check all projects (ignore state cache):

```bash
./scripts/track-agent-updates.sh --force
```

### Help

```bash
./scripts/track-agent-updates.sh --help
```

## Output

### Reports

Individual project reports are saved to:
```
docs/reports/{project_name}_{YYYY-MM}.md
```

Example: `docs/reports/openclaw_2026-03.md`

Each report includes:
- Recent commits (last 20)
- New releases/tags
- Documentation updates

### Main Document Update

Updates `docs/LATEST_UPDATES.md` with monthly summary section including:
- Month header
- Key findings from all projects
- Links to detailed reports

### Blog Posts

When using `--blog` flag, creates:
```
_posts/{YYYY-MM-DD}-agent-ecosystem-update-{YYYY-MM}.md
```

Blog post includes:
- Monthly overview
- Significant findings
- Links to detailed reports
- Methodology notes

## Automation

### Cron Setup

Add to crontab for daily automatic tracking:

```bash
# Edit crontab
crontab -e

# Add daily check at 9 AM
0 9 * * * cd /path/to/allclaws && ./scripts/track-agent-updates.sh >> logs/tracker.log 2>&1
```

### Weekly Checks

```bash
# Every Monday at 9 AM
0 9 * * 1 cd /path/to/allclaws && ./scripts/track-agent-updates.sh --blog >> logs/tracker.log 2>&1
```

## Configuration

### Environment Variables

- **TRACKER_STATE_FILE**: Path to state tracking file (default: `.tracker-state.json`)

```bash
export TRACKER_STATE_FILE=/custom/path/.tracker-state.json
./scripts/track-agent-updates.sh
```

### Tracked Projects

Edit the `AGENT_PROJECTS` array in the script to add/remove projects:

```bash
declare -A AGENT_PROJECTS=(
  ["openclaw"]="OpenClaw - TypeScript AI Agent Platform"
  # Add more projects here
)
```

## State Tracking

The script maintains state in `.tracker-state.json`:

```json
{
  "last_check": "2026-03-31",
  "projects": {
    "openclaw": {
      "last_check": "2026-03-31",
      "last_commit": "abc123..."
    }
  }
}
```

This prevents duplicate reporting and enables incremental updates.

## Significant Change Detection

The script automatically detects significant changes by looking for keywords in commit messages:
- `breaking`
- `security`
- `CVE`
- `critical`
- `major`
- `release`
- `architecture`
- `performance`
- `vulnerability`

Significant changes are highlighted in reports and trigger blog post creation.

## Requirements

- **git** - For fetching repository updates
- **jq** - For JSON state file processing
- **bash** - Shell script execution
- **Git submodules** - Projects tracked as submodules

### Install jq

```bash
# Ubuntu/Debian
sudo apt-get install jq

# macOS
brew install jq

# Arch
sudo pacman -S jq
```

## Workflow

### Manual Research Workflow

1. **Weekly/Monthly run:**
   ```bash
   ./scripts/track-agent-updates.sh --blog --since "30 days ago"
   ```

2. **Review reports:**
   - Check `docs/reports/` for detailed project updates
   - Review `docs/LATEST_UPDATES.md` for ecosystem overview

3. **Blog post review:**
   - Edit generated blog post in `_posts/`
   - Add insights and analysis
   - Publish via git push

4. **Share findings:**
   - Commit reports and blog post
   - Push to GitHub
   - Auto-deploys to blog

## Integration with Research Process

This skill supports the allclaws research methodology:

1. **Data Collection** - Automatically gathers commits, releases, docs
2. **Analysis** - Identifies significant changes
3. **Documentation** - Updates research documents
4. **Publication** - Creates blog posts for dissemination

## Troubleshooting

### Submodule Not Initialized

```bash
cd /path/to/allclaws
git submodule update --init --recursive
```

### State File Corrupted

```bash
rm .tracker-state.json
./scripts/track-agent-updates.sh --force
```

### No Changes Detected

- Check if submodules are up to date: `git submodule status`
- Try force check: `--force` flag
- Check network connectivity to GitHub

### Permission Issues

```bash
chmod +x scripts/track-agent-updates.sh
```

## Examples

### Initial Setup Run

```bash
# First run - check last 30 days and create initial reports
./scripts/track-agent-updates.sh --since "30 days ago" --blog
```

### Daily Automated Check

```bash
# For cron - daily check since last run
./scripts/track-agent-updates.sh
```

### Monthly Research Update

```bash
# Comprehensive monthly update with blog post
./scripts/track-agent-updates.sh --blog --since "30 days ago"
```

### Quick Check Without Updates

```bash
# Generate report only, don't modify docs
./scripts/track-agent-updates.sh --report-only
```

## Output Format

### Console Output

```
[INFO] === Agent Updates Tracker ===
[INFO] Checking 8 agent projects...
[INFO]
[INFO] Checking for changes since: 7 days ago
[INFO]
[INFO] Analyzing openclaw: OpenClaw - TypeScript AI Agent Platform
[SUCCESS] Report generated: docs/reports/openclaw_2026-03.md
...
[INFO]
[INFO] === Summary ===
[SUCCESS] Found significant changes in some projects!
- **openclaw**: Found significant changes (check report for details)
- **ironclaw**: Found significant changes (check report for details)
[SUCCESS] Tracking complete!
```

## Future Enhancements

Potential improvements:

- [ ] GitHub API integration for issue/PR tracking
- [ ] Automated commit categorization (features, fixes, docs)
- [ ] Performance benchmark tracking
- [ ] Security vulnerability monitoring
- [ ] Dependency update tracking
- [ ] Release notes aggregation
- [ ] Comparison with previous month trends
- [ ] Visual charts and graphs

## Contributing

To extend this skill:

1. **Add new project**: Update `AGENT_PROJECTS` array
2. **Change detection logic**: Modify `analyze_changes()` function
3. **Report format**: Edit `generate_project_report()` function
4. **Significance criteria**: Update keywords in main logic

## License

Part of the allclaws project. See main project LICENSE.
