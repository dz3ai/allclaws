"""Task spec loading + validation for long-running benchmarks.

Spec files live at test_framework/tasks/<task-id>/spec.json with the layout:

    tasks/<task-id>/
    ├── spec.json              # this schema (machine-checkable task definition)
    ├── fixture/               # the repo template the agent works in (pristine,
    │                          #  never touched by runs; runner copies it to a
    │                          #  scratch dir and git-inits the copy)
    └── acceptance/            # hidden tests NOT visible to the agent; mounted
        │                      #  into the run copy at scoring time
        ├── test_*.py          # pytest acceptance tests
        ├── check*.py          # optional non-pytest checks (exit 0 = pass)
        └── reference_fix.patch  # git diff proving the fixture is solvable

Schema (keys mirror docs/reports/long-running-benchmark-research-plan.md):
    id, type, fixture_repo, task_prompt, timeout_minutes, max_turns,
    acceptance{method, command, pass_criteria}, cost_cap_usd
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

REQUIRED_KEYS = (
    "id",
    "type",
    "fixture_repo",
    "task_prompt",
    "timeout_minutes",
    "max_turns",
    "acceptance",
    "cost_cap_usd",
)

TASK_TYPES = (
    "github-issue",
    "multi-file-refactor",
    "feature-crud",
    "triage-burndown",
    "legacy-migrate",
)


class SpecError(ValueError):
    """Raised when a spec.json fails validation."""


@dataclass
class TaskSpec:
    id: str
    type: str
    fixture_repo: str
    task_prompt: str
    timeout_minutes: int
    max_turns: int
    acceptance: dict[str, str]
    cost_cap_usd: float
    task_dir: Path
    difficulty: str = ""
    notes: str = ""
    extra: dict[str, Any] = field(default_factory=dict)

    # ---- derived paths -------------------------------------------------
    @property
    def fixture_dir(self) -> Path:
        """Pristine repo template the agent works in (copied per run)."""
        return (self.task_dir / self.fixture_repo).resolve()

    @property
    def acceptance_dir(self) -> Path:
        """Hidden tests + reference fix (mounted at scoring time only)."""
        return self.task_dir / "acceptance"

    @property
    def timeout_seconds(self) -> int:
        return int(self.timeout_minutes * 60)

    # ---- serialization --------------------------------------------------
    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "type": self.type,
            "fixture_repo": self.fixture_repo,
            "task_prompt": self.task_prompt,
            "timeout_minutes": self.timeout_minutes,
            "max_turns": self.max_turns,
            "acceptance": self.acceptance,
            "cost_cap_usd": self.cost_cap_usd,
            "difficulty": self.difficulty,
            "notes": self.notes,
        }


def load_spec(path: Path) -> TaskSpec:
    """Load + validate a spec.json. Raises SpecError with a clear message."""
    path = Path(path).resolve()
    if not path.is_file():
        raise SpecError(f"spec not found: {path}")
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise SpecError(f"{path}: invalid JSON ({e})") from e

    missing = [k for k in REQUIRED_KEYS if k not in raw]
    if missing:
        raise SpecError(f"{path}: missing required keys: {', '.join(missing)}")

    acc = raw["acceptance"]
    for key in ("method", "command", "pass_criteria"):
        if key not in acc:
            raise SpecError(f"{path}: acceptance.{key} is required")

    if raw["type"] not in TASK_TYPES:
        raise SpecError(
            f"{path}: unknown type {raw['type']!r} (expected one of {TASK_TYPES})"
        )
    if not (1 <= int(raw["timeout_minutes"]) <= 240):
        raise SpecError(f"{path}: timeout_minutes out of range 1-240")
    if not (1 <= int(raw["max_turns"]) <= 2000):
        raise SpecError(f"{path}: max_turns out of range 1-2000")
    if not (0 < float(raw["cost_cap_usd"]) <= 10):
        raise SpecError(f"{path}: cost_cap_usd out of range (0, 10]")

    spec = TaskSpec(
        id=str(raw["id"]),
        type=str(raw["type"]),
        fixture_repo=str(raw["fixture_repo"]),
        task_prompt=str(raw["task_prompt"]),
        timeout_minutes=int(raw["timeout_minutes"]),
        max_turns=int(raw["max_turns"]),
        acceptance={k: str(v) for k, v in acc.items()},
        cost_cap_usd=float(raw["cost_cap_usd"]),
        task_dir=path.parent,
        difficulty=str(raw.get("difficulty", "")),
        notes=str(raw.get("notes", "")),
        extra={k: v for k, v in raw.items() if k not in REQUIRED_KEYS},
    )

    if not spec.fixture_dir.is_dir():
        raise SpecError(f"{path}: fixture dir does not exist: {spec.fixture_dir}")
    if not spec.acceptance_dir.is_dir():
        raise SpecError(f"{path}: acceptance dir does not exist: {spec.acceptance_dir}")
    return spec


def load_all_tasks(tasks_root: Path) -> list[TaskSpec]:
    """Load every tasks/<task-id>/spec.json under tasks_root (sorted by id)."""
    tasks_root = Path(tasks_root)
    specs = []
    for spec_path in sorted(tasks_root.glob("*/spec.json")):
        specs.append(load_spec(spec_path))
    return specs
