# Benchmark System Python Rewrite

## Goal

Replace 4 bash benchmark scripts with a unified Python package under `test_framework/benchmark/`.

## Decisions

| Choice | Decision |
|--------|----------|
| Scope | All 4 scripts: runtime, static, sandbox, report |
| Structure | 5-file package with shared utils |
| CLI | argparse (stdlib) |
| Dependencies | stdlib + requests only |
| Container runtime | sandbox.py handles Docker/Podman separately |

## File Structure

```
test_framework/benchmark/
├── __init__.py          # version
├── cli.py               # argparse entry + dispatch (~80 lines)
├── utils.py             # shared: timing, RSS, statistics, JSON/MD output (~150 lines)
├── runtime.py           # local runtime benchmarks — cold start/memory/latency/size (~350 lines)
├── static.py            # static analysis — LOC/dependencies/file counts (~300 lines)
├── sandbox.py           # Docker/Podman container health checks (~250 lines)
└── report.py            # weekly report — aggregate N runs into summary (~200 lines)
```

## CLI Interface

```
python3 -m benchmark.cli <command> [options]

Commands:
  runtime       Local runtime benchmarks (replaces run_agent_runtime_benchmarks.sh)
  static        Static code analysis (replaces run_benchmarks.sh)
  sandbox       Container health checks (replaces run_sandbox_runtime_tests.sh)
  report        Weekly report aggregation (replaces weekly_report.sh)

Global options:
  --config PATH     Config file (default: ../config.json)
  --output-dir DIR  Output directory (default: ../benchmark_results/)
  --json-only       Output JSON only (default: JSON + Markdown)
  --platform P      Target platform(s), comma-separated
  --skip P          Skip platform(s)

Runtime options:
  --runs N          Sample count for timing metrics (default: 5)

Report options:
  --last N          Number of recent runs to aggregate (default: 5)
  --regression N    Regression threshold % (default: 20)
```

## Data Model

### Runtime Metric

```python
@dataclass
class Metric:
    platform: str
    metric: str       # e.g. "cold_start_time_ms"
    value: float
    unit: str         # e.g. "ms", "MB", "KB"
    notes: str = ""
    samples: list[float] | None = None  # raw samples if N > 1
    stats: dict | None = None           # mean, stddev, p50, p95 if N > 1
```

### Benchmark Result

```python
@dataclass
class BenchmarkResult:
    timestamp: str
    engine_version: str
    command: str        # "runtime", "static", "sandbox"
    toolchain: dict     # available tools detected
    metrics: list[Metric]
    skipped: list[dict] # {platform, reason}
```

## utils.py Shared Functions

- `time_command(cmd, timeout=60)` — run subprocess, return (exit_code, elapsed_ms)
- `measure_rss(cmd)` — peak RSS via /usr/bin/time -v or ps fallback
- `compute_stats(values)` — mean, stddev, min, max, p50, p95
- `size_of(path)` — du -k equivalent
- `detect_toolchain()` — check cargo/node/go/python3/time-v availability
- `load_config(path)` — read config.json
- `write_json(result, path)` — serialize BenchmarkResult to JSON
- `write_markdown(result, path)` — generate Markdown report
- `write_summary_table(result)` — sorted comparison table for GitHub Actions

## Platform Coverage (24 platforms)

All platforms from config.json supported. Missing directories gracefully skipped.

### Language-specific measurement:

| Language | Cold Start | Memory | Binary Size | Install Size | Build Proxy |
|----------|-----------|--------|-------------|--------------|-------------|
| Rust | `binary --help` | RSS via time -v | `du target/release/` | `du target/` | `cargo check` |
| Go | `binary --help` | RSS via time -v | `du bin/` | `du vendor/` | `go vet` |
| TypeScript | `node -e parse` | RSS via time -v | `du dist/` | `du node_modules/` | N/A |
| Python | `python -c import` | RSS with real package import | N/A | `du .venv/` | N/A |
| Verilog | Skipped | Skipped | Skipped | Skipped | Skipped |

## Sampling (N=5)

Only timing metrics are sampled: cold_start_time, response_latency, build_proxy_time, mod_download_time.

Size/count metrics measured once (deterministic).

Output includes per-metric: mean (primary value), stddev, p95 as separate metrics with `_stddev` and `_p95` suffixes.

## Output Compatibility

JSON output matches existing bash script structure (additive fields only):
- Top-level: timestamp, engine_version, metric_count, command, toolchain, sampling, metrics, skipped
- Per metric: platform, metric, value, unit, notes
- New: samples[], stats{} for sampled metrics

Markdown reports follow same table format for historical consistency.

## CI Integration

Workflow calls: `python3 -m benchmark.cli runtime --runs 5`
Weekly report: `python3 -m benchmark.cli report --last 5`

## Replaced Scripts

| Old bash script | New Python module |
|-----------------|-------------------|
| run_agent_runtime_benchmarks.sh (1177 lines) | benchmark.runtime |
| run_benchmarks.sh (~400 lines) | benchmark.static |
| run_sandbox_runtime_tests.sh (408 lines) | benchmark.sandbox |
| weekly_report.sh (not yet created) | benchmark.report |
