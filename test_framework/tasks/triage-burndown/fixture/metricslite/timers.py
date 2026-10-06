"""Stopwatch timers measured with a monotonic clock."""

from __future__ import annotations

import contextlib
import time
from collections.abc import Iterator


class Timer:
    """One-shot stopwatch.

    Contract (README): elapsed time is measured with a MONOTONIC clock, so
    results are immune to system wall-clock adjustments (NTP steps, manual
    time changes). ``stop()`` returns the elapsed seconds and freezes them
    in ``elapsed``.
    """

    def __init__(self) -> None:
        self._start: float | None = None
        self._elapsed: float | None = None

    def start(self) -> None:
        """Start measuring. Raises RuntimeError if already running."""
        if self._start is not None:
            raise RuntimeError("timer already started")
        self._start = time.time()

    def stop(self) -> float:
        """Stop measuring and return elapsed seconds (timer becomes idle)."""
        if self._start is None:
            raise RuntimeError("timer not started")
        self._elapsed = time.time() - self._start
        self._start = None
        return self._elapsed

    @property
    def elapsed(self) -> float:
        """Seconds reported by the last completed stop()."""
        if self._elapsed is None:
            raise RuntimeError("timer has no completed measurement")
        return self._elapsed

    def running(self) -> bool:
        """True between start() and stop()."""
        return self._start is not None


@contextlib.contextmanager
def measure() -> Iterator[Timer]:
    """Context manager: time the block; read ``timer.elapsed`` after exit."""
    timer = Timer()
    timer.start()
    try:
        yield timer
    finally:
        timer.stop()


def human_duration(seconds: float) -> str:
    """Render a duration as a compact human string.

    Contract (README): below one minute -> ``"12.3s"`` (one decimal);
    below one hour -> ``"4:05"`` (minutes:seconds); otherwise
    ``"1:02:03"`` (hours:minutes:seconds). Negative input is invalid and
    raises ValueError.
    """
    if seconds < 0:
        raise ValueError("duration must be non-negative")
    if seconds < 60:
        return f"{round(float(seconds), 1)}s"
    total = int(seconds)
    minutes, sec = divmod(total, 60)
    hours, mins = divmod(minutes, 60)
    if hours:
        return f"{hours}:{mins:02d}:{sec:02d}"
    return f"{mins}:{sec:02d}"
