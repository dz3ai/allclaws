"""Report generation — aggregate N benchmark runs into summary."""

import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

from .utils import (
    BenchmarkResult,
    Metric,
    compute_stats,
    detect_toolchain,
    load_config,
    now_timestamp,
    write_json,
    write_markdown,
)


class ReportGenerator:
    """Aggregate multiple benchmark runs into a summary report."""

    def __init__(self, results_dir: str, output_dir: str,
                 last: int = 5, regression_pct: int = 20):
        self.results_dir = Path(results_dir)
        self.output_dir = Path(output_dir)
        self.last = last
        self.regression_pct = regression_pct

    def generate(self, command: str = "runtime") -> Optional[BenchmarkResult]:
        """Load recent runs, aggregate, and produce a summary result."""
        runs = self._load_recent_runs(command)
        if not runs:
            print(f"No recent {command} runs found in {self.results_dir}")
            return None

        print(f"Aggregating {len(runs)} recent {command} runs")
        return self._aggregate(runs, command)

    def _load_recent_runs(self, command: str) -> list:
        """Find and load the N most recent benchmark result JSON files."""
        # Search for result files in the results directory
        pattern_map = {
            "runtime": "*-agent-runtime*results.json",
            "static": "*results.json",
            "sandbox": "*findings.json",
        }
        pattern = pattern_map.get(command, "*results.json")
        json_files = sorted(
            self.results_dir.rglob(pattern),
            key=lambda f: f.stat().st_mtime,
            reverse=True,
        )

        # Also try broader search if specific pattern finds nothing
        if not json_files:
            json_files = sorted(
                self.results_dir.rglob("*results*.json"),
                key=lambda f: f.stat().st_mtime,
                reverse=True,
            )

        runs = []
        for jf in json_files[:self.last]:
            try:
                data = json.loads(jf.read_text())
                runs.append((jf, data))
                print(f"  Loaded: {jf.name}")
            except (OSError, json.JSONDecodeError) as e:
                print(f"  WARN: Could not load {jf.name}: {e}")

        return runs

    def _aggregate(self, runs: list, command: str) -> BenchmarkResult:
        """Aggregate metrics across runs, detect regressions."""
        toolchain = detect_toolchain()
        aggregated_metrics: list[Metric] = []
        regressions = []
        improvements = []

        # Collect all unique platform+metric pairs
        pairs: dict[str, list[tuple]] = {}  # key -> [(file, value, unit, notes)]
        for jf, data in runs:
            for m in data.get("metrics", []):
                key = f"{m['platform']}::{m['metric']}"
                if key not in pairs:
                    pairs[key] = []
                pairs[key].append((
                    jf.name,
                    float(m.get("value", 0)),
                    m.get("unit", ""),
                    m.get("notes", ""),
                ))

        # Compute aggregates
        for key, samples in sorted(pairs.items()):
            platform, metric = key.split("::", 1)
            values = [s[1] for s in samples]
            unit = samples[0][2] if samples else ""
            notes = samples[-1][3] if samples else ""

            stats = compute_stats(values)
            trend = ""

            # Detect regression (compare oldest to newest mean)
            if len(values) >= 2:
                old_mean = sum(values[:len(values)//2]) / (len(values)//2)
                new_mean = sum(values[len(values)//2:]) / (len(values) - len(values)//2)
                if old_mean > 0:
                    change_pct = ((new_mean - old_mean) / old_mean) * 100
                    if change_pct > self.regression_pct:
                        trend = f"REGRESSION +{change_pct:.1f}%"
                        regressions.append({
                            "platform": platform,
                            "metric": metric,
                            "change_pct": round(change_pct, 1),
                            "old_mean": round(old_mean, 2),
                            "new_mean": round(new_mean, 2),
                        })
                    elif change_pct < -self.regression_pct:
                        trend = f"IMPROVED {change_pct:.1f}%"
                        improvements.append({
                            "platform": platform,
                            "metric": metric,
                            "change_pct": round(change_pct, 1),
                            "old_mean": round(old_mean, 2),
                            "new_mean": round(new_mean, 2),
                        })

            aggregated_metrics.append(Metric(
                platform=platform,
                metric=metric,
                value=stats["mean"],
                unit=unit,
                notes=f"({len(runs)} runs) {trend}" if trend else f"({len(runs)} runs)",
                samples=[round(v, 2) for v in values],
                stats=stats,
            ))

        # Build skipped list from all runs
        all_skipped = []
        seen_skipped = set()
        for _, data in runs:
            for s in data.get("skipped", []):
                key = f"{s['platform']}:{s['reason']}"
                if key not in seen_skipped:
                    all_skipped.append(s)
                    seen_skipped.add(key)

        result = BenchmarkResult(
            timestamp=now_timestamp(),
            engine_version="3.0.0",
            command=f"{command}_report",
            toolchain=toolchain,
            metrics=aggregated_metrics,
            skipped=all_skipped,
        )

        # Print summary
        print(f"\n  Total metrics:  {len(aggregated_metrics)}")
        print(f"  Regressions:    {len(regressions)}")
        print(f"  Improvements:   {len(improvements)}")
        print(f"  Skipped:        {len(all_skipped)}")

        if regressions:
            print("\n  REGRESSIONS:")
            for r in regressions:
                print(f"    {r['platform']}/{r['metric']}: "
                      f"{r['old_mean']} -> {r['new_mean']} "
                      f"(+{r['change_pct']}%)")

        if improvements:
            print("\n  IMPROVEMENTS:")
            for imp in improvements:
                print(f"    {imp['platform']}/{imp['metric']}: "
                      f"{imp['old_mean']} -> {imp['new_mean']} "
                      f"({imp['change_pct']}%)")

        return result
