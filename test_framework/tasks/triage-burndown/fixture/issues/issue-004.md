# Issue 004: Counter keys are case-sensitive, API promises case-insensitive

The README contract says `Counter` keys are case-insensitive: `inc("Error")`
and `get("error")` must address the same bucket, and `keys()` reports the
canonical (lowercase) spellings. The implementation stores and looks up the
raw key string, so `inc("Error")` followed by `get("error")` returns `0`,
and mixed-case increments create duplicate buckets. Normalize keys so the
documented case-insensitive contract holds.

Repro:

```
/usr/bin/python3 -m pytest tests/test_issue_004.py -q
```

Test: `tests/test_issue_004.py`.
