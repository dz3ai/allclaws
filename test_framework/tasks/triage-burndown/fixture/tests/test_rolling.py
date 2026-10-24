"""Green-path tests for metricslite.rolling."""

import pytest

from metricslite import RollingMean, RollingPeak


class TestRollingMean:
    def test_explicit_window_evicts_oldest(self):
        r = RollingMean(window=3)
        for value in (1, 2, 3, 4, 5):
            r.add(value)
        assert r.mean() == 4.0

    def test_window_of_one_tracks_last_value(self):
        r = RollingMean(window=1)
        r.add(5)
        assert r.mean() == 5.0
        r.add(9)
        assert r.mean() == 9.0

    def test_fewer_than_window_averages_partial(self):
        r = RollingMean(window=10)
        r.add(1)
        r.add(2)
        assert r.mean() == 1.5

    def test_empty_mean_is_zero(self):
        assert RollingMean(window=4).mean() == 0.0

    def test_len_tracks_samples_in_window(self):
        r = RollingMean(window=2)
        assert len(r) == 0
        r.add(1)
        r.add(2)
        assert len(r) == 2
        r.add(3)
        assert len(r) == 2

    def test_window_property(self):
        assert RollingMean(window=7).window == 7

    def test_invalid_window_rejected(self):
        with pytest.raises(ValueError):
            RollingMean(window=0)

    def test_last_and_full(self):
        r = RollingMean(window=2)
        assert r.last() is None
        assert r.full() is False
        r.add(4)
        assert r.last() == 4.0
        assert r.full() is False
        r.add(6)
        assert r.full() is True
        assert r.last() == 6.0


class TestRollingPeak:
    def test_peak_tracks_maximum_in_window(self):
        p = RollingPeak(window=3)
        assert p.peak() is None
        for value in (3, 9, 1, 5):
            p.add(value)
        # window now holds 9, 1, 5
        assert p.peak() == 9.0
        p.add(2)
        p.add(0)
        # window now holds 1, 5, 2 -> peak 5 (9 was evicted)
        assert p.peak() == 5.0

    def test_window_guard(self):
        with pytest.raises(ValueError):
            RollingPeak(window=0)

    def test_len(self):
        p = RollingPeak(window=5)
        p.add(1)
        assert len(p) == 1
