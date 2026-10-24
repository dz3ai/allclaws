"""Green-path tests for metricslite.timers."""

import time

import pytest

from metricslite import Timer, human_duration, measure


class TestTimer:
    def test_stop_returns_elapsed_seconds(self):
        t = Timer()
        t.start()
        time.sleep(0.01)
        elapsed = t.stop()
        assert 0.0 < elapsed < 1.0

    def test_elapsed_property_matches_stop(self):
        t = Timer()
        t.start()
        time.sleep(0.01)
        stopped = t.stop()
        assert t.elapsed == stopped

    def test_running_transitions(self):
        t = Timer()
        assert t.running() is False
        t.start()
        assert t.running() is True
        t.stop()
        assert t.running() is False

    def test_double_start_raises(self):
        t = Timer()
        t.start()
        with pytest.raises(RuntimeError):
            t.start()

    def test_stop_without_start_raises(self):
        with pytest.raises(RuntimeError):
            Timer().stop()

    def test_elapsed_before_stop_raises(self):
        with pytest.raises(RuntimeError):
            Timer().elapsed


class TestMeasure:
    def test_context_manager_records_elapsed(self):
        with measure() as timer:
            time.sleep(0.01)
        assert 0.0 < timer.elapsed < 1.0

    def test_context_stops_on_exception(self):
        with pytest.raises(RuntimeError):  # noqa: PT012 - single statement
            with measure() as timer:
                raise RuntimeError("boom")
        assert timer.elapsed >= 0.0


class TestHumanDuration:
    def test_below_a_minute(self):
        assert human_duration(0) == "0.0s"
        assert human_duration(45.25) == "45.2s"  # one decimal

    def test_below_an_hour(self):
        assert human_duration(60) == "1:00"
        assert human_duration(90) == "1:30"
        assert human_duration(600.4) == "10:00"

    def test_hours(self):
        assert human_duration(3600) == "1:00:00"
        assert human_duration(3671) == "1:01:11"

    def test_negative_rejected(self):
        with pytest.raises(ValueError):
            human_duration(-1)
