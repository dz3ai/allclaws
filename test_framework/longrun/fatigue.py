"""Fatigue detection engine for triage-burndown runs (plan §Fatigue Detection Protocol).

Scenario 4 (triage-burndown) scores 5 sequential same-difficulty issues in one
continuous session. Window dicts come from scoring.score_windows with the hard
shape {"window": int, "solved": bool, "tokens": int|None, "turns": int|None,
"wall_seconds": float|None}.

Three pure functions, stdlib only, no longrun imports:

- window_signals(list[dict]) -> dict         within-run signals for ONE run
- analyze_repeats(list[list[dict]]) -> dict  cross-repeat median + spread and
                                             fatigue_flagged
- summarize(list[dict]) -> dict              report.py convenience over the
                                             two, grouping run dicts by repeat

Fatigue flagging is deliberately conservative (plan: "flag fatigue only if
monotone decline across repeats"). Definition used by analyze_repeats: let
c_r = number of solved windows in repeat r; fatigue_flagged is True iff
c_1 >= c_2 >= ... >= c_n (non-increasing across repeats) AND at least one
step strictly decreases (c_r > c_r+1 for some r). Fewer than 2 repeats ->
False.

Synthetic self-demo (no pytest, no agent launches):
    PYTHONPATH=test_framework /usr/bin/python3 test_framework/longrun/fatigue.py
"""

from __future__ import annotations

import statistics


def _is_number(value: object) -> bool:
    """int/float gate; type-is check so bool (an int subtype) is rejected."""
    return type(value) is int or type(value) is float


def _trend(values: list) -> str | None:
    """Direction over adjacent window pairs where BOTH carry the metric.

    Sign of the summed window-over-window deltas (telescopes to
    last-present minus first-present for contiguous data): "rising" /
    "falling" / "flat"; None with fewer than one valid adjacent pair.
    """
    deltas = []
    for prev, curr in zip(values, values[1:]):
        if _is_number(prev) and _is_number(curr):
            deltas.append(curr - prev)
    if not deltas:
        return None
    total = sum(deltas)
    if total > 0:
        return "rising"
    if total < 0:
        return "falling"
    return "flat"


def window_signals(windows: list[dict]) -> dict:
    """Within-run fatigue signals for one triage-burndown run.

    windows: scoring.score_windows output. Entries not matching the window
    shape are ignored rather than raising.

    Returns:
        solve_rate: fraction of windows whose "solved" is exactly bool True
            (None when no well-formed window is present).
        token_trend / turn_trend / wall_trend: _trend() over the metric
            column ("rising" | "falling" | "flat" | None).
    """
    well_formed = [w for w in windows if type(w) is dict]
    solved = [
        1 if w["solved"] else 0 for w in well_formed if type(w.get("solved")) is bool
    ]
    return {
        "solve_rate": (sum(solved) / len(solved)) if solved else None,
        "token_trend": _trend([w.get("tokens") for w in well_formed]),
        "turn_trend": _trend([w.get("turns") for w in well_formed]),
        "wall_trend": _trend([w.get("wall_seconds") for w in well_formed]),
    }


def analyze_repeats(repeat_runs: list[list[dict]]) -> dict:
    """Cross-repeat statistics (plan: "3 repeats per agent; report median +
    spread; flag fatigue only if monotone decline across repeats").

    Each inner list is one repeat's window dicts (scoring.score_windows
    shape). Malformed entries are skipped; never raises.

    Returns:
        per_window: one entry per window number seen in any repeat (sorted),
            with solved/tokens/turns median + spread across repeats (solved
            as 0/1). spread = max - min over the repeats where the value is
            present; median/spread are None when no repeat carries the value
            (spread also None with fewer than 2 present values).
        fatigue_flagged: True iff the per-repeat solved-window counts are
            non-increasing across repeats with at least one strict decrease
            (definition documented in the module docstring); False with
            fewer than 2 repeats.
    """
    runs = [run for run in repeat_runs if type(run) is list]
    solved_counts = [
        sum(
            1
            for w in run
            if type(w) is dict and type(w.get("solved")) is bool and w["solved"]
        )
        for run in runs
    ]
    flagged = False
    if len(solved_counts) >= 2:
        non_increasing = all(
            solved_counts[i] >= solved_counts[i + 1]
            for i in range(len(solved_counts) - 1)
        )
        strict_drop = any(
            solved_counts[i] > solved_counts[i + 1]
            for i in range(len(solved_counts) - 1)
        )
        flagged = non_increasing and strict_drop

    by_window: dict[int, dict[str, list[int]]] = {}
    for run in runs:
        for w in run:
            if type(w) is not dict:
                continue
            number = w.get("window")
            if type(number) is not int:
                continue
            slot = by_window.setdefault(number, {"solved": [], "tokens": [], "turns": []})
            if type(w.get("solved")) is bool:
                slot["solved"].append(1 if w["solved"] else 0)
            for key in ("tokens", "turns"):
                if type(w.get(key)) is int:
                    slot[key].append(w[key])

    per_window: list[dict] = []
    for number in sorted(by_window):
        entry: dict = {"window": number}
        for key in ("solved", "tokens", "turns"):
            values = by_window[number][key]
            entry[f"{key}_median"] = statistics.median(values) if values else None
            entry[f"{key}_spread"] = (
                max(values) - min(values) if len(values) >= 2 else None
            )
        per_window.append(entry)

    return {"per_window": per_window, "fatigue_flagged": flagged}


