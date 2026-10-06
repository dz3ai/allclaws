"""metricslite — tiny stdlib-only metrics helpers.

Public API (see README.md for the full contract):

- percentiles:  percentile, median, percentile_rank
- rolling:      RollingMean, RollingPeak
- counters:     Counter
- timers:       Timer, measure, human_duration
- summary:      summarize, stdev, merge_summaries
- cli:          python -m metricslite.cli summarize|percentile
"""

from __future__ import annotations

from .counters import Counter
from .percentiles import median, percentile, percentile_rank
from .rolling import RollingMean, RollingPeak
from .summary import merge_summaries, stdev, summarize
from .timers import Timer, human_duration, measure

__all__ = [
    "Counter",
    "RollingMean",
    "RollingPeak",
    "Timer",
    "human_duration",
    "measure",
    "median",
    "merge_summaries",
    "percentile",
    "percentile_rank",
    "stdev",
    "summarize",
]

__version__ = "1.0.0"
