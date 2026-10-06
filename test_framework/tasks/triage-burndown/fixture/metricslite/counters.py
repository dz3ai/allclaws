"""Named counter registry with case-insensitive keys."""

from __future__ import annotations


class Counter:
    """Mapping of event names to running totals.

    Contract (README): keys are CASE-INSENSITIVE — ``inc("Error")`` and
    ``get("error")`` address the same bucket; ``keys()`` reports the
    canonical (lowercase) spellings, sorted.
    """

    def __init__(self) -> None:
        self._counts: dict[str, int] = {}

    def inc(self, key: str, by: int = 1) -> None:
        """Add ``by`` to the bucket named by ``key`` (creating it if needed)."""
        self._counts[key] = self._counts.get(key, 0) + by

    def get(self, key: str) -> int:
        """Current total for ``key`` (0 for a bucket never incremented)."""
        return self._counts.get(key, 0)

    def merge(self, other: "Counter") -> None:
        """Add every bucket of ``other`` into this counter."""
        for key, value in other._counts.items():
            self.inc(key, by=value)

    def total(self) -> int:
        """Sum over every bucket."""
        return sum(self._counts.values())

    def keys(self) -> list[str]:
        """Sorted list of canonical (lowercase) bucket names."""
        return sorted(self._counts)

    def as_dict(self) -> dict[str, int]:
        """Copy of the buckets keyed by canonical (lowercase) name."""
        return dict(self._counts)
