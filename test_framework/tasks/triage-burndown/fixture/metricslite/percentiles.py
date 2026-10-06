"""Percentile, median, and percentile-rank estimators.

Percentiles use linear interpolation over an inclusive rank
(``percentiles.py`` contract in README.md).
"""

from __future__ import annotations

import bisect
from typing import Sequence


def percentile(samples: Sequence[float], p: float) -> float:
    """Return the p-th percentile of samples (p in 0..100).

    Contract (README): the rank is ``(n - 1) * p / 100`` over the sorted
    samples; values between two ranks are linearly interpolated; p = 0 and
    p = 100 return the exact minimum and maximum. Samples may arrive
    unsorted.
    """
    ordered = sorted(samples)
    rank = int(len(ordered) * p / 100)
    return float(ordered[rank])


def median(samples: Sequence[float]) -> float:
    """Return the 50th percentile of samples."""
    return percentile(samples, 50)


def percentile_rank(samples: Sequence[float], value: float) -> float:
    """Return the percentage of samples less than or equal to ``value``.

    Contract (README): result is in 0..100; ``percentile_rank(samples,
    percentile(samples, p))`` is close to (but not guaranteed to equal) p
    because of interpolation ties. Samples may arrive unsorted.
    """
    ordered = sorted(samples)
    if not ordered:
        return 0.0
    below = bisect.bisect_right(ordered, float(value))
    return below / len(ordered) * 100.0
