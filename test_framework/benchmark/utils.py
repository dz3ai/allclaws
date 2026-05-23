"""Shared utilities for the AllClaws benchmark suite."""

import json
import math
import os
import shutil
import subprocess
import time
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


@dataclass
class Metric:
    """A single benchmark measurement."""
    platform: str
    metric: str
    value: float
    unit: str
    notes: str = ""
    samples: Optional[list] = None
    stats: Optional[dict] = None


@dataclass
class BenchmarkResult:
    """Complete benchmark run result."""
    timestamp: str
    engine_version: str
    command: str
    toolchain: dict
    metrics: list = field(default_factory=list)
    skipped: list = field(default_factory=list)

    def to_json_dict(self) -> dict:
        """Serialize for JSON output (backward-compatible with bash script format)."""
        return {
            "timestamp": self.timestamp,
            "engine_version": self.engine_version,
            "metric_count": len(self.metrics),
            "skipped_count": len(self.skipped),
            "command": self.command,
            "toolchain": self.toolchain,
            "metrics": [_metric_to_dict(m) for m in self.metrics],
            "skipped": self.skipped,
        }


def _metric_to_dict(m: Metric) -> dict:
    """Serialize a Metric to JSON-compatible dict."""
    d = {"platform": m.platform, "metric": m.metric, "value": m.value, "unit": m.unit}
    if m.notes:
        d["notes"] = m.notes
    if m.samples is not None:
        d["samples"] = m.samples
    if m.stats is not None:
        d["stats"] = m.stats
    return d


def detect_toolchain() -> dict:
    """Check availability of build tools and utilities."""
    checks = {
        "python3": ["python3", "--version"],
        "cargo": ["cargo", "--version"],
        "node": ["node", "--version"],
        "go": ["go", "version"],
        "docker": ["docker", "--version"],
        "podman": ["podman", "--version"],
        "ps": ["ps", "--version"],
    }
    result = {}
    for name, cmd in checks.items():
        try:
            subprocess.run(cmd, capture_output=True, timeout=5)
            result[name] = True
        except (OSError, subprocess.TimeoutExpired):
            result[name] = False
    # /usr/bin/time -v needs special check
    result["time_v"] = False
    try:
        out = subprocess.run(
            ["/usr/bin/time", "-v", "true"],
            capture_output=True, timeout=5, text=True,
        )
        if "Maximum resident" in out.stderr:
            result["time_v"] = True
    except (OSError, subprocess.TimeoutExpired):
        pass
    return result


def time_command(cmd: list, timeout: int = 60) -> tuple:
    """Run a subprocess command and return (exit_code, elapsed_ms).

    Uses time.perf_counter_ns() for sub-millisecond precision.
    """
    start = time.perf_counter_ns()
    try:
        proc = subprocess.run(
            cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            timeout=timeout,
        )
        elapsed_ms = (time.perf_counter_ns() - start) / 1_000_000
        return (proc.returncode, elapsed_ms)
    except subprocess.TimeoutExpired:
        elapsed_ms = (time.perf_counter_ns() - start) / 1_000_000
        return (-1, elapsed_ms)
    except OSError:
        return (-1, 0.0)


def measure_rss(cmd: list) -> tuple:
    """Run command with /usr/bin/time -v to measure peak RSS.

    Returns (exit_code, peak_rss_kb).
    Falls back to ps polling if /usr/bin/time -v is unavailable.
    """
    # Try /usr/bin/time -v first
    try:
        proc = subprocess.run(
            ["/usr/bin/time", "-v"] + cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            text=True,
            timeout=120,
        )
        for line in proc.stderr.splitlines():
            if "Maximum resident set size" in line:
                peak_kb = int(line.split()[-1])
                return (proc.returncode, peak_kb)
    except (OSError, subprocess.TimeoutExpired, ValueError, IndexError):
        pass

    # Fallback: spawn and poll via ps
    try:
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        time.sleep(0.5)
        peak_kb = 0
        try:
            out = subprocess.run(
                ["ps", "-o", "rss=", "-p", str(proc.pid)],
                capture_output=True, text=True, timeout=5,
            )
            rss_str = out.stdout.strip()
            if rss_str:
                peak_kb = int(rss_str)
        except (OSError, subprocess.TimeoutExpired, ValueError):
            pass
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait()
        return (proc.returncode, peak_kb)
    except OSError:
        return (-1, 0)


