"""Documented-red test for issue-002 (RollingMean default window is 3, not 5).

Red on the pristine fixture BY DESIGN. Green once issue-002 is fixed.
Repro: /usr/bin/python3 -m pytest tests/test_issue_002.py -q
"""

from metricslite import RollingMean


def test_default_window_is_five():
    rolling = RollingMean()
    for value in (1, 2, 3, 4, 5):
        rolling.add(value)
    # window 5 -> mean(1..5) = 3.0 (window 3 would give mean(3,4,5) = 4.0)
    assert rolling.mean() == 3.0
