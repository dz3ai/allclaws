# Issue 003: summarize([]) raises ZeroDivisionError instead of ValueError

The README contract says `summarize` raises `ValueError` when called with
an empty sample list. There is no input validation, so the division inside
the mean computation leaks a raw `ZeroDivisionError` to callers instead.
Callers are told to catch `ValueError`; make `summarize` validate its input
and raise the documented error type.

Repro:

```
/usr/bin/python3 -m pytest tests/test_issue_003.py -q
```

Test: `tests/test_issue_003.py`.
