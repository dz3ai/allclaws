"""HIDDEN acceptance suite for triage-burndown (mounted at scoring time only).

One check-group per issue (1-5), each STRONGER than the fixture's visible
bug test: exact corrected behavior plus regression checks on green paths.
The suite FAILS as a whole on the pristine fixture (one group per unfixed
issue) and PASSES only when all five issues are fixed. Runs with cwd = the
agent's worktree root.
"""

import time
from unittest import mock

import pytest

from metricslite import Counter, RollingMean, Timer, measure, median, percentile, summarize


class TestIssue001Percentile:
    def test_interpolation_exact(self):
        assert percentile([10, 20], 50) == pytest.approx(15.0)
        assert percentile([10, 20, 30, 40], 25) == pytest.approx(17.5)
        assert percentile([10, 20, 30, 40], 50) == pytest.approx(25.0)
        assert percentile([10, 20, 30, 40], 75) == pytest.approx(32.5)

    def test_endpoints_are_exact_min_max(self):
        assert percentile([10, 20, 30], 0) == pytest.approx(10.0)
        assert percentile([10, 20, 30], 100) == pytest.approx(30.0)

    def test_median_matches_percentile_50(self):
        samples = [9.0, 1.0, 5.0]
        assert median(samples) == pytest.approx(percentile(samples, 50))
        assert median(samples) == pytest.approx(5.0)

    def test_single_element_regression(self):
        assert percentile([42.0], 37) == pytest.approx(42.0)


class TestIssue002RollingDefault:
    def test_default_window_is_five(self):
        r = RollingMean()
        assert r.window == 5
        for value in (1, 2, 3, 4, 5):
            r.add(value)
        assert r.mean() == pytest.approx(3.0)
        r.add(6)
        assert r.mean() == pytest.approx(4.0)

    def test_explicit_window_regression(self):
        r = RollingMean(window=3)
        for value in (1, 2, 3, 4, 5):
            r.add(value)
        assert r.mean() == pytest.approx(4.0)
        assert r.window == 3

    def test_empty_and_partial_regression(self):
        assert RollingMean().mean() == 0.0
        r = RollingMean()
        r.add(10)
        assert r.mean() == pytest.approx(10.0)


class TestIssue003SummaryValidation:
    def test_empty_raises_value_error(self):
        with pytest.raises(ValueError):
            summarize([])

    def test_exact_stats_regression(self):
        assert summarize([1, 2, 3]) == {
            "count": 3,
            "mean": 2.0,
            "min": 1.0,
            "max": 3.0,
        }

    def test_single_element_regression(self):
        assert summarize([7.5])["count"] == 1
        assert summarize([7.5])["mean"] == pytest.approx(7.5)


class TestIssue004CounterCaseInsensitive:
    def test_case_insensitive_matrix(self):
        c = Counter()
        c.inc("Error")
        assert c.get("error") == 1
        assert c.get("ERROR") == 1
        assert c.get("Error") == 1
        c.inc("error", by=2)
        c.inc("ERROR")
        assert c.get("Error") == 4
        assert c.total() == 4
        assert c.keys() == ["error"]

    def test_canonical_keys_sorted(self):
        c = Counter()
        c.inc("Warnings", by=2)
        c.inc("INFO")
        assert c.keys() == ["info", "warnings"]

    def test_same_case_regression(self):
        c = Counter()
        c.inc("hits", by=3)
        assert c.get("hits") == 3
        assert Counter().get("nope") == 0


class TestIssue005TimerMonotonic:
    def test_immune_to_wall_clock_steps(self):
        fake = {"now": 2_000_000.0}

        def stepping_time():
            fake["now"] -= 100.0
            return fake["now"]

        with mock.patch("time.time", stepping_time):
            t = Timer()
            t.start()
            time.sleep(0.02)
            elapsed = t.stop()
        assert 0.0 <= elapsed < 1.0
        assert t.elapsed == elapsed

    def test_normal_timing_regression(self):
        t = Timer()
        t.start()
        time.sleep(0.02)
        elapsed = t.stop()
        assert 0.0 < elapsed < 1.0

    def test_error_paths_and_measure_regression(self):
        t = Timer()
        with pytest.raises(RuntimeError):
            t.stop()
        with pytest.raises(RuntimeError):
            t.elapsed
        with mock.patch("time.time", lambda: 500.0):
            with measure() as timed:
                time.sleep(0.01)
        assert 0.0 <= timed.elapsed < 1.0
