# REASONIX.md — AllClaws

## Stack

- **Site** — Jekyll static site, GitHub Pages, `_config.yml` at root.
- **Test Framework** — Python-based (`test_framework/`), Docker/Podman sandboxed testing across 13+ AI agent platforms.
- **CI** — GitHub Actions: `agent-tests.yml` (static analysis + sandboxed runtime tests), `benchmark-suite.yml`, `jekyll-gh-pages.yml`.

## Layout

| Path | What lives there |
|---|---|
| `ironclaw/`, `goclaw/`, `clawteam/`, `hermes-agent/`, `zeroclaw/`, `maxclaw/`, `nanoclaw/`, `nanobot/`, `hiclaw/`, `openclaw/`, `claw-ai-lab/` | Self-contained AI agent platform — each has its own build system, test runner, language. |
| `coding-agents/` | CLI coding agents: `aider/` (Python), `reasonix/` (TypeScript), `copilot-cli/`. |
| `test_framework/` | Unified testing & benchmarking harness — config, evals, security tests, benchmark results. |
| `_posts/` | Jekyll blog posts (AI agent ecosystem research reports). |
| `_layouts/` | Jekyll HTML templates (`default.html`, `post.html`). |
| `architecture/` | Cross-platform comparison docs (runtime, MCP, governance, multi-agent). |
| `docs/` | Project docs: mission, roadmaps, validation reports, plans. |
| `scripts/` | Link checkers and site validation scripts (Shell + Python). |
| `openhuman/` | Rust-based "human digital twin" platform. |

## Commands

| Command | Action |
|---|---|
| `make build` | Build Jekyll site |
| `make serve` | Start Jekyll dev server |
| `make test` | Run link checker on built site |
| `make test-blog` | Blog link checker (no build) |
| `make validate` | Run all validation checks |
| `make clean` | Clean build artifacts (`_site`, cache) |

Per-platform build/test/run scripts live inside each subdirectory. See that subdirectory's own `Makefile`, `package.json`, `Cargo.toml`, `pyproject.toml`, or `go.mod`.

## Conventions

- **Blog posts** follow Jekyll frontmatter with `date`, `layout: post`, permalink `/blog/:year/:month/:day/:title/`.
- **Multilingual READMEs** — many platforms ship README translations (`README.zh-CN.md`, `README.ja.md`, etc.) alongside the English one.
- **CI timezone** — GitHub Actions sets `Asia/Shanghai (+0800)` for all jobs.
- **Docker sandboxing** — each platform tested in its own container image (`node:22-alpine`, `rust:alpine`, `golang:1.23-alpine`, `python:3.11-slim`).
- **Git hooks** — `ironclaw/` uses `.githooks/` (commit-msg, pre-commit, pre-push). Other platforms may vary.

## Watch out for

- **Monorepo sprawl** — each platform subdirectory has its own language, build system, test runner, and conventions. Do not assume a pattern from one applies across the board.
- **`test_framework/benchmark_results/`** is gitignored — CI artifacts, do not edit by hand.
- **`_posts/` are blog content, not code** — markdown with YAML frontmatter, not source files.
- **Root has no top-level package.json** — the root is a Jekyll site, not a Node project. `package.json` files live inside each subdirectory.