def compute_stats(values: list) -> dict:
    """Compute mean, stddev, min, max, p50, p95 from a list of floats."""
    if not values:
        return {"mean": 0, "stddev": 0, "min": 0, "max": 0, "p50": 0, "p95": 0}
    n = len(values)
    s = sorted(values)
    mean = sum(s) / n
    variance = sum((x - mean) ** 2 for x in s) / n if n >= 2 else 0.0
    stddev = math.sqrt(variance)
    p50 = s[int(n * 0.50)] if n >= 2 else s[0]
    p95 = s[min(int(n * 0.95), n - 1)] if n >= 2 else s[0]
    return {
        "mean": round(mean, 2),
        "stddev": round(stddev, 2),
        "min": round(s[0], 2),
        "max": round(s[-1], 2),
        "p50": round(p50, 2),
        "p95": round(p95, 2),
    }


def size_of(path: str) -> int:
    """du -sk equivalent: return total size in KB using os.walk."""
    p = Path(path)
    if not p.exists():
        return 0
    total_bytes = 0
    for dirpath, dirnames, filenames in os.walk(p):
        # Skip common build/venv dirs to match bash behavior
        skip = {"node_modules", "target", "vendor", "__pycache__",
                ".venv", "venv", ".git", "dist", "build", ".next",
                "coverage", ".turbo", ".claude"}
        dirnames[:] = [d for d in dirnames if d not in skip]
        for f in filenames:
            fp = os.path.join(dirpath, f)
            try:
                total_bytes += os.path.getsize(fp)
            except OSError:
                pass
    return total_bytes // 1024


def size_of_raw(path: str) -> int:
    """Unfiltered size_of — no directory exclusions."""
    p = Path(path)
    if not p.exists():
        return 0
    total_bytes = 0
    for dirpath, dirnames, filenames in os.walk(p):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            try:
                total_bytes += os.path.getsize(fp)
            except OSError:
                pass
    return total_bytes // 1024


def load_config(path: str) -> dict:
    """Read and return a JSON config file."""
    with open(path) as f:
        return json.load(f)


def sample_metric(platform: str, metric: str, cmd: list, unit: str,
                  runs: int = 5, notes: str = "") -> Metric:
    """Run a command N times, collect timings, compute stats.

    Returns a Metric with samples and stats populated.
    """
    samples = []
    for _ in range(runs):
        _, elapsed_ms = time_command(cmd)
        if elapsed_ms > 0:
            samples.append(elapsed_ms)
    if not samples:
        return Metric(platform=platform, metric=metric, value=0.0,
                       unit=unit, notes=notes or "all runs failed")
    stats = compute_stats(samples)
    return Metric(
        platform=platform, metric=metric, value=stats["mean"],
        unit=unit, notes=notes, samples=round_vals(samples),
        stats=stats,
    )


def round_vals(values: list, decimals: int = 2) -> list:
    """Round all floats in a list."""
    return [round(v, decimals) for v in values]


def write_json(result: BenchmarkResult, path: str):
    """Serialize BenchmarkResult to JSON file with indent=2."""
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w") as f:
        json.dump(result.to_json_dict(), f, indent=2, default=str)
        f.write("\n")


