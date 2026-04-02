# Test Scripts

This directory contains various test and validation scripts for the allclaws project.

## Link Checkers

### `check_blog_links.py` (Recommended)

A lightweight link checker for blog-related files only. No build or external dependencies required.

**Features:**
- Checks `index.md`, `blog.md`, `_layouts/`, and `_posts/`
- Validates internal links and markdown references
- Lists all external links
- Skips Jekyll Liquid template variables automatically

**Usage:**
```bash
python3 scripts/check_blog_links.py
# Or using make:
make test-blog
```

**Output:**
```
Found 8 blog files to check

Checking: _layouts/default.html
Checking: _layouts/post.html
Checking: _posts/2026-03-30-welcome-to-allclaws.md
...

============================================================
BLOG LINK CHECK RESULTS
============================================================
Total links checked: 28
Internal links: 1
External links: 27
Valid links: 28
Invalid links: 0
```

### `test_links.py`

A comprehensive link checker for the built Jekyll site. Requires Python dependencies.

**Dependencies:**
```bash
pip install requests beautifulsoup4
```

**Usage:**
```bash
python3 scripts/test_links.py [--build] [--skip-external]
```

**Options:**
- `--build` - Build Jekyll site before checking
- `--skip-external` - Skip external link validation
- `--base-url` - Specify base URL (default: https://dz3ai.github.io/allclaws/)

### `test_links.sh`

A shell-based link checker that doesn't require Python dependencies.

**Usage:**
```bash
./scripts/test_links.sh [--build] [--skip-external]
```

## Makefile Targets

- `make test-blog` - Run blog link checker (no build required)
- `make test-build` - Build Jekyll site then check links
- `make build` - Build Jekyll site
- `make serve` - Start Jekyll development server
- `make clean` - Clean build artifacts

## CI/CD Integration

To add link checking to your CI/CD pipeline:

```yaml
# .github/workflows/test.yml example
- name: Check blog links
  run: python3 scripts/check_blog_links.py
```
