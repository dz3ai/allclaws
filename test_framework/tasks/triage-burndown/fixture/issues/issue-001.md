# Issue 001: percentile() skips interpolation and is off by one rank

The README contract says `percentile(samples, p)` uses rank
`(n - 1) * p / 100` with linear interpolation, and that `p = 0` / `p = 100`
return the exact min/max. The current implementation truncates the rank to
an int and indexes with `n` instead of `n - 1`, so mid-range percentiles
return a raw sample instead of the interpolated value (and `p = 100` can
even index out of range). Example: `percentile([10, 20], 50)` returns
`10.0` but must return `15.0`. Fix the rank computation and add the
interpolation step.

Repro:

```
/usr/bin/python3 -m pytest tests/test_issue_001.py -q
```

Test: `tests/test_issue_001.py`.
