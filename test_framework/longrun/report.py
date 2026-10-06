"""Report generation for long-run benchmark grids (Markdown + JSON rollup)."""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any


def load_runs(run_dir: Path) -> list[dict[str, Any]]:
    """Load every result.json under a timestamped run dir.

    Phase 2 layout: <platform>/<task-id>/rep<N>/result.json (repeat-aware run
    dirs — plan §Fatigue Detection Protocol needs all repeats on disk). The
    pre-Phase-2 flat layout <platform>/<task-id>/result.json is kept as a
    fallback so older run dirs still load; payloads lacking "repeat" default
    to 1 (a grid runs repeats=1 unless told otherwise).
    """
    runs = []
    seen: set[Path] = set()
    for pattern in ("*/*/rep*/result.json", "*/*/result.json"):
        for result_path in sorted(run_dir.glob(pattern)):
            if result_path in seen:
                continue
            seen.add(result_path)
            try:
                run = json.loads(result_path.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                continue
            if type(run) is dict:
                run.setdefault("repeat", 1)
                runs.append(run)
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
        "fatigue": _fatigue_summary(runs),
    }


def _windows_by_repeat(runs: list[dict[str, Any]]) -> dict[int, list]:
    """Concatenated extra.windows per repeat (longrun.fatigue.summarize grouping)."""
    by_repeat: dict[int, list] = {}
    for run in runs:
        extra = run.get("extra")
        windows = extra.get("windows") if type(extra) is dict else None
        if type(windows) is not list:
            continue
        repeat = run.get("repeat")
        if type(repeat) is not int:
            repeat = 1
        by_repeat.setdefault(repeat, []).extend(windows)
    return by_repeat


def _fatigue_summary(runs: list[dict[str, Any]]) -> dict[str, Any]:
    """Per-platform fatigue rollup for the JSON summary dict.

    Carries fatigue.summarize's signals (repeats / signals_by_repeat /
    cross_repeat) plus the raw windows themselves under windows_by_repeat.
    Defensively lazy: a missing/broken longrun.fatigue degrades to {} —
    the summary must never fail because the fatigue engine does.
    """
    platforms = {
        run.get("platform", "?")
        for run in runs
        if type(run.get("extra")) is dict
        and type(run["extra"].get("windows")) is list
    }
    if not platforms:
        return {}
    try:
        from longrun.fatigue import summarize as fatigue_summarize
    except Exception:
        return {}

    out: dict[str, Any] = {}
    for platform in sorted(platforms):
        prows = [r for r in runs if r.get("platform", "?") == platform]
        by_repeat = _windows_by_repeat(prows)
        try:
            entry = fatigue_summarize(
                [{"repeat": r, "extra": {"windows": w}} for r, w in sorted(by_repeat.items())]
            )
        except Exception:
            entry = {}
        entry["windows_by_repeat"] = {str(r): w for r, w in sorted(by_repeat.items())}
        out[platform] = entry
    return out


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
    lines += _render_fatigue(runs)
    return "\n".join(lines) + "\n"


def _fatigue_na() -> list[str]:
    return ["", "## Fatigue (triage-burndown)", "", "n/a", ""]


def _window_marks(windows: list) -> str:
    """Per-window solved marks, e.g. `Y N Y Y N`; `?` when malformed."""
    marks = []
    for w in windows:
        solved = w.get("solved") if type(w) is dict else None
        marks.append("Y" if solved is True else "N" if solved is False else "?")
    return " ".join(marks) if marks else "-"


def _metric_marks(windows: list, key: str) -> str:
    """Per-window metric values (`/`-joined) where present, else `-`."""
    marks = []
    for w in windows:
        v = w.get(key) if type(w) is dict else None
        if type(v) is int:
            marks.append(str(v))
        elif type(v) is float:
            marks.append(f"{v:.0f}")
        else:
            marks.append("-")
    return "/".join(marks) if marks and any(m != "-" for m in marks) else "-"


def _render_fatigue(runs: list[dict[str, Any]]) -> list[str]:
    """'Fatigue (triage-burndown)' section for runs carrying extra.windows.

    Per-platform table: repeat, per-window solved marks, tokens/turns per
    window where present, plus window_signals; analyze_repeats'
    fatigue_flagged is appended when >= 2 repeats are present. Lazily and
    defensively imports longrun.fatigue — the section renders as "n/a" when
    the import or the data is missing (scoring.score_windows contract: any
    failure degrades, never raises).
    """
    try:
        from longrun.fatigue import (
            summarize as fatigue_summarize,
            window_signals,
        )
    except Exception:
        return _fatigue_na()

    by_platform: dict[str, dict[int, list]] = {}
    for run in runs:
        extra = run.get("extra")
        windows = extra.get("windows") if type(extra) is dict else None
        if type(windows) is not list:
            continue
        by_platform.setdefault(run.get("platform", "?"), {})
        repeat = run.get("repeat")
        if type(repeat) is not int:
            repeat = 1
        by_platform[run.get("platform", "?")].setdefault(repeat, []).extend(windows)
    if not by_platform:
        return _fatigue_na()

    lines = [
        "",
        "## Fatigue (triage-burndown)",
        "",
        "| platform | repeat | solved / window | tokens / window | turns / window | solve rate | token trend |",
        "|---|---|---|---|---|---|---|",
    ]
    for platform, by_repeat in sorted(by_platform.items()):
        try:
            f = fatigue_summarize(
                [{"repeat": r, "extra": {"windows": w}} for r, w in sorted(by_repeat.items())]
            )
        except Exception:
            f = {}
        for repeat in sorted(by_repeat):
            windows = by_repeat[repeat]
            try:
                sig = window_signals(windows)
            except Exception:
                sig = {}
            rate = sig.get("solve_rate") if type(sig) is dict else None
            rate_s = f"{rate:.0%}" if type(rate) is float else "n/a"
            trend = sig.get("token_trend") if type(sig) is dict else None
            lines.append(
                f"| {platform} | {repeat} | {_window_marks(windows)} | "
                f"{_metric_marks(windows, 'tokens')} | {_metric_marks(windows, 'turns')} | "
                f"{rate_s} | {trend or 'n/a'} |"
            )
        if len(by_repeat) >= 2:
            flagged = (f.get("cross_repeat") or {}).get("fatigue_flagged")
            if flagged is not None:
                lines += [
                    "",
                    f"fatigue_flagged ({platform}): {flagged} — monotone "
                    "decline across repeats (plan §Fatigue Detection Protocol)",
                ]
    lines.append("")
    return lines


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
