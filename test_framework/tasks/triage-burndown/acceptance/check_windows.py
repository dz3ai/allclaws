#!/usr/bin/env python3
"""Per-window (per-issue) scoring checks for triage-burndown.

No pytest dependency — duplicates the 5 acceptance checks' logic directly.
Prints exactly ONE JSON line to stdout:

    {"windows": [{"window": 1, "solved": false}, ...]}

window = issue number (1-5), solved = bool. Exit code is ALWAYS 0: the
fatigue engine (plan §Fatigue Detection Protocol) parses stdout, so any
internal error must degrade to solved=false rather than a crash.

Usage: check_windows.py [worktree-root]
       (default: parent of this script's directory — matches how scoring
       mounts acceptance/ into a worktree root)
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def check_1_percentile() -> bool:
    from metricslite import percentile

    return (
        percentile([10, 20], 50) == 15.0
        and percentile([10, 20, 30, 40], 25) == 17.5
        and percentile([10, 20, 30, 40], 50) == 25.0
        and percentile([10, 20, 30], 0) == 10.0
        and percentile([10, 20, 30], 100) == 30.0
    )


def check_2_rolling_default() -> bool:
    from metricslite import RollingMean

    rolling = RollingMean()
    for value in (1, 2, 3, 4, 5, 6):
        rolling.add(value)
    if rolling.window != 5 or rolling.mean() != 4.0:
        return False
    explicit = RollingMean(window=3)
    for value in (1, 2, 3, 4, 5):
        explicit.add(value)
    return explicit.mean() == 4.0 and RollingMean().mean() == 0.0


def check_3_summary_validation() -> bool:
    from metricslite import summarize

    try:
        summarize([])
    except ValueError:
        pass
    except Exception:
        return False
    else:
        return False
    return summarize([1.0, 2.0, 3.0]) == {
        "count": 3,
        "mean": 2.0,
        "min": 1.0,
        "max": 3.0,
    }


def check_4_counter_case_insensitive() -> bool:
    from metricslite import Counter

    counter = Counter()
    counter.inc("Error")
    counter.inc("ERROR", by=2)
    counter.inc("error")
    return (
        counter.get("Error") == 4
        and counter.get("error") == 4
        and counter.get("ERROR") == 4
        and counter.keys() == ["error"]
        and counter.total() == 4
    )


def check_5_timer_monotonic() -> bool:
    from metricslite import Timer

    fake = {"now": 3_000_000.0}

    def stepping_time():
        fake["now"] -= 100.0
        return fake["now"]

    real_time = time.time
    time.time = stepping_time  # wall clock steps back 100s between reads
    try:
        timer = Timer()
        timer.start()
        time.sleep(0.01)
        elapsed = timer.stop()
    except Exception:
        return False
    finally:
        time.time = real_time
    return 0.0 <= elapsed < 1.0


CHECKS = (
    check_1_percentile,
    check_2_rolling_default,
    check_3_summary_validation,
    check_4_counter_case_insensitive,
    check_5_timer_monotonic,
)


def main() -> None:
    windows = []
    for number, check in enumerate(CHECKS, start=1):
        try:
            solved = bool(check())
        except Exception:
            solved = False
        windows.append({"window": number, "solved": solved})
    print(json.dumps({"windows": windows}))


if __name__ == "__main__":
    main()
    sys.exit(0)