def write_markdown(result: BenchmarkResult, path: str):
    """Generate Markdown report with tables from BenchmarkResult."""
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    lines = []

    title_map = {
        "runtime": "Runtime Benchmark Results",
        "static": "Static Analysis Benchmark Results",
        "sandbox": "Sandbox Health Check Results",
    }
    title = title_map.get(result.command, "Benchmark Results")
    lines.append(f"# {title} — {result.timestamp}")
    lines.append("")
    lines.append(
        f"Engine v{result.engine_version} | "
        f"{len(result.metrics)} metrics across "
        f"{len(set(m.platform for m in result.metrics))} platforms"
    )
    lines.append("")

    # Toolchain table
    lines.append("## Toolchain")
    lines.append("")
    lines.append("| Tool | Available |")
    lines.append("|------|-----------|")
    for tool, available in result.toolchain.items():
        lines.append(f"| {tool} | {str(available).lower()} |")
    lines.append("")

    # Group metrics by category
    if result.command == "runtime":
        _md_runtime_tables(lines, result)
    elif result.command == "static":
        _md_static_tables(lines, result)
    elif result.command == "sandbox":
        _md_sandbox_tables(lines, result)

    # Raw metrics table
    lines.append("## All Metrics (Raw)")
    lines.append("")
    lines.append("| Platform | Metric | Value | Unit | Notes |")
    lines.append("|----------|--------|-------|------|-------|")
    for m in result.metrics:
        notes = m.notes[:60] if m.notes else ""
        lines.append(f"| {m.platform} | {m.metric} | {m.value} | {m.unit} | {notes} |")
    lines.append("")

    # Skipped platforms
    if result.skipped:
        lines.append("## Skipped Platforms")
        lines.append("")
        for s in result.skipped:
            lines.append(f"- **{s['platform']}**: {s['reason']}")
        lines.append("")

    with open(p, "w") as f:
        f.write("\n".join(lines))


def write_summary_table(result: BenchmarkResult) -> str:
    """Sorted comparison table suitable for CI job summary."""
    lines = []
    lines.append(f"## {result.command.title()} Summary — {result.timestamp}")
    lines.append("")

    # Collect one representative metric per platform
    primary_metrics = {
        "runtime": "cold_start_time",
        "static": "repo_size",
        "sandbox": "findings_total",
    }
    primary = primary_metrics.get(result.command, None)

    if primary:
        rows = []
        seen = set()
        for m in result.metrics:
            if m.metric == primary and m.platform not in seen:
                rows.append((m.platform, m.value, m.unit, m.notes))
                seen.add(m.platform)
        rows.sort(key=lambda r: r[1])

        lines.append(f"| Platform | {primary} | Unit | Notes |")
        lines.append(f"|----------|{'-' * 20}|------|-------|")
        for platform, value, unit, notes in rows:
            notes = notes[:50] if notes else ""
            lines.append(f"| {platform} | {value} | {unit} | {notes} |")
        lines.append("")

    return "\n".join(lines)


def _md_runtime_tables(lines: list, result: BenchmarkResult):
    """Generate runtime-specific markdown tables."""
    metric_tables = [
        ("Cold Start Time (ms)", "cold_start_time", ["Platform", "Cold Start (ms)", "Notes"]),
        ("Memory Usage", "memory_idle_mb",
         ["Platform", "Idle (MB)", "Active (MB)", "Notes"]),
        ("Binary / Installation Size", "binary_size",
         ["Platform", "Binary Size (KB)", "Install Footprint (KB)", "Notes"]),
        ("Response Latency (ms)", "response_latency_ms",
         ["Platform", "Latency (ms)", "Notes"]),
        ("Build Proxy Time (ms)", "build_proxy_time",
         ["Platform", "Build Time (ms)", "Notes"]),
    ]
    for section_title, key_metric, headers in metric_tables:
        lines.append(f"## {section_title}")
        lines.append("")
        lines.append("| " + " | ".join(headers) + " |")
        lines.append("|" + "|".join(["-" * (len(h) + 2) for h in headers]) + "|")
        _emit_metric_rows(lines, result, key_metric, headers)
        lines.append("")


