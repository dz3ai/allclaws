"""Documented-red test for issue-001 (percentile rank off-by-one, no interpolation).

Red on the pristine fixture BY DESIGN. Green once issue-001 is fixed.
Repro: /usr/bin/python3 -m pytest tests/test_issue_001.py -q
"""

from metricslite import percentile


def test_percentile_interpolates_between_ranks():
    # p50 of four samples lands between the two middle values: (30 + 20) / 2
    assert percentile([10, 20, 30, 40], 50) == 25.0
