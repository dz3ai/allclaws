"""Documented-red test for issue-005 (Timer reads the wall clock, not monotonic).

Red on the pristine fixture BY DESIGN. Green once issue-005 is fixed.
Repro: /usr/bin/python3 -m pytest tests/test_issue_005.py -q
"""

import time
from unittest import mock

from metricslite import Timer


def test_timer_immune_to_wall_clock_steps():
    # Wall clock steps back 100s between the start() and stop() reads; the
    # monotonic contract says elapsed must stay a small positive value.
    fake = {"now": 1_000_000.0}

    def stepping_time():
        fake["now"] -= 100.0
        return fake["now"]

    with mock.patch("time.time", stepping_time):
        timer = Timer()
        timer.start()
        time.sleep(0.01)
        elapsed = timer.stop()

    assert 0.0 <= elapsed < 1.0
