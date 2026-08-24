# Bug: /users/<id> status code for missing users + case-sensitive search

## Summary

Two related defects shipped in the v1.0 endpoint layer:

1. **`GET /users/<id>` returns `200` for a missing user.** The README API
   contract says a nonexistent id must produce `404`, but the handler sends
   a JSON error body with a `200` status line. API clients retry forever
   instead of giving up.

2. **`GET /items?search=q` is case-sensitive.** The documented behavior is
   case-insensitive substring matching over item names, but the current
   implementation matches case-sensitively, so searching `widget` finds
   nothing when items are named `Widget`. The implementation also loops
   over each search keyword for every item in a way that makes the cost
   quadratic; while you are in there, make the scan linear.

## Steps to reproduce

```
/usr/bin/python3 -m pytest tests/ -q
```

Two tests fail: `test_get_missing_user_returns_404` and
`test_search_is_case_insensitive`.

## Expected behavior

- `GET /users/u-999999` → `404` with `{"error": ...}` body
- `GET /items?search=widget` matches items named `Widget`, `WIDGET`, etc.
- All other endpoints keep working exactly as documented in README.md

## Acceptance

- The full test suite passes without editing any test in `tests/`.
- No third-party dependencies are added.
