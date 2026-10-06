# Issue 002: RollingMean default window is 3, documented default is 5

The README contract says `RollingMean(window: int = 5)` — the window
defaults to 5 samples. The constructor currently defaults to 3, so callers
who rely on the documented default get a mean over the wrong number of
samples. Example: after `add(1)..add(5)`, `mean()` must be `3.0` (mean of
all five), not `4.0` (mean of the last three). Align the default with the
documented contract.

Repro:

```
/usr/bin/python3 -m pytest tests/test_issue_002.py -q
```

Test: `tests/test_issue_002.py`.
