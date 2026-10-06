# metricslite — tiny stdlib-only metrics helpers

A small dependency-free (stdlib-only) library of metrics primitives used for
bug-fixing exercises: percentiles, rolling means, counters, timers, and
summary stats, plus a tiny CLI.

## Public API contract (MUST NOT change)

All names below are exported from the `metricslite` package:

| Name | Signature | Behavior |
|---|---|---|
| `percentile` | `(samples, p: float) -> float` | p-th percentile (p in 0..100), linear interpolation over sorted samples with rank `(n-1) * p / 100`; `p=0`/`p=100` return the exact min/max; samples may be unsorted |
| `median` | `(samples) -> float` | 50th percentile |
| `percentile_rank` | `(samples, value) -> float` | percentage of samples <= value, in 0..100 |
| `RollingMean` | `(window: int = 5)` | mean over the last `window` samples; `window` defaults to **5**; `mean()` is `0.0` when empty; fewer samples than the window averages what is there |
| `RollingMean.add` | `(value) -> None` | record one sample, evicting the oldest once full |
| `RollingMean.mean` | `() -> float` | mean of the samples currently in the window |
| `RollingMean.last` / `.full` | | newest sample still in the window (None if empty) / True once exactly `window` samples are held |
| `RollingPeak` | `(window: int)` | max over the last `window` samples; `peak()` is None when empty |
| `Counter` | `()` | named buckets with **case-insensitive** keys: `inc("Error")` and `get("error")` address the same bucket; `keys()` lists canonical lowercase names, sorted |
| `Counter.inc` | `(key, by: int = 1) -> None` | add `by` to a bucket |
| `Counter.get` | `(key) -> int` | bucket total, `0` if never incremented |
| `Counter.merge` / `.total` / `.keys` / `.as_dict` | | add another counter's buckets / sum over buckets / sorted canonical names / dict copy |
| `Timer` | `()` | one-shot stopwatch measured with a **monotonic** clock (immune to wall-clock adjustments); `start()`, `stop() -> float`, `.elapsed`, `.running()`; double `start()`/`stop()` without `start()` raise `RuntimeError` |
| `measure` | `() -> context manager` | times the block; read `timer.elapsed` after exit |
| `human_duration` | `(seconds) -> str` | `"12.3s"` below a minute, `"4:05"` below an hour, `"1:02:03"` above; negative input raises ValueError |
| `summarize` | `(samples) -> dict` | `{"count": int, "mean": float, "min": float, "max": float}`; raises `ValueError` on empty input |
| `stdev` | `(samples) -> float` | population standard deviation; raises `ValueError` on empty input; single sample -> 0.0 |
| `merge_summaries` | `(*summaries) -> dict` | combine summarize() dicts (count-weighted mean, extreme min/max) |

## CLI

```
/usr/bin/python3 -m metricslite.cli summarize  --samples 1,2,3
/usr/bin/python3 -m metricslite.cli percentile --samples 1,2,3 --p 50
```

Both print a single JSON object.

## Open issues

The triage queue lives in `issues/` — `issue-001.md` … `issue-005.md`, to be
worked strictly in order. Each issue names the test in `tests/` that
documents it.

## Rules

- Do not edit or weaken any test in `tests/`.
- Keep the public API above unchanged (signatures + documented behavior).
- Python stdlib only; no third-party dependencies.
- Check with: `/usr/bin/python3 -m pytest tests/ -q`

## Layout

```
metricslite/
├── __init__.py      # public exports
├── percentiles.py   # percentile + median + percentile_rank
├── rolling.py       # RollingMean + RollingPeak
├── counters.py      # Counter
├── timers.py        # Timer + measure + human_duration
├── summary.py       # summarize + stdev + merge_summaries
└── cli.py           # argparse CLI
```
