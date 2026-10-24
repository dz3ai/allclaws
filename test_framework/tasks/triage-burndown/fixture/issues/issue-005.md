# Issue 005: Timer uses the wall clock, contract promises a monotonic clock

The README contract says `Timer` measures elapsed time with a MONOTONIC
clock, so results are immune to system wall-clock adjustments (NTP steps,
manual time changes). The implementation reads `time.time()` (wall clock),
so if the system clock is stepped between `start()` and `stop()`, the
reported elapsed time is wrong — it can even come out negative. Example:
with the wall clock stepped back 100 seconds mid-measurement, `stop()`
reports about `-100.0` instead of the real elapsed time. Switch both clock
reads to a monotonic time source.

Repro:

```
/usr/bin/python3 -m pytest tests/test_issue_005.py -q
```

Test: `tests/test_issue_005.py`.
