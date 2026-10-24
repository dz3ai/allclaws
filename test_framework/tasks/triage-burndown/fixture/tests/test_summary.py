"""Green-path tests for metricslite.summary."""

import math

import pytest

from metricslite import merge_summaries, stdev, summarize


class TestSummarize:
    def test_exact_stats(self):
        assert summarize([1, 2, 3]) == {
            "count": 3,
            "mean": 2.0,
            "min": 1.0,
            "max": 3.0,
        }

    def test_single_element(self):
        assert summarize([4.5]) == {
            "count": 1,
            "mean": 4.5,
            "min": 4.5,
            "max": 4.5,
        }

    def test_float_samples(self):
        stats = summarize([0.5, 1.5])
        assert stats["count"] == 2
        assert stats["mean"] == pytest.approx(1.0)
        assert stats["min"] == pytest.approx(0.5)
        assert stats["max"] == pytest.approx(1.5)

    def test_count_is_int(self):
        assert isinstance(summarize([1, 2])["count"], int)


class TestStdev:
    def test_two_samples(self):
        assert stdev([2, 6]) == pytest.approx(2.0)

    def test_classic_set(self):
        assert stdev([2, 4, 4, 4, 5, 5, 7, 9]) == pytest.approx(2.0)

    def test_single_sample_is_zero(self):
        assert stdev([5.0]) == 0.0

    def test_empty_rejected(self):
        with pytest.raises(ValueError):
            stdev([])


class TestMergeSummaries:
    def test_combines_count_weighted_mean(self):
        a = summarize([1, 2, 3])   # mean 2.0
        b = summarize([10, 20])    # mean 15.0
        merged = merge_summaries(a, b)
        assert merged["count"] == 5
        assert merged["mean"] == pytest.approx(7.2)
        assert merged["min"] == pytest.approx(1.0)
        assert merged["max"] == pytest.approx(20.0)

    def test_no_inputs_is_empty_summary(self):
        merged = merge_summaries()
        assert merged["count"] == 0
        assert math.isinf(merged["min"]) and merged["min"] > 0
        assert math.isinf(merged["max"]) and merged["max"] < 0
