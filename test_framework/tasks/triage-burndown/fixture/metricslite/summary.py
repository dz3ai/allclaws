"""Descriptive summary statistics for a sample sequence."""

from __future__ import annotations

import math
from typing import Sequence


def summarize(samples: Sequence[float]) -> dict:
    """Return ``{"count", "mean", "min", "max"}`` for samples.

    Contract (README): raises ValueError when samples is empty; count is an
    int; mean/min/max are floats.
    """
    count = len(samples)
    total = 0.0
    for value in samples:
        total += float(value)
    return {
        "count": count,
        "mean": total / count,
        "min": float(min(samples)),
        "max": float(max(samples)),
    }


def stdev(samples: Sequence[float]) -> float:
    """Population standard deviation of samples.

    Contract (README): raises ValueError when samples is empty; a single
    sample has stdev 0.0.
    """
    if not samples:
        raise ValueError("samples must be non-empty")
    values = [float(value) for value in samples]
    mean = sum(values) / len(values)
    variance = sum((value - mean) ** 2 for value in values) / len(values)
    return math.sqrt(variance)


def merge_summaries(*summaries: dict) -> dict:
    """Combine summary dicts (as produced by summarize) into one.

    Contract (README): count/mean combine exactly; min/max are the extremes
    across every input. With no inputs, the result is count 0, mean 0.0,
    min +inf, max -inf (an empty summary).
    """
    count = 0
    total = 0.0
    minimum = math.inf
    maximum = -math.inf
    for stats in summaries:
        count += int(stats["count"])
        total += float(stats["mean"]) * int(stats["count"])
        minimum = min(minimum, float(stats["min"]))
        maximum = max(maximum, float(stats["max"]))
    mean = total / count if count else 0.0
    return {"count": count, "mean": mean, "min": minimum, "max": maximum}