def summarize(result_dicts: list[dict]) -> dict:
    """Report-facing convenience over window_signals + analyze_repeats.

    result_dicts: run dicts as returned by runner.run_one / collected in
    runner.run_grid — each carrying "repeat" (int) and the RunResult extra
    under "extra", whose "windows" key holds the run's window dicts. Callers
    should pass one platform's runs (report.py renders per-platform); runner
    construction guarantees one run per (platform, task, repeat), and if
    several runs share a repeat their windows are concatenated.

    Returns:
        repeats: sorted repeat numbers seen (ints)
        signals_by_repeat: {str(repeat): window_signals(...)} — JSON-safe
            string keys
        cross_repeat: analyze_repeats over the repeats in ascending order
    """
    by_repeat: dict[int, list[dict]] = {}
    for run in result_dicts:
        if type(run) is not dict:
            continue
        repeat = run.get("repeat")
        if type(repeat) is not int:
            continue
        extra = run.get("extra")
        windows = extra.get("windows") if type(extra) is dict else None
        if type(windows) is not list:
            windows = []
        by_repeat.setdefault(repeat, []).extend(windows)

    return {
        "repeats": sorted(by_repeat),
        "signals_by_repeat": {
            str(repeat): window_signals(by_repeat[repeat])
            for repeat in sorted(by_repeat)
        },
        "cross_repeat": analyze_repeats([by_repeat[r] for r in sorted(by_repeat)]),
    }


def _window(
    number: int,
    solved: bool,
    tokens: int | None,
    turns: int | None,
    wall_seconds: float | None,
) -> dict:
    return {
        "window": number,
        "solved": solved,
        "tokens": tokens,
        "turns": turns,
        "wall_seconds": wall_seconds,
    }


if __name__ == "__main__":
    import json

    # Fatigue case: each repeat solves strictly fewer windows while the same-
    # difficulty issues cost MORE tokens (plan: token inflation signal).
    fatigued = [
        [_window(n, True, 900 + 40 * n, 6, 60.0 + n) for n in range(1, 6)],
        [_window(n, n <= 4, 1500 + 90 * n, 9, 80.0 + n) for n in range(1, 6)],
        [_window(n, n <= 3, 2400 + 150 * n, 13, 110.0 + n) for n in range(1, 6)],
    ]
    # Healthy case: solved counts 5, 4, 5 — not non-increasing -> never flagged.
    healthy = [
        [_window(n, True, 1000 + 30 * n, 6, 60.0) for n in range(1, 6)],
        [_window(n, n != 3, 1050 + 25 * n, 7, 62.0) for n in range(1, 6)],
        [_window(n, True, 1010 + 28 * n, 6, 61.0) for n in range(1, 6)],
    ]

    fatigued_analysis = analyze_repeats(fatigued)
    healthy_analysis = analyze_repeats(healthy)
    assert fatigued_analysis["fatigue_flagged"] is True
    assert healthy_analysis["fatigue_flagged"] is False

    # Flat case: non-increasing (3, 3, 3) but no strict decrease -> False.
    flat = [[_window(n, n <= 3, 1000, 6, 60.0) for n in range(1, 6)] for _ in range(3)]
    assert analyze_repeats(flat)["fatigue_flagged"] is False

    # window_signals on one fatigued repeat: solve rate + inflation trend.
    signals = window_signals(fatigued[2])
    assert signals["solve_rate"] == 0.6
    assert signals["token_trend"] == "rising"
    assert signals["wall_trend"] == "rising"

    # Malformed input must not crash: junk entries degrade, never raise.
    robust = window_signals([None, {"window": 1}, {"window": 2, "solved": "yes"}])
    assert robust["solve_rate"] is None and robust["token_trend"] is None

    # summarize() over runner-shaped run dicts (extra.windows + repeat).
    summary = summarize(
        [
            {"repeat": repeat + 1, "extra": {"windows": fatigued[repeat]}}
            for repeat in range(3)
        ]
    )
    assert summary["repeats"] == [1, 2, 3]
    assert summary["cross_repeat"]["fatigue_flagged"] is True
    assert summary["signals_by_repeat"]["3"]["solve_rate"] == 0.6

    print("fatigue case: fatigue_flagged =", fatigued_analysis["fatigue_flagged"])
    print(json.dumps(fatigued_analysis, indent=2))
    print("healthy case: fatigue_flagged =", healthy_analysis["fatigue_flagged"])
    print(json.dumps(healthy_analysis, indent=2))
    print("signals (fatigued repeat 3):", json.dumps(signals))
    print("summarize():", json.dumps(summary, indent=2))
    print("ALL FATIGUE SELF-CHECKS PASSED")
