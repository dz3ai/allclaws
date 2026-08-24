"""Report generation for long-run benchmark grids (Markdown + JSON rollup)."""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any


def load_runs(run_dir: Path) -> list[dict[str, Any]]:
    """Load every <platform>/<task-id>/result.json under a timestamped run dir."""
    runs = []
    for result_path in sorted(run_dir.glob("*/*/result.json")):
        try:
            runs.append(json.loads(result_path.read_text(encoding="utf-8")))
        except (json.JSONDecodeError, OSError):
            continue
    return runs


def summarize(runs: list[dict[str, Any]]) -> dict[str, Any]:
    """Grid-level aggregates: per-platform pass rates, tokens, cost, time."""
    by_platform: dict[str, list[dict]] = {}
    for run in runs:
        by_platform.setdefault(run.get("platform", "?"), []).append(run)

    platform_stats = {}
    for platform, prows in sorted(by_platform.items()):
        n = len(prows)
        passed = sum(1 for r in prows if r.get("score", {}).get("passed"))
        tin = [r.get("tokens_in") or 0 for r in prows]
        tout = [r.get("tokens_out") or 0 for r in prows]
        wall = [r.get("wall_seconds") or 0 for r in prows]
        cost = [r.get("cost_usd") or 0 for r in prows]
        platform_stats[platform] = {
            "runs": n,
            "pass_rate": round(passed / n, 3) if n else 0.0,
            "median_tokens_in": _median(tin),
            "median_tokens_out": _median(tout),
            "median_wall_seconds": round(_median(wall), 1),
            "total_cost_usd": round(sum(cost), 4),
        }
    return {
        "generated": time.strftime("%Y-%m-%dT%H-%M-%S"),
        "total_runs": len(runs),
        "platforms": platform_stats,
        "total_cost_usd": round(sum(r.get("cost_usd") or 0 for r in runs), 4),
    }


def render_markdown(summary: dict[str, Any], runs: list[dict[str, Any]]) -> str:
    """Human-facing smoke report: platform table + per-task outcome grid."""
    lines = [
        "# Long-Run Benchmark Smoke Report",
        "",
        f"Generated: {summary['generated']}  |  runs: {summary['total_runs']}  |  "
        f"spend: ${summary['total_cost_usd']:.4f}",
        "",
        "## Per-platform summary",
        "",
        "| platform | runs | pass rate | tok in (med) | tok out (med) | wall s (med) | cost $ |",
        "|---|---|---|---|---|---|---|",
    ]
    for platform, s in summary["platforms"].items():
        lines.append(
            f"| {platform} | {s['runs']} | {s['pass_rate']:.0%} | "
            f"{s['median_tokens_in']:,} | {s['median_tokens_out']:,} | "
            f"{s['median_wall_seconds']} | {s['total_cost_usd']:.4f} |"
        )
    lines += ["", "## Per-run outcomes", "",
              "| platform | task | status | scored | wall s | tokens in/out | notes |",
              "|---|---|---|---|---|---|---|"]
    for r in runs:
        scored = "PASS" if r.get("score", {}).get("passed") else "FAIL"
        notes = (r.get("notes") or "").replace("|", "/")[:60]
        lines.append(
            f"| {r.get('platform')} | {r.get('task_id')} | {r.get('status')} | "
            f"{scored} | {r.get('wall_seconds', 0):.0f} | "
            f"{r.get('tokens_in') or 0:,}/{r.get('tokens_out') or 0:,} | {notes} |"
        )
    return "\n".join(lines) + "\n"


def _median(values: list) -> float:
    xs = sorted(v for v in values if isinstance(v, (int, float)))
    if not xs:
        return 0
    n = len(xs)
    mid = n // 2
    return xs[mid] if n % 2 else (xs[mid - 1] + xs[mid]) / 2


def write_report(run_dir: Path) -> Path:
    """Load all runs under run_dir, write summary.json + report.md alongside."""
    runs = load_runs(run_dir)
    summary = summarize(runs)
    (run_dir / "summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    md = render_markdown(summary, runs)
    out = run_dir / "report.md"
    out.write_text(md, encoding="utf-8")
    return out
