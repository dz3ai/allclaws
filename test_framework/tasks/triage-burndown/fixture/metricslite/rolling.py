"""Rolling (windowed) statistics over the most recent samples."""

from __future__ import annotations

from collections.abc import Iterator


class RollingMean:
    """Arithmetic mean over the last ``window`` samples.

    Contract (README): the window defaults to 5 samples; ``mean()`` is 0.0
    before any sample arrives; with fewer samples than the window, mean()
    averages the samples seen so far.
    """

    def __init__(self, window: int = 3) -> None:
        if window < 1:
            raise ValueError("window must be >= 1")
        self._window = int(window)
        self._values: list[float] = []

    @property
    def window(self) -> int:
        """Size of the rolling window."""
        return self._window

    def add(self, value: float) -> None:
        """Record one sample, evicting the oldest once the window is full."""
        self._values.append(float(value))
        if len(self._values) > self._window:
            self._values.pop(0)

    def mean(self) -> float:
        """Mean over the samples currently inside the window (0.0 if empty)."""
        if not self._values:
            return 0.0
        return sum(self._values) / len(self._values)

    def last(self) -> float | None:
        """Most recent sample still inside the window (None if empty)."""
        return self._values[-1] if self._values else None

    def full(self) -> bool:
        """True once the window holds exactly ``window`` samples."""
        return len(self._values) == self._window

    def __len__(self) -> int:
        return len(self._values)

    def __iter__(self) -> Iterator[float]:
        return iter(self._values)


class RollingPeak:
    """Maximum over the last ``window`` samples.

    Contract (README): ``peak()`` is None before any sample arrives; the
    peak only ever considers samples still inside the window.
    """

    def __init__(self, window: int) -> None:
        if window < 1:
            raise ValueError("window must be >= 1")
        self._window = int(window)
        self._values: list[float] = []

    def add(self, value: float) -> None:
        """Record one sample, evicting the oldest once the window is full."""
        self._values.append(float(value))
        if len(self._values) > self._window:
            self._values.pop(0)

    def peak(self) -> float | None:
        """Largest sample currently inside the window (None if empty)."""
        return max(self._values) if self._values else None

    def __len__(self) -> int:
        return len(self._values)
