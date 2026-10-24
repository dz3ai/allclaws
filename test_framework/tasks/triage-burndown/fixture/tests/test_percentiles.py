"""Green-path tests for metricslite.percentiles."""

import pytest

from metricslite import median, percentile, percentile_rank


class TestPercentile:
    def test_zeroth_percentile_is_min(self):
        assert percentile([10, 20, 30], 0) == 10.0

    def test_median_of_three(self):
        assert percentile([10, 20, 30], 50) == 20.0

    def test_single_element_any_p(self):
        for p in (0, 37, 50):
            assert percentile([42.0], p) == 42.0

    def test_unsorted_input_is_sorted_internally(self):
        assert percentile([30, 10, 20], 50) == 20.0


class TestMedian:
    def test_single_element(self):
        assert median([7]) == 7.0

    def test_odd_length_unsorted(self):
        assert median([3, 1, 2]) == 2.0

    def test_matches_percentile_50(self):
        samples = [5.0, 1.0, 9.0, 3.0, 7.0]
        assert median(samples) == percentile(samples, 50)


class TestPercentileRank:
    def test_exact_buckets(self):
        samples = [10, 20, 30, 40]
        assert percentile_rank(samples, 10) == 25.0
        assert percentile_rank(samples, 30) == 75.0
        assert percentile_rank(samples, 40) == 100.0

    def test_below_and_above_range(self):
        samples = [10, 20, 30]
        assert percentile_rank(samples, 5) == 0.0
        assert percentile_rank(samples, 999) == 100.0

    def test_unsorted_input(self):
        assert percentile_rank([30, 10, 20], 20) == pytest.approx(66.666, abs=0.01)