def _md_static_tables(lines: list, result: BenchmarkResult):
    """Generate static-analysis markdown tables."""
    lines.append("## Repository Size & Code Metrics")
    lines.append("")
    lines.append("| Platform | Repo Size (KB) | Source Files | LOC | Deps | Tests |")
    lines.append("|----------|----------------|-------------|-----|------|-------|")
    # Collect per-platform summary data
    platforms = sorted(set(m.platform for m in result.metrics))
    for plat in platforms:
        repo = _get_val(result, plat, "repo_size")
        # Try language-specific source/loc
        src = (_get_val(result, plat, "rust_files") or
               _get_val(result, plat, "ts_files") or
               _get_val(result, plat, "go_files") or
               _get_val(result, plat, "py_files") or
               _get_val(result, plat, "verilog_files") or 0)
        loc = (_get_val(result, plat, "rust_loc") or
               _get_val(result, plat, "ts_loc") or
               _get_val(result, plat, "go_loc") or
               _get_val(result, plat, "py_loc") or
               _get_val(result, plat, "verilog_loc") or 0)
        deps = (_get_val(result, plat, "cargo_deps") or
                _get_val(result, plat, "npm_deps") or
                _get_val(result, plat, "go_deps") or
                _get_val(result, plat, "py_deps") or 0)
        tests = _get_val(result, plat, "test_files") or 0
        lines.append(f"| {plat} | {repo} | {src} | {loc} | {deps} | {tests} |")
    lines.append("")

    lines.append("## Project Health")
    lines.append("")
    lines.append("| Platform | CI Workflows | CI Steps | Dockerfiles | Makefile | README | Docs (KB) | i18n |")
    lines.append("|----------|-------------|----------|-------------|----------|--------|-----------|------|")
    for plat in platforms:
        ci = _get_val(result, plat, "ci_workflows") or 0
        steps = _get_val(result, plat, "ci_steps") or 0
        df = _get_val(result, plat, "dockerfiles") or 0
        mf = _get_val(result, plat, "makefile_targets") or 0
        rl = _get_val(result, plat, "readme_lines") or 0
        ds = _get_val(result, plat, "docs_size") or 0
        i18 = _get_val(result, plat, "i18n_files") or 0
        lines.append(f"| {plat} | {ci} | {steps} | {df} | {mf} | {rl} | {ds} | {i18} |")
    lines.append("")


def _md_sandbox_tables(lines: list, result: BenchmarkResult):
    """Generate sandbox findings markdown tables."""
    lines.append("## Findings Summary")
    lines.append("")
    severity_counts = {"critical": 0, "error": 0, "warning": 0, "success": 0, "info": 0}
    for m in result.metrics:
        if m.metric == "finding":
            sev = m.notes.split("|")[0].strip().lower() if "|" in m.notes else m.notes.lower()
            if sev in severity_counts:
                severity_counts[sev] += 1
    lines.append("| Severity | Count |")
    lines.append("|----------|-------|")
    for sev, count in severity_counts.items():
        if count > 0:
            lines.append(f"| {sev} | {count} |")
    lines.append("")

    # Group by platform
    platforms = sorted(set(m.platform for m in result.metrics))
    for plat in platforms:
        findings = [m for m in result.metrics if m.platform == plat and m.metric == "finding"]
        if not findings:
            continue
        lines.append(f"### {plat}")
        for f in findings:
            lines.append(f"- [{f.unit}] {f.notes}")
        lines.append("")


def _emit_metric_rows(lines: list, result: BenchmarkResult, key_metric: str, headers: list):
    """Emit table rows for a specific metric key."""
    platforms = sorted(set(m.platform for m in result.metrics))
    for plat in platforms:
        primary = _get_val(result, plat, key_metric)
        if primary is None:
            continue
        primary_m = _get_metric(result, plat, key_metric)
        notes = primary_m.notes[:50] if primary_m and primary_m.notes else ""
        if key_metric == "memory_idle_mb":
            active = _get_val(result, plat, "memory_active_mb") or 0
            lines.append(f"| {plat} | {primary} | {active} | {notes} |")
        elif key_metric == "binary_size":
            inst = _get_val(result, plat, "install_footprint") or 0
            inst_m = _get_metric(result, plat, "install_footprint")
            inst_notes = inst_m.notes[:30] if inst_m and inst_m.notes else ""
            lines.append(f"| {plat} | {primary} | {inst} | {inst_notes} |")
        else:
            lines.append(f"| {plat} | {primary} | {notes} |")


def _get_val(result: BenchmarkResult, platform: str, metric: str):
    """Get metric value for a platform, or None."""
    for m in result.metrics:
        if m.platform == platform and m.metric == metric:
            return m.value
    return None


def _get_metric(result: BenchmarkResult, platform: str, metric: str):
    """Get full Metric object, or None."""
    for m in result.metrics:
        if m.platform == platform and m.metric == metric:
            return m
    return None


def now_timestamp() -> str:
    """Return ISO 8601 timestamp suitable for filenames and JSON."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")
