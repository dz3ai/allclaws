"""Token -> USD cost model + cumulative spend ledger (plan: budget ceiling).

Pricing table: USD per 1M tokens, list price. Re-check before live batches.

The ledger is a JSON file at <results_root>/spend_ledger.json. The runner
consults it before EVERY launch: if cumulative spend + this run's cap would
exceed the ceiling, the grid aborts with a clear message (hard stop per plan).
"""

from __future__ import annotations

import json
import time
from dataclasses import dataclass
from pathlib import Path

BUDGET_CEILING_USD = 150.0  # plan: total ceiling ~$150 / ¥1000, hard stop

# USD per 1M tokens (input, output). List prices; update before live runs.
PRICING = {
    # domestic statistical cohort
    "glm-4.7": (0.14, 0.56),
    "glm-4.5-air": (0.14, 0.56),
    "deepseek-chat": (0.27, 1.10),
    "deepseek-reasoner": (0.55, 2.19),
    # frontier spot-check tier
    "gpt-5.2": (1.25, 10.00),
    "gpt-5.2-codex": (1.25, 10.00),
    "claude-sonnet-4.6": (3.00, 15.00),
    "sonnet": (3.00, 15.00),
    # unknown fallback (conservative mid domestic)
    "_default": (0.30, 1.20),
}

KNOWN_MODELS = sorted(k for k in PRICING if k != "_default")


@dataclass
class LedgerEntry:
    timestamp: float
    platform: str
    task_id: str
    model: str
    tokens_in: int
    tokens_out: int
    cost_usd: float


def usd_cost(model: str, tokens_in: int, tokens_out: int) -> float:
    """Cost of one run from token counts. Unknown models use _default rates."""
    rate_in, rate_out = PRICING.get(model, PRICING["_default"])
    return (tokens_in / 1e6) * rate_in + (tokens_out / 1e6) * rate_out


class SpendLedger:
    """Cumulative spend tracker with hard ceiling enforcement."""

    def __init__(self, path: Path, ceiling: float = BUDGET_CEILING_USD):
        self.path = Path(path)
        self.ceiling = ceiling
        self.entries: list[LedgerEntry] = []
        self._load()

    def _load(self) -> None:
        if self.path.is_file():
            try:
                raw = json.loads(self.path.read_text(encoding="utf-8"))
                self.entries = [LedgerEntry(**e) for e in raw.get("entries", [])]
            except (json.JSONDecodeError, TypeError):
                self.entries = []

    def total_usd(self) -> float:
        return round(sum(e.cost_usd for e in self.entries), 4)

    def remaining_budget(self) -> float:
        return round(self.ceiling - self.total_usd(), 4)

    def check_run_allowed(self, cost_cap_usd: float) -> tuple[bool, str]:
        """Hard stop: refuse when current spend + next-run cap exceeds ceiling."""
        remaining = self.remaining_budget()
        if remaining <= 0:
            return False, f"budget exhausted ({self.total_usd():.2f}$ spent, ceiling {self.ceiling}$)"
        if remaining < cost_cap_usd:
            return False, (
                f"remaining budget {remaining:.2f}$ < run cap {cost_cap_usd:.2f}$ "
                f"({self.total_usd():.2f}$ spent of {self.ceiling}$)"
            )
        return True, "ok"

    def record(
        self, platform: str, task_id: str, model: str, tokens_in: int, tokens_out: int
    ) -> LedgerEntry:
        entry = LedgerEntry(
            timestamp=time.time(),
            platform=platform,
            task_id=task_id,
            model=model,
            tokens_in=int(tokens_in or 0),
            tokens_out=int(tokens_out or 0),
            cost_usd=round(usd_cost(model, tokens_in or 0, tokens_out or 0), 4),
        )
        self.entries.append(entry)
        self._save()
        return entry

    def _save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "ceiling_usd": self.ceiling,
            "total_usd": self.total_usd(),
            "updated": time.strftime("%Y-%m-%dT%H-%M-%S"),
            "entries": [e.__dict__ for e in self.entries],
        }
        self.path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
